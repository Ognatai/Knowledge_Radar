---
title_en: Graph Neural Networks
title_de: Graph Neural Networks
entity_type: Method
aliases:
- Graph neural networks
- Graph neural network
- GNN
- GNNs
- Graph convolutional network
- GCN
- Message passing neural network
- GraphSAGE
- Graph attention network
- GAT
- R-GCN
sources:
- https://arxiv.org/abs/1609.02907
- https://arxiv.org/abs/1704.01212
- https://arxiv.org/abs/1706.02216
- https://arxiv.org/abs/1710.10903
- https://arxiv.org/abs/1810.00826
- https://arxiv.org/abs/1703.06103
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Graph neural networks (GNNs) learn vector representations of nodes, edges or whole graphs by repeatedly aggregating and transforming the representations of each node's neighbours (Xu et al., 2019). The general scheme is message passing: every node collects messages from its neighbours, updates its state, and after several rounds a readout combines node states into a graph-level output (Gilmer et al., 2017). Well-known variants are graph convolutional networks (Kipf & Welling, 2017), GraphSAGE for unseen nodes (Hamilton et al., 2017), graph attention networks (Veličković et al., 2018) and relational GCNs for [[knowledge-graphs|knowledge graphs]] (Schlichtkrull et al., 2018).

### How it works

```text
graph G = (nodes with features x_v, edges with optional features e_vw)
   ▼
h_v⁰ = x_v
for t = 1 … T (one layer per round):
    message   m_v = Σ_{w ∈ N(v)} M_t(h_v, h_w, e_vw)       (aggregate over neighbours)
    update    h_v ← U_t(h_v, m_v)                          (learned, e.g. MLP or GRU)
   ▼
node tasks: classify h_v      edge tasks: score (h_u, h_v)      graph tasks: ŷ = R({h_v})  (permutation-invariant readout)
```

#### 1. Message passing

Gilmer et al. (2017) unified earlier models in the message passing neural network (MPNN) framework: in each of T steps, a node v sums messages `M_t(h_v, h_w, e_vw)` from its neighbours w and updates its state with `U_t`; a readout function R then computes a graph-level vector. M, U and R are learned differentiable functions, and R must be invariant to the order of the nodes so that the model is invariant to graph isomorphism (Gilmer et al., 2017). After k layers, a node's representation depends on its k-hop neighbourhood.

#### 2. Graph convolutional networks

Kipf and Welling (2017) motivated a simple layer from a first-order approximation of spectral graph convolutions: `H^(l+1) = σ(D̃^(-1/2) Ã D̃^(-1/2) H^(l) W^(l))`, where `Ã = A + I` is the adjacency matrix with self-loops, D̃ its degree matrix and W a trainable weight matrix. The normalisation keeps repeated application numerically stable, and the cost grows linearly with the number of edges; a two-layer GCN outperformed related methods for semi-supervised node classification on citation networks and a knowledge graph data set (Kipf & Welling, 2017).

#### 3. Sampling and attention

GCN as proposed is transductive: all nodes must be present during training. GraphSAGE instead learns functions that sample a fixed-size set of neighbours and aggregate their features, for example with a mean, an [[lstm|LSTM]] or a pooling aggregator, so it can embed nodes and even whole graphs unseen in training (Hamilton et al., 2017). Graph attention networks weight neighbours by learned attention coefficients computed with a small feed-forward network and a [[softmax|softmax]] over the neighbourhood, without costly matrix operations or knowledge of the whole graph structure in advance (Veličković et al., 2018; [[attention-and-transformers|attention]]).

#### 4. How expressive are GNNs?

Xu et al. (2019) related GNNs to the Weisfeiler–Lehman graph isomorphism test: a GNN can at most distinguish what this test distinguishes, and only if its aggregation is injective on multisets of neighbour features. Mean and max aggregators lose information (mean captures proportions, max ignores multiplicities), so GCN and GraphSAGE cannot distinguish certain simple structures; the Graph Isomorphism Network (GIN) uses sum aggregation followed by an MLP and is provably as powerful as the test (Xu et al., 2019).

#### 5. GNNs on knowledge graphs

Relational GCNs use a separate transformation per relation type to handle the many relations of knowledge bases; as an encoder for [[distmult|DistMult]] link prediction they improved results by 29.8% on FB15k-237 over a decoder-only baseline, and they also classify entities (Schlichtkrull et al., 2018; [[knowledge-graph-embeddings|knowledge graph embeddings]]).

#### Origin and variants

GCN appeared at ICLR 2017 (Kipf & Welling, 2017), MPNN at ICML 2017 (Gilmer et al., 2017), GraphSAGE at NeurIPS 2017 (Hamilton et al., 2017), GAT at ICLR 2018 (Veličković et al., 2018) and GIN at ICLR 2019 (Xu et al., 2019). MPNNs were applied to molecular property prediction in quantum chemistry (Gilmer et al., 2017).

