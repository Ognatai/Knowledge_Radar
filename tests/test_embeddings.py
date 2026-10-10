import json

from app.backend.knowledge_radar import embeddings


class Response:
    def __init__(self, count):
        self.count = count

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps({"embeddings": [[1.0]] * self.count}).encode("utf-8")


def capture(monkeypatch):
    bodies = []

    def urlopen(request, timeout):
        body = json.loads(request.data)
        bodies.append(body)
        return Response(len(body["input"]))

    monkeypatch.setattr(embeddings.urllib.request, "urlopen", urlopen)
    return bodies


def test_embeddings_use_the_gpu_by_default(monkeypatch):
    monkeypatch.delenv("KNOWLEDGE_RADAR_EMBEDDING_ON_CPU", raising=False)
    bodies = capture(monkeypatch)

    assert embeddings.embed(["a", "b"]) == [[1.0], [1.0]]
    assert "options" not in bodies[0]


def test_embeddings_can_be_kept_on_the_cpu(monkeypatch):
    monkeypatch.setenv("KNOWLEDGE_RADAR_EMBEDDING_ON_CPU", "1")
    bodies = capture(monkeypatch)

    embeddings.embed(["a"])

    assert bodies[0]["options"] == {"num_gpu": 0}
