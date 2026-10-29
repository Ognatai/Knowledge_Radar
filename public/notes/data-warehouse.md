---
title_en: Data Warehouse
title_de: Data Warehouse
entity_type: Concept
aliases:
- Data warehousing
- Enterprise data warehouse
- EDW
- DWH
- OLAP
- Column store
- Cloud data warehouse
sources:
- https://sigmodrecord.org/publications/sigmodRecord/9703/pdfs/248603.248616.pdf
- https://www.vldb.org/archives/website/2005/program/paper/thu/p553-stonebraker.pdf
- https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf
- https://info.snowflake.net/rs/252-RFO-227/images/Snowflake_SIGMOD.pdf
- https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/enterprise-data-warehouse-bus-architecture/
- https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/conformed-dimension/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR
A data warehouse is a "subject-oriented, integrated, time-varying, non-volatile collection of data that is used primarily in organizational decision making", kept separately from the operational databases that run day-to-day business (Chaudhuri & Dayal, 1997). Data from many sources is extracted, cleaned, integrated and loaded into it, modelled multidimensionally as facts and dimensions, and queried with analytical (OLAP) queries that scan, join and aggregate millions of records. Modern warehouses store data by column and, in the cloud, separate storage from compute, so that analytical queries over very large tables return in seconds (Stonebraker et al., 2005; Melnik et al., 2010; Dageville et al., 2016).

### How it works

A warehouse sits between the systems where data is created and the people and tools that analyse it. Back-end processes fill it, a warehouse server stores and serves it, and front-end tools query it (Chaudhuri & Dayal, 1997).

```text
operational databases ─┐
external sources ──────┼─▶ extract ─▶ clean ─▶ transform ─▶ load / refresh
                       │                                          │
                       │                                          ▼
                       │                       data warehouse ──▶ data marts
                       │                         (facts + dimensions, summary tables)
                       │                                          │
                       │                        warehouse / OLAP servers
                       │                                          │
                       │             query and reporting · OLAP analysis · data mining
                       └──────────── metadata repository · monitoring and administration
```

#### 1. Why a separate system
Operational databases serve online transaction processing (OLTP): short, structured, repetitive transactions such as order entry, which read or update a few records by primary key and need current, detailed data; transaction throughput is the key measure. Decision support needs historical, summarised and consolidated data from many sources, often orders of magnitude larger, and runs ad hoc queries that scan, join and aggregate millions of records; query throughput and response time matter most (Chaudhuri & Dayal, 1997). Running such queries on the tuned operational databases would perform unacceptably, the operational systems lack the history needed for trends, and data from heterogeneous sources has to be reconciled first. For these reasons the warehouse is implemented separately (Chaudhuri & Dayal, 1997).

#### 2. Loading and refreshing
Back-end tools extract the data, clean it and load it; the steps are the extract–transform–load process described in [[data-pipelines|data pipelines]]. Cleaning matters because errors are likely with large volumes from many sources: inconsistent field lengths, descriptions and codes, missing entries and violated integrity constraints. Loading also checks constraints, sorts, builds summary tables and indexes and partitions the data (Chaudhuri & Dayal, 1997). Design choices:

