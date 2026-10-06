> **Wichtiger Hinweis:** Diese Seite ist eine LLM-generierte Zusammenfassung. Sie kann unvollständig, veraltet oder falsch sein. Sie ist keine Rechtsberatung und entfaltet keine rechtliche Wirkung; verbindlich ist allein der im Bundesgesetzblatt veröffentlichte Text.

### TL;DR

Das Gesetz zum Schutz von Geschäftsgeheimnissen (GeschGehG) setzt die EU-Richtlinie (EU) 2016/943 über den Schutz vertraulichen Know-hows um. Geschützt ist eine Information nur, wenn sie nicht allgemein bekannt und deshalb wirtschaftlich wertvoll ist, an ihrer Geheimhaltung ein berechtigtes Interesse besteht und der Inhaber angemessene Geheimhaltungsmaßnahmen getroffen hat (§ 2). Das Gesetz legt fest, welche Handlungen erlaubt sind (etwa eigenständige Entwicklung und Reverse Engineering, § 3) und welche verboten (§ 4), nimmt Whistleblowing und Journalismus aus (§ 5) und gibt dem Inhaber Ansprüche auf Unterlassung, Vernichtung, Rückruf, Auskunft und Schadensersatz. Für Gerichtsverfahren gibt es besondere Geheimhaltungsregeln; vorsätzliche Verletzungen sind strafbar.

### Eckdaten

| | |
| --- | --- |
| Fundstelle | Gesetz zum Schutz von Geschäftsgeheimnissen, BGBl. I 2019, 466 |
| Art und Geltung | deutsches Bundesgesetz; setzt die Richtlinie (EU) 2016/943 um |
| Ausgefertigt | 18. April 2019 |
| Inkrafttreten | 26. April 2019; ersetzt die Strafvorschriften der §§ 17 bis 19 UWG |
| Zuständige Behörden | keine Aufsichtsbehörde; Durchsetzung über die Zivilgerichte (ausschließlich Landgerichte, § 15) und die Strafverfolgung (§ 23) |
| Zusammengefasste Fassung | Fassung vom 18. April 2019; das Gesetz wurde seither nicht geändert |

### Anwendungsbereich

**Was** (§ 2 Nr. 1): Geschäftsgeheimnisse aller Art, etwa technisches Know-how, Rezepturen, Quellcode, Kundenlisten, Geschäftsstrategien oder Daten, sofern die drei Voraussetzungen erfüllt sind. Ohne angemessene Geheimhaltungsmaßnahmen (technisch, organisatorisch, vertraglich) gibt es keinen Schutz.

**Wer**: Inhaber ist, wer die rechtmäßige Kontrolle über das Geschäftsgeheimnis hat (§ 2 Nr. 2); Ansprüche richten sich gegen den Rechtsverletzer (§ 2 Nr. 3) und unter Umständen gegen den Inhaber des Unternehmens, für das er arbeitet (§ 12).

**Vorrang und Abgrenzung** (§ 1): Öffentlich-rechtliche Geheimhaltungsvorschriften gehen vor; Meinungs- und Pressefreiheit, Tarifautonomie, Arbeitnehmerrechte und der berufsrechtliche Geheimnisschutz nach § 203 StGB bleiben unberührt.

**Aufbau**: vier Abschnitte: Allgemeines (§§ 1–5), Ansprüche bei Rechtsverletzungen (§§ 6–14), Verfahren in Geschäftsgeheimnisstreitsachen (§§ 15–22) und Strafvorschriften (§ 23).

<!-- PROVISIONS -->

### Zeitplan

| Datum | Ereignis |
| --- | --- |
| 8. Juni 2016 | Verabschiedung der Richtlinie (EU) 2016/943; Umsetzungsfrist bis 9. Juni 2018 |
| 18. April 2019 | Ausfertigung des GeschGehG |
| 26. April 2019 | Inkrafttreten |

### Durchsetzung und Sanktionen

