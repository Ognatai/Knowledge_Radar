---
title_en: Prompt Injection
title_de: Prompt Injection
entity_type: Concept
sources:
- https://arxiv.org/abs/2302.12173
- https://arxiv.org/abs/2306.05499
- https://arxiv.org/abs/2403.02691
- https://arxiv.org/abs/2610.05266
- https://arxiv.org/abs/2610.11634
- https://arxiv.org/abs/2610.06401
- https://arxiv.org/abs/2610.06966
- https://arxiv.org/abs/2610.08571
- https://arxiv.org/abs/2610.17457
- https://arxiv.org/abs/2610.18408
- https://arxiv.org/abs/2610.19452
- https://arxiv.org/abs/2610.20907
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR
Prompt injection is an attack on applications built on [[large-language-models|large language models]]: text crafted by an attacker overrides the instructions the application gives the model, so that the model follows the attacker instead (Greshake et al., 2023; Liu et al., 2023). In indirect prompt injection, the attacker does not talk to the model at all but places the instructions in data the application retrieves, such as web pages, emails or tool outputs; for [[agentic-ai|agents]] that act on such data, this can lead to harmful actions and data theft (Greshake et al., 2023; Zhan et al., 2024).

### How it works

LLM-integrated applications put their own instructions, the user's request and external data into one prompt. The model receives all of it as text and has no reliable way to tell which part is an instruction and which part is data; LLM-integrated applications therefore blur the line between data and instructions (Greshake et al., 2023).

```text
application instructions ─┐
user request ─────────────┼─▶ one prompt ─▶ LLM ─▶ answer or tool call
retrieved data ───────────┘        ▲
  (web page, email, tool output)   └─ injected instructions arrive here
```

#### 1. Direct and indirect injection
In direct prompt injection, a user types instructions that override the application's original instructions and controls (Greshake et al., 2023). Greshake et al. (2023) showed that the attacker does not need a direct interface: indirect prompt injection places prompts in data that the application is likely to retrieve, and the application processes them when it reads that data. They demonstrated this against real systems, including Bing's GPT-4-powered chat and code-completion engines, and showed that retrieved prompts can act like arbitrary code execution, manipulate the application's functionality and control whether and how other [[apis|APIs]] are called.

#### 2. Building an injection
Liu et al. (2023) borrow from traditional web injection attacks such as SQL injection. Their black-box attack HouYi builds the injected text from three components: a framework component that blends in with the application's own prompt, a separator component that makes the model treat what follows as a new context, and a disruptor component that carries the attacker's actual objective. HouYi uses an LLM to infer what the target application does and adapts the injected prompt to it. Applied to 36 real LLM-integrated applications, it found 31 of them susceptible; consequences included unrestricted use of the application's LLM and theft of its prompt, and 10 vendors, among them Notion, confirmed the findings (Liu et al., 2023).

#### 3. Injection into agents
Agents call tools and read their results, which gives injected instructions a way to trigger actions. The InjecAgent benchmark (Zhan et al., 2024) contains 1,054 test cases with 17 user tools that fetch content an attacker can modify and 62 attacker tools that perform harmful actions. It distinguishes two attack goals: direct harm to the user and exfiltration of private data, for example sending it on with an email tool. Of 30 evaluated agents, a ReAct-prompted GPT-4 agent followed the injected instructions in 24% of the cases; reinforcing the injected instructions with a "hacking prompt" nearly doubled that rate. As agents combine more capability units such as tools, [[mcp-and-related-protocols|MCP servers]] and skills, the number of possible carriers for injected instructions grows (Zheng et al., 2026).

#### 4. Manipulating decisions instead of actions
An injection does not have to trigger an obviously harmful action. Wang et al. (2026) show that in proactive personal agents, a provider that controls only the content about its own product can steer which recommendation the agent makes, without access to the user's private context, without compromising the agent and without extra permissions. Across three agent environments and six simulated user models, such content increased how often users authorised the provider's target in every tested combination, by up to 77.4 percentage points.

#### 5. Defences
Defences fall into two groups (Zhan et al., 2024): black-box defences that need no access to the model's parameters, such as an extra prompt that warns the model of attacks or special delimiters around external content, and white-box defences that change the model, for example fine-tuning it on attack examples or separating prompts and data into two channels. Recent work illustrates the range:

