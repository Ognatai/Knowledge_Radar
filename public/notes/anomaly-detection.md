---
title_en: Anomaly Detection
title_de: Anomalieerkennung
entity_type: Method
aliases:
- Anomaly detection
- Outlier detection
- Novelty detection
- Isolation Forest
- Local Outlier Factor
- LOF
- One-class classification
- Anomalieerkennung
- Ausreißererkennung
sources:
- https://arxiv.org/abs/2009.11732
- https://scikit-learn.org/stable/modules/outlier_detection.html
- https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Anomaly detection finds observations that deviate from the normal pattern of the data, such as fraudulent card transactions, damaged products or unusual network traffic (Liu et al., 2008; Ruff et al., 2021). Because anomalies are rare and usually unlabelled, most methods model what is normal and score how far a new observation lies from it: by density, distance to neighbours, a learned boundary around normal data or reconstruction error (Ruff et al., 2021). Isolation Forest takes the opposite route and isolates anomalies directly with random splits, which makes it fast on large data (Liu et al., 2008). [[scikit-learn|scikit-learn]] distinguishes outlier detection, where the training data is contaminated, from novelty detection, where it is clean (scikit-learn).

### How it works

```text
data (mostly normal, few or no labelled anomalies)
   ▼
choose a model of normality
   density / probabilistic   │  distance / neighbours (LOF)  │  one-class boundary (OC-SVM, SVDD)
   reconstruction (PCA, autoencoder)  │  isolation (Isolation Forest)
   ▼
anomaly score s(x) for every observation
   ▼
threshold (e.g. from expected contamination) ──► anomaly / normal ──► review, alert, retrain
```

#### 1. Kinds of anomalies

A point anomaly is a single unusual observation, such as an illegal transaction; a contextual anomaly is unusual only in its context, such as a spike in an otherwise normal [[time-series-analysis|time series]] whose value lies within the normal global range; a group or collective anomaly is a set of related points that is anomalous together, such as a cluster of related network attacks (Ruff et al., 2021).

#### 2. Settings: unsupervised, semi-supervised, supervised

Labelled anomalies are usually rare or missing and rarely cover all kinds of abnormality, so most methods are unsupervised (Ruff et al., 2021). scikit-learn calls the case with contaminated training data outlier detection or unsupervised anomaly detection, and the case with clean training data novelty detection or semi-supervised anomaly detection; in outlier detection the anomalies must not form a dense cluster, because the estimators assume they lie in low-density regions (scikit-learn). When labelled anomalies exist, the problem becomes heavily imbalanced [[classification|classification]] (Ruff et al., 2021).

#### 3. Model families

Ruff et al. (2021) organise methods into probabilistic models, which estimate the density of normal data and flag low-density points; one-class classification, which learns a boundary around normal data directly, such as the one-class SVM or support vector data description; and reconstruction models, such as [[principal-component-analysis|PCA]] or [[autoencoders-and-gans|autoencoders]], which flag points they reconstruct badly; each has shallow and deep variants. Distance-based methods such as the Local Outlier Factor compare a point's local density, estimated from its k nearest neighbours, with that of its neighbours: the score is the ratio of the neighbours' average local density to the point's own, so points in much sparser regions than their neighbours stand out (scikit-learn; [[k-nearest-neighbours|k-nearest neighbours]]).

#### 4. Isolation Forest

Anomalies are "few and different", so they are easier to isolate than normal points (Liu et al., 2008). Isolation Forest builds random trees that repeatedly pick a feature and a random split value between its minimum and maximum; the number of splits needed to isolate a point equals its path length, and averaged over the forest, short paths indicate anomalies (Liu et al., 2008; scikit-learn). Each tree is built on a small random subsample with height limit `⌈log₂ ψ⌉` for subsample size ψ, which gives linear time with low memory, works with many irrelevant attributes and even without anomalies in the training set, and performed favourably against LOF, ORCA and random forests in AUC and speed (Liu et al., 2008; [[ensemble-methods|ensemble methods]]).

#### 5. Scores and thresholds

Most methods output a continuous anomaly score; a binary detector follows from a threshold, which can be derived from the empirical distribution of scores (Ruff et al., 2021). In scikit-learn, `predict` labels inliers 1 and outliers −1 based on a threshold set through the `contamination` parameter, while `score_samples` and `decision_function` expose the raw scores (scikit-learn).

#### Origin and variants

