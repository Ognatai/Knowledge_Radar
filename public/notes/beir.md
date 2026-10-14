---
title_en: BEIR (Benchmarking IR)
title_de: BEIR (Benchmarking IR)
entity_type: Dataset
aliases:
- BEIR
- BEIR benchmark
sources:
- https://arxiv.org/abs/2104.08663
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

BEIR is a benchmark for zero-shot evaluation of retrieval models: it bundles 18 public datasets from nine retrieval tasks and many domains, and evaluates models that were trained elsewhere, mostly on [[ms-marco|MS MARCO]], without any further training on the target data (Thakur et al., 2021). Its main finding was that in-domain performance does not predict generalisation: [[bm25|BM25]] remained a strong baseline, rerankers and late-interaction models such as [[colbert|ColBERT]] generalised best but at high cost, and several dense retrievers fell below BM25 on many datasets (Thakur et al., 2021). The standard metric is nDCG@10.

### How it works

```text
18 datasets, 9 tasks (fact checking, citation prediction, duplicate questions, argument retrieval,
news, question answering, tweets, bio-medical IR, entity retrieval)
 ▼ unified format: corpus, queries, relevance judgements (binary or graded)
 ▼ model trained on another dataset (mostly MS MARCO) → retrieve top documents per query
 ▼ nDCG@10 per dataset (+ Recall@100) → average and comparison with BM25
```

#### 1. Datasets and tasks

BEIR covers fact checking (FEVER, Climate-FEVER, SciFact), citation prediction (SCIDOCS), duplicate-question retrieval (CQADupStack, Quora), argument retrieval (ArguAna, Touché-2020), news retrieval (TREC-NEWS, Robust04), question answering (NQ, HotpotQA, FiQA-2018), tweet retrieval (Signal-1M), bio-medical retrieval (TREC-COVID, NFCorpus, BioASQ) and entity retrieval (DBPedia) (Thakur et al., 2021). Corpora range from 3,600 to 15 million documents, average query lengths from 3 to 192 words and document lengths from 11 to 635 words. The datasets are converted into one format and released with an open-source package (Thakur et al., 2021).

#### 2. Metric

[[classification-metrics|Precision]] and recall are not rank-aware, and MRR and MAP cannot handle graded relevance, so BEIR uses nDCG@10, which suits both binary and graded judgements (Thakur et al., 2021). Metrics are explained in [[rag-retrieval-evaluation|RAG retrieval evaluation]] and [[information-retrieval|information retrieval]].

#### 3. Evaluated systems

Ten systems from five families were tested: lexical (BM25), sparse (DeepCT, SPARTA, docT5query), dense ([[dense-passage-retrieval|DPR]], ANCE, TAS-B, GenQ), late interaction (ColBERT) and re-ranking (BM25 plus a [[cross-encoder|cross-encoder]]) (Thakur et al., 2021). Except for DPR, which was trained on Natural Questions and other QA data, the neural models were trained on MS MARCO.

#### 4. Findings

- **In-domain is not out-of-domain:** BM25 trailed neural models by 7 to 18 points on MS MARCO itself but was a strong baseline across BEIR (Thakur et al., 2021).
- **Re-ranking generalises best:** BM25 plus cross-encoder was the best system overall, about 11% above BM25 on average and better on 16 of 18 datasets; ColBERT was 2.5% above BM25 on average (Thakur et al., 2021).
- **Dense retrievers struggle under domain shift:** dense models were strong on some datasets but far below BM25 on others, for example under domain shift (BioASQ) or task shift (Touché-2020); DPR was on average 47.7% below BM25, TAS-B was the best dense model at 2.8% below (Thakur et al., 2021).
- **Document expansion helps sparse models:** docT5query, which adds generated keywords to documents, beat BM25 on 11 of 18 datasets, while learned term weighting (DeepCT, SPARTA) failed to generalise (Thakur et al., 2021).

#### 5. Lexical bias in the judgements

