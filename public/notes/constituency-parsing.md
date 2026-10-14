---
title_en: Constituency Parsing
title_de: Konstituentenparsing
entity_type: Method
aliases:
- Constituency parser
- Syntactic parsing
- Context-free grammar
- CFG
- Probabilistic context-free grammar
- PCFG
- CKY algorithm
- Treebank
sources:
- https://web.stanford.edu/~jurafsky/slp3/19.pdf
- https://web.stanford.edu/~jurafsky/slp3/E.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Constituency is the idea that groups of words, such as noun phrases, behave as single units; context-free grammars (CFGs) model this with rules like S → NP VP, and syntactic parsing assigns a sentence its parse tree (Jurafsky & Martin, 2026, ch. 19). The CKY algorithm uses dynamic programming to represent all parses of an ambiguous sentence compactly but does not choose one. Disambiguation is done with probabilistic context-free grammars (PCFGs), which pick the most probable tree (Jurafsky & Martin, 2026, App. E), or with neural span-based parsers that score each constituent. Parsers are evaluated with the PARSEVAL metrics (Jurafsky & Martin, 2026, ch. 19).

### How it works

```text
sentence ─► grammar in Chomsky normal form (A → B C, A → w)
         ─► CKY chart: cell [i,j] = all constituents spanning words i..j   (bottom-up)
         ─► disambiguation:
              PCFG: P(tree) = Π P(rule)  →  probabilistic CKY picks the most probable tree
              neural: score s(i,j,label) per span  →  CKY over span scores
         ─► PARSEVAL: labeled precision, recall, F1, crossing brackets against a treebank
```

#### 1. Context-free grammars and treebanks

A CFG consists of rules over non-terminals (NP, VP, PP) and terminals (words); a derivation from the start symbol S yields a parse tree. The idea of constituent structure goes back to Wilhelm Wundt (1900) and was formalised by Chomsky (1956) and, independently, by Backus (1959), whose Backus-Naur form is equivalent. Treebanks such as the Penn Treebank annotate every sentence with a tree, usually by hand-correcting parser output; their grammars are very flat, with about 4,500 rules for expanding VPs alone (Jurafsky & Martin, 2026, ch. 19).

#### 2. Ambiguity

Structural ambiguity is the most serious problem for parsers. In *I shot an elephant in my pajamas* the prepositional phrase can attach to the noun phrase or the verb phrase (PP-attachment ambiguity); in *old men and women* the adjective can scope over both nouns or one (coordination ambiguity). Real sentences have many grammatically correct but semantically unreasonable parses (Jurafsky & Martin, 2026, ch. 19).

#### 3. The CKY algorithm

CKY (Cocke, Kasami, Younger) requires Chomsky normal form, where every rule has two non-terminals or one terminal on the right; any CFG can be converted to a weakly equivalent CNF grammar. For a sentence of n words it fills the upper triangle of an (n+1)×(n+1) table; cell [i,j] holds all non-terminals spanning positions i to j, built from pairs [i,k] and [k,j]. With backpointers, the table contains all possible parses, but CKY does not say which is right (Jurafsky & Martin, 2026, ch. 19).

#### 4. Probabilistic CFGs

A PCFG attaches a probability P(β | A) to every rule A → β; the probability of a tree is the product of its rule probabilities, and the parser chooses the most probable tree, using probabilistic CKY (Ney, 1991). For *Book the dinner flight*, the sensible parse gets 2.2×10⁻⁶ and the nonsensical one 6.1×10⁻⁷. Rule probabilities are counted from a treebank, or learned from unparsed text with the inside-outside algorithm (Baker, 1979), an EM generalisation of forward-backward. PCFGs can also serve as language models that condition on the whole previous context (Jurafsky & Martin, 2026, App. E).

#### 5. Problems of PCFGs and their fixes

PCFG rules are independent of their context, although NPs in subject position are pronouns 91% of the time and in object position only 34%. They also ignore words: a PCFG always prefers either NP or VP attachment, so it cannot get both *dumped sacks into a bin* (VP) and *caught tons of herring* (NP) right. Fixes are splitting non-terminals, for example by parent annotation (NP^S vs NP^VP) or the automatic split-and-merge algorithm, and lexicalised PCFGs that annotate each constituent with its head word, as in the Collins and Charniak parsers (Jurafsky & Martin, 2026, App. E).

#### 6. Neural span-based parsing

Neural CKY trains a classifier to score each labelled span s(i,j,l): words are encoded with a pretrained model such as [[bert|BERT]] plus extra Transformer layers, a span is represented by the difference of its fencepost vectors, and an MLP outputs a score per label. The tree score is the sum of its span scores and a CKY variant finds the best tree without a hand-written grammar; even greedy labelling formed valid trees for 95% of bracketings (Jurafsky & Martin, 2026, ch. 19).

