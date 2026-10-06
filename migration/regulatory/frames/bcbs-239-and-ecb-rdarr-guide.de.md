> **Wichtiger Hinweis:** Diese Seite ist eine LLM-generierte Zusammenfassung. Sie kann unvollständig, veraltet oder falsch sein. Sie ist keine Rechtsberatung und entfaltet keine rechtliche Wirkung; maßgeblich sind allein die vom Basler Ausschuss für Bankenaufsicht und von der Europäischen Zentralbank veröffentlichten Dokumente. Beide liegen nur auf Englisch vor; die deutschen Bezeichnungen und Zusammenfassungen auf dieser Seite sind nicht amtlich.

### TL;DR

BCBS 239 sind die 14 Grundsätze des Basler Ausschusses für die effektive Aggregation von Risikodaten und die Risikoberichterstattung (RDARR), veröffentlicht im Januar 2013 als Reaktion auf die Finanzkrise, in der viele Banken ihre Risikopositionen nicht schnell und genau zusammenführen konnten. Die Grundsätze betreffen Governance und IT-Infrastruktur, Genauigkeit, Vollständigkeit, Aktualität und Anpassungsfähigkeit der Risikodaten, die Qualität der Risikoberichte und die aufsichtliche Überprüfung. Der EZB-Leitfaden zur effektiven Aggregation von Risikodaten und Risikoberichterstattung vom Mai 2024 legt die Mindesterwartungen der EZB an die direkt beaufsichtigten Banken fest, mit Schwerpunkten auf der Verantwortung des Leitungsorgans, dem Anwendungsbereich, der Data Governance, einer integrierten Datenarchitektur, dem Datenqualitätsmanagement, zeitnaher Berichterstattung und Umsetzungsprogrammen.

### Eckdaten

| | |
| --- | --- |
| Fundstelle | Basler Ausschuss für Bankenaufsicht, Principles for effective risk data aggregation and risk reporting (BCBS 239), Januar 2013; EZB-Bankenaufsicht, Guide on effective risk data aggregation and risk reporting, Mai 2024 |
| Art und Geltung | internationaler Standard des Basler Ausschusses und aufsichtlicher Leitfaden der EZB; beide sind rechtlich nicht verbindlich, dienen der Aufsicht aber als Maßstab |
| Veröffentlicht | Januar 2013 (BCBS 239); Mai 2024 (EZB-Leitfaden) |
| Zuständige Behörden | die nationalen Aufsichtsbehörden; für bedeutende Institute im Euroraum die EZB im Einheitlichen Aufsichtsmechanismus |
| Zusammengefasste Fassung | veröffentlichte Fassungen; beide nur auf Englisch verfügbar |

### Anwendungsbereich

**Wer**: BCBS 239 gilt vor allem für global systemrelevante Banken (G-SIBs); der Basler Ausschuss empfiehlt nachdrücklich, die Grundsätze auch auf national systemrelevante Banken (D-SIBs) drei Jahre nach deren Einstufung anzuwenden. Der EZB-Leitfaden richtet sich an die von der EZB direkt beaufsichtigten bedeutenden Institute und nutzt die BCBS-239-Grundsätze als Maßstab bewährter Verfahren.

**Verhältnismäßigkeit**: Die Grundsätze können auf weitere Banken angewendet werden, verhältnismäßig zu Größe, Art und Komplexität ihrer Geschäfte.

**Rechtliche Verankerung in der EU**: Die Erwartungen konkretisieren die Anforderungen der [[crr-and-crd|CRD]] an Governance und Risikomanagement (Artikel 74, 76 und 88) in der Auslegung durch die [[eba-governance-and-outsourcing-guidelines|EBA-Leitlinien zur internen Governance]].

**Aufbau**: BCBS 239 gliedert die 14 Grundsätze in vier Teile: übergreifende Governance und Infrastruktur (Grundsätze 1–2), Fähigkeiten zur Aggregation von Risikodaten (3–6), Risikoberichterstattung (7–11) sowie aufsichtliche Überprüfung, Instrumente und Zusammenarbeit (12–14). Der EZB-Leitfaden enthält sieben aufsichtliche Erwartungen (Abschnitt 3) und den aufsichtlichen Ansatz (Abschnitt 4).

