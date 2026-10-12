---
title_en: Web Crawling
title_de: Web-Crawling
entity_type: Method
aliases:
- Web crawler
- Crawler
- Spider
- URL frontier
- robots.txt
sources:
- https://nlp.stanford.edu/IR-book/pdf/20crawl.pdf
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

A web crawler starts from seed URLs, fetches pages, extracts their text for the indexer and their links for the URL frontier, and repeats, traversing the web graph (Manning et al., 2008, ch. 20). A crawler must be robust against spider traps and polite to web servers; it should be distributed, scalable, efficient, biased towards useful pages, fresh and extensible. Its core is the URL frontier, which orders URLs by priority and keeps only one connection per host with pauses between requests (Manning et al., 2008, ch. 20).

### How it works

```text
URL frontier ─► DNS resolution ─► fetch (http) ─► parse: text → indexer, links + anchor text
     ▲                                                     │
     │        content seen? (fingerprint / shingles)  ◄────┘
     │        URL filter + robots.txt
     │        URL normalisation
     └────────duplicate URL elimination ◄──────────────────┘
```

#### 1. Requirements

A crawler must be robust, because some servers generate an infinite number of pages that trap crawlers, often by faulty site design rather than malice, and polite, respecting servers' implicit and explicit limits on visit rates. It should be distributed and scalable across machines, use processor, storage and bandwidth efficiently, fetch useful pages first, keep copies fresh by revisiting pages about as often as they change, and be modular enough to add formats and protocols (Manning et al., 2008, ch. 20). Any crawler should open only one connection to a host at a time and wait a few seconds between requests to the same host (Manning et al., 2008, ch. 20).

#### 2. The crawl loop

A crawler thread takes a URL from the frontier, fetches the page via http and stores it temporarily. The parser passes the text to the indexer ([[inverted-index|Inverted Index]]) and the links with their anchor text to the indexer for ranking ([[pagerank|PageRank and Link Analysis]]). Each link then passes several tests before it enters the frontier (Manning et al., 2008, ch. 20). The book follows the Mercator crawler, which has formed the basis of a number of research and commercial crawlers; fetching a billion pages in a month requires several hundred pages per second (Manning et al., 2008, ch. 20).

#### 3. Tests before the frontier

- **Content seen?** A fingerprint such as a checksum detects pages whose content was already fetched at another URL; shingles detect near-duplicates ([[near-duplicate-detection|Near-Duplicate Detection]]).
- **URL filter:** excludes or includes domains, and applies the Robots Exclusion Protocol: a robots.txt file at the root of a site lists paths that robots, or specific robots, must not visit. robots.txt files are cached, but the check is made just before fetching, because a URL may wait in the frontier for days while the file changes.
- **Normalisation:** relative links are turned into absolute URLs.
- **Duplicate URL elimination:** URLs already in the frontier, or already crawled in a one-off crawl, are not added again (Manning et al., 2008, ch. 20).

#### 4. DNS resolution

Turning a host name into an IP address is a well-known bottleneck, since a lookup can take seconds. Crawlers cache DNS results and implement their own asynchronous resolver, because the standard library lookups block other threads (Manning et al., 2008, ch. 20).

#### 5. The URL frontier: priority and politeness

The frontier returns URLs by two considerations: high-quality pages that change often should be crawled often, so priority combines change rate and quality, as many spam pages change completely on every fetch; and politeness forbids repeated requests to one host in a short time. A common heuristic waits between requests to a host for an order of magnitude longer than the last fetch from it took. In the Mercator design, F front queues implement priority, a prioritiser assigning each URL a queue by its fetch history, and B back queues implement politeness, each holding URLs of a single host (Manning et al., 2008, ch. 20).

#### 6. Distributed crawling and indexing

Crawler threads run on many nodes, each responsible for a set of hosts, with a host splitter passing URLs to the right node (Manning et al., 2008, ch. 20). The resulting index can be partitioned by terms, which complicates multi-word queries and load balancing, or more commonly by documents, where each query goes to all nodes and global statistics such as idf are computed by background processes (Manning et al., 2008, ch. 20).