#### 7. Evaluation and heads

PARSEVAL counts a hypothesis constituent as correct if a reference constituent has the same start, end and label, and reports labelled [[classification-metrics|precision]], recall, F1 and crossing brackets; evalb is the standard implementation. Each constituent has a lexical head (N for NP, V for VP), found with hand-written head rules (Collins, Magerman); heads map constituency to dependency structure (Jurafsky & Martin, 2026, ch. 19).

#### Origin and variants

Pāṇini described the grammar of Sanskrit between the 7th and 4th centuries BCE. Immediate-constituent analysis was established in American linguistics by Bloomfield (1933), while European tradition kept relations between words, the basis of dependency grammar. A dynamic programming parser with the roots of CKY was implemented by John Cocke in 1960; Earley (1968) described top-down dynamic programming parsing. PCFGs were worked out by Booth (1969) and Salomaa (1969) (Jurafsky & Martin, 2026, ch. 19, App. E).

### When to use it

- Grammar checking: sentences that cannot be parsed may contain errors (Jurafsky & Martin, 2026, ch. 19).
- As an intermediate representation for formal semantic analysis (Jurafsky & Martin, 2026, ch. 19).
- Text analysis that models the relationship between elements in sentences (Jurafsky & Martin, 2026, ch. 19).

### Strengths and limitations

**Strengths**
- CKY handles structural ambiguity efficiently by storing each constituent once (Jurafsky & Martin, 2026, ch. 19).
- PCFGs with automatic splits and merges reach very high parsing accuracy (Jurafsky & Martin, 2026, App. E).

**Limitations**
- Plain CKY returns all parses without choosing one (Jurafsky & Martin, 2026, ch. 19).
- CNF trees may not match the grammar developers' original grammar and complicate syntax-driven semantics (Jurafsky & Martin, 2026, ch. 19).
- Raw PCFGs have poor independence assumptions and lack lexical conditioning; splitting non-terminals enlarges the grammar and risks overfitting (Jurafsky & Martin, 2026, App. E).

### Comparison

| Approach | Chooses a parse by | Grammar |
|----------|-------------------|---------|
| CKY | Does not choose | Hand-written CFG in CNF |
| PCFG + probabilistic CKY | Highest product of rule probabilities | Treebank grammar |
| Lexicalised PCFG (Collins) | Probabilities conditioned on head words | Treebank grammar with heads |
| Neural span-based CKY | Highest sum of learned span scores | None; learned from spans |

Source: Jurafsky & Martin (2026, ch. 19, App. E).

### In practice

Parsing builds on [[part-of-speech-tagging|Part-of-Speech Tagging]], since the non-terminal for each word is its part of speech (Jurafsky & Martin, 2026, ch. 19). Dependency grammars, the European tradition, are covered in [[dependency-parsing|Dependency Parsing]]; heads link the two representations (Jurafsky & Martin, 2026, ch. 19).

### Key takeaway

Constituency parsing assigns a sentence a tree of nested phrases; CKY finds all parses by dynamic programming, and PCFGs or neural span scorers pick the best one.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Context-Free Grammars and Constituency Parsing.* Speech and Language Processing, 3rd ed. draft, Chapter 19. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/19.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Statistical Constituency Parsing.* Speech and Language Processing, 3rd ed. draft, Appendix E. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/E.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Konstituenz ist die Idee, dass Wortgruppen wie Nominalphrasen sich wie eine Einheit verhalten; kontextfreie Grammatiken (CFGs) modellieren das mit Regeln wie S → NP VP, und syntaktisches Parsing weist einem Satz seinen Parse-Baum zu (Jurafsky & Martin, 2026, Kap. 19). Der CKY-Algorithmus stellt mit dynamischer Programmierung alle Analysen eines mehrdeutigen Satzes kompakt dar, wählt aber keine aus. Disambiguiert wird mit probabilistischen kontextfreien Grammatiken (PCFGs), die den wahrscheinlichsten Baum wählen (Jurafsky & Martin, 2026, Anh. E), oder mit neuronalen spannenbasierten Parsern, die jede Konstituente bewerten. Parser werden mit den PARSEVAL-Metriken evaluiert (Jurafsky & Martin, 2026, Kap. 19).

### Funktionsweise

```text
Satz ─► Grammatik in Chomsky-Normalform (A → B C, A → w)
     ─► CKY-Tabelle: Zelle [i,j] = alle Konstituenten über die Wörter i..j   (bottom-up)
     ─► Disambiguierung:
          PCFG: P(Baum) = Π P(Regel)  →  probabilistisches CKY wählt den wahrscheinlichsten Baum
          neuronal: Score s(i,j,Label) pro Spanne  →  CKY über Spannen-Scores
     ─► PARSEVAL: gelabelte Precision, Recall, F1, Crossing Brackets gegen eine Treebank
```

