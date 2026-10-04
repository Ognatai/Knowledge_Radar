"""Untracked, per-machine configuration (see `local-config.example.yaml`).

The only setting so far is where the private repository is checked out. It must be
a sibling checkout: a private repo nested inside this public repo is rejected, so
public tooling can never pick up private files by walking this repository's tree.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml

from app.backend.knowledge_radar.notes import REPOSITORY_ROOT

DEFAULT_CONFIG_PATH = REPOSITORY_ROOT / "local-config.yaml"
CONFIG_PATH_ENVIRONMENT_VARIABLE = "KNOWLEDGE_RADAR_CONFIG"


class LocalConfigError(ValueError):
    """Raised when the local configuration file is malformed or points somewhere unsafe."""


@dataclass(frozen=True)
class LocalConfig:
    private_repo_path: Path | None = None

    @property
    def has_private_repo(self) -> bool:
        return self.private_repo_path is not None


def configured_config_path() -> Path:
    configured = os.environ.get(CONFIG_PATH_ENVIRONMENT_VARIABLE)
    return Path(configured).expanduser() if configured else DEFAULT_CONFIG_PATH


def load_local_config(
    config_path: Path | None = None,
    repository_root: Path = REPOSITORY_ROOT,
) -> LocalConfig:
    """Load the local config; a missing file means "public repo only"."""
    path = config_path or configured_config_path()
    if not path.is_file():
        return LocalConfig()

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise LocalConfigError(f"{path}: could not read local config: {exc}") from exc
    if not isinstance(raw, dict):
        raise LocalConfigError(f"{path}: local config must be a YAML mapping.")

    value = raw.get("private_repo_path")
    if value is None or (isinstance(value, str) and not value.strip()):
        return LocalConfig()
    if not isinstance(value, str):
        raise LocalConfigError(f"{path}: 'private_repo_path' must be a string.")

    private_repo = Path(value).expanduser()
    if not private_repo.is_absolute():
        raise LocalConfigError(f"{path}: 'private_repo_path' must be an absolute path.")
    private_repo = private_repo.resolve()
    if not private_repo.is_dir():
        raise LocalConfigError(f"{path}: private repo directory does not exist: {private_repo}")

    public_repo = repository_root.resolve()
    if private_repo == public_repo or private_repo.is_relative_to(public_repo):
        raise LocalConfigError(
            f"{path}: the private repo must be a sibling checkout, not inside {public_repo}."
        )
    if public_repo.is_relative_to(private_repo):
        raise LocalConfigError(f"{path}: the public repo must not live inside the private repo.")
    return LocalConfig(private_repo_path=private_repo)
