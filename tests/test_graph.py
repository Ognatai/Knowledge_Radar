import pytest

from app.backend.knowledge_radar.graph import GraphError, load_graph, note_sha256
from app.backend.knowledge_radar.notes import load_notes
from tests.test_notes_api import write_note

REGISTRY = """version: 1
entities:
  - id: microsoft
    type: Organization
    name_en: Microsoft
    name_de: Microsoft
    aliases: [Microsoft Research]
  - id: knowledge-graph
    type: Concept
    name_en: Knowledge graph
    name_de: Wissensgraph
"""


def note_hash(path):
    return note_sha256(path)


def setup_repo(tmp_path, registry=REGISTRY):
    notes_dir = tmp_path / "notes"
    alpha = write_note(
        notes_dir,
        name="alpha.md",
        entity_type="Method",
        content_en="Alpha was developed by **Microsoft** and builds on [[beta|Beta]].",
    )
    write_note(notes_dir, name="beta.md", entity_type="Method")
    graph_dir = tmp_path / "graph"
    (graph_dir / "extractions").mkdir(parents=True)
    (graph_dir / "entities.yaml").write_text(registry, encoding="utf-8")
    return notes_dir, graph_dir, alpha


def write_extraction(graph_dir, slug, body):
    path = graph_dir / "extractions" / f"{slug}.yaml"
    path.write_text(body, encoding="utf-8")
    return path


def extraction(note_sha, relations="", discusses="[microsoft, beta]"):
    return f"""version: 1
note_sha256: "{note_sha}"
extracted_by: manual
discusses: {discusses}
relations:{relations or " []"}
"""


ALPHA_RELATIONS = """
  - from: alpha
    type: DEVELOPED_BY
    to: microsoft
    evidence: Alpha was developed by Microsoft
  - from: alpha
    type: BASED_ON
    to: beta
    evidence: builds on Beta
"""


def test_load_graph_combines_note_entities_registry_and_extractions(tmp_path):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    write_extraction(graph_dir, "alpha", extraction(note_hash(alpha), ALPHA_RELATIONS))

    graph = load_graph(graph_dir, load_notes(notes_dir), notes_dir)

    assert graph.entities["alpha"].note == "alpha"
    assert graph.entities["alpha"].type == "Method"
    assert graph.entities["microsoft"].note is None
    assert graph.entities["microsoft"].aliases == ["Microsoft Research"]
    assert graph.discusses == {("alpha", "alpha"), ("alpha", "microsoft"), ("alpha", "beta"), ("beta", "beta")}
    assert {(r.source, r.type, r.target) for r in graph.relations} == {
        ("alpha", "DEVELOPED_BY", "microsoft"),
        ("alpha", "BASED_ON", "beta"),
    }
    assert graph.stale_extractions == []


def test_missing_graph_directory_yields_note_entities_only(tmp_path):
    notes_dir, _, _ = setup_repo(tmp_path)

    graph = load_graph(tmp_path / "missing", load_notes(notes_dir), notes_dir)

    assert set(graph.entities) == {"alpha", "beta"}
    assert graph.relations == []


def test_changed_note_marks_extraction_stale(tmp_path):
    notes_dir, graph_dir, _ = setup_repo(tmp_path)
    write_extraction(graph_dir, "alpha", extraction("0" * 64))

    graph = load_graph(graph_dir, load_notes(notes_dir), notes_dir)

    assert graph.stale_extractions == ["alpha"]


def test_relation_types_follow_schema(tmp_path):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    relations = """
  - from: microsoft
    type: BASED_ON
    to: alpha
    evidence: Alpha was developed by Microsoft
"""
    write_extraction(graph_dir, "alpha", extraction(note_hash(alpha), relations))

    with pytest.raises(GraphError, match="BASED_ON.*Organization"):
        load_graph(graph_dir, load_notes(notes_dir), notes_dir)


@pytest.mark.parametrize("relation_type", ["DISCUSSES", "RELATED_TO", "RETRO_OF", "UNKNOWN"])
def test_only_public_entity_relations_are_allowed(tmp_path, relation_type):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    relations = f"""
  - from: alpha
    type: {relation_type}
    to: beta
    evidence: builds on Beta
"""
    write_extraction(graph_dir, "alpha", extraction(note_hash(alpha), relations))

    with pytest.raises(GraphError, match=relation_type):
        load_graph(graph_dir, load_notes(notes_dir), notes_dir)


def test_evidence_must_be_quoted_from_the_note(tmp_path):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    relations = """
  - from: alpha
    type: DEVELOPED_BY
    to: microsoft
    evidence: Alpha was invented by Microsoft
"""
    write_extraction(graph_dir, "alpha", extraction(note_hash(alpha), relations))

    with pytest.raises(GraphError, match="evidence"):
        load_graph(graph_dir, load_notes(notes_dir), notes_dir)


def test_relation_endpoints_must_be_discussed_by_the_note(tmp_path):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    write_extraction(
        graph_dir, "alpha", extraction(note_hash(alpha), ALPHA_RELATIONS, discusses="[beta]")
    )

    with pytest.raises(GraphError, match="microsoft"):
        load_graph(graph_dir, load_notes(notes_dir), notes_dir)


