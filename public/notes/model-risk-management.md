---
title_en: Model Risk Management
title_de: Modellrisikomanagement
entity_type: Concept
aliases:
- Model risk management
- MRM
- Model risk
- Model validation
- Model governance
- Model inventory
- SR 11-7
- Modellrisiko
- Modellvalidierung
sources:
- https://www.federalreserve.gov/boarddocs/srletters/2011/sr1107a1.pdf
- https://www.bankingsupervision.europa.eu/ecb/pub/pdf/ssm.supervisory_guide202507.en.pdf
- https://www.bankingsupervision.europa.eu/press/pr/date/2025/html/ssm.pr250728~2b36305822.en.html
- https://www.bafin.de/SharedDocs/Downloads/DE/Rundschreiben/dl_rs_0626_9_marisk.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Model risk is "the potential for adverse consequences from decisions based on incorrect or misused model outputs and reports", and model risk management (MRM) is the set of practices that keeps it under control: sound development and use, independent validation, and governance with a model inventory, policies and clear responsibilities (Board of Governors of the Federal Reserve System & OCC, 2011). The US supervisory guidance SR 11-7 from 2011 made "effective challenge" by objective, competent and influential parties the guiding principle (Board of Governors of the Federal Reserve System & OCC, 2011). In the euro area, the ECB guide to internal models expects banks to have a model risk management framework for their internal capital models and, since its 2025 revision, sets out how models using machine learning must be governed, validated, explained and audited (ECB Banking Supervision, 2025a; 2025b).

### How it works

```text
             ┌──────────── governance: board, senior management, policies, model inventory ────────────┐
             │                                                                                          │
 develop ──► test ──► validate (independent) ──► approve ──► use ──► monitor ──► revalidate / retire
  purpose,     accuracy,   1. conceptual soundness        limits on   overrides,     at least annually,
  data,        robustness, 2. ongoing monitoring           use,        drift,         after material
  documented   stability      (process verification,       reports     benchmarks     changes
  assumptions                 benchmarking)
                           3. outcomes analysis (back-testing)
             └──────────── internal audit checks the whole framework ───────────────────────────────────┘
```

#### 1. What a model is and why it carries risk

A model is a quantitative method that applies statistical, economic, financial or mathematical theories and assumptions to turn input data into quantitative estimates; it has an input, a processing and a reporting component, and the definition includes approaches with partly qualitative or expert-judgement inputs if the output is quantitative (Board of Governors of the Federal Reserve System & OCC, 2011). Model risk arises for two reasons: the model may have fundamental errors anywhere from design to implementation, including errors in input data, or a sound model may be used incorrectly, for instance outside the environment it was built for (Board of Governors of the Federal Reserve System & OCC, 2011). Model risk grows with complexity, uncertainty about inputs and assumptions, broader use and larger potential impact, and should be assessed for single models and in aggregate, since models share data and assumptions (Board of Governors of the Federal Reserve System & OCC, 2011).

#### 2. Development, implementation and use

Development starts with a clear statement of purpose; design, theory and logic are documented, data quality and relevance are assessed rigorously, and data proxies are identified and justified ([[data-quality|data quality]]) (Board of Governors of the Federal Reserve System & OCC, 2011). Testing checks accuracy, robustness and stability, behaviour over a range of inputs and extreme values, and a variety of tests is needed because any single test is rarely sufficient (Board of Governors of the Federal Reserve System & OCC, 2011). Because all models are imperfect, banks should account for uncertainty, for example by reporting ranges instead of point estimates or by conservative adjustments that are justified and measured rather than merely claimed (Board of Governors of the Federal Reserve System & OCC, 2011).

#### 3. Validation

Validation verifies that models perform as expected and is done by people who are not responsible for development or use and have the authority to challenge them; it applies equally to in-house and vendor models (Board of Governors of the Federal Reserve System & OCC, 2011). It has three core elements: evaluation of conceptual soundness, ongoing monitoring with process verification and benchmarking against alternative models or data, and outcomes analysis, including back-testing against actual outcomes in a period not used for development (Board of Governors of the Federal Reserve System & OCC, 2011). Holdout-sample performance is important during development but no substitute for back-testing ([[cross-validation|cross-validation]]); each model should be reviewed at least annually, and models with severe deficiencies should not be used or only under tight constraints (Board of Governors of the Federal Reserve System & OCC, 2011).

