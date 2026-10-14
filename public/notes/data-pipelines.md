---
title_en: Data Pipelines
title_de: Datenpipelines
entity_type: Concept
aliases:
- Data pipeline
- ETL
- ELT
sources:
- https://www.getdbt.com/blog/extract-load-transform
- https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html
- https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
- https://kafka.apache.org/intro
- https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A data pipeline moves data from sources such as databases, applications and sensors into a system where it is stored, transformed and used, for example a data warehouse, a search index or a [[knowledge-graphs|knowledge graph]]. Pipelines either transform before loading (ETL) or load raw data first and transform it in the warehouse (ELT) (dbt: ELT), run as scheduled batches orchestrated as task graphs (Airflow docs: Overview) or continuously on event streams (Kafka docs: Introduction), and must produce the same result when a step is re-run (Airflow docs: Best practices).

### How it works

A pipeline is a chain of steps whose dependencies form a directed acyclic graph:

```text
sources ──extract──► raw storage ──transform──► cleaned / modelled data ──► consumers
 (DBs, APIs,           (staging,      (validate, join,       (warehouse tables,     (dashboards,
  files, events)        topics)        aggregate, enrich)     index, graph)          ML, RAG)
          ▲                                                                   │
          └──────────── orchestration: schedule, dependencies, retries ◄──────┘
```

#### 1. Extract

Data is read from operational sources: databases, files, [[apis|APIs]] or event streams. In event streaming, events are captured in real time from sources such as databases, sensors and mobile devices; an event records that something happened and has a key, a value, a timestamp and optional headers (Kafka docs: Introduction).

#### 2. Load and transform: ETL or ELT

In ETL, the traditional standard for moving data from several sources into a central system, data is transformed before it is loaded into the warehouse. ELT flips the order: raw data is loaded first and transformed later inside the warehouse, using its computing power (dbt: ELT). ELT makes data available sooner and keeps transformations flexible, but stores raw data in the warehouse, which raises storage costs and security and compliance questions (dbt: ELT).

#### 3. Batch and streaming

Batch pipelines process a fixed slice of data per run, identified by its data interval (Airflow docs: Best practices). Streaming pipelines process events continuously: in Kafka, producers write events to topics, consumers read them, and both are fully decoupled; topics are partitioned across servers, events with the same key go to the same partition and are read in the order written, and topics can be replicated, commonly with a replication factor of 3 (Kafka docs: Introduction). Kafka Connect imports and exports data as event streams, and Kafka Streams implements stream processing applications (Kafka docs: Introduction). Akidau et al. (2015) argue that large unbounded, unordered datasets should not be forced into finite batches; their Dataflow Model instead lets practitioners choose the trade-off between correctness, latency and cost.

#### 4. Orchestration

An orchestrator runs the steps in order. In Apache Airflow, a workflow is a DAG (directed acyclic graph) of tasks; tasks fetch data, run analyses or trigger other systems, and the DAG defines the order through task dependencies. Operators are predefined tasks, and the scheduler triggers scheduled workflows and submits tasks to an executor (Airflow docs: Overview).

#### 5. Idempotent re-runs

Because a failed task is retried, every task should produce the same outcome on every re-run; tasks are treated like database transactions (Airflow docs: Best practices). In practice this means: write with UPSERT instead of INSERT, which would duplicate rows on a re-run; never read "the latest" data but a fixed data interval, for example partitioned by the interval start; do not compute critical values from the current time; and exchange larger data between tasks through remote storage, not the local file system, as the next task may run on another server (Airflow docs: Best practices).

#### 6. Origin and variants

ETL predates ELT, which moved transformation into the warehouse (dbt: ELT). Event streaming platforms such as Kafka (Kafka docs: Introduction) and the Dataflow Model for unbounded data (Akidau et al., 2015) extended pipelines from scheduled batches to continuous processing.

### When to use it

