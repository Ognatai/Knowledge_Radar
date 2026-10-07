---
title_en: Knowledge Graph Engineering
title_de: Knowledge Graph Engineering
entity_type: Method
sources:
- https://arxiv.org/abs/2003.02320
- https://www.w3.org/TR/shacl/
- https://arxiv.org/abs/1905.06397
- https://doi.org/10.3233/SW-160218
- https://doi.org/10.3233/SW-150175
- https://www.w3.org/TR/prov-o/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Knowledge graph engineering is the practice of building and operating knowledge graphs as reliable data products: pipelines create and enrich the graph, entity resolution merges duplicate descriptions, validation checks the data against shapes, refinement completes and corrects it, and provenance records where each fact came from (Hogan et al., 2020). Key tools are SHACL for validation (W3C SHACL), entity resolution workflows (Christophides et al., 2019), quality dimensions and metrics (Zaveri et al., 2016) and PROV-O for provenance (W3C PROV-O).

### How it works

Source data passes through extraction and mapping into the graph, duplicate entities are resolved, the result is validated and quality-checked, errors and gaps are refined, and every change is versioned and documented with provenance before the graph is published.

```text
1. From modelling to pipeline
▼
2. Entity resolution
▼
3. Validation with shapes
▼
4. Quality assessment
▼
5. Refinement: completion and error detection
▼
6. Provenance and versioning
```

#### 1. From modelling to pipeline

Hogan et al. (2020) summarise the life cycle of knowledge graphs: creation from text, structured data and other sources, enrichment, quality assessment, refinement and publication. A schema or ontology governs which types and relations are allowed ([[ontology-design|Ontology Design]]), and the pipeline that populates the graph is treated like any other data pipeline, with automated, repeatable steps.

#### 2. Entity resolution

Entity resolution identifies different descriptions that refer to the same real-world entity and is one of the most important tasks for data quality (Christophides et al., 2019). Modern workflows handle loosely structured, diverse, fast-changing and large collections of entity descriptions through blocking or indexing, which limits the candidate pairs, followed by matching and clustering; the database, semantic web and machine learning communities have proposed different methods for these steps.

#### 3. Validation with shapes

SHACL validates RDF graphs against shapes, which state for targeted nodes which properties are required, how often they may occur, which datatypes or classes their values must have and which patterns they must follow (W3C SHACL). A SHACL processor produces a validation report listing every violation, so validation can run automatically after each pipeline run. Unlike OWL reasoning, SHACL checks the data as it is, under a closed-world view.

#### 4. Quality assessment

Zaveri et al. (2016) reviewed quality assessment for Linked Data, whose quality ranges from carefully curated to crowdsourced and automatically extracted data of low quality. They unified the terminology and identified 18 quality dimensions, such as completeness, accuracy, consistency and timeliness, with 69 metrics, and analysed 30 core approaches and 12 tools.

#### 5. Refinement: completion and error detection

Knowledge graphs such as DBpedia, YAGO and Freebase are never complete or fully correct (Paulheim, 2017). Refinement methods either add missing knowledge, such as missing types or relations, or detect erroneous facts, using information within the graph or external sources. Their evaluation uses partial gold standards, retrospective human evaluation or the graph itself, and these choices affect how comparable results are.

#### 6. Provenance and versioning

PROV-O describes provenance with entities, the activities that used or generated them and the agents responsible, connected by relations such as wasGeneratedBy, used, wasDerivedFrom and wasAttributedTo (W3C PROV-O). Recording which source and which pipeline version produced each fact makes the graph traceable and allows changes to be rolled back.

#### Origin and variants

Hogan et al. (2020) frame the knowledge graph life cycle; entity resolution (Christophides et al., 2019), linked data quality (Zaveri et al., 2016) and refinement (Paulheim, 2017) are established research areas, and SHACL (W3C SHACL) and PROV-O (W3C PROV-O) are the corresponding W3C standards.

### When to use it

- When a knowledge graph is used in production and must stay correct as sources change (Hogan et al., 2020).
- When data from several sources describes the same entities and must be merged (Christophides et al., 2019).
- When downstream applications, such as GraphRAG, depend on the graph's correctness ([[graphrag|GraphRAG]]).

