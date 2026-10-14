---
title_en: Conversation Design
title_de: Conversation Design
entity_type: Method
aliases:
- Conversation design
- Conversational design
- Conversational UX
- Voice user interface design
- Dialogdesign
sources:
- https://developers.google.com/assistant/conversation-design/what-is-conversation-design
- https://developers.google.com/assistant/conversation-design/learn-about-conversation
- https://developers.google.com/assistant/conversation-design/create-a-persona
- https://developers.google.com/assistant/conversation-design/write-sample-dialogs
- https://developers.google.com/assistant/conversation-design/errors
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Conversation design is "a design language based on human conversation" for chat and voice interfaces, combining voice user interface, interaction, visual, motion and audio design with UX writing (Google, What is). It applies how people actually talk, cooperation, turn-taking, implicature and context, to the design of assistants: a consistent persona, sample dialogs that are role-played and read aloud before any flow is built, and deliberate handling of errors such as not understanding or not hearing the user (Google, Learn about conversation; Google, Persona; Google, Sample dialogs; Google, Errors). The technical side, understanding the user and tracking the dialogue, is covered in [[conversational-ai|conversational AI]]; conversation design decides what the system says and when.

### How it works

```text
requirements: users, use cases, constraints
 ▼
persona: 4–6 core traits, matching voice
 ▼
sample dialogs: role-play, transcribe, listen to prompts via TTS
 ▼
flow: abstract paths, shortcuts for experienced users
 ▼
prompts and repair: brief turns, one question at a time, reprompts for No Match / No Input
 ▼
test with users, analyse real conversations, iterate
```

#### 1. Principles from human conversation

People assume "an undercurrent of cooperation between conversational participants" and expect a system persona to cooperate in the same way (Google, Learn about conversation). Grice's maxims translate into design rules: quality (be truthful), quantity (as much information as needed, neither more nor less), relevance (stay on topic) and manner (clear, without ambiguity). Turn-taking keeps both sides in sync, so each prompt should ask "only a single question at a time" and make clear when the user is expected to speak. Implicature means that "knowing what someone said is not the same as knowing what they meant": a "thanks" or "I'm done" may end the conversation. Context matters because utterances often cannot be understood in isolation; earlier turns resolve pronouns and follow-up questions, and on multimodal devices on-screen content is part of the context (Google, Learn about conversation). Resolving such references is the job of [[dialogue-state-tracking|dialogue state tracking]].

#### 2. Persona

"Users will project a persona onto your Action whether you plan for one or not", so designing it deliberately makes the experience consistent and builds trust (Google, Persona). Google recommends listing adjectives for the qualities users should perceive, narrowing them to four to six core traits, imagining characters that embody them, writing a short description of how the chosen character would speak and act, focusing on personality rather than gender or age, and choosing a voice that matches the traits, using the adjectives as a scorecard when auditioning voices (Google, Persona). Synthetic voices are covered in [[text-to-speech|text-to-speech]].

#### 3. Sample dialogs before flows

Sample dialogs give "a quick, low-fidelity sense of the 'sound-and-feel' of the interaction" (Google, Sample dialogs). Two people role-play one persona and one key use case, record it and transcribe it as the first draft; this is repeated for other personas and use cases. Each system prompt is then listened to through text-to-speech, because written prompts often sound wrong when spoken. Only after several dialogs exist is the flow abstracted from them, as a map of how users move through the interface that balances clear paths with shortcuts for experienced users (Google, Sample dialogs).

#### 4. Errors and repair

Google distinguishes three error types (Google, Errors): No Match, when the system cannot interpret the user's response in context; No Input, when it heard nothing in time; and system errors, when it understood but a dependent system failed. After a first No Match, a rapid reprompt apologises briefly and asks a condensed version of the question without repeating the original verbatim; after a second, it escalates with options or examples, which give users "an implicit model of what to say and how to say it". No Input is handled by rephrasing and then restating the question. After two failed attempts, and at most three consecutive errors overall, the system ends politely, points to alternative ways to complete the task and avoids vague promises (Google, Errors). Fallback and escalation to a human agent are covered in [[conversational-ai|conversational AI]].

#### 5. Writing turns

Turns should be "brief and optimally relevant from the user's point of view", repairs short and language plain, without technical terms users would not recognise (Google, Learn about conversation). Interfaces built for screens rarely work unchanged as conversation, so conversation design should not be an afterthought (Google, What is).

