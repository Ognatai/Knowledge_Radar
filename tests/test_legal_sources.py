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
