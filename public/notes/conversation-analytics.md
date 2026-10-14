---
title_en: Conversation Analytics
title_de: Conversation Analytics
entity_type: Method
aliases:
- Containment rate
- Drop-off points
- Dialogue evaluation
- Conversation quality
sources:
- https://web.stanford.edu/~jurafsky/slp3/K.pdf
- https://arxiv.org/abs/cmp-lg/9704004
- https://docs.aws.amazon.com/lexv2/latest/dg/analytics-key-definitions.html
- https://docs.aws.amazon.com/lexv2/latest/dg/conversation-dashboard.html
- https://docs.cloud.google.com/dialogflow/cx/docs/concept/analytics
- https://www.cognigy.com/glossary/what-is-containment-rate
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Conversation analytics measures how well a [[conversational-ai|conversational AI]] system or [[voice-agents|voice agent]] performs on real conversations: whether tasks succeed, where users drop off, how often they are handed to a human, and how well intents and slots are understood (Amazon Lex: Key definitions; Dialogflow CX: Analytics). It builds on dialogue evaluation research, which measures task success, slot error rate and efficiency costs (Jurafsky & Martin, 2026) and compares dialogue strategies across tasks (Walker et al., 1997).

### How it works

Metrics are computed on four levels, from the whole conversation down to the single utterance (Amazon Lex: Key definitions):

```text
conversation ─► success / failed / dropped, handoff, duration, turns
  intent     ─► success / failed / switched / dropped, escalation rate
    slot     ─► success / failed (after max retries) / dropped
      utterance ─► detected / missed (no-match)
```

#### 1. Task success and dialogue costs

The basic measure of a task-based dialogue system is task success, the percentage of dialogues in which the system did the right thing, such as booking the right flight; the slot error rate counts inserted, deleted and substituted slots relative to the reference, and efficiency costs such as dialogue length in seconds or turns complement them (Jurafsky & Martin, 2026). The PARADISE framework separates what the task requires from how the agent behaves, computes performance over subdialogues and whole dialogues, identifies how much each factor contributes and normalises for task complexity, so that agents performing different tasks can be compared (Walker et al., 1997).

#### 2. Conversation outcomes

Amazon Lex counts a conversation as a success when its final intent was fulfilled, as failed when the final intent failed or the bot fell back to its fallback intent, and as dropped when the customer stopped responding before either happened (Amazon Lex: Key definitions). Dialogflow CX reports abandoned conversations, conversations in which human escalation was requested (live agent handoff), and a remaining category such as a user who says hello and leaves (Dialogflow CX: Analytics).

#### 3. Containment

Containment rate is the percentage of customer interactions fully resolved by an AI agent without escalation to a human agent (Cognigy glossary). The outcome categories above show why it must be read with care: a conversation that is dropped is not escalated either, yet it is not a success (Amazon Lex: Key definitions), so containment and task success are reported side by side.

#### 4. Intents, slots and utterances

Intents are categorised as success, failed (for example a declined confirmation or a switch to the fallback intent), switched (the bot moved to another intent first) or dropped; slots as success, failed (not filled even after the maximum number of retries) or dropped; utterances as detected or missed (Amazon Lex: Key definitions). Dialogflow CX reports per intent the escalation rate, the share of sessions that requested a human, and per page the no-match rate, the share of turns that matched nothing; it also lists missing transitions, where an existing intent would have matched if it had been in scope (Dialogflow CX: Analytics). Missed utterances show where [[natural-language-understanding|NLU]] did not recognise the input (Amazon Lex: Key definitions).

#### 5. Drop-off points and conversation flows

Conversation flows visualise the order of intents customers take, with the share and count of conversations at each step; selecting a node lists the conversations that followed that path, with their transcripts and the slot attempts (Amazon Lex: Conversation dashboard). Steps after which many conversations end are the drop-off points worth investigating.

#### 6. Operational signals

[[data-visualisation|Dashboards]] add total conversations, average duration and average turns per conversation (Amazon Lex: Conversation dashboard), and webhook calls, failures, timeout rate and average latency for back-end calls (Dialogflow CX: Analytics). For tracing of LLM-based agents, see [[llm-observability-and-tracing|LLM Observability and Tracing]].

### When to use it

