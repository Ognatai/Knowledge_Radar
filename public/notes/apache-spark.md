---
title_en: Apache Spark
title_de: Apache Spark
entity_type: Technology
aliases:
- Apache Spark
- Spark
- PySpark
- Spark SQL
- Resilient Distributed Dataset
- RDD
sources:
- https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia
- https://people.csail.mit.edu/matei/papers/2015/sigmod_spark_sql.pdf
- https://spark.apache.org/docs/latest/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Apache Spark is "a unified analytics engine for large-scale data processing" with [[apis|APIs]] in Java, Scala, Python (PySpark) and R and libraries for SQL, pandas-style workloads, machine learning (MLlib), graphs and streaming (Apache Spark). It started at UC Berkeley around resilient distributed datasets (RDDs), immutable partitioned collections that are built by coarse-grained transformations and can be kept in memory, so that iterative algorithms and interactive queries do not have to write every intermediate result to disk as [[mapreduce|MapReduce]] does; lost partitions are recomputed from their lineage (Zaharia et al., 2012). Most code today uses DataFrames and Spark SQL, which are evaluated lazily and optimised by the Catalyst optimiser (Armbrust et al., 2015).

### Core concepts

```text
driver program (SparkSession)
 ▼ builds a logical plan from transformations (lazy)
action (count, collect, write) triggers execution
 ▼ Catalyst: analysis → logical optimisation → physical planning → code generation
DAG of stages, split at shuffles (wide dependencies)
 ▼
tasks on executors, scheduled for data locality; partitions cached in memory if persisted
```

#### 1. Resilient distributed datasets

An RDD is "a read-only, partitioned collection of records" that can only be created by deterministic operations on data in stable storage or on other RDDs (Zaharia et al., 2012). Because these transformations (map, filter, join and others) apply the same operation to many records, Spark only needs to log the transformations, the lineage, instead of replicating data: if a partition is lost, it is recomputed from its parents. Users can persist RDDs they reuse, in memory by default with spilling to disk, and can partition them by key, for example so that two datasets that will be joined are hash-partitioned the same way (Zaharia et al., 2012). RDDs suit batch analytics that apply one operation to all records, not applications with fine-grained, asynchronous updates such as a web application's storage (Zaharia et al., 2012).

#### 2. Transformations, actions and lazy evaluation

Transformations define new datasets, actions return a value or write data, for example `count`, `collect` or `save`; Spark computes RDDs lazily the first time they are used in an action, which lets it pipeline transformations (Zaharia et al., 2012). DataFrames are lazy in the same way: each DataFrame represents a logical plan, and nothing runs until an output operation, which enables optimisation across all operations (Armbrust et al., 2015).

#### 3. Narrow and wide dependencies, stages and shuffles

With a narrow dependency, each parent partition is used by at most one child partition, as with `map` or `filter`; with a wide dependency, several child partitions depend on it, as with a `join` of datasets that are not partitioned alike (Zaharia et al., 2012). Narrow dependencies can be pipelined on one node and recovered cheaply; wide dependencies require a shuffle of data across nodes, "a MapReduce-like operation". When an action runs, the scheduler turns the lineage graph into a DAG of stages split at shuffles, pipelines narrow transformations inside each stage, skips stages whose output is already in memory and assigns tasks to nodes that hold their data (Zaharia et al., 2012).

#### 4. DataFrames, Spark SQL and Catalyst

Spark SQL integrates relational processing with Spark's functional API: DataFrames are distributed collections of rows with a schema that support relational operators such as `where` and `groupBy`, and SQL queries can be mixed with procedural code and libraries such as MLlib (Armbrust et al., 2015). The Catalyst optimiser compiles a query in four phases: analysis to resolve references, rule-based logical optimisation, physical planning, where several plans may be compared by cost, and code generation to Java bytecode (Armbrust et al., 2015). DataFrames store data in a columnar format that is more compact than Java or Python objects (Armbrust et al., 2015).

