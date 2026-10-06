---
title_en: Information Security and Control Systems in Banking
title_de: Informationssicherheit und Kontrollsysteme im Bankumfeld
entity_type: Concept
sources:
- https://www.bundesbank.de/de/aufgaben/bankenaufsicht/einzelaspekte/risikomanagement/bait-dora-598580
- https://eur-lex.europa.eu/eli/reg/2022/2554/oj
- https://www.bafin.de/SharedDocs/Downloads/DE/Rundschreiben/dl_rs_0626_9_marisk.html
- https://www.gesetze-im-internet.de/kredwg/__25a.html
- https://www.eba.europa.eu/activities/single-rulebook/regulatory-activities/internal-governance/guidelines-internal-governance-under-crd
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

German banks organise information security and internal control on the basis of § 25a of the [[kwg|KWG]], which requires a proper business organisation with an internal control system and internal audit. [[marisk|MaRisk]] specifies the internal control system, and the three lines of defence separate business lines, independent control functions and internal audit. For IT and information security, the BaFin circular BAIT used to set the details; since 17 January 2025, [[dora|DORA]] governs ICT risk management for institutions within its scope, and the BAIT will be repealed at the end of 2026.

### How it works

Several layers of rules build on each other: the statutory duty of a proper business organisation, its specification in MaRisk, the three lines of defence as the organising principle of control, and the directly applicable ICT risk management requirements of DORA, including the information security policy and access control.

```text
1. § 25a KWG: proper business organisation
▼
2. MaRisk: internal control system
▼
3. Three lines of defence
▼
4. DORA: ICT risk management framework
▼
5. DORA: information security policy and access control
```

#### 1. Legal basis: proper business organisation

§ 25a KWG requires institutions to have a proper business organisation that ensures compliance with legal requirements, including appropriate and effective risk management with strategies, procedures to ensure risk-bearing capacity, internal control procedures with an internal control system and an internal audit function, and contingency management, in particular for IT systems (§ 25a KWG). The BaFin circular MaRisk specifies these requirements for institutions that are not directly supervised by the European Central Bank (MaRisk (2026)). § 25a KWG is also the legal basis of the BAIT, the circular with IT requirements for banks (Bundesbank, BAIT / DORA).

#### 2. The internal control system

Under MaRisk, the internal control system comprises rules on organisational structure and processes, risk management and risk control processes, a risk control function and a compliance function (AT 4.3, MaRisk (2026)). Incompatible activities must be carried out by different staff (AT 4.3.1), and the risk control function must be separated, up to and including management level, from the units that initiate or conclude business (AT 4.4.1). Every institution needs an internal audit function with full and unrestricted rights to information (AT 4.4.3). Technical and organisational resources must match the business activities and risk situation, with effective processes to ensure data quality (AT 7.2), and activities and processes that constitute critical or important functions require a contingency plan (AT 7.3).

#### 3. Three lines of defence

The EBA guidelines on internal governance follow the three lines of defence model: the business lines take and manage the risks they incur (first line), the risk management and compliance functions monitor them independently (second line), and the internal audit function reviews the whole system independently (third line) (EBA internal governance guidelines (2021)). Internal control functions must be independent of the business they control, adequately resourced and led by heads who can address the management body in its supervisory function; internal audit must not be combined with another control function. DORA applies the same principle to ICT risk: financial entities other than microenterprises must ensure appropriate segregation and independence of ICT risk management, control and internal audit functions according to the three lines of defence model or an internal risk management and control model (Art. 6(4), DORA (2022)).

#### 4. ICT risk management under DORA

Under DORA, the management body defines, approves and oversees the ICT risk management framework, is responsible for its implementation and bears ultimate responsibility for ICT risk (Art. 5(2), DORA (2022)). Financial entities other than microenterprises assign the management and oversight of ICT risk to a control function with an appropriate level of independence (Art. 6(4)). The ICT risk management framework must be documented and reviewed at least once a year, and upon major ICT-related incidents (Art. 6(5)).

#### 5. Information security policy and access control

As part of the ICT risk management framework, financial entities develop and document an information security policy that sets rules to protect the availability, authenticity, integrity and confidentiality of data, information assets and ICT assets, including those of their customers (Art. 9(4)(a), DORA (2022)). They also implement policies that limit physical or logical access to information assets and ICT assets to what is required for legitimate and approved functions and activities (Art. 9(4)(c)). This is the least-privilege principle as a legal requirement.

#### Origin and variants

