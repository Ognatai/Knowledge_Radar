"""Typed data returned by the public-note API and the static site export."""

from pydantic import BaseModel, Field


class NoteSummary(BaseModel):
    slug: str
    title_en: str
    title_de: str
    entity_type: str
    sources: list[str]
    links: list[str] = Field(
        default_factory=list,
        description="Slugs of notes referenced via [[wikilinks]] (RELATED_TO edges).",
    )


class NoteDetail(NoteSummary):
    content_en: str
    content_de: str
    original_source_text: str | None = None


class NoteSearchResults(BaseModel):
    items: list[NoteSummary]
    total: int
    offset: int
    limit: int