Many BEIR datasets were annotated using lexical retrieval systems, so relevant documents found only by neural models may be unjudged and count as non-relevant (Thakur et al., 2021). Re-annotating the missing judgements on TREC-COVID for the tested systems significantly improved the scores of non-lexical approaches; the authors call for less biased datasets. This pooling problem is discussed in [[rag-retrieval-evaluation|RAG retrieval evaluation]].

#### Origin and variants

Nandan Thakur, Nils Reimers and colleagues at the UKP Lab of TU Darmstadt published BEIR in 2021 (Thakur et al., 2021). The benchmark and an integration of many retrieval systems are available as an open-source package (Thakur et al., 2021); evaluating embedding models is discussed in [[embeddings|embeddings]].

### When to use it

- Choosing a retriever or embedding model for a domain without labelled training data, by looking at results on similar BEIR tasks (Thakur et al., 2021).
- Testing whether a new retrieval method generalises beyond its training data (Thakur et al., 2021).
- As a template for building an in-house benchmark in the same format.

### Strengths and limitations

**Strengths**
- Many tasks, domains and corpus sizes in one format (Thakur et al., 2021).
- Zero-shot setting reflects the common situation without in-domain training data (Thakur et al., 2021).
- Open-source tooling with integrations for many retrieval systems (Thakur et al., 2021).

**Limitations**
- Lexical bias in relevance judgements disadvantages neural retrievers (Thakur et al., 2021).
- Different datasets favour different model families; no single approach is best on all of them (Thakur et al., 2021).
- nDCG@10 alone does not capture recall at larger depths, which matters for [[retrieval-augmented-generation|RAG]] pipelines with rerankers (Thakur et al., 2021 report Recall@100 separately).

### Comparison

| Benchmark | Setting | Focus |
|---|---|---|
| [[ms-marco\|MS MARCO]] | in-domain, large training set | web passage ranking |
| BEIR | zero-shot, 18 datasets | generalisation across tasks and domains |
| Own evaluation set | in-domain, small | the actual application |

Source: Thakur et al. (2021).

### In practice

BEIR results guide the shortlist, but the final choice should be tested on queries and documents from the target application ([[rag-retrieval-evaluation|RAG retrieval evaluation]]). Combining BM25 with a dense retriever and reranking the union hedges against the weaknesses BEIR exposes ([[reciprocal-rank-fusion|reciprocal rank fusion]], [[rag-retrieval|RAG retrieval]]).

### Key takeaway

BEIR tests retrievers zero-shot on 18 heterogeneous datasets and showed that BM25 is hard to beat outside the training domain, that cross-encoder reranking generalises best, and that relevance judgements built with lexical systems can understate neural retrievers.

### Sources

