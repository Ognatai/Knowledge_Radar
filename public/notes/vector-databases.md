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
Hierarchical Graph Construction (HNSW)
▼
Hierarchical Navigation for Query Processing (HNSW)
▼
Inverted-File Partitioning and GPU Search (FAISS)
▼
Vector Compression via Product Quantization (PQ)
▼
Anisotropic Quantization for Inner Product Search
▼
Metadata Filtering, Origin and variants
```

#### 1. Hierarchical Graph Construction (HNSW)

Hierarchical Graph Construction in HNSW incrementally builds a multi-layer graph where each layer `l` (starting from 0) represents a proximity graph over a nested subset of the stored vectors. The maximum layer for a vector is selected randomly with an exponentially decaying probability distribution proportional to `p^l` (where `0 < p < 1`), as established in Malkov & Yashunin (2016). This ensures higher layers contain fewer, more widely distributed vectors, creating scale separation in link distances. The search algorithm initiates at the highest layer and navigates downward, leveraging the hierarchical structure to achieve logarithmic query complexity relative to the dataset size. This design significantly improves search speed and recall, especially for clustered data, by reducing the number of distance computations compared to single-layer approaches. Trade-offs include increased memory overhead for the layered structure and more complex index construction, though these are offset by superior query performance. The method relies on proximity metrics like [[embeddings|Similarity-Metriken]] to define graph connections, avoiding the need for auxiliary search structures.

#### 2. Hierarchical Navigation for Query Processing (HNSW)

HNSW (Hierarchical Navigable Small World) processes queries using a multi-layer proximity graph index. The index consists of nested layers, where each layer contains a subset of data points; the top layer has the fewest points, and lower layers contain progressively more points. Query processing begins at the top layer, identifying the nearest neighbor to the query vector. It then descends greedily to lower layers, starting from the current node and selecting the closest neighbor in the new layer (based on a heuristic prioritizing high similarity), continuing until the bottom layer is reached. This greedy navigation, combined with the heuristic neighbor selection (which improves recall in clustered data), ensures efficient search. The hierarchical structure with scale separation enables search effort to scale roughly logarithmically with dataset size, as shown by Malkov & Yashunin (2016). Inputs are a query vector and the HNSW index; outputs are the k approximate nearest neighbors. Design choices include the exponentially decaying probability for layer assignment (to balance layer density) and the absence of auxiliary search structures, trading higher storage for logarithmic query complexity. This contrasts with non-hierarchical methods like NSW, which lack the layered optimization.

#### 3. Inverted-File Partitioning and GPU Search (FAISS)

Inverted-file partitioning (IVF) clusters the vector space using a coarse quantizer, such as k-means, which partitions vectors into centroids. Each vector is assigned to a centroid (code), and vectors are grouped into inverted lists per centroid. During a query, the coarse quantizer identifies the relevant cluster(s), reducing the search space to only a few lists. This is combined with compressed codes (e.g., product quantization), where vectors are split into sub-vectors and quantized into compact codes. Search operates in three modes: brute-force (exact comparison within the selected lists), approximate (distance estimation from compressed codes), and compressed-domain (direct distance computation from codes without decompression). Johnson et al. (2017) introduced GPU-optimized k-selection achieving 55% of theoretical peak performance, enabling 8.5x faster search than prior GPU methods and supporting billion-scale indexing (e.g., 1 billion vectors in <12 hours on 4 GPUs). The design trades recall reduction (due to cluster pruning) for significant speed and storage gains, making it suitable for large-scale applications like [[retrieval-augmented-generation|Retrieval-Augmented Generation]].

#### 4. Vector Compression via Product Quantization (PQ)

Product Quantization (PQ) compresses high-dimensional vectors by partitioning each vector into M non-overlapping sub-vectors. For each sub-vector, a small codebook (a set of centroids learned via k-means clustering) is created. Each sub-vector is then represented by a code (an index into its codebook), reducing storage from floating-point values to small integers. The input is a set of high-dimensional vectors; the output comprises compact codes for each vector and the associated codebooks. Distance estimation between vectors is computed as the sum of precomputed distances between corresponding sub-vector codes (using centroid distances), avoiding full vector distance calculations during search. Key design choices include the number of sub-vectors M and the codebook size per sub-vector. Increasing M or codebook size improves distance accuracy but raises codebook storage requirements. PQ, introduced by Jégou et al. (2011), enables efficient approximate nearest neighbor search in large vector databases by balancing compression ratio and search precision, a critical component for scalable [[retrieval-augmented-generation|Retrieval-Augmented Generation]] systems.

#### 5. Anisotropic Quantization for Inner Product Search

Anisotropic quantization for maximum inner product search (MIPS) modifies the quantization loss to penalize the parallel component of the error relative to the query vector more heavily than the orthogonal component. Traditional quantization minimizes total reconstruction error, but MIPS ranking depends primarily on the parallel error component. The loss function weights the parallel residual error more strongly, leading to quantized representations that better preserve inner product structure. Inputs are high-dimensional database vectors and a query vector; outputs are compact quantized codes enabling efficient MIPS. This design choice leverages statistical assumptions about data distribution to optimize for the relevant error component, improving recall and precision without increasing storage overhead significantly. Guo et al. (2019) demonstrated that this method achieves state-of-the-art results on public MIPS benchmarks, though it requires adherence to the underlying statistical model for optimal performance.

#### 6. Metadata Filtering

Metadata filtering applies structured criteria to vector search results. Pre-filtering restricts the candidate set to vectors matching metadata conditions before similarity search, typically using secondary indexes (e.g., B-trees for key-value or range queries) on metadata fields. This reduces the number of vectors processed, improving search speed but risking reduced recall if filters exclude relevant vectors. Post-filtering applies metadata conditions to the top-k results from full vector search, preserving the vector search's recall but potentially reducing the final result count below k. The candidate set size for pre-filtering is the intersection of metadata and vector proximity; for post-filtering, it is the top-k vector results after metadata filtering. Design trade-offs involve balancing query efficiency (pre-filtering) against recall preservation (post-filtering), with pre-filtering preferred for large datasets and high filter specificity, while post-filtering offers simpler implementation but higher computational cost for the vector search phase. [[rag-retrieval|Retrieval]] and [[rag-evaluation|Evaluation]] metrics must account for the filtering method's impact on result quality.

#### Origin and variants

Vector database management systems (VDBMSs) evolved from similarity search libraries (e.g., FAISS) that provided indexing structures but lacked full database features like metadata management, CRUD operations, and scalable persistence. Pan et al. (2023) note over 20 commercial VDBMSs emerged within the past five years, driven by applications requiring scalable vector search for high-dimensional embeddings. Inputs are high-dimensional vectors (e.g., embeddings) and metadata; outputs are top-k similar vectors with metadata filtering. Key index structures include HNSW (Hierarchical Navigable Small World), a hierarchical graph enabling logarithmic search complexity (Malkov & Yashunin, 2016), IVF (Inverted File Index), which partitions vectors into clusters to reduce search space, and PQ (Product Quantization), which compresses vectors via sub-vector quantization for memory efficiency (Jégou et al., 2011). Modern VDBMSs combine these: IVF for coarse clustering, HNSW for fine-grained search within clusters, and PQ for vector compression. Design trade-offs involve HNSW’s high recall and memory cost versus IVF’s speed at potential recall loss, and PQ’s storage savings versus precision degradation. These combinations balance speed, recall, and storage for production systems.

### When to use it

- When exact search becomes computationally infeasible for datasets exceeding millions of vectors (Johnson et al. (2017) process 1 billion vectors in <12 hours on 4 GPUs).
- For high-recall similarity search requiring logarithmic query complexity (Malkov & Yashunin (2016) show HNSW achieves logarithmic scaling).
- For [[retrieval-augmented-generation|Retrieval-Augmented Generation]] systems demanding scalable retrieval over vast unstructured data (Pan et al. (2023) identify this as a primary driver).

### Strengths and limitations

**Strengths**
- HNSW achieves logarithmic complexity scaling for approximate nearest neighbor search (Malkov & Yashunin (2016)).
- GPU-based implementations achieve up to 8.5x speedup over prior GPU approaches for similarity search (Johnson et al. (2017)).
- Product quantization enables efficient approximate search with reduced memory footprint (Jégou et al. (2011)).

**Limitations**
- Approximate nearest neighbor search inherently trades off recall for speed, making exact search necessary for critical applications (Pan et al. (2023)).
- Vector quantization introduces information loss, potentially degrading retrieval accuracy (Guo et al. (2019)).
- Hybrid queries combining attribute filtering and vector similarity are challenging to optimize efficiently (Pan et al. (2023)).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Vector Database | Integrates scalable approximate nearest neighbor search (e.g., HNSW, IVF) with full database features (CRUD, metadata management, scalability). | Large-scale production RAG systems requiring persistent storage, updates, metadata filtering, and multi-tenancy (Pan et al. 2023). |
| Exact search | Uses brute-force distance computation for exact matches, scaling linearly with dataset size (O(n) per query). | Small datasets (e.g., <10,000 vectors) where exact recall is critical. |
| Vector index library (e.g., FAISS) | Provides indexing and search capabilities but lacks integrated database management (e.g., no persistent storage, no metadata filtering). | Prototyping, small-scale applications, or as a component within a custom application (e.g., [[rag-chunking|chunking]] pipelines). |

Vector databases become necessary when scalability and metadata management are required for production systems, unlike exact search for small-scale use cases or index libraries for simple indexing. Commercial VDBMS adoption has accelerated due to demand for efficient similarity search in large-scale RAG applications (Pan et al. 2023).

### In practice

Evaluation metrics include recall@k and latency; [[rag-retrieval-evaluation|ANN Benchmark]] shows that anisotropic quantization (Guo et al. 2019) achieves higher recall at 8 bits than standard quantization. Typical failure modes include using unnormalized embeddings with cosine similarity (distorting ranking) and selecting top-k values exceeding context window limits (increasing token costs). Key HNSW parameters are the maximum layer index and connections per node (Malkov & Yashunin 2016), while product quantization requires sub-vector count and codebook size (Jégou et al. 2011).

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

Vektordatenbanken bieten skalierbare Approximate Nearest Neighbor Suche für hochdimensionale Vektorembeddings, wodurch der hohe rechnerische Aufwand für exakte Suche in großen Datensätzen gelöst wird. Diese Fähigkeit ist für effiziente [[retrieval-augmented-generation|Retrieval-Augmented Generation]]-Systeme entscheidend, die schnelle Ähnlichkeitsretrieval über umfangreiche unstrukturierte Datenspeicher erfordern.

### Funktionsweise

Vektordatenbanken implementieren Approximate Nearest Neighbor Search durch hierarchische Graphenkonstruktion für effiziente Navigation (HNSW) (Malkov & Yashunin, 2016), inverted-file Partitionierung mit GPU-Beschleunigung (FAISS) (Johnson et al., 2017), Vektorkompression über Product Quantization (PQ) (Jégou et al., 2011) und anisotrope Quantisierung für Innenproduktsuche (Guo et al., 2019), wobei Metadaten-Filterung für kontextbewusste Retrieval unterstützt wird.

```text
Hierarchische Graphenkonstruktion (HNSW)
▼
Hierarchische Navigation für Query-Verarbeitung (HNSW)
▼
Inverted-File Partitionierung und GPU-Suche (FAISS)
▼
Vektorkompression über Product Quantization (PQ)
▼
Anisotrope Quantisierung für Innenproduktsuche
▼
Metadaten-Filterung, Ursprung und Varianten
```

#### 1. Hierarchische Graphenkonstruktion (HNSW)

Die hierarchische Graphenkonstruktion in HNSW baut schrittweise einen mehrschichtigen Graphen auf, wobei jeder Schicht `l` (beginnend bei 0) ein Proximity-Graph über einer geschachtelten Teilmenge der gespeicherten Vektoren entspricht. Die maximale Schicht für einen Vektor wird zufällig mit einer exponentiell abnehmenden Wahrscheinlichkeitsverteilung proportional zu `p^l` (wobei `0 < p < 1`) ausgewählt, wie in Malkov & Yashunin (2016) festgelegt. Dies stellt sicher, dass höhere Schichten weniger, aber weit verbreitete Vektoren enthalten, was eine Skalierungstrennung in Verknüpfungsdistanzen erzeugt. Der Suchalgorithmus beginnt in der höchsten Schicht und navigiert nach unten, wobei die hierarchische Struktur genutzt wird, um eine logarithmische Abfragekomplexität in Beziehung zum Datensatzumfang zu erreichen. Dieses Design verbessert erheblich die Suchgeschwindigkeit und Recall, insbesondere bei gruppierten Daten, indem die Anzahl der Distanzberechnungen im Vergleich zu Einzelschichtansätzen reduziert wird. Kompromisse umfassen erhöhten Speicherbedarf für die Schichtstruktur und komplexere Indexkonstruktion, wobei diese durch überlegene Abfrageleistung ausgeglichen werden. Der Ansatz nutzt Proximity-Metriken wie [[embeddings|Similarity-Metriken]], um Graphenverbindungen zu definieren, wodurch das Bedürfnis nach Hilfs-Suchstrukturen vermieden wird.

#### 2. Hierarchische Navigation für Query-Verarbeitung (HNSW)

HNSW (Hierarchical Navigable Small World) verarbeitet Abfragen mithilfe eines mehrschichtigen Proximity-Graphen-Index. Der Index besteht aus geschachtelten Schichten, wobei jede Schicht eine Teilmenge der Datenpunkte enthält; die oberste Schicht hat die wenigsten Punkte, und untere Schichten enthalten zunehmend mehr Punkte. Die Abfrageverarbeitung beginnt in der obersten Schicht, wobei der nächstgelegene Nachbar zum Abfragevektor identifiziert wird. Danach wird gierig zu unteren Schichten abgestiegen, wobei von dem aktuellen Knoten aus der nächstgelegene Nachbar in der neuen Schicht (basierend auf einer Heuristik, die hohe Ähnlichkeit priorisiert) ausgewählt wird, bis die unterste Schicht erreicht ist. Diese gierige Navigation, kombiniert mit der Heuristik zur Nachbarschaftsauswahl (die Recall bei gruppierten Daten verbessert), gewährleistet eine effiziente Suche. Die hierarchische Struktur mit Skalierungstrennung ermöglicht es, dass der Suchaufwand ungefähr logarithmisch mit der Datensatzgröße skaliert, wie Malkov & Yashunin (2016) zeigen. Die Eingaben sind ein Abfragevektor und der HNSW-Index; die Ausgaben sind die k ungefähren nächsten Nachbarn. Designentscheidungen umfassen die exponentiell abnehmende Wahrscheinlichkeit für die Schichtzuordnung (um die Schichtdichte auszugleichen) und das Fehlen von Hilfs-Suchstrukturen, wodurch ein höherer Speicherbedarf für logarithmische Abfragekomplexität getauscht wird. Dies steht im Kontrast zu nicht-hierarchischen Methoden wie NSW, die die geschichtete Optimierung nicht besitzen.

#### 3. Inverted-File Partitionierung und GPU-Suche (FAISS)

Die Inverted-File Partitionierung (IVF) gruppiert den Vektorraum mithilfe eines groben Quantisierers, wie z. B. k-means, der Vektoren in Zentroiden unterteilt. Jeder Vektor wird einem Zentroid (Code) zugeordnet, und Vektoren werden in Inverted-Listen pro Zentroid gruppiert. Während einer Abfrage identifiziert der grobe Quantisierer die relevanten Cluster(s), wodurch der Suchraum auf nur wenige Listen reduziert wird. Dies wird mit komprimierten Codes (z. B. Product Quantization) kombiniert, bei denen Vektoren in Untervektoren aufgeteilt und in kompakte Codes quantisiert werden. Die Suche erfolgt in drei Modi: brute-force (genaue Vergleichsoperation innerhalb der ausgewählten Listen), approximativ (Distanzabschätzung aus komprimierten Codes) und komprimiert (direkte Distanzberechnung aus Codes ohne Dekomprimierung). Johnson et al. (2017) führten eine GPU-optimierte k-Selektion ein, die 55 % der theoretischen Spitzenleistung erreicht, wodurch eine 8,5-fache Beschleunigung gegenüber früheren GPU-Methoden ermöglicht wird und eine Billionenskalierung (z. B. 1 Milliarde Vektoren in weniger als 12 Stunden auf 4 GPUs) unterstützt wird. Das Design tauscht Recall-Reduktion (aufgrund von Cluster-Pruning) gegen erhebliche Geschwindigkeits- und Speichererhöhung, wodurch es für großskalige Anwendungen wie [[retrieval-augmented-generation|Retrieval-Augmented Generation]] geeignet ist.

#### 4. Vektorkompression über Product Quantization (PQ)

Product Quantization (PQ) komprimiert hochdimensionale Vektoren, indem jeder Vektor in M nicht überlappende Untervektoren unterteilt wird. Für jeden Untervektor wird ein kleiner Codebuch (eine Menge von Zentroiden, gelernt über k-means-Clustering) erstellt. Jeder Untervektor wird dann durch einen Code (einen Index in das Codebuch) dargestellt, wodurch der Speicherbedarf von Gleitkommawerten auf kleine Ganzzahlen reduziert wird. Die Eingabe besteht aus einer Menge hochdimensionaler Vektoren; die Ausgabe umfasst kompakte Codes für jeden Vektor und die zugehörigen Codebücher. Die Distanzberechnung zwischen Vektoren wird als Summe vorberechneter Distanzen zwischen entsprechenden Untervektor-Codes (mithilfe von Zentroiddistanzen) berechnet, wodurch vollständige Vektordistanzberechnungen während der Suche vermieden werden. Wichtige Designentscheidungen umfassen die Anzahl der Untervektoren M und die Codebuchgröße pro Untervektor. Eine Erhöhung von M oder der Codebuchgröße verbessert die Distanzgenauigkeit, erhöht aber auch die Codebuchspeicheranforderungen. PQ, eingeführt von Jégou et al. (2011), ermöglicht effiziente ungefähre nächstgelegene Nachbarsuche in großen Vektordatenbanken, indem der Komprimierungsgrad und die Suchgenauigkeit ausgewogen werden, was ein entscheidender Bestandteil für skalierbare [[retrieval-augmented-generation|Retrieval-Augmented Generation]]-Systeme ist.

#### 5. Anisotrope Quantisierung für Innenproduktsuche

Die anisotrope Quantisierung für maximale Innenproduktsuche (MIPS) modifiziert den Quantisierungsfehler, um den parallelen Fehlerkomponenten relativ zum Abfragevektor stärker als die orthogonale Fehlerkomponente bestraft zu werden. Traditionelle Quantisierung minimiert den Gesamtrekonstruktionsfehler, aber die MIPS-Rangliste hängt hauptsächlich vom parallelen Fehlerkomponenten ab. Die Verlustfunktion gewichtet den parallenen Residuierungsfehler stärker, was zu quantisierten Darstellungen führt, die besser die Innenproduktstruktur bewahren. Die Eingaben sind hochdimensionale Datenbankvektoren und ein Abfragevektor; die Ausgaben sind kompakte quantisierte Codes, die eine effiziente MIPS ermöglichen. Diese Designentscheidung nutzt statistische Annahmen über die Datenverteilung, um den relevanten Fehlerkomponenten zu optimieren, wodurch Recall und Präzision verbessert werden, ohne den Speicherbedarf erheblich zu erhöhen. Guo et al. (2019) zeigten, dass dieser Ansatz auf öffentlichen MIPS-Benchmarks state-of-the-art Ergebnisse erzielt, obwohl er zur optimalen Leistung die Einhaltung des zugrunde liegenden statistischen Modells erfordert.

#### 6. Metadaten-Filterung

Metadaten-Filterung wendet strukturierte Kriterien auf Vektorsuchergebnisse an. Vorabfilterung beschränkt die Kandidatenmenge auf Vektoren, die Metadatenbedingungen erfüllen, bevor eine Ähnlichkeitsuche durchgeführt wird, typischerweise mithilfe sekundärer Indizes (z. B. B-Bäume für Schlüssel-Wert- oder Bereichsabfragen) auf Metadatenfelder. Dies reduziert die Anzahl der verarbeiteten Vektoren, verbessert die Suchgeschwindigkeit, birgt aber das Risiko einer reduzierten Recall, wenn Filter relevante Vektoren ausschließen. Nachabfilterung wendet Metadatenbedingungen auf die Top-k-Ergebnisse aus der vollständigen Vektorsuche an, wodurch die Recall des Vektorsuchvorgangs erhalten bleibt, aber die Anzahl der endgültigen Ergebnisse unter k fallen kann. Die Kandidatenmenge für Vorabfilterung ist der Schnitt aus Metadaten und Vektornähe; für Nachabfilterung ist sie die Top-k-Vektorergebnisse nach Metadatenfilterung. Designkompromisse umfassen das Ausbalancieren der Abfrageeffizienz (Vorabfilterung) gegen die Erhaltung der Recall (Nachabfilterung), wobei Vorabfilterung bei großen Datensätzen und hoher Filterpräzision bevorzugt wird, während Nachabfilterung eine einfachere Implementierung bietet, aber einen höheren Rechenaufwand für den Vektorsuchvorgang hat. [[rag-retrieval|Retrieval]] und [[rag-evaluation|Evaluation]]-Metriken müssen den Einfluss der Filtermethode auf die Ergebnisqualität berücksichtigen.

#### Ursprung und Varianten

Vektordatenbankmanagementsysteme (VDBMSs) entwickelten sich aus Ähnlichkeitsuche-Bibliotheken (z. B. FAISS), die Indizesstrukturen bereitstellten, aber keine vollständigen Datenbankfunktionen wie Metadatenverwaltung, CRUD-Operationen oder skalierbare Persistenz besaßen. Pan et al. (2023) betonen, dass über 20 kommerzielle VDBMSs in den letzten fünf Jahren entstanden sind, getrieben durch Anwendungen, die skalierbare Vektorsuche für hochdimensionale Embeddings benötigen. Die Eingaben sind hochdimensionale Vektoren (z. B. Embeddings) und Metadaten; die Ausgaben sind die Top-k-ähnlichen Vektoren mit Metadatenfilterung. Wichtige Indexstrukturen umfassen HNSW (Hierarchical Navigable Small World), einen hierarchischen Graphen, der eine logarithmische Suchkomplexität ermöglicht (Malkov & Yashunin, 2016), IVF (Inverted File Index), der Vektoren in Cluster unterteilt, um den Suchraum zu reduzieren, und PQ (Product Quantization), der Vektoren durch Untervektorquantisierung für Speichereffizienz komprimiert (Jégou et al., 2011). Moderne VDBMSs kombinieren diese: IVF für grobe Clustering, HNSW für feingranulare Suche innerhalb der Cluster und PQ für Vektorkompression. Designkompromisse umfassen HNSWs hohe Recall und Speicherkosten im Vergleich zu IVFs Geschwindigkeit bei potenzieller Recall-Verlust, und PQs Speichereinsparungen im Vergleich zur Präzisionsverringerung. Diese Kombinationen balancieren Geschwindigkeit, Recall und Speicher für Produktionsumgebungen.

### Wann einsetzen

- Wenn präzise Suche für Datensätze, die mehrere Millionen Vektoren umfassen, rechnerisch nicht mehr umsetzbar ist (Johnson et al. (2017) verarbeiten 1 Milliarde Vektoren in <12 Stunden auf 4 GPUs).
- Für hochpräzise Ähnlichkeitsuche mit logarithmischer Abfrageskomplexität (Malkov & Yashunin (2016) zeigen, dass HNSW logarithmische Skalierung erreicht).
- Für [[retrieval-augmented-generation|Retrieval-Augmented Generation]]-Systeme, die skalierbare Retrieval über umfangreiche unstrukturierte Daten erfordern (Pan et al. (2023) identifizieren dies als primären Treiber).

### Stärken und Grenzen

**Vorteile**
- HNSW erreicht logarithmische Komplexitätsskalierung für Approximate Nearest Neighbor Search (Malkov & Yashunin (2016)).
- GPU-basierte Implementierungen erzielen bis zu 8,5-fache Geschwindigkeitssteigerung gegenüber früheren GPU-Ansätzen bei der Ähnlichkeitsuche (Johnson et al. (2017)).
- Product Quantization ermöglicht effiziente Approximationsuche mit reduziertem Speicheraufwand (Jégou et al. (2011)).

**Einschränkungen**
- Approximate Nearest Neighbor Search weist grundlegend einen Kompromiss zwischen Recall und Geschwindigkeit auf, wodurch exakte Suche für kritische Anwendungen erforderlich ist (Pan et al. (2023)).
- Vektorquantisierung führt zu Informationsverlust, der möglicherweise die Retrievalgenauigkeit verringert (Guo et al. (2019)).
- Hybridabfragen, die Attributfilterung und Vektorschwerpunktsimilarität kombinieren, sind schwierig effizient zu optimieren (Pan et al. (2023)).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Vektordatenbank | Integriert skalierbare Approximate Nearest Neighbor Suche (z. B. HNSW, IVF) mit vollständigen Datenbankfunktionen (CRUD, Metadatenverwaltung, Skalierbarkeit). | Großskalige Produktions-RAG-Systeme, die persistenter Speicherung, Updates, Metadatenfilterung und Multi-Tenancy erfordern (Pan et al. 2023). |
| Exakte Suche | Verwendet brute-force Distanzberechnung für exakte Übereinstimmungen, die linear mit der Datengröße skaliert (O(n) pro Abfrage). | Kleine Datensätze (z. B. <10.000 Vektoren), bei denen exakte Recall kritisch ist. |
| Vektordatenbank-Bibliothek (z. B. FAISS) | Bietet Indexierung und Suchfunktionen, verfügt jedoch nicht über integrierte Datenbankverwaltung (z. B. keine persistente Speicherung, keine Metadatenfilterung). | Prototypen, kleine Anwendungen oder als Komponente innerhalb einer benutzerdefinierten Anwendung (z. B. [[rag-chunking|Chunking]]-Pipelines). |

Vektordatenbanken werden erforderlich, wenn Skalierbarkeit und Metadatenverwaltung für Produktionsysteme benötigt werden, im Gegensatz zur exakten Suche für kleine Anwendungsfälle oder Indexbibliotheken für einfache Indexierung. Die Adoption kommerzieller VDBMS hat sich aufgrund des Bedarfs nach effizienter Ähnlichkeitsuche in großskaligen RAG-Anwendungen beschleunigt (Pan et al. 2023).

### In der Praxis

Bewertungskriterien umfassen Recall@k und Latenz; [[rag-retrieval-evaluation|ANN Benchmark]] zeigt, dass anisotropes Quantisieren (Guo et al. 2019) bei 8 Bit eine höhere Recall erzielt als das Standard-Quantisieren. Typische Fehlmodi umfassen die Verwendung von nicht normalisierten Embeddings mit Kosinusähnlichkeit (die das Ranking verzerren) und das Auswählen von top-k Werten, die die Grenzen des Kontextfensters überschreiten (die Tokenkosten erhöhen). Wichtige HNSW-Parameter sind der maximale Schichtindex und die Anzahl der Verbindungen pro Knoten (Malkov & Yashunin 2016), während Product Quantization die Anzahl der Untervektoren und die Größe des Codebuchs erfordert (Jégou et al. 2011).

### Merksatz

Vektordatenbanken verwenden Approximate Nearest Neighbor (ANN)-Suche für hochdimensionale [[embeddings|Embeddings]], wobei Genauigkeit bei der Retrieval gegen Geschwindigkeit und Skalierbarkeit getauscht wird.

### Quellen

- Malkov, Y. A. & Yashunin, D. A. (2016). *Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs.* [arXiv:1603.09320](https://arxiv.org/abs/1603.09320)
- Johnson, J. et al. (2017). *Billion-scale similarity search with GPUs.* [arXiv:1702.08734](https://arxiv.org/abs/1702.08734)
- Pan, J. J. et al. (2023). *Survey of Vector Database Management Systems.* [arXiv:2310.14021](https://arxiv.org/abs/2310.14021)
- Guo, R. et al. (2019). *Accelerating Large-Scale Inference with Anisotropic Vector Quantization.* [arXiv:1908.10396](https://arxiv.org/abs/1908.10396)
- Jégou, H., Douze, M. & Schmid, C. (2011). *Product Quantization for Nearest Neighbor Search.* IEEE Transactions on Pattern Analysis and Machine Intelligence 33(1). [doi:10.1109/TPAMI.2010.57](https://doi.org/10.1109/TPAMI.2010.57)
