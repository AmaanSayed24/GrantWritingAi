---
last_mapped_commit: 608c6728678e22a32e463bee82bf321f2f44f9e8
last_mapped_at: 2026-10-08
---
# Testing Patterns

**Project:** Grant Writing AI  
**Analysis Date:** 2026-10-08  
**Scope:** Full repository (`tests/` directory, `pyproject.toml` pytest config)

---

## 1. Test Framework & Configuration

| Aspect | Detail |
|--------|--------|
| Framework | **pytest** (>=8.2.0) |
| Config | `pyproject.toml` `[tool.pytest.ini_options]` |
| Test discovery | `testpaths = ["tests"]` |
| File pattern | `python_files = ["test_*.py"]` |
| Class pattern | `python_classes = ["Test*"]` |
| Function pattern | `python_functions = ["test_*"]` |
| Default options | `-v --strict-markers` |
| Coverage | `pytest-cov>=5.0.0` available |

---

## 2. Test Structure

```
tests/
├── __init__.py          # Empty (makes tests a package)
├── conftest.py          # Shared fixtures (session/module scope)
└── test_types.py        # Unit tests for Pydantic models
```

**Current test file:** `test_types.py` (~424 lines, ~20 test classes, ~80 test methods)

---

## 3. Fixtures (conftest.py)

### Fixture Categories

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `sample_page_limits` | function | Pre-configured `PageLimits` with all defaults |
| `sample_format_rules` | function | Pre-configured `FormatRules` with all defaults |
| `sample_budget_rules` | function | Pre-configured `BudgetRules` with all defaults |
| `sample_foa_metadata` | function | Minimal `FOAMetadata` for testing |
| `sample_application_plan` | function | Full `ApplicationPlan` with all sections (depends on above) |
| `sample_grants_config` | function | `GrantsConfig` with full YAML-equivalent data |
| `sample_foa_config` | function | `FOAConfig` with overrides (e.g., research_strategy=6) |
| `config_dir` | function | Path to `config/` directory |
| `grants_yaml_path` | function | Path to `config/grants.yaml` |

### Fixture Composition

- Higher-level fixtures compose lower-level ones (e.g., `sample_application_plan` depends on 4 other fixtures)
- All fixtures return **fully constructed model instances**, not raw dicts
- Fixtures use type hints for return types

---

## 4. Test Organization (test_types.py)

### Test Classes by Domain

| Class | Models Tested | Test Count |
|-------|---------------|------------|
| `TestEnums` | All StrEnum/plain Enum classes | 6 methods |
| `TestPageLimits` | `PageLimits` | 5 methods |
| `TestFormatRules` | `FormatRules` | 3 methods |
| `TestBudgetRules` | `BudgetRules` | 3 methods |
| `TestFOAMetadata` | `FOAMetadata` | 2 methods |
| `TestSectionSpec` | `SectionSpec` | 1 method |
| `TestApplicationPlan` | `ApplicationPlan` | 6 methods |
| `TestGrantsConfig` | `GrantsConfig` | 2 methods |
| `TestFOAConfig` | `FOAConfig` | 2 methods |
| `TestMergeUtilities` | `deep_merge`, `merge_lists_unique` | 5 methods |
| `TestSerialization` | All models (dump/dump_json) | 4 methods |
| `TestValidateAssignment` | `validate_assignment=True` behavior | 2 methods |

### Naming Convention

- **Classes:** `Test<ModelName>` or `Test<Feature>`
- **Methods:** `test_<behavior>_<condition>` or `test_<method_name>`
- **Validation tests:** `test_<model>_validation_<constraint>` (e.g., `test_page_limits_validation_ge`)

---

## 5. Test Patterns

### 5.1 Happy Path / Default Values

```python
def test_default_page_limits(self):
    limits = PageLimits()
    assert limits.specific_aims == 1
    assert limits.research_strategy == 12
    assert limits.biosketch == 5
    assert limits.budget_justification == "no_limit"
```

### 5.2 Custom Construction

```python
def test_custom_page_limits(self):
    limits = PageLimits(specific_aims=2, research_strategy=6, biosketch=4)
    assert limits.specific_aims == 2
    assert limits.research_strategy == 6
    assert limits.biosketch == 4
```

### 5.3 Validation Errors (Constraint Testing)

```python
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
```

### 5.4 Method Behavior

