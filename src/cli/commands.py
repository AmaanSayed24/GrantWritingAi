# src/cli/commands.py
"""Command implementations for the Grant Writing AI CLI."""

import asyncio
import logging
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.agents.planner.agent import PlannerAgent
from src.agents.planner.parser import FOAParser
from src.config.loader import load_foa_config, load_grants_config
from src.llm.ollama_client import OllamaClient

logger = logging.getLogger(__name__)
console = Console()


def parse_foa_command(
    foa_pdf: Path = typer.Argument(
        ...,
        help="Path to the NIH FOA PDF file.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    model: str = typer.Option(
        "llama3.1:8b-instruct-q4_K_M",
        "--model",
        "-m",
        help="Ollama model to use for extraction.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file to write ApplicationPlan JSON to (stdout if not specified).",
    ),
    project_title: str = typer.Option(
        "Research Project Grant",
        "--title",
        "-t",
        help="Proposed project title.",
    ),
    pi: str = typer.Option(
        "Principal Investigator",
        "--pi",
        help="Principal investigator name.",
    ),
    institution: str = typer.Option(
        "Research Institution",
        "--institution",
        "-i",
        help="Applicant institution name.",
    ),
) -> None:
    """Parse an NIH FOA PDF into a structured ApplicationPlan JSON."""
    resolved_pdf = foa_pdf.resolve()
    console.print(f"[bold blue]Parsing FOA PDF:[/bold blue] {resolved_pdf}")

    ollama = OllamaClient()
    parser = FOAParser(ollama=ollama, model=model)
    agent = PlannerAgent(parser=parser)

    try:
        plan = asyncio.run(
            agent.create_plan(
                foa_pdf=resolved_pdf,
                project_title=project_title,
                principal_investigator=pi,
                institution=institution,
            )
        )
    except Exception as e:
        console.print(f"[bold red]Error parsing FOA:[/bold red] {e}")
        raise typer.Exit(code=1) from e

    plan_json = plan.model_dump_json(indent=2)

    if output:
        output_path = output.resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(plan_json, encoding="utf-8")
        console.print(f"[bold green]ApplicationPlan written to:[/bold green] {output_path}")
    else:
        # Print JSON directly
        typer.echo(plan_json)


def validate_config_command(
    foa_id: str | None = typer.Argument(
        None,
        help="Optional FOA identifier (e.g. 'example') to validate FOA-specific overrides against base.",
    ),
) -> None:
    """Validate grants.yaml and optional FOA-specific configuration."""
    console.print("[bold blue]Validating grant configuration...[/bold blue]")

    try:
        base_config = load_grants_config()
        console.print("[green]OK - Base config (config/grants.yaml) loaded and validated.[/green]")
    except Exception as e:
        console.print(f"[bold red]Failed to load grants.yaml:[/bold red] {e}")
        raise typer.Exit(code=1) from e

    if foa_id:
        try:
            merged = load_foa_config(foa_id, base_config)
            console.print(
                f"[green]OK - FOA config (config/foa-{foa_id}.yaml) merged and validated.[/green]"
            )

            # Display merged details
            table = Table(title=f"Configuration for FOA: {foa_id}")
            table.add_column("Section / Rule", style="cyan")
            table.add_column("Configured Limit / Value", style="magenta")

            table.add_row("Specific Aims Limit", str(merged.merged_page_limits.specific_aims))
            table.add_row("Research Strategy Limit", str(merged.merged_page_limits.research_strategy))
            table.add_row("Biosketch Limit", str(merged.merged_page_limits.biosketch))
            table.add_row("Font Family", str(merged.merged_format.font_family.value))
            table.add_row("Font Size (pt)", str(merged.merged_format.font_size_pt))
            table.add_row("Margins (in)", str(merged.merged_format.margins_inches))
            table.add_row("Modular Budget Increment", f"${merged.merged_budget.modular_budget_increment:,}")
            table.add_row("Max Direct Costs", f"${merged.merged_budget.modular_budget_max_direct_costs:,}")

            console.print(table)
        except Exception as e:
            console.print(f"[bold red]Failed to load or merge foa-{foa_id}.yaml:[/bold red] {e}")
            raise typer.Exit(code=1) from e
    else:
        # Base config summary
        table = Table(title="Base NIH R01 Rules (config/grants.yaml)")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="magenta")

        table.add_row("Specific Aims Limit", str(base_config.page_limits.specific_aims))
        table.add_row("Research Strategy Limit", str(base_config.page_limits.research_strategy))
        table.add_row("Biosketch Limit", str(base_config.page_limits.biosketch))
        table.add_row("Font Family", str(base_config.format.font_family.value))
        table.add_row("Font Size (pt)", str(base_config.format.font_size_pt))
        table.add_row("Margins (in)", str(base_config.format.margins_inches))
        table.add_row("eRA Commons Checks", f"{len(base_config.era_commons_checks)} checks configured")

        console.print(table)

    console.print(
        Panel(
            "[bold green]Configuration is fully compliant with Pydantic validation schemas.[/bold green]",
            title="Validation Status",
        )
    )
