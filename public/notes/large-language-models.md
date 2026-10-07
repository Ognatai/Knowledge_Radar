---
title_en: Large Language Models
title_de: Large Language Models
entity_type: Concept
sources:
- https://arxiv.org/abs/1706.03762
- https://arxiv.org/abs/2005.14165
- https://arxiv.org/abs/2001.08361
- https://arxiv.org/abs/2203.15556
- https://arxiv.org/abs/2203.02155
- https://arxiv.org/abs/2206.07682
- https://arxiv.org/abs/1508.07909
- https://arxiv.org/abs/1904.09751
- https://edoc.ub.uni-muenchen.de/36297/
- https://doi.org/10.1007/978-3-031-74630-7_20
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Large language models (LLMs) are Transformer-based neural networks ([[attention-and-transformers|Attention and Transformers]]) trained on large text corpora to predict the next token. At sufficient scale they can perform many tasks from instructions or a few examples in the prompt, without task-specific fine-tuning ([[prompt-engineering|Prompt Engineering]]), and instruction tuning with human feedback aligns their outputs with user intent (Brown et al., 2020; Ouyang et al., 2022).

### How it works

Text is split into subword tokens, a Transformer computes a contextual representation of the token sequence, and the model outputs a probability distribution over the next token. Generation repeats this step token by token, guided by a decoding strategy. The model is first pretrained on large corpora and then aligned through instruction tuning and reinforcement learning from human feedback; scaling laws describe how performance depends on model size, data and compute.

```text
1. Subword tokenization
▼
2. Transformer architecture
▼
3. Autoregressive next-token prediction
▼
4. Training phases: pretraining, instruction tuning, RLHF
▼
5. Decoding at inference time
▼
6. Scaling
▼
7. Proprietary and open models
```

#### 1. Subword tokenization

Text is split into subword units so that rare and unknown words can be represented as sequences of more frequent pieces ([[tokenization|Tokenization]]). Byte pair encoding (BPE) builds the vocabulary by repeatedly merging the most frequent pair of adjacent symbols in the training corpus, so that frequent words become single tokens while rare words are composed of several subwords (Sennrich et al., 2015). The vocabulary is fixed before training, and context length is measured in tokens rather than characters or words. In neural machine translation, subword units improved over a back-off dictionary baseline by up to 1.1 BLEU (English-German) and 1.3 BLEU (English-Russian) (Sennrich et al., 2015).

#### 2. Transformer architecture

The Transformer replaces recurrence and convolutions with attention (Vaswani et al., 2017). Self-attention computes, for every token, a weighted combination of all tokens in the sequence using query, key and value vectors: `attention = softmax(Q K^T / sqrt(d_k)) V`. Multi-head attention runs several attention computations with different learned projections in parallel, and position-wise feed-forward layers follow; because attention itself ignores word order, positional encodings are added to the token embeddings. Without recurrence, all positions of a training sequence can be processed in parallel, which makes training on large data sets much faster than with recurrent networks (Vaswani et al., 2017).

#### 3. Autoregressive next-token prediction

Given the preceding tokens, the model outputs a probability distribution over the vocabulary for the next token. Generation is iterative: a token is chosen from this distribution, appended to the input, and the step is repeated until a stop condition is reached (Brown et al., 2020). The context window, the maximum number of tokens the model can process at once, limits how much preceding text is visible. Because each new token depends on the previous ones, generation is sequential, so producing long outputs takes proportionally longer.

#### 4. Training phases

Pretraining optimises next-token prediction on large text corpora. With 175 billion parameters, GPT-3 performed many tasks from a task description and a few examples in the prompt, without gradient updates or fine-tuning (Brown et al., 2020). Larger models are not automatically better at following user intent and can produce untruthful or toxic outputs; InstructGPT therefore fine-tuned GPT-3 on demonstrations written by labellers and then applied reinforcement learning from human feedback ([[reinforcement-learning|Reinforcement Learning Fundamentals]]) using rankings of model outputs (Ouyang et al., 2022). In human evaluations, outputs of the 1.3B-parameter InstructGPT model were preferred to those of the 175B GPT-3, despite 100 times fewer parameters, with improvements in truthfulness and reductions in toxic output (Ouyang et al., 2022). In RLHF, a reward model trained on human preferences guides the fine-tuning, and a Kullback-Leibler penalty keeps the updated model close to its original distribution (Urchs, 2025). ChatGPT combined a GPT model trained this way with a dialogue interface, which made LLMs accessible to the general public and raised new concerns about ethics, misinformation and AI governance (Urchs, 2025).

