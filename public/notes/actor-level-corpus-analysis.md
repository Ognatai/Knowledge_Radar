---
title_en: Actor-Level Corpus Analysis
title_de: Akteursbasierte Korpusanalyse
entity_type: Method
aliases:
- Actor-level corpus analysis
- Actor-level discrimination detection
- Nomination and predication analysis
sources:
- https://aclanthology.org/2024.gebnlp-1.8/
- https://edoc.ub.uni-muenchen.de/36297/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Actor-level corpus analysis detects gender discrimination in texts by looking at the people a text talks about, its actors, instead of treating the text as a whole (Urchs et al., 2024). It partly automates two strategies from linguistic discourse analysis with [[information-extraction|information extraction]]: nomination, how an actor is named and referred to, and predication, which traits and characteristics the text ascribes to them. A four-step pipeline extracts actors, approximates their gender only from the pronouns used for them, collects their predications and compiles a discrimination report per gender, with counts of actors and mentions, sentiment and gender-coded words (Urchs et al., 2024). Urchs (2025) scaled the approach to 1.8 million German newspaper articles and extended it to filter and rebalance training corpora; the reports describe asymmetries rather than labelling texts as discriminatory.

### How it works

```text
text / corpus
  │ 1 actor extraction       tokenise, parse, NER → PERSON entities; merge name parts, titles, generic names
  │ 2 gender approximation   coreference → pronouns per actor; ≥ 70 % one gender → woman / man, else undefined
  │ 3 predication extraction sentences that mention the actor
  │ 4 discrimination analysis per gender: actors, mentions, sentiment, gender-coded words
  ▼                          (+ corpus version: PMI words, subject/object role, quotation style, generic masculine)
discrimination report  →  human interpretation, optional filtering and corpus balancing
```

#### 1. Actors, nomination and predication

In linguistic discourse analysis, actors are the entities in a text that perform actions, such as individuals, groups or institutions (Urchs et al., 2024). Nomination covers how an actor is named: proper names, generic names, pronouns and deagentification, where the actor is not named at all. Predication covers the traits, characteristics, qualities and features ascribed to the actor, visible in attributes, prepositional attributes, collocations and relative clauses (Urchs et al., 2024). Focusing on actors aims to reveal subtle discrimination that word lists of drastic terms miss.

#### 2. Actor extraction

The pipeline tokenises the text without further preprocessing, parses dependency trees, tags parts of speech and runs named entity recognition; person entities become the actors (Urchs et al., 2024; [[entity-extraction|entity extraction]], [[dependency-parsing|dependency parsing]]). Name parts, titles and abbreviations are merged under one key per actor, and generic names are added from a list. The proof of concept used spaCy with coreferee for coreference (Urchs et al., 2024).

#### 3. Gender approximation from pronouns

Gender is approximated only from the pronouns that refer to an actor: if at least 70% refer to one gender, the actor is labelled woman or man; non-binary only if gender-neutral pronouns are used consistently; otherwise undefined (Urchs et al., 2024). The method deliberately avoids name-based inference and external databases, which are culturally biased, so that all information comes from the text itself (Urchs, 2025).

#### 4. Predication and the discrimination report

Every sentence that mentions an actor is assigned to that actor's predication; the report then gives, overall and per actor, the number of actors and mentions per gender, the sentiment of the predication sentences, feminine- and masculine-coded words from an existing list of gender-coded word stems and abusive terms (Urchs et al., 2024). Counting mentions as well as actors matters: one woman mentioned ten times is not the same as ten men mentioned once each (Urchs, 2025).

#### Origin and variants

The method was first tested on single English news texts and texts generated with [[chatgpt|ChatGPT]] (Urchs et al., 2024). Urchs (2025, chapter 7) adapted it to German and to corpus scale with multiprocessing, using the dominant pronouns sie and er, adding markers for the generic masculine and gender-neutral language and PMI scores for the most characteristic adjectives per actor ([[collocations|collocations]]); applied to the taz2024full corpus of over 1.8 million taz articles from 1980 to 2024, it found men mentioned more often and framed more positively than women, though coverage of women increased over time. Chapter 8 added syntactic agency (subject vs. object position), direct vs. indirect quotation and named vs. pronominal reference, and used these metrics to exclude articles with strong asymmetries and then rebalance the corpus to a user-defined equilibrium, which reached near parity in actor and mention ratios (Urchs, 2025).

### When to use it

