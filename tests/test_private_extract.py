"""Extraction over the private repository, with a fake local model."""

import json
import re

import pytest
import yaml

from app.agents.private_extract import (
    TopicIndex,
    document_slug,
    extract_free_text,
    extract_requirements,
    match_requirement,
    private_graph_directory,
    requirements_graph,
)
from app.backend.knowledge_radar.graph import Entity
from app.backend.knowledge_radar.models import NoteDetail
from app.backend.knowledge_radar.private_repo import PrivateRepoError, load_documents
from tests.test_private_repo import repo  # noqa: F401  (fixture)

KNOWN = {"retrieval-augmented-generation": Entity("retrieval-augmented-generation", "Method", "Retrieval-Augmented Generation", "RAG", ["RAG"])}


def extraction_model(prompt, json_schema=None, **options):
    """Registers one organisation and discusses RAG; relates something to the document itself."""
    if "new_entities" in (json_schema or {}).get("properties", {}):
        found = re.search(r"private-[a-z0-9-]+", prompt)
        slug = found.group(0) if found else "private-document"
        return json.dumps(
            {
                "new_entities": [{"id": "acme-labs", "type": "Organization", "name_en": "ACME Labs", "name_de": "ACME Labs"}],
                "discusses": ["acme-labs", "retrieval-augmented-generation"],
                "relations": [{"from": slug, "type": "BASED_ON", "to": "retrieval-augmented-generation", "evidence": "x"}],
            }
        )
    return json.dumps({})


def test_free_text_is_extracted_into_the_private_graph_only(repo):
    (repo / "notes" / "search.md").write_text("ACME Labs uses RAG for search.\n", encoding="utf-8")
    results = extract_free_text(repo, load_documents(repo), KNOWN, generate=extraction_model, embed=None, log=lambda line: None)

    retro = next(d for d in load_documents(repo) if d.id == "notes/search")
    extraction = results[retro.id]
    assert extraction.discusses == ["acme-labs", "retrieval-augmented-generation"]
    assert extraction.relations == []  # relations to the document itself are dropped
    graph = repo / "graph"
    assert (graph / "extractions" / f"{document_slug(retro)}.yaml").is_file()
    registry = yaml.safe_load((graph / "entities.yaml").read_text(encoding="utf-8"))
    assert [e["id"] for e in registry["entities"]] == ["acme-labs"]


def test_unchanged_documents_are_skipped(repo):
    extract_free_text(repo, load_documents(repo), KNOWN, generate=extraction_model, embed=None, log=lambda line: None)

    def must_not_run(prompt, **options):
        raise AssertionError("an unchanged document was extracted again")

    assert extract_free_text(repo, load_documents(repo), KNOWN, generate=must_not_run, embed=None, log=lambda line: None) == {}


def test_requirements_must_appear_in_the_posting(repo):
    posting = next(d for d in load_documents(repo) if d.kind == "job_posting")

    def generate(prompt, json_schema=None, **options):
        return json.dumps({"requirements": [{"text": "RAG", "category": "skill"}, {"text": "10 years of Rust", "category": "experience"}]})

    assert extract_requirements(posting, generate) == [{"text": "RAG", "category": "skill"}]


def test_requirement_matches_are_limited_to_the_shortlist():
    def generate(prompt, json_schema=None, **options):
        assert json_schema["properties"]["matches"]["items"]["enum"] == ["rag", "bm25"]
        return json.dumps({"matches": ["rag", "invented", "rag"]})

    assert match_requirement("RAG", [("rag", "RAG: ..."), ("bm25", "BM25: ...")], generate) == ["rag"]


def test_requirements_graph_links_postings_requirements_and_topics(repo):
    notes = {"rag": NoteDetail.model_construct(slug="rag", title_en="RAG", content_en="### TL;DR\nRetrieval.\n")}

    def embed(texts):
        return [[1.0] for _ in texts]

    def generate(prompt, json_schema=None, **options):
        if "requirements" in json_schema["properties"]:
            return json.dumps({"requirements": [{"text": "RAG", "category": "skill"}]})
        return json.dumps({"matches": ["rag"]})

    postings = [d for d in load_documents(repo) if d.kind == "job_posting"]
    path = requirements_graph(repo, postings, TopicIndex.build(notes, embed), embed=embed, generate=generate, log=lambda line: None)

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["entities"][0]["id"] == "req-acme-gmbh-ml-engineer-1"
    triples = {(r["from"], r["type"], r["to"]) for r in data["relations"]}
    assert triples == {
        ("posting-acme-gmbh-ml-engineer", "REQUIRES", "req-acme-gmbh-ml-engineer-1"),
        ("req-acme-gmbh-ml-engineer-1", "MATCHES", "rag"),
    }


def test_private_results_never_go_into_the_public_repository(tmp_path):
    with pytest.raises(PrivateRepoError, match="public repository"):
        private_graph_directory(tmp_path / "inside", public_root=tmp_path)
