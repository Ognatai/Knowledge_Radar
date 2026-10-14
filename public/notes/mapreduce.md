---
title_en: MapReduce
title_de: MapReduce
entity_type: Method
aliases:
- MapReduce
- Map-Reduce
- Hadoop MapReduce
- Apache Hadoop
- Hadoop
sources:
- https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/
- https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html
- https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

MapReduce is "a programming model and an associated implementation for processing and generating large data sets": users write a map function that turns each input key/value pair into intermediate key/value pairs and a reduce function that merges all intermediate values with the same key, and the runtime takes care of partitioning the input, scheduling across thousands of machines, handling machine failures and moving data between them (Dean & Ghemawat, 2004). Google introduced it in 2004 for jobs such as building its web search index; Apache Hadoop made it widely available as open source (Dean & Ghemawat, 2004; Apache Hadoop). Because every job reads from and writes to a distributed file system, MapReduce is inefficient for iterative algorithms and interactive analysis, which motivated in-memory successors such as [[apache-spark|Apache Spark]] (Zaharia et al., 2012).

### How it works

```text
input files in a distributed file system, split into M pieces (16–64 MB)
 ▼
map tasks (in parallel, close to the data): map(k1, v1) → list(k2, v2)
 ▼
optional combiner: partial aggregation on the map machine
 ▼
partition intermediate pairs into R regions, e.g. hash(key) mod R, written to local disk
 ▼
shuffle: reduce workers fetch their region from every map worker, sort by key
 ▼
reduce tasks: reduce(k2, list(v2)) → list(v2), one output file per reduce task
```

#### 1. The programming model

The computation takes a set of input key/value pairs and produces a set of output key/value pairs. Map, written by the user, takes one input pair and produces intermediate pairs; the library groups all intermediate values with the same key and passes them to Reduce, which merges them into a usually smaller set, often zero or one value (Dean & Ghemawat, 2004). The types are `map (k1, v1) → list(k2, v2)` and `reduce (k2, list(v2)) → list(v2)`. The canonical example is counting words: map emits `(word, 1)` for every word in a document, reduce sums the counts per word. Other examples from the paper are distributed grep, counting URL accesses, the reverse web-link graph, term vectors per host, distributed sort and building an [[inverted-index|inverted index]], where map emits `(word, document ID)` and reduce emits the sorted list of document IDs per word (Dean & Ghemawat, 2004). The model is inspired by the map and reduce primitives of Lisp and other functional languages.

#### 2. Execution

The library splits the input into M pieces of typically 16 to 64 MB and starts copies of the program on the cluster; one copy, the master, assigns M map tasks and R reduce tasks to idle workers (Dean & Ghemawat, 2004). A map worker reads its split, calls Map for each record and periodically writes the buffered intermediate pairs to local disk, partitioned into R regions by a partitioning function, by default `hash(key) mod R`. The master passes the locations to the reduce workers, which read their region from all map workers by remote procedure call, sort it by key (with an external sort if it does not fit in memory) and call Reduce once per key; each reduce task appends to its own output file (Dean & Ghemawat, 2004). M and R are chosen much larger than the number of machines for load balancing; Dean & Ghemawat (2004) report typical runs with M = 200,000 and R = 5,000 on 2,000 machines.

#### 3. Fault tolerance

The master pings workers periodically; when one fails, its in-progress tasks and its completed map tasks are rescheduled elsewhere, because map output lives on the failed machine's local disk, while completed reduce output is already in the global file system (Dean & Ghemawat, 2004). Re-execution is the main recovery mechanism: in one job, network maintenance made groups of 80 machines unreachable for minutes, and the job still completed. Atomic commits of task outputs ensure that deterministic map and reduce functions give the same result as a sequential run. A single master failure aborts the job (Dean & Ghemawat, 2004).

#### 4. Refinements

Several refinements matter in practice (Dean & Ghemawat, 2004):
- **Locality:** the master schedules map tasks on machines that hold a replica of the input block in the Google File System, so most input is read locally.
- **Backup tasks:** near the end of a job, the remaining tasks are run a second time to work around stragglers, slow machines that would otherwise delay completion; without them, the sort benchmark took 44% longer.
- **Combiner:** when Reduce is commutative and associative, a combiner pre-aggregates map output on the map machine, for example summing the many `(the, 1)` pairs in word counting before they cross the network.
- **Custom partitioning and ordering:** a partitioning function such as `hash(Hostname(urlkey)) mod R` puts all URLs of a host in one output file; within a partition keys are processed in sorted order.
- **Skipping bad records:** records that make user code crash deterministically can be skipped.

