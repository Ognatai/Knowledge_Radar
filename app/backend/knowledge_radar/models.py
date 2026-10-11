"""Typed data returned by the API (public notes, local chat) and the static site export."""

from typing import Literal

from pydantic import BaseModel, Field


class NoteSummary(BaseModel):
    slug: str
    title_en: str
    title_de: str
    entity_type: str
    sources: list[str]
    aliases: list[str] = Field(
        default_factory=list,
        description="Other names of the entity the note describes (frontmatter `aliases`).",
    )
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


class ChatTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=20000)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    # The conversation so far, kept by the frontend; the server stores nothing.
    history: list[ChatTurn] = Field(default_factory=list, max_length=40)
    language: Literal["de", "en"] = "de"
    # Which indices to search: both, or only the public or the private one.
    scope: Literal["all", "public", "private"] = "all"


class ChatSource(BaseModel):
    number: int
    note: str
    title: str
    heading: str
    visibility: str
    text: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]
    facts: list[str]
    unavailable: list[str]
