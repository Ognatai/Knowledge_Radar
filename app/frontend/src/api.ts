export type Scope = "all" | "public" | "private";
export type Language = "de" | "en";

export interface Turn {
  role: "user" | "assistant";
  content: string;
}

export interface ChatSource {
  number: number;
  note: string;
  title: string;
  heading: string;
  visibility: "public" | "private";
  text: string;
  score: number;
}

export interface ChatAnswer {
  answer: string;
  sources: ChatSource[];
  facts: string[];
  unavailable: string[];
}

// Public notes open on the published site; private documents have no public address.
export const PUBLIC_SITE = "https://ognatai.github.io/Knowledge_Radar/";

export function publicNoteUrl(slug: string): string {
  return `${PUBLIC_SITE}?view=note&slug=${encodeURIComponent(slug)}`;
}

export async function ask(question: string, history: Turn[], scope: Scope, language: Language): Promise<ChatAnswer> {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, history, scope, language }),
  });
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      detail = (await response.json()).detail ?? detail;
    } catch {
      // not JSON (e.g. nginx error page); keep the status line
    }
    throw new Error(String(detail));
  }
  return response.json();
}
