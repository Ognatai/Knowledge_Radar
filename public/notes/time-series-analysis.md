---
title_en: Time Series Analysis
title_de: Zeitreihenanalyse
entity_type: Method
sources:
- https://otexts.com/fpp3/
- https://doi.org/10.1080/01621459.1979.10482531
- https://doi.org/10.1016/j.ijforecast.2006.03.001
- https://doi.org/10.1016/j.ijforecast.2018.06.001
- https://doi.org/10.1162/neco.1997.9.8.1735
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Time series analysis models data observed over time to understand and forecast it. It describes patterns such as trend and seasonality, checks whether a series is stationary (Dickey & Fuller, 1979), uses autocorrelation to select models such as exponential smoothing and ARIMA, and evaluates forecasts on later data (Hyndman & Athanasopoulos, 2021). In a large forecasting competition, combinations of methods and a hybrid statistical-neural method did best, while pure machine learning methods did poorly (Makridakis et al., 2018).

### How it works

A series is inspected for trend, seasonality and autocorrelation, transformed to stationarity if the model requires it, and a forecasting model is fitted. Forecasts are evaluated on data that comes after the training period.

```text
1. Patterns and decomposition
▼
2. Stationarity and unit roots
▼
3. Autocorrelation
▼
4. Classical forecasting models
▼
5. Forecast evaluation
▼
6. Neural sequence models
```

#### 1. Patterns and decomposition

Time series show patterns such as trend, seasonality and cycles, and decomposition methods separate a series into these components and a remainder (Hyndman & Athanasopoulos, 2021). Recognising them is the starting point for choosing a model.

#### 2. Stationarity and unit roots

Many models, such as ARIMA, assume that a series is stationary, i.e. that its statistical properties do not change over time; differencing removes trends (Hyndman & Athanasopoulos, 2021). Dickey & Fuller (1979) derived the distribution of the regression estimator and t test for the autoregressive model Y_t = ρY_(t−1) + e_t under ρ = 1, which provides a test of the hypothesis of a unit root, i.e. non-stationarity.

#### 3. Autocorrelation

The autocorrelation function (ACF) shows how strongly a series is correlated with its own past values, and the partial autocorrelation function (PACF) shows this after removing the effect of the intermediate lags. Both guide the choice of model orders (Hyndman & Athanasopoulos, 2021).

#### 4. Classical forecasting models

Exponential smoothing (ETS) and ARIMA models, including seasonal ARIMA, are the classical forecasting models (Hyndman & Athanasopoulos, 2021). In the M4 competition on 100,000 time series, combinations of methods performed well, the best method was a hybrid of a statistical model and a neural network, and pure machine learning methods performed poorly compared with statistical benchmarks (Makridakis et al., 2018).

#### 5. Forecast evaluation

Forecasts are evaluated on test data from after the training period and with time series cross-validation, never on randomly shuffled data (Hyndman & Athanasopoulos, 2021). Hyndman & Koehler (2006) showed that many accuracy measures can be infinite, undefined or misleading, for example percentage errors when actual values are zero or close to zero, and proposed the mean absolute scaled error (MASE), which scales errors by the in-sample mean absolute error of a naive forecast.

#### 6. Neural sequence models

Long short-term memory (LSTM) networks keep error flow constant over long time lags through gated memory cells and can learn dependencies over more than 1000 time steps, where earlier recurrent networks failed (Hochreiter & Schmidhuber, 1997; [[recurrent-neural-networks|Recurrent Neural Networks]]).

#### Origin and variants

Unit-root testing (Dickey & Fuller, 1979), LSTM networks (Hochreiter & Schmidhuber, 1997), scale-free accuracy measures (Hyndman & Koehler, 2006) and the M4 competition (Makridakis et al., 2018) are milestones; Hyndman & Athanasopoulos (2021) give a textbook overview of classical forecasting.

### When to use it

