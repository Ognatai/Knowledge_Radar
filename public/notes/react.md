---
title_en: ReAct
title_de: ReAct
entity_type: Method
aliases:
- ReAct
- Reasoning and Acting
- ReAct prompting
- ReAct agent
sources:
- https://arxiv.org/abs/2210.03629
- https://arxiv.org/abs/2201.11903
- https://arxiv.org/abs/2203.11171
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

ReAct (Reasoning and Acting) prompts a language model to alternate between free-text reasoning steps ("thoughts") and actions that query an external environment, such as a search API, and to read the resulting observations before the next step (Yao et al., 2022). Reasoning helps the model plan, track progress and handle exceptions; actions give it facts it does not have, which reduced the hallucinations and error propagation of pure [[chain-of-thought-prompting|chain-of-thought]] reasoning on question answering and fact verification (Yao et al., 2022). On the interactive benchmarks ALFWorld and WebShop, ReAct with one or two in-context examples beat imitation and reinforcement learning methods by 34 and 10 percentage points in success rate (Yao et al., 2022). The thought-action-observation loop became the standard pattern of LLM [[agentic-ai|agents]].

### How it works

```text
task + few-shot trajectories (thought / action / observation examples)
 ▼
Thought: reason about the goal and what is missing
 ▼
Action: call a tool, e.g. search[entity], lookup[string]
 ▼
Observation: tool result appended to the context
 ▼
repeat … until  Action: finish[answer]
```

#### 1. An action space extended by language

In a classic agent setting, an agent chooses actions from a task-specific action space and receives observations from the environment. ReAct extends the action space by the space of language: a "thought" is an action that does not affect the environment and returns no observation, but updates the context so that later reasoning or acting is better informed (Yao et al., 2022). Useful thoughts decompose goals into plans, inject commonsense knowledge, extract the important part of an observation, track progress and handle exceptions by adjusting the plan (Yao et al., 2022). Because the language space is unlimited, learning to act in it requires strong language priors, which is why ReAct relies on a large pretrained model (Yao et al., 2022).

#### 2. Prompting with trajectories

The main setup uses a frozen PaLM-540B prompted with a few in-context examples, each a human-written trajectory of thoughts, actions and observations for one task instance (Yao et al., 2022). For reasoning-heavy tasks such as question answering, thoughts and actions alternate at every step; for decision-making tasks with many actions, thoughts appear only where they help, so that the model decides when to reason (Yao et al., 2022). The appendix also reports GPT-3 results, which outperformed PaLM-540B (Yao et al., 2022). This is a form of [[few-shot-prompting|few-shot prompting]], and the trajectories are the prompt's main design element ([[prompt-engineering|prompt engineering]]).

#### 3. Tools: a deliberately simple Wikipedia API

For HotpotQA (multi-hop question answering) and FEVER (fact verification), the model gets three actions: `search[entity]` returns the first five sentences of the matching Wikipedia page or suggests the five most similar entities, `lookup[string]` returns the next sentence on the page containing the string, like Ctrl+F, and `finish[answer]` ends the task (Yao et al., 2022). The authors note that this API is much weaker than state-of-the-art lexical or neural retrievers; it is meant to mimic how people browse Wikipedia (Yao et al., 2022). Today the same loop runs over arbitrary functions via [[tool-calling|tool calling]].

#### 4. Results on knowledge tasks

With PaLM-540B, ReAct reached 27.4 exact match on HotpotQA and 60.9% accuracy on FEVER, against 25.7 and 58.9 for acting without thoughts (Act) and 29.4 and 56.3 for chain-of-thought (Wei et al., 2022), so it was better than CoT on FEVER and slightly worse on HotpotQA (Yao et al., 2022). The best results came from combining internal and external knowledge with [[self-consistency|self-consistency]] (Wang et al., 2022): falling back from ReAct to CoT with self-consistency when ReAct gives no answer within 7 (HotpotQA) or 5 (FEVER) steps reached 35.1 on HotpotQA, and falling back from CoT with self-consistency to ReAct when the majority answer occurs in fewer than half of the samples reached 64.6% on FEVER (Yao et al., 2022). Fine-tuning smaller PaLM models (8B and 62B) on 3,000 correct ReAct trajectories also showed the benefit of reasoning traces for informed acting (Yao et al., 2022).

