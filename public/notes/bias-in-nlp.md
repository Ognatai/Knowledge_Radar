---
title_en: Bias in NLP
title_de: Bias in NLP
entity_type: Concept
sources:
- https://edoc.ub.uni-muenchen.de/36297/
- https://doi.org/10.1007/978-3-031-74630-7_20
- https://aclanthology.org/2024.gebnlp-1.8/
- https://arxiv.org/abs/1607.06520
- https://arxiv.org/abs/1608.07187
- https://arxiv.org/abs/2005.14050
- https://arxiv.org/abs/2004.09456
- https://arxiv.org/abs/2110.08193
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Bias in NLP means that language technology reproduces or amplifies social stereotypes and unequal treatment learned from text, for example gender stereotypes in word embeddings (Bolukbasi et al., 2016). It is measured with association tests on embeddings (Caliskan et al., 2016) and with benchmarks for language models and downstream tasks (Nadeem et al., 2020; Parrish et al., 2021). A critical survey argues that such work must state which system behaviours are harmful, in what ways, to whom and why (Blodgett et al., 2020). Because corrections applied after training can overcorrect, discrimination can also be detected and reduced earlier, in the training data itself (Urchs, 2025).

### How it works

Models learn from large amounts of human-written text and pick up the associations it contains, including stereotypes. Bias research measures these associations in embeddings, language models and task outputs, tries to reduce them, and asks what exactly counts as harmful.

```text
1. Bias in word embeddings
▼
2. Association tests
▼
3. Stereotypes in pretrained language models
▼
4. Bias in a downstream task
▼
5. Defining what bias means
▼
6. Bias in generative language models
▼
7. Detecting discrimination in training data
```

#### 1. Bias in word embeddings

Bolukbasi et al. (2016) showed that even word embeddings trained on Google News articles exhibit female/male gender stereotypes to a disturbing extent, and that their widespread use tends to amplify these biases. Geometrically, gender bias is captured by a direction in the embedding, and gender-neutral words are linearly separable from gender-definition words. Using these properties, the authors modify an embedding to remove stereotypes, such as the association between receptionist and female, while keeping desired associations such as between queen and female. They define metrics for direct and indirect gender bias, and their algorithms significantly reduced gender bias while preserving useful properties such as solving analogies ([[embeddings|Embeddings]]). Later work summarised by Urchs (2025) questions whether removing one direction is enough: bias is distributed across many dimensions of the embedding, and gender can still be predicted from supposedly debiased embeddings well above chance.

#### 2. Association tests

Caliskan et al. (2016) showed that standard machine learning on ordinary web text reproduces human-like biases. Using GloVe embeddings, they replicated a spectrum of biases known from the Implicit Association Test and other psychological studies, from morally neutral ones (towards insects or flowers) to problematic ones (towards race or gender) and ones that simply reflect the status quo, such as the distribution of gender across careers. To measure this, they introduced the Word Embedding Association Test (WEAT) and the Word Embedding Factual Association Test (WEFAT), which compare how strongly sets of target words are associated with sets of attribute words in the embedding.

#### 3. Stereotypes in pretrained language models

StereoSet (Nadeem et al., 2020) is a large-scale natural dataset in English for measuring stereotypical bias in four domains: gender, profession, race and religion. The authors note that earlier work evaluated models on small sets of artificially constructed sentences. On StereoSet, popular pretrained models such as BERT, GPT-2, RoBERTa and XLNet showed strong stereotypical biases. A leaderboard with a hidden test set tracks the bias of future models.

#### 4. Bias in a downstream task

The Bias Benchmark for QA (BBQ; Parrish et al., 2021) consists of hand-built question sets on social biases against people in protected classes along nine social dimensions relevant for U.S. English-speaking contexts. It tests two things: with an under-informative context, how strongly answers reflect social biases; and with an adequately informative context, whether the model's biases override a correct answer. Models often relied on stereotypes when the context was under-informative. With informative contexts they were more accurate, but still up to 3.4 percentage points more accurate when the correct answer aligned with a social bias than when it conflicted with it, and over 5 points for gender-related examples for most models tested (Parrish et al., 2021).

