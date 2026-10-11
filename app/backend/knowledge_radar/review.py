"""The Review Dashboard: what the weekly run proposed, and the decisions on it.

Public proposals are the local branches `proposals/<run>` on the Desktop (propose.py),
never pushed. The dashboard shows each run's drafts with their diff and the curator's
review report, and records a decision per draft: "wanted" (to be published after
Claude's review against the sources, which no button replaces) or "discarded". A
discarded promotion counts as declined, so that the relevance agent does not propose it
again until more notes discuss the entity. Removing a run deletes its branch. Decided
2026-10-11.

Private proposals are the branches `inbox/<run>` in the private GitLab repository
(inbox.py): gap news for interview preparation, nothing that gets published. Accepting
merges a branch into main (pushed to GitLab) and puts its notes into the private
checkout without touching anything else there; discarding deletes the branch.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from app.backend.knowledge_radar.private_git import PrivateGitError, PrivateRepo

PROPOSALS_PREFIX = "refs/heads/proposals/"
INBOX_PREFIX = "inbox/"
STATUSES = ("open", "wanted", "discarded")
RUN_NAME = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{6}$")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ReviewError(ValueError):
    """A request the dashboard cannot carry out (unknown run, untidy checkout …)."""


@dataclass
class DraftSummary:
    slug: str
    kind: str  # promotion, update, new_topic or draft
    new_note: bool
    verdicts: str
    status: str = "open"


@dataclass
class ProposalRun:
    run: str
    branch: str
    created: str
    drafts: list[DraftSummary] = field(default_factory=list)


def _review_kind(review: str) -> str:
    match = re.search(r"^# Review: \S+ \((\w+)\)", review, re.MULTILINE)
    return match.group(1) if match else "draft"


def _verdicts(review: str) -> str:
    parts = []
    template = re.search(r"## Template\n- (.+)", review)
    if template:
        parts.append(f"template: {template.group(1)}")
    for heading in ("Originality", "Faithfulness"):
        match = re.search(rf"## {heading}: (.+)", review)
        if match:
            parts.append(f"{heading.lower()}: {match.group(1)}")
    return "; ".join(parts)


class PublicProposals:
    def __init__(self, git_dir: Path, decisions_path: Path, declined_path: Path,
                 discussing_notes: Callable[[str], int] | None = None, today: Callable[[], dt.date] = dt.date.today) -> None:
        self.git_dir = git_dir
        self.decisions_path = decisions_path
        self.declined_path = declined_path
        self.discussing_notes = discussing_notes
        self.today = today

    def git(self, *args: str) -> str:
        result = subprocess.run(["git", f"--git-dir={self.git_dir}", *args], capture_output=True,
                                env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
        if result.returncode != 0:
            raise ReviewError(f"git {args[0]} failed: {result.stderr.decode('utf-8', 'replace').strip()}")
        # Drafts written on Windows carry CRLF line ends.
        return result.stdout.decode("utf-8", "replace").replace("\r\n", "\n")

    def _decisions(self) -> dict[str, dict[str, Any]]:
        if not self.decisions_path.is_file():
            return {}
        return json.loads(self.decisions_path.read_text(encoding="utf-8"))

    def _save_decisions(self, decisions: dict[str, dict[str, Any]]) -> None:
        self.decisions_path.parent.mkdir(parents=True, exist_ok=True)
        self.decisions_path.write_text(json.dumps(decisions, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")

    def _branch(self, run: str) -> str:
        if not RUN_NAME.match(run):
            raise ReviewError(f"Not a run name: {run!r}.")
        branch = f"proposals/{run}"
        try:
            self.git("rev-parse", "--verify", "--quiet", f"refs/heads/{branch}^{{commit}}")
        except ReviewError as exc:
            raise ReviewError(f"No proposal branch {branch}.") from exc
        return branch

    def available(self) -> bool:
        return (self.git_dir / "HEAD").is_file()

    def runs(self) -> list[ProposalRun]:
        if not self.available():
            return []
        listed = self.git("for-each-ref", "--sort=-committerdate", "--format=%(refname)%09%(committerdate:short)", PROPOSALS_PREFIX)
        decisions = self._decisions()
        runs = []
        for line in listed.splitlines():
            ref, created = line.split("\t")
            run = ref.removeprefix(PROPOSALS_PREFIX)
            branch = f"proposals/{run}"
            changed = self.git("diff", "--name-status", f"{branch}^", branch, "--", "public/notes").splitlines()
            drafts = []
            for entry in changed:
                status, path = entry.split("\t")[0], entry.split("\t")[-1]
                slug = Path(path).stem
                review = self._show(branch, f"proposals/{run}/{slug}.review.md")
                drafts.append(DraftSummary(slug, _review_kind(review), status.startswith("A"), _verdicts(review),
                                           decisions.get(run, {}).get(slug, {}).get("status", "open")))
            runs.append(ProposalRun(run, branch, created, drafts))
        return runs

    def _show(self, branch: str, path: str) -> str:
        try:
            return self.git("show", f"{branch}:{path}")
        except ReviewError:
            return ""

    def detail(self, run: str, slug: str) -> dict[str, str]:
        branch = self._branch(run)
        if not SLUG.match(slug):
            raise ReviewError(f"Not a note slug: {slug!r}.")
        return {
            "review": self._show(branch, f"proposals/{run}/{slug}.review.md"),
            "diff": self.git("diff", f"{branch}^", branch, "--", f"public/notes/{slug}.md"),
            "draft": self._show(branch, f"public/notes/{slug}.md"),
        }

    def decide(self, run: str, slug: str, status: str) -> None:
        if status not in STATUSES:
            raise ReviewError(f"Unknown decision {status!r}.")
        drafts = {d.slug: d for r in self.runs() if r.run == run for d in r.drafts}
        if slug not in drafts:
            raise ReviewError(f"No draft {slug} in run {run}.")
        decisions = self._decisions()
        decisions.setdefault(run, {})[slug] = {"status": status, "decided": self.today().isoformat()}
        self._save_decisions(decisions)
        if status == "discarded" and drafts[slug].kind == "promotion":
            self._decline(slug)

    def _decline(self, slug: str) -> None:
        """The relevance agent proposes a declined promotion again only when more notes discuss it."""
        declined = json.loads(self.declined_path.read_text(encoding="utf-8")) if self.declined_path.is_file() else {}
        declined[slug] = {
            "discussing_notes": self.discussing_notes(slug) if self.discussing_notes else 0,
            "discarded_in_review": True,
            "checked": self.today().isoformat(),
        }
        self.declined_path.parent.mkdir(parents=True, exist_ok=True)
        self.declined_path.write_text(json.dumps(declined, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")

    def remove(self, run: str) -> None:
        branch = self._branch(run)
        self.git("update-ref", "-d", f"refs/heads/{branch}")
        decisions = self._decisions()
        if run in decisions:
            decisions[run]["_removed"] = {"status": "removed", "decided": self.today().isoformat()}
            self._save_decisions(decisions)


@dataclass
class InboxFile:
    path: str
    title: str
    text: str


@dataclass
class InboxBranch:
    branch: str
    files: list[InboxFile]


class PrivateInbox:
    def __init__(self, repo: PrivateRepo) -> None:
        self.repo = repo

    def _tracking(self, branch: str) -> str:
        if not branch.startswith(INBOX_PREFIX) or not RUN_NAME.match(branch.removeprefix(INBOX_PREFIX)):
            raise ReviewError(f"Not an inbox branch: {branch!r}.")
        return f"refs/remotes/origin/{branch}"

    def refresh(self) -> None:
        self.repo.fetch("+refs/heads/main:refs/remotes/origin/main", "+refs/heads/inbox/*:refs/remotes/origin/inbox/*")

    def _added(self, tracking: str) -> dict[str, str]:
        base = self.repo.git("merge-base", "refs/remotes/origin/main", tracking)
        listed = self.repo.git("diff", "--name-status", "--no-renames", base, tracking)
        added = {}
        for line in listed.splitlines():
            status, path = line.split("\t", 1)
            if status != "A" or not path.startswith("notes/") or not path.endswith(".md"):
                raise ReviewError(f"{tracking}: an inbox branch may only add notes; it changes {path} ({status}).")
            added[path] = self.repo.git("show", f"{tracking}:{path}")
        return added

    def branches(self, fetch: bool = True) -> list[InboxBranch]:
        if fetch:
            self.refresh()
        refs = self.repo.git("for-each-ref", "--format=%(refname)", "refs/remotes/origin/inbox/").splitlines()
        found = []
        for ref in sorted(refs, reverse=True):
            branch = ref.removeprefix("refs/remotes/origin/")
            files = []
            for path, text in self._added(ref).items():
                title = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
                files.append(InboxFile(path, title.group(1).strip().strip("'\"") if title else path, text))
            found.append(InboxBranch(branch, files))
        return found

    def accept(self, branch: str) -> list[str]:
        """Merge into main, push, and put the notes into the checkout; returns their paths."""
        tracking = self._tracking(branch)
        self.refresh()
        tip = self.repo.git("rev-parse", "--verify", f"{tracking}^{{commit}}")
        if self.repo.git("symbolic-ref", "HEAD") != "refs/heads/main":
            raise ReviewError("The private checkout is not on main; switch to main first.")
        main = self.repo.git("rev-parse", "--verify", "refs/heads/main^{commit}")
        try:
            self.repo.git("merge-base", "--is-ancestor", "refs/remotes/origin/main", main)
        except PrivateGitError as exc:
            raise ReviewError("GitLab's main has commits the private checkout lacks; run git pull there first.") from exc
        added = self._added(tracking)
        root = self.repo.root
        for path in added:
            tracked = self.repo.git("ls-files", "--", path)
            if tracked or (root / path).exists():
                raise ReviewError(f"{path} exists already in the private checkout.")
        commit = self.repo.commit_files(main, {path: text.encode("utf-8") + b"\n" for path, text in added.items()},
                                        f"Accept {branch}\n\nGap news accepted in the Review Dashboard.", parents=[main, tip])
        self.repo.push(f"{commit}:refs/heads/main")
        self.repo.git("update-ref", "refs/heads/main", commit, main)
        self.repo.git("update-ref", "refs/remotes/origin/main", commit)
        # Only the accepted notes enter the user's index and working tree.
        for path, text in added.items():
            blob = self.repo.git("rev-parse", f"{commit}:{path}")
            self.repo.git("update-index", "--add", "--cacheinfo", f"100644,{blob},{path}")
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text + "\n", encoding="utf-8")
        self._delete(branch, tracking)
        return sorted(added)

    def discard(self, branch: str) -> None:
        tracking = self._tracking(branch)
        self._delete(branch, tracking)

    def _delete(self, branch: str, tracking: str) -> None:
        self.repo.push(f":refs/heads/{branch}")
        self.repo.git("update-ref", "-d", tracking)


def as_dict(items: list[Any]) -> list[dict[str, Any]]:
    return [asdict(item) for item in items]
