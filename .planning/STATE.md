# Project State: Grant Writing AI

**Project:** Grant Writing AI
**Version:** v1 (Prototype)
**Last Updated:** 2026-10-07
**Current Phase:** 0 (Initialized — ready for Phase 1)

---

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-10-07 after initialization)

**Core value:** End-to-end R01 draft generation (Specific Aims, Research Strategy, Biosketches, Budget) with compliance validation — all local, all free, human-in-the-loop at decision points.

**Current focus:** Phase 1: Foundation & Planner

---

## Phase Status

| Phase | Name | Status | Started | Completed | Notes |
|-------|------|--------|---------|-----------|-------|
| 0 | Initialization | ✅ Done | 2026-10-07 | 2026-10-07 | PROJECT.md, config.json, research/, REQUIREMENTS.md, ROADMAP.md created |
| 1 | Foundation & Planner | ⏳ Ready | — | — | FOA parser, Planner, ApplicationPlan |
| 2 | RAG & Retriever | ⏳ Pending | — | — | ChromaDB, anonymization, ingestion, Retriever |
| 3 | Drafter Core | ⏳ Pending | — | — | Aims + Strategy, few-shot, iterative loop |
| 4 | Critic & Compliance | ⏳ Pending | — | — | YAML rules, cross-checks, page validation |
| 5 | Formatter & DOCX | ⏳ Pending | — | — | python-docx template, biosketch, page loop |
| 6 | React UI & Gates | ⏳ Pending | — | — | Vite/React/TS, 3 gates, progress polling |
| 7 | Integration & Pilot | ⏳ Pending | — | — | End-to-end, Git workflow, 2-3 PI test |

---

## Active Requirements (v1)

### Phase 1 Target
- REQ-01: FOA parser → ApplicationPlan
- REQ-02: Planner agent creates ApplicationPlan
- REQ-03: UI upload + metadata (can start in parallel)
- REQ-35: Config system loads
- REQ-36: Ollama connects

### Phase 2 Target
- REQ-04: Anonymization pipeline
- REQ-05: PDF ingestion → ChromaDB
- REQ-06: RePORTER API
- REQ-07: Section-aware hybrid Retriever
- REQ-08: Ranked chunks with citations

### Phase 3 Target
- REQ-09: Specific Aims generator
- REQ-10: Research Strategy generator
- REQ-13: Few-shot templates
- REQ-14: Iterative Drafter↔Critic loop

### Phase 4 Target
- REQ-15 to REQ-20: Full compliance validation

### Phase 5 Target
- REQ-21 to REQ-25: DOCX export

### Phase 6 Target
- REQ-26 to REQ-32: UI + 3 human gates

### Phase 7 Target
- REQ-33 to REQ-37: Integration + pilot

---

## Key Decisions Log

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| NIH R01 only for prototype | Highest volume, most structured, PI partners NIH-funded | ✅ Good |
| Full pipeline in prototype | Validates end-to-end; partial hides integration issues | ✅ Good |
| React web UI (like Friday) | PIs prefer visual; Friday codebase reusable | ✅ Good |
| Local LLMs only (Ollama/llama.cpp) | Zero cost; privacy; data never leaves institution | ✅ Good |
| PI-provided anonymized PDFs as corpus | Immediate availability; FOIA too slow | ✅ Good |
| Compliance validator in prototype | Critical differentiator; NIH rejects non-compliant | ✅ Good |
| Git-backed version control | PIs expect track changes; enables iteration history | ✅ Good |
| Fine granularity (7 phases) | 1-week sprint; each phase ~1 day; parallelizable | ✅ Good |
| Model profile: inherit | Uses current session model; works with local Ollama | ✅ Good |
| Compact content: yes | Smaller context footprint for long sessions | ✅ Good |

---

## Context Updates

**2026-10-07:** Project initialized via `/gsd-new-project`. Research completed (STACK, FEATURES, ARCHITECTURE, PITFALLS, SUMMARY). REQUIREMENTS.md (37 v1 requirements) and ROADMAP.md (7 phases, fine granularity, MVP mode) created. Config: YOLO mode, fine granularity, parallel execution, git tracking, inherit model profile, research+plan_check+verifier enabled, compact content on, drift guard on.

**PI Partners:** 2-3 identified co-design partners with anonymized funded R01s for corpus.

**Stack Confirmed:** Python 3.11+ (LangGraph, ChromaDB, Ollama, python-docx, PyMuPDF) + React 18/TypeScript/Vite (use-local-llm, Tailwind). Models: Llama-3.1-8B-Instruct-Q4_K_M primary.

**Critical Risks Tracked:**
1. Local LLM quality for 12-page Strategy → mitigated by section-by-section + few-shot + iterative loop
2. FOA compliance variability → mitigated by FOA parser → YAML config
3. RAG relevance for niche domains → mitigated by hybrid search + PI tagging
4. Anonymization failures → mitigated by multi-layer + PI review UI

---

## Next Actions

1. **Start Phase 1:** Create project structure, config files, FOA parser, Planner agent
2. **Parallel:** Begin React UI setup (Vite + TypeScript + use-local-llm) — can start Day 2
3. **Prepare PI onboarding:** 1-page data requirements doc for pilot partners
4. **Test models:** `ollama pull llama3.1:8b-instruct-q4_K_M` and verify inference

---

## Artifacts Index

| Artifact | Location | Last Modified |
|----------|----------|---------------|
| PROJECT.md | `.planning/PROJECT.md` | 2026-10-07 |
| config.json | `.planning/config.json` | 2026-10-07 |
| STACK.md | `.planning/research/STACK.md` | 2026-10-07 |
| FEATURES.md | `.planning/research/FEATURES.md` | 2026-10-07 |
| ARCHITECTURE.md | `.planning/research/ARCHITECTURE.md` | 2026-10-07 |
| PITFALLS.md | `.planning/research/PITFALLS.md` | 2026-10-07 |
| SUMMARY.md | `.planning/research/SUMMARY.md` | 2026-10-07 |
| REQUIREMENTS.md | `.planning/REQUIREMENTS.md` | 2026-10-07 |
| ROADMAP.md | `.planning/ROADMAP.md` | 2026-10-07 |
| STATE.md | `.planning/STATE.md` | 2026-10-07 |

---

*This file is updated at each phase transition and milestone. See PROJECT.md ## Evolution for update rules.*