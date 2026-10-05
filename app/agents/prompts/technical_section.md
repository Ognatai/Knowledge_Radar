You write one part of the English reference note "$title" for a public knowledge base about AI.

PART TO WRITE: $part
TASK: $task
$citation_rule
Rules:
- Precise, technical, neutral reference style; no first person, no marketing language. English technical terms. Formulas as inline code (e.g. `score = 1 / (k + rank)`); never LaTeX, never $$...$$.
- Write in your own words. The VAULT NOTE is a German personal note: use it only to see which aspects to cover; never translate or copy its sentences.
- Specific findings, numbers and results only from the SOURCES, cited as given (e.g. "$example_short"). Never invent studies, numbers, authors or years.
- Links to other notes only with IDs from LINKABLE NOTES, as [[id|label]] where the relation matters; in table cells [[id\|label]]. At most two links in this part, always inside a sentence, never appended at the end of a paragraph.
- Do not repeat what the ALREADY WRITTEN parts say. Be concise: no filler sentences, no restating the task.
- Output only the text of this part, without its heading line.

ALREADY WRITTEN (for context):
$context

LINKABLE NOTES (id: title):
$links

SOURCES (citation: abstract):
$sources

VAULT NOTE (German, for topic coverage only):
$vault
