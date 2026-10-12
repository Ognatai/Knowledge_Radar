---
title_en: Voice Activity Detection (VAD)
title_de: Voice Activity Detection (VAD)
entity_type: Method
aliases:
- VAD
- Speech activity detection
sources:
- https://web.stanford.edu/~jurafsky/slp3/17.pdf
- https://web.stanford.edu/~jurafsky/slp3/16.pdf
- https://github.com/snakers4/silero-vad
- https://docs.livekit.io/agents/build/turns/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Voice activity detection (VAD) decides, frame by frame, whether an audio signal contains speech, and thus finds the segments of continuous speech and the pauses between them (Jurafsky & Martin, 2026, ch. 17). It is the first filter in many speech pipelines: speaker diarisation uses it to find speech segments, [[automatic-speech-recognition|ASR]] models such as Whisper also perform it, and [[voice-agents|voice agents]] use it to detect when the user starts or stops speaking (Jurafsky & Martin, 2026, ch. 16 and 17; LiveKit docs: Turns).

### How it works

```text
audio stream ─► chunks of ~30 ms ─► VAD model ─► speech probability per chunk
                                                   │
                         threshold + minimum durations ─► speech segments / silence
```

#### 1. Chunked classification

The audio is processed in short chunks, and a classifier outputs for each chunk whether it contains speech. Silero VAD, an open pre-trained detector, processes a chunk of 30 ms or more in under a millisecond on one CPU thread, supports sampling rates of 8 kHz and 16 kHz, is about 2 MB in size and was trained on corpora covering over 6,000 languages (Silero VAD).

#### 2. From frames to segments

Chunk decisions are turned into speech segments with start and end times; Silero VAD, for example, returns speech timestamps for a recording (Silero VAD).

#### 3. Uses in speech pipelines

- **Speaker diarisation** ("who spoke when"): systems often use VAD to find segments of continuous speech, extract speaker embeddings and cluster them (Jurafsky & Martin, 2026, ch. 17).
- **ASR:** Whisper is a multitask model that also performs voice activity detection alongside transcription and translation (Jurafsky & Martin, 2026, ch. 16).
- **Turn detection in voice agents:** most turn detection techniques rely on VAD to detect periods of silence in user input, and apply heuristics to find the end of a sentence or thought; a semantic turn detector can predict the end of a turn from the meaning and the acoustics of speech on top of VAD (LiveKit docs: Turns).
- **Interruptions:** an agent pauses its own speech when VAD detects user speech; a VAD detection without real speech counts as a false interruption, after which the agent resumes (LiveKit docs: Turns).

#### 4. Origin and variants

Related on-device detectors include wake word detection, which spots a short phrase to activate an assistant with a small, fast model on the device (Jurafsky & Martin, 2026, ch. 17). Neural VADs such as Silero target voice interfaces, telephony and call-centre automation, voice bots and data preparation (Silero VAD).

### When to use it

- Before ASR, to send only speech segments to the recogniser and to cut long recordings (Silero VAD; Jurafsky & Martin, 2026, ch. 16).
- In [[voice-agents|voice agents]] and telephony bots, to detect turn ends and interruptions (LiveKit docs: Turns).
- For diarisation and for cleaning speech datasets (Jurafsky & Martin, 2026, ch. 17; Silero VAD).

### Strengths and limitations

**Strengths**
- Very cheap: fractions of a millisecond per chunk on a CPU (Silero VAD).
- Trained on corpora covering over 6,000 languages (Silero VAD).
- Gives voice agents a fast signal for interruptions (LiveKit docs: Turns).

**Limitations**
- Silence alone is a weak signal for the end of a turn; frameworks add endpointing delays, heuristics and semantic turn detectors on top of VAD (LiveKit docs: Turns).
- VAD can detect speech where there is none, which then counts as a false interruption (LiveKit docs: Turns).
- Supported sampling rates are limited, for example 8 and 16 kHz for Silero (Silero VAD).

### Comparison

