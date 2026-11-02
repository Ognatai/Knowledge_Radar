---
title_en: LLM Inference and Serving
title_de: LLM-Inferenz und Serving
entity_type: Method
aliases:
- LLM serving
- LLM inference
- Inference serving
- KV cache
- KV-Cache
- PagedAttention
- vLLM
- Continuous batching
- Iteration-level scheduling
- Grouped-query attention
- Multi-query attention
sources:
- https://web.stanford.edu/~jurafsky/slp3/7.pdf
- https://arxiv.org/abs/2309.06180
- https://www.usenix.org/conference/osdi22/presentation/yu
- https://arxiv.org/abs/1911.02150
- https://arxiv.org/abs/2305.13245
- https://arxiv.org/abs/2312.07104
- https://arxiv.org/abs/2211.17192
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Serving a large language model means generating tokens for many concurrent requests at low latency and high throughput. Generation is autoregressive, one token per forward pass, so it is limited by memory bandwidth rather than compute, and the keys and values of all earlier tokens are kept in a KV cache that grows with every token (Kwon et al., 2023; Jurafsky & Martin, 2026). Serving systems therefore batch requests at the level of single iterations (continuous batching, Yu et al., 2022), manage the KV cache like virtual memory in pages (PagedAttention in vLLM, Kwon et al., 2023), share cached prefixes between requests (Zheng et al., 2024) and shrink the cache with multi-query or grouped-query attention (Shazeer, 2019; Ainslie et al., 2023).

### How it works

```text
requests arrive ──► scheduler (iteration-level: add / remove requests every step)
                        │
          prefill: whole prompt in parallel ──► KV cache for prompt tokens   (compute-bound)
                        │
          decode loop: one token per request per step, reads all weights + KV cache   (memory-bound)
                        │
          KV cache manager: fixed-size blocks, block tables, copy-on-write, prefix sharing (radix tree)
                        ▼
          stream tokens back; free blocks when a request finishes
```

#### 1. Prefill and decode

In the prompt (prefill) phase, all prompt tokens are known, so the model computes them in parallel with matrix–matrix multiplications and stores their keys and values; in the generation (decode) phase, tokens are produced one at a time and each step depends on the previous one (Kwon et al., 2023). The decode phase underutilises GPU compute, is memory-bound and accounts for most of a request's latency (Kwon et al., 2023). Training does not have this problem, because all positions of a sequence are computed at once (Jurafsky & Martin, 2026; [[attention-and-transformers|attention]]).

#### 2. The KV cache

Recomputing keys and values of all earlier tokens at every step would waste computation, so they are stored in a KV cache and only the new token's query, key and value are computed (Jurafsky & Martin, 2026). For a 13-billion-parameter model on a 40 GB A100, about 65% of memory holds the weights and close to 30% the KV cache of active requests; since weights are fixed, KV cache management decides the maximum batch size and thus throughput (Kwon et al., 2023). Its size grows with the [[context-window|context length]] and the number of concurrent requests.

#### 3. Continuous batching

Batching many requests uses the GPU better, but request-level batching keeps finished requests waiting until the whole batch ends and makes new requests wait for the next batch. Orca schedules at the granularity of a single model iteration, so requests join and leave the batch after every token, and applies batching selectively only to operations where it is possible; on GPT-3 175B it achieved 36.9 times the throughput of NVIDIA FasterTransformer at the same latency (Yu et al., 2022).

#### 4. PagedAttention and vLLM

Earlier systems reserved a contiguous chunk of memory for each request's maximum length, causing reserved slots, internal and external fragmentation; only 20.4% to 38.2% of KV cache memory held actual token states (Kwon et al., 2023). PagedAttention, inspired by virtual memory and paging in operating systems, stores the KV cache in fixed-size blocks that need not be contiguous and are allocated on demand, mapped through a block table (Kwon et al., 2023). This brings memory waste close to zero and allows blocks to be shared, for example the prompt of a request sampled several times or common prefixes of beam search hypotheses, with copy-on-write when a shared block must change; vLLM, built on it, improved throughput 2 to 4 times over FasterTransformer and Orca at the same latency, more for longer sequences, larger models and complex decoding (Kwon et al., 2023; [[decoding-strategies|decoding strategies]]).

#### 5. Reusing prefixes across requests

Many applications send the same system prompt, few-shot examples or conversation history repeatedly. SGLang's RadixAttention keeps KV caches of finished requests in a radix tree keyed by token sequences, finds the longest cached prefix of a new request, evicts least recently used leaves when memory is needed and schedules requests to increase cache hits; together with other runtime optimisations it achieved up to 6.4 times higher throughput on agent, RAG, JSON and multi-turn workloads (Zheng et al., 2024; [[agentic-ai|agentic AI]], [[retrieval-augmented-generation|RAG]]).

