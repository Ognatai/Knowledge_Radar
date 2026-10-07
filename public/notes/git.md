---
title_en: Git
title_de: Git
entity_type: Technology
sources:
- https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F
- https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell
- https://git-scm.com/docs/gitignore
- https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
---

## EN

> **Note:** LLM-generated summary based on the listed sources; it may be incomplete, outdated or wrong.

### TL;DR

Git is a distributed version control system that stores a project's history as a series of snapshots; every clone contains the full history, so nearly all operations are local and fast (Pro Git). Changes move through three states, modified, staged and committed, and branches are lightweight pointers to commits that make parallel work and merging cheap (Pro Git branching). A .gitignore file keeps untracked files out of the repository (gitignore docs), and SSH keys authenticate pushes to hosting services such as GitHub (GitHub SSH docs).

### Core concepts

- **Snapshots:** Git thinks of its data as snapshots of the whole project rather than lists of file changes; content is checksummed, so changes cannot go unnoticed (Pro Git).
- **Three states:** Files are modified (changed but not committed), staged (marked for the next commit) or committed (stored in the repository), corresponding to the working tree, the staging area and the repository (Pro Git).
- **Local and distributed:** Each clone holds the complete history, and remotes are synchronised with fetch, pull and push (Pro Git).
- **Branches:** A branch is a lightweight movable pointer to a commit, and HEAD points to the current branch; merging combines diverging histories, by fast-forward or with a merge commit, and conflicting edits must be resolved by hand (Pro Git branching).
- **.gitignore:** Each line is a pattern for intentionally untracked files; ! negates a pattern, a trailing slash matches only directories, and files that are already tracked are not affected (gitignore docs).
- **SSH authentication:** A key pair generated with ssh-keygen authenticates the machine to the hosting service; the ssh-agent remembers the passphrase (GitHub SSH docs).

### Common usage

```bash
git clone git@github.com:org/repo.git      # copy a repository with full history
git switch -c feature/notes               # create and switch to a new branch
git status                                 # see modified and staged files
git add notes/new.md                       # stage changes
git commit -m "Add new note"               # record a snapshot
git pull --rebase                          # update with remote changes
git push -u origin feature/notes           # publish the branch
git restore notes/draft.md                 # discard unstaged changes in a file
git revert <commit>                        # undo a commit with a new commit

ssh-keygen -t ed25519 -C "you@example.com" # create an SSH key for GitHub
```

Undo operations differ in how far they reach: restore discards changes in the working tree, reset moves the branch pointer (and can discard commits), and revert creates a new commit that undoes an earlier one, which is safe for shared history (Pro Git).

### When to use it

- For any code, configuration or text project whose history should be tracked and shared (Pro Git).
- When several people work in parallel, using branches and merges (Pro Git branching).
- Large binary files and generated artefacts belong in .gitignore or specialised storage rather than in the repository (gitignore docs).

### Strengths and limitations

**Strengths**
- Full local history makes operations fast and work possible offline (Pro Git).
- Cheap branches support parallel work and experiments (Pro Git branching).
- Checksums protect the integrity of the history (Pro Git).

**Limitations**
- Concurrent edits to the same lines produce merge conflicts that must be resolved manually (Pro Git branching).
- Files that are already tracked are not affected by later .gitignore rules (gitignore docs).
- Rewriting shared history, for example with reset or rebase, can disrupt collaborators (Pro Git).

### Comparison

| Approach | How it differs | Suited for |
|----------|----------------|------------|
| Merge | Combines histories, keeps the branch structure (Pro Git branching) | Shared branches |
| Rebase | Replays commits on a new base for a linear history (Pro Git) | Local branches before publishing |
| HTTPS remote | Authenticates with credentials or tokens | Occasional access |
| SSH remote | Authenticates with a key pair (GitHub SSH docs) | Regular pushes from a trusted machine |

### In practice

Commits are small, focused and described in the imperative mood, work happens on feature branches that are merged after review, and secrets and environment files are listed in .gitignore. Experiments in ML projects are tracked separately from the code ([[experiment-tracking|Experiment Tracking]]), and CI pipelines start from commits ([[mlops-and-deployment|MLOps and Deployment]]).

### Key takeaway

Git records snapshots of a project in a full local history; staging, commits and cheap branches make change tracking and collaboration reliable.

### Sources