- Whenever data from several sources must be combined for analysis, reporting or machine learning ([[mlops-and-deployment|MLOps and Deployment]]).
- To feed retrieval systems: documents are extracted, split and embedded for [[retrieval-augmented-generation|RAG]], or entities and relations are extracted into a [[knowledge-graphs|knowledge graph]] ([[knowledge-graph-engineering|Knowledge Graph Engineering]]).
- Batch with an orchestrator when results are needed per day or hour; streaming when events must be processed as they happen (Airflow docs: Overview; Kafka docs: Introduction).

### Strengths and limitations

**Strengths**
- Automates recurring data movement with defined dependencies and retries (Airflow docs: Overview; Airflow docs: Best practices).
- ELT keeps raw data, so transformations can be changed and re-run later (dbt: ELT).
- Event streaming decouples producers from consumers and stores events durably (Kafka docs: Introduction).

**Limitations**
- Non-idempotent steps produce duplicates or different results on retries (Airflow docs: Best practices).
- Raw data in the warehouse costs storage and can pose security and compliance risks (dbt: ELT).
- Unbounded, out-of-order data forces a trade-off between correctness, latency and cost (Akidau et al., 2015).

### Comparison

| Approach | Transformation | Typical use |
|----------|----------------|-------------|
| ETL | Before loading (dbt: ELT) | Fixed target schemas, sensitive raw data |
| ELT | In the warehouse after loading (dbt: ELT) | Analytics with changing questions |
| Orchestrated batch | Scheduled task DAG (Airflow docs: Overview) | Daily or hourly loads, ML training data |
| Event streaming | Continuous, per event (Kafka docs: Introduction) | Real-time processing, decoupled services |

### In practice

DAGs are production code: they get tests, and a staging environment runs the complete DAG before deployment (Airflow docs: Best practices). XCom passes only small messages between Airflow tasks (Airflow docs: Best practices). In Kafka, retention is configured per topic, so events can be read again later (Kafka docs: Introduction).

### Key takeaway

A data pipeline extracts, loads and transforms data as a graph of steps, in batches or as a stream; each step must give the same result when it is re-run.

### Sources

