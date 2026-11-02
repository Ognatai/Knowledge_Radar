---
title_en: Recommender Systems
title_de: Recommender-Systeme
entity_type: Method
aliases:
- Recommender systems
- Recommender system
- Recommendation systems
- Collaborative filtering
- Matrix factorisation for recommendation
- Bayesian Personalized Ranking
- BPR
- Neural collaborative filtering
- Empfehlungssysteme
sources:
- https://arxiv.org/abs/1205.2618
- https://arxiv.org/abs/1708.05031
- https://arxiv.org/abs/2005.09683
- https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45530.pdf
- https://arxiv.org/abs/2403.05440
- https://eur-lex.europa.eu/eli/reg/2022/2065/oj/eng
- https://eur-lex.europa.eu/eli/reg/2022/2065/oj/deu
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A recommender system predicts which items, such as videos, products or articles, a user is likely to want and presents a personalised ranking (Rendle et al., 2009). Collaborative filtering learns this from the interactions of many users, typically from implicit feedback such as clicks and purchases rather than explicit ratings, by giving users and items [[embeddings|embeddings]] whose dot product scores how well they match (Rendle et al., 2009; Rendle et al., 2020). Large systems such as YouTube split the work into candidate generation, which narrows millions of items to hundreds, and a ranking model that orders the final few (Covington et al., 2016).

### How it works

```text
interaction log (user, item, click / watch / purchase, time)
   ▼
learn user embeddings p_u and item embeddings q_i   (matrix factorisation, neural models)
   score(u, i) = p_u · q_i            trained for ranking, e.g. BPR: item seen > item not seen
   ▼
candidate generation: nearest-neighbour search over item embeddings  →  millions ▸ hundreds
   ▼
ranking model with rich features (context, freshness, item metadata)  →  hundreds ▸ dozens
   ▼
offline metrics (precision, recall, ranking loss) ──► A/B test online (click-through rate, watch time)
```

#### 1. Feedback and the task

Item recommendation is the task of predicting a personalised ranking over items; the most common scenario uses implicit feedback such as clicks or purchases, where only positive interactions are observed and missing entries mix negatives with items the user simply has not seen (Rendle et al., 2009). YouTube rarely obtains ground truth of user satisfaction and models noisy implicit signals instead, and its corpus changes constantly as many hours of video are uploaded every second, which requires balancing new and established content (Covington et al., 2016).

#### 2. Matrix factorisation

Embedding-based models have been the state of the art in collaborative filtering for over a decade: users and items get latent vectors and their dot product predicts the preference, as in matrix factorisation (Rendle et al., 2020). Similar users end up with similar vectors because they interacted with similar items, without any item content being needed. Learned embeddings have a scaling freedom that leaves dot products unchanged, so [[cosine-similarity|cosine similarities]] between them can be arbitrary; scores should be computed the way the model was trained (Steck et al., 2024).

#### 3. Training for ranking: BPR

Methods such as matrix factorisation or adaptive k-nearest neighbours are used for ranking but were not trained for it. Bayesian Personalized Ranking (BPR) creates user-specific pairwise preferences, an observed item i is preferred to an unobserved item j, and maximises `Σ log σ(x̂_ui − x̂_uj)` plus regularisation, the maximum posterior estimator for this assumption; it is learned with [[gradient-descent|stochastic gradient descent]] over bootstrap-sampled triples and outperformed the standard training of matrix factorisation and kNN for personalised ranking (Rendle et al., 2009). The criterion is closely related to optimising the area under the ROC curve (Rendle et al., 2009; [[learning-to-rank|learning to rank]]).

#### 4. Neural models and their evaluation

Neural collaborative filtering replaced the dot product with a multilayer perceptron that can learn an arbitrary interaction function (He et al., 2017). Rendle et al. (2020) revisited these experiments: with proper hyperparameter selection, a plain dot product substantially outperformed the learned MLP similarity, an MLP has difficulty learning a dot product, and dot products allow efficient nearest-neighbour retrieval, which MLPs do not ([[vector-databases|vector databases]]). Careful baselines and tuning therefore decide such comparisons ([[hyperparameter-optimisation|hyperparameter optimisation]]).

