# Feature Landscape

**Domain:** Autonomous Grant Writing Pipeline (NIH R01)
**Researched:** 2026-10-07

## Table Stakes

Features users expect. Missing = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Specific Aims generator (1 page) | Core of every R01; reviewers decide here | Medium | 2-3 independent aims with hypothesis, outcomes, impact |
| Research Strategy writer (12 pages) | Main technical content: Significance, Innovation, Approach | High | Must follow NIH structure; 12-page limit |
| Biosketch generator (5 pages each) | Required for every senior/key person | Medium | 2026 Common Form + Supplement format |
| Budget justification writer | Required attachment; detailed rules | Medium | Modular: personnel, equipment, supplies, travel, other |
| Compliance validator | NIH auto-rejects non-compliant; critical differentiator | High | Page limits, font (Arial 11pt), margins (0.5"), headers, section completeness |
| DOCX export (NIH-compliant) | Submission requires specific formatting | Medium | Styles, page numbering, headers/footers, tables |
| RAG over user PDFs | PIs have prior grants, papers, preliminary data | Medium | ChromaDB + sentence-transformers; anonymization first |
| NIH RePORTER integration | Find relevant funded grants for context | Low | Public API; abstracts only (no full text) |
| Human decision gates | PI must approve hypothesis, aims, strategy | Low | UI checkpoints between agents |
| Version control for drafts | PIs expect track changes; iteration history | Low | Git-backed; commit per agent pass |

## Differentiators

Features that set product apart. Not expected, but valued.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Multi-agent pipeline (not chat wrapper) | Each agent specialized; better quality than single-pass | High | Planner→Retriever→Drafter→Critic→Formatter |
| Study-section-aware language tuning | Different reviewers = different language preferences | High | Requires corpus; defer to post-prototype |
| Cross-section consistency checker | Ensures Aims match Strategy match Budget | Medium | Critic agent validates alignment |
| Anonymization pipeline | PI data never leaves machine; institutional compliance | Medium | Regex + NER for names, institutions, grant numbers |
| Real-time collaboration hints | "Reviewer 2 typically asks about..." | High | Requires corpus; defer |
| Grant-specific FOA parser | Auto-extracts requirements from PDF FOA | Medium | PDF parsing + structured extraction |
| Budget builder with NIH templates | Not just justification; full budget entry | Medium | Use NIH budget template; justification text in prototype |

## Anti-Features

Features to explicitly NOT build.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Cloud-hosted API | Privacy, cost, institutional policy | Local-only (Ollama/llama.cpp) |
| NSF/private foundation formats | Scope creep; different rules | Extensibility designed in; R01 only for prototype |
| Full-text funded grant corpus via FOIA | Legal burden; 6+ months | Start with PI-provided anonymized PDFs |
| Multi-user/team workspaces | Auth, permissions, sync complexity | Single-PI prototype first |
| Synthetic training data | Unrealistic; doesn't capture real grant language | Use real anonymized PI PDFs |
| Fine-tuning models | GPU cost; time; data needs | RAG + prompt engineering for prototype |

## Feature Dependencies

```
RAG pipeline → Retriever agent → Drafter agent
Planner agent → FOA parser → All downstream agents
Compliance rules → Critic agent → Formatter agent
DOCX generator → Formatter agent → UI download
Anonymization → All agents (pre-processing)
Git versioning → UI → All drafts
```

## MVP Recommendation

Prioritize:
1. **Planner + FOA parser** — structures everything downstream
2. **RAG + Retriever** — grounds drafting in PI's actual work
3. **Drafter (Specific Aims + Research Strategy)** — core value
4. **Critic (compliance + consistency)** — differentiator
5. **Formatter + DOCX export** — deliverable
6. **React UI (upload, review, download)** — PI interaction
7. **Biosketch + Budget justification** — complete R01
8. **Version control + anonymization** — production readiness

Defer:
- Study-section tuning: requires corpus we don't have yet
- NSF/foundation formats: extensibility designed in
- Full budget builder: NIH template + justification text sufficient
- Collaboration: single-PI first

## Sources

- NIH R01 Application Guide (grants.nih.gov)
- CASRAI NIH format guides (page limits, biosketch 2026)
- GrantFlux, GrantCopilot, GrantedAI, NIH Payline feature analysis
- Local LLM agent patterns (LangGraph + Ollama)
- python-docx NIH biosketch builder patterns