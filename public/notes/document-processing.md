---
title_en: Document Processing (OCR, Layout Analysis and Parsing)
title_de: Dokumentenverarbeitung (OCR, Layoutanalyse und Parsing)
entity_type: Method
aliases:
- Document processing
- Document parsing
- Document AI
- Intelligent document processing
- OCR
- Optical character recognition
- Layout analysis
- Document layout analysis
- Visual document understanding
- Dokumentenverarbeitung
sources:
- https://github.com/tesseract-ocr/tesseract
- https://arxiv.org/abs/2206.01062
- https://arxiv.org/abs/1912.13318
- https://arxiv.org/abs/2111.15664
- https://arxiv.org/abs/2408.09869
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Document processing turns PDFs, scans, forms and office files into structured, machine-readable content: text in reading order, headings, tables, key-value fields and metadata. The classic pipeline runs optical character recognition (OCR) with engines such as Tesseract, detects layout elements such as paragraphs, tables and figures with object-detection models trained on datasets like DocLayNet, and then extracts information with models that combine text and layout, such as LayoutLM (Tesseract; Pfitzmann et al., 2022; Xu et al., 2020). OCR-free models such as Donut read the document image directly and avoid the cost and error propagation of a separate OCR step (Kim et al., 2022). Open-source converters such as Docling bundle layout analysis and table-structure recognition for use in RAG and extraction pipelines (Auer et al., 2024).

### How it works

```text
input: born-digital PDF, scanned image, DOCX, XML, HTML
 ▼
text layer: embedded text, or OCR for scans (Tesseract, LSTM line recognition)
 ▼
layout analysis: detect regions (title, paragraph, table, figure, list, header, footer …)
 ▼
structure: reading order, table structure, section hierarchy
 ▼
understanding / extraction: text + layout (+ image) models, or OCR-free models
 ▼
output: Markdown / JSON / fields → chunking, indexing, information extraction
```

#### 1. Getting the text: born-digital versus scanned

Born-digital PDFs and office files already contain text, although often without reliable reading order or table structure; scans and photos contain only pixels and need OCR. Tesseract is a widely used open-source OCR engine: since version 4 it includes an LSTM-based neural engine that recognises whole text lines, it supports more than 100 languages and can be trained for others, and it outputs plain text, hOCR, searchable PDF, TSV, ALTO and PAGE (Tesseract). Formats such as hOCR and ALTO keep the position of each word, which later steps need. Tesseract was developed at Hewlett-Packard from 1985 to 1994, open-sourced in 2005 and maintained by Google until 2017 (Tesseract).

#### 2. Layout analysis

Layout analysis detects the regions of a page and their type, usually with object-detection models from [[computer-vision|computer vision]]. Training data matters: earlier datasets such as PubLayNet and DocBank come from scientific articles and lack variety, whereas DocLayNet contains 80,863 manually annotated pages from diverse sources with 11 layout classes; models trained on it generalise better, and common detectors still score about 10% below the agreement between human annotators (Pfitzmann et al., 2022). The detected regions determine reading order, exclude page headers and footers from the text, and route tables to a separate table-structure model.

#### 3. Text and layout together

Where something is on a page carries meaning: in a form or invoice, the value next to "Total" or under "Date" is what matters. LayoutLM jointly models text and layout in scanned documents, adding image features for the visual appearance of words; it was the first framework to pre-train text and layout jointly at document level and improved form understanding from 70.72 to 79.27, receipt understanding from 94.02 to 95.24 and document image classification from 93.07 to 94.42 (Xu et al., 2020). Such models feed [[information-extraction|information extraction]] and [[entity-extraction|entity extraction]] from documents.

#### 4. OCR-free document understanding

