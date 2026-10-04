import pytest

from app.backend.knowledge_radar.config import LocalConfigError, load_local_config


def write_config(path, private_repo_path):
    path.write_text(f"private_repo_path: '{private_repo_path}'\n", encoding="utf-8")
    return path


def test_missing_config_means_public_only(tmp_path):
    config = load_local_config(tmp_path / "local-config.yaml", repository_root=tmp_path)

    assert not config.has_private_repo


def test_empty_private_repo_path_means_public_only(tmp_path):
    path = tmp_path / "local-config.yaml"
    path.write_text("private_repo_path:\n", encoding="utf-8")

    assert load_local_config(path, repository_root=tmp_path).private_repo_path is None


def test_accepts_sibling_checkout(tmp_path):
    public_repo = tmp_path / "knowledge-radar"
    private_repo = tmp_path / "private"
    public_repo.mkdir()
    private_repo.mkdir()
    path = write_config(public_repo / "local-config.yaml", private_repo)

    config = load_local_config(path, repository_root=public_repo)

    assert config.private_repo_path == private_repo.resolve()


def test_rejects_private_repo_nested_in_public_repo(tmp_path):
    nested = tmp_path / "private"
    nested.mkdir()
    path = write_config(tmp_path / "local-config.yaml", nested)

    with pytest.raises(LocalConfigError, match="sibling checkout"):
        load_local_config(path, repository_root=tmp_path)


def test_rejects_public_repo_nested_in_private_repo(tmp_path):
    public_repo = tmp_path / "knowledge-radar"
    public_repo.mkdir()
    path = write_config(public_repo / "local-config.yaml", tmp_path)

    with pytest.raises(LocalConfigError, match="must not live inside the private repo"):
        load_local_config(path, repository_root=public_repo)


@pytest.mark.parametrize("value", ["relative/path", "/does/not/exist/anywhere"])
def test_rejects_relative_or_missing_paths(tmp_path, value):
    path = write_config(tmp_path / "local-config.yaml", value)

    with pytest.raises(LocalConfigError):
        load_local_config(path, repository_root=tmp_path / "repo")
