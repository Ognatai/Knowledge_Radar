---
title_en: Structured Context Construction
title_de: Strukturierte Kontextbildung
entity_type: Method
sources:
- https://arxiv.org/abs/2307.03172
- https://arxiv.org/abs/2310.11324
- https://arxiv.org/abs/2305.13062
- https://arxiv.org/abs/2401.18059
- https://arxiv.org/abs/2404.16130
- https://arxiv.org/abs/2005.11401
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Structured context construction means arranging retrieved information in the prompt deliberately, with clear sections, metadata, ordering and suitable formats, instead of concatenating text chunks (Lewis et al., 2020). It matters because language models use long contexts unevenly and do best with relevant information at the beginning or end (Liu et al., 2023), react strongly to formatting choices (Sclar et al., 2023; Sui et al., 2023), and answer broad questions better from hierarchical summaries than from isolated chunks (Sarthi et al., 2024; Edge et al., 2024).

### How it works

Retrieved passages, records and summaries are selected, deduplicated and ordered by relevance, labelled with their source and key attributes, and rendered in a consistent format such as headed sections, tables or key-value lists before the question is added.

```text
1. Flat versus structured context
▼
2. Position in the context
▼
3. Formatting choices
▼
4. Structured data in the prompt
▼
5. Hierarchical and graph-based context
```

#### 1. Flat versus structured context

A RAG model conditions its generation on retrieved passages (Lewis et al., 2020; [[retrieval-augmented-generation|Retrieval-Augmented Generation]]). In the simplest form, chunks are pasted one after another without labels; structured context adds boundaries, source references, dates or document types and a deliberate order, so the model can tell passages apart and cite them ([[context-engineering|Context Engineering]]).

#### 2. Position in the context

Liu et al. (2023) found that performance on multi-document question answering and key-value retrieval was often highest when the relevant information was at the beginning or end of the input, and degraded significantly when it was in the middle of a long context, even for explicitly long-context models. Placing the most relevant passages first or last and keeping the context short therefore helps.

#### 3. Formatting choices

Meaning-preserving formatting choices can change results substantially: in few-shot settings, performance of LLaMA-2-13B differed by up to 76 accuracy points across prompt formats, and the sensitivity persisted with larger models, more examples and instruction tuning (Sclar et al., 2023; [[prompt-comparison|Prompt Comparison]]). A consistent format should therefore be chosen and tested rather than assumed to be neutral.

#### 4. Structured data in the prompt

Tables and records can be serialised into the prompt, but how well LLMs understand them depends on the input choices. In a benchmark of structural understanding tasks such as cell lookup and row retrieval, GPT-3.5 and GPT-4 performed differently depending on table format, content order, role prompting and partition marks; structural prompting combined with careful input choices improved results on several table tasks (Sui et al., 2023).

#### 5. Hierarchical and graph-based context

Retrieving only short contiguous chunks limits understanding of the overall document. RAPTOR recursively embeds, clusters and summarises chunks into a tree with different levels of abstraction and retrieves from it; with GPT-4, this improved the best performance on the QuALITY benchmark by 20% in absolute accuracy (Sarthi et al., 2024). GraphRAG similarly provides community summaries of an entity graph as context for global questions about a corpus (Edge et al., 2024; [[graphrag|GraphRAG]]).

#### Origin and variants

RAG (Lewis et al., 2020) introduced conditioning generation on retrieved passages. The findings on position (Liu et al., 2023), formatting (Sclar et al., 2023) and tables (Sui et al., 2023) showed that the form of the context matters, and RAPTOR (Sarthi et al., 2024) and GraphRAG (Edge et al., 2024) provide structured, multi-level context.

### When to use it

- When the prompt combines many retrieved passages from different sources (Liu et al., 2023).
- When context includes tables or records, such as contract attributes or metadata (Sui et al., 2023).
- When questions require an overview of long documents or a whole corpus (Sarthi et al., 2024; Edge et al., 2024).

### Strengths and limitations

**Strengths**
- Placing relevant information at the edges counters the lost-in-the-middle effect (Liu et al., 2023).
- Source labels make answers traceable and citable (Lewis et al., 2020).
- Hierarchical summaries support questions that need information across a long document (Sarthi et al., 2024).

**Limitations**
- Models remain sensitive to formatting, so the best format must be tested per model (Sclar et al., 2023).
- Table understanding varies with the chosen input format (Sui et al., 2023).
- Building summaries or graphs adds indexing cost (Edge et al., 2024).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Flat chunk concatenation | Passages pasted without structure (Lewis et al., 2020) | Short contexts with few passages |
| Ordered, labelled sections | Relevance order, source and metadata per passage (Liu et al., 2023) | Most RAG prompts |
| Serialised tables | Structured records in a chosen table format (Sui et al., 2023) | Attribute and record data |
| Hierarchical summaries | Tree of summaries at several levels (Sarthi et al., 2024) | Long documents, overview questions |

