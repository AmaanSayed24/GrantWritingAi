# tests/test_types.py
"""Unit tests for core Pydantic data models."""

import pytest
from pydantic import ValidationError

from src.types import (
    ActivityCode,
    ApplicationPlan,
    AttachmentSpec,
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
    deep_merge,
    merge_lists_unique,
)


class TestEnums:
    """Test enum values."""

    def test_activity_code_values(self):
        assert ActivityCode.R01 == "R01"
        assert ActivityCode.R21 == "R21"
        assert ActivityCode.K08 == "K08"

    def test_section_name_values(self):
        assert SectionName.SPECIFIC_AIMS == "specific_aims"
        assert SectionName.RESEARCH_STRATEGY == "research_strategy"
        assert SectionName.BIOSKETCH == "biosketch"

    def test_biosketch_format_values(self):
        assert BiosketchFormat.COMMON_FORM_2026 == "2026_common_form"
        assert BiosketchFormat.LEGACY == "legacy"

    def test_font_family_values(self):
        assert FontFamily.ARIAL == "Arial"
        assert FontFamily.HELVETICA == "Helvetica"

    def test_line_spacing_values(self):
        assert LineSpacing.SINGLE == "single"
        assert LineSpacing.ONE_AND_HALF == "1.5"

    def test_page_numbering_values(self):
        assert PageNumbering.BOTTOM_RIGHT == "bottom-right"
        assert PageNumbering.TOP_CENTER == "top-center"

    def test_paper_size_values(self):
        assert PaperSize.LETTER == "letter"
        assert PaperSize.A4 == "a4"


class TestPageLimits:
    """Test PageLimits model."""

    def test_default_page_limits(self):
        limits = PageLimits()
        assert limits.specific_aims == 1
        assert limits.research_strategy == 12
        assert limits.biosketch == 5
        assert limits.budget_justification == "no_limit"

    def test_custom_page_limits(self):
        limits = PageLimits(
            specific_aims=2,
            research_strategy=6,
            biosketch=4,
        )
        assert limits.specific_aims == 2
        assert limits.research_strategy == 6
        assert limits.biosketch == 4

    def test_page_limits_validation_ge(self):
        with pytest.raises(ValidationError):
            PageLimits(specific_aims=0)  # must be >= 1
        
        with pytest.raises(ValidationError):
            PageLimits(research_strategy=0)

    def test_page_limits_validation_le(self):
        with pytest.raises(ValidationError):
            PageLimits(specific_aims=6)  # must be <= 5
        
        with pytest.raises(ValidationError):
            PageLimits(research_strategy=31)  # must be <= 30

    def test_get_limit(self):
        limits = PageLimits()
        assert limits.get_limit(SectionName.SPECIFIC_AIMS) == 1
        assert limits.get_limit(SectionName.RESEARCH_STRATEGY) == 12
        assert limits.get_limit(SectionName.BUDGET_JUSTIFICATION) == "no_limit"


class TestFormatRules:
    """Test FormatRules model."""

    def test_default_format_rules(self):
        rules = FormatRules()
        assert rules.font_family == FontFamily.ARIAL
        assert rules.font_size_pt == 11
        assert rules.margins_inches == 0.5
        assert rules.line_spacing == LineSpacing.SINGLE
        assert rules.page_numbering == PageNumbering.BOTTOM_RIGHT
        assert rules.headers is True
        assert rules.paper_size == PaperSize.LETTER

    def test_custom_format_rules(self):
        rules = FormatRules(
            font_family=FontFamily.GEORGIA,
            font_size_pt=12,
            margins_inches=1.0,
            line_spacing=LineSpacing.DOUBLE,
        )
        assert rules.font_family == FontFamily.GEORGIA
        assert rules.font_size_pt == 12
        assert rules.margins_inches == 1.0
        assert rules.line_spacing == LineSpacing.DOUBLE

    def test_format_rules_validation(self):
        with pytest.raises(ValidationError):
            FormatRules(font_size_pt=9)  # must be >= 10
        
        with pytest.raises(ValidationError):
            FormatRules(font_size_pt=13)  # must be <= 12
        
        with pytest.raises(ValidationError):
            FormatRules(margins_inches=0.4)  # must be >= 0.5
        
        with pytest.raises(ValidationError):
            FormatRules(margins_inches=1.1)  # must be <= 1.0


