---
title_en: Causal Inference
title_de: Kausale Inferenz
entity_type: Method
sources:
- https://doi.org/10.1080/01621459.1986.10478354
- https://doi.org/10.1214/09-SS057
- https://doi.org/10.1093/biomet/70.1.41
- https://doi.org/10.1080/01621459.1996.10476902
- https://doi.org/10.1126/science.187.4175.398
- https://miguelhernan.org/whatifbook
- https://arxiv.org/abs/1703.06856
- https://edoc.ub.uni-muenchen.de/36297/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Causal inference asks what would happen if something were changed, not only which variables move together. Because each unit can only be observed under one condition, causal effects cannot be read directly from data (Holland, 1986); they are estimated with randomised experiments or, for observational data, with methods such as propensity scores (Rosenbaum & Rubin, 1983) and instrumental variables (Angrist et al., 1996), based on explicit causal assumptions that are often expressed as causal graphs (Pearl, 2009). Causal reasoning also underlies counterfactual fairness (Kusner et al., 2017; Urchs, 2025).

### How it works

A causal question is stated, the assumptions about how variables influence each other are made explicit, and a design or estimation method is chosen whose assumptions are plausible for the data. The result is an estimate of a causal effect that is only as credible as these assumptions.

```text
1. Correlation and causation
▼
2. Potential outcomes and the fundamental problem
▼
3. Causal graphs and structural models
▼
4. Randomised experiments
▼
5. Methods for observational data
▼
6. Causal inference and fairness
```

#### 1. Correlation and causation

Correlation does not imply causation (Holland, 1986). Aggregated data can even point in the wrong direction: graduate admissions at the University of California, Berkeley, in fall 1973 showed a clear pattern of bias against women in the aggregate, but disaggregated by department there was little evidence of discrimination and, properly pooled, a small bias in favour of women (Bickel et al., 1975). The aggregate pattern arose because women applied more often to departments that were harder to enter for applicants of either sex, an instance of Simpson's paradox.

#### 2. Potential outcomes and the fundamental problem

In the potential-outcomes model, each unit has an outcome under treatment and an outcome under control, and the causal effect is their difference (Holland, 1986). Only one of the two can ever be observed for a given unit, which Holland calls the fundamental problem of causal inference. Causal inference therefore estimates average effects over groups under assumptions, for example those justified by randomisation (Hernán & Robins, 2020).

#### 3. Causal graphs and structural models

Pearl (2009) describes causal inference with the structural causal model, which unifies other approaches and represents causal assumptions, for example as directed graphs of which variable influences which. Such graphs make confounding and selection bias visible (Hernán & Robins, 2020). All causal claims rest on assumptions that cannot be tested from data alone, and the tools address three kinds of questions: effects of interventions, probabilities of counterfactuals, and direct and indirect effects (Pearl, 2009).

#### 4. Randomised experiments

When treatment is assigned at random, treated and untreated groups are comparable in expectation, so differences in outcomes can be attributed to the treatment; randomised experiments are therefore the reference design for causal effects (Holland, 1986; Hernán & Robins, 2020). Online A/B tests apply this idea to product decisions ([[statistics-fundamentals|Statistics Fundamentals]]).

#### 5. Methods for observational data

Without randomisation, causal effects can be estimated under assumptions such as exchangeability given measured covariates (Hernán & Robins, 2020). The propensity score, the probability of receiving treatment given observed covariates, is sufficient to remove bias due to all observed covariates, and can be used for matching, subclassification or adjustment (Rosenbaum & Rubin, 1983). When assignment is random but compliance is imperfect, instrumental variables identify the average causal effect for the subgroup of compliers under simple, interpretable assumptions; Angrist et al. (1996) applied this to the effect of veteran status in the Vietnam era on mortality, using the draft lottery as instrument.

#### 6. Causal inference and fairness