#### 5. Decoding at inference time

Greedy decoding always picks the most probable token, and beam search keeps several high-probability candidate sequences; both maximisation-based methods tend to produce bland, repetitive text (Holtzman et al., 2019). Sampling methods introduce randomness: temperature divides the model's scores (logits) before the softmax, with low temperatures making the distribution sharper and high temperatures flatter; top-k sampling restricts the choice to the k most probable tokens. Nucleus (top-p) sampling samples from the smallest set of tokens whose cumulative probability exceeds p, so the candidate set grows or shrinks with the shape of the distribution and the unreliable tail is cut off (Holtzman et al., 2019).

#### 6. Scaling

The cross-entropy loss of language models falls as a power law with model size, data set size and training compute, and larger models are more sample-efficient (Kaplan et al., 2020). For compute-optimal training, model size and the number of training tokens should be scaled in equal proportion: for every doubling of model size, the number of training tokens should also be doubled (Hoffmann et al., 2022). Following this, Chinchilla (70B parameters, trained on four times more data than Gopher with the same compute) outperformed larger models such as Gopher (280B) and GPT-3 (175B), reaching an average accuracy of 67.5% on MMLU, more than 7 percentage points above Gopher (Hoffmann et al., 2022). Some abilities are described as emergent: they are absent in smaller models and appear only in larger ones, so they cannot be predicted by extrapolating from smaller models (Wei et al., 2022).

#### 7. Proprietary and open models

Besides the GPT family, proprietary model families such as Anthropic's Claude 3, Google DeepMind's Gemini, Mistral's models and Amazon's Titan are widely used; like GPT, they raise concerns about transparency, reproducibility and the opacity of their training data (Urchs, 2025). Open alternatives such as LLaMA, Zephyr and DeepSeek LLM promote reproducibility and equitable access; DeepSeek LLM, for example, was trained from scratch on 2 trillion English and Chinese tokens, is available with 7 and 67 billion parameters under the MIT licence and outperformed LLaMA-2 70B on several benchmarks, especially in reasoning, mathematics and coding. Even for open models, however, transparency about pretraining data and fine-tuning often remains limited (Urchs, 2025).

#### Origin and variants

The Transformer (Vaswani et al., 2017) was introduced for machine translation and reached 28.4 BLEU on WMT 2014 English-German and 41.8 BLEU on English-French. GPT-3 (Brown et al., 2020) showed that scaling a Transformer language model to 175 billion parameters enables few-shot learning from prompts. InstructGPT (Ouyang et al., 2022) added instruction tuning and reinforcement learning from human feedback, and Chinchilla (Hoffmann et al., 2022) showed that many large models had been trained on too little data for their size. ChatGPT brought such models to a broad public, and proprietary and open model families now coexist (Urchs, 2025).

### When to use it

- When a task can be described in natural language and little task-specific training data is available, so that prompting with instructions or a few examples suffices ([[prompt-engineering|Prompt Engineering]], Brown et al., 2020).
- When outputs must follow user instructions, in which case instruction-tuned models aligned with human feedback are preferable to base pretrained models (Ouyang et al., 2022).
- When a model is trained or selected under a fixed compute budget, in which case compute-optimal scaling of parameters and data is relevant (Hoffmann et al., 2022).

### Strengths and limitations

**Strengths**
- A single pretrained model can perform many tasks from prompts without task-specific fine-tuning (Brown et al., 2020).
- Performance improves predictably with model size, data and compute, following power laws (Kaplan et al., 2020).
- Without recurrence, Transformers train in parallel over sequence positions, which made training on very large corpora practical (Vaswani et al., 2017).

