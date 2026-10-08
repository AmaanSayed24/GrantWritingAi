---
last_mapped_commit: 608c6728678e22a32e463bee82bf321f2f44f9e8
last_mapped_at: 2026-10-08
---
# Codebase Conventions

**Project:** Grant Writing AI  
**Analysis Date:** 2026-10-08  
**Scope:** Full repository (Python source in `src/`, tests in `tests/`, config in `config/`)

---

## 1. Project Structure & Layout

```
Grant Writing AI/
├── src/                    # Python package (src-layout)
│   ├── types/              # Pydantic data models
│   │   ├── __init__.py     # Public exports
│   │   ├── common.py       # Enums, base model
│   │   ├── application_plan.py  # Core application models
│   │   ├── config.py       # Config models (GrantsConfig, FOAConfig, MergedFOAConfig)
│   │   └── merge.py        # Utility functions (deep_merge, merge_lists_unique)
│   └── config/             # Config loading & merging
│       ├── __init__.py
│       ├── loader.py       # YAML loading, type conversion
│       └── merge.py        # Deep merge (duplicate of types/merge.py)
├── config/                 # Runtime YAML configuration
│   └── grants.yaml         # Base NIH R01 compliance rules
├── tests/                  # pytest test suite
│   ├── __init__.py
│   ├── conftest.py         # Shared fixtures
│   └── test_types.py       # Model unit tests
├── .planning/              # GSD planning artifacts (committed)
└── pyproject.toml          # Build config, tool settings
```

**Package Discovery:** `pyproject.toml` uses `setuptools.find` with `where = ["src"]` and `include = ["grant_writing_ai*"]`.

---

## 2. Python Version & Dependencies

- **Python:** `>=3.11` (uses `StrEnum`, `int | str` union syntax)
- **Core Dependencies:**
  - `pydantic>=2.8.0`, `pydantic-settings>=2.4.0`
  - `pyyaml>=6.0.1`
  - `pymupdf>=1.24.0`
  - `ollama>=0.4.0`
  - `langgraph>=0.2.0`, `langchain-core>=0.3.0`
  - `typer>=0.12.0`, `rich>=13.7.0`
- **Dev Dependencies:** `pytest>=8.2.0`, `pytest-cov>=5.0.0`, `ruff>=0.6.0`, `mypy>=1.11.0`

---

## 3. Code Style (Ruff)

Configured in `pyproject.toml` `[tool.ruff]`:

| Setting | Value |
|---------|-------|
| Target version | `py311` |
| Line length | `100` |
| Quote style | `double` |
| Indent style | `space` (4 spaces) |
| Skip magic trailing comma | `false` |

**Selected Rules:** `E`, `F`, `I`, `UP`, `B`, `C4`, `SIM`  
**Ignored:** `E501` (line length handled by formatter), `B008` (function calls in default args)  
**Excludes:** `.git`, `__pycache__`, `.venv`, `venv`, `dist`, `build`

---

## 4. Type Checking (MyPy)

Configured in `pyproject.toml` `[tool.mypy]`:

- `python_version = "3.11"`
- `strict = true`
- `disallow_untyped_defs = true`
- `warn_return_any = true`
- `warn_unused_configs = true`
- **Excludes:** `tests/`

---

## 5. Naming Conventions

| Element | Convention | Examples |
|---------|------------|----------|
| Classes | PascalCase | `ApplicationPlan`, `PageLimits`, `BaseModelExtraForbid` |
| Functions/Methods | snake_case | `deep_merge`, `merge_lists_unique`, `get_section`, `model_post_init` |
| Enums (class) | PascalCase | `ActivityCode`, `SectionName`, `FontFamily` |
| Enum members | UPPER_CASE | `ActivityCode.R01`, `SectionName.SPECIFIC_AIMS` |
| Module files | snake_case | `application_plan.py`, `common.py`, `loader.py` |
| Type variables | PascalCase | `Any` (from typing) |
| Constants | UPPER_SNAKE_CASE | `CONFIG_DIR` (module-level) |
| Private module functions | `_leading_underscore` | `_convert_config_types`, `_init_default_sections` |
| Pydantic config | `model_config` | `ConfigDict(extra="forbid", validate_assignment=True)` |

