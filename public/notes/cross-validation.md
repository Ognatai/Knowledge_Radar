---
title_en: Cross-validation
title_de: Kreuzvalidierung
entity_type: Method
aliases:
- k-fold cross-validation
sources:
- https://www.ijcai.org/Proceedings/95-2/Papers/016.pdf
- https://doi.org/10.1186/1471-2105-7-91
- https://www.jmlr.org/papers/v11/cawley10a.html
- https://doi.org/10.1162/089976698300017197
- https://otexts.com/fpp3/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR
Cross-validation estimates how well a model will perform on new data: the data is split into k parts, the model is trained k times on all parts but one and tested on the remaining part, and the k results are averaged (Kohavi, 1995). It is used to compare models and to tune hyperparameters; if the same cross-validation is used both to tune a model and to report its error, the estimate is biased, which nested cross-validation avoids (Varma & Simon, 2006).

### How it works

```text
data:    [ fold 1 | fold 2 | fold 3 | fold 4 | fold 5 ]
run 1:     TEST     train    train    train    train
run 2:     train    TEST     train    train    train
 ...
run 5:     train    train    train    train    TEST
estimate = average of the 5 test results
```

#### 1. Hold-out
The simplest estimate splits the data once into a training and a test set. Because a model usually gets better with more training data, the hold-out estimate is pessimistic, and it depends on which instances happen to land in the test set (Kohavi, 1995).

#### 2. k-fold cross-validation
The data is split at random into k mutually exclusive folds of about equal size. The model is trained k times, each time on all folds except one, and tested on the fold left out; the estimate combines the test results of all k runs, so every instance is used for testing exactly once (Kohavi, 1995).

#### 3. Stratification and leave-one-out
In stratified cross-validation, each fold contains about the same class proportions as the whole dataset (Kohavi, 1995). Leave-one-out is the extreme case k = n: almost unbiased, but with high variance, which makes its estimates unreliable (Kohavi, 1995). In a study of over half a million runs on real-world datasets, ten-fold stratified cross-validation was the best method for model selection, even when computation allowed more folds (Kohavi, 1995).

#### 4. Nested cross-validation
When cross-validation is used to choose hyperparameters, the error of the chosen model on the same folds is no longer an honest estimate. Nested cross-validation adds a loop: an inner cross-validation tunes the hyperparameters, an outer one estimates the error of the whole procedure, tuning included. All steps of building the model must be repeated inside each outer fold (Varma & Simon, 2006). The idea goes back to the "double cross" of Stone (1974), as Cawley & Talbot (2010) note.

#### 5. Time series
For time series, folds must respect time order. In time series cross-validation, also called evaluation on a rolling forecasting origin, each test set follows its training set in time, so no future observations are used for a forecast; the error is averaged over the test sets (Hyndman & Athanasopoulos, 2021). See [[time-series-analysis|Time Series Analysis]].

#### Origin and variants
Kohavi (1995) compared cross-validation with the bootstrap and gave the widely used recommendation of ten-fold stratified cross-validation; the bootstrap had low variance but extremely large bias on some problems. Dietterich (1998) studied statistical tests built on cross-validation and proposed the 5×2 cv test ([[model-comparison|Model Comparison]]). Varma & Simon (2006) and Cawley & Talbot (2010) showed how tuning on cross-validation biases the reported error.

### When to use it
- Estimating the performance of a model when data is too scarce to set aside a large test set (Kohavi, 1995).
- Selecting between models or hyperparameter settings, for example the cost parameter and kernel of [[support-vector-machines|support vector machines]] ([[regularization-and-hyperparameters|Regularisation and Hyperparameters]]).
- Reporting the error of a tuned model, with nested cross-validation (Varma & Simon, 2006).
- Comparing two learning algorithms with a statistical test, such as the 5×2 cv test (Dietterich, 1998; [[statistics-fundamentals|Statistics Fundamentals]]).
- Evaluating forecasts on a rolling origin (Hyndman & Athanasopoulos, 2021).

### Strengths and limitations

**Strengths**
- Uses every instance for both training and testing, which matters for small datasets (Kohavi, 1995).
- Less dependent on a single random split than hold-out (Kohavi, 1995).
- Nested cross-validation gives an almost unbiased estimate of the error of a tuned model (Varma & Simon, 2006).

