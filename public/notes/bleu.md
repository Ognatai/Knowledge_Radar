---
title_en: BLEU (Bilingual Evaluation Understudy)
title_de: BLEU (Bilingual Evaluation Understudy)
entity_type: Method
aliases:
- BLEU
- BLEU score
- SacreBLEU
sources:
- https://aclanthology.org/P02-1040/
- https://aclanthology.org/W18-6319/
- https://arxiv.org/abs/1904.09675
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

BLEU (Bilingual Evaluation Understudy) scores a machine translation by its n-gram overlap with one or more human reference translations: it combines clipped n-gram precisions for n = 1 to 4 in a geometric mean and multiplies the result by a brevity penalty for output that is shorter than the references (Papineni et al., 2002). Introduced by IBM in 2002 as a quick, cheap, language-independent "understudy" for human judges, it correlated highly with human rankings of translation systems and became the dominant metric in machine translation (Papineni et al., 2002; Post, 2018). BLEU is a corpus-level metric that rewards surface overlap, so it penalises valid paraphrases, and scores computed with different [[tokenisation|tokenisation]] are not comparable, which SacreBLEU standardises (Zhang et al., 2020; Post, 2018).

### How it works

```text
candidate translations + reference translations (one or more per sentence)
 ▼
for n = 1…4: modified n-gram precision p_n
   count of each candidate n-gram clipped at its maximum count in any single reference,
   summed over the corpus, divided by the number of candidate n-grams
 ▼
geometric mean: exp( Σ_n w_n · log p_n ),  w_n = 1/4
 ▼
brevity penalty: BP = 1 if c > r, else e^(1 − r/c)    (c = candidate length, r = effective reference length)
 ▼
BLEU = BP · exp( Σ_n w_n · log p_n )   ∈ [0, 1], often reported × 100
```

#### 1. Modified n-gram precision

Plain [[classification-metrics|precision]], the share of candidate words that occur in a reference, rewards degenerate output: the candidate "the the the the the the the" has a unigram precision of 7/7 against "The cat is on the mat" (Papineni et al., 2002). BLEU therefore clips each word's count at the maximum number of times it occurs in any single reference, `Count_clip = min(Count, MaxRefCount)`, giving a modified unigram precision of 2/7 in this example. The same clipping applies to bigrams, trigrams and four-grams; unigram matches capture adequacy, longer n-grams fluency. Counts are summed over the whole test corpus before dividing (Papineni et al., 2002).

#### 2. Brevity penalty

Precision alone favours short output, and recall is hard to use with several references that differ in wording (Papineni et al., 2002). BLEU instead multiplies by a brevity penalty computed over the whole corpus: c is the total candidate length and r the effective reference length, the sum of the reference lengths closest to each candidate sentence; `BP = 1` if `c > r`, otherwise `e^(1 − r/c)`. Computing it per corpus rather than per sentence avoids punishing length deviations in short sentences too harshly (Papineni et al., 2002).

#### 3. Combination and range

BLEU is `BP · exp(Σ_{n=1..N} w_n log p_n)` with N = 4 and uniform weights `w_n = 1/4` (Papineni et al., 2002). The score lies between 0 and 1; even human translations rarely reach 1, and scores rise with the number of references, so values are only comparable on the same test set with the same references. In the original evaluation, BLEU's ranking of five systems correlated with monolingual human judgements at 0.99 and with bilingual judgements at 0.96 (Papineni et al., 2002).

#### 4. Reporting: SacreBLEU

BLEU is a parameterised metric: tokenisation, normalisation and the handling of references change the value (Post, 2018). Post (2018) found differences of up to 1.8 points between commonly used configurations, mainly caused by user-supplied tokenisation of the references, and proposed SacreBLEU, which computes BLEU on detokenised output with the standard WMT processing and prints a signature of the settings. Scores computed against differently processed references are not comparable.

#### 5. Limits of surface overlap

Because BLEU counts exact n-grams, it fails to recognise paraphrases: for the reference "people like foreign cars", BLEU scores "people like visiting places abroad" higher than "consumers prefer imported cars" (Zhang et al., 2020). It also only mildly penalises swapping cause and effect clauses when the phrases are long. Embedding-based metrics such as [[bertscore|BERTScore]] address these weaknesses ([[text-similarity-metrics|text similarity metrics]]).

#### Origin and variants

