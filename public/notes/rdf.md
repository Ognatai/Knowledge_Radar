---
title_en: RDF (Resource Description Framework)
title_de: RDF (Resource Description Framework)
entity_type: Technology
sources:
- https://www.w3.org/TR/rdf11-concepts/
- https://www.w3.org/TR/turtle/
- https://www.w3.org/TR/rdf11-primer/
- https://www.w3.org/TR/rdf-schema/
- https://www.w3.org/TR/json-ld11/
- https://www.w3.org/TR/owl2-primer/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

RDF (Resource Description Framework) is the W3C data model for knowledge graphs: every statement is a triple of subject, predicate and object, and resources are named with globally unique IRIs, so data from different sources can be merged (W3C RDF 1.1 Concepts). RDF graphs are written in formats such as Turtle, JSON-LD or N-Triples (W3C Turtle; W3C JSON-LD 1.1; W3C RDF 1.1 Primer), described with vocabularies from RDF Schema and OWL (W3C RDF Schema 1.1; W3C OWL 2 Primer), and queried with SPARQL ([[sparql|SPARQL]]).

### Core concepts

- **Triples:** Subject and predicate are IRIs (the subject may also be a blank node); the object is an IRI, a literal such as a string, number or date with a datatype or language tag, or a blank node, which denotes a resource without a global name (W3C RDF 1.1 Concepts).
- **Graphs and datasets:** A set of triples is an RDF graph; an RDF dataset groups a default graph and named graphs identified by IRIs, which can record, for example, the source of a group of statements (W3C RDF 1.1 Concepts).
- **Turtle:** Prefixes abbreviate IRIs, a semicolon repeats the subject, a comma repeats subject and predicate, and the keyword a stands for rdf:type (W3C Turtle).
- **Serialisations:** Turtle and TriG (with named graphs), N-Triples and N-Quads (one statement per line), JSON-LD and RDF/XML express the same data model (W3C RDF 1.1 Primer; W3C JSON-LD 1.1).
- **Vocabularies:** RDF Schema defines classes, subclasses, domain and range (W3C RDF Schema 1.1); OWL adds richer axioms for reasoning (W3C OWL 2 Primer); common vocabularies include FOAF, Dublin Core, schema.org and SKOS (W3C RDF 1.1 Primer).
- **Reification:** The RDF Schema vocabulary rdf:Statement, rdf:subject, rdf:predicate and rdf:object describes a triple as a resource, so that statements can be made about statements (W3C RDF Schema 1.1).

### Common usage

```turtle
@prefix ex:   <http://example.org/legal#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

ex:Decision a rdfs:Class .
ex:cites rdfs:domain ex:Decision ;
         rdfs:range  ex:Norm .

ex:Case123 a ex:Decision ;
    rdfs:label "Judgment of 12 March 2024"@en ;
    ex:date "2024-03-12"^^xsd:date ;
    ex:cites ex:GDPR_Art6, ex:GDPR_Art17 .
```

The same data in JSON-LD uses a @context that maps JSON keys to IRIs, with @id for the node's identifier and @type for its class, so web developers can work with familiar JSON (W3C JSON-LD 1.1).

### When to use it

- When data from several organisations or sources must be integrated with stable, global identifiers (W3C RDF 1.1 Concepts).
- When data should be published as linked data and reused with standard vocabularies (W3C RDF 1.1 Primer).
- When an application mainly needs fast traversal inside one database, a property graph may be simpler ([[graph-databases|Graph Databases]]).

### Strengths and limitations

**Strengths**
- Global IRIs make merging graphs from different sources straightforward (W3C RDF 1.1 Concepts).
- One data model with several serialisations, including JSON-LD for web developers (W3C RDF 1.1 Primer; W3C JSON-LD 1.1).
- Standard vocabularies and OWL reasoning add shared meaning (W3C RDF Schema 1.1; W3C OWL 2 Primer).

**Limitations**
- Statements about statements need reification or named graphs, which makes data more verbose (W3C RDF Schema 1.1; W3C RDF 1.1 Concepts).
- Blank nodes have no global name, which complicates merging and comparison (W3C RDF 1.1 Concepts).
- Formal OWL semantics follow the open-world assumption, which differs from database intuitions (W3C OWL 2 Primer).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Turtle | Compact, human-readable triples (W3C Turtle) | Writing and reading RDF by hand |
| JSON-LD | JSON with a context that maps keys to IRIs (W3C JSON-LD 1.1) | Web APIs and structured data on websites |
| N-Triples / N-Quads | One statement per line (W3C RDF 1.1 Primer) | Bulk loading and streaming |
| Property graphs | Nodes and relationships with key-value properties ([[graph-databases|Graph Databases]]) | Database-internal graph applications |

