import json
import urllib.parse
from datetime import date

from app.agents.monitoring.foundations import (
    abstract_text,
    arxiv_id_for_title,
    foundational_findings,
    openalex_query_url,
)

WORKS = json.dumps(
    {
        "results": [
            {
                "id": "https://openalex.org/W1",
                "title": "Not What You've Signed Up For:  Compromising Applications",
                "publication_year": 2023,
                "cited_by_count": 577,
                "doi": "https://doi.org/10.1145/3605764.3623985",
                "authorships": [{"author": {"display_name": "Kai Greshake"}}, {"author": {"display_name": "Sahar Abdelnabi"}}],
                "abstract_inverted_index": {"Prompt": [0], "injection": [1], "attacks.": [2]},
            },
            {"id": "https://openalex.org/W2", "title": "Rarely cited", "cited_by_count": 3, "abstract_inverted_index": {"x": [0]}},
            {"id": "https://openalex.org/W3", "title": "No abstract", "cited_by_count": 300, "abstract_inverted_index": None},
            {
                "id": "https://openalex.org/W4",
                "title": "Prompt Injection attack against LLM-integrated Applications",
                "publication_year": 2023,
                "cited_by_count": 84,
                "doi": None,
                "authorships": [],
                "abstract_inverted_index": {"Attacks": [0]},
            },
        ]
    }
)

ARXIV = """<feed xmlns="http://www.w3.org/2005/Atom"><entry>
<id>http://arxiv.org/abs/2306.05499v2</id><published>2023-06-08T00:00:00Z</published>
<title>Prompt Injection attack against LLM-integrated Applications</title><summary>s</summary>
</entry></feed>"""


def test_query_searches_titles_in_computer_science_by_citations():
    query = urllib.parse.parse_qs(urllib.parse.urlparse(openalex_query_url("prompt injection")).query)

    assert query["filter"] == ['title.search:"prompt injection",primary_topic.field.id:17,has_abstract:true']
    assert query["sort"] == ["cited_by_count:desc"]


def test_abstracts_are_rebuilt_from_the_inverted_index():
    assert abstract_text({"world": [1], "Hello": [0], "again": [3], "hello": [2]}) == "Hello world hello again"
    assert abstract_text(None) == ""


def test_arxiv_ids_are_matched_by_exact_title():
    assert arxiv_id_for_title("Prompt Injection Attack against LLM-integrated Applications!", fetch=lambda url: ARXIV) == "2306.05499"
    assert arxiv_id_for_title("Another paper", fetch=lambda url: ARXIV) is None


def test_well_cited_works_with_abstracts_become_findings():
    findings = foundational_findings(
        "prompt injection",
        limit=3,
        fetch=lambda url: WORKS,
        find_arxiv=lambda title: "2306.05499" if title.startswith("Prompt Injection") else None,
    )

    assert [f.id for f in findings] == ["openalex:W1", "arxiv:2306.05499"]
    first = findings[0]
    assert first.title == "Not What You've Signed Up For: Compromising Applications"
    assert first.url == "https://doi.org/10.1145/3605764.3623985"
    assert first.summary == "Prompt injection attacks."
    assert first.authors == ["Kai Greshake", "Sahar Abdelnabi"]
    assert first.published == date(2023, 1, 1)
    assert findings[1].url == "https://arxiv.org/abs/2306.05499"
