"""Fetch German federal law from gesetze-im-internet.de and split it into sections.

Every law is offered as official XML (`https://www.gesetze-im-internet.de/<slug>/xml.zip`,
gii-norm DTD). The XML lists structural units (Teil, Kapitel, Abschnitt; nesting
given by the length of `gliederungskennzahl`) and the individual norms (§ or
Art.) with title and text, plus metadata such as the official citation and the
"Stand". Downloads are cached under `.knowledge-radar/cache/gesetze/`.
"""

from __future__ import annotations

import io
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

from app.agents.legal_text import Heading, Section
from app.backend.knowledge_radar.notes import REPOSITORY_ROOT

CACHE_DIRECTORY = REPOSITORY_ROOT / ".knowledge-radar" / "cache" / "gesetze"
XML_URL = "https://www.gesetze-im-internet.de/{slug}/xml.zip"
HTML_URL = "https://www.gesetze-im-internet.de/{slug}/"


class GesetzeError(RuntimeError):
    """Raised when a law cannot be fetched or parsed."""


@dataclass
class Law:
    slug: str
    abbreviation: str  # e.g. "BDSG"
    title: str  # e.g. "Bundesdatenschutzgesetz"
    enacted: str  # ISO date of the Ausfertigung
    citation: str  # e.g. "BGBl I 2017, 2097"
    status: list[str] = field(default_factory=list)  # "Stand" notes
    sections: list[Section] = field(default_factory=list)

    @property
    def url(self) -> str:
        return HTML_URL.format(slug=self.slug)


def fetch_xml(slug: str, cache_directory: Path = CACHE_DIRECTORY, refresh: bool = False) -> bytes:
    cache_directory.mkdir(parents=True, exist_ok=True)
    cached = cache_directory / f"{slug}.xml"
    if cached.is_file() and not refresh:
        return cached.read_bytes()
    try:
        with urllib.request.urlopen(XML_URL.format(slug=slug), timeout=60) as response:
            archive = zipfile.ZipFile(io.BytesIO(response.read()))
    except (OSError, zipfile.BadZipFile) as exc:
        raise GesetzeError(f"could not download {slug}: {exc}") from exc
    names = [name for name in archive.namelist() if name.endswith(".xml")]
    if len(names) != 1:
        raise GesetzeError(f"{slug}: expected one XML file, found {names}")
    data = archive.read(names[0])
    cached.write_bytes(data)
    return data


def _text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    parts: list[str] = []

    def walk(node: ET.Element) -> None:
        # Document order: own text, children (each followed by its tail).
        if node.tag in {"P", "DT", "DD", "LA", "BR"} and parts and not parts[-1].endswith("\n"):
            parts.append("\n")
        if node.text:
            parts.append(node.text)
        for child in node:
            walk(child)
            if child.tail:
                if child.tag in {"DL", "BR"} and parts and not parts[-1].endswith("\n"):
                    parts.append("\n")
                parts.append(child.tail)

    walk(element)
    text = "".join(parts)
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\s*\n\s*", "\n", text).strip()


def _join_hyphenation(title: str) -> str:
    """Undo line-break hyphenation ("Anwendungs- bereiche"), keep "Bußgeld- und Straf..."."""
    return re.sub(r"(\w)- (?!und\b|oder\b|sowie\b|bzw\.)([a-zäöüß])", r"\1\2", title)


def parse(xml: bytes, slug: str) -> Law:
    root = ET.fromstring(xml)
    norms = root.findall("norm")
    if not norms:
        raise GesetzeError(f"{slug}: no norms in XML")
    meta = norms[0].find("metadaten")
    law = Law(
        slug=slug,
        abbreviation=(meta.findtext("amtabk") or meta.findtext("jurabk") or slug).strip(),
        title=(meta.findtext("langue") or meta.findtext("kurzue") or "").strip(),
        enacted=(meta.findtext("ausfertigung-datum") or "").strip(),
        citation=" ".join(
            part.strip()
            for part in (meta.findtext("fundstelle/periodikum") or "", meta.findtext("fundstelle/zitstelle") or "")
            if part.strip()
        ),
        status=[
            (entry.findtext("standkommentar") or "").strip()
            for entry in meta.findall("standangabe")
            if (entry.findtext("standtyp") or "").strip() == "Stand"
        ],
    )

    path: list[Heading] = []
    for norm in norms[1:]:
        meta = norm.find("metadaten")
        unit = meta.find("gliederungseinheit")
        number = (meta.findtext("enbez") or "").strip()
        if unit is not None and not number:
            level = max(1, len((unit.findtext("gliederungskennzahl") or "").strip()) // 3)
            heading = Heading(level, (unit.findtext("gliederungsbez") or "").strip(),
                              (unit.findtext("gliederungstitel") or "").strip())
            path = [h for h in path if h.level < level] + [heading]
            continue
        if not re.match(r"^(§|Art\.?|Artikel)\s*\d", number):
            continue  # table of contents, annexes, final formulas
        law.sections.append(Section(
            number=number,
            title=_join_hyphenation((meta.findtext("titel") or "").strip()),
            text=_text(norm.find("textdaten/text/Content")),
            path=tuple(path),
        ))
    if not law.sections:
        raise GesetzeError(f"{slug}: no sections found")
    return law


def load(slug: str, refresh: bool = False) -> Law:
    return parse(fetch_xml(slug, refresh=refresh), slug)