- Chacon, S. & Straub, B. *Pro Git* (2nd ed.), 1.3 What is Git? Apress / git-scm.com. [git-scm.com](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
- Chacon, S. & Straub, B. *Pro Git* (2nd ed.), 3.1 Branches in a Nutshell. Apress / git-scm.com. [git-scm.com](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- Git project. *gitignore Documentation.* git-scm.com. [git-scm.com](https://git-scm.com/docs/gitignore)
- GitHub. *Generating a new SSH key and adding it to the ssh-agent.* GitHub Docs. [docs.github.com](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

## DE

> **Hinweis:** LLM-generierte Zusammenfassung auf Grundlage der angegebenen Quellen; sie kann unvollständig, veraltet oder falsch sein.

### TL;DR

Git ist ein verteiltes Versionsverwaltungssystem, das die Geschichte eines Projekts als Folge von Snapshots speichert; jeder Klon enthält die vollständige Historie, sodass fast alle Operationen lokal und schnell sind (Pro Git). Änderungen durchlaufen drei Zustände, geändert, vorgemerkt und committet, und Branches sind leichtgewichtige Zeiger auf Commits, die paralleles Arbeiten und Zusammenführen günstig machen (Pro Git branching). Eine .gitignore-Datei hält nicht zu verfolgende Dateien aus dem Repository heraus (gitignore docs), und SSH-Schlüssel authentifizieren Pushes zu Hosting-Diensten wie GitHub (GitHub SSH docs).

### Kernkonzepte

- **Snapshots:** Git betrachtet seine Daten als Snapshots des ganzen Projekts statt als Listen von Dateiänderungen; Inhalte werden mit Prüfsummen versehen, sodass Änderungen nicht unbemerkt bleiben (Pro Git).
- **Drei Zustände:** Dateien sind geändert (verändert, aber nicht committet), vorgemerkt (für den nächsten Commit markiert) oder committet (im Repository gespeichert), entsprechend Arbeitsverzeichnis, Staging Area und Repository (Pro Git).
- **Lokal und verteilt:** Jeder Klon enthält die vollständige Historie, und Remotes werden mit fetch, pull und push abgeglichen (Pro Git).
- **Branches:** Ein Branch ist ein leichtgewichtiger, beweglicher Zeiger auf einen Commit, und HEAD zeigt auf den aktuellen Branch; Merging verbindet auseinanderlaufende Historien per Fast-Forward oder mit einem Merge-Commit, und widersprüchliche Änderungen müssen von Hand aufgelöst werden (Pro Git branching).
- **.gitignore:** Jede Zeile ist ein Muster für absichtlich nicht verfolgte Dateien; ! kehrt ein Muster um, ein abschließender Schrägstrich passt nur auf Verzeichnisse, und bereits verfolgte Dateien sind nicht betroffen (gitignore docs).
- **SSH-Authentifizierung:** Ein mit ssh-keygen erzeugtes Schlüsselpaar authentifiziert den Rechner beim Hosting-Dienst; der ssh-agent merkt sich die Passphrase (GitHub SSH docs).

### Typische Verwendung

```bash
git clone git@github.com:org/repo.git      # Repository mit voller Historie kopieren
git switch -c feature/notes               # neuen Branch anlegen und wechseln
git status                                 # geänderte und vorgemerkte Dateien anzeigen
git add notes/new.md                       # Änderungen vormerken
git commit -m "Add new note"               # Snapshot festhalten
git pull --rebase                          # mit entfernten Änderungen aktualisieren
git push -u origin feature/notes           # Branch veröffentlichen
git restore notes/draft.md                 # nicht vorgemerkte Änderungen verwerfen
git revert <commit>                        # Commit durch neuen Commit rückgängig machen

ssh-keygen -t ed25519 -C "you@example.com" # SSH-Schlüssel für GitHub erzeugen
```

Rückgängig-Operationen unterscheiden sich in ihrer Reichweite: restore verwirft Änderungen im Arbeitsverzeichnis, reset verschiebt den Branch-Zeiger (und kann Commits verwerfen), und revert erzeugt einen neuen Commit, der einen früheren rückgängig macht, was für geteilte Historie sicher ist (Pro Git).

### Wann einsetzen

- Für jedes Code-, Konfigurations- oder Textprojekt, dessen Historie nachverfolgt und geteilt werden soll (Pro Git).
- Wenn mehrere Personen parallel arbeiten, mit Branches und Merges (Pro Git branching).
- Große Binärdateien und erzeugte Artefakte gehören in .gitignore oder spezialisierte Speicher statt ins Repository (gitignore docs).

### Stärken und Grenzen

**Stärken**
- Die vollständige lokale Historie macht Operationen schnell und Arbeit offline möglich (Pro Git).
- Günstige Branches unterstützen paralleles Arbeiten und Experimente (Pro Git branching).
- Prüfsummen schützen die Integrität der Historie (Pro Git).

**Einschränkungen**
- Gleichzeitige Änderungen derselben Zeilen erzeugen Merge-Konflikte, die von Hand gelöst werden müssen (Pro Git branching).
- Bereits verfolgte Dateien sind von späteren .gitignore-Regeln nicht betroffen (gitignore docs).
- Geteilte Historie umzuschreiben, etwa mit reset oder rebase, kann Mitarbeitende behindern (Pro Git).

### Vergleich

| Ansatz | Unterschiede | Geeignet für |
|----------|----------------|------------|
| Merge | Verbindet Historien, erhält die Branch-Struktur (Pro Git branching) | Geteilte Branches |
| Rebase | Spielt Commits auf einer neuen Basis ab, für eine lineare Historie (Pro Git) | Lokale Branches vor der Veröffentlichung |
| HTTPS-Remote | Authentifizierung mit Zugangsdaten oder Tokens | Gelegentlicher Zugriff |
| SSH-Remote | Authentifizierung mit Schlüsselpaar (GitHub SSH docs) | Regelmäßige Pushes von einem vertrauenswürdigen Rechner |

### In der Praxis

Commits sind klein, fokussiert und im Imperativ beschrieben, gearbeitet wird auf Feature-Branches, die nach einem Review zusammengeführt werden, und Geheimnisse sowie Umgebungsdateien stehen in .gitignore. Experimente in ML-Projekten werden getrennt vom Code nachverfolgt ([[experiment-tracking|Experiment Tracking]]), und CI-Pipelines starten bei Commits ([[mlops-and-deployment|MLOps und Deployment]]).

### Merksatz

Git hält Snapshots eines Projekts in einer vollständigen lokalen Historie fest; Staging, Commits und günstige Branches machen Änderungsverfolgung und Zusammenarbeit verlässlich.

### Quellen

- Chacon, S. & Straub, B. *Pro Git* (2nd ed.), 1.3 What is Git? Apress / git-scm.com. [git-scm.com](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
- Chacon, S. & Straub, B. *Pro Git* (2nd ed.), 3.1 Branches in a Nutshell. Apress / git-scm.com. [git-scm.com](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- Git project. *gitignore Documentation.* git-scm.com. [git-scm.com](https://git-scm.com/docs/gitignore)
- GitHub. *Generating a new SSH key and adding it to the ssh-agent.* GitHub Docs. [docs.github.com](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
