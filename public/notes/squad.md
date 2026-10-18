---
title_en: SQuAD
title_de: SQuAD
entity_type: Dataset
aliases:
- SQuAD
- Stanford Question Answering Dataset
- SQuAD 1.1
- SQuAD 2.0
sources:
- https://arxiv.org/abs/1606.05250
- https://arxiv.org/abs/1806.03822
- https://arxiv.org/abs/1910.10683
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

The Stanford Question Answering Dataset (SQuAD) is a reading comprehension benchmark in which crowdworkers wrote more than 100,000 questions about Wikipedia paragraphs, and the answer to each question is a span of text from the paragraph (Rajpurkar et al., 2016). Systems are scored by exact match and token-level F1 against human answers; at release, a [[classification|logistic regression]] model reached 51.0% F1 against 86.8% for humans (Rajpurkar et al., 2016). SQuAD 2.0 added over 50,000 unanswerable questions written to look answerable, so that systems must also know when to abstain: a strong model with 86% F1 on SQuAD 1.1 reached only 66% on SQuAD 2.0 (Rajpurkar et al., 2018). SQuAD became one of the standard benchmarks for extractive [[information-extraction|question answering]] and is part of the evaluation of models such as [[t5|T5]] (Raffel et al., 2019).

### How it works

```text
Wikipedia: top 10,000 articles by PageRank → 536 sampled → 23,215 paragraphs
 ▼
crowdworkers ask and answer up to 5 questions per paragraph (answer = span)
 ▼
≥ 2 additional answers per question from other workers (dev / test)
 ▼
split by article: 80% train, 10% dev, 10% test
 ▼
system predicts a span → exact match and F1 against all reference answers
 ▼
SQuAD 2.0: + 53,775 adversarial unanswerable questions → predict span or "no answer"
```

#### 1. Building the passages

To get high-quality articles, the authors took the top 10,000 articles of English Wikipedia by an internal PageRank, sampled 536 of them uniformly at random, extracted paragraphs, removed images, figures and tables and discarded paragraphs shorter than 500 characters; the result was 23,215 paragraphs on topics from musical celebrities to abstract concepts (Rajpurkar et al., 2016). Articles, not paragraphs, were split randomly into training (80%), development (10%) and test (10%) sets, so that test questions come from unseen articles (Rajpurkar et al., 2016). Link-based ranking of this kind is explained in [[pagerank|PageRank]].

#### 2. Collecting questions and answers

Crowdworkers on Amazon Mechanical Turk, via the Daemo platform, located in the United States or Canada and with high acceptance rates, were asked to spend 4 minutes per paragraph, were paid 9 US dollars per hour, and posed and answered questions whose answers are spans in the paragraph (Rajpurkar et al., 2016). SQuAD 1.0 contains 107,785 question-answer pairs on the 536 articles, almost two orders of magnitude more than earlier manually labelled reading comprehension datasets such as MCTest (Rajpurkar et al., 2016). Unlike multiple-choice datasets, SQuAD gives no answer options: systems must choose among all possible spans in the passage (Rajpurkar et al., 2016).

#### 3. Metrics: exact match and F1

Exact match counts a prediction as correct only if it equals one of the reference answers; F1 measures token overlap between prediction and reference and gives partial credit (Rajpurkar et al., 2016). Human performance, measured by treating one worker's answer as the prediction, was 77.0% exact match and 86.8% F1 on the test set; mismatches were mostly about including or excluding non-essential phrases rather than real disagreement (Rajpurkar et al., 2016). The metrics are related to the overlap measures in [[text-similarity-metrics|text similarity metrics]] and to precision and recall in [[classification-metrics|classification metrics]].

#### 4. What the questions require

The authors analysed the reasoning needed with dependency and constituency trees ([[dependency-parsing|dependency parsing]], [[constituency-parsing|constituency parsing]]). Their logistic regression baseline depended strongly on lexical and dependency-path features, and its performance dropped as answer types became more complex and as the syntax of the question diverged from the sentence containing the answer, while human performance did not drop (Rajpurkar et al., 2016). A sliding-window baseline reached about 20% F1 (Rajpurkar et al., 2016).

