---
title_en: Memory in LLMs
title_de: Gedächtnis in LLMs
entity_type: Concept
aliases:
- LLM memory
- Memory bank
- Memory Bank
- Agent memory
- Long-term memory for LLMs
- Conditional memory
sources:
- https://arxiv.org/abs/2012.14913
- https://arxiv.org/abs/1911.00172
- https://arxiv.org/abs/2203.08913
- https://arxiv.org/abs/2601.07372
- https://arxiv.org/abs/2310.08560
- https://arxiv.org/abs/2305.10250
- https://arxiv.org/abs/2304.03442
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

"Memory" in [[large-language-models|large language models]] refers to several different mechanisms. Parametric memory is knowledge stored in the weights; the feed-forward layers of transformers act as key-value memories over textual patterns (Geva et al., 2020). Inside the architecture, models can add explicit memories that are looked up rather than computed: nearest-neighbour memories over past representations (Khandelwal et al., 2019; Wu et al., 2022) or, as in DeepSeek's Engram, a large table of n-gram embeddings retrieved in constant time, which relieved the network from reconstructing static knowledge and improved reasoning as well as knowledge tasks (Cheng et al., 2026). Outside the model, agents keep a memory bank of past conversations, summaries and reflections that is retrieved into the context when needed, as in MemoryBank, [[memgpt|MemGPT]] and Generative Agents (Zhong et al., 2023; Packer et al., 2023; Park et al., 2023). The common goal is to make more knowledge available than the context window holds, without retraining the model for every new fact.

### How it works

```text
                ┌─ parametric memory: weights (FFN layers as key-value memories)
inside model ───┼─ conditional memory: hashed n-gram table, O(1) lookup (Engram)
                └─ retrieval memory: kNN over stored (key, value) representations
working memory:   context window (prompt, history, retrieved items)
outside model:    memory bank / store ──► retriever ──► context
                  (conversations, event summaries, user profile, reflections)
                  ◄── updater: write, summarise, forget
```

#### 1. Parametric memory in the weights

Feed-forward layers make up two-thirds of a transformer's parameters, and Geva et al. (2020) showed that they operate as key-value memories: each key correlates with textual patterns in the training data, and each value induces a distribution over the output vocabulary. Lower layers capture shallow patterns and upper layers more semantic ones, and the output of a layer is a composition of its memories that is refined through the residual connections ([[attention-and-transformers|attention and transformers]]; Geva et al., 2020). Such knowledge is acquired in training and changes only through further training, which is why adding knowledge usually means [[llm-adaptation|fine-tuning]] or [[retrieval-augmented-generation|retrieval]] instead ([[rag-vs-fine-tuning|RAG vs. fine-tuning]]).

#### 2. Working memory: the context window

Everything the model can use at inference time without weights or external stores has to fit into its context: prompt, conversation history and retrieved material. Limited context windows constrain extended conversations and document analysis, which is the starting point of memory systems for agents (Packer et al., 2023). Deciding what goes into this window is the subject of [[context-engineering|context engineering]].

#### 3. Retrieval memories inside the model

Khandelwal et al. (2019) extended a pretrained language model with a k-nearest-neighbour model over its own embedding space (kNN-LM): neighbours from any text collection are retrieved and interpolated with the model's prediction, which lowered Wikitext-103 perplexity to 15.79 without extra training and helped most with rare patterns such as factual knowledge. Memorizing Transformers let the model memorise internal representations of past inputs at inference time: an approximate kNN lookup into a non-differentiable memory of recent (key, value) pairs improved language modelling on web text, arXiv papers, books, code and formal theorems, kept improving with memory sizes up to 262K tokens and allowed the model to use functions and theorems defined only at test time (Wu et al., 2022). Both use [[k-nearest-neighbours|nearest-neighbour search]] over [[embeddings|embeddings]], as in [[vector-databases|vector databases]].

#### 4. Conditional memory: Engram

