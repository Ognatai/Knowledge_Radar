from app.agents import eurlex, gesetze

EURLEX_PAGE = """<html><body>
<div id="cpt_I"><p class="title-division-1">CHAPTER I</p><p class="title-division-2"><span>GENERAL PROVISIONS</span></p>
<div class="eli-subdivision" id="art_1"><p class="title-article-norm">Article 1</p>
<div class="eli-title"><p class="stitle-article-norm">Subject matter'</p></div>
<p>1. This Regulation lays down rules.</p></div></div>
<div id="cpt_III"><p class="title-division-1">CHAPTER III</p><p class="title-division-2">HIGH-RISK</p>
<div id="cpt_III.sct_2"><p class="title-division-1">SECTION 2</p><p class="title-division-2">Requirements</p>
<div class="eli-subdivision" id="art_9"><p class="title-article-norm">Article 9</p>
<div class="eli-title"><p class="stitle-article-norm">Risk management system</p></div>
<p>1. A system shall be established.</p></div></div></div>
<div id="anx_I"><p>ANNEX I</p></div>
</body></html>"""

GESETZ_XML = """<?xml version="1.0" encoding="UTF-8"?>
<dokumente><norm><metadaten><jurabk>BDSG 2018</jurabk><amtabk>BDSG</amtabk>
<ausfertigung-datum>2017-06-30</ausfertigung-datum>
<fundstelle typ="amtlich"><periodikum>BGBl I</periodikum><zitstelle>2017, 2097</zitstelle></fundstelle>
<langue>Bundesdatenschutzgesetz</langue>
<standangabe><standtyp>Stand</standtyp><standkommentar>Zuletzt geändert durch Art. 3 G v. 12.5.2026</standkommentar></standangabe>
</metadaten></norm>
<norm><metadaten><enbez>Inhaltsübersicht</enbez></metadaten></norm>
<norm><metadaten><gliederungseinheit><gliederungskennzahl>010</gliederungskennzahl><gliederungsbez>Teil 1</gliederungsbez><gliederungstitel>Gemeinsame Bestimmungen</gliederungstitel></gliederungseinheit></metadaten></norm>
<norm><metadaten><gliederungseinheit><gliederungskennzahl>010010</gliederungskennzahl><gliederungsbez>Kapitel 1</gliederungsbez><gliederungstitel>Anwendungsbereich</gliederungstitel></gliederungseinheit></metadaten></norm>
<norm><metadaten><enbez>§ 1</enbez><titel>Anwendungsbereich des Gesetzes</titel></metadaten>
<textdaten><text><Content><P>(1) Dieses Gesetz gilt.</P><P>(2) Ausnahmen.</P></Content></text></textdaten></norm>
<norm><metadaten><gliederungseinheit><gliederungskennzahl>020</gliederungskennzahl><gliederungsbez>Teil 2</gliederungsbez><gliederungstitel>Durchführung</gliederungstitel></gliederungseinheit></metadaten></norm>
<norm><metadaten><enbez>§ 26</enbez><titel>Beschäftigungsverhältnisse</titel></metadaten>
<textdaten><text><Content><P>(1) Daten von Beschäftigten.</P></Content></text></textdaten></norm>
</dokumente>"""


def test_eurlex_structure_has_chapters_sections_and_clean_titles():
    sections = eurlex.parse_structure(EURLEX_PAGE)

    assert [s.number for s in sections] == ["Article 1", "Article 9"]
    assert sections[0].title == "Subject matter"
    assert sections[0].text == "1. This Regulation lays down rules."
    assert [(h.label, h.title) for h in sections[1].path] == [("CHAPTER III", "HIGH-RISK"), ("SECTION 2", "Requirements")]
    assert sections[1].key == "9"


def test_gesetze_parses_metadata_structure_and_sections():
    law = gesetze.parse(GESETZ_XML.encode("utf-8"), "bdsg_2018")

    assert (law.abbreviation, law.title, law.enacted, law.citation) == (
        "BDSG", "Bundesdatenschutzgesetz", "2017-06-30", "BGBl I 2017, 2097",
    )
    assert law.status == ["Zuletzt geändert durch Art. 3 G v. 12.5.2026"]
    assert [s.number for s in law.sections] == ["§ 1", "§ 26"]
    assert law.sections[0].text == "(1) Dieses Gesetz gilt.\n(2) Ausnahmen."
    assert [h.label for h in law.sections[0].path] == ["Teil 1", "Kapitel 1"]
    assert [h.label for h in law.sections[1].path] == ["Teil 2"]
    assert law.url == "https://www.gesetze-im-internet.de/bdsg_2018/"


