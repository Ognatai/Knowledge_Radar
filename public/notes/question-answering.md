---
title_en: Question Answering
title_de: Question Answering
entity_type: Concept
aliases:
- Question answering
- QA
- Open-domain question answering
- Reading comprehension
- Machine reading comprehension
- Closed-book question answering
- Open-book question answering
sources:
- https://web.stanford.edu/~jurafsky/slp3/11.pdf
- https://arxiv.org/abs/1606.05250
- https://arxiv.org/abs/1806.03822
- https://arxiv.org/abs/1704.00051
- https://arxiv.org/abs/2004.04906
- https://arxiv.org/abs/2005.11401
- https://arxiv.org/abs/1809.09600
- https://arxiv.org/abs/2002.08910
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Question answering (QA) is the task of returning an answer to a question posed in natural language, either from given documents (reading comprehension, open-book QA) or from a model's own parameters (closed-book QA) (Jurafsky & Martin, 2026). Modern open-domain systems combine a retriever that finds candidate passages in a large collection with a reader or generator that extracts or writes the answer (Chen et al., 2017; Karpukhin et al., 2020), which is the pattern behind [[retrieval-augmented-generation|retrieval-augmented generation]] (Lewis et al., 2020). Answers are evaluated with exact match and token-level F1 against gold answers (Jurafsky & Martin, 2026).

### How it works

```text
question ──► retriever (TF-IDF / BM25 / dense) ──► top-k passages from a collection
                                                      │
                     ┌────────────────────────────────┴──────────────────────────────┐
                     ▼                                                               ▼
       extractive reader: predict answer span                  generator (LLM): write answer
       in the passages (SQuAD-style)                           conditioned on question + passages
                     └────────────────────────────────┬──────────────────────────────┘
                                                      ▼
                         answer (+ citation of the supporting passage) ──► EM / F1 against gold
```

QA systems differ in where the knowledge comes from (given document, retrieved collection, model parameters, knowledge base), in the answer format (span, free text, multiple choice) and in the reasoning needed (single fact, several documents).

#### 1. Task variants

- **Reading comprehension:** a model gets a question and a document and must extract the answer from it (Jurafsky & Martin, 2026). In SQuAD, crowdworkers wrote more than 100,000 questions on Wikipedia articles, each answered by a span of the passage (Rajpurkar et al., 2016; [[squad|SQuAD]]).
- **Open-domain (open-book) QA:** the system must first find relevant documents in a large collection; Chen et al. (2017) call this machine reading at scale, with Wikipedia's more than 5 million articles as the only knowledge source.
- **Closed-book QA:** the language model answers without any retrieved context. Roberts et al. (2020) fine-tuned T5 to answer from its parameters alone and found that performance scales with model size and is competitive with open-domain systems that retrieve from an external knowledge source ([[t5|T5]]).
- **Multi-hop QA:** questions need facts from several documents; HotpotQA has 113,000 Wikipedia-based questions with sentence-level supporting facts and comparison questions (Yang et al., 2018).
- **Knowledge-based QA:** questions are mapped to a formal query over a database, from semantic parsing to text-to-[[sql|SQL]] (Jurafsky & Martin, 2026; [[knowledge-graphs|knowledge graphs]]).

#### 2. Retriever

Open-domain QA traditionally retrieved passages with sparse vector space models such as [[tf-idf|TF-IDF]] or [[bm25|BM25]] (Karpukhin et al., 2020). DrQA's document retriever used bigram hashing and TF-IDF matching over Wikipedia (Chen et al., 2017). Dense Passage Retrieval learns question and passage [[embeddings|embeddings]] with a dual encoder from a small number of question–passage pairs and outperformed a Lucene BM25 system by 9 to 19 percentage points in top-20 passage retrieval accuracy; on [[natural-questions|Natural Questions]] it reached 65.2% top-5 accuracy against 42.9% for BM25 (Karpukhin et al., 2020; [[dense-passage-retrieval|dense passage retrieval]]).

#### 3. Reader or generator

The extractive reader predicts the start and end of the answer span in a retrieved paragraph; DrQA used a multi-layer recurrent network ([[lstm|LSTM]]) trained to detect answers in Wikipedia paragraphs (Chen et al., 2017). The generator in RAG is a pre-trained [[attention-and-transformers|sequence-to-sequence model]] conditioned on retrieved passages, either using the same passage for the whole answer (RAG-Sequence) or a different passage per token (RAG-Token) (Lewis et al., 2020). With today's [[large-language-models|large language models]], the basic algorithm is to retrieve the top-k passages, put them into a prompt with the question ("Based on these texts, answer this question: …") and let the LLM generate the answer, optionally with knowledge citations such as numbered references to sources (Jurafsky & Martin, 2026).