#### 1. Kontextfreie Grammatiken und Treebanks

Eine CFG besteht aus Regeln über Nichtterminale (NP, VP, PP) und Terminale (Wörter); eine Ableitung vom Startsymbol S ergibt einen Parse-Baum. Die Idee der Konstituentenstruktur geht auf Wilhelm Wundt (1900) zurück und wurde von Chomsky (1956) und unabhängig von Backus (1959) formalisiert, dessen Backus-Naur-Form äquivalent ist. Treebanks wie die Penn Treebank versehen jeden Satz mit einem Baum, meist durch Korrektur von Parser-Ausgaben von Hand; ihre Grammatiken sind sehr flach, mit etwa 4.500 Regeln allein für die Expansion von VPs (Jurafsky & Martin, 2026, Kap. 19).

#### 2. Mehrdeutigkeit

Strukturelle Mehrdeutigkeit ist das größte Problem für Parser. In *I shot an elephant in my pajamas* kann die Präpositionalphrase an die Nominalphrase oder an die Verbalphrase angehängt werden (PP-Attachment-Ambiguität); in *old men and women* kann sich das Adjektiv auf beide Nomen oder eines beziehen (Koordinationsambiguität). Reale Sätze haben viele grammatisch korrekte, aber semantisch unsinnige Analysen (Jurafsky & Martin, 2026, Kap. 19).

#### 3. Der CKY-Algorithmus

CKY (Cocke, Kasami, Younger) verlangt die Chomsky-Normalform, in der jede Regel rechts zwei Nichtterminale oder ein Terminal hat; jede CFG lässt sich in eine schwach äquivalente CNF-Grammatik umwandeln. Für einen Satz mit n Wörtern füllt er das obere Dreieck einer (n+1)×(n+1)-Tabelle; Zelle [i,j] enthält alle Nichtterminale über die Positionen i bis j, gebildet aus Paaren [i,k] und [k,j]. Mit Rückzeigern enthält die Tabelle alle möglichen Analysen, CKY sagt aber nicht, welche richtig ist (Jurafsky & Martin, 2026, Kap. 19).

#### 4. Probabilistische CFGs

Eine PCFG versieht jede Regel A → β mit einer Wahrscheinlichkeit P(β | A); die Wahrscheinlichkeit eines Baums ist das Produkt seiner Regelwahrscheinlichkeiten, und der Parser wählt den wahrscheinlichsten Baum mit probabilistischem CKY (Ney, 1991). Für *Book the dinner flight* erhält die sinnvolle Analyse 2,2×10⁻⁶ und die unsinnige 6,1×10⁻⁷. Regelwahrscheinlichkeiten werden aus einer Treebank gezählt oder aus ungeparstem Text mit dem Inside-Outside-Algorithmus gelernt (Baker, 1979), einer EM-Verallgemeinerung von Forward-Backward. PCFGs können auch als Sprachmodelle dienen, die den gesamten vorherigen Kontext berücksichtigen (Jurafsky & Martin, 2026, Anh. E).

#### 5. Probleme der PCFGs und ihre Lösungen

PCFG-Regeln sind von ihrem Kontext unabhängig, obwohl NPs in Subjektposition zu 91 % Pronomen sind und in Objektposition nur zu 34 %. Sie ignorieren außerdem die Wörter: Eine PCFG bevorzugt immer entweder NP- oder VP-Attachment und kann daher nicht sowohl *dumped sacks into a bin* (VP) als auch *caught tons of herring* (NP) richtig analysieren. Lösungen sind das Aufspalten von Nichtterminalen, etwa durch Parent Annotation (NP^S vs. NP^VP) oder den automatischen Split-and-Merge-Algorithmus, und lexikalisierte PCFGs, die jede Konstituente mit ihrem Kopfwort annotieren, wie die Parser von Collins und Charniak (Jurafsky & Martin, 2026, Anh. E).

#### 6. Neuronales spannenbasiertes Parsing

Neuronales CKY trainiert einen Klassifikator, der jede gelabelte Spanne s(i,j,l) bewertet: Wörter werden mit einem vortrainierten Modell wie [[bert|BERT]] plus zusätzlichen Transformer-Schichten kodiert, eine Spanne wird durch die Differenz ihrer Grenzvektoren dargestellt, und ein MLP gibt einen Score pro Label aus. Der Baum-Score ist die Summe seiner Spannen-Scores, und eine CKY-Variante findet den besten Baum ohne handgeschriebene Grammatik; selbst gieriges Labeln ergab bei 95 % der Klammerungen gültige Bäume (Jurafsky & Martin, 2026, Kap. 19).