Cheng et al. (2026) argue that transformers lack a native primitive for knowledge lookup and therefore simulate retrieval through computation. Their Engram module modernises classic [[n-gram-language-models|n-gram]] embeddings: suffix n-grams of the input are compressed (tokenizer compression, so that variants such as "Apple" and " apple" can share an entry) and mapped by multi-head hashing to entries of a large embedding table, the retrieved vectors are gated by the current hidden state and refined by a lightweight convolution, and the result is fused into the backbone (Cheng et al., 2026). Because the addresses depend only on the input tokens, lookups are deterministic and take constant time, and the table can be prefetched from host memory: offloading a 100-billion-parameter table incurred negligible overhead (Cheng et al., 2026). The authors frame this as conditional memory, a second axis of sparsity next to the conditional computation of Mixture-of-Experts, and found a U-shaped scaling law for splitting parameters between the two; Engram-27B outperformed an MoE baseline with the same parameters and FLOPs, with gains not only on knowledge benchmarks (MMLU +3.4, CMMLU +4.0) but larger ones on reasoning (BBH +5.0, ARC-Challenge +3.7), code and maths ([[humaneval|HumanEval]] +3.0, MATH +2.4) and long-context retrieval (Multi-Query NIAH from 84.2 to 97.0) (Cheng et al., 2026). Mechanistic analyses suggest that Engram relieves the early layers from reconstructing static knowledge, which effectively deepens the network for reasoning, and that delegating local dependencies to lookups frees attention for global context (Cheng et al., 2026).

#### 5. External memory for agents

Agents store what happened in earlier sessions outside the model and retrieve it later, in effect [[retrieval-augmented-generation|retrieval-augmented generation]] over their own history.

- **MemGPT** applies virtual context management, inspired by hierarchical memory in operating systems: the LLM manages memory tiers and moves data between fast and slow memory, using interrupts to manage control flow, so that it can analyse documents far larger than its context window and hold multi-session conversations (Packer et al., 2023).
- **MemoryBank** consists of a memory storage, a memory retriever and a memory updater. The storage holds conversation records with timestamps, hierarchical summaries of past events and an evolving profile of the user's personality; the retriever encodes every conversation turn and summary with a dual-tower dense retriever similar to [[dense-passage-retrieval|Dense Passage Retrieval]], indexes them with [[faiss|FAISS]] and searches them with the encoded current context; the updater, inspired by the Ebbinghaus forgetting curve, lets memories fade with elapsed time and strengthens those that are recalled (Zhong et al., 2023). MemoryBank works with closed and open models and was demonstrated in a companion chatbot, SiliconFriend (Zhong et al., 2023).
- **Generative Agents** store a complete record of an agent's experiences in natural language, synthesise these memories over time into higher-level reflections and retrieve them to plan behaviour; ablations showed that observation, planning and reflection each contributed critically to believable behaviour (Park et al., 2023).

Provider [[apis|APIs]] offer memory as a tool: [[anthropic|Anthropic]]'s memory tool lets a model store and retrieve information across conversations in files that the developer controls ([[tool-calling|tool calling]]; Anthropic documentation).

#### Origin and variants

Parametric memory was analysed by Geva et al. (2020); retrieval memories inside the model followed with kNN-LM (Khandelwal et al., 2019) and Memorizing Transformers (Wu et al., 2022), and conditional memory with Engram (Cheng et al., 2026). Agent memories were developed in 2023 with MemoryBank, MemGPT and Generative Agents (Zhong et al., 2023; Packer et al., 2023; Park et al., 2023), and agent frameworks now ship memory and session state as a standard building block ([[agent-frameworks|agent frameworks]]).

### When to use it

- External memory: when an assistant has to remember users or tasks across sessions, as in companions, personal assistants or long-running agents (Zhong et al., 2023; Packer et al., 2023).
- Retrieval memories: when knowledge should be added or swapped at inference time without retraining, for example for domain adaptation (Khandelwal et al., 2019; Wu et al., 2022).
- Conditional memory: as an architecture choice when training models, to add capacity for static knowledge cheaply (Cheng et al., 2026).

### Strengths and limitations