#### 4. Unanswerable questions

Extractive systems tend to make unreliable guesses when the context does not contain the answer. SQuAD 2.0 added over 50,000 adversarially written unanswerable questions that look like answerable ones; the best model at the time reached 66.3 F1, against 89.5 F1 for humans and 48.9 F1 for a baseline that always abstains (Rajpurkar et al., 2018). Abstaining when evidence is missing is the QA counterpart of avoiding hallucinations in RAG ([[hallucination-detection|hallucination detection]]).

#### 5. Evaluation

For multiple-choice questions such as [[mmlu|MMLU]], systems are scored by exact match, the percentage of predictions identical to the gold answer; for free-text answers such as Natural Questions, token-level F1 treats prediction and gold answer as bags of tokens and averages F1 over questions (Jurafsky & Martin, 2026; [[classification-metrics|classification metrics]]). Before comparison, answers are usually lower-cased and stripped of articles, punctuation and extra whitespace (Roberts et al., 2020). On the first SQuAD, a [[logistic-regression|logistic regression]] model reached 51.0% F1 and humans 86.8% (Rajpurkar et al., 2016).

#### Origin and variants

Early systems in the 1960s and 1970s matched parsed questions against parsed text or translated them into logical forms over databases, such as LUNAR for lunar geology; the TREC evaluations added an influential QA track in 1999 (Jurafsky & Martin, 2026). Neural reading comprehension followed on SQuAD, then [[semantic-retrieval|dense retrieval]] with span readers, and then large language models that answer from their parameters or with retrieval (Jurafsky & Martin, 2026). Agent-based RAG lets the system decide when and from which collection to retrieve (Jurafsky & Martin, 2026; [[agentic-ai|agentic AI]]).

### When to use it

- Answering questions over a fixed document collection such as manuals, policies or contracts, usually as RAG ([[retrieval-augmented-generation|RAG]]).
- Customer support and assistants that must cite where an answer comes from ([[conversational-ai|conversational AI]]).
- Benchmarks for the knowledge and reading ability of language models ([[llm-evaluation|LLM evaluation]]).
- Natural language interfaces to databases and knowledge graphs.

### Strengths and limitations

**Strengths**
- Open-book QA can answer from current or private documents that were not in the model's training data (Jurafsky & Martin, 2026).
- Retrieved passages give provenance that users can check (Lewis et al., 2020).
- Extractive answers are copied from the source, which limits invention.

**Limitations**
- The answer can only be as good as retrieval: a passage that is not retrieved cannot be read ([[rag-failure-modes|RAG failure modes]]).
- Models guess when the answer is not in the context unless trained or prompted to abstain (Rajpurkar et al., 2018).
- Multi-hop questions need reasoning across documents, which single-step retrieval often misses (Yang et al., 2018).
- Exact match and token F1 penalise correct answers phrased differently from the gold answer.

### Comparison

| Setting | Knowledge source | Answer | Example dataset |
|---|---|---|---|
| Reading comprehension | one given passage | span | [[squad\|SQuAD]] |
| Open-domain QA | retrieved passages from a large collection | span or generated text | Natural Questions, [[ms-marco\|MS MARCO]] |
| Closed-book QA | model parameters | generated text | TriviaQA, Natural Questions (closed) |
| Multi-hop QA | several retrieved documents | span or comparison | HotpotQA |
| Exam-style QA | model parameters | multiple choice | MMLU |

Sources: Jurafsky & Martin (2026), Roberts et al. (2020), Yang et al. (2018).

### In practice

Datasets differ in whether their questions are natural information needs, such as anonymised search queries in Natural Questions and Bing queries in MS MARCO, or probing questions written to test systems, such as exam questions in MMLU; the same dataset can be used open-book or closed-book (Jurafsky & Martin, 2026). For RAG, an LLM can be instruction-tuned on questions annotated with retrieved passages and correct answers, and the retriever can be trained end to end with the generator (Jurafsky & Martin, 2026). Evaluating only the final answer hides whether retrieval or generation failed, so both are measured separately ([[rag-retrieval-evaluation|retrieval evaluation]], [[rag-generation-evaluation|generation evaluation]]).

### Key takeaway

