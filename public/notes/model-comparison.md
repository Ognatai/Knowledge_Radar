---
title_en: Model Comparison
title_de: Modellvergleiche
entity_type: Method
sources:
- https://doi.org/10.1162/089976698300017197
- https://jmlr.org/papers/v7/demsar06a.html
- https://arxiv.org/abs/2103.03098
- https://arxiv.org/abs/1909.03004
- https://arxiv.org/abs/1807.03341
- https://arxiv.org/abs/2211.09110
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Model comparison asks whether one model really performs better than another, not just on one run or one test set. A single difference in a metric can be noise from data sampling, initialisation or hyperparameter choices (Bouthillier et al., 2021), so comparisons use suitable statistical tests (Dietterich, 1998; Demšar, 2006), report the computational budget behind each result (Dodge et al., 2019) and measure several criteria, not only accuracy (Liang et al., 2022).

### How it works

The criteria and test data are fixed in advance, each model is trained and evaluated under the same conditions, repeatedly where possible, and differences are tested statistically and reported together with variance and cost.

```text
1. Comparison criteria
▼
2. Statistical tests on one dataset
▼
3. Comparisons over multiple datasets
▼
4. Sources of variance
▼
5. Reporting the budget
▼
6. Typical mistakes
```

#### 1. Comparison criteria

Accuracy alone rarely decides which model is better. Holistic evaluation of language models measures several metrics, accuracy, calibration, robustness, fairness, bias, toxicity and efficiency, across many scenarios, so that trade-offs between them become visible (Liang et al., 2022; [[llm-evaluation|LLM Evaluation]]). Cost, latency and interpretability are further criteria in practice.

#### 2. Statistical tests on one dataset

Dietterich (1998) compared five tests for whether one learning algorithm outperforms another on one task. A difference-of-proportions test and a paired t test over several random train-test splits had a high probability of detecting differences that do not exist and should not be used; the paired t test over 10-fold cross-validation had a somewhat elevated type I error. McNemar's test and the 5×2 cv test had acceptable type I error ([[statistics-fundamentals|Statistics Fundamentals]]).

#### 3. Comparisons over multiple datasets

When classifiers are compared over several datasets, Demšar (2006) recommends non-parametric tests: the Wilcoxon signed-ranks test for two classifiers, and the Friedman test with post-hoc tests for several classifiers. Results can be shown in critical difference diagrams.

#### 4. Sources of variance

Strong evidence that one algorithm outperforms another would require many trials varying data sampling, data augmentation, parameter initialisation and hyperparameters, which is expensive (Bouthillier et al., 2021). Modelling the whole benchmarking process, the authors found that variance from data sampling, initialisation and hyperparameter choice markedly affects results, and that randomising more sources of variation in fewer runs approximates the ideal estimate at a 51 times lower compute cost. They derive recommendations for performance comparisons.

#### 5. Reporting the budget

Test-set scores alone are insufficient to conclude which model performs best (Dodge et al., 2019). The authors propose reporting the expected validation performance of the best model found as a function of the computation budget, such as the number of hyperparameter trials. With this, several published comparisons would have reached a different conclusion with more or less computation.

#### 6. Typical mistakes

Lipton & Steinhardt (2018) describe troubling trends in machine learning papers, among them failing to distinguish explanation from speculation and failing to identify the sources of empirical gains, for example attributing improvements to architectural changes when they actually stem from hyperparameter tuning. Unequal tuning effort between a new model and its baselines is therefore a common source of misleading comparisons.

#### Origin and variants

Dietterich (1998) and Demšar (2006) established statistical tests for comparing learning algorithms. Lipton & Steinhardt (2018), Dodge et al. (2019) and Bouthillier et al. (2021) addressed reporting practice and variance in benchmarks, and HELM (Liang et al., 2022) extended comparisons of language models to many metrics and scenarios.

### When to use it

- When a new model is claimed to be better than a baseline, its advantage should be tested statistically (Dietterich, 1998).
- When several models are compared across many datasets, rank-based tests apply (Demšar, 2006).
- When choosing a model for production, several criteria such as calibration, robustness and efficiency should be compared (Liang et al., 2022).