def test_unknown_entities_are_rejected(tmp_path):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    write_extraction(graph_dir, "alpha", extraction(note_hash(alpha), discusses="[openai]"))

    with pytest.raises(GraphError, match="openai"):
        load_graph(graph_dir, load_notes(notes_dir), notes_dir)


def test_extraction_for_unknown_note_is_rejected(tmp_path):
    notes_dir, graph_dir, _ = setup_repo(tmp_path)
    write_extraction(graph_dir, "gamma", extraction("0" * 64, discusses="[]"))

    with pytest.raises(GraphError, match="gamma"):
        load_graph(graph_dir, load_notes(notes_dir), notes_dir)


def test_registry_ids_must_not_shadow_note_entities(tmp_path):
    registry = REGISTRY + """  - id: alpha
    type: Concept
    name_en: Alpha
    name_de: Alpha
"""
    notes_dir, graph_dir, _ = setup_repo(tmp_path, registry)

    with pytest.raises(GraphError, match="alpha"):
        load_graph(graph_dir, load_notes(notes_dir), notes_dir)


@pytest.mark.parametrize("entity_type", ["Note", "Company", "Unknown"])
def test_registry_types_must_be_public_entity_types(tmp_path, entity_type):
    registry = REGISTRY.replace("type: Organization", f"type: {entity_type}")
    notes_dir, graph_dir, _ = setup_repo(tmp_path, registry)

    with pytest.raises(GraphError, match=entity_type):
        load_graph(graph_dir, load_notes(notes_dir), notes_dir)


def test_registry_ids_are_slugs(tmp_path):
    registry = REGISTRY.replace("id: microsoft", "id: Microsoft Corp")
    notes_dir, graph_dir, _ = setup_repo(tmp_path, registry)

    with pytest.raises(GraphError, match="Microsoft Corp"):
        load_graph(graph_dir, load_notes(notes_dir), notes_dir)


def test_note_hash_ignores_line_endings(tmp_path):
    lf = tmp_path / "lf.md"
    crlf = tmp_path / "crlf.md"
    lf.write_bytes(b"---\ntitle_en: A\n---\n")
    crlf.write_bytes(b"---\r\ntitle_en: A\r\n---\r\n")

    assert note_sha256(lf) == note_sha256(crlf)


def test_symmetric_relations_are_stored_in_one_direction(tmp_path):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    relations = """
  - from: beta
    type: COMPLEMENTS
    to: alpha
    evidence: Alpha was developed by Microsoft and builds on Beta
"""
    write_extraction(graph_dir, "alpha", extraction(note_hash(alpha), relations))

    graph = load_graph(graph_dir, load_notes(notes_dir), notes_dir)

    assert [(r.source, r.type, r.target) for r in graph.relations] == [("alpha", "COMPLEMENTS", "beta")]


def test_evidence_may_differ_in_surrounding_punctuation(tmp_path):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    relations = """
  - from: alpha
    type: DEVELOPED_BY
    to: microsoft
    evidence: "Alpha was developed by Microsoft."
"""
    write_extraction(graph_dir, "alpha", extraction(note_hash(alpha), relations))

    graph = load_graph(graph_dir, load_notes(notes_dir), notes_dir)

    assert len(graph.relations) == 1


def test_note_entities_carry_frontmatter_aliases(tmp_path):
    notes_dir = tmp_path / "notes"
    write_note(notes_dir, name="gamma.md", extra_frontmatter="aliases: [GA, Gamma Act]\n")

    graph = load_graph(None, load_notes(notes_dir))

    assert graph.entities["gamma"].aliases == ["GA", "Gamma Act"]


def test_entity_keys_cover_names_aliases_and_parentheses():
    from app.backend.knowledge_radar.graph import Entity, entity_keys

    entity = Entity(id="w3c", type="Organization", name_en="World Wide Web Consortium (W3C)", name_de="W3C", aliases=["Web Consortium"])

    assert {"w3c", "worldwidewebconsortium", "webconsortium"} <= entity_keys(entity)


def test_an_entity_cannot_relate_to_itself(tmp_path):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    relations = """
  - from: beta
    type: BASED_ON
    to: beta
    evidence: builds on Beta
"""
    write_extraction(graph_dir, "alpha", extraction(note_hash(alpha), relations))

    with pytest.raises(GraphError, match="itself"):
        load_graph(graph_dir, load_notes(notes_dir), notes_dir)


def test_entity_keys_split_parentheses_only_for_acronyms():
    from app.backend.knowledge_radar.graph import Entity, entity_keys

    space = Entity(id="confluence-space", type="Concept", name_en="Space (Confluence)", name_de="Bereich (Confluence)")

    assert "confluence" not in entity_keys(space) and "space" not in entity_keys(space)


def test_only_a_trailing_acronym_in_parentheses_is_a_name():
    from app.backend.knowledge_radar.graph import name_parts

    assert name_parts("Directive (EU) 2019/790 on copyright") == ["Directive (EU) 2019/790 on copyright"]
    assert name_parts("General Data Protection Regulation (GDPR)") == [
        "General Data Protection Regulation (GDPR)",
        "GDPR",
        "General Data Protection Regulation",
    ]
