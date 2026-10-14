---
title_en: GloVe (Global Vectors)
title_de: GloVe (Global Vectors)
entity_type: Method
aliases:
- GloVe
- Global Vectors for Word Representation
sources:
- https://nlp.stanford.edu/pubs/glove.pdf
- https://arxiv.org/abs/1607.06520
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

GloVe (Global Vectors for Word Representation) learns static word vectors by fitting them to the logarithm of global word-word co-occurrence counts: for every pair of words that co-occur in the corpus, the dot product of their vectors plus two biases should equal the log of how often they co-occur, weighted so that rare and very frequent pairs count less (Pennington et al., 2014). It combines the global statistics of matrix-factorisation methods such as latent semantic analysis with the local-window training of [[word2vec|Word2Vec]], and trains only on the non-zero entries of the co-occurrence matrix (Pennington et al., 2014). Trained on 42 billion tokens, GloVe reached 75% on the word analogy task, better than the Word2Vec baselines in the paper (Pennington et al., 2014). Word embeddings trained on large amounts of text can encode gender stereotypes, which also has to be checked for GloVe vectors (Bolukbasi et al., 2016).

### How it works

```text
corpus → co-occurrence matrix X  (X_ij = how often word j appears in the context window of word i)
 ▼
model: w_iᵀ w̃_j + b_i + b̃_j ≈ log X_ij        (word vector, context vector, two biases)
 ▼
weighted least squares over non-zero X_ij:
   J = Σ f(X_ij) (w_iᵀ w̃_j + b_i + b̃_j − log X_ij)²
   f(x) = (x / x_max)^α  for x < x_max, else 1     (x_max = 100, α = 3/4)
 ▼
word vector = w + w̃
```

#### 1. Ratios of co-occurrence probabilities

Pennington et al. (2014) start from the observation that meaning shows up in ratios of co-occurrence probabilities. For the target words "ice" and "steam", the ratio P(k|ice)/P(k|steam) is large for a context word k related to ice but not steam, such as "solid" (8.9 in their corpus), small for one related to steam, such as "gas", and close to 1 for words related to both, such as "water", or to neither, such as "fashion". Differences between word vectors should therefore encode such ratios, which leads to a model in which the dot product of two vectors approximates the logarithm of their co-occurrence count (Pennington et al., 2014).

#### 2. The weighted least-squares objective

The model fits `w_iᵀ w̃_j + b_i + b̃_j = log X_ij` for all co-occurring pairs, where w are word vectors, w̃ separate context vectors and b, b̃ biases (Pennington et al., 2014). A plain least-squares fit would weigh all co-occurrences equally, although rare ones are noisy and zero entries make up 75 to 95% of the matrix. GloVe therefore weights each squared error by `f(X_ij)`, which is zero for unseen pairs, grows with the count and is capped at 1 above `x_max`; the authors use `x_max = 100` and `α = 3/4`, noting that Word2Vec found a similar 3/4 power useful (Pennington et al., 2014). Training uses AdaGrad on the non-zero entries only, and the sum of word and context vectors serves as the final embedding.

#### 3. Relation to other methods

Matrix-factorisation methods such as latent semantic analysis ([[latent-semantic-indexing|latent semantic indexing]]) use global statistics efficiently but do poorly on analogies; local-window methods such as skip-gram do well on analogies but do not use global counts directly (Pennington et al., 2014). GloVe aims to combine the two: it is a log-bilinear regression on the global co-occurrence matrix, and the authors show that skip-gram's objective can be related to a weighted factorisation of the same matrix (Pennington et al., 2014).

#### 4. Results

On the word analogy task, 300-dimensional GloVe vectors trained on 6 billion tokens (Wikipedia 2014 plus Gigaword 5) reached 71.7% overall, against 69.1% for skip-gram and 65.7% for CBOW trained by the authors on the same corpus; trained on 42 billion tokens of Common Crawl, GloVe reached 75.0% (Pennington et al., 2014). With equal training time on the same 6-billion-token corpus, GloVe outperformed both Word2Vec variants in the authors' comparison. Vectors were also released for an 840-billion-token web corpus (Pennington et al., 2014).

#### Origin and variants

