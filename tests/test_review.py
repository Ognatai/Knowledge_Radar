"""The Review Dashboard: public proposal branches (local) and private inbox branches (GitLab)."""

import datetime as dt
import json
import subprocess
from datetime import date, datetime, timezone

import pytest

from app.agents.monitoring.findings import Finding
from app.agents.monitoring.inbox import gap_findings, gap_note, note_path, propose_inbox
from app.agents.monitoring.propose import create_proposal_branch
from app.backend.knowledge_radar.private_git import PrivateRepo, https_url
from app.backend.knowledge_radar.review import PrivateInbox, PublicProposals, ReviewError
from tests.test_propose import REVIEW, drafts_directory, repository

TODAY = lambda: dt.date(2026, 10, 18)  # noqa: E731


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True, text=True).stdout.strip()


def public(tmp_path, discussing=lambda slug: 4):
    repo = repository(tmp_path)
    create_proposal_branch(drafts_directory(tmp_path), "2026-10-18_020000", repo=repo)
    state = tmp_path / "state"
    return repo, PublicProposals(repo / ".git", state / "review-decisions.json", state / "promotions-declined.json", discussing, TODAY)


def test_runs_list_their_drafts_with_kind_and_verdicts(tmp_path):
    _, proposals = public(tmp_path)

    [run] = proposals.runs()

    assert run.run == "2026-10-18_020000" and run.branch == "proposals/2026-10-18_020000"
    drafts = {d.slug: d for d in run.drafts}
    assert drafts["bm25"].kind == "promotion" and drafts["bm25"].new_note
    assert drafts["bm25"].verdicts.startswith("template: conforms; originality: passed")
    assert drafts["rag"].kind == "draft" and not drafts["rag"].new_note
    assert all(d.status == "open" for d in run.drafts)


def test_the_detail_shows_review_diff_and_draft(tmp_path):
    _, proposals = public(tmp_path)

    detail = proposals.detail("2026-10-18_020000", "rag")

    assert "-old RAG note" in detail["diff"] and "+RAG note with an update entry" in detail["diff"]
    assert detail["draft"].startswith("RAG note")
    with pytest.raises(ReviewError):
        proposals.detail("../../etc", "rag")


def test_a_discarded_promotion_counts_as_declined(tmp_path):
    _, proposals = public(tmp_path)

    proposals.decide("2026-10-18_020000", "bm25", "discarded")
    proposals.decide("2026-10-18_020000", "rag", "wanted")

    statuses = {d.slug: d.status for d in proposals.runs()[0].drafts}
    assert statuses == {"bm25": "discarded", "rag": "wanted"}
    declined = json.loads(proposals.declined_path.read_text(encoding="utf-8"))
    assert declined == {"bm25": {"checked": "2026-10-18", "discarded_in_review": True, "discussing_notes": 4}}


def test_removing_a_run_deletes_only_its_branch(tmp_path):
    repo, proposals = public(tmp_path)
    status = git(repo, "status", "--porcelain")

    proposals.remove("2026-10-18_020000")

    assert proposals.runs() == []
    assert git(repo, "branch", "--show-current") == "work" and git(repo, "status", "--porcelain") == status


def finding(title, query=None, tier="preprint", published=date(2026, 10, 15), summary="About things."):
    return Finding(id=f"arxiv:{title}", source="arXiv", category="arxiv", url=f"https://arxiv.org/abs/{len(title)}", title=title,
                   summary=summary, published=published, authors=[], tier=tier, source_kind="primary_research",
                   fetched_at=datetime(2026, 10, 18, tzinfo=timezone.utc), query=query)


def test_findings_belong_to_a_gap_by_search_phrase_or_mention():
    findings = [finding("Temperature scaling revisited", query="model calibration"),
                finding("A survey", summary="We study model calibration of LLMs.", tier="peer_reviewed", published=date(2026, 10, 1)),
                finding("Miscalibration", summary="no match"), finding("RAG at scale", query="retrieval")]

    grouped = gap_findings(findings, ["model calibration", "quantum annealing"])

    assert list(grouped) == ["model calibration"]
    assert [f.title for f in grouped["model calibration"]] == ["A survey", "Temperature scaling revisited"]


def test_the_gap_note_is_a_private_note_with_a_reading_list():
    text = gap_note("model calibration", [finding("Temperature scaling revisited", query="model calibration")], "2026-10-18_020000")

    assert note_path("2026-10-18_020000", "model calibration") == "notes/gap-news-2026-10-18-model-calibration.md"
    assert text.startswith("---\ntitle: 'New on your gap: model calibration (2026-10-18)'\ngap_topic: model calibration\n")
    assert "## [Temperature scaling revisited](https://arxiv.org/abs/29)\n_arXiv, 2026-10-15_" in text


