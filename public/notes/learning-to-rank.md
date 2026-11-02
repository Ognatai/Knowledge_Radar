---
title_en: Learning to Rank
title_de: Learning to Rank
entity_type: Method
aliases:
- Learning to rank
- LTR
- Machine-learned ranking
- RankNet
- LambdaRank
- LambdaMART
- Ranking SVM
- RankSVM
sources:
- https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/MSR-TR-2010-82.pdf
- https://www.cs.cornell.edu/people/tj/publications/joachims_02c.pdf
- https://arxiv.org/abs/1901.04085
- https://arxiv.org/abs/1306.2597
- https://arxiv.org/abs/1205.2618
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Learning to rank trains a model to order a list of candidates, such as documents for a query or items for a user, so that the most relevant come first (Burges, 2010). Instead of predicting an absolute label, many methods learn from pairs, document A should be ranked above document B, which can come from relevance judgements or from clicks (Joachims, 2002), and some optimise ranking metrics such as NDCG that weight the top positions most (Burges, 2010). Ensembles of LambdaMART, a boosted-tree ranker, won the 2010 Yahoo! Learning to Rank Challenge (Burges, 2010), and today fine-tuned Transformers re-rank the candidates of a first-stage retriever (Nogueira & Cho, 2019).

### How it works

```text
query q + candidate documents d_1 … d_n (from a first-stage retriever such as BM25 or dense retrieval)
   ▼  features per (q, d): BM25 score, field matches, link and click signals …  or the raw text pair
model s(q, d) ──► score per document ──► sort
   ▼  training signal
   pointwise: relevance label per document (e.g. relevant / not relevant)
   pairwise:  preferences d_i ≻ d_j from judgements or clicks       (RankSVM, RankNet, BPR)
   metric-aware: weight pair gradients by the change in NDCG          (LambdaRank, LambdaMART)
   ▼
evaluate with ranking metrics (NDCG, MRR, MAP) on held-out queries
```

#### 1. Training data: labels and clicks

Classic learning-to-rank data sets provide feature vectors and relevance judgements per query–document pair; LETOR 4.0, for example, uses the Gov2 collection of about 25 million web pages with about 1,700 labelled queries in MQ2007 and 800 in MQ2008, along with standard features, data splits and evaluation tools (Qin & Liu, 2013). Expert judgements are expensive, so Joachims (2002) learned from clickthrough logs: users scan only the first results and click on the relatively most promising links, so a click is not an absolute relevance judgement, but a clicked link is probably preferred over higher-ranked links the user skipped, which yields pairwise preferences such as "link 3 ≻ link 2".

#### 2. Pointwise ranking

The simplest approach scores each document independently with a classifier or regressor and sorts by the score. The BERT re-ranker of Nogueira and Cho (2019) is pointwise: it feeds query and passage together into [[bert|BERT]], classifies the pair as relevant or not with a [[cross-entropy|cross-entropy]] loss and ranks passages by the probability; it took first place on the MS MARCO passage leaderboard with a 27% relative improvement in MRR@10 ([[cross-encoder|cross-encoder]], [[ms-marco|MS MARCO]]).

#### 3. Pairwise ranking

The Ranking SVM learns a linear scoring function from pairwise preferences in an SVM framework, which Joachims (2002) showed to be feasible for large sets of queries and features; adapted to one group of users from clicks, it outperformed Google in retrieval quality after a few hundred training examples ([[support-vector-machines|support vector machines]]). RankNet models the probability that document i should rank above j as a sigmoid of the score difference `σ(s_i − s_j)` and minimises the cross-entropy against the target preference with [[gradient-descent|stochastic gradient descent]]; it thus approximately minimises the number of pairwise errors (Burges, 2010). BPR applies the same pairwise idea to recommendation from implicit feedback ([[recommender-systems|recommender systems]]; Rendle et al., 2009).

#### 4. Optimising ranking metrics: LambdaRank and LambdaMART

Metrics such as NDCG emphasise the top results and are not smooth functions of the scores because they depend on sorting. Burges (2010) shows why counting pairwise errors is not enough: a change that reduces pairwise errors can still move relevant documents down from the top positions. LambdaRank therefore writes down the desired gradients ("λs") directly instead of deriving them from a cost: the RankNet gradient of each pair is multiplied by the change in NDCG that swapping the two documents would cause (Burges, 2010). LambdaMART uses these λ-gradients in MART, gradient-boosted regression trees ([[ensemble-methods|ensemble methods]], [[decision-trees|decision trees]]), and ensembles of LambdaMART rankers won Track 1 of the 2010 Yahoo! Learning to Rank Challenge (Burges, 2010).

#### Origin and variants