class TestBudgetRules:
    """Test BudgetRules model."""

    def test_default_budget_rules(self):
        rules = BudgetRules()
        assert rules.modular_budget_enabled is True
        assert rules.modular_budget_increment == 25000
        assert rules.modular_budget_max_direct_costs == 250000
        assert rules.pi_minimum_effort_pct == 30
        assert rules.equipment_threshold_usd == 5000

    def test_custom_budget_rules(self):
        rules = BudgetRules(
            modular_budget_increment=50000,
            pi_minimum_effort_pct=25,
        )
        assert rules.modular_budget_increment == 50000
        assert rules.pi_minimum_effort_pct == 25

    def test_budget_rules_validation(self):
        with pytest.raises(ValidationError):
            BudgetRules(modular_budget_increment=5000)  # must be >= 10000
        
        with pytest.raises(ValidationError):
            BudgetRules(pi_minimum_effort_pct=0)  # must be >= 1
        
        with pytest.raises(ValidationError):
            BudgetRules(pi_minimum_effort_pct=101)  # must be <= 100


class TestFOAMetadata:
    """Test FOAMetadata model."""

    def test_minimal_foa_metadata(self):
        metadata = FOAMetadata(
            foa_id="RFA-TEST-001",
            title="Test FOA",
        )
        assert metadata.foa_id == "RFA-TEST-001"
        assert metadata.title == "Test FOA"
        assert metadata.agency == "NIH"
        assert metadata.activity_code == "R01"
        assert metadata.special_instructions == []
        assert metadata.required_attachments == []

    def test_full_foa_metadata(self):
        metadata = FOAMetadata(
            foa_id="RFA-TEST-001",
            title="Test FOA",
            agency="NIH",
            activity_code="R21",
            release_date="2026-01-01",
            application_due_date="2026-06-01",
            expiration_date="2026-12-31",
            description="Test description",
            special_instructions=["Instruction 1", "Instruction 2"],
            required_attachments=[
                AttachmentSpec(name=SectionName.SPECIFIC_AIMS, required=True, page_limit=1),
            ],
        )
        assert metadata.activity_code == "R21"
        assert len(metadata.special_instructions) == 2
        assert len(metadata.required_attachments) == 1


class TestSectionSpec:
    """Test SectionSpec model."""

    def test_section_spec(self):
        spec = SectionSpec(
            name=SectionName.SPECIFIC_AIMS,
            required=True,
            page_limit=1,
            description="One-page specific aims",
        )
        assert spec.name == SectionName.SPECIFIC_AIMS
        assert spec.required is True
        assert spec.page_limit == 1
        assert spec.subsections == []
        assert spec.content_guidance == ""


class TestApplicationPlan:
    """Test ApplicationPlan model."""

    def test_application_plan_creation(
        self,
        sample_application_plan: ApplicationPlan,
    ):
        plan = sample_application_plan
        assert plan.foa_id == "RFA-EX-001"
        assert plan.foa_title == "Test FOA"
        assert plan.project_title == "Test Project"
        assert plan.principal_investigator == "Dr. Test PI"
        assert plan.institution == "Test University"
        assert plan.activity_code == "R01"

    def test_application_plan_default_sections(self):
        """Test that default sections are initialized."""
        foa_metadata = FOAMetadata(
            foa_id="RFA-TEST-001",
            title="Test FOA",
        )
        plan = ApplicationPlan(
            foa_id="RFA-TEST-001",
            foa_title="Test FOA",
            foa_metadata=foa_metadata,
            project_title="Test Project",
            principal_investigator="Dr. Test PI",
            institution="Test University",
            project_start_date="2026-07-01",
            project_end_date="2031-06-30",
        )
        # Check that default sections were created
        assert SectionName.SPECIFIC_AIMS in plan.sections
        assert SectionName.RESEARCH_STRATEGY in plan.sections
        assert SectionName.BIOSKETCH in plan.sections
        assert SectionName.BUDGET_JUSTIFICATION in plan.sections
        assert SectionName.DATA_MANAGEMENT_SHARING in plan.sections

    def test_get_section(self, sample_application_plan: ApplicationPlan):
        plan = sample_application_plan
        spec = plan.get_section(SectionName.SPECIFIC_AIMS)
        assert spec is not None
        assert spec.name == SectionName.SPECIFIC_AIMS
        assert spec.required is True

    def test_is_section_required(self, sample_application_plan: ApplicationPlan):
        plan = sample_application_plan
        assert plan.is_section_required(SectionName.SPECIFIC_AIMS) is True
        assert plan.is_section_required(SectionName.FACILITIES_RESOURCES) is False

    def test_get_page_limit(self, sample_application_plan: ApplicationPlan):
        plan = sample_application_plan
        assert plan.get_page_limit(SectionName.SPECIFIC_AIMS) == 1
        assert plan.get_page_limit(SectionName.RESEARCH_STRATEGY) == 12
        assert plan.get_page_limit(SectionName.BUDGET_JUSTIFICATION) == "no_limit"

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        foa_metadata = FOAMetadata(
            foa_id="RFA-TEST-001",
            title="Test FOA",
        )
        with pytest.raises(ValidationError):
            ApplicationPlan(
                foa_id="RFA-TEST-001",
                foa_title="Test FOA",
                foa_metadata=foa_metadata,
                project_title="Test Project",
                principal_investigator="Dr. Test PI",
                institution="Test University",
                project_start_date="2026-07-01",
                project_end_date="2031-06-30",
                extra_field="not allowed",
            )


