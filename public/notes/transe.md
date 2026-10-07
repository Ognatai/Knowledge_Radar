---
title_en: TransE
title_de: TransE
entity_type: Method
sources:
- https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data
- https://arxiv.org/abs/1412.6575
- https://doi.org/10.1109/TKDE.2017.2754499
- https://arxiv.org/abs/1902.10197
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

TransE embeds the entities and relations of a knowledge graph as vectors and models each relation as a translation: for a true triple (head, relation, tail), the head vector plus the relation vector should lie close to the tail vector (Bordes et al., 2013). It is simple, has few parameters and scales to large graphs, which made it a standard baseline for link prediction ([[knowledge-graphs|Knowledge Graphs]]). It struggles with one-to-many, many-to-one and many-to-many relations and cannot model symmetric relations well, which later models address (Wang et al., 2017; Sun et al., 2019).

### How it works

Every entity and every relation gets a vector of the same dimension. Training pulls h + r towards t for observed triples and pushes it away for corrupted triples in which the head or tail has been replaced; at prediction time, candidate entities are ranked by their distance.

```text
1. Translation as a relation model
▼
2. Scoring function
▼
3. Training with negative triples
▼
4. Link prediction
▼
5. Limitations and extensions
```

#### 1. Translation as a relation model

Bordes et al. (2013) interpret relationships as translations operating on low-dimensional embeddings of entities. If (Berlin, capitalOf, Germany) holds, the vector of Berlin plus the vector of capitalOf should be close to the vector of Germany.

#### 2. Scoring function

The plausibility of a triple is measured by the distance between h + r and t, for example with the L1 or L2 norm: the smaller the distance, the more plausible the triple (Bordes et al., 2013). TransE belongs to the family of translational distance models, in contrast to semantic matching models such as DistMult, which score triples by similarity (Wang et al., 2017; [[distmult|DistMult]]).

#### 3. Training with negative triples

Knowledge graphs contain only true facts, so training creates negative examples by corrupting observed triples, replacing the head or the tail with a random entity. A margin-based ranking loss requires observed triples to score better than corrupted ones by a margin (Bordes et al., 2013; Wang et al., 2017). The model was trained on a dataset with 1 million entities, 25,000 relationships and more than 17 million training triples (Bordes et al., 2013).

#### 4. Link prediction

To predict a missing tail for (h, r, ?), all entities are ranked by their distance to h + r. TransE outperformed earlier methods on link prediction on WordNet and Freebase (Bordes et al., 2013). Yang et al. (2014) later showed in a unified framework that a simple bilinear model reached a top-10 accuracy of 73.2% on Freebase, compared with 54.7% for TransE.

#### 5. Limitations and extensions

A single translation vector per relation fits one-to-one relations best; for one-to-many, many-to-one and many-to-many relations, different tails would need the same position, which is why extensions such as TransH and TransR project entities into relation-specific spaces (Wang et al., 2017). Symmetric relations are also problematic, since h + r ≈ t and t + r ≈ h force r towards zero; RotatE models relations as rotations in complex space and can represent symmetry, antisymmetry, inversion and composition (Sun et al., 2019; [[rotate|RotatE]]).

#### Origin and variants

TransE (Bordes et al., 2013) started the family of translational embedding models. Wang et al. (2017) survey its extensions, Yang et al. (2014) generalise it within a framework of linear and bilinear models, and RotatE (Sun et al., 2019) generalises translation to rotation.

### When to use it

- As a simple, scalable baseline for link prediction on large knowledge graphs (Bordes et al., 2013).
- When relations are mostly one-to-one and not symmetric (Wang et al., 2017).
- When relation patterns such as symmetry or composition matter, newer models such as RotatE are more suitable (Sun et al., 2019).

### Strengths and limitations

**Strengths**
- Very simple model with few parameters (Bordes et al., 2013).
- Scales to graphs with millions of entities and triples (Bordes et al., 2013).
- Intuitive geometric interpretation of relations as translations (Wang et al., 2017).

**Limitations**
- Weak for one-to-many, many-to-one and many-to-many relations (Wang et al., 2017).
- Cannot represent symmetric relations well (Sun et al., 2019).
- Outperformed by bilinear and complex-valued models on standard benchmarks (Yang et al., 2014; Sun et al., 2019).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| TransE | Relation as translation h + r ≈ t (Bordes et al., 2013) | Simple baseline, one-to-one relations |
| DistMult | Bilinear score with diagonal relation matrix (Yang et al., 2014) | Symmetric relations |
| RotatE | Relation as rotation in complex space (Sun et al., 2019) | Symmetry, inversion and composition |

### In practice

