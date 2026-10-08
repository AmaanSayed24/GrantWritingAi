---
last_mapped_commit: 608c6728678e22a32e463bee82bf321f2f44f9e8
last_mapped_at: 2026-10-08
---
# Technology Stack

**Project:** Grant Writing AI  
**Analysis Date:** 2026-10-08  
**Scope:** Full repository

---

## Language & Runtime

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | >=3.11 | Primary language for agent orchestration, RAG pipeline, DOCX generation |
| Node.js | 18+ | Frontend build and development (React/Vite) |

---

## Core Dependencies (Python)

### Agent Orchestration & LLM

| Package | Version | Purpose |
|---------|---------|---------|
| `langgraph` | >=0.2.0 | Multi-agent workflow orchestration, state management |
| `langchain-core` | >=0.3.0 | Core LangChain abstractions for chains, tools, prompts |
| `ollama` | >=0.4.0 | Local LLM serving via OpenAI-compatible API |

### Data Validation & Configuration

| Package | Version | Purpose |
|---------|---------|---------|
| `pydantic` | >=2.8.0 | Data models, validation, settings management |
| `pydantic-settings` | >=2.4.0 | Environment-based configuration |
| `pyyaml` | >=6.0.1 | YAML configuration file parsing |

### RAG & Vector Search

| Package | Version | Purpose |
|---------|---------|---------|
| `chromadb` | 0.5+ | Local vector database for document embeddings |
| `sentence-transformers` | 2.2+ | Embeddings (all-MiniLM-L6-v2) for semantic search |

### Document Processing

| Package | Version | Purpose |
|---------|---------|---------|
| `pymupdf` (fitz) | >=1.24.0 | PDF text extraction from PI-provided PDFs |
| `pdfplumber` | 0.10+ | Table extraction from PDFs (biosketches, budgets) |
| `python-docx` | 1.1+ | NIH-compliant DOCX generation with styles, tables, headers/footers |

### CLI & Output

| Package | Version | Purpose |
|---------|---------|---------|
| `typer` | >=0.12.0 | CLI command framework |
| `rich` | >=13.7.0 | Terminal formatting, progress displays |

### Development Tooling

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | >=8.2.0 | Unit and integration testing |
| `pytest-cov` | >=5.0.0 | Coverage reporting |
| `ruff` | >=0.6.0 | Linting and formatting (replaces black/isort/flake8) |
| `mypy` | >=1.11.0 | Static type checking |

---

## Frontend Stack (Planned - `ui/` directory)

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18+ | Web UI for PI interaction |
| TypeScript | 5+ | Type safety across frontend/backend |
| Vite | 5+ | Fast build tool with HMR |
| Tailwind CSS | Latest | Utility-first styling |
| `use-local-llm` | Latest | React hooks for local LLM integration (Ollama-compatible) |

---

## Local LLM Models (via Ollama)

| Model | Parameters | Quantization | Use Case |
|-------|------------|--------------|----------|
| `llama3.1:8b-instruct-q4_K_M` | 8B | Q4_K_M | Primary generation model (Aims, Strategy, Biosketches) |
| `nemotron3:ultra-q4` | 53B | Q4 | Complex sections requiring higher reasoning |

---

## Configuration Files

| File | Format | Purpose |
|------|--------|---------|
| `pyproject.toml` | TOML | Project metadata, dependencies, tool config (ruff, mypy, pytest) |
| `config/grants.yaml` | YAML | Base NIH R01 compliance rules (page limits, format, budget, validation) |
| `config/foa-{id}.yaml` | YAML | FOA-specific overrides (optional, per funding opportunity) |

---

## Project Structure

```
Grant Writing AI/
├── .planning/           # GSD planning artifacts
│   ├── codebase/        # This analysis output
│   ├── research/        # Stack, features, architecture research
│   └── phases/          # Phase plans and context
├── config/              # Runtime configuration
│   ├── grants.yaml      # Base R01 compliance rules
│   └── foa-*.yaml       # FOA-specific overrides
├── src/
│   ├── config/          # Configuration loader & merge logic
│   ├── types/           # Pydantic data models
│   │   ├── common.py    # Enums, base models
│   │   ├── config.py    # GrantsConfig, FOAConfig, MergedFOAConfig
│   │   ├── application_plan.py  # ApplicationPlan, SectionSpec, PageLimits, etc.
│   │   └── merge.py     # Deep merge utilities
│   └── (planned agents/, orchestrator/, rag/, compliance/, formatter/, cli/)
├── tests/               # pytest test suite
└── ui/                  # React frontend (to be created)
```

---

## Build & Tool Configuration

### Ruff (linting/formatting)

- Target: Python 3.11
- Line length: 100
- Select: E, F, I, UP, B, C4, SIM
- Ignore: E501 (line length), B008 (default arg calls)
- Format: double quotes, space indent, no magic trailing comma skip

### MyPy (type checking)

- Python version: 3.11
- Strict mode: enabled
- Warn on: return-any, unused-configs, untyped-defs
- Excludes: tests/

### Pytest

- Test paths: tests/
- Pattern: test_*.py
- Classes: Test*
- Functions: test_*
- Options: -v --strict-markers

### Setuptools

- Package discovery: src/ layout
- Package: grant_writing_ai*

---

## External Tools & Services

| Tool | Purpose |
|------|---------|
| Ollama | Local LLM model serving (must be installed separately) |
| Git | Version control for drafts (agent/drafts, pi/edits, main branches) |
| LibreOffice (headless) | DOCX → PDF conversion for page count validation (planned) |

---

*Generated by codebase analysis on 2026-10-08*
