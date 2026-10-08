# src/llm/__init__.py
"""LLM client and model utilities."""

from .models import RECOMMENDED_MODELS, ModelInfo
from .ollama_client import OllamaClient

__all__ = ["OllamaClient", "ModelInfo", "RECOMMENDED_MODELS"]
