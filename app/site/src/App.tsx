import { Children, isValidElement, lazy, Suspense, useEffect, useMemo, useState, type FormEvent, type MouseEvent, type ReactNode } from "react";
import { useTranslation } from "react-i18next";
import ReactMarkdown, { type Components } from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  areaName,
  buildSearchIndex,
  contextSnippet,
  entityName,
  loadSiteData,
  noteContent,
  noteTitle,
  renderWikilinks,
  wikilinkResolver,
  type Area,
  type EntityNode,
  type GraphNode,
  type Note,
  type SiteData,
} from "./data";
import type { Language } from "./i18n";
import { ADDRESS_TOKEN, decodeAddress, decodeEmail, EMAIL_HREF, isDraft, legalPages } from "./legal";
import { outlineNote, slugify, type TocEntry } from "./toc";

type Screen =
  | { kind: "graph" }
  | { kind: "notes"; page: number }
  | { kind: "search"; query: string; page: number }
  | { kind: "note"; slug: string }
  | { kind: "entity"; id: string }
  | { kind: "legal"; pageId: string };

const PAGE_SIZE = 24;
// The force-graph bundle is large; load it only when the graph is shown.
const GraphView = lazy(() => import("./GraphView").then((module) => ({ default: module.GraphView })));

function readScreen(): Screen {
  const params = new URLSearchParams(window.location.search);
  const page = Math.max(1, Number.parseInt(params.get("page") ?? "1", 10) || 1);
  switch (params.get("view")) {
    case "notes":
      return { kind: "notes", page };
    case "search": {
      const query = params.get("q");
      return query ? { kind: "search", query, page } : { kind: "graph" };
    }
    case "note": {
      const slug = params.get("slug");
      return slug ? { kind: "note", slug } : { kind: "graph" };
    }
    case "entity": {
      const id = params.get("id");
      return id ? { kind: "entity", id } : { kind: "graph" };
    }
    case "legal": {
      const pageId = params.get("id");
      return pageId ? { kind: "legal", pageId } : { kind: "graph" };
    }
    default:
      return { kind: "graph" };
  }
}

function screenUrl(screen: Screen): string {
  const params = new URLSearchParams();
  if (screen.kind !== "graph") params.set("view", screen.kind);
  if ((screen.kind === "notes" || screen.kind === "search") && screen.page > 1) {
    params.set("page", String(screen.page));
  }
  if (screen.kind === "search") params.set("q", screen.query);
  if (screen.kind === "note") params.set("slug", screen.slug);
  if (screen.kind === "entity" || screen.kind === "legal") {
    params.set("id", screen.kind === "entity" ? screen.id : screen.pageId);
  }
  const query = params.toString();
  return query ? `${window.location.pathname}?${query}` : window.location.pathname;
}

function headingText(children: ReactNode): string {
  return Children.toArray(children)
    .map((child) => {
      if (typeof child === "string" || typeof child === "number") return String(child);
      if (isValidElement<{ children?: ReactNode }>(child)) {
        return headingText(child.props.children);
      }
      return "";
    })
    .join("");
}

function headingId(children: ReactNode): string {
  return slugify(headingText(children));
}