Question answering pairs a source of knowledge with a way to read it: a retriever and a reader or LLM for open-book QA, the model's parameters for closed-book QA, scored by exact match and token F1.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 11: Information Retrieval and RAG. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/11.pdf)
- Rajpurkar, P., Zhang, J., Lopyrev, K. & Liang, P. (2016). *SQuAD: 100,000+ Questions for Machine Comprehension of Text.* EMNLP 2016. [arXiv:1606.05250](https://arxiv.org/abs/1606.05250)
- Rajpurkar, P., Jia, R. & Liang, P. (2018). *Know What You Don't Know: Unanswerable Questions for SQuAD.* ACL 2018. [arXiv:1806.03822](https://arxiv.org/abs/1806.03822)
- Chen, D., Fisch, A., Weston, J. & Bordes, A. (2017). *Reading Wikipedia to Answer Open-Domain Questions.* ACL 2017. [arXiv:1704.00051](https://arxiv.org/abs/1704.00051)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
- Yang, Z. et al. (2018). *HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering.* EMNLP 2018. [arXiv:1809.09600](https://arxiv.org/abs/1809.09600)
- Roberts, A., Raffel, C. & Shazeer, N. (2020). *How Much Knowledge Can You Pack Into the Parameters of a Language Model?* EMNLP 2020. [arXiv:2002.08910](https://arxiv.org/abs/2002.08910)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Question Answering (QA) ist die Aufgabe, auf eine in natürlicher Sprache gestellte Frage eine Antwort zu liefern, entweder aus gegebenen Dokumenten (Reading Comprehension, Open-Book-QA) oder aus den eigenen Parametern eines Modells (Closed-Book-QA) (Jurafsky & Martin, 2026). Moderne Open-Domain-Systeme kombinieren einen Retriever, der in einer großen Sammlung Kandidatenpassagen findet, mit einem Reader oder Generator, der die Antwort herausschneidet oder formuliert (Chen et al., 2017; Karpukhin et al., 2020); das ist das Muster hinter [[retrieval-augmented-generation|Retrieval-Augmented Generation]] (Lewis et al., 2020). Antworten werden mit Exact Match und F1 auf Token-Ebene gegen Referenzantworten bewertet (Jurafsky & Martin, 2026).

### Funktionsweise

```text
Frage ──► Retriever (TF-IDF / BM25 / dicht) ──► Top-k-Passagen aus einer Sammlung
                                                   │
                  ┌────────────────────────────────┴──────────────────────────────┐
                  ▼                                                               ▼
    extraktiver Reader: Antwortspanne                        Generator (LLM): Antwort schreiben,
    in den Passagen vorhersagen (wie SQuAD)                  bedingt auf Frage + Passagen
                  └────────────────────────────────┬──────────────────────────────┘
                                                   ▼
                   Antwort (+ Verweis auf die stützende Passage) ──► EM / F1 gegen Referenz
```

QA-Systeme unterscheiden sich darin, woher das Wissen kommt (gegebenes Dokument, durchsuchte Sammlung, Modellparameter, Wissensbasis), im Antwortformat (Spanne, freier Text, Multiple Choice) und im nötigen Schlussfolgern (einzelner Fakt, mehrere Dokumente).

#### 1. Varianten der Aufgabe

- **Reading Comprehension:** Ein Modell erhält eine Frage und ein Dokument und muss die Antwort daraus extrahieren (Jurafsky & Martin, 2026). Für SQuAD schrieben Crowdworker mehr als 100.000 Fragen zu Wikipedia-Artikeln, jeweils beantwortet durch eine Spanne der Passage (Rajpurkar et al., 2016; [[squad|SQuAD]]).
- **Open-Domain-QA (Open Book):** Das System muss zuerst relevante Dokumente in einer großen Sammlung finden; Chen et al. (2017) nennen das Machine Reading at Scale, mit den mehr als 5 Millionen Wikipedia-Artikeln als einziger Wissensquelle.
- **Closed-Book-QA:** Das Sprachmodell antwortet ohne abgerufenen Kontext. Roberts et al. (2020) trainierten T5 darauf nach, allein aus seinen Parametern zu antworten, und stellten fest, dass die Leistung mit der Modellgröße wächst und mit Open-Domain-Systemen mithält, die aus einer externen Wissensquelle abrufen ([[t5|T5]]).
- **Multi-Hop-QA:** Fragen brauchen Fakten aus mehreren Dokumenten; HotpotQA enthält 113.000 Wikipedia-basierte Fragen mit stützenden Fakten auf Satzebene und Vergleichsfragen (Yang et al., 2018).
- **Wissensbasiertes QA:** Fragen werden in eine formale Abfrage über eine Datenbank übersetzt, von semantischem Parsing bis Text-to-[[sql|SQL]] (Jurafsky & Martin, 2026; [[knowledge-graphs|Knowledge Graphs]]).

#### 2. Retriever

Open-Domain-QA rief Passagen traditionell mit dünn besetzten Vektorraummodellen wie [[tf-idf|TF-IDF]] oder [[bm25|BM25]] ab (Karpukhin et al., 2020). Der Dokument-Retriever von DrQA nutzte Bigram-Hashing und TF-IDF-Matching über Wikipedia (Chen et al., 2017). Dense Passage Retrieval lernt Frage- und Passagen-Embeddings mit einem Dual-Encoder aus wenigen Frage-Passagen-Paaren und übertraf ein Lucene-BM25-System bei der Top-20-Retrieval-Genauigkeit um 9 bis 19 Prozentpunkte; auf [[natural-questions|Natural Questions]] erreichte es 65,2 % Top-5-Genauigkeit gegenüber 42,9 % für BM25 (Karpukhin et al., 2020; [[dense-passage-retrieval|Dense Passage Retrieval]]).

#### 3. Reader oder Generator

Der extraktive Reader sagt Anfang und Ende der Antwortspanne in einem abgerufenen Absatz vorher; DrQA nutzte ein mehrschichtiges rekurrentes Netz ([[lstm|LSTM]]), das darauf trainiert war, Antworten in Wikipedia-Absätzen zu finden (Chen et al., 2017). Der Generator in RAG ist ein vortrainiertes Sequence-to-Sequence-Modell, das auf abgerufene Passagen bedingt ist und entweder dieselbe Passage für die ganze Antwort (RAG-Sequence) oder pro Token eine andere Passage nutzt (RAG-Token) (Lewis et al., 2020). Mit heutigen großen Sprachmodellen lautet der Grundalgorithmus: die Top-k-Passagen abrufen, sie mit der Frage in einen Prompt setzen („Based on these texts, answer this question: …“) und das LLM die Antwort erzeugen lassen, optional mit Quellenverweisen wie nummerierten Referenzen (Jurafsky & Martin, 2026).

#### 4. Unbeantwortbare Fragen

Extraktive Systeme raten oft unzuverlässig, wenn der Kontext die Antwort nicht enthält. SQuAD 2.0 ergänzte über 50.000 gezielt so geschriebene unbeantwortbare Fragen, dass sie beantwortbaren ähneln; das damals beste Modell erreichte 66,3 F1, Menschen 89,5 F1 und eine Baseline, die immer passt, 48,9 F1 (Rajpurkar et al., 2018). Sich zu enthalten, wenn Belege fehlen, ist das QA-Gegenstück zur Vermeidung von Halluzinationen in RAG ([[hallucination-detection|Halluzinationserkennung]]).

#### 5. Evaluation

Multiple-Choice-Fragen wie in [[mmlu|MMLU]] werden mit Exact Match bewertet, dem Anteil der Vorhersagen, die mit der Referenzantwort identisch sind; bei Freitextantworten wie in Natural Questions behandelt F1 auf Token-Ebene Vorhersage und Referenz als Bags of Tokens und mittelt F1 über die Fragen (Jurafsky & Martin, 2026; [[classification-metrics|Klassifikationsmetriken]]). Vor dem Vergleich werden Antworten meist kleingeschrieben und von Artikeln, Satzzeichen und überzähligen Leerzeichen befreit (Roberts et al., 2020). Beim ersten SQuAD erreichte ein Modell mit logistischer Regression 51,0 % F1 und Menschen 86,8 % (Rajpurkar et al., 2016).

#### Ursprung und Varianten

Frühe Systeme der 1960er- und 1970er-Jahre glichen geparste Fragen mit geparstem Text ab oder übersetzten sie in logische Formen über Datenbanken, etwa LUNAR für die Mondgeologie; die TREC-Evaluationen ergänzten 1999 einen einflussreichen QA-Track (Jurafsky & Martin, 2026). Es folgten neuronale Reading Comprehension auf SQuAD, dann [[semantic-retrieval|Dense Retrieval]] mit Span-Readern und dann große Sprachmodelle, die aus ihren Parametern oder mit Retrieval antworten (Jurafsky & Martin, 2026). Agentenbasiertes RAG lässt das System entscheiden, wann und aus welcher Sammlung abgerufen wird (Jurafsky & Martin, 2026; [[agentic-ai|Agentic AI]]).

### Wann einsetzen

- Fragen über eine feste Dokumentsammlung wie Handbücher, Richtlinien oder Verträge beantworten, meist als RAG ([[retrieval-augmented-generation|RAG]]).
- Kundensupport und Assistenten, die angeben müssen, woher eine Antwort stammt ([[conversational-ai|Conversational AI]]).
- Benchmarks für Wissen und Lesefähigkeit von Sprachmodellen ([[llm-evaluation|LLM-Evaluation]]).
- Natürlichsprachliche Schnittstellen zu Datenbanken und Knowledge Graphs.

### Stärken und Grenzen

**Stärken**
- Open-Book-QA kann aus aktuellen oder privaten Dokumenten antworten, die nicht in den Trainingsdaten des Modells waren (Jurafsky & Martin, 2026).
- Abgerufene Passagen liefern eine Herkunft, die Nutzende prüfen können (Lewis et al., 2020).
- Extraktive Antworten werden aus der Quelle kopiert, was Erfindungen begrenzt.

**Grenzen**
- Die Antwort kann nur so gut sein wie das Retrieval: Eine nicht abgerufene Passage kann nicht gelesen werden ([[rag-failure-modes|RAG-Fehlermuster]]).
- Modelle raten, wenn die Antwort nicht im Kontext steht, sofern sie nicht trainiert oder angewiesen werden, sich zu enthalten (Rajpurkar et al., 2018).
- Multi-Hop-Fragen erfordern Schlussfolgern über Dokumente hinweg, das einstufiges Retrieval oft verfehlt (Yang et al., 2018).
- Exact Match und Token-F1 bestrafen richtige Antworten, die anders formuliert sind als die Referenz.

### Vergleich

| Setting | Wissensquelle | Antwort | Beispieldatensatz |
|---|---|---|---|
| Reading Comprehension | eine gegebene Passage | Spanne | [[squad\|SQuAD]] |
| Open-Domain-QA | abgerufene Passagen aus einer großen Sammlung | Spanne oder generierter Text | Natural Questions, [[ms-marco\|MS MARCO]] |
| Closed-Book-QA | Modellparameter | generierter Text | TriviaQA, Natural Questions (geschlossen) |
| Multi-Hop-QA | mehrere abgerufene Dokumente | Spanne oder Vergleich | HotpotQA |
| Prüfungsfragen | Modellparameter | Multiple Choice | MMLU |

Quellen: Jurafsky & Martin (2026), Roberts et al. (2020), Yang et al. (2018).

### In der Praxis

Datensätze unterscheiden sich darin, ob ihre Fragen echte Informationsbedürfnisse sind, etwa anonymisierte Suchanfragen in Natural Questions und Bing-Anfragen in MS MARCO, oder Prüffragen, die Systeme testen sollen, etwa Prüfungsfragen in MMLU; derselbe Datensatz lässt sich Open Book oder Closed Book nutzen (Jurafsky & Martin, 2026). Für RAG kann ein LLM per [[instruction-tuning|Instruction Tuning]] auf Fragen mit abgerufenen Passagen und richtigen Antworten trainiert werden, und der Retriever lässt sich Ende-zu-Ende mit dem Generator trainieren (Jurafsky & Martin, 2026). Wird nur die Endantwort bewertet, bleibt verborgen, ob Retrieval oder Generierung versagt hat; deshalb werden beide getrennt gemessen ([[rag-retrieval-evaluation|Retrieval-Evaluation]], [[rag-generation-evaluation|Generierungs-Evaluation]]).

### Merksatz

Question Answering verbindet eine Wissensquelle mit einem Weg, sie zu lesen: Retriever und Reader oder LLM bei Open-Book-QA, die Modellparameter bei Closed-Book-QA, bewertet mit Exact Match und Token-F1.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 11: Information Retrieval and RAG. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/11.pdf)
- Rajpurkar, P., Zhang, J., Lopyrev, K. & Liang, P. (2016). *SQuAD: 100,000+ Questions for Machine Comprehension of Text.* EMNLP 2016. [arXiv:1606.05250](https://arxiv.org/abs/1606.05250)
- Rajpurkar, P., Jia, R. & Liang, P. (2018). *Know What You Don't Know: Unanswerable Questions for SQuAD.* ACL 2018. [arXiv:1806.03822](https://arxiv.org/abs/1806.03822)
- Chen, D., Fisch, A., Weston, J. & Bordes, A. (2017). *Reading Wikipedia to Answer Open-Domain Questions.* ACL 2017. [arXiv:1704.00051](https://arxiv.org/abs/1704.00051)
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP 2020. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
- Yang, Z. et al. (2018). *HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering.* EMNLP 2018. [arXiv:1809.09600](https://arxiv.org/abs/1809.09600)
- Roberts, A., Raffel, C. & Shazeer, N. (2020). *How Much Knowledge Can You Pack Into the Parameters of a Language Model?* EMNLP 2020. [arXiv:2002.08910](https://arxiv.org/abs/2002.08910)