#### Origin and variants

Google published its conversation design guidelines for the Google Assistant; Conversational Actions themselves were deprecated on 13 June 2023, while the design guidelines are still published (Google, What is). For LLM-based assistants, the corresponding levers are system prompts ([[prompt-engineering|prompt engineering]]) and runtime checks ([[llm-guardrails-and-red-teaming|LLM guardrails]]).

### When to use it

- Designing chatbots or voice assistants for customer service, where dialogue quality decides whether users complete their task without escalation (Google, Errors).
- Voice-only channels, where there is no screen to fall back on and prompts must work when heard (Google, Sample dialogs), see [[voice-agents|voice agents]].
- Moving an existing graphical process to a conversational channel, whose logic rarely transfers as is (Google, What is).

### Strengths and limitations

**Strengths**
- Interfaces that follow human conversation need less user training (Google, What is).
- A persona with defined traits keeps tone and voice consistent across all prompts (Google, Persona).
- Sample dialogs and role-play find problems cheaply before anything is built (Google, Sample dialogs).
- Defined repair strategies reduce frustration and dead ends (Google, Errors).

**Limitations**
- The Google Assistant platform for which the guidelines were written has been deprecated (Google, What is).

### Comparison

| | Conversation design | [[conversational-ai\|Conversational AI]] engineering |
|---|---|---|
| Question | What does the system say, how and when? | How does the system understand and decide? |
| Artefacts | persona, sample dialogs, flows, prompts, repair strategies | NLU models, dialogue state, policies, integrations |
| Evaluation | user tests, transcript reviews | intent accuracy, containment, task success ([[conversation-analytics\|conversation analytics]]) |

Sources: Google (What is; Sample dialogs; Errors).

### In practice

Prompts are tested by listening to them through text-to-speech and by testing with users, then iterated (Google, Sample dialogs). Analysing real conversations for misunderstood turns and missing paths is covered in [[conversation-analytics|conversation analytics]]. Recognising what users mean is covered in [[natural-language-understanding|natural language understanding]].

### Key takeaway

Conversation design applies the rules of human conversation, cooperation, brevity, one question per turn, context and graceful repair, through a consistent persona, role-played sample dialogs and explicit error handling, before and alongside the technical build of a chat or voice assistant.

### Sources