#### 5. Libraries and deployment

On top of the core, Spark offers Spark SQL, the pandas API on Spark, MLlib for machine learning, GraphX for graphs and Structured Streaming for incremental and stream processing (Apache Spark). Spark Connect, introduced in Spark 3.4, separates client applications from the cluster in a client-server architecture. Spark runs standalone or on Hadoop YARN or [[kubernetes|Kubernetes]]; the current documentation covers version 4.2.0 and Java 17/21/25, Scala 2.13 and Python 3.10 or later (Apache Spark).

### Common usage

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("orders").getOrCreate()
orders = spark.read.parquet("s3://bucket/orders/")          # lazy
daily = (orders.where(F.col("status") == "paid")
               .groupBy("order_date")
               .agg(F.sum("amount").alias("revenue")))     # still lazy
daily.write.mode("overwrite").parquet("s3://bucket/gold/daily_revenue/")  # action
```

| Operation | Kind | Dependency |
|---|---|---|
| `select`, `where` / `filter`, `withColumn`, `map` | transformation | narrow |
| `groupBy().agg()`, `join`, `distinct`, `repartition` | transformation | wide (shuffle) |
| `count`, `collect`, `show`, `write` | action | triggers execution |
| `cache` / `persist` | marks data for reuse | — |

Sources: Zaharia et al. (2012); Armbrust et al. (2015); Apache Spark. The example is illustrative.

### When to use it

- Datasets too large for one machine, for [[data-pipelines|ETL]], aggregation or feature engineering, typically on a [[data-lakehouse|data lakehouse]] (Apache Spark).
- Iterative ML and graph algorithms that reuse data, such as k-means, logistic regression or [[pagerank|PageRank]] (Zaharia et al., 2012).
- Interactive exploration of large data, which Zaharia et al. (2012) demonstrated by scanning 1 TB with 5–7 s latency.

### Strengths and limitations

**Strengths**
- Keeping data in memory made Spark up to 20 times faster than Hadoop for iterative applications in the original evaluation (Zaharia et al., 2012).
- Lineage-based recovery avoids replicating intermediate data (Zaharia et al., 2012).
- One engine for SQL, DataFrames, ML, graphs and streaming, with an optimiser that rewrites whole query plans (Armbrust et al., 2015; Apache Spark).

**Limitations**
- Not designed for fine-grained, asynchronous updates to shared state (Zaharia et al., 2012).
- Wide dependencies require shuffles across the network, and a failed node in a lineage with wide dependencies can force recomputation of many ancestors (Zaharia et al., 2012).

### Comparison

| | [[mapreduce\|MapReduce]] | Spark (RDD) | Spark SQL / DataFrames |
|---|---|---|---|
| Model | map and reduce | functional transformations | relational operators and SQL |
| Intermediate data | on disk | in memory if persisted | in memory, columnar |
| Optimisation | by the programmer | pipelining within stages | Catalyst: rules, cost, code generation |

Sources: Zaharia et al. (2012); Armbrust et al. (2015). Single-machine alternatives for smaller data are described in [[python|Python]] (pandas) and [[sql|SQL]].

### In practice

Wide dependencies mean shuffles across the network, so joins and aggregations are planned around partitioning, for example by hash-partitioning datasets that will be joined in the same way (Zaharia et al., 2012). Several aggregates can be computed in one pass with a single SQL statement, which is hard to express with the functional API (Armbrust et al., 2015). Persisting a DataFrame only pays off when it is reused several times (Zaharia et al., 2012). In ML pipelines, Spark typically prepares features before training, see [[feature-engineering|feature engineering]] and [[ml-pipelines|ML pipelines]].

### Key takeaway

Spark processes large data as immutable, partitioned datasets that are evaluated lazily, kept in memory when reused and recovered from lineage, and its DataFrame and SQL layer lets an optimiser plan the whole computation.

### Sources

- Zaharia, M., Chowdhury, M., Das, T., Dave, A., Ma, J., McCauley, M., Franklin, M. J., Shenker, S. & Stoica, I. (2012). *Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing.* NSDI 2012. [usenix.org](https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia)
- Armbrust, M., Xin, R. S., Lian, C., Huai, Y., Liu, D., Bradley, J. K., Meng, X., Kaftan, T., Franklin, M. J., Ghodsi, A. & Zaharia, M. (2015). *Spark SQL: Relational Data Processing in Spark.* SIGMOD 2015. [people.csail.mit.edu](https://people.csail.mit.edu/matei/papers/2015/sigmod_spark_sql.pdf)
- Apache Spark. *Spark Overview.* Documentation for Spark 4.2.0. [spark.apache.org](https://spark.apache.org/docs/latest/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Apache Spark ist „a unified analytics engine for large-scale data processing“ mit [[apis|APIs]] in Java, Scala, Python (PySpark) und R sowie Bibliotheken für SQL, pandas-artige Workloads, Machine Learning (MLlib), Graphen und Streaming (Apache Spark). Es entstand an der UC Berkeley rund um Resilient Distributed Datasets (RDDs), unveränderliche, partitionierte Sammlungen, die durch grobgranulare Transformationen entstehen und im Speicher gehalten werden können, damit iterative Algorithmen und interaktive Abfragen nicht wie bei [[mapreduce|MapReduce]] jedes Zwischenergebnis auf die Festplatte schreiben müssen; verlorene Partitionen werden aus ihrer Lineage neu berechnet (Zaharia et al., 2012). Der meiste Code nutzt heute DataFrames und Spark SQL, die verzögert ausgewertet und vom Optimierer Catalyst optimiert werden (Armbrust et al., 2015).

### Kernkonzepte

```text
Driver-Programm (SparkSession)
 ▼ baut aus Transformationen einen logischen Plan (verzögert)
