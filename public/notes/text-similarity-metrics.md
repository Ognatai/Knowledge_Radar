---
title_en: Text Similarity Metrics
title_de: Textähnlichkeitsmetriken
entity_type: Concept
sources:
- https://aclanthology.org/P02-1040/
- https://aclanthology.org/W04-1013/
- https://arxiv.org/abs/1904.09675
- https://arxiv.org/abs/1908.10084
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Text similarity metrics score how close a candidate text is to a reference or to another text. Lexical metrics such as BLEU (Papineni et al., 2002) and ROUGE (Lin, 2004) count overlapping n-grams. Embedding-based methods compare learned representations instead: BERTScore matches tokens via contextual embeddings (Zhang et al., 2019), and Sentence-BERT compares whole sentences by the cosine similarity of their [[embeddings|Embeddings]] (Reimers & Gurevych, 2019).

### How it works

The candidate text is compared with one or more references, either by counting shared word sequences or by comparing vector representations of tokens or sentences. The result is a score that can be averaged over a test set.

```text
1. BLEU: clipped n-gram precision
▼
2. ROUGE: recall-oriented overlap
▼
3. BERTScore: token similarity with contextual embeddings
▼
4. Sentence embeddings with cosine similarity
```

#### 1. BLEU

BLEU (Papineni et al., 2002) scores a candidate translation against one or more reference translations. For n-grams up to length four it computes a modified n-gram precision: each candidate n-gram is counted at most as often as it occurs in a reference (clipping), so repeating a correct word does not inflate the score. The precisions are combined by a geometric mean and multiplied by a brevity penalty for candidates shorter than the references, since precision alone would reward very short outputs. BLEU was shown to correlate with human judgements at corpus level.

#### 2. ROUGE

ROUGE (Lin, 2004) evaluates summaries by their overlap with reference summaries and is recall-oriented, i.e. it asks how much of the reference content the candidate covers. Its variants differ in what counts as overlap: ROUGE-N uses n-grams, ROUGE-L the longest common subsequence, ROUGE-W a weighted longest common subsequence that favours consecutive matches, and ROUGE-S skip-bigrams, i.e. pairs of words in sentence order with arbitrary gaps between them.

#### 3. BERTScore

BERTScore (Zhang et al., 2019) computes a similarity score for each token in the candidate with each token in the reference, but instead of exact matches it uses contextual embeddings, so different words with similar meaning in context can still match. Evaluated on the outputs of 363 machine translation and image captioning systems, BERTScore correlated better with human judgements and gave stronger model selection than existing metrics, and on an adversarial paraphrase detection task it was more robust to challenging examples (Zhang et al., 2019).

#### 4. Sentence embeddings with cosine similarity

BERT can score sentence pairs well, but both sentences have to be fed into the network together. Finding the most similar pair in a collection of 10,000 sentences therefore needs about 50 million inference computations, roughly 65 hours (Reimers & Gurevych, 2019). Sentence-BERT modifies BERT with siamese and triplet network structures so that each sentence is encoded once into an embedding, and embeddings are compared with cosine similarity. This reduces the search from 65 hours to about 5 seconds while maintaining BERT's accuracy, and makes semantic similarity search and clustering practical ([[vector-databases|Vector Databases]]).

#### Origin and variants

BLEU (Papineni et al., 2002) was developed for machine translation and ROUGE (Lin, 2004) for summarization. In 2019, BERTScore (Zhang et al., 2019) brought contextual embeddings into evaluation metrics, and Sentence-BERT (Reimers & Gurevych, 2019) made sentence embeddings efficient enough for similarity search over large collections.

### When to use it

- When machine translation output is evaluated against reference translations at corpus level (Papineni et al., 2002).
- When summaries are evaluated by how much of the reference content they cover (Lin, 2004).
- When paraphrases with different wording should still count as matches, embedding-based metrics are a better fit than exact n-gram overlap (Zhang et al., 2019).
- When many texts have to be compared with each other, for example in semantic search or clustering, sentence embeddings avoid scoring every pair with the full model (Reimers & Gurevych, 2019).

