import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

# The checker is a standalone script (it runs before the package is installed).
SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_private_leaks.py"
spec = importlib.util.spec_from_file_location("check_private_leaks", SCRIPT)
leaks = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = leaks
spec.loader.exec_module(leaks)


def rules_hit(text, rules=None):
    return [finding.rule for finding in leaks.scan_line("f", 1, text, rules or leaks.BUILTIN_RULES)]


@pytest.mark.parametrize(
    "text",
    [
        r"see C:\Users\someone\notes.md",
        "path: D:/data/export.json",
        "open /Users/someone/project/file",
        'cp "/home/someone/x" .',
        "../knowledge-radar-private/applications/acme.md",
    ],
)
def test_builtin_rules_flag_out_of_repo_references(text):
    assert rules_hit(text)


@pytest.mark.parametrize(
    "text",
    [
        "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689",
        "https://github.com/home/users/example",
        "Ratio 3:1 and time 12:30",
        "the separate private repository",
        "${workspaceFolder}\\.venv\\Scripts\\python.exe",
    ],
)
def test_builtin_rules_ignore_ordinary_text(text):
    assert rules_hit(text) == []


def test_private_patterns_come_from_environment(monkeypatch):
    monkeypatch.setenv(leaks.PATTERNS_ENVIRONMENT_VARIABLE, "# comment\nacme corp\n\nretro:")
    monkeypatch.setattr(leaks, "LOCAL_PATTERNS_FILE", Path("does-not-exist"))

    rules = leaks.private_rules()

    assert [label for label, _ in rules] == ["private-data pattern #1", "private-data pattern #2"]
    assert rules_hit("Interview at ACME Corp", rules) == ["private-data pattern #1"]


def test_added_lines_tracks_paths_and_line_numbers():
    diff = (
        "diff --git a/x.md b/x.md\n"
        "--- a/x.md\n"
        "+++ b/x.md\n"
        "@@ -1,0 +2,2 @@\n"
        "+first\n"
        "+second\n"
        "diff --git a/gone.md b/gone.md\n"
        "--- a/gone.md\n"
        "+++ /dev/null\n"
        "@@ -1 +0,0 @@\n"
        "-removed\n"
    )

    assert list(leaks.added_lines(diff)) == [("x.md", 2, "first"), ("x.md", 3, "second")]


def test_symlinks_in_raw_diff():
    raw = ":000000 120000 0000000 abcdef1 A\0link\0:100644 100644 1111111 2222222 M\0file.md\0"

    assert leaks.symlinks_in_raw_diff(raw) == ["link"]


def test_staged_scan_end_to_end(tmp_path, monkeypatch):
    def run(*args):
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True)

    run("init", "-q")
    (tmp_path / "ok.md").write_text("harmless\n", encoding="utf-8")
    (tmp_path / "bad.md").write_text("one\nsee C:\\Users\\me\\secret.txt\n", encoding="utf-8")
    run("add", "ok.md", "bad.md")
    monkeypatch.setattr(leaks, "REPOSITORY_ROOT", tmp_path)

    findings = leaks.scan_diff(["--cached"], leaks.BUILTIN_RULES)

    assert [str(finding) for finding in findings] == ["bad.md:2: absolute Windows path"]