#### 4. Governance

The board of directors and senior management are ultimately responsible; policies define roles, and a firm-wide model inventory lists each model's purpose, usage, restrictions, inputs, outputs, status and owners (Board of Governors of the Federal Reserve System & OCC, 2011). Internal audit assesses whether the framework as a whole works, including the accuracy of the inventory (Board of Governors of the Federal Reserve System & OCC, 2011). The ECB expects at least a written model risk management policy with a definition of a model and of model risk, a register of internal models, guidelines on known deficiencies such as data deficiencies, model misuse or implementation errors, methods to measure model risk, life-cycle guidelines, reporting procedures, defined roles, and skills and training for each stakeholder group (ECB Banking Supervision, 2025a). Each internal model also undergoes a regular complexity assessment, and highly complex models, for example because of machine learning, or dynamic models must be identified (ECB Banking Supervision, 2025a).

#### 5. Machine learning in internal models

For the ECB, machine learning techniques are models with many parameters that can represent highly non-linear functions or need large amounts of training data, and are characterised by high complexity and limited explainability; generalised linear models such as linear or [[logistic-regression|logistic regression]] are not counted (ECB Banking Supervision, 2025a). Using ML raises a model's complexity and, all else being equal, makes it more likely to be classified as material (ECB Banking Supervision, 2025a). Expectations include:

- **Validation** must challenge whether the complexity is justified, the stability of results across hyperparameters and training randomness, and [[overfitting|overfitting]], using out-of-sample and out-of-time data ([[hyperparameter-optimisation|hyperparameter optimisation]]) (ECB Banking Supervision, 2025a).
- **Replicability**: documentation must allow replication, including parameters, hyperparameters, random seeds and, where training depends on it as in [[gradient-descent|stochastic gradient descent]], the order of observations (ECB Banking Supervision, 2025a).
- **Explainability**: institutions use [[explainable-ai|explainability]] techniques that show each risk driver's global contribution and its contribution to individual predictions; explanations must be robust, accurate and actionable to allow informed human oversight, and the explainability tools themselves are validated at least yearly (ECB Banking Supervision, 2025a).
- **Data**: input data undergo additional exploratory analysis of formats, missing values and potential sources of bias (ECB Banking Supervision, 2025a).
- **Changes and drift**: the change policy must define what counts as a change to an ML model; switching from a traditional to a mostly ML-based design is generally a material change, and dynamic models must be monitored for model drift so that material changes are not implemented automatically ([[mlops-and-deployment|MLOps]]) (ECB Banking Supervision, 2025a).
- **Traceability**: IT infrastructure should version models and let the institution replicate and verify the decisions of ML-based models ([[experiment-tracking|experiment tracking]]) (ECB Banking Supervision, 2025a).

#### Origin and variants

SR 11-7, issued in April 2011 by the Board of Governors of the Federal Reserve System and the Office of the Comptroller of the Currency, broadened earlier guidance that focused on model validation to all aspects of model risk management (Board of Governors of the Federal Reserve System & OCC, 2011). The ECB first published its guide to internal models in October 2019 as part of the targeted review of internal models (TRIM), which addressed inconsistencies in complex internal models and unwarranted variability of their outputs; version 4.0 of July 2025 added the section on machine learning (ECB Banking Supervision, 2025b). In Germany, the [[marisk|MaRisk]] (AT 4.3.4) set requirements for models used in risk management, expressly including artificial intelligence, such as justified assumptions, data quality, rules on overrides, regular validation and sufficient explainability (BaFin, 2026).

### When to use it

- Banks using models for credit decisions, valuation, risk measurement, capital and stress testing (Board of Governors of the Federal Reserve System & OCC, 2011).
- Banks calculating own funds requirements with internal models under the [[crr-and-crd|CRR]], which need approval by ECB Banking Supervision; as of June 2024, about 60% of significant banks' credit risk exposure amounts were calculated with internal models (ECB Banking Supervision, 2025b).
- Any organisation where decisions depend on model outputs; the same principles of independent validation, monitoring and inventory carry over to ML systems in production ([[monitoring-and-alerting|monitoring]]).

