"""Chat over both local indices: retrieval in the app, the answer from the local model.

The public and the private index stay physically separate (decided 2026-10-11); only
this app process, on the ThinkPad, reads both and merges what it finds. The question
is embedded once, each index returns its nearest passages, the best of both form the
numbered sources, and the relations of the entities those notes describe add the graph
around them. The answer comes from the local Ollama model only; private passages never
leave the machine.

The chat remembers the conversation only as long as the frontend sends it along: the
last turns come with every question, a follow-up question is first rewritten into a
standalone one for the search, and nothing is stored on the server.
"""

from __future__ import annotations

import os
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol

from app.agents import llm
from app.backend.knowledge_radar import embeddings

# Small model while developing (decided 2026-10-11); the ThinkPad's model is set per
# deployment with KNOWLEDGE_RADAR_CHAT_MODEL. The instruct variant answers directly: the
# plain qwen3:4b (2507) always reasons first and wrote that reasoning into the answer.
DEFAULT_CHAT_MODEL = "qwen3:4b-instruct"
# Many candidates, because a note has a chunk per section and language: for "Wie hängen
# Prompt Injection und MCP zusammen?" the first MCP passage was the 13th hit.
PASSAGES_PER_INDEX = 40
MAX_SOURCES = 6
# One long note would otherwise fill every source slot (seen 2026-10-11: four sections
# of the prompt-injection note, none of the MCP note, for a question about both).
MAX_PASSAGES_PER_NOTE = 2
MAX_HISTORY_TURNS = 6
MAX_HISTORY_CHARACTERS = 1200
MAX_FACTS = 30
MAX_PASSAGE_CHARACTERS = 1500
SCOPES = ("all", "public", "private")
CITATION = re.compile(r"\[(\d+)\]")
THINKING = re.compile(r"<think>.*?</think>", re.DOTALL)


class SearchableStore(Protocol):
    def search(self, vector: list[float], limit: int = 5) -> list[dict[str, Any]]: ...
    def facts(self, slugs: list[str], limit: int = 30) -> list[dict[str, Any]]: ...


def chat_model() -> str:
    return os.environ.get("KNOWLEDGE_RADAR_CHAT_MODEL", DEFAULT_CHAT_MODEL)


@dataclass
class Turn:
    role: str  # "user" or "assistant"
    content: str


@dataclass
class Source:
    number: int
    note: str
    title: str
    heading: str
    visibility: str
    text: str
    score: float


@dataclass
class Retrieval:
    sources: list[Source]
    facts: list[str]
    # Indices that could not be searched (e.g. the private index is not running).
    unavailable: list[str] = field(default_factory=list)


@dataclass
class ChatAnswer:
    answer: str
    sources: list[Source]
    facts: list[str]
    unavailable: list[str]


def _title(hit: dict[str, Any], language: str) -> str:
    preferred = hit.get("title_de") if language == "de" else hit.get("title_en")
    return preferred or hit.get("title_en") or hit["note"]


def merge_hits(hits: dict[str, list[dict[str, Any]]], language: str, limit: int = MAX_SOURCES) -> list[Source]:
    """The best passages of all indices, one per note and heading, numbered for citation.

    A note's German and English chunk of the same section count once; the one in the
    question's language wins when both are found."""
    ranked = sorted(
        ((visibility, hit) for visibility, found in hits.items() for hit in found),
        key=lambda item: (item[1]["score"] + (0.01 if item[1].get("language") == language else 0)),
        reverse=True,
    )
    sources: list[Source] = []
    seen: set[tuple[str, str]] = set()
    per_note: dict[str, int] = {}
    for visibility, hit in ranked:
        key = (hit["note"], (hit.get("heading") or "").casefold())
        if key in seen or per_note.get(hit["note"], 0) >= MAX_PASSAGES_PER_NOTE:
            continue
        seen.add(key)
        per_note[hit["note"]] = per_note.get(hit["note"], 0) + 1
        sources.append(
            Source(
                number=len(sources) + 1,
                note=hit["note"],
                title=_title(hit, language),
                heading=hit.get("heading") or "",
                visibility=visibility,
                text=(hit.get("text") or "")[:MAX_PASSAGE_CHARACTERS],
                score=float(hit["score"]),
            )
        )
        if len(sources) == limit:
            break
    return sources


def fact_lines(facts: list[dict[str, Any]], limit: int = MAX_FACTS) -> list[str]:
    lines: list[str] = []
    for fact in facts:
        line = f"{fact['source']} {fact['relation']} {fact['target']}"
        if line not in lines:
            lines.append(line)
    return lines[:limit]


