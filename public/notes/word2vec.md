---
title_en: Word2Vec
title_de: Word2Vec
entity_type: Method
aliases:
- word2vec
- Word2Vec
- Skip-gram
- CBOW
- Continuous bag-of-words
sources:
- https://arxiv.org/abs/1301.3781
- https://arxiv.org/abs/1310.4546
- https://arxiv.org/abs/1607.06520
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Word2Vec is a family of two shallow neural models from Google that learn a dense vector for every word from its contexts in a large corpus: continuous bag-of-words (CBOW) predicts a word from its surrounding words, and skip-gram predicts the surrounding words from a word (Mikolov et al., 2013a). Trained in less than a day on 1.6 billion words, the vectors capture syntactic and semantic regularities, so that vector arithmetic such as "King" − "Man" + "Woman" lands closest to "Queen" (Mikolov et al., 2013a). Negative sampling and subsampling of frequent words made training faster and the vectors better, and frequent phrases can be learned as single tokens (Mikolov et al., 2013b). Word2Vec gives one static vector per word regardless of context, which contextual models such as [[bert|BERT]] later replaced for most tasks, and its vectors reproduce social stereotypes in the training text (Bolukbasi et al., 2016).

### How it works

```text
corpus (billions of words) → vocabulary (e.g. 1 million most frequent words)
 ▼ subsample frequent words: drop w with probability 1 − √(t / f(w)), t ≈ 10⁻⁵
 ▼ slide a context window (up to C words on each side)
CBOW:      average of context word vectors → predict the centre word
skip-gram: centre word vector → predict each context word
 ▼ output layer: hierarchical softmax over a Huffman tree, or negative sampling with k noise words
 ▼ learned input vectors = word embeddings (e.g. 300 dimensions)
```

#### 1. From atomic words to vectors

Many NLP systems treated words as atomic indices with no notion of similarity; Word2Vec instead learns continuous vectors in which similar words are close (Mikolov et al., 2013a). The models remove the non-linear hidden layer of earlier neural language models, keeping only a projection layer and a log-linear classifier, which cuts training cost enough to use billions of words. The idea of distributed word representations goes back to Rumelhart, Hinton and Williams in 1986 (Mikolov et al., 2013b). Embeddings in general are covered in [[embeddings|embeddings]].

#### 2. CBOW and skip-gram

CBOW projects the vectors of the surrounding words, four before and four after in the best setting, into one averaged vector and classifies the current word; word order in the window does not matter, hence "bag of words" (Mikolov et al., 2013a). Skip-gram reverses this: the current word is the input, and the model predicts words within a window of up to C positions before and after it, sampling distant words less often because they are usually less related. Skip-gram was slightly worse than CBOW on syntactic questions but much better on semantic ones; with 300 dimensions trained on 783 million words, it reached 53.3% total accuracy on the analogy test set against 36.1% for CBOW (Mikolov et al., 2013a).

#### 3. Efficient output layers

A full softmax over a vocabulary of V words is expensive. Hierarchical softmax arranges the vocabulary in a Huffman tree so that only about log₂(V) outputs are evaluated per word (Mikolov et al., 2013a). Negative sampling replaces the softmax with a [[classification|logistic regression]] that distinguishes the observed context word from k words drawn from a noise distribution: `log σ(v′_O · v_I) + Σ_{i=1..k} E_{w_i ∼ P_n} [log σ(−v′_{w_i} · v_I)]` (Mikolov et al., 2013b). Values of k from 5 to 20 suit small datasets, 2 to 5 large ones, and the unigram distribution raised to the power 3/4 worked best as noise distribution. On the analogy task, negative sampling outperformed hierarchical softmax (Mikolov et al., 2013b).

#### 4. Subsampling and phrases

Very frequent words such as "the" carry little information; each occurrence of word w is discarded with probability `1 − √(t / f(w))`, where f(w) is its frequency and t a threshold around 10⁻⁵, which sped up training several times and improved the vectors of rare words (Mikolov et al., 2013b). Phrases whose meaning is not the sum of their parts, such as "Air Canada" or "New York Times", are detected from co-occurrence statistics and replaced by single tokens before training; with 1,000-dimensional vectors trained on about 33 billion words, phrase analogies were solved with 72% accuracy (Mikolov et al., 2013b).

#### 5. Linear regularities

Mikolov et al. (2013a) built a test set of 8,869 semantic and 10,675 syntactic analogy questions, such as "Athens is to Greece as Oslo is to ?" or "great is to greater as tough is to ?", answered by finding the word closest to `vec(b) − vec(a) + vec(c)`. Skip-gram vectors also combine by addition: the sum of "Russian" and "river" is close to "Volga River" (Mikolov et al., 2013b). A PCA projection of country and capital vectors shows parallel offsets, although no information about capitals was given in training (Mikolov et al., 2013b).

