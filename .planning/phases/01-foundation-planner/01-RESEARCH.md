# Phase 1: Foundation & Planner - Research

**Researched:** 2026-10-07
**Domain:** Project scaffolding, configuration system, FOA PDF parsing, Pydantic data models, Ollama integration
**Confidence:** HIGH

## Summary

Phase 1 establishes the project foundation for the Grant Writing AI pipeline. The core deliverables are: a configuration system merging base R01 rules with FOA-specific overrides, a FOA PDF parser using PyMuPDF + LLM extraction, Pydantic ApplicationPlan data model, Ollama client with model management, and the initial project module structure. All downstream phases depend on the ApplicationPlan structure produced by the Planner agent.

**Primary recommendation:** Use Pydantic v2 for all data models, PyMuPDF for PDF extraction, ollama Python package for LLM integration, and structure the project as a proper Python package with `src/` layout.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Configuration loading | Backend (Python) | — | Loaded at startup, used by all agents |
| FOA PDF parsing | Backend (Python) | — | CPU-intensive, runs on server |
| ApplicationPlan models | Backend (Python) | — | Shared types for all agents |
| Ollama client | Backend (Python) | — | Manages local LLM inference |
| CLI entry point | Backend (Python) | — | Developer-facing tooling |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.11+ | Primary language | Required by LangGraph, modern typing |
| Pydantic | 2.8+ | Data validation, settings | Fast, v2 has better performance, JSON Schema generation |
| PyMuPDF (fitz) | 1.23+ | PDF text extraction | Fastest, most accurate PDF parser for Python |
| ollama | 0.3+ | Ollama Python client | Official client, OpenAI-compatible API |
| LangGraph | 0.2+ | Agent orchestration | State machines with human-in-the-loop |
| typer | 0.12+ | CLI framework | Modern, type-hint based, auto-completion |
| pyyaml | 6.0+ | YAML config loading | Standard for YAML in Python |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Ruff | 0.5+ | Linting/formatting | Replaces black/isort/flake8, extremely fast |
| pytest | 8.2+ | Testing | Standard Python testing |
| pytest-asyncio | 0.23+ | Async testing | For testing async agent code |
| python-dotenv | 1.0+ | Environment config | Load .env files for local development |
| rich | 13.7+ | CLI output | Progress bars, tables, pretty printing |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Pydantic | TypedDict + manual validation | More boilerplate, no automatic validation |
| PyMuPDF | pdfplumber / pdfminer | Slower, less accurate text extraction |
| ollama package | Raw HTTP to Ollama API | More boilerplate, manual retry/streaming |
| typer | Click / argparse | Less modern, no type-hint integration |
| Ruff | Black + isort + flake8 | Slower, multiple tools to configure |

**Installation:**
```bash
pip install pydantic pymupdf ollama langgraph typer pyyaml ruff pytest pytest-asyncio python-dotenv rich
```

**Version verification:**
```bash
python -c "import pydantic; print(pydantic.VERSION)"
python -c "import fitz; print(fitz.__doc__[:50])"
ollama --version
```

## Package Legitimacy Audit

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| pydantic | PyPI | 7 yrs | 50M+/mo | github.com/pydantic/pydantic | OK | Approved |
| pymupdf | PyPI | 15 yrs | 10M+/mo | github.com/pymupdf/PyMuPDF | OK | Approved |
| ollama | PyPI | 2 yrs | 1M+/mo | github.com/ollama/ollama-python | OK | Approved |
| langgraph | PyPI | 1 yr | 500k+/mo | github.com/langchain-ai/langgraph | OK | Approved |
| typer | PyPI | 4 yrs | 5M+/mo | github.com/fastapi/typer | OK | Approved |
| pyyaml | PyPI | 15 yrs | 100M+/mo | github.com/yaml/pyyaml | OK | Approved |
| ruff | PyPI | 2 yrs | 20M+/mo | github.com/astral-sh/ruff | OK | Approved |
| pytest | PyPI | 15 yrs | 200M+/mo | github.com/pytest-dev/pytest | OK | Approved |