Action (count, collect, write) löst die Ausführung aus
 ▼ Catalyst: Analyse → logische Optimierung → physische Planung → Codegenerierung
DAG aus Stages, getrennt an Shuffles (breite Abhängigkeiten)
 ▼
Tasks auf Executors, nach Datenlokalität eingeplant; Partitionen bei persist im Speicher
```

#### 1. Resilient Distributed Datasets

Ein RDD ist „a read-only, partitioned collection of records“, das nur durch deterministische Operationen auf Daten in stabilem Speicher oder auf anderen RDDs entstehen kann (Zaharia et al., 2012). Weil diese Transformationen (map, filter, join und andere) dieselbe Operation auf viele Datensätze anwenden, muss Spark nur die Transformationen protokollieren, die Lineage, statt Daten zu replizieren: Geht eine Partition verloren, wird sie aus ihren Eltern neu berechnet. Nutzende können wiederverwendete RDDs persistieren, standardmäßig im Speicher mit Auslagerung auf die Platte, und sie nach Schlüssel partitionieren, etwa damit zwei Datensätze, die später verknüpft werden, gleich per Hash partitioniert sind (Zaharia et al., 2012). RDDs eignen sich für Batch-Analysen, die eine Operation auf alle Datensätze anwenden, nicht für Anwendungen mit feingranularen, asynchronen Aktualisierungen wie den Speicher einer Webanwendung (Zaharia et al., 2012).

#### 2. Transformationen, Actions und verzögerte Auswertung

Transformationen definieren neue Datensätze, Actions liefern einen Wert zurück oder schreiben Daten, etwa `count`, `collect` oder `save`; Spark berechnet RDDs verzögert beim ersten Einsatz in einer Action und kann so Transformationen hintereinanderschalten (Zaharia et al., 2012). DataFrames sind ebenso verzögert: Jeder DataFrame steht für einen logischen Plan, und nichts läuft vor einer Ausgabeoperation, was eine Optimierung über alle Operationen hinweg ermöglicht (Armbrust et al., 2015).

#### 3. Schmale und breite Abhängigkeiten, Stages und Shuffles

Bei einer schmalen Abhängigkeit wird jede Elternpartition von höchstens einer Kindpartition genutzt, wie bei `map` oder `filter`; bei einer breiten Abhängigkeit hängen mehrere Kindpartitionen von ihr ab, wie bei einem `join` von Datensätzen, die nicht gleich partitioniert sind (Zaharia et al., 2012). Schmale Abhängigkeiten lassen sich auf einem Knoten hintereinanderschalten und günstig wiederherstellen; breite Abhängigkeiten erfordern einen Shuffle der Daten über die Knoten, „a MapReduce-like operation“. Läuft eine Action, wandelt der Scheduler den Lineage-Graphen in einen DAG aus Stages um, getrennt an Shuffles, schaltet schmale Transformationen innerhalb jeder Stage hintereinander, überspringt Stages, deren Ausgabe schon im Speicher liegt, und weist Tasks den Knoten zu, die ihre Daten halten (Zaharia et al., 2012).

#### 4. DataFrames, Spark SQL und Catalyst

Spark SQL verbindet relationale Verarbeitung mit der funktionalen API von Spark: DataFrames sind verteilte Sammlungen von Zeilen mit Schema, die relationale Operatoren wie `where` und `groupBy` unterstützen, und SQL-Abfragen lassen sich mit prozeduralem Code und Bibliotheken wie MLlib mischen (Armbrust et al., 2015). Der Optimierer Catalyst übersetzt eine Abfrage in vier Phasen: Analyse zum Auflösen von Verweisen, regelbasierte logische Optimierung, physische Planung, bei der mehrere Pläne nach Kosten verglichen werden können, und Codegenerierung zu Java-Bytecode (Armbrust et al., 2015). DataFrames speichern Daten spaltenorientiert und kompakter als Java- oder Python-Objekte (Armbrust et al., 2015).

#### 5. Bibliotheken und Betrieb

Auf dem Kern bietet Spark Spark SQL, die pandas-API auf Spark, MLlib für Machine Learning, GraphX für Graphen und Structured Streaming für inkrementelle und Stream-Verarbeitung (Apache Spark). Spark Connect, eingeführt mit Spark 3.4, trennt Client-Anwendungen in einer Client-Server-Architektur vom Cluster. Spark läuft eigenständig oder auf Hadoop YARN oder [[kubernetes|Kubernetes]]; die aktuelle Dokumentation behandelt Version 4.2.0 sowie Java 17/21/25, Scala 2.13 und Python ab 3.10 (Apache Spark).

### Typische Verwendung

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("orders").getOrCreate()
orders = spark.read.parquet("s3://bucket/orders/")          # verzögert
daily = (orders.where(F.col("status") == "paid")
               .groupBy("order_date")
               .agg(F.sum("amount").alias("revenue")))     # weiterhin verzögert
daily.write.mode("overwrite").parquet("s3://bucket/gold/daily_revenue/")  # Action
```

