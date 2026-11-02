---
title_en: Decoding Strategies
title_de: Decoding-Strategien
entity_type: Method
aliases:
- Decoding strategies
- Decoding
- Greedy decoding
- Beam search
- Top-k sampling
- Top-p sampling
- Nucleus sampling
- Temperature sampling
- Min-p sampling
sources:
- https://web.stanford.edu/~jurafsky/slp3/7.pdf
- https://web.stanford.edu/~jurafsky/slp3/13.pdf
- https://arxiv.org/abs/1904.09751
- https://arxiv.org/abs/1805.04833
- https://arxiv.org/abs/1610.02424
- https://arxiv.org/abs/2407.01082
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A language model only gives a probability distribution over the next token; a decoding strategy decides which token is actually generated, step by step, until an end token (Jurafsky & Martin, 2026). Greedy decoding and beam search look for high-probability sequences and suit tightly constrained tasks such as [[machine-translation|machine translation]], while open-ended generation uses sampling, usually truncated with top-k, top-p (nucleus) or min-p and shaped with a temperature, because maximising likelihood produces bland and repetitive text (Holtzman et al., 2020; Jurafsky & Martin, 2026). The choice of decoding can change output quality dramatically even for the same model (Holtzman et al., 2020).

### How it works

```text
context w<t ──► LLM ──► logits u ──► softmax(u / τ) ──► P(w | w<t)
                                                │
          ┌─────────────────────────────────────┼──────────────────────────────────────┐
          ▼                                     ▼                                      ▼
   greedy: argmax              beam search: keep k best          sampling: truncate the tail, then sample
                               partial sequences (log probs)       top-k │ top-p (nucleus) │ min-p
          └─────────────────────────────────────┬──────────────────────────────────────┘
                                                ▼
                       append token, repeat until EOS or length limit
```

#### 1. Greedy decoding

Greedy decoding picks the most probable token at every step; it is deterministic, so the same context always yields the same string (Jurafsky & Martin, 2026). Its weakness is that a locally best choice can rule out a better continuation: in Jurafsky and Martin's example the most probable sequence "ok ok EOS" is missed because "yes" has the highest probability at the first step (Jurafsky & Martin, 2026).

#### 2. Beam search

Beam search keeps the k best hypotheses (partial outputs with their log probabilities) at each step, extends each with every vocabulary token, scores the k × |V| extensions and prunes them back to k; k is the beam width, typically 5 to 10 in machine translation (Jurafsky & Martin, 2026). Because longer outputs accumulate lower probabilities, scores are length-normalised, for example by dividing the log probability by the number of tokens (Jurafsky & Martin, 2026). Beam outputs tend to differ only slightly from each other; Diverse Beam Search adds a diversity term to the objective and even found better top-1 solutions (Vijayakumar et al., 2018). Minimum Bayes risk decoding instead chooses the candidate with the lowest expected error under an evaluation metric and can work better than beam search (Jurafsky & Martin, 2026).

#### 3. Why maximising likelihood degenerates

For open-ended generation, beam search and greedy decoding lead to degeneration: output that is bland, incoherent or stuck in repetitive loops, even with GPT-2 Large; the probability of a repeated phrase rises with each repetition, a positive feedback loop (Holtzman et al., 2020). Human text is not the most probable text; it shows higher variance in per-token probability (Holtzman et al., 2020). Pure sampling from the full distribution fails in the opposite way, producing incoherent text, because the "unreliable tail" of tens of thousands of low-probability tokens is over-represented in aggregate (Holtzman et al., 2020; Jurafsky & Martin, 2026).

#### 4. Truncated sampling

- **Temperature:** dividing the logits by τ before the [[softmax|softmax]] sharpens the distribution for τ < 1 and flattens it for τ > 1; τ → 0 approaches greedy decoding (Jurafsky & Martin, 2026).
- **Top-k:** keep the k most probable tokens, renormalise and sample; k = 1 is greedy (Jurafsky & Martin, 2026; Fan et al., 2018). Because k is fixed while the shape of the distribution changes, the top k may cover most or only a small part of the probability mass (Jurafsky & Martin, 2026).
- **Top-p (nucleus):** keep the smallest set of tokens whose cumulative probability reaches p, which adapts the pool size to the model's confidence (Holtzman et al., 2020). Top-k and top-p are often combined, top-k as a hard filter first (Jurafsky & Martin, 2026).
- **Min-p:** keep tokens whose probability is at least `p_base × p_max`, a threshold scaled by the top token's probability, so the pool widens when the model is uncertain; it improved quality and diversity especially at high temperatures for models from 1B to 123B parameters and was adopted by frameworks such as Hugging Face Transformers and [[llm-inference-serving|vLLM]] (Nguyen et al., 2025).

