---
title_en: Inverted Index
title_de: Invertierter Index (Inverted Index)
entity_type: Concept
aliases:
- Postings list
- Index construction
- Index compression
sources:
- https://nlp.stanford.edu/IR-book/pdf/01bool.pdf
- https://nlp.stanford.edu/IR-book/pdf/02voc.pdf
- https://nlp.stanford.edu/IR-book/pdf/04const.pdf
- https://nlp.stanford.edu/IR-book/pdf/05comp.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

An inverted index maps every term of a collection to its postings list, the sorted list of IDs of the documents that contain it; queries are answered by looking up the terms and merging their postings lists instead of scanning the documents (Manning et al., 2008, ch. 1). Large collections are indexed block by block on disk or distributed with [[mapreduce|MapReduce]], changing collections with auxiliary indexes, and the postings are compressed by storing gaps between document IDs with variable byte or γ codes (Manning et al., 2008, ch. 4 and 5). It is the core data structure of lexical search such as [[bm25|BM25]] and of [[information-retrieval|information retrieval]] in general.

### How it works

```text
documents ─► tokens ─► (term, docID) pairs ─► sort / group by term ─► dictionary + postings lists
                                                                        brutus  → 1, 2, 4, 11, 31 …
                                                                        caesar  → 1, 2, 4, 5, 6 …
query "brutus AND caesar" ─► look up both ─► intersect postings ─► 1, 2, 4 …
```

#### 1. Dictionary and postings

The index has two parts: the dictionary of terms, which also stores each term's document frequency, and for each term a postings list of the documents it occurs in, sorted by document ID. It is built by collecting all term-docID pairs, sorting them by term and then docID, and grouping the docIDs of each term into its postings list (Manning et al., 2008, ch. 1).

#### 2. Answering Boolean queries

For brutus AND calpurnia, the system looks up both terms and intersects their postings lists by walking through both at once and advancing the pointer at the smaller docID; for lists of length x and y this takes O(x + y) steps, and it requires that all lists are sorted by one global order, such as docID. For an AND of several terms, the standard heuristic processes terms in order of increasing document frequency, so that intermediate results stay small (Manning et al., 2008, ch. 1).

#### 3. Skip pointers

Skip pointers stored at indexing time let the intersection jump over parts of a postings list that cannot match; a simple heuristic that works well is about √P evenly spaced skips for a list of length P. They help only for AND queries, not for OR queries, and only for the original lists, not for intermediate results (Manning et al., 2008, ch. 2).

#### 4. Positional index

For phrase queries, a positional index stores each posting as docID with the list of positions where the term occurs; phrase matching then checks that positions are adjacent. A positional index is about 2 to 4 times as large as a non-positional one, and compressed it takes about a third to a half of the size of the raw text (Manning et al., 2008, ch. 2).

#### 5. Building large indexes

When the term-docID pairs do not fit into memory, blocked sort-based indexing (BSBI) sorts pairs block by block in memory, writes each block's inverted index to disk and finally merges all blocks; its time is Θ(T log T) for T pairs. Single-pass in-memory indexing (SPIMI) adds postings directly to a dictionary per block without sorting pairs and without termIDs, so it can index collections of any size given enough disk. For web-scale collections, MapReduce distributes the work: parsers in the map phase write term-docID pairs into segment files by term partition, and inverters in the reduce phase build the postings of each partition; a master node reassigns the work of failed machines (Manning et al., 2008, ch. 4).

#### 6. Changing collections

Rebuilding the whole index periodically works if changes are few. Otherwise new documents go into a small in-memory auxiliary index, searched together with the main index; deletions are recorded in an invalidation bit vector, and updates are a delete plus an insert. Logarithmic merging keeps a sequence of indexes of size n, 2n, 4n …, so that each posting is merged only once per level, giving Θ(T log(T/n)) construction time at the cost of querying several indexes (Manning et al., 2008, ch. 4).

#### 7. Compression

The vocabulary keeps growing with the collection, as Heaps' law M = k·T^b describes (typically 30 ≤ k ≤ 100 and b ≈ 0.5), and term frequencies fall with rank roughly as Zipf's law cf_i ∝ 1/i (Manning et al., 2008, ch. 5). Postings are compressed by storing the gaps between consecutive docIDs instead of the IDs, because gaps of frequent terms are small. Variable byte codes use 7 payload bits per byte plus a continuation bit; γ codes write the length of the binary offset in unary followed by the offset, using 2·⌊log2 G⌋ + 1 bits, within a factor of 2 of optimal. For Reuters-RCV1, uncompressed 20-bit postings take 250 MB, variable byte 116 MB and γ codes 101 MB; the dictionary shrinks from 11.2 MB to 5.9 MB with blocking and front coding (Manning et al., 2008, ch. 5).

