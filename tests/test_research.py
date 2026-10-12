"""Company and interviewer research with Claude: only names leave, within a monthly cap."""

import datetime as dt
from types import SimpleNamespace

import pytest
import yaml

from app.backend.knowledge_radar import prep, research
from app.backend.knowledge_radar.interviews import Interviewer, applications, create_application, create_round
from app.backend.knowledge_radar.private_repo import load_documents

TODAY = lambda: dt.date(2026, 10, 12)  # noqa: E731


@pytest.fixture
def root(tmp_path):
    root = tmp_path / "private"
    create_application(root, company_name="ACME GmbH", role_title="ML Engineer", posting_text="Secret posting text.",
                       round_notes="Secret round notes.", interviewers=[Interviewer("Jane Doe", "Head of Data Science", "NLP")],
                       today=TODAY)
    create_round(root, company="acme-gmbh", role="ml-engineer", interviewers=[Interviewer("Jane Doe"), Interviewer("John Roe", "CTO")])
    return root


def finding(text="### Role\nLeads the NLP team.", cost=0.30):
    return research.Finding(text, [{"title": "Team page", "url": "https://acme.example/team"}], cost, "claude-opus-5-5", 2)


def test_the_company_and_each_interviewer_are_pending_once(root):
    lookups = research.pending(root)
    assert [(lookup.kind, lookup.person) for lookup in lookups] == [("company", ""), ("person", "Jane Doe"), ("person", "John Roe")]


def test_only_names_leave_the_machine(root):
    queries = [lookup.query for lookup in research.pending(root)]
    assert queries == ["Company: ACME GmbH", "Person: Jane Doe\nAt company: ACME GmbH", "Person: John Roe\nAt company: ACME GmbH"]
    assert not any("Secret" in query or "Head of Data Science" in query or "CTO" in query for query in queries)


def test_findings_are_written_once_and_spend_is_recorded(root):
    asked = []
    run = research.Research(ask=lambda lookup: asked.append(lookup) or finding(), today=TODAY)
    run(root, log=lambda line: None)
    person = (root / "companies/acme-gmbh/_research/jane-doe.md").read_text(encoding="utf-8")
    assert "name: Jane Doe" in person and "Leads the NLP team." in person and "https://acme.example/team" in person
    assert (root / "companies/acme-gmbh/_research/company.md").is_file()
    spend = yaml.safe_load((root / research.SPEND_FILE).read_text(encoding="utf-8"))["lookups"]
    assert [entry["kind"] for entry in spend] == ["company", "person", "person"]
    assert "Jane" not in (root / research.SPEND_FILE).read_text(encoding="utf-8")

    run(root, log=lambda line: None)
    assert len(asked) == 3


def test_lookups_stop_at_the_monthly_cap(root):
    (root / research.SPEND_FILE).write_text(yaml.safe_dump({"lookups": [
        {"date": "2026-10-01", "kind": "company", "cost_usd": 2.00},
        {"date": "2026-09-30", "kind": "company", "cost_usd": 2.90},
    ]}), encoding="utf-8")
    asked, lines = [], []
    research.Research(ask=lambda lookup: asked.append(lookup) or finding(cost=0.30), today=TODAY)(root, log=lines.append)
    # 2.00 + 0.75 reserve fits once (then 2.30 spent), not twice.
    assert len(asked) == 1
    assert sum("monthly budget used" in line for line in lines) == 2


def test_a_failed_lookup_is_retried_and_a_missing_answer_is_not(root):
    def fail(lookup):
        raise research.ResearchError("overloaded")

    research.Research(ask=fail, today=TODAY)(root, log=lambda line: None)
    assert research.pending(root) and not (root / research.SPEND_FILE).exists()

    refused = research.Finding("", [], 0.05, "claude-opus-5-5", refused=True)
    research.Research(ask=lambda lookup: refused, today=TODAY)(root, log=lambda line: None)
    assert research.pending(root) == []
    assert research.NO_ANSWER in (root / "companies/acme-gmbh/_research/john-roe.md").read_text(encoding="utf-8")


def test_research_files_are_documents_but_no_role(root):
    research.Research(ask=lambda lookup: finding(), today=TODAY)(root, log=lambda line: None)
    kinds = {document.id: document.kind for document in load_documents(root)}
    assert kinds["companies/acme-gmbh/_research/jane-doe"] == "research"
    assert [a.role for a in applications(root)] == ["ml-engineer"]


def test_prep_reads_the_research(root):
    research.Research(ask=lambda lookup: finding(f"### About\n{lookup.person or 'the company'} facts."), today=TODAY)(
        root, log=lambda line: None)
    context = prep.gather(root, "acme-gmbh", "ml-engineer", 2)
    assert context.company_research.endswith("the company facts.")
    assert [p.get("background", "").endswith(f"{p['name']} facts.") for p in context.interviewers] == [True, True]
    assert "<research>" in prep._context_block(context)


def test_cost_counts_tokens_cache_and_searches():
    usage = SimpleNamespace(input_tokens=10_000, output_tokens=2_000, cache_creation_input_tokens=0, cache_read_input_tokens=0,
                            server_tool_use=SimpleNamespace(web_search_requests=3))
    assert research.cost(usage, "claude-opus-5-5") == pytest.approx(0.04 + 0.04 + 0.03)
    # An unknown (fallback) model is priced like the most expensive one listed.
    assert research.cost(usage, "claude-other") == pytest.approx(0.05 + 0.05 + 0.03)


class FakeClient:
    def __init__(self, responses):
        self.responses = list(responses)
        self.requests = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self.create))

    def create(self, **request):
        self.requests.append(request)
        return self.responses.pop(0)


def response(stop_reason, content):
    usage = SimpleNamespace(input_tokens=1000, output_tokens=100, cache_creation_input_tokens=0, cache_read_input_tokens=0,
                            server_tool_use=SimpleNamespace(web_search_requests=1))
    return SimpleNamespace(stop_reason=stop_reason, content=content, usage=usage, model="claude-opus-5-5")


def test_a_paused_search_is_resumed_and_citations_become_sources():
    citation = SimpleNamespace(url="https://acme.example", title="ACME")
    paused = response("pause_turn", [SimpleNamespace(type="server_tool_use")])
    done = response("end_turn", [SimpleNamespace(type="text", text="ACME builds ", citations=[citation]),
                                 SimpleNamespace(type="text", text="robots.", citations=[citation])])
    client = FakeClient([paused, done])
    result = research.ask_claude(research.Lookup("company", "acme-gmbh", "ACME GmbH"), client=client)
    assert result.text == "ACME builds robots."
    assert result.sources == [{"title": "ACME", "url": "https://acme.example"}]
    assert result.searches == 2
    assert client.requests[1]["messages"][1] == {"role": "assistant", "content": paused.content}
    assert client.requests[0]["messages"] == [{"role": "user", "content": "Company: ACME GmbH"}]
    assert [tool["type"] for tool in client.requests[0]["tools"]] == ["web_search_20260209"]


def test_only_the_own_key_switches_research_on(monkeypatch):
    monkeypatch.delenv(research.KEY_VARIABLE, raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "another tool's key")
    assert research.api_key(lambda service, user: None) is None
    assert research.api_key(lambda service, user: "stored") == "stored"
    monkeypatch.setenv(research.KEY_VARIABLE, "key")
    assert research.api_key(lambda service, user: None) == "key"
