# src/types/application_plan.py
from typing import Any

from pydantic import Field, model_validator

from .common import (
    BaseModelExtraForbid,
    BiosketchFormat,
    FontFamily,
    LineSpacing,
    PageNumbering,
    PaperSize,
    SectionName,
)


class PageLimits(BaseModelExtraForbid):
    """Page limits for each application section."""

    specific_aims: int = Field(default=1, ge=1, le=5)
    research_strategy: int = Field(default=12, ge=1, le=30)
    biosketch: int = Field(default=5, ge=1, le=10)
    biosketch_supplement: int = Field(default=2, ge=1, le=5)
    budget_justification: int | str = Field(default="no_limit")
    facilities_resources: int | str = Field(default="no_limit")
    equipment: int | str = Field(default="no_limit")
    data_management_sharing: int = Field(default=2, ge=1, le=5)
    authentication_key_biological_resources: int = Field(default=1, ge=1, le=3)
    human_subjects_protection: int | str = Field(default="no_limit")
    vertebrate_animals: int | str = Field(default="no_limit")
    select_agent_research: int = Field(default=1, ge=1, le=3)
    multiple_pi_leadership_plan: int = Field(default=3, ge=1, le=6)
    consortium_contractual: int | str = Field(default="no_limit")
    letters_of_support: int | str = Field(default="no_limit")
    resource_sharing_plan: int = Field(default=1, ge=1, le=3)

    def get_limit(self, section: SectionName) -> int | str:
        """Get page limit for a section by name."""
        return getattr(self, section.value, "no_limit")


class FormatRules(BaseModelExtraForbid):
    """Formatting rules for the application."""

    font_family: FontFamily = Field(default=FontFamily.ARIAL)
    font_size_pt: int = Field(default=11, ge=10, le=12)
    margins_inches: float = Field(default=0.5, ge=0.5, le=1.0)
    line_spacing: LineSpacing = Field(default=LineSpacing.SINGLE)
    page_numbering: PageNumbering = Field(default=PageNumbering.BOTTOM_RIGHT)
    headers: bool = Field(default=True)
    header_format: str = Field(default="PI Last Name / Project Title / Page X of Y")
    paper_size: PaperSize = Field(default=PaperSize.LETTER)

    # Detailed margins
    margin_top: float = Field(default=0.5, ge=0.5, le=1.0)
    margin_bottom: float = Field(default=0.5, ge=0.5, le=1.0)
    margin_left: float = Field(default=0.5, ge=0.5, le=1.0)
    margin_right: float = Field(default=0.5, ge=0.5, le=1.0)

    # Allowed fonts
    allowed_fonts: list[FontFamily] = Field(
        default_factory=lambda: [
            FontFamily.ARIAL,
            FontFamily.HELVETICA,
            FontFamily.GEORGIA,
            FontFamily.PALATINO_LINOTYPE,
        ]
    )
    default_font: FontFamily = Field(default=FontFamily.ARIAL)
    minimum_font_size_pt: int = Field(default=11, ge=10, le=12)


