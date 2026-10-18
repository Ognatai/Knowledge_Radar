---
title_en: LLaMA (Llama Model Family)
title_de: LLaMA (Llama-Modellfamilie)
entity_type: Method
aliases:
- LLaMA
- Llama
- Llama 2
- Llama 3
- Llama 3.1
sources:
- https://arxiv.org/abs/2302.13971
- https://arxiv.org/abs/2307.09288
- https://arxiv.org/abs/2407.21783
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

LLaMA is [[meta|Meta]]'s family of openly released [[large-language-models|large language models]]. The first LLaMA models (7 to 65 billion parameters, 2023) were trained only on publicly available data for 1 to 1.4 trillion tokens; LLaMA-13B outperformed GPT-3 with 175 billion parameters on most benchmarks, showing that smaller models trained longer are cheaper at inference (Touvron et al., 2023a). Llama 2 (7 to 70 billion) added 40% more training data, a doubled context of 4,096 tokens and chat versions aligned with RLHF, released for research and commercial use (Touvron et al., 2023b). Llama 3.1 (8, 70 and 405 billion) trained on 15.6 trillion tokens with a context of up to 128,000 tokens, supports eight languages and [[tool-calling|tool use]], and reached quality comparable to GPT-4 on many tasks (Llama Team, 2024).

### How it works

```text
pre-training data: public web (CommonCrawl, C4), code, Wikipedia, books, arXiv, StackExchange …
 ▼ BPE tokenisation
decoder-only Transformer with
   pre-normalisation (RMSNorm) · SwiGLU activation · rotary position embeddings (RoPE)
   + grouped-query attention for larger models (Llama 2 34B/70B, Llama 3)
 ▼ next-token prediction on trillions of tokens (AdamW, cosine schedule)
 ▼ post-training: SFT → RLHF (Llama 2: rejection sampling + PPO) / SFT + rejection sampling + DPO (Llama 3)
 ▼ released weights: base and chat/instruct models, plus safety classifiers (Llama Guard 3)
```

#### 1. Training compute-optimal for inference

Scaling laws suggest how to split a fixed training budget between model size and data, but they ignore the cost of serving the model (Touvron et al., 2023a). LLaMA instead targets the best performance for a given inference budget by training smaller models on more tokens than usual: the authors found a 7-billion-parameter model still improving after 1 trillion tokens, although earlier guidance recommended about 200 billion tokens for a 10-billion model. The 33B and 65B models were trained on 1.4 trillion tokens; training the 65B model took about 21 days on 2,048 A100 GPUs at about 380 tokens per second per GPU (Touvron et al., 2023a). Scaling behaviour is discussed in [[large-language-models|large language models]].

#### 2. Data

The first LLaMA used only publicly available data: mostly English CommonCrawl and C4, plus GitHub code, Wikipedia in 20 languages, the Gutenberg and Books3 book corpora, arXiv and StackExchange (Touvron et al., 2023a). Llama 2 trained on 2 trillion tokens with more robust cleaning and removed data from sites known to contain a high volume of personal information (Touvron et al., 2023b). Llama 3 used a multilingual corpus of about 15 trillion tokens, compared with 1.8 trillion for Llama 2 (Llama Team, 2024). The legal questions of training data are covered in [[copyright-and-ai-training-data|copyright and AI training data]].

#### 3. Architecture

LLaMA is a decoder-only Transformer ([[attention-and-transformers|attention and Transformers]]) with three changes from the original design: pre-normalisation of each sub-layer's input with RMSNorm for stable training, the SwiGLU activation instead of ReLU, and rotary position [[embeddings|embeddings]] (RoPE) instead of absolute positions (Touvron et al., 2023a). Llama 2 adds grouped-query attention to the 34B and 70B models to make inference more scalable (Touvron et al., 2023b). For Llama 3, the team deliberately kept a standard dense Transformer rather than a mixture-of-experts model to keep training stable, with the largest model at 405 billion parameters (Llama Team, 2024).

#### 4. Post-training and safety

Llama 2-Chat was fine-tuned with supervised examples and then with reinforcement learning from human feedback, using two reward models for helpfulness and safety and both rejection sampling and proximal policy optimisation; a technique called Ghost Attention keeps system instructions effective over multiple turns (Touvron et al., 2023b). Llama 3 replaced PPO with rounds of supervised fine-tuning, rejection sampling and direct preference optimisation, and was released together with Llama Guard 3, a classifier for input and output safety (Llama Team, 2024). The alignment methods are explained in [[llm-alignment|LLM alignment]], safety classifiers in [[llm-guardrails|LLM guardrails]].

