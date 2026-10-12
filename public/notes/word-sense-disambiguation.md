---
title_en: Word Sense Disambiguation and WordNet
title_de: Wortsinn-Disambiguierung und WordNet
entity_type: Method
aliases:
- Word sense disambiguation
- WSD
- WordNet
- Word sense
- Lesk algorithm
- Word sense induction
sources:
- https://web.stanford.edu/~jurafsky/slp3/I.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Words are ambiguous: *bank* can be a financial institution or a sloping mound; a word sense is a discrete representation of one aspect of a word's meaning (Jurafsky & Martin, 2026). WordNet is a large lexical database that groups senses into synsets and links them by relations such as hypernymy (IS-A), meronymy (part-whole) and antonymy. Word sense disambiguation (WSD) chooses the sense a word has in context; the best-performing method is a 1-nearest-neighbour classifier over contextual embeddings such as BERT, with the most frequent sense and the Lesk algorithm as baselines (Jurafsky & Martin, 2026).

### How it works

```text
training (SemCor):  every sense-tagged token ─► contextual embedding (e.g. BERT, last 4 layers summed)
                    sense embedding v_s = mean of its tokens' embeddings
                    unseen senses ─► average over synset, hypernym or supersense in WordNet
test:               target word in context ─► embedding t ─► argmax_s cosine(t, v_s)
baselines:          most frequent sense (WordNet's first sense) · Lesk (gloss overlap)
```

#### 1. Word senses and their relations

A sense can be defined by a gloss, a dictionary definition written for people, or by its relations to other senses. Two uses are likely different senses if they have different truth conditions or syntax; a zeugma such as *?Does Air France serve breakfast and Philadelphia?* signals two senses of *serve*. Synonymy holds between senses, not words: *big* and *large* are synonyms in *How big is that plane?* but not in *big sister*. Antonyms are opposite on one scale but share almost everything else, which makes them hard to separate from synonyms. Hyponymy (*car* is a kind of *vehicle*) is usually transitive; meronymy is the part-whole relation; structured polysemy such as metonymy relates senses systematically (the building versus the organisation called *bank*) (Jurafsky & Martin, 2026).

#### 2. WordNet

English WordNet has separate databases for nouns, verbs, and adjectives and adverbs; version 3.0 has 117,798 nouns, 11,529 verbs, 22,479 adjectives and 4,481 adverbs, with an average of 1.23 senses per noun and 2.16 per verb. A synset is a set of near-synonymous senses with a shared gloss and acts as a concept; most relations hold between synsets. Each synset carries one of 26 noun or 15 verb lexicographic categories, called supersenses (such as ANIMAL, ARTIFACT, FOOD), which serve as coarse senses. Relations include hypernym and hyponym, instance relations (*Austen* → *author*), part meronym and holonym, antonym, and for verbs troponym (*walk* → *stroll*) and entailment (*snore* → *sleep*) (Jurafsky & Martin, 2026).

#### 3. The WSD task

The sense inventory depends on the task: WordNet senses, supersenses, the translations of a word in another language, or thesaurus entries such as MeSH. Lexical sample tasks disambiguate a few target words; all-words tasks disambiguate every content word, like [[part-of-speech-tagging|POS tagging]] with a much larger tag set. Supervised systems train on semantic concordances such as SemCor (226,036 words of the Brown corpus tagged with WordNet senses) and are evaluated with F1. Choosing the most frequent sense, WordNet's first sense, is a surprisingly strong baseline; the one-sense-per-discourse heuristic holds best for coarse, unrelated senses (Jurafsky & Martin, 2026).

#### 4. Contextual embeddings

Each sense-tagged token in SemCor is encoded with a contextual model, and the embeddings of a sense's tokens are averaged into a sense embedding; at test time the sense with the highest cosine to the target token's embedding wins. For senses missing from SemCor, Loureiro and Jorge (2019) impute embeddings bottom-up through WordNet: from the synset, then the hypernym, then the supersense, which guarantees a representation for every sense (Jurafsky & Martin, 2026).

#### 5. Feature-based and knowledge-based WSD

Feature-based classifiers such as IMS use an SVM with POS tags and collocation features in a window of 3 words and a distance-weighted average of embeddings, and work almost as well. Knowledge-based methods need no labelled data: the Lesk algorithm chooses the sense whose gloss and examples share the most words with the context (for *The bank can guarantee deposits …*, *deposits* and *mortgage* overlap with sense 1); weighting by IDF or comparing embeddings improves it (Jurafsky & Martin, 2026).

#### 6. Related tasks

