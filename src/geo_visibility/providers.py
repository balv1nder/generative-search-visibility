"""Provider-neutral generation interface and an optional local Ollama adapter."""
# part that talks to a model. 
# It defines a common way to send a request and receive a response.
from __future__ import annotations

import hashlib
import json
import os
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class LLMRequest:
    prompt: str
    model: str
    temperature: float = 0.0
    top_p: float | None = None
    seed: int | None = None
    response_format: str | None = None


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    provider: str
    provider_version: str | None = None


class LLMProvider(Protocol):
    def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate one response for a fully specified request."""


@dataclass(frozen=True)
class OllamaConfig:
    base_url: str
    model: str

    @classmethod
    def from_env(cls) -> "OllamaConfig":
        model = os.environ.get("GEO_OLLAMA_MODEL", "").strip()
        if not model:
            raise ValueError(
                "Set GEO_OLLAMA_MODEL to an installed Ollama model tag; no model is hard-coded."
            )
        base_url = os.environ.get("GEO_OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
        return cls(base_url=base_url, model=model)


class OllamaProvider:
    def __init__(self, config: OllamaConfig, timeout_seconds: float = 180.0):
        self.config = config
        self.timeout_seconds = timeout_seconds
        self._model_digest: str | None = None

    def _resolve_model_digest(self) -> str:
        if self._model_digest is not None:
            return self._model_digest
        request = urllib.request.Request(f"{self.config.base_url}/api/tags", method="GET")
        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
            body = json.loads(response.read().decode("utf-8"))
        if not isinstance(body, dict) or not isinstance(body.get("models"), list):
            raise ValueError("Ollama returned an invalid model-list payload")
        for model in body["models"]:
            if (
                isinstance(model, dict)
                and model.get("name") == self.config.model
                and isinstance(model.get("digest"), str)
            ):
                self._model_digest = model["digest"]
                return self._model_digest
        raise ValueError(
            f"Configured Ollama model {self.config.model!r} is not installed; "
            "install it explicitly before running the pilot."
        )

    def cache_identity(self) -> dict[str, str]:
        return {
            "provider": "ollama",
            "base_url": self.config.base_url,
            "model": self.config.model,
            "model_digest": self._resolve_model_digest(),
        }

    def generate(self, request: LLMRequest) -> LLMResponse:
        if request.model != self.config.model:
            raise ValueError("request model must match the configured Ollama model tag")
        model_digest = self._resolve_model_digest()
        options: dict[str, object] = {"temperature": request.temperature}
        if request.top_p is not None:
            options["top_p"] = request.top_p
        if request.seed is not None:
            options["seed"] = request.seed
        payload_value: dict[str, object] = {
            "model": request.model,
            "prompt": request.prompt,
            "stream": False,
            "options": options,
        }
        if request.response_format is not None:
            payload_value["format"] = request.response_format
        payload = json.dumps(payload_value).encode("utf-8")
        http_request = urllib.request.Request(
            f"{self.config.base_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(http_request, timeout=self.timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Ollama request failed ({error.code}): {detail}") from error
        if not isinstance(body, dict) or not isinstance(body.get("response"), str):
            raise ValueError("Ollama returned an invalid response payload")
        returned_model = body.get("model")
        if not isinstance(returned_model, str) or not returned_model:
            raise ValueError("Ollama response did not identify the model used")
        return LLMResponse(
            text=body["response"],
            model=returned_model,
            provider="ollama",
            provider_version=model_digest,
        )


class CachedProvider:
    """Disk cache keyed by provider, model tag, prompt, and sampling parameters."""

    def __init__(self, provider: LLMProvider, cache_dir: str | Path):
        self.provider = provider
        self.cache_dir = Path(cache_dir)

    def generate(self, request: LLMRequest) -> LLMResponse:
        identity = {
            "provider": (
                self.provider.cache_identity()
                if callable(getattr(self.provider, "cache_identity", None))
                else type(self.provider).__name__
            ),
            "request": asdict(request),
        }
        cache_key = hashlib.sha256(
            json.dumps(identity, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.is_file():
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
            if not isinstance(cached, dict):
                raise ValueError(f"Invalid cached response: {cache_file}")
            return LLMResponse(**cached)

        result = self.provider.generate(request)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        temporary_file = cache_file.with_suffix(".tmp")
        temporary_file.write_text(
            json.dumps(asdict(result), ensure_ascii=False), encoding="utf-8"
        )
        temporary_file.replace(cache_file)
        return result