- Auditing a text corpus for gender representation before training a language model on it (Urchs, 2025; [[bias-in-nlp|bias in NLP]]).
- Diachronic studies of how media portray different genders (Urchs, 2025).
- Curating training data with transparent, user-configurable exclusion and balancing criteria instead of downstream debiasing (Urchs, 2025).
- Supporting social scientists who analyse discourse at a scale that manual analysis cannot reach (Urchs et al., 2024).

### Strengths and limitations

**Strengths**
- Works without labelled data, pretrained gender classifiers or external knowledge bases (Urchs, 2025).
- Modular and language-agnostic: components can be exchanged, for example for domain-specific sentiment or hate speech models (Urchs et al., 2024).
- Reports asymmetries for human judgement instead of imposing a normative label (Urchs, 2025).

**Limitations**
- Only texts that describe specific actors can be analysed (Urchs et al., 2024).
- Coreference tools handle gender-neutral pronouns poorly; in the proof of concept, non-binary actors were detected in only one of three test texts (Urchs et al., 2024).
- Assigning every sentence that mentions an actor to their predication is a simplification; it also distorts sentiment when a sentence names several actors (Urchs et al., 2024).
- A sentiment model trained on movie reviews misjudged news language (Urchs et al., 2024).
- Covers gender only, not other or intersectional forms of discrimination (Urchs, 2025).

### Comparison

| Approach | Unit of analysis | Gender information | Output |
|---|---|---|---|
| Word lists / hate speech detection | text | not needed | flag for drastic wording |
| Gender Gap Tracker (Canadian news) | quoted people in news | name-based external service | quotation statistics |
| Actor-level corpus analysis | actors in text or corpus | pronouns in the text | per-gender report, optional filtering |

Sources: Urchs et al. (2024); Urchs (2025).

### In practice

Read the report as a description: the aim is to make representation visible, while the decision whether a text or corpus is acceptable stays with people who know its context (Urchs, 2025). Training data loses the context of a text, so evaluate it assuming an out-group reader and current social norms (Urchs et al., 2024). Replace general-purpose components, especially sentiment, with domain-specific ones, and check a sample of coreference results by hand ([[fairness-metrics|fairness metrics]]). The code is available on GitHub (Ognatai/nomination_predication, corpus_pipeline, corpus_balancing).

### Key takeaway

Actor-level corpus analysis asks who appears in a text, how they are named and how they are described, approximates their gender from pronouns alone and reports asymmetries per gender; at corpus scale, the same metrics can filter and rebalance training data.

### Sources

