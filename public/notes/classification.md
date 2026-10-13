---
title_en: Classification
title_de: Klassifikation
entity_type: Concept
aliases:
- Logistic regression
- Probability calibration
sources:
- https://doi.org/10.1111/j.2517-6161.1958.tb00292.x
- https://doi.org/10.1111/j.1469-1809.1936.tb02137.x
- https://proceedings.neurips.cc/paper/2001/hash/7b7a53e239400a13bd6be6c91c4f6c4e-Abstract.html
- https://hastie.su.domains/ElemStatLearn/
- https://doi.org/10.1145/1102351.1102430
- https://nlp.stanford.edu/IR-book/pdf/13bayes.pdf
- https://nlp.stanford.edu/IR-book/pdf/14vcat.pdf
- https://nlp.stanford.edu/IR-book/pdf/15svm.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Classification predicts a discrete class from input features. Classical methods are logistic regression (Cox, 1958), [[naive-bayes|naive Bayes]] and discriminant analysis (Fisher, 1936; Hastie et al., 2009). Discriminative models such as logistic regression model the class probability directly, while generative models such as naive Bayes model how the features are distributed in each class (Ng & Jordan, 2001). Predicted probabilities are often distorted and need calibration (Niculescu-Mizil & Caruana, 2005). For text, the amount of labelled data decides between hand-written rules, simple high-bias learners and more complex classifiers (Manning et al., 2008, ch. 15).

### How it works

A model is fitted to labelled examples and returns, for a new example, a class or a probability for each class. The class is then chosen by a decision threshold, and the quality is measured with suitable metrics ([[classification-metrics|Classification Metrics]]).

```text
1. Logistic regression
▼
2. Naive Bayes
▼
3. Discriminant analysis (LDA and QDA)
▼
4. Calibrated probabilities
```

#### 1. Logistic regression

Cox (1958) considered a sequence of 0s and 1s in which the chance that a trial is a 1 depends on one or more independent variables, and developed tests and estimates for this situation; this is an early foundation of logistic regression for binary outcomes. Logistic regression models the class probability directly as a function of the inputs, which makes it a discriminative model (Hastie et al., 2009).

#### 2. Naive Bayes

Naive Bayes is a generative classifier: it models the distribution of the features within each class, assuming that the features are independent given the class, and derives the class probability from that (Hastie et al., 2009). Ng & Jordan (2001) compared it with logistic regression: the discriminative model has the lower asymptotic error, but naive Bayes approaches its own, higher asymptotic error much faster, so with few training examples naive Bayes can perform better.

#### 3. Discriminant analysis (LDA and QDA)

Fisher (1936) introduced the linear discriminant function, a linear combination of several measurements chosen to separate groups as well as possible, illustrated with measurements of iris flowers. Linear discriminant analysis (LDA) assumes that all classes share one covariance matrix, which gives linear decision boundaries; quadratic discriminant analysis (QDA) allows a separate covariance matrix per class, which gives quadratic boundaries but requires more parameters (Hastie et al., 2009).

#### 4. Calibrated probabilities

Predicted probabilities do not always match true probabilities. Niculescu-Mizil & Caruana (2005) showed that boosted trees and stumps push predicted probabilities away from 0 and 1, naive Bayes pushes them toward 0 and 1, and neural nets and bagged trees are well calibrated. Platt scaling and isotonic regression correct these distortions; after calibration, boosted trees, random forests and SVMs predicted the best probabilities.

#### 5. Text classification: rules or learning

