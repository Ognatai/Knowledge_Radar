// The documents tab: per application and round, the saved preparation and the study
// guide, rendered and printable as PDF (for reading on the phone). Both are built from
// the files when opened, so they include notes added later.
import { useEffect, useState } from "react";
import { Application, Language, privateApi } from "./api";
import Markdown from "./Markdown";

const TEXT = {
  de: {
    title: "Unterlagen",
    intro: "Vorbereitung und Lernunterlage je Gesprächsrunde. Beide werden beim Öffnen aus den Dateien erstellt und sind damit immer aktuell.",
    loading: "Lädt …",
    noPrivate: "Kein privates Repository konfiguriert.",
    none: "Noch keine Bewerbung. Lege eine im Chat mit /new-application an.",
    round: "Runde",
    dateOpen: "Datum offen",
    prep: "Vorbereitung",
    noPrep: "Vorbereitung (noch keine, /prep im Chat)",
    guide: "Lernunterlage",
    back: "Zurück zur Übersicht",
    pdf: "Als PDF speichern",
    pdfHint: "Im Druckdialog „Als PDF speichern“ wählen.",
  },
  en: {
    title: "Documents",
    intro: "Preparation and study guide per interview round. Both are built from the files when opened, so they are always current.",
    loading: "Loading …",
    noPrivate: "No private repository configured.",
    none: "No application yet. Start one in the chat with /new-application.",
    round: "Round",
    dateOpen: "date open",
    prep: "Preparation",
    noPrep: "Preparation (none yet, /prep in the chat)",
    guide: "Study guide",
    back: "Back to the overview",
    pdf: "Save as PDF",
    pdfHint: "Choose “Save as PDF” in the print dialog.",
  },
};

interface Open {
  title: string;
  markdown: string;
}

export default function Documents({ language }: { language: Language }) {
  const t = TEXT[language];
  const [applications, setApplications] = useState<Application[] | null>(null);
  const [configured, setConfigured] = useState(true);
  const [open, setOpen] = useState<Open | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    privateApi
      .applications()
      .then((result) => {
        setConfigured(result.configured);
        setApplications(result.applications);
      })
      .catch((e: Error) => setError(e.message));
  }, []);

  async function show(kind: "prep" | "study-guide", application: Application, round: number) {
    setLoading(true);
    setError("");
    try {
      const { markdown } = await privateApi.document(application.company, application.role, round, kind);
      const name = kind === "prep" ? t.prep : t.guide;
      setOpen({ title: `${name}: ${application.company_name} – ${application.role_title}, ${t.round} ${round}`, markdown });
      window.scrollTo(0, 0);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }

  function print(title: string) {
    // The PDF's default file name is the page title.
    const previous = document.title;
    document.title = title;
    window.print();
    document.title = previous;
  }

  if (open) {
    return (
      <section className="documents">
        <div className="document-actions no-print">
          <button className="text-link" onClick={() => setOpen(null)}>← {t.back}</button>
          <button className="primary" onClick={() => print(open.title)} title={t.pdfHint}>{t.pdf}</button>
        </div>
        <article className="document">
          <Markdown text={open.markdown} />
        </article>
      </section>
    );
  }

  return (
    <section className="documents">
      <h2>{t.title}</h2>
      <p className="subtitle">{t.intro}</p>
      {error && <p className="notice">{error}</p>}
      {!configured && <p className="empty">{t.noPrivate}</p>}
      {applications === null && !error && <p className="thinking">{t.loading}</p>}
      {applications?.length === 0 && configured && <p className="empty">{t.none}</p>}
      {loading && <p className="thinking">{t.loading}</p>}
      {applications?.map((application) => (
        <div className="run-card" key={`${application.company}/${application.role}`}>
          <h3>{application.company_name} – {application.role_title}</h3>
          <ul className="draft-list">
            {application.rounds.map((round) => (
              <li className="draft-row" key={round.number}>
                <div className="draft-head">
                  <strong>{t.round} {round.number} <span className="kind">({round.date ?? t.dateOpen})</span></strong>
                  <button className="text-link" disabled={!round.has_prep || loading} onClick={() => show("prep", application, round.number)}>
                    {round.has_prep ? t.prep : t.noPrep}
                  </button>
                  <button className="text-link" disabled={loading} onClick={() => show("study-guide", application, round.number)}>
                    {t.guide}
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </section>
  );
}
