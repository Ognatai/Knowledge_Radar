---
title_en: N-gram Language Models and Smoothing
title_de: N-Gramm-Sprachmodelle und Glättung
entity_type: Method
aliases:
- N-gram language model
- N-gram model
- Bigram model
- Trigram model
- Kneser-Ney smoothing
- Laplace smoothing
- Add-one smoothing
- Stupid backoff
sources:
- https://web.stanford.edu/~jurafsky/slp3/3.pdf
- https://web.stanford.edu/~jurafsky/slp3/C.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A language model assigns a probability to each possible next word and to whole sentences; an n-gram model makes the Markov assumption that the next word depends only on the previous n−1 words and estimates the probabilities by counting and normalising (maximum likelihood estimation) (Jurafsky & Martin, 2026, ch. 3). Language models are evaluated by perplexity, the inverse probability of a test set normalised by its length. Because any corpus misses acceptable word sequences, smoothing moves probability mass to unseen n-grams: Laplace (add-one), add-k, interpolation, backoff, and, as the standard baseline, interpolated Kneser-Ney (Jurafsky & Martin, 2026, ch. 3, App. C).

### How it works

```text
corpus ─► counts C(w_{n-1} w_n) ─► MLE P(w_n | w_{n-1}) = C(w_{n-1} w_n) / C(w_{n-1})
sentence ─► chain rule + Markov assumption ─► P(w_1:n) ≈ Π P(w_k | w_{k-1})   (in log space)
zeros in test data ─► smoothing: add-one · add-k · interpolation · backoff · Kneser-Ney
test set ─► perplexity = P(w_1 … w_N)^(-1/N)   (lower is better)
```

#### 1. The Markov assumption

The chain rule writes the probability of a sequence as the product of each word's probability given all previous words, but long histories cannot be counted because language is creative. A bigram model approximates P(w_n | w_1:n−1) by P(w_n | w_n−1); trigram, 4-gram and 5-gram models look two to four words back. Sentences are padded with `<s>` and `</s>` so that the bigram model is a true probability distribution (Jurafsky & Martin, 2026, ch. 3).

#### 2. Maximum likelihood estimation

The MLE of a bigram probability is the bigram count divided by the count of the preceding word. In the Berkeley Restaurant Project corpus, P(i | `<s>`) = 0.25 and P(want | i) = 0.33; the bigram statistics encode syntax (after *to* usually comes a verb), task facts (sentences start with *I*) and even cultural preferences (Chinese over English food). Probabilities are stored as log probabilities to avoid numerical underflow (Jurafsky & Martin, 2026, ch. 3).

#### 3. Perplexity

Models are compared on a held-out test set; the better model assigns it a higher probability. Perplexity normalises this by length: the N-th root of the inverse test-set probability, so lower perplexity means a better model. On the Wall Street Journal, unigram, bigram and trigram models trained on 38 million words reached perplexities of 962, 170 and 109. Perplexity is only comparable with identical vocabularies, and an intrinsic improvement does not guarantee an extrinsic improvement in a task such as speech recognition. It can be read as a weighted average branching factor and is 2 raised to the cross-entropy (Jurafsky & Martin, 2026, ch. 3).

#### 4. Laplace and add-k smoothing

Unseen n-grams get probability zero, which underestimates real sequences and makes perplexity undefined. Laplace smoothing adds one to every count: P(w_n | w_n−1) = (C(w_n−1 w_n) + 1) / (C(w_n−1) + V). It moves too much mass to the zeros: in the restaurant corpus P(to | want) fell from 0.66 to 0.26. Add-k adds a fraction k instead; both are useful for text [[classification|classification]] but do not work well for language modelling (Jurafsky & Martin, 2026, ch. 3).

#### 5. Interpolation and backoff

