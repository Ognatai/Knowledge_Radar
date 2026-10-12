---
title_en: Near-Duplicate Detection
title_de: Erkennung von Beinahe-Duplikaten (Near-Duplicate Detection)
entity_type: Method
aliases:
- Shingling
- MinHash
- Deduplication
- Near duplicates
sources:
- https://nlp.stanford.edu/IR-book/pdf/19web.pdf
- https://arxiv.org/abs/2107.06499
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Near-duplicate detection finds documents that are identical except for small differences, such as a page that differs only in its last-modified date. Exact fingerprints miss such pairs, and comparing all pairs is infeasible for billions of documents. Shingling turns each document into the set of its overlapping k-word sequences, the Jaccard overlap of two shingle sets measures their similarity, and min-hash sketches of 200 random permutations estimate that overlap cheaply (Manning et al., 2008, ch. 19). Deduplicating language model training data in this way reduces memorised output and needs fewer training steps (Lee et al., 2022).

### How it works

```text
document ─► k-shingles (k = 4) ─► 64-bit hashes ─► min under 200 random permutations = sketch
pairs with overlapping sketches ─► count shared values ─► above threshold (e.g. 160 of 200)
   ─► union-find ─► clusters of near-duplicates ─► keep one per cluster
```

#### 1. Why exact fingerprints are not enough

The simplest test computes a short digest, say 64 bits, of each page and checks pages with equal fingerprints for equality. By some estimates, as many as 40 % of web pages duplicate other pages, many of them legitimately, such as mirrors. But many pages differ from each other only in a few characters, such as a timestamp, and the fingerprint test misses them (Manning et al., 2008, ch. 19).

#### 2. Shingles and the Jaccard coefficient

The k-shingles of a document are all its consecutive sequences of k terms; k = 4 is typical for web pages. For "a rose is a rose is a rose", the 4-shingles are "a rose is a", "rose is a rose" and "is a rose is". Two documents are near-duplicates if the Jaccard coefficient of their shingle sets, |S1 ∩ S2| / |S1 ∪ S2|, exceeds a threshold such as 0.9 (Manning et al., 2008, ch. 19).

#### 3. Min-hash sketches

Each shingle is hashed into 64 bits. Under a random permutation π of the hash values, the probability that two documents have the same smallest permuted value equals the Jaccard coefficient of their shingle sets. Repeating this for 200 random permutations gives each document a sketch of 200 values, and the share of matching values estimates the Jaccard coefficient (Manning et al., 2008, ch. 19).

#### 4. Finding similar pairs without comparing all pairs

Identical documents are first reduced to one copy by their fingerprints, and common HTML tags and integers can be removed from shingling. From the list of (sketch value, document) pairs sorted by value, every pair of documents sharing a value is generated and the shared values are counted; pairs above the threshold, for example at least 160 of 200 for 80 %, are grouped with a union-find algorithm into near-duplicate clusters, a variant of single-link [[clustering|clustering]] (Manning et al., 2008, ch. 19).

#### 5. Deduplicating training data for language models

Language modelling datasets contain many near-duplicate examples and long repeated substrings; one 61-word English sentence occurs more than 60,000 times in C4, and over 1 % of the unprompted output of models trained on such data is copied verbatim from the training data. Lee et al. (2022) built two deduplication tools; models trained on deduplicated data emit memorised text ten times less often and reach the same or better accuracy in fewer training steps. Train-test overlap affects over 4 % of the validation sets of standard datasets, so deduplication also makes evaluation more accurate (Lee et al., 2022).

#### Origin and variants

Shingling with min-hash sketches was developed for detecting near-duplicate web pages (Manning et al., 2008, ch. 19). Its use for cleaning pre-training corpora of [[large-language-models|large language models]] is studied by Lee et al. (2022).

### When to use it

- In crawling and indexing, to avoid storing and processing the same content several times ([[web-crawling|Web Crawling]]; Manning et al., 2008, ch. 19).
- Before training a language model, to remove repeated examples and substrings (Lee et al., 2022).
- Before evaluation, to remove test examples that also occur in the training data (Lee et al., 2022).

### Strengths and limitations

**Strengths**
- Finds pages that differ only slightly, which fingerprints miss (Manning et al., 2008, ch. 19).
- Sketches of 200 values per document avoid comparing all pairs of documents (Manning et al., 2008, ch. 19).
- Deduplicated training data reduces memorisation and training cost (Lee et al., 2022).

**Limitations**
- The estimate is probabilistic; the threshold trades missed duplicates against false matches (Manning et al., 2008, ch. 19).
- Very common shingles, such as markup, must be removed first to avoid spurious matches (Manning et al., 2008, ch. 19).

