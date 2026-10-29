---
title_en: Data Lakehouse
title_de: Data Lakehouse
entity_type: Concept
aliases:
- Data lakehouse
- Lakehouse
- Delta Lake
- Medallion architecture
- Data lake
sources:
- https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf
- https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf
- https://docs.databricks.com/aws/en/lakehouse/medallion
- https://docs.databricks.com/aws/en/data-governance/unity-catalog/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A lakehouse is "a data management system based on low-cost and directly-accessible storage that also provides traditional analytical DBMS management and performance features such as ACID transactions, data versioning, auditing, indexing, caching, and query optimization" (Armbrust et al., 2021). It replaces the common two-tier architecture, in which raw data lands in a data lake and a curated subset is copied again into a [[data-warehouse|data warehouse]], with one copy of the data in open file formats such as Apache Parquet on a cloud object store, plus a transactional metadata layer such as Delta Lake or Apache Iceberg on top (Armbrust et al., 2021). Business intelligence, data science and machine learning then work on the same tables. [[databricks|Databricks]], whose researchers set out the architecture, builds its platform on this design (Armbrust et al., 2021).

### How it works

```text
sources (operational databases, events, files, documents)
 ▼
cloud object store (S3, ADLS, GCS) with files in an open format (Parquet)
 ▼
metadata layer (Delta Lake, Iceberg, Hudi): transaction log, schema, versions, statistics
 ▼
medallion layers: bronze (raw) → silver (validated) → gold (business-level aggregates)
 ▼
engines: SQL for BI · DataFrame APIs for data science and ML · governance via a catalogue
```

#### 1. From warehouse to lake to lakehouse

First-generation analytics platforms loaded data from operational databases into a central warehouse with schema-on-write, optimised for business intelligence (Armbrust et al., 2021). As data grew and became unstructured (video, audio, text), raw data moved into data lakes: low-cost storage with a file API and open formats such as Parquet and ORC, first on Hadoop's HDFS and from 2015 on cloud object stores. The lake was schema-on-read and pushed quality and governance downstream, and a subset of its data was copied again into a warehouse; this two-tier architecture became dominant (Armbrust et al., 2021). Armbrust et al. (2021) name four problems with it: keeping lake and warehouse consistent is unreliable, warehouse data is stale, ML systems such as TensorFlow, PyTorch and XGBoost cannot read warehouse formats efficiently, and duplicated storage and proprietary formats raise cost and lock-in.

#### 2. The transactional metadata layer

Object stores only offer a key-value interface in which even updating a table that spans several files is not atomic (Armbrust et al., 2020). The lakehouse adds a metadata layer that records which files belong to which table version. Delta Lake stores this transaction log in the object store itself, compacted into Parquet, which provides ACID transactions, time travel to earlier versions, fast metadata operations over billions of objects, upserts and audit logs; Apache Iceberg, started at Netflix, uses a similar design, and Apache Hudi, started at Uber, focuses on streaming ingest (Armbrust et al., 2020; Armbrust et al., 2021). An existing directory of Parquet files can be turned into a Delta table without copying, by writing a log entry that references the files (Armbrust et al., 2021). The same layer enforces schemas and constraints, rejecting or quarantining records that violate them, and is a natural place for access control and audit logging (Armbrust et al., 2021).

#### 3. SQL performance on open formats

Because the file format is part of the public interface, a lakehouse cannot optimise storage freely as a closed warehouse does. Armbrust et al. (2021) propose three format-independent techniques: caching hot files on SSD or RAM of the compute nodes, which the transaction log makes safe; auxiliary data such as per-file min-max statistics for data skipping and Bloom-filter indexes; and data layout optimisation, for example ordering records with Z-order or Hilbert curves so that related records are read together. With these, the Delta Engine ran the TPC-DS benchmark at scale factor 30,000 faster and more cheaply than four popular cloud data warehouses in the authors' test (Armbrust et al., 2021).

#### 4. Machine learning on the same data