Word-in-context (WiC) asks whether a word has the same sense in two sentences; a baseline thresholds the cosine of the two contextual embeddings. Wikipedia links serve as sense annotations, and mapping them to WordNet produced BabelNet. Thesauri also improve embeddings: retrofitting and counterfitting push synonyms together and antonyms apart. Word sense induction clusters context vectors of a word's tokens into unnamed senses, without human-defined inventories (Jurafsky & Martin, 2026).

#### Origin and variants

Weaver (1949) observed that a word's meaning can be decided if one sees enough words on either side. Kelly and Stone (1975) hand-crafted disambiguation rules for 1,790 words; Lesk (1986) first used a machine-readable dictionary; Yarowsky (1995) used bootstrapping; Fellbaum (1998) collects early work on WordNet (Jurafsky & Martin, 2026).

### When to use it

- Question answering, for example knowing which *bat* a question about bat care means (Jurafsky & Martin, 2026).
- [[machine-translation|Machine translation]], since senses often have different translations (*murciélago* versus *bate*) (Jurafsky & Martin, 2026).
- Evaluating how language models represent word senses (Jurafsky & Martin, 2026).
- Distinguishing antonyms that embeddings confuse, such as turning music up rather than down (Jurafsky & Martin, 2026).

### Strengths and limitations

**Strengths**
- WordNet relations support tasks such as textual entailment and question answering (*leukemia* is a type of *cancer*) (Jurafsky & Martin, 2026).
- Knowledge-based methods work in languages or domains with dictionaries but no sense-labelled corpora (Jurafsky & Martin, 2026).

**Limitations**
- Sense-labelled corpora are expensive to build, and SemCor covers only a small fraction of WordNet's words (Jurafsky & Martin, 2026).
- Dictionary senses are very fine-grained, so tasks often cluster them into coarser senses (Jurafsky & Martin, 2026).
- Glosses are circular and not a formal meaning representation; for word sense induction no evaluation metric has become standard (Jurafsky & Martin, 2026).

### Comparison

| Method | Needs | Notes |
|--------|-------|-------|
| Most frequent sense | Sense frequencies | Strong baseline; WordNet's first sense |
| Lesk | Glosses and examples | Knowledge-based; no labelled data |
| Feature-based (IMS) | Labelled data | SVM; almost as good as contextual |
| Contextual 1-NN | Labelled data + encoder | Best performing |
| Word sense induction | Unlabelled text | Clusters; no named senses |

Source: Jurafsky & Martin (2026).

### In practice

Static [[embeddings|Embeddings]] do not divide into discrete senses, while contextual models such as [[bert|BERT]] represent a word in its context and underlie modern WSD (Jurafsky & Martin, 2026). The contextual method is a nearest-neighbour classifier ([[k-nearest-neighbors|k-Nearest Neighbors]]), feature-based WSD uses collocation features ([[collocations|Collocations]]), and word sense induction relies on [[clustering|Clustering]] (Jurafsky & Martin, 2026).

### Key takeaway

WordNet lists word senses as synsets connected by relations such as IS-A and part-whole; WSD picks a word's sense in context, best with nearest-neighbour search over contextual sense embeddings.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Word Senses and WordNet.* Speech and Language Processing, 3rd ed. draft, Appendix I. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/I.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Wörter sind mehrdeutig: *bank* kann ein Geldinstitut oder eine Böschung sein; ein Wortsinn ist eine diskrete Darstellung eines Aspekts der Bedeutung eines Wortes (Jurafsky & Martin, 2026). WordNet ist eine große lexikalische Datenbank, die Wortsinne zu Synsets bündelt und über Relationen wie Hyperonymie (IS-A), Meronymie (Teil-Ganzes) und Antonymie verbindet. Wortsinn-Disambiguierung (WSD) wählt den Sinn, den ein Wort im Kontext hat; das beste Verfahren ist ein 1-Nächster-Nachbar-Klassifikator über kontextuellen Embeddings wie BERT, mit dem häufigsten Sinn und dem Lesk-Algorithmus als Baselines (Jurafsky & Martin, 2026).

### Funktionsweise

```text
Training (SemCor):  jedes sinnannotierte Token ─► kontextuelles Embedding (z. B. BERT, letzte 4 Schichten summiert)
                    Sinn-Embedding v_s = Mittel der Embeddings seiner Token
                    ungesehene Sinne ─► Mittel über Synset, Hyperonym oder Supersense in WordNet
Test:               Zielwort im Kontext ─► Embedding t ─► argmax_s Kosinus(t, v_s)
Baselines:          häufigster Sinn (erster Sinn in WordNet) · Lesk (Überlappung mit der Glosse)
```

