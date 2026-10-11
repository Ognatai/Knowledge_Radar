"""The private repository reader and the structural graph, on an invented fixture."""

import pytest
import yaml

from app.agents.private_ingest import ingest, write_structure
from app.backend.knowledge_radar.graph import Entity
from app.backend.knowledge_radar.private_repo import (
    PrivateRepoError,
    StructuralGraph,
    load_documents,
    parse_interviewers,
    structural_graph,
)

KNOWN = {
    "calibration": Entity("calibration", "Concept", "Model calibration", "Modellkalibrierung"),
    "jane-doe-public": Entity("jane-doe-public", "Person", "Jane Doe", "Jane Doe"),
}


def write(root, relative, text):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "private"
    write(root, "notes/star-stories.md", "---\ntitle: STAR stories\n---\nA story.\n")
    write(root, "companies/acme-gmbh/company.md", "---\nname: ACME GmbH\naliases: [ACME]\n---\nInsurer.\n")
    write(root, "companies/acme-gmbh/ml-engineer/job_posting.md", "---\ntitle: ML Engineer\ndate: 2026-10-01\n---\nWe need RAG.\n")
    round_dir = "companies/acme-gmbh/ml-engineer/round-1"
    write(root, f"{round_dir}/round.md", "---\nround_number: 1\ndate: 2026-10-20\n---\nOnline.\n")
    write(root, f"{round_dir}/interviewers.md", "## Jane Doe\n- role: Head of Data Science\n- focus: NLP\n\n## John Roe\n- role: HR\n")
    write(
        root,
        f"{round_dir}/retro.md",
        "---\ndate: 2026-10-20\nquestions_asked: [\"How to evaluate RAG?\"]\nkb_gaps_identified: [model calibration, quantum annealing]\n---\nOk.\n",
    )
    write(root, f"{round_dir}/notes/call.md", "Talked about the team.\n")
    write(root, "companies/acme-gmbh/ml-engineer/round-2/retro.md", "---\nquestions_asked: []\n---\nNo round.md yet.\n")
    return root


def test_documents_are_read_by_kind_and_place(repo):
    documents = load_documents(repo)

    kinds = [(d.kind, d.company, d.role, d.round) for d in documents]
    assert ("note", None, None, None) in kinds
    assert ("company", "acme-gmbh", None, None) in kinds
    assert ("job_posting", "acme-gmbh", "ml-engineer", None) in kinds
    assert ("round_note", "acme-gmbh", "ml-engineer", 1) in kinds
    retro = next(d for d in documents if d.kind == "retro" and d.round == 1)
    assert retro.id == "companies/acme-gmbh/ml-engineer/round-1/retro"
    assert retro.frontmatter["questions_asked"] == ["How to evaluate RAG?"]


def test_interviewers_are_sections_with_fields():
    people = parse_interviewers("## Jane Doe\n- role: Head of Data Science\n- focus: NLP, MLOps\n\n## John Roe\n- role: HR\n")

    assert people == [
        {"name": "Jane Doe", "role": "Head of Data Science", "focus": "NLP, MLOps"},
        {"name": "John Roe", "role": "HR"},
    ]


def test_the_folders_become_a_connected_graph(repo):
    graph = structural_graph(load_documents(repo), KNOWN)

    ids = {e["id"]: e["type"] for e in graph.entities}
    assert ids["company-acme-gmbh"] == "Company"
    assert ids["posting-acme-gmbh-ml-engineer"] == "JobPosting"
    assert ids["round-acme-gmbh-ml-engineer-1"] == "InterviewRound"
    assert ids["round-acme-gmbh-ml-engineer-2"] == "InterviewRound"  # a retro without round.md still has its round
    assert ids["person-john-roe"] == "Person"
    assert "person-jane-doe" not in ids  # resolved to the known person
    triples = {(r["from"], r["type"], r["to"]) for r in graph.relations}
    assert ("posting-acme-gmbh-ml-engineer", "POSTED_BY", "company-acme-gmbh") in triples
    assert ("round-acme-gmbh-ml-engineer-1", "FOR_POSTING", "posting-acme-gmbh-ml-engineer") in triples
    assert ("round-acme-gmbh-ml-engineer-1", "INTERVIEWED_BY", "jane-doe-public") in triples
    assert ("retro-acme-gmbh-ml-engineer-1", "RETRO_OF", "round-acme-gmbh-ml-engineer-1") in triples
    assert ("retro-acme-gmbh-ml-engineer-1", "IDENTIFIED_GAP_IN", "calibration") in triples
    assert graph.open_gaps == [{"retro": "retro-acme-gmbh-ml-engineer-1", "topic": "quantum annealing"}]


@pytest.mark.parametrize(
    "relative, text, message",
    [
        ("companies/Acme/company.md", "---\nname: A\n---\n", "lowercase slugs"),
        ("companies/acme/company.md", "---\nindustry: x\n---\n", "missing frontmatter field"),
        ("companies/acme/role/r1/round.md", "---\nround_number: 1\n---\n", "round-<n>"),
        ("companies/acme/role/round-1/retro.md", "---\nkb_gaps_identified: calibration\n---\n", "must be a list"),
    ],
)
def test_malformed_files_are_reported(tmp_path, relative, text, message):
    root = tmp_path / "private"
    if not relative.endswith("company.md"):
        write(root, "companies/acme/company.md", "---\nname: ACME\n---\n")
    write(root, relative, text)

    with pytest.raises(PrivateRepoError, match=message):
        load_documents(root)


def test_the_structure_is_written_into_the_private_repository(repo):
    graph, path = ingest(repo, KNOWN)

    assert path == (repo / "graph" / "structure.yaml").resolve()
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["open_gaps"] == graph.open_gaps and len(data["relations"]) == len(graph.relations)


def test_nothing_is_written_into_the_public_repository(tmp_path):
    public = tmp_path / "public-repo"
    with pytest.raises(PrivateRepoError, match="public repository"):
        write_structure(public / "private-inside", StructuralGraph(), public_root=public)
