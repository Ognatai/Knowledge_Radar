---
title_en: Ragas
title_de: Ragas
entity_type: Technology
aliases:
- RAGAS
- Retrieval Augmented Generation Assessment
sources:
- https://arxiv.org/abs/2309.15217
- https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/
- https://docs.ragas.io/en/stable/getstarted/rag_eval/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Ragas (Retrieval Augmented Generation Assessment) is an open-source framework for evaluating [[retrieval-augmented-generation|retrieval-augmented generation]] pipelines with metrics computed by prompting an LLM (Es et al., 2024). The original paper proposed three reference-free metrics: faithfulness (is the answer grounded in the retrieved context?), answer relevance (does it address the question?) and context relevance (is the retrieved context focused?). On the WikiEval dataset, the Ragas faithfulness metric agreed with human judgements in 95% of pairwise comparisons, far more than asking [[chatgpt|ChatGPT]] directly for a score (Es et al., 2024). The library has since grown to include context precision and recall, noise sensitivity, metrics for agents and tool use, [[sql|SQL]] and classical text comparison metrics (Ragas documentation, 2026).

### Core concepts

```text
question q ──→ retriever ──→ context c(q) ──→ LLM ──→ answer a(q)
                                │                        │
        context relevance / precision / recall      faithfulness: claims in a(q) supported by c(q)?
                                                     answer relevance: questions generated from a(q) ≈ q?
every metric = LLM prompts (+ embeddings) → score in [0, 1]
```

#### Faithfulness

An answer is faithful if the claims it makes can be inferred from the context (Es et al., 2024). An LLM first decomposes the answer into short statements, then checks for each statement whether the context supports it; the score is the share of supported statements, |V| / |S| (Es et al., 2024). Faithfulness targets [[hallucination-detection|hallucinations]] relative to the retrieved sources.

#### Answer relevance

Answer relevance penalises incomplete or redundant answers and ignores factuality (Es et al., 2024). The LLM generates n questions that the answer would respond to; the score is the average [[text-similarity-metrics|cosine similarity]] between the [[embeddings|embeddings]] of these questions and the original question (Es et al., 2024). The current library calls it response relevancy (Ragas documentation, 2026).

#### Context relevance, precision and recall

In the paper, context relevance is the share of context sentences that an LLM extracts as crucial for answering the question, which penalises redundant context (Es et al., 2024). The current library adds context precision, which evaluates whether the retriever ranks relevant chunks above irrelevant ones as an average of [[rag-retrieval-evaluation|precision@k]], and context recall, which measures how many of the relevant pieces of information were retrieved; context recall always needs a reference, and the main context precision variant uses a reference answer (Ragas documentation, 2026).

#### Origin and variants

Ragas was introduced with three reference-free metrics and integrations for llama-index and LangChain (Es et al., 2024); the documentation now also lists metrics for agents and tool use (topic adherence, tool call accuracy, agent goal accuracy), natural language comparison (factual correctness, semantic similarity, [[bleu|BLEU]], ROUGE, exact match), SQL, summarisation and general-purpose rubric-based scoring (Ragas documentation, 2026).

### Common usage

```python
from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness
from langchain_openai import ChatOpenAI

samples = [{"user_input": query,                 # question
            "retrieved_contexts": contexts,     # list of retrieved chunks
            "response": answer,                 # generated answer
            "reference": expected_answer}]      # optional reference answer
dataset = EvaluationDataset.from_list(samples)
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="..."))   # any judge model
result = evaluate(dataset=dataset,
                  metrics=[LLMContextRecall(), Faithfulness(), FactualCorrectness()],
                  llm=evaluator_llm)
# e.g. {'context_recall': 1.0, 'faithfulness': 0.857, 'factual_correctness': 0.728}
```

Source: Ragas documentation (2026), "Evaluate a simple RAG system".

### When to use it

- Comparing RAG configurations, such as chunking, retriever, prompt or model, without a fully annotated test set (Es et al., 2024; [[rag-evaluation|RAG evaluation]]).
- Separating retrieval problems from generation problems ([[rag-retrieval|RAG retrieval]], [[rag-generation-evaluation|RAG generation evaluation]]).
- Integrating evaluation into llama-index or LangChain workflows, for which the paper describes integrations (Es et al., 2024).

### Strengths and limitations

**Strengths**
- Faithfulness, answer relevance and context relevance can be computed without human reference answers (Es et al., 2024).
- On WikiEval, agreement with human judgements was 0.95 for faithfulness, 0.78 for answer relevance and 0.70 for context relevance, against 0.72, 0.52 and 0.63 for direct [[gpt|GPT]] scoring (Es et al., 2024).
- Faster evaluation cycles for RAG systems (Es et al., 2024).

**Limitations**
- Every score depends on the judge LLM and its prompts; the paper used gpt-3.5-turbo-16k and text-embedding-ada-002 ([[llm-as-a-judge|LLM-as-a-judge]]).
- Context relevance was the hardest dimension; ChatGPT often struggled to pick the crucial sentences, especially in long contexts (Es et al., 2024).
- WikiEval is small: 50 Wikipedia pages, with two annotators (Es et al., 2024).
- Several of the newer retrieval metrics need a reference after all (Ragas documentation, 2026).

