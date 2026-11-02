---
title_en: Natural Questions
title_de: Natural Questions
entity_type: Dataset
aliases:
- Natural Questions
- NQ
- Natural Questions corpus
- NQ-Open
sources:
- https://aclanthology.org/Q19-1026/
- https://web.stanford.edu/~jurafsky/slp3/11.pdf
- https://arxiv.org/abs/2004.04906
- https://arxiv.org/abs/2002.08910
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Natural Questions (NQ) is a [[question-answering|question answering]] benchmark built from real, anonymised queries to the Google search engine, each paired with a Wikipedia page from the top five search results (Kwiatkowski et al., 2019). Annotators mark a long answer (typically a paragraph), a short answer (one or more entities) or yes/no, or null if the page does not answer the question; the public release has 307,373 training examples and 5-way annotated development and test sets (Kwiatkowski et al., 2019). Its open-domain version, in which systems must find the answer in all of Wikipedia, became a standard test for retrievers and [[retrieval-augmented-generation|RAG]] (Karpukhin et al., 2020).

### How it works

```text
Google search queries (anonymised, aggregated)
   ▼  heuristic filters keep question-like queries of ≥ 8 words
   ▼  keep queries with a Wikipedia page among the top 5 results
(question, Wikipedia page)
   ▼  annotator: long answer (paragraph, table, list) │ short answer (entities) or yes/no │ NULL
training: 307,373 single-annotated  ·  dev: 7,830 and test: 7,842 with 5 annotations each
   ▼
evaluation: precision / recall / F1 for long and short answers against 5-way annotations
```

#### 1. Questions from real information needs

Unlike data sets whose questions were written by crowdworkers looking at a passage, NQ uses questions that people actually asked a search engine (Kwiatkowski et al., 2019). Simple heuristics keep queries that look like questions, for example those starting with "who" followed by a verb, while discarding most non-questions and retaining the majority of questions of eight words or more; longer queries were preferred because they are more complex (Kwiatkowski et al., 2019). Jurafsky and Martin (2026) classify NQ, like [[ms-marco|MS MARCO]], as a natural information-seeking data set, in contrast to probing data sets such as [[mmlu|MMLU]].

#### 2. Long and short answers

Given the question and an entire Wikipedia page, the annotator selects a long answer, an HTML bounding box such as a paragraph or table that contains the information needed, and within it a short answer: one or more entities, or a yes/no flag (Kwiatkowski et al., 2019). For example, "When are hops added to the brewing process?" has the short answer "the boiling process" and a paragraph from the Wikipedia page on brewing as long answer (Jurafsky & Martin, 2026). Annotators found a long answer for 49% of the examples and a short answer or yes/no for 36%; the remaining 51% without an answer are kept, because deciding whether to answer is part of the task (Kwiatkowski et al., 2019).

#### 3. Quality and human variability

Post-hoc checks found 90% precision for long and 84% for short answers (Kwiatkowski et al., 2019). 25-way annotation of 302 examples showed that for natural questions there is often genuine ambiguity about whether an answer is acceptable and frequently several acceptable answers; evaluation therefore uses five annotations per development and test example (Kwiatkowski et al., 2019).

#### 4. Evaluation and baselines

Systems are scored by precision, recall and F1 against the 5-way annotations (Kwiatkowski et al., 2019; [[classification-metrics|classification metrics]]). A "super-annotator" upper bound reached 87.2 F1 for long and 75.7 F1 for short answers, while the best baseline in the original paper reached 55.0 and 35.1 F1 on the test set, a large gap (Kwiatkowski et al., 2019).

#### 5. Open-domain and closed-book use

In the open-domain version, a model receives only the question and must retrieve evidence itself and produce a single normalised answer (Roberts et al., 2020). Dense Passage Retrieval was evaluated this way and outperformed [[bm25|BM25]] by a wide margin in top-5 accuracy, 65.2% against 42.9% ([[dense-passage-retrieval|dense passage retrieval]]; Karpukhin et al., 2020). Roberts et al. (2020) used the same questions closed-book, answering from T5's parameters alone ([[t5|T5]]). The same data set can thus be used open-book or closed-book (Jurafsky & Martin, 2026).