Jeffrey Pennington, Richard Socher and Christopher Manning at Stanford presented GloVe at EMNLP 2014 and released pre-trained vectors (Pennington et al., 2014). Contextual models such as [[bert|BERT]] later added vectors that depend on the sentence ([[embeddings|embeddings]]). Bolukbasi et al. (2016) found that gender bias in word embeddings is captured by a direction in the vector space, which can be measured for any static embedding ([[bias-in-nlp|bias in NLP]]).

### When to use it

- Pre-trained, lightweight word vectors for similarity, [[clustering|clustering]] or as features ([[embeddings|embeddings]]).
- Analysing word associations in a corpus, including stereotypes (Bolukbasi et al., 2016).
- When global co-occurrence statistics of a fixed corpus are to be captured cheaply (Pennington et al., 2014).

### Strengths and limitations

**Strengths**
- Uses global co-occurrence statistics efficiently by training only on non-zero entries (Pennington et al., 2014).
- Strong analogy and similarity performance with fast training (Pennington et al., 2014).
- Pre-trained vectors for several corpus sizes are available (Pennington et al., 2014).

**Limitations**
- One vector per word type, independent of context.
- The co-occurrence matrix must be built and stored before training, which grows with vocabulary size (Pennington et al., 2014).
- Reproduces stereotypes present in the training text (Bolukbasi et al., 2016).

### Comparison

| | GloVe | [[word2vec\|Word2Vec]] | [[latent-semantic-indexing\|LSA / LSI]] |
|---|---|---|---|
| Input | global co-occurrence counts | local context windows | term-document matrix |
| Objective | weighted least squares on log counts | predict context words | truncated SVD |
| Analogy task (6B tokens, 300 d) | 71.7% | 69.1% (skip-gram) | far lower (SVD baselines) |

Source: Pennington et al. (2014).

### In practice

The authors released pre-trained vectors and report that the weighting parameters x_max and α need little tuning, since performance depends only weakly on x_max (Pennington et al., 2014). Before using them in applications that affect people, associations should be measured ([[fairness-metrics|fairness metrics]]), as Bolukbasi et al. (2016) showed for embeddings trained on news text.

### Key takeaway

GloVe fits word vectors so that their dot products match the logarithm of global co-occurrence counts, weighted to downplay rare and very frequent pairs; it unites matrix factorisation and local-window ideas and gives strong static word embeddings, with the same context-blindness and bias issues as Word2Vec.

### Sources