Interpolation mixes unigram, bigram and trigram estimates with weights λ that sum to 1, optionally conditioned on the context; the λs are set on a held-out corpus, for example with the EM algorithm. Backoff uses a lower-order n-gram only when the higher-order one has zero count; to remain a probability distribution it must discount the higher orders. Stupid backoff (Brants et al., 2007) gives that up and multiplies the lower-order score by a fixed weight, with λ = 0.4 working well (Jurafsky & Martin, 2026, ch. 3).

#### 6. Kneser-Ney smoothing

Absolute discounting subtracts a fixed discount d from each count: Church and Gale found that a bigram seen 4 times in 22 million words of AP newswire occurred on average 3.23 times in another 22 million, so d ≈ 0.75 fits. Kneser-Ney replaces the unigram distribution with a continuation probability: how many different words a word follows. *Kong* is frequent but almost only after *Hong*, so it gets a low continuation probability, whereas *glasses* follows many words. Modified Kneser-Ney (Chen & Goodman, 1998) uses three discounts for counts of 1, 2 and three or more (Jurafsky & Martin, 2026, App. C).

#### Origin and variants

Markov (1913) used bigrams and trigrams of letters in Pushkin's *Eugene Onegin*; Shannon (1948) applied n-grams to English word sequences. Chomsky's arguments that finite-state Markov processes cannot model grammar led many linguists to ignore statistical modelling for decades, until IBM (Jelinek) and CMU (Baker) used n-grams for speech recognition; the IBM group coined the terms *language model* and *perplexity*. Modified interpolated Kneser-Ney became the standard n-gram baseline around 2000; SRILM and KenLM are public toolkits (Jurafsky & Martin, 2026, ch. 3).

### When to use it

- To introduce training and test sets, perplexity, sampling and interpolation, which carry over to large language models (Jurafsky & Martin, 2026, ch. 3).
- Choosing the more probable variant in spelling and grammar correction or speech recognition, and word prediction in augmentative and alternative communication (Jurafsky & Martin, 2026, ch. 3).
- Very large n-gram counts: Google Web 5-grams from 1 trillion words, Google Books Ngrams, or infini-gram, which computes n-grams of any length over 5 trillion tokens with suffix arrays (Jurafsky & Martin, 2026, ch. 3).

### Strengths and limitations

**Strengths**
- Simple, transparent formalisation, trained by counting (Jurafsky & Martin, 2026, ch. 3).
- Scales with quantised probabilities, hashed words, reverse tries and pruning (Jurafsky & Martin, 2026, ch. 3).

**Limitations**
- The number of parameters grows exponentially with n, and n-grams cannot generalise to contexts that use different words; neural models solve both by representing words in a continuous space (Jurafsky & Martin, 2026, ch. 3).
- Strong dependence on the training corpus: models trained on Shakespeare and on the Wall Street Journal generate sentences with almost no overlap, so genre and dialect of the training data must match the task (Jurafsky & Martin, 2026, ch. 3).
- Natural language is not stationary, so n-gram models only approximate its distribution (Jurafsky & Martin, 2026, ch. 3).

### Comparison

| Smoothing | Idea | Assessment |
|-----------|------|------------|
| Laplace (add-one) | Add 1 to every count | Moves too much mass to zeros (ch. 3) |
| Add-k | Add a fraction k | Still poor variances for LMs (ch. 3) |
| Interpolation | Weighted mix of orders | λs from held-out data (ch. 3) |
| Stupid backoff | Fall back with fixed weight 0.4 | Not a true distribution (ch. 3) |
| Interpolated Kneser-Ney | Absolute discount + continuation probability | Standard baseline (ch. 3, App. C) |

Source: Jurafsky & Martin (2026).

### In practice

Language models today are mostly computed over subword tokens, so a test set never contains unseen tokens ([[tokenization|Tokenisation]]) (Jurafsky & Martin, 2026, ch. 3). Laplace smoothing is a practical choice for text classification such as [[naive-bayes|Naive Bayes]] (Jurafsky & Martin, 2026, ch. 3). Large language models are trained on the same next-word objective ([[large-language-models|Large Language Models]]), and n-gram models were long a component of [[automatic-speech-recognition|Automatic Speech Recognition]] (Jurafsky & Martin, 2026, ch. 3).

