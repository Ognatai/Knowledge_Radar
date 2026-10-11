"""Bring the private side up to date after the app wrote to the private repository.

/new-application, /new-round and /retro end with this refresh, so that the new data is
available to the chat and /prep right away (architecture: "triggers a reindex"):
structural graph, local extraction of what changed (free text and the postings'
requirements, local Ollama only), then the private index. Each step skips what is
unchanged, so a refresh after one new retro is quick.

The app runs one refresh at a time; a request during a run starts one more run after it.
"""

from __future__ import annotations

import datetime as dt
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.agents.private_extract import extract_all
from app.agents.private_ingest import ingest
from app.backend.knowledge_radar.graph import DEFAULT_GRAPH_DIRECTORY, load_graph
from app.backend.knowledge_radar.index import Neo4jStore
from app.backend.knowledge_radar.notes import configured_notes_directory, load_notes
from app.backend.knowledge_radar.private_index import update_private_index
from app.backend.knowledge_radar.private_repo import load_documents


def refresh(root: Path, connect: Callable[[], Any], *, model: str | None = None, log: Callable[[str], None] = print) -> None:
    notes_directory = configured_notes_directory()
    notes = {note.slug: note for note in load_notes(notes_directory)}
    public = load_graph(DEFAULT_GRAPH_DIRECTORY, list(notes.values()), notes_directory)
    structure, _ = ingest(root, public.entities)
    log(f"Structure: {len(structure.entities)} entities, {len(structure.relations)} relations")
    extract_all(root, load_documents(root), public, notes, model=model, log=log)
    driver = connect()
    try:
        result = update_private_index(Neo4jStore(driver, visibility="private"), root, public.entities, progress=log)
    finally:
        driver.close()
    log(f"Private index: {len(result.embedded)} documents embedded, {len(result.deleted)} removed")


@dataclass
class RefreshStatus:
    state: str = "idle"  # idle, running, done, failed
    message: str = ""
    started: str | None = None
    finished: str | None = None
    log: list[str] = field(default_factory=list)


class Refresher:
    """Runs `refresh` in a background thread, one at a time."""

    def __init__(self, run: Callable[[Callable[[str], None]], None], now: Callable[[], dt.datetime] = dt.datetime.now) -> None:
        self.run = run
        self.now = now
        self.status = RefreshStatus()
        self.lock = threading.Lock()
        self.pending = False
        self.thread: threading.Thread | None = None

    def request(self) -> None:
        with self.lock:
            if self.status.state == "running":
                self.pending = True
                return
            self._start()

    def _start(self) -> None:
        self.status = RefreshStatus(state="running", started=self.now().isoformat(timespec="seconds"))
        self.thread = threading.Thread(target=self._work, daemon=True)
        self.thread.start()

    def _log(self, line: str) -> None:
        self.status.log = [*self.status.log, line][-50:]

    def _work(self) -> None:
        try:
            self.run(self._log)
            state, message = "done", "The private index is up to date."
        except Exception as exc:  # noqa: BLE001 - reported to the user, the app keeps running
            state, message = "failed", f"{type(exc).__name__}: {exc}"
        with self.lock:
            self.status.state, self.status.message = state, message
            self.status.finished = self.now().isoformat(timespec="seconds")
            if self.pending:
                self.pending = False
                self._start()