Kishore Papineni, Salim Roukos, Todd Ward and Wei-Jing Zhu at IBM presented BLEU at ACL 2002 (Papineni et al., 2002). Its reasonable correlation with human judgement, language independence and ease of computation made it the dominant metric of machine translation research (Post, 2018). A sentence-level variant, SentBLEU, is less reliable for single segments than embedding-based metrics (Zhang et al., 2020); SacreBLEU fixed the reporting conventions (Post, 2018).

### When to use it

- Comparing machine translation systems on the same test set and references, with SacreBLEU signatures ([[machine-translation|machine translation]]).
- Tracking regressions during system development, where quick and frequent evaluation matters (Papineni et al., 2002).
- As one signal among several for other generation tasks with reference outputs ([[llm-evaluation|LLM evaluation]]).

### Strengths and limitations

**Strengths**
- Fast, cheap, language-independent and reproducible (Papineni et al., 2002).
- High correlation with human system rankings in the original study (Papineni et al., 2002).
- Supports multiple references (Papineni et al., 2002).

**Limitations**
- Penalises paraphrases and synonyms that do not share n-grams with the references (Zhang et al., 2020).
- Not meaningful for single sentences or across different test sets and reference sets (Papineni et al., 2002).
- Values depend on tokenisation and must be reported with their configuration (Post, 2018).

### Comparison

| Metric | Matches | Level | Main use |
|---|---|---|---|
| BLEU | exact n-grams, precision + brevity penalty | corpus | machine translation |
| ROUGE | n-gram / subsequence recall | summary | summarisation ([[text-similarity-metrics\|text similarity metrics]]) |
| [[bertscore\|BERTScore]] | contextual [[embeddings\|embeddings]] of tokens | sentence | general text generation |
| [[llm-as-a-judge\|LLM as a judge]] | model judgement | answer | open-ended LLM output |

Sources: Papineni et al. (2002); Zhang et al. (2020).

### In practice

Report BLEU with its SacreBLEU signature and on standard test sets, so that others can reproduce it (Post, 2018). For LLM outputs without fixed reference wording, n-gram metrics are weak signals; reference-free checks and human or model judgements are more informative ([[llm-evaluation|LLM evaluation]], [[rag-generation-evaluation|RAG generation evaluation]]).

### Key takeaway

BLEU multiplies the geometric mean of clipped 1- to 4-gram precisions by a brevity penalty, giving a fast corpus-level translation score that tracks human system rankings but ignores paraphrases and must be computed with standardised settings to be comparable.

### Sources

