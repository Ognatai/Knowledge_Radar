---
title_en: Natural Language Understanding (NLU)
title_de: Natural Language Understanding (NLU)
entity_type: Method
aliases:
- NLU
- Intent classification
- Intent detection
- Slot filling
sources:
- https://web.stanford.edu/~jurafsky/slp3/K.pdf
- https://arxiv.org/abs/1902.10909
- https://docs.cloud.google.com/dialogflow/cx/docs/concept/intent
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

In dialogue systems, natural language understanding (NLU) turns a user utterance into a structured representation: the domain, the user's intent and the slots with their values, such as INTENT: SHOW-FLIGHTS, ORIGIN-CITY: Boston (Jurafsky & Martin, 2026). Intent classification and slot filling are usually learned together, for example with a pretrained encoder that tags each token and classifies the whole utterance (Jurafsky & Martin, 2026; Chen et al., 2019); platforms add a confidence threshold below which the input counts as not understood ([[dialogflow-cx|Dialogflow CX]]: Intents).

### How it works

NLU extracts three things from each utterance and hands them to the [[dialogue-state-tracking|dialogue state tracker]] of a [[conversational-ai|conversational AI]] system (Jurafsky & Martin, 2026):

```text
"Show me morning flights from Boston to San Francisco on Tuesday"
        │
        ▼  encoder + classifiers
DOMAIN: AIR-TRAVEL   INTENT: SHOW-FLIGHTS
ORIGIN-CITY: Boston  DEST-CITY: San Francisco  ORIGIN-DATE: Tuesday  ORIGIN-TIME: morning
        │
        ▼  normalisation (San Francisco → SFO, Tuesday → date)
```

#### 1. Domain classification and intent determination

Domain [[classification|classification]] decides what the user is talking about, for example air travel, an alarm clock or a calendar; intent determination decides which general task the user wants to accomplish, such as find a movie or remove a calendar appointment. Together, they select the frame to be filled (Jurafsky & Martin, 2026). Dialogflow CX defines an intent as the categorisation of an end user's intention for one conversation turn and learns it from training phrases, recommending at least 10 to 20 per intent depending on its complexity (Dialogflow CX: Intents).

#### 2. Slot filling as sequence labelling

Slot filling extracts the slots and values the user means. The simplest systems use handwritten rules, such as a regular expression for "wake me up | set an alarm"; most systems use supervised learning on sentences annotated with domain, intent and slots in BIO format: B marks the beginning of a slot, I its inside and O tokens outside any slot, as in B-DES I-DES for "San Francisco" (Jurafsky & Martin, 2026). In platforms, the parts of training phrases to be extracted must be annotated as parameters with entity types (Dialogflow CX: Intents).

#### 3. Joint models

A typical architecture passes the words through a pretrained language model encoder, followed by a feedforward layer and a softmax over BIO tags at each position; domain and intent are added as the label of a final end-of-sentence token, so one model performs all three tasks (Jurafsky & Martin, 2026). Chen et al. (2019) proposed joint intent classification and slot filling on [[bert|BERT]] and reported clear improvements over attention-based recurrent and slot-gated models in intent accuracy, slot F1 and sentence-level semantic frame accuracy; they also pointed to the limited amount of human-labelled data as a problem for generalisation, especially for rare words.

#### 4. Normalisation

Extracted strings are mapped to the canonical form of the ontology, for example "SF", "SFO" and "San Francisco" to the airport code SFO, often with dictionaries of synonyms; in industry, rules and machine learning are often combined for each component (Jurafsky & Martin, 2026).

#### 5. Confidence and no-match

Classifiers return a confidence between 0.0 and 1.0 for each intent; the best intent is returned only if it reaches the classification threshold, otherwise a no-match event is raised, which the dialogue handles as a fallback. A negative intent with example phrases catches inputs that should not match any intent, though too many of them can hurt normal matching (Dialogflow CX: Intents).

#### 6. Origin and variants

Machine learning was applied to slot filling from the 1990s on (Jurafsky & Martin, 2026); pretrained encoders made joint models standard (Chen et al., 2019). Related extraction tasks on documents are covered in [[entity-extraction|Entity Extraction]] and [[information-extraction|Information Extraction]].

### When to use it

- In task-oriented chat and voice assistants that must collect specific values, such as dates, amounts or contract numbers (Jurafsky & Martin, 2026).
- When each intent should lead to its own handling and low confidence to a fallback (Dialogflow CX: Intents).

### Strengths and limitations

**Strengths**
- A structured output that downstream logic can check and act on (Jurafsky & Martin, 2026).
- Joint models share one encoder for intent and slots (Jurafsky & Martin, 2026; Chen et al., 2019).
- The confidence threshold makes "not understood" an explicit, testable case (Dialogflow CX: Intents).

**Limitations**
- Needs annotated training data; scarce labels limit generalisation, especially for rare words (Chen et al., 2019).
- Intents need enough training phrases, and too many negative examples degrade normal matching (Dialogflow CX: Intents).
- In speech systems, recognition errors propagate into NLU (Jurafsky & Martin, 2026; [[automatic-speech-recognition|Automatic Speech Recognition]]).

