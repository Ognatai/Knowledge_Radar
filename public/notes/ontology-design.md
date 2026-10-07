---
title_en: Ontology Design
title_de: Ontologie-Design
entity_type: Method
sources:
- https://protege.stanford.edu/publications/ontology_development/ontology101.pdf
- https://www.w3.org/TR/owl2-primer/
- https://www.w3.org/TR/rdf-schema/
- https://www.w3.org/TR/skos-reference/
- https://arxiv.org/abs/2003.02320
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

An ontology is an explicit formal specification of the terms in a domain and the relations among them; it gives people and software a shared vocabulary and makes domain assumptions explicit (Noy & McGuinness, 2001). Ontology design proceeds iteratively from the questions the ontology must answer to classes, properties and instances, and is expressed in standards such as RDF Schema, OWL and SKOS (W3C RDF Schema 1.1; W3C OWL 2 Primer; W3C SKOS). It provides the schema layer of a knowledge graph (Hogan et al., 2020).

### How it works

The designer fixes the domain and the questions the ontology should answer, reuses existing vocabularies where possible, collects the important terms, organises them into a class hierarchy, defines properties with their constraints, and finally creates instances; the cycle is repeated as the ontology is tested in use.

```text
1. Scope and competency questions
▼
2. Reuse existing ontologies
▼
3. Classes and hierarchy
▼
4. Properties and constraints
▼
5. Instances and standards
```

#### 1. Scope and competency questions

Reasons to develop an ontology include sharing a common understanding of the structure of information, reusing domain knowledge, making domain assumptions explicit and separating domain knowledge from operational knowledge (Noy & McGuinness, 2001). Design starts by fixing the domain and scope, for example with competency questions, i.e. questions the knowledge base built on the ontology should be able to answer; they also serve as a test of the finished ontology.

#### 2. Reuse existing ontologies

Before modelling, existing ontologies and vocabularies should be checked for reuse (Noy & McGuinness, 2001). Widely used vocabularies include SKOS for thesauri and taxonomies, with concepts, preferred and alternative labels and broader and narrower links (W3C SKOS), and PROV-O for provenance.

#### 3. Classes and hierarchy

Important terms are enumerated and organised into classes and a class hierarchy, developed top-down, bottom-up or in combination (Noy & McGuinness, 2001). RDF Schema expresses classes with rdfs:Class, membership with rdf:type and hierarchies with rdfs:subClassOf (W3C RDF Schema 1.1). OWL adds, for example, disjointness between classes, so that a reasoner can detect contradictions (W3C OWL 2 Primer).

#### 4. Properties and constraints

Properties (slots) describe the internal structure of classes, and facets such as value type and cardinality constrain them (Noy & McGuinness, 2001). In RDF Schema, rdfs:domain and rdfs:range state which classes a property connects (W3C RDF Schema 1.1); OWL properties can be declared transitive, symmetric, inverse or functional, which lets reasoners infer implicit facts under the open-world assumption (W3C OWL 2 Primer).

#### 5. Instances and standards

Finally, individual instances of the classes are created (Noy & McGuinness, 2001). The ontology then forms the schema of a knowledge graph, alongside identity and context (Hogan et al., 2020; [[knowledge-graphs|Knowledge Graphs]]); data can be validated against required structures with shape languages ([[knowledge-graph-engineering|Knowledge Graph Engineering]]).

#### Origin and variants

Noy & McGuinness (2001) wrote the widely used introductory guide to ontology development. RDF Schema (W3C RDF Schema 1.1), OWL 2 (W3C OWL 2 Primer) and SKOS (W3C SKOS) are the W3C standards for vocabularies of increasing or different expressiveness, and Hogan et al. (2020) place ontologies within knowledge graphs.

### When to use it

- When several teams or systems must share the same understanding of domain terms (Noy & McGuinness, 2001).
- When a knowledge graph needs a schema that allows reasoning, OWL fits (W3C OWL 2 Primer).
- When only a controlled vocabulary or taxonomy is needed, the lighter SKOS fits (W3C SKOS).

### Strengths and limitations

**Strengths**
- Makes domain assumptions explicit and reusable (Noy & McGuinness, 2001).
- Formal semantics allow reasoning and consistency checks (W3C OWL 2 Primer).
- Standard vocabularies make data interoperable (W3C RDF Schema 1.1; W3C SKOS).

**Limitations**
- There is no single correct way to model a domain; the right model depends on the intended application (Noy & McGuinness, 2001).
- Under the open-world assumption, OWL does not flag missing information as an error (W3C OWL 2 Primer).
- Ontologies must evolve together with the domain and the graph built on them (Hogan et al., 2020).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| SKOS | Concepts with labels and broader or narrower links, no formal logic (W3C SKOS) | Thesauri, taxonomies, controlled vocabularies |
| RDF Schema | Classes, subclasses, domain and range (W3C RDF Schema 1.1) | Lightweight schemas |
| OWL 2 | Rich axioms for reasoning, open-world semantics (W3C OWL 2 Primer) | Formal domain models with inference |

