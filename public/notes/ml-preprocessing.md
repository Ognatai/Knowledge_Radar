---
title_en: Preprocessing for Machine Learning
title_de: Preprocessing für Machine Learning
entity_type: Method
sources:
- https://jmlr.org/papers/v12/pedregosa11a.html
- https://www.ijcai.org/Proceedings/95-2/Papers/016.pdf
- https://doi.org/10.1109/TKDE.2008.239
- https://doi.org/10.1613/jair.953
- https://doi.org/10.1145/1102351.1102430
- https://arxiv.org/abs/1706.04599
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Preprocessing prepares data for training and fair evaluation. Features are scaled, data is split into training, validation and test sets, and models are compared with cross-validation, for which ten-fold stratified cross-validation is a robust default (Kohavi, 1995). Imbalanced classes require suitable metrics and, if needed, resampling such as SMOTE (He & Garcia, 2009; Chawla et al., 2002), and predicted probabilities are often calibrated (Niculescu-Mizil & Caruana, 2005; Guo et al., 2017).

### How it works

The data is split before any model sees it. Transformations such as scaling are fitted on the training data only, models are compared with cross-validation, and the test set is used once at the end. Class imbalance and probability calibration are handled as part of the same pipeline.

```text
1. Scaling and pipelines
▼
2. Train, validation and test splits
▼
3. Cross-validation and stratification
▼
4. Imbalanced classes
▼
5. Probability calibration
```

#### 1. Scaling and pipelines

Scalers bring features to comparable ranges, which matters for distance-based and gradient-based methods ([[k-nearest-neighbors|k-Nearest Neighbors]]). In scikit-learn, preprocessing steps and models share a consistent API (Pedregosa et al., 2011), so they can be combined and fitted on the training data only, which avoids leaking information from validation or test data ([[feature-engineering|Feature Engineering]]).

#### 2. Train, validation and test splits

To estimate how well a model generalises, its accuracy must be measured on data not used for fitting (Kohavi, 1995). The test set is held back until the final evaluation; choices of model and hyperparameters are made on a validation set or with cross-validation on the training data.

#### 3. Cross-validation and stratification

Kohavi (1995) compared cross-validation and the bootstrap for estimating accuracy in a large-scale experiment with over half a million runs of C4.5 and naive Bayes on real-world datasets, varying the number of folds and whether the folds were stratified, i.e. kept the class proportions. For datasets like these, the recommended method for model selection was ten-fold stratified cross-validation, even when computation would allow more folds.

#### 4. Imbalanced classes

Data is imbalanced when classes are not approximately equally represented, and misclassifying the rare class is often costlier (Chawla et al., 2002). He & Garcia (2009) review sampling methods, cost-sensitive learning and assessment metrics suited to imbalanced data instead of plain accuracy ([[classification-metrics|Classification Metrics]]). SMOTE over-samples the minority class by creating synthetic examples between minority examples and their nearest minority neighbours; combined with under-sampling the majority class, it achieved better performance in ROC space than under-sampling alone (Chawla et al., 2002).

#### 5. Probability calibration

Some models produce distorted probabilities: boosted trees push them away from 0 and 1, naive Bayes toward 0 and 1, and Platt scaling and isotonic regression correct these distortions (Niculescu-Mizil & Caruana, 2005). Modern neural networks are also poorly calibrated; on most datasets, temperature scaling, a single-parameter variant of Platt scaling, was surprisingly effective (Guo et al., 2017).

#### Origin and variants

Kohavi (1995) established stratified ten-fold cross-validation as a default, Chawla et al. (2002) introduced SMOTE, He & Garcia (2009) reviewed imbalanced learning, and Niculescu-Mizil & Caruana (2005) and Guo et al. (2017) studied calibration for classical models and neural networks. scikit-learn implements most of these steps (Pedregosa et al., 2011).

### When to use it

- Always before training: split the data and fit transformations on the training part only (Pedregosa et al., 2011; Kohavi, 1995).
- When classes are imbalanced, choose suitable metrics and consider resampling (He & Garcia, 2009; Chawla et al., 2002).
- When predicted probabilities feed into decisions, check and correct their calibration (Niculescu-Mizil & Caruana, 2005; Guo et al., 2017).