#### Origin and variants

The book's chapters build up from Boolean retrieval to the index structures and compression used in search engines (Manning et al., 2008). The same idea, extended with term frequencies and weights, underlies ranked retrieval with tf-idf and BM25 ([[information-retrieval|Information Retrieval]]; [[bm25|BM25]]).

### When to use it

- For keyword search over any text collection, from enterprise search to the sparse part of hybrid [[rag-retrieval|RAG retrieval]] ([[bm25|BM25]]).
- Positional indexes when phrase queries must be supported (Manning et al., 2008, ch. 2).
- Distributed construction with MapReduce when the collection does not fit on one machine (Manning et al., 2008, ch. 4).

### Strengths and limitations

**Strengths**
- Queries touch only the postings of their terms, not the whole collection (Manning et al., 2008, ch. 1).
- Compression shrinks the postings to well under half of their uncompressed size, so more of the index fits in memory (Manning et al., 2008, ch. 5).
- Construction scales from a single machine to clusters (Manning et al., 2008, ch. 4).

**Limitations**
- Frequent updates need auxiliary indexes or logarithmic merging, which complicate statistics and query processing (Manning et al., 2008, ch. 4).
- Positional information makes the index 2 to 4 times larger (Manning et al., 2008, ch. 2).

### Comparison

| Structure | What it stores | Suited for |
|-----------|----------------|------------|
| Inverted index | Term → sorted docIDs (Manning et al., 2008, ch. 1) | Boolean and ranked keyword search |
| Positional index | Term → docIDs with positions (Manning et al., 2008, ch. 2) | Phrase and proximity queries |
| Term-document incidence matrix | One bit per term and document; 40,000 MB for Reuters-RCV1 against 101 MB of γ-coded postings (Manning et al., 2008, ch. 5) | Tiny collections only |
| [[vector-databases\|Vector database]] | Dense [[embeddings\|embeddings]] with an approximate nearest-neighbour index | Semantic similarity |

### In practice

Terms are processed in order of increasing document frequency, and skip pointers are added for long, rarely changing lists (Manning et al., 2008, ch. 1 and 2). Variable byte codes offer an excellent trade-off between time and space and are simple to implement; bit-level codes such as γ compress better when disk space is scarce (Manning et al., 2008, ch. 5). Document IDs must follow one global order so that lists can be merged in linear time (Manning et al., 2008, ch. 1).

### Key takeaway

An inverted index stores, for every term, the sorted list of documents containing it; queries merge these lists, construction scales with blocked or distributed sorting, and gap encoding compresses the postings to a fraction of the text.

### Sources

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Boolean retrieval.* Introduction to Information Retrieval, Chapter 1. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/01bool.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *The term vocabulary and postings lists.* Introduction to Information Retrieval, Chapter 2. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/02voc.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Index construction.* Introduction to Information Retrieval, Chapter 4. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/04const.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Index compression.* Introduction to Information Retrieval, Chapter 5. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/05comp.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Inverted Index ordnet jedem Term einer Sammlung seine Postings-Liste zu, die sortierte Liste der IDs der Dokumente, die ihn enthalten; Anfragen werden beantwortet, indem die Terme nachgeschlagen und ihre Postings-Listen zusammengeführt werden, statt die Dokumente zu durchsuchen (Manning et al., 2008, Kap. 1). Große Sammlungen werden blockweise auf der Festplatte oder verteilt mit [[mapreduce|MapReduce]] indexiert, sich ändernde Sammlungen mit Hilfsindizes, und die Postings werden komprimiert, indem die Abstände zwischen Dokument-IDs mit Variable-Byte- oder γ-Codes gespeichert werden (Manning et al., 2008, Kap. 4 und 5). Er ist die zentrale Datenstruktur der lexikalischen Suche wie [[bm25|BM25]] und des [[information-retrieval|Information Retrieval]] allgemein.

### Funktionsweise

```text
Dokumente ─► Token ─► (Term, DocID)-Paare ─► nach Term sortieren / gruppieren ─► Wörterbuch + Postings-Listen
                                                                                brutus  → 1, 2, 4, 11, 31 …
                                                                                caesar  → 1, 2, 4, 5, 6 …
Anfrage "brutus AND caesar" ─► beide nachschlagen ─► Postings schneiden ─► 1, 2, 4 …
```

#### 1. Wörterbuch und Postings