In [[information-retrieval|information retrieval]], classification sorts documents into classes such as topics, spam or sentiment, routes them for standing queries and supports vertical search; most retrieval systems contain several classifiers (Manning et al., 2008, ch. 13). There are three approaches: manual classification, which is expensive to scale; hand-written rules, which a skilled domain expert can make as accurate as learned classifiers but which are laborious to create and maintain; and machine learning, which learns the decision criterion from labelled training documents. Labelling is easier than writing rules, since almost anyone can decide whether a document is about China (Manning et al., 2008, ch. 13). Which approach fits depends first on how much labelled data exists: without any, hand-written rules, tuned on development data, can become very accurate, at roughly two days of work per class plus maintenance as content drifts; with little data, a high-bias classifier such as [[naive-bayes|Naive Bayes]], semi-supervised training or active learning, which can cut annotation costs by a factor of 2–4; with a reasonable amount, methods such as [[support-vector-machines|SVMs]], ideally with an overlay of hand-written rules for quick corrections; with huge amounts, the choice of classifier probably matters little. Domain-specific text features often bring larger gains than switching between learning methods (Manning et al., 2008, ch. 15).

#### 6. Vector space classification: Rocchio and kNN

Vector space classifiers represent documents as length-normalised tf-idf vectors and rely on the contiguity hypothesis: documents of one class form a contiguous region that does not overlap with other classes. Whether it holds depends on the representation; a stop list, for example, removes the pronoun *I*, which distinguishes single authors from groups. Rocchio classification assigns a document to the class with the nearest centroid; it is simple and efficient but inaccurate if classes are not roughly spheres of similar radius. k nearest neighbour ([[k-nearest-neighbors|kNN]]) assigns the majority class of the k nearest training documents; it needs no explicit training, is slower at test time and handles non-spherical classes better when the training set is large (Manning et al., 2008, ch. 14).

#### 7. Linear versus nonlinear classifiers and the bias-variance tradeoff

A linear classifier compares a linear combination of the features with a threshold; Naive Bayes and Rocchio are linear, kNN is nonlinear. Bias measures how consistently a learning method is wrong, variance how much the learned classifier changes with the training set. Linear methods have low variance, while kNN has high variance, is sensitive to noise documents and is prone to overfitting. The tradeoff explains why no learning method is universally optimal; nonlinear models are not systematically better than linear ones, because they have more parameters to fit on limited, noisy data (Manning et al., 2008, ch. 14).

#### 8. More than two classes

In any-of (multilabel) classification a document can belong to several classes, and one two-class classifier is trained per class. In one-of (multiclass) classification the classes are mutually exclusive, and two-class classifiers are combined, for example by ranking the classes and choosing the top one. True one-of problems are less common in text classification, since a document can be about the UK, China and coffee at once, but a one-of assumption works well for language identification (Manning et al., 2008, ch. 14).

#### Origin and variants

Fisher (1936) introduced the linear discriminant and Cox (1958) the regression analysis of binary outcomes. Ng & Jordan (2001) compared generative and discriminative classifiers, and Niculescu-Mizil & Caruana (2005) studied the calibration of predicted probabilities. Tree ensembles, support vector machines and [[neural-networks|neural networks]] are further classifiers ([[ensemble-methods|Ensemble Methods]], [[support-vector-machines|Support Vector Machines]]).

### When to use it

- When an interpretable model of how inputs affect a binary outcome is needed, logistic regression fits (Cox, 1958; Hastie et al., 2009).
- When only few training examples are available, naive Bayes can outperform logistic regression (Ng & Jordan, 2001).
- When decisions depend on probabilities, for example on risk thresholds, the probabilities should be calibrated (Niculescu-Mizil & Caruana, 2005).
- When no labelled data exist but domain experts do, hand-written rules can be very accurate (Manning et al., 2008, ch. 15).
- When classes are not spherical and the training set is large, kNN; when classes are roughly spherical, Rocchio is simple and efficient (Manning et al., 2008, ch. 14).

### Strengths and limitations

**Strengths**
- Logistic regression and LDA are simple and interpretable (Hastie et al., 2009).
- Naive Bayes learns quickly from few examples (Ng & Jordan, 2001).
- Calibration methods can turn distorted scores into usable probabilities (Niculescu-Mizil & Caruana, 2005).
- Linear classifiers have low variance and are hard to beat on limited, noisy data (Manning et al., 2008, ch. 14).

