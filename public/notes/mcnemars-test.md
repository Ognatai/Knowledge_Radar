---
title_en: McNemar's Test
title_de: McNemar-Test
entity_type: Method
aliases:
- McNemar's test
- McNemar test
- Within-subjects chi-squared test
sources:
- https://arxiv.org/abs/1811.12808
- https://rasbt.github.io/mlxtend/user_guide/evaluate/mcnemar/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

McNemar's test, introduced by Quinn McNemar in 1947, is a non-parametric test for paired nominal data; in machine learning it compares two classifiers on the same test set by looking only at the examples on which they disagree (Raschka, 2018). From a 2×2 table of "model 1 correct or wrong" against "model 2 correct or wrong", it uses the two off-diagonal counts B and C and tests the null hypothesis that both kinds of disagreement are equally likely, with χ² = (B − C)² / (B + C) or Edwards' continuity-corrected version (Raschka, 2018). Dietterich (1998) found it preferable to the difference-of-proportions test, and Raschka recommends it for comparing models on large datasets; it does not account for variation across training sets, which the [[five-two-cv-test|5×2cv test]] addresses (Raschka, 2018).

### How it works

```text
                     model 2 correct   model 2 wrong
model 1 correct            A                 B
model 1 wrong              C                 D
H0: p(B) = p(C)  (neither model is better)
χ² = (|B − C| − 1)² / (B + C)   (Edwards' correction; without "−1": original)
→ χ² distribution with 1 degree of freedom → p-value
small B + C: exact binomial test with p = 0.5
```

#### 1. The 2×2 contingency table

Unlike a usual confusion matrix of one model, the table compares the predictions of two models on the same n test examples: A counts examples both get right, D examples both get wrong, B examples only model 1 gets right and C examples only model 2 gets right (Raschka, 2018). Accuracy of model 1 is (A + B)/n and of model 2 (A + C)/n, but only B and C show how the models differ (Raschka, 2018).

#### 2. The test statistic

The null hypothesis is that p(B) and p(C) are equal, so that neither model performs better; the statistic χ² = (B − C)² / (B + C) approximately follows a χ² distribution with one degree of freedom when B and C are reasonably large (Raschka, 2018). In Raschka's example, two models with nearly the same accuracy on 10,000 test examples disagree 11 to 1 in one scenario (χ² ≈ 8.3, p = 0.0039, significant at α = 0.05) and 25 to 15 in another (χ² = 2.5, p = 0.1138, not significant) (Raschka, 2018).

#### 3. Continuity correction and exact test

About a year after McNemar, Allen L. Edwards proposed subtracting 1 from |B − C| before squaring, the variant more commonly used today (Raschka, 2018). If B and C are small, the χ² approximation is poor, and an exact binomial test with proportion 0.5 over the n = B + C disagreements gives the p-value; for B and C above about 50, the corrected test and the exact test give almost identical p-values (Raschka, 2018).

#### 4. More than two models

Running pairwise tests on many models raises the problem of multiple hypothesis testing; a common approach is an omnibus test such as Cochran's Q, a generalisation of McNemar's test to three or more models, followed by pairwise McNemar tests with a correction for multiple comparisons (Raschka, 2018).

#### Origin and variants

Quinn McNemar published the test in 1947, Edwards the continuity correction in 1948 (Raschka, 2018). Dietterich (1998) found it preferable to the difference-of-proportions test for comparing classifiers (Raschka, 2018). MLxtend implements it as `mcnemar(ary, corrected=True, exact=False)`, so the continuity correction is the default and the exact test is an option (Raschka, n.d.).

### When to use it

- Comparing two trained classifiers on the same, large test set, for example a new model against the production model (Raschka, 2018).
- When models are too expensive to train more than once (Raschka, 2018).
- Not for comparing learning algorithms in general: it ignores how results vary with the training set, so use the [[five-two-cv-test|5×2cv test]] or nested [[cross-validation|cross-validation]] for that on small datasets (Raschka, 2018).

### Strengths and limitations

**Strengths**
- Needs only one fit per model and one test set (Raschka, 2018).
- Uses the pairing of predictions on the same examples, which the difference-of-proportions test ignores (Raschka, 2018).
- Low false positive rate in Dietterich's simulations (Raschka, 2018).

**Limitations**
- Tests a difference between two fitted models, not between algorithms; training-set variance is not taken into account (Raschka, 2018).
- The χ² approximation is unreliable when B and C are small; then the exact binomial test is needed (Raschka, 2018).
- Only uses correct versus wrong, so it says nothing about calibration or the size of the effect ([[classification-metrics|classification metrics]]).

### Comparison

