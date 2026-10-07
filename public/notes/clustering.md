---
title_en: Clustering
title_de: Clustering
entity_type: Method
sources:
- https://doi.org/10.1109/TIT.1982.1056489
- https://theory.stanford.edu/~sergei/papers/kMeansPP-soda.pdf
- https://doi.org/10.1080/01621459.1963.10500845
- https://cdn.aaai.org/KDD/1996/KDD96-037.pdf
- https://jmlr.org/papers/v12/pedregosa11a.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Clustering groups unlabelled data points so that points in the same group are similar to each other. k-means minimises the squared distances between points and their cluster centres (Lloyd, 1982; Arthur & Vassilvitskii, 2007), hierarchical clustering merges groups step by step into a hierarchy (Ward, 1963), and DBSCAN finds dense regions of arbitrary shape and marks isolated points as noise (Ester et al., 1996).

### How it works

A clustering method takes data points and a notion of distance or density and assigns each point to a cluster, or to noise. The methods differ in what they consider a cluster: points close to a centre, groups that are cheap to merge, or regions of high density.

```text
1. k-means (Lloyd's algorithm)
▼
2. Seeding with k-means++
▼
3. Hierarchical clustering with Ward's criterion
▼
4. Density-based clustering (DBSCAN)
▼
5. Implementation
```

#### 1. k-means (Lloyd's algorithm)

k-means seeks k centres that minimise the sum of squared distances between each point and its closest centre (Arthur & Vassilvitskii, 2007). Lloyd's algorithm, originally derived for optimal quantisation of signals (Lloyd, 1982), alternates two steps: assign each point to the nearest centre, then move each centre to the mean of its assigned points. It is simple and fast but offers no accuracy guarantee (Arthur & Vassilvitskii, 2007).

#### 2. Seeding with k-means++

The result of Lloyd's algorithm depends on the initial centres, which are typically chosen uniformly at random. k-means++ chooses them with a simple randomised seeding technique, which makes the algorithm Theta(log k)-competitive with the optimal clustering; in experiments it improved both speed and accuracy, often considerably (Arthur & Vassilvitskii, 2007).

#### 3. Hierarchical clustering with Ward's criterion

Agglomerative hierarchical clustering starts with every point as its own group and repeatedly merges the pair of groups whose union best preserves an objective function (Ward, 1963). With Ward's criterion, this is the merge with the smallest increase in within-group sum of squares. Repeating this until one group remains yields the complete hierarchy and a measure of the loss at each stage, so the number of clusters can be chosen afterwards.

#### 4. Density-based clustering (DBSCAN)

DBSCAN (Ester et al., 1996) relies on a density-based notion of clusters: clusters are regions where points lie densely, separated by regions of low density. It discovers clusters of arbitrary shape and marks points in low-density regions as noise. It requires only one input parameter and supports the user in choosing it. In the experiments it was more effective than CLARANS at finding clusters of arbitrary shape and more than 100 times faster.

#### 5. Implementation

k-means, hierarchical clustering and DBSCAN are available in scikit-learn (Pedregosa et al., 2011). Because all three rely on distances, features should be scaled to comparable ranges first ([[ml-preprocessing|ML Preprocessing]]).

#### Origin and variants

Ward (1963) proposed hierarchical grouping by an objective function, Lloyd (1982) the quantisation algorithm behind k-means, Ester et al. (1996) DBSCAN, and Arthur & Vassilvitskii (2007) the k-means++ seeding.

### When to use it

- When roughly spherical groups of similar size are expected and the number of clusters is known, k-means with k-means++ seeding is a fast choice (Arthur & Vassilvitskii, 2007).
- When the number of clusters is unknown or a hierarchy of groups is of interest, hierarchical clustering helps (Ward, 1963).
- When clusters have arbitrary shapes or the data contains noise, DBSCAN is suitable (Ester et al., 1996).

### Strengths and limitations

**Strengths**
- k-means is simple and fast; k-means++ adds an accuracy guarantee (Arthur & Vassilvitskii, 2007).
- Hierarchical clustering yields the whole hierarchy and the cost of each merge (Ward, 1963).
- DBSCAN finds clusters of arbitrary shape and identifies noise (Ester et al., 1996).

**Limitations**
- k-means needs the number of clusters in advance and depends on initialisation (Arthur & Vassilvitskii, 2007).
- Agglomerative clustering compares all pairs of groups at each step, which becomes expensive for large n (Ward, 1963).
- All three rely on distances, so results depend on the chosen distance and on feature scaling (Lloyd, 1982; Ward, 1963; Ester et al., 1996).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| k-means | Minimises squared distances to k centres (Lloyd, 1982; Arthur & Vassilvitskii, 2007) | Compact clusters, known k |
| Hierarchical (Ward) | Merges groups with the smallest increase in within-group sum of squares (Ward, 1963) | Unknown number of clusters, hierarchies |
| DBSCAN | Density-based, arbitrary shapes, noise points (Ester et al., 1996) | Irregular shapes, noisy data |