### Comparison

| Approach | How it works | Suited for |
|----------|--------------|------------|
| Rules and regular expressions | Handwritten patterns per intent (Jurafsky & Martin, 2026) | Very few, fixed phrasings |
| Supervised joint model | Encoder with BIO tagging and intent label (Jurafsky & Martin, 2026; Chen et al., 2019) | Stable intents with training data |
| Platform intents | Training phrases, annotated parameters, threshold (Dialogflow CX: Intents) | Production dialogue systems |

### In practice

Intent accuracy and slot F1 are measured on held-out utterances; at dialogue level, the slot error rate counts inserted, deleted and substituted slots relative to the reference slots (Jurafsky & Martin, 2026; Chen et al., 2019). Entity types should be defined explicitly rather than relying on implicitly defined values (Dialogflow CX: Intents). For quality [[monitoring-and-alerting|monitoring]] in production, see [[conversation-analytics|Conversation Analytics]].

### Key takeaway

NLU maps each utterance to a domain, an intent and slot values, usually with one jointly trained encoder, and treats low confidence as an explicit "not understood".

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Frame-Based Dialogue Systems.* Speech and Language Processing, 3rd ed. draft, Appendix K. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/K.pdf)
- Chen, Q., Zhuo, Z. & Wang, W. (2019). *BERT for Joint Intent Classification and Slot Filling.* arXiv:1902.10909. [arxiv.org](https://arxiv.org/abs/1902.10909)
- Google Cloud. *Intents.* Dialogflow CX documentation. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/intent)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

In Dialogsystemen macht Natural Language Understanding (NLU) aus einer Nutzeräußerung eine strukturierte Darstellung: die Domäne, den Intent des Nutzers und die Slots mit ihren Werten, etwa INTENT: SHOW-FLIGHTS, ORIGIN-CITY: Boston (Jurafsky & Martin, 2026). Intent-Klassifikation und Slot Filling werden meist gemeinsam gelernt, etwa mit einem vortrainierten Encoder, der jedes Token taggt und die ganze Äußerung klassifiziert (Jurafsky & Martin, 2026; Chen et al., 2019); Plattformen ergänzen eine Konfidenzschwelle, unterhalb derer die Eingabe als nicht verstanden gilt ([[dialogflow-cx|Dialogflow CX]]: Intents).

### Funktionsweise

NLU gewinnt aus jeder Äußerung drei Dinge und gibt sie an den [[dialogue-state-tracking|Dialogue State Tracker]] eines [[conversational-ai|Conversational-AI]]-Systems weiter (Jurafsky & Martin, 2026):

```text
"Show me morning flights from Boston to San Francisco on Tuesday"
        │
        ▼  Encoder + Klassifikatoren
DOMAIN: AIR-TRAVEL   INTENT: SHOW-FLIGHTS
ORIGIN-CITY: Boston  DEST-CITY: San Francisco  ORIGIN-DATE: Tuesday  ORIGIN-TIME: morning
        │
        ▼  Normalisierung (San Francisco → SFO, Tuesday → Datum)
```

#### 1. Domänenklassifikation und Intent-Bestimmung

Die Domänenklassifikation entscheidet, worüber der Nutzer spricht, etwa Flugreisen, einen Wecker oder einen Kalender; die Intent-Bestimmung entscheidet, welche Aufgabe der Nutzer erledigen will, etwa einen Film finden oder einen Termin löschen. Zusammen wählen sie den Frame, der gefüllt wird (Jurafsky & Martin, 2026). Dialogflow CX definiert einen Intent als Einordnung der Absicht eines Endnutzers für einen Gesprächs-Turn und lernt ihn aus Trainingsphrasen; empfohlen werden je nach Komplexität mindestens 10 bis 20 pro Intent (Dialogflow CX: Intents).

#### 2. Slot Filling als Sequenz-Labeling

Slot Filling gewinnt die gemeinten Slots und Werte. Die einfachsten Systeme nutzen handgeschriebene Regeln, etwa einen regulären Ausdruck für „wake me up | set an alarm“; die meisten Systeme lernen überwacht aus Sätzen, die mit Domäne, Intent und Slots im BIO-Format annotiert sind: B markiert den Beginn eines Slots, I sein Inneres und O Token außerhalb jedes Slots, etwa B-DES I-DES für „San Francisco“ (Jurafsky & Martin, 2026). In Plattformen müssen die zu extrahierenden Teile von Trainingsphrasen als Parameter mit Entity-Typen annotiert werden (Dialogflow CX: Intents).

#### 3. Gemeinsame Modelle

Eine typische Architektur gibt die Wörter durch einen vortrainierten Sprachmodell-Encoder, gefolgt von einer Feedforward-Schicht und einem Softmax über BIO-Tags an jeder Position; Domäne und Intent kommen als Label eines abschließenden Satzende-Tokens hinzu, sodass ein Modell alle drei Aufgaben löst (Jurafsky & Martin, 2026). Chen et al. (2019) schlugen gemeinsame Intent-Klassifikation und Slot Filling auf [[bert|BERT]] vor und berichteten deutliche Verbesserungen gegenüber Attention-basierten rekurrenten und Slot-Gated-Modellen bei Intent-Accuracy, Slot-F1 und Semantic Frame Accuracy auf Satzebene; zugleich nannten sie die geringe Menge menschlich annotierter Daten als Problem für die Generalisierung, besonders bei seltenen Wörtern.

