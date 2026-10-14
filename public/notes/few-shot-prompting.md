---
title_en: Few-Shot Prompting
title_de: Few-Shot-Prompting
entity_type: Method
aliases:
- Few-shot prompting
- In-context learning
- Few-shot learning with language models
sources:
- https://arxiv.org/abs/2005.14165
- https://arxiv.org/abs/2102.09690
- https://arxiv.org/abs/2202.12837
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Few-shot prompting gives a language model a few demonstrations of a task in the prompt, pairs of context and desired completion, followed by a new input whose completion the model should produce, without any weight updates (Brown et al., 2020). Brown et al. called this ability "in-context learning" and showed with GPT-3 that it improves strongly with model size: few-shot performance grew faster with scale than zero-shot performance ([[gpt|GPT]]). Few-shot prompting needs far less task-specific data than fine-tuning, but results can vary from near chance to near state of the art depending on the format, the choice and even the order of the examples (Zhao et al., 2021). The demonstrations seem to work mainly by showing the label space, the input distribution and the format; randomly replacing their labels barely hurt performance in [[classification|classification]] and multiple-choice tasks (Min et al., 2022).

### How it works

```text
[optional task description]  "Translate English to French:"
demonstration 1              sea otter => loutre de mer
demonstration 2              peppermint => menthe poivrée
...  (K examples)
query                        cheese =>
model completes              fromage
no gradient update – the "learning" happens in the forward pass over the context
```

#### 1. Zero-shot, one-shot, few-shot

Brown et al. (2020) place the settings on a spectrum of how much task-specific data they use: fine-tuning updates the weights on thousands to hundreds of thousands of labelled examples; few-shot gives K demonstrations of context and completion at inference time, typically 10 to 100 for GPT-3, as many as fit in its context window of 2,048 tokens; one-shot gives a single demonstration plus a task description; zero-shot gives only a natural-language instruction. Zero-shot is the most convenient but also the hardest setting, because the format of a task can be unclear without examples (Brown et al., 2020).

#### 2. In-context learning

Brown et al. (2020) describe pre-training as an outer loop in which the model acquires broad skills and pattern recognition, and in-context learning as an inner loop within a single forward pass over the sequence, in which the model adapts to or recognises the task. On TriviaQA, GPT-3 reached 64.3% zero-shot, 68.0% one-shot and 71.2% few-shot, in a closed-book setting without fine-tuning (Brown et al., 2020). Whether the model learns the task "from scratch" or recognises a task seen during pre-training remains unclear and may vary by task (Brown et al., 2020).

#### 3. What the demonstrations contribute

Min et al. (2022) found, across 12 models including GPT-3, that demonstrations with random labels performed almost as well as demonstrations with correct labels on classification and multiple-choice tasks. The main drivers were that demonstrations show examples of the label space, the distribution of the input text and the overall format of the sequence (Min et al., 2022).

#### 4. Instability and calibration

The prompt format, the training examples and their order can make accuracy vary from near chance to near state of the art (Zhao et al., 2021). Zhao et al. trace this to biases of the model towards certain answers, for example those near the end of the prompt or frequent in the pre-training data. Their contextual calibration estimates this bias with a content-free input such as "N/A" and fits calibration parameters that make the prediction for it uniform; this improved the average accuracy of GPT-3 and GPT-2 by up to 30.0 percentage points and reduced variance across prompts (Zhao et al., 2021).

#### Origin and variants

Few-shot prompting became prominent with GPT-3 (Brown et al., 2020); Brown et al. note that it is related to few-shot learning elsewhere in machine learning, since both learn from a broad distribution of tasks and then adapt quickly to a new one. Few-shot [[chain-of-thought-prompting|chain-of-thought prompting]] adds intermediate reasoning steps to the demonstrations.

### When to use it

- Tasks for which a few examples are easy to write but a fine-tuning dataset is not available (Brown et al., 2020).
- Fixing an output format, label set or style that is hard to describe in words alone (Brown et al., 2020; Min et al., 2022).
- Prototyping before deciding whether fine-tuning is worth it ([[llm-adaptation|LLM adaptation]]).

