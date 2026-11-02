---
title_en: Context Window
title_de: Kontextfenster
entity_type: Concept
aliases:
- Context window
- Context length
- Context size
- Long context
- Long-context language models
- Kontextfenster
sources:
- https://web.stanford.edu/~jurafsky/slp3/7.pdf
- https://arxiv.org/abs/2104.09864
- https://arxiv.org/abs/2108.12409
- https://arxiv.org/abs/2306.15595
- https://arxiv.org/abs/2309.00071
- https://arxiv.org/abs/2307.03172
- https://arxiv.org/abs/2404.06654
- https://arxiv.org/abs/2205.14135
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

The context window is the span of tokens a Transformer language model can attend to at once: prompt, retrieved documents, conversation history and the output generated so far all have to fit into it (Jurafsky & Martin, 2026). Its length is fixed by training and by the position encoding, and attention cost grows quadratically with it (Jurafsky & Martin, 2026; Dao et al., 2022). Methods such as RoPE scaling (Position Interpolation, YaRN) extend windows to tens or hundreds of thousands of tokens, but models do not use long contexts uniformly: information in the middle is used worse than at the beginning or end (Liu et al., 2023), and the effective length is often far below the advertised one (Hsieh et al., 2024).

### How it works

```text
system prompt + instructions + retrieved passages + history + user turn  ──►  tokens 1 … N   (N ≤ window size)
                                                                                 │
          token embedding + position information (learned / sinusoidal / RoPE / ALiBi)
                                                                                 ▼
          causal self-attention: each token attends to all earlier tokens  →  N × N score matrix (quadratic)
                                                                                 ▼
          generation: one new token per step; keys/values of earlier tokens kept in the KV cache
                                                                                 ▼
          when N would exceed the window: truncate, summarise, retrieve selectively, or use a longer-context model
```

#### 1. What the window contains

In a causal language model, the representation of token i is computed from token i and all earlier tokens in the context window, which spans thousands of tokens or more (Jurafsky & Martin, 2026). Everything the model is to use at inference time, the prompt, few-shot examples, retrieved passages in [[retrieval-augmented-generation|RAG]] and earlier turns of a conversation, competes for the same window; how it is filled is the subject of [[context-engineering|context engineering]]. Large models are pre-trained by filling the full window with text, packing several shorter documents with end-of-text tokens in between (Jurafsky & Martin, 2026).

#### 2. Why the window has a limit: attention cost

Self-attention computes a dot product between every pair of positions, so the score matrix is N × N and attention is quadratic in the input length (Jurafsky & Martin, 2026; [[attention-and-transformers|attention]]). Time and memory complexity of self-attention are quadratic in sequence length, which makes Transformers slow and memory-hungry on long sequences; FlashAttention computes exact attention with fewer reads and writes to GPU high-bandwidth memory and made longer contexts practical, for example a 3× speed-up on GPT-2 with sequence length 1K (Dao et al., 2022). During generation, the keys and values of earlier tokens are stored in a KV cache instead of being recomputed, so memory also grows with the context length (Jurafsky & Martin, 2026).

#### 3. Position information

Transformers need position information added to the token embeddings. Learned absolute position embeddings see few training examples for the last positions, which may then generalise poorly; sinusoidal embeddings use a fixed function of the position (Jurafsky & Martin, 2026). Rotary Position Embedding (RoPE) encodes absolute position with a rotation matrix while making attention depend on relative position, and has become the most popular method (Su et al., 2024; Jurafsky & Martin, 2026). ALiBi adds no position embeddings but penalises attention scores in proportion to the query–key distance; a 1.3-billion-parameter model trained on 1,024 tokens extrapolated to 2,048 with the same perplexity as a sinusoidal model trained on 2,048, while training 11% faster (Press et al., 2022).

#### 4. Extending the window

RoPE-based models fail to generalise beyond the sequence length they were trained on (Peng et al., 2024). Position Interpolation linearly scales down the position indices to fit into the original window instead of extrapolating, which could produce catastrophically high attention scores; it extended LLaMA models from 2,048 to up to 32,768 tokens within 1,000 fine-tuning steps, while plain fine-tuning on longer inputs only moved the effective window from 2,048 to 2,560 after more than 10,000 batches (Chen et al., 2023). YaRN refines RoPE scaling and needs 10 times fewer tokens and 2.5 times fewer training steps than earlier methods; a Llama 2 model fine-tuned on 64K-token data extrapolated to 128K (Peng et al., 2024).