**Packages removed due to [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

## Architecture Patterns

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 1 FOUNDATION ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│  │  CLI Entry   │───▶│  Config      │───▶│  FOA Parser  │                 │
│  │  (typer)     │    │  Loader      │    │  (PyMuPDF +  │                 │
│  └──────────────┘    └──────────────┘    │   LLM)       │                 │
│         │                   │            └──────┬───────┘                 │
│         │                   │                   │                         │
│         ▼                   ▼                   ▼                         │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                    ApplicationPlan (Pydantic)                      │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐              │   │
│  │  │Sections  │ │PageLimits│ │Format    │ │Budget    │              │   │
│  │  │Specs     │ │          │ │Rules     │ │Rules     │              │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘              │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Recommended Project Structure

```
src/
├── agents/
│   └── planner/
│       ├── __init__.py
│       ├── agent.py          # Planner agent (LangGraph node)
│       ├── parser.py         # FOA PDF parser
│       └── prompts.py        # LLM prompts for parsing
├── types/
│   ├── __init__.py
│   ├── application_plan.py   # ApplicationPlan, SectionSpec, PageLimits, etc.
│   ├── config.py             # Config models (GrantsConfig, FOAConfig)
│   └── common.py             # Shared types, enums
├── config/
│   ├── __init__.py
│   ├── loader.py             # load_grants_config(), load_foa_config()
│   └── merge.py              # deep_merge_configs()
├── cli/
│   ├── __init__.py
│   └── main.py               # Typer CLI entry point
├── llm/
│   ├── __init__.py
│   ├── ollama_client.py      # OllamaClient with streaming, fallback
│   └── models.py             # Model metadata, availability checking
└── utils/
    ├── __init__.py
    └── pdf.py                # PDF extraction utilities
```

### Pattern 1: Pydantic Configuration with Deep Merge

**What:** Config loaded from YAML, validated by Pydantic, merged with FOA overrides using deep merge.

**When:** Any phase that loads configuration from multiple YAML sources with precedence.

**Example:**
```python
# src/config/loader.py
from pathlib import Path
from typing import Any
import yaml
from pydantic import BaseModel, ConfigDict

from .merge import deep_merge
from ..types.config import GrantsConfig, FOAConfig

def load_grants_config(path: Path = None) -> GrantsConfig:
    """Load base R01 compliance rules from grants.yaml."""
    if path is None:
        path = Path(__file__).parent.parent.parent.parent / "config" / "grants.yaml"
    with open(path) as f:
        data = yaml.safe_load(f)
    return GrantsConfig.model_validate(data)

def load_foa_config(foa_id: str, base: GrantsConfig) -> FOAConfig:
    """Load FOA-specific overrides and merge with base config."""
    foa_path = Path(__file__).parent.parent.parent.parent / "config" / f"foa-{foa_id}.yaml"
    if not foa_path.exists():
        return FOAConfig.model_validate(base.model_dump())
    
    with open(foa_path) as f:
        foa_data = yaml.safe_load(f)
    
    # Deep merge: base + FOA overrides
    merged = deep_merge(base.model_dump(), foa_data)
    return FOAConfig.model_validate(merged)
```

```python
# src/config/merge.py
def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base, with override taking precedence."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result
```

### Pattern 2: FOA PDF Parser with LLM Extraction

**What:** Extract text with PyMuPDF, then use structured LLM prompt to extract FOA requirements.

**When:** Parsing semi-structured PDFs where regex is insufficient.

**Example:**
```python
# src/agents/planner/parser.py
import fitz  # PyMuPDF
from pathlib import Path
from typing import Optional
from ..types.application_plan import ApplicationPlan, FOAMetadata
from ..llm.ollama_client import OllamaClient

class FOAParser:
    def __init__(self, ollama: OllamaClient, model: str = "llama3.1:8b-instruct-q4_K_M"):
        self.ollama = ollama
        self.model = model
    
    def extract_text(self, pdf_path: Path) -> str:
        """Extract all text from FOA PDF."""
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    
    async def parse(self, pdf_path: Path) -> ApplicationPlan:
        """Parse FOA PDF into structured ApplicationPlan."""
        text = self.extract_text(pdf_path)
        
        # First pass: extract metadata (FOA number, title, dates)
        metadata_prompt = f"""Extract FOA metadata from this text. Return JSON only:
        {{
          "foa_number": "string",
          "title": "string", 
          "release_date": "YYYY-MM-DD",
          "due_date": "YYYY-MM-DD",
          "activity_codes": ["R01", "R21"]
        }}
        
        Text (first 5000 chars):
        {text[:5000]}"""
        
        metadata = await self.ollama.generate_json(self.model, metadata_prompt)
        
        # Second pass: extract structured requirements
        parser_prompt = f"""Parse this NIH FOA into structured requirements. Return JSON:
        {{
          "page_limits": {{"section_name": page_count}},
          "required_attachments": ["attachment_name"],
          "format_rules": {{"font": "Arial", "size": 11, "margins": 0.5}},
          "special_instructions": ["instruction"],
          "budget_rules": {{"modular": true, "max_direct": 250000}}
        }}
        
        FOA Text:
        {text[:15000]}"""
        
        parsed = await self.ollama.generate_json(self.model, parser_prompt)
        
        return ApplicationPlan(
            foa_metadata=FOAMetadata(**metadata),
            page_limits=parsed["page_limits"],
            required_attachments=parsed["required_attachments"],
            format_rules=parsed["format_rules"],
            special_instructions=parsed["special_instructions"],
            budget_rules=parsed["budget_rules"]
        )
```

### Pattern 3: Ollama Client with Model Management

**What:** Wrapper around ollama Python package with availability checking, streaming, and fallback.

**When:** Any component needing local LLM inference.

**Example:**
```python
# src/llm/ollama_client.py
import ollama
import subprocess
from typing import AsyncGenerator, Optional
from pydantic import BaseModel
from rich.console import Console

console = Console()

class OllamaClient:
    def __init__(self, host: str = "http://localhost:11434"):
        self.client = ollama.AsyncClient(host=host)
        self._model_cache: dict[str, dict] = {}
    
    async def list_models(self) -> list[dict]:
        """Get available models from Ollama."""
        try:
            response = await self.client.list()
            models = response.get("models", [])
            self._model_cache = {m["name"]: m for m in models}
            return models
        except Exception as e:
            console.print(f"[yellow]Ollama unavailable: {e}[/yellow]")
            return []
    
    async def is_model_available(self, model: str) -> bool:
        """Check if model is available locally."""
        if not self._model_cache:
            await self.list_models()
        return model in self._model_cache
    
    async def pull_model(self, model: str) -> bool:
        """Pull model from Ollama registry."""
        try:
            await self.client.pull(model)
            return True
        except Exception:
            return False
    
    async def generate(
        self, 
        model: str, 
        prompt: str, 
        stream: bool = True,
        options: Optional[dict] = None
    ) -> AsyncGenerator[str, None] | str:
        """Generate text with optional streaming."""
        if stream:
            async for chunk in await self.client.generate(
                model=model, prompt=prompt, stream=True, options=options
            ):
                yield chunk["response"]
        else:
            response = await self.client.generate(
                model=model, prompt=prompt, stream=False, options=options
            )
            return response["response"]
    
    async def generate_json(
        self, 
        model: str, 
        prompt: str,
        schema: Optional[dict] = None
    ) -> dict:
        """Generate structured JSON output."""
        # Use format parameter for JSON mode (supported by Ollama)
        response = await self.client.generate(
            model=model,
            prompt=prompt,
            stream=False,
            format="json" if schema is None else schema,
            options={"temperature": 0.1}
        )
        import json
        return json.loads(response["response"])
    
    def fallback_llama_cpp(self, model_path: str, prompt: str) -> str:
        """Fallback to direct llama.cpp if Ollama unavailable."""
        result = subprocess.run(
            ["llama-cli", "-m", model_path, "-p", prompt, "-n", "2048"],
            capture_output=True, text=True
        )
        return result.stdout
```

### Anti-Patterns to Avoid

| Anti-Pattern | Why Bad | Instead |
|--------------|---------|---------|
| Raw dict for config | No validation, typos silent | Pydantic models with validation |
| Regex-only FOA parsing | FOAs vary in structure, regex breaks | PyMuPDF + LLM for flexible extraction |
| Global config singleton | Hard to test, hidden dependencies | Dependency injection via function params |
| No model availability check | Fails at runtime with cryptic errors | Check `ollama list` at startup |
| Hardcoded paths | Breaks on different machines | Pathlib with relative-to-package resolution |

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| YAML config loading with merge | Custom merge logic | `deep_merge` function + Pydantic | Edge cases in nested merge |
| PDF text extraction | Custom PDF parser | PyMuPDF (fitz) | Handles encoding, layouts, tables |
| LLM JSON output parsing | Custom JSON repair | Ollama `format="json"` + Pydantic | Native structured output |
| CLI argument parsing | Manual sys.argv parsing | Typer | Auto-completion, type hints, help |
| Model availability checking | Try/catch on first call | `ollama list` at startup | Fail fast, clear error messages |

**Key insight:** Configuration and parsing are solved problems. Custom solutions accumulate edge-case bugs that surface weeks later.

## Runtime State Inventory

> Phase 1 is greenfield — no existing runtime state to migrate.

| Category | Items Found | Action Required |
|----------|-------------|-----------------|
| Stored data | None — new project | N/A |
| Live service config | None — Ollama starts fresh | N/A |
| OS-registered state | None | N/A |
| Secrets/env vars | None — local only | N/A |
| Build artifacts | None | N/A |

## Common Pitfalls

### Pitfall 1: Pydantic v1 vs v2 Migration
**What goes wrong:** Using v1 patterns (`Config` class, `@validator`) in v2 codebase.
**Why it happens:** Many tutorials still show v1 syntax.
**How to avoid:** Use v2 patterns: `ConfigDict`, `@field_validator`, `model_validate()`.
**Warning signs:** Import errors on `Config`, deprecation warnings.

### Pitfall 2: FOA PDF Text Extraction Quality
**What goes wrong:** PyMuPDF extracts text in wrong order (columns, headers/footers mixed in).
**Why it happens:** PDFs don't have logical reading order; text is positioned absolutely.
**How to avoid:** Use `page.get_text("dict")` for structured extraction, filter by font/bbox.
**Warning signs:** Extracted text has headers/footers interleaved with body.

### Pitfall 3: Ollama Model Not Available
**What goes wrong:** Code assumes model exists, fails at generation time.
**Why it happens:** Ollama models must be explicitly pulled; not bundled.
**How to avoid:** Check `ollama list` at startup; auto-pull or error with clear instructions.
**Warning signs:** Connection refused, model not found errors at runtime.

### Pitfall 4: Config Merge Loses Nested Keys
**What goes wrong:** Shallow merge overwrites entire nested sections instead of merging.
**Why it happens:** `dict.update()` doesn't recurse.
**How to avoid:** Use recursive deep_merge function; test with nested YAML.
**Warning signs:** FOA-specific settings disappear after merge.

### Pitfall 5: Streaming vs Non-Streaming Confusion
**What goes wrong:** Using streaming for JSON output (chunks aren't valid JSON).
**Why it happens:** Streaming returns partial tokens; only full response is valid JSON.
**How to avoid:** Use `stream=False` + `format="json"` for structured output; streaming only for text.
**Warning signs:** JSON parse errors on partial chunks.

## Code Examples

### ApplicationPlan Pydantic Models
```python
# src/types/application_plan.py
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class ActivityCode(str, Enum):
    R01 = "R01"
    R21 = "R21"
    R03 = "R03"
    K99 = "K99"

class FOAMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    foa_number: str = Field(..., description="FOA number e.g. PA-24-123")
    title: str
    release_date: str  # YYYY-MM-DD
    due_date: str      # YYYY-MM-DD
    activity_codes: list[ActivityCode] = [ActivityCode.R01]

class PageLimits(BaseModel):
    model_config = ConfigDict(extra="forbid")
    specific_aims: int = 1
    research_strategy: int = 12
    biosketch: int = 5
    biosketch_supplement: int = 2
    budget_justification: Optional[int] = None  # no_limit
    # ... other sections

class FormatRules(BaseModel):
    model_config = ConfigDict(extra="forbid")
    font_family: str = "Arial"
    font_size_pt: int = 11
    margins_inches: float = 0.5
    line_spacing: str = "single"
    page_numbering: str = "bottom-right"
    headers: bool = True

class BudgetRules(BaseModel):
    model_config = ConfigDict(extra="forbid")
    modular_budget: bool = True
    increment_usd: int = 25000
    max_direct_costs_usd: int = 250000
    pi_minimum_effort_pct: int = 30
    equipment_threshold_usd: int = 5000

class ApplicationPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)
    
    foa_metadata: FOAMetadata
    page_limits: PageLimits
    format_rules: FormatRules
    budget_rules: BudgetRules
    required_attachments: list[str] = []
    special_instructions: list[str] = []
    section_order: list[str] = [
        "specific_aims",
        "research_strategy",
        "biosketch",
        "budget_justification"
    ]
```

### Config Models
```python
# src/types/config.py
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from .application_plan import PageLimits, FormatRules, BudgetRules

class GrantsConfig(BaseModel):
    """Base R01 compliance rules from grants.yaml"""
    model_config = ConfigDict(extra="forbid")
    page_limits: PageLimits
    format: FormatRules
    sections: dict
    budget_rules: BudgetRules
    fonts: dict
    page_margins: dict
    validation: dict
    era_commons_checks: list[str]

class FOAConfig(GrantsConfig):
    """FOA-specific config (extends base with overrides)"""
    foa_id: str
    foa_specific_overrides: dict = Field(default_factory=dict)
```

### CLI Entry Point
```python
# src/cli/main.py
import typer
from pathlib import Path
from rich.console import Console

from ..config.loader import load_grants_config, load_foa_config
from ..agents.planner.parser import FOAParser
from ..llm.ollama_client import OllamaClient

app = typer.Typer(help="Grant Writing AI - NIH R01 Pipeline")
console = Console()

@app.command()
def parse_foa(
    foa_pdf: Path = typer.Argument(..., help="Path to FOA PDF"),
    output: Path = typer.Option(None, help="Output JSON path"),
    model: str = typer.Option("llama3.1:8b-instruct-q4_K_M", help="Ollama model"),
):
    """Parse FOA PDF into ApplicationPlan JSON."""
    console.print(f"[cyan]Parsing FOA:[/cyan] {foa_pdf}")
    
    ollama = OllamaClient()
    models = await ollama.list_models()
    if not any(m["name"] == model for m in models):
        console.print(f"[yellow]Model {model} not found. Available: {[m['name'] for m in models]}[/yellow]")
        if not typer.confirm("Pull model?"):
            raise typer.Exit(1)
        await ollama.pull_model(model)
    
    parser = FOAParser(ollama, model)
    plan = await parser.parse(foa_pdf)
    
    json_output = plan.model_dump_json(indent=2)
    if output:
        output.write_text(json_output)
        console.print(f"[green]Saved to {output}[/green]")
    else:
        console.print(json_output)

@app.command()
def validate_config(
    foa_id: str = typer.Argument(..., help="FOA ID (e.g. PA-24-123)"),
):
    """Validate config merge for a FOA."""
    base = load_grants_config()
    foa = load_foa_config(foa_id, base)
    console.print(f"[green]Config valid for {foa_id}[/green]")
    console.print(f"Page limits: {foa.page_limits.model_dump()}")

if __name__ == "__main__":
    app()
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual config dicts | Pydantic Settings v2 | 2024 | Type-safe, validated config |
| pdfminer/pdfplumber | PyMuPDF (fitz) | 2023 | 10x faster, better accuracy |
| Raw HTTP to Ollama | ollama Python package | 2024 | Official client, streaming, retries |
| Click/argparse | Typer | 2022 | Type hints → CLI auto-generation |
| Black+isort+flake8 | Ruff | 2023 | 100x faster, single tool |

**Deprecated/outdated:**
- Pydantic v1 patterns (`Config` class, `@validator`) — use v2 `ConfigDict`, `@field_validator`
- `pdfminer.six` for PDF extraction — slower, less accurate than PyMuPDF
- Manual JSON parsing from LLM — use Ollama `format="json"` + Pydantic validation

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | PyMuPDF extracts FOA text in readable order | FOA Parser | Parser fails on complex PDF layouts; need fallback to pdfplumber |
| A2 | Ollama `format="json"` produces valid JSON for our schemas | Ollama Client | Structured output fails; need JSON repair logic |
| A3 | FOA-specific YAML files follow same schema as grants.yaml | Config Merge | Validation errors on load; need flexible schema |
| A4 | Llama-3.1-8B can parse FOA text accurately | FOA Parser | Parsing hallucinates; need few-shot examples or larger model |
| A5 | Deep merge handles all config override cases | Config Merge | Silent config corruption; need comprehensive tests |

## Open Questions

1. **FOA parser prompt engineering:** What few-shot examples work best for NIH FOA parsing? Need to test with real FOA PDFs.
2. **Model selection:** Is Llama-3.1-8B sufficient for FOA parsing, or do we need Nemotron-3-Ultra for accuracy?
3. **Config versioning:** How to version FOA configs when NIH updates rules? Need migration strategy.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python | All | ✓ | 3.11+ | — |
| Ollama | LLM inference | ? | — | llama.cpp direct |
| PyMuPDF | PDF parsing | ✓ | 1.23+ | pdfplumber |
| Pydantic | Data models | ✓ | 2.8+ | — |
| LangGraph | Agent orchestration | ✓ | 0.2+ | — |
| Ruff | Linting | ✓ | 0.5+ | — |

**Missing dependencies with no fallback:** Ollama (if not installed) — document install instructions
**Missing dependencies with fallback:** llama.cpp direct subprocess if Ollama unavailable

## Validation Architecture

> Included because `workflow.nyquist_validation` is not explicitly `false` in config.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 8.2+ with pytest-asyncio |
| Config file | `pytest.ini` / `pyproject.toml` |
| Quick run command | `pytest tests/unit -x -q` |
| Full suite command | `pytest tests/ -v` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| REQ-01 | FOA parser extracts page limits | unit | `pytest tests/test_foa_parser.py::test_page_limits -x` | ❌ Wave 0 |
| REQ-02 | Planner outputs valid ApplicationPlan | unit | `pytest tests/test_planner.py::test_application_plan -x` | ❌ Wave 0 |
| REQ-03 | CLI accepts FOA PDF path | integration | `pytest tests/test_cli.py::test_parse_foa -x` | ❌ Wave 0 |
| REQ-35 | Config loads grants.yaml + foa-*.yaml | unit | `pytest tests/test_config.py::test_merge -x` | ❌ Wave 0 |
| REQ-36 | Ollama client lists models | unit | `pytest tests/test_ollama.py::test_list_models -x` | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** `pytest tests/unit -x -q`
- **Per wave merge:** `pytest tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/test_foa_parser.py` — covers REQ-01
- [ ] `tests/test_planner.py` — covers REQ-02
- [ ] `tests/test_config.py` — covers REQ-35
- [ ] `tests/test_ollama.py` — covers REQ-36
- [ ] `tests/test_cli.py` — covers REQ-03
- [ ] `tests/conftest.py` — shared fixtures (Ollama mock, sample FOA PDF)
- [ ] Framework install: `pip install pytest pytest-asyncio pytest-mock` — if none detected

## Security Domain

> Required since `security_enforcement` not explicitly `false`.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V5 Input Validation | yes | Pydantic validation on all inputs |
| V10 Malicious File Upload | yes | PDF type checking, size limits |

### Known Threat Patterns for Python/PDF/LLM Stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Malicious PDF (parser exploit) | Tampering | PyMuPDF sandboxed, size limits, timeout |
| Prompt injection in FOA text | Spoofing | Input sanitization, delimiter-based prompts |
| Model extraction via API | Information Disclosure | Local-only, no external API |

## Sources

### Primary (HIGH confidence)
- Pydantic v2 docs (Context7) — Configuration, validation patterns
- PyMuPDF docs (Context7) — Text extraction, structured output
- Ollama Python package docs (Context7) — Client usage, JSON mode
- LangGraph docs (Context7) — State machine, node patterns
- Typer docs (Context7) — CLI patterns

### Secondary (MEDIUM confidence)
- NIH FOA format guides (grants.nih.gov) — Page limits, structure
- Ruff docs — Linting rules, config

### Tertiary (LOW confidence)
- WebSearch: "PyMuPDF FOA PDF parsing best practices" — marked for validation

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all packages verified on PyPI, widely used
- Architecture: HIGH — patterns from existing codebases (Friday, friday-assistant, S_Agent)
- Pitfalls: HIGH — based on known issues in GSD PITFALLS.md and local LLM research
- Code examples: MEDIUM — adapted from patterns, not yet tested in this project

**Research date:** 2026-10-07
**Valid until:** 2026-11-07 (30 days for stable stack)