### Key takeaway

An n-gram model predicts the next word from the previous n−1 words with counted probabilities, is evaluated by perplexity, and needs smoothing such as Kneser-Ney for unseen n-grams.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *N-gram Language Models.* Speech and Language Processing, 3rd ed. draft, Chapter 3. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/3.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Kneser-Ney Smoothing.* Speech and Language Processing, 3rd ed. draft, Appendix C. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/C.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Sprachmodell weist jedem möglichen nächsten Wort und ganzen Sätzen eine Wahrscheinlichkeit zu; ein N-Gramm-Modell trifft die Markov-Annahme, dass das nächste Wort nur von den vorherigen n−1 Wörtern abhängt, und schätzt die Wahrscheinlichkeiten durch Zählen und Normalisieren (Maximum-Likelihood-Schätzung) (Jurafsky & Martin, 2026, Kap. 3). Sprachmodelle werden über die Perplexität bewertet, die inverse Wahrscheinlichkeit einer Testmenge, normiert auf ihre Länge. Weil jedem Korpus zulässige Wortfolgen fehlen, verschiebt Glättung Wahrscheinlichkeitsmasse auf ungesehene N-Gramme: Laplace (Add-one), Add-k, Interpolation, Backoff und als Standard-Baseline interpoliertes Kneser-Ney (Jurafsky & Martin, 2026, Kap. 3, Anh. C).

### Funktionsweise

```text
Korpus ─► Zählungen C(w_{n-1} w_n) ─► MLE P(w_n | w_{n-1}) = C(w_{n-1} w_n) / C(w_{n-1})
Satz ─► Kettenregel + Markov-Annahme ─► P(w_1:n) ≈ Π P(w_k | w_{k-1})   (im Log-Raum)
Nullen in Testdaten ─► Glättung: Add-one · Add-k · Interpolation · Backoff · Kneser-Ney
Testmenge ─► Perplexität = P(w_1 … w_N)^(-1/N)   (niedriger ist besser)
```

#### 1. Die Markov-Annahme

Die Kettenregel schreibt die Wahrscheinlichkeit einer Folge als Produkt der Wahrscheinlichkeiten jedes Wortes gegeben alle vorherigen, doch lange Vorgeschichten lassen sich nicht zählen, weil Sprache kreativ ist. Ein Bigramm-Modell nähert P(w_n | w_1:n−1) durch P(w_n | w_n−1) an; Trigramm-, 4-Gramm- und 5-Gramm-Modelle schauen zwei bis vier Wörter zurück. Sätze werden mit `<s>` und `</s>` umrahmt, damit das Bigramm-Modell eine echte Wahrscheinlichkeitsverteilung ist (Jurafsky & Martin, 2026, Kap. 3).

#### 2. Maximum-Likelihood-Schätzung

Die MLE einer Bigramm-Wahrscheinlichkeit ist die Bigramm-Zählung geteilt durch die Zählung des vorangehenden Wortes. Im Korpus des Berkeley Restaurant Project ist P(i | `<s>`) = 0,25 und P(want | i) = 0,33; die Bigramm-Statistiken enthalten Syntax (nach *to* folgt meist ein Verb), Aufgabenwissen (Sätze beginnen mit *I*) und sogar kulturelle Vorlieben (chinesisches statt englisches Essen). Wahrscheinlichkeiten werden als Log-Wahrscheinlichkeiten gespeichert, um numerischen Unterlauf zu vermeiden (Jurafsky & Martin, 2026, Kap. 3).

#### 3. Perplexität