class TestGrantsConfig:
    """Test GrantsConfig model."""

    def test_grants_config_creation(self, sample_grants_config: GrantsConfig):
        config = sample_grants_config
        assert config.page_limits.specific_aims == 1
        assert config.format.font_family == FontFamily.ARIAL
        assert "required" in config.sections
        assert config.budget_rules.modular_budget_enabled is True

    def test_grants_config_extra_fields_forbidden(self):
        with pytest.raises(ValidationError):
            GrantsConfig(extra_field="not allowed")


class TestFOAConfig:
    """Test FOAConfig model."""

    def test_foa_config_creation(self, sample_foa_config: FOAConfig):
        config = sample_foa_config
        assert config.foa_id == "RFA-TEST-001"
        assert config.title == "Test FOA Override"
        assert config.page_limits is not None
        assert config.page_limits["research_strategy"] == 6  # Override

    def test_foa_config_minimal(self):
        config = FOAConfig(
            foa_id="RFA-MIN-001",
            title="Minimal FOA",
        )
        assert config.foa_id == "RFA-MIN-001"
        assert config.title == "Minimal FOA"
        assert config.agency == "NIH"
        assert config.page_limits is None


class TestMergeUtilities:
    """Test merge utility functions."""

    def test_deep_merge_simple(self):
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        result = deep_merge(base, override)
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_deep_merge_nested(self):
        base = {"a": {"x": 1, "y": 2}, "b": 2}
        override = {"a": {"y": 3, "z": 4}, "c": 5}
        result = deep_merge(base, override)
        assert result == {"a": {"x": 1, "y": 3, "z": 4}, "b": 2, "c": 5}

    def test_deep_merge_override_none(self):
        base = {"a": 1}
        override = {}
        result = deep_merge(base, override)
        assert result == {"a": 1}

    def test_merge_lists_unique(self):
        base = [1, 2, 3]
        override = [3, 4, 5]
        result = merge_lists_unique(base, override)
        assert result == [3, 4, 5, 1, 2]

    def test_merge_lists_unique_strings(self):
        base = ["a", "b", "c"]
        override = ["c", "d", "e"]
        result = merge_lists_unique(base, override)
        assert result == ["c", "d", "e", "a", "b"]


class TestSerialization:
    """Test model serialization."""

    def test_application_plan_json_serialization(
        self,
        sample_application_plan: ApplicationPlan,
    ):
        plan = sample_application_plan
        json_str = plan.model_dump_json()
        assert "RFA-EX-001" in json_str
        assert "Test Project" in json_str

    def test_application_plan_dict_serialization(
        self,
        sample_application_plan: ApplicationPlan,
    ):
        plan = sample_application_plan
        data = plan.model_dump()
        assert data["foa_id"] == "RFA-EX-001"
        assert data["project_title"] == "Test Project"
        assert "sections" in data
        assert "page_limits" in data

    def test_page_limits_serialization(self):
        limits = PageLimits(specific_aims=2, research_strategy=6)
        data = limits.model_dump()
        assert data["specific_aims"] == 2
        assert data["research_strategy"] == 6

    def test_format_rules_serialization(self):
        rules = FormatRules(font_family=FontFamily.GEORGIA, font_size_pt=12)
        data = rules.model_dump()
        assert data["font_family"] == "Georgia"
        assert data["font_size_pt"] == 12


class TestValidateAssignment:
    """Test validate_assignment=True behavior."""

    def test_page_limits_assignment_validation(self):
        limits = PageLimits()
        limits.specific_aims = 2
        assert limits.specific_aims == 2
        
        with pytest.raises(ValidationError):
            limits.specific_aims = 0  # must be >= 1

    def test_format_rules_assignment_validation(self):
        rules = FormatRules()
        rules.font_size_pt = 12
        assert rules.font_size_pt == 12
        
        with pytest.raises(ValidationError):
            rules.font_size_pt = 9  # must be >= 10