- Urchs, S., Thurner, V., Aßenmacher, M., Heumann, C. & Thiemichen, S. (2024). Detecting Gender Discrimination on Actor Level Using Linguistic Discourse Analysis. *Proceedings of the 5th Workshop on Gender Bias in Natural Language Processing (GeBNLP)*, 140–149. [ACL Anthology](https://aclanthology.org/2024.gebnlp-1.8/)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing*. Dissertation, LMU München, chapters 3, 6–8. [edoc.ub.uni-muenchen.de](https://edoc.ub.uni-muenchen.de/36297/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die akteursbasierte Korpusanalyse erkennt Geschlechterdiskriminierung in Texten, indem sie die Personen betrachtet, über die ein Text spricht, seine Akteure, statt den Text als Ganzes zu behandeln (Urchs et al., 2024). Sie automatisiert teilweise zwei Strategien der linguistischen Diskursanalyse mit [[information-extraction|Informationsextraktion]]: Nomination, also wie ein Akteur benannt und bezeichnet wird, und Prädikation, also welche Eigenschaften und Merkmale der Text ihm zuschreibt. Eine vierstufige Pipeline extrahiert Akteure, schätzt ihr Geschlecht allein aus den für sie verwendeten Pronomen, sammelt ihre Prädikationen und erstellt einen Diskriminierungsbericht je Geschlecht mit der Zahl der Akteure und Erwähnungen, dem Sentiment und geschlechtlich konnotierten Wörtern (Urchs et al., 2024). Urchs (2025) skalierte den Ansatz auf 1,8 Millionen deutsche Zeitungsartikel und erweiterte ihn zum Filtern und Ausbalancieren von Trainingskorpora; die Berichte beschreiben Asymmetrien, statt Texte als diskriminierend zu etikettieren.

### Funktionsweise

```text
Text / Korpus
  │ 1 Akteursextraktion        tokenisieren, parsen, NER → PERSON-Entitäten; Namensteile, Titel, generische Namen zusammenführen
  │ 2 Geschlechtsschätzung     Koreferenz → Pronomen je Akteur; ≥ 70 % ein Geschlecht → Frau / Mann, sonst undefiniert
  │ 3 Prädikationsextraktion   Sätze, die den Akteur erwähnen
  │ 4 Diskriminierungsanalyse  je Geschlecht: Akteure, Erwähnungen, Sentiment, geschlechtlich konnotierte Wörter
  ▼                            (+ Korpusversion: PMI-Wörter, Subjekt-/Objektrolle, Zitierweise, generisches Maskulinum)
Diskriminierungsbericht  →  menschliche Deutung, optional Filterung und Korpusausgleich
```

#### 1. Akteure, Nomination und Prädikation

In der linguistischen Diskursanalyse sind Akteure die Entitäten eines Textes, die handeln, etwa Einzelpersonen, Gruppen oder Institutionen (Urchs et al., 2024). Nomination umfasst, wie ein Akteur benannt wird: Eigennamen, generische Namen, Pronomen und Deagentivierung, bei der der Akteur gar nicht genannt wird. Prädikation umfasst die Eigenschaften, Merkmale, Qualitäten und Züge, die dem Akteur zugeschrieben werden, erkennbar an Attributen, Präpositionalattributen, Kollokationen und Relativsätzen (Urchs et al., 2024). Der Fokus auf Akteure soll subtile Diskriminierung sichtbar machen, die Wortlisten drastischer Begriffe übersehen.

#### 2. Akteursextraktion

Die Pipeline tokenisiert den Text ohne weitere Vorverarbeitung, erstellt Dependenzbäume, bestimmt Wortarten und führt Named Entity Recognition aus; Personen-Entitäten werden zu Akteuren (Urchs et al., 2024; [[entity-extraction|Entitätsextraktion]], [[dependency-parsing|Dependenzparsing]]). Namensteile, Titel und Abkürzungen werden unter einem Schlüssel je Akteur zusammengeführt, und generische Namen werden aus einer Liste ergänzt. Der Proof of Concept nutzte spaCy mit coreferee für die Koreferenzauflösung (Urchs et al., 2024).

#### 3. Geschlechtsschätzung aus Pronomen

Das Geschlecht wird allein aus den Pronomen geschätzt, die sich auf einen Akteur beziehen: Beziehen sich mindestens 70 % auf ein Geschlecht, wird der Akteur als Frau oder Mann gekennzeichnet; nichtbinär nur, wenn durchgängig geschlechtsneutrale Pronomen verwendet werden; sonst undefiniert (Urchs et al., 2024). Das Verfahren vermeidet bewusst namensbasierte Zuordnung und externe Datenbanken, die kulturell verzerrt sind, sodass alle Informationen aus dem Text selbst stammen (Urchs, 2025).

#### 4. Prädikation und Diskriminierungsbericht

Jeder Satz, der einen Akteur erwähnt, wird dessen Prädikation zugeordnet; der Bericht nennt dann insgesamt und je Akteur die Zahl der Akteure und Erwähnungen je Geschlecht, das Sentiment der Prädikationssätze, weiblich und männlich konnotierte Wörter aus einer bestehenden Liste geschlechtlich konnotierter Wortstämme und abwertende Begriffe (Urchs et al., 2024). Neben den Akteuren auch die Erwähnungen zu zählen, ist wichtig: Eine Frau, die zehnmal erwähnt wird, ist nicht dasselbe wie zehn Männer, die je einmal erwähnt werden (Urchs, 2025).

#### Herkunft und Varianten

Das Verfahren wurde zunächst an einzelnen englischen Nachrichtentexten und mit [[chatgpt|ChatGPT]] erzeugten Texten erprobt (Urchs et al., 2024). Urchs (2025, Kapitel 7) passte es mit Multiprocessing an das Deutsche und an Korpusgröße an, nutzte die vorherrschenden Pronomen sie und er, ergänzte Marker für das generische Maskulinum und geschlechtergerechte Sprache sowie PMI-Werte für die charakteristischsten Adjektive je Akteur ([[collocations|Kollokationen]]); angewandt auf das Korpus taz2024full mit über 1,8 Millionen taz-Artikeln von 1980 bis 2024 zeigte sich, dass Männer häufiger erwähnt und positiver dargestellt wurden als Frauen, wobei die Berichterstattung über Frauen im Lauf der Zeit zunahm. Kapitel 8 ergänzte syntaktische Handlungsmacht (Subjekt- vs. Objektposition), direkte vs. indirekte Zitate und namentliche vs. pronominale Bezugnahme und nutzte diese Metriken, um Artikel mit starken Asymmetrien auszuschließen und das Korpus anschließend auf ein nutzerdefiniertes Gleichgewicht auszubalancieren, was nahezu Parität bei den Verhältnissen von Akteuren und Erwähnungen erreichte (Urchs, 2025).

### Wann einsetzen

- Prüfung eines Textkorpus auf die Repräsentation der Geschlechter, bevor ein Sprachmodell darauf trainiert wird (Urchs, 2025; [[bias-in-nlp|Bias in NLP]]).
- Diachrone Studien dazu, wie Medien verschiedene Geschlechter darstellen (Urchs, 2025).
- Kuratierung von Trainingsdaten mit transparenten, konfigurierbaren Ausschluss- und Ausgleichskriterien statt nachgelagertem Debiasing (Urchs, 2025).
- Unterstützung sozialwissenschaftlicher Diskursanalysen in einem Umfang, den manuelle Analyse nicht erreicht (Urchs et al., 2024).

### Stärken und Grenzen

**Stärken**
- Funktioniert ohne gelabelte Daten, vortrainierte Geschlechtsklassifikatoren oder externe Wissensbasen (Urchs, 2025).
- Modular und sprachunabhängig: Komponenten lassen sich austauschen, etwa gegen domänenspezifische Sentiment- oder Hassrede-Modelle (Urchs et al., 2024).
- Berichtet Asymmetrien zur menschlichen Beurteilung, statt ein normatives Etikett zu vergeben (Urchs, 2025).

**Grenzen**
- Nur Texte, die bestimmte Akteure beschreiben, lassen sich analysieren (Urchs et al., 2024).
- Koreferenzwerkzeuge verarbeiten geschlechtsneutrale Pronomen schlecht; im Proof of Concept wurden nichtbinäre Akteure nur in einem von drei Testtexten erkannt (Urchs et al., 2024).
- Jeden Satz, der einen Akteur erwähnt, seiner Prädikation zuzuordnen, ist eine Vereinfachung; sie verzerrt auch das Sentiment, wenn ein Satz mehrere Akteure nennt (Urchs et al., 2024).
- Ein auf Filmrezensionen trainiertes Sentiment-Modell beurteilte Nachrichtensprache falsch (Urchs et al., 2024).
- Deckt nur das Geschlecht ab, keine anderen oder intersektionalen Formen von Diskriminierung (Urchs, 2025).

### Vergleich

| Ansatz | Analyseeinheit | Geschlechtsinformation | Ergebnis |
|---|---|---|---|
| Wortlisten / Hassrede-Erkennung | Text | nicht nötig | Markierung drastischer Wortwahl |
| Gender Gap Tracker (kanadische Nachrichten) | zitierte Personen in Nachrichten | namensbasierter externer Dienst | Zitierstatistiken |
| Akteursbasierte Korpusanalyse | Akteure in Text oder Korpus | Pronomen im Text | Bericht je Geschlecht, optional Filterung |

Quellen: Urchs et al. (2024); Urchs (2025).

### In der Praxis

Der Bericht ist als Beschreibung zu lesen: Ziel ist, Repräsentation sichtbar zu machen, während die Entscheidung, ob ein Text oder Korpus akzeptabel ist, bei Menschen bleibt, die seinen Kontext kennen (Urchs, 2025). Trainingsdaten verlieren den Kontext eines Textes, daher sollten sie unter Annahme einer Außengruppen-Leserschaft und aktueller sozialer Normen bewertet werden (Urchs et al., 2024). Allgemeine Komponenten, vor allem das Sentiment, sollten durch domänenspezifische ersetzt und Koreferenzergebnisse stichprobenartig von Hand geprüft werden ([[fairness-metrics|Fairness-Metriken]]). Der Code liegt auf GitHub (Ognatai/nomination_predication, corpus_pipeline, corpus_balancing).

### Merksatz

Die akteursbasierte Korpusanalyse fragt, wer in einem Text vorkommt, wie die Personen benannt und beschrieben werden, schätzt ihr Geschlecht allein aus Pronomen und berichtet Asymmetrien je Geschlecht; auf Korpusebene können dieselben Metriken Trainingsdaten filtern und ausbalancieren.

### Quellen

- Urchs, S., Thurner, V., Aßenmacher, M., Heumann, C. & Thiemichen, S. (2024). Detecting Gender Discrimination on Actor Level Using Linguistic Discourse Analysis. *Proceedings of the 5th Workshop on Gender Bias in Natural Language Processing (GeBNLP)*, 140–149. [ACL Anthology](https://aclanthology.org/2024.gebnlp-1.8/)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing*. Dissertation, LMU München, Kapitel 3, 6–8. [edoc.ub.uni-muenchen.de](https://edoc.ub.uni-muenchen.de/36297/)
