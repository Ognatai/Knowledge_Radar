/** Table of contents for a note, derived from its `###`/`####` headings. */

export interface TocEntry {
  id: string;
  text: string;
  children: TocEntry[];
}

export interface NoteOutline {
  /** Markdown before the table of contents (notice + TL;DR). */
  intro: string;
  /** Markdown after it. */
  body: string;
  entries: TocEntry[];
}

// The summary section that precedes the table of contents.
const LEAD_HEADINGS = new Set(["tl;dr", "at a glance", "auf einen blick", "kurz zusammengefasst"]);

/** Anchor id for a heading text; must match the ids set on rendered headings. */
export function slugify(text: string): string {
  return text
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/&/g, " and ")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

function plainText(markdown: string): string {
  return markdown
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/[*_`]/g, "")
    .trim();
}

export function outlineNote(markdown: string): NoteOutline {
  const lines = markdown.split("\n");
  const headings: { level: 3 | 4; text: string; offset: number }[] = [];
  let offset = 0;
  let inFence = false;
  for (const line of lines) {
    if (/^(```|~~~)/.test(line)) inFence = !inFence;
    const match = !inFence && /^(#{3,4})\s+(.+?)\s*#*\s*$/.exec(line);
    if (match) {
      headings.push({ level: match[1].length as 3 | 4, text: plainText(match[2]), offset });
    }
    offset += line.length + 1;
  }

  const topLevel = headings.filter((heading) => heading.level === 3);
  const leadIsSummary = topLevel[0] && LEAD_HEADINGS.has(topLevel[0].text.toLowerCase());
  const split = (leadIsSummary ? topLevel[1] : topLevel[0])?.offset ?? markdown.length;

  const entries: TocEntry[] = [];
  for (const heading of headings) {
    if (heading.offset < split) continue;
    const entry = { id: slugify(heading.text), text: heading.text, children: [] };
    const parent = entries[entries.length - 1];
    if (heading.level === 4 && parent) parent.children.push(entry);
    else entries.push(entry);
  }
  return { intro: markdown.slice(0, split), body: markdown.slice(split), entries };
}
