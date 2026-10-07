# Roadmap: Grant Writing AI

**Project:** Grant Writing AI
**Version:** v1 (Prototype)
**Date:** 2026-10-07
**Granularity:** Fine
**Mode:** mvp

---

## Phase Overview

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Foundation & Planner | Project setup, config, FOA parser, Planner agent, ApplicationPlan model | REQ-01, REQ-02, REQ-03, REQ-35, REQ-36 | FOA PDF → structured ApplicationPlan; config loads; Ollama connects |
| 2 | RAG & Retriever | ChromaDB, anonymization, PDF ingestion, RePORTER, section-aware hybrid Retriever | REQ-04, REQ-05, REQ-06, REQ-07, REQ-08 | PI PDFs → anonymized → embedded → retrieved per section with citations |
| 3 | Drafter Core (Aims + Strategy) | Section-by-section Drafter, few-shot templates, iterative refine loop (2-3 rounds) | REQ-09, REQ-10, REQ-13, REQ-14 | Specific Aims (1pg) + Research Strategy (12pg) grounded in retrieved context |
| 4 | Critic & Compliance | Externalized YAML rules, FOA-parsed config, cross-section checks, page validation | REQ-15, REQ-16, REQ-17, REQ-18, REQ-19, REQ-20 | All compliance rules pass; cross-section consistency validated |
| 5 | Formatter & DOCX Export | python-docx NIH template, biosketch tables, budget justification, page count loop | REQ-21, REQ-22, REQ-23, REQ-24, REQ-25 | NIH-compliant DOCX within page limits; all attachments ordered |
| 6 | React UI & Human Gates | Vite/React/TS, upload, metadata, 3 gates (Aims, Full Draft, Final), progress polling | REQ-26, REQ-27, REQ-28, REQ-29, REQ-30, REQ-31, REQ-32 | PI completes full flow: upload → gate reviews → download DOCX |
| 7 | Integration & Pilot Prep | End-to-end pipeline, Git versioning, anonymization audit, PI onboarding, 2-3 PI test | REQ-33, REQ-34, REQ-37, REQ-03, REQ-09 | 2-3 PIs produce valid R01 drafts; feedback captured |

---

## Phase Details

### Phase 1: Foundation & Planner
**Goal:** Project setup, configuration, FOA parser, Planner agent, ApplicationPlan data model
**Mode:** mvp
**Requirements:** REQ-01, REQ-02, REQ-03, REQ-35, REQ-36

**Success Criteria:**
1. `git init` + `.planning/` structure committed
2. `config.json` and `config/grants.yaml` (base R01 rules) load correctly
3. Ollama runs locally; `ollama list` shows target models
4. FOA parser extracts: page limits per section, required attachments, formatting rules, special instructions
5. Planner agent outputs `ApplicationPlan` (TypedDict/Pydantic) with all sections, limits, rules
6. Unit tests: FOA parser on 3+ real FOA PDFs; Planner output validated

### Phase 2: RAG & Retriever
**Goal:** ChromaDB setup, anonymization pipeline, PDF ingestion, RePORTER integration, section-aware hybrid Retriever
**Mode:** mvp
**Requirements:** REQ-04, REQ-05, REQ-06, REQ-07, REQ-08

**Success Criteria:**
1. Anonymization pipeline: regex + spaCy NER redacts names, institutions, grant numbers; PI reviews redactions in UI
2. PDF ingestion: PyMuPDF extracts text → chunked (500 tokens, 100 overlap) → embedded (all-MiniLM-L6-v2) → ChromaDB
3. RePORTER API: fetches abstracts for PI's research area (MeSH terms from metadata)
4. Retriever agent: hybrid search (BM25 + vector, 50/50 weight) per section query template
5. Retriever returns: ranked chunks with source (PI PDF vs RePORTER), relevance scores, section mapping
6. Integration test: PI uploads 5 PDFs → anonymized → ingested → Retriever returns relevant chunks for each section

### Phase 3: Drafter Core (Aims + Strategy)
**Goal:** Section-by-section Drafter agent, few-shot prompt templates from PI grants, iterative refinement loop with Critic
**Mode:** mvp
**Requirements:** REQ-09, REQ-10, REQ-13, REQ-14

**Success Criteria:**
1. Drafter generates Specific Aims (1 page): hypothesis, 2-3 independent aims, expected outcomes, impact statement
2. Drafter generates Research Strategy (12 pages): Significance, Innovation, Approach with subsections
3. Few-shot templates: 3-5 examples per section from PI's anonymized grants
3. Iterative loop: Drafter → Critic feedback → Drafter revision (2-3 rounds per section)
4. Output: structured `SectionDraft` per section with metadata (model, chunks used, iteration count)
5. Human Gate 1: PI reviews Specific Aims in UI; approves/edits; Orchestrator continues
6. Quality: PI rates Aims draft ≥4/5 on relevance, specificity, feasibility

### Phase 4: Critic & Compliance
**Goal:** Critic agent with externalized YAML rules, FOA-parsed config, cross-section consistency checks, page limit validation
**Mode:** mvp
**Requirements:** REQ-15, REQ-16, REQ-17, REQ-18, REQ-19, REQ-20

