---
title_en: FAISS
title_de: FAISS
entity_type: Technology
aliases:
- FAISS
- Faiss
sources:
- https://arxiv.org/abs/2401.08281
- https://arxiv.org/abs/1702.08734
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

FAISS (Facebook AI Similarity Search) is an open-source library from [[meta|Meta]] for vector similarity search: "a toolkit of indexing methods and related primitives used to search, cluster, compress and transform vectors" (Douze et al., 2024). It offers exact brute-force search, inverted-file (IVF) indexes that only search the clusters nearest to the query, graph indexes such as [[hnsw|HNSW]], and vector compression with product quantisation, on CPU and GPU (Douze et al., 2024). Its GPU implementation made k-nearest-neighbour search 8.5 times faster than the previous GPU state of the art and built a k-NN graph over 95 million images in 35 minutes (Johnson et al., 2017). FAISS serves as the core engine of, or model for, several [[vector-databases|vector databases]] and is the index behind retrievers such as [[dense-passage-retrieval|DPR]].

### Core concepts

```text
vectors (embeddings)
 ▼ optional preprocessing: PCA, OPQ rotation, normalisation
 ▼ index type:
    Flat        exact search over all vectors
    IVF         coarse quantiser (k-means centroids) → inverted lists; search nprobe nearest lists
    HNSW        layered proximity graph
 ▼ encoding of stored vectors: none (Flat) · scalar quantiser · product quantiser (PQ) · additive quantisers
 ▼ optional refinement: re-rank candidates with exact distances
search(query, k) → k nearest ids and distances  (L2, inner product, cosine via normalisation)
```

#### 1. The trade-off: accuracy, speed, memory

Every vector index trades accuracy against search time and memory, plus index-building time; when the raw data fits in memory several times, memory may not matter, and when the index is built once and queried often, building time may not matter (Douze et al., 2024). FAISS lets users choose the active constraints and measures settings by their Pareto frontier: the fastest setting for a given accuracy. Search-time parameters such as `nprobe` for IVF indexes trade speed for accuracy without rebuilding the index (Douze et al., 2024).

#### 2. Exhaustive search and metrics

`IndexFlat` implements brute-force search and returns exact neighbours (Douze et al., 2024). Besides k-nearest-neighbour search, FAISS supports range search, batched queries, and the metrics L2 distance and inner product; [[text-similarity-metrics|cosine similarity]] is obtained by normalising vectors, and the library documents transformations that let an index for one metric serve another (Douze et al., 2024). Below about 10,000 vectors, exhaustive search is usually sufficient.

#### 3. Inverted files (IVF)

For larger collections, an IVF index clusters the database vectors with a coarse quantiser, typically k-means with K centroids, and stores each cluster's vectors contiguously in an inverted list; at search time only the `nprobe` lists whose centroids are nearest to the query are scanned (Douze et al., 2024). With exhaustive coarse quantisation and uncompressed lists, the number of distance computations is `K + nprobe · N / K`, minimal at `K = √(nprobe · N)`, which gives the common rule of thumb of setting K proportional to √N. For very large K, the coarse quantiser itself can be an HNSW index (Douze et al., 2024).

#### 4. Compression with product quantisation

Product quantisation (PQ) splits each vector into M sub-vectors and quantises each with its own k-means codebook, so a vector is stored as M short codes; `PQ6x10` means 6 sub-vectors with 10 bits each (Douze et al., 2024). Distances are computed directly in the compressed domain using lookup tables. FAISS also offers scalar quantisers, residual and other additive quantisers, and rotations such as OPQ that make PQ more accurate. Combined with IVF, the PQ codes usually encode the residual between a vector and its centroid (IVFPQ). Compression lowers memory use below that of the raw vectors at a cost in accuracy, which a refinement step with exact distances can partly recover (Douze et al., 2024).

#### 5. GPU search

