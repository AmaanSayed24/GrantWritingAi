---
last_mapped_commit: 608c6728678e22a32e463bee82bf321f2f44f9e8
last_mapped_at: 2026-10-08
---
<!-- refreshed: 2026-10-08 -->

# Architecture

**Analysis Date:** 2026-10-08

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                      CLI / Web UI                            │
├──────────────────┬──────────────────┬───────────────────────┤
│  src/cli/main.py │  ui/ (React)     │  Orchestrator         │
│  `src/cli/`      │  `ui/src/`       │  `src/orchestrator/`  │
└────────┬─────────┴────────┬─────────┴──────────┬────────────┘
         │                  │                     │
         ▼                  ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Agents Layer                              │
│  `src/agents/` (Planner, Retriever, Drafter, Critic,        │
│   Formatter)                                                 │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              Core Domain & Infrastructure                    │
├──────────────────┬──────────────────┬───────────────────────┤
│  src/types/      │  src/config/     │  src/compliance/      │
│  Domain models   │  Config loading  │  Validation engine    │
│  `src/types/`    │  `src/config/`   │  `src/compliance/`    │
├──────────────────┼──────────────────┼───────────────────────┤
│  src/rag/        │  src/formatter/  │  src/rag/             │
│  RAG pipeline    │  DOCX generation │  ChromaDB, ingestion  │
│  `src/rag/`      │  `src/formatter/`│  `src/rag/`           │
└──────────────────┴──────────────────┴───────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              External / Persistence                          │
├──────────────────┬──────────────────┬───────────────────────┤
│  Ollama (LLM)    │  ChromaDB        │  Filesystem           │
│  `ollama serve`  │  Vector store    │  PDFs, YAML configs   │
│                  │                  │  `config/`            │
└──────────────────┴──────────────────┴───────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| **CLI Entry Point** | Main command-line interface, phase execution | `src/cli/main.py` |
| **Web UI** | React frontend for human-in-the-loop review | `ui/src/` |
| **Orchestrator** | LangGraph state machine coordinating agents | `src/orchestrator/` |
| **Planner Agent** | Creates application plan from FOA + PI inputs | `src/agents/planner/` |
| **Retriever Agent** | RAG over PI's prior publications, NIH guidelines | `src/agents/retriever/` |
| **Drafter Agent** | Generates section drafts from plan + retrieved context | `src/agents/drafter/` |
| **Critic Agent** | Validates compliance, checks consistency | `src/agents/critic/` |
| **Formatter Agent** | Produces final DOCX with NIH formatting | `src/agents/formatter/` |
| **Domain Types** | Pydantic models for config, plan, sections, rules | `src/types/` |
| **Config Loader** | Loads/merges grants.yaml + FOA-specific YAML | `src/config/loader.py` |
| **Compliance Engine** | Validates page limits, format, budget, cross-section | `src/compliance/` |
| **RAG Pipeline** | Document ingestion, anonymization, vector search | `src/rag/` |
| **DOCX Formatter** | python-docx generation with NIH formatting | `src/formatter/` |

## Pattern Overview

**Overall:** Multi-agent pipeline with LangGraph orchestration, Pydantic-first domain modeling, YAML-based configuration with hierarchical override.

**Key Characteristics:**
- **Pipeline Architecture:** Linear 5-stage pipeline (Planner → Retriever → Drafter → Critic → Formatter) with human gates at 3 points
- **Configuration-Driven:** Base `grants.yaml` + FOA-specific `foa-{id}.yaml` with deep merge semantics
- **Type-Safe Domain Models:** Pydantic v2 models with `extra="forbid"` and `validate_assignment=True` throughout
- **Local-First LLM:** Ollama integration for zero-cost, private inference
- **RAG-Enhanced Drafting:** ChromaDB vector store with anonymization for PI publication retrieval

## Layers

**Presentation Layer:**
- Purpose: User interaction (CLI + Web UI)
- Location: `src/cli/`, `ui/src/`
- Contains: Typer CLI commands, React components, state management
- Depends on: Orchestrator, Agents
- Used by: End users (PIs, research admins)

