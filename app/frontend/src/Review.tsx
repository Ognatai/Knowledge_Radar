import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { DraftStatus, DraftSummary, InboxBranch, Language, ProposalRun, reviewApi, ReviewOverview } from "./api";

const TEXT = {
  de: {
    loading: "Lädt die Vorschläge …",
    reload: "Neu laden",
    publicTitle: "Öffentliche Vorschläge",
    publicNote:
      "Entwürfe des wöchentlichen Laufs (lokale Branches auf dem Desktop). Veröffentlicht wird erst nach Claudes Prüfung gegen die Quellen: Vormerken heißt „bitte prüfen und übernehmen“.",
    noBranches: "Auf diesem Rechner gibt es keine Vorschlags-Branches; sie liegen auf dem Desktop.",
    noRuns: "Keine offenen Vorschläge.",
    run: "Lauf",
    removeRun: "Lauf entfernen",
    confirmRemove: (run: string) => `Branch proposals/${run} löschen? Die Entscheidungen bleiben gespeichert.`,
    kinds: { promotion: "neue Notiz (Beförderung)", update: "Aktualisierung", new_topic: "neues Thema", draft: "Entwurf" } as Record<string, string>,
    newNote: "neu",
    changed: "geändert",
    status: { open: "offen", wanted: "vorgemerkt", discarded: "verworfen" } as Record<DraftStatus, string>,
    show: "Ansehen",
    hide: "Zuklappen",
    want: "Vormerken",
    discard: "Verwerfen",
    reset: "Zurücksetzen",
    report: "Prüfbericht",
    diff: "Änderungen gegenüber der veröffentlichten Fassung",
    privateTitle: "Private Inbox",
    privateNote: "Neues zu den Lücken aus deinen Retros (Branches im privaten GitLab-Repo). Annehmen legt die Notiz in notes/ und aktualisiert den privaten Index.",
    noPrivate: "Kein privates Repository konfiguriert.",
    noInbox: "Keine offenen Inbox-Vorschläge.",
    accept: "Annehmen",
    accepted: (files: string[]) => `Angenommen: ${files.join(", ")}. Der private Index wird aktualisiert.`,
    discarded: (branch: string) => `Verworfen: ${branch}.`,
  },
  en: {
    loading: "Loading the proposals …",
    reload: "Reload",
    publicTitle: "Public proposals",
    publicNote:
      "Drafts of the weekly run (local branches on the Desktop). Nothing is published before Claude's review against the sources: “want” means “please review and take over”.",
    noBranches: "This machine has no proposal branches; they live on the Desktop.",
    noRuns: "No open proposals.",
    run: "Run",
    removeRun: "Remove run",
    confirmRemove: (run: string) => `Delete branch proposals/${run}? The decisions stay recorded.`,
    kinds: { promotion: "new note (promotion)", update: "update", new_topic: "new topic", draft: "draft" } as Record<string, string>,
    newNote: "new",
    changed: "changed",
    status: { open: "open", wanted: "wanted", discarded: "discarded" } as Record<DraftStatus, string>,
    show: "Show",
    hide: "Hide",
    want: "Want",
    discard: "Discard",
    reset: "Reset",
    report: "Review report",
    diff: "Changes against the published version",
    privateTitle: "Private inbox",
    privateNote: "News on the gaps from your retros (branches in the private GitLab repo). Accepting puts the note into notes/ and updates the private index.",
    noPrivate: "No private repository configured.",
    noInbox: "No open inbox proposals.",
    accept: "Accept",
    accepted: (files: string[]) => `Accepted: ${files.join(", ")}. The private index is being updated.`,
    discarded: (branch: string) => `Discarded: ${branch}.`,
  },
};

function Diff({ text }: { text: string }) {
  return (
    <pre className="diff">
      {text.split("\n").map((line, index) => (
        <span key={index} className={line.startsWith("+") && !line.startsWith("+++") ? "add" : line.startsWith("-") && !line.startsWith("---") ? "del" : line.startsWith("@@") ? "hunk" : ""}>
          {line}
          {"\n"}
        </span>
      ))}
    </pre>
  );
}

