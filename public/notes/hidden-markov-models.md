---
title_en: Hidden Markov Models
title_de: Hidden-Markov-Modelle
entity_type: Method
aliases:
- Hidden Markov model
- HMM
- Viterbi algorithm
- Forward algorithm
- Forward-backward algorithm
- Baum-Welch algorithm
- Markov chain
sources:
- https://web.stanford.edu/~jurafsky/slp3/A.pdf
- https://web.stanford.edu/~jurafsky/slp3/18.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A hidden Markov model (HMM) relates a sequence of observations, such as words, to a sequence of hidden states, such as part-of-speech tags, that are thought to have caused them (Jurafsky & Martin, 2026, App. A). It consists of transition probabilities between states (A), emission probabilities of observations given a state (B) and a start distribution (π). Three problems define it: computing the likelihood of an observation sequence (forward algorithm), finding the best hidden state sequence (Viterbi algorithm) and learning A and B from unlabelled data (forward-backward or Baum-Welch algorithm) (Jurafsky & Martin, 2026, App. A).

### How it works

```text
hidden states   q1 ──a12──► q2 ──a23──► q3        transition probabilities A, start π
                 │           │           │
                b1(o1)      b2(o2)      b3(o3)     emission probabilities B
observations    o1          o2          o3

likelihood P(O|λ)      forward algorithm   (sum over paths, O(N²T))
best state sequence    Viterbi algorithm   (max over paths + backpointers)
learn A and B          forward-backward    (EM: E-step γ, ξ · M-step re-estimate)
```

#### 1. Markov chain and hidden states

A Markov chain assigns probabilities to sequences of states under the Markov assumption that only the current state matters for predicting the next; a bigram language model is a Markov chain over words. Often the events of interest are hidden: one sees words, not their part-of-speech tags. A first-order HMM adds two assumptions: a state depends only on the previous state, and an observation depends only on the state that produced it (output independence) (Jurafsky & Martin, 2026, App. A).

#### 2. Likelihood: the forward algorithm

The textbook example (after Jason Eisner) infers hot and cold days from the number of ice creams eaten. The probability of an observation sequence sums over all hidden state sequences, of which there are N^T for N states and T observations. The forward algorithm avoids this with dynamic programming: each trellis cell α_t(j) = Σ_i α_t−1(i)·a_ij·b_j(o_t) holds the probability of the first t observations and ending in state j, giving O(N²T) time (Jurafsky & Martin, 2026, App. A).

#### 3. Decoding: the Viterbi algorithm

Decoding finds the most probable hidden state sequence. The Viterbi algorithm is identical to the forward algorithm except that it takes the maximum over previous paths instead of the sum, and keeps backpointers so that the best path can be traced back at the end. It resembles the minimum edit distance algorithm (Jurafsky & Martin, 2026, App. A).

#### 4. Learning: the forward-backward algorithm

With labelled data, A and B are estimated by counting. Without labels, the forward-backward or Baum-Welch algorithm (Baum, 1972), a special case of the EM algorithm, iterates: in the E-step it uses forward and backward probabilities to compute the expected state occupancy γ and expected transitions ξ; in the M-step it re-estimates A and B from them. In practice the initial conditions matter a lot; in HMM speech recognition, for example, the structure is set by hand and only the probabilities are trained (Jurafsky & Martin, 2026, App. A).

#### 5. HMM part-of-speech tagging

An HMM tagger estimates tag transitions P(t_i | t_i−1) and emissions P(w_i | t_i) by counting on a tagged corpus: in the WSJ corpus, P(VB | MD) = 0.80 and P(will | MD) = 0.31. The best tag sequence maximises the product of emission and transition probabilities and is found with Viterbi (Jurafsky & Martin, 2026, ch. 18). Details are in [[part-of-speech-tagging|Part-of-Speech Tagging]].

#### Origin and variants

