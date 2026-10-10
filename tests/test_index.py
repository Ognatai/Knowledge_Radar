import pytest

from app.backend.knowledge_radar.graph import load_graph
from app.backend.knowledge_radar.index import (
    CHUNKER_VERSION,
    IndexState,
    chunk_note,
    neo4j_password,
    plan_update,
    update_index,
)
from app.backend.knowledge_radar.notes import load_notes
from tests.test_graph import extraction, note_hash, setup_repo, write_extraction
from tests.test_notes_api import write_note

LONG_SECTION = "\n\n".join(f"Paragraph {number} " + "word " * 80 for number in range(12))


def note_with(tmp_path, content_en, content_de="Kurzer Text."):
    notes_dir = tmp_path / "notes"
    write_note(notes_dir, name="alpha.md", content_en=content_en, content_de=content_de)
    return load_notes(notes_dir)[0]


def test_chunks_follow_headings_per_language(tmp_path):
    note = note_with(tmp_path, "### TL;DR\nShort summary.\n\n### How it works\nDetails here.")

    chunks = chunk_note(note)

    assert [(chunk.language, chunk.heading) for chunk in chunks] == [
        ("en", "TL;DR"),
        ("en", "How it works"),
        ("de", ""),
    ]
    assert chunks[0].text == "Short summary."
    assert len({chunk.id for chunk in chunks}) == len(chunks)


def test_embedding_text_carries_title_and_heading(tmp_path):
    note = note_with(tmp_path, "### How it works\nDetails here.")

    chunk = chunk_note(note)[0]

    assert chunk.embedding_text.startswith(f"{note.title_en} > How it works\n\n")
    assert chunk.embedding_text.endswith("Details here.")


def test_long_sections_are_split_at_paragraphs(tmp_path):
    note = note_with(tmp_path, f"### How it works\n{LONG_SECTION}")

    chunks = [chunk for chunk in chunk_note(note, max_characters=1500) if chunk.language == "en"]

    assert len(chunks) > 1
    assert all(len(chunk.text) <= 1500 for chunk in chunks)
    assert all(chunk.heading == "How it works" for chunk in chunks)
    assert chunks[0].text.startswith("Paragraph 0 ")


def test_source_lists_are_not_indexed(tmp_path):
    note = note_with(
        tmp_path,
        "### TL;DR\nSummary.\n\n### Sources\n- Author (2024). A paper.",
        "### TL;DR\nZusammenfassung.\n\n### Quellen\n- Autorin (2024). Ein Paper.",
    )

    headings = [chunk.heading for chunk in chunk_note(note)]

    assert headings == ["TL;DR", "TL;DR"]


def test_plan_embeds_new_and_changed_notes_and_deletes_removed_ones():
    state = IndexState(model="m", chunker_version=CHUNKER_VERSION, note_hashes={"same": "1", "changed": "2", "gone": "3"})

    plan = plan_update({"same": "1", "changed": "2b", "new": "4"}, state, model="m")

    assert plan.embed == ["changed", "new"]
    assert plan.delete == ["gone"]
    assert not plan.full_rebuild


@pytest.mark.parametrize(
    "state",
    [
        None,
        IndexState(model="other-model", chunker_version=CHUNKER_VERSION, note_hashes={"a": "1"}),
        IndexState(model="m", chunker_version=CHUNKER_VERSION - 1, note_hashes={"a": "1"}),
    ],
)
def test_plan_rebuilds_without_state_or_after_model_or_chunker_change(state):
    plan = plan_update({"a": "1"}, state, model="m")

    assert plan.full_rebuild
    assert plan.embed == ["a"]


def test_plan_rebuilds_when_asked():
    state = IndexState(model="m", chunker_version=CHUNKER_VERSION, note_hashes={"a": "1"})

    assert plan_update({"a": "1"}, state, model="m", rebuild=True).embed == ["a"]


class FakeStore:
    def __init__(self, state=None):
        self.state = state
        self.chunks: dict[str, list] = {}
        self.graph = None
        self.cleared = False

    def ensure_schema(self, dimensions):
        self.dimensions = dimensions

    def read_state(self):
        return self.state

    def clear(self):
        self.cleared = True
        self.chunks = {}

    def sync_graph(self, notes, graph):
        self.graph = (sorted(note.slug for note in notes), len(graph.relations))

    def replace_chunks(self, slug, content_hash, chunks, vectors):
        assert len(chunks) == len(vectors)
        self.chunks[slug] = chunks

    def delete_chunks(self, slugs):
        for slug in slugs:
            self.chunks.pop(slug, None)

    def write_state(self, state):
        self.state = state


def fake_embed(texts):
    return [[1.0, 0.0] for _ in texts]


def test_update_index_syncs_graph_and_embeds_only_changed_notes(tmp_path):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    write_extraction(graph_dir, "alpha", extraction(note_hash(alpha)))
    notes = load_notes(notes_dir)
    graph = load_graph(graph_dir, notes, notes_dir)
    store = FakeStore()

    first = update_index(store, notes, graph, notes_dir, embed=fake_embed, model="m")
    store.chunks = {}
    second = update_index(store, notes, graph, notes_dir, embed=fake_embed, model="m")

    assert first.embedded == ["alpha", "beta"] and store.cleared
    assert second.embedded == [] and store.chunks == {}
    assert store.graph == (["alpha", "beta"], 0)
    assert store.dimensions == 2
    assert set(store.state.note_hashes) == {"alpha", "beta"}


def test_update_index_removes_deleted_notes(tmp_path):
    notes_dir, graph_dir, _ = setup_repo(tmp_path)
    write_note(notes_dir, name="gamma.md")
    notes = load_notes(notes_dir)
    graph = load_graph(graph_dir, notes, notes_dir)
    store = FakeStore()
    update_index(store, notes, graph, notes_dir, embed=fake_embed, model="m")

    (notes_dir / "gamma.md").unlink()
    notes = load_notes(notes_dir)
    result = update_index(store, notes, load_graph(graph_dir, notes, notes_dir), notes_dir, embed=fake_embed, model="m")

    assert result.deleted == ["gamma"]
    assert set(store.chunks) == {"alpha", "beta"}
    assert set(store.state.note_hashes) == {"alpha", "beta"}


def test_password_comes_from_environment_before_keyring(monkeypatch):
    monkeypatch.setenv("NEO4J_PASSWORD", "from-env")

    assert neo4j_password(keyring_lookup=lambda service, user: "from-keyring") == "from-env"


def test_password_falls_back_to_keyring(monkeypatch):
    monkeypatch.delenv("NEO4J_PASSWORD", raising=False)

    assert neo4j_password(keyring_lookup=lambda service, user: "from-keyring") == "from-keyring"


def test_missing_password_explains_how_to_set_it(monkeypatch):
    monkeypatch.delenv("NEO4J_PASSWORD", raising=False)

    with pytest.raises(RuntimeError, match="keyring set knowledge-radar neo4j"):
        neo4j_password(keyring_lookup=lambda service, user: None)
