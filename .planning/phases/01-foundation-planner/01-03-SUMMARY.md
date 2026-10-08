# Plan 01-03 Summary: Typer CLI Entry Point

- **Phase:** 01-foundation-planner
- **Plan:** 03
- **Status:** Complete
- **Date:** 2026-10-08

## Deliverables Created / Verified

1. **Typer CLI (`src/cli/`):**
   - `src/cli/main.py`: Typer app registering `parse-foa` and `validate-config`; `main()` console entry point.
   - `src/cli/commands.py`: Command implementations with Rich console output.
     - `parse-foa`: validates FOA PDF path (exists/readable); options `--model`, `--output`, `--title`, `--pi`, `--institution`; wires `OllamaClient` -> `FOAParser` -> `PlannerAgent`; writes `ApplicationPlan` JSON to file or stdout.
     - `validate-config`: optional `[foa_id]` argument; loads `config/grants.yaml`, merges `config/foa-{id}.yaml`, renders merged page-limit/format/budget tables; exit codes 0 on success, 1 on failure.
   - `src/cli/__init__.py`: package exports.

2. **Integration Tests (`tests/test_cli.py`):**
   - 7 tests: help text, base config validation, FOA merge validation, invalid FOA error path, missing PDF error path, parse-foa to stdout (schema-validated), parse-foa to file (schema-validated).
   - `tests/fixtures/sample_foa.pdf` fixture; `.gitignore` exception `!tests/fixtures/*.pdf` added so the fixture is committed despite the global `*.pdf` rule.

3. **Verification Results:**
   - `python -m pytest tests/ -q` -> **64 passed** (all plans combined)
   - `ruff check src tests` -> all checks passed
   - `python -m src.cli.main --help` -> exit 0; lists `parse-foa` and `validate-config`
   - `python -m src.cli.main validate-config example` -> exit 0; merged table (Specific Aims 1, Research Strategy 12, Arial 11pt, 0.5in margins, $25,000 increment, $250,000 max direct)
   - `python -m src.cli.main validate-config` -> exit 0; base R01 rules table
   - `python -m src.cli.main validate-config <invalid>` -> exit 1 with clear error
   - `python -m src.cli.main parse-foa tests/fixtures/sample_foa.pdf --output <file>` -> exit 0; saved JSON validates against `ApplicationPlan` schema (foa_id `PA-20-185`, research_strategy limit 12)

4. **Defect found and fixed during verification:**
   - `UnicodeEncodeError` (U+2714 not encodable in cp1252) crashed `validate-config` on Windows consoles. Replaced it with ASCII `OK -` (U+2714 checkmark) in `src/cli/commands.py`; exit code verified 0 after fix.

## Traceability
- **REQ-03 (CLI half):** `parse-foa` accepts FOA PDF path plus project metadata (`--title`, `--pi`, `--institution`; dates use defaults); UI upload lands in Phase 6.
- **REQ-35:** CLI validates `config/grants.yaml` and merges `config/foa-*.yaml` overrides end-to-end.
- **REQ-36:** Ollama model configurable via `--model`; graceful fallback when Ollama is unreachable still produces a valid plan.
