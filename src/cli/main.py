# src/cli/main.py
"""Typer CLI entry point for Grant Writing AI."""

import typer

from src.cli.commands import parse_foa_command, validate_config_command

app = typer.Typer(
    name="grant-writing-ai",
    help="Autonomous grant writing pipeline for NIH R01 applications.",
    add_completion=False,
)

app.command("parse-foa", help="Parse an NIH FOA PDF into an ApplicationPlan.")(parse_foa_command)
app.command("validate-config", help="Validate grants.yaml and optional FOA overrides.")(validate_config_command)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
