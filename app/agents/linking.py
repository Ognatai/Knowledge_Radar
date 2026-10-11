"""Linking agent: wikilinks from notes to the notes they mention without linking.

Algorithmic, no generative model (architecture, step 4):

1. Mentions: the first unlinked mention of another note's title or alias in each
   language section, outside headings, notices, code, tables of sources and
   existing links. Mixed-case and all-caps names (ComplEx, RAG) match
   case-sensitively, so "complex" does not link to ComplEx.
2. Sense check: a name can mean something else ("classification" of entities
   under NIS2 is not the ML task). The sentence around the mention is compared
   with the target note's summary by embedding similarity; only mentions at or
   above `MIN_SCORE` are linked.

    python -m app.agents.linking                         # report the suggestions
    python -m app.agents.linking --target gpt            # only links to one note
    python -m app.agents.linking --target gpt --apply    # write them into the notes
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass, replace
from pathlib import Path

from app.backend.knowledge_radar import embeddings
from app.backend.knowledge_radar.models import NoteDetail
from app.backend.knowledge_radar.notes import configured_notes_directory, load_notes

# Calibrated on all 243 suggestions of 2026-10-11: below it were nearly all wrong senses
# ("classification" of entities in DORA, KWG, NIS2, MaRisk, the AI Act), above it one
# ("quantization" of signals); correct but incidental mentions below it are skipped.
MIN_SCORE = 0.36
MIN_NAME_LENGTH = 3
SOURCE_HEADINGS = {"Sources", "Quellen", "Official sources", "Amtliche Quellen"}
PROTECTED = re.compile(r"\[\[[^\]]*\]\]|\[[^\]]*\]\([^)]*\)|`[^`]*`|https?://\S+")
SENTENCE_END = re.compile(r"(?<!\bvs\.)(?<!\bal\.)(?<!e\.g\.)(?<!i\.e\.)(?<!z\.\sB\.)(?<=[.!?])\s+(?=[A-ZÄÖÜ\[])")
LINK_INSTRUCTION = "Given a sentence that mentions a term, retrieve the encyclopedia article about that term"


@dataclass(frozen=True)
class Mention:
    target: str  # the note to link to
    source: str  # the note that mentions it
    language: str  # "EN" or "DE"
    line: int  # index of the line in the note file
    start: int
    end: int
    text: str  # the matched words, kept as the link label
    sentence: str
    score: float | None = None


def target_names(note: NoteDetail, language: str) -> list[str]:
    """Title in the language, aliases, and the title without a parenthesised addition."""
    names = {note.title_en if language == "EN" else note.title_de, *note.aliases}
    names |= {re.sub(r"\s*\([^)]*\)\s*$", "", name).strip() for name in names}
    return sorted((name for name in names if len(name) >= MIN_NAME_LENGTH), key=len, reverse=True)


def name_pattern(name: str) -> re.Pattern[str]:
    # "Clustering" and "neural networks" match in any case; "ComplEx", "RAG", "LoRA" only as written.
    plain = name in (name.lower(), name.capitalize(), name.title())
    return re.compile(rf"(?<![\w\-./])({re.escape(name)})(?![\w\-])", re.IGNORECASE if plain else 0)


def _links_to(text: str, slug: str) -> bool:
    return f"[[{slug}|" in text or f"[[{slug}\\|" in text or f"[[{slug}]]" in text


def _sentence(line: str, start: int) -> str:
    """The sentence of `line` that contains position `start` (a table row counts as one)."""
    begin = 0
    for boundary in SENTENCE_END.finditer(line):
        if boundary.start() >= start:
            return line[begin : boundary.start()].strip()
        begin = boundary.end()
    return line[begin:].strip()


def find_mentions(texts: dict[str, str], notes: dict[str, NoteDetail], targets: set[str] | None = None) -> list[Mention]:
    """First unlinked mention of each target per note and language section."""
    patterns = {
        (slug, language): [name_pattern(name) for name in target_names(note, language)]
        for slug, note in notes.items()
        if targets is None or slug in targets
        for language in ("EN", "DE")
    }
    mentions: list[Mention] = []
    for source, text in texts.items():
        lines = text.split("\n")
        sections: dict[str, tuple[int, int]] = {}
        starts = [(i, line[3:].strip()) for i, line in enumerate(lines) if line in ("## EN", "## DE")]
        for index, (start, language) in enumerate(starts):
            end = starts[index + 1][0] if index + 1 < len(starts) else len(lines)
            sections[language] = (start, end)
        for (slug, language), pats in patterns.items():
            if slug == source or language not in sections:
                continue
            start, end = sections[language]
            if _links_to("\n".join(lines[start:end]), slug):
                continue
            mention = _first_mention(lines, start, end, pats)
            if mention:
                line, match_start, match_end = mention
                mentions.append(
                    Mention(slug, source, language, line, match_start, match_end, lines[line][match_start:match_end], _sentence(lines[line], match_start))
                )
    return mentions


def _first_mention(lines: list[str], start: int, end: int, patterns: list[re.Pattern[str]]) -> tuple[int, int, int] | None:
    in_code = in_sources = False
    for index in range(start + 1, end):
        line = lines[index]
        if line.startswith("```"):
            in_code = not in_code
            continue
        if line.startswith("### "):
            in_sources = line[4:].strip() in SOURCE_HEADINGS
            continue
        if in_code or in_sources or line.startswith("#") or line.startswith(">") or not line.strip():
            continue
        protected = [match.span() for match in PROTECTED.finditer(line)]
        best = None
        for pattern in patterns:
            for match in pattern.finditer(line):
                if any(a <= match.start() < b for a, b in protected):
                    continue
                if best is None or match.start() < best[1]:
                    best = (index, match.start(), match.end())
                break
        if best:
            return best
    return None


def summary(note: NoteDetail) -> str:
    """Title and TL;DR of a note: what it is about."""
    match = re.search(r"^### TL;DR\s*\n+(.+?)(?:\n###|\Z)", note.content_en, re.MULTILINE | re.DOTALL)
    return f"{note.title_en}: {(match.group(1) if match else note.content_en)[:600].strip()}"


def score_mentions(
    mentions: list[Mention],
    notes: dict[str, NoteDetail],
    embed: Callable[[list[str]], list[list[float]]] = embeddings.embed,
) -> list[Mention]:
    """Each mention with the similarity of its sentence to the target's summary."""
    if not mentions:
        return []
    targets = sorted({mention.target for mention in mentions})
    target_vectors = dict(zip(targets, embed([summary(notes[slug]) for slug in targets])))
    sentence_vectors = embed([embeddings.query_text(mention.sentence, LINK_INSTRUCTION) for mention in mentions])
    return [
        replace(mention, score=round(sum(a * b for a, b in zip(vector, target_vectors[mention.target])), 3))
        for mention, vector in zip(mentions, sentence_vectors)
    ]


