---
title_en: ML Test Score
title_de: ML Test Score
entity_type: Method
aliases:
- ML Test Score
- ML test rubric
sources:
- https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

The ML Test Score is a rubric from Google of 28 concrete tests and monitoring needs that measures how ready a machine learning system is for production and how much [[technical-debt|technical debt]] it carries (Breck et al., 2017). The tests fall into four sections of seven: features and data, model development, ML infrastructure, and monitoring. Each test earns half a point if it is run manually and documented and a full point if it runs automatically; the final score is the minimum of the four section scores, so no area can be neglected (Breck et al., 2017). The rubric complements, but does not replace, general software engineering practice such as unit tests ([[software-testing|software testing]]).

### How it works

```text
4 sections × 7 tests = 28 assertions
  Data         schema, feature value and cost, privacy, feature code tested, ...
  Model        reviewed specs, offline ↔ online metrics, baseline, data slices, inclusion, ...
  Infra        reproducible training, unit + integration tests, validation before serving, canary, rollback, ...
  Monitoring   dependencies, data invariants, training/serving skew, staleness, stability, latency, quality
per test: 0 = not done | 0.5 = manual, documented | 1 = automated, repeated
section score = sum ; ML Test Score = min(section scores)
```

#### 1. Why ML systems need their own tests

ML system behaviour depends strongly on data and models that cannot be specified in advance; by analogy with compilation, training data needs testing like code, and a trained model needs production practices like a binary, such as debuggability, rollbacks and monitoring (Breck et al., 2017). In a survey of several dozen Google teams, none of the tests was implemented by more than 80% of the teams, yet most tests had a non-zero score for at least half of them (Breck et al., 2017).

#### 2. Tests for features and data

The seven data tests: feature expectations are captured in a schema, all features are beneficial, no feature costs too much, features adhere to meta-level requirements, the [[data-pipelines|data pipeline]] has appropriate privacy controls, new features can be added quickly, and all input feature code is tested (Breck et al., 2017). The schema can start from statistics of the training data adjusted with domain knowledge, and is later used to monitor inputs. Privacy tests include checking that user-requested data deletion propagates to the training pipeline and to learned models (Breck et al., 2017; [[data-governance|data governance]]).

#### 3. Tests for model development

Model specifications are reviewed and checked into a repository; offline proxy metrics correlate with online impact; all hyperparameters have been tuned; the impact of model staleness is known; a simpler model is not better; model quality is sufficient on all important data slices; and the model has been tested for considerations of inclusion (Breck et al., 2017). Slicing prevents a global metric from hiding problems, for example global accuracy improving by 1% while accuracy for one country drops by 50% (Breck et al., 2017). The inclusion test examines whether input features correlate strongly with protected user categories and whether predictions differ materially across user groups ([[fairness-metrics|fairness metrics]]).

#### 4. Tests for ML infrastructure

Training is reproducible; model specification code is unit tested; the full ML pipeline is integration tested; model quality is validated before serving; the model can be debugged step by step on a single example; models are canaried before serving; and serving models can be rolled back quickly and safely (Breck et al., 2017). A useful unit test trains a model for a single step of gradient descent on random input to catch library mistakes; "golden tests" that compare a partially trained model to a stored one are hard to maintain and should be avoided (Breck et al., 2017). Validation before serving checks both slow degradation over many versions and sudden drops relative to the previous model ([[regression-testing|regression testing]]).

#### 5. Monitoring tests

Dependency changes result in notification; data invariants hold in training and serving inputs; training and serving compute the same feature values; models are not too stale; models are numerically stable, for example no NaNs or infinities; computing performance has not regressed; and prediction quality on served data has not regressed (Breck et al., 2017). Training/serving skew arises when the code paths that compute features differ between training and inference, and is detected by logging a sample of serving traffic and comparing feature values or distributions (Breck et al., 2017; [[monitoring-and-alerting|monitoring and alerting]]).

#### Origin and variants

Breck, Cai, Nielsen, Salib and Sculley at Google presented the rubric at IEEE Big Data 2017, based on experience with production systems such as ad click prediction and interviews with 36 teams (Breck et al., 2017). It was inspired by Google's Test Certified programme, a scored ladder for test robustness. Among the interviewed teams, integration testing of the whole pipeline and monitoring of training/serving skew were among the least implemented tests, while canarying was common; a hypothetical system using the TFX pipeline platform with its standard recommendations already scored as "reasonably tested" (Breck et al., 2017).

