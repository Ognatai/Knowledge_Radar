---
title_en: LLM Guardrails and Red Teaming
title_de: LLM-Guardrails und Red Teaming
entity_type: Method
aliases:
- LLM guardrails
- Guardrails
- Red teaming
- Red Teaming
- AI red teaming
sources:
- https://arxiv.org/abs/2202.03286
- https://arxiv.org/abs/2209.07858
- https://arxiv.org/abs/2312.06674
- https://arxiv.org/abs/2310.10501
- https://genai.owasp.org/llm-top-10/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Red teaming deliberately attacks an LLM application before and during deployment to find harmful or unwanted behaviour, either with human testers or with another language model that generates test cases (Ganguli et al., 2022; Perez et al., 2022). Guardrails are runtime controls around the model that check inputs and outputs and steer the dialogue: classifiers such as [[llama|Llama]] Guard label prompts and responses against a risk taxonomy, and toolkits such as NeMo Guardrails add programmable rails for topics, moderation, fact-checking and hallucination outside the model (Inan et al., 2023; Rebedea et al., 2023). Both complement alignment training: red teaming finds the failures, guardrails catch some of them in production, and neither is complete. The OWASP Top 10 for LLM applications lists the main security risks they address (OWASP, 2025).

### How it works

```text
risk taxonomy and threat model (harms, OWASP risks, domain rules)
 ▼
red teaming: human attackers + LM-generated test cases → classify replies → findings
 ▼
mitigations: alignment / fine-tuning · system prompt · guardrails · tool permissions
 ▼
runtime: input rail → dialogue / topical rails → LLM → output rail (+ fact-check) → user
 ▼
monitoring of flagged traffic → new test cases → repeat
```

#### 1. Human red teaming

Ganguli et al. (2022) red-teamed models of 2.7, 13 and 52 billion parameters in four variants: a plain language model, a model prompted to be helpful, honest and harmless, a model using rejection sampling, and a model trained with reinforcement learning from human feedback (RLHF). RLHF models became harder to red team as they grew, while the other three variants stayed roughly flat with scale. The authors released 38,961 red team attacks, whose harmful outputs ranged from offensive language to subtle, non-violent unethical behaviour, and documented their instructions and statistical methods to help establish shared norms (Ganguli et al., 2022). Alignment methods such as RLHF are covered in [[llm-alignment|LLM alignment]].

#### 2. Automated red teaming with language models

Human-written test cases are expensive and limited in number and diversity. Perez et al. (2022) therefore let one language model generate test cases for a target model and scored the replies with a classifier for offensive content, with generation methods ranging from zero-shot prompting to reinforcement learning. Against a 280-billion-parameter chatbot they found tens of thousands of offensive replies, groups of people the chatbot discussed offensively, cases where it gave real personal and hospital phone numbers as its own contact details, leakage of private training data and harms that only emerge over several turns (Perez et al., 2022). They describe the approach as one tool among several. Bias found this way is discussed in [[bias-in-nlp|bias in NLP]] and measured with [[fairness-metrics|fairness metrics]].

#### 3. Input and output classifiers

A safeguard model classifies both the user's prompt and the model's response. Llama Guard is a Llama 2 7B model instruction-tuned on a small, high-quality dataset to classify prompts and responses against a safety risk taxonomy; it matches or exceeds existing moderation tools on the OpenAI Moderation Evaluation dataset and ToxicChat, and users can adapt the taxonomy and output format through further tuning or zero- and few-shot prompting (Inan et al., 2023). Its weights were released. Such classifiers can be placed before the model (to block malicious requests) and after it (to block harmful outputs).

#### 4. Programmable rails

NeMo Guardrails adds rails at runtime, outside the model, so that they can be defined and inspected without retraining and work with different LLM providers (Rebedea et al., 2023). Topical rails control the dialogue: developers describe flows in the modelling language Colang, and the runtime first maps each user message to a canonical form by similarity-based few-shot prompting, then follows a matching flow or lets the LLM decide the next step, and finally generates the bot message conditioned on that step, so that, for example, political questions are deflected (Rebedea et al., 2023). Execution rails are custom actions that monitor input and output: a fact-checking rail asks an LLM whether the response is entailed by the retrieved evidence, a hallucination rail compares several sampled answers for consistency in the style of SelfCheckGPT, and moderation rails check the input for jailbreak attempts and the output for harmful content before it is returned (Rebedea et al., 2023). The checks correspond to methods in [[hallucination-detection|hallucination detection]] and [[natural-language-inference|natural language inference]].