function Draft({ run, draft, language, onChange }: { run: string; draft: DraftSummary; language: Language; onChange: (error?: string) => void }) {
  const t = TEXT[language];
  const [detail, setDetail] = useState<{ review: string; diff: string } | null>(null);
  const [open, setOpen] = useState(false);
  const [working, setWorking] = useState(false);

  async function toggle() {
    if (!open && !detail) {
      try {
        setDetail(await reviewApi.draft(run, draft.slug));
      } catch (error) {
        onChange((error as Error).message);
        return;
      }
    }
    setOpen(!open);
  }

  async function decide(status: DraftStatus) {
    setWorking(true);
    try {
      await reviewApi.decide(run, draft.slug, status);
      onChange();
    } catch (error) {
      onChange((error as Error).message);
    } finally {
      setWorking(false);
    }
  }

  return (
    <li className={`draft-row status-${draft.status}`}>
      <div className="draft-head">
        <strong>{draft.slug}</strong>
        <span className="kind">{t.kinds[draft.kind] ?? draft.kind}</span>
        <span className="kind">{draft.new_note ? t.newNote : t.changed}</span>
        <span className={`badge-status ${draft.status}`}>{t.status[draft.status]}</span>
      </div>
      {draft.verdicts && <p className="verdicts">{draft.verdicts}</p>}
      <div className="choices">
        <button onClick={() => void toggle()}>{open ? t.hide : t.show}</button>
        {draft.status !== "wanted" && <button onClick={() => void decide("wanted")} disabled={working}>{t.want}</button>}
        {draft.status !== "discarded" && <button onClick={() => void decide("discarded")} disabled={working}>{t.discard}</button>}
        {draft.status !== "open" && <button onClick={() => void decide("open")} disabled={working}>{t.reset}</button>}
      </div>
      {open && detail && (
        <div className="draft-detail">
          <details open>
            <summary>{t.report}</summary>
            <div className="report">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{detail.review}</ReactMarkdown>
            </div>
          </details>
          <details>
            <summary>{t.diff}</summary>
            <Diff text={detail.diff} />
          </details>
        </div>
      )}
    </li>
  );
}

function Inbox({ branch, language, onDone }: { branch: InboxBranch; language: Language; onDone: (message: string, error?: boolean) => void }) {
  const t = TEXT[language];
  const [working, setWorking] = useState(false);

  async function act(accept: boolean) {
    setWorking(true);
    try {
      if (accept) onDone(t.accepted((await reviewApi.accept(branch.branch)).files));
      else onDone(t.discarded((await reviewApi.discard(branch.branch)).discarded));
    } catch (error) {
      onDone((error as Error).message, true);
    } finally {
      setWorking(false);
    }
  }

  return (
    <article className="run-card">
      <h3>{branch.branch}</h3>
      {branch.files.map((file) => (
        <details key={file.path}>
          <summary>{file.title}</summary>
          <div className="report">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{file.text.replace(/^---[\s\S]*?\n---\n/, "")}</ReactMarkdown>
          </div>
        </details>
      ))}
      <div className="choices">
        <button onClick={() => void act(true)} disabled={working}>{t.accept}</button>
        <button onClick={() => void act(false)} disabled={working}>{t.discard}</button>
      </div>
    </article>
  );
}

export default function Review({ language }: { language: Language }) {
  const t = TEXT[language];
  const [overview, setOverview] = useState<ReviewOverview | null>(null);
  const [message, setMessage] = useState<{ text: string; error: boolean } | null>(null);

  async function load() {
    try {
      setOverview(await reviewApi.overview());
    } catch (error) {
      setMessage({ text: (error as Error).message, error: true });
    }
  }

  useEffect(() => {
    void load();
  }, []);

  const changed = (error?: string) => {
    if (error) setMessage({ text: error, error: true });
    void load();
  };

  async function removeRun(run: ProposalRun) {
    if (!window.confirm(t.confirmRemove(run.run))) return;
    try {
      await reviewApi.removeRun(run.run);
      void load();
    } catch (error) {
      setMessage({ text: (error as Error).message, error: true });
    }
  }

  if (!overview) return <p className="thinking">{message?.text ?? t.loading}</p>;

  return (
    <div className="review">
      <div className="toolbar">
        <span />
        <button className="text-link" onClick={() => void load()}>
          {t.reload}
        </button>
      </div>
      {message && <p className={message.error ? "notice" : "success"}>{message.text}</p>}

      <section>
        <h2>{t.publicTitle}</h2>
        <p className="subtitle">{t.publicNote}</p>
        {!overview.public.available && <p className="empty">{t.noBranches}</p>}
        {overview.public.available && !overview.public.runs.length && <p className="empty">{t.noRuns}</p>}
        {overview.public.runs.map((run) => (
          <article key={run.run} className="run-card">
            <div className="draft-head">
              <h3>
                {t.run} {run.run}
              </h3>
              <button className="text-link" onClick={() => void removeRun(run)}>
                {t.removeRun}
              </button>
            </div>
            <ul className="draft-list">
              {run.drafts.map((draft) => (
                <Draft key={draft.slug} run={run.run} draft={draft} language={language} onChange={changed} />
              ))}
            </ul>
          </article>
        ))}
      </section>

      <section>
        <h2>{t.privateTitle}</h2>
        <p className="subtitle">{t.privateNote}</p>
        {!overview.private.configured && <p className="empty">{t.noPrivate}</p>}
        {overview.private.error && <p className="notice">{overview.private.error}</p>}
        {overview.private.configured && !overview.private.error && !overview.private.branches.length && <p className="empty">{t.noInbox}</p>}
        {overview.private.branches.map((branch) => (
          <Inbox
            key={branch.branch}
            branch={branch}
            language={language}
            onDone={(text, error) => {
              setMessage({ text, error: !!error });
              void load();
            }}
          />
        ))}
      </section>
    </div>
  );
}
