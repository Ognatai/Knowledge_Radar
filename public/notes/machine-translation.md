---
title_en: Machine Translation
title_de: Maschinelle Übersetzung
entity_type: Method
aliases:
- MT
- Neural machine translation
- Backtranslation
- chrF
sources:
- https://web.stanford.edu/~jurafsky/slp3/13.pdf
- https://edoc.ub.uni-muenchen.de/36297/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Machine translation (MT) uses computers to translate from one language to another, mostly for information access, as drafts for human post-editing and for in-the-moment communication (Jurafsky & Martin, 2026). Languages differ in word order, in how they divide meaning into words and in what they may omit, so MT must reorder and disambiguate. The standard architecture is the encoder-decoder Transformer, trained on parallel corpora of aligned sentences and decoded with beam search. Translations are judged for adequacy and fluency, by human raters or by automatic metrics such as chrF, [[bleu|BLEU]], COMET or [[bertscore|BERTScore]] (Jurafsky & Martin, 2026).

### How it works

```text
parallel corpus (bitext) ─► sentence alignment + cleanup ─► shared subword vocabulary (BPE, wordpiece, unigram)
source tokens ─► encoder (bidirectional self-attention) ─► H_enc
                 decoder (causal self-attention + cross-attention to H_enc) ─► next target token
decoding: beam search (k = 5–10) or minimum Bayes risk
evaluation: human adequacy/fluency · chrF · BLEU · COMET/BLEURT · BERTScore
```

#### 1. Language divergences

About 7,000 languages differ systematically, which linguistic typology studies. English, German and Mandarin are SVO languages, Hindi and Japanese SOV, Irish and Arabic VSO; VO languages tend to have prepositions, OV languages postpositions. Lexical divergences require disambiguation: English *wall* is German *Wand* or *Mauer*, *bass* is Spanish *lubina* or *bajo*, which links MT to word sense disambiguation. Some languages have lexical gaps, mark direction of motion on the verb (Spanish *salió flotando*) or on a satellite (English *floated out*), or drop pronouns (pro-drop languages such as Chinese and Japanese), so translation into English must recover the omitted referent (Jurafsky & Martin, 2026).

#### 2. Encoder-decoder Transformer

The model maximises P(y_1, …, y_m | x_1, …, x_n). The encoder maps the source tokens to representations H_enc; the decoder is a conditional language model whose blocks add a cross-attention layer, in which queries come from the decoder and keys and values from the encoder output. Training uses cross-entropy loss with teacher forcing. Source and target share a subword vocabulary, which makes copying names easy and handles languages without spaces; the unigram (SentencePiece) algorithm tends to produce more meaningful tokens than BPE (Jurafsky & Martin, 2026).

#### 3. Training data

Parallel corpora include Europarl (400,000 to 2 million sentences in each of 21 languages), the United Nations Parallel Corpus, OpenSubtitles and ParaCrawl (223 million sentence pairs). New corpora need sentence alignment, scored with multilingual sentence [[embeddings|embeddings]] and solved with dynamic programming, and cleanup of noisy pairs (Jurafsky & Martin, 2026).

#### 4. Decoding

Greedy decoding can miss the most probable sequence. Beam search keeps the k best hypotheses at each step, scores them by summed log probabilities and normalises for length; MT uses k between 5 and 10. Minimum Bayes risk decoding samples candidates and picks the one most similar to the others under a metric such as chrF, which can work even better than beam search (Jurafsky & Martin, 2026).

#### 5. Low-resource translation

Backtranslation trains a reverse system on a small bitext, translates monolingual target-language text back and adds the synthetic pairs; it gets about 2/3 of the gain of the same amount of natural bitext. Multilingual models mark source and target language with special tokens and let low-resource languages profit from related ones, such as Galician from Spanish. An audit found that many multilingual corpora had less than 50% acceptable sentences, and participatory approaches involve native speakers as curators and evaluators (Jurafsky & Martin, 2026).

#### 6. Evaluation

Human raters score adequacy (fidelity to the source meaning) and fluency, rank candidates or post-edit outputs. chrF averages character n-gram [[classification-metrics|precision]] and recall and weights recall twice (β = 2); it is simple, robust and correlates well with human judgments. BLEU is a word-based n-gram precision with a brevity penalty, sensitive to tokenisation; SacreBLEU standardises it. Overlap metrics are local and best for comparing changes to one system, with paired bootstrap tests for significance. COMET and BLEURT are trained on human ratings, BERTScore matches tokens by embedding similarity (Jurafsky & Martin, 2026).

#### 7. Bias

