"""Legal status of EU acts from the Publications Office's CELLAR SPARQL endpoint.

EUR-Lex pages are protected against automated access; CELLAR offers the same
metadata as an open machine interface. Used to check, before writing a note,
which consolidated versions exist and which acts amend or repeal an act.

    python -m app.agents.cellar 32023R2854 32014R0910
"""

from __future__ import annotations

import csv
import io
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, field

ENDPOINT = "https://publications.europa.eu/webapi/rdf/sparql"
PREFIX = "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>\n"
RELATIONS = {
    "resource_legal_amends_resource_legal": "amended by",
    "resource_legal_repeals_resource_legal": "repealed by",
    "resource_legal_implicitly_repeals_resource_legal": "implicitly repealed by",
}


class CellarError(RuntimeError):
    """Raised when the SPARQL endpoint cannot be queried."""


@dataclass
class ActStatus:
    celex: str
    consolidated: list[str] = field(default_factory=list)  # e.g. ["02014R0910-20241018"]
    changes: list[tuple[str, str, str]] = field(default_factory=list)  # (relation, celex, date)

    @property
    def latest_consolidated(self) -> str | None:
        return self.consolidated[-1] if self.consolidated else None


def query(sparql: str, timeout: int = 180) -> list[dict[str, str]]:
    data = urllib.parse.urlencode({"query": PREFIX + sparql}).encode()
    request = urllib.request.Request(ENDPOINT, data=data, headers={"Accept": "text/csv"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            text = response.read().decode("utf-8")
    except OSError as exc:
        raise CellarError(f"CELLAR query failed: {exc}") from exc
    return list(csv.DictReader(io.StringIO(text)))


def status(celex_numbers: list[str]) -> dict[str, ActStatus]:
    """Consolidated versions and amending/repealing acts for base acts like "32023R2854"."""
    result = {celex: ActStatus(celex) for celex in celex_numbers}
    starts = " || ".join(f'STRSTARTS(STR(?celex), "0{celex[1:]}")' for celex in celex_numbers)
    for row in query(f"SELECT DISTINCT ?celex WHERE {{ ?w cdm:resource_legal_id_celex ?celex . "
                     f"FILTER({starts}) }} ORDER BY ?celex"):
        base = "3" + row["celex"][1:].split("-")[0]
        if base in result:
            result[base].consolidated.append(row["celex"])

    values = " ".join(f'"{celex}"' for celex in celex_numbers)
    relations = ", ".join(f"cdm:{name}" for name in RELATIONS)
    rows = query(
        f"SELECT DISTINCT ?target ?rel ?celex ?date WHERE {{ VALUES ?target {{ {values} }} "
        f"?t cdm:resource_legal_id_celex ?tc . FILTER(STR(?tc) = ?target) ?a ?rel ?t . "
        f"FILTER(?rel IN ({relations})) ?a cdm:resource_legal_id_celex ?celex . "
        f"OPTIONAL {{ ?a cdm:work_date_document ?date }} }} ORDER BY ?target ?date"
    )
    for row in rows:
        relation = RELATIONS.get(row["rel"].rsplit("#", 1)[-1], row["rel"])
        result[row["target"]].changes.append((relation, row["celex"], row.get("date", "")))
    return result


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    try:
        for celex, act in status(sys.argv[1:]).items():
            print(f"{celex}: latest consolidated {act.latest_consolidated or '-'}")
            for relation, other, date in act.changes:
                print(f"    {relation} {other} ({date})")
    except CellarError as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