#### 5. Quality versus diversity

Methods that emphasise the most probable tokens produce output that people rate as more accurate, coherent and factual but also more boring and repetitive; giving more weight to middle-probability tokens is more creative and diverse but less factual (Jurafsky & Martin, 2026). Beam search works well in constrained tasks such as machine translation, while in most other tasks people prefer text generated by sampling methods that add some diversity (Jurafsky & Martin, 2026).

#### Origin and variants

Beam search was first proposed by Lowerre in 1976, and sampling from language models goes back to Shannon (1948) (Jurafsky & Martin, 2026). Top-k sampling became popular for story generation (Fan et al., 2018) and GPT-2, nucleus sampling was introduced by Holtzman et al. (2020), and min-p by Nguyen et al. (2025). Decoding can also be sped up without changing the output distribution by [[speculative-decoding|speculative decoding]], or sampled several times and aggregated by majority vote as in [[self-consistency|self-consistency]].

### When to use it

- Greedy or low temperature for factual answers, extraction and structured outputs ([[tool-calling|tool calling]]).
- Beam search for machine translation and other tasks whose output is tightly determined by the input (Jurafsky & Martin, 2026).
- Top-p, top-k or min-p sampling with moderate temperature for open-ended text, dialogue and creative writing (Holtzman et al., 2020; Nguyen et al., 2025).
- Several samples when answers are later compared or voted on ([[self-consistency|self-consistency]], [[llm-as-a-judge|LLM-as-a-judge]]).

### Strengths and limitations

**Strengths**
- Changing decoding needs no retraining and can strongly change output quality (Holtzman et al., 2020).
- Truncated sampling avoids both repetition and incoherence (Holtzman et al., 2020).
- Beam search finds higher-probability outputs than greedy decoding (Jurafsky & Martin, 2026).

**Limitations**
- Maximisation-based decoding degenerates on open-ended text (Holtzman et al., 2020).
- Sampling makes outputs non-deterministic, which complicates testing ([[regression-testing|regression testing]]).
- Parameters interact (temperature with top-p or min-p) and must be tuned per task (Nguyen et al., 2025).
- Beam search multiplies compute by the beam width.

### Comparison

| Strategy | Deterministic | Typical setting | Known problem |
|---|---|---|---|
| Greedy | yes | short factual answers | misses better sequences |
| Beam search | yes | translation, k = 5–10 | repetition in open text |
| Pure sampling | no | rarely used alone | incoherence from the tail |
| Top-k | no | k fixed | ignores distribution shape |
| Top-p (nucleus) | no | p = 0.95 in Holtzman et al. (2020) | still admits tail at high τ |
| Min-p | no | high-temperature creativity | needs base threshold |

Sources: Jurafsky & Martin (2026), Holtzman et al. (2020), Nguyen et al. (2025).

### In practice

Greedy decoding always produces the same string for the same context (Jurafsky & Martin, 2026), whereas sampled outputs vary between runs, so evaluations record the decoding parameters ([[llm-evaluation|LLM evaluation]]). Holtzman et al. (2020) used nucleus sampling with p = 0.95 in their comparisons. High temperatures combined with top-p can still produce incoherent text, which min-p was designed to counter (Nguyen et al., 2025).

### Key takeaway

