"""Interview-relevant findings into the private repository, as a GitLab branch to review.

What counts as interview-relevant follows from the index separation: the monitoring
pipeline knows nothing private except the topic names of knowledge gaps from interview
retros (watchlist.py). A finding is interview-relevant when one of those gap topics
found it (its search phrase) or names it in its title or summary. For each gap topic
with new findings, the run proposes one private note, "New on your gap: <topic>", with
the findings as a reading list.

The proposal is a branch `inbox/<run>` in the private GitLab repository, built from
GitLab's main without touching the Desktop's private checkout, and pushed (GitLab is
private, unlike the public repository's proposal branches). The Review Dashboard on the
ThinkPad accepts it, which merges the notes into main, or discards it. Accepted notes
land in `notes/`, where the chat finds them.

    python -m app.agents.monitoring.inbox                       # latest findings run
    python -m app.agents.monitoring.inbox --run <findings.jsonl> --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

from app.agents.monitoring.findings import RUNS_DIRECTORY, Finding
from app.backend.knowledge_radar.private_git import PrivateGitError, PrivateRepo, gitlab_token
from app.backend.knowledge_radar.private_repo import slugify

BRANCH_PREFIX = "inbox/"
MAX_FINDINGS_PER_TOPIC = 5
MAX_SUMMARY_CHARACTERS = 400


def _mentions(finding: Finding, topic: str) -> bool:
    pattern = rf"(?<!\w){re.escape(topic.casefold())}(?!\w)"
    return re.search(pattern, f"{finding.title} {finding.summary}".casefold()) is not None


def gap_findings(findings: list[Finding], topics: list[str], limit: int = MAX_FINDINGS_PER_TOPIC) -> dict[str, list[Finding]]:
    """Per gap topic, the findings it found or that name it; peer-reviewed and recent first."""
    grouped: dict[str, list[Finding]] = {}
    for topic in topics:
        matching = [f for f in findings if (f.query or "").casefold() == topic.casefold() or _mentions(f, topic)]
        matching.sort(key=lambda f: (f.tier != "peer_reviewed", -(f.published or date.min).toordinal()))
        if matching:
            grouped[topic] = matching[:limit]
    return grouped


def note_path(run: str, topic: str) -> str:
    return f"notes/gap-news-{run[:10]}-{slugify(topic)}.md"


def gap_note(topic: str, findings: list[Finding], run: str) -> str:
    frontmatter = {"title": f"New on your gap: {topic} ({run[:10]})", "gap_topic": topic, "weekly_run": run}
    lines = ["---", yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True, width=1000).strip(), "---",
             f"New findings of the weekly monitoring on **{topic}**, a gap from an interview retro. "
             "Not reviewed: titles and summaries as the sources publish them.", ""]
    for finding in findings:
        details = ", ".join(part for part in (finding.source, finding.published.isoformat() if finding.published else "",
                                              "peer-reviewed" if finding.tier == "peer_reviewed" else "") if part)
        summary = " ".join(finding.summary.split())
        if len(summary) > MAX_SUMMARY_CHARACTERS:
            summary = summary[: MAX_SUMMARY_CHARACTERS - 2].rsplit(" ", 1)[0] + " …"
        lines += [f"## [{finding.title}]({finding.url})", f"_{details}_", "", summary, ""]
    return "\n".join(lines).rstrip() + "\n"


def propose_inbox(repo: PrivateRepo, run: str, files: dict[str, str]) -> str | None:
    """Push the notes as branch inbox/<run>, based on GitLab's main; None without notes."""
    if not files:
        return None
    repo.fetch("+refs/heads/main:refs/remotes/origin/main")
    base = repo.git("rev-parse", "--verify", "refs/remotes/origin/main^{commit}")
    message = f"Gap news of the weekly run {run}\n\nNot reviewed; accept or discard in the Review Dashboard."
    commit = repo.commit_files(base, {path: text.encode("utf-8") for path, text in files.items()}, message)
    branch = f"{BRANCH_PREFIX}{run}"
    repo.push(f"{commit}:refs/heads/{branch}")
    return branch


def latest_run(directory: Path = RUNS_DIRECTORY) -> Path | None:
    runs = sorted(directory.glob("findings-*.jsonl"))
    return runs[-1] if runs else None


def main() -> int:
    from app.agents.monitoring.relevance import finding_from_json
    from app.agents.monitoring.run_sources import local_config, public_entities
    from app.backend.knowledge_radar.watchlist import gap_topics

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--run", type=Path, help="findings file (default: the latest run)")
    parser.add_argument("--dry-run", action="store_true", help="print the notes; push nothing")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    private_root = local_config().private_repo_path
    if private_root is None:
        print("No private repository configured; no inbox.")
        return 0
    topics = gap_topics(private_root, public_entities())
    run_path = args.run or latest_run()
    if not topics or run_path is None:
        print("No gap topics from interview retros or no findings run; no inbox.")
        return 0
    run = run_path.stem.replace("findings-", "")
    findings = [finding_from_json(json.loads(line)) for line in run_path.read_text(encoding="utf-8").splitlines() if line]
    grouped = gap_findings(findings, topics)
    files = {note_path(run, topic): gap_note(topic, found, run) for topic, found in grouped.items()}
    for topic, found in grouped.items():
        print(f"{topic}: {len(found)} findings")
    if args.dry_run:
        for path, text in files.items():
            print(f"--- {path}\n{text}")
        return 0
    try:
        branch = propose_inbox(PrivateRepo(private_root, gitlab_token()), run, files)
    except PrivateGitError as exc:
        print(f"Could not push the inbox branch: {exc}", file=sys.stderr)
        return 1
    print(f"INBOX: {branch or 'nothing to propose'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