#### 5. Defining what bias means

Blodgett et al. (2020) surveyed 146 papers that analyse "bias" in NLP systems. Their motivations were often vague, inconsistent and lacking in normative reasoning, and the proposed measurement and mitigation techniques were poorly matched to these motivations and did not engage with relevant literature outside NLP. The authors recommend recognising the relationships between language and social hierarchies, stating explicitly what kinds of system behaviour are harmful, in what ways, to whom and why, and centring work on the lived experiences of communities affected by NLP systems. Urchs (2025) likewise separates bias, meaning imbalances in data or model behaviour, from discrimination, its manifestation as systematically unequal treatment, and focuses on detecting the latter.

#### 6. Bias in generative language models

Urchs et al. (2023) prompted ChatGPT in English and German to answer from a female, male or neutral perspective and repeated identical prompts to see how responses vary. ChatGPT helped non-IT users draft texts, but its responses had to be checked for biases as well as grammatical mistakes. Overt discrimination was rare, but post-hoc fairness interventions led to overcorrection: neutral prompts produced an over-representation of female personas, and gendered prompts an exaggerated emphasis on diversity. Urchs (2025) concludes that such downstream mitigation after training is not enough and that mitigation should start upstream, in the training data ([[large-language-models|Large Language Models]]).

#### 7. Detecting discrimination in training data

To analyse training data, Urchs et al. (2024) combine linguistic discourse analysis with information extraction: a pipeline identifies the people mentioned in a text (actors), how they are named (nomination) and how they are described (predication). Gender is approximated only from the pronouns used for each actor, without name-based inference or external databases, and the pipeline reports the number of actors and mentions, sentiment and gender-coded language per gender rather than labelling texts as discriminatory (Urchs, 2025; [[information-extraction|Information Extraction]]). Applied to taz2024full, more than 1.8 million German newspaper articles from 1980 to 2024, it showed that men consistently appear more often and receive more textual space, with a gradual shift towards balance in recent years; filtering and rebalancing the corpus reduced surface-level asymmetries, but subtler bias in sentiment and framing persisted (Urchs, 2025).

#### Origin and variants

Bias in word embeddings and its reduction were described by Bolukbasi et al. (2016) and Caliskan et al. (2016). Benchmarks then moved to pretrained language models (Nadeem et al., 2020) and to downstream tasks such as question answering (Parrish et al., 2021), while Blodgett et al. (2020) critically reviewed how the field defines and measures bias. Studies of generative models such as ChatGPT (Urchs et al., 2023) and actor-level analyses of training corpora (Urchs et al., 2024; Urchs, 2025) extend the work to large language models and their data.

### When to use it

- When word embeddings are used in an application, they should be checked for stereotypical associations, for example with association tests (Caliskan et al., 2016; Bolukbasi et al., 2016).
- When a pretrained language model is selected or released, stereotype benchmarks give a first comparison (Nadeem et al., 2020).
- When a system answers questions about people, task-level tests with under-informative and informative contexts show whether stereotypes drive the answers (Parrish et al., 2021).
- When a text corpus is collected for training a language model, an actor-level analysis shows how genders are represented before the model learns from it (Urchs et al., 2024; Urchs, 2025).

### Strengths and limitations

**Strengths**
- Embedding bias can be measured and partly removed while preserving useful properties such as analogy solving (Bolukbasi et al., 2016).
- Association tests make biases measurable that are known from psychology (Caliskan et al., 2016).
- Benchmarks such as StereoSet and BBQ make bias in language models and QA systems comparable (Nadeem et al., 2020; Parrish et al., 2021).
- Actor-level corpus analysis works without labelled data or external gender databases and scales to millions of texts (Urchs, 2025).

