---
title_en: Fairness Metrics
title_de: Fairness-Metriken
entity_type: Concept
sources:
- https://edoc.ub.uni-muenchen.de/36297/
- https://doi.org/10.1145/2090236.2090255
- https://arxiv.org/abs/1610.02413
- https://arxiv.org/abs/1609.05807
- https://arxiv.org/abs/1703.00056
- https://proceedings.mlr.press/v80/kearns18a.html
- https://doi.org/10.1145/3457607
- https://arxiv.org/abs/1703.06856
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Fairness metrics turn normative ideas of fair treatment into measurable criteria for a classifier's decisions. They fall into three families: individual fairness (similar people are treated similarly), group fairness (statistics such as approval or error rates are equal across groups) and subgroup fairness (the same guarantees hold for many intersecting subgroups) (Urchs, 2025; Mehrabi et al., 2021). Common group criteria cannot all be satisfied at once when base rates differ (Kleinberg et al., 2016; Chouldechova, 2017), so choosing a metric is a normative decision, not a purely technical one.

### How it works

A protected attribute such as gender is fixed, the classifier's predictions are compared with the true labels per person or per group, and the chosen criterion is checked. If it is violated, the model, its threshold or its training data is adjusted, for example by post-processing the predictions (Hardt et al., 2016).

```text
1. Bias, fairness and discrimination
▼
2. Individual fairness
▼
3. Group fairness
▼
4. Incompatibility of group criteria
▼
5. Subgroup fairness
▼
6. Limits of formal metrics
```

#### 1. Bias, fairness and discrimination

Urchs (2025) distinguishes three related concepts. Bias refers to imbalances or distortions in data or model behaviour. Fairness is the effort to identify and mitigate differences in treatment that are considered normatively problematic; it is context-dependent and goes back to Aristotle's idea of treating equals equally, which requires a normative decision about who counts as equal for a given task. Discrimination is the manifestation of unequal treatment that systematically disadvantages people because of attributes such as gender. Most fairness metrics are bias-preserving: they aim at formal equality and try to reflect the observed world without adding new distortions. Bias-transforming approaches instead correct for existing inequalities, which requires contested value judgements about what a better world should look like (Urchs, 2025).

#### 2. Individual fairness

Individual fairness asks whether similar individuals receive similar outcomes. Fairness through awareness (Dwork et al., 2012) uses a task-specific similarity metric d between individuals and requires that the distance between their predicted outcome distributions is at most d(x, x′); for example, two loan applicants with nearly identical income and credit score should receive similar approval probabilities (Urchs, 2025). Fairness through unawareness simply removes the protected attribute from the input, but remains vulnerable to proxies such as name or occupation. Counterfactual fairness (Kusner et al., 2017) uses a causal model: a decision is fair towards an individual if it would be the same in a counterfactual world in which the individual belonged to a different demographic group ([[causal-inference|Causal Inference]]).

#### 3. Group fairness

Group fairness compares aggregate statistics between groups defined by the protected attribute (Mehrabi et al., 2021; Urchs, 2025). With prediction Ŷ, true label Y and attribute A:

- **Demographic parity:** P(Ŷ = 1 | A = a) = P(Ŷ = 1 | A = a′), equal rates of favourable predictions regardless of qualification.
- **Equalised odds:** P(Ŷ = 1 | Y = y, A = a) = P(Ŷ = 1 | Y = y, A = a′) for y ∈ {0, 1}, equal true positive and false positive rates.
- **Equal opportunity:** only equal true positive rates, i.e. qualified individuals have the same chance in every group (Hardt et al., 2016).
- **Predictive parity:** equal precision, P(Y = 1 | Ŷ = 1, A = a) = P(Y = 1 | Ŷ = 1, A = a′).

Further criteria include conditional statistical parity, treatment equality (equal ratio of false negatives to false positives), false positive and false negative rate balance and overall accuracy equality (Urchs, 2025). Hardt et al. (2016) show how any learned predictor can be optimally adjusted to satisfy equal opportunity, and note that such criteria are oblivious: they depend only on the joint statistics of prediction, target and attribute.