Modelle werden auf einer zurückgehaltenen Testmenge verglichen; das bessere Modell weist ihr eine höhere Wahrscheinlichkeit zu. Die Perplexität normiert das auf die Länge: die N-te Wurzel der inversen Wahrscheinlichkeit der Testmenge, niedrigere Perplexität bedeutet also ein besseres Modell. Auf dem Wall Street Journal erreichten Unigramm-, Bigramm- und Trigramm-Modelle, trainiert auf 38 Millionen Wörtern, Perplexitäten von 962, 170 und 109. Perplexität ist nur bei identischem Vokabular vergleichbar, und eine intrinsische Verbesserung garantiert keine extrinsische in einer Aufgabe wie der Spracherkennung. Sie lässt sich als gewichteter mittlerer Verzweigungsfaktor lesen und ist 2 hoch der Kreuzentropie (Jurafsky & Martin, 2026, Kap. 3).

#### 4. Laplace- und Add-k-Glättung

Ungesehene N-Gramme erhalten die Wahrscheinlichkeit null, was reale Folgen unterschätzt und die Perplexität undefiniert macht. Laplace-Glättung addiert zu jeder Zählung eins: P(w_n | w_n−1) = (C(w_n−1 w_n) + 1) / (C(w_n−1) + V). Sie verschiebt zu viel Masse auf die Nullen: Im Restaurant-Korpus fiel P(to | want) von 0,66 auf 0,26. Add-k addiert stattdessen einen Bruchteil k; beide sind für Textklassifikation nützlich, funktionieren für Sprachmodellierung aber nicht gut (Jurafsky & Martin, 2026, Kap. 3).

#### 5. Interpolation und Backoff

Interpolation mischt Unigramm-, Bigramm- und Trigramm-Schätzungen mit Gewichten λ, die sich zu 1 summieren und optional vom Kontext abhängen; die λ werden auf einem Held-out-Korpus bestimmt, etwa mit dem EM-Algorithmus. Backoff nutzt ein N-Gramm niedrigerer Ordnung nur, wenn das höherer Ordnung die Zählung null hat; um eine Wahrscheinlichkeitsverteilung zu bleiben, muss es die höheren Ordnungen abwerten. Stupid Backoff (Brants et al., 2007) verzichtet darauf und multipliziert den Wert niedrigerer Ordnung mit einem festen Gewicht, wobei λ = 0,4 gut funktionierte (Jurafsky & Martin, 2026, Kap. 3).

#### 6. Kneser-Ney-Glättung

Absolute Discounting zieht von jeder Zählung einen festen Abschlag d ab: Church und Gale fanden, dass ein Bigramm, das in 22 Millionen Wörtern AP-Nachrichten 4-mal vorkam, in weiteren 22 Millionen im Mittel 3,23-mal auftrat, also passt d ≈ 0,75. Kneser-Ney ersetzt die Unigramm-Verteilung durch eine Fortsetzungswahrscheinlichkeit: wie vielen verschiedenen Wörtern ein Wort folgt. *Kong* ist häufig, aber fast nur nach *Hong*, und erhält deshalb eine niedrige Fortsetzungswahrscheinlichkeit, während *glasses* auf viele Wörter folgt. Modifiziertes Kneser-Ney (Chen & Goodman, 1998) nutzt drei Abschläge für Zählungen von 1, 2 und drei oder mehr (Jurafsky & Martin, 2026, Anh. C).

#### Herkunft und Varianten

Markov (1913) nutzte Bigramme und Trigramme von Buchstaben in Puschkins *Eugen Onegin*; Shannon (1948) wandte N-Gramme auf englische Wortfolgen an. Chomskys Argumente, dass endliche Markov-Prozesse Grammatik nicht modellieren können, ließen viele Linguisten die statistische Modellierung jahrzehntelang ignorieren, bis IBM (Jelinek) und CMU (Baker) N-Gramme für die Spracherkennung nutzten; die IBM-Gruppe prägte die Begriffe *Sprachmodell* und *Perplexität*. Modifiziertes interpoliertes Kneser-Ney wurde um 2000 zur Standard-Baseline für N-Gramme; SRILM und KenLM sind öffentliche Werkzeuge (Jurafsky & Martin, 2026, Kap. 3).

### Wann einsetzen