#### 5. SQuAD 2.0: unanswerable questions

Extractive systems tend to make unreliable guesses when the paragraph does not contain the answer (Rajpurkar et al., 2018). SQuAD 2.0 combines SQuAD 1.1 with 53,775 new unanswerable questions about the same paragraphs, written by crowdworkers so that they are relevant to the paragraph and the paragraph contains a plausible answer of the right type (Rajpurkar et al., 2018). Systems must answer when possible and abstain otherwise; a state-of-the-art model reached 66.3% F1 on SQuAD 2.0 against 89.5% for humans, while the same architecture trained on SQuAD 1.1 reached 85.8% (Rajpurkar et al., 2018). Abstaining when the context lacks the answer is the same requirement as in [[retrieval-augmented-generation|RAG]] systems ([[hallucination-detection|hallucination detection]]).

#### 6. Results over time

Neural models soon improved on the baseline, for example to 70.3% F1 on SQuAD 1.1 shortly after release (Rajpurkar et al., 2016). By 2019, [[t5|T5]]-11B outperformed the previous best result on SQuAD by more than one point exact match; its authors noted that human performance is estimated at 82.3 exact match and 91.2 F1, so further improvements may not be meaningful (Raffel et al., 2019).

#### Origin and variants

SQuAD was released by Rajpurkar et al. (2016) at Stanford; SQuAD 2.0 added unanswerable questions (Rajpurkar et al., 2018). It is a component of multi-task evaluations such as the one in the T5 study (Raffel et al., 2019).

### When to use it

- To evaluate extractive question answering, where the answer must be a span of a given passage (Rajpurkar et al., 2016).
- To test whether a system abstains when the passage does not contain the answer, with SQuAD 2.0 (Rajpurkar et al., 2018).
- As a reading comprehension component of a broader benchmark suite (Raffel et al., 2019).

### Strengths and limitations

**Strengths**
- Large, human-written dataset with clear, automatic metrics (Rajpurkar et al., 2016).
- Article-level splits avoid overlap between training and test passages (Rajpurkar et al., 2016).
- SQuAD 2.0 tests abstention with adversarially written unanswerable questions (Rajpurkar et al., 2018).

**Limitations**
- Span-based answers are more constrained than open, interpretative questions (Rajpurkar et al., 2016).
- Models have reached or exceeded estimated human performance, which limits how much further gains mean (Raffel et al., 2019).
- English Wikipedia only, and a feature-based baseline already depended strongly on lexical features (Rajpurkar et al., 2016).

### Comparison

| Dataset | Answer form | Unanswerable questions | Source of passages |
|---|---|---|---|
| SQuAD 1.1 | span in paragraph | no | 536 Wikipedia articles |
| SQuAD 2.0 | span or no answer | 53,775 adversarial | same paragraphs |
| [[ms-marco\|MS MARCO]] | human-written answers from web passages | yes, labelled | real Bing queries |
| [[glue\|GLUE]] | labels for classification tasks | – | various |
| Multiple-choice reading tests (e.g. MCTest) | choice among options | – | – |

Sources: Rajpurkar et al. (2016); Rajpurkar et al. (2018).

### In practice

Report exact match and F1 together and state which version (1.1 or 2.0) is used, since scores are not comparable across versions (Rajpurkar et al., 2018). For generative models, answers often need normalisation before exact match, because extra words count as errors; this is why F1 is usually the more informative number (Rajpurkar et al., 2016). Reading comprehension is one ingredient of [[rag-generation-evaluation|evaluating RAG generation]], which additionally checks faithfulness to retrieved context.

### Key takeaway

SQuAD measures whether a system can find the answer span to a question in a Wikipedia paragraph, and SQuAD 2.0 whether it can also tell when there is none; both are scored with exact match and F1.

