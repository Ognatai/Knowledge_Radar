---
title_en: Conversational AI
title_de: Conversational AI
entity_type: Concept
aliases:
- Dialogue systems
- Task-oriented dialogue
- Multi-turn dialogue systems
sources:
- https://web.stanford.edu/~jurafsky/slp3/K.pdf
- https://docs.cloud.google.com/dialogflow/cx/docs/concept/handler
- https://docs.cloud.google.com/dialogflow/cx/docs/concept/playbook
- https://docs.cloud.google.com/dialogflow/cx/docs/concept/flow
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Conversational AI covers systems that talk with users over several turns, in text or speech, to help them solve a task such as booking a trip or changing a contract (Jurafsky & Martin, 2026). The classic architecture fills the slots of a task frame: it understands each utterance, tracks the dialogue state, decides on the next dialogue act and generates a response; production platforms add fallbacks for unrecognised or missing input and escalation to a human agent (Jurafsky & Martin, 2026; Dialogflow CX: Handlers). Today, deterministic flows are combined with generative, LLM-based components (Dialogflow CX: Playbooks).

### How it works

The dialogue-state architecture splits a task-oriented dialogue system into components that run once per user turn (Jurafsky & Martin, 2026):

```text
speech ─► ASR ─► NLU ─────────► dialogue state ─► dialogue policy ─► NLG ─► TTS ─► speech
                (domain, intent,  tracker          (next act:         (sentence
                 slots)           (all slots so far) ask, confirm,     realisation)
                                                     answer, reject)
```

#### 1. Frames and slots

A frame represents what the system must know to perform a task; it consists of slots that take values, often of a semantic type such as CITY, DATE or TIME. The system's goal is to fill the slots with the values the user intends and then perform the action, such as a query or a booking. A set of frames is called a domain ontology; the frame-based paradigm goes back to the GUS travel system of 1977 (Jurafsky & Martin, 2026).

#### 2. Understanding the utterance

[[natural-language-understanding|Natural language understanding]] extracts three things from each utterance: the domain, the user's intent, and the slot fillers, for example SHOW-FLIGHTS with origin Boston and destination San Francisco (Jurafsky & Martin, 2026). In speech systems, [[automatic-speech-recognition|automatic speech recognition]] produces the text first.

#### 3. Tracking the dialogue state

The [[dialogue-state-tracking|dialogue state tracker]] keeps the current state of the frame, summarising all of the user's constraints so far, and the user's most recent dialogue act; dialogue acts such as INFORM, REQUEST, CONFIRM or DENY describe what an utterance does (Jurafsky & Martin, 2026).

#### 4. Dialogue policy: confirm, reject, ask

The dialogue policy decides which act comes next: answer, ask a clarification question, confirm or reject. Explicit confirmation ("Is that correct?") makes correcting errors easy but is slow and awkward; implicit confirmation repeats the understanding while asking the next question. Rejection ("I'm sorry, I didn't understand that") expresses lack of understanding. Systems can choose between them by the recogniser's confidence, for example rejecting below one threshold, confirming explicitly above it and not confirming at all at very high confidence (Jurafsky & Martin, 2026).

#### 5. Generating the response

Natural language generation turns the chosen act and its slots into a sentence. Trained realisers often work on delexicalised examples, in which slot values are replaced by placeholders, and fill the values back in afterwards (Jurafsky & Martin, 2026). In voice systems, [[text-to-speech|text-to-speech]] speaks the response.

#### 6. Fallback and escalation in production

Platforms make error handling explicit. In Dialogflow CX, every flow has handlers for the built-in events no-match (input matches no intent in scope) and no-input (no input received, such as empty or unrecognised audio or a no-speech timeout); they are created automatically and cannot be deleted, and numbered variants allow a different reaction to the first, second and further failures. A request to talk to a human ends a flow with a human-escalation event that the calling page can handle (Dialogflow CX: Handlers). Conversation paths are modelled as flows made of pages (Dialogflow CX: Flows).

#### 7. Origin and variants

ELIZA (Weizenbaum, 1966) was an early pattern-action chatbot; the GUS system of the late 1970s established the frame-based paradigm, which dominated industry for over 30 years and reached phones with assistants such as Siri around 2010; dialogue state tracking was advanced by an annual challenge series (Jurafsky & Martin, 2026). Generative agents now build an LLM prompt from a playbook's goal, instructions and tools for each turn, and can hand sub-tasks to deterministic flows (Dialogflow CX: Playbooks); see [[large-language-models|Large Language Models]] and [[agentic-ai|Agentic AI]].