### Comparison

| Metric (paper) | Question it answers | Needs reference |
|---|---|---|
| Faithfulness | Is every claim in the answer supported by the context? | no |
| Answer relevance | Does the answer address the question, completely and without redundancy? | no |
| Context relevance | How much of the retrieved context is actually needed? | no |
| Context recall (library) | Were the relevant pieces of information retrieved? | yes |

Sources: Es et al. (2024); Ragas documentation (2026).

### In practice

Fix the judge model and the Ragas version when comparing runs, since both change the scores. Check a sample of judgements by hand before relying on them, as the judge itself can be wrong ([[llm-as-a-judge|LLM-as-a-judge]]). Reference-free metrics show whether answers are grounded and on topic, not whether they are correct; for correctness, a small annotated reference set with context recall or factual correctness complements them ([[rag-evaluation|RAG evaluation]]).

### Key takeaway

Ragas evaluates RAG pipelines with LLM-computed metrics, notably faithfulness, answer relevance and context relevance without reference answers; it agrees well with humans on faithfulness, but its scores are only as good as the judge model behind them.

### Sources

- Es, S., James, J., Espinosa-Anke, L. & Schockaert, S. (2024). Ragas: Automated Evaluation of Retrieval Augmented Generation. *EACL 2024 System Demonstrations*. [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- Ragas documentation (2026). *List of available metrics*. [docs.ragas.io](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)
- Ragas documentation (2026). *Evaluate a simple RAG system*. [docs.ragas.io](https://docs.ragas.io/en/stable/getstarted/rag_eval/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ragas (Retrieval Augmented Generation Assessment) ist ein Open-Source-Framework zur Evaluation von [[retrieval-augmented-generation|Retrieval-Augmented-Generation]]-Pipelines mit Metriken, die durch Prompting eines LLM berechnet werden (Es et al., 2024). Das ursprüngliche Paper schlug drei referenzfreie Metriken vor: Faithfulness (ist die Antwort im abgerufenen Kontext begründet?), Answer Relevance (geht sie auf die Frage ein?) und Context Relevance (ist der abgerufene Kontext fokussiert?). Auf dem Datensatz WikiEval stimmte die Faithfulness-Metrik von Ragas in 95 % der paarweisen Vergleiche mit menschlichen Urteilen überein, weit häufiger als eine direkte Bewertung durch [[chatgpt|ChatGPT]] (Es et al., 2024). Die Bibliothek umfasst inzwischen auch Context Precision und Recall, Noise Sensitivity, Metriken für Agenten und Tool-Nutzung, [[sql|SQL]] sowie klassische Textvergleichsmetriken (Ragas documentation, 2026).

### Kernkonzepte

```text
Frage q ──→ Retriever ──→ Kontext c(q) ──→ LLM ──→ Antwort a(q)
                              │                        │
      Context Relevance / Precision / Recall      Faithfulness: Aussagen in a(q) durch c(q) gestützt?
                                                   Answer Relevance: aus a(q) erzeugte Fragen ≈ q?
jede Metrik = LLM-Prompts (+ Embeddings) → Wert in [0, 1]
```

#### Faithfulness

Eine Antwort ist faithful, wenn sich ihre Aussagen aus dem Kontext ableiten lassen (Es et al., 2024). Ein LLM zerlegt die Antwort zunächst in kurze Aussagen und prüft dann für jede, ob der Kontext sie stützt; der Wert ist der Anteil gestützter Aussagen, |V| / |S| (Es et al., 2024). Faithfulness zielt auf [[hallucination-detection|Halluzinationen]] gegenüber den abgerufenen Quellen.

#### Answer Relevance

Answer Relevance bestraft unvollständige oder redundante Antworten und lässt die Faktentreue außer Acht (Es et al., 2024). Das LLM erzeugt n Fragen, auf die die Antwort passen würde; der Wert ist die mittlere Kosinus-Ähnlichkeit zwischen den [[embeddings|Embeddings]] dieser Fragen und der ursprünglichen Frage (Es et al., 2024). Die aktuelle Bibliothek nennt sie Response Relevancy (Ragas documentation, 2026).

#### Context Relevance, Precision und Recall

Im Paper ist Context Relevance der Anteil der Kontextsätze, die ein LLM als entscheidend für die Antwort auf die Frage extrahiert, was redundanten Kontext bestraft (Es et al., 2024). Die aktuelle Bibliothek ergänzt Context Precision, die bewertet, ob der Retriever relevante Chunks vor irrelevanten einordnet, als Mittel von [[rag-retrieval-evaluation|Precision@k]], sowie Context Recall, die misst, wie viele der relevanten Informationen abgerufen wurden; Context Recall braucht immer eine Referenz, und die Hauptvariante von Context Precision nutzt eine Referenzantwort (Ragas documentation, 2026).

#### Herkunft und Varianten

Ragas wurde mit drei referenzfreien Metriken und Integrationen für llama-index und LangChain vorgestellt (Es et al., 2024); die Dokumentation führt inzwischen auch Metriken für Agenten und Tool-Nutzung (Topic Adherence, Tool Call Accuracy, Agent Goal Accuracy), für den Vergleich natürlicher Sprache (Factual Correctness, Semantic Similarity, [[bleu|BLEU]], ROUGE, Exact Match), für SQL, Zusammenfassungen sowie allgemeine, rubrikbasierte Bewertung auf (Ragas documentation, 2026).

### Typische Verwendung

```python
from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness
from langchain_openai import ChatOpenAI

samples = [{"user_input": query,                 # Frage
            "retrieved_contexts": contexts,     # Liste abgerufener Chunks
            "response": answer,                 # erzeugte Antwort
            "reference": expected_answer}]      # optionale Referenzantwort
dataset = EvaluationDataset.from_list(samples)
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="..."))   # beliebiges Bewertungsmodell
result = evaluate(dataset=dataset,
                  metrics=[LLMContextRecall(), Faithfulness(), FactualCorrectness()],
                  llm=evaluator_llm)
# z. B. {'context_recall': 1.0, 'faithfulness': 0.857, 'factual_correctness': 0.728}
```

Quelle: Ragas documentation (2026), "Evaluate a simple RAG system".

### Wann einsetzen

- Vergleich von RAG-Konfigurationen wie Chunking, Retriever, Prompt oder Modell ohne vollständig annotierte Testmenge (Es et al., 2024; [[rag-evaluation|RAG-Evaluation]]).
- Trennung von Retrieval- und Generierungsproblemen ([[rag-retrieval|RAG-Retrieval]], [[rag-generation-evaluation|Evaluation der RAG-Generierung]]).
- Einbindung der Evaluation in llama-index- oder LangChain-Workflows, für die das Paper Integrationen beschreibt (Es et al., 2024).

### Stärken und Grenzen

**Stärken**
- Faithfulness, Answer Relevance und Context Relevance lassen sich ohne menschliche Referenzantworten berechnen (Es et al., 2024).
- Auf WikiEval lag die Übereinstimmung mit menschlichen Urteilen bei 0,95 für Faithfulness, 0,78 für Answer Relevance und 0,70 für Context Relevance, gegenüber 0,72, 0,52 und 0,63 bei direkter GPT-Bewertung (Es et al., 2024).
- Schnellere Evaluationszyklen für RAG-Systeme (Es et al., 2024).

**Grenzen**
- Jeder Wert hängt vom bewertenden LLM und seinen Prompts ab; das Paper nutzte gpt-3.5-turbo-16k und text-embedding-ada-002 ([[llm-as-a-judge|LLM-as-a-Judge]]).
- Context Relevance war die schwierigste Dimension; ChatGPT hatte oft Mühe, die entscheidenden Sätze auszuwählen, besonders bei langen Kontexten (Es et al., 2024).
- WikiEval ist klein: 50 Wikipedia-Seiten mit zwei Annotatoren (Es et al., 2024).
- Mehrere der neueren Retrieval-Metriken brauchen doch eine Referenz (Ragas documentation, 2026).

### Vergleich

| Metrik (Paper) | Beantwortete Frage | Braucht Referenz |
|---|---|---|
| Faithfulness | Ist jede Aussage der Antwort durch den Kontext gestützt? | nein |
| Answer Relevance | Geht die Antwort vollständig und ohne Redundanz auf die Frage ein? | nein |
| Context Relevance | Wie viel des abgerufenen Kontexts wird tatsächlich gebraucht? | nein |
| Context Recall (Bibliothek) | Wurden die relevanten Informationen abgerufen? | ja |

Quellen: Es et al. (2024); Ragas documentation (2026).

### In der Praxis

Beim Vergleich von Durchläufen sollten das bewertende Modell und die Ragas-Version festgehalten werden, da beide die Werte verändern. Eine Stichprobe der Urteile sollte von Hand geprüft werden, bevor man sich auf sie verlässt, da auch der Bewerter irren kann ([[llm-as-a-judge|LLM-as-a-Judge]]). Referenzfreie Metriken zeigen, ob Antworten begründet und beim Thema sind, nicht, ob sie korrekt sind; für die Korrektheit ergänzt eine kleine annotierte Referenzmenge mit Context Recall oder Factual Correctness sie ([[rag-evaluation|RAG-Evaluation]]).

### Merksatz

Ragas evaluiert RAG-Pipelines mit LLM-berechneten Metriken, vor allem Faithfulness, Answer Relevance und Context Relevance ohne Referenzantworten; bei Faithfulness stimmt es gut mit Menschen überein, doch seine Werte sind nur so gut wie das bewertende Modell dahinter.

### Quellen

- Es, S., James, J., Espinosa-Anke, L. & Schockaert, S. (2024). Ragas: Automated Evaluation of Retrieval Augmented Generation. *EACL 2024 System Demonstrations*. [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- Ragas documentation (2026). *List of available metrics*. [docs.ragas.io](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)
- Ragas documentation (2026). *Evaluate a simple RAG system*. [docs.ragas.io](https://docs.ragas.io/en/stable/getstarted/rag_eval/)
