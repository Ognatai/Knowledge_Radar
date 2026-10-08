import io
import json

import pytest

from app.agents import llm


def test_llm_generate_sends_model_and_disables_thinking(monkeypatch):
    sent = {}

    def fake_urlopen(request, timeout):
        sent.update(json.loads(request.data))
        return io.BytesIO(json.dumps({"response": " answer "}).encode())

    monkeypatch.setattr(llm.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setenv("KNOWLEDGE_RADAR_MODEL", "test-model")

    assert llm.generate("hello", json_output=True) == "answer"
    assert sent["model"] == "test-model" and sent["think"] is False and sent["format"] == "json"


def test_llm_errors_are_wrapped(monkeypatch):
    def failing_urlopen(request, timeout):
        raise OSError("connection refused")

    monkeypatch.setattr(llm.urllib.request, "urlopen", failing_urlopen)

    with pytest.raises(llm.LLMError, match="connection refused"):
        llm.generate("hello")


def test_llm_generate_can_constrain_output_to_a_json_schema(monkeypatch):
    sent = {}

    def fake_urlopen(request, timeout):
        sent.update(json.loads(request.data))
        return io.BytesIO(json.dumps({"response": "{}"}).encode())

    monkeypatch.setattr(llm.urllib.request, "urlopen", fake_urlopen)
    schema = {"type": "object", "properties": {"a": {"type": "string"}}}

    llm.generate("hello", json_schema=schema)

    assert sent["format"] == schema
