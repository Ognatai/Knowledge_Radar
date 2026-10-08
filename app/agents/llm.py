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


def translation_model_name() -> str:
    """Model for EN->DE translation; Qwen3 14B translates reliably without reasoning mode."""
    return os.environ.get("KNOWLEDGE_RADAR_TRANSLATION_MODEL", DEFAULT_MODEL)


def generate(
    prompt: str,
    *,
    temperature: float = 0.2,
    json_output: bool = False,
    json_schema: dict[str, Any] | None = None,
    context_tokens: int = 24576,
    max_tokens: int | None = None,
    sampling: dict[str, float] | None = None,
    think: bool = False,
    model: str | None = None,
    timeout: float = 3600,
) -> str:
    """Return the model's completion for a single prompt.

    `json_schema` constrains the answer to that JSON schema (Ollama structured
    outputs); `json_output` only requires valid JSON. `max_tokens` caps the output including reasoning (protects against loops);
    `sampling` adds options such as top_p or presence_penalty. With `think`,
    the model reasons first; Ollama returns that reasoning separately, so the
    answer contains only the final text (models such as qwen3:30b-a3b otherwise
    write their planning into the answer).
    """
    options: dict[str, Any] = {"temperature": temperature, "num_ctx": context_tokens}
    if max_tokens:
        options["num_predict"] = max_tokens
    options.update(sampling or {})
    body: dict[str, Any] = {
        "model": model or model_name(),
        "prompt": prompt,
        "stream": False,
        "think": think,
        "options": options,
    }
    if json_schema is not None:
        body["format"] = json_schema
    elif json_output:
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
