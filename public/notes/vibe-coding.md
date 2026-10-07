---
title_en: Vibe Coding
title_de: Vibe Coding
entity_type: Concept
sources:
- https://simonwillison.net/2025/Mar/19/vibe-coding/
- https://thenewstack.io/loop-engineering/
- https://arxiv.org/abs/2211.03622
- https://arxiv.org/abs/2507.09089
- https://www.anthropic.com/engineering/building-effective-agents
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Vibe coding is building software with an LLM without reviewing the code it writes (Willison, 2025). The term was coined by Andrej Karpathy in February 2025 for a style in which one gives in to the vibes, accepts all changes without reading the diffs and pastes error messages back until things work, described in the original post as not too bad for throwaway weekend projects (Willison, 2025). Not all AI-assisted programming is vibe coding: code that was reviewed, tested and can be explained to someone else is ordinary software development (Willison, 2025). Vibe coding shifts trust from reading the code to running and testing it, and is only as safe as that testing.

### How it works

#### 1. Characteristics

- Intent is described in natural language instead of code.
- Iteration with a coding agent in a loop ([[agentic-ai|Agentic AI]]).
- Verification by running and testing, not by line-by-line review.
- Fast cycles, often without understanding every implementation detail.

#### 2. A spectrum, not a switch

```text
classical programming   →   AI-assisted programming          →   vibe coding
every line written          suggestions, but every change        intent described,
by hand                     reviewed and understood              result tested instead of read
```

Most real work lies somewhere in between and varies by task. Willison's rule for production code: do not commit code you could not explain exactly to somebody else (Willison, 2025).

#### 3. What keeps it viable

Vibe coding relies on the same foundations as reliable agents in general:

- a **harness** with controlled tool access, sandboxing and visible diffs ([[harness-engineering|Harness Engineering]]);
- a **loop** with clear stopping conditions instead of endless patching ([[loop-engineering|Loop Engineering]]);
- a reliable **test suite and execution environment** as replacement for manual review ([[regression-testing|Regression Testing]]; [[quality-control|Quality Control]]).

Coding is a good fit for agents because code solutions are verifiable through automated tests and agents can iterate on test results, but human review remains crucial to ensure that solutions match broader system requirements (Anthropic, 2024a).

#### Origin and variants

Karpathy's post of 6 February 2025 named the practice, and the term quickly spread to mainstream media; Willison warned early that it was being applied to all AI-assisted programming, which dilutes it (Willison, 2025). With agents running autonomously in loops in 2026, the related risk of comprehension debt, the gap that widens when a system ships code nobody read, is discussed for loop engineering as well (Janakiram MSV, 2026).

### When to use it

| Context | Suitability |
|----------|----------------|
| Prototypes, experiments, throwaway scripts | Good: fast iteration matters more than longevity (Willison, 2025) |
| Internal tools with limited impact | Suitable with basic tests |
| Production code with high correctness requirements | Only with review, test coverage and guardrails |
| Security-critical or regulated systems | Risky without an additional control layer |
| Legacy code with implicit dependencies | Risky, because missing understanding makes errors more likely |

Before vibe coding something, consider how much harm bugs or vulnerabilities could cause, whether secrets or private data are involved, whether the code makes requests to other services and whether usage-based billing could rack up charges (Willison, 2025).

### Strengths and limitations

**Strengths**
- Lowers the initial barrier to building custom tools, even for people without programming training (Willison, 2025).
- Helps experienced developers build intuition for what LLMs can and cannot do (Willison, 2025).
- Very fast for prototypes and low-stakes projects.

**Limitations**
- Errors outside the test coverage remain undetected, especially in edge cases.
- Security: participants with an AI code assistant wrote significantly less secure code but were more likely to believe it was secure (Perry et al., 2022); exposed secrets and data leaks are typical risks (Willison, 2025).
- Perceived and actual speed can differ: experienced open-source developers took 19% longer with early-2025 AI tools, although they estimated they had been 20% faster (Becker et al., 2025).
- Technical debt grows unnoticed when nobody keeps a mental model of the code (Janakiram MSV, 2026).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Classical programming | Every line written and understood | Any code, at higher effort |
| AI-assisted programming | LLM suggests, human reviews and can explain every change (Willison, 2025) | Production code |
| Vibe coding | LLM writes, human tests the result without reading the code (Willison, 2025) | Prototypes, personal tools |
| Autonomous loop | Agents find, write and verify work on a schedule ([[loop-engineering|Loop Engineering]]) | Recurring maintenance tasks with strong tests |

### In practice

Sandboxes make it hard to cause harm: code restricted to an isolated environment without network access cannot damage other systems (Willison, 2025). Before shared or production use, someone experienced reviews the code. The more code a model produces, the more important it becomes to judge architecture, test coverage and security; AI-assisted programming moves effort from writing code to assessing code and its verification ([[engineering-methods-for-ai-systems|Engineering Methods for AI Systems]]). Context and conventions for the agent are kept in instruction files and skills ([[context-engineering|Context Engineering]]; [[agent-skills|Agent Skills]]; [[prompt-engineering|Prompt Engineering]]), external tools are connected via [[mcp-and-related-protocols|MCP and Related Protocols]], and multi-agent setups are discussed as [[graph-engineering|Graph Engineering]]. Usage-based APIs need spending limits ([[llm-cost-optimization|LLM Cost Optimization]]), and agent runs can be traced ([[llm-observability-and-tracing|LLM Observability and Tracing]]).