Pipelines that depend on an external OCR engine have three problems: OCR is computationally expensive, it adapts poorly to new languages or document types, and its errors propagate into later steps (Kim et al., 2022). Donut (Document understanding transformer) is a Transformer that maps the document image directly to the desired output, trained with a cross-entropy objective and pre-trained on synthetic documents to adapt across languages and domains; it reached state-of-the-art speed and accuracy on several visual document understanding tasks (Kim et al., 2022). Multimodal LLMs that read page images follow the same idea, see [[multimodal-models|multimodal models]].

#### 5. Conversion toolkits for LLM pipelines

For RAG and agents, documents are usually converted into Markdown or JSON that preserves headings and tables. Docling is an MIT-licensed, self-contained package for PDF conversion that uses a layout-analysis model trained on DocLayNet and the TableFormer model for table structure and runs efficiently on commodity hardware (Auer et al., 2024). The converted structure then guides [[rag-chunking|chunking]], so that chunks follow sections and tables instead of arbitrary character windows. Hosted parsing services from framework vendors serve the same purpose ([[agent-frameworks|agent frameworks]]).

#### Origin and variants

OCR is the oldest step; open engines such as Tesseract date back to the 1980s (Tesseract). Deep-learning layout analysis and layout-aware language models appeared around 2019–2022 (Xu et al., 2020; Pfitzmann et al., 2022), followed by OCR-free models (Kim et al., 2022) and integrated open-source converters (Auer et al., 2024).

### When to use it

- Building a [[retrieval-augmented-generation|RAG]] system over PDFs, scans or office documents, where text quality and structure determine retrieval quality (Auer et al., 2024).
- Extracting fields from forms, invoices, receipts or contracts (Xu et al., 2020; Kim et al., 2022), as in [[contract-intelligence|contract intelligence]].
- Digitising archives of scanned documents (Tesseract).

### Strengths and limitations

**Strengths**
- Layout-aware models use position and appearance, which pure text models lose (Xu et al., 2020).
- Open engines and converters run locally, which matters for confidential documents (Tesseract; Auer et al., 2024).
- OCR-free models avoid OCR cost and error propagation (Kim et al., 2022).

**Limitations**
- OCR errors on poor scans propagate into every later step (Kim et al., 2022).
- Layout models trained on narrow document types generalise poorly to others (Pfitzmann et al., 2022).
- Even on diverse data, layout detection remains below human agreement (Pfitzmann et al., 2022).

### Comparison

| Approach | Input | Strength | Weakness |
|---|---|---|---|
| Text extraction from born-digital files | PDF text layer, DOCX, XML | exact characters, fast | reading order and tables often lost |
| OCR + layout analysis | scans, images | works on any page | OCR errors, several models to maintain |
| Text + layout models (LayoutLM) | OCR tokens with positions + image | strong on forms and receipts | needs OCR first |
| OCR-free models (Donut) | page image | no OCR step, adaptable | needs task-specific fine-tuning |

Sources: Tesseract; Xu et al. (2020); Kim et al. (2022); Pfitzmann et al. (2022).

### In practice

Quality is checked on a sample of real documents before indexing, since extraction errors are hard to see later in RAG answers ([[rag-failure-modes|RAG failure modes]]). Scanned and born-digital documents are often routed to different paths. For legal documents, keeping section and paragraph numbers intact matters for citations ([[legal-ai|legal AI]]).

### Key takeaway

Document processing combines OCR, layout analysis and layout-aware or OCR-free models to turn PDFs and scans into structured text and fields; its quality sets an upper bound for every RAG or extraction system built on top.

### Sources

