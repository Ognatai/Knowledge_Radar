"""CV per application, what the company told in a retro, and practice questions on request."""

import datetime as dt
import json

import yaml

from app.backend.knowledge_radar import prep
from app.backend.knowledge_radar.interviews import create_application, draft_retro, write_retro
from app.backend.knowledge_radar.models import NoteDetail
from app.backend.knowledge_radar.private_repo import load_documents

TODAY = lambda: dt.date(2026, 10, 12)  # noqa: E731
NOTES = {"neo4j": NoteDetail.model_construct(slug="neo4j", title_en="Neo4j", title_de="Neo4j", content_en="", content_de="")}


def make(tmp_path, cv=""):
    root = tmp_path / "private"
    create_application(root, company_name="ACME GmbH", role_title="Graph Engineer", posting_text="Neo4j und Cypher.",
                       round_date="2026-10-20", cv_text=cv, today=TODAY)
    return root


def test_the_cv_is_stored_with_the_application(tmp_path):
    root = make(tmp_path, cv="2019-2025 PhD on gender bias in NLP at LMU Munich.")
    kinds = {d.id: d.kind for d in load_documents(root)}
    assert kinds["companies/acme-gmbh/graph-engineer/cv"] == "cv"
    assert "PhD on gender bias" in (root / "companies/acme-gmbh/graph-engineer/cv.md").read_text(encoding="utf-8")


def test_without_a_cv_no_file_is_written(tmp_path):
    root = make(tmp_path)
    assert not (root / "companies/acme-gmbh/graph-engineer/cv.md").exists()


def test_what_the_company_told_is_kept_verbatim_and_added_to_the_company_note(tmp_path):
    root = make(tmp_path)

    def generate(prompt, **options):
        assert "only questions the interviewers actually asked" in prompt
        return json.dumps({key: [] for key in ("questions_asked", "struggled_with", "personal_improvement", "kb_gaps_identified")})

    text = draft_retro({"questions_asked": "Keine Fachfragen.", "company_told": "Team of 12, builds GraphRAG for insurers."},
                       date="2026-10-20", generate=generate, today=TODAY)
    assert yaml.safe_load(text.split("---")[1])["company_told"] == "Team of 12, builds GraphRAG for insurers."
    written = write_retro(root, company="acme-gmbh", role="graph-engineer", round_number=1, text=text)
    company = (root / "companies/acme-gmbh/company.md").read_text(encoding="utf-8")
    assert "### From the interview: graph-engineer, round 1 (2026-10-20)" in company
    assert company.rstrip().endswith("Team of 12, builds GraphRAG for insurers.")
    assert "companies/acme-gmbh/company.md" in written


def model(prompts):
    def generate(prompt, json_schema=None, **options):
        prompts.append(prompt)
        properties = json_schema["properties"]
        if "sentences" in properties:
            return json.dumps({"sentences": [{"text": "Ich habe in München promoviert.", "evidence": "PhD on gender bias in NLP"}],
                               "adaptations": []})
        if "topic" in properties["questions"]["items"]["properties"]:
            return json.dumps({"questions": [{"question": "Wie funktioniert MERGE?", "topic": "Neo4j"},
                                             {"question": "Warum diese Stelle?", "topic": "general"}]})
        return json.dumps({"questions": []})
    return generate


def write_topics(root):
    topics = {"topics": {"companies/acme-gmbh/graph-engineer/job_posting": [{"name": "Neo4j", "phrase": "Neo4j", "note": "neo4j"}]}}
    (root / "graph").mkdir(exist_ok=True)
    (root / "graph" / "topics.yaml").write_text(yaml.safe_dump(topics), encoding="utf-8")


def test_the_cv_backs_the_pitch_and_practice_questions_come_only_on_request(tmp_path):
    root = make(tmp_path, cv="2019-2025 PhD on gender bias in NLP at LMU Munich.")
    write_topics(root)
    prompts = []
    without = prep.draft_prep(root, "acme-gmbh", "graph-engineer", 1, notes=NOTES, stores={}, generate=model(prompts),
                              embed=lambda texts: [[0.1] for _ in texts], today=TODAY)
    assert "PhD on gender bias" in prompts[0]
    assert "Ich habe in München promoviert." in without and "prüfen: nicht aus deinen Notizen belegt" not in without
    assert "## Übungsfragen" not in without and len(prompts) == 2

    with_practice = prep.draft_prep(root, "acme-gmbh", "graph-engineer", 1, notes=NOTES, stores={}, generate=model([]),
                                    embed=lambda texts: [[0.1] for _ in texts], today=TODAY, practice=True)
    section = with_practice.split("## Übungsfragen")[1]
    assert "- Wie funktioniert MERGE? _(Lernen mit [Neo4j]" in section
    assert "- Warum diese Stelle?\n" in section + "\n"