- Continuously after launch, to find intents, pages and slots that fail or escalate often (Dialogflow CX: Analytics; Amazon Lex: Key definitions).
- To compare dialogue strategies or versions, normalised for task complexity (Walker et al., 1997).

### Strengths and limitations

**Strengths**
- Clear, platform-defined outcome categories for conversations, intents, slots and utterances (Amazon Lex: Key definitions).
- Paths and drop-off points become visible, down to individual transcripts (Amazon Lex: Conversation dashboard).
- Frameworks such as PARADISE normalise for task complexity, so agents with different tasks become comparable (Walker et al., 1997).

**Limitations**
- Containment alone hides dropped conversations, which are not escalated but not successful either (Amazon Lex: Key definitions; Cognigy glossary).
- Definitions differ between platforms: Dialogflow CX reports handoffs as counts and per-intent rates, Amazon Lex as outcome categories (Dialogflow CX: Analytics; Amazon Lex: Key definitions).
- Analytics depends on stored conversation history, which must be enabled (Dialogflow CX: Analytics).

### Comparison

| Measure | What it shows | Source |
|---------|---------------|--------|
| Task success | Did the system do the right thing? | Jurafsky & Martin (2026) |
| Containment rate | Resolved without a human | Cognigy glossary |
| Escalation / handoff rate | Share of sessions asking for a human | Dialogflow CX: Analytics |
| No-match rate / missed utterances | Understanding failures per page or utterance | Dialogflow CX: Analytics; Amazon Lex: Key definitions |
| Slot error rate | Wrong, missing or extra slot values | Jurafsky & Martin (2026) |
| Duration, turns | Efficiency costs | Amazon Lex: Conversation dashboard |

### In practice

Reports separate success, failure, dropped and escalated conversations rather than collapsing them into one containment number (Amazon Lex: Key definitions; Cognigy glossary). The no-match rate per page and the list of missing transitions point to concrete design fixes, and the webhook timeout rate shows whether back-end calls slow the conversation down (Dialogflow CX: Analytics). Conversation analytics complements offline evaluation such as [[llm-evaluation|LLM Evaluation]] with what happens in production.

### Key takeaway