Counterfactual fairness uses causal models to define fair decisions: a decision is fair towards an individual if it would be the same in a counterfactual world in which the individual belonged to a different demographic group (Kusner et al., 2017). Urchs (2025) illustrates this with a loan example: a woman denied a loan must also be denied in the counterfactual world in which she is male with the same qualifications, which matters even if gender is not a feature, because gender may have influenced intermediate variables such as income history. The approach offers strong guarantees but depends on a well-specified causal model ([[fairness-metrics|Fairness Metrics]]). Urchs (2025) also describes causal front-door adjustment, which routes an intervention through intermediate variables such as chain-of-thought prompts, as one strategy for mitigating bias in language models.

#### Origin and variants

Holland (1986) set out the potential-outcomes view, Rosenbaum & Rubin (1983) introduced the propensity score, Angrist et al. (1996) embedded instrumental variables in the potential-outcomes model, and Pearl (2009) summarised the structural causal model. Hernán & Robins (2020) give a textbook treatment, and Kusner et al. (2017) carried causal reasoning into fairness.

### When to use it

- When a decision depends on the effect of an intervention, such as a treatment, a policy or a product change, rather than on a prediction (Holland, 1986).
- When randomisation is impossible and observational data must be used, with propensity scores or instrumental variables under explicit assumptions (Rosenbaum & Rubin, 1983; Angrist et al., 1996).
- When fairness should be defined in terms of what would have happened with a different protected attribute (Kusner et al., 2017).

### Strengths and limitations

**Strengths**
- Randomised experiments provide credible causal effects (Holland, 1986).
- Causal graphs make assumptions explicit and reveal confounding (Pearl, 2009; Hernán & Robins, 2020).
- Propensity scores reduce adjustment for many covariates to a single score (Rosenbaum & Rubin, 1983).

**Limitations**
- The fundamental problem means individual causal effects are never observed (Holland, 1986).
- Causal claims rest on assumptions that cannot be tested from data alone (Pearl, 2009).
- Propensity scores only remove bias from observed covariates (Rosenbaum & Rubin, 1983).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Randomised experiment | Random assignment makes groups comparable (Holland, 1986) | Interventions that can be assigned |
| Propensity score methods | Adjust for observed covariates via one score (Rosenbaum & Rubin, 1983) | Observational data with rich covariates |
| Instrumental variables | Use a variable that affects treatment but not the outcome directly (Angrist et al., 1996) | Imperfect compliance, unobserved confounding |
| Structural causal models | Graphs and equations for interventions and counterfactuals (Pearl, 2009) | Explicit modelling of causal assumptions |

### In practice

The causal question and the assumptions are written down, ideally as a causal graph, before any data is analysed (Hernán & Robins, 2020). Results are reported together with the assumptions they depend on, and aggregated comparisons are checked for confounding by stratifying on relevant variables, as the Berkeley example shows (Bickel et al., 1975).

### Key takeaway

Causal inference estimates what would happen under an intervention, which requires either randomisation or explicit, defensible assumptions about how the variables are connected.

### Sources

