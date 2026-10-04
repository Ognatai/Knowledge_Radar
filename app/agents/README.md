# Agent utilities

`validate_notes.py` checks public notes before they enter the future monitoring
and curation pipeline. It enforces the bilingual frontmatter and mandatory
source URL requirements without calling an LLM or changing note files.

Run from the repository root:

```powershell
python -m app.agents.validate_notes
```
