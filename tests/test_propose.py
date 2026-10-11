"""The proposal branch is built without touching the working tree, and never pushed."""

import subprocess
from datetime import datetime, timezone

from app.agents.monitoring.propose import create_proposal_branch, git, overview
from app.agents.monitoring.weekly import run
from tests.test_weekly import fake_steps

REVIEW = "# Review: bm25 (promotion)\n\n## Template\n- conforms\n\n## Originality: passed (2% copied 8-grams)\n\n## Faithfulness: 3 of 10 sentences unsupported\n"


def repository(tmp_path):
    repo = tmp_path / "repo"
    (repo / "public" / "notes").mkdir(parents=True)
    (repo / "public" / "notes" / "rag.md").write_text("old RAG note\n", encoding="utf-8")
    for args in (["init", "-q", "-b", "main"], ["config", "user.name", "Test"], ["config", "user.email", "t@example.org"],
                 ["add", "-A"], ["commit", "-q", "-m", "base"], ["checkout", "-q", "-b", "work"]):
        git(*args, repo=repo)
    # Work in progress that the run must not touch.
    (repo / "public" / "notes" / "rag.md").write_text("uncommitted edit\n", encoding="utf-8")
    return repo


def drafts_directory(tmp_path):
    drafts = tmp_path / "drafts" / "2026-10-18_020000"
    drafts.mkdir(parents=True)
    (drafts / "bm25.md").write_text("draft BM25 note\n", encoding="utf-8")
    (drafts / "bm25.review.md").write_text(REVIEW, encoding="utf-8")
    (drafts / "rag.md").write_text("RAG note with an update entry\n", encoding="utf-8")
    return drafts


def test_drafts_land_on_a_branch_from_main_without_touching_the_working_tree(tmp_path):
    repo, drafts = repository(tmp_path), drafts_directory(tmp_path)
    status_before = git("status", "--porcelain", repo=repo)

    branch = create_proposal_branch(drafts, "2026-10-18_020000", repo=repo)

    assert branch == "proposals/2026-10-18_020000"
    assert git("show", f"{branch}:public/notes/bm25.md", repo=repo) == "draft BM25 note"
    assert git("show", f"{branch}:public/notes/rag.md", repo=repo) == "RAG note with an update entry"
    assert "bm25" in git("show", f"{branch}:proposals/2026-10-18_020000/README.md", repo=repo)
    assert git("show", f"{branch}:proposals/2026-10-18_020000/bm25.review.md", repo=repo).startswith("# Review: bm25")
    assert git("rev-parse", f"{branch}^", repo=repo) == git("rev-parse", "main", repo=repo)
    assert git("branch", "--show-current", repo=repo) == "work"
    assert git("status", "--porcelain", repo=repo) == status_before
    assert (repo / "public" / "notes" / "rag.md").read_text(encoding="utf-8") == "uncommitted edit\n"
    assert git("remote", repo=repo) == ""  # nothing to push to, and nothing was pushed


def test_a_run_without_drafts_makes_no_branch(tmp_path):
    repo = repository(tmp_path)
    empty = tmp_path / "drafts" / "empty"
    empty.mkdir(parents=True)

    assert create_proposal_branch(empty, "empty", repo=repo) is None
    assert "proposals/" not in git("branch", "--list", repo=repo)


def test_the_overview_names_each_draft_with_its_review(tmp_path):
    lines = overview("run", drafts_directory(tmp_path)).splitlines()

    assert "- **bm25** (promotion): template: conforms; originality: passed (2% copied 8-grams); faithfulness: 3 of 10 sentences unsupported" in lines


def test_a_failing_branch_does_not_fail_the_run(tmp_path):
    runs, drafts = tmp_path / "runs", tmp_path / "drafts"
    runs.mkdir()
    run_step, _ = fake_steps({}, runs, drafts)

    def propose(directory, name):
        raise subprocess.CalledProcessError(128, "git")

    summary = run(run_step=run_step, log=lambda line: None, now=lambda: datetime(2026, 10, 18, tzinfo=timezone.utc),
                  runs=runs, drafts=drafts, propose=propose)

    assert summary.failed_step is None and summary.branch is None and summary.branch_error
