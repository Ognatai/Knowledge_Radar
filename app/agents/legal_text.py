"""Source-independent structure of a legal text: headings and articles/sections.

`eurlex` (EU acts) and `gesetze` (German federal law) both produce these types,
so that regulatory notes are built the same way for either source.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Heading:
    level: int  # 1 = Chapter/Teil, 2 = Section/Kapitel, ...
    label: str  # e.g. "CHAPTER II", "Teil 1"
    title: str


@dataclass(frozen=True)
class Section:
    number: str  # e.g. "Article 5", "§ 26"
    title: str
    text: str
    path: tuple[Heading, ...]  # enclosing structural units, outermost first

    @property
    def key(self) -> str:
        """Bare number used in configs and draft file names, e.g. "5", "4a", "26"."""
        return self.number.split()[-1].rstrip(".")