When translating from gender-neutral Hungarian *ő* into English, MT systems chose *she* for a nurse and *he* for a CEO, amplifying stereotypes beyond labour statistics; WinoMT shows worse performance for non-stereotypical gender roles. Because MT is used in medical and legal settings, systems need confidence values so they can abstain (Jurafsky & Martin, 2026). LLMs show related problems: [[chatgpt|ChatGPT]] translated the gender-neutral English *they* into German as third person plural, producing an incorrect sentence with a possibly different meaning (Urchs, 2025).

#### Origin and variants

MT was proposed by Weaver (1949); the 1966 ALPAC report cut US funding. Early architectures were direct, transfer and interlingua approaches (Vauquois triangle). Statistical MT began around 1990 with the IBM Models and the Hansard corpus, followed by phrase-based translation, minimum error rate training on BLEU and toolkits such as Moses. The neural encoder-decoder was applied to MT by Bahdanau et al. (2015), and the Transformer was proposed by Vaswani et al. (2017) (Jurafsky & Martin, 2026).

### When to use it

- Information access across languages, which helps reduce the digital divide (Jurafsky & Martin, 2026).
- Computer-aided translation and localisation, with human post-editing (Jurafsky & Martin, 2026).
- Incremental speech translation and translation of text in images (Jurafsky & Martin, 2026).

### Strengths and limitations

**Strengths**
- Encoder-decoder networks handle complex reorderings and divergences between languages (Jurafsky & Martin, 2026).
- Google Translate alone translates hundreds of billions of words a day between over 100 languages (Jurafsky & Martin, 2026).

**Limitations**
- Most languages lack large parallel corpora, and many systems centre on English (Jurafsky & Martin, 2026).
- Automatic metrics cannot evaluate discourse coherence and compare very different systems poorly (Jurafsky & Martin, 2026).
- Gender bias in translating gender-neutral source languages (Jurafsky & Martin, 2026; Urchs, 2025).

### Comparison

| Metric | Basis | Note |
|--------|-------|------|
| Human adequacy/fluency | Raters | Most accurate, expensive |
| chrF | Character n-gram F-score | Simple, robust, good correlation |
| BLEU | Word n-gram precision + brevity penalty | Tokenisation-sensitive |
| COMET / BLEURT | Trained on human ratings | High correlation with humans |
| BERTScore | Token embedding similarity | No human ratings needed |

Source: Jurafsky & Martin (2026).

### In practice

MT relies on [[attention-and-transformers|Attention and Transformers]] and subword [[tokenisation|Tokenisation]]; sense ambiguities connect it to [[word-sense-disambiguation|Word Sense Disambiguation]], and n-gram overlap metrics are related to [[text-similarity-metrics|Text Similarity Metrics]] (Jurafsky & Martin, 2026). Gender bias in translation is one case of [[bias-in-nlp|Bias in NLP]] (Jurafsky & Martin, 2026; Urchs, 2025).

### Key takeaway

Machine translation maps sentences between languages with encoder-decoder Transformers trained on parallel corpora, decoded with beam search and evaluated by humans or metrics such as chrF; low-resource languages and gender bias remain open problems.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Machine Translation.* Speech and Language Processing, 3rd ed. draft, Chapter 13. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/13.pdf)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Maschinelle Übersetzung (MT) übersetzt mit Computern von einer Sprache in eine andere, vor allem für den Informationszugang, als Entwurf für menschliches Post-Editing und für Kommunikation im Moment (Jurafsky & Martin, 2026). Sprachen unterscheiden sich in der Wortstellung, darin, wie sie Bedeutung auf Wörter verteilen, und darin, was sie weglassen dürfen, daher muss MT umordnen und disambiguieren. Die Standardarchitektur ist der Encoder-Decoder-Transformer, trainiert auf Parallelkorpora alignierter Sätze und dekodiert mit Beam Search. Übersetzungen werden nach Adäquatheit und Flüssigkeit bewertet, von menschlichen Bewertenden oder mit automatischen Metriken wie chrF, [[bleu|BLEU]], COMET oder [[bertscore|BERTScore]] (Jurafsky & Martin, 2026).

### Funktionsweise

```text
Parallelkorpus (Bitext) ─► Satz-Alignment + Bereinigung ─► gemeinsames Subword-Vokabular (BPE, Wordpiece, Unigram)
Quell-Token ─► Encoder (bidirektionale Self-Attention) ─► H_enc
               Decoder (kausale Self-Attention + Cross-Attention auf H_enc) ─► nächstes Ziel-Token
Dekodierung: Beam Search (k = 5–10) oder Minimum Bayes Risk
Evaluation: menschliche Adäquatheit/Flüssigkeit · chrF · BLEU · COMET/BLEURT · BERTScore
```