#### 5. Security risks to test and guard

The OWASP Top 10 for LLM applications (2025) names prompt injection, sensitive information disclosure, supply chain, data and model poisoning, improper output handling, excessive agency, system prompt leakage, vector and embedding weaknesses, misinformation and unbounded consumption (OWASP, 2025). Red-team plans and guardrails can be organised along these categories; prompt injection is covered in [[prompt-injection|prompt injection]], and excessive agency matters most for tool-using agents ([[agentic-ai|agentic AI]]).

#### Origin and variants

For language models, Perez et al. (2022) and Ganguli et al. (2022) described automated and human red teaming in detail. Classifier-based safeguards such as Llama Guard and rail toolkits such as NeMo Guardrails followed in 2023 (Inan et al., 2023; Rebedea et al., 2023). Cloud platforms ship their own content filters, see [[cloud-ai-platforms|cloud AI platforms]].

### When to use it

- Before releasing any user-facing LLM application, and again after model or prompt changes (Ganguli et al., 2022; Perez et al., 2022).
- When an assistant must stay within a defined scope, such as a customer service bot that should not discuss unrelated topics (Rebedea et al., 2023).
- When outputs must be grounded in retrieved documents, as in [[retrieval-augmented-generation|RAG]] systems for regulated domains (Rebedea et al., 2023).

### Strengths and limitations

**Strengths**
- Automated red teaming finds many failure cases cheaply and covers more variety than hand-written tests (Perez et al., 2022).
- Runtime rails are independent of the model, interpretable and changeable without retraining (Rebedea et al., 2023).
- Safeguard classifiers can be adapted to an organisation's own taxonomy (Inan et al., 2023).

**Limitations**
- Red teaming only finds what testers or generators think of; Perez et al. (2022) call it one tool among several.
- Classifiers and LLM-based rails are models themselves and can be wrong or attacked.
- Extra rails add latency and cost, for example the repeated sampling of the hallucination rail (Rebedea et al., 2023).

### Comparison

| Measure | When | What it does | Example |
|---|---|---|---|
| Alignment training | before deployment | changes the model's behaviour | [[llm-alignment\|RLHF, DPO]] |
| Red teaming | before and during deployment | finds failures | Ganguli et al. (2022), Perez et al. (2022) |
| Input / output classifier | at runtime | blocks unsafe prompts or responses | Llama Guard |
| Programmable rails | at runtime | steers dialogue, checks facts | NeMo Guardrails |
| Evaluation sets | in CI and [[monitoring-and-alerting\|monitoring]] | measures quality over versions | [[llm-evaluation\|LLM evaluation]] |

Sources: Ganguli et al. (2022); Perez et al. (2022); Inan et al. (2023); Rebedea et al. (2023).

### In practice

Red-team findings become regression test cases that run before every release ([[regression-testing|regression testing]]). Guardrail decisions are logged and traced so that false positives and missed cases can be reviewed ([[llm-observability-and-tracing|LLM observability and tracing]]). For agents, the strongest guardrail is often limiting which tools can be called and requiring approval for actions with side effects ([[agent-frameworks|agent frameworks]]).

### Regulatory context

The [[eu-ai-act|EU AI Act]] requires providers of general-purpose AI models with systemic risk to conduct and document adversarial testing of the model. Organisational responsibilities for such measures are discussed in [[responsible-ai|responsible AI]].

### Key takeaway

Red teaming finds harmful behaviour by attacking the system with people and generated test cases; guardrails check inputs and outputs and steer the dialogue at runtime; together with alignment and evaluation they reduce, but do not remove, the risks listed in the OWASP Top 10 for LLM applications.

### Sources

