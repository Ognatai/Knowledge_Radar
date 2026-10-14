---
title_en: HNSW (Hierarchical Navigable Small World)
title_de: HNSW (Hierarchical Navigable Small World)
entity_type: Method
aliases:
- HNSW
- Hierarchical Navigable Small World
- Hierarchical NSW
sources:
- https://arxiv.org/abs/1603.09320
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

HNSW is a graph-based index for approximate nearest neighbour search: vectors are nodes in several layers of proximity graphs, sparse at the top with long links and dense at the bottom with short links, and a query descends greedily from the top layer to the bottom (Malkov & Yashunin, 2020). Each vector's top layer is drawn at random from an exponentially decaying distribution, as in a skip list, which gives search complexity that scales logarithmically with the number of vectors (Malkov & Yashunin, 2020). A neighbour-selection heuristic keeps the graph connected even for clustered data. HNSW outperformed the open-source alternatives of its time by a large margin on high-dimensional data and is one of the main index types in [[vector-databases|vector databases]], including [[neo4j|Neo4j]]'s vector index.

### How it works

```text
insert vector q:
  level l = ⌊−ln(U(0,1)) · mL⌋                       (exponentially decaying, mL ≈ 1/ln(M))
  from the top layer down to l+1: greedy search with ef = 1 → closest entry point
  from layer min(L, l) down to 0: search efConstruction candidates,
     connect q to M neighbours chosen by the heuristic, prune neighbours above Mmax (Mmax0 = 2M on layer 0)
query vector:
  greedy descent from the top layer (ef = 1) → on layer 0 search with ef ≥ K → return K nearest
```

#### 1. From navigable small-world graphs to layers

Exact K-nearest-neighbour search compares the query with every stored vector, which scales linearly and is infeasible for large collections; approximate methods trade a little recall for much speed (Malkov & Yashunin, 2020). Navigable small world (NSW) graphs, the predecessor of HNSW, allow greedy routing: start at a node and keep moving to the neighbour closest to the query. In NSW, however, routing passes through ever more highly connected hubs as the graph grows, which gives polylogarithmic complexity. HNSW separates links by their length scale into layers, so that each layer only needs a fixed number of connections per node, and the search starts on the top layer with the longest links (Malkov & Yashunin, 2020).

#### 2. Random levels as in a skip list

For every inserted element, the maximum layer is chosen as `l = ⌊−ln(unif(0,1)) · mL⌋`, an exponentially decaying distribution normalised by `mL` (Malkov & Yashunin, 2020). Most elements live only on layer 0, few reach the upper layers, and the expected number of layers grows logarithmically. A simple near-optimal choice is `mL = 1/ln(M)`, which corresponds to a skip list with parameter `p = 1/M`. The structure generalises the probabilistic skip list by replacing its linked lists with proximity graphs. Because randomness comes from the level draw, elements do not have to be shuffled before insertion, and the index can be built incrementally (Malkov & Yashunin, 2020).

#### 3. Search

The search starts at a fixed entry point on the top layer and greedily moves to closer neighbours until it reaches a local minimum, then drops to the next layer and repeats from there (Malkov & Yashunin, 2020). On each layer, a dynamic list of the `ef` closest elements found so far is kept, and the neighbourhood of the closest unevaluated element is expanded until no better candidates appear. In the upper layers `ef = 1`; on layer 0 a larger `ef` controls the trade-off between recall and speed at query time (Malkov & Yashunin, 2020).

#### 4. Construction and the neighbour heuristic

Insertion uses the same layered search with `efConstruction` candidates and connects the new element on each of its layers (Malkov & Yashunin, 2020). Instead of simply linking to the M closest candidates, a heuristic links to a candidate only if it is closer to the new element than to any already connected candidate; this creates diverse connections and keeps links between clusters, which would otherwise be missing because all closest neighbours lie in the same cluster. The heuristic gave equal or better performance in all tests and was decisive for clustered and low-dimensional data. Neighbours whose degree exceeds `Mmax` (`Mmax0` on layer 0) are pruned with the same heuristic (Malkov & Yashunin, 2020).

#### 5. Parameters and memory

M, the number of connections per new element, is the main user parameter; a reasonable range is 5 to 48, with smaller M better for low recall or low-dimensional data and larger M for high recall or high-dimensional data (Malkov & Yashunin, 2020). `Mmax0 = 2·M` on layer 0 is a good default, and `efConstruction` should be large enough for a construction recall close to 1 (about 0.95 suffices). Memory is dominated by the links: about `(Mmax0 + mL · Mmax) · bytes_per_link` per element, typically 60 to 450 bytes per object excluding the vectors themselves (Malkov & Yashunin, 2020).