| Test | Compares | Fits per model | Typical use |
|---|---|---|---|
| McNemar's test | two models on one test set | 1 | large datasets, model comparison |
| Cochran's Q + McNemar | three or more models on one test set | 1 | large datasets, several models |
| Combined 5×2cv F-test | two learning algorithms | 10 | small datasets, algorithm comparison |

Source: Raschka (2018).

### In practice

Collect the predictions of both models on the same held-out test set, count B and C, and use the exact binomial version when the disagreement counts are small: for the 11-to-1 scenario, with B + C = 12 below the recommended 25, the MLxtend guide computes an exact p-value of about 0.0059 (Raschka, 2018; Raschka, n.d.). Report the counts and the accuracies alongside the p-value, and correct for multiple comparisons when testing many models ([[model-comparison|model comparison]]).

### Key takeaway

McNemar's test asks whether two classifiers' disagreements on the same test set are lopsided enough to be more than chance; it is cheap and robust for model comparison, but it does not compare learning algorithms across training sets.

### Sources

- Raschka, S. (2018). Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning, sections 4.2–4.6 and 4.15. [arXiv:1811.12808](https://arxiv.org/abs/1811.12808)
- Raschka, S. (n.d.). *mcnemar: McNemar's test for classifier comparisons*. MLxtend User Guide. [rasbt.github.io](https://rasbt.github.io/mlxtend/user_guide/evaluate/mcnemar/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Der McNemar-Test, 1947 von Quinn McNemar eingeführt, ist ein nichtparametrischer Test für gepaarte nominale Daten; im maschinellen Lernen vergleicht er zwei Klassifikatoren auf derselben Testmenge, indem er nur die Beispiele betrachtet, bei denen sie sich unterscheiden (Raschka, 2018). Aus einer 2×2-Tabelle „Modell 1 richtig oder falsch“ gegen „Modell 2 richtig oder falsch“ nutzt er die beiden Werte B und C außerhalb der Diagonale und prüft die Nullhypothese, dass beide Arten von Abweichung gleich wahrscheinlich sind, mit χ² = (B − C)² / (B + C) oder der Fassung mit Stetigkeitskorrektur nach Edwards (Raschka, 2018). Dietterich (1998) zog ihn dem Test auf Differenz von Anteilen vor, und Raschka empfiehlt ihn für den Vergleich von Modellen auf großen Datensätzen; Schwankungen über verschiedene Trainingsmengen berücksichtigt er nicht, dafür ist der [[five-two-cv-test|5×2cv-Test]] gedacht (Raschka, 2018).

### Funktionsweise

```text
                     Modell 2 richtig   Modell 2 falsch
Modell 1 richtig           A                  B
Modell 1 falsch            C                  D
H0: p(B) = p(C)  (keines der Modelle ist besser)
χ² = (|B − C| − 1)² / (B + C)   (Korrektur nach Edwards; ohne „−1“: Original)
→ χ²-Verteilung mit 1 Freiheitsgrad → p-Wert
kleines B + C: exakter Binomialtest mit p = 0,5
```

#### 1. Die 2×2-Kontingenztafel

Anders als die übliche Konfusionsmatrix eines Modells vergleicht die Tabelle die Vorhersagen zweier Modelle auf denselben n Testbeispielen: A zählt Beispiele, die beide richtig vorhersagen, D Beispiele, die beide falsch vorhersagen, B Beispiele, die nur Modell 1 richtig hat, und C Beispiele, die nur Modell 2 richtig hat (Raschka, 2018). Die Accuracy von Modell 1 ist (A + B)/n, die von Modell 2 (A + C)/n, aber nur B und C zeigen, worin sich die Modelle unterscheiden (Raschka, 2018).

#### 2. Die Teststatistik

Die Nullhypothese lautet, dass p(B) und p(C) gleich sind, also keines der Modelle besser abschneidet; die Statistik χ² = (B − C)² / (B + C) folgt näherungsweise einer χ²-Verteilung mit einem Freiheitsgrad, wenn B und C hinreichend groß sind (Raschka, 2018). In Raschkas Beispiel unterscheiden sich zwei Modelle mit fast gleicher Accuracy auf 10 000 Testbeispielen in einem Szenario im Verhältnis 11 zu 1 (χ² ≈ 8,3, p = 0,0039, signifikant bei α = 0,05) und in einem anderen im Verhältnis 25 zu 15 (χ² = 2,5, p = 0,1138, nicht signifikant) (Raschka, 2018).

#### 3. Stetigkeitskorrektur und exakter Test

Etwa ein Jahr nach McNemar schlug Allen L. Edwards vor, vor dem Quadrieren 1 von |B − C| abzuziehen; diese Variante ist heute gebräuchlicher (Raschka, 2018). Sind B und C klein, ist die χ²-Näherung schlecht, und ein exakter Binomialtest mit Anteil 0,5 über die n = B + C Abweichungen liefert den p-Wert; für B und C über etwa 50 ergeben korrigierter und exakter Test fast identische p-Werte (Raschka, 2018).

#### 4. Mehr als zwei Modelle

Paarweise Tests über viele Modelle führen zum Problem multipler Hypothesentests; ein üblicher Ansatz ist ein Omnibus-Test wie Cochrans Q, eine Verallgemeinerung des McNemar-Tests auf drei oder mehr Modelle, gefolgt von paarweisen McNemar-Tests mit Korrektur für Mehrfachvergleiche (Raschka, 2018).

#### Herkunft und Varianten

Quinn McNemar veröffentlichte den Test 1947, Edwards die Stetigkeitskorrektur 1948 (Raschka, 2018). Dietterich (1998) zog ihn für den Vergleich von Klassifikatoren dem Test auf Differenz von Anteilen vor (Raschka, 2018). MLxtend stellt ihn als `mcnemar(ary, corrected=True, exact=False)` bereit; die Stetigkeitskorrektur ist also voreingestellt, der exakte Test eine Option (Raschka, n.d.).

### Wann einsetzen

- Zum Vergleich zweier trainierter Klassifikatoren auf derselben großen Testmenge, etwa eines neuen Modells mit dem Produktivmodell (Raschka, 2018).
- Wenn Modelle zu teuer sind, um sie mehr als einmal zu trainieren (Raschka, 2018).
- Nicht für den allgemeinen Vergleich von Lernverfahren: Er lässt außer Acht, wie Ergebnisse mit der Trainingsmenge schwanken; dafür eignen sich bei kleinen Datensätzen der [[five-two-cv-test|5×2cv-Test]] oder verschachtelte [[cross-validation|Kreuzvalidierung]] (Raschka, 2018).

### Stärken und Grenzen

**Stärken**
- Braucht nur ein Training je Modell und eine Testmenge (Raschka, 2018).
- Nutzt die Paarung der Vorhersagen auf denselben Beispielen, die der Test auf Differenz von Anteilen außer Acht lässt (Raschka, 2018).
- Niedrige Rate falsch positiver Ergebnisse in Dietterichs Simulationen (Raschka, 2018).

**Grenzen**
- Prüft einen Unterschied zwischen zwei trainierten Modellen, nicht zwischen Lernverfahren; die Varianz über Trainingsmengen bleibt unberücksichtigt (Raschka, 2018).
- Die χ²-Näherung ist unzuverlässig, wenn B und C klein sind; dann ist der exakte Binomialtest nötig (Raschka, 2018).
- Nutzt nur richtig gegen falsch und sagt daher nichts über Kalibrierung oder die Größe des Effekts ([[classification-metrics|Klassifikationsmetriken]]).

### Vergleich

| Test | Vergleicht | Trainings je Modell | Typische Verwendung |
|---|---|---|---|
| McNemar-Test | zwei Modelle auf einer Testmenge | 1 | große Datensätze, Modellvergleich |
| Cochrans Q + McNemar | drei oder mehr Modelle auf einer Testmenge | 1 | große Datensätze, mehrere Modelle |
| Kombinierter 5×2cv-F-Test | zwei Lernverfahren | 10 | kleine Datensätze, Vergleich von Lernverfahren |

Quelle: Raschka (2018).

### In der Praxis

Die Vorhersagen beider Modelle auf derselben zurückgehaltenen Testmenge werden gesammelt, B und C gezählt, und bei kleinen Abweichungszahlen wird die exakte Binomialfassung genutzt: Für das Szenario 11 zu 1, mit B + C = 12 unter den empfohlenen 25, berechnet die MLxtend-Anleitung einen exakten p-Wert von etwa 0,0059 (Raschka, 2018; Raschka, n.d.). Neben dem p-Wert werden die Zählwerte und die Accuracy-Werte berichtet, und beim Testen vieler Modelle wird für Mehrfachvergleiche korrigiert ([[model-comparison|Modellvergleich]]).

### Merksatz

Der McNemar-Test fragt, ob die Abweichungen zweier Klassifikatoren auf derselben Testmenge so einseitig sind, dass sie mehr als Zufall sind; er ist günstig und robust für den Modellvergleich, vergleicht aber keine Lernverfahren über Trainingsmengen hinweg.

### Quellen

- Raschka, S. (2018). Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning, Abschnitte 4.2–4.6 und 4.15. [arXiv:1811.12808](https://arxiv.org/abs/1811.12808)
- Raschka, S. (n.d.). *mcnemar: McNemar's test for classifier comparisons*. MLxtend User Guide. [rasbt.github.io](https://rasbt.github.io/mlxtend/user_guide/evaluate/mcnemar/)
