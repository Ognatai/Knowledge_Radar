---
title_en: Naive Bayes for Text Classification
title_de: Naive Bayes für Textklassifikation
entity_type: Method
aliases:
- Naive Bayes
- Multinomial Naive Bayes
- Bernoulli Naive Bayes
- Feature selection for text
sources:
- https://nlp.stanford.edu/IR-book/pdf/13bayes.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Naive Bayes assigns a document to the class c that maximises P(c)·Π P(t_k | c): the prior of the class times the probability of each of its terms in that class, estimated from counts in labelled training documents with [[n-gram-language-models|add-one smoothing]] (Manning et al., 2008, ch. 13). Its independence assumptions are naive for language, so its probability estimates are poor, but its decisions are often good; it trains and classifies in one pass over the data, which makes it a common baseline. Feature selection with mutual information or χ² removes noise terms (Manning et al., 2008, ch. 13). For the general picture of classifiers, see [[classification|Classification]].

### How it works

```text
training documents with classes ─► counts per class: documents (prior), term occurrences
                                 ─► P(c) = N_c / N,  P(t|c) = (T_ct + 1) / (Σ T_ct' + |V|)
new document t1 … tn ─► score(c) = log P(c) + Σ log P(t_k|c) ─► class with the highest score
```

#### 1. The multinomial model

The probability that document d is in class c is proportional to P(c)·Π_k P(t_k | c), over the document's tokens that are in the vocabulary. The best class is the maximum a posteriori class. Because many small probabilities are multiplied, implementations add logarithms instead, which avoids floating-point underflow and keeps the same ranking; each log P(t | c) is then a weight saying how good an indicator t is for c (Manning et al., 2008, ch. 13).

#### 2. Estimating the parameters

The prior P(c) is the share of training documents in class c; P(t | c) is the relative frequency of term t among all tokens of class c. The maximum likelihood estimate is zero for a term never seen in a class, which would rule the class out entirely, a problem of sparse data. Add-one (Laplace) smoothing adds one to every count: `P(t|c) = (T_ct + 1) / (Σ_t' T_ct' + B)` with B the vocabulary size (Manning et al., 2008, ch. 13).

#### 3. Two independence assumptions

Conditional independence assumes that terms are independent of each other given the class, although pairs such as hong and kong clearly are not. Positional independence assumes that a term's probability does not depend on its position, which amounts to the bag-of-words model. Together they reduce the parameters from a number exponential in the vocabulary size to one per term and class (Manning et al., 2008, ch. 13).

#### 4. Multinomial versus Bernoulli

The Bernoulli model represents a document by binary indicators of which vocabulary terms occur and also counts the absence of terms; the multinomial model counts occurrences and ignores absent terms. The Bernoulli model works best for short documents and few features and makes many mistakes on long ones; it may assign a whole book to China because of one occurrence of China. The multinomial model handles longer documents and more features (Manning et al., 2008, ch. 13).

#### 5. Why it works despite bad estimates

With many indicative terms, the winning class gets a probability near 1 and the others near 0, far from the true probabilities, but the decision depends only on which class scores highest. Correct estimation implies accurate prediction, but not the other way round: Naive Bayes estimates badly but often classifies well, and it is an optimal classifier for data where its independence assumptions hold (Manning et al., 2008, ch. 13).

#### 6. Feature selection

Feature selection keeps a subset of terms, which makes training and classification cheaper and often more accurate by removing noise features, terms that by accident occur only in one class in the training data and cause [[overfitting|overfitting]] (Manning et al., 2008, ch. 13):
- **Mutual information** measures how much the presence or absence of a term contributes to the correct class decision.
- **χ²** tests whether occurrence of the term and of the class are independent, ranking terms by the deviation of observed from expected counts.
- **Frequency-based** selection keeps the most common terms of a class; it often does well with many thousands of features but also selects uninformative terms such as weekdays.

#### Origin and variants