#### Origin and variants

Yury Malkov and Dmitry Yashunin first posted HNSW in 2016; it was published in IEEE Transactions on Pattern Analysis and Machine Intelligence and implemented in C++ in the open-source nmslib and hnswlib libraries (Malkov & Yashunin, 2020). Libraries such as [[faiss|FAISS]] also provide HNSW indexes, alongside inverted-file and product-quantisation indexes.

### When to use it

- Low-latency, high-recall search over millions of embedding vectors held in memory, as in [[retrieval-augmented-generation|RAG]] retrieval ([[rag-retrieval|RAG retrieval]], [[semantic-retrieval|semantic retrieval]]).
- Collections that grow continuously, since HNSW supports incremental insertion (Malkov & Yashunin, 2020).
- Data with complex structure, such as clusters or varying effective dimensionality, where the authors found HNSW robust (Malkov & Yashunin, 2020).

### Strengths and limitations

**Strengths**
- Logarithmic complexity scaling and leading performance on many datasets, especially high-dimensional ones (Malkov & Yashunin, 2020).
- Few parameters; recall and speed can be tuned at query time with `ef` (Malkov & Yashunin, 2020).
- Incremental indexing without rebuilding (Malkov & Yashunin, 2020).

**Limitations**
- The graph must be held in memory, adding 60 to 450 bytes of links per vector to the vectors themselves (Malkov & Yashunin, 2020).
- Distributed search is harder than with flat NSW, because every search starts on the top layer (Malkov & Yashunin, 2020).
- Updates and removal of elements were left for future work in the original paper (Malkov & Yashunin, 2020).

### Comparison

| Index | Idea | Strength | Weakness |
|---|---|---|---|
| Flat (exact) | compare with every vector | exact | linear cost |
| HNSW | layered proximity graph, greedy descent | high recall at low latency | memory for links |
| IVF ([[faiss\|FAISS]]) | cluster vectors, search nearest clusters | smaller memory with compression | recall depends on probed clusters |
| NSW | single small-world graph | simple, distributable | polylogarithmic scaling |

Source: Malkov & Yashunin (2020); further index types are compared in [[vector-databases|vector databases]].

### In practice

Tuning starts with M in the recommended range and an `efConstruction` that reaches a construction recall close to 1; `ef` is then raised at query time until recall on a sample is high enough (Malkov & Yashunin, 2020). Recall of approximate search should be measured against exact search on a sample before deployment, as part of [[rag-retrieval-evaluation|retrieval evaluation]].

### Key takeaway

HNSW stacks proximity graphs in randomly assigned layers like a skip list, descends greedily from long to short links and uses a diversity heuristic for neighbours, giving fast, high-recall approximate nearest neighbour search at the cost of memory for the graph.

### Sources