- Holland, P. W. (1986). *Statistics and Causal Inference.* Journal of the American Statistical Association 81(396). [doi:10.1080/01621459.1986.10478354](https://doi.org/10.1080/01621459.1986.10478354)
- Pearl, J. (2009). *Causal inference in statistics: An overview.* Statistics Surveys 3. [doi:10.1214/09-SS057](https://doi.org/10.1214/09-SS057)
- Rosenbaum, P. R. & Rubin, D. B. (1983). *The central role of the propensity score in observational studies for causal effects.* Biometrika 70(1). [doi:10.1093/biomet/70.1.41](https://doi.org/10.1093/biomet/70.1.41)
- Angrist, J. D., Imbens, G. W. & Rubin, D. B. (1996). *Identification of Causal Effects Using Instrumental Variables.* Journal of the American Statistical Association 91(434). [doi:10.1080/01621459.1996.10476902](https://doi.org/10.1080/01621459.1996.10476902)
- Bickel, P. J., Hammel, E. A. & O'Connell, J. W. (1975). *Sex Bias in Graduate Admissions: Data from Berkeley.* Science 187(4175). [doi:10.1126/science.187.4175.398](https://doi.org/10.1126/science.187.4175.398)
- Hernán, M. A. & Robins, J. M. (2020). *Causal Inference: What If.* Chapman & Hall/CRC. [book website](https://miguelhernan.org/whatifbook)
- Kusner, M. J. et al. (2017). *Counterfactual Fairness.* NeurIPS 2017. [arXiv:1703.06856](https://arxiv.org/abs/1703.06856)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Kausale Inferenz fragt, was geschähe, wenn etwas verändert würde, und nicht nur, welche Variablen gemeinsam variieren. Da jede Einheit nur unter einer Bedingung beobachtet werden kann, lassen sich kausale Effekte nicht direkt aus Daten ablesen (Holland, 1986); sie werden mit randomisierten Experimenten geschätzt oder bei Beobachtungsdaten mit Verfahren wie Propensity Scores (Rosenbaum & Rubin, 1983) und Instrumentvariablen (Angrist et al., 1996), gestützt auf ausdrückliche kausale Annahmen, die oft als kausale Graphen formuliert werden (Pearl, 2009). Kausales Denken liegt auch der Counterfactual Fairness zugrunde (Kusner et al., 2017; Urchs, 2025).

### Funktionsweise

Eine kausale Frage wird formuliert, die Annahmen darüber, wie sich Variablen gegenseitig beeinflussen, werden offengelegt, und es wird ein Design oder Schätzverfahren gewählt, dessen Annahmen für die Daten plausibel sind. Das Ergebnis ist eine Schätzung eines kausalen Effekts, die nur so glaubwürdig ist wie diese Annahmen.

```text
1. Korrelation und Kausalität
▼
2. Potenzielle Ergebnisse und das Fundamentalproblem
▼
3. Kausale Graphen und Strukturmodelle
▼
4. Randomisierte Experimente
▼
5. Verfahren für Beobachtungsdaten
▼
6. Kausale Inferenz und Fairness
```

#### 1. Korrelation und Kausalität

Korrelation bedeutet keine Kausalität (Holland, 1986). Aggregierte Daten können sogar in die falsche Richtung weisen: Die Zulassungen zum Graduiertenstudium an der University of California, Berkeley, im Herbst 1973 zeigten insgesamt ein deutliches Muster der Benachteiligung von Frauen, nach Fachbereichen aufgeschlüsselt gab es aber kaum Hinweise auf Diskriminierung und, korrekt zusammengefasst, eine leichte Bevorzugung von Frauen (Bickel et al., 1975). Das Gesamtmuster entstand, weil sich Frauen häufiger bei Fachbereichen bewarben, die für Bewerbende beiderlei Geschlechts schwerer zugänglich waren, ein Fall des Simpson-Paradoxons.

#### 2. Potenzielle Ergebnisse und das Fundamentalproblem

Im Modell der potenziellen Ergebnisse (Potential Outcomes) hat jede Einheit ein Ergebnis unter Behandlung und eines unter Kontrolle, und der kausale Effekt ist ihre Differenz (Holland, 1986). Für eine gegebene Einheit lässt sich immer nur eines der beiden beobachten; Holland nennt dies das Fundamentalproblem der kausalen Inferenz. Kausale Inferenz schätzt daher durchschnittliche Effekte über Gruppen unter Annahmen, etwa solchen, die durch Randomisierung gerechtfertigt sind (Hernán & Robins, 2020).

#### 3. Kausale Graphen und Strukturmodelle

Pearl (2009) beschreibt kausale Inferenz mit dem strukturellen Kausalmodell, das andere Ansätze vereint und kausale Annahmen darstellt, etwa als gerichtete Graphen, welche Variable welche beeinflusst. Solche Graphen machen Confounding und Selektionsverzerrung sichtbar (Hernán & Robins, 2020). Alle kausalen Aussagen beruhen auf Annahmen, die sich allein aus Daten nicht prüfen lassen, und die Werkzeuge beantworten drei Arten von Fragen: Effekte von Interventionen, Wahrscheinlichkeiten kontrafaktischer Aussagen sowie direkte und indirekte Effekte (Pearl, 2009).

#### 4. Randomisierte Experimente

Wird eine Behandlung zufällig zugeteilt, sind behandelte und unbehandelte Gruppen im Erwartungswert vergleichbar, sodass Unterschiede in den Ergebnissen der Behandlung zugeschrieben werden können; randomisierte Experimente sind daher das Referenzdesign für kausale Effekte (Holland, 1986; Hernán & Robins, 2020). Online-A/B-Tests übertragen diese Idee auf Produktentscheidungen ([[statistics-fundamentals|Statistik-Grundlagen]]).

#### 5. Verfahren für Beobachtungsdaten

Ohne Randomisierung lassen sich kausale Effekte unter Annahmen wie der Austauschbarkeit gegeben die gemessenen Kovariaten schätzen (Hernán & Robins, 2020). Der Propensity Score, die Wahrscheinlichkeit, bei gegebenen beobachteten Kovariaten behandelt zu werden, genügt, um die Verzerrung durch alle beobachteten Kovariaten zu beseitigen, und kann für Matching, Subklassifikation oder Adjustierung genutzt werden (Rosenbaum & Rubin, 1983). Ist die Zuteilung zufällig, wird sie aber nicht vollständig befolgt, identifizieren Instrumentvariablen unter einfachen, interpretierbaren Annahmen den durchschnittlichen kausalen Effekt für die Teilgruppe derer, die der Zuteilung folgen (Compliers); Angrist et al. (1996) wandten das auf den Effekt des Veteranenstatus in der Vietnam-Ära auf die Sterblichkeit an, mit der Einberufungslotterie als Instrument.

#### 6. Kausale Inferenz und Fairness

Counterfactual Fairness definiert faire Entscheidungen über kausale Modelle: Eine Entscheidung ist gegenüber einer Person fair, wenn sie in einer kontrafaktischen Welt, in der die Person einer anderen demografischen Gruppe angehörte, gleich ausfiele (Kusner et al., 2017). Urchs (2025) veranschaulicht das an einem Kreditbeispiel: Wird einer Frau ein Kredit verweigert, muss er ihr auch in der kontrafaktischen Welt verweigert werden, in der sie bei gleicher Qualifikation männlich ist; das ist selbst dann relevant, wenn das Geschlecht kein Merkmal des Modells ist, weil es Zwischenvariablen wie den Einkommensverlauf beeinflusst haben kann. Der Ansatz bietet starke Garantien, hängt aber von einem gut spezifizierten Kausalmodell ab ([[fairness-metrics|Fairness-Metriken]]). Urchs (2025) beschreibt außerdem die kausale Front-Door-Adjustierung, die eine Intervention über Zwischenvariablen wie Chain-of-Thought-Prompts leitet, als eine Strategie zur Minderung von Bias in Sprachmodellen.

#### Ursprung und Varianten

Holland (1986) legte die Sicht der potenziellen Ergebnisse dar, Rosenbaum & Rubin (1983) führten den Propensity Score ein, Angrist et al. (1996) verankerten Instrumentvariablen im Modell der potenziellen Ergebnisse, und Pearl (2009) fasste das strukturelle Kausalmodell zusammen. Hernán & Robins (2020) bieten eine Lehrbuchdarstellung, und Kusner et al. (2017) übertrugen kausales Denken auf Fairness.

### Wann einsetzen

- Wenn eine Entscheidung vom Effekt einer Intervention abhängt, etwa einer Behandlung, einer Maßnahme oder einer Produktänderung, und nicht von einer Vorhersage (Holland, 1986).
- Wenn Randomisierung unmöglich ist und Beobachtungsdaten genutzt werden müssen, mit Propensity Scores oder Instrumentvariablen unter ausdrücklichen Annahmen (Rosenbaum & Rubin, 1983; Angrist et al., 1996).
- Wenn Fairness darüber definiert werden soll, was mit einem anderen geschützten Merkmal geschehen wäre (Kusner et al., 2017).

### Stärken und Grenzen

**Stärken**
- Randomisierte Experimente liefern glaubwürdige kausale Effekte (Holland, 1986).
- Kausale Graphen legen Annahmen offen und zeigen Confounding (Pearl, 2009; Hernán & Robins, 2020).
- Propensity Scores reduzieren die Adjustierung für viele Kovariaten auf einen einzigen Wert (Rosenbaum & Rubin, 1983).

**Einschränkungen**
- Wegen des Fundamentalproblems sind individuelle kausale Effekte nie beobachtbar (Holland, 1986).
- Kausale Aussagen beruhen auf Annahmen, die sich allein aus Daten nicht prüfen lassen (Pearl, 2009).
- Propensity Scores beseitigen nur die Verzerrung durch beobachtete Kovariaten (Rosenbaum & Rubin, 1983).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Randomisiertes Experiment | Zufällige Zuteilung macht Gruppen vergleichbar (Holland, 1986) | Zuteilbare Interventionen |
| Propensity-Score-Verfahren | Adjustieren für beobachtete Kovariaten über einen Wert (Rosenbaum & Rubin, 1983) | Beobachtungsdaten mit vielen Kovariaten |
| Instrumentvariablen | Nutzen eine Variable, die die Behandlung beeinflusst, das Ergebnis aber nicht direkt (Angrist et al., 1996) | Unvollständige Befolgung, unbeobachtetes Confounding |
| Strukturelle Kausalmodelle | Graphen und Gleichungen für Interventionen und kontrafaktische Aussagen (Pearl, 2009) | Ausdrückliche Modellierung kausaler Annahmen |

### In der Praxis

Die kausale Frage und die Annahmen werden vor jeder Datenanalyse aufgeschrieben, idealerweise als kausaler Graph (Hernán & Robins, 2020). Ergebnisse werden zusammen mit den Annahmen berichtet, auf denen sie beruhen, und aggregierte Vergleiche werden durch Schichtung nach relevanten Variablen auf Confounding geprüft, wie das Berkeley-Beispiel zeigt (Bickel et al., 1975).

### Merksatz

Kausale Inferenz schätzt, was unter einer Intervention geschähe; dafür braucht es entweder Randomisierung oder ausdrückliche, begründbare Annahmen darüber, wie die Variablen zusammenhängen.

### Quellen

- Holland, P. W. (1986). *Statistics and Causal Inference.* Journal of the American Statistical Association 81(396). [doi:10.1080/01621459.1986.10478354](https://doi.org/10.1080/01621459.1986.10478354)
- Pearl, J. (2009). *Causal inference in statistics: An overview.* Statistics Surveys 3. [doi:10.1214/09-SS057](https://doi.org/10.1214/09-SS057)
- Rosenbaum, P. R. & Rubin, D. B. (1983). *The central role of the propensity score in observational studies for causal effects.* Biometrika 70(1). [doi:10.1093/biomet/70.1.41](https://doi.org/10.1093/biomet/70.1.41)
- Angrist, J. D., Imbens, G. W. & Rubin, D. B. (1996). *Identification of Causal Effects Using Instrumental Variables.* Journal of the American Statistical Association 91(434). [doi:10.1080/01621459.1996.10476902](https://doi.org/10.1080/01621459.1996.10476902)
- Bickel, P. J., Hammel, E. A. & O'Connell, J. W. (1975). *Sex Bias in Graduate Admissions: Data from Berkeley.* Science 187(4175). [doi:10.1126/science.187.4175.398](https://doi.org/10.1126/science.187.4175.398)
- Hernán, M. A. & Robins, J. M. (2020). *Causal Inference: What If.* Chapman & Hall/CRC. [book website](https://miguelhernan.org/whatifbook)
- Kusner, M. J. et al. (2017). *Counterfactual Fairness.* NeurIPS 2017. [arXiv:1703.06856](https://arxiv.org/abs/1703.06856)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
