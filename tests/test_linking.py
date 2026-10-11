from app.agents.linking import Mention, _sentence, apply_mentions, find_mentions, name_pattern, score_mentions, target_names
from app.backend.knowledge_radar.models import NoteDetail


def note(slug, title_en, title_de=None, aliases=(), content_en="### TL;DR\nAbout it.\n"):
    return NoteDetail.model_construct(
        slug=slug, title_en=title_en, title_de=title_de or title_en, aliases=list(aliases), content_en=content_en
    )


NOTES = {
    "clustering": note("clustering", "Clustering"),
    "complex": note("complex", "ComplEx"),
    "rag": note("rag", "Retrieval-Augmented Generation", aliases=["RAG"]),
    "source": note("source", "Source"),
}

TEXT = """---
title_en: Source
---

## EN

### TL;DR
A complex method for clustering documents; Clustering again. RAG helps.

#### Clustering in detail
| Approach | Suited for |
|---|---|
| k-means | RAG pipelines |

```text
clustering in code
```

### Sources
- Doe, J. (2020). *Clustering things.* [x](https://example.org/clustering)

## DE

### TL;DR
Ein Verfahren für [[clustering|Clustering]] und RAG.
"""


def test_first_unlinked_mention_per_section_outside_headings_code_and_sources():
    mentions = find_mentions({"source": TEXT}, NOTES)

    found = {(m.target, m.language): (m.line, m.text) for m in mentions}
    lines = TEXT.split("\n")
    assert found[("clustering", "EN")] == (lines.index("A complex method for clustering documents; Clustering again. RAG helps."), "clustering")
    assert found[("rag", "EN")][1] == "RAG"
    assert ("clustering", "DE") not in found  # the DE section links it already
    assert found[("rag", "DE")][1] == "RAG"
    assert not any(m.target == "complex" for m in mentions)  # "complex" is not ComplEx
    assert not any(m.target == "source" for m in mentions)  # no links to the note itself


def test_only_the_requested_targets_are_searched():
    assert {m.target for m in find_mentions({"source": TEXT}, NOTES, targets={"rag"})} == {"rag"}


def test_names_include_aliases_and_titles_without_parentheses():
    sbert = note("sentence-bert", "Sentence-BERT (SBERT)", aliases=["SBERT"])

    assert target_names(sbert, "EN") == ["Sentence-BERT (SBERT)", "Sentence-BERT", "SBERT"]
    assert name_pattern("ComplEx").search("a complex case") is None
    assert name_pattern("Clustering").search("hierarchical clustering") is not None
    assert name_pattern("BM25").search("BM25F") is None


def test_links_keep_the_matched_words_and_escape_pipes_in_tables():
    lines = ["Text about clustering here.", "| k-means | RAG pipelines |"]
    mentions = [
        Mention("clustering", "s", "EN", 0, 11, 21, "clustering", ""),
        Mention("rag", "s", "EN", 1, 12, 15, "RAG", ""),
    ]

    assert apply_mentions("\n".join(lines), mentions).split("\n") == [
        "Text about [[clustering|clustering]] here.",
        "| k-means | [[rag\\|RAG]] pipelines |",
    ]


def test_the_sentence_around_a_mention_is_scored_against_the_target_summary():
    def embed(texts):
        return [[1.0, 0.0] if "clustering" in text.casefold() else [0.0, 1.0] for text in texts]

    mentions = [
        Mention("clustering", "s", "EN", 0, 0, 1, "x", "We group documents by clustering."),
        Mention("clustering", "s", "EN", 1, 0, 1, "x", "Entities need a classification under the act."),
    ]
    scored = score_mentions(mentions, {"clustering": note("clustering", "Clustering")}, embed)

    assert [m.score for m in scored] == [1.0, 0.0]


def test_sentence_is_the_one_containing_the_mention():
    line = "First sentence here. Second with clustering, e.g. k-means. Third one."

    assert _sentence(line, line.index("clustering")) == "Second with clustering, e.g. k-means."