#### Origin and variants

NQ was created by Google Research and published in the Transactions of the Association for Computational Linguistics in 2019 (Kwiatkowski et al., 2019). Variants include the open-domain question set used by retrieval papers and the multi-answer reading comprehension setting of the original task (Roberts et al., 2020).

### When to use it

- Evaluating open-domain retrievers and RAG pipelines on real user questions ([[rag-retrieval-evaluation|retrieval evaluation]]).
- Training and testing reading comprehension over full Wikipedia pages, including the decision not to answer.
- Measuring closed-book knowledge of language models ([[llm-evaluation|LLM evaluation]]).

### Strengths and limitations

**Strengths**
- Questions reflect real information needs rather than passage-driven crowd questions (Kwiatkowski et al., 2019).
- Includes unanswerable examples and multiple annotations for robust evaluation (Kwiatkowski et al., 2019).
- Large training set and widely used, so results are comparable across papers.

**Limitations**
- English only and Wikipedia only; questions come from one search engine's users.
- Answers can be genuinely ambiguous, which caps achievable scores (Kwiatkowski et al., 2019).
- Short answers are entities or yes/no, so long explanatory answers are not evaluated as such.

### Comparison

| Data set | Question source | Context | Answer |
|---|---|---|---|
| Natural Questions | Google queries | whole Wikipedia page | long + short answer, or null |
| [[squad\|SQuAD]] | crowdworkers reading a passage | one paragraph | span |
| [[ms-marco\|MS MARCO]] | Bing queries | retrieved passages | human-written answer |
| [[mmlu\|MMLU]] | exams | none (closed book) | multiple choice |

Sources: Kwiatkowski et al. (2019), Jurafsky & Martin (2026).

### In practice

Results reported on "NQ" can refer to the original long/short-answer task on Wikipedia pages or to the open-domain question set with exact match on a normalised answer, so the setting must be stated when comparing systems (Roberts et al., 2020; Kwiatkowski et al., 2019).

### Key takeaway

Natural Questions pairs real Google search questions with Wikipedia pages and annotated long and short answers, and its open-domain version is a standard benchmark for retrieval and RAG.

### Sources