### Strengths and limitations

**Strengths**
- Shapes make data requirements explicit and automatically checkable (W3C SHACL).
- A shared set of quality dimensions and metrics makes quality measurable (Zaveri et al., 2016).
- Provenance makes every fact traceable to its source (W3C PROV-O).

**Limitations**
- Knowledge graphs are never complete or fully correct (Paulheim, 2017).
- Entity resolution at scale must handle diverse, fast-changing and loosely structured descriptions (Christophides et al., 2019).
- Evaluating refinement methods is difficult and depends on the gold standard used (Paulheim, 2017).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| SHACL validation | Closed-world checks of data against shapes (W3C SHACL) | Enforcing required structure |
| OWL reasoning | Open-world inference of implicit facts ([[ontology-design|Ontology Design]]) | Deriving knowledge, consistency checks |
| Entity resolution | Merges descriptions of the same entity (Christophides et al., 2019) | Integrating sources |
| Refinement | Completes missing facts or detects errors (Paulheim, 2017) | Improving an existing graph |

### In practice

Graph pipelines are versioned, tested and monitored like other data and ML pipelines ([[mlops-and-deployment|MLOps and Deployment]]): SHACL validation and quality metrics run after each update, and failures block publication (W3C SHACL; Zaveri et al., 2016). Incremental updates are preferred for large graphs, with a full rebuild when the schema changes.

### Key takeaway

Knowledge graph engineering keeps a graph trustworthy over time through repeatable pipelines, entity resolution, shape validation, quality metrics and provenance.

### Sources

