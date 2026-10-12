"""FastAPI endpoints of the local app: read-only public notes and the chat over both indices.

The app runs only on localhost (ThinkPad, Docker); the chat is the one place where the
public and the private index are read together (see chat.py).
"""

from __future__ import annotations

import re
import threading
from collections.abc import Callable
from dataclasses import asdict
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.agents.private_refresh import FOREGROUND
from app.backend.knowledge_radar import chat, interviews, prep, review, study_guide
from app.backend.knowledge_radar.areas import areas_path, load_areas
from app.backend.knowledge_radar.config import LocalConfigError, load_local_config
from app.backend.knowledge_radar.models import (
    ChatRequest,
    ChatResponse,
    ChatSource,
    DraftDecision,
    InboxAction,
    NewApplication,
    NewRound,
    NoteDetail,
    NoteSearchResults,
    NoteSummary,
    PrepIn,
    PrepRequest,
    RetroDraftRequest,
    RetroIn,
)
from app.backend.knowledge_radar.private_repo import PrivateRepoError
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


def configured_private_root() -> Path | None:
    try:
        return load_local_config().private_repo_path
    except LocalConfigError:
        return None


def default_refresher(root: Path | None):
    """Research, structure, local extraction and private index after each write (app/agents/private_refresh.py)."""
    from app.agents.private_refresh import Refresher, refresh
    from app.backend.knowledge_radar.private_index import connect_private
    from app.backend.knowledge_radar.research import default_research

    if not root:
        return None
    research = default_research()
    return Refresher(lambda log: refresh(root, connect_private, model=chat.chat_model(), log=log, research=research))


def default_proposals() -> review.PublicProposals:
    """The Desktop's local proposal branches; on the ThinkPad there are none."""
    from app.agents.monitoring.findings import STATE_DIRECTORY
    from app.backend.knowledge_radar.notes import REPOSITORY_ROOT

    def discussing_notes(slug: str) -> int:
        from app.backend.knowledge_radar.graph import DEFAULT_GRAPH_DIRECTORY, load_graph
        from app.backend.knowledge_radar.notes import configured_notes_directory, load_notes

        notes_directory = configured_notes_directory()
        graph = load_graph(DEFAULT_GRAPH_DIRECTORY, load_notes(notes_directory), notes_directory)
        return sum(1 for note, entity in graph.discusses if entity == slug and note != slug)

    return review.PublicProposals(REPOSITORY_ROOT / ".git", STATE_DIRECTORY / "review-decisions.json",
                                  STATE_DIRECTORY / "promotions-declined.json", discussing_notes)


def default_inbox(root: Path | None) -> review.PrivateInbox | None:
    from app.backend.knowledge_radar.private_git import PrivateRepo, gitlab_token

    return review.PrivateInbox(PrivateRepo(root, gitlab_token())) if root else None