#### 5. Hadoop MapReduce

Apache Hadoop implements the same model in Java: "Hadoop MapReduce is a software framework for easily writing applications which process vast amounts of data" on clusters of commodity hardware (Apache Hadoop). Storage in HDFS and compute share the same nodes, so tasks are scheduled where the data is. Resource management uses a ResourceManager, a NodeManager per node and an application master per job; the stages are Mapper, optional Combiner, Partitioner (by default hashing), shuffle and sort over HTTP, and Reducer. Jobs can also be written in other languages through Hadoop Streaming, which runs any executable as mapper or reducer, or Hadoop Pipes for C++ (Apache Hadoop).

#### Origin and variants

Jeffrey Dean and Sanjay Ghemawat presented MapReduce at OSDI 2004. At Google it replaced the ad-hoc distributed passes of the production indexing system, which processed more than 20 TB of crawled documents in five to ten MapReduce operations; one phase shrank from about 3,800 to about 700 lines of C++ (Dean & Ghemawat, 2004). Hadoop followed as an open-source implementation (Apache Hadoop). Spark generalised the model with resilient distributed datasets that keep intermediate data in memory and can express MapReduce as a special case (Zaharia et al., 2012).

### When to use it

- One-pass batch jobs over very large datasets that are easy to split: log analysis, counting, sorting, building indexes (Dean & Ghemawat, 2004).
- Existing Hadoop clusters with data already in HDFS (Apache Hadoop).
- As a mental model: many distributed data operations, including those in Spark and [[sql|SQL]] engines, are combinations of map, shuffle by key and reduce (Zaharia et al., 2012).

### Strengths and limitations

**Strengths**
- Programmers without experience in distributed systems can use a large cluster, because parallelisation, distribution and fault tolerance are hidden in the library (Dean & Ghemawat, 2004).
- Scales to thousands of commodity machines and tolerates frequent failures through re-execution (Dean & Ghemawat, 2004).
- Data locality saves scarce network bandwidth (Dean & Ghemawat, 2004).

**Limitations**
- The only way to reuse data between jobs is to write it to stable storage, which makes iterative ML and graph algorithms such as PageRank, k-means or logistic regression slow (Zaharia et al., 2012).
- Not suited to interactive queries; Spark was up to 20 times faster than Hadoop for iterative applications (Zaharia et al., 2012).
- Expressing multi-step logic requires chaining several jobs, each with a full shuffle through disk (Dean & Ghemawat, 2004; Zaharia et al., 2012).

### Comparison

| | MapReduce / Hadoop | [[apache-spark\|Apache Spark]] |
|---|---|---|
| Data between steps | written to the distributed file system | kept in memory as RDDs or DataFrames |
| Fault tolerance | re-execution of tasks, replicated storage | recomputation from lineage |
| Programming model | map and reduce functions | many operators, SQL, DataFrames |
| Iterative and interactive work | slow | designed for it |

Sources: Dean & Ghemawat (2004); Zaharia et al. (2012). Today's data platforms build on these ideas, see [[data-lakehouse|data lakehouse]] and [[data-pipelines|data pipelines]].

### In practice

The word-count pattern, including the combiner, is the standard first example in both Google's paper and the Hadoop tutorial (Dean & Ghemawat, 2004; Apache Hadoop). PageRank, which iterates over a link graph, is a classic case where MapReduce is slow because every iteration writes to disk (Zaharia et al., 2012); see [[pagerank|PageRank]].

### Key takeaway

MapReduce expresses a large batch computation as a map over input records and a reduce over all values per key, and a runtime parallelises it across a cluster with locality and re-execution for fault tolerance; its disk-based data sharing led to in-memory successors such as Spark.

### Sources

