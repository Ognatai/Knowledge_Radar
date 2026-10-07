import io

import pytest

from app.agents import sources

ATOM = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom"><entry>
<title>Dense X Retrieval: What Retrieval
  Granularity Should We Use?</title>
<published>2023-12-11T00:00:00Z</published>
<summary>Propositions as retrieval units.</summary>
<author><name>Tong Chen</name></author><author><name>Hongwei Wang</name></author>
<author><name>Sihao Chen</name></author>
</entry></feed>"""


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