Der Index hat zwei Teile: das Wörterbuch der Terme, das auch die Dokumentfrequenz jedes Terms speichert, und für jeden Term eine Postings-Liste der Dokumente, in denen er vorkommt, sortiert nach Dokument-ID. Gebaut wird er, indem alle Term-DocID-Paare gesammelt, nach Term und dann DocID sortiert und die DocIDs jedes Terms zu seiner Postings-Liste zusammengefasst werden (Manning et al., 2008, Kap. 1).

#### 2. Boolesche Anfragen beantworten

Für brutus AND calpurnia schlägt das System beide Terme nach und schneidet ihre Postings-Listen, indem es beide gleichzeitig durchläuft und jeweils den Zeiger mit der kleineren DocID weiterbewegt; bei Listen der Länge x und y braucht das O(x + y) Schritte und setzt voraus, dass alle Listen nach einer globalen Ordnung sortiert sind, etwa der DocID. Bei einem AND über mehrere Terme verarbeitet die Standardheuristik die Terme in aufsteigender Dokumentfrequenz, damit Zwischenergebnisse klein bleiben (Manning et al., 2008, Kap. 1).

#### 3. Skip Pointers

Beim Indexieren gespeicherte Skip Pointers lassen den Schnitt Teile einer Postings-Liste überspringen, die nicht passen können; eine einfache, in der Praxis bewährte Heuristik sind etwa √P gleichmäßig verteilte Sprünge für eine Liste der Länge P. Sie helfen nur bei AND-Anfragen, nicht bei OR-Anfragen, und nur bei den ursprünglichen Listen, nicht bei Zwischenergebnissen (Manning et al., 2008, Kap. 2).

#### 4. Positionsindex

Für Phrasenanfragen speichert ein Positionsindex jedes Posting als DocID mit der Liste der Positionen, an denen der Term vorkommt; das Phrasen-Matching prüft dann, ob Positionen aufeinanderfolgen. Ein Positionsindex ist etwa 2- bis 4-mal so groß wie ein Index ohne Positionen und komprimiert etwa ein Drittel bis halb so groß wie der Rohtext (Manning et al., 2008, Kap. 2).

#### 5. Große Indizes bauen

Passen die Term-DocID-Paare nicht in den Speicher, sortiert das Blocked Sort-Based Indexing (BSBI) die Paare blockweise im Speicher, schreibt den invertierten Index jedes Blocks auf die Festplatte und führt am Ende alle Blöcke zusammen; seine Laufzeit ist Θ(T log T) für T Paare. Single-Pass In-Memory Indexing (SPIMI) fügt Postings direkt in ein Wörterbuch pro Block ein, ohne Paare zu sortieren und ohne Term-IDs, und kann so bei genug Festplattenplatz Sammlungen jeder Größe indexieren. Für Sammlungen im Web-Maßstab verteilt MapReduce die Arbeit: Parser schreiben in der Map-Phase Term-DocID-Paare nach Term-Partition in Segmentdateien, und Inverter bauen in der Reduce-Phase die Postings jeder Partition; ein Master-Knoten vergibt die Arbeit ausgefallener Maschinen neu (Manning et al., 2008, Kap. 4).

#### 6. Sich ändernde Sammlungen

Den ganzen Index periodisch neu zu bauen funktioniert, wenn es wenige Änderungen gibt. Andernfalls kommen neue Dokumente in einen kleinen Hilfsindex im Speicher, der zusammen mit dem Hauptindex durchsucht wird; Löschungen werden in einem Invalidierungs-Bitvektor festgehalten, und Änderungen sind Löschen plus Einfügen. Logarithmic Merging hält eine Folge von Indizes der Größe n, 2n, 4n …, sodass jedes Posting nur einmal pro Ebene zusammengeführt wird, was Θ(T log(T/n)) Bauzeit ergibt, um den Preis, mehrere Indizes abfragen zu müssen (Manning et al., 2008, Kap. 4).

#### 7. Kompression

Das Vokabular wächst mit der Sammlung weiter, wie Heaps' Law M = k·T^b beschreibt (typisch 30 ≤ k ≤ 100 und b ≈ 0,5), und Termhäufigkeiten fallen mit dem Rang ungefähr nach Zipfs Gesetz cf_i ∝ 1/i (Manning et al., 2008, Kap. 5). Postings werden komprimiert, indem statt der IDs die Abstände zwischen aufeinanderfolgenden DocIDs gespeichert werden, weil die Abstände häufiger Terme klein sind. Variable-Byte-Codes nutzen 7 Nutzbits pro Byte plus ein Fortsetzungsbit; γ-Codes schreiben die Länge des binären Offsets unär und dann den Offset und brauchen 2·⌊log2 G⌋ + 1 Bits, höchstens doppelt so viel wie optimal. Für Reuters-RCV1 belegen unkomprimierte 20-Bit-Postings 250 MB, Variable Byte 116 MB und γ-Codes 101 MB; das Wörterbuch schrumpft mit Blockbildung und Front Coding von 11,2 MB auf 5,9 MB (Manning et al., 2008, Kap. 5).

