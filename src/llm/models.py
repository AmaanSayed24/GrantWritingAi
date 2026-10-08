# src/llm/models.py
"""Model information and metadata structures for LLM inference."""

from dataclasses import dataclass
from typing import Any


@dataclass
class ModelInfo:
    """Metadata about an LLM model."""

    name: str
    model_family: str = "llama"
    parameter_size: str = "8B"
    quantization_level: str = "Q4_K_M"
    context_window: int = 128000
    is_recommended: bool = True
    size_bytes: int = 0

    @classmethod
    def from_ollama_dict(cls, data: dict[str, Any]) -> "ModelInfo":
        """Create ModelInfo from an Ollama list response entry."""
        name = data.get("name", "unknown")
        size = data.get("size", 0)
        details = data.get("details", {})
        family = details.get("family", "llama")
        param_size = details.get("parameter_size", "8B")
        quant = details.get("quantization_level", "Q4_K_M")

        is_rec = "llama3.1" in name.lower() or "8b" in name.lower()

        return cls(
            name=name,
            model_family=family,
            parameter_size=param_size,
            quantization_level=quant,
            size_bytes=size,
            is_recommended=is_rec,
        )


RECOMMENDED_MODELS = [
    "llama3.1:8b-instruct-q4_K_M",
    "llama3.1:8b",
    "llama3.1:latest",
    "mistral:latest",
]
