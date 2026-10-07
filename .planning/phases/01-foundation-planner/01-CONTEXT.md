# Phase 01: Foundation & Planner - Context

**Phase:** 1
**Name:** Foundation & Planner
**Date:** 2026-10-07
**Scope:** Complete

---

## Domain Boundary

This phase establishes the project foundation: configuration system, FOA PDF parser, Planner agent, and the ApplicationPlan data model. All downstream phases depend on the ApplicationPlan structure.

---

## Decisions Captured

### FOA Parser Strategy
- **Approach:** PyMuPDF for text extraction + LLM-based parsing (Ollama) for structured extraction
- **Fields to extract:** Page limits per section, required attachments, formatting rules, special instructions, FOA-specific overrides
- **Rationale:** FOAs have variable structure; LLM parsing handles natural language better than regex

### ApplicationPlan Data Model
- **Format:** Pydantic models (not TypedDict) for validation and serialization
- **Structure:** Nested models for sections, page limits, rule overrides, required attachments, special instructions
- **Key models:** `ApplicationPlan`, `SectionSpec`, `PageLimits`, `FormatRules`, `BudgetRules`, `AttachmentSpec`

### Config Merge Logic
- **Strategy:** Deep merge with FOA-specific overrides taking precedence over base `grants.yaml`
- **Priority:** `config/foa-{id}.yaml` > `config/grants.yaml` > hardcoded defaults
- **Validation:** Pydantic model validation on load; fail fast on schema violations

### Ollama Client & Model Selection
- **Client:** `ollama` Python package (official, OpenAI-compatible API)
- **Model availability:** Check via `ollama list` at startup; cache model metadata
- **Fallback:** Direct `llama.cpp` subprocess if Ollama unavailable
- **Streaming:** Use streaming for all generation; non-streaming for structured output (JSON)

### Project Module Structure
- **Planner location:** `src/agents/planner/`
- **Shared types:** `src/types/` (ApplicationPlan, SectionSpec, etc.)
- **CLI entry:** `src/cli/main.py` with `typer` for subcommands
- **Config loading:** `src/config/` with `load_grants_config()` and `load_foa_config(foa_id)`

---

## Canonical References

- `.planning/PROJECT.md` — Project context and requirements
- `.planning/REQUIREMENTS.md` — REQ-01, REQ-02, REQ-03, REQ-35, REQ-36
- `.planning/ROADMAP.md` — Phase 1 success criteria
- `.planning/research/STACK.md` — Technology stack decisions
- `.planning/research/ARCHITECTURE.md` — Architecture patterns (LangGraph, Pydantic, PyMuPDF)
- `.planning/research/PITFALLS.md` — Critical pitfalls (FOA variability, local LLM quality)
- `config/grants.yaml` — Base R01 compliance rules
- `AGENTS.md` — Project guidance for AI agents

---

## Code Context (Reusable Assets)

### From Friday (React/Node AI Assistant)
- `Friday/src/` — React component patterns, UI patterns
- `Friday/package.json` — Dependency patterns

### From friday-assistant (Python Agent Framework)
- `friday-assistant/src/` — Agent orchestration patterns, base agent classes
- `friday-assistant/src/agent/` — LangGraph state machine patterns

### From S_Agent (CampusWatch Agent)
- `S_Agent/src/` — Agent patterns, configuration loading

### From hills-den-website (HTML/JS with Hermes)
- `.hermes/` — Hermes configuration patterns

---

## Deferred Ideas (Future Phases)

- Study-section-specific language tuning (requires corpus)
- NSF/foundation format support
- Cloud deployment option
- Multi-user collaboration
- Full budget builder UI
- FOIA corpus ingestion

---

## Configuration

- **Mode:** YOLO (auto-approve)
- **Granularity:** Fine (7 phases)
- **Execution:** Parallel
- **Git tracking:** Yes
- **Model profile:** Inherit
- **Research:** Enabled
- **Plan check:** Enabled
- **Verifier:** Enabled
- **Compact content:** Yes
- **Drift guard:** Yes
- **MVP mode:** true (from ROADMAP.md)
- **Tracer mode:** true (default)
- **Reversibility gates:** true (default)