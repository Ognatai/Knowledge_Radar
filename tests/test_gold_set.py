from app.backend.knowledge_radar.graph import load_graph
from app.backend.knowledge_radar.notes import DEFAULT_NOTES_DIRECTORY, REPOSITORY_ROOT, load_notes

GOLD_DIRECTORY = REPOSITORY_ROOT / "eval" / "gold"


def test_gold_set_is_valid_and_current():
    graph = load_graph(GOLD_DIRECTORY, load_notes(DEFAULT_NOTES_DIRECTORY), DEFAULT_NOTES_DIRECTORY)

    # A note changed after labelling: its gold labels must be reviewed again.
    assert graph.stale_extractions == []
    assert list((GOLD_DIRECTORY / "extractions").glob("*.yaml"))


def test_split_covers_every_gold_note_exactly_once():
    import yaml

    split = yaml.safe_load((GOLD_DIRECTORY / "split.yaml").read_text(encoding="utf-8"))
    labelled = sorted(path.stem for path in (GOLD_DIRECTORY / "extractions").glob("*.yaml"))

    assert sorted(split["dev"] + split["test"]) == labelled
    assert not set(split["dev"]) & set(split["test"])
