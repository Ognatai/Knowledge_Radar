---
title_en: RotatE
title_de: RotatE
entity_type: Method
sources:
- https://arxiv.org/abs/1902.10197
- https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data
- https://arxiv.org/abs/1412.6575
- https://arxiv.org/abs/1606.06357
- https://arxiv.org/abs/2002.00388
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

RotatE models each relation of a knowledge graph as a rotation in complex vector space: the tail embedding should equal the head embedding rotated element-wise by the relation (Sun et al., 2019). This lets one model represent and infer the main relation patterns, symmetry and antisymmetry, inversion and composition, which earlier models cover only partly (Bordes et al., 2013; Yang et al., 2014; Trouillon et al., 2016). Trained with self-adversarial negative sampling, it outperformed earlier models on link prediction benchmarks.

### How it works

Entities are complex vectors, and each relation is a complex vector whose entries all have modulus 1, i.e. pure rotations. A triple is plausible if rotating the head by the relation lands close to the tail; training contrasts observed triples with negatives that are weighted by how hard they are.

```text
1. Relation patterns
▼
2. Relations as rotations
▼
3. Scoring function
▼
4. Self-adversarial negative sampling
▼
5. Comparison with earlier models
```

#### 1. Relation patterns

Predicting missing links depends on modelling and inferring the patterns of relations (Sun et al., 2019): symmetry (if a relation holds from a to b, it holds from b to a), antisymmetry (it never holds in both directions), inversion (one relation is the reverse of another, such as "parent of" and "child of") and composition (one relation follows from two others, such as "mother's husband" and "father").

#### 2. Relations as rotations

RotatE defines each relation as a rotation from the source entity to the target entity in the complex vector space: t = h ∘ r, where ∘ is the element-wise product and every element of r has modulus 1 (Sun et al., 2019). A rotation by 180° applied twice returns to the start, which captures symmetry; the inverse relation is the opposite rotation; and composing relations corresponds to adding their rotation angles.

#### 3. Scoring function

A triple's plausibility is measured by the distance between the rotated head and the tail, ‖h ∘ r − t‖: the smaller the distance, the more plausible the triple (Sun et al., 2019). This generalises the translational idea of TransE, h + r ≈ t, from vector addition to rotation (Bordes et al., 2013; [[transe|TransE]]).

#### 4. Self-adversarial negative sampling

Uniformly sampled negative triples are often trivially false and contribute little to training. Sun et al. (2019) propose self-adversarial negative sampling, which weights negative samples according to how plausible the current model finds them, so that training focuses on harder negatives; it trains RotatE efficiently and effectively.

#### 5. Comparison with earlier models

TransE cannot model symmetric relations well, DistMult only symmetric ones, and ComplEx covers symmetry, antisymmetry and inversion but not composition (Bordes et al., 2013; Yang et al., 2014; Trouillon et al., 2016). RotatE covers all four patterns, is scalable, and significantly outperformed existing state-of-the-art models on link prediction across several benchmark knowledge graphs (Sun et al., 2019).

#### Origin and variants

RotatE (Sun et al., 2019) builds on translational models (Bordes et al., 2013), bilinear models (Yang et al., 2014) and complex-valued embeddings (Trouillon et al., 2016). Ji et al. (2020) place it among embedding models organised by representation space and scoring function.

### When to use it

- When a knowledge graph contains relations with different patterns, including composition (Sun et al., 2019).
- When link prediction quality matters more than the simplicity of TransE (Sun et al., 2019).
- As a strong baseline in comparisons of knowledge graph embedding models (Ji et al., 2020).

### Strengths and limitations

**Strengths**
- Models symmetry, antisymmetry, inversion and composition (Sun et al., 2019).
- Scalable and significantly better than earlier models on link prediction (Sun et al., 2019).
- Self-adversarial negative sampling makes training more effective (Sun et al., 2019).

**Limitations**
- Each relation is a single rotation, so one-to-many relations remain difficult, as for other distance-based models ([[transe|TransE]]).
- Complex-valued embeddings are less intuitive than real-valued ones (Trouillon et al., 2016).
- Like other embedding models, it only scores entities seen during training (Ji et al., 2020).

### Comparison

| Approach | Symmetry | Antisymmetry | Inversion | Composition |
|----------|----------|--------------|-----------|-------------|
| TransE (Bordes et al., 2013) | no | yes | yes | yes |
| DistMult (Yang et al., 2014) | yes | no | no | no |
| ComplEx (Trouillon et al., 2016) | yes | yes | yes | no |
| RotatE (Sun et al., 2019) | yes | yes | yes | yes |

### In practice

