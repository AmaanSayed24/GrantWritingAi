---
last_mapped_commit: 608c6728678e22a32e463bee82bf321f2f44f9e8
last_mapped_at: 2026-10-08
---
# Codebase Structure

**Analysis Date:** 2026-10-08

## Directory Layout

```
Grant Writing AI/
├── .planning/                    # GSD planning artifacts
│   ├── codebase/                 # Codebase analysis documents (this folder)
│   ├── phases/                   # Phase-specific plans and artifacts
│   ├── PROJECT.md               # Living project context
│   ├── config.json              # Workflow preferences
│   ├── REQUIREMENTS.md          # 37 v1 requirements
│   ├── ROADMAP.md               # 7-phase execution plan
│   ├── STATE.md                 # Current status
│   └── research/                # Domain research (STACK, FEATURES, ARCHITECTURE, PITFALLS, SUMMARY)
├── config/                       # Runtime configuration (YAML)
│   ├── grants.yaml              # Base R01 compliance rules
│   └── foa-*.yaml               # FOA-specific overrides (generated as needed)
├── src/                          # Python source code
│   ├── agents/                  # Specialized LLM agents
│   │   ├── planner/             # Application planner agent
│   │   ├── retriever/           # RAG retriever agent
│   │   ├── drafter/             # Section drafter agent
│   │   ├── critic/              # Compliance critic agent
│   │   └── formatter/           # DOCX formatter agent
│   ├── cli/                     # Command-line interface
│   │   └── main.py              # Typer CLI entry point
│   ├── compliance/              # Validation rules engine
│   │   ├── validators/          # Individual validators (page_limits, format, budget, etc.)
│   │   └── engine.py            # Orchestration of all validators
│   ├── config/                  # Configuration loading & merging
│   │   ├── loader.py            # YAML load + type conversion
│   │   ├── merge.py             # Deep merge utility
│   │   └── __init__.py          # Exports
│   ├── formatter/               # DOCX generation
│   │   ├── document.py          # python-docx document builder
│   │   ├── styles.py            # NIH style definitions
│   │   └── sections/            # Per-section formatters
│   ├── orchestrator/            # LangGraph workflow orchestration
│   │   ├── graph.py             # State graph definition
│   │   ├── state.py             # TypedState for LangGraph
│   │   ├── nodes/               # Graph nodes (one per agent + human gates)
│   │   └── checkpoints/         # Checkpointing for human-in-the-loop
│   ├── rag/                     # Retrieval-Augmented Generation
│   │   ├── client.py            # ChromaDB client singleton
│   │   ├── ingestion.py         # PDF anonymization, chunking, embedding
│   │   ├── retrieval.py         # Query building, vector search
│   │   └── anonymization.py     # PI/PHI redaction
│   └── types/                   # Core domain models (Pydantic)
│       ├── application_plan.py  # ApplicationPlan, SectionSpec, FOAMetadata, etc.
│       ├── common.py            # Enums, BaseModelExtraForbid
│       ├── config.py            # GrantsConfig, FOAConfig, MergedFOAConfig
│       ├── merge.py             # deep_merge, merge_lists_unique
│       └── __init__.py          # Barrel exports
├── tests/                        # pytest test suite
│   ├── conftest.py              # Shared fixtures
│   ├── test_types.py            # Unit tests for domain models
│   └── __init__.py
├── ui/                           # React frontend (Vite + TypeScript + Tailwind)
│   ├── src/                     # React source
│   │   ├── components/          # Reusable UI components
│   │   ├── pages/               # Page-level components (Dashboard, Review, Settings)
│   │   ├── hooks/               # Custom React hooks
│   │   ├── services/            # API client, WebSocket for real-time updates
│   │   ├── store/               # State management (Zustand/Redux)
│   │   └── types/               # TypeScript types mirroring Python models
│   ├── public/                  # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── AGENTS.md                    # AI agent guidance for this project
├── pyproject.toml               # Python project config (dependencies, tooling)
├── README.md                    # Project overview
└── .gitignore
```

