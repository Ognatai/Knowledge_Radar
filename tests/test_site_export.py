import json

from app.backend.knowledge_radar.site_export import entity_id, export_site_data
from tests.test_notes_api import write_note


def test_export_builds_two_layer_graph(tmp_path):
    notes_dir = tmp_path / "notes"
    write_note(notes_dir, name="alpha.md", entity_type="Method", content_en="See [[beta]].")
    write_note(notes_dir, name="beta.md", entity_type="Regulation")

    output = export_site_data(notes_dir, tmp_path / "out")
    data = json.loads(output.read_text(encoding="utf-8"))

    assert [note["slug"] for note in data["notes"]] == ["alpha", "beta"]
    nodes = {node["id"]: node for node in data["graph"]["nodes"]}
    alpha_entity = entity_id("Method", "Example alpha.md")
    assert nodes["note:alpha"]["kind"] == "note"
    assert nodes[alpha_entity] == {
        "id": alpha_entity,
        "kind": "entity",
        "entity_type": "Method",
        "name_en": "Example alpha.md",
        "name_de": "Beispiel alpha.md",
        "note": "alpha",
    }
    assert {(edge["source"], edge["target"], edge["type"]) for edge in data["graph"]["edges"]} == {
        ("note:alpha", alpha_entity, "DISCUSSES"),
        ("note:beta", entity_id("Regulation", "Example beta.md"), "DISCUSSES"),
        ("note:alpha", "note:beta", "RELATED_TO"),
    }


def test_entity_id_is_ascii_slug():
    assert entity_id("Regulation", "Künstliche Intelligenz & Recht") == (
        "entity:Regulation:kunstliche-intelligenz-recht"
    )
