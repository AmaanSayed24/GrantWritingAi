# Requirements: Grant Writing AI

**Project:** Grant Writing AI
**Version:** v1 (Prototype)
**Date:** 2026-10-07

---

## v1 Requirements

### Authentication & Project Setup

- [ ] **REQ-01**: Planner agent parses FOA PDF and extracts structured requirements (page limits, sections, formatting rules, special attachments)
- [ ] **REQ-02**: Planner agent creates ApplicationPlan data model with all sections, page limits, and FOA-specific rules
- [ ] **REQ-03**: UI allows PI to upload FOA PDF and enter project metadata (title, PIs, institution, dates)

### RAG & Retrieval

- [ ] **REQ-04**: Anonymization pipeline scrubs PI PDFs (names, institutions, grant numbers, collaborator names) before any processing
- [ ] **REQ-05**: PDF ingestion pipeline extracts text, chunks with overlap, generates embeddings (sentence-transformers), stores in ChromaDB
- [ ] **REQ-06**: NIH RePORTER API integration fetches relevant funded grant abstracts for PI's research area
- [ ] **REQ-07**: Retriever agent performs section-aware hybrid search (BM25 + vector) per ApplicationPlan section
- [ ] **REQ-08**: Retriever returns ranked chunks with source citations for Drafter grounding

### Drafting (Core Pipeline)

- [ ] **REQ-09**: Drafter agent generates Specific Aims (1 page): hypothesis, 2-3 independent aims, expected outcomes, impact
- [ ] **REQ-10**: Drafter agent generates Research Strategy (12 pages): Significance, Innovation, Approach per NIH structure
- [ ] **REQ-11**: Drafter agent generates Biosketches (5 pages each, 2026 Common Form + Supplement) for all senior/key personnel
- [ ] **REQ-12**: Drafter agent generates Budget Justification text for all categories (personnel, equipment, supplies, travel, other)
- [ ] **REQ-13**: Drafter uses few-shot examples from PI's anonymized grants for each section type
- [ ] **REQ-14**: Drafter iterates 2-3 times per section based on Critic feedback (Drafter→Critic→Drafter loop)

### Compliance & Validation

- [ ] **REQ-15**: Critic agent validates page limits per section (FOA-specific + base R01 rules)
- [ ] **REQ-16**: Critic agent validates format: Arial 11pt, 0.5" margins, single spacing, headers/footers, page numbering
- [ ] **REQ-17**: Critic agent validates budget rules: effort %, equipment thresholds, foreign travel, modular budget
- [ ] **REQ-18**: Critic agent validates cross-section consistency: Aims count matches Strategy, personnel in Budget match Biosketches, preliminary data referenced in Significance
- [ ] **REQ-19**: Critic agent validates required sections present per FOA (no missing attachments)
- [ ] **REQ-20**: Compliance rules stored as external YAML config (base + FOA-specific), not hardcoded

### Formatting & Export

- [ ] **REQ-21**: Formatter agent generates NIH-compliant DOCX from validated drafts
- [ ] **REQ-22**: DOCX uses proper styles: heading hierarchy, body text, table styles, page numbering (bottom-right)
- [ ] **REQ-23**: Biosketch tables render correctly (Contributions to Science, Positions & Honors, Research Support)
- [ ] **REQ-24**: Page count verification: render → count → adjust → re-render loop until within limits
- [ ] **REQ-25**: Final DOCX package includes all attachments in correct order per FOA

### UI & Human Gates

- [ ] **REQ-26**: React UI: FOA/PDF upload, metadata entry, model selection (Ollama models)
- [ ] **REQ-27**: Human Gate 1: PI reviews/edits Specific Aims draft → approves to continue
- [ ] **REQ-28**: Human Gate 2: PI reviews/edits full draft (Strategy, Biosketches, Budget) → approves to continue
- [ ] **REQ-29**: Human Gate 3: PI final review of formatted DOCX → downloads
- [ ] **REQ-30**: UI shows retrieved chunks per section for PI verification
- [ ] **REQ-31**: UI shows real-time progress (agent status, estimated time remaining)
- [ ] **REQ-32**: UI allows PI to edit drafts at gates with structured forms (not free text)

### Infrastructure

- [ ] **REQ-33**: Git repo initialized; Orchestrator commits after each agent pass with structured messages
- [ ] **REQ-34**: Git branches: `agent/drafts` (agent output), `pi/edits` (PI modifications), `main` (approved)
- [ ] **REQ-35**: Configuration via `.planning/config.json` and `config/grants.yaml` (compliance rules)
- [ ] **REQ-36**: Local LLM via Ollama (primary) with llama.cpp fallback; model configurable
- [ ] **REQ-37**: Anonymization audit log: what was redacted, confidence, PI review confirmation

---

## v2 Requirements (Deferred)

