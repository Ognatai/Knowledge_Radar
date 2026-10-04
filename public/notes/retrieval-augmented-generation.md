---
title_en: Retrieval-Augmented Generation
title_de: Retrieval-Augmented Generation
entity_type: Method
aliases: [RAG]
sources:
  - https://arxiv.org/abs/2005.11401
  - https://arxiv.org/abs/2312.10997
  - https://arxiv.org/abs/1908.10084
  - https://arxiv.org/abs/1603.09320
  - https://arxiv.org/abs/1702.08734
  - https://doi.org/10.1561/1500000019
  - https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
  - https://arxiv.org/abs/1901.04085
  - https://arxiv.org/abs/2004.04906
  - https://arxiv.org/abs/2307.03172
  - https://arxiv.org/abs/2309.15217
  - https://arxiv.org/abs/2312.05934
  - https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Retrieval-Augmented Generation (RAG) combines a generative [[large-language-models|language model]] with an external knowledge source. At query time, a retriever searches the knowledge source for passages relevant to the input, and the model generates its answer conditioned on both the input and the retrieved passages. RAG lets a model use knowledge that is current, domain-specific or citable without storing it in the model weights.

### How it works

A RAG system has two phases. **Indexing** runs offline: documents are split into chunks, converted into searchable representations and stored in indexes. **Querying** runs for every request: the query is converted in the same way, matched against the indexes, and the best passages are placed into the prompt of the language model.

```text
INDEXING (offline)
documents
 ▼
1 chunking ─┬─▶ 2 embedding model ─▶ 3 vector index (ANN)
            └─▶ tokenisation ──────▶ 3 inverted index (BM25)

QUERYING (per request)
query
 ▼
4 query processing ─┬─▶ embedding ─▶ 5 ANN search (vector index)
                    └─▶ terms ─────▶ 5 BM25 search (inverted index)
 ▼
5 fusion of both result lists (RRF)
 ▼
6 reranking (cross-encoder)
 ▼
7 context construction ─▶ prompt
 ▼
8 LLM ─▶ answer + citations
```

#### 1. Chunking

Documents are split into passages (chunks) that are small enough to be matched precisely and to fit several of them into the prompt, but large enough to carry a self-contained statement. Common strategies:

- **Fixed size**: a fixed number of tokens per chunk, with an overlap between neighbouring chunks so that a sentence on a boundary is not lost.
- **Structure-based**: splitting along headings, paragraphs, list items or (for law) articles and paragraphs.
- **Semantic**: starting a new chunk where the topic changes, e.g. where the embedding similarity between consecutive sentences drops.

Each chunk keeps metadata (document, section, page, date, access rights) that is later used for filtering and for citations. Details: [[rag-chunking|RAG: chunking]].

#### 2. Embedding

An [[embeddings|embedding model]] maps each chunk to a vector of fixed dimension (typically a few hundred to a few thousand numbers), such that passages with similar meaning lie close together. RAG uses **bi-encoders**: query and passage are encoded independently by the same model. This is what makes retrieval over large collections feasible: all passage vectors are computed once in advance, and a query needs a single encoder call plus a vector comparison. Reimers & Gurevych (2019) illustrate the difference: finding the most similar pair among 10,000 sentences takes about 65 hours when every pair is fed through BERT jointly, and about 5 seconds with precomputed sentence embeddings (SBERT). Query and passages must be embedded with the same model, otherwise their vectors are not comparable.

#### 3. Indexing

The vectors are stored in a [[vector-databases|vector database]] or a vector index. Comparing a query with every stored vector (exact nearest-neighbour search) costs time proportional to the number of vectors and becomes too slow for large collections. Vector indexes therefore use **approximate nearest-neighbour (ANN)** search, which trades a small loss in recall for a large gain in speed:

- **HNSW** (Malkov & Yashunin, 2016) builds a hierarchy of proximity graphs. Each vector is inserted into the bottom layer and, with exponentially decreasing probability, into higher layers. A search starts in the sparse top layer, moves greedily towards the query and descends layer by layer; search effort grows roughly logarithmically with collection size.
- **Inverted-file and quantisation methods**, as implemented in FAISS (Johnson et al., 2017), partition the vector space into clusters and compress vectors (product quantisation), so that only a few clusters are searched and billions of vectors fit into memory.

For lexical search, the chunks are additionally tokenised into an **inverted index** that maps each term to the chunks containing it.

#### 4. Query processing

The user's query is prepared before retrieval: conversational context is resolved ("and what about Article 6?" becomes a standalone question), the query can be rewritten or expanded with synonyms, or split into sub-questions. Metadata filters (e.g. document type, date, permissions) are derived from the request.

#### 5. Retrieval

The prepared query is matched against the indexes ([[rag-retrieval|RAG: retrieval]]):

- **Dense retrieval** embeds the query with the same model as the chunks and retrieves the *k* nearest vectors from the ANN index. Closeness is usually measured by cosine similarity, `cos(q, d) = (q · d) / (‖q‖ · ‖d‖)`, or by the inner product on normalised vectors. Dense retrieval finds passages that match the meaning even without shared words. Karpukhin et al. (2020) showed that a learned dense retriever outperformed a BM25 baseline by 9–19 percentage points in top-20 passage retrieval accuracy on open-domain question answering.
- **Sparse retrieval** with **BM25** (Robertson & Zaragoza, 2009) scores chunks by the query terms they contain: rare terms weigh more (inverse document frequency), repeated occurrences add less and less (term-frequency saturation), and long chunks are normalised. BM25 is strong on exact terms such as names, article numbers or error codes, where embeddings are often imprecise.
- **Hybrid retrieval** runs both and merges the result lists. A common method is **Reciprocal Rank Fusion** (Cormack et al., 2009): each passage receives `RRF(d) = Σ 1 / (k + rank_r(d))` summed over all result lists *r*, with *k* = 60 in the original paper. RRF needs only ranks, not scores, so the incompatible score scales of BM25 and cosine similarity do not matter.

#### 6. Reranking

The candidates from step 5 (often a few dozen to a few hundred) are re-scored by a **cross-encoder**. Unlike the bi-encoder, it reads query and passage *together*: Nogueira & Cho (2019) feed the query and the passage jointly into BERT and turn the output of the `[CLS]` token into the probability that the passage is relevant. This is considerably more accurate but too expensive to apply to the whole collection, hence the two stages: fast retrieval for recall, slow reranking for precision.

#### 7. Context construction

The top *n* passages after reranking are assembled into the prompt. This step decides about duplicates, the order of passages, the token budget of the context window and the source identifiers the model should cite. Order matters: models use information at the beginning or end of a long context best and information in the middle markedly worse (Liu et al., 2023). The prompt usually instructs the model to answer only from the given passages, to cite them and to say when they do not contain the answer.

#### 8. Generation

The language model generates the answer from the prompt. Optionally, a post-processing step checks that every citation exists and supports the statement it is attached to, or triggers a further retrieval round if the passages were insufficient.

#### Origin and variants

The term goes back to Lewis et al. (2020). Their model combines a *parametric memory* (a pre-trained sequence-to-sequence model) with a *non-parametric memory* (a dense vector index of Wikipedia), trains retriever and generator jointly, and comes in two variants: **RAG-Sequence** uses the same retrieved passages for the whole output, **RAG-Token** may draw on different passages for each generated token. Today, RAG mostly denotes the pipeline above around an unchanged LLM. Gao et al. (2023) describe three stages of development: **Naive RAG** (index, retrieve, generate), **Advanced RAG** (added query processing, reranking and context compression) and **Modular RAG** (interchangeable modules and flexible control flows, e.g. iterative or agent-driven retrieval, see [[agentic-ai|Agentic AI]]).

### When to use it

- The answers depend on knowledge that changes frequently or is newer than the model's training data.
- The knowledge is internal or domain-specific (manuals, contracts, regulations).
- Answers must be traceable to sources.
- Knowledge must be updated or deleted without retraining the model.