def test_gesetze_keeps_text_after_lists_in_order_and_joins_hyphenation():
    xml = GESETZ_XML.replace(
        "<titel>Beschäftigungsverhältnisse</titel>",
        "<titel>Tätigkeiten außerhalb der Anwendungs- bereiche; Bußgeld- und Strafverfahren</titel>",
    ).replace(
        "<P>(1) Daten von Beschäftigten.</P>",
        '<P>(1) Dienste, die <DL Type="arabic"><DT>1.</DT><DD><LA>A haben,</LA></DD>'
        "<DT>2.</DT><DD><LA>B haben,</LA></DD></DL>können anerkannt werden.</P>",
    )
    section = gesetze.parse(xml.encode("utf-8"), "bdsg_2018").sections[1]

    assert section.text == "(1) Dienste, die\n1.\nA haben,\n2.\nB haben,\nkönnen anerkannt werden."
    assert section.title == "Tätigkeiten außerhalb der Anwendungsbereiche; Bußgeld- und Strafverfahren"


FLAT_PAGE = """<html><body><p class="title-doc-first">RICHTLINIE 2002/58/EG</p>
<p class="title-article-norm">Artikel 1</p><p class="stitle-article-norm">Geltungsbereich</p>
<p>(1) Diese Richtlinie gilt.</p>
<p class="title-article-norm">Artikel 14a</p><p class="stitle-article-norm">Ausschussverfahren</p>
<p>(1) Die Kommission.</p>
<p class="title-annex">ANHANG</p><p>Anhangtext</p>
</body></html>"""


def test_eurlex_parses_older_format_without_article_containers():
    sections = eurlex.parse_structure(FLAT_PAGE)

    assert [(s.number, s.title, s.key) for s in sections] == [
        ("Artikel 1", "Geltungsbereich", "1"), ("Artikel 14a", "Ausschussverfahren", "14a"),
    ]
    assert sections[0].text == "(1) Diese Richtlinie gilt."
    assert "Anhangtext" not in sections[1].text


OJ_PAGE = """<html><body>
<div id="cpt_I"><p id="d1" class="oj-ti-section-1">CHAPTER I</p>
<div class="eli-title" id="cpt_I.tit_1"><p id="d2" class="oj-ti-section-2"><span class="oj-bold">GENERAL PROVISIONS</span></p></div>
<div class="eli-subdivision" id="art_1"><p id="d3" class="oj-ti-art">Article 1</p>
<div class="eli-title" id="art_1.tit_1"><p class="oj-sti-art">Subject matter</p></div>
<p class="oj-normal">1. This Regulation lays down rules.</p></div></div>
</body></html>"""

PARTS_PAGE = """<html><body>
<div id="prt_I"><p class="title-division-1">PART I</p><p class="title-division-2">FRAMEWORK</p>
<div id="prt_I.tis_I"><p class="title-division-1">TITLE I</p><p class="title-division-2">SCOPE</p>
<div id="prt_I.tis_I.cpt_I"><p class="title-division-1">CHAPTER I</p><p class="title-division-2">Definitions</p>
<div class="eli-subdivision" id="art_2"><p class="title-article-norm">Article 2</p>
<p class="stitle-article-norm">Definitions</p><p>For the purposes of this Directive.</p></div></div></div></div>
</body></html>"""


def test_official_journal_xhtml_is_parsed_after_class_mapping(tmp_path, monkeypatch):
    class Response:
        def __init__(self, body):
            self.body = body
        def read(self):
            return self.body.encode("utf-8")
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False

    monkeypatch.setattr(eurlex.urllib.request, "urlopen", lambda request, timeout: Response(OJ_PAGE))
    page = eurlex.fetch_cellar("32023R2854", "en", tmp_path)
    sections = eurlex.parse_structure(page)

    assert [(s.number, s.title, s.text) for s in sections] == [("Article 1", "Subject matter", "1. This Regulation lays down rules.")]
    assert [(h.label, h.title) for h in sections[0].path] == [("CHAPTER I", "GENERAL PROVISIONS")]


def test_parts_titles_and_chapters_nest():
    section = eurlex.parse_structure(PARTS_PAGE)[0]

    assert [(h.level, h.label) for h in section.path] == [(1, "PART I"), (2, "TITLE I"), (3, "CHAPTER I")]


TITLES_PAGE = """<html><body>
<div id="tis_II"><p class="title-division-1">TITLE II</p><p class="title-division-2">ENISA</p>
<div id="tis_II.cpt_III"><p class="title-division-1">CHAPTER III</p><p class="title-division-2">Organisation</p>
<div id="tis_II.cpt_III.sct_1"><p class="title-division-1">SECTION 1</p><p class="title-division-2">Board</p>
<div class="eli-subdivision" id="art_14"><p class="title-article-norm">Article 14</p>
<p class="stitle-article-norm">Composition</p><p>The Board is composed of members.</p></div></div></div></div>
</body></html>"""


def test_top_level_titles_nest_like_parts():
    # Consolidated texts with titles but no parts (e.g. the Cybersecurity Act) use tis_ containers.
    section = eurlex.parse_structure(TITLES_PAGE)[0]
    assert [(h.level, h.label, h.title) for h in section.path] == [
        (1, "TITLE II", "ENISA"), (2, "CHAPTER III", "Organisation"), (3, "SECTION 1", "Board")]
