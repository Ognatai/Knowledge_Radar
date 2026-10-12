---
title_en: Dialogue State Tracking
title_de: Dialogue State Tracking
entity_type: Method
aliases:
- DST
- Belief tracking
- Dialogue state
sources:
- https://web.stanford.edu/~jurafsky/slp3/K.pdf
- https://arxiv.org/abs/1606.03777
- https://arxiv.org/abs/1810.00278
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Dialogue state tracking (DST), also called belief tracking, estimates the user's goal at every step of a dialogue: the current values of all slots of the task frame and the user's most recent dialogue act, accumulated over all turns rather than taken from the last sentence alone (Jurafsky & Martin, 2026; Mrkšić et al., 2017). It sits between [[natural-language-understanding|natural language understanding]] and the dialogue policy in a [[conversational-ai|conversational AI]] system and is trained and evaluated on annotated corpora such as MultiWOZ (Budzianowski et al., 2018).

### How it works

After every user turn, the tracker updates the state with what the turn adds, changes or requests (Jurafsky & Martin, 2026):

```text
User: I'm looking for a cheaper restaurant
  state: inform(price=cheap)
User: Thai food, somewhere downtown
  state: inform(price=cheap, food=Thai, area=centre)
User: Where is it?
  state: inform(price=cheap, food=Thai, area=centre); request(address)
```

#### 1. Dialogue acts

Dialogue acts generalise speech acts and say what an utterance does: HELLO, INFORM, REQUEST, CONFIRM, AFFIRM, NEGATE, DENY or BYE, each with the slot values it communicates, as in the HIS restaurant system (Jurafsky & Martin, 2026). Act detection works like intent classification: an encoder plus an act classifier, often given the previous act as well; because acts constrain slots and values, act detection and slot filling are often performed jointly (Jurafsky & Martin, 2026).

#### 2. Updating the state

The state is the entire frame at this point, summarising all of the user's constraints, not just the slot fillers of the current sentence. A tracker can simply take the output of a slot-filling sequence model after each sentence, or train a classifier that decides whether a value has changed (Jurafsky & Martin, 2026).

#### 3. Detecting corrections

When the system misunderstands, users repeat or rephrase. Such correction acts are important to detect, especially in speech, but harder to recognise than normal sentences, because frustrated users hyperarticulate, speaking louder, longer or with exaggerated pitch ("I said BAL-TI-MORE, not Boston"). Detectors use semantic similarity to the previous utterance, phonetic overlap, prosodic features and ASR confidence (Jurafsky & Martin, 2026).

#### 4. Learned trackers

Earlier trackers relied on language understanding models needing much annotated data or on hand-crafted lexicons of phrasings, and scaled poorly to larger domains. The Neural Belief Tracker composes pretrained word vectors into representations of the utterance and the dialogue context, matching lexicon-based models and outperforming them when no lexicon is available (Mrkšić et al., 2017).

#### 5. Data and evaluation

MultiWOZ is a fully labelled collection of about 10,000 human-human written dialogues across several domains, annotated with belief states and dialogue acts and collected by crowd-sourcing; it provides baselines for belief tracking, dialogue act prediction and response generation (Budzianowski et al., 2018). An annual challenge series evaluated state tracking algorithms and made DST a central problem of task-oriented dialogue (Jurafsky & Martin, 2026).

#### 6. Origin and variants

The dialogue-state model grew out of linguistic and machine learning work on dialogue acts in the 1990s (Jurafsky & Martin, 2026); data-driven trackers followed (Mrkšić et al., 2017), trained on corpora such as MultiWOZ (Budzianowski et al., 2018).

### When to use it

- In multi-turn task dialogues where users give information over several turns, change their mind or ask follow-up questions (Jurafsky & Martin, 2026).
- In voice systems, where recognition errors make corrections frequent (Jurafsky & Martin, 2026; [[automatic-speech-recognition|Automatic Speech Recognition]]).
- As the input of the dialogue policy, which decides whether to ask, confirm or answer ([[conversational-ai|Conversational AI]]).

### Strengths and limitations

**Strengths**
- Summarises all of the user's constraints so far, not only the last sentence (Jurafsky & Martin, 2026).
- Makes corrections and changed values explicit (Jurafsky & Martin, 2026).
- Learned trackers avoid hand-crafted lexicons (Mrkšić et al., 2017).

**Limitations**
- Needs dialogues annotated with states and acts, which are costly to collect (Budzianowski et al., 2018).
- Corrections are hard to detect, especially in speech (Jurafsky & Martin, 2026).
- Hand-crafted approaches scale poorly to larger, more complex domains (Mrkšić et al., 2017).

### Comparison

