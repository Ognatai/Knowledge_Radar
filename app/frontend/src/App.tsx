import { FormEvent, KeyboardEvent, useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { ask, ChatSource, Language, publicNoteUrl, Scope, Turn } from "./api";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: ChatSource[];
  facts?: string[];
  unavailable?: string[];
  error?: boolean;
}

const TEXT = {
  de: {
    subtitle: "Lokaler Chat über die öffentliche und die private Wissensbasis. Alles bleibt auf diesem Rechner.",
    chat: "Chat",
    review: "Review",
    soon: "folgt",
    scope: "Suchen in",
    scopes: { all: "Beiden", public: "Öffentlich", private: "Privat" } as Record<Scope, string>,
    placeholder: "Frage stellen … (Enter sendet, Umschalt+Enter für neue Zeile)",
    send: "Senden",
    thinking: "Sucht und formuliert die Antwort …",
    newChat: "Neues Gespräch",
    sources: "Quellen",
    facts: "Zusammenhänge aus dem Graphen",
    private: "privat",
    unavailable: (names: string) => `Nicht erreichbar: ${names === "private" ? "privater Index" : names === "public" ? "öffentlicher Index" : names}. Die Antwort nutzt nur den Rest.`,
    memory: "Der Chat kennt die bisherigen Fragen dieses Gesprächs. „Neues Gespräch“ vergisst sie.",
    empty: "Zum Beispiel: „Wie hängen Prompt Injection und MCP zusammen?“",
  },
  en: {
    subtitle: "Local chat over the public and the private knowledge base. Everything stays on this machine.",
    chat: "Chat",
    review: "Review",
    soon: "coming",
    scope: "Search in",
    scopes: { all: "Both", public: "Public", private: "Private" } as Record<Scope, string>,
    placeholder: "Ask a question … (Enter sends, Shift+Enter for a new line)",
    send: "Send",
    thinking: "Searching and writing the answer …",
    newChat: "New conversation",
    sources: "Sources",
    facts: "Connections from the graph",
    private: "private",
    unavailable: (names: string) => `Not reachable: ${names === "private" ? "private index" : names === "public" ? "public index" : names}. The answer uses the rest only.`,
    memory: "The chat knows the earlier questions of this conversation. “New conversation” forgets them.",
    empty: "For example: “How are prompt injection and MCP related?”",
  },
};

// Kept in the tab only: closing it ends the conversation; the server stores nothing.
const STORAGE_KEY = "knowledge-radar-chat";

function loadMessages(): Message[] {
  try {
    return JSON.parse(sessionStorage.getItem(STORAGE_KEY) ?? "[]");
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
  const [busy, setBusy] = useState(false);
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

  async function submit(event?: FormEvent) {
    event?.preventDefault();
    const text = question.trim();
    if (!text || busy) return;
    const history: Turn[] = messages.filter((m) => !m.error).map(({ role, content }) => ({ role, content }));
    setMessages((current) => [...current, { role: "user", content: text }]);
    setQuestion("");
    setBusy(true);
    try {
      const answer = await ask(text, history, scope, language);
      setMessages((current) => [
        ...current,
        { role: "assistant", content: answer.answer, sources: answer.sources, facts: answer.facts, unavailable: answer.unavailable },
      ]);
    } catch (error) {
      setMessages((current) => [...current, { role: "assistant", content: String((error as Error).message), error: true }]);
    } finally {
      setBusy(false);
    }
  }

  function onKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void submit();
    }
  }

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
          <button className="text-link" onClick={() => setMessages([])} disabled={busy || !messages.length}>
            {t.newChat}
          </button>
        </div>

        <section className="messages" aria-live="polite">
          {!messages.length && <p className="empty">{t.empty}</p>}
          {messages.map((message, index) => (
            <article key={index} className={`message ${message.role}${message.error ? " error" : ""}`}>
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
                </>
              ) : (
                <p>{message.content}</p>
              )}
            </article>
          ))}
          {busy && <p className="thinking">{t.thinking}</p>}
          <div ref={end} />
        </section>

        <form className="ask" onSubmit={submit}>
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            onKeyDown={onKeyDown}
            placeholder={t.placeholder}
            rows={3}
            maxLength={2000}
            aria-label={t.placeholder}
          />
          <button type="submit" disabled={busy || !question.trim()}>
            {t.send}
          </button>
        </form>
        {!!messages.length && <p className="memory">{t.memory}</p>}
      </main>
    </div>
  );
}