**Success Criteria:**
1. Compliance rules loaded from `config/grants.yaml` (base) + `config/foa-{id}.yaml` (FOA-specific)
2. Page limit validation: test-render each section → count pages → flag overages
3. Format validation: font (Arial 11pt), margins (0.5"), spacing, headers, page numbering
4. Budget rules: effort % ≤100%, equipment >$5k justified, foreign travel pre-approved, modular budget rules
5. Cross-section checks: Aims count = Strategy aims; Budget personnel = Biosketches; preliminary data cited
6. Required attachments check: all FOA-mandated sections present
7. Output: `ValidationReport` with pass/fail per rule, warnings, suggested fixes
8. Test: Run on 3 real FOAs + PI drafts; zero false negatives on compliance

### Phase 5: Formatter & DOCX Export
**Goal:** Formatter agent generates NIH-compliant DOCX, biosketch tables, budget justification, page count verification loop
**Mode:** mvp
**Requirements:** REQ-21, REQ-22, REQ-23, REQ-24, REQ-25

**Success Criteria:**
1. python-docx template: styles for all heading levels, body, tables, headers/footers, page numbering (bottom-right)
2. Biosketch generator: 2026 Common Form + Supplement tables (Contributions, Positions, Research Support)
3. Budget justification: structured text per category from PI-entered numbers
4. Page count loop: render DOCX → LibreOffice headless convert to PDF → count pages → adjust content → repeat (max 3 iterations)
5. Final package: all attachments in FOA-specified order, combined or separate per FOA
6. Output: bytes + metadata (page counts, validation status)
7. Test: Generated DOCX passes NIH format checker (Proposia/text-to-space)

### Phase 6: React UI & Human Gates
**Goal:** Vite/React/TypeScript UI with upload, metadata, 3 human gates, progress polling, diff view
**Mode:** mvp
**Requirements:** REQ-26, REQ-27, REQ-28, REQ-29, REQ-30, REQ-31, REQ-32

**Success Criteria:**
1. Setup: `npm create vite@latest ui -- --template react-ts` + `use-local-llm` + Tailwind CSS
2. Upload page: FOA PDF drag-drop, PI PDFs multi-upload, metadata form (title, PIs, institution, dates)
3. Model selection: dropdown of `ollama list` models; shows VRAM requirements
4. Gate 1 (Specific Aims): side-by-side view (AI draft | PI edit); structured form for each aim; approve button
5. Gate 2 (Full Draft): tabbed view per section; retrieved chunks panel; structured edit forms; approve button
6. Gate 3 (Final): rendered preview (PDF.js); download DOCX; "request revision" loops back to Gate 2
7. Progress: WebSocket/polling shows agent status, chunks retrieved, tokens generated, ETA
8. Anonymization review: PI sees detected redactions before ingestion; can add manual redactions
9. Resume: Orchestrator persists state; PI can close browser and resume at last gate

### Phase 7: Integration & Pilot Prep
**Goal:** End-to-end pipeline, Git versioning, anonymization audit, PI onboarding, 2-3 PI pilot test
**Mode:** mvp
**Requirements:** REQ-33, REQ-34, REQ-37, REQ-03, REQ-09

**Success Criteria:**
1. Git workflow: `agent/drafts` branch (auto-commits per agent), `pi/edits` branch (PI gate commits), `main` (approved)
2. Commit messages: structured (agent, model, chunks, REQ-IDs, gate status)
3. Anonymization audit log: JSONL with detected entities, confidence, PI confirmation
4. PI onboarding doc: 1-page quickstart, data requirements, expected timeline, known limitations
5. Pilot test: 2-3 PIs run full pipeline on real R01 FOAs with their anonymized PDFs
6. Metrics captured: time saved (target: 6 weeks → 4 hours), PI satisfaction (≥4/5), compliance pass rate (100%)
7. Feedback logged: per-section quality, UI usability, missing features, model preferences
8. Go/No-Go decision: documented with evidence for Phase 2 funding

---

## MVP Scope Boundary

**In Scope (Phases 1-7):**
- NIH R01 only (parent announcements + common RFAs)
- Local-only (Ollama/llama.cpp)
- Single PI workflow
- 3 human gates
- Anonymization + Git versioning
- DOCX export (NIH-compliant)

**Out of Scope (v2+):**
- NSF / foundation formats
- Study-section tuning
- Cloud deployment
- Multi-user / collaboration
- Full budget builder UI
- FOIA corpus
- Reviewer simulation
- Mobile UI

---

## Timeline (1 Week Sprint)

| Day | Phase | Deliverable |
|-----|-------|-------------|
| Day 1 | 1 | Foundation, config, FOA parser, Planner, ApplicationPlan |
| Day 2 | 2 | ChromaDB, anonymization, ingestion, RePORTER, Retriever |
| Day 3 | 3 | Drafter (Aims + Strategy), few-shot templates, iterative loop, Gate 1 |
| Day 4 | 4 | Critic, compliance YAML, cross-checks, page validation |
| Day 5 | 5 | Formatter, DOCX template, biosketch tables, page count loop |
| Day 6 | 6 | React UI, 3 gates, progress polling, anonymization review |
| Day 7 | 7 | Integration, Git workflow, pilot prep, PI test run |

**Buffer:** Phases can run in parallel where independent (e.g., UI Phase 6 starts Day 3 alongside Drafter)

---

*Generated by gsd-roadmapper. Approve to commit.*