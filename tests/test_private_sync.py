"""The weekly run's private update: only a fast-forward of main, never an overwrite."""

import subprocess

import pytest

from app.agents.private_sync import fast_forward
from app.backend.knowledge_radar.private_git import PrivateRepo


def git(directory, *args):
    return subprocess.run(["git", "-C", str(directory), *args], check=True, capture_output=True, text=True).stdout.strip()


def commit(directory, name, text):
    (directory / name).write_text(text, encoding="utf-8")
    git(directory, "add", name)
    git(directory, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", name)


@pytest.fixture
def repos(tmp_path):
    """A GitLab stand-in (another clone pushes to it) and this machine's checkout."""
    remote, other, local = tmp_path / "remote.git", tmp_path / "other", tmp_path / "local"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
    subprocess.run(["git", "clone", "-q", str(remote), str(other)], check=True, capture_output=True)
    git(other, "checkout", "-q", "-b", "main")
    commit(other, "README.md", "data\n")
    git(other, "push", "-q", "origin", "main")
    subprocess.run(["git", "clone", "-q", str(remote), str(local)], check=True)
    commit(other, "retro.md", "gap\n")
    git(other, "push", "-q", "origin", "main")
    return other, local


def test_main_is_fast_forwarded_to_the_remote(repos):
    other, local = repos
    lines = []
    assert fast_forward(PrivateRepo(local), lines.append)
    assert (local / "retro.md").is_file()
    assert git(local, "rev-parse", "HEAD") == git(other, "rev-parse", "HEAD")
    assert lines[-1].startswith("Private checkout updated")


def test_uncommitted_files_stay_and_a_diverged_main_is_left_alone(repos):
    other, local = repos
    (local / "draft.md").write_text("mine\n", encoding="utf-8")
    commit(local, "local.md", "only here\n")
    head = git(local, "rev-parse", "HEAD")
    lines = []
    assert not fast_forward(PrivateRepo(local), lines.append)
    assert git(local, "rev-parse", "HEAD") == head
    assert (local / "draft.md").read_text(encoding="utf-8") == "mine\n"
    assert "not updated" in lines[-1]


def test_another_branch_is_left_alone(repos):
    _, local = repos
    git(local, "checkout", "-q", "-b", "work")
    lines = []
    assert not fast_forward(PrivateRepo(local), lines.append)
    assert "'work'" in lines[-1]