#### Origin and variants

Tomas Mikolov, Kai Chen, Greg Corrado and Jeffrey Dean at Google introduced CBOW and skip-gram in 2013, and a NIPS 2013 paper with Ilya Sutskever added negative sampling, subsampling and phrases (Mikolov et al., 2013a; 2013b). [[glove|GloVe]] learns similar vectors from global co-occurrence counts. Contextual models such as [[bert|BERT]] give each occurrence of a word its own vector ([[attention-and-transformers|attention and Transformers]]).

### When to use it

- Lightweight word similarity, [[clustering|clustering]] or features where context-dependent meaning is not needed ([[embeddings|embeddings]]).
- Studying how meanings and associations are encoded in a corpus, including social bias (Bolukbasi et al., 2016).
- Domain-specific vocabularies where a small model can be trained quickly on in-house text (Mikolov et al., 2013a).

### Strengths and limitations

**Strengths**
- Very cheap to train: an optimised single-machine implementation can process more than 100 billion words in a day (Mikolov et al., 2013b).
- Captures syntactic and semantic regularities that support analogies and similarity (Mikolov et al., 2013a).

**Limitations**
- One vector per word type: "bank" has the same vector in every sentence (Mikolov et al., 2013b note the indifference to word order and idioms).
- Words outside the vocabulary get no vector (Mikolov et al., 2013a).
- Embeddings trained on news text "exhibit female/male gender stereotypes to a disturbing extent" (Bolukbasi et al., 2016); see [[bias-in-nlp|bias in NLP]].

### Comparison

| | Word2Vec | [[glove\|GloVe]] | [[bert\|BERT]] embeddings |
|---|---|---|---|
| Training signal | predict words in a local window | factorise global co-occurrence counts | masked language modelling |
| Vector per | word type | word type | word occurrence (contextual) |
| Cost | very low | low | high |

Sources: Mikolov et al. (2013a; 2013b); see the linked notes for GloVe and BERT.

### In practice

Typical settings are 100 to 300 dimensions, a window of about 5 and negative sampling with 5 to 20 noise words, plus subsampling (Mikolov et al., 2013a; 2013b). Analogy accuracy rises with both dimensionality and amount of training data, so increasing only one of them gives diminishing returns (Mikolov et al., 2013a). Before using pre-trained vectors in decisions about people, their associations should be measured ([[fairness-metrics|fairness metrics]], [[bias-in-nlp|bias in NLP]]).

### Key takeaway

Word2Vec learns static word vectors by predicting words from their local context (CBOW) or context from words (skip-gram), made cheap by negative sampling and subsampling; the vectors encode analogies and similarities, but also the stereotypes of their training text.

### Sources

- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013a). *Efficient Estimation of Word Representations in Vector Space.* arXiv:1301.3781. [arXiv:1301.3781](https://arxiv.org/abs/1301.3781)
- Mikolov, T., Sutskever, I., Chen, K., Corrado, G. & Dean, J. (2013b). *Distributed Representations of Words and Phrases and their Compositionality.* NIPS 2013. [arXiv:1310.4546](https://arxiv.org/abs/1310.4546)
- Bolukbasi, T., Chang, K.-W., Zou, J., Saligrama, V. & Kalai, A. (2016). *Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings.* NeurIPS 2016. [arXiv:1607.06520](https://arxiv.org/abs/1607.06520)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Word2Vec ist eine Familie aus zwei flachen neuronalen Modellen von Google, die aus den Kontexten in einem großen Korpus für jedes Wort einen dichten Vektor lernen: Continuous Bag-of-Words (CBOW) sagt ein Wort aus den umgebenden Wörtern vorher, Skip-gram die umgebenden Wörter aus einem Wort (Mikolov et al., 2013a). In weniger als einem Tag auf 1,6 Milliarden Wörtern trainiert, erfassen die Vektoren syntaktische und semantische Regelmäßigkeiten, sodass Vektorrechnungen wie „King“ − „Man“ + „Woman“ am nächsten bei „Queen“ landen (Mikolov et al., 2013a). Negative Sampling und das Ausdünnen häufiger Wörter machten das Training schneller und die Vektoren besser, und häufige Wortgruppen lassen sich als einzelne Token lernen (Mikolov et al., 2013b). Word2Vec liefert einen statischen Vektor je Wort unabhängig vom Kontext, den kontextuelle Modelle wie [[bert|BERT]] später für die meisten Aufgaben ablösten, und seine Vektoren geben soziale Stereotype des Trainingstexts wieder (Bolukbasi et al., 2016).

### Funktionsweise

```text
Korpus (Milliarden Wörter) → Vokabular (z. B. 1 Million häufigste Wörter)
 ▼ häufige Wörter ausdünnen: w mit Wahrscheinlichkeit 1 − √(t / f(w)) verwerfen, t ≈ 10⁻⁵
 ▼ Kontextfenster verschieben (bis zu C Wörter auf jeder Seite)
CBOW:      Mittel der Kontextvektoren → mittleres Wort vorhersagen
Skip-gram: Vektor des mittleren Worts → jedes Kontextwort vorhersagen
 ▼ Ausgabeschicht: hierarchischer Softmax über einen Huffman-Baum oder Negative Sampling mit k Rauschwörtern
 ▼ gelernte Eingabevektoren = Wort-Embeddings (z. B. 300 Dimensionen)
```

#### 1. Von atomaren Wörtern zu Vektoren

Viele NLP-Systeme behandelten Wörter als atomare Indizes ohne jede Vorstellung von Ähnlichkeit; Word2Vec lernt stattdessen stetige Vektoren, in denen ähnliche Wörter nahe beieinanderliegen (Mikolov et al., 2013a). Die Modelle verzichten auf die nichtlineare verborgene Schicht früherer neuronaler Sprachmodelle und behalten nur eine Projektionsschicht und einen log-linearen Klassifikator, was die Trainingskosten so weit senkt, dass Milliarden Wörter nutzbar werden. Die Idee verteilter Wortrepräsentationen geht auf Rumelhart, Hinton und Williams 1986 zurück (Mikolov et al., 2013b). Embeddings allgemein behandelt [[embeddings|Embeddings]].

#### 2. CBOW und Skip-gram

CBOW projiziert die Vektoren der umgebenden Wörter, in der besten Einstellung vier davor und vier danach, auf einen gemittelten Vektor und klassifiziert das aktuelle Wort; die Wortreihenfolge im Fenster spielt keine Rolle, daher „Bag of Words“ (Mikolov et al., 2013a). Skip-gram kehrt das um: Das aktuelle Wort ist die Eingabe, und das Modell sagt Wörter in einem Fenster von bis zu C Positionen davor und danach vorher, wobei entfernte Wörter seltener gezogen werden, weil sie meist weniger verwandt sind. Skip-gram war bei syntaktischen Fragen etwas schlechter als CBOW, bei semantischen aber deutlich besser; mit 300 Dimensionen und 783 Millionen Trainingswörtern erreichte es auf dem Analogietest 53,3 % Gesamtgenauigkeit gegenüber 36,1 % für CBOW (Mikolov et al., 2013a).

#### 3. Effiziente Ausgabeschichten

Ein voller Softmax über ein Vokabular aus V Wörtern ist teuer. Der hierarchische Softmax ordnet das Vokabular in einem Huffman-Baum an, sodass je Wort nur etwa log₂(V) Ausgaben berechnet werden (Mikolov et al., 2013a). Negative Sampling ersetzt den Softmax durch eine logistische Regression, die das beobachtete Kontextwort von k Wörtern aus einer Rauschverteilung unterscheidet: `log σ(v′_O · v_I) + Σ_{i=1..k} E_{w_i ∼ P_n} [log σ(−v′_{w_i} · v_I)]` (Mikolov et al., 2013b). Werte von k zwischen 5 und 20 passen zu kleinen Datensätzen, 2 bis 5 zu großen, und die Unigramm-Verteilung hoch 3/4 funktionierte als Rauschverteilung am besten. Bei der Analogieaufgabe übertraf Negative Sampling den hierarchischen Softmax (Mikolov et al., 2013b).

#### 4. Ausdünnen und Wortgruppen

Sehr häufige Wörter wie „the“ tragen wenig Information; jedes Vorkommen eines Worts w wird mit Wahrscheinlichkeit `1 − √(t / f(w))` verworfen, wobei f(w) seine Häufigkeit und t ein Schwellenwert um 10⁻⁵ ist, was das Training um ein Mehrfaches beschleunigte und die Vektoren seltener Wörter verbesserte (Mikolov et al., 2013b). Wortgruppen, deren Bedeutung nicht die Summe ihrer Teile ist, etwa „Air Canada“ oder „New York Times“, werden anhand von Kookkurrenzstatistiken erkannt und vor dem Training durch einzelne Token ersetzt; mit 1.000-dimensionalen Vektoren, trainiert auf etwa 33 Milliarden Wörtern, wurden Analogien zu Wortgruppen mit 72 % Genauigkeit gelöst (Mikolov et al., 2013b).

#### 5. Lineare Regelmäßigkeiten

Mikolov et al. (2013a) bauten einen Test aus 8.869 semantischen und 10.675 syntaktischen Analogiefragen, etwa „Athens verhält sich zu Greece wie Oslo zu ?“ oder „great zu greater wie tough zu ?“, die beantwortet werden, indem das Wort gesucht wird, das `vec(b) − vec(a) + vec(c)` am nächsten liegt. Skip-gram-Vektoren lassen sich auch addieren: Die Summe aus „Russian“ und „river“ liegt nahe bei „Volga River“ (Mikolov et al., 2013b). Eine PCA-Projektion der Vektoren von Ländern und Hauptstädten zeigt parallele Abstände, obwohl im Training keine Information über Hauptstädte vorlag (Mikolov et al., 2013b).

#### Herkunft und Varianten

Tomas Mikolov, Kai Chen, Greg Corrado und Jeffrey Dean stellten CBOW und Skip-gram 2013 bei Google vor, und ein Paper auf der NIPS 2013 mit Ilya Sutskever ergänzte Negative Sampling, Ausdünnen und Wortgruppen (Mikolov et al., 2013a; 2013b). [[glove|GloVe]] lernt ähnliche Vektoren aus globalen Kookkurrenzzählungen. Kontextuelle Modelle wie [[bert|BERT]] geben jedem Vorkommen eines Worts einen eigenen Vektor ([[attention-and-transformers|Attention und Transformer]]).

### Wann einsetzen

- Leichtgewichtige Wortähnlichkeit, [[clustering|Clustering]] oder Merkmale, wenn kontextabhängige Bedeutung nicht nötig ist ([[embeddings|Embeddings]]).
- Untersuchen, wie Bedeutungen und Assoziationen in einem Korpus kodiert sind, einschließlich sozialer Verzerrungen (Bolukbasi et al., 2016).
- Fachvokabulare, für die sich ein kleines Modell schnell auf eigenen Texten trainieren lässt (Mikolov et al., 2013a).

### Stärken und Grenzen

**Stärken**
- Sehr günstig zu trainieren: Eine optimierte Implementierung auf einem Rechner kann mehr als 100 Milliarden Wörter an einem Tag verarbeiten (Mikolov et al., 2013b).
- Erfasst syntaktische und semantische Regelmäßigkeiten, die Analogien und Ähnlichkeit tragen (Mikolov et al., 2013a).

**Grenzen**
- Ein Vektor je Worttyp: „Bank“ hat in jedem Satz denselben Vektor (Mikolov et al., 2013b nennen die Gleichgültigkeit gegenüber Wortreihenfolge und Redewendungen).
- Wörter außerhalb des Vokabulars erhalten keinen Vektor (Mikolov et al., 2013a).
- Auf Nachrichtentexten trainierte Embeddings „exhibit female/male gender stereotypes to a disturbing extent“ (Bolukbasi et al., 2016); siehe [[bias-in-nlp|Bias in NLP]].

### Vergleich

| | Word2Vec | [[glove\|GloVe]] | [[bert\|BERT]]-Embeddings |
|---|---|---|---|
| Trainingssignal | Wörter im lokalen Fenster vorhersagen | globale Kookkurrenzzählungen faktorisieren | Masked Language Modelling |
| Vektor je | Worttyp | Worttyp | Wortvorkommen (kontextuell) |
| Kosten | sehr gering | gering | hoch |

Quellen: Mikolov et al. (2013a; 2013b); zu GloVe und BERT siehe die verlinkten Notizen.

### In der Praxis

Übliche Einstellungen sind 100 bis 300 Dimensionen, ein Fenster von etwa 5 und Negative Sampling mit 5 bis 20 Rauschwörtern, dazu Ausdünnen (Mikolov et al., 2013a; 2013b). Die Analogiegenauigkeit steigt mit Dimensionalität und Trainingsdatenmenge zugleich, sodass das Erhöhen nur einer Größe abnehmenden Nutzen bringt (Mikolov et al., 2013a). Bevor vortrainierte Vektoren in Entscheidungen über Menschen einfließen, sollten ihre Assoziationen gemessen werden ([[fairness-metrics|Fairness-Metriken]], [[bias-in-nlp|Bias in NLP]]).

### Merksatz

Word2Vec lernt statische Wortvektoren, indem es Wörter aus ihrem lokalen Kontext (CBOW) oder den Kontext aus Wörtern (Skip-gram) vorhersagt, günstig gemacht durch Negative Sampling und Ausdünnen; die Vektoren kodieren Analogien und Ähnlichkeiten, aber auch die Stereotype ihres Trainingstexts.

### Quellen

- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013a). *Efficient Estimation of Word Representations in Vector Space.* arXiv:1301.3781. [arXiv:1301.3781](https://arxiv.org/abs/1301.3781)
- Mikolov, T., Sutskever, I., Chen, K., Corrado, G. & Dean, J. (2013b). *Distributed Representations of Words and Phrases and their Compositionality.* NIPS 2013. [arXiv:1310.4546](https://arxiv.org/abs/1310.4546)
- Bolukbasi, T., Chang, K.-W., Zou, J., Saligrama, V. & Kalai, A. (2016). *Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings.* NeurIPS 2016. [arXiv:1607.06520](https://arxiv.org/abs/1607.06520)
