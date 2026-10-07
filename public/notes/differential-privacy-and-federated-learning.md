---
title_en: Differential Privacy and Federated Learning
title_de: Differential Privacy und Federated Learning
entity_type: Method
sources:
- https://doi.org/10.1007/11681878_14
- https://doi.org/10.1561/0400000042
- https://arxiv.org/abs/1607.00133
- https://arxiv.org/abs/1602.05629
- https://arxiv.org/abs/1912.04977
- https://arxiv.org/abs/1906.08935
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Differential privacy and federated learning are two techniques for privacy-preserving machine learning. Differential privacy guarantees that the output of an analysis changes only slightly when one person's data is added or removed, achieved by adding calibrated noise (Dwork et al., 2006; Dwork & Roth, 2014). Federated learning keeps training data on clients and shares only model updates (McMahan et al., 2016), but shared gradients can still reveal training data (Zhu et al., 2019), so the two are often combined.

### How it works

With differential privacy, noise is added to a computation, for example to gradients during training, so that the result reveals little about any individual. With federated learning, clients train locally and send model updates to a server, which aggregates them into a shared model.

```text
1. Definition of differential privacy
▼
2. Differentially private deep learning
▼
3. Federated learning
▼
4. Open problems in federated learning
▼
5. Leakage from shared gradients
```

#### 1. Definition of differential privacy

Dwork et al. (2006) introduced the definition now known as ε-differential privacy: a mechanism is private if its output distribution changes only slightly, bounded by ε, when a single individual's record is added or removed. Privacy is achieved by adding noise, for example Laplace noise, calibrated to the sensitivity of the function, i.e. how much one record can change its result. Dwork & Roth (2014) present differential privacy as a robust and mathematically rigorous definition of privacy, together with fundamental techniques for achieving it and limits on what can be achieved.

#### 2. Differentially private deep learning

Abadi et al. (2016) developed algorithmic techniques for learning and a refined analysis of privacy costs within the framework of differential privacy. They showed that deep neural networks with non-convex objectives can be trained under a modest privacy budget, at a manageable cost in software complexity, training efficiency and model quality.

#### 3. Federated learning

McMahan et al. (2016) proposed leaving the training data distributed on mobile devices and learning a shared model by aggregating locally computed updates, an approach they called federated learning. Their method is based on iterative model averaging. It was robust to the unbalanced and non-IID data distributions typical of this setting, and since communication is the main constraint, it reduced the required communication rounds by 10 to 100 times compared with synchronised stochastic gradient descent.

#### 4. Open problems in federated learning

In federated learning, many clients, such as mobile devices or whole organisations, collaboratively train a model under the orchestration of a central server while the training data stays decentralised (Kairouz et al., 2019). The approach embodies the principles of focused data collection and data minimisation and can mitigate many privacy risks and costs of centralised machine learning. Kairouz et al. survey recent advances and collect an extensive list of open problems.

#### 5. Leakage from shared gradients

Sharing gradients was long considered safe. Zhu et al. (2019) showed that private training data can be recovered from publicly shared gradients, pixel-wise accurate for images and token-wise matching for text. Of the defences they discussed, gradient pruning was the most effective. Federated learning alone therefore does not guarantee privacy.

#### Origin and variants

Differential privacy was defined by Dwork et al. (2006) and systematised by Dwork & Roth (2014); Abadi et al. (2016) applied it to deep learning. Federated learning was proposed by McMahan et al. (2016) and surveyed by Kairouz et al. (2019), and Zhu et al. (2019) showed its limits through gradient leakage.

### When to use it

- When statistics or models are released from data about individuals and individual records must not be identifiable, differential privacy provides a formal guarantee (Dwork & Roth, 2014).
- When training data cannot be centralised, for example because it resides on devices or at different organisations, federated learning applies (McMahan et al., 2016; Kairouz et al., 2019).
- When shared updates could reveal training data, federated learning should be combined with further protection such as differential privacy (Zhu et al., 2019; Abadi et al., 2016).

### Strengths and limitations