### When to use it

- Assessing the production readiness of an ML system before launch or in a review ([[mlops-and-deployment|MLOps and deployment]]).
- Prioritising technical debt paydown with a measurable score (Breck et al., 2017).
- As a checklist when designing [[ml-pipelines|ML pipelines]] and their CI/CD checks ([[ci-cd|CI/CD]]).

### Strengths and limitations

**Strengths**
- Concrete, actionable assertions with "how to" advice for each test (Breck et al., 2017).
- The minimum over sections forces attention to all four areas (Breck et al., 2017).
- Checklists helped even expert teams, for example to discover a thousand-line untested feature file (Breck et al., 2017).

**Limitations**
- Focused on supervised systems trained continuously and served online at low latency, though most advice carries over (Breck et al., 2017).
- Teams working purely with image or audio data found many data tests less applicable (Breck et al., 2017).
- Expensive labels make quality tests such as staleness impact and validation before serving hard to implement (Breck et al., 2017).
- Taking the minimum reduces how much an individual's effort shows in the score (Breck et al., 2017).
- Written before LLM-based systems; tests for prompts, retrieval or generated text are not covered.

### Comparison

| Score | Interpretation |
|---|---|
| 0 | more of a research project than a productionised system |
| (0, 1] | not totally untested, but serious holes in reliability are possible |
| (1, 2] | a first pass at basic productionisation |
| (2, 3] | reasonably tested, more could be automated |
| (3, 5] | strong automated testing and monitoring, appropriate for mission-critical systems |
| > 5 | exceptional automated testing and monitoring |

Source: Breck et al. (2017), Table V.

### In practice

Score the system in a short structured interview, as the authors did with 36 teams, then raise the weakest section first, since it determines the score (Breck et al., 2017). Automate tests that are run by hand, because only automated, repeated tests earn a full point. Training/serving skew deserves early attention: it caused production issues across many teams yet was rarely tested (Breck et al., 2017). The rubric's monitoring tests map directly onto drift and quality monitoring in operation ([[quality-control|quality control]]).

### Key takeaway

The ML Test Score turns ML production readiness into 28 testable assertions across data, model, infrastructure and monitoring; the overall score is the weakest section, which keeps teams from neglecting any of them.

### Sources

