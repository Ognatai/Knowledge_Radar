---
title_en: Natural Language Inference
title_de: Natural Language Inference
entity_type: Method
aliases:
- Natural language inference (NLI)
- NLI
- Recognising textual entailment
- Recognizing Textual Entailment
- RTE
- Textual entailment
sources:
- https://arxiv.org/abs/1508.05326
- https://arxiv.org/abs/1704.05426
- https://arxiv.org/abs/1803.02324
- https://arxiv.org/abs/2204.04991
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Natural language inference (NLI), also known as recognising textual entailment, is the task of deciding for a pair of sentences, a premise and a hypothesis, whether the premise entails the hypothesis, contradicts it or neither, which is labelled neutral (Williams et al., 2018). The large crowdsourced corpora SNLI, with 570,152 sentence pairs, and MultiNLI, with 433k pairs from ten genres, made it possible to train neural models on the task (Bowman et al., 2015; Williams et al., 2018). Hypotheses written by crowdworkers leave clues: a classifier that sees only the hypothesis labels about 67% of SNLI correctly (Gururangan et al., 2018). NLI models are also used to check whether generated text is consistent with its source, with the source as premise and the generated text as hypothesis (Honovich et al., 2022).

### How it works

```text
premise (source text)  +  hypothesis (claim)
 ▼
NLI model: classifier over the sentence pair
 ▼
entailment · neutral · contradiction (with probabilities)
 ▼
uses: benchmark for sentence understanding · training sentence embeddings
      · factual consistency check (source = premise, generated text = hypothesis)
```

#### 1. Task and labels

A model is presented with a pair of sentences and judges the relationship between their meanings by picking a label from a small set, typically entailment, neutral and contradiction. Solving the task requires no hard machine learning problem other than representing the meaning of sentences well: a model must handle lexical entailment, quantification, coreference, tense, belief, modality and lexical and syntactic ambiguity (Williams et al., 2018). Entailment and contradiction are central to natural language meaning, which makes NLI relevant to tasks ranging from [[information-retrieval|information retrieval]] to semantic parsing and commonsense reasoning (Bowman et al., 2015). Technically, NLI is a three-class [[classification|classification]] of sentence pairs.

#### 2. SNLI

Before 2015, the main NLI data came from the Recognizing Textual Entailment (RTE) challenges, whose high-quality data sets had fewer than a thousand examples each; the SemEval 2014 SICK data had 4,500 training examples (Bowman et al., 2015). For the Stanford Natural Language Inference corpus (SNLI), workers on Amazon Mechanical Turk received image captions from the Flickr30k corpus as premises, without the images, and wrote one hypothesis for each of the three labels, which balances the classes. Because premise and hypothesis describe the same scene, the corpus avoids much of the uncertainty about whether two sentences refer to the same event or entity. In a validation phase, 56,951 pairs were labelled by four further annotators; the gold label is the label chosen by at least three of the five, no such majority existed for 2.0% of the pairs, and Fleiss' κ was 0.70 overall. With 570,152 pairs, SNLI was two orders of magnitude larger than all earlier resources of its type. A lexicalised classifier reached 78.2% and an [[recurrent-neural-networks|LSTM]] sentence-embedding model 77.6% three-class test accuracy (Bowman et al., 2015).

#### 3. MultiNLI

SNLI's premises come from a single genre, image captions, so its hypotheses are short and simple. The Multi-Genre NLI corpus (MultiNLI) uses the same collection method with premises from ten genres of written and spoken American English: face-to-face conversations, government documents, letters, the 9/11 Commission report, non-fiction books from Oxford University Press, Slate magazine articles, telephone conversations, travel guides, Verbatim posts about linguistics and fiction. Only five genres are in the training set, so the matched test set measures performance within the training domains and the mismatched test set performance on unseen genres. Premises are longer than in SNLI, with a mean of 22.3 words against 14.1. The baseline models were about 15 percentage points worse on MultiNLI than on SNLI; trained on MultiNLI, only ESIM exceeded 70%, with 72.3% matched and 72.1% mismatched test accuracy (Williams et al., 2018).

#### 4. Annotation artefacts

Because crowdworkers wrote one hypothesis per label for each premise, the hypotheses themselves carry clues to the label. A simple text classifier that sees only the hypothesis labels about 67% of SNLI and 53% of MultiNLI correctly; negation and vagueness are strongly correlated with particular classes. The authors conclude that progress on NLI has been overestimated and that the task remains a hard open problem (Gururangan et al., 2018).