**Limitations**
- Naive Bayes rests on an unrealistic independence assumption and pushes probabilities toward 0 and 1 (Niculescu-Mizil & Caruana, 2005).
- With more data, generative models end up with a higher asymptotic error than discriminative ones (Ng & Jordan, 2001).
- QDA needs a covariance matrix per class and therefore more data (Hastie et al., 2009).
- Obtaining enough labelled data is often the biggest practical challenge; many problems need hundreds or thousands of examples per class (Manning et al., 2008, ch. 15).
- kNN has high variance and is slow at test time, since it compares each document with the training set (Manning et al., 2008, ch. 14).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Logistic regression | Discriminative; models the class probability directly (Cox, 1958; Hastie et al., 2009) | Interpretable models, larger datasets |
| Naive Bayes | Generative; features independent given the class (Ng & Jordan, 2001) | Few training examples, many features |
| LDA | Generative; shared covariance, linear boundaries (Fisher, 1936; Hastie et al., 2009) | Classes with similar spread |
| QDA | Generative; class-specific covariance, quadratic boundaries (Hastie et al., 2009) | Classes with different spread and enough data |
| Rocchio | Nearest class centroid; linear (Manning et al., 2008, ch. 14) | Roughly spherical classes, speed |
| kNN | Majority of the k nearest neighbours; nonlinear (Manning et al., 2008, ch. 14) | Complex class shapes, large training sets |
| Hand-written rules | Boolean conditions written by experts (Manning et al., 2008, ch. 15) | No labelled data, quick manual corrections |

### In practice

Classifiers are compared with [[cross-validation|cross-validation]] on appropriate metrics ([[classification-metrics|Classification Metrics]], [[ml-preprocessing|ML Preprocessing]]). If predicted probabilities are used for decisions, their calibration is checked and, if needed, corrected with Platt scaling or isotonic regression on held-out data (Niculescu-Mizil & Caruana, 2005).

### Key takeaway

Classification predicts classes either by modelling the class probability directly or by modelling the features per class, and the predicted probabilities usually need to be checked for calibration.

### Sources

