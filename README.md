# Grant Writing AI

> Autonomous grant writing pipeline for NIH R01 applications — reduces 6 weeks of professor time to 4 hours using local, zero-cost multi-agent AI.

## Overview

**Grant Writing AI** is a multi-agent system that generates complete NIH R01 grant applications (Specific Aims, Research Strategy, Biosketches, Budget Justification) with full compliance validation. Runs entirely locally via Ollama/llama.cpp — zero API costs, full privacy.

**Pipeline:** Planner → Retriever → Drafter → Critic → Formatter
**Interface:** React web UI (like Friday)
**Human Gates:** PI reviews/edits at Specific Aims, Full Draft, Final DOCX

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama installed and running
- Git

### Installation

```bash
# Clone and enter
cd "Grant Writing AI"

# Python dependencies
pip install -r requirements.txt

# Frontend
cd ui && npm install && cd ..

# Pull models (run once)
ollama pull llama3.1:8b-instruct-q4_K_M
ollama pull nemotron3:ultra-q4  # optional, for complex sections
```

### Run the Pipeline

```bash
# Start Ollama (if not running)
ollama serve

# Run CLI (Phase 1: Foundation & Planner)
python -m src.cli.main --phase 1 --foa path/to/foa.pdf --pdfs path/to/pdfs/
```

### Run the UI

```bash
cd ui && npm run dev
# Opens http://localhost:5173
```

## Project Structure

```
Grant Writing AI/
├── .planning/           # GSD planning artifacts
│   ├── PROJECT.md       # Living project context
│   ├── config.json      # Workflow preferences
│   ├── REQUIREMENTS.md  # 37 v1 requirements
│   ├── ROADMAP.md       # 7-phase execution plan
│   ├── STATE.md         # Current status
│   └── research/        # Domain research
├── config/              # Runtime configuration
│   ├── grants.yaml      # Base R01 compliance rules
│   └── foa-*.yaml       # FOA-specific overrides
├── src/                 # Python agents
│   ├── agents/          # Planner, Retriever, Drafter, Critic, Formatter
│   ├── orchestrator/    # LangGraph state machine
│   ├── rag/             # ChromaDB, anonymization, ingestion
│   ├── compliance/      # Validation rules engine
│   ├── formatter/       # python-docx DOCX generation
│   └── cli/             # CLI entry points
├── ui/                  # React frontend (Vite + TS + Tailwind)
├── tests/               # pytest tests
├── AGENTS.md            # AI agent guidance
└── README.md
```

## Development Workflow

This project uses **GSD (Git. Ship. Done.)** — spec-driven development for AI agents.

```bash
# Show current phase
/gsd-progress

# Discuss approach for current phase
/gsd-discuss-phase 1

# Create execution plan
/gsd-plan-phase 1

# Execute plan
/gsd-execute-phase 1

# Transition to next phase
/gsd-transition 1
```

See `.planning/ROADMAP.md` for all 7 phases and `.planning/REQUIREMENTS.md` for requirements.

## Current Status

**Phase 1: Foundation & Planner** — Ready to start
- Project initialized with GSD
- Research complete (STACK, FEATURES, ARCHITECTURE, PITFALLS, SUMMARY)
- Requirements defined (REQ-01 to REQ-37)
- Roadmap created (7 phases, fine granularity, MVP mode)
- Config: YOLO mode, parallel execution, git tracking, local LLMs

## Target Users

- **Primary:** University PIs (2-3 co-design partners for prototype)
- **Secondary:** Research administrators, grant consultants
- **Pilot:** 2-3 PIs with anonymized funded R01s

## Stack

| Layer | Technology |
|-------|------------|
| Agents | Python 3.11+, LangGraph, Ollama |
| RAG | ChromaDB, sentence-transformers |
| Documents | python-docx, PyMuPDF, pdfplumber |
| Frontend | React 18, TypeScript, Vite, Tailwind, use-local-llm |
| LLM | Llama-3.1-8B-Instruct-Q4_K_M (primary) |
| Version Control | Git (agent/drafts, pi/edits, main branches) |

## Compliance

Validates against NIH R01 requirements:
- Page limits (Specific Aims: 1, Research Strategy: 12, Biosketch: 5)
- Format (Arial 11pt, 0.5" margins, single spacing)
- Budget rules (modular, effort %, equipment thresholds)
- Cross-section consistency
- FOA-specific overrides via parsed config


## Related Projects

- **Friday** — React/Node AI assistant (UI patterns reused)
- **friday-assistant** — Python agent framework (orchestration patterns)
- **S_Agent** — CampusWatch agent (agent patterns)

---

