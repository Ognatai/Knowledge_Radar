"""The one narrow channel from the private repository to the monitoring pipeline.

Interview retros name topics the knowledge base should cover better ("I was asked about
X and didn't know it"). Approved on 2026-10-11, the monitoring run may use their topic
names as extra search phrases, and nothing else: no company or person names, no text.
Only two kinds of strings leave the private repository, both from the structural graph
(`graph/structure.yaml`): open gaps, which name no known topic, and the names of
*public* topics that retros point to. Each is cut to one short line of plain
characters.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from app.backend.knowledge_radar.graph import Entity

STRUCTURE_FILE = Path("graph") / "structure.yaml"
MAX_TOPIC_LENGTH = 60
ALLOWED = re.compile(r"^[\w .+#/-]+$")


def _clean(topic: object) -> str | None:
    text = " ".join(str(topic).split())
    if 3 <= len(text) <= MAX_TOPIC_LENGTH and ALLOWED.match(text):
        return text
    return None


def gap_topics(private_root: Path | None, public_entities: dict[str, Entity]) -> list[str]:
    """Topic names of knowledge gaps from interview retros, or [] without a private repo."""
    if private_root is None:
        return []
    path = private_root / STRUCTURE_FILE
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    topics = [gap.get("topic") for gap in data.get("open_gaps") or []]
    topics += [
        public_entities[relation["to"]].name_en
        for relation in data.get("relations") or []
        if relation.get("type") == "IDENTIFIED_GAP_IN" and relation.get("to") in public_entities
    ]
    cleaned: dict[str, str] = {}
    for topic in topics:
        text = _clean(topic)
        if text:
            cleaned.setdefault(text.casefold(), text)
    return list(cleaned.values())