### When to use it

- Data whose structure is a graph: citation networks, social networks such as Reddit, molecules and protein interactions (Kipf & Welling, 2017; Gilmer et al., 2017; Hamilton et al., 2017).
- Node classification, link prediction and knowledge graph completion (Schlichtkrull et al., 2018; [[knowledge-graphs|knowledge graphs]]).
- Graph classification, for example of molecules (Gilmer et al., 2017; Xu et al., 2019).
- Recommendation and other tasks on large graphs with new nodes, using inductive methods (Hamilton et al., 2017).

### Strengths and limitations

**Strengths**
- Use both node features and graph structure (Kipf & Welling, 2017).
- Invariant to node ordering by construction (Gilmer et al., 2017).
- Inductive variants generalise to unseen nodes and graphs (Hamilton et al., 2017).

**Limitations**
- Expressive power is bounded by the Weisfeiler–Lehman test, and common aggregators fall below it (Xu et al., 2019).
- Each layer only reaches one hop further, so long-range dependencies need many layers.
- Full-graph training needs the whole graph in memory; sampling methods such as GraphSAGE trade exactness for scalability (Hamilton et al., 2017).

### Comparison

| Model | Aggregation | Inductive | Note |
|---|---|---|---|
| GCN | normalised sum over neighbours | no (as proposed) | simple, linear in edges |
| GraphSAGE | sampled neighbours, mean/LSTM/pool | yes | large evolving graphs |
| GAT | attention-weighted neighbours | yes | learned neighbour importance |
| GIN | sum + MLP | yes | as powerful as WL test |
| R-GCN | one transform per relation | – | multi-relational knowledge graphs |

Sources: Kipf & Welling (2017), Hamilton et al. (2017), Veličković et al. (2018), Xu et al. (2019), Schlichtkrull et al. (2018).

### In practice

In the original GCN experiments a two-layer model was the default, with deeper models up to 10 layers examined separately (Kipf & Welling, 2017). For text-heavy graphs, node features can come from [[embeddings|text embeddings]] (Hamilton et al., 2017 used text attributes as node features).

### Key takeaway

GNNs pass messages along edges so that each node's representation summarises its neighbourhood; GCN, GraphSAGE, GAT and GIN differ mainly in how they aggregate, which also bounds what they can distinguish.

### Sources

