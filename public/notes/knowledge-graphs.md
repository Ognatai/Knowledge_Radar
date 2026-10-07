---
title_en: Knowledge Graphs
title_de: Wissensgraphen
entity_type: Concept
sources:
- https://arxiv.org/abs/2003.02320
- https://www.w3.org/TR/rdf11-concepts/
- https://www.w3.org/TR/owl2-primer/
- https://neo4j.com/docs/cypher-manual/current/introduction/
- https://arxiv.org/abs/2002.00388
- https://arxiv.org/abs/2306.08302
- https://arxiv.org/abs/2404.16130
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A knowledge graph represents knowledge as a graph of entities connected by typed relationships, so that facts from diverse, large-scale and changing sources can be integrated, queried and reasoned over (Hogan et al., 2020). Two data models dominate: RDF, where every fact is a subject-predicate-object triple with globally unique identifiers (W3C RDF 1.1 Concepts), and property graphs, where nodes and relationships carry key-value properties (Neo4j Cypher Manual). Ontologies add formal meaning (W3C OWL 2 Primer), and knowledge graphs increasingly complement large language models, for example in GraphRAG (Pan et al., 2023; Edge et al., 2024).

### How it works

Entities become nodes and facts become edges between them. A schema or ontology defines which types and relations exist, data is extracted or mapped from sources into the graph, and applications query it with graph query languages, reason over it or learn embeddings from it.

```text
1. Triples, entities and relations
▼
2. Data models: RDF and property graphs
▼
3. Schema and ontologies
▼
4. Building a knowledge graph
▼
5. Querying and reasoning
▼
6. Knowledge graphs and language models
```

#### 1. Triples, entities and relations

The basic unit of a knowledge graph is a fact connecting two entities by a relation, such as (Regulation, appliesTo, Company) (Hogan et al., 2020). Knowledge graphs are used where diverse, dynamic, large-scale collections of data must be exploited, and their graph structure makes it easy to add new entities and relations without redesigning a schema.

#### 2. Data models: RDF and property graphs

In RDF, information is a set of triples of subject, predicate and object; subjects and predicates are IRIs, while objects can also be literals such as strings or numbers. IRIs give resources globally unique names, so that graphs from different sources can be merged (W3C RDF 1.1 Concepts; [[rdf|RDF (Resource Description Framework)]]). In property graphs, nodes carry labels, relationships have exactly one type and a direction, and both nodes and relationships can carry properties as key-value pairs (Neo4j Cypher Manual; [[graph-databases|Graph Databases]]).

#### 3. Schema and ontologies

Hogan et al. (2020) discuss the roles of schema, identity and context in knowledge graphs. An ontology defines classes, properties and their relationships with formal meaning; with OWL, reasoners can derive implicit facts, for example from class hierarchies or transitive properties, and check consistency, under an open-world assumption in which missing information is not taken as false (W3C OWL 2 Primer; [[ontology-design|Ontology Design]]).

#### 4. Building a knowledge graph

Knowledge is represented and extracted with a combination of deductive techniques, such as rules and reasoning, and inductive techniques, such as machine learning (Hogan et al., 2020). Creation and enrichment draw on structured sources and on text via information extraction ([[information-extraction|Information Extraction]]); quality assessment, refinement and publication follow ([[knowledge-graph-engineering|Knowledge Graph Engineering]]).

#### 5. Querying and reasoning

Graph query languages match patterns of nodes and edges: Cypher, for example, writes patterns in an ASCII-art-like syntax such as (a:Person)-[:KNOWS]->(b:Person) (Neo4j Cypher Manual), and SPARQL matches triple patterns in RDF ([[sparql|SPARQL]]). Knowledge graph embeddings represent entities and relations as vectors for tasks such as predicting missing links, and knowledge acquisition and completion are core research topics (Ji et al., 2020; [[transe|TransE]]).

#### 6. Knowledge graphs and language models

Large language models are black boxes that often fall short in capturing and accessing factual knowledge, whereas knowledge graphs store facts explicitly but are hard to construct and keep up to date; Pan et al. (2023) outline three ways to combine them: knowledge-graph-enhanced LLMs, LLM-augmented knowledge graphs, and synergised systems. GraphRAG, for example, uses an LLM to build an entity knowledge graph from documents and answer questions over it (Edge et al., 2024; [[graphrag|GraphRAG]]).

#### Origin and variants