```python
def test_get_limit(self):
    limits = PageLimits()
    assert limits.get_limit(SectionName.SPECIFIC_AIMS) == 1
    assert limits.get_limit(SectionName.RESEARCH_STRATEGY) == 12
    assert limits.get_limit(SectionName.BUDGET_JUSTIFICATION) == "no_limit"
```

### 5.5 Extra Fields Forbidden (BaseModelExtraForbid)

```python
def test_extra_fields_forbidden(self):
    foa_metadata = FOAMetadata(foa_id="RFA-TEST-001", title="Test FOA")
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
```

### 5.6 Default Section Initialization (model_post_init)

```python
def test_application_plan_default_sections(self):
    foa_metadata = FOAMetadata(foa_id="RFA-TEST-001", title="Test FOA")
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
    assert SectionName.SPECIFIC_AIMS in plan.sections
    assert SectionName.RESEARCH_STRATEGY in plan.sections
    assert SectionName.BIOSKETCH in plan.sections
    # ... more assertions
```

### 5.7 Merge Utilities

```python
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

def test_merge_lists_unique(self):
    base = [1, 2, 3]
    override = [3, 4, 5]
    result = merge_lists_unique(base, override)
    assert result == [3, 4, 5, 1, 2]  # override first, then base unique
```

### 5.8 Serialization

```python
def test_application_plan_json_serialization(self, sample_application_plan: ApplicationPlan):
    plan = sample_application_plan
    json_str = plan.model_dump_json()
    assert "RFA-EX-001" in json_str
    assert "Test Project" in json_str

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
```

### 5.9 Validate Assignment (validate_assignment=True)

```python
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
```

---

## 6. Mocking & Test Doubles

**Current state:** No mocking framework used (no `unittest.mock`, no `pytest-mock`).  
**Reason:** All tests exercise pure Pydantic models with no external dependencies (no I/O, no network, no LLM calls).

**When mocking is needed** (future):
- Use `unittest.mock.patch` or `pytest-mock` `mocker` fixture
- Mock at module boundary (e.g., `src.config.loader.yaml.safe_load`)
- Prefer dependency injection over patching where possible

---

## 7. Coverage

**Current:** No coverage configuration or enforcement.  
**Available:** `pytest-cov` in dev dependencies.

**Recommended additions to pyproject.toml:**

```toml
[tool.pytest.ini_options]
addopts = "-v --strict-markers --cov=src --cov-report=term-missing --cov-fail-under=80"
```

---

## 8. Running Tests

```bash

# Run all tests

pytest

# Run with coverage

pytest --cov=src --cov-report=term-missing

# Run specific test file

pytest tests/test_types.py

# Run specific test class

pytest tests/test_types.py::TestPageLimits

# Run specific test method

pytest tests/test_types.py::TestPageLimits::test_default_page_limits

# Run with verbose output

pytest -v

# Run with warnings as errors

pytest -W error
```

---

## 9. Test Data Philosophy

| Principle | Practice |
|-----------|----------|
| **Realistic but minimal** | Fixtures use realistic NIH R01 values (e.g., `specific_aims=1`, `research_strategy=12`) |
| **Composable** | Large fixtures built from smaller ones |
| **Type-safe** | Fixtures return typed model instances, not dicts |
| **Isolated** | Each test gets fresh instances (function-scoped fixtures) |
| **Explicit** | Test data constructed inline for simple cases, fixtures for complex |

---

## 10. Gaps & Recommendations

| Area | Status | Recommendation |
|------|--------|----------------|
| Config loading tests | ❌ Missing | Add tests for `load_grants_config`, `load_foa_config`, `_convert_config_types` |
| Integration tests | ❌ Missing | Add tests for YAML round-trip (load → merge → ApplicationPlan) |
| Edge cases | Partial | Add tests for empty strings, None handling, boundary values |
| Property-based tests | ❌ Missing | Consider `hypothesis` for merge utilities |
| Performance tests | ❌ Missing | Not needed yet (no perf-critical paths) |
| Coverage enforcement | ❌ Missing | Add `--cov-fail-under` threshold |

---

## 11. CI Integration

**Current:** No CI configuration found.  
**Recommended (GitHub Actions example):**

```yaml
- name: Run tests
  run: |
    pip install -e ".[dev]"
    pytest --cov=src --cov-report=xml --cov-fail-under=80
```

---

*Refreshed: 2026-10-08*
