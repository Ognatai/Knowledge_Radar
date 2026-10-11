import datetime as dt

import pytest

from app.backend.knowledge_radar.areas import AreaError, load_areas, news, update_entries
from app.backend.knowledge_radar.models import NoteDetail

AREAS = """version: 1
areas:
  - id: retrieval
    name_en: Retrieval
    name_de: Retrieval
    notes: [bm25, rag]
  - id: law
    name_en: Law
    name_de: Recht
    notes: [gdpr]
    also: [rag]
"""


def write(tmp_path, text=AREAS):
    path = tmp_path / "areas.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def test_areas_keep_their_order_and_secondary_notes(tmp_path):
    areas = load_areas({"bm25", "rag", "gdpr"}, write(tmp_path))

    assert [(a.id, a.notes, a.also) for a in areas] == [("retrieval", ["bm25", "rag"], []), ("law", ["gdpr"], ["rag"])]


@pytest.mark.parametrize(
    "text, slugs, message",
    [
        (AREAS, {"bm25", "rag", "gdpr", "new-note"}, "without a main area: new-note"),
        (AREAS.replace("notes: [gdpr]", "notes: [gdpr, bm25]"), {"bm25", "rag", "gdpr"}, "two main areas"),
        (AREAS.replace("also: [rag]", "also: [gdpr]"), {"bm25", "rag", "gdpr"}, "its own main area"),
        (AREAS.replace("notes: [gdpr]", "notes: [gdpr, gone]"), {"bm25", "rag", "gdpr"}, "unknown notes: gone"),
    ],
)
def test_every_note_needs_exactly_one_main_area(tmp_path, text, slugs, message):
    with pytest.raises(AreaError, match=message):
        load_areas(slugs, write(tmp_path, text))


def note(slug, content_en="Text.", content_de="Text."):
    return NoteDetail.model_construct(slug=slug, content_en=content_en, content_de=content_de)


UPDATED_EN = "Text.\n\n### Updates\n\n#### 2026-10-12 — Judges are unstable\nBody.\n"
UPDATED_DE = "Text.\n\n### Aktualisierungen\n\n#### 2026-10-12 — Bewerter sind instabil\nInhalt.\n"


def test_update_entries_are_read_per_language():
    assert update_entries(UPDATED_EN, "en") == [(dt.date(2026, 10, 12), "Judges are unstable")]
    assert update_entries(UPDATED_DE, "de") == [(dt.date(2026, 10, 12), "Bewerter sind instabil")]
    assert update_entries("No updates.", "en") == []


def test_news_lists_new_notes_and_updates_after_the_migration_newest_first():
    notes = [note("old"), note("bm25"), note("judge", UPDATED_EN, UPDATED_DE)]
    added = {"old": dt.date(2026, 10, 7), "bm25": dt.date(2026, 10, 11), "judge": dt.date(2026, 10, 6)}

    items = news(notes, added, since=dt.date(2026, 10, 8))

    assert items == [
        {"kind": "update", "slug": "judge", "date": "2026-10-12", "title_en": "Judges are unstable", "title_de": "Bewerter sind instabil"},
        {"kind": "new", "slug": "bm25", "date": "2026-10-11"},
    ]


def test_news_is_capped():
    notes = [note(f"n{i}") for i in range(5)]
    added = {f"n{i}": dt.date(2026, 10, 10 + i) for i in range(5)}

    assert [item["slug"] for item in news(notes, added, since=dt.date(2026, 10, 8), limit=2)] == ["n4", "n3"]
