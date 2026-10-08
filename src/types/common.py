# src/types/common.py
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class ActivityCode(StrEnum):
    """NIH Activity Codes for grant mechanisms."""

    R01 = "R01"
    R03 = "R03"
    R21 = "R21"
    R15 = "R15"
    U01 = "U01"
    U19 = "U19"
    P01 = "P01"
    P30 = "P30"
    P50 = "P50"
    K01 = "K01"
    K08 = "K08"
    K23 = "K23"
    K99 = "K99"
    F31 = "F31"
    F32 = "F32"
    T32 = "T32"


class SectionName(StrEnum):
    """Standard NIH application section names."""

    SPECIFIC_AIMS = "specific_aims"
    RESEARCH_STRATEGY = "research_strategy"
    SIGNIFICANCE = "significance"
    INNOVATION = "innovation"
    APPROACH = "approach"
    BIOSKETCH = "biosketch"
    BIOSKETCH_SUPPLEMENT = "biosketch_supplement"
    BUDGET_JUSTIFICATION = "budget_justification"
    FACILITIES_RESOURCES = "facilities_resources"
    EQUIPMENT = "equipment"
    DATA_MANAGEMENT_SHARING = "data_management_sharing"
    AUTHENTICATION_KEY_BIOLOGICAL_RESOURCES = "authentication_key_biological_resources"
    HUMAN_SUBJECTS_PROTECTION = "human_subjects_protection"
    VERTEBRATE_ANIMALS = "vertebrate_animals"
    SELECT_AGENT_RESEARCH = "select_agent_research"
    MULTIPLE_PI_LEADERSHIP_PLAN = "multiple_pi_leadership_plan"
    CONSORTIUM_CONTRACTUAL = "consortium_contractual"
    LETTERS_OF_SUPPORT = "letters_of_support"
    RESOURCE_SHARING_PLAN = "resource_sharing_plan"


class BiosketchFormat(StrEnum):
    """Biosketch format versions."""

    COMMON_FORM_2026 = "2026_common_form"
    LEGACY = "legacy"


class FontFamily(StrEnum):
    """Allowed font families for NIH applications."""

    ARIAL = "Arial"
    HELVETICA = "Helvetica"
    GEORGIA = "Georgia"
    PALATINO_LINOTYPE = "Palatino Linotype"


class LineSpacing(StrEnum):
    """Line spacing options."""

    SINGLE = "single"
    ONE_AND_HALF = "1.5"
    DOUBLE = "double"


class PageNumbering(StrEnum):
    """Page numbering position."""

    BOTTOM_RIGHT = "bottom-right"
    BOTTOM_CENTER = "bottom-center"
    TOP_RIGHT = "top-right"
    TOP_CENTER = "top-center"


class PaperSize(StrEnum):
    """Paper size options."""

    LETTER = "letter"
    A4 = "a4"


class BaseModelExtraForbid(BaseModel):
    """Base model with extra='forbid' and validate_assignment=True."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)