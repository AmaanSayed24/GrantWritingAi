# Discussion Log — Phase 1: Foundation & Planner

**Project:** Grant Writing AI
**Phase:** 1
**Date:** 2026-10-07

---

## Summary

Phase discussion completed via default interactive mode. User selected "Use defaults — skip to planning" for all 5 identified gray areas, accepting sensible defaults for each.

---

## Gray Areas Discussed

### 1. FOA Parser Strategy
**Question:** How to extract structured requirements from FOA PDFs? PyMuPDF text extraction + LLM parsing vs pure regex/heuristics? What specific fields beyond page limits?

**Decision:** PyMuPDF for text extraction + LLM-based parsing (Ollama) for structured extraction
- Fields: Page limits per section, required attachments, formatting rules, special instructions, FOA-specific overrides
- Rationale: FOAs have variable structure; LLM parsing handles natural language better than regex

### 2. ApplicationPlan Data Model
**Question:** Pydantic models vs TypedDict? How to represent: sections with page limits, FOA-specific rule overrides, required attachments, special instructions? Nested structure?

**Decision:** Pydantic models (not TypedDict) for validation and serialization
- Structure: Nested models for sections, page limits, rule overrides, required attachments, special instructions
- Key models: `ApplicationPlan`, `SectionSpec`, `PageLimits`, `FormatRules`, `BudgetRules`, `AttachmentSpec`

### 3. Config Merge Logic
**Question:** How to merge base `grants.yaml` + FOA-specific `foa-{id}.yaml`? Deep merge? Priority order? Validation on load?

**Decision:** Deep merge with FOA-specific overrides taking precedence over base `grants.yaml`
- Priority: `config/foa-{id}.yaml` > `config/grants.yaml` > hardcoded defaults
- Validation: Pydantic model validation on load; fail fast on schema violations

### 4. Ollama Client & Model Selection
**Question:** Direct `ollama` Python package vs raw HTTP? How to handle model availability checking, fallback to llama.cpp, streaming vs non-streaming?

**Decision:** `ollama` Python package (official, OpenAI-compatible API)
- Model availability: Check via `ollama list` at startup; cache model metadata
- Fallback: Direct `llama.cpp` subprocess if Ollama unavailable
- Streaming: Use streaming for all generation; non-streaming for structured output (JSON)

### 5. Project Module Structure
**Question:** Where does Planner live? `src/agents/planner/` or `src/planner/`? Shared types in `src/types/` or `src/models/`? CLI entry point design?

**Decision:** 
- Planner location: `src/agents/planner/`
- Shared types: `src/types/` (ApplicationPlan, SectionSpec, etc.)
- CLI entry: `src/cli/main.py` with `typer` for subcommands
- Config loading: `src/config/` with `load_grants_config()` and `load_foa_config(foa_id)`

---

## Deferred Ideas (Noted for Later)

- Study-section-specific language tuning (requires corpus) — future phase
- NSF/foundation format support — future phase
- Cloud deployment option — future phase
- Multi-user collaboration — future phase
- Full budget builder UI — future phase
- FOIA corpus ingestion — future phase

---

## Next Steps

1. Run `/gsd-plan-phase 1` to create detailed execution plans
2. Phase 1 will include: project scaffolding, config system, FOA parser, Planner agent, ApplicationPlan models, unit tests