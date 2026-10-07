# Architecture Patterns

**Domain:** Autonomous Grant Writing Pipeline (NIH R01)
**Researched:** 2026-10-07

## Recommended Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GRANT WRITING AI ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐  │
│  │   REACT UI   │───▶│  ORCHESTRATOR│───▶│  AGENT PIPE  │───▶│  OUTPUT  │  │
│  │  (Vite/TS)   │    │  (LangGraph) │    │  (5 Agents)  │    │  (DOCX)  │  │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────┘  │
│         │                    │                    │               ▲         │
│         │                    │                    │               │         │
│         ▼                    ▼                    ▼               │         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      SHARED INFRASTRUCTURE                            │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────────────┐  │   │
│  │  │  ChromaDB   │ │   Ollama    │ │  Git Repo   │ │  Config/State  │  │   │
│  │  │  (Vector    │ │  (LLM API)  │ │  (Drafts)   │ │  (YAML/JSON)   │  │   │
│  │  │   Store)    │ │             │ │             │ │                │  │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|---------------|-------------------|
| **React UI** | PI interaction: upload PDFs, enter metadata, review/edit drafts at gates, download DOCX | Orchestrator via REST/WebSocket |
| **Orchestrator (LangGraph)** | Manages agent pipeline state, human gates, version control, error recovery | All agents, UI, Git, ChromaDB, Ollama |
| **Planner Agent** | Parses FOA, creates application structure, defines section requirements | Retriever (provides structure), Orchestrator |
| **Retriever Agent** | RAG over PI PDFs + RePORTER; returns relevant chunks per section | Planner (structure), Drafter (context), ChromaDB |
| **Drafter Agent** | Writes each section (Aims, Strategy, Biosketch, Budget) using retrieved context | Retriever (context), Critic (feedback), Orchestrator |
| **Critic Agent** | Validates compliance (page limits, format, budget rules), cross-section consistency | Drafter (drafts), Formatter (final), Orchestrator |
| **Formatter Agent** | Generates NIH-compliant DOCX with styles, tables, headers/footers | Critic (validated drafts), UI (download) |
| **ChromaDB** | Vector store for PI PDF embeddings + RePORTER abstracts | Retriever (query), Ingestion pipeline |
| **Ollama** | Local LLM inference (OpenAI-compatible API) | All agents (generation) |
| **Git Repo** | Version control for all drafts, commits per agent pass | Orchestrator (commits), UI (history) |

### Data Flow

1. **PI uploads PDFs + enters metadata** → UI → Orchestrator
2. **Orchestrator** → Anonymization pipeline → ChromaDB ingestion (embeddings)
3. **Planner** reads FOA/structure → emits `ApplicationPlan` (sections, page limits, requirements)
4. **Retriever** queries ChromaDB per section → returns `RetrievedContext` chunks
5. **Drafter** generates `SectionDraft` for each section using plan + context
6. **Human Gate 1**: PI reviews Specific Aims → approves/edits → Orchestrator continues
6. **Drafter** continues with Research Strategy, Biosketches, Budget
7. **Human Gate 2**: PI reviews full draft → approves/edits
8. **Critic** validates all drafts against compliance rules → emits `ValidationReport`
9. **Formatter** generates final DOCX from validated drafts
10. **Human Gate 3**: PI final review → download
11. **Orchestrator** commits final version to Git

## Patterns to Follow

### Pattern 1: LangGraph State Machine for Agent Pipeline
**What:** Each agent is a node in a LangGraph state machine with explicit state transitions.
**When:** Multi-step workflows with human gates and error recovery.
**Example:**
```python
from langgraph.graph import StateGraph, END

class GrantState(TypedDict):
    foa_text: str
    pi_pdfs: list[Path]
    metadata: dict
    application_plan: ApplicationPlan
    retrieved_context: dict[str, list[Chunk]]
    section_drafts: dict[str, SectionDraft]
    validation_report: ValidationReport
    final_docx: bytes
    current_gate: str

graph = StateGraph(GrantState)
graph.add_node("planner", planner_agent)
graph.add_node("retriever", retriever_agent)
graph.add_node("drafter", drafter_agent)
graph.add_node("critic", critic_agent)
graph.add_node("formatter", formatter_agent)
graph.add_node("human_gate", human_gate_node)

graph.add_edge("planner", "retriever")
graph.add_edge("retriever", "drafter")
graph.add_conditional_edges("drafter", route_after_draft)
graph.add_edge("critic", "formatter")
graph.add_edge("formatter", "human_gate")
graph.add_conditional_edges("human_gate", route_after_gate)
graph.set_entry_point("planner")
```

