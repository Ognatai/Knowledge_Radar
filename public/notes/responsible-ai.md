---
title_en: Responsible AI and AI Governance
title_de: Responsible AI und KI-Governance
entity_type: Concept
aliases:
- Responsible AI
- AI governance
- Trustworthy AI
- AI risk management
- NIST AI RMF
- AI Risk Management Framework
- ISO/IEC 42001
- AI management system
- KI-Governance
- Vertrauenswürdige KI
sources:
- https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf
- https://evs.ee/en/iso-iec-42001-2023
- https://arxiv.org/abs/1810.03993
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Responsible AI is the practice of developing and using AI systems so that they are trustworthy and their risks to people and organisations are identified and managed; AI governance is the organisational side of it: roles, policies, processes, documentation and oversight. The NIST AI Risk Management Framework names seven characteristics of trustworthy AI, valid and reliable, safe, secure and resilient, accountable and transparent, explainable and interpretable, privacy-enhanced, and fair with harmful bias managed, and organises the work into four functions: GOVERN, MAP, MEASURE and MANAGE (NIST, 2023). ISO/IEC 42001 turns this into a certifiable management system for AI (EVS, 2023), and documentation such as model cards makes the evaluation of each model transparent (Mitchell et al., 2019). In the EU, the [[eu-ai-act|AI Act]] makes many of these practices mandatory for high-risk systems.

### How it works

```text
GOVERN (cross-cutting): policies, roles, risk tolerance, culture, third-party rules
 ▼
MAP: context, purpose, affected people, risks of a specific system
 ▼
MEASURE: test and monitor trustworthiness characteristics, before and during operation
 ▼
MANAGE: prioritise and treat risks, respond to incidents, improve
 (documented throughout: model cards, impact assessments, audit trails)
```

#### 1. Characteristics of trustworthy AI

NIST (2023) describes trustworthiness through seven characteristics. Valid and reliable is a necessary condition and the base for the others; accountable and transparent relates to all others. The remaining ones are safe, secure and resilient, explainable and interpretable, privacy-enhanced, and fair with harmful bias managed. Addressing them one by one does not guarantee a trustworthy system: trade-offs are usual, not all apply in every setting, and "trustworthiness is a social concept that ranges across a spectrum and is only as strong as its weakest characteristics" (NIST, 2023). Human judgement decides which metrics and thresholds to use. Methods for single characteristics are covered in [[explainable-ai|explainable AI]], [[fairness-metrics|fairness metrics]], [[differential-privacy-and-federated-learning|differential privacy and federated learning]] and [[llm-guardrails|LLM guardrails]] and [[red-teaming|red teaming]].

#### 2. GOVERN

GOVERN cultivates a culture of risk management, sets out processes, documents and organisational structures to anticipate, identify and manage risks, includes impact assessment, aligns AI risk management with organisational principles and priorities and covers the whole product lifecycle including third-party software, hardware and data (NIST, 2023). It is cross-cutting and informs the other three functions; senior leadership sets the tone and risk tolerance, and "documentation can enhance transparency, improve human review processes, and bolster accountability in AI system teams" (NIST, 2023). In companies this typically becomes an AI policy, an inventory of AI systems, defined roles and approval steps, sometimes called an AI operating model.

#### 3. MAP and MEASURE

MAP establishes the context of a specific system: its purpose, the deployment setting, the people who use it or are affected by it, and the risks that follow; because actors in one part of the AI lifecycle often cannot see the others, NIST recommends involving diverse internal teams and external stakeholders (NIST, 2023). MEASURE uses quantitative, qualitative or mixed methods to analyse, benchmark and monitor these risks; AI systems should be tested before deployment and regularly in operation, with rigorous software testing and performance assessment (NIST, 2023). Technical evaluation is covered in [[llm-evaluation|LLM evaluation]], [[software-testing|software testing]] and [[monitoring-and-alerting|monitoring and alerting]].

#### 4. MANAGE

