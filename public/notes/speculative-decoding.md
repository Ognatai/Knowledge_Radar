---
title_en: Speculative Decoding
title_de: Speculative Decoding
entity_type: Method
aliases:
- Speculative decoding
- Speculative sampling
- Speculative Sampling
- Draft-and-verify decoding
sources:
- https://arxiv.org/abs/2211.17192
- https://arxiv.org/abs/2302.01318
- https://arxiv.org/abs/2401.10774
- https://arxiv.org/abs/2401.15077
- https://arxiv.org/abs/2607.05147
- https://github.com/deepseek-ai/DeepSpec
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Speculative decoding speeds up text generation of a large autoregressive model without changing its outputs: a cheap draft model proposes several tokens, the large target model checks all of them in one parallel forward pass, and a modified rejection sampling rule keeps the longest acceptable prefix so that the result follows exactly the target model's distribution (Leviathan et al., 2022; Chen et al., 2023). This gave 2 to 3 times faster decoding for T5-XXL and 2 to 2.5 times for the 70-billion-parameter Chinchilla (Leviathan et al., 2022; Chen et al., 2023). Later methods replace the separate draft model with extra decoding heads (Medusa) or a light feature-level extrapolator (EAGLE), and DSpark from DeepSeek (2026) combines a parallel drafter with a small sequential module and verifies only as many tokens as current server load makes worthwhile, accelerating per-user generation in DeepSeek-V4 by 60 to 85 percent (Cai et al., 2024; Li et al., 2024; Cheng et al., 2026).

### How it works

```text
prefix
 ▼
draft model M_q proposes γ tokens  x1 … xγ   (cheap, sequential or parallel)
 ▼
target model M_p scores prefix+x1 … prefix+xγ in ONE parallel pass
 ▼
accept/reject left to right:
   keep xi if q(xi) ≤ p(xi), else keep with probability p(xi)/q(xi)
   first rejection → resample from norm(max(0, p − q)) and stop
   all accepted   → one bonus token from M_p
 ▼
append accepted tokens → repeat
```

#### 1. Why decoding is slow

An autoregressive model generates one token per forward pass, so decoding K tokens takes K serial runs of the model (Leviathan et al., 2022). Each step has to move the full model parameters from high-bandwidth memory to the accelerator, which makes decoding memory-bound rather than compute-bound (Cai et al., 2024). Chen et al. (2023) observed that scoring a short continuation in parallel takes about as long as sampling a single token from the large model, which leaves spare compute per step. The idea of speculative decoding is to use it: some tokens are easy and can be guessed by a much smaller model (Leviathan et al., 2022).

#### 2. Drafting

A draft model `M_q` with distribution `q` proposes a block of `γ` tokens after the current prefix (Leviathan et al., 2022). In the original methods it is a separate, smaller and faster language model (Leviathan et al., 2022; Chen et al., 2023). Its quality decides the speed-up: the more of its tokens the target model accepts, the more tokens each expensive pass yields, while a slow drafter eats the gain. Drafting latency of autoregressive drafters grows linearly with the block size, which forces short blocks and shallow drafters (Cheng et al., 2026).

#### 3. Parallel verification

The target model `M_p` with distribution `p` runs once on the prefix extended by all draft tokens, which gives `p` for every draft position at the same time (Leviathan et al., 2022). This single pass replaces up to `γ + 1` sequential passes of the target model.

#### 4. Acceptance rule

To sample `x ~ p(x)`, the method samples `x ~ q(x)` instead, keeps it if `q(x) ≤ p(x)`, and otherwise rejects it with probability `1 − p(x)/q(x)` and samples again from the adjusted distribution `p'(x) = norm(max(0, p(x) − q(x)))` (Leviathan et al., 2022). For any `p` and `q`, tokens sampled this way follow exactly `p` (Leviathan et al., 2022); Chen et al. (2023) describe the same modified rejection sampling and note that it preserves the target distribution within hardware numerics. Tokens are checked left to right; the first rejection ends the round, and if all draft tokens are accepted, the target model adds one more token from its own pass (Cheng et al., 2026). The output is therefore identical in distribution to normal decoding, which is why the method needs no retraining or change to the target model (Leviathan et al., 2022).

