"""The private index is built from the private repository and kept apart from the public one."""

import re
from pathlib import Path

import pytest
import yaml

from app.backend.knowledge_radar.graph import Entity
from app.backend.knowledge_radar.private_index import private_graph, private_notes, private_uri
from app.backend.knowledge_radar.private_repo import document_slug, load_documents
from tests.test_private_repo import repo  # noqa: F401  (fixture)

PUBLIC = {
    "retrieval-augmented-generation": Entity("retrieval-augmented-generation", "Method", "Retrieval-Augmented Generation", "RAG"),
    "bm25": Entity("bm25", "Method", "BM25", "BM25"),
}


def write_yaml(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data), encoding="utf-8")


def test_the_private_graph_combines_the_private_files_and_referenced_public_entities(repo):
    documents = load_documents(repo)
    note = next(d for d in documents if d.kind == "round_note")
    graph = repo / "graph"
    write_yaml(graph / "entities.yaml", {"entities": [{"id": "acme-labs", "type": "Organisation", "name_en": "ACME Labs"}]})
    write_yaml(graph / "structure.yaml", {"entities": [{"id": "company-acme-gmbh", "type": "Company", "name_en": "ACME GmbH"}], "relations": []})
    write_yaml(
        graph / "requirements.yaml",
        {
            "entities": [{"id": "req-1", "type": "Requirement", "name_en": "RAG"}],
            "relations": [
                {"from": "req-1", "type": "MATCHES", "to": "retrieval-augmented-generation", "source": "x"},
                {"from": "req-1", "type": "MATCHES", "to": "gone", "source": "x"},
            ],
        },
    )
    write_yaml(graph / "extractions" / f"{document_slug(note)}.yaml", {"discusses": ["acme-labs"], "relations": []})
    write_yaml(graph / "extractions" / "private-deleted-document.yaml", {"discusses": ["bm25"], "relations": []})

    result = private_graph(repo, documents, PUBLIC)

    assert set(result.entities) == {"acme-labs", "company-acme-gmbh", "req-1", "retrieval-augmented-generation"}
    assert [(r.source, r.type, r.target) for r in result.relations] == [("req-1", "MATCHES", "retrieval-augmented-generation")]
    assert result.discusses == {(document_slug(note), "acme-labs")}  # extractions of deleted documents are ignored


def test_documents_with_text_become_notes_with_their_files(repo):
    notes, paths = private_notes(load_documents(repo))

    assert all(paths[note.slug].is_file() for note in notes)
    assert "private-notes-star-stories" in paths


def test_the_private_index_never_uses_the_public_address(monkeypatch):
    monkeypatch.setenv("NEO4J_PRIVATE_URI", "bolt://127.0.0.1:7687")
    monkeypatch.delenv("NEO4J_URI", raising=False)

    with pytest.raises(RuntimeError, match="public index"):
        private_uri()


def test_the_monitoring_pipeline_cannot_reach_private_data():
    """Nothing the monitoring pipeline runs may import the private index or read private documents."""
    monitoring = Path(__file__).parents[1] / "app" / "agents" / "monitoring"
    forbidden = re.compile(r"private_index|connect_private|private_extract|load_documents")
    offenders = [path.name for path in monitoring.glob("*.py") if forbidden.search(path.read_text(encoding="utf-8"))]
    assert offenders == []
