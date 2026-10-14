---
title_en: MS MARCO
title_de: MS MARCO
entity_type: Dataset
aliases:
- MS MARCO
- MSMARCO
- Microsoft MAchine Reading COmprehension
sources:
- https://arxiv.org/abs/1611.09268
- https://arxiv.org/abs/2104.08663
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

MS MARCO (Microsoft MAchine Reading COmprehension) is a large dataset of real Bing search questions with passages from web documents and human-written answers: 1,010,916 anonymised questions, 8,841,823 passages from 3,563,535 web documents and 182,669 rewritten well-formed answers (Bajaj et al., 2016). Besides answer generation tasks, it defines a passage ranking task, re-ranking 1,000 BM25 candidates per question, which became a main training set for neural retrieval: most models evaluated zero-shot in [[beir|BEIR]] were trained on it (Bajaj et al., 2016; Thakur et al., 2021). Its relevance labels are incomplete: only passages the editors used are marked relevant.

### How it works

```text
Bing query logs → filter question-like queries (classifier) → anonymise
 ▼
Bing retrieves documents → passages extracted (≈ 10 per question)
 ▼
human editors: mark passages used (is_selected), write an answer or "No Answer Present"
 ▼ some answers rewritten as well-formed answers
tasks: (i) answerability + answer generation · (ii) well-formed answers · (iii) passage (re-)ranking
```

#### 1. Collection

Questions were sampled from Bing's search logs, non-question queries were filtered out by a classifier, and the remaining queries were anonymised (Bajaj et al., 2016). For each question, Bing retrieved documents from its web index, about 10 passages were extracted, and human editors marked the passages they used (`is_selected`) and composed a natural-language answer strictly from them; questions without an answer in the passages are labelled as unanswerable. Because the questions come from real users, they are often ambiguous or contain typos, which makes them more representative of real information needs than crowd-written questions (Bajaj et al., 2016).

#### 2. Components

The release contains six components: the questions, about 10 candidate passages per question, the editors' answers (zero, one or more per question), well-formed answers rewritten by a second editor when the first answer was ungrammatical, copied too closely from a passage or not understandable without context, the source documents with URL, title and body text, and an automatic question type such as numeric, entity, location, person or description (Bajaj et al., 2016). About 300,000 documents could no longer be retrieved from Bing's index.

#### 3. Tasks

Three tasks were proposed (Bajaj et al., 2016): a novice task (decide whether the passages answer the question and, if so, generate the answer), an intermediate task (generate a well-formed answer that makes sense on its own), and a passage re-ranking task (rank 1,000 BM25-retrieved passages by how likely they contain relevant information). Answer generation was evaluated with ROUGE-L and [[bleu|BLEU]] ([[text-similarity-metrics|text similarity metrics]]); ranking results are reported with measures such as MRR@10, as in [[colbert|ColBERT]].

#### 4. The passage ranking collection

For retrieval research, the union of all passages forms one collection, with relevant question-passage pairs taken from the `is_selected` annotations (Bajaj et al., 2016). Because editors did not judge every retrieved passage, these labels are incomplete: there are likely passages in the collection that answer a question but are not marked. The collection was also used for the TREC 2019 Deep Learning track. Neural models such as [[colbert|ColBERT]] and many dense retrievers report MRR@10 on this collection and are trained on its training pairs (Bajaj et al., 2016; Thakur et al., 2021).

#### 5. In-domain versus zero-shot

On MS MARCO itself, neural retrievers trained on it beat [[bm25|BM25]] by 7 to 18 nDCG@10 points, but on the 18 other datasets of BEIR several of them fell below BM25 (Thakur et al., 2021). Strong MS MARCO results therefore do not guarantee good retrieval in another domain.

#### Origin and variants

[[microsoft|Microsoft]] AI & Research presented MS MARCO at NIPS 2016; version 1.1 followed in January 2017, version 2.1 in 2018, and additional passage-ranking files in October 2018 (Bajaj et al., 2016). Prior retrieval work typically trains on MS MARCO, with 533,000 training examples, or on Natural Questions, with 133,000, the dataset used for [[dense-passage-retrieval|DPR]] (Thakur et al., 2021).