#### 1. Sprachliche Divergenzen

Etwa 7.000 Sprachen unterscheiden sich systematisch, was die Sprachtypologie untersucht. Englisch, Deutsch und Mandarin sind SVO-Sprachen, Hindi und Japanisch SOV, Irisch und Arabisch VSO; VO-Sprachen haben meist Präpositionen, OV-Sprachen Postpositionen. Lexikalische Divergenzen verlangen Disambiguierung: Englisch *wall* ist deutsch *Wand* oder *Mauer*, *bass* ist spanisch *lubina* oder *bajo*, was MT mit der Wortsinn-Disambiguierung verbindet. Manche Sprachen haben lexikalische Lücken, markieren die Bewegungsrichtung am Verb (spanisch *salió flotando*) oder an einem Satelliten (englisch *floated out*) oder lassen Pronomen weg (Pro-Drop-Sprachen wie Chinesisch und Japanisch), sodass eine Übersetzung ins Englische den ausgelassenen Referenten wiederherstellen muss (Jurafsky & Martin, 2026).

#### 2. Encoder-Decoder-Transformer

Das Modell maximiert P(y_1, …, y_m | x_1, …, x_n). Der Encoder bildet die Quell-Token auf Repräsentationen H_enc ab; der Decoder ist ein bedingtes Sprachmodell, dessen Blöcke eine Cross-Attention-Schicht ergänzen, in der die Queries vom Decoder und Keys und Values aus der Encoder-Ausgabe stammen. Trainiert wird mit Kreuzentropie und Teacher Forcing. Quelle und Ziel teilen sich ein Subword-Vokabular, was das Kopieren von Namen erleichtert und Sprachen ohne Leerzeichen abdeckt; der Unigram-Algorithmus (SentencePiece) erzeugt meist bedeutungsvollere Token als BPE (Jurafsky & Martin, 2026).

#### 3. Trainingsdaten

Parallelkorpora sind etwa Europarl (400.000 bis 2 Millionen Sätze in jeder von 21 Sprachen), das United Nations Parallel Corpus, OpenSubtitles und ParaCrawl (223 Millionen Satzpaare). Neue Korpora brauchen ein Satz-Alignment, bewertet mit mehrsprachigen Satz-Embeddings und gelöst mit dynamischer Programmierung, sowie die Bereinigung verrauschter Paare (Jurafsky & Martin, 2026).

#### 4. Dekodierung

Gierige Dekodierung kann die wahrscheinlichste Folge verfehlen. Beam Search behält in jedem Schritt die k besten Hypothesen, bewertet sie über summierte Log-Wahrscheinlichkeiten und normiert auf die Länge; in der MT ist k meist 5 bis 10. Minimum-Bayes-Risk-Dekodierung sampelt Kandidaten und wählt den, der den anderen nach einer Metrik wie chrF am ähnlichsten ist, was noch besser als Beam Search funktionieren kann (Jurafsky & Martin, 2026).

#### 5. Übersetzung mit wenig Ressourcen

Backtranslation trainiert ein System in Gegenrichtung auf einem kleinen Bitext, übersetzt einsprachigen Text der Zielsprache zurück und ergänzt die synthetischen Paare; das bringt etwa 2/3 des Gewinns derselben Menge natürlicher Paralleldaten. Mehrsprachige Modelle markieren Quell- und Zielsprache mit Spezial-Token und lassen ressourcenarme Sprachen von verwandten profitieren, etwa Galicisch von Spanisch. Ein Audit fand, dass viele mehrsprachige Korpora weniger als 50 % akzeptable Sätze enthielten, und partizipative Ansätze beziehen Muttersprachler als Kuratierende und Bewertende ein (Jurafsky & Martin, 2026).

#### 6. Evaluation

Menschliche Bewertende beurteilen Adäquatheit (Treue zur Bedeutung der Quelle) und Flüssigkeit, ranken Kandidaten oder bearbeiten Ausgaben nach. chrF mittelt [[classification-metrics|Precision]] und Recall von Zeichen-N-Grammen und gewichtet den Recall doppelt (β = 2); es ist einfach, robust und korreliert gut mit menschlichen Urteilen. BLEU ist eine wortbasierte N-Gramm-Precision mit Kürzestrafe und empfindlich gegenüber der Tokenisierung; SacreBLEU standardisiert sie. Überlappungsmetriken sind lokal und eignen sich am besten für Änderungen an einem System, mit gepaarten Bootstrap-Tests für die Signifikanz. COMET und BLEURT sind auf menschlichen Bewertungen trainiert, BERTScore gleicht Token über Embedding-Ähnlichkeit ab (Jurafsky & Martin, 2026).

