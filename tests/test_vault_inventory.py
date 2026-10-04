import pytest

from app.agents.vault_inventory import build_inventory, parse_note

MAPPING = {
    "areas": {"KI": "ai", "Legal": "legal"},
    "notes": {
        "Übersicht": {"hub": True},
        "RAG": {"id": "rag", "title_en": "RAG", "title_de": "RAG", "entity_type": "Method"},
        "DSGVO": {
            "id": "gdpr",
            "title_en": "GDPR",
            "title_de": "DSGVO",
            "entity_type": "Regulation",
            "jurisdiction": "EU",
        },
    },
}


def test_parse_note_tracks_sections_and_ignores_code():
    parsed = parse_note(
        "# Title\n\nIntro [[A]]\n\n## Basics\nSee [[B|label]] and ![[C#part]].\n"
        "```\n[[InCode]]\n```\n## Verwandte Themen\n- [[D]]\n"
    )

    assert parsed.title == "Title"
    assert parsed.sections == ["Basics", "Verwandte Themen"]
    assert parsed.links == [("A", None), ("B", "Basics"), ("C", "Basics"), ("D", "Verwandte Themen")]


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_build_inventory_resolves_ids_and_separates_link_kinds(tmp_path):
    write(tmp_path / "Übersicht.md", "# Hub\n## Methods\n- [[RAG]]\n## Law\n- [[DSGVO]]\n")
    write(
        tmp_path / "KI" / "RAG.md",
        "# RAG\n[[Übersicht|back]]\n## Data\nPersonal data: [[DSGVO]], [[ADR-1]]\n"
        "## Verwandte Themen\n- [[DSGVO]]\n- [[RAG]]\n",
    )
    write(tmp_path / "Legal" / "DSGVO.md", "# DSGVO\n## Verwandte Themen\n- [[RAG]]\n")

    inventory = build_inventory(tmp_path, MAPPING)

    notes = {note["id"]: note for note in inventory["notes"]}
    assert notes["rag"]["links_inline"] == ["gdpr"]
    assert notes["rag"]["links_related_only"] == []
    assert notes["rag"]["template"] == "technical"
    assert notes["gdpr"]["template"] == "regulatory"
    assert notes["gdpr"]["jurisdiction"] == "EU"
    assert notes["gdpr"]["links_related_only"] == ["rag"]
    assert inventory["hubs"][0]["groups"] == {"Methods": ["rag"], "Law": ["gdpr"]}
    assert inventory["summary"]["reciprocal_pairs"] == 1
    assert inventory["summary"]["cross_area_pairs"] == {"ai <-> legal": 1}
    assert inventory["summary"]["unresolved_links"] == [{"note": "RAG", "target": "ADR-1"}]
    assert str(tmp_path) not in str(inventory)


def test_build_inventory_requires_complete_mapping(tmp_path):
    write(tmp_path / "Unknown.md", "# Unknown\n")

    with pytest.raises(ValueError, match="Unmapped notes: \\['Unknown'\\]"):
        build_inventory(tmp_path, MAPPING)
