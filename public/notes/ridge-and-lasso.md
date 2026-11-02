---
title_en: Ridge and Lasso Regression
title_de: Ridge- und Lasso-Regression
entity_type: Method
aliases:
- Ridge regression
- Lasso
- Lasso regression
- L2 regularisation
- L1 regularisation
- Elastic net
- Shrinkage methods
sources:
- https://www.statlearning.com/
- https://scikit-learn.org/stable/modules/linear_model.html
- https://web.stanford.edu/~jurafsky/slp3/4.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Ridge regression and the lasso fit a [[linear-regression|linear model]] by least squares plus a penalty on the size of the coefficients: ridge adds the sum of squared coefficients (L2 penalty), the lasso the sum of their absolute values (L1 penalty) (James et al., 2023). Both shrink the estimates towards zero, trading a little bias for a large reduction in variance, which improves prediction when least squares is unstable, for example with many or correlated predictors (James et al., 2023). The lasso also sets some coefficients exactly to zero and thereby selects variables; the elastic net combines both penalties (James et al., 2023; scikit-learn). The same penalties are the standard L2 and L1 [[regularisation-and-hyperparameters|regularisation]] of [[logistic-regression|logistic regression]] and [[neural-networks|neural networks]] (Jurafsky & Martin, 2026).

### How it works

```text
standardise predictors (mean 0, standard deviation 1)
   ▼
ridge:  minimise  RSS + λ Σ_j β_j²        (L2)   → all coefficients shrunk, none exactly 0
lasso:  minimise  RSS + λ Σ_j |β_j|       (L1)   → some coefficients exactly 0 (sparse)
elastic net:  RSS + α ρ ‖β‖₁ + α (1−ρ)/2 ‖β‖₂²    → sparse, but keeps groups of correlated features
   ▼
choose λ (or α, ρ) by cross-validation on a grid  → refit on all data
```

#### 1. The penalised objective

Least squares minimises the residual sum of squares, `RSS = Σ_i (y_i − β₀ − Σ_j β_j x_ij)²`. Ridge regression minimises `RSS + λ Σ_j β_j²` and the lasso `RSS + λ Σ_j |β_j|`, where the tuning parameter λ ≥ 0 controls the strength of the shrinkage penalty: λ = 0 gives least squares, and as λ grows all estimates approach zero (James et al., 2023). The intercept β₀ is not penalised, because it only measures the mean response (James et al., 2023; Jurafsky & Martin, 2026). Unlike least squares, which gives one solution, ridge and lasso give a path of solutions, one for each λ (James et al., 2023).

#### 2. Why standardise first

Least squares estimates are scale equivariant: measuring a predictor in thousands instead of units only rescales its coefficient. Penalised estimates are not, because the penalty depends on the size of the coefficients, so ridge and lasso are applied after standardising every predictor to standard deviation one (James et al., 2023; [[ml-preprocessing|preprocessing]]).

#### 3. Why shrinkage helps: bias and variance

When the relationship is close to linear, least squares has low bias but may have high variance, especially when the number of predictors p approaches the number of observations n, and for p > n it has no unique solution (James et al., 2023). Increasing λ reduces variance quickly at first with little added bias; in James et al.'s simulation with p = 45 and n = 50, the test error fell sharply up to λ ≈ 10 and was lowest around λ = 30, while least squares was almost as bad as predicting the mean ([[bias-variance-tradeoff|bias-variance trade-off]]; James et al., 2023). When features are correlated, the least squares design matrix becomes nearly singular and the estimates very sensitive to noise, which ridge counters (scikit-learn).

#### 4. Why the lasso gives zeros

Both methods can be written as least squares under a budget: the lasso keeps `Σ |β_j| ≤ s`, ridge `Σ β_j² ≤ s` (James et al., 2023). With two predictors, the lasso budget is a diamond and the ridge budget a circle; the RSS contours usually first touch the diamond at a corner, where one coefficient is exactly zero, but touch the circle away from the axes (James et al., 2023). The lasso is therefore a computationally feasible relative of best subset selection and yields sparse, interpretable models; scikit-learn fits it with coordinate descent (James et al., 2023; scikit-learn). In Bayesian terms, ridge is the posterior mode under a Gaussian prior on the coefficients and the lasso the posterior mode under a Laplace prior, which is sharply peaked at zero (James et al., 2023; Jurafsky & Martin, 2026).

#### 5. Choosing λ and the elastic net

λ is chosen by [[cross-validation|cross-validation]] over a grid of values, and the model is then refit on all data; in a sparse simulation with 45 predictors and 50 observations, cross-validated lasso kept exactly the two true signal variables, while least squares gave a large coefficient to only one of them (James et al., 2023). The elastic net mixes both penalties with a ratio ρ; when several features are correlated, the lasso tends to pick one of them at random, while the elastic net tends to keep them together (scikit-learn).