- **Learned delimiters:** LTBD keeps the model's parameters unchanged and learns a small number of delimiters that mark which part of the input is a trusted user instruction and which part is untrusted external data (Zhao et al., 2026).
- **Training for invariance:** training-time defences reduce attack success but can degrade general capabilities, for example by making an agent skip a legitimate step that a tool output asks for. RAISED trains the model to behave on injected inputs as it does on the clean version of the same task and reports lower attack success without that loss of utility (Dhouib et al., 2026).
- **Control at the execution boundary:** APEX does not try to recognise attack patterns. It checks, at the point where an agent turns internal state into an external action, whether the effect is authorised by the trusted task and whether the information that leads to it is endorsed by that task (Zheng et al., 2026).
- **Detection:** classifiers can flag injected content before it reaches the model. On the RAG-PIBench benchmark of 4,876 examples from retrieval-augmented settings, a fine-tuned [[distilbert|DistilBERT]] detected injections best (F1 0.896), while simple [[information-retrieval|TF-IDF]] baselines remained competitive (Jaffal et al., 2026). Section 6 covers detectors in detail.

#### 6. Detecting injections
Detectors usually serve as a fast first filter: they screen inputs or tool outputs and send what they flag to a slower and more expensive second check, such as a second language model, so every false alarm costs one more check (Kale & Vishwanath, 2026). They read either the text, as fine-tuned classifiers such as Prompt Guard 2 or a prompted [[llm-as-a-judge|LLM judge]] do (Lan et al., 2026), or the model's own computation, such as hidden states, [[attention-and-transformers|attention]] patterns or role representations (Gupta & Tembey, 2026). Recent evaluations point to four pitfalls:

- **False alarms on benign content:** web pages contain many legitimate instructions, such as button labels and help text. The benchmark BrowseSafe++ pairs each of 38,675 attacked pages with the same page without the injection; most of its injections were observed on production websites. Even the prompted detector with the highest [[classification-metrics|F1]] falsely flagged 13.82–15.10% of benign pages, while BrowseSafe-Guard, a 0.8B-parameter detector trained on the pairs, reached 92.98–98.29 F1 at 1.35–7.40% false positives. The ranking of models also changed between the HTML, Markdown and accessibility-tree views of the same pages (Chen et al., 2026).
- **Shortcuts instead of injections:** in the standard evaluation of probes on hidden states, the position in the conversation and text lengths alone reach 0.91–0.98 AUROC without looking at the model. Adding matched negatives to the training data, namely the same moment of a clean run of the same task and harmless text in the injection's formatting, cut false alarms on injection-free conversations from 41–80% to 4–27% across six open models in applications seen during training (Kale & Vishwanath, 2026).
- **Presence is not success:** detectors trained to recognise that an injection is present, such as PIShield, separated unsuccessful attacks from benign inputs better than successful ones. Attention Tracker, which measures how far attention shifts away from the trusted instruction, separated successful attacks best (AUROC 0.949 on Qwen and 0.887 on Gemma) (Gupta & Tembey, 2026). Likewise, in 74.15% of the cases in which a model followed an injection on BrowseSafe++, the same model had flagged it in a separate detection test (Chen et al., 2026).
- **Scores are not decisions:** a deployed system must allow, block or escalate an input. On 47,611 held-out examples, a GPT-5.5 judge ranked attacks best (AUROC 0.897), ahead of Jev, a model trained for calibrated decisions (0.871), and Prompt Guard 2 with 86M and 22M parameters (0.757 and 0.714). Each gate reached a false-negative rate of at most 1% only when more than 91.8% of inputs were escalated to the reviewer, with 40.6–45.8% false positives; calibrated probabilities alone did not make the decisions reliable (Lan et al., 2026).

#### Origin and variants
Greshake et al. (2023) introduced indirect prompt injection and a taxonomy of its impacts, including data theft, worming and contamination of the information ecosystem. Liu et al. (2023) systematised injection attacks on deployed applications, and Zhan et al. (2024) provided a benchmark for tool-using agents. Later work targets specific settings such as [[retrieval-augmented-generation|retrieval-augmented generation]] (Jaffal et al., 2026) and proactive agents (Wang et al., 2026).

### When to use it
The topic matters wherever a model processes text that someone other than the user controls:

- Agents that browse the web, read emails or documents, or call tools whose output can contain attacker-controlled text (Greshake et al., 2023; Zhan et al., 2024).
- Applications that wrap their own prompt around user input and must protect that prompt and their LLM access (Liu et al., 2023).
- Retrieval-augmented systems whose retrieved passages may contain injected instructions (Jaffal et al., 2026).
- Agents that make recommendations or decisions based on third-party content (Wang et al., 2026).

