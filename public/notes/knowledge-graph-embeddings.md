---
title_en: Knowledge Graph Embeddings
title_de: Knowledge Graph Embeddings
entity_type: Method
aliases:
- Knowledge graph embedding
- KGE
- Link prediction
sources:
- https://arxiv.org/abs/2003.02320
- https://arxiv.org/abs/2006.13365
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Knowledge graph embeddings map the entities and relations of a [[knowledge-graphs|knowledge graph]] to low-dimensional vectors, trained so that a scoring function gives true edges a high plausibility and corrupted edges a low one (Hogan et al., 2021). The embeddings are used to complete missing edges (link prediction), to assign confidence to extracted edges and to find similar or duplicate entities. The main families are translational models such as TransE and RotatE, tensor decomposition models such as DistMult and ComplEx, neural models, models built on word-embedding techniques, and models that also use ontologies or rules (Hogan et al., 2021). A large reproduction study found that training approach, loss function and the modelling of inverse relations matter as much as the architecture (Ali et al., 2021).

### How it works

```text
knowledge graph (subject, relation, object) edges
 ▼
positive edges + negative edges (subject or object replaced)
 ▼
scoring function f(e_s, r_p, e_o)   translational · tensor decomposition · neural
 ▼
train embeddings: high score for positives, low for negatives
 ▼
uses: link prediction (rank candidate entities) · edge confidence · entity similarity
evaluation: rank of the true entity → MR, MRR, Hits@k
```

#### 1. Plausibility scoring and self-supervision

Each entity and relation gets a vector of dimension d. A scoring function estimates how plausible an edge (s, p, o) is; training maximises the plausibility of edges in the graph and minimises it for negative examples, usually edges with the subject or object changed so that they are no longer in the graph. The resulting embeddings are learnt through self-supervision and encode latent features of the graph (Hogan et al., 2021).

#### 2. Translational models

Translational models read a relation as a transformation from subject to object. [[transe|TransE]] learns vectors such that e_s + r_p is as close as possible to e_o for true edges and far from it for negatives. It can be too simple: a relation with many objects pushes all of them towards the same vector, and cyclical relations tend to get a zero vector. TransH and TransR project entities into relation-specific hyperplanes or spaces before the translation; [[rotate|RotatE]] translates in complex space, which captures direction, symmetry, inversion, antisymmetry and composition of relations (Hogan et al., 2021).

#### 3. Tensor decomposition models

A graph can be written as a sparse 3-order tensor of nodes × relations × nodes, which rank decompositions approximate with latent factors. [[distmult|DistMult]] scores an edge as the sum of the element-wise product of e_s, r_p and e_o; this equals a canonical polyadic decomposition in which each entity has one vector used twice, so it scores (s, p, o) and (o, p, s) the same and ignores edge direction. RESCAL uses a matrix per relation and can capture direction at a higher cost; [[complex|ComplEx]] uses complex-valued vectors to break DistMult's symmetry with few parameters; TuckER, based on a Tucker decomposition, gave state-of-the-art results on standard benchmarks at the time of the survey (Hogan et al., 2021).

#### 4. Neural, language-based and entailment-aware models

Neural models learn non-linear scoring functions: early proposals such as Neural Tensor Networks have many parameters and limited scalability, while convolutional models such as ConvE and HypER share parameters. Language-based models reuse word-embedding methods: RDF2Vec feeds random walks over the graph as "sentences" into word2vec, KGloVe adapts GloVe. Entailment-aware models such as KALE use ontology definitions or rules, for example through t-norm fuzzy logics, to refine the embeddings (Hogan et al., 2021).

#### 5. Evaluation of link prediction

For each test edge, the model ranks the true entity against all candidates. Common measures are the mean rank (MR), the adjusted mean rank, which corrects for chance, the mean reciprocal rank (MRR) and Hits@k, the share of test edges whose true entity is among the top k. Codebases compute ranks differently, for example when several candidates share a score, which can change results significantly, so optimistic, pessimistic and realistic rank definitions should be distinguished (Ali et al., 2021). Benchmarks need care: about 81% of the FB15K test edges and about 94% of the WN18 test edges are inverses of training edges, which lets even simple rule-based systems compete; FB15K-237 and WN18RR remove these inverse relations (Ali et al., 2021).

#### Origin and variants

