---
title_en: Text Summarisation
title_de: Automatische Textzusammenfassung
entity_type: Method
aliases:
- Text summarisation
- Text summarization
- Summarisation
- Summarization
- Automatic summarisation
- Abstractive summarisation
- Extractive summarisation
sources:
- https://aclanthology.org/W04-1013/
- https://aclanthology.org/W04-3252/
- https://arxiv.org/abs/1509.00685
- https://arxiv.org/abs/1602.06023
- https://arxiv.org/abs/1704.04368
- https://arxiv.org/abs/1808.08745
- https://arxiv.org/abs/1910.13461
- https://arxiv.org/abs/1912.08777
- https://arxiv.org/abs/2005.00661
- https://arxiv.org/abs/2209.12356
- https://arxiv.org/abs/2301.13848
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Text summarisation produces a shorter text that keeps the important content of one or more documents. Extractive methods select and rearrange sentences from the source; abstractive methods generate new text, which can paraphrase but also invent content (See et al., 2017). The field moved from graph-based sentence extraction such as TextRank (Mihalcea & Tarau, 2004) through neural sequence-to-sequence models (Rush et al., 2015; See et al., 2017) and pre-trained encoder-decoders (Lewis et al., 2020; Zhang et al., 2020) to prompted [[large-language-models|large language models]], whose news summaries humans prefer or rate on par with freelance writers (Goyal et al., 2022; Zhang et al., 2023). Evaluation with ROUGE (Lin, 2004) remains standard, but it cannot reliably judge LLM summaries, and faithfulness to the source is the main open problem (Goyal et al., 2022; Maynez et al., 2020).

### How it works

```text
source document(s)
   │
   ├─ extractive:  score sentences (position, centrality, learned model) ──► pick top sentences ──► reorder
   │
   └─ abstractive: encoder reads source ──► decoder generates summary token by token
                     (attention over source · copy mechanism · pre-training · or a prompted LLM)
   ▼
summary ──► automatic metrics (ROUGE, embedding metrics) + human judgement of faithfulness and quality
```

#### 1. Extractive summarisation

Extractive methods assemble summaries only from passages of the source, which guarantees a basic level of grammaticality and accuracy; most early work was extractive (See et al., 2017). TextRank builds a graph whose vertices are sentences and whose edges are weighted by content overlap, ranks the vertices with a [[pagerank|PageRank]]-style algorithm and picks the highest-ranked sentences, without training data (Mihalcea & Tarau, 2004). For news, the lead-3 baseline (the first three sentences) is strong because articles put the most important information first (See et al., 2017).

#### 2. Neural abstractive summarisation

Rush et al. (2015) generated each word of a sentence summary with a local attention model conditioned on the input. Nallapati et al. (2016) used attentional encoder-decoder recurrent networks with extensions for keywords, sentence hierarchy and rare words, and introduced the multi-sentence CNN/Daily Mail data set; in See et al.'s version it has 287,226 training pairs of news articles (781 tokens on average) and summaries (3.75 sentences on average) (See et al., 2017). Sequence-to-sequence models reproduce factual details inaccurately and repeat themselves; the pointer-generator network lets the model copy words from the source and adds a coverage mechanism against repetition, beating the abstractive state of the art by at least 2 ROUGE points (See et al., 2017).

#### 3. Pre-trained encoder-decoders

BART is pre-trained as a denoising autoencoder, reconstructing text after sentence shuffling and span in-filling, and improved abstractive summarisation by up to 6 ROUGE (Lewis et al., 2020). PEGASUS removes important sentences from a document and generates them from the rest (gap sentence generation); it reached the state of the art on 12 summarisation data sets, surpassed previous results on 6 data sets with only 1,000 training examples, and matched human performance on several data sets in human evaluation (Zhang et al., 2020). [[t5|T5]] treats summarisation as one of its text-to-text tasks.

#### 4. Prompted large language models

Humans overwhelmingly preferred news summaries from GPT-3 prompted with only a task description over those of fine-tuned models, and these summaries avoided dataset-specific problems such as poor factuality (Goyal et al., 2022). Zhang et al. (2023) compared ten LLMs and found that [[instruction-tuning|instruction tuning]], not model size, is the key to zero-shot summarisation; low-quality references had made earlier evaluations underestimate human and few-shot performance, and with high-quality summaries from freelance writers as reference, LLM summaries were judged on par with human ones.

