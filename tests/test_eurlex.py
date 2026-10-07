"""Tests for the EUR-Lex article splitter."""

import pytest

from app.agents import eurlex

PAGE = """<html><body>
<div id="cpt_I"><p>CHAPTER I GENERAL PROVISIONS</p>
<div class="eli-subdivision" id="art_1"><p>Article 1 Subject matter</p><p>&#9660;M1 1. This Regulation lays down rules. 2. It applies from 2025.</p></div>
<div class="eli-subdivision" id="art_4a"><p>Article 4a Bias</p><p>1. Processing is allowed for 3 purposes.</p></div>
</div>
<div id="cpt_II"><p>CHAPTER II</p>
<div class="eli-subdivision" id="art_5"><p>Article 5 Prohibitions</p><p>1. Fines up to EUR 35 000 000.</p></div>
</div>
<div class="eli-subdivision" id="fnp_1"><p>Done at Brussels.</p></div>
<div id="anx_I"><p>ANNEX I</p></div>
</body></html>"""


def test_split_articles_stops_at_structural_units_and_drops_markers():
    articles = eurlex.split_articles(PAGE)

    assert list(articles) == ["1", "4a", "5"]
    assert articles["1"] == "Article 1 Subject matter 1. This Regulation lays down rules. 2. It applies from 2025."
    assert "CHAPTER II" not in articles["4a"]
    assert "Brussels" not in articles["5"] and "ANNEX" not in articles["5"]


def test_split_articles_rejects_pages_without_articles():
    with pytest.raises(eurlex.EurLexError):
        eurlex.split_articles("<html>blocked</html>")