### In practice

Features are scaled before clustering, and the result is checked for plausibility with domain knowledge, since there are no labels to evaluate against. High-dimensional data is often reduced first, for example with [[principal-component-analysis|Principal Component Analysis]]. Clustering of embeddings is used, for example, to group similar documents ([[embeddings|Embeddings]]).

### Key takeaway

Clustering finds groups without labels; the right method depends on whether clusters are compact (k-means), hierarchical (Ward) or of arbitrary shape with noise (DBSCAN).

### Sources

- Lloyd, S. P. (1982). *Least Squares Quantization in PCM.* IEEE Transactions on Information Theory 28(2). [doi:10.1109/TIT.1982.1056489](https://doi.org/10.1109/TIT.1982.1056489)
- Arthur, D. & Vassilvitskii, S. (2007). *k-means++: The Advantages of Careful Seeding.* SODA 2007. [PDF](https://theory.stanford.edu/~sergei/papers/kMeansPP-soda.pdf)
- Ward, J. H. (1963). *Hierarchical Grouping to Optimize an Objective Function.* Journal of the American Statistical Association 58(301). [doi:10.1080/01621459.1963.10500845](https://doi.org/10.1080/01621459.1963.10500845)
- Ester, M., Kriegel, H.-P., Sander, J. & Xu, X. (1996). *A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise.* KDD 1996. [PDF](https://cdn.aaai.org/KDD/1996/KDD96-037.pdf)
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12. [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Clustering gruppiert nicht gelabelte Datenpunkte so, dass Punkte derselben Gruppe einander ähnlich sind. k-Means minimiert die quadrierten Abstände zwischen Punkten und ihren Clusterzentren (Lloyd, 1982; Arthur & Vassilvitskii, 2007), hierarchisches Clustering fasst Gruppen schrittweise zu einer Hierarchie zusammen (Ward, 1963), und DBSCAN findet dichte Regionen beliebiger Form und markiert vereinzelte Punkte als Rauschen (Ester et al., 1996).

### Funktionsweise

Ein Clustering-Verfahren erhält Datenpunkte und einen Abstands- oder Dichtebegriff und ordnet jeden Punkt einem Cluster oder dem Rauschen zu. Die Verfahren unterscheiden sich darin, was sie als Cluster ansehen: Punkte nahe einem Zentrum, Gruppen, die sich günstig zusammenlegen lassen, oder Regionen hoher Dichte.

```text
1. k-Means (Lloyd-Algorithmus)
▼
2. Initialisierung mit k-Means++
▼
3. Hierarchisches Clustering nach Ward
▼
4. Dichtebasiertes Clustering (DBSCAN)
▼
5. Implementierung
```

#### 1. k-Means (Lloyd-Algorithmus)

k-Means sucht k Zentren, die die Summe der quadrierten Abstände zwischen jedem Punkt und seinem nächsten Zentrum minimieren (Arthur & Vassilvitskii, 2007). Der Lloyd-Algorithmus, ursprünglich für die optimale Quantisierung von Signalen hergeleitet (Lloyd, 1982), wechselt zwischen zwei Schritten: jeden Punkt dem nächsten Zentrum zuordnen, dann jedes Zentrum auf den Mittelwert seiner Punkte verschieben. Er ist einfach und schnell, bietet aber keine Genauigkeitsgarantie (Arthur & Vassilvitskii, 2007).

#### 2. Initialisierung mit k-Means++

Das Ergebnis des Lloyd-Algorithmus hängt von den Startzentren ab, die meist gleichverteilt zufällig gewählt werden. k-Means++ wählt sie mit einem einfachen randomisierten Verfahren und ist damit Theta(log k)-kompetitiv zum optimalen Clustering; in Experimenten verbesserte es Geschwindigkeit und Genauigkeit, oft deutlich (Arthur & Vassilvitskii, 2007).

#### 3. Hierarchisches Clustering nach Ward

Agglomeratives hierarchisches Clustering beginnt mit jedem Punkt als eigener Gruppe und legt wiederholt das Gruppenpaar zusammen, dessen Vereinigung eine Zielfunktion am besten erhält (Ward, 1963). Beim Ward-Kriterium ist das die Zusammenlegung mit dem geringsten Anstieg der Quadratsumme innerhalb der Gruppen. Wiederholt man das, bis eine Gruppe übrig bleibt, erhält man die vollständige Hierarchie und ein Maß für den Verlust in jedem Schritt; die Clusterzahl kann dann nachträglich gewählt werden.

#### 4. Dichtebasiertes Clustering (DBSCAN)

DBSCAN (Ester et al., 1996) beruht auf einem dichtebasierten Clusterbegriff: Cluster sind Regionen dicht liegender Punkte, getrennt durch Regionen geringer Dichte. Es findet Cluster beliebiger Form und markiert Punkte in dünn besetzten Regionen als Rauschen. Es benötigt nur einen Eingabeparameter und unterstützt dessen Wahl. In den Experimenten fand es Cluster beliebiger Form zuverlässiger als CLARANS und war mehr als 100-mal schneller.

#### 5. Implementierung

k-Means, hierarchisches Clustering und DBSCAN sind in scikit-learn verfügbar (Pedregosa et al., 2011). Da alle drei auf Abständen beruhen, sollten die Merkmale vorher auf vergleichbare Bereiche skaliert werden ([[ml-preprocessing|Preprocessing für Machine Learning]]).

#### Ursprung und Varianten

Ward (1963) schlug hierarchisches Gruppieren nach einer Zielfunktion vor, Lloyd (1982) den Quantisierungsalgorithmus hinter k-Means, Ester et al. (1996) DBSCAN und Arthur & Vassilvitskii (2007) die Initialisierung mit k-Means++.

### Wann einsetzen

- Wenn etwa kugelförmige Gruppen ähnlicher Größe erwartet werden und die Clusterzahl bekannt ist, ist k-Means mit k-Means++-Initialisierung eine schnelle Wahl (Arthur & Vassilvitskii, 2007).
- Wenn die Clusterzahl unbekannt ist oder eine Hierarchie von Gruppen interessiert, hilft hierarchisches Clustering (Ward, 1963).
- Wenn Cluster beliebige Formen haben oder die Daten Rauschen enthalten, eignet sich DBSCAN (Ester et al., 1996).

### Stärken und Grenzen

**Stärken**
- k-Means ist einfach und schnell; k-Means++ ergänzt eine Genauigkeitsgarantie (Arthur & Vassilvitskii, 2007).
- Hierarchisches Clustering liefert die gesamte Hierarchie und die Kosten jeder Zusammenlegung (Ward, 1963).
- DBSCAN findet Cluster beliebiger Form und erkennt Rauschen (Ester et al., 1996).

**Einschränkungen**
- k-Means braucht die Clusterzahl vorab und hängt von der Initialisierung ab (Arthur & Vassilvitskii, 2007).
- Agglomeratives Clustering vergleicht in jedem Schritt alle Gruppenpaare, was bei großem n aufwendig wird (Ward, 1963).
- Alle drei beruhen auf Abständen; die Ergebnisse hängen daher vom gewählten Abstandsmaß und der Skalierung ab (Lloyd, 1982; Ward, 1963; Ester et al., 1996).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| k-Means | Minimiert quadrierte Abstände zu k Zentren (Lloyd, 1982; Arthur & Vassilvitskii, 2007) | Kompakte Cluster, bekanntes k |
| Hierarchisch (Ward) | Legt Gruppen mit dem geringsten Anstieg der Quadratsumme zusammen (Ward, 1963) | Unbekannte Clusterzahl, Hierarchien |
| DBSCAN | Dichtebasiert, beliebige Formen, Rauschpunkte (Ester et al., 1996) | Unregelmäßige Formen, verrauschte Daten |

### In der Praxis

Die Merkmale werden vor dem Clustering skaliert, und das Ergebnis wird mit Fachwissen auf Plausibilität geprüft, da keine Labels zur Bewertung vorliegen. Hochdimensionale Daten werden oft vorher reduziert, etwa mit der [[principal-component-analysis|Hauptkomponentenanalyse (PCA)]]. Clustering von Embeddings dient zum Beispiel dazu, ähnliche Dokumente zu gruppieren ([[embeddings|Embeddings]]).

### Merksatz

Clustering findet Gruppen ohne Labels; welches Verfahren passt, hängt davon ab, ob die Cluster kompakt (k-Means), hierarchisch (Ward) oder beliebig geformt und verrauscht (DBSCAN) sind.

### Quellen

- Lloyd, S. P. (1982). *Least Squares Quantization in PCM.* IEEE Transactions on Information Theory 28(2). [doi:10.1109/TIT.1982.1056489](https://doi.org/10.1109/TIT.1982.1056489)
- Arthur, D. & Vassilvitskii, S. (2007). *k-means++: The Advantages of Careful Seeding.* SODA 2007. [PDF](https://theory.stanford.edu/~sergei/papers/kMeansPP-soda.pdf)
- Ward, J. H. (1963). *Hierarchical Grouping to Optimize an Objective Function.* Journal of the American Statistical Association 58(301). [doi:10.1080/01621459.1963.10500845](https://doi.org/10.1080/01621459.1963.10500845)
- Ester, M., Kriegel, H.-P., Sander, J. & Xu, X. (1996). *A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise.* KDD 1996. [PDF](https://cdn.aaai.org/KDD/1996/KDD96-037.pdf)
- Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12. [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html)