Classic approaches include PCA, the one-class SVM, support vector data description and nearest-neighbour methods; deep variants include deep autoencoders, deep one-class classification and generative models (Ruff et al., 2021). Isolation Forest was presented at ICDM 2008 (Liu et al., 2008).

### When to use it

- Fraud and intrusion detection, where anomalies are rare and labels scarce (Liu et al., 2008; Ruff et al., 2021).
- [[quality-control|Quality control]] in manufacturing, for example images of damaged products (Ruff et al., 2021).
- Monitoring metrics and time series, where time-series anomalies are the most prominent contextual anomalies (Ruff et al., 2021; [[monitoring-and-alerting|monitoring and alerting]]).
- Cleaning data sets before training other models (scikit-learn; [[ml-preprocessing|preprocessing]]).

### Strengths and limitations

**Strengths**
- Works without labelled anomalies (Ruff et al., 2021).
- Isolation Forest scales linearly and handles high-dimensional data with irrelevant attributes (Liu et al., 2008).
- Scores can be ranked for human review instead of forcing a hard decision (Ruff et al., 2021).

**Limitations**
- Detection in high dimensions or without assumptions on the normal distribution is very challenging (scikit-learn).
- The one-class SVM is sensitive to outliers in the training data and needs careful tuning (scikit-learn).
- The threshold, or the assumed contamination, decides how many alarms are raised (scikit-learn; Ruff et al., 2021).
- Training data is often noisy or contaminated, which violates the assumption that it is all normal (Ruff et al., 2021).

### Comparison

| Method | Idea | Note |
|---|---|---|
| Density estimation | low probability = anomalous | needs a good density model |
| Local Outlier Factor | lower local density than neighbours | moderately high dimensions (scikit-learn) |
| One-class SVM | boundary around normal data | sensitive to outliers in training data |
| Reconstruction (PCA, autoencoder) | high reconstruction error | learns normal structure |
| Isolation Forest | short random isolation paths | fast, large and high-dimensional data |
| Supervised classifier | learn from labelled anomalies | only if labels exist; imbalanced |

Sources: Ruff et al. (2021), scikit-learn, Liu et al. (2008).

### In practice

scikit-learn's comparison found Isolation Forest and LOF to perform reasonably well on its toy data sets, while the one-class SVM did not perform very well for outlier detection (scikit-learn). Evaluation uses held-out labelled anomalies where available, for example with ROC curves ([[classification-metrics|classification metrics]]; scikit-learn). With LOF for novelty detection, scores must only be computed on new data, not on the training samples (scikit-learn).

### Key takeaway

Anomaly detection models normality and scores deviation from it, by density, neighbours, boundaries, reconstruction or isolation; without labels, the choice of method and threshold determines what counts as an anomaly.

### Sources

