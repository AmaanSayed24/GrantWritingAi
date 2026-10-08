# src/config/__init__.py
"""Config loading utilities."""

from .loader import load_foa_config, load_grants_config

__all__ = ["load_grants_config", "load_foa_config"]