### In practice

A simple legal ontology might define classes such as Norm, Decision and Party, with properties such as cites (from Decision to Norm) and amends (from Norm to Norm), and test it against competency questions such as "which decisions cite this norm?" (Noy & McGuinness, 2001). Typical mistakes are confusing classes with instances and building hierarchies that do not reflect the questions the application needs to answer.

### Key takeaway

Ontology design turns the vocabulary of a domain into explicit classes, properties and constraints, guided by the questions the resulting knowledge base must answer.

### Sources

- Noy, N. F. & McGuinness, D. L. (2001). *Ontology Development 101: A Guide to Creating Your First Ontology.* Stanford Knowledge Systems Laboratory Technical Report KSL-01-05. [PDF](https://protege.stanford.edu/publications/ontology_development/ontology101.pdf)
- W3C (2012). *OWL 2 Web Ontology Language Primer (Second Edition).* W3C Recommendation. [w3.org](https://www.w3.org/TR/owl2-primer/)
- W3C (2014). *RDF Schema 1.1.* W3C Recommendation. [w3.org](https://www.w3.org/TR/rdf-schema/)
- W3C (2009). *SKOS Simple Knowledge Organization System Reference.* W3C Recommendation. [w3.org](https://www.w3.org/TR/skos-reference/)
- Hogan, A. et al. (2020). *Knowledge Graphs.* ACM Computing Surveys 2021. [arXiv:2003.02320](https://arxiv.org/abs/2003.02320)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Eine Ontologie ist eine ausdrückliche, formale Spezifikation der Begriffe eines Fachgebiets und ihrer Beziehungen; sie gibt Menschen und Software ein gemeinsames Vokabular und macht Annahmen über das Fachgebiet ausdrücklich (Noy & McGuinness, 2001). Ontologie-Design geht schrittweise von den Fragen, die die Ontologie beantworten soll, zu Klassen, Eigenschaften und Instanzen vor und wird in Standards wie RDF Schema, OWL und SKOS ausgedrückt (W3C RDF Schema 1.1; W3C OWL 2 Primer; W3C SKOS). Es liefert die Schemaebene eines Wissensgraphen (Hogan et al., 2020).

### Funktionsweise

Das Fachgebiet und die zu beantwortenden Fragen werden festgelegt, bestehende Vokabulare nach Möglichkeit wiederverwendet, die wichtigen Begriffe gesammelt, in eine Klassenhierarchie geordnet, Eigenschaften mit ihren Einschränkungen definiert und schließlich Instanzen angelegt; der Zyklus wiederholt sich, während die Ontologie im Einsatz erprobt wird.

```text
1. Umfang und Competency Questions
▼
2. Bestehende Ontologien wiederverwenden
▼
3. Klassen und Hierarchie
▼
4. Eigenschaften und Einschränkungen
▼
5. Instanzen und Standards
```

#### 1. Umfang und Competency Questions

Gründe für eine Ontologie sind ein gemeinsames Verständnis der Informationsstruktur, die Wiederverwendung von Fachwissen, das Offenlegen von Annahmen über das Fachgebiet und die Trennung von Fachwissen und operativem Wissen (Noy & McGuinness, 2001). Der Entwurf beginnt damit, Fachgebiet und Umfang festzulegen, etwa mit Competency Questions, also Fragen, die eine auf der Ontologie aufbauende Wissensbasis beantworten können soll; sie dienen auch als Test der fertigen Ontologie.

#### 2. Bestehende Ontologien wiederverwenden

Vor der Modellierung sollten bestehende Ontologien und Vokabulare auf Wiederverwendbarkeit geprüft werden (Noy & McGuinness, 2001). Verbreitete Vokabulare sind etwa SKOS für Thesauri und Taxonomien mit Konzepten, bevorzugten und alternativen Bezeichnungen sowie über- und untergeordneten Verknüpfungen (W3C SKOS) und PROV-O für Provenienz.

#### 3. Klassen und Hierarchie

Die wichtigen Begriffe werden gesammelt und zu Klassen und einer Klassenhierarchie geordnet, von oben nach unten, von unten nach oben oder kombiniert (Noy & McGuinness, 2001). RDF Schema drückt Klassen mit rdfs:Class, Zugehörigkeit mit rdf:type und Hierarchien mit rdfs:subClassOf aus (W3C RDF Schema 1.1). OWL ergänzt etwa die Disjunktheit von Klassen, sodass ein Reasoner Widersprüche erkennen kann (W3C OWL 2 Primer).

#### 4. Eigenschaften und Einschränkungen

Eigenschaften (Slots) beschreiben die innere Struktur von Klassen, und Facetten wie Wertetyp und Kardinalität schränken sie ein (Noy & McGuinness, 2001). In RDF Schema legen rdfs:domain und rdfs:range fest, welche Klassen eine Eigenschaft verbindet (W3C RDF Schema 1.1); OWL-Eigenschaften lassen sich als transitiv, symmetrisch, invers oder funktional deklarieren, wodurch Reasoner unter der Open-World-Annahme implizite Fakten ableiten können (W3C OWL 2 Primer).

#### 5. Instanzen und Standards

Zum Schluss werden einzelne Instanzen der Klassen angelegt (Noy & McGuinness, 2001). Die Ontologie bildet dann neben Identität und Kontext das Schema eines Wissensgraphen (Hogan et al., 2020; [[knowledge-graphs|Wissensgraphen]]); Daten lassen sich mit Shape-Sprachen gegen erforderliche Strukturen validieren ([[knowledge-graph-engineering|Knowledge Graph Engineering]]).

#### Ursprung und Varianten

Noy & McGuinness (2001) schrieben den viel genutzten Einführungsleitfaden zur Ontologieentwicklung. RDF Schema (W3C RDF Schema 1.1), OWL 2 (W3C OWL 2 Primer) und SKOS (W3C SKOS) sind die W3C-Standards für Vokabulare unterschiedlicher Ausdrucksstärke, und Hogan et al. (2020) ordnen Ontologien in Wissensgraphen ein.

### Wann einsetzen

- Wenn mehrere Teams oder Systeme dasselbe Verständnis fachlicher Begriffe teilen müssen (Noy & McGuinness, 2001).
- Wenn ein Wissensgraph ein Schema braucht, das Schlussfolgern erlaubt, passt OWL (W3C OWL 2 Primer).
- Wenn nur ein kontrolliertes Vokabular oder eine Taxonomie gebraucht wird, passt das leichtere SKOS (W3C SKOS).

### Stärken und Grenzen

**Stärken**
- Macht Annahmen über das Fachgebiet ausdrücklich und wiederverwendbar (Noy & McGuinness, 2001).
- Formale Semantik erlaubt Schlussfolgern und Konsistenzprüfungen (W3C OWL 2 Primer).
- Standardvokabulare machen Daten interoperabel (W3C RDF Schema 1.1; W3C SKOS).

**Einschränkungen**
- Es gibt nicht die eine richtige Modellierung eines Fachgebiets; das passende Modell hängt von der geplanten Anwendung ab (Noy & McGuinness, 2001).
- Unter der Open-World-Annahme meldet OWL fehlende Information nicht als Fehler (W3C OWL 2 Primer).
- Ontologien müssen sich mit dem Fachgebiet und dem darauf aufbauenden Graphen weiterentwickeln (Hogan et al., 2020).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| SKOS | Konzepte mit Bezeichnungen und über- oder untergeordneten Verknüpfungen, keine formale Logik (W3C SKOS) | Thesauri, Taxonomien, kontrollierte Vokabulare |
| RDF Schema | Klassen, Unterklassen, Domain und Range (W3C RDF Schema 1.1) | Leichtgewichtige Schemata |
| OWL 2 | Reichhaltige Axiome für Schlussfolgerungen, Open-World-Semantik (W3C OWL 2 Primer) | Formale Fachmodelle mit Inferenz |

### In der Praxis

Eine einfache juristische Ontologie könnte Klassen wie Norm, Entscheidung und Partei mit Eigenschaften wie zitiert (von Entscheidung zu Norm) und ändert (von Norm zu Norm) definieren und gegen Competency Questions wie „Welche Entscheidungen zitieren diese Norm?“ geprüft werden (Noy & McGuinness, 2001). Typische Fehler sind die Verwechslung von Klassen und Instanzen und Hierarchien, die nicht zu den Fragen passen, die die Anwendung beantworten muss.

### Merksatz

Ontologie-Design macht aus dem Vokabular eines Fachgebiets ausdrückliche Klassen, Eigenschaften und Einschränkungen, geleitet von den Fragen, die die entstehende Wissensbasis beantworten soll.

### Quellen

- Noy, N. F. & McGuinness, D. L. (2001). *Ontology Development 101: A Guide to Creating Your First Ontology.* Stanford Knowledge Systems Laboratory Technical Report KSL-01-05. [PDF](https://protege.stanford.edu/publications/ontology_development/ontology101.pdf)
- W3C (2012). *OWL 2 Web Ontology Language Primer (Second Edition).* W3C Recommendation. [w3.org](https://www.w3.org/TR/owl2-primer/)
- W3C (2014). *RDF Schema 1.1.* W3C Recommendation. [w3.org](https://www.w3.org/TR/rdf-schema/)
- W3C (2009). *SKOS Simple Knowledge Organization System Reference.* W3C Recommendation. [w3.org](https://www.w3.org/TR/skos-reference/)
- Hogan, A. et al. (2020). *Knowledge Graphs.* ACM Computing Surveys 2021. [arXiv:2003.02320](https://arxiv.org/abs/2003.02320)
