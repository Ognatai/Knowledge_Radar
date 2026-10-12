---
title_en: Automatic Speech Recognition (ASR)
title_de: Automatische Spracherkennung (ASR)
entity_type: Method
aliases:
- ASR
- Speech recognition
- Speech-to-text
- STT
sources:
- https://web.stanford.edu/~jurafsky/slp3/16.pdf
- https://arxiv.org/abs/2212.04356
- https://arxiv.org/abs/2006.11477
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Automatic speech recognition (ASR) maps an audio waveform to the string of words that was spoken (Jurafsky & Martin, 2026). Modern systems turn the audio into log mel spectral frames, shorten the sequence with convolutional layers and decode it either with an attention-based encoder-decoder such as Whisper or with a self-supervised encoder such as wav2vec 2.0 and the CTC loss; quality is measured as word error rate (WER) (Jurafsky & Martin, 2026; Radford et al., 2023; Baevski et al., 2020).

### How it works

```text
waveform ─► log mel frames ─► convolutional layers ─► transformer encoder ─► decoder ─► text
           (25 ms window,      (shorter sequence)                          (attention-based
            10 ms stride)                                                    or CTC)
```

#### 1. Acoustic features

The waveform is cut into overlapping frames and turned into a log mel spectrum, a vector per frame with one channel per mel filter. Whisper, for example, extracts 128-channel log mel features with a 25 ms window and a 10 ms stride, giving 3,000 frames for its 30-second context window (Jurafsky & Martin, 2026).

#### 2. Convolutional front end

Speech frames are much shorter than letters or words, so convolutional layers with a stride greater than one shorten the sequence before transformer layers process it; Whisper, wav2vec 2.0 and HuBERT all start with stacked convolutional layers (Jurafsky & Martin, 2026).

#### 3. Encoder-decoder (attention-based)

An attention-based encoder-decoder, also called Listen Attend and Spell, encodes the frames and generates the transcript token by token while attending to the encoder output, usually with beam search (Jurafsky & Martin, 2026). Whisper uses this architecture; it was trained on 680,000 hours of multilingual and multitask audio from the internet, generalises to standard benchmarks without fine-tuning, approaches human accuracy and robustness, and was released with its inference code (Radford et al., 2023). It also performs speech translation, language identification and [[voice-activity-detection|voice activity detection]] (Jurafsky & Martin, 2026).

#### 4. Self-supervised encoders and CTC

wav2vec 2.0 learns speech representations from unlabelled raw audio by masking the input in a latent space and solving a contrastive task over quantised representations; fine-tuned with one hour of labelled data it beat the previous best result on the 100-hour LibriSpeech subset, and with ten minutes of labelled data it reached 4.8 % and 8.2 % WER on the clean and other test sets (Baevski et al., 2020). Such encoders are decoded with CTC (Connectionist Temporal Classification), which outputs one character per frame, including a special blank symbol, and then collapses repeated characters and removes blanks (Jurafsky & Martin, 2026).

#### 5. Word error rate

WER is the minimum number of word substitutions, insertions and deletions needed to turn the system's transcript into the reference, divided by the number of words in the reference and multiplied by 100; because insertions count, it can exceed 100 % (Jurafsky & Martin, 2026).

#### 6. Origin and variants

Early systems solved small vocabularies such as yes/no or digits; open-ended transcription of conversations remains harder (Jurafsky & Martin, 2026). Current families are attention-based encoder-decoders such as Whisper and its open reproduction OWSM, and self-supervised encoders with CTC such as wav2vec 2.0 and HuBERT (Jurafsky & Martin, 2026; Baevski et al., 2020).

### When to use it

- In voice interfaces and assistants, as the first step of a [[voice-agents|voice agent]] or a spoken [[conversational-ai|conversational AI]] system (Jurafsky & Martin, 2026).
- For transcription, such as captions for audio and video, dictation, or meeting minutes (Jurafsky & Martin, 2026).
- Self-supervised models when little labelled speech exists for a language or domain (Baevski et al., 2020).

### Strengths and limitations

**Strengths**
- Read English speech is transcribed very accurately: around 1.4 % WER on LibriSpeech clean (Jurafsky & Martin, 2026).
- Large weakly supervised models work across languages and tasks without fine-tuning (Radford et al., 2023).
- Self-supervised pre-training reduces the need for labelled data (Baevski et al., 2020).

**Limitations**
- Conversations are harder: about 5.8 % WER on Switchboard telephone calls, 11 % on family calls and meetings, and up to 25.5 % on dinner-party speech with distant microphones (Jurafsky & Martin, 2026).
- Error rates are higher for varieties such as African American English (16.2 %) and much higher for lower-resource languages, around 40 to 51 % for some (Jurafsky & Martin, 2026).
- Whisper tended to transcribe plausible but almost always wrong guesses for speakers' names, because training transcripts often contained them (Jurafsky & Martin, 2026).