#### Origin and variants

In statistics, L2 regularisation is known as ridge regression and L1 regularisation as the lasso, introduced by Tibshirani in 1996; both are common in language processing (Jurafsky & Martin, 2026). Ridge regression goes back to Hoerl and Kennard in 1970, as discussed in [[regularisation-and-hyperparameters|regularisation and hyperparameters]]. scikit-learn implements `Ridge`, `Lasso` and `ElasticNet` with cross-validated variants such as `RidgeCV` and `ElasticNetCV` (scikit-learn; [[scikit-learn|scikit-learn]]).

### When to use it

- Linear models with many predictors relative to observations, or with correlated predictors (James et al., 2023; scikit-learn).
- Lasso when only a few predictors are expected to matter and an interpretable, sparse model is wanted ([[feature-engineering|feature selection]]; James et al., 2023).
- Ridge when many predictors each have a small effect (James et al., 2023).
- As the penalty in logistic regression and neural network training (Jurafsky & Martin, 2026); for adaptive optimisers, L2 regularisation and weight decay are not the same ([[adam-optimiser|Adam]]).

### Strengths and limitations

**Strengths**
- Large variance reduction at small cost in bias, often better test error than least squares (James et al., 2023).
- Ridge is computationally almost as cheap as least squares, even for all λ at once (James et al., 2023).
- Lasso performs variable selection, giving simpler models (James et al., 2023).

**Limitations**
- Results depend on predictor scaling, so standardisation is required (James et al., 2023).
- Neither method dominates: ridge did better when all 45 predictors mattered, the lasso when only 2 did, and the truth is unknown in real data (James et al., 2023).
- Lasso picks one of several correlated features arbitrarily (scikit-learn).
- Shrunken coefficients are biased, so they are not unbiased effect estimates for inference.

### Comparison

| Method | Penalty | Zero coefficients | Typical use |
|---|---|---|---|
| Least squares | none | no | few, uncorrelated predictors |
| Ridge | λ Σ β² | no | many small effects, collinearity |
| Lasso | λ Σ \|β\| | yes | sparse signal, interpretability |
| Elastic net | mix of both | yes | correlated groups of features |
| Best subset selection | number of non-zero β | yes | small p only (2^p models) |

Sources: James et al. (2023), scikit-learn.

### In practice

Standardise predictors, fit the regularisation path, pick λ by cross-validation and refit on all data (James et al., 2023). If the cross-validation curve is flat, least squares may be just as good (James et al., 2023). For [[classification|classification]], the same penalties are set in logistic regression; in scikit-learn through the inverse strength C ([[logistic-regression|logistic regression]]).

### Key takeaway

Ridge and lasso stabilise linear models by penalising coefficient size; ridge shrinks all coefficients, the lasso sets some to zero, and λ is chosen by cross-validation on standardised predictors.

### Sources

