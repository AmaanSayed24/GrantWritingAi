# Grant Writing AI

## What This Is

An autonomous grant writing pipeline for research organizations (universities, hospitals, nonprofits) that reduces 6 weeks of professor time to 4 hours for NIH R01 applications. A multi-agent system: Planner → Retriever → Drafter → Critic → Formatter, running locally with zero API costs via llama.cpp/ollama. PIs interact through a React web UI (like Friday). Target: working prototype in 1 week for 2-3 co-design PI partners.

## Core Value

End-to-end R01 draft generation (Specific Aims, Research Strategy, Biosketches, Budget) with compliance validation — all local, all free, human-in-the-loop at decision points.

## Business Context

- **Customer**: University PIs, research administrators, grant consultants
- **Revenue model**: SaaS per submission / seat license after pilot validation
- **Success metric**: Hours saved per grant × submission success rate lift
- **Strategy notes**: See Obsidian "Grant Writing AI" note for full strategy

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] **REQ-01**: Planner agent structures R01 application per FOA requirements (page limits, sections, formatting rules)
- [ ] **REQ-02**: Retriever agent performs RAG over user-provided PDFs + NIH RePORTER abstracts for relevant prior work
- [ ] **REQ-03**: Drafter agent writes Specific Aims (1 page), Research Strategy (12 pages), Biosketches (5 pages each), Budget justification
- [ ] **REQ-04**: Critic agent validates compliance: page limits, format (margins, font, headers), budget rules, section completeness, cross-section consistency
- [ ] **REQ-05**: Formatter agent exports NIH-compliant DOCX with proper styles, headers/footers, page numbering, biosketch tables
- [ ] **REQ-06**: React web UI for PIs: upload PDFs, enter project metadata, review/edit drafts at each stage, download final DOCX
- [ ] **REQ-07**: Local LLM inference via llama.cpp/ollama (zero API cost) with model selection (e.g., Llama-3.1-8B, Nemotron-3-Ultra)
- [ ] **REQ-08**: Anonymized funded grant corpus ingestion pipeline (PI-provided PDFs → chunked → embedded → vector store)
- [ ] **REQ-09**: Human decision gates: hypothesis approval, aim ordering, strategy direction, final sign-off
- [ ] **REQ-10**: Version control for drafts (git-backed) with change tracking between iterations

### Out of Scope

- NSF/private foundation formats — defer to post-prototype (extensibility designed in)
- Full-text funded grant corpus via FOIA — legal/time burden; start with PI-provided PDFs
- Multi-user collaboration / team workspaces — single-PI prototype first
- Cloud deployment / hosted API — local-only prototype
- Advanced study-section-specific tuning — requires corpus we don't have yet
- Budget builder UI — use NIH budget template; justification text only in prototype

## Context

- **Technical environment**: Python 3.11+ for agents/RAG, React 18+ for UI, llama.cpp/ollama for local LLM, Chroma/FAISS for vector store, python-docx for DOCX export
- **Prior work**: Friday (React/Node AI assistant), friday-assistant (Python agent framework), S_Agent (CampusWatch agent), llama.cpp skill, docx skill, ECC multi-agent orchestration
- **User research**: 2-3 PI co-design partners identified; they have anonymized funded R01s for corpus
- **Known issues**: Local LLM quality for long-form structured writing; compliance rule encoding complexity; RAG retrieval relevance for niche domains

## Constraints

- **Tech stack**: Python + React + llama.cpp/ollama only — no external API dependencies
- **Timeline**: 1 week prototype (spike pace)
- **Budget**: $0 — all local, open-source models and tools
- **Dependencies**: Must leverage existing Friday/friday-assistant/S_Agent code patterns
- **Compatibility**: NIH R01 FOA requirements (SF424 R&R format, page limits, font: Arial 11pt, 0.5" margins)
- **Performance**: Full pipeline < 30 min on consumer GPU (RTX 3080/4080 class) or CPU fallback
- **Security**: Anonymization of PI-provided PDFs before any processing; no data leaves machine

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Target NIH R01 only for prototype | Highest volume, most structured format, PI partners are NIH-funded | — Pending |
| Full pipeline in prototype (not just Aims) | Validates end-to-end flow; partial pipeline hides integration issues | — Pending |
| React web UI (like Friday) | PIs prefer visual interface; Friday codebase reusable | — Pending |
| Local LLMs only (llama.cpp/ollama) | Zero cost; privacy; PI data never leaves institution | — Pending |
| PI-provided anonymized PDFs as corpus | Immediate availability; FOIA too slow; synthetic data unrealistic | — Pending |
| Compliance validator in prototype | Critical differentiator; NIH rejects non-compliant automatically | — Pending |
| Git-backed version control for drafts | PIs expect track changes; enables iteration history | — Pending |

---

*Last updated: 2026-10-07 after initialization*

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state