#### 5. Drafters built into the target model

Maintaining a separate draft model is inconvenient, so Medusa adds extra decoding heads to the target model that predict several following tokens in parallel, builds several candidate continuations and verifies them together with tree-based attention (Cai et al., 2024). Medusa-1 trains only the heads on a frozen model and achieves over 2.2 times speed-up without loss in quality; Medusa-2 trains heads and model together for 2.3 to 3.6 times, at the cost of a special training recipe (Cai et al., 2024). EAGLE drafts at the level of second-to-top-layer features instead of tokens and adds the token sequence advanced by one step to resolve feature uncertainty; for LLaMA2-Chat 70B it reported 2.7 to 3.5 times lower latency and doubled throughput while keeping the output distribution (Li et al., 2024).

#### 6. DSpark: semi-autoregressive drafting and scheduled verification

Parallel drafters produce a whole block in one forward pass, so their latency hardly depends on block size, but because each position is predicted independently, acceptance decays quickly towards the end of the block; verifying long blocks also wastes batch capacity on tokens that are likely to be rejected, which hurts throughput in busy serving systems (Cheng et al., 2026). DSpark, by DeepSeek-AI and Peking University, keeps the expensive draft backbone parallel and appends a lightweight sequential head that models dependencies within the block (semi-autoregressive generation), and adds confidence-scheduled verification: a confidence head estimates the probability that each prefix survives, and a hardware-aware scheduler uses engine throughput profiles to decide per request how many draft tokens are worth verifying (Cheng et al., 2026). On Qwen3 4B, 8B and 14B targets it increased the average accepted length by 26.7 to 30.9 percent over the autoregressive drafter Eagle3 and by 16.3 to 18.4 percent over the parallel drafter DFlash; in the DeepSeek-V4 serving system under live traffic it raised per-user generation speed by 60 to 85 percent (V4-Flash) and 57 to 78 percent (V4-Pro) over the previous production baseline MTP-1 at matched throughput (Cheng et al., 2026). The checkpoints and the training code base DeepSpec, which also includes Eagle3 and DFlash, are open source (Cheng et al., 2026; DeepSpec repository).

#### Origin and variants

Leviathan et al. (2022) and Chen et al. (2023) independently introduced speculative decoding and speculative sampling with exact rejection sampling, building on earlier blockwise parallel decoding (Cheng et al., 2026). Variants differ mainly in the drafter: separate small models, extra heads (Medusa), feature extrapolation (EAGLE, Eagle3), parallel drafters (DFlash) and semi-autoregressive drafters with load-aware verification (DSpark).

### When to use it

- When generation latency per user matters, for example in chat and [[voice-agents|voice agents]], and the model is served on hardware with spare compute per decoding step (Chen et al., 2023).
- When the output must stay exactly as it would be without acceleration, which rules out lossy speed-ups (Leviathan et al., 2022).
- When a suitable drafter exists or can be trained for the target model, for example released DSpark or EAGLE checkpoints (Cheng et al., 2026; Li et al., 2024).

### Strengths and limitations

**Strengths**
- Lossless: the output distribution of the target model is preserved (Leviathan et al., 2022; Chen et al., 2023).
- Works with existing models without retraining or architecture changes when a separate drafter is used (Leviathan et al., 2022).
- Typical speed-ups of 2 to 3.6 times, and more per user in production serving (Cai et al., 2024; Li et al., 2024; Cheng et al., 2026).

**Limitations**
- The gain depends on how often draft tokens are accepted; hard text with few predictable tokens gives little speed-up.
- Verifying rejected tokens costs compute, which can reduce throughput under high load unless verification length is adapted (Cheng et al., 2026).
- Built-in drafters need training per target model, and joint training such as Medusa-2 needs a recipe that preserves the model's capabilities (Cai et al., 2024).

### Comparison

| Method | Faster how | Output unchanged? | Example |
|---|---|---|---|
| Speculative decoding | draft and verify in parallel | yes | Leviathan et al. (2022), DSpark |
| [[quantisation\|Quantisation]] | lower-precision weights | no, approximate | INT8, 4-bit |
| [[knowledge-distillation\|Knowledge distillation]] | smaller student model | no, different model | [[distilbert\|DistilBERT]] |
| [[model-compression\|Model compression]] | pruning and other reductions | no | pruning |
| [[llm-cost-optimisation\|Caching and routing]] | avoid or shorten calls | depends | prompt caching |

