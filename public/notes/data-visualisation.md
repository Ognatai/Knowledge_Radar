---
title_en: Data Visualisation
title_de: Datenvisualisierung
entity_type: Method
aliases:
- Data visualisation
- Data visualization
- Information visualisation
- Grammar of graphics
- Dashboards
- Datenvisualisierung
sources:
- https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf
- https://vita.had.co.nz/papers/layered-grammar.pdf
- https://arxiv.org/abs/2212.10533
- https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Data visualisation turns data into graphics so that people can see patterns, compare values and find details. Three ideas guide good charts and dashboards. A grammar of graphics describes any chart as data mapped to visual properties, drawn with geometric objects in layers, with scales, a coordinate system and facets, which is how libraries such as ggplot2 work (Wickham, 2010). Perception research ranks visual encodings by how accurately people read them, with position on a common scale best and length, angle and volume progressively worse, although individuals deviate from the average ranking (Davis et al., 2022). For interactive tools, Shneiderman's mantra "overview first, zoom and filter, then details-on-demand" structures the interaction (Shneiderman, 1996). Accessible charts never rely on colour alone ([[w3c|W3C]], 2023).

### How it works

```text
question and audience
 ▼
data: tidy table, aggregated at the right grain
 ▼
encoding: map variables to position, length, angle, area, colour, shape (best-read channels for the key comparison)
 ▼
grammar: layers (geom + stat + position) · scales · coordinate system · facets
 ▼
interaction (dashboards): overview → zoom and filter → details on demand
 ▼
accessibility check: not colour alone, labels, contrast
```

#### 1. The grammar of graphics

"A grammar of graphics is a tool that enables us to concisely describe the components of a graphic", moving beyond named chart types such as the scatterplot to the structure underneath (Wickham, 2010). In Wickham's layered grammar, building on Wilkinson's, a plot consists of a default dataset and mappings from variables to aesthetics; one or more layers, each with one geometric object (points, lines, bars), one statistical transformation (for example binning or smoothing) and one position adjustment; one scale per aesthetic; a coordinate system; and a facet specification that splits the data into small multiples (Wickham, 2010). Because the components are independent, a bar chart becomes a pie chart by changing only the coordinate system, and a scatterplot gains a trend line by adding a layer. ggplot2 for R implements this grammar; declarative chart libraries in Python and JavaScript follow similar ideas.

#### 2. Choosing encodings

Cleveland and McGill's graphical perception experiments ranked visual encodings by how accurately people judge numerical values: position is most accurate, followed by length, angle and then volume (Davis et al., 2022). The practical rule is to show the most important comparison with position on a common scale, as in bar charts, dot plots or line charts, and to use angle (pie charts), area or colour intensity only for secondary information. A replication with Bayesian multilevel models found that some individuals credibly depart from this ranking, which is based on an "average observer"; population averages can hide that variation (Davis et al., 2022).

#### 3. Interaction: overview, zoom and filter, details on demand

Shneiderman (1996) summarises interactive visualisation in the Visual Information-Seeking Mantra, "overview first, zoom and filter, then details-on-demand", and a taxonomy of seven tasks: overview of the whole collection, zoom on items of interest, filter out uninteresting items, details-on-demand for a selected item or group, relate items to each other, history of actions for undo and replay, and extract sub-collections and query parameters. The tasks apply to seven data types: one-, two- and three-dimensional data, temporal data, multi-dimensional data, trees and networks (Shneiderman, 1996). Dashboards follow the mantra when they show a few key figures first and let users drill down. Network data is visualised in the graph view of this site, see [[knowledge-graphs|knowledge graphs]].

#### 4. Accessibility

WCAG success criterion 1.4.1 requires that "color is not used as the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element", because people with colour vision deficiencies may not see the difference (W3C, 2023). In charts, series and categories distinguished by colour are therefore also labelled directly, numbered with a legend or given patterns; a lightness difference with a contrast ratio of at least 3:1 can count as an additional visual distinction (W3C, 2023).

#### Origin and variants

Shneiderman's taxonomy (1996) came from information visualisation for user interfaces; Wilkinson's grammar of graphics and Wickham's layered version (2010) from statistical graphics; Cleveland and McGill's perception experiments (1984) from statistics, with recent replications refining them (Davis et al., 2022). Visualising model internals and explanations is covered in [[explainable-ai|explainable AI]], visualising high-dimensional data in [[principal-component-analysis|principal component analysis]].