- Pennington, J., Socher, R. & Manning, C. D. (2014). *GloVe: Global Vectors for Word Representation.* EMNLP 2014. [nlp.stanford.edu](https://nlp.stanford.edu/pubs/glove.pdf)
- Bolukbasi, T., Chang, K.-W., Zou, J., Saligrama, V. & Kalai, A. (2016). *Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings.* NeurIPS 2016. [arXiv:1607.06520](https://arxiv.org/abs/1607.06520)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

GloVe (Global Vectors for Word Representation) lernt statische Wortvektoren, indem es sie an den Logarithmus globaler Kookkurrenzzählungen von Wortpaaren anpasst: Für jedes Paar von Wörtern, die im Korpus gemeinsam vorkommen, soll das Skalarprodukt ihrer Vektoren plus zwei Bias-Terme dem Logarithmus ihrer gemeinsamen Häufigkeit entsprechen, gewichtet so, dass seltene und sehr häufige Paare weniger zählen (Pennington et al., 2014). Es verbindet die globale Statistik von Matrixfaktorisierungsverfahren wie der latenten semantischen Analyse mit dem Training auf lokalen Fenstern von [[word2vec|Word2Vec]] und trainiert nur auf den von null verschiedenen Einträgen der Kookkurrenzmatrix (Pennington et al., 2014). Auf 42 Milliarden Token trainiert, erreichte GloVe 75 % bei der Wortanalogieaufgabe, mehr als die Word2Vec-Baselines im Paper (Pennington et al., 2014). Auf großen Textmengen trainierte Wort-Embeddings können Geschlechterstereotype kodieren, was auch für GloVe-Vektoren zu prüfen ist (Bolukbasi et al., 2016).

### Funktionsweise

```text
Korpus → Kookkurrenzmatrix X  (X_ij = wie oft Wort j im Kontextfenster von Wort i vorkommt)
 ▼
Modell: w_iᵀ w̃_j + b_i + b̃_j ≈ log X_ij        (Wortvektor, Kontextvektor, zwei Bias-Terme)
 ▼
gewichtete kleinste Quadrate über von null verschiedene X_ij:
   J = Σ f(X_ij) (w_iᵀ w̃_j + b_i + b̃_j − log X_ij)²
   f(x) = (x / x_max)^α  für x < x_max, sonst 1     (x_max = 100, α = 3/4)
 ▼
Wortvektor = w + w̃
```

#### 1. Verhältnisse von Kookkurrenzwahrscheinlichkeiten

Pennington et al. (2014) gehen von der Beobachtung aus, dass sich Bedeutung in Verhältnissen von Kookkurrenzwahrscheinlichkeiten zeigt. Für die Zielwörter „ice“ und „steam“ ist das Verhältnis P(k|ice)/P(k|steam) groß für ein Kontextwort k, das mit Eis, aber nicht mit Dampf zusammenhängt, etwa „solid“ (8,9 in ihrem Korpus), klein für eines, das mit Dampf zusammenhängt, etwa „gas“, und nahe 1 für Wörter, die mit beiden zusammenhängen, etwa „water“, oder mit keinem, etwa „fashion“. Unterschiede zwischen Wortvektoren sollten daher solche Verhältnisse kodieren, was zu einem Modell führt, in dem das Skalarprodukt zweier Vektoren den Logarithmus ihrer Kookkurrenzzahl annähert (Pennington et al., 2014).

#### 2. Die gewichtete Zielfunktion der kleinsten Quadrate

Das Modell passt `w_iᵀ w̃_j + b_i + b̃_j = log X_ij` für alle gemeinsam vorkommenden Paare an, wobei w Wortvektoren, w̃ eigene Kontextvektoren und b, b̃ Bias-Terme sind (Pennington et al., 2014). Eine einfache Anpassung nach kleinsten Quadraten würde alle Kookkurrenzen gleich gewichten, obwohl seltene verrauscht sind und Nulleinträge 75 bis 95 % der Matrix ausmachen. GloVe gewichtet daher jeden quadrierten Fehler mit `f(X_ij)`, das für nicht beobachtete Paare null ist, mit der Zählung wächst und oberhalb von `x_max` bei 1 gedeckelt ist; die Autoren nutzen `x_max = 100` und `α = 3/4` und merken an, dass Word2Vec eine ähnliche Potenz von 3/4 als nützlich fand (Pennington et al., 2014). Trainiert wird mit AdaGrad nur auf den von null verschiedenen Einträgen, und die Summe aus Wort- und Kontextvektor dient als endgültiges Embedding.

#### 3. Verhältnis zu anderen Verfahren

Matrixfaktorisierungsverfahren wie die latente semantische Analyse ([[latent-semantic-indexing|Latent Semantic Indexing]]) nutzen globale Statistik effizient, schneiden aber bei Analogien schlecht ab; Verfahren mit lokalen Fenstern wie Skip-gram schneiden bei Analogien gut ab, nutzen globale Zählungen aber nicht direkt (Pennington et al., 2014). GloVe will beides verbinden: Es ist eine log-bilineare Regression auf der globalen Kookkurrenzmatrix, und die Autoren zeigen, dass sich die Zielfunktion von Skip-gram auf eine gewichtete Faktorisierung derselben Matrix zurückführen lässt (Pennington et al., 2014).

#### 4. Ergebnisse

Bei der Wortanalogieaufgabe erreichten 300-dimensionale GloVe-Vektoren, trainiert auf 6 Milliarden Token (Wikipedia 2014 plus Gigaword 5), insgesamt 71,7 %, gegenüber 69,1 % für Skip-gram und 65,7 % für CBOW, von den Autoren auf demselben Korpus trainiert; auf 42 Milliarden Token aus Common Crawl erreichte GloVe 75,0 % (Pennington et al., 2014). Bei gleicher Trainingszeit auf demselben Korpus aus 6 Milliarden Token übertraf GloVe im Vergleich der Autoren beide Word2Vec-Varianten. Vektoren wurden auch für einen Webkorpus aus 840 Milliarden Token veröffentlicht (Pennington et al., 2014).

#### Herkunft und Varianten

Jeffrey Pennington, Richard Socher und Christopher Manning von der Stanford University stellten GloVe auf der EMNLP 2014 vor und veröffentlichten vortrainierte Vektoren (Pennington et al., 2014). Kontextuelle Modelle wie [[bert|BERT]] ergänzten später Vektoren, die vom Satz abhängen ([[embeddings|Embeddings]]). Bolukbasi et al. (2016) fanden, dass Geschlechter-Bias in Wort-Embeddings durch eine Richtung im Vektorraum erfasst wird, die sich für jedes statische Embedding messen lässt ([[bias-in-nlp|Bias in NLP]]).

### Wann einsetzen

- Vortrainierte, leichtgewichtige Wortvektoren für Ähnlichkeit, [[clustering|Clustering]] oder als Merkmale ([[embeddings|Embeddings]]).
- Wortassoziationen in einem Korpus untersuchen, einschließlich Stereotypen (Bolukbasi et al., 2016).
- Wenn globale Kookkurrenzstatistiken eines festen Korpus günstig erfasst werden sollen (Pennington et al., 2014).

### Stärken und Grenzen

**Stärken**
- Nutzt globale Kookkurrenzstatistik effizient, indem nur auf von null verschiedenen Einträgen trainiert wird (Pennington et al., 2014).
- Starke Ergebnisse bei Analogien und Ähnlichkeit bei schnellem Training (Pennington et al., 2014).
- Vortrainierte Vektoren für mehrere Korpusgrößen sind verfügbar (Pennington et al., 2014).

**Grenzen**
- Ein Vektor je Worttyp, unabhängig vom Kontext.
- Die Kookkurrenzmatrix muss vor dem Training aufgebaut und gespeichert werden und wächst mit dem Vokabular (Pennington et al., 2014).
- Gibt Stereotype aus dem Trainingstext wieder (Bolukbasi et al., 2016).

### Vergleich

| | GloVe | [[word2vec\|Word2Vec]] | [[latent-semantic-indexing\|LSA / LSI]] |
|---|---|---|---|
| Eingabe | globale Kookkurrenzzählungen | lokale Kontextfenster | Term-Dokument-Matrix |
| Zielfunktion | gewichtete kleinste Quadrate auf Log-Zählungen | Kontextwörter vorhersagen | abgeschnittene SVD |
| Analogieaufgabe (6 Mrd. Token, 300 d) | 71,7 % | 69,1 % (Skip-gram) | deutlich niedriger (SVD-Baselines) |

Quelle: Pennington et al. (2014).

### In der Praxis

Die Autoren veröffentlichten vortrainierte Vektoren und berichten, dass die Gewichtungsparameter x_max und α wenig Abstimmung brauchen, weil die Leistung nur schwach von x_max abhängt (Pennington et al., 2014). Vor dem Einsatz in Anwendungen, die Menschen betreffen, sollten die Assoziationen gemessen werden ([[fairness-metrics|Fairness-Metriken]]), wie Bolukbasi et al. (2016) für auf Nachrichtentexten trainierte Embeddings zeigten.

### Merksatz

GloVe passt Wortvektoren so an, dass ihre Skalarprodukte dem Logarithmus globaler Kookkurrenzzählungen entsprechen, gewichtet so, dass seltene und sehr häufige Paare weniger zählen; es verbindet Matrixfaktorisierung mit lokalen Fenstern und liefert starke statische Wort-Embeddings, mit derselben Kontextblindheit und denselben Bias-Problemen wie Word2Vec.

### Quellen

- Pennington, J., Socher, R. & Manning, C. D. (2014). *GloVe: Global Vectors for Word Representation.* EMNLP 2014. [nlp.stanford.edu](https://nlp.stanford.edu/pubs/glove.pdf)
- Bolukbasi, T., Chang, K.-W., Zou, J., Saligrama, V. & Kalai, A. (2016). *Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings.* NeurIPS 2016. [arXiv:1607.06520](https://arxiv.org/abs/1607.06520)