#### 5. Failure modes

In a manual analysis of HotpotQA trajectories, hallucinated facts accounted for 56% of chain-of-thought failures but none of ReAct's; ReAct's failures were mostly reasoning errors, including getting stuck in repetitive steps (47%), and search results that were empty or unhelpful (23%) (Yao et al., 2022). Among successful answers, 6% of ReAct's and 14% of CoT's rested on hallucinated reasoning or facts (Yao et al., 2022). Grounding thus removes hallucination as the main failure, but makes the agent dependent on the quality of its tools, a trade-off also known from [[retrieval-augmented-generation|retrieval-augmented generation]].

#### 6. Interactive decision making

On ALFWorld, a text-based game in which an agent reaches household goals by navigating and interacting with a simulated household, and on WebShop, an online shopping environment with 1.18 million real products and 12,000 human instructions in which an agent has to buy a product matching an instruction, ReAct used thoughts sparingly to plan subgoals and track progress; with one or two examples it improved absolute success rates by 34 and 10 percentage points over imitation and reinforcement learning methods trained on 10^3 to 10^5 task instances (Yao et al., 2022). The authors also stress interpretability: humans can see which information came from the model and which from the environment, and can inspect the reasoning behind each action (Yao et al., 2022).

#### Origin and variants

ReAct was introduced by Yao et al. (2022), combining chain-of-thought prompting (Wei et al., 2022) with action generation. It is the default loop of [[agent-frameworks|agent frameworks]] such as [[langchain-and-langgraph|LangChain and LangGraph]] and a building block of [[multi-agent-systems|multi-agent systems]]; the original paper already showed that ReAct trajectories can also be used to fine-tune smaller models (Yao et al., 2022).

### When to use it

- When answers depend on facts that must be looked up step by step, as in multi-hop questions or fact checking (Yao et al., 2022).
- When a task requires interacting with an environment over several steps, such as web navigation or tool use ([[agentic-ai|agentic AI]]).
- When intermediate steps should be inspectable for debugging and trust (Yao et al., 2022).

### Strengths and limitations

**Strengths**
- Grounds reasoning in external information and so reduces hallucination (Yao et al., 2022).
- Works with a few in-context examples and a frozen model (Yao et al., 2022).
- Produces interpretable trajectories that show why each action was taken (Yao et al., 2022).

**Limitations**
- Depends on tool quality: empty or unhelpful search results were a major cause of failure (Yao et al., 2022).
- Can loop on repetitive steps and fail to recover (Yao et al., 2022).
- On tasks where the model's own knowledge suffices, it can be slightly worse than chain-of-thought, as on HotpotQA (Yao et al., 2022).
- Each step is another model call, which adds latency and cost ([[llm-cost-optimisation|LLM cost optimisation]]).

### Comparison

| Approach | Reasoning | Acting | Example result (PaLM-540B) |
|---|---|---|---|
| Standard prompting | no | no | HotpotQA 28.7, FEVER 57.1 |
| [[chain-of-thought-prompting\|Chain-of-thought]] | yes | no | HotpotQA 29.4, FEVER 56.3 |
| Act only | no | yes | HotpotQA 25.7, FEVER 58.9 |
| ReAct | yes | yes | HotpotQA 27.4, FEVER 60.9 |
| ReAct + CoT with self-consistency | yes | yes | HotpotQA 35.1, FEVER 64.6 (best combination per task) |

Sources: Yao et al. (2022); Wei et al. (2022); Wang et al. (2022).

### In practice

ReAct-style agents need a step limit and a fallback, as the paper's 7- and 5-step limits show (Yao et al., 2022). Traces of thoughts, actions and observations are logged to debug wrong tool use ([[llm-observability-and-tracing|LLM observability and tracing]]), and agents are evaluated on task success rather than on single answers ([[llm-evaluation|LLM evaluation]]). Since observations come from outside, they can carry [[prompt-injection|prompt injection]]; tool permissions and [[llm-guardrails|guardrails]] limit the damage.

### Key takeaway

ReAct interleaves reasoning and tool actions in one prompt-driven loop, so the model can look up what it does not know and show how it got there; this loop is the basis of today's LLM agents.

### Sources

- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. & Cao, Y. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* arXiv:2210.03629. [arXiv](https://arxiv.org/abs/2210.03629)
- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q. & Zhou, D. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.* arXiv:2201.11903. [arXiv](https://arxiv.org/abs/2201.11903)
- Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A. & Zhou, D. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models.* arXiv:2203.11171. [arXiv](https://arxiv.org/abs/2203.11171)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

ReAct (Reasoning and Acting) lässt ein Sprachmodell abwechselnd freie Denkschritte („Thoughts“) und Aktionen erzeugen, die eine externe Umgebung abfragen, etwa eine Such-API, und die so entstehenden Beobachtungen vor dem nächsten Schritt lesen (Yao et al., 2022). Das Schlussfolgern hilft beim Planen, beim Verfolgen des Fortschritts und beim Umgang mit Ausnahmen; die Aktionen liefern Fakten, die das Modell nicht hat, was bei Fragebeantwortung und Faktenprüfung die Halluzinationen und die Fehlerfortpflanzung reinen [[chain-of-thought-prompting|Chain-of-Thought]]-Schlussfolgerns verringerte (Yao et al., 2022). Auf den interaktiven Benchmarks ALFWorld und WebShop übertraf ReAct mit ein oder zwei Beispielen im Prompt Imitations- und Reinforcement-Learning-Verfahren um 34 und 10 Prozentpunkte Erfolgsquote (Yao et al., 2022). Die Schleife aus Thought, Action und Observation wurde zum Standardmuster von LLM-[[agentic-ai|Agenten]].

### Funktionsweise

```text
Aufgabe + Few-Shot-Trajektorien (Beispiele für Thought / Action / Observation)
 ▼
Thought: über das Ziel nachdenken und darüber, was fehlt
 ▼
Action: ein Tool aufrufen, z. B. search[entity], lookup[string]
 ▼
Observation: Tool-Ergebnis wird an den Kontext angehängt
 ▼
wiederholen … bis  Action: finish[answer]
```

#### 1. Ein um Sprache erweiterter Aktionsraum

In einem klassischen Agentenszenario wählt ein Agent Aktionen aus einem aufgabenspezifischen Aktionsraum und erhält Beobachtungen aus der Umgebung. ReAct erweitert den Aktionsraum um den Raum der Sprache: Ein „Thought“ ist eine Aktion, die die Umgebung nicht verändert und keine Beobachtung liefert, aber den Kontext aktualisiert, sodass späteres Schlussfolgern oder Handeln besser informiert ist (Yao et al., 2022). Nützliche Thoughts zerlegen Ziele in Pläne, bringen Alltagswissen ein, ziehen das Wichtige aus einer Beobachtung heraus, verfolgen den Fortschritt und behandeln Ausnahmen, indem sie den Plan anpassen (Yao et al., 2022). Weil der Raum der Sprache unbegrenzt ist, braucht Handeln darin starkes sprachliches Vorwissen; deshalb stützt sich ReAct auf ein großes vortrainiertes Modell (Yao et al., 2022).

#### 2. Prompting mit Trajektorien

Der Hauptaufbau nutzt ein eingefrorenes PaLM-540B, das mit wenigen Beispielen im Prompt arbeitet, jedes eine von Menschen geschriebene Trajektorie aus Thoughts, Actions und Observations für eine Aufgabe (Yao et al., 2022). Bei Aufgaben, in denen das Schlussfolgern im Vordergrund steht, etwa Fragebeantwortung, wechseln Thoughts und Actions in jedem Schritt; bei Entscheidungsaufgaben mit vielen Aktionen erscheinen Thoughts nur dort, wo sie helfen, sodass das Modell selbst entscheidet, wann es nachdenkt (Yao et al., 2022). Der Anhang berichtet auch Ergebnisse mit GPT-3, das PaLM-540B übertraf (Yao et al., 2022). Das ist eine Form von [[few-shot-prompting|Few-Shot-Prompting]], und die Trajektorien sind das zentrale Gestaltungselement des Prompts ([[prompt-engineering|Prompt Engineering]]).

#### 3. Tools: eine bewusst einfache Wikipedia-API

Für HotpotQA (mehrstufige Fragebeantwortung) und FEVER (Faktenprüfung) erhält das Modell drei Aktionen: `search[entity]` liefert die ersten fünf Sätze der passenden Wikipedia-Seite oder schlägt die fünf ähnlichsten Entitäten vor, `lookup[string]` liefert den nächsten Satz der Seite, der die Zeichenkette enthält, wie Strg+F, und `finish[answer]` beendet die Aufgabe (Yao et al., 2022). Die Autorinnen und Autoren halten fest, dass diese API deutlich schwächer ist als moderne lexikalische oder neuronale Retriever; sie soll nachbilden, wie Menschen Wikipedia durchsuchen (Yao et al., 2022). Heute läuft dieselbe Schleife über beliebige Funktionen per [[tool-calling|Tool Calling]].

#### 4. Ergebnisse bei Wissensaufgaben

Mit PaLM-540B erreichte ReAct 27,4 Exact Match auf HotpotQA und 60,9 % Genauigkeit auf FEVER, gegenüber 25,7 und 58,9 für Handeln ohne Thoughts (Act) und 29,4 und 56,3 für Chain-of-Thought (Wei et al., 2022); es war also auf FEVER besser als CoT und auf HotpotQA etwas schlechter (Yao et al., 2022). Die besten Ergebnisse entstanden, wenn internes und externes Wissen mit [[self-consistency|Self-Consistency]] (Wang et al., 2022) kombiniert wurden: Der Rückfall von ReAct auf CoT mit Self-Consistency, wenn ReAct innerhalb von 7 (HotpotQA) bzw. 5 (FEVER) Schritten keine Antwort liefert, erreichte 35,1 auf HotpotQA, und der Rückfall von CoT mit Self-Consistency auf ReAct, wenn die Mehrheitsantwort in weniger als der Hälfte der Stichproben vorkommt, erreichte 64,6 % auf FEVER (Yao et al., 2022). Auch Fine-Tuning kleinerer PaLM-Modelle (8B und 62B) auf 3.000 korrekten ReAct-Trajektorien zeigte den Nutzen von Gedankengängen für informiertes Handeln (Yao et al., 2022).

#### 5. Fehlerarten

In einer manuellen Analyse von HotpotQA-Trajektorien machten erfundene Fakten 56 % der Fehler von Chain-of-Thought aus, bei ReAct keine; die Fehler von ReAct waren meist Schlussfolgerungsfehler, darunter das Festhängen in sich wiederholenden Schritten (47 %), sowie leere oder unbrauchbare Suchergebnisse (23 %) (Yao et al., 2022). Unter den richtigen Antworten beruhten 6 % bei ReAct und 14 % bei CoT auf erfundenen Gedankengängen oder Fakten (Yao et al., 2022). Die Verankerung beseitigt Halluzinationen als Hauptfehler, macht den Agenten aber von der Qualität seiner Tools abhängig, ein Zielkonflikt, der auch von [[retrieval-augmented-generation|Retrieval-Augmented Generation]] bekannt ist.

#### 6. Interaktives Entscheiden

Auf ALFWorld, einem textbasierten Spiel, in dem ein Agent Ziele im Haushalt erreicht, indem er sich in einem simulierten Haushalt bewegt und mit ihm interagiert, und auf WebShop, einer Onlineshop-Umgebung mit 1,18 Millionen echten Produkten und 12.000 menschlichen Anweisungen, in der ein Agent ein zu einer Anweisung passendes Produkt kaufen muss, setzte ReAct Thoughts sparsam ein, um Teilziele zu planen und den Fortschritt zu verfolgen; mit ein oder zwei Beispielen verbesserte es die absolute Erfolgsquote um 34 und 10 Prozentpunkte gegenüber Imitations- und Reinforcement-Learning-Verfahren, die auf 10^3 bis 10^5 Aufgabeninstanzen trainiert waren (Yao et al., 2022). Die Autorinnen und Autoren betonen auch die Nachvollziehbarkeit: Menschen sehen, welche Information aus dem Modell und welche aus der Umgebung stammt, und können die Begründung jeder Aktion prüfen (Yao et al., 2022).

#### Herkunft und Varianten

ReAct wurde von Yao et al. (2022) eingeführt und verbindet Chain-of-Thought-Prompting (Wei et al., 2022) mit der Erzeugung von Aktionen. Es ist die Standardschleife von [[agent-frameworks|Agent-Frameworks]] wie [[langchain-and-langgraph|LangChain und LangGraph]] und ein Baustein von [[multi-agent-systems|Multi-Agenten-Systemen]]; schon das Originalpapier zeigte, dass sich ReAct-Trajektorien auch zum Fine-Tuning kleinerer Modelle nutzen lassen (Yao et al., 2022).

### Wann einsetzen

- Wenn Antworten von Fakten abhängen, die Schritt für Schritt nachgeschlagen werden müssen, etwa bei mehrstufigen Fragen oder Faktenprüfung (Yao et al., 2022).
- Wenn eine Aufgabe Interaktion mit einer Umgebung über mehrere Schritte erfordert, etwa Webnavigation oder Tool-Nutzung ([[agentic-ai|Agentic AI]]).
- Wenn Zwischenschritte für Debugging und Vertrauen nachvollziehbar sein sollen (Yao et al., 2022).

### Stärken und Grenzen

**Stärken**
- Verankert das Schlussfolgern in externen Informationen und verringert so Halluzinationen (Yao et al., 2022).
- Funktioniert mit wenigen Beispielen im Prompt und einem eingefrorenen Modell (Yao et al., 2022).
- Erzeugt nachvollziehbare Trajektorien, die zeigen, warum jede Aktion gewählt wurde (Yao et al., 2022).

**Grenzen**
- Hängt von der Qualität der Tools ab: Leere oder unbrauchbare Suchergebnisse waren eine Hauptursache von Fehlern (Yao et al., 2022).
- Kann in sich wiederholenden Schritten festhängen, ohne herauszufinden (Yao et al., 2022).
- Bei Aufgaben, für die das eigene Wissen des Modells reicht, kann es etwas schlechter sein als Chain-of-Thought, wie auf HotpotQA (Yao et al., 2022).
- Jeder Schritt ist ein weiterer Modellaufruf, was Latenz und Kosten erhöht ([[llm-cost-optimisation|LLM-Kostenoptimierung]]).

### Vergleich

| Ansatz | Schlussfolgern | Handeln | Beispielergebnis (PaLM-540B) |
|---|---|---|---|
| Standard-Prompting | nein | nein | HotpotQA 28,7, FEVER 57,1 |
| [[chain-of-thought-prompting\|Chain-of-Thought]] | ja | nein | HotpotQA 29,4, FEVER 56,3 |
| Nur Act | nein | ja | HotpotQA 25,7, FEVER 58,9 |
| ReAct | ja | ja | HotpotQA 27,4, FEVER 60,9 |
| ReAct + CoT mit Self-Consistency | ja | ja | HotpotQA 35,1, FEVER 64,6 (beste Kombination je Aufgabe) |

Quellen: Yao et al. (2022); Wei et al. (2022); Wang et al. (2022).

### In der Praxis

ReAct-Agenten brauchen ein Schrittlimit und einen Rückfallweg, wie die Grenzen von 7 und 5 Schritten im Papier zeigen (Yao et al., 2022). Trajektorien aus Thoughts, Actions und Observations werden protokolliert, um falsche Tool-Nutzung zu debuggen ([[llm-observability-and-tracing|LLM-Observability und Tracing]]), und Agenten werden am Aufgabenerfolg gemessen statt an einzelnen Antworten ([[llm-evaluation|LLM-Evaluation]]). Da Beobachtungen von außen kommen, können sie [[prompt-injection|Prompt Injection]] enthalten; Tool-Berechtigungen und [[llm-guardrails|Guardrails]] begrenzen den Schaden.

### Merksatz

ReAct verschränkt Schlussfolgern und Tool-Aktionen in einer per Prompt gesteuerten Schleife, sodass das Modell nachschlagen kann, was es nicht weiß, und zeigt, wie es zu seiner Antwort kam; diese Schleife ist die Grundlage heutiger LLM-Agenten.

### Quellen

- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. & Cao, Y. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* arXiv:2210.03629. [arXiv](https://arxiv.org/abs/2210.03629)
- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q. & Zhou, D. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.* arXiv:2201.11903. [arXiv](https://arxiv.org/abs/2201.11903)
- Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A. & Zhou, D. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models.* arXiv:2203.11171. [arXiv](https://arxiv.org/abs/2203.11171)
