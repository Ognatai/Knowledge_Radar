---
title_en: Linear Regression
title_de: Lineare Regression
entity_type: Method
aliases:
- Linear regression
- Ordinary least squares
- OLS
- Least squares regression
- Multiple linear regression
sources:
- https://www.statlearning.com/
- https://scikit-learn.org/stable/modules/linear_model.html
- https://web.stanford.edu/~jurafsky/slp3/4.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Linear regression predicts a numeric response as a weighted sum of predictors plus an intercept, `Y ≈ β₀ + β₁X₁ + … + β_pX_p`, and estimates the coefficients by ordinary least squares, which minimises the sum of squared differences between observed and predicted values (James et al., 2023; scikit-learn). It is the basic supervised learning method for quantitative targets and a tool for inference: standard errors, confidence intervals and t-tests show which predictors are associated with the response (James et al., 2023). Ridge and lasso add penalties on the coefficients to reduce variance and, for lasso, to select features (scikit-learn).

### How it works

```text
data (x_i, y_i), i = 1…n
   ▼
model    ŷ_i = β₀ + β₁ x_i1 + … + β_p x_ip
   ▼
residual e_i = y_i − ŷ_i      RSS = Σ e_i²
   ▼
least squares: choose β that minimises RSS   (closed form via SVD, or gradient descent)
   ▼
assess:  standard errors, t-statistics, p-values  ·  RSE, R²  ·  F-statistic
check:   residual plots for non-linearity, heteroscedasticity, outliers, leverage, collinearity
```

#### 1. The model

Simple linear regression assumes an approximately linear relationship between one predictor X and a response Y, `Y ≈ β₀ + β₁X`, where β₀ is the intercept and β₁ the slope (James et al., 2023). Multiple linear regression gives each predictor its own coefficient, interpreted as the average change in Y for a one-unit increase in that predictor while the others are held fixed (James et al., 2023). Predictors can be transformed, for example squared to fit a curved relationship, or multiplied to model interactions, and the model stays linear in its coefficients (James et al., 2023).

#### 2. Least squares estimation

For observations `(x_i, y_i)`, the residual `e_i = y_i − ŷ_i` is the difference between observed and predicted response, and least squares chooses the coefficients that minimise the residual sum of squares `RSS = Σ e_i²` (James et al., 2023). For one predictor the solution is `β̂₁ = Σ(x_i − x̄)(y_i − ȳ) / Σ(x_i − x̄)²` and `β̂₀ = ȳ − β̂₁ x̄`; in the Advertising data this gives `β̂₀ = 7.03` and `β̂₁ = 0.0475`, so 1,000 dollars more TV advertising is associated with about 47.5 more units sold (James et al., 2023). scikit-learn's `LinearRegression` solves `min_w ||Xw − y||²` with a singular value decomposition at cost `O(n_samples · n_features²)` (scikit-learn). For very large data, the same objective can be minimised with [[gradient-descent|stochastic gradient descent]] (scikit-learn).

#### 3. Accuracy of the coefficients

The standard error of a coefficient says how much its estimate would vary across samples; it gives a 95% confidence interval of roughly two standard errors around the estimate and a t-statistic for testing whether the coefficient is zero (James et al., 2023). A small p-value indicates that an association this strong would be unlikely if there were none; typical cutoffs are 5% or 1% (James et al., 2023; [[statistics-fundamentals|statistics fundamentals]]). In multiple regression, the F-statistic tests whether at least one predictor is associated with the response (James et al., 2023).

#### 4. Fit of the model

The residual standard error (RSE) measures the typical deviation of the response from the regression line in the units of Y; R² is the proportion of variance explained, `R² = 1 − RSS/TSS` with `TSS = Σ(y_i − ȳ)²`, and lies between 0 and 1 (James et al., 2023). For a regression of sales on TV advertising, R² was 0.61 (James et al., 2023). What counts as a good R² depends on the application (James et al., 2023).

