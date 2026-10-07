---
title_en: Classification Metrics
title_de: Klassifikationsmetriken
entity_type: Concept
sources:
- https://doi.org/10.1016/j.ipm.2009.03.002
- https://doi.org/10.1016/j.patrec.2005.10.010
- https://doi.org/10.1145/1143844.1143874
- https://doi.org/10.1371/journal.pone.0118432
- https://doi.org/10.1186/s12864-019-6413-7
- https://arxiv.org/abs/1606.05250
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Classification metrics measure how well a classifier's predictions match the true labels. Most are computed from the confusion matrix of true and false positives and negatives: accuracy, precision, recall (sensitivity), specificity and the F1 score (Sokolova & Lapalme, 2009). Threshold-free views such as ROC and precision-recall curves summarise performance over all decision thresholds (Fawcett, 2006; Davis & Goadrich, 2006). On imbalanced data, accuracy and even F1 can be misleading, and precision-recall curves or the Matthews correlation coefficient are more informative (Saito & Rehmsmeier, 2015; Chicco & Jurman, 2020).

### How it works

Predictions are compared with true labels and counted in a confusion matrix. Metrics combine these counts in different ways, so each emphasises a different kind of error; the metric is chosen according to which errors matter most in the application.

```text
1. Confusion matrix
▼
2. Precision, recall, specificity and accuracy
▼
3. F1 score and the Matthews correlation coefficient
▼
4. ROC curves and AUC
▼
5. Precision-recall curves for imbalanced data
▼
6. Exact match for extracted answers
```

#### 1. Confusion matrix

For a binary classifier, each prediction is a true positive (TP), false positive (FP), true negative (TN) or false negative (FN). These four counts form the confusion matrix, from which most classification metrics are computed; the same idea extends to multi-class, multi-labelled and hierarchical classification (Sokolova & Lapalme, 2009).

#### 2. Precision, recall, specificity and accuracy

Precision, TP / (TP + FP), is the share of positive predictions that are correct. Recall or sensitivity, TP / (TP + FN), is the share of actual positives that are found. Specificity, TN / (TN + FP), is the share of actual negatives that are correctly rejected, and accuracy, (TP + TN) divided by all predictions, is the share of correct predictions overall. Sokolova & Lapalme (2009) show that measures differ in which changes of the confusion matrix they are invariant to: precision, recall and F-score, for example, do not change when only the number of true negatives changes, which matters when negatives are abundant.

#### 3. F1 score and the Matthews correlation coefficient

The F1 score is the harmonic mean of precision and recall and is high only if both are high (Sokolova & Lapalme, 2009). Accuracy and F1 can nevertheless show overoptimistic, inflated results on imbalanced datasets. The Matthews correlation coefficient (MCC) produces a high score only if the prediction is good in all four confusion-matrix categories, proportionally to the sizes of the positive and negative classes (Chicco & Jurman, 2020).

#### 4. ROC curves and AUC

A receiver operating characteristic (ROC) curve plots the true positive rate against the false positive rate as the decision threshold of a scoring classifier varies (Fawcett, 2006). The area under the curve (AUC) equals the probability that the classifier ranks a randomly chosen positive instance higher than a randomly chosen negative one. ROC curves are insensitive to changes in the class distribution.

#### 5. Precision-recall curves for imbalanced data

When negatives far outnumber positives, ROC plots can look reassuring while most positive predictions are wrong, because the false positive rate stays small even with many false positives. Precision-recall (PR) curves show the fraction of true positives among positive predictions and give a more accurate picture in such settings (Saito & Rehmsmeier, 2015). A curve dominates in ROC space if and only if it dominates in PR space, but linear interpolation between points is wrong in PR space, and optimising the area under the ROC curve does not guarantee a good area under the PR curve (Davis & Goadrich, 2006).

#### 6. Exact match for extracted answers

For extractive question answering, where the answer is a span of text, predictions are scored with exact match, i.e. whether the predicted span equals a reference answer, and with a token-level F1 score that gives partial credit for overlap. On SQuAD, a logistic regression baseline reached an F1 of 51.0%, compared with 86.8% for humans (Rajpurkar et al., 2016; [[text-similarity-metrics|Text Similarity Metrics]]).

#### Origin and variants

Sokolova & Lapalme (2009) systematised confusion-matrix measures, Fawcett (2006) introduced ROC analysis to a broad audience, Davis & Goadrich (2006) and Saito & Rehmsmeier (2015) clarified the role of precision-recall curves, and Chicco & Jurman (2020) argued for MCC. Rajpurkar et al. (2016) popularised exact match and F1 for extractive question answering.

### When to use it

