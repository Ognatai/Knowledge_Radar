---
title_en: Confluence
title_de: Confluence
entity_type: Technology
sources:
- https://support.atlassian.com/confluence-cloud/docs/what-is-a-space/
- https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/
- https://developer.atlassian.com/cloud/confluence/rest/v2/intro/
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Confluence is Atlassian's team wiki: content lives in spaces, which act as collaborative workspaces or knowledge bases for a team, project or initiative and contain pages organised in a page tree (Confluence spaces docs). Content can be searched with the Confluence Query Language (CQL), which has an SQL-like look but is not a database query language (Confluence CQL docs), and automated through a REST API (Confluence REST API docs). It is a common source system for enterprise RAG and knowledge management.

### Core concepts

- **Spaces:** A space is a container where a team creates, stores and collaborates on work related to a team, shared project or initiative (Confluence spaces docs).
- **Pages and page tree:** Pages are organised hierarchically with parent and child pages; blog posts complement them for time-based updates (Confluence spaces docs).
- **Labels, macros and templates:** Labels categorise content, macros insert dynamic elements such as a table of contents, a page tree, a status or a code block, and templates standardise new pages (Confluence spaces docs).
- **CQL:** A clause consists of a field, an operator and one or more values or functions, for example space = "TEST"; clauses are combined with AND, OR and NOT and sorted with ORDER BY, but there is no SELECT statement (Confluence CQL docs).
- **REST API:** Endpoints for pages, blog posts, spaces, attachments, comments, labels and properties; lists use cursor-based pagination with limit and cursor parameters, and the Link header points to the next page of results (Confluence REST API docs).

### Common usage

```text
# CQL: recently changed pages in a space with a label
space = "LEGAL" AND type = page AND label = "gdpr"
  AND lastmodified > now("-30d") ORDER BY lastmodified DESC

# CQL: full-text search for a term
text ~ "data protection impact assessment" AND type = page
```

```bash
# REST API v2: list pages, five at a time (cursor-based pagination)
curl -u "$USER:$API_TOKEN" \
  "https://<site>.atlassian.net/wiki/api/v2/pages?limit=5"
# follow the URL in the Link header (rel="next") for the next five pages
```

The content REST API accepts CQL as a query parameter, so searches defined in CQL can be reused in scripts (Confluence CQL docs).

### When to use it

- When a team needs a shared, structured place for documentation and decisions (Confluence spaces docs).
- When documentation must be searched by space, label, author or date (Confluence CQL docs).
- When pages should be exported or synchronised automatically, for example into a RAG index (Confluence REST API docs; [[retrieval-augmented-generation|Retrieval-Augmented Generation]]).

### Strengths and limitations

**Strengths**
- Spaces and page trees give teams a clear structure (Confluence spaces docs).
- CQL searches across fields such as space, type, label and modification date (Confluence CQL docs).
- The REST API allows automation and integration (Confluence REST API docs).

**Limitations**
- CQL only searches content and is not a general database query language (Confluence CQL docs).
- API results are paginated, so exports must follow the cursor links (Confluence REST API docs).
- Content stored in macros and page structure is harder to process than plain Markdown files.

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Confluence | Hosted wiki with spaces, page trees, permissions, CQL and REST API (Confluence spaces docs; Confluence REST API docs) | Team documentation in organisations |
| Markdown vault (e.g. Obsidian) | Local Markdown files with links, versionable with Git ([[git|Git]]) | Personal or developer knowledge bases |
| Knowledge graph | Explicit entities and relations ([[knowledge-graphs|Knowledge Graphs]]) | Structured, queryable domain knowledge |

### In practice

For a RAG system over Confluence, pages are fetched through the REST API with pagination, filtered with CQL by space or label, converted to text with their metadata (space, title, last modified date) and chunked for indexing (Confluence REST API docs; Confluence CQL docs; [[rag-chunking|RAG: Chunking]]). Permissions must be respected, so that the assistant only answers from pages the user may see.

### Key takeaway

Confluence organises team knowledge in spaces and page trees; CQL finds content and the REST API makes it available to scripts and RAG pipelines.

### Sources