- Um Trainings- und Testmengen, Perplexität, Sampling und Interpolation einzuführen, die sich auf große Sprachmodelle übertragen (Jurafsky & Martin, 2026, Kap. 3).
- Die wahrscheinlichere Variante bei Rechtschreib- und Grammatikkorrektur oder Spracherkennung wählen und Wortvorhersage in der unterstützten Kommunikation (Jurafsky & Martin, 2026, Kap. 3).
- Sehr große N-Gramm-Zählungen: Google Web 5-grams aus 1 Billion Wörtern, Google Books Ngrams oder infini-gram, das N-Gramme beliebiger Länge über 5 Billionen Token mit Suffix-Arrays berechnet (Jurafsky & Martin, 2026, Kap. 3).

### Stärken und Grenzen

**Stärken**
- Einfache, durchschaubare Formalisierung, trainiert durch Zählen (Jurafsky & Martin, 2026, Kap. 3).
- Skaliert mit quantisierten Wahrscheinlichkeiten, gehashten Wörtern, Reverse Tries und Pruning (Jurafsky & Martin, 2026, Kap. 3).

**Grenzen**
- Die Zahl der Parameter wächst exponentiell mit n, und N-Gramme können nicht auf Kontexte mit anderen Wörtern verallgemeinern; neuronale Modelle lösen beides, indem sie Wörter in einem kontinuierlichen Raum darstellen (Jurafsky & Martin, 2026, Kap. 3).
- Starke Abhängigkeit vom Trainingskorpus: Auf Shakespeare und auf dem Wall Street Journal trainierte Modelle erzeugen Sätze fast ohne Überschneidung, daher müssen Genre und Varietät der Trainingsdaten zur Aufgabe passen (Jurafsky & Martin, 2026, Kap. 3).
- Natürliche Sprache ist nicht stationär, daher nähern N-Gramm-Modelle ihre Verteilung nur an (Jurafsky & Martin, 2026, Kap. 3).

### Vergleich

| Glättung | Idee | Bewertung |
|----------|------|-----------|
| Laplace (Add-one) | 1 zu jeder Zählung addieren | Verschiebt zu viel Masse auf Nullen (Kap. 3) |
| Add-k | Bruchteil k addieren | Weiter schlechte Varianzen für LMs (Kap. 3) |
| Interpolation | Gewichtete Mischung der Ordnungen | λ aus Held-out-Daten (Kap. 3) |
| Stupid Backoff | Rückfall mit festem Gewicht 0,4 | Keine echte Verteilung (Kap. 3) |
| Interpoliertes Kneser-Ney | Absoluter Abschlag + Fortsetzungswahrscheinlichkeit | Standard-Baseline (Kap. 3, Anh. C) |

Quelle: Jurafsky & Martin (2026).

### In der Praxis

Sprachmodelle werden heute meist über Subword-Token berechnet, sodass eine Testmenge nie ungesehene Token enthält ([[tokenization|Tokenisierung]]) (Jurafsky & Martin, 2026, Kap. 3). Laplace-Glättung ist für Textklassifikation wie [[naive-bayes|Naive Bayes]] eine praktische Wahl (Jurafsky & Martin, 2026, Kap. 3). Große Sprachmodelle werden auf dasselbe Ziel der Wortvorhersage trainiert ([[large-language-models|Große Sprachmodelle]]), und N-Gramm-Modelle waren lange Bestandteil der [[automatic-speech-recognition|automatischen Spracherkennung]] (Jurafsky & Martin, 2026, Kap. 3).

### Merksatz

Ein N-Gramm-Modell sagt das nächste Wort aus den vorherigen n−1 Wörtern mit gezählten Wahrscheinlichkeiten voraus, wird über Perplexität bewertet und braucht Glättung wie Kneser-Ney für ungesehene N-Gramme.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *N-gram Language Models.* Speech and Language Processing, 3rd ed. draft, Chapter 3. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/3.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Kneser-Ney Smoothing.* Speech and Language Processing, 3rd ed. draft, Appendix C. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/C.pdf)
