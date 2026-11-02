"""The pop-up after the weekly run: what each step did, read from the run's log.

The run happens at night, when a toast notification goes unseen. run-monitoring.ps1
writes this notice to `.knowledge-radar/monitoring/run-notice.json` after every run,
successful or not; scripts/show-run-notice.ps1 shows it as a window right away and,
until it was closed, again at logon and when the PC is unlocked. The texts are German
and address no one, like the site.

    python -m app.agents.monitoring.notice <log file>
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from app.agents.monitoring.findings import RUNS_DIRECTORY
from app.agents.monitoring.weekly import STEPS

NOTICE_FILE = RUNS_DIRECTORY.parent / "run-notice.json"
MAX_ERRORS = 12
WEEKDAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
LOG_LINE = re.compile(r"^(\d{4}-\d\d-\d\d) ([0-9]{2}:[0-9]{2}):[0-9]{2}  ?(.*)$")
HEADER = re.compile(r"^=== (.+?) ===$")
EXITED = re.compile(r"^=== (.+?) exited with (-?\d+) ===$")

STEP_LABELS = {
    "validate notes": "Notes geprüft",
    "update index": "Index aktualisiert",
    "update private repo": "Privates Repo aktualisiert",
    "fetch sources": "Quellen abgerufen",
    "assess relevance": "Relevanz bewertet",
    "write drafts": "Entwürfe geschrieben",
    "propose inbox": "Private Inbox",
}
DECISION_LABELS = {
    "irrelevant": "irrelevant",
    "duplicate": "schon abgedeckt",
    "update": "Ergänzung",
    "new_topic": "neues Thema",
    "promotion": "Hochstufung",
}


@dataclass
class Notice:
    title: str
    message: str
    log: str
    failed: bool

    def to_json(self) -> str:
        return json.dumps({"title": self.title, "message": self.message, "log": self.log, "failed": self.failed},
                          ensure_ascii=False, indent=1)


def _first(pattern: str, lines: list[str]) -> re.Match[str] | None:
    return next((match for line in lines if (match := re.search(pattern, line))), None)


def _detail(step: str, lines: list[str]) -> str:
    """What one step did, from its own lines of the log; empty when it printed nothing known."""
    if step == "validate notes" and (m := _first(r"Validated (\d+) public note.*\((\d+) entities, (\d+) relations\)", lines)):
        return f"{m[1]} Notes, {m[2]} Entitäten, {m[3]} Relationen"
    if step == "update index" and (m := _first(r"Updated index: (\d+) notes embedded, (\d+) removed", lines)):
        return f"{m[1]} Notes neu eingebettet, {m[2]} entfernt"
    if step == "update private repo" and (m := _first(r"Structure rebuilt: .*?(\d+) open gaps", lines)):
        return f"{m[1]} offene Lücken aus Retros"
    if step == "fetch sources" and (m := _first(r"^(\d+) new findings", lines)):
        return f"{m[1]} neue Funde"
    if step == "assess relevance" and (m := _first(r"^\d+ \w+(, \d+ \w+)*$", lines)):
        counts = re.findall(r"(\d+) (\w+)", m[0])
        return ", ".join(f"{count} {DECISION_LABELS.get(name, name)}" for count, name in counts if count != "0") or "keine Funde"
    if step == "write drafts":
        checked = sum(1 for line in lines if line.startswith("Checking "))
        failed = sum(1 for line in lines if line.startswith("Failed "))
        text = f"{checked} Entwürfe" if checked else "keine"
        return text + (f", {failed} fehlgeschlagen" if failed else "")
    if step == "propose inbox":
        if (m := _first(r"^INBOX: (.+)$", lines)) and m[1] != "nothing to propose":
            return f"neue Funde auf Branch {m[1]}"
        if _first(r"^No private repository", lines):
            return "kein privates Repo eingerichtet"
        return "nichts Neues zu Lücken aus Retros"
    return ""


def build_notice(log_text: str, log_path: str) -> Notice:
    entries = [m.groups() for line in log_text.lstrip("\ufeff").splitlines() if (m := LOG_LINE.match(line))]
    messages = [text for _, _, text in entries]

    sections: dict[str, list[str]] = {}
    codes: dict[str, int] = {}
    current = None
    for text in messages:
        if exited := EXITED.match(text):
            codes[exited[1]] = int(exited[2])
            continue
        if (header := HEADER.match(text)) and header[1] in STEP_LABELS:
            current = header[1]
            sections[current] = []
            codes.setdefault(current, 0)
            continue
        if text.startswith("SUMMARY: ") or text.startswith("Monitoring run "):
            current = None
        if current:
            sections[current].append(text)

    failure = _first(r"^Monitoring run FAILED: (.*)$", messages)
    succeeded = failure is None and "Monitoring run finished successfully." in messages
    lines = []
    if entries:
        day = date.fromisoformat(entries[0][0])
        lines += [f"{WEEKDAYS[day.weekday()]}, {day:%d.%m.%Y}, {entries[0][1]}–{entries[-1][1]} Uhr", ""]
    for step in STEPS:
        label = STEP_LABELS[step.name]
        if step.name not in sections:
            lines.append(f"–  {label}: nicht gelaufen")
            continue
        detail = _detail(step.name, sections[step.name])
        if codes[step.name] != 0:
            lines.append(f"✗  {label}: fehlgeschlagen (Exit-Code {codes[step.name]})" + (f"; {detail}" if detail else ""))
        else:
            lines.append(f"✓  {label}" + (f": {detail}" if detail else ""))

    errors = [text.removeprefix("Error: ").rstrip(":") for text in sections.get("fetch sources", []) if text.startswith("Error: ")]
    if errors:
        lines += ["", f"Quellenfehler ({len(errors)}):"]
        lines += [f"   •  {error}" for error in errors[:MAX_ERRORS]]
        if len(errors) > MAX_ERRORS:
            lines.append(f"   •  … und {len(errors) - MAX_ERRORS} weitere (siehe Log)")

    lines.append("")
    branch = _first(r"^=== drafts on local branch (\S+) ===$", messages)
    if not succeeded:
        lines.append(f"Fehler: {failure[1] if failure else 'Der Run hat nicht zu Ende gefunden.'}")
    elif branch:
        lines.append(f"Entwürfe warten auf das Review: Branch {branch[1]}.")
    elif _detail("write drafts", sections.get("write drafts", [])) not in ("", "keine"):
        lines.append("Entwürfe geschrieben, aber kein Branch angelegt (siehe Log).")
    else:
        lines.append("Keine Vorschläge diese Woche.")

    title = "Knowledge Radar: Weekly Run erfolgreich" if succeeded else "Knowledge Radar: Weekly Run fehlgeschlagen"
    return Notice(title=title, message="\n".join(lines), log=log_path, failed=not succeeded)


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the pop-up notice for a weekly run from its log.")
    parser.add_argument("log", type=Path)
    parser.add_argument("--out", type=Path, default=NOTICE_FILE)
    args = parser.parse_args()
    notice = build_notice(args.log.read_text(encoding="utf-8"), str(args.log.resolve()))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(notice.to_json(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