- Breck, E., Cai, S., Nielsen, E., Salib, M. & Sculley, D. (2017). The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction. *IEEE International Conference on Big Data 2017*. [Google Research](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Der ML Test Score ist eine Bewertungsrubrik von Google aus 28 konkreten Tests und Monitoring-Anforderungen, die misst, wie produktionsreif ein System des maschinellen Lernens ist und wie viel technische Schuld es trägt (Breck et al., 2017). Die Tests verteilen sich auf vier Abschnitte zu je sieben: Merkmale und Daten, Modellentwicklung, ML-Infrastruktur und Monitoring. Jeder Test bringt einen halben Punkt, wenn er manuell ausgeführt und dokumentiert wird, und einen ganzen Punkt, wenn er automatisch läuft; der Gesamtwert ist das Minimum der vier Abschnittswerte, sodass kein Bereich vernachlässigt werden kann (Breck et al., 2017). Die Rubrik ergänzt allgemeine Softwaretechnik wie Unit-Tests, ersetzt sie aber nicht ([[software-testing|Softwaretests]]).

### Funktionsweise

```text
4 Abschnitte × 7 Tests = 28 Zusicherungen
  Daten        Schema, Nutzen und Kosten von Merkmalen, Datenschutz, getesteter Merkmalscode, ...
  Modell       geprüfte Spezifikationen, Offline- ↔ Online-Metriken, Baseline, Datenausschnitte, Inklusion, ...
  Infra        reproduzierbares Training, Unit- + Integrationstests, Validierung vor dem Ausrollen, Canary, Rollback, ...
  Monitoring   Abhängigkeiten, Dateninvarianten, Training/Serving-Skew, Veralterung, Stabilität, Latenz, Qualität
je Test: 0 = nicht umgesetzt | 0,5 = manuell, dokumentiert | 1 = automatisiert, wiederholt
Abschnittswert = Summe ; ML Test Score = min(Abschnittswerte)
```

#### 1. Warum ML-Systeme eigene Tests brauchen

Das Verhalten von ML-Systemen hängt stark von Daten und Modellen ab, die sich nicht im Voraus festlegen lassen; in Analogie zur Kompilierung brauchen Trainingsdaten Tests wie Code, und ein trainiertes Modell braucht Produktionspraktiken wie ein Binary, etwa Debugbarkeit, Rollbacks und Monitoring (Breck et al., 2017). In einer Umfrage unter mehreren Dutzend Google-Teams setzten bei keinem Test mehr als 80 % der Teams ihn um, doch die meisten Tests hatten bei mindestens der Hälfte der Teams einen Wert über null (Breck et al., 2017).

#### 2. Tests für Merkmale und Daten

Die sieben Datentests: Erwartungen an Merkmale sind in einem Schema erfasst, alle Merkmale sind nützlich, kein Merkmal kostet zu viel, Merkmale erfüllen übergeordnete Anforderungen, die Datenpipeline hat angemessene Datenschutzkontrollen, neue Merkmale lassen sich schnell hinzufügen, und der gesamte Code für Eingabemerkmale ist getestet (Breck et al., 2017). Das Schema kann von Statistiken der Trainingsdaten ausgehen, die mit Domänenwissen angepasst werden, und dient später dem Monitoring der Eingaben. Zu den Datenschutztests gehört die Prüfung, dass eine von Nutzenden verlangte Datenlöschung bis in die Trainingspipeline und in gelernte Modelle durchgreift (Breck et al., 2017; [[data-governance|Data Governance]]).

#### 3. Tests für die Modellentwicklung

Modellspezifikationen werden geprüft und in ein Repository eingecheckt; Offline-Ersatzmetriken korrelieren mit der Online-Wirkung; alle Hyperparameter sind abgestimmt; die Auswirkung veralteter Modelle ist bekannt; ein einfacheres Modell ist nicht besser; die Modellqualität reicht auf allen wichtigen Datenausschnitten; und das Modell wurde auf Inklusionsaspekte getestet (Breck et al., 2017). Das Aufteilen in Ausschnitte verhindert, dass eine globale Metrik Probleme verdeckt, etwa wenn die globale Accuracy um 1 % steigt, während sie für ein Land um 50 % fällt (Breck et al., 2017). Der Inklusionstest prüft, ob Eingabemerkmale stark mit geschützten Nutzergruppen korrelieren und ob sich Vorhersagen zwischen Nutzergruppen deutlich unterscheiden ([[fairness-metrics|Fairness-Metriken]]).

#### 4. Tests für die ML-Infrastruktur

Training ist reproduzierbar; Code der Modellspezifikation hat Unit-Tests; die gesamte ML-Pipeline hat Integrationstests; die Modellqualität wird vor dem Ausrollen validiert; das Modell lässt sich an einem einzelnen Beispiel Schritt für Schritt debuggen; Modelle durchlaufen vor dem Ausrollen einen Canary-Prozess; und ausgerollte Modelle lassen sich schnell und sicher zurückrollen (Breck et al., 2017). Ein nützlicher Unit-Test trainiert ein Modell einen einzigen Gradientenschritt lang auf zufälligen Eingaben, um Fehler in der Bibliotheksnutzung zu finden; „Golden Tests“, die ein teilweise trainiertes Modell mit einem gespeicherten vergleichen, sind schwer zu pflegen und sollten vermieden werden (Breck et al., 2017). Die Validierung vor dem Ausrollen prüft sowohl schleichende Verschlechterung über viele Versionen als auch plötzliche Einbrüche gegenüber dem vorherigen Modell ([[regression-testing|Regressionstests]]).

#### 5. Monitoring-Tests

Änderungen an Abhängigkeiten lösen Benachrichtigungen aus; Dateninvarianten gelten für Trainings- und Betriebseingaben; Training und Betrieb berechnen dieselben Merkmalswerte; Modelle sind nicht zu alt; Modelle sind numerisch stabil, etwa ohne NaNs oder Unendlichkeiten; die Rechenleistung hat sich nicht verschlechtert; und die Vorhersagequalität auf Betriebsdaten hat sich nicht verschlechtert (Breck et al., 2017). Training/Serving-Skew entsteht, wenn sich die Codepfade zur Merkmalsberechnung zwischen Training und Inferenz unterscheiden, und wird erkannt, indem eine Stichprobe des Betriebsverkehrs protokolliert und Merkmalswerte oder Verteilungen verglichen werden (Breck et al., 2017; [[monitoring-and-alerting|Monitoring und Alerting]]).

#### Herkunft und Varianten

Breck, Cai, Nielsen, Salib und Sculley von Google stellten die Rubrik auf der IEEE Big Data 2017 vor, gestützt auf Erfahrungen mit Produktionssystemen wie der Vorhersage von Anzeigenklicks und auf Interviews mit 36 Teams (Breck et al., 2017). Vorbild war Googles Programm Test Certified, eine bewertete Stufenleiter für robuste Tests. Unter den befragten Teams gehörten Integrationstests der gesamten Pipeline und das Monitoring von Training/Serving-Skew zu den am seltensten umgesetzten Tests, während Canarying verbreitet war; ein hypothetisches System mit der Pipeline-Plattform TFX und ihren Standardempfehlungen galt bereits als „angemessen getestet“ (Breck et al., 2017).

### Wann einsetzen

- Bewertung der Produktionsreife eines ML-Systems vor dem Start oder in einem Review ([[mlops-and-deployment|MLOps und Deployment]]).
- Priorisierung des Abbaus technischer Schuld mit einem messbaren Wert (Breck et al., 2017).
- Als Checkliste beim Entwurf von [[ml-pipelines|ML-Pipelines]] und ihren CI/CD-Prüfungen ([[ci-cd|CI/CD]]).

### Stärken und Grenzen

**Stärken**
- Konkrete, umsetzbare Zusicherungen mit Hinweisen zur Umsetzung je Test (Breck et al., 2017).
- Das Minimum über die Abschnitte erzwingt Aufmerksamkeit für alle vier Bereiche (Breck et al., 2017).
- Checklisten halfen selbst erfahrenen Teams, etwa beim Entdecken einer tausendzeiligen, ungetesteten Merkmalsdatei (Breck et al., 2017).

**Grenzen**
- Ausgerichtet auf überwachte Systeme, die kontinuierlich trainiert und online mit geringer Latenz betrieben werden, auch wenn sich die meisten Ratschläge übertragen lassen (Breck et al., 2017).
- Teams, die nur mit Bild- oder Audiodaten arbeiten, fanden viele Datentests weniger passend (Breck et al., 2017).
- Teure Labels erschweren Qualitätstests wie die Auswirkung veralteter Modelle und die Validierung vor dem Ausrollen (Breck et al., 2017).
- Das Minimum verringert, wie sehr sich der Einsatz Einzelner im Wert zeigt (Breck et al., 2017).
- Vor LLM-basierten Systemen geschrieben; Tests für Prompts, Retrieval oder generierten Text sind nicht abgedeckt.

### Vergleich

| Wert | Deutung |
|---|---|
| 0 | eher ein Forschungsprojekt als ein produktives System |
| (0, 1] | nicht völlig ungetestet, aber ernste Lücken in der Zuverlässigkeit sind möglich |
| (1, 2] | ein erster Schritt zur grundlegenden Produktionsreife |
| (2, 3] | angemessen getestet, mehr ließe sich automatisieren |
| (3, 5] | starkes automatisiertes Testen und Monitoring, geeignet für geschäftskritische Systeme |
| > 5 | außergewöhnliches automatisiertes Testen und Monitoring |

Quelle: Breck et al. (2017), Tabelle V.

### In der Praxis

Das System wird in einem kurzen strukturierten Interview bewertet, wie es die Autoren mit 36 Teams taten, und dann wird zuerst der schwächste Abschnitt verbessert, da er den Wert bestimmt (Breck et al., 2017). Manuell ausgeführte Tests sollten automatisiert werden, weil nur automatisierte, wiederholte Tests einen ganzen Punkt bringen. Training/Serving-Skew verdient früh Aufmerksamkeit: Er verursachte bei vielen Teams Produktionsprobleme, wurde aber selten getestet (Breck et al., 2017). Die Monitoring-Tests der Rubrik entsprechen direkt der Drift- und Qualitätsüberwachung im Betrieb ([[quality-control|Qualitätskontrolle]]).

### Merksatz

Der ML Test Score übersetzt die Produktionsreife von ML in 28 prüfbare Zusicherungen zu Daten, Modell, Infrastruktur und Monitoring; der Gesamtwert ist der schwächste Abschnitt, was verhindert, dass Teams einen davon vernachlässigen.

### Quellen

- Breck, E., Cai, S., Nielsen, E., Salib, M. & Sculley, D. (2017). The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction. *IEEE International Conference on Big Data 2017*. [Google Research](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)
