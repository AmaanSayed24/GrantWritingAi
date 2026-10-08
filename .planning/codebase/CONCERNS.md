---
last_mapped_commit: 608c6728678e22a32e463bee82bf321f2f44f9e8
last_mapped_at: 2026-10-08
---
# Codebase Concerns: Grant Writing AI

**Analysis Date:** 2026-10-08  
**Scope:** Full repository (C:/Users/sayed/OneDrive/Documents/Project/Grant Writing AI)  
**Project Phase:** Phase 0 (Initialized) — Phase 1 (Foundation & Planner) ready to start

---

## Executive Summary

The codebase is in **pre-implementation state**. Only core data types (`src/types/`) and configuration loading (`src/config/`) exist. All seven phases of the roadmap (agents, RAG, compliance, formatter, UI, integration) remain unimplemented. This is expected for a project at Phase 0, but the following concerns should be tracked as implementation begins.

---

## 🔴 Critical Concerns (Blockers for Phase 1+)

### 1. Zero Agent Implementation

**Location:** `src/agents/`, `src/orchestrator/`, `src/rag/`, `src/compliance/`, `src/formatter/`, `src/cli/` — **do not exist**

- No Planner, Retriever, Drafter, Critic, or Formatter agents
- No LangGraph orchestrator / state machine
- No ChromaDB integration, no anonymization pipeline, no PDF ingestion
- No compliance validation engine, no python-docx formatter, no CLI entry points
- **Impact:** Phase 1 cannot start until project structure is created

### 2. No Test Infrastructure Beyond Types

**Location:** `tests/` — only `test_types.py` exists

- No integration tests, no agent tests, no RAG tests, no compliance tests
- No test fixtures for FOA PDFs, no mock Ollama/ChromaDB setup
- **Impact:** Regression risk as implementation grows; no CI validation

### 3. No UI Implementation

**Location:** `ui/` — **does not exist**

- No Vite/React/TypeScript setup, no `use-local-llm` integration
- No upload, metadata, or gate components
- **Impact:** Phase 6 (UI) blocked until scaffold created

---

## 🟡 High-Priority Technical Debt (Design Risks)

### 4. Configuration Type Safety Gaps

**Location:** `src/config/loader.py`, `src/types/config.py`

- `_convert_config_types()` uses heuristic string parsing (lines 72-103) — fragile for complex YAML
- `FOAConfig` uses `dict[str, Any]` for all override sections (lines 84-90) — loses Pydantic validation
- `deep_merge()` (in `src/config/merge.py` and `src/types/merge.py` — **duplicated**) doesn't handle list merging semantics (replace vs. merge)
- **Risk:** Silent config errors; FOA overrides may not apply correctly

### 5. Duplicated Merge Logic

**Location:** `src/config/merge.py` (lines 1-26) AND `src/types/merge.py` (lines 1-26) — **identical code**

- Two copies of `deep_merge()` must be kept in sync
- `merge_lists_unique()` only in `src/types/merge.py`
- **Fix:** Single source of truth in `src/types/merge.py`, re-export from `src/config/merge.py`

### 6. PageLimits Model Allows String "no_limit" Mixed with Ints

**Location:** `src/types/application_plan.py` lines 24-35

```python
budget_justification: int | str = Field(default="no_limit")
facilities_resources: int | str = Field(default="no_limit")

# ... 7 more fields with int | str

```

- `get_limit()` returns `int | str` — callers must handle both
- Validation only constrains `int` values (ge/le), not `"no_limit"` string
- **Risk:** Type confusion in page counting, rendering, validation logic

### 7. LineSpacing, PageNumbering, PaperSize Use Plain `str, Enum` Not `StrEnum`

**Location:** `src/types/common.py` lines 68-89

```python
class LineSpacing(str, Enum):  # Not StrEnum
    SINGLE = "single"
```

- Inconsistent with `ActivityCode`, `SectionName`, `BiosketchFormat`, `FontFamily` which use `StrEnum`
- May cause comparison issues (`LineSpacing.SINGLE == "single"` works but `isinstance(x, str)` differs)
- **Fix:** Use `StrEnum` consistently (Python 3.11+)

### 8. FOA Config Merge Logic Has Bug

**Location:** `src/types/config.py` lines 192-196

```python
if "page_limits" in self.foa_config.model_fields_set:
    foa_page_limits = self.foa_config.page_limits or {}
    if section_name.value in foa_page_limits:
        page_limit = foa_page_limits[section_name.value]
```

- Checks `model_fields_set` on the FOAConfig instance, but `page_limits` is a field with default `None`
- If user explicitly sets `page_limits: {}` in YAML, it's in `model_fields_set` but empty — logic still runs
- If user omits `page_limits` entirely, it's NOT in `model_fields_set` — but `deep_merge` already applied overrides
- **Result:** Double-application or missed-application of page limit overrides depending on YAML structure