#### Origin and variants

The Mercator crawler design underlies many research and commercial crawlers (Manning et al., 2008, ch. 20). Continuous crawling puts fetched URLs back into the frontier to refresh them later (Manning et al., 2008, ch. 20).

### When to use it

- To build a search index over web pages, an intranet or any hypertext collection (Manning et al., 2008, ch. 20).
- Continuous crawling when the index must stay current with changing pages (Manning et al., 2008, ch. 20).
- As the extraction stage of a [[data-pipelines|data pipeline]] that collects web documents.

### Strengths and limitations

**Strengths**
- A simple loop that scales out by adding machines and bandwidth (Manning et al., 2008, ch. 20).
- Prioritisation spends the crawl budget on useful, often-changing pages (Manning et al., 2008, ch. 20).
- Fingerprints and shingles avoid indexing the same content twice (Manning et al., 2008, ch. 20).

**Limitations**
- Spider traps can produce infinite pages (Manning et al., 2008, ch. 20).
- Politeness limits the fetch rate per host and the DNS cache hit rate (Manning et al., 2008, ch. 20).
- Spam pages that change on every fetch defeat change-rate heuristics unless quality is also considered (Manning et al., 2008, ch. 20).

### Comparison

| Component | Purpose | Detail |
|-----------|---------|--------|
| URL frontier | Order of fetching | Front queues for priority, back queues for politeness (Manning et al., 2008, ch. 20) |
| robots.txt | Respect site rules | Checked just before fetching (Manning et al., 2008, ch. 20) |
| Content fingerprint | Exact duplicates | Checksum per page (Manning et al., 2008, ch. 20) |
| Shingles | Near-duplicates | See [[near-duplicate-detection\|Near-Duplicate Detection]] |
| Document-partitioned index | Serving queries | Each node indexes a subset of documents (Manning et al., 2008, ch. 20) |

### In practice

A housekeeping thread logs crawl statistics every few seconds and checkpoints the frontier to disk every few hours, so that a failed crawl can restart from the last checkpoint (Manning et al., 2008, ch. 20). A simple way to partition the index is to assign all pages from one host to a single node (Manning et al., 2008, ch. 20).

### Key takeaway

A crawler loops over a URL frontier, fetching, parsing and filtering pages; politeness per host, priority by quality and change rate, and duplicate detection make it practical at web scale.

### Sources

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Web crawling and indexes.* Introduction to Information Retrieval, Chapter 20. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/20crawl.pdf)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Ein Web-Crawler beginnt mit Start-URLs, lädt Seiten, gibt ihren Text an den Indexer und ihre Links an die URL Frontier weiter und wiederholt das, wobei er den Web-Graphen durchläuft (Manning et al., 2008, Kap. 20). Ein Crawler muss robust gegen Spider Traps und höflich gegenüber Webservern sein; er sollte verteilt, skalierbar und effizient sein, nützliche Seiten bevorzugen, Kopien aktuell halten und erweiterbar sein. Sein Kern ist die URL Frontier, die URLs nach Priorität ordnet und pro Host nur eine Verbindung mit Pausen zwischen den Anfragen zulässt (Manning et al., 2008, Kap. 20).

### Funktionsweise

```text
URL Frontier ─► DNS-Auflösung ─► Abruf (http) ─► Parsen: Text → Indexer, Links + Ankertext
     ▲                                                       │
     │        Inhalt schon gesehen? (Fingerprint / Shingles) ◄┘
     │        URL-Filter + robots.txt
     │        URL-Normalisierung
     └────────Entfernen doppelter URLs ◄─────────────────────┘
```

#### 1. Anforderungen

