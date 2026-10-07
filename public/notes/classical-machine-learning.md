---
title_en: Classical Machine Learning Methods
title_de: Klassische ML-Verfahren
entity_type: Concept
sources:
- https://hastie.su.domains/ElemStatLearn/
- https://www.statlearning.com/
- https://jmlr.org/papers/v12/pedregosa11a.html
- https://arxiv.org/abs/2207.08815
- https://arxiv.org/abs/2106.03253
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Classical machine learning comprises statistical learning methods such as linear and logistic regression, decision trees and their ensembles, support vector machines, nearest neighbours, clustering and principal component analysis (Hastie et al., 2009). It distinguishes supervised learning, where a model predicts a known response, from unsupervised learning, where it finds structure in unlabelled data (James et al., 2021). On medium-sized tabular data, tree-based ensembles still outperform deep learning (Grinsztajn et al., 2022).

### How it works

A method is chosen for the task, fitted to training data and assessed on data it has not seen. Both steps share the same building blocks across methods: a model family, a loss or objective, and a way to estimate prediction error.

```text
1. Supervised and unsupervised learning
▼
2. Families of methods
▼
3. Model assessment and the bias-variance trade-off
▼
4. Common tooling
▼
5. Classical methods versus deep learning on tabular data
```

#### 1. Supervised and unsupervised learning

In supervised learning each observation comes with a response, and the model learns to predict it from the inputs: a number in regression, a class in [[classification|Classification]]. In unsupervised learning there is no response, and the goal is to find structure, for example groups of similar observations ([[clustering|Clustering]]) or a lower-dimensional representation ([[principal-component-analysis|Principal Component Analysis]]) (James et al., 2021).

#### 2. Families of methods

The standard textbooks cover linear methods for regression and classification, [[decision-trees|Decision Trees]], boosting and random forests ([[ensemble-methods|Ensemble Methods]]), [[support-vector-machines|Support Vector Machines]] and [[k-nearest-neighbors|k-Nearest Neighbors]] for supervised learning, and clustering and principal components for unsupervised learning (Hastie et al., 2009; James et al., 2021). They also include neural networks, which share the same framework of models, losses and error estimation.

#### 3. Model assessment and the bias-variance trade-off

The prediction error of a model is framed through the bias-variance trade-off: flexible models fit the training data closely but vary strongly with the sample, rigid models are stable but may miss structure (Hastie et al., 2009). Models are therefore assessed and selected on data not used for fitting, with cross-validation and the bootstrap ([[ml-preprocessing|ML Preprocessing]]).

#### 4. Common tooling

scikit-learn is a Python module that integrates a wide range of machine learning algorithms for medium-scale supervised and unsupervised problems, with an emphasis on ease of use, performance, documentation and API consistency (Pedregosa et al., 2011). Its consistent interface makes it easy to try several classical methods on the same data.

#### 5. Classical methods versus deep learning on tabular data

On a benchmark of 45 tabular datasets, tree-based models such as XGBoost and random forests remained state of the art on medium-sized data of about 10,000 samples, even without accounting for their superior speed (Grinsztajn et al., 2022). The authors derive challenges for tabular neural networks: be robust to uninformative features, preserve the orientation of the data, and learn irregular functions easily. In a second comparison, XGBoost outperformed recently proposed deep models for tabular data across datasets, including the datasets used in the papers proposing them, and needed much less tuning; an ensemble of deep models and XGBoost performed best (Shwartz-Ziv & Armon, 2021).

#### Origin and variants

The statistical learning textbooks (Hastie et al., 2009; James et al., 2021) systematise the field. scikit-learn made the methods widely available (Pedregosa et al., 2011), and recent benchmarks compare them with deep learning on tabular data (Grinsztajn et al., 2022; Shwartz-Ziv & Armon, 2021).

### When to use it

