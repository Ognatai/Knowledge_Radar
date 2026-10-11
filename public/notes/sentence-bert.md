---
title_en: Sentence-BERT (SBERT)
title_de: Sentence-BERT (SBERT)
entity_type: Method
aliases:
- SBERT
sources:
- https://arxiv.org/abs/1908.10084
- https://arxiv.org/abs/1810.04805
- https://arxiv.org/abs/1905.01969
- https://arxiv.org/abs/2004.04906
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR
Sentence-BERT (SBERT) fine-tunes [[bert|BERT]] (Devlin et al., 2018) in a siamese network so that every sentence gets its own fixed-size embedding, and the similarity of two sentences is the cosine similarity of their embeddings (Reimers & Gurevych, 2019). This makes semantic search and [[clustering|clustering]] feasible: finding the most similar pair among 10,000 sentences took about 65 hours with BERT reading every pair and about 5 seconds with SBERT, with comparable accuracy.

### How it works

```text
sentence A ─▶ BERT ─▶ mean pooling ─▶ u ─┐
                (shared weights)          ├─▶ cosine(u, v)   or   softmax(W · [u, v, |u − v|])
sentence B ─▶ BERT ─▶ mean pooling ─▶ v ─┘
```

#### 1. Siamese network and pooling
Both sentences pass through the same BERT network with tied weights. A pooling layer turns the token vectors into one sentence vector; SBERT tested the [CLS] output, the mean of all token vectors and their maximum, and uses the mean by default (Reimers & Gurevych, 2019).

#### 2. Training objectives
The network is fine-tuned with one of three objectives (Reimers & Gurevych, 2019):
- **[[classification|Classification]]:** u, v and the element-wise difference |u − v| are concatenated and fed to a softmax classifier. SBERT was trained this way on natural language inference data, SNLI (570,000 sentence pairs) and MultiNLI (430,000), labelled contradiction, entailment or neutral.
- **Regression:** the cosine similarity of u and v is trained against a similarity score with mean squared error, as on the STS benchmark.
- **Triplet:** an anchor sentence must be closer to a positive than to a negative sentence by a margin, measured with Euclidean distance.

#### 3. Inference
At inference only the encoder is used: every sentence is embedded once, and similarities are computed between the stored vectors with cosine similarity or Manhattan or Euclidean distance (Reimers & Gurevych, 2019). This is what makes the vectors usable in [[vector-databases|vector databases]] and [[semantic-retrieval|semantic retrieval]].

#### Origin and variants
Reimers & Gurevych (2019) proposed SBERT because BERT, used as a [[cross-encoder|cross-encoder]] that reads both sentences together, computes no independent sentence embeddings and is too slow for comparing many sentences; averaging BERT's token vectors or taking its [CLS] output gave poor sentence embeddings, often worse than averaged GloVe vectors. The same separate-encoding idea is called a bi-encoder (Humeau et al., 2019); Dense Passage Retrieval uses it with two BERT encoders, one for questions and one for passages (Karpukhin et al., 2020). See [[embeddings|Embeddings]] for the wider family of text representations.

### When to use it
- Semantic similarity search over a large collection, where each text is embedded once and stored (Reimers & Gurevych, 2019).
- Clustering of sentences or short texts by meaning (Reimers & Gurevych, 2019).
- As the first stage of retrieval, whose candidates a cross-encoder can re-rank ([[rag-retrieval|RAG: Retrieval]]).
- Measuring the semantic similarity of texts ([[text-similarity-metrics|Text Similarity Metrics]]).

### Strengths and limitations

**Strengths**
- Each sentence is encoded once; comparing 10,000 sentences takes seconds instead of hours (Reimers & Gurevych, 2019).
- On seven semantic textual similarity tasks, SBERT outperformed InferSent by 11.7 points and the Universal Sentence Encoder by 5.5 points (Reimers & Gurevych, 2019).
- Fixed-size vectors can be indexed, cached and clustered (Reimers & Gurevych, 2019).

**Limitations**
- Comparing separate embeddings is less precise than reading both sentences together: a cross-encoder can compare the sentences word by word with attention, while SBERT must compress each sentence into one vector (Reimers & Gurevych, 2019; Humeau et al., 2019).
- Quality depends on the training data: on argument pairs from topics not seen in training, SBERT dropped by about 7 points Spearman correlation (Reimers & Gurevych, 2019).

### Comparison
| Approach | How it differs | Suited for |
|----------|---------------|------------|
| SBERT (bi-encoder) | Each sentence embedded separately, compared by cosine similarity (Reimers & Gurevych, 2019) | Search, clustering, large collections |
| [[cross-encoder\|Cross-encoder]] (BERT on the pair) | Reads both sentences together; more accurate, one model pass per pair (Reimers & Gurevych, 2019) | Re-ranking a short candidate list |
| Averaged BERT token vectors / [CLS] | No fine-tuning for similarity; often worse than averaged GloVe vectors (Reimers & Gurevych, 2019) | Not recommended for sentence similarity |
| Dense Passage Retrieval | Two separate BERT encoders for questions and passages, trained for retrieval (Karpukhin et al., 2020) | Open-domain question answering |