- Hogan, A. et al. (2020). *Knowledge Graphs.* ACM Computing Surveys 2021. [arXiv:2003.02320](https://arxiv.org/abs/2003.02320)
- W3C (2017). *Shapes Constraint Language (SHACL).* W3C Recommendation. [w3.org](https://www.w3.org/TR/shacl/)
- Christophides, V. et al. (2019). *End-to-End Entity Resolution for Big Data: A Survey.* ACM Computing Surveys 2021. [arXiv:1905.06397](https://arxiv.org/abs/1905.06397)
- Paulheim, H. (2017). *Knowledge graph refinement: A survey of approaches and evaluation methods.* Semantic Web 8(3). [doi:10.3233/SW-160218](https://doi.org/10.3233/SW-160218)
- Zaveri, A., Rula, A., Maurino, A., Pietrobon, R., Lehmann, J. & Auer, S. (2016). *Quality assessment for Linked Data: A Survey.* Semantic Web 7(1). [doi:10.3233/SW-150175](https://doi.org/10.3233/SW-150175)
- W3C (2013). *PROV-O: The PROV Ontology.* W3C Recommendation. [w3.org](https://www.w3.org/TR/prov-o/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Knowledge Graph Engineering bedeutet, Wissensgraphen als verlässliche Datenprodukte aufzubauen und zu betreiben: Pipelines erzeugen und reichern den Graphen an, Entity Resolution führt doppelte Beschreibungen zusammen, Validierung prüft die Daten gegen Shapes, Verfeinerung ergänzt und korrigiert sie, und Provenienzangaben halten fest, woher jeder Fakt stammt (Hogan et al., 2020). Wichtige Werkzeuge sind SHACL für die Validierung (W3C SHACL), Workflows für Entity Resolution (Christophides et al., 2019), Qualitätsdimensionen und -metriken (Zaveri et al., 2016) und PROV-O für Provenienz (W3C PROV-O).

### Funktionsweise

Quelldaten durchlaufen Extraktion und Abbildung in den Graphen, doppelte Entitäten werden aufgelöst, das Ergebnis wird validiert und auf Qualität geprüft, Fehler und Lücken werden verfeinert, und jede Änderung wird versioniert und mit Provenienz dokumentiert, bevor der Graph veröffentlicht wird.

```text
1. Von der Modellierung zur Pipeline
▼
2. Entity Resolution
▼
3. Validierung mit Shapes
▼
4. Qualitätsbewertung
▼
5. Verfeinerung: Vervollständigung und Fehlererkennung
▼
6. Provenienz und Versionierung
```

#### 1. Von der Modellierung zur Pipeline

Hogan et al. (2020) fassen den Lebenszyklus von Wissensgraphen zusammen: Aufbau aus Text, strukturierten Daten und anderen Quellen, Anreicherung, Qualitätsbewertung, Verfeinerung und Veröffentlichung. Ein Schema oder eine Ontologie legt fest, welche Typen und Beziehungen zulässig sind ([[ontology-design|Ontologie-Design]]), und die Pipeline, die den Graphen befüllt, wird wie jede andere Datenpipeline mit automatisierten, wiederholbaren Schritten behandelt.

#### 2. Entity Resolution

Entity Resolution erkennt unterschiedliche Beschreibungen, die sich auf dieselbe reale Entität beziehen, und ist eine der wichtigsten Aufgaben für die Datenqualität (Christophides et al., 2019). Moderne Workflows verarbeiten locker strukturierte, vielfältige, sich schnell ändernde und große Sammlungen von Entitätsbeschreibungen mit Blocking oder Indexierung, die die Kandidatenpaare begrenzen, gefolgt von Abgleich und Clustering; Datenbank-, Semantic-Web- und Machine-Learning-Community haben dafür unterschiedliche Verfahren vorgeschlagen.

#### 3. Validierung mit Shapes

SHACL validiert RDF-Graphen gegen Shapes, die für die betroffenen Knoten festlegen, welche Eigenschaften vorhanden sein müssen, wie oft sie vorkommen dürfen, welche Datentypen oder Klassen ihre Werte haben müssen und welchen Mustern sie folgen (W3C SHACL). Ein SHACL-Prozessor erzeugt einen Validierungsbericht mit jedem Verstoß, sodass die Validierung nach jedem Pipelinelauf automatisch laufen kann. Anders als das Schlussfolgern mit OWL prüft SHACL die Daten so, wie sie sind, unter einer Closed-World-Sicht.

#### 4. Qualitätsbewertung

Zaveri et al. (2016) werteten Verfahren zur Qualitätsbewertung von Linked Data aus, deren Qualität von sorgfältig kuratierten bis zu per Crowdsourcing gesammelten und automatisch extrahierten Daten geringer Qualität reicht. Sie vereinheitlichten die Begriffe und benannten 18 Qualitätsdimensionen wie Vollständigkeit, Korrektheit, Konsistenz und Aktualität mit 69 Metriken und analysierten 30 zentrale Verfahren und 12 Werkzeuge.

#### 5. Verfeinerung: Vervollständigung und Fehlererkennung

Wissensgraphen wie DBpedia, YAGO und Freebase sind nie vollständig oder völlig korrekt (Paulheim, 2017). Verfeinerungsverfahren ergänzen entweder fehlendes Wissen, etwa fehlende Typen oder Beziehungen, oder erkennen fehlerhafte Fakten, mithilfe von Information im Graphen selbst oder aus externen Quellen. Ihre Evaluation nutzt partielle Goldstandards, nachträgliche menschliche Bewertung oder den Graphen selbst, und diese Wahl beeinflusst, wie vergleichbar Ergebnisse sind.

#### 6. Provenienz und Versionierung

PROV-O beschreibt Provenienz mit Entitäten, den Aktivitäten, die sie genutzt oder erzeugt haben, und den verantwortlichen Akteuren, verbunden durch Beziehungen wie wasGeneratedBy, used, wasDerivedFrom und wasAttributedTo (W3C PROV-O). Wird festgehalten, welche Quelle und welche Pipelineversion einen Fakt erzeugt hat, bleibt der Graph nachvollziehbar, und Änderungen lassen sich zurücknehmen.

#### Ursprung und Varianten

Hogan et al. (2020) beschreiben den Lebenszyklus von Wissensgraphen; Entity Resolution (Christophides et al., 2019), Qualität von Linked Data (Zaveri et al., 2016) und Verfeinerung (Paulheim, 2017) sind etablierte Forschungsfelder, und SHACL (W3C SHACL) sowie PROV-O (W3C PROV-O) sind die zugehörigen W3C-Standards.

### Wann einsetzen

- Wenn ein Wissensgraph produktiv genutzt wird und bei sich ändernden Quellen korrekt bleiben muss (Hogan et al., 2020).
- Wenn Daten aus mehreren Quellen dieselben Entitäten beschreiben und zusammengeführt werden müssen (Christophides et al., 2019).
- Wenn nachgelagerte Anwendungen wie GraphRAG von der Korrektheit des Graphen abhängen ([[graphrag|GraphRAG]]).

### Stärken und Grenzen

**Stärken**
- Shapes machen Anforderungen an die Daten ausdrücklich und automatisch prüfbar (W3C SHACL).
- Gemeinsame Qualitätsdimensionen und -metriken machen Qualität messbar (Zaveri et al., 2016).
- Provenienz macht jeden Fakt bis zu seiner Quelle nachvollziehbar (W3C PROV-O).

**Einschränkungen**
- Wissensgraphen sind nie vollständig oder völlig korrekt (Paulheim, 2017).
- Entity Resolution im großen Maßstab muss vielfältige, sich schnell ändernde und locker strukturierte Beschreibungen bewältigen (Christophides et al., 2019).
- Verfeinerungsverfahren zu evaluieren ist schwierig und hängt vom verwendeten Goldstandard ab (Paulheim, 2017).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| SHACL-Validierung | Prüfung der Daten gegen Shapes unter Closed-World-Sicht (W3C SHACL) | Durchsetzen erforderlicher Strukturen |
| OWL-Schlussfolgern | Ableiten impliziter Fakten unter Open-World-Annahme ([[ontology-design|Ontologie-Design]]) | Wissen ableiten, Konsistenz prüfen |
| Entity Resolution | Führt Beschreibungen derselben Entität zusammen (Christophides et al., 2019) | Quellen integrieren |
| Verfeinerung | Ergänzt fehlende Fakten oder erkennt Fehler (Paulheim, 2017) | Bestehenden Graphen verbessern |

### In der Praxis

Graph-Pipelines werden wie andere Daten- und ML-Pipelines versioniert, getestet und überwacht ([[mlops-and-deployment|MLOps und Deployment]]): SHACL-Validierung und Qualitätsmetriken laufen nach jeder Aktualisierung, und Fehlschläge blockieren die Veröffentlichung (W3C SHACL; Zaveri et al., 2016). Bei großen Graphen werden inkrementelle Aktualisierungen bevorzugt, ein vollständiger Neuaufbau erfolgt bei Schemaänderungen.

### Merksatz

Knowledge Graph Engineering hält einen Graphen dauerhaft vertrauenswürdig, mit wiederholbaren Pipelines, Entity Resolution, Validierung gegen Shapes, Qualitätsmetriken und Provenienz.

### Quellen

- Hogan, A. et al. (2020). *Knowledge Graphs.* ACM Computing Surveys 2021. [arXiv:2003.02320](https://arxiv.org/abs/2003.02320)
- W3C (2017). *Shapes Constraint Language (SHACL).* W3C Recommendation. [w3.org](https://www.w3.org/TR/shacl/)
- Christophides, V. et al. (2019). *End-to-End Entity Resolution for Big Data: A Survey.* ACM Computing Surveys 2021. [arXiv:1905.06397](https://arxiv.org/abs/1905.06397)
- Paulheim, H. (2017). *Knowledge graph refinement: A survey of approaches and evaluation methods.* Semantic Web 8(3). [doi:10.3233/SW-160218](https://doi.org/10.3233/SW-160218)
- Zaveri, A., Rula, A., Maurino, A., Pietrobon, R., Lehmann, J. & Auer, S. (2016). *Quality assessment for Linked Data: A Survey.* Semantic Web 7(1). [doi:10.3233/SW-150175](https://doi.org/10.3233/SW-150175)
- W3C (2013). *PROV-O: The PROV Ontology.* W3C Recommendation. [w3.org](https://www.w3.org/TR/prov-o/)