#### 1. Wortsinne und ihre Relationen

Ein Sinn lässt sich über eine Glosse, eine für Menschen geschriebene Wörterbuchdefinition, oder über seine Relationen zu anderen Sinnen bestimmen. Zwei Verwendungen sind wahrscheinlich verschiedene Sinne, wenn sie unterschiedliche Wahrheitsbedingungen oder Syntax haben; ein Zeugma wie *?Does Air France serve breakfast and Philadelphia?* zeigt zwei Sinne von *serve* an. Synonymie besteht zwischen Sinnen, nicht Wörtern: *big* und *large* sind in *How big is that plane?* synonym, nicht aber in *big sister*. Antonyme liegen an entgegengesetzten Enden einer Skala, teilen aber fast alles andere, was sie schwer von Synonymen unterscheidbar macht. Hyponymie (*car* ist eine Art *vehicle*) ist meist transitiv; Meronymie ist die Teil-Ganzes-Relation; strukturierte Polysemie wie Metonymie verbindet Sinne systematisch (das Gebäude gegenüber der Organisation namens *bank*) (Jurafsky & Martin, 2026).

#### 2. WordNet

Das englische WordNet hat getrennte Datenbanken für Nomen, Verben sowie Adjektive und Adverbien; Version 3.0 umfasst 117.798 Nomen, 11.529 Verben, 22.479 Adjektive und 4.481 Adverbien, mit durchschnittlich 1,23 Sinnen pro Nomen und 2,16 pro Verb. Ein Synset ist eine Menge nahezu synonymer Sinne mit gemeinsamer Glosse und steht für ein Konzept; die meisten Relationen bestehen zwischen Synsets. Jedes Synset trägt eine von 26 lexikographischen Kategorien für Nomen oder 15 für Verben, Supersenses genannt (etwa ANIMAL, ARTIFACT, FOOD), die als grobe Sinne dienen. Relationen sind Hyperonym und Hyponym, Instanzrelationen (*Austen* → *author*), Teil-Meronym und -Holonym, Antonym und bei Verben Troponym (*walk* → *stroll*) und Implikation (*snore* → *sleep*) (Jurafsky & Martin, 2026).

#### 3. Die WSD-Aufgabe

Das Sinninventar hängt von der Aufgabe ab: WordNet-Sinne, Supersenses, die Übersetzungen eines Wortes in eine andere Sprache oder Thesauruseinträge wie MeSH. Lexical-Sample-Aufgaben disambiguieren wenige Zielwörter; All-Words-Aufgaben jedes Inhaltswort, ähnlich dem [[part-of-speech-tagging|Wortart-Tagging]] mit einem viel größeren Tagset. Überwachte Systeme trainieren auf semantischen Konkordanzen wie SemCor (226.036 Wörter des Brown-Korpus, mit WordNet-Sinnen annotiert) und werden mit F1 evaluiert. Den häufigsten Sinn, also den ersten in WordNet, zu wählen, ist eine überraschend starke Baseline; die Heuristik „ein Sinn pro Diskurs“ gilt am besten für grobe, unverwandte Sinne (Jurafsky & Martin, 2026).

#### 4. Kontextuelle Embeddings

Jedes sinnannotierte Token in SemCor wird mit einem kontextuellen Modell kodiert, und die Embeddings der Token eines Sinns werden zu einem Sinn-Embedding gemittelt; beim Test gewinnt der Sinn mit dem höchsten Kosinus zum Embedding des Zieltokens. Für Sinne, die in SemCor fehlen, berechnen Loureiro und Jorge (2019) Embeddings von unten nach oben durch WordNet: aus dem Synset, dann dem Hyperonym, dann dem Supersense, was für jeden Sinn eine Darstellung garantiert (Jurafsky & Martin, 2026).

#### 5. Merkmals- und wissensbasierte WSD

Merkmalsbasierte Klassifikatoren wie IMS nutzen eine SVM mit Wortarten und Kollokationsmerkmalen in einem Fenster von 3 Wörtern sowie einem nach Abstand gewichteten Mittel der Embeddings und funktionieren fast genauso gut. Wissensbasierte Verfahren brauchen keine gelabelten Daten: Der Lesk-Algorithmus wählt den Sinn, dessen Glosse und Beispiele die meisten Wörter mit dem Kontext teilen (bei *The bank can guarantee deposits …* überlappen *deposits* und *mortgage* mit Sinn 1); Gewichtung mit IDF oder der Vergleich von Embeddings verbessert ihn (Jurafsky & Martin, 2026).

#### 6. Verwandte Aufgaben