def apply_mentions(text: str, mentions: list[Mention]) -> str:
    """The note text with a wikilink at every mention; a table cell needs an escaped pipe."""
    lines = text.split("\n")
    for mention in sorted(mentions, key=lambda m: (m.line, m.start), reverse=True):
        line = lines[mention.line]
        separator = "\\|" if line.lstrip().startswith("|") else "|"
        lines[mention.line] = f"{line[:mention.start]}[[{mention.target}{separator}{mention.text}]]{line[mention.end:]}"
    return "\n".join(lines)


def suggest(
    notes_directory: Path,
    targets: set[str] | None = None,
    min_score: float = MIN_SCORE,
    embed: Callable[[list[str]], list[list[float]]] = embeddings.embed,
) -> tuple[list[Mention], list[Mention]]:
    """(accepted, rejected) suggestions for all notes."""
    notes = {note.slug: note for note in load_notes(notes_directory)}
    texts = {slug: (notes_directory / f"{slug}.md").read_text(encoding="utf-8") for slug in notes}
    scored = score_mentions(find_mentions(texts, notes, targets), notes, embed)
    accepted = [mention for mention in scored if mention.score is not None and mention.score >= min_score]
    rejected = [mention for mention in scored if mention not in accepted]
    return accepted, rejected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target", action="append", help="only links to this note slug (repeatable)")
    parser.add_argument("--apply", action="store_true", help="write the accepted links into the notes")
    parser.add_argument("--min-score", type=float, default=MIN_SCORE)
    parser.add_argument(
        "--exclude", action="append", default=[], metavar="SOURCE:TARGET",
        help="skip a suggestion that names something else (repeatable), e.g. clustering:quantization",
    )
    parser.add_argument("--notes-dir", type=Path, default=configured_notes_directory())
    args = parser.parse_args()
    # Redirected output on Windows defaults to cp1252, which cannot print all note text.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    try:
        accepted, rejected = suggest(args.notes_dir, set(args.target) if args.target else None, args.min_score)
    except embeddings.EmbeddingError as exc:
        print(exc, file=sys.stderr)
        return 1
    excluded = {tuple(pair.split(":", 1)) for pair in args.exclude}
    rejected += [m for m in accepted if (m.source, m.target) in excluded]
    accepted = [m for m in accepted if (m.source, m.target) not in excluded]
    for label, group in (("link", accepted), ("skip", rejected)):
        for m in sorted(group, key=lambda m: (m.source, m.language, m.target)):
            print(f"{label} {m.score:.3f} {m.source} {m.language} -> {m.target}: {m.text!r} | {m.sentence[:110]}")
    print(f"{len(accepted)} links suggested, {len(rejected)} mentions below {args.min_score}")
    if args.apply:
        by_source: dict[str, list[Mention]] = {}
        for mention in accepted:
            by_source.setdefault(mention.source, []).append(mention)
        for source, mentions in by_source.items():
            path = args.notes_dir / f"{source}.md"
            path.write_text(apply_mentions(path.read_text(encoding="utf-8"), mentions), encoding="utf-8")
        print(f"Wrote links into {len(by_source)} notes; refresh the extraction hashes before committing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
