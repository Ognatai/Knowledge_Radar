---
title_en: Context Engineering
title_de: Context Engineering
entity_type: Method
sources:
- https://arxiv.org/abs/2507.13334
- https://arxiv.org/abs/2307.03172
- https://arxiv.org/abs/2310.05736
- https://arxiv.org/abs/2310.08560
- https://arxiv.org/abs/2005.11401
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Context engineering is the systematic optimisation of everything a language model receives at inference time, going beyond the wording of the prompt ([[prompt-engineering|Prompt Engineering]]) to cover retrieval, processing and management of context (Mei et al., 2025). Its main levers are which information enters the limited context window, where it is placed, how it is compressed and how information that does not fit is kept in external memory.

### How it works

A model sees only what is in its context window, and how well it uses that information depends on what is included, how much space it takes and where it appears. Context engineering assembles instructions, retrieved knowledge, conversation history, memory and tool results, compresses them where needed and moves information between the window and external storage.

```text
1. Components: retrieval and generation, processing, management
▼
2. Retrieval of external knowledge
▼
3. Position of relevant information
▼
4. Compression
▼
5. Memory beyond the context window
▼
6. Understanding versus generation
```

#### 1. Components of the context

Mei et al. (2025) define context engineering as a formal discipline for the systematic optimisation of the information payloads given to LLMs. Their taxonomy distinguishes three foundational components, context retrieval and generation, context processing, and context management, and shows how they are combined in system implementations such as retrieval-augmented generation, memory systems, tool-integrated reasoning and multi-agent systems.

#### 2. Retrieval of external knowledge

Retrieval adds knowledge that is not stored in the model's parameters. Lewis et al. (2020) combined a pretrained sequence-to-sequence model with a dense vector index of Wikipedia accessed through a neural retriever ([[retrieval-augmented-generation|Retrieval-Augmented Generation]]). Because the knowledge lives in the index, it can be updated without retraining, and these models set the state of the art on three open-domain question answering tasks (Lewis et al., 2020).

#### 3. Position in the context

Where relevant information appears matters. Liu et al. (2023) found in multi-document question answering and key-value retrieval that performance is often highest when the relevant information is at the beginning or end of the input and degrades significantly when it is in the middle, even for models built for long contexts. Adding more retrieved material therefore does not automatically help, and relevant content is better placed at the edges of the context.

#### 4. Compression

Compression keeps the context within budget. LLMLingua (Jiang et al., 2023) compresses prompts with a budget controller that preserves semantic integrity under high compression ratios, a token-level iterative compression algorithm that models the interdependence of the compressed content, and an instruction-tuning-based alignment of distributions between the small model used for compression and the target model. On data sets including GSM8K, BBH, ShareGPT and Arxiv-March23, it allowed up to 20x compression with little performance loss (Jiang et al., 2023).

#### 5. Memory beyond the context window

When information does not fit into the window, it can be moved to external storage. MemGPT (Packer et al., 2023) uses virtual context management inspired by the hierarchical memory of operating systems: it moves data between fast and slow memory tiers to provide the appearance of a larger context, and uses interrupts to manage control flow between itself and the user. It was evaluated on analysing documents far larger than the context window and on multi-session chat in which agents remember and adapt over long interactions (Packer et al., 2023).

#### 6. Understanding versus generation

Mei et al. (2025) identify an asymmetry as a critical research gap: current models, augmented with advanced context engineering, are remarkably good at understanding complex contexts but show pronounced limitations in generating equally sophisticated long-form outputs. Better context therefore improves comprehension more than it improves long outputs.

#### Origin and variants

Context engineering grew out of prompt engineering as LLM applications started to combine retrieved knowledge (Lewis et al., 2020), long contexts (Liu et al., 2023), compression (Jiang et al., 2023) and external memory (Packer et al., 2023). Mei et al. (2025) analysed more than 1,400 research papers to systematise the field.

### When to use it