### When to use it

- For customer service, bookings and other tasks with a known set of information to collect (Jurafsky & Martin, 2026).
- Flows when the conversation paths should be defined explicitly as pages and routes; generative playbooks when an LLM should pursue a goal by following instructions and calling tools (Dialogflow CX: Flows; Dialogflow CX: Playbooks).
- In voice channels, together with speech recognition and synthesis in a [[voice-agents|voice agent]].

### Strengths and limitations

**Strengths**
- The frame-and-slot model makes clear what the system still needs to know (Jurafsky & Martin, 2026).
- Explicit fallback and escalation paths keep conversations from dead-ending (Dialogflow CX: Handlers).
- Flows and generative playbooks can be combined in one agent (Dialogflow CX: Playbooks).

**Limitations**
- Speech systems often misrecognise users; corrections are harder to recognise than normal utterances, because frustrated users hyperarticulate (Jurafsky & Martin, 2026).
- Confirming everything is slow and awkward; confirming nothing lets errors through (Jurafsky & Martin, 2026).
- Generative components depend on the instructions in the prompt and need the same controls as other LLM applications (Dialogflow CX: Playbooks; [[hallucination-detection|Hallucination Detection]]).

### Comparison

| Approach | How it works | Suited for |
|----------|--------------|------------|
| Pattern-action chatbot | Rules map patterns to answers, as in ELIZA (Jurafsky & Martin, 2026) | Very narrow scripted dialogues |
| Frame-based dialogue system | NLU, state tracking, policy, NLG (Jurafsky & Martin, 2026) | Tasks with known slots |
| Flow-based platform | Flows of pages, routes, event handlers (Dialogflow CX: Flows; Dialogflow CX: Handlers) | Explicitly modelled conversation paths |
| Generative agent | LLM prompt from goal, instructions and tools (Dialogflow CX: Playbooks) | Free phrasing, tool use; see [[agentic-ai\|Agentic AI]] |

### In practice

Task success, the share of dialogues in which the system did the right thing, and the slot error rate are the basic measures, complemented by efficiency costs such as dialogue length ([[conversation-analytics|Conversation Analytics]]; Jurafsky & Martin, 2026). Every flow should define what happens after repeated no-match and no-input events, ending with a handover to a human (Dialogflow CX: Handlers). Errors are detected from user corrections, which can be recognised from semantic, phonetic, prosodic and ASR-confidence features (Jurafsky & Martin, 2026).

### Key takeaway

Conversational AI fills a task frame over several turns by understanding, tracking state, choosing the next act and responding; robust systems plan for misunderstanding with confirmation, fallback and escalation to a human.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Frame-Based Dialogue Systems.* Speech and Language Processing, 3rd ed. draft, Appendix K. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/K.pdf)
- Google Cloud. *State handlers.* Dialogflow CX documentation. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/handler)
- Google Cloud. *Playbooks.* Dialogflow CX documentation. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/playbook)
- Google Cloud. *Flows.* Dialogflow CX documentation. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/flow)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Conversational AI umfasst Systeme, die über mehrere Turns per Text oder Sprache mit Nutzern sprechen, um ihnen bei einer Aufgabe zu helfen, etwa eine Reise zu buchen oder einen Vertrag zu ändern (Jurafsky & Martin, 2026). Die klassische Architektur füllt die Slots eines Aufgaben-Frames: Sie versteht jede Äußerung, verfolgt den Dialogzustand, wählt den nächsten Dialogakt und erzeugt eine Antwort; Produktionsplattformen ergänzen Fallbacks für unerkannte oder fehlende Eingaben und die Eskalation an einen Menschen (Jurafsky & Martin, 2026; Dialogflow CX: Handlers). Heute werden deterministische Flows mit generativen, LLM-basierten Komponenten kombiniert (Dialogflow CX: Playbooks).

### Funktionsweise

Die Dialogue-State-Architektur teilt ein aufgabenorientiertes Dialogsystem in Komponenten, die einmal pro Nutzer-Turn laufen (Jurafsky & Martin, 2026):

