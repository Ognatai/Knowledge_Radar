---
title_en: Tokenization
title_de: Tokenisierung
entity_type: Method
sources:
- https://arxiv.org/abs/1508.07909
- https://arxiv.org/abs/1609.08144
- https://arxiv.org/abs/1804.10959
- https://arxiv.org/abs/1808.06226
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Tokenization splits text into the units a model processes. Modern neural models use subword units: the vocabulary stays fixed and manageable, while rare and unknown words are represented as sequences of smaller pieces, which solves the open-vocabulary problem (Sennrich et al., 2015). The main algorithms are byte pair encoding (BPE), wordpieces and the unigram language model, implemented for example in SentencePiece ([[natural-language-processing|Natural Language Processing]]).

### How it works

A subword vocabulary is learned from training data. At inference time, each word or raw sentence is segmented into vocabulary units, so every input can be represented without an unknown-word token.

```text
1. The open-vocabulary problem
▼
2. Byte pair encoding (BPE)
▼
3. Wordpieces
▼
4. Unigram language model and subword regularization
▼
5. SentencePiece
```

#### 1. The open-vocabulary problem

Neural translation models typically work with a fixed vocabulary, but translation is an open-vocabulary problem: new names, compounds and rare words keep appearing. Earlier systems translated out-of-vocabulary words by backing off to a dictionary. Sennrich et al. (2015) instead encoded rare and unknown words as sequences of subword units, based on the intuition that many word classes are translatable via smaller units, for instance names via character copying or transliteration and compounds via compositional translation.

#### 2. Byte pair encoding (BPE)

Sennrich et al. (2015) adapted the byte pair encoding compression algorithm to word segmentation. Starting from characters, the most frequent adjacent pair of symbols in the training data is repeatedly merged into a new symbol; the number of merge operations determines the final vocabulary size. Frequent words end up as single tokens, rare words as sequences of subwords. Subword models improved over a back-off dictionary baseline by 1.1 BLEU on WMT 15 English-German and 1.3 BLEU on English-Russian (Sennrich et al., 2015).

#### 3. Wordpieces

Google's neural machine translation system (GNMT) divides words into a limited set of common sub-word units, called wordpieces, for both input and output (Wu et al., 2016). According to the authors, this gives a good balance between the flexibility of character-delimited models and the efficiency of word-delimited models, naturally handles the translation of rare words, and improves the overall accuracy of the system.

#### 4. Unigram language model and subword regularization

Subword segmentation is ambiguous: even with the same vocabulary, a sentence can usually be segmented in several ways. Kudo (2018) uses this ambiguity as noise to make translation models more robust. Subword regularization trains the model on multiple segmentations sampled probabilistically during training, and for better sampling the paper proposes a new segmentation algorithm based on a unigram language model. The method gave consistent improvements, especially in low-resource and out-of-domain settings (Kudo, 2018).

#### 5. SentencePiece

SentencePiece (Kudo & Richardson, 2018) is a language-independent subword tokenizer and detokenizer with open-source C++ and Python implementations. Existing subword tools assume that the input has already been split into words; SentencePiece trains subword models directly from raw sentences, which makes a purely end-to-end and language-independent system possible. In an English-Japanese translation experiment, training directly from raw sentences achieved accuracy comparable to subword training on pre-tokenized input.

#### Origin and variants

BPE was introduced for neural machine translation by Sennrich et al. (2015). GNMT used wordpieces (Wu et al., 2016). Kudo (2018) added the unigram language model and subword regularization, and SentencePiece (Kudo & Richardson, 2018) packaged subword training as a language-independent toolkit that works on raw text.

### When to use it

- When a neural model must handle an open vocabulary, such as names, compounds and rare words, without a dictionary fallback (Sennrich et al., 2015).
- When training data is scarce or the target domain differs from the training domain, subword regularization can make models more robust (Kudo, 2018).
- When text comes in languages or scripts where splitting into words is not straightforward, a tokenizer that works on raw sentences avoids language-specific pre-tokenization (Kudo & Richardson, 2018).