#### 4. Normalisierung

Gefundene Zeichenketten werden auf die kanonische Form der Ontologie abgebildet, etwa „SF“, „SFO“ und „San Francisco“ auf den Flughafencode SFO, oft mit Synonymwörterbüchern; in der Industrie werden für jede Komponente häufig Regeln und Machine Learning kombiniert (Jurafsky & Martin, 2026).

#### 5. Konfidenz und no-match

Klassifikatoren liefern für jeden Intent eine Konfidenz zwischen 0,0 und 1,0; der beste Intent wird nur zurückgegeben, wenn er die Klassifikationsschwelle erreicht, sonst wird ein no-match-Ereignis ausgelöst, das der Dialog als Fallback behandelt. Ein negativer Intent mit Beispielphrasen fängt Eingaben ab, die zu keinem Intent passen sollen, zu viele davon können das normale Matching aber verschlechtern (Dialogflow CX: Intents).

#### 6. Herkunft und Varianten

Machine Learning wurde ab den 1990er-Jahren für Slot Filling eingesetzt (Jurafsky & Martin, 2026); vortrainierte Encoder machten gemeinsame Modelle zum Standard (Chen et al., 2019). Verwandte Extraktionsaufgaben auf Dokumenten behandeln [[entity-extraction|Entity Extraction]] und [[information-extraction|Information Extraction]].

### Wann einsetzen

- In aufgabenorientierten Chat- und Sprachassistenten, die bestimmte Werte erfragen müssen, etwa Daten, Beträge oder Vertragsnummern (Jurafsky & Martin, 2026).
- Wenn jeder Intent eine eigene Behandlung auslösen soll und geringe Konfidenz einen Fallback (Dialogflow CX: Intents).

### Stärken und Grenzen

**Stärken**
- Eine strukturierte Ausgabe, die nachgelagerte Logik prüfen und verarbeiten kann (Jurafsky & Martin, 2026).
- Gemeinsame Modelle teilen einen Encoder für Intent und Slots (Jurafsky & Martin, 2026; Chen et al., 2019).
- Die Konfidenzschwelle macht „nicht verstanden“ zu einem ausdrücklichen, testbaren Fall (Dialogflow CX: Intents).

**Grenzen**
- Braucht annotierte Trainingsdaten; wenige Labels begrenzen die Generalisierung, besonders bei seltenen Wörtern (Chen et al., 2019).
- Intents brauchen genug Trainingsphrasen, und zu viele negative Beispiele verschlechtern das normale Matching (Dialogflow CX: Intents).
- In Sprachsystemen setzen sich Erkennungsfehler in die NLU fort (Jurafsky & Martin, 2026; [[automatic-speech-recognition|Automatische Spracherkennung]]).

### Vergleich

| Ansatz | Funktionsweise | Geeignet für |
|--------|----------------|--------------|
| Regeln und reguläre Ausdrücke | Handgeschriebene Muster pro Intent (Jurafsky & Martin, 2026) | Sehr wenige, feste Formulierungen |
| Überwachtes gemeinsames Modell | Encoder mit BIO-Tagging und Intent-Label (Jurafsky & Martin, 2026; Chen et al., 2019) | Stabile Intents mit Trainingsdaten |
| Plattform-Intents | Trainingsphrasen, annotierte Parameter, Schwelle (Dialogflow CX: Intents) | Dialogsysteme im Betrieb |

### In der Praxis

Intent-Accuracy und Slot-F1 werden auf zurückgehaltenen Äußerungen gemessen; auf Dialogebene zählt die Slot Error Rate eingefügte, gelöschte und ersetzte Slots relativ zu den Referenz-Slots (Jurafsky & Martin, 2026; Chen et al., 2019). Entity-Typen sollten ausdrücklich definiert werden, statt sich auf implizit definierte Werte zu verlassen (Dialogflow CX: Intents). Zur Qualitätsüberwachung im Betrieb siehe [[conversation-analytics|Conversation Analytics]].

### Merksatz

NLU ordnet jeder Äußerung eine Domäne, einen Intent und Slot-Werte zu, meist mit einem gemeinsam trainierten Encoder, und behandelt geringe Konfidenz als ausdrückliches „nicht verstanden“.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Frame-Based Dialogue Systems.* Speech and Language Processing, 3rd ed. draft, Appendix K. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/K.pdf)
- Chen, Q., Zhuo, Z. & Wang, W. (2019). *BERT for Joint Intent Classification and Slot Filling.* arXiv:1902.10909. [arxiv.org](https://arxiv.org/abs/1902.10909)
- Google Cloud. *Intents.* Dialogflow CX documentation. [docs.cloud.google.com](https://docs.cloud.google.com/dialogflow/cx/docs/concept/intent)
