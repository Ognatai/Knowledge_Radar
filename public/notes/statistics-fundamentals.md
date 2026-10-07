---
title_en: Statistics Fundamentals
title_de: Statistik-Grundlagen
entity_type: Concept
sources:
- https://doi.org/10.1007/s10654-016-0149-3
- https://doi.org/10.1080/00031305.2016.1154108
- https://doi.org/10.1214/aos/1176344552
- https://doi.org/10.1007/s10618-008-0114-1
- https://doi.org/10.1162/089976698300017197
- https://sites.stat.columbia.edu/gelman/book/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Statistical fundamentals for machine learning are about quantifying uncertainty. A metric measured on a sample is only an estimate; the bootstrap (Efron, 1979) and confidence intervals describe its uncertainty, hypothesis tests and A/B tests decide whether differences are real (Kohavi et al., 2009), and comparing learning algorithms needs tests with controlled error rates (Dietterich, 1998). p-values and confidence intervals are widely misinterpreted (Greenland et al., 2016; Wasserstein & Lazar, 2016).

### How it works

An evaluation result is treated as an estimate from a sample, not as an exact value. Its uncertainty is quantified, differences between models or variants are tested with suitable methods, and results are reported with their uncertainty rather than as a single number.

```text
1. Estimates and the bootstrap
▼
2. Confidence intervals and p-values
▼
3. A/B tests
▼
4. Comparing learning algorithms
▼
5. Bayesian and frequentist views
```

#### 1. Estimates and the bootstrap

A statistic computed from a sample, such as a model's accuracy on a test set, estimates an unknown quantity and would differ on another sample. The bootstrap estimates the sampling distribution of such a statistic from the observed data by resampling it, and works on a variety of estimation problems, for example the error rate of a linear discriminant analysis (Efron, 1979).

#### 2. Confidence intervals and p-values

Greenland et al. (2016) give correct definitions of tests, p-values, confidence intervals and power and list common misinterpretations, such as reading a p-value as the probability that the null hypothesis is true, or a 95% confidence interval as having a 95% chance of containing the true value. The American Statistical Association states six principles: p-values can indicate how incompatible data are with a model; they do not measure the probability that a hypothesis is true; decisions should not rest only on whether a p-value passes a threshold; proper inference requires full reporting and transparency; a p-value does not measure the size or importance of an effect; and by itself it is not a good measure of evidence (Wasserstein & Lazar, 2016).

#### 3. A/B tests

Online controlled experiments, or A/B tests, randomly assign users to a control and a treatment variant; they are the best scientific design for establishing a causal effect of a change on user behaviour (Kohavi et al., 2009). Their practical guide covers statistical power, sample size and techniques for variance reduction, and discusses their limitations.

#### 4. Comparing learning algorithms

Dietterich (1998) compared five tests for whether one learning algorithm outperforms another. A test for the difference of two proportions and a paired t test over several random train-test splits had a high probability of detecting differences that do not exist (type I error) and should not be used; a paired t test based on 10-fold cross-validation had a somewhat elevated type I error. McNemar's test and the new 5×2 cv test, based on five repetitions of twofold cross-validation, had acceptable type I error ([[model-comparison|Model Comparison]]).

#### 5. Bayesian and frequentist views

In Bayesian inference, unknown quantities are treated as random: a prior distribution is combined with the likelihood of the data via Bayes' rule into a posterior distribution, and uncertainty is summarised with posterior intervals (Gelman et al., 2013). This contrasts with frequentist tests and confidence intervals, which describe how a procedure behaves over repeated samples.

#### Origin and variants

The bootstrap (Efron, 1979), tests for comparing classifiers (Dietterich, 1998), the practical guide to online experiments (Kohavi et al., 2009) and Bayesian data analysis (Gelman et al., 2013) are core references; Greenland et al. (2016) and Wasserstein & Lazar (2016) address misinterpretations of p-values and confidence intervals.

### When to use it

- When model metrics are reported, they should come with an estimate of uncertainty, for example from the bootstrap (Efron, 1979).
- When a product change is evaluated with real users, a randomised A/B test is the method of choice (Kohavi et al., 2009).
- When two learning algorithms are compared on one dataset, tests with controlled type I error such as McNemar's test or 5×2 cv should be used (Dietterich, 1998).

