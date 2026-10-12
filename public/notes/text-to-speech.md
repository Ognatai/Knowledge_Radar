---
title_en: Text-to-Speech (TTS)
title_de: Sprachsynthese (Text-to-Speech, TTS)
entity_type: Method
aliases:
- TTS
- Speech synthesis
- Zero-shot TTS
sources:
- https://web.stanford.edu/~jurafsky/slp3/17.pdf
- https://arxiv.org/abs/2301.02111
- https://www.w3.org/TR/speech-synthesis11/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Text-to-speech (TTS) generates a speech waveform for a given text in a desired voice (Jurafsky & Martin, 2026). Modern systems treat TTS as conditional language modelling: a neural audio codec turns speech into discrete tokens, and a language model generates the tokens of the new utterance from the text and a few seconds of the target voice, as in VALL-E (Jurafsky & Martin, 2026; Wang et al., 2023). Applications steer pronunciation, pauses and prosody with the W3C markup language SSML (W3C SSML 1.1); quality is judged by listeners as a mean opinion score (Jurafsky & Martin, 2026).

### How it works

```text
text ──► text tokens ─┐
                      ├─► language model ─► audio tokens ─► codec decoder ─► waveform
voice sample (3 s) ─► codec encoder ─► audio tokens ─┘
```

#### 1. From single-speaker to zero-shot TTS

Historically, a TTS system was trained on hundreds of hours from one speaker recorded in a lab, and it could speak only in that voice. Modern synthesisers are speaker-independent, trained on tens of thousands of hours from thousands of speakers, and create a voice unseen in training from about 3 seconds of that speaker; this is called zero-shot TTS (Jurafsky & Martin, 2026).

#### 2. Audio tokens from a neural codec

A neural audio codec (coder/decoder) compresses speech into discrete tokens: a convolutional encoder downsamples the waveform into embeddings, a quantiser turns them into tokens, and a convolutional decoder reconstructs a lossy waveform. Vector quantisation maps each vector to the nearest codeword of a codebook; residual vector quantisation then quantises the remaining difference again, giving several codes per frame (Jurafsky & Martin, 2026).

#### 3. Conditional generation with a language model

A language model whose vocabulary includes text and audio tokens is trained to take a transcript and a short speech sample and to generate the audio tokens of the transcript in that voice; at inference, the generated tokens are decoded into a waveform (Jurafsky & Martin, 2026). VALL-E applied this to 60,000 hours of English speech, generated speech for unseen speakers from a 3-second recording, outperformed the previous zero-shot system in naturalness and speaker similarity, and kept the emotion and acoustic environment of the prompt (Wang et al., 2023).

#### 4. Controlling the output with SSML

The Speech Synthesis Markup Language, a W3C Recommendation since 2010 in version 1.1, gives authors a standard way to control pronunciation, volume, pitch and rate across synthesis platforms. The root element speak sets the language; break, emphasis and prosody guide pauses and prosody; say-as states the type of a text construct, such as a date or number; phoneme gives a phonetic pronunciation; sub replaces text with an alias for pronunciation; voice requests a different voice; lexicon references external pronunciation lexicons; audio inserts recorded audio (W3C SSML 1.1).

#### 5. Evaluation

Listeners rate synthesised utterances on a scale from 1 to 5, the mean opinion score (MOS); two systems can be compared with paired tests on the same sentences, or with comparative MOS (CMOS), where listeners pick the better of two versions on a scale from -3 to 3. Automatic checks complement this: running the output through ASR and computing the word error rate tests intelligibility, and a speaker verification system scores how close the voice is to the enrolled sample (Jurafsky & Martin, 2026).

#### 6. Origin and variants

Older neural pipelines used an acoustic model and a vocoder with mel spectrograms as intermediate representation; codec language models such as VALL-E replace them with discrete audio codes (Wang et al., 2023).

### When to use it

- To speak the answers of [[voice-agents|voice agents]] and spoken [[conversational-ai|conversational AI]] systems.
- With SSML whenever numbers, dates, abbreviations or names must be pronounced in a specific way (W3C SSML 1.1).

### Strengths and limitations

**Strengths**
- New voices from a few seconds of speech, without collecting data from each speaker (Jurafsky & Martin, 2026; Wang et al., 2023).
- Natural-sounding output that keeps emotion and acoustic environment of the prompt (Wang et al., 2023).
- SSML works across synthesis platforms (W3C SSML 1.1).

**Limitations**
- A voice unseen in training can be imitated from a 3-second recording of the speaker (Wang et al., 2023).
- The codec is lossy: the decoder reconstructs an approximation of the waveform (Jurafsky & Martin, 2026).
- Quality is best judged by human listeners, which is costly; automatic metrics only add information (Jurafsky & Martin, 2026).

### Comparison