- Kipf, T. N. & Welling, M. (2017). *Semi-Supervised Classification with Graph Convolutional Networks.* ICLR 2017. [arXiv:1609.02907](https://arxiv.org/abs/1609.02907)
- Gilmer, J., Schoenholz, S. S., Riley, P. F., Vinyals, O. & Dahl, G. E. (2017). *Neural Message Passing for Quantum Chemistry.* ICML 2017. [arXiv:1704.01212](https://arxiv.org/abs/1704.01212)
- Hamilton, W. L., Ying, R. & Leskovec, J. (2017). *Inductive Representation Learning on Large Graphs.* NeurIPS 2017. [arXiv:1706.02216](https://arxiv.org/abs/1706.02216)
- Veličković, P. et al. (2018). *Graph Attention Networks.* ICLR 2018. [arXiv:1710.10903](https://arxiv.org/abs/1710.10903)
- Xu, K., Hu, W., Leskovec, J. & Jegelka, S. (2019). *How Powerful are Graph Neural Networks?* ICLR 2019. [arXiv:1810.00826](https://arxiv.org/abs/1810.00826)
- Schlichtkrull, M. et al. (2018). *Modeling Relational Data with Graph Convolutional Networks.* ESWC 2018. [arXiv:1703.06103](https://arxiv.org/abs/1703.06103)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Graph Neural Networks (GNNs) lernen Vektorrepräsentationen von Knoten, Kanten oder ganzen Graphen, indem sie die Repräsentationen der Nachbarn jedes Knotens wiederholt aggregieren und transformieren (Xu et al., 2019). Das allgemeine Schema ist Message Passing: Jeder Knoten sammelt Nachrichten seiner Nachbarn, aktualisiert seinen Zustand, und nach mehreren Runden fasst ein Readout die Knotenzustände zu einer Ausgabe für den ganzen Graphen zusammen (Gilmer et al., 2017). Bekannte Varianten sind Graph Convolutional Networks (Kipf & Welling, 2017), GraphSAGE für ungesehene Knoten (Hamilton et al., 2017), Graph Attention Networks (Veličković et al., 2018) und relationale GCNs für [[knowledge-graphs|Knowledge Graphs]] (Schlichtkrull et al., 2018).

### Funktionsweise

```text
Graph G = (Knoten mit Merkmalen x_v, Kanten mit optionalen Merkmalen e_vw)
   ▼
h_v⁰ = x_v
für t = 1 … T (eine Schicht pro Runde):
    Nachricht    m_v = Σ_{w ∈ N(v)} M_t(h_v, h_w, e_vw)     (über Nachbarn aggregieren)
    Update       h_v ← U_t(h_v, m_v)                        (gelernt, z. B. MLP oder GRU)
   ▼
Knotenaufgaben: h_v klassifizieren   Kantenaufgaben: (h_u, h_v) bewerten   Graphaufgaben: ŷ = R({h_v})  (permutationsinvarianter Readout)
```

#### 1. Message Passing

Gilmer et al. (2017) vereinheitlichten frühere Modelle im Rahmen der Message Passing Neural Networks (MPNN): In jedem von T Schritten summiert ein Knoten v Nachrichten `M_t(h_v, h_w, e_vw)` seiner Nachbarn w und aktualisiert seinen Zustand mit `U_t`; eine Readout-Funktion R berechnet dann einen Vektor für den ganzen Graphen. M, U und R sind gelernte differenzierbare Funktionen, und R muss gegenüber der Reihenfolge der Knoten invariant sein, damit das Modell invariant gegenüber Graphisomorphie ist (Gilmer et al., 2017). Nach k Schichten hängt die Repräsentation eines Knotens von seiner k-Hop-Nachbarschaft ab.

#### 2. Graph Convolutional Networks

Kipf und Welling (2017) leiteten eine einfache Schicht aus einer Approximation erster Ordnung spektraler Graphfaltungen her: `H^(l+1) = σ(D̃^(-1/2) Ã D̃^(-1/2) H^(l) W^(l))`, mit `Ã = A + I` als Adjazenzmatrix mit Selbstschleifen, D̃ ihrer Gradmatrix und W einer trainierbaren Gewichtsmatrix. Die Normalisierung hält die wiederholte Anwendung numerisch stabil, und der Aufwand wächst linear mit der Zahl der Kanten; ein zweischichtiges GCN übertraf verwandte Verfahren bei der semi-überwachten Knotenklassifikation auf Zitationsnetzen und einem Knowledge-Graph-Datensatz (Kipf & Welling, 2017).

#### 3. Sampling und Attention

GCN ist in der vorgeschlagenen Form transduktiv: Alle Knoten müssen beim Training vorhanden sein. GraphSAGE lernt stattdessen Funktionen, die eine feste Zahl von Nachbarn ziehen und deren Merkmale aggregieren, etwa mit Mittelwert, [[lstm|LSTM]] oder Pooling, und kann so Knoten und sogar ganze Graphen einbetten, die beim Training nicht vorkamen (Hamilton et al., 2017). Graph Attention Networks gewichten Nachbarn mit gelernten Attention-Koeffizienten, berechnet mit einem kleinen Feedforward-Netz und einer [[softmax|Softmax]] über die Nachbarschaft, ohne aufwendige Matrixoperationen oder Kenntnis der ganzen Graphstruktur im Voraus (Veličković et al., 2018; [[attention-and-transformers|Attention]]).

#### 4. Wie ausdrucksstark sind GNNs?

Xu et al. (2019) setzten GNNs mit dem Weisfeiler-Lehman-Test auf Graphisomorphie in Beziehung: Ein GNN kann höchstens unterscheiden, was dieser Test unterscheidet, und nur, wenn seine Aggregation auf Multimengen von Nachbarmerkmalen injektiv ist. Mittelwert- und Maximum-Aggregation verlieren Information (der Mittelwert erfasst Anteile, das Maximum ignoriert Vielfachheiten), sodass GCN und GraphSAGE bestimmte einfache Strukturen nicht unterscheiden können; das Graph Isomorphism Network (GIN) nutzt Summen-Aggregation gefolgt von einem MLP und ist beweisbar so mächtig wie der Test (Xu et al., 2019).

#### 5. GNNs auf Knowledge Graphs

Relationale GCNs nutzen pro Relationstyp eine eigene Transformation, um die vielen Relationen von Wissensbasen zu verarbeiten; als Encoder für die Link-Vorhersage mit [[distmult|DistMult]] verbesserten sie die Ergebnisse auf FB15k-237 um 29,8 % gegenüber einer Baseline nur mit Decoder, und sie klassifizieren außerdem Entitäten (Schlichtkrull et al., 2018; [[knowledge-graph-embeddings|Knowledge-Graph-Embeddings]]).

#### Ursprung und Varianten

GCN erschien auf der ICLR 2017 (Kipf & Welling, 2017), MPNN auf der ICML 2017 (Gilmer et al., 2017), GraphSAGE auf der NeurIPS 2017 (Hamilton et al., 2017), GAT auf der ICLR 2018 (Veličković et al., 2018) und GIN auf der ICLR 2019 (Xu et al., 2019). MPNNs wurden zur Vorhersage von Moleküleigenschaften in der Quantenchemie eingesetzt (Gilmer et al., 2017).

### Wann einsetzen

- Daten, deren Struktur ein Graph ist: Zitationsnetze, soziale Netze wie Reddit, Moleküle und Proteininteraktionen (Kipf & Welling, 2017; Gilmer et al., 2017; Hamilton et al., 2017).
- Knotenklassifikation, Link-Vorhersage und Vervollständigung von Knowledge Graphs (Schlichtkrull et al., 2018; [[knowledge-graphs|Knowledge Graphs]]).
- Klassifikation ganzer Graphen, etwa von Molekülen (Gilmer et al., 2017; Xu et al., 2019).
- Empfehlungen und andere Aufgaben auf großen Graphen mit neuen Knoten, mit induktiven Verfahren (Hamilton et al., 2017).

### Stärken und Grenzen

**Stärken**
- Nutzen sowohl Knotenmerkmale als auch die Graphstruktur (Kipf & Welling, 2017).
- Durch ihre Konstruktion invariant gegenüber der Reihenfolge der Knoten (Gilmer et al., 2017).
- Induktive Varianten generalisieren auf ungesehene Knoten und Graphen (Hamilton et al., 2017).

**Grenzen**
- Die Ausdrucksstärke ist durch den Weisfeiler-Lehman-Test begrenzt, und verbreitete Aggregationen bleiben darunter (Xu et al., 2019).
- Jede Schicht reicht nur einen Hop weiter, sodass weitreichende Abhängigkeiten viele Schichten brauchen.
- Training auf dem ganzen Graphen braucht ihn vollständig im Speicher; Sampling-Verfahren wie GraphSAGE tauschen Exaktheit gegen Skalierbarkeit (Hamilton et al., 2017).

### Vergleich

| Modell | Aggregation | Induktiv | Bemerkung |
|---|---|---|---|
| GCN | normalisierte Summe über Nachbarn | nein (wie vorgeschlagen) | einfach, linear in den Kanten |
| GraphSAGE | gezogene Nachbarn, Mittelwert/LSTM/Pooling | ja | große, sich verändernde Graphen |
| GAT | attention-gewichtete Nachbarn | ja | gelernte Wichtigkeit der Nachbarn |
| GIN | Summe + MLP | ja | so mächtig wie der WL-Test |
| R-GCN | eine Transformation pro Relation | – | multirelationale Knowledge Graphs |

Quellen: Kipf & Welling (2017), Hamilton et al. (2017), Veličković et al. (2018), Xu et al. (2019), Schlichtkrull et al. (2018).

### In der Praxis

In den ursprünglichen GCN-Experimenten war ein zweischichtiges Modell die Voreinstellung, tiefere Modelle bis 10 Schichten wurden gesondert untersucht (Kipf & Welling, 2017). Bei textlastigen Graphen können Knotenmerkmale aus [[embeddings|Text-Embeddings]] stammen (Hamilton et al., 2017 nutzten Textattribute als Knotenmerkmale).

### Merksatz

GNNs reichen Nachrichten entlang der Kanten weiter, sodass die Repräsentation jedes Knotens seine Nachbarschaft zusammenfasst; GCN, GraphSAGE, GAT und GIN unterscheiden sich vor allem in der Aggregation, die auch begrenzt, was sie unterscheiden können.

### Quellen

- Kipf, T. N. & Welling, M. (2017). *Semi-Supervised Classification with Graph Convolutional Networks.* ICLR 2017. [arXiv:1609.02907](https://arxiv.org/abs/1609.02907)
- Gilmer, J., Schoenholz, S. S., Riley, P. F., Vinyals, O. & Dahl, G. E. (2017). *Neural Message Passing for Quantum Chemistry.* ICML 2017. [arXiv:1704.01212](https://arxiv.org/abs/1704.01212)
- Hamilton, W. L., Ying, R. & Leskovec, J. (2017). *Inductive Representation Learning on Large Graphs.* NeurIPS 2017. [arXiv:1706.02216](https://arxiv.org/abs/1706.02216)
- Veličković, P. et al. (2018). *Graph Attention Networks.* ICLR 2018. [arXiv:1710.10903](https://arxiv.org/abs/1710.10903)
- Xu, K., Hu, W., Leskovec, J. & Jegelka, S. (2019). *How Powerful are Graph Neural Networks?* ICLR 2019. [arXiv:1810.00826](https://arxiv.org/abs/1810.00826)
- Schlichtkrull, M. et al. (2018). *Modeling Relational Data with Graph Convolutional Networks.* ESWC 2018. [arXiv:1703.06103](https://arxiv.org/abs/1703.06103)
