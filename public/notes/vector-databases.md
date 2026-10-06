---
title_en: Vector Databases
title_de: Vektordatenbanken
entity_type: Concept
sources:
- https://arxiv.org/abs/1603.09320
- https://arxiv.org/abs/1702.08734
- https://arxiv.org/abs/2310.14021
- https://arxiv.org/abs/1908.10396
- https://doi.org/10.1109/TPAMI.2010.57
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Vector databases provide scalable approximate nearest neighbor search for high-dimensional vector embeddings, solving the high computational cost of exact search in large datasets. This capability is essential for efficient [[retrieval-augmented-generation|Retrieval-Augmented Generation]] systems requiring fast similarity retrieval over vast unstructured data stores.

### How it works

Vector databases implement approximate nearest neighbor search through hierarchical graph construction for efficient navigation (HNSW) (Malkov & Yashunin, 2016), inverted-file partitioning with GPU acceleration (FAISS) (Johnson et al., 2017), vector compression via product quantization (PQ) (Jégou et al., 2011), and anisotropic quantization for inner product search (Guo et al., 2019), supporting metadata filtering for context-aware retrieval.

```text
vectors + metadata
 ▼
index: graph (HNSW) | inverted file (IVF) | flat
       optionally with compressed codes (PQ, anisotropic quantization)
 ▼
query vector (+ metadata filter)
 ▼
approximate nearest-neighbour search ─▶ top-k ids, scores, metadata
```

#### 1. Hierarchical Graph Construction (HNSW)

Hierarchical Graph Construction in HNSW incrementally builds a multi-layer graph where each layer `l` (starting from 0) represents a proximity graph over a nested subset of the stored vectors. The maximum layer for a vector is selected randomly with an exponentially decaying probability distribution proportional to `p^l` (where `0 < p < 1`), as established in Malkov & Yashunin (2016). This ensures higher layers contain fewer, more widely distributed vectors, creating scale separation in link distances. The search algorithm initiates at the highest layer and navigates downward, leveraging the hierarchical structure to achieve logarithmic query complexity relative to the dataset size. This design significantly improves search speed and recall, especially for clustered data, by reducing the number of distance computations compared to single-layer approaches. Trade-offs include increased memory overhead for the layered structure and more complex index construction, though these are offset by superior query performance. Graph connections are defined by the same distance or similarity measure as the search (see [[embeddings|Embeddings]]), and Malkov & Yashunin (2016) note that the approach needs no additional search structures, which other proximity-graph methods use for the coarse search stage.

#### 2. Hierarchical Navigation for Query Processing (HNSW)

HNSW (Hierarchical Navigable Small World) processes queries using a multi-layer proximity graph index. The index consists of nested layers, where each layer contains a subset of data points; the top layer has the fewest points, and lower layers contain progressively more points. Query processing begins at the top layer, identifying the nearest neighbor to the query vector. It then descends greedily to lower layers, starting from the current node and selecting the closest neighbor in the new layer (based on a heuristic prioritizing high similarity), continuing until the bottom layer is reached. This greedy navigation, combined with the heuristic neighbor selection (which improves recall in clustered data), ensures efficient search. The hierarchical structure with scale separation enables search effort to scale roughly logarithmically with dataset size, as shown by Malkov & Yashunin (2016). Inputs are a query vector and the HNSW index; outputs are the k approximate nearest neighbors. Design choices include the exponentially decaying probability for layer assignment (to balance layer density) and the absence of auxiliary search structures, trading higher storage for logarithmic query complexity. This contrasts with non-hierarchical methods like NSW, which lack the layered optimization.

#### 3. Inverted-File Partitioning and GPU Search (FAISS)