#### 5. NLI for factual consistency

Generated text is often inconsistent with the input it is conditioned on. TRUE standardised 11 data sets from summarisation, dialogue, fact verification and paraphrasing to binary labels for factual consistency and evaluated metrics per example with ROC AUC (Honovich et al., 2022). An NLI model built by fine-tuning T5-11B on the Adversarial NLI data set takes the grounding text as premise and the generated text as hypothesis and uses the entailment probability as the consistency score. It reached an average ROC AUC of 81.5; NLI-based models were best on 6 data sets, and Q², which generates questions and compares the answers with an NLI model, reached 80.7. Averaging Q², the ANLI model and the NLI-based summarisation metric SummaC raised the best single result by 4.5 ROC AUC (Honovich et al., 2022).

#### Origin and variants

NLI continues the textual entailment work of the RTE challenges (Bowman et al., 2015). SNLI made neural models competitive on the task for the first time (Bowman et al., 2015), MultiNLI extended it to many genres and to evaluation on unseen genres (Williams et al., 2018), and the discovery of annotation artefacts showed the limits of crowdsourced hypotheses (Gururangan et al., 2018). The task resembles factual consistency evaluation, which has led to NLI models being used to measure it (Honovich et al., 2022).

### When to use it

- Testing whether a model represents sentence meaning, including on genres not seen in training (Williams et al., 2018).
- Training sentence representations: SNLI is large enough to train neural sentence-embedding models (Bowman et al., 2015), as [[sentence-bert|Sentence-BERT]] later did.
- Checking whether generated text is supported by its source, for example in [[hallucination-detection|hallucination detection]] and [[rag-generation-evaluation|RAG generation evaluation]] (Honovich et al., 2022).

### Strengths and limitations

**Strengths**
- Large, human-written and human-validated corpora with reasonable inter-annotator agreement (Bowman et al., 2015; Williams et al., 2018).
- An NLI-based consistency score works across tasks: all three best metrics in TRUE averaged above 80 ROC AUC on the 11 data sets (Honovich et al., 2022).

**Limitations**
- Annotation artefacts let models score well from the hypothesis alone, so benchmark results overstate understanding (Gururangan et al., 2018).
- Models trained on one corpus transfer poorly: the LSTM trained on SNLI failed on SICK and labelled more neutral examples as contradictions than correctly (Bowman et al., 2015).
- As consistency checks, all metrics degrade for grounding texts longer than 200 tokens, and the best metrics missed subtle inconsistencies in 21 of 180 analysed examples (Honovich et al., 2022).

### Comparison

| Data set | Premises | Size |
|----------|----------|------|
| RTE challenges | Various, hand-labelled | Fewer than 1,000 examples each |
| SICK (SemEval 2014) | Partly automatic construction | 4,500 training examples |
| SNLI | Flickr30k image captions | 570,152 sentence pairs |
| MultiNLI | Ten genres of written and spoken English | 433k sentence pairs |

Sources: Bowman et al. (2015); Williams et al. (2018).

### In practice

For a consistency check, the source or retrieved passage is the premise and the generated text the hypothesis; the entailment probability serves as the score (Honovich et al., 2022). NLI and question answering models may struggle with long inputs; SummaC splits document and summary into sentences and scores every pair of document and summary sentence. Aggregating scores over parts of a text can hide a small inconsistency; taking the minimum instead of the average catches more of them at the cost of more false negatives. Combining NLI with question-generation-based checks gives better results than either alone (Honovich et al., 2022). An [[llm-as-a-judge|LLM as a judge]] is an alternative for the same verification step.

### Key takeaway

NLI classifies a sentence pair as entailment, contradiction or neutral; large crowdsourced corpora made it a standard benchmark, annotation artefacts limit what scores on them mean, and NLI models are a strong, cheap check of whether generated text is supported by its source.

### Sources