#### Herkunft und Varianten

Die Kapitel des Buchs bauen vom booleschen Retrieval bis zu den Indexstrukturen und Kompressionsverfahren von Suchmaschinen auf (Manning et al., 2008). Dieselbe Idee, ergänzt um Termhäufigkeiten und Gewichte, liegt dem gerankten Retrieval mit tf-idf und BM25 zugrunde ([[information-retrieval|Information Retrieval]]; [[bm25|BM25]]).

### Wann einsetzen

- Für Stichwortsuche in jeder Textsammlung, von der Unternehmenssuche bis zum Sparse-Teil des hybriden [[rag-retrieval|RAG-Retrievals]] ([[bm25|BM25]]).
- Positionsindizes, wenn Phrasenanfragen unterstützt werden müssen (Manning et al., 2008, Kap. 2).
- Verteilter Aufbau mit MapReduce, wenn die Sammlung nicht auf eine Maschine passt (Manning et al., 2008, Kap. 4).

### Stärken und Grenzen

**Stärken**
- Anfragen berühren nur die Postings ihrer Terme, nicht die ganze Sammlung (Manning et al., 2008, Kap. 1).
- Kompression verkleinert die Postings auf deutlich weniger als die Hälfte, sodass mehr vom Index in den Speicher passt (Manning et al., 2008, Kap. 5).
- Der Aufbau skaliert von einer Maschine bis zu Clustern (Manning et al., 2008, Kap. 4).

**Grenzen**
- Häufige Änderungen erfordern Hilfsindizes oder Logarithmic Merging, was Statistiken und Anfrageverarbeitung verkompliziert (Manning et al., 2008, Kap. 4).
- Positionsinformationen machen den Index 2- bis 4-mal größer (Manning et al., 2008, Kap. 2).

### Vergleich

| Struktur | Was sie speichert | Geeignet für |
|----------|-------------------|--------------|
| Inverted Index | Term → sortierte DocIDs (Manning et al., 2008, Kap. 1) | Boolesche und gerankte Stichwortsuche |
| Positionsindex | Term → DocIDs mit Positionen (Manning et al., 2008, Kap. 2) | Phrasen- und Nähesuche |
| Term-Dokument-Inzidenzmatrix | Ein Bit pro Term und Dokument; 40.000 MB für Reuters-RCV1 gegenüber 101 MB γ-kodierter Postings (Manning et al., 2008, Kap. 5) | Nur winzige Sammlungen |
| [[vector-databases\|Vektordatenbank]] | Dichte [[embeddings\|Embeddings]] mit einem Index für Approximate Nearest Neighbor Search | Semantische Ähnlichkeit |

### In der Praxis

Terme werden in aufsteigender Dokumentfrequenz verarbeitet, und für lange, selten geänderte Listen werden Skip Pointers ergänzt (Manning et al., 2008, Kap. 1 und 2). Variable-Byte-Codes bieten einen sehr guten Kompromiss zwischen Zeit und Platz und sind einfach umzusetzen; Codes auf Bitebene wie γ komprimieren besser, wenn Speicherplatz knapp ist (Manning et al., 2008, Kap. 5). Dokument-IDs müssen einer globalen Ordnung folgen, damit Listen in linearer Zeit zusammengeführt werden können (Manning et al., 2008, Kap. 1).

### Merksatz

Ein Inverted Index speichert für jeden Term die sortierte Liste der Dokumente, die ihn enthalten; Anfragen führen diese Listen zusammen, der Aufbau skaliert mit blockweisem oder verteiltem Sortieren, und Gap-Kodierung komprimiert die Postings auf einen Bruchteil des Texts.

### Quellen

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Boolean retrieval.* Introduction to Information Retrieval, Chapter 1. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/01bool.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *The term vocabulary and postings lists.* Introduction to Information Retrieval, Chapter 2. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/02voc.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Index construction.* Introduction to Information Retrieval, Chapter 4. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/04const.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Index compression.* Introduction to Information Retrieval, Chapter 5. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/05comp.pdf)