Inverted-file partitioning (IVF) clusters the vector space using a coarse quantizer, such as k-means, which partitions vectors into centroids. Each vector is assigned to a centroid (code), and vectors are grouped into inverted lists per centroid. During a query, the coarse quantizer identifies the relevant cluster(s), reducing the search space to only a few lists. The vectors inside the lists can additionally be stored as compressed codes (product quantization, see below), which is known as IVF-PQ. Johnson et al. (2017) proposed a GPU design for k-selection that runs at up to 55% of theoretical peak performance, making nearest-neighbour search 8.5x faster than the prior GPU state of the art, with optimized brute-force, approximate and compressed-domain search; with it, a k-NN graph connecting 1 billion vectors was built in less than 12 hours on 4 GPUs. Their implementation is the FAISS library. The design trades recall reduction (due to cluster pruning) for significant speed and storage gains, making it suitable for large-scale applications like [[retrieval-augmented-generation|Retrieval-Augmented Generation]].

#### 4. Vector Compression via Product Quantization (PQ)

Product Quantization (PQ) compresses high-dimensional vectors by partitioning each vector into M non-overlapping sub-vectors. For each sub-vector, a small codebook (a set of centroids learned via k-means clustering) is created. Each sub-vector is then represented by a code (an index into its codebook), reducing storage from floating-point values to small integers. The input is a set of high-dimensional vectors; the output comprises compact codes for each vector and the associated codebooks. Distance estimation between vectors is computed as the sum of precomputed distances between corresponding sub-vector codes (using centroid distances), avoiding full vector distance calculations during search. Key design choices include the number of sub-vectors M and the codebook size per sub-vector. Increasing M or codebook size improves distance accuracy but raises codebook storage requirements. PQ, introduced by Jégou et al. (2011), enables efficient approximate nearest neighbor search in large vector databases by balancing compression ratio and search precision, a critical component for scalable [[retrieval-augmented-generation|Retrieval-Augmented Generation]] systems.

#### 5. Anisotropic Quantization for Inner Product Search

Anisotropic quantization for maximum inner product search (MIPS) modifies the quantization loss: instead of minimizing the total reconstruction error of the database points, it penalizes the component of a datapoint's residual that is parallel to the datapoint more heavily than the orthogonal component. The motivation is that, for a given query, the database points with the largest inner products matter most for the result. The loss function weights the parallel residual error more strongly, leading to quantized representations that better preserve inner product structure. Inputs are high-dimensional database vectors and a query vector; outputs are compact quantized codes enabling efficient MIPS. The loss is derived under natural statistical assumptions about the data and does not increase the code size. Guo et al. (2019) report state-of-the-art results on the public ann-benchmarks; the method is implemented in Google's ScaNN library.

#### 6. Metadata Filtering

Metadata filtering applies structured criteria to vector search results. Pre-filtering restricts the candidate set to vectors matching metadata conditions before similarity search, typically using secondary indexes (e.g., B-trees for key-value or range queries) on metadata fields. This reduces the number of vectors processed, improving search speed but risking reduced recall if filters exclude relevant vectors. Post-filtering applies metadata conditions to the top-k results from full vector search, preserving the vector search's recall but potentially reducing the final result count below k. The candidate set size for pre-filtering is the intersection of metadata and vector proximity; for post-filtering, it is the top-k vector results after metadata filtering. Design trade-offs involve balancing query efficiency (pre-filtering) against recall preservation (post-filtering), with pre-filtering preferred for large datasets and high filter specificity, while post-filtering offers simpler implementation but higher computational cost for the vector search phase. [[rag-retrieval|Retrieval]] and [[rag-evaluation|Evaluation]] metrics must account for the filtering method's impact on result quality.

#### Origin and variants

