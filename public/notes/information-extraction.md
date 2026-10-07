---
title_en: Information Extraction
title_de: Informationsextraktion
entity_type: Method
sources:
- https://www.ijcai.org/Proceedings/07/Papers/429.pdf
- https://aclanthology.org/2021.findings-emnlp.204/
- https://arxiv.org/abs/2312.17617
- https://arxiv.org/abs/1603.01360
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Information extraction (IE) turns unstructured text into structured knowledge such as entities, relations and events (Xu et al., 2023). It ranges from extracting a predefined schema to open extraction of arbitrary relation tuples from the web (Banko et al., 2007), and is increasingly done by generating the structure directly with sequence-to-sequence models (Huguet Cabot & Navigli, 2021) or large language models (Xu et al., 2023). The results feed applications such as [[knowledge-graphs|Knowledge Graphs]] and [[contract-intelligence|Contract Intelligence]].

### How it works

Entities are identified first, because they are the arguments that relations connect. Relations between them are then extracted, either as open tuples with free relation phrases or as triplets with relation types from a fixed inventory, and the results are stored in a structured form.

```text
1. Entities as building blocks
▼
2. Open information extraction
▼
3. Relation extraction as generation
▼
4. Generative IE with large language models
```

#### 1. Entities as building blocks

Relations connect entities, so entity recognition is usually the first step ([[entity-extraction|Entity Extraction]]). Lample et al. (2016) showed that neural architectures, a bidirectional LSTM with a conditional random field and a transition-based model, reach state-of-the-art entity recognition in four languages without hand-crafted features or gazetteers, using character-based word representations and word representations learned from unannotated text.

#### 2. Open information extraction

Classical relation extraction targets a predefined set of relations and needs labelled examples for each of them. Open information extraction (Banko et al., 2007) drops this restriction: the system TextRunner extracts relational tuples of the form (argument, relation phrase, argument) from web text, in a single pass over the corpus and without hand-labelled examples for each relation. The relation is expressed by a phrase from the text, not by a type from a schema, so the extractions cover relations nobody specified in advance.

#### 3. Relation extraction as generation

REBEL (Huguet Cabot & Navigli, 2021) treats relation extraction as sequence-to-sequence generation. A BART-based model reads a text and generates the relation triplets expressed in it as a linearised sequence, covering more than 200 relation types. Entities and relations are produced together in one step instead of by separate components. The model was evaluated on several relation extraction benchmarks.

#### 4. Generative IE with large language models

Generative large language models have strong text understanding and generation capabilities, and many recent works use them for IE in a generative paradigm (Xu et al., 2023). Their survey categorises these works by IE subtask, such as named entity recognition, relation extraction and event extraction, and by technique, empirically analyses the most advanced methods and identifies emerging trends and open research directions. In practice, the desired output structure is usually described in the prompt ([[prompt-engineering|Prompt Engineering]]).

#### Origin and variants

Open IE (Banko et al., 2007) extracted relation tuples from the web without a fixed schema. Neural entity recognition (Lample et al., 2016) replaced hand-crafted features, REBEL (Huguet Cabot & Navigli, 2021) generated relation triplets end to end, and LLM-based generative IE (Xu et al., 2023) extends the generative approach to many IE subtasks.

### When to use it

- When relations of interest are not known in advance and a broad overview of a large text collection is needed, open IE avoids defining a schema first (Banko et al., 2007).
- When relations from a fixed inventory are needed, for example to populate a knowledge graph, generative relation extraction produces typed triplets (Huguet Cabot & Navigli, 2021).
- When extraction tasks change often or labelled data is scarce, LLM-based generative IE can be adapted through the prompt (Xu et al., 2023).

### Strengths and limitations

**Strengths**
- Open IE needs no hand-labelled examples per relation and processes a corpus in a single pass (Banko et al., 2007).
- Generative relation extraction covers more than 200 relation types with one model (Huguet Cabot & Navigli, 2021).
- Neural entity recognition works without hand-crafted features or gazetteers (Lample et al., 2016).

**Limitations**
- Open IE relation phrases are not mapped to a schema, so the same relation can appear under different phrases (Banko et al., 2007).
- Typed relation extraction only finds relations from its inventory (Huguet Cabot & Navigli, 2021).
- LLM-based IE is an active research area with open problems that the survey identifies (Xu et al., 2023).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Open IE (TextRunner) | Free relation phrases, no schema, no labelled examples per relation (Banko et al., 2007) | Broad exploration of large text collections |
| Generative relation extraction (REBEL) | Typed triplets from a fixed inventory, generated by a fine-tuned seq2seq model (Huguet Cabot & Navigli, 2021) | Populating a schema or knowledge graph |
| LLM-based generative IE | Structure described in the prompt, many subtasks with one model (Xu et al., 2023) | Changing tasks, little labelled data |

### In practice

