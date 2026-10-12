---
title_en: Part-of-Speech Tagging
title_de: Wortart-Tagging
entity_type: Method
aliases:
- POS tagging
- Part-of-speech tagger
- Sequence labeling
- Conditional random field
- CRF
- Linear-chain CRF
sources:
- https://web.stanford.edu/~jurafsky/slp3/18.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Part-of-speech (POS) tagging assigns each word in a text a part of speech such as NOUN or VERB; it is a disambiguation task, because many frequent words can take several tags (Jurafsky & Martin, 2026). It is a sequence labelling task, like named entity recognition, solved classically with a generative hidden Markov model or a discriminative conditional random field (CRF), and today with neural models. Accuracy on English is about 97% for HMMs, CRFs and [[bert|BERT]] alike, close to human agreement; the most-frequent-tag baseline reaches about 92% (Jurafsky & Martin, 2026).

### How it works

```text
Janet   will   back   the   bill        words x1 … xn
  │       │      │      │      │
 NNP     MD     VB     DT     NN         tags y1 … yn (one per word)

HMM:  argmax Π P(w_i | t_i) · P(t_i | t_i-1)           generative, counts from a tagged corpus
CRF:  argmax Σ_i Σ_k w_k f_k(y_i-1, y_i, X, i)          discriminative, arbitrary features
both decoded with the Viterbi algorithm
```

#### 1. Parts of speech and tagsets

Parts of speech go back to the eight word classes of Dionysius Thrax. Closed classes such as prepositions, determiners and pronouns have fixed membership and are mostly short, frequent function words; open classes such as nouns, verbs, adjectives, adverbs and interjections keep growing (*iPhone*, *to fax*). The Universal Dependencies tagset has 17 tags; the English Penn Treebank tagset has 36 core tags and distinguishes, for example, verb tense and participles (Jurafsky & Martin, 2026).

#### 2. Ambiguity and the baseline

In the WSJ and Brown corpora, 85–86% of word types are unambiguous, but the ambiguous ones are frequent, so 55–67% of tokens in running text are ambiguous; *back* alone can be an adjective, noun, verb, particle or adverb. Always choosing a word's most frequent tag in the training corpus reaches about 92%, which every tagger must beat (Jurafsky & Martin, 2026).

#### 3. HMM tagger

The HMM tagger estimates transition probabilities P(t_i | t_i−1) and emission probabilities P(w_i | t_i) by counting on a tagged corpus; in the WSJ, a modal (MD) is followed by a base-form verb with probability 0.80. Using Bayes' rule, the Markov assumption and output independence, the best tag sequence maximises the product of emissions and transitions and is found with the Viterbi algorithm ([[hidden-markov-models|Hidden Markov Models]]) (Jurafsky & Martin, 2026).

#### 4. Conditional random fields

HMMs make it hard to add features for unknown words, such as capitalisation or the suffix *-ed*. A linear-chain CRF is a log-linear model that computes P(Y | X) for the whole tag sequence directly: local features may use the current and previous tag, the entire input and the position, and are summed and normalised over the sequence. Feature templates generate features such as "tag VB and word *back*"; word shape (*DC10-30* → *XXdd-dd*), prefixes and suffixes help with unknown words. Decoding uses Viterbi and training uses stochastic gradient descent with a CRF version of forward-backward and L1 or L2 regularisation (Jurafsky & Martin, 2026).

#### 5. Named entities as sequence labelling

Named entity recognition finds and types spans such as PER, ORG, LOC and GPE. BIO tagging (begin, inside, outside) turns span finding into one tag per word, so the same sequence labellers apply; NER is evaluated per entity with precision, recall and F1, POS tagging with accuracy (Jurafsky & Martin, 2026). Details are in [[entity-extraction|Entity Extraction]].

#### Origin and variants

The earliest POS tagger was part of Zellig Harris's TDAP parser (1958–1959) with 14 hand-written rules; TAGGIT tagged 77% of the Brown corpus correctly. Church's PARTS tagger (1988) was probably the first implemented HMM tagger; Ratnaparkhi (1996) introduced log-linear tagging with maximum entropy Markov models, a simpler version of the CRF (Lafferty et al., 2001). State-of-the-art taggers use bidirectional RNNs or Transformers such as BERT, with HMM and CRF taggers likely only slightly lower. Morphologically rich languages such as Turkish need tags that are sequences of morphological features, making tagsets 4 to 10 times larger (Jurafsky & Martin, 2026).

### When to use it

- As a key step in parsing, because word classes predict neighbouring words and syntactic structure (Jurafsky & Martin, 2026).
- As features for named entity recognition, together with word shape and gazetteers (Jurafsky & Martin, 2026).
- Datasets: Universal Dependencies has POS-tagged corpora in over a hundred languages (Jurafsky & Martin, 2026).

### Strengths and limitations

**Strengths**
- Very high accuracy, about 97% on English treebanks and over 97% across 15 UD languages (Jurafsky & Martin, 2026).
- CRFs combine arbitrary features in a principled way while keeping efficient Viterbi decoding (Jurafsky & Martin, 2026).

