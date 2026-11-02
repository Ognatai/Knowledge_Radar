---
title_en: Cross-Entropy
title_de: Cross-Entropy
entity_type: Concept
aliases:
- Cross-entropy
- Cross entropy
- Cross-entropy loss
- Log loss
- Negative log-likelihood
- Negative log likelihood loss
- Kreuzentropie
sources:
- https://web.stanford.edu/~jurafsky/slp3/4.pdf
- https://web.stanford.edu/~jurafsky/slp3/7.pdf
- https://www.deeplearningbook.org/contents/prob.html
- https://www.deeplearningbook.org/contents/mlp.html
- https://arxiv.org/abs/1512.00567
- https://arxiv.org/abs/1906.02629
- https://arxiv.org/abs/1708.02002
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Cross-entropy measures how well a predicted probability distribution Q matches a true distribution P: `H(P, Q) = −E_{x∼P} log Q(x)` (Goodfellow et al., 2016). As a loss function it is the negative log probability that a model assigns to the correct label, which makes minimising it the same as maximum likelihood estimation; it is the standard loss for [[logistic-regression|logistic regression]], neural classifiers and language models (Jurafsky & Martin, 2026; Goodfellow et al., 2016). For language models, the exponential of the mean cross-entropy is the perplexity (Jurafsky & Martin, 2026).

### How it works

```text
true distribution y (often one-hot: 1 for the correct class)
predicted distribution ŷ = softmax(z)
   ▼
L_CE(ŷ, y) = − Σ_k y_k log ŷ_k   =  − log ŷ_correct      (one-hot case)
   ▼
gradient w.r.t. logits:  ∂L/∂z_k = ŷ_k − y_k             (bounded between −1 and 1)
   ▼
average over the batch ──► gradient descent ──► (language models) perplexity = exp(mean loss)
```

#### 1. From information theory

The Shannon entropy `H(P) = −E log P(x)` is the expected information of an event drawn from P; the Kullback–Leibler divergence `D_KL(P‖Q) = E_P[log P(x) − log Q(x)]` measures how different Q is from P, is non-negative and is 0 only if the distributions are equal (Goodfellow et al., 2016). Cross-entropy is `H(P, Q) = H(P) + D_KL(P‖Q)`; because H(P) does not depend on Q, minimising cross-entropy with respect to Q is equivalent to minimising the KL divergence (Goodfellow et al., 2016). With the natural logarithm the unit is nats, with base 2 it is bits (Goodfellow et al., 2016).

#### 2. Binary cross-entropy

For a binary classifier with output `ŷ = σ(w · x + b)`, the probability of the correct label is `ŷ^y (1 − ŷ)^(1−y)`; taking the log and flipping the sign gives `L_CE = −[y log ŷ + (1 − y) log(1 − ŷ)]` (Jurafsky & Martin, 2026). In Jurafsky and Martin's sentiment example, a model that gives the correct positive label probability 0.70 has a loss of `−log 0.70 = 0.36`, and if the true label were negative the loss would be `−log 0.30 = 1.2`; the loss ranges from 0 for a perfect prediction to infinity for probability 0 on the correct label (Jurafsky & Martin, 2026).

#### 3. Multi-class cross-entropy

With K classes and a one-hot target y, the loss `−Σ_k y_k log ŷ_k` reduces to the negative log probability of the correct class, which is why it is also called negative log-likelihood loss (Jurafsky & Martin, 2026). Combined with a [[softmax|softmax]] output, the log undoes the exponential, the loss does not saturate when the model is confidently wrong, and the gradient with respect to the logits is simply `p(k) − q(k)`, bounded between −1 and 1 (Goodfellow et al., 2016; Szegedy et al., 2016).

#### 4. Language modelling and perplexity

A language model is trained to minimise the cross-entropy of the next token: at each position the loss is `−log ŷ_t[w_{t+1}]`, the negative log probability of the actual next token, with the correct history given as input (teacher forcing), averaged over the sequence and batch (Jurafsky & Martin, 2026; [[large-language-models|large language models]]). Perplexity, the inverse probability of a test set normalised by its length, equals the exponential of the mean cross-entropy; lower is better, but because it depends on the number of tokens it is only comparable between models with the same tokeniser (Jurafsky & Martin, 2026; [[tokenisation|tokenisation]]).

