---
title_en: Data Quality
title_de: Datenqualität
entity_type: Concept
aliases:
- Data quality
- Data quality dimensions
- Data validation
- Training-serving skew
- Datenqualität
sources:
- https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework
- https://mlsys.org/Conferences/2019/doc/2019/167.pdf
- https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng
- https://eur-lex.europa.eu/eli/reg/2024/1689/oj/deu
- https://www.bis.org/publ/bcbs239.htm
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Data quality describes how fit data is for its intended use. The UK Government Data Quality Framework measures it along six dimensions defined by DAMA UK, completeness, uniqueness, consistency, timeliness, validity and accuracy, and checks it at every stage of the data lifecycle (Government Data Quality Hub, 2020). For machine learning, errors in training or serving data can cancel out any gain from better algorithms, so production systems validate every batch of data against a schema and watch for skew between training and serving data (Breck et al., 2019). Regulation sets data quality requirements too, for example for the training data of high-risk AI systems under the [[eu-ai-act|EU AI Act]] and for bank risk data under [[bcbs-239-and-ecb-rdarr-guide|BCBS 239]].

### How it works

```text
plan ──► collect / ingest ──► prepare, store, maintain ──► use, process ──► share, publish ──► archive / destroy
  │            │                       │                         │                │
  rules,       validation at source,   cleaning, linking,        log errors,      document quality,
  standards    metadata                monitoring for decay      risk-based use   metadata
   ▼
measure: completeness · uniqueness · consistency · timeliness · validity · accuracy   (DAMA UK)
   ▼
ML pipelines: schema per feature ──► validate each batch ──► alert ──► fix data or update schema
              compare training vs serving data ──► detect feature, distribution and scoring skew
```

#### 1. Dimensions

DAMA UK's six core dimensions, as adopted by the UK framework, make quality measurable (Government Data Quality Hub, 2020):

- **Completeness:** the degree to which records are present and essential values filled; 294 of 300 emergency contact numbers recorded is 98% complete.
- **Uniqueness:** no duplicate records; 501 records for 500 students (Fred Smith entered twice as "Freddy Smith") is 99.8% unique.
- **Consistency:** values do not contradict other values for the same entity, within or across data sets, such as a mother's date of birth before her child's.
- **Timeliness:** data reflects the period it represents and is available soon enough for its use.
- **Validity:** values are in the expected range and format, for example an age between 4 and 11 for primary school applications.
- **Accuracy:** data matches reality; a valid US-format date of birth read as a UK date is valid but inaccurate.

The list is not prescriptive; dimensions are prioritised by user needs, and they trade off, for example timeliness against completeness or accuracy, as when monthly GDP estimates were introduced (Government Data Quality Hub, 2020).

#### 2. Quality across the lifecycle

Problems arise at each lifecycle stage: poor collection design and missing validation rules when planning; manual entry errors, duplicates and inconsistent formats at ingestion; faulty linking, missing metadata and accuracy decaying over time in storage; unlogged errors and human mistakes during analysis; and undocumented quality when data is shared (Government Data Quality Hub, 2020). Quality should therefore be assessed at every stage and documented for later users ([[data-governance|data governance]], [[data-pipelines|data pipelines]]).

#### 3. Data validation for machine learning

[[google|Google]]'s data validation system in TFX checks petabytes of training and serving data per day for hundreds of product teams (Breck et al., 2019). A schema codifies the expectations for each feature, such as type, presence and value domain; unlike in databases, the data comes first, so the schema is inferred from data and co-evolves with it under human review (Breck et al., 2019). Each new batch is validated against the schema and alerts must be high-precision and actionable; statistical tests such as chi-squared proved too sensitive at this scale (Breck et al., 2019). The schema is also used to unit-test training code, revealing mismatches between the data and the algorithm's assumptions ([[software-testing|software testing]], [[ml-test-score|ML test score]]).

#### 4. Training–serving skew

Training and serving data often come from different code paths and drift apart (Breck et al., 2019). Feature skew means a feature takes different values in training and serving, for example when a click count is looked up later for training data and therefore includes clicks that happened after serving ("time travel"); distribution skew means the overall distributions differ, for example through a flawed sampling scheme; scoring/serving skew arises when only served items get labels, creating a feedback loop against lower-ranked items (Breck et al., 2019; [[recommender-systems|recommender systems]]). The validator continuously compares logged serving data with training data to detect these (Breck et al., 2019; [[monitoring-and-alerting|monitoring and alerting]]).

#### Origin and variants

The six dimensions come from a DAMA UK working group paper and were adopted by the UK Government Data Quality Framework in 2020 (Government Data Quality Hub, 2020). Breck et al. (2019) describe the data-centric approach to ML that treats data as a production asset on a par with algorithms and infrastructure, implemented in the open-source TensorFlow Data Validation library.