#### 5. Evaluation

ROUGE (Recall-Oriented Understudy for Gisting Evaluation) counts overlapping units between a system summary and human reference summaries: ROUGE-N is n-gram [[classification-metrics|recall]], ROUGE-L uses the longest common subsequence, ROUGE-W a weighted version of it and ROUGE-S skip-bigrams (Lin, 2004). It was introduced because manual evaluation, as in the Document Understanding Conference, would require more than 3,000 hours of human effort (Lin, 2004). Reference-based and reference-free automatic metrics could not reliably evaluate GPT-3 summaries (Goyal et al., 2022), so human judgement and LLM judges complement them ([[text-similarity-metrics|text similarity metrics]], [[llm-as-a-judge|LLM-as-a-judge]]).

#### 6. Faithfulness and hallucination

Maynez et al. (2020) distinguish intrinsic hallucinations, which misrepresent information in the document, from extrinsic ones, which add information that cannot be verified from it. In single-sentence summaries of the XSum data set, hallucinations occurred in more than 70% of summaries, most were extrinsic, and over 90% of the extrinsic ones were erroneous; pre-trained models were best both on ROUGE and on human judgements of faithfulness (Maynez et al., 2020; [[hallucination-detection|hallucination detection]]). XSum itself asks for one-sentence answers to "What is the article about?" over 226,711 BBC articles and does not favour extractive strategies (Narayan et al., 2018).

#### Origin and variants

Variants include single- versus multi-document, generic versus query- or keyword-focused summarisation (Goyal et al., 2022), headline or extreme one-sentence summarisation (Narayan et al., 2018) and long-document summarisation, which depends on the [[context-window|context window]].

### When to use it

- Condensing news, reports, meeting transcripts or support tickets for faster reading.
- Producing snippets or abstracts in search and [[retrieval-augmented-generation|RAG]] systems, including summaries of retrieved passages.
- Compressing conversation history or documents to fit a context window ([[memory-in-llms|memory in LLMs]]).
- Extractive methods where every sentence must be traceable to the source, abstractive or LLM methods where fluency and brevity matter.

### Strengths and limitations

**Strengths**
- Extractive summaries stay grammatical and close to the source (See et al., 2017).
- Pre-trained and prompted models produce fluent summaries and need little task-specific data (Zhang et al., 2020; Goyal et al., 2022).
- LLM summaries reach human quality on news in careful evaluations (Zhang et al., 2023).

**Limitations**
- Abstractive models hallucinate, and many hallucinations are factually wrong (Maynez et al., 2020).
- ROUGE rewards overlap with a reference, not correctness, and fails for LLM outputs (Goyal et al., 2022).
- Reference summaries in benchmarks can be of low quality (Zhang et al., 2023).
- News lead bias makes simple baselines strong and can hide weaknesses (See et al., 2017).

### Comparison

| Approach | Output | Training data | Faithfulness risk |
|---|---|---|---|
| TextRank (extractive) | source sentences | none | low, but may lack coherence |
| Pointer-generator | generated with copying | large paired data | moderate |
| BART / PEGASUS | generated | pre-training + fine-tuning | lower than non-pre-trained models |
| Prompted LLM | generated | instruction tuning | needs checking |

Sources: Mihalcea & Tarau (2004), See et al. (2017), Maynez et al. (2020), Goyal et al. (2022).

### In practice

Summaries used for decisions should be checked for faithfulness to the source, for example by comparing claims with the document or with an LLM judge, since overlap metrics do not detect invented facts (Maynez et al., 2020; Goyal et al., 2022; [[rag-generation-evaluation|generation evaluation]]). Keyword- or query-focused prompts steer what the summary covers (Goyal et al., 2022). When references are used for evaluation, their quality should be checked first (Zhang et al., 2023).

### Key takeaway

Summarisation went from extracting central sentences to generating summaries with pre-trained and prompted models that read as well as human ones; the remaining problems are faithfulness and evaluation beyond ROUGE.

