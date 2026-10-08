# tests/test_planner_agent.py
"""Tests for PlannerAgent orchestration."""

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from src.agents.planner.agent import PlannerAgent
from src.agents.planner.parser import FOAParser
from src.types.application_plan import ApplicationPlan, SectionName


@pytest.fixture
def sample_pdf_path() -> Path:
    return Path(__file__).parent / "fixtures" / "sample_foa.pdf"


def test_planner_agent_with_pdf(sample_pdf_path):
    mock_parser = AsyncMock(spec=FOAParser)
    from src.types.application_plan import FOAMetadata, FormatRules, PageLimits

    mock_parser.parse.return_value = ApplicationPlan(
        foa_id="RFA-TEST-001",
        foa_title="Mock FOA",
        foa_metadata=FOAMetadata(
            foa_id="RFA-TEST-001",
            title="Mock FOA",
            release_date="",
            application_due_date="",
        ),
        project_title="Test Project",
        principal_investigator="Dr. Tester",
        institution="Test University",
        project_start_date="2026-07-01",
        project_end_date="2031-06-30",
        page_limits=PageLimits(),
        format_rules=FormatRules(),
    )

    agent = PlannerAgent(parser=mock_parser)
    plan = asyncio.run(
        agent.create_plan(
            foa_pdf=sample_pdf_path,
            project_title="Test Project",
            principal_investigator="Dr. Tester",
        )
    )

    assert isinstance(plan, ApplicationPlan)
    assert plan.foa_id == "RFA-TEST-001"
    assert len(plan.era_commons_checks) > 0


def test_planner_agent_with_foa_id():
    agent = PlannerAgent()
    plan = asyncio.run(
        agent.create_plan(
            foa_id="example",
            project_title="Config-driven Project",
            principal_investigator="Dr. Smith",
        )
    )

    assert isinstance(plan, ApplicationPlan)
    assert plan.foa_id == "example"
    assert plan.project_title == "Config-driven Project"
    assert plan.get_page_limit(SectionName.SPECIFIC_AIMS) == 1


def test_planner_agent_fallback_base():
    agent = PlannerAgent()
    plan = asyncio.run(
        agent.create_plan(
            project_title="Default NIH R01 Application",
            principal_investigator="Dr. Researcher",
        )
    )

    assert isinstance(plan, ApplicationPlan)
    assert plan.foa_id == "PA-20-185"
    assert plan.activity_code == "R01"
    assert plan.is_section_required(SectionName.SPECIFIC_AIMS) is True