- **Full or incremental load:** a full load can run as one long batch transaction while the old database still answers queries, but may take too long; incremental loading inserts only changed tuples, at the cost of harder management (Chaudhuri & Dayal, 1997).
- **Refresh:** usually periodic, daily or weekly; only queries that need current data justify propagating every update. Replication can refresh incrementally by data shipping (triggers write changes to a snapshot log) or transaction shipping (the source's transaction log is read) (Chaudhuri & Dayal, 1997).
- **Derived data:** summary tables and indexes have to be updated with the base data; incrementally maintaining such materialized views is a long-standing research problem (Chaudhuri & Dayal, 1997).

#### 3. The multidimensional model and OLAP
Data in a warehouse is modelled as numeric measures, such as sales or revenue, each determined by a set of dimensions such as product, city and date; dimension attributes often form hierarchies such as day–month–quarter–year (Chaudhuri & Dayal, 1997). Typical OLAP operations are:

- **Roll-up:** aggregate further, for example from cities to states.
- **Drill-down:** the reverse, towards more detail.
- **Slice and dice:** select and project, reducing the dimensions viewed.
- **Pivot:** re-orient the view, for example cities as rows and years as columns.

In a relational warehouse the model is stored as a star schema, one fact table with foreign keys to one table per dimension, or as a snowflake schema with normalised dimension tables; several fact tables sharing dimensions form a fact constellation (Chaudhuri & Dayal, 1997). How to design these tables is covered in [[data-modelling|data modelling]]. Relational OLAP (ROLAP) servers map the model onto SQL over such tables, while multidimensional OLAP (MOLAP) servers store it directly in array structures, which index well but use storage poorly for sparse data (Chaudhuri & Dayal, 1997).

#### 4. Enterprise warehouse, data marts and the bus architecture
An enterprise warehouse covers all subjects of an organisation but takes long to build and needs extensive business modelling; data marts are departmental subsets on selected subjects that roll out faster but may lead to complex integration problems later (Chaudhuri & Dayal, 1997). Kimball's enterprise data warehouse bus architecture builds the enterprise system incrementally, broken down by business process, and delivers integration through conformed dimensions that are reused across processes (Kimball Group, bus architecture). Dimension tables conform when they share column names and domain contents; facts from separate fact tables can then be combined on the same rows in one "drill-across" report, which Kimball calls the essence of integration (Kimball Group, conformed dimensions).

#### 5. Query processing
Warehouse servers speed up analytical queries with structures that operational systems rarely need (Chaudhuri & Dayal, 1997):

- **Bitmap indexes** represent the rows with a given value as a bit vector, so that conditions on several columns are combined by AND and OR of bit vectors; they suit low-cardinality columns and, compressed, higher ones.
- **Join indexes** precompute joins between a dimension attribute and the matching rows of the fact table.
- **Materialized views** store pre-aggregated results; a view with total sales by quarter and product can answer a query for yearly sales of one product by selection and roll-up, as long as the aggregate, such as a sum, can be rolled up.
- **SQL extensions** such as `ROLLUP` and `CUBE` compute several groupings in one statement; `CUBE` over `k` columns produces all `2^k` groupings.
- **Parallelism:** partitioning data and processing queries in parallel across nodes.

#### 6. Column stores
Row stores place all fields of a record together, so one write stores a whole record; they are write-optimised and suit OLTP. A warehouse, loaded in bulk and then queried for long periods, should be read-optimised: a column store keeps the values of each column together, reads only the columns a query needs, and can code and densely pack the values of a column, trading abundant CPU cycles for scarce disk bandwidth (Stonebraker et al., 2005). C-Store stores overlapping groups of columns sorted on different attributes ("projections") and combines a small writeable store for inserts with a large read-optimised store, connected by a tuple mover that moves records in batches. In preliminary tests on seven TPC-H queries, it was on average 164 times faster than a commercial row store and 21 times faster than a commercial column store when space was constrained (Stonebraker et al., 2005).

#### 7. Cloud data warehouses
Dremel at Google combined a columnar layout for nested records with multi-level execution trees and ran aggregation queries over trillion-row tables in seconds, on thousands of CPUs and petabytes of data, reading data in place from a distributed file system; it complements rather than replaces [[mapreduce|MapReduce]] (Melnik et al., 2010). Snowflake, a data warehouse built for the cloud, separates storage and compute: tables are stored as immutable files in Amazon S3, each holding the values of each column together and compressed, while queries run on "virtual warehouses", clusters of compute nodes that can be created, resized or shut down at any time without affecting the data. Several virtual warehouses can work on the same tables without copying them, which gives departments isolated compute on shared data. Instead of indexes, Snowflake keeps the minimum and maximum of each column per file and skips files that cannot match a query predicate (min-max pruning) (Dageville et al., 2016).

#### Origin and variants
Chaudhuri & Dayal (1997) surveyed warehousing and OLAP technology as it had grown in industry in the mid-1990s, from back-end tools to ROLAP and MOLAP servers. Column stores such as C-Store made the read-optimised design explicit (Stonebraker et al., 2005). Dremel and Snowflake moved interactive analysis into large shared clusters and the cloud, with columnar files and, in Snowflake, a strict separation of storage and compute (Melnik et al., 2010; Dageville et al., 2016). The [[data-lakehouse|data lakehouse]] adds warehouse features on top of open file formats in a data lake.

### When to use it
- Reporting, business intelligence and ad hoc analysis over historical data integrated from several source systems (Chaudhuri & Dayal, 1997).
- When analytical queries would slow down or not run on the operational databases (Chaudhuri & Dayal, 1997).
- When several departments need consistent figures: conformed dimensions let reports combine facts from different business processes (Kimball Group, conformed dimensions).
- In the cloud, when workloads vary and compute should scale independently of the data volume (Dageville et al., 2016).

### Strengths and limitations
Strengths:
- One integrated, cleaned and historised view of the organisation's data, separate from the systems that run the business (Chaudhuri & Dayal, 1997).
- Fast aggregation over large tables through column storage, compression, pruning and parallelism (Stonebraker et al., 2005; Dageville et al., 2016).
- Elastic, isolated compute on shared data in cloud warehouses (Dageville et al., 2016).

Limitations:
- Data is only as current as the last refresh, typically daily or weekly (Chaudhuri & Dayal, 1997).
- An enterprise warehouse takes long to build and needs agreement across the organisation; independent data marts are faster but can create integration problems (Chaudhuri & Dayal, 1997).
- Traditional warehouses depend on deep ETL pipelines and physical tuning that assume predictable, slow-moving data, and struggle with semi-structured data from external sources (Dageville et al., 2016).
- Column stores are read-optimised; frequent small updates need extra mechanisms such as C-Store's writeable store (Stonebraker et al., 2005).

### Comparison
| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Operational database ([[sql\|SQL]], row store) | Current, detailed data; short transactions on few records | Running the business (OLTP) |
| Data warehouse | Integrated, historical data; scans and aggregates over many records | Reporting and analysis (OLAP) |
| [[data-lakehouse\|Data lakehouse]] | Warehouse features (transactions, SQL performance) on open files in a data lake, also for machine learning | Mixed BI and ML workloads on one copy of the data |
| [[apache-spark\|Apache Spark]] / [[mapreduce\|MapReduce]] | General-purpose distributed processing rather than an integrated, modelled store | Large transformations and custom computation |

### In practice
- Clean data before it reaches the warehouse: because the warehouse is used for decisions, its data has to be correct, and optional fields in data entry forms are a significant source of inconsistent data (Chaudhuri & Dayal, 1997).
- Choose materialized views and indexes from the actual query workload, the cost of keeping them up to date and the storage budget (Chaudhuri & Dayal, 1997).
- Define conformed dimensions once, together with the business's [[data-governance|data governance]] representatives, and reuse them across fact tables (Kimball Group, conformed dimensions).
- In elastic cloud warehouses, compute is a separate cost: Snowflake encourages shutting down all virtual warehouses when no queries run (Dageville et al., 2016).

### Regulatory context
[[bcbs-239-and-ecb-rdarr-guide|BCBS 239]] requires banks to maintain data architecture and IT infrastructure that fully support risk data aggregation and reporting, in normal times and in crises, and the [[ecb|ECB]] guide asks for a documented, integrated data architecture with a dictionary of business definitions and a metadata repository. A warehouse with integrated sources and a metadata repository, as in the classic architecture, is one way to provide this (Chaudhuri & Dayal, 1997).

### Key takeaway
A data warehouse copies data out of the operational systems into a separate, integrated and historised store that is organised and physically optimised for analytical queries rather than for transactions.

### Sources
- Chaudhuri, S. & Dayal, U. (1997). *An Overview of Data Warehousing and OLAP Technology.* ACM SIGMOD Record 26(1). [sigmodrecord.org](https://sigmodrecord.org/publications/sigmodRecord/9703/pdfs/248603.248616.pdf)
- Stonebraker, M. et al. (2005). *C-Store: A Column-oriented DBMS.* VLDB 2005. [vldb.org](https://www.vldb.org/archives/website/2005/program/paper/thu/p553-stonebraker.pdf)
- Melnik, S. et al. (2010). *Dremel: Interactive Analysis of Web-Scale Datasets.* PVLDB 3(1). [research.google.com](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf)
- Dageville, B. et al. (2016). *The Snowflake Elastic Data Warehouse.* SIGMOD 2016. [snowflake.net](https://info.snowflake.net/rs/252-RFO-227/images/Snowflake_SIGMOD.pdf)
- Kimball Group (n.d.). *Enterprise Data Warehouse Bus Architecture.* Kimball Dimensional Modeling Techniques. [kimballgroup.com](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/enterprise-data-warehouse-bus-architecture/)
- Kimball Group (n.d.). *Conformed Dimensions.* Kimball Dimensional Modeling Techniques. [kimballgroup.com](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/conformed-dimension/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Basis der angegebenen Quellen; sie kann unvollständig, veraltet oder fehlerhaft sein.

### TL;DR
Ein Data Warehouse ist eine „subject-oriented, integrated, time-varying, non-volatile collection of data that is used primarily in organizational decision making“, getrennt von den operativen Datenbanken, die das Tagesgeschäft abwickeln (Chaudhuri & Dayal, 1997). Daten aus vielen Quellen werden extrahiert, bereinigt, integriert und geladen, multidimensional als Fakten und Dimensionen modelliert und mit analytischen Abfragen (OLAP) ausgewertet, die Millionen von Datensätzen durchsuchen, verknüpfen und aggregieren. Moderne Warehouses speichern Daten spaltenweise und trennen in der Cloud Speicher und Rechenleistung, sodass analytische Abfragen über sehr große Tabellen in Sekunden antworten (Stonebraker et al., 2005; Melnik et al., 2010; Dageville et al., 2016).

### Funktionsweise

Ein Warehouse liegt zwischen den Systemen, in denen Daten entstehen, und den Menschen und Werkzeugen, die sie auswerten. Back-End-Prozesse befüllen es, ein Warehouse-Server speichert die Daten und stellt sie bereit, und Front-End-Werkzeuge fragen sie ab (Chaudhuri & Dayal, 1997).

```text
operative Datenbanken ─┐
externe Quellen ───────┼─▶ Extrahieren ─▶ Bereinigen ─▶ Transformieren ─▶ Laden / Aktualisieren
                       │                                                       │
                       │                                                       ▼
                       │                              Data Warehouse ──▶ Data Marts
                       │                         (Fakten + Dimensionen, Summentabellen)
                       │                                                       │
                       │                                   Warehouse- / OLAP-Server
                       │                                                       │
                       │                 Abfragen und Berichte · OLAP-Analyse · Data Mining
                       └──────────────── Metadaten-Repository · Überwachung und Administration
```

#### 1. Warum ein eigenes System
Operative Datenbanken dienen der Transaktionsverarbeitung (OLTP): kurzen, strukturierten, wiederkehrenden Transaktionen wie der Auftragserfassung, die wenige Datensätze über den Primärschlüssel lesen oder ändern und aktuelle, detaillierte Daten brauchen; entscheidend ist der Transaktionsdurchsatz. Entscheidungsunterstützung braucht historische, zusammengefasste und konsolidierte Daten aus vielen Quellen, oft um Größenordnungen umfangreicher, und stellt Ad-hoc-Abfragen, die Millionen von Datensätzen durchsuchen, verknüpfen und aggregieren; entscheidend sind Abfragedurchsatz und Antwortzeit (Chaudhuri & Dayal, 1997). Solche Abfragen auf den optimierten operativen Datenbanken auszuführen, wäre unzumutbar langsam, den operativen Systemen fehlt die Historie für Trends, und Daten aus heterogenen Quellen müssen erst abgeglichen werden. Aus diesen Gründen wird das Warehouse getrennt betrieben (Chaudhuri & Dayal, 1997).

#### 2. Laden und Aktualisieren
Back-End-Werkzeuge extrahieren die Daten, bereinigen und laden sie; die Schritte entsprechen dem Extract-Transform-Load-Prozess, den [[data-pipelines|Datenpipelines]] beschreibt. Die Bereinigung ist wichtig, weil bei großen Mengen aus vielen Quellen Fehler wahrscheinlich sind: uneinheitliche Feldlängen, Beschreibungen und Codes, fehlende Einträge und verletzte Integritätsbedingungen. Beim Laden werden außerdem Bedingungen geprüft, Daten sortiert, Summentabellen und Indizes aufgebaut und die Daten partitioniert (Chaudhuri & Dayal, 1997). Entwurfsentscheidungen:

- **Voll- oder inkrementelles Laden:** Ein Volllauf kann als eine lange Batch-Transaktion laufen, während die alte Datenbank weiter Abfragen beantwortet, dauert aber womöglich zu lange; inkrementelles Laden fügt nur geänderte Tupel ein, ist aber schwerer zu steuern (Chaudhuri & Dayal, 1997).
- **Aktualisierung:** meist periodisch, täglich oder wöchentlich; nur Abfragen, die aktuelle Daten brauchen, rechtfertigen es, jede Änderung weiterzugeben. Replikation kann inkrementell aktualisieren, per Data Shipping (Trigger schreiben Änderungen in ein Snapshot-Log) oder per Transaction Shipping (das Transaktionslog der Quelle wird ausgelesen) (Chaudhuri & Dayal, 1997).
- **Abgeleitete Daten:** Summentabellen und Indizes müssen mit den Basisdaten aktualisiert werden; die inkrementelle Pflege solcher materialisierten Sichten ist ein altes Forschungsproblem (Chaudhuri & Dayal, 1997).

#### 3. Das multidimensionale Modell und OLAP
Daten in einem Warehouse werden als numerische Kennzahlen modelliert, etwa Umsatz oder Erlös, die jeweils durch Dimensionen wie Produkt, Stadt und Datum bestimmt sind; Dimensionsattribute bilden oft Hierarchien wie Tag–Monat–Quartal–Jahr (Chaudhuri & Dayal, 1997). Typische OLAP-Operationen sind:

- **Roll-up:** weiter aggregieren, etwa von Städten zu Bundesstaaten.
- **Drill-down:** das Gegenteil, hin zu mehr Detail.
- **Slice and Dice:** auswählen und projizieren, sodass weniger Dimensionen betrachtet werden.
- **Pivot:** die Sicht drehen, etwa Städte als Zeilen und Jahre als Spalten.

In einem relationalen Warehouse wird das Modell als Sternschema gespeichert, eine Faktentabelle mit Fremdschlüsseln auf je eine Tabelle pro Dimension, oder als Schneeflockenschema mit normalisierten Dimensionstabellen; mehrere Faktentabellen mit gemeinsamen Dimensionen bilden eine Faktenkonstellation (Chaudhuri & Dayal, 1997). Wie man diese Tabellen entwirft, behandelt [[data-modelling|Datenmodellierung]]. Relationale OLAP-Server (ROLAP) bilden das Modell auf SQL über solchen Tabellen ab, multidimensionale OLAP-Server (MOLAP) speichern es direkt in Array-Strukturen, die sich gut indizieren lassen, bei dünn besetzten Daten aber viel Speicher verschwenden (Chaudhuri & Dayal, 1997).

#### 4. Unternehmens-Warehouse, Data Marts und die Bus-Architektur
Ein unternehmensweites Warehouse deckt alle Themen einer Organisation ab, braucht aber lange und eine umfangreiche Geschäftsmodellierung; Data Marts sind abteilungsbezogene Teilmengen zu ausgewählten Themen, die schneller eingeführt sind, später aber zu schwierigen Integrationsproblemen führen können (Chaudhuri & Dayal, 1997). Kimballs Enterprise Data Warehouse Bus Architecture baut das unternehmensweite System schrittweise auf, gegliedert nach Geschäftsprozessen, und erreicht die Integration über Conformed Dimensions, die prozessübergreifend wiederverwendet werden (Kimball Group, Bus-Architektur). Dimensionstabellen sind konform, wenn sie dieselben Spaltennamen und Inhalte haben; Fakten aus getrennten Faktentabellen lassen sich dann in einem „Drill-across“-Bericht in denselben Zeilen zusammenführen, was Kimball als Kern der Integration bezeichnet (Kimball Group, Conformed Dimensions).

#### 5. Abfrageverarbeitung
Warehouse-Server beschleunigen analytische Abfragen mit Strukturen, die operative Systeme selten brauchen (Chaudhuri & Dayal, 1997):

- **Bitmap-Indizes** stellen die Zeilen mit einem bestimmten Wert als Bitvektor dar, sodass Bedingungen auf mehreren Spalten durch UND und ODER von Bitvektoren verknüpft werden; sie eignen sich für Spalten mit wenigen Werten und, komprimiert, auch für mehr.
- **Join-Indizes** berechnen Verknüpfungen zwischen einem Dimensionsattribut und den passenden Zeilen der Faktentabelle im Voraus.
- **Materialisierte Sichten** speichern voraggregierte Ergebnisse; eine Sicht mit Umsatz je Quartal und Produkt kann eine Abfrage nach dem Jahresumsatz eines Produkts durch Auswahl und Roll-up beantworten, sofern sich die Aggregatfunktion, etwa eine Summe, weiter aggregieren lässt.
- **SQL-Erweiterungen** wie `ROLLUP` und `CUBE` berechnen mehrere Gruppierungen in einer Anweisung; `CUBE` über `k` Spalten erzeugt alle `2^k` Gruppierungen.
- **Parallelität:** Daten partitionieren und Abfragen parallel auf mehreren Knoten verarbeiten.

#### 6. Spaltenorientierte Speicherung
Zeilenorientierte Systeme legen alle Felder eines Datensatzes zusammen ab, sodass ein Schreibvorgang einen ganzen Datensatz speichert; sie sind schreiboptimiert und passen zu OLTP. Ein Warehouse, das in großen Mengen geladen und danach lange abgefragt wird, sollte leseoptimiert sein: Ein Column Store hält die Werte jeder Spalte zusammen, liest nur die Spalten, die eine Abfrage braucht, und kann die Werte einer Spalte kodieren und dicht packen, also reichlich vorhandene CPU-Zyklen gegen knappe Festplattenbandbreite tauschen (Stonebraker et al., 2005). C-Store speichert überlappende Gruppen von Spalten, sortiert nach verschiedenen Attributen („Projektionen“), und kombiniert einen kleinen beschreibbaren Speicher für Einfügungen mit einem großen leseoptimierten Speicher, verbunden durch einen Tuple Mover, der Datensätze stapelweise verschiebt. In vorläufigen Tests mit sieben TPC-H-Abfragen war es bei begrenztem Speicherplatz im Mittel 164-mal schneller als ein kommerzielles zeilenorientiertes und 21-mal schneller als ein kommerzielles spaltenorientiertes System (Stonebraker et al., 2005).

#### 7. Cloud Data Warehouses
Dremel bei Google kombinierte ein spaltenorientiertes Format für verschachtelte Datensätze mit mehrstufigen Ausführungsbäumen und führte Aggregationsabfragen über Tabellen mit Billionen Zeilen in Sekunden aus, auf Tausenden CPUs und Petabytes an Daten, wobei es die Daten direkt aus einem verteilten Dateisystem las; es ergänzt [[mapreduce|MapReduce]], statt es zu ersetzen (Melnik et al., 2010). Snowflake, ein für die Cloud gebautes Data Warehouse, trennt Speicher und Rechenleistung: Tabellen liegen als unveränderliche Dateien in Amazon S3, in denen die Werte jeder Spalte zusammen und komprimiert gespeichert sind, während Abfragen auf „virtuellen Warehouses“ laufen, Clustern von Rechenknoten, die jederzeit erzeugt, in der Größe geändert oder abgeschaltet werden können, ohne die Daten zu berühren. Mehrere virtuelle Warehouses können auf denselben Tabellen arbeiten, ohne sie zu kopieren; Abteilungen erhalten so getrennte Rechenleistung auf gemeinsamen Daten. Statt Indizes speichert Snowflake für jede Datei Minimum und Maximum jeder Spalte und überspringt Dateien, die ein Abfrageprädikat nicht erfüllen können (Min-Max-Pruning) (Dageville et al., 2016).

#### Ursprung und Varianten
Chaudhuri & Dayal (1997) gaben einen Überblick über Warehousing- und OLAP-Technik, wie sie Mitte der 1990er-Jahre in der Industrie entstanden war, von Back-End-Werkzeugen bis zu ROLAP- und MOLAP-Servern. Column Stores wie C-Store machten den leseoptimierten Entwurf ausdrücklich (Stonebraker et al., 2005). Dremel und Snowflake brachten interaktive Analyse in große gemeinsam genutzte Cluster und in die Cloud, mit spaltenorientierten Dateien und bei Snowflake mit einer strikten Trennung von Speicher und Rechenleistung (Melnik et al., 2010; Dageville et al., 2016). Das [[data-lakehouse|Data Lakehouse]] ergänzt Warehouse-Funktionen auf offenen Dateiformaten in einem Data Lake.

### Wann einsetzen
- Berichtswesen, Business Intelligence und Ad-hoc-Analysen über historische Daten, die aus mehreren Quellsystemen integriert sind (Chaudhuri & Dayal, 1997).
- Wenn analytische Abfragen die operativen Datenbanken ausbremsen oder dort nicht laufen würden (Chaudhuri & Dayal, 1997).
- Wenn mehrere Abteilungen einheitliche Zahlen brauchen: Conformed Dimensions erlauben Berichte, die Fakten aus verschiedenen Geschäftsprozessen zusammenführen (Kimball Group, Conformed Dimensions).
- In der Cloud, wenn die Last schwankt und die Rechenleistung unabhängig von der Datenmenge skalieren soll (Dageville et al., 2016).

### Stärken und Grenzen
Stärken:
- Eine integrierte, bereinigte und historisierte Sicht auf die Daten der Organisation, getrennt von den Systemen, die das Geschäft abwickeln (Chaudhuri & Dayal, 1997).
- Schnelle Aggregation über große Tabellen durch spaltenorientierte Speicherung, Kompression, Pruning und Parallelität (Stonebraker et al., 2005; Dageville et al., 2016).
- Elastische, voneinander getrennte Rechenleistung auf gemeinsamen Daten in Cloud-Warehouses (Dageville et al., 2016).

Grenzen:
- Die Daten sind nur so aktuell wie die letzte Aktualisierung, typischerweise täglich oder wöchentlich (Chaudhuri & Dayal, 1997).
- Ein unternehmensweites Warehouse braucht lange und Einigkeit über die ganze Organisation; unabhängige Data Marts sind schneller, können aber Integrationsprobleme schaffen (Chaudhuri & Dayal, 1997).
- Klassische Warehouses hängen von tiefen ETL-Pipelines und physischem Tuning ab, die vorhersehbare, sich langsam ändernde Daten voraussetzen, und tun sich mit halbstrukturierten Daten aus externen Quellen schwer (Dageville et al., 2016).
- Column Stores sind leseoptimiert; häufige kleine Änderungen brauchen zusätzliche Mechanismen wie den beschreibbaren Speicher von C-Store (Stonebraker et al., 2005).

### Vergleich
| Ansatz | Unterschied | Geeignet für |
|--------|-------------|--------------|
| Operative Datenbank ([[sql\|SQL]], zeilenorientiert) | Aktuelle, detaillierte Daten; kurze Transaktionen auf wenigen Datensätzen | Das Geschäft abwickeln (OLTP) |
| Data Warehouse | Integrierte, historische Daten; Durchsuchen und Aggregieren vieler Datensätze | Berichte und Analyse (OLAP) |
| [[data-lakehouse\|Data Lakehouse]] | Warehouse-Funktionen (Transaktionen, SQL-Performance) auf offenen Dateien in einem Data Lake, auch für Machine Learning | Gemischte BI- und ML-Last auf einer Kopie der Daten |
| [[apache-spark\|Apache Spark]] / [[mapreduce\|MapReduce]] | Allgemeine verteilte Verarbeitung statt eines integrierten, modellierten Datenbestands | Große Transformationen und eigene Berechnungen |

### In der Praxis
- Daten bereinigen, bevor sie ins Warehouse gelangen: Weil das Warehouse für Entscheidungen genutzt wird, müssen seine Daten stimmen, und optionale Felder in Eingabeformularen sind eine wesentliche Quelle inkonsistenter Daten (Chaudhuri & Dayal, 1997).
- Materialisierte Sichten und Indizes anhand der tatsächlichen Abfragelast, der Kosten für ihre Aktualisierung und des Speicherbudgets auswählen (Chaudhuri & Dayal, 1997).
- Conformed Dimensions einmal gemeinsam mit den Verantwortlichen für [[data-governance|Data Governance]] festlegen und über Faktentabellen hinweg wiederverwenden (Kimball Group, Conformed Dimensions).
- In elastischen Cloud-Warehouses ist Rechenleistung ein eigener Kostenpunkt: Snowflake empfiehlt, alle virtuellen Warehouses abzuschalten, wenn keine Abfragen laufen (Dageville et al., 2016).

### Regulatorischer Kontext
[[bcbs-239-and-ecb-rdarr-guide|BCBS 239]] verlangt von Banken eine Datenarchitektur und IT-Infrastruktur, die die Aggregation von Risikodaten und das Risikoberichtswesen in normalen Zeiten und in Krisen vollständig unterstützt, und der EZB-Leitfaden fordert eine dokumentierte, integrierte Datenarchitektur mit einem Verzeichnis fachlicher Definitionen und einem Metadaten-Repository. Ein Warehouse mit integrierten Quellen und einem Metadaten-Repository, wie in der klassischen Architektur, ist ein Weg, dies bereitzustellen (Chaudhuri & Dayal, 1997).

### Merksatz
Ein Data Warehouse kopiert Daten aus den operativen Systemen in einen getrennten, integrierten und historisierten Bestand, der für analytische Abfragen statt für Transaktionen organisiert und physisch optimiert ist.

### Quellen
- Chaudhuri, S. & Dayal, U. (1997). *An Overview of Data Warehousing and OLAP Technology.* ACM SIGMOD Record 26(1). [sigmodrecord.org](https://sigmodrecord.org/publications/sigmodRecord/9703/pdfs/248603.248616.pdf)
- Stonebraker, M. et al. (2005). *C-Store: A Column-oriented DBMS.* VLDB 2005. [vldb.org](https://www.vldb.org/archives/website/2005/program/paper/thu/p553-stonebraker.pdf)
- Melnik, S. et al. (2010). *Dremel: Interactive Analysis of Web-Scale Datasets.* PVLDB 3(1). [research.google.com](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf)
- Dageville, B. et al. (2016). *The Snowflake Elastic Data Warehouse.* SIGMOD 2016. [snowflake.net](https://info.snowflake.net/rs/252-RFO-227/images/Snowflake_SIGMOD.pdf)
- Kimball Group (n.d.). *Enterprise Data Warehouse Bus Architecture.* Kimball Dimensional Modeling Techniques. [kimballgroup.com](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/enterprise-data-warehouse-bus-architecture/)
- Kimball Group (n.d.). *Conformed Dimensions.* Kimball Dimensional Modeling Techniques. [kimballgroup.com](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/conformed-dimension/)
