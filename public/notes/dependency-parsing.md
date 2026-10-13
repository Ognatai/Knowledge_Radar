---
title_en: Dependency Parsing
title_de: Dependenzparsing
entity_type: Method
aliases:
- Dependency parser
- Dependency grammar
- Transition-based parsing
- Graph-based dependency parsing
- Universal Dependencies
sources:
- https://web.stanford.edu/~jurafsky/slp3/20.pdf
- https://edoc.ub.uni-muenchen.de/36297/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Dependency grammars describe the syntax of a sentence solely as directed, labelled relations between words, from heads to their dependents, such as *prefer* →nsubj→ *I* (Jurafsky & Martin, 2026). Head-dependent relations are a good proxy for the semantic relations between predicates and their arguments and cope well with free word order, which is why dependency grammars are currently more common in NLP than constituency grammars. Two families of parsers exist: fast, greedy transition-based parsers with a stack and a learned oracle, and more accurate graph-based parsers that find the maximum spanning tree over scored edges. Parsers are evaluated with labelled and unlabelled attachment scores (Jurafsky & Martin, 2026).

### How it works

```text
I  prefer  the  morning  flight  through  Denver
   root ─► prefer ─nsubj─► I
           prefer ─obj──► flight ─det─► the, ─compound─► morning, ─nmod─► Denver ─case─► through

transition-based:  stack + buffer + oracle (SHIFT, LEFTARC, RIGHTARC)  → O(n), greedy, projective
graph-based:       score every head→dependent edge, maximum spanning tree (Chu-Liu-Edmonds) → O(n³)
evaluation:        LAS (head + label correct), UAS (head correct)
```

#### 1. Dependency relations and trees

Each relation links a head, the central organising word, to a dependent with a grammatical function such as subject (NSUBJ), direct object (OBJ), determiner (DET) or case marker (CASE). Universal Dependencies (UD) defines 37 relations and has almost 200 treebanks in more than 100 languages. A dependency tree has a single root without incoming arcs, every other word has exactly one head, and there is a unique path from the root to every word. A tree is projective if it can be drawn without crossing arcs; non-projective trees occur particularly in languages with flexible word order (Jurafsky & Martin, 2026).

#### 2. Transition-based parsing

Based on shift-reduce parsing for programming languages, a transition-based parser keeps a stack, a buffer of words and a set of relations. In the arc-standard system, an oracle chooses at each step between SHIFT (move the next word onto the stack), LEFTARC and RIGHTARC (attach one of the top two stack words to the other and pop the dependent). The parser makes a single left-to-right pass, so it is linear in sentence length, but it is greedy and cannot undo decisions (Jurafsky & Martin, 2026).

#### 3. Training the oracle

Treebanks contain trees, not transitions, so training data is created by simulating the parser on each reference tree: choose LEFTARC if it produces a correct relation, RIGHTARC if it does and the word on top already has all its dependents, otherwise SHIFT. The oracle can be a feature-based classifier (word forms, parts of speech and relations at the top of the stack and the front of the buffer) or a neural classifier that concatenates the encodings of the top two stack words and the first buffer word (Jurafsky & Martin, 2026).

#### 4. Variants: arc-eager and beam search

The arc-eager system attaches words to their heads as early as possible and adds a REDUCE operator; other transition systems assign POS tags, produce non-projective trees or parse code-mixed text. Beam search keeps several configurations, scored by the sum of their transition scores, instead of one greedy choice (Jurafsky & Martin, 2026).

#### 5. Graph-based parsing

Graph-based parsers score entire trees as the sum of their edge scores (edge-factored) and search all possible trees. They build a fully connected graph with an edge for every possible head-dependent pair; the best parse is the maximum spanning tree from the root. The Chu-Liu-Edmonds algorithm picks the best incoming edge for each word, and if this creates a cycle, rescales the weights, contracts the cycle into one node and recurses, in O(n³) for a sentence of n words. Edge scores come from features with perceptron-style learning or, in state-of-the-art parsers, from the biaffine scorer of Dozat and Manning: separate feedforward networks produce head and dependent representations, a biaffine function scores each pair, and a second classifier assigns labels (Jurafsky & Martin, 2026).

#### 6. Evaluation