MANAGE allocates resources to the mapped and measured risks according to the priorities set by GOVERN; risk treatment includes plans to respond to, recover from and communicate about incidents, and processes for emergent risks and continual improvement (NIST, 2023). Systematic documentation from the earlier functions supports transparency and accountability here.

#### 5. Management system: ISO/IEC 42001

ISO/IEC 42001 "specifies the requirements and guides for establishing, implementing, maintaining and continually improving an AI (artificial intelligence) management system within the context of an organization"; it has been valid since 18 December 2023 (EVS, 2023). Like other ISO management system standards, it can be audited and certified, which makes it a common way for companies to demonstrate structured AI governance alongside information security management (see [[it-governance-frameworks|IT governance frameworks]]).

#### 6. Documentation: model cards

Model cards are short documents that accompany a trained model and report its performance under varied conditions, including across demographic, cultural and phenotypic groups and their intersections, together with the intended use and the evaluation procedure (Mitchell et al., 2019). Their purpose is to prevent models from being used where they perform poorly; Mitchell et al. (2019) illustrate them with a smiling-face detector and a toxic-comment classifier. The data-side counterpart is documented in [[data-governance|data governance]].

#### Origin and variants

NIST published the AI RMF 1.0 in January 2023 as a voluntary, rights-preserving, non-sector-specific and use-case-agnostic framework, accompanied by a playbook (NIST, 2023). ISO/IEC 42001 followed in December 2023 (EVS, 2023). Model cards were proposed at the ACM FAT* conference in 2019 (Mitchell et al., 2019). Companies and public bodies publish their own principles and standards on the same themes.

### When to use it

- An organisation develops or buys AI systems and needs a consistent way to approve, document and monitor them (NIST, 2023).
- AI systems affect people's access to jobs, credit, health care or similar, where errors and bias have serious consequences (Mitchell et al., 2019).
- Regulation or customers require evidence of structured AI risk management, for example under the [[eu-ai-act|EU AI Act]] or through certification (EVS, 2023).

### Strengths and limitations

**Strengths**
- A shared vocabulary of trustworthiness characteristics and functions that works across sectors (NIST, 2023).
- Certifiable management systems make governance auditable (EVS, 2023).
- Documentation such as model cards exposes performance gaps between groups before deployment (Mitchell et al., 2019).

**Limitations**
- Frameworks such as the AI RMF are voluntary and describe outcomes, not concrete technical measures (NIST, 2023).
- Characteristics conflict, for example accuracy and privacy, and must be balanced case by case (NIST, 2023).

### Comparison

| | NIST AI RMF | ISO/IEC 42001 | EU AI Act |
|---|---|---|---|
| Type | voluntary framework | certifiable management system standard | binding regulation |
| Scope | AI risks in any sector | AI management system of an organisation | AI systems placed on the EU market or used in the EU |
| Core | 7 characteristics, 4 functions | requirements for establishing and improving an AI management system | risk classes with obligations |

Sources: NIST (2023); EVS (2023). The regulation is summarised in [[eu-ai-act|EU AI Act]].

### In practice

A typical setup combines an inventory of AI use cases, a risk classification aligned with the [[eu-ai-act|EU AI Act]], an approval step before deployment, model and data documentation, evaluation and red-teaming results, and monitoring with an incident process. Financial institutions embed this into existing governance under [[marisk|MaRisk]] and [[dora|DORA]]. Bias in language technology, a central fairness concern, is discussed in [[bias-in-nlp|bias in NLP]].

### Regulatory context

The [[eu-ai-act|EU AI Act]] requires risk management, data governance, technical documentation, transparency, human oversight, accuracy and robustness for high-risk AI systems, and AI literacy measures for providers and deployers. The [[gdpr|GDPR]] adds rules for automated decisions and data protection impact assessments.

### Key takeaway

Responsible AI makes trustworthiness concrete through defined characteristics, an organisational process of governing, mapping, measuring and managing risks, certifiable management systems and transparent documentation, with the EU AI Act turning much of it into obligations.

### Sources