### Strengths and limitations
What current defences achieve:
- Delimiter-based defences such as LTBD work without changing the model's parameters (Zhao et al., 2026).
- Training-based defences can reduce attack success while preserving utility if they keep the model's clean behaviour (Dhouib et al., 2026).
- Checks at the execution boundary apply independently of how an injection is built (Zheng et al., 2026).
- Small fine-tuned detectors can be accurate and cheap: BrowseSafe-Guard costs about $0.18 per 1,000 pages on a rented GPU, compared with $18.95–180.61 for frontier models (Chen et al., 2026).

Open problems:
- When Greshake et al. (2023) described indirect prompt injection, effective mitigations were lacking; defences built on handcrafted prompts remain brittle and vulnerable to adaptive attacks (Zhao et al., 2026).
- Training-based defences can shift the model's behaviour on benign tasks (Dhouib et al., 2026).
- Defences that recognise attack patterns fall behind as the carriers of injections multiply (Zheng et al., 2026).
- Manipulation of recommendations is hard to recognise as an attack, because no single action is obviously harmful (Wang et al., 2026).
- Fixed attack strings understate the risk: injections observed on websites succeeded on only 0.49–4.00% of tasks when replayed, but on 30.66–95.41% once revised from the agent's feedback (Chen et al., 2026).
- A detector that flags an injection does not show that the model resists it, and a high detection score does not show that the model was compromised (Chen et al., 2026; Gupta & Tembey, 2026).

### Comparison
| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Delimiters and warning prompts | Mark or warn about external content in the prompt; no access to model parameters needed (Zhan et al., 2024) | Applications on closed models |
| Learned delimiters (LTBD) | Learn the trust boundary instead of handcrafting it; model unchanged (Zhao et al., 2026) | Open models whose input [[embeddings\|embeddings]] can be extended |
| Training-based defences (RAISED) | Change the model so that injected content does not alter its behaviour (Dhouib et al., 2026) | Teams that fine-tune their own agent models |
| Execution-boundary control (APEX) | Authorise effects from the trusted task instead of detecting attacks (Zheng et al., 2026) | Agents that act through tools; see [[harness-engineering\|harness engineering]] |
| Injection detectors | Classify content or the model's internal state as benign or malicious before the model acts (Jaffal et al., 2026; Kale & Vishwanath, 2026) | A fast first filter in front of a second check; screening retrieved passages in RAG systems |

### In practice
Benchmarks such as InjecAgent measure how often an agent follows injected instructions (Zhan et al., 2024). For detectors, Jaffal et al. (2026) recommend comparing against strong lightweight baselines and keeping model development strictly separate from the final test set, because otherwise results look better than they are. Kale & Vishwanath (2026) recommend training injection monitors with clean runs of the same tasks and harmless look-alikes, and reporting a baseline without the model, a comparison against clean twins and the share of successful attacks stopped at a fixed false-alarm budget. Detection of injections and detection of successful attacks should be reported separately (Gupta & Tembey, 2026), and web detectors should be tested in every page view the agent uses (Chen et al., 2026). Defences are evaluated not only by attack success rate but also by whether they preserve the agent's usefulness on benign tasks (Dhouib et al., 2026).

### Regulatory context
The [[cyber-resilience-act|Cyber Resilience Act]] requires actively exploited vulnerabilities to be reported within 24 hours; prompt injection leading to code execution in an AI feature of a product is such a vulnerability. Under the [[nis2-directive|NIS2 Directive]], a prompt injection that leads to a data leak can be a significant incident. Article 15 of the [[eu-ai-act|EU AI Act]] requires high-risk AI systems to be resilient against attempts by unauthorised third parties to alter their use, outputs or performance by exploiting system vulnerabilities.

### Key takeaway
Language models do not separate instructions from data, so any text an application feeds them, including retrieved content and tool outputs, can carry instructions from an attacker.