#### 6. Smaller KV caches: MQA and GQA

Incremental decoding is slow because the large key and value tensors must be loaded repeatedly from memory. Multi-query attention shares one set of keys and values across all attention heads, which greatly reduces the cache and the bandwidth per step at a minor cost in quality (Shazeer, 2019). Grouped-query attention uses an intermediate number of key–value heads; existing multi-head checkpoints can be uptrained to it with 5% of the original pre-training compute, reaching quality close to multi-head attention at a speed comparable to MQA (Ainslie et al., 2023).

#### Origin and variants

Other techniques address the same bottleneck: [[speculative-decoding|speculative decoding]] lets a small model propose several tokens that the large model verifies in one pass, which gave 2 to 3 times faster decoding of T5-XXL with identical outputs (Leviathan et al., 2023); [[quantisation|quantisation]] shrinks weights and caches; [[flashattention|FlashAttention]] speeds up the attention kernel itself; and [[mixture-of-experts|mixture-of-experts]] models activate only part of their parameters per token.

### When to use it

- Self-hosting open models for an application or team instead of using a provider API ([[cloud-ai-platforms|cloud AI platforms]], [[mlops-and-deployment|MLOps and deployment]]).
- Workloads with many concurrent users, long prompts or shared system prompts, where batching and prefix caching pay off (Kwon et al., 2023; Zheng et al., 2024).
- Sampling several outputs per request or beam search, which benefit from shared KV blocks (Kwon et al., 2023).

### Strengths and limitations

**Strengths**
- Iteration-level batching and paged KV memory multiply throughput without changing model outputs (Yu et al., 2022; Kwon et al., 2023).
- Prefix sharing cuts repeated prefill work for agents and RAG (Zheng et al., 2024).
- MQA/GQA reduce memory traffic at small quality cost (Shazeer, 2019; Ainslie et al., 2023).

**Limitations**
- Decode remains memory-bound; latency per token is bounded by memory bandwidth (Kwon et al., 2023).
- Long contexts and many users still exhaust KV cache memory, forcing smaller batches or eviction (Kwon et al., 2023; Zheng et al., 2024).
- MQA and GQA must be part of the model architecture or added by uptraining (Ainslie et al., 2023).
- Throughput gains are reported at a fixed latency level, so batch size has to be tuned against latency targets (Yu et al., 2022; Kwon et al., 2023).

### Comparison

| Technique | Problem addressed | Reported effect |
|---|---|---|
| KV cache | recomputing earlier keys and values | avoids redundant compute (Jurafsky & Martin, 2026) |
| Continuous (iteration-level) batching | requests waiting for a whole batch | 36.9× throughput vs FasterTransformer (Yu et al., 2022) |
| PagedAttention / vLLM | KV cache fragmentation | 2–4× throughput vs FasterTransformer and Orca (Kwon et al., 2023) |
| RadixAttention / SGLang | repeated prefixes | up to 6.4× throughput (Zheng et al., 2024) |
| MQA / GQA | KV cache size and bandwidth | near multi-head quality at MQA speed (Ainslie et al., 2023) |
| [[speculative-decoding\|Speculative decoding]] | one token per large-model pass | 2–3× faster T5-XXL decoding (Leviathan et al., 2023) |

Sources as given in the table.

### In practice

Capacity planning starts from memory: weights plus KV cache per token times context length times concurrent requests must fit on the GPUs (Kwon et al., 2023). Putting stable content such as system prompts and tool descriptions at the start of the prompt makes prefix caching effective (Zheng et al., 2024; [[context-engineering|context engineering]]). Because prefill is parallel and decode is memory-bound (Kwon et al., 2023), the latency until the first token and the time per later token behave differently and are worth tracking separately ([[llm-observability-and-tracing|observability]], [[llm-cost-optimisation|cost optimisation]]).

### Key takeaway