ML libraries can read open formats such as Parquet directly, and declarative DataFrame APIs let the engine optimise ML data access in the same way as [[sql|SQL]] queries (Armbrust et al., 2021). ML workloads therefore get transactions, versioning and governance without exporting data from a warehouse; the transaction log also makes it possible to reproduce training on a past version of a table (Armbrust et al., 2020). Compute is separate from storage, so a GPU cluster for training and a SQL cluster for reports can read the same tables (Armbrust et al., 2021). Distributed processing on these tables is usually done with [[apache-spark|Apache Spark]].

#### 5. Medallion architecture

Databricks recommends organising lakehouse tables in layers that "incrementally and progressively improve the structure and quality of data" (Databricks Medallion):
- **Bronze:** raw data in its original form, with provenance metadata but almost no clean-up, so that unexpected schema changes do not break ingestion.
- **Silver:** validated, cleaned and enriched data: schema enforcement, handling of nulls and late-arriving data, deduplication, quality checks and joins, with at least one validated, non-aggregated version of every record.
- **Gold:** refined views for analytics, [[data-visualisation|dashboards]], ML and applications, typically dimensional models and aggregates optimised for query performance.

The pattern is a recommended practice, not a requirement (Databricks Medallion). Modelling the gold layer is covered in [[data-modelling|data modelling]], the pipelines between the layers in [[data-pipelines|data pipelines]].

#### Origin and variants

Michael Armbrust, Ali Ghodsi, Reynold Xin and [[matei-zaharia|Matei Zaharia]] of Databricks set out the lakehouse architecture at CIDR 2021; Databricks had begun developing Delta Lake in 2016 and described it at VLDB 2020 (Armbrust et al., 2021; Armbrust et al., 2020). Governance across the lakehouse is provided by a catalogue such as Unity Catalog, which has an open-source implementation (Databricks Unity Catalog); see [[data-governance|data governance]].

### When to use it

- An organisation runs BI, data science and ML on the same data and wants to avoid copying it between a lake and a warehouse (Armbrust et al., 2021).
- Large or unstructured datasets (documents, images, sensor data) have to be stored cheaply but still queried with transactions and versioning (Armbrust et al., 2021).
- Training data must be reproducible from earlier table versions (Armbrust et al., 2020).

### Strengths and limitations

**Strengths**
- One copy of the data in an open format, readable by many engines, reduces lock-in and storage cost (Armbrust et al., 2021).
- ACID transactions, time travel and schema enforcement on cheap object storage (Armbrust et al., 2020).
- Fewer ETL steps and fresher data than the two-tier architecture (Armbrust et al., 2021).

**Limitations**
- Transactions in Delta Lake, Iceberg and Hudi cover one table at a time, and storing the log in the object store limits the transaction rate (Armbrust et al., 2021).
- Exposing the storage format gives up part of the data independence of a classic DBMS, which makes some optimisations harder (Armbrust et al., 2021).
- ETL logic to build curated tables is still needed (Armbrust et al., 2021).

### Comparison

| | Data warehouse | Data lake | Lakehouse |
|---|---|---|---|
| Storage | proprietary format, coupled to the engine | open files on cheap storage | open files on cheap storage |
| Schema | on write | on read | enforced by the metadata layer |
| Transactions, versioning | yes | no | yes |
| Unstructured data | hardly | yes | yes |
| Direct ML access | via export | yes | yes |

Source: Armbrust et al. (2021). Managed AI services on the major clouds are compared in [[cloud-ai-platforms|cloud AI platforms]]; the batch processing model behind early data lakes is described in [[mapreduce|MapReduce]].

### In practice

On Databricks, tables are governed in Unity Catalog with a three-level namespace `catalog.schema.table`, and models and model services are governed in the same catalogue (Databricks Unity Catalog). Ingestion frequency is a cost lever: continuous ingestion has the lowest latency and highest cost, batch ingestion the opposite (Databricks Medallion). Bronze tables keep most fields as strings or semi-structured types to survive source changes (Databricks Medallion).

### Key takeaway

A lakehouse keeps all data once, in open files on cheap object storage, and adds a transactional metadata layer that gives warehouse-like reliability and performance, so BI, data science and ML can share the same tables.

### Sources