#### 7. Bias

Beim Übersetzen des geschlechtsneutralen ungarischen *ő* ins Englische wählten MT-Systeme *she* für eine Pflegekraft und *he* für einen CEO und verstärkten Stereotype über die Arbeitsmarktstatistik hinaus; WinoMT zeigt schlechtere Leistung bei nicht-stereotypen Geschlechterrollen. Weil MT im medizinischen und juristischen Bereich eingesetzt wird, brauchen Systeme Konfidenzwerte, um sich enthalten zu können (Jurafsky & Martin, 2026). LLMs zeigen verwandte Probleme: [[chatgpt|ChatGPT]] übersetzte das geschlechtsneutrale englische *they* ins Deutsche mit der dritten Person Plural und erzeugte so einen falschen Satz mit womöglich anderer Bedeutung (Urchs, 2025).

#### Herkunft und Varianten

MT wurde von Weaver (1949) vorgeschlagen; der ALPAC-Bericht von 1966 kürzte die Förderung in den USA. Frühe Architekturen waren direkte, Transfer- und Interlingua-Ansätze (Vauquois-Dreieck). Statistische MT begann um 1990 mit den IBM-Modellen und dem Hansard-Korpus, gefolgt von phrasenbasierter Übersetzung, Minimum Error Rate Training auf BLEU und Werkzeugen wie Moses. Den neuronalen Encoder-Decoder wandten Bahdanau et al. (2015) auf MT an, und den Transformer schlugen Vaswani et al. (2017) vor (Jurafsky & Martin, 2026).

### Wann einsetzen

- Informationszugang über Sprachgrenzen, der die digitale Kluft verringern hilft (Jurafsky & Martin, 2026).
- Computergestützte Übersetzung und Lokalisierung mit menschlichem Post-Editing (Jurafsky & Martin, 2026).
- Inkrementelle Sprachübersetzung und Übersetzung von Text in Bildern (Jurafsky & Martin, 2026).

### Stärken und Grenzen

**Stärken**
- Encoder-Decoder-Netze bewältigen komplexe Umordnungen und Divergenzen zwischen Sprachen (Jurafsky & Martin, 2026).
- Google Translate allein übersetzt täglich Hunderte Milliarden Wörter zwischen über 100 Sprachen (Jurafsky & Martin, 2026).

**Grenzen**
- Den meisten Sprachen fehlen große Parallelkorpora, und viele Systeme sind auf Englisch ausgerichtet (Jurafsky & Martin, 2026).
- Automatische Metriken können Diskurskohärenz nicht bewerten und vergleichen sehr unterschiedliche Systeme schlecht (Jurafsky & Martin, 2026).
- Gender-Bias beim Übersetzen aus geschlechtsneutralen Quellsprachen (Jurafsky & Martin, 2026; Urchs, 2025).

### Vergleich

| Metrik | Grundlage | Hinweis |
|--------|-----------|---------|
| Menschliche Adäquatheit/Flüssigkeit | Bewertende | Am genauesten, teuer |
| chrF | F-Score über Zeichen-N-Gramme | Einfach, robust, gute Korrelation |
| BLEU | Wort-N-Gramm-Precision + Kürzestrafe | Tokenisierungsabhängig |
| COMET / BLEURT | Auf menschlichen Bewertungen trainiert | Hohe Korrelation mit Menschen |
| BERTScore | Ähnlichkeit von Token-Embeddings | Keine menschlichen Bewertungen nötig |

Quelle: Jurafsky & Martin (2026).

### In der Praxis

MT beruht auf [[attention-and-transformers|Attention und Transformer]] und Subword-[[tokenisation|Tokenisierung]]; Sinnmehrdeutigkeiten verbinden sie mit der [[word-sense-disambiguation|Wortsinn-Disambiguierung]], und N-Gramm-Überlappungsmetriken sind mit den [[text-similarity-metrics|Textähnlichkeitsmetriken]] verwandt (Jurafsky & Martin, 2026). Gender-Bias in der Übersetzung ist ein Fall von [[bias-in-nlp|Bias in NLP]] (Jurafsky & Martin, 2026; Urchs, 2025).

### Merksatz

Maschinelle Übersetzung bildet Sätze zwischen Sprachen mit Encoder-Decoder-Transformern ab, die auf Parallelkorpora trainiert, mit Beam Search dekodiert und von Menschen oder mit Metriken wie chrF bewertet werden; ressourcenarme Sprachen und Gender-Bias bleiben offene Probleme.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Machine Translation.* Speech and Language Processing, 3rd ed. draft, Chapter 13. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/13.pdf)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