**Limitations**
- Pretrained models can produce untruthful, toxic or unhelpful outputs and need alignment, for instance with human feedback (Ouyang et al., 2022).
- GPT-3's few-shot learning still struggled on some data sets, and some data sets raised methodological issues related to training on large web corpora (Brown et al., 2020).
- Many large models were significantly undertrained because the amount of training data was kept constant while model size grew (Hoffmann et al., 2022).
- Training data and fine-tuning methods are often not disclosed, even for openly released models (Urchs, 2025).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Pretrained base model (GPT-3) | Trained only on next-token prediction; tasks are specified through prompts and examples (Brown et al., 2020) | Few-shot use and as a starting point for further adaptation |
| Instruction-tuned model with RLHF (InstructGPT) | Additionally fine-tuned on demonstrations and optimised with human preference rankings (Ouyang et al., 2022) | Assistants and applications that must follow user instructions |
| Compute-optimal model (Chinchilla) | Smaller model trained on proportionally more tokens for the same compute (Hoffmann et al., 2022) | Settings where inference cost matters, since a smaller model is cheaper to run |

### In practice

LLMs are evaluated with benchmarks such as MMLU, which Hoffmann et al. (2022) report for Chinchilla, and, for alignment, with human preference judgements (Ouyang et al., 2022); see [[llm-evaluation|LLM Evaluation]]. Decoding settings such as temperature or the nucleus threshold p are chosen per application, since maximisation-based decoding tends to produce repetitive text (Holtzman et al., 2019). Untruthful outputs remain a known failure mode even after alignment (Ouyang et al., 2022). Responses should also be checked for biases and language errors: in a study of ChatGPT in English and German, identical prompts gave varying answers, and post-hoc fairness interventions led to overcorrection, such as an over-representation of female personas for neutral prompts (Urchs et al., 2023; [[bias-in-nlp|Bias in NLP]]).

### Key takeaway

LLMs generate text by repeatedly predicting the next token with a Transformer; their abilities grow with scale, and instruction tuning with human feedback makes them follow user intent.

### Sources

