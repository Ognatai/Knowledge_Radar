---
title_en: Voice Agents
title_de: Voice Agents
entity_type: Concept
aliases:
- Voice agent
- Voice bot
- Voicebot
- Speech pipeline
sources:
- https://docs.livekit.io/agents/build/turns/
- https://web.stanford.edu/~jurafsky/slp3/K.pdf
- https://docs.cloud.google.com/dialogflow/cx/docs/concept/handler
- https://github.com/snakers4/silero-vad
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A voice agent is a [[conversational-ai|conversational AI]] system that users talk to, for example on the phone: it hears speech, decides what to do and answers with synthesised speech, in real time and with natural turn-taking (Jurafsky & Martin, 2026; LiveKit docs: Turns). It is built either as a pipeline of speech-to-text, a language model and text-to-speech, or on a realtime model that handles audio directly; in both cases voice activity detection and turn detection decide when the user has finished and when they interrupt (LiveKit docs: Turns).

### How it works

```text
caller audio ─► VAD ─► turn detection ─► STT ─► LLM / dialogue logic ─► TTS ─► agent audio
                 │                                (tools, APIs, state)          ▲
                 └────────────── user speech while agent talks: interrupt ──────┘
```

#### 1. The speech pipeline

The dialogue-state architecture already places [[automatic-speech-recognition|automatic speech recognition]] before understanding and [[text-to-speech|speech synthesis]] after generation (Jurafsky & Martin, 2026). Voice [[agent-frameworks|agent frameworks]] call this the STT-LLM-TTS pipeline, in which the language model does the understanding and response generation; alternatively, realtime models take audio in and produce audio out and bring their own turn detection (LiveKit docs: Turns).

#### 2. Hearing: VAD and turn detection

[[voice-activity-detection|Voice activity detection]] finds periods of silence in the user's audio; heuristics on top of it decide whether a sentence or thought has ended (LiveKit docs: Turns). Endpointing waits between a configurable minimum and maximum delay before ending the turn; dynamic endpointing adapts this delay to the pauses observed in the session; a semantic turn detector predicts the end of a turn from the meaning and the acoustics of speech, on top of VAD (LiveKit docs: Turns). Lightweight neural VADs process a 30 ms chunk in under a millisecond on a CPU (Silero VAD).

#### 3. Interruptions (barge-in)

The agent pauses its own speech whenever it detects user speech; when a VAD is used, interim transcripts do not trigger an interruption, but final transcripts do. If the detected speech was not real, the interruption is a false positive and the agent resumes from where it stopped. In adaptive mode, the framework briefly stops treating VAD speech as an interruption after the agent starts speaking and re-enables it once a genuine interruption is identified (LiveKit docs: Turns).

#### 4. Thinking: dialogue logic and tools

Between hearing and speaking, the agent fills the slots of the task, tracks the [[dialogue-state-tracking|dialogue state]] and decides on the next act: answer, ask, confirm or reject; speech systems in particular must confirm or reject when recognition confidence is low (Jurafsky & Martin, 2026). Back-end actions such as looking up a contract go through [[apis|APIs]]; slow calls are handled with [[asynchronous-apis|asynchronous APIs]].

#### 5. Failure paths

If no input arrives, including empty or unrecognised audio or a no-speech timeout, a no-input event is raised; input that matches nothing raises no-match; and a request to talk to a person ends the flow with a human-escalation event (Dialogflow CX: Handlers). Users who are misunderstood repeat themselves with hyperarticulated speech, which is even harder for recognisers (Jurafsky & Martin, 2026).

#### 6. Origin and variants

Spoken dialogue systems with the frame-based architecture reached phones with assistants such as Siri around 2010 (Jurafsky & Martin, 2026). Current agents either chain STT, an LLM and TTS or use realtime speech models with built-in turn detection, such as the Gemini Live API (LiveKit docs: Turns).

### When to use it

- For telephone service, call-centre automation and voice bots (Silero VAD; Jurafsky & Martin, 2026).
- The pipeline when each stage should be chosen and controlled separately; a realtime model when turn-taking should be left to the model (LiveKit docs: Turns).

### Strengths and limitations

**Strengths**
- Turn detection is configurable: endpointing delays, VAD and a semantic turn detector (LiveKit docs: Turns).
- Voice activity detection is cheap enough to run on a CPU in real time (Silero VAD).
- Interruptions and false interruptions are handled explicitly (LiveKit docs: Turns).

**Limitations**
- Recognition errors are frequent in speech and propagate into understanding (Jurafsky & Martin, 2026).
- Turn-taking is hard: silence alone does not mark the end of a turn (LiveKit docs: Turns).
- With server-side turn detection in a realtime model, the model decides about interruptions and client-side control is limited (LiveKit docs: Turns).

