"""Text embeddings from the local Ollama server, for the local index.

qwen3-embedding:0.6b is multilingual (the notes are German and English), small
enough to run next to the ThinkPad's chat model, and returns 1024 dimensions.
Qwen3 embeddings expect an instruction before a search query, not before the
documents being indexed.
"""

from __future__ import annotations

import json
import os
import urllib.request

DEFAULT_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen3-embedding:0.6b"
QUERY_INSTRUCTION = "Given a question, retrieve passages from a knowledge base that answer it"
BATCH_SIZE = 16


class EmbeddingError(RuntimeError):
    """Raised when the embedding model cannot be reached or returns no vectors."""


def model_name() -> str:
    return os.environ.get("KNOWLEDGE_RADAR_EMBEDDING_MODEL", DEFAULT_MODEL)


def query_text(query: str) -> str:
    return f"Instruct: {QUERY_INSTRUCTION}\nQuery: {query}"


def embed(texts: list[str], *, model: str | None = None, timeout: float = 600) -> list[list[float]]:
    """One normalised vector per text, in order."""
    base_url = os.environ.get("OLLAMA_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    vectors: list[list[float]] = []
    for start in range(0, len(texts), BATCH_SIZE):
        batch = texts[start : start + BATCH_SIZE]
        request = urllib.request.Request(
            f"{base_url}/api/embed",
            data=json.dumps({"model": model or model_name(), "input": batch}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                result = json.loads(response.read())["embeddings"]
        except (OSError, KeyError, json.JSONDecodeError) as exc:
            raise EmbeddingError(f"Ollama embedding request to {base_url} failed: {exc}") from exc
        if len(result) != len(batch):
            raise EmbeddingError(f"Expected {len(batch)} embeddings, got {len(result)}.")
        vectors.extend(result)
    return vectors