### Strengths and limitations

**Strengths**
- Effective challenge by independent, competent and influential reviewers catches errors that developers and users overlook, since user challenge tends to be asymmetric (Board of Governors of the Federal Reserve System & OCC, 2011).
- An inventory makes aggregate model risk visible across the institution (Board of Governors of the Federal Reserve System & OCC, 2011).
- The ECB's ML expectations tie complexity to a demonstrated performance gain (ECB Banking Supervision, 2025a).

**Limitations**
- Model risk cannot be eliminated, even with skilled modelling and robust validation (Board of Governors of the Federal Reserve System & OCC, 2011).
- Conservatism can be misleading: an extreme point on a misestimated distribution is not conservative, and excessive conservatism can make users discount model outputs (Board of Governors of the Federal Reserve System & OCC, 2011).
- Vendor models may not give access to code and implementation details, so validation relies more on sensitivity analysis and benchmarking (Board of Governors of the Federal Reserve System & OCC, 2011).

### Comparison

| Aspect | SR 11-7 (US, 2011) | ECB guide to internal models (2025) |
|---|---|---|
| Scope | all models used by banks | internal models for own funds requirements (credit, market, counterparty credit risk) |
| Core principle | effective challenge | model risk management framework across the group |
| Validation | conceptual soundness, ongoing monitoring, outcomes analysis | internal validation per CRR, with additional ML expectations |
| Inventory | firm-wide model inventory | register of internal models |
| Machine learning | not addressed specifically | dedicated section: explainability, replicability, drift, change policy |

Sources: Board of Governors of the Federal Reserve System & OCC (2011); ECB Banking Supervision (2025a).

### Regulatory context

In the euro area, banks' use of internal models to calculate risk-weighted assets requires initial approval by ECB Banking Supervision, followed by internal model investigations and ongoing model monitoring; the guide refers to the definition of model risk in Article 3(1)(11) of the CRD ([[crr-and-crd|CRR and CRD]], [[ecb|ECB]]) (ECB Banking Supervision, 2025a; 2025b). The [[marisk|MaRisk]] cover models outside the scope of the CRR, and the [[eu-ai-act|EU AI Act]] adds requirements for high-risk AI systems such as creditworthiness assessment ([[creditworthiness-assessment|creditworthiness assessment]]).

### Key takeaway

Model risk comes from wrong models and from right models used wrongly; it is managed through documented development, independent validation with monitoring and back-testing, an inventory and clear governance, and for machine learning additionally through justified complexity, replicability, explainability and drift control.

### Sources