Johnson et al. (2017) designed a GPU k-selection algorithm that runs at up to 55% of theoretical peak performance and optimised brute-force, approximate and compressed-domain search on GPUs. Their implementation was 8.5 times faster than the previous GPU state of the art, built a high-accuracy k-NN graph on 95 million images from YFCC100M in 35 minutes, and a graph connecting 1 billion vectors in less than 12 hours on four GPUs (Johnson et al., 2017).

#### Origin and variants

FAISS was released as open source in 2017 together with the GPU paper (Johnson et al., 2017). By 2024 it had about 37,000 GitHub stars and its packages had been downloaded 6 million times; vector database companies such as Zilliz and Pinecone either use FAISS as their core engine or reimplemented its algorithms (Douze et al., 2024). Related libraries include hnswlib, Google's ScaNN and Microsoft's DiskANN (Douze et al., 2024).

### Common usage

```python
import faiss, numpy as np

d = 768
xb = np.random.rand(100_000, d).astype("float32")   # database vectors
xq = np.random.rand(5, d).astype("float32")          # queries

index = faiss.index_factory(d, "IVF1024,PQ64")      # IVF with 1024 lists, PQ with 64 sub-vectors
index.train(xb)                                      # k-means for centroids and PQ codebooks
index.add(xb)
index.nprobe = 16                                    # lists to scan: speed vs accuracy
distances, ids = index.search(xq, 10)
```

| Factory string | Index | Use |
|---|---|---|
| `Flat` | exact search | small collections, ground truth |
| `HNSW32` | graph with 32 links per node | fast in-memory search |
| `IVF4096,Flat` | inverted file, uncompressed | large collections, exact distances within lists |
| `IVF4096,PQ64` | inverted file with product quantisation | very large collections, low memory |
| `PCA160,IVF20000_HNSW,PQ20x10,RFlat` | PCA, HNSW coarse quantiser, PQ, exact re-ranking | billion-scale with refinement |

Sources: Douze et al. (2024); the code is an illustrative example.

### When to use it

- Similarity search over millions to billions of embeddings inside an application, without running a separate database server (Douze et al., 2024).
- Retrieval for RAG and open-domain question answering, where the passage index is built offline ([[dense-passage-retrieval|DPR]], [[retrieval-augmented-generation|RAG]]).
- [[clustering|Clustering]], [[near-duplicate-detection|deduplication]] and data mining on large datasets, for example removing duplicates from 1.3 billion images or mining bilingual text (Douze et al., 2024).

### Strengths and limitations

**Strengths**
- A broad range of index types and compressions in one library, on CPU and GPU (Douze et al., 2024).
- Scales from thousands to trillions of vectors; one deployment indexed 1.5 trillion 144-dimensional vectors with about 1 second per query (Douze et al., 2024).
- Fast GPU implementations (Johnson et al., 2017).

**Limitations**
- A library, not a database: storage, metadata filtering, access control and replication have to be added around it ([[vector-databases|vector databases]]).
- Choosing an index and its parameters requires measuring the accuracy-speed-memory trade-off on the target data (Douze et al., 2024).
- Compressed indexes return approximate distances and lose some accuracy (Douze et al., 2024).

### Comparison

| | FAISS | [[vector-databases\|Vector database]] |
|---|---|---|
| Type | library of many index types ([[hnsw\|HNSW]], IVF, PQ, …) | server with storage and APIs |
| Compression | PQ, scalar, additive quantisers | depends on product |
| GPU | yes | depends on product |
| Metadata, filters, persistence | to be added by the application | built in |

Sources: Douze et al. (2024); Johnson et al. (2017).

### In practice

The usual workflow is to build an exact `Flat` index on a sample as ground truth, then compare candidate indexes by recall and query time on that sample before choosing one (Douze et al., 2024). Inner product search on normalised vectors gives cosine similarity, a common metric for text [[embeddings|embeddings]] (Douze et al., 2024).

### Key takeaway

FAISS is Meta's open-source toolkit for vector search that combines exact search, inverted files, graph indexes and product quantisation on CPU and GPU, letting users trade accuracy, speed and memory for collections from thousands to trillions of vectors.

### Sources