**Orchestration Layer:**
- Purpose: Coordinate multi-agent workflow, manage state, human gates
- Location: `src/orchestrator/`
- Contains: LangGraph state graph, checkpointing, human-in-the-loop nodes
- Depends on: Agents, Domain Types
- Used by: CLI, Web UI

**Agent Layer:**
- Purpose: Specialized LLM agents for each pipeline stage
- Location: `src/agents/`
- Contains: Planner, Retriever, Drafter, Critic, Formatter agents with prompts + tools
- Depends on: Domain Types, Config, RAG, Compliance
- Used by: Orchestrator

**Domain Layer:**
- Purpose: Core data models, validation rules, business logic
- Location: `src/types/`, `src/config/`, `src/compliance/`
- Contains: Pydantic models (ApplicationPlan, PageLimits, FormatRules, etc.), config loader/merger, validation engine
- Depends on: Pydantic, PyYAML
- Used by: All layers

**Infrastructure Layer:**
- Purpose: External service integration, persistence, document processing
- Location: `src/rag/`, `src/formatter/`
- Contains: ChromaDB client, PDF ingestion (PyMuPDF), DOCX generation (python-docx), Ollama client
- Depends on: External services (Ollama, ChromaDB)
- Used by: Agents, Domain Layer

## Data Flow

### Primary Pipeline Flow (CLI/Orchestrator → Agents)

1. **Input** — CLI receives FOA PDF path + PI PDFs directory (`src/cli/main.py`)
2. **Parse FOA** — Extract FOA metadata, requirements from PDF (`src/rag/ingestion.py`)
3. **Load Config** — Load base `grants.yaml` + FOA override `foa-{id}.yaml`, deep merge (`src/config/loader.py`)
4. **Planner** — Create `ApplicationPlan` with sections, page limits, rules from merged config (`src/agents/planner/`)
5. **Retriever** — Anonymize PI PDFs, ingest to ChromaDB, retrieve relevant context per section (`src/agents/retriever/`, `src/rag/`)
6. **Drafter** — Generate section drafts using plan + retrieved context + LLM (`src/agents/drafter/`)
7. **Human Gate 1** — PI reviews Specific Aims (web UI)
8. **Drafter (cont.)** — Generate remaining sections (Research Strategy, Biosketch, Budget)
9. **Human Gate 2** — PI reviews full draft (web UI)
10. **Critic** — Validate compliance: page limits, format, budget rules, cross-section consistency (`src/agents/critic/`, `src/compliance/`)
11. **Human Gate 3** — PI reviews final DOCX (web UI)
12. **Formatter** — Produce final DOCX with NIH formatting (`src/agents/formatter/`, `src/formatter/`)

### Configuration Merge Flow

1. **Load Base** — `load_grants_config()` reads `config/grants.yaml` → `GrantsConfig` (`src/config/loader.py:14`)
2. **Load FOA** — `load_foa_config()` reads `config/foa-{id}.yaml` → `FOAConfig` (`src/config/loader.py:41`)
3. **Deep Merge** — `FOAConfig.merge_with_base()` recursively merges each section (`src/types/config.py:92`)
4. **Produce Merged** — Returns `MergedFOAConfig` with all resolved values (`src/types/config.py:165`)
5. **To ApplicationPlan** — `to_application_plan()` converts to runtime `ApplicationPlan` (`src/types/config.py:179`)

### RAG Retrieval Flow

1. **Ingest** — `ingest_pdfs()` anonymizes PI PDFs, chunks, embeds, stores in ChromaDB (`src/rag/ingestion.py`)
2. **Query** — For each section, build query from plan + section guidance, retrieve top-K chunks (`src/rag/retrieval.py`)
3. **Inject** — Retrieved context passed to Drafter agent prompt for grounded generation

## Key Abstractions

**ApplicationPlan:**
- Purpose: Complete runtime representation of an NIH application with all sections, rules, metadata
- Examples: `src/types/application_plan.py:131`
- Pattern: Pydantic model with post-init default section initialization