Markov (1913) used Markov chains on letters in *Eugene Onegin*; the HMM was developed by Baum and colleagues at the Institute for Defense Analyses in Princeton (Baum & Petrie, 1966). The Viterbi algorithm was discovered independently in information theory (Viterbi, 1967), speech processing (Vintsyuk, 1968), molecular biology (Needleman & Wunsch, 1970) and computer science (Wagner & Fischer, 1974). Rabiner's (1989) tutorial framed the three fundamental problems (Jurafsky & Martin, 2026, App. A). Segmental HMMs or semi-HMMs drop the one-to-one mapping between states and observations (Jurafsky & Martin, 2026, App. A).

### When to use it

- Sequence labelling where hidden classes explain observations, such as part-of-speech tagging (Jurafsky & Martin, 2026, ch. 18).
- Speech recognition, where HMM structures are set by hand and their probabilities trained (Jurafsky & Martin, 2026, App. A).
- When no labelled data exist, forward-backward can in principle learn the parameters without supervision (Jurafsky & Martin, 2026, App. A).

### Strengths and limitations

**Strengths**
- Efficient exact inference by dynamic programming (Jurafsky & Martin, 2026, App. A).
- HMM taggers reach accuracies close to the state of the art (Jurafsky & Martin, 2026, ch. 18).

**Limitations**
- As generative models, HMMs make it hard to add arbitrary features such as capitalisation or suffixes for unknown words; each knowledge source must be encoded in P(tag | tag) or P(word | tag) (Jurafsky & Martin, 2026, ch. 18).
- Fully unsupervised EM did not work well for tagging; hand-labelled data were important (Merialdo, 1994, in Jurafsky & Martin, 2026, ch. 18).
- Unsupervised training depends heavily on initial conditions (Jurafsky & Martin, 2026, App. A).

### Comparison

| Model | Type | Features | Decoding |
|-------|------|----------|----------|
| HMM | Generative, P(X\|Y)·P(Y) | Only tag transitions and word emissions | Viterbi |
| Linear-chain CRF | Discriminative, P(Y\|X) directly | Arbitrary features of the whole input | Viterbi |

Source: Jurafsky & Martin (2026, ch. 18).

### In practice

Linear-chain CRFs reuse the Viterbi and forward-backward algorithms of the HMM while allowing rich features (Jurafsky & Martin, 2026, ch. 18). HMMs and n-gram models share the Markov assumption ([[n-gram-language-models|N-gram Language Models]]), and the Viterbi algorithm was first applied to speech and language processing in speech recognition (Vintsyuk, 1968), see [[automatic-speech-recognition|Automatic Speech Recognition]] (Jurafsky & Martin, 2026, App. A).

### Key takeaway

An HMM explains observations by hidden states with transition and emission probabilities; the forward algorithm computes likelihoods, Viterbi finds the best state sequence and forward-backward learns the parameters.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Hidden Markov Models.* Speech and Language Processing, 3rd ed. draft, Appendix A. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/A.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Sequence Labeling for Parts of Speech and Named Entities.* Speech and Language Processing, 3rd ed. draft, Chapter 18. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/18.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Hidden-Markov-Modell (HMM) verknüpft eine Folge von Beobachtungen, etwa Wörtern, mit einer Folge verborgener Zustände, etwa Part-of-Speech-Tags, die sie verursacht haben sollen (Jurafsky & Martin, 2026, Anh. A). Es besteht aus Übergangswahrscheinlichkeiten zwischen Zuständen (A), Emissionswahrscheinlichkeiten der Beobachtungen gegeben einen Zustand (B) und einer Startverteilung (π). Drei Probleme bestimmen es: die Likelihood einer Beobachtungsfolge berechnen (Forward-Algorithmus), die beste verborgene Zustandsfolge finden (Viterbi-Algorithmus) und A und B aus ungelabelten Daten lernen (Forward-Backward- oder Baum-Welch-Algorithmus) (Jurafsky & Martin, 2026, Anh. A).

### Funktionsweise