- Thakur, N., Reimers, N., Rücklé, A., Srivastava, A. & Gurevych, I. (2021). *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* NeurIPS 2021 Datasets and Benchmarks Track. [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

BEIR ist ein Benchmark für die Zero-Shot-Evaluation von Retrieval-Modellen: Er bündelt 18 öffentliche Datensätze aus neun Retrieval-Aufgaben und vielen Domänen und bewertet Modelle, die anderswo trainiert wurden, meist auf [[ms-marco|MS MARCO]], ohne weiteres Training auf den Zieldaten (Thakur et al., 2021). Sein wichtigster Befund war, dass die Leistung in der eigenen Domäne die Verallgemeinerung nicht vorhersagt: [[bm25|BM25]] blieb eine starke Baseline, Reranker und Late-Interaction-Modelle wie [[colbert|ColBERT]] verallgemeinerten am besten, aber zu hohen Kosten, und mehrere Dense Retriever lagen auf vielen Datensätzen unter BM25 (Thakur et al., 2021). Die Standardmetrik ist nDCG@10.

### Funktionsweise

```text
18 Datensätze, 9 Aufgaben (Faktenprüfung, Zitationsvorhersage, Duplikatfragen, Argument-Retrieval,
Nachrichten, Fragebeantwortung, Tweets, biomedizinisches IR, Entitäts-Retrieval)
 ▼ einheitliches Format: Korpus, Anfragen, Relevanzurteile (binär oder abgestuft)
 ▼ auf einem anderen Datensatz trainiertes Modell (meist MS MARCO) → Top-Dokumente je Anfrage abrufen
 ▼ nDCG@10 je Datensatz (+ Recall@100) → Mittelwert und Vergleich mit BM25
```

#### 1. Datensätze und Aufgaben

BEIR umfasst Faktenprüfung (FEVER, Climate-FEVER, SciFact), Zitationsvorhersage (SCIDOCS), Retrieval von Duplikatfragen (CQADupStack, Quora), Argument-Retrieval (ArguAna, Touché-2020), Nachrichten-Retrieval (TREC-NEWS, Robust04), Fragebeantwortung (NQ, HotpotQA, FiQA-2018), Tweet-Retrieval (Signal-1M), biomedizinisches Retrieval (TREC-COVID, NFCorpus, BioASQ) und Entitäts-Retrieval (DBPedia) (Thakur et al., 2021). Die Korpora reichen von 3.600 bis 15 Millionen Dokumenten, die mittlere Anfragelänge von 3 bis 192 Wörtern und die Dokumentlänge von 11 bis 635 Wörtern. Die Datensätze sind in ein gemeinsames Format überführt und mit einem Open-Source-Paket veröffentlicht (Thakur et al., 2021).

#### 2. Metrik

[[classification-metrics|Precision]] und Recall berücksichtigen keine Rangfolge, und MRR sowie MAP können keine abgestufte Relevanz abbilden, daher nutzt BEIR nDCG@10, das für binäre und abgestufte Urteile passt (Thakur et al., 2021). Die Metriken erklären [[rag-retrieval-evaluation|RAG: Evaluation des Retrievals]] und [[information-retrieval|Information Retrieval]].

#### 3. Bewertete Systeme

Getestet wurden zehn Systeme aus fünf Familien: lexikalisch (BM25), spärlich (DeepCT, SPARTA, docT5query), dicht ([[dense-passage-retrieval|DPR]], ANCE, TAS-B, GenQ), Late Interaction (ColBERT) und Re-Ranking (BM25 plus [[cross-encoder|Cross-Encoder]]) (Thakur et al., 2021). Außer DPR, das auf Natural Questions und weiteren QA-Daten trainiert war, wurden die neuronalen Modelle auf MS MARCO trainiert.

#### 4. Befunde

- **Innerhalb der Domäne ist nicht außerhalb:** BM25 lag auf MS MARCO selbst 7 bis 18 Punkte hinter neuronalen Modellen, war über BEIR hinweg aber eine starke Baseline (Thakur et al., 2021).
- **Re-Ranking verallgemeinert am besten:** BM25 plus Cross-Encoder war insgesamt das beste System, im Mittel etwa 11 % über BM25 und auf 16 von 18 Datensätzen besser; ColBERT lag im Mittel 2,5 % über BM25 (Thakur et al., 2021).
- **Dense Retriever haben Mühe mit Domänenwechseln:** Dichte Modelle waren auf manchen Datensätzen stark, auf anderen weit unter BM25, etwa bei Domänenwechsel (BioASQ) oder Aufgabenwechsel (Touché-2020); DPR lag im Mittel 47,7 % unter BM25, TAS-B war mit 2,8 % darunter das beste dichte Modell (Thakur et al., 2021).
- **Dokumenterweiterung hilft spärlichen Modellen:** docT5query, das Dokumenten erzeugte Schlüsselwörter hinzufügt, schlug BM25 auf 11 von 18 Datensätzen, während gelernte Termgewichtung (DeepCT, SPARTA) nicht verallgemeinerte (Thakur et al., 2021).

#### 5. Lexikalische Verzerrung der Relevanzurteile

Viele BEIR-Datensätze wurden mithilfe lexikalischer Retrieval-Systeme annotiert, sodass relevante Dokumente, die nur neuronale Modelle finden, womöglich nicht beurteilt sind und als nicht relevant zählen (Thakur et al., 2021). Das Nachannotieren der fehlenden Urteile auf TREC-COVID für die getesteten Systeme verbesserte die Werte nicht-lexikalischer Ansätze deutlich; die Autorinnen und Autoren fordern weniger verzerrte Datensätze. Dieses Pooling-Problem behandelt [[rag-retrieval-evaluation|RAG: Evaluation des Retrievals]].

#### Herkunft und Varianten

Nandan Thakur, Nils Reimers und Kolleginnen und Kollegen am UKP Lab der TU Darmstadt veröffentlichten BEIR 2021 (Thakur et al., 2021). Benchmark und Anbindungen vieler Retrieval-Systeme sind als Open-Source-Paket verfügbar (Thakur et al., 2021); die Evaluation von Embedding-Modellen behandelt [[embeddings|Embeddings]].

### Wann einsetzen

- Einen Retriever oder ein Embedding-Modell für eine Domäne ohne gelabelte Trainingsdaten auswählen, anhand der Ergebnisse auf ähnlichen BEIR-Aufgaben (Thakur et al., 2021).
- Prüfen, ob ein neues Retrieval-Verfahren über seine Trainingsdaten hinaus verallgemeinert (Thakur et al., 2021).
- Als Vorlage für einen eigenen Benchmark im selben Format.

### Stärken und Grenzen

**Stärken**
- Viele Aufgaben, Domänen und Korpusgrößen in einem Format (Thakur et al., 2021).
- Die Zero-Shot-Einstellung spiegelt die häufige Lage ohne Trainingsdaten aus der eigenen Domäne (Thakur et al., 2021).
- Open-Source-Werkzeuge mit Anbindungen an viele Retrieval-Systeme (Thakur et al., 2021).

**Grenzen**
- Lexikalische Verzerrung der Relevanzurteile benachteiligt neuronale Retriever (Thakur et al., 2021).
- Verschiedene Datensätze begünstigen verschiedene Modellfamilien; kein einzelner Ansatz ist auf allen am besten (Thakur et al., 2021).
- nDCG@10 allein erfasst keinen Recall in größerer Tiefe, der für RAG-Pipelines mit Rerankern zählt (Thakur et al., 2021 berichten Recall@100 getrennt).

### Vergleich

| Benchmark | Einstellung | Schwerpunkt |
|---|---|---|
| [[ms-marco\|MS MARCO]] | in der Domäne, großer Trainingsdatensatz | Ranking von Web-Passagen |
| BEIR | Zero-Shot, 18 Datensätze | Verallgemeinerung über Aufgaben und Domänen |
| Eigenes Evaluationsset | in der Domäne, klein | die tatsächliche Anwendung |

Quelle: Thakur et al. (2021).

### In der Praxis

BEIR-Ergebnisse helfen bei der Vorauswahl, die endgültige Wahl sollte aber mit Anfragen und Dokumenten aus der Zielanwendung getestet werden ([[rag-retrieval-evaluation|RAG: Evaluation des Retrievals]]). BM25 mit einem Dense Retriever zu kombinieren und die Vereinigung neu zu ordnen, sichert gegen die Schwächen ab, die BEIR zeigt ([[reciprocal-rank-fusion|Reciprocal Rank Fusion]], [[rag-retrieval|RAG: Retrieval]]).

### Merksatz

BEIR testet Retriever ohne Nachtraining auf 18 heterogenen Datensätzen und zeigte, dass BM25 außerhalb der Trainingsdomäne schwer zu schlagen ist, dass Re-Ranking mit Cross-Encodern am besten verallgemeinert und dass mit lexikalischen Systemen erstellte Relevanzurteile neuronale Retriever unterschätzen können.

### Quellen

- Thakur, N., Reimers, N., Rücklé, A., Srivastava, A. & Gurevych, I. (2021). *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* NeurIPS 2021 Datasets and Benchmarks Track. [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)
