"""Minimal client for the local Ollama server (the pipeline's default LLM)."""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Any

DEFAULT_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen3:14b"


class LLMError(RuntimeError):
    """Raised when the local model cannot be reached or returns no usable answer."""


def base_url() -> str:
    return os.environ.get("OLLAMA_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def model_name() -> str:
    return os.environ.get("KNOWLEDGE_RADAR_MODEL", DEFAULT_MODEL)


def generate(
    prompt: str,
    *,
    temperature: float = 0.2,
    json_output: bool = False,
    context_tokens: int = 24576,
    timeout: float = 1800,
) -> str:
    """Return the model's completion for a single prompt (thinking disabled)."""
    body: dict[str, Any] = {
        "model": model_name(),
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {"temperature": temperature, "num_ctx": context_tokens},
    }
    if json_output:
        body["format"] = "json"
    request = urllib.request.Request(
        f"{base_url()}/api/generate",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            answer = json.loads(response.read())["response"]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        raise LLMError(f"Ollama request to {base_url()} failed: {exc}") from exc
    return answer.strip()