TransE was the first and most elementary translational model; TransH, TransR, TransD, RotatE and the hyperbolic MuRP extend it, while RESCAL, DistMult, HolE, ComplEx, SimplE and TuckER come from tensor decomposition (Hogan et al., 2021). Ali et al. (2021) re-implemented 21 models in the PyKEEN library and ran several thousand experiments with 24,804 GPU hours.

### When to use it

- Completing an incomplete knowledge graph by predicting missing edges (Hogan et al., 2021; Ali et al., 2021).
- Assigning confidence to edges extracted from external sources before adding them (Hogan et al., 2021).
- Finding similar or duplicate entities and making recommendations from vector similarity (Hogan et al., 2021).

### Strengths and limitations

**Strengths**
- Learnt from the graph itself through self-supervision, without labelled data (Hogan et al., 2021).
- Several older architectures reach results competitive with the state of the art when configured carefully (Ali et al., 2021).

**Limitations**
- Simple models cannot represent all relation patterns: TransE struggles with one-to-many and cyclical relations, DistMult ignores edge direction (Hogan et al., 2021).
- Published results are often hard to reproduce: some could only be reproduced with other hyperparameters, some not at all (Ali et al., 2021).
- Benchmarks with test leakage and inconsistent rank definitions can make results look better than they are (Ali et al., 2021).

### Comparison

| Family | Idea | Examples |
|--------|------|----------|
| Translational | Relation translates subject to object | TransE, TransH, TransR, RotatE |
| Tensor decomposition | Low-rank factors of the graph tensor | RESCAL, DistMult, ComplEx, TuckER |
| Neural | Learnt non-linear scoring function | NTN, ConvE, HypER |
| Language-based | Word-embedding methods on graph walks | RDF2Vec, KGloVe |
| Entailment-aware | Embeddings constrained by rules or ontologies | KALE |

Source: Hogan et al. (2021).

### In practice

Training choices such as the loss function, negative sampling and the explicit modelling of inverse relations should be tuned and reported together with the architecture, and results compared on FB15K-237 or WN18RR with a stated rank definition (Ali et al., 2021). The ranking measures are the same as in retrieval ([[rag-retrieval-evaluation|RAG: Retrieval Evaluation]]); knowledge graphs themselves can be stored and queried in a [[graph-databases|graph database]] (Hogan et al., 2021).

### Key takeaway

Knowledge graph embeddings learn vectors for entities and relations so that a scoring function separates true from corrupted edges; they predict missing links, but their quality depends as much on training and evaluation choices as on the model family.

### Sources

