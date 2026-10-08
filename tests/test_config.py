# tests/test_config.py
"""Unit tests for configuration loader and merge logic."""

import pytest

from src.config.loader import create_foa_template, load_foa_config, load_grants_config
from src.config.merge import deep_merge
from src.types import GrantsConfig, SectionName


class TestConfigLoader:
    """Test configuration loading from files."""

    def test_load_grants_config_default(self):
        config = load_grants_config()
        assert isinstance(config, GrantsConfig)
        assert config.page_limits.specific_aims == 1
        assert config.page_limits.research_strategy == 12
        assert config.format.font_size_pt == 11
        assert config.format.margins_inches == 0.5
        assert "specific_aims" in config.sections["required"]
        assert config.budget_rules.modular_budget_enabled is True
        assert config.budget_rules.modular_budget_increment == 25000
        assert len(config.era_commons_checks) > 0

    def test_load_grants_config_missing_file(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_grants_config(tmp_path / "nonexistent.yaml")

    def test_load_foa_config(self, sample_grants_config):
        foa = load_foa_config("example", sample_grants_config)
        assert foa.foa_config.foa_id == "example"
        assert foa.merged_page_limits.specific_aims == 1
        assert foa.merged_page_limits.research_strategy == 12

    def test_load_foa_config_missing_file(self, sample_grants_config):
        with pytest.raises(FileNotFoundError):
            load_foa_config("nonexistent_foa_12345", sample_grants_config)

    def test_create_foa_template(self, tmp_path):
        target = tmp_path / "foa-test.yaml"
        created = create_foa_template("test", target)
        assert created.exists()
        content = created.read_text()
        assert 'foa_id: "test"' in content


class TestMergeLogic:
    """Test deep merge behavior for configs."""

    def test_deep_merge_page_limits(self):
        base = {"specific_aims": 1, "research_strategy": 12, "biosketch": 5}
        override = {"research_strategy": 6}
        merged = deep_merge(base, override)
        assert merged["specific_aims"] == 1
        assert merged["research_strategy"] == 6
        assert merged["biosketch"] == 5

    def test_foa_config_merge_with_base(self, sample_grants_config, sample_foa_config):
        merged = sample_foa_config.merge_with_base(sample_grants_config)
        assert merged.merged_page_limits.research_strategy == 6
        assert merged.merged_page_limits.specific_aims == 1
        plan = merged.to_application_plan(
            project_title="My R01 Project",
            principal_investigator="Dr. Alice Smith",
            institution="University of Excellence",
            project_start_date="2026-07-01",
            project_end_date="2031-06-30",
        )
        assert plan.project_title == "My R01 Project"
        assert plan.get_page_limit(SectionName.RESEARCH_STRATEGY) == 6