def create_app(
    notes_directory: Path | None = None,
    indices: Indices | None = None,
    ask: Callable[..., chat.ChatAnswer] = chat.ask,
    private_root: Path | None | str = "configured",
    refresher: Any = "default",
    generate: Callable[..., str] | None = None,
    proposals: Any = "default",
    inbox: Any = "default",
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
            with FOREGROUND:
                result = ask(request.question, chat_indices.factories(request.scope), language=request.language, history=history)
        except Exception as exc:  # noqa: BLE001 - the model or the embedding server is down
            raise HTTPException(status_code=503, detail=f"The local model is not available: {exc}") from exc
        return ChatResponse(
            answer=result.answer,
            sources=[ChatSource(**vars(source)) for source in result.sources],
            facts=result.facts,
            unavailable=result.unavailable,
        )

    root = configured_private_root() if private_root == "configured" else private_root
    refresh_job = default_refresher(root) if refresher == "default" else refresher

    def private() -> Path:
        if root is None:
            raise HTTPException(status_code=409, detail="No private repository is configured (private_repo_path).")
        return root

    def written(files: list[str]) -> dict[str, Any]:
        if refresh_job is not None:
            refresh_job.request()
        return {"files": files, "refresh": asdict(refresh_job.status) if refresh_job else None}

    def interview_errors(action: Callable[[], list[str]]) -> dict[str, Any]:
        try:
            return written(action())
        except (interviews.InterviewError, PrivateRepoError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/api/private/applications")
    def list_applications() -> dict[str, Any]:
        if root is None:
            return {"configured": False, "applications": []}
        return {"configured": True, "applications": [asdict(a) for a in interviews.applications(root)]}

    @app.post("/api/private/applications")
    def new_application(request: NewApplication) -> dict[str, Any]:
        people = [interviews.Interviewer(**person.model_dump()) for person in request.interviewers]
        fields = request.model_dump(exclude={"interviewers"})
        return interview_errors(lambda: interviews.create_application(private(), **fields, interviewers=people))

    @app.post("/api/private/rounds")
    def new_round(request: NewRound) -> dict[str, Any]:
        people = [interviews.Interviewer(**person.model_dump()) for person in request.interviewers]
        fields = request.model_dump(exclude={"interviewers"})
        return interview_errors(lambda: interviews.create_round(private(), **fields, interviewers=people))

    @app.post("/api/private/retro/draft")
    def retro_draft(request: RetroDraftRequest) -> dict[str, str]:
        private()
        answers = request.model_dump(exclude={"date"})
        try:
            options = {"generate": generate} if generate else {}
            with FOREGROUND:  # the background refresh waits for the local model meanwhile
                text = interviews.draft_retro(answers, date=request.date, model=chat.chat_model(), **options)
        except interviews.InterviewError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:  # noqa: BLE001 - the local model is down or answered no JSON
            raise HTTPException(status_code=503, detail=f"The local model could not draft the retro: {exc}") from exc
        return {"text": text}

    @app.post("/api/private/retro")
    def save_retro(request: RetroIn) -> dict[str, Any]:
        return interview_errors(lambda: interviews.write_retro(private(), company=request.company, role=request.role,
                                                              round_number=request.round, text=request.text))

    @app.post("/api/private/prep/draft")
    def prep_draft(request: PrepRequest) -> dict[str, Any]:
        root_path = private()
        notes = {note.slug: note for note in read_notes()}
        try:
            options = {"generate": generate} if generate else {}
            with FOREGROUND:
                text = prep.draft_prep(root_path, request.company, request.role, request.round, notes=notes,
                                       stores=chat_indices.factories("all"), language=request.language, **options)
        except interviews.InterviewError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:  # noqa: BLE001 - the local model or an index is down
            raise HTTPException(status_code=503, detail=f"The prep could not be drafted: {exc}") from exc
        exists = (root_path / "companies" / request.company / request.role / f"round-{request.round}" / "prep.md").is_file()
        return {"text": text, "exists": exists}

    @app.post("/api/private/prep")
    def save_prep(request: PrepIn) -> dict[str, Any]:
        return interview_errors(lambda: prep.write_prep(private(), company=request.company, role=request.role,
                                                        round_number=request.round, text=request.text, replace=request.replace))

    # The documents tab: the saved preparation and the study guide of a round, built fresh
    # from the files each time, so that notes added later show up.
    def round_dir(company: str, role: str, round_number: int) -> Path:
        for part in (company, role):
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", part):
                raise HTTPException(status_code=400, detail="Invalid company or role.")
        directory = private() / "companies" / company / role / f"round-{round_number}"
        if not (directory / "round.md").is_file():
            raise HTTPException(status_code=404, detail="Unknown round.")
        return directory

    @app.get("/api/private/documents/{company}/{role}/{round_number}/prep")
    def saved_prep(company: str, role: str, round_number: int) -> dict[str, str]:
        path = round_dir(company, role, round_number) / "prep.md"
        if not path.is_file():
            raise HTTPException(status_code=404, detail="No preparation saved for this round.")
        return {"markdown": prep._body(path)}

    @app.get("/api/private/documents/{company}/{role}/{round_number}/study-guide")
    def study_guide_document(company: str, role: str, round_number: int) -> dict[str, str]:
        round_dir(company, role, round_number)
        notes = {note.slug: note for note in read_notes()}
        areas = load_areas(set(notes), areas_path(public_notes_directory))
        return {"markdown": study_guide.build(private(), company, role, round_number, notes, areas)}

    public_proposals = default_proposals() if proposals == "default" else proposals
    private_inbox = default_inbox(root) if inbox == "default" else inbox

    def review_errors(action: Callable[[], Any]) -> Any:
        try:
            return action()
        except HTTPException:
            raise
        except review.ReviewError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:  # noqa: BLE001 - git or GitLab failed; the message says why
            raise HTTPException(status_code=502, detail=str(exc)) from exc

    @app.get("/api/review")
    def review_overview() -> dict[str, Any]:
        overview: dict[str, Any] = {"public": {"available": False, "runs": []}, "private": {"configured": private_inbox is not None, "branches": [], "error": None}}
        if public_proposals is not None and public_proposals.available():
            overview["public"] = {"available": True, "runs": review.as_dict(review_errors(public_proposals.runs))}
        if private_inbox is not None:
            try:
                overview["private"]["branches"] = review.as_dict(private_inbox.branches())
            except Exception as exc:  # noqa: BLE001 - offline or no token: show the public part anyway
                hint = "" if private_inbox.repo.token else "No GitLab token (python -m keyring set knowledge-radar gitlab, then restart the app). "
                overview["private"]["error"] = f"{hint}{exc}"
        return overview

    def proposals_or_404() -> review.PublicProposals:
        if public_proposals is None or not public_proposals.available():
            raise HTTPException(status_code=404, detail="No proposal branches on this machine (they live on the Desktop).")
        return public_proposals

    @app.get("/api/review/public/{run}/{slug}")
    def draft_detail(run: str, slug: str) -> dict[str, str]:
        return review_errors(lambda: proposals_or_404().detail(run, slug))

    @app.post("/api/review/public/{run}/{slug}")
    def decide_draft(run: str, slug: str, decision: DraftDecision) -> dict[str, str]:
        review_errors(lambda: proposals_or_404().decide(run, slug, decision.status))
        return {"status": decision.status}

    @app.post("/api/review/public/{run}")
    def remove_run(run: str) -> dict[str, str]:
        review_errors(lambda: proposals_or_404().remove(run))
        return {"removed": run}

    def inbox_or_409() -> review.PrivateInbox:
        if private_inbox is None:
            raise HTTPException(status_code=409, detail="No private repository is configured (private_repo_path).")
        return private_inbox

    @app.post("/api/review/private/accept")
    def accept_inbox(action: InboxAction) -> dict[str, Any]:
        files = review_errors(lambda: inbox_or_409().accept(action.branch))
        return written(files)

    @app.post("/api/review/private/discard")
    def discard_inbox(action: InboxAction) -> dict[str, str]:
        review_errors(lambda: inbox_or_409().discard(action.branch))
        return {"discarded": action.branch}

    @app.get("/api/private/refresh")
    def refresh_status() -> dict[str, Any] | None:
        return asdict(refresh_job.status) if refresh_job else None

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
