"""Bring the private side up to date after the app wrote to the private repository.

/new-application, /new-round and /retro end with this refresh, so that the new data is
available to the chat and /prep right away (architecture: "triggers a reindex"). What
the user needs first comes first:

1. structural graph, then the private index: the chat finds the new files
2. the postings' requirements and matching notes: what /prep needs
   -> the run reports READY: chat and /prep have the new data
3. local extraction of the free text (entities and relations; local Ollama only)
4. the private index again, with the extracted graph

Company and interviewer research with Claude (research.py; only with an API key) runs
in its own thread alongside, as it needs no GPU; its files are indexed in step 4.
Each step skips what is unchanged, so a refresh after one new retro is quick.

The local model serves one request at a time. While the user waits for the chat,
/prep or a retro draft (FOREGROUND), steps 2 and 3 pause before their next model call.

The app runs one refresh at a time; a request during a run starts one more run after it.
"""

from __future__ import annotations

import datetime as dt
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.agents.private_extract import extract_free_text, extract_requirements_all, known_entities
from app.agents.private_ingest import ingest
from app.backend.knowledge_radar.graph import DEFAULT_GRAPH_DIRECTORY, load_graph
from app.backend.knowledge_radar.index import Neo4jStore
from app.backend.knowledge_radar.notes import configured_notes_directory, load_notes
from app.backend.knowledge_radar.private_index import update_private_index
from app.backend.knowledge_radar.private_repo import load_documents


READY = "READY"


class Foreground:
    """Counts the user's requests to the local model; background work waits for none."""

    def __init__(self) -> None:
        self.active = 0
        self.idle = threading.Condition()

    def __enter__(self) -> "Foreground":
        with self.idle:
            self.active += 1
        return self

    def __exit__(self, *exc: Any) -> None:
        with self.idle:
            self.active -= 1
            self.idle.notify_all()

    def wait_idle(self, timeout: float = 900) -> None:
        with self.idle:
            self.idle.wait_for(lambda: self.active == 0, timeout)


FOREGROUND = Foreground()


def refresh(root: Path, connect: Callable[[], Any], *, model: str | None = None, log: Callable[[str], None] = print,
            research: Callable[[Path, Callable[[str], None]], None] | None = None,
            pause: Callable[[], None] = FOREGROUND.wait_idle) -> None:
    researcher = None
    if research is not None:
        researcher = threading.Thread(target=research, args=(root, log), daemon=True)
        researcher.start()
    notes_directory = configured_notes_directory()
    notes = {note.slug: note for note in load_notes(notes_directory)}
    public = load_graph(DEFAULT_GRAPH_DIRECTORY, list(notes.values()), notes_directory)

    def index() -> None:
        driver = connect()
        try:
            result = update_private_index(Neo4jStore(driver, visibility="private"), root, public.entities, progress=log)
        finally:
            driver.close()
        log(f"Private index: {len(result.embedded)} documents embedded, {len(result.deleted)} removed")

    structure, _ = ingest(root, public.entities)
    log(f"Structure: {len(structure.entities)} entities, {len(structure.relations)} relations")
    index()
    extract_requirements_all(root, load_documents(root), notes, model=model, log=log, pause=pause)
    log(READY)
    extract_free_text(root, load_documents(root), known_entities(root, public.entities), public_graph=public,
                      public_notes=notes, model=model, log=log, pause=pause)
    if researcher is not None:
        researcher.join()
    index()


@dataclass
class RefreshStatus:
    state: str = "idle"  # idle, running, done, failed
    message: str = ""
    started: str | None = None
    finished: str | None = None
    log: list[str] = field(default_factory=list)
    # The chat and /prep have the new data; the rest runs on in the background.
    ready: bool = False


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
        if line == READY:
            self.status.ready = True
            return
        self.status.log = [*self.status.log, line][-50:]

    def _work(self) -> None:
        try:
            self.run(self._log)
            state, message = "done", "The private index is up to date."
            self.status.ready = True
        except Exception as exc:  # noqa: BLE001 - reported to the user, the app keeps running
            state, message = "failed", f"{type(exc).__name__}: {exc}"
        with self.lock:
            self.status.state, self.status.message = state, message
            self.status.finished = self.now().isoformat(timespec="seconds")
            if self.pending:
                self.pending = False
                self._start()