**Strengths**
- Differential privacy is a mathematically rigorous definition of privacy (Dwork & Roth, 2014).
- Deep networks can be trained with differential privacy under a modest privacy budget (Abadi et al., 2016).
- Federated learning keeps raw data on clients and supports data minimisation (Kairouz et al., 2019).

**Limitations**
- Differential privacy costs some model quality and training efficiency (Abadi et al., 2016).
- Shared gradients can leak training data (Zhu et al., 2019).
- Federated learning still has many open problems (Kairouz et al., 2019).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Differential privacy | Calibrated noise bounds the influence of any individual (Dwork et al., 2006) | Releasing statistics or models trained on personal data |
| DP training (DP-SGD style) | Privacy accounting during neural network training (Abadi et al., 2016) | Deep learning on sensitive data |
| Federated learning | Data stays on clients; only updates are aggregated (McMahan et al., 2016) | Decentralised data on devices or across organisations |
| Federated learning with DP | Combines decentralisation with a formal guarantee (Kairouz et al., 2019; Zhu et al., 2019) | Protecting against leakage from updates |

### In practice

The privacy budget ε must be chosen and reported, since it determines how strong the guarantee is (Dwork & Roth, 2014). In federated settings, updates should be protected, because gradients alone can reveal training examples (Zhu et al., 2019). Whether data protected this way still counts as personal data is a legal question answered by data protection law, not by the technique ([[gdpr|GDPR]]).

### Key takeaway

Differential privacy limits what a result reveals about any individual, federated learning keeps data where it is, and because shared updates can leak data, the two complement each other.

### Sources