#### 5. Regularised variants

When predictors are correlated, the design matrix becomes close to singular and least squares estimates become highly sensitive to random errors (multicollinearity) (scikit-learn). Ridge regression adds `α ||w||²₂` to the objective and shrinks coefficients; lasso adds `α ||w||₁` and can set coefficients exactly to zero, which reduces the number of features the model depends on (scikit-learn; [[regularisation-and-hyperparameters|regularisation]]). In statistics these are known as ridge and lasso regression; L2 corresponds to a Gaussian prior on the weights and L1 to a Laplace prior (Jurafsky & Martin, 2026).

#### Origin and variants

James et al. (2023) describe linear regression as a useful and widely used statistical learning method that many fancier approaches generalise or extend. Generalised linear models such as [[logistic-regression|logistic regression]] keep the linear predictor but change the distribution and link function (James et al., 2023; scikit-learn). Non-negative least squares constrains all coefficients to be non-negative (scikit-learn).

### When to use it

- Predicting a numeric quantity such as sales, prices or demand when the relationship is close to linear (James et al., 2023).
- Estimating and testing the association between predictors and a response, with uncertainty (James et al., 2023).
- As a baseline before non-linear models such as [[ensemble-methods|tree ensembles]] or [[neural-networks|neural networks]].
- With few observations per predictor, where parametric models tend to beat non-parametric ones such as [[k-nearest-neighbours|k-nearest neighbours]] (James et al., 2023).

### Strengths and limitations

**Strengths**
- Interpretable coefficients and well-understood inference (James et al., 2023).
- Closed-form, fast fitting (scikit-learn).
- Outperforms non-parametric methods when the true relationship is close to linear, and is often preferred for interpretability even when KNN is slightly more accurate (James et al., 2023).

**Limitations**
- If the true relationship is far from linear, conclusions and predictions are unreliable; residual plots reveal this (James et al., 2023).
- Correlated errors, as in time series, make standard errors too small and p-values too low (James et al., 2023; [[time-series-analysis|time series analysis]]).
- Non-constant error variance (heteroscedasticity), outliers and high-leverage points distort the fit; a log transform of Y can reduce heteroscedasticity (James et al., 2023).
- Collinear predictors make individual effects hard to separate; the variance inflation factor diagnoses it (James et al., 2023).
- Coefficients describe associations; a causal reading needs a design that rules out confounding ([[causal-inference|causal inference]]).

### Comparison

| Method | Model form | Fitting | Feature selection |
|---|---|---|---|
| Ordinary least squares | linear | minimise RSS | no |
| Ridge | linear | RSS + α‖w‖²₂ | no, shrinks |
| Lasso | linear | RSS + α‖w‖₁ | yes, sets zeros |
| [[k-nearest-neighbours\|KNN regression]] | non-parametric | average of neighbours | no |
| [[logistic-regression\|Logistic regression]] | linear in log odds | maximum likelihood | with L1 |

Sources: James et al. (2023), scikit-learn.

### In practice

Regression output is read together with diagnostics: a residual plot against fitted values should show no pattern, a funnel shape signals heteroscedasticity, and a curved pattern suggests adding transformed predictors such as `horsepower²` (James et al., 2023). Features with very different ranges are standardised to comparable scales (Jurafsky & Martin, 2026), and the penalty α can be chosen by [[cross-validation|cross-validation]], for example with `RidgeCV`, which defaults to efficient leave-one-out cross-validation (scikit-learn). Comparing training and test error guards against [[overfitting|overfitting]], following the [[bias-variance-tradeoff|bias-variance trade-off]].

### Key takeaway

Linear regression fits a weighted sum of predictors by least squares and gives interpretable coefficients with uncertainty, provided its assumptions are checked with residual diagnostics.

### Sources

