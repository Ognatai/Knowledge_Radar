"""Put a weekly run's drafts on a local branch, for the review.

The branch `proposals/<run>` starts from what is published (`origin/main`) and holds what the run proposes: each
draft at the place it would take (`public/notes/<slug>.md`), so that
`git diff main proposals/<run>` shows exactly the proposal, plus an overview and the
curator's review reports under `proposals/<run>/`. The review then compares this branch
with the notes Claude writes from it; the drafts themselves are not published as they
are.

The branch is built with git plumbing (`hash-object`, a temporary index, `commit-tree`,
`update-ref`): the run starts at night and must not touch the working tree, the checked
out branch or the index, whatever is open there. It is never pushed: on GitHub, a branch
of the public repository would make unreviewed drafts public (decided 2026-10-11).
"""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path

from app.backend.knowledge_radar.notes import REPOSITORY_ROOT

BRANCH_PREFIX = "proposals/"
Git = Callable[..., str]


def git(*args: str, repo: Path = REPOSITORY_ROOT, stdin: bytes | None = None, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, input=stdin, capture_output=True, check=True,
        env={**os.environ, **(env or {})},
    )
    return result.stdout.decode("utf-8").strip()


def _review_line(review: str) -> str:
    """The review report's verdicts in one line: template, originality, faithfulness."""
    parts = []
    template = re.search(r"## Template\n- (.+)", review)
    if template:
        parts.append(f"template: {template.group(1)}")
    for heading in ("Originality", "Faithfulness"):
        match = re.search(rf"## {heading}: (.+)", review)
        if match:
            parts.append(f"{heading.lower()}: {match.group(1)}")
    return "; ".join(parts)


def overview(run: str, drafts: Path) -> str:
    lines = [f"# Proposals of the weekly run {run}", "", "Drafts of the local model, not reviewed. Each needs Claude's review against the sources before anything is published.", ""]
    for draft in sorted(drafts.glob("*.md")):
        if draft.name.endswith(".review.md"):
            continue
        review_path = draft.with_name(f"{draft.stem}.review.md")
        review = review_path.read_text(encoding="utf-8") if review_path.is_file() else ""
        kind = re.search(r"^# Review: \S+ \((\w+)\)", review, re.MULTILINE)
        lines.append(f"- **{draft.stem}** ({kind.group(1) if kind else 'draft'}): {_review_line(review)}")
    return "\n".join(lines) + "\n"


def base_commit(repo: Path, run_git: Git = git) -> str:
    """What is published: origin/main (updated by every push), else the local main, which
    lags behind when changes are pushed from another branch."""
    for ref in ("origin/main", "main"):
        try:
            return run_git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}", repo=repo)
        except subprocess.CalledProcessError:
            continue
    raise RuntimeError("Neither origin/main nor main exists.")


def create_proposal_branch(drafts: Path, run: str, *, base: str | None = None, repo: Path = REPOSITORY_ROOT, run_git: Git = git) -> str | None:
    """The branch name, or None when the run has no drafts. Touches no working tree."""
    files: dict[str, bytes] = {}
    for draft in sorted(drafts.glob("*.md")):
        if draft.name.endswith(".review.md"):
            files[f"proposals/{run}/{draft.name}"] = draft.read_bytes()
        else:
            files[f"public/notes/{draft.name}"] = draft.read_bytes()
    if not any(path.startswith("public/notes/") for path in files):
        return None
    files[f"proposals/{run}/README.md"] = overview(run, drafts).encode("utf-8")

    branch = f"{BRANCH_PREFIX}{run}"
    start = run_git("rev-parse", "--verify", f"{base}^{{commit}}", repo=repo) if base else base_commit(repo, run_git)
    with tempfile.TemporaryDirectory() as temporary:
        index = {"GIT_INDEX_FILE": str(Path(temporary) / "index")}
        run_git("read-tree", start, repo=repo, env=index)
        for path, content in files.items():
            blob = run_git("hash-object", "-w", "--stdin", repo=repo, stdin=content)
            run_git("update-index", "--add", "--cacheinfo", f"100644,{blob},{path}", repo=repo, env=index)
        tree = run_git("write-tree", repo=repo, env=index)
    message = f"Proposals of the weekly run {run}\n\nDrafts of the local model, not reviewed; see proposals/{run}/README.md."
    commit = run_git("commit-tree", tree, "-p", start, "-m", message, repo=repo)
    run_git("update-ref", f"refs/heads/{branch}", commit, repo=repo)
    return branch