- Board of Governors of the Federal Reserve System & Office of the Comptroller of the Currency (2011). *Supervisory Guidance on Model Risk Management* (SR Letter 11-7, Attachment). [federalreserve.gov](https://www.federalreserve.gov/boarddocs/srletters/2011/sr1107a1.pdf)
- ECB Banking Supervision (2025a). *ECB guide to internal models*, version 4.0, July 2025. [bankingsupervision.europa.eu](https://www.bankingsupervision.europa.eu/ecb/pub/pdf/ssm.supervisory_guide202507.en.pdf)
- ECB Banking Supervision (2025b). *ECB publishes revised guide to internal models.* Press release, 28 July 2025. [bankingsupervision.europa.eu](https://www.bankingsupervision.europa.eu/press/pr/date/2025/html/ssm.pr250728~2b36305822.en.html)
- BaFin (2026). *Mindestanforderungen an das Risikomanagement (MaRisk)*, Rundschreiben 06/2026 (BA), AT 4.3.4. [bafin.de](https://www.bafin.de/SharedDocs/Downloads/DE/Rundschreiben/dl_rs_0626_9_marisk.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Modellrisiko ist „the potential for adverse consequences from decisions based on incorrect or misused model outputs and reports“, und Modellrisikomanagement (MRM) umfasst die Praktiken, die es beherrschbar machen: solide Entwicklung und Nutzung, unabhängige Validierung und eine Governance mit Modellinventar, Richtlinien und klaren Zuständigkeiten (Board of Governors of the Federal Reserve System & OCC, 2011). Die US-Aufsichtsleitlinie SR 11-7 von 2011 machte „effective challenge“ durch objektive, kompetente und einflussreiche Beteiligte zum Leitprinzip (Board of Governors of the Federal Reserve System & OCC, 2011). Im Euroraum erwartet der EZB-Leitfaden zu internen Modellen von Banken einen Rahmen für das Modellrisikomanagement ihrer internen Eigenmittelmodelle und legt seit der Überarbeitung 2025 fest, wie Modelle mit maschinellem Lernen gesteuert, validiert, erklärt und geprüft werden müssen (ECB Banking Supervision, 2025a; 2025b).

### Funktionsweise

```text
             ┌──────────── Governance: Aufsichtsorgan, Geschäftsleitung, Richtlinien, Modellinventar ───────┐
             │                                                                                             │
 entwickeln ──► testen ──► validieren (unabhängig) ──► freigeben ──► nutzen ──► überwachen ──► revalidieren / stilllegen
  Zweck,         Genauigkeit,  1. konzeptionelle Solidität     Nutzungs-    Overrides,     mindestens jährlich,
  Daten,         Robustheit,   2. laufendes Monitoring         grenzen,     Drift,         nach wesentlichen
  dokumentierte  Stabilität       (Prozessprüfung,             Berichte     Benchmarks     Änderungen
  Annahmen                        Benchmarking)
                               3. Ergebnisanalyse (Backtesting)
             └──────────── Interne Revision prüft den gesamten Rahmen ──────────────────────────────────────┘
```

#### 1. Was ein Modell ist und warum es Risiken birgt

Ein Modell ist eine quantitative Methode, die statistische, ökonomische, finanzielle oder mathematische Theorien und Annahmen anwendet, um Eingabedaten in quantitative Schätzungen zu überführen; es hat eine Eingabe-, eine Verarbeitungs- und eine Berichtskomponente, und die Definition umfasst auch Ansätze mit teils qualitativen oder auf Expertenurteil beruhenden Eingaben, wenn die Ausgabe quantitativ ist (Board of Governors of the Federal Reserve System & OCC, 2011). Modellrisiko entsteht aus zwei Gründen: Das Modell kann grundlegende Fehler haben, irgendwo zwischen Entwurf und Implementierung, einschließlich Fehlern in den Eingabedaten, oder ein solides Modell wird falsch eingesetzt, etwa außerhalb des Umfelds, für das es gebaut wurde (Board of Governors of the Federal Reserve System & OCC, 2011). Modellrisiko wächst mit Komplexität, Unsicherheit über Eingaben und Annahmen, breiterer Nutzung und größerer möglicher Wirkung und sollte für einzelne Modelle und insgesamt bewertet werden, da Modelle Daten und Annahmen teilen (Board of Governors of the Federal Reserve System & OCC, 2011).

#### 2. Entwicklung, Implementierung und Nutzung

Die Entwicklung beginnt mit einer klaren Zweckbestimmung; Entwurf, Theorie und Logik werden dokumentiert, Datenqualität und -relevanz gründlich bewertet und Ersatzdaten (Proxys) benannt und begründet ([[data-quality|Datenqualität]]) (Board of Governors of the Federal Reserve System & OCC, 2011). Tests prüfen Genauigkeit, Robustheit und Stabilität, das Verhalten über eine Bandbreite von Eingaben und bei Extremwerten, und es braucht verschiedene Tests, weil ein einzelner Test selten ausreicht (Board of Governors of the Federal Reserve System & OCC, 2011). Weil alle Modelle unvollkommen sind, sollten Banken Unsicherheit berücksichtigen, etwa durch Bandbreiten statt Punktschätzungen oder durch konservative Anpassungen, die begründet und gemessen statt nur behauptet werden (Board of Governors of the Federal Reserve System & OCC, 2011).

#### 3. Validierung

Die Validierung prüft, ob Modelle wie erwartet funktionieren, und wird von Personen durchgeführt, die weder für Entwicklung noch Nutzung verantwortlich sind und befugt sind, diese infrage zu stellen; sie gilt für eigene Modelle ebenso wie für Modelle von Anbietern (Board of Governors of the Federal Reserve System & OCC, 2011). Sie hat drei Kernelemente: die Bewertung der konzeptionellen Solidität, laufendes Monitoring mit Prozessprüfung und Benchmarking gegen alternative Modelle oder Daten sowie die Ergebnisanalyse einschließlich Backtesting gegen tatsächliche Ergebnisse in einem Zeitraum, der nicht für die Entwicklung genutzt wurde (Board of Governors of the Federal Reserve System & OCC, 2011). Die Leistung auf Holdout-Stichproben ist in der Entwicklung wichtig, ersetzt aber kein Backtesting ([[cross-validation|Kreuzvalidierung]]); jedes Modell sollte mindestens jährlich überprüft werden, und Modelle mit schweren Mängeln sollten nicht oder nur unter engen Auflagen genutzt werden (Board of Governors of the Federal Reserve System & OCC, 2011).

#### 4. Governance

Letztverantwortlich sind Aufsichtsorgan und Geschäftsleitung; Richtlinien legen Rollen fest, und ein institutsweites Modellinventar führt für jedes Modell Zweck, Nutzung, Einschränkungen, Eingaben, Ausgaben, Status und Verantwortliche (Board of Governors of the Federal Reserve System & OCC, 2011). Die interne Revision beurteilt, ob der Rahmen als Ganzes funktioniert, einschließlich der Richtigkeit des Inventars (Board of Governors of the Federal Reserve System & OCC, 2011). Die EZB erwartet mindestens eine schriftliche Richtlinie zum Modellrisikomanagement mit einer Definition von Modell und Modellrisiko, ein Register der internen Modelle, Leitlinien zu bekannten Mängeln wie Datenmängeln, Fehlnutzung oder Implementierungsfehlern, Methoden zur Messung des Modellrisikos, Leitlinien zum Modelllebenszyklus, Berichtsverfahren, festgelegte Rollen sowie Kompetenzen und Schulungen für jede Gruppe von Beteiligten (ECB Banking Supervision, 2025a). Jedes interne Modell durchläuft außerdem eine regelmäßige Komplexitätsbewertung, und hochkomplexe Modelle, etwa wegen maschinellen Lernens, oder dynamische Modelle müssen gekennzeichnet werden (ECB Banking Supervision, 2025a).

#### 5. Maschinelles Lernen in internen Modellen

Für die EZB sind Techniken des maschinellen Lernens Modelle mit vielen Parametern, die hochgradig nichtlineare Funktionen abbilden können oder große Trainingsdatenmengen brauchen, und zeichnen sich durch hohe Komplexität und begrenzte Erklärbarkeit aus; verallgemeinerte lineare Modelle wie die lineare oder [[logistic-regression|logistische Regression]] zählen nicht dazu (ECB Banking Supervision, 2025a). Der Einsatz von ML erhöht die Komplexität eines Modells und macht es unter sonst gleichen Bedingungen wahrscheinlicher, dass es als wesentlich eingestuft wird (ECB Banking Supervision, 2025a). Zu den Erwartungen gehören:

- **Validierung** muss hinterfragen, ob die Komplexität gerechtfertigt ist, wie stabil die Ergebnisse über Hyperparameter und den Zufall im Training sind und ob [[overfitting|Overfitting]] vorliegt, anhand von Out-of-Sample- und Out-of-Time-Daten ([[hyperparameter-optimisation|Hyperparameter-Optimierung]]) (ECB Banking Supervision, 2025a).
- **Reproduzierbarkeit**: Die Dokumentation muss eine Replikation erlauben, einschließlich Parametern, Hyperparametern, Zufallsstartwerten und, wo das Training davon abhängt wie beim [[gradient-descent|stochastischen Gradientenabstieg]], der Reihenfolge der Beobachtungen (ECB Banking Supervision, 2025a).
- **Erklärbarkeit**: Institute nutzen [[explainable-ai|Erklärbarkeits]]-Techniken, die den globalen Beitrag jedes Risikotreibers und seinen Beitrag zu einzelnen Vorhersagen zeigen; Erklärungen müssen robust, genau und handlungsrelevant sein, um eine informierte menschliche Aufsicht zu ermöglichen, und die Erklärbarkeitswerkzeuge selbst werden mindestens jährlich validiert (ECB Banking Supervision, 2025a).
- **Daten**: Eingabedaten durchlaufen eine zusätzliche explorative Analyse zu Formaten, fehlenden Werten und möglichen Quellen von Verzerrungen (ECB Banking Supervision, 2025a).
- **Änderungen und Drift**: Die Änderungsrichtlinie muss festlegen, was als Änderung eines ML-Modells gilt; der Wechsel von einem traditionellen zu einem überwiegend ML-basierten Entwurf ist in der Regel eine wesentliche Änderung, und dynamische Modelle müssen auf Modelldrift überwacht werden, damit wesentliche Änderungen nicht automatisch umgesetzt werden ([[mlops-and-deployment|MLOps]]) (ECB Banking Supervision, 2025a).
- **Nachvollziehbarkeit**: Die IT-Infrastruktur sollte Modelle versionieren und es dem Institut ermöglichen, die Entscheidungen ML-basierter Modelle zu replizieren und zu überprüfen ([[experiment-tracking|Experiment-Tracking]]) (ECB Banking Supervision, 2025a).

#### Ursprung und Varianten

SR 11-7, im April 2011 vom Board of Governors of the Federal Reserve System und dem Office of the Comptroller of the Currency herausgegeben, erweiterte frühere, auf die Modellvalidierung ausgerichtete Leitlinien auf alle Aspekte des Modellrisikomanagements (Board of Governors of the Federal Reserve System & OCC, 2011). Die EZB veröffentlichte ihren Leitfaden zu internen Modellen erstmals im Oktober 2019 im Rahmen der gezielten Überprüfung interner Modelle (TRIM), die Inkonsistenzen komplexer interner Modelle und eine ungerechtfertigte Streuung ihrer Ergebnisse angehen sollte; Version 4.0 vom Juli 2025 ergänzte den Abschnitt zu maschinellem Lernen (ECB Banking Supervision, 2025b). In Deutschland stellen die [[marisk|MaRisk]] (AT 4.3.4) Anforderungen an Modelle im Risikomanagement, ausdrücklich auch an künstliche Intelligenz, etwa an die Begründung der Annahmen, die Datenqualität, Überschreibungen, die regelmäßige Validierung und eine hinreichende Erklärbarkeit (BaFin, 2026).

### Wann einsetzen

- Banken, die Modelle für Kreditentscheidungen, Bewertung, Risikomessung, Kapitalplanung und Stresstests nutzen (Board of Governors of the Federal Reserve System & OCC, 2011).
- Banken, die Eigenmittelanforderungen nach der [[crr-and-crd|CRR]] mit internen Modellen berechnen, die von der EZB-Bankenaufsicht genehmigt werden müssen; im Juni 2024 wurden rund 60 % der risikogewichteten Positionsbeträge für das Kreditrisiko bedeutender Banken mit internen Modellen berechnet (ECB Banking Supervision, 2025b).
- Jede Organisation, deren Entscheidungen von Modellausgaben abhängen; dieselben Prinzipien aus unabhängiger Validierung, Monitoring und Inventar lassen sich auf ML-Systeme im Betrieb übertragen ([[monitoring-and-alerting|Monitoring]]).

### Stärken und Grenzen

**Stärken**
- Effective Challenge durch unabhängige, kompetente und einflussreiche Prüfende fängt Fehler ab, die Entwickelnde und Nutzende übersehen, da Einwände von Nutzenden oft einseitig sind (Board of Governors of the Federal Reserve System & OCC, 2011).
- Ein Inventar macht das Modellrisiko des gesamten Instituts sichtbar (Board of Governors of the Federal Reserve System & OCC, 2011).
- Die ML-Erwartungen der EZB knüpfen Komplexität an einen nachgewiesenen Leistungsgewinn (ECB Banking Supervision, 2025a).

**Grenzen**
- Modellrisiko lässt sich auch mit guter Modellierung und robuster Validierung nicht beseitigen (Board of Governors of the Federal Reserve System & OCC, 2011).
- Konservatismus kann täuschen: Ein Extrempunkt einer falsch geschätzten Verteilung ist nicht konservativ, und übertriebener Konservatismus kann dazu führen, dass Nutzende Modellausgaben abwerten (Board of Governors of the Federal Reserve System & OCC, 2011).
- Modelle von Anbietern gewähren oft keinen Zugang zu Code und Implementierungsdetails, sodass die Validierung stärker auf Sensitivitätsanalysen und Benchmarking angewiesen ist (Board of Governors of the Federal Reserve System & OCC, 2011).

### Vergleich

| Aspekt | SR 11-7 (USA, 2011) | EZB-Leitfaden zu internen Modellen (2025) |
|---|---|---|
| Anwendungsbereich | alle von Banken genutzten Modelle | interne Modelle für Eigenmittelanforderungen (Kredit-, Markt-, Gegenparteiausfallrisiko) |
| Leitprinzip | Effective Challenge | Rahmen für das Modellrisikomanagement in der Gruppe |
| Validierung | konzeptionelle Solidität, laufendes Monitoring, Ergebnisanalyse | interne Validierung nach CRR, mit zusätzlichen ML-Erwartungen |
| Inventar | institutsweites Modellinventar | Register der internen Modelle |
| Maschinelles Lernen | nicht eigens behandelt | eigener Abschnitt: Erklärbarkeit, Reproduzierbarkeit, Drift, Änderungsrichtlinie |

Quellen: Board of Governors of the Federal Reserve System & OCC (2011); ECB Banking Supervision (2025a).

### Regulatorischer Kontext

Im Euroraum bedarf die Nutzung interner Modelle zur Berechnung risikogewichteter Aktiva der Erstgenehmigung durch die EZB-Bankenaufsicht, gefolgt von Prüfungen interner Modelle und laufender Modellüberwachung; der Leitfaden verweist auf die Definition des Modellrisikos in Artikel 3 Absatz 1 Nummer 11 der CRD ([[crr-and-crd|CRR und CRD]], [[ecb|EZB]]) (ECB Banking Supervision, 2025a; 2025b). Die [[marisk|MaRisk]] erfassen Modelle außerhalb des Anwendungsbereichs der CRR, und die [[eu-ai-act|KI-Verordnung]] stellt zusätzliche Anforderungen an Hochrisiko-KI-Systeme wie die Kreditwürdigkeitsprüfung ([[creditworthiness-assessment|Kreditwürdigkeitsprüfung]]).

### Merksatz

Modellrisiko entsteht aus falschen Modellen und aus richtigen Modellen, die falsch genutzt werden; es wird durch dokumentierte Entwicklung, unabhängige Validierung mit Monitoring und Backtesting, ein Inventar und klare Governance gesteuert, beim maschinellen Lernen zusätzlich durch begründete Komplexität, Reproduzierbarkeit, Erklärbarkeit und Driftkontrolle.

### Quellen

- Board of Governors of the Federal Reserve System & Office of the Comptroller of the Currency (2011). *Supervisory Guidance on Model Risk Management* (SR Letter 11-7, Attachment). [federalreserve.gov](https://www.federalreserve.gov/boarddocs/srletters/2011/sr1107a1.pdf)
- ECB Banking Supervision (2025a). *ECB guide to internal models*, Version 4.0, Juli 2025. [bankingsupervision.europa.eu](https://www.bankingsupervision.europa.eu/ecb/pub/pdf/ssm.supervisory_guide202507.en.pdf)
- ECB Banking Supervision (2025b). *ECB publishes revised guide to internal models.* Pressemitteilung vom 28. Juli 2025. [bankingsupervision.europa.eu](https://www.bankingsupervision.europa.eu/press/pr/date/2025/html/ssm.pr250728~2b36305822.en.html)
- BaFin (2026). *Mindestanforderungen an das Risikomanagement (MaRisk)*, Rundschreiben 06/2026 (BA), AT 4.3.4. [bafin.de](https://www.bafin.de/SharedDocs/Downloads/DE/Rundschreiben/dl_rs_0626_9_marisk.html)