Vector database management systems (VDBMSs) evolved from similarity search libraries (e.g., FAISS) that provided indexing structures but lacked full database features like metadata management, CRUD operations, and scalable persistence. Pan et al. (2023) count over 20 commercial VDBMSs, all produced within the past five years, driven by data-intensive applications, notably large language models. Inputs are high-dimensional vectors (e.g., embeddings) and metadata; outputs are top-k similar vectors with metadata filtering. Key index structures include HNSW (Hierarchical Navigable Small World), a hierarchical graph enabling logarithmic search complexity (Malkov & Yashunin, 2016), IVF (Inverted File Index), which partitions vectors into clusters to reduce search space, and PQ (Product Quantization), which compresses vectors via sub-vector quantization for memory efficiency (Jégou et al., 2011). Systems combine these building blocks, for example IVF with PQ for very large collections, or graph indexes such as HNSW with compressed vectors to reduce memory. Design trade-offs involve HNSW’s high recall and memory cost versus IVF’s speed at potential recall loss, and PQ’s storage savings versus precision degradation. These combinations balance speed, recall, and storage for production systems.

### When to use it

- When exact search over all vectors becomes too slow for the latency budget, typically from hundreds of thousands to millions of vectors upwards.
- For high-recall similarity search requiring logarithmic query complexity (Malkov & Yashunin (2016) show HNSW achieves logarithmic scaling).
- For [[retrieval-augmented-generation|Retrieval-Augmented Generation]] systems that need filtering, updates and persistence in addition to search; large language models are a main driver of vector databases (Pan et al., 2023).

### Strengths and limitations

**Strengths**
- HNSW achieves logarithmic complexity scaling for approximate nearest neighbor search (Malkov & Yashunin (2016)).
- GPU-based implementations achieve up to 8.5x speedup over prior GPU approaches for similarity search (Johnson et al. (2017)).
- Product quantization enables efficient approximate search with reduced memory footprint (Jégou et al. (2011)).

**Limitations**
- Approximate nearest neighbor search trades recall for speed; the recall of the index has to be measured and tuned.
- Quantization approximates the vectors and therefore the distances, which can lower retrieval accuracy.
- Hybrid queries that combine attribute filters and vector similarity are hard to answer efficiently, one of the five main obstacles named by Pan et al. (2023).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Vector Database | Integrates scalable approximate nearest neighbor search (e.g., HNSW, IVF) with full database features (CRUD, metadata management, scalability). | Large-scale production RAG systems requiring persistent storage, updates, metadata filtering, and multi-tenancy (Pan et al. 2023). |
| Exact search | Uses brute-force distance computation for exact matches, scaling linearly with dataset size (O(n) per query). | Small datasets (e.g., <10,000 vectors) where exact recall is critical. |
| Vector index library (e.g., FAISS) | Provides indexing and search capabilities but lacks integrated database management (e.g., no persistent storage, no metadata filtering). | Prototyping, small-scale applications, or as a component within a custom application (e.g., [[rag-chunking|chunking]] pipelines). |

Vector databases become necessary when scalability and metadata management are required for production systems, unlike exact search for small-scale use cases or index libraries for simple indexing.

### In practice

Evaluation compares the recall of the approximate index against exact search together with latency and memory; ann-benchmarks is a public benchmark for this, and retrieval quality for the application is measured separately, see [[rag-retrieval-evaluation|retrieval evaluation]]. Typical failure modes include using unnormalized embeddings with cosine similarity (distorting ranking) and selecting top-k values exceeding context window limits (increasing token costs). Key HNSW parameters are the number of connections per node and the size of the candidate lists during construction and search (Malkov & Yashunin 2016), while product quantization requires sub-vector count and codebook size (Jégou et al. 2011).

### Key takeaway

Vector databases employ approximate nearest neighbor (ANN) search for high-dimensional [[embeddings|Embeddings]], trading retrieval accuracy for speed and scalability.

### Sources