### Strengths and limitations

**Strengths**
- No training and only a small amount of task-specific data (Brown et al., 2020).
- Less risk of learning an overly narrow distribution than fine-tuning on a large but narrow dataset (Brown et al., 2020).
- Benefits grow with model size (Brown et al., 2020).

**Limitations**
- Results were much worse than state-of-the-art fine-tuned models on many tasks in 2020, and GPT-3 did little better than chance few-shot on some comparison tasks such as WiC and ANLI (Brown et al., 2020).
- Sensitive to format, choice and order of examples (Zhao et al., 2021).
- Demonstrations take up context and add cost to every request.
- Benchmark results can be inflated if test data appeared in the pre-training corpus (Brown et al., 2020).

### Comparison

| Setting | Task-specific data | Weight updates | Typical use |
|---|---|---|---|
| Zero-shot | instruction only | no | simple, well-described tasks |
| One-shot | one demonstration + instruction | no | tasks communicated like to a human worker |
| Few-shot | about 10–100 demonstrations (GPT-3) | no | format or label set matters |
| Fine-tuning | thousands of examples or more | yes | high, stable task performance |

Source: Brown et al. (2020).

### In practice

Keep the format of the demonstrations identical to the expected output, cover all labels, and test several orders and selections of examples before trusting a prompt (Zhao et al., 2021). Since correct labels mattered little in the study by Min et al. (2022), the format and the realistic input distribution deserve the most care. For classification with an LLM, calibrating against a content-free input can remove systematic label bias (Zhao et al., 2021). Prompt variants are compared on a fixed evaluation set before one is chosen ([[prompt-engineering|prompt engineering]]).

### Key takeaway

Few-shot prompting teaches a task through a handful of examples in the prompt instead of training; it works better with larger models, but its results depend strongly on the format, selection and order of the examples.

### Sources

