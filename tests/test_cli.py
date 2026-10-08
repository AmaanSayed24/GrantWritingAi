# tests/test_cli.py
"""Integration tests for Typer CLI commands."""

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from src.cli.main import app
from src.types.application_plan import ApplicationPlan

runner = CliRunner()


@pytest.fixture
def sample_pdf_path() -> Path:
    return Path(__file__).parent / "fixtures" / "sample_foa.pdf"


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "parse-foa" in result.stdout
    assert "validate-config" in result.stdout


def test_cli_validate_config_base():
    result = runner.invoke(app, ["validate-config"])
    assert result.exit_code == 0
    assert "Base config (config/grants.yaml) loaded and validated" in result.stdout
    assert "Base NIH R01 Rules" in result.stdout


def test_cli_validate_config_foa():
    result = runner.invoke(app, ["validate-config", "example"])
    assert result.exit_code == 0
    assert "FOA config (config/foa-example.yaml) merged and validated" in result.stdout
    assert "Configuration for FOA: example" in result.stdout


def test_cli_validate_config_invalid():
    result = runner.invoke(app, ["validate-config", "definitely_nonexistent_foa_xyz"])
    assert result.exit_code == 1
    assert "Failed to load or merge" in result.stdout


def test_cli_parse_foa_missing_file(tmp_path):
    missing_file = tmp_path / "not_found.pdf"
    result = runner.invoke(app, ["parse-foa", str(missing_file)])
    assert result.exit_code != 0


def test_cli_parse_foa_stdout(sample_pdf_path):
    result = runner.invoke(app, ["parse-foa", str(sample_pdf_path)])
    assert result.exit_code == 0

    # Locate JSON in output
    stdout = result.stdout
    start_idx = stdout.find("{")
    assert start_idx != -1
    json_str = stdout[start_idx:]
    data = json.loads(json_str)

    # Validate against ApplicationPlan schema
    plan = ApplicationPlan(**data)
    assert plan.foa_id == "PA-20-185"
    assert plan.page_limits.research_strategy == 12


def test_cli_parse_foa_to_output_file(sample_pdf_path, tmp_path):
    output_file = tmp_path / "plan_out.json"
    result = runner.invoke(app, ["parse-foa", str(sample_pdf_path), "--output", str(output_file)])
    assert result.exit_code == 0
    assert output_file.exists()

    content = output_file.read_text(encoding="utf-8")
    data = json.loads(content)
    plan = ApplicationPlan(**data)
    assert plan.foa_id == "PA-20-185"