Hogan et al. (2020) give a comprehensive introduction to data models, query languages, schema, deductive and inductive knowledge, and the life cycle of knowledge graphs. RDF (W3C RDF 1.1 Concepts) and OWL (W3C OWL 2 Primer) are W3C standards, property graphs are popularised by graph databases such as Neo4j (Neo4j Cypher Manual), and Ji et al. (2020) and Pan et al. (2023) survey representation learning and the combination with LLMs.

### When to use it

- When data from many sources about the same entities must be integrated and connected (Hogan et al., 2020; W3C RDF 1.1 Concepts).
- When questions depend on relationships across several steps, such as which regulations apply to which company through which activity (Neo4j Cypher Manual).
- When an LLM application needs explicit, verifiable facts or answers over a whole document collection (Pan et al., 2023; Edge et al., 2024).

### Strengths and limitations

**Strengths**
- Flexible integration of diverse, changing data (Hogan et al., 2020).
- Explicit, inspectable facts that can be reasoned over with ontologies (W3C OWL 2 Primer).
- Complement LLMs with factual knowledge and interpretability (Pan et al., 2023).

**Limitations**
- Knowledge graphs are hard to construct and evolve constantly (Pan et al., 2023).
- They are incomplete; missing facts must be predicted or added (Ji et al., 2020).
- Schema, identity and quality need ongoing management (Hogan et al., 2020).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| RDF knowledge graph | Triples with global IRIs, W3C standards, ontology reasoning (W3C RDF 1.1 Concepts; W3C OWL 2 Primer) | Data integration and publication across organisations |
| Property graph | Labelled nodes and typed relationships with properties (Neo4j Cypher Manual) | Application databases with traversal-heavy queries |
| Relational database | Fixed tables and joins ([[sql|SQL]]) | Stable schemas and transactional data |
| Vector database | Similarity search over embeddings ([[vector-databases|Vector Databases]]) | Semantic search without explicit relations |

### In practice

A knowledge graph project starts with the questions it must answer and a schema or ontology, then builds pipelines to populate and validate the graph (Hogan et al., 2020; [[knowledge-graph-engineering|Knowledge Graph Engineering]]). In legal applications, for example, norms, cases and parties are modelled as entities with relations such as "cites" or "amends" ([[legal-ai|Legal AI]]).

### Key takeaway

Knowledge graphs store facts as entities and typed relations, which makes knowledge from many sources integrable, queryable and usable alongside language models.

### Sources