- James, G., Witten, D., Hastie, T., Tibshirani, R. & Taylor, J. (2023). *An Introduction to Statistical Learning with Applications in Python*, chapter 6: Linear Model Selection and Regularization. Springer. [statlearning.com](https://www.statlearning.com/)
- scikit-learn developers. *Linear Models: Ridge, Lasso, Elastic-Net.* scikit-learn documentation. [scikit-learn.org](https://scikit-learn.org/stable/modules/linear_model.html)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 4, section 4.14: Regularization. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/4.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ridge-Regression und Lasso passen ein [[linear-regression|lineares Modell]] nach kleinsten Quadraten plus einem Strafterm auf die Größe der Koeffizienten an: Ridge addiert die Summe der quadrierten Koeffizienten (L2-Strafterm), das Lasso die Summe ihrer Beträge (L1-Strafterm) (James et al., 2023). Beide schrumpfen die Schätzungen Richtung null und tauschen etwas Bias gegen eine große Verringerung der Varianz, was die Vorhersage verbessert, wenn kleinste Quadrate instabil sind, etwa bei vielen oder korrelierten Prädiktoren (James et al., 2023). Das Lasso setzt zudem manche Koeffizienten genau auf null und wählt so Variablen aus; das Elastic Net kombiniert beide Strafterme (James et al., 2023; scikit-learn). Dieselben Strafterme sind die übliche L2- und L1-[[regularisation-and-hyperparameters|Regularisierung]] der [[logistic-regression|logistischen Regression]] und neuronaler Netze (Jurafsky & Martin, 2026).

### Funktionsweise

```text
Prädiktoren standardisieren (Mittelwert 0, Standardabweichung 1)
   ▼
Ridge:  RSS + λ Σ_j β_j² minimieren        (L2)   → alle Koeffizienten geschrumpft, keiner genau 0
Lasso:  RSS + λ Σ_j |β_j| minimieren       (L1)   → manche Koeffizienten genau 0 (dünn besetzt)
Elastic Net:  RSS + α ρ ‖β‖₁ + α (1−ρ)/2 ‖β‖₂²    → dünn besetzt, behält aber Gruppen korrelierter Merkmale
   ▼
λ (bzw. α, ρ) per Kreuzvalidierung auf einem Raster wählen  → auf allen Daten neu anpassen
```

#### 1. Die bestrafte Zielfunktion

Kleinste Quadrate minimieren die Residuenquadratsumme `RSS = Σ_i (y_i − β₀ − Σ_j β_j x_ij)²`. Die Ridge-Regression minimiert `RSS + λ Σ_j β_j²`, das Lasso `RSS + λ Σ_j |β_j|`, wobei der Tuning-Parameter λ ≥ 0 die Stärke des Schrumpfungsterms steuert: λ = 0 ergibt kleinste Quadrate, und mit wachsendem λ nähern sich alle Schätzungen null (James et al., 2023). Der Achsenabschnitt β₀ wird nicht bestraft, weil er nur die mittlere Zielgröße misst (James et al., 2023; Jurafsky & Martin, 2026). Anders als kleinste Quadrate, die eine Lösung liefern, ergeben Ridge und Lasso einen Pfad von Lösungen, eine für jedes λ (James et al., 2023).

#### 2. Warum zuerst standardisiert wird

Schätzungen nach kleinsten Quadraten sind skalenäquivariant: Wird ein Prädiktor in Tausendern statt in Einheiten gemessen, wird nur sein Koeffizient umskaliert. Bestrafte Schätzungen sind es nicht, weil der Strafterm von der Größe der Koeffizienten abhängt; Ridge und Lasso werden daher angewendet, nachdem jeder Prädiktor auf Standardabweichung eins standardisiert wurde (James et al., 2023; [[ml-preprocessing|Vorverarbeitung]]).

#### 3. Warum Schrumpfen hilft: Bias und Varianz

Ist der Zusammenhang annähernd linear, haben kleinste Quadrate geringen Bias, aber womöglich hohe Varianz, besonders wenn die Zahl der Prädiktoren p sich der Zahl der Beobachtungen n nähert; für p > n gibt es keine eindeutige Lösung (James et al., 2023). Ein wachsendes λ senkt die Varianz zunächst schnell bei wenig zusätzlichem Bias; in der Simulation von James et al. mit p = 45 und n = 50 fiel der Testfehler bis λ ≈ 10 stark und war um λ = 30 am niedrigsten, während kleinste Quadrate fast so schlecht waren wie die Vorhersage des Mittelwerts ([[bias-variance-tradeoff|Bias-Varianz-Kompromiss]]; James et al., 2023). Sind Merkmale korreliert, wird die Designmatrix der kleinsten Quadrate nahezu singulär und die Schätzungen reagieren stark auf Rauschen, was Ridge ausgleicht (scikit-learn).

#### 4. Warum das Lasso Nullen liefert

Beide Verfahren lassen sich als kleinste Quadrate unter einem Budget schreiben: Das Lasso hält `Σ |β_j| ≤ s` ein, Ridge `Σ β_j² ≤ s` (James et al., 2023). Bei zwei Prädiktoren ist das Lasso-Budget eine Raute und das Ridge-Budget ein Kreis; die RSS-Höhenlinien berühren die Raute meist zuerst an einer Ecke, an der ein Koeffizient genau null ist, den Kreis dagegen abseits der Achsen (James et al., 2023). Das Lasso ist damit ein rechnerisch machbarer Verwandter der Best-Subset-Selektion und liefert dünn besetzte, interpretierbare Modelle; scikit-learn passt es per Coordinate Descent an (James et al., 2023; scikit-learn). Bayesianisch betrachtet ist Ridge der Posterior-Modus unter einer Gauß-Priorverteilung der Koeffizienten und das Lasso der Posterior-Modus unter einer Laplace-Priorverteilung, die bei null spitz zuläuft (James et al., 2023; Jurafsky & Martin, 2026).

#### 5. λ wählen und das Elastic Net

λ wird per [[cross-validation|Kreuzvalidierung]] über ein Raster von Werten gewählt, danach wird das Modell auf allen Daten neu angepasst; in einer dünn besetzten Simulation mit 45 Prädiktoren und 50 Beobachtungen behielt das kreuzvalidierte Lasso genau die beiden echten Signalvariablen, während kleinste Quadrate nur einer davon einen großen Koeffizienten gaben (James et al., 2023). Das Elastic Net mischt beide Strafterme mit einem Verhältnis ρ; sind mehrere Merkmale korreliert, wählt das Lasso eher eines davon zufällig, das Elastic Net behält sie eher zusammen (scikit-learn).

#### Ursprung und Varianten

In der Statistik heißt die L2-Regularisierung Ridge-Regression und die L1-Regularisierung Lasso, eingeführt von Tibshirani 1996; beide sind in der Sprachverarbeitung verbreitet (Jurafsky & Martin, 2026). Die Ridge-Regression geht auf Hoerl und Kennard 1970 zurück, wie unter [[regularisation-and-hyperparameters|Regularisierung und Hyperparameter]] beschrieben. scikit-learn bietet `Ridge`, `Lasso` und `ElasticNet` mit kreuzvalidierten Varianten wie `RidgeCV` und `ElasticNetCV` (scikit-learn; [[scikit-learn|scikit-learn]]).

### Wann einsetzen

- Lineare Modelle mit vielen Prädiktoren im Verhältnis zu den Beobachtungen oder mit korrelierten Prädiktoren (James et al., 2023; scikit-learn).
- Lasso, wenn nur wenige Prädiktoren eine Rolle spielen dürften und ein interpretierbares, dünn besetztes Modell gewünscht ist ([[feature-engineering|Merkmalsauswahl]]; James et al., 2023).
- Ridge, wenn viele Prädiktoren jeweils einen kleinen Effekt haben (James et al., 2023).
- Als Strafterm im Training logistischer Regression und neuronaler Netze (Jurafsky & Martin, 2026); bei adaptiven Optimierern sind L2-Regularisierung und Weight Decay nicht dasselbe ([[adam-optimiser|Adam]]).

### Stärken und Grenzen

**Stärken**
- Große Verringerung der Varianz bei geringem Bias, oft mit besserem Testfehler als kleinste Quadrate (James et al., 2023).
- Ridge ist rechnerisch fast so günstig wie kleinste Quadrate, selbst für alle λ zugleich (James et al., 2023).
- Das Lasso wählt Variablen aus und liefert einfachere Modelle (James et al., 2023).

**Grenzen**
- Die Ergebnisse hängen von der Skalierung der Prädiktoren ab, Standardisierung ist daher nötig (James et al., 2023).
- Keines der Verfahren dominiert: Ridge war besser, wenn alle 45 Prädiktoren eine Rolle spielten, das Lasso, wenn es nur 2 waren, und in echten Daten ist die Wahrheit unbekannt (James et al., 2023).
- Das Lasso wählt unter mehreren korrelierten Merkmalen willkürlich eines (scikit-learn).
- Geschrumpfte Koeffizienten sind verzerrt und daher keine unverzerrten Effektschätzungen für die Inferenz.

### Vergleich

| Verfahren | Strafterm | Koeffizienten genau null | Typischer Einsatz |
|---|---|---|---|
| Kleinste Quadrate | keiner | nein | wenige, unkorrelierte Prädiktoren |
| Ridge | λ Σ β² | nein | viele kleine Effekte, Kollinearität |
| Lasso | λ Σ \|β\| | ja | dünn besetztes Signal, Interpretierbarkeit |
| Elastic Net | Mischung aus beiden | ja | korrelierte Gruppen von Merkmalen |
| Best-Subset-Selektion | Zahl der β ungleich null | ja | nur kleines p (2^p Modelle) |

Quellen: James et al. (2023), scikit-learn.

### In der Praxis

Prädiktoren standardisieren, den Regularisierungspfad anpassen, λ per Kreuzvalidierung wählen und auf allen Daten neu anpassen (James et al., 2023). Ist die Kreuzvalidierungskurve flach, können kleinste Quadrate ebenso gut sein (James et al., 2023). Für die [[classification|Klassifikation]] werden dieselben Strafterme in der logistischen Regression gesetzt, in scikit-learn über die inverse Stärke C ([[logistic-regression|logistische Regression]]).

### Merksatz

Ridge und Lasso stabilisieren lineare Modelle, indem sie die Größe der Koeffizienten bestrafen; Ridge schrumpft alle Koeffizienten, das Lasso setzt manche auf null, und λ wird per Kreuzvalidierung auf standardisierten Prädiktoren gewählt.

### Quellen

- James, G., Witten, D., Hastie, T., Tibshirani, R. & Taylor, J. (2023). *An Introduction to Statistical Learning with Applications in Python*, Kapitel 6: Linear Model Selection and Regularization. Springer. [statlearning.com](https://www.statlearning.com/)
- scikit-learn developers. *Linear Models: Ridge, Lasso, Elastic-Net.* scikit-learn-Dokumentation. [scikit-learn.org](https://scikit-learn.org/stable/modules/linear_model.html)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 4, Abschnitt 4.14: Regularization. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/4.pdf)