- **Zivilrechtliche Ansprüche** (§§ 6–13): Beseitigung und Unterlassung, Vernichtung, Herausgabe, Rückruf und Rücknahme rechtsverletzender Produkte vom Markt, Auskunft und Schadensersatz, berechnet nach konkretem Schaden, Verletzergewinn oder angemessener Lizenzgebühr; Ausschluss bei Unverhältnismäßigkeit (§ 9) und Missbrauchsverbot (§ 14).
- **Geheimnisschutz im Prozess** (§§ 16–20): Das Gericht kann Informationen als geheimhaltungsbedürftig einstufen und den Zugang beschränken; Verstöße kosten Ordnungsgeld bis **100.000 Euro** oder Ordnungshaft bis sechs Monate (§ 17).
- **Straftat** (§ 23): Freiheitsstrafe bis zu **drei Jahren** oder Geldstrafe, bei gewerbsmäßigem Handeln oder Nutzung im Ausland bis zu **fünf Jahren**; der Versuch ist strafbar, verfolgt wird grundsätzlich nur auf Antrag.

### Verhältnis zu anderen Rechtsakten

- **[[data-act|Data Act]]**: Bei Pflichten zur Datenweitergabe sind Geschäftsgeheimnisse durch Vertraulichkeitsmaßnahmen zu wahren; Dateninhaber können die Weitergabe in Ausnahmefällen verweigern.
- **[[eu-ai-act|EU AI Act]]**: Die Behörden müssen Geschäftsgeheimnisse vertraulich behandeln; die Zusammenfassung der Trainingsdaten von KI-Modellen mit allgemeinem Verwendungszweck berücksichtigt das Interesse am Schutz von Geschäftsgeheimnissen.
- **[[gdpr|DSGVO]]**: Auskunftsrechte betroffener Personen dürfen Rechte anderer nicht beeinträchtigen, darunter Geschäftsgeheimnisse; umgekehrt rechtfertigt ein Geschäftsgeheimnis keine vollständige Verweigerung der Auskunft.
- **[[copyright-and-ai-training-data|Urheberrecht und KI-Trainingsdaten]]**: Urheberrecht schützt Werke unabhängig von Geheimhaltung; das GeschGehG schützt auch nicht urheberrechtsfähige Informationen, aber nur, solange sie geheim gehalten werden.

### Bedeutung für die KI-Entwicklung

- **Modelle, Gewichte und Trainingsdaten als Geschäftsgeheimnisse** (§ 2 Nr. 1): Modellgewichte, Trainingsdatensätze, Architekturdetails oder System-Prompts können geschützt sein, wenn sie nicht allgemein bekannt sind und angemessen gesichert werden, etwa durch Zugriffsbeschränkungen und Vertraulichkeitsvereinbarungen. Mit der Veröffentlichung als Open Source entfällt der Schutz.
- **Reverse Engineering** (§ 3 Abs. 1 Nr. 2): Das Untersuchen und Testen öffentlich verfügbarer Produkte ist erlaubt; bei rechtmäßig besessenen Produkten nur, wenn keine Pflicht zur Beschränkung besteht. Nutzungsbedingungen, die etwa das Extrahieren von Modellen über eine Schnittstelle untersagen, können deshalb entscheidend sein.
- **Rechtsverletzende Produkte** (§ 2 Nr. 4, § 7): Ein KI-Modell oder Produkt, dessen Konzeption oder Funktionsweise in erheblichem Umfang auf einem rechtswidrig erlangten Geschäftsgeheimnis beruht, kann Ansprüchen auf Rückruf, Vernichtung und Rücknahme vom Markt unterliegen.
- **Eingaben in externe KI-Dienste**: Geben Beschäftigte vertrauliche Informationen in externe KI-Werkzeuge ein, kann das gegen Geheimhaltungspflichten verstoßen und die angemessenen Geheimhaltungsmaßnahmen in Frage stellen; Unternehmen regeln das deshalb in Richtlinien und Verträgen.
- **Whistleblowing** (§ 5 Nr. 2): Die Offenlegung von Geschäftsgeheimnissen zur Aufdeckung rechtswidriger Praktiken, auch beim Training oder Einsatz von KI-Systemen, kann gerechtfertigt sein.

### Amtliche Quellen

- [GeschGehG auf gesetze-im-internet.de](https://www.gesetze-im-internet.de/geschgehg/)