#### 5. Two-stage architecture at scale

YouTube's system uses one deep network for candidate generation, which treats recommendation as a [[classification|classification]] over millions of videos with a [[softmax|softmax]] trained on sampled negative classes and selects hundreds of candidates from the user's history, search tokens and demographics, and a second network for ranking, which scores the candidates with richer features (Covington et al., 2016). The ranking model was trained to predict expected watch time with weighted [[logistic-regression|logistic regression]], because click-through rate favours deceptive "clickbait" videos that users do not finish (Covington et al., 2016).

#### Origin and variants

BPR appeared at UAI 2009 (Rendle et al., 2009), neural collaborative filtering at WWW 2017 (He et al., 2017) and its re-examination at RecSys 2020 (Rendle et al., 2020). Content features such as text or images can be added through their embeddings, and graph-based recommenders use [[graph-neural-networks|graph neural networks]].

### When to use it

- Personalising feeds, shops, media and search results from user behaviour (Covington et al., 2016).
- "Users who liked this also liked" suggestions from interaction data alone (Rendle et al., 2009).
- Large catalogues where candidate retrieval with embeddings must precede expensive ranking (Covington et al., 2016).

### Strengths and limitations

**Strengths**
- Learns from implicit feedback without explicit ratings or item descriptions (Rendle et al., 2009).
- Dot-product embeddings are fast to serve with nearest-neighbour search (Rendle et al., 2020).
- The two-stage design combines broad recall with precise ranking (Covington et al., 2016).

**Limitations**
- New items and users have no interactions yet; freshness has to be modelled explicitly (Covington et al., 2016).
- Implicit feedback is noisy and does not show what users disliked (Rendle et al., 2009; Covington et al., 2016).
- Optimising engagement proxies can reward clickbait unless the objective is chosen carefully (Covington et al., 2016).
- Offline metrics do not always agree with live A/B tests (Covington et al., 2016).

### Comparison

| Approach | Score | Training signal | Note |
|---|---|---|---|
| Matrix factorisation | p_u · q_i | ratings or implicit feedback | strong, fast baseline |
| BPR-trained MF | p_u · q_i | pairwise: seen > unseen | optimises ranking |
| Neural collaborative filtering | MLP(p_u, q_i) | implicit feedback | dot product beat it when tuned |
| Two-stage deep system (YouTube) | candidate softmax, then ranker | watches, context | scales to millions of items |

Sources: Rendle et al. (2009), He et al. (2017), Rendle et al. (2020), Covington et al. (2016).

### In practice

Offline metrics such as precision, recall and ranking loss guide development, but the final decision rests on live A/B tests measuring click-through rate, watch time and other engagement metrics, because the two do not always agree (Covington et al., 2016; [[classification-metrics|classification metrics]]). Under the [[digital-services-act|Digital Services Act]], online platforms that use recommender systems must state their main parameters and the options to influence them in their terms (Art. 27), and very large platforms must offer at least one option not based on profiling (Art. 38).

### Key takeaway

Recommender systems learn user and item embeddings from implicit feedback, train them to rank seen items above unseen ones, and at scale retrieve candidates by embedding similarity before a richer model ranks them; dot products remain a strong default.

### Sources

