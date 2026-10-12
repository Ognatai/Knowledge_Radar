"""The study guide: parts by subject area, a chapter per covered topic, gaps, and the appendix."""

import yaml
from fastapi.testclient import TestClient

from app.backend.knowledge_radar import study_guide
from app.backend.knowledge_radar.api import create_app
from app.backend.knowledge_radar.areas import Area
from app.backend.knowledge_radar.interviews import Interviewer, create_application
from app.backend.knowledge_radar.models import NoteDetail

POSTING_ID = "companies/acme-gmbh/graph-engineer/job_posting"
NOTES = {
    "rdf": NoteDetail.model_construct(
        slug="rdf", title_en="RDF", title_de="RDF", sources=["https://www.w3.org/TR/rdf11-concepts/"], content_en="",
        content_de="> **Hinweis:** LLM-generiert.\n\n### TL;DR\n\nTripel für [[knowledge-graphs|Wissensgraphen]].\n\n### Quellen\n\n- W3C"),
    "python": NoteDetail.model_construct(slug="python", title_en="Python", title_de="Python", sources=[], content_en="### TL;DR\n\nA language.",
                                         content_de=""),
}
AREAS = [Area("software", "Software", "Software", ["python"]), Area("graphs", "Graphs", "Wissensgraphen", ["rdf"])]


def make_root(tmp_path):
    root = tmp_path / "private"
    create_application(root, company_name="ACME GmbH", role_title="Graph Engineer", posting_text="RDF, Neo4j und Python.",
                       interviewers=[Interviewer("Jane Doe", "Teamlead")])
    topics = {"version": 1, "postings": {POSTING_ID: "x"}, "topics": {POSTING_ID: [
        {"name": "RDF", "phrase": "RDF", "note": "rdf", "entity": "rdf"},
        {"name": "Neo4j", "phrase": "Neo4j", "note": None, "entity": "neo4j"},
        {"name": "Python", "phrase": "Python", "note": "python", "entity": "python"},
    ]}}
    (root / "graph").mkdir(exist_ok=True)
    (root / "graph" / "topics.yaml").write_text(yaml.safe_dump(topics), encoding="utf-8")
    (root / "notes").mkdir(exist_ok=True)
    (root / "notes" / "profile.md").write_text("---\ntitle: Profile\n---\n### Summary\nx\n### STAR: Graph migration\nS, T, A, R.\n### Skills\ny\n",
                                               encoding="utf-8")
    return root


def test_parts_follow_the_areas_and_chapters_carry_the_posting_and_the_note(tmp_path):
    text = study_guide.build(make_root(tmp_path), "acme-gmbh", "graph-engineer", 1, NOTES, AREAS)
    assert text.index("## Teil 1: Software") < text.index("### 1 Python") < text.index("## Teil 2: Wissensgraphen") < text.index("### 2 RDF")
    assert "_In der Anzeige: „RDF“_" in text and "Tripel für Wissensgraphen." in text
    assert "#### TL;DR" in text and "Hinweis" not in text and "#### Quellen" not in text
    assert "**Quellen:** <https://www.w3.org/TR/rdf11-concepts/>" in text
    assert "A language." in text  # English when there is no German text
    assert "](#teil-1-software)" in text and "](#2-rdf)" in text


def test_gaps_and_appendix(tmp_path):
    text = study_guide.build(make_root(tmp_path), "acme-gmbh", "graph-engineer", 1, NOTES, AREAS)
    gaps = text[text.index("## Noch nicht abgedeckt"):text.index("## Anhang")]
    assert "**Neo4j**: „Neo4j“ (im Graphen bekannt, noch ohne eigene Notiz)" in gaps
    assert "#### Jane Doe (Teamlead)" in text
    assert "#### Graph migration\n\nS, T, A, R." in text and "\ny\n" not in text.split("STAR-Geschichten")[1].split("###")[1]
    assert "Noch keine gespeicherte Vorbereitung" in text
    assert "- [ ] Kurzvorstellung laut geübt" in text


def test_the_documents_endpoints(tmp_path, monkeypatch):
    root = make_root(tmp_path)
    monkeypatch.setattr("app.backend.knowledge_radar.api.load_areas", lambda slugs, path: AREAS)
    app = create_app(indices=None, private_root=root, refresher=None, proposals=None, inbox=None)
    monkeypatch.setattr(study_guide, "build", lambda *args: "# Lernunterlage")
    client = TestClient(app)
    assert client.get("/api/private/documents/acme-gmbh/graph-engineer/1/study-guide").json() == {"markdown": "# Lernunterlage"}
    assert client.get("/api/private/documents/acme-gmbh/graph-engineer/1/prep").status_code == 404
    assert client.get("/api/private/documents/acme-gmbh/graph-engineer/9/prep").status_code == 404
    assert client.get("/api/private/documents/..%2F..%2Fx/graph-engineer/1/prep").status_code in (400, 404)
