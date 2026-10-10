"""Integration test against a real Neo4j instance.

It wipes the database, so it runs only when KNOWLEDGE_RADAR_NEO4J_TEST_URI names a
throwaway instance (password in KNOWLEDGE_RADAR_NEO4J_TEST_PASSWORD), never the
local index itself.
"""

import os

import pytest

from app.backend.knowledge_radar.graph import load_graph
from app.backend.knowledge_radar.index import Neo4jStore, update_index
from app.backend.knowledge_radar.notes import load_notes
from tests.test_graph import ALPHA_RELATIONS, extraction, note_hash, setup_repo, write_extraction

TEST_URI = os.environ.get("KNOWLEDGE_RADAR_NEO4J_TEST_URI")
pytestmark = pytest.mark.skipif(not TEST_URI, reason="no throwaway Neo4j instance configured")


def fake_embed(texts):
    return [[1.0, float(position), 0.5] for position, _ in enumerate(texts, start=1)]


@pytest.fixture
def store():
    from neo4j import GraphDatabase

    password = os.environ.get("KNOWLEDGE_RADAR_NEO4J_TEST_PASSWORD", "")
    with GraphDatabase.driver(TEST_URI, auth=("neo4j", password)) as driver:
        driver.execute_query("MATCH (n) DETACH DELETE n")
        driver.execute_query("DROP INDEX chunk_embedding IF EXISTS")
        yield Neo4jStore(driver)


def count(store, query):
    return store._run(query)[0][0]


def test_index_round_trip(tmp_path, store):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    write_extraction(graph_dir, "alpha", extraction(note_hash(alpha), ALPHA_RELATIONS))
    notes = load_notes(notes_dir)
    graph = load_graph(graph_dir, notes, notes_dir)

    first = update_index(store, notes, graph, notes_dir, embed=fake_embed, model="m")
    second = update_index(store, notes, graph, notes_dir, embed=fake_embed, model="m")

    assert first.full_rebuild and first.embedded == ["alpha", "beta"]
    assert second.embedded == []
    assert count(store, "MATCH (n:Note) RETURN count(n)") == 2
    assert count(store, "MATCH (:Note {slug: 'alpha'})-[:DISCUSSES]->(e:Entity) RETURN count(e)") == 3
    assert count(store, "MATCH (:Note {slug: 'alpha'})-[:RELATED_TO]->(:Note {slug: 'beta'}) RETURN count(*)") == 1
    assert count(store, "MATCH (:Entity {id: 'alpha'})-[r:DEVELOPED_BY]->(:Organization {id: 'microsoft'}) RETURN count(r)") == 1
    assert count(store, "MATCH (c:Chunk)-[:PART_OF]->(:Note) RETURN count(c)") == 4
    hits = store.search([1.0, 1.0, 0.5], limit=2)
    assert len(hits) == 2 and hits[0]["note"] in {"alpha", "beta"}


def test_changed_and_removed_notes_are_updated(tmp_path, store):
    notes_dir, graph_dir, alpha = setup_repo(tmp_path)
    notes = load_notes(notes_dir)
    update_index(store, notes, load_graph(graph_dir, notes, notes_dir), notes_dir, embed=fake_embed, model="m")

    alpha.write_text(alpha.read_text(encoding="utf-8").replace("builds on", "extends"), encoding="utf-8")
    notes = load_notes(notes_dir)
    result = update_index(store, notes, load_graph(graph_dir, notes, notes_dir), notes_dir, embed=fake_embed, model="m")

    assert result.embedded == ["alpha"]
    texts = [record[0] for record in store._run("MATCH (c:Chunk)-[:PART_OF]->(:Note {slug: 'alpha'}) RETURN c.text")]
    assert any("extends" in text for text in texts)

    result = update_index(store, notes, load_graph(graph_dir, notes, notes_dir), notes_dir, embed=fake_embed, model="other")
    assert result.full_rebuild
    assert count(store, "MATCH (c:Chunk) RETURN count(c)") == 4