**Limitations**
- The model is trained k times (Kohavi, 1995), and unbiased evaluation of a tuned model needs even more computationally intensive protocols such as nested cross-validation (Cawley & Talbot, 2010).
- Tuning on cross-validation and reporting the same estimate is biased: on data with no difference between classes, the cross-validation error of tuned classifiers was below 30% on 18.5% (shrunken centroids) and 38% (SVM) of the datasets, while their performance on independent test data was no better than chance (Varma & Simon, 2006).
- Over-fitting the model selection criterion can cause performance differences of the same size as those between learning algorithms (Cawley & Talbot, 2010).
- A paired t test over the folds of 10-fold cross-validation has a somewhat elevated type I error (Dietterich, 1998).
- Random folds are wrong for time series and other ordered data (Hyndman & Athanasopoulos, 2021).

### Comparison
| Approach | How it differs | Suited for |
|----------|---------------|------------|
| Hold-out | One train–test split; pessimistic and dependent on the split (Kohavi, 1995) | Large datasets, final evaluation on an untouched test set |
| k-fold (stratified) cross-validation | k splits, each instance tested once; ten-fold stratified recommended for model selection (Kohavi, 1995) | Model selection and error estimation |
| Leave-one-out | k = n; almost unbiased, high variance (Kohavi, 1995) | Very small datasets |
| Nested cross-validation | Inner loop tunes, outer loop estimates the error of the tuned procedure (Varma & Simon, 2006) | Reporting the performance of a tuned model |
| Rolling forecasting origin | Test data always follows training data in time (Hyndman & Athanasopoulos, 2021) | Time series |

### In practice
Every step that learns from data, such as scaling, feature selection or oversampling, belongs inside the cross-validation loop and is fitted on the training folds only; otherwise information from the test fold leaks into the model ([[ml-preprocessing|ML Preprocessing]]). Proper use of cross-validation requires that all steps of the algorithm, including tuning, are repeated in each loop (Varma & Simon, 2006). A final test set is still kept apart and used once at the end ([[ml-preprocessing|ML Preprocessing]]). Cross-validation is usually run on [[classification-metrics|classification metrics]] or regression errors; for imbalanced classes, stratified folds keep the class proportions (Kohavi, 1995). See [[classical-machine-learning|Classical Machine Learning]] for its role in the overall workflow.

### Key takeaway
Cross-validation trains and tests a model on several splits of the same data to estimate how it will perform on new data; whatever is tuned on it must be evaluated with an outer loop it has not seen.