#### 5. Why not squared error

Maximum likelihood with a Gaussian output recovers mean squared error, so cross-entropy is the general principle and MSE a special case (Goodfellow et al., 2016). For classification, mean squared and mean absolute error often give poor results with gradient-based training, because saturating output units then produce very small gradients; this is one reason cross-entropy is more popular even when no full distribution is needed (Goodfellow et al., 2016).

#### Origin and variants

- **Label smoothing** replaces the one-hot target with `(1 − ε) δ_{k,y} + ε/K`; Szegedy et al. (2016) introduced it because a one-hot target pushes the correct logit far above all others, which can overfit and makes the model too confident, and with ε = 0.1 they found about 0.2 percentage points lower top-1 and top-5 error on ImageNet. Müller et al. (2019) showed that it also improves calibration, but makes knowledge distillation from such a teacher less effective ([[knowledge-distillation|knowledge distillation]]).
- **Focal loss** multiplies cross-entropy by `(1 − p_t)^γ` to down-weight easy examples under extreme class imbalance; with γ = 2, an example classified with probability 0.9 gets 100 times less loss than with plain cross-entropy (Lin et al., 2017).

### When to use it

- Training any probabilistic classifier, from logistic regression to deep networks ([[classification|classification]], [[neural-network-training|neural network training]]).
- Pre-training and fine-tuning language models on next-token prediction (Jurafsky & Martin, 2026).
- Evaluating language models by perplexity on held-out text with the same tokeniser (Jurafsky & Martin, 2026).
- Matching a student's predictions to a teacher's soft targets ([[knowledge-distillation|knowledge distillation]]).

### Strengths and limitations

**Strengths**
- Follows directly from maximum likelihood, so every probabilistic model brings its own loss (Goodfellow et al., 2016).
- Strong, non-saturating gradients with softmax and sigmoid outputs (Goodfellow et al., 2016).
- Convex for logistic regression (Jurafsky & Martin, 2026).

**Limitations**
- Usually has no minimum for models that cannot output exactly 0 or 1, so it rewards ever more confident predictions unless regularised (Goodfellow et al., 2016).
- One-hot targets encourage over-confidence, which label smoothing counteracts (Szegedy et al., 2016; Müller et al., 2019).
- Treats all classes and examples alike; heavy class imbalance needs weighting or a focal loss (Lin et al., 2017).
- A low loss on training data says nothing about calibration or fairness on new data ([[temperature-scaling|temperature scaling]], [[fairness-metrics|fairness metrics]]).

### Comparison

| Loss | Formula (one example) | Typical use |
|---|---|---|
| Cross-entropy | `−log ŷ_correct` | classification, language models |
| Binary cross-entropy | `−[y log ŷ + (1−y) log(1−ŷ)]` | binary outputs ([[logistic-regression\|logistic regression]]) |
| Mean squared error | `(y − ŷ)²` | regression ([[linear-regression\|linear regression]]) |
| Label-smoothed cross-entropy | cross-entropy against `(1−ε)·one-hot + ε/K` | large classifiers, translation |
| Focal loss | `−(1 − p_t)^γ log p_t` | dense detection with class imbalance |

Sources: Jurafsky & Martin (2026), Goodfellow et al. (2016), Szegedy et al. (2016), Lin et al. (2017).

### In practice

Training curves report the mean cross-entropy per token or example; for language models it is often converted to perplexity, and comparisons across tokenisers need care (Jurafsky & Martin, 2026). Label smoothing has been used in image classification, translation and speech recognition models; because it erases information about similarities between classes in the logits, it should be switched off for a model that will serve as a distillation teacher (Müller et al., 2019).

### Key takeaway

Cross-entropy is the negative log probability of the correct answer; minimising it is maximum likelihood, it pairs naturally with softmax outputs, and its exponential is the perplexity of a language model.

