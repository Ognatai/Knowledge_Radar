---
title_en: Stream Processing
title_de: Stream Processing
entity_type: Concept
aliases:
- Stream processing
- Event stream processing
- Event streaming
- Streaming data processing
- Unbounded data processing
- Dataflow Model
- Event time
- Structured Streaming
- Streamverarbeitung
sources:
- https://kafka.apache.org/intro
- https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/
- https://spark.apache.org/docs/latest/streaming/getting-started.html
- https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Stream processing computes results continuously over data that keeps arriving, such as payments, sensor readings or clicks, instead of waiting for a complete data set (Kafka docs: Introduction). Because such data is unbounded and often arrives out of order, stream processors distinguish when an event happened (event time) from when it is processed (processing time), group events into windows and use watermarks to estimate when a window is complete (Akidau et al., 2015; Flink docs: Timely stream processing). Platforms such as Apache Kafka store the event streams durably and decouple producers from consumers, while engines such as Apache Flink, Spark Structured Streaming and Google Cloud Dataflow run the computations (Kafka docs: Introduction; Spark docs: Structured Streaming; Akidau et al., 2015).

### How it works

```text
producers ──► topic (partitions P1…Pn, replicated, retained) ──► stream processor ──► sink
 (apps,          events: key, value, timestamp                   │                     (database,
  sensors)                                                       │                      dashboard,
                                                                 ▼                      next topic)
                     assign event time ─► window (fixed / sliding / session)
                     watermark W(t): "no more events ≤ t expected"
                     trigger: emit result (pane) at watermark, periodically or per count
                     late data: update earlier result (accumulate / retract)
```

#### 1. Event streams and logs

An event records that something happened and has a key, a value, a timestamp and optional headers, for example key "Alice", value "Made a payment of $200 to Bob" (Kafka docs: Introduction). In Kafka, producers write events to topics and consumers read them; producers and consumers are fully decoupled, so producers never wait for consumers (Kafka docs: Introduction). Unlike traditional messaging systems, events are not deleted after consumption but kept for a configurable retention period and can be read as often as needed (Kafka docs: Introduction). Topics are split into partitions spread over several brokers; events with the same key go to the same partition, which every consumer reads in the order written, and partitions are commonly replicated three times for fault tolerance (Kafka docs: Introduction). Kafka Streams adds transformations, aggregations, joins and windowing on top (Kafka docs: Introduction; [[data-pipelines|data pipelines]]).

#### 2. Event time and processing time

Event time is when an event actually occurred on its producing device; processing time is the clock of the machine processing it (Flink docs: Timely stream processing). Processing time is simplest and has the lowest latency but is not deterministic, because results depend on how fast records arrive and on outages (Flink docs: Timely stream processing). Event time gives consistent results even for out-of-order, late or replayed historical data, at the cost of waiting for late events (Flink docs: Timely stream processing). The gap between the two domains, event-time skew, changes constantly with communication delays and scheduling (Akidau et al., 2015).

#### 3. Windows

Because a stream is unbounded, aggregates such as counts or sums are scoped by windows, "count over the last 5 minutes" or "sum of the last 100 elements" (Flink docs: Timely stream processing). Fixed (tumbling) windows have a static size such as one hour; sliding windows have a size and a slide period, for example hourly windows starting every minute, and may overlap; session windows group a key's events until a gap of inactivity (Akidau et al., 2015). Filtering, mapping and inner joins need no windows; aggregations and outer joins do (Akidau et al., 2015).

#### 4. Watermarks, triggers and late data

A watermark Watermark(t) flows inline with the data and declares that no more events with timestamps up to t are expected; an operator with several inputs takes the minimum of their event times (Flink docs: Timely stream processing). For most real-world sources a perfect watermark is impossible, so watermarks are heuristic: sometimes too fast, letting late data arrive behind them, and sometimes too slow, held back by a single slow datum (Akidau et al., 2015). The Dataflow Model therefore adds triggers, which decide when in processing time a window's result is emitted, and three refinement modes for later results: discarding, accumulating, or accumulating and retracting the earlier value (Akidau et al., 2015). It splits every pipeline into four questions: what is computed, where in event time, when in processing time, and how refinements relate (Akidau et al., 2015).

#### 5. Streams as tables and exactly-once results

Spark Structured Streaming treats a live stream as a table that is continuously appended; a query is written like a batch query and run incrementally, keeping only the minimal state needed, such as running counts (Spark docs: Structured Streaming). Results go to the sink in complete, append or update mode (Spark docs: Structured Streaming). For end-to-end exactly-once results, sources must be replayable with offsets, as in Kafka, the engine records progress with checkpointing and write-ahead logs, and sinks are idempotent (Spark docs: Structured Streaming; [[apache-spark|Apache Spark]]).

