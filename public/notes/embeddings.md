---
title_en: Embeddings
title_de: Embeddings
entity_type: Concept
sources:
- https://arxiv.org/abs/1301.3781
- https://arxiv.org/abs/1810.04805
- https://arxiv.org/abs/1908.10084
- https://arxiv.org/abs/2210.07316
- https://arxiv.org/abs/2205.13147
- https://aclanthology.org/D14-1162/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Embeddings are dense vector representations of text that encode semantic similarity, enabling retrieval systems to find relevant documents based on contextual meaning rather than exact keyword matches. This approach overcomes the limitations of lexical search by mapping semantically similar text to nearby points in a high-dimensional space, as fundamental to modern information retrieval [[information-retrieval|Information Retrieval]].

### How it works

A text embedding model turns a text into one dense vector: the text is tokenized, encoded into contextual token vectors by a Transformer, and pooled into a single vector. The model is trained so that texts with similar meaning get similar vectors (Reimers & Gurevych, 2019); at search time, vectors are compared by cosine similarity or inner product, usually in a [[vector-databases|vector database]]. Dimensionality (e.g. Matryoshka representations, Kusupati et al., 2022) and evaluation on benchmarks such as MTEB (Muennighoff et al., 2022) determine cost and fitness for a task.

```text
text ─▶ tokenizer ─▶ Transformer encoder ─▶ token vectors
                                              ▼
                                   pooling (mean or [CLS])
                                              ▼
                              text embedding (optionally L2-normalised)
                                              ▼
                       similarity search (cosine / inner product)
training: pairs or triplets of similar and dissimilar texts
```

#### 1. Tokenization

Tokenization processes input text into a sequence of subword tokens using a fixed vocabulary, commonly implemented via WordPiece (Devlin et al., 2018). The algorithm greedily segments words into the longest possible subword units present in the vocabulary, decomposing unknown words into sequences of known subwords (e.g., "unhappiness" → ["un", "happ", "iness"]). A typical vocabulary size is 30,000 tokens (as used in BERT), balancing coverage of common words against computational efficiency. This design minimizes out-of-vocabulary (OOV) tokens compared to word-level tokenization, though it may fragment frequent words. The trade-off involves memory usage and segmentation accuracy: larger vocabularies reduce OOV but increase memory overhead and model size, while smaller vocabularies risk OOV and suboptimal segmentation. The fixed vocabulary structure enables consistent token-to-index mapping during inference, critical for efficient embedding model processing and integration with [[vector-databases|Vector Databases]].

#### 2. Transformer Encoding

Transformer encoders generate contextual token representations by processing input token sequences through multiple layers of self-attention and feed-forward networks. Inputs consist of tokenized text sequences, typically including special tokens (e.g., [CLS], [SEP] in BERT), with each token's embedding initially drawn from a lookup table. The output is a sequence of dense vectors, one per token, where the vector for a token depends on its full contextual surroundings. Crucially, identical tokens produce distinct vectors based on context—for example, "bank" in "river bank" and "bank account" yields different representations. This bidirectional context modeling, jointly conditioning on left and right context across all layers (Devlin et al., 2018), captures richer semantic relationships than unidirectional models. However, it incurs quadratic computational complexity relative to sequence length, limiting scalability for very long texts. This design prioritizes representation quality over efficiency, making it suitable for tasks requiring deep contextual understanding like [[rag-retrieval|RAG: Retrieval]], where precise semantic matching is essential.

#### 3. Pooling

Raw BERT outputs consist of a sequence of token embeddings (shape `[n, d]` for `n` tokens and dimension `d`). To form a single sentence embedding, these must be aggregated, typically via [CLS] token extraction (the first token) or mean pooling (element-wise average over all tokens). The [CLS] token is optimized for classification tasks, not semantic similarity, leading to inadequate sentence representations. Mean pooling without fine-tuning fails to capture nuanced semantic relationships due to inconsistent token weighting (e.g., stop words diluting meaning). This is why Reimers & Gurevych (2019) fine-tune the whole encoder together with the pooling step on sentence pairs; the alternative, feeding every sentence pair jointly through BERT, takes about 65 hours to find the most similar pair among 10,000 sentences and is unsuitable for similarity search.

#### 4. Training for Semantic Similarity