- Papineni, K., Roukos, S., Ward, T. & Zhu, W.-J. (2002). *BLEU: a Method for Automatic Evaluation of Machine Translation.* ACL 2002. [aclanthology.org](https://aclanthology.org/P02-1040/)
- Post, M. (2018). *A Call for Clarity in Reporting BLEU Scores.* WMT 2018. [aclanthology.org](https://aclanthology.org/W18-6319/)
- Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q. & Artzi, Y. (2020). *BERTScore: Evaluating Text Generation with BERT.* ICLR 2020. [arXiv:1904.09675](https://arxiv.org/abs/1904.09675)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

BLEU (Bilingual Evaluation Understudy) bewertet eine maschinelle Übersetzung anhand ihrer N-Gramm-Überlappung mit einer oder mehreren menschlichen Referenzübersetzungen: Es verbindet gekappte N-Gramm-Präzisionen für n = 1 bis 4 in einem geometrischen Mittel und multipliziert das Ergebnis mit einer Kürzestrafe für Ausgaben, die kürzer als die Referenzen sind (Papineni et al., 2002). 2002 von IBM als schneller, günstiger und sprachunabhängiger „Ersatz“ für menschliche Gutachtende eingeführt, korrelierte es stark mit menschlichen Rangfolgen von Übersetzungssystemen und wurde zur vorherrschenden Metrik der maschinellen Übersetzung (Papineni et al., 2002; Post, 2018). BLEU ist eine Metrik auf Korpusebene, die Oberflächenüberlappung belohnt; es bestraft daher gültige Umschreibungen, und Werte mit unterschiedlicher Tokenisierung sind nicht vergleichbar, was SacreBLEU vereinheitlicht (Zhang et al., 2020; Post, 2018).

### Funktionsweise

```text
Kandidatenübersetzungen + Referenzübersetzungen (eine oder mehrere je Satz)
 ▼
für n = 1…4: modifizierte N-Gramm-Präzision p_n
   Anzahl jedes Kandidaten-N-Gramms, gekappt bei seiner höchsten Anzahl in einer einzelnen Referenz,
   über den Korpus summiert, geteilt durch die Zahl der Kandidaten-N-Gramme
 ▼
geometrisches Mittel: exp( Σ_n w_n · log p_n ),  w_n = 1/4
 ▼
Kürzestrafe: BP = 1, wenn c > r, sonst e^(1 − r/c)    (c = Kandidatenlänge, r = effektive Referenzlänge)
 ▼
BLEU = BP · exp( Σ_n w_n · log p_n )   ∈ [0, 1], oft × 100 angegeben
```

#### 1. Modifizierte N-Gramm-Präzision

Einfache Präzision, der Anteil der Kandidatenwörter, die in einer Referenz vorkommen, belohnt entartete Ausgaben: Der Kandidat „the the the the the the the“ hat gegenüber „The cat is on the mat“ eine Unigramm-Präzision von 7/7 (Papineni et al., 2002). BLEU kappt daher die Anzahl jedes Worts bei der höchsten Anzahl, mit der es in einer einzelnen Referenz vorkommt, `Count_clip = min(Count, MaxRefCount)`, was in diesem Beispiel eine modifizierte Unigramm-Präzision von 2/7 ergibt. Dieselbe Kappung gilt für Bigramme, Trigramme und Vierergramme; Unigramm-Treffer erfassen die inhaltliche Angemessenheit, längere N-Gramme die Flüssigkeit. Die Zählungen werden vor dem Teilen über den gesamten Testkorpus summiert (Papineni et al., 2002).

#### 2. Kürzestrafe

Präzision allein begünstigt kurze Ausgaben, und [[classification-metrics|Recall]] ist bei mehreren unterschiedlich formulierten Referenzen schwer zu nutzen (Papineni et al., 2002). BLEU multipliziert stattdessen mit einer Kürzestrafe über den ganzen Korpus: c ist die Gesamtlänge der Kandidaten und r die effektive Referenzlänge, die Summe der Referenzlängen, die jedem Kandidatensatz am nächsten liegen; `BP = 1`, wenn `c > r`, sonst `e^(1 − r/c)`. Die Berechnung je Korpus statt je Satz verhindert, dass Längenabweichungen in kurzen Sätzen zu hart bestraft werden (Papineni et al., 2002).

#### 3. Kombination und Wertebereich

BLEU ist `BP · exp(Σ_{n=1..N} w_n log p_n)` mit N = 4 und gleichen Gewichten `w_n = 1/4` (Papineni et al., 2002). Der Wert liegt zwischen 0 und 1; selbst menschliche Übersetzungen erreichen selten 1, und die Werte steigen mit der Zahl der Referenzen, sodass sie nur auf demselben Testset mit denselben Referenzen vergleichbar sind. In der ursprünglichen Evaluation korrelierte BLEUs Rangfolge von fünf Systemen mit Urteilen einsprachiger Personen zu 0,99 und mit Urteilen zweisprachiger Personen zu 0,96 (Papineni et al., 2002).

#### 4. Berichten: SacreBLEU

BLEU ist eine parametrisierte Metrik: Tokenisierung, Normalisierung und Behandlung der Referenzen verändern den Wert (Post, 2018). Post (2018) fand Unterschiede von bis zu 1,8 Punkten zwischen verbreiteten Konfigurationen, vor allem durch selbst gewählte Tokenisierung der Referenzen, und schlug SacreBLEU vor, das BLEU auf detokenisierten Ausgaben mit der Standardverarbeitung von WMT berechnet und eine Signatur der Einstellungen ausgibt. Werte gegen unterschiedlich verarbeitete Referenzen sind nicht vergleichbar.

#### 5. Grenzen der Oberflächenüberlappung

Weil BLEU exakte N-Gramme zählt, erkennt es Umschreibungen nicht: Zur Referenz „people like foreign cars“ bewertet BLEU „people like visiting places abroad“ höher als „consumers prefer imported cars“ (Zhang et al., 2020). Zudem bestraft es das Vertauschen von Ursache und Wirkung nur schwach, wenn die Satzteile lang sind. Embedding-basierte Metriken wie [[bertscore|BERTScore]] gehen diese Schwächen an ([[text-similarity-metrics|Metriken für Textähnlichkeit]]).

#### Herkunft und Varianten

Kishore Papineni, Salim Roukos, Todd Ward und Wei-Jing Zhu von IBM stellten BLEU auf der ACL 2002 vor (Papineni et al., 2002). Seine brauchbare Korrelation mit menschlichen Urteilen, Sprachunabhängigkeit und einfache Berechnung machten es zur vorherrschenden Metrik der Forschung zur maschinellen Übersetzung (Post, 2018). Die Variante auf Satzebene, SentBLEU, ist für einzelne Segmente weniger verlässlich als Embedding-basierte Metriken (Zhang et al., 2020); SacreBLEU legte die Konventionen für das Berichten fest (Post, 2018).

### Wann einsetzen

- Systeme zur maschinellen Übersetzung auf demselben Testset mit denselben Referenzen vergleichen, mit SacreBLEU-Signaturen ([[machine-translation|Maschinelle Übersetzung]]).
- Rückschritte während der Systementwicklung verfolgen, wenn schnelle und häufige Evaluation zählt (Papineni et al., 2002).
- Als ein Signal unter mehreren für andere Generierungsaufgaben mit Referenzausgaben ([[llm-evaluation|LLM-Evaluation]]).

### Stärken und Grenzen

**Stärken**
- Schnell, günstig, sprachunabhängig und reproduzierbar (Papineni et al., 2002).
- Hohe Korrelation mit menschlichen Systemrangfolgen in der ursprünglichen Studie (Papineni et al., 2002).
- Unterstützt mehrere Referenzen (Papineni et al., 2002).

**Grenzen**
- Bestraft Umschreibungen und Synonyme, die keine N-Gramme mit den Referenzen teilen (Zhang et al., 2020).
- Nicht aussagekräftig für einzelne Sätze oder über verschiedene Testsets und Referenzsätze hinweg (Papineni et al., 2002).
- Die Werte hängen von der Tokenisierung ab und müssen mit ihrer Konfiguration berichtet werden (Post, 2018).

### Vergleich

| Metrik | Abgleich | Ebene | Hauptzweck |
|---|---|---|---|
| BLEU | exakte N-Gramme, Präzision + Kürzestrafe | Korpus | maschinelle Übersetzung |
| ROUGE | Recall von N-Grammen / Teilfolgen | Zusammenfassung | Zusammenfassung ([[text-similarity-metrics\|Metriken für Textähnlichkeit]]) |
| [[bertscore\|BERTScore]] | kontextuelle [[embeddings\|Embeddings]] von Token | Satz | allgemeine Textgenerierung |
| [[llm-as-a-judge\|LLM as a Judge]] | Modellurteil | Antwort | offene LLM-Ausgaben |

Quellen: Papineni et al. (2002); Zhang et al. (2020).

### In der Praxis

BLEU wird mit seiner SacreBLEU-Signatur und auf Standard-Testsets berichtet, damit andere es reproduzieren können (Post, 2018). Für LLM-Ausgaben ohne feste Referenzformulierung sind N-Gramm-Metriken schwache Signale; referenzfreie Prüfungen sowie Urteile von Menschen oder Modellen sind aussagekräftiger ([[llm-evaluation|LLM-Evaluation]], [[rag-generation-evaluation|RAG: Evaluation der Generierung]]).

### Merksatz

BLEU multipliziert das geometrische Mittel gekappter 1- bis 4-Gramm-Präzisionen mit einer Kürzestrafe und liefert so einen schnellen Übersetzungswert auf Korpusebene, der menschlichen Systemrangfolgen folgt, Umschreibungen aber ignoriert und mit standardisierten Einstellungen berechnet werden muss, um vergleichbar zu sein.

### Quellen

- Papineni, K., Roukos, S., Ward, T. & Zhu, W.-J. (2002). *BLEU: a Method for Automatic Evaluation of Machine Translation.* ACL 2002. [aclanthology.org](https://aclanthology.org/P02-1040/)
- Post, M. (2018). *A Call for Clarity in Reporting BLEU Scores.* WMT 2018. [aclanthology.org](https://aclanthology.org/W18-6319/)
- Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q. & Artzi, Y. (2020). *BERTScore: Evaluating Text Generation with BERT.* ICLR 2020. [arXiv:1904.09675](https://arxiv.org/abs/1904.09675)