#### Origin and variants

The Dataflow Model, presented at VLDB 2015, describes the processing model of Google Cloud Dataflow, built on FlumeJava and MillWheel, with an open-source runtime-agnostic SDK (Akidau et al., 2015; [[google|Google]]). It argues for the terms unbounded and bounded data instead of streaming and batch, which describe execution engines: batch systems have long processed unbounded data in repeated runs, and streaming systems can process bounded data (Akidau et al., 2015). The Lambda Architecture runs a streaming and a batch pipeline side by side; it reaches many goals but requires building and maintaining two systems (Akidau et al., 2015). Flink implements many techniques from the Dataflow Model (Flink docs: Timely stream processing).

### When to use it

- Results are needed as events happen: real-time payments, fleet tracking, sensor data from factories, customer orders or patient monitoring (Kafka docs: Introduction; [[time-series-analysis|time series]]).
- Detecting anomalies or fraud on live data ([[anomaly-detection|anomaly detection]]).
- Connecting services and departments through durable event streams, for example in event-driven architectures and microservices (Kafka docs: Introduction; [[asynchronous-apis|asynchronous APIs]]).

### Strengths and limitations

**Strengths**
- Low latency: results update continuously instead of after each batch run (Akidau et al., 2015).
- Durable, replayable logs decouple producers from consumers and allow reprocessing of historical data (Kafka docs: Introduction).
- One model can trade correctness, latency and cost per use case (Akidau et al., 2015).

**Limitations**
- Completeness of unbounded data can never be known for certain; watermarks are estimates (Akidau et al., 2015).
- Waiting for late events adds latency, and only a finite wait is possible (Flink docs: Timely stream processing).
- Constraints of CPU, memory and disk remain; what is impractical in batch stays impractical in streaming (Akidau et al., 2015).

### Comparison

| Aspect | Batch processing | Stream processing |
|---|---|---|
| Input | bounded, complete slice | unbounded, continuous |
| Latency | per run (hours, days) | seconds or less |
| Grouping | whole data set or interval | windows over event time |
| Completeness | known when run starts | estimated via watermarks |
| Corrections | rerun the job | triggers, accumulation, retractions |

Sources: Akidau et al. (2015); Flink docs: Timely stream processing; [[data-pipelines|data pipelines]].

### Key takeaway

Stream processing treats data as an unbounded flow: events are grouped into event-time windows, watermarks estimate completeness and triggers decide when to emit and refine results.

### Sources