- Hogan, A. et al. (2021). *Knowledge Graphs.* ACM Computing Surveys 54(4). [arXiv:2003.02320](https://arxiv.org/abs/2003.02320)
- Ali, M. et al. (2021). *Bringing Light Into the Dark: A Large-scale Evaluation of Knowledge Graph Embedding Models under a Unified Framework.* IEEE Transactions on Pattern Analysis and Machine Intelligence. [arXiv:2006.13365](https://arxiv.org/abs/2006.13365)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Knowledge Graph Embeddings bilden die Entitäten und Relationen eines [[knowledge-graphs|Knowledge Graphs]] auf niedrigdimensionale Vektoren ab, die so trainiert werden, dass eine Bewertungsfunktion wahren Kanten eine hohe und verfälschten Kanten eine niedrige Plausibilität gibt (Hogan et al., 2021). Die Embeddings dienen dazu, fehlende Kanten zu ergänzen (Link Prediction), extrahierten Kanten eine Konfidenz zuzuweisen und ähnliche oder doppelte Entitäten zu finden. Die wichtigsten Familien sind translationale Modelle wie TransE und RotatE, Tensorzerlegungsmodelle wie DistMult und ComplEx, neuronale Modelle, Modelle auf Basis von Wort-Embedding-Verfahren und Modelle, die zusätzlich Ontologien oder Regeln nutzen (Hogan et al., 2021). Eine große Reproduktionsstudie ergab, dass Trainingsverfahren, Verlustfunktion und die Modellierung inverser Relationen ebenso viel ausmachen wie die Architektur (Ali et al., 2021).

### Funktionsweise

```text
Knowledge Graph mit Kanten (Subjekt, Relation, Objekt)
 ▼
positive Kanten + negative Kanten (Subjekt oder Objekt ersetzt)
 ▼
Bewertungsfunktion f(e_s, r_p, e_o)   translational · Tensorzerlegung · neuronal
 ▼
Embeddings trainieren: hoher Wert für positive, niedriger für negative Kanten
 ▼
Einsatz: Link Prediction (Kandidaten ranken) · Kantenkonfidenz · Entitätsähnlichkeit
Evaluation: Rang der wahren Entität → MR, MRR, Hits@k
```

#### 1. Plausibilitätsbewertung und Selbstüberwachung

Jede Entität und Relation erhält einen Vektor der Dimension d. Eine Bewertungsfunktion schätzt, wie plausibel eine Kante (s, p, o) ist; das Training maximiert die Plausibilität der Kanten im Graphen und minimiert sie für negative Beispiele, meist Kanten, deren Subjekt oder Objekt so geändert wurde, dass sie nicht mehr im Graphen stehen. Die Embeddings werden so selbstüberwacht gelernt und kodieren latente Merkmale des Graphen (Hogan et al., 2021).

#### 2. Translationale Modelle

Translationale Modelle verstehen eine Relation als Verschiebung vom Subjekt zum Objekt. [[transe|TransE]] lernt Vektoren so, dass e_s + r_p für wahre Kanten möglichst nah an e_o liegt und für negative weit davon entfernt. Das kann zu einfach sein: Eine Relation mit vielen Objekten drückt alle zum selben Vektor, und zyklische Relationen erhalten tendenziell einen Nullvektor. TransH und TransR projizieren Entitäten vor der Verschiebung in relationsspezifische Hyperebenen oder Räume; [[rotate|RotatE]] verschiebt im komplexen Raum und erfasst damit Richtung, Symmetrie, Inversion, Antisymmetrie und Komposition von Relationen (Hogan et al., 2021).

#### 3. Tensorzerlegungsmodelle

Ein Graph lässt sich als dünn besetzter Tensor dritter Ordnung aus Knoten × Relationen × Knoten schreiben, den Rangzerlegungen mit latenten Faktoren annähern. [[distmult|DistMult]] bewertet eine Kante als Summe des elementweisen Produkts von e_s, r_p und e_o; das entspricht einer kanonischen polyadischen Zerlegung, in der jede Entität einen Vektor hat, der doppelt verwendet wird, daher bewertet es (s, p, o) und (o, p, s) gleich und ignoriert die Kantenrichtung. RESCAL nutzt eine Matrix pro Relation und kann die Richtung zu höheren Kosten erfassen; [[complex|ComplEx]] verwendet komplexwertige Vektoren, um die Symmetrie von DistMult mit wenigen Parametern aufzubrechen; TuckER, das auf einer Tucker-Zerlegung beruht, lieferte zum Zeitpunkt des Überblicks die besten Ergebnisse auf Standard-Benchmarks (Hogan et al., 2021).

#### 4. Neuronale, sprachbasierte und folgerungsbewusste Modelle

Neuronale Modelle lernen nichtlineare Bewertungsfunktionen: Frühe Vorschläge wie Neural Tensor Networks haben viele Parameter und skalieren schlecht, während faltende Modelle wie ConvE und HypER Parameter teilen. Sprachbasierte Modelle nutzen Wort-Embedding-Verfahren: RDF2Vec gibt Zufallspfade über den Graphen als „Sätze“ in word2vec, KGloVe passt GloVe an. Folgerungsbewusste Modelle wie KALE verfeinern die Embeddings mit Ontologie-Definitionen oder Regeln, etwa über t-Norm-Fuzzy-Logiken (Hogan et al., 2021).

#### 5. Evaluation der Link Prediction

Für jede Testkante rankt das Modell die wahre Entität gegen alle Kandidaten. Übliche Maße sind der Mean Rank (MR), der um Zufall bereinigte Adjusted Mean Rank, der Mean Reciprocal Rank (MRR) und Hits@k, der Anteil der Testkanten, deren wahre Entität unter den ersten k liegt. Codebasen berechnen Ränge unterschiedlich, etwa wenn mehrere Kandidaten denselben Wert haben, was die Ergebnisse deutlich verändern kann; daher sollten optimistische, pessimistische und realistische Rangdefinitionen unterschieden werden (Ali et al., 2021). Benchmarks brauchen Sorgfalt: Etwa 81 % der FB15K-Testkanten und etwa 94 % der WN18-Testkanten sind Inverse von Trainingskanten, sodass selbst einfache regelbasierte Systeme mithalten; FB15K-237 und WN18RR entfernen diese inversen Relationen (Ali et al., 2021).

#### Herkunft und Varianten

TransE war das erste und einfachste translationale Modell; TransH, TransR, TransD, RotatE und das hyperbolische MuRP erweitern es, während RESCAL, DistMult, HolE, ComplEx, SimplE und TuckER aus der Tensorzerlegung stammen (Hogan et al., 2021). Ali et al. (2021) implementierten 21 Modelle in der Bibliothek PyKEEN neu und führten mehrere tausend Experimente mit 24.804 GPU-Stunden durch.

### Wann einsetzen

- Einen unvollständigen Knowledge Graph ergänzen, indem fehlende Kanten vorhergesagt werden (Hogan et al., 2021; Ali et al., 2021).
- Aus externen Quellen extrahierten Kanten vor dem Hinzufügen eine Konfidenz zuweisen (Hogan et al., 2021).
- Ähnliche oder doppelte Entitäten finden und Empfehlungen aus Vektorähnlichkeit ableiten (Hogan et al., 2021).

### Stärken und Grenzen

**Stärken**
- Selbstüberwacht aus dem Graphen gelernt, ohne gelabelte Daten (Hogan et al., 2021).
- Mehrere ältere Architekturen erreichen bei sorgfältiger Konfiguration Ergebnisse auf dem Stand der Technik (Ali et al., 2021).

**Grenzen**
- Einfache Modelle können nicht alle Relationsmuster darstellen: TransE hat Probleme mit 1:n- und zyklischen Relationen, DistMult ignoriert die Kantenrichtung (Hogan et al., 2021).
- Veröffentlichte Ergebnisse sind oft schwer zu reproduzieren: Manche ließen sich nur mit anderen Hyperparametern, manche gar nicht reproduzieren (Ali et al., 2021).
- Benchmarks mit Test-Leakage und uneinheitliche Rangdefinitionen können Ergebnisse besser aussehen lassen, als sie sind (Ali et al., 2021).

### Vergleich

| Familie | Idee | Beispiele |
|---------|------|-----------|
| Translational | Relation verschiebt Subjekt zum Objekt | TransE, TransH, TransR, RotatE |
| Tensorzerlegung | Niedrigrangige Faktoren des Graphtensors | RESCAL, DistMult, ComplEx, TuckER |
| Neuronal | Gelernte nichtlineare Bewertungsfunktion | NTN, ConvE, HypER |
| Sprachbasiert | Wort-Embedding-Verfahren auf Graphpfaden | RDF2Vec, KGloVe |
| Folgerungsbewusst | Durch Regeln oder Ontologien beschränkte Embeddings | KALE |

Quelle: Hogan et al. (2021).

### In der Praxis

Trainingsentscheidungen wie Verlustfunktion, Negative Sampling und die explizite Modellierung inverser Relationen sollten zusammen mit der Architektur abgestimmt und berichtet werden, und Ergebnisse sollten auf FB15K-237 oder WN18RR mit angegebener Rangdefinition verglichen werden (Ali et al., 2021). Die Rangmaße sind dieselben wie im Retrieval ([[rag-retrieval-evaluation|RAG: Evaluation des Retrievals]]); Knowledge Graphs selbst lassen sich in einer [[graph-databases|Graphdatenbank]] speichern und abfragen (Hogan et al., 2021).

### Merksatz

Knowledge Graph Embeddings lernen Vektoren für Entitäten und Relationen, sodass eine Bewertungsfunktion wahre von verfälschten Kanten trennt; sie sagen fehlende Links vorher, doch ihre Qualität hängt ebenso von Trainings- und Evaluationsentscheidungen ab wie von der Modellfamilie.

### Quellen

- Hogan, A. et al. (2021). *Knowledge Graphs.* ACM Computing Surveys 54(4). [arXiv:2003.02320](https://arxiv.org/abs/2003.02320)
- Ali, M. et al. (2021). *Bringing Light Into the Dark: A Large-scale Evaluation of Knowledge Graph Embedding Models under a Unified Framework.* IEEE Transactions on Pattern Analysis and Machine Intelligence. [arXiv:2006.13365](https://arxiv.org/abs/2006.13365)