- Dwork, C., McSherry, F., Nissim, K. & Smith, A. (2006). *Calibrating Noise to Sensitivity in Private Data Analysis.* TCC 2006. [doi:10.1007/11681878_14](https://doi.org/10.1007/11681878_14)
- Dwork, C. & Roth, A. (2014). *The Algorithmic Foundations of Differential Privacy.* Foundations and Trends in Theoretical Computer Science 9(3-4). [doi:10.1561/0400000042](https://doi.org/10.1561/0400000042)
- Abadi, M. et al. (2016). *Deep Learning with Differential Privacy.* CCS 2016. [arXiv:1607.00133](https://arxiv.org/abs/1607.00133)
- McMahan, H. B. et al. (2016). *Communication-Efficient Learning of Deep Networks from Decentralized Data.* AISTATS 2017. [arXiv:1602.05629](https://arxiv.org/abs/1602.05629)
- Kairouz, P. et al. (2019). *Advances and Open Problems in Federated Learning.* [arXiv:1912.04977](https://arxiv.org/abs/1912.04977)
- Zhu, L. et al. (2019). *Deep Leakage from Gradients.* NeurIPS 2019. [arXiv:1906.08935](https://arxiv.org/abs/1906.08935)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Differential Privacy und Federated Learning sind zwei Techniken für datenschutzfreundliches maschinelles Lernen. Differential Privacy garantiert, dass sich das Ergebnis einer Analyse nur geringfügig ändert, wenn die Daten einer Person hinzukommen oder wegfallen; erreicht wird das durch kalibriertes Rauschen (Dwork et al., 2006; Dwork & Roth, 2014). Federated Learning belässt die Trainingsdaten bei den Clients und teilt nur Modellaktualisierungen (McMahan et al., 2016), doch geteilte Gradienten können dennoch Trainingsdaten preisgeben (Zhu et al., 2019); deshalb werden beide oft kombiniert.

### Funktionsweise

Bei Differential Privacy wird einer Berechnung Rauschen hinzugefügt, etwa den Gradienten während des Trainings, sodass das Ergebnis wenig über einzelne Personen verrät. Beim Federated Learning trainieren Clients lokal und senden Modellaktualisierungen an einen Server, der sie zu einem gemeinsamen Modell zusammenführt.

```text
1. Definition von Differential Privacy
▼
2. Deep Learning mit Differential Privacy
▼
3. Federated Learning
▼
4. Offene Probleme des Federated Learning
▼
5. Leakage über geteilte Gradienten
```

#### 1. Definition von Differential Privacy

Dwork et al. (2006) führten die heute als ε-Differential-Privacy bekannte Definition ein: Ein Verfahren ist privat, wenn sich die Verteilung seiner Ausgaben nur geringfügig, begrenzt durch ε, ändert, wenn der Datensatz einer einzelnen Person hinzugefügt oder entfernt wird. Erreicht wird das durch Rauschen, etwa Laplace-Rauschen, das auf die Sensitivität der Funktion kalibriert ist, also darauf, wie stark ein einzelner Datensatz ihr Ergebnis verändern kann. Dwork & Roth (2014) stellen Differential Privacy als robuste, mathematisch strenge Definition von Privatsphäre dar, zusammen mit grundlegenden Techniken, sie zu erreichen, und den Grenzen des Erreichbaren.

#### 2. Deep Learning mit Differential Privacy

Abadi et al. (2016) entwickelten algorithmische Lernverfahren und eine verfeinerte Analyse der Privatsphärekosten im Rahmen von Differential Privacy. Sie zeigten, dass sich tiefe neuronale Netze mit nichtkonvexen Zielfunktionen bei moderatem Privacy-Budget trainieren lassen, zu vertretbaren Kosten bei Softwarekomplexität, Trainingseffizienz und Modellqualität.

#### 3. Federated Learning

McMahan et al. (2016) schlugen vor, die Trainingsdaten verteilt auf den Mobilgeräten zu belassen und ein gemeinsames Modell durch Zusammenführen lokal berechneter Aktualisierungen zu lernen; diesen Ansatz nannten sie Federated Learning. Ihr Verfahren beruht auf iterativer Mittelung der Modelle. Es war robust gegenüber den unausgewogenen und nicht unabhängig identisch verteilten (Non-IID) Daten, die für dieses Szenario typisch sind, und da die Kommunikation der Engpass ist, verringerte es die nötigen Kommunikationsrunden gegenüber synchronisiertem stochastischem Gradientenabstieg um das 10- bis 100-Fache.

#### 4. Offene Probleme des Federated Learning

Beim Federated Learning trainieren viele Clients, etwa Mobilgeräte oder ganze Organisationen, gemeinsam ein Modell unter der Koordination eines zentralen Servers, während die Trainingsdaten dezentral bleiben (Kairouz et al., 2019). Der Ansatz verkörpert die Prinzipien gezielter Datenerhebung und Datenminimierung und kann viele Datenschutzrisiken und Kosten des zentralisierten maschinellen Lernens abmildern. Kairouz et al. fassen den Forschungsstand zusammen und tragen eine umfangreiche Liste offener Probleme zusammen.

#### 5. Leakage über geteilte Gradienten

Das Teilen von Gradienten galt lange als sicher. Zhu et al. (2019) zeigten, dass sich private Trainingsdaten aus öffentlich geteilten Gradienten rekonstruieren lassen, bei Bildern pixelgenau und bei Texten tokengenau. Von den diskutierten Gegenmaßnahmen war Gradient Pruning am wirksamsten. Federated Learning allein garantiert daher keine Privatsphäre.

#### Ursprung und Varianten

Differential Privacy wurde von Dwork et al. (2006) definiert und von Dwork & Roth (2014) systematisiert; Abadi et al. (2016) übertrugen es auf Deep Learning. Federated Learning wurde von McMahan et al. (2016) vorgeschlagen und von Kairouz et al. (2019) im Überblick dargestellt, und Zhu et al. (2019) zeigten seine Grenzen durch Leakage über Gradienten.

### Wann einsetzen

- Wenn Statistiken oder Modelle aus Daten über Personen veröffentlicht werden und einzelne Datensätze nicht erkennbar sein dürfen, bietet Differential Privacy eine formale Garantie (Dwork & Roth, 2014).
- Wenn Trainingsdaten nicht zentral zusammengeführt werden können, etwa weil sie auf Geräten oder bei verschiedenen Organisationen liegen, eignet sich Federated Learning (McMahan et al., 2016; Kairouz et al., 2019).
- Wenn geteilte Aktualisierungen Trainingsdaten preisgeben könnten, sollte Federated Learning mit weiterem Schutz wie Differential Privacy kombiniert werden (Zhu et al., 2019; Abadi et al., 2016).

### Stärken und Grenzen

**Stärken**
- Differential Privacy ist eine mathematisch strenge Definition von Privatsphäre (Dwork & Roth, 2014).
- Tiefe Netze lassen sich mit Differential Privacy bei moderatem Privacy-Budget trainieren (Abadi et al., 2016).
- Federated Learning belässt die Rohdaten bei den Clients und unterstützt Datenminimierung (Kairouz et al., 2019).

**Einschränkungen**
- Differential Privacy kostet etwas Modellqualität und Trainingseffizienz (Abadi et al., 2016).
- Geteilte Gradienten können Trainingsdaten preisgeben (Zhu et al., 2019).
- Federated Learning hat noch viele offene Probleme (Kairouz et al., 2019).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Differential Privacy | Kalibriertes Rauschen begrenzt den Einfluss jeder einzelnen Person (Dwork et al., 2006) | Veröffentlichung von Statistiken oder Modellen aus personenbezogenen Daten |
| DP-Training (nach Art von DP-SGD) | Privacy Accounting während des Trainings neuronaler Netze (Abadi et al., 2016) | Deep Learning auf sensiblen Daten |
| Federated Learning | Daten bleiben bei den Clients; nur Aktualisierungen werden zusammengeführt (McMahan et al., 2016) | Dezentrale Daten auf Geräten oder über Organisationen hinweg |
| Federated Learning mit DP | Verbindet Dezentralität mit einer formalen Garantie (Kairouz et al., 2019; Zhu et al., 2019) | Schutz vor Leakage über Aktualisierungen |

### In der Praxis

Das Privacy-Budget ε muss gewählt und berichtet werden, da es bestimmt, wie stark die Garantie ist (Dwork & Roth, 2014). In föderierten Szenarien sollten Aktualisierungen geschützt werden, weil schon Gradienten Trainingsbeispiele verraten können (Zhu et al., 2019). Ob so geschützte Daten noch personenbezogen sind, ist eine Rechtsfrage, die das Datenschutzrecht beantwortet, nicht die Technik ([[gdpr|Datenschutz-Grundverordnung (DSGVO)]]).

### Merksatz

Differential Privacy begrenzt, was ein Ergebnis über einzelne Personen verrät, Federated Learning lässt Daten dort, wo sie sind, und weil geteilte Aktualisierungen Daten preisgeben können, ergänzen sich beide.

### Quellen

- Dwork, C., McSherry, F., Nissim, K. & Smith, A. (2006). *Calibrating Noise to Sensitivity in Private Data Analysis.* TCC 2006. [doi:10.1007/11681878_14](https://doi.org/10.1007/11681878_14)
- Dwork, C. & Roth, A. (2014). *The Algorithmic Foundations of Differential Privacy.* Foundations and Trends in Theoretical Computer Science 9(3-4). [doi:10.1561/0400000042](https://doi.org/10.1561/0400000042)
- Abadi, M. et al. (2016). *Deep Learning with Differential Privacy.* CCS 2016. [arXiv:1607.00133](https://arxiv.org/abs/1607.00133)
- McMahan, H. B. et al. (2016). *Communication-Efficient Learning of Deep Networks from Decentralized Data.* AISTATS 2017. [arXiv:1602.05629](https://arxiv.org/abs/1602.05629)
- Kairouz, P. et al. (2019). *Advances and Open Problems in Federated Learning.* [arXiv:1912.04977](https://arxiv.org/abs/1912.04977)
- Zhu, L. et al. (2019). *Deep Leakage from Gradients.* NeurIPS 2019. [arXiv:1906.08935](https://arxiv.org/abs/1906.08935)