- Malkov, Y. A. & Yashunin, D. A. (2020). *Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs.* IEEE Transactions on Pattern Analysis and Machine Intelligence 42(4). [arXiv:1603.09320](https://arxiv.org/abs/1603.09320)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

HNSW ist ein graphbasierter Index für Approximate Nearest Neighbor Search: Vektoren sind Knoten in mehreren Schichten von Nachbarschaftsgraphen, oben dünn mit langen Kanten, unten dicht mit kurzen Kanten, und eine Anfrage steigt gierig von der obersten zur untersten Schicht ab (Malkov & Yashunin, 2020). Die oberste Schicht jedes Vektors wird zufällig aus einer exponentiell abfallenden Verteilung gezogen, wie bei einer Skip-Liste, wodurch der Suchaufwand logarithmisch mit der Zahl der Vektoren wächst (Malkov & Yashunin, 2020). Eine Heuristik zur Auswahl der Nachbarn hält den Graphen auch bei geclusterten Daten verbunden. HNSW übertraf die Open-Source-Alternativen seiner Zeit bei hochdimensionalen Daten deutlich und ist eine der wichtigsten Indexarten in [[vector-databases|Vektordatenbanken]], auch im Vektorindex von [[neo4j|Neo4j]].

### Funktionsweise

```text
Vektor q einfügen:
  Ebene l = ⌊−ln(U(0,1)) · mL⌋                        (exponentiell abfallend, mL ≈ 1/ln(M))
  von der obersten Schicht bis l+1: gierige Suche mit ef = 1 → nächster Einstiegspunkt
  von Schicht min(L, l) bis 0: efConstruction Kandidaten suchen,
     q mit M per Heuristik gewählten Nachbarn verbinden, Nachbarn über Mmax kürzen (Mmax0 = 2M auf Schicht 0)
Anfragevektor:
  gieriger Abstieg von der obersten Schicht (ef = 1) → auf Schicht 0 Suche mit ef ≥ K → K nächste zurückgeben
```

#### 1. Von navigierbaren Small-World-Graphen zu Schichten

Exakte Suche nach den K nächsten Nachbarn vergleicht die Anfrage mit jedem gespeicherten Vektor, wächst linear und ist für große Sammlungen nicht praktikabel; approximative Verfahren tauschen etwas Recall gegen viel Geschwindigkeit (Malkov & Yashunin, 2020). Navigable-Small-World-Graphen (NSW), der Vorgänger von HNSW, erlauben gieriges Routing: an einem Knoten beginnen und immer zum Nachbarn wechseln, der der Anfrage am nächsten ist. In NSW führt das Routing mit wachsendem Graphen jedoch über immer stärker vernetzte Knotenpunkte, was polylogarithmischen Aufwand ergibt. HNSW trennt Kanten nach ihrer Längenskala in Schichten, sodass jede Schicht nur eine feste Zahl von Verbindungen je Knoten braucht, und die Suche beginnt auf der obersten Schicht mit den längsten Kanten (Malkov & Yashunin, 2020).

#### 2. Zufällige Ebenen wie in einer Skip-Liste

Für jedes eingefügte Element wird die höchste Schicht als `l = ⌊−ln(unif(0,1)) · mL⌋` gewählt, eine exponentiell abfallende Verteilung, normiert durch `mL` (Malkov & Yashunin, 2020). Die meisten Elemente liegen nur auf Schicht 0, wenige erreichen die oberen Schichten, und die erwartete Zahl der Schichten wächst logarithmisch. Eine einfache, nahezu optimale Wahl ist `mL = 1/ln(M)`, was einer Skip-Liste mit Parameter `p = 1/M` entspricht. Die Struktur verallgemeinert die probabilistische Skip-Liste, indem sie deren verkettete Listen durch Nachbarschaftsgraphen ersetzt. Weil der Zufall aus der Ziehung der Ebene stammt, müssen Elemente vor dem Einfügen nicht gemischt werden, und der Index lässt sich inkrementell aufbauen (Malkov & Yashunin, 2020).

#### 3. Suche

Die Suche beginnt an einem festen Einstiegspunkt auf der obersten Schicht und wechselt gierig zu näheren Nachbarn, bis sie ein lokales Minimum erreicht, steigt dann zur nächsten Schicht ab und wiederholt das von dort (Malkov & Yashunin, 2020). Auf jeder Schicht wird eine dynamische Liste der `ef` nächsten bisher gefundenen Elemente geführt, und die Nachbarschaft des nächsten noch nicht ausgewerteten Elements wird erweitert, bis keine besseren Kandidaten mehr auftauchen. In den oberen Schichten gilt `ef = 1`; auf Schicht 0 steuert ein größeres `ef` zur Anfragezeit den Abtausch zwischen Recall und Geschwindigkeit (Malkov & Yashunin, 2020).

#### 4. Aufbau und Nachbarschaftsheuristik

Das Einfügen nutzt dieselbe geschichtete Suche mit `efConstruction` Kandidaten und verbindet das neue Element auf jeder seiner Schichten (Malkov & Yashunin, 2020). Statt einfach mit den M nächsten Kandidaten zu verbinden, verbindet eine Heuristik nur dann mit einem Kandidaten, wenn dieser dem neuen Element näher ist als jedem bereits verbundenen Kandidaten; das erzeugt vielfältige Verbindungen und erhält Kanten zwischen Clustern, die sonst fehlen würden, weil alle nächsten Nachbarn im selben Cluster liegen. Die Heuristik war in allen Tests gleich gut oder besser und entscheidend für geclusterte und niedrigdimensionale Daten. Nachbarn, deren Grad `Mmax` überschreitet (`Mmax0` auf Schicht 0), werden mit derselben Heuristik gekürzt (Malkov & Yashunin, 2020).

#### 5. Parameter und Speicher

M, die Zahl der Verbindungen je neuem Element, ist der wichtigste Parameter für Nutzende; ein sinnvoller Bereich ist 5 bis 48, wobei kleineres M für niedrigen Recall oder niedrigdimensionale Daten besser ist und größeres M für hohen Recall oder hochdimensionale Daten (Malkov & Yashunin, 2020). `Mmax0 = 2·M` auf Schicht 0 ist eine gute Voreinstellung, und `efConstruction` sollte groß genug für einen Recall beim Aufbau nahe 1 sein (etwa 0,95 genügt). Den Speicher bestimmen die Kanten: etwa `(Mmax0 + mL · Mmax) · bytes_per_link` je Element, typischerweise 60 bis 450 Byte je Objekt ohne die Vektoren selbst (Malkov & Yashunin, 2020).

#### Herkunft und Varianten

Yury Malkov und Dmitry Yashunin veröffentlichten HNSW erstmals 2016; erschienen ist es in den IEEE Transactions on Pattern Analysis and Machine Intelligence, umgesetzt in C++ in den Open-Source-Bibliotheken nmslib und hnswlib (Malkov & Yashunin, 2020). Bibliotheken wie [[faiss|FAISS]] bieten HNSW-Indizes ebenfalls an, neben Inverted-File- und Product-Quantization-Indizes.

### Wann einsetzen

- Suche mit geringer Latenz und hohem Recall über Millionen Embedding-Vektoren im Arbeitsspeicher, etwa beim Retrieval für [[retrieval-augmented-generation|RAG]] ([[rag-retrieval|RAG: Retrieval]], [[semantic-retrieval|Semantisches Retrieval]]).
- Sammlungen, die laufend wachsen, weil HNSW inkrementelles Einfügen unterstützt (Malkov & Yashunin, 2020).
- Daten mit komplexer Struktur, etwa Clustern oder wechselnder effektiver Dimensionalität, bei denen die Autoren HNSW als robust befanden (Malkov & Yashunin, 2020).

### Stärken und Grenzen

**Stärken**
- Logarithmisches Skalierungsverhalten und Spitzenleistung auf vielen Datensätzen, vor allem hochdimensionalen (Malkov & Yashunin, 2020).
- Wenige Parameter; Recall und Geschwindigkeit lassen sich zur Anfragezeit über `ef` einstellen (Malkov & Yashunin, 2020).
- Inkrementelle Indexierung ohne Neuaufbau (Malkov & Yashunin, 2020).

**Grenzen**
- Der Graph muss im Speicher liegen und fügt den Vektoren 60 bis 450 Byte an Kanten je Vektor hinzu (Malkov & Yashunin, 2020).
- Verteilte Suche ist schwieriger als mit flachem NSW, weil jede Suche auf der obersten Schicht beginnt (Malkov & Yashunin, 2020).
- Aktualisieren und Entfernen von Elementen ließ das ursprüngliche Paper für künftige Arbeiten offen (Malkov & Yashunin, 2020).

### Vergleich

| Index | Idee | Stärke | Schwäche |
|---|---|---|---|
| Flach (exakt) | mit jedem Vektor vergleichen | exakt | linearer Aufwand |
| HNSW | geschichteter Nachbarschaftsgraph, gieriger Abstieg | hoher Recall bei geringer Latenz | Speicher für Kanten |
| IVF ([[faiss\|FAISS]]) | Vektoren clustern, nächste Cluster durchsuchen | weniger Speicher mit Kompression | Recall hängt von den durchsuchten Clustern ab |
| NSW | ein einzelner Small-World-Graph | einfach, verteilbar | polylogarithmisches Wachstum |

Quelle: Malkov & Yashunin (2020); weitere Indexarten vergleicht [[vector-databases|Vektordatenbanken]].

### In der Praxis

Die Abstimmung beginnt mit M im empfohlenen Bereich und einem `efConstruction`, das einen Recall beim Aufbau nahe 1 erreicht; danach wird `ef` zur Anfragezeit erhöht, bis der Recall auf einer Stichprobe hoch genug ist (Malkov & Yashunin, 2020). Der Recall der approximativen Suche sollte vor dem Einsatz auf einer Stichprobe gegen die exakte Suche gemessen werden, als Teil der [[rag-retrieval-evaluation|Evaluation des Retrievals]].

### Merksatz

HNSW stapelt Nachbarschaftsgraphen in zufällig zugewiesenen Schichten wie eine Skip-Liste, steigt gierig von langen zu kurzen Kanten ab und wählt Nachbarn mit einer Vielfaltsheuristik; das ergibt schnelle Approximate Nearest Neighbor Search mit hohem Recall, bezahlt mit Speicher für den Graphen.

### Quellen

- Malkov, Y. A. & Yashunin, D. A. (2020). *Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs.* IEEE Transactions on Pattern Analysis and Machine Intelligence 42(4). [arXiv:1603.09320](https://arxiv.org/abs/1603.09320)