- Douze, M., Guzhva, A., Deng, C., Johnson, J., Szilvasy, G., Mazaré, P.-E., Lomeli, M., Hosseini, L. & Jégou, H. (2024). *The Faiss library.* arXiv:2401.08281. [arXiv:2401.08281](https://arxiv.org/abs/2401.08281)
- Johnson, J., Douze, M. & Jégou, H. (2017). *Billion-scale similarity search with GPUs.* arXiv:1702.08734. [arXiv:1702.08734](https://arxiv.org/abs/1702.08734)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

FAISS (Facebook AI Similarity Search) ist eine Open-Source-Bibliothek von [[meta|Meta]] für Vektorähnlichkeitssuche: „a toolkit of indexing methods and related primitives used to search, cluster, compress and transform vectors“ (Douze et al., 2024). Sie bietet exakte Brute-Force-Suche, Inverted-File-Indizes (IVF), die nur die der Anfrage nächsten Cluster durchsuchen, Graphindizes wie [[hnsw|HNSW]] und Vektorkompression mit Product Quantization, auf CPU und GPU (Douze et al., 2024). Ihre GPU-Implementierung machte die Suche nach den k nächsten Nachbarn 8,5-mal schneller als der bisherige Stand der Technik auf GPUs und baute einen k-NN-Graphen über 95 Millionen Bilder in 35 Minuten (Johnson et al., 2017). FAISS dient mehreren [[vector-databases|Vektordatenbanken]] als Kern oder Vorbild und ist der Index hinter Retrievern wie [[dense-passage-retrieval|DPR]].

### Kernkonzepte

```text
Vektoren (Embeddings)
 ▼ optionale Vorverarbeitung: PCA, OPQ-Rotation, Normalisierung
 ▼ Indexart:
    Flat        exakte Suche über alle Vektoren
    IVF         Grobquantisierer (k-Means-Zentroide) → invertierte Listen; nprobe nächste Listen durchsuchen
    HNSW        geschichteter Nachbarschaftsgraph
 ▼ Kodierung gespeicherter Vektoren: keine (Flat) · Skalarquantisierer · Product Quantizer (PQ) · additive Quantisierer
 ▼ optionale Verfeinerung: Kandidaten mit exakten Distanzen neu ordnen
search(query, k) → k nächste IDs und Distanzen  (L2, Skalarprodukt, Cosine über Normalisierung)
```

#### 1. Der Zielkonflikt: Genauigkeit, Geschwindigkeit, Speicher

Jeder Vektorindex wägt Genauigkeit gegen Suchzeit und Speicher ab, dazu die Zeit für den Indexaufbau; passen die Rohdaten mehrfach in den Speicher, spielt Speicher womöglich keine Rolle, und wird der Index einmal gebaut und oft abgefragt, spielt die Aufbauzeit womöglich keine Rolle (Douze et al., 2024). FAISS lässt Nutzende die maßgeblichen Bedingungen wählen und bewertet Einstellungen über ihre Pareto-Front: die schnellste Einstellung für eine gegebene Genauigkeit. Parameter zur Suchzeit wie `nprobe` bei IVF-Indizes tauschen Geschwindigkeit gegen Genauigkeit, ohne den Index neu zu bauen (Douze et al., 2024).

#### 2. Erschöpfende Suche und Metriken

`IndexFlat` setzt Brute-Force-Suche um und liefert exakte Nachbarn (Douze et al., 2024). Neben der Suche nach den k nächsten Nachbarn unterstützt FAISS Bereichssuche, gebündelte Anfragen sowie die Metriken L2-Distanz und Skalarprodukt; [[text-similarity-metrics|Cosine Similarity]] ergibt sich durch Normalisierung der Vektoren, und die Bibliothek dokumentiert Transformationen, mit denen ein Index für eine Metrik eine andere bedienen kann (Douze et al., 2024). Unterhalb von etwa 10.000 Vektoren genügt meist erschöpfende Suche.

#### 3. Inverted Files (IVF)

Für größere Sammlungen clustert ein IVF-Index die Datenbankvektoren mit einem Grobquantisierer, typischerweise k-Means mit K Zentroiden, und speichert die Vektoren jedes Clusters zusammenhängend in einer invertierten Liste; zur Suchzeit werden nur die `nprobe` Listen durchsucht, deren Zentroide der Anfrage am nächsten sind (Douze et al., 2024). Bei erschöpfender Grobquantisierung und unkomprimierten Listen beträgt die Zahl der Distanzberechnungen `K + nprobe · N / K`, minimal bei `K = √(nprobe · N)`, woraus die übliche Faustregel folgt, K proportional zu √N zu wählen. Bei sehr großem K kann der Grobquantisierer selbst ein HNSW-Index sein (Douze et al., 2024).

#### 4. Kompression mit Product Quantization

Product Quantization (PQ) zerlegt jeden Vektor in M Teilvektoren und quantisiert jeden mit einem eigenen k-Means-Codebuch, sodass ein Vektor als M kurze Codes gespeichert wird; `PQ6x10` bedeutet 6 Teilvektoren mit je 10 Bit (Douze et al., 2024). Distanzen werden mithilfe von Nachschlagetabellen direkt im komprimierten Raum berechnet. FAISS bietet außerdem Skalarquantisierer, residuale und andere additive Quantisierer sowie Rotationen wie OPQ, die PQ genauer machen. In Verbindung mit IVF kodieren die PQ-Codes meist die Differenz zwischen einem Vektor und seinem Zentroid (IVFPQ). Kompression senkt den Speicherbedarf unter den der Rohvektoren, kostet aber Genauigkeit, die ein Verfeinerungsschritt mit exakten Distanzen teilweise zurückholen kann (Douze et al., 2024).

#### 5. Suche auf der GPU

Johnson et al. (2017) entwarfen einen k-Selection-Algorithmus für GPUs, der bis zu 55 % der theoretischen Spitzenleistung erreicht, und optimierten Brute-Force-, approximative und komprimierte Suche auf GPUs. Ihre Implementierung war 8,5-mal schneller als der bisherige Stand der Technik auf GPUs, baute einen genauen k-NN-Graphen über 95 Millionen Bilder aus YFCC100M in 35 Minuten und einen Graphen über 1 Milliarde Vektoren in weniger als 12 Stunden auf vier GPUs (Johnson et al., 2017).

#### Herkunft und Varianten

FAISS wurde 2017 zusammen mit dem GPU-Paper als Open Source veröffentlicht (Johnson et al., 2017). Bis 2024 hatte es etwa 37.000 GitHub-Sterne, und seine Pakete waren 6 Millionen Mal heruntergeladen worden; Anbieter von Vektordatenbanken wie Zilliz und Pinecone nutzen FAISS als Kern oder haben seine Algorithmen nachgebaut (Douze et al., 2024). Verwandte Bibliotheken sind hnswlib, Googles ScaNN und Microsofts DiskANN (Douze et al., 2024).

### Typische Verwendung

```python
import faiss, numpy as np

d = 768
xb = np.random.rand(100_000, d).astype("float32")   # Datenbankvektoren
xq = np.random.rand(5, d).astype("float32")          # Anfragen

index = faiss.index_factory(d, "IVF1024,PQ64")      # IVF mit 1024 Listen, PQ mit 64 Teilvektoren
index.train(xb)                                      # k-Means für Zentroide und PQ-Codebücher
index.add(xb)
index.nprobe = 16                                    # zu durchsuchende Listen: Geschwindigkeit vs. Genauigkeit
distances, ids = index.search(xq, 10)
```

| Factory-String | Index | Einsatz |
|---|---|---|
| `Flat` | exakte Suche | kleine Sammlungen, Referenzergebnis |
| `HNSW32` | Graph mit 32 Kanten je Knoten | schnelle Suche im Arbeitsspeicher |
| `IVF4096,Flat` | Inverted File, unkomprimiert | große Sammlungen, exakte Distanzen innerhalb der Listen |
| `IVF4096,PQ64` | Inverted File mit Product Quantization | sehr große Sammlungen, wenig Speicher |
| `PCA160,IVF20000_HNSW,PQ20x10,RFlat` | PCA, HNSW-Grobquantisierer, PQ, exaktes Neuordnen | Milliardenmaßstab mit Verfeinerung |

Quellen: Douze et al. (2024); der Code ist ein Beispiel zur Veranschaulichung.

### Wann einsetzen

- Ähnlichkeitssuche über Millionen bis Milliarden Embeddings innerhalb einer Anwendung, ohne eigenen Datenbankserver (Douze et al., 2024).
- Retrieval für RAG und Open-Domain-Fragebeantwortung, bei dem der Passagenindex offline gebaut wird ([[dense-passage-retrieval|DPR]], [[retrieval-augmented-generation|RAG]]).
- [[clustering|Clustering]], Deduplizierung und Data Mining auf großen Datensätzen, etwa das Entfernen von Duplikaten aus 1,3 Milliarden Bildern oder das Gewinnen zweisprachiger Texte (Douze et al., 2024).

### Stärken und Grenzen

**Stärken**
- Viele Indexarten und Kompressionsverfahren in einer Bibliothek, auf CPU und GPU (Douze et al., 2024).
- Skaliert von Tausenden bis Billionen Vektoren; ein Einsatz indexierte 1,5 Billionen 144-dimensionale Vektoren bei etwa 1 Sekunde je Anfrage (Douze et al., 2024).
- Schnelle GPU-Implementierungen (Johnson et al., 2017).

**Grenzen**
- Eine Bibliothek, keine Datenbank: Speicherung, Filter auf Metadaten, Zugriffskontrolle und Replikation müssen darum herum ergänzt werden ([[vector-databases|Vektordatenbanken]]).
- Die Wahl von Index und Parametern erfordert, den Zielkonflikt aus Genauigkeit, Geschwindigkeit und Speicher auf den Zieldaten zu messen (Douze et al., 2024).
- Komprimierte Indizes liefern approximative Distanzen und verlieren etwas Genauigkeit (Douze et al., 2024).

### Vergleich

| | FAISS | [[vector-databases\|Vektordatenbank]] |
|---|---|---|
| Art | Bibliothek mit vielen Indexarten ([[hnsw\|HNSW]], IVF, PQ, …) | Server mit Speicherung und APIs |
| Kompression | PQ, Skalar-, additive Quantisierer | je nach Produkt |
| GPU | ja | je nach Produkt |
| Metadaten, Filter, Persistenz | muss die Anwendung ergänzen | eingebaut |

Quellen: Douze et al. (2024); Johnson et al. (2017).

### In der Praxis

Üblich ist, auf einer Stichprobe einen exakten `Flat`-Index als Referenz zu bauen und dann Kandidatenindizes nach [[classification-metrics|Recall]] und Anfragezeit auf dieser Stichprobe zu vergleichen, bevor einer gewählt wird (Douze et al., 2024). Suche per Skalarprodukt auf normalisierten Vektoren ergibt Cosine Similarity, eine verbreitete Metrik für Text-[[embeddings|Embeddings]] (Douze et al., 2024).

### Merksatz

FAISS ist Metas Open-Source-Werkzeugkasten für Vektorsuche, der exakte Suche, Inverted Files, Graphindizes und Product Quantization auf CPU und GPU verbindet und Genauigkeit, Geschwindigkeit und Speicher für Sammlungen von Tausenden bis Billionen Vektoren abwägen lässt.

### Quellen

- Douze, M., Guzhva, A., Deng, C., Johnson, J., Szilvasy, G., Mazaré, P.-E., Lomeli, M., Hosseini, L. & Jégou, H. (2024). *The Faiss library.* arXiv:2401.08281. [arXiv:2401.08281](https://arxiv.org/abs/2401.08281)
- Johnson, J., Douze, M. & Jégou, H. (2017). *Billion-scale similarity search with GPUs.* arXiv:1702.08734. [arXiv:1702.08734](https://arxiv.org/abs/1702.08734)