#### 5. Capabilities and releases

LLaMA-65B was competitive with Chinchilla-70B and PaLM-540B (Touvron et al., 2023a). Llama 2-Chat outperformed open-source chat models on most tested benchmarks and, in the authors' human evaluations of helpfulness and safety, may substitute for closed models (Touvron et al., 2023b). Llama 3.1 supports eight languages (English, German, French, Italian, Portuguese, Hindi, Spanish and Thai), coding, reasoning and tool use, and the 405B model reached quality comparable to GPT-4 on many tasks; all three sizes were released under the Llama 3 Community License (Llama Team, 2024).

#### Origin and variants

Meta AI released the first LLaMA models to the research community in February 2023, Llama 2 in July 2023 for research and commercial use, and Llama 3.1 in July 2024 (Touvron et al., 2023a; 2023b; Llama Team, 2024). Experiments in the Llama 3 paper also attach image, video and speech encoders, see [[multimodal-models|multimodal models]]. Because the weights are available, Llama models are a common base for fine-tuning with methods such as [[lora|LoRA]] and [[qlora|QLoRA]] and for local deployment ([[llm-adaptation|LLM adaptation]], [[quantisation|quantisation]]).

### When to use it

- Applications that need an LLM running on own infrastructure, for example for data protection or cost reasons ([[mlops-and-deployment|MLOps and deployment]]).
- Fine-tuning or adapting a model to a domain, where open weights are required ([[llm-adaptation|LLM adaptation]]).
- Research on LLM behaviour, bias or safety, where model internals must be accessible (Touvron et al., 2023a).

### Strengths and limitations

**Strengths**
- Open weights in several sizes, from models that run on one GPU to frontier scale (Llama Team, 2024).
- Smaller models trained on many tokens give strong quality per inference cost (Touvron et al., 2023a).
- Documented training data, architecture and safety work (Touvron et al., 2023a; 2023b).

**Limitations**
- Licences carry conditions; the Llama 2 and 3 releases use Meta's own licences rather than a standard open-source licence (Touvron et al., 2023b; Llama Team, 2024).
- Like other LLMs trained on web data, the models can reproduce biases and produce toxic content; the authors note their evaluations are not sufficient to understand all risks (Touvron et al., 2023a).
- Llama 3 8B and 70B were pre-trained on multilingual data but initially intended for English (Llama Team, 2024).

### Comparison

| Generation | Sizes | Training tokens | Context | Post-training |
|---|---|---|---|---|
| LLaMA (2023) | 7B–65B | 1–1.4 T | 2,048 | none (base models) |
| Llama 2 (2023) | 7B–70B | 2 T | 4,096 | SFT + RLHF (rejection sampling, PPO) |
| Llama 3.1 (2024) | 8B, 70B, 405B | 15.6 T (405B) | up to 128K | SFT + rejection sampling + DPO |

Sources: Touvron et al. (2023a; 2023b); Llama Team (2024). The 2,048-token (2k) context of the first LLaMA is taken from the comparison table in Touvron et al. (2023b). Other model families are compared in [[large-language-models|large language models]] and [[gpt|GPT]].

### In practice

Llama models are typically run quantised on local GPUs or served through cloud model catalogues ([[cloud-ai-platforms|cloud AI platforms]], [[quantisation|quantisation]]). Bias and safety evaluation remains the deployer's task: LLaMA's own analysis found biases across categories such as gender, religion and age ([[bias-in-nlp|bias in NLP]]; Touvron et al., 2023a).

### Regulatory context

Providers of general-purpose AI models released under free and open-source licences have reduced obligations under the [[eu-ai-act|EU AI Act]], unless the model has systemic risk; whether Llama's licence qualifies is a legal question beyond this note.

### Key takeaway

The Llama family showed that openly released, comparatively small decoder-only Transformers trained on many tokens of public data can match much larger closed models, and its later generations added RLHF or DPO alignment, long context, multilinguality and frontier scale.

### Sources

- Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.-A., Lacroix, T., Rozière, B., Goyal, N., Hambro, E., Azhar, F., Rodriguez, A., Joulin, A., Grave, E. & Lample, G. (2023a). *LLaMA: Open and Efficient Foundation Language Models.* arXiv:2302.13971. [arXiv:2302.13971](https://arxiv.org/abs/2302.13971)
- Touvron, H., Martin, L., Stone, K. et al. (2023b). *Llama 2: Open Foundation and Fine-Tuned Chat Models.* arXiv:2307.09288. [arXiv:2307.09288](https://arxiv.org/abs/2307.09288)
- Llama Team, AI @ Meta (2024). *The Llama 3 Herd of Models.* arXiv:2407.21783. [arXiv:2407.21783](https://arxiv.org/abs/2407.21783)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

LLaMA ist Metas Familie offen veröffentlichter [[large-language-models|großer Sprachmodelle]]. Die ersten LLaMA-Modelle (7 bis 65 Milliarden Parameter, 2023) wurden ausschließlich auf öffentlich verfügbaren Daten mit 1 bis 1,4 Billionen Token trainiert; LLaMA-13B übertraf GPT-3 mit 175 Milliarden Parametern auf den meisten Benchmarks und zeigte, dass kleinere, länger trainierte Modelle in der Inferenz günstiger sind (Touvron et al., 2023a). Llama 2 (7 bis 70 Milliarden) ergänzte 40 % mehr Trainingsdaten, einen verdoppelten Kontext von 4.096 Token und mit RLHF ausgerichtete Chat-Versionen, freigegeben für Forschung und kommerzielle Nutzung (Touvron et al., 2023b). Llama 3.1 (8, 70 und 405 Milliarden) wurde auf 15,6 Billionen Token mit einem Kontext von bis zu 128.000 Token trainiert, unterstützt acht Sprachen und Tool-Nutzung und erreichte bei vielen Aufgaben eine mit GPT-4 vergleichbare Qualität (Llama Team, 2024).

### Funktionsweise

```text
Vortrainingsdaten: öffentliches Web (CommonCrawl, C4), Code, Wikipedia, Bücher, arXiv, StackExchange …
 ▼ BPE-Tokenisierung
Decoder-only-Transformer mit
   Pre-Normalisierung (RMSNorm) · SwiGLU-Aktivierung · Rotary Position Embeddings (RoPE)
   + Grouped-Query Attention für größere Modelle (Llama 2 34B/70B, Llama 3)
 ▼ Vorhersage des nächsten Tokens auf Billionen Token (AdamW, Cosine-Lernratenplan)
 ▼ Post-Training: SFT → RLHF (Llama 2: Rejection Sampling + PPO) / SFT + Rejection Sampling + DPO (Llama 3)
 ▼ veröffentlichte Gewichte: Basis- und Chat-/Instruct-Modelle, dazu Sicherheitsklassifikatoren (Llama Guard 3)
```

#### 1. Rechenoptimal für die Inferenz trainieren

Skalierungsgesetze zeigen, wie ein festes Trainingsbudget zwischen Modellgröße und Daten aufgeteilt wird, berücksichtigen aber nicht die Kosten des Betriebs (Touvron et al., 2023a). LLaMA zielt stattdessen auf die beste Leistung bei gegebenem Inferenzbudget, indem kleinere Modelle auf mehr Token als üblich trainiert werden: Die Autoren fanden, dass sich ein Modell mit 7 Milliarden Parametern auch nach 1 Billion Token noch verbesserte, obwohl frühere Empfehlungen für ein Modell mit 10 Milliarden etwa 200 Milliarden Token nannten. Die Modelle mit 33 und 65 Milliarden Parametern wurden auf 1,4 Billionen Token trainiert; das Training des 65B-Modells dauerte etwa 21 Tage auf 2.048 A100-GPUs bei etwa 380 Token pro Sekunde und GPU (Touvron et al., 2023a). Das Skalierungsverhalten behandelt [[large-language-models|Große Sprachmodelle]].

#### 2. Daten

Das erste LLaMA nutzte nur öffentlich verfügbare Daten: überwiegend englisches CommonCrawl und C4, dazu Code von GitHub, Wikipedia in 20 Sprachen, die Buchkorpora Gutenberg und Books3, arXiv und StackExchange (Touvron et al., 2023a). Llama 2 wurde auf 2 Billionen Token mit gründlicherer Bereinigung trainiert und ließ Daten von Websites weg, die bekanntermaßen viele personenbezogene Informationen enthalten (Touvron et al., 2023b). Llama 3 nutzte einen mehrsprachigen Korpus aus etwa 15 Billionen Token, gegenüber 1,8 Billionen für Llama 2 (Llama Team, 2024). Rechtsfragen zu Trainingsdaten behandelt [[copyright-and-ai-training-data|Urheberrecht und KI-Trainingsdaten]].

#### 3. Architektur

LLaMA ist ein Decoder-only-Transformer ([[attention-and-transformers|Attention und Transformer]]) mit drei Änderungen gegenüber dem ursprünglichen Entwurf: Pre-Normalisierung der Eingabe jeder Teilschicht mit RMSNorm für stabiles Training, SwiGLU-Aktivierung statt ReLU und Rotary Position [[embeddings|Embeddings]] (RoPE) statt absoluter Positionen (Touvron et al., 2023a). Llama 2 ergänzt Grouped-Query Attention in den Modellen mit 34 und 70 Milliarden Parametern, um die Inferenz besser skalierbar zu machen (Touvron et al., 2023b). Für Llama 3 blieb das Team bewusst bei einem gewöhnlichen dichten Transformer statt eines Mixture-of-Experts-Modells, um das Training stabil zu halten, mit dem größten Modell bei 405 Milliarden Parametern (Llama Team, 2024).

#### 4. Post-Training und Sicherheit

Llama 2-Chat wurde mit überwachten Beispielen und anschließend mit Reinforcement Learning from Human Feedback feinjustiert, mit zwei Reward-Modellen für Hilfsbereitschaft und Sicherheit sowie Rejection Sampling und Proximal Policy Optimization; eine Technik namens Ghost Attention hält Systemanweisungen über mehrere Gesprächsrunden wirksam (Touvron et al., 2023b). Llama 3 ersetzte PPO durch Runden aus überwachtem Fine-Tuning, Rejection Sampling und Direct Preference Optimization und wurde zusammen mit Llama Guard 3 veröffentlicht, einem Klassifikator für die Sicherheit von Ein- und Ausgaben (Llama Team, 2024). Die Alignment-Verfahren erklärt [[llm-alignment|LLM-Alignment]], Sicherheitsklassifikatoren [[llm-guardrails|LLM-Guardrails]].

#### 5. Fähigkeiten und Veröffentlichungen

LLaMA-65B war konkurrenzfähig mit Chinchilla-70B und PaLM-540B (Touvron et al., 2023a). Llama 2-Chat übertraf quelloffene Chat-Modelle auf den meisten getesteten Benchmarks und könnte nach den menschlichen Bewertungen der Autoren zu Hilfsbereitschaft und Sicherheit geschlossene Modelle ersetzen (Touvron et al., 2023b). Llama 3.1 unterstützt acht Sprachen (Englisch, Deutsch, Französisch, Italienisch, Portugiesisch, Hindi, Spanisch und Thai), Programmierung, Schlussfolgern und Tool-Nutzung, und das 405B-Modell erreichte bei vielen Aufgaben eine mit GPT-4 vergleichbare Qualität; alle drei Größen wurden unter der Llama 3 Community License veröffentlicht (Llama Team, 2024).

#### Herkunft und Varianten

[[meta|Meta]] AI gab die ersten LLaMA-Modelle im Februar 2023 an die Forschungsgemeinschaft frei, Llama 2 im Juli 2023 für Forschung und kommerzielle Nutzung und Llama 3.1 im Juli 2024 (Touvron et al., 2023a; 2023b; Llama Team, 2024). Experimente im Llama-3-Paper koppeln zudem Encoder für Bild, Video und Sprache an, siehe [[multimodal-models|Multimodale Modelle]]. Weil die Gewichte verfügbar sind, sind Llama-Modelle eine verbreitete Basis für Fine-Tuning mit Verfahren wie [[lora|LoRA]] und [[qlora|QLoRA]] und für den lokalen Betrieb ([[llm-adaptation|LLM-Anpassung]], [[quantisation|Quantisierung]]).

### Wann einsetzen

- Anwendungen, die ein LLM auf eigener Infrastruktur brauchen, etwa aus Gründen des Datenschutzes oder der Kosten ([[mlops-and-deployment|MLOps und Deployment]]).
- Fine-Tuning oder Anpassung eines Modells an eine Domäne, wofür offene Gewichte nötig sind ([[llm-adaptation|LLM-Anpassung]]).
- Forschung zu Verhalten, Bias oder Sicherheit von LLMs, für die Modellinterna zugänglich sein müssen (Touvron et al., 2023a).

### Stärken und Grenzen

**Stärken**
- Offene Gewichte in mehreren Größen, von Modellen für eine GPU bis zum Spitzenmaßstab (Llama Team, 2024).
- Kleinere, auf vielen Token trainierte Modelle liefern hohe Qualität je Inferenzkosten (Touvron et al., 2023a).
- Dokumentierte Trainingsdaten, Architektur und Sicherheitsarbeit (Touvron et al., 2023a; 2023b).

**Grenzen**
- Die Lizenzen enthalten Bedingungen; Llama 2 und 3 stehen unter eigenen Lizenzen von Meta statt einer üblichen Open-Source-Lizenz (Touvron et al., 2023b; Llama Team, 2024).
- Wie andere auf Webdaten trainierte LLMs können die Modelle Verzerrungen wiedergeben und toxische Inhalte erzeugen; die Autoren betonen, dass ihre Evaluationen nicht ausreichen, um alle Risiken zu verstehen (Touvron et al., 2023a).
- Llama 3 8B und 70B wurden auf mehrsprachigen Daten vortrainiert, waren zunächst aber für Englisch gedacht (Llama Team, 2024).

### Vergleich

| Generation | Größen | Trainingstoken | Kontext | Post-Training |
|---|---|---|---|---|
| LLaMA (2023) | 7B–65B | 1–1,4 Bio. | 2.048 | keines (Basismodelle) |
| Llama 2 (2023) | 7B–70B | 2 Bio. | 4.096 | SFT + RLHF (Rejection Sampling, PPO) |
| Llama 3.1 (2024) | 8B, 70B, 405B | 15,6 Bio. (405B) | bis 128K | SFT + Rejection Sampling + DPO |

Quellen: Touvron et al. (2023a; 2023b); Llama Team (2024). Der Kontext von 2.048 Token (2k) des ersten LLaMA stammt aus der Vergleichstabelle bei Touvron et al. (2023b). Andere Modellfamilien vergleichen [[large-language-models|Große Sprachmodelle]] und [[gpt|GPT]].

### In der Praxis

Llama-Modelle laufen typischerweise quantisiert auf lokalen GPUs oder werden über Modellkataloge in der Cloud bereitgestellt ([[cloud-ai-platforms|Cloud-KI-Plattformen]], [[quantisation|Quantisierung]]). Die Bewertung von Bias und Sicherheit bleibt Aufgabe der Betreibenden: LLaMAs eigene Analyse fand Verzerrungen in Kategorien wie Geschlecht, Religion und Alter ([[bias-in-nlp|Bias in NLP]]; Touvron et al., 2023a).

### Regulatorischer Kontext

Anbieter von KI-Modellen mit allgemeinem Verwendungszweck, die unter freien und quelloffenen Lizenzen veröffentlicht werden, haben nach dem [[eu-ai-act|EU AI Act]] geringere Pflichten, sofern das Modell kein systemisches Risiko hat; ob Llamas Lizenz darunter fällt, ist eine Rechtsfrage jenseits dieser Notiz.

### Merksatz

Die Llama-Familie zeigte, dass offen veröffentlichte, vergleichsweise kleine Decoder-only-Transformer, trainiert auf vielen Token öffentlicher Daten, deutlich größere geschlossene Modelle erreichen können; spätere Generationen ergänzten Alignment mit RLHF oder DPO, langen Kontext, Mehrsprachigkeit und Spitzengröße.

### Quellen

- Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.-A., Lacroix, T., Rozière, B., Goyal, N., Hambro, E., Azhar, F., Rodriguez, A., Joulin, A., Grave, E. & Lample, G. (2023a). *LLaMA: Open and Efficient Foundation Language Models.* arXiv:2302.13971. [arXiv:2302.13971](https://arxiv.org/abs/2302.13971)
- Touvron, H., Martin, L., Stone, K. et al. (2023b). *Llama 2: Open Foundation and Fine-Tuned Chat Models.* arXiv:2307.09288. [arXiv:2307.09288](https://arxiv.org/abs/2307.09288)
- Llama Team, AI @ Meta (2024). *The Llama 3 Herd of Models.* arXiv:2407.21783. [arXiv:2407.21783](https://arxiv.org/abs/2407.21783)