#### 4. Incompatibility of group criteria

Kleinberg et al. (2016) formalised three fairness conditions for risk scores and proved that, except in highly constrained special cases, no method can satisfy all three at the same time. Chouldechova (2017) showed for recidivism prediction instruments that several fairness criteria cannot all hold when the prevalence of the outcome differs between groups, and that disparate impact can arise when error rates are not balanced. Choosing a criterion therefore means choosing which kind of equality matters in the application.

#### 5. Subgroup fairness

Group criteria are checked for a few predefined groups and are susceptible to fairness gerrymandering: a classifier looks fair for each group but discriminates against structured subgroups defined over several protected attributes (Kearns et al., 2018). Urchs (2025) gives an example: a classifier that approves loans only for Black men and White women approves 50% of applicants by gender and 50% by race, satisfying demographic parity for each attribute, but never approves White men or Black women. Subgroup fairness therefore requires that statistical parity or false positive rates hold across a rich class of subgroups, with deviations weighted by subgroup size; auditing this is computationally hard in the worst case, but practical algorithms exist (Kearns et al., 2018).

#### 6. Limits of formal metrics

Formal metrics need discrete group labels, stable similarity notions and enough data per subgroup, which is difficult for intersectional or fluid identities such as non-binary gender (Urchs, 2025). They tend to treat groups as symmetric and ahistorical, so that even statistical parity can create an illusion of fairness while ignoring structural inequality. Different definitions can also be mutually incompatible (Chouldechova, 2017).

#### Origin and variants

Fairness through awareness (Dwork et al., 2012) defined individual fairness, equal opportunity and equalised odds (Hardt et al., 2016) became standard group criteria, the impossibility results of Kleinberg et al. (2016) and Chouldechova (2017) showed their trade-offs, and subgroup fairness (Kearns et al., 2018) and counterfactual fairness (Kusner et al., 2017) extended the definitions. Mehrabi et al. (2021) survey the field, and Urchs (2025) systematises the metrics for gender fairness in NLP.

### When to use it

- When a classifier makes decisions about people, such as loans, hiring or admissions, and unequal treatment must be measured (Mehrabi et al., 2021).
- When the qualified members of each group should have the same chance, equal opportunity fits (Hardt et al., 2016).
- When several protected attributes interact, subgroup fairness reveals discrimination that per-attribute checks miss (Kearns et al., 2018).

### Strengths and limitations

**Strengths**
- Make normative goals measurable and usable as constraints during model development (Urchs, 2025).
- Any learned predictor can be post-processed to satisfy equal opportunity (Hardt et al., 2016).
- Subgroup fairness protects intersectional groups against fairness gerrymandering (Kearns et al., 2018).

**Limitations**
- Common group criteria cannot all be satisfied when base rates differ (Kleinberg et al., 2016; Chouldechova, 2017).
- Oblivious criteria only use joint statistics and cannot tell why outcomes differ (Hardt et al., 2016).
- Metrics need discrete group labels and ignore structural, historical inequality (Urchs, 2025).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Individual fairness | Similar individuals receive similar outcomes; needs a similarity metric (Dwork et al., 2012) | Decisions where a task-specific similarity can be justified |
| Counterfactual fairness | Decision unchanged in a world with a different protected attribute; needs a causal model (Kusner et al., 2017) | Settings with a credible causal model |
| Demographic parity | Equal rates of favourable predictions (Mehrabi et al., 2021) | Representation goals independent of labels |
| Equalised odds / equal opportunity | Equal error rates conditioned on the true label (Hardt et al., 2016) | Decisions where the observed labels are trusted |
| Subgroup fairness | Guarantees across many intersecting subgroups (Kearns et al., 2018) | Several interacting protected attributes |

### In practice