Word-in-Context (WiC) fragt, ob ein Wort in zwei Sätzen denselben Sinn hat; eine Baseline setzt einen Schwellenwert auf den Kosinus der beiden kontextuellen Embeddings. Wikipedia-Links dienen als Sinnannotationen, und ihre Zuordnung zu WordNet ergab BabelNet. Thesauri verbessern auch Embeddings: Retrofitting und Counterfitting ziehen Synonyme zusammen und schieben Antonyme auseinander. Word Sense Induction clustert Kontextvektoren der Token eines Wortes zu unbenannten Sinnen, ohne von Menschen definierte Inventare (Jurafsky & Martin, 2026).

#### Herkunft und Varianten

Weaver (1949) bemerkte, dass sich die Bedeutung eines Wortes bestimmen lässt, wenn man genug Wörter auf beiden Seiten sieht. Kelly und Stone (1975) erstellten von Hand Disambiguierungsregeln für 1.790 Wörter; Lesk (1986) nutzte als Erster ein maschinenlesbares Wörterbuch; Yarowsky (1995) setzte Bootstrapping ein; Fellbaum (1998) sammelt frühe Arbeiten zu WordNet (Jurafsky & Martin, 2026).

### Wann einsetzen

- Question Answering, etwa um zu wissen, welche *bat* eine Frage zur Pflege meint (Jurafsky & Martin, 2026).
- [[machine-translation|Maschinelle Übersetzung]], da Sinne oft unterschiedliche Übersetzungen haben (*murciélago* gegenüber *bate*) (Jurafsky & Martin, 2026).
- Evaluieren, wie Sprachmodelle Wortsinne repräsentieren (Jurafsky & Martin, 2026).
- Antonyme unterscheiden, die Embeddings verwechseln, etwa Musik lauter statt leiser stellen (Jurafsky & Martin, 2026).

### Stärken und Grenzen

**Stärken**
- WordNet-Relationen unterstützen Aufgaben wie Textual Entailment und Question Answering (*leukemia* ist eine Art *cancer*) (Jurafsky & Martin, 2026).
- Wissensbasierte Verfahren funktionieren in Sprachen oder Domänen mit Wörterbüchern, aber ohne sinnannotierte Korpora (Jurafsky & Martin, 2026).

**Grenzen**
- Sinnannotierte Korpora sind teuer, und SemCor deckt nur einen kleinen Teil der Wörter in WordNet ab (Jurafsky & Martin, 2026).
- Wörterbuchsinne sind sehr feinkörnig, daher werden sie für Aufgaben oft zu groberen Sinnen geclustert (Jurafsky & Martin, 2026).
- Glossen sind zirkulär und keine formale Bedeutungsdarstellung; für Word Sense Induction hat sich keine Evaluationsmetrik als Standard durchgesetzt (Jurafsky & Martin, 2026).

### Vergleich

| Verfahren | Braucht | Hinweise |
|-----------|---------|----------|
| Häufigster Sinn | Sinnhäufigkeiten | Starke Baseline; erster Sinn in WordNet |
| Lesk | Glossen und Beispiele | Wissensbasiert; keine gelabelten Daten |
| Merkmalsbasiert (IMS) | Gelabelte Daten | SVM; fast so gut wie kontextuell |
| Kontextuelles 1-NN | Gelabelte Daten + Encoder | Beste Leistung |
| Word Sense Induction | Ungelabelter Text | Cluster; keine benannten Sinne |

Quelle: Jurafsky & Martin (2026).

### In der Praxis

Statische [[embeddings|Embeddings]] teilen sich nicht in diskrete Sinne, während kontextuelle Modelle wie [[bert|BERT]] ein Wort in seinem Kontext darstellen und modernen WSD-Verfahren zugrunde liegen (Jurafsky & Martin, 2026). Das kontextuelle Verfahren ist ein Nächster-Nachbar-Klassifikator ([[k-nearest-neighbors|k-Nearest Neighbors]]), merkmalsbasierte WSD nutzt Kollokationsmerkmale ([[collocations|Kollokationen]]), und Word Sense Induction beruht auf [[clustering|Clustering]] (Jurafsky & Martin, 2026).

### Merksatz

WordNet listet Wortsinne als Synsets, verbunden durch Relationen wie IS-A und Teil-Ganzes; WSD wählt den Sinn eines Wortes im Kontext, am besten per Nächster-Nachbar-Suche über kontextuellen Sinn-Embeddings.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Word Senses and WordNet.* Speech and Language Processing, 3rd ed. draft, Appendix I. [stanford.edu](https://web.stanford.edu/~jurafsky/slp3/I.pdf)
