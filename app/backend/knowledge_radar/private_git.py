"""Git on the private checkout, with the GitLab token for fetch and push.

The weekly run (Desktop) pushes inbox branches and the Review Dashboard (ThinkPad, in
Docker, without SSH keys) merges or deletes them, so both reach GitLab over HTTPS with
a project access token from the Windows Credential Manager (`knowledge-radar` /
`gitlab`; the start script passes it to the container as GITLAB_TOKEN). The token goes
to git as an HTTP header through GIT_CONFIG_* environment variables, never on the
command line or into a file. Without a token, the checkout's own remote is used (SSH on
the Desktop).

Local work never touches the working tree or the index beyond the files a merge adds:
the user may have uncommitted files from /retro or /prep in the same checkout.
"""

from __future__ import annotations

import base64
import os
import re
import subprocess
from pathlib import Path

KEYRING_SERVICE = "knowledge-radar"
KEYRING_USER = "gitlab"
SSH_REMOTE = re.compile(r"^(?:ssh://)?git@([^:/]+)[:/](.+?)(?:\.git)?$")


class PrivateGitError(RuntimeError):
    """A git operation on the private checkout failed; the message says which and why."""


def gitlab_token() -> str | None:
    token = os.environ.get("GITLAB_TOKEN")
    if token:
        return token
    try:
        import keyring

        return keyring.get_password(KEYRING_SERVICE, KEYRING_USER)
    except Exception:  # noqa: BLE001 - no keyring backend (e.g. in the container): no token
        return None


def https_url(remote: str) -> str:
    """git@gitlab.com:user/repo.git -> https://gitlab.com/user/repo.git"""
    match = SSH_REMOTE.match(remote.strip())
    if match:
        return f"https://{match.group(1)}/{match.group(2)}.git"
    return remote.strip()


class PrivateRepo:
    def __init__(self, root: Path, token: str | None = None) -> None:
        self.root = root
        self.token = token

    def git(self, *args: str, stdin: bytes | None = None, env: dict[str, str] | None = None, network: bool = False) -> str:
        environment = {**os.environ, **(env or {}), "GIT_TERMINAL_PROMPT": "0"}
        if network and self.token:
            header = base64.b64encode(f"oauth2:{self.token}".encode()).decode()
            environment.update({"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "http.extraHeader",
                                "GIT_CONFIG_VALUE_0": f"Authorization: Basic {header}"})
        result = subprocess.run(["git", "-C", str(self.root), *args], input=stdin, capture_output=True, env=environment)
        if result.returncode != 0:
            message = result.stderr.decode("utf-8", "replace").strip()
            if self.token:
                message = message.replace(self.token, "***")
            raise PrivateGitError(f"git {args[0]} failed: {message}")
        return result.stdout.decode("utf-8").strip()

    def remote(self) -> str:
        """Where to fetch from and push to: HTTPS with the token, else the checkout's origin."""
        return https_url(self.git("remote", "get-url", "origin")) if self.token else "origin"

    def fetch(self, *refspecs: str) -> None:
        self.git("fetch", "--prune", self.remote(), *refspecs, network=True)

    def push(self, *refspecs: str) -> None:
        self.git("push", self.remote(), *refspecs, network=True)

    def commit_files(self, base: str, files: dict[str, bytes], message: str, parents: list[str] | None = None) -> str:
        """A commit of `base`'s tree plus `files`, built in a temporary index (no working tree)."""
        import tempfile

        with tempfile.TemporaryDirectory() as temporary:
            index = {"GIT_INDEX_FILE": str(Path(temporary) / "index")}
            self.git("read-tree", base, env=index)
            for path, content in files.items():
                blob = self.git("hash-object", "-w", "--stdin", stdin=content)
                self.git("update-index", "--add", "--cacheinfo", f"100644,{blob},{path}", env=index)
            tree = self.git("write-tree", env=index)
        parent_args = [arg for parent in (parents or [base]) for arg in ("-p", parent)]
        return self.git("commit-tree", tree, *parent_args, "-m", message,
                        env={"GIT_AUTHOR_NAME": "Knowledge Radar", "GIT_AUTHOR_EMAIL": "knowledge-radar@localhost",
                             "GIT_COMMITTER_NAME": "Knowledge Radar", "GIT_COMMITTER_EMAIL": "knowledge-radar@localhost"})
