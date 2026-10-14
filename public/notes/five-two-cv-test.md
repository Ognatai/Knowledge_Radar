---
title_en: 5×2cv Paired t-Test
title_de: 5×2cv-gepaarter t-Test
entity_type: Method
aliases:
- 5×2 cv test
- 5x2cv paired t-test
- 5x2cv test
- 5×2-cv-Test
- Combined 5x2cv F-test
sources:
- https://arxiv.org/abs/1811.12808
- https://doi.org/10.1162/089976698300017197
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

The 5×2cv paired t-test compares two learning algorithms on one dataset: the data is split in half five times, both algorithms are trained on one half and tested on the other and then the halves are swapped, and a t statistic built from the ten performance differences is compared with a t distribution with 5 degrees of freedom (Raschka, 2018). Thomas Dietterich proposed it in 1998 to fix the inflated false positive rates of the resampled paired t-test and the k-fold cross-validated paired t-test, whose overlapping training and test sets violate the independence assumptions of Student's t-test (Raschka, 2018). In Dietterich's simulations it had a low false positive rate, similar to McNemar's test, and was slightly more powerful, at about ten times the computation (Raschka, 2018). Alpaydin's combined 5×2cv F-test (1999) is a more robust variant.

### How it works

```text
repeat i = 1..5:
    shuffle, split data S into halves A and B (50 % / 50 %)
    train C1, C2 on A, test on B  → difference d_i,A = acc(C1) − acc(C2)
    train C1, C2 on B, test on A  → difference d_i,B
    mean_i = (d_i,A + d_i,B) / 2 ;  s_i² = (d_i,A − mean_i)² + (d_i,B − mean_i)²
t = d_1,A / sqrt( (1/5) Σ s_i² )        ~ t distribution with 5 degrees of freedom under H0
p < α  →  reject "both algorithms perform equally"
```

#### 1. Algorithm comparison, not model comparison

Tests such as McNemar's test compare two fitted models on one test set and ignore how much the result depends on the particular training set (Raschka, 2018). When the question is which learning algorithm works better for a kind of problem, the variance across training sets matters, so the algorithms have to be refitted on different training sets; this is the setting the 5×2cv test addresses (Raschka, 2018).

#### 2. Five times twofold cross-validation

In each of five iterations, the data is split into two halves of equal size; both classifiers are fitted on the first half and evaluated on the second, then training and test halves are swapped, which gives two performance differences per iteration (Raschka, 2018). With twofold splitting, the two training sets of an iteration do not overlap, whereas in k-fold [[cross-validation|cross-validation]] with larger k they share most of their examples (Raschka, 2018).

#### 3. The t statistic

For each iteration, the mean and the variance s_i² of the two differences are computed; the t statistic divides the difference from the first fold of the first iteration by the square root of the average of the five variances and approximately follows a t distribution with 5 degrees of freedom under the null hypothesis of equal performance (Raschka, 2018). If the p-value is below the chosen significance level, such as 0.05, the null hypothesis is rejected (Raschka, 2018).

#### Origin and variants

Dietterich (1998) compared approximate statistical tests for supervised [[classification|classification]] learning algorithms on simulated datasets: the difference-of-proportions test and the resampled paired t-test had high false positive rates, the k-fold cross-validated t-test a somewhat elevated one, while McNemar's test and the new 5×2cv test had low false positive rates (Raschka, 2018). Alpaydin (1999) proposed the combined 5×2cv F-test, which uses all ten differences and is approximately F-distributed with 10 and 5 degrees of freedom, as a more robust alternative (Raschka, 2018). The 5×2 setting of nested cross-validation (five outer folds, two inner folds) is a different procedure and is often confused with Dietterich's method (Raschka, 2018).

### When to use it

- Comparing two learning algorithms on one dataset when they can be refitted ten times (Raschka, 2018).
- Small or medium datasets where a single test split would be too noisy ([[model-comparison|model comparison]]).
- Not for comparisons over many datasets, which use other procedures ([[statistics-fundamentals|statistics fundamentals]]).

### Strengths and limitations

**Strengths**
- Low false positive rate, similar to McNemar's test, and slightly more power (Raschka, 2018).
- Takes the variation caused by different training sets into account (Raschka, 2018).
- Implementations exist, for example in MLxtend (Raschka, 2018).

**Limitations**
- About ten times the computation of McNemar's test (Raschka, 2018).
- Each model is trained on only half the data, so its accuracy can be lower than with the full dataset.
- Parametric tests for comparing models usually violate some independence assumption, so the result is a heuristic aid for decisions rather than proof (Raschka, 2018).
- A significant p-value says nothing about effect size; large samples can make small differences significant (Raschka, 2018).