<!-- PROVISIONS -->

### Zeitplan

| Datum | Ereignis |
| --- | --- |
| Januar 2013 | Veröffentlichung von BCBS 239 |
| Januar 2016 | Frist für die 2011 oder 2012 eingestuften G-SIBs; später eingestufte G-SIBs haben drei Jahre ab Einstufung |
| Mai 2024 | Veröffentlichung des EZB-Leitfadens zur effektiven Aggregation von Risikodaten und Risikoberichterstattung |

### Durchsetzung und Sanktionen

- **Keine eigenen Sanktionen**: BCBS 239 und der EZB-Leitfaden sind rechtlich nicht verbindlich; sie beschreiben aufsichtliche Erwartungen.
- **Aufsichtliche Maßnahmen** (Grundsatz 13): Die Aufsichtsbehörden sollen wirksame und rechtzeitige Abhilfe verlangen und können verschiedene Instrumente nutzen, auch Maßnahmen der Säule 2 nach der [[crr-and-crd|CRD]].
- **Ansatz der EZB** (Abschnitt 4 des Leitfadens): gezieltere Aufsichtstätigkeiten und ein stärkerer Einsatz von Aufsichtsbefugnissen bei schwerwiegenden, lang anhaltenden Mängeln.

### Verhältnis zu anderen Rechtsakten

- **[[crr-and-crd|CRR und CRD]]**: Die RDARR-Erwartungen bauen auf den Anforderungen der CRD an solide Governance-Regelungen und Risikomanagement auf.
- **[[eba-governance-and-outsourcing-guidelines|EBA-Leitlinien zur internen Governance]]**: Der EZB-Leitfaden verweist für die Verantwortung des Leitungsorgans auf Titel II der EBA-Leitlinien.
- **[[marisk|MaRisk]]**: Für weniger bedeutende Institute in Deutschland greifen die MaRisk-Anforderungen an Datenqualität (AT 7.2) und Risikoberichterstattung (BT 2) dieselben Grundsätze auf.
- **[[dora|DORA]]**: Datenarchitektur und IT-Infrastruktur für die Aggregation von Risikodaten unterliegen auch den Anforderungen von DORA an das IKT-Risikomanagement.

### Bedeutung für die KI-Entwicklung

- **Datenqualität als Voraussetzung**: Genaue, vollständige und aktuelle Risikodaten (Grundsätze 3–6) sind auch Voraussetzung für verlässliche Modelle des maschinellen Lernens im Bankbetrieb; der EZB-Leitfaden bezieht Modelle ausdrücklich in den Anwendungsbereich der Datenarchitektur ein.
- **Automatisierung** (Grundsatz 3): Risikodaten sollen weitgehend automatisiert aggregiert werden, um Fehler zu vermeiden; das spricht für automatisierte Datenpipelines mit dokumentierten Kontrollen.
- **Datenherkunft und Metadaten** (EZB-Leitfaden Abschnitte 3.2 und 3.4): Datentaxonomien, ein Verzeichnis fachlicher Begriffe, ein Metadaten-Repository und die Abdeckung des gesamten Datenlebenszyklus unterstützen die Nachvollziehbarkeit, die auch für Trainings- und Eingabedaten von KI-Systemen nötig ist.
- **Ad-hoc-Auswertungen** (Grundsatz 6): Die Fähigkeit, aggregierte Risikodaten auf Abruf und auch in Krisen zu liefern, ist ein Anwendungsfall für KI-gestützte Analysen; die Ergebnisse müssen aber dieselben Anforderungen an Genauigkeit und Validierung erfüllen.
- **Berichterstattung** (Grundsätze 7–11): KI-erstellte Risikoberichte müssen genau, abgestimmt und validiert, klar und auf ihre Empfänger zugeschnitten sein.

### Amtliche Quellen

- [BCBS 239 – Principles for effective risk data aggregation and risk reporting (bis.org, Englisch)](https://www.bis.org/publ/bcbs239.htm)
- [EZB-Leitfaden zur effektiven Aggregation von Risikodaten und Risikoberichterstattung (bankingsupervision.europa.eu, Englisch)](https://www.bankingsupervision.europa.eu/ecb/pub/pdf/ssm.supervisory_guides240503_riskreporting.en.pdf)
