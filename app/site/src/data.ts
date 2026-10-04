import MiniSearch from "minisearch";
import type { Language } from "./i18n";

/** Shape written by `python -m app.backend.knowledge_radar.site_export`. */
export interface Note {
  slug: string;
  title_en: string;
  title_de: string;
  entity_type: string;
  sources: string[];
  links: string[];
  content_en: string;
  content_de: string;
  original_source_text: string | null;
}

export interface NoteNode {
  id: string;
  kind: "note";
  slug: string;
  title_en: string;
  title_de: string;
}

export interface EntityNode {
  id: string;
  kind: "entity";
  entity_type: string;
  name_en: string;
  name_de: string;
  note: string | null;
}

export type GraphNode = NoteNode | EntityNode;

export interface GraphEdge {
  source: string;
  target: string;
  type: string;
}

export interface SiteData {
  version: number;
  notes: Note[];
  graph: { nodes: GraphNode[]; edges: GraphEdge[] };
}

export async function loadSiteData(): Promise<SiteData> {
  const response = await fetch(`${import.meta.env.BASE_URL}data/site-data.json`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json() as Promise<SiteData>;
}

export const noteTitle = (note: Note | NoteNode, language: Language) =>
  language === "en" ? note.title_en : note.title_de;

export const entityName = (entity: EntityNode, language: Language) =>
  language === "en" ? entity.name_en : entity.name_de;

export const nodeLabel = (node: GraphNode, language: Language) =>
  node.kind === "note" ? noteTitle(node, language) : entityName(node, language);

export const noteContent = (note: Note, language: Language) =>
  language === "en" ? note.content_en : note.content_de;

/** Resolve a wikilink target like the exporter does: full slug, or unique file name. */
export function wikilinkResolver(slugs: string[]): (target: string) => string | null {
  const bySlug = new Set(slugs);
  const byName = new Map<string, string[]>();
  for (const slug of slugs) {
    const name = slug.split("/").pop() ?? slug;
    byName.set(name, [...(byName.get(name) ?? []), slug]);
  }
  return (target) => {
    const cleaned = target.trim().replace(/\.md$/, "");
    if (bySlug.has(cleaned)) return cleaned;
    const candidates = byName.get(cleaned) ?? [];
    return candidates.length === 1 ? candidates[0] : null;
  };
}

// Inside Markdown tables the pipe is escaped: [[target\|label]].
const WIKILINK = /\[\[([^[\]|#\\]+)(#[^[\]|\\]*)?(?:\\?\|([^[\]]*))?\]\]/g;

/** Turn [[target|label]] into Markdown links to the note view. */
export function renderWikilinks(
  markdown: string,
  resolve: (target: string) => string | null,
  titleOf: (slug: string) => string,
): string {
  return markdown.replace(WIKILINK, (_match, target: string, _heading, label?: string) => {
    const slug = resolve(target);
    const text = (label ?? (slug ? titleOf(slug) : target)).replace(/[[\]]/g, "");
    return slug ? `[${text}](?view=note&slug=${encodeURIComponent(slug)})` : text;
  });
}

/** One full-text index per language; search only ever looks at the active one. */
export function buildSearchIndex(notes: Note[], language: Language): MiniSearch<Note> {
  const index = new MiniSearch<Note>({
    idField: "slug",
    fields: ["title", "content"],
    storeFields: ["slug"],
    extractField: (note, field) => {
      if (field === "slug") return note.slug;
      if (field === "title") return noteTitle(note, language);
      if (language === "de") {
        return [note.content_de, note.original_source_text ?? ""].join("\n");
      }
      return note.content_en;
    },
    searchOptions: { boost: { title: 3 }, prefix: true, fuzzy: 0.2 },
  });
  index.addAll(notes);
  return index;
}

/** A short excerpt around the first mention of `term`, for the entity stub view. */
export function contextSnippet(markdown: string, term: string, radius = 140): string | null {
  const plain = markdown
    .replace(WIKILINK, (_m, t: string, _h, l?: string) => l ?? t)
    .replace(/[#>*_`]/g, "")
    .replace(/\s+/g, " ");
  const position = plain.toLowerCase().indexOf(term.toLowerCase());
  if (position < 0) return null;
  const start = Math.max(0, position - radius);
  const end = Math.min(plain.length, position + term.length + radius);
  return `${start > 0 ? "…" : ""}${plain.slice(start, end).trim()}${end < plain.length ? "…" : ""}`;
}
