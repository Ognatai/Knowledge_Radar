import json

from app.backend.knowledge_radar.site_export import export_site_data
from tests.test_graph import ALPHA_RELATIONS, extraction, note_hash, setup_repo, write_extraction


def test_export_builds_two_layer_graph(tmp_path):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    write_extraction(graph_dir, "alpha", extraction(note_hash(alpha), ALPHA_RELATIONS))

    output = export_site_data(notes_dir, graph_dir, tmp_path / "out")
    data = json.loads(output.read_text(encoding="utf-8"))

    assert [note["slug"] for note in data["notes"]] == ["alpha", "beta"]
    nodes = {node["id"]: node for node in data["graph"]["nodes"]}
    assert nodes["note:alpha"]["kind"] == "note"
    assert nodes["entity:alpha"] == {
        "id": "entity:alpha",
        "kind": "entity",
        "entity_type": "Method",
        "name_en": "Example alpha.md",
        "name_de": "Beispiel alpha.md",
        "note": "alpha",
    }
    assert nodes["entity:microsoft"]["note"] is None
    assert nodes["entity:knowledge-graph"]["kind"] == "entity"
    assert {(edge["source"], edge["target"], edge["type"]) for edge in data["graph"]["edges"]} == {
        ("note:alpha", "entity:alpha", "DISCUSSES"),
        ("note:alpha", "entity:microsoft", "DISCUSSES"),
        ("note:alpha", "entity:beta", "DISCUSSES"),
        ("note:beta", "entity:beta", "DISCUSSES"),
        ("note:alpha", "note:beta", "RELATED_TO"),
        ("entity:alpha", "entity:microsoft", "DEVELOPED_BY"),
        ("entity:alpha", "entity:beta", "BASED_ON"),
    }


def test_relation_supported_by_several_notes_is_exported_once(tmp_path):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    write_extraction(graph_dir, "alpha", extraction(note_hash(alpha), ALPHA_RELATIONS + ALPHA_RELATIONS))

    output = export_site_data(notes_dir, graph_dir, tmp_path / "out")
    edges = json.loads(output.read_text(encoding="utf-8"))["graph"]["edges"]

    assert sum(edge["type"] == "DEVELOPED_BY" for edge in edges) == 1