LLM serving is dominated by the memory-bound decode loop and the KV cache; iteration-level batching, paged and shared KV memory and fewer key–value heads let one GPU serve many more requests without changing the model's outputs.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 7: Transformers and Pretraining (KV cache). [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/7.pdf)
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention.* SOSP 2023. [arXiv:2309.06180](https://arxiv.org/abs/2309.06180)
- Yu, G.-I., Jeong, J. S., Kim, G.-W., Kim, S. & Chun, B.-G. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models.* OSDI 2022. [usenix.org](https://www.usenix.org/conference/osdi22/presentation/yu)
- Shazeer, N. (2019). *Fast Transformer Decoding: One Write-Head is All You Need.* [arXiv:1911.02150](https://arxiv.org/abs/1911.02150)
- Ainslie, J. et al. (2023). *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints.* EMNLP 2023. [arXiv:2305.13245](https://arxiv.org/abs/2305.13245)
- Zheng, L. et al. (2024). *SGLang: Efficient Execution of Structured Language Model Programs.* NeurIPS 2024. [arXiv:2312.07104](https://arxiv.org/abs/2312.07104)
- Leviathan, Y., Kalman, M. & Matias, Y. (2023). *Fast Inference from Transformers via Speculative Decoding.* ICML 2023. [arXiv:2211.17192](https://arxiv.org/abs/2211.17192)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein großes Sprachmodell zu betreiben (Serving) heißt, für viele gleichzeitige Anfragen mit geringer Latenz und hohem Durchsatz Tokens zu erzeugen. Die Generierung ist autoregressiv, ein Token pro Forward Pass, und wird daher von der Speicherbandbreite statt von der Rechenleistung begrenzt; Keys und Values aller früheren Tokens liegen in einem KV-Cache, der mit jedem Token wächst (Kwon et al., 2023; Jurafsky & Martin, 2026). Serving-Systeme bündeln Anfragen daher auf Ebene einzelner Iterationen (Continuous Batching, Yu et al., 2022), verwalten den KV-Cache wie virtuellen Speicher in Seiten (PagedAttention in vLLM, Kwon et al., 2023), teilen zwischengespeicherte Präfixe zwischen Anfragen (Zheng et al., 2024) und verkleinern den Cache mit Multi-Query- oder Grouped-Query-Attention (Shazeer, 2019; Ainslie et al., 2023).

### Funktionsweise

```text
Anfragen treffen ein ──► Scheduler (auf Iterationsebene: Anfragen in jedem Schritt hinzufügen / entfernen)
                            │
          Prefill: ganzer Prompt parallel ──► KV-Cache für die Prompt-Tokens   (rechengebunden)
                            │
          Decode-Schleife: ein Token pro Anfrage und Schritt, liest alle Gewichte + KV-Cache   (speichergebunden)
                            │
          KV-Cache-Verwaltung: Blöcke fester Größe, Blocktabellen, Copy-on-Write, Präfix-Teilung (Radix-Baum)
                            ▼
          Tokens zurückstreamen; Blöcke freigeben, wenn eine Anfrage fertig ist
```

#### 1. Prefill und Decode

In der Prompt-Phase (Prefill) sind alle Prompt-Tokens bekannt, sodass das Modell sie parallel mit Matrix-Matrix-Multiplikationen berechnet und ihre Keys und Values speichert; in der Generierungsphase (Decode) entstehen Tokens einzeln, und jeder Schritt hängt vom vorigen ab (Kwon et al., 2023). Die Decode-Phase lastet die GPU-Rechenleistung kaum aus, ist speichergebunden und macht den größten Teil der Latenz einer Anfrage aus (Kwon et al., 2023). Beim Training gibt es dieses Problem nicht, weil alle Positionen einer Sequenz zugleich berechnet werden (Jurafsky & Martin, 2026; [[attention-and-transformers|Attention]]).

#### 2. Der KV-Cache

Keys und Values aller früheren Tokens in jedem Schritt neu zu berechnen, wäre verschwendete Rechenzeit; sie werden daher in einem KV-Cache gespeichert, und nur Query, Key und Value des neuen Tokens werden berechnet (Jurafsky & Martin, 2026). Bei einem Modell mit 13 Milliarden Parametern auf einer A100 mit 40 GB belegen die Gewichte etwa 65 % des Speichers und der KV-Cache der aktiven Anfragen knapp 30 %; da die Gewichte fest sind, entscheidet die Verwaltung des KV-Cache über die maximale Batch-Größe und damit den Durchsatz (Kwon et al., 2023). Seine Größe wächst mit der [[context-window|Kontextlänge]] und der Zahl gleichzeitiger Anfragen.

#### 3. Continuous Batching

Viele Anfragen zu bündeln nutzt die GPU besser, doch Batching auf Anfrageebene lässt fertige Anfragen warten, bis der ganze Batch endet, und neue Anfragen auf den nächsten Batch. Orca plant auf der Ebene einer einzelnen Modelliteration, sodass Anfragen nach jedem Token dem Batch beitreten und ihn verlassen, und wendet Batching selektiv nur auf Operationen an, bei denen es möglich ist; auf GPT-3 175B erreichte es bei gleicher Latenz das 36,9-Fache des Durchsatzes von NVIDIA FasterTransformer (Yu et al., 2022).

#### 4. PagedAttention und vLLM

Frühere Systeme reservierten für jede Anfrage einen zusammenhängenden Speicherblock für ihre maximale Länge, was reservierte Plätze sowie interne und externe Fragmentierung verursachte; nur 20,4 % bis 38,2 % des KV-Cache-Speichers enthielten tatsächliche Token-Zustände (Kwon et al., 2023). PagedAttention, inspiriert von virtuellem Speicher und Paging in Betriebssystemen, speichert den KV-Cache in Blöcken fester Größe, die nicht zusammenhängen müssen und bei Bedarf zugeteilt werden, abgebildet über eine Blocktabelle (Kwon et al., 2023). Das senkt die Speicherverschwendung fast auf null und erlaubt das Teilen von Blöcken, etwa des Prompts einer mehrfach gezogenen Anfrage oder gemeinsamer Präfixe von Beam-Search-Hypothesen, mit Copy-on-Write, wenn sich ein geteilter Block ändern muss; das darauf aufbauende vLLM steigerte den Durchsatz gegenüber FasterTransformer und Orca bei gleicher Latenz um das 2- bis 4-Fache, stärker bei längeren Sequenzen, größeren Modellen und komplexem Decoding (Kwon et al., 2023; [[decoding-strategies|Decoding-Strategien]]).

#### 5. Präfixe über Anfragen hinweg wiederverwenden

Viele Anwendungen senden denselben System-Prompt, dieselben Few-Shot-Beispiele oder denselben Gesprächsverlauf wiederholt. RadixAttention in SGLang hält die KV-Caches abgeschlossener Anfragen in einem Radix-Baum über Token-Sequenzen, findet das längste zwischengespeicherte Präfix einer neuen Anfrage, verdrängt bei Speicherbedarf die am längsten nicht genutzten Blätter und plant Anfragen so, dass mehr Cache-Treffer entstehen; zusammen mit weiteren Laufzeitoptimierungen erreichte es bei Agenten-, RAG-, JSON- und Mehrrunden-Workloads bis zu 6,4-fach höheren Durchsatz (Zheng et al., 2024; [[agentic-ai|Agentic AI]], [[retrieval-augmented-generation|RAG]]).

#### 6. Kleinere KV-Caches: MQA und GQA

Inkrementelles Decoding ist langsam, weil die großen Key- und Value-Tensoren immer wieder aus dem Speicher geladen werden müssen. Multi-Query-Attention teilt einen Satz Keys und Values über alle Attention-Heads, was den Cache und die Bandbreite pro Schritt stark verringert, bei geringem Qualitätsverlust (Shazeer, 2019). Grouped-Query-Attention nutzt eine mittlere Zahl von Key-Value-Heads; bestehende Multi-Head-Checkpoints lassen sich mit 5 % der ursprünglichen Vortrainingsrechenleistung darauf nachtrainieren und erreichen eine Qualität nahe Multi-Head-Attention bei einer Geschwindigkeit vergleichbar mit MQA (Ainslie et al., 2023).

#### Ursprung und Varianten

Andere Techniken setzen am selben Engpass an: [[speculative-decoding|Speculative Decoding]] lässt ein kleines Modell mehrere Tokens vorschlagen, die das große Modell in einem Durchgang prüft, was T5-XXL bei identischen Ausgaben 2- bis 3-mal schneller dekodierte (Leviathan et al., 2023); [[quantisation|Quantisierung]] verkleinert Gewichte und Caches; [[flashattention|FlashAttention]] beschleunigt den Attention-Kernel selbst; und [[mixture-of-experts|Mixture-of-Experts]]-Modelle aktivieren pro Token nur einen Teil ihrer Parameter.

### Wann einsetzen

- Offene Modelle für eine Anwendung oder ein Team selbst betreiben, statt eine Anbieter-API zu nutzen ([[cloud-ai-platforms|Cloud-KI-Plattformen]], [[mlops-and-deployment|MLOps und Deployment]]).
- Workloads mit vielen gleichzeitigen Nutzenden, langen Prompts oder geteilten System-Prompts, bei denen sich Batching und Präfix-Caching auszahlen (Kwon et al., 2023; Zheng et al., 2024).
- Mehrere Ausgaben pro Anfrage oder Beam Search, die von geteilten KV-Blöcken profitieren (Kwon et al., 2023).

### Stärken und Grenzen

**Stärken**
- Batching auf Iterationsebene und seitenweiser KV-Speicher vervielfachen den Durchsatz, ohne die Modellausgaben zu ändern (Yu et al., 2022; Kwon et al., 2023).
- Das Teilen von Präfixen spart wiederholte Prefill-Arbeit bei Agenten und RAG (Zheng et al., 2024).
- MQA/GQA verringern den Speicherverkehr bei geringem Qualitätsverlust (Shazeer, 2019; Ainslie et al., 2023).

**Grenzen**
- Decode bleibt speichergebunden; die Latenz pro Token wird von der Speicherbandbreite begrenzt (Kwon et al., 2023).
- Lange Kontexte und viele Nutzende erschöpfen weiterhin den KV-Cache-Speicher und erzwingen kleinere Batches oder Verdrängung (Kwon et al., 2023; Zheng et al., 2024).
- MQA und GQA müssen Teil der Modellarchitektur sein oder durch Nachtraining ergänzt werden (Ainslie et al., 2023).
- Durchsatzgewinne werden bei festem Latenzniveau berichtet, die Batch-Größe muss daher gegen Latenzziele abgestimmt werden (Yu et al., 2022; Kwon et al., 2023).

### Vergleich

| Technik | Adressiertes Problem | Berichteter Effekt |
|---|---|---|
| KV-Cache | Neuberechnung früherer Keys und Values | vermeidet redundante Rechnung (Jurafsky & Martin, 2026) |
| Continuous Batching (Iterationsebene) | Anfragen warten auf einen ganzen Batch | 36,9-facher Durchsatz gegenüber FasterTransformer (Yu et al., 2022) |
| PagedAttention / vLLM | Fragmentierung des KV-Cache | 2- bis 4-facher Durchsatz gegenüber FasterTransformer und Orca (Kwon et al., 2023) |
| RadixAttention / SGLang | wiederholte Präfixe | bis zu 6,4-facher Durchsatz (Zheng et al., 2024) |
| MQA / GQA | Größe und Bandbreite des KV-Cache | Qualität nahe Multi-Head bei MQA-Geschwindigkeit (Ainslie et al., 2023) |
| [[speculative-decoding\|Speculative Decoding]] | ein Token pro Durchgang des großen Modells | 2- bis 3-fach schnelleres Decoding von T5-XXL (Leviathan et al., 2023) |

Quellen wie in der Tabelle angegeben.

### In der Praxis

Die Kapazitätsplanung beginnt beim Speicher: Gewichte plus KV-Cache pro Token mal Kontextlänge mal gleichzeitige Anfragen müssen auf die GPUs passen (Kwon et al., 2023). Stabile Inhalte wie System-Prompts und Tool-Beschreibungen an den Anfang des Prompts zu stellen macht Präfix-Caching wirksam (Zheng et al., 2024; [[context-engineering|Context Engineering]]). Weil Prefill parallel läuft und Decode speichergebunden ist (Kwon et al., 2023), verhalten sich die Latenz bis zum ersten Token und die Zeit pro weiterem Token unterschiedlich und lohnen eine getrennte Beobachtung ([[llm-observability-and-tracing|Observability]], [[llm-cost-optimisation|Kostenoptimierung]]).

### Merksatz

LLM-Serving wird von der speichergebundenen Decode-Schleife und dem KV-Cache bestimmt; Batching auf Iterationsebene, seitenweiser und geteilter KV-Speicher und weniger Key-Value-Heads lassen eine GPU viel mehr Anfragen bedienen, ohne die Ausgaben des Modells zu ändern.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 7: Transformers and Pretraining (KV-Cache). [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/7.pdf)
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention.* SOSP 2023. [arXiv:2309.06180](https://arxiv.org/abs/2309.06180)
- Yu, G.-I., Jeong, J. S., Kim, G.-W., Kim, S. & Chun, B.-G. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models.* OSDI 2022. [usenix.org](https://www.usenix.org/conference/osdi22/presentation/yu)
- Shazeer, N. (2019). *Fast Transformer Decoding: One Write-Head is All You Need.* [arXiv:1911.02150](https://arxiv.org/abs/1911.02150)
- Ainslie, J. et al. (2023). *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints.* EMNLP 2023. [arXiv:2305.13245](https://arxiv.org/abs/2305.13245)
- Zheng, L. et al. (2024). *SGLang: Efficient Execution of Structured Language Model Programs.* NeurIPS 2024. [arXiv:2312.07104](https://arxiv.org/abs/2312.07104)
- Leviathan, Y., Kalman, M. & Matias, Y. (2023). *Fast Inference from Transformers via Speculative Decoding.* ICML 2023. [arXiv:2211.17192](https://arxiv.org/abs/2211.17192)