### Pattern 2: RAG with Section-Aware Retrieval
**What:** Retriever queries ChromaDB with section-specific prompts (e.g., "Find preliminary data for Specific Aim 1").
**When:** Different sections need different types of evidence.
**Example:**
```python
SECTION_QUERIES = {
    "specific_aims": "hypothesis preliminary data significance innovation",
    "significance": "gap in field impact public health",
    "innovation": "novel approach paradigm shift methodology",
    "approach": "methodology experiments preliminary results feasibility",
    "biosketch": "publications honors positions contributions",
    "budget": "personnel equipment supplies travel costs"
}
```

### Pattern 3: Compliance Rules as Data, Not Code
**What:** NIH format rules (page limits, font, margins) defined in YAML/JSON, loaded by Critic.
**When:** Rules change per FOA; avoids code changes for new requirements.
**Example:**
```yaml
# compliance/r01_rules.yaml
page_limits:
  specific_aims: 1
  research_strategy: 12
  biosketch: 5
  budget_justification: no_limit
format:
  font: "Arial"
  font_size: 11
  margins: 0.5
  line_spacing: "single"
  headers: true
  page_numbering: "bottom-right"
```

### Pattern 4: Git Commits Per Agent Pass
**What:** Orchestrator commits to Git after each agent completes, with structured commit messages.
**When:** PIs expect full history; enables rollback and comparison.
**Example:**
```bash
git add .planning/drafts/
git commit -m "feat(drafter): Specific Aims draft v1

REQ-IDs: REQ-01, REQ-03
Agent: drafter
Model: llama3.1:8b-instruct-q4_K_M
Context-chunks: 47
Human-gate: pending"
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Monolithic Single-Pass Generation
**What:** One giant prompt generates entire grant.
**Why bad:** Hallucinations compound; no grounding; impossible to validate per-section; no human checkpoints.
**Instead:** Multi-agent pipeline with RAG grounding per section, human gates.

### Anti-Pattern 2: Hardcoding Compliance Logic in Agents
**What:** Page limit checks, font validation embedded in Critic code.
**Why bad:** NIH updates rules; different FOAs have different limits; unmaintainable.
**Instead:** Externalize rules to config files; Critic loads and applies them.

### Anti-Pattern 3: Skipping Anonymization
**What:** Send PI PDFs directly to LLM without scrubbing.
**Why bad:** Institutional policy violation; data leakage; legal risk.
**Instead:** Mandatory anonymization pipeline before any embedding or LLM call.

### Anti-Pattern 4: No Version Control Between Iterations
**What:** Overwrite drafts in place.
**Why bad:** PIs can't compare versions; no rollback; lost work.
**Instead:** Git commit per agent pass + per human gate.

## Scalability Considerations

| Concern | At 1 PI (Prototype) | At 10 PIs (Pilot) | At 100+ (Production) |
|---------|---------------------|-------------------|----------------------|
| LLM Inference | Ollama local | Ollama + model routing | vLLM cluster / TGI |
| Vector Store | ChromaDB local | ChromaDB + persistence | Qdrant / Pinecone |
| Orchestration | LangGraph in-process | LangGraph + Celery | Temporal / Prefect |
| UI | React + Vite dev | React + Nginx | Next.js + Vercel/K8s |
| Git | Local repo | GitLab/GitHub org | GitLab/GitHub Enterprise |
| Anonymization | Regex + spaCy | Dedicated service | PII detection API |

## Sources

- LangGraph documentation (state machines, human-in-the-loop)
- NIH R01 Application Guide (structure, compliance)
- CASRAI format guides
- Local LLM agent patterns (LangGraph + Ollama)
- python-docx for structured DOCX generation
- ChromaDB persistence patterns