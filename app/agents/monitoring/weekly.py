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

The run is a LangGraph state graph: one node per step, a conditional edge after
each that ends the steps when a required one failed, then the summary, the
proposal branch (only with drafts) and the saved summary. `--diagram` prints it as
Mermaid (docs/weekly-run.md).

    python -m app.agents.monitoring.weekly
    python -m app.agents.monitoring.weekly --diagram
"""

from __future__ import annotations

import argparse
import json
import operator
import os
import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Annotated, Any, TypedDict

from langgraph.graph import END, START, StateGraph

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


class RunState(TypedDict):
    summary: Summary
    # Exit code per step; each step node adds its own.
    steps: Annotated[dict[str, int], operator.or_]


SUMMARISE, PROPOSE, SAVE = "summarise", "propose branch", "save summary"


def build_graph(
    steps: list[Step] = STEPS,
    run_step: Callable[[Step, Callable[[str], None]], int] = run_module,
    log: Callable[[str], None] = lambda line: print(line, flush=True),
    started_at: float = 0.0,
    runs: Path = RUNS_DIRECTORY,
    drafts: Path = DRAFTS_DIRECTORY,
    propose: Callable[[Path, str], str | None] = create_proposal_branch,
) -> Any:
    """The run as a compiled LangGraph graph over RunState."""
    graph = StateGraph(RunState)

    def step_node(step: Step) -> Callable[[RunState], dict[str, Any]]:
        def node(state: RunState) -> dict[str, Any]:
            log(f"=== {step.name} ===")
            code = run_step(step, log)
            if code != 0:
                log(f"=== {step.name} exited with {code} ===")
                if step.required:
                    state["summary"].failed_step = step.name
            return {"steps": {step.name: code}}
        return node

    def after(step: Step, following: str) -> Callable[[RunState], str]:
        return lambda state: SUMMARISE if state["summary"].failed_step == step.name else following

    def summarise_node(state: RunState) -> dict[str, Any]:
        summary = state["summary"]
        summary.steps = dict(state["steps"])
        summarise(summary, started_at, runs, drafts)
        return {"summary": summary}

    def propose_node(state: RunState) -> dict[str, Any]:
        summary = state["summary"]
        directory = Path(summary.drafts_directory or "")
        try:
            summary.branch = propose(directory, directory.name)
            log(f"=== drafts on local branch {summary.branch} ===")
        except Exception as exc:  # the drafts stay in the drafts directory either way
            summary.branch_error = str(exc)
            log(f"=== could not create the proposal branch: {exc} ===")
        return {"summary": summary}

    def save_node(state: RunState) -> dict[str, Any]:
        summary = state["summary"]
        start = datetime.fromisoformat(summary.started)
        runs.mkdir(parents=True, exist_ok=True)
        (runs / f"weekly-{start:%Y-%m-%d_%H%M%S}.json").write_text(json.dumps(asdict(summary), indent=1), encoding="utf-8")
        return {}

    names = [step.name for step in steps]
    for step in steps:
        graph.add_node(step.name, step_node(step))
    graph.add_node(SUMMARISE, summarise_node)
    graph.add_node(PROPOSE, propose_node)
    graph.add_node(SAVE, save_node)
    graph.add_edge(START, names[0] if names else SUMMARISE)
    for step, following in zip(steps, [*names[1:], SUMMARISE]):
        if step.required:
            graph.add_conditional_edges(step.name, after(step, following), [following, SUMMARISE] if following != SUMMARISE else [SUMMARISE])
        else:
            graph.add_edge(step.name, following)
    graph.add_conditional_edges(SUMMARISE, lambda state: PROPOSE if state["summary"].drafts and state["summary"].drafts_directory else SAVE,
                                [PROPOSE, SAVE])
    graph.add_edge(PROPOSE, SAVE)
    graph.add_edge(SAVE, END)
    return graph.compile()


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
    graph = build_graph(steps, run_step, log, started_at, runs, drafts, propose)
    summary = Summary(started=start.isoformat(timespec="seconds"))
    graph.invoke({"summary": summary, "steps": {}}, {"recursion_limit": len(steps) + 10})
    return summary


def diagram() -> str:
    """The graph as Mermaid, for the documentation; node ids without escaped spaces."""
    return build_graph(run_step=lambda step, log: 0).get_graph().draw_mermaid().replace("\\20", "_")


def main() -> int:
    parser = argparse.ArgumentParser(description="The weekly monitoring run.")
    parser.add_argument("--diagram", action="store_true", help="print the run's graph as Mermaid and exit")
    if parser.parse_args().diagram:
        print(diagram())
        return 0
    summary = run()
    print(f"SUMMARY: {summary.line()}", flush=True)
    return 1 if summary.failed_step else 0


if __name__ == "__main__":
    raise SystemExit(main())
