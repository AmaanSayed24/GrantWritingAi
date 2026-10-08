# src/types/__init__.py
"""Core data types for Grant Writing AI."""

from .application_plan import (
    ApplicationPlan,
    AttachmentSpec,
    BudgetRules,
    FOAMetadata,
    FormatRules,
    PageLimits,
    SectionSpec,
)
from .common import (
    ActivityCode,
    BaseModelExtraForbid,
    BiosketchFormat,
    FontFamily,
    LineSpacing,
    PageNumbering,
    PaperSize,
    SectionName,
)
from .config import (
    FOAConfig,
    GrantsConfig,
    MergedFOAConfig,
)
from .merge import (
    deep_merge,
    merge_lists_unique,
)

__all__ = [
    # Base
    "BaseModelExtraForbid",
    # Enums
    "ActivityCode",
    "SectionName",
    "BiosketchFormat",
    "FontFamily",
    "LineSpacing",
    "PageNumbering",
    "PaperSize",
    # Application Plan
    "PageLimits",
    "FormatRules",
    "BudgetRules",
    "AttachmentSpec",
    "SectionSpec",
    "FOAMetadata",
    "ApplicationPlan",
    # Config
    "GrantsConfig",
    "FOAConfig",
    "MergedFOAConfig",
    # Merge utilities
    "deep_merge",
    "merge_lists_unique",
]