### When to use it

- Defining measurable rules and service levels for data used in decisions and reporting (Government Data Quality Hub, 2020).
- Guarding [[ml-pipelines|ML pipelines]] with schema validation and skew detection before training and deployment (Breck et al., 2019; [[mlops-and-deployment|MLOps]]).
- Meeting regulatory data requirements in AI and banking (see Regulatory context).

### Strengths and limitations

**Strengths**
- Dimensions turn vague complaints into measurable checks (Government Data Quality Hub, 2020).
- Early validation catches errors before they propagate through feedback loops and degrade models (Breck et al., 2019).

**Limitations**
- Perfect quality is rarely achievable; dimensions must be prioritised and traded off (Government Data Quality Hub, 2020).
- Valid or complete data can still be inaccurate (Government Data Quality Hub, 2020).
- Validation rules can raise spammy or non-actionable alerts if not tuned (Breck et al., 2019).
- Bias makes data unrepresentative, an accuracy problem that format checks do not detect (Government Data Quality Hub, 2020; [[bias-in-nlp|bias]]).

### Comparison

| Dimension | Question | Typical check |
|---|---|---|
| Completeness | Are all records and essential values there? | share of non-missing values |
| Uniqueness | Is each entity recorded once? | duplicate detection ([[near-duplicate-detection\|near-duplicates]]) |
| Consistency | Do values agree within and across data sets? | cross-field and cross-system rules |
| Timeliness | Is the data recent enough? | lag against agreed service level |
| Validity | Are values in the expected format and range? | schema and range rules |
| Accuracy | Does the data match reality? | comparison with a trusted source |

Source: Government Data Quality Hub (2020).

### Regulatory context

Under Article 10(3) of the [[eu-ai-act|EU AI Act]], training, validation and testing data sets of high-risk AI systems must be relevant, sufficiently representative and, as far as possible, free of errors and complete in view of their intended purpose, with appropriate statistical properties (Regulation (EU) 2024/1689). [[bcbs-239-and-ecb-rdarr-guide|BCBS 239]] requires banks to produce accurate risk data aggregated largely automatically (Principle 3) and to capture all material risk data across the group (Principle 4) (Basel Committee on Banking Supervision, 2013).

### Key takeaway

Data quality is fitness for use, measured along dimensions such as completeness, validity and accuracy and checked throughout the lifecycle; in ML it means validating every batch against a schema and catching training–serving skew.

### Sources