- Kwiatkowski, T. et al. (2019). *Natural Questions: A Benchmark for Question Answering Research.* Transactions of the Association for Computational Linguistics 7. [aclanthology.org](https://aclanthology.org/Q19-1026/)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 11: Information Retrieval and RAG. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/11.pdf)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
- Roberts, A., Raffel, C. & Shazeer, N. (2020). *How Much Knowledge Can You Pack Into the Parameters of a Language Model?* EMNLP 2020. [arXiv:2002.08910](https://arxiv.org/abs/2002.08910)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Natural Questions (NQ) ist ein Benchmark für [[question-answering|Question Answering]] aus echten, anonymisierten Anfragen an die Google-Suchmaschine, jeweils gepaart mit einer Wikipedia-Seite aus den ersten fünf Suchergebnissen (Kwiatkowski et al., 2019). Annotierende markieren eine lange Antwort (meist einen Absatz), eine kurze Antwort (eine oder mehrere Entitäten) oder Ja/Nein, oder Null, wenn die Seite die Frage nicht beantwortet; die öffentliche Version umfasst 307.373 Trainingsbeispiele sowie fünffach annotierte Entwicklungs- und Testmengen (Kwiatkowski et al., 2019). Ihre Open-Domain-Variante, bei der Systeme die Antwort in ganz Wikipedia finden müssen, wurde zu einem Standardtest für Retriever und [[retrieval-augmented-generation|RAG]] (Karpukhin et al., 2020).

### Funktionsweise

```text
Google-Suchanfragen (anonymisiert, aggregiert)
   ▼  heuristische Filter behalten frageartige Anfragen mit ≥ 8 Wörtern
   ▼  behalten Anfragen mit einer Wikipedia-Seite unter den ersten 5 Ergebnissen
(Frage, Wikipedia-Seite)
   ▼  Annotation: lange Antwort (Absatz, Tabelle, Liste) │ kurze Antwort (Entitäten) oder Ja/Nein │ NULL
Training: 307.373 einfach annotiert  ·  Dev: 7.830 und Test: 7.842 mit je 5 Annotationen
   ▼
Evaluation: Precision / Recall / F1 für lange und kurze Antworten gegen die fünffachen Annotationen
```

#### 1. Fragen aus echten Informationsbedürfnissen

Anders als Datensätze, deren Fragen Crowdworker beim Lesen einer Passage schrieben, nutzt NQ Fragen, die Menschen tatsächlich an eine Suchmaschine gestellt haben (Kwiatkowski et al., 2019). Einfache Heuristiken behalten Anfragen, die wie Fragen aussehen, etwa solche, die mit „who“ und einem Verb beginnen, verwerfen die meisten Nicht-Fragen und behalten die Mehrheit der Fragen mit acht oder mehr Wörtern; längere Anfragen wurden bevorzugt, weil sie komplexer sind (Kwiatkowski et al., 2019). Jurafsky und Martin (2026) ordnen NQ wie [[ms-marco|MS MARCO]] den Datensätzen mit echten Informationsbedürfnissen zu, im Gegensatz zu Prüfdatensätzen wie [[mmlu|MMLU]].

#### 2. Lange und kurze Antworten

Mit der Frage und einer ganzen Wikipedia-Seite wählt die annotierende Person eine lange Antwort, einen HTML-Bereich wie einen Absatz oder eine Tabelle, der die nötige Information enthält, und darin eine kurze Antwort: eine oder mehrere Entitäten oder eine Ja/Nein-Markierung (Kwiatkowski et al., 2019). So hat „When are hops added to the brewing process?“ die kurze Antwort „the boiling process“ und als lange Antwort einen Absatz der Wikipedia-Seite über das Bierbrauen (Jurafsky & Martin, 2026). Für 49 % der Beispiele wurde eine lange Antwort gefunden, für 36 % eine kurze Antwort oder Ja/Nein; die übrigen 51 % ohne Antwort bleiben enthalten, weil die Entscheidung, ob geantwortet wird, Teil der Aufgabe ist (Kwiatkowski et al., 2019).

#### 3. Qualität und menschliche Variabilität

Nachträgliche Prüfungen ergaben 90 % Precision für lange und 84 % für kurze Antworten (Kwiatkowski et al., 2019). Die 25-fache Annotation von 302 Beispielen zeigte, dass bei natürlichen Fragen oft echte Mehrdeutigkeit besteht, ob eine Antwort akzeptabel ist, und häufig mehrere akzeptable Antworten existieren; die Evaluation nutzt daher fünf Annotationen pro Entwicklungs- und Testbeispiel (Kwiatkowski et al., 2019).

#### 4. Evaluation und Baselines

Systeme werden mit Precision, Recall und F1 gegen die fünffachen Annotationen bewertet (Kwiatkowski et al., 2019; [[classification-metrics|Klassifikationsmetriken]]). Eine obere Schranke durch einen „Super-Annotator“ erreichte 87,2 F1 für lange und 75,7 F1 für kurze Antworten, während die beste Baseline des ursprünglichen Papers auf der Testmenge 55,0 und 35,1 F1 erreichte, ein großer Abstand (Kwiatkowski et al., 2019).

#### 5. Open-Domain- und Closed-Book-Nutzung

In der Open-Domain-Variante erhält ein Modell nur die Frage, muss Belege selbst abrufen und eine einzelne normalisierte Antwort erzeugen (Roberts et al., 2020). Dense Passage Retrieval wurde so evaluiert und übertraf [[bm25|BM25]] bei der Top-5-Genauigkeit deutlich, mit 65,2 % gegenüber 42,9 % ([[dense-passage-retrieval|Dense Passage Retrieval]]; Karpukhin et al., 2020). Roberts et al. (2020) nutzten dieselben Fragen Closed Book und beantworteten sie allein aus den Parametern von T5 ([[t5|T5]]). Derselbe Datensatz lässt sich also Open Book oder Closed Book nutzen (Jurafsky & Martin, 2026).

#### Ursprung und Varianten

NQ wurde von [[google|Google Research]] erstellt und 2019 in den Transactions of the Association for Computational Linguistics veröffentlicht (Kwiatkowski et al., 2019). Zu den Varianten gehören die Open-Domain-Fragenmenge der Retrieval-Arbeiten und das Multi-Answer-Setting der ursprünglichen Reading-Comprehension-Aufgabe (Roberts et al., 2020).

### Wann einsetzen

- Open-Domain-Retriever und RAG-Pipelines auf echten Nutzerfragen bewerten ([[rag-retrieval-evaluation|Retrieval-Evaluation]]).
- Reading Comprehension über ganze Wikipedia-Seiten trainieren und testen, einschließlich der Entscheidung, nicht zu antworten.
- Das Closed-Book-Wissen von Sprachmodellen messen ([[llm-evaluation|LLM-Evaluation]]).

### Stärken und Grenzen

**Stärken**
- Die Fragen spiegeln echte Informationsbedürfnisse statt passagengetriebener Crowd-Fragen (Kwiatkowski et al., 2019).
- Enthält unbeantwortbare Beispiele und mehrfache Annotationen für eine robuste Evaluation (Kwiatkowski et al., 2019).
- Große Trainingsmenge und weit verbreitet, sodass Ergebnisse zwischen Arbeiten vergleichbar sind.

**Grenzen**
- Nur Englisch und nur Wikipedia; die Fragen stammen von den Nutzenden einer Suchmaschine.
- Antworten können echt mehrdeutig sein, was die erreichbaren Werte begrenzt (Kwiatkowski et al., 2019).
- Kurze Antworten sind Entitäten oder Ja/Nein, lange erklärende Antworten werden als solche nicht bewertet.

### Vergleich

| Datensatz | Herkunft der Fragen | Kontext | Antwort |
|---|---|---|---|
| Natural Questions | Google-Anfragen | ganze Wikipedia-Seite | lange + kurze Antwort oder Null |
| [[squad\|SQuAD]] | Crowdworker beim Lesen einer Passage | ein Absatz | Spanne |
| [[ms-marco\|MS MARCO]] | Bing-Anfragen | abgerufene Passagen | von Menschen geschriebene Antwort |
| [[mmlu\|MMLU]] | Prüfungen | keiner (Closed Book) | Multiple Choice |

Quellen: Kwiatkowski et al. (2019), Jurafsky & Martin (2026).

### In der Praxis

Ergebnisse zu „NQ“ können sich auf die ursprüngliche Aufgabe mit langen und kurzen Antworten auf Wikipedia-Seiten oder auf die Open-Domain-Fragenmenge mit Exact Match auf eine normalisierte Antwort beziehen; beim Vergleich von Systemen muss das Setting daher angegeben werden (Roberts et al., 2020; Kwiatkowski et al., 2019).

### Merksatz

Natural Questions verbindet echte Google-Suchfragen mit Wikipedia-Seiten und annotierten langen und kurzen Antworten; seine Open-Domain-Variante ist ein Standard-Benchmark für Retrieval und RAG.

### Quellen

- Kwiatkowski, T. et al. (2019). *Natural Questions: A Benchmark for Question Answering Research.* Transactions of the Association for Computational Linguistics 7. [aclanthology.org](https://aclanthology.org/Q19-1026/)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 11: Information Retrieval and RAG. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/11.pdf)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
- Roberts, A., Raffel, C. & Shazeer, N. (2020). *How Much Knowledge Can You Pack Into the Parameters of a Language Model?* EMNLP 2020. [arXiv:2002.08910](https://arxiv.org/abs/2002.08910)
