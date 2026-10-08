from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field

from .application_plan import BudgetRules, FOAMetadata, FormatRules, PageLimits
from .common import BaseModelExtraForbid, BiosketchFormat, SectionName

if TYPE_CHECKING:
    from .application_plan import ApplicationPlan


class GrantsConfig(BaseModelExtraForbid):
    """Base grants configuration from grants.yaml."""

    page_limits: PageLimits = Field(default_factory=PageLimits)
    format: FormatRules = Field(default_factory=FormatRules)
    sections: dict[str, Any] = Field(default_factory=dict)
    budget_rules: BudgetRules = Field(default_factory=BudgetRules)
    fonts: dict[str, Any] = Field(default_factory=dict)
    page_margins: dict[str, float] = Field(default_factory=dict)
    validation: dict[str, bool] = Field(default_factory=dict)
    era_commons_checks: list[str] = Field(default_factory=list)

    def to_application_plan_base(self, foa_id: str, foa_title: str, project_title: str,
                                  principal_investigator: str, institution: str,
                                  project_start_date: str, project_end_date: str) -> ApplicationPlan:
        """Convert base config to ApplicationPlan base (without FOA-specific overrides)."""
        from .application_plan import ApplicationPlan, SectionSpec

        # Build sections dict
        sections_dict = {}
        for section_name in SectionName:
            sections_dict[section_name] = SectionSpec(
                name=section_name,
                required=section_name in self.sections.get("required", []),
                page_limit=getattr(self.page_limits, section_name.value, "no_limit"),
                subsections=self.sections.get("research_strategy_subsections", []) if section_name == SectionName.RESEARCH_STRATEGY else [],
            )

        # Handle biosketch format
        biosketch_format_str = self.sections.get("biosketch_format", "2026_common_form")
        biosketch_format = BiosketchFormat.COMMON_FORM_2026 if "common_form" in biosketch_format_str else BiosketchFormat.LEGACY

        foa_metadata = FOAMetadata(
            foa_id=foa_id,
            title=foa_title,
            activity_code="R01",
            release_date="",
            application_due_date="",
        )

        return ApplicationPlan(
            foa_id=foa_id,
            foa_title=foa_title,
            foa_metadata=foa_metadata,
            project_title=project_title,
            principal_investigator=principal_investigator,
            institution=institution,
            project_start_date=project_start_date,
            project_end_date=project_end_date,
            sections=sections_dict,
            page_limits=self.page_limits,
            format_rules=self.format,
            budget_rules=self.budget_rules,
            biosketch_format=biosketch_format,
            biosketch_supplement_required=self.sections.get("biosketch_supplement_required", True),
            validation=self.validation,
            era_commons_checks=self.era_commons_checks,
        )