class BudgetRules(BaseModelExtraForbid):
    """Budget rules and constraints."""

    modular_budget_enabled: bool = Field(default=True)
    modular_budget_increment: int = Field(default=25000, ge=10000, le=50000)
    modular_budget_max_direct_costs: int = Field(default=250000, ge=100000, le=500000)

    pi_minimum_effort_pct: int = Field(default=30, ge=1, le=100)
    co_investigator_minimum_effort_pct: int = Field(default=10, ge=1, le=100)
    max_total_effort_pct: int = Field(default=100, ge=1, le=100)

    equipment_threshold_usd: int = Field(default=5000, ge=1000, le=20000)
    equipment_requires_justification_above: bool = Field(default=True)

    foreign_travel_requires_approval: bool = Field(default=True)
    domestic_conference_max_per_year: int = Field(default=2, ge=0, le=10)

    consortium_f_and_a_on_first_25k_only: bool = Field(default=True)

    @model_validator(mode="before")
    @classmethod
    def _flatten_nested(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        res = dict(data)
        if "modular_budget" in res and isinstance(res["modular_budget"], dict):
            mb = res.pop("modular_budget")
            if "enabled" in mb:
                res["modular_budget_enabled"] = mb["enabled"]
            if "increment" in mb:
                res["modular_budget_increment"] = mb["increment"]
            if "max_direct_costs" in mb:
                res["modular_budget_max_direct_costs"] = mb["max_direct_costs"]
        if "personnel" in res and isinstance(res["personnel"], dict):
            p = res.pop("personnel")
            if "pi_minimum_effort_pct" in p:
                res["pi_minimum_effort_pct"] = p["pi_minimum_effort_pct"]
            if "co_investigator_minimum_effort_pct" in p:
                res["co_investigator_minimum_effort_pct"] = p["co_investigator_minimum_effort_pct"]
            if "max_total_effort_pct" in p:
                res["max_total_effort_pct"] = p["max_total_effort_pct"]
        if "equipment" in res and isinstance(res["equipment"], dict):
            eq = res.pop("equipment")
            if "threshold_usd" in eq:
                res["equipment_threshold_usd"] = eq["threshold_usd"]
            if "requires_justification_above" in eq:
                res["equipment_requires_justification_above"] = eq["requires_justification_above"]
        if "travel" in res and isinstance(res["travel"], dict):
            tr = res.pop("travel")
            if "foreign_travel_requires_approval" in tr:
                res["foreign_travel_requires_approval"] = tr["foreign_travel_requires_approval"]
            if "domestic_conference_max_per_year" in tr:
                res["domestic_conference_max_per_year"] = tr["domestic_conference_max_per_year"]
        if "consortium" in res and isinstance(res["consortium"], dict):
            co = res.pop("consortium")
            if "f_and_a_on_first_25k_only" in co:
                res["consortium_f_and_a_on_first_25k_only"] = co["f_and_a_on_first_25k_only"]
        return res


class AttachmentSpec(BaseModelExtraForbid):
    """Specification for a required attachment."""

    name: SectionName
    required: bool = Field(default=True)
    page_limit: int | str = Field(default="no_limit")
    description: str = Field(default="")


class SectionSpec(BaseModelExtraForbid):
    """Specification for a section of the application."""

    name: SectionName
    required: bool = Field(default=True)
    page_limit: int | str = Field(default="no_limit")
    subsections: list[str] = Field(default_factory=list)
    description: str = Field(default="")
    content_guidance: str = Field(default="")


class FOAMetadata(BaseModelExtraForbid):
    """Metadata about a Funding Opportunity Announcement."""

    foa_id: str
    title: str
    agency: str = Field(default="NIH")
    activity_code: str = Field(default="R01")
    release_date: str = Field(default="")
    application_due_date: str = Field(default="")
    expiration_date: str | None = None
    description: str = Field(default="")
    special_instructions: list[str] = Field(default_factory=list)
    required_attachments: list[AttachmentSpec] = Field(default_factory=list)
    contact_pi_eligible: bool = Field(default=True)
    multiple_pi_allowed: bool = Field(default=True)
    foreign_organizations_eligible: bool = Field(default=False)


class ApplicationPlan(BaseModelExtraForbid):
    """Complete application plan with all sections, rules, and FOA metadata."""

    # FOA identification
    foa_id: str
    foa_title: str
    foa_metadata: FOAMetadata

    # Project metadata
    project_title: str
    principal_investigator: str
    institution: str
    project_start_date: str
    project_end_date: str
    activity_code: str = Field(default="R01")

    # Section specifications
    sections: dict[SectionName, SectionSpec] = Field(default_factory=dict)

    # Page limits
    page_limits: PageLimits = Field(default_factory=PageLimits)

    # Format rules
    format_rules: FormatRules = Field(default_factory=FormatRules)

    # Budget rules
    budget_rules: BudgetRules = Field(default_factory=BudgetRules)

    # Biosketch format
    biosketch_format: BiosketchFormat = Field(default=BiosketchFormat.COMMON_FORM_2026)
    biosketch_supplement_required: bool = Field(default=True)

    # Validation rules
    validation: dict[str, bool] = Field(default_factory=lambda: {
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
    })

    # ERA Commons checks
    era_commons_checks: list[str] = Field(default_factory=lambda: [
        "Page limits per attachment",
        "Font size and type",
        "Margins",
        "Required attachments present",
        "Budget modular/non-modular consistency",
        "Senior/Key Person biosketches",
        "Data Management and Sharing Plan",
        "Authentication of Key Biological Resources",
        "Human Subjects / Vertebrate Animals sections if applicable",
    ])

    def get_section(self, name: SectionName) -> SectionSpec | None:
        """Get section specification by name."""
        return self.sections.get(name)

    def is_section_required(self, name: SectionName) -> bool:
        """Check if a section is required."""
        spec = self.sections.get(name)
        return spec.required if spec else False

    def get_page_limit(self, name: SectionName) -> int | str:
        """Get page limit for a section."""
        spec = self.sections.get(name)
        if spec:
            return spec.page_limit
        return self.page_limits.get_limit(name)

    def model_post_init(self, __context: Any) -> None:
        """Initialize default sections after model creation."""
        if not self.sections:
            self._init_default_sections()

    def _init_default_sections(self) -> None:
        """Initialize default NIH R01 sections."""
        self.sections = {
            SectionName.SPECIFIC_AIMS: SectionSpec(
                name=SectionName.SPECIFIC_AIMS,
                required=True,
                page_limit=self.page_limits.specific_aims,
                description="One-page statement of specific aims",
            ),
            SectionName.RESEARCH_STRATEGY: SectionSpec(
                name=SectionName.RESEARCH_STRATEGY,
                required=True,
                page_limit=self.page_limits.research_strategy,
                subsections=["significance", "innovation", "approach"],
                description="Research strategy with Significance, Innovation, and Approach",
            ),
            SectionName.BIOSKETCH: SectionSpec(
                name=SectionName.BIOSKETCH,
                required=True,
                page_limit=self.page_limits.biosketch,
                description="Biosketch in NIH 2026 Common Form",
            ),
            SectionName.BUDGET_JUSTIFICATION: SectionSpec(
                name=SectionName.BUDGET_JUSTIFICATION,
                required=True,
                page_limit=self.page_limits.budget_justification,
                description="Budget justification for all categories",
            ),
            SectionName.FACILITIES_RESOURCES: SectionSpec(
                name=SectionName.FACILITIES_RESOURCES,
                required=False,
                page_limit=self.page_limits.facilities_resources,
                description="Facilities and other resources",
            ),
            SectionName.EQUIPMENT: SectionSpec(
                name=SectionName.EQUIPMENT,
                required=False,
                page_limit=self.page_limits.equipment,
                description="Equipment list and justification",
            ),
            SectionName.DATA_MANAGEMENT_SHARING: SectionSpec(
                name=SectionName.DATA_MANAGEMENT_SHARING,
                required=True,
                page_limit=self.page_limits.data_management_sharing,
                description="Data management and sharing plan",
            ),
            SectionName.AUTHENTICATION_KEY_BIOLOGICAL_RESOURCES: SectionSpec(
                name=SectionName.AUTHENTICATION_KEY_BIOLOGICAL_RESOURCES,
                required=True,
                page_limit=self.page_limits.authentication_key_biological_resources,
                description="Authentication of key biological resources",
            ),
            SectionName.HUMAN_SUBJECTS_PROTECTION: SectionSpec(
                name=SectionName.HUMAN_SUBJECTS_PROTECTION,
                required=False,
                page_limit=self.page_limits.human_subjects_protection,
                description="Human subjects protection",
            ),
            SectionName.VERTEBRATE_ANIMALS: SectionSpec(
                name=SectionName.VERTEBRATE_ANIMALS,
                required=False,
                page_limit=self.page_limits.vertebrate_animals,
                description="Vertebrate animals section",
            ),
            SectionName.SELECT_AGENT_RESEARCH: SectionSpec(
                name=SectionName.SELECT_AGENT_RESEARCH,
                required=False,
                page_limit=self.page_limits.select_agent_research,
                description="Select agent research",
            ),
            SectionName.MULTIPLE_PI_LEADERSHIP_PLAN: SectionSpec(
                name=SectionName.MULTIPLE_PI_LEADERSHIP_PLAN,
                required=False,
                page_limit=self.page_limits.multiple_pi_leadership_plan,
                description="Multiple PI leadership plan",
            ),
            SectionName.CONSORTIUM_CONTRACTUAL: SectionSpec(
                name=SectionName.CONSORTIUM_CONTRACTUAL,
                required=False,
                page_limit=self.page_limits.consortium_contractual,
                description="Consortium/contractual arrangements",
            ),
            SectionName.LETTERS_OF_SUPPORT: SectionSpec(
                name=SectionName.LETTERS_OF_SUPPORT,
                required=False,
                page_limit=self.page_limits.letters_of_support,
                description="Letters of support",
            ),
            SectionName.RESOURCE_SHARING_PLAN: SectionSpec(
                name=SectionName.RESOURCE_SHARING_PLAN,
                required=False,
                page_limit=self.page_limits.resource_sharing_plan,
                description="Resource sharing plan",
            ),
            SectionName.BIOSKETCH_SUPPLEMENT: SectionSpec(
                name=SectionName.BIOSKETCH_SUPPLEMENT,
                required=self.biosketch_supplement_required,
                page_limit=self.page_limits.biosketch_supplement,
                description="Biosketch supplement (2026 Common Form)",
            ),
        }