### Comparison

| Approach | How it works | Control |
|----------|--------------|---------|
| STT-LLM-TTS pipeline | Separate stages with VAD and turn detector (LiveKit docs: Turns) | Each stage configurable |
| Realtime speech model | Audio in, audio out, built-in turn detection (LiveKit docs: Turns) | Turn-taking left to the model |
| Flow-based voice bot | Pages, intents and event handlers (Dialogflow CX: Handlers) | Explicit paths and fallbacks |

### In practice

Every voice flow needs answers to no-input, no-match and repeated failures, ending with a handover to a human agent (Dialogflow CX: Handlers). Endpointing delays can be fixed or adapted dynamically to the pauses of a session (LiveKit docs: Turns). Quality is followed with the measures in [[conversation-analytics|Conversation Analytics]].

### Key takeaway

A voice agent chains hearing, thinking and speaking in real time; its quality depends as much on turn detection, interruption handling and failure paths as on the language model.

### Sources

- LiveKit. *Turns overview.* LiveKit Agents documentation. [docs.livekit.io](https://docs.livekit.io/agents/build/turns/)
- Jurafsky, D. & Martin, J. H. (2026). *Frame-Based Dialogue Systems.* Speech and Language Processing, 3rd ed. draft, Appendix K. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/K.pdf)
- Google Cloud. *State handlers.* Dialogflow CX documentation. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/handler)
- Silero Team. *Silero VAD.* GitHub repository. [github.com](https://github.com/snakers4/silero-vad)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Voice Agent ist ein [[conversational-ai|Conversational-AI]]-System, mit dem Nutzer sprechen, etwa am Telefon: Es hört Sprache, entscheidet, was zu tun ist, und antwortet mit synthetisierter Sprache, in Echtzeit und mit natürlichem Sprecherwechsel (Jurafsky & Martin, 2026; LiveKit docs: Turns). Gebaut wird er entweder als Pipeline aus Speech-to-Text, einem Sprachmodell und Text-to-Speech oder auf einem Realtime-Modell, das Audio direkt verarbeitet; in beiden Fällen entscheiden Voice Activity Detection und Turn Detection, wann der Nutzer fertig ist und wann er unterbricht (LiveKit docs: Turns).

### Funktionsweise

```text
Anrufer-Audio ─► VAD ─► Turn Detection ─► STT ─► LLM / Dialoglogik ─► TTS ─► Agenten-Audio
                  │                                 (Tools, APIs, Zustand)         ▲
                  └────────── Nutzer spricht, während der Agent spricht: Unterbrechung ┘
```

#### 1. Die Sprach-Pipeline

Schon die Dialogue-State-Architektur setzt die [[automatic-speech-recognition|automatische Spracherkennung]] vor das Verstehen und die [[text-to-speech|Sprachsynthese]] hinter die Generierung (Jurafsky & Martin, 2026). Frameworks für Voice Agents nennen das die STT-LLM-TTS-Pipeline, in der das Sprachmodell Verstehen und Antwortgenerierung übernimmt; alternativ nehmen Realtime-Modelle Audio entgegen, geben Audio aus und bringen ihre eigene Turn Detection mit (LiveKit docs: Turns).

#### 2. Hören: VAD und Turn Detection

[[voice-activity-detection|Voice Activity Detection]] findet Stille im Audio des Nutzers; Heuristiken darauf entscheiden, ob ein Satz oder Gedanke zu Ende ist (LiveKit docs: Turns). Endpointing wartet zwischen einer einstellbaren minimalen und maximalen Verzögerung, bevor der Turn endet; dynamisches Endpointing passt diese Verzögerung an die in der Sitzung beobachteten Pausen an; ein semantischer Turn Detector sagt das Ende eines Turns zusätzlich zur VAD aus Bedeutung und Akustik der Sprache voraus (LiveKit docs: Turns). Leichte neuronale VADs verarbeiten einen 30-ms-Abschnitt in unter einer Millisekunde auf einer CPU (Silero VAD).

#### 3. Unterbrechungen (Barge-in)

Der Agent pausiert seine Sprachausgabe, sobald er Sprache des Nutzers erkennt; wird eine VAD genutzt, lösen vorläufige Transkripte keine Unterbrechung aus, endgültige schon. War die erkannte Sprache keine echte, ist die Unterbrechung ein Fehlalarm, und der Agent spricht an der Stelle weiter, an der er aufgehört hat. Im adaptiven Modus behandelt das Framework VAD-Sprache kurz nach Beginn der Agentenausgabe nicht als Unterbrechung und aktiviert das wieder, sobald eine echte Unterbrechung erkannt ist (LiveKit docs: Turns).

#### 4. Denken: Dialoglogik und Tools

Zwischen Hören und Sprechen füllt der Agent die Slots der Aufgabe, verfolgt den [[dialogue-state-tracking|Dialogzustand]] und entscheidet über den nächsten Akt: antworten, fragen, bestätigen oder ablehnen; gerade Sprachsysteme müssen bei geringer Erkennungskonfidenz bestätigen oder ablehnen (Jurafsky & Martin, 2026). Aktionen im Backend, etwa das Nachschlagen eines Vertrags, laufen über [[apis|APIs]]; langsame Aufrufe werden mit [[asynchronous-apis|asynchronen APIs]] behandelt.

#### 5. Fehlerpfade

Kommt keine Eingabe, auch leeres oder unerkanntes Audio oder ein Timeout ohne Sprache, wird ein no-input-Ereignis ausgelöst; eine Eingabe, die zu nichts passt, löst no-match aus; und der Wunsch, mit einem Menschen zu sprechen, beendet den Flow mit einem Human-Escalation-Ereignis (Dialogflow CX: Handlers). Falsch verstandene Nutzer wiederholen sich mit überdeutlicher Sprache, die für Erkenner noch schwieriger ist (Jurafsky & Martin, 2026).

#### 6. Herkunft und Varianten

Gesprochene Dialogsysteme mit Frame-Architektur kamen um 2010 mit Assistenten wie Siri auf Smartphones (Jurafsky & Martin, 2026). Heutige Agenten verketten entweder STT, ein LLM und TTS oder nutzen Realtime-Sprachmodelle mit eingebauter Turn Detection wie die Gemini Live API (LiveKit docs: Turns).

### Wann einsetzen

- Für Telefonservice, Callcenter-Automatisierung und Voicebots (Silero VAD; Jurafsky & Martin, 2026).
- Die Pipeline, wenn jede Stufe einzeln gewählt und gesteuert werden soll; ein Realtime-Modell, wenn der Sprecherwechsel dem Modell überlassen werden soll (LiveKit docs: Turns).

### Stärken und Grenzen

**Stärken**
- Die Turn Detection ist einstellbar: Endpointing-Verzögerungen, VAD und ein semantischer Turn Detector (LiveKit docs: Turns).
- Voice Activity Detection ist günstig genug, um in Echtzeit auf einer CPU zu laufen (Silero VAD).
- Unterbrechungen und Fehlalarme werden ausdrücklich behandelt (LiveKit docs: Turns).

**Grenzen**
- Erkennungsfehler sind bei Sprache häufig und setzen sich ins Verstehen fort (Jurafsky & Martin, 2026).
- Der Sprecherwechsel ist schwierig: Stille allein markiert nicht das Ende eines Turns (LiveKit docs: Turns).
- Mit serverseitiger Turn Detection in einem Realtime-Modell entscheidet das Modell über Unterbrechungen, die Steuerung auf Client-Seite ist begrenzt (LiveKit docs: Turns).

### Vergleich

| Ansatz | Funktionsweise | Steuerung |
|--------|----------------|-----------|
| STT-LLM-TTS-Pipeline | Getrennte Stufen mit VAD und Turn Detector (LiveKit docs: Turns) | Jede Stufe einstellbar |
| Realtime-Sprachmodell | Audio rein, Audio raus, eingebaute Turn Detection (LiveKit docs: Turns) | Sprecherwechsel dem Modell überlassen |
| Flow-basierter Voicebot | Pages, Intents und Event-Handler (Dialogflow CX: Handlers) | Ausdrückliche Pfade und Fallbacks |

### In der Praxis

Jeder Sprach-Flow braucht Antworten auf no-input, no-match und wiederholte Fehlschläge, bis hin zur Übergabe an einen Menschen (Dialogflow CX: Handlers). Endpointing-Verzögerungen können fest sein oder sich dynamisch an die Pausen einer Sitzung anpassen (LiveKit docs: Turns). Die Qualität wird mit den Maßen aus [[conversation-analytics|Conversation Analytics]] verfolgt.

### Merksatz

Ein Voice Agent verkettet Hören, Denken und Sprechen in Echtzeit; seine Qualität hängt ebenso von Turn Detection, Umgang mit Unterbrechungen und Fehlerpfaden ab wie vom Sprachmodell.

### Quellen

- LiveKit. *Turns overview.* LiveKit Agents documentation. [docs.livekit.io](https://docs.livekit.io/agents/build/turns/)
- Jurafsky, D. & Martin, J. H. (2026). *Frame-Based Dialogue Systems.* Speech and Language Processing, 3rd ed. draft, Appendix K. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/K.pdf)
- Google Cloud. *State handlers.* Dialogflow CX documentation. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/handler)
- Silero Team. *Silero VAD.* GitHub repository. [github.com](https://github.com/snakers4/silero-vad)
