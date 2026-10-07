---
title_en: Feature Engineering
title_de: Feature Engineering
entity_type: Method
sources:
- https://jmlr.org/papers/v3/guyon03a.html
- https://doi.org/10.1145/507533.507538
- https://doi.org/10.1145/2382577.2382579
- https://jmlr.org/papers/v12/pedregosa11a.html
- https://otexts.com/fpp3/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Feature engineering turns raw data into input variables that help a model learn. Numerical features are transformed, categorical features encoded, for example by target encoding (Micci-Barreca, 2001), seasonal patterns represented explicitly (Hyndman & Athanasopoulos, 2021), and relevant features selected (Guyon & Elisseeff, 2003). The biggest risk is leakage: features that carry information about the target which would not be available when the model is used (Kaufman et al., 2012).

### How it works

Raw columns are transformed into features that make the relevant patterns easy for the chosen model to pick up. All transformations that learn from data, such as encodings or scalers, are fitted on the training data only and then applied unchanged to new data.

```text
1. Transforming numerical features
▼
2. Encoding categorical variables
▼
3. Representing time and seasonality
▼
4. Feature selection
▼
5. Leakage
```

#### 1. Transforming numerical features

Mathematical transformations such as logarithms or Box-Cox transformations can stabilise variation and make relationships easier to model (Hyndman & Athanasopoulos, 2021). Scaling to comparable ranges matters for distance-based and gradient-based methods ([[ml-preprocessing|ML Preprocessing]]).

#### 2. Encoding categorical variables

Many algorithms require numeric inputs, and categorical fields with a large number of distinct values are hard to represent (Micci-Barreca, 2001). Target encoding replaces each category with an estimate of the target statistic for that category, blended with the overall prior using empirical Bayes, so that rare categories are not over-trusted. For hierarchical categories such as ZIP codes, statistics from several levels of aggregation can be combined (Micci-Barreca, 2001).

#### 3. Representing time and seasonality

For time series regression, useful predictors include a trend, seasonal dummy variables and Fourier terms, i.e. pairs of sine and cosine terms that model seasonal patterns smoothly (Hyndman & Athanasopoulos, 2021; [[time-series-analysis|Time Series Analysis]]).

#### 4. Feature selection

Variable and feature selection aims at better predictive performance, faster and more cost-effective predictors and a better understanding of the underlying process (Guyon & Elisseeff, 2003). Approaches include ranking individual variables, filter methods that select features independently of the model, wrapper methods that evaluate subsets with the model, and embedded methods that select during training, such as the lasso ([[regularization-and-hyperparameters|Regularization and Hyperparameters]]). The selection itself must be validated, since it can overfit too.

#### 5. Leakage

Leakage is the introduction of information about the target that should not legitimately be available to the model; it is considered one of the top data mining mistakes and has affected major public competitions (Kaufman et al., 2012). Kaufman et al. explain leakage by explicitly defining the modelling goal and derive methodology to detect and avoid it. A common source is fitting transformations on all data before splitting; combining preprocessing and model in a pipeline that is fitted on training data only prevents this (Pedregosa et al., 2011).

#### Origin and variants

Target encoding for high-cardinality categories (Micci-Barreca, 2001), the systematic treatment of feature selection (Guyon & Elisseeff, 2003) and the formulation of leakage (Kaufman et al., 2012) are key contributions. Deep learning learns representations from raw data, but for tabular data, engineered features and tree-based models remain common ([[classical-machine-learning|Classical Machine Learning]]).

### When to use it

- When categorical variables have many distinct values, target encoding avoids very wide one-hot representations (Micci-Barreca, 2001).
- When seasonal patterns should be captured by a regression model, Fourier terms and seasonal dummies help (Hyndman & Athanasopoulos, 2021).
- When there are many candidate features, feature selection can improve performance and interpretability (Guyon & Elisseeff, 2003).

### Strengths and limitations

**Strengths**
- Target encoding makes high-cardinality categories usable for models that need numeric input (Micci-Barreca, 2001).
- Feature selection can make predictors faster, cheaper and easier to understand (Guyon & Elisseeff, 2003).
- Explicit seasonal features let simple models capture recurring patterns (Hyndman & Athanasopoulos, 2021).

**Limitations**
- Leakage can make models look excellent in evaluation and fail in use (Kaufman et al., 2012).
- Target encoding uses the target and therefore must be fitted on training data only (Micci-Barreca, 2001; Pedregosa et al., 2011).
- Feature selection performed on all data biases the evaluation (Guyon & Elisseeff, 2003).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Mathematical transformations | Change the scale or shape of numerical features (Hyndman & Athanasopoulos, 2021) | Skewed or multiplicative data |
| Target encoding | Category replaced by a smoothed target statistic (Micci-Barreca, 2001) | High-cardinality categories |
| Fourier terms and seasonal dummies | Explicit features for seasonality (Hyndman & Athanasopoulos, 2021) | Seasonal time series |
| Filter, wrapper, embedded selection | Differ in how the model is involved in the selection (Guyon & Elisseeff, 2003) | Many candidate features |