The BAIT (BaFin circular 10/2017 (BA)) specified IT and information security requirements for banks under § 25a KWG (Bundesbank, BAIT / DORA). Since DORA has applied from 17 January 2025, all institutions that must carry out ICT risk management under Articles 5 to 15 or Article 16 DORA are excluded from the scope of the BAIT, and the BAIT will be repealed completely at the end of 31 December 2026. BaFin withdrew the corresponding circulars for payment institutions, insurers and investment management companies (ZAIT, VAIT and KAIT) on 17 January 2025. The 2026 version of MaRisk adds requirements for models, expressly including artificial intelligence, which must be validated and sufficiently explainable (AT 4.3.4), and it excludes ICT services subject to ICT third-party risk management under DORA from its outsourcing rules (AT 9) (MaRisk (2026)).

### When to use it

- When a bank or other financial entity in Germany organises its internal control system, control functions and internal audit (§ 25a KWG, MaRisk (2026)).
- When an institution within DORA's scope sets up or reviews its ICT risk management framework, information security policy and access rules (Art. 5, 6, 9, DORA (2022)).
- When an AI system is introduced into banking processes and must be assigned to the existing control structure, including model validation and explainability (MaRisk AT 4.3.4).

### Strengths and limitations

**Strengths**
- The three lines of defence give MaRisk, the EBA guidelines and DORA a common control architecture (EBA internal governance guidelines (2021), Art. 6(4), DORA (2022)).
- DORA makes the management body explicitly and ultimately responsible for ICT risk (Art. 5(2)).
- With DORA directly applicable and the BAIT being repealed, institutions within DORA's scope follow one EU-wide set of ICT rules instead of national IT circulars (Bundesbank, BAIT / DORA).

**Limitations**
- Until the end of 2026, institutions outside DORA's ICT risk management scope remain subject to the BAIT, so two regimes coexist during the transition (Bundesbank, BAIT / DORA).
- MaRisk applies only to institutions not directly supervised by the ECB (MaRisk (2026)).
- The rules set organisational requirements and principles; how access control, separation of duties and control functions are implemented technically is left to the institution.

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| MaRisk (2026) | BaFin circular specifying § 25a KWG: internal control system, control functions, internal audit, resources, contingency plans, models | Institutions not directly supervised by the ECB, for the overall control system |
| DORA (2022) | Directly applicable EU regulation for ICT risk: management body responsibility, ICT control function, information security policy, access limitation | Financial entities within DORA's scope, for ICT and information security |
| BAIT (BaFin circular 10/2017) | National IT circular based on § 25a KWG; no longer applies to institutions under DORA's ICT risk management and will be repealed at the end of 2026 | Remaining institutions outside DORA's ICT risk management scope until the end of 2026 |

### In practice

Institutions assign every function, including teams that build or operate AI systems, to one of the three lines so that development, independent control and audit stay separate (EBA internal governance guidelines (2021), Art. 6(4), DORA (2022)). Access rights for AI applications and agents that use banking data or systems follow the same rule as for staff: only what legitimate and approved functions require (Art. 9(4)(c)), which also concerns the tool permissions of [[agentic-ai|agentic AI]] systems. Models used in risk management processes, including machine learning models, are validated and checked for explainability before and during use (MaRisk AT 4.3.4).

### Key takeaway

In German banks, information security rests on the proper business organisation of § 25a KWG and the three lines of defence, with DORA replacing the national BAIT for ICT risk management of institutions in its scope.

### Sources