- [ ] **REQ-100**: Study-section-specific language tuning (requires funded grant corpus)
- [ ] **REQ-101**: NSF GRFP / CAREER / Standard Grant support
- [ ] **REQ-102**: Private foundation formats (Gates, HHMI, etc.)
- [ ] **REQ-103**: Full budget builder UI (not just justification text)
- [ ] **REQ-104**: Multi-user collaboration / team workspaces
- [ ] **REQ-105**: Cloud deployment option (hosted API)
- [ ] **REQ-106**: FOIA-funded grant corpus ingestion pipeline
- [ ] **REQ-107**: Real-time reviewer simulation ("Reviewer 2 would ask...")
- [ ] **REQ-108**: Advanced anonymization (ML-based PII detection)
- [ ] **REQ-109**: Grant calendar / deadline tracking
- [ ] **REQ-110**: Co-PI / multi-institution workflow

---

## Out of Scope (Explicit Exclusions)

| Exclusion | Reason |
|-----------|--------|
| NSF/private foundation formats | Scope creep; different rules; extensibility designed in for post-prototype |
| Full-text funded grant corpus via FOIA | Legal burden; 6+ months; start with PI-provided PDFs |
| Multi-user/team workspaces | Auth, permissions, sync complexity; single-PI prototype first |
| Cloud deployment / hosted API | Privacy, cost, institutional policy; local-only prototype |
| Synthetic training data | Unrealistic; doesn't capture real grant language |
| Fine-tuning models | GPU cost; time; data needs; RAG + prompting sufficient for prototype |
| Full budget entry UI | NIH budget template + justification text sufficient for prototype |
| Collaboration features | Single-PI first; real-time sync complex |
| Scanned PDF OCR | Edge case; warn PI; tesseract fallback if needed post-prototype |
| Mobile UI | PIs work on desktop/laptop; responsive web sufficient |

---

## Traceability

| REQ-ID | Phase | Source |
|--------|-------|--------|
| REQ-01 | 1 | PROJECT.md REQ-01 |
| REQ-02 | 1 | PROJECT.md REQ-01 |
| REQ-03 | 6 | PROJECT.md REQ-06 |
| REQ-04 | 2 | PROJECT.md REQ-08, PITFALLS Pitfall 4 |
| REQ-05 | 2 | PROJECT.md REQ-02, REQ-08 |
| REQ-06 | 2 | PROJECT.md REQ-02 |
| REQ-07 | 2 | PROJECT.md REQ-02, FEATURES Table Stakes |
| REQ-08 | 2 | PROJECT.md REQ-02 |
| REQ-09 | 3 | PROJECT.md REQ-03 |
| REQ-10 | 3 | PROJECT.md REQ-03 |
| REQ-11 | 5 | PROJECT.md REQ-03 |
| REQ-12 | 5 | PROJECT.md REQ-03 |
| REQ-13 | 3 | FEATURES Differentiators, PITFALLS Pitfall 1 |
| REQ-14 | 3 | ARCHITECTURE Pattern 1, PITFALLS Pitfall 1 |
| REQ-15 | 4 | PROJECT.md REQ-04, PITFALLS Pitfall 2 |
| REQ-16 | 4 | PROJECT.md REQ-04 |
| REQ-17 | 4 | PROJECT.md REQ-04, PITFALLS Pitfall 6 |
| REQ-18 | 4 | PROJECT.md REQ-04, PITFALLS Pitfall 7 |
| REQ-19 | 4 | PROJECT.md REQ-04 |
| REQ-20 | 4 | ARCHITECTURE Pattern 3, PITFALLS Pitfall 2 |
| REQ-21 | 5 | PROJECT.md REQ-05 |
| REQ-22 | 5 | PROJECT.md REQ-05 |
| REQ-23 | 5 | PROJECT.md REQ-05, PITFALLS Pitfall 5 |
| REQ-24 | 5 | ARCHITECTURE, PITFALLS Pitfall 5 |
| REQ-25 | 5 | PROJECT.md REQ-05 |
| REQ-26 | 6 | PROJECT.md REQ-06 |
| REQ-27 | 6 | PROJECT.md REQ-09 |
| REQ-28 | 6 | PROJECT.md REQ-09 |
| REQ-29 | 6 | PROJECT.md REQ-09 |
| REQ-30 | 6 | FEATURES Table Stakes |
| REQ-31 | 6 | PITFALLS Pitfall 11 |
| REQ-32 | 6 | PROJECT.md REQ-09 |
| REQ-33 | 7 | PROJECT.md REQ-10 |
| REQ-34 | 7 | ARCHITECTURE Pattern 4 |
| REQ-35 | 1 | PROJECT.md Constraints |
| REQ-36 | 1 | PROJECT.md Constraints |
| REQ-37 | 7 | PROJECT.md REQ-08, PITFALLS Pitfall 4 |

---

*Generated from PROJECT.md and research artifacts. Update at each phase transition.*