- When false positives are costly, for example when wrongly flagging a document, precision matters most (Sokolova & Lapalme, 2009).
- When missing positives is costly, for example in screening, recall matters most (Sokolova & Lapalme, 2009).
- When classes are strongly imbalanced, precision-recall curves and MCC are more informative than accuracy or ROC (Saito & Rehmsmeier, 2015; Chicco & Jurman, 2020).

### Strengths and limitations

**Strengths**
- Confusion-matrix metrics are simple and make the kind of error explicit (Sokolova & Lapalme, 2009).
- ROC curves and AUC summarise performance over all thresholds (Fawcett, 2006).
- MCC accounts for all four confusion-matrix categories (Chicco & Jurman, 2020).

**Limitations**
- Accuracy and F1 can be inflated on imbalanced data (Chicco & Jurman, 2020).
- ROC plots can be visually deceptive on strongly imbalanced data (Saito & Rehmsmeier, 2015).
- A good ROC AUC does not imply a good PR AUC (Davis & Goadrich, 2006).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Accuracy | Share of all correct predictions (Sokolova & Lapalme, 2009) | Balanced classes, equal error costs |
| Precision / recall / F1 | Focus on the positive class; ignore true negatives (Sokolova & Lapalme, 2009) | Retrieval and extraction tasks |
| MCC | Balanced use of all four confusion-matrix cells (Chicco & Jurman, 2020) | Imbalanced binary classification |
| ROC AUC | Ranking quality over all thresholds, insensitive to class distribution (Fawcett, 2006) | Comparing scoring classifiers |
| PR AUC | Precision over recall levels (Davis & Goadrich, 2006; Saito & Rehmsmeier, 2015) | Rare positive class |

### In practice

The metric is chosen before evaluation, based on the costs of the different errors, and reported together with the confusion matrix (Sokolova & Lapalme, 2009). Metrics are computed per group when fairness matters, since equal overall accuracy can hide unequal error rates ([[fairness-metrics|Fairness Metrics]]). Differences between models are tested for significance rather than read from single numbers ([[model-comparison|Model Comparison]]).

### Key takeaway

Classification metrics weigh different errors differently; on imbalanced data, precision-recall curves and MCC say more than accuracy.

### Sources