- dbt Labs. *Extract, Load, Transform (ELT).* [getdbt.com](https://www.getdbt.com/blog/extract-load-transform)
- Apache Software Foundation. *Architecture Overview.* Apache Airflow documentation. [airflow.apache.org](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)
- Apache Software Foundation. *Best Practices.* Apache Airflow documentation. [airflow.apache.org](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- Apache Software Foundation. *Introduction.* Apache Kafka documentation. [kafka.apache.org](https://kafka.apache.org/intro)
- Akidau, T. et al. (2015). *The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing.* Proceedings of the VLDB Endowment 8. [research.google](https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Eine Datenpipeline bringt Daten aus Quellen wie Datenbanken, Anwendungen und Sensoren in ein System, in dem sie gespeichert, transformiert und genutzt werden, etwa ein Data Warehouse, einen Suchindex oder einen [[knowledge-graphs|Knowledge Graph]]. Pipelines transformieren entweder vor dem Laden (ETL) oder laden zuerst Rohdaten und transformieren sie im Warehouse (ELT) (dbt: ELT), laufen als geplante Batches, orchestriert als Task-Graphen (Airflow docs: Overview), oder fortlaufend auf Event-Streams (Kafka docs: Introduction), und müssen bei einer Wiederholung eines Schritts dasselbe Ergebnis liefern (Airflow docs: Best practices).

### Funktionsweise

Eine Pipeline ist eine Kette von Schritten, deren Abhängigkeiten einen gerichteten azyklischen Graphen bilden:

```text
Quellen ──Extract──► Rohdaten ──Transform──► bereinigte / modellierte Daten ──► Nutzer
 (DBs, APIs,          (Staging,     (prüfen, verknüpfen,    (Warehouse-Tabellen,     (Dashboards,
  Dateien, Events)     Topics)       aggregieren, anreichern) Index, Graph)            ML, RAG)
          ▲                                                                   │
          └──────────── Orchestrierung: Zeitplan, Abhängigkeiten, Wiederholungen ◄──┘
```

#### 1. Extract

Daten werden aus operativen Quellen gelesen: Datenbanken, Dateien, [[apis|APIs]] oder Event-Streams. Beim Event Streaming werden Ereignisse in Echtzeit aus Quellen wie Datenbanken, Sensoren und Mobilgeräten erfasst; ein Event hält fest, dass etwas passiert ist, und hat einen Schlüssel, einen Wert, einen Zeitstempel und optionale Header (Kafka docs: Introduction).

#### 2. Laden und Transformieren: ETL oder ELT

Bei ETL, dem traditionellen Standard, um Daten aus mehreren Quellen in ein zentrales System zu bringen, werden die Daten vor dem Laden ins Warehouse transformiert. ELT dreht die Reihenfolge um: Rohdaten werden zuerst geladen und später im Warehouse transformiert, mit dessen Rechenleistung (dbt: ELT). ELT macht Daten schneller verfügbar und hält Transformationen flexibel, speichert aber Rohdaten im Warehouse, was Speicherkosten sowie Sicherheits- und Compliance-Fragen aufwirft (dbt: ELT).

#### 3. Batch und Streaming

Batch-Pipelines verarbeiten pro Lauf einen festen Ausschnitt der Daten, bestimmt durch sein Datenintervall (Airflow docs: Best practices). Streaming-Pipelines verarbeiten Events fortlaufend: In Kafka schreiben Producer Events in Topics, Consumer lesen sie, und beide sind vollständig entkoppelt; Topics sind über Server partitioniert, Events mit demselben Schlüssel landen in derselben Partition und werden in der geschriebenen Reihenfolge gelesen, und Topics lassen sich replizieren, üblich ist ein Replikationsfaktor von 3 (Kafka docs: Introduction). Kafka Connect importiert und exportiert Daten als Event-Streams, Kafka Streams setzt Anwendungen zur Stream-Verarbeitung um (Kafka docs: Introduction). Akidau et al. (2015) argumentieren, dass große unbegrenzte, ungeordnete Datenmengen nicht in endliche Batches gezwängt werden sollten; ihr Dataflow-Modell lässt stattdessen den Kompromiss zwischen Korrektheit, Latenz und Kosten bewusst wählen.

#### 4. Orchestrierung

Ein Orchestrator führt die Schritte in der richtigen Reihenfolge aus. In Apache Airflow ist ein Workflow ein DAG (Directed Acyclic Graph) aus Tasks; Tasks holen Daten, führen Analysen aus oder stoßen andere Systeme an, und der DAG legt die Reihenfolge über die Abhängigkeiten der Tasks fest. Operatoren sind vordefinierte Tasks, und der Scheduler startet geplante Workflows und übergibt Tasks an einen Executor (Airflow docs: Overview).

#### 5. Idempotente Wiederholungen

Weil ein fehlgeschlagener Task wiederholt wird, sollte jeder Task bei jeder Wiederholung dasselbe Ergebnis liefern; Tasks werden wie Datenbanktransaktionen behandelt (Airflow docs: Best practices). Praktisch heißt das: mit UPSERT statt INSERT schreiben, das bei einer Wiederholung Zeilen doppelt anlegen würde; nie „die neuesten“ Daten lesen, sondern ein festes Datenintervall, etwa nach dessen Beginn partitioniert; kritische Werte nicht aus der aktuellen Uhrzeit berechnen; und größere Daten zwischen Tasks über entfernten Speicher austauschen, nicht über das lokale Dateisystem, da der nächste Task auf einem anderen Server laufen kann (Airflow docs: Best practices).

#### 6. Herkunft und Varianten

ETL ist älter als ELT, das die Transformation ins Warehouse verlegt hat (dbt: ELT). Event-Streaming-Plattformen wie Kafka (Kafka docs: Introduction) und das Dataflow-Modell für unbegrenzte Daten (Akidau et al., 2015) haben Pipelines von geplanten Batches auf fortlaufende Verarbeitung erweitert.

### Wann einsetzen

- Immer wenn Daten aus mehreren Quellen für Analyse, Reporting oder Machine Learning zusammengeführt werden ([[mlops-and-deployment|MLOps und Deployment]]).
- Um Retrieval-Systeme zu versorgen: Dokumente werden für [[retrieval-augmented-generation|RAG]] extrahiert, zerlegt und eingebettet, oder Entitäten und Relationen werden in einen [[knowledge-graphs|Knowledge Graph]] extrahiert ([[knowledge-graph-engineering|Knowledge Graph Engineering]]).
- Batch mit Orchestrator, wenn Ergebnisse pro Tag oder Stunde reichen; Streaming, wenn Events sofort verarbeitet werden müssen (Airflow docs: Overview; Kafka docs: Introduction).

### Stärken und Grenzen

**Stärken**
- Automatisiert wiederkehrende Datenbewegungen mit festgelegten Abhängigkeiten und Wiederholungen (Airflow docs: Overview; Airflow docs: Best practices).
- ELT behält die Rohdaten, sodass Transformationen später geändert und neu ausgeführt werden können (dbt: ELT).
- Event Streaming entkoppelt Producer und Consumer und speichert Events dauerhaft (Kafka docs: Introduction).

**Grenzen**
- Nicht idempotente Schritte erzeugen bei Wiederholungen Duplikate oder andere Ergebnisse (Airflow docs: Best practices).
- Rohdaten im Warehouse kosten Speicher und können Sicherheits- und Compliance-Risiken bergen (dbt: ELT).
- Unbegrenzte, ungeordnete Daten erzwingen einen Kompromiss zwischen Korrektheit, Latenz und Kosten (Akidau et al., 2015).

### Vergleich

| Ansatz | Transformation | Typischer Einsatz |
|--------|----------------|-------------------|
| ETL | Vor dem Laden (dbt: ELT) | Feste Zielschemata, sensible Rohdaten |
| ELT | Im Warehouse nach dem Laden (dbt: ELT) | Analysen mit wechselnden Fragen |
| Orchestrierter Batch | Geplanter Task-DAG (Airflow docs: Overview) | Tägliche oder stündliche Ladevorgänge, ML-Trainingsdaten |
| Event Streaming | Fortlaufend, pro Event (Kafka docs: Introduction) | Echtzeitverarbeitung, entkoppelte Dienste |

### In der Praxis

DAGs sind Produktionscode: Sie bekommen Tests, und eine Staging-Umgebung führt den vollständigen DAG vor dem Deployment aus (Airflow docs: Best practices). XCom reicht zwischen Airflow-Tasks nur kleine Nachrichten weiter (Airflow docs: Best practices). In Kafka wird die Aufbewahrungsdauer pro Topic eingestellt, sodass Events später erneut gelesen werden können (Kafka docs: Introduction).

### Merksatz

Eine Datenpipeline extrahiert, lädt und transformiert Daten als Graph von Schritten, in Batches oder als Stream; jeder Schritt muss bei einer Wiederholung dasselbe Ergebnis liefern.

### Quellen

- dbt Labs. *Extract, Load, Transform (ELT).* [getdbt.com](https://www.getdbt.com/blog/extract-load-transform)
- Apache Software Foundation. *Architecture Overview.* Apache Airflow documentation. [airflow.apache.org](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)
- Apache Software Foundation. *Best Practices.* Apache Airflow documentation. [airflow.apache.org](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- Apache Software Foundation. *Introduction.* Apache Kafka documentation. [kafka.apache.org](https://kafka.apache.org/intro)
- Akidau, T. et al. (2015). *The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing.* Proceedings of the VLDB Endowment 8. [research.google](https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/)
