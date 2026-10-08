"""Read and validate public Markdown notes."""

from __future__ import annotations

import os
import re
from functools import cache
from pathlib import Path
from urllib.parse import urlparse

import yaml

from app.backend.knowledge_radar.models import NoteDetail

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_NOTES_DIRECTORY = REPOSITORY_ROOT / "public" / "notes"
SCHEMA_PATH = REPOSITORY_ROOT / "schema.yaml"
FRONTMATTER_PATTERN = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", re.DOTALL)
SECTION_PATTERN = re.compile(
    r"(?m)^## (EN|DE|Original Source Text \(DE\))\s*$"
)
# [[target]], [[target|label]], [[target#heading]], [[target#heading|label]];
# inside Markdown tables the pipe is escaped: [[target\|label]].
WIKILINK_PATTERN = re.compile(r"\[\[([^\[\]|#\\]+)(?:#[^\[\]|\\]*)?(?:\\?\|[^\[\]]*)?\]\]")
# Note-to-note relations come from [[wikilinks]] (RELATED_TO), not from frontmatter.
UNSUPPORTED_FRONTMATTER_KEYS = {
    "related_notes": "use [[wikilinks]] in the note text instead",
    "topics": "topics are not part of the note format",
}


class NoteRepositoryError(ValueError):
    """Raised when public notes cannot be read or do not follow the note contract."""


def configured_notes_directory() -> Path:
    """Return the configured public notes directory or the repository default."""
    configured = os.environ.get("KNOWLEDGE_RADAR_NOTES_DIR")
    return Path(configured).expanduser() if configured else DEFAULT_NOTES_DIRECTORY


@cache
def public_entity_types(schema_path: Path = SCHEMA_PATH) -> frozenset[str]:
    """Entity types a public note may describe: public node types except `Note` itself."""
    try:
        schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise NoteRepositoryError(f"Could not read schema {schema_path}: {exc}") from exc
    node_types = schema.get("node_types", {}) if isinstance(schema, dict) else {}
    return frozenset(
        name
        for name, definition in node_types.items()
        if name != "Note"
        and isinstance(definition, dict)
        and definition.get("visibility") == "public"
    )


def _required_text(frontmatter: dict[str, object], key: str, path: Path) -> str:
    value = frontmatter.get(key)
    if not isinstance(value, str) or not value.strip():
        raise NoteRepositoryError(f"{path}: '{key}' must be a non-empty string.")
    return value.strip()


def wikilink_targets(markdown: str) -> list[str]:
    """Return wikilink targets in order of first appearance, without '.md' suffixes."""
    targets: list[str] = []
    for match in WIKILINK_PATTERN.finditer(markdown):
        target = match.group(1).strip().removesuffix(".md")
        if target and target not in targets:
            targets.append(target)
    return targets


def _parse_sections(markdown: str, path: Path) -> dict[str, str | None]:
    headers = list(SECTION_PATTERN.finditer(markdown))
    sections: dict[str, str | None] = {
        "EN": None,
        "DE": None,
        "Original Source Text (DE)": None,
    }
    for index, header in enumerate(headers):
        end = headers[index + 1].start() if index + 1 < len(headers) else len(markdown)
        sections[header.group(1)] = markdown[header.end() : end].strip()

    for required in ("EN", "DE"):
        if sections[required] is None or not sections[required]:
            raise NoteRepositoryError(
                f"{path}: required '## {required}' section is missing or empty."
            )
    return sections


