---
title_en: MemGPT
title_de: MemGPT
entity_type: Method
aliases:
- MemGPT
- MemoryGPT
- Virtual context management
sources:
- https://arxiv.org/abs/2310.08560
- https://arxiv.org/abs/2307.03172
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

MemGPT gives a language model with a fixed context window the illusion of a much larger memory by borrowing ideas from operating systems: the prompt acts as main memory, external databases act as disk, and the model itself moves information between them through function calls (Packer et al., 2023). A queue manager warns the model when the context fills up, evicts old messages into a searchable recall store with a recursive summary, and an archival store holds documents of any length (Packer et al., 2023). In multi-session chat, MemGPT raised GPT-4's accuracy in answering questions about earlier conversations from 32.1% to 92.5%, and in document analysis its accuracy did not drop as more documents were retrieved, while fixed-context models had to truncate (Packer et al., 2023). It is one of the main designs for [[memory-in-llms|memory in LLM agents]].

### How it works

```text
            ┌──────────── main context (prompt tokens) ────────────┐
            │ system instructions │ working context │ FIFO queue    │
            └──────────────────────────────────────────────────────┘
events ──► queue manager ──► LLM processor ──► function executor
 (user msg, system alert,     (completion tokens      │
  timer)                       = function calls)       ▼
            ◄──── recall storage (all messages)  · archival storage (any text, vector search)
```

#### 1. Main context: what the model sees

The prompt is split into three parts: read-only system instructions describing the control flow, the memory levels and how to use the MemGPT functions; a fixed-size, read-write working context of unstructured text, writable only through function calls, which in chat stores key facts and preferences about the user and the persona the agent adopts; and a first-in-first-out queue with the rolling history of messages, system messages such as memory warnings and the inputs and outputs of function calls (Packer et al., 2023). The first entry of the queue is a recursive summary of messages already evicted (Packer et al., 2023).

#### 2. External context: recall and archival storage

Everything outside the context window is external context, which the model cannot see directly and must bring into main context by function calls (Packer et al., 2023). Recall storage is the message database: the queue manager writes every incoming message and every model output to it, and messages retrieved by a function call are appended to the queue again (Packer et al., 2023). Archival storage is a read-write database for text objects of any length; in the experiments it was PostgreSQL with the pgvector extension and an [[hnsw|HNSW]] index for approximate vector search over [[embeddings|embeddings]] (Packer et al., 2023), the same building blocks as in [[vector-databases|vector databases]].

#### 3. Queue manager and memory pressure

When the prompt exceeds a warning threshold, for example 70% of the context window, the queue manager inserts a "memory pressure" warning so that the model can save important information from the queue into working context or archival storage (Packer et al., 2023). When the prompt reaches the flush threshold, for example 100%, the queue manager evicts a share of the messages, for example 50% of the context window, and writes a new recursive summary from the old summary and the evicted messages; the evicted messages remain readable in recall storage (Packer et al., 2023). Retrieval calls are paginated so that results do not overflow the context window (Packer et al., 2023).

#### 4. Function executor and control flow

The model's output is interpreted as function calls, which the function executor runs to move data between main and external context ([[tool-calling|tool calling]]; Packer et al., 2023). By setting the argument `request_heartbeat=true`, the model asks for another inference step immediately, which lets it chain calls, for example several searches in a row, before answering (Packer et al., 2023). Inference is triggered by events: user messages, system messages such as capacity warnings, user interactions such as a finished upload, and timed events that let MemGPT run without user input (Packer et al., 2023).

#### 5. Results in conversation

On a "deep memory retrieval" task built from the Multi-Session Chat dataset, the agent had to answer a question that refers to earlier sessions; the baselines saw a lossy summary of the past five conversations, while MemGPT had the full history but had to search it (Packer et al., 2023). Accuracy rose from 38.7% to 66.9% with GPT-3.5 Turbo, from 32.1% to 92.5% with GPT-4 and from 35.3% to 93.4% with GPT-4 Turbo, judged by an LLM and by ROUGE-L recall (Packer et al., 2023). Conversation openers written from working context were similar to, and sometimes better than, human-written openers (Packer et al., 2023).