### Strengths and limitations

**Strengths**
- Suitable tests keep false claims of improvement under control (Dietterich, 1998).
- Non-parametric tests over many datasets make few assumptions (Demšar, 2006).
- Reporting the budget makes results reproducible and comparable (Dodge et al., 2019).

**Limitations**
- Repeated training to estimate variance is expensive (Bouthillier et al., 2021).
- Some widely used tests have a high type I error (Dietterich, 1998).
- Gains are often attributed to the wrong cause (Lipton & Steinhardt, 2018).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| McNemar's test / 5×2 cv | Controlled type I error on one dataset (Dietterich, 1998) | Two algorithms, one task |
| Wilcoxon / Friedman tests | Rank-based tests over many datasets (Demšar, 2006) | Benchmarks with several datasets |
| Randomising sources of variance | Varies data, initialisation and hyperparameters across runs (Bouthillier et al., 2021) | Deep learning benchmarks |
| Expected validation performance | Performance as a function of compute budget (Dodge et al., 2019) | Comparing models with different tuning effort |
| Holistic evaluation | Many metrics across many scenarios (Liang et al., 2022) | Language models |

### In practice

All models get the same data splits and comparable tuning budgets, and the budget is reported (Dodge et al., 2019). Results are given as means with variability over several runs, and differences are tested (Bouthillier et al., 2021; Dietterich, 1998). For prompt and LLM comparisons, the same principles apply ([[prompt-comparison|Prompt Comparison]]).

### Key takeaway

A model is only shown to be better if the difference survives the variance of training and data, is tested with a suitable test and was obtained with comparable effort for all models.

### Sources