### Comparison

| Test | False positives in Dietterich's study | Cost |
|---|---|---|
| Difference of proportions | high | cheap |
| Resampled paired t-test | high | very expensive |
| k-fold cross-validated paired t-test | somewhat elevated | k fits |
| McNemar's test | low | one fit |
| 5×2cv paired t-test | low | ten fits |

Source: Raschka (2018), summarising Dietterich (1998).

### In practice

MLxtend provides `paired_ttest_5x2cv` and `combined_ftest_5x2cv` (Raschka, 2018). Raschka recommends McNemar's test for large datasets or when models can be fitted only once, and the combined 5×2cv F-test or nested cross-validation for algorithm comparison on small datasets (Raschka, 2018). Report effect sizes and the variation across splits along with the p-value ([[model-comparison|model comparison]]).

### Key takeaway

The 5×2cv test compares two learning algorithms through five rounds of twofold cross-validation and a t statistic with 5 degrees of freedom; it keeps false positives low where naive cross-validated t-tests do not.

### Sources

- Raschka, S. (2018). Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning, sections 4.8–4.14. [arXiv:1811.12808](https://arxiv.org/abs/1811.12808)
- Dietterich, T. G. (1998). Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms. *Neural Computation*, 10(7). [doi:10.1162/089976698300017197](https://doi.org/10.1162/089976698300017197)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Der 5×2cv-gepaarte t-Test vergleicht zwei Lernverfahren auf einem Datensatz: Die Daten werden fünfmal halbiert, beide Verfahren werden auf einer Hälfte trainiert und auf der anderen getestet, dann werden die Hälften getauscht, und eine aus den zehn Leistungsunterschieden gebildete t-Statistik wird mit einer t-Verteilung mit 5 Freiheitsgraden verglichen (Raschka, 2018). Thomas Dietterich schlug ihn 1998 vor, um die überhöhten Falsch-positiv-Raten des Resampled Paired t-Test und des k-fach kreuzvalidierten gepaarten t-Tests zu beheben, deren überlappende Trainings- und Testmengen die Unabhängigkeitsannahmen des Student-t-Tests verletzen (Raschka, 2018). In Dietterichs Simulationen hatte er eine niedrige Falsch-positiv-Rate, ähnlich wie der McNemar-Test, und war etwas trennschärfer, bei etwa zehnfachem Rechenaufwand (Raschka, 2018). Alpaydins kombinierter 5×2cv-F-Test (1999) ist eine robustere Variante.

### Funktionsweise

```text
wiederhole i = 1..5:
    mischen, Daten S in Hälften A und B teilen (50 % / 50 %)
    C1, C2 auf A trainieren, auf B testen  → Differenz d_i,A = acc(C1) − acc(C2)
    C1, C2 auf B trainieren, auf A testen  → Differenz d_i,B
    mean_i = (d_i,A + d_i,B) / 2 ;  s_i² = (d_i,A − mean_i)² + (d_i,B − mean_i)²
t = d_1,A / sqrt( (1/5) Σ s_i² )        ~ t-Verteilung mit 5 Freiheitsgraden unter H0
p < α  →  „beide Verfahren sind gleich gut“ verwerfen
```

#### 1. Vergleich von Lernverfahren, nicht von Modellen

Tests wie der McNemar-Test vergleichen zwei trainierte Modelle auf einer Testmenge und lassen außer Acht, wie stark das Ergebnis von der konkreten Trainingsmenge abhängt (Raschka, 2018). Lautet die Frage, welches Lernverfahren für eine Art von Problem besser funktioniert, zählt die Varianz über Trainingsmengen hinweg, daher müssen die Verfahren auf verschiedenen Trainingsmengen neu angepasst werden; das ist die Situation, für die der 5×2cv-Test gedacht ist (Raschka, 2018).

#### 2. Fünfmal zweifache Kreuzvalidierung

In jeder von fünf Iterationen werden die Daten in zwei gleich große Hälften geteilt; beide Klassifikatoren werden auf der ersten Hälfte angepasst und auf der zweiten bewertet, dann werden Trainings- und Testhälfte getauscht, was zwei Leistungsunterschiede je Iteration ergibt (Raschka, 2018). Bei der Zweiteilung überschneiden sich die beiden Trainingsmengen einer Iteration nicht, während sie bei k-facher [[cross-validation|Kreuzvalidierung]] mit größerem k den Großteil ihrer Beispiele teilen (Raschka, 2018).

#### 3. Die t-Statistik

Für jede Iteration werden Mittelwert und Varianz s_i² der beiden Differenzen berechnet; die t-Statistik teilt die Differenz aus dem ersten Fold der ersten Iteration durch die Wurzel aus dem Mittel der fünf Varianzen und folgt unter der Nullhypothese gleicher Leistung näherungsweise einer t-Verteilung mit 5 Freiheitsgraden (Raschka, 2018). Liegt der p-Wert unter dem gewählten Signifikanzniveau, etwa 0,05, wird die Nullhypothese verworfen (Raschka, 2018).

#### Herkunft und Varianten

Dietterich (1998) verglich näherungsweise statistische Tests für überwachte Klassifikationsverfahren auf simulierten Datensätzen: Der Test auf Differenz von Anteilen und der Resampled Paired t-Test hatten hohe Falsch-positiv-Raten, der k-fach kreuzvalidierte t-Test eine etwas erhöhte, während der McNemar-Test und der neue 5×2cv-Test niedrige Falsch-positiv-Raten hatten (Raschka, 2018). Alpaydin (1999) schlug den kombinierten 5×2cv-F-Test vor, der alle zehn Differenzen nutzt und näherungsweise F-verteilt mit 10 und 5 Freiheitsgraden ist, als robustere Alternative (Raschka, 2018). Die 5×2-Konfiguration der verschachtelten Kreuzvalidierung (fünf äußere, zwei innere Folds) ist ein anderes Verfahren und wird oft mit Dietterichs Methode verwechselt (Raschka, 2018).

### Wann einsetzen

- Vergleich zweier Lernverfahren auf einem Datensatz, wenn sie zehnmal neu angepasst werden können (Raschka, 2018).
- Kleine oder mittlere Datensätze, bei denen eine einzelne Testaufteilung zu verrauscht wäre ([[model-comparison|Modellvergleich]]).
- Nicht für Vergleiche über viele Datensätze, für die andere Verfahren genutzt werden ([[statistics-fundamentals|Statistik-Grundlagen]]).

### Stärken und Grenzen

**Stärken**
- Niedrige Falsch-positiv-Rate, ähnlich wie beim McNemar-Test, und etwas mehr Trennschärfe (Raschka, 2018).
- Berücksichtigt die Schwankung durch unterschiedliche Trainingsmengen (Raschka, 2018).
- Implementierungen gibt es, etwa in MLxtend (Raschka, 2018).

**Grenzen**
- Etwa zehnfacher Rechenaufwand gegenüber dem McNemar-Test (Raschka, 2018).
- Jedes Modell wird nur auf der Hälfte der Daten trainiert, seine Accuracy kann daher niedriger sein als mit dem vollständigen Datensatz.
- Parametrische Tests für Modellvergleiche verletzen meist eine Unabhängigkeitsannahme; das Ergebnis ist daher eher eine heuristische Entscheidungshilfe als ein Beweis (Raschka, 2018).
- Ein signifikanter p-Wert sagt nichts über die Effektstärke; große Stichproben können kleine Unterschiede signifikant machen (Raschka, 2018).

### Vergleich

| Test | Falsch-positive in Dietterichs Studie | Aufwand |
|---|---|---|
| Differenz von Anteilen | hoch | gering |
| Resampled Paired t-Test | hoch | sehr hoch |
| k-fach kreuzvalidierter gepaarter t-Test | etwas erhöht | k Anpassungen |
| McNemar-Test | niedrig | eine Anpassung |
| 5×2cv-gepaarter t-Test | niedrig | zehn Anpassungen |

Quelle: Raschka (2018), als Zusammenfassung von Dietterich (1998).

### In der Praxis

MLxtend stellt `paired_ttest_5x2cv` und `combined_ftest_5x2cv` bereit (Raschka, 2018). Raschka empfiehlt den McNemar-Test für große Datensätze oder wenn Modelle nur einmal angepasst werden können, und den kombinierten 5×2cv-F-Test oder verschachtelte Kreuzvalidierung für den Vergleich von Lernverfahren auf kleinen Datensätzen (Raschka, 2018). Neben dem p-Wert gehören Effektstärken und die Schwankung über die Aufteilungen in den Bericht ([[model-comparison|Modellvergleich]]).

### Merksatz

Der 5×2cv-Test vergleicht zwei Lernverfahren über fünf Runden zweifacher Kreuzvalidierung und eine t-Statistik mit 5 Freiheitsgraden; er hält Falsch-positive niedrig, wo naive kreuzvalidierte t-Tests das nicht tun.

### Quellen

- Raschka, S. (2018). Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning, Abschnitte 4.8–4.14. [arXiv:1811.12808](https://arxiv.org/abs/1811.12808)
- Dietterich, T. G. (1998). Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms. *Neural Computation*, 10(7). [doi:10.1162/089976698300017197](https://doi.org/10.1162/089976698300017197)
