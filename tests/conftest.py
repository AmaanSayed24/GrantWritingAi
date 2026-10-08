# tests/conftest.py
"""Pytest fixtures for Grant Writing AI tests."""

from pathlib import Path

import pytest

from src.types import (
    ApplicationPlan,
    BiosketchFormat,
    BudgetRules,
    FOAConfig,
    FOAMetadata,
    FontFamily,
    FormatRules,
    GrantsConfig,
    LineSpacing,
    PageLimits,
    PageNumbering,
    PaperSize,
    SectionName,
    SectionSpec,
)


@pytest.fixture
def sample_page_limits() -> PageLimits:
    """Sample PageLimits for testing."""
    return PageLimits(
        specific_aims=1,
        research_strategy=12,
        biosketch=5,
        biosketch_supplement=2,
        budget_justification="no_limit",
        facilities_resources="no_limit",
        equipment="no_limit",
        data_management_sharing=2,
        authentication_key_biological_resources=1,
        human_subjects_protection="no_limit",
        vertebrate_animals="no_limit",
        select_agent_research=1,
        multiple_pi_leadership_plan=3,
        consortium_contractual="no_limit",
        letters_of_support="no_limit",
        resource_sharing_plan=1,
    )


@pytest.fixture
def sample_format_rules() -> FormatRules:
    """Sample FormatRules for testing."""
    return FormatRules(
        font_family=FontFamily.ARIAL,
        font_size_pt=11,
        margins_inches=0.5,
        line_spacing=LineSpacing.SINGLE,
        page_numbering=PageNumbering.BOTTOM_RIGHT,
        headers=True,
        header_format="PI Last Name / Project Title / Page X of Y",
        paper_size=PaperSize.LETTER,
    )


@pytest.fixture
def sample_budget_rules() -> BudgetRules:
    """Sample BudgetRules for testing."""
    return BudgetRules(
        modular_budget_enabled=True,
        modular_budget_increment=25000,
        modular_budget_max_direct_costs=250000,
        pi_minimum_effort_pct=30,
        co_investigator_minimum_effort_pct=10,
        max_total_effort_pct=100,
        equipment_threshold_usd=5000,
        equipment_requires_justification_above=True,
        foreign_travel_requires_approval=True,
        domestic_conference_max_per_year=2,
        consortium_f_and_a_on_first_25k_only=True,
    )


@pytest.fixture
def sample_foa_metadata() -> FOAMetadata:
    """Sample FOAMetadata for testing."""
    return FOAMetadata(
        foa_id="RFA-EX-001",
        title="Test FOA",
        agency="NIH",
        activity_code="R01",
        release_date="2026-01-01",
        application_due_date="2026-06-01",
        description="Test FOA for unit tests",
        special_instructions=["Test instruction"],
    )


@pytest.fixture
def sample_application_plan(
    sample_page_limits: PageLimits,
    sample_format_rules: FormatRules,
    sample_budget_rules: BudgetRules,
    sample_foa_metadata: FOAMetadata,
) -> ApplicationPlan:
    """Sample ApplicationPlan for testing."""
    sections = {}
    for section_name in SectionName:
        sections[section_name] = SectionSpec(
            name=section_name,
            required=section_name in [
                SectionName.SPECIFIC_AIMS,
                SectionName.RESEARCH_STRATEGY,
                SectionName.BIOSKETCH,
                SectionName.BUDGET_JUSTIFICATION,
                SectionName.DATA_MANAGEMENT_SHARING,
                SectionName.AUTHENTICATION_KEY_BIOLOGICAL_RESOURCES,
            ],
            page_limit=getattr(sample_page_limits, section_name.value, "no_limit"),
        )
    
    return ApplicationPlan(
        foa_id="RFA-EX-001",
        foa_title="Test FOA",
        foa_metadata=sample_foa_metadata,
        project_title="Test Project",
        principal_investigator="Dr. Test PI",
        institution="Test University",
        project_start_date="2026-07-01",
        project_end_date="2031-06-30",
        sections=sections,
        page_limits=sample_page_limits,
        format_rules=sample_format_rules,
        budget_rules=sample_budget_rules,
        biosketch_format=BiosketchFormat.COMMON_FORM_2026,
        biosketch_supplement_required=True,
        validation={
            "check_page_limits": True,
            "check_font": True,
            "check_margins": True,
            "check_line_spacing": True,
            "check_page_numbering": True,
            "check_headers": True,
            "check_required_sections": True,
            "check_budget_rules": True,
            "check_cross_section_consistency": True,
            "check_biosketch_format": True,
            "check_biosketch_page_limit": True,
        },
        era_commons_checks=[
            "Page limits per attachment",
            "Font size and type",
            "Margins",
        ],
    )


@pytest.fixture
def sample_grants_config() -> GrantsConfig:
    """Sample GrantsConfig for testing."""
    return GrantsConfig(
        page_limits=PageLimits(),
        format=FormatRules(),
        sections={
            "required": [
                "specific_aims",
                "research_strategy",
                "biosketch",
                "budget_justification",
            ],
            "research_strategy_subsections": [
                "significance",
                "innovation",
                "approach",
            ],
            "biosketch_format": "2026_common_form",
            "biosketch_supplement_required": True,
        },
        budget_rules=BudgetRules(),
        fonts={
            "allowed": ["Arial", "Helvetica", "Georgia", "Palatino Linotype"],
            "default": "Arial",
            "minimum_size_pt": 11,
        },
        page_margins={
            "top": 0.5,
            "bottom": 0.5,
            "left": 0.5,
            "right": 0.5,
        },
        validation={
            "check_page_limits": True,
            "check_font": True,
            "check_margins": True,
            "check_line_spacing": True,
            "check_page_numbering": True,
            "check_headers": True,
            "check_required_sections": True,
            "check_budget_rules": True,
            "check_cross_section_consistency": True,
            "check_biosketch_format": True,
            "check_biosketch_page_limit": True,
        },
        era_commons_checks=[
            "Page limits per attachment",
            "Font size and type",
            "Margins",
        ],
    )


@pytest.fixture
def sample_foa_config() -> FOAConfig:
    """Sample FOAConfig for testing."""
    return FOAConfig(
        foa_id="RFA-TEST-001",
        title="Test FOA Override",
        agency="NIH",
        activity_code="R01",
        release_date="2026-01-01",
        application_due_date="2026-06-01",
        description="Test FOA with overrides",
        special_instructions=["FOA-specific instruction"],
        page_limits={
            "specific_aims": 1,
            "research_strategy": 6,  # Override: 6 pages instead of 12
            "biosketch": 5,
        },
        format={
            "font_size_pt": 11,
            "margins_inches": 0.5,
        },
        sections={
            "required": [
                "specific_aims",
                "research_strategy",
                "biosketch",
                "budget_justification",
                "data_management_sharing",
            ],
            "research_strategy_subsections": [
                "significance",
                "innovation",
                "approach",
            ],
            "biosketch_format": "2026_common_form",
            "biosketch_supplement_required": True,
        },
    )


@pytest.fixture
def config_dir() -> Path:
    """Path to config directory."""
    return Path(__file__).parent.parent / "config"


@pytest.fixture
def grants_yaml_path(config_dir: Path) -> Path:
    """Path to grants.yaml."""
    return config_dir / "grants.yaml"