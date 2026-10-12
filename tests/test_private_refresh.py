"""The private refresh: what the user needs first comes first, and the user goes first."""

import threading
from types import SimpleNamespace

from app.agents import private_refresh
from app.agents.private_refresh import READY, Foreground, Refresher


def test_index_and_requirements_come_before_the_extraction(monkeypatch, tmp_path):
    steps = []
    monkeypatch.setattr(private_refresh, "configured_notes_directory", lambda: tmp_path)
    monkeypatch.setattr(private_refresh, "load_notes", lambda directory: [])
    monkeypatch.setattr(private_refresh, "load_graph", lambda *args: SimpleNamespace(entities={}))
    monkeypatch.setattr(private_refresh, "load_documents", lambda root: [SimpleNamespace(kind="job_posting")])
    monkeypatch.setattr(private_refresh, "known_entities", lambda root, entities: {})
    monkeypatch.setattr(private_refresh, "ingest", lambda root, entities: steps.append("structure") or (SimpleNamespace(entities=[], relations=[]), None))
    monkeypatch.setattr(private_refresh, "update_private_index",
                        lambda *args, **kwargs: steps.append("index") or SimpleNamespace(embedded=[], deleted=[]))
    monkeypatch.setattr(private_refresh, "extract_requirements_all", lambda *args, **kwargs: steps.append("requirements"))
    monkeypatch.setattr(private_refresh, "topics_graph", lambda *args, **kwargs: steps.append("topics"))
    monkeypatch.setattr(private_refresh, "extract_free_text", lambda *args, **kwargs: steps.append("extraction"))
    monkeypatch.setattr(private_refresh, "Neo4jStore", lambda driver, visibility: None)

    def research(root, log):
        steps.append("research")

    log = []
    private_refresh.refresh(tmp_path, lambda: SimpleNamespace(close=lambda: None), log=log.append, research=research,
                            pause=lambda: None)
    local = [step for step in steps if step != "research"]
    assert local == ["structure", "index", "requirements", "topics", "extraction", "index"]
    assert "research" in steps and READY in log
    assert steps.index("research") < len(steps) - 1  # indexed in the last step


def test_ready_is_reported_before_the_run_ends():
    release = threading.Event()

    def run(log):
        log("Structure: 3 entities")
        log(READY)
        release.wait(5)

    refresher = Refresher(run)
    refresher.request()
    for _ in range(100):
        if refresher.status.ready:
            break
        threading.Event().wait(0.02)
    assert refresher.status.ready and refresher.status.state == "running"
    assert READY not in refresher.status.log
    release.set()
    refresher.thread.join(5)


def test_background_work_waits_while_the_user_is_served():
    foreground, order = Foreground(), []
    with foreground:
        waiter = threading.Thread(target=lambda: (foreground.wait_idle(5), order.append("background")))
        waiter.start()
        threading.Event().wait(0.1)
        order.append("user")
    waiter.join(5)
    assert order == ["user", "background"]