- James, G., Witten, D., Hastie, T., Tibshirani, R. & Taylor, J. (2023). *An Introduction to Statistical Learning with Applications in Python*, chapter 3: Linear Regression. Springer. [statlearning.com](https://www.statlearning.com/)
- scikit-learn developers. *Linear Models.* scikit-learn documentation. [scikit-learn.org](https://scikit-learn.org/stable/modules/linear_model.html)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3rd ed. draft, 19 August 2026), chapter 4: Logistic Regression and Text Classification, section 4.14: Regularization. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/4.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Die lineare Regression sagt eine numerische Zielgröße als gewichtete Summe von Prädiktoren plus Achsenabschnitt vorher, `Y ≈ β₀ + β₁X₁ + … + β_pX_p`, und schätzt die Koeffizienten mit der Methode der kleinsten Quadrate, die die Summe der quadrierten Abweichungen zwischen beobachteten und vorhergesagten Werten minimiert (James et al., 2023; scikit-learn). Sie ist das grundlegende Verfahren des überwachten Lernens für quantitative Ziele und ein Werkzeug der Inferenz: Standardfehler, Konfidenzintervalle und t-Tests zeigen, welche Prädiktoren mit der Zielgröße zusammenhängen (James et al., 2023). Ridge und Lasso fügen Strafterme auf die Koeffizienten hinzu, um die Varianz zu senken und, beim Lasso, Merkmale auszuwählen (scikit-learn).

### Funktionsweise

```text
Daten (x_i, y_i), i = 1…n
   ▼
Modell    ŷ_i = β₀ + β₁ x_i1 + … + β_p x_ip
   ▼
Residuum  e_i = y_i − ŷ_i      RSS = Σ e_i²
   ▼
kleinste Quadrate: β so wählen, dass RSS minimal ist   (geschlossen per SVD oder Gradientenabstieg)
   ▼
bewerten:  Standardfehler, t-Statistiken, p-Werte  ·  RSE, R²  ·  F-Statistik
prüfen:    Residuenplots auf Nichtlinearität, Heteroskedastizität, Ausreißer, Hebelpunkte, Kollinearität
```

#### 1. Das Modell

Die einfache lineare Regression nimmt einen annähernd linearen Zusammenhang zwischen einem Prädiktor X und einer Zielgröße Y an, `Y ≈ β₀ + β₁X`, mit β₀ als Achsenabschnitt und β₁ als Steigung (James et al., 2023). Die multiple lineare Regression gibt jedem Prädiktor einen eigenen Koeffizienten, der als mittlere Änderung von Y bei Erhöhung dieses Prädiktors um eine Einheit gedeutet wird, während die anderen festgehalten werden (James et al., 2023). Prädiktoren lassen sich transformieren, etwa quadrieren, um einen gekrümmten Zusammenhang abzubilden, oder multiplizieren, um Wechselwirkungen zu modellieren; das Modell bleibt dabei linear in seinen Koeffizienten (James et al., 2023).

#### 2. Schätzung nach kleinsten Quadraten

Für Beobachtungen `(x_i, y_i)` ist das Residuum `e_i = y_i − ŷ_i` die Differenz zwischen beobachteter und vorhergesagter Zielgröße, und die Methode der kleinsten Quadrate wählt die Koeffizienten, die die Residuenquadratsumme `RSS = Σ e_i²` minimieren (James et al., 2023). Für einen Prädiktor lautet die Lösung `β̂₁ = Σ(x_i − x̄)(y_i − ȳ) / Σ(x_i − x̄)²` und `β̂₀ = ȳ − β̂₁ x̄`; in den Advertising-Daten ergibt das `β̂₀ = 7,03` und `β̂₁ = 0,0475`, sodass 1.000 Dollar mehr Fernsehwerbung mit etwa 47,5 zusätzlich verkauften Einheiten einhergehen (James et al., 2023). `LinearRegression` in scikit-learn löst `min_w ||Xw − y||²` mit einer Singulärwertzerlegung zum Aufwand `O(n_samples · n_features²)` (scikit-learn). Bei sehr großen Daten lässt sich dasselbe Ziel mit [[gradient-descent|stochastischem Gradientenabstieg]] minimieren (scikit-learn).

#### 3. Genauigkeit der Koeffizienten

Der Standardfehler eines Koeffizienten gibt an, wie stark seine Schätzung zwischen Stichproben schwanken würde; er liefert ein 95-%-Konfidenzintervall von etwa zwei Standardfehlern um die Schätzung und eine t-Statistik für den Test, ob der Koeffizient null ist (James et al., 2023). Ein kleiner p-Wert zeigt, dass ein so starker Zusammenhang unwahrscheinlich wäre, wenn es keinen gäbe; übliche Schwellen sind 5 % oder 1 % (James et al., 2023; [[statistics-fundamentals|Statistik-Grundlagen]]). In der multiplen Regression prüft die F-Statistik, ob mindestens ein Prädiktor mit der Zielgröße zusammenhängt (James et al., 2023).

#### 4. Güte des Modells

Der Residual Standard Error (RSE) misst die typische Abweichung der Zielgröße von der Regressionsgeraden in den Einheiten von Y; R² ist der Anteil erklärter Varianz, `R² = 1 − RSS/TSS` mit `TSS = Σ(y_i − ȳ)²`, und liegt zwischen 0 und 1 (James et al., 2023). Für eine Regression des Absatzes auf Fernsehwerbung betrug R² 0,61 (James et al., 2023). Was ein gutes R² ist, hängt von der Anwendung ab (James et al., 2023).

#### 5. Regularisierte Varianten

Sind Prädiktoren korreliert, wird die Designmatrix nahezu singulär, und die Schätzungen nach kleinsten Quadraten reagieren stark auf zufällige Fehler (Multikollinearität) (scikit-learn). Die Ridge-Regression fügt dem Ziel `α ||w||²₂` hinzu und schrumpft die Koeffizienten; das Lasso fügt `α ||w||₁` hinzu und kann Koeffizienten genau auf null setzen, was die Zahl der Merkmale verringert, von denen das Modell abhängt (scikit-learn; [[regularisation-and-hyperparameters|Regularisierung]]). In der Statistik heißen sie Ridge- und Lasso-Regression; L2 entspricht einer Gauß-Priorverteilung auf den Gewichten, L1 einer Laplace-Priorverteilung (Jurafsky & Martin, 2026).

#### Ursprung und Varianten

James et al. (2023) beschreiben die lineare Regression als nützliches und weit verbreitetes Verfahren des statistischen Lernens, das viele aufwendigere Ansätze verallgemeinern oder erweitern. Verallgemeinerte lineare Modelle wie die [[logistic-regression|logistische Regression]] behalten den linearen Prädiktor, ändern aber Verteilung und Link-Funktion (James et al., 2023; scikit-learn). Non-Negative Least Squares beschränkt alle Koeffizienten auf nichtnegative Werte (scikit-learn).

### Wann einsetzen

- Eine numerische Größe wie Absatz, Preise oder Nachfrage vorhersagen, wenn der Zusammenhang annähernd linear ist (James et al., 2023).
- Den Zusammenhang zwischen Prädiktoren und Zielgröße schätzen und testen, mit Unsicherheitsangabe (James et al., 2023).
- Als Baseline vor nichtlinearen Modellen wie [[ensemble-methods|Baum-Ensembles]] oder [[neural-networks|neuronalen Netzen]].
- Bei wenigen Beobachtungen pro Prädiktor, wo parametrische Modelle nichtparametrische wie [[k-nearest-neighbours|k-nächste Nachbarn]] meist übertreffen (James et al., 2023).

### Stärken und Grenzen

**Stärken**
- Interpretierbare Koeffizienten und gut verstandene Inferenz (James et al., 2023).
- Geschlossene, schnelle Anpassung (scikit-learn).
- Übertrifft nichtparametrische Verfahren, wenn der wahre Zusammenhang annähernd linear ist, und wird wegen der Interpretierbarkeit oft auch vorgezogen, wenn KNN etwas genauer ist (James et al., 2023).

**Grenzen**
- Ist der wahre Zusammenhang weit von linear entfernt, sind Schlussfolgerungen und Vorhersagen unzuverlässig; Residuenplots zeigen das (James et al., 2023).
- Korrelierte Fehler, wie in Zeitreihen, machen Standardfehler zu klein und p-Werte zu niedrig (James et al., 2023; [[time-series-analysis|Zeitreihenanalyse]]).
- Nicht konstante Fehlervarianz (Heteroskedastizität), Ausreißer und Hebelpunkte verzerren die Anpassung; eine Log-Transformation von Y kann Heteroskedastizität verringern (James et al., 2023).
- Kollineare Prädiktoren machen einzelne Effekte schwer trennbar; der Varianzinflationsfaktor zeigt das an (James et al., 2023).
- Koeffizienten beschreiben Zusammenhänge; eine kausale Deutung braucht ein Design, das Störfaktoren ausschließt ([[causal-inference|kausale Inferenz]]).

### Vergleich

| Verfahren | Modellform | Anpassung | Merkmalsauswahl |
|---|---|---|---|
| Kleinste Quadrate (OLS) | linear | RSS minimieren | nein |
| Ridge | linear | RSS + α‖w‖²₂ | nein, schrumpft |
| Lasso | linear | RSS + α‖w‖₁ | ja, setzt Nullen |
| [[k-nearest-neighbours\|KNN-Regression]] | nichtparametrisch | Mittel der Nachbarn | nein |
| [[logistic-regression\|Logistische Regression]] | linear in den Log-Odds | Maximum Likelihood | mit L1 |

Quellen: James et al. (2023), scikit-learn.

### In der Praxis

Regressionsergebnisse werden zusammen mit Diagnosen gelesen: Ein Residuenplot gegen die angepassten Werte sollte kein Muster zeigen, eine Trichterform weist auf Heteroskedastizität hin, und ein gekrümmtes Muster legt transformierte Prädiktoren wie `horsepower²` nahe (James et al., 2023). Merkmale mit sehr unterschiedlichen Wertebereichen werden auf vergleichbare Skalen standardisiert (Jurafsky & Martin, 2026), und der Strafterm α lässt sich per [[cross-validation|Kreuzvalidierung]] wählen, etwa mit `RidgeCV`, das standardmäßig eine effiziente Leave-One-Out-Kreuzvalidierung nutzt (scikit-learn). Der Vergleich von Trainings- und Testfehler schützt vor [[overfitting|Overfitting]], gemäß dem [[bias-variance-tradeoff|Bias-Varianz-Kompromiss]].

### Merksatz

Die lineare Regression passt eine gewichtete Summe von Prädiktoren nach kleinsten Quadraten an und liefert interpretierbare Koeffizienten mit Unsicherheit, sofern ihre Annahmen mit Residuendiagnosen geprüft werden.

### Quellen

- James, G., Witten, D., Hastie, T., Tibshirani, R. & Taylor, J. (2023). *An Introduction to Statistical Learning with Applications in Python*, Kapitel 3: Linear Regression. Springer. [statlearning.com](https://www.statlearning.com/)
- scikit-learn developers. *Linear Models.* scikit-learn-Dokumentation. [scikit-learn.org](https://scikit-learn.org/stable/modules/linear_model.html)
- Jurafsky, D. & Martin, J. H. (2026). *Speech and Language Processing* (3. Aufl., Entwurf vom 19. August 2026), Kapitel 4: Logistic Regression and Text Classification, Abschnitt 4.14: Regularization. [web.stanford.edu](https://web.stanford.edu/~jurafsky/slp3/4.pdf)