- Bowman, S. R., Angeli, G., Potts, C. & Manning, C. D. (2015). *A large annotated corpus for learning natural language inference.* EMNLP 2015. [arXiv:1508.05326](https://arxiv.org/abs/1508.05326)
- Williams, A., Nangia, N. & Bowman, S. R. (2018). *A Broad-Coverage Challenge Corpus for Sentence Understanding through Inference.* NAACL 2018. [arXiv:1704.05426](https://arxiv.org/abs/1704.05426)
- Gururangan, S., Swayamdipta, S., Levy, O., Schwartz, R., Bowman, S. R. & Smith, N. A. (2018). *Annotation Artifacts in Natural Language Inference Data.* NAACL 2018. [arXiv:1803.02324](https://arxiv.org/abs/1803.02324)
- Honovich, O. et al. (2022). *TRUE: Re-evaluating Factual Consistency Evaluation.* NAACL 2022. [arXiv:2204.04991](https://arxiv.org/abs/2204.04991)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Natural Language Inference (NLI), auch Recognizing Textual Entailment genannt, ist die Aufgabe, für ein Satzpaar aus Prämisse und Hypothese zu entscheiden, ob die Prämisse die Hypothese impliziert (Entailment), ihr widerspricht (Contradiction) oder keins von beiden gilt (Neutral) (Williams et al., 2018). Die großen per Crowdsourcing erstellten Korpora SNLI mit 570.152 Satzpaaren und MultiNLI mit 433.000 Paaren aus zehn Genres machten es möglich, neuronale Modelle für die Aufgabe zu trainieren (Bowman et al., 2015; Williams et al., 2018). Von Crowdworkern geschriebene Hypothesen enthalten Hinweise auf das Label: Ein Klassifikator, der nur die Hypothese sieht, ordnet etwa 67 % von SNLI richtig zu (Gururangan et al., 2018). NLI-Modelle prüfen auch, ob generierter Text mit seiner Quelle übereinstimmt, mit der Quelle als Prämisse und dem generierten Text als Hypothese (Honovich et al., 2022).

### Funktionsweise

```text
Prämisse (Quelltext)  +  Hypothese (Aussage)
 ▼
NLI-Modell: Klassifikator über das Satzpaar
 ▼
Entailment · Neutral · Contradiction (mit Wahrscheinlichkeiten)
 ▼
Einsatz: Benchmark für Satzverständnis · Training von Satz-Embeddings
         · Prüfung der faktischen Konsistenz (Quelle = Prämisse, generierter Text = Hypothese)
```

#### 1. Aufgabe und Labels

Ein Modell erhält ein Satzpaar und beurteilt die Beziehung zwischen den Bedeutungen der beiden Sätze, indem es ein Label aus einer kleinen Menge wählt, typischerweise Entailment, Neutral und Contradiction. Die Aufgabe verlangt kein schwieriges Problem des maschinellen Lernens außer einer guten Repräsentation der Satzbedeutung: Ein Modell muss lexikalische Implikation, Quantifizierung, Koreferenz, Tempus, Überzeugungen, Modalität sowie lexikalische und syntaktische Mehrdeutigkeit verarbeiten (Williams et al., 2018). Implikation und Widerspruch sind zentral für die Bedeutung natürlicher Sprache, weshalb NLI für Aufgaben vom [[information-retrieval|Information Retrieval]] über semantisches Parsing bis zum Alltagsschließen relevant ist (Bowman et al., 2015). Technisch ist NLI eine [[classification|Klassifikation]] von Satzpaaren in drei Klassen.

#### 2. SNLI

Vor 2015 stammten die wichtigsten NLI-Daten aus den Recognizing-Textual-Entailment-Challenges (RTE), deren hochwertige Datensätze jeweils weniger als tausend Beispiele hatten; die SICK-Daten von SemEval 2014 hatten 4.500 Trainingsbeispiele (Bowman et al., 2015). Für das Stanford Natural Language Inference Corpus (SNLI) erhielten Crowdworker auf Amazon Mechanical Turk Bildbeschreibungen aus dem Flickr30k-Korpus als Prämissen, ohne die Bilder, und schrieben zu jedem der drei Labels eine Hypothese, wodurch die Klassen ausgeglichen sind. Da Prämisse und Hypothese dieselbe Szene beschreiben, vermeidet das Korpus einen Großteil der Unsicherheit darüber, ob sich zwei Sätze auf dasselbe Ereignis oder dieselbe Entität beziehen. In einer Validierungsphase wurden 56.951 Paare von vier weiteren Annotierenden gelabelt; das Gold-Label ist das Label, das mindestens drei der fünf wählten, für 2,0 % der Paare gab es keine solche Mehrheit, und Fleiss' κ lag insgesamt bei 0,70. Mit 570.152 Paaren war SNLI zwei Größenordnungen größer als alle früheren Ressourcen dieser Art. Ein lexikalisierter Klassifikator erreichte 78,2 % und ein [[recurrent-neural-networks|LSTM]]-Modell mit Satz-Embeddings 77,6 % Genauigkeit auf dem Testset mit drei Klassen (Bowman et al., 2015).

#### 3. MultiNLI

Die Prämissen von SNLI stammen aus einem einzigen Genre, Bildbeschreibungen, sodass seine Hypothesen kurz und einfach sind. Das Multi-Genre NLI Corpus (MultiNLI) verwendet dasselbe Erhebungsverfahren mit Prämissen aus zehn Genres des geschriebenen und gesprochenen amerikanischen Englisch: persönliche Gespräche, Regierungsdokumente, Briefe, der Bericht der 9/11-Kommission, Sachbücher von Oxford University Press, Artikel des Magazins Slate, Telefongespräche, Reiseführer, Verbatim-Beiträge über Linguistik und Belletristik. Nur fünf Genres sind im Trainingsset, sodass das Matched-Testset die Leistung innerhalb der Trainingsdomänen und das Mismatched-Testset die Leistung auf ungesehenen Genres misst. Die Prämissen sind länger als in SNLI, im Mittel 22,3 gegenüber 14,1 Wörtern. Die Baseline-Modelle waren auf MultiNLI etwa 15 Prozentpunkte schlechter als auf SNLI; mit Training auf MultiNLI übertraf nur ESIM 70 %, mit 72,3 % Matched- und 72,1 % Mismatched-Genauigkeit auf dem Testset (Williams et al., 2018).

#### 4. Annotationsartefakte

Da Crowdworker zu jeder Prämisse eine Hypothese pro Label schrieben, tragen die Hypothesen selbst Hinweise auf das Label. Ein einfacher Textklassifikator, der nur die Hypothese sieht, ordnet etwa 67 % von SNLI und 53 % von MultiNLI richtig zu; Negation und Vagheit hängen stark mit bestimmten Klassen zusammen. Die Autoren folgern, dass der Fortschritt bei NLI überschätzt wurde und die Aufgabe ein schwieriges offenes Problem bleibt (Gururangan et al., 2018).

#### 5. NLI für faktische Konsistenz

Generierter Text stimmt oft nicht mit der Eingabe überein, auf der er beruht. TRUE vereinheitlichte 11 Datensätze aus Zusammenfassung, Dialog, Faktenprüfung und Paraphrasierung zu binären Labels für faktische Konsistenz und bewertete Metriken pro Beispiel mit ROC AUC (Honovich et al., 2022). Ein NLI-Modell, für das T5-11B auf dem Datensatz Adversarial NLI feinabgestimmt wurde, nimmt den Quelltext als Prämisse und den generierten Text als Hypothese und verwendet die Entailment-Wahrscheinlichkeit als Konsistenzwert. Es erreichte im Mittel einen ROC AUC von 81,5; NLI-basierte Modelle waren auf 6 Datensätzen am besten, und Q², das Fragen generiert und die Antworten mit einem NLI-Modell vergleicht, erreichte 80,7. Der Mittelwert aus Q², dem ANLI-Modell und der NLI-basierten Zusammenfassungsmetrik SummaC verbesserte das beste Einzelergebnis um 4,5 ROC AUC (Honovich et al., 2022).

#### Herkunft und Varianten

NLI setzt die Arbeiten zu Textual Entailment aus den RTE-Challenges fort (Bowman et al., 2015). SNLI machte neuronale Modelle erstmals konkurrenzfähig für die Aufgabe (Bowman et al., 2015), MultiNLI erweiterte sie auf viele Genres und auf die Bewertung mit ungesehenen Genres (Williams et al., 2018), und die Entdeckung der Annotationsartefakte zeigte die Grenzen von per Crowdsourcing geschriebenen Hypothesen (Gururangan et al., 2018). Die Aufgabe ähnelt der Bewertung faktischer Konsistenz, weshalb NLI-Modelle zu deren Messung eingesetzt werden (Honovich et al., 2022).

### Wann einsetzen

- Prüfen, ob ein Modell Satzbedeutung repräsentiert, auch für Genres, die im Training nicht vorkamen (Williams et al., 2018).
- Training von Satzrepräsentationen: SNLI ist groß genug, um neuronale Modelle für Satz-Embeddings zu trainieren (Bowman et al., 2015), wie es später [[sentence-bert|Sentence-BERT]] tat.
- Prüfen, ob generierter Text von seiner Quelle gestützt wird, etwa bei der [[hallucination-detection|Halluzinationserkennung]] und der [[rag-generation-evaluation|Evaluation der RAG-Generierung]] (Honovich et al., 2022).

### Stärken und Grenzen

**Stärken**
- Große, von Menschen geschriebene und validierte Korpora mit ordentlicher Übereinstimmung zwischen Annotierenden (Bowman et al., 2015; Williams et al., 2018).
- Ein NLI-basierter Konsistenzwert funktioniert aufgabenübergreifend: Alle drei besten Metriken in TRUE lagen auf den 11 Datensätzen im Mittel über 80 ROC AUC (Honovich et al., 2022).

**Grenzen**
- Annotationsartefakte erlauben gute Ergebnisse allein anhand der Hypothese, sodass Benchmark-Ergebnisse das Verständnis überschätzen (Gururangan et al., 2018).
- Auf einem Korpus trainierte Modelle übertragen sich schlecht: Das auf SNLI trainierte LSTM versagte auf SICK und ordnete mehr neutrale Beispiele als Widerspruch ein als richtig (Bowman et al., 2015).
- Als Konsistenzprüfung verschlechtern sich alle Metriken für Quelltexte mit mehr als 200 Tokens, und die besten Metriken übersahen subtile Inkonsistenzen in 21 von 180 analysierten Beispielen (Honovich et al., 2022).

### Vergleich

| Datensatz | Prämissen | Größe |
|-----------|-----------|-------|
| RTE-Challenges | Verschieden, von Hand gelabelt | Jeweils weniger als 1.000 Beispiele |
| SICK (SemEval 2014) | Teilweise automatisch erstellt | 4.500 Trainingsbeispiele |
| SNLI | Bildbeschreibungen aus Flickr30k | 570.152 Satzpaare |
| MultiNLI | Zehn Genres geschriebenen und gesprochenen Englischs | 433.000 Satzpaare |

Quellen: Bowman et al. (2015); Williams et al. (2018).

### In der Praxis

Für eine Konsistenzprüfung ist die Quelle oder die abgerufene Passage die Prämisse und der generierte Text die Hypothese; die Entailment-Wahrscheinlichkeit dient als Wert (Honovich et al., 2022). NLI- und Question-Answering-Modelle können mit langen Eingaben Schwierigkeiten haben; SummaC zerlegt Dokument und Zusammenfassung in Sätze und bewertet jedes Paar aus Dokument- und Zusammenfassungssatz. Werte über Teile eines Textes zu aggregieren kann eine kleine Inkonsistenz verdecken; das Minimum statt des Mittelwerts erfasst mehr davon, um den Preis von mehr falsch Negativen. Die Kombination von NLI mit Prüfungen über generierte Fragen liefert bessere Ergebnisse als jedes Verfahren allein (Honovich et al., 2022). Ein [[llm-as-a-judge|LLM als Bewerter]] ist eine Alternative für denselben Prüfschritt.

### Merksatz

NLI ordnet ein Satzpaar als Entailment, Contradiction oder Neutral ein; große per Crowdsourcing erstellte Korpora machten die Aufgabe zum Standard-Benchmark, Annotationsartefakte begrenzen die Aussagekraft der Ergebnisse darauf, und NLI-Modelle sind eine starke, günstige Prüfung, ob generierter Text von seiner Quelle gestützt wird.

### Quellen

- Bowman, S. R., Angeli, G., Potts, C. & Manning, C. D. (2015). *A large annotated corpus for learning natural language inference.* EMNLP 2015. [arXiv:1508.05326](https://arxiv.org/abs/1508.05326)
- Williams, A., Nangia, N. & Bowman, S. R. (2018). *A Broad-Coverage Challenge Corpus for Sentence Understanding through Inference.* NAACL 2018. [arXiv:1704.05426](https://arxiv.org/abs/1704.05426)
- Gururangan, S., Swayamdipta, S., Levy, O., Schwartz, R., Bowman, S. R. & Smith, N. A. (2018). *Annotation Artifacts in Natural Language Inference Data.* NAACL 2018. [arXiv:1803.02324](https://arxiv.org/abs/1803.02324)
- Honovich, O. et al. (2022). *TRUE: Re-evaluating Factual Consistency Evaluation.* NAACL 2022. [arXiv:2204.04991](https://arxiv.org/abs/2204.04991)
