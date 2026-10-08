# tests/test_foa_parser.py
"""Tests for FOAParser extraction, fallback, and LLM parsing."""

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from src.agents.planner.parser import FOAParser
from src.llm.ollama_client import OllamaClient
from src.types.application_plan import ApplicationPlan


@pytest.fixture
def sample_pdf_path() -> Path:
    return Path(__file__).parent / "fixtures" / "sample_foa.pdf"


def test_extract_text_success(sample_pdf_path):
    parser = FOAParser()
    text = parser.extract_text(sample_pdf_path)
    assert "PA-20-185" in text
    assert "Research Project Grant" in text
    assert "Specific Aims" in text


def test_extract_text_missing_file(tmp_path):
    parser = FOAParser()
    with pytest.raises(FileNotFoundError):
        parser.extract_text(tmp_path / "does_not_exist.pdf")


def test_fallback_metadata(sample_pdf_path):
    parser = FOAParser()
    text = parser.extract_text(sample_pdf_path)
    metadata = parser._fallback_metadata(text)
    assert metadata["foa_id"] == "PA-20-185"
    assert metadata["agency"] == "NIH"


def test_parse_with_mock_llm(sample_pdf_path):
    mock_ollama = AsyncMock(spec=OllamaClient)
    mock_ollama.generate_json.side_effect = [
        # Pass 1: metadata
        {
            "foa_id": "PA-20-185",
            "title": "Research Project Grant (Parent R01)",
            "agency": "NIH",
            "activity_code": "R01",
            "release_date": "2020-05-08",
            "application_due_date": "2020-09-05",
            "description": "NIH parent R01 announcement",
            "special_instructions": [],
        },
        # Pass 2: requirements
        {
            "page_limits": {
                "specific_aims": 1,
                "research_strategy": 12,
                "biosketch": 5,
            },
            "required_attachments": [
                {"name": "specific_aims", "required": True, "page_limit": 1},
                {"name": "research_strategy", "required": True, "page_limit": 12},
                {"name": "biosketch", "required": True, "page_limit": 5},
            ],
            "format_rules": {
                "font_family": "Arial",
                "font_size_pt": 11,
                "margins_inches": 0.5,
            },
            "budget_rules": {
                "modular_budget_enabled": True,
                "modular_budget_increment": 25000,
                "modular_budget_max_direct_costs": 250000,
            },
        },
    ]

    parser = FOAParser(ollama=mock_ollama)
    plan = asyncio.run(
        parser.parse(
            sample_pdf_path,
            project_title="Neural Basis of Decision Making",
            principal_investigator="Dr. Jane Doe",
            institution="Stanford University",
        )
    )

    assert isinstance(plan, ApplicationPlan)
    assert plan.foa_id == "PA-20-185"
    assert plan.project_title == "Neural Basis of Decision Making"
    assert plan.principal_investigator == "Dr. Jane Doe"
    assert plan.page_limits.research_strategy == 12


def test_parse_fallback_when_ollama_offline(sample_pdf_path):
    mock_ollama = AsyncMock(spec=OllamaClient)
    mock_ollama.generate_json.side_effect = ConnectionError("Ollama offline")

    parser = FOAParser(ollama=mock_ollama)
    plan = asyncio.run(parser.parse(sample_pdf_path))

    assert isinstance(plan, ApplicationPlan)
    assert plan.foa_id == "PA-20-185"
    assert plan.page_limits.specific_aims == 1
    assert plan.page_limits.research_strategy == 12