**Limitations**
- Many bias studies do not state what they consider harmful and why, and their measurements are poorly matched to their motivations (Blodgett et al., 2020).
- Benchmarks cover selected domains and contexts, for example BBQ only U.S. English-speaking contexts (Parrish et al., 2021).
- Some associations in language simply reflect the status quo, so measuring an association does not by itself show which ones are harmful (Caliskan et al., 2016).
- Post-hoc corrections of a trained model can overcorrect and introduce new distortions (Urchs et al., 2023).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Embedding association tests (WEAT) | Association between target and attribute word sets in an embedding (Caliskan et al., 2016) | Static word embeddings |
| Geometric debiasing | Removes the bias direction from gender-neutral words (Bolukbasi et al., 2016) | Reducing gender bias in embeddings |
| StereoSet | Natural sentences in four domains (Nadeem et al., 2020) | Pretrained language models |
| BBQ | Questions with under-informative and informative contexts on nine dimensions (Parrish et al., 2021) | Question answering systems |
| Actor-level corpus analysis | Nomination and predication of actors per gender, gender from pronouns (Urchs et al., 2024; Urchs, 2025) | Training corpora before model training |

### In practice

Bias tests should be chosen for the application: embedding tests for systems that use static embeddings, task-level tests such as BBQ for systems that answer questions (Caliskan et al., 2016; Parrish et al., 2021). Results should be reported per group rather than only as one aggregate score ([[fairness-metrics|Fairness Metrics]]). Outputs of generative models should be checked repeatedly, since identical prompts can yield different responses (Urchs et al., 2023), and training corpora can be analysed and rebalanced before training (Urchs, 2025). Before measuring, the team should state which behaviours it considers harmful and for whom, as Blodgett et al. (2020) recommend.

### Regulatory context

For high-risk AI systems, the [[eu-ai-act|EU AI Act]] requires training, validation and test data to be examined for possible biases and appropriate measures to detect, prevent and mitigate them (Art. 10(2)(f) and (g)).

### Key takeaway

Bias in NLP is learned from text and can be measured in embeddings, language models and task outputs, but meaningful measurement starts with stating which behaviours are harmful and to whom.

### Sources

- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
- Urchs, S., Thurner, V., Aßenmacher, M., Heumann, C. & Thiemichen, S. (2023). *How Prevalent Is Gender Bias in ChatGPT? Exploring German and English ChatGPT Responses.* ECML PKDD 2023 Workshops, Communications in Computer and Information Science 2133, Springer (2025). [doi:10.1007/978-3-031-74630-7_20](https://doi.org/10.1007/978-3-031-74630-7_20)
- Urchs, S., Thurner, V., Aßenmacher, M., Heumann, C. & Thiemichen, S. (2024). *Detecting Gender Discrimination on Actor Level Using Linguistic Discourse Analysis.* Proceedings of the 5th Workshop on Gender Bias in Natural Language Processing (GeBNLP), ACL 2024. [ACL Anthology](https://aclanthology.org/2024.gebnlp-1.8/)
- Bolukbasi, T. et al. (2016). *Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings.* NeurIPS 2016. [arXiv:1607.06520](https://arxiv.org/abs/1607.06520)
- Caliskan, A. et al. (2016). *Semantics derived automatically from language corpora contain human-like biases.* Science. [arXiv:1608.07187](https://arxiv.org/abs/1608.07187)
- Blodgett, S. L. et al. (2020). *Language (Technology) is Power: A Critical Survey of "Bias" in NLP.* ACL 2020. [arXiv:2005.14050](https://arxiv.org/abs/2005.14050)
- Nadeem, M. et al. (2020). *StereoSet: Measuring stereotypical bias in pretrained language models.* ACL 2021. [arXiv:2004.09456](https://arxiv.org/abs/2004.09456)
- Parrish, A. et al. (2021). *BBQ: A Hand-Built Bias Benchmark for Question Answering.* Findings of ACL 2022. [arXiv:2110.08193](https://arxiv.org/abs/2110.08193)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Bias in NLP bedeutet, dass Sprachtechnologie soziale Stereotype und Ungleichbehandlung, die sie aus Texten gelernt hat, reproduziert oder verstärkt, zum Beispiel Geschlechterstereotype in Wort-Embeddings (Bolukbasi et al., 2016). Gemessen wird Bias mit Assoziationstests auf Embeddings (Caliskan et al., 2016) und mit Benchmarks für Sprachmodelle und nachgelagerte Aufgaben (Nadeem et al., 2020; Parrish et al., 2021). Eine kritische Übersichtsarbeit fordert, dabei offenzulegen, welche Systemverhaltensweisen schädlich sind, auf welche Weise, für wen und warum (Blodgett et al., 2020). Weil Korrekturen nach dem Training zu Überkorrekturen führen können, lässt sich Diskriminierung auch früher erkennen und verringern, nämlich in den Trainingsdaten selbst (Urchs, 2025).

### Funktionsweise

Modelle lernen aus großen Mengen von Menschen geschriebener Texte und übernehmen die darin enthaltenen Assoziationen, auch Stereotype. Die Bias-Forschung misst diese Assoziationen in Embeddings, Sprachmodellen und Aufgabenergebnissen, versucht sie zu verringern und fragt, was genau als schädlich gilt.

```text
1. Bias in Wort-Embeddings
▼
2. Assoziationstests
▼
3. Stereotype in vortrainierten Sprachmodellen
▼
4. Bias in einer nachgelagerten Aufgabe
▼
5. Was Bias bedeutet
▼
6. Bias in generativen Sprachmodellen
▼
7. Diskriminierung in Trainingsdaten erkennen
```

#### 1. Bias in Wort-Embeddings

Bolukbasi et al. (2016) zeigten, dass selbst Wort-Embeddings, die auf Artikeln von Google News trainiert wurden, Geschlechterstereotype in beunruhigendem Ausmaß enthalten und dass ihre verbreitete Nutzung diese Verzerrungen tendenziell verstärkt. Geometrisch wird Geschlechterbias durch eine Richtung im Embedding erfasst, und geschlechtsneutrale Wörter sind linear von geschlechtsdefinierenden Wörtern trennbar. Auf dieser Grundlage verändern die Autoren ein Embedding so, dass Stereotype wie die Assoziation zwischen „receptionist“ und weiblich entfernt werden, gewünschte Assoziationen wie zwischen „queen“ und weiblich aber erhalten bleiben. Sie definieren Metriken für direkten und indirekten Geschlechterbias, und ihre Algorithmen verringerten den Bias deutlich, während nützliche Eigenschaften wie das Lösen von Analogien erhalten blieben ([[embeddings|Embeddings]]). Spätere Arbeiten, die Urchs (2025) zusammenfasst, bezweifeln, dass das Entfernen einer Richtung genügt: Der Bias verteilt sich über viele Dimensionen des Embeddings, und das Geschlecht lässt sich aus angeblich bereinigten Embeddings weiterhin deutlich besser als zufällig vorhersagen.

#### 2. Assoziationstests

Caliskan et al. (2016) zeigten, dass gewöhnliches maschinelles Lernen auf alltäglichem Webtext menschenähnliche Verzerrungen reproduziert. Mit GloVe-Embeddings replizierten sie eine Reihe von Verzerrungen, die aus dem Impliziten Assoziationstest und anderen psychologischen Studien bekannt sind: moralisch neutrale (gegenüber Insekten oder Blumen), problematische (bezogen auf Herkunft oder Geschlecht) und solche, die schlicht den Status quo abbilden, etwa die Verteilung der Geschlechter auf Berufe. Zur Messung führten sie den Word Embedding Association Test (WEAT) und den Word Embedding Factual Association Test (WEFAT) ein, die vergleichen, wie stark Mengen von Zielwörtern im Embedding mit Mengen von Attributwörtern assoziiert sind.

#### 3. Stereotype in vortrainierten Sprachmodellen

StereoSet (Nadeem et al., 2020) ist ein großer englischsprachiger Datensatz aus natürlichen Sätzen, der stereotype Verzerrungen in vier Bereichen misst: Geschlecht, Beruf, Herkunft und Religion. Die Autoren weisen darauf hin, dass frühere Arbeiten Modelle mit kleinen Mengen künstlich konstruierter Sätze bewerteten. Auf StereoSet zeigten verbreitete vortrainierte Modelle wie BERT, GPT-2, RoBERTa und XLNet starke stereotype Verzerrungen. Ein Leaderboard mit verborgenem Testdatensatz verfolgt den Bias künftiger Modelle.

#### 4. Bias in einer nachgelagerten Aufgabe

Der Bias Benchmark for QA (BBQ; Parrish et al., 2021) besteht aus von den Autoren erstellten Fragensets zu sozialen Vorurteilen gegenüber Angehörigen geschützter Gruppen entlang neun sozialer Dimensionen, die für US-amerikanische, englischsprachige Kontexte relevant sind. Er prüft zweierlei: bei unzureichend informativem Kontext, wie stark die Antworten soziale Vorurteile widerspiegeln, und bei ausreichend informativem Kontext, ob die Vorurteile des Modells eine richtige Antwort verdrängen. Bei unzureichendem Kontext stützten sich die Modelle oft auf Stereotype. Bei informativem Kontext waren sie genauer, aber immer noch um bis zu 3,4 Prozentpunkte genauer, wenn die richtige Antwort mit einem sozialen Vorurteil übereinstimmte, als wenn sie ihm widersprach; bei geschlechterbezogenen Beispielen betrug der Unterschied für die meisten getesteten Modelle über 5 Punkte (Parrish et al., 2021).

#### 5. Was Bias bedeutet

Blodgett et al. (2020) werteten 146 Arbeiten aus, die „Bias“ in NLP-Systemen untersuchen. Deren Motivation war oft vage, inkonsistent und ohne normative Begründung, und die vorgeschlagenen Verfahren zur Messung und Minderung passten schlecht zu diesen Motivationen und ignorierten relevante Literatur außerhalb des NLP. Die Autoren empfehlen, die Beziehungen zwischen Sprache und sozialen Hierarchien anzuerkennen, ausdrücklich zu benennen, welche Systemverhaltensweisen auf welche Weise, für wen und warum schädlich sind, und die Arbeit an den gelebten Erfahrungen der von NLP-Systemen betroffenen Gemeinschaften auszurichten. Auch Urchs (2025) trennt Bias, also Ungleichgewichte in Daten oder Modellverhalten, von Diskriminierung als dessen Ausprägung in systematisch ungleicher Behandlung und konzentriert sich darauf, Letztere zu erkennen.

#### 6. Bias in generativen Sprachmodellen

Urchs et al. (2023) ließen ChatGPT auf Englisch und Deutsch aus weiblicher, männlicher oder neutraler Perspektive antworten und wiederholten identische Prompts, um zu sehen, wie stark die Antworten schwanken. ChatGPT half Personen ohne IT-Hintergrund beim Entwerfen von Texten, die Antworten mussten aber auf Bias ebenso wie auf grammatische Fehler geprüft werden. Offene Diskriminierung war selten, doch nachträgliche Fairness-Eingriffe führten zu Überkorrekturen: Neutrale Prompts erzeugten überproportional viele weibliche Personen, geschlechtsbezogene Prompts eine übertriebene Betonung von Diversität. Urchs (2025) folgert, dass eine solche nachgelagerte Korrektur nach dem Training nicht ausreicht und die Minderung bereits vorher, bei den Trainingsdaten, ansetzen sollte ([[large-language-models|Large Language Models]]).

#### 7. Diskriminierung in Trainingsdaten erkennen

Um Trainingsdaten zu untersuchen, verbinden Urchs et al. (2024) linguistische Diskursanalyse mit Informationsextraktion: Eine Pipeline erkennt die in einem Text genannten Personen (Akteur:innen), wie sie benannt werden (Nomination) und wie sie beschrieben werden (Prädikation). Das Geschlecht wird ausschließlich aus den Pronomen erschlossen, die für eine Person verwendet werden, ohne namensbasierte Zuordnung oder externe Datenbanken, und die Pipeline berichtet Zahl der Akteur:innen und Erwähnungen, Sentiment und geschlechtlich konnotierte Sprache je Geschlecht, statt Texte als diskriminierend einzustufen (Urchs, 2025; [[information-extraction|Informationsextraktion]]). Angewendet auf taz2024full, mehr als 1,8 Millionen deutschsprachige Zeitungsartikel von 1980 bis 2024, zeigte sie, dass Männer durchgängig häufiger vorkommen und mehr Textraum erhalten, mit einer allmählichen Annäherung in den letzten Jahren; Filtern und Neugewichten des Korpus verringerte oberflächliche Asymmetrien, subtilerer Bias in Sentiment und Darstellung blieb aber bestehen (Urchs, 2025).

#### Ursprung und Varianten

Bias in Wort-Embeddings und seine Verringerung beschrieben Bolukbasi et al. (2016) und Caliskan et al. (2016). Benchmarks wandten sich danach vortrainierten Sprachmodellen (Nadeem et al., 2020) und nachgelagerten Aufgaben wie der Fragebeantwortung zu (Parrish et al., 2021), während Blodgett et al. (2020) kritisch prüften, wie das Fachgebiet Bias definiert und misst. Untersuchungen generativer Modelle wie ChatGPT (Urchs et al., 2023) und Analysen von Trainingskorpora auf Ebene der Akteur:innen (Urchs et al., 2024; Urchs, 2025) übertragen die Arbeit auf große Sprachmodelle und ihre Daten.

### Wann einsetzen

- Wenn Wort-Embeddings in einer Anwendung verwendet werden, sollten sie auf stereotype Assoziationen geprüft werden, etwa mit Assoziationstests (Caliskan et al., 2016; Bolukbasi et al., 2016).
- Wenn ein vortrainiertes Sprachmodell ausgewählt oder veröffentlicht wird, bieten Stereotyp-Benchmarks einen ersten Vergleich (Nadeem et al., 2020).
- Wenn ein System Fragen über Menschen beantwortet, zeigen aufgabenbezogene Tests mit unzureichendem und informativem Kontext, ob Stereotype die Antworten steuern (Parrish et al., 2021).
- Wenn ein Textkorpus für das Training eines Sprachmodells zusammengestellt wird, zeigt eine Analyse auf Ebene der Akteur:innen, wie die Geschlechter repräsentiert sind, bevor das Modell daraus lernt (Urchs et al., 2024; Urchs, 2025).

### Stärken und Grenzen

**Stärken**
- Bias in Embeddings lässt sich messen und teilweise entfernen, wobei nützliche Eigenschaften wie das Lösen von Analogien erhalten bleiben (Bolukbasi et al., 2016).
- Assoziationstests machen Verzerrungen messbar, die aus der Psychologie bekannt sind (Caliskan et al., 2016).
- Benchmarks wie StereoSet und BBQ machen Bias in Sprachmodellen und QA-Systemen vergleichbar (Nadeem et al., 2020; Parrish et al., 2021).
- Korpusanalysen auf Ebene der Akteur:innen kommen ohne annotierte Daten oder externe Geschlechterdatenbanken aus und skalieren auf Millionen von Texten (Urchs, 2025).

**Einschränkungen**
- Viele Bias-Studien legen nicht offen, was sie als schädlich ansehen und warum, und ihre Messungen passen schlecht zu ihren Motivationen (Blodgett et al., 2020).
- Benchmarks decken ausgewählte Bereiche und Kontexte ab, BBQ etwa nur US-amerikanische, englischsprachige Kontexte (Parrish et al., 2021).
- Manche Assoziationen in der Sprache bilden schlicht den Status quo ab; eine gemessene Assoziation zeigt daher allein noch nicht, welche davon schädlich ist (Caliskan et al., 2016).
- Nachträgliche Korrekturen eines trainierten Modells können überkorrigieren und neue Verzerrungen erzeugen (Urchs et al., 2023).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Assoziationstests auf Embeddings (WEAT) | Assoziation zwischen Ziel- und Attributwortmengen in einem Embedding (Caliskan et al., 2016) | Statische Wort-Embeddings |
| Geometrisches Debiasing | Entfernt die Bias-Richtung aus geschlechtsneutralen Wörtern (Bolukbasi et al., 2016) | Verringerung von Geschlechterbias in Embeddings |
| StereoSet | Natürliche Sätze in vier Bereichen (Nadeem et al., 2020) | Vortrainierte Sprachmodelle |
| BBQ | Fragen mit unzureichendem und informativem Kontext in neun Dimensionen (Parrish et al., 2021) | Systeme zur Fragebeantwortung |
| Korpusanalyse auf Ebene der Akteur:innen | Nomination und Prädikation je Geschlecht, Geschlecht aus Pronomen (Urchs et al., 2024; Urchs, 2025) | Trainingskorpora vor dem Modelltraining |

### In der Praxis

Bias-Tests sollten zur Anwendung passen: Embedding-Tests für Systeme mit statischen Embeddings, aufgabenbezogene Tests wie BBQ für Systeme, die Fragen beantworten (Caliskan et al., 2016; Parrish et al., 2021). Ergebnisse sollten je Gruppe berichtet werden, nicht nur als ein aggregierter Wert ([[fairness-metrics|Fairness-Metriken]]). Ausgaben generativer Modelle sollten mehrfach geprüft werden, da identische Prompts unterschiedliche Antworten liefern können (Urchs et al., 2023), und Trainingskorpora lassen sich vor dem Training analysieren und neu gewichten (Urchs, 2025). Vor der Messung sollte das Team festhalten, welche Verhaltensweisen es für wen als schädlich ansieht, wie Blodgett et al. (2020) empfehlen.

### Regulatorischer Kontext

Für Hochrisiko-KI-Systeme verlangt die [[eu-ai-act|KI-Verordnung]], dass Trainings-, Validierungs- und Testdatensätze im Hinblick auf mögliche Verzerrungen (Bias) untersucht und geeignete Maßnahmen zur Erkennung, Verhinderung und Abschwächung solcher Verzerrungen getroffen werden (Art. 10 Abs. 2 Buchst. f und g).

### Merksatz

Bias in NLP wird aus Texten gelernt und lässt sich in Embeddings, Sprachmodellen und Aufgabenergebnissen messen; sinnvolle Messung beginnt aber mit der Festlegung, welche Verhaltensweisen für wen schädlich sind.

### Quellen

- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
- Urchs, S., Thurner, V., Aßenmacher, M., Heumann, C. & Thiemichen, S. (2023). *How Prevalent Is Gender Bias in ChatGPT? Exploring German and English ChatGPT Responses.* ECML PKDD 2023 Workshops, Communications in Computer and Information Science 2133, Springer (2025). [doi:10.1007/978-3-031-74630-7_20](https://doi.org/10.1007/978-3-031-74630-7_20)
- Urchs, S., Thurner, V., Aßenmacher, M., Heumann, C. & Thiemichen, S. (2024). *Detecting Gender Discrimination on Actor Level Using Linguistic Discourse Analysis.* Proceedings of the 5th Workshop on Gender Bias in Natural Language Processing (GeBNLP), ACL 2024. [ACL Anthology](https://aclanthology.org/2024.gebnlp-1.8/)
- Bolukbasi, T. et al. (2016). *Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings.* NeurIPS 2016. [arXiv:1607.06520](https://arxiv.org/abs/1607.06520)
- Caliskan, A. et al. (2016). *Semantics derived automatically from language corpora contain human-like biases.* Science. [arXiv:1608.07187](https://arxiv.org/abs/1608.07187)
- Blodgett, S. L. et al. (2020). *Language (Technology) is Power: A Critical Survey of "Bias" in NLP.* ACL 2020. [arXiv:2005.14050](https://arxiv.org/abs/2005.14050)
- Nadeem, M. et al. (2020). *StereoSet: Measuring stereotypical bias in pretrained language models.* ACL 2021. [arXiv:2004.09456](https://arxiv.org/abs/2004.09456)
- Parrish, A. et al. (2021). *BBQ: A Hand-Built Bias Benchmark for Question Answering.* Findings of ACL 2022. [arXiv:2110.08193](https://arxiv.org/abs/2110.08193)
