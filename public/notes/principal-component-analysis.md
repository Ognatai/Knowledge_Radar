---
title_en: Principal Component Analysis (PCA)
title_de: Hauptkomponentenanalyse (PCA)
entity_type: Method
sources:
- https://doi.org/10.1080/14786440109462720
- https://doi.org/10.1098/rsta.2015.0202
- https://arxiv.org/abs/1404.1100
- https://doi.org/10.1126/science.1127647
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Principal component analysis (PCA) reduces the dimensionality of data by replacing the original variables with new, uncorrelated variables, the principal components, which successively capture as much of the variance as possible (Jolliffe & Cadima, 2016). Finding them reduces to an eigenvalue problem. PCA is linear; deep autoencoders can learn non-linear low-dimensional codes that worked much better than PCA in experiments (Hinton & Salakhutdinov, 2006).

### How it works

The data is centred, a covariance or correlation matrix is computed, and its eigenvectors give the directions of the principal components, ordered by the variance they capture. Projecting the data onto the first few components gives a lower-dimensional representation.

```text
1. Best-fitting lines and planes
▼
2. Components that maximise variance
▼
3. Scaling: covariance or correlation matrix
▼
4. Choosing the number of components
▼
5. Non-linear alternative: autoencoders
```

#### 1. Best-fitting lines and planes

PCA goes back to Pearson (1901), who determined the lines and planes that best fit a system of points in space in the least-squares sense, i.e. by minimising the perpendicular distances of the points. The first principal component is the line of closest fit.

#### 2. Components that maximise variance

PCA creates new variables that are uncorrelated and successively maximise variance, which reduces dimensionality while minimising information loss (Jolliffe & Cadima, 2016). Finding these principal components reduces to solving an eigenvalue/eigenvector problem, and because the components are derived from the data at hand rather than fixed in advance, PCA is an adaptive data analysis technique. Shlens (2014) derives the mathematics step by step from simple intuitions.

#### 3. Scaling: covariance or correlation matrix

PCA on the covariance matrix depends on the units of the variables, so variables with large values dominate the first components. Using the correlation matrix instead corresponds to standardising all variables first; which choice is appropriate depends on whether the variables are measured on comparable scales (Jolliffe & Cadima, 2016; [[ml-preprocessing|ML Preprocessing]]).

#### 4. Choosing the number of components

Each component captures a share of the total variance, and the shares decrease from component to component. The number of components to keep is chosen by how much of the variance should be retained (Jolliffe & Cadima, 2016; Shlens, 2014).

#### 5. Non-linear alternative: autoencoders

An autoencoder is a neural network with a small central layer that is trained to reconstruct its inputs, so that the central layer learns a low-dimensional code (Hinton & Salakhutdinov, 2006). With a suitable weight initialisation, deep autoencoders learned codes that worked much better than PCA as a tool to reduce dimensionality ([[autoencoders-and-gans|Autoencoders and GANs]]).

#### Origin and variants

PCA goes back to Pearson (1901). Jolliffe & Cadima (2016) review the method and its variants for different data types, Shlens (2014) offers a tutorial derivation, and autoencoders (Hinton & Salakhutdinov, 2006) provide a non-linear alternative.

### When to use it

- When many correlated variables should be summarised by a few uncorrelated ones (Jolliffe & Cadima, 2016).
- When data should be visualised or prepared for distance-based methods such as clustering or k-NN ([[clustering|Clustering]], [[k-nearest-neighbors|k-Nearest Neighbors]]).
- When structure in the data is strongly non-linear, an autoencoder may be the better choice (Hinton & Salakhutdinov, 2006).

### Strengths and limitations

**Strengths**
- Reduces dimensionality while minimising information loss (Jolliffe & Cadima, 2016).
- Computed by a standard eigenvalue problem, without iterative training (Jolliffe & Cadima, 2016).
- The components are uncorrelated and ordered by importance (Jolliffe & Cadima, 2016).

**Limitations**
- Results depend on the scaling of the variables (Jolliffe & Cadima, 2016).
- PCA captures only linear structure; deep autoencoders learned better low-dimensional codes (Hinton & Salakhutdinov, 2006).
- Principal components are combinations of all original variables and can be hard to interpret (Jolliffe & Cadima, 2016).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| PCA on the covariance matrix | Uses the original units (Jolliffe & Cadima, 2016) | Variables on comparable scales |
| PCA on the correlation matrix | Equivalent to standardising first (Jolliffe & Cadima, 2016) | Variables in different units |
| Autoencoder | Non-linear code learned by a neural network (Hinton & Salakhutdinov, 2006) | Strongly non-linear structure |

