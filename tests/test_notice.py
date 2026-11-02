from app.agents.monitoring.notice import build_notice

SUCCESS_LOG = "\ufeff" + """2026-11-01 02:00:01  Monitoring run started in C:\\repo.
2026-11-01 02:00:06  === validate notes ===
2026-11-01 02:00:10  Validated 276 public note(s) in C:\\repo\\public\\notes and the graph (906 entities, 1200 relations).
2026-11-01 02:00:10  === update index ===
2026-11-01 02:00:15  Updated index: 2 notes embedded, 1 removed.
2026-11-01 02:00:15  === update private repo ===
2026-11-01 02:00:20  Structure rebuilt: 0 entities, 3 open gaps -> C:\\private\\graph\\structure.yaml
2026-11-01 02:00:20  === fetch sources ===
2026-11-01 02:08:54     5  Hugging Face Daily Papers
2026-11-01 02:08:54  Error: Semantic Scholar (dense retrieval): HTTP Error 429:
2026-11-01 02:08:54  Error: Anthropic (YouTube): HTTP Error 404: Not Found
2026-11-01 02:08:54  11 new findings -> C:\\repo\\findings.jsonl
2026-11-01 02:08:54  === assess relevance ===
2026-11-01 02:10:13  [1/11] duplicate  4 Work Agents -> agentic-ai
2026-11-01 02:10:33  6 irrelevant, 3 duplicate, 2 update, 0 new_topic
2026-11-01 02:10:33  Error: a finding the model could not read
2026-11-01 02:10:33  === write drafts ===
2026-11-01 02:10:34  Checking bm25 ...
2026-11-01 02:10:35  Checking gpt ...
2026-11-01 02:10:36  Drafts: C:\\repo\\drafts
2026-11-01 02:10:36  === propose inbox ===
2026-11-01 02:10:39  INBOX: inbox/2026-11-01_020020
2026-11-01 02:10:39  === drafts on local branch proposals/2026-11-01_020020 ===
2026-11-01 02:10:39  SUMMARY: 11 new findings; proposals: 2 update; 2 drafts to review on branch proposals/2026-11-01_020020.
2026-11-01 02:10:39  Monitoring run finished successfully.
"""


def test_a_successful_run_lists_every_step_the_source_errors_and_the_drafts():
    notice = build_notice(SUCCESS_LOG, "C:\\repo\\run.log")

    assert notice.title == "Knowledge Radar: Weekly Run erfolgreich"
    assert not notice.failed and notice.log == "C:\\repo\\run.log"
    assert notice.message.splitlines() == [
        "Sonntag, 01.11.2026, 02:00–02:10 Uhr",
        "",
        "✓  Notes geprüft: 276 Notes, 906 Entitäten, 1200 Relationen",
        "✓  Index aktualisiert: 2 Notes neu eingebettet, 1 entfernt",
        "✓  Privates Repo aktualisiert: 3 offene Lücken aus Retros",
        "✓  Quellen abgerufen: 11 neue Funde",
        "✓  Relevanz bewertet: 6 irrelevant, 3 schon abgedeckt, 2 Ergänzung",
        "✓  Entwürfe geschrieben: 2 Entwürfe",
        "✓  Private Inbox: neue Funde auf Branch inbox/2026-11-01_020020",
        "",
        "Quellenfehler (2):",
        "   •  Semantic Scholar (dense retrieval): HTTP Error 429",
        "   •  Anthropic (YouTube): HTTP Error 404: Not Found",
        "",
        "Entwürfe warten auf das Review: Branch proposals/2026-11-01_020020.",
    ]


def test_a_failed_required_step_is_marked_and_the_later_steps_did_not_run():
    log = """2026-11-08 02:00:01  Monitoring run started in C:\\repo.
2026-11-08 02:00:06  === validate notes ===
2026-11-08 02:00:10  Validated 276 public note(s) in C:\\repo and the graph (906 entities, 1200 relations).
2026-11-08 02:00:10  === update index ===
2026-11-08 02:00:12  Neo4j is not reachable.
2026-11-08 02:00:12  === update index exited with 1 ===
2026-11-08 02:00:12  SUMMARY: Step 'update index' failed; see the log.
2026-11-08 02:00:12  Monitoring run FAILED: Step 'update index' failed; see the log.
"""
    notice = build_notice(log, "run.log")

    assert notice.failed and notice.title == "Knowledge Radar: Weekly Run fehlgeschlagen"
    lines = notice.message.splitlines()
    assert "✗  Index aktualisiert: fehlgeschlagen (Exit-Code 1)" in lines
    assert "–  Quellen abgerufen: nicht gelaufen" in lines
    assert lines[-1] == "Fehler: Step 'update index' failed; see the log."


def test_a_run_that_failed_before_the_pipeline_still_gets_a_notice():
    log = """2026-11-08 02:00:01  Monitoring run started in C:\\repo.
2026-11-08 02:05:01  Monitoring run FAILED: Docker did not become ready within 300 seconds.
"""
    notice = build_notice(log, "run.log")

    assert notice.failed
    assert notice.message.splitlines()[2] == "–  Notes geprüft: nicht gelaufen"
    assert notice.message.endswith("Fehler: Docker did not become ready within 300 seconds.")


def test_many_source_errors_are_cut_short():
    errors = "".join(f"2026-11-01 02:08:54  Error: Feed {n}: HTTP Error 503\n" for n in range(15))
    log = "2026-11-01 02:00:20  === fetch sources ===\n" + errors + "2026-11-01 02:10:39  Monitoring run finished successfully.\n"

    message = build_notice(log, "run.log").message

    assert "Quellenfehler (15):" in message
    assert "   •  Feed 11: HTTP Error 503" in message and "Feed 12:" not in message
    assert "   •  … und 3 weitere (siehe Log)" in message