Exact sentence match is too pessimistic. The labelled attachment score (LAS) is the percentage of words with the correct head and relation, the unlabelled attachment score (UAS) ignores the relation, and [[classification-metrics|precision]] and recall can be computed per relation type such as NSUBJ (Jurafsky & Martin, 2026).

#### Origin and variants

Dependency grammar is much older than constituency grammar and goes back to Pāṇini and ancient Greek traditions; contemporary theories build on Tesnière (1959). Computational dependency parsing began with [[machine-translation|machine translation]] at the RAND Corporation (David Hays). Nivre (2003) defined the modern transition-based approach, Chen and Manning (2014) pioneered the neural one, and McDonald et al. (2005) introduced graph-based maximum spanning tree parsing (Jurafsky & Martin, 2026).

### When to use it

- Information extraction, semantic parsing and question answering, which benefit directly from head-dependent relations (Jurafsky & Martin, 2026).
- Languages with free word order such as Czech, where one relation type can cover an adverbial in any position (Jurafsky & Martin, 2026).
- Multilingual work, using the UD treebanks (Jurafsky & Martin, 2026).

### Strengths and limitations

**Strengths**
- Arguments are linked directly to their predicate, unlike the more distant connection in phrase-structure trees (Jurafsky & Martin, 2026).
- Transition-based parsing is linear-time and allows swapping transition systems without changing the algorithm (Jurafsky & Martin, 2026).
- Graph-based parsers are more accurate, especially on long sentences, and can produce non-projective trees (McDonald & Nivre, 2011, in Jurafsky & Martin, 2026).

**Limitations**
- Transition-based parsers can only produce projective trees and struggle when heads are far from their dependents (Jurafsky & Martin, 2026).
- English dependency treebanks derived automatically from phrase-structure treebanks are always projective and therefore wrong for non-projective sentences (Jurafsky & Martin, 2026).

### Comparison

| | Transition-based | Graph-based |
|-|------------------|-------------|
| Search | Greedy (or beam) over transitions | Maximum spanning tree over all edges |
| Complexity | Linear | O(n³) with Chu-Liu-Edmonds |
| Non-projective trees | No (basic system) | Yes |
| Long-distance heads | Weaker | Stronger |

Source: Jurafsky & Martin (2026).

### In practice

Dependency treebanks are created by annotators directly, by correcting parser output, or by converting constituency treebanks with head rules ([[constituency-parsing|Constituency Parsing]]) (Jurafsky & Martin, 2026). Dependency parses feed [[information-extraction|Information Extraction]] (Jurafsky & Martin, 2026). An actor-centred pipeline for detecting gender discrimination in news uses spaCy's tokenisation, [[part-of-speech-tagging|POS tagging]], dependency parsing and named entity recognition to find the actors, and tracks whether they appear in subject or object position, because subjects typically act and objects are acted upon (Urchs, 2025).

### Key takeaway

Dependency parsing links each word to its head with a grammatical relation; transition-based parsers are fast and greedy, graph-based parsers find the maximum spanning tree and are more accurate.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Dependency Parsing.* Speech and Language Processing, 3rd ed. draft, Chapter 20. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/20.pdf)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Dependenzgrammatiken beschreiben die Syntax eines Satzes allein als gerichtete, gelabelte Relationen zwischen Wörtern, vom Kopf zu seinen Dependenten, etwa *prefer* →nsubj→ *I* (Jurafsky & Martin, 2026). Kopf-Dependent-Relationen sind ein guter Stellvertreter für die semantischen Beziehungen zwischen Prädikaten und ihren Argumenten und kommen mit freier Wortstellung gut zurecht, weshalb Dependenzgrammatiken im NLP derzeit verbreiteter sind als Konstituentengrammatiken. Es gibt zwei Familien von Parsern: schnelle, gierige transitionsbasierte Parser mit Stack und gelerntem Orakel und genauere graphbasierte Parser, die den maximalen Spannbaum über bewerteten Kanten finden. Evaluiert wird mit gelabelten und ungelabelten Attachment Scores (Jurafsky & Martin, 2026).

### Funktionsweise

```text
I  prefer  the  morning  flight  through  Denver
   root ─► prefer ─nsubj─► I
           prefer ─obj──► flight ─det─► the, ─compound─► morning, ─nmod─► Denver ─case─► through

transitionsbasiert:  Stack + Puffer + Orakel (SHIFT, LEFTARC, RIGHTARC)  → O(n), gierig, projektiv
graphbasiert:        jede Kante Kopf→Dependent bewerten, maximaler Spannbaum (Chu-Liu-Edmonds) → O(n³)
Evaluation:          LAS (Kopf + Label korrekt), UAS (Kopf korrekt)
```

