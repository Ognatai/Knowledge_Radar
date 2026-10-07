---
title_en: DistMult
title_de: DistMult
entity_type: Method
sources:
- https://arxiv.org/abs/1412.6575
- https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data
- https://arxiv.org/abs/1606.06357
- https://doi.org/10.1109/TKDE.2017.2754499
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

DistMult is a knowledge graph embedding model that scores a triple with a bilinear product of the head and tail vectors and a diagonal relation matrix, i.e. a weighted element-wise product (Yang et al., 2014). In a unified framework of embedding models, this simple bilinear formulation achieved a top-10 link prediction accuracy of 73.2% on Freebase, compared with 54.7% for TransE. Because the score is symmetric in head and tail, DistMult cannot distinguish a relation from its reverse, which ComplEx later fixes (Wang et al., 2017; Trouillon et al., 2016).

### How it works

Entities are vectors and each relation is a vector of weights. The score of (h, r, t) is the sum over dimensions of h times r times t; training raises the scores of observed triples above those of corrupted ones, and the relation embeddings can also be composed to mine logical rules.

```text
1. A unified framework
▼
2. Bilinear scoring with a diagonal matrix
▼
3. Training and link prediction
▼
4. Rule mining from embeddings
▼
5. The symmetry limitation
```

#### 1. A unified framework

Yang et al. (2014) show that most existing embedding models, including the neural tensor network and TransE (Bordes et al., 2013), fit a unified framework in which entities are low-dimensional vectors learned by a neural network and relations are linear and/or bilinear mapping functions. Within this framework, they compare models on link prediction ([[transe|TransE]]).

#### 2. Bilinear scoring with a diagonal matrix

Semantic matching models score triples with a bilinear form between head and tail embeddings and a relation matrix (Wang et al., 2017). DistMult restricts this matrix to be diagonal, so the score becomes Σ hᵢ·rᵢ·tᵢ, the element-wise product of the three vectors summed over dimensions; this sharply reduces the number of parameters per relation (Yang et al., 2014; Wang et al., 2017).

#### 3. Training and link prediction

Like other embedding models, DistMult is trained to score observed triples higher than corrupted ones and is evaluated by ranking candidate entities for missing heads or tails. The simple bilinear formulation achieved new state-of-the-art results, a top-10 accuracy of 73.2% on Freebase versus 54.7% for TransE (Yang et al., 2014).

#### 4. Rule mining from embeddings

Embeddings learned with the bilinear objective capture relational semantics well, and composing relations corresponds to multiplying their matrices (Yang et al., 2014). The authors use this to mine logical rules such as "BornInCity(a, b) and CityInCountry(b, c) ⇒ Nationality(a, c)", and their embedding-based approach outperformed a state-of-the-art confidence-based rule miner on Horn rules involving compositional reasoning.

#### 5. The symmetry limitation

Because the diagonal score is the same for (h, r, t) and (t, r, h), DistMult treats every relation as symmetric and cannot model antisymmetric relations such as "is parent of" (Wang et al., 2017). ComplEx uses complex-valued embeddings with the Hermitian dot product to handle symmetric and antisymmetric relations while staying linear in space and time (Trouillon et al., 2016; [[complex|ComplEx]]).

#### Origin and variants

DistMult was introduced by Yang et al. (2014) as part of a unified framework that also covers TransE (Bordes et al., 2013). Wang et al. (2017) classify it among semantic matching models, and ComplEx (Trouillon et al., 2016) extends it to complex numbers.

### When to use it

- As a strong, simple baseline for link prediction (Yang et al., 2014).
- When most relations are symmetric, such as "is married to" or "is similar to" (Wang et al., 2017).
- When rules should be mined from learned embeddings (Yang et al., 2014).

### Strengths and limitations

**Strengths**
- Few parameters per relation thanks to the diagonal matrix (Wang et al., 2017).
- Outperformed TransE on Freebase link prediction (Yang et al., 2014).
- Embeddings support compositional rule mining (Yang et al., 2014).

**Limitations**
- Can only model symmetric relations (Wang et al., 2017).
- Cannot distinguish a relation from its inverse direction (Trouillon et al., 2016).
- Superseded by complex-valued models for antisymmetric relations (Trouillon et al., 2016).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| TransE | Translation h + r ≈ t (Bordes et al., 2013) | One-to-one relations |
| DistMult | Bilinear score with diagonal relation matrix (Yang et al., 2014) | Symmetric relations, simple baseline |
| ComplEx | Complex embeddings, Hermitian product (Trouillon et al., 2016) | Symmetric and antisymmetric relations |