def retrieve(
    question: str,
    stores: dict[str, Callable[[], SearchableStore]],
    *,
    language: str = "de",
    embed: Callable[[list[str]], list[list[float]]] = embeddings.embed,
) -> Retrieval:
    """Search every index in `stores` (name -> store factory); an index that cannot be
    reached is reported, not fatal, so the chat keeps working with the public one."""
    vector = embed([embeddings.query_text(question)])[0]
    hits: dict[str, list[dict[str, Any]]] = {}
    opened: dict[str, SearchableStore] = {}
    unavailable: list[str] = []
    for name, open_store in stores.items():
        try:
            store = open_store()
            hits[name] = store.search(vector, PASSAGES_PER_INDEX)
            opened[name] = store
        except Exception:  # noqa: BLE001 - any connection or query failure means "not available"
            unavailable.append(name)
    sources = merge_hits(hits, language)
    raw_facts: list[dict[str, Any]] = []
    for name, store in opened.items():
        slugs = [source.note for source in sources if source.visibility == name]
        if slugs:
            try:
                raw_facts.extend(store.facts(slugs, MAX_FACTS))
            except Exception:  # noqa: BLE001 - facts are a bonus; the passages still answer
                pass
    return Retrieval(sources=sources, facts=fact_lines(raw_facts), unavailable=unavailable)


def recent(history: list[Turn]) -> list[Turn]:
    return [Turn(turn.role, turn.content[:MAX_HISTORY_CHARACTERS]) for turn in history[-MAX_HISTORY_TURNS:]]


def conversation(history: list[Turn]) -> str:
    return "\n".join(f"{'User' if turn.role == 'user' else 'Assistant'}: {turn.content}" for turn in recent(history))


def clean(answer: str) -> str:
    """The answer without reasoning that a thinking model wrote into it."""
    return THINKING.sub("", answer).strip()


def standalone_question(question: str, history: list[Turn], generate: Callable[..., str] = llm.generate) -> str:
    """A follow-up ("und wie verhindert man das?") rewritten so that the search
    understands it without the conversation; the question itself when there is none."""
    if not history:
        return question
    prompt = (
        "Rewrite the last question of this conversation as a standalone question that can be "
        "understood without the conversation: replace words such as \"das\", \"dagegen\", \"it\" "
        "or \"that\" with what they refer to. Keep its language. Return only the question.\n\n"
        "Example:\nUser: Was ist BM25?\nAssistant: Ein Ranking-Verfahren.\nUser: Und wann nutzt man es?\n"
        "Standalone question: Wann nutzt man BM25?\n\n"
        f"{conversation(history)}\nUser: {question}\nStandalone question:"
    )
    rewritten = clean(generate(prompt, model=chat_model(), context_tokens=4096, max_tokens=200, timeout=120))
    rewritten = rewritten.splitlines()[0].strip() if rewritten else ""
    if rewritten and rewritten.casefold() != question.strip().casefold():
        return rewritten
    # The small model sometimes returns the follow-up unchanged; then the previous
    # question gives the search its subject.
    previous = next((turn.content for turn in reversed(history) if turn.role == "user"), "")
    return f"{previous} {question}".strip()


def build_prompt(question: str, retrieval: Retrieval, language: str = "de", history: list[Turn] | None = None) -> str:
    answer_language = "German" if language == "de" else "English"
    parts = [
        "You answer questions from a personal knowledge base. Use only the numbered sources "
        "and the graph facts below. Cite every statement with the number of its source in "
        "square brackets, e.g. [1] or [2][3]. Sources whose title starts with \"Private:\" are "
        "the user's own notes, job postings and interview retros. If the sources do not answer "
        "the question, say so plainly instead of guessing.",
        f"Answer in {answer_language}, concisely, in Markdown.",
        "",
        "## Sources",
    ]
    for source in retrieval.sources:
        heading = f" - {source.heading}" if source.heading else ""
        private = "Private: " if source.visibility == "private" else ""
        parts.append(f"[{source.number}] {private}{source.title}{heading}\n{source.text}\n")
    if not retrieval.sources:
        parts.append("(none found)")
    if retrieval.facts:
        parts += ["## Graph facts", *(f"- {fact}" for fact in retrieval.facts)]
    if history:
        parts += ["", "## Conversation so far", conversation(history)]
    parts += ["", f"## Question\n{question}"]
    return "\n".join(parts)


def cited(answer: str, sources: list[Source]) -> list[Source]:
    """The sources the answer cites, in order of number; all of them if it cites none."""
    numbers = {int(number) for number in CITATION.findall(answer)}
    used = [source for source in sources if source.number in numbers]
    return used or sources


def ask(
    question: str,
    stores: dict[str, Callable[[], SearchableStore]],
    *,
    language: str = "de",
    embed: Callable[[list[str]], list[list[float]]] = embeddings.embed,
    generate: Callable[..., str] = llm.generate,
    history: list[Turn] | None = None,
) -> ChatAnswer:
    history = history or []
    search_question = standalone_question(question, history, generate)
    retrieval = retrieve(search_question, stores, language=language, embed=embed)
    if not retrieval.sources:
        empty = "Dazu habe ich in der Wissensbasis nichts gefunden." if language == "de" else "I found nothing on this in the knowledge base."
        return ChatAnswer(answer=empty, sources=[], facts=[], unavailable=retrieval.unavailable)
    prompt = build_prompt(question, retrieval, language, history)
    answer = clean(generate(prompt, model=chat_model(), context_tokens=8192, max_tokens=1500, timeout=600))
    return ChatAnswer(answer=answer, sources=cited(answer, retrieval.sources), facts=retrieval.facts, unavailable=retrieval.unavailable)