function App() {
  const { t, i18n } = useTranslation();
  const language = (i18n.language === "de" ? "de" : "en") as Language;
  const [data, setData] = useState<SiteData | null>(null);
  const [query, setQuery] = useState("");
  // On the graph page, the search box filters the graph instead of searching notes.
  const [graphFilter, setGraphFilter] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [showBackToTop, setShowBackToTop] = useState(false);
  const [screen, setScreen] = useState<Screen>(readScreen);

  useEffect(() => {
    let active = true;
    loadSiteData()
      .then((result) => {
        if (active) setData(result);
      })
      .catch((cause: unknown) => {
        if (active) setError(t("loadError", { message: cause instanceof Error ? cause.message : String(cause) }));
      });
    return () => {
      active = false;
    };
    // Loaded once; the error message keeps the language active at load time.
  }, []);

  useEffect(() => {
    const updateScrollState = () => setShowBackToTop(window.scrollY > 400);
    updateScrollState();
    window.addEventListener("scroll", updateScrollState, { passive: true });
    return () => window.removeEventListener("scroll", updateScrollState);
  }, []);

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  useEffect(() => {
    const handlePopState = () => setScreen(readScreen());
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  useEffect(() => {
    if (screen.kind === "search") setQuery(screen.query);
  }, [screen]);

  // Renamed notes and entities: replace an old address with the current one.
  useEffect(() => {
    const redirects = data?.redirects;
    if (!redirects) return;
    let next: Screen | null = null;
    if (screen.kind === "note" && redirects.notes[screen.slug]) {
      next = { kind: "note", slug: redirects.notes[screen.slug] };
    } else if (screen.kind === "entity") {
      const bare = screen.id.replace(/^entity:/, "");
      const target = redirects.entities[bare];
      if (target) next = { kind: "entity", id: screen.id.startsWith("entity:") ? `entity:${target}` : target };
    }
    if (next) {
      window.history.replaceState(null, "", screenUrl(next));
      setScreen(next);
    }
  }, [data, screen]);

  const notes = data?.notes ?? [];
  const notesBySlug = useMemo(() => new Map(notes.map((note) => [note.slug, note])), [notes]);
  const nodesById = useMemo(
    () => new Map((data?.graph.nodes ?? []).map((node) => [node.id, node])),
    [data],
  );
  const resolveWikilink = useMemo(() => wikilinkResolver(notes.map((note) => note.slug)), [notes]);
  const searchIndex = useMemo(() => buildSearchIndex(notes, language), [language, notes]);

  function navigate(next: Screen) {
    window.history.pushState(null, "", screenUrl(next));
    setScreen(next);
    window.scrollTo({ top: 0, behavior: "auto" });
  }

  function openNode(node: GraphNode) {
    if (node.kind === "note") navigate({ kind: "note", slug: node.slug });
    else if (node.note) navigate({ kind: "note", slug: node.note });
    else navigate({ kind: "entity", id: node.id });
  }

  function search(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = query.trim();
    if (screen.kind === "graph") {
      setError(null);
      setGraphFilter(trimmed);
      // The graph sits below the introduction and the news; bring it into view.
      requestAnimationFrame(() => document.getElementById("graph-title")?.scrollIntoView({ behavior: "smooth", block: "start" }));
      return;
    }
    if (!trimmed) {
      setError(t("enterSearchTerm"));
      return;
    }
    setError(null);
    navigate({ kind: "search", query: trimmed, page: 1 });
  }

  const searchHits = useMemo(() => {
    if (screen.kind !== "search") return [];
    return searchIndex
      .search(screen.query)
      .flatMap((hit) => notesBySlug.get(String(hit.id)) ?? []);
  }, [notesBySlug, screen, searchIndex]);

  const listedNotes = screen.kind === "search"
    ? searchHits
    : [...notes].sort((a, b) => noteTitle(a, language).localeCompare(noteTitle(b, language), language));
  const activeNote = screen.kind === "note" ? notesBySlug.get(screen.slug) : undefined;
  const activeEntityNode = screen.kind === "entity" ? nodesById.get(screen.id) : undefined;
  const activeEntity = activeEntityNode?.kind === "entity" ? activeEntityNode : undefined;
  const legalPage = screen.kind === "legal" ? legalPages.find((item) => item.id === screen.pageId) : undefined;

  const screenHeading = (() => {
    switch (screen.kind) {
      case "graph":
        return t("headingGraph");
      case "notes":
        return t("headingNotes");
      case "search":
        return t("headingSearch");
      case "note":
        return activeNote ? noteTitle(activeNote, language) : data ? t("headingNotFound") : t("loading");
      case "entity":
        return activeEntity ? entityName(activeEntity, language) : data ? t("headingNotFound") : t("loading");
      case "legal":
        return legalPage ? (language === "en" ? legalPage.title_en : legalPage.title_de) : t("headingInformation");
    }
  })();

  function scrollToTop() {
    document.getElementById("page-heading")?.focus({ preventScroll: true });
    window.scrollTo({
      top: 0,
      behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth",
    });
  }

  return (
    <div className="page-shell">
      <a className="skip-link" href="#main-content">{t("skipToContent")}</a>
      <header className="topbar">
        <a
          className="brand"
          href="./"
          onClick={(event) => {
            event.preventDefault();
            navigate({ kind: "graph" });
          }}
        >
          <span className="brand-mark" aria-hidden="true">◉</span>
          <span>Knowledge Radar</span>
        </a>
        <nav className="primary-nav" aria-label={t("mainNavigation")}>
          <button
            aria-current={screen.kind === "graph" ? "page" : undefined}
            onClick={() => navigate({ kind: "graph" })}
            type="button"
          >
            {t("navGraph")}
          </button>
          <button
            aria-current={screen.kind === "notes" || screen.kind === "note" ? "page" : undefined}
            onClick={() => navigate({ kind: "notes", page: 1 })}
            type="button"
          >
            {t("navNotes")}
          </button>
        </nav>
        <form className="header-search" onSubmit={search} role="search">
          <label className="visually-hidden" htmlFor="global-search">{t("searchLabel")}</label>
          <input
            id="global-search"
            onChange={(event) => setQuery(event.target.value)}
            placeholder={t(screen.kind === "graph" ? "graphSearchPlaceholder" : "searchPlaceholder")}
            value={query}
          />
          <button aria-label={t("search")} type="submit">⌕</button>
        </form>
        <div className="language-toggle" role="group" aria-label={t("chooseLanguage")}>
          {(["en", "de"] as const).map((value) => (
            <button
              aria-pressed={language === value}
              aria-label={value === "en" ? "English" : "Deutsch"}
              className={language === value ? "selected" : ""}
              key={value}
              onClick={() => void i18n.changeLanguage(value)}
              type="button"
            >
              {value.toUpperCase()}
            </button>
          ))}
        </div>
      </header>

      <main id="main-content" tabIndex={-1}>
        <section className="intro" aria-labelledby="page-heading">
          <p className="eyebrow">{t("eyebrow")}</p>
          <h1 id="page-heading" tabIndex={-1}>{screenHeading}</h1>
          {screen.kind === "graph" && <p className="intro-copy">{t("introGraph")}</p>}
          {screen.kind === "search" && data && (
            <p className="intro-copy" role="status" aria-live="polite">
              {t("resultsFor", { count: searchHits.length, query: screen.query })}
            </p>
          )}
          {screen.kind !== "graph" && (
            <div className="breadcrumbs">
              <button onClick={() => navigate({ kind: "graph" })} type="button">{t("backToGraph")}</button>
            </div>
          )}
        </section>

        {error && <div className="error-message" role="alert">{error}</div>}
        {!data && !error && <p className="muted" role="status" aria-live="polite">{t("loading")}</p>}

        {data && screen.kind === "graph" && (
          <>
            <section className="content-card about-section" aria-labelledby="about-title">
              <p className="eyebrow">{t("aboutEyebrow")}</p>
              <h2 id="about-title">{t("aboutTitle")}</h2>
              <p>{t("aboutBody")}</p>
            </section>
            <NewsSection
              data={data}
              language={language}
              limit={6}
              notesBySlug={notesBySlug}
              openNote={(slug) => navigate({ kind: "note", slug })}
              showAll={() => navigate({ kind: "notes", page: 1 })}
            />
            <section className="content-card graph-section" aria-labelledby="graph-title">
              <div className="section-heading">
                <div>
                  <p className="eyebrow">{t("graphEyebrow")}</p>
                  <h2 id="graph-title">{t("graphTitle")}</h2>
                </div>
              </div>
              <Suspense fallback={<p className="muted">{t("loading")}</p>}>
                <GraphView
                  clearFilter={() => {
                    setGraphFilter("");
                    setQuery("");
                  }}
                  edges={data.graph.edges}
                  filter={graphFilter}
                  language={language}
                  nodes={data.graph.nodes}
                  openNode={openNode}
                />
              </Suspense>
            </section>
          </>
        )}

        {data && screen.kind === "notes" && (data.areas?.length ?? 0) > 0 && (
          <NoteAreas
            data={data}
            language={language}
            notesBySlug={notesBySlug}
            openNote={(slug) => navigate({ kind: "note", slug })}
          />
        )}

        {data && screen.kind === "search" && (data.areas?.length ?? 0) > 0 && (
          <SearchResultsByArea
            areas={data.areas ?? []}
            language={language}
            notes={searchHits}
            openNote={(slug) => navigate({ kind: "note", slug })}
          />
        )}

        {data && ((screen.kind === "search" || screen.kind === "notes") && !data.areas?.length) && (
          <NoteResults
            changePage={(page) => navigate({ ...screen, page })}
            language={language}
            notes={listedNotes}
            openNote={(slug) => navigate({ kind: "note", slug })}
            page={screen.page}
          />
        )}

        {data && screen.kind === "note" && (
          activeNote ? (
            <NoteArticle
              data={data}
              language={language}
              navigate={navigate}
              note={activeNote}
              notesBySlug={notesBySlug}
              openNode={openNode}
              resolveWikilink={resolveWikilink}
            />
          ) : (
            <div className="error-message" role="alert">{t("noteNotFound")}</div>
          )
        )}

        {data && screen.kind === "entity" && (
          activeEntity ? (
            <EntityStub data={data} entity={activeEntity} language={language} navigate={navigate} notesBySlug={notesBySlug} />
          ) : (
            <div className="error-message" role="alert">{t("entityNotFound")}</div>
          )
        )}

        {screen.kind === "legal" && (
          legalPage ? (
            <article className="content-card legal-draft" aria-labelledby="legal-title">
              {isDraft(legalPage) && <p className="draft-label">{t("draftLabel")}</p>}
              <h2 id="legal-title">{language === "en" ? legalPage.title_en : legalPage.title_de}</h2>
              <div className="markdown-body">
                {(language === "en" ? legalPage.body_en : legalPage.body_de).split(ADDRESS_TOKEN).map((part, index) => (
                  <div key={index}>
                    {index > 0 && <PostalAddress />}
                    <ReactMarkdown components={legalComponents} remarkPlugins={[remarkGfm]}>{part}</ReactMarkdown>
                  </div>
                ))}
              </div>
            </article>
          ) : (
            <div className="error-message" role="alert">{t("legalNotFound")}</div>
          )
        )}
      </main>

      <footer className="site-footer">
        <span>Knowledge Radar</span>
        <nav aria-label={t("legalNavigation")}>
          {legalPages.map((page) => (
            <a
              href={`?view=legal&id=${encodeURIComponent(page.id)}`}
              key={page.id}
              onClick={(event) => {
                event.preventDefault();
                navigate({ kind: "legal", pageId: page.id });
              }}
            >
              {language === "en" ? page.title_en : page.title_de}
            </a>
          ))}
        </nav>
      </footer>
      {showBackToTop && (
        <button aria-label={t("backToTop")} className="back-to-top" onClick={scrollToTop} type="button">
          <span aria-hidden="true">↑</span>
        </button>
      )}
    </div>
  );
}

interface NoteResultsProps {
  language: Language;
  notes: Note[];
  openNote: (slug: string) => void;
  page: number;
  changePage: (page: number) => void;
}

function NoteResults({ language, notes, openNote, page, changePage }: NoteResultsProps) {
  const { t } = useTranslation();
  const totalPages = Math.max(1, Math.ceil(notes.length / PAGE_SIZE));
  const current = Math.min(page, totalPages);
  const visible = notes.slice((current - 1) * PAGE_SIZE, current * PAGE_SIZE);
  return (
    <section className="content-card" aria-label={t("navNotes")}>
      {notes.length === 0 ? (
        <p className="muted" role="status" aria-live="polite">{t("noNotesFound")}</p>
      ) : (
        <>
          <p className="results-count">
            {t("notesCount", { count: notes.length })} · {t("pageOf", { page: current, total: totalPages })}
          </p>
          <ul className="result-list">
            {visible.map((note) => (
              <li key={note.slug}>
                <button className="result-card" onClick={() => openNote(note.slug)} type="button">
                  <span className="note-type">{t(`entityTypes.${note.entity_type}`, { defaultValue: note.entity_type })}</span>
                  <span className="note-title">{noteTitle(note, language)}</span>
                </button>
              </li>
            ))}
          </ul>
          {totalPages > 1 && (
            <nav className="pagination" aria-label={t("resultPages")}>
              <button disabled={current <= 1} onClick={() => changePage(current - 1)} type="button">{t("previous")}</button>
              <span aria-current="page">{current} / {totalPages}</span>
              <button disabled={current >= totalPages} onClick={() => changePage(current + 1)} type="button">{t("next")}</button>
            </nav>
          )}
        </>
      )}
    </section>
  );
}

interface SearchResultsByAreaProps {
  areas: Area[];
  language: Language;
  notes: Note[];
  openNote: (slug: string) => void;
}

/** Search hits grouped by their main area; areas keep their order, hits their rank. */
function SearchResultsByArea({ areas, language, notes, openNote }: SearchResultsByAreaProps) {
  const { t } = useTranslation();
  const mainArea = new Map(areas.flatMap((area) => area.notes.map((slug) => [slug, area.id] as const)));
  // The area of the best hit comes first and is open; the others follow by their best hit.
  const groups = [
    ...areas.map((area) => ({ id: area.id, name: areaName(area, language), hits: notes.filter((note) => mainArea.get(note.slug) === area.id) })),
    { id: "other", name: t("otherArea"), hits: notes.filter((note) => !mainArea.has(note.slug)) },
  ]
    .filter((group) => group.hits.length > 0)
    .sort((a, b) => notes.indexOf(a.hits[0]) - notes.indexOf(b.hits[0]));
  return (
    <section className="content-card" aria-label={t("headingSearch")}>
      {notes.length === 0 ? (
        <p className="muted" role="status" aria-live="polite">{t("noNotesFound")}</p>
      ) : (
        <>
          <p className="results-count" role="status">{t("notesCount", { count: notes.length })}</p>
          {groups.map((group, index) => (
            <details className="area" key={group.id} open={index === 0 || groups.length <= 3}>
              <summary>
                <span className="area-name">{group.name}</span>
                <span className="area-count">{group.hits.length}</span>
              </summary>
              <ul className="result-list area-notes">
                {group.hits.map((note) => (
                  <li key={note.slug}>
                    <button className="result-card" onClick={() => openNote(note.slug)} type="button">
                      <span className="note-type">{t(`entityTypes.${note.entity_type}`, { defaultValue: note.entity_type })}</span>
                      <span className="note-title">{noteTitle(note, language)}</span>
                    </button>
                  </li>
                ))}
              </ul>
            </details>
          ))}
        </>
      )}
    </section>
  );
}

interface NewsSectionProps {
  data: SiteData;
  language: Language;
  notesBySlug: Map<string, Note>;
  openNote: (slug: string) => void;
  /** Show at most this many items, with a link to the full list in the notes view. */
  limit?: number;
  /** Leads to the full list; without it, the section expands in place. */
  showAll?: () => void;
}

/** Notes added after the initial migration and dated update entries, newest first. */
function NewsSection({ data, language, notesBySlug, openNote, limit, showAll }: NewsSectionProps) {
  const { t } = useTranslation();
  const [expanded, setExpanded] = useState(false);
  const all = (data.news ?? []).filter((item) => notesBySlug.has(item.slug));
  const news = limit && !expanded ? all.slice(0, limit) : all;
  if (news.length === 0) return null;
  const formatDate = (date: string) =>
    new Date(`${date}T00:00:00`).toLocaleDateString(language === "en" ? "en-GB" : "de-DE", { day: "numeric", month: "short", year: "numeric" });
  return (
    <section className="content-card" aria-labelledby="news-title">
      <h2 className="area-section-title" id="news-title">{t("newAndUpdated")}</h2>
      <ul className="news-list">
        {news.map((item) => {
          const note = notesBySlug.get(item.slug)!;
          const updateTitle = language === "en" ? item.title_en : item.title_de;
          return (
            <li key={`${item.kind}:${item.slug}:${item.date}`}>
              <button className="news-item" onClick={() => openNote(item.slug)} type="button">
                <span className="news-meta">
                  <span className={`news-badge news-badge-${item.kind}`}>{t(item.kind === "new" ? "newNote" : "updatedNote")}</span>
                  <time dateTime={item.date}>{formatDate(item.date)}</time>
                </span>
                <span className="note-title">{noteTitle(note, language)}</span>
                {item.kind === "update" && updateTitle && <span className="news-detail">{updateTitle}</span>}
              </button>
            </li>
          );
        })}
      </ul>
      {limit && all.length > limit && (expanded ? (
        <button className="news-more" onClick={() => setExpanded(false)} type="button">{t("fewerNewAndUpdated")}</button>
      ) : (
        <button className="news-more" onClick={showAll ?? (() => setExpanded(true))} type="button">{t("allNewAndUpdated", { count: all.length })}</button>
      ))}
    </section>
  );
}

interface NoteAreasProps {
  data: SiteData;
  language: Language;
  notesBySlug: Map<string, Note>;
  openNote: (slug: string) => void;
}

/** The note list grouped by subject area, with the latest additions and updates first. */
function NoteAreas({ data, language, notesBySlug, openNote }: NoteAreasProps) {
  const { t } = useTranslation();
  const areas = data.areas ?? [];
  const mainArea = new Map(areas.flatMap((area) => area.notes.map((slug) => [slug, area] as const)));
  return (
    <>
      <NewsSection data={data} language={language} limit={6} notesBySlug={notesBySlug} openNote={openNote} />

      <section className="content-card" aria-labelledby="areas-title">
        <h2 className="area-section-title" id="areas-title">{t("byArea")}</h2>
        <p className="results-count">{t("notesCount", { count: data.notes.length })}</p>
        {areas.map((area) => {
          const entries = [
            ...area.notes.map((slug) => ({ slug, from: undefined as Area | undefined })),
            ...area.also.map((slug) => ({ slug, from: mainArea.get(slug) })),
          ].filter((entry) => notesBySlug.has(entry.slug));
          return (
            <details className="area" key={area.id}>
              <summary>
                <span className="area-name">{areaName(area, language)}</span>
                <span className="area-count" aria-label={t("areaCount", { count: area.notes.length })}>{area.notes.length}</span>
              </summary>
              <ul className="result-list area-notes">
                {entries.map(({ slug, from }) => {
                  const note = notesBySlug.get(slug)!;
                  return (
                    <li key={slug}>
                      <button className={`result-card${from ? " result-card-secondary" : ""}`} onClick={() => openNote(slug)} type="button">
                        <span className="note-type">{t(`entityTypes.${note.entity_type}`, { defaultValue: note.entity_type })}</span>
                        <span className="note-title">{noteTitle(note, language)}</span>
                        {from && <span className="also-from">{t("alsoFrom", { area: areaName(from, language) })}</span>}
                      </button>
                    </li>
                  );
                })}
              </ul>
            </details>
          );
        })}
      </section>
    </>
  );
}

interface NoteArticleProps {
  data: SiteData;
  language: Language;
  navigate: (screen: Screen) => void;
  note: Note;
  notesBySlug: Map<string, Note>;
  openNode: (node: GraphNode) => void;
  resolveWikilink: (target: string) => string | null;
}

function NoteArticle({ data, language, navigate, note, notesBySlug, openNode, resolveWikilink }: NoteArticleProps) {
  const { t } = useTranslation();
  const noteId = `note:${note.slug}`;
  const discussed = data.graph.edges
    .filter((edge) => edge.type === "DISCUSSES" && edge.source === noteId)
    .flatMap((edge) => {
      const node = data.graph.nodes.find((candidate) => candidate.id === edge.target);
      return node?.kind === "entity" && node.note !== note.slug ? [node] : [];
    });
  const backlinks = data.notes.filter((other) => other.links.includes(note.slug));
  const titleOf = (slug: string) => {
    const linked = notesBySlug.get(slug);
    return linked ? noteTitle(linked, language) : slug;
  };
  const markdown = renderWikilinks(noteContent(note, language), resolveWikilink, titleOf);
  // Template notes cite their sources in the text; the frontmatter list is only a fallback.
  const hasSourcesSection = /^###\s+(Official sources|Sources|Amtliche Quellen|Quellen)\s*$/m.test(markdown);
  const outline = outlineNote(markdown);

  const components: Components = {
    h3: ({ children, ...props }) => <h3 id={headingId(children)} tabIndex={-1} {...props}>{children}</h3>,
    h4: ({ children, ...props }) => <h4 id={headingId(children)} tabIndex={-1} {...props}>{children}</h4>,
    h5: ({ children, ...props }) => <h5 id={headingId(children)} tabIndex={-1} {...props}>{children}</h5>,
    a: ({ href, children, ...props }) => {
      const internal = href?.startsWith("?view=note&slug=");
      if (!internal) return <a href={href} {...props}>{children}</a>;
      const slug = decodeURIComponent(href!.slice("?view=note&slug=".length));
      return (
        <a
          href={href}
          onClick={(event) => {
            event.preventDefault();
            navigate({ kind: "note", slug });
          }}
          {...props}
        >
          {children}
        </a>
      );
    },
  };

  return (
    <article className="content-card note-detail" aria-labelledby="note-title">
      <div className="article-meta">
        <span className="note-type">{t(`entityTypes.${note.entity_type}`, { defaultValue: note.entity_type })}</span>
      </div>
      <h2 id="note-title">{noteTitle(note, language)}</h2>
      {/* react-markdown never renders raw HTML, so note content cannot inject markup. */}
      <div className="markdown-body">
        <ReactMarkdown components={components} remarkPlugins={[remarkGfm]}>{outline.intro}</ReactMarkdown>
      </div>
      {outline.entries.length >= 3 && <TableOfContents entries={outline.entries} />}
      <div className="markdown-body">
        <ReactMarkdown components={components} remarkPlugins={[remarkGfm]}>{outline.body}</ReactMarkdown>
      </div>
      {note.original_source_text && (
        <section className="original-source" lang="de">
          <h3>{t("originalSourceText")}</h3>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{note.original_source_text}</ReactMarkdown>
        </section>
      )}
      {(discussed.length > 0 || note.links.length > 0 || backlinks.length > 0) && (
        <div className="related-notes">
          {discussed.length > 0 && (
            <section>
              <h3>{t("discusses")}</h3>
              {discussed.map((entity) => (
                <button key={entity.id} onClick={() => openNode(entity)} type="button">{entityName(entity, language)}</button>
              ))}
            </section>
          )}
          {note.links.length > 0 && (
            <section>
              <h3>{t("linksTo")}</h3>
              {note.links.map((slug) => (
                <button key={slug} onClick={() => navigate({ kind: "note", slug })} type="button">{titleOf(slug)}</button>
              ))}
            </section>
          )}
          {backlinks.length > 0 && (
            <section>
              <h3>{t("linkedFrom")}</h3>
              {backlinks.map((other) => (
                <button key={other.slug} onClick={() => navigate({ kind: "note", slug: other.slug })} type="button">
                  {noteTitle(other, language)}
                </button>
              ))}
            </section>
          )}
        </div>
      )}
      {!hasSourcesSection && (
        <section className="sources">
          <h3>{t("sources")}</h3>
          <ul>
            {note.sources.map((source) => (
              <li key={source}>
                <a href={source} rel="noreferrer" target="_blank">
                  {source}
                  <span className="visually-hidden">{t("opensInNewTab")}</span>
                </a>
              </li>
            ))}
          </ul>
        </section>
      )}
    </article>
  );
}

// Short outlines show every sub-entry; long ones (e.g. a regulation with all its
// articles) show only the top level and expand per section on click.
const TOC_EXPANDED_LIMIT = 25;

function TableOfContents({ entries }: { entries: TocEntry[] }) {
  const { t } = useTranslation();
  const expanded = entries.reduce((sum, entry) => sum + entry.children.length, 0) <= TOC_EXPANDED_LIMIT;
  function jump(event: MouseEvent<HTMLAnchorElement>, id: string) {
    const target = document.getElementById(id);
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({
      behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth",
    });
    target.focus({ preventScroll: true });
  }
  const link = (entry: TocEntry) => (
    <a href={`#${entry.id}`} onClick={(event) => jump(event, entry.id)}>{entry.text}</a>
  );
  return (
    <nav aria-labelledby="toc-title" className="toc">
      <h3 id="toc-title">{t("tableOfContents")}</h3>
      <ol>
        {entries.map((entry) => (
          <li key={entry.id}>
            {entry.children.length === 0 ? link(entry) : (
              <details open={expanded}>
                <summary>{link(entry)}</summary>
                <ol>
                  {entry.children.map((child) => <li key={child.id}>{link(child)}</li>)}
                </ol>
              </details>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

interface EntityStubProps {
  data: SiteData;
  entity: EntityNode;
  language: Language;
  navigate: (screen: Screen) => void;
  notesBySlug: Map<string, Note>;
}

/** Auto-generated view for entities without their own note, assembled from the graph only. */
function EntityStub({ data, entity, language, navigate, notesBySlug }: EntityStubProps) {
  const { t } = useTranslation();
  const mentioning = data.graph.edges
    .filter((edge) => edge.type === "DISCUSSES" && edge.target === entity.id)
    .flatMap((edge) => notesBySlug.get(edge.source.replace(/^note:/, "")) ?? []);
  const summary = language === "en" ? entity.summary_en : entity.summary_de;
  return (
    <article className="content-card note-detail" aria-labelledby="entity-title">
      <div className="article-meta">
        <span className="note-type">{t(`entityTypes.${entity.entity_type}`, { defaultValue: entity.entity_type })}</span>
        <span className="draft-label">{t("stubLabel")}</span>
      </div>
      <h2 id="entity-title">{entityName(entity, language)}</h2>
      {summary ? (
        <section className="entity-summary">
          <p className="muted">{t("summaryNotice")}</p>
          <p>{summary}</p>
          <h3>{t("sources")}</h3>
          <ul>
            {(entity.sources ?? []).map((url) => (
              <li key={url}>
                <a href={url} rel="noreferrer" target="_blank">{sourceLabel(url)}</a>
              </li>
            ))}
          </ul>
        </section>
      ) : (
        <p className="muted">{t("stubIntro")}</p>
      )}
      <section className="related-notes">
        <h3>{t("mentionedIn")}</h3>
        <ul className="stub-mentions">
          {mentioning.map((note) => (
            <li key={note.slug}>
              <button onClick={() => navigate({ kind: "note", slug: note.slug })} type="button">
                {noteTitle(note, language)}
              </button>
              <p>{contextSnippet(noteContent(note, language), entityName(entity, language)) ?? ""}</p>
            </li>
          ))}
        </ul>
      </section>
    </article>
  );
}

export default App;

/** Host and path of a source URL, shown as its link text. */
function sourceLabel(url: string): string {
  try {
    const parsed = new URL(url);
    return `${parsed.host}${parsed.pathname === "/" ? "" : parsed.pathname}`;
  } catch {
    return url;
  }
}

/** Renders the decoded postal address; it is assembled in the browser, so it is not in the HTML. */
function PostalAddress() {
  const [lines, setLines] = useState<string[]>([]);
  useEffect(() => setLines(decodeAddress()), []);
  return (
    <p>
      {lines.map((line, index) => (
        <span key={index}>
          {line}
          {index < lines.length - 1 && <br />}
        </span>
      ))}
    </p>
  );
}

/** Renders the decoded email address as a mailto link; like the postal address, it is not in the HTML. */
function EmailLink() {
  const [email, setEmail] = useState("");
  useEffect(() => setEmail(decodeEmail()), []);
  return <a href={email ? `mailto:${email}` : undefined}>{email}</a>;
}

const legalComponents: Components = {
  a: ({ href, children }) => (href === EMAIL_HREF ? <EmailLink /> : <a href={href}>{children}</a>),
};