### Strengths and limitations

**Strengths**
- Represents rare and unknown words without a dictionary fallback and improved translation quality over such a baseline (Sennrich et al., 2015).
- Balances the flexibility of character-level and the efficiency of word-level models (Wu et al., 2016).
- Can be trained directly on raw text in a language-independent way (Kudo & Richardson, 2018).

**Limitations**
- Segmentation is ambiguous, since several segmentations are possible with the same vocabulary (Kudo, 2018).
- Rare words are split into several pieces, so they take up more tokens than frequent words (Sennrich et al., 2015).
- Most tools assume pre-tokenized input, which ties them to language-specific word splitting (Kudo & Richardson, 2018).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Word vocabulary with dictionary back-off | Unknown words are looked up in a dictionary instead of being modelled (Sennrich et al., 2015) | Closed domains with a stable vocabulary |
| BPE | Deterministic merges of frequent symbol pairs (Sennrich et al., 2015) | General subword segmentation |
| Wordpieces | Limited set of common sub-word units for input and output (Wu et al., 2016) | Large production translation systems |
| Unigram language model | Probabilistic segmentation, allows sampling of several segmentations (Kudo, 2018) | Robust training, low-resource and out-of-domain settings |

### In practice

The effect of a tokenizer is usually measured through the downstream task, for example BLEU in machine translation (Sennrich et al., 2015; [[text-similarity-metrics|Text Similarity Metrics]]). Vocabulary size is the central parameter: in BPE it is set through the number of merge operations (Sennrich et al., 2015). Specialised terms that were rare in the training data, such as legal citations, are split into many pieces, which matters for retrieval and is one reason why lexical search still complements semantic search ([[information-retrieval|Information Retrieval]]). SentencePiece (Kudo & Richardson, 2018) is a common choice when one tokenizer must work across languages.

### Key takeaway

Subword tokenization gives a model a fixed, manageable vocabulary while still representing every word, by splitting rare words into smaller pieces.

### Sources