- Tesseract. *Tesseract Open Source OCR Engine.* GitHub repository and README. [github.com](https://github.com/tesseract-ocr/tesseract)
- Pfitzmann, B., Auer, C., Dolfi, M., Nassar, A. S. & Staar, P. W. J. (2022). *DocLayNet: A Large Human-Annotated Dataset for Document-Layout Analysis.* KDD 2022. [arXiv](https://arxiv.org/abs/2206.01062)
- Xu, Y., Li, M., Cui, L., Huang, S., Wei, F. & Zhou, M. (2020). *LayoutLM: Pre-training of Text and Layout for Document Image Understanding.* KDD 2020. [arXiv](https://arxiv.org/abs/1912.13318)
- Kim, G., Hong, T., Yim, M., Nam, J., Park, J., Yim, J., Hwang, W., Yun, S., Han, D. & Park, S. (2022). *OCR-free Document Understanding Transformer.* ECCV 2022. [arXiv](https://arxiv.org/abs/2111.15664)
- Auer, C., Lysak, M., Nassar, A. et al. (2024). *Docling Technical Report.* arXiv:2408.09869. [arXiv](https://arxiv.org/abs/2408.09869)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Dokumentenverarbeitung macht aus PDFs, Scans, Formularen und Office-Dateien strukturierte, maschinenlesbare Inhalte: Text in Lesereihenfolge, Überschriften, Tabellen, Schlüssel-Wert-Felder und Metadaten. Die klassische Pipeline führt optische Zeichenerkennung (OCR) mit Engines wie Tesseract aus, erkennt Layoutelemente wie Absätze, Tabellen und Abbildungen mit Modellen zur Objekterkennung, die auf Datensätzen wie DocLayNet trainiert sind, und extrahiert dann Informationen mit Modellen, die Text und Layout verbinden, etwa LayoutLM (Tesseract; Pfitzmann et al., 2022; Xu et al., 2020). OCR-freie Modelle wie Donut lesen das Dokumentbild direkt und vermeiden die Kosten und die Fehlerfortpflanzung eines eigenen OCR-Schritts (Kim et al., 2022). Open-Source-Konverter wie Docling bündeln Layoutanalyse und Tabellenstrukturerkennung für RAG- und Extraktionspipelines (Auer et al., 2024).

### Funktionsweise

```text
Eingabe: digital erzeugtes PDF, gescanntes Bild, DOCX, XML, HTML
 ▼
Textebene: eingebetteter Text oder OCR für Scans (Tesseract, LSTM-Zeilenerkennung)
 ▼
Layoutanalyse: Bereiche erkennen (Titel, Absatz, Tabelle, Abbildung, Liste, Kopf-, Fußzeile …)
 ▼
Struktur: Lesereihenfolge, Tabellenstruktur, Gliederung
 ▼
Verstehen / Extraktion: Modelle für Text + Layout (+ Bild) oder OCR-freie Modelle
 ▼
Ausgabe: Markdown / JSON / Felder → Chunking, Indexierung, Informationsextraktion
```

#### 1. Den Text gewinnen: digital erzeugt oder gescannt

Digital erzeugte PDFs und Office-Dateien enthalten bereits Text, wenn auch oft ohne verlässliche Lesereihenfolge oder Tabellenstruktur; Scans und Fotos enthalten nur Pixel und brauchen OCR. Tesseract ist eine verbreitete Open-Source-OCR-Engine: Seit Version 4 enthält sie eine neuronale LSTM-Engine, die ganze Textzeilen erkennt, sie unterstützt mehr als 100 Sprachen, lässt sich für weitere trainieren und gibt reinen Text, hOCR, durchsuchbares PDF, TSV, ALTO und PAGE aus (Tesseract). Formate wie hOCR und ALTO bewahren die Position jedes Wortes, die spätere Schritte brauchen. Tesseract wurde von 1985 bis 1994 bei Hewlett-Packard entwickelt, 2005 als Open Source veröffentlicht und bis 2017 von Google gepflegt (Tesseract).

#### 2. Layoutanalyse

Die Layoutanalyse erkennt die Bereiche einer Seite und ihren Typ, meist mit Modellen zur Objekterkennung aus der [[computer-vision|Computer Vision]]. Die Trainingsdaten sind entscheidend: Frühere Datensätze wie PubLayNet und DocBank stammen aus wissenschaftlichen Artikeln und sind wenig vielfältig, während DocLayNet 80.863 von Hand annotierte Seiten aus unterschiedlichen Quellen mit 11 Layoutklassen enthält; darauf trainierte Modelle verallgemeinern besser, und verbreitete Detektoren liegen dennoch etwa 10 % unter der Übereinstimmung menschlicher Annotierender (Pfitzmann et al., 2022). Die erkannten Bereiche bestimmen die Lesereihenfolge, nehmen Kopf- und Fußzeilen aus dem Text heraus und leiten Tabellen an ein eigenes Modell für die Tabellenstruktur weiter.

#### 3. Text und Layout gemeinsam

Wo etwas auf einer Seite steht, trägt Bedeutung: In einem Formular oder einer Rechnung zählt der Wert neben „Summe“ oder unter „Datum“. LayoutLM modelliert Text und Layout in gescannten Dokumenten gemeinsam und ergänzt Bildmerkmale für das Aussehen der Wörter; es war das erste Framework, das Text und Layout auf Dokumentebene gemeinsam vortrainierte, und verbesserte das Formularverständnis von 70,72 auf 79,27, das Belegverständnis von 94,02 auf 95,24 und die [[classification|Klassifikation]] von Dokumentbildern von 93,07 auf 94,42 (Xu et al., 2020). Solche Modelle speisen [[information-extraction|Informationsextraktion]] und [[entity-extraction|Entitätsextraktion]] aus Dokumenten.

#### 4. OCR-freies Dokumentverstehen

Pipelines, die von einer externen OCR-Engine abhängen, haben drei Probleme: OCR ist rechenaufwendig, passt sich schlecht an neue Sprachen oder Dokumenttypen an, und ihre Fehler pflanzen sich in spätere Schritte fort (Kim et al., 2022). Donut (Document understanding transformer) ist ein Transformer, der das Dokumentbild direkt auf die gewünschte Ausgabe abbildet, mit Cross-Entropy trainiert und auf synthetischen Dokumenten vortrainiert, um sich an Sprachen und Domänen anzupassen; es erreichte bei mehreren Aufgaben des visuellen Dokumentverstehens Bestwerte bei Geschwindigkeit und Genauigkeit (Kim et al., 2022). Multimodale LLMs, die Seitenbilder lesen, folgen derselben Idee, siehe [[multimodal-models|multimodale Modelle]].

#### 5. Konvertierungswerkzeuge für LLM-Pipelines

Für RAG und Agenten werden Dokumente meist in Markdown oder JSON umgewandelt, das Überschriften und Tabellen erhält. Docling ist ein MIT-lizenziertes, eigenständiges Paket zur PDF-Konvertierung, das ein auf DocLayNet trainiertes Modell zur Layoutanalyse und das Modell TableFormer für die Tabellenstruktur nutzt und effizient auf Standardhardware läuft (Auer et al., 2024). Die gewonnene Struktur steuert dann das [[rag-chunking|Chunking]], sodass Chunks Abschnitten und Tabellen folgen statt beliebigen Zeichenfenstern. Gehostete Parsing-Dienste von Framework-Anbietern dienen demselben Zweck ([[agent-frameworks|Agent-Frameworks]]).

#### Herkunft und Varianten

OCR ist der älteste Schritt; offene Engines wie Tesseract reichen bis in die 1980er-Jahre zurück (Tesseract). Layoutanalyse mit Deep Learning und layoutbewusste Sprachmodelle entstanden um 2019 bis 2022 (Xu et al., 2020; Pfitzmann et al., 2022), gefolgt von OCR-freien Modellen (Kim et al., 2022) und integrierten Open-Source-Konvertern (Auer et al., 2024).

### Wann einsetzen

- Beim Aufbau eines [[retrieval-augmented-generation|RAG]]-Systems über PDFs, Scans oder Office-Dokumente, bei dem Textqualität und Struktur die Retrieval-Qualität bestimmen (Auer et al., 2024).
- Beim Extrahieren von Feldern aus Formularen, Rechnungen, Belegen oder Verträgen (Xu et al., 2020; Kim et al., 2022), wie bei [[contract-intelligence|Contract Intelligence]].
- Beim Digitalisieren von Archiven gescannter Dokumente (Tesseract).

### Stärken und Grenzen

**Stärken**
- Layoutbewusste Modelle nutzen Position und Erscheinungsbild, die reinen Textmodellen verloren gehen (Xu et al., 2020).
- Offene Engines und Konverter laufen lokal, was bei vertraulichen Dokumenten wichtig ist (Tesseract; Auer et al., 2024).
- OCR-freie Modelle vermeiden OCR-Kosten und Fehlerfortpflanzung (Kim et al., 2022).

**Grenzen**
- OCR-Fehler bei schlechten Scans pflanzen sich in jeden weiteren Schritt fort (Kim et al., 2022).
- Layoutmodelle, die auf engen Dokumenttypen trainiert sind, verallgemeinern schlecht auf andere (Pfitzmann et al., 2022).
- Selbst auf vielfältigen Daten bleibt die Layouterkennung unter der menschlichen Übereinstimmung (Pfitzmann et al., 2022).

### Vergleich

| Ansatz | Eingabe | Stärke | Schwäche |
|---|---|---|---|
| Textextraktion aus digital erzeugten Dateien | PDF-Textebene, DOCX, XML | exakte Zeichen, schnell | Lesereihenfolge und Tabellen gehen oft verloren |
| OCR + Layoutanalyse | Scans, Bilder | funktioniert auf jeder Seite | OCR-Fehler, mehrere Modelle zu pflegen |
| Modelle für Text + Layout (LayoutLM) | OCR-Token mit Positionen + Bild | stark bei Formularen und Belegen | braucht vorher OCR |
| OCR-freie Modelle (Donut) | Seitenbild | kein OCR-Schritt, anpassbar | braucht aufgabenspezifisches Fine-Tuning |

Quellen: Tesseract; Xu et al. (2020); Kim et al. (2022); Pfitzmann et al. (2022).

### In der Praxis

Die Qualität wird vor dem Indexieren an einer Stichprobe echter Dokumente geprüft, weil Extraktionsfehler später in RAG-Antworten schwer zu erkennen sind ([[rag-failure-modes|RAG: Fehlerbilder]]). Gescannte und digital erzeugte Dokumente werden oft auf getrennte Wege geleitet. Bei juristischen Dokumenten ist es für Zitate wichtig, Paragraphen- und Absatznummern zu erhalten ([[legal-ai|Legal AI]]).

### Merksatz

Dokumentenverarbeitung verbindet OCR, Layoutanalyse und layoutbewusste oder OCR-freie Modelle, um aus PDFs und Scans strukturierten Text und Felder zu machen; ihre Qualität setzt die Obergrenze für jedes RAG- oder Extraktionssystem, das darauf aufbaut.

### Quellen

- Tesseract. *Tesseract Open Source OCR Engine.* GitHub-Repository und README. [github.com](https://github.com/tesseract-ocr/tesseract)
- Pfitzmann, B., Auer, C., Dolfi, M., Nassar, A. S. & Staar, P. W. J. (2022). *DocLayNet: A Large Human-Annotated Dataset for Document-Layout Analysis.* KDD 2022. [arXiv](https://arxiv.org/abs/2206.01062)
- Xu, Y., Li, M., Cui, L., Huang, S., Wei, F. & Zhou, M. (2020). *LayoutLM: Pre-training of Text and Layout for Document Image Understanding.* KDD 2020. [arXiv](https://arxiv.org/abs/1912.13318)
- Kim, G., Hong, T., Yim, M., Nam, J., Park, J., Yim, J., Hwang, W., Yun, S., Han, D. & Park, S. (2022). *OCR-free Document Understanding Transformer.* ECCV 2022. [arXiv](https://arxiv.org/abs/2111.15664)
- Auer, C., Lysak, M., Nassar, A. et al. (2024). *Docling Technical Report.* arXiv:2408.09869. [arXiv](https://arxiv.org/abs/2408.09869)