Learning from clickthrough data dates to Joachims (2002); RankNet, LambdaRank and LambdaMART were developed at Microsoft Research and summarised by Burges (2010); LETOR provides benchmark data (Qin & Liu, 2013); BERT-based re-ranking (Nogueira & Cho, 2019) brought pretrained language models to the task.

### When to use it

- Re-ranking the top candidates of a first-stage retriever in search and [[retrieval-augmented-generation|RAG]] ([[rag-retrieval|RAG retrieval]]; Nogueira & Cho, 2019).
- Combining many relevance signals, such as [[bm25|BM25]], freshness and click features, into one ranking (Burges, 2010).
- Personalised ranking in recommendation and advertising (Rendle et al., 2009).

### Strengths and limitations

**Strengths**
- Learns how to weigh many signals instead of hand-tuning a formula (Burges, 2010).
- Pairwise preferences can be obtained cheaply from clicks (Joachims, 2002).
- Metric-aware methods focus learning on the positions users actually see (Burges, 2010).

**Limitations**
- Clicks only reflect the results users actually looked at and give relative, potentially noisy judgements (Joachims, 2002).
- Needs a candidate set from a first-stage retriever; it cannot rank documents that were not retrieved.
- Cross-encoder re-rankers score every query–document pair and are too slow for full collections ([[cross-encoder|cross-encoder]]).

### Comparison

| Approach | Training signal | Example | Note |
|---|---|---|---|
| Pointwise | relevance label per document | BERT re-ranker | simple, ignores relative order |
| Pairwise | preference between two documents | Ranking SVM, RankNet, BPR | learns from clicks |
| Metric-aware | pair gradients weighted by ΔNDCG | LambdaRank, LambdaMART | targets top positions |
| Unsupervised fusion | ranks of several systems | [[reciprocal-rank-fusion\|RRF]] | no training data |

Sources: Burges (2010), Joachims (2002), Nogueira & Cho (2019), Rendle et al. (2009).

### In practice

Learning-to-rank models are evaluated on held-out queries with ranking metrics such as NDCG, MRR and MAP ([[rag-retrieval-evaluation|retrieval evaluation]]); Burges (2010) notes that RankNet can already work well for such measures when the measure is used as a stopping criterion on a validation set. Pretrained re-rankers need relatively little task data: a BERT model trained on 100,000 question–passage pairs, less than 0.3% of the MS MARCO training data, already performed well (Nogueira & Cho, 2019).

### Key takeaway

Learning to rank learns a scoring function for ordering candidates from labels, pairwise preferences or metric-weighted gradients; LambdaMART and cross-encoder re-rankers are its best-known forms.

### Sources