**Limitations**
- Supervised tagging relies on in-domain data hand-labelled by experts (Jurafsky & Martin, 2026).
- Of the remaining errors of a strong tagger, a third to a half are due to errors or inconsistencies in the training data (Manning, 2011, in Jurafsky & Martin, 2026).
- Rich morphology means large vocabularies and many unknown words, which degrades performance (Jurafsky & Martin, 2026).

### Comparison

| Approach | Model | Accuracy on English |
|----------|-------|---------------------|
| Most frequent tag | Lookup | about 92% |
| HMM | Generative, counts | about 97% |
| CRF | Discriminative, features | about 97% |
| BERT / neural | Contextual representations | about 97% |

Source: Jurafsky & Martin (2026).

### In practice

POS tags and named entities are useful clues to sentence structure and meaning ([[natural-language-processing|Natural Language Processing]]), and commercial NER often combines lists and rules with some supervised learning (Jurafsky & Martin, 2026). Parsers build on tagging: see [[constituency-parsing|Constituency Parsing]] and [[dependency-parsing|Dependency Parsing]].

### Key takeaway

POS tagging labels every word with its word class; HMMs and CRFs with Viterbi decoding reach about 97% on English, close to human agreement and only five points above the most-frequent-tag baseline.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Sequence Labeling for Parts of Speech and Named Entities.* Speech and Language Processing, 3rd ed. draft, Chapter 18. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/18.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Wortart-Tagging (POS-Tagging) weist jedem Wort eines Textes eine Wortart wie NOUN oder VERB zu; es ist eine Disambiguierungsaufgabe, weil viele häufige Wörter mehrere Tags annehmen können (Jurafsky & Martin, 2026). Es ist eine Sequenzmarkierungsaufgabe wie die Named Entity Recognition und wird klassisch mit einem generativen Hidden-Markov-Modell oder einem diskriminativen Conditional Random Field (CRF) gelöst, heute mit neuronalen Modellen. Die Genauigkeit auf Englisch liegt bei HMMs, CRFs und [[bert|BERT]] gleichermaßen bei etwa 97 %, nahe an der Übereinstimmung von Menschen; die Baseline mit dem häufigsten Tag erreicht etwa 92 % (Jurafsky & Martin, 2026).

### Funktionsweise

```text
Janet   will   back   the   bill        Wörter x1 … xn
  │       │      │      │      │
 NNP     MD     VB     DT     NN         Tags y1 … yn (eines pro Wort)

HMM:  argmax Π P(w_i | t_i) · P(t_i | t_i-1)           generativ, Zählungen aus getaggtem Korpus
CRF:  argmax Σ_i Σ_k w_k f_k(y_i-1, y_i, X, i)          diskriminativ, beliebige Merkmale
beide mit dem Viterbi-Algorithmus dekodiert
```

#### 1. Wortarten und Tagsets

Wortarten gehen auf die acht Wortklassen des Dionysios Thrax zurück. Geschlossene Klassen wie Präpositionen, Determinierer und Pronomen haben einen festen Bestand und sind meist kurze, häufige Funktionswörter; offene Klassen wie Nomen, Verben, Adjektive, Adverbien und Interjektionen wachsen ständig (*iPhone*, *to fax*). Das Tagset von Universal Dependencies hat 17 Tags; das englische Penn-Treebank-Tagset hat 36 Kern-Tags und unterscheidet etwa Tempus und Partizipien von Verben (Jurafsky & Martin, 2026).

#### 2. Mehrdeutigkeit und Baseline

In den Korpora WSJ und Brown sind 85–86 % der Worttypen eindeutig, doch die mehrdeutigen sind häufig, sodass 55–67 % der Token in laufendem Text mehrdeutig sind; *back* allein kann Adjektiv, Nomen, Verb, Partikel oder Adverb sein. Immer das im Trainingskorpus häufigste Tag eines Wortes zu wählen, erreicht etwa 92 %, was jeder Tagger übertreffen muss (Jurafsky & Martin, 2026).

#### 3. HMM-Tagger

Der HMM-Tagger schätzt Übergangswahrscheinlichkeiten P(t_i | t_i−1) und Emissionswahrscheinlichkeiten P(w_i | t_i) durch Zählen auf einem getaggten Korpus; im WSJ folgt auf ein Modalverb (MD) mit Wahrscheinlichkeit 0,80 ein Verb in der Grundform. Mit der Bayes-Regel, der Markov-Annahme und der Ausgabe-Unabhängigkeit maximiert die beste Tag-Folge das Produkt aus Emissionen und Übergängen und wird mit dem Viterbi-Algorithmus gefunden ([[hidden-markov-models|Hidden-Markov-Modelle]]) (Jurafsky & Martin, 2026).

#### 4. Conditional Random Fields