### Sources

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 4: Logistic Regression and Text Classification. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/4.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 7: Transformers and Pretraining. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/7.pdf)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, chapter 3: Probability and Information Theory. MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/prob.html)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, chapter 6: Deep Feedforward Networks. MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/mlp.html)
- Szegedy, C., Vanhoucke, V., Ioffe, S., Shlens, J. & Wojna, Z. (2016). *Rethinking the Inception Architecture for Computer Vision.* CVPR 2016. [arXiv:1512.00567](https://arxiv.org/abs/1512.00567)
- Müller, R., Kornblith, S. & Hinton, G. (2019). *When Does Label Smoothing Help?* NeurIPS 2019. [arXiv:1906.02629](https://arxiv.org/abs/1906.02629)
- Lin, T.-Y., Goyal, P., Girshick, R., He, K. & Dollár, P. (2017). *Focal Loss for Dense Object Detection.* ICCV 2017. [arXiv:1708.02002](https://arxiv.org/abs/1708.02002)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die Cross-Entropy (Kreuzentropie) misst, wie gut eine vorhergesagte Wahrscheinlichkeitsverteilung Q zu einer wahren Verteilung P passt: `H(P, Q) = −E_{x∼P} log Q(x)` (Goodfellow et al., 2016). Als Verlustfunktion ist sie die negative logarithmierte Wahrscheinlichkeit, die ein Modell dem richtigen Label zuweist; ihre Minimierung ist daher dasselbe wie eine Maximum-Likelihood-Schätzung, und sie ist der Standardverlust für [[logistic-regression|logistische Regression]], neuronale Klassifikatoren und Sprachmodelle (Jurafsky & Martin, 2026; Goodfellow et al., 2016). Bei Sprachmodellen ist die Exponentialfunktion der mittleren Cross-Entropy die Perplexität (Jurafsky & Martin, 2026).

### Funktionsweise

```text
wahre Verteilung y (oft One-hot: 1 für die richtige Klasse)
vorhergesagte Verteilung ŷ = softmax(z)
   ▼
L_CE(ŷ, y) = − Σ_k y_k log ŷ_k   =  − log ŷ_richtig      (One-hot-Fall)
   ▼
Gradient nach den Logits:  ∂L/∂z_k = ŷ_k − y_k          (beschränkt zwischen −1 und 1)
   ▼
Mittel über den Batch ──► Gradientenabstieg ──► (Sprachmodelle) Perplexität = exp(mittlerer Verlust)
```

#### 1. Aus der Informationstheorie

Die Shannon-Entropie `H(P) = −E log P(x)` ist die erwartete Information eines aus P gezogenen Ereignisses; die Kullback-Leibler-Divergenz `D_KL(P‖Q) = E_P[log P(x) − log Q(x)]` misst, wie sehr Q von P abweicht, ist nichtnegativ und nur dann 0, wenn die Verteilungen gleich sind (Goodfellow et al., 2016). Die Cross-Entropy ist `H(P, Q) = H(P) + D_KL(P‖Q)`; weil H(P) nicht von Q abhängt, ist die Minimierung der Cross-Entropy nach Q gleichbedeutend mit der Minimierung der KL-Divergenz (Goodfellow et al., 2016). Mit dem natürlichen Logarithmus ist die Einheit Nats, mit Basis 2 Bits (Goodfellow et al., 2016).

#### 2. Binäre Cross-Entropy

Für einen binären Klassifikator mit Ausgabe `ŷ = σ(w · x + b)` ist die Wahrscheinlichkeit des richtigen Labels `ŷ^y (1 − ŷ)^(1−y)`; Logarithmieren und Umkehren des Vorzeichens ergibt `L_CE = −[y log ŷ + (1 − y) log(1 − ŷ)]` (Jurafsky & Martin, 2026). Im Sentiment-Beispiel von Jurafsky und Martin hat ein Modell, das dem richtigen positiven Label die Wahrscheinlichkeit 0,70 gibt, einen Verlust von `−log 0,70 = 0,36`; wäre das wahre Label negativ, betrüge der Verlust `−log 0,30 = 1,2`; der Verlust reicht von 0 bei perfekter Vorhersage bis unendlich bei Wahrscheinlichkeit 0 für das richtige Label (Jurafsky & Martin, 2026).

#### 3. Cross-Entropy für mehrere Klassen

Bei K Klassen und einem One-hot-Ziel y reduziert sich der Verlust `−Σ_k y_k log ŷ_k` auf die negative logarithmierte Wahrscheinlichkeit der richtigen Klasse, weshalb er auch Negative-Log-Likelihood-Verlust heißt (Jurafsky & Martin, 2026). Zusammen mit einer [[softmax|Softmax]]-Ausgabe hebt der Logarithmus die Exponentialfunktion auf, der Verlust sättigt nicht, wenn das Modell sich sicher irrt, und der Gradient nach den Logits ist einfach `p(k) − q(k)`, beschränkt zwischen −1 und 1 (Goodfellow et al., 2016; Szegedy et al., 2016).

#### 4. Sprachmodellierung und Perplexität

Ein Sprachmodell wird darauf trainiert, die Cross-Entropy des nächsten Tokens zu minimieren: An jeder Position ist der Verlust `−log ŷ_t[w_{t+1}]`, die negative logarithmierte Wahrscheinlichkeit des tatsächlichen nächsten Tokens, wobei die richtige Vorgeschichte als Eingabe dient (Teacher Forcing), gemittelt über Sequenz und Batch (Jurafsky & Martin, 2026; [[large-language-models|große Sprachmodelle]]). Die Perplexität, die inverse Wahrscheinlichkeit eines Testdatensatzes normiert auf seine Länge, ist gleich der Exponentialfunktion der mittleren Cross-Entropy; niedriger ist besser, aber weil sie von der Zahl der Tokens abhängt, ist sie nur zwischen Modellen mit demselben Tokenizer vergleichbar (Jurafsky & Martin, 2026; [[tokenisation|Tokenisierung]]).

#### 5. Warum nicht der quadratische Fehler

Maximum Likelihood mit einer Gauß-Ausgabe ergibt den mittleren quadratischen Fehler; die Cross-Entropy ist also das allgemeine Prinzip und der MSE ein Spezialfall (Goodfellow et al., 2016). Für die Klassifikation liefern mittlerer quadratischer und mittlerer absoluter Fehler bei gradientenbasiertem Training oft schlechte Ergebnisse, weil sättigende Ausgabeeinheiten dann sehr kleine Gradienten erzeugen; das ist ein Grund, warum die Cross-Entropy beliebter ist, auch wenn keine volle Verteilung gebraucht wird (Goodfellow et al., 2016).

#### Ursprung und Varianten

- **Label Smoothing** ersetzt das One-hot-Ziel durch `(1 − ε) δ_{k,y} + ε/K`; Szegedy et al. (2016) führten es ein, weil ein One-hot-Ziel den richtigen Logit weit über alle anderen treibt, was zu Overfitting führen kann und das Modell zu selbstsicher macht, und fanden mit ε = 0,1 etwa 0,2 Prozentpunkte niedrigere Top-1- und Top-5-Fehler auf ImageNet. Müller et al. (2019) zeigten, dass es auch die Kalibrierung verbessert, aber die Knowledge Distillation von einem so trainierten Lehrermodell weniger wirksam macht ([[knowledge-distillation|Knowledge Distillation]]).
- **Focal Loss** multipliziert die Cross-Entropy mit `(1 − p_t)^γ`, um bei extremem Klassenungleichgewicht einfache Beispiele herunterzugewichten; mit γ = 2 erhält ein Beispiel, das mit Wahrscheinlichkeit 0,9 richtig klassifiziert ist, 100-mal weniger Verlust als mit einfacher Cross-Entropy (Lin et al., 2017).

### Wann einsetzen

- Training jedes probabilistischen Klassifikators, von logistischer Regression bis zu tiefen Netzen ([[classification|Klassifikation]], [[neural-network-training|Training neuronaler Netze]]).
- Vortraining und Fine-Tuning von Sprachmodellen auf die Vorhersage des nächsten Tokens (Jurafsky & Martin, 2026).
- Bewertung von Sprachmodellen per Perplexität auf zurückgehaltenem Text mit demselben Tokenizer (Jurafsky & Martin, 2026).
- Angleichen der Vorhersagen eines Schülermodells an die weichen Zielwerte eines Lehrermodells ([[knowledge-distillation|Knowledge Distillation]]).

### Stärken und Grenzen

**Stärken**
- Folgt direkt aus Maximum Likelihood, sodass jedes probabilistische Modell seinen eigenen Verlust mitbringt (Goodfellow et al., 2016).
- Starke, nicht sättigende Gradienten mit Softmax- und Sigmoid-Ausgaben (Goodfellow et al., 2016).
- Konvex bei logistischer Regression (Jurafsky & Martin, 2026).

**Grenzen**
- Hat meist kein Minimum bei Modellen, die nicht genau 0 oder 1 ausgeben können, und belohnt daher immer selbstsicherere Vorhersagen, sofern nicht regularisiert wird (Goodfellow et al., 2016).
- One-hot-Ziele fördern übermäßige Selbstsicherheit, der Label Smoothing entgegenwirkt (Szegedy et al., 2016; Müller et al., 2019).
- Behandelt alle Klassen und Beispiele gleich; starkes Klassenungleichgewicht braucht Gewichtung oder einen Focal Loss (Lin et al., 2017).
- Ein niedriger Verlust auf Trainingsdaten sagt nichts über Kalibrierung oder Fairness auf neuen Daten ([[temperature-scaling|Temperature Scaling]], [[fairness-metrics|Fairness-Metriken]]).

### Vergleich

| Verlust | Formel (ein Beispiel) | Typischer Einsatz |
|---|---|---|
| Cross-Entropy | `−log ŷ_richtig` | Klassifikation, Sprachmodelle |
| Binäre Cross-Entropy | `−[y log ŷ + (1−y) log(1−ŷ)]` | binäre Ausgaben ([[logistic-regression\|logistische Regression]]) |
| Mittlerer quadratischer Fehler | `(y − ŷ)²` | Regression ([[linear-regression\|lineare Regression]]) |
| Cross-Entropy mit Label Smoothing | Cross-Entropy gegen `(1−ε)·One-hot + ε/K` | große Klassifikatoren, Übersetzung |
| Focal Loss | `−(1 − p_t)^γ log p_t` | dichte Objekterkennung mit Klassenungleichgewicht |

Quellen: Jurafsky & Martin (2026), Goodfellow et al. (2016), Szegedy et al. (2016), Lin et al. (2017).

### In der Praxis

Trainingskurven zeigen die mittlere Cross-Entropy pro Token oder Beispiel; bei Sprachmodellen wird sie oft in Perplexität umgerechnet, und Vergleiche über Tokenizer hinweg erfordern Vorsicht (Jurafsky & Martin, 2026). Label Smoothing wurde in Modellen für Bildklassifikation, Übersetzung und Spracherkennung eingesetzt; weil es in den Logits Information über Ähnlichkeiten zwischen Klassen löscht, wird es bei einem Modell, das später als Lehrer für Distillation dient, besser abgeschaltet (Müller et al., 2019).

### Merksatz

Die Cross-Entropy ist die negative logarithmierte Wahrscheinlichkeit der richtigen Antwort; ihre Minimierung ist Maximum Likelihood, sie passt natürlich zu Softmax-Ausgaben, und ihre Exponentialfunktion ist die Perplexität eines Sprachmodells.

### Quellen

- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 4: Logistic Regression and Text Classification. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/4.pdf)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 7: Transformers and Pretraining. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/7.pdf)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, Kapitel 3: Probability and Information Theory. MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/prob.html)
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, Kapitel 6: Deep Feedforward Networks. MIT Press. [deeplearningbook.org](https://www.deeplearningbook.org/contents/mlp.html)
- Szegedy, C., Vanhoucke, V., Ioffe, S., Shlens, J. & Wojna, Z. (2016). *Rethinking the Inception Architecture for Computer Vision.* CVPR 2016. [arXiv:1512.00567](https://arxiv.org/abs/1512.00567)
- Müller, R., Kornblith, S. & Hinton, G. (2019). *When Does Label Smoothing Help?* NeurIPS 2019. [arXiv:1906.02629](https://arxiv.org/abs/1906.02629)
- Lin, T.-Y., Goyal, P., Girshick, R., He, K. & Dollár, P. (2017). *Focal Loss for Dense Object Detection.* ICCV 2017. [arXiv:1708.02002](https://arxiv.org/abs/1708.02002)
