"""Read-only FastAPI endpoints for public notes."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.backend.knowledge_radar.models import NoteDetail, NoteSearchResults, NoteSummary
from app.backend.knowledge_radar.notes import (
    NoteRepositoryError,
    configured_notes_directory,
    load_notes,
)


def create_app(notes_directory: Path | None = None) -> FastAPI:
    app = FastAPI(
        title="Knowledge Radar API",
        description="Read-only search and access to the public Markdown notes.",
        version="0.1.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    public_notes_directory = notes_directory or configured_notes_directory()

    def read_notes() -> list[NoteDetail]:
        try:
            return load_notes(public_notes_directory)
        except NoteRepositoryError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/notes", response_model=list[NoteSummary])
    def list_notes() -> list[NoteDetail]:
        return read_notes()

    @app.get("/api/notes/search", response_model=NoteSearchResults)
    def search_notes(
        q: str = Query(min_length=1, max_length=200),
        limit: int = Query(default=25, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
    ) -> NoteSearchResults:
        query = q.strip().casefold()
        if not query:
            return NoteSearchResults(items=[], total=0, offset=offset, limit=limit)
        matching = [
            note
            for note in read_notes()
            if query
            in " ".join(
                [
                    note.title_en,
                    note.title_de,
                    note.entity_type,
                    note.content_en,
                    note.content_de,
                ]
            ).casefold()
        ]
        return NoteSearchResults(
            items=[NoteSummary.model_validate(note) for note in matching[offset : offset + limit]],
            total=len(matching),
            offset=offset,
            limit=limit,
        )

    @app.get("/api/notes/{slug:path}", response_model=NoteDetail)
    def get_note(slug: str) -> NoteDetail:
        for note in read_notes():
            if note.slug == slug:
                return note
        raise HTTPException(status_code=404, detail=f"Public note not found: {slug}")

    return app


app = create_app()