### In practice

A context template typically states the task, then lists each passage with an identifier, source and date, ordered by relevance, before the question, and the format is evaluated on test questions like any other prompt change (Sclar et al., 2023; [[rag-generation-evaluation|RAG: Generation Evaluation]]). Removing duplicates and irrelevant passages keeps the context short (Liu et al., 2023).

### Key takeaway

How retrieved information is ordered and formatted in the prompt affects answers as much as what is retrieved, so the context should be structured and tested deliberately.

### Sources

- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL 2024. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Sclar, M. et al. (2023). *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting.* ICLR 2024. [arXiv:2310.11324](https://arxiv.org/abs/2310.11324)
- Sui, Y. et al. (2023). *Table Meets LLM: Can Large Language Models Understand Structured Table Data? A Benchmark and Empirical Study.* WSDM 2024. [arXiv:2305.13062](https://arxiv.org/abs/2305.13062)
- Sarthi, P. et al. (2024). *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval.* ICLR 2024. [arXiv:2401.18059](https://arxiv.org/abs/2401.18059)
- Edge, D. et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Strukturierte Kontextbildung bedeutet, abgerufene Information gezielt im Prompt anzuordnen, mit klaren Abschnitten, Metadaten, Reihenfolge und passenden Formaten, statt Textabschnitte einfach aneinanderzuhängen (Lewis et al., 2020). Das ist wichtig, weil Sprachmodelle lange Kontexte ungleichmäßig nutzen und am besten abschneiden, wenn relevante Information am Anfang oder Ende steht (Liu et al., 2023), stark auf Formatierungsentscheidungen reagieren (Sclar et al., 2023; Sui et al., 2023) und breite Fragen besser aus hierarchischen Zusammenfassungen beantworten als aus isolierten Abschnitten (Sarthi et al., 2024; Edge et al., 2024).

### Funktionsweise

Abgerufene Passagen, Datensätze und Zusammenfassungen werden ausgewählt, von Dubletten befreit und nach Relevanz geordnet, mit ihrer Quelle und wichtigen Attributen gekennzeichnet und in einem einheitlichen Format wie Abschnitten mit Überschriften, Tabellen oder Schlüssel-Wert-Listen dargestellt, bevor die Frage angefügt wird.

```text
1. Flacher und strukturierter Kontext
▼
2. Position im Kontext
▼
3. Formatierungsentscheidungen
▼
4. Strukturierte Daten im Prompt
▼
5. Hierarchischer und graphbasierter Kontext
```

#### 1. Flacher und strukturierter Kontext

Ein RAG-Modell bedingt seine Generierung auf abgerufene Passagen (Lewis et al., 2020; [[retrieval-augmented-generation|Retrieval-Augmented Generation]]). In der einfachsten Form werden Abschnitte ohne Kennzeichnung hintereinander eingefügt; strukturierter Kontext ergänzt Grenzen, Quellenangaben, Daten oder Dokumenttypen und eine bewusste Reihenfolge, sodass das Modell die Passagen unterscheiden und zitieren kann ([[context-engineering|Context Engineering]]).

#### 2. Position im Kontext

Liu et al. (2023) fanden, dass die Leistung bei Fragebeantwortung über mehrere Dokumente und beim Abruf von Schlüssel-Wert-Paaren oft am höchsten war, wenn die relevante Information am Anfang oder Ende der Eingabe stand, und deutlich sank, wenn sie in der Mitte eines langen Kontexts lag, selbst bei ausdrücklich auf lange Kontexte ausgelegten Modellen. Die relevantesten Passagen an den Anfang oder das Ende zu stellen und den Kontext kurz zu halten hilft daher.

#### 3. Formatierungsentscheidungen

Bedeutungserhaltende Formatierungsentscheidungen können Ergebnisse erheblich verändern: Bei Few-Shot-Aufgaben unterschied sich die Leistung von LLaMA-2-13B je nach Prompt-Format um bis zu 76 Prozentpunkte, und die Empfindlichkeit blieb bei größeren Modellen, mehr Beispielen und Instruction Tuning bestehen (Sclar et al., 2023; [[prompt-comparison|Prompt-Vergleiche]]). Ein einheitliches Format sollte daher gewählt und getestet werden, statt es für neutral zu halten.

#### 4. Strukturierte Daten im Prompt

Tabellen und Datensätze lassen sich in den Prompt serialisieren, doch wie gut LLMs sie verstehen, hängt von den Eingabeentscheidungen ab. In einem Benchmark mit Aufgaben zum Strukturverständnis wie dem Nachschlagen von Zellen und dem Abrufen von Zeilen schnitten GPT-3.5 und GPT-4 je nach Tabellenformat, Reihenfolge der Inhalte, Rollenvorgabe und Trennzeichen unterschiedlich ab; strukturelles Prompting zusammen mit sorgfältig gewählten Eingaben verbesserte die Ergebnisse bei mehreren Tabellenaufgaben (Sui et al., 2023).

#### 5. Hierarchischer und graphbasierter Kontext

Nur kurze zusammenhängende Abschnitte abzurufen begrenzt das Verständnis des gesamten Dokuments. RAPTOR bettet Abschnitte rekursiv ein, clustert und fasst sie zu einem Baum mit verschiedenen Abstraktionsebenen zusammen und ruft daraus ab; mit GPT-4 verbesserte das die beste Leistung auf dem QuALITY-Benchmark um 20 Prozentpunkte (Sarthi et al., 2024). GraphRAG liefert ähnlich Gemeinschaftszusammenfassungen eines Entitätengraphen als Kontext für globale Fragen an ein Korpus (Edge et al., 2024; [[graphrag|GraphRAG]]).

#### Ursprung und Varianten

RAG (Lewis et al., 2020) führte die Generierung auf Basis abgerufener Passagen ein. Die Befunde zu Position (Liu et al., 2023), Formatierung (Sclar et al., 2023) und Tabellen (Sui et al., 2023) zeigten, dass die Form des Kontexts zählt, und RAPTOR (Sarthi et al., 2024) sowie GraphRAG (Edge et al., 2024) liefern strukturierten Kontext auf mehreren Ebenen.

### Wann einsetzen

- Wenn der Prompt viele abgerufene Passagen aus verschiedenen Quellen verbindet (Liu et al., 2023).
- Wenn der Kontext Tabellen oder Datensätze enthält, etwa Vertragsattribute oder Metadaten (Sui et al., 2023).
- Wenn Fragen einen Überblick über lange Dokumente oder ein ganzes Korpus erfordern (Sarthi et al., 2024; Edge et al., 2024).

### Stärken und Grenzen

**Stärken**
- Relevante Information an den Rändern wirkt dem Lost-in-the-Middle-Effekt entgegen (Liu et al., 2023).
- Quellenkennzeichnungen machen Antworten nachvollziehbar und zitierbar (Lewis et al., 2020).
- Hierarchische Zusammenfassungen unterstützen Fragen, die Information aus einem ganzen langen Dokument brauchen (Sarthi et al., 2024).

**Einschränkungen**
- Modelle bleiben formatempfindlich; das beste Format muss je Modell getestet werden (Sclar et al., 2023).
- Das Tabellenverständnis schwankt mit dem gewählten Eingabeformat (Sui et al., 2023).
- Zusammenfassungen oder Graphen aufzubauen erhöht den Indexierungsaufwand (Edge et al., 2024).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Flaches Aneinanderhängen von Abschnitten | Passagen ohne Struktur eingefügt (Lewis et al., 2020) | Kurze Kontexte mit wenigen Passagen |
| Geordnete, gekennzeichnete Abschnitte | Relevanzreihenfolge, Quelle und Metadaten je Passage (Liu et al., 2023) | Die meisten RAG-Prompts |
| Serialisierte Tabellen | Strukturierte Datensätze in einem gewählten Tabellenformat (Sui et al., 2023) | Attribut- und Datensatzdaten |
| Hierarchische Zusammenfassungen | Baum von Zusammenfassungen auf mehreren Ebenen (Sarthi et al., 2024) | Lange Dokumente, Überblicksfragen |

### In der Praxis

Eine Kontextvorlage nennt meist zuerst die Aufgabe, listet dann jede Passage mit Kennung, Quelle und Datum nach Relevanz geordnet auf und stellt die Frage ans Ende; das Format wird wie jede andere Prompt-Änderung an Testfragen evaluiert (Sclar et al., 2023; [[rag-generation-evaluation|RAG: Evaluation der Generierung]]). Dubletten und irrelevante Passagen zu entfernen hält den Kontext kurz (Liu et al., 2023).

### Merksatz

Wie abgerufene Information im Prompt geordnet und formatiert wird, beeinflusst die Antworten ebenso sehr wie das, was abgerufen wird; der Kontext sollte daher bewusst strukturiert und getestet werden.

### Quellen

- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL 2024. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Sclar, M. et al. (2023). *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting.* ICLR 2024. [arXiv:2310.11324](https://arxiv.org/abs/2310.11324)
- Sui, Y. et al. (2023). *Table Meets LLM: Can Large Language Models Understand Structured Table Data? A Benchmark and Empirical Study.* WSDM 2024. [arXiv:2305.13062](https://arxiv.org/abs/2305.13062)
- Sarthi, P. et al. (2024). *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval.* ICLR 2024. [arXiv:2401.18059](https://arxiv.org/abs/2401.18059)
- Edge, D. et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