#### 1. Dependenzrelationen und -bäume

Jede Relation verbindet einen Kopf, das zentrale ordnende Wort, mit einem Dependenten in einer grammatischen Funktion wie Subjekt (NSUBJ), direktes Objekt (OBJ), Determinierer (DET) oder Kasusmarker (CASE). Universal Dependencies (UD) definiert 37 Relationen und umfasst fast 200 Treebanks in über 100 Sprachen. Ein Dependenzbaum hat eine einzige Wurzel ohne eingehende Kanten, jedes andere Wort hat genau einen Kopf, und von der Wurzel führt ein eindeutiger Pfad zu jedem Wort. Ein Baum ist projektiv, wenn er sich ohne sich kreuzende Kanten zeichnen lässt; nicht-projektive Bäume treten besonders in Sprachen mit freier Wortstellung auf (Jurafsky & Martin, 2026).

#### 2. Transitionsbasiertes Parsing

Aufbauend auf dem Shift-Reduce-Parsing für Programmiersprachen führt ein transitionsbasierter Parser einen Stack, einen Puffer von Wörtern und eine Menge von Relationen. Im Arc-Standard-System wählt ein Orakel in jedem Schritt zwischen SHIFT (nächstes Wort auf den Stack), LEFTARC und RIGHTARC (eines der beiden obersten Stack-Wörter an das andere hängen und den Dependenten entfernen). Der Parser macht einen einzigen Durchlauf von links nach rechts und ist daher linear in der Satzlänge, aber gierig und kann Entscheidungen nicht zurücknehmen (Jurafsky & Martin, 2026).

#### 3. Das Orakel trainieren

Treebanks enthalten Bäume, keine Transitionen, deshalb entstehen Trainingsdaten, indem der Parser auf jedem Referenzbaum simuliert wird: LEFTARC wählen, wenn es eine korrekte Relation erzeugt, RIGHTARC, wenn es das tut und das oberste Wort schon alle Dependenten hat, sonst SHIFT. Das Orakel kann ein merkmalsbasierter Klassifikator sein (Wortformen, Wortarten und Relationen oben auf dem Stack und vorn im Puffer) oder ein neuronaler Klassifikator, der die Kodierungen der beiden obersten Stack-Wörter und des ersten Pufferworts verkettet (Jurafsky & Martin, 2026).

#### 4. Varianten: Arc-Eager und Beam Search

Das Arc-Eager-System hängt Wörter so früh wie möglich an ihre Köpfe und ergänzt einen REDUCE-Operator; andere Transitionssysteme vergeben Wortarten, erzeugen nicht-projektive Bäume oder parsen Text mit Sprachmischung. Beam Search behält mehrere Konfigurationen, bewertet über die Summe ihrer Transitions-Scores, statt einer einzigen gierigen Wahl (Jurafsky & Martin, 2026).

#### 5. Graphbasiertes Parsing

Graphbasierte Parser bewerten ganze Bäume als Summe ihrer Kanten-Scores (edge-factored) und durchsuchen alle möglichen Bäume. Sie bauen einen vollständig verbundenen Graphen mit einer Kante für jedes mögliche Kopf-Dependent-Paar; die beste Analyse ist der maximale Spannbaum ab der Wurzel. Der Chu-Liu-Edmonds-Algorithmus wählt für jedes Wort die beste eingehende Kante, und wenn dabei ein Zyklus entsteht, skaliert er die Gewichte um, fasst den Zyklus zu einem Knoten zusammen und rekursiert, in O(n³) für einen Satz mit n Wörtern. Kanten-Scores stammen aus Merkmalen mit Perzeptron-Lernen oder, bei aktuellen Parsern, aus dem biaffinen Scorer von Dozat und Manning: Getrennte Feedforward-Netze erzeugen Kopf- und Dependent-Repräsentationen, eine biaffine Funktion bewertet jedes Paar, und ein zweiter Klassifikator vergibt die Labels (Jurafsky & Martin, 2026).

#### 6. Evaluation

