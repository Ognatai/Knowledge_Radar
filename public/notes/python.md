---
title_en: Python
title_de: Python
entity_type: Technology
sources:
- https://docs.python.org/3/tutorial/index.html
- https://docs.python.org/3/library/collections.html
- https://docs.python.org/3/library/venv.html
- https://peps.python.org/pep-0008/
- https://doi.org/10.1038/s41586-020-2649-2
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Python is an easy-to-learn, interpreted programming language with dynamic typing, efficient high-level data structures and a simple approach to object-oriented programming, which makes it the standard language for data science and machine learning (Python Tutorial). Its standard library offers specialised containers such as Counter and defaultdict (Python collections docs), projects isolate their dependencies in virtual environments (Python venv docs), PEP 8 defines the common code style (PEP 8), and NumPy forms the foundation of the scientific Python ecosystem (Harris et al., 2020).

### Core concepts

- **Syntax and typing:** Blocks are defined by indentation, and variables are dynamically typed; the interpreter runs code directly, which suits scripting and rapid development (Python Tutorial).
- **Data structures:** Lists (mutable sequences), tuples (immutable), sets (unique elements) and dictionaries (key-value mappings) are built in; strings are immutable and support slicing and f-strings; list comprehensions build lists concisely (Python Tutorial).
- **Functions and errors:** Functions support default and keyword arguments; errors are exceptions that are handled with try/except/else/finally and raised with raise (Python Tutorial).
- **Classes:** Classes bundle data and functionality; instances hold attributes and methods, and inheritance, including multiple base classes, lets derived classes override methods (Python Tutorial).
- **Iterators and generators:** Generators use yield to produce values lazily one at a time, which saves memory for large or infinite sequences (Python Tutorial).
- **collections:** namedtuple, deque (fast appends and pops on both ends), Counter (counting hashable objects), OrderedDict, defaultdict (default values for missing keys) and ChainMap complement the built-in containers (Python collections docs).
- **Virtual environments:** venv creates isolated environments with their own installed packages on top of a base Python installation (Python venv docs).

### Common usage

```python
from collections import Counter, defaultdict

words = ["norm", "court", "norm", "party"]
counts = Counter(words)                # Counter({'norm': 2, 'court': 1, 'party': 1})
by_letter = defaultdict(list)
for w in words:
    by_letter[w[0]].append(w)          # no KeyError for new keys

def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:                 # generator: one line at a time
            yield line.rstrip("\n")

try:
    value = int("42")
except ValueError as error:
    print(f"not a number: {error}")
```

A project typically starts with python -m venv .venv, activates the environment and installs packages with pip (Python venv docs). For data science, NumPy provides vectorised array operations, broadcasting and indexing on which libraries such as pandas and scikit-learn build (Harris et al., 2020; [[classical-machine-learning|Classical Machine Learning Methods]]).

### When to use it

- For data analysis, machine learning and scientific computing, thanks to NumPy and the ecosystem built on it (Harris et al., 2020).
- For scripting, automation and rapid prototyping (Python Tutorial).
- When performance-critical inner loops are needed, vectorised NumPy operations or compiled extensions should replace pure Python loops (Harris et al., 2020).

### Strengths and limitations

**Strengths**
- Easy to learn, with readable syntax and powerful built-in data structures (Python Tutorial).
- Extensive standard library, including specialised containers (Python collections docs).
- The foundation of the scientific and ML ecosystem (Harris et al., 2020).

**Limitations**
- Dynamic typing finds type errors only at run time (Python Tutorial).
- Without virtual environments, package versions of different projects conflict (Python venv docs).
- Pure Python loops are slow compared with vectorised array operations (Harris et al., 2020).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Built-in containers | list, tuple, set, dict (Python Tutorial) | General-purpose data handling |
| collections | Specialised containers such as Counter and deque (Python collections docs) | Counting, queues, default values |
| NumPy arrays | Homogeneous, vectorised arrays (Harris et al., 2020) | Numerical computing |

### In practice

