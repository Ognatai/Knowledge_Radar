import json
from datetime import datetime, timezone

from app.agents.monitoring.weekly import STEPS, Step, Summary, diagram, run

NOW = datetime(2026, 10, 18, 2, 0, tzinfo=timezone.utc)


def fake_steps(codes, runs, drafts):
    """A step runner that returns the given exit codes and writes what the real steps write."""
    called = []

    def run_step(step, log):
        called.append(step.name)
        if step.name == "fetch sources":
            (runs / "findings-2026-10-18_020000.jsonl").write_text('{"id": "a"}\n{"id": "b"}\n', encoding="utf-8")
        if step.name == "assess relevance":
            proposals = [{"decision": "update"}, {"decision": "new_topic"}, {"decision": "promotion"}]
            (runs / "relevance-2026-10-18_020000.json").write_text(json.dumps({"proposals": proposals}), encoding="utf-8")
        if step.name == "write drafts":
            out = drafts / "2026-10-18_020000"
            out.mkdir(parents=True)
            for name in ("bm25.md", "bm25.review.md", "gpt.md", "gpt.review.md"):
                (out / name).write_text("x", encoding="utf-8")
        return codes.get(step.name, 0)

    return run_step, called


def test_the_run_executes_every_step_and_summarises_proposals_and_drafts(tmp_path):
    runs, drafts = tmp_path / "runs", tmp_path / "drafts"
    runs.mkdir()
    run_step, called = fake_steps({}, runs, drafts)

    summary = run(run_step=run_step, log=lambda line: None, now=lambda: NOW, runs=runs, drafts=drafts, propose=lambda d, r: f"proposals/{r}")

    assert called == [step.name for step in STEPS]
    assert summary.findings == 2
    assert summary.proposals == {"new_topic": 1, "promotion": 1, "update": 1}
    assert summary.drafts == ["bm25", "gpt"]
    assert summary.line() == "2 new findings; proposals: 1 new_topic, 1 promotion, 1 update; 2 drafts to review on branch proposals/2026-10-18_020000."
    assert json.loads((runs / "weekly-2026-10-18_020000.json").read_text(encoding="utf-8"))["findings"] == 2


def test_a_failing_required_step_stops_the_run(tmp_path):
    runs, drafts = tmp_path / "runs", tmp_path / "drafts"
    runs.mkdir()
    run_step, called = fake_steps({"update index": 1}, runs, drafts)

    summary = run(run_step=run_step, log=lambda line: None, now=lambda: NOW, runs=runs, drafts=drafts, propose=lambda d, r: f"proposals/{r}")

    assert called == ["validate notes", "update index"]
    assert summary.failed_step == "update index"
    assert summary.line() == "Step 'update index' failed; see the log."


def test_a_failing_curator_does_not_fail_the_run(tmp_path):
    runs, drafts = tmp_path / "runs", tmp_path / "drafts"
    runs.mkdir()
    run_step, _ = fake_steps({"write drafts": 1}, runs, drafts)

    summary = run(run_step=run_step, log=lambda line: None, now=lambda: NOW, runs=runs, drafts=drafts, propose=lambda d, r: f"proposals/{r}")

    assert summary.failed_step is None and summary.steps["write drafts"] == 1


def test_a_week_without_proposals_says_so():
    assert Summary(started="x", findings=4).line() == "4 new findings, no proposals this week."


def test_the_run_is_a_graph_that_skips_to_the_summary_after_a_required_step():
    mermaid = diagram()
    assert "validate_notes -.-> summarise;" in mermaid and "validate_notes -.-> update_index;" in mermaid
    # Optional steps always go on.
    assert "write_drafts --> propose_inbox;" in mermaid
    assert "\\20" not in mermaid