Before measuring, the team decides which notion of equality matters and whether a bias-preserving or bias-transforming goal is pursued (Urchs, 2025). Metrics are reported per group and, where several attributes matter, per subgroup (Kearns et al., 2018). For language technology, the same questions arise in text: [[bias-in-nlp|Bias in NLP]] covers how stereotypes are measured in embeddings and language models, and in the EU high-risk AI systems must be examined for possible biases ([[eu-ai-act|EU AI Act]]).

### Key takeaway

Fairness metrics make different notions of equal treatment measurable, but they conflict with each other, so choosing one is a normative decision that must fit the application.

### Sources

- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
- Dwork, C., Hardt, M., Pitassi, T., Reingold, O. & Zemel, R. (2012). *Fairness Through Awareness.* ITCS 2012. [doi:10.1145/2090236.2090255](https://doi.org/10.1145/2090236.2090255)
- Hardt, M. et al. (2016). *Equality of Opportunity in Supervised Learning.* NeurIPS 2016. [arXiv:1610.02413](https://arxiv.org/abs/1610.02413)
- Kleinberg, J. et al. (2016). *Inherent Trade-Offs in the Fair Determination of Risk Scores.* ITCS 2017. [arXiv:1609.05807](https://arxiv.org/abs/1609.05807)
- Chouldechova, A. (2017). *Fair prediction with disparate impact: A study of bias in recidivism prediction instruments.* [arXiv:1703.00056](https://arxiv.org/abs/1703.00056)
- Kearns, M., Neel, S., Roth, A. & Wu, Z. S. (2018). *Preventing Fairness Gerrymandering: Auditing and Learning for Subgroup Fairness.* ICML 2018. [PMLR](https://proceedings.mlr.press/v80/kearns18a.html)
- Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. & Galstyan, A. (2021). *A Survey on Bias and Fairness in Machine Learning.* ACM Computing Surveys 54(6). [doi:10.1145/3457607](https://doi.org/10.1145/3457607)
- Kusner, M. J. et al. (2017). *Counterfactual Fairness.* NeurIPS 2017. [arXiv:1703.06856](https://arxiv.org/abs/1703.06856)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Fairness-Metriken übersetzen normative Vorstellungen fairer Behandlung in messbare Kriterien für die Entscheidungen eines Klassifikators. Sie bilden drei Familien: individuelle Fairness (ähnliche Personen werden ähnlich behandelt), Gruppenfairness (Kennzahlen wie Zusage- oder Fehlerraten sind zwischen Gruppen gleich) und Subgruppen-Fairness (dieselben Garantien gelten für viele sich überschneidende Teilgruppen) (Urchs, 2025; Mehrabi et al., 2021). Gängige Gruppenkriterien lassen sich bei unterschiedlichen Basisraten nicht alle gleichzeitig erfüllen (Kleinberg et al., 2016; Chouldechova, 2017); die Wahl einer Metrik ist daher eine normative und keine rein technische Entscheidung.

### Funktionsweise

Ein geschütztes Merkmal wie das Geschlecht wird festgelegt, die Vorhersagen des Klassifikators werden je Person oder je Gruppe mit den tatsächlichen Labels verglichen, und das gewählte Kriterium wird geprüft. Ist es verletzt, werden Modell, Schwellenwert oder Trainingsdaten angepasst, etwa durch Nachbearbeitung der Vorhersagen (Hardt et al., 2016).

```text
1. Bias, Fairness und Diskriminierung
▼
2. Individuelle Fairness
▼
3. Gruppenfairness
▼
4. Unvereinbarkeit von Gruppenkriterien
▼
5. Subgruppen-Fairness
▼
6. Grenzen formaler Metriken
```

#### 1. Bias, Fairness und Diskriminierung

Urchs (2025) unterscheidet drei verwandte Begriffe. Bias bezeichnet Ungleichgewichte oder Verzerrungen in Daten oder im Modellverhalten. Fairness ist das Bemühen, Unterschiede in der Behandlung zu erkennen und abzumildern, die als normativ problematisch gelten; sie ist kontextabhängig und geht auf Aristoteles' Gedanken zurück, Gleiches gleich zu behandeln, was eine normative Entscheidung darüber verlangt, wer für eine Aufgabe als gleich gilt. Diskriminierung ist die Ausprägung ungleicher Behandlung, die Menschen aufgrund von Merkmalen wie dem Geschlecht systematisch benachteiligt. Die meisten Fairness-Metriken sind bias-erhaltend (bias-preserving): Sie zielen auf formale Gleichheit und versuchen, die beobachtete Welt ohne neue Verzerrungen abzubilden. Bias-transformierende Ansätze korrigieren dagegen bestehende Ungleichheiten und setzen damit umstrittene Werturteile darüber voraus, wie eine bessere Welt aussehen soll (Urchs, 2025).

#### 2. Individuelle Fairness

Individuelle Fairness fragt, ob ähnliche Personen ähnliche Ergebnisse erhalten. Fairness through Awareness (Dwork et al., 2012) nutzt ein aufgabenspezifisches Ähnlichkeitsmaß d zwischen Personen und verlangt, dass der Abstand zwischen ihren vorhergesagten Ergebnisverteilungen höchstens d(x, x′) beträgt; zwei Kreditantragstellende mit nahezu gleichem Einkommen und ähnlicher Bonität sollten etwa ähnliche Zusagewahrscheinlichkeiten erhalten (Urchs, 2025). Fairness through Unawareness entfernt das geschützte Merkmal einfach aus der Eingabe, bleibt aber anfällig für Stellvertretermerkmale (Proxys) wie Name oder Beruf. Counterfactual Fairness (Kusner et al., 2017) nutzt ein kausales Modell: Eine Entscheidung ist gegenüber einer Person fair, wenn sie in einer kontrafaktischen Welt, in der die Person einer anderen demografischen Gruppe angehörte, gleich ausfiele ([[causal-inference|Kausale Inferenz]]).

#### 3. Gruppenfairness

Gruppenfairness vergleicht aggregierte Kennzahlen zwischen Gruppen, die durch das geschützte Merkmal definiert sind (Mehrabi et al., 2021; Urchs, 2025). Mit Vorhersage Ŷ, tatsächlichem Label Y und Merkmal A:

- **Demographic Parity:** P(Ŷ = 1 | A = a) = P(Ŷ = 1 | A = a′), gleiche Raten günstiger Vorhersagen unabhängig von der Qualifikation.
- **Equalised Odds:** P(Ŷ = 1 | Y = y, A = a) = P(Ŷ = 1 | Y = y, A = a′) für y ∈ {0, 1}, gleiche Richtig-positiv- und Falsch-positiv-Raten.
- **Equal Opportunity:** nur gleiche Richtig-positiv-Raten, qualifizierte Personen haben also in jeder Gruppe dieselbe Chance (Hardt et al., 2016).
- **Predictive Parity:** gleiche Precision, P(Y = 1 | Ŷ = 1, A = a) = P(Y = 1 | Ŷ = 1, A = a′).

Weitere Kriterien sind Conditional Statistical Parity, Treatment Equality (gleiches Verhältnis von falsch negativen zu falsch positiven Entscheidungen), ausgeglichene Falsch-positiv- und Falsch-negativ-Raten sowie gleiche Gesamtgenauigkeit (Urchs, 2025). Hardt et al. (2016) zeigen, wie sich jeder gelernte Prädiktor optimal so anpassen lässt, dass er Equal Opportunity erfüllt, und weisen darauf hin, dass solche Kriterien „oblivious“ sind: Sie hängen nur von der gemeinsamen Verteilung von Vorhersage, Zielgröße und Merkmal ab.

#### 4. Unvereinbarkeit von Gruppenkriterien

Kleinberg et al. (2016) formalisierten drei Fairness-Bedingungen für Risikoscores und bewiesen, dass sich außer in eng begrenzten Sonderfällen keine Methode findet, die alle drei gleichzeitig erfüllt. Chouldechova (2017) zeigte für Instrumente zur Rückfallprognose, dass mehrere Fairness-Kriterien nicht zugleich gelten können, wenn sich die Häufigkeit des Ereignisses zwischen den Gruppen unterscheidet, und dass mittelbare Benachteiligung (Disparate Impact) entstehen kann, wenn die Fehlerraten nicht ausgeglichen sind. Die Wahl eines Kriteriums ist daher die Wahl, welche Art von Gleichheit in der Anwendung zählt.

#### 5. Subgruppen-Fairness

Gruppenkriterien werden für wenige vorab festgelegte Gruppen geprüft und sind anfällig für Fairness Gerrymandering: Ein Klassifikator wirkt für jede Gruppe fair, benachteiligt aber strukturierte Teilgruppen, die über mehrere geschützte Merkmale definiert sind (Kearns et al., 2018). Urchs (2025) gibt ein Beispiel: Ein Klassifikator, der Kredite nur Schwarzen Männern und weißen Frauen gewährt, gewährt nach Geschlecht und nach Herkunft jeweils 50 % der Anträge und erfüllt Demographic Parity für jedes Merkmal einzeln, gewährt aber nie weißen Männern oder Schwarzen Frauen einen Kredit. Subgruppen-Fairness verlangt deshalb, dass Statistical Parity oder gleiche Falsch-positiv-Raten über eine reichhaltige Klasse von Teilgruppen gelten, wobei Abweichungen nach Gruppengröße gewichtet werden; die Prüfung ist im ungünstigsten Fall rechnerisch schwer, es gibt aber praktikable Algorithmen (Kearns et al., 2018).

#### 6. Grenzen formaler Metriken

Formale Metriken brauchen diskrete Gruppenlabels, stabile Ähnlichkeitsbegriffe und ausreichend Daten je Teilgruppe, was bei intersektionalen oder fluiden Identitäten wie nichtbinärem Geschlecht schwierig ist (Urchs, 2025). Sie behandeln Gruppen tendenziell als symmetrisch und geschichtslos, sodass selbst Statistical Parity den Anschein von Fairness erzeugen kann, während strukturelle Ungleichheit unbeachtet bleibt. Zudem können sich verschiedene Definitionen gegenseitig ausschließen (Chouldechova, 2017).

#### Ursprung und Varianten

Fairness through Awareness (Dwork et al., 2012) definierte individuelle Fairness, Equal Opportunity und Equalised Odds (Hardt et al., 2016) wurden zu Standardkriterien der Gruppenfairness, die Unmöglichkeitsresultate von Kleinberg et al. (2016) und Chouldechova (2017) zeigten ihre Zielkonflikte, und Subgruppen-Fairness (Kearns et al., 2018) sowie Counterfactual Fairness (Kusner et al., 2017) erweiterten die Definitionen. Mehrabi et al. (2021) geben einen Überblick über das Gebiet, und Urchs (2025) systematisiert die Metriken für Geschlechterfairness im NLP.

### Wann einsetzen

- Wenn ein Klassifikator über Menschen entscheidet, etwa über Kredite, Einstellungen oder Zulassungen, und ungleiche Behandlung gemessen werden muss (Mehrabi et al., 2021).
- Wenn die qualifizierten Angehörigen jeder Gruppe dieselbe Chance haben sollen, passt Equal Opportunity (Hardt et al., 2016).
- Wenn mehrere geschützte Merkmale zusammenwirken, deckt Subgruppen-Fairness Diskriminierung auf, die Prüfungen je Merkmal übersehen (Kearns et al., 2018).

### Stärken und Grenzen

**Stärken**
- Machen normative Ziele messbar und als Nebenbedingungen in der Modellentwicklung nutzbar (Urchs, 2025).
- Jeder gelernte Prädiktor lässt sich nachträglich so anpassen, dass er Equal Opportunity erfüllt (Hardt et al., 2016).
- Subgruppen-Fairness schützt intersektionale Gruppen vor Fairness Gerrymandering (Kearns et al., 2018).

**Einschränkungen**
- Gängige Gruppenkriterien lassen sich bei unterschiedlichen Basisraten nicht alle erfüllen (Kleinberg et al., 2016; Chouldechova, 2017).
- „Oblivious“ Kriterien nutzen nur gemeinsame Verteilungen und können nicht erklären, warum Ergebnisse sich unterscheiden (Hardt et al., 2016).
- Die Metriken brauchen diskrete Gruppenlabels und blenden strukturelle, historisch gewachsene Ungleichheit aus (Urchs, 2025).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Individuelle Fairness | Ähnliche Personen erhalten ähnliche Ergebnisse; braucht ein Ähnlichkeitsmaß (Dwork et al., 2012) | Entscheidungen, für die sich eine aufgabenspezifische Ähnlichkeit begründen lässt |
| Counterfactual Fairness | Entscheidung bleibt in einer Welt mit anderem geschütztem Merkmal gleich; braucht ein kausales Modell (Kusner et al., 2017) | Szenarien mit glaubwürdigem Kausalmodell |
| Demographic Parity | Gleiche Raten günstiger Vorhersagen (Mehrabi et al., 2021) | Repräsentationsziele unabhängig von Labels |
| Equalised Odds / Equal Opportunity | Gleiche Fehlerraten, bedingt auf das tatsächliche Label (Hardt et al., 2016) | Entscheidungen, bei denen den beobachteten Labels vertraut wird |
| Subgruppen-Fairness | Garantien über viele sich überschneidende Teilgruppen (Kearns et al., 2018) | Mehrere zusammenwirkende geschützte Merkmale |

### In der Praxis

Vor der Messung legt das Team fest, welcher Gleichheitsbegriff zählt und ob ein bias-erhaltendes oder ein bias-transformierendes Ziel verfolgt wird (Urchs, 2025). Metriken werden je Gruppe und, wenn mehrere Merkmale relevant sind, je Teilgruppe berichtet (Kearns et al., 2018). Für Sprachtechnologie stellen sich dieselben Fragen im Text: [[bias-in-nlp|Bias in NLP]] behandelt, wie Stereotype in Embeddings und Sprachmodellen gemessen werden, und in der EU müssen Hochrisiko-KI-Systeme auf mögliche Verzerrungen untersucht werden ([[eu-ai-act|KI-Verordnung]]).

### Merksatz

Fairness-Metriken machen unterschiedliche Vorstellungen gleicher Behandlung messbar, widersprechen einander aber; die Wahl einer Metrik ist daher eine normative Entscheidung, die zur Anwendung passen muss.

### Quellen

- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
- Dwork, C., Hardt, M., Pitassi, T., Reingold, O. & Zemel, R. (2012). *Fairness Through Awareness.* ITCS 2012. [doi:10.1145/2090236.2090255](https://doi.org/10.1145/2090236.2090255)
- Hardt, M. et al. (2016). *Equality of Opportunity in Supervised Learning.* NeurIPS 2016. [arXiv:1610.02413](https://arxiv.org/abs/1610.02413)
- Kleinberg, J. et al. (2016). *Inherent Trade-Offs in the Fair Determination of Risk Scores.* ITCS 2017. [arXiv:1609.05807](https://arxiv.org/abs/1609.05807)
- Chouldechova, A. (2017). *Fair prediction with disparate impact: A study of bias in recidivism prediction instruments.* [arXiv:1703.00056](https://arxiv.org/abs/1703.00056)
- Kearns, M., Neel, S., Roth, A. & Wu, Z. S. (2018). *Preventing Fairness Gerrymandering: Auditing and Learning for Subgroup Fairness.* ICML 2018. [PMLR](https://proceedings.mlr.press/v80/kearns18a.html)
- Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. & Galstyan, A. (2021). *A Survey on Bias and Fairness in Machine Learning.* ACM Computing Surveys 54(6). [doi:10.1145/3457607](https://doi.org/10.1145/3457607)
- Kusner, M. J. et al. (2017). *Counterfactual Fairness.* NeurIPS 2017. [arXiv:1703.06856](https://arxiv.org/abs/1703.06856)
