"""Topics to study for a posting: tied to its words, matched to notes without forcing a match."""

import json

import yaml

from app.agents.posting_topics import extract_topics, read_topics, registry_note, topics_graph
from app.agents.private_extract import TopicIndex
from app.backend.knowledge_radar.graph import Entity
from app.backend.knowledge_radar.interviews import create_application
from app.backend.knowledge_radar.models import NoteDetail
from app.backend.knowledge_radar.private_repo import load_documents

POSTING = "Erste Erfahrung mit Knowledge Graphen in RDF oder Neo4j. Gute Python-Kenntnisse. Teamgeist."
NOTES = {slug: NoteDetail.model_construct(slug=slug, title_en=title, title_de=title, content_en="", content_de="")
         for slug, title in [("rdf", "RDF"), ("python", "Python"), ("knowledge-graphs", "Knowledge graphs")]}
ENTITIES = {
    "rdf": Entity("rdf", "Technology", "Resource Description Framework", "RDF", ["RDF"], note="rdf"),
    "python": Entity("python", "Technology", "Python", "Python", note="python"),
    "neo4j": Entity("neo4j", "Technology", "Neo4j", "Neo4j"),  # known, but no note of its own
}


def model(calls):
    def generate(prompt, json_schema=None, **options):
        calls.append(prompt)
        if "topics" in json_schema["properties"]:
            return json.dumps({"topics": [
                {"name": "RDF", "phrase": "RDF"}, {"name": "Neo4j", "phrase": "Neo4j"},
                {"name": "Python", "phrase": "Python-Kenntnisse"}, {"name": "Knowledge Graphs", "phrase": "Knowledge Graphen"},
                {"name": "Kubernetes", "phrase": "Kubernetes-Cluster"},  # not in the posting
            ]})
        return json.dumps({"article": "knowledge-graphs" if "Knowledge Graphs" in prompt else "none"})
    return generate


def topic_index():
    return TopicIndex(list(NOTES), [n.title_en for n in NOTES.values()], [[1.0] for _ in NOTES])


def repo(tmp_path):
    root = tmp_path / "private"
    create_application(root, company_name="ACME GmbH", role_title="Graph Engineer", posting_text=POSTING)
    return root, [d for d in load_documents(root) if d.kind == "job_posting"]


def test_topics_must_be_named_in_the_posting(tmp_path):
    _, postings = repo(tmp_path)
    names = [t["name"] for t in extract_topics(postings[0], model([]))]
    assert names == ["RDF", "Neo4j", "Python", "Knowledge Graphs"]


def test_the_registry_matches_by_name_and_alias_without_a_model():
    assert registry_note("rdf", ENTITIES, NOTES) == ("rdf", "rdf")
    assert registry_note("Neo4j", ENTITIES, NOTES) == (None, "neo4j")
    assert registry_note("Kubernetes", ENTITIES, NOTES) == (None, None)


def test_the_model_may_find_no_note_and_an_unchanged_posting_is_kept(tmp_path):
    root, postings = repo(tmp_path)
    calls = []
    topics_graph(root, postings, ENTITIES, NOTES, topic_index, embed=lambda texts: [[1.0] for _ in texts],
                 generate=model(calls), log=lambda line: None)
    topics = {t["name"]: t["note"] for t in read_topics(root, postings[0].id)}
    assert topics == {"RDF": "rdf", "Neo4j": None, "Python": "python", "Knowledge Graphs": "knowledge-graphs"}
    # One call lists the topics; only the topics the registry does not resolve to a note go to the model.
    assert len(calls) == 3

    def must_not_run(*args, **kwargs):
        raise AssertionError("an unchanged posting goes to the model again")

    topics_graph(root, postings, ENTITIES, NOTES, topic_index, embed=lambda texts: [], generate=must_not_run, log=lambda line: None)
    assert yaml.safe_load((root / "graph" / "topics.yaml").read_text(encoding="utf-8"))["topics"][postings[0].id][0]["name"] == "RDF"
