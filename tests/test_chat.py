"""The chat searches both indices, merges what it finds and answers with cited sources."""

from fastapi.testclient import TestClient

from app.backend.knowledge_radar import chat
from app.backend.knowledge_radar.api import Indices, create_app


def hit(note, score, heading="Overview", language="de", text="text", visibility="public"):
    return {"note": note, "title_en": note.upper(), "title_de": f"{note} (de)", "visibility": visibility,
            "language": language, "heading": heading, "text": text, "score": score, "entities": []}


class FakeStore:
    def __init__(self, hits, facts=(), round_passages=()):
        self.hits, self.fact_rows, self.fact_requests = hits, list(facts), []
        self.round_passages, self.prefix_requests = list(round_passages), []

    def passages_with_prefix(self, prefixes, exclude, limit=3):
        self.prefix_requests.append((prefixes, exclude))
        return self.round_passages[:limit]

    def search(self, vector, limit=5):
        return self.hits[:limit]

    def facts(self, slugs, limit=30):
        self.fact_requests.append(slugs)
        return self.fact_rows


def fake_embed(texts):
    return [[0.1, 0.2] for _ in texts]


def test_the_best_passages_of_both_indices_are_merged_and_numbered():
    sources = chat.merge_hits(
        {"public": [hit("rag", 0.80), hit("bm25", 0.60)], "private": [hit("private-retro-acme", 0.75, visibility="private")]},
        language="de",
    )

    assert [(s.number, s.note, s.visibility) for s in sources] == [(1, "rag", "public"), (2, "private-retro-acme", "private"), (3, "bm25", "public")]
    assert sources[0].title == "rag (de)"


def test_a_section_found_in_both_languages_counts_once_in_the_question_language():
    sources = chat.merge_hits({"public": [hit("rag", 0.80, language="en", text="English"), hit("rag", 0.795, language="de", text="Deutsch")]}, language="de")

    assert [s.text for s in sources] == ["Deutsch"]


def test_an_unreachable_private_index_leaves_the_public_answer():
    public = FakeStore([hit("rag", 0.8)], facts=[{"source": "RAG", "relation": "USES", "target": "BM25"}])

    def broken():
        raise ConnectionError("private index not running")

    retrieval = chat.retrieve("Was ist RAG?", {"public": lambda: public, "private": broken}, embed=fake_embed)

    assert [s.note for s in retrieval.sources] == ["rag"]
    assert retrieval.unavailable == ["private"]
    assert retrieval.facts == ["RAG USES BM25"]
    assert public.fact_requests == [["rag"]]


def test_facts_are_asked_only_from_the_index_the_note_lives_in():
    public, private = FakeStore([hit("rag", 0.8)]), FakeStore([hit("private-retro-acme", 0.7, visibility="private")])

    chat.retrieve("q", {"public": lambda: public, "private": lambda: private}, embed=fake_embed)

    assert public.fact_requests == [["rag"]] and private.fact_requests == [["private-retro-acme"]]


def test_the_prompt_numbers_the_sources_and_marks_private_ones():
    retrieval = chat.Retrieval(
        sources=chat.merge_hits({"private": [hit("private-retro-acme", 0.7, heading="", text="They asked about RAG evaluation.")]}, "en"),
        facts=["RAG USES BM25"],
    )

    prompt = chat.build_prompt("What did ACME ask?", retrieval, language="en")

    assert "[1] Private: PRIVATE-RETRO-ACME\nThey asked about RAG evaluation." in prompt
    assert "- RAG USES BM25" in prompt
    assert "Answer in English" in prompt
    assert prompt.endswith("## Question\nWhat did ACME ask?")


def test_only_the_cited_sources_are_returned():
    sources = chat.merge_hits({"public": [hit("rag", 0.8), hit("bm25", 0.7), hit("gpt", 0.6)]}, "de")

    assert [s.note for s in chat.cited("RAG kombiniert Suche und Generierung [1][3].", sources)] == ["rag", "gpt"]
    assert len(chat.cited("Keine Belege.", sources)) == 3


def test_without_sources_the_model_is_not_asked():
    def generate(*args, **kwargs):
        raise AssertionError("the model must not be asked")

    answer = chat.ask("q", {"public": lambda: FakeStore([])}, embed=fake_embed, generate=generate)

    assert answer.sources == [] and "nichts gefunden" in answer.answer