```text
Sprache ─► ASR ─► NLU ─────────► Dialogzustand ─► Dialog-Policy ─► NLG ─► TTS ─► Sprache
                 (Domäne, Intent,  (alle Slots      (nächster Akt:     (Satz-
                  Slots)            bisher)          fragen, bestätigen, erzeugung)
                                                     antworten, ablehnen)
```

#### 1. Frames und Slots

Ein Frame beschreibt, was das System für eine Aufgabe wissen muss; er besteht aus Slots, die Werte annehmen, oft eines semantischen Typs wie CITY, DATE oder TIME. Ziel des Systems ist, die Slots mit den vom Nutzer gemeinten Werten zu füllen und dann die Aktion auszuführen, etwa eine Abfrage oder Buchung. Eine Menge von Frames heißt Domänenontologie; das Frame-Paradigma geht auf das Reisesystem GUS von 1977 zurück (Jurafsky & Martin, 2026).

#### 2. Die Äußerung verstehen

[[natural-language-understanding|Natural Language Understanding]] gewinnt aus jeder Äußerung drei Dinge: die Domäne, den Intent des Nutzers und die Slot-Werte, etwa SHOW-FLIGHTS mit Abflugort Boston und Ziel San Francisco (Jurafsky & Martin, 2026). In Sprachsystemen erzeugt zuvor die [[automatic-speech-recognition|automatische Spracherkennung]] den Text.

#### 3. Den Dialogzustand verfolgen

Der [[dialogue-state-tracking|Dialogue State Tracker]] hält den aktuellen Zustand des Frames, also alle bisherigen Vorgaben des Nutzers, und den jüngsten Dialogakt des Nutzers fest; Dialogakte wie INFORM, REQUEST, CONFIRM oder DENY beschreiben, was eine Äußerung tut (Jurafsky & Martin, 2026).

#### 4. Dialog-Policy: bestätigen, ablehnen, fragen

Die Dialog-Policy entscheidet, welcher Akt als Nächstes kommt: antworten, eine Rückfrage stellen, bestätigen oder ablehnen. Explizite Bestätigung („Ist das richtig?“) macht Korrekturen leicht, ist aber langsam und umständlich; implizite Bestätigung wiederholt das Verstandene in der nächsten Frage. Ablehnung („Das habe ich leider nicht verstanden“) drückt Nichtverstehen aus. Systeme können anhand der Konfidenz der Spracherkennung wählen, etwa unter einer Schwelle ablehnen, darüber explizit bestätigen und bei sehr hoher Konfidenz gar nicht bestätigen (Jurafsky & Martin, 2026).

#### 5. Die Antwort erzeugen

Natural Language Generation macht aus dem gewählten Akt und seinen Slots einen Satz. Trainierte Generatoren arbeiten oft mit delexikalisierten Beispielen, in denen Slot-Werte durch Platzhalter ersetzt sind, und setzen die Werte danach wieder ein (Jurafsky & Martin, 2026). In Sprachsystemen spricht [[text-to-speech|Text-to-Speech]] die Antwort.

#### 6. Fallback und Eskalation im Betrieb

Plattformen machen die Fehlerbehandlung explizit. In Dialogflow CX hat jeder Flow Handler für die eingebauten Ereignisse no-match (die Eingabe passt zu keinem Intent im Geltungsbereich) und no-input (keine Eingabe erhalten, etwa leeres oder unerkanntes Audio oder ein Timeout ohne Sprache); sie werden automatisch angelegt und lassen sich nicht löschen, und nummerierte Varianten erlauben eine andere Reaktion auf den ersten, zweiten und weitere Fehlschläge. Der Wunsch, mit einem Menschen zu sprechen, beendet einen Flow mit einem Human-Escalation-Ereignis, das die aufrufende Seite behandeln kann (Dialogflow CX: Handlers). Gesprächspfade werden als Flows aus Pages modelliert (Dialogflow CX: Flows).

#### 7. Herkunft und Varianten

ELIZA (Weizenbaum, 1966) war ein früher Chatbot aus Mustern und Aktionen; das System GUS aus den späten 1970ern begründete das Frame-Paradigma, das die Industrie über 30 Jahre prägte und um 2010 mit Assistenten wie Siri auf Smartphones kam; Dialogue State Tracking wurde durch eine jährliche Challenge-Reihe vorangebracht (Jurafsky & Martin, 2026). Generative Agenten bauen heute in jedem Turn einen LLM-Prompt aus Ziel, Anweisungen und Tools eines Playbooks und können Teilaufgaben an deterministische Flows abgeben (Dialogflow CX: Playbooks); siehe [[large-language-models|Large Language Models]] und [[agentic-ai|Agentic AI]].

