# Technology Stack

**Project:** Grant Writing AI
**Researched:** 2026-10-07

## Recommended Stack

### Core Framework

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Python | 3.11+ | Agent orchestration, RAG pipeline, DOCX generation | Primary language for AI agents; mature ecosystem for llama.cpp, LangChain, python-docx |
| React | 18+ | Web UI for PIs | Reuses Friday codebase; component-driven for grant editing workflow |
| Vite | 5+ | Frontend build tool | Fast HMR, simple config, works with React |
| TypeScript | 5+ | Type safety across frontend/backend | Catches integration errors between UI and Python agents |

### Local LLM Inference

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Ollama | Latest | Model serving, API compatibility | OpenAI-compatible API; model management; streaming; works with use-local-llm React hooks |
| llama.cpp | Latest | High-performance CPU/GPU inference | Direct integration option; quantization support; lower overhead than Ollama for batch |
| Models: Llama-3.1-8B-Instruct-Q4_K_M, Nemotron-3-Ultra-Q4 | 8B-53B params | Primary generation models | Balance of quality/speed for structured writing; fits consumer GPU (8-16GB VRAM) |

### RAG & Vector Store

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| ChromaDB | 0.5+ | Vector database | Local, persistent, Python-native, no separate server needed |
| sentence-transformers | 2.2+ | Embeddings (all-MiniLM-L6-v2) | Fast, small, good for scientific text; runs on CPU |
| LangChain / LangGraph | Latest | Agent orchestration, RAG chains | Structured multi-agent workflows; state management; tool calling |

### Document Processing

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| python-docx | 1.1+ | DOCX generation | Native NIH-compliant output; styles, tables, headers/footers |
| PyMuPDF (fitz) | 1.23+ | PDF parsing | Fast, accurate text extraction from PI-provided PDFs |
| pdfplumber | 0.10+ | Table extraction from PDFs | Biosketch tables, budget tables |

### Infrastructure

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Git | Latest | Version control for drafts | PI expectation; iteration history; branching for alternatives |
| pytest | 7+ | Testing | Unit + integration tests for agents |
| Ruff | Latest | Linting/formatting | Fast, replaces black/isort/flake8 |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Pydantic | 2+ | Data validation, settings | Agent inputs/outputs, config |
| Rich / Textual | Latest | CLI/TUI if needed | Progress display, debugging |
| httpx | 0.27+ | HTTP client | NIH RePORTER API, Ollama API |
| python-dotenv | 1.0+ | Environment config | Model paths, API keys (if any) |

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| LLM Serving | Ollama | LM Studio | Less scriptable; no OpenAI-compatible API by default |
| LLM Serving | Ollama | vLLM | Overkill for local single-user; higher memory |
| Vector Store | ChromaDB | FAISS | FAISS requires more manual persistence management |
| Vector Store | ChromaDB | Qdrant | Qdrant needs separate Docker/process |
| Agent Framework | LangGraph | CrewAI | CrewAI less flexible for custom state machines |
| Agent Framework | LangGraph | AutoGen | AutoGen more complex; LangGraph better for DAG workflows |
| Frontend | React + Vite | Next.js | No SSR needed; simpler deployment |
| Frontend | React + Vite | Streamlit | Less control over grant editing UX |
| PDF Parsing | PyMuPDF | pdfminer | PyMuPDF faster and more accurate |

## Installation

```bash
# Core Python
pip install ollama langchain langgraph chromadb sentence-transformers python-docx pymupdf pdfplumber pydantic httpx python-dotenv pytest ruff

# Frontend
cd ui && npm create vite@latest . -- --template react-ts && npm install use-local-llm

# Models (via Ollama)
ollama pull llama3.1:8b-instruct-q4_K_M
ollama pull nemotron3:ultra-q4  # if available
```

## Sources

- NIH R01 Application Guide (grants.nih.gov)
- CASRAI NIH format guides
- Local LLM stack guides (promptquorum.com, localaimaster.com)
- use-local-llm GitHub (pooyagolchian/use-local-llm)
- LangGraph documentation
- python-docx documentation
- ChromaDB documentation