### 9. ApplicationPlan Default Sections Hardcoded

**Location:** `src/types/application_plan.py` lines 212-311

- `_init_default_sections()` creates 18 hardcoded sections
- No mechanism to customize per FOA beyond `required` flag and `page_limit`
- Subsections for Research Strategy hardcoded to `["significance", "innovation", "approach"]`
- **Risk:** FOAs with different section structures (e.g., R21, K-awards) cannot be modeled

### 10. No Anonymization Implementation — Design Only

**Location:** Referenced in `REQUIREMENTS.md` (REQ-04), `PITFALLS.md` (Pitfall 4), `ROADMAP.md` Phase 2

- No code exists for regex + spaCy NER pipeline
- No audit log structure defined
- No UI for PI review of redactions
- **Risk:** Phase 2 scope creep; anonymization is a known hard problem (Pitfall 4)

---

## 🟠 Medium-Priority Concerns (Maintenance Risks)

### 11. Missing Requirements.txt / Lockfile

**Location:** Project root

- `README.md` references `requirements.txt` (line 28) but only `pyproject.toml` exists
- No `uv.lock` or `poetry.lock` for reproducible installs
- `pyproject.toml` has no version pins for transitive dependencies
- **Fix:** Add `requirements.txt` generated from `pip compile` or use `uv sync`

### 12. Python Version Mismatch Risk

**Location:** `pyproject.toml` line 6 (`requires-python = ">=3.11"`), runtime shows Python 3.14.7

- Project requires 3.11+ but environment is 3.14.7 (pre-release)
- `pydantic>=2.8.0` may have issues on 3.14
- **Risk:** CI/CD on 3.11 vs local 3.14 divergence

### 13. No Linting/CI Configuration

**Location:** Project root

- `ruff` configured in `pyproject.toml` but no pre-commit hooks
- No GitHub Actions / CI pipeline
- No `mypy` strict enforcement in CI (configured but not run automatically)
- **Risk:** Code quality drift as multiple contributors add code

### 14. Hardcoded Paths in Config Loader

**Location:** `src/config/loader.py` line 11

```python
CONFIG_DIR = Path(__file__).parent.parent.parent / "config"
```

- Brittle if file moves; assumes fixed project structure
- **Fix:** Use `importlib.resources` or environment variable for config root

### 15. GrantsConfig.to_application_plan_base() Duplicates Logic

**Location:** `src/types/config.py` lines 22-67

- Rebuilds sections dict that `ApplicationPlan._init_default_sections()` also builds
- Two sources of truth for default sections
- **Risk:** Drift between config-driven and model-driven defaults

### 16. Enum Value Mismatch Risk: BiosketchFormat

**Location:** `src/types/common.py` line 55 vs `grants.yaml` line 43

```python

# common.py

COMMON_FORM_2026 = "2026_common_form"

# grants.yaml

biosketch_format: "2026_common_form"
```

- Config parsing in `GrantsConfig.to_application_plan_base()` line 39-40 does string matching:

```python
biosketch_format = BiosketchFormat.COMMON_FORM_2026 if "common_form" in biosketch_format_str else BiosketchFormat.LEGACY
```

- Fragile: if YAML uses `"2026-common-form"` or `"common_form_2026"`, falls back to LEGACY silently
- **Fix:** Use enum directly in YAML with Pydantic validation

### 17. BudgetRules Missing Validation for Consortium F&A

**Location:** `src/types/application_plan.py` line 90

```python
consortium_f_and_a_on_first_25k_only: bool = Field(default=True)
```

- No dollar amount validation, no check that it's only applied when consortium exists
- **Risk:** Invalid budget rules pass validation

### 18. No Error Handling for Missing FOA Configs

**Location:** `src/config/loader.py` lines 58-59

```python
if not config_path.exists():
    raise FileNotFoundError(f"FOA config not found: {config_path}")
```

- No fallback to base config, no template suggestion
- CLI will crash instead of guiding user to create `foa-{id}.yaml`

---

## 🟢 Low-Priority / Future-Proofing

### 19. Incomplete Test Coverage for Config Merge

**Location:** `tests/test_types.py`

- Tests `deep_merge` and `merge_lists_unique` but not `FOAConfig.merge_with_base()`
- No tests for `GrantsConfig.to_application_plan_base()` or `MergedFOAConfig.to_application_plan()`
- No tests for type conversion edge cases in `_convert_config_types()`

### 20. Missing Model Serialization Tests for Nested Configs

**Location:** `tests/test_types.py` class `TestSerialization`

