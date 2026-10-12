// Markdown with heading ids, so that a document's table of contents can link to its
// chapters. The id rule matches `anchor` in app/backend/knowledge_radar/study_guide.py.
import { Children, createElement, isValidElement, ReactNode } from "react";
import ReactMarkdown, { Components } from "react-markdown";
import remarkGfm from "remark-gfm";

function textOf(node: ReactNode): string {
  return Children.toArray(node)
    .map((child) => (typeof child === "string" || typeof child === "number" ? String(child) : isValidElement(child) ? textOf(child.props.children) : ""))
    .join("");
}

export function anchor(text: string): string {
  return text.toLocaleLowerCase().replace(/[^\p{L}\p{N}]+/gu, "-").replace(/^-+|-+$/g, "");
}

const heading = (level: number) =>
  function Heading({ children }: { children?: ReactNode }) {
    return createElement(`h${level}`, { id: anchor(textOf(children)) }, children);
  };

const components: Components = {
  h1: heading(1),
  h2: heading(2),
  h3: heading(3),
  h4: heading(4),
  // Links within the document jump; others open in a new tab.
  a: ({ href, children }) =>
    href?.startsWith("#") ? <a href={href}>{children}</a> : <a href={href} target="_blank" rel="noreferrer">{children}</a>,
};

export default function Markdown({ text }: { text: string }) {
  return <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>{text}</ReactMarkdown>;
}