Ein Crawler muss robust sein, weil manche Server unendlich viele Seiten erzeugen, die Crawler festhalten, oft durch fehlerhaftes Website-Design statt Absicht, und höflich, also die impliziten und expliziten Grenzen der Server für Besuchsraten respektieren. Er sollte verteilt und über Maschinen skalierbar sein, Prozessor, Speicher und Bandbreite effizient nutzen, nützliche Seiten zuerst laden, Kopien aktuell halten, indem er Seiten etwa so oft besucht, wie sie sich ändern, und modular genug sein, um Formate und Protokolle zu ergänzen (Manning et al., 2008, Kap. 20). Jeder Crawler sollte nur eine Verbindung gleichzeitig zu einem Host öffnen und zwischen Anfragen an denselben Host einige Sekunden warten (Manning et al., 2008, Kap. 20).

#### 2. Die Crawl-Schleife

Ein Crawler-Thread nimmt eine URL aus der Frontier, lädt die Seite per http und speichert sie zwischen. Der Parser gibt den Text an den Indexer ([[inverted-index|Inverted Index]]) und die Links mit ihrem Ankertext an den Indexer für das Ranking ([[pagerank|PageRank und Linkanalyse]]). Jeder Link durchläuft dann mehrere Prüfungen, bevor er in die Frontier kommt (Manning et al., 2008, Kap. 20). Das Buch folgt dem Crawler Mercator, der die Grundlage einer Reihe von Forschungs- und kommerziellen Crawlern bildet; eine Milliarde Seiten in einem Monat zu laden erfordert mehrere Hundert Seiten pro Sekunde (Manning et al., 2008, Kap. 20).

#### 3. Prüfungen vor der Frontier

- **Inhalt schon gesehen?** Ein Fingerprint wie eine Prüfsumme erkennt Seiten, deren Inhalt schon unter einer anderen URL geladen wurde; Shingles erkennen Beinahe-Duplikate ([[near-duplicate-detection|Near-Duplicate Detection]]).
- **URL-Filter:** schließt Domains aus oder ein und wendet das Robots Exclusion Protocol an: Eine Datei robots.txt im Wurzelverzeichnis einer Website listet Pfade, die Robots oder bestimmte Robots nicht besuchen dürfen. robots.txt-Dateien werden zwischengespeichert, die Prüfung erfolgt aber direkt vor dem Abruf, weil eine URL tagelang in der Frontier warten kann, während sich die Datei ändert.
- **Normalisierung:** Relative Links werden zu absoluten URLs.
- **Entfernen doppelter URLs:** URLs, die schon in der Frontier sind oder bei einem einmaligen Crawl schon geladen wurden, kommen nicht erneut hinein (Manning et al., 2008, Kap. 20).

#### 4. DNS-Auflösung

Einen Hostnamen in eine IP-Adresse aufzulösen ist ein bekannter Engpass, weil eine Abfrage Sekunden dauern kann. Crawler speichern DNS-Ergebnisse zwischen und setzen einen eigenen asynchronen Resolver um, weil die Abfragen der Standardbibliotheken andere Threads blockieren (Manning et al., 2008, Kap. 20).

#### 5. Die URL Frontier: Priorität und Höflichkeit

Die Frontier gibt URLs nach zwei Gesichtspunkten aus: Hochwertige Seiten, die sich oft ändern, sollen oft geladen werden, daher verbindet die Priorität Änderungsrate und Qualität, denn viele Spam-Seiten ändern sich bei jedem Abruf vollständig; und Höflichkeit verbietet wiederholte Anfragen an einen Host in kurzer Zeit. Eine übliche Heuristik wartet zwischen Anfragen an einen Host eine Größenordnung länger, als der letzte Abruf von dort gedauert hat. Im Mercator-Design setzen F Front Queues die Priorität um, wobei ein Priorisierer jeder URL anhand ihrer Abrufhistorie eine Queue zuweist, und B Back Queues die Höflichkeit, jede mit URLs eines einzigen Hosts (Manning et al., 2008, Kap. 20).

#### 6. Verteiltes Crawlen und Indexieren

