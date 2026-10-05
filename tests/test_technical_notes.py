import io

import pytest

from app.agents import sources
from app.agents import technical_notes as tn
from app.backend.knowledge_radar.templates import check_template

PAPER = sources.Source(
    url="https://arxiv.org/abs/2409.04701",
    citation="Günther, M. et al. (2024). *Late Chunking.* [arXiv:2409.04701](https://arxiv.org/abs/2409.04701)",
    short="Günther et al. (2024)",
    summary="Late chunking embeds the whole document before splitting into chunks.",
)

ATOM = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom"><entry>
<title>Dense X Retrieval: What Retrieval
  Granularity Should We Use?</title>
<published>2023-12-11T00:00:00Z</published>
<summary>Propositions as retrieval units.</summary>
<author><name>Tong Chen</name></author><author><name>Hongwei Wang</name></author>
<author><name>Sihao Chen</name></author>
</entry></feed>"""


def test_clean_unwraps_markdown_but_keeps_code_blocks():
    assert tn.clean("```markdown\nSome text.\n```") == "Some text."
    diagram = "Intro.\n\n```text\nA ─▶ B\n```"
    assert tn.clean(diagram) == diagram
    assert tn.clean("Intro.\n\n```text\nA ─▶ B") == "Intro.\n\n```text\nA ─▶ B\n```"
    assert tn.clean("Body.\n\n### Sources\n- x") == "Body."


@pytest.mark.parametrize(
    "text",
    ["as shown by Günther et al. (2024)", "(Günther et al., 2024)", "Günther and colleagues (2024)"],
)
def test_cites_accepts_common_citation_forms(text):
    assert tn.cites(text, PAPER)


def test_cites_requires_the_year():
    assert not tn.cites("Günther et al. proposed it", PAPER)


def test_originality_overlap_detects_copied_passages():
    source = "late chunking embeds the whole document before splitting into chunks for retrieval"
    copied = "In short, late chunking embeds the whole document before splitting into chunks."
    rewritten = "The method encodes a long text first and only afterwards pools token vectors per segment."

    assert tn.originality_overlap(copied, [source]) > 0.5
    assert tn.originality_overlap(rewritten, [source]) == 0


def test_unknown_numbers_ignore_diagrams_headings_and_sources():
    text = (
        "#### 3. Overlap\nUse 512 tokens with 10 % overlap.\n\n```text\nstep 7\n```\n\n"
        "### Sources\n- Paper (2024)"
    )
    assert tn.unknown_numbers(text, ["chunks of 512 tokens"]) == ["10"]


def test_assembled_note_passes_the_technical_template():
    plan = tn.NotePlan("rag-chunking", "RAG - Chunking", "RAG: Chunking", "RAG: Chunking", "Method", [], [])
    en_required, _ = tn.sections_for("Method", 0)
    de_required, _ = tn.sections_for("Method", 1)
    english = tn.NOTICE_EN + "".join(
        f"\n\n### {h}\n\nText by {PAPER.short}." for h in en_required if h != "Sources"
    )
    german = tn.NOTICE_DE + "".join(
        f"\n\n### {h}\n\nText von {PAPER.short}." for h in de_required if h != "Quellen"
    )

    note = tn.assemble(plan, [PAPER], english, german)

    assert check_template(note) == []
    assert "### Sources\n\n- Günther, M. et al. (2024)" in note
    assert tn.uncited(english, [PAPER]) == []


def test_format_authors():
    assert sources.format_authors(["Nils Reimers", "Iryna Gurevych"]) == (
        "Reimers, N. & Gurevych, I.", "Reimers & Gurevych",
    )
    assert sources.format_authors(["Patrick Lewis", "A B", "C D"]) == ("Lewis, P. et al.", "Lewis et al.")


def test_resolve_arxiv_verifies_the_title(tmp_path, monkeypatch):
    monkeypatch.setattr(sources, "REQUEST_SPACING_SECONDS", 0)
    monkeypatch.setattr(sources.urllib.request, "urlopen", lambda url, timeout: io.BytesIO(ATOM.encode()))

    source = sources.resolve({"arxiv": "2312.06648", "expect": "Dense X Retrieval"}, tmp_path)

    assert source.short == "Chen et al. (2023)"
    assert source.citation.startswith("Chen, T. et al. (2023). *Dense X Retrieval: What Retrieval Granularity Should We Use?*")
    with pytest.raises(sources.SourceError, match="does not contain"):
        sources.resolve({"arxiv": "2312.06648", "expect": "Late Chunking"}, tmp_path)


def test_non_arxiv_sources_need_a_citation():
    with pytest.raises(sources.SourceError, match="needs 'citation'"):
        sources.resolve({"url": "https://example.org"})