#### 6. Results in document analysis

In multi-document question answering on NaturalQuestions-Open, following the retriever-reader setup of Liu et al. (2023), fixed-context baselines had to truncate retrieved documents to fit, which reduced accuracy as more documents were retrieved, whereas MemGPT, which loaded all documents into archival storage and searched them, was unaffected by the number of documents (Packer et al., 2023). Liu et al. (2023) had shown that models use information in long contexts unevenly, which is one reason to page context in and out instead of filling it ([[structured-context-construction|structured context construction]]). In a nested key-value task with 140 UUID pairs, GPT-3.5 fell to 0% accuracy at one nesting level and GPT-4 and GPT-4 Turbo at three, while MemGPT with GPT-4 was unaffected by nesting depth; MemGPT performed worst with GPT-3.5 because of its weaker function calling (Packer et al., 2023).

#### Origin and variants

MemGPT was introduced by Packer et al. (2023) at the University of California, Berkeley, with code and data released. Its idea of self-editing memory through function calls reappears in agent frameworks that ship memory and session state as a building block ([[agent-frameworks|agent frameworks]]); other approaches to long-term memory, such as MemoryBank with a forgetting curve, are compared in [[memory-in-llms|memory in LLMs]].

### When to use it

- For conversational agents that must stay consistent over many sessions, such as assistants or companions (Packer et al., 2023).
- For analysing document collections much larger than the context window (Packer et al., 2023).
- When the base model is good at function calling, since MemGPT relies on it (Packer et al., 2023).

### Strengths and limitations

**Strengths**
- Large gains on questions about earlier conversations compared with summary-only baselines (Packer et al., 2023).
- Performance does not degrade with the number of documents or with nested lookups (Packer et al., 2023).
- Memory is explicit and inspectable: working context, recall and archival storage can be read and edited.

**Limitations**
- Depends on the model's function-calling ability; with GPT-3.5 document analysis degraded significantly (Packer et al., 2023).
- Every memory operation is an extra model call, which adds latency and cost ([[llm-cost-optimisation|LLM cost optimisation]]).
- Retrieval from archival storage inherits the failure modes of retrieval, such as missing the relevant passage ([[rag-failure-modes|RAG failure modes]]).

### Comparison

| Approach | How more context is used | Who decides what is in context | Example |
|---|---|---|---|
| Long context window | everything in the prompt | the application | GPT-4 Turbo with 128k tokens |
| Truncation / summary | compress or cut history | fixed rule | recursive summary baseline |
| [[retrieval-augmented-generation\|RAG]] | retrieve before the call | retrieval pipeline | top-k documents |
| MemGPT | page in and out via function calls | the model itself | recall and archival storage |
| Memory with forgetting | store, summarise, fade | updater rules | MemoryBank |

Sources: Packer et al. (2023); Liu et al. (2023).

### In practice

The thresholds (warning at 70%, flush at 100%, evict 50%) are configurable examples from the paper and can be tuned to the model's context length (Packer et al., 2023). Memory writes and reads should be logged like other tool calls ([[llm-observability-and-tracing|LLM observability and tracing]]), and personal data in working context or recall storage needs deletion and access rules ([[gdpr|GDPR]]). Choosing what stays in the prompt is part of [[context-engineering|context engineering]].

### Key takeaway

MemGPT treats the context window like main memory and lets the model page information in and out of external storage through function calls, which keeps long conversations and large document sets usable within a fixed window.

### Sources

- Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I. & Gonzalez, J. E. (2023). *MemGPT: Towards LLMs as Operating Systems.* arXiv:2310.08560. [arXiv](https://arxiv.org/abs/2310.08560)
- Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F. & Liang, P. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* arXiv:2307.03172. [arXiv](https://arxiv.org/abs/2307.03172)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

MemGPT verschafft einem Sprachmodell mit festem Kontextfenster den Eindruck eines viel größeren Speichers, indem es Ideen aus Betriebssystemen übernimmt: Der Prompt dient als Hauptspeicher, externe Datenbanken dienen als Festplatte, und das Modell verschiebt Informationen selbst per Funktionsaufruf zwischen beiden (Packer et al., 2023). Ein Queue Manager warnt das Modell, wenn sich der Kontext füllt, verdrängt alte Nachrichten mit einer rekursiven Zusammenfassung in einen durchsuchbaren Recall-Speicher, und ein Archivspeicher nimmt Dokumente beliebiger Länge auf (Packer et al., 2023). In Chats über mehrere Sitzungen steigerte MemGPT die Genauigkeit von GPT-4 bei Fragen zu früheren Gesprächen von 32,1 % auf 92,5 %, und in der Dokumentanalyse sank seine Genauigkeit nicht, wenn mehr Dokumente abgerufen wurden, während Modelle mit festem Kontext kürzen mussten (Packer et al., 2023). Es ist einer der wichtigsten Entwürfe für [[memory-in-llms|Gedächtnis in LLM-Agenten]].

### Funktionsweise

```text
            ┌──────────── Main Context (Prompt-Tokens) ────────────┐
            │ Systemanweisungen │ Working Context │ FIFO-Queue      │
            └──────────────────────────────────────────────────────┘
Ereignisse ──► Queue Manager ──► LLM-Prozessor ──► Function Executor
 (Nachricht, System-          (Completion-Tokens       │
  hinweis, Timer)              = Funktionsaufrufe)      ▼
            ◄──── Recall Storage (alle Nachrichten) · Archival Storage (beliebiger Text, Vektorsuche)
```

#### 1. Main Context: was das Modell sieht

Der Prompt besteht aus drei Teilen: schreibgeschützten Systemanweisungen, die den Ablauf, die Speicherebenen und die Nutzung der MemGPT-Funktionen beschreiben; einem Working Context fester Größe aus unstrukturiertem Text, lesbar und nur per Funktionsaufruf beschreibbar, der im Chat wichtige Fakten und Vorlieben der Nutzenden sowie die vom Agenten eingenommene Persona festhält; und einer First-in-first-out-Warteschlange mit dem fortlaufenden Nachrichtenverlauf, Systemnachrichten wie Speicherwarnungen sowie Ein- und Ausgaben von Funktionsaufrufen (Packer et al., 2023). Der erste Eintrag der Warteschlange ist eine rekursive Zusammenfassung der bereits verdrängten Nachrichten (Packer et al., 2023).

#### 2. External Context: Recall und Archival Storage

Alles außerhalb des Kontextfensters ist External Context, den das Modell nicht direkt sieht und per Funktionsaufruf in den Main Context holen muss (Packer et al., 2023). Recall Storage ist die Nachrichtendatenbank: Der Queue Manager schreibt jede eingehende Nachricht und jede Modellausgabe hinein, und per Funktionsaufruf abgerufene Nachrichten werden wieder an die Warteschlange angehängt (Packer et al., 2023). Archival Storage ist eine les- und beschreibbare Datenbank für Textobjekte beliebiger Länge; in den Experimenten war das PostgreSQL mit der Erweiterung pgvector und einem [[hnsw|HNSW]]-Index für approximative Vektorsuche über [[embeddings|Embeddings]] (Packer et al., 2023), dieselben Bausteine wie in [[vector-databases|Vektordatenbanken]].

#### 3. Queue Manager und Memory Pressure

Überschreitet der Prompt eine Warnschwelle, etwa 70 % des Kontextfensters, fügt der Queue Manager eine „Memory Pressure“-Warnung ein, damit das Modell wichtige Informationen aus der Warteschlange in den Working Context oder den Archivspeicher sichern kann (Packer et al., 2023). Erreicht der Prompt die Flush-Schwelle, etwa 100 %, verdrängt der Queue Manager einen Teil der Nachrichten, etwa 50 % des Kontextfensters, und schreibt aus der alten Zusammenfassung und den verdrängten Nachrichten eine neue rekursive Zusammenfassung; die verdrängten Nachrichten bleiben im Recall Storage lesbar (Packer et al., 2023). Abrufe werden seitenweise geliefert, damit die Ergebnisse das Kontextfenster nicht sprengen (Packer et al., 2023).

#### 4. Function Executor und Ablaufsteuerung

Die Ausgabe des Modells wird als Funktionsaufruf interpretiert, den der Function Executor ausführt, um Daten zwischen Main und External Context zu verschieben ([[tool-calling|Tool Calling]]; Packer et al., 2023). Mit dem Argument `request_heartbeat=true` fordert das Modell sofort einen weiteren Inferenzschritt an und kann so Aufrufe verketten, etwa mehrere Suchen hintereinander, bevor es antwortet (Packer et al., 2023). Inferenz wird durch Ereignisse ausgelöst: Nachrichten der Nutzenden, Systemnachrichten wie Kapazitätswarnungen, Interaktionen wie ein abgeschlossener Upload und zeitgesteuerte Ereignisse, mit denen MemGPT auch ohne Eingabe der Nutzenden läuft (Packer et al., 2023).

#### 5. Ergebnisse im Gespräch

In einer „Deep Memory Retrieval“-Aufgabe auf Basis des Datensatzes Multi-Session Chat musste der Agent eine Frage beantworten, die sich auf frühere Sitzungen bezieht; die Vergleichsmodelle sahen eine verlustbehaftete Zusammenfassung der letzten fünf Gespräche, MemGPT hatte den gesamten Verlauf, musste ihn aber durchsuchen (Packer et al., 2023). Die Genauigkeit stieg mit GPT-3.5 Turbo von 38,7 % auf 66,9 %, mit GPT-4 von 32,1 % auf 92,5 % und mit GPT-4 Turbo von 35,3 % auf 93,4 %, bewertet von einem LLM und mit ROUGE-L-Recall (Packer et al., 2023). Gesprächseröffnungen, die aus dem Working Context geschrieben wurden, waren ähnlich gut wie von Menschen geschriebene und manchmal besser (Packer et al., 2023).

#### 6. Ergebnisse in der Dokumentanalyse

Bei der Fragebeantwortung über mehrere Dokumente auf NaturalQuestions-Open, im Retriever-Reader-Aufbau von Liu et al. (2023), mussten Modelle mit festem Kontext die abgerufenen Dokumente kürzen, was die Genauigkeit mit mehr Dokumenten senkte, während MemGPT, das alle Dokumente in den Archivspeicher lud und durchsuchte, von der Zahl der Dokumente unberührt blieb (Packer et al., 2023). Liu et al. (2023) hatten gezeigt, dass Modelle Informationen in langen Kontexten ungleichmäßig nutzen; das ist ein Grund, Kontext ein- und auszulagern, statt ihn aufzufüllen ([[structured-context-construction|strukturierter Kontextaufbau]]). In einer verschachtelten Key-Value-Aufgabe mit 140 UUID-Paaren fiel GPT-3.5 schon bei einer Verschachtelungsebene auf 0 % Genauigkeit, GPT-4 und GPT-4 Turbo bei drei, während MemGPT mit GPT-4 von der Verschachtelungstiefe unberührt blieb; am schlechtesten schnitt MemGPT mit GPT-3.5 ab, wegen dessen schwächeren Function Calling (Packer et al., 2023).

#### Herkunft und Varianten

MemGPT wurde von Packer et al. (2023) an der University of California, Berkeley, eingeführt; Code und Daten sind veröffentlicht. Die Idee eines selbst bearbeiteten Gedächtnisses per Funktionsaufruf findet sich in Agent-Frameworks wieder, die Gedächtnis und Sitzungszustand als Baustein mitliefern ([[agent-frameworks|Agent-Frameworks]]); andere Ansätze für Langzeitgedächtnis, etwa MemoryBank mit Vergessenskurve, vergleicht [[memory-in-llms|Gedächtnis in LLMs]].

### Wann einsetzen

- Für Dialogagenten, die über viele Sitzungen konsistent bleiben müssen, etwa Assistenten oder Companions (Packer et al., 2023).
- Für die Analyse von Dokumentsammlungen, die weit größer sind als das Kontextfenster (Packer et al., 2023).
- Wenn das Basismodell Function Calling gut beherrscht, da MemGPT darauf angewiesen ist (Packer et al., 2023).

### Stärken und Grenzen

**Stärken**
- Große Verbesserungen bei Fragen zu früheren Gesprächen gegenüber Vergleichsmodellen mit bloßer Zusammenfassung (Packer et al., 2023).
- Die Leistung sinkt weder mit der Zahl der Dokumente noch bei verschachtelten Lookups (Packer et al., 2023).
- Das Gedächtnis ist explizit und prüfbar: Working Context, Recall und Archival Storage lassen sich lesen und bearbeiten.

**Grenzen**
- Hängt von der Function-Calling-Fähigkeit des Modells ab; mit GPT-3.5 verschlechterte sich die Dokumentanalyse deutlich (Packer et al., 2023).
- Jede Speicheroperation ist ein zusätzlicher Modellaufruf, was Latenz und Kosten erhöht ([[llm-cost-optimisation|LLM-Kostenoptimierung]]).
- Abrufe aus dem Archivspeicher erben die Fehlerarten des Retrievals, etwa dass die relevante Stelle fehlt ([[rag-failure-modes|RAG: Fehlerarten]]).

### Vergleich

| Ansatz | Wie mehr Kontext genutzt wird | Wer entscheidet, was im Kontext steht | Beispiel |
|---|---|---|---|
| Langes Kontextfenster | alles im Prompt | die Anwendung | GPT-4 Turbo mit 128.000 Tokens |
| Kürzen / Zusammenfassen | Verlauf komprimieren oder abschneiden | feste Regel | Vergleichsmodell mit rekursiver Zusammenfassung |
| [[retrieval-augmented-generation\|RAG]] | vor dem Aufruf abrufen | Retrieval-Pipeline | Top-k-Dokumente |
| MemGPT | per Funktionsaufruf ein- und auslagern | das Modell selbst | Recall und Archival Storage |
| Gedächtnis mit Vergessen | speichern, zusammenfassen, verblassen lassen | Regeln des Updaters | MemoryBank |

Quellen: Packer et al. (2023); Liu et al. (2023).

### In der Praxis

Die Schwellen (Warnung bei 70 %, Flush bei 100 %, Verdrängen von 50 %) sind einstellbare Beispiele aus dem Papier und lassen sich an die Kontextlänge des Modells anpassen (Packer et al., 2023). Lese- und Schreibzugriffe auf das Gedächtnis sollten wie andere Tool-Aufrufe protokolliert werden ([[llm-observability-and-tracing|LLM-Observability und Tracing]]), und personenbezogene Daten im Working Context oder Recall Storage brauchen Regeln für Löschung und Zugriff ([[gdpr|DSGVO]]). Was im Prompt bleibt, ist Teil des [[context-engineering|Context Engineering]].

### Merksatz

MemGPT behandelt das Kontextfenster wie einen Hauptspeicher und lässt das Modell Informationen per Funktionsaufruf in externe Speicher aus- und wieder einlagern; so bleiben lange Gespräche und große Dokumentsammlungen in einem festen Fenster nutzbar.

### Quellen

- Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I. & Gonzalez, J. E. (2023). *MemGPT: Towards LLMs as Operating Systems.* arXiv:2310.08560. [arXiv](https://arxiv.org/abs/2310.08560)
- Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F. & Liang, P. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* arXiv:2307.03172. [arXiv](https://arxiv.org/abs/2307.03172)