| Approach | How it works | Voice |
|----------|--------------|-------|
| Single-speaker TTS | Trained on hundreds of hours of one speaker (Jurafsky & Martin, 2026) | Only that voice |
| Acoustic model + vocoder | Mel spectrogram as intermediate step (Wang et al., 2023) | Voices seen in training |
| Codec language model (VALL-E) | Audio tokens generated by a language model (Wang et al., 2023) | Unseen voices from 3 seconds |

### In practice

Pronunciation of domain terms, numbers and abbreviations is fixed with say-as, sub, phoneme or a pronunciation lexicon rather than by changing the text (W3C SSML 1.1). Intelligibility is checked automatically by transcribing the output with [[automatic-speech-recognition|ASR]] and computing the word error rate; for comparisons between versions, CMOS tests with around 50 sentences in random order are a common setup (Jurafsky & Martin, 2026).

### Key takeaway

Modern TTS generates discrete audio tokens with a language model conditioned on text and a short voice sample, controls pronunciation with SSML and is judged by listeners as a mean opinion score.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Text-to-Speech.* Speech and Language Processing, 3rd ed. draft, Chapter 17. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/17.pdf)
- Wang, C. et al. (2023). *Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers.* arXiv:2301.02111. [arxiv.org](https://arxiv.org/abs/2301.02111)
- W3C (2010). *Speech Synthesis Markup Language (SSML) Version 1.1.* W3C Recommendation. [w3.org](https://www.w3.org/TR/speech-synthesis11/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Sprachsynthese (Text-to-Speech, TTS) erzeugt zu einem gegebenen Text eine Sprach-Wellenform in einer gewünschten Stimme (Jurafsky & Martin, 2026). Moderne Systeme behandeln TTS als bedingte Sprachmodellierung: Ein neuronaler Audio-Codec macht aus Sprache diskrete Token, und ein Sprachmodell erzeugt die Token der neuen Äußerung aus dem Text und wenigen Sekunden der Zielstimme, wie bei VALL-E (Jurafsky & Martin, 2026; Wang et al., 2023). Anwendungen steuern Aussprache, Pausen und Prosodie mit der W3C-Auszeichnungssprache SSML (W3C SSML 1.1); die Qualität beurteilen Hörende als Mean Opinion Score (Jurafsky & Martin, 2026).

### Funktionsweise

```text
Text ──► Text-Token ─┐
                     ├─► Sprachmodell ─► Audio-Token ─► Codec-Decoder ─► Wellenform
Stimmprobe (3 s) ─► Codec-Encoder ─► Audio-Token ─┘
```

#### 1. Von einer Stimme zu Zero-Shot-TTS

Früher wurde ein TTS-System mit Hunderten Stunden einer einzigen, im Labor aufgenommenen Person trainiert und konnte nur in dieser Stimme sprechen. Moderne Synthesizer sind sprecherunabhängig, mit Zehntausenden Stunden von Tausenden Sprechenden trainiert, und erzeugen eine im Training ungesehene Stimme aus etwa 3 Sekunden dieser Person; das heißt Zero-Shot-TTS (Jurafsky & Martin, 2026).

#### 2. Audio-Token aus einem neuronalen Codec

Ein neuronaler Audio-Codec (Coder/Decoder) komprimiert Sprache in diskrete Token: Ein Faltungs-Encoder verkleinert die Wellenform zu Embeddings, ein Quantisierer macht daraus Token, und ein Faltungs-Decoder rekonstruiert eine verlustbehaftete Wellenform. Vektorquantisierung ordnet jedem Vektor das nächste Codewort eines Codebuchs zu; Residual Vector Quantization quantisiert anschließend den verbleibenden Unterschied erneut und liefert so mehrere Codes pro Frame (Jurafsky & Martin, 2026).

#### 3. Bedingte Erzeugung mit einem Sprachmodell

Ein Sprachmodell, dessen Vokabular Text- und Audio-Token umfasst, lernt, aus einem Transkript und einer kurzen Sprachprobe die Audio-Token des Transkripts in dieser Stimme zu erzeugen; bei der Inferenz werden die erzeugten Token zu einer Wellenform dekodiert (Jurafsky & Martin, 2026). VALL-E wandte das auf 60.000 Stunden englischer Sprache an, erzeugte aus einer 3-Sekunden-Aufnahme Sprache für ungesehene Sprechende, übertraf das bisherige Zero-Shot-System bei Natürlichkeit und Sprecherähnlichkeit und behielt Emotion und akustische Umgebung der Vorgabe bei (Wang et al., 2023).

#### 4. Die Ausgabe mit SSML steuern

Die Speech Synthesis Markup Language, seit 2010 in Version 1.1 eine W3C-Empfehlung, gibt Autoren einen einheitlichen Weg, Aussprache, Lautstärke, Tonhöhe und Sprechtempo über Syntheseplattformen hinweg zu steuern. Das Wurzelelement speak legt die Sprache fest; break, emphasis und prosody steuern Pausen und Prosodie; say-as gibt den Typ eines Textbausteins an, etwa ein Datum oder eine Zahl; phoneme liefert eine phonetische Aussprache; sub ersetzt Text für die Aussprache durch einen Alias; voice fordert eine andere Stimme an; lexicon verweist auf externe Aussprachelexika; audio fügt aufgenommenes Audio ein (W3C SSML 1.1).

#### 5. Evaluation

Hörende bewerten synthetisierte Äußerungen auf einer Skala von 1 bis 5, dem Mean Opinion Score (MOS); zwei Systeme lassen sich mit gepaarten Tests auf denselben Sätzen vergleichen oder mit Comparative MOS (CMOS), bei dem Hörende auf einer Skala von −3 bis 3 die bessere von zwei Fassungen wählen. Automatische Prüfungen ergänzen das: Die Ausgabe durch ASR zu schicken und die Word Error Rate zu berechnen prüft die Verständlichkeit, und ein System zur Sprecherverifikation bewertet, wie nah die Stimme an der Probe liegt (Jurafsky & Martin, 2026).

#### 6. Herkunft und Varianten

Ältere neuronale Pipelines nutzten ein akustisches Modell und einen Vocoder mit Mel-Spektrogrammen als Zwischendarstellung; Codec-Sprachmodelle wie VALL-E ersetzen sie durch diskrete Audio-Codes (Wang et al., 2023).

### Wann einsetzen

- Um die Antworten von [[voice-agents|Voice Agents]] und gesprochenen [[conversational-ai|Conversational-AI]]-Systemen zu sprechen.
- Mit SSML immer dann, wenn Zahlen, Daten, Abkürzungen oder Namen auf eine bestimmte Weise ausgesprochen werden müssen (W3C SSML 1.1).

### Stärken und Grenzen

**Stärken**
- Neue Stimmen aus wenigen Sekunden Sprache, ohne Daten von jeder Person zu sammeln (Jurafsky & Martin, 2026; Wang et al., 2023).
- Natürlich klingende Ausgabe, die Emotion und akustische Umgebung der Vorgabe behält (Wang et al., 2023).
- SSML funktioniert über Syntheseplattformen hinweg (W3C SSML 1.1).

**Grenzen**
- Eine im Training ungesehene Stimme lässt sich aus einer 3-Sekunden-Aufnahme der Person nachahmen (Wang et al., 2023).
- Der Codec ist verlustbehaftet: Der Decoder rekonstruiert eine Annäherung an die Wellenform (Jurafsky & Martin, 2026).
- Die Qualität beurteilen Hörende am besten, was aufwendig ist; automatische Metriken liefern nur zusätzliche Hinweise (Jurafsky & Martin, 2026).

### Vergleich

| Ansatz | Funktionsweise | Stimme |
|--------|----------------|--------|
| TTS für eine Stimme | Trainiert mit Hunderten Stunden einer Person (Jurafsky & Martin, 2026) | Nur diese Stimme |
| Akustisches Modell + Vocoder | Mel-Spektrogramm als Zwischenschritt (Wang et al., 2023) | Im Training gesehene Stimmen |
| Codec-Sprachmodell (VALL-E) | Audio-Token von einem Sprachmodell erzeugt (Wang et al., 2023) | Ungesehene Stimmen aus 3 Sekunden |

### In der Praxis

Die Aussprache von Fachbegriffen, Zahlen und Abkürzungen wird mit say-as, sub, phoneme oder einem Aussprachelexikon festgelegt, statt den Text zu ändern (W3C SSML 1.1). Die Verständlichkeit wird automatisch geprüft, indem die Ausgabe mit [[automatic-speech-recognition|ASR]] transkribiert und die Word Error Rate berechnet wird; für den Vergleich von Fassungen sind CMOS-Tests mit rund 50 Sätzen in zufälliger Reihenfolge ein üblicher Aufbau (Jurafsky & Martin, 2026).

### Merksatz

Moderne TTS erzeugt diskrete Audio-Token mit einem Sprachmodell, das auf Text und eine kurze Stimmprobe bedingt ist, steuert die Aussprache mit SSML und wird von Hörenden als Mean Opinion Score bewertet.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Text-to-Speech.* Speech and Language Processing, 3rd ed. draft, Chapter 17. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/17.pdf)
- Wang, C. et al. (2023). *Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers.* arXiv:2301.02111. [arxiv.org](https://arxiv.org/abs/2301.02111)
- W3C (2010). *Speech Synthesis Markup Language (SSML) Version 1.1.* W3C Recommendation. [w3.org](https://www.w3.org/TR/speech-synthesis11/)
