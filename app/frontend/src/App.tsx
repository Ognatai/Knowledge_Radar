import { FormEvent, KeyboardEvent, useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Application, ask, ChatSource, Language, privateApi, publicNoteUrl, RefreshStatus, Scope, Turn, Written } from "./api";
import {
  Choice,
  CommandName,
  COMMANDS,
  confirmed,
  parseInterviewers,
  retroDate,
  SKIP,
  startWizard,
  text as stepText,
  value,
  Wizard,
} from "./commands";

interface Draft {
  kind: "retro" | "prep";
  text: string;
  company: string;
  role: string;
  round: number;
  // A prep.md exists already: saving replaces it.
  exists?: boolean;
  state: "editing" | "saving" | "saved" | "cancelled";
}

interface Message {
  id: number;
  role: "user" | "assistant";
  content: string;
  // Command dialogue (/new-application …): never sent to the model as chat history.
  command?: boolean;
  sources?: ChatSource[];
  facts?: string[];
  unavailable?: string[];
  error?: boolean;
  choices?: Choice[];
  draft?: Draft;
  refresh?: RefreshStatus;
}

const TEXT = {
  de: {
    subtitle: "Lokaler Chat über die öffentliche und die private Wissensbasis. Alles bleibt auf diesem Rechner.",
    chat: "Chat",
    review: "Review",
    soon: "folgt",
    scope: "Suchen in",
    scopes: { all: "Beiden", public: "Öffentlich", private: "Privat" } as Record<Scope, string>,
    placeholder: "Frage stellen oder / für Befehle … (Enter sendet, Umschalt+Enter für neue Zeile)",
    send: "Senden",
    thinking: "Sucht und formuliert die Antwort …",
    working: "Arbeitet …",
    newChat: "Neues Gespräch",
    sources: "Quellen",
    facts: "Zusammenhänge aus dem Graphen",
    private: "privat",
    unavailable: (name: string) => `Nicht erreichbar: ${name === "private" ? "privater Index" : name === "public" ? "öffentlicher Index" : name}. Die Antwort nutzt nur den Rest.`,
    memory: "Der Chat kennt die bisherigen Fragen dieses Gesprächs. „Neues Gespräch“ vergisst sie.",
    empty: "Zum Beispiel: „Wie hängen Prompt Injection und MCP zusammen?“ – oder ein Befehl:",
    skip: "Überspringen",
    cancel: "Abbrechen",
    cancelled: "Abgebrochen, nichts gespeichert.",
    cancelWords: ["abbrechen", "abbruch", "cancel", "stop"],
    unknownCommand: "Unbekannter Befehl. Es gibt:",
    noPrivate: "Für diesen Befehl braucht die App das private Repository (private_repo_path, siehe SETUP.md).",
    pickChoice: "Bitte wähle eine der Möglichkeiten oben (Klick oder Nummer).",
    saved: (files: string[]) => `Gespeichert im privaten Repository:\n${files.map((f) => `- \`${f}\``).join("\n")}\n\nDie Dateien sind noch nicht committet.`,
    draftIntro: "Entwurf der Retro. Prüfe und ändere ihn bei Bedarf, dann speichern:",
    prepIntro: "Entwurf der Vorbereitung. Prüfe ihn, vor allem die Kurzvorstellung (Platzhalter in [eckigen Klammern] füllst du selbst):",
    saveDraft: "Retro speichern",
    savePrep: "Vorbereitung speichern",
    replacePrep: "Vorhandene Vorbereitung überschreiben",
    preparing: "Erstellt die Vorbereitung (Anforderungen, frühere Runden, Kurzvorstellung, Fragen) …",
    refreshing: "Aktualisiere den privaten Index (Struktur, lokale Extraktion, Embeddings) …",
    refreshed: "Privater Index aktualisiert. Die neuen Daten sind im Chat verfügbar.",
    refreshFailed: (message: string) => `Aktualisierung fehlgeschlagen: ${message}`,
  },
  en: {
    subtitle: "Local chat over the public and the private knowledge base. Everything stays on this machine.",
    chat: "Chat",
    review: "Review",
    soon: "coming",
    scope: "Search in",
    scopes: { all: "Both", public: "Public", private: "Private" } as Record<Scope, string>,
    placeholder: "Ask a question or type / for commands … (Enter sends, Shift+Enter for a new line)",
    send: "Send",
    thinking: "Searching and writing the answer …",
    working: "Working …",
    newChat: "New conversation",
    sources: "Sources",
    facts: "Connections from the graph",
    private: "private",
    unavailable: (name: string) => `Not reachable: ${name === "private" ? "private index" : name === "public" ? "public index" : name}. The answer uses the rest only.`,
    memory: "The chat knows the earlier questions of this conversation. “New conversation” forgets them.",
    empty: "For example: “How are prompt injection and MCP related?” – or a command:",
    skip: "Skip",
    cancel: "Cancel",
    cancelled: "Cancelled, nothing saved.",
    cancelWords: ["abbrechen", "cancel", "stop"],
    unknownCommand: "Unknown command. Available:",
    noPrivate: "This command needs the private repository (private_repo_path, see SETUP.md).",
    pickChoice: "Please pick one of the options above (click or number).",
    saved: (files: string[]) => `Saved in the private repository:\n${files.map((f) => `- \`${f}\``).join("\n")}\n\nThe files are not committed yet.`,
    draftIntro: "Draft of the retro. Check it, change what you like, then save:",
    prepIntro: "Draft of the preparation. Check it, above all the self-introduction (fill in the [placeholders] yourself):",
    saveDraft: "Save retro",
    savePrep: "Save preparation",
    replacePrep: "Replace the existing preparation",
    preparing: "Writing the preparation (requirements, earlier rounds, introduction, questions) …",
    refreshing: "Updating the private index (structure, local extraction, embeddings) …",
    refreshed: "Private index updated. The new data is available in the chat.",
    refreshFailed: (message: string) => `Update failed: ${message}`,
  },
};

// Kept in the tab only: closing it ends the conversation; the server stores nothing.
const STORAGE_KEY = "knowledge-radar-chat";
let nextId = Date.now();
const newId = () => ++nextId;

function loadMessages(): Message[] {
  try {
    const stored: Message[] = JSON.parse(sessionStorage.getItem(STORAGE_KEY) ?? "[]");
    // A dialogue cannot be resumed after a reload: drop its buttons.
    return stored.map((m) => ({ ...m, choices: undefined, draft: m.draft?.state === "editing" ? { ...m.draft, state: "cancelled" } : m.draft }));
  } catch {
    return [];
  }
}

function Sources({ sources, label, privateLabel }: { sources: ChatSource[]; label: string; privateLabel: string }) {
  if (!sources.length) return null;
  return (
    <details className="sources">
      <summary>
        {label} ({sources.length})
      </summary>
      <ol>
        {sources.map((source) => (
          <li key={source.number} value={source.number}>
            {source.visibility === "public" ? (
              <a href={publicNoteUrl(source.note)} target="_blank" rel="noreferrer">
                {source.title}
              </a>
            ) : (
              <span>{source.title}</span>
            )}
            {source.heading && <span className="heading"> · {source.heading}</span>}
            {source.visibility === "private" && <span className="badge">{privateLabel}</span>}
            <p>{source.text}</p>
          </li>
        ))}
      </ol>
    </details>
  );
}

export default function App() {
  const [language, setLanguage] = useState<Language>("de");
  const [scope, setScope] = useState<Scope>("all");
  const [messages, setMessages] = useState<Message[]>(loadMessages);
  const [question, setQuestion] = useState("");
  const [busy, setBusy] = useState<"" | "chat" | "command">("");
  const [wizard, setWizard] = useState<Wizard | null>(null);
  const [applications, setApplications] = useState<Application[]>([]);
  const [preparing, setPreparing] = useState(false);
  const end = useRef<HTMLDivElement>(null);
  const t = TEXT[language];

  useEffect(() => {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    } catch {
      // storage unavailable: the conversation still works in memory
    }
    end.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, busy]);

  const add = (message: Omit<Message, "id">) => {
    const id = newId();
    setMessages((current) => [...current.map((m) => ({ ...m, choices: undefined })), { ...message, id }]);
    return id;
  };
  const update = (id: number, change: Partial<Message>) =>
    setMessages((current) => current.map((m) => (m.id === id ? { ...m, ...change } : m)));

  function ask_step(next: Wizard) {
    const step = next.steps[next.index];
    const choices = [...(step.choices ?? []), ...(step.optional ? [{ label: t.skip, value: SKIP }] : []), { label: t.cancel, value: "cancel" }];
    add({ role: "assistant", content: stepText(step.prompt, next.answers, language), command: true, choices });
  }

  function trackRefresh(status: RefreshStatus | null) {
    if (!status) return;
    const id = add({ role: "assistant", content: t.refreshing, command: true, refresh: status });
    const poll = window.setInterval(async () => {
      try {
        const current = await privateApi.refresh();
        if (!current || current.state === "running") return;
        window.clearInterval(poll);
        update(id, { content: current.state === "done" ? t.refreshed : t.refreshFailed(current.message), refresh: current, error: current.state === "failed" });
      } catch (error) {
        window.clearInterval(poll);
        update(id, { content: t.refreshFailed((error as Error).message), error: true });
      }
    }, 3000);
  }

  function reportWritten(result: Written) {
    add({ role: "assistant", content: t.saved(result.files), command: true });
    trackRefresh(result.refresh);
  }

  async function finish(done: Wizard) {
    setWizard(null);
    const a = done.answers;
    if (done.command !== "/retro" && done.command !== "/prep" && !confirmed(done)) {
      add({ role: "assistant", content: t.cancelled, command: true });
      return;
    }
    setBusy("command");
    setPreparing(done.command === "/prep");
    try {
      const round = { round_date: value(a, "round_date") || null, round_notes: value(a, "round_notes"), interviewers: parseInterviewers(a.interviewers ?? SKIP) };
      if (done.command === "/new-application") {
        reportWritten(
          await privateApi.newApplication({
            company_name: a.company_name, industry: value(a, "industry"), role_title: a.role_title,
            posting_text: a.posting_text, posting_url: value(a, "posting_url"), ...round,
          }),
        );
      } else if (done.command === "/prep") {
        const [company, role, number] = a.round.split("/");
        const draft = await privateApi.draftPrep({ company, role, round: Number(number), language });
        add({
          role: "assistant", content: t.prepIntro, command: true,
          draft: { kind: "prep", text: draft.text, company, role, round: Number(number), exists: draft.exists, state: "editing" },
        });
      } else if (done.command === "/new-round") {
        const [company, role] = a.application.split("/");
        reportWritten(await privateApi.newRound({ company, role, ...round }));
      } else {
        const [company, role, number] = a.round.split("/");
        const draft = await privateApi.draftRetro({
          date: retroDate(done, applications),
          questions_asked: value(a, "questions_asked"), struggled_with: value(a, "struggled_with"),
          personal_improvement: value(a, "personal_improvement"), kb_gaps_identified: value(a, "kb_gaps_identified"),
          reflection: value(a, "reflection"),
        });
        add({ role: "assistant", content: t.draftIntro, command: true, draft: { kind: "retro", text: draft.text, company, role, round: Number(number), state: "editing" } });
      }
    } catch (error) {
      add({ role: "assistant", content: (error as Error).message, command: true, error: true });
    } finally {
      setBusy("");
      setPreparing(false);
    }
  }

  async function saveDraft(message: Message) {
    const draft = message.draft!;
    update(message.id, { draft: { ...draft, state: "saving" } });
    try {
      const place = { company: draft.company, role: draft.role, round: draft.round, text: draft.text };
      const result = draft.kind === "prep" ? await privateApi.savePrep({ ...place, replace: !!draft.exists }) : await privateApi.saveRetro(place);
      update(message.id, { draft: { ...draft, state: "saved" } });
      reportWritten(result);
    } catch (error) {
      update(message.id, { draft: { ...draft, state: "editing" } });
      add({ role: "assistant", content: (error as Error).message, command: true, error: true });
    }
  }

  function answer(current: Wizard, input: string, label?: string) {
    add({ role: "user", content: label ?? input, command: true });
    const cleaned = input.trim();
    if (cleaned === "cancel" || t.cancelWords.includes(cleaned.toLowerCase())) {
      setWizard(null);
      add({ role: "assistant", content: t.cancelled, command: true });
      return;
    }
    const step = current.steps[current.index];
    let given = cleaned;
    if (step.choices) {
      const byNumber = step.choices[Number(cleaned) - 1];
      const match = step.choices.find((c) => c.value === cleaned || c.label.toLowerCase() === cleaned.toLowerCase()) ?? byNumber;
      if (!match && !(step.optional && cleaned === SKIP)) {
        add({ role: "assistant", content: t.pickChoice, command: true });
        ask_step(current);
        return;
      }
      given = match?.value ?? SKIP;
    }
    if (!given || (given === SKIP && !step.optional)) {
      ask_step(current);
      return;
    }
    const problem = step.validate?.(given);
    if (problem) {
      add({ role: "assistant", content: problem[language], command: true });
      ask_step(current);
      return;
    }
    const next = { ...current, index: current.index + 1, answers: { ...current.answers, [step.key]: given } };
    if (next.index < next.steps.length) {
      setWizard(next);
      ask_step(next);
    } else {
      void finish(next);
    }
  }

  async function startCommand(command: string) {
    add({ role: "user", content: command, command: true });
    if (!(command in COMMANDS)) {
      add({ role: "assistant", content: `${t.unknownCommand}\n${commandList()}`, command: true });
      return;
    }
    setBusy("command");
    try {
      const listed = await privateApi.applications();
      if (!listed.configured) {
        add({ role: "assistant", content: t.noPrivate, command: true, error: true });
        return;
      }
      setApplications(listed.applications);
      const started = startWizard(command as CommandName, listed.applications, language);
      if (typeof started === "string") {
        add({ role: "assistant", content: started, command: true });
        return;
      }
      setWizard(started);
      ask_step(started);
    } catch (error) {
      add({ role: "assistant", content: (error as Error).message, command: true, error: true });
    } finally {
      setBusy("");
    }
  }

  function commandList() {
    return (Object.keys(COMMANDS) as CommandName[]).map((name) => `- \`${name}\`: ${COMMANDS[name][language]}`).join("\n");
  }

  async function chat(text: string) {
    const history: Turn[] = messages.filter((m) => !m.error && !m.command).map(({ role, content }) => ({ role, content }));
    add({ role: "user", content: text });
    setBusy("chat");
    try {
      const result = await ask(text, history, scope, language);
      add({ role: "assistant", content: result.answer, sources: result.sources, facts: result.facts, unavailable: result.unavailable });
    } catch (error) {
      add({ role: "assistant", content: (error as Error).message, error: true });
    } finally {
      setBusy("");
    }
  }

  function submit(event?: FormEvent) {
    event?.preventDefault();
    const text = question.trim();
    if (!text || busy) return;
    setQuestion("");
    if (wizard) answer(wizard, text);
    else if (text.startsWith("/")) void startCommand(text.split(/\s+/)[0].toLowerCase());
    else void chat(text);
  }

  function onKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      submit();
    }
  }

  const typedCommand = !wizard && question.startsWith("/") && !question.includes("\n");
  const suggestions = typedCommand ? (Object.keys(COMMANDS) as CommandName[]).filter((name) => name.startsWith(question.trim().toLowerCase())) : [];

  return (
    <div className="page-shell">
      <header className="topbar">
        <span className="brand">
          <span className="brand-mark" aria-hidden="true">◎</span> Knowledge Radar <span className="local">lokal</span>
        </span>
        <nav className="primary-nav" aria-label="Main">
          <button aria-current="page">{t.chat}</button>
          <button disabled title={t.soon}>
            {t.review} <small>({t.soon})</small>
          </button>
        </nav>
        <div className="language-toggle" role="group" aria-label="Language">
          {(["de", "en"] as Language[]).map((code) => (
            <button key={code} className={language === code ? "selected" : ""} onClick={() => setLanguage(code)}>
              {code.toUpperCase()}
            </button>
          ))}
        </div>
      </header>

      <main className="chat">
        <p className="subtitle">{t.subtitle}</p>
        <div className="toolbar">
          <div className="scope" role="group" aria-label={t.scope}>
            <span>{t.scope}</span>
            {(["all", "public", "private"] as Scope[]).map((option) => (
              <button key={option} className={scope === option ? "selected" : ""} onClick={() => setScope(option)}>
                {t.scopes[option]}
              </button>
            ))}
          </div>
          <button
            className="text-link"
            onClick={() => {
              setMessages([]);
              setWizard(null);
            }}
            disabled={!!busy || !messages.length}
          >
            {t.newChat}
          </button>
        </div>

        <section className="messages" aria-live="polite">
          {!messages.length && (
            <div className="empty">
              <p>{t.empty}</p>
              <ReactMarkdown>{commandList()}</ReactMarkdown>
            </div>
          )}
          {messages.map((message) => (
            <article key={message.id} className={`message ${message.role}${message.error ? " error" : ""}${message.command ? " command" : ""}`}>
              {message.role === "assistant" ? (
                <>
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
                  {message.unavailable?.map((name) => (
                    <p key={name} className="notice">
                      {t.unavailable(name)}
                    </p>
                  ))}
                  <Sources sources={message.sources ?? []} label={t.sources} privateLabel={t.private} />
                  {!!message.facts?.length && (
                    <details className="sources">
                      <summary>{t.facts}</summary>
                      <ul>
                        {message.facts.map((fact) => (
                          <li key={fact}>{fact}</li>
                        ))}
                      </ul>
                    </details>
                  )}
                  {message.refresh?.state === "running" && <p className="thinking">{message.refresh.log[message.refresh.log.length - 1] ?? ""}</p>}
                  {message.choices && wizard && (
                    <div className="choices">
                      {message.choices.map((choice, index) => (
                        <button key={choice.value} onClick={() => answer(wizard, choice.value, choice.label)} disabled={!!busy}>
                          {choice.value !== SKIP && choice.value !== "cancel" && message.choices!.length > 3 ? `${index + 1}. ` : ""}
                          {choice.label}
                        </button>
                      ))}
                    </div>
                  )}
                  {message.draft && (
                    <div className="draft">
                      <textarea
                        value={message.draft.text}
                        readOnly={message.draft.state !== "editing"}
                        onChange={(event) => update(message.id, { draft: { ...message.draft!, text: event.target.value } })}
                        rows={Math.min(24, message.draft.text.split("\n").length + 2)}
                      />
                      {message.draft.state === "editing" && (
                        <div className="choices">
                          <button onClick={() => void saveDraft(message)}>
                            {message.draft.kind === "retro" ? t.saveDraft : message.draft.exists ? t.replacePrep : t.savePrep}
                          </button>
                          <button
                            onClick={() => {
                              update(message.id, { draft: { ...message.draft!, state: "cancelled" } });
                              add({ role: "assistant", content: t.cancelled, command: true });
                            }}
                          >
                            {t.cancel}
                          </button>
                        </div>
                      )}
                    </div>
                  )}
                </>
              ) : (
                <p>{message.content}</p>
              )}
            </article>
          ))}
          {busy && <p className="thinking">{busy === "chat" ? t.thinking : wizard === null && preparing ? t.preparing : t.working}</p>}
          <div ref={end} />
        </section>

        <form className="ask" onSubmit={submit}>
          {suggestions.length > 0 && (
            <ul className="suggestions" role="listbox">
              {suggestions.map((name) => (
                <li key={name}>
                  <button type="button" onClick={() => setQuestion(name)}>
                    <code>{name}</code> {COMMANDS[name][language]}
                  </button>
                </li>
              ))}
            </ul>
          )}
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            onKeyDown={onKeyDown}
            placeholder={t.placeholder}
            rows={3}
            maxLength={50000}
            aria-label={t.placeholder}
          />
          <button type="submit" disabled={!!busy || !question.trim()}>
            {t.send}
          </button>
        </form>
        {messages.some((m) => !m.command) && <p className="memory">{t.memory}</p>}
      </main>
    </div>
  );
}