- When future values of a series must be forecast from its past, for example demand or load (Hyndman & Athanasopoulos, 2021).
- When forecast accuracy must be compared across series with different scales or zero values, MASE is suitable (Hyndman & Koehler, 2006).
- When choosing between statistical and machine learning methods, the M4 results suggest starting with statistical methods and combinations (Makridakis et al., 2018).

### Strengths and limitations

**Strengths**
- Classical models such as ETS and ARIMA are well understood and interpretable (Hyndman & Athanasopoulos, 2021).
- Combinations and hybrid methods performed best in a large competition (Makridakis et al., 2018).
- LSTMs can capture long-range dependencies (Hochreiter & Schmidhuber, 1997).

**Limitations**
- Many models require stationarity, which has to be tested and established (Dickey & Fuller, 1979).
- Common accuracy measures can be undefined or misleading (Hyndman & Koehler, 2006).
- Pure machine learning methods performed poorly in the M4 competition (Makridakis et al., 2018).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Exponential smoothing (ETS) | Weighted averages of past observations with trend and seasonality (Hyndman & Athanasopoulos, 2021) | Series with clear trend and seasonality |
| ARIMA | Models autocorrelation of a stationary (differenced) series (Hyndman & Athanasopoulos, 2021) | Series with autocorrelation structure |
| Hybrid statistical-neural methods | Combine statistical models and neural networks (Makridakis et al., 2018) | Large collections of series |
| LSTM | Recurrent network with gated memory cells (Hochreiter & Schmidhuber, 1997) | Long-range dependencies, large data |

### In practice

Data is split in time order, never at random, and models are evaluated with time series cross-validation against simple benchmarks such as the naive forecast (Hyndman & Athanasopoulos, 2021; Hyndman & Koehler, 2006). Seasonal patterns can also be given to regression models as features ([[feature-engineering|Feature Engineering]]).

### Key takeaway

Time series analysis builds forecasts from trend, seasonality and autocorrelation, evaluates them strictly on later data, and simple statistical methods and combinations are hard to beat.

### Sources