HMMs erschweren Merkmale für unbekannte Wörter, etwa Großschreibung oder das Suffix *-ed*. Ein Linear-Chain-CRF ist ein log-lineares Modell, das P(Y | X) für die ganze Tag-Folge direkt berechnet: Lokale Merkmale dürfen das aktuelle und das vorherige Tag, die gesamte Eingabe und die Position nutzen und werden über die Folge summiert und normalisiert. Merkmalsvorlagen erzeugen Merkmale wie „Tag VB und Wort *back*“; Wortform (*DC10-30* → *XXdd-dd*), Präfixe und Suffixe helfen bei unbekannten Wörtern. Dekodiert wird mit Viterbi, trainiert mit stochastischem Gradientenabstieg, einer CRF-Version von Forward-Backward und L1- oder L2-Regularisierung (Jurafsky & Martin, 2026).

#### 5. Named Entities als Sequenzmarkierung

Named Entity Recognition findet und typisiert Spannen wie PER, ORG, LOC und GPE. BIO-Tagging (begin, inside, outside) macht aus der Spannensuche ein Tag pro Wort, sodass dieselben Sequenzmarkierer greifen; NER wird pro Entität mit Precision, Recall und F1 bewertet, Wortart-Tagging mit Accuracy (Jurafsky & Martin, 2026). Details stehen in [[entity-extraction|Entitätsextraktion]].

#### Herkunft und Varianten

Der früheste Wortart-Tagger war Teil von Zellig Harris' Parser TDAP (1958–1959) mit 14 handgeschriebenen Regeln; TAGGIT taggte 77 % des Brown-Korpus korrekt. Churchs PARTS-Tagger (1988) war wohl der erste implementierte HMM-Tagger; Ratnaparkhi (1996) führte log-lineares Tagging mit Maximum-Entropy-Markov-Modellen ein, einer einfacheren Version des CRF (Lafferty et al., 2001). Aktuelle Tagger nutzen bidirektionale RNNs oder Transformer wie BERT, HMM- und CRF-Tagger liegen vermutlich nur wenig darunter. Morphologisch reiche Sprachen wie Türkisch brauchen Tags aus Folgen morphologischer Merkmale, wodurch Tagsets 4- bis 10-mal größer werden (Jurafsky & Martin, 2026).

### Wann einsetzen

- Als wichtiger Schritt beim Parsing, weil Wortklassen benachbarte Wörter und syntaktische Struktur vorhersagen (Jurafsky & Martin, 2026).
- Als Merkmale für Named Entity Recognition, zusammen mit Wortform und Gazetteers (Jurafsky & Martin, 2026).
- Datensätze: Universal Dependencies bietet getaggte Korpora in über hundert Sprachen (Jurafsky & Martin, 2026).

### Stärken und Grenzen

**Stärken**
- Sehr hohe Genauigkeit, etwa 97 % auf englischen Treebanks und über 97 % in 15 UD-Sprachen (Jurafsky & Martin, 2026).
- CRFs kombinieren beliebige Merkmale auf prinzipielle Weise und behalten die effiziente Viterbi-Dekodierung (Jurafsky & Martin, 2026).

**Grenzen**
- Überwachtes Tagging braucht von Fachleuten gelabelte Daten aus der Zieldomäne (Jurafsky & Martin, 2026).
- Von den verbleibenden Fehlern eines starken Taggers gehen ein Drittel bis die Hälfte auf Fehler oder Inkonsistenzen in den Trainingsdaten zurück (Manning, 2011, in Jurafsky & Martin, 2026).
- Reiche Morphologie bedeutet große Vokabulare und viele unbekannte Wörter, was die Leistung senkt (Jurafsky & Martin, 2026).

### Vergleich

| Ansatz | Modell | Genauigkeit auf Englisch |
|--------|--------|--------------------------|
| Häufigstes Tag | Nachschlagen | etwa 92 % |
| HMM | Generativ, Zählungen | etwa 97 % |
| CRF | Diskriminativ, Merkmale | etwa 97 % |
| BERT / neuronal | Kontextuelle Repräsentationen | etwa 97 % |

Quelle: Jurafsky & Martin (2026).

### In der Praxis

Wortarten und Named Entities sind nützliche Hinweise auf Satzstruktur und Bedeutung ([[natural-language-processing|Natural Language Processing]]), und kommerzielle NER kombiniert oft Listen und Regeln mit etwas überwachtem Lernen (Jurafsky & Martin, 2026). Parser bauen auf dem Tagging auf: siehe [[constituency-parsing|Konstituentenparsing]] und [[dependency-parsing|Dependenzparsing]].

### Merksatz

Wortart-Tagging versieht jedes Wort mit seiner Wortklasse; HMMs und CRFs mit Viterbi-Dekodierung erreichen auf Englisch etwa 97 %, nahe an menschlicher Übereinstimmung und nur fünf Punkte über der Baseline mit dem häufigsten Tag.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Sequence Labeling for Parts of Speech and Named Entities.* Speech and Language Processing, 3rd ed. draft, Chapter 18. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/18.pdf)