def test_the_chat_endpoint_answers_with_sources(tmp_path):
    indices = Indices({"public": lambda: "public driver", "private": lambda: "private driver"})
    calls = []

    def ask(question, stores, language, history):
        calls.append((question, sorted(stores), language, history))
        source = chat.Source(1, "rag", "RAG", "Overview", "public", "text", 0.8)
        return chat.ChatAnswer(answer="RAG [1]", sources=[source], facts=[], unavailable=["private"])

    client = TestClient(create_app(tmp_path, indices=indices, ask=ask))
    history = [{"role": "user", "content": "Was ist BM25?"}, {"role": "assistant", "content": "Ein Ranking [1]."}]
    response = client.post("/api/chat", json={"question": "Was ist RAG?", "scope": "public", "history": history})

    assert response.status_code == 200
    assert response.json()["sources"][0]["note"] == "rag"
    assert response.json()["unavailable"] == ["private"]
    assert calls == [("Was ist RAG?", ["public"], "de", [chat.Turn("user", "Was ist BM25?"), chat.Turn("assistant", "Ein Ranking [1].")])]


def test_a_failing_model_is_reported_as_unavailable(tmp_path):
    def ask(question, stores, language, history):
        raise RuntimeError("Ollama is not running")

    client = TestClient(create_app(tmp_path, indices=Indices({}), ask=ask))

    response = client.post("/api/chat", json={"question": "Was ist RAG?"})

    assert response.status_code == 503 and "Ollama is not running" in response.json()["detail"]


def test_one_note_fills_at_most_two_source_slots():
    hits = [hit("prompt-injection", 0.9 - i / 100, heading=f"Section {i}") for i in range(4)] + [hit("mcp", 0.8)]

    sources = chat.merge_hits({"public": hits}, "de")

    assert [s.note for s in sources] == ["prompt-injection", "prompt-injection", "mcp"]


def test_a_follow_up_is_searched_as_a_standalone_question():
    prompts, searched = [], []

    def generate(prompt, **kwargs):
        prompts.append(prompt)
        return "<think>plan</think>Wie verhindert man Prompt Injection?" if len(prompts) == 1 else "<think>x</think>Durch Trennung [1]."

    def embed(texts):
        searched.extend(texts)
        return fake_embed(texts)

    history = [chat.Turn("user", "Was ist Prompt Injection?"), chat.Turn("assistant", "Ein Angriff [1].")]
    answer = chat.ask("und wie verhindert man das?", {"public": lambda: FakeStore([hit("prompt-injection", 0.9)])},
                      embed=embed, generate=generate, history=history)

    assert "Wie verhindert man Prompt Injection?" in searched[0]
    assert "User: Was ist Prompt Injection?\nAssistant: Ein Angriff [1]." in prompts[1]
    assert prompts[1].endswith("## Question\nund wie verhindert man das?")
    assert answer.answer == "Durch Trennung [1]."


def test_a_first_question_is_not_rewritten():
    assert chat.standalone_question("Was ist RAG?", [], generate=None) == "Was ist RAG?"


def test_an_unchanged_follow_up_is_searched_with_the_previous_question():
    history = [chat.Turn("user", "Was ist Prompt Injection?"), chat.Turn("assistant", "Ein Angriff [1].")]

    searched = chat.standalone_question("Und wie schützt man sich?", history, generate=lambda prompt, **kwargs: "Und wie schützt man sich?")

    assert searched == "Was ist Prompt Injection? Und wie schützt man sich?"


def test_a_hit_on_a_round_brings_the_applications_retro_along():
    round_slug = "private-companies-acme-gmbh-ml-engineer-round-1-round"
    retro = hit("private-companies-acme-gmbh-ml-engineer-round-1-retro", 0.0, text="Questions asked: RAG", visibility="private")
    private = FakeStore([hit(round_slug, 0.85, visibility="private"), hit("private-notes-star-stories", 0.8, visibility="private")],
                        round_passages=[retro])

    retrieval = chat.retrieve("Was wurde ich gefragt?", {"private": lambda: private}, embed=fake_embed)

    assert private.prefix_requests == [(["private-companies-acme-gmbh-ml-engineer-"], [round_slug, "private-notes-star-stories"])]
    assert [(s.number, s.note) for s in retrieval.sources][-1] == (3, retro["note"])