### In practice
A common pipeline embeds all documents once with a bi-encoder such as SBERT, stores the vectors in a [[vector-databases|vector database]], retrieves the nearest neighbours of a query and re-ranks them with a [[cross-encoder|cross-encoder]] ([[rag-retrieval|RAG: Retrieval]]). Because quality drops on topics unlike the training data, the model should be evaluated on queries from the target domain ([[rag-retrieval-evaluation|RAG: Retrieval Evaluation]]). Embedding similarity measures closeness in meaning as learnt from the training data, not factual agreement ([[text-similarity-metrics|Text Similarity Metrics]]).

### Key takeaway
Sentence-BERT turns BERT into an encoder that gives every sentence its own vector, trading a little accuracy against a cross-encoder for search that scales from hours to seconds.

### Sources
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL 2019. [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- Humeau, S., Shuster, K., Lachaux, M.-A. & Weston, J. (2019). *Poly-encoders: Architectures and Pre-training Strategies for Fast and Accurate Multi-sentence Scoring.* ICLR 2020. [arXiv:1905.01969](https://arxiv.org/abs/1905.01969)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Basis der angegebenen Quellen; sie kann unvollständig, veraltet oder fehlerhaft sein.

### TL;DR
Sentence-BERT (SBERT) justiert [[bert|BERT]] (Devlin et al., 2018) in einem siamesischen Netz so nach, dass jeder Satz ein eigenes Embedding fester Größe erhält; die Ähnlichkeit zweier Sätze ist die Kosinus-Ähnlichkeit ihrer Embeddings (Reimers & Gurevych, 2019). Damit werden semantische Suche und [[clustering|Clustering]] praktikabel: Das ähnlichste Paar unter 10.000 Sätzen zu finden, dauerte mit BERT, das jedes Paar liest, etwa 65 Stunden, mit SBERT etwa 5 Sekunden, bei vergleichbarer Genauigkeit.

### Funktionsweise

```text
Satz A ─▶ BERT ─▶ Mean Pooling ─▶ u ─┐
           (gemeinsame Gewichte)      ├─▶ cos(u, v)   oder   softmax(W · [u, v, |u − v|])
Satz B ─▶ BERT ─▶ Mean Pooling ─▶ v ─┘
```

#### 1. Siamesisches Netz und Pooling
Beide Sätze laufen durch dasselbe BERT-Netz mit geteilten Gewichten. Eine Pooling-Schicht macht aus den Token-Vektoren einen Satzvektor; SBERT testete die [CLS]-Ausgabe, den Mittelwert aller Token-Vektoren und deren Maximum und verwendet standardmäßig den Mittelwert (Reimers & Gurevych, 2019).

#### 2. Trainingsziele
Das Netz wird mit einem von drei Zielen feinjustiert (Reimers & Gurevych, 2019):
- **[[classification|Klassifikation]]:** u, v und die elementweise Differenz |u − v| werden verbunden und in einen Softmax-Klassifikator gegeben. So wurde SBERT auf Daten zur natürlichsprachlichen Inferenz trainiert, SNLI (570.000 Satzpaare) und MultiNLI (430.000), gelabelt als Widerspruch, Folgerung oder neutral.
- **Regression:** Die Kosinus-Ähnlichkeit von u und v wird mit mittlerem quadratischem Fehler gegen einen Ähnlichkeitswert trainiert, etwa auf dem STS-Benchmark.
- **Triplet:** Ein Ankersatz muss einem positiven Satz um einen Mindestabstand näher sein als einem negativen, gemessen mit euklidischer Distanz.

#### 3. Inferenz
Bei der Inferenz wird nur der Encoder genutzt: Jeder Satz wird einmal eingebettet, und Ähnlichkeiten werden zwischen den gespeicherten Vektoren per Kosinus-Ähnlichkeit oder Manhattan- bzw. euklidischer Distanz berechnet (Reimers & Gurevych, 2019). Dadurch lassen sich die Vektoren in [[vector-databases|Vektordatenbanken]] und für [[semantic-retrieval|semantisches Retrieval]] nutzen.

#### Ursprung und Varianten
Reimers & Gurevych (2019) schlugen SBERT vor, weil BERT als [[cross-encoder|Cross-Encoder]], der beide Sätze gemeinsam liest, keine eigenständigen Satz-Embeddings berechnet und für den Vergleich vieler Sätze zu langsam ist; gemittelte Token-Vektoren von BERT oder seine [CLS]-Ausgabe ergaben schlechte Satz-Embeddings, oft schlechter als gemittelte GloVe-Vektoren. Dieselbe Idee der getrennten Kodierung heißt Bi-Encoder (Humeau et al., 2019); Dense Passage Retrieval nutzt sie mit zwei BERT-Encodern, einem für Fragen und einem für Passagen (Karpukhin et al., 2020). Zur größeren Familie der Textrepräsentationen siehe [[embeddings|Embeddings]].

### Wann einsetzen
- Semantische Ähnlichkeitssuche in einer großen Sammlung, in der jeder Text einmal eingebettet und gespeichert wird (Reimers & Gurevych, 2019).
- Clustering von Sätzen oder kurzen Texten nach Bedeutung (Reimers & Gurevych, 2019).
- Als erste Retrieval-Stufe, deren Kandidaten ein Cross-Encoder neu sortieren kann ([[rag-retrieval|RAG: Retrieval]]).
- Messung der semantischen Ähnlichkeit von Texten ([[text-similarity-metrics|Textähnlichkeitsmetriken]]).

### Stärken und Grenzen

**Stärken**
- Jeder Satz wird einmal kodiert; der Vergleich von 10.000 Sätzen dauert Sekunden statt Stunden (Reimers & Gurevych, 2019).
- Auf sieben Aufgaben zur semantischen Textähnlichkeit übertraf SBERT InferSent um 11,7 Punkte und den Universal Sentence Encoder um 5,5 Punkte (Reimers & Gurevych, 2019).
- Vektoren fester Größe lassen sich indexieren, zwischenspeichern und clustern (Reimers & Gurevych, 2019).

**Grenzen**
- Getrennte Embeddings zu vergleichen, ist ungenauer, als beide Sätze gemeinsam zu lesen: Ein Cross-Encoder kann die Sätze per Attention Wort für Wort vergleichen, SBERT muss jeden Satz in einen Vektor verdichten (Reimers & Gurevych, 2019; Humeau et al., 2019).
- Die Qualität hängt von den Trainingsdaten ab: Bei Argumentpaaren zu Themen, die im Training nicht vorkamen, sank SBERT um etwa 7 Punkte Spearman-Korrelation (Reimers & Gurevych, 2019).

### Vergleich
| Ansatz | Unterschied | Geeignet für |
|--------|-------------|--------------|
| SBERT (Bi-Encoder) | Jeder Satz einzeln eingebettet, Vergleich per Kosinus-Ähnlichkeit (Reimers & Gurevych, 2019) | Suche, Clustering, große Sammlungen |
| [[cross-encoder\|Cross-Encoder]] (BERT auf dem Paar) | Liest beide Sätze gemeinsam; genauer, ein Modelldurchlauf pro Paar (Reimers & Gurevych, 2019) | Re-Ranking einer kurzen Kandidatenliste |
| Gemittelte BERT-Token-Vektoren / [CLS] | Kein Fine-Tuning auf Ähnlichkeit; oft schlechter als gemittelte GloVe-Vektoren (Reimers & Gurevych, 2019) | Für Satzähnlichkeit nicht zu empfehlen |
| Dense Passage Retrieval | Zwei getrennte BERT-Encoder für Fragen und Passagen, auf Retrieval trainiert (Karpukhin et al., 2020) | Open-Domain-Question-Answering |

### In der Praxis
Eine verbreitete Pipeline bettet alle Dokumente einmal mit einem Bi-Encoder wie SBERT ein, speichert die Vektoren in einer [[vector-databases|Vektordatenbank]], holt die nächsten Nachbarn einer Anfrage und sortiert sie mit einem [[cross-encoder|Cross-Encoder]] neu ([[rag-retrieval|RAG: Retrieval]]). Weil die Qualität bei Themen abseits der Trainingsdaten sinkt, sollte das Modell mit Anfragen aus der Zieldomäne evaluiert werden ([[rag-retrieval-evaluation|RAG: Retrieval-Evaluation]]). Embedding-Ähnlichkeit misst inhaltliche Nähe, wie sie aus den Trainingsdaten gelernt wurde, nicht sachliche Übereinstimmung ([[text-similarity-metrics|Textähnlichkeitsmetriken]]).

### Merksatz
Sentence-BERT macht aus BERT einen Encoder, der jedem Satz einen eigenen Vektor gibt, und tauscht etwas Genauigkeit gegenüber einem Cross-Encoder gegen eine Suche, die von Stunden auf Sekunden schrumpft.

### Quellen
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL 2019. [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- Humeau, S., Shuster, K., Lachaux, M.-A. & Weston, J. (2019). *Poly-encoders: Architectures and Pre-training Strategies for Fast and Accurate Multi-sentence Scoring.* ICLR 2020. [arXiv:1905.01969](https://arxiv.org/abs/1905.01969)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