- Apache Software Foundation. *Introduction.* Apache Kafka documentation. [kafka.apache.org](https://kafka.apache.org/intro)
- Apache Software Foundation. *Timely Stream Processing.* Apache Flink documentation. [nightlies.apache.org](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/)
- Apache Software Foundation. *Structured Streaming Programming Guide.* Apache Spark documentation. [spark.apache.org](https://spark.apache.org/docs/latest/streaming/getting-started.html)
- Akidau, T., Bradshaw, R., Chambers, C., Chernyak, S., Fernández-Moctezuma, R. J., Lax, R., McVeety, S., Mills, D., Perry, F., Schmidt, E. & Whittle, S. (2015). *The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing.* PVLDB 8(12). [vldb.org](https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Stream Processing berechnet Ergebnisse fortlaufend über Daten, die ständig eintreffen, etwa Zahlungen, Sensorwerte oder Klicks, statt auf einen vollständigen Datensatz zu warten (Kafka docs: Introduction). Weil solche Daten unbegrenzt sind und oft ungeordnet ankommen, unterscheiden Stream-Prozessoren, wann ein Ereignis geschah (Event Time), von dem Zeitpunkt, zu dem es verarbeitet wird (Processing Time), fassen Ereignisse in Fenstern zusammen und schätzen mit Watermarks, wann ein Fenster vollständig ist (Akidau et al., 2015; Flink docs: Timely stream processing). Plattformen wie Apache Kafka speichern die Event-Streams dauerhaft und entkoppeln Producer von Consumern, während Engines wie Apache Flink, Spark Structured Streaming und Google Cloud Dataflow die Berechnungen ausführen (Kafka docs: Introduction; Spark docs: Structured Streaming; Akidau et al., 2015).

### Funktionsweise

```text
Producer ──► Topic (Partitionen P1…Pn, repliziert, aufbewahrt) ──► Stream-Prozessor ──► Senke
 (Anwendungen,   Events: Schlüssel, Wert, Zeitstempel               │                   (Datenbank,
  Sensoren)                                                         │                    Dashboard,
                                                                    ▼                    nächstes Topic)
                     Event Time zuordnen ─► Fenster (fest / gleitend / Session)
                     Watermark W(t): „keine Events ≤ t mehr erwartet“
                     Trigger: Ergebnis (Pane) bei Watermark, periodisch oder pro Anzahl ausgeben
                     verspätete Daten: früheres Ergebnis aktualisieren (akkumulieren / zurücknehmen)
```

#### 1. Event-Streams und Logs

Ein Event hält fest, dass etwas geschehen ist, und hat einen Schlüssel, einen Wert, einen Zeitstempel und optionale Header, etwa Schlüssel „Alice“, Wert „Made a payment of $200 to Bob“ (Kafka docs: Introduction). In Kafka schreiben Producer Events in Topics, und Consumer lesen sie; Producer und Consumer sind vollständig entkoppelt, sodass Producer nie auf Consumer warten (Kafka docs: Introduction). Anders als bei klassischen Messaging-Systemen werden Events nach dem Lesen nicht gelöscht, sondern für eine einstellbare Aufbewahrungsdauer gespeichert und können beliebig oft gelesen werden (Kafka docs: Introduction). Topics sind in Partitionen aufgeteilt, die auf mehrere Broker verteilt sind; Events mit demselben Schlüssel landen in derselben Partition, die jeder Consumer in Schreibreihenfolge liest, und Partitionen werden zur Ausfallsicherheit üblicherweise dreifach repliziert (Kafka docs: Introduction). Kafka Streams ergänzt Transformationen, Aggregationen, Joins und Fenster (Kafka docs: Introduction; [[data-pipelines|Datenpipelines]]).

#### 2. Event Time und Processing Time

Event Time ist der Zeitpunkt, zu dem ein Ereignis auf dem erzeugenden Gerät tatsächlich eintrat; Processing Time ist die Uhr der verarbeitenden Maschine (Flink docs: Timely stream processing). Processing Time ist am einfachsten und hat die geringste Latenz, ist aber nicht deterministisch, weil die Ergebnisse davon abhängen, wie schnell Datensätze ankommen, und von Ausfällen (Flink docs: Timely stream processing). Event Time liefert konsistente Ergebnisse auch bei ungeordneten, verspäteten oder erneut eingespielten historischen Daten, um den Preis des Wartens auf verspätete Events (Flink docs: Timely stream processing). Der Abstand zwischen beiden Zeitdomänen, der Event-Time-Skew, ändert sich ständig mit Kommunikationsverzögerungen und Scheduling (Akidau et al., 2015).

#### 3. Fenster

Weil ein Stream unbegrenzt ist, werden Aggregate wie Zählungen oder Summen auf Fenster bezogen, „Anzahl in den letzten 5 Minuten“ oder „Summe der letzten 100 Elemente“ (Flink docs: Timely stream processing). Feste (Tumbling) Fenster haben eine feste Größe wie eine Stunde; gleitende Fenster haben eine Größe und eine Schrittweite, etwa stündliche Fenster, die jede Minute beginnen, und können sich überlappen; Session-Fenster fassen die Events eines Schlüssels bis zu einer Inaktivitätslücke zusammen (Akidau et al., 2015). Filtern, Abbilden und Inner Joins brauchen keine Fenster, Aggregationen und Outer Joins schon (Akidau et al., 2015).

#### 4. Watermarks, Trigger und verspätete Daten

Eine Watermark Watermark(t) fließt mit den Daten und erklärt, dass keine Events mit Zeitstempeln bis t mehr erwartet werden; ein Operator mit mehreren Eingängen übernimmt das Minimum ihrer Event Times (Flink docs: Timely stream processing). Für die meisten realen Quellen ist eine perfekte Watermark unmöglich, Watermarks sind daher heuristisch: mal zu schnell, sodass verspätete Daten hinter ihnen eintreffen, mal zu langsam, weil ein einziger langsamer Datensatz sie aufhält (Akidau et al., 2015). Das Dataflow-Modell ergänzt deshalb Trigger, die festlegen, wann in Processing Time das Ergebnis eines Fensters ausgegeben wird, und drei Modi für spätere Ergebnisse: Verwerfen, Akkumulieren oder Akkumulieren mit Zurücknahme des früheren Werts (Akidau et al., 2015). Es zerlegt jede Pipeline in vier Fragen: was berechnet wird, wo in Event Time, wann in Processing Time und wie Verfeinerungen zusammenhängen (Akidau et al., 2015).

#### 5. Streams als Tabellen und Exactly-once-Ergebnisse

Spark Structured Streaming behandelt einen Live-Stream als Tabelle, an die fortlaufend Zeilen angehängt werden; eine Abfrage wird wie eine Batch-Abfrage geschrieben und inkrementell ausgeführt, wobei nur der minimal nötige Zustand, etwa laufende Zählungen, erhalten bleibt (Spark docs: Structured Streaming). Ergebnisse gehen im Complete-, Append- oder Update-Modus an die Senke (Spark docs: Structured Streaming). Für Exactly-once-Ergebnisse von Ende zu Ende müssen Quellen mit Offsets wiederholbar sein, wie bei Kafka, die Engine hält den Fortschritt mit Checkpoints und Write-Ahead-Logs fest, und Senken sind idempotent (Spark docs: Structured Streaming; [[apache-spark|Apache Spark]]).

#### Ursprung und Varianten

Das Dataflow-Modell, vorgestellt auf der VLDB 2015, beschreibt das Verarbeitungsmodell von Google Cloud Dataflow, das auf FlumeJava und MillWheel aufbaut, mit einem quelloffenen, laufzeitunabhängigen SDK (Akidau et al., 2015; [[google|Google]]). Es plädiert für die Begriffe unbegrenzte und begrenzte Daten statt Streaming und Batch, die Ausführungs-Engines beschreiben: Batch-Systeme verarbeiten unbegrenzte Daten seit jeher in wiederholten Läufen, und Streaming-Systeme können begrenzte Daten verarbeiten (Akidau et al., 2015). Die Lambda-Architektur betreibt eine Streaming- und eine Batch-Pipeline nebeneinander; sie erreicht viele Ziele, verlangt aber, zwei Systeme zu bauen und zu pflegen (Akidau et al., 2015). Flink setzt viele Techniken des Dataflow-Modells um (Flink docs: Timely stream processing).

### Wann einsetzen

- Ergebnisse werden gebraucht, während Ereignisse geschehen: Zahlungen in Echtzeit, Flottenverfolgung, Sensordaten aus Fabriken, Kundenbestellungen oder Patientenüberwachung (Kafka docs: Introduction; [[time-series-analysis|Zeitreihen]]).
- Anomalien oder Betrug in Live-Daten erkennen ([[anomaly-detection|Anomalieerkennung]]).
- Dienste und Abteilungen über dauerhafte Event-Streams verbinden, etwa in ereignisgetriebenen Architekturen und Microservices (Kafka docs: Introduction; [[asynchronous-apis|asynchrone APIs]]).

### Stärken und Grenzen

**Stärken**
- Geringe Latenz: Ergebnisse aktualisieren sich fortlaufend statt nach jedem Batch-Lauf (Akidau et al., 2015).
- Dauerhafte, wiederholbare Logs entkoppeln Producer von Consumern und erlauben die erneute Verarbeitung historischer Daten (Kafka docs: Introduction).
- Ein Modell kann Korrektheit, Latenz und Kosten je Anwendungsfall abwägen (Akidau et al., 2015).

**Grenzen**
- Die Vollständigkeit unbegrenzter Daten ist nie sicher bekannt; Watermarks sind Schätzungen (Akidau et al., 2015).
- Warten auf verspätete Events erhöht die Latenz, und nur ein endliches Warten ist möglich (Flink docs: Timely stream processing).
- Grenzen von CPU, Speicher und Festplatte bleiben; was im Batch unpraktikabel ist, bleibt es auch im Streaming (Akidau et al., 2015).

### Vergleich

| Aspekt | Batch-Verarbeitung | Stream Processing |
|---|---|---|
| Eingabe | begrenzter, vollständiger Ausschnitt | unbegrenzt, fortlaufend |
| Latenz | pro Lauf (Stunden, Tage) | Sekunden oder weniger |
| Gruppierung | ganzer Datensatz oder Intervall | Fenster über Event Time |
| Vollständigkeit | bei Laufbeginn bekannt | über Watermarks geschätzt |
| Korrekturen | Job erneut ausführen | Trigger, Akkumulation, Zurücknahmen |

Quellen: Akidau et al. (2015); Flink docs: Timely stream processing; [[data-pipelines|Datenpipelines]].

### Merksatz

Stream Processing behandelt Daten als unbegrenzten Fluss: Events werden in Event-Time-Fenstern gruppiert, Watermarks schätzen die Vollständigkeit, und Trigger entscheiden, wann Ergebnisse ausgegeben und verfeinert werden.

### Quellen

- Apache Software Foundation. *Introduction.* Apache Kafka documentation. [kafka.apache.org](https://kafka.apache.org/intro)
- Apache Software Foundation. *Timely Stream Processing.* Apache Flink documentation. [nightlies.apache.org](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/)
- Apache Software Foundation. *Structured Streaming Programming Guide.* Apache Spark documentation. [spark.apache.org](https://spark.apache.org/docs/latest/streaming/getting-started.html)
- Akidau, T., Bradshaw, R., Chambers, C., Chernyak, S., Fernández-Moctezuma, R. J., Lax, R., McVeety, S., Mills, D., Perry, F., Schmidt, E. & Whittle, S. (2015). *The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing.* PVLDB 8(12). [vldb.org](https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf)