### Sources

- Rajpurkar, P., Zhang, J., Lopyrev, K. & Liang, P. (2016). *SQuAD: 100,000+ Questions for Machine Comprehension of Text.* arXiv:1606.05250. [arXiv](https://arxiv.org/abs/1606.05250)
- Rajpurkar, P., Jia, R. & Liang, P. (2018). *Know What You Don't Know: Unanswerable Questions for SQuAD.* arXiv:1806.03822. [arXiv](https://arxiv.org/abs/1806.03822)
- Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W. & Liu, P. J. (2019). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer.* arXiv:1910.10683. [arXiv](https://arxiv.org/abs/1910.10683)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Der Stanford Question Answering Dataset (SQuAD) ist ein Benchmark für Leseverständnis, in dem Crowdworker mehr als 100.000 Fragen zu Wikipedia-Absätzen geschrieben haben; die Antwort auf jede Frage ist ein Textabschnitt (Span) aus dem Absatz (Rajpurkar et al., 2016). Systeme werden mit Exact Match und F1 auf Tokenebene gegen menschliche Antworten bewertet; bei der Veröffentlichung erreichte ein Modell mit logistischer Regression 51,0 % F1, Menschen 86,8 % (Rajpurkar et al., 2016). SQuAD 2.0 ergänzte über 50.000 unbeantwortbare Fragen, die beantwortbar wirken sollen, sodass Systeme auch erkennen müssen, wann sie sich enthalten: Ein starkes Modell mit 86 % F1 auf SQuAD 1.1 erreichte auf SQuAD 2.0 nur 66 % (Rajpurkar et al., 2018). SQuAD wurde zu einem der Standard-Benchmarks für extraktive [[information-extraction|Fragebeantwortung]] und gehört zur Evaluation von Modellen wie [[t5|T5]] (Raffel et al., 2019).

### Funktionsweise

```text
Wikipedia: 10.000 Top-Artikel nach PageRank → 536 gezogen → 23.215 Absätze
 ▼
Crowdworker stellen und beantworten bis zu 5 Fragen je Absatz (Antwort = Span)
 ▼
≥ 2 zusätzliche Antworten je Frage von anderen Personen (Dev / Test)
 ▼
Aufteilung nach Artikeln: 80 % Training, 10 % Dev, 10 % Test
 ▼
System sagt einen Span vorher → Exact Match und F1 gegen alle Referenzantworten
 ▼
SQuAD 2.0: + 53.775 adversarial geschriebene unbeantwortbare Fragen → Span oder „keine Antwort“
```

#### 1. Aufbau der Textpassagen

Für hochwertige Artikel nahmen die Autoren die 10.000 wichtigsten Artikel der englischen Wikipedia nach einem internen PageRank, zogen davon 536 gleichverteilt zufällig, extrahierten die Absätze, entfernten Bilder, Abbildungen und Tabellen und verwarfen Absätze unter 500 Zeichen; das ergab 23.215 Absätze zu Themen von Musikstars bis zu abstrakten Begriffen (Rajpurkar et al., 2016). Aufgeteilt wurden Artikel, nicht Absätze, zufällig in Training (80 %), Entwicklung (10 %) und Test (10 %), sodass Testfragen aus unbekannten Artikeln stammen (Rajpurkar et al., 2016). Linkbasierte Rangfolgen dieser Art erklärt [[pagerank|PageRank]].

#### 2. Fragen und Antworten sammeln

Crowdworker auf Amazon Mechanical Turk, über die Plattform Daemo, aus den USA oder Kanada und mit hohen Annahmequoten, sollten 4 Minuten je Absatz aufwenden, erhielten 9 US-Dollar pro Stunde und stellten und beantworteten Fragen, deren Antworten Spans im Absatz sind (Rajpurkar et al., 2016). SQuAD 1.0 enthält 107.785 Frage-Antwort-Paare zu den 536 Artikeln, fast zwei Größenordnungen mehr als frühere, manuell annotierte Leseverständnis-Datensätze wie MCTest (Rajpurkar et al., 2016). Anders als Multiple-Choice-Datensätze gibt SQuAD keine Antwortoptionen vor: Systeme müssen unter allen möglichen Spans der Passage wählen (Rajpurkar et al., 2016).

#### 3. Metriken: Exact Match und F1

Exact Match wertet eine Vorhersage nur dann als richtig, wenn sie einer der Referenzantworten gleicht; F1 misst die Überlappung der Tokens zwischen Vorhersage und Referenz und rechnet Teilübereinstimmungen an (Rajpurkar et al., 2016). Die menschliche Leistung, gemessen, indem die Antwort einer Person als Vorhersage behandelt wurde, lag auf dem Testset bei 77,0 % Exact Match und 86,8 % F1; Abweichungen betrafen meist das Ein- oder Weglassen unwesentlicher Wörter, nicht echte Uneinigkeit (Rajpurkar et al., 2016). Die Metriken sind mit den Überlappungsmaßen der [[text-similarity-metrics|Textähnlichkeitsmetriken]] und mit Precision und Recall der [[classification-metrics|Klassifikationsmetriken]] verwandt.

#### 4. Was die Fragen verlangen

Die Autoren analysierten das nötige Schlussfolgern mit Dependenz- und Konstituentenbäumen ([[dependency-parsing|Dependency Parsing]], [[constituency-parsing|Konstituentenanalyse]]). Ihre Vergleichsbasis mit logistischer Regression hing stark von lexikalischen Merkmalen und Merkmalen entlang von Dependenzpfaden ab, und ihre Leistung sank, je komplexer die Antworttypen wurden und je stärker die Syntax der Frage von der des Antwortsatzes abwich, während die menschliche Leistung nicht sank (Rajpurkar et al., 2016). Eine Sliding-Window-Basis erreichte etwa 20 % F1 (Rajpurkar et al., 2016).

#### 5. SQuAD 2.0: unbeantwortbare Fragen

Extraktive Systeme neigen zu unzuverlässigen Vermutungen, wenn der Absatz die Antwort nicht enthält (Rajpurkar et al., 2018). SQuAD 2.0 verbindet SQuAD 1.1 mit 53.775 neuen unbeantwortbaren Fragen zu denselben Absätzen, von Crowdworkern so geschrieben, dass sie zum Absatz passen und der Absatz eine plausible Antwort des richtigen Typs enthält (Rajpurkar et al., 2018). Systeme müssen antworten, wenn es möglich ist, und sich sonst enthalten; ein führendes Modell erreichte auf SQuAD 2.0 66,3 % F1, Menschen 89,5 %, während dieselbe Architektur auf SQuAD 1.1 85,8 % erreichte (Rajpurkar et al., 2018). Sich zu enthalten, wenn der Kontext die Antwort nicht enthält, ist dieselbe Anforderung wie bei [[retrieval-augmented-generation|RAG]]-Systemen ([[hallucination-detection|Halluzinationserkennung]]).

#### 6. Ergebnisse im Zeitverlauf

Neuronale Modelle übertrafen die Vergleichsbasis bald, etwa mit 70,3 % F1 auf SQuAD 1.1 kurz nach der Veröffentlichung (Rajpurkar et al., 2016). 2019 übertraf [[t5|T5]]-11B das bisher beste Ergebnis auf SQuAD um mehr als einen Punkt Exact Match; die Autorinnen und Autoren wiesen darauf hin, dass die menschliche Leistung auf 82,3 Exact Match und 91,2 F1 geschätzt wird und weitere Verbesserungen daher womöglich wenig aussagen (Raffel et al., 2019).

#### Herkunft und Varianten

SQuAD wurde von Rajpurkar et al. (2016) in Stanford veröffentlicht; SQuAD 2.0 ergänzte unbeantwortbare Fragen (Rajpurkar et al., 2018). Es ist Bestandteil von Multi-Task-Evaluationen wie der in der T5-Untersuchung (Raffel et al., 2019).

### Wann einsetzen

- Um extraktive Fragebeantwortung zu bewerten, bei der die Antwort ein Span einer gegebenen Passage sein muss (Rajpurkar et al., 2016).
- Um mit SQuAD 2.0 zu prüfen, ob ein System sich enthält, wenn die Passage die Antwort nicht enthält (Rajpurkar et al., 2018).
- Als Leseverständnis-Baustein einer breiteren Benchmark-Sammlung (Raffel et al., 2019).

### Stärken und Grenzen

**Stärken**
- Großer, von Menschen geschriebener Datensatz mit klaren, automatischen Metriken (Rajpurkar et al., 2016).
- Die Aufteilung nach Artikeln vermeidet Überschneidungen zwischen Trainings- und Testpassagen (Rajpurkar et al., 2016).
- SQuAD 2.0 prüft das Enthalten mit adversarial geschriebenen unbeantwortbaren Fragen (Rajpurkar et al., 2018).

**Grenzen**
- Span-basierte Antworten sind enger als offene, interpretierende Fragen (Rajpurkar et al., 2016).
- Modelle haben die geschätzte menschliche Leistung erreicht oder übertroffen, was die Aussagekraft weiterer Gewinne begrenzt (Raffel et al., 2019).
- Nur englische Wikipedia, und schon eine merkmalsbasierte Vergleichsbasis hing stark von lexikalischen Merkmalen ab (Rajpurkar et al., 2016).

### Vergleich

| Datensatz | Antwortform | Unbeantwortbare Fragen | Herkunft der Passagen |
|---|---|---|---|
| SQuAD 1.1 | Span im Absatz | nein | 536 Wikipedia-Artikel |
| SQuAD 2.0 | Span oder keine Antwort | 53.775 adversarial | dieselben Absätze |
| [[ms-marco\|MS MARCO]] | von Menschen geschriebene Antworten aus Webpassagen | ja, gelabelt | echte Bing-Anfragen |
| [[glue\|GLUE]] | Labels für Klassifikationsaufgaben | – | verschiedene |
| Multiple-Choice-Lesetests (z. B. MCTest) | Wahl zwischen Optionen | – | – |

Quellen: Rajpurkar et al. (2016); Rajpurkar et al. (2018).

### In der Praxis

Exact Match und F1 gemeinsam berichten und angeben, welche Fassung (1.1 oder 2.0) genutzt wird, da die Werte zwischen den Fassungen nicht vergleichbar sind (Rajpurkar et al., 2018). Bei generativen Modellen müssen Antworten vor dem Exact Match oft vereinheitlicht werden, weil zusätzliche Wörter als Fehler zählen; deshalb ist F1 meist die aussagekräftigere Zahl (Rajpurkar et al., 2016). Leseverständnis ist ein Bestandteil der [[rag-generation-evaluation|Evaluation der RAG-Generierung]], die zusätzlich die Treue zum abgerufenen Kontext prüft.

### Merksatz

SQuAD misst, ob ein System den Antwort-Span zu einer Frage in einem Wikipedia-Absatz findet, und SQuAD 2.0, ob es auch erkennt, wenn es keinen gibt; beide werden mit Exact Match und F1 bewertet.

### Quellen

- Rajpurkar, P., Zhang, J., Lopyrev, K. & Liang, P. (2016). *SQuAD: 100,000+ Questions for Machine Comprehension of Text.* arXiv:1606.05250. [arXiv](https://arxiv.org/abs/1606.05250)
- Rajpurkar, P., Jia, R. & Liang, P. (2018). *Know What You Don't Know: Unanswerable Questions for SQuAD.* arXiv:1806.03822. [arXiv](https://arxiv.org/abs/1806.03822)
- Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W. & Liu, P. J. (2019). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer.* arXiv:1910.10683. [arXiv](https://arxiv.org/abs/1910.10683)