- Atlassian. *What is a space?* Confluence Cloud documentation. [support.atlassian.com](https://support.atlassian.com/confluence-cloud/docs/what-is-a-space/)
- Atlassian. *Advanced searching using CQL.* Confluence developer documentation. [developer.atlassian.com](https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/)
- Atlassian. *The Confluence Cloud REST API v2.* Confluence developer documentation. [developer.atlassian.com](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Confluence ist das Team-Wiki von Atlassian: Inhalte liegen in Bereichen (Spaces), die als gemeinsame Arbeitsräume oder Wissensbasen für ein Team, ein Projekt oder eine Initiative dienen und Seiten in einem Seitenbaum enthalten (Confluence spaces docs). Inhalte lassen sich mit der Confluence Query Language (CQL) durchsuchen, die SQL-ähnlich aussieht, aber keine Datenbank-Abfragesprache ist (Confluence CQL docs), und über eine REST-API automatisieren (Confluence REST API docs). Confluence ist ein häufiges Quellsystem für RAG und Wissensmanagement in Unternehmen.

### Kernkonzepte

- **Bereiche (Spaces):** Ein Bereich ist ein Container, in dem ein Team Arbeit zu einem Team, einem gemeinsamen Projekt oder einer Initiative erstellt, speichert und gemeinsam bearbeitet (Confluence spaces docs).
- **Seiten und Seitenbaum:** Seiten sind hierarchisch mit über- und untergeordneten Seiten organisiert; Blogbeiträge ergänzen sie für zeitbezogene Mitteilungen (Confluence spaces docs).
- **Labels, Makros und Vorlagen:** Labels kategorisieren Inhalte, Makros fügen dynamische Elemente wie Inhaltsverzeichnis, Seitenbaum, Status oder Codeblock ein, und Vorlagen vereinheitlichen neue Seiten (Confluence spaces docs).
- **CQL:** Eine Klausel besteht aus einem Feld, einem Operator und einem oder mehreren Werten oder Funktionen, etwa space = "TEST"; Klauseln werden mit AND, OR und NOT verbunden und mit ORDER BY sortiert, eine SELECT-Anweisung gibt es aber nicht (Confluence CQL docs).
- **REST-API:** Endpunkte für Seiten, Blogbeiträge, Bereiche, Anhänge, Kommentare, Labels und Eigenschaften; Listen nutzen cursorbasierte Paginierung mit den Parametern limit und cursor, und der Link-Header verweist auf die nächste Ergebnisseite (Confluence REST API docs).

### Typische Verwendung

```text
# CQL: kürzlich geänderte Seiten in einem Bereich mit einem Label
space = "LEGAL" AND type = page AND label = "gdpr"
  AND lastmodified > now("-30d") ORDER BY lastmodified DESC

# CQL: Volltextsuche nach einem Begriff
text ~ "Datenschutz-Folgenabschätzung" AND type = page
```

```bash
# REST-API v2: Seiten auflisten, jeweils fünf (cursorbasierte Paginierung)
curl -u "$USER:$API_TOKEN" \
  "https://<site>.atlassian.net/wiki/api/v2/pages?limit=5"
# für die nächsten fünf Seiten der URL im Link-Header (rel="next") folgen
```

Die Content-REST-API akzeptiert CQL als Abfrageparameter, sodass in CQL formulierte Suchen in Skripten wiederverwendet werden können (Confluence CQL docs).

### Wann einsetzen

- Wenn ein Team einen gemeinsamen, strukturierten Ort für Dokumentation und Entscheidungen braucht (Confluence spaces docs).
- Wenn Dokumentation nach Bereich, Label, Autor oder Datum durchsucht werden muss (Confluence CQL docs).
- Wenn Seiten automatisch exportiert oder synchronisiert werden sollen, etwa in einen RAG-Index (Confluence REST API docs; [[retrieval-augmented-generation|Retrieval-Augmented Generation]]).

### Stärken und Grenzen

**Stärken**
- Bereiche und Seitenbäume geben Teams eine klare Struktur (Confluence spaces docs).
- CQL sucht über Felder wie Bereich, Typ, Label und Änderungsdatum (Confluence CQL docs).
- Die REST-API ermöglicht Automatisierung und Integration (Confluence REST API docs).

**Einschränkungen**
- CQL durchsucht nur Inhalte und ist keine allgemeine Datenbank-Abfragesprache (Confluence CQL docs).
- API-Ergebnisse sind paginiert, Exporte müssen also den Cursor-Links folgen (Confluence REST API docs).
- In Makros und Seitenstruktur abgelegte Inhalte sind schwerer zu verarbeiten als einfache Markdown-Dateien.

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Confluence | Gehostetes Wiki mit Bereichen, Seitenbäumen, Berechtigungen, CQL und REST-API (Confluence spaces docs; Confluence REST API docs) | Teamdokumentation in Organisationen |
| Markdown-Vault (z. B. Obsidian) | Lokale Markdown-Dateien mit Links, versionierbar mit Git ([[git|Git]]) | Persönliche oder Entwickler-Wissensbasen |
| Wissensgraph | Ausdrückliche Entitäten und Beziehungen ([[knowledge-graphs|Wissensgraphen]]) | Strukturiertes, abfragbares Fachwissen |

### In der Praxis

Für ein RAG-System über Confluence werden Seiten über die REST-API mit Paginierung abgerufen, mit CQL nach Bereich oder Label gefiltert, samt Metadaten (Bereich, Titel, letztes Änderungsdatum) in Text umgewandelt und für die Indexierung in Abschnitte zerlegt (Confluence REST API docs; Confluence CQL docs; [[rag-chunking|RAG: Chunking]]). Berechtigungen müssen beachtet werden, damit der Assistent nur aus Seiten antwortet, die die Person sehen darf.

### Merksatz

Confluence ordnet Teamwissen in Bereichen und Seitenbäumen; CQL findet Inhalte, und die REST-API macht sie für Skripte und RAG-Pipelines verfügbar.

### Quellen

- Atlassian. *What is a space?* Confluence Cloud documentation. [support.atlassian.com](https://support.atlassian.com/confluence-cloud/docs/what-is-a-space/)
- Atlassian. *Advanced searching using CQL.* Confluence developer documentation. [developer.atlassian.com](https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/)
- Atlassian. *The Confluence Cloud REST API v2.* Confluence developer documentation. [developer.atlassian.com](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/)