**Strengths**
- External and retrieval memories extend what a model can use beyond its context window and can be updated without training (Packer et al., 2023; Khandelwal et al., 2019).
- Explicit lookup memory adds capacity at low compute cost and can live in cheaper host memory (Cheng et al., 2026).
- Agent memories can summarise and forget, so that the stored history stays relevant (Zhong et al., 2023).

**Limitations**
- Parametric memory can only be changed by training (Geva et al., 2020).
- External memory depends on retrieval quality: memories that are not retrieved do not exist for the model, as with any [[rag-failure-modes|RAG failure]].
- Stored conversation histories and user profiles are personal data in many applications, which raises questions of deletion and access.
- Conditional memory such as Engram is part of pretraining and cannot be added to an existing model by users (Cheng et al., 2026).

### Comparison

| Memory | Where | Written by | Read by | Example |
|---|---|---|---|---|
| Parametric | weights | training | forward pass | FFN key-value memories |
| Conditional | embedding table in the model | training | hashed n-gram lookup | Engram |
| Retrieval inside the model | datastore of representations | inference or offline | kNN search | kNN-LM, Memorizing Transformers |
| Working | context window | application | attention | prompt, history |
| External / memory bank | database or files | agent or application | retriever, tool call | MemoryBank, MemGPT |

Sources: Geva et al. (2020); Cheng et al. (2026); Khandelwal et al. (2019); Wu et al. (2022); Zhong et al. (2023); Packer et al. (2023).

### In practice

External memories are built from the same components as [[rag-retrieval|RAG retrieval]]: chunking of conversations, [[semantic-retrieval|semantic retrieval]] and ranking, plus policies for summarising and forgetting. What is stored has to be traceable and deletable, especially user profiles ([[gdpr|GDPR]]), and memory reads and writes are logged like any tool call ([[llm-observability-and-tracing|LLM observability and tracing]]).

### Regulatory context

Persistent memories about users are personal data when they relate to identifiable people; the [[gdpr|GDPR]] then applies, including erasure under Art. 17. Keeping such data in an external store rather than in model weights makes deletion feasible.

### Key takeaway

LLM memory is a family of mechanisms, from knowledge in the weights and hashed n-gram lookup tables inside the model to memory banks that agents fill, summarise and retrieve from, all aimed at giving the model more knowledge than its context window holds.

### Sources