Conversation analytics tracks success, drop-off, escalation and understanding errors per conversation, intent, slot and utterance; containment is only meaningful next to task success.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Frame-Based Dialogue Systems.* Speech and Language Processing, 3rd ed. draft, Appendix K. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/K.pdf)
- Walker, M. A., Litman, D. J., Kamm, C. A. & Abella, A. (1997). *PARADISE: A Framework for Evaluating Spoken Dialogue Agents.* ACL 1997. [arxiv.org](https://arxiv.org/abs/cmp-lg/9704004)
- Amazon Web Services. *Key definitions.* Amazon Lex V2 Developer Guide. [docs.aws.amazon.com](https://docs.aws.amazon.com/lexv2/latest/dg/analytics-key-definitions.html)
- Amazon Web Services. *Conversation dashboard.* Amazon Lex V2 Developer Guide. [docs.aws.amazon.com](https://docs.aws.amazon.com/lexv2/latest/dg/conversation-dashboard.html)
- Google Cloud. *Analytics.* Dialogflow CX documentation. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/analytics)
- Cognigy. *What is Containment Rate?* Glossary. [cognigy.com](https://www.cognigy.com/glossary/what-is-containment-rate)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Conversation Analytics misst, wie gut ein [[conversational-ai|Conversational-AI]]-System oder ein [[voice-agents|Voice Agent]] in echten Gesprächen funktioniert: ob Aufgaben gelingen, wo Nutzer abbrechen, wie oft an einen Menschen übergeben wird und wie gut Intents und Slots verstanden werden (Amazon Lex: Key definitions; Dialogflow CX: Analytics). Sie baut auf der Forschung zur Dialogevaluation auf, die Task Success, Slot Error Rate und Effizienzkosten misst (Jurafsky & Martin, 2026) und Dialogstrategien über Aufgaben hinweg vergleicht (Walker et al., 1997).

### Funktionsweise

Die Metriken werden auf vier Ebenen berechnet, vom ganzen Gespräch bis zur einzelnen Äußerung (Amazon Lex: Key definitions):

```text
Gespräch ─► Erfolg / fehlgeschlagen / abgebrochen, Übergabe, Dauer, Turns
  Intent ─► Erfolg / fehlgeschlagen / gewechselt / abgebrochen, Eskalationsrate
    Slot ─► Erfolg / fehlgeschlagen (nach maximalen Versuchen) / abgebrochen
      Äußerung ─► erkannt / verfehlt (no-match)
```

#### 1. Task Success und Dialogkosten

Das Grundmaß eines aufgabenorientierten Dialogsystems ist der Task Success, der Anteil der Dialoge, in denen das System das Richtige getan hat, etwa den richtigen Flug gebucht; die Slot Error Rate zählt eingefügte, gelöschte und ersetzte Slots relativ zur Referenz, und Effizienzkosten wie die Dialoglänge in Sekunden oder Turns ergänzen sie (Jurafsky & Martin, 2026). Das Framework PARADISE trennt, was die Aufgabe verlangt, von dem, wie sich der Agent verhält, berechnet die Leistung über Teildialoge und ganze Dialoge, bestimmt, wie viel jeder Faktor beiträgt, und normalisiert für die Komplexität der Aufgabe, sodass Agenten mit verschiedenen Aufgaben vergleichbar werden (Walker et al., 1997).

#### 2. Gesprächsergebnisse

Amazon Lex zählt ein Gespräch als Erfolg, wenn der letzte Intent erfüllt wurde, als fehlgeschlagen, wenn der letzte Intent scheiterte oder der Bot auf seinen Fallback-Intent zurückfiel, und als abgebrochen, wenn der Kunde vorher nicht mehr antwortete (Amazon Lex: Key definitions). Dialogflow CX meldet abgebrochene Gespräche, Gespräche mit Wunsch nach menschlicher Übernahme (Live Agent Handoff) und eine Restkategorie, etwa einen Nutzer, der Hallo sagt und geht (Dialogflow CX: Analytics).

#### 3. Containment

Die Containment Rate ist der Anteil der Kundeninteraktionen, die ein KI-Agent ohne Eskalation an einen menschlichen Mitarbeiter vollständig löst (Cognigy glossary). Die Ergebniskategorien oben zeigen, warum sie mit Vorsicht zu lesen ist: Ein abgebrochenes Gespräch wird ebenfalls nicht eskaliert, ist aber kein Erfolg (Amazon Lex: Key definitions); daher werden Containment und Task Success nebeneinander berichtet.

#### 4. Intents, Slots und Äußerungen

Intents werden als Erfolg, fehlgeschlagen (etwa bei abgelehnter Bestätigung oder Wechsel zum Fallback-Intent), gewechselt (der Bot ging zuerst zu einem anderen Intent) oder abgebrochen eingeordnet; Slots als Erfolg, fehlgeschlagen (auch nach der maximalen Zahl an Versuchen nicht gefüllt) oder abgebrochen; Äußerungen als erkannt oder verfehlt (Amazon Lex: Key definitions). Dialogflow CX meldet pro Intent die Eskalationsrate, den Anteil der Sitzungen mit Wunsch nach einem Menschen, und pro Page die No-Match-Rate, den Anteil der Turns ohne Treffer; außerdem listet es fehlende Übergänge, bei denen ein vorhandener Intent gepasst hätte, wenn er im Geltungsbereich gewesen wäre (Dialogflow CX: Analytics). Verfehlte Äußerungen zeigen, wo die [[natural-language-understanding|NLU]] die Eingabe nicht erkannt hat (Amazon Lex: Key definitions).

#### 5. Abbruchstellen und Gesprächsverläufe

Conversation Flows zeigen die Reihenfolge der Intents, die Kunden durchlaufen, mit Anteil und Zahl der Gespräche je Schritt; ein ausgewählter Knoten listet die Gespräche dieses Pfads mit Transkript und Slot-Versuchen (Amazon Lex: Conversation dashboard). Schritte, nach denen viele Gespräche enden, sind die Abbruchstellen, die es zu untersuchen gilt.

#### 6. Betriebliche Signale

[[data-visualisation|Dashboards]] ergänzen die Gesamtzahl der Gespräche, die durchschnittliche Dauer und die durchschnittliche Zahl der Turns pro Gespräch (Amazon Lex: Conversation dashboard) sowie Aufrufe, Fehler, Timeout-Rate und durchschnittliche Latenz von [[asynchronous-apis|Webhooks]] für Backend-Aufrufe (Dialogflow CX: Analytics). Zum Tracing LLM-basierter Agenten siehe [[llm-observability-and-tracing|LLM Observability and Tracing]].

### Wann einsetzen

- Fortlaufend nach dem Start, um Intents, Pages und Slots zu finden, die oft scheitern oder eskalieren (Dialogflow CX: Analytics; Amazon Lex: Key definitions).
- Um Dialogstrategien oder Versionen zu vergleichen, normalisiert für die Aufgabenkomplexität (Walker et al., 1997).

### Stärken und Grenzen

**Stärken**
- Klare, von der Plattform definierte Ergebniskategorien für Gespräche, Intents, Slots und Äußerungen (Amazon Lex: Key definitions).
- Pfade und Abbruchstellen werden sichtbar, bis hin zu einzelnen Transkripten (Amazon Lex: Conversation dashboard).
- Frameworks wie PARADISE normalisieren für die Aufgabenkomplexität, sodass Agenten mit verschiedenen Aufgaben vergleichbar werden (Walker et al., 1997).

**Grenzen**
- Containment allein verdeckt abgebrochene Gespräche, die nicht eskaliert, aber auch nicht erfolgreich sind (Amazon Lex: Key definitions; Cognigy glossary).
- Die Definitionen unterscheiden sich zwischen Plattformen: Dialogflow CX meldet Übergaben als Zahlen und Raten pro Intent, Amazon Lex als Ergebniskategorien (Dialogflow CX: Analytics; Amazon Lex: Key definitions).
- Analytics hängt an gespeicherter Gesprächshistorie, die aktiviert sein muss (Dialogflow CX: Analytics).

### Vergleich

| Maß | Was es zeigt | Quelle |
|-----|--------------|--------|
| Task Success | Hat das System das Richtige getan? | Jurafsky & Martin (2026) |
| Containment Rate | Ohne Menschen gelöst | Cognigy glossary |
| Eskalations-/Übergaberate | Anteil der Sitzungen mit Wunsch nach einem Menschen | Dialogflow CX: Analytics |
| No-Match-Rate / verfehlte Äußerungen | Verstehensfehler pro Page oder Äußerung | Dialogflow CX: Analytics; Amazon Lex: Key definitions |
| Slot Error Rate | Falsche, fehlende oder zusätzliche Slot-Werte | Jurafsky & Martin (2026) |
| Dauer, Turns | Effizienzkosten | Amazon Lex: Conversation dashboard |

### In der Praxis

Berichte trennen erfolgreiche, fehlgeschlagene, abgebrochene und eskalierte Gespräche, statt sie in einer einzigen Containment-Zahl zusammenzufassen (Amazon Lex: Key definitions; Cognigy glossary). Die No-Match-Rate pro Page und die Liste fehlender Übergänge zeigen konkrete Designkorrekturen, und die Webhook-Timeout-Rate zeigt, ob Backend-Aufrufe das Gespräch bremsen (Dialogflow CX: Analytics). Conversation Analytics ergänzt Offline-Evaluation wie [[llm-evaluation|LLM-Evaluation]] um das, was im Betrieb passiert.

### Merksatz

Conversation Analytics verfolgt Erfolg, Abbruch, Eskalation und Verstehensfehler pro Gespräch, Intent, Slot und Äußerung; Containment ist nur neben dem Task Success aussagekräftig.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Frame-Based Dialogue Systems.* Speech and Language Processing, 3rd ed. draft, Appendix K. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/K.pdf)
- Walker, M. A., Litman, D. J., Kamm, C. A. & Abella, A. (1997). *PARADISE: A Framework for Evaluating Spoken Dialogue Agents.* ACL 1997. [arxiv.org](https://arxiv.org/abs/cmp-lg/9704004)
- Amazon Web Services. *Key definitions.* Amazon Lex V2 Developer Guide. [docs.aws.amazon.com](https://docs.aws.amazon.com/lexv2/latest/dg/analytics-key-definitions.html)
- Amazon Web Services. *Conversation dashboard.* Amazon Lex V2 Developer Guide. [docs.aws.amazon.com](https://docs.aws.amazon.com/lexv2/latest/dg/conversation-dashboard.html)
- Google Cloud. *Analytics.* Dialogflow CX documentation. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/analytics)
- Cognigy. *What is Containment Rate?* Glossary. [cognigy.com](https://www.cognigy.com/glossary/what-is-containment-rate)