### In practice

RDF data is modelled against an ontology ([[ontology-design|Ontology Design]]), validated with shapes and stored in a triple store, with named graphs recording the source of each part of the data ([[knowledge-graph-engineering|Knowledge Graph Engineering]]). Reusing established vocabularies instead of inventing new terms makes data easier to integrate (W3C RDF 1.1 Primer).

### Key takeaway

RDF expresses knowledge as triples with global identifiers, which makes graphs from different sources mergeable and gives them shared meaning through standard vocabularies.

### Sources

- W3C (2014). *RDF 1.1 Concepts and Abstract Syntax.* W3C Recommendation. [w3.org](https://www.w3.org/TR/rdf11-concepts/)
- W3C (2014). *RDF 1.1 Turtle: Terse RDF Triple Language.* W3C Recommendation. [w3.org](https://www.w3.org/TR/turtle/)
- W3C (2014). *RDF 1.1 Primer.* W3C Working Group Note. [w3.org](https://www.w3.org/TR/rdf11-primer/)
- W3C (2014). *RDF Schema 1.1.* W3C Recommendation. [w3.org](https://www.w3.org/TR/rdf-schema/)
- W3C (2020). *JSON-LD 1.1: A JSON-based Serialization for Linked Data.* W3C Recommendation. [w3.org](https://www.w3.org/TR/json-ld11/)
- W3C (2012). *OWL 2 Web Ontology Language Primer (Second Edition).* W3C Recommendation. [w3.org](https://www.w3.org/TR/owl2-primer/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

RDF (Resource Description Framework) ist das W3C-Datenmodell für Wissensgraphen: Jede Aussage ist ein Tripel aus Subjekt, Prädikat und Objekt, und Ressourcen werden mit global eindeutigen IRIs benannt, sodass sich Daten aus verschiedenen Quellen zusammenführen lassen (W3C RDF 1.1 Concepts). RDF-Graphen werden in Formaten wie Turtle, JSON-LD oder N-Triples geschrieben (W3C Turtle; W3C JSON-LD 1.1; W3C RDF 1.1 Primer), mit Vokabularen aus RDF Schema und OWL beschrieben (W3C RDF Schema 1.1; W3C OWL 2 Primer) und mit SPARQL abgefragt ([[sparql|SPARQL]]).

### Kernkonzepte

- **Tripel:** Subjekt und Prädikat sind IRIs (das Subjekt kann auch ein Blank Node sein); das Objekt ist eine IRI, ein Literal wie eine Zeichenkette, Zahl oder ein Datum mit Datentyp oder Sprachkennung, oder ein Blank Node, der eine Ressource ohne globalen Namen bezeichnet (W3C RDF 1.1 Concepts).
- **Graphen und Datasets:** Eine Menge von Tripeln ist ein RDF-Graph; ein RDF-Dataset fasst einen Standardgraphen und benannte Graphen (Named Graphs) mit IRIs zusammen, die etwa die Quelle einer Gruppe von Aussagen festhalten können (W3C RDF 1.1 Concepts).
- **Turtle:** Präfixe kürzen IRIs ab, ein Semikolon wiederholt das Subjekt, ein Komma Subjekt und Prädikat, und das Schlüsselwort a steht für rdf:type (W3C Turtle).
- **Serialisierungen:** Turtle und TriG (mit Named Graphs), N-Triples und N-Quads (eine Aussage je Zeile), JSON-LD und RDF/XML drücken dasselbe Datenmodell aus (W3C RDF 1.1 Primer; W3C JSON-LD 1.1).
- **Vokabulare:** RDF Schema definiert Klassen, Unterklassen, Domain und Range (W3C RDF Schema 1.1); OWL ergänzt reichhaltigere Axiome für das Schlussfolgern (W3C OWL 2 Primer); verbreitete Vokabulare sind FOAF, Dublin Core, schema.org und SKOS (W3C RDF 1.1 Primer).
- **Reifikation:** Das RDF-Schema-Vokabular rdf:Statement, rdf:subject, rdf:predicate und rdf:object beschreibt ein Tripel als Ressource, sodass Aussagen über Aussagen möglich werden (W3C RDF Schema 1.1).

### Typische Verwendung

```turtle
@prefix ex:   <http://example.org/legal#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

ex:Decision a rdfs:Class .
ex:cites rdfs:domain ex:Decision ;
         rdfs:range  ex:Norm .

ex:Case123 a ex:Decision ;
    rdfs:label "Urteil vom 12. März 2024"@de ;
    ex:date "2024-03-12"^^xsd:date ;
    ex:cites ex:GDPR_Art6, ex:GDPR_Art17 .
```

Dieselben Daten in JSON-LD nutzen einen @context, der JSON-Schlüssel auf IRIs abbildet, mit @id für den Bezeichner des Knotens und @type für seine Klasse, sodass Webentwickelnde mit vertrautem JSON arbeiten können (W3C JSON-LD 1.1).

### Wann einsetzen

- Wenn Daten mehrerer Organisationen oder Quellen mit stabilen, globalen Bezeichnern zusammengeführt werden müssen (W3C RDF 1.1 Concepts).
- Wenn Daten als Linked Data veröffentlicht und mit Standardvokabularen wiederverwendet werden sollen (W3C RDF 1.1 Primer).
- Wenn eine Anwendung vor allem schnelle Traversierung innerhalb einer Datenbank braucht, kann ein Property Graph einfacher sein ([[graph-databases|Graphdatenbanken]]).

### Stärken und Grenzen

**Stärken**
- Globale IRIs machen das Zusammenführen von Graphen aus verschiedenen Quellen einfach (W3C RDF 1.1 Concepts).
- Ein Datenmodell mit mehreren Serialisierungen, darunter JSON-LD für Webentwickelnde (W3C RDF 1.1 Primer; W3C JSON-LD 1.1).
- Standardvokabulare und OWL-Schlussfolgern ergänzen gemeinsame Bedeutung (W3C RDF Schema 1.1; W3C OWL 2 Primer).

**Einschränkungen**
- Aussagen über Aussagen erfordern Reifikation oder Named Graphs, was die Daten umfangreicher macht (W3C RDF Schema 1.1; W3C RDF 1.1 Concepts).
- Blank Nodes haben keinen globalen Namen, was Zusammenführen und Vergleichen erschwert (W3C RDF 1.1 Concepts).
- Die formale OWL-Semantik folgt der Open-World-Annahme, die von Datenbank-Intuitionen abweicht (W3C OWL 2 Primer).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Turtle | Kompakte, menschenlesbare Tripel (W3C Turtle) | RDF von Hand schreiben und lesen |
| JSON-LD | JSON mit einem Kontext, der Schlüssel auf IRIs abbildet (W3C JSON-LD 1.1) | Web-APIs und strukturierte Daten auf Websites |
| N-Triples / N-Quads | Eine Aussage je Zeile (W3C RDF 1.1 Primer) | Massenimport und Streaming |
| Property Graphs | Knoten und Beziehungen mit Schlüssel-Wert-Eigenschaften ([[graph-databases|Graphdatenbanken]]) | Graphanwendungen innerhalb einer Datenbank |

### In der Praxis

RDF-Daten werden gegen eine Ontologie modelliert ([[ontology-design|Ontologie-Design]]), mit Shapes validiert und in einem Triplestore gespeichert, wobei Named Graphs die Quelle jedes Datenteils festhalten ([[knowledge-graph-engineering|Knowledge Graph Engineering]]). Etablierte Vokabulare wiederzuverwenden, statt neue Begriffe zu erfinden, erleichtert die Integration der Daten (W3C RDF 1.1 Primer).

### Merksatz

RDF drückt Wissen als Tripel mit globalen Bezeichnern aus, wodurch sich Graphen aus verschiedenen Quellen zusammenführen lassen und über Standardvokabulare eine gemeinsame Bedeutung erhalten.

### Quellen

- W3C (2014). *RDF 1.1 Concepts and Abstract Syntax.* W3C Recommendation. [w3.org](https://www.w3.org/TR/rdf11-concepts/)
- W3C (2014). *RDF 1.1 Turtle: Terse RDF Triple Language.* W3C Recommendation. [w3.org](https://www.w3.org/TR/turtle/)
- W3C (2014). *RDF 1.1 Primer.* W3C Working Group Note. [w3.org](https://www.w3.org/TR/rdf11-primer/)
- W3C (2014). *RDF Schema 1.1.* W3C Recommendation. [w3.org](https://www.w3.org/TR/rdf-schema/)
- W3C (2020). *JSON-LD 1.1: A JSON-based Serialization for Linked Data.* W3C Recommendation. [w3.org](https://www.w3.org/TR/json-ld11/)
- W3C (2012). *OWL 2 Web Ontology Language Primer (Second Edition).* W3C Recommendation. [w3.org](https://www.w3.org/TR/owl2-primer/)