**GrantsConfig / FOAConfig / MergedFOAConfig:**
- Purpose: Hierarchical configuration with base + override merge semantics
- Examples: `src/types/config.py:10`, `src/types/config.py:70`, `src/types/config.py:165`
- Pattern: Pydantic models with `deep_merge()` utility for recursive dict merging

**SectionSpec:**
- Purpose: Specification for one application section (required, page limit, subsections, guidance)
- Examples: `src/types/application_plan.py:102`
- Pattern: Value object with validation, used as dict value in `ApplicationPlan.sections`

**PageLimits / FormatRules / BudgetRules:**
- Purpose: Strongly-typed rule containers with validation constraints
- Examples: `src/types/application_plan.py:17`, `src/types/application_plan.py:42`, `src/types/application_plan.py:73`
- Pattern: Pydantic models with Field constraints (ge, le), used directly in validation

## Entry Points

**CLI Main:**
- Location: `src/cli/main.py`
- Triggers: `python -m src.cli.main --phase 1 --foa path/to/foa.pdf --pdfs path/to/pdfs/`
- Responsibilities: Parse args, initialize orchestrator, execute pipeline phase, handle errors

**Orchestrator Graph:**
- Location: `src/orchestrator/graph.py` (expected)
- Triggers: Invoked by CLI with phase config
- Responsibilities: Build LangGraph, manage checkpoints, route to human gates

**Web UI Dev Server:**
- Location: `ui/package.json` → `npm run dev`
- Triggers: `cd ui && npm run dev`
- Responsibilities: Vite dev server, React app, API proxy to orchestrator

## Architectural Constraints

- **Threading:** Single-threaded async Python (LangGraph runs in event loop); Ollama/ChromaDB are external processes
- **Global State:** Minimal — config loaded per-run, ChromaDB client singleton in `src/rag/client.py`
- **Circular Imports:** Avoided via `src/types/__init__.py` barrel exports; config imports types, types don't import config
- **Immutability:** Pydantic `validate_assignment=True` enforces validation on mutation; configs are merged into new objects
- **External Dependencies:** Ollama must be running locally; ChromaDB runs embedded or as separate server

## Anti-Patterns

### Direct Config Access in Agents

**What happens:** Agents reading `config/grants.yaml` directly instead of receiving `ApplicationPlan`
**Why it's wrong:** Bypasses FOA override merge, violates separation of concerns, makes testing harder
**Do this instead:** Pass `ApplicationPlan` (already merged) to agents via orchestrator state

### Hardcoded Page Limits

**What happens:** Magic numbers like `12` for research strategy in agent prompts
**Why it's wrong:** FOA-specific overrides won't apply; single source of truth is `ApplicationPlan.page_limits`
**Do this instead:** Read `plan.page_limits.research_strategy` or `plan.get_page_limit(SectionName.RESEARCH_STRATEGY)`

### Bypassing Validation

**What happens:** Formatters generating DOCX without running compliance checks
**Why it's wrong:** Produces non-compliant output that fails eRA Commons
**Do this instead:** Always run Critic agent → Compliance engine before Formatter

## Error Handling

**Strategy:** Fail-fast with structured exceptions; validation errors use Pydantic `ValidationError`; runtime errors wrapped in custom exceptions

**Patterns:**
- Config loading: `FileNotFoundError` with descriptive path for missing YAML
- Type conversion: `_convert_config_types()` handles string→int/float/bool gracefully (`src/config/loader.py:72`)
- Merge: `deep_merge()` handles missing keys, nested dicts, type mismatches (`src/types/merge.py:5`)
- LLM calls: Retry with exponential backoff via Ollama client (expected in `src/rag/` or agents)
- Human gates: Timeout/expiration handled by orchestrator checkpointing

## Cross-Cutting Concerns

**Logging:** Python `logging` module; structured JSON logs for orchestrator, debug for agents (expected)

**Validation:** Two-layer — Pydantic model validation at boundaries + Compliance engine runtime checks (`src/compliance/`)

**Authentication:** None for local Ollama/ChromaDB; Web UI may add auth later (not implemented)

---

*Architecture analysis: 2026-10-08*
