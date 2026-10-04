import pytest

from app.backend.knowledge_radar.templates import check_template

SOURCE = "https://example.org/paper"


def technical(entity_type="Method", en_extra="", de_extra="", mechanism=None):
    en_mechanism, de_mechanism = mechanism or (
        "### How it works\n\n#### 1. Step\nText.\n",
        "### Funktionsweise\n\n#### 1. Schritt\nText.\n",
    )
    return f"""---
title_en: Example
title_de: Beispiel
entity_type: {entity_type}
sources:
  - {SOURCE}
---

## EN

> **Note:** LLM-generated summary.

### TL;DR
Text.

{en_mechanism}
### When to use it
Text.

### Strengths and limitations
Text.

### Comparison
Text.
{en_extra}
### Key takeaway
Text.

### Sources
- [Paper]({SOURCE})

## DE

> **Hinweis:** LLM-generierte Zusammenfassung.

### TL;DR
Text.

{de_mechanism}
### Wann einsetzen
Text.

### Stärken und Grenzen
Text.

### Vergleich
Text.
{de_extra}
### Merksatz
Text.

### Quellen
- [Paper]({SOURCE})
"""


def regulatory(frontmatter_extra=None):
    fields = {
        "jurisdiction": "EU",
        "instrument": "regulation",
        "status": "in-force",
        "official_reference": '"Regulation (EU) 2016/679"',
        "consolidated_version": "2016-05-04",
    }
    fields.update(frontmatter_extra or {})
    extra = "".join(f"{key}: {value}\n" for key, value in fields.items() if value is not None)
    sections_en = ["TL;DR", "Key facts", "Scope", "Chapter I — General", "Timeline",
                   "Enforcement and penalties", "Relationship to other acts",
                   "Relevance for AI development", "Official sources"]
    sections_de = ["TL;DR", "Eckdaten", "Anwendungsbereich", "Kapitel I – Allgemeines", "Zeitplan",
                   "Durchsetzung und Sanktionen", "Verhältnis zu anderen Rechtsakten",
                   "Bedeutung für die KI-Entwicklung", "Amtliche Quellen"]
    body_en = "".join(f"### {title}\nText.\n\n" for title in sections_en)
    body_de = "".join(f"### {title}\nText.\n\n" for title in sections_de)
    return f"""---
title_en: GDPR
title_de: DSGVO
entity_type: Regulation
{extra}sources:
  - {SOURCE}
---

## EN

> **Important notice:** LLM-generated summary, not legal advice.

{body_en}[Official Journal]({SOURCE})

## DE

> **Wichtiger Hinweis:** LLM-generierte Zusammenfassung, keine Rechtsberatung.

{body_de}[Amtsblatt]({SOURCE})
"""


def test_conforming_notes_pass():
    assert check_template(technical()) == []
    assert check_template(regulatory()) == []


def test_optional_technical_sections_are_allowed():
    note = technical(
        en_extra="\n### In practice\nText.\n\n### Regulatory context\nText.\n",
        de_extra="\n### In der Praxis\nText.\n\n### Regulatorischer Kontext\nText.\n",
    )
    assert check_template(note) == []


def test_technology_notes_use_core_concepts_and_common_usage():
    mechanism = (
        "### Core concepts\nText.\n\n### Common usage\nText.\n",
        "### Kernkonzepte\nText.\n\n### Typische Verwendung\nText.\n",
    )
    assert check_template(technical("Technology", mechanism=mechanism)) == []
    assert any("missing sections: Core concepts" in p for p in check_template(technical("Technology")))


@pytest.mark.parametrize(
    ("mutate", "expected"),
    [
        (lambda n: n.replace("> **Note:** LLM-generated summary.\n", ""), "EN: must open with the LLM notice"),
        (lambda n: n.replace("### TL;DR\nText.\n\n### How it works", "### How it works", 1),
         "EN: the first section must be '### TL;DR'"),
        (lambda n: n.replace("### Comparison\nText.\n", ""), "EN: missing sections: Comparison"),
        (lambda n: n.replace("### Vergleich\nText.\n", "### Verwandte Themen\n- x\n"), "DE: remove '### Verwandte Themen'"),
        (lambda n: n.replace("### Key takeaway\nText.\n", "### Background\nText.\n\n### Key takeaway\nText.\n"),
         "EN: sections not in the technical template: Background"),
        (lambda n: n.replace("#### 1. Schritt\nText.\n", ""), "EN and DE must have the same outline"),
        (lambda n: n.replace("- [Paper](https://example.org/paper)", "- Paper", 2), "source not cited in the text"),
    ],
)
def test_technical_violations_are_reported(mutate, expected):
    problems = check_template(mutate(technical()))

    assert any(expected in problem for problem in problems), problems


def test_section_order_is_enforced():
    note = technical().replace(
        "### When to use it\nText.\n\n### Strengths and limitations\nText.\n",
        "### Strengths and limitations\nText.\n\n### When to use it\nText.\n",
    )
    assert any("EN: sections must follow the order" in p for p in check_template(note))


@pytest.mark.parametrize(
    ("extra", "expected"),
    [
        ({"status": "valid"}, "'status' must be one of"),
        ({"instrument": None}, "'instrument' must be one of"),
        ({"official_reference": None}, "'official_reference' is required"),
        ({"consolidated_version": '"recent"'}, "'consolidated_version' must be a date"),
    ],
)
def test_regulation_frontmatter_is_checked(extra, expected):
    assert any(expected in p for p in check_template(regulatory(extra)))


def test_regulatory_sections_are_required():
    note = regulatory().replace("### Timeline\nText.\n\n", "")

    assert any("EN: missing sections: Timeline" in p for p in check_template(note))


def test_code_blocks_are_not_headings():
    note = technical().replace("#### 1. Step\nText.\n", "#### 1. Step\n```text\n### not a heading\n```\n")

    assert check_template(note) == []
