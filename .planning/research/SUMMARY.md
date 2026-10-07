# Research Summary: Grant Writing AI

**Domain:** Autonomous Grant Writing Pipeline for NIH R01 Applications
**Researched:** 2026-10-07
**Overall confidence:** HIGH

## Executive Summary

The Grant Writing AI prototype targets a well-defined, high-value problem: reducing NIH R01 grant preparation from 6 weeks to 4 hours using a local, zero-cost multi-agent pipeline. Research confirms the technical approach is feasible with current local LLM capabilities (Llama-3.1-8B, Nemotron-3-Ultra via Ollama/llama.cpp), but success hinges on three critical factors: (1) section-by-section generation with heavy RAG grounding from PI-provided PDFs, (2) externalized compliance rules parsed from FOA PDFs rather than hardcoded, and (3) human decision gates at Specific Aims and full-draft review points. The React web UI (reusing Friday patterns) with use-local-llm hooks provides the right PI interaction model. The 1-week timeline is aggressive but achievable by leveraging existing codebases (Friday, friday-assistant, S_Agent) and focusing on the R01 happy path only.

## Key Findings

**Stack:** Python 3.11+ (LangGraph, ChromaDB, Ollama, python-docx) + React 18/TypeScript/Vite (use-local-llm) — all local, zero API cost. Models: Llama-3.1-8B-Instruct-Q4_K_M primary, Nemotron-3-Ultra-Q4 for complex sections.

**Architecture:** LangGraph state machine orchestrating 5 agents (Planner→Retriever→Drafter→Critic→Formatter) with shared infrastructure (ChromaDB, Ollama, Git, Config). Section-aware RAG retrieval. Compliance rules as YAML config parsed from FOA. Git commits per agent pass.

**Critical pitfall:** Local LLM quality for 12-page coherent Research Strategy — mitigated by section-by-section generation, few-shot from PI grants, iterative Drafter↔Critic loops (2-3 rounds), and optional API fallback for pilot validation.

## Implications for Roadmap

Based on research, suggested phase structure:

1. **Phase 1: Foundation & Planner** — Project setup, config, FOA parser, Planner agent, ApplicationPlan data model. Establishes structure for everything downstream.
   - Addresses: REQ-01, REQ-08 (ingestion pipeline)
   - Avoids: Pitfall 2 (FOA variability) by building parser first

2. **Phase 2: RAG & Retriever** — ChromaDB setup, anonymization pipeline, PDF ingestion, section-aware Retriever agent, hybrid search (BM25 + vector).
   - Addresses: REQ-02, REQ-08
   - Avoids: Pitfall 3 (retrieval relevance) via hybrid search + PI tagging

3. **Phase 3: Drafter Core (Aims + Strategy)** — Drafter agent with section-by-section generation, few-shot prompt templates from PI grants, iterative refinement loop with Critic feedback.
   - Addresses: REQ-03 (core)
   - Avoids: Pitfall 1 (LLM quality) via sectioning + few-shot + iteration

4. **Phase 4: Critic & Compliance** — Critic agent with externalized YAML rules, FOA-parsed config, cross-section consistency checks, page limit validation via test render.
   - Addresses: REQ-04
   - Avoids: Pitfall 2 (compliance) + Pitfall 7 (consistency)

5. **Phase 5: Formatter & DOCX Export** — Formatter agent, python-docx NIH template, biosketch tables, budget justification, page count verification loop.
   - Addresses: REQ-05, REQ-03 (biosketch/budget)
   - Avoids: Pitfall 5 (biosketch format) + Pitfall 6 (budget rules)

6. **Phase 6: React UI & Human Gates** — Vite/React/TS UI, upload, metadata entry, gate reviews (Aims, full draft), diff view, DOCX download, progress polling.
   - Addresses: REQ-06, REQ-09
   - Avoids: Pitfall 11 (UI sync) via persistent state + polling

7. **Phase 7: Integration & Pilot Prep** — End-to-end pipeline, Git versioning, anonymization audit, PI onboarding docs, test with 2-3 partner PIs.
   - Addresses: REQ-07, REQ-08, REQ-10
   - Avoids: Pitfall 4 (anonymization) + Pitfall 8 (Git noise)

**Phase ordering rationale:**
- Planner first: everything depends on ApplicationPlan structure
- RAG before Drafter: Drafter needs retrieved context
- Drafter before Critic: Critic validates Drafter output
- Formatter last: needs validated drafts
- UI in parallel with Phases 3-5: can be built incrementally, integrated at gates
- Integration last: validates full flow with real PI data

**Research flags for phases:**
- Phase 3 (Drafter): Likely needs deeper research on prompt templates for each section type
- Phase 5 (Formatter): Page count verification loop may need research on python-docx pagination
- Phase 7: PI feedback will drive post-prototype research

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Proven local LLM stack; Friday codebase reusable; all components have working examples |
| Features | HIGH | Clear NIH R01 requirements; table stakes well-defined; differentiators validated by competitor analysis |
| Architecture | HIGH | LangGraph + Ollama pattern documented; section-aware RAG is standard practice; compliance-as-config is sound |
| Pitfalls | HIGH | All critical pitfalls have concrete mitigations; based on real local LLM benchmarks and NIH compliance docs |

## Gaps to Address

- **Prompt templates per section:** Need few-shot examples from PI's anonymized grants for Specific Aims, Significance, Innovation, Approach, Biosketch, Budget — will collect during Phase 1-2 with PI partners
- **FOA parser coverage:** Need to test against 10+ real FOA PDFs to ensure rule extraction completeness — Phase 1 deliverable
- **Local model selection:** Nemotron-3-Ultra availability on Ollama uncertain; may need direct llama.cpp — test in Phase 1
- **Page count verification:** python-docx doesn't render to pages; need test-render approach (LibreOffice headless or PDF conversion) — Phase 5 research
- **Anonymization audit:** Need institutional IRB review of anonymization pipeline — Phase 7, before pilot