@pytest.fixture
def private(tmp_path):
    """A bare 'GitLab' and the user's checkout of it, on main, with an uncommitted retro."""
    remote = tmp_path / "gitlab.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
    checkout = tmp_path / "private"
    subprocess.run(["git", "clone", "-q", str(remote), str(checkout)], check=True, capture_output=True)
    for args in (["config", "user.name", "Test"], ["config", "user.email", "t@example.org"]):
        git(checkout, *args)
    (checkout / "notes").mkdir()
    (checkout / "notes" / "profile.md").write_text("---\ntitle: Profile\n---\nMe.\n", encoding="utf-8")
    git(checkout, "add", "-A")
    git(checkout, "commit", "-q", "-m", "start")
    git(checkout, "push", "-q", "origin", "main")
    (checkout / "retro.md").write_text("uncommitted\n", encoding="utf-8")
    return checkout


def propose(checkout, run="2026-10-18_020000"):
    files = {note_path(run, "model calibration"): gap_note("model calibration", [finding("Temperature scaling")], run)}
    return propose_inbox(PrivateRepo(checkout), run, files)


def test_the_weekly_run_pushes_an_inbox_branch_without_touching_the_checkout(private):
    status = git(private, "status", "--porcelain")

    assert propose(private) == "inbox/2026-10-18_020000"

    assert "refs/heads/inbox/2026-10-18_020000" in git(private, "ls-remote", "origin")
    assert git(private, "status", "--porcelain") == status and git(private, "branch", "--show-current") == "main"


def test_accepting_merges_into_main_and_adds_only_the_notes(private):
    propose(private)
    inbox = PrivateInbox(PrivateRepo(private))
    [branch] = inbox.branches()
    assert branch.files[0].title == "New on your gap: model calibration (2026-10-18)"

    accepted = inbox.accept(branch.branch)

    assert accepted == ["notes/gap-news-2026-10-18-model-calibration.md"]
    assert (private / accepted[0]).read_text(encoding="utf-8").startswith("---\ntitle: 'New on your gap")
    assert git(private, "status", "--porcelain") == "?? retro.md"  # the user's own file untouched, the note committed
    assert git(private, "rev-parse", "main") == git(private, "ls-remote", "origin", "refs/heads/main").split()[0]
    assert "inbox/" not in git(private, "ls-remote", "origin") and inbox.branches() == []


def test_discarding_deletes_the_branch_on_gitlab(private):
    propose(private)
    inbox = PrivateInbox(PrivateRepo(private))

    inbox.discard("inbox/2026-10-18_020000")

    assert "inbox/" not in git(private, "ls-remote", "origin") and inbox.branches() == []
    assert not (private / "notes" / "gap-news-2026-10-18-model-calibration.md").exists()


def test_accepting_needs_the_checkout_up_to_date_with_gitlab(private, tmp_path):
    propose(private)
    other = tmp_path / "other"
    subprocess.run(["git", "clone", "-q", str(tmp_path / "gitlab.git"), str(other)], check=True, capture_output=True)
    (other / "notes" / "x.md").write_text("x\n", encoding="utf-8")
    for args in (["-c", "user.name=T", "-c", "user.email=t@e", "add", "-A"], ["-c", "user.name=T", "-c", "user.email=t@e", "commit", "-q", "-m", "x"],
                 ["push", "-q", "origin", "main"]):
        git(other, *args)

    with pytest.raises(ReviewError, match="git pull"):
        PrivateInbox(PrivateRepo(private)).accept("inbox/2026-10-18_020000")


def test_ssh_remotes_become_https_for_the_token():
    assert https_url("git@gitlab.com:urchs01/knowledge_radar_private.git") == "https://gitlab.com/urchs01/knowledge_radar_private.git"
    assert https_url("https://gitlab.com/a/b.git") == "https://gitlab.com/a/b.git"


def test_the_dashboard_api_lists_decides_and_removes(tmp_path):
    from fastapi.testclient import TestClient

    from app.backend.knowledge_radar.api import Indices, create_app

    _, proposals = public(tmp_path)
    client = TestClient(create_app(tmp_path / "notes", indices=Indices({}), private_root=None, refresher=None, proposals=proposals, inbox=None))

    overview = client.get("/api/review").json()
    assert overview["private"] == {"configured": False, "branches": [], "error": None}
    assert [d["slug"] for d in overview["public"]["runs"][0]["drafts"]] == ["bm25", "rag"]
    assert client.post("/api/review/public/2026-10-18_020000/rag", json={"status": "wanted"}).status_code == 200
    assert client.post("/api/review/public/2026-10-18_020000/nope", json={"status": "wanted"}).status_code == 400
    assert client.post("/api/review/private/discard", json={"branch": "inbox/x"}).status_code == 409
    assert client.post("/api/review/public/2026-10-18_020000").json() == {"removed": "2026-10-18_020000"}
    assert client.get("/api/review").json()["public"]["runs"] == []