- When an application has to bring knowledge into the model that is not in its parameters or changes over time, through retrieval (Lewis et al., 2020).
- When long inputs are used and relevant information risks being overlooked in the middle of the context (Liu et al., 2023).
- When prompts become too long or expensive and can be compressed (Jiang et al., 2023).
- When conversations or documents exceed the context window and information has to be kept in external memory (Packer et al., 2023).

### Strengths and limitations

**Strengths**
- Retrieval lets knowledge be updated without retraining the model (Lewis et al., 2020).
- Compression can shorten prompts considerably with little performance loss (Jiang et al., 2023).
- Virtual context management extends the usable context beyond the model's window (Packer et al., 2023).

**Limitations**
- Long contexts are used unevenly: information in the middle is used less well (Liu et al., 2023).
- Better context engineering improves understanding more than long-form generation (Mei et al., 2025).
- Each technique adds a component, such as a retriever, a compression model or a memory manager, that has to be built and evaluated.

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| [[prompt-engineering|Prompt Engineering]] | Designs the instructions and demonstrations in the prompt | Tasks where the needed information fits in a short prompt |
| Retrieval augmentation | Adds retrieved documents from an index (Lewis et al., 2020) | Knowledge-intensive tasks |
| Prompt compression | Removes tokens while preserving meaning (Jiang et al., 2023) | Long or costly prompts |
| Virtual context management | Moves information between the context window and external memory (Packer et al., 2023) | Long documents and multi-session conversations |

### In practice

Relevant documents are placed at the beginning or end of the context rather than in the middle, and the number of retrieved passages is limited to what the model can use (Liu et al., 2023; [[rag-chunking|RAG: Chunking]]). Long prompts can be compressed before they are sent to the model (Jiang et al., 2023), and assistants that must remember earlier sessions keep information in external memory (Packer et al., 2023). The effect of each change is measured on the target task ([[llm-evaluation|LLM Evaluation]]).

### Key takeaway

Context engineering decides what a model sees, where and in how many tokens, and these choices affect results as much as the wording of the prompt.

### Sources