Sources: Leviathan et al. (2022); Chen et al. (2023); Cheng et al. (2026).

### In practice

DeepSpec releases DSpark, DFlash and Eagle3 drafters for Qwen3-4B, Qwen3-8B, Qwen3-14B and gemma-4-12B-it and asks anyone citing its results to align with the repository's training settings (DeepSpec repository). The relevant metrics are the accepted length per round, per-user tokens per second and total throughput, measured together because a setting that speeds up one user can slow the system down under load (Cheng et al., 2026). Deployment and serving are covered in [[mlops-and-deployment|MLOps and deployment]] and cost in [[llm-cost-optimisation|LLM cost optimisation]].

### Key takeaway

Speculative decoding lets a cheap drafter guess several tokens that the large model verifies in one pass, which speeds up generation without changing what the model would have produced.

### Sources

- Leviathan, Y., Kalman, M. & Matias, Y. (2022). *Fast Inference from Transformers via Speculative Decoding.* arXiv:2211.17192. [arXiv](https://arxiv.org/abs/2211.17192)
- Chen, C., Borgeaud, S., Irving, G., Lespiau, J.-B., Sifre, L. & Jumper, J. (2023). *Accelerating Large Language Model Decoding with Speculative Sampling.* arXiv:2302.01318. [arXiv](https://arxiv.org/abs/2302.01318)
- Cai, T., Li, Y., Geng, Z., Peng, H., Lee, J. D., Chen, D. & Dao, T. (2024). *Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads.* arXiv:2401.10774. [arXiv](https://arxiv.org/abs/2401.10774)
- Li, Y., Wei, F., Zhang, C. & Zhang, H. (2024). *EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty.* arXiv:2401.15077. [arXiv](https://arxiv.org/abs/2401.15077)
- Cheng, X., Yu, X., Shao, C., Li, J., Xiong, Y. et al. (2026). *DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation.* arXiv:2607.05147. [arXiv](https://arxiv.org/abs/2607.05147)
- DeepSeek-AI (2026). *DeepSpec: a full-stack codebase for training and evaluating speculative decoding algorithms.* GitHub repository. [github.com](https://github.com/deepseek-ai/DeepSpec)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Speculative Decoding beschleunigt die Textgenerierung eines großen autoregressiven Modells, ohne seine Ausgaben zu verändern: Ein günstiges Draft-Modell schlägt mehrere Tokens vor, das große Zielmodell prüft sie alle in einem parallelen Forward Pass, und eine abgewandelte Rejection-Sampling-Regel behält das längste annehmbare Präfix, sodass das Ergebnis genau der Verteilung des Zielmodells folgt (Leviathan et al., 2022; Chen et al., 2023). Das ergab für T5-XXL eine 2- bis 3-mal schnellere Dekodierung und für das 70-Milliarden-Parameter-Modell Chinchilla eine 2- bis 2,5-mal schnellere (Leviathan et al., 2022; Chen et al., 2023). Spätere Verfahren ersetzen das separate Draft-Modell durch zusätzliche Decoding-Köpfe (Medusa) oder einen leichten Extrapolator auf Feature-Ebene (EAGLE), und DSpark von DeepSeek (2026) verbindet einen parallelen Drafter mit einem kleinen sequenziellen Modul und prüft nur so viele Tokens, wie es die aktuelle Serverlast lohnend macht; in DeepSeek-V4 beschleunigte das die Generierung je Nutzer um 60 bis 85 Prozent (Cai et al., 2024; Li et al., 2024; Cheng et al., 2026).

### Funktionsweise

```text
Präfix
 ▼
Draft-Modell M_q schlägt γ Tokens vor  x1 … xγ   (günstig, sequenziell oder parallel)
 ▼
Zielmodell M_p bewertet Präfix+x1 … Präfix+xγ in EINEM parallelen Durchlauf
 ▼
Annehmen/Verwerfen von links nach rechts:
   xi behalten, wenn q(xi) ≤ p(xi), sonst mit Wahrscheinlichkeit p(xi)/q(xi)
   erste Ablehnung → neu ziehen aus norm(max(0, p − q)) und stoppen
   alle angenommen → ein Bonus-Token von M_p
 ▼
angenommene Tokens anhängen → wiederholen
```

#### 1. Warum Dekodierung langsam ist

Ein autoregressives Modell erzeugt ein Token pro Forward Pass, für K Tokens braucht es also K serielle Durchläufe (Leviathan et al., 2022). Jeder Schritt muss alle Modellparameter aus dem High-Bandwidth Memory in den Beschleuniger laden, wodurch die Dekodierung durch den Speicher statt durch die Rechenleistung begrenzt ist (Cai et al., 2024). Chen et al. (2023) beobachteten, dass das parallele Bewerten einer kurzen Fortsetzung etwa so lange dauert wie das Ziehen eines einzigen Tokens aus dem großen Modell, sodass je Schritt Rechenleistung übrig bleibt. Speculative Decoding nutzt sie: Manche Tokens sind leicht und lassen sich von einem viel kleineren Modell erraten (Leviathan et al., 2022).

#### 2. Entwurf (Drafting)

Ein Draft-Modell `M_q` mit Verteilung `q` schlägt nach dem aktuellen Präfix einen Block von `γ` Tokens vor (Leviathan et al., 2022). In den ursprünglichen Verfahren ist das ein separates, kleineres und schnelleres Sprachmodell (Leviathan et al., 2022; Chen et al., 2023). Seine Qualität bestimmt die Beschleunigung: Je mehr seiner Tokens das Zielmodell annimmt, desto mehr Tokens liefert jeder teure Durchlauf, während ein langsamer Drafter den Gewinn aufzehrt. Die Latenz autoregressiver Drafter wächst linear mit der Blockgröße, was kurze Blöcke und flache Drafter erzwingt (Cheng et al., 2026).

#### 3. Parallele Prüfung

Das Zielmodell `M_p` mit Verteilung `p` läuft einmal auf dem Präfix, verlängert um alle Draft-Tokens, und liefert so `p` für alle Draft-Positionen gleichzeitig (Leviathan et al., 2022). Dieser eine Durchlauf ersetzt bis zu `γ + 1` sequenzielle Durchläufe des Zielmodells.

#### 4. Annahmeregel

Um `x ~ p(x)` zu ziehen, zieht das Verfahren stattdessen `x ~ q(x)`, behält es, wenn `q(x) ≤ p(x)`, und verwirft es andernfalls mit Wahrscheinlichkeit `1 − p(x)/q(x)` und zieht neu aus der angepassten Verteilung `p'(x) = norm(max(0, p(x) − q(x)))` (Leviathan et al., 2022). Für beliebige `p` und `q` folgen so gezogene Tokens genau `p` (Leviathan et al., 2022); Chen et al. (2023) beschreiben dasselbe abgewandelte Rejection Sampling und halten fest, dass es die Zielverteilung bis auf die Rechengenauigkeit der Hardware erhält. Die Tokens werden von links nach rechts geprüft; die erste Ablehnung beendet die Runde, und werden alle Draft-Tokens angenommen, fügt das Zielmodell aus seinem Durchlauf ein weiteres Token hinzu (Cheng et al., 2026). Die Ausgabe ist daher in ihrer Verteilung identisch mit normaler Dekodierung, weshalb das Verfahren weder erneutes Training noch Änderungen am Zielmodell braucht (Leviathan et al., 2022).

#### 5. In das Zielmodell eingebaute Drafter

Ein separates Draft-Modell zu pflegen ist umständlich, daher ergänzt Medusa das Zielmodell um zusätzliche Decoding-Köpfe, die mehrere folgende Tokens parallel vorhersagen, bildet mehrere Kandidatenfortsetzungen und prüft sie gemeinsam mit baumbasierter Attention (Cai et al., 2024). Medusa-1 trainiert nur die Köpfe auf einem eingefrorenen Modell und erreicht über 2,2-fache Beschleunigung ohne Qualitätsverlust; Medusa-2 trainiert Köpfe und Modell gemeinsam für das 2,3- bis 3,6-Fache, braucht dafür aber ein besonderes Trainingsverfahren (Cai et al., 2024). EAGLE entwirft auf der Ebene der Features der vorletzten Schicht statt auf Token-Ebene und nimmt die um einen Schritt vorgerückte Tokenfolge hinzu, um die Unsicherheit der Features aufzulösen; für LLaMA2-Chat 70B berichtete es eine 2,7- bis 3,5-mal geringere Latenz und doppelten Durchsatz bei unveränderter Ausgabeverteilung (Li et al., 2024).

#### 6. DSpark: halb-autoregressiver Entwurf und geplante Prüfung

Parallele Drafter erzeugen einen ganzen Block in einem Forward Pass, ihre Latenz hängt also kaum von der Blockgröße ab, doch weil jede Position unabhängig vorhergesagt wird, sinkt die Annahme zum Blockende hin schnell; lange Blöcke zu prüfen verschwendet zudem Batch-Kapazität auf Tokens, die wahrscheinlich verworfen werden, was den Durchsatz in ausgelasteten Serving-Systemen senkt (Cheng et al., 2026). DSpark von DeepSeek-AI und der Peking University hält das teure Draft-Backbone parallel und hängt einen leichten sequenziellen Kopf an, der Abhängigkeiten innerhalb des Blocks modelliert (halb-autoregressive Generierung), und ergänzt eine konfidenzgesteuerte Prüfung: Ein Confidence Head schätzt, mit welcher Wahrscheinlichkeit jedes Präfix besteht, und ein hardwarebewusster Scheduler entscheidet anhand von Durchsatzprofilen der Engine je Anfrage, wie viele Draft-Tokens sich zu prüfen lohnen (Cheng et al., 2026). Bei den Zielmodellen Qwen3 4B, 8B und 14B erhöhte es die mittlere akzeptierte Länge um 26,7 bis 30,9 Prozent gegenüber dem autoregressiven Drafter Eagle3 und um 16,3 bis 18,4 Prozent gegenüber dem parallelen Drafter DFlash; im Serving-System von DeepSeek-V4 steigerte es unter echtem Nutzerverkehr die Generierungsgeschwindigkeit je Nutzer um 60 bis 85 Prozent (V4-Flash) und 57 bis 78 Prozent (V4-Pro) gegenüber der bisherigen Produktionsbasis MTP-1 bei gleichem Durchsatz (Cheng et al., 2026). Die Checkpoints und die Trainings-Codebasis DeepSpec, die auch Eagle3 und DFlash enthält, sind Open Source (Cheng et al., 2026; DeepSpec-Repository).

#### Herkunft und Varianten

Leviathan et al. (2022) und Chen et al. (2023) führten Speculative Decoding und Speculative Sampling mit exaktem Rejection Sampling unabhängig voneinander ein, aufbauend auf früherer blockweise paralleler Dekodierung (Cheng et al., 2026). Varianten unterscheiden sich vor allem im Drafter: separate kleine Modelle, zusätzliche Köpfe (Medusa), Feature-Extrapolation (EAGLE, Eagle3), parallele Drafter (DFlash) und halb-autoregressive Drafter mit lastabhängiger Prüfung (DSpark).

### Wann einsetzen

- Wenn die Latenz je Nutzer zählt, etwa bei Chat und [[voice-agents|Voice Agents]], und das Modell auf Hardware mit freier Rechenleistung je Dekodierschritt läuft (Chen et al., 2023).
- Wenn die Ausgabe genau so bleiben muss wie ohne Beschleunigung, was verlustbehaftete Beschleunigungen ausschließt (Leviathan et al., 2022).
- Wenn für das Zielmodell ein passender Drafter existiert oder trainiert werden kann, etwa veröffentlichte DSpark- oder EAGLE-Checkpoints (Cheng et al., 2026; Li et al., 2024).

### Stärken und Grenzen

**Stärken**
- Verlustfrei: Die Ausgabeverteilung des Zielmodells bleibt erhalten (Leviathan et al., 2022; Chen et al., 2023).
- Funktioniert mit einem separaten Drafter für bestehende Modelle ohne erneutes Training oder Architekturänderung (Leviathan et al., 2022).
- Typische Beschleunigungen um das 2- bis 3,6-Fache, im Produktivbetrieb je Nutzer auch mehr (Cai et al., 2024; Li et al., 2024; Cheng et al., 2026).

**Grenzen**
- Der Gewinn hängt davon ab, wie oft Draft-Tokens angenommen werden; schwieriger Text mit wenigen vorhersehbaren Tokens bringt wenig.
- Das Prüfen verworfener Tokens kostet Rechenleistung und kann unter hoher Last den Durchsatz senken, wenn die Prüflänge nicht angepasst wird (Cheng et al., 2026).
- Eingebaute Drafter müssen je Zielmodell trainiert werden, und gemeinsames Training wie bei Medusa-2 braucht ein Verfahren, das die Fähigkeiten des Modells erhält (Cai et al., 2024).

### Vergleich

| Verfahren | Wodurch schneller | Ausgabe unverändert? | Beispiel |
|---|---|---|---|
| Speculative Decoding | parallel entwerfen und prüfen | ja | Leviathan et al. (2022), DSpark |
| [[quantisation\|Quantisierung]] | Gewichte mit geringerer Genauigkeit | nein, angenähert | INT8, 4 Bit |
| [[knowledge-distillation\|Knowledge Distillation]] | kleineres Schülermodell | nein, anderes Modell | [[distilbert\|DistilBERT]] |
| [[model-compression\|Modellkompression]] | Pruning und andere Verkleinerungen | nein | Pruning |
| [[llm-cost-optimisation\|Caching und Routing]] | Aufrufe vermeiden oder verkürzen | je nach Verfahren | Prompt Caching |

Quellen: Leviathan et al. (2022); Chen et al. (2023); Cheng et al. (2026).

### In der Praxis

DeepSpec veröffentlicht DSpark-, DFlash- und Eagle3-Drafter für Qwen3-4B, Qwen3-8B, Qwen3-14B und gemma-4-12B-it und bittet, beim Zitieren der Ergebnisse die Trainingseinstellungen des Repositorys zu übernehmen (DeepSpec-Repository). Maßgeblich sind die akzeptierte Länge je Runde, die Tokens pro Sekunde je Nutzer und der Gesamtdurchsatz, gemeinsam gemessen, weil eine Einstellung, die eine Nutzerin oder einen Nutzer beschleunigt, das System unter Last verlangsamen kann (Cheng et al., 2026). Betrieb und Serving behandelt [[mlops-and-deployment|MLOps und Deployment]], Kosten die [[llm-cost-optimisation|LLM-Kostenoptimierung]].

### Merksatz

Speculative Decoding lässt einen günstigen Drafter mehrere Tokens raten, die das große Modell in einem Durchlauf prüft; das beschleunigt die Generierung, ohne zu verändern, was das Modell erzeugt hätte.

### Quellen

- Leviathan, Y., Kalman, M. & Matias, Y. (2022). *Fast Inference from Transformers via Speculative Decoding.* arXiv:2211.17192. [arXiv](https://arxiv.org/abs/2211.17192)
- Chen, C., Borgeaud, S., Irving, G., Lespiau, J.-B., Sifre, L. & Jumper, J. (2023). *Accelerating Large Language Model Decoding with Speculative Sampling.* arXiv:2302.01318. [arXiv](https://arxiv.org/abs/2302.01318)
- Cai, T., Li, Y., Geng, Z., Peng, H., Lee, J. D., Chen, D. & Dao, T. (2024). *Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads.* arXiv:2401.10774. [arXiv](https://arxiv.org/abs/2401.10774)
- Li, Y., Wei, F., Zhang, C. & Zhang, H. (2024). *EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty.* arXiv:2401.15077. [arXiv](https://arxiv.org/abs/2401.15077)
- Cheng, X., Yu, X., Shao, C., Li, J., Xiong, Y. et al. (2026). *DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation.* arXiv:2607.05147. [arXiv](https://arxiv.org/abs/2607.05147)
- DeepSeek-AI (2026). *DeepSpec: a full-stack codebase for training and evaluating speculative decoding algorithms.* GitHub repository. [github.com](https://github.com/deepseek-ai/DeepSpec)
