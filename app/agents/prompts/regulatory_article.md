You write one section of a factual reference note about $act_context.

Write the detailed section for Article $article in $language.

Rules:
- Use ONLY information contained in the OFFICIAL ARTICLE TEXT below and the APPLICATION DATE given. Do not add facts, numbers, authorities, examples or interpretations from outside knowledge. If the article refers to other articles or annexes, name them, but do not describe their content.
- Cite paragraph and point numbers only as they appear in the official text.
- In "$heading_requires" go through the article paragraph by paragraph: every numbered paragraph of the official text must be covered, each as its own bullet starting with its number ($paragraph_label), stating precisely to whom it applies and what it says. Long enumerations may be summarised, but name their categories. Never generalise a rule beyond the systems or actors the paragraph names.
- Neutral, precise reference style. No first person, no marketing language. Short paragraphs and lists.
- Start with this heading line exactly: $title
- Then use exactly these sub-headings in this order (omit one only if the article gives nothing for it):
$headings
- $practice_rule Practical examples there must stay generic and clearly optional.
- "$heading_open" lists only things the wording of the article deliberately leaves open.
- In "$heading_applies" state: $application.
- Put key numbers and dates in **bold**.
- $language_rules Length: 300-900 words depending on the article's length. Output only the Markdown section, nothing else.

STYLE EXAMPLE (another article in the same format; imitate structure and tone only, not its content):
$example

CURRENT SHORT SUMMARY IN THE NOTE (may be outdated; the official text takes precedence):
$existing

OFFICIAL ARTICLE TEXT ($language):
$official