- Government Data Quality Hub (2020). *The Government Data Quality Framework.* GOV.UK. [gov.uk](https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework)
- Breck, E., Polyzotis, N., Roy, S., Whang, S. E. & Zinkevich, M. (2019). *Data Validation for Machine Learning.* SysML 2019. [mlsys.org](https://mlsys.org/Conferences/2019/doc/2019/167.pdf)
- Regulation (EU) 2024/1689 (Artificial Intelligence Act), Article 10. [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)
- Basel Committee on Banking Supervision (2013). *Principles for effective risk data aggregation and risk reporting* (BCBS 239). [bis.org](https://www.bis.org/publ/bcbs239.htm)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Datenqualität beschreibt, wie gut Daten für ihren vorgesehenen Zweck geeignet sind. Das Data Quality Framework der britischen Regierung misst sie entlang von sechs von DAMA UK definierten Dimensionen, Vollständigkeit, Eindeutigkeit, Konsistenz, Aktualität, Gültigkeit und Richtigkeit, und prüft sie in jeder Phase des Datenlebenszyklus (Government Data Quality Hub, 2020). Beim maschinellen Lernen können Fehler in Trainings- oder Betriebsdaten jeden Gewinn durch bessere Algorithmen zunichtemachen; Produktivsysteme validieren daher jeden Datenbatch gegen ein Schema und achten auf Abweichungen zwischen Trainings- und Betriebsdaten (Breck et al., 2019). Auch Regulierung stellt Anforderungen an die Datenqualität, etwa an die Trainingsdaten von Hochrisiko-KI-Systemen nach der [[eu-ai-act|KI-Verordnung]] und an Risikodaten von Banken nach [[bcbs-239-and-ecb-rdarr-guide|BCBS 239]].

### Funktionsweise

```text
planen ──► erheben / übernehmen ──► aufbereiten, speichern, pflegen ──► nutzen, verarbeiten ──► teilen, veröffentlichen ──► archivieren / löschen
  │              │                          │                              │                   │
  Regeln,        Validierung an der Quelle, Bereinigung, Verknüpfung,     Fehler protokollieren, Qualität dokumentieren,
  Standards      Metadaten                  Überwachung auf Verfall        risikobasierte Nutzung Metadaten
   ▼
messen: Vollständigkeit · Eindeutigkeit · Konsistenz · Aktualität · Gültigkeit · Richtigkeit   (DAMA UK)
   ▼
ML-Pipelines: Schema pro Merkmal ──► jeden Batch validieren ──► Alarm ──► Daten korrigieren oder Schema anpassen
              Trainings- mit Betriebsdaten vergleichen ──► Feature-, Verteilungs- und Scoring-Skew erkennen
```

#### 1. Dimensionen

Die sechs Kerndimensionen von DAMA UK, wie sie das britische Framework übernimmt, machen Qualität messbar (Government Data Quality Hub, 2020):

- **Vollständigkeit:** in welchem Maß Datensätze vorhanden und wesentliche Werte befüllt sind; 294 von 300 erfassten Notfallnummern sind 98 % vollständig.
- **Eindeutigkeit:** keine doppelten Datensätze; 501 Datensätze für 500 Schülerinnen und Schüler (Fred Smith zusätzlich als „Freddy Smith“ erfasst) sind zu 99,8 % eindeutig.
- **Konsistenz:** Werte widersprechen anderen Werten zur selben Entität nicht, innerhalb eines Datensatzes oder über Datensätze hinweg, etwa liegt das Geburtsdatum einer Mutter vor dem ihres Kindes.
- **Aktualität:** Die Daten spiegeln den Zeitraum, den sie darstellen, und stehen früh genug für ihren Zweck bereit.
- **Gültigkeit:** Werte liegen im erwarteten Bereich und Format, etwa ein Alter zwischen 4 und 11 bei Grundschulanmeldungen.
- **Richtigkeit:** Die Daten entsprechen der Wirklichkeit; ein im US-Format angegebenes Geburtsdatum, das als britisches Datum gelesen wird, ist gültig, aber falsch.

Die Liste ist nicht abschließend; Dimensionen werden nach den Bedürfnissen der Nutzenden gewichtet und stehen im Zielkonflikt, etwa Aktualität gegen Vollständigkeit oder Richtigkeit, wie bei der Einführung monatlicher Schätzungen des BIP (Government Data Quality Hub, 2020).

#### 2. Qualität über den Lebenszyklus

Probleme entstehen in jeder Phase: schlechtes Erhebungsdesign und fehlende Validierungsregeln bei der Planung; Eingabefehler, Duplikate und uneinheitliche Formate bei der Übernahme; fehlerhafte Verknüpfungen, fehlende Metadaten und mit der Zeit nachlassende Richtigkeit bei der Speicherung; nicht protokollierte Fehler und menschliche Irrtümer bei der Analyse; und undokumentierte Qualität beim Teilen von Daten (Government Data Quality Hub, 2020). Qualität sollte daher in jeder Phase bewertet und für spätere Nutzende dokumentiert werden ([[data-governance|Data Governance]], [[data-pipelines|Datenpipelines]]).

#### 3. Datenvalidierung für maschinelles Lernen

Das Datenvalidierungssystem von [[google|Google]] in TFX prüft für Hunderte Produktteams täglich Petabytes an Trainings- und Betriebsdaten (Breck et al., 2019). Ein Schema hält die Erwartungen an jedes Merkmal fest, etwa Typ, Vorhandensein und Wertebereich; anders als bei Datenbanken kommen die Daten zuerst, sodass das Schema aus den Daten abgeleitet wird und sich unter menschlicher Prüfung mit ihnen weiterentwickelt (Breck et al., 2019). Jeder neue Batch wird gegen das Schema validiert, und Alarme müssen präzise und umsetzbar sein; statistische Tests wie der Chi-Quadrat-Test erwiesen sich in diesem Maßstab als zu empfindlich (Breck et al., 2019). Das Schema dient außerdem dazu, Trainingscode per Unit-Test zu prüfen, was Abweichungen zwischen den Daten und den Annahmen des Algorithmus aufdeckt ([[software-testing|Softwaretests]], [[ml-test-score|ML Test Score]]).

#### 4. Training-Serving-Skew

Trainings- und Betriebsdaten stammen oft aus unterschiedlichen Codepfaden und laufen auseinander (Breck et al., 2019). Feature-Skew bedeutet, dass ein Merkmal im Training andere Werte annimmt als im Betrieb, etwa wenn eine Klickzahl für Trainingsdaten später abgefragt wird und daher Klicks enthält, die erst nach der Auslieferung geschahen („Zeitreise“); Verteilungs-Skew bedeutet, dass die Gesamtverteilungen abweichen, etwa durch ein fehlerhaftes Stichprobenverfahren; Scoring/Serving-Skew entsteht, wenn nur ausgelieferte Elemente Labels erhalten, was eine Rückkopplung gegen niedriger eingestufte Elemente erzeugt (Breck et al., 2019; [[recommender-systems|Recommender-Systeme]]). Der Validator vergleicht protokollierte Betriebsdaten laufend mit Trainingsdaten, um diese Abweichungen zu erkennen (Breck et al., 2019; [[monitoring-and-alerting|Monitoring und Alerting]]).

#### Ursprung und Varianten

Die sechs Dimensionen stammen aus einem Papier einer Arbeitsgruppe von DAMA UK und wurden 2020 vom Data Quality Framework der britischen Regierung übernommen (Government Data Quality Hub, 2020). Breck et al. (2019) beschreiben den datenzentrierten Ansatz für ML, der Daten als Produktionsgut gleichrangig mit Algorithmen und Infrastruktur behandelt, umgesetzt in der quelloffenen Bibliothek TensorFlow Data Validation.

### Wann einsetzen

- Messbare Regeln und Service-Levels für Daten festlegen, die in Entscheidungen und Berichte eingehen (Government Data Quality Hub, 2020).
- [[ml-pipelines|ML-Pipelines]] vor Training und Deployment mit Schemavalidierung und Skew-Erkennung absichern (Breck et al., 2019; [[mlops-and-deployment|MLOps]]).
- Regulatorische Datenanforderungen bei KI und im Bankwesen erfüllen (siehe Regulatorischer Kontext).

### Stärken und Grenzen

**Stärken**
- Dimensionen machen aus vagen Beschwerden messbare Prüfungen (Government Data Quality Hub, 2020).
- Frühe Validierung fängt Fehler ab, bevor sie sich über Rückkopplungen ausbreiten und Modelle verschlechtern (Breck et al., 2019).

**Grenzen**
- Perfekte Qualität ist selten erreichbar; Dimensionen müssen gewichtet und gegeneinander abgewogen werden (Government Data Quality Hub, 2020).
- Gültige oder vollständige Daten können trotzdem falsch sein (Government Data Quality Hub, 2020).
- Validierungsregeln können ohne Abstimmung zu viele oder nicht umsetzbare Alarme erzeugen (Breck et al., 2019).
- Verzerrungen machen Daten unrepräsentativ, ein Problem der Richtigkeit, das Formatprüfungen nicht erkennen (Government Data Quality Hub, 2020; [[bias-in-nlp|Bias]]).

### Vergleich

| Dimension | Frage | Typische Prüfung |
|---|---|---|
| Vollständigkeit | Sind alle Datensätze und wesentlichen Werte da? | Anteil nicht fehlender Werte |
| Eindeutigkeit | Ist jede Entität einmal erfasst? | Duplikaterkennung ([[near-duplicate-detection\|Beinahe-Duplikate]]) |
| Konsistenz | Stimmen Werte innerhalb und zwischen Datensätzen überein? | feld- und systemübergreifende Regeln |
| Aktualität | Sind die Daten aktuell genug? | Verzögerung gegenüber vereinbartem Service-Level |
| Gültigkeit | Liegen Werte im erwarteten Format und Bereich? | Schema- und Bereichsregeln |
| Richtigkeit | Entsprechen die Daten der Wirklichkeit? | Abgleich mit einer verlässlichen Quelle |

Quelle: Government Data Quality Hub (2020).

### Regulatorischer Kontext

Nach Artikel 10 Absatz 3 der [[eu-ai-act|KI-Verordnung]] müssen Trainings-, Validierungs- und Testdatensätze von Hochrisiko-KI-Systemen im Hinblick auf ihre Zweckbestimmung relevant, hinreichend repräsentativ und so weit wie möglich fehlerfrei und vollständig sein und angemessene statistische Merkmale aufweisen (Verordnung (EU) 2024/1689). [[bcbs-239-and-ecb-rdarr-guide|BCBS 239]] verlangt von Banken genaue, weitgehend automatisiert aggregierte Risikodaten (Grundsatz 3) und die Erfassung aller wesentlichen Risikodaten der Gruppe (Grundsatz 4) (Basler Ausschuss für Bankenaufsicht, 2013).

### Merksatz

Datenqualität ist Eignung für den Zweck, gemessen an Dimensionen wie Vollständigkeit, Gültigkeit und Richtigkeit und über den ganzen Lebenszyklus geprüft; im ML heißt das, jeden Batch gegen ein Schema zu validieren und Training-Serving-Skew abzufangen.

### Quellen

- Government Data Quality Hub (2020). *The Government Data Quality Framework.* GOV.UK. [gov.uk](https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework)
- Breck, E., Polyzotis, N., Roy, S., Whang, S. E. & Zinkevich, M. (2019). *Data Validation for Machine Learning.* SysML 2019. [mlsys.org](https://mlsys.org/Conferences/2019/doc/2019/167.pdf)
- Verordnung (EU) 2024/1689 (KI-Verordnung), Artikel 10. [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/deu)
- Basler Ausschuss für Bankenaufsicht (2013). *Principles for effective risk data aggregation and risk reporting* (BCBS 239). [bis.org](https://www.bis.org/publ/bcbs239.htm)