### Comparison

| Approach | Decoding | Training data |
|----------|----------|---------------|
| Attention-based encoder-decoder (Whisper) | Autoregressive, beam search (Jurafsky & Martin, 2026) | 680,000 hours weakly supervised (Radford et al., 2023) |
| Self-supervised encoder + CTC (wav2vec 2.0) | Frame-wise characters, collapsed (Jurafsky & Martin, 2026) | Unlabelled audio plus little labelled data (Baevski et al., 2020) |

### In practice

WER is computed against a reference transcript of the target domain, because error rates differ widely between read speech, telephone calls and meetings (Jurafsky & Martin, 2026). In spoken dialogue, misrecognitions propagate into [[natural-language-understanding|NLU]], and users react with corrections that are themselves harder to recognise ([[dialogue-state-tracking|Dialogue State Tracking]]).

### Key takeaway

ASR turns log mel frames into text with an attention-based encoder-decoder or a self-supervised encoder with CTC; it is very accurate on read speech but much less so on conversations, accents and low-resource languages, measured by word error rate.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Automatic Speech Recognition.* Speech and Language Processing, 3rd ed. draft, Chapter 16. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/16.pdf)
- Radford, A. et al. (2023). *Robust Speech Recognition via Large-Scale Weak Supervision.* ICML 2023. [arxiv.org](https://arxiv.org/abs/2212.04356)
- Baevski, A., Zhou, H., Mohamed, A. & Auli, M. (2020). *wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations.* NeurIPS 2020. [arxiv.org](https://arxiv.org/abs/2006.11477)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Automatische Spracherkennung (Automatic Speech Recognition, ASR) bildet eine Audio-Wellenform auf die gesprochene Wortfolge ab (Jurafsky & Martin, 2026). Moderne Systeme machen aus dem Audio Log-Mel-Spektralframes, verkürzen die Folge mit Faltungsschichten und dekodieren sie entweder mit einem Attention-basierten Encoder-Decoder wie Whisper oder mit einem selbstüberwacht trainierten Encoder wie wav2vec 2.0 und der CTC-Loss; gemessen wird die Qualität als Word Error Rate (WER) (Jurafsky & Martin, 2026; Radford et al., 2023; Baevski et al., 2020).

### Funktionsweise

```text
Wellenform ─► Log-Mel-Frames ─► Faltungsschichten ─► Transformer-Encoder ─► Decoder ─► Text
             (25-ms-Fenster,     (kürzere Folge)                             (Attention-basiert
              10-ms-Schritt)                                                  oder CTC)
```

#### 1. Akustische Merkmale

Die Wellenform wird in überlappende Frames zerlegt und in ein Log-Mel-Spektrum überführt, einen Vektor pro Frame mit einem Kanal je Mel-Filter. Whisper etwa gewinnt 128-kanalige Log-Mel-Merkmale mit 25-ms-Fenster und 10-ms-Schritt, was 3.000 Frames für sein 30-Sekunden-Kontextfenster ergibt (Jurafsky & Martin, 2026).

#### 2. Faltungsschichten am Anfang

Sprachframes sind viel kürzer als Buchstaben oder Wörter, daher verkürzen Faltungsschichten mit einer Schrittweite größer eins die Folge, bevor Transformer-Schichten sie verarbeiten; Whisper, wav2vec 2.0 und HuBERT beginnen alle mit gestapelten Faltungsschichten (Jurafsky & Martin, 2026).

#### 3. Encoder-Decoder (Attention-basiert)

Ein Attention-basierter Encoder-Decoder, auch Listen Attend and Spell genannt, kodiert die Frames und erzeugt das Transkript Token für Token, wobei er auf die Encoder-Ausgabe achtet, meist mit Beam Search (Jurafsky & Martin, 2026). Whisper nutzt diese Architektur; es wurde mit 680.000 Stunden mehrsprachigem Multitask-Audio aus dem Internet trainiert, generalisiert ohne Fine-Tuning auf Standard-Benchmarks, nähert sich menschlicher Genauigkeit und Robustheit und wurde mitsamt Inferenzcode veröffentlicht (Radford et al., 2023). Es beherrscht außerdem Sprachübersetzung, Spracherkennung der Sprache und [[voice-activity-detection|Voice Activity Detection]] (Jurafsky & Martin, 2026).

#### 4. Selbstüberwachte Encoder und CTC

wav2vec 2.0 lernt Sprachrepräsentationen aus unannotiertem Rohaudio, indem es die Eingabe in einem latenten Raum maskiert und eine kontrastive Aufgabe über quantisierten Repräsentationen löst; mit einer Stunde annotierter Daten feinjustiert übertraf es das bis dahin beste Ergebnis auf der 100-Stunden-Teilmenge von LibriSpeech, mit zehn Minuten erreichte es 4,8 % und 8,2 % WER auf den Testmengen clean und other (Baevski et al., 2020). Solche Encoder werden mit CTC (Connectionist Temporal Classification) dekodiert, das pro Frame ein Zeichen ausgibt, einschließlich eines besonderen Blank-Symbols, und dann wiederholte Zeichen zusammenfasst und Blanks entfernt (Jurafsky & Martin, 2026).

#### 5. Word Error Rate

Die WER ist die minimale Zahl an Wortersetzungen, -einfügungen und -löschungen, die das Transkript des Systems in die Referenz überführt, geteilt durch die Zahl der Wörter der Referenz und mal 100; weil Einfügungen mitzählen, kann sie über 100 % liegen (Jurafsky & Martin, 2026).

#### 6. Herkunft und Varianten

Frühe Systeme lösten kleine Vokabulare wie Ja/Nein oder Ziffern; die offene Transkription von Gesprächen bleibt schwieriger (Jurafsky & Martin, 2026). Heutige Familien sind Attention-basierte Encoder-Decoder wie Whisper und seine offene Nachbildung OWSM sowie selbstüberwachte Encoder mit CTC wie wav2vec 2.0 und HuBERT (Jurafsky & Martin, 2026; Baevski et al., 2020).

### Wann einsetzen

- In Sprachschnittstellen und Assistenten, als erster Schritt eines [[voice-agents|Voice Agents]] oder eines gesprochenen [[conversational-ai|Conversational-AI]]-Systems (Jurafsky & Martin, 2026).
- Für Transkription, etwa Untertitel für Audio und Video, Diktat oder Besprechungsprotokolle (Jurafsky & Martin, 2026).
- Selbstüberwachte Modelle, wenn für eine Sprache oder Domäne wenig annotierte Sprache vorliegt (Baevski et al., 2020).

### Stärken und Grenzen

**Stärken**
- Vorgelesenes Englisch wird sehr genau transkribiert: rund 1,4 % WER auf LibriSpeech clean (Jurafsky & Martin, 2026).
- Große, schwach überwachte Modelle funktionieren über Sprachen und Aufgaben hinweg ohne Fine-Tuning (Radford et al., 2023).
- Selbstüberwachtes Vortraining senkt den Bedarf an annotierten Daten (Baevski et al., 2020).

**Grenzen**
- Gespräche sind schwieriger: etwa 5,8 % WER bei Switchboard-Telefonaten, 11 % bei Familientelefonaten und Besprechungen und bis zu 25,5 % bei Abendessen-Gesprächen mit entfernten Mikrofonen (Jurafsky & Martin, 2026).
- Bei Varietäten wie African American English liegen die Fehlerraten höher (16,2 %), bei ressourcenarmen Sprachen deutlich höher, für einige bei rund 40 bis 51 % (Jurafsky & Martin, 2026).
- Whisper neigte dazu, plausible, aber fast immer falsche Namen von Sprechenden zu transkribieren, weil die Trainingstranskripte sie oft enthielten (Jurafsky & Martin, 2026).

### Vergleich

| Ansatz | Dekodierung | Trainingsdaten |
|--------|-------------|----------------|
| Attention-basierter Encoder-Decoder (Whisper) | Autoregressiv, Beam Search (Jurafsky & Martin, 2026) | 680.000 Stunden schwach überwacht (Radford et al., 2023) |
| Selbstüberwachter Encoder + CTC (wav2vec 2.0) | Zeichen pro Frame, zusammengefasst (Jurafsky & Martin, 2026) | Unannotiertes Audio plus wenig annotierte Daten (Baevski et al., 2020) |

### In der Praxis

Die WER wird gegen ein Referenztranskript aus der Zieldomäne berechnet, weil sich die Fehlerraten zwischen vorgelesener Sprache, Telefonaten und Besprechungen stark unterscheiden (Jurafsky & Martin, 2026). Im gesprochenen Dialog setzen sich Erkennungsfehler in die [[natural-language-understanding|NLU]] fort, und Nutzer reagieren mit Korrekturen, die selbst schwerer zu erkennen sind ([[dialogue-state-tracking|Dialogue State Tracking]]).

### Merksatz

ASR macht mit einem Attention-basierten Encoder-Decoder oder einem selbstüberwachten Encoder mit CTC aus Log-Mel-Frames Text; bei vorgelesener Sprache ist sie sehr genau, bei Gesprächen, Varietäten und ressourcenarmen Sprachen deutlich weniger, gemessen als Word Error Rate.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Automatic Speech Recognition.* Speech and Language Processing, 3rd ed. draft, Chapter 16. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/16.pdf)
- Radford, A. et al. (2023). *Robust Speech Recognition via Large-Scale Weak Supervision.* ICML 2023. [arxiv.org](https://arxiv.org/abs/2212.04356)
- Baevski, A., Zhou, H., Mohamed, A. & Auli, M. (2020). *wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations.* NeurIPS 2020. [arxiv.org](https://arxiv.org/abs/2006.11477)