RotatE is evaluated with ranking metrics such as mean reciprocal rank and hits@k on standard link prediction benchmarks, and compared with TransE, DistMult and ComplEx on the same data (Sun et al., 2019; Ji et al., 2020). Predicted links are candidates that should be checked before they are added to a production graph ([[knowledge-graph-engineering|Knowledge Graph Engineering]]).

### Key takeaway

RotatE treats each relation as a rotation in complex space, which lets one model capture symmetry, inversion and composition of relations.

### Sources

- Sun, Z. et al. (2019). *RotatE: Knowledge Graph Embedding by Relational Rotation in Complex Space.* ICLR 2019. [arXiv:1902.10197](https://arxiv.org/abs/1902.10197)
- Bordes, A., Usunier, N., Garcia-Durán, A., Weston, J. & Yakhnenko, O. (2013). *Translating Embeddings for Modeling Multi-relational Data.* NeurIPS 2013. [NeurIPS proceedings](https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data)
- Yang, B. et al. (2014). *Embedding Entities and Relations for Learning and Inference in Knowledge Bases.* ICLR 2015. [arXiv:1412.6575](https://arxiv.org/abs/1412.6575)
- Trouillon, T. et al. (2016). *Complex Embeddings for Simple Link Prediction.* ICML 2016. [arXiv:1606.06357](https://arxiv.org/abs/1606.06357)
- Ji, S. et al. (2020). *A Survey on Knowledge Graphs: Representation, Acquisition and Applications.* IEEE TNNLS 2022. [arXiv:2002.00388](https://arxiv.org/abs/2002.00388)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

RotatE modelliert jede Beziehung eines Wissensgraphen als Drehung im komplexen Vektorraum: Das Schwanz-Embedding soll dem elementweise um die Beziehung gedrehten Kopf-Embedding entsprechen (Sun et al., 2019). So kann ein Modell die wichtigsten Beziehungsmuster darstellen und erschließen, nämlich Symmetrie und Antisymmetrie, Inversion und Komposition, die frühere Modelle nur teilweise abdecken (Bordes et al., 2013; Yang et al., 2014; Trouillon et al., 2016). Mit selbstadversarialem Negative Sampling trainiert, übertraf es frühere Modelle auf Benchmarks für Link Prediction.

### Funktionsweise

Entitäten sind komplexe Vektoren, und jede Beziehung ist ein komplexer Vektor, dessen Einträge alle den Betrag 1 haben, also reine Drehungen. Ein Tripel ist plausibel, wenn der um die Beziehung gedrehte Kopf nahe am Schwanz landet; das Training stellt beobachtete Tripel Negativbeispielen gegenüber, die danach gewichtet werden, wie schwer sie sind.

```text
1. Beziehungsmuster
▼
2. Beziehungen als Drehungen
▼
3. Bewertungsfunktion
▼
4. Selbstadversariales Negative Sampling
▼
5. Vergleich mit früheren Modellen
```

#### 1. Beziehungsmuster

Fehlende Verbindungen vorherzusagen hängt davon ab, die Muster von Beziehungen zu modellieren und zu erschließen (Sun et al., 2019): Symmetrie (gilt eine Beziehung von a nach b, gilt sie auch von b nach a), Antisymmetrie (sie gilt nie in beide Richtungen), Inversion (eine Beziehung ist die Umkehrung einer anderen, etwa „Elternteil von“ und „Kind von“) und Komposition (eine Beziehung folgt aus zwei anderen, etwa „Ehemann der Mutter“ und „Vater“).

#### 2. Beziehungen als Drehungen

RotatE definiert jede Beziehung als Drehung von der Ausgangs- zur Zielentität im komplexen Vektorraum: t = h ∘ r, wobei ∘ das elementweise Produkt ist und jedes Element von r den Betrag 1 hat (Sun et al., 2019). Eine zweimal angewendete Drehung um 180° führt zum Ausgangspunkt zurück, was Symmetrie abbildet; die inverse Beziehung ist die entgegengesetzte Drehung; und das Zusammensetzen von Beziehungen entspricht dem Addieren ihrer Drehwinkel.

#### 3. Bewertungsfunktion

Die Plausibilität eines Tripels wird über den Abstand zwischen gedrehtem Kopf und Schwanz gemessen, ‖h ∘ r − t‖: Je kleiner der Abstand, desto plausibler das Tripel (Sun et al., 2019). Das verallgemeinert die translationale Idee von TransE, h + r ≈ t, von der Vektoraddition auf die Drehung (Bordes et al., 2013; [[transe|TransE]]).

#### 4. Selbstadversariales Negative Sampling

Gleichverteilt gezogene negative Tripel sind oft offensichtlich falsch und tragen wenig zum Training bei. Sun et al. (2019) schlagen selbstadversariales Negative Sampling vor, das Negativbeispiele danach gewichtet, wie plausibel das aktuelle Modell sie findet, sodass sich das Training auf schwierigere Negativbeispiele konzentriert; damit lässt sich RotatE effizient und wirksam trainieren.

#### 5. Vergleich mit früheren Modellen

TransE kann symmetrische Beziehungen schlecht modellieren, DistMult nur symmetrische, und ComplEx deckt Symmetrie, Antisymmetrie und Inversion ab, aber keine Komposition (Bordes et al., 2013; Yang et al., 2014; Trouillon et al., 2016). RotatE deckt alle vier Muster ab, skaliert und übertraf bei Link Prediction auf mehreren Benchmark-Wissensgraphen die bis dahin besten Modelle deutlich (Sun et al., 2019).

#### Ursprung und Varianten

RotatE (Sun et al., 2019) baut auf translationalen Modellen (Bordes et al., 2013), bilinearen Modellen (Yang et al., 2014) und komplexwertigen Embeddings (Trouillon et al., 2016) auf. Ji et al. (2020) ordnen es unter Embedding-Modellen nach Repräsentationsraum und Bewertungsfunktion ein.

### Wann einsetzen

- Wenn ein Wissensgraph Beziehungen mit unterschiedlichen Mustern einschließlich Komposition enthält (Sun et al., 2019).
- Wenn die Qualität der Link Prediction wichtiger ist als die Einfachheit von TransE (Sun et al., 2019).
- Als starke Baseline beim Vergleich von Knowledge-Graph-Embedding-Modellen (Ji et al., 2020).

### Stärken und Grenzen

**Stärken**
- Modelliert Symmetrie, Antisymmetrie, Inversion und Komposition (Sun et al., 2019).
- Skaliert und ist bei Link Prediction deutlich besser als frühere Modelle (Sun et al., 2019).
- Selbstadversariales Negative Sampling macht das Training wirksamer (Sun et al., 2019).

**Einschränkungen**
- Jede Beziehung ist eine einzige Drehung, sodass 1:n-Beziehungen wie bei anderen distanzbasierten Modellen schwierig bleiben ([[transe|TransE]]).
- Komplexwertige Embeddings sind weniger anschaulich als reellwertige (Trouillon et al., 2016).
- Wie andere Embedding-Modelle bewertet es nur Entitäten, die im Training vorkamen (Ji et al., 2020).

### Vergleich

| Ansatz | Symmetrie | Antisymmetrie | Inversion | Komposition |
|----------|----------|--------------|-----------|-------------|
| TransE (Bordes et al., 2013) | nein | ja | ja | ja |
| DistMult (Yang et al., 2014) | ja | nein | nein | nein |
| ComplEx (Trouillon et al., 2016) | ja | ja | ja | nein |
| RotatE (Sun et al., 2019) | ja | ja | ja | ja |

### In der Praxis

RotatE wird mit Ranking-Metriken wie Mean Reciprocal Rank und Hits@k auf Standard-Benchmarks für Link Prediction bewertet und auf denselben Daten mit TransE, DistMult und ComplEx verglichen (Sun et al., 2019; Ji et al., 2020). Vorhergesagte Verbindungen sind Kandidaten, die geprüft werden sollten, bevor sie in einen produktiven Graphen übernommen werden ([[knowledge-graph-engineering|Knowledge Graph Engineering]]).

### Merksatz

RotatE behandelt jede Beziehung als Drehung im komplexen Raum, wodurch ein Modell Symmetrie, Inversion und Komposition von Beziehungen erfassen kann.

### Quellen

- Sun, Z. et al. (2019). *RotatE: Knowledge Graph Embedding by Relational Rotation in Complex Space.* ICLR 2019. [arXiv:1902.10197](https://arxiv.org/abs/1902.10197)
- Bordes, A., Usunier, N., Garcia-Durán, A., Weston, J. & Yakhnenko, O. (2013). *Translating Embeddings for Modeling Multi-relational Data.* NeurIPS 2013. [NeurIPS proceedings](https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data)
- Yang, B. et al. (2014). *Embedding Entities and Relations for Learning and Inference in Knowledge Bases.* ICLR 2015. [arXiv:1412.6575](https://arxiv.org/abs/1412.6575)
- Trouillon, T. et al. (2016). *Complex Embeddings for Simple Link Prediction.* ICML 2016. [arXiv:1606.06357](https://arxiv.org/abs/1606.06357)
- Ji, S. et al. (2020). *A Survey on Knowledge Graphs: Representation, Acquisition and Applications.* IEEE TNNLS 2022. [arXiv:2002.00388](https://arxiv.org/abs/2002.00388)