### When to use it

- Exploring data before modelling, to find distributions, outliers and relationships ([[statistics-fundamentals|statistics fundamentals]]).
- Communicating results to stakeholders who need the key comparison at a glance (Davis et al., 2022).
- Building dashboards for monitoring business or model metrics, where overview and drill-down matter (Shneiderman, 1996), see [[monitoring-and-alerting|monitoring and alerting]].

### Strengths and limitations

**Strengths**
- A grammar makes charts composable and reproducible in code (Wickham, 2010).
- Encoding rankings give a principled basis for choosing chart types (Davis et al., 2022).
- The mantra gives a simple structure for interactive tools (Shneiderman, 1996).

**Limitations**
- Perception rankings describe average observers; individual readers differ (Davis et al., 2022).
- The seven tasks are high-level and need refinement for specific domains, as Shneiderman (1996) notes.
- Colour-only distinctions exclude readers with colour vision deficiencies (W3C, 2023).

### Comparison

| Encoding | Reading accuracy (Cleveland & McGill ranking) | Typical charts |
|---|---|---|
| Position on a common scale | highest | bar chart, dot plot, line chart, scatterplot |
| Length | high | bar chart without common baseline |
| Angle | medium | pie chart |
| Area / volume | low | bubble chart, treemap |

Source: Davis et al. (2022) summarising Cleveland and McGill.

### In practice

Dashboards are usually built on dimensional models in the warehouse ([[data-modelling|data modelling]]). Each chart should answer one question, with the key comparison encoded by position (Davis et al., 2022), and dashboards should offer an overview with drill-down rather than everything at once (Shneiderman, 1996). Charts are created in code with [[python|Python]] libraries or rendered interactively in web frontends ([[frontend-development|frontend development]]).

### Key takeaway

Good data visualisation maps the key comparison to the most accurately read encoding, builds charts compositionally from a grammar of layers, scales and coordinates, structures interaction as overview, zoom and filter, details on demand, and never relies on colour alone.

### Sources