- Dietterich, T. G. (1998). *Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms.* Neural Computation 10(7). [doi:10.1162/089976698300017197](https://doi.org/10.1162/089976698300017197)
- Demšar, J. (2006). *Statistical Comparisons of Classifiers over Multiple Data Sets.* JMLR 7. [JMLR](https://jmlr.org/papers/v7/demsar06a.html)
- Bouthillier, X. et al. (2021). *Accounting for Variance in Machine Learning Benchmarks.* MLSys 2021. [arXiv:2103.03098](https://arxiv.org/abs/2103.03098)
- Dodge, J. et al. (2019). *Show Your Work: Improved Reporting of Experimental Results.* EMNLP 2019. [arXiv:1909.03004](https://arxiv.org/abs/1909.03004)
- Lipton, Z. C. & Steinhardt, J. (2018). *Troubling Trends in Machine Learning Scholarship.* [arXiv:1807.03341](https://arxiv.org/abs/1807.03341)
- Liang, P. et al. (2022). *Holistic Evaluation of Language Models.* TMLR. [arXiv:2211.09110](https://arxiv.org/abs/2211.09110)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Modellvergleich fragt, ob ein Modell wirklich besser ist als ein anderes, nicht nur in einem Lauf oder auf einer Testmenge. Ein einzelner Unterschied in einer Metrik kann Rauschen sein, das aus Datenstichprobe, Initialisierung oder Hyperparameterwahl stammt (Bouthillier et al., 2021). Vergleiche nutzen daher geeignete statistische Tests (Dietterich, 1998; Demšar, 2006), berichten den Rechenaufwand hinter jedem Ergebnis (Dodge et al., 2019) und messen mehrere Kriterien, nicht nur die Accuracy (Liang et al., 2022).

### Funktionsweise

Kriterien und Testdaten werden vorab festgelegt, jedes Modell wird unter gleichen Bedingungen trainiert und evaluiert, nach Möglichkeit mehrfach, und Unterschiede werden statistisch geprüft und zusammen mit Varianz und Aufwand berichtet.

```text
1. Vergleichskriterien
▼
2. Statistische Tests auf einem Datensatz
▼
3. Vergleiche über mehrere Datensätze
▼
4. Quellen der Varianz
▼
5. Den Aufwand berichten
▼
6. Typische Fehler
```

#### 1. Vergleichskriterien

Die Accuracy allein entscheidet selten, welches Modell besser ist. Die ganzheitliche Evaluation von Sprachmodellen misst mehrere Metriken, nämlich Accuracy, Kalibrierung, Robustheit, Fairness, Bias, Toxizität und Effizienz, über viele Szenarien, sodass Zielkonflikte zwischen ihnen sichtbar werden (Liang et al., 2022; [[llm-evaluation|LLM-Evaluation]]). Kosten, Latenz und Interpretierbarkeit sind in der Praxis weitere Kriterien.

#### 2. Statistische Tests auf einem Datensatz

Dietterich (1998) verglich fünf Tests dafür, ob ein Lernverfahren ein anderes auf einer Aufgabe übertrifft. Ein Test auf die Differenz zweier Anteile und ein gepaarter t-Test über mehrere zufällige Trainings-Test-Aufteilungen fanden mit hoher Wahrscheinlichkeit Unterschiede, die nicht existieren, und sollten nicht verwendet werden; der gepaarte t-Test über zehnfache Kreuzvalidierung hatte einen etwas erhöhten Fehler erster Art. Der McNemar-Test und der 5×2-cv-Test hatten einen akzeptablen Fehler erster Art ([[statistics-fundamentals|Statistik-Grundlagen]]).

#### 3. Vergleiche über mehrere Datensätze

Werden Klassifikatoren über mehrere Datensätze verglichen, empfiehlt Demšar (2006) nichtparametrische Tests: den Wilcoxon-Vorzeichen-Rang-Test für zwei Klassifikatoren und den Friedman-Test mit Post-hoc-Tests für mehrere Klassifikatoren. Die Ergebnisse lassen sich in Critical-Difference-Diagrammen darstellen.

#### 4. Quellen der Varianz

Belastbare Belege dafür, dass ein Verfahren ein anderes übertrifft, würden viele Läufe mit variierter Datenstichprobe, Datenaugmentation, Parameterinitialisierung und Hyperparametern erfordern, was teuer ist (Bouthillier et al., 2021). Bei der Modellierung des gesamten Benchmark-Prozesses fanden die Autoren, dass die Varianz aus Datenstichprobe, Initialisierung und Hyperparameterwahl die Ergebnisse deutlich beeinflusst und dass das Randomisieren mehrerer Varianzquellen in weniger Läufen die ideale Schätzung bei 51-mal geringerem Rechenaufwand annähert. Daraus leiten sie Empfehlungen für Leistungsvergleiche ab.

#### 5. Den Aufwand berichten

Ergebnisse auf der Testmenge allein reichen nicht aus, um zu entscheiden, welches Modell am besten ist (Dodge et al., 2019). Die Autoren schlagen vor, die erwartete Validierungsleistung des besten gefundenen Modells als Funktion des Rechenbudgets zu berichten, etwa der Zahl der Hyperparameterversuche. Damit wären mehrere veröffentlichte Vergleiche bei mehr oder weniger Rechenaufwand zu einem anderen Schluss gekommen.

#### 6. Typische Fehler

Lipton & Steinhardt (2018) beschreiben problematische Entwicklungen in Arbeiten zum maschinellen Lernen, darunter die fehlende Trennung von Erklärung und Spekulation und die fehlende Klärung, woher empirische Verbesserungen stammen, etwa wenn Verbesserungen Architekturänderungen zugeschrieben werden, obwohl sie tatsächlich aus dem Hyperparameter-Tuning stammen. Ungleicher Tuning-Aufwand zwischen einem neuen Modell und seinen Baselines ist daher eine häufige Quelle irreführender Vergleiche.

#### Ursprung und Varianten

Dietterich (1998) und Demšar (2006) etablierten statistische Tests zum Vergleich von Lernverfahren. Lipton & Steinhardt (2018), Dodge et al. (2019) und Bouthillier et al. (2021) befassten sich mit Berichtspraxis und Varianz in Benchmarks, und HELM (Liang et al., 2022) erweiterte Vergleiche von Sprachmodellen auf viele Metriken und Szenarien.

### Wann einsetzen

- Wenn behauptet wird, ein neues Modell sei besser als eine Baseline, sollte sein Vorsprung statistisch geprüft werden (Dietterich, 1998).
- Wenn mehrere Modelle über viele Datensätze verglichen werden, eignen sich rangbasierte Tests (Demšar, 2006).
- Bei der Wahl eines Modells für den Produktivbetrieb sollten mehrere Kriterien wie Kalibrierung, Robustheit und Effizienz verglichen werden (Liang et al., 2022).

### Stärken und Grenzen

**Stärken**
- Geeignete Tests halten falsche Verbesserungsbehauptungen unter Kontrolle (Dietterich, 1998).
- Nichtparametrische Tests über viele Datensätze kommen mit wenigen Annahmen aus (Demšar, 2006).
- Wer den Aufwand berichtet, macht Ergebnisse reproduzierbar und vergleichbar (Dodge et al., 2019).

**Einschränkungen**
- Wiederholtes Training zur Schätzung der Varianz ist teuer (Bouthillier et al., 2021).
- Einige verbreitete Tests haben einen hohen Fehler erster Art (Dietterich, 1998).
- Verbesserungen werden oft der falschen Ursache zugeschrieben (Lipton & Steinhardt, 2018).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| McNemar-Test / 5×2 cv | Kontrollierter Fehler erster Art auf einem Datensatz (Dietterich, 1998) | Zwei Verfahren, eine Aufgabe |
| Wilcoxon- / Friedman-Test | Rangbasierte Tests über viele Datensätze (Demšar, 2006) | Benchmarks mit mehreren Datensätzen |
| Randomisieren der Varianzquellen | Variiert Daten, Initialisierung und Hyperparameter über die Läufe (Bouthillier et al., 2021) | Deep-Learning-Benchmarks |
| Erwartete Validierungsleistung | Leistung als Funktion des Rechenbudgets (Dodge et al., 2019) | Modelle mit unterschiedlichem Tuning-Aufwand |
| Ganzheitliche Evaluation | Viele Metriken über viele Szenarien (Liang et al., 2022) | Sprachmodelle |

### In der Praxis

Alle Modelle erhalten dieselben Datenaufteilungen und vergleichbare Tuning-Budgets, und das Budget wird berichtet (Dodge et al., 2019). Ergebnisse werden als Mittelwerte mit Streuung über mehrere Läufe angegeben, und Unterschiede werden getestet (Bouthillier et al., 2021; Dietterich, 1998). Für Prompt- und LLM-Vergleiche gelten dieselben Grundsätze ([[prompt-comparison|Prompt-Vergleiche]]).

### Merksatz

Ein Modell ist erst dann nachweislich besser, wenn der Unterschied die Varianz von Training und Daten übersteht, mit einem geeigneten Test geprüft wurde und für alle Modelle mit vergleichbarem Aufwand zustande kam.

### Quellen

- Dietterich, T. G. (1998). *Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms.* Neural Computation 10(7). [doi:10.1162/089976698300017197](https://doi.org/10.1162/089976698300017197)
- Demšar, J. (2006). *Statistical Comparisons of Classifiers over Multiple Data Sets.* JMLR 7. [JMLR](https://jmlr.org/papers/v7/demsar06a.html)
- Bouthillier, X. et al. (2021). *Accounting for Variance in Machine Learning Benchmarks.* MLSys 2021. [arXiv:2103.03098](https://arxiv.org/abs/2103.03098)
- Dodge, J. et al. (2019). *Show Your Work: Improved Reporting of Experimental Results.* EMNLP 2019. [arXiv:1909.03004](https://arxiv.org/abs/1909.03004)
- Lipton, Z. C. & Steinhardt, J. (2018). *Troubling Trends in Machine Learning Scholarship.* [arXiv:1807.03341](https://arxiv.org/abs/1807.03341)
- Liang, P. et al. (2022). *Holistic Evaluation of Language Models.* TMLR. [arXiv:2211.09110](https://arxiv.org/abs/2211.09110)