### In practice

DistMult is often included as a baseline when comparing knowledge graph embedding models on link prediction (Wang et al., 2017). Before choosing it, the relations of the graph are checked: if many are directional, a model such as ComplEx or RotatE is more appropriate ([[rotate|RotatE]]).

### Key takeaway

DistMult scores triples with a simple element-wise product of three vectors, which works well but treats every relation as symmetric.

### Sources

- Yang, B. et al. (2014). *Embedding Entities and Relations for Learning and Inference in Knowledge Bases.* ICLR 2015. [arXiv:1412.6575](https://arxiv.org/abs/1412.6575)
- Bordes, A., Usunier, N., Garcia-Durán, A., Weston, J. & Yakhnenko, O. (2013). *Translating Embeddings for Modeling Multi-relational Data.* NeurIPS 2013. [NeurIPS proceedings](https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data)
- Trouillon, T. et al. (2016). *Complex Embeddings for Simple Link Prediction.* ICML 2016. [arXiv:1606.06357](https://arxiv.org/abs/1606.06357)
- Wang, Q., Mao, Z., Wang, B. & Guo, L. (2017). *Knowledge Graph Embedding: A Survey of Approaches and Applications.* IEEE Transactions on Knowledge and Data Engineering 29(12). [doi:10.1109/TKDE.2017.2754499](https://doi.org/10.1109/TKDE.2017.2754499)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

DistMult ist ein Modell für Knowledge Graph Embeddings, das ein Tripel mit einem bilinearen Produkt aus Kopf- und Schwanzvektor und einer diagonalen Beziehungsmatrix bewertet, also mit einem gewichteten elementweisen Produkt (Yang et al., 2014). In einem gemeinsamen Rahmen für Embedding-Modelle erreichte diese einfache bilineare Formulierung bei Link Prediction auf Freebase eine Top-10-Genauigkeit von 73,2 %, TransE 54,7 %. Da die Bewertung in Kopf und Schwanz symmetrisch ist, kann DistMult eine Beziehung nicht von ihrer Umkehrung unterscheiden, was ComplEx später behebt (Wang et al., 2017; Trouillon et al., 2016).

### Funktionsweise

Entitäten sind Vektoren, und jede Beziehung ist ein Vektor von Gewichten. Die Bewertung von (h, r, t) ist die Summe über alle Dimensionen von h mal r mal t; das Training hebt die Bewertung beobachteter Tripel über die verfälschter Tripel, und die Beziehungs-Embeddings lassen sich auch zusammensetzen, um logische Regeln zu gewinnen.

```text
1. Ein gemeinsamer Rahmen
▼
2. Bilineare Bewertung mit diagonaler Matrix
▼
3. Training und Link Prediction
▼
4. Regeln aus Embeddings gewinnen
▼
5. Die Symmetrie-Grenze
```

#### 1. Ein gemeinsamer Rahmen

Yang et al. (2014) zeigen, dass sich die meisten bestehenden Embedding-Modelle, darunter das Neural Tensor Network und TransE (Bordes et al., 2013), in einen gemeinsamen Rahmen fassen lassen, in dem Entitäten niedrigdimensionale, von einem neuronalen Netz gelernte Vektoren und Beziehungen lineare und/oder bilineare Abbildungen sind. In diesem Rahmen vergleichen sie Modelle bei Link Prediction ([[transe|TransE]]).

#### 2. Bilineare Bewertung mit diagonaler Matrix

Semantic-Matching-Modelle bewerten Tripel mit einer bilinearen Form aus Kopf- und Schwanz-Embedding und einer Beziehungsmatrix (Wang et al., 2017). DistMult beschränkt diese Matrix auf eine Diagonalmatrix, sodass die Bewertung zu Σ hᵢ·rᵢ·tᵢ wird, dem über die Dimensionen summierten elementweisen Produkt der drei Vektoren; das verringert die Zahl der Parameter je Beziehung stark (Yang et al., 2014; Wang et al., 2017).

#### 3. Training und Link Prediction

Wie andere Embedding-Modelle wird DistMult so trainiert, dass beobachtete Tripel höher bewertet werden als verfälschte, und durch Ranking von Kandidatenentitäten für fehlende Köpfe oder Schwänze evaluiert. Die einfache bilineare Formulierung erzielte neue Bestwerte, eine Top-10-Genauigkeit von 73,2 % auf Freebase gegenüber 54,7 % für TransE (Yang et al., 2014).

#### 4. Regeln aus Embeddings gewinnen

Mit dem bilinearen Ziel gelernte Embeddings erfassen die Bedeutung von Beziehungen gut, und das Zusammensetzen von Beziehungen entspricht der Multiplikation ihrer Matrizen (Yang et al., 2014). Die Autoren nutzen das, um logische Regeln wie „BornInCity(a, b) und CityInCountry(b, c) ⇒ Nationality(a, c)“ zu gewinnen, und ihr embedding-basierter Ansatz übertraf bei Horn-Regeln mit kompositionellem Schließen ein führendes konfidenzbasiertes Regel-Mining-Verfahren.

#### 5. Die Symmetrie-Grenze

Da die diagonale Bewertung für (h, r, t) und (t, r, h) gleich ist, behandelt DistMult jede Beziehung als symmetrisch und kann antisymmetrische Beziehungen wie „ist Elternteil von“ nicht modellieren (Wang et al., 2017). ComplEx nutzt komplexwertige Embeddings mit dem hermiteschen Skalarprodukt, um symmetrische und antisymmetrische Beziehungen abzubilden, und bleibt dabei linear in Speicher und Zeit (Trouillon et al., 2016; [[complex|ComplEx]]).

#### Ursprung und Varianten

DistMult wurde von Yang et al. (2014) als Teil eines gemeinsamen Rahmens eingeführt, der auch TransE (Bordes et al., 2013) umfasst. Wang et al. (2017) ordnen es den Semantic-Matching-Modellen zu, und ComplEx (Trouillon et al., 2016) erweitert es auf komplexe Zahlen.

### Wann einsetzen

- Als starke, einfache Baseline für Link Prediction (Yang et al., 2014).
- Wenn die meisten Beziehungen symmetrisch sind, etwa „ist verheiratet mit“ oder „ist ähnlich zu“ (Wang et al., 2017).
- Wenn aus gelernten Embeddings Regeln gewonnen werden sollen (Yang et al., 2014).

### Stärken und Grenzen

**Stärken**
- Wenige Parameter je Beziehung dank Diagonalmatrix (Wang et al., 2017).
- Übertraf TransE bei Link Prediction auf Freebase (Yang et al., 2014).
- Embeddings unterstützen kompositionelles Regel-Mining (Yang et al., 2014).

**Einschränkungen**
- Kann nur symmetrische Beziehungen modellieren (Wang et al., 2017).
- Kann eine Beziehung nicht von ihrer Gegenrichtung unterscheiden (Trouillon et al., 2016).
- Bei antisymmetrischen Beziehungen von komplexwertigen Modellen abgelöst (Trouillon et al., 2016).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| TransE | Verschiebung h + r ≈ t (Bordes et al., 2013) | 1:1-Beziehungen |
| DistMult | Bilineare Bewertung mit diagonaler Beziehungsmatrix (Yang et al., 2014) | Symmetrische Beziehungen, einfache Baseline |
| ComplEx | Komplexe Embeddings, hermitesches Produkt (Trouillon et al., 2016) | Symmetrische und antisymmetrische Beziehungen |

### In der Praxis

DistMult wird beim Vergleich von Knowledge-Graph-Embedding-Modellen für Link Prediction oft als Baseline mitgeführt (Wang et al., 2017). Vor der Wahl werden die Beziehungen des Graphen geprüft: Sind viele gerichtet, ist ein Modell wie ComplEx oder RotatE geeigneter ([[rotate|RotatE]]).

### Merksatz

DistMult bewertet Tripel mit einem einfachen elementweisen Produkt dreier Vektoren; das funktioniert gut, behandelt aber jede Beziehung als symmetrisch.

### Quellen

- Yang, B. et al. (2014). *Embedding Entities and Relations for Learning and Inference in Knowledge Bases.* ICLR 2015. [arXiv:1412.6575](https://arxiv.org/abs/1412.6575)
- Bordes, A., Usunier, N., Garcia-Durán, A., Weston, J. & Yakhnenko, O. (2013). *Translating Embeddings for Modeling Multi-relational Data.* NeurIPS 2013. [NeurIPS proceedings](https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data)
- Trouillon, T. et al. (2016). *Complex Embeddings for Simple Link Prediction.* ICML 2016. [arXiv:1606.06357](https://arxiv.org/abs/1606.06357)
- Wang, Q., Mao, Z., Wang, B. & Guo, L. (2017). *Knowledge Graph Embedding: A Survey of Approaches and Applications.* IEEE Transactions on Knowledge and Data Engineering 29(12). [doi:10.1109/TKDE.2017.2754499](https://doi.org/10.1109/TKDE.2017.2754499)