- Sokolova, M. & Lapalme, G. (2009). *A systematic analysis of performance measures for classification tasks.* Information Processing & Management 45(4). [doi:10.1016/j.ipm.2009.03.002](https://doi.org/10.1016/j.ipm.2009.03.002)
- Fawcett, T. (2006). *An introduction to ROC analysis.* Pattern Recognition Letters 27(8). [doi:10.1016/j.patrec.2005.10.010](https://doi.org/10.1016/j.patrec.2005.10.010)
- Davis, J. & Goadrich, M. (2006). *The relationship between Precision-Recall and ROC curves.* ICML 2006. [doi:10.1145/1143844.1143874](https://doi.org/10.1145/1143844.1143874)
- Saito, T. & Rehmsmeier, M. (2015). *The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets.* PLoS ONE 10(3). [doi:10.1371/journal.pone.0118432](https://doi.org/10.1371/journal.pone.0118432)
- Chicco, D. & Jurman, G. (2020). *The advantages of the Matthews correlation coefficient (MCC) over F1 score and accuracy in binary classification evaluation.* BMC Genomics 21. [doi:10.1186/s12864-019-6413-7](https://doi.org/10.1186/s12864-019-6413-7)
- Rajpurkar, P. et al. (2016). *SQuAD: 100,000+ Questions for Machine Comprehension of Text.* EMNLP 2016. [arXiv:1606.05250](https://arxiv.org/abs/1606.05250)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Klassifikationsmetriken messen, wie gut die Vorhersagen eines Klassifikators mit den tatsächlichen Labels übereinstimmen. Die meisten werden aus der Konfusionsmatrix der richtig und falsch positiven und negativen Entscheidungen berechnet: Accuracy, Precision, Recall (Sensitivität), Spezifität und F1-Score (Sokolova & Lapalme, 2009). Schwellenwertfreie Darstellungen wie ROC- und Precision-Recall-Kurven fassen die Leistung über alle Entscheidungsschwellen zusammen (Fawcett, 2006; Davis & Goadrich, 2006). Bei unausgewogenen Daten können Accuracy und selbst F1 irreführen; Precision-Recall-Kurven oder der Matthews-Korrelationskoeffizient sind dann aussagekräftiger (Saito & Rehmsmeier, 2015; Chicco & Jurman, 2020).

### Funktionsweise

Vorhersagen werden mit den tatsächlichen Labels verglichen und in einer Konfusionsmatrix gezählt. Die Metriken kombinieren diese Zählwerte unterschiedlich und betonen so jeweils andere Fehlerarten; gewählt wird die Metrik danach, welche Fehler in der Anwendung am meisten zählen.

```text
1. Konfusionsmatrix
▼
2. Precision, Recall, Spezifität und Accuracy
▼
3. F1-Score und Matthews-Korrelationskoeffizient
▼
4. ROC-Kurven und AUC
▼
5. Precision-Recall-Kurven bei unausgewogenen Daten
▼
6. Exact Match für extrahierte Antworten
```

#### 1. Konfusionsmatrix

Bei einem binären Klassifikator ist jede Vorhersage richtig positiv (TP), falsch positiv (FP), richtig negativ (TN) oder falsch negativ (FN). Diese vier Zählwerte bilden die Konfusionsmatrix, aus der die meisten Klassifikationsmetriken berechnet werden; dieselbe Idee lässt sich auf Mehrklassen-, Multi-Label- und hierarchische Klassifikation übertragen (Sokolova & Lapalme, 2009).

#### 2. Precision, Recall, Spezifität und Accuracy

Precision, TP / (TP + FP), ist der Anteil korrekter unter den positiven Vorhersagen. Recall oder Sensitivität, TP / (TP + FN), ist der Anteil gefundener unter den tatsächlich positiven Fällen. Spezifität, TN / (TN + FP), ist der Anteil korrekt abgelehnter unter den tatsächlich negativen Fällen, und Accuracy, (TP + TN) geteilt durch alle Vorhersagen, ist der Anteil korrekter Vorhersagen insgesamt. Sokolova & Lapalme (2009) zeigen, dass sich die Maße darin unterscheiden, gegenüber welchen Änderungen der Konfusionsmatrix sie invariant sind: Precision, Recall und F-Score ändern sich zum Beispiel nicht, wenn sich nur die Zahl der richtig negativen Fälle ändert, was bei sehr vielen Negativfällen wichtig ist.

#### 3. F1-Score und Matthews-Korrelationskoeffizient

Der F1-Score ist das harmonische Mittel aus Precision und Recall und nur dann hoch, wenn beide hoch sind (Sokolova & Lapalme, 2009). Accuracy und F1 können auf unausgewogenen Datensätzen dennoch überoptimistische, aufgeblähte Ergebnisse zeigen. Der Matthews-Korrelationskoeffizient (MCC) ergibt nur dann einen hohen Wert, wenn die Vorhersage in allen vier Feldern der Konfusionsmatrix gut ist, im Verhältnis zur Größe der positiven und der negativen Klasse (Chicco & Jurman, 2020).

#### 4. ROC-Kurven und AUC

Eine ROC-Kurve (Receiver Operating Characteristic) trägt die Richtig-positiv-Rate gegen die Falsch-positiv-Rate auf, während die Entscheidungsschwelle eines bewertenden Klassifikators variiert (Fawcett, 2006). Die Fläche unter der Kurve (AUC) entspricht der Wahrscheinlichkeit, dass der Klassifikator einen zufällig gewählten positiven Fall höher einstuft als einen zufällig gewählten negativen. ROC-Kurven sind unempfindlich gegenüber Änderungen der Klassenverteilung.

#### 5. Precision-Recall-Kurven bei unausgewogenen Daten

Wenn negative Fälle weit überwiegen, können ROC-Kurven beruhigend aussehen, obwohl die meisten positiven Vorhersagen falsch sind, weil die Falsch-positiv-Rate selbst bei vielen falsch positiven Fällen klein bleibt. Precision-Recall-Kurven (PR-Kurven) zeigen den Anteil richtig positiver unter den positiven Vorhersagen und geben in solchen Fällen ein genaueres Bild (Saito & Rehmsmeier, 2015). Eine Kurve dominiert im ROC-Raum genau dann, wenn sie im PR-Raum dominiert; lineare Interpolation zwischen Punkten ist im PR-Raum aber falsch, und die Optimierung der Fläche unter der ROC-Kurve garantiert keine gute Fläche unter der PR-Kurve (Davis & Goadrich, 2006).

#### 6. Exact Match für extrahierte Antworten

Bei extraktiver Fragebeantwortung, bei der die Antwort ein Textabschnitt ist, werden Vorhersagen mit Exact Match bewertet, also danach, ob der vorhergesagte Abschnitt einer Referenzantwort entspricht, und mit einem F1-Score auf Token-Ebene, der Überlappungen teilweise anrechnet. Auf SQuAD erreichte eine Baseline mit logistischer Regression einen F1-Wert von 51,0 %, Menschen 86,8 % (Rajpurkar et al., 2016; [[text-similarity-metrics|Textähnlichkeitsmetriken]]).

#### Ursprung und Varianten

Sokolova & Lapalme (2009) systematisierten die Maße auf Basis der Konfusionsmatrix, Fawcett (2006) machte die ROC-Analyse einem breiten Publikum zugänglich, Davis & Goadrich (2006) sowie Saito & Rehmsmeier (2015) klärten die Rolle von Precision-Recall-Kurven, und Chicco & Jurman (2020) sprachen sich für den MCC aus. Rajpurkar et al. (2016) machten Exact Match und F1 für extraktive Fragebeantwortung bekannt.

### Wann einsetzen

- Wenn falsch positive Entscheidungen teuer sind, etwa wenn ein Dokument fälschlich markiert wird, zählt vor allem die Precision (Sokolova & Lapalme, 2009).
- Wenn übersehene positive Fälle teuer sind, etwa beim Screening, zählt vor allem der Recall (Sokolova & Lapalme, 2009).
- Wenn die Klassen stark unausgewogen sind, sind Precision-Recall-Kurven und MCC aussagekräftiger als Accuracy oder ROC (Saito & Rehmsmeier, 2015; Chicco & Jurman, 2020).

### Stärken und Grenzen

**Stärken**
- Metriken auf Basis der Konfusionsmatrix sind einfach und machen die Fehlerart sichtbar (Sokolova & Lapalme, 2009).
- ROC-Kurven und AUC fassen die Leistung über alle Schwellenwerte zusammen (Fawcett, 2006).
- Der MCC berücksichtigt alle vier Felder der Konfusionsmatrix (Chicco & Jurman, 2020).

**Einschränkungen**
- Accuracy und F1 können auf unausgewogenen Daten zu hoch ausfallen (Chicco & Jurman, 2020).
- ROC-Darstellungen können bei stark unausgewogenen Daten optisch täuschen (Saito & Rehmsmeier, 2015).
- Eine gute ROC-AUC bedeutet keine gute PR-AUC (Davis & Goadrich, 2006).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Accuracy | Anteil aller korrekten Vorhersagen (Sokolova & Lapalme, 2009) | Ausgewogene Klassen, gleiche Fehlerkosten |
| Precision / Recall / F1 | Fokus auf die positive Klasse; richtig negative Fälle bleiben unberücksichtigt (Sokolova & Lapalme, 2009) | Retrieval- und Extraktionsaufgaben |
| MCC | Ausgewogene Nutzung aller vier Felder der Konfusionsmatrix (Chicco & Jurman, 2020) | Unausgewogene binäre Klassifikation |
| ROC-AUC | Ranking-Qualität über alle Schwellen, unabhängig von der Klassenverteilung (Fawcett, 2006) | Vergleich bewertender Klassifikatoren |
| PR-AUC | Precision über verschiedene Recall-Stufen (Davis & Goadrich, 2006; Saito & Rehmsmeier, 2015) | Seltene positive Klasse |

### In der Praxis

Die Metrik wird vor der Evaluation anhand der Kosten der verschiedenen Fehler gewählt und zusammen mit der Konfusionsmatrix berichtet (Sokolova & Lapalme, 2009). Wenn Fairness eine Rolle spielt, werden die Metriken je Gruppe berechnet, da gleiche Gesamtgenauigkeit ungleiche Fehlerraten verbergen kann ([[fairness-metrics|Fairness-Metriken]]). Unterschiede zwischen Modellen werden auf Signifikanz geprüft, statt sie aus einzelnen Zahlen abzulesen ([[model-comparison|Modellvergleiche]]).

### Merksatz

Klassifikationsmetriken gewichten Fehler unterschiedlich; bei unausgewogenen Daten sagen Precision-Recall-Kurven und MCC mehr aus als die Accuracy.

### Quellen

- Sokolova, M. & Lapalme, G. (2009). *A systematic analysis of performance measures for classification tasks.* Information Processing & Management 45(4). [doi:10.1016/j.ipm.2009.03.002](https://doi.org/10.1016/j.ipm.2009.03.002)
- Fawcett, T. (2006). *An introduction to ROC analysis.* Pattern Recognition Letters 27(8). [doi:10.1016/j.patrec.2005.10.010](https://doi.org/10.1016/j.patrec.2005.10.010)
- Davis, J. & Goadrich, M. (2006). *The relationship between Precision-Recall and ROC curves.* ICML 2006. [doi:10.1145/1143844.1143874](https://doi.org/10.1145/1143844.1143874)
- Saito, T. & Rehmsmeier, M. (2015). *The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets.* PLoS ONE 10(3). [doi:10.1371/journal.pone.0118432](https://doi.org/10.1371/journal.pone.0118432)
- Chicco, D. & Jurman, G. (2020). *The advantages of the Matthews correlation coefficient (MCC) over F1 score and accuracy in binary classification evaluation.* BMC Genomics 21. [doi:10.1186/s12864-019-6413-7](https://doi.org/10.1186/s12864-019-6413-7)
- Rajpurkar, P. et al. (2016). *SQuAD: 100,000+ Questions for Machine Comprehension of Text.* EMNLP 2016. [arXiv:1606.05250](https://arxiv.org/abs/1606.05250)