### Sources

- Lin, C.-Y. (2004). *ROUGE: A Package for Automatic Evaluation of Summaries.* Text Summarization Branches Out, ACL 2004 workshop. [aclanthology.org](https://aclanthology.org/W04-1013/)
- Mihalcea, R. & Tarau, P. (2004). *TextRank: Bringing Order into Texts.* EMNLP 2004. [aclanthology.org](https://aclanthology.org/W04-3252/)
- Rush, A. M., Chopra, S. & Weston, J. (2015). *A Neural Attention Model for Abstractive Sentence Summarization.* EMNLP 2015. [arXiv:1509.00685](https://arxiv.org/abs/1509.00685)
- Nallapati, R., Zhou, B., dos Santos, C., Gulcehre, C. & Xiang, B. (2016). *Abstractive Text Summarization Using Sequence-to-Sequence RNNs and Beyond.* CoNLL 2016. [arXiv:1602.06023](https://arxiv.org/abs/1602.06023)
- See, A., Liu, P. J. & Manning, C. D. (2017). *Get To The Point: Summarization with Pointer-Generator Networks.* ACL 2017. [arXiv:1704.04368](https://arxiv.org/abs/1704.04368)
- Narayan, S., Cohen, S. B. & Lapata, M. (2018). *Don't Give Me the Details, Just the Summary! Topic-Aware Convolutional Neural Networks for Extreme Summarization.* EMNLP 2018. [arXiv:1808.08745](https://arxiv.org/abs/1808.08745)
- Lewis, M. et al. (2020). *BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension.* ACL 2020. [arXiv:1910.13461](https://arxiv.org/abs/1910.13461)
- Zhang, J., Zhao, Y., Saleh, M. & Liu, P. J. (2020). *PEGASUS: Pre-training with Extracted Gap-sentences for Abstractive Summarization.* ICML 2020. [arXiv:1912.08777](https://arxiv.org/abs/1912.08777)
- Maynez, J., Narayan, S., Bohnet, B. & McDonald, R. (2020). *On Faithfulness and Factuality in Abstractive Summarization.* ACL 2020. [arXiv:2005.00661](https://arxiv.org/abs/2005.00661)
- Goyal, T., Li, J. J. & Durrett, G. (2022). *News Summarization and Evaluation in the Era of GPT-3.* [arXiv:2209.12356](https://arxiv.org/abs/2209.12356)
- Zhang, T. et al. (2023). *Benchmarking Large Language Models for News Summarization.* [arXiv:2301.13848](https://arxiv.org/abs/2301.13848)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die automatische Textzusammenfassung erzeugt einen kürzeren Text, der den wichtigen Inhalt eines oder mehrerer Dokumente bewahrt. Extraktive Verfahren wählen Sätze aus der Quelle aus und ordnen sie neu; abstraktive Verfahren erzeugen neuen Text, der paraphrasieren, aber auch Inhalte erfinden kann (See et al., 2017). Das Feld entwickelte sich von graphbasierter Satzextraktion wie TextRank (Mihalcea & Tarau, 2004) über neuronale Sequence-to-Sequence-Modelle (Rush et al., 2015; See et al., 2017) und vortrainierte Encoder-Decoder (Lewis et al., 2020; Zhang et al., 2020) zu gepromptenen großen Sprachmodellen, deren Nachrichtenzusammenfassungen Menschen bevorzugen oder als gleichwertig mit denen freiberuflicher Autorinnen und Autoren bewerten (Goyal et al., 2022; Zhang et al., 2023). Die Evaluation mit ROUGE (Lin, 2004) bleibt Standard, kann LLM-Zusammenfassungen aber nicht zuverlässig beurteilen, und die Treue zur Quelle ist das wichtigste offene Problem (Goyal et al., 2022; Maynez et al., 2020).

### Funktionsweise

```text
Quelldokument(e)
   │
   ├─ extraktiv:  Sätze bewerten (Position, Zentralität, gelerntes Modell) ──► beste Sätze wählen ──► ordnen
   │
   └─ abstraktiv: Encoder liest die Quelle ──► Decoder erzeugt die Zusammenfassung Token für Token
                    (Attention auf die Quelle · Kopiermechanismus · Vortraining · oder ein gepromptetes LLM)
   ▼
Zusammenfassung ──► automatische Metriken (ROUGE, Embedding-Metriken) + menschliches Urteil über Treue und Qualität
```

#### 1. Extraktive Zusammenfassung

Extraktive Verfahren setzen Zusammenfassungen nur aus Passagen der Quelle zusammen, was ein Grundmaß an Grammatikalität und Genauigkeit sichert; die meisten frühen Arbeiten waren extraktiv (See et al., 2017). TextRank baut einen Graphen, dessen Knoten Sätze sind und dessen Kanten nach inhaltlicher Überlappung gewichtet werden, ordnet die Knoten mit einem Algorithmus nach dem Vorbild von [[pagerank|PageRank]] und wählt die am höchsten bewerteten Sätze, ohne Trainingsdaten (Mihalcea & Tarau, 2004). Bei Nachrichten ist die Lead-3-Baseline (die ersten drei Sätze) stark, weil Artikel die wichtigste Information an den Anfang stellen (See et al., 2017).

#### 2. Neuronale abstraktive Zusammenfassung

Rush et al. (2015) erzeugten jedes Wort einer Satzzusammenfassung mit einem lokalen Attention-Modell, das auf die Eingabe bedingt ist. Nallapati et al. (2016) nutzten rekurrente Encoder-Decoder-Netze mit Attention und Erweiterungen für Schlüsselwörter, Satzhierarchie und seltene Wörter und führten den Datensatz CNN/Daily Mail mit mehrsätzigen Zusammenfassungen ein; in der Fassung von See et al. umfasst er 287.226 Trainingspaare aus Nachrichtenartikeln (im Mittel 781 Tokens) und Zusammenfassungen (im Mittel 3,75 Sätze) (See et al., 2017). Sequence-to-Sequence-Modelle geben Fakten ungenau wieder und wiederholen sich; das Pointer-Generator-Netz lässt das Modell Wörter aus der Quelle kopieren und ergänzt einen Coverage-Mechanismus gegen Wiederholungen, womit es den abstraktiven Stand der Technik um mindestens 2 ROUGE-Punkte übertraf (See et al., 2017).

#### 3. Vortrainierte Encoder-Decoder

BART wird als Denoising Autoencoder vortrainiert, der Text nach Vertauschen von Sätzen und Auffüllen von Spannen rekonstruiert, und verbesserte die abstraktive Zusammenfassung um bis zu 6 ROUGE (Lewis et al., 2020). PEGASUS entfernt wichtige Sätze aus einem Dokument und erzeugt sie aus dem Rest (Gap Sentence Generation); es erreichte auf 12 Zusammenfassungsdatensätzen den Stand der Technik, übertraf auf 6 Datensätzen mit nur 1.000 Trainingsbeispielen frühere Ergebnisse und erreichte in menschlicher Bewertung auf mehreren Datensätzen menschliche Leistung (Zhang et al., 2020). [[t5|T5]] behandelt Zusammenfassen als eine seiner Text-to-Text-Aufgaben.

#### 4. Gepromptete große Sprachmodelle

Menschen bevorzugten Nachrichtenzusammenfassungen von GPT-3, das nur mit einer Aufgabenbeschreibung gepromptet wurde, mit großer Mehrheit gegenüber denen nachtrainierter Modelle, und diese Zusammenfassungen vermieden datensatzspezifische Probleme wie mangelnde Faktentreue (Goyal et al., 2022). Zhang et al. (2023) verglichen zehn LLMs und fanden, dass [[instruction-tuning|Instruction Tuning]] und nicht die Modellgröße der Schlüssel zum Zero-Shot-Zusammenfassen ist; Referenzen geringer Qualität hatten frühere Evaluationen die menschliche und die Few-Shot-Leistung unterschätzen lassen, und mit hochwertigen Zusammenfassungen freiberuflicher Autorinnen und Autoren als Referenz wurden LLM-Zusammenfassungen als gleichwertig mit menschlichen bewertet.

#### 5. Evaluation

ROUGE (Recall-Oriented Understudy for Gisting Evaluation) zählt überlappende Einheiten zwischen einer Systemzusammenfassung und menschlichen Referenzzusammenfassungen: ROUGE-N ist der N-Gramm-Recall, ROUGE-L nutzt die längste gemeinsame Teilfolge, ROUGE-W eine gewichtete Variante davon und ROUGE-S Skip-Bigramme (Lin, 2004). Es wurde eingeführt, weil eine manuelle Evaluation wie bei der Document Understanding Conference mehr als 3.000 Stunden menschlicher Arbeit erfordern würde (Lin, 2004). Referenzbasierte und referenzfreie automatische Metriken konnten GPT-3-Zusammenfassungen nicht zuverlässig bewerten (Goyal et al., 2022), weshalb menschliches Urteil und LLM-Judges sie ergänzen ([[text-similarity-metrics|Textähnlichkeitsmetriken]], [[llm-as-a-judge|LLM-as-a-Judge]]).

#### 6. Treue und Halluzination

Maynez et al. (2020) unterscheiden intrinsische Halluzinationen, die Information aus dem Dokument falsch darstellen, von extrinsischen, die Information hinzufügen, die sich aus ihm nicht prüfen lässt. In einsätzigen Zusammenfassungen des Datensatzes XSum traten Halluzinationen in mehr als 70 % der Zusammenfassungen auf, die meisten waren extrinsisch, und über 90 % der extrinsischen waren falsch; vortrainierte Modelle schnitten sowohl bei ROUGE als auch im menschlichen Urteil über Treue am besten ab (Maynez et al., 2020; [[hallucination-detection|Halluzinationserkennung]]). XSum selbst verlangt einsätzige Antworten auf „Worum geht es im Artikel?“ über 226.711 BBC-Artikel und begünstigt keine extraktiven Strategien (Narayan et al., 2018).

#### Ursprung und Varianten

Zu den Varianten gehören Einzel- und Mehrdokument-Zusammenfassung, generische sowie anfrage- oder schlüsselwortbezogene Zusammenfassung (Goyal et al., 2022), Schlagzeilen- oder extreme Einsatzzusammenfassung (Narayan et al., 2018) und die Zusammenfassung langer Dokumente, die vom [[context-window|Kontextfenster]] abhängt.

### Wann einsetzen

- Nachrichten, Berichte, Besprechungsprotokolle oder Support-Tickets für schnelleres Lesen verdichten.
- Snippets oder Abstracts in Such- und [[retrieval-augmented-generation|RAG]]-Systemen erzeugen, auch Zusammenfassungen abgerufener Passagen.
- Gesprächsverlauf oder Dokumente verdichten, damit sie in ein Kontextfenster passen ([[memory-in-llms|Gedächtnis in LLMs]]).
- Extraktive Verfahren, wo jeder Satz auf die Quelle zurückführbar sein muss, abstraktive oder LLM-Verfahren, wo Lesbarkeit und Kürze zählen.

### Stärken und Grenzen

**Stärken**
- Extraktive Zusammenfassungen bleiben grammatisch und nah an der Quelle (See et al., 2017).
- Vortrainierte und gepromptete Modelle liefern flüssige Zusammenfassungen und brauchen wenige aufgabenspezifische Daten (Zhang et al., 2020; Goyal et al., 2022).
- LLM-Zusammenfassungen erreichen bei Nachrichten in sorgfältigen Evaluationen menschliche Qualität (Zhang et al., 2023).

**Grenzen**
- Abstraktive Modelle halluzinieren, und viele Halluzinationen sind sachlich falsch (Maynez et al., 2020).
- ROUGE belohnt Überlappung mit einer Referenz, nicht Richtigkeit, und versagt bei LLM-Ausgaben (Goyal et al., 2022).
- Referenzzusammenfassungen in Benchmarks können von geringer Qualität sein (Zhang et al., 2023).
- Der Lead-Bias von Nachrichten macht einfache Baselines stark und kann Schwächen verdecken (See et al., 2017).

### Vergleich

| Ansatz | Ausgabe | Trainingsdaten | Risiko für die Treue |
|---|---|---|---|
| TextRank (extraktiv) | Sätze der Quelle | keine | gering, aber evtl. wenig zusammenhängend |
| Pointer-Generator | generiert mit Kopieren | viele Paare | mittel |
| BART / PEGASUS | generiert | Vortraining + Fine-Tuning | geringer als bei nicht vortrainierten Modellen |
| Gepromptetes LLM | generiert | Instruction Tuning | muss geprüft werden |

Quellen: Mihalcea & Tarau (2004), See et al. (2017), Maynez et al. (2020), Goyal et al. (2022).

### In der Praxis

Zusammenfassungen, auf die sich Entscheidungen stützen, sollten auf ihre Treue zur Quelle geprüft werden, etwa durch Abgleich der Aussagen mit dem Dokument oder mit einem LLM-Judge, da Überlappungsmetriken erfundene Fakten nicht erkennen (Maynez et al., 2020; Goyal et al., 2022; [[rag-generation-evaluation|Generierungs-Evaluation]]). Schlüsselwort- oder anfragebezogene Prompts steuern, was die Zusammenfassung abdeckt (Goyal et al., 2022). Werden Referenzen zur Evaluation genutzt, sollte zuerst ihre Qualität geprüft werden (Zhang et al., 2023).

### Merksatz

Die Textzusammenfassung entwickelte sich vom Extrahieren zentraler Sätze zum Generieren mit vortrainierten und gepromptenen Modellen, deren Ergebnisse sich wie menschliche lesen; offen bleiben Treue zur Quelle und Evaluation jenseits von ROUGE.

### Quellen

- Lin, C.-Y. (2004). *ROUGE: A Package for Automatic Evaluation of Summaries.* Text Summarization Branches Out, Workshop der ACL 2004. [aclanthology.org](https://aclanthology.org/W04-1013/)
- Mihalcea, R. & Tarau, P. (2004). *TextRank: Bringing Order into Texts.* EMNLP 2004. [aclanthology.org](https://aclanthology.org/W04-3252/)
- Rush, A. M., Chopra, S. & Weston, J. (2015). *A Neural Attention Model for Abstractive Sentence Summarization.* EMNLP 2015. [arXiv:1509.00685](https://arxiv.org/abs/1509.00685)
- Nallapati, R., Zhou, B., dos Santos, C., Gulcehre, C. & Xiang, B. (2016). *Abstractive Text Summarization Using Sequence-to-Sequence RNNs and Beyond.* CoNLL 2016. [arXiv:1602.06023](https://arxiv.org/abs/1602.06023)
- See, A., Liu, P. J. & Manning, C. D. (2017). *Get To The Point: Summarization with Pointer-Generator Networks.* ACL 2017. [arXiv:1704.04368](https://arxiv.org/abs/1704.04368)
- Narayan, S., Cohen, S. B. & Lapata, M. (2018). *Don't Give Me the Details, Just the Summary! Topic-Aware Convolutional Neural Networks for Extreme Summarization.* EMNLP 2018. [arXiv:1808.08745](https://arxiv.org/abs/1808.08745)
- Lewis, M. et al. (2020). *BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension.* ACL 2020. [arXiv:1910.13461](https://arxiv.org/abs/1910.13461)
- Zhang, J., Zhao, Y., Saleh, M. & Liu, P. J. (2020). *PEGASUS: Pre-training with Extracted Gap-sentences for Abstractive Summarization.* ICML 2020. [arXiv:1912.08777](https://arxiv.org/abs/1912.08777)
- Maynez, J., Narayan, S., Bohnet, B. & McDonald, R. (2020). *On Faithfulness and Factuality in Abstractive Summarization.* ACL 2020. [arXiv:2005.00661](https://arxiv.org/abs/2005.00661)
- Goyal, T., Li, J. J. & Durrett, G. (2022). *News Summarization and Evaluation in the Era of GPT-3.* [arXiv:2209.12356](https://arxiv.org/abs/2209.12356)
- Zhang, T. et al. (2023). *Benchmarking Large Language Models for News Summarization.* [arXiv:2301.13848](https://arxiv.org/abs/2301.13848)