#### 5. How well long contexts are used

Liu et al. (2023) moved the passage containing the answer through the input of multi-document question answering and found a U-shaped curve: performance is highest when relevant information is at the beginning (primacy) or end (recency) and degrades in the middle, even for models built for long contexts. With the relevant passage in the middle, GPT-3.5-Turbo scored below its closed-book result without any documents (56.1%) (Liu et al., 2023; [[structured-context-construction|structured context construction]]). RULER extends needle-in-a-haystack tests with multiple needles, multi-hop tracing and aggregation; although almost all 17 tested models reached near-perfect accuracy on the plain needle test, only half of the models claiming 32K tokens or more performed satisfactorily at 32K (Hsieh et al., 2024).

#### Origin and variants

The original Transformer used sinusoidal position encodings (Jurafsky & Martin, 2026). Later work added relative encodings such as RoPE (Su et al., 2024) and ALiBi (Press et al., 2022), context extension by RoPE scaling (Chen et al., 2023; Peng et al., 2024), IO-aware exact attention (Dao et al., 2022) and benchmarks for effective context length (Hsieh et al., 2024). Non-Transformer architectures tested by RULER, RWKV and Mamba, degraded markedly beyond 8K (Hsieh et al., 2024).

### When to use it

Planning around the context window matters whenever inputs are long or numerous:

- RAG and document question answering, where the number and order of retrieved chunks must fit and the most relevant ones should not sit in the middle ([[rag-chunking|RAG chunking]], [[question-answering|question answering]]).
- Long conversations and agents, whose history grows with every step ([[memory-in-llms|memory in LLMs]], [[agentic-ai|agentic AI]]).
- Summarising or analysing long documents, where truncation silently drops content.
- Choosing a model: the effective, not the advertised, length decides ([[llm-evaluation|LLM evaluation]]).

### Strengths and limitations

**Strengths**
- Everything in the window is available to every later token through attention, without retrieval or training (Jurafsky & Martin, 2026).
- Windows can be extended after pre-training with modest fine-tuning (Chen et al., 2023; Peng et al., 2024).

**Limitations**
- Quadratic attention cost and a KV cache that grows with length (Jurafsky & Martin, 2026; Dao et al., 2022).
- Information in the middle of long inputs is used less reliably (Liu et al., 2023).
- Effective context length is often much shorter than the claimed one (Hsieh et al., 2024).
- Longer prompts cost more per request and add latency ([[llm-cost-optimisation|LLM cost optimisation]]).

### Comparison

| Approach | What it changes | Example result |
|---|---|---|
| Learned absolute positions | one embedding per position | last positions poorly trained (Jurafsky & Martin, 2026) |
| RoPE | rotation encodes relative position | most popular method (Jurafsky & Martin, 2026) |
| ALiBi | distance penalty on attention scores | 1,024 → 2,048 tokens extrapolation (Press et al., 2022) |
| Position Interpolation | rescales RoPE positions | 2,048 → 32,768 tokens (Chen et al., 2023) |
| YaRN | refined RoPE scaling | 128K with less training (Peng et al., 2024) |
| [[retrieval-augmented-generation\|RAG]] | puts only relevant passages into the window | depends on retrieval quality |

Sources as given in the table.

### In practice

Long-context benchmarks should test more than a single needle: RULER showed large drops with growing length and task complexity even for models that pass the vanilla test (Hsieh et al., 2024). Placing the most relevant material at the start or end of the prompt and keeping the context short counter the U-shaped curve found by Liu et al. (2023). Because the KV cache grows with every token, serving cost and memory depend on context length as much as on model size (Jurafsky & Martin, 2026).

### Key takeaway