### Sources
- Greshake, K. et al. (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.* AISec 2023. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)
- Liu, Y. et al. (2023). *Prompt Injection attack against LLM-integrated Applications.* [arXiv:2306.05499](https://arxiv.org/abs/2306.05499)
- Zhan, Q. et al. (2024). *InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents.* Findings of ACL 2024. [arXiv:2403.02691](https://arxiv.org/abs/2403.02691)
- Wang, R. et al. (2026). *Who Is Your Agent Serving? Provider-Side Indirect Prompt Injection in Proactive Agents.* [arXiv:2610.05266](https://arxiv.org/abs/2610.05266)
- Zhao, L. et al. (2026). *LTBD: Learnable Trust-Boundary Delimiters for Prompt Injection Defense.* [arXiv:2610.11634](https://arxiv.org/abs/2610.11634)
- Dhouib, M. et al. (2026). *RAISED: Self-Distillation for Robustness to Prompt Injection in LLM Agents.* [arXiv:2610.06401](https://arxiv.org/abs/2610.06401)
- Zheng, X. et al. (2026). *APEX: Active Protection at Execution Boundaries for LLM Agents.* [arXiv:2610.06966](https://arxiv.org/abs/2610.06966)
- Jaffal, N. O. et al. (2026). *RAG-PIBench: A Leakage-Aware Benchmark for Prompt-Injection Detection in Trustworthy RAG Systems.* [arXiv:2610.08571](https://arxiv.org/abs/2610.08571)
- Chen, Y. et al. (2026). *BrowseSafe++: Benchmarking Prompt Injection Detection Across Web Contexts, Languages, and Browser Views.* [arXiv:2610.17457](https://arxiv.org/abs/2610.17457)
- Kale, K. & Vishwanath, S. (2026). *Prompt-Injection Probes Learn the Conversation, Not Just the Injection.* [arXiv:2610.18408](https://arxiv.org/abs/2610.18408)
- Gupta, S. & Tembey, P. (2026). *Are You Reading the Right Thing? Rethinking Internal Signals for Prompt-Injection Detection.* [arXiv:2610.19452](https://arxiv.org/abs/2610.19452)
- Lan, Q. et al. (2026). *From Detection to Decision: Calibration and Deferral for Prompt-Injection Detection.* [arXiv:2610.20907](https://arxiv.org/abs/2610.20907)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Basis der angegebenen Quellen; sie kann unvollständig, veraltet oder fehlerhaft sein.

### TL;DR
Prompt Injection ist ein Angriff auf Anwendungen, die auf großen Sprachmodellen aufbauen: Von einem Angreifer gestalteter Text setzt die Anweisungen außer Kraft, die die Anwendung dem Modell gibt, sodass das Modell dem Angreifer folgt (Greshake et al., 2023; Liu et al., 2023). Bei Indirect Prompt Injection spricht der Angreifer gar nicht mit dem Modell, sondern legt die Anweisungen in Daten ab, die die Anwendung abruft, etwa Webseiten, E-Mails oder Tool-Ausgaben; bei [[agentic-ai|Agenten]], die auf solche Daten hin handeln, kann das zu schädlichen Aktionen und Datendiebstahl führen (Greshake et al., 2023; Zhan et al., 2024).

### Funktionsweise

LLM-basierte Anwendungen fügen ihre eigenen Anweisungen, die Anfrage des Nutzers und externe Daten zu einem Prompt zusammen. Das Modell erhält alles als Text und kann nicht zuverlässig unterscheiden, welcher Teil Anweisung und welcher Teil Daten ist; LLM-basierte Anwendungen verwischen daher die Grenze zwischen Daten und Anweisungen (Greshake et al., 2023).

```text
Anweisungen der Anwendung ─┐
Anfrage des Nutzers ───────┼─▶ ein Prompt ─▶ LLM ─▶ Antwort oder Tool-Aufruf
abgerufene Daten ──────────┘        ▲
  (Webseite, E-Mail, Tool-Ausgabe)  └─ eingeschleuste Anweisungen kommen hier an
```

#### 1. Direkte und indirekte Injection
Bei Direct Prompt Injection gibt ein Nutzer Anweisungen ein, die die ursprünglichen Anweisungen und Kontrollen der Anwendung außer Kraft setzen (Greshake et al., 2023). Greshake et al. (2023) zeigten, dass der Angreifer keine direkte Schnittstelle braucht: Indirect Prompt Injection platziert Prompts in Daten, die die Anwendung voraussichtlich abruft, und die Anwendung verarbeitet sie, sobald sie diese Daten liest. Sie demonstrierten das an realen Systemen, darunter der GPT-4-basierte Chat von Bing und Code-Completion-Engines, und zeigten, dass abgerufene Prompts wie die Ausführung beliebigen Codes wirken, die Funktionen der Anwendung manipulieren und steuern können, ob und wie andere [[apis|APIs]] aufgerufen werden.

#### 2. Aufbau einer Injection
Liu et al. (2023) orientieren sich an klassischen Web-Injection-Angriffen wie [[sql|SQL]] Injection. Ihr Black-Box-Angriff HouYi setzt den eingeschleusten Text aus drei Komponenten zusammen: einer Framework-Komponente, die sich in den Prompt der Anwendung einfügt, einer Separator-Komponente, die das Modell das Folgende als neuen Kontext behandeln lässt, und einer Disruptor-Komponente, die das eigentliche Ziel des Angreifers enthält. HouYi leitet mit einem LLM ab, was die Zielanwendung tut, und passt den eingeschleusten Prompt daran an. Angewandt auf 36 reale LLM-basierte Anwendungen erwiesen sich 31 als anfällig; zu den Folgen gehörten die uneingeschränkte Nutzung des LLM der Anwendung und der Diebstahl ihres Prompts, und 10 Anbieter, darunter Notion, bestätigten die Befunde (Liu et al., 2023).

#### 3. Injection in Agenten
Agenten rufen Tools auf und lesen deren Ergebnisse; damit können eingeschleuste Anweisungen Aktionen auslösen. Der Benchmark InjecAgent (Zhan et al., 2024) enthält 1.054 Testfälle mit 17 Nutzer-Tools, die von Angreifern veränderbare Inhalte abrufen, und 62 Angreifer-Tools, die schädliche Aktionen ausführen. Er unterscheidet zwei Angriffsziele: direkten Schaden für den Nutzer und das Abgreifen privater Daten, etwa durch Weiterleitung mit einem E-Mail-Tool. Von 30 untersuchten Agenten folgte ein mit [[react|ReAct]] gepromptetes GPT-4 in 24 % der Fälle den eingeschleusten Anweisungen; wurden diese mit einem „Hacking-Prompt“ verstärkt, verdoppelte sich die Rate nahezu. Je mehr Bausteine Agenten kombinieren, etwa Tools, [[mcp-and-related-protocols|MCP-Server]] und Skills, desto mehr mögliche Träger für eingeschleuste Anweisungen gibt es (Zheng et al., 2026).

#### 4. Entscheidungen statt Aktionen manipulieren
Eine Injection muss keine offensichtlich schädliche Aktion auslösen. Wang et al. (2026) zeigen, dass bei proaktiven persönlichen Agenten ein Anbieter, der nur die Inhalte zu seinem eigenen Produkt kontrolliert, steuern kann, welche Empfehlung der Agent gibt – ohne Zugriff auf den privaten Kontext des Nutzers, ohne den Agenten zu kompromittieren und ohne zusätzliche Berechtigungen. In drei Agentenumgebungen mit sechs simulierten Nutzermodellen erhöhten solche Inhalte in jeder getesteten Kombination, wie oft Nutzer das Ziel des Anbieters freigaben, um bis zu 77,4 Prozentpunkte.

#### 5. Abwehr
Abwehrmaßnahmen lassen sich in zwei Gruppen einteilen (Zhan et al., 2024): Black-Box-Abwehr, die keinen Zugriff auf die Modellparameter braucht, etwa ein zusätzlicher Prompt, der das Modell vor Angriffen warnt, oder spezielle Begrenzer um externe Inhalte, und White-Box-Abwehr, die das Modell verändert, zum Beispiel durch Fine-Tuning mit Angriffsbeispielen oder durch Trennung von Prompts und Daten in zwei Kanäle. Neuere Arbeiten zeigen die Bandbreite:

- **Gelernte Begrenzer:** LTBD lässt die Modellparameter unverändert und lernt eine kleine Zahl von Begrenzern, die markieren, welcher Teil der Eingabe eine vertrauenswürdige Nutzeranweisung und welcher Teil unvertrauenswürdige externe Daten sind (Zhao et al., 2026).
- **Training auf Invarianz:** Abwehr durch Training senkt den Angriffserfolg, kann aber allgemeine Fähigkeiten verschlechtern, etwa wenn ein Agent einen legitimen Schritt auslässt, den eine Tool-Ausgabe verlangt. RAISED trainiert das Modell, sich bei manipulierten Eingaben so zu verhalten wie bei der unveränderten Fassung derselben Aufgabe, und berichtet geringeren Angriffserfolg ohne diesen Verlust an Nützlichkeit (Dhouib et al., 2026).
- **Kontrolle an der Ausführungsgrenze:** APEX versucht nicht, Angriffsmuster zu erkennen. Es prüft an der Stelle, an der ein Agent internen Zustand in eine externe Aktion umsetzt, ob die Wirkung durch die vertrauenswürdige Aufgabe autorisiert ist und ob die dorthin führenden Informationen von dieser Aufgabe gedeckt sind (Zheng et al., 2026).
- **Erkennung:** Klassifikatoren können eingeschleuste Inhalte markieren, bevor sie das Modell erreichen. Auf dem Benchmark RAG-PIBench mit 4.876 Beispielen aus Retrieval-Szenarien erkannte ein feinabgestimmtes [[distilbert|DistilBERT]] Injections am besten (F1 0,896), während einfache TF-IDF-Baselines konkurrenzfähig blieben (Jaffal et al., 2026). Abschnitt 6 behandelt Detektoren ausführlich.

#### 6. Injections erkennen
Detektoren dienen meist als schneller erster Filter: Sie prüfen Eingaben oder Tool-Ausgaben und schicken, was sie markieren, an eine langsamere und teurere zweite Prüfung, etwa ein zweites Sprachmodell; jeder Fehlalarm kostet also eine weitere Prüfung (Kale & Vishwanath, 2026). Sie lesen entweder den Text, wie feinabgestimmte Klassifikatoren, etwa Prompt Guard 2, oder ein gepromptetes [[llm-as-a-judge|LLM als Bewerter]] (Lan et al., 2026), oder die Berechnung des Modells selbst, etwa Hidden States, [[attention-and-transformers|Attention]]-Muster oder Rollenrepräsentationen (Gupta & Tembey, 2026). Neuere Evaluationen zeigen vier Fallstricke:

- **Fehlalarme bei harmlosen Inhalten:** Webseiten enthalten viele legitime Anweisungen, etwa Beschriftungen von Schaltflächen und Hilfetexte. Der Benchmark BrowseSafe++ stellt jeder von 38.675 angegriffenen Seiten dieselbe Seite ohne Injection gegenüber; die meisten Injections wurden auf produktiven Websites beobachtet. Selbst der gepromptete Detektor mit dem höchsten [[classification-metrics|F1]] markierte fälschlich 13,82–15,10 % der harmlosen Seiten, während BrowseSafe-Guard, ein auf den Paaren trainierter Detektor mit 0,8 Milliarden Parametern, 92,98–98,29 F1 bei 1,35–7,40 % Falsch-Positiven erreichte. Auch die Rangfolge der Modelle änderte sich zwischen der HTML-, Markdown- und Accessibility-Tree-Ansicht derselben Seiten (Chen et al., 2026).
- **Abkürzungen statt Injections:** In der Standardevaluation von Probes auf Hidden States erreichen allein die Position im Gespräch und Textlängen 0,91–0,98 AUROC, ohne das Modell zu betrachten. Wurden den Trainingsdaten passende Negativbeispiele hinzugefügt, nämlich derselbe Zeitpunkt eines sauberen Durchlaufs derselben Aufgabe und harmloser Text im Format der Injection, sanken die Fehlalarme bei Gesprächen ohne Injection bei sechs offenen Modellen in bereits im Training gesehenen Anwendungen von 41–80 % auf 4–27 % (Kale & Vishwanath, 2026).
- **Vorhandensein ist nicht Erfolg:** Detektoren, die erkennen sollen, dass eine Injection vorhanden ist, etwa PIShield, trennten erfolglose Angriffe besser von harmlosen Eingaben als erfolgreiche. Attention Tracker, der misst, wie weit sich die Aufmerksamkeit von der vertrauenswürdigen Anweisung wegverlagert, trennte erfolgreiche Angriffe am besten (AUROC 0,949 bei Qwen und 0,887 bei Gemma) (Gupta & Tembey, 2026). Ebenso hatte auf BrowseSafe++ in 74,15 % der Fälle, in denen ein Modell einer Injection folgte, dasselbe Modell sie in einem separaten Erkennungstest markiert (Chen et al., 2026).
- **Scores sind keine Entscheidungen:** Ein eingesetztes System muss eine Eingabe zulassen, blockieren oder eskalieren. Auf 47.611 zurückgehaltenen Beispielen ordnete ein GPT-5.5-Bewerter Angriffe am besten (AUROC 0,897), vor Jev, einem auf kalibrierte Entscheidungen trainierten Modell (0,871), und Prompt Guard 2 mit 86 und 22 Millionen Parametern (0,757 und 0,714). Jedes Gate erreichte eine Falsch-Negativ-Rate von höchstens 1 % erst, wenn mehr als 91,8 % der Eingaben an den Prüfer eskaliert wurden, bei 40,6–45,8 % Falsch-Positiven; kalibrierte Wahrscheinlichkeiten allein machten die Entscheidungen nicht verlässlich (Lan et al., 2026).

#### Ursprung und Varianten
Greshake et al. (2023) führten Indirect Prompt Injection ein, zusammen mit einer Taxonomie ihrer Folgen, darunter Datendiebstahl, Wurm-artige Verbreitung und die Verunreinigung des Informationsökosystems. Liu et al. (2023) systematisierten Injection-Angriffe auf eingesetzte Anwendungen, und Zhan et al. (2024) schufen einen Benchmark für Tool-nutzende Agenten. Spätere Arbeiten zielen auf bestimmte Szenarien wie [[retrieval-augmented-generation|Retrieval-Augmented Generation]] (Jaffal et al., 2026) und proaktive Agenten (Wang et al., 2026).

### Wann einsetzen
Das Thema ist überall relevant, wo ein Modell Text verarbeitet, den jemand anderes als der Nutzer kontrolliert:

- Agenten, die im Web suchen, E-Mails oder Dokumente lesen oder Tools aufrufen, deren Ausgabe Text eines Angreifers enthalten kann (Greshake et al., 2023; Zhan et al., 2024).
- Anwendungen, die ihren eigenen Prompt um die Nutzereingabe legen und diesen Prompt sowie ihren LLM-Zugang schützen müssen (Liu et al., 2023).
- Retrieval-Systeme, deren abgerufene Passagen eingeschleuste Anweisungen enthalten können (Jaffal et al., 2026).
- Agenten, die auf Grundlage von Inhalten Dritter Empfehlungen geben oder Entscheidungen treffen (Wang et al., 2026).

### Stärken und Grenzen
Was heutige Abwehrmaßnahmen leisten:
- Begrenzer-basierte Abwehr wie LTBD funktioniert, ohne die Modellparameter zu ändern (Zhao et al., 2026).
- Abwehr durch Training kann den Angriffserfolg senken und die Nützlichkeit erhalten, wenn sie das Verhalten des Modells auf unveränderten Eingaben bewahrt (Dhouib et al., 2026).
- Prüfungen an der Ausführungsgrenze greifen unabhängig davon, wie eine Injection aufgebaut ist (Zheng et al., 2026).
- Kleine feinabgestimmte Detektoren können genau und günstig sein: BrowseSafe-Guard kostet etwa 0,18 $ je 1.000 Seiten auf einer gemieteten GPU, gegenüber 18,95–180,61 $ für Frontier-Modelle (Chen et al., 2026).

Offene Probleme:
- Als Greshake et al. (2023) Indirect Prompt Injection beschrieben, fehlten wirksame Gegenmaßnahmen; Abwehr auf Basis handgeschriebener Prompts bleibt fragil und anfällig für adaptive Angriffe (Zhao et al., 2026).
- Abwehr durch Training kann das Verhalten des Modells bei harmlosen Aufgaben verschieben (Dhouib et al., 2026).
- Abwehr, die Angriffsmuster erkennt, fällt zurück, wenn sich die Träger von Injections vervielfachen (Zheng et al., 2026).
- Manipulierte Empfehlungen sind schwer als Angriff zu erkennen, weil keine einzelne Aktion offensichtlich schädlich ist (Wang et al., 2026).
- Feste Angriffstexte unterschätzen das Risiko: Auf Websites beobachtete Injections waren unverändert wiederholt nur bei 0,49–4,00 % der Aufgaben erfolgreich, nach Überarbeitung anhand der Rückmeldungen des Agenten bei 30,66–95,41 % (Chen et al., 2026).
- Dass ein Detektor eine Injection markiert, zeigt nicht, dass das Modell ihr widersteht, und ein hoher Erkennungswert zeigt nicht, dass das Modell kompromittiert wurde (Chen et al., 2026; Gupta & Tembey, 2026).

### Vergleich
| Ansatz | Unterschied | Geeignet für |
|--------|-------------|--------------|
| Begrenzer und Warn-Prompts | Externe Inhalte im Prompt markieren oder vor ihnen warnen; kein Zugriff auf Modellparameter nötig (Zhan et al., 2024) | Anwendungen auf geschlossenen Modellen |
| Gelernte Begrenzer (LTBD) | Die Vertrauensgrenze lernen statt von Hand festlegen; Modell unverändert (Zhao et al., 2026) | Offene Modelle, deren Eingabe-Embeddings erweitert werden können |
| Abwehr durch Training (RAISED) | Das Modell so verändern, dass eingeschleuste Inhalte sein Verhalten nicht ändern (Dhouib et al., 2026) | Teams, die ihre eigenen Agentenmodelle feinabstimmen |
| Kontrolle an der Ausführungsgrenze (APEX) | Wirkungen aus der vertrauenswürdigen Aufgabe autorisieren statt Angriffe zu erkennen (Zheng et al., 2026) | Agenten, die über Tools handeln; siehe [[harness-engineering\|Harness Engineering]] |
| Injection-Detektoren | Inhalte oder den internen Zustand des Modells als harmlos oder bösartig klassifizieren, bevor das Modell handelt (Jaffal et al., 2026; Kale & Vishwanath, 2026) | Schneller erster Filter vor einer zweiten Prüfung; Prüfung abgerufener Passagen in RAG-Systemen |

### In der Praxis
Benchmarks wie InjecAgent messen, wie oft ein Agent eingeschleusten Anweisungen folgt (Zhan et al., 2024). Für Detektoren empfehlen Jaffal et al. (2026), mit starken leichtgewichtigen Baselines zu vergleichen und die Modellentwicklung strikt vom finalen Testdatensatz zu trennen, weil Ergebnisse sonst besser aussehen, als sie sind. Kale & Vishwanath (2026) empfehlen, Injection-Monitore mit sauberen Durchläufen derselben Aufgaben und harmlosen Doppelgängern zu trainieren und eine Baseline ohne das Modell, einen Vergleich mit den sauberen Gegenstücken sowie den Anteil gestoppter erfolgreicher Angriffe bei festem Budget für Fehlalarme anzugeben. Die Erkennung von Injections und die Erkennung erfolgreicher Angriffe sollten getrennt berichtet werden (Gupta & Tembey, 2026), und Detektoren für Webseiten sollten in jeder Seitenansicht getestet werden, die der Agent nutzt (Chen et al., 2026). Abwehrmaßnahmen werden nicht nur nach der Angriffserfolgsrate bewertet, sondern auch danach, ob der Agent bei harmlosen Aufgaben nützlich bleibt (Dhouib et al., 2026).

### Regulatorischer Kontext
Der [[cyber-resilience-act|Cyber Resilience Act]] verlangt, aktiv ausgenutzte Schwachstellen innerhalb von 24 Stunden zu melden; eine Prompt Injection, die in einer KI-Funktion eines Produkts zur Codeausführung führt, ist eine solche Schwachstelle. Unter der [[nis2-directive|NIS-2-Richtlinie]] kann eine Prompt Injection, die zu einem Datenabfluss führt, ein erheblicher Sicherheitsvorfall sein. Artikel 15 der [[eu-ai-act|KI-Verordnung]] verlangt, dass Hochrisiko-KI-Systeme widerstandsfähig gegen Versuche unbefugter Dritter sind, ihre Verwendung, Ausgaben oder Leistung durch Ausnutzung von Schwachstellen zu verändern.

### Merksatz
Sprachmodelle trennen Anweisungen nicht von Daten; jeder Text, den eine Anwendung ihnen zuführt, auch abgerufene Inhalte und Tool-Ausgaben, kann Anweisungen eines Angreifers enthalten.

### Quellen
- Greshake, K. et al. (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.* AISec 2023. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)
- Liu, Y. et al. (2023). *Prompt Injection attack against LLM-integrated Applications.* [arXiv:2306.05499](https://arxiv.org/abs/2306.05499)
- Zhan, Q. et al. (2024). *InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents.* Findings of ACL 2024. [arXiv:2403.02691](https://arxiv.org/abs/2403.02691)
- Wang, R. et al. (2026). *Who Is Your Agent Serving? Provider-Side Indirect Prompt Injection in Proactive Agents.* [arXiv:2610.05266](https://arxiv.org/abs/2610.05266)
- Zhao, L. et al. (2026). *LTBD: Learnable Trust-Boundary Delimiters for Prompt Injection Defense.* [arXiv:2610.11634](https://arxiv.org/abs/2610.11634)
- Dhouib, M. et al. (2026). *RAISED: Self-Distillation for Robustness to Prompt Injection in LLM Agents.* [arXiv:2610.06401](https://arxiv.org/abs/2610.06401)
- Zheng, X. et al. (2026). *APEX: Active Protection at Execution Boundaries for LLM Agents.* [arXiv:2610.06966](https://arxiv.org/abs/2610.06966)
- Jaffal, N. O. et al. (2026). *RAG-PIBench: A Leakage-Aware Benchmark for Prompt-Injection Detection in Trustworthy RAG Systems.* [arXiv:2610.08571](https://arxiv.org/abs/2610.08571)
- Chen, Y. et al. (2026). *BrowseSafe++: Benchmarking Prompt Injection Detection Across Web Contexts, Languages, and Browser Views.* [arXiv:2610.17457](https://arxiv.org/abs/2610.17457)
- Kale, K. & Vishwanath, S. (2026). *Prompt-Injection Probes Learn the Conversation, Not Just the Injection.* [arXiv:2610.18408](https://arxiv.org/abs/2610.18408)
- Gupta, S. & Tembey, P. (2026). *Are You Reading the Right Thing? Rethinking Internal Signals for Prompt-Injection Detection.* [arXiv:2610.19452](https://arxiv.org/abs/2610.19452)
- Lan, Q. et al. (2026). *From Detection to Decision: Calibration and Deferral for Prompt-Injection Detection.* [arXiv:2610.20907](https://arxiv.org/abs/2610.20907)
