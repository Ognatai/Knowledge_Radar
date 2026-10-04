"""Fail if added content references anything outside this public repository.

Used by the pre-commit hook (`--staged`) and by GitHub Actions (`--range` / `--all`).
It checks for:

* absolute local paths (Windows drives, /Users/..., /home/...) and paths into the
  private repository checkout,
* symlinks (which could point outside this repository),
* private-data patterns (company names, interview-retro markers, ...). These are
  never stored in this public repo; they come from the environment variable
  KNOWLEDGE_RADAR_PRIVATE_PATTERNS (a GitHub Actions secret in CI) and/or the
  untracked file `.knowledge-radar/private-patterns.txt` (one regex per line).

Findings report file, line, and rule only, never the matched text, so CI logs
do not repeat a leaked value.

Standard library only, so the hook works before the package is installed.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LOCAL_PATTERNS_FILE = REPOSITORY_ROOT / ".knowledge-radar" / "private-patterns.txt"
PATTERNS_ENVIRONMENT_VARIABLE = "KNOWLEDGE_RADAR_PRIVATE_PATTERNS"
SYMLINK_MODE = "120000"

BUILTIN_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("absolute Windows path", re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/](?=[^\\/\s])")),
    ("absolute home-directory path", re.compile(r"(?<![\w.\-/:~])(?:/Users|/home)/[^/\s]+/")),
    ("path into the private repository", re.compile(r"knowledge[-_]radar[-_]private[\\/]", re.I)),
]

# The checker and its tests necessarily contain the patterns they look for.
EXCLUDED_PATHS = {
    "scripts/check_private_leaks.py",
    "tests/test_check_private_leaks.py",
}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int | None
    rule: str

    def __str__(self) -> str:
        location = f"{self.path}:{self.line}" if self.line is not None else self.path
        return f"{location}: {self.rule}"


def private_rules(patterns_file: Path | None = None) -> list[tuple[str, re.Pattern[str]]]:
    raw_patterns = os.environ.get(PATTERNS_ENVIRONMENT_VARIABLE, "").splitlines()
    for file in (LOCAL_PATTERNS_FILE, patterns_file):
        if file is not None and file.is_file():
            raw_patterns += file.read_text(encoding="utf-8").splitlines()

    rules: list[tuple[str, re.Pattern[str]]] = []
    for raw in raw_patterns:
        pattern = raw.strip()
        if not pattern or pattern.startswith("#"):
            continue
        try:
            compiled = re.compile(pattern, re.IGNORECASE)
        except re.error as exc:
            raise SystemExit(f"Invalid private-data pattern #{len(rules) + 1}: {exc}") from exc
        rules.append((f"private-data pattern #{len(rules) + 1}", compiled))
    return rules


def scan_line(path: str, line_number: int | None, text: str, rules) -> list[Finding]:
    return [Finding(path, line_number, label) for label, pattern in rules if pattern.search(text)]


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-c", "core.quotepath=off", *args],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise SystemExit(f"git {' '.join(args)} failed: {message}")
    return result.stdout.decode("utf-8", errors="replace")


HUNK_HEADER = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def added_lines(diff: str):
    """Yield (path, line_number, text) for every added line in a unified diff."""
    path: str | None = None
    line_number = 0
    previous = ""
    for line in diff.splitlines():
        is_file_header = line.startswith("+++ ") and previous.startswith("--- ")
        previous = line
        if is_file_header:
            target = line[4:]
            path = target[2:] if target.startswith("b/") else None
        elif line.startswith("@@"):
            match = HUNK_HEADER.match(line)
            line_number = int(match.group(1)) if match else 0
        elif line.startswith("+") and path is not None:
            yield path, line_number, line[1:]
            line_number += 1
        elif not line.startswith("-") and not line.startswith("\\"):
            line_number += 1


def symlinks_in_raw_diff(raw: str) -> list[str]:
    """Return paths whose new mode is a symlink, from `git diff --raw -z` output."""
    entries = raw.split("\0")
    paths: list[str] = []
    index = 0
    while index < len(entries):
        header = entries[index]
        if not header.startswith(":"):
            index += 1
            continue
        fields = header[1:].split()
        status = fields[4] if len(fields) > 4 else ""
        path_count = 2 if status[:1] in {"R", "C"} else 1
        new_path = entries[index + path_count] if index + path_count < len(entries) else ""
        if len(fields) > 1 and fields[1] == SYMLINK_MODE:
            paths.append(new_path)
        index += path_count + 1
    return paths


def scan_diff(diff_args: list[str], rules) -> list[Finding]:
    findings = [
        Finding(path, None, "symlink (could point outside the repository)")
        for path in symlinks_in_raw_diff(git("diff", "--raw", "-z", "--no-renames", *diff_args))
        if path not in EXCLUDED_PATHS
    ]
    diff = git("diff", "-U0", "--no-color", "--no-ext-diff", "--no-renames", *diff_args)
    for path, line_number, text in added_lines(diff):
        if path not in EXCLUDED_PATHS:
            findings += scan_line(path, line_number, text, rules)
    return findings


def scan_tracked_files(rules) -> list[Finding]:
    findings: list[Finding] = []
    for entry in git("ls-files", "-s", "-z").split("\0"):
        if not entry:
            continue
        meta, path = entry.split("\t", 1)
        if path in EXCLUDED_PATHS:
            continue
        if meta.split()[0] == SYMLINK_MODE:
            findings.append(Finding(path, None, "symlink (could point outside the repository)"))
            continue
        try:
            content = (REPOSITORY_ROOT / path).read_bytes()
        except OSError:
            continue
        if b"\0" in content[:8000]:
            continue  # binary
        for line_number, text in enumerate(content.decode("utf-8", "replace").splitlines(), 1):
            findings += scan_line(path, line_number, text, rules)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--staged", action="store_true", help="scan staged changes")
    mode.add_argument("--range", metavar="BASE..HEAD", help="scan a commit range")
    mode.add_argument("--all", action="store_true", help="scan all tracked files")
    parser.add_argument("--patterns-file", type=Path, help="extra private-data patterns")
    args = parser.parse_args()

    rules = BUILTIN_RULES + private_rules(args.patterns_file)
    if args.staged:
        findings = scan_diff(["--cached"], rules)
    elif args.range:
        findings = scan_diff([args.range], rules)
    else:
        findings = scan_tracked_files(rules)

    if findings:
        print("Possible private data or out-of-repo references found:", file=sys.stderr)
        for finding in findings:
            print(f"  {finding}", file=sys.stderr)
        print(
            "Remove them, or rephrase if this is a false positive. "
            "Private content belongs in the separate private repository.",
            file=sys.stderr,
        )
        return 1
    print(f"No private-data findings ({len(rules)} rules checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