- Mei, L. et al. (2025). *A Survey of Context Engineering for Large Language Models.* [arXiv:2507.13334](https://arxiv.org/abs/2507.13334)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Jiang, H. et al. (2023). *LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models.* EMNLP 2023. [arXiv:2310.05736](https://arxiv.org/abs/2310.05736)
- Packer, C. et al. (2023). *MemGPT: Towards LLMs as Operating Systems.* [arXiv:2310.08560](https://arxiv.org/abs/2310.08560)
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Context Engineering ist die systematische Optimierung aller Informationen, die ein Sprachmodell zur Inferenzzeit erhält; es geht über die Formulierung des Prompts ([[prompt-engineering|Prompt Engineering]]) hinaus und umfasst Retrieval, Verarbeitung und Verwaltung des Kontexts (Mei et al., 2025). Seine Haupthebel sind, welche Informationen in das begrenzte Kontextfenster gelangen, wo sie platziert werden, wie sie komprimiert werden und wie Informationen, die nicht passen, in externem Speicher gehalten werden.

### Funktionsweise

Ein Modell sieht nur das, was in seinem Kontextfenster enthalten ist, und wie gut es diese Informationen nutzt, hängt davon ab, was enthalten ist, wie viel Platz es einnimmt und wo es erscheint. Context Engineering stellt Anweisungen, abgerufenes Wissen, Gesprächsverlauf, Gedächtnis und Tool-Ergebnisse zusammen, komprimiert sie wo nötig und bewegt Informationen zwischen dem Fenster und dem externen Speicher.

```text
1. Komponenten: Retrieval und Generierung, Verarbeitung, Verwaltung
▼
2. Retrieval externen Wissens
▼
3. Position relevanter Informationen
▼
4. Kompression
▼
5. Gedächtnis außerhalb des Kontextfensters
▼
6. Verständnis versus Generierung
```

#### 1. Komponenten des Kontexts

Mei et al. (2025) definieren Context Engineering als formale Disziplin zur systematischen Optimierung der Informationen, die LLMs übergeben werden. Ihre Taxonomie unterscheidet drei grundlegende Komponenten, nämlich Kontext-Retrieval und -Generierung, Kontextverarbeitung und Kontextmanagement, und zeigt, wie sie in Systemen wie Retrieval-Augmented Generation, Gedächtnissystemen, werkzeuggestütztem Schließen und Multi-Agenten-Systemen kombiniert werden.

#### 2. Retrieval externen Wissens

Retrieval fügt Wissen hinzu, das nicht in den Parametern des Modells gespeichert ist. Lewis et al. (2020) kombinierten ein vortrainiertes Sequence-to-Sequence-Modell mit einem dichten Vektorindex von Wikipedia, der über einen neuronalen Retriever zugänglich ist ([[retrieval-augmented-generation|Retrieval-Augmented Generation]]). Da das Wissen im Index liegt, kann es ohne Neutraining aktualisiert werden, und diese Modelle erreichten den Stand der Technik bei drei Aufgaben des Open-Domain-Question-Answering (Lewis et al., 2020).

#### 3. Position im Kontext

Wo relevante Informationen auftauchen, spielt eine Rolle. Liu et al. (2023) fanden bei Fragebeantwortung über mehrere Dokumente und beim Abruf von Schlüssel-Wert-Paaren heraus, dass die Leistung oft am höchsten ist, wenn die relevanten Informationen am Anfang oder Ende der Eingabe stehen und deutlich abnimmt, wenn sie in der Mitte liegen, selbst bei Modellen, die für lange Kontexte entwickelt wurden. Mehr abgerufenes Material hilft daher nicht automatisch, und relevante Inhalte stehen besser an den Rändern des Kontexts.

#### 4. Kompression

Die Kompression hält den Kontext innerhalb des Budgets. LLMLingua (Jiang et al., 2023) komprimiert Prompts mit einem Budget-Controller, der die semantische Integrität unter hohen Komprimierungsverhältnissen bewahrt, einem iterativen Komprimierungsalgorithmus auf Token-Ebene, der die Abhängigkeiten des komprimierten Inhalts modelliert, und einer auf Instruction Tuning basierenden Angleichung der Verteilungen zwischen dem kleinen Modell, das für die Komprimierung verwendet wird, und dem Zielmodell. Auf Datensätzen einschließlich GSM8K, BBH, ShareGPT und Arxiv-March23 ermöglichte es bis zu 20-fache Kompression mit geringem Leistungsverlust (Jiang et al., 2023).

#### 5. Gedächtnis über das Kontextfenster hinaus

Wenn Informationen nicht in das Fenster passen, können sie in externen Speicher verschoben werden. MemGPT (Packer et al., 2023) verwendet eine virtuelle Kontextverwaltung nach dem Vorbild der Speicherhierarchie von Betriebssystemen: Es verschiebt Daten zwischen schnellen und langsamen Speicherebenen, um den Eindruck eines größeren Kontexts zu erzeugen, und nutzt Interrupts, um den Kontrollfluss zwischen sich und dem Nutzer zu steuern. Es wurde bei der Analyse von Dokumenten getestet, die weit größer als das Kontextfenster waren, und bei Chats über mehrere Sitzungen, bei denen Agenten sich über lange Interaktionen erinnern und anpassen (Packer et al., 2023).

#### 6. Verständnis versus Generierung

Mei et al. (2025) identifizieren eine Asymmetrie als kritische Forschungslücke: Aktuelle Modelle sind, unterstützt durch fortgeschrittenes Context Engineering, erstaunlich gut darin, komplexe Kontexte zu verstehen, zeigen jedoch deutliche Einschränkungen bei der Generierung ebenso anspruchsvoller langer Ausgaben. Besserer Kontext verbessert daher das Verständnis stärker als lange Ausgaben.

#### Ursprung und Varianten

Context Engineering entstand aus Prompt Engineering, als Anwendungen von LLMs begannen, abgerufenes Wissen (Lewis et al., 2020), lange Kontexte (Liu et al., 2023), Kompression (Jiang et al., 2023) und externes Gedächtnis (Packer et al., 2023) zu kombinieren. Mei et al. (2025) analysierten mehr als 1.400 Forschungsarbeiten, um den Bereich zu systematisieren.

### Wann einsetzen

- Wenn eine Anwendung Wissen in das Modell bringen muss, das nicht in seinen Parametern enthalten ist oder sich im Laufe der Zeit ändert, durch Retrieval (Lewis et al., 2020).
- Wenn lange Eingaben verwendet werden und relevante Informationen in der Mitte des Kontexts übersehen werden können (Liu et al., 2023).
- Wenn Prompts zu lang oder zu teuer werden und komprimiert werden können (Jiang et al., 2023).
- Wenn Gespräche oder Dokumente das Kontextfenster überschreiten und Informationen in externem Speicher gehalten werden müssen (Packer et al., 2023).

### Stärken und Grenzen

**Stärken**
- Retrieval ermöglicht es, Wissen ohne Neutraining des Modells zu aktualisieren (Lewis et al., 2020).
- Kompression kann Prompts erheblich kürzen, mit geringem Verlust an Leistung (Jiang et al., 2023).
- Virtuelle Kontextverwaltung erweitert den nutzbaren Kontext über das Fenster des Modells hinaus (Packer et al., 2023).

**Einschränkungen**
- Lange Kontexte werden ungleichmäßig genutzt: Informationen in der Mitte werden schlechter genutzt (Liu et al., 2023).
- Besseres Context Engineering verbessert das Verständnis stärker als die Generierung langer Texte (Mei et al., 2025).
- Jede Technik fügt eine Komponente hinzu, etwa einen Retriever, ein Kompressionsmodell oder einen Speichermanager, die gebaut und evaluiert werden muss.

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| [[prompt-engineering|Prompt Engineering]] | Gestaltet die Anweisungen und Beispiele im Prompt | Aufgaben, bei denen die benötigten Informationen in einen kurzen Prompt passen |
| Retrieval-Augmentation | Fügt abgerufene Dokumente aus einem Index hinzu (Lewis et al., 2020) | Wissensintensive Aufgaben |
| Prompt-Kompression | Entfernt Token und bewahrt dabei die Bedeutung (Jiang et al., 2023) | Lange oder teure Prompts |
| Virtuelle Kontextverwaltung | Verschiebt Informationen zwischen Kontextfenster und externem Speicher (Packer et al., 2023) | Lange Dokumente und Gespräche über mehrere Sitzungen |

### In der Praxis

Relevante Dokumente werden am Anfang oder Ende des Kontexts platziert, nicht in der Mitte, und die Anzahl der abgerufenen Passagen ist auf das begrenzt, was das Modell verwenden kann (Liu et al., 2023; [[rag-chunking|RAG: Chunking]]). Lange Prompts können vor dem Senden an das Modell komprimiert werden (Jiang et al., 2023), und Assistenten, die sich an frühere Sitzungen erinnern müssen, halten Informationen in externem Speicher (Packer et al., 2023). Der Effekt jeder Änderung wird anhand der Zielaufgabe gemessen ([[llm-evaluation|LLM Evaluation]]).

### Merksatz

Context Engineering bestimmt, was ein Modell sieht, wo und in wie vielen Token, und diese Entscheidungen beeinflussen die Ergebnisse genauso stark wie die Formulierung des Prompts.

### Quellen

- Mei, L. et al. (2025). *A Survey of Context Engineering for Large Language Models.* [arXiv:2507.13334](https://arxiv.org/abs/2507.13334)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Jiang, H. et al. (2023). *LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models.* EMNLP 2023. [arXiv:2310.05736](https://arxiv.org/abs/2310.05736)
- Packer, C. et al. (2023). *MemGPT: Towards LLMs as Operating Systems.* [arXiv:2310.08560](https://arxiv.org/abs/2310.08560)
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