### Key takeaway

Vibe coding shifts trust from code review to testing and is only as safe as that testing; it is fine for low-stakes prototypes, while production code still needs someone who understands and can explain it.

### Sources

- Willison, S. (2025). *Not all AI-assisted programming is vibe coding (but vibe coding rocks).* Simon Willison's Weblog, 19 March 2025. [simonwillison.net](https://simonwillison.net/2025/Mar/19/vibe-coding/)
- Janakiram MSV (2026). *The Anthropic leader who built Claude Code says he ditched prompting — now he just writes loops.* The New Stack, 10 June 2026. [thenewstack.io](https://thenewstack.io/loop-engineering/)
- Perry, N. et al. (2022). *Do Users Write More Insecure Code with AI Assistants?* ACM CCS 2023. [arXiv:2211.03622](https://arxiv.org/abs/2211.03622)
- Becker, J. et al. (2025). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.* [arXiv:2507.09089](https://arxiv.org/abs/2507.09089)
- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Vibe Coding bedeutet, Software mit einem LLM zu bauen, ohne den Code zu prüfen, den es schreibt (Willison, 2025). Den Begriff prägte Andrej Karpathy im Februar 2025 für einen Stil, bei dem man sich ganz den „Vibes“ überlässt, alle Änderungen annimmt, ohne die Diffs zu lesen, und Fehlermeldungen zurückkopiert, bis es funktioniert; Karpathy hielt das für Wegwerf-Projekte am Wochenende für vertretbar (Willison, 2025). Nicht jedes KI-gestützte Programmieren ist Vibe Coding: Code, der geprüft, getestet und erklärbar ist, ist gewöhnliche Softwareentwicklung (Willison, 2025). Vibe Coding verlagert Vertrauen vom Lesen des Codes zum Ausführen und Testen und ist nur so sicher wie diese Tests.

### Funktionsweise

#### 1. Merkmale

- Die Absicht wird in natürlicher Sprache beschrieben statt in Code.
- Iteration mit einem Coding-Agenten in einer Schleife ([[agentic-ai|Agentic AI]]).
- Verifikation durch Ausführen und Testen, nicht durch zeilenweises Review.
- Schnelle Zyklen, oft ohne jedes Implementierungsdetail zu verstehen.

#### 2. Ein Spektrum, kein Schalter

```text
klassisches Programmieren   →   KI-gestütztes Programmieren          →   Vibe Coding
jede Zeile selbst               Vorschläge, aber jede Änderung           Absicht beschrieben,
geschrieben                     geprüft und verstanden                   Ergebnis getestet statt gelesen
```

Die meiste reale Arbeit liegt dazwischen und variiert je nach Aufgabe. Willisons Regel für Produktivcode: keinen Code committen, den man nicht jemand anderem genau erklären könnte (Willison, 2025).

#### 3. Was es tragfähig macht

Vibe Coding beruht auf denselben Grundlagen wie zuverlässige Agenten allgemein:

- ein **Harness** mit kontrolliertem Werkzeugzugriff, Sandboxing und sichtbaren Diffs ([[harness-engineering|Harness Engineering]]);
- eine **Schleife** mit klaren Abbruchbedingungen statt endlosem Nachbessern ([[loop-engineering|Loop Engineering]]);
- eine belastbare **Testsuite und Ausführungsumgebung** als Ersatz für manuelles Review ([[regression-testing|Regressionstests]]; [[quality-control|Qualitätskontrolle]]).

Programmieren eignet sich gut für Agenten, weil sich Codelösungen durch automatisierte Tests prüfen lassen und Agenten anhand der Testergebnisse iterieren können; die menschliche Prüfung bleibt aber entscheidend, damit Lösungen zu den übergeordneten Systemanforderungen passen (Anthropic, 2024a).

#### Ursprung und Varianten

Karpathys Beitrag vom 6. Februar 2025 gab der Praxis ihren Namen, und der Begriff gelangte schnell in große Medien; Willison warnte früh, dass er auf jedes KI-gestützte Programmieren angewendet und dadurch verwässert werde (Willison, 2025). Seit Agenten 2026 autonom in Schleifen laufen, wird das verwandte Risiko der „Comprehension Debt“, der Lücke, die wächst, wenn ein System ungelesenen Code ausliefert, auch für Loop Engineering diskutiert (Janakiram MSV, 2026).

### Wann einsetzen

| Kontext | Eignung |
|----------|----------------|
| Prototypen, Experimente, Wegwerf-Skripte | Gut: schnelle Iteration zählt mehr als Langlebigkeit (Willison, 2025) |
| Interne Werkzeuge mit begrenzter Tragweite | Geeignet, mit grundlegenden Tests |
| Produktivcode mit hohem Korrektheitsanspruch | Nur mit Review, Testabdeckung und Guardrails |
| Sicherheitskritische oder regulierte Systeme | Riskant ohne zusätzliche Kontrollschicht |
| Legacy-Code mit impliziten Abhängigkeiten | Riskant, weil fehlendes Verständnis Fehler wahrscheinlicher macht |

Vor dem Vibe Coding lohnt die Frage, wie viel Schaden Fehler oder Sicherheitslücken anrichten könnten, ob Geheimnisse oder private Daten betroffen sind, ob der Code Anfragen an andere Dienste stellt und ob nutzungsabhängige Abrechnung hohe Kosten verursachen könnte (Willison, 2025).

### Stärken und Grenzen

**Stärken**
- Senkt die Einstiegshürde, eigene Werkzeuge zu bauen, auch für Menschen ohne Programmierausbildung (Willison, 2025).
- Hilft erfahrenen Entwickler:innen, ein Gespür dafür zu entwickeln, was LLMs können und was nicht (Willison, 2025).
- Sehr schnell für Prototypen und Projekte mit geringer Tragweite.

**Einschränkungen**
- Fehler außerhalb der Testabdeckung bleiben unentdeckt, besonders in Randfällen.
- Sicherheit: Teilnehmende mit KI-Code-Assistent schrieben deutlich unsichereren Code, hielten ihn aber eher für sicher (Perry et al., 2022); offengelegte Geheimnisse und Datenabflüsse sind typische Risiken (Willison, 2025).
- Gefühlte und tatsächliche Geschwindigkeit können auseinanderfallen: Erfahrene Open-Source-Entwickler:innen brauchten mit KI-Werkzeugen von Anfang 2025 19 % länger, schätzten aber, 20 % schneller gewesen zu sein (Becker et al., 2025).
- Technische Schulden wachsen unbemerkt, wenn niemand ein mentales Modell des Codes behält (Janakiram MSV, 2026).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Klassisches Programmieren | Jede Zeile geschrieben und verstanden | Jeder Code, mit höherem Aufwand |
| KI-gestütztes Programmieren | LLM schlägt vor, Mensch prüft und kann jede Änderung erklären (Willison, 2025) | Produktivcode |
| Vibe Coding | LLM schreibt, Mensch testet das Ergebnis, ohne den Code zu lesen (Willison, 2025) | Prototypen, persönliche Werkzeuge |
| Autonome Schleife | Agenten finden, schreiben und prüfen Arbeit nach Zeitplan ([[loop-engineering|Loop Engineering]]) | Wiederkehrende Wartungsaufgaben mit starken Tests |

### In der Praxis

Sandboxes machen es schwer, Schaden anzurichten: Code, der auf eine isolierte Umgebung ohne Netzwerkzugriff beschränkt ist, kann andere Systeme nicht beschädigen (Willison, 2025). Vor gemeinsamer oder produktiver Nutzung prüft eine erfahrene Person den Code. Je mehr Code ein Modell erzeugt, desto wichtiger wird es, Architektur, Testabdeckung und Sicherheit beurteilen zu können; KI-gestütztes Programmieren verlagert Aufwand vom Schreiben des Codes zur Beurteilung des Codes und seiner Verifikation ([[engineering-methods-for-ai-systems|Engineering-Methoden für KI-Systeme]]). Kontext und Konventionen für den Agenten stehen in Anweisungsdateien und Skills ([[context-engineering|Context Engineering]]; [[agent-skills|Agent Skills]]; [[prompt-engineering|Prompt Engineering]]), externe Werkzeuge werden über [[mcp-and-related-protocols|MCP und ähnliche Protokolle]] angebunden, und Multi-Agenten-Setups werden als [[graph-engineering|Graph Engineering]] diskutiert. Nutzungsabhängige APIs brauchen Ausgabelimits ([[llm-cost-optimization|LLM-Kostenoptimierung]]), und Agentenläufe lassen sich tracen ([[llm-observability-and-tracing|LLM-Observability und Tracing]]).

### Merksatz

Vibe Coding verlagert Vertrauen vom Code-Review zu Tests und ist nur so sicher wie diese Tests; für Prototypen mit geringer Tragweite ist es in Ordnung, Produktivcode braucht weiterhin jemanden, der ihn versteht und erklären kann.

### Quellen

- Willison, S. (2025). *Not all AI-assisted programming is vibe coding (but vibe coding rocks).* Simon Willison's Weblog, 19 March 2025. [simonwillison.net](https://simonwillison.net/2025/Mar/19/vibe-coding/)
- Janakiram MSV (2026). *The Anthropic leader who built Claude Code says he ditched prompting — now he just writes loops.* The New Stack, 10 June 2026. [thenewstack.io](https://thenewstack.io/loop-engineering/)
- Perry, N. et al. (2022). *Do Users Write More Insecure Code with AI Assistants?* ACM CCS 2023. [arXiv:2211.03622](https://arxiv.org/abs/2211.03622)
- Becker, J. et al. (2025). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.* [arXiv:2507.09089](https://arxiv.org/abs/2507.09089)
- Erik S. & Zhang, B. (2024). *Building effective agents.* Anthropic Engineering, 19 December 2024. [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)