- Malkov, Y. A. & Yashunin, D. A. (2016). *Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs.* [arXiv:1603.09320](https://arxiv.org/abs/1603.09320)
- Johnson, J. et al. (2017). *Billion-scale similarity search with GPUs.* [arXiv:1702.08734](https://arxiv.org/abs/1702.08734)
- Pan, J. J. et al. (2023). *Survey of Vector Database Management Systems.* [arXiv:2310.14021](https://arxiv.org/abs/2310.14021)
- Guo, R. et al. (2019). *Accelerating Large-Scale Inference with Anisotropic Vector Quantization.* [arXiv:1908.10396](https://arxiv.org/abs/1908.10396)
- Jégou, H., Douze, M. & Schmid, C. (2011). *Product Quantization for Nearest Neighbor Search.* IEEE Transactions on Pattern Analysis and Machine Intelligence 33(1). [doi:10.1109/TPAMI.2010.57](https://doi.org/10.1109/TPAMI.2010.57)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Vektordatenbanken bieten skalierbare Approximate Nearest Neighbor Suche für hochdimensionale Vektorembbeddings, wodurch der hohe rechnerische Aufwand für exakte Suche in großen Datensätzen gelöst wird. Diese Fähigkeit ist für effiziente [[retrieval-augmented-generation|Retrieval-Augmented Generation]]-Systeme entscheidend, die eine schnelle Ähnlichkeitsrecherche über umfangreiche unstrukturierte Datenspeicher erfordern.

### Funktionsweise

Vektordatenbanken implementieren Approximate Nearest Neighbor Search durch hierarchische Graphenkonstruktion für effiziente Navigation (HNSW) (Malkov & Yashunin, 2016), inverted-file-Partitionierung mit GPU-Beschleunigung (FAISS) (Johnson et al., 2017), Vektorkompression über Product Quantization (PQ) (Jégou et al., 2011) und anisotrope Quantisierung für Inneprodukt-Suche (Guo et al., 2019), wobei Metadaten-Filterung für kontextbewusste Retrieval unterstützt wird.

```text
Vektoren + Metadaten
 ▼
Index: Graph (HNSW) | Inverted File (IVF) | Flat
       optional mit komprimierten Codes (PQ, anisotrope Quantisierung)
 ▼
Abfragevektor (+ Metadaten-Filter)
 ▼
Approximate Nearest-Neighbor-Suche ─▶ top-k IDs, Scores, Metadaten
```

#### 1. Hierarchische Graphenkonstruktion (HNSW)

Die hierarchische Graphenkonstruktion in HNSW baut schrittweise einen mehrschichtigen Graphen auf, wobei jeder Schicht `l` (beginnend mit 0) ein Proximity-Graph über einer verschachtelten Teilmenge der gespeicherten Vektoren entspricht. Die maximale Schicht für einen Vektor wird zufällig mit einer exponentiell abnehmenden Wahrscheinlichkeitsverteilung ausgewählt, die proportional zu `p^l` (wobei `0 < p < 1`) ist, wie in Malkov & Yashunin (2016) festgelegt. Dies stellt sicher, dass höhere Schichten weniger, aber weit verteilter Vektoren enthalten, was eine Skalierungstrennung in den Verknüpfungsdistanzen erzeugt. Der Suchalgorithmus beginnt in der höchsten Schicht und navigiert nach unten, wobei er die hierarchische Struktur nutzt, um eine logarithmische Abfragekomplexität in Beziehung zum Datensatzumfang zu erreichen. Dieses Design verbessert die Suchgeschwindigkeit und den Recall erheblich, insbesondere bei gruppierten Daten, indem es im Vergleich zu Einzelschichtansätzen die Anzahl der Distanzberechnungen reduziert. Kompromisse umfassen einen erhöhten Speicherbedarf für die Schichtstruktur und eine komplexere Indexkonstruktion, wobei diese durch die überlegene Abfrageleistung ausgeglichen werden. Die Graphenverknüpfungen werden durch denselben Abstand oder Ähnlichkeitsmaßstab definiert wie die Suche (siehe [[embeddings|Embeddings]]), und Malkov & Yashunin (2016) weisen darauf hin, dass der Ansatz keine zusätzlichen Suchstrukturen benötigt, die andere Proximity-Graph-Methoden für die grobe Suchphase verwenden.

#### 2. Hierarchische Navigation für die Abfrageverarbeitung (HNSW)

HNSW (Hierarchical Navigable Small World) verarbeitet Abfragen mithilfe eines mehrschichtigen Proximitätsgraphen-Index. Der Index besteht aus ineinander verschachtelten Schichten, wobei jede Schicht eine Teilmenge der Datenpunkte enthält; die oberste Schicht enthält die wenigsten Punkte, und untergeordnete Schichten enthalten zunehmend mehr Punkte. Die Abfrageverarbeitung beginnt in der obersten Schicht, wobei der nächstgelegene Nachbar zum Abfragevektor identifiziert wird. Danach wird gierig in untere Schichten abgestiegen, beginnend vom aktuellen Knoten und indem der nächste Nachbar in der neuen Schicht ausgewählt wird (basierend auf einer Heuristik, die hohe Ähnlichkeit priorisiert), bis die unterste Schicht erreicht ist. Diese gierige Navigation, kombiniert mit der Heuristik für die Nachbarschaftsauswahl (die die Erinnerung bei gruppierten Daten verbessert), gewährleistet eine effiziente Suche. Die hierarchische Struktur mit Skalierungstrennung ermöglicht es, den Suchaufwand ungefähr logarithmisch mit der Größe der Datensammlung skalieren zu lassen, wie Malkov & Yashunin (2016) zeigen. Die Eingaben sind ein Abfragevektor und der HNSW-Index; die Ausgaben sind die k ungefähren nächsten Nachbarn. Designentscheidungen umfassen die exponentiell abnehmende Wahrscheinlichkeit für die Schichtzuordnung (um die Schichtdichte auszugleichen) und das Fehlen von Hilfssuchstrukturen, wodurch höherer Speicherbedarf gegen logarithmische Abfragekomplexität getauscht wird. Dies unterscheidet sich von nicht-hierarchischen Methoden wie NSW, die die geschichtete Optimierung nicht besitzen.

#### 3. Invertierte-Datei-Partitionierung und GPU-Suche (FAISS)

Die invertierte-Datei-Partitionierung (IVF) gruppiert den Vektorraum mithilfe eines groben Quantisierers, wie z. B. k-means, der die Vektoren in Zentroiden unterteilt. Jeder Vektor wird einem Zentroid (Code) zugewiesen, und die Vektoren werden in invertierte Listen pro Zentroid gruppiert. Während einer Abfrage identifiziert der grobe Quantisierer die relevanten Cluster(s), wodurch der Suchraum auf nur wenige Listen reduziert wird. Die Vektoren innerhalb der Listen können zusätzlich als komprimierte Codes gespeichert werden (Produkt-Quantisierung, siehe unten), was als IVF-PQ bekannt ist. Johnson et al. (2017) schlugen ein GPU-Design für k-Auswahl vor, das bis zu 55 % der theoretischen Spitzenleistung erreicht, wodurch die Suche nach nächsten Nachbarn 8,5-mal schneller als der vorherige GPU-Zustand der Technik ist, mit optimiertem Brute-Force-, approximiertem und komprimiertendomänenbasiertem Suchverfahren; mit diesem Verfahren wurde ein k-NN-Graph, der 1 Milliarde Vektoren verbindet, in weniger als 12 Stunden auf 4 GPUs erstellt. Ihre Implementierung ist die FAISS-Bibliothek. Das Design tauscht eine Verringerung der Erinnerung (aufgrund der Cluster-Pruning) gegen erhebliche Geschwindigkeits- und Speicherungsgewinne, wodurch es für großskalige Anwendungen wie [[retrieval-augmented-generation|Retrieval-Augmented Generation]] geeignet ist.

#### 4. Vektorkompression über Product Quantization (PQ)

Product Quantization (PQ) komprimiert hochdimensionale Vektoren, indem jeder Vektor in M nicht überlappende Untervektoren unterteilt wird. Für jeden Untervektor wird ein kleiner Codebuch (ein Satz von Zentroiden, die über das k-means-Clustering gelernt wurden) erstellt. Jeder Untervektor wird anschließend durch einen Code (einen Index in seinem Codebuch) dargestellt, wodurch der Speicherbedarf von Gleitkommawerten auf kleine ganze Zahlen reduziert wird. Die Eingabe besteht aus einem Satz hochdimensionaler Vektoren; die Ausgabe umfasst kompakte Codes für jeden Vektor und die zugehörigen Codebücher. Die Distanzberechnung zwischen Vektoren wird als Summe der vorberechneten Distanzen zwischen den entsprechenden Untervektor-Codes berechnet (mithilfe der Zentroiden-Distanzen), wodurch vollständige Vektor-Distanzberechnungen während der Suche vermieden werden. Wichtige Gestaltungswahlmöglichkeiten umfassen die Anzahl der Untervektoren M und die Größe des Codebuchs pro Untervektor. Eine Erhöhung von M oder der Codebuchgröße verbessert die Distanzgenauigkeit, erhöht aber auch die Speicheranforderungen für das Codebuch. PQ, eingeführt von Jégou et al. (2011), ermöglicht effiziente Approximate Nearest Neighbor Suche in großen Vektordatenbanken, indem der Komprimierungsgrad und die Suchgenauigkeit ausgewogen werden, ein entscheidender Bestandteil für skalierbare [[retrieval-augmented-generation|Retrieval-Augmented Generation]]-Systeme.

#### 5. Anisotropische Quantisierung für die Suche nach dem inneren Produkt

Die anisotropische Quantisierung für die Suche nach dem maximalen inneren Produkt (MIPS) modifiziert die Quantisierungsverlustfunktion: Anstatt die Gesamtrekonstruktionsfehler der Datenbankpunkte zu minimieren, bestraft sie den Komponententeil des Residuums eines Datensatzpunkts, der parallel zum Datensatzpunkt liegt, stärker als den orthogonalen Komponententeil. Die Motivation besteht darin, dass für eine gegebene Abfrage die Datenbankpunkte mit den größten inneren Produkten am meisten für das Ergebnis entscheiden. Die Verlustfunktion gewichtet den parallelen Residuumsfehler stärker, was zu quantisierten Darstellungen führt, die besser die Struktur des inneren Produkts bewahren. Eingaben sind hochdimensionale Datenbankvektoren und ein Abfragevektor; Ausgaben sind kompakte quantisierte Codes, die eine effiziente MIPS ermöglichen. Der Verlust wird unter natürlichen statistischen Annahmen über die Daten abgeleitet und erhöht nicht die Codesgröße. Guo et al. (2019) berichten über state-of-the-art-Ergebnisse auf den öffentlichen ann-benchmarks; die Methode wird in Googles ScaNN-Bibliothek implementiert.

#### 6. Metadaten-Filterung

Die Metadaten-Filterung wendet strukturierte Kriterien auf die Ergebnisse der Vektorsuche an. Die Vorab-Filterung beschränkt die Kandidatenmenge auf Vektoren, die den Metadatenbedingungen entsprechen, bevor die Ähnlichkeitssuche durchgeführt wird. Dazu werden typischerweise sekundäre Indizes (z. B. B-Bäume für Schlüssel-Wert- oder Bereichsabfragen) auf Metadatenfelder verwendet. Dies reduziert die Anzahl der verarbeiteten Vektoren und verbessert die Suchgeschwindigkeit, birgt jedoch das Risiko einer verringerten Recall, wenn Filter relevante Vektoren ausschließen. Die Nach-Filterung wendet Metadatenbedingungen auf die Top-k-Ergebnisse der vollständigen Vektorsuche an, wodurch die Recall der Vektorsuche erhalten bleibt, aber die Anzahl der endgültigen Ergebnisse unter k fallen kann. Die Größe der Kandidatenmenge bei der Vorab-Filterung ist der Schnittmengen von Metadaten und Vektor-Nähe; bei der Nach-Filterung ist sie die Top-k-Vektorergebnisse nach der Metadaten-Filterung. Die Gestaltungskompromisse bestehen darin, die Abfrageeffizienz (Vorab-Filterung) mit der Erhaltung der Recall (Nach-Filterung) abzuwägen. Vorab-Filterung wird bei großen Datensätzen und hoher Filterpräzision bevorzugt, während Nach-Filterung eine einfachere Implementierung bietet, aber einen höheren Rechenaufwand für die Vektorsuchphase verursacht. [[rag-retrieval|Retrieval]] und [[rag-evaluation|Evaluation]]-Metriken müssen den Einfluss der Filtermethode auf die Ergebnisqualität berücksichtigen.

#### Ursprung und Varianten

Vektor-Datenbank-Managementsysteme (VDBMS) entwickelten sich aus Ähnlichkeits-Such-Bibliotheken (z. B. FAISS), die Indizierungsstrukturen bereitstellten, aber keine vollständigen Datenbankfunktionen wie Metadaten-Management, CRUD-Operationen oder skalierbare Persistenz besaßen. Pan et al. (2023) zählen über 20 kommerzielle VDBMS, alle innerhalb der letzten fünf Jahre entwickelt, getrieben durch datenintensive Anwendungen, insbesondere große Sprachmodelle. Eingaben sind hochdimensionale Vektoren (z. B. Embeddings) und Metadaten; Ausgaben sind die top-k ähnlichen Vektoren mit Metadaten-Filterung. Wichtige Indizierungsstrukturen umfassen HNSW (Hierarchical Navigable Small World), einen hierarchischen Graphen, der eine logarithmische Suchkomplexität ermöglicht (Malkov & Yashunin, 2016), IVF (Inverted File Index), der Vektoren in Cluster unterteilt, um den Suchraum zu reduzieren, und PQ (Product Quantization), der Vektoren durch Sub-Vektor-Quantisierung komprimiert, um die Speichereffizienz zu verbessern (Jégou et al., 2011). Systeme kombinieren diese Bausteine, beispielsweise IVF mit PQ für sehr große Sammlungen oder Graph-Indizes wie HNSW mit komprimierten Vektoren, um den Speicherbedarf zu reduzieren. Design-Kompromisse beinhalten den hohen Recall und den hohen Speicherbedarf von HNSW im Vergleich zur Geschwindigkeit von IVF bei möglicher Recall-Verlust, und den Speicherbedarfseinsparungen von PQ im Vergleich zur Präzisionsverringerung. Diese Kombinationen balancieren Geschwindigkeit, Recall und Speicherbedarf für Produktionsumgebungen.

### Wann einsetzen

- Wenn die exakte Suche über alle Vektoren aufgrund der Latenzbudgets zu langsam wird, typischerweise ab Hunderttausenden bis Millionen von Vektoren.
- Für hochgenaue Ähnlichkeitsuche mit logarithmischer Abfrageskomplexität (Malkov & Yashunin (2016) zeigen, dass HNSW logarithmische Skalierung erreicht).
- Für [[retrieval-augmented-generation|Retrieval-Augmented Generation]-Systeme, die neben der Suche auch Filterung, Updates und Persistenz benötigen; große Sprachmodelle sind ein Haupttreiber für Vektordatenbanken (Pan et al., 2023).

### Stärken und Grenzen

**Stärken**
- HNSW erreicht eine logarithmische Komplexitätsskalierung für die Approximate Nearest Neighbor Suche (Malkov & Yashunin (2016)).
- GPU-basierte Implementierungen erzielen bis zu 8,5-fache Geschwindigkeitssteigerung gegenüber früheren GPU-Ansätzen bei der Ähnlichkeitssuche (Johnson et al. (2017)).
- Product Quantization ermöglicht effiziente approximierte Suche mit reduziertem Speicherbedarf (Jégou et al. (2011)).

**Einschränkungen**
- Die Approximate Nearest Neighbor Suche tauscht Recall gegen Geschwindigkeit; der Recall des Index muss gemessen und eingestellt werden.
- Quantisierung approximiert die Vektoren und damit auch die Distanzen, was die Retrievalgenauigkeit verringern kann.
- Hybridabfragen, die Attributfilter und Vektorsimilarität kombinieren, sind schwer effizient zu beantworten; eine der fünf Haupthindernisse, die Pan et al. (2023) nennen.

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Vektordatenbank | Integriert skalierbare Approximate Nearest Neighbor Suche (z. B. HNSW, IVF) mit vollständigen Datenbankfunktionen (CRUD, Metadatenverwaltung, Skalierbarkeit). | Große Produktions-RAG-Systeme, die persistente Speicherung, Updates, Metadatenfilterung und Multi-Tenancy erfordern (Pan et al. 2023). |
| Exakte Suche | Verwendet brute-force Distanzberechnung für exakte Übereinstimmungen, skaliert linear mit der Datengröße (O(n) pro Abfrage). | Kleine Datensätze (z. B. <10.000 Vektoren), bei denen exakte Recall kritisch ist. |
| Vektordatenbankbibliothek (z. B. FAISS) | Bietet Indexierung und Suchfunktionen, verfügt aber nicht über integrierte Datenbankverwaltung (z. B. keine persistente Speicherung, keine Metadatenfilterung). | Prototypen, kleine Anwendungen oder als Komponente innerhalb einer benutzerdefinierten Anwendung (z. B. [[rag-chunking|Chunking]]-Pipelines). |

Vektordatenbanken werden erforderlich, wenn Skalierbarkeit und Metadatenverwaltung für Produktionsysteme benötigt werden, im Gegensatz zur exakten Suche für kleine Anwendungsfälle oder Indexbibliotheken für einfache Indexierung.

### In der Praxis

Die Evaluation vergleicht die Recall des ungefähren Index mit der exakten Suche zusammen mit Latenz und Speicher; ann-benchmarks ist ein öffentliches Benchmarking für dies, und die Retrieval-Qualität für die Anwendung wird separat gemessen, siehe [[rag-retrieval-evaluation|Retrieval-Evaluation]]. Typische Fehlmodi umfassen die Verwendung von nicht normalisierten Embeddings mit Cosinus-Ähnlichkeit (Verzerrung der Rangliste) und das Auswählen von top-k-Werten, die die Grenzen des Kontextfensters überschreiten (Erhöhung der Tokenkosten). Schlüsselparameter von HNSW sind die Anzahl der Verbindungen pro Knoten und die Größe der Kandidatenlisten während der Konstruktion und Suche (Malkov & Yashunin 2016), während Product Quantization die Anzahl der Untervektoren und die Größe des Codebooks erfordert (Jégou et al. 2011).

### Merksatz

Vektordatenbanken verwenden Approximate Nearest Neighbor (ANN)-Suche für hochdimensionale [[embeddings|Embeddings]], wobei Genauigkeit bei der Retrieval gegen Geschwindigkeit und Skalierbarkeit getauscht wird.

### Quellen

- Malkov, Y. A. & Yashunin, D. A. (2016). *Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs.* [arXiv:1603.09320](https://arxiv.org/abs/1603.09320)
- Johnson, J. et al. (2017). *Billion-scale similarity search with GPUs.* [arXiv:1702.08734](https://arxiv.org/abs/1702.08734)
- Pan, J. J. et al. (2023). *Survey of Vector Database Management Systems.* [arXiv:2310.14021](https://arxiv.org/abs/2310.14021)
- Guo, R. et al. (2019). *Accelerating Large-Scale Inference with Anisotropic Vector Quantization.* [arXiv:1908.10396](https://arxiv.org/abs/1908.10396)
- Jégou, H., Douze, M. & Schmid, C. (2011). *Product Quantization for Nearest Neighbor Search.* IEEE Transactions on Pattern Analysis and Machine Intelligence 33(1). [doi:10.1109/TPAMI.2010.57](https://doi.org/10.1109/TPAMI.2010.57)