### Sources
- Kohavi, R. (1995). *A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection.* IJCAI 1995. [PDF](https://www.ijcai.org/Proceedings/95-2/Papers/016.pdf)
- Varma, S. & Simon, R. (2006). *Bias in error estimation when using cross-validation for model selection.* BMC Bioinformatics 7, 91. [doi:10.1186/1471-2105-7-91](https://doi.org/10.1186/1471-2105-7-91)
- Cawley, G. C. & Talbot, N. L. C. (2010). *On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation.* Journal of Machine Learning Research 11. [JMLR](https://www.jmlr.org/papers/v11/cawley10a.html)
- Dietterich, T. G. (1998). *Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms.* Neural Computation 10(7). [doi:10.1162/089976698300017197](https://doi.org/10.1162/089976698300017197)
- Hyndman, R. J. & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3rd ed.), section 5.10. OTexts. [online edition](https://otexts.com/fpp3/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Basis der angegebenen Quellen; sie kann unvollständig, veraltet oder fehlerhaft sein.

### TL;DR
Kreuzvalidierung schätzt, wie gut ein Modell auf neuen Daten abschneiden wird: Die Daten werden in k Teile aufgeteilt, das Modell wird k-mal auf allen Teilen bis auf einen trainiert und auf dem verbleibenden Teil getestet, und die k Ergebnisse werden gemittelt (Kohavi, 1995). Sie dient zum Vergleich von Modellen und zur Abstimmung von Hyperparametern; wird dieselbe Kreuzvalidierung sowohl zum Abstimmen eines Modells als auch zum Berichten seines Fehlers genutzt, ist die Schätzung verzerrt, was verschachtelte Kreuzvalidierung (Nested Cross-Validation) vermeidet (Varma & Simon, 2006).

### Funktionsweise

```text
Daten:      [ Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 ]
Lauf 1:       TEST     Train    Train    Train    Train
Lauf 2:       Train    TEST     Train    Train    Train
 ...
Lauf 5:       Train    Train    Train    Train    TEST
Schätzung = Mittel der 5 Testergebnisse
```

#### 1. Hold-out
Die einfachste Schätzung teilt die Daten einmal in eine Trainings- und eine Testmenge. Da ein Modell mit mehr Trainingsdaten meist besser wird, ist die Hold-out-Schätzung pessimistisch, und sie hängt davon ab, welche Instanzen zufällig in der Testmenge landen (Kohavi, 1995).

#### 2. k-fache Kreuzvalidierung
Die Daten werden zufällig in k disjunkte Folds etwa gleicher Größe geteilt. Das Modell wird k-mal trainiert, jeweils auf allen Folds bis auf einen, und auf dem ausgelassenen Fold getestet; die Schätzung fasst die Testergebnisse aller k Läufe zusammen, sodass jede Instanz genau einmal zum Testen dient (Kohavi, 1995).

#### 3. Stratifizierung und Leave-one-out
Bei stratifizierter Kreuzvalidierung enthält jeder Fold etwa dieselben Klassenanteile wie der gesamte Datensatz (Kohavi, 1995). Leave-one-out ist der Extremfall k = n: nahezu unverzerrt, aber mit hoher Varianz, was die Schätzungen unzuverlässig macht (Kohavi, 1995). In einer Studie mit über einer halben Million Läufen auf realen Datensätzen war zehnfache stratifizierte Kreuzvalidierung die beste Methode zur Modellauswahl, selbst wenn die Rechenleistung mehr Folds erlaubt hätte (Kohavi, 1995).

#### 4. Verschachtelte Kreuzvalidierung
Wird Kreuzvalidierung zur Wahl von Hyperparametern genutzt, ist der Fehler des gewählten Modells auf denselben Folds keine ehrliche Schätzung mehr. Verschachtelte Kreuzvalidierung ergänzt eine Schleife: Eine innere Kreuzvalidierung stimmt die Hyperparameter ab, eine äußere schätzt den Fehler des gesamten Verfahrens einschließlich der Abstimmung. Alle Schritte der Modellbildung müssen in jedem äußeren Fold wiederholt werden (Varma & Simon, 2006). Die Idee geht auf das „Double Cross“ von Stone (1974) zurück, wie Cawley & Talbot (2010) anmerken.

#### 5. Zeitreihen
Bei Zeitreihen müssen die Folds die zeitliche Reihenfolge einhalten. Bei der Zeitreihen-Kreuzvalidierung, auch Evaluation mit rollierendem Prognoseursprung genannt, folgt jede Testmenge zeitlich auf ihre Trainingsmenge, sodass für eine Prognose keine zukünftigen Beobachtungen verwendet werden; der Fehler wird über die Testmengen gemittelt (Hyndman & Athanasopoulos, 2021). Siehe [[time-series-analysis|Zeitreihenanalyse]].

#### Ursprung und Varianten
Kohavi (1995) verglich Kreuzvalidierung mit dem Bootstrap und gab die verbreitete Empfehlung der zehnfachen stratifizierten Kreuzvalidierung; der Bootstrap hatte geringe Varianz, aber bei manchen Problemen eine extrem große Verzerrung. Dietterich (1998) untersuchte statistische Tests auf Basis von Kreuzvalidierung und schlug den 5×2-cv-Test vor ([[model-comparison|Modellvergleich]]). Varma & Simon (2006) und Cawley & Talbot (2010) zeigten, wie Abstimmung per Kreuzvalidierung den berichteten Fehler verzerrt.

### Wann einsetzen
- Die Leistung eines Modells schätzen, wenn zu wenige Daten vorliegen, um eine große Testmenge zurückzuhalten (Kohavi, 1995).
- Zwischen Modellen oder Hyperparameter-Einstellungen wählen, etwa Kostenparameter und Kernel von [[support-vector-machines|Support Vector Machines]] ([[regularization-and-hyperparameters|Regularisierung und Hyperparameter]]).
- Den Fehler eines abgestimmten Modells berichten, mit verschachtelter Kreuzvalidierung (Varma & Simon, 2006).
- Zwei Lernverfahren mit einem statistischen Test vergleichen, etwa dem 5×2-cv-Test (Dietterich, 1998; [[statistics-fundamentals|Statistische Grundlagen]]).
- Prognosen mit rollierendem Ursprung evaluieren (Hyndman & Athanasopoulos, 2021).

### Stärken und Grenzen

**Stärken**
- Jede Instanz dient sowohl dem Training als auch dem Test, was bei kleinen Datensätzen zählt (Kohavi, 1995).
- Weniger abhängig von einer einzelnen zufälligen Aufteilung als Hold-out (Kohavi, 1995).
- Verschachtelte Kreuzvalidierung liefert eine nahezu unverzerrte Schätzung des Fehlers eines abgestimmten Modells (Varma & Simon, 2006).

**Grenzen**
- Das Modell wird k-mal trainiert (Kohavi, 1995), und die unverzerrte Evaluation eines abgestimmten Modells braucht noch rechenintensivere Protokolle wie verschachtelte Kreuzvalidierung (Cawley & Talbot, 2010).
- Abstimmen per Kreuzvalidierung und Berichten derselben Schätzung ist verzerrt: Auf Daten ohne Unterschied zwischen den Klassen lag der Kreuzvalidierungsfehler abgestimmter Klassifikatoren bei 18,5 % (Shrunken Centroids) bzw. 38 % (SVM) der Datensätze unter 30 %, während ihre Leistung auf unabhängigen Testdaten nicht besser als Zufall war (Varma & Simon, 2006).
- Überanpassung an das Modellauswahlkriterium kann Leistungsunterschiede derselben Größenordnung verursachen wie die zwischen Lernverfahren (Cawley & Talbot, 2010).
- Ein gepaarter t-Test über die Folds einer zehnfachen Kreuzvalidierung hat einen etwas erhöhten Fehler 1. Art (Dietterich, 1998).
- Zufällige Folds sind für Zeitreihen und andere geordnete Daten falsch (Hyndman & Athanasopoulos, 2021).

### Vergleich
| Ansatz | Unterschied | Geeignet für |
|--------|-------------|--------------|
| Hold-out | Eine Aufteilung in Training und Test; pessimistisch und abhängig von der Aufteilung (Kohavi, 1995) | Große Datensätze, finale Evaluation auf einer unberührten Testmenge |
| k-fache (stratifizierte) Kreuzvalidierung | k Aufteilungen, jede Instanz einmal getestet; zehnfach stratifiziert für die Modellauswahl empfohlen (Kohavi, 1995) | Modellauswahl und Fehlerschätzung |
| Leave-one-out | k = n; nahezu unverzerrt, hohe Varianz (Kohavi, 1995) | Sehr kleine Datensätze |
| Verschachtelte Kreuzvalidierung | Innere Schleife stimmt ab, äußere schätzt den Fehler des abgestimmten Verfahrens (Varma & Simon, 2006) | Leistung eines abgestimmten Modells berichten |
| Rollierender Prognoseursprung | Testdaten folgen zeitlich immer auf die Trainingsdaten (Hyndman & Athanasopoulos, 2021) | Zeitreihen |

### In der Praxis
Jeder Schritt, der aus Daten lernt, etwa Skalierung, Merkmalsauswahl oder Oversampling, gehört in die Kreuzvalidierungsschleife und wird nur auf den Trainings-Folds angepasst; sonst gelangen Informationen aus dem Test-Fold ins Modell ([[ml-preprocessing|ML-Vorverarbeitung]]). Korrekt eingesetzt verlangt Kreuzvalidierung, dass alle Schritte des Verfahrens einschließlich der Abstimmung in jeder Schleife wiederholt werden (Varma & Simon, 2006). Eine finale Testmenge wird trotzdem zurückgehalten und am Ende einmal verwendet ([[ml-preprocessing|ML-Vorverarbeitung]]). Ausgewertet wird meist mit [[classification-metrics|Klassifikationsmetriken]] oder Regressionsfehlern; bei unausgewogenen Klassen halten stratifizierte Folds die Klassenanteile (Kohavi, 1995). Zur Rolle im gesamten Ablauf siehe [[classical-machine-learning|Klassisches Machine Learning]].

### Merksatz
Kreuzvalidierung trainiert und testet ein Modell auf mehreren Aufteilungen derselben Daten, um seine Leistung auf neuen Daten zu schätzen; was mit ihr abgestimmt wird, muss mit einer äußeren Schleife evaluiert werden, die es nicht gesehen hat.

### Quellen
- Kohavi, R. (1995). *A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection.* IJCAI 1995. [PDF](https://www.ijcai.org/Proceedings/95-2/Papers/016.pdf)
- Varma, S. & Simon, R. (2006). *Bias in error estimation when using cross-validation for model selection.* BMC Bioinformatics 7, 91. [doi:10.1186/1471-2105-7-91](https://doi.org/10.1186/1471-2105-7-91)
- Cawley, G. C. & Talbot, N. L. C. (2010). *On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation.* Journal of Machine Learning Research 11. [JMLR](https://www.jmlr.org/papers/v11/cawley10a.html)
- Dietterich, T. G. (1998). *Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms.* Neural Computation 10(7). [doi:10.1162/089976698300017197](https://doi.org/10.1162/089976698300017197)
- Hyndman, R. J. & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3rd ed.), section 5.10. OTexts. [online edition](https://otexts.com/fpp3/)
