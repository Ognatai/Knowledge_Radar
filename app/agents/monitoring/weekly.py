"""The weekly monitoring run: every pipeline step in order, with one summary.

1. validate the public notes
2. update the local index (Neo4j must be running)
3. source agents: new findings of the last 7 days
4. relevance agent: proposals, including promotions
5. curator: drafts and review reports for the proposals
6. inbox: findings on gaps from interview retros, as a branch `inbox/<run>` in the
   private GitLab repository (inbox.py)
7. the drafts on a local branch `proposals/<run>` (propose.py), never pushed

Each step runs as its own process, so that its output lands in the log as it
happens and a crash in one step is reported instead of killing the run. Steps 1
to 4 must succeed; the curator may fail on single proposals (they are retried
next week) and still count as done, and a failed inbox does not fail the run. The summary is written to
`.knowledge-radar/monitoring/runs/weekly-<time>.json` and printed as one line
for the notification.

    python -m app.agents.monitoring.weekly
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from app.agents.monitoring.findings import RUNS_DIRECTORY
from app.agents.monitoring.propose import create_proposal_branch

DRAFTS_DIRECTORY = RUNS_DIRECTORY.parent / "drafts"


@dataclass(frozen=True)
class Step:
    name: str
    module: str
    required: bool = True
    args: tuple[str, ...] = ()


STEPS = [
    Step("validate notes", "app.agents.validate_notes"),
    Step("update index", "app.backend.knowledge_radar.index", args=("update",)),
    Step("fetch sources", "app.agents.monitoring.run_sources"),
    Step("assess relevance", "app.agents.monitoring.relevance"),
    Step("write drafts", "app.agents.monitoring.curator", required=False),
    # Findings on gaps from interview retros, as a branch in the private GitLab repo.
    Step("propose inbox", "app.agents.monitoring.inbox", required=False),
]


@dataclass
class Summary:
    started: str
    steps: dict[str, int] = field(default_factory=dict)
    findings: int | None = None
    proposals: dict[str, int] = field(default_factory=dict)
    drafts: list[str] = field(default_factory=list)
    drafts_directory: str | None = None
    # The local branch with the drafts (propose.py); never pushed.
    branch: str | None = None
    branch_error: str | None = None
    failed_step: str | None = None

    def line(self) -> str:
        if self.failed_step:
            return f"Step '{self.failed_step}' failed; see the log."
        if not self.proposals:
            return f"{self.findings or 0} new findings, no proposals this week."
        kinds = ", ".join(f"{count} {kind}" for kind, count in sorted(self.proposals.items()))
        where = f" on branch {self.branch}" if self.branch else ""
        return f"{self.findings} new findings; proposals: {kinds}; {len(self.drafts)} drafts to review{where}."


def run_module(step: Step, log: Callable[[str], None]) -> int:
    process = subprocess.Popen(
        [sys.executable, "-u", "-m", step.module, *step.args],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        # Feed titles contain emoji; the Windows default code page cannot print them.
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    assert process.stdout is not None
    for line in process.stdout:
        log(line.rstrip())
    return process.wait()


def latest(directory: Path, pattern: str, after: float) -> Path | None:
    """The newest file matching `pattern` written during this run."""
    files = [path for path in directory.glob(pattern) if path.stat().st_mtime >= after]
    return max(files, key=lambda path: path.stat().st_mtime, default=None)


def summarise(summary: Summary, started_at: float, runs: Path = RUNS_DIRECTORY, drafts: Path = DRAFTS_DIRECTORY) -> None:
    findings = latest(runs, "findings-*.jsonl", started_at)
    if findings:
        summary.findings = sum(1 for line in findings.read_text(encoding="utf-8").splitlines() if line.strip())
    report = latest(runs, "relevance-*.json", started_at)
    if report:
        for proposal in json.loads(report.read_text(encoding="utf-8")).get("proposals", []):
            summary.proposals[proposal["decision"]] = summary.proposals.get(proposal["decision"], 0) + 1
        directory = drafts / report.stem.replace("relevance-", "")
        if directory.is_dir():
            summary.drafts_directory = str(directory)
            summary.drafts = sorted(path.stem for path in directory.glob("*.md") if not path.stem.endswith(".review"))


def run(
    steps: list[Step] = STEPS,
    run_step: Callable[[Step, Callable[[str], None]], int] = run_module,
    log: Callable[[str], None] = lambda line: print(line, flush=True),
    now: Callable[[], datetime] = lambda: datetime.now().astimezone(),
    runs: Path = RUNS_DIRECTORY,
    drafts: Path = DRAFTS_DIRECTORY,
    propose: Callable[[Path, str], str | None] = create_proposal_branch,
) -> Summary:
    start = now()
    # Files written by the steps are recognised by their modification time.
    started_at = time.time() - 1
    summary = Summary(started=start.isoformat(timespec="seconds"))
    for step in steps:
        log(f"=== {step.name} ===")
        code = run_step(step, log)
        summary.steps[step.name] = code
        if code != 0:
            log(f"=== {step.name} exited with {code} ===")
            if step.required:
                summary.failed_step = step.name
                break
    summarise(summary, started_at, runs, drafts)
    if summary.drafts and summary.drafts_directory:
        directory = Path(summary.drafts_directory)
        try:
            summary.branch = propose(directory, directory.name)
            log(f"=== drafts on local branch {summary.branch} ===")
        except Exception as exc:  # the drafts stay in the drafts directory either way
            summary.branch_error = str(exc)
            log(f"=== could not create the proposal branch: {exc} ===")
    runs.mkdir(parents=True, exist_ok=True)
    (runs / f"weekly-{start:%Y-%m-%d_%H%M%S}.json").write_text(json.dumps(asdict(summary), indent=1), encoding="utf-8")
    return summary


def main() -> int:
    summary = run()
    print(f"SUMMARY: {summary.line()}", flush=True)
    return 1 if summary.failed_step else 0


if __name__ == "__main__":
    raise SystemExit(main())
