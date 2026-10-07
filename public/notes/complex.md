---
title_en: ComplEx
title_de: ComplEx
entity_type: Method
sources:
- https://arxiv.org/abs/1606.06357
- https://arxiv.org/abs/1412.6575
- https://arxiv.org/abs/1902.10197
- https://arxiv.org/abs/2002.00388
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

ComplEx embeds entities and relations of a knowledge graph as complex-valued vectors and scores triples with the Hermitian dot product, the complex counterpart of the ordinary dot product (Trouillon et al., 2016). Because the Hermitian product uses the complex conjugate of the tail, the score of (h, r, t) can differ from that of (t, r, h), so ComplEx handles both symmetric and antisymmetric relations, which DistMult cannot (Yang et al., 2014). It stays linear in space and time and outperformed more complex models on standard link prediction benchmarks.

### How it works

Each entity and relation is a vector of complex numbers. The score of a triple is the real part of the sum over dimensions of the head, the relation and the complex conjugate of the tail; training raises scores of observed triples, and link prediction ranks candidate entities by their score.

```text
1. Link prediction by latent factorisation
▼
2. Why complex numbers
▼
3. The Hermitian dot product
▼
4. Training and efficiency
▼
5. Relation patterns and successors
```

#### 1. Link prediction by latent factorisation

Link prediction, inferring missing facts in large knowledge bases, is key to understanding their structure; ComplEx approaches it through latent factorisation, like earlier embedding models (Trouillon et al., 2016; [[knowledge-graphs|Knowledge Graphs]]). Knowledge graph embedding is organised by representation space, scoring function and encoding model, and ComplEx stands for complex vector spaces (Ji et al., 2020).

#### 2. Why complex numbers

DistMult scores triples with a bilinear product and a diagonal relation matrix, which is symmetric in head and tail (Yang et al., 2014; [[distmult|DistMult]]). With complex-valued embeddings, the composition of embeddings can handle a large variety of binary relations, among them symmetric and antisymmetric ones (Trouillon et al., 2016).

#### 3. The Hermitian dot product

ComplEx uses only the Hermitian dot product, Re(Σ hᵢ · rᵢ · conj(tᵢ)), where conj denotes the complex conjugate (Trouillon et al., 2016). Swapping head and tail changes the conjugation, so the imaginary parts of the relation embedding make the score direction-dependent: relations with purely real embeddings behave symmetrically, those with imaginary parts antisymmetrically. Compared with models such as the neural tensor network and holographic embeddings, this is arguably simpler.

#### 4. Training and efficiency

The approach is scalable to large datasets because it remains linear in both space and time, and it consistently outperformed alternative approaches on standard link prediction benchmarks (Trouillon et al., 2016).

#### 5. Relation patterns and successors

ComplEx can model symmetry, antisymmetry and inversion. RotatE, also in complex space, models each relation as a rotation and additionally covers composition of relations, with a self-adversarial negative sampling technique for training (Sun et al., 2019; [[rotate|RotatE]]).

#### Origin and variants

ComplEx (Trouillon et al., 2016) extended the bilinear DistMult (Yang et al., 2014) to complex numbers. RotatE (Sun et al., 2019) followed with rotations in complex space, and Ji et al. (2020) survey the wider family of knowledge graph embeddings.

### When to use it

- When a knowledge graph contains both symmetric and directional relations (Trouillon et al., 2016).
- When a scalable model with linear time and space complexity is needed (Trouillon et al., 2016).
- When relation composition must be modelled, RotatE may be the better choice (Sun et al., 2019).

### Strengths and limitations

**Strengths**
- Handles symmetric and antisymmetric relations (Trouillon et al., 2016).
- Linear in space and time, scalable to large datasets (Trouillon et al., 2016).
- Outperformed alternative approaches on standard link prediction benchmarks (Trouillon et al., 2016).

**Limitations**
- Does not model composition of relations explicitly, unlike RotatE (Sun et al., 2019).
- Complex-valued embeddings are less intuitive to interpret than translations ([[transe|TransE]]).
- As a latent factorisation model, it only predicts links between entities seen during training (Ji et al., 2020).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| DistMult | Real-valued bilinear score, symmetric (Yang et al., 2014) | Symmetric relations |
| ComplEx | Complex embeddings with Hermitian product (Trouillon et al., 2016) | Symmetric and antisymmetric relations |
| RotatE | Relations as rotations in complex space (Sun et al., 2019) | Additionally composition and inversion |

