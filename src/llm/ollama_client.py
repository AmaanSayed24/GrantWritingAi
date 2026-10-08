# src/llm/ollama_client.py
"""Ollama client with availability checking, model management, and structured generation."""

import json
import logging
from collections.abc import AsyncGenerator
from typing import Any

import ollama

from .models import ModelInfo

logger = logging.getLogger(__name__)


class OllamaClient:
    """Async client for interacting with local Ollama service."""

    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host
        self.client = ollama.AsyncClient(host=host)
        self._model_cache: dict[str, dict[str, Any]] = {}

    async def list_models(self) -> list[dict[str, Any]]:
        """Get available models from Ollama."""
        try:
            response = await self.client.list()
            models_list: list[dict[str, Any]] = []
            raw_models = getattr(response, "models", None)
            if raw_models is None and isinstance(response, dict):
                raw_models = response.get("models", [])

            if raw_models:
                for m in raw_models:
                    if hasattr(m, "model_dump"):
                        m_dict = m.model_dump()
                    elif isinstance(m, dict):
                        m_dict = m
                    else:
                        m_name = getattr(m, "model", getattr(m, "name", str(m)))
                        m_dict = {"name": m_name}
                    models_list.append(m_dict)

            self._model_cache = {m.get("name", ""): m for m in models_list}
            return models_list
        except Exception as e:
            logger.warning(f"Ollama unavailable at {self.host}: {e}")
            return []

    async def list_model_infos(self) -> list[ModelInfo]:
        """Get available models converted to ModelInfo objects."""
        models = await self.list_models()
        return [ModelInfo.from_ollama_dict(m) for m in models]

    async def is_model_available(self, model: str) -> bool:
        """Check if model is available locally."""
        if not self._model_cache:
            await self.list_models()
        for cached_name in self._model_cache:
            if (
                cached_name == model
                or cached_name.startswith(f"{model}:")
                or model.startswith(f"{cached_name}:")
            ):
                return True
        return False

    async def pull_model(self, model: str) -> bool:
        """Pull model from Ollama registry."""
        try:
            await self.client.pull(model)
            await self.list_models()
            return True
        except Exception as e:
            logger.error(f"Failed to pull model {model}: {e}")
            return False

    async def generate(
        self,
        model: str,
        prompt: str,
        stream: bool = False,
        options: dict[str, Any] | None = None,
    ) -> AsyncGenerator[str, None] | str:
        """Generate text with optional streaming."""
        if stream:
            async def _stream() -> AsyncGenerator[str, None]:
                response_stream = await self.client.generate(
                    model=model,
                    prompt=prompt,
                    stream=True,
                    options=options,
                )
                async for chunk in response_stream:
                    if isinstance(chunk, dict):
                        yield chunk.get("response", "")
                    else:
                        yield getattr(chunk, "response", "")

            return _stream()

        response = await self.client.generate(
            model=model,
            prompt=prompt,
            stream=False,
            options=options,
        )
        if isinstance(response, dict):
            return response.get("response", "")
        return getattr(response, "response", "")

    async def generate_json(
        self,
        model: str,
        prompt: str,
        schema: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Generate structured JSON output."""
        gen_options: dict[str, Any] = {"temperature": 0.1}
        if options:
            gen_options.update(options)

        response = await self.client.generate(
            model=model,
            prompt=prompt,
            stream=False,
            format="json" if schema is None else schema,
            options=gen_options,
        )
        text = (
            response.get("response", "")
            if isinstance(response, dict)
            else getattr(response, "response", "")
        )
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        return json.loads(text)
