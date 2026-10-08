# src/config/loader.py
"""Configuration loader for grants.yaml and FOA-specific configs."""

from pathlib import Path
from typing import Any

import yaml

from src.types import FOAConfig, GrantsConfig, MergedFOAConfig

CONFIG_DIR = Path(__file__).parent.parent.parent / "config"


def load_grants_config(config_path: Path | str | None = None) -> GrantsConfig:
    """
    Load base grants configuration from grants.yaml.
    
    Args:
        config_path: Optional path to grants.yaml. Defaults to config/grants.yaml.
        
    Returns:
        GrantsConfig instance
    """
    if config_path is None:
        config_path = CONFIG_DIR / "grants.yaml"
    
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Grants config not found: {config_path}")
    
    with open(config_path) as f:
        data = yaml.safe_load(f)
    
    # Convert string values to appropriate types
    data = _convert_config_types(data)
    
    return GrantsConfig(**data)


def load_foa_config(foa_id: str, base: GrantsConfig, config_path: Path | str | None = None) -> MergedFOAConfig:
    """
    Load FOA-specific configuration and merge with base config.
    
    Args:
        foa_id: FOA identifier (e.g., "example", "RFA-CA-24-001")
        base: Base GrantsConfig instance
        config_path: Optional path to foa-{id}.yaml. Defaults to config/foa-{id}.yaml.
        
    Returns:
        MergedFOAConfig instance
    """
    if config_path is None:
        config_path = CONFIG_DIR / f"foa-{foa_id}.yaml"
    
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"FOA config not found: {config_path}")
    
    with open(config_path) as f:
        data = yaml.safe_load(f)
    
    # Convert string values to appropriate types
    data = _convert_config_types(data)
    
    foa_config = FOAConfig(**data)
    
    return foa_config.merge_with_base(base)


def _convert_config_types(data: dict[str, Any]) -> dict[str, Any]:
    """Convert string values in config to appropriate Python types."""
    if not isinstance(data, dict):
        return data
    
    result = {}
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = _convert_config_types(value)
        elif isinstance(value, list):
            result[key] = [_convert_config_types(v) if isinstance(v, dict) else v for v in value]
        elif isinstance(value, str):
            # Convert numeric strings
            if value.lower() == "true":
                result[key] = True
            elif value.lower() == "false":
                result[key] = False
            elif value.lower() == "no_limit":
                result[key] = "no_limit"
            else:
                # Try to convert to int or float
                try:
                    if "." in value:
                        result[key] = float(value)
                    else:
                        result[key] = int(value)
                except ValueError:
                    result[key] = value
        else:
            result[key] = value
    
    return result


def create_foa_template(foa_id: str, output_path: Path | str | None = None) -> Path:
    """
    Create a template FOA config file.
    
    Args:
        foa_id: FOA identifier
        output_path: Optional output path. Defaults to config/foa-{id}.yaml.
        
    Returns:
        Path to created file
    """
    if output_path is None:
        output_path = CONFIG_DIR / f"foa-{foa_id}.yaml"
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    template = f"""# FOA-specific configuration for {foa_id}
# This file overrides base grants.yaml settings for this specific FOA.
# Only include sections you want to override.

foa_id: "{foa_id}"
title: "Funding Opportunity Title"
agency: "NIH"
activity_code: "R01"
release_date: "2026-01-01"
application_due_date: "2026-06-01"
expiration_date: "2026-12-31"
description: "Description of the funding opportunity"
special_instructions:
  - "Special instruction 1"
  - "Special instruction 2"

# Override page limits (only include sections that differ from base)
page_limits:
  specific_aims: 1
  research_strategy: 12
  biosketch: 5
  # budget_justification: no_limit

# Override format rules
format:
  font_family: "Arial"
  font_size_pt: 11
  margins_inches: 0.5
  line_spacing: "single"
  page_numbering: "bottom-right"
  headers: true
  header_format: "PI Last Name / Project Title / Page X of Y"
  paper_size: "letter"

# Override sections
sections:
  required:
    - specific_aims
    - research_strategy
    - biosketch
    - budget_justification
  research_strategy_subsections:
    - significance
    - innovation
    - approach
  biosketch_format: "2026_common_form"
  biosketch_supplement_required: true

# Override budget rules
budget_rules:
  modular_budget:
    enabled: true
    increment: 25000
    max_direct_costs: 250000
  personnel:
    pi_minimum_effort_pct: 30
    co_investigator_minimum_effort_pct: 10
    max_total_effort_pct: 100
  equipment:
    threshold_usd: 5000
    requires_justification_above: true
  travel:
    foreign_travel_requires_approval: true
    domestic_conference_max_per_year: 2
  consortium:
    f_and_a_on_first_25k_only: true

# Override fonts
fonts:
  allowed: ["Arial", "Helvetica", "Georgia", "Palatino Linotype"]
  default: "Arial"
  minimum_size_pt: 11

# Override page margins
page_margins:
  top: 0.5
  bottom: 0.5
  left: 0.5
  right: 0.5

# Override validation rules
validation:
  check_page_limits: true
  check_font: true
  check_margins: true
  check_line_spacing: true
  check_page_numbering: true
  check_headers: true
  check_required_sections: true
  check_budget_rules: true
  check_cross_section_consistency: true
  check_biosketch_format: true
  check_biosketch_page_limit: true
"""
    
    with open(output_path, "w") as f:
        f.write(template)
    
    return output_path