Code follows PEP 8: 4-space indentation, imports at the top grouped into standard library, third-party and local modules, lowercase_with_underscores for functions and variables, CapWords for classes and UPPER_CASE for constants (PEP 8). Each project gets its own virtual environment and a pinned list of dependencies, and version control tracks the code but not the environment ([[git|Git]]). Readable code beyond the style guide is the subject of [[clean-code|Clean Code]], and web services built with Python expose [[apis|APIs]].

### Key takeaway

Python combines readable syntax and rich built-in data structures with virtual environments and NumPy, which makes it the default language for data and ML work.

### Sources

- Python Software Foundation. *The Python Tutorial.* Python 3 documentation. [docs.python.org](https://docs.python.org/3/tutorial/index.html)
- Python Software Foundation. *collections — Container datatypes.* Python 3 documentation. [docs.python.org](https://docs.python.org/3/library/collections.html)
- Python Software Foundation. *venv — Creation of virtual environments.* Python 3 documentation. [docs.python.org](https://docs.python.org/3/library/venv.html)
- van Rossum, G., Warsaw, B. & Coghlan, A. (2001). *PEP 8 – Style Guide for Python Code.* Python Enhancement Proposal. [peps.python.org](https://peps.python.org/pep-0008/)
- Harris, C. R., Millman, K. J., van der Walt, S. J. et al. (2020). *Array programming with NumPy.* Nature 585. [doi:10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Python ist eine leicht erlernbare, interpretierte Programmiersprache mit dynamischer Typisierung, effizienten High-Level-Datenstrukturen und einem einfachen Ansatz zur objektorientierten Programmierung; dadurch ist sie die Standardsprache für Data Science und maschinelles Lernen (Python Tutorial). Die Standardbibliothek bietet spezialisierte Container wie Counter und defaultdict (Python collections docs), Projekte isolieren ihre Abhängigkeiten in virtuellen Umgebungen (Python venv docs), PEP 8 legt den gemeinsamen Codestil fest (PEP 8), und NumPy bildet die Grundlage des wissenschaftlichen Python-Ökosystems (Harris et al., 2020).

### Kernkonzepte

- **Syntax und Typisierung:** Blöcke werden durch Einrückung festgelegt, und Variablen sind dynamisch typisiert; der Interpreter führt Code direkt aus, was Skripting und schnelle Entwicklung begünstigt (Python Tutorial).
- **Datenstrukturen:** Listen (veränderliche Sequenzen), Tupel (unveränderlich), Mengen (eindeutige Elemente) und Dictionaries (Schlüssel-Wert-Zuordnungen) sind eingebaut; Strings sind unveränderlich und unterstützen Slicing und f-Strings; List Comprehensions bilden Listen kompakt (Python Tutorial).
- **Funktionen und Fehler:** Funktionen unterstützen Standard- und Schlüsselwortargumente; Fehler sind Ausnahmen, die mit try/except/else/finally behandelt und mit raise ausgelöst werden (Python Tutorial).
- **Klassen:** Klassen bündeln Daten und Funktionalität; Instanzen tragen Attribute und Methoden, und Vererbung, auch von mehreren Basisklassen, erlaubt abgeleiteten Klassen, Methoden zu überschreiben (Python Tutorial).
- **Iteratoren und Generatoren:** Generatoren erzeugen mit yield Werte bedarfsgesteuert einzeln, was bei großen oder unendlichen Folgen Speicher spart (Python Tutorial).
- **collections:** namedtuple, deque (schnelles Anfügen und Entfernen an beiden Enden), Counter (Zählen hashbarer Objekte), OrderedDict, defaultdict (Standardwerte für fehlende Schlüssel) und ChainMap ergänzen die eingebauten Container (Python collections docs).
- **Virtuelle Umgebungen:** venv erzeugt isolierte Umgebungen mit eigenen installierten Paketen auf Basis einer Python-Grundinstallation (Python venv docs).

### Typische Verwendung

```python
from collections import Counter, defaultdict

words = ["norm", "court", "norm", "party"]
counts = Counter(words)                # Counter({'norm': 2, 'court': 1, 'party': 1})
by_letter = defaultdict(list)
for w in words:
    by_letter[w[0]].append(w)          # kein KeyError bei neuen Schlüsseln

def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:                 # Generator: eine Zeile nach der anderen
            yield line.rstrip("\n")

try:
    value = int("42")
except ValueError as error:
    print(f"keine Zahl: {error}")
```

Ein Projekt beginnt typischerweise mit python -m venv .venv, aktiviert die Umgebung und installiert Pakete mit pip (Python venv docs). Für Data Science stellt NumPy vektorisierte Array-Operationen, Broadcasting und Indexierung bereit, auf denen Bibliotheken wie pandas und scikit-learn aufbauen (Harris et al., 2020; [[classical-machine-learning|Klassische ML-Verfahren]]).

### Wann einsetzen

- Für Datenanalyse, maschinelles Lernen und wissenschaftliches Rechnen, dank NumPy und des darauf aufbauenden Ökosystems (Harris et al., 2020).
- Für Skripte, Automatisierung und schnelles Prototyping (Python Tutorial).
- Wenn leistungskritische innere Schleifen nötig sind, sollten vektorisierte NumPy-Operationen oder kompilierte Erweiterungen reine Python-Schleifen ersetzen (Harris et al., 2020).

### Stärken und Grenzen

**Stärken**
- Leicht zu lernen, mit lesbarer Syntax und leistungsfähigen eingebauten Datenstrukturen (Python Tutorial).
- Umfangreiche Standardbibliothek einschließlich spezialisierter Container (Python collections docs).
- Grundlage des wissenschaftlichen und ML-Ökosystems (Harris et al., 2020).

**Einschränkungen**
- Dynamische Typisierung findet Typfehler erst zur Laufzeit (Python Tutorial).
- Ohne virtuelle Umgebungen geraten die Paketversionen verschiedener Projekte in Konflikt (Python venv docs).
- Reine Python-Schleifen sind langsam im Vergleich zu vektorisierten Array-Operationen (Harris et al., 2020).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Eingebaute Container | list, tuple, set, dict (Python Tutorial) | Allgemeine Datenverarbeitung |
| collections | Spezialisierte Container wie Counter und deque (Python collections docs) | Zählen, Warteschlangen, Standardwerte |
| NumPy-Arrays | Homogene, vektorisierte Arrays (Harris et al., 2020) | Numerisches Rechnen |

### In der Praxis

Code folgt PEP 8: Einrückung mit 4 Leerzeichen, Importe am Dateianfang, gruppiert nach Standardbibliothek, Drittanbietern und lokalen Modulen, lowercase_with_underscores für Funktionen und Variablen, CapWords für Klassen und UPPER_CASE für Konstanten (PEP 8). Jedes Projekt erhält eine eigene virtuelle Umgebung und eine festgelegte Liste von Abhängigkeiten, und die Versionsverwaltung erfasst den Code, nicht aber die Umgebung ([[git|Git]]). Lesbarer Code über den Styleguide hinaus ist Thema von [[clean-code|Clean Code]], und mit Python gebaute Webdienste stellen [[apis|APIs (Programmierschnittstellen)]] bereit.

### Merksatz

Python verbindet lesbare Syntax und reichhaltige eingebaute Datenstrukturen mit virtuellen Umgebungen und NumPy und ist dadurch die Standardsprache für Daten- und ML-Arbeit.

### Quellen

- Python Software Foundation. *The Python Tutorial.* Python 3 documentation. [docs.python.org](https://docs.python.org/3/tutorial/index.html)
- Python Software Foundation. *collections — Container datatypes.* Python 3 documentation. [docs.python.org](https://docs.python.org/3/library/collections.html)
- Python Software Foundation. *venv — Creation of virtual environments.* Python 3 documentation. [docs.python.org](https://docs.python.org/3/library/venv.html)
- van Rossum, G., Warsaw, B. & Coghlan, A. (2001). *PEP 8 – Style Guide for Python Code.* Python Enhancement Proposal. [peps.python.org](https://peps.python.org/pep-0008/)
- Harris, C. R., Millman, K. J., van der Walt, S. J. et al. (2020). *Array programming with NumPy.* Nature 585. [doi:10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2)