```text
verborgene Zustände  q1 ──a12──► q2 ──a23──► q3     Übergangswahrscheinlichkeiten A, Start π
                      │           │           │
                     b1(o1)      b2(o2)      b3(o3)  Emissionswahrscheinlichkeiten B
Beobachtungen        o1          o2          o3

Likelihood P(O|λ)        Forward-Algorithmus   (Summe über Pfade, O(N²T))
beste Zustandsfolge      Viterbi-Algorithmus   (Maximum über Pfade + Rückzeiger)
A und B lernen           Forward-Backward      (EM: E-Schritt γ, ξ · M-Schritt neu schätzen)
```

#### 1. Markov-Kette und verborgene Zustände

Eine Markov-Kette weist Zustandsfolgen Wahrscheinlichkeiten zu, unter der Markov-Annahme, dass für die Vorhersage des nächsten Zustands nur der aktuelle zählt; ein Bigramm-Sprachmodell ist eine Markov-Kette über Wörtern. Oft sind die interessierenden Ereignisse verborgen: Man sieht Wörter, nicht ihre Part-of-Speech-Tags. Ein HMM erster Ordnung fügt zwei Annahmen hinzu: Ein Zustand hängt nur vom vorherigen ab, und eine Beobachtung hängt nur von dem Zustand ab, der sie erzeugt hat (Ausgabe-Unabhängigkeit) (Jurafsky & Martin, 2026, Anh. A).

#### 2. Likelihood: der Forward-Algorithmus

Das Lehrbuchbeispiel (nach Jason Eisner) erschließt heiße und kalte Tage aus der Zahl gegessener Eiskugeln. Die Wahrscheinlichkeit einer Beobachtungsfolge summiert über alle verborgenen Zustandsfolgen, von denen es bei N Zuständen und T Beobachtungen N^T gibt. Der Forward-Algorithmus vermeidet das mit dynamischer Programmierung: Jede Zelle des Trellis α_t(j) = Σ_i α_t−1(i)·a_ij·b_j(o_t) enthält die Wahrscheinlichkeit der ersten t Beobachtungen bei Endzustand j, was O(N²T) Zeit ergibt (Jurafsky & Martin, 2026, Anh. A).

#### 3. Dekodierung: der Viterbi-Algorithmus

Dekodierung findet die wahrscheinlichste verborgene Zustandsfolge. Der Viterbi-Algorithmus gleicht dem Forward-Algorithmus, nimmt aber das Maximum statt der Summe über vorherige Pfade und speichert Rückzeiger, damit sich der beste Pfad am Ende zurückverfolgen lässt. Er ähnelt dem Algorithmus für die minimale Editierdistanz (Jurafsky & Martin, 2026, Anh. A).

#### 4. Lernen: der Forward-Backward-Algorithmus

Mit gelabelten Daten werden A und B durch Zählen geschätzt. Ohne Labels iteriert der Forward-Backward- oder Baum-Welch-Algorithmus (Baum, 1972), ein Spezialfall des EM-Algorithmus: Im E-Schritt berechnet er mit Vorwärts- und Rückwärtswahrscheinlichkeiten die erwartete Zustandsbelegung γ und die erwarteten Übergänge ξ; im M-Schritt schätzt er A und B daraus neu. In der Praxis sind die Anfangsbedingungen sehr wichtig; in der HMM-Spracherkennung wird etwa die Struktur von Hand festgelegt und nur die Wahrscheinlichkeiten werden trainiert (Jurafsky & Martin, 2026, Anh. A).

#### 5. Part-of-Speech-Tagging mit HMM

Ein HMM-Tagger schätzt Tag-Übergänge P(t_i | t_i−1) und Emissionen P(w_i | t_i) durch Zählen auf einem getaggten Korpus: Im WSJ-Korpus ist P(VB | MD) = 0,80 und P(will | MD) = 0,31. Die beste Tag-Folge maximiert das Produkt aus Emissions- und Übergangswahrscheinlichkeiten und wird mit Viterbi gefunden (Jurafsky & Martin, 2026, Kap. 18). Details stehen in [[part-of-speech-tagging|Part-of-Speech-Tagging]].

#### Herkunft und Varianten