### When to use it

- Training dense retrievers, cross-encoders or late-interaction models that need many labelled query-passage pairs (Thakur et al., 2021).
- Comparing ranking models on a common, large benchmark (Bajaj et al., 2016).
- Studying question answering over noisy, real web queries (Bajaj et al., 2016).

### Strengths and limitations

**Strengths**
- Very large, with real user questions rather than questions written from a given text (Bajaj et al., 2016).
- Human-written answers and passage relevance marks (Bajaj et al., 2016).
- Widely used, so results are comparable across papers (Thakur et al., 2021).

**Limitations**
- Relevance labels are incomplete, so unmarked relevant passages count as wrong (Bajaj et al., 2016).
- Web domain only; models trained on it can generalise poorly elsewhere (Thakur et al., 2021).
- Source documents may have changed since extraction, and some are missing (Bajaj et al., 2016).

### Comparison

| Dataset | Questions | Corpus | Main use |
|---|---|---|---|
| MS MARCO | about 1 million real Bing questions | 8.8 million web passages | training and in-domain ranking |
| Natural Questions | real Google questions | Wikipedia | open-domain QA ([[dense-passage-retrieval\|DPR]]) |
| [[beir\|BEIR]] | 18 datasets | 3.6k to 15 million documents | zero-shot evaluation |

Sources: Bajaj et al. (2016); Thakur et al. (2021).

### In practice

Pre-trained retrievers and rerankers are often trained on MS MARCO; before using one, its results should be checked on the target domain, because MS MARCO performance overstates generalisation (Thakur et al., 2021). Incomplete labels also mean that a model may be penalised for retrieving relevant but unjudged passages, a problem discussed in [[rag-retrieval-evaluation|RAG retrieval evaluation]].

### Key takeaway

MS MARCO provides about a million real Bing questions with web passages and human answers; its passage ranking collection trained much of modern neural retrieval, but its incomplete labels and single domain mean that in-domain scores overstate generalisation.

### Sources