- Ruff, L. et al. (2021). *A Unifying Review of Deep and Shallow Anomaly Detection.* Proceedings of the IEEE. [arXiv:2009.11732](https://arxiv.org/abs/2009.11732)
- scikit-learn developers. *Novelty and Outlier Detection.* scikit-learn documentation. [scikit-learn.org](https://scikit-learn.org/stable/modules/outlier_detection.html)
- Liu, F. T., Ting, K. M. & Zhou, Z.-H. (2008). *Isolation Forest.* ICDM 2008. [cs.nju.edu.cn](https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die Anomalieerkennung findet Beobachtungen, die vom normalen Muster der Daten abweichen, etwa betrügerische Kartentransaktionen, beschädigte Produkte oder ungewöhnlichen Netzwerkverkehr (Liu et al., 2008; Ruff et al., 2021). Weil Anomalien selten und meist nicht gelabelt sind, modellieren die meisten Verfahren, was normal ist, und bewerten, wie weit eine neue Beobachtung davon entfernt liegt: über Dichte, Abstand zu Nachbarn, eine gelernte Grenze um die normalen Daten oder den Rekonstruktionsfehler (Ruff et al., 2021). Isolation Forest geht den umgekehrten Weg und isoliert Anomalien direkt mit zufälligen Teilungen, was es auf großen Daten schnell macht (Liu et al., 2008). [[scikit-learn|scikit-learn]] unterscheidet die Ausreißererkennung, bei der die Trainingsdaten verunreinigt sind, von der Novelty Detection, bei der sie sauber sind (scikit-learn).

### Funktionsweise

```text
Daten (überwiegend normal, wenige oder keine gelabelten Anomalien)
   ▼
Modell der Normalität wählen
   Dichte / probabilistisch   │  Abstand / Nachbarn (LOF)  │  One-Class-Grenze (OC-SVM, SVDD)
   Rekonstruktion (PCA, Autoencoder)  │  Isolation (Isolation Forest)
   ▼
Anomalie-Score s(x) für jede Beobachtung
   ▼
Schwelle (z. B. aus erwarteter Verunreinigung) ──► Anomalie / normal ──► prüfen, alarmieren, neu trainieren
```

#### 1. Arten von Anomalien

Eine Punktanomalie ist eine einzelne ungewöhnliche Beobachtung, etwa eine illegale Transaktion; eine kontextuelle Anomalie ist nur in ihrem Kontext ungewöhnlich, etwa ein Ausschlag in einer sonst normalen [[time-series-analysis|Zeitreihe]], dessen Wert im normalen Gesamtbereich liegt; eine Gruppen- oder kollektive Anomalie ist eine Menge zusammenhängender Punkte, die gemeinsam anomal ist, etwa eine Häufung verwandter Netzwerkangriffe (Ruff et al., 2021).

#### 2. Settings: unüberwacht, semi-überwacht, überwacht

Gelabelte Anomalien sind meist selten oder fehlen und decken selten alle Arten von Abweichung ab, weshalb die meisten Verfahren unüberwacht sind (Ruff et al., 2021). scikit-learn nennt den Fall mit verunreinigten Trainingsdaten Ausreißererkennung oder unüberwachte Anomalieerkennung und den Fall mit sauberen Trainingsdaten Novelty Detection oder semi-überwachte Anomalieerkennung; bei der Ausreißererkennung dürfen die Anomalien keinen dichten Cluster bilden, weil die Schätzer annehmen, dass sie in Regionen geringer Dichte liegen (scikit-learn). Gibt es gelabelte Anomalien, wird das Problem zu einer stark unausgeglichenen [[classification|Klassifikation]] (Ruff et al., 2021).

#### 3. Familien von Verfahren

Ruff et al. (2021) ordnen die Verfahren in probabilistische Modelle, die die Dichte normaler Daten schätzen und Punkte geringer Dichte markieren; One-Class-Klassifikation, die direkt eine Grenze um die normalen Daten lernt, etwa die One-Class-SVM oder Support Vector Data Description; und Rekonstruktionsmodelle wie [[principal-component-analysis|PCA]] oder [[autoencoders-and-gans|Autoencoder]], die Punkte markieren, die sie schlecht rekonstruieren; zu jeder Familie gibt es flache und tiefe Varianten. Abstandsbasierte Verfahren wie der Local Outlier Factor vergleichen die lokale Dichte eines Punktes, geschätzt aus seinen k nächsten Nachbarn, mit der seiner Nachbarn: Der Score ist das Verhältnis der mittleren lokalen Dichte der Nachbarn zur eigenen, sodass Punkte in viel dünneren Regionen als ihre Nachbarn auffallen (scikit-learn; [[k-nearest-neighbours|k-nächste Nachbarn]]).

#### 4. Isolation Forest

Anomalien sind „wenige und andersartig“ und daher leichter zu isolieren als normale Punkte (Liu et al., 2008). Isolation Forest baut Zufallsbäume, die wiederholt ein Merkmal und einen zufälligen Teilungswert zwischen dessen Minimum und Maximum wählen; die Zahl der Teilungen bis zur Isolation eines Punktes entspricht seiner Pfadlänge, und gemittelt über den Wald deuten kurze Pfade auf Anomalien (Liu et al., 2008; scikit-learn). Jeder Baum entsteht auf einer kleinen Zufallsstichprobe mit Höhenbegrenzung `⌈log₂ ψ⌉` bei Stichprobengröße ψ; das ergibt lineare Laufzeit bei geringem Speicherbedarf, funktioniert mit vielen irrelevanten Attributen und sogar ohne Anomalien in den Trainingsdaten und schnitt gegenüber LOF, ORCA und Random Forests bei AUC und Geschwindigkeit günstig ab (Liu et al., 2008; [[ensemble-methods|Ensemble-Verfahren]]).

#### 5. Scores und Schwellen

Die meisten Verfahren liefern einen kontinuierlichen Anomalie-Score; ein binärer Detektor ergibt sich über eine Schwelle, die sich aus der empirischen Verteilung der Scores ableiten lässt (Ruff et al., 2021). In scikit-learn kennzeichnet `predict` normale Punkte mit 1 und Ausreißer mit −1 anhand einer über den Parameter `contamination` gesetzten Schwelle, während `score_samples` und `decision_function` die rohen Scores liefern (scikit-learn).

#### Ursprung und Varianten

Zu den klassischen Ansätzen gehören PCA, die One-Class-SVM, Support Vector Data Description und Nachbarschaftsverfahren; tiefe Varianten umfassen tiefe Autoencoder, tiefe One-Class-Klassifikation und generative Modelle (Ruff et al., 2021). Isolation Forest wurde auf der ICDM 2008 vorgestellt (Liu et al., 2008).

### Wann einsetzen

- Betrugs- und Einbruchserkennung, bei der Anomalien selten und Labels knapp sind (Liu et al., 2008; Ruff et al., 2021).
- [[quality-control|Qualitätskontrolle]] in der Fertigung, etwa Bilder beschädigter Produkte (Ruff et al., 2021).
- Überwachung von Metriken und Zeitreihen, wobei Zeitreihenanomalien das bekannteste Beispiel kontextueller Anomalien sind (Ruff et al., 2021; [[monitoring-and-alerting|Monitoring und Alerting]]).
- Datensätze bereinigen, bevor andere Modelle trainiert werden (scikit-learn; [[ml-preprocessing|Vorverarbeitung]]).

### Stärken und Grenzen

**Stärken**
- Funktioniert ohne gelabelte Anomalien (Ruff et al., 2021).
- Isolation Forest skaliert linear und kommt mit hochdimensionalen Daten und irrelevanten Attributen zurecht (Liu et al., 2008).
- Scores lassen sich für die menschliche Prüfung ordnen, statt eine harte Entscheidung zu erzwingen (Ruff et al., 2021).

**Grenzen**
- Erkennung in hohen Dimensionen oder ohne Annahmen über die normale Verteilung ist sehr schwierig (scikit-learn).
- Die One-Class-SVM reagiert empfindlich auf Ausreißer in den Trainingsdaten und braucht sorgfältiges Tuning (scikit-learn).
- Die Schwelle oder die angenommene Verunreinigung entscheidet, wie viele Alarme ausgelöst werden (scikit-learn; Ruff et al., 2021).
- Trainingsdaten sind oft verrauscht oder verunreinigt, was der Annahme widerspricht, dass alles normal ist (Ruff et al., 2021).

### Vergleich

| Verfahren | Idee | Bemerkung |
|---|---|---|
| Dichteschätzung | geringe Wahrscheinlichkeit = anomal | braucht ein gutes Dichtemodell |
| Local Outlier Factor | geringere lokale Dichte als die Nachbarn | mäßig hohe Dimensionen (scikit-learn) |
| One-Class-SVM | Grenze um normale Daten | empfindlich gegenüber Ausreißern im Training |
| Rekonstruktion (PCA, Autoencoder) | hoher Rekonstruktionsfehler | lernt normale Struktur |
| Isolation Forest | kurze zufällige Isolationspfade | schnell, große und hochdimensionale Daten |
| Überwachter Klassifikator | aus gelabelten Anomalien lernen | nur wenn Labels existieren; unausgeglichen |

Quellen: Ruff et al. (2021), scikit-learn, Liu et al. (2008).

### In der Praxis

Im Vergleich von scikit-learn schnitten Isolation Forest und LOF auf den Spielzeugdatensätzen ordentlich ab, während die One-Class-SVM für die Ausreißererkennung nicht sehr gut funktionierte (scikit-learn). Die Evaluation nutzt zurückgehaltene gelabelte Anomalien, wo vorhanden, etwa mit ROC-Kurven ([[classification-metrics|Klassifikationsmetriken]]; scikit-learn). Beim LOF für Novelty Detection dürfen Scores nur auf neuen Daten berechnet werden, nicht auf den Trainingsbeispielen (scikit-learn).

### Merksatz

Die Anomalieerkennung modelliert Normalität und bewertet Abweichungen davon, über Dichte, Nachbarn, Grenzen, Rekonstruktion oder Isolation; ohne Labels bestimmen Verfahren und Schwelle, was als Anomalie gilt.

### Quellen

- Ruff, L. et al. (2021). *A Unifying Review of Deep and Shallow Anomaly Detection.* Proceedings of the IEEE. [arXiv:2009.11732](https://arxiv.org/abs/2009.11732)
- scikit-learn developers. *Novelty and Outlier Detection.* scikit-learn-Dokumentation. [scikit-learn.org](https://scikit-learn.org/stable/modules/outlier_detection.html)
- Liu, F. T., Ting, K. M. & Zhou, Z.-H. (2008). *Isolation Forest.* ICDM 2008. [cs.nju.edu.cn](https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf)