- Rendle, S., Freudenthaler, C., Gantner, Z. & Schmidt-Thieme, L. (2009). *BPR: Bayesian Personalized Ranking from Implicit Feedback.* UAI 2009. [arXiv:1205.2618](https://arxiv.org/abs/1205.2618)
- He, X. et al. (2017). *Neural Collaborative Filtering.* WWW 2017. [arXiv:1708.05031](https://arxiv.org/abs/1708.05031)
- Rendle, S., Krichene, W., Zhang, L. & Anderson, J. (2020). *Neural Collaborative Filtering vs. Matrix Factorization Revisited.* RecSys 2020. [arXiv:2005.09683](https://arxiv.org/abs/2005.09683)
- Covington, P., Adams, J. & Sargin, E. (2016). *Deep Neural Networks for YouTube Recommendations.* RecSys 2016. [research.google](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45530.pdf)
- Steck, H., Ekanadham, C. & Kallus, N. (2024). *Is Cosine-Similarity of Embeddings Really About Similarity?* WWW 2024 Companion. [arXiv:2403.05440](https://arxiv.org/abs/2403.05440)
- Regulation (EU) 2022/2065 (Digital Services Act), Articles 27 and 38. [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg/2022/2065/oj/eng)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Recommender-System sagt vorher, welche Elemente wie Videos, Produkte oder Artikel eine Person vermutlich haben möchte, und zeigt eine personalisierte Rangfolge (Rendle et al., 2009). Collaborative Filtering lernt das aus den Interaktionen vieler Nutzender, meist aus implizitem Feedback wie Klicks und Käufen statt aus expliziten Bewertungen, indem es Nutzenden und Elementen [[embeddings|Embeddings]] gibt, deren Skalarprodukt bewertet, wie gut sie zusammenpassen (Rendle et al., 2009; Rendle et al., 2020). Große Systeme wie YouTube teilen die Arbeit in eine Kandidatengenerierung, die Millionen Elemente auf Hunderte eingrenzt, und ein Ranking-Modell, das die letzten wenigen ordnet (Covington et al., 2016).

### Funktionsweise

```text
Interaktionsprotokoll (Nutzende, Element, Klick / Ansicht / Kauf, Zeit)
   ▼
Nutzer-Embeddings p_u und Element-Embeddings q_i lernen   (Matrixfaktorisierung, neuronale Modelle)
   score(u, i) = p_u · q_i            für das Ranking trainiert, z. B. BPR: gesehenes Element > ungesehenes
   ▼
Kandidatengenerierung: Nächste-Nachbarn-Suche über Element-Embeddings  →  Millionen ▸ Hunderte
   ▼
Ranking-Modell mit reichen Merkmalen (Kontext, Aktualität, Metadaten)  →  Hunderte ▸ Dutzende
   ▼
Offline-Metriken (Precision, Recall, Ranking-Verlust) ──► A/B-Test online (Klickrate, Sehdauer)
```

#### 1. Feedback und Aufgabe

Element-Empfehlung ist die Aufgabe, eine personalisierte Rangfolge über Elemente vorherzusagen; das häufigste Szenario nutzt implizites Feedback wie Klicks oder Käufe, bei dem nur positive Interaktionen beobachtet werden und fehlende Einträge echte Ablehnungen mit Elementen vermischen, die die Person schlicht nicht gesehen hat (Rendle et al., 2009). YouTube erhält selten eine Grundwahrheit über die Zufriedenheit der Nutzenden und modelliert stattdessen verrauschte implizite Signale, und sein Bestand ändert sich ständig, weil jede Sekunde viele Stunden Video hochgeladen werden, was ein Abwägen zwischen neuen und etablierten Inhalten verlangt (Covington et al., 2016).

#### 2. Matrixfaktorisierung

Embedding-basierte Modelle sind seit über einem Jahrzehnt der Stand der Technik im Collaborative Filtering: Nutzende und Elemente erhalten latente Vektoren, deren Skalarprodukt die Präferenz vorhersagt, wie bei der Matrixfaktorisierung (Rendle et al., 2020). Ähnliche Nutzende erhalten ähnliche Vektoren, weil sie mit ähnlichen Elementen interagierten, ohne dass Inhalte der Elemente nötig wären. Gelernte Embeddings haben einen Skalierungsfreiheitsgrad, der die Skalarprodukte unverändert lässt, sodass [[cosine-similarity|Cosine Similarities]] zwischen ihnen beliebig sein können; Scores sollten so berechnet werden, wie das Modell trainiert wurde (Steck et al., 2024).

#### 3. Training für das Ranking: BPR

Verfahren wie Matrixfaktorisierung oder adaptive k-nächste Nachbarn werden für Rankings genutzt, aber nicht dafür trainiert. Bayesian Personalized Ranking (BPR) bildet nutzerspezifische paarweise Präferenzen, ein beobachtetes Element i wird einem nicht beobachteten j vorgezogen, und maximiert `Σ log σ(x̂_ui − x̂_uj)` plus Regularisierung, den Maximum-a-posteriori-Schätzer für diese Annahme; gelernt wird mit [[gradient-descent|stochastischem Gradientenabstieg]] über per Bootstrap gezogene Tripel, und es übertraf das übliche Training von Matrixfaktorisierung und kNN beim personalisierten Ranking (Rendle et al., 2009). Das Kriterium ist eng mit der Optimierung der Fläche unter der ROC-Kurve verwandt (Rendle et al., 2009; [[learning-to-rank|Learning to Rank]]).

#### 4. Neuronale Modelle und ihre Evaluation

Neural Collaborative Filtering ersetzte das Skalarprodukt durch ein mehrschichtiges Perzeptron, das eine beliebige Interaktionsfunktion lernen kann (He et al., 2017). Rendle et al. (2020) wiederholten diese Experimente: Mit sorgfältiger Wahl der Hyperparameter übertraf ein einfaches Skalarprodukt die gelernte MLP-Ähnlichkeit deutlich, ein MLP lernt ein Skalarprodukt nur schwer, und Skalarprodukte erlauben eine effiziente Nächste-Nachbarn-Suche, MLPs nicht ([[vector-databases|Vektordatenbanken]]). Sorgfältige Baselines und Tuning entscheiden solche Vergleiche daher ([[hyperparameter-optimisation|Hyperparameter-Optimierung]]).

#### 5. Zweistufige Architektur im großen Maßstab

Das System von YouTube nutzt ein tiefes Netz für die Kandidatengenerierung, das die Empfehlung als [[classification|Klassifikation]] über Millionen Videos mit einer auf gezogenen Negativklassen trainierten [[softmax|Softmax]] behandelt und aus Verlauf, Suchbegriffen und demografischen Merkmalen Hunderte Kandidaten auswählt, und ein zweites Netz für das Ranking, das die Kandidaten mit reicheren Merkmalen bewertet (Covington et al., 2016). Das Ranking-Modell wurde mit gewichteter logistischer Regression darauf trainiert, die erwartete Sehdauer vorherzusagen, weil die Klickrate irreführende „Clickbait“-Videos begünstigt, die Nutzende nicht zu Ende sehen (Covington et al., 2016).

#### Ursprung und Varianten

BPR erschien auf der UAI 2009 (Rendle et al., 2009), Neural Collaborative Filtering auf der WWW 2017 (He et al., 2017) und seine Nachprüfung auf der RecSys 2020 (Rendle et al., 2020). Inhaltsmerkmale wie Text oder Bilder lassen sich über ihre Embeddings ergänzen, und graphbasierte Recommender nutzen [[graph-neural-networks|Graph Neural Networks]].

### Wann einsetzen

- Feeds, Shops, Medienangebote und Suchergebnisse anhand des Nutzungsverhaltens personalisieren (Covington et al., 2016).
- Vorschläge der Art „Wer das mochte, mochte auch“ allein aus Interaktionsdaten (Rendle et al., 2009).
- Große Kataloge, bei denen eine Kandidatensuche mit Embeddings dem aufwendigen Ranking vorausgehen muss (Covington et al., 2016).

### Stärken und Grenzen

**Stärken**
- Lernt aus implizitem Feedback ohne explizite Bewertungen oder Beschreibungen der Elemente (Rendle et al., 2009).
- Embeddings mit Skalarprodukt lassen sich mit Nächste-Nachbarn-Suche schnell bedienen (Rendle et al., 2020).
- Die zweistufige Architektur verbindet breiten Recall mit präzisem Ranking (Covington et al., 2016).

**Grenzen**
- Neue Elemente und Nutzende haben noch keine Interaktionen; Aktualität muss ausdrücklich modelliert werden (Covington et al., 2016).
- Implizites Feedback ist verrauscht und zeigt nicht, was Nutzenden missfiel (Rendle et al., 2009; Covington et al., 2016).
- Das Optimieren von Engagement-Ersatzgrößen kann Clickbait belohnen, wenn das Ziel nicht sorgfältig gewählt ist (Covington et al., 2016).
- Offline-Metriken stimmen nicht immer mit Live-A/B-Tests überein (Covington et al., 2016).

### Vergleich

| Ansatz | Score | Trainingssignal | Bemerkung |
|---|---|---|---|
| Matrixfaktorisierung | p_u · q_i | Bewertungen oder implizites Feedback | starke, schnelle Baseline |
| Mit BPR trainierte MF | p_u · q_i | paarweise: gesehen > ungesehen | optimiert das Ranking |
| Neural Collaborative Filtering | MLP(p_u, q_i) | implizites Feedback | getuntes Skalarprodukt war besser |
| Zweistufiges tiefes System (YouTube) | Kandidaten-Softmax, dann Ranker | Ansichten, Kontext | skaliert auf Millionen Elemente |

Quellen: Rendle et al. (2009), He et al. (2017), Rendle et al. (2020), Covington et al. (2016).

### In der Praxis

Offline-Metriken wie Precision, Recall und Ranking-Verlust leiten die Entwicklung, die endgültige Entscheidung beruht aber auf Live-A/B-Tests, die Klickrate, Sehdauer und andere Engagement-Metriken messen, weil beides nicht immer übereinstimmt (Covington et al., 2016; [[classification-metrics|Klassifikationsmetriken]]). Nach dem [[digital-services-act|Digital Services Act]] müssen Online-Plattformen, die Empfehlungssysteme nutzen, deren wichtigste Parameter und die Möglichkeiten, sie zu beeinflussen, in ihren Geschäftsbedingungen angeben (Art. 27), und sehr große Plattformen müssen mindestens eine Option anbieten, die nicht auf Profiling beruht (Art. 38).

### Merksatz

Recommender-Systeme lernen Embeddings von Nutzenden und Elementen aus implizitem Feedback, trainieren sie darauf, gesehene Elemente über ungesehene zu stellen, und holen im großen Maßstab Kandidaten über Embedding-Ähnlichkeit, bevor ein reicheres Modell sie ordnet; das Skalarprodukt bleibt eine starke Voreinstellung.

### Quellen

- Rendle, S., Freudenthaler, C., Gantner, Z. & Schmidt-Thieme, L. (2009). *BPR: Bayesian Personalized Ranking from Implicit Feedback.* UAI 2009. [arXiv:1205.2618](https://arxiv.org/abs/1205.2618)
- He, X. et al. (2017). *Neural Collaborative Filtering.* WWW 2017. [arXiv:1708.05031](https://arxiv.org/abs/1708.05031)
- Rendle, S., Krichene, W., Zhang, L. & Anderson, J. (2020). *Neural Collaborative Filtering vs. Matrix Factorization Revisited.* RecSys 2020. [arXiv:2005.09683](https://arxiv.org/abs/2005.09683)
- Covington, P., Adams, J. & Sargin, E. (2016). *Deep Neural Networks for YouTube Recommendations.* RecSys 2016. [research.google](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45530.pdf)
- Steck, H., Ekanadham, C. & Kallus, N. (2024). *Is Cosine-Similarity of Embeddings Really About Similarity?* WWW 2024 Companion. [arXiv:2403.05440](https://arxiv.org/abs/2403.05440)
- Verordnung (EU) 2022/2065 (Gesetz über digitale Dienste), Artikel 27 und 38. [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg/2022/2065/oj/deu)
