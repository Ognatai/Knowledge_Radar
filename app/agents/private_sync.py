"""Bring the private checkout up to date before the weekly run, then rebuild its structure.

Retros may be written on another machine (the ThinkPad). So that their knowledge gaps
reach this machine's weekly run, this step fast-forwards the private checkout's `main`
to GitLab's and rebuilds `graph/structure.yaml` (private_ingest, no language model),
which watchlist.py reads. It runs as its own process, outside the monitoring package:
the monitoring code still sees only the gap topic names.

The update never overwrites anything: only a fast-forward of a checkout that is on
`main`. A diverged branch, another branch or a conflict with uncommitted files leaves
the checkout as it is, and the structure is rebuilt from what is there.

    python -m app.agents.private_sync
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

from app.agents.private_ingest import ingest
from app.backend.knowledge_radar.config import LocalConfigError, load_local_config
from app.backend.knowledge_radar.graph import DEFAULT_GRAPH_DIRECTORY, load_graph
from app.backend.knowledge_radar.notes import configured_notes_directory, load_notes
from app.backend.knowledge_radar.private_git import PrivateGitError, PrivateRepo, gitlab_token
from app.backend.knowledge_radar.private_repo import PrivateRepoError


def fast_forward(repo: PrivateRepo, log: Callable[[str], None] = print) -> bool:
    """Fast-forward `main` to GitLab's `main`; False (and the reason logged) when not possible."""
    try:
        branch = repo.git("rev-parse", "--abbrev-ref", "HEAD")
        if branch != "main":
            log(f"Private checkout is on '{branch}', not main; left as it is.")
            return False
        before = repo.git("rev-parse", "HEAD")
        repo.fetch("+refs/heads/main:refs/remotes/origin/main")
        repo.git("merge", "--ff-only", "refs/remotes/origin/main")
        after = repo.git("rev-parse", "HEAD")
    except PrivateGitError as exc:
        log(f"Private checkout not updated: {exc}")
        return False
    log("Private checkout up to date." if before == after else f"Private checkout updated: {before[:7]}..{after[:7]}")
    return True


def main() -> int:
    try:
        config = load_local_config()
    except LocalConfigError as exc:
        print(exc, file=sys.stderr)
        return 1
    if not config.has_private_repo:
        print("No private_repo_path in local-config.yaml; nothing to update.")
        return 0
    root = Path(config.private_repo_path)
    fast_forward(PrivateRepo(root, gitlab_token()))
    notes_directory = configured_notes_directory()
    public = load_graph(DEFAULT_GRAPH_DIRECTORY, load_notes(notes_directory), notes_directory)
    try:
        graph, path = ingest(root, public.entities)
    except PrivateRepoError as exc:
        print(f"Structure not rebuilt: {exc}", file=sys.stderr)
        return 1
    print(f"Structure rebuilt: {len(graph.entities)} entities, {len(graph.open_gaps)} open gaps -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