### In practice

Variables measured in different units are standardised before PCA (Jolliffe & Cadima, 2016). The PCA transformation is fitted on the training data only and then applied to validation and test data, to avoid leakage ([[feature-engineering|Feature Engineering]]). The retained variance is reported together with the chosen number of components.

### Key takeaway

PCA replaces many correlated variables with a few uncorrelated components that capture most of the variance; it is fast and linear but depends on how the variables are scaled.

### Sources

- Pearson, K. (1901). *On Lines and Planes of Closest Fit to Systems of Points in Space.* Philosophical Magazine 2(11). [doi:10.1080/14786440109462720](https://doi.org/10.1080/14786440109462720)
- Jolliffe, I. T. & Cadima, J. (2016). *Principal component analysis: a review and recent developments.* Philosophical Transactions of the Royal Society A 374(2065). [doi:10.1098/rsta.2015.0202](https://doi.org/10.1098/rsta.2015.0202)
- Shlens, J. (2014). *A Tutorial on Principal Component Analysis.* [arXiv:1404.1100](https://arxiv.org/abs/1404.1100)
- Hinton, G. E. & Salakhutdinov, R. R. (2006). *Reducing the Dimensionality of Data with Neural Networks.* Science 313(5786). [doi:10.1126/science.1127647](https://doi.org/10.1126/science.1127647)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die Hauptkomponentenanalyse (PCA) reduziert die Dimension von Daten, indem sie die ursprünglichen Variablen durch neue, unkorrelierte Variablen ersetzt, die Hauptkomponenten, die nacheinander möglichst viel der Varianz erfassen (Jolliffe & Cadima, 2016). Ihre Berechnung läuft auf ein Eigenwertproblem hinaus. PCA ist linear; tiefe Autoencoder können nichtlineare niedrigdimensionale Codes lernen, die in Experimenten deutlich besser funktionierten als PCA (Hinton & Salakhutdinov, 2006).

### Funktionsweise

Die Daten werden zentriert, eine Kovarianz- oder Korrelationsmatrix berechnet, und ihre Eigenvektoren geben die Richtungen der Hauptkomponenten an, geordnet nach der erfassten Varianz. Die Projektion der Daten auf die ersten Komponenten ergibt eine niedrigdimensionale Darstellung.

```text
1. Bestangepasste Geraden und Ebenen
▼
2. Komponenten maximaler Varianz
▼
3. Skalierung: Kovarianz- oder Korrelationsmatrix
▼
4. Wahl der Komponentenzahl
▼
5. Nichtlineare Alternative: Autoencoder
```

#### 1. Bestangepasste Geraden und Ebenen

PCA geht auf Pearson (1901) zurück, der die Geraden und Ebenen bestimmte, die ein Punktsystem im Raum im Sinne kleinster Quadrate am besten annähern, also mit minimalen senkrechten Abständen der Punkte. Die erste Hauptkomponente ist die bestangepasste Gerade.

#### 2. Komponenten maximaler Varianz

PCA erzeugt neue Variablen, die unkorreliert sind und nacheinander die Varianz maximieren; so wird die Dimension reduziert und der Informationsverlust minimiert (Jolliffe & Cadima, 2016). Die Berechnung dieser Hauptkomponenten läuft auf ein Eigenwert-/Eigenvektorproblem hinaus, und da die Komponenten aus den vorliegenden Daten abgeleitet und nicht vorab festgelegt werden, ist PCA ein adaptives Analyseverfahren. Shlens (2014) leitet die Mathematik Schritt für Schritt aus einfachen Intuitionen her.

#### 3. Skalierung: Kovarianz- oder Korrelationsmatrix

PCA auf der Kovarianzmatrix hängt von den Einheiten der Variablen ab, sodass Variablen mit großen Werten die ersten Komponenten dominieren. Die Korrelationsmatrix zu verwenden entspricht dagegen einer vorherigen Standardisierung aller Variablen; welche Wahl angemessen ist, hängt davon ab, ob die Variablen auf vergleichbaren Skalen gemessen sind (Jolliffe & Cadima, 2016; [[ml-preprocessing|Preprocessing für Machine Learning]]).

#### 4. Wahl der Komponentenzahl

Jede Komponente erfasst einen Anteil der Gesamtvarianz, und die Anteile nehmen von Komponente zu Komponente ab. Wie viele Komponenten behalten werden, richtet sich danach, wie viel der Varianz erhalten bleiben soll (Jolliffe & Cadima, 2016; Shlens, 2014).

#### 5. Nichtlineare Alternative: Autoencoder

Ein Autoencoder ist ein neuronales Netz mit einer kleinen mittleren Schicht, das darauf trainiert wird, seine Eingaben zu rekonstruieren; die mittlere Schicht lernt dabei einen niedrigdimensionalen Code (Hinton & Salakhutdinov, 2006). Mit einer geeigneten Initialisierung der Gewichte lernten tiefe Autoencoder Codes, die zur Dimensionsreduktion deutlich besser funktionierten als PCA ([[autoencoders-and-gans|Autoencoder und GANs]]).

#### Ursprung und Varianten

PCA geht auf Pearson (1901) zurück. Jolliffe & Cadima (2016) geben einen Überblick über das Verfahren und seine Varianten für verschiedene Datentypen, Shlens (2014) eine Herleitung als Tutorial, und Autoencoder (Hinton & Salakhutdinov, 2006) bieten eine nichtlineare Alternative.

### Wann einsetzen

- Wenn viele korrelierte Variablen durch wenige unkorrelierte zusammengefasst werden sollen (Jolliffe & Cadima, 2016).
- Wenn Daten visualisiert oder für abstandsbasierte Verfahren wie Clustering oder k-NN vorbereitet werden sollen ([[clustering|Clustering]], [[k-nearest-neighbors|k-Nearest Neighbors]]).
- Wenn die Struktur der Daten stark nichtlinear ist, kann ein Autoencoder die bessere Wahl sein (Hinton & Salakhutdinov, 2006).

### Stärken und Grenzen

**Stärken**
- Reduziert die Dimension bei minimalem Informationsverlust (Jolliffe & Cadima, 2016).
- Wird über ein Standard-Eigenwertproblem berechnet, ohne iteratives Training (Jolliffe & Cadima, 2016).
- Die Komponenten sind unkorreliert und nach Bedeutung geordnet (Jolliffe & Cadima, 2016).

**Einschränkungen**
- Die Ergebnisse hängen von der Skalierung der Variablen ab (Jolliffe & Cadima, 2016).
- PCA erfasst nur lineare Strukturen; tiefe Autoencoder lernten bessere niedrigdimensionale Codes (Hinton & Salakhutdinov, 2006).
- Hauptkomponenten sind Kombinationen aller ursprünglichen Variablen und oft schwer zu interpretieren (Jolliffe & Cadima, 2016).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| PCA auf der Kovarianzmatrix | Verwendet die ursprünglichen Einheiten (Jolliffe & Cadima, 2016) | Variablen auf vergleichbaren Skalen |
| PCA auf der Korrelationsmatrix | Entspricht vorheriger Standardisierung (Jolliffe & Cadima, 2016) | Variablen in unterschiedlichen Einheiten |
| Autoencoder | Nichtlinearer Code, gelernt von einem neuronalen Netz (Hinton & Salakhutdinov, 2006) | Stark nichtlineare Strukturen |

### In der Praxis

Variablen in unterschiedlichen Einheiten werden vor der PCA standardisiert (Jolliffe & Cadima, 2016). Die PCA-Transformation wird nur auf den Trainingsdaten angepasst und dann auf Validierungs- und Testdaten angewendet, um Leakage zu vermeiden ([[feature-engineering|Feature Engineering]]). Die erhaltene Varianz wird zusammen mit der gewählten Komponentenzahl berichtet.

### Merksatz

PCA ersetzt viele korrelierte Variablen durch wenige unkorrelierte Komponenten, die den Großteil der Varianz erfassen; sie ist schnell und linear, hängt aber davon ab, wie die Variablen skaliert sind.

### Quellen

- Pearson, K. (1901). *On Lines and Planes of Closest Fit to Systems of Points in Space.* Philosophical Magazine 2(11). [doi:10.1080/14786440109462720](https://doi.org/10.1080/14786440109462720)
- Jolliffe, I. T. & Cadima, J. (2016). *Principal component analysis: a review and recent developments.* Philosophical Transactions of the Royal Society A 374(2065). [doi:10.1098/rsta.2015.0202](https://doi.org/10.1098/rsta.2015.0202)
- Shlens, J. (2014). *A Tutorial on Principal Component Analysis.* [arXiv:1404.1100](https://arxiv.org/abs/1404.1100)
- Hinton, G. E. & Salakhutdinov, R. R. (2006). *Reducing the Dimensionality of Data with Neural Networks.* Science 313(5786). [doi:10.1126/science.1127647](https://doi.org/10.1126/science.1127647)