- Cox, D. R. (1958). *The Regression Analysis of Binary Sequences.* Journal of the Royal Statistical Society, Series B 20(2). [doi:10.1111/j.2517-6161.1958.tb00292.x](https://doi.org/10.1111/j.2517-6161.1958.tb00292.x)
- Fisher, R. A. (1936). *The Use of Multiple Measurements in Taxonomic Problems.* Annals of Eugenics 7(2). [doi:10.1111/j.1469-1809.1936.tb02137.x](https://doi.org/10.1111/j.1469-1809.1936.tb02137.x)
- Ng, A. Y. & Jordan, M. I. (2001). *On Discriminative vs. Generative Classifiers: A comparison of logistic regression and naive Bayes.* NIPS 14. [NeurIPS proceedings](https://proceedings.neurips.cc/paper/2001/hash/7b7a53e239400a13bd6be6c91c4f6c4e-Abstract.html)
- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [book website](https://hastie.su.domains/ElemStatLearn/)
- Niculescu-Mizil, A. & Caruana, R. (2005). *Predicting good probabilities with supervised learning.* ICML 2005. [doi:10.1145/1102351.1102430](https://doi.org/10.1145/1102351.1102430)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Text classification and Naive Bayes.* Introduction to Information Retrieval, Chapter 13. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/13bayes.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Vector space classification.* Introduction to Information Retrieval, Chapter 14. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/14vcat.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Support vector machines and machine learning on documents.* Introduction to Information Retrieval, Chapter 15. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/15svm.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Klassifikation sagt aus Eingabemerkmalen eine diskrete Klasse vorher. Klassische Verfahren sind die logistische Regression (Cox, 1958), [[naive-bayes|Naive Bayes]] und die Diskriminanzanalyse (Fisher, 1936; Hastie et al., 2009). Diskriminative Modelle wie die logistische Regression modellieren die Klassenwahrscheinlichkeit direkt, generative Modelle wie Naive Bayes modellieren, wie die Merkmale in jeder Klasse verteilt sind (Ng & Jordan, 2001). Vorhergesagte Wahrscheinlichkeiten sind oft verzerrt und müssen kalibriert werden (Niculescu-Mizil & Caruana, 2005). Bei Text entscheidet die Menge gelabelter Daten zwischen handgeschriebenen Regeln, einfachen Lernverfahren mit hohem Bias und komplexeren Klassifikatoren (Manning et al., 2008, Kap. 15).

### Funktionsweise

Ein Modell wird an gelabelten Beispielen angepasst und liefert für ein neues Beispiel eine Klasse oder eine Wahrscheinlichkeit je Klasse. Die Klasse ergibt sich dann über einen Entscheidungsschwellenwert, und die Qualität wird mit geeigneten Metriken gemessen ([[classification-metrics|Klassifikationsmetriken]]).

```text
1. Logistische Regression
▼
2. Naive Bayes
▼
3. Diskriminanzanalyse (LDA und QDA)
▼
4. Kalibrierte Wahrscheinlichkeiten
```

#### 1. Logistische Regression

Cox (1958) betrachtete eine Folge von Nullen und Einsen, bei der die Wahrscheinlichkeit einer Eins von einer oder mehreren unabhängigen Variablen abhängt, und entwickelte Tests und Schätzer für diese Situation; das ist eine frühe Grundlage der logistischen Regression für binäre Zielgrößen. Die logistische Regression modelliert die Klassenwahrscheinlichkeit direkt als Funktion der Eingaben und ist damit ein diskriminatives Modell (Hastie et al., 2009).

#### 2. Naive Bayes

Naive Bayes ist ein generativer Klassifikator: Er modelliert die Verteilung der Merkmale innerhalb jeder Klasse unter der Annahme, dass die Merkmale bei gegebener Klasse unabhängig sind, und leitet daraus die Klassenwahrscheinlichkeit ab (Hastie et al., 2009). Ng & Jordan (2001) verglichen ihn mit der logistischen Regression: Das diskriminative Modell hat den geringeren asymptotischen Fehler, Naive Bayes erreicht seinen eigenen, höheren asymptotischen Fehler aber viel schneller und kann daher bei wenigen Trainingsbeispielen besser abschneiden.

#### 3. Diskriminanzanalyse (LDA und QDA)

Fisher (1936) führte die lineare Diskriminanzfunktion ein, eine Linearkombination mehrerer Messungen, die Gruppen möglichst gut trennt, veranschaulicht an Messungen von Schwertlilien. Die lineare Diskriminanzanalyse (LDA) nimmt eine gemeinsame Kovarianzmatrix für alle Klassen an und liefert lineare Entscheidungsgrenzen; die quadratische Diskriminanzanalyse (QDA) erlaubt je Klasse eine eigene Kovarianzmatrix, was quadratische Grenzen ergibt, aber mehr Parameter erfordert (Hastie et al., 2009).

#### 4. Kalibrierte Wahrscheinlichkeiten

Vorhergesagte Wahrscheinlichkeiten stimmen nicht immer mit den tatsächlichen überein. Niculescu-Mizil & Caruana (2005) zeigten, dass Boosted Trees und Stumps die Wahrscheinlichkeiten von 0 und 1 wegdrängen, Naive Bayes sie zu 0 und 1 hindrängt und [[neural-networks|neuronale Netze]] sowie Bagged Trees gut kalibriert sind. Platt Scaling und isotone Regression korrigieren diese Verzerrungen; nach der Kalibrierung lieferten Boosted Trees, Random Forests und SVMs die besten Wahrscheinlichkeiten.

#### 5. Textklassifikation: Regeln oder Lernen

Im [[information-retrieval|Information Retrieval]] ordnet Klassifikation Dokumente Klassen wie Themen, Spam oder Stimmung zu, leitet sie für dauerhafte Suchanfragen (Standing Queries) weiter und unterstützt vertikale Suche; die meisten Retrieval-Systeme enthalten mehrere Klassifikatoren (Manning et al., 2008, Kap. 13). Es gibt drei Ansätze: manuelle Klassifikation, die sich schlecht skalieren lässt; handgeschriebene Regeln, die eine geübte Fachperson so genau machen kann wie gelernte Klassifikatoren, deren Erstellung und Pflege aber aufwendig ist; und maschinelles Lernen, das das Entscheidungskriterium aus gelabelten Trainingsdokumenten lernt. Labeln ist leichter als Regeln zu schreiben, da fast jede Person entscheiden kann, ob ein Dokument von China handelt (Manning et al., 2008, Kap. 13). Welcher Ansatz passt, hängt zuerst davon ab, wie viele gelabelte Daten es gibt: ohne Daten können handgeschriebene Regeln, auf Entwicklungsdaten abgestimmt, sehr genau werden, bei grob zwei Tagen Arbeit pro Klasse plus Pflege, wenn sich die Inhalte verschieben; mit wenigen Daten ein Klassifikator mit hohem Bias wie [[naive-bayes|Naive Bayes]], halbüberwachtes Training oder Active Learning, das den Annotationsaufwand um den Faktor 2–4 senken kann; mit einer vernünftigen Menge Verfahren wie [[support-vector-machines|SVMs]], idealerweise überlagert von handgeschriebenen Regeln für schnelle Korrekturen; mit sehr großen Mengen spielt die Wahl des Klassifikators vermutlich kaum eine Rolle. Domänenspezifische Textmerkmale bringen oft mehr als der Wechsel zwischen Lernverfahren (Manning et al., 2008, Kap. 15).

#### 6. Klassifikation im Vektorraum: Rocchio und kNN

Vektorraum-Klassifikatoren stellen Dokumente als längennormierte tf-idf-Vektoren dar und beruhen auf der Kontiguitätshypothese: Dokumente einer Klasse bilden einen zusammenhängenden Bereich, der sich nicht mit anderen Klassen überschneidet. Ob sie gilt, hängt von der Repräsentation ab; eine Stoppwortliste entfernt etwa das Pronomen *I*, das Einzelautorinnen und -autoren von Gruppen unterscheidet. Die Rocchio-Klassifikation ordnet ein Dokument der Klasse mit dem nächsten Zentroid zu; sie ist einfach und effizient, aber ungenau, wenn Klassen nicht annähernd Kugeln mit ähnlichem Radius sind. k-Nächste-Nachbarn ([[k-nearest-neighbors|kNN]]) wählt die Mehrheitsklasse der k nächsten Trainingsdokumente; es braucht kein explizites Training, ist beim Klassifizieren langsamer und kommt mit nicht kugelförmigen Klassen besser zurecht, wenn die Trainingsmenge groß ist (Manning et al., 2008, Kap. 14).

#### 7. Lineare und nichtlineare Klassifikatoren und der Bias-Varianz-Zielkonflikt

Ein linearer Klassifikator vergleicht eine Linearkombination der Merkmale mit einem Schwellenwert; Naive Bayes und Rocchio sind linear, kNN ist nichtlinear. Bias misst, wie beständig ein Lernverfahren danebenliegt, Varianz, wie stark sich der gelernte Klassifikator mit der Trainingsmenge ändert. Lineare Verfahren haben geringe Varianz, kNN dagegen hohe Varianz, reagiert empfindlich auf verrauschte Dokumente und neigt zur Überanpassung. Der Zielkonflikt erklärt, warum kein Lernverfahren allgemein optimal ist; nichtlineare Modelle sind nicht systematisch besser als lineare, weil sie mehr Parameter auf begrenzten, verrauschten Daten anpassen müssen (Manning et al., 2008, Kap. 14).

#### 8. Mehr als zwei Klassen

Bei Any-of-Klassifikation (Multilabel) kann ein Dokument zu mehreren Klassen gehören, und pro Klasse wird ein Zwei-Klassen-Klassifikator trainiert. Bei One-of-Klassifikation (Multiclass) schließen sich die Klassen gegenseitig aus, und Zwei-Klassen-Klassifikatoren werden kombiniert, etwa indem die Klassen gerankt und die oberste gewählt wird. Echte One-of-Probleme sind in der Textklassifikation seltener, da ein Dokument zugleich von Großbritannien, China und Kaffee handeln kann, doch für die Spracherkennung funktioniert die One-of-Annahme gut (Manning et al., 2008, Kap. 14).

#### Ursprung und Varianten

Fisher (1936) führte die lineare Diskriminanzfunktion ein, Cox (1958) die Regressionsanalyse binärer Zielgrößen. Ng & Jordan (2001) verglichen generative und diskriminative Klassifikatoren, Niculescu-Mizil & Caruana (2005) untersuchten die Kalibrierung vorhergesagter Wahrscheinlichkeiten. Baum-Ensembles, Support Vector Machines und neuronale Netze sind weitere Klassifikatoren ([[ensemble-methods|Ensemble-Methoden]], [[support-vector-machines|Support Vector Machines]]).

### Wann einsetzen

- Wenn ein interpretierbares Modell dafür gebraucht wird, wie Eingaben eine binäre Zielgröße beeinflussen, passt die logistische Regression (Cox, 1958; Hastie et al., 2009).
- Wenn nur wenige Trainingsbeispiele vorliegen, kann Naive Bayes die logistische Regression übertreffen (Ng & Jordan, 2001).
- Wenn Entscheidungen von Wahrscheinlichkeiten abhängen, etwa von Risikoschwellen, sollten diese kalibriert sein (Niculescu-Mizil & Caruana, 2005).
- Wenn keine gelabelten Daten, aber Fachleute vorhanden sind, können handgeschriebene Regeln sehr genau sein (Manning et al., 2008, Kap. 15).
- Wenn Klassen nicht kugelförmig sind und die Trainingsmenge groß ist, kNN; bei annähernd kugelförmigen Klassen ist Rocchio einfach und effizient (Manning et al., 2008, Kap. 14).

### Stärken und Grenzen

**Stärken**
- Logistische Regression und LDA sind einfach und interpretierbar (Hastie et al., 2009).
- Naive Bayes lernt schnell aus wenigen Beispielen (Ng & Jordan, 2001).
- Kalibrierungsverfahren machen aus verzerrten Werten brauchbare Wahrscheinlichkeiten (Niculescu-Mizil & Caruana, 2005).
- Lineare Klassifikatoren haben geringe Varianz und sind auf begrenzten, verrauschten Daten schwer zu schlagen (Manning et al., 2008, Kap. 14).

**Einschränkungen**
- Naive Bayes beruht auf einer unrealistischen Unabhängigkeitsannahme und drängt Wahrscheinlichkeiten zu 0 und 1 (Niculescu-Mizil & Caruana, 2005).
- Mit mehr Daten erreichen generative Modelle einen höheren asymptotischen Fehler als diskriminative (Ng & Jordan, 2001).
- QDA braucht eine Kovarianzmatrix je Klasse und damit mehr Daten (Hastie et al., 2009).
- Genug gelabelte Daten zu bekommen ist oft die größte praktische Hürde; viele Probleme brauchen Hunderte oder Tausende Beispiele pro Klasse (Manning et al., 2008, Kap. 15).
- kNN hat hohe Varianz und ist beim Klassifizieren langsam, da es jedes Dokument mit der Trainingsmenge vergleicht (Manning et al., 2008, Kap. 14).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Logistische Regression | Diskriminativ; modelliert die Klassenwahrscheinlichkeit direkt (Cox, 1958; Hastie et al., 2009) | Interpretierbare Modelle, größere Datensätze |
| Naive Bayes | Generativ; Merkmale bei gegebener Klasse unabhängig (Ng & Jordan, 2001) | Wenige Trainingsbeispiele, viele Merkmale |
| LDA | Generativ; gemeinsame Kovarianz, lineare Grenzen (Fisher, 1936; Hastie et al., 2009) | Klassen mit ähnlicher Streuung |
| QDA | Generativ; klassenspezifische Kovarianz, quadratische Grenzen (Hastie et al., 2009) | Klassen mit unterschiedlicher Streuung und genug Daten |
| Rocchio | Nächstes Klassenzentroid; linear (Manning et al., 2008, Kap. 14) | Annähernd kugelförmige Klassen, Geschwindigkeit |
| kNN | Mehrheit der k nächsten Nachbarn; nichtlinear (Manning et al., 2008, Kap. 14) | Komplexe Klassenformen, große Trainingsmengen |
| Handgeschriebene Regeln | Boolesche Bedingungen von Fachleuten (Manning et al., 2008, Kap. 15) | Keine gelabelten Daten, schnelle manuelle Korrekturen |

### In der Praxis

Klassifikatoren werden per [[cross-validation|Kreuzvalidierung]] mit geeigneten Metriken verglichen ([[classification-metrics|Klassifikationsmetriken]], [[ml-preprocessing|Preprocessing für Machine Learning]]). Werden vorhergesagte Wahrscheinlichkeiten für Entscheidungen genutzt, wird ihre Kalibrierung geprüft und bei Bedarf mit Platt Scaling oder isotoner Regression auf zurückgehaltenen Daten korrigiert (Niculescu-Mizil & Caruana, 2005).

### Merksatz

Klassifikation sagt Klassen voraus, indem sie entweder die Klassenwahrscheinlichkeit direkt oder die Merkmale je Klasse modelliert, und die vorhergesagten Wahrscheinlichkeiten müssen meist auf ihre Kalibrierung geprüft werden.

### Quellen

- Cox, D. R. (1958). *The Regression Analysis of Binary Sequences.* Journal of the Royal Statistical Society, Series B 20(2). [doi:10.1111/j.2517-6161.1958.tb00292.x](https://doi.org/10.1111/j.2517-6161.1958.tb00292.x)
- Fisher, R. A. (1936). *The Use of Multiple Measurements in Taxonomic Problems.* Annals of Eugenics 7(2). [doi:10.1111/j.1469-1809.1936.tb02137.x](https://doi.org/10.1111/j.1469-1809.1936.tb02137.x)
- Ng, A. Y. & Jordan, M. I. (2001). *On Discriminative vs. Generative Classifiers: A comparison of logistic regression and naive Bayes.* NIPS 14. [NeurIPS proceedings](https://proceedings.neurips.cc/paper/2001/hash/7b7a53e239400a13bd6be6c91c4f6c4e-Abstract.html)
- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [book website](https://hastie.su.domains/ElemStatLearn/)
- Niculescu-Mizil, A. & Caruana, R. (2005). *Predicting good probabilities with supervised learning.* ICML 2005. [doi:10.1145/1102351.1102430](https://doi.org/10.1145/1102351.1102430)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Text classification and Naive Bayes.* Introduction to Information Retrieval, Chapter 13. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/13bayes.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Vector space classification.* Introduction to Information Retrieval, Chapter 14. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/14vcat.pdf)
- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Support vector machines and machine learning on documents.* Introduction to Information Retrieval, Chapter 15. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/15svm.pdf)