---

## 6. Pydantic Patterns

### Base Model

```python
class BaseModelExtraForbid(BaseModel):
    """Base model with extra='forbid' and validate_assignment=True."""
    model_config = ConfigDict(extra="forbid", validate_assignment=True)
```

All models inherit from `BaseModelExtraForbid` (defined in `common.py`).

### Field Constraints

Extensive use of `Field()` with validation:

```python
specific_aims: int = Field(default=1, ge=1, le=5)
font_size_pt: int = Field(default=11, ge=10, le=12)
margins_inches: float = Field(default=0.5, ge=0.5, le=1.0)
modular_budget_increment: int = Field(default=25000, ge=10000, le=50000)
```

### Enums

- **StrEnum** for string-valued enums (preferred):
  ```python
  class ActivityCode(StrEnum):
      R01 = "R01"
      R21 = "R21"
  ```
- **Plain Enum** with string values for non-StrEnum cases:
  ```python
  class LineSpacing(str, Enum):
      SINGLE = "single"
      DOUBLE = "double"
  ```

### Default Factories

```python
sections: dict[SectionName, SectionSpec] = Field(default_factory=dict)
special_instructions: list[str] = Field(default_factory=list)
allowed_fonts: list[FontFamily] = Field(default_factory=lambda: [...])
validation: dict[str, bool] = Field(default_factory=lambda: {...})
```

### Post-Init Initialization

```python
def model_post_init(self, __context: Any) -> None:
    """Initialize default sections after model creation."""
    if not self.sections:
        self._init_default_sections()
```

### Serialization

- `model_dump()` for dict
- `model_dump_json()` for JSON string
- Enums serialize to their string values automatically

---

## 7. Error Handling

| Scenario | Approach |
|----------|----------|
| Validation errors | Pydantic `ValidationError` raised automatically (extra fields forbidden, constraint violations) |
| Missing config files | `FileNotFoundError` with descriptive path |
| Type conversion failures | Try/except with fallback to string (in `_convert_config_types`) |
| YAML parsing errors | Propagate `yaml.YAMLError` |

**No custom exception classes** defined yet.

---

## 8. Config Loading & Merging

### YAML Loading (`src/config/loader.py`)

- `yaml.safe_load()` for parsing
- Recursive type conversion (`_convert_config_types`):
  - `"true"`/`"false"` → `bool`
  - `"no_limit"` → string `"no_limit"` (preserved)
  - Numeric strings → `int` or `float`
  - Nested dicts/lists processed recursively

### Deep Merge (`src/types/merge.py` & `src/config/merge.py`)

```python
def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result
```

- Override takes precedence
- Recursive for nested dicts
- Duplicate implementation in two locations (should consolidate)

### List Merge (`merge_lists_unique`)

```python
def merge_lists_unique(base: list[Any], override: list[Any]) -> list[Any]:
    # Override items first (preserve order), then base items not in override
```

- Preserves order
- Removes duplicates
- Override items appear first

---

## 9. Import Organization

```python

# Standard library

from enum import StrEnum
from pathlib import Path
from typing import Any

# Third-party

import yaml
from pydantic import BaseModel, ConfigDict, Field

# Local (relative)

from .common import BaseModelExtraForbid, SectionName, ...
from .application_plan import BudgetRules, FOAMetadata, ...
```

- Standard library first
- Third-party second
- Local relative imports last
- Grouped by module, alphabetized within groups

---

## 10. Documentation

- **Module docstrings:** One-line at top of file (`"""Core data types for Grant Writing AI."""`)
- **Class docstrings:** One-line summary (`"""Page limits for each application section."""`)
- **Method docstrings:** One-line with Args/Returns for complex functions
- **Type hints:** Full coverage (enforced by MyPy `disallow_untyped_defs`)

---

## 11. Git & Workflow

- **GSD (Git. Ship. Done.)** workflow for phase-driven development
- **Branch strategy:** `agent/drafts` (auto-commits), `pi/edits` (human gates), `main` (approved)
- **Commit format:** `type(scope): message` with REQ-IDs, agent, model, chunks
- **Planning artifacts** in `.planning/` are committed

---

*Refreshed: 2026-10-08*