- Shneiderman, B. (1996). *The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations.* Proceedings of the IEEE Symposium on Visual Languages 1996. [cs.umd.edu](https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf)
- Wickham, H. (2010). *A Layered Grammar of Graphics.* Journal of Computational and Graphical Statistics 19(1), 3–28. [vita.had.co.nz](https://vita.had.co.nz/papers/layered-grammar.pdf)
- Davis, R., Pu, X., Ding, Y., Hall, B. D., Bonilla, K., Feng, M., Kay, M. & Harrison, L. (2022). *The Risks of Ranking: Revisiting Graphical Perception to Model Individual Differences in Visualization Performance.* IEEE Transactions on Visualization and Computer Graphics. [arXiv](https://arxiv.org/abs/2212.10533)
- W3C (2023). *Understanding Success Criterion 1.4.1: Use of Color.* WCAG 2.2. [w3.org](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Datenvisualisierung macht aus Daten Grafiken, damit Menschen Muster sehen, Werte vergleichen und Details finden können. Drei Ideen leiten gute Diagramme und Dashboards. Eine Grammar of Graphics beschreibt jedes Diagramm als Daten, die visuellen Eigenschaften zugeordnet und mit geometrischen Objekten in Schichten gezeichnet werden, mit Skalen, einem Koordinatensystem und Facetten; so arbeiten Bibliotheken wie ggplot2 (Wickham, 2010). Die Wahrnehmungsforschung ordnet visuelle Kodierungen danach, wie genau Menschen sie ablesen: Position auf einer gemeinsamen Skala am besten, Länge, Winkel und Volumen zunehmend schlechter, wobei Einzelne von der durchschnittlichen Rangfolge abweichen (Davis et al., 2022). Für interaktive Werkzeuge strukturiert Shneidermans Mantra „overview first, zoom and filter, then details-on-demand“ die Interaktion (Shneiderman, 1996). Barrierefreie Diagramme verlassen sich nie allein auf Farbe ([[w3c|W3C]], 2023).

### Funktionsweise

```text
Frage und Zielgruppe
 ▼
Daten: aufgeräumte Tabelle, in passender Granularität aggregiert
 ▼
Kodierung: Variablen auf Position, Länge, Winkel, Fläche, Farbe, Form abbilden (die genauesten Kanäle für den wichtigsten Vergleich)
 ▼
Grammatik: Schichten (Geom + Stat + Position) · Skalen · Koordinatensystem · Facetten
 ▼
Interaktion (Dashboards): Überblick → Zoomen und Filtern → Details bei Bedarf
 ▼
Barrierefreiheit prüfen: nicht nur Farbe, Beschriftungen, Kontrast
```

#### 1. Die Grammar of Graphics

„A grammar of graphics is a tool that enables us to concisely describe the components of a graphic“ und führt von benannten Diagrammtypen wie dem Streudiagramm zur darunterliegenden Struktur (Wickham, 2010). In Wickhams geschichteter Grammatik, die auf Wilkinsons aufbaut, besteht ein Diagramm aus einem Standarddatensatz und Zuordnungen von Variablen zu Ästhetiken; einer oder mehreren Schichten mit jeweils einem geometrischen Objekt (Punkte, Linien, Balken), einer statistischen Transformation (etwa Klassenbildung oder Glättung) und einer Positionsanpassung; einer Skala je Ästhetik; einem Koordinatensystem; und einer Facettenangabe, die die Daten in Small Multiples aufteilt (Wickham, 2010). Weil die Bestandteile unabhängig sind, wird aus einem Balkendiagramm ein Tortendiagramm, indem nur das Koordinatensystem geändert wird, und ein Streudiagramm erhält eine Trendlinie durch eine zusätzliche Schicht. ggplot2 für R setzt diese Grammatik um; deklarative Diagrammbibliotheken in Python und JavaScript folgen ähnlichen Ideen.

#### 2. Kodierungen wählen

Die Experimente von Cleveland und McGill zur grafischen Wahrnehmung ordneten visuelle Kodierungen danach, wie genau Menschen Zahlenwerte beurteilen: Position am genauesten, gefolgt von Länge, Winkel und dann Volumen (Davis et al., 2022). Die praktische Regel lautet, den wichtigsten Vergleich über Position auf einer gemeinsamen Skala zu zeigen, wie in Balken-, Punkt- oder Liniendiagrammen, und Winkel (Tortendiagramme), Fläche oder Farbintensität nur für Nebeninformationen zu nutzen. Eine Replikation mit bayesschen Mehrebenenmodellen fand, dass einzelne Personen glaubhaft von dieser Rangfolge abweichen, die auf einem „average observer“ beruht; Durchschnittswerte einer Population können diese Unterschiede verdecken (Davis et al., 2022).

#### 3. Interaktion: Überblick, Zoomen und Filtern, Details bei Bedarf

Shneiderman (1996) fasst interaktive Visualisierung im Visual Information-Seeking Mantra zusammen, „overview first, zoom and filter, then details-on-demand“, und in einer Taxonomie aus sieben Aufgaben: Überblick über die gesamte Sammlung, Zoomen auf interessante Elemente, Herausfiltern uninteressanter Elemente, Details bei Bedarf zu einem ausgewählten Element oder einer Gruppe, Beziehungen zwischen Elementen zeigen, Verlauf der Aktionen für Rückgängig-Machen und Wiederholen sowie Extrahieren von Teilmengen und Abfrageparametern. Die Aufgaben gelten für sieben Datentypen: ein-, zwei- und dreidimensionale Daten, zeitliche Daten, mehrdimensionale Daten, Bäume und Netzwerke (Shneiderman, 1996). Dashboards folgen dem Mantra, wenn sie zuerst wenige Kennzahlen zeigen und dann das Hineinzoomen erlauben. Netzwerkdaten werden in der Graphansicht dieser Seite dargestellt, siehe [[knowledge-graphs|Knowledge Graphs]].

#### 4. Barrierefreiheit

Das WCAG-Erfolgskriterium 1.4.1 verlangt, dass „color is not used as the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element“, weil Menschen mit Farbsehschwäche den Unterschied womöglich nicht sehen (W3C, 2023). In Diagrammen werden farblich unterschiedene Reihen und Kategorien daher zusätzlich direkt beschriftet, mit Legende nummeriert oder mit Mustern versehen; ein Helligkeitsunterschied mit einem Kontrastverhältnis von mindestens 3:1 kann als zusätzliche visuelle Unterscheidung gelten (W3C, 2023).

#### Herkunft und Varianten

Shneidermans Taxonomie (1996) stammt aus der Informationsvisualisierung für Benutzeroberflächen, Wilkinsons Grammar of Graphics und Wickhams geschichtete Fassung (2010) aus der statistischen Grafik, die Wahrnehmungsexperimente von Cleveland und McGill (1984) aus der Statistik, verfeinert durch neuere Replikationen (Davis et al., 2022). Die Visualisierung von Modellinterna und Erklärungen behandelt [[explainable-ai|Explainable AI]], die Visualisierung hochdimensionaler Daten [[principal-component-analysis|Hauptkomponentenanalyse]].

### Wann einsetzen

- Daten vor der Modellierung erkunden, um Verteilungen, Ausreißer und Zusammenhänge zu finden ([[statistics-fundamentals|Statistik-Grundlagen]]).
- Ergebnisse für Beteiligte darstellen, die den wichtigsten Vergleich auf einen Blick brauchen (Davis et al., 2022).
- Dashboards zur Überwachung von Geschäfts- oder Modellkennzahlen bauen, bei denen Überblick und Drill-down zählen (Shneiderman, 1996), siehe [[monitoring-and-alerting|Monitoring und Alerting]].

### Stärken und Grenzen

**Stärken**
- Eine Grammatik macht Diagramme im Code zusammensetzbar und reproduzierbar (Wickham, 2010).
- Rangfolgen von Kodierungen geben eine begründete Grundlage für die Wahl des Diagrammtyps (Davis et al., 2022).
- Das Mantra gibt interaktiven Werkzeugen eine einfache Struktur (Shneiderman, 1996).

**Grenzen**
- Wahrnehmungsrangfolgen beschreiben durchschnittliche Betrachtende; einzelne Lesende unterscheiden sich (Davis et al., 2022).
- Die sieben Aufgaben sind sehr allgemein und müssen für bestimmte Domänen verfeinert werden, wie Shneiderman (1996) anmerkt.
- Unterscheidungen allein über Farbe schließen Lesende mit Farbsehschwäche aus (W3C, 2023).

### Vergleich

| Kodierung | Ablesegenauigkeit (Rangfolge nach Cleveland & McGill) | Typische Diagramme |
|---|---|---|
| Position auf gemeinsamer Skala | am höchsten | Balken-, Punkt-, Linien-, Streudiagramm |
| Länge | hoch | Balkendiagramm ohne gemeinsame Grundlinie |
| Winkel | mittel | Tortendiagramm |
| Fläche / Volumen | niedrig | Blasendiagramm, Treemap |

Quelle: Davis et al. (2022) mit Zusammenfassung von Cleveland und McGill.

### In der Praxis

Dashboards entstehen meist auf dimensionalen Modellen im Warehouse ([[data-modelling|Datenmodellierung]]). Jedes Diagramm sollte eine Frage beantworten, mit dem wichtigsten Vergleich über Position kodiert (Davis et al., 2022), und Dashboards sollten einen Überblick mit Drill-down bieten statt alles auf einmal (Shneiderman, 1996). Diagramme entstehen im Code mit [[python|Python]]-Bibliotheken oder werden interaktiv in Web-Frontends gezeichnet ([[frontend-development|Frontend-Entwicklung]]).

### Merksatz

Gute Datenvisualisierung bildet den wichtigsten Vergleich auf die am genauesten ablesbare Kodierung ab, setzt Diagramme aus einer Grammatik von Schichten, Skalen und Koordinaten zusammen, gliedert Interaktion in Überblick, Zoomen und Filtern und Details bei Bedarf und verlässt sich nie allein auf Farbe.

### Quellen

- Shneiderman, B. (1996). *The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations.* Proceedings of the IEEE Symposium on Visual Languages 1996. [cs.umd.edu](https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf)
- Wickham, H. (2010). *A Layered Grammar of Graphics.* Journal of Computational and Graphical Statistics 19(1), 3–28. [vita.had.co.nz](https://vita.had.co.nz/papers/layered-grammar.pdf)
- Davis, R., Pu, X., Ding, Y., Hall, B. D., Bonilla, K., Feng, M., Kay, M. & Harrison, L. (2022). *The Risks of Ranking: Revisiting Graphical Perception to Model Individual Differences in Visualization Performance.* IEEE Transactions on Visualization and Computer Graphics. [arXiv](https://arxiv.org/abs/2212.10533)
- W3C (2023). *Understanding Success Criterion 1.4.1: Use of Color.* WCAG 2.2. [w3.org](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)