Extraction quality is measured with precision, recall and F1 against annotated data, separately for entities and relations. The target structure should be defined first, for example as an ontology ([[ontology-design|Ontology Design]]), so that extracted entities and relations can be linked and stored consistently ([[knowledge-graphs|Knowledge Graphs]]). With LLMs, the output format and the allowed types are given in the prompt and the output is validated against the schema before it is stored.

### Key takeaway

Information extraction turns text into entities, relations and events, either openly without a schema or into a fixed schema, and is increasingly done by generating the structure directly.

### Sources

- Banko, M., Cafarella, M. J., Soderland, S., Broadhead, M. & Etzioni, O. (2007). *Open Information Extraction from the Web.* IJCAI 2007. [PDF](https://www.ijcai.org/Proceedings/07/Papers/429.pdf)
- Huguet Cabot, P.-L. & Navigli, R. (2021). *REBEL: Relation Extraction By End-to-end Language generation.* Findings of EMNLP 2021. [ACL Anthology](https://aclanthology.org/2021.findings-emnlp.204/)
- Xu, D. et al. (2023). *Large Language Models for Generative Information Extraction: A Survey.* [arXiv:2312.17617](https://arxiv.org/abs/2312.17617)
- Lample, G. et al. (2016). *Neural Architectures for Named Entity Recognition.* NAACL 2016. [arXiv:1603.01360](https://arxiv.org/abs/1603.01360)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Informationsextraktion (IE) überführt unstrukturierten Text in strukturiertes Wissen wie Entitäten, Relationen und Ereignisse (Xu et al., 2023). Sie reicht von der Extraktion nach einem vorgegebenen Schema bis zur offenen Extraktion beliebiger Relationstupel aus dem Web (Banko et al., 2007) und erfolgt zunehmend, indem die Struktur direkt mit Sequence-to-Sequence-Modellen (Huguet Cabot & Navigli, 2021) oder großen Sprachmodellen (Xu et al., 2023) erzeugt wird. Die Ergebnisse speisen Anwendungen wie [[knowledge-graphs|Wissensgraphen]] und [[contract-intelligence|Contract Intelligence]].

### Funktionsweise

Zuerst werden Entitäten erkannt, denn sie sind die Argumente, die Relationen verbinden. Dann werden die Relationen zwischen ihnen extrahiert, entweder als offene Tupel mit frei formulierten Relationsphrasen oder als Tripel mit Relationstypen aus einem festen Inventar, und die Ergebnisse werden strukturiert gespeichert.

```text
1. Entitäten als Bausteine
▼
2. Offene Informationsextraktion
▼
3. Relationsextraktion als Generierung
▼
4. Generative IE mit großen Sprachmodellen
```

#### 1. Entitäten als Bausteine

Relationen verbinden Entitäten, daher ist die Entitätserkennung meist der erste Schritt ([[entity-extraction|Entitätsextraktion]]). Lample et al. (2016) zeigten, dass neuronale Architekturen, ein bidirektionales LSTM mit Conditional Random Field und ein transitionsbasiertes Modell, in vier Sprachen den Stand der Technik bei der Entitätserkennung erreichen, ohne handgefertigte Merkmale oder Gazetteers. Sie nutzen zeichenbasierte Wortrepräsentationen und Wortrepräsentationen, die aus nicht annotiertem Text gelernt wurden.

#### 2. Offene Informationsextraktion

Klassische Relationsextraktion zielt auf eine vorgegebene Menge von Relationen und braucht für jede davon annotierte Beispiele. Offene Informationsextraktion (Banko et al., 2007) hebt diese Beschränkung auf: Das System TextRunner extrahiert Relationstupel der Form (Argument, Relationsphrase, Argument) aus Webtext, in einem einzigen Durchlauf über das Korpus und ohne manuell annotierte Beispiele für jede Relation. Die Relation wird durch eine Phrase aus dem Text ausgedrückt, nicht durch einen Typ aus einem Schema, sodass die Extraktionen auch Relationen abdecken, die niemand vorab festgelegt hat.

#### 3. Relationsextraktion als Generierung

REBEL (Huguet Cabot & Navigli, 2021) behandelt Relationsextraktion als Sequence-to-Sequence-Generierung. Ein BART-basiertes Modell liest einen Text und erzeugt die darin ausgedrückten Relationstripel als linearisierte Sequenz; abgedeckt sind mehr als 200 Relationstypen. Entitäten und Relationen entstehen gemeinsam in einem Schritt statt in getrennten Komponenten. Das Modell wurde auf mehreren Benchmarks zur Relationsextraktion evaluiert.

#### 4. Generative IE mit großen Sprachmodellen

Generative große Sprachmodelle verfügen über ausgeprägte Fähigkeiten im Verstehen und Erzeugen von Text, und viele neuere Arbeiten setzen sie im generativen Paradigma für IE ein (Xu et al., 2023). Deren Übersichtsarbeit ordnet diese Arbeiten nach IE-Teilaufgaben wie Named Entity Recognition, Relationsextraktion und Ereignisextraktion sowie nach Techniken, analysiert die fortgeschrittensten Methoden empirisch und benennt Trends und offene Forschungsfragen. In der Praxis wird die gewünschte Ausgabestruktur meist im Prompt beschrieben ([[prompt-engineering|Prompt Engineering]]).

#### Ursprung und Varianten

Open IE (Banko et al., 2007) extrahierte Relationstupel aus dem Web ohne festes Schema. Neuronale Entitätserkennung (Lample et al., 2016) löste handgefertigte Merkmale ab, REBEL (Huguet Cabot & Navigli, 2021) erzeugte Relationstripel durchgängig in einem Modell, und LLM-basierte generative IE (Xu et al., 2023) überträgt den generativen Ansatz auf viele IE-Teilaufgaben.

### Wann einsetzen

- Wenn die relevanten Relationen vorab nicht bekannt sind und ein breiter Überblick über eine große Textsammlung gebraucht wird, erspart Open IE das vorherige Definieren eines Schemas (Banko et al., 2007).
- Wenn Relationen aus einem festen Inventar benötigt werden, etwa zum Befüllen eines Wissensgraphen, liefert generative Relationsextraktion typisierte Tripel (Huguet Cabot & Navigli, 2021).
- Wenn sich Extraktionsaufgaben oft ändern oder annotierte Daten knapp sind, lässt sich LLM-basierte generative IE über den Prompt anpassen (Xu et al., 2023).

### Stärken und Grenzen

**Stärken**
- Open IE braucht keine manuell annotierten Beispiele pro Relation und verarbeitet ein Korpus in einem Durchlauf (Banko et al., 2007).
- Generative Relationsextraktion deckt mit einem Modell mehr als 200 Relationstypen ab (Huguet Cabot & Navigli, 2021).
- Neuronale Entitätserkennung kommt ohne handgefertigte Merkmale oder Gazetteers aus (Lample et al., 2016).

**Einschränkungen**
- Relationsphrasen aus Open IE werden keinem Schema zugeordnet, sodass dieselbe Relation unter verschiedenen Phrasen auftreten kann (Banko et al., 2007).
- Typisierte Relationsextraktion findet nur Relationen aus ihrem Inventar (Huguet Cabot & Navigli, 2021).
- LLM-basierte IE ist ein aktives Forschungsfeld mit offenen Problemen, die die Übersichtsarbeit benennt (Xu et al., 2023).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Open IE (TextRunner) | Freie Relationsphrasen, kein Schema, keine annotierten Beispiele pro Relation (Banko et al., 2007) | Breite Exploration großer Textsammlungen |
| Generative Relationsextraktion (REBEL) | Typisierte Tripel aus einem festen Inventar, erzeugt von einem feinabgestimmten Seq2Seq-Modell (Huguet Cabot & Navigli, 2021) | Befüllen eines Schemas oder Wissensgraphen |
| LLM-basierte generative IE | Struktur im Prompt beschrieben, viele Teilaufgaben mit einem Modell (Xu et al., 2023) | Wechselnde Aufgaben, wenige annotierte Daten |

### In der Praxis

Die Extraktionsqualität wird mit Precision, Recall und F1 gegen annotierte Daten gemessen, getrennt für Entitäten und Relationen. Die Zielstruktur sollte vorab festgelegt werden, etwa als Ontologie ([[ontology-design|Ontologie-Design]]), damit extrahierte Entitäten und Relationen konsistent verknüpft und gespeichert werden können ([[knowledge-graphs|Wissensgraphen]]). Bei LLMs werden Ausgabeformat und zulässige Typen im Prompt vorgegeben, und die Ausgabe wird vor dem Speichern gegen das Schema validiert.

### Merksatz

Informationsextraktion überführt Text in Entitäten, Relationen und Ereignisse, entweder offen ohne Schema oder in ein festes Schema, und erzeugt die Struktur zunehmend direkt.

### Quellen

- Banko, M., Cafarella, M. J., Soderland, S., Broadhead, M. & Etzioni, O. (2007). *Open Information Extraction from the Web.* IJCAI 2007. [PDF](https://www.ijcai.org/Proceedings/07/Papers/429.pdf)
- Huguet Cabot, P.-L. & Navigli, R. (2021). *REBEL: Relation Extraction By End-to-end Language generation.* Findings of EMNLP 2021. [ACL Anthology](https://aclanthology.org/2021.findings-emnlp.204/)
- Xu, D. et al. (2023). *Large Language Models for Generative Information Extraction: A Survey.* [arXiv:2312.17617](https://arxiv.org/abs/2312.17617)
- Lample, G. et al. (2016). *Neural Architectures for Named Entity Recognition.* NAACL 2016. [arXiv:1603.01360](https://arxiv.org/abs/1603.01360)