The multinomial model is equivalent to a multinomial unigram language model per class ([[query-likelihood-model|Language Models for Information Retrieval]]; Manning et al., 2008, ch. 13).

### When to use it

- When a few extra percentage points of accuracy are not worth the effort (Manning et al., 2008, ch. 13).
- When there is a very large amount of training data, where more data helps more than a better classifier on less data (Manning et al., 2008, ch. 13).
- When robustness to concept drift matters, the gradual change of what a class means over time (Manning et al., 2008, ch. 13).
- As a baseline for text classification research (Manning et al., 2008, ch. 13).

### Strengths and limitations

**Strengths**
- Training and classification in one pass over the data, optimal time complexity (Manning et al., 2008, ch. 13).
- Excels when many equally important features jointly decide the class (Manning et al., 2008, ch. 13).
- Somewhat robust to noise features and concept drift; the Bernoulli model performs decently with fewer than a dozen terms (Manning et al., 2008, ch. 13).

**Limitations**
- Its probability estimates are poor and should not be read as confidences (Manning et al., 2008, ch. 13; [[classification|Classification]]).
- Ignores word order: "He moved from London, Ontario, to London, England" and the reverse look alike (Manning et al., 2008, ch. 13).
- Usually not the most accurate method for text (Manning et al., 2008, ch. 13).

### Comparison

| Model | Document representation | Suited for |
|-------|------------------------|------------|
| Multinomial NB | Token counts (Manning et al., 2008, ch. 13) | Longer documents, many features |
| Bernoulli NB | Binary presence and absence of each term (Manning et al., 2008, ch. 13) | Short documents, few features |
| [[k-nearest-neighbours\|k-nearest neighbours]] | Similar training documents | Can be tuned closely to one period, which hurts under drift (Manning et al., 2008, ch. 13) |

### In practice

Scores are computed as sums of log probabilities (Manning et al., 2008, ch. 13). With χ² feature selection, peak effectiveness was reached at about 300 features in the book's experiment, with mutual information slightly earlier and at a similar level (Manning et al., 2008, ch. 13). In systems with many classifiers, a single shared feature set is often preferred over one per classifier (Manning et al., 2008, ch. 13).

### Key takeaway

Naive Bayes multiplies a class prior with smoothed per-class term probabilities; its estimates are poor but its decisions are fast and often good, which makes it a strong baseline for text classification.

### Sources

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Text classification and Naive Bayes.* Introduction to Information Retrieval, Chapter 13. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/13bayes.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Naive Bayes ordnet ein Dokument der Klasse c zu, die P(c)·Π P(t_k | c) maximiert: die A-priori-Wahrscheinlichkeit der Klasse mal der Wahrscheinlichkeit jedes seiner Terme in dieser Klasse, geschätzt aus Zählungen in annotierten Trainingsdokumenten mit Add-one-Glättung (Manning et al., 2008, Kap. 13). Seine Unabhängigkeitsannahmen sind für Sprache naiv, daher sind seine Wahrscheinlichkeitsschätzungen schlecht, seine Entscheidungen aber oft gut; es trainiert und klassifiziert in einem Durchlauf über die Daten, was es zu einer üblichen Baseline macht. Feature Selection mit Mutual Information oder χ² entfernt Rauschterme (Manning et al., 2008, Kap. 13). Den Überblick über Klassifikatoren gibt [[classification|Klassifikation]].

### Funktionsweise

```text
Trainingsdokumente mit Klassen ─► Zählungen pro Klasse: Dokumente (Prior), Termvorkommen
                               ─► P(c) = N_c / N,  P(t|c) = (T_ct + 1) / (Σ T_ct' + |V|)
neues Dokument t1 … tn ─► score(c) = log P(c) + Σ log P(t_k|c) ─► Klasse mit dem höchsten Wert
```

#### 1. Das multinomiale Modell