### In practice

Every feature is checked for whether it would be available at prediction time, and all fitted transformations live inside a pipeline that is refitted in each cross-validation fold (Kaufman et al., 2012; Pedregosa et al., 2011). In regulated settings, features derived from personal data must also respect data protection requirements ([[gdpr|GDPR]]).

### Key takeaway

Feature engineering makes patterns visible to a model through transformations, encodings, seasonal features and selection, and every feature must be checked for leakage.

### Sources

- Guyon, I. & Elisseeff, A. (2003). *An Introduction to Variable and Feature Selection.* JMLR 3. [JMLR](https://jmlr.org/papers/v3/guyon03a.html)
- Micci-Barreca, D. (2001). *A preprocessing scheme for high-cardinality categorical attributes in classification and prediction problems.* ACM SIGKDD Explorations 3(1). [doi:10.1145/507533.507538](https://doi.org/10.1145/507533.507538)
- Kaufman, S., Rosset, S., Perlich, C. & Stitelman, O. (2012). *Leakage in Data Mining: Formulation, Detection, and Avoidance.* ACM Transactions on Knowledge Discovery from Data 6(4). [doi:10.1145/2382577.2382579](https://doi.org/10.1145/2382577.2382579)
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12. [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html)
- Hyndman, R. J. & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3rd ed.). OTexts. [online edition](https://otexts.com/fpp3/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Feature Engineering macht aus Rohdaten Eingabevariablen, aus denen ein Modell gut lernen kann. Numerische Merkmale werden transformiert, kategoriale Merkmale kodiert, etwa per Target Encoding (Micci-Barreca, 2001), saisonale Muster ausdrücklich dargestellt (Hyndman & Athanasopoulos, 2021) und relevante Merkmale ausgewählt (Guyon & Elisseeff, 2003). Das größte Risiko ist Leakage: Merkmale, die Informationen über die Zielgröße enthalten, die beim späteren Einsatz des Modells nicht verfügbar wären (Kaufman et al., 2012).

### Funktionsweise

Rohspalten werden in Merkmale umgeformt, die die relevanten Muster für das gewählte Modell leicht erkennbar machen. Alle Transformationen, die aus Daten lernen, etwa Kodierungen oder Scaler, werden nur auf den Trainingsdaten angepasst und dann unverändert auf neue Daten angewendet.

```text
1. Transformation numerischer Merkmale
▼
2. Kodierung kategorialer Variablen
▼
3. Darstellung von Zeit und Saisonalität
▼
4. Merkmalsauswahl
▼
5. Leakage
```

#### 1. Transformation numerischer Merkmale

Mathematische Transformationen wie Logarithmen oder Box-Cox-Transformationen können Schwankungen stabilisieren und Zusammenhänge leichter modellierbar machen (Hyndman & Athanasopoulos, 2021). Die Skalierung auf vergleichbare Bereiche ist für abstands- und gradientenbasierte Verfahren wichtig ([[ml-preprocessing|Preprocessing für Machine Learning]]).

#### 2. Kodierung kategorialer Variablen

Viele Verfahren benötigen numerische Eingaben, und kategoriale Felder mit sehr vielen verschiedenen Werten sind schwer darzustellen (Micci-Barreca, 2001). Target Encoding ersetzt jede Kategorie durch eine Schätzung der Zielgröße für diese Kategorie, die per Empirical Bayes mit dem Gesamtmittel gemischt wird, damit seltenen Kategorien nicht zu viel Gewicht zukommt. Bei hierarchischen Kategorien wie Postleitzahlen lassen sich Statistiken mehrerer Aggregationsebenen kombinieren (Micci-Barreca, 2001).

#### 3. Darstellung von Zeit und Saisonalität

Für Regressionsmodelle auf Zeitreihen sind ein Trend, saisonale Dummy-Variablen und Fourier-Terme nützliche Prädiktoren; Fourier-Terme sind Paare aus Sinus- und Kosinustermen, die saisonale Muster glatt abbilden (Hyndman & Athanasopoulos, 2021; [[time-series-analysis|Zeitreihenanalyse]]).

#### 4. Merkmalsauswahl

Variablen- und Merkmalsauswahl zielt auf bessere Vorhersageleistung, schnellere und kostengünstigere Prädiktoren und ein besseres Verständnis des zugrunde liegenden Prozesses (Guyon & Elisseeff, 2003). Zu den Ansätzen gehören das Ranking einzelner Variablen, Filterverfahren, die Merkmale unabhängig vom Modell auswählen, Wrapper-Verfahren, die Teilmengen mit dem Modell bewerten, und eingebettete Verfahren, die während des Trainings auswählen, wie das Lasso ([[regularization-and-hyperparameters|Regularisierung und Hyperparameter]]). Die Auswahl selbst muss validiert werden, da auch sie überanpassen kann.

#### 5. Leakage

Leakage bezeichnet das Einbringen von Informationen über die Zielgröße, die dem Modell rechtmäßigerweise nicht zur Verfügung stehen sollten; es gilt als einer der häufigsten Fehler im Data Mining und betraf auch große öffentliche Wettbewerbe (Kaufman et al., 2012). Kaufman et al. erklären Leakage über eine ausdrückliche Definition des Modellierungsziels und leiten daraus Methoden ab, es zu erkennen und zu vermeiden. Eine häufige Ursache ist das Anpassen von Transformationen auf allen Daten vor der Aufteilung; eine Pipeline aus Vorverarbeitung und Modell, die nur auf den Trainingsdaten angepasst wird, verhindert das (Pedregosa et al., 2011).

#### Ursprung und Varianten

Target Encoding für Kategorien mit vielen Ausprägungen (Micci-Barreca, 2001), die systematische Behandlung der Merkmalsauswahl (Guyon & Elisseeff, 2003) und die Formulierung von Leakage (Kaufman et al., 2012) sind zentrale Beiträge. Deep Learning lernt Repräsentationen aus Rohdaten, doch bei tabellarischen Daten sind konstruierte Merkmale und baumbasierte Modelle weiterhin üblich ([[classical-machine-learning|Klassische ML-Verfahren]]).

### Wann einsetzen

- Wenn kategoriale Variablen sehr viele Ausprägungen haben, vermeidet Target Encoding sehr breite One-Hot-Darstellungen (Micci-Barreca, 2001).
- Wenn ein Regressionsmodell saisonale Muster erfassen soll, helfen Fourier-Terme und saisonale Dummies (Hyndman & Athanasopoulos, 2021).
- Wenn es viele Kandidatenmerkmale gibt, kann die Merkmalsauswahl Leistung und Interpretierbarkeit verbessern (Guyon & Elisseeff, 2003).

### Stärken und Grenzen

**Stärken**
- Target Encoding macht Kategorien mit vielen Ausprägungen für Modelle nutzbar, die numerische Eingaben brauchen (Micci-Barreca, 2001).
- Merkmalsauswahl kann Prädiktoren schneller, günstiger und verständlicher machen (Guyon & Elisseeff, 2003).
- Ausdrückliche saisonale Merkmale lassen einfache Modelle wiederkehrende Muster erfassen (Hyndman & Athanasopoulos, 2021).

**Einschränkungen**
- Leakage kann Modelle in der Evaluation hervorragend aussehen lassen, die im Einsatz versagen (Kaufman et al., 2012).
- Target Encoding nutzt die Zielgröße und darf daher nur auf den Trainingsdaten angepasst werden (Micci-Barreca, 2001; Pedregosa et al., 2011).
- Eine auf allen Daten durchgeführte Merkmalsauswahl verzerrt die Evaluation (Guyon & Elisseeff, 2003).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Mathematische Transformationen | Ändern Skala oder Form numerischer Merkmale (Hyndman & Athanasopoulos, 2021) | Schiefe oder multiplikative Daten |
| Target Encoding | Kategorie durch geglättete Zielstatistik ersetzt (Micci-Barreca, 2001) | Kategorien mit vielen Ausprägungen |
| Fourier-Terme und saisonale Dummies | Ausdrückliche Merkmale für Saisonalität (Hyndman & Athanasopoulos, 2021) | Saisonale Zeitreihen |
| Filter-, Wrapper- und eingebettete Auswahl | Unterscheiden sich darin, wie das Modell an der Auswahl beteiligt ist (Guyon & Elisseeff, 2003) | Viele Kandidatenmerkmale |

### In der Praxis

Für jedes Merkmal wird geprüft, ob es zum Vorhersagezeitpunkt verfügbar wäre, und alle angepassten Transformationen liegen in einer Pipeline, die in jedem Kreuzvalidierungs-Fold neu angepasst wird (Kaufman et al., 2012; Pedregosa et al., 2011). In regulierten Umgebungen müssen Merkmale, die aus personenbezogenen Daten abgeleitet sind, zudem den Datenschutzanforderungen genügen ([[gdpr|Datenschutz-Grundverordnung (DSGVO)]]).

### Merksatz

Feature Engineering macht Muster durch Transformationen, Kodierungen, saisonale Merkmale und Auswahl für ein Modell sichtbar, und jedes Merkmal muss auf Leakage geprüft werden.

### Quellen

- Guyon, I. & Elisseeff, A. (2003). *An Introduction to Variable and Feature Selection.* JMLR 3. [JMLR](https://jmlr.org/papers/v3/guyon03a.html)
- Micci-Barreca, D. (2001). *A preprocessing scheme for high-cardinality categorical attributes in classification and prediction problems.* ACM SIGKDD Explorations 3(1). [doi:10.1145/507533.507538](https://doi.org/10.1145/507533.507538)
- Kaufman, S., Rosset, S., Perlich, C. & Stitelman, O. (2012). *Leakage in Data Mining: Formulation, Detection, and Avoidance.* ACM Transactions on Knowledge Discovery from Data 6(4). [doi:10.1145/2382577.2382579](https://doi.org/10.1145/2382577.2382579)
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12. [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html)
- Hyndman, R. J. & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3rd ed.). OTexts. [online edition](https://otexts.com/fpp3/)
