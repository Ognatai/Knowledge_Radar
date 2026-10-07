---
title_en: Explainable AI (XAI)
title_de: Erklärbare KI (XAI)
entity_type: Concept
sources:
- https://arxiv.org/abs/1702.08608
- https://arxiv.org/abs/1811.10154
- https://arxiv.org/abs/1602.04938
- https://arxiv.org/abs/1705.07874
- https://arxiv.org/abs/1703.01365
- https://arxiv.org/abs/1711.00399
- https://arxiv.org/abs/1810.03292
- https://arxiv.org/abs/1902.10186
- https://arxiv.org/abs/2305.04388
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Explainable AI (XAI) aims to make a model's predictions understandable to people, so that they can assess trust, debug the model or act on a decision (Ribeiro et al., 2016; Doshi-Velez & Kim, 2017). It uses either inherently interpretable models (Rudin, 2018) or post-hoc explanation methods for black-box models, such as local surrogate models (Ribeiro et al., 2016), Shapley-value attributions (Lundberg & Lee, 2017), gradient-based attributions (Sundararajan et al., 2017) and counterfactual explanations (Wachter et al., 2017). Explanations themselves can be misleading and need to be tested (Adebayo et al., 2018; Turpin et al., 2023).

### How it works

Either the model is built to be interpretable from the start, or a separate method explains an existing model's prediction, for example by assigning each input feature an importance value or by describing the smallest change that would alter the decision. The explanation is then checked for whether it actually reflects the model.

```text
1. Why explanations are needed
▼
2. Inherently interpretable models
▼
3. Local surrogate models (LIME)
▼
4. Feature attributions (SHAP, Integrated Gradients)
▼
5. Counterfactual explanations
▼
6. Evaluating explanations
```

#### 1. Why explanations are needed

Understanding the reasons behind predictions is important for assessing trust, for deciding whether to deploy a model, and for improving an untrustworthy model (Ribeiro et al., 2016). Explanations are often used to assess other criteria indirectly, such as safety or non-discrimination, yet there is little consensus on what interpretability is and how it should be measured; Doshi-Velez & Kim (2017) define interpretability, describe when it is needed and when it is not, and propose a taxonomy for its rigorous evaluation.

#### 2. Inherently interpretable models

Rudin (2018) argues that explaining black-box models in high-stakes decisions, for example in healthcare or criminal justice, is likely to perpetuate bad practice and can cause serious harm. Instead, models should be inherently interpretable, and in many applications interpretable models could replace black boxes. Decision trees and linear models are typical interpretable models ([[decision-trees|Decision Trees]]).

#### 3. Local surrogate models (LIME)

LIME (Ribeiro et al., 2016) explains the prediction of any classifier by learning an interpretable model locally around that prediction. To give an overview of a model, it selects representative individual predictions and their explanations in a non-redundant way. The authors applied it to text and image classifiers, such as random forests and neural networks.

#### 4. Feature attributions (SHAP, Integrated Gradients)

SHAP (Lundberg & Lee, 2017) assigns each feature an importance value for a particular prediction. It identifies a class of additive feature importance measures, shows that there is a unique solution in this class with a set of desirable properties, and unifies six existing methods. For deep networks, Sundararajan et al. (2017) formulate two axioms that attribution methods should satisfy, sensitivity and implementation invariance, show that most known methods violate them, and propose Integrated Gradients, which needs only a few calls to the standard gradient operator and no change to the network.

#### 5. Counterfactual explanations

A counterfactual explanation describes how the input would have to change for the decision to be different, without opening the black box (Wachter et al., 2017). Wachter et al. argue that such explanations help a data subject act, not merely understand, and relate them to the discussion of a right to explanation in the GDPR.

#### 6. Evaluating explanations

Explanations can look convincing without reflecting the model. Adebayo et al. (2018) proposed sanity checks and found that some saliency methods are independent of both the model and the data-generating process, so visual assessment alone can mislead. In NLP, attention weights are frequently uncorrelated with gradient-based importance, and very different attention distributions can yield the same prediction, so attention should not be treated as an explanation (Jain & Wallace, 2019). For language models, chain-of-thought explanations can systematically misrepresent the true reason for a prediction: when models were biased towards an answer, for example by reordering answer options, they rationalised it without mentioning the bias, and accuracy dropped by up to 36% on 13 BIG-Bench Hard tasks (Turpin et al., 2023).