- Sennrich, R. et al. (2015). *Neural Machine Translation of Rare Words with Subword Units.* ACL 2016. [arXiv:1508.07909](https://arxiv.org/abs/1508.07909)
- Wu, Y. et al. (2016). *Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation.* [arXiv:1609.08144](https://arxiv.org/abs/1609.08144)
- Kudo, T. (2018). *Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates.* ACL 2018. [arXiv:1804.10959](https://arxiv.org/abs/1804.10959)
- Kudo, T. & Richardson, J. (2018). *SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing.* EMNLP 2018. [arXiv:1808.06226](https://arxiv.org/abs/1808.06226)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Tokenisierung zerlegt Text in die Einheiten, mit denen ein Modell arbeitet. Moderne neuronale Modelle verwenden Subword-Einheiten: Das Vokabular bleibt fest und überschaubar, während seltene und unbekannte Wörter als Folgen kleinerer Teile dargestellt werden. Das löst das Problem des offenen Vokabulars (Sennrich et al., 2015). Die wichtigsten Verfahren sind Byte Pair Encoding (BPE), Wordpieces und das Unigram-Sprachmodell, implementiert etwa in SentencePiece ([[natural-language-processing|Natural Language Processing]]).

### Funktionsweise

Aus Trainingsdaten wird ein Subword-Vokabular gelernt. Bei der Inferenz wird jedes Wort oder jeder Rohsatz in Einheiten dieses Vokabulars zerlegt, sodass sich jede Eingabe ohne Token für unbekannte Wörter darstellen lässt.

```text
1. Das Problem des offenen Vokabulars
▼
2. Byte Pair Encoding (BPE)
▼
3. Wordpieces
▼
4. Unigram-Sprachmodell und Subword-Regularisierung
▼
5. SentencePiece
```

#### 1. Das Problem des offenen Vokabulars

Neuronale Übersetzungsmodelle arbeiten meist mit einem festen Vokabular, Übersetzung ist aber ein Problem mit offenem Vokabular: Neue Namen, Komposita und seltene Wörter tauchen immer wieder auf. Frühere Systeme übersetzten Wörter außerhalb des Vokabulars, indem sie auf ein Wörterbuch zurückgriffen. Sennrich et al. (2015) kodierten seltene und unbekannte Wörter stattdessen als Folgen von Subword-Einheiten. Dahinter steht die Beobachtung, dass sich viele Wortklassen über kleinere Einheiten übersetzen lassen, etwa Namen durch Kopieren oder Transliterieren von Zeichen und Komposita durch kompositionelle Übersetzung.

#### 2. Byte Pair Encoding (BPE)

Sennrich et al. (2015) übertrugen den Kompressionsalgorithmus Byte Pair Encoding auf die Wortsegmentierung. Ausgehend von einzelnen Zeichen wird das häufigste benachbarte Symbolpaar in den Trainingsdaten wiederholt zu einem neuen Symbol zusammengeführt; die Anzahl der Merge-Operationen bestimmt die Größe des Vokabulars. Häufige Wörter werden so zu einzelnen Token, seltene Wörter zu Folgen von Subwords. Subword-Modelle übertrafen eine Baseline mit Wörterbuch-Rückgriff um 1,1 BLEU auf WMT 15 Englisch-Deutsch und um 1,3 BLEU auf Englisch-Russisch (Sennrich et al., 2015).

#### 3. Wordpieces

Googles neuronales Übersetzungssystem GNMT zerlegt Wörter für Ein- und Ausgabe in eine begrenzte Menge häufiger Subword-Einheiten, sogenannte Wordpieces (Wu et al., 2016). Laut den Autoren verbindet das die Flexibilität zeichenbasierter Modelle mit der Effizienz wortbasierter Modelle, behandelt die Übersetzung seltener Wörter auf natürliche Weise und verbessert die Gesamtgenauigkeit des Systems.

#### 4. Unigram-Sprachmodell und Subword-Regularisierung

Die Subword-Segmentierung ist mehrdeutig: Selbst mit demselben Vokabular lässt sich ein Satz meist auf mehrere Arten zerlegen. Kudo (2018) nutzt diese Mehrdeutigkeit als Rauschen, um Übersetzungsmodelle robuster zu machen. Die Subword-Regularisierung trainiert das Modell mit mehreren Segmentierungen, die während des Trainings probabilistisch gesampelt werden; für besseres Sampling schlägt der Artikel einen neuen Segmentierungsalgorithmus auf Basis eines Unigram-Sprachmodells vor. Die Methode brachte durchgängig Verbesserungen, besonders bei wenigen Trainingsdaten und bei Daten außerhalb der Trainingsdomäne (Kudo, 2018).

#### 5. SentencePiece

SentencePiece (Kudo & Richardson, 2018) ist ein sprachunabhängiger Subword-Tokenizer und -Detokenizer mit Open-Source-Implementierungen in C++ und Python. Bestehende Subword-Werkzeuge setzen voraus, dass die Eingabe bereits in Wörter zerlegt ist; SentencePiece trainiert Subword-Modelle direkt auf Rohsätzen und ermöglicht so ein durchgängiges, sprachunabhängiges System. In einem Übersetzungsexperiment Englisch-Japanisch erreichte das Training direkt auf Rohsätzen eine vergleichbare Genauigkeit wie Subword-Training auf vorab tokenisierter Eingabe.

#### Ursprung und Varianten

BPE wurde von Sennrich et al. (2015) für die neuronale maschinelle Übersetzung eingeführt. GNMT verwendete Wordpieces (Wu et al., 2016). Kudo (2018) ergänzte das Unigram-Sprachmodell und die Subword-Regularisierung, und SentencePiece (Kudo & Richardson, 2018) machte das Subword-Training zu einem sprachunabhängigen Werkzeug, das auf Rohtext arbeitet.

### Wann einsetzen

- Wenn ein neuronales Modell ein offenes Vokabular mit Namen, Komposita und seltenen Wörtern ohne Wörterbuch-Rückgriff verarbeiten muss (Sennrich et al., 2015).
- Wenn Trainingsdaten knapp sind oder die Zieldomäne von der Trainingsdomäne abweicht, kann Subword-Regularisierung Modelle robuster machen (Kudo, 2018).
- Wenn Texte in Sprachen oder Schriften vorliegen, in denen die Zerlegung in Wörter nicht einfach ist, vermeidet ein Tokenizer, der auf Rohsätzen arbeitet, eine sprachspezifische Vortokenisierung (Kudo & Richardson, 2018).

### Stärken und Grenzen

**Stärken**
- Stellt seltene und unbekannte Wörter ohne Wörterbuch-Rückgriff dar und verbesserte die Übersetzungsqualität gegenüber einer solchen Baseline (Sennrich et al., 2015).
- Verbindet die Flexibilität zeichenbasierter mit der Effizienz wortbasierter Modelle (Wu et al., 2016).
- Lässt sich sprachunabhängig direkt auf Rohtext trainieren (Kudo & Richardson, 2018).

**Einschränkungen**
- Die Segmentierung ist mehrdeutig, da mit demselben Vokabular mehrere Zerlegungen möglich sind (Kudo, 2018).
- Seltene Wörter werden in mehrere Teile zerlegt und belegen daher mehr Token als häufige Wörter (Sennrich et al., 2015).
- Die meisten Werkzeuge setzen vortokenisierte Eingabe voraus und sind damit an eine sprachspezifische Wortzerlegung gebunden (Kudo & Richardson, 2018).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Wortvokabular mit Wörterbuch-Rückgriff | Unbekannte Wörter werden in einem Wörterbuch nachgeschlagen statt modelliert (Sennrich et al., 2015) | Geschlossene Domänen mit stabilem Vokabular |
| BPE | Deterministisches Zusammenführen häufiger Symbolpaare (Sennrich et al., 2015) | Allgemeine Subword-Segmentierung |
| Wordpieces | Begrenzte Menge häufiger Subword-Einheiten für Ein- und Ausgabe (Wu et al., 2016) | Große produktive Übersetzungssysteme |
| Unigram-Sprachmodell | Probabilistische Segmentierung, mehrere Zerlegungen können gesampelt werden (Kudo, 2018) | Robustes Training, wenige Daten und fremde Domänen |

### In der Praxis

Die Wirkung eines Tokenizers wird meist über die nachgelagerte Aufgabe gemessen, etwa mit BLEU in der maschinellen Übersetzung (Sennrich et al., 2015; [[text-similarity-metrics|Textähnlichkeitsmetriken]]). Zentraler Parameter ist die Vokabulargröße, die bei BPE über die Anzahl der Merge-Operationen festgelegt wird (Sennrich et al., 2015). Fachbegriffe, die in den Trainingsdaten selten waren, etwa juristische Zitate, werden in viele Teile zerlegt; das ist für das Retrieval relevant und ein Grund, warum lexikalische Suche die semantische Suche weiterhin ergänzt ([[information-retrieval|Information Retrieval]]). SentencePiece (Kudo & Richardson, 2018) ist eine verbreitete Wahl, wenn ein Tokenizer für mehrere Sprachen funktionieren muss.

### Merksatz

Subword-Tokenisierung gibt einem Modell ein festes, überschaubares Vokabular und kann trotzdem jedes Wort darstellen, indem sie seltene Wörter in kleinere Teile zerlegt.

### Quellen

- Sennrich, R. et al. (2015). *Neural Machine Translation of Rare Words with Subword Units.* ACL 2016. [arXiv:1508.07909](https://arxiv.org/abs/1508.07909)
- Wu, Y. et al. (2016). *Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation.* [arXiv:1609.08144](https://arxiv.org/abs/1609.08144)
- Kudo, T. (2018). *Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates.* ACL 2018. [arXiv:1804.10959](https://arxiv.org/abs/1804.10959)
- Kudo, T. & Richardson, J. (2018). *SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing.* EMNLP 2018. [arXiv:1808.06226](https://arxiv.org/abs/1808.06226)