- Vaswani, A. et al. (2017). *Attention Is All You Need.* NeurIPS 2017. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners.* NeurIPS 2020. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)
- Kaplan, J. et al. (2020). *Scaling Laws for Neural Language Models.* [arXiv:2001.08361](https://arxiv.org/abs/2001.08361)
- Hoffmann, J. et al. (2022). *Training Compute-Optimal Large Language Models.* [arXiv:2203.15556](https://arxiv.org/abs/2203.15556)
- Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback.* [arXiv:2203.02155](https://arxiv.org/abs/2203.02155)
- Wei, J. et al. (2022). *Emergent Abilities of Large Language Models.* TMLR. [arXiv:2206.07682](https://arxiv.org/abs/2206.07682)
- Sennrich, R. et al. (2015). *Neural Machine Translation of Rare Words with Subword Units.* ACL 2016. [arXiv:1508.07909](https://arxiv.org/abs/1508.07909)
- Holtzman, A. et al. (2019). *The Curious Case of Neural Text Degeneration.* ICLR 2020. [arXiv:1904.09751](https://arxiv.org/abs/1904.09751)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
- Urchs, S., Thurner, V., Aßenmacher, M., Heumann, C. & Thiemichen, S. (2023). *How Prevalent Is Gender Bias in ChatGPT? Exploring German and English ChatGPT Responses.* ECML PKDD 2023 Workshops, Communications in Computer and Information Science 2133, Springer (2025). [doi:10.1007/978-3-031-74630-7_20](https://doi.org/10.1007/978-3-031-74630-7_20)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Große Sprachmodelle (LLMs) sind Transformer-basierte neuronale Netze ([[attention-and-transformers|Attention and Transformers]]), die auf großen Textkorpora darauf trainiert werden, das nächste Token vorherzusagen. Bei ausreichender Größe können sie viele Aufgaben aus Anweisungen oder einigen Beispielen im Prompt ausführen, ohne eine task-spezifische Feinabstimmung ([[prompt-engineering|Prompt Engineering]]), und Instruction Tuning mit menschlichem Feedback richtet ihre Ausgaben an der Absicht der Nutzer aus (Brown et al., 2020; Ouyang et al., 2022).

### Funktionsweise

Text wird in Subwort-Token aufgeteilt, ein Transformer berechnet eine kontextuelle Darstellung der Token-Reihe, und das Modell gibt eine Wahrscheinlichkeitsverteilung über das nächste Token aus. Die Generierung wiederholt diesen Schritt Token für Token, unter Berücksichtigung einer Decodierstrategie. Das Modell wird zunächst auf großen Corpora vortrainiert und dann durch Instruction Tuning und Reinforcement Learning from Human Feedback (RLHF) ausgerichtet; Skalierungsgesetze beschreiben, wie die Leistung von der Modellgröße, Daten und Rechenleistung abhängt.

```text
1. Subwort-Tokenisierung
▼
2. Transformer-Architektur
▼
3. Autoregressive Vorhersage des nächsten Tokens
▼
4. Trainingsphasen: Vortraining, Instruction Tuning, RLHF
▼
5. Decodierung zur Inferenzzeit
▼
6. Skalierung
▼
7. Proprietäre und offene Modelle
```

#### 1. Subwort-Tokenisierung

Text wird in Subwort-Einheiten aufgeteilt, damit seltene und unbekannte Wörter als Sequenzen häufigerer Einheiten dargestellt werden können ([[tokenization|Tokenisierung]]). Byte Pair Encoding (BPE) erstellt das Vokabular, indem es wiederholt das häufigste Paar benachbarter Symbole im Trainingskorpus zusammenführt, sodass häufige Wörter zu einzelnen Token werden, während seltene Wörter aus mehreren Subwörtern bestehen (Sennrich et al., 2015). Das Vokabular ist vor dem Training festgelegt, und die Länge des Kontexts wird in Token gemessen, nicht in Zeichen oder Wörtern. In der neuronalen maschinellen Übersetzung verbesserten Subwort-Einheiten eine Baseline mit Back-off-Wörterbuch um bis zu 1,1 BLEU (Englisch-Deutsch) und 1,3 BLEU (Englisch-Russisch) (Sennrich et al., 2015).

#### 2. Transformer-Architektur

Der Transformer ersetzt Rekurrenzen und Faltungen durch Aufmerksamkeit (Vaswani et al., 2017). Die Selbstaufmerksamkeit berechnet für jedes Token eine gewichtete Kombination aller Tokens in der Sequenz mithilfe von Query-, Key- und Value-Vektoren: `attention = softmax(Q K^T / sqrt(d_k)) V`. Die mehrköpfige Aufmerksamkeit führt mehrere Aufmerksamkeitsberechnungen mit unterschiedlichen gelernten Projektionen parallel durch, gefolgt von positionsspezifischen Feed-Forward-Schichten; da Aufmerksamkeit selbst die Wortreihenfolge ignoriert, werden positionale Kodierungen den Token-Embeddings hinzugefügt. Ohne Rekurrenzen können alle Positionen einer Trainingssequenz parallel verarbeitet werden, was das Training auf großen Datensätzen viel schneller macht als bei rekurrenten Netzwerken (Vaswani et al., 2017).

#### 3. Autoregressives Vorhersagen des nächsten Tokens

Gegeben die vorherigen Tokens gibt das Modell eine Wahrscheinlichkeitsverteilung über das Vokabular für das nächste Token aus. Die Generierung ist iterativ: ein Token wird aus dieser Verteilung gewählt, an die Eingabe angehängt, und der Schritt wird wiederholt, bis eine Stop-Bedingung erreicht ist (Brown et al., 2020). Das Kontextfenster, die maximale Anzahl an Token, die das Modell gleichzeitig verarbeiten kann, begrenzt, wie viel vorheriger Text sichtbar ist. Da jedes neue Token von den vorherigen abhängt, ist die Generierung sequenziell, weshalb das Erzeugen langer Ausgaben proportional länger dauert.

#### 4. Trainingsphasen

Das Vortraining optimiert die Vorhersage des nächsten Tokens anhand großer Textkorpora. Mit 175 Milliarden Parametern konnte GPT-3 viele Aufgaben aus einer Aufgabenbeschreibung und einigen Beispielen im Prompt durchführen, ohne Gradientenupdates oder Feinabstimmung (Brown et al., 2020). Größere Modelle sind nicht automatisch besser darin, der Absicht der Nutzer zu folgen, und können unwahre oder toxische Ausgaben erzeugen; InstructGPT hat GPT-3 daher anhand von Demonstrationen, die von Annotatoren geschrieben wurden, feinabgestimmt und anschließend Verstärkungslernen aus menschlicher Rückmeldung ([[reinforcement-learning|Reinforcement Learning Fundamentals]]) angewendet, wobei Ranglisten der Modellausgaben genutzt wurden (Ouyang et al., 2022). In menschlichen Evaluierungen wurden die Ausgaben des 1,3B-Parametern-InstructGPT-Modells gegenüber denen des 175B GPT-3 bevorzugt, obwohl es nur ein Hundertstel so viele Parameter hatte, bei höherer Wahrhaftigkeit und weniger toxischen Ausgaben (Ouyang et al., 2022). Bei RLHF steuert ein auf menschlichen Präferenzen trainiertes Reward-Modell das Fine-Tuning, und ein Kullback-Leibler-Strafterm hält das angepasste Modell nahe an seiner ursprünglichen Verteilung (Urchs, 2025). ChatGPT verband ein so trainiertes GPT-Modell mit einer Dialogoberfläche, machte LLMs damit einer breiten Öffentlichkeit zugänglich und warf neue Fragen zu Ethik, Desinformation und KI-Governance auf (Urchs, 2025).

#### 5. Decodieren zur Inferenzzeit

Greedy-Decodierung wählt immer den wahrscheinlichsten Token aus, und der Beam-Search behält mehrere Kandidatenfolgen mit hoher Wahrscheinlichkeit bei; beide, auf Maximierung basierende Methoden, neigen dazu, langweilige, repetitive Texte zu erzeugen (Holtzman et al., 2019). Sampling-Methoden führen Zufälligkeit ein: die Temperatur teilt die Scores (Logits) des Modells vor dem Softmax, wobei niedrige Temperaturen die Verteilung schärfer und hohe Temperaturen flacher machen; das Top-k-Sampling beschränkt die Wahl auf die k wahrscheinlichsten Token. Nucleus-Sampling (Top-p) zieht aus der kleinsten Menge an Token, deren kumulative Wahrscheinlichkeit p übersteigt; so wächst oder schrumpft die Kandidatenmenge mit der Form der Verteilung, und der unzuverlässige Rand der Verteilung wird abgeschnitten (Holtzman et al., 2019).

#### 6. Skalierung

Die Kreuzentropie-Verlustfunktion von Sprachmodellen nimmt mit der Modellgröße, der Größe des Datensatzes und dem Rechenaufwand für das Training nach einem Potenzgesetz ab, und größere Modelle sind dateneffizienter (Kaplan et al., 2020). Für ein rechenoptimales Training sollten Modellgröße und die Anzahl der Trainings-Token im gleichen Verhältnis skaliert werden: bei jedem Verdoppeln der Modellgröße sollte auch die Anzahl der Trainings-Token verdoppelt werden (Hoffmann et al., 2022). Danach übertraf Chinchilla (70B Parameter, trainiert auf viermal mehr Daten als Gopher mit demselben Rechenaufwand) größere Modelle wie Gopher (280B) und GPT-3 (175B), indem es eine durchschnittliche Genauigkeit von 67,5 % auf MMLU erreichte, was mehr als 7 Prozentpunkte über Gopher lag (Hoffmann et al., 2022). Einige Fähigkeiten werden als emergent beschrieben: sie fehlen in kleineren Modellen und treten erst in größeren auf, weshalb sie nicht durch Extrapolation von kleineren Modellen vorhergesagt werden können (Wei et al., 2022).

#### 7. Proprietäre und offene Modelle

Neben der GPT-Familie sind proprietäre Modellfamilien wie Claude 3 von Anthropic, Gemini von Google DeepMind, die Modelle von Mistral und Titan von Amazon verbreitet; wie bei GPT bestehen Bedenken hinsichtlich Transparenz, Reproduzierbarkeit und der Undurchsichtigkeit ihrer Trainingsdaten (Urchs, 2025). Offene Alternativen wie LLaMA, Zephyr und DeepSeek LLM fördern Reproduzierbarkeit und gleichberechtigten Zugang; DeepSeek LLM etwa wurde von Grund auf mit 2 Billionen englischen und chinesischen Token trainiert, ist mit 7 und 67 Milliarden Parametern unter der MIT-Lizenz verfügbar und übertraf LLaMA-2 70B auf mehreren Benchmarks, vor allem beim Schließen, in Mathematik und beim Programmieren. Auch bei offenen Modellen bleibt die Transparenz über Vortrainingsdaten und Fine-Tuning aber oft begrenzt (Urchs, 2025).

#### Ursprung und Varianten

Der Transformer (Vaswani et al., 2017) wurde für maschinelles Übersetzen eingeführt und erreichte 28,4 BLEU auf WMT 2014 Englisch-Deutsch und 41,8 BLEU auf Englisch-Französisch. GPT-3 (Brown et al., 2020) zeigte, dass das Skalieren eines Transformer-Sprachmodells auf 175 Milliarden Parameter das Lernen aus Prompts mit wenigen Beispielen ermöglicht. InstructGPT (Ouyang et al., 2022) ergänzte Instruction Tuning und Reinforcement Learning from Human Feedback, und Chinchilla (Hoffmann et al., 2022) zeigte, dass viele große Modelle auf zu wenig Daten für ihre Größe trainiert wurden. ChatGPT brachte solche Modelle einer breiten Öffentlichkeit nahe, und heute bestehen proprietäre und offene Modellfamilien nebeneinander (Urchs, 2025).

### Wann einsetzen

- Wenn eine Aufgabe in natürlicher Sprache beschrieben werden kann und nur wenig spezifische Trainingsdaten für die Aufgabe vorliegen, sodass das Erstellen von Anweisungen oder das Verwenden einiger Beispiele ausreicht ([[prompt-engineering|Prompt Engineering]], Brown et al., 2020).
- Wenn Ausgaben den Anweisungen des Nutzers folgen müssen, wobei dann mit Instruction Tuning und menschlichem Feedback ausgerichtete Modelle reinen vortrainierten Basismodellen vorzuziehen sind (Ouyang et al., 2022).
- Wenn ein Modell unter einem festen Rechenbudget trainiert oder ausgewählt wird, wobei in diesem Fall eine rechenoptimale Skalierung von Parametern und Daten relevant ist (Hoffmann et al., 2022).

### Stärken und Grenzen

**Stärken**
- Ein einzelnes vortrainiertes Modell kann viele Aufgaben aus Prompts ohne task-spezifisches Fine-Tuning ausführen (Brown et al., 2020).
- Die Leistung verbessert sich vorhersagbar mit der Modellgröße, Datenmenge und Rechenleistung, gemäß Potenzgesetzen (Kaplan et al., 2020).
- Ohne Rekurrenz trainieren Transformer parallel über Sequenzpositionen, was das Training auf sehr großen Corpora praktisch machte (Vaswani et al., 2017).

**Einschränkungen**
- Vortrainierte Modelle können unwahre, toxische oder unhilfreiche Ausgaben produzieren und benötigen Ausrichtung, beispielsweise durch menschliche Rückmeldung (Ouyang et al., 2022).
- Das few-shot Learning von GPT-3 hatte immer noch Schwierigkeiten mit einigen Datensätzen, und einige Datensätze brachten methodische Probleme hervor, die mit dem Training auf großen Web-Corpora zusammenhingen (Brown et al., 2020).
- Viele große Modelle wurden erheblich untertrainiert, da die Menge an Trainingsdaten konstant blieb, während die Modellgröße wuchs (Hoffmann et al., 2022).
- Trainingsdaten und Fine-Tuning-Verfahren werden oft nicht offengelegt, selbst bei offen veröffentlichten Modellen (Urchs, 2025).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Vortrainiertes Basismodell (GPT-3) | Nur auf Vorhersage des nächsten Tokens trainiert; Aufgaben werden durch Prompts und Beispiele spezifiziert (Brown et al., 2020) | Few-Shot-Nutzung und als Ausgangspunkt für weitere Anpassungen |
| Modell mit Instruction Tuning und RLHF (InstructGPT) | Zusätzlich anhand von Demonstrationen feinabgestimmt und mit menschlichen Präferenzrangierungen optimiert (Ouyang et al., 2022) | Assistenten und Anwendungen, die Benutzeranweisungen folgen müssen |
| Rechenoptimales Modell (Chinchilla) | Kleineres Modell, trainiert auf einer proportional größeren Anzahl an Tokens bei gleicher Rechenleistung (Hoffmann et al., 2022) | Umgebungen, in denen die Inferenzkosten eine Rolle spielen, da ein kleineres Modell günstiger zu betreiben ist |

### In der Praxis

LLMs werden mit Benchmarks wie MMLU bewertet, für die Hoffmann et al. (2022) die Ergebnisse für Chinchilla berichten, und für die Ausrichtung mit menschlichen Präferenzurteilen (Ouyang et al., 2022); siehe [[llm-evaluation|LLM Evaluation]]. Decodier-Einstellungen wie Temperatur oder der Nucleus-Threshold p werden je nach Anwendung gewählt, da auf Maximierung basierende Decodierverfahren tendenziell wiederholten Text erzeugen (Holtzman et al., 2019). Unwahre Ausgaben bleiben auch nach der Ausrichtung ein bekannter Fehlermodus (Ouyang et al., 2022). Antworten sollten zudem auf Bias und sprachliche Fehler geprüft werden: In einer Untersuchung von ChatGPT auf Englisch und Deutsch lieferten identische Prompts unterschiedliche Antworten, und nachträgliche Fairness-Eingriffe führten zu Überkorrekturen, etwa zu überproportional vielen weiblichen Personen bei neutralen Prompts (Urchs et al., 2023; [[bias-in-nlp|Bias in NLP]]).

### Merksatz

LLMs generieren Text, indem sie mit einem Transformer wiederholt den nächsten Token vorhersagen; ihre Fähigkeiten wachsen mit der Skalierung, und Instruction Tuning mit menschlichem Feedback bringt sie dazu, der Absicht der Nutzer zu folgen.

### Quellen

- Vaswani, A. et al. (2017). *Attention Is All You Need.* NeurIPS 2017. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners.* NeurIPS 2020. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)
- Kaplan, J. et al. (2020). *Scaling Laws for Neural Language Models.* [arXiv:2001.08361](https://arxiv.org/abs/2001.08361)
- Hoffmann, J. et al. (2022). *Training Compute-Optimal Large Language Models.* [arXiv:2203.15556](https://arxiv.org/abs/2203.15556)
- Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback.* [arXiv:2203.02155](https://arxiv.org/abs/2203.02155)
- Wei, J. et al. (2022). *Emergent Abilities of Large Language Models.* TMLR. [arXiv:2206.07682](https://arxiv.org/abs/2206.07682)
- Sennrich, R. et al. (2015). *Neural Machine Translation of Rare Words with Subword Units.* ACL 2016. [arXiv:1508.07909](https://arxiv.org/abs/1508.07909)
- Holtzman, A. et al. (2019). *The Curious Case of Neural Text Degeneration.* ICLR 2020. [arXiv:1904.09751](https://arxiv.org/abs/1904.09751)
- Urchs, S. (2025). *Detecting Gender Discrimination in Natural Language Processing.* Dissertation, Ludwig-Maximilians-Universität München. [LMU edoc](https://edoc.ub.uni-muenchen.de/36297/)
- Urchs, S., Thurner, V., Aßenmacher, M., Heumann, C. & Thiemichen, S. (2023). *How Prevalent Is Gender Bias in ChatGPT? Exploring German and English ChatGPT Responses.* ECML PKDD 2023 Workshops, Communications in Computer and Information Science 2133, Springer (2025). [doi:10.1007/978-3-031-74630-7_20](https://doi.org/10.1007/978-3-031-74630-7_20)