### Strengths and limitations

**Strengths**
- Stratified ten-fold cross-validation gives reliable model selection on typical datasets (Kohavi, 1995).
- SMOTE combined with under-sampling improved minority-class performance (Chawla et al., 2002).
- Temperature scaling calibrates neural networks with a single parameter (Guo et al., 2017).

**Limitations**
- The cross-validation recommendation was derived for datasets similar to those studied (Kohavi, 1995).
- Plain accuracy is misleading on imbalanced data (He & Garcia, 2009).
- Calibration methods need held-out data to fit (Niculescu-Mizil & Caruana, 2005).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Single train/test split | One held-out set | Large datasets, final evaluation |
| Stratified k-fold cross-validation | k splits that keep class proportions (Kohavi, 1995) | Model selection on moderate datasets |
| SMOTE plus under-sampling | Synthetic minority examples, fewer majority examples (Chawla et al., 2002) | Strong class imbalance |
| Platt scaling, isotonic regression, temperature scaling | Post-hoc calibration of scores (Niculescu-Mizil & Caruana, 2005; Guo et al., 2017) | Probabilities used for decisions |

### In practice

All preprocessing steps are fitted within each cross-validation fold, ideally as a pipeline, so that validation data never influences the transformations (Pedregosa et al., 2011). Resampling such as SMOTE is applied to the training data only, never to the test data (Chawla et al., 2002). For time series, splits follow time order instead of random shuffling ([[time-series-analysis|Time Series Analysis]]).

### Key takeaway

Good preprocessing keeps evaluation honest: split first, fit transformations on training data only, use stratified cross-validation, and handle imbalance and calibration explicitly.

### Sources

- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12. [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html)
- Kohavi, R. (1995). *A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection.* IJCAI 1995. [PDF](https://www.ijcai.org/Proceedings/95-2/Papers/016.pdf)
- He, H. & Garcia, E. A. (2009). *Learning from Imbalanced Data.* IEEE Transactions on Knowledge and Data Engineering 21(9). [doi:10.1109/TKDE.2008.239](https://doi.org/10.1109/TKDE.2008.239)
- Chawla, N. V., Bowyer, K. W., Hall, L. O. & Kegelmeyer, W. P. (2002). *SMOTE: Synthetic Minority Over-sampling Technique.* Journal of Artificial Intelligence Research 16. [doi:10.1613/jair.953](https://doi.org/10.1613/jair.953)
- Niculescu-Mizil, A. & Caruana, R. (2005). *Predicting good probabilities with supervised learning.* ICML 2005. [doi:10.1145/1102351.1102430](https://doi.org/10.1145/1102351.1102430)
- Guo, C. et al. (2017). *On Calibration of Modern Neural Networks.* ICML 2017. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Preprocessing bereitet Daten für Training und faire Evaluation vor. Merkmale werden skaliert, Daten in Trainings-, Validierungs- und Testmengen aufgeteilt, und Modelle werden per Kreuzvalidierung verglichen, wofür zehnfache stratifizierte Kreuzvalidierung ein robuster Standard ist (Kohavi, 1995). Unausgewogene Klassen erfordern geeignete Metriken und bei Bedarf Resampling wie SMOTE (He & Garcia, 2009; Chawla et al., 2002), und vorhergesagte Wahrscheinlichkeiten werden oft kalibriert (Niculescu-Mizil & Caruana, 2005; Guo et al., 2017).

### Funktionsweise

Die Daten werden aufgeteilt, bevor ein Modell sie sieht. Transformationen wie Skalierung werden nur auf den Trainingsdaten angepasst, Modelle per Kreuzvalidierung verglichen, und die Testmenge wird einmal am Ende verwendet. Klassenungleichgewicht und Kalibrierung werden in derselben Pipeline behandelt.

```text
1. Skalierung und Pipelines
▼
2. Trainings-, Validierungs- und Testmenge
▼
3. Kreuzvalidierung und Stratifizierung
▼
4. Unausgewogene Klassen
▼
5. Kalibrierung von Wahrscheinlichkeiten
```

#### 1. Skalierung und Pipelines

Scaler bringen Merkmale auf vergleichbare Bereiche, was für abstands- und gradientenbasierte Verfahren wichtig ist ([[k-nearest-neighbors|k-Nearest Neighbors]]). In scikit-learn teilen Vorverarbeitungsschritte und Modelle eine konsistente API (Pedregosa et al., 2011), sodass sie kombiniert und nur auf den Trainingsdaten angepasst werden können; das verhindert, dass Informationen aus Validierungs- oder Testdaten einfließen ([[feature-engineering|Feature Engineering]]).

#### 2. Trainings-, Validierungs- und Testmenge

Um abzuschätzen, wie gut ein Modell generalisiert, muss seine Genauigkeit auf Daten gemessen werden, die nicht zur Anpassung dienten (Kohavi, 1995). Die Testmenge bleibt bis zur abschließenden Evaluation zurückgehalten; Modell- und Hyperparameterwahl erfolgen auf einer Validierungsmenge oder per Kreuzvalidierung auf den Trainingsdaten.

#### 3. Kreuzvalidierung und Stratifizierung

Kohavi (1995) verglich Kreuzvalidierung und Bootstrap zur Genauigkeitsschätzung in einem groß angelegten Experiment mit über einer halben Million Läufen von C4.5 und Naive Bayes auf realen Datensätzen und variierte dabei die Zahl der Folds und ob diese stratifiziert waren, also die Klassenanteile beibehielten. Für Datensätze dieser Art war die empfohlene Methode zur Modellauswahl die zehnfache stratifizierte Kreuzvalidierung, selbst wenn die Rechenleistung mehr Folds erlauben würde.

#### 4. Unausgewogene Klassen

Daten sind unausgewogen, wenn die Klassen nicht annähernd gleich häufig vertreten sind, und eine Fehlklassifikation der seltenen Klasse ist oft teurer (Chawla et al., 2002). He & Garcia (2009) geben einen Überblick über Sampling-Verfahren, kostensensitives Lernen und Bewertungsmetriken, die sich für unausgewogene Daten besser eignen als die reine Accuracy ([[classification-metrics|Klassifikationsmetriken]]). SMOTE überabtastet die Minderheitsklasse, indem es synthetische Beispiele zwischen Minderheitsbeispielen und ihren nächsten Nachbarn derselben Klasse erzeugt; kombiniert mit Unterabtastung der Mehrheitsklasse erzielte es im ROC-Raum bessere Ergebnisse als Unterabtastung allein (Chawla et al., 2002).

#### 5. Kalibrierung von Wahrscheinlichkeiten

Manche Modelle liefern verzerrte Wahrscheinlichkeiten: Boosted Trees drängen sie von 0 und 1 weg, Naive Bayes zu 0 und 1 hin, und Platt Scaling sowie isotone Regression korrigieren diese Verzerrungen (Niculescu-Mizil & Caruana, 2005). Auch moderne neuronale Netze sind schlecht kalibriert; auf den meisten Datensätzen war Temperature Scaling, eine Variante von Platt Scaling mit einem einzigen Parameter, überraschend wirksam (Guo et al., 2017).

#### Ursprung und Varianten

Kohavi (1995) etablierte die stratifizierte zehnfache Kreuzvalidierung als Standard, Chawla et al. (2002) führten SMOTE ein, He & Garcia (2009) gaben einen Überblick über das Lernen aus unausgewogenen Daten, und Niculescu-Mizil & Caruana (2005) sowie Guo et al. (2017) untersuchten die Kalibrierung klassischer Modelle und neuronaler Netze. scikit-learn implementiert die meisten dieser Schritte (Pedregosa et al., 2011).

### Wann einsetzen

- Immer vor dem Training: Daten aufteilen und Transformationen nur auf dem Trainingsteil anpassen (Pedregosa et al., 2011; Kohavi, 1995).
- Bei unausgewogenen Klassen geeignete Metriken wählen und Resampling erwägen (He & Garcia, 2009; Chawla et al., 2002).
- Wenn vorhergesagte Wahrscheinlichkeiten in Entscheidungen einfließen, ihre Kalibrierung prüfen und korrigieren (Niculescu-Mizil & Caruana, 2005; Guo et al., 2017).

### Stärken und Grenzen

**Stärken**
- Stratifizierte zehnfache Kreuzvalidierung ermöglicht eine verlässliche Modellauswahl auf typischen Datensätzen (Kohavi, 1995).
- SMOTE in Kombination mit Unterabtastung verbesserte die Ergebnisse für die Minderheitsklasse (Chawla et al., 2002).
- Temperature Scaling kalibriert neuronale Netze mit einem einzigen Parameter (Guo et al., 2017).

**Einschränkungen**
- Die Empfehlung zur Kreuzvalidierung wurde für Datensätze ähnlich den untersuchten abgeleitet (Kohavi, 1995).
- Reine Accuracy ist bei unausgewogenen Daten irreführend (He & Garcia, 2009).
- Kalibrierungsverfahren brauchen zurückgehaltene Daten zur Anpassung (Niculescu-Mizil & Caruana, 2005).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Einfache Aufteilung in Training und Test | Eine zurückgehaltene Menge | Große Datensätze, abschließende Evaluation |
| Stratifizierte k-fache Kreuzvalidierung | k Aufteilungen, die die Klassenanteile erhalten (Kohavi, 1995) | Modellauswahl auf mittelgroßen Datensätzen |
| SMOTE plus Unterabtastung | Synthetische Minderheitsbeispiele, weniger Mehrheitsbeispiele (Chawla et al., 2002) | Starkes Klassenungleichgewicht |
| Platt Scaling, isotone Regression, Temperature Scaling | Nachträgliche Kalibrierung von Werten (Niculescu-Mizil & Caruana, 2005; Guo et al., 2017) | Wahrscheinlichkeiten, die in Entscheidungen einfließen |

### In der Praxis

Alle Vorverarbeitungsschritte werden innerhalb jedes Kreuzvalidierungs-Folds angepasst, idealerweise als Pipeline, damit Validierungsdaten die Transformationen nie beeinflussen (Pedregosa et al., 2011). Resampling wie SMOTE wird nur auf die Trainingsdaten angewendet, nie auf die Testdaten (Chawla et al., 2002). Bei Zeitreihen folgen die Aufteilungen der zeitlichen Reihenfolge statt einer zufälligen Mischung ([[time-series-analysis|Zeitreihenanalyse]]).

### Merksatz

Gutes Preprocessing hält die Evaluation ehrlich: zuerst aufteilen, Transformationen nur auf Trainingsdaten anpassen, stratifiziert kreuzvalidieren und Ungleichgewicht sowie Kalibrierung ausdrücklich behandeln.

### Quellen

- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12. [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html)
- Kohavi, R. (1995). *A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection.* IJCAI 1995. [PDF](https://www.ijcai.org/Proceedings/95-2/Papers/016.pdf)
- He, H. & Garcia, E. A. (2009). *Learning from Imbalanced Data.* IEEE Transactions on Knowledge and Data Engineering 21(9). [doi:10.1109/TKDE.2008.239](https://doi.org/10.1109/TKDE.2008.239)
- Chawla, N. V., Bowyer, K. W., Hall, L. O. & Kegelmeyer, W. P. (2002). *SMOTE: Synthetic Minority Over-sampling Technique.* Journal of Artificial Intelligence Research 16. [doi:10.1613/jair.953](https://doi.org/10.1613/jair.953)
- Niculescu-Mizil, A. & Caruana, R. (2005). *Predicting good probabilities with supervised learning.* ICML 2005. [doi:10.1145/1102351.1102430](https://doi.org/10.1145/1102351.1102430)
- Guo, C. et al. (2017). *On Calibration of Modern Neural Networks.* ICML 2017. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)