### Strengths and limitations

**Strengths**
- The bootstrap estimates uncertainty without strong assumptions (Efron, 1979).
- Randomised experiments establish causal effects (Kohavi et al., 2009).
- Suitable tests keep the rate of false discoveries under control (Dietterich, 1998).

**Limitations**
- p-values and confidence intervals are widely misinterpreted (Greenland et al., 2016).
- A p-value says nothing about the size or importance of an effect (Wasserstein & Lazar, 2016).
- Some widely used tests for comparing algorithms have a high type I error (Dietterich, 1998).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Bootstrap | Resampling the observed data (Efron, 1979) | Uncertainty of any statistic |
| Frequentist tests and confidence intervals | Behaviour of a procedure over repeated samples (Greenland et al., 2016) | Decisions with controlled error rates |
| Bayesian inference | Posterior distribution from prior and data (Gelman et al., 2013) | Incorporating prior knowledge, direct probability statements |
| A/B test | Randomised assignment of users (Kohavi et al., 2009) | Causal effects of product changes |

### In practice

Evaluation results are reported with intervals and effect sizes, not only with p-values (Wasserstein & Lazar, 2016). Analyses are not chosen after looking at which one gives a significant result, because this distorts p-values (Greenland et al., 2016). For LLM-based systems, the same principles apply when prompt or model variants are compared ([[prompt-comparison|Prompt Comparison]]).

### Key takeaway

Every evaluation result is an estimate with uncertainty; quantify it, use tests with controlled error rates, and do not mistake a p-value for the probability that a hypothesis is true.

### Sources