#### 7. Evaluation und Köpfe

PARSEVAL zählt eine Konstituente der Hypothese als korrekt, wenn eine Referenzkonstituente denselben Anfang, dasselbe Ende und dasselbe Label hat, und berichtet gelabelte [[classification-metrics|Precision]], Recall, F1 und Crossing Brackets; evalb ist die Standardimplementierung. Jede Konstituente hat einen lexikalischen Kopf (N für NP, V für VP), der mit handgeschriebenen Kopfregeln (Collins, Magerman) bestimmt wird; Köpfe übersetzen Konstituenten- in Dependenzstruktur (Jurafsky & Martin, 2026, Kap. 19).

#### Herkunft und Varianten

Pāṇini beschrieb die Grammatik des Sanskrit zwischen dem 7. und 4. Jahrhundert v. Chr. Die Analyse unmittelbarer Konstituenten etablierte sich in der amerikanischen Linguistik mit Bloomfield (1933), während die europäische Tradition Beziehungen zwischen Wörtern beibehielt, die Grundlage der Dependenzgrammatik. Einen Parser mit dynamischer Programmierung und den Wurzeln von CKY implementierte John Cocke 1960; Earley (1968) beschrieb Top-down-Parsing mit dynamischer Programmierung. PCFGs wurden von Booth (1969) und Salomaa (1969) ausgearbeitet (Jurafsky & Martin, 2026, Kap. 19, Anh. E).

### Wann einsetzen

- Grammatikprüfung: Sätze, die sich nicht parsen lassen, können Fehler enthalten (Jurafsky & Martin, 2026, Kap. 19).
- Als Zwischenrepräsentation für formale semantische Analyse (Jurafsky & Martin, 2026, Kap. 19).
- Textanalyse, die die Beziehungen zwischen Satzelementen modelliert (Jurafsky & Martin, 2026, Kap. 19).

### Stärken und Grenzen

**Stärken**
- CKY behandelt strukturelle Mehrdeutigkeit effizient, indem jede Konstituente nur einmal gespeichert wird (Jurafsky & Martin, 2026, Kap. 19).
- PCFGs mit automatischem Aufspalten und Zusammenführen erreichen sehr hohe Parsing-Genauigkeit (Jurafsky & Martin, 2026, Anh. E).

**Grenzen**
- Reines CKY liefert alle Analysen, ohne eine auszuwählen (Jurafsky & Martin, 2026, Kap. 19).
- CNF-Bäume passen nicht unbedingt zur ursprünglichen Grammatik der Entwickler und erschweren syntaxgetriebene Semantik (Jurafsky & Martin, 2026, Kap. 19).
- Einfache PCFGs haben schlechte Unabhängigkeitsannahmen und keine lexikalische Konditionierung; das Aufspalten von Nichtterminalen vergrößert die Grammatik und birgt Overfitting (Jurafsky & Martin, 2026, Anh. E).

### Vergleich

| Ansatz | Wählt eine Analyse über | Grammatik |
|--------|------------------------|-----------|
| CKY | Wählt nicht | Handgeschriebene CFG in CNF |
| PCFG + probabilistisches CKY | Höchstes Produkt der Regelwahrscheinlichkeiten | Treebank-Grammatik |
| Lexikalisierte PCFG (Collins) | Wahrscheinlichkeiten abhängig von Kopfwörtern | Treebank-Grammatik mit Köpfen |
| Neuronales spannenbasiertes CKY | Höchste Summe gelernter Spannen-Scores | Keine; aus Spannen gelernt |

Quelle: Jurafsky & Martin (2026, Kap. 19, Anh. E).

### In der Praxis

Parsing baut auf dem [[part-of-speech-tagging|Part-of-Speech-Tagging]] auf, da das Nichtterminal jedes Wortes sein Part-of-Speech-Tag ist (Jurafsky & Martin, 2026, Kap. 19). Dependenzgrammatiken, die europäische Tradition, behandelt [[dependency-parsing|Dependenzparsing]]; Köpfe verbinden die beiden Darstellungen (Jurafsky & Martin, 2026, Kap. 19).

### Merksatz

Konstituentenparsing weist einem Satz einen Baum verschachtelter Phrasen zu; CKY findet alle Analysen per dynamischer Programmierung, und PCFGs oder neuronale Spannenbewerter wählen die beste aus.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Context-Free Grammars and Constituency Parsing.* Speech and Language Processing, 3rd ed. draft, Chapter 19. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/19.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Statistical Constituency Parsing.* Speech and Language Processing, 3rd ed. draft, Appendix E. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/E.pdf)