Training for semantic similarity employs siamese or triplet network architectures to position similar text embeddings close together and dissimilar ones far apart in the embedding space. Inputs consist of text pairs (siamese) or triplets (anchor, positive, negative examples; triplet), where positive pairs share semantic meaning and negative pairs do not. The model processes each input through shared subnetworks (e.g., BERT), producing fixed-length embeddings. The loss function, typically a contrastive or triplet loss, enforces that the cosine similarity between similar pairs exceeds that of dissimilar pairs by a predefined margin. Inputs are text sequences, outputs are normalized embeddings enabling efficient cosine similarity computation. Key design choices include using cosine similarity (requiring L2-normalized embeddings) for retrieval efficiency and leveraging shared weights in siamese networks to reduce parameters. Trade-offs involve the need for large, high-quality paired datasets to avoid trivial solutions in siamese training, while triplet networks require careful negative sampling to maintain effective margin enforcement. Reimers & Gurevych (2019) demonstrated that this approach, as implemented in Sentence-BERT, reduces semantic similarity search latency from ~65 hours (for BERT) to ~5 seconds on 10,000 sentences while preserving accuracy.

#### 5. Similarity and Normalisation

In similarity search, embeddings are compared using cosine similarity or inner product. Cosine similarity normalizes the dot product by vector magnitudes: `cos_sim = (query · doc) / (||query|| ||doc||)`. The inner product `query · doc` depends on both direction and magnitude. L2-normalization (scaling embeddings to unit length, `||vec|| = 1`) eliminates magnitude differences, making `cos_sim = query · doc`. Thus, L2-normalized embeddings yield identical document rankings under both metrics. This allows [[vector-databases|vector databases]] to use plain inner product search (e.g., FAISS' `IndexFlatIP`), with the normalisation done once at indexing time. Queries and documents must be embedded with the same model (or a model pair trained together); otherwise their vectors are not comparable.

#### 6. Dimensionality and Matryoshka Representations

Embedding dimensionality presents a fundamental trade-off: higher dimensions typically improve semantic quality but increase memory footprint and slow search operations due to higher computational costs per comparison. Conversely, lower dimensions reduce memory and accelerate search but risk semantic degradation. Matryoshka Representation Learning (MRL; Kusupati et al., 2022) addresses this by designing nested embeddings where a single high-dimensional vector encodes information at multiple granularities. The representation structure ensures that truncating to a lower dimension (e.g., 768 to 384) retains sufficient semantic fidelity for downstream tasks without retraining. This approach minimally modifies existing pipelines, imposes no inference cost, and enables adaptive resource allocation. Kusupati et al. (2022) report up to 14x smaller embeddings at the same accuracy for ImageNet-1K classification and up to 14x real-world speed-ups for large-scale retrieval on ImageNet, and show that MRL also works for language models such as BERT; a single model can thus replace several separately trained low-dimensional ones. The nested design allows a unified embedding to serve diverse computational constraints, making it particularly effective for [[vector-databases|vector databases]] where latency and storage efficiency are critical.

#### 7. Evaluating Embedding Models

Embedding models must be evaluated across diverse tasks including retrieval, clustering, and classification to assess their general applicability. The Massive Text Embedding Benchmark (MTEB) spans 8 tasks across 58 datasets and 112 languages, revealing that no single model dominates all tasks (Muennighoff et al., 2022). Inputs are text sequences processed through tokenization and a transformer encoder, with outputs being fixed-dimensional dense vectors (e.g., 384 or 768 dimensions). Common design choices include pooling methods (mean, CLS token) and L2 normalization, which enables efficient similarity computation via inner product (`score = A · B` for normalized vectors). Trade-offs involve dimensionality (higher dimensions increase expressiveness but storage and computation costs), task-specific optimization (e.g., a model excelling at semantic textual similarity may underperform in clustering), and the need for task-specific validation. Crucially, models must be evaluated on the target application's data and task, as performance varies significantly across domains and use cases; general benchmarks cannot substitute for empirical validation on the specific corpus and queries, as part of [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]].

#### Origin and variants

Static word embeddings, including word2vec (Mikolov et al. 2013) and GloVe (Pennington et al. 2014), generate fixed vector representations per word independent of context. word2vec employs neural networks (CBOW or skip-gram) trained on local context windows to predict surrounding words or a target word, while GloVe factorizes a global word co-occurrence matrix using a weighted least-squares objective. Both methods are computationally efficient but cannot resolve polysemy (e.g., "bank" shares one vector for all meanings). Contextual embeddings, such as those from BERT (Devlin et al. 2018), produce token-level vectors conditioned on the entire sentence via bidirectional transformer encoders, resolving polysemy through joint left-right context modeling. This requires full sentence processing, increasing computational cost. Sentence embeddings are typically derived by aggregating contextual token embeddings (e.g., via mean pooling or [CLS] token extraction), trading efficiency for context-aware semantics. This enables more accurate semantic matching in retrieval systems [[rag-retrieval|Retrieval]].

### When to use it

- For efficient semantic similarity search in large collections (e.g., 10,000 sentences), SBERT reduces inference time from ~65 hours (BERT) to ~5 seconds while maintaining accuracy, typically implemented with [[vector-databases|Vector Databases]] (Reimers & Gurevych, 2019).
- When memory or latency budgets vary, Matryoshka embeddings can be truncated to fewer dimensions with little loss (Kusupati et al., 2022).
- For clustering, deduplication or classification of texts by meaning, using the same vectors as for search.
- Static word vectors (Mikolov et al., 2013) only where word-level similarity is enough and resources are very limited; contextual models are the standard today.

### Strengths and limitations

**Strengths**
- SBERT reduces semantic similarity search time from ~65 hours (BERT) to ~5 seconds for 10,000 sentences (Reimers & Gurevych, 2019).
- Embeddings enable diverse applications including semantic search, clustering, and reranking across multiple tasks (Muennighoff et al., 2022).
- Matryoshka Representation Learning (MRL) lets one embedding serve different computational budgets (Kusupati et al., 2022).

**Limitations**
- One vector per text compresses its meaning; long or multi-topic texts lose detail, and exact terms such as identifiers are matched less reliably than by lexical search.
- Off-the-shelf BERT used as a cross-encoder is unsuitable for similarity search and clustering because it must process every pair jointly; dedicated sentence-embedding training is needed (Reimers & Gurevych, 2019).
- No single embedding method dominates all tasks, necessitating task-specific evaluation (Muennighoff et al., 2022).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Dense embeddings | Encode semantic meaning in continuous vector space (e.g., via cosine similarity), contrasting with sparse representations that use discrete, high-dimensional vectors and rely on exact word matches. | Semantic search, paraphrase detection, and contexts requiring contextual meaning. |
| Sparse representations (e.g., TF-IDF, BM25) | Represent text as sparse vectors based on term frequencies, measuring similarity via bag-of-words overlap; lacks semantic understanding beyond lexical matching. | Exact keyword matching, identifiers, and scenarios where semantic nuance is not required. |
| Static word embeddings (word2vec, GloVe) | One vector per word regardless of context. | Lightweight word-level similarity. |
| Cross-encoders | Score a text pair jointly instead of producing reusable vectors. | Reranking a short candidate list. |

Dense and sparse representations are often combined in hybrid retrieval, see [[rag-retrieval|RAG: Retrieval]].

### In practice

Evaluation should be conducted on task-specific retrieval datasets rather than standard semantic textual similarity benchmarks, as no embedding method dominates all tasks (Muennighoff et al. (2022)). Common failure modes include domain shift (reduced performance in specialized domains) and chunk dilution (reduced precision from multi-topic chunks), which can be mitigated through domain adaptation or optimized [[rag-chunking|chunking strategies]]. For parameter choices, embedding dimensionality should balance expressiveness and computational cost; Matryoshka representations (Kusupati et al. (2022)) allow truncating vectors without training separate models. The maximum input length of the model also limits chunk size.

### Key takeaway

Embeddings provide dense semantic representations for text but require balancing computational cost against accuracy, a key constraint in [[rag-retrieval|retrieval systems]].

### Sources

- Mikolov, T. et al. (2013). *Efficient Estimation of Word Representations in Vector Space.* [arXiv:1301.3781](https://arxiv.org/abs/1301.3781)
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Muennighoff, N. et al. (2022). *MTEB: Massive Text Embedding Benchmark.* [arXiv:2210.07316](https://arxiv.org/abs/2210.07316)
- Kusupati, A. et al. (2022). *Matryoshka Representation Learning.* [arXiv:2205.13147](https://arxiv.org/abs/2205.13147)
- Pennington, J., Socher, R. & Manning, C. D. (2014). *GloVe: Global Vectors for Word Representation.* EMNLP 2014. [ACL Anthology](https://aclanthology.org/D14-1162/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Embeddings sind dichte Vektorrepräsentationen von Text, die semantische Ähnlichkeit kodieren und Retrieval-Systemen ermöglichen, relevante Dokumente anhand des kontextuellen Sinnes zu finden, statt durch exakte Schlüsselwortübereinstimmungen. Dieser Ansatz überwindet die Grenzen der lexikalischen Suche, indem semantisch ähnlicher Text in der Nähe von Punkten in einem hochdimensionalen Raum abgebildet wird, was grundlegend für moderne Information Retrieval [[information-retrieval|Information Retrieval]] ist.

### Funktionsweise

Ein Text-Embedding-Modell verwandelt einen Text in einen dichten Vektor: der Text wird tokenisiert, in kontextuelle Token-Vektoren durch einen Transformer kodiert und in einen einzelnen Vektor gepoolt. Das Modell wird so trainiert, dass Texte mit ähnlicher Bedeutung ähnliche Vektoren erhalten (Reimers & Gurevych, 2019); zur Suchzeit werden Vektoren durch Kosinusähnlichkeit oder Skalarprodukt verglichen, meist in einer [[vector-databases|Vektordatenbank]]. Die Dimensionalität (z. B. Matryoshka-Darstellungen, Kusupati et al., 2022) und die Bewertung anhand von Benchmarks wie MTEB (Muennighoff et al., 2022) bestimmen Kosten und Eignung für eine Aufgabe.

```text
text ─▶ tokenizer ─▶ Transformer encoder ─▶ token vectors
                                              ▼
                                   pooling (mean or [CLS])
                                              ▼
                              text embedding (optionally L2-normalised)
                                              ▼
                       similarity search (cosine / inner product)
training: pairs or triplets of similar and dissimilar texts
```

#### 1. Tokenisierung

Die Tokenisierung verwandelt den Eingabetext in eine Sequenz von Unterworts-Token mithilfe eines festen Vokabulars, was häufig über WordPiece implementiert wird (Devlin et al., 2018). Der Algorithmus segmentiert die Wörter gierig in die längsten möglichen Unterworts-Einheiten, die im Vokabular vorhanden sind, und zerlegt unbekannte Wörter in Sequenzen bekannter Unterwörter (z. B. „unhappiness“ → [„un“, „happ“, „iness“]). Eine typische Vokabulargröße beträgt 30.000 Token (wie bei BERT verwendet), was eine Balance zwischen der Abdeckung häufiger Wörter und der Rechenleistung ermöglicht. Dieses Design minimiert verglichen mit der Tokenisierung auf Wortebene die Anzahl der out-of-vocabulary (OOV) Token, obwohl es häufige Wörter fragmentieren kann. Der Kompromiss besteht in der Speicherung und der Segmentierungsgenauigkeit: größere Vokabulare reduzieren OOV, erhöhen aber den Speicherbedarf und die Modellgröße, während kleinere Vokabulare das Risiko von OOV und einer suboptimalen Segmentierung erhöhen. Die feste Vokabularstruktur ermöglicht eine konsistente Zuordnung von Token zu Index während der Inferenz, was für die effiziente Verarbeitung durch Embedding-Modelle und die Integration mit [[vector-databases|Vektordatenbanken]] entscheidend ist.

#### 2. Transformer-Encoding

Transformer-Encoder erzeugen kontextuelle Token-Vertretungen, indem sie Eingabetoken-Seqeuenzen durch mehrere Schichten von Selbstattenion und Feed-Forward-Netzwerken verarbeiten. Eingaben bestehen aus tokenisierten Textsequenzen, typischerweise mit speziellen Tokens (z. B. [CLS], [SEP] bei BERT), wobei die Embedding jedes Tokens ursprünglich aus einer Lookup-Tabelle gezogen wird. Das Ausgabeergebnis ist eine Sequenz von Dense Vektoren, ein Vektor pro Token, wobei der Vektor eines Tokens von seinem vollständigen kontextuellen Umfeld abhängt. Entscheidend ist, dass identische Tokens aufgrund des Kontexts unterschiedliche Vektoren erzeugen – beispielsweise erzeugt „bank“ in „river bank“ und „bank account“ unterschiedliche Vertretungen. Dieses bidirektionale Kontextmodell, das in allen Schichten auf links und rechts liegenden Kontext gemeinsam konditioniert (Devlin et al., 2018), erfasst reichere semantische Beziehungen als unidirektionale Modelle. Allerdings verursacht es eine quadratische rechnerische Komplexität in Bezug auf die Sequenlänge, was die Skalierbarkeit bei sehr langen Texten begrenzt. Dieses Design priorisiert die Qualität der Vertretungen gegenüber der Effizienz, wodurch es für Aufgaben geeignet ist, die tiefe kontextuelle Verständnis erfordern, wie z. B. [[rag-retrieval|RAG: Retrieval]], bei denen präzises semantisches Matching entscheidend ist.

#### 3. Pooling

Die Rohausgaben von BERT bestehen aus einer Folge von Token-Embeddings (Form `[n, d]` für `n` Token und Dimension `d`). Um ein einzelnes Satz-Embedding zu bilden, müssen diese aggregiert werden, typischerweise über die Extraktion des [CLS]-Tokens (das erste Token) oder mittels Mittelwert-Pooling (elementweises Durchschnitt aller Token). Das [CLS]-Token ist für Klassifizierungsaufgaben optimiert, nicht jedoch für semantische Ähnlichkeit, was zu unzureichenden Satzrepräsentationen führt. Mittelwert-Pooling ohne Feinabstimmung ist nicht in der Lage, feine semantische Beziehungen zu erfassen, aufgrund von ungleichmäßiger Token-Bewertung (z. B. Stoppwörter, die die Bedeutung verzerren). Deshalb feinabstimmen Reimers & Gurevych (2019) den gesamten Encoder gemeinsam mit dem Pooling-Schritt anhand von Satzpaaren; die Alternative, jedes Satzpaar gemeinsam durch BERT zu führen, benötigt etwa 65 Stunden, um das ähnlichste Paar unter 10.000 Sätzen zu finden und ist für Ähnlichkeitssuche ungeeignet.

#### 4. Training für semantische Ähnlichkeit

Das Training für semantische Ähnlichkeit verwendet Architekturen von siamesischen oder Dreier-Netzwerken, um ähnliche Text-Embeddings nahe beieinander und unähnliche weit voneinander entfernt in den Embedding-Raum zu positionieren. Die Eingaben bestehen aus Textpaaren (siamesisch) oder Dreiergruppen (Anchor, positiv, negativ; Dreiergruppe), wobei positive Paare eine gemeinsame semantische Bedeutung haben und negative Paare nicht. Das Modell verarbeitet jede Eingabe über gemeinsame Unter Netzwerke (z. B. BERT), wodurch feste Länge Embeddings erzeugt werden. Die Verlustfunktion, typischerweise ein kontrastiver oder Dreier-Verlust, erzwingt, dass die Kosinusähnlichkeit zwischen ähnlichen Paaren die von unähnlichen Paaren um einen vordefinierten Abstand übertrifft. Eingaben sind Textsequenzen, Ausgaben sind normalisierte Embeddings, die eine effiziente Kosinusähnlichkeitsberechnung ermöglichen. Wichtige Gestaltungswahlmöglichkeiten umfassen die Verwendung der Kosinusähnlichkeit (erfordert L2-normalisierte Embeddings) zur Effizienz bei der Retrieval und die Nutzung gemeinsamer Gewichte in siamesischen Netzwerken zur Reduktion der Parameter. Kompromisse umfassen den Bedarf an großen, hochwertigen Paardatensätzen, um triviale Lösungen im siamesischen Training zu vermeiden, während Dreier-Netzwerke sorgfältige negative Sampling erfordern, um eine effektive Abstandssteuerung zu gewährleisten. Reimers & Gurevych (2019) zeigten, dass dieser Ansatz, wie in Sentence-BERT implementiert, die Latenzzeit für semantische Ähnlichkeitssuche von ~65 Stunden (für BERT) auf ~5 Sekunden für 10.000 Sätze reduziert, während die Genauigkeit erhalten bleibt.

#### 5. Ähnlichkeit und Normalisierung

Bei der Ähnlichkeitsuche werden Embeddings mithilfe des Cosine Similaritysmaßes oder des Skalarprodukts verglichen. Das Cosine Similaritysmaß normalisiert das Skalarprodukt durch die Vektormagnituden: `cos_sim = (query · doc) / (||query|| ||doc||)`. Das Skalarprodukt `query · doc` hängt sowohl von der Richtung als auch von der Größe ab. Die L2-Normalisierung (Skalierung der Embeddings auf Einheitslänge, `||vec|| = 1`) eliminiert Unterschiede in der Größe, wodurch `cos_sim = query · doc` gilt. Somit erzeugen L2-normalisierte Embeddings unter beiden Metriken identische Dokumentranglisten. Dies ermöglicht [[vector-databases|Vektordatenbanken]], das einfache Skalarprodukt-Search (z. B. FAISS' `IndexFlatIP`) zu verwenden, wobei die Normalisierung nur einmal zur Indexzeit durchgeführt wird. Abfragen und Dokumente müssen mit demselben Modell (oder einem Modellpaar, das gemeinsam trainiert wurde) eingebettet werden; andernfalls sind ihre Vektoren nicht vergleichbar.

#### 6. Dimensionalität und Matryoshka-Darstellungen

Die Dimensionalität von Embeddings stellt einen grundlegenden Kompromiss dar: höhere Dimensionen verbessern in der Regel die semantische Qualität, erhöhen aber den Speicherbedarf und verlangsamen Suchvorgänge aufgrund höherer Rechenkosten pro Vergleich. Umgekehrt reduzieren niedrigere Dimensionen den Speicherbedarf und beschleunigen die Suche, bergen aber das Risiko einer semantischen Degradierung. Matryoshka Representation Learning (MRL; Kusupati et al., 2022) löst dies, indem es verschachtelte Embeddings entwirft, bei denen ein einzelner hochdimensionaler Vektor Informationen auf verschiedenen Granularitätsstufen kodiert. Die Darstellungsgestaltung gewährleistet, dass das Truncieren auf eine niedrigere Dimension (z. B. 768 auf 384) die semantische Genauigkeit für nachfolgende Aufgaben ohne Neutraining beibehält. Dieser Ansatz verändert bestehende Pipelines minimal, verursacht keine Inferenzkosten und ermöglicht eine adaptive Ressourcenverteilung. Kusupati et al. (2022) berichten über bis zu 14-fach kleinere Embeddings bei gleicher Genauigkeit für die Klassifizierung von ImageNet-1K und bis zu 14-fache Geschwindigkeitsverbesserungen bei großskaligen Retrieval-Vorgängen auf ImageNet und zeigen, dass MRL auch für Sprachmodelle wie BERT funktioniert; ein einzelnes Modell kann somit mehrere separat trainierte niedrigdimensionale Modelle ersetzen. Die verschachtelte Gestaltung ermöglicht einem einheitlichen Embedding, diverse rechnerische Einschränkungen zu erfüllen, wodurch es insbesondere für [[vector-databases|Vektordatenbanken]] effektiv ist, bei denen Latenz und Speichereffizienz kritisch sind.

#### 7. Beurteilung von Embedding-Modellen

Embedding-Modelle müssen über verschiedene Aufgaben hinweg bewertet werden, einschließlich Retrieval, Clustering und Klassifizierung, um ihre allgemeine Anwendbarkeit zu beurteilen. Der Massive Text Embedding Benchmark (MTEB) umfasst 8 Aufgaben über 58 Datensätze und 112 Sprachen und zeigt, dass kein einziges Modell alle Aufgaben dominiert (Muennighoff et al., 2022). Eingaben sind Textsequenzen, die über Tokenisierung und einen Transformer-Encoder verarbeitet werden, wobei die Ausgaben feste dimensionale Dense Vektoren sind (z. B. 384 oder 768 Dimensionen). Häufige Gestaltungswahlmöglichkeiten umfassen Pooling-Methoden (Mittelwert, CLS-Token) und L2-Normalisierung, die eine effiziente Ähnlichkeitsberechnung über das Skalarprodukt ermöglicht (`score = A · B` für normalisierte Vektoren). Kompromisse betreffen die Dimensionalität (höhere Dimensionen erhöhen die Ausdruckskraft, erhöhen aber auch Lager- und Rechenkosten), Aufgaben-spezifische Optimierung (z. B. ein Modell, das bei semantischer Textähnlichkeit hervorragt, kann in Clustering schlechter abschneiden) und den Bedarf an Aufgaben-spezifischer Validierung. Entscheidend ist, dass Modelle auf den Daten und der Aufgabe der Zielanwendung bewertet werden müssen, da die Leistung sich erheblich über verschiedene Domänen und Anwendungsfälle unterscheidet; allgemeine Benchmarks können nicht als Ersatz für empirische Validierung auf dem spezifischen Corpus und den Abfragen dienen, wie Teil von [[rag-retrieval-evaluation|RAG: Retrieval Evaluation]].

#### Ursprung und Varianten

Statische Wortembeddings, einschließlich word2vec (Mikolov et al. 2013) und GloVe (Pennington et al. 2014), erzeugen feste Vektorrepräsentationen pro Wort, unabhängig vom Kontext. word2vec verwendet neuronale Netze (CBOW oder skip-gram), die auf lokalen Kontextfenstern trainiert werden, um umgebende Wörter oder ein Zielwort vorherzusagen, während GloVe eine globale Wortko-occurrenzmatrix mithilfe eines gewichteten kleinsten-Quadrate-Objektivs faktorisiert. Beide Methoden sind rechenleistungseffizient, können aber keine Polysemie lösen (z. B. teilt „bank“ einen Vektor für alle Bedeutungen). Kontextuelle Embeddings, wie sie beispielsweise von BERT (Devlin et al. 2018) stammen, erzeugen Token-Vektoren, die auf die gesamte Satzstruktur über bidirektionale Transformer-Encoder konditioniert sind, und lösen Polysemie durch gemeinsame Modellierung von links- und rechtsseitigem Kontext. Dies erfordert die vollständige Verarbeitung eines Satzes und erhöht die Rechenkosten. Satzembeddings werden typischerweise durch Aggregation kontextueller Token-Embeddings gewonnen (z. B. über Mittelwert-Pooling oder Extraktion des [CLS]-Tokens), wodurch Effizienz zugunsten kontextsensitiver Semantik aufgegeben wird. Dies ermöglicht präzisere semantische Übereinstimmung in Retrieval-Systemen [[rag-retrieval|Retrieval]].

### Wann einsetzen

- Für effiziente semantische Ähnlichkeitssuche in großen Sammlungen (z. B. 10.000 Sätze) reduziert SBERT die Inferenzzeit von ~65 Stunden (BERT) auf ~5 Sekunden, während die Genauigkeit gewahrt bleibt, typischerweise mit [[vector-databases|Vektordatenbank]] implementiert (Reimers & Gurevych, 2019).
- Wenn Speicher- oder Latenzbudgets variieren, können Matryoshka-Embeddings auf weniger Dimensionen gekürzt werden, wobei nur geringer Verlust auftritt (Kusupati et al., 2022).
- Für das Clustering, die Deduplizierung oder die Klassifizierung von Texten nach Bedeutung, unter Verwendung der gleichen Vektoren wie bei der Suche.
- Statische Wortvektoren (Mikolov et al., 2013) nur dort, wo die Wortebene ausreicht und Ressourcen sehr begrenzt sind; kontextuelle Modelle sind heute der Standard.

### Stärken und Grenzen

**Vorteile**
- SBERT reduziert die Zeit für eine semantische Ähnlichkeitsuche von ~65 Stunden (BERT) auf ~5 Sekunden für 10.000 Sätze (Reimers & Gurevych, 2019).
- Embeddings ermöglichen diverse Anwendungen, einschließlich semantischer Suche, Clustering und Re-Ranking über mehrere Aufgaben hinweg (Muennighoff et al., 2022).
- Matryoshka Representation Learning (MRL) ermöglicht es einem Embedding, unterschiedliche rechnerische Budgets zu bedienen (Kusupati et al., 2022).

**Einschränkungen**
- Ein Vektor pro Text komprimiert seine Bedeutung; lange oder mehrthemenbehaftete Texte verlieren Details, und exakte Begriffe wie Identifikatoren werden weniger zuverlässig als durch lexikalische Suche abgeglichen.
- Ein BERT-Modell, das als Cross-Encoder verwendet wird, ist für Ähnlichkeitsuche und Clustering ungeeignet, da es jedes Paar gemeinsam verarbeiten muss; eine spezifische Ausrichtung auf Satz-Embeddings ist erforderlich (Reimers & Gurevych, 2019).
- Keine einzelne Embedding-Methode dominiert alle Aufgaben, was eine Aufgaben-spezifische Evaluierung erfordert (Muennighoff et al., 2022).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Dichte Embeddings | Kodieren die semantische Bedeutung in einem kontinuierlichen Vektorraum (z. B. über Kosinusähnlichkeit), im Gegensatz zu sparsamen Darstellungen, die diskrete, hochdimensionale Vektoren verwenden und auf exakte Wortübereinstimmungen zurückgreifen. | Semantische Suche, Erkennung von Paraphrasen und Kontexte, die kontextuelle Bedeutung erfordern. |
| Sparsame Darstellungen (z. B. TF-IDF, BM25) | Stellen Text als sparsame Vektoren basierend auf Begriffshäufigkeiten dar, messen Ähnlichkeit über die Übereinstimmung von Wortmengen; fehlen semantisches Verständnis jenseits lexikalischer Übereinstimmung. | Exakte Schlüsselwortübereinstimmung, Identifikatoren und Szenarien, in denen semantische Nuancen nicht erforderlich sind. |
| Statische Wortembeddings (word2vec, GloVe) | Ein Vektor pro Wort, unabhängig vom Kontext. | Leichte Wortebene-Ähnlichkeit. |
| Cross-Encoder | Bewerten ein Textpaar gemeinsam, anstatt wiederverwendbare Vektoren zu erzeugen. | Wiederholungsbewertung einer kurzen Kandidatenliste. |

Dichte und sparsame Darstellungen werden oft in hybrider Retrieval-Methoden kombiniert, siehe [[rag-retrieval|RAG: Retrieval]].

### In der Praxis

Die Evaluation sollte an task-spezifischen Retrieval-Datensätzen statt an Standard-semantic-textual-similarity-Benchmarks durchgeführt werden, da keine Embedding-Methode alle Aufgaben dominiert (Muennighoff et al. (2022)). Häufige Fehlschläge umfassen Domain-Shift (verringerte Leistung in spezialisierten Bereichen) und Chunk-Dilution (verringerte Präzision durch mehrthemenbehaftete Chunks), die durch Domain-Adaptation oder optimierte [[rag-chunking|Chunking-Strategien]] gemildert werden können. Bei der Wahl der Parameter sollte die Embedding-Dimensionalität Ausdruckskraft und Rechenkosten ausbalancieren; Matryoshka-Representations (Kusupati et al. (2022)) ermöglichen das Truncieren von Vektoren ohne das Training separater Modelle. Die maximale Eingabelänge des Modells begrenzt ebenfalls die Chunk-Größe.

### Merksatz

Embedding liefern dichte semantische Darstellungen für Text, erfordern jedoch ein Ausbalancieren zwischen Rechenkosten und Genauigkeit, eine entscheidende Einschränkung in [[rag-retrieval|Retrieval-Systemen]].

### Quellen

- Mikolov, T. et al. (2013). *Efficient Estimation of Word Representations in Vector Space.* [arXiv:1301.3781](https://arxiv.org/abs/1301.3781)
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Muennighoff, N. et al. (2022). *MTEB: Massive Text Embedding Benchmark.* [arXiv:2210.07316](https://arxiv.org/abs/2210.07316)
- Kusupati, A. et al. (2022). *Matryoshka Representation Learning.* [arXiv:2205.13147](https://arxiv.org/abs/2205.13147)
- Pennington, J., Socher, R. & Manning, C. D. (2014). *GloVe: Global Vectors for Word Representation.* EMNLP 2014. [ACL Anthology](https://aclanthology.org/D14-1162/)