- NIST (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0).* NIST AI 100-1, January 2023. [nvlpubs.nist.gov](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- EVS (2023). *ISO/IEC 42001:2023 Information technology — Artificial intelligence — Management system.* Estonian Centre for Standardisation and Accreditation, catalogue entry. [evs.ee](https://evs.ee/en/iso-iec-42001-2023)
- Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D. & Gebru, T. (2019). *Model Cards for Model Reporting.* FAT* 2019. [arXiv](https://arxiv.org/abs/1810.03993)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Responsible AI ist die Praxis, KI-Systeme so zu entwickeln und zu nutzen, dass sie vertrauenswürdig sind und ihre Risiken für Menschen und Organisationen erkannt und gesteuert werden; KI-Governance ist die organisatorische Seite davon: Rollen, Richtlinien, Prozesse, Dokumentation und Aufsicht. Das AI Risk Management Framework von NIST nennt sieben Merkmale vertrauenswürdiger KI, gültig und zuverlässig, sicher, geschützt und widerstandsfähig, rechenschaftspflichtig und transparent, erklärbar und interpretierbar, datenschutzfreundlich sowie fair mit gesteuerten schädlichen Verzerrungen, und ordnet die Arbeit in vier Funktionen: GOVERN, MAP, MEASURE und MANAGE (NIST, 2023). ISO/IEC 42001 macht daraus ein zertifizierbares Managementsystem für KI (EVS, 2023), und Dokumentation wie Model Cards macht die Evaluation jedes Modells transparent (Mitchell et al., 2019). In der EU macht der [[eu-ai-act|AI Act]] viele dieser Praktiken für Hochrisikosysteme verpflichtend.

### Funktionsweise

```text
GOVERN (übergreifend): Richtlinien, Rollen, Risikotoleranz, Kultur, Regeln für Dritte
 ▼
MAP: Kontext, Zweck, betroffene Menschen, Risiken eines konkreten Systems
 ▼
MEASURE: Merkmale der Vertrauenswürdigkeit testen und überwachen, vor und während des Betriebs
 ▼
MANAGE: Risiken priorisieren und behandeln, auf Vorfälle reagieren, verbessern
 (durchgehend dokumentiert: Model Cards, Folgenabschätzungen, Prüfpfade)
```

#### 1. Merkmale vertrauenswürdiger KI

NIST (2023) beschreibt Vertrauenswürdigkeit über sieben Merkmale. Gültig und zuverlässig ist eine notwendige Bedingung und die Grundlage der übrigen; rechenschaftspflichtig und transparent bezieht sich auf alle anderen. Die übrigen sind sicher, geschützt und widerstandsfähig, erklärbar und interpretierbar, datenschutzfreundlich sowie fair mit gesteuerten schädlichen Verzerrungen. Sie einzeln zu behandeln, garantiert kein vertrauenswürdiges System: Zielkonflikte sind üblich, nicht alle gelten in jedem Kontext, und „trustworthiness is a social concept that ranges across a spectrum and is only as strong as its weakest characteristics“ (NIST, 2023). Welche Metriken und Schwellenwerte gelten, entscheidet menschliches Urteil. Verfahren für einzelne Merkmale behandeln [[explainable-ai|Explainable AI]], [[fairness-metrics|Fairness-Metriken]], [[differential-privacy-and-federated-learning|Differential Privacy und Federated Learning]] sowie [[llm-guardrails|LLM-Guardrails]] und [[red-teaming|Red Teaming]].

#### 2. GOVERN

GOVERN fördert eine Kultur des Risikomanagements, legt Prozesse, Dokumente und Organisationsstrukturen fest, um Risiken vorherzusehen, zu erkennen und zu steuern, umfasst Folgenabschätzungen, richtet das KI-Risikomanagement an Grundsätzen und Prioritäten der Organisation aus und deckt den gesamten Produktlebenszyklus einschließlich Software, Hardware und Daten von Dritten ab (NIST, 2023). Die Funktion ist übergreifend und prägt die anderen drei; die Leitung gibt Ton und Risikotoleranz vor, und „documentation can enhance transparency, improve human review processes, and bolster accountability in AI system teams“ (NIST, 2023). In Unternehmen wird daraus typischerweise eine KI-Richtlinie, ein Verzeichnis der KI-Systeme, festgelegte Rollen und Freigabeschritte, teils als KI-Operating-Modell bezeichnet.

#### 3. MAP und MEASURE

MAP legt den Kontext eines konkreten Systems fest: seinen Zweck, das Einsatzumfeld, die Menschen, die es nutzen oder davon betroffen sind, und die daraus folgenden Risiken; weil Beteiligte in einem Teil des KI-Lebenszyklus die anderen oft nicht überblicken, empfiehlt NIST, vielfältige interne Teams und externe Betroffene einzubeziehen (NIST, 2023). MEASURE nutzt quantitative, qualitative oder gemischte Methoden, um diese Risiken zu analysieren, zu vergleichen und zu überwachen; KI-Systeme sollten vor dem Einsatz und regelmäßig im Betrieb getestet werden, mit gründlichen Softwaretests und Leistungsbewertungen (NIST, 2023). Die technische Evaluation behandeln [[llm-evaluation|LLM-Evaluation]], [[software-testing|Softwaretests]] und [[monitoring-and-alerting|Monitoring und Alerting]].

#### 4. MANAGE

MANAGE ordnet den erfassten und gemessenen Risiken Ressourcen nach den Prioritäten aus GOVERN zu; zur Risikobehandlung gehören Pläne für Reaktion, Wiederherstellung und Kommunikation bei Vorfällen sowie Prozesse für neu entstehende Risiken und kontinuierliche Verbesserung (NIST, 2023). Die systematische Dokumentation aus den vorherigen Funktionen stützt hier Transparenz und Rechenschaft.

#### 5. Managementsystem: ISO/IEC 42001

ISO/IEC 42001 „specifies the requirements and guides for establishing, implementing, maintaining and continually improving an AI (artificial intelligence) management system within the context of an organization“; die Norm gilt seit dem 18. Dezember 2023 (EVS, 2023). Wie andere ISO-Normen für Managementsysteme lässt sie sich prüfen und zertifizieren und ist damit ein verbreiteter Weg für Unternehmen, strukturierte KI-Governance neben dem Informationssicherheitsmanagement nachzuweisen (siehe [[it-governance-frameworks|IT-Governance-Rahmenwerke]]).

#### 6. Dokumentation: Model Cards

Model Cards sind kurze Dokumente, die ein trainiertes Modell begleiten und seine Leistung unter verschiedenen Bedingungen berichten, auch über demografische, kulturelle und phänotypische Gruppen und deren Überschneidungen, zusammen mit dem vorgesehenen Einsatz und dem Evaluationsverfahren (Mitchell et al., 2019). Sie sollen verhindern, dass Modelle dort eingesetzt werden, wo sie schlecht funktionieren; Mitchell et al. (2019) veranschaulichen sie mit einem Lächeln-Detektor und einem Klassifikator für toxische Kommentare. Das Gegenstück auf der Datenseite beschreibt [[data-governance|Data Governance]].

#### Herkunft und Varianten

NIST veröffentlichte das AI RMF 1.0 im Januar 2023 als freiwilliges, rechtewahrendes, branchen- und anwendungsunabhängiges Rahmenwerk mit begleitendem Playbook (NIST, 2023). ISO/IEC 42001 folgte im Dezember 2023 (EVS, 2023). Model Cards wurden 2019 auf der Konferenz ACM FAT* vorgeschlagen (Mitchell et al., 2019). Unternehmen und öffentliche Stellen veröffentlichen eigene Grundsätze und Standards zu denselben Themen.

### Wann einsetzen

- Eine Organisation entwickelt oder kauft KI-Systeme und braucht ein einheitliches Vorgehen, um sie freizugeben, zu dokumentieren und zu überwachen (NIST, 2023).
- KI-Systeme beeinflussen den Zugang von Menschen zu Arbeit, Kredit, Gesundheitsversorgung oder Ähnlichem, wo Fehler und Verzerrungen schwere Folgen haben (Mitchell et al., 2019).
- Regulierung oder Kundschaft verlangen Nachweise für strukturiertes KI-Risikomanagement, etwa nach dem [[eu-ai-act|EU AI Act]] oder durch eine Zertifizierung (EVS, 2023).

### Stärken und Grenzen

**Stärken**
- Ein gemeinsames Vokabular aus Merkmalen der Vertrauenswürdigkeit und Funktionen, das branchenübergreifend funktioniert (NIST, 2023).
- Zertifizierbare Managementsysteme machen Governance prüfbar (EVS, 2023).
- Dokumentation wie Model Cards zeigt Leistungsunterschiede zwischen Gruppen vor dem Einsatz (Mitchell et al., 2019).

**Grenzen**
- Rahmenwerke wie das AI RMF sind freiwillig und beschreiben Ergebnisse, keine konkreten technischen Maßnahmen (NIST, 2023).
- Merkmale stehen in Konflikt, etwa Genauigkeit und Datenschutz, und müssen im Einzelfall abgewogen werden (NIST, 2023).

### Vergleich

| | NIST AI RMF | ISO/IEC 42001 | EU AI Act |
|---|---|---|---|
| Art | freiwilliges Rahmenwerk | zertifizierbare Norm für Managementsysteme | verbindliche Verordnung |
| Geltungsbereich | KI-Risiken in jeder Branche | KI-Managementsystem einer Organisation | KI-Systeme auf dem EU-Markt oder in der EU genutzt |
| Kern | 7 Merkmale, 4 Funktionen | Anforderungen an Aufbau und Verbesserung eines KI-Managementsystems | Risikoklassen mit Pflichten |

Quellen: NIST (2023); EVS (2023). Die Verordnung fasst [[eu-ai-act|EU AI Act]] zusammen.

### In der Praxis

Eine typische Umsetzung verbindet ein Verzeichnis der KI-Anwendungsfälle, eine am [[eu-ai-act|EU AI Act]] ausgerichtete Risikoeinstufung, einen Freigabeschritt vor dem Einsatz, Dokumentation von Modellen und Daten, Ergebnisse aus Evaluation und Red Teaming sowie Monitoring mit einem Prozess für Vorfälle. Finanzinstitute binden das in die bestehende Governance nach [[marisk|MaRisk]] und [[dora|DORA]] ein. Verzerrungen in Sprachtechnologie, ein zentrales Fairness-Thema, behandelt [[bias-in-nlp|Bias in NLP]].

### Regulatorischer Kontext

Der [[eu-ai-act|EU AI Act]] verlangt für Hochrisiko-KI-Systeme Risikomanagement, Data Governance, technische Dokumentation, Transparenz, menschliche Aufsicht, Genauigkeit und Robustheit sowie Maßnahmen zur KI-Kompetenz bei Anbietern und Betreibern. Die [[gdpr|DSGVO]] ergänzt Regeln zu automatisierten Entscheidungen und Datenschutz-Folgenabschätzungen.

### Merksatz

Responsible AI macht Vertrauenswürdigkeit konkret, über festgelegte Merkmale, einen organisatorischen Prozess aus Steuern, Erfassen, Messen und Behandeln von Risiken, zertifizierbare Managementsysteme und transparente Dokumentation; der EU AI Act macht vieles davon zur Pflicht.

### Quellen

- NIST (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0).* NIST AI 100-1, Januar 2023. [nvlpubs.nist.gov](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- EVS (2023). *ISO/IEC 42001:2023 Information technology — Artificial intelligence — Management system.* Estonian Centre for Standardisation and Accreditation, Katalogeintrag. [evs.ee](https://evs.ee/en/iso-iec-42001-2023)
- Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D. & Gebru, T. (2019). *Model Cards for Model Reporting.* FAT* 2019. [arXiv](https://arxiv.org/abs/1810.03993)
