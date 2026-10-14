---
title_en: BERTScore
title_de: BERTScore
entity_type: Method
aliases:
- BERTScore
- BERT Score
sources:
- https://arxiv.org/abs/1904.09675
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

BERTScore evaluates generated text against a reference by matching tokens through their contextual embeddings instead of exact strings: each token of one sentence is paired with its most similar token in the other by cosine similarity, and the averages give [[classification-metrics|precision]], recall and F1 (Zhang et al., 2020). Because contextual embeddings represent meaning in context, BERTScore credits paraphrases that n-gram metrics such as [[bleu|BLEU]] miss. In tests on the outputs of 363 [[machine-translation|machine translation]] and image captioning systems it correlated better with human judgements than existing metrics, and it was more robust on adversarial paraphrase pairs (Zhang et al., 2020). The authors recommend F1 with the 24-layer RoBERTa-large model for English.

### How it works

```text
reference x = ⟨x₁ … x_k⟩, candidate x̂ = ⟨x̂₁ … x̂_l⟩
 ▼ contextual embeddings from a pre-trained Transformer layer (normalised)
 ▼ similarity matrix: cos(x_i, x̂_j) = x_iᵀ x̂_j
 ▼ greedy matching
   R_BERT = (1/|x|) Σ_i max_j x_iᵀ x̂_j        (each reference token → best candidate token)
   P_BERT = (1/|x̂|) Σ_j max_i x_iᵀ x̂_j        (each candidate token → best reference token)
   F_BERT = 2 P R / (P + R)
 ▼ optional: idf weighting of tokens; baseline rescaling for readability
```

#### 1. Why embeddings instead of n-grams

N-gram metrics fail in two ways: they do not match paraphrases, and they hardly penalise changes in order that alter meaning (Zhang et al., 2020). For the reference "people like foreign cars", BLEU and METEOR score "people like visiting places abroad" higher than "consumers prefer imported cars". BERTScore represents each token with a contextual embedding from a pre-trained model such as [[bert|BERT]], so that tokens with similar meaning in context have similar vectors (Zhang et al., 2020). Embeddings are explained in [[embeddings|embeddings]].

#### 2. Greedy matching, precision, recall and F1

With normalised vectors, the cosine similarity of two tokens is their dot product (Zhang et al., 2020). Recall matches every reference token to its most similar candidate token and averages these maxima; precision does the same in the other direction; F1 combines both. Matching is greedy, each token independently taking its best partner, which is simple and fast; the authors compared it with optimal assignment in an appendix. Although each match compares single tokens, the contextual embeddings carry information from the rest of the sentence (Zhang et al., 2020).

#### 3. Importance weighting

Rare words are often more telling for sentence similarity than common ones, so BERTScore can weight each reference token by its inverse document frequency computed over the reference sentences of the test set, with plus-one smoothing for unknown word pieces (Zhang et al., 2020). In the experiments, idf weighting sometimes helped and sometimes did not, so the main results do not use it.

#### 4. Baseline rescaling

Scores lie in the range of cosine similarity, but in practice cluster in a narrow band, which makes them hard to read (Zhang et al., 2020). BERTScore therefore subtracts an empirical baseline b, the average score of one million random sentence pairs from Common Crawl per language and model, and divides by `1 − b`, giving values typically between 0 and 1. The rescaling changes neither rankings nor correlation with human judgements (Zhang et al., 2020).

#### 5. Model choice and results

Twelve pre-trained models were evaluated, using a validation set to select the best layer of each (Zhang et al., 2020). On WMT18 machine translation and COCO image captioning, BERTScore correlated better with human judgements than existing task-agnostic metrics and supported model selection; F1 was the most reliable variant across settings (Zhang et al., 2020). On the adversarial paraphrase set PAWS, where word-overlap metrics fell almost to chance, BERTScore dropped only slightly. The authors recommend RoBERTa-large for English and multilingual BERT for other languages, the latter being less stable for low-resource languages (Zhang et al., 2020).

#### Origin and variants

Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Weinberger and Yoav Artzi at Cornell presented BERTScore at ICLR 2020 (Zhang et al., 2020). A concurrent method, MoverScore, combines contextual embeddings with earth mover's distance; the authors report that adding its improvements to BERTScore makes it equivalent or better (Zhang et al., 2020). Other generation metrics are compared in [[text-similarity-metrics|text similarity metrics]].

### When to use it

- Evaluating generated text against references where valid outputs may use different words, such as translation, captioning or summarisation (Zhang et al., 2020).
- Segment-level comparisons, where sentence-level BLEU is less reliable (Zhang et al., 2020).
- As a reference-based signal in LLM and [[retrieval-augmented-generation|RAG]] evaluation pipelines ([[rag-generation-evaluation|RAG generation evaluation]]).

### Strengths and limitations

**Strengths**
- Credits paraphrases and synonyms (Zhang et al., 2020).
- Better correlation with human judgements and more robust to adversarial paraphrases than n-gram metrics (Zhang et al., 2020).
- Simple, task-agnostic and easy to use (Zhang et al., 2020).