- Hyndman, R. J. & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3rd ed.). OTexts. [online edition](https://otexts.com/fpp3/)
- Dickey, D. A. & Fuller, W. A. (1979). *Distribution of the Estimators for Autoregressive Time Series with a Unit Root.* Journal of the American Statistical Association 74(366). [doi:10.1080/01621459.1979.10482531](https://doi.org/10.1080/01621459.1979.10482531)
- Hyndman, R. J. & Koehler, A. B. (2006). *Another look at measures of forecast accuracy.* International Journal of Forecasting 22(4). [doi:10.1016/j.ijforecast.2006.03.001](https://doi.org/10.1016/j.ijforecast.2006.03.001)
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2018). *The M4 Competition: Results, findings, conclusion and way forward.* International Journal of Forecasting 34(4). [doi:10.1016/j.ijforecast.2018.06.001](https://doi.org/10.1016/j.ijforecast.2018.06.001)
- Hochreiter, S. & Schmidhuber, J. (1997). *Long Short-Term Memory.* Neural Computation 9(8). [doi:10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Zeitreihenanalyse modelliert über die Zeit beobachtete Daten, um sie zu verstehen und vorherzusagen. Sie beschreibt Muster wie Trend und Saisonalität, prüft, ob eine Reihe stationär ist (Dickey & Fuller, 1979), wählt anhand der Autokorrelation Modelle wie exponentielle Glättung und ARIMA und bewertet Prognosen auf späteren Daten (Hyndman & Athanasopoulos, 2021). In einem großen Prognosewettbewerb schnitten Kombinationen von Verfahren und eine hybride statistisch-neuronale Methode am besten ab, reine Machine-Learning-Verfahren dagegen schlecht (Makridakis et al., 2018).

### Funktionsweise

Eine Reihe wird auf Trend, Saisonalität und Autokorrelation untersucht, bei Bedarf in eine stationäre Form überführt und mit einem Prognosemodell beschrieben. Prognosen werden auf Daten bewertet, die nach dem Trainingszeitraum liegen.

```text
1. Muster und Zerlegung
▼
2. Stationarität und Einheitswurzeln
▼
3. Autokorrelation
▼
4. Klassische Prognosemodelle
▼
5. Bewertung von Prognosen
▼
6. Neuronale Sequenzmodelle
```

#### 1. Muster und Zerlegung

Zeitreihen zeigen Muster wie Trend, Saisonalität und Zyklen, und Zerlegungsverfahren trennen eine Reihe in diese Komponenten und einen Rest (Hyndman & Athanasopoulos, 2021). Sie zu erkennen ist der Ausgangspunkt für die Modellwahl.

#### 2. Stationarität und Einheitswurzeln

Viele Modelle wie ARIMA setzen voraus, dass eine Reihe stationär ist, ihre statistischen Eigenschaften sich also über die Zeit nicht ändern; Differenzenbildung entfernt Trends (Hyndman & Athanasopoulos, 2021). Dickey & Fuller (1979) leiteten für das autoregressive Modell Y_t = ρY_(t−1) + e_t die Verteilung des Regressionsschätzers und des t-Tests unter ρ = 1 her; das liefert einen Test der Hypothese einer Einheitswurzel, also von Nichtstationarität.

#### 3. Autokorrelation

Die Autokorrelationsfunktion (ACF) zeigt, wie stark eine Reihe mit ihren eigenen früheren Werten korreliert, die partielle Autokorrelationsfunktion (PACF) zeigt dies nach Herausrechnen der dazwischenliegenden Verzögerungen. Beide leiten die Wahl der Modellordnungen an (Hyndman & Athanasopoulos, 2021).

#### 4. Klassische Prognosemodelle

Exponentielle Glättung (ETS) und ARIMA-Modelle, einschließlich saisonaler ARIMA, sind die klassischen Prognosemodelle (Hyndman & Athanasopoulos, 2021). Im M4-Wettbewerb mit 100.000 Zeitreihen schnitten Kombinationen von Verfahren gut ab, die beste Methode war eine Hybride aus statistischem Modell und neuronalem Netz, und reine Machine-Learning-Verfahren schnitten im Vergleich zu statistischen Benchmarks schlecht ab (Makridakis et al., 2018).

#### 5. Bewertung von Prognosen

Prognosen werden auf Testdaten aus der Zeit nach dem Trainingszeitraum und mit Zeitreihen-Kreuzvalidierung bewertet, nie auf zufällig gemischten Daten (Hyndman & Athanasopoulos, 2021). Hyndman & Koehler (2006) zeigten, dass viele Genauigkeitsmaße unendlich, undefiniert oder irreführend sein können, etwa prozentuale Fehler bei tatsächlichen Werten von null oder nahe null, und schlugen den Mean Absolute Scaled Error (MASE) vor, der Fehler durch den mittleren absoluten Fehler einer naiven Prognose im Trainingszeitraum skaliert.

#### 6. Neuronale Sequenzmodelle

Long Short-Term Memory (LSTM) hält den Fehlerfluss über gesteuerte Speicherzellen auch über lange Zeitabstände konstant und kann Abhängigkeiten über mehr als 1000 Zeitschritte lernen, woran frühere rekurrente Netze scheiterten (Hochreiter & Schmidhuber, 1997; [[recurrent-neural-networks|RNN und Zeitreihen]]).

#### Ursprung und Varianten

Tests auf Einheitswurzeln (Dickey & Fuller, 1979), LSTM-Netze (Hochreiter & Schmidhuber, 1997), skalenfreie Genauigkeitsmaße (Hyndman & Koehler, 2006) und der M4-Wettbewerb (Makridakis et al., 2018) sind Meilensteine; Hyndman & Athanasopoulos (2021) geben einen Lehrbuchüberblick über klassische Prognoseverfahren.

### Wann einsetzen

- Wenn künftige Werte einer Reihe aus ihrer Vergangenheit vorhergesagt werden sollen, etwa Nachfrage oder Last (Hyndman & Athanasopoulos, 2021).
- Wenn die Prognosegüte über Reihen mit unterschiedlichen Skalen oder Nullwerten hinweg verglichen werden soll, eignet sich MASE (Hyndman & Koehler, 2006).
- Bei der Wahl zwischen statistischen und Machine-Learning-Verfahren legen die M4-Ergebnisse nahe, mit statistischen Verfahren und Kombinationen zu beginnen (Makridakis et al., 2018).

### Stärken und Grenzen

**Stärken**
- Klassische Modelle wie ETS und ARIMA sind gut verstanden und interpretierbar (Hyndman & Athanasopoulos, 2021).
- Kombinationen und hybride Verfahren schnitten in einem großen Wettbewerb am besten ab (Makridakis et al., 2018).
- LSTMs können weitreichende Abhängigkeiten erfassen (Hochreiter & Schmidhuber, 1997).

**Einschränkungen**
- Viele Modelle setzen Stationarität voraus, die geprüft und hergestellt werden muss (Dickey & Fuller, 1979).
- Gängige Genauigkeitsmaße können undefiniert oder irreführend sein (Hyndman & Koehler, 2006).
- Reine Machine-Learning-Verfahren schnitten im M4-Wettbewerb schlecht ab (Makridakis et al., 2018).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Exponentielle Glättung (ETS) | Gewichtete Mittel vergangener Beobachtungen mit Trend und Saisonalität (Hyndman & Athanasopoulos, 2021) | Reihen mit klarem Trend und klarer Saisonalität |
| ARIMA | Modelliert die Autokorrelation einer stationären (differenzierten) Reihe (Hyndman & Athanasopoulos, 2021) | Reihen mit Autokorrelationsstruktur |
| Hybride statistisch-neuronale Verfahren | Kombinieren statistische Modelle und neuronale Netze (Makridakis et al., 2018) | Große Sammlungen von Reihen |
| LSTM | Rekurrentes Netz mit gesteuerten Speicherzellen (Hochreiter & Schmidhuber, 1997) | Weitreichende Abhängigkeiten, große Datenmengen |

### In der Praxis

Daten werden in zeitlicher Reihenfolge aufgeteilt, nie zufällig, und Modelle werden mit Zeitreihen-Kreuzvalidierung gegen einfache Benchmarks wie die naive Prognose bewertet (Hyndman & Athanasopoulos, 2021; Hyndman & Koehler, 2006). Saisonale Muster lassen sich Regressionsmodellen auch als Merkmale mitgeben ([[feature-engineering|Feature Engineering]]).

### Merksatz

Zeitreihenanalyse erstellt Prognosen aus Trend, Saisonalität und Autokorrelation, bewertet sie streng auf späteren Daten, und einfache statistische Verfahren und Kombinationen sind schwer zu schlagen.

### Quellen

- Hyndman, R. J. & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3rd ed.). OTexts. [online edition](https://otexts.com/fpp3/)
- Dickey, D. A. & Fuller, W. A. (1979). *Distribution of the Estimators for Autoregressive Time Series with a Unit Root.* Journal of the American Statistical Association 74(366). [doi:10.1080/01621459.1979.10482531](https://doi.org/10.1080/01621459.1979.10482531)
- Hyndman, R. J. & Koehler, A. B. (2006). *Another look at measures of forecast accuracy.* International Journal of Forecasting 22(4). [doi:10.1016/j.ijforecast.2006.03.001](https://doi.org/10.1016/j.ijforecast.2006.03.001)
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2018). *The M4 Competition: Results, findings, conclusion and way forward.* International Journal of Forecasting 34(4). [doi:10.1016/j.ijforecast.2018.06.001](https://doi.org/10.1016/j.ijforecast.2018.06.001)
- Hochreiter, S. & Schmidhuber, J. (1997). *Long Short-Term Memory.* Neural Computation 9(8). [doi:10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735)