#### Origin and variants

LIME (Ribeiro et al., 2016), SHAP (Lundberg & Lee, 2017) and Integrated Gradients (Sundararajan et al., 2017) are widely used post-hoc methods, counterfactual explanations were proposed by Wachter et al. (2017), and Doshi-Velez & Kim (2017) and Rudin (2018) shaped the debate about what interpretability should mean. Adebayo et al. (2018), Jain & Wallace (2019) and Turpin et al. (2023) showed the limits of popular explanation types.

### When to use it

- When decisions about people have high stakes, inherently interpretable models should be considered first (Rudin, 2018).
- When a black-box model is used and individual predictions must be justified, local explanations or feature attributions help (Ribeiro et al., 2016; Lundberg & Lee, 2017).
- When affected people need to know what they could change, counterfactual explanations fit (Wachter et al., 2017).

### Strengths and limitations

**Strengths**
- Explanations support trust decisions and debugging (Ribeiro et al., 2016).
- SHAP gives attributions with a unique solution under stated properties (Lundberg & Lee, 2017).
- Counterfactual explanations work without access to the model's internals (Wachter et al., 2017).

**Limitations**
- Some saliency methods do not depend on the model at all (Adebayo et al., 2018).
- Attention weights are not reliable explanations (Jain & Wallace, 2019).
- Chain-of-thought explanations of language models can be unfaithful (Turpin et al., 2023).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Inherently interpretable models | The model itself is understandable (Rudin, 2018) | High-stakes decisions |
| LIME | Local interpretable surrogate around one prediction (Ribeiro et al., 2016) | Any classifier, individual predictions |
| SHAP | Additive attributions with unique solution under desirable properties (Lundberg & Lee, 2017) | Feature importance for individual predictions |
| Integrated Gradients | Gradient-based attribution satisfying sensitivity and implementation invariance (Sundararajan et al., 2017) | Deep networks |
| Counterfactual explanations | Smallest change that alters the decision (Wachter et al., 2017) | Explanations for affected people |

### In practice

The purpose of an explanation, debugging, trust or recourse, determines which method fits and how it is evaluated (Doshi-Velez & Kim, 2017). Explanation methods are checked with sanity tests before they are relied on (Adebayo et al., 2018), and explanations generated by language models are treated as claims to be verified rather than as insight into the model (Turpin et al., 2023). Explanations can also reveal discriminatory features ([[fairness-metrics|Fairness Metrics]]).

### Regulatory context

The [[gdpr|GDPR]] requires meaningful information about the logic involved in automated decision-making under Article 22, and the [[eu-ai-act|EU AI Act]] gives affected persons a right to an explanation of individual decisions based on the output of certain high-risk AI systems (Art. 86).

### Key takeaway

Explainable AI makes predictions understandable through interpretable models or post-hoc explanations, but explanations must themselves be checked for whether they reflect the model.

### Sources