| Approach | Signal | Use |
|----------|--------|-----|
| VAD | Speech vs. no speech per chunk (Silero VAD) | Segmentation, interruptions |
| VAD + endpointing delay | Silence longer than a minimum and maximum delay (LiveKit docs: Turns) | Simple turn detection |
| Semantic turn detector | Meaning and acoustics on top of VAD (LiveKit docs: Turns) | Natural turn-taking |
| Wake word detection | One fixed phrase (Jurafsky & Martin, 2026, ch. 17) | Activating an assistant |

### In practice

Turn detection in voice agents combines VAD with a configurable minimum and maximum endpointing delay; dynamic endpointing adapts the delay to the pause statistics of the session (LiveKit docs: Turns). Interim ASR transcripts do not trigger an interruption when a VAD is present, while final transcripts do (LiveKit docs: Turns).

### Key takeaway

VAD marks which parts of an audio stream contain speech; it is cheap and essential for ASR, diarisation and voice agents, but silence alone does not tell when a speaker has finished.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Text-to-Speech* (section 17.5, Other speech tasks). Speech and Language Processing, 3rd ed. draft, Chapter 17. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/17.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Automatic Speech Recognition.* Speech and Language Processing, 3rd ed. draft, Chapter 16. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/16.pdf)
- Silero Team. *Silero VAD.* GitHub repository. [github.com](https://github.com/snakers4/silero-vad)
- LiveKit. *Turns overview.* LiveKit Agents documentation. [docs.livekit.io](https://docs.livekit.io/agents/build/turns/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Voice Activity Detection (VAD) entscheidet Frame für Frame, ob ein Audiosignal Sprache enthält, und findet so die Abschnitte zusammenhängender Sprache und die Pausen dazwischen (Jurafsky & Martin, 2026, Kap. 17). In vielen Sprach-Pipelines ist sie der erste Filter: Speaker Diarization nutzt sie, um Sprachabschnitte zu finden, [[automatic-speech-recognition|ASR]]-Modelle wie Whisper beherrschen sie ebenfalls, und [[voice-agents|Voice Agents]] erkennen damit, wann der Nutzer zu sprechen beginnt oder aufhört (Jurafsky & Martin, 2026, Kap. 16 und 17; LiveKit docs: Turns).

### Funktionsweise

```text
Audiostrom ─► Abschnitte von ~30 ms ─► VAD-Modell ─► Sprachwahrscheinlichkeit pro Abschnitt
                                                       │
                             Schwelle + Mindestdauern ─► Sprachabschnitte / Stille
```

#### 1. Klassifikation in Abschnitten

Das Audio wird in kurzen Abschnitten verarbeitet, und ein Klassifikator gibt für jeden Abschnitt aus, ob er Sprache enthält. Silero VAD, ein offener vortrainierter Detektor, verarbeitet einen Abschnitt von 30 ms oder mehr in unter einer Millisekunde auf einem CPU-Thread, unterstützt Abtastraten von 8 kHz und 16 kHz, ist etwa 2 MB groß und wurde auf Korpora mit über 6.000 Sprachen trainiert (Silero VAD).

#### 2. Von Frames zu Abschnitten

Die Entscheidungen pro Abschnitt werden zu Sprachsegmenten mit Start- und Endzeit; Silero VAD etwa liefert für eine Aufnahme die Zeitstempel der Sprache (Silero VAD).

#### 3. Einsatz in Sprach-Pipelines

- **Speaker Diarization** („wer sprach wann“): Systeme nutzen oft VAD, um Abschnitte zusammenhängender Sprache zu finden, Sprecher-Embeddings zu gewinnen und sie zu clustern (Jurafsky & Martin, 2026, Kap. 17).
- **ASR:** Whisper ist ein Multitask-Modell, das neben Transkription und Übersetzung auch Voice Activity Detection beherrscht (Jurafsky & Martin, 2026, Kap. 16).
- **Turn Detection in Voice Agents:** Die meisten Verfahren der Turn Detection stützen sich auf VAD, um Stille in der Nutzereingabe zu erkennen, und wenden Heuristiken an, um das Ende eines Satzes oder Gedankens zu finden; ein semantischer Turn Detector kann das Ende eines Turns zusätzlich zur VAD aus Bedeutung und Akustik der Sprache vorhersagen (LiveKit docs: Turns).
- **Unterbrechungen:** Ein Agent pausiert seine eigene Sprachausgabe, wenn die VAD Sprache des Nutzers erkennt; eine VAD-Erkennung ohne echte Sprache gilt als falsche Unterbrechung, nach der der Agent weiterspricht (LiveKit docs: Turns).

#### 4. Herkunft und Varianten

Verwandt sind Detektoren auf dem Gerät wie die Wake-Word-Erkennung, die mit einem kleinen, schnellen Modell eine kurze Phrase zum Aktivieren eines Assistenten erkennt (Jurafsky & Martin, 2026, Kap. 17). Neuronale VADs wie Silero zielen auf Sprachschnittstellen, Telefonie und Callcenter-Automatisierung, Voicebots und Datenaufbereitung (Silero VAD).

### Wann einsetzen

- Vor der ASR, um nur Sprachabschnitte an die Erkennung zu geben und lange Aufnahmen zu zerlegen (Silero VAD; Jurafsky & Martin, 2026, Kap. 16).
- In [[voice-agents|Voice Agents]] und Telefonbots, um Turn-Enden und Unterbrechungen zu erkennen (LiveKit docs: Turns).
- Für Diarization und zum Bereinigen von Sprachdatensätzen (Jurafsky & Martin, 2026, Kap. 17; Silero VAD).

### Stärken und Grenzen

**Stärken**
- Sehr günstig: Bruchteile einer Millisekunde pro Abschnitt auf einer CPU (Silero VAD).
- Trainiert auf Korpora mit über 6.000 Sprachen (Silero VAD).
- Liefert Voice Agents ein schnelles Signal für Unterbrechungen (LiveKit docs: Turns).

**Grenzen**
- Stille allein ist ein schwaches Signal für das Ende eines Turns; Frameworks ergänzen die VAD um Endpointing-Verzögerungen, Heuristiken und semantische Turn Detectors (LiveKit docs: Turns).
- VAD kann Sprache erkennen, wo keine ist, was dann als falsche Unterbrechung gilt (LiveKit docs: Turns).
- Die unterstützten Abtastraten sind begrenzt, bei Silero etwa 8 und 16 kHz (Silero VAD).

### Vergleich

| Ansatz | Signal | Einsatz |
|--------|--------|---------|
| VAD | Sprache oder keine Sprache pro Abschnitt (Silero VAD) | Segmentierung, Unterbrechungen |
| VAD + Endpointing-Verzögerung | Stille länger als eine Mindest- und Höchstverzögerung (LiveKit docs: Turns) | Einfache Turn Detection |
| Semantischer Turn Detector | Bedeutung und Akustik zusätzlich zur VAD (LiveKit docs: Turns) | Natürlicher Sprecherwechsel |
| Wake-Word-Erkennung | Eine feste Phrase (Jurafsky & Martin, 2026, Kap. 17) | Aktivieren eines Assistenten |

### In der Praxis

Turn Detection in Voice Agents kombiniert VAD mit einer einstellbaren minimalen und maximalen Endpointing-Verzögerung; dynamisches Endpointing passt die Verzögerung an die Pausenstatistik der Sitzung an (LiveKit docs: Turns). Vorläufige ASR-Transkripte lösen keine Unterbrechung aus, wenn eine VAD vorhanden ist, endgültige Transkripte schon (LiveKit docs: Turns).

### Merksatz

VAD markiert, welche Teile eines Audiostroms Sprache enthalten; sie ist günstig und unverzichtbar für ASR, Diarization und Voice Agents, aber Stille allein sagt nicht, wann jemand fertig gesprochen hat.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Text-to-Speech* (Abschnitt 17.5, Other speech tasks). Speech and Language Processing, 3rd ed. draft, Chapter 17. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/17.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Automatic Speech Recognition.* Speech and Language Processing, 3rd ed. draft, Chapter 16. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/16.pdf)
- Silero Team. *Silero VAD.* GitHub repository. [github.com](https://github.com/snakers4/silero-vad)
- LiveKit. *Turns overview.* LiveKit Agents documentation. [docs.livekit.io](https://docs.livekit.io/agents/build/turns/)