- Dean, J. & Ghemawat, S. (2004). *MapReduce: Simplified Data Processing on Large Clusters.* OSDI 2004. [research.google](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/)
- Apache Hadoop. *MapReduce Tutorial.* Hadoop documentation. [hadoop.apache.org](https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)
- Zaharia, M., Chowdhury, M., Das, T., Dave, A., Ma, J., McCauley, M., Franklin, M. J., Shenker, S. & Stoica, I. (2012). *Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing.* NSDI 2012. [usenix.org](https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

MapReduce ist „a programming model and an associated implementation for processing and generating large data sets“: Nutzende schreiben eine Map-Funktion, die jedes Eingabepaar aus Schlüssel und Wert in Zwischenpaare umwandelt, und eine Reduce-Funktion, die alle Zwischenwerte mit demselben Schlüssel zusammenführt; die Laufzeitumgebung übernimmt das Aufteilen der Eingabe, die Verteilung auf Tausende Rechner, den Umgang mit Rechnerausfällen und den Datentransport zwischen ihnen (Dean & Ghemawat, 2004). Google führte es 2004 für Aufgaben wie den Aufbau seines Suchindex ein; Apache Hadoop machte es als Open Source breit verfügbar (Dean & Ghemawat, 2004; Apache Hadoop). Weil jeder Job aus einem verteilten Dateisystem liest und in eines schreibt, ist MapReduce für iterative Algorithmen und interaktive Analysen ineffizient, was In-Memory-Nachfolger wie [[apache-spark|Apache Spark]] hervorbrachte (Zaharia et al., 2012).

### Funktionsweise

```text
Eingabedateien in einem verteilten Dateisystem, aufgeteilt in M Teile (16–64 MB)
 ▼
Map-Tasks (parallel, nahe an den Daten): map(k1, v1) → list(k2, v2)
 ▼
optionaler Combiner: Teilaggregation auf dem Map-Rechner
 ▼
Zwischenpaare in R Bereiche partitionieren, z. B. hash(key) mod R, auf lokale Platte schreiben
 ▼
Shuffle: Reduce-Worker holen ihren Bereich von jedem Map-Worker und sortieren nach Schlüssel
 ▼
Reduce-Tasks: reduce(k2, list(v2)) → list(v2), eine Ausgabedatei je Reduce-Task
```

#### 1. Das Programmiermodell

Die Berechnung nimmt eine Menge von Eingabepaaren aus Schlüssel und Wert und erzeugt eine Menge von Ausgabepaaren. Map, von den Nutzenden geschrieben, nimmt ein Eingabepaar und erzeugt Zwischenpaare; die Bibliothek gruppiert alle Zwischenwerte mit demselben Schlüssel und übergibt sie an Reduce, das sie zu einer meist kleineren Menge zusammenführt, oft zu null oder einem Wert (Dean & Ghemawat, 2004). Die Typen lauten `map (k1, v1) → list(k2, v2)` und `reduce (k2, list(v2)) → list(v2)`. Das Standardbeispiel ist das Zählen von Wörtern: Map gibt für jedes Wort eines Dokuments `(Wort, 1)` aus, Reduce summiert die Zählungen je Wort. Weitere Beispiele aus dem Paper sind verteiltes Grep, das Zählen von URL-Zugriffen, der umgekehrte Link-Graph, Termvektoren je Host, verteiltes Sortieren und der Aufbau eines [[inverted-index|Inverted Index]], bei dem Map `(Wort, Dokument-ID)` ausgibt und Reduce die sortierte Liste der Dokument-IDs je Wort (Dean & Ghemawat, 2004). Das Modell ist von den Primitiven map und reduce in Lisp und anderen funktionalen Sprachen inspiriert.

#### 2. Ausführung

Die Bibliothek teilt die Eingabe in M Teile von typischerweise 16 bis 64 MB und startet Kopien des Programms im Cluster; eine Kopie, der Master, verteilt M Map-Tasks und R Reduce-Tasks an freie Worker (Dean & Ghemawat, 2004). Ein Map-Worker liest seinen Teil, ruft Map für jeden Datensatz auf und schreibt die gepufferten Zwischenpaare regelmäßig auf die lokale Platte, aufgeteilt in R Bereiche durch eine Partitionsfunktion, standardmäßig `hash(key) mod R`. Der Master gibt die Speicherorte an die Reduce-Worker weiter, die ihren Bereich per Remote Procedure Call von allen Map-Workern lesen, nach Schlüssel sortieren (mit externem Sortieren, wenn er nicht in den Speicher passt) und Reduce einmal je Schlüssel aufrufen; jeder Reduce-Task schreibt in seine eigene Ausgabedatei (Dean & Ghemawat, 2004). M und R werden deutlich größer als die Zahl der Rechner gewählt, um die Last auszugleichen; Dean & Ghemawat (2004) berichten von typischen Läufen mit M = 200.000 und R = 5.000 auf 2.000 Rechnern.

#### 3. Fehlertoleranz

Der Master pingt die Worker regelmäßig an; fällt einer aus, werden seine laufenden Tasks und seine abgeschlossenen Map-Tasks anderswo neu eingeplant, weil die Map-Ausgabe auf der lokalen Platte des ausgefallenen Rechners liegt, während abgeschlossene Reduce-Ausgaben bereits im globalen Dateisystem stehen (Dean & Ghemawat, 2004). Erneute Ausführung ist der wichtigste Wiederherstellungsmechanismus: In einem Job machten Netzwerkwartungen Gruppen von 80 Rechnern minutenlang unerreichbar, und der Job wurde dennoch abgeschlossen. Atomare Commits der Task-Ausgaben sorgen dafür, dass deterministische Map- und Reduce-Funktionen dasselbe Ergebnis liefern wie ein sequenzieller Lauf. Fällt der einzige Master aus, bricht der Job ab (Dean & Ghemawat, 2004).

#### 4. Verfeinerungen

Mehrere Verfeinerungen sind in der Praxis wichtig (Dean & Ghemawat, 2004):
- **Lokalität:** Der Master plant Map-Tasks auf Rechnern ein, die eine Kopie des Eingabeblocks im Google File System halten, sodass die meiste Eingabe lokal gelesen wird.
- **Backup-Tasks:** Gegen Ende eines Jobs werden die verbleibenden Tasks ein zweites Mal gestartet, um Nachzügler zu umgehen, langsame Rechner, die den Abschluss sonst verzögern würden; ohne sie dauerte der Sortier-Benchmark 44 % länger.
- **Combiner:** Ist Reduce kommutativ und assoziativ, aggregiert ein Combiner die Map-Ausgabe schon auf dem Map-Rechner vor, beim Wörterzählen etwa die vielen Paare `(the, 1)`, bevor sie über das Netz gehen.
- **Eigene Partitionierung und Reihenfolge:** Eine Partitionsfunktion wie `hash(Hostname(urlkey)) mod R` legt alle URLs eines Hosts in eine Ausgabedatei; innerhalb einer Partition werden Schlüssel sortiert verarbeitet.
- **Überspringen fehlerhafter Datensätze:** Datensätze, die den Nutzercode deterministisch abstürzen lassen, können übersprungen werden.

#### 5. Hadoop MapReduce

Apache Hadoop setzt dasselbe Modell in Java um: „Hadoop MapReduce is a software framework for easily writing applications which process vast amounts of data“ auf Clustern aus Standardhardware (Apache Hadoop). Speicherung in HDFS und Rechenleistung teilen sich dieselben Knoten, sodass Tasks dort eingeplant werden, wo die Daten liegen. Die Ressourcenverwaltung nutzt einen ResourceManager, einen NodeManager je Knoten und einen Application Master je Job; die Stufen sind Mapper, optionaler Combiner, Partitioner (standardmäßig per Hashing), Shuffle und Sortierung über HTTP sowie Reducer. Jobs lassen sich auch in anderen Sprachen schreiben, über Hadoop Streaming, das jedes Programm als Mapper oder Reducer ausführt, oder Hadoop Pipes für C++ (Apache Hadoop).

#### Herkunft und Varianten

Jeffrey Dean und Sanjay Ghemawat stellten MapReduce auf der OSDI 2004 vor. Bei Google ersetzte es die selbstgebauten verteilten Durchläufe des produktiven Indexierungssystems, das mehr als 20 TB gecrawlter Dokumente in fünf bis zehn MapReduce-Operationen verarbeitete; eine Phase schrumpfte von etwa 3.800 auf etwa 700 Zeilen C++ (Dean & Ghemawat, 2004). Hadoop folgte als Open-Source-Implementierung (Apache Hadoop). Spark verallgemeinerte das Modell mit Resilient Distributed Datasets, die Zwischendaten im Speicher halten und MapReduce als Spezialfall ausdrücken können (Zaharia et al., 2012).

### Wann einsetzen

- Batch-Jobs mit einem Durchlauf über sehr große, leicht teilbare Datenmengen: Log-Analyse, Zählen, Sortieren, Indexaufbau (Dean & Ghemawat, 2004).
- Bestehende Hadoop-Cluster mit Daten bereits in HDFS (Apache Hadoop).
- Als Denkmodell: Viele verteilte Datenoperationen, auch in Spark und SQL-Engines, sind Kombinationen aus Map, Shuffle nach Schlüssel und Reduce (Zaharia et al., 2012).

### Stärken und Grenzen

**Stärken**
- Auch Programmierende ohne Erfahrung mit verteilten Systemen können einen großen Cluster nutzen, weil Parallelisierung, Verteilung und Fehlertoleranz in der Bibliothek verborgen sind (Dean & Ghemawat, 2004).
- Skaliert auf Tausende Standardrechner und verkraftet häufige Ausfälle durch erneute Ausführung (Dean & Ghemawat, 2004).
- Datenlokalität spart knappe Netzwerkbandbreite (Dean & Ghemawat, 2004).

**Grenzen**
- Daten lassen sich zwischen Jobs nur über stabilen Speicher weitergeben, was iterative ML- und Graphalgorithmen wie PageRank, k-Means oder logistische Regression langsam macht (Zaharia et al., 2012).
- Nicht für interaktive Abfragen geeignet; Spark war bei iterativen Anwendungen bis zu 20-mal schneller als Hadoop (Zaharia et al., 2012).
- Mehrstufige Logik erfordert verkettete Jobs, jeder mit vollständigem Shuffle über die Festplatte (Dean & Ghemawat, 2004; Zaharia et al., 2012).

### Vergleich

| | MapReduce / Hadoop | [[apache-spark\|Apache Spark]] |
|---|---|---|
| Daten zwischen Schritten | ins verteilte Dateisystem geschrieben | als RDDs oder DataFrames im Speicher gehalten |
| Fehlertoleranz | erneute Ausführung von Tasks, replizierter Speicher | Neuberechnung aus der Lineage |
| Programmiermodell | Map- und Reduce-Funktionen | viele Operatoren, [[sql\|SQL]], DataFrames |
| Iterative und interaktive Arbeit | langsam | dafür entworfen |

Quellen: Dean & Ghemawat (2004); Zaharia et al. (2012). Heutige Datenplattformen bauen auf diesen Ideen auf, siehe [[data-lakehouse|Data Lakehouse]] und [[data-pipelines|Datenpipelines]].

### In der Praxis

Das Muster des Wörterzählens, einschließlich Combiner, ist das übliche erste Beispiel sowohl in Googles Paper als auch im Hadoop-Tutorial (Dean & Ghemawat, 2004; Apache Hadoop). PageRank, das wiederholt über einen Link-Graphen iteriert, ist ein klassischer Fall, in dem MapReduce langsam ist, weil jede Iteration auf die Festplatte schreibt (Zaharia et al., 2012); siehe [[pagerank|PageRank]].

### Merksatz

MapReduce drückt eine große Batch-Berechnung als Map über die Eingabedatensätze und Reduce über alle Werte je Schlüssel aus, und eine Laufzeitumgebung parallelisiert sie über einen Cluster, mit Datenlokalität und erneuter Ausführung für Fehlertoleranz; der Datenaustausch über die Festplatte führte zu In-Memory-Nachfolgern wie Spark.

### Quellen

- Dean, J. & Ghemawat, S. (2004). *MapReduce: Simplified Data Processing on Large Clusters.* OSDI 2004. [research.google](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/)
- Apache Hadoop. *MapReduce Tutorial.* Hadoop-Dokumentation. [hadoop.apache.org](https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)
- Zaharia, M., Chowdhury, M., Das, T., Dave, A., Ma, J., McCauley, M., Franklin, M. J., Shenker, S. & Stoica, I. (2012). *Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing.* NSDI 2012. [usenix.org](https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia)
