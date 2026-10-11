"""FastAPI endpoints of the local app: read-only public notes and the chat over both indices.

The app runs only on localhost (ThinkPad, Docker); the chat is the one place where the
public and the private index are read together (see chat.py).
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.backend.knowledge_radar import chat
from app.backend.knowledge_radar.models import ChatRequest, ChatResponse, ChatSource, NoteDetail, NoteSearchResults, NoteSummary
from app.backend.knowledge_radar.notes import (
    NoteRepositoryError,
    configured_notes_directory,
    load_notes,
)


class Indices:
    """One Neo4j driver per index, opened on first use and kept; an index that cannot be
    reached is tried again on the next question."""

    def __init__(self, connectors: dict[str, Callable[[], Any]]) -> None:
        self.connectors = connectors
        self.drivers: dict[str, Any] = {}
        self.lock = threading.Lock()

    def store(self, name: str) -> chat.SearchableStore:
        from app.backend.knowledge_radar.index import Neo4jStore

        with self.lock:
            if name not in self.drivers:
                self.drivers[name] = self.connectors[name]()
            return Neo4jStore(self.drivers[name], visibility=name)

    def factories(self, scope: str) -> dict[str, Callable[[], chat.SearchableStore]]:
        names = [name for name in self.connectors if scope in ("all", name)]
        return {name: (lambda name=name: self.store(name)) for name in names}

    def close(self) -> None:
        for driver in self.drivers.values():
            driver.close()
        self.drivers.clear()


def default_indices() -> Indices:
    from app.backend.knowledge_radar.index import connect
    from app.backend.knowledge_radar.private_index import connect_private

    return Indices({"public": connect, "private": connect_private})


def create_app(
    notes_directory: Path | None = None,
    indices: Indices | None = None,
    ask: Callable[..., chat.ChatAnswer] = chat.ask,
) -> FastAPI:
    app = FastAPI(
        title="Knowledge Radar API",
        description="Public notes (read-only) and the local chat over the public and the private index.",
        version="0.2.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
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

    chat_indices = indices or default_indices()
    app.router.on_shutdown.append(chat_indices.close)

    @app.post("/api/chat", response_model=ChatResponse)
    def ask_question(request: ChatRequest) -> ChatResponse:
        try:
            history = [chat.Turn(turn.role, turn.content) for turn in request.history]
            result = ask(request.question, chat_indices.factories(request.scope), language=request.language, history=history)
        except Exception as exc:  # noqa: BLE001 - the model or the embedding server is down
            raise HTTPException(status_code=503, detail=f"The local model is not available: {exc}") from exc
        return ChatResponse(
            answer=result.answer,
            sources=[ChatSource(**vars(source)) for source in result.sources],
            facts=result.facts,
            unavailable=result.unavailable,
        )

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