Die Wahrscheinlichkeit, dass Dokument d zur Klasse c gehört, ist proportional zu P(c)·Π_k P(t_k | c) über die Token des Dokuments, die im Vokabular sind. Die beste Klasse ist die Maximum-a-posteriori-Klasse. Weil viele kleine Wahrscheinlichkeiten multipliziert werden, addieren Implementierungen stattdessen Logarithmen, was Gleitkomma-Unterlauf vermeidet und dieselbe Rangfolge ergibt; jedes log P(t | c) ist dann ein Gewicht dafür, wie gut t die Klasse c anzeigt (Manning et al., 2008, Kap. 13).

#### 2. Die Parameter schätzen

Der Prior P(c) ist der Anteil der Trainingsdokumente in Klasse c; P(t | c) ist die relative Häufigkeit von Term t unter allen Token der Klasse c. Die Maximum-Likelihood-Schätzung ist null für einen Term, der in einer Klasse nie vorkam, was die Klasse ganz ausschlösse, ein Problem dünn besetzter Daten. Add-one-Glättung (Laplace) addiert zu jeder Zählung eins: `P(t|c) = (T_ct + 1) / (Σ_t' T_ct' + B)` mit B als Vokabulargröße (Manning et al., 2008, Kap. 13).

#### 3. Zwei Unabhängigkeitsannahmen

Bedingte Unabhängigkeit nimmt an, dass Terme gegeben die Klasse voneinander unabhängig sind, obwohl Paare wie hong und kong es offensichtlich nicht sind. Positionsunabhängigkeit nimmt an, dass die Wahrscheinlichkeit eines Terms nicht von seiner Position abhängt, was dem Bag-of-Words-Modell entspricht. Zusammen senken sie die Zahl der Parameter von einer im Vokabular exponentiellen Zahl auf einen pro Term und Klasse (Manning et al., 2008, Kap. 13).

#### 4. Multinomial gegenüber Bernoulli

Das Bernoulli-Modell stellt ein Dokument durch binäre Indikatoren dar, welche Vokabularterme vorkommen, und berücksichtigt auch das Fehlen von Termen; das multinomiale Modell zählt Vorkommen und ignoriert fehlende Terme. Das Bernoulli-Modell funktioniert am besten bei kurzen Dokumenten und wenigen Features und macht bei langen viele Fehler; es kann ein ganzes Buch wegen eines einzigen Vorkommens von China der Klasse China zuordnen. Das multinomiale Modell kommt mit längeren Dokumenten und mehr Features zurecht (Manning et al., 2008, Kap. 13).

#### 5. Warum es trotz schlechter Schätzungen funktioniert

Bei vielen aussagekräftigen Termen erhält die gewinnende Klasse eine Wahrscheinlichkeit nahe 1 und die übrigen nahe 0, weit entfernt von den wahren Wahrscheinlichkeiten, doch die Entscheidung hängt nur davon ab, welche Klasse den höchsten Wert hat. Korrekte Schätzung impliziert genaue Vorhersage, aber nicht umgekehrt: Naive Bayes schätzt schlecht, klassifiziert aber oft gut, und es ist ein optimaler Klassifikator für Daten, in denen seine Unabhängigkeitsannahmen gelten (Manning et al., 2008, Kap. 13).

#### 6. Feature Selection

Feature Selection behält eine Teilmenge der Terme, was Training und Klassifikation günstiger und durch das Entfernen von Rauschfeatures oft genauer macht, also von Termen, die im Training zufällig nur in einer Klasse vorkommen und [[overfitting|Overfitting]] verursachen (Manning et al., 2008, Kap. 13):
- **Mutual Information** misst, wie viel das Vorkommen oder Fehlen eines Terms zur richtigen Klassenentscheidung beiträgt.
- **χ²** prüft, ob das Vorkommen des Terms und der Klasse unabhängig sind, und rankt Terme nach der Abweichung beobachteter von erwarteten Zählungen.
- **Häufigkeitsbasierte** Auswahl behält die häufigsten Terme einer Klasse; sie funktioniert bei vielen Tausend Features oft gut, wählt aber auch nichtssagende Terme wie Wochentage.