- Google, What is. *What is conversation design?* Google Assistant conversation design guidelines. [developers.google.com](https://developers.google.com/assistant/conversation-design/what-is-conversation-design)
- Google, Learn about conversation. *Learn about conversation.* [developers.google.com](https://developers.google.com/assistant/conversation-design/learn-about-conversation)
- Google, Persona. *Create a persona.* [developers.google.com](https://developers.google.com/assistant/conversation-design/create-a-persona)
- Google, Sample dialogs. *Write sample dialogs.* [developers.google.com](https://developers.google.com/assistant/conversation-design/write-sample-dialogs)
- Google, Errors. *Errors.* [developers.google.com](https://developers.google.com/assistant/conversation-design/errors)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Conversation Design ist „a design language based on human conversation“ für Chat- und Sprachschnittstellen und verbindet Voice User Interface Design, Interaktions-, visuelles, Motion- und Audiodesign mit UX Writing (Google, What is). Es überträgt, wie Menschen tatsächlich sprechen, Kooperation, Sprecherwechsel, Implikatur und Kontext, auf die Gestaltung von Assistenten: eine konsistente Persona, Beispieldialoge, die nachgespielt und laut gelesen werden, bevor ein Ablauf gebaut wird, und bewusster Umgang mit Fehlern, etwa wenn das System die Nutzenden nicht versteht oder nicht hört (Google, Learn about conversation; Google, Persona; Google, Sample dialogs; Google, Errors). Die technische Seite, das Verstehen der Nutzenden und das Verfolgen des Dialogs, behandelt [[conversational-ai|Conversational AI]]; Conversation Design entscheidet, was das System wann sagt.

### Funktionsweise

```text
Anforderungen: Nutzende, Anwendungsfälle, Rahmenbedingungen
 ▼
Persona: 4–6 Kerneigenschaften, passende Stimme
 ▼
Beispieldialoge: nachspielen, transkribieren, Prompts per TTS anhören
 ▼
Ablauf: Pfade abstrahieren, Abkürzungen für Erfahrene
 ▼
Prompts und Reparatur: kurze Beiträge, eine Frage pro Turn, Reprompts bei No Match / No Input
 ▼
mit Nutzenden testen, echte Gespräche auswerten, iterieren
```

#### 1. Prinzipien aus menschlichen Gesprächen

Menschen setzen „an undercurrent of cooperation between conversational participants“ voraus und erwarten, dass eine Systempersona ebenso kooperiert (Google, Learn about conversation). Die Konversationsmaximen von Grice werden zu Gestaltungsregeln: Qualität (wahrhaftig sein), Quantität (so viel Information wie nötig, nicht mehr und nicht weniger), Relevanz (beim Thema bleiben) und Modalität (klar, ohne Mehrdeutigkeit). Sprecherwechsel hält beide Seiten im Takt, daher sollte jeder Prompt „only a single question at a time“ stellen und deutlich machen, wann die Nutzenden sprechen sollen. Implikatur heißt, dass „knowing what someone said is not the same as knowing what they meant“: Ein „Danke“ oder „Das war's“ kann das Gespräch beenden. Kontext zählt, weil Äußerungen oft nicht isoliert verständlich sind; frühere Beiträge klären Pronomen und Anschlussfragen, und auf multimodalen Geräten gehören Bildschirminhalte zum Kontext (Google, Learn about conversation). Solche Bezüge aufzulösen, ist Aufgabe des [[dialogue-state-tracking|Dialogue State Tracking]].

#### 2. Persona

„Users will project a persona onto your Action whether you plan for one or not“, daher macht eine bewusst gestaltete Persona das Erlebnis konsistent und schafft Vertrauen (Google, Persona). Google empfiehlt, Adjektive für die Eigenschaften zu sammeln, die Nutzende wahrnehmen sollen, sie auf vier bis sechs Kerneigenschaften einzugrenzen, sich Figuren vorzustellen, die sie verkörpern, kurz zu beschreiben, wie die gewählte Figur spricht und handelt, sich auf die Persönlichkeit statt auf Geschlecht oder Alter zu konzentrieren und eine passende Stimme zu wählen, wobei die Adjektive beim Vergleich von Stimmen als Bewertungsbogen dienen (Google, Persona). Synthetische Stimmen behandelt [[text-to-speech|Text-to-Speech]].

#### 3. Beispieldialoge vor Abläufen

Beispieldialoge geben „a quick, low-fidelity sense of the 'sound-and-feel' of the interaction“ (Google, Sample dialogs). Zwei Personen spielen eine Persona und einen zentralen Anwendungsfall nach, nehmen das Gespräch auf und transkribieren es als ersten Entwurf; das wird für weitere Personas und Anwendungsfälle wiederholt. Jeder Systemprompt wird anschließend per Text-to-Speech angehört, weil geschriebene Prompts gesprochen oft falsch klingen. Erst wenn mehrere Dialoge vorliegen, wird daraus der Ablauf abstrahiert, als Karte, wie sich Nutzende durch die Schnittstelle bewegen, die klare Pfade mit Abkürzungen für Erfahrene verbindet (Google, Sample dialogs).

#### 4. Fehler und Reparatur

Google unterscheidet drei Fehlerarten (Google, Errors): No Match, wenn das System die Antwort im Kontext nicht deuten kann; No Input, wenn es rechtzeitig nichts gehört hat; und Systemfehler, wenn es verstanden hat, aber ein abhängiges System versagt. Nach einem ersten No Match entschuldigt sich ein schneller Reprompt kurz und stellt eine verkürzte Fassung der Frage, ohne das Original wörtlich zu wiederholen; nach einem zweiten wird mit Optionen oder Beispielen eskaliert, die Nutzenden „an implicit model of what to say and how to say it“ geben. No Input wird durch Umformulieren und anschließend erneutes Stellen der Frage behandelt. Nach zwei erfolglosen Versuchen und höchstens drei aufeinanderfolgenden Fehlern insgesamt beendet das System höflich, verweist auf andere Wege, die Aufgabe zu erledigen, und vermeidet vage Versprechen (Google, Errors). Fallback und Übergabe an eine Person behandelt [[conversational-ai|Conversational AI]].

#### 5. Beiträge formulieren

Beiträge sollten „brief and optimally relevant from the user's point of view“ sein, Reparaturen kurz und die Sprache einfach, ohne Fachbegriffe, die Nutzende nicht kennen (Google, Learn about conversation). Für Bildschirme gebaute Oberflächen funktionieren selten unverändert als Gespräch, daher sollte Conversation Design kein nachträglicher Gedanke sein (Google, What is).

#### Herkunft und Varianten

Google veröffentlichte seine Richtlinien zum Conversation Design für den Google Assistant; die Conversational Actions selbst wurden am 13. Juni 2023 eingestellt, die Gestaltungsrichtlinien sind aber weiterhin veröffentlicht (Google, What is). Bei LLM-basierten Assistenten sind die entsprechenden Stellschrauben System-Prompts ([[prompt-engineering|Prompt Engineering]]) und Prüfungen zur Laufzeit ([[llm-guardrails-and-red-teaming|LLM-Guardrails]]).

### Wann einsetzen

- Beim Gestalten von Chatbots oder Sprachassistenten im Kundenservice, wo die Dialogqualität entscheidet, ob Nutzende ihre Aufgabe ohne Eskalation erledigen (Google, Errors).
- In reinen Sprachkanälen ohne Bildschirm als Rückfallebene, in denen Prompts beim Hören funktionieren müssen (Google, Sample dialogs), siehe [[voice-agents|Voice Agents]].
- Beim Übertragen eines bestehenden grafischen Prozesses in einen Gesprächskanal, dessen Logik selten unverändert passt (Google, What is).

### Stärken und Grenzen

**Stärken**
- Oberflächen, die menschlichen Gesprächen folgen, erfordern weniger Einarbeitung (Google, What is).
- Eine Persona mit festgelegten Eigenschaften hält Ton und Stimme über alle Prompts konsistent (Google, Persona).
- Beispieldialoge und Rollenspiel finden Probleme günstig, bevor etwas gebaut wird (Google, Sample dialogs).
- Festgelegte Reparaturstrategien verringern Frust und Sackgassen (Google, Errors).

**Grenzen**
- Die Plattform Google Assistant, für die die Richtlinien geschrieben wurden, ist eingestellt (Google, What is).

### Vergleich

| | Conversation Design | Engineering für [[conversational-ai\|Conversational AI]] |
|---|---|---|
| Frage | Was sagt das System, wie und wann? | Wie versteht und entscheidet das System? |
| Artefakte | Persona, Beispieldialoge, Abläufe, Prompts, Reparaturstrategien | NLU-Modelle, Dialogzustand, Policies, Integrationen |
| Bewertung | Nutzertests, Durchsicht von Transkripten | Intent-Genauigkeit, Containment, Aufgabenerfolg ([[conversation-analytics\|Conversation Analytics]]) |

Quellen: Google (What is; Sample dialogs; Errors).

### In der Praxis

Prompts werden geprüft, indem sie per Text-to-Speech angehört und mit Nutzenden getestet werden, und dann überarbeitet (Google, Sample dialogs). Die Auswertung echter Gespräche auf missverstandene Beiträge und fehlende Pfade behandelt [[conversation-analytics|Conversation Analytics]]. Das Erkennen dessen, was Nutzende meinen, behandelt [[natural-language-understanding|Natural Language Understanding]].

### Merksatz

Conversation Design überträgt die Regeln menschlicher Gespräche, Kooperation, Kürze, eine Frage pro Beitrag, Kontext und behutsame Reparatur, über eine konsistente Persona, nachgespielte Beispieldialoge und explizite Fehlerbehandlung auf Chat- und Sprachassistenten, vor und neben deren technischem Aufbau.

### Quellen

- Google, What is. *What is conversation design?* Richtlinien zum Conversation Design für den Google Assistant. [developers.google.com](https://developers.google.com/assistant/conversation-design/what-is-conversation-design)
- Google, Learn about conversation. *Learn about conversation.* [developers.google.com](https://developers.google.com/assistant/conversation-design/learn-about-conversation)
- Google, Persona. *Create a persona.* [developers.google.com](https://developers.google.com/assistant/conversation-design/create-a-persona)
- Google, Sample dialogs. *Write sample dialogs.* [developers.google.com](https://developers.google.com/assistant/conversation-design/write-sample-dialogs)
- Google, Errors. *Errors.* [developers.google.com](https://developers.google.com/assistant/conversation-design/errors)