### Wann einsetzen

- Für Kundenservice, Buchungen und andere Aufgaben mit bekannter Menge an Informationen, die erfragt werden müssen (Jurafsky & Martin, 2026).
- Flows, wenn die Gesprächspfade ausdrücklich als Pages und Routen festgelegt werden sollen; generative Playbooks, wenn ein LLM ein Ziel verfolgen soll, indem es Anweisungen folgt und Tools aufruft (Dialogflow CX: Flows; Dialogflow CX: Playbooks).
- In Sprachkanälen zusammen mit Spracherkennung und Sprachsynthese in einem [[voice-agents|Voice Agent]].

### Stärken und Grenzen

**Stärken**
- Das Frame-Slot-Modell macht klar, was das System noch wissen muss (Jurafsky & Martin, 2026).
- Explizite Fallback- und Eskalationspfade verhindern Gesprächssackgassen (Dialogflow CX: Handlers).
- Flows und generative Playbooks lassen sich in einem Agenten kombinieren (Dialogflow CX: Playbooks).

**Grenzen**
- Sprachsysteme verstehen Nutzer oft falsch; Korrekturen sind schwerer zu erkennen als normale Äußerungen, weil frustrierte Nutzer überdeutlich sprechen (Jurafsky & Martin, 2026).
- Alles zu bestätigen ist langsam und umständlich; nichts zu bestätigen lässt Fehler durch (Jurafsky & Martin, 2026).
- Generative Komponenten hängen an den Anweisungen im Prompt und brauchen dieselben Kontrollen wie andere LLM-Anwendungen (Dialogflow CX: Playbooks; [[hallucination-detection|Hallucination Detection]]).

### Vergleich

| Ansatz | Funktionsweise | Geeignet für |
|--------|----------------|--------------|
| Muster-Aktions-Chatbot | Regeln ordnen Mustern Antworten zu, wie bei ELIZA (Jurafsky & Martin, 2026) | Sehr enge, geskriptete Dialoge |
| Frame-basiertes Dialogsystem | NLU, State Tracking, Policy, NLG (Jurafsky & Martin, 2026) | Aufgaben mit bekannten Slots |
| Flow-basierte Plattform | Flows aus Pages, Routen, Event-Handler (Dialogflow CX: Flows; Dialogflow CX: Handlers) | Ausdrücklich modellierte Gesprächspfade |
| Generativer Agent | LLM-Prompt aus Ziel, Anweisungen und Tools (Dialogflow CX: Playbooks) | Freie Formulierung, Tool-Nutzung; siehe [[agentic-ai\|Agentic AI]] |

### In der Praxis

Task Success, der Anteil der Dialoge, in denen das System das Richtige getan hat, und die Slot Error Rate sind die Grundmaße, ergänzt um Effizienzkosten wie die Dialoglänge ([[conversation-analytics|Conversation Analytics]]; Jurafsky & Martin, 2026). Jeder Flow sollte festlegen, was nach wiederholten no-match- und no-input-Ereignissen passiert, bis hin zur Übergabe an einen Menschen (Dialogflow CX: Handlers). Fehler zeigen sich an Korrekturen der Nutzer, die sich an semantischen, phonetischen und prosodischen Merkmalen sowie an der ASR-Konfidenz erkennen lassen (Jurafsky & Martin, 2026).

### Merksatz

Conversational AI füllt über mehrere Turns einen Aufgaben-Frame, indem sie versteht, den Zustand verfolgt, den nächsten Akt wählt und antwortet; robuste Systeme planen Missverständnisse mit Bestätigung, Fallback und Eskalation an einen Menschen ein.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Frame-Based Dialogue Systems.* Speech and Language Processing, 3rd ed. draft, Appendix K. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/K.pdf)
- Google Cloud. *State handlers.* Dialogflow CX documentation. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/handler)
- Google Cloud. *Playbooks.* Dialogflow CX documentation. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/playbook)
- Google Cloud. *Flows.* Dialogflow CX documentation. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/flow)