class FOAConfig(BaseModelExtraForbid):
    """FOA-specific configuration that extends base grants config."""

    foa_id: str
    title: str
    agency: str = Field(default="NIH")
    activity_code: str = Field(default="R01")
    release_date: str = Field(default="")
    application_due_date: str = Field(default="")
    expiration_date: str | None = None
    description: str = Field(default="")
    special_instructions: list[str] = Field(default_factory=list)

    # Override base config sections
    page_limits: dict[str, int | str] | None = None
    format: dict[str, Any] | None = None
    sections: dict[str, Any] | None = None
    budget_rules: dict[str, Any] | None = None
    fonts: dict[str, Any] | None = None
    page_margins: dict[str, float] | None = None
    validation: dict[str, bool] | None = None

    def merge_with_base(self, base: GrantsConfig) -> MergedFOAConfig:
        """Merge FOA-specific config with base config."""
        from .merge import deep_merge

        # Create merged page_limits
        merged_page_limits = deep_merge(
            base.page_limits.model_dump(),
            self.page_limits or {}
        )

        # Create merged format_rules
        merged_format = deep_merge(
            base.format.model_dump(),
            self.format or {}
        )

        # Create merged budget_rules
        merged_budget = deep_merge(
            base.budget_rules.model_dump(),
            self.budget_rules or {}
        )

        # Create merged sections
        merged_sections = deep_merge(
            base.sections,
            self.sections or {}
        )

        # Create merged fonts
        merged_fonts = deep_merge(
            base.fonts,
            self.fonts or {}
        )

        # Create merged page_margins
        merged_margins = deep_merge(
            base.page_margins,
            self.page_margins or {}
        )

        # Create merged validation
        merged_validation = deep_merge(
            base.validation,
            self.validation or {}
        )

        # Build FOAMetadata
        foa_metadata = FOAMetadata(
            foa_id=self.foa_id,
            title=self.title,
            agency=self.agency,
            activity_code=self.activity_code,
            release_date=self.release_date,
            application_due_date=self.application_due_date,
            expiration_date=self.expiration_date,
            description=self.description,
            special_instructions=self.special_instructions,
        )

        return MergedFOAConfig(
            base=base,
            foa_config=self,
            merged_page_limits=PageLimits(**merged_page_limits),
            merged_format=FormatRules(**merged_format),
            merged_budget=BudgetRules(**merged_budget),
            merged_sections=merged_sections,
            merged_fonts=merged_fonts,
            merged_margins=merged_margins,
            merged_validation=merged_validation,
            foa_metadata=foa_metadata,
        )


class MergedFOAConfig(BaseModelExtraForbid):
    """Result of merging base config with FOA-specific config."""

    base: GrantsConfig
    foa_config: FOAConfig
    merged_page_limits: PageLimits
    merged_format: FormatRules
    merged_budget: BudgetRules
    merged_sections: dict[str, Any]
    merged_fonts: dict[str, Any]
    merged_margins: dict[str, float]
    merged_validation: dict[str, bool]
    foa_metadata: FOAMetadata

    def to_application_plan(self, project_title: str, principal_investigator: str,
                             institution: str, project_start_date: str,
                             project_end_date: str) -> ApplicationPlan:
        """Convert merged config to ApplicationPlan."""
        from .application_plan import ApplicationPlan, SectionSpec

        # Build sections dict with merged settings
        sections_dict = {}
        required_sections = self.merged_sections.get("required", [])
        research_strategy_subsections = self.merged_sections.get("research_strategy_subsections", [])

        for section_name in SectionName:
            page_limit = getattr(self.merged_page_limits, section_name.value, "no_limit")
            # Check if FOA has override for this section
            if "page_limits" in self.foa_config.model_fields_set:
                foa_page_limits = self.foa_config.page_limits or {}
                if section_name.value in foa_page_limits:
                    page_limit = foa_page_limits[section_name.value]

            sections_dict[section_name] = SectionSpec(
                name=section_name,
                required=section_name.value in required_sections,
                page_limit=page_limit,
                subsections=research_strategy_subsections if section_name == SectionName.RESEARCH_STRATEGY else [],
            )

        # Handle biosketch format
        biosketch_format_str = self.merged_sections.get("biosketch_format", "2026_common_form")
        biosketch_format = BiosketchFormat.COMMON_FORM_2026 if "common_form" in biosketch_format_str else BiosketchFormat.LEGACY

        return ApplicationPlan(
            foa_id=self.foa_config.foa_id,
            foa_title=self.foa_config.title,
            foa_metadata=self.foa_metadata,
            project_title=project_title,
            principal_investigator=principal_investigator,
            institution=institution,
            project_start_date=project_start_date,
            project_end_date=project_end_date,
            sections=sections_dict,
            page_limits=self.merged_page_limits,
            format_rules=self.merged_format,
            budget_rules=self.merged_budget,
            biosketch_format=biosketch_format,
            biosketch_supplement_required=self.merged_sections.get("biosketch_supplement_required", True),
            validation=self.merged_validation,
            era_commons_checks=self.base.era_commons_checks,
        )