- Hogan, A. et al. (2020). *Knowledge Graphs.* ACM Computing Surveys 2021. [arXiv:2003.02320](https://arxiv.org/abs/2003.02320)
- W3C (2014). *RDF 1.1 Concepts and Abstract Syntax.* W3C Recommendation. [w3.org](https://www.w3.org/TR/rdf11-concepts/)
- W3C (2012). *OWL 2 Web Ontology Language Primer (Second Edition).* W3C Recommendation. [w3.org](https://www.w3.org/TR/owl2-primer/)
- Neo4j. *Cypher Manual: Introduction.* Neo4j documentation. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/introduction/)
- Ji, S. et al. (2020). *A Survey on Knowledge Graphs: Representation, Acquisition and Applications.* IEEE TNNLS 2022. [arXiv:2002.00388](https://arxiv.org/abs/2002.00388)
- Pan, S. et al. (2023). *Unifying Large Language Models and Knowledge Graphs: A Roadmap.* IEEE TKDE 2024. [arXiv:2306.08302](https://arxiv.org/abs/2306.08302)
- Edge, D. et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Wissensgraph stellt Wissen als Graph aus Entitäten dar, die durch typisierte Beziehungen verbunden sind, sodass sich Fakten aus vielfältigen, großen und sich ändernden Quellen zusammenführen, abfragen und für Schlussfolgerungen nutzen lassen (Hogan et al., 2020). Zwei Datenmodelle dominieren: RDF, in dem jeder Fakt ein Tripel aus Subjekt, Prädikat und Objekt mit global eindeutigen Bezeichnern ist (W3C RDF 1.1 Concepts), und Property Graphs, in denen Knoten und Kanten Schlüssel-Wert-Eigenschaften tragen (Neo4j Cypher Manual). Ontologien fügen formale Bedeutung hinzu (W3C OWL 2 Primer), und Wissensgraphen ergänzen zunehmend große Sprachmodelle, etwa in GraphRAG (Pan et al., 2023; Edge et al., 2024).

### Funktionsweise

Entitäten werden zu Knoten, Fakten zu Kanten zwischen ihnen. Ein Schema oder eine Ontologie legt fest, welche Typen und Beziehungen es gibt, Daten werden aus Quellen extrahiert oder in den Graphen abgebildet, und Anwendungen fragen ihn mit Graph-Abfragesprachen ab, ziehen Schlussfolgerungen oder lernen Embeddings daraus.

```text
1. Tripel, Entitäten und Beziehungen
▼
2. Datenmodelle: RDF und Property Graphs
▼
3. Schema und Ontologien
▼
4. Aufbau eines Wissensgraphen
▼
5. Abfragen und Schlussfolgern
▼
6. Wissensgraphen und Sprachmodelle
```

#### 1. Tripel, Entitäten und Beziehungen

Die Grundeinheit eines Wissensgraphen ist ein Fakt, der zwei Entitäten über eine Beziehung verbindet, etwa (Verordnung, giltFür, Unternehmen) (Hogan et al., 2020). Wissensgraphen werden dort eingesetzt, wo vielfältige, dynamische und große Datensammlungen genutzt werden müssen, und ihre Graphstruktur erlaubt es, neue Entitäten und Beziehungen hinzuzufügen, ohne ein Schema neu zu entwerfen.

#### 2. Datenmodelle: RDF und Property Graphs

In RDF ist Information eine Menge von Tripeln aus Subjekt, Prädikat und Objekt; Subjekte und Prädikate sind IRIs, Objekte können auch Literale wie Zeichenketten oder Zahlen sein. IRIs geben Ressourcen global eindeutige Namen, sodass sich Graphen aus verschiedenen Quellen zusammenführen lassen (W3C RDF 1.1 Concepts; [[rdf|RDF (Resource Description Framework)]]). In Property Graphs tragen Knoten Labels, Beziehungen haben genau einen Typ und eine Richtung, und sowohl Knoten als auch Beziehungen können Eigenschaften als Schlüssel-Wert-Paare tragen (Neo4j Cypher Manual; [[graph-databases|Graphdatenbanken]]).

#### 3. Schema und Ontologien

Hogan et al. (2020) behandeln die Rolle von Schema, Identität und Kontext in Wissensgraphen. Eine Ontologie definiert Klassen, Eigenschaften und ihre Beziehungen mit formaler Bedeutung; mit OWL können Reasoner implizite Fakten ableiten, etwa aus Klassenhierarchien oder transitiven Eigenschaften, und die Konsistenz prüfen, unter der Open-World-Annahme, nach der fehlende Information nicht als falsch gilt (W3C OWL 2 Primer; [[ontology-design|Ontologie-Design]]).

#### 4. Aufbau eines Wissensgraphen

Wissen wird mit einer Kombination aus deduktiven Techniken wie Regeln und Schlussfolgern und induktiven Techniken wie maschinellem Lernen dargestellt und extrahiert (Hogan et al., 2020). Aufbau und Anreicherung nutzen strukturierte Quellen und über Informationsextraktion auch Text ([[information-extraction|Informationsextraktion]]); es folgen Qualitätsbewertung, Verfeinerung und Veröffentlichung ([[knowledge-graph-engineering|Knowledge Graph Engineering]]).

#### 5. Abfragen und Schlussfolgern

Graph-Abfragesprachen suchen nach Mustern aus Knoten und Kanten: Cypher schreibt Muster etwa in einer ASCII-Art-ähnlichen Syntax wie (a:Person)-[:KNOWS]->(b:Person) (Neo4j Cypher Manual), und SPARQL sucht Tripelmuster in RDF ([[sparql|SPARQL]]). Knowledge Graph Embeddings stellen Entitäten und Beziehungen als Vektoren dar, etwa um fehlende Verbindungen vorherzusagen, und Wissenserwerb und -vervollständigung sind zentrale Forschungsthemen (Ji et al., 2020; [[transe|TransE]]).

#### 6. Wissensgraphen und Sprachmodelle

Große Sprachmodelle sind Black Boxes, die Faktenwissen oft nur unzureichend erfassen und abrufen, während Wissensgraphen Fakten ausdrücklich speichern, aber schwer aufzubauen und aktuell zu halten sind; Pan et al. (2023) skizzieren drei Arten der Kombination: durch Wissensgraphen verbesserte LLMs, durch LLMs erweiterte Wissensgraphen und synergetische Systeme. GraphRAG etwa nutzt ein LLM, um aus Dokumenten einen Entitäten-Wissensgraphen aufzubauen und Fragen darüber zu beantworten (Edge et al., 2024; [[graphrag|GraphRAG]]).

#### Ursprung und Varianten

Hogan et al. (2020) geben eine umfassende Einführung in Datenmodelle, Abfragesprachen, Schema, deduktives und induktives Wissen und den Lebenszyklus von Wissensgraphen. RDF (W3C RDF 1.1 Concepts) und OWL (W3C OWL 2 Primer) sind W3C-Standards, Property Graphs wurden durch Graphdatenbanken wie Neo4j verbreitet (Neo4j Cypher Manual), und Ji et al. (2020) sowie Pan et al. (2023) geben einen Überblick über Repräsentationslernen und die Kombination mit LLMs.

### Wann einsetzen

- Wenn Daten aus vielen Quellen über dieselben Entitäten zusammengeführt und verknüpft werden müssen (Hogan et al., 2020; W3C RDF 1.1 Concepts).
- Wenn Fragen von Beziehungen über mehrere Schritte abhängen, etwa welche Vorschriften über welche Tätigkeit für welches Unternehmen gelten (Neo4j Cypher Manual).
- Wenn eine LLM-Anwendung ausdrückliche, überprüfbare Fakten oder Antworten über eine ganze Dokumentsammlung braucht (Pan et al., 2023; Edge et al., 2024).

### Stärken und Grenzen

**Stärken**
- Flexible Zusammenführung vielfältiger, sich ändernder Daten (Hogan et al., 2020).
- Ausdrückliche, prüfbare Fakten, über die sich mit Ontologien schlussfolgern lässt (W3C OWL 2 Primer).
- Ergänzen LLMs um Faktenwissen und Nachvollziehbarkeit (Pan et al., 2023).

**Einschränkungen**
- Wissensgraphen sind schwer aufzubauen und verändern sich laufend (Pan et al., 2023).
- Sie sind unvollständig; fehlende Fakten müssen vorhergesagt oder ergänzt werden (Ji et al., 2020).
- Schema, Identität und Qualität erfordern fortlaufende Pflege (Hogan et al., 2020).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| RDF-Wissensgraph | Tripel mit globalen IRIs, W3C-Standards, Schlussfolgern mit Ontologien (W3C RDF 1.1 Concepts; W3C OWL 2 Primer) | Datenintegration und Veröffentlichung über Organisationen hinweg |
| Property Graph | Knoten mit Labels und typisierte Beziehungen mit Eigenschaften (Neo4j Cypher Manual) | Anwendungsdatenbanken mit vielen Traversierungen |
| Relationale Datenbank | Feste Tabellen und Joins ([[sql|SQL]]) | Stabile Schemata und Transaktionsdaten |
| Vektordatenbank | Ähnlichkeitssuche über Embeddings ([[vector-databases|Vektordatenbanken]]) | Semantische Suche ohne ausdrückliche Beziehungen |

### In der Praxis

Ein Wissensgraph-Projekt beginnt mit den Fragen, die der Graph beantworten soll, und einem Schema oder einer Ontologie und baut dann Pipelines, um den Graphen zu befüllen und zu validieren (Hogan et al., 2020; [[knowledge-graph-engineering|Knowledge Graph Engineering]]). In juristischen Anwendungen werden etwa Normen, Entscheidungen und Beteiligte als Entitäten mit Beziehungen wie „zitiert“ oder „ändert“ modelliert ([[legal-ai|Legal AI]]).

### Merksatz

Wissensgraphen speichern Fakten als Entitäten und typisierte Beziehungen und machen Wissen aus vielen Quellen so zusammenführbar, abfragbar und gemeinsam mit Sprachmodellen nutzbar.

### Quellen

- Hogan, A. et al. (2020). *Knowledge Graphs.* ACM Computing Surveys 2021. [arXiv:2003.02320](https://arxiv.org/abs/2003.02320)
- W3C (2014). *RDF 1.1 Concepts and Abstract Syntax.* W3C Recommendation. [w3.org](https://www.w3.org/TR/rdf11-concepts/)
- W3C (2012). *OWL 2 Web Ontology Language Primer (Second Edition).* W3C Recommendation. [w3.org](https://www.w3.org/TR/owl2-primer/)
- Neo4j. *Cypher Manual: Introduction.* Neo4j documentation. [neo4j.com](https://neo4j.com/docs/cypher-manual/current/introduction/)
- Ji, S. et al. (2020). *A Survey on Knowledge Graphs: Representation, Acquisition and Applications.* IEEE TNNLS 2022. [arXiv:2002.00388](https://arxiv.org/abs/2002.00388)
- Pan, S. et al. (2023). *Unifying Large Language Models and Knowledge Graphs: A Roadmap.* IEEE TKDE 2024. [arXiv:2306.08302](https://arxiv.org/abs/2306.08302)
- Edge, D. et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)