### Comparison

| Method | Detects | Cost |
|--------|---------|------|
| Exact fingerprint | Identical documents (Manning et al., 2008, ch. 19) | One hash per document |
| Shingles + Jaccard | Near-duplicates (Manning et al., 2008, ch. 19) | Pairwise comparison, infeasible at scale |
| Min-hash sketches | Near-duplicates, estimated (Manning et al., 2008, ch. 19) | 200 values per document |

### In practice

A threshold such as 0.9 for the Jaccard coefficient, or 80 % of matching sketch values, decides which pairs count as near-duplicates (Manning et al., 2008, ch. 19). For language model corpora, deduplication is applied both within the training data and between training and test data (Lee et al., 2022).

### Key takeaway

Near-duplicate detection compares documents as sets of overlapping word sequences and estimates their overlap with min-hash sketches; it keeps indexes lean and makes language model training data less repetitive.

### Sources

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Web search basics* (section 19.6, Near-duplicates and shingling). Introduction to Information Retrieval, Chapter 19. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/19web.pdf)
- Lee, K. et al. (2022). *Deduplicating Training Data Makes Language Models Better.* ACL 2022. [arxiv.org](https://arxiv.org/abs/2107.06499)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die Erkennung von Beinahe-Duplikaten findet Dokumente, die bis auf kleine Unterschiede gleich sind, etwa eine Seite, die sich nur im Datum der letzten Änderung unterscheidet. Exakte Fingerprints übersehen solche Paare, und alle Paare zu vergleichen ist bei Milliarden Dokumenten nicht machbar. Shingling macht aus jedem Dokument die Menge seiner überlappenden Folgen von k Wörtern, die Jaccard-Überlappung zweier Shingle-Mengen misst ihre Ähnlichkeit, und Min-Hash-Sketches aus 200 zufälligen Permutationen schätzen diese Überlappung günstig (Manning et al., 2008, Kap. 19). Trainingsdaten von Sprachmodellen so zu deduplizieren, verringert auswendig gelernte Ausgaben und braucht weniger Trainingsschritte (Lee et al., 2022).

### Funktionsweise

```text
Dokument ─► k-Shingles (k = 4) ─► 64-Bit-Hashes ─► Minimum unter 200 Zufallspermutationen = Sketch
Paare mit überlappenden Sketches ─► gemeinsame Werte zählen ─► über Schwelle (z. B. 160 von 200)
   ─► Union-Find ─► Cluster von Beinahe-Duplikaten ─► je Cluster eines behalten
```

#### 1. Warum exakte Fingerprints nicht reichen

Der einfachste Test berechnet für jede Seite eine kurze Prüfsumme, etwa 64 Bit, und prüft Seiten mit gleichem Fingerprint auf Gleichheit. Schätzungen zufolge sind bis zu 40 % der Webseiten Duplikate anderer Seiten, viele davon legitim, etwa Spiegelserver. Viele Seiten unterscheiden sich aber nur in wenigen Zeichen, etwa einem Zeitstempel, und der Fingerprint-Test übersieht sie (Manning et al., 2008, Kap. 19).

#### 2. Shingles und der Jaccard-Koeffizient

Die k-Shingles eines Dokuments sind alle seine aufeinanderfolgenden Folgen von k Termen; k = 4 ist für Webseiten üblich. Für „a rose is a rose is a rose“ sind die 4-Shingles „a rose is a“, „rose is a rose“ und „is a rose is“. Zwei Dokumente sind Beinahe-Duplikate, wenn der Jaccard-Koeffizient ihrer Shingle-Mengen, |S1 ∩ S2| / |S1 ∪ S2|, eine Schwelle wie 0,9 überschreitet (Manning et al., 2008, Kap. 19).

#### 3. Min-Hash-Sketches

Jedes Shingle wird auf 64 Bit gehasht. Unter einer zufälligen Permutation π der Hashwerte ist die Wahrscheinlichkeit, dass zwei Dokumente denselben kleinsten permutierten Wert haben, gleich dem Jaccard-Koeffizienten ihrer Shingle-Mengen. Wiederholt für 200 zufällige Permutationen erhält jedes Dokument einen Sketch aus 200 Werten, und der Anteil übereinstimmender Werte schätzt den Jaccard-Koeffizienten (Manning et al., 2008, Kap. 19).

#### 4. Ähnliche Paare finden, ohne alle Paare zu vergleichen

Identische Dokumente werden zuerst über ihre Fingerprints auf eine Kopie reduziert, und häufige HTML-Tags und Zahlen können aus dem Shingling entfernt werden. Aus der nach Wert sortierten Liste von Paaren (Sketch-Wert, Dokument) werden alle Dokumentpaare mit einem gemeinsamen Wert erzeugt und die gemeinsamen Werte gezählt; Paare über der Schwelle, etwa mindestens 160 von 200 bei 80 %, werden mit einem Union-Find-Algorithmus zu Clustern von Beinahe-Duplikaten zusammengefasst, einer Variante des Single-Link-[[clustering|Clusterings]] (Manning et al., 2008, Kap. 19).

#### 5. Trainingsdaten für Sprachmodelle deduplizieren

Datensätze für Sprachmodellierung enthalten viele Beinahe-Duplikate und lange wiederholte Teilstrings; ein englischer Satz aus 61 Wörtern kommt in C4 mehr als 60.000-mal vor, und über 1 % der Ausgaben ohne Prompt von Modellen, die auf solchen Daten trainiert wurden, sind wörtlich aus den Trainingsdaten kopiert. Lee et al. (2022) bauten zwei Werkzeuge zur Deduplizierung; Modelle, die auf deduplizierten Daten trainiert wurden, geben zehnmal seltener auswendig gelernten Text aus und erreichen dieselbe oder bessere Genauigkeit in weniger Trainingsschritten. Überschneidungen zwischen Trainings- und Testdaten betreffen über 4 % der Validierungsmengen gängiger Datensätze, sodass Deduplizierung auch die Evaluation genauer macht (Lee et al., 2022).

#### Herkunft und Varianten

Shingling mit Min-Hash-Sketches wurde zum Erkennen beinahe gleicher Webseiten entwickelt (Manning et al., 2008, Kap. 19). Seinen Einsatz zum Bereinigen der Vortrainingskorpora von [[large-language-models|Large Language Models]] untersuchen Lee et al. (2022).

### Wann einsetzen

- Beim Crawlen und Indexieren, um denselben Inhalt nicht mehrfach zu speichern und zu verarbeiten ([[web-crawling|Web-Crawling]]; Manning et al., 2008, Kap. 19).
- Vor dem Training eines Sprachmodells, um wiederholte Beispiele und Teilstrings zu entfernen (Lee et al., 2022).
- Vor der Evaluation, um Testbeispiele zu entfernen, die auch in den Trainingsdaten vorkommen (Lee et al., 2022).

### Stärken und Grenzen

**Stärken**
- Findet Seiten mit nur geringen Unterschieden, die Fingerprints übersehen (Manning et al., 2008, Kap. 19).
- Sketches aus 200 Werten pro Dokument ersparen den Vergleich aller Dokumentpaare (Manning et al., 2008, Kap. 19).
- Deduplizierte Trainingsdaten verringern Auswendiglernen und Trainingsaufwand (Lee et al., 2022).

**Grenzen**
- Die Schätzung ist probabilistisch; die Schwelle wägt übersehene Duplikate gegen falsche Treffer ab (Manning et al., 2008, Kap. 19).
- Sehr häufige Shingles wie Markup müssen vorher entfernt werden, um Scheintreffer zu vermeiden (Manning et al., 2008, Kap. 19).

### Vergleich

| Methode | Erkennt | Aufwand |
|---------|---------|---------|
| Exakter Fingerprint | Identische Dokumente (Manning et al., 2008, Kap. 19) | Ein Hash pro Dokument |
| Shingles + Jaccard | Beinahe-Duplikate (Manning et al., 2008, Kap. 19) | Paarweiser Vergleich, im großen Maßstab unmöglich |
| Min-Hash-Sketches | Beinahe-Duplikate, geschätzt (Manning et al., 2008, Kap. 19) | 200 Werte pro Dokument |

### In der Praxis

Eine Schwelle wie 0,9 für den Jaccard-Koeffizienten oder 80 % übereinstimmender Sketch-Werte entscheidet, welche Paare als Beinahe-Duplikate gelten (Manning et al., 2008, Kap. 19). Bei Korpora für Sprachmodelle wird sowohl innerhalb der Trainingsdaten als auch zwischen Trainings- und Testdaten dedupliziert (Lee et al., 2022).

### Merksatz

Die Erkennung von Beinahe-Duplikaten vergleicht Dokumente als Mengen überlappender Wortfolgen und schätzt ihre Überlappung mit Min-Hash-Sketches; sie hält Indizes schlank und macht Trainingsdaten von Sprachmodellen weniger repetitiv.

### Quellen

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Web search basics* (Abschnitt 19.6, Near-duplicates and shingling). Introduction to Information Retrieval, Chapter 19. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/19web.pdf)
- Lee, K. et al. (2022). *Deduplicating Training Data Makes Language Models Better.* ACL 2022. [arxiv.org](https://arxiv.org/abs/2107.06499)
