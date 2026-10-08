---
last_mapped_commit: 608c6728678e22a32e463bee82bf321f2f44f9e8
last_mapped_at: 2026-10-08
---
# External Integrations

**Project:** Grant Writing AI  
**Analysis Date:** 2026-10-08  
**Scope:** Full repository

---

## Overview

Grant Writing AI is designed to run **entirely locally** with **zero external API dependencies** for the core pipeline. All LLM inference, vector storage, and document processing happen on the user's machine. The only external integrations are optional data sources and the local Ollama service.

---

## Local Services (Required)

### Ollama

| Aspect | Details |
|--------|---------|
| **Type** | Local LLM inference server |
| **Protocol** | HTTP (OpenAI-compatible API) |
| **Default Endpoint** | `http://localhost:11434` |
| **Auth** | None (local only) |
| **Models Used** | `llama3.1:8b-instruct-q4_K_M` (primary), `nemotron3:ultra-q4` (optional) |
| **Purpose** | All text generation: planning, drafting, critique, formatting |
| **Dependency** | Required — must be installed and running (`ollama serve`) |

---

## Optional External Data Sources

### NIH RePORTER API

| Aspect | Details |
|--------|---------|
| **Type** | Public REST API |
| **Base URL** | `https://api.reporter.nih.gov/v2/` |
| **Auth** | None (public) |
| **Rate Limits** | ~120 requests/minute (unofficial) |
| **Purpose** | Fetch funded grant abstracts, PI publications, similar projects for RAG context |
| **Integration Point** | Phase 2: Retriever agent — supplements PI-provided PDFs with public literature |
| **Data Retrieved** | Project titles, abstracts, PIs, institutions, funding years, MeSH terms |
| **Usage** | Optional enhancement; pipeline works with PI PDFs only |

#### Example Queries

```
GET /projects/search
  - criteria: { pi_names: ["Smith J"], fiscal_years: [2023, 2024] }
  - fields: ["project_title", "abstract_text", "terms", "principal_investigators"]

```

---

## File-Based Integrations (Input/Output)

### Input: FOA PDF

| Aspect | Details |
|--------|---------|
| **Format** | PDF (Funding Opportunity Announcement) |
| **Source** | User upload via UI or CLI `--foa` argument |
| **Processing** | PyMuPDF text extraction → FOA parser → structured config |
| **Output** | `FOAConfig` / `MergedFOAConfig` (page limits, required sections, special instructions) |

### Input: PI Reference PDFs

| Aspect | Details |
|--------|---------|
| **Format** | PDF (previously funded grants, papers, biosketches) |
| **Source** | User upload via UI (multi-file) or CLI `--pdfs` directory |
| **Processing** | Anonymization → PyMuPDF/pdfplumber extraction → chunking → embedding → ChromaDB |
| **Privacy** | Never leaves local machine; anonymized before embedding |

### Output: NIH-Compliant DOCX

| Aspect | Details |
|--------|---------|
| **Format** | `.docx` (Microsoft Word) |
| **Generator** | `python-docx` with NIH template styles |
| **Sections** | Specific Aims, Research Strategy, Biosketches, Budget Justification, all attachments |
| **Validation** | Page counts verified via LibreOffice headless PDF conversion |
| **Delivery** | Downloaded via UI or written to output directory via CLI |

---

## Configuration Integration

### Base Configuration: `config/grants.yaml`

- **Type**: YAML file
- **Loads at**: Startup (via `src.config.loader.load_grants_config`)
- **Contains**: Page limits, format rules, budget rules, validation checks, ERA Commons checks
- **Schema**: Validated by `GrantsConfig` Pydantic model

### FOA Override: `config/foa-{id}.yaml`

- **Type**: YAML file (optional, per FOA)
- **Loads at**: Pipeline start for specific FOA (via `load_foa_config`)
- **Merges with**: Base config via deep merge (`src.config.merge.deep_merge`)
- **Priority**: FOA values override base config
- **Schema**: Validated by `FOAConfig` Pydantic model

---

## Version Control Integration (Git)

### Branching Strategy

| Branch | Purpose | Commits By |
|--------|---------|------------|
| `main` | Approved, finalized application | PI (Gate 3 approval) |
| `pi/edits` | PI review edits at each gate | PI (via UI) |
| `agent/drafts` | Auto-commits per agent iteration | Orchestrator (automated) |

### Commit Message Format

```
<agent>|<model>|<chunks_used>|<req_ids>|<gate_status>
Example: drafter|llama3.1:8b|12|REQ-09,REQ-10|gate1-pending
```

### Automation

- Agent commits: Auto-commit after each section draft/revision
- PI commits: Commit on "Approve" at each gate
- Merge: `pi/edits` → `main` on final approval

---

## Development Tool Integrations

| Tool | Integration Type | Purpose |
|------|------------------|---------|
| **pytest** | Test runner | Unit tests for types, config, merge; integration tests for pipeline |
| **ruff** | Linter/formatter | Pre-commit / CI checks (line length, imports, style) |
| **mypy** | Type checker | Strict type validation on all source |
| **GitHub Actions** (planned) | CI/CD | Lint, type-check, test on PR |

---

## Future / Planned Integrations (Out of MVP Scope)

| Integration | Purpose | Phase |
|-------------|---------|-------|
| **NSF API** | NSF grant format support | v2+ |
| **FOIA Request Automation** | Public corpus for RAG | v2+ |
| **Institutional HR/Finance Systems** | Auto-populate biosketches, budgets | v2+ |
| **eRA Commons Validation API** | Pre-submission format check | v2+ |
| **Cloud Deployment (AWS/GCP/Azure)** | Shared institutional deployment | v2+ |
| **Collaborative Editing (Yjs/Automerge)** | Multi-PI real-time editing | v2+ |

---

## Security & Privacy Model

| Principle | Implementation |
|-----------|----------------|
| **Zero Data Egress** | All processing local; no telemetry, no API calls to external LLMs |
| **Anonymization First** | PI PDFs redacted (names, institutions, grant IDs) before embedding |
| **PI Control** | PI reviews all redactions in UI before ingestion |
| **Local Models Only** | Ollama/llama.cpp; no OpenAI, Anthropic, or other cloud APIs |
| **Audit Log** | JSONL log of all anonymization decisions with confidence scores |

---

## Network Requirements

| Component | Network Access |
|-----------|----------------|
| Ollama | Localhost only (11434) |
| NIH RePORTER | HTTPS outbound (optional, Phase 2+) |
| Model Downloads | HTTPS outbound (one-time `ollama pull`) |
| All Other | None — fully air-gapped capable |

---

## Summary Table

| Integration | Required | Type | Auth | Data Direction |
|-------------|----------|------|------|----------------|
| Ollama | ✅ Yes | Local HTTP | None | Bidirectional (prompts ↔ completions) |
| NIH RePORTER | ❌ Optional | Public REST | None | Inbound (abstracts, metadata) |
| FOA PDF | ✅ Yes | File upload | None | Inbound (config) |
| PI PDFs | ✅ Yes | File upload | None | Inbound (corpus) |
| DOCX Output | ✅ Yes | File download | None | Outbound (final application) |
| Git | ✅ Yes | Local VCS | SSH/HTTPS (remote) | Bidirectional (version history) |

---

*Generated by codebase analysis on 2026-10-08*