#### Herkunft und Varianten

Das multinomiale Modell entspricht einem multinomialen Unigramm-Sprachmodell pro Klasse ([[query-likelihood-model|Sprachmodelle für Information Retrieval]]; Manning et al., 2008, Kap. 13).

### Wann einsetzen

- Wenn ein paar zusätzliche Prozentpunkte Genauigkeit den Aufwand nicht wert sind (Manning et al., 2008, Kap. 13).
- Wenn sehr viele Trainingsdaten vorliegen, sodass mehr Daten mehr bringen als ein besserer Klassifikator auf weniger Daten (Manning et al., 2008, Kap. 13).
- Wenn Robustheit gegenüber Concept Drift zählt, der allmählichen Änderung dessen, was eine Klasse bedeutet (Manning et al., 2008, Kap. 13).
- Als Baseline in der Forschung zur Textklassifikation (Manning et al., 2008, Kap. 13).

### Stärken und Grenzen

**Stärken**
- Training und Klassifikation in einem Durchlauf über die Daten, optimale Zeitkomplexität (Manning et al., 2008, Kap. 13).
- Glänzt, wenn viele gleich wichtige Features gemeinsam über die Klasse entscheiden (Manning et al., 2008, Kap. 13).
- Einigermaßen robust gegen Rauschfeatures und Concept Drift; das Bernoulli-Modell funktioniert schon mit weniger als einem Dutzend Termen ordentlich (Manning et al., 2008, Kap. 13).

**Grenzen**
- Seine Wahrscheinlichkeitsschätzungen sind schlecht und sollten nicht als Konfidenzen gelesen werden (Manning et al., 2008, Kap. 13; [[classification|Klassifikation]]).
- Ignoriert die Wortreihenfolge: „He moved from London, Ontario, to London, England“ und die Umkehrung sehen gleich aus (Manning et al., 2008, Kap. 13).
- Meist nicht das genaueste Verfahren für Text (Manning et al., 2008, Kap. 13).

### Vergleich

| Modell | Darstellung des Dokuments | Geeignet für |
|--------|---------------------------|--------------|
| Multinomiales NB | Tokenzählungen (Manning et al., 2008, Kap. 13) | Längere Dokumente, viele Features |
| Bernoulli-NB | Binäres Vorkommen und Fehlen jedes Terms (Manning et al., 2008, Kap. 13) | Kurze Dokumente, wenige Features |
| [[k-nearest-neighbours\|k-nächste Nachbarn]] | Ähnliche Trainingsdokumente | Lässt sich eng auf einen Zeitraum abstimmen, was bei Drift schadet (Manning et al., 2008, Kap. 13) |

### In der Praxis

Werte werden als Summen von Log-Wahrscheinlichkeiten berechnet (Manning et al., 2008, Kap. 13). Mit χ²-Feature-Selection wurde im Experiment des Buchs die höchste Effektivität bei etwa 300 Features erreicht, mit Mutual Information etwas früher und auf ähnlichem Niveau (Manning et al., 2008, Kap. 13). In Systemen mit vielen Klassifikatoren wird oft eine gemeinsame Feature-Menge statt einer pro Klassifikator bevorzugt (Manning et al., 2008, Kap. 13).

### Merksatz

Naive Bayes multipliziert eine Klassen-A-priori-Wahrscheinlichkeit mit geglätteten Termwahrscheinlichkeiten pro Klasse; seine Schätzungen sind schlecht, seine Entscheidungen aber schnell und oft gut, was es zu einer starken Baseline für Textklassifikation macht.

### Quellen

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Text classification and Naive Bayes.* Introduction to Information Retrieval, Chapter 13. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/13bayes.pdf)