Decoding turns next-token probabilities into text: greedy and beam search maximise likelihood and suit constrained tasks, while truncated sampling with top-k, top-p or min-p and a temperature gives open-ended text that is neither repetitive nor incoherent.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 7: Transformers and Pretraining (section 7.6, Decoding). [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/7.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 13: Machine Translation (section 13.4, Beam Search). [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/13.pdf)
- Holtzman, A., Buys, J., Du, L., Forbes, M. & Choi, Y. (2020). *The Curious Case of Neural Text Degeneration.* ICLR 2020. [arXiv:1904.09751](https://arxiv.org/abs/1904.09751)
- Fan, A., Lewis, M. & Dauphin, Y. (2018). *Hierarchical Neural Story Generation.* ACL 2018. [arXiv:1805.04833](https://arxiv.org/abs/1805.04833)
- Vijayakumar, A. K. et al. (2018). *Diverse Beam Search: Decoding Diverse Solutions from Neural Sequence Models.* AAAI 2018. [arXiv:1610.02424](https://arxiv.org/abs/1610.02424)
- Nguyen, M. N. et al. (2025). *Turning Up the Heat: Min-p Sampling for Creative and Coherent LLM Outputs.* ICLR 2025. [arXiv:2407.01082](https://arxiv.org/abs/2407.01082)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Sprachmodell liefert nur eine Wahrscheinlichkeitsverteilung über das nächste Token; eine Decoding-Strategie entscheidet, welches Token tatsächlich erzeugt wird, Schritt für Schritt bis zu einem End-Token (Jurafsky & Martin, 2026). Greedy Decoding und Beam Search suchen nach wahrscheinlichen Sequenzen und passen zu eng festgelegten Aufgaben wie der [[machine-translation|maschinellen Übersetzung]], während offene Textgenerierung Sampling nutzt, meist mit Top-k, Top-p (Nucleus) oder Min-p beschnitten und mit einer Temperatur geformt, weil das Maximieren der Wahrscheinlichkeit langweiligen und repetitiven Text erzeugt (Holtzman et al., 2020; Jurafsky & Martin, 2026). Die Wahl des Decodings kann die Qualität der Ausgabe selbst beim selben Modell drastisch verändern (Holtzman et al., 2020).

### Funktionsweise

```text
Kontext w<t ──► LLM ──► Logits u ──► softmax(u / τ) ──► P(w | w<t)
                                                │
          ┌─────────────────────────────────────┼──────────────────────────────────────┐
          ▼                                     ▼                                      ▼
   Greedy: Argmax               Beam Search: k beste                Sampling: Ende der Verteilung abschneiden, dann ziehen
                                Teilsequenzen behalten (Log-Wahrsch.)  Top-k │ Top-p (Nucleus) │ Min-p
          └─────────────────────────────────────┬──────────────────────────────────────┘
                                                ▼
                       Token anhängen, wiederholen bis EOS oder Längengrenze
```

#### 1. Greedy Decoding

Greedy Decoding wählt in jedem Schritt das wahrscheinlichste Token; es ist deterministisch, sodass derselbe Kontext immer dieselbe Zeichenkette ergibt (Jurafsky & Martin, 2026). Seine Schwäche: Eine lokal beste Wahl kann eine bessere Fortsetzung ausschließen; im Beispiel von Jurafsky und Martin wird die wahrscheinlichste Sequenz „ok ok EOS“ verfehlt, weil „yes“ im ersten Schritt die höchste Wahrscheinlichkeit hat (Jurafsky & Martin, 2026).

#### 2. Beam Search

Beam Search behält in jedem Schritt die k besten Hypothesen (Teilausgaben mit ihren Log-Wahrscheinlichkeiten), erweitert jede um jedes Token des Vokabulars, bewertet die k × |V| Erweiterungen und beschneidet sie wieder auf k; k ist die Beam-Breite, in der maschinellen Übersetzung typischerweise 5 bis 10 (Jurafsky & Martin, 2026). Weil längere Ausgaben niedrigere Wahrscheinlichkeiten ansammeln, werden die Scores längennormalisiert, etwa durch Teilen der Log-Wahrscheinlichkeit durch die Zahl der Tokens (Jurafsky & Martin, 2026). Beam-Ausgaben unterscheiden sich oft nur wenig; Diverse Beam Search ergänzt das Ziel um einen Diversitätsterm und fand dabei sogar bessere Top-1-Lösungen (Vijayakumar et al., 2018). Minimum-Bayes-Risk-Decoding wählt stattdessen den Kandidaten mit dem geringsten erwarteten Fehler unter einer Evaluationsmetrik und kann besser funktionieren als Beam Search (Jurafsky & Martin, 2026).

#### 3. Warum das Maximieren der Wahrscheinlichkeit entartet

Bei offener Generierung führen Beam Search und Greedy Decoding zur Degeneration: Ausgaben, die langweilig, inkohärent oder in Wiederholungsschleifen gefangen sind, selbst mit GPT-2 Large; die Wahrscheinlichkeit einer wiederholten Phrase steigt mit jeder Wiederholung, eine positive Rückkopplung (Holtzman et al., 2020). Menschlicher Text ist nicht der wahrscheinlichste Text; seine Wahrscheinlichkeit pro Token schwankt stärker (Holtzman et al., 2020). Reines Sampling aus der vollen Verteilung scheitert in die Gegenrichtung und erzeugt inkohärenten Text, weil das „unzuverlässige Ende“ aus Zehntausenden wenig wahrscheinlicher Tokens in der Summe überrepräsentiert ist (Holtzman et al., 2020; Jurafsky & Martin, 2026).

#### 4. Beschnittenes Sampling

- **Temperatur:** Teilt man die Logits vor der [[softmax|Softmax]] durch τ, wird die Verteilung für τ < 1 schärfer und für τ > 1 flacher; τ → 0 nähert sich dem Greedy Decoding (Jurafsky & Martin, 2026).
- **Top-k:** die k wahrscheinlichsten Tokens behalten, renormalisieren und ziehen; k = 1 ist Greedy (Jurafsky & Martin, 2026; Fan et al., 2018). Weil k fest ist, die Form der Verteilung sich aber ändert, können die k besten Tokens den Großteil oder nur einen kleinen Teil der Wahrscheinlichkeitsmasse abdecken (Jurafsky & Martin, 2026).
- **Top-p (Nucleus):** die kleinste Menge von Tokens behalten, deren kumulierte Wahrscheinlichkeit p erreicht, was die Größe des Pools an die Sicherheit des Modells anpasst (Holtzman et al., 2020). Top-k und Top-p werden oft kombiniert, Top-k zuerst als harter Filter (Jurafsky & Martin, 2026).
- **Min-p:** Tokens behalten, deren Wahrscheinlichkeit mindestens `p_base × p_max` beträgt, eine mit der Wahrscheinlichkeit des besten Tokens skalierte Schwelle, sodass der Pool wächst, wenn das Modell unsicher ist; es verbesserte Qualität und Vielfalt vor allem bei hohen Temperaturen für Modelle von 1 bis 123 Milliarden Parametern und wurde von Frameworks wie Hugging Face Transformers und [[llm-inference-serving|vLLM]] übernommen (Nguyen et al., 2025).

#### 5. Qualität gegen Vielfalt

Verfahren, die die wahrscheinlichsten Tokens betonen, erzeugen Ausgaben, die Menschen als genauer, kohärenter und faktentreuer, aber auch als langweiliger und repetitiver bewerten; mehr Gewicht auf Tokens mittlerer Wahrscheinlichkeit ist kreativer und vielfältiger, aber weniger faktentreu (Jurafsky & Martin, 2026). Beam Search funktioniert gut bei eng festgelegten Aufgaben wie der maschinellen Übersetzung, während bei den meisten anderen Aufgaben Text aus Sampling-Verfahren bevorzugt wird, die etwas Vielfalt hinzufügen (Jurafsky & Martin, 2026).

#### Ursprung und Varianten

Beam Search schlug Lowerre 1976 erstmals vor, und das Sampling aus Sprachmodellen geht auf Shannon (1948) zurück (Jurafsky & Martin, 2026). Top-k-Sampling wurde für Story Generation (Fan et al., 2018) und GPT-2 populär, Nucleus Sampling führten Holtzman et al. (2020) ein und Min-p Nguyen et al. (2025). Decoding lässt sich außerdem ohne Änderung der Ausgabeverteilung per [[speculative-decoding|Speculative Decoding]] beschleunigen oder mehrfach ziehen und per Mehrheitsentscheid zusammenführen wie bei [[self-consistency|Self-Consistency]].

### Wann einsetzen

- Greedy oder niedrige Temperatur für Faktenantworten, Extraktion und strukturierte Ausgaben ([[tool-calling|Tool Calling]]).
- Beam Search für maschinelle Übersetzung und andere Aufgaben, deren Ausgabe eng von der Eingabe bestimmt ist (Jurafsky & Martin, 2026).
- Top-p-, Top-k- oder Min-p-Sampling mit mittlerer Temperatur für offenen Text, Dialog und kreatives Schreiben (Holtzman et al., 2020; Nguyen et al., 2025).
- Mehrere Stichproben, wenn Antworten später verglichen oder abgestimmt werden ([[self-consistency|Self-Consistency]], [[llm-as-a-judge|LLM-as-a-Judge]]).

### Stärken und Grenzen

**Stärken**
- Ein anderes Decoding braucht kein neues Training und kann die Qualität der Ausgabe stark verändern (Holtzman et al., 2020).
- Beschnittenes Sampling vermeidet sowohl Wiederholung als auch Inkohärenz (Holtzman et al., 2020).
- Beam Search findet wahrscheinlichere Ausgaben als Greedy Decoding (Jurafsky & Martin, 2026).

**Grenzen**
- Maximierendes Decoding entartet bei offenem Text (Holtzman et al., 2020).
- Sampling macht Ausgaben nicht deterministisch, was das Testen erschwert ([[regression-testing|Regressionstests]]).
- Parameter wirken zusammen (Temperatur mit Top-p oder Min-p) und müssen pro Aufgabe eingestellt werden (Nguyen et al., 2025).
- Beam Search vervielfacht den Rechenaufwand um die Beam-Breite.

### Vergleich

| Strategie | Deterministisch | Typisches Setting | Bekanntes Problem |
|---|---|---|---|
| Greedy | ja | kurze Faktenantworten | verfehlt bessere Sequenzen |
| Beam Search | ja | Übersetzung, k = 5–10 | Wiederholungen bei offenem Text |
| Reines Sampling | nein | selten allein genutzt | Inkohärenz durch das Verteilungsende |
| Top-k | nein | k fest | ignoriert die Form der Verteilung |
| Top-p (Nucleus) | nein | p = 0,95 bei Holtzman et al. (2020) | lässt bei hohem τ noch das Ende zu |
| Min-p | nein | Kreativität bei hoher Temperatur | braucht eine Grundschwelle |

Quellen: Jurafsky & Martin (2026), Holtzman et al. (2020), Nguyen et al. (2025).

### In der Praxis

Greedy Decoding erzeugt für denselben Kontext immer dieselbe Zeichenkette (Jurafsky & Martin, 2026), während gezogene Ausgaben zwischen Läufen variieren; Evaluationen halten daher die Decoding-Parameter fest ([[llm-evaluation|LLM-Evaluation]]). Holtzman et al. (2020) nutzten in ihren Vergleichen Nucleus Sampling mit p = 0,95. Hohe Temperaturen zusammen mit Top-p können weiterhin inkohärenten Text erzeugen, wogegen Min-p entwickelt wurde (Nguyen et al., 2025).

### Merksatz

Decoding macht aus Wahrscheinlichkeiten für das nächste Token Text: Greedy und Beam Search maximieren die Wahrscheinlichkeit und passen zu eng festgelegten Aufgaben, beschnittenes Sampling mit Top-k, Top-p oder Min-p und einer Temperatur liefert offenen Text, der weder repetitiv noch inkohärent ist.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 7: Transformers and Pretraining (Abschnitt 7.6, Decoding). [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/7.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 13: Machine Translation (Abschnitt 13.4, Beam Search). [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/13.pdf)
- Holtzman, A., Buys, J., Du, L., Forbes, M. & Choi, Y. (2020). *The Curious Case of Neural Text Degeneration.* ICLR 2020. [arXiv:1904.09751](https://arxiv.org/abs/1904.09751)
- Fan, A., Lewis, M. & Dauphin, Y. (2018). *Hierarchical Neural Story Generation.* ACL 2018. [arXiv:1805.04833](https://arxiv.org/abs/1805.04833)
- Vijayakumar, A. K. et al. (2018). *Diverse Beam Search: Decoding Diverse Solutions from Neural Sequence Models.* AAAI 2018. [arXiv:1610.02424](https://arxiv.org/abs/1610.02424)
- Nguyen, M. N. et al. (2025). *Turning Up the Heat: Min-p Sampling for Creative and Coherent LLM Outputs.* ICLR 2025. [arXiv:2407.01082](https://arxiv.org/abs/2407.01082)