- Burges, C. J. C. (2010). *From RankNet to LambdaRank to LambdaMART: An Overview.* Microsoft Research Technical Report MSR-TR-2010-82. [microsoft.com](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/MSR-TR-2010-82.pdf)
- Joachims, T. (2002). *Optimizing Search Engines using Clickthrough Data.* KDD 2002. [cs.cornell.edu](https://www.cs.cornell.edu/people/tj/publications/joachims_02c.pdf)
- Nogueira, R. & Cho, K. (2019). *Passage Re-ranking with BERT.* [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)
- Qin, T. & Liu, T.-Y. (2013). *Introducing LETOR 4.0 Datasets.* [arXiv:1306.2597](https://arxiv.org/abs/1306.2597)
- Rendle, S., Freudenthaler, C., Gantner, Z. & Schmidt-Thieme, L. (2009). *BPR: Bayesian Personalized Ranking from Implicit Feedback.* UAI 2009. [arXiv:1205.2618](https://arxiv.org/abs/1205.2618)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Learning to Rank trainiert ein Modell darauf, eine Liste von Kandidaten, etwa Dokumente zu einer Anfrage oder Elemente für eine Person, so zu ordnen, dass die relevantesten zuerst stehen (Burges, 2010). Statt ein absolutes Label vorherzusagen, lernen viele Verfahren aus Paaren, Dokument A soll über Dokument B stehen, die aus Relevanzurteilen oder aus Klicks stammen können (Joachims, 2002), und manche optimieren Ranking-Metriken wie NDCG, die die oberen Positionen am stärksten gewichten (Burges, 2010). Ensembles aus LambdaMART, einem Ranker aus Boosted Trees, gewannen 2010 die Yahoo! Learning to Rank Challenge (Burges, 2010), und heute ordnen nachtrainierte Transformer die Kandidaten eines Retrievers der ersten Stufe neu (Nogueira & Cho, 2019).

### Funktionsweise

```text
Anfrage q + Kandidatendokumente d_1 … d_n (aus einem Retriever der ersten Stufe wie BM25 oder Dense Retrieval)
   ▼  Merkmale pro (q, d): BM25-Score, Feldtreffer, Link- und Klicksignale …  oder das rohe Textpaar
Modell s(q, d) ──► Score pro Dokument ──► sortieren
   ▼  Trainingssignal
   punktweise: Relevanzlabel pro Dokument (z. B. relevant / nicht relevant)
   paarweise:  Präferenzen d_i ≻ d_j aus Urteilen oder Klicks         (RankSVM, RankNet, BPR)
   metrikbewusst: Paar-Gradienten mit der Änderung von NDCG gewichten  (LambdaRank, LambdaMART)
   ▼
Bewertung mit Ranking-Metriken (NDCG, MRR, MAP) auf zurückgehaltenen Anfragen
```

#### 1. Trainingsdaten: Labels und Klicks

Klassische Datensätze für Learning to Rank liefern Merkmalsvektoren und Relevanzurteile pro Paar aus Anfrage und Dokument; LETOR 4.0 etwa nutzt die Gov2-Sammlung mit rund 25 Millionen Webseiten mit etwa 1.700 gelabelten Anfragen in MQ2007 und 800 in MQ2008, dazu Standardmerkmale, Aufteilungen und Evaluationswerkzeuge (Qin & Liu, 2013). Urteile von Fachleuten sind teuer; Joachims (2002) lernte daher aus Klickprotokollen: Nutzende überfliegen nur die ersten Ergebnisse und klicken auf die relativ vielversprechendsten Links, ein Klick ist also kein absolutes Relevanzurteil, doch ein angeklickter Link wird wahrscheinlich höher platzierten, übersprungenen Links vorgezogen, was paarweise Präferenzen wie „Link 3 ≻ Link 2“ ergibt.

#### 2. Punktweises Ranking

Der einfachste Ansatz bewertet jedes Dokument einzeln mit einem Klassifikator oder Regressor und sortiert nach dem Score. Der BERT-Re-Ranker von Nogueira und Cho (2019) ist punktweise: Er gibt Anfrage und Passage gemeinsam in [[bert|BERT]], klassifiziert das Paar mit einem [[cross-entropy|Cross-Entropy]]-Verlust als relevant oder nicht und ordnet Passagen nach der Wahrscheinlichkeit; er erreichte den ersten Platz im MS-MARCO-Passagen-Leaderboard mit einer relativen Verbesserung von 27 % bei MRR@10 ([[cross-encoder|Cross-Encoder]], [[ms-marco|MS MARCO]]).

#### 3. Paarweises Ranking

Die Ranking-SVM lernt eine lineare Bewertungsfunktion aus paarweisen Präferenzen in einem SVM-Rahmen, was Joachims (2002) auch für große Mengen von Anfragen und Merkmalen als machbar zeigte; aus Klicks an eine Nutzergruppe angepasst, übertraf sie Google in der Retrieval-Qualität nach wenigen hundert Trainingsbeispielen ([[support-vector-machines|Support Vector Machines]]). RankNet modelliert die Wahrscheinlichkeit, dass Dokument i über j stehen soll, als Sigmoid der Score-Differenz `σ(s_i − s_j)` und minimiert die Cross-Entropy gegenüber der Zielpräferenz mit [[gradient-descent|stochastischem Gradientenabstieg]]; damit minimiert es näherungsweise die Zahl paarweiser Fehler (Burges, 2010). BPR überträgt dieselbe paarweise Idee auf Empfehlungen aus implizitem Feedback ([[recommender-systems|Recommender-Systeme]]; Rendle et al., 2009).

#### 4. Ranking-Metriken optimieren: LambdaRank und LambdaMART

Metriken wie NDCG betonen die obersten Ergebnisse und sind keine glatten Funktionen der Scores, weil sie vom Sortieren abhängen. Burges (2010) zeigt, warum das Zählen paarweiser Fehler nicht genügt: Eine Änderung, die paarweise Fehler verringert, kann relevante Dokumente dennoch von den obersten Positionen nach unten verschieben. LambdaRank schreibt die gewünschten Gradienten („λs“) daher direkt hin, statt sie aus einer Kostenfunktion abzuleiten: Der RankNet-Gradient jedes Paares wird mit der Änderung von NDCG multipliziert, die ein Vertauschen der beiden Dokumente bewirken würde (Burges, 2010). LambdaMART nutzt diese λ-Gradienten in MART, gradient-geboosteten Regressionsbäumen ([[ensemble-methods|Ensemble-Verfahren]], [[decision-trees|Entscheidungsbäume]]), und Ensembles aus LambdaMART-Rankern gewannen Track 1 der Yahoo! Learning to Rank Challenge 2010 (Burges, 2010).

#### Ursprung und Varianten

Das Lernen aus Klickdaten geht auf Joachims (2002) zurück; RankNet, LambdaRank und LambdaMART entstanden bei [[microsoft|Microsoft Research]] und wurden von Burges (2010) zusammengefasst; LETOR stellt Benchmark-Daten bereit (Qin & Liu, 2013); BERT-basiertes Re-Ranking (Nogueira & Cho, 2019) brachte vortrainierte Sprachmodelle in die Aufgabe.

### Wann einsetzen

- Die besten Kandidaten eines Retrievers der ersten Stufe in Suche und [[retrieval-augmented-generation|RAG]] neu ordnen ([[rag-retrieval|RAG-Retrieval]]; Nogueira & Cho, 2019).
- Viele Relevanzsignale wie [[bm25|BM25]], Aktualität und Klickmerkmale zu einem Ranking verbinden (Burges, 2010).
- Personalisiertes Ranking in Empfehlung und Werbung (Rendle et al., 2009).

### Stärken und Grenzen

**Stärken**
- Lernt, wie viele Signale zu gewichten sind, statt eine Formel von Hand abzustimmen (Burges, 2010).
- Paarweise Präferenzen lassen sich günstig aus Klicks gewinnen (Joachims, 2002).
- Metrikbewusste Verfahren richten das Lernen auf die Positionen, die Nutzende tatsächlich sehen (Burges, 2010).

**Grenzen**
- Klicks spiegeln nur die Ergebnisse, die Nutzende tatsächlich angesehen haben, und liefern relative, womöglich verrauschte Urteile (Joachims, 2002).
- Braucht eine Kandidatenmenge aus einem Retriever der ersten Stufe; nicht abgerufene Dokumente kann es nicht ordnen.
- Cross-Encoder-Re-Ranker bewerten jedes Paar aus Anfrage und Dokument und sind für ganze Sammlungen zu langsam ([[cross-encoder|Cross-Encoder]]).

### Vergleich

| Ansatz | Trainingssignal | Beispiel | Bemerkung |
|---|---|---|---|
| Punktweise | Relevanzlabel pro Dokument | BERT-Re-Ranker | einfach, ignoriert die relative Reihenfolge |
| Paarweise | Präferenz zwischen zwei Dokumenten | Ranking-SVM, RankNet, BPR | lernt aus Klicks |
| Metrikbewusst | mit ΔNDCG gewichtete Paar-Gradienten | LambdaRank, LambdaMART | zielt auf die obersten Positionen |
| Unüberwachte Fusion | Ränge mehrerer Systeme | [[reciprocal-rank-fusion\|RRF]] | keine Trainingsdaten |

Quellen: Burges (2010), Joachims (2002), Nogueira & Cho (2019), Rendle et al. (2009).

### In der Praxis

Learning-to-Rank-Modelle werden auf zurückgehaltenen Anfragen mit Ranking-Metriken wie NDCG, MRR und MAP bewertet ([[rag-retrieval-evaluation|Retrieval-Evaluation]]); Burges (2010) merkt an, dass RankNet für solche Maße schon gut funktionieren kann, wenn das Maß als Abbruchkriterium auf einer Validierungsmenge dient. Vortrainierte Re-Ranker brauchen relativ wenige Aufgabendaten: Ein BERT-Modell, trainiert auf 100.000 Frage-Passage-Paaren, weniger als 0,3 % der MS-MARCO-Trainingsdaten, schnitt bereits gut ab (Nogueira & Cho, 2019).

### Merksatz

Learning to Rank lernt eine Bewertungsfunktion zum Ordnen von Kandidaten aus Labels, paarweisen Präferenzen oder metrikgewichteten Gradienten; LambdaMART und Cross-Encoder-Re-Ranker sind seine bekanntesten Formen.

### Quellen

- Burges, C. J. C. (2010). *From RankNet to LambdaRank to LambdaMART: An Overview.* Microsoft Research Technical Report MSR-TR-2010-82. [microsoft.com](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/MSR-TR-2010-82.pdf)
- Joachims, T. (2002). *Optimizing Search Engines using Clickthrough Data.* KDD 2002. [cs.cornell.edu](https://www.cs.cornell.edu/people/tj/publications/joachims_02c.pdf)
- Nogueira, R. & Cho, K. (2019). *Passage Re-ranking with BERT.* [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)
- Qin, T. & Liu, T.-Y. (2013). *Introducing LETOR 4.0 Datasets.* [arXiv:1306.2597](https://arxiv.org/abs/1306.2597)
- Rendle, S., Freudenthaler, C., Gantner, Z. & Schmidt-Thieme, L. (2009). *BPR: Bayesian Personalized Ranking from Implicit Feedback.* UAI 2009. [arXiv:1205.2618](https://arxiv.org/abs/1205.2618)