- Perez, E., Huang, S., Song, F., Cai, T., Ring, R., Aslanides, J., Glaese, A., McAleese, N. & Irving, G. (2022). *Red Teaming Language Models with Language Models.* arXiv:2202.03286. [arXiv](https://arxiv.org/abs/2202.03286)
- Ganguli, D., Lovitt, L. et al. (2022). *Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned.* arXiv:2209.07858. [arXiv](https://arxiv.org/abs/2209.07858)
- Inan, H., Upasani, K., Chi, J., Rungta, R., Iyer, K., Mao, Y., Tontchev, M., Hu, Q., Fuller, B., Testuggine, D. & Khabsa, M. (2023). *Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations.* arXiv:2312.06674. [arXiv](https://arxiv.org/abs/2312.06674)
- Rebedea, T., Dinu, R., Sreedhar, M., Parisien, C. & Cohen, J. (2023). *NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails.* EMNLP 2023 System Demonstrations. [arXiv](https://arxiv.org/abs/2310.10501)
- OWASP (2025). *OWASP Top 10 for LLM Applications 2025.* OWASP GenAI Security Project. [genai.owasp.org](https://genai.owasp.org/llm-top-10/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Red Teaming greift eine LLM-Anwendung vor und während des Betriebs gezielt an, um schädliches oder unerwünschtes Verhalten zu finden, entweder mit menschlichen Testerinnen und Testern oder mit einem weiteren Sprachmodell, das Testfälle erzeugt (Ganguli et al., 2022; Perez et al., 2022). Guardrails sind Kontrollen zur Laufzeit rund um das Modell, die Ein- und Ausgaben prüfen und den Dialog lenken: Klassifikatoren wie [[llama|Llama]] Guard bewerten Prompts und Antworten anhand einer Risikotaxonomie, und Toolkits wie NeMo Guardrails ergänzen außerhalb des Modells programmierbare Rails für Themen, Moderation, Faktenprüfung und Halluzinationen (Inan et al., 2023; Rebedea et al., 2023). Beides ergänzt das Alignment-Training: Red Teaming findet die Fehler, Guardrails fangen einen Teil davon im Betrieb ab, und keines ist vollständig. Die OWASP Top 10 für LLM-Anwendungen nennen die wichtigsten Sicherheitsrisiken, auf die sie zielen (OWASP, 2025).

### Funktionsweise

```text
Risikotaxonomie und Bedrohungsmodell (Schäden, OWASP-Risiken, Domänenregeln)
 ▼
Red Teaming: menschliche Angreifende + vom Sprachmodell erzeugte Testfälle → Antworten klassifizieren → Befunde
 ▼
Gegenmaßnahmen: Alignment / Fine-Tuning · System-Prompt · Guardrails · Tool-Berechtigungen
 ▼
Laufzeit: Input Rail → Dialog-/Themen-Rails → LLM → Output Rail (+ Faktenprüfung) → Nutzende
 ▼
Monitoring markierter Anfragen → neue Testfälle → Wiederholung
```

#### 1. Red Teaming durch Menschen

Ganguli et al. (2022) testeten Modelle mit 2,7, 13 und 52 Milliarden Parametern in vier Varianten: ein reines Sprachmodell, ein Modell mit Prompt für hilfreiche, ehrliche und harmlose Antworten, ein Modell mit Rejection Sampling und ein Modell, das mit Reinforcement Learning from Human Feedback (RLHF) trainiert wurde. RLHF-Modelle wurden mit wachsender Größe schwerer anzugreifen, während die anderen drei Varianten über die Größen etwa gleich blieben. Die Autorinnen und Autoren veröffentlichten 38.961 Red-Team-Angriffe, deren schädliche Ausgaben von beleidigender Sprache bis zu subtilem, nicht gewalttätigem unethischem Verhalten reichten, und dokumentierten ihre Anleitungen und statistischen Methoden, um gemeinsame Normen zu fördern (Ganguli et al., 2022). Alignment-Verfahren wie RLHF behandelt [[llm-alignment|LLM-Alignment]].

#### 2. Automatisiertes Red Teaming mit Sprachmodellen

Von Menschen geschriebene Testfälle sind teuer und in Zahl und Vielfalt begrenzt. Perez et al. (2022) ließen daher ein Sprachmodell Testfälle für ein Zielmodell erzeugen und bewerteten die Antworten mit einem Klassifikator für beleidigende Inhalte, wobei die Erzeugung von Zero-Shot-Prompting bis zu Reinforcement Learning reichte. Bei einem Chatbot mit 280 Milliarden Parametern fanden sie Zehntausende beleidigender Antworten, Personengruppen, über die der Chatbot beleidigend sprach, Fälle, in denen er echte private Telefonnummern und Krankenhausnummern als eigene Kontaktdaten ausgab, das Durchsickern privater Trainingsdaten sowie Schäden, die erst über mehrere Gesprächsrunden entstehen (Perez et al., 2022). Sie beschreiben den Ansatz als ein Werkzeug unter mehreren. So gefundene Verzerrungen behandelt [[bias-in-nlp|Bias in NLP]], gemessen werden sie mit [[fairness-metrics|Fairness-Metriken]].

#### 3. Klassifikatoren für Ein- und Ausgaben

Ein Schutzmodell klassifiziert sowohl den Prompt der Nutzenden als auch die Antwort des Modells. Llama Guard ist ein Llama-2-7B-Modell, das auf einem kleinen, hochwertigen Datensatz per Instruction Tuning darauf trainiert wurde, Prompts und Antworten anhand einer Taxonomie von Sicherheitsrisiken zu klassifizieren; es erreicht oder übertrifft bestehende Moderationswerkzeuge auf dem OpenAI Moderation Evaluation Dataset und ToxicChat, und Nutzende können Taxonomie und Ausgabeformat durch weiteres Tuning oder Zero- und Few-Shot-Prompting anpassen (Inan et al., 2023). Die Gewichte wurden veröffentlicht. Solche Klassifikatoren können vor dem Modell (um bösartige Anfragen zu blockieren) und danach (um schädliche Ausgaben zu blockieren) stehen.

#### 4. Programmierbare Rails

NeMo Guardrails ergänzt Rails zur Laufzeit außerhalb des Modells, sodass sie ohne erneutes Training festgelegt und geprüft werden können und mit verschiedenen LLM-Anbietern funktionieren (Rebedea et al., 2023). Themen-Rails (Topical Rails) steuern den Dialog: Entwicklerinnen und Entwickler beschreiben Abläufe in der Modellierungssprache Colang, und die Laufzeitumgebung ordnet jede Nachricht zunächst per ähnlichkeitsbasiertem Few-Shot-Prompting einer kanonischen Form zu, folgt dann einem passenden Ablauf oder lässt das LLM den nächsten Schritt bestimmen und erzeugt schließlich die Antwort abhängig von diesem Schritt, sodass etwa politische Fragen abgelenkt werden (Rebedea et al., 2023). Execution Rails sind eigene Aktionen, die Ein- und Ausgaben überwachen: Eine Rail zur Faktenprüfung fragt ein LLM, ob die Antwort aus den abgerufenen Belegen folgt, eine Halluzinations-Rail vergleicht mehrere erzeugte Antworten auf Übereinstimmung nach Art von SelfCheckGPT, und Moderations-Rails prüfen die Eingabe auf Jailbreak-Versuche und die Ausgabe auf schädliche Inhalte, bevor sie zurückgegeben wird (Rebedea et al., 2023). Die Prüfungen entsprechen Verfahren aus der [[hallucination-detection|Halluzinationserkennung]] und der [[natural-language-inference|Natural Language Inference]].

#### 5. Zu prüfende und abzusichernde Sicherheitsrisiken

Die OWASP Top 10 für LLM-Anwendungen (2025) nennen Prompt Injection, Offenlegung sensibler Informationen, Lieferkette, Daten- und Modellvergiftung, unsachgemäße Verarbeitung von Ausgaben, übermäßige Handlungsbefugnis (Excessive Agency), Offenlegung des System-Prompts, Schwächen von Vektoren und [[embeddings|Embeddings]], Fehlinformation und unbegrenzten Ressourcenverbrauch (OWASP, 2025). Red-Team-Pläne und Guardrails lassen sich entlang dieser Kategorien ordnen; Prompt Injection behandelt [[prompt-injection|Prompt Injection]], und übermäßige Handlungsbefugnis ist vor allem bei Agenten mit Tools relevant ([[agentic-ai|Agentic AI]]).

#### Herkunft und Varianten

Für Sprachmodelle beschrieben Perez et al. (2022) und Ganguli et al. (2022) automatisiertes und menschliches Red Teaming ausführlich. Schutzklassifikatoren wie Llama Guard und Rail-Toolkits wie NeMo Guardrails folgten 2023 (Inan et al., 2023; Rebedea et al., 2023). Cloud-Plattformen liefern eigene Inhaltsfilter mit, siehe [[cloud-ai-platforms|Cloud-KI-Plattformen]].

### Wann einsetzen

- Vor dem Release jeder LLM-Anwendung für Nutzende und erneut nach Änderungen an Modell oder Prompt (Ganguli et al., 2022; Perez et al., 2022).
- Wenn ein Assistent in einem festgelegten Rahmen bleiben muss, etwa ein Kundenservice-Bot, der keine fremden Themen besprechen soll (Rebedea et al., 2023).
- Wenn Ausgaben in abgerufenen Dokumenten verankert sein müssen, etwa bei RAG-Systemen in regulierten Bereichen (Rebedea et al., 2023).

### Stärken und Grenzen

**Stärken**
- Automatisiertes Red Teaming findet viele Fehlerfälle günstig und deckt mehr Vielfalt ab als handgeschriebene Tests (Perez et al., 2022).
- Rails zur Laufzeit sind unabhängig vom Modell, nachvollziehbar und ohne erneutes Training änderbar (Rebedea et al., 2023).
- Schutzklassifikatoren lassen sich an die eigene Taxonomie einer Organisation anpassen (Inan et al., 2023).

**Grenzen**
- Red Teaming findet nur, woran Testende oder Generatoren denken; Perez et al. (2022) nennen es ein Werkzeug unter mehreren.
- Klassifikatoren und LLM-basierte Rails sind selbst Modelle und können irren oder angegriffen werden.
- Zusätzliche Rails erhöhen Latenz und Kosten, etwa durch das wiederholte Sampling der Halluzinations-Rail (Rebedea et al., 2023).

### Vergleich

| Maßnahme | Wann | Was sie tut | Beispiel |
|---|---|---|---|
| Alignment-Training | vor dem Betrieb | verändert das Verhalten des Modells | [[llm-alignment\|RLHF, DPO]] |
| Red Teaming | vor und während des Betriebs | findet Fehler | Ganguli et al. (2022), Perez et al. (2022) |
| Ein-/Ausgabeklassifikator | zur Laufzeit | blockiert unsichere Prompts oder Antworten | Llama Guard |
| Programmierbare Rails | zur Laufzeit | lenkt den Dialog, prüft Fakten | NeMo Guardrails |
| Evaluationssets | in CI und [[monitoring-and-alerting\|Monitoring]] | misst Qualität über Versionen | [[llm-evaluation\|LLM-Evaluation]] |

Quellen: Ganguli et al. (2022); Perez et al. (2022); Inan et al. (2023); Rebedea et al. (2023).

### In der Praxis

Befunde aus dem Red Teaming werden zu Regressionstestfällen, die vor jedem Release laufen ([[regression-testing|Regressionstests]]). Entscheidungen der Guardrails werden protokolliert und nachverfolgt, damit Fehlalarme und übersehene Fälle geprüft werden können ([[llm-observability-and-tracing|LLM-Observability und Tracing]]). Bei Agenten ist die wirksamste Guardrail oft, die aufrufbaren Tools zu begrenzen und für Aktionen mit Nebenwirkungen eine Freigabe zu verlangen ([[agent-frameworks|Agent-Frameworks]]).

### Regulatorischer Kontext

Der [[eu-ai-act|EU AI Act]] verlangt von Anbietern von KI-Modellen mit allgemeinem Verwendungszweck und systemischem Risiko, Angriffstests (Adversarial Testing) des Modells durchzuführen und zu dokumentieren. Organisatorische Zuständigkeiten für solche Maßnahmen behandelt [[responsible-ai|Responsible AI]].

### Merksatz

Red Teaming findet schädliches Verhalten, indem es das System mit Menschen und erzeugten Testfällen angreift; Guardrails prüfen Ein- und Ausgaben und lenken den Dialog zur Laufzeit; zusammen mit Alignment und Evaluation verringern sie die in den OWASP Top 10 für LLM-Anwendungen genannten Risiken, beseitigen sie aber nicht.

### Quellen

- Perez, E., Huang, S., Song, F., Cai, T., Ring, R., Aslanides, J., Glaese, A., McAleese, N. & Irving, G. (2022). *Red Teaming Language Models with Language Models.* arXiv:2202.03286. [arXiv](https://arxiv.org/abs/2202.03286)
- Ganguli, D., Lovitt, L. et al. (2022). *Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned.* arXiv:2209.07858. [arXiv](https://arxiv.org/abs/2209.07858)
- Inan, H., Upasani, K., Chi, J., Rungta, R., Iyer, K., Mao, Y., Tontchev, M., Hu, Q., Fuller, B., Testuggine, D. & Khabsa, M. (2023). *Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations.* arXiv:2312.06674. [arXiv](https://arxiv.org/abs/2312.06674)
- Rebedea, T., Dinu, R., Sreedhar, M., Parisien, C. & Cohen, J. (2023). *NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails.* EMNLP 2023 System Demonstrations. [arXiv](https://arxiv.org/abs/2310.10501)
- OWASP (2025). *OWASP Top 10 for LLM Applications 2025.* OWASP GenAI Security Project. [genai.owasp.org](https://genai.owasp.org/llm-top-10/)