- Brown, T. B. et al. (2020). Language Models are Few-Shot Learners. *NeurIPS 2020*. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)
- Zhao, T. Z., Wallace, E., Feng, S., Klein, D. & Singh, S. (2021). Calibrate Before Use: Improving Few-Shot Performance of Language Models. *ICML 2021*. [arXiv:2102.09690](https://arxiv.org/abs/2102.09690)
- Min, S., Lyu, X., Holtzman, A., Artetxe, M., Lewis, M., Hajishirzi, H. & Zettlemoyer, L. (2022). Rethinking the Role of Demonstrations: What Makes In-Context Learning Work? *EMNLP 2022*. [arXiv:2202.12837](https://arxiv.org/abs/2202.12837)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Few-Shot-Prompting gibt einem Sprachmodell im Prompt einige Demonstrationen einer Aufgabe, Paare aus Kontext und gewünschter Vervollständigung, gefolgt von einer neuen Eingabe, deren Vervollständigung das Modell erzeugen soll, ohne Gewichtsänderungen (Brown et al., 2020). Brown et al. nannten diese Fähigkeit „In-Context Learning“ und zeigten mit GPT-3, dass sie stark mit der Modellgröße zunimmt: Die Few-Shot-Leistung wuchs mit der Größe schneller als die Zero-Shot-Leistung ([[gpt|GPT]]). Few-Shot-Prompting braucht weit weniger aufgabenspezifische Daten als Fine-Tuning, doch die Ergebnisse können je nach Format, Auswahl und sogar Reihenfolge der Beispiele von nahe Zufall bis nahe am Stand der Technik schwanken (Zhao et al., 2021). Die Demonstrationen wirken offenbar vor allem, indem sie den Label-Raum, die Verteilung der Eingaben und das Format zeigen; zufällig ersetzte Labels verschlechterten die Leistung bei Klassifikations- und Multiple-Choice-Aufgaben kaum (Min et al., 2022).

### Funktionsweise

```text
[optionale Aufgabenbeschreibung]  "Translate English to French:"
Demonstration 1                   sea otter => loutre de mer
Demonstration 2                   peppermint => menthe poivrée
...  (K Beispiele)
Anfrage                           cheese =>
Modell vervollständigt            fromage
keine Gradientenänderung – das „Lernen“ geschieht im Vorwärtsdurchlauf über den Kontext
```

#### 1. Zero-Shot, One-Shot, Few-Shot

Brown et al. (2020) ordnen die Varianten auf einem Spektrum danach ein, wie viele aufgabenspezifische Daten sie nutzen: Fine-Tuning ändert die Gewichte anhand von Tausenden bis Hunderttausenden gelabelten Beispielen; Few-Shot gibt zur Inferenzzeit K Demonstrationen aus Kontext und Vervollständigung, bei GPT-3 typischerweise 10 bis 100, so viele, wie in das Kontextfenster von 2.048 Token passen; One-Shot gibt eine einzige Demonstration plus Aufgabenbeschreibung; Zero-Shot gibt nur eine Anweisung in natürlicher Sprache. Zero-Shot ist am bequemsten, aber auch am schwierigsten, weil das Format einer Aufgabe ohne Beispiele unklar sein kann (Brown et al., 2020).

#### 2. In-Context Learning

Brown et al. (2020) beschreiben das Vortraining als äußere Schleife, in der das Modell breite Fähigkeiten und Mustererkennung erwirbt, und In-Context Learning als innere Schleife innerhalb eines einzigen Vorwärtsdurchlaufs über die Sequenz, in der sich das Modell an die Aufgabe anpasst oder sie erkennt. Bei TriviaQA erreichte GPT-3 64,3 % Zero-Shot, 68,0 % One-Shot und 71,2 % Few-Shot, im Closed-Book-Setting ohne Fine-Tuning (Brown et al., 2020). Ob das Modell die Aufgabe „von Grund auf“ lernt oder eine im Vortraining gesehene Aufgabe wiedererkennt, bleibt unklar und kann je nach Aufgabe variieren (Brown et al., 2020).

#### 3. Was die Demonstrationen beitragen

Min et al. (2022) stellten bei 12 Modellen einschließlich GPT-3 fest, dass Demonstrationen mit zufälligen Labels bei Klassifikations- und Multiple-Choice-Aufgaben fast so gut abschnitten wie Demonstrationen mit korrekten Labels. Entscheidend war vor allem, dass Demonstrationen Beispiele für den Label-Raum, die Verteilung des Eingabetexts und das Gesamtformat der Sequenz zeigen (Min et al., 2022).

#### 4. Instabilität und Kalibrierung

Prompt-Format, Trainingsbeispiele und ihre Reihenfolge können die Genauigkeit von nahe Zufall bis nahe am Stand der Technik schwanken lassen (Zhao et al., 2021). Zhao et al. führen dies auf Verzerrungen des Modells zugunsten bestimmter Antworten zurück, etwa solcher am Ende des Prompts oder solcher, die in den Vortrainingsdaten häufig sind. Ihre kontextuelle Kalibrierung schätzt diese Verzerrung mit einer inhaltsfreien Eingabe wie „N/A“ und passt Kalibrierungsparameter so an, dass die Vorhersage dafür gleichverteilt ist; das verbesserte die durchschnittliche Genauigkeit von GPT-3 und GPT-2 um bis zu 30,0 Prozentpunkte und verringerte die Schwankung zwischen Prompts (Zhao et al., 2021).

#### Herkunft und Varianten

Few-Shot-Prompting wurde mit GPT-3 bekannt (Brown et al., 2020); Brown et al. merken an, dass es mit Few-Shot-Learning in anderen Bereichen des maschinellen Lernens verwandt ist, da beide aus einer breiten Verteilung von Aufgaben lernen und sich dann schnell an eine neue anpassen. Few-Shot-[[chain-of-thought-prompting|Chain-of-Thought-Prompting]] ergänzt die Demonstrationen um Zwischenschritte des Denkens.

### Wann einsetzen

- Aufgaben, für die sich einige Beispiele leicht schreiben lassen, aber kein Datensatz für Fine-Tuning vorliegt (Brown et al., 2020).
- Festlegen eines Ausgabeformats, Label-Satzes oder Stils, der sich in Worten allein schwer beschreiben lässt (Brown et al., 2020; Min et al., 2022).
- Prototyping, bevor entschieden wird, ob sich Fine-Tuning lohnt ([[llm-adaptation|LLM-Anpassung]]).

### Stärken und Grenzen

**Stärken**
- Kein Training und nur wenige aufgabenspezifische Daten (Brown et al., 2020).
- Geringeres Risiko als beim Fine-Tuning auf einem großen, aber engen Datensatz, eine zu enge Verteilung zu lernen (Brown et al., 2020).
- Der Nutzen wächst mit der Modellgröße (Brown et al., 2020).

**Grenzen**
- Die Ergebnisse lagen 2020 bei vielen Aufgaben deutlich unter dem Stand der Technik mit Fine-Tuning, und GPT-3 war Few-Shot bei einigen Vergleichsaufgaben wie WiC und ANLI kaum besser als Zufall (Brown et al., 2020).
- Empfindlich gegenüber Format, Auswahl und Reihenfolge der Beispiele (Zhao et al., 2021).
- Demonstrationen belegen Kontext und erhöhen die Kosten jeder Anfrage.
- Benchmark-Ergebnisse können überhöht sein, wenn Testdaten im Vortrainingskorpus vorkamen (Brown et al., 2020).

### Vergleich

| Variante | Aufgabenspezifische Daten | Gewichtsänderung | Typischer Einsatz |
|---|---|---|---|
| Zero-Shot | nur Anweisung | nein | einfache, gut beschriebene Aufgaben |
| One-Shot | eine Demonstration + Anweisung | nein | Aufgaben, die man auch einem Menschen so erklären würde |
| Few-Shot | etwa 10–100 Demonstrationen (GPT-3) | nein | Format oder Label-Satz ist wichtig |
| Fine-Tuning | Tausende Beispiele oder mehr | ja | hohe, stabile Aufgabenleistung |

Quelle: Brown et al. (2020).

### In der Praxis

Das Format der Demonstrationen sollte genau der erwarteten Ausgabe entsprechen, alle Labels abdecken, und verschiedene Reihenfolgen und Auswahlen von Beispielen sollten getestet werden, bevor einem Prompt vertraut wird (Zhao et al., 2021). Da korrekte Labels in der Studie von Min et al. (2022) wenig ausmachten, verdienen das Format und eine realistische Eingabeverteilung die meiste Sorgfalt. Bei der [[classification|Klassifikation]] mit einem LLM kann die Kalibrierung gegen eine inhaltsfreie Eingabe systematische Label-Verzerrungen beseitigen (Zhao et al., 2021). Promptvarianten werden auf einem festen Evaluierungssatz verglichen, bevor eine ausgewählt wird ([[prompt-engineering|Prompt Engineering]]).

### Merksatz

Few-Shot-Prompting vermittelt eine Aufgabe über eine Handvoll Beispiele im Prompt statt über Training; es funktioniert mit größeren Modellen besser, doch die Ergebnisse hängen stark von Format, Auswahl und Reihenfolge der Beispiele ab.

### Quellen

- Brown, T. B. et al. (2020). Language Models are Few-Shot Learners. *NeurIPS 2020*. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)
- Zhao, T. Z., Wallace, E., Feng, S., Klein, D. & Singh, S. (2021). Calibrate Before Use: Improving Few-Shot Performance of Language Models. *ICML 2021*. [arXiv:2102.09690](https://arxiv.org/abs/2102.09690)
- Min, S., Lyu, X., Holtzman, A., Artetxe, M., Lewis, M., Hajishirzi, H. & Zettlemoyer, L. (2022). Rethinking the Role of Demonstrations: What Makes In-Context Learning Work? *EMNLP 2022*. [arXiv:2202.12837](https://arxiv.org/abs/2202.12837)
