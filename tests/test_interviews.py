"""/new-application, /new-round and /retro write the private repository's formats."""

import datetime as dt
import json

import pytest
import yaml
from fastapi.testclient import TestClient

from app.agents.private_refresh import RefreshStatus, Refresher
from app.backend.knowledge_radar import interviews
from app.backend.knowledge_radar.api import Indices, create_app
from app.backend.knowledge_radar.private_repo import load_documents, parse_interviewers, structural_graph

TODAY = lambda: dt.date(2026, 10, 11)  # noqa: E731
POSTING = "We need experience with RAG and model evaluation."


def new_application(root, **overrides):
    fields = dict(company_name="Müller & Söhne GmbH", industry="Insurance", role_title="ML Engineer", posting_text=POSTING,
                  round_date="20.10.2026", round_notes="Video call.",
                  interviewers=[interviews.Interviewer("Jane Doe", "Head of Data Science", "NLP")], today=TODAY)
    return interviews.create_application(root, **{**fields, **overrides})


def frontmatter(source):
    text = source if isinstance(source, str) else source.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---")[1])


def test_a_new_application_writes_company_posting_and_first_round(tmp_path):
    files = new_application(tmp_path)

    base = "companies/mueller-soehne-gmbh"
    assert files == [f"{base}/company.md", f"{base}/ml-engineer/job_posting.md", f"{base}/ml-engineer/round-1/round.md",
                     f"{base}/ml-engineer/round-1/interviewers.md"]
    assert frontmatter(tmp_path / base / "company.md") == {"name": "Müller & Söhne GmbH", "industry": "Insurance"}
    assert frontmatter(tmp_path / base / "ml-engineer" / "job_posting.md") == {"title": "ML Engineer", "date": dt.date(2026, 10, 11)}
    assert frontmatter(tmp_path / base / "ml-engineer" / "round-1" / "round.md") == {"round_number": 1, "date": dt.date(2026, 10, 20)}
    people = parse_interviewers((tmp_path / base / "ml-engineer" / "round-1" / "interviewers.md").read_text(encoding="utf-8"))
    assert people == [{"name": "Jane Doe", "role": "Head of Data Science", "focus": "NLP"}]
    # What the app writes is what the ingestion reads.
    graph = structural_graph(load_documents(tmp_path), {})
    assert {r["type"] for r in graph.relations} >= {"FOR_POSTING", "POSTED_BY", "INTERVIEWED_BY"}


def test_a_known_company_is_reused_and_an_existing_role_refused(tmp_path):
    new_application(tmp_path)

    files = new_application(tmp_path, company_name="müller & söhne gmbh", role_title="Data Scientist")
    assert files[0] == "companies/mueller-soehne-gmbh/data-scientist/job_posting.md"

    with pytest.raises(interviews.InterviewError, match="/new-round"):
        new_application(tmp_path)


def test_a_further_round_gets_the_next_number(tmp_path):
    new_application(tmp_path)

    files = interviews.create_round(tmp_path, company="mueller-soehne-gmbh", role="ml-engineer", round_date="2026-11-02")

    assert files == ["companies/mueller-soehne-gmbh/ml-engineer/round-2/round.md"]
    rounds = interviews.applications(tmp_path)[0].rounds
    assert [(r.number, r.date) for r in rounds] == [(1, "2026-10-20"), (2, "2026-11-02")]


def test_an_unknown_application_has_no_round(tmp_path):
    with pytest.raises(interviews.InterviewError, match="/new-application"):
        interviews.create_round(tmp_path, company="acme", role="ml-engineer")


def test_a_file_that_does_not_load_is_removed_with_everything_written_before(tmp_path):
    with pytest.raises(interviews.InterviewError, match="date"):
        new_application(tmp_path, round_date="next Tuesday")
    assert not (tmp_path / "companies").exists() or not any((tmp_path / "companies").iterdir())


def test_the_retro_draft_splits_answers_and_keeps_the_reflection():
    def generate(prompt, json_schema=None, **options):
        assert "Keep the candidate's wording" in prompt and "RAG evaluieren" in prompt
        return json.dumps({"questions_asked": ["Wie würdest du RAG evaluieren?", "Was ist Kalibrierung?"],
                           "struggled_with": ["Kalibrierung erklären"], "personal_improvement": ["invented"],
                           "kb_gaps_identified": ["model calibration"]})

    answers = {"questions_asked": "Wie würdest du RAG evaluieren? Und: was ist Kalibrierung?", "struggled_with": "Kalibrierung erklären",
               "personal_improvement": "", "kb_gaps_identified": "Kalibrierung", "reflection": "Lief gut."}
    text = interviews.draft_retro(answers, date="20.10.2026", generate=generate, today=TODAY)

    data = frontmatter(text)
    assert data["date"] == dt.date(2026, 10, 20)
    assert data["questions_asked"] == ["Wie würdest du RAG evaluieren?", "Was ist Kalibrierung?"]
    assert data["personal_improvement"] == []  # nothing answered, nothing invented
    assert text.endswith("---\nLief gut.\n")


