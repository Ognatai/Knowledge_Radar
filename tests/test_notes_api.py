import pytest
from fastapi.testclient import TestClient

from app.backend.knowledge_radar.api import create_app
from app.backend.knowledge_radar.notes import load_notes, wikilink_targets


def write_note(
    directory,
    name="example.md",
    sources="https://example.org/source",
    entity_type="Concept",
    extra_frontmatter="",
    content_en="An English description.",
    content_de="Eine deutsche Beschreibung.",
):
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    path.write_text(
        f"""---
title_en: Example {name}
title_de: Beispiel {name}
entity_type: {entity_type}
{extra_frontmatter}sources:
  - {sources}
---

## EN
{content_en}

## DE
{content_de}
""",
        encoding="utf-8",
    )
    return path


def test_load_notes_requires_sources(tmp_path):
    write_note(tmp_path, sources="file:///private/note")

    with pytest.raises(ValueError, match="absolute HTTP\\(S\\) URL"):
        load_notes(tmp_path)


def test_api_lists_searches_and_returns_note_detail(tmp_path):
    write_note(tmp_path)
    client = TestClient(create_app(tmp_path))

    list_response = client.get("/api/notes")
    assert list_response.status_code == 200
    assert list_response.json()[0]["title_en"] == "Example example.md"

    search_response = client.get("/api/notes/search", params={"q": "deutsche"})
    assert search_response.status_code == 200
    assert [item["slug"] for item in search_response.json()["items"]] == ["example"]
    assert search_response.json()["total"] == 1

    detail_response = client.get("/api/notes/example")
    assert detail_response.status_code == 200
    assert detail_response.json()["content_de"] == "Eine deutsche Beschreibung."
    assert detail_response.json()["links"] == []


def test_search_paginates_results(tmp_path):
    write_note(tmp_path, name="alpha.md")
    write_note(tmp_path, name="beta.md")
    client = TestClient(create_app(tmp_path))

    response = client.get("/api/notes/search", params={"q": "description", "limit": 1, "offset": 1})

    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert len(response.json()["items"]) == 1


def test_wikilink_targets_support_labels_and_headings():
    text = (
        "See [[rag]], [[methods/rag|RAG]], [[eu-ai-act#Article 5|Art. 5]] and [[rag.md]].\n"
        "| [[graphrag\\|GraphRAG]] | table cell |"
    )

    assert wikilink_targets(text) == ["rag", "methods/rag", "eu-ai-act", "graphrag"]


def test_wikilinks_become_resolved_note_links(tmp_path):
    write_note(tmp_path, name="alpha.md", content_en="Builds on [[beta|Beta]] and [[nested]].")
    write_note(tmp_path, name="beta.md", content_en="Links back to [[alpha]] and itself: [[beta]].")
    write_note(tmp_path / "topic", name="nested.md")

    notes = {note.slug: note for note in load_notes(tmp_path)}

    assert notes["alpha"].links == ["beta", "topic/nested"]
    assert notes["beta"].links == ["alpha"]


def test_load_notes_rejects_unknown_wikilink(tmp_path):
    write_note(tmp_path, content_en="See [[missing-note]].")

    with pytest.raises(ValueError, match="wikilinks point to unknown public notes: missing-note"):
        load_notes(tmp_path, planned_slugs=frozenset())


def test_wikilinks_to_planned_notes_are_accepted_but_not_linked_yet(tmp_path):
    write_note(tmp_path, content_en="See [[planned-note|a planned note]].")

    (note,) = load_notes(tmp_path, planned_slugs=frozenset({"planned-note"}))

    assert note.links == []


@pytest.mark.parametrize(
    ("extra", "message"),
    [
        ("related_notes: []\n", "use \\[\\[wikilinks\\]\\]"),
        ("topics: []\n", "topics are not part of the note format"),
    ],
)
def test_load_notes_rejects_unsupported_frontmatter(tmp_path, extra, message):
    write_note(tmp_path, extra_frontmatter=extra)

    with pytest.raises(ValueError, match=message):
        load_notes(tmp_path)


@pytest.mark.parametrize("entity_type", ["Company", "InterviewRetro", "Note", "Unknown"])
def test_load_notes_rejects_non_public_entity_types(tmp_path, entity_type):
    write_note(tmp_path, entity_type=entity_type)

    with pytest.raises(ValueError, match="not a public entity type"):
        load_notes(tmp_path)


def test_api_reports_malformed_public_notes(tmp_path):
    tmp_path.mkdir(exist_ok=True)
    (tmp_path / "broken.md").write_text("No frontmatter", encoding="utf-8")
    client = TestClient(create_app(tmp_path))

    response = client.get("/api/notes")

    assert response.status_code == 500
    assert "YAML frontmatter is required" in response.json()["detail"]


def test_api_returns_404_for_unknown_note(tmp_path):
    write_note(tmp_path)
    client = TestClient(create_app(tmp_path))

    response = client.get("/api/notes/missing")

    assert response.status_code == 404
