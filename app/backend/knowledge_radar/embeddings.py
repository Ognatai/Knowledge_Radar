"""Text embeddings from the local Ollama server, for the local index.

qwen3-embedding:0.6b is multilingual (the notes are German and English), small
enough to run next to the ThinkPad's chat model, and returns 1024 dimensions.
Qwen3 embeddings expect an instruction before a search query, not before the
documents being indexed.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen3-embedding:0.6b"
QUERY_INSTRUCTION = "Given a question, retrieve passages from a knowledge base that answer it"
BATCH_SIZE = 16
# Ollama sporadically rejected an embedding request with HTTP 400 that succeeded
# when sent again (2026-10-11, with the chat model loaded next to it).
RETRIES = 2


class EmbeddingError(RuntimeError):
    """Raised when the embedding model cannot be reached or returns no vectors."""


def model_name() -> str:
    return os.environ.get("KNOWLEDGE_RADAR_EMBEDDING_MODEL", DEFAULT_MODEL)


def on_cpu() -> bool:
    """KNOWLEDGE_RADAR_EMBEDDING_ON_CPU=1 keeps the embedding model off the GPU, so that
    Ollama does not swap it with a large generation model that fills the GPU memory."""
    return os.environ.get("KNOWLEDGE_RADAR_EMBEDDING_ON_CPU", "").lower() in {"1", "true", "yes"}


def query_text(query: str, instruction: str = QUERY_INSTRUCTION) -> str:
    return f"Instruct: {instruction}\nQuery: {query}"


def embed(texts: list[str], *, model: str | None = None, timeout: float = 600) -> list[list[float]]:
    """One normalised vector per text, in order."""
    base_url = os.environ.get("OLLAMA_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    vectors: list[list[float]] = []
    for start in range(0, len(texts), BATCH_SIZE):
        batch = texts[start : start + BATCH_SIZE]
        body: dict = {"model": model or model_name(), "input": batch}
        if on_cpu():
            body["options"] = {"num_gpu": 0}
        request = urllib.request.Request(
            f"{base_url}/api/embed",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        for attempt in range(RETRIES + 1):
            try:
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    result = json.loads(response.read())["embeddings"]
                break
            except urllib.error.HTTPError as exc:
                reason = exc.read().decode("utf-8", "replace")[:300]
                if attempt == RETRIES:
                    raise EmbeddingError(f"Ollama embedding request to {base_url} failed: {exc} {reason}") from exc
                time.sleep(2 * (attempt + 1))
            except (OSError, KeyError, json.JSONDecodeError) as exc:
                raise EmbeddingError(f"Ollama embedding request to {base_url} failed: {exc}") from exc
        if len(result) != len(batch):
            raise EmbeddingError(f"Expected {len(batch)} embeddings, got {len(result)}.")
        vectors.extend(result)
    return vectors