| Approach | State | Suited for |
|----------|-------|------------|
| Last-turn slot filling | Only the values of the current sentence (Jurafsky & Martin, 2026) | Single-turn commands |
| Rule- or lexicon-based tracker | Accumulated by hand-written rules (Mrkšić et al., 2017) | Small, stable domains |
| Learned tracker | Accumulated by a trained model (Mrkšić et al., 2017) | Larger domains with training data |

### In practice

State tracking quality shows in the slot error rate and in task success at dialogue level ([[conversation-analytics|Conversation Analytics]]; Jurafsky & Martin, 2026). Slot values extracted by [[natural-language-understanding|NLU]] are normalised to the canonical form of the ontology, for example with synonym dictionaries (Jurafsky & Martin, 2026).

### Key takeaway

Dialogue state tracking keeps the user's goal across turns as the full set of slot values and the latest dialogue act, and must catch corrections when the system has misunderstood.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Frame-Based Dialogue Systems.* Speech and Language Processing, 3rd ed. draft, Appendix K. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/K.pdf)
- Mrkšić, N., Ó Séaghdha, D., Wen, T.-H., Thomson, B. & Young, S. (2017). *Neural Belief Tracker: Data-Driven Dialogue State Tracking.* ACL 2017. [arxiv.org](https://arxiv.org/abs/1606.03777)
- Budzianowski, P. et al. (2018). *MultiWOZ: A Large-Scale Multi-Domain Wizard-of-Oz Dataset for Task-Oriented Dialogue Modelling.* EMNLP 2018. [arxiv.org](https://arxiv.org/abs/1810.00278)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Dialogue State Tracking (DST), auch Belief Tracking, schätzt in jedem Schritt eines Dialogs das Ziel des Nutzers: die aktuellen Werte aller Slots des Aufgaben-Frames und den jüngsten Dialogakt des Nutzers, gesammelt über alle Turns statt nur aus dem letzten Satz (Jurafsky & Martin, 2026; Mrkšić et al., 2017). Es liegt in einem [[conversational-ai|Conversational-AI]]-System zwischen [[natural-language-understanding|Natural Language Understanding]] und der Dialog-Policy und wird auf annotierten Korpora wie MultiWOZ trainiert und evaluiert (Budzianowski et al., 2018).

### Funktionsweise

Nach jedem Nutzer-Turn ergänzt der Tracker den Zustand um das, was der Turn hinzufügt, ändert oder erfragt (Jurafsky & Martin, 2026):

```text
User: I'm looking for a cheaper restaurant
  state: inform(price=cheap)
User: Thai food, somewhere downtown
  state: inform(price=cheap, food=Thai, area=centre)
User: Where is it?
  state: inform(price=cheap, food=Thai, area=centre); request(address)
```

#### 1. Dialogakte

Dialogakte verallgemeinern Sprechakte und sagen, was eine Äußerung tut: HELLO, INFORM, REQUEST, CONFIRM, AFFIRM, NEGATE, DENY oder BYE, jeweils mit den übermittelten Slot-Werten, wie im Restaurantsystem HIS (Jurafsky & Martin, 2026). Die Erkennung von Akten funktioniert wie die Intent-Klassifikation: ein Encoder plus ein Akt-Klassifikator, oft zusätzlich mit dem vorigen Akt als Eingabe; weil Akte Slots und Werte einschränken, werden Akterkennung und Slot Filling oft gemeinsam ausgeführt (Jurafsky & Martin, 2026).

#### 2. Den Zustand aktualisieren

Der Zustand ist der gesamte Frame zu diesem Zeitpunkt, der alle Vorgaben des Nutzers zusammenfasst, nicht nur die Slot-Werte des aktuellen Satzes. Ein Tracker kann einfach nach jedem Satz die Ausgabe eines Slot-Filling-Sequenzmodells übernehmen oder einen Klassifikator trainieren, der entscheidet, ob sich ein Wert geändert hat (Jurafsky & Martin, 2026).

#### 3. Korrekturen erkennen

Versteht das System etwas falsch, wiederholen oder formulieren Nutzer neu. Solche Korrekturakte zu erkennen ist wichtig, besonders bei Sprache, aber schwerer als bei normalen Sätzen, weil frustrierte Nutzer überdeutlich sprechen, lauter, länger oder mit übertriebener Tonhöhe („I said BAL-TI-MORE, not Boston“). Detektoren nutzen semantische Ähnlichkeit zur vorigen Äußerung, phonetische Überlappung, prosodische Merkmale und die ASR-Konfidenz (Jurafsky & Martin, 2026).

#### 4. Gelernte Tracker

Frühere Tracker stützten sich auf Sprachverstehensmodelle mit großem Bedarf an annotierten Daten oder auf handgefertigte Lexika von Formulierungen und skalierten schlecht auf größere Domänen. Der Neural Belief Tracker setzt vortrainierte Wortvektoren zu Darstellungen der Äußerung und des Dialogkontexts zusammen; er erreicht Lexikon-basierte Modelle und übertrifft sie, wenn kein Lexikon vorhanden ist (Mrkšić et al., 2017).

#### 5. Daten und Evaluation

MultiWOZ ist eine vollständig annotierte Sammlung von rund 10.000 geschriebenen Mensch-Mensch-Dialogen über mehrere Domänen, annotiert mit Belief States und Dialogakten und per Crowdsourcing gesammelt; sie liefert Baselines für Belief Tracking, die Vorhersage von Dialogakten und die Antwortgenerierung (Budzianowski et al., 2018). Eine jährliche Challenge-Reihe evaluierte State-Tracking-Algorithmen und machte DST zu einem zentralen Problem aufgabenorientierter Dialoge (Jurafsky & Martin, 2026).

#### 6. Herkunft und Varianten

Das Dialogue-State-Modell entstand aus linguistischer und Machine-Learning-Arbeit zu Dialogakten in den 1990er-Jahren (Jurafsky & Martin, 2026); datengetriebene Tracker folgten (Mrkšić et al., 2017), trainiert auf Korpora wie MultiWOZ (Budzianowski et al., 2018).

### Wann einsetzen

- In aufgabenorientierten Dialogen über mehrere Turns, in denen Nutzer Informationen nach und nach geben, ihre Meinung ändern oder nachfragen (Jurafsky & Martin, 2026).
- In Sprachsystemen, in denen Erkennungsfehler Korrekturen häufig machen (Jurafsky & Martin, 2026; [[automatic-speech-recognition|Automatische Spracherkennung]]).
- Als Eingabe der Dialog-Policy, die entscheidet, ob gefragt, bestätigt oder geantwortet wird ([[conversational-ai|Conversational AI]]).

### Stärken und Grenzen

**Stärken**
- Fasst alle bisherigen Vorgaben des Nutzers zusammen, nicht nur den letzten Satz (Jurafsky & Martin, 2026).
- Macht Korrekturen und geänderte Werte ausdrücklich (Jurafsky & Martin, 2026).
- Gelernte Tracker kommen ohne handgefertigte Lexika aus (Mrkšić et al., 2017).

**Grenzen**
- Braucht mit Zuständen und Akten annotierte Dialoge, deren Erhebung aufwendig ist (Budzianowski et al., 2018).
- Korrekturen sind schwer zu erkennen, besonders bei Sprache (Jurafsky & Martin, 2026).
- Handgefertigte Ansätze skalieren schlecht auf größere, komplexere Domänen (Mrkšić et al., 2017).

### Vergleich

| Ansatz | Zustand | Geeignet für |
|--------|---------|--------------|
| Slot Filling nur im letzten Turn | Nur die Werte des aktuellen Satzes (Jurafsky & Martin, 2026) | Einzelne Befehle |
| Regel- oder Lexikon-basierter Tracker | Gesammelt durch handgeschriebene Regeln (Mrkšić et al., 2017) | Kleine, stabile Domänen |
| Gelernter Tracker | Gesammelt durch ein trainiertes Modell (Mrkšić et al., 2017) | Größere Domänen mit Trainingsdaten |

### In der Praxis

Die Qualität des State Trackings zeigt sich in der Slot Error Rate und im Task Success auf Dialogebene ([[conversation-analytics|Conversation Analytics]]; Jurafsky & Martin, 2026). Von der [[natural-language-understanding|NLU]] gefundene Slot-Werte werden auf die kanonische Form der Ontologie gebracht, etwa mit Synonymwörterbüchern (Jurafsky & Martin, 2026).

### Merksatz

Dialogue State Tracking hält das Ziel des Nutzers über alle Turns als vollständige Menge der Slot-Werte und den jüngsten Dialogakt fest und muss Korrekturen erkennen, wenn das System etwas falsch verstanden hat.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Frame-Based Dialogue Systems.* Speech and Language Processing, 3rd ed. draft, Appendix K. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/K.pdf)
- Mrkšić, N., Ó Séaghdha, D., Wen, T.-H., Thomson, B. & Young, S. (2017). *Neural Belief Tracker: Data-Driven Dialogue State Tracking.* ACL 2017. [arxiv.org](https://arxiv.org/abs/1606.03777)
- Budzianowski, P. et al. (2018). *MultiWOZ: A Large-Scale Multi-Domain Wizard-of-Oz Dataset for Task-Oriented Dialogue Modelling.* EMNLP 2018. [arxiv.org](https://arxiv.org/abs/1810.00278)