### Strengths and limitations

**Strengths**
- BLEU and ROUGE are cheap, transparent and need only reference texts (Papineni et al., 2002; Lin, 2004).
- BLEU correlates with human judgements at corpus level (Papineni et al., 2002).
- BERTScore correlates better with human judgements than earlier metrics and is more robust to adversarial paraphrases (Zhang et al., 2019).

**Limitations**
- Lexical metrics only count exact overlaps, so correct paraphrases score low (Zhang et al., 2019).
- The correlation of BLEU with human judgements was shown at corpus level, not for single sentences (Papineni et al., 2002).
- Scoring every sentence pair with BERT is impractical for large collections (Reimers & Gurevych, 2019).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| BLEU | Clipped n-gram precision up to length four with brevity penalty (Papineni et al., 2002) | Machine translation at corpus level |
| ROUGE | Recall-oriented overlap of n-grams, subsequences or skip-bigrams (Lin, 2004) | Summarization |
| BERTScore | Token similarity via contextual embeddings instead of exact matches (Zhang et al., 2019) | Evaluating generated text with paraphrases |
| Sentence-BERT | One embedding per sentence, compared with cosine similarity (Reimers & Gurevych, 2019) | Semantic search, clustering, sentence similarity |

### In practice

Metric scores are usually reported as averages over a test set and are compared with human judgements before being trusted for a new task (Papineni et al., 2002; Zhang et al., 2019). For RAG answers and other generated text, lexical and embedding-based metrics are complemented by task-specific checks such as faithfulness to the retrieved context ([[rag-generation-evaluation|RAG: Generation Evaluation]]) or by LLM judges ([[llm-as-a-judge|LLM-as-a-Judge]]). For retrieval and clustering, sentence embeddings are computed once and stored, so that comparisons reduce to cheap cosine similarities (Reimers & Gurevych, 2019).

### Key takeaway

Lexical metrics such as BLEU and ROUGE measure word overlap cheaply, while embedding-based methods such as BERTScore and Sentence-BERT also recognise paraphrases.

### Sources