- Greenland, S., Senn, S. J., Rothman, K. J., Carlin, J. B., Poole, C., Goodman, S. N. & Altman, D. G. (2016). *Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations.* European Journal of Epidemiology 31(4). [doi:10.1007/s10654-016-0149-3](https://doi.org/10.1007/s10654-016-0149-3)
- Wasserstein, R. L. & Lazar, N. A. (2016). *The ASA Statement on p-Values: Context, Process, and Purpose.* The American Statistician 70(2). [doi:10.1080/00031305.2016.1154108](https://doi.org/10.1080/00031305.2016.1154108)
- Efron, B. (1979). *Bootstrap Methods: Another Look at the Jackknife.* The Annals of Statistics 7(1). [doi:10.1214/aos/1176344552](https://doi.org/10.1214/aos/1176344552)
- Kohavi, R., Longbotham, R., Sommerfield, D. & Henne, R. M. (2009). *Controlled experiments on the web: survey and practical guide.* Data Mining and Knowledge Discovery 18(1). [doi:10.1007/s10618-008-0114-1](https://doi.org/10.1007/s10618-008-0114-1)
- Dietterich, T. G. (1998). *Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms.* Neural Computation 10(7). [doi:10.1162/089976698300017197](https://doi.org/10.1162/089976698300017197)
- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A. & Rubin, D. B. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press. [book website](https://sites.stat.columbia.edu/gelman/book/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Statistische Grundlagen für maschinelles Lernen drehen sich um die Quantifizierung von Unsicherheit. Eine auf einer Stichprobe gemessene Metrik ist nur eine Schätzung; Bootstrap (Efron, 1979) und Konfidenzintervalle beschreiben ihre Unsicherheit, Hypothesentests und A/B-Tests entscheiden, ob Unterschiede echt sind (Kohavi et al., 2009), und der Vergleich von Lernverfahren braucht Tests mit kontrollierter Fehlerrate (Dietterich, 1998). p-Werte und Konfidenzintervalle werden häufig falsch interpretiert (Greenland et al., 2016; Wasserstein & Lazar, 2016).

### Funktionsweise

Ein Evaluationsergebnis wird als Schätzung aus einer Stichprobe behandelt, nicht als exakter Wert. Seine Unsicherheit wird quantifiziert, Unterschiede zwischen Modellen oder Varianten werden mit geeigneten Verfahren getestet, und Ergebnisse werden mit ihrer Unsicherheit berichtet statt als einzelne Zahl.

```text
1. Schätzungen und Bootstrap
▼
2. Konfidenzintervalle und p-Werte
▼
3. A/B-Tests
▼
4. Vergleich von Lernverfahren
▼
5. Bayes'sche und frequentistische Sicht
```

#### 1. Schätzungen und Bootstrap

Eine aus einer Stichprobe berechnete Statistik, etwa die Accuracy eines Modells auf einer Testmenge, schätzt eine unbekannte Größe und fiele auf einer anderen Stichprobe anders aus. Der Bootstrap schätzt die Stichprobenverteilung einer solchen Statistik aus den beobachteten Daten durch erneutes Ziehen mit Zurücklegen und funktioniert bei vielen Schätzproblemen, etwa für die Fehlerrate einer linearen Diskriminanzanalyse (Efron, 1979).

#### 2. Konfidenzintervalle und p-Werte

Greenland et al. (2016) geben korrekte Definitionen von Tests, p-Werten, Konfidenzintervallen und Teststärke und listen häufige Fehldeutungen auf, etwa einen p-Wert als Wahrscheinlichkeit zu lesen, dass die Nullhypothese wahr ist, oder einem 95-%-Konfidenzintervall eine 95-%-Wahrscheinlichkeit zuzuschreiben, den wahren Wert zu enthalten. Die American Statistical Association formuliert sechs Grundsätze: p-Werte können anzeigen, wie unvereinbar Daten mit einem Modell sind; sie messen nicht die Wahrscheinlichkeit, dass eine Hypothese wahr ist; Entscheidungen sollten nicht allein davon abhängen, ob ein p-Wert eine Schwelle unterschreitet; korrekte Inferenz erfordert vollständige Berichterstattung und Transparenz; ein p-Wert misst weder Größe noch Bedeutung eines Effekts; und für sich genommen ist er kein gutes Maß für Evidenz (Wasserstein & Lazar, 2016).

#### 3. A/B-Tests

Kontrollierte Online-Experimente, auch A/B-Tests, teilen Nutzende zufällig einer Kontroll- und einer Testvariante zu; sie sind das beste wissenschaftliche Design, um einen kausalen Effekt einer Änderung auf das Nutzungsverhalten nachzuweisen (Kohavi et al., 2009). Ihr Praxisleitfaden behandelt Teststärke, Stichprobengröße und Verfahren zur Varianzreduktion und diskutiert ihre Grenzen.

#### 4. Vergleich von Lernverfahren

Dietterich (1998) verglich fünf Tests dafür, ob ein Lernverfahren ein anderes übertrifft. Ein Test auf die Differenz zweier Anteile und ein gepaarter t-Test über mehrere zufällige Trainings-Test-Aufteilungen fanden mit hoher Wahrscheinlichkeit Unterschiede, die nicht existieren (Fehler erster Art), und sollten nicht verwendet werden; ein gepaarter t-Test auf Basis zehnfacher Kreuzvalidierung hatte einen etwas erhöhten Fehler erster Art. Der McNemar-Test und der neue 5×2-cv-Test, der auf fünf Wiederholungen zweifacher Kreuzvalidierung beruht, hatten einen akzeptablen Fehler erster Art ([[model-comparison|Modellvergleiche]]).

#### 5. Bayes'sche und frequentistische Sicht

In der Bayes'schen Inferenz werden unbekannte Größen als zufällig behandelt: Eine Prior-Verteilung wird über die Bayes-Regel mit der Likelihood der Daten zu einer Posterior-Verteilung verknüpft, und die Unsicherheit wird mit Posterior-Intervallen zusammengefasst (Gelman et al., 2013). Frequentistische Tests und Konfidenzintervalle beschreiben dagegen, wie sich ein Verfahren über wiederholte Stichproben verhält.

#### Ursprung und Varianten

Der Bootstrap (Efron, 1979), Tests zum Vergleich von Klassifikatoren (Dietterich, 1998), der Praxisleitfaden zu Online-Experimenten (Kohavi et al., 2009) und die Bayes'sche Datenanalyse (Gelman et al., 2013) sind zentrale Referenzen; Greenland et al. (2016) und Wasserstein & Lazar (2016) behandeln Fehldeutungen von p-Werten und Konfidenzintervallen.

### Wann einsetzen

- Wenn Modellmetriken berichtet werden, sollten sie eine Schätzung der Unsicherheit enthalten, etwa per Bootstrap (Efron, 1979).
- Wenn eine Produktänderung mit echten Nutzenden bewertet wird, ist ein randomisierter A/B-Test das Mittel der Wahl (Kohavi et al., 2009).
- Wenn zwei Lernverfahren auf einem Datensatz verglichen werden, sollten Tests mit kontrolliertem Fehler erster Art wie der McNemar-Test oder 5×2 cv verwendet werden (Dietterich, 1998).

### Stärken und Grenzen

**Stärken**
- Der Bootstrap schätzt Unsicherheit ohne starke Annahmen (Efron, 1979).
- Randomisierte Experimente weisen kausale Effekte nach (Kohavi et al., 2009).
- Geeignete Tests halten die Rate falscher Befunde unter Kontrolle (Dietterich, 1998).

**Einschränkungen**
- p-Werte und Konfidenzintervalle werden häufig falsch interpretiert (Greenland et al., 2016).
- Ein p-Wert sagt nichts über Größe oder Bedeutung eines Effekts aus (Wasserstein & Lazar, 2016).
- Einige verbreitete Tests zum Vergleich von Lernverfahren haben einen hohen Fehler erster Art (Dietterich, 1998).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Bootstrap | Erneutes Ziehen aus den beobachteten Daten (Efron, 1979) | Unsicherheit beliebiger Statistiken |
| Frequentistische Tests und Konfidenzintervalle | Verhalten eines Verfahrens über wiederholte Stichproben (Greenland et al., 2016) | Entscheidungen mit kontrollierten Fehlerraten |
| Bayes'sche Inferenz | Posterior-Verteilung aus Prior und Daten (Gelman et al., 2013) | Einbezug von Vorwissen, direkte Wahrscheinlichkeitsaussagen |
| A/B-Test | Zufällige Zuteilung von Nutzenden (Kohavi et al., 2009) | Kausale Effekte von Produktänderungen |

### In der Praxis

Evaluationsergebnisse werden mit Intervallen und Effektgrößen berichtet, nicht nur mit p-Werten (Wasserstein & Lazar, 2016). Analysen werden nicht erst danach ausgewählt, welche ein signifikantes Ergebnis liefert, weil das die p-Werte verzerrt (Greenland et al., 2016). Bei LLM-basierten Systemen gelten dieselben Grundsätze, wenn Prompt- oder Modellvarianten verglichen werden ([[prompt-comparison|Prompt-Vergleiche]]).

### Merksatz

Jedes Evaluationsergebnis ist eine Schätzung mit Unsicherheit; sie sollte quantifiziert, mit Tests kontrollierter Fehlerrate geprüft und ein p-Wert nie als Wahrscheinlichkeit für die Wahrheit einer Hypothese gelesen werden.

### Quellen

- Greenland, S., Senn, S. J., Rothman, K. J., Carlin, J. B., Poole, C., Goodman, S. N. & Altman, D. G. (2016). *Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations.* European Journal of Epidemiology 31(4). [doi:10.1007/s10654-016-0149-3](https://doi.org/10.1007/s10654-016-0149-3)
- Wasserstein, R. L. & Lazar, N. A. (2016). *The ASA Statement on p-Values: Context, Process, and Purpose.* The American Statistician 70(2). [doi:10.1080/00031305.2016.1154108](https://doi.org/10.1080/00031305.2016.1154108)
- Efron, B. (1979). *Bootstrap Methods: Another Look at the Jackknife.* The Annals of Statistics 7(1). [doi:10.1214/aos/1176344552](https://doi.org/10.1214/aos/1176344552)
- Kohavi, R., Longbotham, R., Sommerfield, D. & Henne, R. M. (2009). *Controlled experiments on the web: survey and practical guide.* Data Mining and Knowledge Discovery 18(1). [doi:10.1007/s10618-008-0114-1](https://doi.org/10.1007/s10618-008-0114-1)
- Dietterich, T. G. (1998). *Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms.* Neural Computation 10(7). [doi:10.1162/089976698300017197](https://doi.org/10.1162/089976698300017197)
- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A. & Rubin, D. B. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press. [book website](https://sites.stat.columbia.edu/gelman/book/)