Crawler-Threads laufen auf vielen Knoten, jeder zuständig für eine Menge von Hosts, und ein Host Splitter gibt URLs an den zuständigen Knoten weiter (Manning et al., 2008, Kap. 20). Der entstehende Index kann nach Termen partitioniert werden, was Mehrwortanfragen und Lastverteilung erschwert, oder häufiger nach Dokumenten, wobei jede Anfrage an alle Knoten geht und globale Statistiken wie idf von Hintergrundprozessen berechnet werden (Manning et al., 2008, Kap. 20).

#### Herkunft und Varianten

Das Design des Crawlers Mercator liegt vielen Forschungs- und kommerziellen Crawlern zugrunde (Manning et al., 2008, Kap. 20). Kontinuierliches Crawlen legt geladene URLs zurück in die Frontier, um sie später zu aktualisieren (Manning et al., 2008, Kap. 20).

### Wann einsetzen

- Um einen Suchindex über Webseiten, ein Intranet oder eine andere Hypertext-Sammlung aufzubauen (Manning et al., 2008, Kap. 20).
- Kontinuierliches Crawlen, wenn der Index mit sich ändernden Seiten aktuell bleiben muss (Manning et al., 2008, Kap. 20).
- Als Extraktionsschritt einer [[data-pipelines|Datenpipeline]], die Web-Dokumente sammelt.

### Stärken und Grenzen

**Stärken**
- Eine einfache Schleife, die durch zusätzliche Maschinen und Bandbreite skaliert (Manning et al., 2008, Kap. 20).
- Priorisierung setzt das Crawl-Budget für nützliche, sich oft ändernde Seiten ein (Manning et al., 2008, Kap. 20).
- Fingerprints und Shingles verhindern, dass derselbe Inhalt zweimal indexiert wird (Manning et al., 2008, Kap. 20).

**Grenzen**
- Spider Traps können unendlich viele Seiten erzeugen (Manning et al., 2008, Kap. 20).
- Höflichkeit begrenzt die Abrufrate pro Host und die Trefferquote des DNS-Caches (Manning et al., 2008, Kap. 20).
- Spam-Seiten, die sich bei jedem Abruf ändern, unterlaufen Heuristiken nach Änderungsrate, wenn nicht auch die Qualität einfließt (Manning et al., 2008, Kap. 20).

### Vergleich

| Komponente | Zweck | Detail |
|------------|-------|--------|
| URL Frontier | Reihenfolge der Abrufe | Front Queues für Priorität, Back Queues für Höflichkeit (Manning et al., 2008, Kap. 20) |
| robots.txt | Regeln der Website beachten | Direkt vor dem Abruf geprüft (Manning et al., 2008, Kap. 20) |
| Inhalts-Fingerprint | Exakte Duplikate | Prüfsumme pro Seite (Manning et al., 2008, Kap. 20) |
| Shingles | Beinahe-Duplikate | Siehe [[near-duplicate-detection\|Near-Duplicate Detection]] |
| Nach Dokumenten partitionierter Index | Anfragen beantworten | Jeder Knoten indexiert eine Teilmenge der Dokumente (Manning et al., 2008, Kap. 20) |

### In der Praxis

Ein Verwaltungs-Thread protokolliert alle paar Sekunden Crawl-Statistiken und sichert die Frontier alle paar Stunden auf die Festplatte, damit ein abgebrochener Crawl vom letzten Checkpoint neu starten kann (Manning et al., 2008, Kap. 20). Eine einfache Partitionierung des Index ordnet alle Seiten eines Hosts einem einzigen Knoten zu (Manning et al., 2008, Kap. 20).

### Merksatz

Ein Crawler arbeitet eine URL Frontier ab, lädt, parst und filtert Seiten; Höflichkeit pro Host, Priorität nach Qualität und Änderungsrate und das Erkennen von Duplikaten machen ihn im Web-Maßstab praktikabel.

### Quellen

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Web crawling and indexes.* Introduction to Information Retrieval, Chapter 20. Cambridge University Press. [stanford.edu](https://nlp.stanford.edu/IR-book/pdf/20crawl.pdf)