- Papineni, K., Roukos, S., Ward, T. & Zhu, W.-J. (2002). *BLEU: a Method for Automatic Evaluation of Machine Translation.* ACL 2002. [ACL Anthology](https://aclanthology.org/P02-1040/)
- Lin, C.-Y. (2004). *ROUGE: A Package for Automatic Evaluation of Summaries.* Text Summarization Branches Out, ACL Workshop. [ACL Anthology](https://aclanthology.org/W04-1013/)
- Zhang, T. et al. (2019). *BERTScore: Evaluating Text Generation with BERT.* ICLR 2020. [arXiv:1904.09675](https://arxiv.org/abs/1904.09675)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Textähnlichkeitsmetriken bewerten, wie nahe ein Kandidatentext an einem Referenztext oder an einem anderen Text liegt. Lexikalische Metriken wie BLEU (Papineni et al., 2002) und ROUGE (Lin, 2004) zählen übereinstimmende n-Gramme. Embedding-basierte Methoden vergleichen stattdessen gelernte Repräsentationen: BERTScore ordnet Token über kontextuelle Embeddings einander zu (Zhang et al., 2019), und Sentence-BERT vergleicht ganze Sätze über die Kosinusähnlichkeit ihrer [[embeddings|Embeddings]] (Reimers & Gurevych, 2019).

### Funktionsweise

Der Kandidatentext wird mit einem oder mehreren Referenztexten verglichen, entweder durch Zählen gemeinsamer Wortfolgen oder durch Vergleich der Vektorrepräsentationen von Token oder Sätzen. Das Ergebnis ist ein Wert, der über einen Testdatensatz gemittelt werden kann.

```text
1. BLEU: n-Gramm-Präzision mit Clipping
▼
2. ROUGE: Recall-orientierte Überlappung
▼
3. BERTScore: Token-Ähnlichkeit mit kontextuellen Embeddings
▼
4. Satz-Embeddings mit Kosinusähnlichkeit
```

#### 1. BLEU

BLEU (Papineni et al., 2002) bewertet eine Kandidatenübersetzung im Vergleich zu einer oder mehreren Referenzübersetzungen. Für n-Gramme bis zu einer Länge von vier berechnet es eine modifizierte n-Gramm-Präzision: jedes Kandidaten-n-Gramm wird maximal so oft gezählt, wie es in einer Referenz vorkommt (Clipping), sodass das Wiederholen eines korrekten Wortes den Wert nicht erhöht. Die Präzisionen werden über das geometrische Mittel kombiniert und mit einer Längenstrafe (Brevity Penalty) für Kandidaten multipliziert, die kürzer sind als die Referenzen, da die Präzision allein sehr kurze Ausgaben belohnen würde. Für BLEU wurde gezeigt, dass es auf Korpusebene mit menschlichen Urteilen korreliert.

#### 2. ROUGE

ROUGE (Lin, 2004) bewertet Zusammenfassungen anhand ihrer Überlappung mit Referenzzusammenfassungen und ist Recall-orientiert, fragt also, wie viel der Referenzinhalte der Kandidat abdeckt. Seine Varianten unterscheiden sich darin, was als Überlappung gilt: ROUGE-N verwendet n-Gramme, ROUGE-L die längste gemeinsame Teilsequenz, ROUGE-W eine gewichtete längste gemeinsame Teilsequenz, die aufeinanderfolgende Übereinstimmungen bevorzugt, und ROUGE-S Skip-Bigramme, also Wortpaare in Satzreihenfolge mit beliebigen Lücken dazwischen.

#### 3. BERTScore

BERTScore (Zhang et al., 2019) berechnet für jedes Token im Kandidaten einen Ähnlichkeitswert mit jedem Token in der Referenz, verwendet jedoch anstelle von exakten Übereinstimmungen kontextuelle Embeddings, sodass verschiedene Wörter mit ähnlicher Bedeutung im Kontext dennoch übereinstimmen können. In einer Evaluation mit den Ausgaben von 363 Systemen für maschinelle Übersetzung und Bildbeschreibung korrelierte BERTScore besser mit menschlichen Urteilen und eignete sich besser zur Modellauswahl als bestehende Metriken. Bei einer adversarialen Aufgabe zur Paraphrasenerkennung war BERTScore robuster gegenüber herausfordernden Beispielen (Zhang et al., 2019).

#### 4. Satz-Embeddings mit Kosinusähnlichkeit

BERT kann Satzpaare gut bewerten, aber beide Sätze müssen gemeinsam in das Netz eingegeben werden. Das Finden des ähnlichsten Paares in einer Sammlung von 10.000 Sätzen benötigt daher etwa 50 Millionen Inferenzberechnungen, also ungefähr 65 Stunden (Reimers & Gurevych, 2019). Sentence-BERT erweitert BERT um siamesische und Triplet-Netzstrukturen, sodass jeder Satz nur einmal in ein Embedding kodiert wird und die Embeddings mit Kosinusähnlichkeit verglichen werden. Dies reduziert die Suche von 65 Stunden auf etwa 5 Sekunden, während die Genauigkeit von BERT beibehalten wird, und macht semantische Ähnlichkeitssuche und Clustering praktikabel ([[vector-databases|Vektordatenbanken]]).

#### Ursprung und Varianten

BLEU (Papineni et al., 2002) wurde für maschinelle Übersetzung entwickelt und ROUGE (Lin, 2004) für die Zusammenfassung. 2019 brachte BERTScore (Zhang et al., 2019) kontextuelle Embeddings in Evaluationsmetriken ein, und Sentence-BERT (Reimers & Gurevych, 2019) machte Satz-Embeddings effizient genug für die Ähnlichkeitssuche über große Sammlungen.

### Wann einsetzen

- Wenn maschinelle Übersetzungen anhand von Referenzübersetzungen auf Korpusebene bewertet werden (Papineni et al., 2002).
- Wenn Zusammenfassungen danach bewertet werden, wie viel des Referenzinhalts sie abdecken (Lin, 2004).
- Wenn Paraphrasen mit unterschiedlicher Formulierung dennoch als Übereinstimmungen gezählt werden sollten, sind Embedding-basierte Metriken besser geeignet als exakte n-Gramm-Übereinstimmung (Zhang et al., 2019).
- Wenn viele Texte miteinander verglichen werden müssen, etwa bei semantischer Suche oder beim Clustering, vermeiden Satz-Embeddings, dass jedes Paar mit dem vollständigen Modell bewertet wird (Reimers & Gurevych, 2019).

### Stärken und Grenzen

**Stärken**
- BLEU und ROUGE sind günstig, transparent und benötigen nur Referenztexte (Papineni et al., 2002; Lin, 2004).
- BLEU korreliert auf Korpusebene mit menschlichen Urteilen (Papineni et al., 2002).
- BERTScore korreliert besser mit menschlichen Urteilen als frühere Metriken und ist robuster gegenüber adversarialen Paraphrasen (Zhang et al., 2019).

**Einschränkungen**
- Lexikalische Metriken zählen nur exakte Übereinstimmungen, daher erhalten korrekte Paraphrasen niedrige Werte (Zhang et al., 2019).
- Die Korrelation von BLEU mit menschlichen Urteilen wurde auf Korpusebene gezeigt, nicht für einzelne Sätze (Papineni et al., 2002).
- Die Bewertung jedes Satzpaars mit BERT ist für große Sammlungen praktisch nicht umsetzbar (Reimers & Gurevych, 2019).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| BLEU | n-Gramm-Präzision mit Clipping bis zur Länge vier und Brevity Penalty (Papineni et al., 2002) | Maschinelle Übersetzung auf Korpusebene |
| ROUGE | Recall-orientierte Überlappung von n-Grammen, Teilsequenzen oder Skip-Bigrammen (Lin, 2004) | Zusammenfassung |
| BERTScore | Token-Ähnlichkeit über kontextuelle Embeddings anstelle von exakten Übereinstimmungen (Zhang et al., 2019) | Bewertung generierter Texte mit Paraphrasen |
| Sentence-BERT | Ein Embedding pro Satz, verglichen mit Kosinusähnlichkeit (Reimers & Gurevych, 2019) | Semantische Suche, Clustering, Satzähnlichkeit |

### In der Praxis

Metrikwerte werden meist als Mittelwerte über einen Testdatensatz berichtet und mit menschlichen Urteilen abgeglichen, bevor man ihnen bei einer neuen Aufgabe vertraut (Papineni et al., 2002; Zhang et al., 2019). Bei RAG-Antworten und anderen generierten Texten werden lexikalische und Embedding-basierte Metriken durch aufgabenspezifische Prüfungen ergänzt, etwa die Treue zum abgerufenen Kontext ([[rag-generation-evaluation|RAG: Evaluation der Generierung]]), oder durch LLM-Judges ([[llm-as-a-judge|LLM-as-a-Judge]]). Beim Retrieval und beim Clustering werden Satz-Embeddings einmal berechnet und gespeichert, sodass Vergleiche auf günstige Kosinusähnlichkeiten reduziert werden (Reimers & Gurevych, 2019).

### Merksatz

Lexikalische Metriken wie BLEU und ROUGE messen die Wortübereinstimmung kostengünstig, während Embedding-basierte Methoden wie BERTScore und Sentence-BERT auch Paraphrasen erkennen.

### Quellen

- Papineni, K., Roukos, S., Ward, T. & Zhu, W.-J. (2002). *BLEU: a Method for Automatic Evaluation of Machine Translation.* ACL 2002. [ACL Anthology](https://aclanthology.org/P02-1040/)
- Lin, C.-Y. (2004). *ROUGE: A Package for Automatic Evaluation of Summaries.* Text Summarization Branches Out, ACL Workshop. [ACL Anthology](https://aclanthology.org/W04-1013/)
- Zhang, T. et al. (2019). *BERTScore: Evaluating Text Generation with BERT.* ICLR 2020. [arXiv:1904.09675](https://arxiv.org/abs/1904.09675)
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* EMNLP 2019. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