- Deutsche Bundesbank. *BAIT / DORA – Aufsichtliche Anforderungen an die IT und die digitale operationale Resilienz.* [bundesbank.de](https://www.bundesbank.de/de/aufgaben/bankenaufsicht/einzelaspekte/risikomanagement/bait-dora-598580)
- Regulation (EU) 2022/2554 on digital operational resilience for the financial sector (DORA). [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2022/2554/oj)
- BaFin, Rundschreiben 06/2026 (BA) – Mindestanforderungen an das Risikomanagement (MaRisk), 30 June 2026. [bafin.de](https://www.bafin.de/SharedDocs/Downloads/DE/Rundschreiben/dl_rs_0626_9_marisk.html)
- Kreditwesengesetz (KWG), § 25a Besondere organisatorische Pflichten. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/kredwg/__25a.html)
- European Banking Authority (2021). *Guidelines on internal governance under Directive 2013/36/EU* (EBA/GL/2021/05). [eba.europa.eu](https://www.eba.europa.eu/activities/single-rulebook/regulatory-activities/internal-governance/guidelines-internal-governance-under-crd)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Deutsche Banken organisieren Informationssicherheit und interne Kontrolle auf der Grundlage von § 25a [[kwg|KWG]], der eine ordnungsgemäße Geschäftsorganisation mit internem Kontrollsystem und Interner Revision verlangt. Die [[marisk|MaRisk]] konkretisieren das interne Kontrollsystem, und die drei Verteidigungslinien trennen Geschäftsbereiche, unabhängige Kontrollfunktionen und Interne Revision. Für IT und Informationssicherheit legte bisher das BaFin-Rundschreiben BAIT die Einzelheiten fest; seit dem 17. Januar 2025 regelt [[dora|DORA]] das IKT-Risikomanagement der Institute in seinem Anwendungsbereich, und die BAIT werden Ende 2026 aufgehoben.

### Funktionsweise

Mehrere Regelungsebenen bauen aufeinander auf: die gesetzliche Pflicht zu einer ordnungsgemäßen Geschäftsorganisation, ihre Konkretisierung in den MaRisk, die drei Verteidigungslinien als Ordnungsprinzip der Kontrolle und die unmittelbar geltenden Anforderungen von DORA an das IKT-Risikomanagement, einschließlich Informationssicherheitsleitlinie und Zugriffsbeschränkung.

```text
1. § 25a KWG: ordnungsgemäße Geschäftsorganisation
▼
2. MaRisk: internes Kontrollsystem
▼
3. Drei Verteidigungslinien
▼
4. DORA: Rahmen für das IKT-Risikomanagement
▼
5. DORA: Informationssicherheitsleitlinie und Zugriffsbeschränkung
```

#### 1. Rechtsgrundlage: ordnungsgemäße Geschäftsorganisation

§ 25a KWG verlangt von Instituten eine ordnungsgemäße Geschäftsorganisation, die die Einhaltung der gesetzlichen Bestimmungen gewährleistet, darunter ein angemessenes und wirksames Risikomanagement mit Strategien, Verfahren zur Sicherstellung der Risikotragfähigkeit, internen Kontrollverfahren mit einem internen Kontrollsystem und einer Internen Revision sowie ein Notfallmanagement, insbesondere für IT-Systeme (§ 25a KWG). Das BaFin-Rundschreiben MaRisk konkretisiert diese Anforderungen für Institute, die nicht direkt von der Europäischen Zentralbank beaufsichtigt werden (MaRisk (2026)). § 25a KWG ist auch die Rechtsgrundlage der BAIT, des Rundschreibens mit IT-Anforderungen an Banken (Bundesbank, BAIT / DORA).

#### 2. Das interne Kontrollsystem

Nach den MaRisk umfasst das interne Kontrollsystem Regelungen zur Aufbau- und Ablauforganisation, Risikosteuerungs- und -controllingprozesse sowie eine Risikocontrolling-Funktion und eine Compliance-Funktion (AT 4.3, MaRisk (2026)). Miteinander unvereinbare Tätigkeiten müssen von verschiedenen Mitarbeitern ausgeführt werden (AT 4.3.1), und die Risikocontrolling-Funktion muss bis einschließlich der Ebene der Geschäftsleitung von den Bereichen getrennt sein, die Geschäfte initiieren oder abschließen (AT 4.4.1). Jedes Institut braucht eine Interne Revision mit vollständigem und uneingeschränktem Informationsrecht (AT 4.4.3). Die technisch-organisatorische Ausstattung muss zu Geschäftsaktivitäten und Risikosituation passen, mit wirksamen Prozessen zur Sicherstellung der Datenqualität (AT 7.2), und für Aktivitäten und Prozesse, die kritische oder wichtige Funktionen darstellen, ist ein Notfallkonzept erforderlich (AT 7.3).

#### 3. Drei Verteidigungslinien

Die EBA-Leitlinien zur internen Governance folgen dem Modell der drei Verteidigungslinien: Die Geschäftsbereiche gehen Risiken ein und steuern sie (erste Linie), Risikomanagement- und Compliance-Funktion überwachen sie unabhängig (zweite Linie), und die Interne Revision prüft das gesamte System unabhängig (dritte Linie) (EBA-Leitlinien zur internen Governance (2021)). Interne Kontrollfunktionen müssen von den kontrollierten Geschäftsbereichen unabhängig, angemessen ausgestattet und von Leitern geführt sein, die sich an das Leitungsorgan in seiner Aufsichtsfunktion wenden können; die Interne Revision darf nicht mit einer anderen Kontrollfunktion kombiniert werden. DORA wendet dasselbe Prinzip auf das IKT-Risiko an: Finanzunternehmen, die keine Kleinstunternehmen sind, müssen eine angemessene Trennung und Unabhängigkeit von IKT-Risikomanagement, Kontrollfunktionen und Innenrevision nach dem Modell der drei Verteidigungslinien oder einem internen Risikomanagement- und Kontrollmodell sicherstellen (Art. 6 Abs. 4, DORA (2022)).

#### 4. IKT-Risikomanagement nach DORA

Nach DORA legt das Leitungsorgan den Rahmen für das IKT-Risikomanagement fest, genehmigt und überwacht ihn, ist für seine Umsetzung verantwortlich und trägt die letzte Verantwortung für das IKT-Risiko (Art. 5 Abs. 2, DORA (2022)). Finanzunternehmen, die keine Kleinstunternehmen sind, übertragen die Steuerung und Überwachung des IKT-Risikos einer Kontrollfunktion mit angemessener Unabhängigkeit (Art. 6 Abs. 4). Der Rahmen für das IKT-Risikomanagement ist zu dokumentieren und mindestens einmal jährlich sowie nach schwerwiegenden IKT-bezogenen Vorfällen zu überprüfen (Art. 6 Abs. 5).

#### 5. Informationssicherheitsleitlinie und Zugriffsbeschränkung

Im Rahmen des IKT-Risikomanagements entwickeln und dokumentieren Finanzunternehmen eine Informationssicherheitsleitlinie mit Regeln zum Schutz der Verfügbarkeit, Authentizität, Integrität und Vertraulichkeit von Daten, Informations- und IKT-Assets, gegebenenfalls auch der ihrer Kunden (Art. 9 Abs. 4 Buchst. a, DORA (2022)). Außerdem führen sie Richtlinien ein, die den physischen oder logischen Zugang zu Informations- und IKT-Assets auf das beschränken, was für legitime und genehmigte Funktionen und Tätigkeiten erforderlich ist (Art. 9 Abs. 4 Buchst. c). Das ist das Prinzip der minimalen Rechte als rechtliche Anforderung.

#### Ursprung und Varianten

Die BAIT (BaFin-Rundschreiben 10/2017 (BA)) konkretisierten die Anforderungen an IT und Informationssicherheit von Banken nach § 25a KWG (Bundesbank, BAIT / DORA). Seit DORA ab dem 17. Januar 2025 gilt, sind alle Institute, die ein IKT-Risikomanagement nach den Artikeln 5 bis 15 oder Artikel 16 DORA betreiben müssen, aus dem Anwenderkreis der BAIT ausgenommen, und die BAIT werden mit Ablauf des 31. Dezember 2026 vollständig aufgehoben. Die entsprechenden Rundschreiben für Zahlungsinstitute, Versicherer und Kapitalverwaltungsgesellschaften (ZAIT, VAIT und KAIT) hat die BaFin am 17. Januar 2025 aufgehoben. Die MaRisk in der Fassung von 2026 enthalten Anforderungen an Modelle, ausdrücklich auch an künstliche Intelligenz, die validiert und hinreichend erklärbar sein müssen (AT 4.3.4), und nehmen IKT-Dienstleistungen, die dem IKT-Drittparteienrisikomanagement nach DORA unterliegen, von ihren Auslagerungsregeln aus (AT 9) (MaRisk (2026)).

### Wann einsetzen

- Wenn eine Bank oder ein anderes Finanzunternehmen in Deutschland sein internes Kontrollsystem, seine Kontrollfunktionen und die Interne Revision organisiert (§ 25a KWG, MaRisk (2026)).
- Wenn ein Institut im Anwendungsbereich von DORA seinen Rahmen für das IKT-Risikomanagement, seine Informationssicherheitsleitlinie und seine Zugriffsregeln einrichtet oder überprüft (Art. 5, 6, 9, DORA (2022)).
- Wenn ein KI-System in Bankprozesse eingeführt wird und in die bestehende Kontrollstruktur einzuordnen ist, einschließlich Modellvalidierung und Erklärbarkeit (MaRisk AT 4.3.4).

### Stärken und Grenzen

**Stärken**
- Die drei Verteidigungslinien geben MaRisk, EBA-Leitlinien und DORA eine gemeinsame Kontrollarchitektur (EBA-Leitlinien zur internen Governance (2021), Art. 6 Abs. 4, DORA (2022)).
- DORA macht das Leitungsorgan ausdrücklich letztverantwortlich für das IKT-Risiko (Art. 5 Abs. 2).
- Mit dem unmittelbar geltenden DORA und der Aufhebung der BAIT folgen Institute im Anwendungsbereich von DORA einem EU-weit einheitlichen IKT-Regelwerk statt nationaler IT-Rundschreiben (Bundesbank, BAIT / DORA).

**Einschränkungen**
- Bis Ende 2026 unterliegen Institute außerhalb des IKT-Risikomanagements nach DORA weiter den BAIT, sodass während des Übergangs zwei Regime nebeneinander bestehen (Bundesbank, BAIT / DORA).
- Die MaRisk gelten nur für Institute, die nicht direkt von der EZB beaufsichtigt werden (MaRisk (2026)).
- Die Regeln setzen organisatorische Anforderungen und Grundsätze; wie Zugriffsbeschränkung, Funktionstrennung und Kontrollfunktionen technisch umgesetzt werden, bleibt dem Institut überlassen.

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| MaRisk (2026) | BaFin-Rundschreiben zur Konkretisierung von § 25a KWG: internes Kontrollsystem, Kontrollfunktionen, Interne Revision, Ausstattung, Notfallkonzepte, Modelle | Institute, die nicht direkt von der EZB beaufsichtigt werden, für das gesamte Kontrollsystem |
| DORA (2022) | Unmittelbar geltende EU-Verordnung zum IKT-Risiko: Verantwortung des Leitungsorgans, IKT-Kontrollfunktion, Informationssicherheitsleitlinie, Zugriffsbeschränkung | Finanzunternehmen im Anwendungsbereich von DORA, für IKT und Informationssicherheit |
| BAIT (BaFin-Rundschreiben 10/2017) | Nationales IT-Rundschreiben auf Grundlage von § 25a KWG; gilt nicht mehr für Institute mit IKT-Risikomanagement nach DORA und wird Ende 2026 aufgehoben | Übrige Institute außerhalb des IKT-Risikomanagements nach DORA bis Ende 2026 |

### In der Praxis

Institute ordnen jede Funktion, auch Teams, die KI-Systeme entwickeln oder betreiben, einer der drei Linien zu, damit Entwicklung, unabhängige Kontrolle und Prüfung getrennt bleiben (EBA-Leitlinien zur internen Governance (2021), Art. 6 Abs. 4, DORA (2022)). Zugriffsrechte für KI-Anwendungen und Agenten, die Bankdaten oder -systeme nutzen, folgen derselben Regel wie für Mitarbeiter: nur, was legitime und genehmigte Funktionen erfordern (Art. 9 Abs. 4 Buchst. c), was auch die Werkzeugrechte von [[agentic-ai|agentischen KI-Systemen]] betrifft. Modelle in Prozessen des Risikomanagements, einschließlich Modellen des maschinellen Lernens, werden vor und während des Einsatzes validiert und auf Erklärbarkeit geprüft (MaRisk AT 4.3.4).

### Merksatz

In deutschen Banken beruht die Informationssicherheit auf der ordnungsgemäßen Geschäftsorganisation nach § 25a KWG und den drei Verteidigungslinien, wobei DORA für Institute in seinem Anwendungsbereich die nationalen BAIT beim IKT-Risikomanagement ablöst.

### Quellen

- Deutsche Bundesbank. *BAIT / DORA – Aufsichtliche Anforderungen an die IT und die digitale operationale Resilienz.* [bundesbank.de](https://www.bundesbank.de/de/aufgaben/bankenaufsicht/einzelaspekte/risikomanagement/bait-dora-598580)
- Regulation (EU) 2022/2554 on digital operational resilience for the financial sector (DORA). [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2022/2554/oj)
- BaFin, Rundschreiben 06/2026 (BA) – Mindestanforderungen an das Risikomanagement (MaRisk), 30 June 2026. [bafin.de](https://www.bafin.de/SharedDocs/Downloads/DE/Rundschreiben/dl_rs_0626_9_marisk.html)
- Kreditwesengesetz (KWG), § 25a Besondere organisatorische Pflichten. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/kredwg/__25a.html)
- European Banking Authority (2021). *Guidelines on internal governance under Directive 2013/36/EU* (EBA/GL/2021/05). [eba.europa.eu](https://www.eba.europa.eu/activities/single-rulebook/regulatory-activities/internal-governance/guidelines-internal-governance-under-crd)
