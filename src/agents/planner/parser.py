# src/agents/planner/parser.py
"""FOA PDF parser using PyMuPDF and Ollama LLM extraction."""

import logging
import re
from pathlib import Path
from typing import Any

import pymupdf

from src.llm.ollama_client import OllamaClient
from src.types.application_plan import (
    ApplicationPlan,
    BudgetRules,
    FOAMetadata,
    FormatRules,
    PageLimits,
    SectionSpec,
)
from src.types.common import SectionName

from .prompts import METADATA_PROMPT, PARSER_PROMPT

logger = logging.getLogger(__name__)


class FOAParser:
    """Extracts text from FOA PDFs and parses structured requirements via LLM."""

    def __init__(
        self,
        ollama: OllamaClient | None = None,
        model: str = "llama3.1:8b-instruct-q4_K_M",
    ):
        self.ollama = ollama or OllamaClient()
        self.model = model

    def extract_text(self, pdf_path: Path | str, max_pages: int = 200) -> str:
        """Extract text from a FOA PDF file."""
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"FOA PDF not found: {path}")

        # Guard against excessively large files (>50MB)
        if path.stat().st_size > 50 * 1024 * 1024:
            raise ValueError(f"FOA PDF exceeds maximum supported size of 50MB: {path}")

        doc = pymupdf.open(path)
        try:
            pages_text = []
            page_count = min(len(doc), max_pages)
            for i in range(page_count):
                page = doc[i]
                pages_text.append(page.get_text())
            return "\n\n".join(pages_text)
        finally:
            doc.close()

    def _fallback_metadata(self, text: str) -> dict[str, Any]:
        """Regex-based fallback extraction of FOA metadata."""
        foa_match = re.search(r"\b(RFA-[A-Z]{2}-\d{2}-\d{3}|PA-\d{2}-\d{3}|PAR-\d{2}-\d{3})\b", text)
        foa_id = foa_match.group(1) if foa_match else "R01-FOA-CUSTOM"

        title_match = re.search(r"Funding Opportunity Title[:\s]+([^\n]+)", text, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "NIH Research Project Grant"

        return {
            "foa_id": foa_id,
            "title": title,
            "agency": "NIH",
            "activity_code": "R01",
            "release_date": "",
            "application_due_date": "",
            "expiration_date": None,
            "description": "Standard NIH Funding Opportunity Announcement",
            "special_instructions": [],
            "contact_pi_eligible": True,
            "multiple_pi_allowed": True,
        }

    async def parse_metadata(self, text: str) -> FOAMetadata:
        """First pass: extract FOA metadata."""
        prompt = METADATA_PROMPT.replace("{foa_text}", text[:6000])
        try:
            data = await self.ollama.generate_json(self.model, prompt)
            return FOAMetadata(**data)
        except Exception as e:
            logger.warning(f"LLM metadata extraction failed ({e}), using fallback: {e}")
            fallback = self._fallback_metadata(text)
            return FOAMetadata(**fallback)

    async def parse_requirements(self, text: str) -> dict[str, Any]:
        """Second pass: extract page limits, format, and attachments."""
        prompt = PARSER_PROMPT.replace("{foa_text}", text[:15000])
        try:
            return await self.ollama.generate_json(self.model, prompt)
        except Exception as e:
            logger.warning(f"LLM requirements extraction failed ({e}), using defaults")
            return {
                "page_limits": {
                    "specific_aims": 1,
                    "research_strategy": 12,
                    "biosketch": 5,
                    "biosketch_supplement": 2,
                    "data_management_sharing": 2,
                },
                "required_attachments": [
                    {"name": "specific_aims", "required": True, "page_limit": 1},
                    {"name": "research_strategy", "required": True, "page_limit": 12},
                    {"name": "biosketch", "required": True, "page_limit": 5},
                    {"name": "budget_justification", "required": True, "page_limit": "no_limit"},
                ],
                "format_rules": {
                    "font_family": "Arial",
                    "font_size_pt": 11,
                    "margins_inches": 0.5,
                },
                "special_instructions": [],
                "budget_rules": {
                    "modular_budget_enabled": True,
                    "modular_budget_increment": 25000,
                    "modular_budget_max_direct_costs": 250000,
                },
            }

    async def parse(
        self,
        pdf_path: Path | str,
        project_title: str = "Research Project Grant",
        principal_investigator: str = "Principal Investigator",
        institution: str = "Research Institution",
        project_start_date: str = "2026-07-01",
        project_end_date: str = "2031-06-30",
    ) -> ApplicationPlan:
        """Parse FOA PDF into an ApplicationPlan."""
        text = self.extract_text(pdf_path)
        metadata = await self.parse_metadata(text)
        requirements = await self.parse_requirements(text)

        raw_page_limits = requirements.get("page_limits", {})
        page_limits = PageLimits(**raw_page_limits) if raw_page_limits else PageLimits()

        raw_format = requirements.get("format_rules", {})
        format_rules = FormatRules(**raw_format) if raw_format else FormatRules()

        raw_budget = requirements.get("budget_rules", {})
        budget_rules = BudgetRules(**raw_budget) if raw_budget else BudgetRules()

        # Build sections map
        sections: dict[SectionName, SectionSpec] = {}
        for sec in SectionName:
            sections[sec] = SectionSpec(
                name=sec,
                required=sec in [
                    SectionName.SPECIFIC_AIMS,
                    SectionName.RESEARCH_STRATEGY,
                    SectionName.BIOSKETCH,
                    SectionName.BUDGET_JUSTIFICATION,
                ],
                page_limit=getattr(page_limits, sec.value, "no_limit"),
                subsections=["significance", "innovation", "approach"] if sec == SectionName.RESEARCH_STRATEGY else [],
            )

        # Update required sections based on extracted attachments if present
        for att in requirements.get("required_attachments", []):
            att_name = att.get("name")
            try:
                sec_enum = SectionName(att_name)
                if sec_enum in sections:
                    sections[sec_enum].required = bool(att.get("required", True))
                    if "page_limit" in att:
                        sections[sec_enum].page_limit = att["page_limit"]
            except ValueError:
                pass

        return ApplicationPlan(
            foa_id=metadata.foa_id,
            foa_title=metadata.title,
            foa_metadata=metadata,
            project_title=project_title,
            principal_investigator=principal_investigator,
            institution=institution,
            project_start_date=project_start_date,
            project_end_date=project_end_date,
            sections=sections,
            page_limits=page_limits,
            format_rules=format_rules,
            budget_rules=budget_rules,
        )