- Bajaj, P., Campos, D., Craswell, N., Deng, L., Gao, J., Liu, X., Majumder, R., McNamara, A., Mitra, B., Nguyen, T., Rosenberg, M., Song, X., Stoica, A., Tiwary, S. & Wang, T. (2016). *MS MARCO: A Human Generated MAchine Reading COmprehension Dataset.* Presented at NIPS 2016; revised 2018. [arXiv:1611.09268](https://arxiv.org/abs/1611.09268)
- Thakur, N., Reimers, N., Rücklé, A., Srivastava, A. & Gurevych, I. (2021). *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* NeurIPS 2021 Datasets and Benchmarks Track. [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

MS MARCO (Microsoft MAchine Reading COmprehension) ist ein großer Datensatz echter Bing-Suchfragen mit Passagen aus Webdokumenten und von Menschen geschriebenen Antworten: 1.010.916 anonymisierte Fragen, 8.841.823 Passagen aus 3.563.535 Webdokumenten und 182.669 überarbeitete, wohlgeformte Antworten (Bajaj et al., 2016). Neben Aufgaben zur Antwortgenerierung definiert er eine Aufgabe zum Ranking von Passagen, das Neuordnen von 1.000 BM25-Kandidaten je Frage; sie wurde zu einem zentralen Trainingsdatensatz für neuronales Retrieval: Die meisten Modelle, die in [[beir|BEIR]] ohne Nachtraining bewertet werden, sind darauf trainiert (Bajaj et al., 2016; Thakur et al., 2021). Seine Relevanzlabels sind unvollständig: Nur Passagen, die die Redakteurinnen und Redakteure verwendet haben, sind als relevant markiert.

### Funktionsweise

```text
Bing-Anfrageprotokolle → frageartige Anfragen filtern (Klassifikator) → anonymisieren
 ▼
Bing ruft Dokumente ab → Passagen extrahiert (≈ 10 je Frage)
 ▼
Redaktion: genutzte Passagen markieren (is_selected), Antwort schreiben oder „No Answer Present“
 ▼ einige Antworten als wohlgeformte Antworten umgeschrieben
Aufgaben: (i) Beantwortbarkeit + Antwortgenerierung · (ii) wohlgeformte Antworten · (iii) Passagen-(Re-)Ranking
```

#### 1. Erhebung

Fragen wurden aus den Suchprotokollen von Bing gezogen, Anfragen, die keine Fragen sind, per Klassifikator herausgefiltert und die übrigen anonymisiert (Bajaj et al., 2016). Für jede Frage rief Bing Dokumente aus seinem Webindex ab, etwa 10 Passagen wurden extrahiert, und eine Redaktion markierte die genutzten Passagen (`is_selected`) und verfasste eine Antwort in natürlicher Sprache ausschließlich auf deren Grundlage; Fragen ohne Antwort in den Passagen werden als nicht beantwortbar gekennzeichnet. Weil die Fragen von echten Nutzenden stammen, sind sie oft mehrdeutig oder enthalten Tippfehler, was sie repräsentativer für echte Informationsbedürfnisse macht als von Crowdworkern geschriebene Fragen (Bajaj et al., 2016).

#### 2. Bestandteile

Die Veröffentlichung umfasst sechs Bestandteile: die Fragen, etwa 10 Kandidatenpassagen je Frage, die Antworten der Redaktion (keine, eine oder mehrere je Frage), wohlgeformte Antworten, die eine zweite Person umschrieb, wenn die erste Antwort grammatisch fehlerhaft, zu nah an einer Passage oder ohne Kontext unverständlich war, die Quelldokumente mit URL, Titel und Text sowie einen automatisch bestimmten Fragetyp wie Zahl, Entität, Ort, Person oder Beschreibung (Bajaj et al., 2016). Etwa 300.000 Dokumente waren im Bing-Index nicht mehr abrufbar.

#### 3. Aufgaben

Vorgeschlagen wurden drei Aufgaben (Bajaj et al., 2016): eine Einsteigeraufgabe (entscheiden, ob die Passagen die Frage beantworten, und gegebenenfalls die Antwort erzeugen), eine mittlere Aufgabe (eine wohlgeformte Antwort erzeugen, die für sich verständlich ist) und eine Aufgabe zum Neuordnen von Passagen (1.000 per BM25 gefundene Passagen danach ordnen, wie wahrscheinlich sie relevante Informationen enthalten). Die Antwortgenerierung wurde mit ROUGE-L und [[bleu|BLEU]] bewertet ([[text-similarity-metrics|Metriken für Textähnlichkeit]]); Ranking-Ergebnisse werden mit Maßen wie MRR@10 berichtet, etwa bei [[colbert|ColBERT]].

#### 4. Die Sammlung für das Passagen-Ranking

Für die Retrieval-Forschung bildet die Vereinigung aller Passagen eine Sammlung, mit relevanten Frage-Passage-Paaren aus den `is_selected`-Markierungen (Bajaj et al., 2016). Weil die Redaktion nicht jede abgerufene Passage beurteilt hat, sind diese Labels unvollständig: In der Sammlung gibt es vermutlich Passagen, die eine Frage beantworten, aber nicht markiert sind. Die Sammlung diente auch dem Deep Learning Track von TREC 2019. Neuronale Modelle wie [[colbert|ColBERT]] und viele Dense Retriever berichten MRR@10 auf dieser Sammlung und werden auf ihren Trainingspaaren trainiert (Bajaj et al., 2016; Thakur et al., 2021).

#### 5. In der Domäne versus Zero-Shot

Auf MS MARCO selbst schlugen darauf trainierte neuronale Retriever [[bm25|BM25]] um 7 bis 18 Punkte nDCG@10, auf den 18 anderen Datensätzen von BEIR lagen aber mehrere von ihnen unter BM25 (Thakur et al., 2021). Starke Ergebnisse auf MS MARCO garantieren daher kein gutes Retrieval in einer anderen Domäne.

#### Herkunft und Varianten

[[microsoft|Microsoft]] AI & Research stellte MS MARCO auf der NIPS 2016 vor; Version 1.1 folgte im Januar 2017, Version 2.1 im Jahr 2018 und zusätzliche Dateien für das Passagen-Ranking im Oktober 2018 (Bajaj et al., 2016). Frühere Retrieval-Arbeiten trainieren typischerweise auf MS MARCO mit 533.000 Trainingsbeispielen oder auf Natural Questions mit 133.000, dem Datensatz, den [[dense-passage-retrieval|DPR]] nutzte (Thakur et al., 2021).

### Wann einsetzen

- Training von Dense Retrievern, Cross-Encodern oder Late-Interaction-Modellen, die viele gelabelte Paare aus Anfrage und Passage brauchen (Thakur et al., 2021).
- Vergleich von Ranking-Modellen auf einem gemeinsamen, großen Benchmark (Bajaj et al., 2016).
- Untersuchung der Fragebeantwortung über verrauschte, echte Webanfragen (Bajaj et al., 2016).

### Stärken und Grenzen

**Stärken**
- Sehr groß, mit echten Fragen von Nutzenden statt Fragen, die zu einem vorgegebenen Text geschrieben wurden (Bajaj et al., 2016).
- Von Menschen geschriebene Antworten und Relevanzmarkierungen für Passagen (Bajaj et al., 2016).
- Weit verbreitet, sodass Ergebnisse zwischen Arbeiten vergleichbar sind (Thakur et al., 2021).

**Grenzen**
- Die Relevanzlabels sind unvollständig, sodass nicht markierte relevante Passagen als falsch zählen (Bajaj et al., 2016).
- Nur Webdomäne; darauf trainierte Modelle verallgemeinern anderswo womöglich schlecht (Thakur et al., 2021).
- Quelldokumente können sich seit der Extraktion geändert haben, und manche fehlen (Bajaj et al., 2016).

### Vergleich

| Datensatz | Fragen | Korpus | Hauptzweck |
|---|---|---|---|
| MS MARCO | etwa 1 Million echte Bing-Fragen | 8,8 Millionen Webpassagen | Training und Ranking in der Domäne |
| Natural Questions | echte Google-Fragen | Wikipedia | Open-Domain-QA ([[dense-passage-retrieval\|DPR]]) |
| [[beir\|BEIR]] | 18 Datensätze | 3.600 bis 15 Millionen Dokumente | Zero-Shot-Evaluation |

Quellen: Bajaj et al. (2016); Thakur et al. (2021).

### In der Praxis

Vortrainierte Retriever und Reranker sind oft auf MS MARCO trainiert; vor dem Einsatz sollten ihre Ergebnisse in der Zieldomäne geprüft werden, weil die Leistung auf MS MARCO die Verallgemeinerung überschätzt (Thakur et al., 2021). Unvollständige Labels bedeuten zudem, dass ein Modell für relevante, aber nicht beurteilte Passagen bestraft werden kann, ein Problem, das [[rag-retrieval-evaluation|RAG: Evaluation des Retrievals]] behandelt.

### Merksatz

MS MARCO liefert rund eine Million echte Bing-Fragen mit Webpassagen und menschlichen Antworten; seine Sammlung für das Passagen-Ranking trainierte einen Großteil des modernen neuronalen Retrievals, doch unvollständige Labels und eine einzige Domäne führen dazu, dass Werte in der Domäne die Verallgemeinerung überschätzen.

### Quellen

- Bajaj, P., Campos, D., Craswell, N., Deng, L., Gao, J., Liu, X., Majumder, R., McNamara, A., Mitra, B., Nguyen, T., Rosenberg, M., Song, X., Stoica, A., Tiwary, S. & Wang, T. (2016). *MS MARCO: A Human Generated MAchine Reading COmprehension Dataset.* Vorgestellt auf der NIPS 2016; überarbeitet 2018. [arXiv:1611.09268](https://arxiv.org/abs/1611.09268)
- Thakur, N., Reimers, N., Rücklé, A., Srivastava, A. & Gurevych, I. (2021). *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* NeurIPS 2021 Datasets and Benchmarks Track. [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)