| Operation | Art | Abhängigkeit |
|---|---|---|
| `select`, `where` / `filter`, `withColumn`, `map` | Transformation | schmal |
| `groupBy().agg()`, `join`, `distinct`, `repartition` | Transformation | breit (Shuffle) |
| `count`, `collect`, `show`, `write` | Action | löst Ausführung aus |
| `cache` / `persist` | markiert Daten zur Wiederverwendung | — |

Quellen: Zaharia et al. (2012); Armbrust et al. (2015); Apache Spark. Das Beispiel dient der Veranschaulichung.

### Wann einsetzen

- Datenmengen, die für einen Rechner zu groß sind, für [[data-pipelines|ETL]], Aggregation oder Feature Engineering, typischerweise auf einem [[data-lakehouse|Data Lakehouse]] (Apache Spark).
- Iterative ML- und Graphalgorithmen, die Daten wiederverwenden, etwa k-Means, logistische Regression oder [[pagerank|PageRank]] (Zaharia et al., 2012).
- Interaktive Erkundung großer Daten; Zaharia et al. (2012) zeigten das Durchsuchen von 1 TB mit 5–7 s Latenz.

### Stärken und Grenzen

**Stärken**
- Daten im Speicher machten Spark in der ursprünglichen Evaluation bei iterativen Anwendungen bis zu 20-mal schneller als Hadoop (Zaharia et al., 2012).
- Wiederherstellung aus der Lineage vermeidet das Replizieren von Zwischendaten (Zaharia et al., 2012).
- Eine Engine für SQL, DataFrames, ML, Graphen und Streaming, mit einem Optimierer, der ganze Abfragepläne umschreibt (Armbrust et al., 2015; Apache Spark).