### In practice

ComplEx is a standard model in knowledge graph embedding libraries and is compared with DistMult and RotatE on the same link prediction benchmarks (Ji et al., 2020). The embedding dimension and the number of negative samples are tuned on validation data.

### Key takeaway

ComplEx uses complex-valued embeddings and the Hermitian dot product so that one simple model can represent both symmetric and directional relations.

### Sources

- Trouillon, T. et al. (2016). *Complex Embeddings for Simple Link Prediction.* ICML 2016. [arXiv:1606.06357](https://arxiv.org/abs/1606.06357)
- Yang, B. et al. (2014). *Embedding Entities and Relations for Learning and Inference in Knowledge Bases.* ICLR 2015. [arXiv:1412.6575](https://arxiv.org/abs/1412.6575)
- Sun, Z. et al. (2019). *RotatE: Knowledge Graph Embedding by Relational Rotation in Complex Space.* ICLR 2019. [arXiv:1902.10197](https://arxiv.org/abs/1902.10197)
- Ji, S. et al. (2020). *A Survey on Knowledge Graphs: Representation, Acquisition and Applications.* IEEE TNNLS 2022. [arXiv:2002.00388](https://arxiv.org/abs/2002.00388)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

ComplEx bettet Entitäten und Beziehungen eines Wissensgraphen als komplexwertige Vektoren ein und bewertet Tripel mit dem hermiteschen Skalarprodukt, dem komplexen Gegenstück zum gewöhnlichen Skalarprodukt (Trouillon et al., 2016). Da das hermitesche Produkt das komplex Konjugierte des Schwanzes nutzt, kann sich die Bewertung von (h, r, t) von der von (t, r, h) unterscheiden; so bildet ComplEx symmetrische und antisymmetrische Beziehungen ab, was DistMult nicht kann (Yang et al., 2014). Es bleibt linear in Speicher und Zeit und übertraf aufwendigere Modelle auf Standard-Benchmarks für Link Prediction.

### Funktionsweise

Jede Entität und Beziehung ist ein Vektor komplexer Zahlen. Die Bewertung eines Tripels ist der Realteil der Summe über alle Dimensionen aus Kopf, Beziehung und komplex konjugiertem Schwanz; das Training hebt die Bewertung beobachteter Tripel an, und Link Prediction rankt Kandidatenentitäten nach ihrer Bewertung.

```text
1. Link Prediction durch latente Faktorisierung
▼
2. Warum komplexe Zahlen
▼
3. Das hermitesche Skalarprodukt
▼
4. Training und Effizienz
▼
5. Beziehungsmuster und Nachfolger
```

#### 1. Link Prediction durch latente Faktorisierung

Link Prediction, also das Erschließen fehlender Fakten in großen Wissensbasen, ist zentral, um deren Struktur zu verstehen; ComplEx geht sie wie frühere Embedding-Modelle über latente Faktorisierung an (Trouillon et al., 2016; [[knowledge-graphs|Wissensgraphen]]). Knowledge Graph Embeddings werden nach Repräsentationsraum, Bewertungsfunktion und Kodierungsmodell geordnet, und ComplEx steht für komplexe Vektorräume (Ji et al., 2020).

#### 2. Warum komplexe Zahlen

DistMult bewertet Tripel mit einem bilinearen Produkt und einer diagonalen Beziehungsmatrix, das in Kopf und Schwanz symmetrisch ist (Yang et al., 2014; [[distmult|DistMult]]). Mit komplexwertigen Embeddings kann die Verknüpfung der Embeddings eine große Vielfalt binärer Beziehungen abbilden, darunter symmetrische und antisymmetrische (Trouillon et al., 2016).

#### 3. Das hermitesche Skalarprodukt

ComplEx nutzt nur das hermitesche Skalarprodukt Re(Σ hᵢ · rᵢ · conj(tᵢ)), wobei conj das komplex Konjugierte bezeichnet (Trouillon et al., 2016). Werden Kopf und Schwanz vertauscht, ändert sich die Konjugation, sodass die Imaginärteile des Beziehungs-Embeddings die Bewertung richtungsabhängig machen: Beziehungen mit rein reellen Embeddings verhalten sich symmetrisch, solche mit Imaginärteilen antisymmetrisch. Gegenüber Modellen wie dem Neural Tensor Network und Holographic Embeddings ist das vergleichsweise einfach.

#### 4. Training und Effizienz

Der Ansatz skaliert auf große Datensätze, weil er in Speicher und Zeit linear bleibt, und übertraf auf Standard-Benchmarks für Link Prediction durchgängig alternative Verfahren (Trouillon et al., 2016).

#### 5. Beziehungsmuster und Nachfolger

ComplEx kann Symmetrie, Antisymmetrie und Inversion modellieren. RotatE, ebenfalls im komplexen Raum, modelliert jede Beziehung als Drehung und deckt zusätzlich die Komposition von Beziehungen ab, mit einer selbstadversarialen Negative-Sampling-Technik für das Training (Sun et al., 2019; [[rotate|RotatE]]).

#### Ursprung und Varianten

ComplEx (Trouillon et al., 2016) erweiterte das bilineare DistMult (Yang et al., 2014) auf komplexe Zahlen. RotatE (Sun et al., 2019) folgte mit Drehungen im komplexen Raum, und Ji et al. (2020) geben einen Überblick über die weitere Familie der Knowledge Graph Embeddings.

### Wann einsetzen

- Wenn ein Wissensgraph sowohl symmetrische als auch gerichtete Beziehungen enthält (Trouillon et al., 2016).
- Wenn ein skalierbares Modell mit linearem Zeit- und Speicherbedarf gebraucht wird (Trouillon et al., 2016).
- Wenn die Komposition von Beziehungen modelliert werden muss, kann RotatE die bessere Wahl sein (Sun et al., 2019).

### Stärken und Grenzen

**Stärken**
- Bildet symmetrische und antisymmetrische Beziehungen ab (Trouillon et al., 2016).
- Linear in Speicher und Zeit, skaliert auf große Datensätze (Trouillon et al., 2016).
- Übertraf alternative Verfahren auf Standard-Benchmarks für Link Prediction (Trouillon et al., 2016).

**Einschränkungen**
- Modelliert die Komposition von Beziehungen nicht ausdrücklich, anders als RotatE (Sun et al., 2019).
- Komplexwertige Embeddings sind weniger anschaulich zu deuten als Verschiebungen ([[transe|TransE]]).
- Als latentes Faktorisierungsmodell sagt es nur Verbindungen zwischen im Training gesehenen Entitäten vorher (Ji et al., 2020).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| DistMult | Reellwertige bilineare Bewertung, symmetrisch (Yang et al., 2014) | Symmetrische Beziehungen |
| ComplEx | Komplexe Embeddings mit hermiteschem Produkt (Trouillon et al., 2016) | Symmetrische und antisymmetrische Beziehungen |
| RotatE | Beziehungen als Drehungen im komplexen Raum (Sun et al., 2019) | Zusätzlich Komposition und Inversion |

### In der Praxis

ComplEx ist ein Standardmodell in Bibliotheken für Knowledge Graph Embeddings und wird auf denselben Benchmarks für Link Prediction mit DistMult und RotatE verglichen (Ji et al., 2020). Embedding-Dimension und Zahl der Negativbeispiele werden auf Validierungsdaten abgestimmt.

### Merksatz

ComplEx nutzt komplexwertige Embeddings und das hermitesche Skalarprodukt, sodass ein einfaches Modell sowohl symmetrische als auch gerichtete Beziehungen darstellen kann.

### Quellen

- Trouillon, T. et al. (2016). *Complex Embeddings for Simple Link Prediction.* ICML 2016. [arXiv:1606.06357](https://arxiv.org/abs/1606.06357)
- Yang, B. et al. (2014). *Embedding Entities and Relations for Learning and Inference in Knowledge Bases.* ICLR 2015. [arXiv:1412.6575](https://arxiv.org/abs/1412.6575)
- Sun, Z. et al. (2019). *RotatE: Knowledge Graph Embedding by Relational Rotation in Complex Space.* ICLR 2019. [arXiv:1902.10197](https://arxiv.org/abs/1902.10197)
- Ji, S. et al. (2020). *A Survey on Knowledge Graphs: Representation, Acquisition and Applications.* IEEE TNNLS 2022. [arXiv:2002.00388](https://arxiv.org/abs/2002.00388)
