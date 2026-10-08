# src/agents/planner/agent.py
"""Planner Agent for establishing ApplicationPlan from FOA PDF and configuration."""

from pathlib import Path

from src.config.loader import load_foa_config, load_grants_config
from src.types.application_plan import ApplicationPlan

from .parser import FOAParser


class PlannerAgent:
    """Agent that produces a validated ApplicationPlan from FOA inputs and rules."""

    def __init__(self, parser: FOAParser | None = None):
        self.parser = parser or FOAParser()

    async def create_plan(
        self,
        foa_pdf: Path | str | None = None,
        foa_id: str | None = None,
        project_title: str = "Research Project Grant",
        principal_investigator: str = "Principal Investigator",
        institution: str = "Research Institution",
        project_start_date: str = "2026-07-01",
        project_end_date: str = "2031-06-30",
    ) -> ApplicationPlan:
        """
        Create a validated ApplicationPlan.

        Either parses a FOA PDF or loads a FOA/base configuration.
        """
        base_config = load_grants_config()

        if foa_pdf:
            # Parse directly from PDF
            plan = await self.parser.parse(
                pdf_path=foa_pdf,
                project_title=project_title,
                principal_investigator=principal_investigator,
                institution=institution,
                project_start_date=project_start_date,
                project_end_date=project_end_date,
            )
            # Inherit ERA Commons checks from base config if empty
            if not plan.era_commons_checks:
                plan.era_commons_checks = list(base_config.era_commons_checks)
            return plan

        if foa_id:
            # Load and merge specific FOA config
            merged = load_foa_config(foa_id, base_config)
            return merged.to_application_plan(
                project_title=project_title,
                principal_investigator=principal_investigator,
                institution=institution,
                project_start_date=project_start_date,
                project_end_date=project_end_date,
            )

        # Fallback to base configuration
        return base_config.to_application_plan_base(
            foa_id="PA-20-185",
            foa_title="NIH Parent R01",
            project_title=project_title,
            principal_investigator=principal_investigator,
            institution=institution,
            project_start_date=project_start_date,
            project_end_date=project_end_date,
        )