### Strengths and limitations

**Strengths**

- The knowledge base can be updated independently of the model.
- Answers can cite the passages they are based on.
- Hallucinations can be reduced, because the model is grounded in retrieved text.
- No training is required to add knowledge.

**Limitations**

- Answer quality is bounded by retrieval quality: information that is not retrieved cannot be used.
- Irrelevant or contradictory passages can degrade the answer.
- RAG reduces hallucinations but does not prevent them; the model can still misread or ignore sources.
- Every query pays for retrieval, reranking and longer prompts in latency and cost.
- Each pipeline step (chunking, embedding model, *k*, fusion, reranker, prompt) is a parameter that has to be tuned and evaluated.

### Comparison

| Approach | Changes | Suited for |
| --- | --- | --- |
| RAG | the context at inference time | current, citable, frequently changing knowledge |
| Fine-tuning | the model weights | behaviour, style, task format |
| Long-context prompting | the context, without retrieval | small, fixed document sets |
| [[graphrag\|GraphRAG]] | retrieval over a knowledge graph | questions spanning relations between entities |

For injecting factual knowledge, Ovadia et al. (2023) found that RAG consistently outperformed unsupervised fine-tuning, both for knowledge seen during pre-training and for entirely new knowledge. The two approaches can be combined; see [[rag-vs-fine-tuning|RAG vs. fine-tuning]].

### In practice

- **Evaluate retrieval and generation separately** ([[rag-evaluation|RAG evaluation]]). Retrieval is measured with ranking metrics such as Recall@k or nDCG ([[rag-retrieval-evaluation|retrieval evaluation]]); generation with criteria such as faithfulness to the retrieved passages and answer relevance ([[rag-generation-evaluation|generation evaluation]]). Frameworks such as RAGAS (Es et al., 2023) compute such metrics without human reference answers, typically using an [[llm-as-a-judge|LLM as a judge]].
- **Typical failure modes** ([[rag-failure-modes|RAG failure modes]]) map onto the pipeline: the relevant passage was split badly (step 1), not retrieved (step 5), ranked below the cut-off (steps 5–6), crowded out of the context (step 7), or the model cites a source that does not support its statement (step 8).

### Regulatory context

The [[gdpr|GDPR]] gives data subjects a right to erasure (Art. 17). Personal data held in a retrieval index can be deleted or corrected there directly, whereas data absorbed into model weights during training cannot be removed selectively without retraining or dedicated unlearning methods.

### Key takeaway

RAG gives a language model access to an external, updatable knowledge base at query time; its answers can only be as good as the passages it retrieves.

### Sources

- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
- Gao, Y. et al. (2023). *Retrieval-Augmented Generation for Large Language Models: A Survey.* [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Malkov, Y. A. & Yashunin, D. A. (2016). *Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs.* [arXiv:1603.09320](https://arxiv.org/abs/1603.09320)
- Johnson, J., Douze, M. & Jégou, H. (2017). *Billion-scale similarity search with GPUs.* [arXiv:1702.08734](https://arxiv.org/abs/1702.08734)
- Robertson, S. & Zaragoza, H. (2009). *The Probabilistic Relevance Framework: BM25 and Beyond.* Foundations and Trends in Information Retrieval. [doi:10.1561/1500000019](https://doi.org/10.1561/1500000019)
- Cormack, G. V., Clarke, C. L. A. & Büttcher, S. (2009). *Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods.* SIGIR 2009. [PDF](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- Nogueira, R. & Cho, K. (2019). *Passage Re-ranking with BERT.* [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Es, S. et al. (2023). *Ragas: Automated Evaluation of Retrieval Augmented Generation.* [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- Ovadia, O. et al. (2023). *Fine-Tuning or Retrieval? Comparing Knowledge Injection in LLMs.* [arXiv:2312.05934](https://arxiv.org/abs/2312.05934)
- Regulation (EU) 2016/679 (GDPR), Art. 17. [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Retrieval-Augmented Generation (RAG) verbindet ein generatives [[large-language-models|Sprachmodell]] mit einer externen Wissensquelle. Zur Laufzeit sucht ein Retriever in dieser Quelle nach Textpassagen, die zur Eingabe passen, und das Modell erzeugt seine Antwort auf Basis der Eingabe und der gefundenen Passagen. So kann ein Modell aktuelles, fachspezifisches oder zitierbares Wissen nutzen, ohne es in seinen Gewichten zu speichern.

### Funktionsweise

Ein RAG-System hat zwei Phasen. Die **Indexierung** läuft offline: Dokumente werden in Chunks zerlegt, in durchsuchbare Darstellungen umgewandelt und in Indizes abgelegt. Die **Anfrage** läuft bei jedem Request: Die Query wird auf dieselbe Weise umgewandelt, gegen die Indizes abgeglichen, und die besten Passagen landen im Prompt des Sprachmodells.

```text
INDEXIERUNG (offline)
Dokumente
 ▼
1 Chunking ─┬─▶ 2 Embedding-Modell ─▶ 3 Vektorindex (ANN)
            └─▶ Tokenisierung ──────▶ 3 Inverted Index (BM25)

ANFRAGE (pro Request)
Query
 ▼
4 Query Processing ─┬─▶ Embedding ─▶ 5 ANN-Suche (Vektorindex)
                    └─▶ Terme ─────▶ 5 BM25-Suche (Inverted Index)
 ▼
5 Fusion beider Ergebnislisten (RRF)
 ▼
6 Reranking (Cross-Encoder)
 ▼
7 Context Construction ─▶ Prompt
 ▼
8 LLM ─▶ Antwort + Quellenangaben
```

#### 1. Chunking

Dokumente werden in Passagen (Chunks) zerlegt, die klein genug sind, um präzise gefunden zu werden und zu mehreren in den Prompt zu passen, aber groß genug, um eine in sich verständliche Aussage zu tragen. Übliche Strategien:

- **Feste Größe**: eine feste Anzahl Tokens pro Chunk, mit Überlappung zwischen benachbarten Chunks, damit ein Satz an der Grenze nicht verloren geht.
- **Strukturbasiert**: Zerlegung entlang von Überschriften, Absätzen, Listenpunkten oder (bei Gesetzen) Artikeln und Absätzen.
- **Semantisch**: Ein neuer Chunk beginnt dort, wo das Thema wechselt, z. B. wo die Embedding-Ähnlichkeit aufeinanderfolgender Sätze abfällt.

Jeder Chunk behält Metadaten (Dokument, Abschnitt, Seite, Datum, Zugriffsrechte), die später zum Filtern und für Quellenangaben genutzt werden. Details: [[rag-chunking|RAG: Chunking]].

#### 2. Embedding

Ein [[embeddings|Embedding-Modell]] bildet jeden Chunk auf einen Vektor fester Länge ab (typischerweise einige hundert bis einige tausend Zahlen), sodass bedeutungsähnliche Passagen nah beieinander liegen. RAG nutzt **Bi-Encoder**: Query und Passage werden unabhängig voneinander vom selben Modell kodiert. Erst das macht die Suche in großen Sammlungen praktikabel: Alle Passagenvektoren werden einmal im Voraus berechnet, und eine Query braucht nur einen Encoder-Aufruf plus einen Vektorvergleich. Reimers & Gurevych (2019) veranschaulichen den Unterschied: Das ähnlichste Paar unter 10.000 Sätzen zu finden, dauert etwa 65 Stunden, wenn jedes Paar gemeinsam durch BERT geschickt wird, und etwa 5 Sekunden mit vorab berechneten Satz-Embeddings (SBERT). Query und Passagen müssen mit demselben Modell eingebettet werden, sonst sind ihre Vektoren nicht vergleichbar.

#### 3. Indexierung

Die Vektoren werden in einer [[vector-databases|Vektordatenbank]] oder einem Vektorindex gespeichert. Eine Query mit jedem gespeicherten Vektor zu vergleichen (exakte Nearest Neighbor Search), kostet Zeit proportional zur Anzahl der Vektoren und wird für große Sammlungen zu langsam. Vektorindizes nutzen deshalb **Approximate Nearest Neighbor Search (ANN)**, die einen kleinen Verlust an Recall gegen einen großen Geschwindigkeitsgewinn eintauscht:

- **HNSW** (Malkov & Yashunin, 2016) baut eine Hierarchie von Proximity Graphs auf. Jeder Vektor wird in die unterste Ebene und mit exponentiell abnehmender Wahrscheinlichkeit auch in höhere Ebenen eingefügt. Eine Suche beginnt in der dünn besetzten obersten Ebene, nähert sich per Greedy Search der Query und steigt Ebene für Ebene ab; der Suchaufwand wächst ungefähr logarithmisch mit der Größe der Sammlung.
- **Inverted-File- und Quantisierungsverfahren**, wie sie FAISS (Johnson et al., 2017) umsetzt, teilen den Vektorraum in Cluster auf und komprimieren die Vektoren (Product Quantization), sodass nur wenige Cluster durchsucht werden müssen und Milliarden Vektoren in den Speicher passen.

Für die lexikalische Suche werden die Chunks zusätzlich tokenisiert und in einem **Inverted Index** abgelegt, der jedem Term die Chunks zuordnet, in denen er vorkommt.

#### 4. Query Processing

Die Anfrage wird vor dem Retrieval aufbereitet: Gesprächskontext wird aufgelöst („und was ist mit Artikel 6?“ wird zu einer eigenständigen Frage), die Query kann umformuliert, um Synonyme erweitert oder in Teilfragen zerlegt werden. Aus der Anfrage werden Metadatenfilter abgeleitet (z. B. Dokumenttyp, Datum, Berechtigungen).

#### 5. Retrieval

Die aufbereitete Query wird gegen die Indizes abgeglichen ([[rag-retrieval|RAG: Retrieval]]):

- **Dense Retrieval** bettet die Query mit demselben Modell ein wie die Chunks und holt die *k* nächsten Vektoren aus dem ANN-Index. Die Nähe wird meist mit der Cosine Similarity gemessen, `cos(q, d) = (q · d) / (‖q‖ · ‖d‖)`, oder mit dem Inner Product normierter Vektoren. Dense Retrieval findet Passagen, die inhaltlich passen, auch ohne gemeinsame Wörter. Karpukhin et al. (2020) zeigten, dass ein gelernter Dense Retriever eine BM25-Baseline bei der Top-20 Retrieval Accuracy für Passagen im Open-Domain-Question-Answering um 9 bis 19 Prozentpunkte übertraf.
- **Sparse Retrieval** mit **BM25** (Robertson & Zaragoza, 2009) bewertet Chunks nach den Query-Termen, die sie enthalten: Seltene Terme wiegen mehr (Inverse Document Frequency), wiederholtes Vorkommen bringt immer weniger hinzu (Term Frequency Saturation), und lange Chunks werden normalisiert. BM25 ist stark bei exakten Begriffen wie Namen, Artikelnummern oder Fehlercodes, bei denen Embeddings oft unscharf sind.
- **Hybrid Retrieval** führt beide Suchen aus und verschmilzt die Ergebnislisten. Ein verbreitetes Verfahren ist **Reciprocal Rank Fusion** (Cormack et al., 2009): Jede Passage erhält `RRF(d) = Σ 1 / (k + rang_r(d))`, summiert über alle Ergebnislisten *r*, mit *k* = 60 im Originalpaper. RRF braucht nur Ränge, keine Scores; die unvereinbaren Skalen von BM25 und Cosine Similarity spielen daher keine Rolle.

#### 6. Reranking

Die Kandidaten aus Schritt 5 (oft einige Dutzend bis einige hundert) werden von einem **Cross-Encoder** neu bewertet. Anders als der Bi-Encoder liest er Query und Passage *gemeinsam*: Nogueira & Cho (2019) geben Query und Passage zusammen in BERT und machen aus der Ausgabe des `[CLS]`-Tokens die Wahrscheinlichkeit, dass die Passage relevant ist. Das ist deutlich genauer, aber zu teuer für die gesamte Sammlung; daher die zwei Stufen: schnelles Retrieval für den Recall, langsames Reranking für die Precision.

#### 7. Context Construction

Die besten *n* Passagen nach dem Reranking werden zum Prompt zusammengesetzt. Dieser Schritt entscheidet über Duplikate, die Reihenfolge der Passagen, das Token-Budget des Kontextfensters und die Quellenkennungen, die das Modell zitieren soll. Die Reihenfolge zählt: Informationen am Anfang oder Ende eines langen Kontexts verwerten Modelle am besten, Informationen in der Mitte deutlich schlechter (Liu et al., 2023). Der Prompt weist das Modell meist an, nur aus den gegebenen Passagen zu antworten, sie zu zitieren und zu sagen, wenn sie die Antwort nicht enthalten.

#### 8. Generierung

Das Sprachmodell erzeugt die Antwort aus dem Prompt. Optional prüft ein Nachverarbeitungsschritt, ob jede Quellenangabe existiert und die zugehörige Aussage stützt, oder löst eine weitere Retrieval-Runde aus, wenn die Passagen nicht ausreichten.

#### Ursprung und Varianten

Der Begriff geht auf Lewis et al. (2020) zurück. Ihr Modell verbindet ein *Parametric Memory* (ein vortrainiertes Sequence-to-Sequence-Modell) mit einem *Non-Parametric Memory* (einem Dense Vector Index über Wikipedia), trainiert Retriever und Generator gemeinsam und existiert in zwei Varianten: **RAG-Sequence** verwendet für die gesamte Ausgabe dieselben Passagen, **RAG-Token** kann für jedes erzeugte Token auf andere Passagen zurückgreifen. Heute bezeichnet RAG meist die oben beschriebene Pipeline um ein unverändertes LLM. Gao et al. (2023) beschreiben drei Entwicklungsstufen: **Naive RAG** (indexieren, abrufen, generieren), **Advanced RAG** (zusätzlich Query Processing, Reranking und Context Compression) und **Modular RAG** (austauschbare Module und flexible Abläufe, z. B. iteratives oder agentengesteuertes Retrieval, siehe [[agentic-ai|Agentic AI]]).

### Wann einsetzen

- Die Antworten hängen von Wissen ab, das sich häufig ändert oder neuer ist als die Trainingsdaten des Modells.
- Das Wissen ist intern oder fachspezifisch (Handbücher, Verträge, Regulierung).
- Antworten müssen auf Quellen zurückführbar sein.
- Wissen muss aktualisiert oder gelöscht werden können, ohne das Modell neu zu trainieren.

### Stärken und Grenzen

**Stärken**

- Die Wissensbasis lässt sich unabhängig vom Modell aktualisieren.
- Antworten können die Passagen zitieren, auf denen sie beruhen.
- Halluzinationen lassen sich verringern, weil das Modell auf abgerufenem Text aufbaut.
- Für neues Wissen ist kein Training nötig.

**Grenzen**

- Die Antwortqualität ist durch die Retrieval-Qualität begrenzt: Was nicht gefunden wird, kann nicht genutzt werden.
- Irrelevante oder widersprüchliche Passagen können die Antwort verschlechtern.
- RAG verringert Halluzinationen, verhindert sie aber nicht; das Modell kann Quellen weiterhin falsch lesen oder ignorieren.
- Jede Anfrage kostet durch Retrieval, Reranking und längere Prompts zusätzliche Latenz und Kosten.
- Jeder Pipeline-Schritt (Chunking, Embedding-Modell, *k*, Fusion, Reranker, Prompt) ist ein Parameter, der abgestimmt und evaluiert werden muss.

### Vergleich

| Ansatz | Verändert | Geeignet für |
| --- | --- | --- |
| RAG | den Kontext zur Laufzeit | aktuelles, zitierbares, häufig wechselndes Wissen |
| Fine-Tuning | die Modellgewichte | Verhalten, Stil, Aufgabenformat |
| Long-Context-Prompting | den Kontext, ohne Retrieval | kleine, feste Dokumentmengen |
| [[graphrag\|GraphRAG]] | Retrieval über einen Wissensgraphen | Fragen über Beziehungen zwischen Entitäten |

Für das Einbringen von Faktenwissen stellten Ovadia et al. (2023) fest, dass RAG unüberwachtes Fine-Tuning durchgängig übertraf, sowohl bei Wissen aus dem Pretraining als auch bei völlig neuem Wissen. Beide Ansätze lassen sich kombinieren; siehe [[rag-vs-fine-tuning|RAG vs. Fine-Tuning]].

### In der Praxis

- **Retrieval und Generierung getrennt evaluieren** ([[rag-evaluation|RAG-Evaluation]]). Das Retrieval wird mit Ranking-Metriken wie Recall@k oder nDCG gemessen ([[rag-retrieval-evaluation|Evaluation des Retrievals]]), die Generierung mit Kriterien wie Faithfulness gegenüber den abgerufenen Passagen und Answer Relevance ([[rag-generation-evaluation|Evaluation der Generierung]]). Frameworks wie RAGAS (Es et al., 2023) berechnen solche Metriken ohne menschliche Referenzantworten, typischerweise mit einem [[llm-as-a-judge|LLM als Bewerter]].
- **Typische Fehlerarten** ([[rag-failure-modes|RAG-Fehlerarten]]) lassen sich den Pipeline-Schritten zuordnen: Die relevante Passage wurde ungünstig zerlegt (Schritt 1), nicht gefunden (Schritt 5), unterhalb des Schnitts eingeordnet (Schritte 5–6), aus dem Kontext verdrängt (Schritt 7), oder das Modell zitiert eine Quelle, die seine Aussage nicht stützt (Schritt 8).

### Regulatorischer Kontext

Die [[gdpr|DSGVO]] gibt betroffenen Personen ein Recht auf Löschung (Art. 17). Personenbezogene Daten in einem Retrieval-Index lassen sich dort direkt löschen oder berichtigen, während Daten, die beim Training in die Modellgewichte eingeflossen sind, ohne erneutes Training oder spezielle Unlearning-Verfahren nicht gezielt entfernt werden können.

### Merksatz

RAG gibt einem Sprachmodell zur Laufzeit Zugriff auf eine externe, aktualisierbare Wissensbasis; seine Antworten sind nur so gut wie die Passagen, die es findet.

### Quellen

- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
- Gao, Y. et al. (2023). *Retrieval-Augmented Generation for Large Language Models: A Survey.* [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Malkov, Y. A. & Yashunin, D. A. (2016). *Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs.* [arXiv:1603.09320](https://arxiv.org/abs/1603.09320)
- Johnson, J., Douze, M. & Jégou, H. (2017). *Billion-scale similarity search with GPUs.* [arXiv:1702.08734](https://arxiv.org/abs/1702.08734)
- Robertson, S. & Zaragoza, H. (2009). *The Probabilistic Relevance Framework: BM25 and Beyond.* Foundations and Trends in Information Retrieval. [doi:10.1561/1500000019](https://doi.org/10.1561/1500000019)
- Cormack, G. V., Clarke, C. L. A. & Büttcher, S. (2009). *Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods.* SIGIR 2009. [PDF](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- Nogueira, R. & Cho, K. (2019). *Passage Re-ranking with BERT.* [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Es, S. et al. (2023). *Ragas: Automated Evaluation of Retrieval Augmented Generation.* [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- Ovadia, O. et al. (2023). *Fine-Tuning or Retrieval? Comparing Knowledge Injection in LLMs.* [arXiv:2312.05934](https://arxiv.org/abs/2312.05934)
- Verordnung (EU) 2016/679 (DSGVO), Art. 17. [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj/deu)