- Doshi-Velez, F. & Kim, B. (2017). *Towards A Rigorous Science of Interpretable Machine Learning.* [arXiv:1702.08608](https://arxiv.org/abs/1702.08608)
- Rudin, C. (2018). *Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead.* Nature Machine Intelligence 2019. [arXiv:1811.10154](https://arxiv.org/abs/1811.10154)
- Ribeiro, M. T. et al. (2016). *"Why Should I Trust You?": Explaining the Predictions of Any Classifier.* KDD 2016. [arXiv:1602.04938](https://arxiv.org/abs/1602.04938)
- Lundberg, S. & Lee, S. (2017). *A Unified Approach to Interpreting Model Predictions.* NeurIPS 2017. [arXiv:1705.07874](https://arxiv.org/abs/1705.07874)
- Sundararajan, M. et al. (2017). *Axiomatic Attribution for Deep Networks.* ICML 2017. [arXiv:1703.01365](https://arxiv.org/abs/1703.01365)
- Wachter, S. et al. (2017). *Counterfactual Explanations without Opening the Black Box: Automated Decisions and the GDPR.* Harvard Journal of Law & Technology 2018. [arXiv:1711.00399](https://arxiv.org/abs/1711.00399)
- Adebayo, J. et al. (2018). *Sanity Checks for Saliency Maps.* NeurIPS 2018. [arXiv:1810.03292](https://arxiv.org/abs/1810.03292)
- Jain, S. & Wallace, B. C. (2019). *Attention is not Explanation.* NAACL 2019. [arXiv:1902.10186](https://arxiv.org/abs/1902.10186)
- Turpin, M. et al. (2023). *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting.* NeurIPS 2023. [arXiv:2305.04388](https://arxiv.org/abs/2305.04388)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Erklärbare KI (Explainable AI, XAI) soll die Vorhersagen eines Modells für Menschen nachvollziehbar machen, damit sie Vertrauen einschätzen, das Modell debuggen oder auf eine Entscheidung reagieren können (Ribeiro et al., 2016; Doshi-Velez & Kim, 2017). Sie nutzt entweder von sich aus interpretierbare Modelle (Rudin, 2018) oder nachträgliche (post-hoc) Erklärungsverfahren für Black-Box-Modelle, etwa lokale Surrogatmodelle (Ribeiro et al., 2016), Attributionen auf Basis von Shapley-Werten (Lundberg & Lee, 2017), gradientenbasierte Attributionen (Sundararajan et al., 2017) und kontrafaktische Erklärungen (Wachter et al., 2017). Erklärungen können selbst irreführen und müssen geprüft werden (Adebayo et al., 2018; Turpin et al., 2023).

### Funktionsweise

Entweder wird das Modell von Anfang an interpretierbar gebaut, oder ein separates Verfahren erklärt die Vorhersage eines bestehenden Modells, etwa indem es jedem Eingabemerkmal einen Wichtigkeitswert zuweist oder die kleinste Änderung beschreibt, die die Entscheidung ändern würde. Anschließend wird geprüft, ob die Erklärung das Modell tatsächlich widerspiegelt.

```text
1. Warum Erklärungen gebraucht werden
▼
2. Von sich aus interpretierbare Modelle
▼
3. Lokale Surrogatmodelle (LIME)
▼
4. Merkmalsattributionen (SHAP, Integrated Gradients)
▼
5. Kontrafaktische Erklärungen
▼
6. Erklärungen bewerten
```

#### 1. Warum Erklärungen gebraucht werden

Die Gründe hinter Vorhersagen zu verstehen ist wichtig, um Vertrauen einzuschätzen, über den Einsatz eines Modells zu entscheiden und ein unzuverlässiges Modell zu verbessern (Ribeiro et al., 2016). Erklärungen dienen oft dazu, andere Kriterien wie Sicherheit oder Diskriminierungsfreiheit indirekt zu beurteilen; doch es gibt wenig Einigkeit darüber, was Interpretierbarkeit ist und wie sie gemessen werden soll. Doshi-Velez & Kim (2017) definieren Interpretierbarkeit, beschreiben, wann sie gebraucht wird und wann nicht, und schlagen eine Taxonomie für ihre strenge Evaluation vor.

#### 2. Von sich aus interpretierbare Modelle

Rudin (2018) argumentiert, dass das Erklären von Black-Box-Modellen bei folgenreichen Entscheidungen, etwa im Gesundheitswesen oder in der Strafjustiz, schlechte Praxis fortschreiben und erheblichen Schaden anrichten kann. Stattdessen sollten Modelle von sich aus interpretierbar sein, und in vielen Anwendungen könnten interpretierbare Modelle Black Boxes ersetzen. Entscheidungsbäume und lineare Modelle sind typische interpretierbare Modelle ([[decision-trees|Entscheidungsbäume]]).

#### 3. Lokale Surrogatmodelle (LIME)

LIME (Ribeiro et al., 2016) erklärt die Vorhersage eines beliebigen Klassifikators, indem es lokal um diese Vorhersage ein interpretierbares Modell lernt. Für einen Überblick über ein Modell wählt es repräsentative Einzelvorhersagen samt Erklärungen ohne Redundanz aus. Die Autoren wandten es auf Text- und Bildklassifikatoren an, etwa Random Forests und neuronale Netze.

#### 4. Merkmalsattributionen (SHAP, Integrated Gradients)

SHAP (Lundberg & Lee, 2017) weist jedem Merkmal einen Wichtigkeitswert für eine bestimmte Vorhersage zu. Es bestimmt eine Klasse additiver Wichtigkeitsmaße, zeigt, dass es in dieser Klasse eine eindeutige Lösung mit einer Reihe wünschenswerter Eigenschaften gibt, und vereinheitlicht sechs bestehende Verfahren. Für tiefe Netze formulieren Sundararajan et al. (2017) zwei Axiome, die Attributionsverfahren erfüllen sollten, Sensitivität und Implementierungsinvarianz, zeigen, dass die meisten bekannten Verfahren sie verletzen, und schlagen Integrated Gradients vor, das nur einige Aufrufe des üblichen Gradientenoperators und keine Änderung am Netz braucht.

#### 5. Kontrafaktische Erklärungen

Eine kontrafaktische Erklärung beschreibt, wie sich die Eingabe ändern müsste, damit die Entscheidung anders ausfällt, ohne die Black Box zu öffnen (Wachter et al., 2017). Wachter et al. argumentieren, dass solche Erklärungen betroffenen Personen helfen, zu handeln und nicht nur zu verstehen, und setzen sie in Beziehung zur Debatte über ein Recht auf Erklärung in der DSGVO.

#### 6. Erklärungen bewerten

Erklärungen können überzeugend aussehen, ohne das Modell widerzuspiegeln. Adebayo et al. (2018) schlugen Plausibilitätsprüfungen (Sanity Checks) vor und fanden, dass einige Saliency-Verfahren weder vom Modell noch vom datenerzeugenden Prozess abhängen; eine rein visuelle Beurteilung kann also täuschen. Im NLP korrelieren Attention-Gewichte häufig nicht mit gradientenbasierter Wichtigkeit, und sehr unterschiedliche Attention-Verteilungen können zur selben Vorhersage führen; Attention sollte daher nicht als Erklärung behandelt werden (Jain & Wallace, 2019). Bei Sprachmodellen können Chain-of-Thought-Erklärungen den wahren Grund einer Vorhersage systematisch falsch darstellen: Wurden Modelle zu einer Antwort hin beeinflusst, etwa durch Umsortieren der Antwortoptionen, rechtfertigten sie diese, ohne die Beeinflussung zu erwähnen, und die Genauigkeit sank auf 13 Aufgaben aus BIG-Bench Hard um bis zu 36 % (Turpin et al., 2023).

#### Ursprung und Varianten

LIME (Ribeiro et al., 2016), SHAP (Lundberg & Lee, 2017) und Integrated Gradients (Sundararajan et al., 2017) sind verbreitete Post-hoc-Verfahren, kontrafaktische Erklärungen schlugen Wachter et al. (2017) vor, und Doshi-Velez & Kim (2017) sowie Rudin (2018) prägten die Debatte darüber, was Interpretierbarkeit bedeuten soll. Adebayo et al. (2018), Jain & Wallace (2019) und Turpin et al. (2023) zeigten die Grenzen verbreiteter Erklärungsarten.

### Wann einsetzen

- Bei folgenreichen Entscheidungen über Menschen sollten zuerst von sich aus interpretierbare Modelle erwogen werden (Rudin, 2018).
- Wenn ein Black-Box-Modell eingesetzt wird und Einzelvorhersagen begründet werden müssen, helfen lokale Erklärungen oder Merkmalsattributionen (Ribeiro et al., 2016; Lundberg & Lee, 2017).
- Wenn Betroffene wissen müssen, was sie ändern könnten, passen kontrafaktische Erklärungen (Wachter et al., 2017).

### Stärken und Grenzen

**Stärken**
- Erklärungen unterstützen Vertrauensentscheidungen und Debugging (Ribeiro et al., 2016).
- SHAP liefert Attributionen mit eindeutiger Lösung unter den genannten Eigenschaften (Lundberg & Lee, 2017).
- Kontrafaktische Erklärungen funktionieren ohne Zugriff auf das Innere des Modells (Wachter et al., 2017).

**Einschränkungen**
- Einige Saliency-Verfahren hängen überhaupt nicht vom Modell ab (Adebayo et al., 2018).
- Attention-Gewichte sind keine verlässlichen Erklärungen (Jain & Wallace, 2019).
- Chain-of-Thought-Erklärungen von Sprachmodellen können unzutreffend sein (Turpin et al., 2023).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Von sich aus interpretierbare Modelle | Das Modell selbst ist verständlich (Rudin, 2018) | Folgenreiche Entscheidungen |
| LIME | Lokales interpretierbares Surrogat um eine Vorhersage (Ribeiro et al., 2016) | Beliebige Klassifikatoren, Einzelvorhersagen |
| SHAP | Additive Attributionen mit eindeutiger Lösung unter wünschenswerten Eigenschaften (Lundberg & Lee, 2017) | Merkmalswichtigkeit für Einzelvorhersagen |
| Integrated Gradients | Gradientenbasierte Attribution, die Sensitivität und Implementierungsinvarianz erfüllt (Sundararajan et al., 2017) | Tiefe Netze |
| Kontrafaktische Erklärungen | Kleinste Änderung, die die Entscheidung ändert (Wachter et al., 2017) | Erklärungen für Betroffene |

### In der Praxis

Der Zweck einer Erklärung, also Debugging, Vertrauen oder Handlungsmöglichkeiten für Betroffene, bestimmt, welches Verfahren passt und wie es bewertet wird (Doshi-Velez & Kim, 2017). Erklärungsverfahren werden mit Plausibilitätsprüfungen getestet, bevor man sich auf sie verlässt (Adebayo et al., 2018), und von Sprachmodellen erzeugte Erklärungen werden als zu prüfende Behauptungen behandelt, nicht als Einblick in das Modell (Turpin et al., 2023). Erklärungen können auch diskriminierende Merkmale aufdecken ([[fairness-metrics|Fairness-Metriken]]).

### Regulatorischer Kontext

Die [[gdpr|Datenschutz-Grundverordnung (DSGVO)]] verlangt bei automatisierter Entscheidungsfindung nach Artikel 22 aussagekräftige Informationen über die involvierte Logik, und die [[eu-ai-act|KI-Verordnung]] gibt Betroffenen ein Recht auf Erläuterung der Entscheidungsfindung im Einzelfall bei Entscheidungen, die auf der Ausgabe bestimmter Hochrisiko-KI-Systeme beruhen (Art. 86).

### Merksatz

Erklärbare KI macht Vorhersagen durch interpretierbare Modelle oder nachträgliche Erklärungen nachvollziehbar, doch Erklärungen müssen selbst daraufhin geprüft werden, ob sie das Modell widerspiegeln.

### Quellen

- Doshi-Velez, F. & Kim, B. (2017). *Towards A Rigorous Science of Interpretable Machine Learning.* [arXiv:1702.08608](https://arxiv.org/abs/1702.08608)
- Rudin, C. (2018). *Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead.* Nature Machine Intelligence 2019. [arXiv:1811.10154](https://arxiv.org/abs/1811.10154)
- Ribeiro, M. T. et al. (2016). *"Why Should I Trust You?": Explaining the Predictions of Any Classifier.* KDD 2016. [arXiv:1602.04938](https://arxiv.org/abs/1602.04938)
- Lundberg, S. & Lee, S. (2017). *A Unified Approach to Interpreting Model Predictions.* NeurIPS 2017. [arXiv:1705.07874](https://arxiv.org/abs/1705.07874)
- Sundararajan, M. et al. (2017). *Axiomatic Attribution for Deep Networks.* ICML 2017. [arXiv:1703.01365](https://arxiv.org/abs/1703.01365)
- Wachter, S. et al. (2017). *Counterfactual Explanations without Opening the Black Box: Automated Decisions and the GDPR.* Harvard Journal of Law & Technology 2018. [arXiv:1711.00399](https://arxiv.org/abs/1711.00399)
- Adebayo, J. et al. (2018). *Sanity Checks for Saliency Maps.* NeurIPS 2018. [arXiv:1810.03292](https://arxiv.org/abs/1810.03292)
- Jain, S. & Wallace, B. C. (2019). *Attention is not Explanation.* NAACL 2019. [arXiv:1902.10186](https://arxiv.org/abs/1902.10186)
- Turpin, M. et al. (2023). *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting.* NeurIPS 2023. [arXiv:2305.04388](https://arxiv.org/abs/2305.04388)