def load_note(path: Path, notes_directory: Path) -> NoteDetail:
    """Load one note and enforce its frontmatter, source, and bilingual sections."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise NoteRepositoryError(f"{path}: could not read note: {exc}") from exc

    match = FRONTMATTER_PATTERN.match(text)
    if match is None:
        raise NoteRepositoryError(f"{path}: YAML frontmatter is required.")

    try:
        frontmatter_value = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise NoteRepositoryError(f"{path}: invalid YAML frontmatter: {exc}") from exc
    if not isinstance(frontmatter_value, dict):
        raise NoteRepositoryError(f"{path}: frontmatter must be a YAML mapping.")
    frontmatter: dict[str, object] = frontmatter_value

    for key, hint in UNSUPPORTED_FRONTMATTER_KEYS.items():
        if key in frontmatter:
            raise NoteRepositoryError(f"{path}: unsupported frontmatter key '{key}': {hint}.")

    title_en = _required_text(frontmatter, "title_en", path)
    title_de = _required_text(frontmatter, "title_de", path)
    entity_type = _required_text(frontmatter, "entity_type", path)
    allowed_types = public_entity_types()
    if entity_type not in allowed_types:
        raise NoteRepositoryError(
            f"{path}: entity_type '{entity_type}' is not a public entity type in schema.yaml "
            f"({', '.join(sorted(allowed_types))})."
        )
    source_value = frontmatter.get("sources")
    if not isinstance(source_value, list) or not source_value:
        raise NoteRepositoryError(f"{path}: 'sources' must be a non-empty list of URLs.")

    sources: list[str] = []
    for source in source_value:
        if not isinstance(source, str) or not source.strip():
            raise NoteRepositoryError(f"{path}: each source must be a non-empty URL.")
        source = source.strip()
        parsed = urlparse(source)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise NoteRepositoryError(
                f"{path}: source must be an absolute HTTP(S) URL: {source!r}."
            )
        sources.append(source)

    alias_value = frontmatter.get("aliases") or []
    if not isinstance(alias_value, list) or not all(isinstance(a, str) and a.strip() for a in alias_value):
        raise NoteRepositoryError(f"{path}: 'aliases' must be a list of non-empty strings.")
    aliases = [str(alias).strip() for alias in alias_value]

    body = text[match.end() :]
    sections = _parse_sections(body, path)
    relative_path = path.relative_to(notes_directory).with_suffix("")
    slug = relative_path.as_posix()
    return NoteDetail(
        slug=slug,
        title_en=title_en,
        title_de=title_de,
        entity_type=entity_type,
        sources=sources,
        aliases=aliases,
        # Unresolved targets; load_notes() resolves them against all public notes.
        links=wikilink_targets(body),
        content_en=sections["EN"] or "",
        content_de=sections["DE"] or "",
        original_source_text=sections["Original Source Text (DE)"],
    )


def load_notes(
    notes_directory: Path | None = None,
    planned_slugs: frozenset[str] = frozenset(),
) -> list[NoteDetail]:
    """Load all public notes in stable title order; fail explicitly on malformed notes.

    Wikilinks to `planned_slugs` (notes that are about to be written) are accepted but
    not yet returned as links; they become links once the target note exists.
    """
    directory = notes_directory or configured_notes_directory()
    if not directory.is_dir():
        raise NoteRepositoryError(f"Public notes directory does not exist: {directory}")

    paths = sorted(
        (
            path
            for path in directory.rglob("*.md")
            if not any(part.startswith(".") for part in path.relative_to(directory).parts)
        ),
        key=lambda path: path.as_posix().casefold(),
    )
    symlinked_notes = [path for path in paths if path.is_symlink()]
    if symlinked_notes:
        names = ", ".join(str(path) for path in symlinked_notes)
        raise NoteRepositoryError(f"Symbolic links are not allowed in public notes: {names}")
    notes = [load_note(path, directory) for path in paths]
    resolve = _wikilink_resolver([note.slug for note in notes])
    resolved_notes: list[NoteDetail] = []
    for note in notes:
        links: list[str] = []
        unknown: list[str] = []
        for target in note.links:
            slug = resolve(target)
            if slug is None:
                if target not in planned_slugs:
                    unknown.append(target)
            elif slug != note.slug and slug not in links:
                links.append(slug)
        if unknown:
            raise NoteRepositoryError(
                f"{note.slug}: wikilinks point to unknown public notes: {', '.join(unknown)}."
            )
        resolved_notes.append(note.model_copy(update={"links": links}))
    return sorted(resolved_notes, key=lambda note: note.title_en.casefold())


def _wikilink_resolver(slugs: list[str]):
    """Resolve a target by full slug, or (Obsidian-style) by unique file name."""
    by_slug = set(slugs)
    by_name: dict[str, list[str]] = {}
    for slug in slugs:
        by_name.setdefault(slug.rsplit("/", 1)[-1], []).append(slug)

    def resolve(target: str) -> str | None:
        if target in by_slug:
            return target
        candidates = by_name.get(target, [])
        return candidates[0] if len(candidates) == 1 else None

    return resolve