Exakte Übereinstimmung ganzer Sätze ist zu pessimistisch. Der Labeled Attachment Score (LAS) ist der Anteil der Wörter mit korrektem Kopf und korrekter Relation, der Unlabeled Attachment Score (UAS) ignoriert die Relation, und [[classification-metrics|Precision]] und Recall lassen sich pro Relationstyp wie NSUBJ berechnen (Jurafsky & Martin, 2026).

#### Herkunft und Varianten

Die Dependenzgrammatik ist viel älter als die Konstituentengrammatik und geht auf Pāṇini und antike griechische Traditionen zurück; heutige Theorien bauen auf Tesnière (1959) auf. Computergestütztes Dependenzparsing begann mit maschineller Übersetzung bei der RAND Corporation (David Hays). Nivre (2003) definierte den modernen transitionsbasierten Ansatz, Chen und Manning (2014) begründeten den neuronalen, und McDonald et al. (2005) führten graphbasiertes Parsing mit maximalen Spannbäumen ein (Jurafsky & Martin, 2026).

### Wann einsetzen

- Informationsextraktion, semantisches Parsing und Question Answering, die direkt von Kopf-Dependent-Relationen profitieren (Jurafsky & Martin, 2026).
- Sprachen mit freier Wortstellung wie Tschechisch, in denen ein Relationstyp ein Adverbial an jeder Position abdecken kann (Jurafsky & Martin, 2026).
- Mehrsprachige Arbeit mit den UD-Treebanks (Jurafsky & Martin, 2026).

### Stärken und Grenzen

**Stärken**
- Argumente sind direkt mit ihrem Prädikat verbunden, anders als die entferntere Verbindung in Phrasenstrukturbäumen (Jurafsky & Martin, 2026).
- Transitionsbasiertes Parsing läuft in linearer Zeit und erlaubt den Austausch des Transitionssystems ohne Änderung am Algorithmus (Jurafsky & Martin, 2026).
- Graphbasierte Parser sind genauer, besonders bei langen Sätzen, und können nicht-projektive Bäume erzeugen (McDonald & Nivre, 2011, in Jurafsky & Martin, 2026).

**Grenzen**
- Transitionsbasierte Parser können nur projektive Bäume erzeugen und haben Probleme, wenn Köpfe weit von ihren Dependenten entfernt sind (Jurafsky & Martin, 2026).
- Englische Dependenz-Treebanks, die automatisch aus Phrasenstruktur-Treebanks abgeleitet wurden, sind immer projektiv und damit für nicht-projektive Sätze falsch (Jurafsky & Martin, 2026).

### Vergleich

| | Transitionsbasiert | Graphbasiert |
|-|--------------------|--------------|
| Suche | Gierig (oder Beam) über Transitionen | Maximaler Spannbaum über alle Kanten |
| Komplexität | Linear | O(n³) mit Chu-Liu-Edmonds |
| Nicht-projektive Bäume | Nein (Grundsystem) | Ja |
| Weit entfernte Köpfe | Schwächer | Stärker |

Quelle: Jurafsky & Martin (2026).

### In der Praxis

Dependenz-Treebanks entstehen direkt durch Annotierende, durch Korrektur von Parser-Ausgaben oder durch Umwandlung von Konstituenten-Treebanks mit Kopfregeln ([[constituency-parsing|Konstituentenparsing]]) (Jurafsky & Martin, 2026). Dependenzanalysen fließen in die [[information-extraction|Informationsextraktion]] ein (Jurafsky & Martin, 2026). Eine akteurszentrierte Pipeline zur Erkennung von Gender-Diskriminierung in Nachrichten nutzt [[tokenization|Tokenisierung]], [[part-of-speech-tagging|Wortart-Tagging]], Dependenzparsing und Named Entity Recognition von spaCy, um die Akteure zu finden, und verfolgt, ob sie in Subjekt- oder Objektposition stehen, weil Subjekte typischerweise handeln und Objekte Handlungen erfahren (Urchs, 2025).

### Merksatz

Dependenzparsing verbindet jedes Wort über eine grammatische Relation mit seinem Kopf; transitionsbasierte Parser sind schnell und gierig, graphbasierte Parser finden den maximalen Spannbaum und sind genauer.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Dependency Parsing.* Speech and Language Processing, 3rd ed. draft, Chapter 20. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/20.pdf)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