Models are evaluated on link prediction with ranking metrics such as hits@10, in which the correct entity must appear among the top ten candidates (Bordes et al., 2013). Libraries for knowledge graph embeddings implement TransE alongside newer models, so several models can be compared on the same graph (Wang et al., 2017).

### Key takeaway

TransE models a relation as a vector that translates the head entity to the tail entity, a simple and scalable idea that works best for one-to-one relations.

### Sources

- Bordes, A., Usunier, N., Garcia-Durán, A., Weston, J. & Yakhnenko, O. (2013). *Translating Embeddings for Modeling Multi-relational Data.* NeurIPS 2013. [NeurIPS proceedings](https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data)
- Yang, B. et al. (2014). *Embedding Entities and Relations for Learning and Inference in Knowledge Bases.* ICLR 2015. [arXiv:1412.6575](https://arxiv.org/abs/1412.6575)
- Wang, Q., Mao, Z., Wang, B. & Guo, L. (2017). *Knowledge Graph Embedding: A Survey of Approaches and Applications.* IEEE Transactions on Knowledge and Data Engineering 29(12). [doi:10.1109/TKDE.2017.2754499](https://doi.org/10.1109/TKDE.2017.2754499)
- Sun, Z. et al. (2019). *RotatE: Knowledge Graph Embedding by Relational Rotation in Complex Space.* ICLR 2019. [arXiv:1902.10197](https://arxiv.org/abs/1902.10197)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

TransE bettet Entitäten und Beziehungen eines Wissensgraphen als Vektoren ein und modelliert jede Beziehung als Verschiebung (Translation): Für ein wahres Tripel (Kopf, Beziehung, Schwanz) soll der Kopfvektor plus der Beziehungsvektor nahe am Schwanzvektor liegen (Bordes et al., 2013). Es ist einfach, hat wenige Parameter und skaliert auf große Graphen, was es zu einer Standard-Baseline für Link Prediction machte ([[knowledge-graphs|Wissensgraphen]]). Schwierigkeiten hat es mit 1:n-, n:1- und n:m-Beziehungen und mit symmetrischen Beziehungen, die spätere Modelle angehen (Wang et al., 2017; Sun et al., 2019).

### Funktionsweise

Jede Entität und jede Beziehung erhält einen Vektor derselben Dimension. Das Training zieht h + r bei beobachteten Tripeln zu t hin und drückt es bei verfälschten Tripeln, in denen Kopf oder Schwanz ersetzt wurde, davon weg; bei der Vorhersage werden Kandidatenentitäten nach ihrem Abstand gerankt.

```text
1. Translation als Beziehungsmodell
▼
2. Bewertungsfunktion
▼
3. Training mit negativen Tripeln
▼
4. Link Prediction
▼
5. Grenzen und Erweiterungen
```

#### 1. Translation als Beziehungsmodell

Bordes et al. (2013) deuten Beziehungen als Verschiebungen, die auf niedrigdimensionalen Embeddings der Entitäten wirken. Gilt (Berlin, hauptstadtVon, Deutschland), soll der Vektor von Berlin plus der Vektor von hauptstadtVon nahe am Vektor von Deutschland liegen.

#### 2. Bewertungsfunktion

Die Plausibilität eines Tripels wird über den Abstand zwischen h + r und t gemessen, etwa mit der L1- oder L2-Norm: Je kleiner der Abstand, desto plausibler das Tripel (Bordes et al., 2013). TransE gehört zur Familie der translationalen Distanzmodelle, im Unterschied zu Semantic-Matching-Modellen wie DistMult, die Tripel über Ähnlichkeit bewerten (Wang et al., 2017; [[distmult|DistMult]]).

#### 3. Training mit negativen Tripeln

Wissensgraphen enthalten nur wahre Fakten; das Training erzeugt daher negative Beispiele, indem beobachtete Tripel verfälscht werden: Kopf oder Schwanz wird durch eine zufällige Entität ersetzt. Ein margenbasierter Ranking-Verlust verlangt, dass beobachtete Tripel um eine Marge besser bewertet werden als verfälschte (Bordes et al., 2013; Wang et al., 2017). Das Modell wurde auf einem Datensatz mit 1 Million Entitäten, 25.000 Beziehungen und mehr als 17 Millionen Trainingstripeln trainiert (Bordes et al., 2013).

#### 4. Link Prediction

Um einen fehlenden Schwanz für (h, r, ?) vorherzusagen, werden alle Entitäten nach ihrem Abstand zu h + r gerankt. TransE übertraf bei Link Prediction auf WordNet und Freebase frühere Verfahren (Bordes et al., 2013). Yang et al. (2014) zeigten später in einem gemeinsamen Rahmen, dass ein einfaches bilineares Modell auf Freebase eine Top-10-Genauigkeit von 73,2 % erreichte, TransE 54,7 %.

#### 5. Grenzen und Erweiterungen

Ein einziger Verschiebungsvektor je Beziehung passt am besten zu 1:1-Beziehungen; bei 1:n-, n:1- und n:m-Beziehungen müssten verschiedene Schwänze dieselbe Position einnehmen, weshalb Erweiterungen wie TransH und TransR Entitäten in beziehungsspezifische Räume projizieren (Wang et al., 2017). Auch symmetrische Beziehungen sind problematisch, da h + r ≈ t und t + r ≈ h den Vektor r gegen null zwingen; RotatE modelliert Beziehungen als Drehungen im komplexen Raum und kann Symmetrie, Antisymmetrie, Inversion und Komposition darstellen (Sun et al., 2019; [[rotate|RotatE]]).

#### Ursprung und Varianten

TransE (Bordes et al., 2013) begründete die Familie translationaler Embedding-Modelle. Wang et al. (2017) geben einen Überblick über seine Erweiterungen, Yang et al. (2014) verallgemeinern es in einem Rahmen linearer und bilinearer Modelle, und RotatE (Sun et al., 2019) verallgemeinert die Verschiebung zur Drehung.

### Wann einsetzen

- Als einfache, skalierbare Baseline für Link Prediction auf großen Wissensgraphen (Bordes et al., 2013).
- Wenn Beziehungen überwiegend 1:1 und nicht symmetrisch sind (Wang et al., 2017).
- Wenn Beziehungsmuster wie Symmetrie oder Komposition wichtig sind, eignen sich neuere Modelle wie RotatE besser (Sun et al., 2019).

### Stärken und Grenzen

**Stärken**
- Sehr einfaches Modell mit wenigen Parametern (Bordes et al., 2013).
- Skaliert auf Graphen mit Millionen von Entitäten und Tripeln (Bordes et al., 2013).
- Anschauliche geometrische Deutung von Beziehungen als Verschiebungen (Wang et al., 2017).

**Einschränkungen**
- Schwach bei 1:n-, n:1- und n:m-Beziehungen (Wang et al., 2017).
- Kann symmetrische Beziehungen schlecht darstellen (Sun et al., 2019).
- Auf Standard-Benchmarks von bilinearen und komplexwertigen Modellen übertroffen (Yang et al., 2014; Sun et al., 2019).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| TransE | Beziehung als Verschiebung h + r ≈ t (Bordes et al., 2013) | Einfache Baseline, 1:1-Beziehungen |
| DistMult | Bilineare Bewertung mit diagonaler Beziehungsmatrix (Yang et al., 2014) | Symmetrische Beziehungen |
| RotatE | Beziehung als Drehung im komplexen Raum (Sun et al., 2019) | Symmetrie, Inversion und Komposition |

### In der Praxis

Modelle werden bei Link Prediction mit Ranking-Metriken wie Hits@10 bewertet, bei der die richtige Entität unter den zehn besten Kandidaten sein muss (Bordes et al., 2013). Bibliotheken für Knowledge Graph Embeddings implementieren TransE neben neueren Modellen, sodass sich mehrere Modelle auf demselben Graphen vergleichen lassen (Wang et al., 2017).

### Merksatz

TransE modelliert eine Beziehung als Vektor, der die Kopfentität auf die Schwanzentität verschiebt; die Idee ist einfach und skalierbar und funktioniert am besten bei 1:1-Beziehungen.

### Quellen

- Bordes, A., Usunier, N., Garcia-Durán, A., Weston, J. & Yakhnenko, O. (2013). *Translating Embeddings for Modeling Multi-relational Data.* NeurIPS 2013. [NeurIPS proceedings](https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data)
- Yang, B. et al. (2014). *Embedding Entities and Relations for Learning and Inference in Knowledge Bases.* ICLR 2015. [arXiv:1412.6575](https://arxiv.org/abs/1412.6575)
- Wang, Q., Mao, Z., Wang, B. & Guo, L. (2017). *Knowledge Graph Embedding: A Survey of Approaches and Applications.* IEEE Transactions on Knowledge and Data Engineering 29(12). [doi:10.1109/TKDE.2017.2754499](https://doi.org/10.1109/TKDE.2017.2754499)
- Sun, Z. et al. (2019). *RotatE: Knowledge Graph Embedding by Relational Rotation in Complex Space.* ICLR 2019. [arXiv:1902.10197](https://arxiv.org/abs/1902.10197)