- Armbrust, M., Ghodsi, A., Xin, R. & Zaharia, M. (2021). *Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics.* CIDR 2021. [cidrdb.org](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf)
- Armbrust, M., Das, T., Sun, L. et al. (2020). *Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores.* PVLDB 13(12), 3411–3424. [vldb.org](https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf)
- Databricks Medallion. *What is the medallion lakehouse architecture?* [docs.databricks.com](https://docs.databricks.com/aws/en/lakehouse/medallion)
- Databricks Unity Catalog. *What is Unity Catalog?* [docs.databricks.com](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Lakehouse ist „a data management system based on low-cost and directly-accessible storage that also provides traditional analytical DBMS management and performance features such as ACID transactions, data versioning, auditing, indexing, caching, and query optimization“ (Armbrust et al., 2021). Es ersetzt die verbreitete zweistufige Architektur, in der Rohdaten in einem Data Lake landen und ein aufbereiteter Teil noch einmal in ein [[data-warehouse|Data Warehouse]] kopiert wird, durch eine einzige Kopie der Daten in offenen Dateiformaten wie Apache Parquet auf einem Cloud-Objektspeicher, darüber eine transaktionale Metadatenschicht wie Delta Lake oder Apache Iceberg (Armbrust et al., 2021). Business Intelligence, Data Science und Machine Learning arbeiten dann auf denselben Tabellen. [[databricks|Databricks]], dessen Forschende die Architektur beschrieben, baut seine Plattform auf diesem Entwurf auf (Armbrust et al., 2021).

### Funktionsweise

```text
Quellen (operative Datenbanken, Events, Dateien, Dokumente)
 ▼
Cloud-Objektspeicher (S3, ADLS, GCS) mit Dateien in offenem Format (Parquet)
 ▼
Metadatenschicht (Delta Lake, Iceberg, Hudi): Transaktionslog, Schema, Versionen, Statistiken
 ▼
Medallion-Schichten: Bronze (roh) → Silber (validiert) → Gold (fachliche Aggregate)
 ▼
Engines: SQL für BI · DataFrame-APIs für Data Science und ML · Governance über einen Katalog
```

#### 1. Vom Warehouse über den Lake zum Lakehouse

Analyseplattformen der ersten Generation luden Daten aus operativen Datenbanken mit Schema-on-Write in ein zentrales Warehouse, optimiert für Business Intelligence (Armbrust et al., 2021). Als die Daten wuchsen und unstrukturiert wurden (Video, Audio, Text), wanderten Rohdaten in Data Lakes: günstige Speicher mit Datei-API und offenen Formaten wie Parquet und ORC, zuerst auf HDFS von Hadoop und ab 2015 auf Cloud-Objektspeichern. Der Lake arbeitete mit Schema-on-Read und schob Qualität und Governance nach hinten, und ein Teil seiner Daten wurde erneut in ein Warehouse kopiert; diese zweistufige Architektur setzte sich durch (Armbrust et al., 2021). Armbrust et al. (2021) nennen vier Probleme: Lake und Warehouse konsistent zu halten ist unzuverlässig, Warehouse-Daten sind veraltet, ML-Systeme wie TensorFlow, PyTorch und XGBoost können Warehouse-Formate nicht effizient lesen, und doppelte Speicherung sowie proprietäre Formate erhöhen Kosten und Abhängigkeit.

#### 2. Die transaktionale Metadatenschicht

Objektspeicher bieten nur eine Key-Value-Schnittstelle, in der selbst das Aktualisieren einer Tabelle über mehrere Dateien nicht atomar ist (Armbrust et al., 2020). Das Lakehouse ergänzt eine Metadatenschicht, die festhält, welche Dateien zu welcher Tabellenversion gehören. Delta Lake speichert dieses Transaktionslog im Objektspeicher selbst, verdichtet zu Parquet, und bietet damit ACID-Transaktionen, Time Travel zu früheren Versionen, schnelle Metadatenoperationen über Milliarden von Objekten, Upserts und Audit-Logs; Apache Iceberg, entstanden bei Netflix, nutzt einen ähnlichen Entwurf, und Apache Hudi, entstanden bei Uber, konzentriert sich auf das Einspielen von Streams (Armbrust et al., 2020; Armbrust et al., 2021). Ein bestehendes Verzeichnis von Parquet-Dateien lässt sich ohne Kopieren in eine Delta-Tabelle umwandeln, indem ein Logeintrag geschrieben wird, der auf die Dateien verweist (Armbrust et al., 2021). Dieselbe Schicht erzwingt Schemata und Constraints, weist verletzende Datensätze zurück oder stellt sie unter Quarantäne und eignet sich für Zugriffskontrolle und Audit-Logging (Armbrust et al., 2021).

#### 3. SQL-Performance auf offenen Formaten

Weil das Dateiformat Teil der öffentlichen Schnittstelle ist, kann ein Lakehouse den Speicher nicht frei optimieren wie ein geschlossenes Warehouse. Armbrust et al. (2021) schlagen drei formatunabhängige Techniken vor: Caching häufig genutzter Dateien auf SSD oder im RAM der Rechenknoten, was das Transaktionslog sicher macht; Hilfsdaten wie Min-Max-Statistiken je Datei für Data Skipping und Bloom-Filter-Indizes; und optimiertes Datenlayout, etwa das Ordnen von Datensätzen nach Z-Order- oder Hilbert-Kurven, damit zusammengehörige Datensätze gemeinsam gelesen werden. Damit lief die Delta Engine im Test der Autoren den TPC-DS-Benchmark mit Skalierungsfaktor 30.000 schneller und günstiger als vier verbreitete Cloud Data Warehouses (Armbrust et al., 2021).

#### 4. Machine Learning auf denselben Daten

ML-Bibliotheken können offene Formate wie Parquet direkt lesen, und deklarative DataFrame-APIs erlauben der Engine, ML-Datenzugriffe ebenso zu optimieren wie SQL-Abfragen (Armbrust et al., 2021). ML-Workloads erhalten so Transaktionen, Versionierung und Governance, ohne Daten aus einem Warehouse zu exportieren; das Transaktionslog erlaubt zudem, ein Training auf einer früheren Version einer Tabelle zu reproduzieren (Armbrust et al., 2020). Rechenleistung ist vom Speicher getrennt, sodass ein GPU-Cluster für das Training und ein SQL-Cluster für Berichte dieselben Tabellen lesen können (Armbrust et al., 2021). Verteilte Verarbeitung auf diesen Tabellen erfolgt meist mit [[apache-spark|Apache Spark]].

#### 5. Medallion-Architektur

Databricks empfiehlt, Lakehouse-Tabellen in Schichten zu ordnen, die „incrementally and progressively improve the structure and quality of data“ (Databricks Medallion):
- **Bronze:** Rohdaten in ursprünglicher Form, mit Metadaten zur Herkunft, aber fast ohne Bereinigung, damit unerwartete Schemaänderungen die Aufnahme nicht brechen.
- **Silber:** validierte, bereinigte und angereicherte Daten: Schemadurchsetzung, Umgang mit Nullwerten und verspätet eintreffenden Daten, Deduplizierung, Qualitätsprüfungen und Joins, mit mindestens einer validierten, nicht aggregierten Fassung jedes Datensatzes.
- **Gold:** aufbereitete Sichten für Analysen, [[data-visualisation|Dashboards]], ML und Anwendungen, typischerweise dimensionale Modelle und Aggregate, optimiert für Abfrageleistung.

Das Muster ist eine Empfehlung, keine Pflicht (Databricks Medallion). Die Modellierung der Gold-Schicht behandelt [[data-modelling|Datenmodellierung]], die Pipelines zwischen den Schichten [[data-pipelines|Datenpipelines]].

#### Herkunft und Varianten

Michael Armbrust, Ali Ghodsi, Reynold Xin und [[matei-zaharia|Matei Zaharia]] von Databricks legten die Lakehouse-Architektur auf der CIDR 2021 dar; Databricks hatte 2016 mit der Entwicklung von Delta Lake begonnen und es auf der VLDB 2020 beschrieben (Armbrust et al., 2021; Armbrust et al., 2020). Governance über das Lakehouse liefert ein Katalog wie Unity Catalog, der auch als Open Source verfügbar ist (Databricks Unity Catalog); siehe [[data-governance|Data Governance]].

### Wann einsetzen

- Eine Organisation betreibt BI, Data Science und ML auf denselben Daten und will sie nicht zwischen Lake und Warehouse kopieren (Armbrust et al., 2021).
- Große oder unstrukturierte Datenbestände (Dokumente, Bilder, Sensordaten) sollen günstig gespeichert und dennoch mit Transaktionen und Versionierung abgefragt werden (Armbrust et al., 2021).
- Trainingsdaten müssen aus früheren Tabellenversionen reproduzierbar sein (Armbrust et al., 2020).

### Stärken und Grenzen

**Stärken**
- Eine einzige Kopie der Daten in offenem Format, lesbar für viele Engines, verringert Abhängigkeit und Speicherkosten (Armbrust et al., 2021).
- ACID-Transaktionen, Time Travel und Schemadurchsetzung auf günstigem Objektspeicher (Armbrust et al., 2020).
- Weniger ETL-Schritte und aktuellere Daten als in der zweistufigen Architektur (Armbrust et al., 2021).

**Grenzen**
- Transaktionen in Delta Lake, Iceberg und Hudi umfassen jeweils nur eine Tabelle, und das Log im Objektspeicher begrenzt die Transaktionsrate (Armbrust et al., 2021).
- Ein offengelegtes Speicherformat gibt einen Teil der Datenunabhängigkeit klassischer Datenbanksysteme auf und erschwert manche Optimierungen (Armbrust et al., 2021).
- ETL-Logik zum Aufbau aufbereiteter Tabellen bleibt nötig (Armbrust et al., 2021).

### Vergleich

| | Data Warehouse | Data Lake | Lakehouse |
|---|---|---|---|
| Speicher | proprietäres Format, an die Engine gebunden | offene Dateien auf günstigem Speicher | offene Dateien auf günstigem Speicher |
| Schema | beim Schreiben | beim Lesen | durch die Metadatenschicht erzwungen |
| Transaktionen, Versionierung | ja | nein | ja |
| Unstrukturierte Daten | kaum | ja | ja |
| Direkter ML-Zugriff | über Export | ja | ja |

Quelle: Armbrust et al. (2021). Verwaltete KI-Dienste der großen Clouds vergleicht [[cloud-ai-platforms|Cloud-KI-Plattformen]]; das Batch-Verarbeitungsmodell hinter frühen Data Lakes beschreibt [[mapreduce|MapReduce]].

### In der Praxis

Auf Databricks werden Tabellen in Unity Catalog mit dem dreistufigen Namensraum `catalog.schema.table` verwaltet, und Modelle sowie Modelldienste werden im selben Katalog verwaltet (Databricks Unity Catalog). Die Häufigkeit der Datenaufnahme ist ein Kostenhebel: Kontinuierliche Aufnahme hat die geringste Latenz und die höchsten Kosten, Batch-Aufnahme umgekehrt (Databricks Medallion). Bronze-Tabellen speichern die meisten Felder als Zeichenketten oder halbstrukturierte Typen, um Änderungen an den Quellen zu überstehen (Databricks Medallion).

### Merksatz

Ein Lakehouse hält alle Daten nur einmal, in offenen Dateien auf günstigem Objektspeicher, und ergänzt eine transaktionale Metadatenschicht, die Zuverlässigkeit und Leistung wie in einem Warehouse bietet, sodass BI, Data Science und ML dieselben Tabellen nutzen können.

### Quellen

- Armbrust, M., Ghodsi, A., Xin, R. & Zaharia, M. (2021). *Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics.* CIDR 2021. [cidrdb.org](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf)
- Armbrust, M., Das, T., Sun, L. et al. (2020). *Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores.* PVLDB 13(12), 3411–3424. [vldb.org](https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf)
- Databricks Medallion. *What is the medallion lakehouse architecture?* [docs.databricks.com](https://docs.databricks.com/aws/en/lakehouse/medallion)
- Databricks Unity Catalog. *What is Unity Catalog?* [docs.databricks.com](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)