## Directory Purposes

**.planning/:**
- Purpose: GSD methodology artifacts — plans, requirements, roadmap, state tracking
- Contains: Markdown documents, JSON config, phase directories
- Key files: `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, `.planning/config.json`

**config/:**
- Purpose: Runtime YAML configuration for NIH compliance rules
- Contains: `grants.yaml` (base), `foa-*.yaml` (overrides)
- Key files: `config/grants.yaml`, `config/foa-example.yaml` (template)

**src/agents/:**
- Purpose: Specialized LLM agents for each pipeline stage
- Contains: One subdirectory per agent with prompts, tools, logic
- Key files: (to be created per phase) `src/agents/planner/agent.py`, etc.

**src/cli/:**
- Purpose: Command-line interface for running pipeline phases
- Contains: Typer app with commands for each phase
- Key files: `src/cli/main.py`

**src/compliance/:**
- Purpose: Validation engine for NIH compliance checks
- Contains: Individual validators + orchestration engine
- Key files: `src/compliance/engine.py`, `src/compliance/validators/page_limits.py`, etc.

**src/config/:**
- Purpose: Configuration loading, type conversion, merging
- Contains: Loader, merge utility, exports
- Key files: `src/config/loader.py`, `src/config/merge.py`, `src/config/__init__.py`

**src/formatter/:**
- Purpose: DOCX generation with NIH formatting
- Contains: Document builder, style definitions, per-section formatters
- Key files: `src/formatter/document.py`, `src/formatter/styles.py`

**src/orchestrator/:**
- Purpose: LangGraph workflow orchestration, state management, human gates
- Contains: Graph definition, typed state, nodes, checkpointing
- Key files: `src/orchestrator/graph.py`, `src/orchestrator/state.py`

**src/rag/:**
- Purpose: RAG pipeline for PI publication retrieval
- Contains: ChromaDB client, ingestion, retrieval, anonymization
- Key files: `src/rag/client.py`, `src/rag/ingestion.py`, `src/rag/retrieval.py`, `src/rag/anonymization.py`

**src/types/:**
- Purpose: Core domain models — single source of truth for all data structures
- Contains: Pydantic models for config, plan, sections, rules, enums
- Key files: `src/types/application_plan.py`, `src/types/common.py`, `src/types/config.py`, `src/types/merge.py`, `src/types/__init__.py`

**tests/:**
- Purpose: Unit and integration tests
- Contains: Fixtures, test modules mirroring src structure
- Key files: `tests/conftest.py`, `tests/test_types.py`

**ui/:**
- Purpose: Web UI for human-in-the-loop review gates
- Contains: React + TypeScript + Vite + Tailwind application
- Key files: `ui/src/App.tsx`, `ui/src/main.tsx`, `ui/package.json`

## Key File Locations

**Entry Points:**
- `src/cli/main.py`: CLI main entry (Typer)
- `src/orchestrator/graph.py`: LangGraph graph builder
- `ui/src/main.tsx`: React app bootstrap
- `ui/vite.config.ts`: Vite dev server config

**Configuration:**
- `config/grants.yaml`: Base NIH R01 compliance rules
- `src/config/loader.py`: Config loading + type conversion
- `src/config/merge.py`: Deep merge utility
- `pyproject.toml`: Python dependencies, tooling (ruff, mypy, pytest)
- `ui/package.json`: Frontend dependencies, scripts

**Core Logic:**
- `src/types/application_plan.py`: ApplicationPlan, PageLimits, FormatRules, BudgetRules, SectionSpec, FOAMetadata
- `src/types/common.py`: Enums (SectionName, ActivityCode, BiosketchFormat, FontFamily, etc.), BaseModelExtraForbid
- `src/types/config.py`: GrantsConfig, FOAConfig, MergedFOAConfig with merge logic
- `src/types/merge.py`: deep_merge(), merge_lists_unique()
- `src/config/loader.py`: load_grants_config(), load_foa_config(), create_foa_template()

**Testing:**
- `tests/conftest.py`: Comprehensive fixtures for all domain models
- `tests/test_types.py`: Unit tests for all Pydantic models, validation, serialization

## Naming Conventions

**Files:**
- Python modules: `snake_case.py` (e.g., `loader.py`, `application_plan.py`)
- Test files: `test_*.py` (e.g., `test_types.py`)
- Config files: `kebab-case.yaml` (e.g., `grants.yaml`, `foa-example.yaml`)
- React components: `PascalCase.tsx` (e.g., `SectionReview.tsx`)
- React hooks: `useCamelCase.ts` (e.g., `usePlanStore.ts`)

**Directories:**
- Python packages: `snake_case/` (e.g., `agents/`, `orchestrator/`)
- React folders: `kebab-case/` or `PascalCase/` for components (e.g., `components/`, `pages/`)

**Code:**
- Classes: `PascalCase` (e.g., `ApplicationPlan`, `GrantsConfig`)
- Functions: `snake_case` (e.g., `load_grants_config`, `deep_merge`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `CONFIG_DIR`)
- Enums: `PascalCase` with `StrEnum` (e.g., `SectionName.SPECIFIC_AIMS`)
- Pydantic fields: `snake_case` (e.g., `page_limits`, `foa_metadata`)

## Where to Add New Code

**New Agent:**
- Implementation: `src/agents/{agent_name}/agent.py`
- Prompts: `src/agents/{agent_name}/prompts.py` or `.md` files
- Tools: `src/agents/{agent_name}/tools.py`
- Tests: `tests/test_{agent_name}.py`

**New Validator (Compliance):**
- Implementation: `src/compliance/validators/{rule_name}.py`
- Registration: `src/compliance/engine.py` (add to validator list)
- Tests: `tests/compliance/test_{rule_name}.py`

**New Domain Model:**
- Definition: `src/types/{domain}.py` (or existing file)
- Export: `src/types/__init__.py` (add to `__all__`)
- Tests: `tests/test_types.py` (add test class)

**New Config Section:**
- Base: Add to `config/grants.yaml`
- Model: Add field to `GrantsConfig` in `src/types/config.py`
- Merge: Ensure `FOAConfig` has override dict + `MergedFOAConfig` merges it
- Template: Update `create_foa_template()` in `src/config/loader.py`

**New API Endpoint (UI):**
- Backend: Add node in `src/orchestrator/nodes/` or extend graph
- Frontend: `ui/src/services/api.ts` + `ui/src/pages/{PageName}.tsx`

**Utility/Helper:**
- Shared: `src/types/merge.py` (for merge utilities) or new `src/utils/` if needed
- RAG: `src/rag/` submodules

## Special Directories

**.planning/codebase/:**
- Purpose: Generated codebase analysis documents
- Generated: Yes (by `/gsd-map-codebase`)
- Committed: Yes

**.planning/phases/:**
- Purpose: Phase-specific plans, execution artifacts, reviews
- Generated: Yes (by GSD workflow)
- Committed: Yes

**.ruff_cache/:**
- Purpose: Ruff linter cache
- Generated: Yes
- Committed: No (in .gitignore)

**config/foa-*.yaml:**
- Purpose: FOA-specific config overrides (created per FOA)
- Generated: Partially (template via `create_foa_template()`, then edited)
- Committed: Yes (project-specific FOAs)

**ui/node_modules/:**
- Purpose: Frontend dependencies
- Generated: Yes (`npm install`)
- Committed: No (in .gitignore)

**ui/dist/:**
- Purpose: Production build output
- Generated: Yes (`npm run build`)
- Committed: No

---

*Structure analysis: 2026-10-08*