- Geva, M., Schuster, R., Berant, J. & Levy, O. (2020). *Transformer Feed-Forward Layers Are Key-Value Memories.* arXiv:2012.14913. [arXiv](https://arxiv.org/abs/2012.14913)
- Khandelwal, U., Levy, O., Jurafsky, D., Zettlemoyer, L. & Lewis, M. (2019). *Generalization through Memorization: Nearest Neighbor Language Models.* arXiv:1911.00172. [arXiv](https://arxiv.org/abs/1911.00172)
- Wu, Y., Rabe, M. N., Hutchins, D. & Szegedy, C. (2022). *Memorizing Transformers.* arXiv:2203.08913. [arXiv](https://arxiv.org/abs/2203.08913)
- Cheng, X., Tian, R., Zeng, W., Dai, D., Chen, Q., Wang, B. et al. (2026). *Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models.* arXiv:2601.07372. [arXiv](https://arxiv.org/abs/2601.07372)
- Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I. & Gonzalez, J. E. (2023). *MemGPT: Towards LLMs as Operating Systems.* arXiv:2310.08560. [arXiv](https://arxiv.org/abs/2310.08560)
- Zhong, W., Guo, L., Gao, Q., Ye, H. & Wang, Y. (2023). *MemoryBank: Enhancing Large Language Models with Long-Term Memory.* arXiv:2305.10250. [arXiv](https://arxiv.org/abs/2305.10250)
- Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P. & Bernstein, M. S. (2023). *Generative Agents: Interactive Simulacra of Human Behavior.* arXiv:2304.03442. [arXiv](https://arxiv.org/abs/2304.03442)
- Anthropic (2026). *Tool use with Claude.* Claude Developer Platform documentation. [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

„Gedächtnis“ (Memory) bezeichnet bei großen Sprachmodellen mehrere verschiedene Mechanismen. Parametrisches Gedächtnis ist in den Gewichten gespeichertes Wissen; die Feed-Forward-Schichten von Transformern wirken als Key-Value-Speicher über Textmuster (Geva et al., 2020). In der Architektur können Modelle explizite Speicher ergänzen, die nachgeschlagen statt berechnet werden: Nearest-Neighbour-Speicher über frühere Repräsentationen (Khandelwal et al., 2019; Wu et al., 2022) oder, wie bei DeepSeeks Engram, eine große Tabelle von n-Gramm-Embeddings, die in konstanter Zeit abgerufen wird; das entlastete das Netz davon, statisches Wissen nachzubilden, und verbesserte sowohl Schlussfolgern als auch Wissensaufgaben (Cheng et al., 2026). Außerhalb des Modells führen Agenten eine Memory Bank aus früheren Gesprächen, Zusammenfassungen und Reflexionen, die bei Bedarf in den Kontext geholt wird, etwa in MemoryBank, [[memgpt|MemGPT]] und Generative Agents (Zhong et al., 2023; Packer et al., 2023; Park et al., 2023). Gemeinsames Ziel ist, mehr Wissen verfügbar zu machen, als das Kontextfenster fasst, ohne das Modell für jede neue Tatsache neu zu trainieren.

### Funktionsweise

```text
                 ┌─ parametrisches Gedächtnis: Gewichte (FFN-Schichten als Key-Value-Speicher)
im Modell ───────┼─ Conditional Memory: gehashte n-Gramm-Tabelle, O(1)-Lookup (Engram)
                 └─ Retrieval-Speicher: kNN über gespeicherte (Key, Value)-Repräsentationen
Arbeitsgedächtnis: Kontextfenster (Prompt, Verlauf, abgerufene Einträge)
außerhalb:         Memory Bank / Speicher ──► Retriever ──► Kontext
                   (Gespräche, Ereigniszusammenfassungen, Nutzerprofil, Reflexionen)
                   ◄── Updater: schreiben, zusammenfassen, vergessen
```

#### 1. Parametrisches Gedächtnis in den Gewichten

Feed-Forward-Schichten machen zwei Drittel der Parameter eines Transformers aus, und Geva et al. (2020) zeigten, dass sie als Key-Value-Speicher arbeiten: Jeder Key korreliert mit Textmustern in den Trainingsdaten, und jeder Value erzeugt eine Verteilung über das Ausgabevokabular. Untere Schichten erfassen oberflächliche Muster, obere eher semantische, und die Ausgabe einer Schicht ist eine Zusammensetzung ihrer Speicher, die über die Residualverbindungen weiter verfeinert wird ([[attention-and-transformers|Attention und Transformer]]; Geva et al., 2020). Solches Wissen entsteht im Training und ändert sich nur durch weiteres Training; deshalb bedeutet Wissen hinzufügen meist [[llm-adaptation|Fine-Tuning]] oder stattdessen [[retrieval-augmented-generation|Retrieval]] ([[rag-vs-fine-tuning|RAG vs. Fine-Tuning]]).

#### 2. Arbeitsgedächtnis: das Kontextfenster

Alles, was das Modell zur Inferenzzeit ohne Gewichte oder externe Speicher nutzen kann, muss in seinen Kontext passen: Prompt, Gesprächsverlauf und abgerufenes Material. Begrenzte Kontextfenster schränken lange Gespräche und Dokumentanalysen ein; hier setzen Gedächtnissysteme für Agenten an (Packer et al., 2023). Was in dieses Fenster gelangt, behandelt [[context-engineering|Context Engineering]].

#### 3. Retrieval-Speicher im Modell

Khandelwal et al. (2019) erweiterten ein vortrainiertes Sprachmodell um ein k-Nearest-Neighbour-Modell über seinem eigenen Embedding-Raum (kNN-LM): Nachbarn aus einer beliebigen Textsammlung werden abgerufen und mit der Vorhersage des Modells interpoliert; das senkte die Perplexität auf Wikitext-103 ohne zusätzliches Training auf 15,79 und half vor allem bei seltenen Mustern wie Faktenwissen. Memorizing Transformers lassen das Modell interne Repräsentationen früherer Eingaben zur Inferenzzeit speichern: Ein Approximate-kNN-Lookup in einen nicht differenzierbaren Speicher jüngerer (Key, Value)-Paare verbesserte die Sprachmodellierung auf Webtext, arXiv-Artikeln, Büchern, Code und formalen Theoremen, wurde mit Speichergrößen bis 262.000 Tokens stetig besser und ließ das Modell Funktionen und Theoreme nutzen, die erst zur Testzeit definiert wurden (Wu et al., 2022). Beide nutzen eine [[k-nearest-neighbours|Nächste-Nachbarn-Suche]] über [[embeddings|Embeddings]], wie in [[vector-databases|Vektordatenbanken]].

#### 4. Conditional Memory: Engram

Cheng et al. (2026) argumentieren, dass Transformern ein eigenes Grundelement zum Nachschlagen von Wissen fehlt und sie Retrieval daher durch Rechnen nachbilden. Ihr Modul Engram modernisiert klassische [[n-gram-language-models|n-Gramm]]-Embeddings: Suffix-n-Gramme der Eingabe werden komprimiert (Tokenizer Compression, damit Varianten wie „Apple“ und „ apple“ einen Eintrag teilen können) und per Multi-Head Hashing auf Einträge einer großen Embedding-Tabelle abgebildet, die abgerufenen Vektoren werden durch den aktuellen Hidden State gewichtet (Gating) und durch eine leichte Faltung verfeinert, und das Ergebnis fließt in das Backbone ein (Cheng et al., 2026). Weil die Adressen nur von den Eingabetokens abhängen, sind die Lookups deterministisch und brauchen konstante Zeit, und die Tabelle kann vorab aus dem Hauptspeicher des Hosts geladen werden: Eine ausgelagerte Tabelle mit 100 Milliarden Parametern verursachte vernachlässigbaren Mehraufwand (Cheng et al., 2026). Die Autorinnen und Autoren beschreiben das als Conditional Memory, eine zweite Achse der Sparsity neben der bedingten Berechnung von Mixture-of-Experts, und fanden ein U-förmiges Skalierungsgesetz für die Aufteilung der Parameter zwischen beiden; Engram-27B übertraf eine MoE-Basis mit gleichen Parametern und FLOPs, nicht nur bei Wissens-Benchmarks (MMLU +3,4, CMMLU +4,0), sondern stärker beim Schlussfolgern (BBH +5,0, ARC-Challenge +3,7), bei Code und Mathematik ([[humaneval|HumanEval]] +3,0, MATH +2,4) und beim Retrieval in langen Kontexten (Multi-Query NIAH von 84,2 auf 97,0) (Cheng et al., 2026). Mechanistische Analysen deuten darauf hin, dass Engram die frühen Schichten davon entlastet, statisches Wissen nachzubilden, was das Netz für das Schlussfolgern effektiv vertieft, und dass das Auslagern lokaler Abhängigkeiten an Lookups Attention für den globalen Kontext frei macht (Cheng et al., 2026).

#### 5. Externes Gedächtnis für Agenten

Agenten speichern, was in früheren Sitzungen geschah, außerhalb des Modells und rufen es später ab, im Grunde [[retrieval-augmented-generation|Retrieval-Augmented Generation]] über die eigene Vorgeschichte.

- **MemGPT** überträgt virtuelle Kontextverwaltung nach dem Vorbild hierarchischen Speichers in Betriebssystemen: Das LLM verwaltet Speicherebenen und verschiebt Daten zwischen schnellem und langsamem Speicher, Interrupts steuern den Ablauf, sodass es Dokumente weit über sein Kontextfenster hinaus analysieren und Gespräche über mehrere Sitzungen führen kann (Packer et al., 2023).
- **MemoryBank** besteht aus einem Speicher, einem Retriever und einem Updater. Der Speicher enthält Gesprächsprotokolle mit Zeitstempeln, hierarchische Zusammenfassungen vergangener Ereignisse und ein sich entwickelndes Profil der Persönlichkeit der Nutzenden; der Retriever kodiert jede Gesprächsrunde und Zusammenfassung mit einem Dual-Tower-Dense-Retriever ähnlich [[dense-passage-retrieval|Dense Passage Retrieval]], indexiert sie mit [[faiss|FAISS]] und durchsucht sie mit dem kodierten aktuellen Kontext; der Updater lässt Erinnerungen nach dem Vorbild der Ebbinghaus'schen Vergessenskurve mit der Zeit verblassen und stärkt die abgerufenen (Zhong et al., 2023). MemoryBank funktioniert mit geschlossenen und offenen Modellen und wurde an einem Companion-Chatbot, SiliconFriend, gezeigt (Zhong et al., 2023).
- **Generative Agents** speichern eine vollständige Aufzeichnung der Erlebnisse eines Agenten in natürlicher Sprache, fassen diese Erinnerungen mit der Zeit zu übergeordneten Reflexionen zusammen und rufen sie zur Verhaltensplanung ab; Ablationen zeigten, dass Beobachtung, Planung und Reflexion jeweils entscheidend zu glaubwürdigem Verhalten beitrugen (Park et al., 2023).

Anbieter-APIs bieten Gedächtnis als Tool an: Mit dem Memory Tool von [[anthropic|Anthropic]] speichert und liest ein Modell Informationen über Gespräche hinweg in Dateien, die die Entwicklerinnen und Entwickler kontrollieren ([[tool-calling|Tool Calling]]; Anthropic-Dokumentation).

#### Herkunft und Varianten

Parametrisches Gedächtnis analysierten Geva et al. (2020); Retrieval-Speicher im Modell folgten mit kNN-LM (Khandelwal et al., 2019) und Memorizing Transformers (Wu et al., 2022), Conditional Memory mit Engram (Cheng et al., 2026). Gedächtnis für Agenten entstand 2023 mit MemoryBank, MemGPT und Generative Agents (Zhong et al., 2023; Packer et al., 2023; Park et al., 2023), und Agent-Frameworks liefern Gedächtnis und Sitzungszustand heute als Standardbaustein mit ([[agent-frameworks|Agent-Frameworks]]).

### Wann einsetzen

- Externes Gedächtnis: wenn ein Assistent sich über Sitzungen hinweg an Nutzende oder Aufgaben erinnern muss, etwa bei Companions, persönlichen Assistenten oder lang laufenden Agenten (Zhong et al., 2023; Packer et al., 2023).
- Retrieval-Speicher: wenn Wissen zur Inferenzzeit ohne erneutes Training ergänzt oder ausgetauscht werden soll, etwa zur Domänenanpassung (Khandelwal et al., 2019; Wu et al., 2022).
- Conditional Memory: als Architekturentscheidung beim Training von Modellen, um günstig Kapazität für statisches Wissen hinzuzufügen (Cheng et al., 2026).

### Stärken und Grenzen

**Stärken**
- Externe und Retrieval-Speicher erweitern, was ein Modell über sein Kontextfenster hinaus nutzen kann, und lassen sich ohne Training aktualisieren (Packer et al., 2023; Khandelwal et al., 2019).
- Explizite Lookup-Speicher fügen Kapazität bei geringem Rechenaufwand hinzu und können im günstigeren Hauptspeicher liegen (Cheng et al., 2026).
- Agentengedächtnis kann zusammenfassen und vergessen, sodass die gespeicherte Vorgeschichte relevant bleibt (Zhong et al., 2023).

**Grenzen**
- Parametrisches Gedächtnis lässt sich nur durch Training ändern (Geva et al., 2020).
- Externes Gedächtnis hängt von der Retrieval-Qualität ab: Was nicht abgerufen wird, existiert für das Modell nicht, wie bei jedem [[rag-failure-modes|RAG-Fehler]].
- Gespeicherte Gesprächsverläufe und Nutzerprofile sind in vielen Anwendungen personenbezogene Daten, was Fragen nach Löschung und Zugriff aufwirft.
- Conditional Memory wie Engram ist Teil des Pretrainings und lässt sich von Nutzenden nicht nachträglich zu einem bestehenden Modell hinzufügen (Cheng et al., 2026).

### Vergleich

| Gedächtnis | Wo | Geschrieben durch | Gelesen durch | Beispiel |
|---|---|---|---|---|
| Parametrisch | Gewichte | Training | Forward Pass | FFN-Key-Value-Speicher |
| Conditional | Embedding-Tabelle im Modell | Training | gehashter n-Gramm-Lookup | Engram |
| Retrieval im Modell | Speicher von Repräsentationen | Inferenz oder offline | kNN-Suche | kNN-LM, Memorizing Transformers |
| Arbeitsgedächtnis | Kontextfenster | Anwendung | Attention | Prompt, Verlauf |
| Extern / Memory Bank | Datenbank oder Dateien | Agent oder Anwendung | Retriever, Tool-Aufruf | MemoryBank, MemGPT |

Quellen: Geva et al. (2020); Cheng et al. (2026); Khandelwal et al. (2019); Wu et al. (2022); Zhong et al. (2023); Packer et al. (2023).

### In der Praxis

Externes Gedächtnis wird aus denselben Bausteinen gebaut wie [[rag-retrieval|RAG-Retrieval]]: Chunking der Gespräche, [[semantic-retrieval|semantisches Retrieval]] und Ranking, dazu Regeln zum Zusammenfassen und Vergessen. Was gespeichert wird, muss nachvollziehbar und löschbar sein, vor allem Nutzerprofile ([[gdpr|DSGVO]]), und Lese- und Schreibzugriffe auf das Gedächtnis werden wie jeder Tool-Aufruf protokolliert ([[llm-observability-and-tracing|LLM-Observability und Tracing]]).

### Regulatorischer Kontext

Dauerhaft gespeicherte Erinnerungen über Nutzende sind personenbezogene Daten, wenn sie sich auf identifizierbare Personen beziehen; dann gilt die [[gdpr|DSGVO]], einschließlich des Rechts auf Löschung nach Art. 17. Solche Daten in einem externen Speicher statt in Modellgewichten zu halten, macht die Löschung praktikabel.

### Merksatz

Gedächtnis in LLMs ist eine Familie von Mechanismen, von Wissen in den Gewichten und gehashten n-Gramm-Tabellen im Modell bis zu Memory Banks, die Agenten füllen, zusammenfassen und abfragen; alle sollen dem Modell mehr Wissen geben, als sein Kontextfenster fasst.

### Quellen

- Geva, M., Schuster, R., Berant, J. & Levy, O. (2020). *Transformer Feed-Forward Layers Are Key-Value Memories.* arXiv:2012.14913. [arXiv](https://arxiv.org/abs/2012.14913)
- Khandelwal, U., Levy, O., Jurafsky, D., Zettlemoyer, L. & Lewis, M. (2019). *Generalization through Memorization: Nearest Neighbor Language Models.* arXiv:1911.00172. [arXiv](https://arxiv.org/abs/1911.00172)
- Wu, Y., Rabe, M. N., Hutchins, D. & Szegedy, C. (2022). *Memorizing Transformers.* arXiv:2203.08913. [arXiv](https://arxiv.org/abs/2203.08913)
- Cheng, X., Tian, R., Zeng, W., Dai, D., Chen, Q., Wang, B. et al. (2026). *Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models.* arXiv:2601.07372. [arXiv](https://arxiv.org/abs/2601.07372)
- Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I. & Gonzalez, J. E. (2023). *MemGPT: Towards LLMs as Operating Systems.* arXiv:2310.08560. [arXiv](https://arxiv.org/abs/2310.08560)
- Zhong, W., Guo, L., Gao, Q., Ye, H. & Wang, Y. (2023). *MemoryBank: Enhancing Large Language Models with Long-Term Memory.* arXiv:2305.10250. [arXiv](https://arxiv.org/abs/2305.10250)
- Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P. & Bernstein, M. S. (2023). *Generative Agents: Interactive Simulacra of Human Behavior.* arXiv:2304.03442. [arXiv](https://arxiv.org/abs/2304.03442)
- Anthropic (2026). *Tool use with Claude.* Claude Developer Platform documentation. [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