Markov (1913) nutzte Markov-Ketten auf Buchstaben in *Eugen Onegin*; das HMM entwickelten Baum und Kollegen am Institute for Defense Analyses in Princeton (Baum & Petrie, 1966). Der Viterbi-Algorithmus wurde unabhängig in der Informationstheorie (Viterbi, 1967), der Sprachverarbeitung (Vintsyuk, 1968), der Molekularbiologie (Needleman & Wunsch, 1970) und der Informatik (Wagner & Fischer, 1974) entdeckt. Rabiners (1989) Tutorial formulierte die drei grundlegenden Probleme (Jurafsky & Martin, 2026, Anh. A). Segmentelle HMMs oder Semi-HMMs geben die Eins-zu-eins-Zuordnung von Zuständen und Beobachtungen auf (Jurafsky & Martin, 2026, Anh. A).

### Wann einsetzen

- Sequenzmarkierung, bei der verborgene Klassen Beobachtungen erklären, etwa Part-of-Speech-Tagging (Jurafsky & Martin, 2026, Kap. 18).
- Spracherkennung, bei der HMM-Strukturen von Hand festgelegt und ihre Wahrscheinlichkeiten trainiert werden (Jurafsky & Martin, 2026, Anh. A).
- Wenn keine gelabelten Daten vorliegen, kann Forward-Backward die Parameter grundsätzlich unüberwacht lernen (Jurafsky & Martin, 2026, Anh. A).

### Stärken und Grenzen

**Stärken**
- Effiziente exakte Inferenz durch dynamische Programmierung (Jurafsky & Martin, 2026, Anh. A).
- HMM-Tagger erreichen Genauigkeiten nahe am Stand der Technik (Jurafsky & Martin, 2026, Kap. 18).

**Grenzen**
- Als generative Modelle erschweren HMMs das Hinzufügen beliebiger Merkmale wie Großschreibung oder Suffixe für unbekannte Wörter; jede Wissensquelle muss in P(Tag | Tag) oder P(Wort | Tag) kodiert werden (Jurafsky & Martin, 2026, Kap. 18).
- Vollständig unüberwachtes EM funktionierte für Tagging nicht gut; von Hand gelabelte Daten waren wichtig (Merialdo, 1994, in Jurafsky & Martin, 2026, Kap. 18).
- Unüberwachtes Training hängt stark von den Anfangsbedingungen ab (Jurafsky & Martin, 2026, Anh. A).

### Vergleich

| Modell | Art | Merkmale | Dekodierung |
|--------|-----|----------|-------------|
| HMM | Generativ, P(X\|Y)·P(Y) | Nur Tag-Übergänge und Wort-Emissionen | Viterbi |
| Linear-Chain-CRF | Diskriminativ, direkt P(Y\|X) | Beliebige Merkmale der ganzen Eingabe | Viterbi |

Quelle: Jurafsky & Martin (2026, Kap. 18).

### In der Praxis

Linear-Chain-CRFs übernehmen den Viterbi- und den Forward-Backward-Algorithmus des HMM und erlauben dabei reichhaltige Merkmale (Jurafsky & Martin, 2026, Kap. 18). HMMs und N-Gramm-Modelle teilen die Markov-Annahme ([[n-gram-language-models|N-Gramm-Sprachmodelle]]), und der Viterbi-Algorithmus wurde in der Sprachverarbeitung zuerst für die Spracherkennung eingesetzt (Vintsyuk, 1968), siehe [[automatic-speech-recognition|automatische Spracherkennung]] (Jurafsky & Martin, 2026, Anh. A).

### Merksatz

Ein HMM erklärt Beobachtungen durch verborgene Zustände mit Übergangs- und Emissionswahrscheinlichkeiten; der Forward-Algorithmus berechnet Likelihoods, Viterbi findet die beste Zustandsfolge, und Forward-Backward lernt die Parameter.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Hidden Markov Models.* Speech and Language Processing, 3rd ed. draft, Appendix A. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/A.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Sequence Labeling for Parts of Speech and Named Entities.* Speech and Language Processing, 3rd ed. draft, Chapter 18. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/18.pdf)