The context window is the model's working memory: its length is set by training and position encoding, its cost grows quadratically, and long windows help only as far as the model actually uses what is in them.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 7: Transformers and Pretraining. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/7.pdf)
- Su, J. et al. (2024). *RoFormer: Enhanced Transformer with Rotary Position Embedding.* Neurocomputing. [arXiv:2104.09864](https://arxiv.org/abs/2104.09864)
- Press, O., Smith, N. A. & Lewis, M. (2022). *Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation.* ICLR 2022. [arXiv:2108.12409](https://arxiv.org/abs/2108.12409)
- Chen, S., Wong, S., Chen, L. & Tian, Y. (2023). *Extending Context Window of Large Language Models via Positional Interpolation.* [arXiv:2306.15595](https://arxiv.org/abs/2306.15595)
- Peng, B., Quesnelle, J., Fan, H. & Shippole, E. (2024). *YaRN: Efficient Context Window Extension of Large Language Models.* ICLR 2024. [arXiv:2309.00071](https://arxiv.org/abs/2309.00071)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Hsieh, C.-P. et al. (2024). *RULER: What's the Real Context Size of Your Long-Context Language Models?* COLM 2024. [arXiv:2404.06654](https://arxiv.org/abs/2404.06654)
- Dao, T., Fu, D. Y., Ermon, S., Rudra, A. & Ré, C. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness.* NeurIPS 2022. [arXiv:2205.14135](https://arxiv.org/abs/2205.14135)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Das Kontextfenster ist die Spanne an Tokens, auf die ein Transformer-Sprachmodell zugleich zugreifen kann: Prompt, abgerufene Dokumente, Gesprächsverlauf und die bisher erzeugte Ausgabe müssen hineinpassen (Jurafsky & Martin, 2026). Seine Länge ist durch das Training und die Positionskodierung festgelegt, und die Kosten der Attention wachsen quadratisch mit ihr (Jurafsky & Martin, 2026; Dao et al., 2022). Verfahren wie RoPE-Skalierung (Position Interpolation, YaRN) erweitern Fenster auf Zehn- oder Hunderttausende Tokens, doch Modelle nutzen lange Kontexte nicht gleichmäßig: Information in der Mitte wird schlechter genutzt als am Anfang oder Ende (Liu et al., 2023), und die effektive Länge liegt oft weit unter der angegebenen (Hsieh et al., 2024).

### Funktionsweise

```text
System-Prompt + Anweisungen + abgerufene Passagen + Verlauf + Nutzereingabe  ──►  Tokens 1 … N   (N ≤ Fenstergröße)
                                                                                   │
          Token-Embedding + Positionsinformation (gelernt / sinusförmig / RoPE / ALiBi)
                                                                                   ▼
          kausale Self-Attention: jedes Token betrachtet alle früheren  →  N × N Score-Matrix (quadratisch)
                                                                                   ▼
          Generierung: ein neues Token pro Schritt; Keys/Values früherer Tokens im KV-Cache
                                                                                   ▼
          wenn N das Fenster übersteigen würde: kürzen, zusammenfassen, gezielt abrufen oder Modell mit längerem Kontext nutzen
```

#### 1. Was das Fenster enthält

In einem kausalen Sprachmodell wird die Repräsentation von Token i aus Token i und allen früheren Tokens im Kontextfenster berechnet, das Tausende Tokens oder mehr umfasst (Jurafsky & Martin, 2026). Alles, was das Modell bei der Inferenz nutzen soll, also Prompt, Few-Shot-Beispiele, abgerufene Passagen in [[retrieval-augmented-generation|RAG]] und frühere Gesprächsrunden, konkurriert um dasselbe Fenster; wie es gefüllt wird, ist Gegenstand des [[context-engineering|Context Engineering]]. Große Modelle werden vortrainiert, indem das ganze Fenster mit Text gefüllt wird; mehrere kürzere Dokumente werden dabei mit End-of-Text-Tokens dazwischen zusammengepackt (Jurafsky & Martin, 2026).

#### 2. Warum das Fenster begrenzt ist: Kosten der Attention

Self-Attention berechnet ein Skalarprodukt zwischen jedem Paar von Positionen, sodass die Score-Matrix N × N groß und die Attention quadratisch in der Eingabelänge ist (Jurafsky & Martin, 2026; [[attention-and-transformers|Attention]]). Zeit- und Speicherbedarf der Self-Attention wachsen quadratisch mit der Sequenzlänge, was Transformer bei langen Sequenzen langsam und speicherhungrig macht; FlashAttention berechnet exakte Attention mit weniger Lese- und Schreibzugriffen auf den High-Bandwidth-Speicher der GPU und machte längere Kontexte praktikabel, etwa mit einer dreifachen Beschleunigung bei GPT-2 mit Sequenzlänge 1K (Dao et al., 2022). Bei der Generierung werden Keys und Values früherer Tokens in einem KV-Cache gespeichert, statt neu berechnet zu werden, sodass auch der Speicher mit der Kontextlänge wächst (Jurafsky & Martin, 2026).

#### 3. Positionsinformation

Transformer brauchen Positionsinformation, die zu den Token-Embeddings hinzukommt. Gelernte absolute Positions-Embeddings sehen für die letzten Positionen wenige Trainingsbeispiele und generalisieren dort womöglich schlecht; sinusförmige Embeddings nutzen eine feste Funktion der Position (Jurafsky & Martin, 2026). Rotary Position Embedding (RoPE) kodiert die absolute Position mit einer Rotationsmatrix und macht die Attention dabei von der relativen Position abhängig; es ist das verbreitetste Verfahren geworden (Su et al., 2024; Jurafsky & Martin, 2026). ALiBi fügt keine Positions-Embeddings hinzu, sondern bestraft Attention-Scores proportional zum Abstand zwischen Query und Key; ein Modell mit 1,3 Milliarden Parametern, trainiert auf 1.024 Tokens, extrapolierte auf 2.048 mit derselben Perplexität wie ein sinusförmiges Modell, das auf 2.048 trainiert wurde, und trainierte dabei 11 % schneller (Press et al., 2022).

#### 4. Das Fenster erweitern

RoPE-basierte Modelle generalisieren nicht über die Sequenzlänge hinaus, auf der sie trainiert wurden (Peng et al., 2024). Position Interpolation skaliert die Positionsindizes linear herunter, damit sie ins ursprüngliche Fenster passen, statt zu extrapolieren, was katastrophal hohe Attention-Scores erzeugen könnte; damit wurden LLaMA-Modelle innerhalb von 1.000 Fine-Tuning-Schritten von 2.048 auf bis zu 32.768 Tokens erweitert, während einfaches Fine-Tuning auf längeren Eingaben das effektive Fenster nach mehr als 10.000 Batches nur von 2.048 auf 2.560 vergrößerte (Chen et al., 2023). YaRN verfeinert die RoPE-Skalierung und braucht 10-mal weniger Tokens und 2,5-mal weniger Trainingsschritte als frühere Verfahren; ein auf 64K-Token-Daten nachtrainiertes Llama-2-Modell extrapolierte auf 128K (Peng et al., 2024).

#### 5. Wie gut lange Kontexte genutzt werden

Liu et al. (2023) verschoben die Passage mit der Antwort durch die Eingabe eines Multi-Dokument-Question-Answering und fanden eine U-förmige Kurve: Die Leistung ist am höchsten, wenn die relevante Information am Anfang (Primacy) oder Ende (Recency) steht, und sinkt in der Mitte, auch bei Modellen für lange Kontexte. Mit der relevanten Passage in der Mitte schnitt GPT-3.5-Turbo schlechter ab als ganz ohne Dokumente im Closed-Book-Setting (56,1 %) (Liu et al., 2023; [[structured-context-construction|strukturierter Kontextaufbau]]). RULER erweitert Needle-in-a-Haystack-Tests um mehrere Nadeln, Multi-Hop-Verfolgung und Aggregation; obwohl fast alle 17 getesteten Modelle beim einfachen Nadeltest nahezu perfekt abschnitten, erreichte nur die Hälfte der Modelle, die 32K Tokens oder mehr angaben, bei 32K eine zufriedenstellende Leistung (Hsieh et al., 2024).

#### Ursprung und Varianten

Der ursprüngliche Transformer nutzte sinusförmige Positionskodierungen (Jurafsky & Martin, 2026). Spätere Arbeiten ergänzten relative Kodierungen wie RoPE (Su et al., 2024) und ALiBi (Press et al., 2022), Kontexterweiterung durch RoPE-Skalierung (Chen et al., 2023; Peng et al., 2024), IO-bewusste exakte Attention (Dao et al., 2022) und Benchmarks für die effektive Kontextlänge (Hsieh et al., 2024). Die von RULER getesteten Nicht-Transformer-Architekturen RWKV und Mamba verschlechterten sich jenseits von 8K deutlich (Hsieh et al., 2024).

### Wann einsetzen

Die Planung rund um das Kontextfenster zählt immer dann, wenn Eingaben lang oder zahlreich sind:

- RAG und Fragen über Dokumente, bei denen Zahl und Reihenfolge der abgerufenen Chunks passen müssen und die relevantesten nicht in der Mitte stehen sollten ([[rag-chunking|RAG-Chunking]], [[question-answering|Question Answering]]).
- Lange Gespräche und Agenten, deren Verlauf mit jedem Schritt wächst ([[memory-in-llms|Gedächtnis in LLMs]], [[agentic-ai|Agentic AI]]).
- Zusammenfassen oder Analysieren langer Dokumente, bei denen Kürzen still Inhalte verwirft.
- Modellwahl: Entscheidend ist die effektive, nicht die angegebene Länge ([[llm-evaluation|LLM-Evaluation]]).

### Stärken und Grenzen

**Stärken**
- Alles im Fenster steht jedem späteren Token über die Attention zur Verfügung, ohne Retrieval oder Training (Jurafsky & Martin, 2026).
- Fenster lassen sich nach dem Vortraining mit moderatem Fine-Tuning erweitern (Chen et al., 2023; Peng et al., 2024).

**Grenzen**
- Quadratische Kosten der Attention und ein KV-Cache, der mit der Länge wächst (Jurafsky & Martin, 2026; Dao et al., 2022).
- Information in der Mitte langer Eingaben wird weniger zuverlässig genutzt (Liu et al., 2023).
- Die effektive Kontextlänge ist oft viel kürzer als die angegebene (Hsieh et al., 2024).
- Längere Prompts kosten pro Anfrage mehr und erhöhen die Latenz ([[llm-cost-optimisation|LLM-Kostenoptimierung]]).

### Vergleich

| Ansatz | Was er ändert | Beispielergebnis |
|---|---|---|
| Gelernte absolute Positionen | ein Embedding pro Position | letzte Positionen schlecht trainiert (Jurafsky & Martin, 2026) |
| RoPE | Rotation kodiert relative Position | verbreitetstes Verfahren (Jurafsky & Martin, 2026) |
| ALiBi | Abstandsstrafe auf Attention-Scores | Extrapolation von 1.024 auf 2.048 Tokens (Press et al., 2022) |
| Position Interpolation | skaliert RoPE-Positionen um | 2.048 → 32.768 Tokens (Chen et al., 2023) |
| YaRN | verfeinerte RoPE-Skalierung | 128K mit weniger Training (Peng et al., 2024) |
| [[retrieval-augmented-generation\|RAG]] | bringt nur relevante Passagen ins Fenster | hängt von der Retrieval-Qualität ab |

Quellen wie in der Tabelle angegeben.

### In der Praxis

Benchmarks für lange Kontexte sollten mehr als eine einzelne Nadel prüfen: RULER zeigte mit wachsender Länge und Aufgabenkomplexität große Einbrüche, auch bei Modellen, die den einfachen Test bestehen (Hsieh et al., 2024). Das wichtigste Material an den Anfang oder das Ende des Prompts zu stellen und den Kontext kurz zu halten wirkt der von Liu et al. (2023) gefundenen U-Kurve entgegen. Weil der KV-Cache mit jedem Token wächst, hängen Betriebskosten und Speicher ebenso von der Kontextlänge ab wie von der Modellgröße (Jurafsky & Martin, 2026).

### Merksatz

Das Kontextfenster ist das Arbeitsgedächtnis des Modells: Seine Länge wird durch Training und Positionskodierung festgelegt, seine Kosten wachsen quadratisch, und lange Fenster helfen nur so weit, wie das Modell ihren Inhalt tatsächlich nutzt.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 7: Transformers and Pretraining. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/7.pdf)
- Su, J. et al. (2024). *RoFormer: Enhanced Transformer with Rotary Position Embedding.* Neurocomputing. [arXiv:2104.09864](https://arxiv.org/abs/2104.09864)
- Press, O., Smith, N. A. & Lewis, M. (2022). *Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation.* ICLR 2022. [arXiv:2108.12409](https://arxiv.org/abs/2108.12409)
- Chen, S., Wong, S., Chen, L. & Tian, Y. (2023). *Extending Context Window of Large Language Models via Positional Interpolation.* [arXiv:2306.15595](https://arxiv.org/abs/2306.15595)
- Peng, B., Quesnelle, J., Fan, H. & Shippole, E. (2024). *YaRN: Efficient Context Window Extension of Large Language Models.* ICLR 2024. [arXiv:2309.00071](https://arxiv.org/abs/2309.00071)
- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* TACL. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Hsieh, C.-P. et al. (2024). *RULER: What's the Real Context Size of Your Long-Context Language Models?* COLM 2024. [arXiv:2404.06654](https://arxiv.org/abs/2404.06654)
- Dao, T., Fu, D. Y., Ermon, S., Rudra, A. & Ré, C. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness.* NeurIPS 2022. [arXiv:2205.14135](https://arxiv.org/abs/2205.14135)
