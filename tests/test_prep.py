"""/prep gathers the round's hard core from files and lets the local model add pitch and questions."""

import datetime as dt
import json

import pytest
import yaml

from app.backend.knowledge_radar import prep
from app.backend.knowledge_radar.interviews import InterviewError, Interviewer, create_application, create_round, write_retro
from app.backend.knowledge_radar.models import NoteDetail
from tests.test_chat import FakeStore, hit

TODAY = lambda: dt.date(2026, 10, 25)  # noqa: E731
NOTES = {
    "retrieval-augmented-generation": NoteDetail.model_construct(
        slug="retrieval-augmented-generation", title_en="Retrieval-Augmented Generation", title_de="Retrieval-Augmented Generation",
        content_en="### TL;DR\nRAG retrieves passages.\n", content_de="### TL;DR\nRAG ruft Passagen ab und\nlässt das Modell antworten.\n### Mehr\nx"),
    "bm25": NoteDetail.model_construct(slug="bm25", title_en="BM25", title_de="BM25", content_en="### TL;DR\nRanking.\n", content_de="### TL;DR\nRanking.\n"),
}


@pytest.fixture
def root(tmp_path):
    root = tmp_path / "private"
    create_application(root, company_name="ACME GmbH", role_title="ML Engineer", posting_text="We need RAG and Rust.",
                       round_date="2026-10-20", interviewers=[Interviewer("Jane Doe", "Head of Data Science", "NLP")], today=TODAY)
    write_retro(root, company="acme-gmbh", role="ml-engineer", round_number=1,
                text="---\ndate: 2026-10-20\nquestions_asked:\n  - How to evaluate RAG?\nstruggled_with:\n  - calibration\n---\nOk.")
    create_round(root, company="acme-gmbh", role="ml-engineer", round_date="2026-11-03",
                 interviewers=[Interviewer("John Roe", "CTO")])
    requirements = {
        "version": 1, "postings": {"companies/acme-gmbh/ml-engineer/job_posting": "hash"},
        "entities": [{"id": "req-acme-gmbh-ml-engineer-1", "type": "Requirement", "name_en": "RAG", "category": "skill"},
                     {"id": "req-acme-gmbh-ml-engineer-2", "type": "Requirement", "name_en": "Rust", "category": "skill"}],
        "relations": [{"from": "posting-acme-gmbh-ml-engineer", "type": "REQUIRES", "to": "req-acme-gmbh-ml-engineer-1"},
                      {"from": "posting-acme-gmbh-ml-engineer", "type": "REQUIRES", "to": "req-acme-gmbh-ml-engineer-2"},
                      {"from": "req-acme-gmbh-ml-engineer-1", "type": "MATCHES", "to": "retrieval-augmented-generation"}],
    }
    (root / "graph").mkdir(exist_ok=True)
    (root / "graph" / "requirements.yaml").write_text(yaml.safe_dump(requirements), encoding="utf-8")
    return root


def fake_embed(texts):
    return [[0.1] for _ in texts]


def model(prompts):
    def generate(prompt, json_schema=None, **options):
        prompts.append(prompt)
        if "sentences" in json_schema["properties"]:
            return json.dumps({"sentences": [
                {"text": "Ich habe eine RAG-Evaluation gebaut.", "evidence": "I built a RAG evaluation"},
                {"text": "Ich spreche fließend Japanisch.", "evidence": "fluent in Japanese"},
                {"text": "Bei [Projekt X] habe ich gelernt.", "evidence": ""}], "adaptations": [
                {"interviewer": "John Roe", "emphasis": "Architektur betonen."}, {"interviewer": "Somebody Else", "emphasis": "x"}]})
        return json.dumps({"questions": [{"question": "Wie groß ist das Team?", "for": "John Roe", "why": "Teamgröße"},
                                         {"question": "Wie wird evaluiert?", "for": "unknown", "why": "Reife"}]})
    return generate


def test_the_hard_core_comes_from_the_files(root):
    context = prep.gather(root, "acme-gmbh", "ml-engineer", 2)

    assert context.company_name == "ACME GmbH" and context.role_title == "ML Engineer" and context.round_date == "2026-11-03"
    assert [p["name"] for p in context.interviewers] == ["John Roe"]
    assert [(r.text, r.notes) for r in context.requirements] == [("RAG", ["retrieval-augmented-generation"]), ("Rust", [])]
    assert context.earlier[0].retro["questions_asked"] == ["How to evaluate RAG?"]


def test_the_draft_renders_requirements_earlier_rounds_pitch_and_questions(root):
    prompts = []
    private = FakeStore([hit("private-notes-my-projects", 0.8, text="I built a RAG evaluation at Foo.", visibility="private")])
    public = FakeStore([hit("bm25", 0.7)])

    text = prep.draft_prep(root, "acme-gmbh", "ml-engineer", 2, notes=NOTES, stores={"public": lambda: public, "private": lambda: private},
                           generate=model(prompts), embed=fake_embed, today=TODAY)

    assert text.startswith("---\nround_number: 2\ngenerated: 2026-10-25\n---\n# Vorbereitung: ACME GmbH – ML Engineer, Runde 2 (2026-11-03)")
    assert "- [Retrieval-Augmented Generation](https://ognatai.github.io/Knowledge_Radar/?view=note&slug=retrieval-augmented-generation): RAG ruft Passagen ab und lässt das Modell antworten." in text
    assert "### Rust (skill)\n- Keine passende Notiz in der Wissensbasis – eine Lücke?" in text
    assert "- **Gefragt:** How to evaluate RAG?" in text and "- **Schwierig:** calibration" in text
    assert "**Für John Roe:** Architektur betonen." in text and "Somebody Else" not in text
    assert ("Ich habe eine RAG-Evaluation gebaut. Ich spreche fließend Japanisch. **[prüfen: nicht aus deinen Notizen belegt]** "
            "Bei [Projekt X] habe ich gelernt.") in text
    assert "- Wie wird evaluiert? _(alle: Reife)_" in text
    assert "## Weitere passende Notizen\n- [BM25]" in text
    # The pitch is built from the candidate's own notes only.
    assert "I built a RAG evaluation at Foo." in prompts[0] and "Use ONLY facts" in prompts[0]


def test_without_extracted_requirements_the_prep_says_so(root):
    (root / "graph" / "requirements.yaml").unlink()

    text = prep.draft_prep(root, "acme-gmbh", "ml-engineer", 1, notes=NOTES, stores={}, generate=model([]), embed=fake_embed, today=TODAY)

    assert "noch nicht ausgelesen" in text and "## Aus früheren Runden" not in text


def test_an_existing_prep_is_replaced_only_on_request(root):
    place = dict(company="acme-gmbh", role="ml-engineer", round_number=2)
    prep.write_prep(root, **place, text="---\nround_number: 2\n---\nFirst.")

    with pytest.raises(InterviewError, match="confirm"):
        prep.write_prep(root, **place, text="---\nround_number: 2\n---\nSecond.")
    prep.write_prep(root, **place, text="---\nround_number: 2\n---\nSecond.", replace=True)

    assert (root / "companies/acme-gmbh/ml-engineer/round-2/prep.md").read_text(encoding="utf-8").endswith("Second.\n")


def test_wikilinks_in_a_tldr_are_plain_text():
    note = NoteDetail.model_construct(slug="x", title_en="X", title_de="X", content_en="",
                                      content_de="### TL;DR\nEin [[large-language-models|Sprachmodell]] und [[rag]].\n")

    assert prep.tldr(note, "de") == "Ein Sprachmodell und rag."
