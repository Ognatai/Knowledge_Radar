from app.backend.knowledge_radar.graph import load_graph
from app.backend.knowledge_radar.notes import DEFAULT_NOTES_DIRECTORY, REPOSITORY_ROOT, load_notes

GOLD_DIRECTORY = REPOSITORY_ROOT / "eval" / "gold"


def test_gold_set_is_valid_and_current():
    graph = load_graph(GOLD_DIRECTORY, load_notes(DEFAULT_NOTES_DIRECTORY), DEFAULT_NOTES_DIRECTORY)

    # A note changed after labelling: its gold labels must be reviewed again.
    assert graph.stale_extractions == []
    assert list((GOLD_DIRECTORY / "extractions").glob("*.yaml"))