def test_a_retro_is_written_once_and_must_have_lists(tmp_path):
    new_application(tmp_path)
    place = dict(company="mueller-soehne-gmbh", role="ml-engineer", round_number=1)

    with pytest.raises(Exception, match="must be a list"):
        interviews.write_retro(tmp_path, **place, text="---\nquestions_asked: one question\n---\n")
    assert not (tmp_path / "companies/mueller-soehne-gmbh/ml-engineer/round-1/retro.md").exists()

    interviews.write_retro(tmp_path, **place, text="---\ndate: 2026-10-20\nquestions_asked:\n  - Q\n---\nGood.")
    with pytest.raises(interviews.InterviewError, match="exists already"):
        interviews.write_retro(tmp_path, **place, text="---\ndate: 2026-10-21\n---\n")


class FakeRefresher:
    def __init__(self):
        self.requests = 0
        self.status = RefreshStatus(state="running")

    def request(self):
        self.requests += 1


def client(tmp_path, refresher=None, generate=None):
    return TestClient(create_app(tmp_path / "notes", indices=Indices({}), private_root=tmp_path / "private",
                                 refresher=refresher, generate=generate))


def test_the_endpoints_write_and_start_a_refresh(tmp_path):
    (tmp_path / "private").mkdir()
    refresher = FakeRefresher()
    app = client(tmp_path, refresher)

    response = app.post("/api/private/applications", json={"company_name": "ACME GmbH", "role_title": "ML Engineer",
                                                           "posting_text": POSTING, "interviewers": [{"name": "Jane Doe"}]})
    assert response.status_code == 200, response.text
    assert response.json()["refresh"]["state"] == "running" and refresher.requests == 1

    listed = app.get("/api/private/applications").json()
    assert listed["configured"] and listed["applications"][0]["company_name"] == "ACME GmbH"

    assert app.post("/api/private/rounds", json={"company": "acme-gmbh", "role": "ml-engineer"}).json()["files"] == [
        "companies/acme-gmbh/ml-engineer/round-2/round.md"]
    retro = app.post("/api/private/retro", json={"company": "acme-gmbh", "role": "ml-engineer", "round": 1,
                                                 "text": "---\ndate: 2026-10-20\n---\nGood."})
    assert retro.status_code == 200 and refresher.requests == 3
    again = app.post("/api/private/retro", json={"company": "acme-gmbh", "role": "ml-engineer", "round": 1, "text": "---\ndate: 2026-10-20\n---\n"})
    assert again.status_code == 400 and "exists already" in again.json()["detail"]


def test_without_a_private_repository_the_commands_say_so(tmp_path):
    app = TestClient(create_app(tmp_path, indices=Indices({}), private_root=None, refresher=None))

    assert app.get("/api/private/applications").json() == {"configured": False, "applications": []}
    response = app.post("/api/private/rounds", json={"company": "a", "role": "b"})
    assert response.status_code == 409 and "No private repository" in response.json()["detail"]


def test_a_refresh_requested_during_a_run_runs_once_more_afterwards():
    import threading

    release, runs = threading.Event(), []

    def run(log):
        runs.append(len(runs))
        log(f"run {len(runs)}")
        if len(runs) == 1:
            release.wait(5)

    refresher = Refresher(run)
    refresher.request()
    refresher.request()
    refresher.request()  # several requests during a run: one more run
    release.set()
    for _ in range(100):
        if refresher.status.state == "done" and len(runs) == 2 and not refresher.pending:
            break
        threading.Event().wait(0.02)

    assert len(runs) == 2 and refresher.status.state == "done" and refresher.status.log == ["run 2"]


def test_a_failing_refresh_is_reported():
    def run(log):
        raise RuntimeError("Ollama is not running")

    refresher = Refresher(run)
    refresher.request()
    refresher.thread.join(5)

    assert refresher.status.state == "failed" and "Ollama is not running" in refresher.status.message