- Tests `ApplicationPlan`, `PageLimits`, `FormatRules` serialization
- No tests for `GrantsConfig`, `FOAConfig`, `MergedFOAConfig` round-trip

### 21. No Docstring Coverage Enforcement

**Location:** `pyproject.toml` — no `ruff` rule for `D` (pydocstyle)

- Public APIs lack consistent docstrings (some have full Google-style, others minimal)
- **Fix:** Add `D` to ruff `select` and enforce in CI

### 22. FOA Template Generator Hardcodes All Values

**Location:** `src/config/loader.py` lines 123-216

- `create_foa_template()` writes 90+ line YAML with all defaults
- No option to generate minimal template (only required fields)
- **Risk:** Users overwhelmed; copy-paste errors

---

## 📋 Phase-Specific Risks (From PITFALLS.md Mapping)

| Phase | Primary Risk | Current Mitigation Status |
|-------|--------------|---------------------------|
| **1: Planner** | FOA PDF parsing accuracy | No parser exists; design only |
| **2: RAG** | Anonymization failures (Pitfall 4) | No implementation; multi-layer design documented |
| **2: RAG** | Retrieval relevance for niche domains (Pitfall 3) | Hybrid search designed; no embedding model selected |
| **3: Drafter** | Local LLM quality for 12-page Strategy (Pitfall 1) | Section-by-section + few-shot + iterative loop designed |
| **4: Critic** | FOA rule conflicts (Pitfall 2) | YAML config designed; merge logic has bugs (Concern #8) |
| **5: Formatter** | Biosketch table generation (Pitfall 5) | No python-docx template exists |
| **5: Formatter** | Page count verification loop | Requires LibreOffice headless; not in deps |
| **6: UI** | Long pipeline state sync (Pitfall 11) | Persistent orchestrator state designed; no implementation |
| **7: Integration** | Git history noise (Pitfall 8) | Branch strategy defined; no automation |

---

## 📦 Dependency Risks

| Dependency | Version Spec | Risk |
|------------|--------------|------|
| `pydantic>=2.8.0` | Unpinned minor | Breaking changes in 2.x series possible |
| `langgraph>=0.2.0` | Pre-1.0 | API instability; major changes likely |
| `ollama>=0.4.0` | Unpinned | Ollama Python client API changes frequently |
| `pymupdf>=1.24.0` | Unpinned | PDF extraction behavior changes |
| `sentence-transformers` | Not in deps yet | Will be needed for Phase 2; GPU/CPU compatibility |

---

## 🔍 Security Considerations

| Area | Concern | Status |
|------|---------|--------|
| **Anonymization** | PI data leakage before processing | Not implemented (Phase 2) |
| **Local LLM** | Model weights supply chain | Ollama pulls from registry; no verification |
| **PDF Parsing** | Malicious PDF exploits (PyMuPDF) | No sandboxing planned |
| **File Upload** | Path traversal in UI upload | No UI yet |
| **Git Commits** | Sensitive data in commit history | Branch strategy separates agent/PI; no automation |

---

## 📈 Recommendations Priority Order

1. **Before Phase 1:** Create project structure (`src/agents/`, `src/orchestrator/`, etc.), fix duplicated `deep_merge`, add `requirements.txt` with pinned versions
2. **Phase 1:** Implement FOA parser with robust error handling; add config merge tests; fix `model_fields_set` bug
3. **Phase 2:** Build anonymization with audit log first; test on real PI PDFs before RAG
4. **Phase 3:** Start Drafter with single section (Specific Aims); validate local LLM quality early
5. **Phase 4:** Implement compliance as pure functions on `ApplicationPlan` — avoid LangGraph coupling
6. **Phase 5:** Use existing NIH DOCX templates (nih-biosketch-builder) rather than building from scratch
7. **Phase 6:** Scaffold UI early (Day 2 per roadmap) to unblock PI feedback
8. **Ongoing:** Add pre-commit hooks, CI pipeline, and integration tests at each phase

---

## 📝 Files Needing Immediate Attention

| File | Issue | Fix |
|------|-------|-----|
| `src/config/merge.py` | Duplicate of `src/types/merge.py` | Remove, import from types |
| `src/types/common.py` | Inconsistent Enum base classes | Use `StrEnum` for all |
| `src/types/application_plan.py` | `int | str` page limits | Use `Optional[int]` with `None` = no limit |
| `src/types/config.py` | FOA merge bug (lines 192-196) | Rewrite override detection |
| `src/config/loader.py` | Heuristic type conversion | Use Pydantic validation instead |
| `pyproject.toml` | No lockfile, unpinned deps | Add `uv.lock` or `requirements.txt` |

---

*Generated by codebase analysis — 2026-10-08*