- When the data is tabular and of medium size, tree-based ensembles are a strong first choice (Grinsztajn et al., 2022).
- When a model must be tuned with limited effort, XGBoost needed much less tuning than deep tabular models (Shwartz-Ziv & Armon, 2021).
- When no labels are available and the goal is to find groups or reduce dimensionality, unsupervised methods apply (James et al., 2021).

### Strengths and limitations

**Strengths**
- Tree-based models remain state of the art on medium-sized tabular data and are fast (Grinsztajn et al., 2022).
- Mature, consistent open-source implementations exist (Pedregosa et al., 2011).
- A common framework of bias, variance and cross-validation applies across methods (Hastie et al., 2009).

**Limitations**
- Tree-based models' advantage was shown for medium-sized tabular data, not for text or images (Grinsztajn et al., 2022).
- Deep tabular models claimed to beat XGBoost did not do so in an independent comparison, so published claims need checking on one's own data (Shwartz-Ziv & Armon, 2021).
- Flexible models overfit without careful assessment on held-out data (Hastie et al., 2009).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Linear and logistic models | Simple, interpretable relationship between inputs and response (Hastie et al., 2009) | Baselines, interpretable models |
| Tree ensembles (random forests, boosting) | Many trees combined; robust to uninformative features (Grinsztajn et al., 2022) | Medium-sized tabular data |
| Deep learning | Learns representations; on tabular data often behind tree ensembles (Grinsztajn et al., 2022; Shwartz-Ziv & Armon, 2021) | Text, images, very large datasets |
| Unsupervised methods | No response; find clusters or low-dimensional structure (James et al., 2021) | Exploration, preprocessing |

### In practice

A simple baseline and a tree ensemble are usually fitted first and compared with cross-validation before more complex models are tried (Hastie et al., 2009; Grinsztajn et al., 2022). Libraries such as scikit-learn provide the common steps from preprocessing to evaluation (Pedregosa et al., 2011). For text and images, neural networks are the usual choice instead ([[neural-networks|Neural Networks]]).

### Key takeaway

Classical machine learning provides well-understood supervised and unsupervised methods, and on medium-sized tabular data tree-based ensembles remain the strongest choice.

### Sources

- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [book website](https://hastie.su.domains/ElemStatLearn/)
- James, G., Witten, D., Hastie, T. & Tibshirani, R. (2021). *An Introduction to Statistical Learning* (2nd ed.). Springer. [book website](https://www.statlearning.com/)
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12. [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html)
- Grinsztajn, L. et al. (2022). *Why do tree-based models still outperform deep learning on tabular data?* NeurIPS 2022 Datasets and Benchmarks. [arXiv:2207.08815](https://arxiv.org/abs/2207.08815)
- Shwartz-Ziv, R. & Armon, A. (2021). *Tabular Data: Deep Learning is Not All You Need.* [arXiv:2106.03253](https://arxiv.org/abs/2106.03253)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Klassisches maschinelles Lernen umfasst statistische Lernverfahren wie lineare und logistische Regression, Entscheidungsbäume und ihre Ensembles, Support Vector Machines, Nächste-Nachbarn-Verfahren, Clustering und Hauptkomponentenanalyse (Hastie et al., 2009). Es unterscheidet überwachtes Lernen, bei dem ein Modell eine bekannte Zielgröße vorhersagt, von unüberwachtem Lernen, bei dem es Strukturen in nicht gelabelten Daten findet (James et al., 2021). Auf mittelgroßen tabellarischen Daten übertreffen baumbasierte Ensembles Deep Learning weiterhin (Grinsztajn et al., 2022).

### Funktionsweise

Für die Aufgabe wird ein Verfahren gewählt, an Trainingsdaten angepasst und auf Daten bewertet, die es nicht gesehen hat. Beide Schritte nutzen über alle Verfahren hinweg dieselben Bausteine: eine Modellfamilie, eine Verlust- oder Zielfunktion und eine Schätzung des Vorhersagefehlers.

```text
1. Überwachtes und unüberwachtes Lernen
▼
2. Verfahrensfamilien
▼
3. Modellbewertung und Bias-Varianz-Abwägung
▼
4. Gängige Werkzeuge
▼
5. Klassische Verfahren und Deep Learning auf tabellarischen Daten
```

#### 1. Überwachtes und unüberwachtes Lernen

Beim überwachten Lernen gehört zu jeder Beobachtung eine Zielgröße, und das Modell lernt, sie aus den Eingaben vorherzusagen: eine Zahl bei der Regression, eine Klasse bei der [[classification|Klassifikation]]. Beim unüberwachten Lernen gibt es keine Zielgröße; gesucht sind Strukturen, etwa Gruppen ähnlicher Beobachtungen ([[clustering|Clustering]]) oder eine niedrigdimensionale Darstellung ([[principal-component-analysis|Hauptkomponentenanalyse (PCA)]]) (James et al., 2021).

#### 2. Verfahrensfamilien

Die Standardlehrbücher behandeln für überwachtes Lernen lineare Verfahren für Regression und Klassifikation, [[decision-trees|Entscheidungsbäume]], Boosting und Random Forests ([[ensemble-methods|Ensemble-Methoden]]), [[support-vector-machines|Support Vector Machines]] und [[k-nearest-neighbors|k-Nearest Neighbors]], für unüberwachtes Lernen Clustering und Hauptkomponenten (Hastie et al., 2009; James et al., 2021). Auch neuronale Netze gehören dazu; sie teilen denselben Rahmen aus Modellen, Verlustfunktionen und Fehlerschätzung.

#### 3. Modellbewertung und Bias-Varianz-Abwägung

Der Vorhersagefehler eines Modells wird über die Bias-Varianz-Abwägung beschrieben: Flexible Modelle passen sich den Trainingsdaten eng an, schwanken aber stark mit der Stichprobe; starre Modelle sind stabil, übersehen aber womöglich Strukturen (Hastie et al., 2009). Modelle werden daher auf Daten bewertet und ausgewählt, die nicht zur Anpassung dienten, mit Kreuzvalidierung und Bootstrap ([[ml-preprocessing|Preprocessing für Machine Learning]]).

#### 4. Gängige Werkzeuge

scikit-learn ist ein Python-Modul, das viele Verfahren des maschinellen Lernens für überwachte und unüberwachte Probleme mittlerer Größe bündelt, mit Schwerpunkt auf Benutzerfreundlichkeit, Leistung, Dokumentation und einer konsistenten API (Pedregosa et al., 2011). Die einheitliche Schnittstelle erleichtert es, mehrere klassische Verfahren auf denselben Daten zu erproben.

#### 5. Klassische Verfahren und Deep Learning auf tabellarischen Daten

In einem Benchmark mit 45 tabellarischen Datensätzen blieben baumbasierte Modelle wie XGBoost und Random Forests bei mittelgroßen Daten von etwa 10.000 Beispielen der Stand der Technik, selbst ohne ihre höhere Geschwindigkeit einzurechnen (Grinsztajn et al., 2022). Die Autoren leiten Anforderungen an tabellarische neuronale Netze ab: robust gegenüber uninformativen Merkmalen sein, die Ausrichtung der Daten erhalten und unregelmäßige Funktionen leicht lernen. In einem zweiten Vergleich übertraf XGBoost neu vorgeschlagene Deep-Learning-Modelle für Tabellendaten auf allen Datensätzen, auch auf denen aus den Originalarbeiten, und brauchte deutlich weniger Tuning; am besten schnitt ein Ensemble aus Deep-Learning-Modellen und XGBoost ab (Shwartz-Ziv & Armon, 2021).

#### Ursprung und Varianten

Die Lehrbücher zum statistischen Lernen (Hastie et al., 2009; James et al., 2021) systematisieren das Gebiet. scikit-learn machte die Verfahren breit verfügbar (Pedregosa et al., 2011), und neuere Benchmarks vergleichen sie mit Deep Learning auf tabellarischen Daten (Grinsztajn et al., 2022; Shwartz-Ziv & Armon, 2021).

### Wann einsetzen

- Bei tabellarischen Daten mittlerer Größe sind baumbasierte Ensembles eine starke erste Wahl (Grinsztajn et al., 2022).
- Wenn ein Modell mit begrenztem Aufwand abgestimmt werden soll: XGBoost brauchte deutlich weniger Tuning als tabellarische Deep-Learning-Modelle (Shwartz-Ziv & Armon, 2021).
- Wenn keine Labels vorliegen und Gruppen gefunden oder Dimensionen reduziert werden sollen, kommen unüberwachte Verfahren infrage (James et al., 2021).

### Stärken und Grenzen

**Stärken**
- Baumbasierte Modelle sind auf mittelgroßen tabellarischen Daten Stand der Technik und schnell (Grinsztajn et al., 2022).
- Es gibt ausgereifte, konsistente Open-Source-Implementierungen (Pedregosa et al., 2011).
- Ein gemeinsamer Rahmen aus Bias, Varianz und Kreuzvalidierung gilt für alle Verfahren (Hastie et al., 2009).

**Einschränkungen**
- Der Vorsprung baumbasierter Modelle wurde für mittelgroße tabellarische Daten gezeigt, nicht für Text oder Bilder (Grinsztajn et al., 2022).
- Tabellarische Deep-Learning-Modelle, die XGBoost angeblich schlagen, taten das in einem unabhängigen Vergleich nicht; veröffentlichte Ergebnisse sollten daher auf eigenen Daten geprüft werden (Shwartz-Ziv & Armon, 2021).
- Flexible Modelle überanpassen ohne sorgfältige Bewertung auf zurückgehaltenen Daten (Hastie et al., 2009).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Lineare und logistische Modelle | Einfacher, interpretierbarer Zusammenhang zwischen Eingaben und Zielgröße (Hastie et al., 2009) | Baselines, interpretierbare Modelle |
| Baum-Ensembles (Random Forests, Boosting) | Viele kombinierte Bäume; robust gegenüber uninformativen Merkmalen (Grinsztajn et al., 2022) | Mittelgroße tabellarische Daten |
| Deep Learning | Lernt Repräsentationen; auf Tabellendaten oft hinter Baum-Ensembles (Grinsztajn et al., 2022; Shwartz-Ziv & Armon, 2021) | Text, Bilder, sehr große Datensätze |
| Unüberwachte Verfahren | Keine Zielgröße; finden Cluster oder niedrigdimensionale Strukturen (James et al., 2021) | Exploration, Vorverarbeitung |

### In der Praxis

Meist werden zuerst eine einfache Baseline und ein Baum-Ensemble angepasst und per Kreuzvalidierung verglichen, bevor komplexere Modelle zum Einsatz kommen (Hastie et al., 2009; Grinsztajn et al., 2022). Bibliotheken wie scikit-learn decken die üblichen Schritte von der Vorverarbeitung bis zur Evaluation ab (Pedregosa et al., 2011). Für Text und Bilder sind dagegen neuronale Netze die übliche Wahl ([[neural-networks|Neuronale Netze]]).

### Merksatz

Klassisches maschinelles Lernen bietet gut verstandene überwachte und unüberwachte Verfahren, und auf mittelgroßen tabellarischen Daten bleiben baumbasierte Ensembles die stärkste Wahl.

### Quellen

- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [book website](https://hastie.su.domains/ElemStatLearn/)
- James, G., Witten, D., Hastie, T. & Tibshirani, R. (2021). *An Introduction to Statistical Learning* (2nd ed.). Springer. [book website](https://www.statlearning.com/)
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12. [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html)
- Grinsztajn, L. et al. (2022). *Why do tree-based models still outperform deep learning on tabular data?* NeurIPS 2022 Datasets and Benchmarks. [arXiv:2207.08815](https://arxiv.org/abs/2207.08815)
- Shwartz-Ziv, R. & Armon, A. (2021). *Tabular Data: Deep Learning is Not All You Need.* [arXiv:2106.03253](https://arxiv.org/abs/2106.03253)