**Grenzen**
- Nicht für feingranulare, asynchrone Aktualisierungen gemeinsamen Zustands gedacht (Zaharia et al., 2012).
- Breite Abhängigkeiten erfordern Shuffles über das Netzwerk, und ein ausgefallener Knoten in einer Lineage mit breiten Abhängigkeiten kann die Neuberechnung vieler Vorgänger erzwingen (Zaharia et al., 2012).

### Vergleich

| | [[mapreduce\|MapReduce]] | Spark (RDD) | Spark SQL / DataFrames |
|---|---|---|---|
| Modell | Map und Reduce | funktionale Transformationen | relationale Operatoren und SQL |
| Zwischendaten | auf der Platte | im Speicher, wenn persistiert | im Speicher, spaltenorientiert |
| Optimierung | durch die Programmierenden | Hintereinanderschalten in Stages | Catalyst: Regeln, Kosten, Codegenerierung |

Quellen: Zaharia et al. (2012); Armbrust et al. (2015). Alternativen auf einem einzelnen Rechner für kleinere Daten beschreiben [[python|Python]] (pandas) und [[sql|SQL]].

### In der Praxis

Breite Abhängigkeiten bedeuten Shuffles über das Netzwerk, daher werden Joins und Aggregationen um die Partitionierung herum geplant, etwa indem Datensätze, die verknüpft werden, gleich per Hash partitioniert werden (Zaharia et al., 2012). Mehrere Aggregate lassen sich mit einer einzigen SQL-Anweisung in einem Durchlauf berechnen, was mit der funktionalen API schwer auszudrücken ist (Armbrust et al., 2015). Einen DataFrame zu persistieren lohnt sich nur, wenn er mehrfach wiederverwendet wird (Zaharia et al., 2012). In ML-Pipelines bereitet Spark typischerweise Features vor dem Training auf, siehe [[feature-engineering|Feature Engineering]] und [[ml-pipelines|ML-Pipelines]].

### Merksatz

Spark verarbeitet große Datenmengen als unveränderliche, partitionierte Datensätze, die verzögert ausgewertet, bei Wiederverwendung im Speicher gehalten und aus ihrer Lineage wiederhergestellt werden, und seine DataFrame- und SQL-Schicht lässt einen Optimierer die gesamte Berechnung planen.

### Quellen

- Zaharia, M., Chowdhury, M., Das, T., Dave, A., Ma, J., McCauley, M., Franklin, M. J., Shenker, S. & Stoica, I. (2012). *Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing.* NSDI 2012. [usenix.org](https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia)
- Armbrust, M., Xin, R. S., Lian, C., Huai, Y., Liu, D., Bradley, J. K., Meng, X., Kaftan, T., Franklin, M. J., Ghodsi, A. & Zaharia, M. (2015). *Spark SQL: Relational Data Processing in Spark.* SIGMOD 2015. [people.csail.mit.edu](https://people.csail.mit.edu/matei/papers/2015/sigmod_spark_sql.pdf)
- Apache Spark. *Spark Overview.* Dokumentation für Spark 4.2.0. [spark.apache.org](https://spark.apache.org/docs/latest/)