**Limitations**
- Requires a reference; it measures similarity, not factual correctness.
- No single configuration is best everywhere; model, layer and weighting must be chosen for the domain and language (Zhang et al., 2020).
- Less stable for low-resource languages with the multilingual model (Zhang et al., 2020).

### Comparison

| Metric | Unit of matching | Paraphrases | Needs reference |
|---|---|---|---|
| [[bleu\|BLEU]] | exact n-grams | no | yes |
| BERTScore | contextual token embeddings | yes | yes |
| [[llm-as-a-judge\|LLM as a judge]] | whole answer judged by a model | yes | optional |

Source: Zhang et al. (2020).

### In practice

Report the model, layer, whether idf weighting was used and whether scores are rescaled, since these settings change the values (Zhang et al., 2020). For checking whether an answer is supported by retrieved sources, BERTScore against a reference answer is not enough; groundedness checks are covered in [[hallucination-detection|hallucination detection]].

### Key takeaway

BERTScore matches each token to its most similar counterpart in contextual embedding space and averages these similarities into precision, recall and F1, which tracks human judgements of generated text better than n-gram overlap and tolerates paraphrases.

### Sources

- Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q. & Artzi, Y. (2020). *BERTScore: Evaluating Text Generation with BERT.* ICLR 2020. [arXiv:1904.09675](https://arxiv.org/abs/1904.09675)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

BERTScore bewertet erzeugten Text gegenüber einer Referenz, indem es Token über ihre kontextuellen Embeddings statt über exakte Zeichenketten abgleicht: Jedes Token eines Satzes wird per Cosine Similarity mit dem ähnlichsten Token des anderen gepaart, und die Mittelwerte ergeben [[classification-metrics|Precision]], Recall und F1 (Zhang et al., 2020). Weil kontextuelle Embeddings Bedeutung im Zusammenhang abbilden, erkennt BERTScore Umschreibungen an, die N-Gramm-Metriken wie [[bleu|BLEU]] übersehen. In Tests auf den Ausgaben von 363 Systemen zur maschinellen Übersetzung und Bildbeschreibung korrelierte es besser mit menschlichen Urteilen als bestehende Metriken und war robuster bei adversarialen Paraphrasenpaaren (Zhang et al., 2020). Die Autoren empfehlen für Englisch F1 mit dem 24-schichtigen Modell RoBERTa-large.

### Funktionsweise

```text
Referenz x = ⟨x₁ … x_k⟩, Kandidat x̂ = ⟨x̂₁ … x̂_l⟩
 ▼ kontextuelle Embeddings aus einer Schicht eines vortrainierten Transformers (normalisiert)
 ▼ Ähnlichkeitsmatrix: cos(x_i, x̂_j) = x_iᵀ x̂_j
 ▼ gieriger Abgleich
   R_BERT = (1/|x|) Σ_i max_j x_iᵀ x̂_j        (jedes Referenz-Token → bestes Kandidaten-Token)
   P_BERT = (1/|x̂|) Σ_j max_i x_iᵀ x̂_j        (jedes Kandidaten-Token → bestes Referenz-Token)
   F_BERT = 2 P R / (P + R)
 ▼ optional: idf-Gewichtung der Token; Baseline-Reskalierung für bessere Lesbarkeit
```

#### 1. Warum Embeddings statt N-Gramme

N-Gramm-Metriken scheitern auf zwei Arten: Sie gleichen Umschreibungen nicht ab, und sie bestrafen bedeutungsverändernde Umstellungen kaum (Zhang et al., 2020). Zur Referenz „people like foreign cars“ bewerten BLEU und METEOR „people like visiting places abroad“ höher als „consumers prefer imported cars“. BERTScore stellt jedes Token mit einem kontextuellen Embedding aus einem vortrainierten Modell wie [[bert|BERT]] dar, sodass Token mit ähnlicher Bedeutung im Kontext ähnliche Vektoren haben (Zhang et al., 2020). Embeddings erklärt [[embeddings|Embeddings]].

#### 2. Gieriger Abgleich, Precision, Recall und F1

Bei normalisierten Vektoren ist die Cosine Similarity zweier Token ihr Skalarprodukt (Zhang et al., 2020). Recall ordnet jedes Referenz-Token dem ähnlichsten Kandidaten-Token zu und mittelt diese Maxima; Precision tut dasselbe in die andere Richtung; F1 verbindet beides. Der Abgleich ist gierig, jedes Token nimmt unabhängig seinen besten Partner, was einfach und schnell ist; die Autoren verglichen das in einem Anhang mit optimaler Zuordnung. Obwohl jeder Abgleich einzelne Token vergleicht, tragen die kontextuellen Embeddings Information aus dem übrigen Satz (Zhang et al., 2020).

#### 3. Gewichtung nach Bedeutung

Seltene Wörter sagen über Satzähnlichkeit oft mehr aus als häufige, daher kann BERTScore jedes Referenz-Token mit seiner inversen Dokumenthäufigkeit gewichten, berechnet über die Referenzsätze des Testsets, mit Plus-eins-Glättung für unbekannte Wortteile (Zhang et al., 2020). In den Experimenten half die idf-Gewichtung mal und mal nicht, daher nutzen die Hauptergebnisse sie nicht.

#### 4. Baseline-Reskalierung

Die Werte liegen im Bereich der Cosine Similarity, ballen sich in der Praxis aber in einem schmalen Band, was sie schwer lesbar macht (Zhang et al., 2020). BERTScore zieht daher eine empirische Baseline b ab, den mittleren Wert von einer Million zufälliger Satzpaare aus Common Crawl je Sprache und Modell, und teilt durch `1 − b`, was Werte typischerweise zwischen 0 und 1 ergibt. Die Reskalierung ändert weder Rangfolgen noch die Korrelation mit menschlichen Urteilen (Zhang et al., 2020).

#### 5. Modellwahl und Ergebnisse

Zwölf vortrainierte Modelle wurden bewertet, wobei für jedes die beste Schicht auf einem Validierungsset gewählt wurde (Zhang et al., 2020). Auf WMT18 ([[machine-translation|maschinelle Übersetzung]]) und COCO (Bildbeschreibung) korrelierte BERTScore besser mit menschlichen Urteilen als bestehende aufgabenunabhängige Metriken und unterstützte die Modellauswahl; F1 war über alle Einstellungen die verlässlichste Variante (Zhang et al., 2020). Auf dem adversarialen Paraphrasendatensatz PAWS, auf dem Metriken auf Wortüberlappung fast auf Zufallsniveau fielen, sank BERTScore nur leicht. Die Autoren empfehlen RoBERTa-large für Englisch und mehrsprachiges BERT für andere Sprachen, wobei Letzteres für ressourcenarme Sprachen weniger stabil ist (Zhang et al., 2020).

#### Herkunft und Varianten

Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Weinberger und Yoav Artzi von der Cornell University stellten BERTScore auf der ICLR 2020 vor (Zhang et al., 2020). Ein zeitgleich entwickeltes Verfahren, MoverScore, verbindet kontextuelle Embeddings mit der Earth Mover's Distance; die Autoren berichten, dass BERTScore mit dessen Verbesserungen gleichwertig oder besser wird (Zhang et al., 2020). Weitere Metriken für Textgenerierung vergleicht [[text-similarity-metrics|Metriken für Textähnlichkeit]].

### Wann einsetzen

- Erzeugten Text gegenüber Referenzen bewerten, wenn gültige Ausgaben andere Wörter verwenden können, etwa bei Übersetzung, Bildbeschreibung oder Zusammenfassung (Zhang et al., 2020).
- Vergleiche auf Satzebene, bei denen BLEU auf Satzebene weniger verlässlich ist (Zhang et al., 2020).
- Als referenzbasiertes Signal in Evaluationspipelines für LLMs und [[retrieval-augmented-generation|RAG]] ([[rag-generation-evaluation|RAG: Evaluation der Generierung]]).

### Stärken und Grenzen

**Stärken**
- Erkennt Umschreibungen und Synonyme an (Zhang et al., 2020).
- Bessere Korrelation mit menschlichen Urteilen und robuster gegenüber adversarialen Paraphrasen als N-Gramm-Metriken (Zhang et al., 2020).
- Einfach, aufgabenunabhängig und leicht zu nutzen (Zhang et al., 2020).

**Grenzen**
- Braucht eine Referenz; es misst Ähnlichkeit, nicht sachliche Richtigkeit.
- Keine einzelne Konfiguration ist überall die beste; Modell, Schicht und Gewichtung müssen für Domäne und Sprache gewählt werden (Zhang et al., 2020).
- Mit dem mehrsprachigen Modell für ressourcenarme Sprachen weniger stabil (Zhang et al., 2020).

### Vergleich

| Metrik | Einheit des Abgleichs | Umschreibungen | Braucht Referenz |
|---|---|---|---|
| [[bleu\|BLEU]] | exakte N-Gramme | nein | ja |
| BERTScore | kontextuelle Token-Embeddings | ja | ja |
| [[llm-as-a-judge\|LLM as a Judge]] | ganze Antwort, von einem Modell beurteilt | ja | optional |

Quelle: Zhang et al. (2020).

### In der Praxis

Berichtet werden Modell, Schicht, ob idf-Gewichtung genutzt wurde und ob die Werte reskaliert sind, weil diese Einstellungen die Werte verändern (Zhang et al., 2020). Um zu prüfen, ob eine Antwort durch abgerufene Quellen gestützt ist, reicht BERTScore gegenüber einer Referenzantwort nicht; Prüfungen auf Verankerung in Quellen behandelt [[hallucination-detection|Halluzinationserkennung]].

### Merksatz

BERTScore ordnet jedes Token seinem ähnlichsten Gegenstück im kontextuellen Embedding-Raum zu und mittelt diese Ähnlichkeiten zu Precision, Recall und F1; das folgt menschlichen Urteilen über erzeugten Text besser als N-Gramm-Überlappung und toleriert Umschreibungen.

### Quellen

- Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q. & Artzi, Y. (2020). *BERTScore: Evaluating Text Generation with BERT.* ICLR 2020. [arXiv:1904.09675](https://arxiv.org/abs/1904.09675)
