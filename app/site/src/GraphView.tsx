import { useEffect, useMemo, useRef, useState } from "react";
import ForceGraph2D, { type NodeObject } from "react-force-graph-2d";
import { useTranslation } from "react-i18next";
import { nodeLabel, type GraphEdge, type GraphNode } from "./data";
import type { Language } from "./i18n";

const ENTITY_COLORS: Record<string, string> = {
  Method: "#177d66",
  Regulation: "#a3552a",
  Person: "#6a4c9c",
  Organization: "#2f6aa3",
  Conference: "#9c7a1c",
  Concept: "#b0466b",
  Technology: "#3d7f8f",
  Source: "#5f6b66",
};
const NOTE_COLOR = "#8f9a94";
const EDGE_COLORS: Record<string, string> = {
  DISCUSSES: "#c9d3ce",
  RELATED_TO: "#8eafa2",
};
// Entity-to-entity relations (BASED_ON, REGULATES, ...) are directed facts.
const RELATION_COLOR = "#5c6f68";
const isRelation = (edge: GraphEdge) => !(edge.type in EDGE_COLORS);

type RenderedNode = NodeObject<GraphNode & { label: string }>;

interface GraphViewProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  language: Language;
  openNode: (node: GraphNode) => void;
}

function escapeHtml(text: string): string {
  return text.replace(/[&<>"']/g, (char) => `&#${char.charCodeAt(0)};`);
}

export function GraphView({ nodes, edges, language, openNode }: GraphViewProps) {
  const { t } = useTranslation();
  const containerRef = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(800);
  const [showNotes, setShowNotes] = useState(false);
  const entityTypes = useMemo(
    () => [...new Set(nodes.flatMap((node) => (node.kind === "entity" ? [node.entity_type] : [])))].sort(),
    [nodes],
  );
  const [hiddenTypes, setHiddenTypes] = useState<Set<string>>(new Set());

  useEffect(() => {
    const element = containerRef.current;
    if (!element) return;
    const observer = new ResizeObserver(([entry]) => setWidth(Math.floor(entry.contentRect.width)));
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  const visibleNodes = useMemo(
    () =>
      nodes.filter((node) =>
        node.kind === "note" ? showNotes : !hiddenTypes.has(node.entity_type),
      ),
    [hiddenTypes, nodes, showNotes],
  );

  // force-graph mutates the objects it receives, so it gets fresh copies.
  const graphData = useMemo(() => {
    const ids = new Set(visibleNodes.map((node) => node.id));
    return {
      nodes: visibleNodes.map((node) => ({ ...node, label: nodeLabel(node, language) })),
      links: edges
        .filter((edge) => ids.has(edge.source) && ids.has(edge.target))
        .map((edge) => ({ ...edge })),
    };
  }, [edges, language, visibleNodes]);

  const height = width < 600 ? 380 : 520;

  function toggleType(type: string) {
    setHiddenTypes((current) => {
      const next = new Set(current);
      if (next.has(type)) next.delete(type);
      else next.add(type);
      return next;
    });
  }

  return (
    <>
      <div className="graph-controls">
        <label className="toggle">
          <input checked={showNotes} onChange={(event) => setShowNotes(event.target.checked)} type="checkbox" />
          {t("showNotes")}
        </label>
        <fieldset className="type-filter">
          <legend className="visually-hidden">{t("filterByType")}</legend>
          {entityTypes.map((type) => (
            <label className="type-chip" key={type}>
              <input checked={!hiddenTypes.has(type)} onChange={() => toggleType(type)} type="checkbox" />
              <span className="type-swatch" style={{ background: ENTITY_COLORS[type] ?? NOTE_COLOR }} />
              {type}
            </label>
          ))}
        </fieldset>
      </div>
      <div className="graph-canvas" ref={containerRef}>
        {graphData.nodes.length === 0 ? (
          <p className="muted graph-empty">{t("graphEmpty")}</p>
        ) : (
          <ForceGraph2D<GraphNode & { label: string }, GraphEdge>
            backgroundColor="#fffefa"
            cooldownTicks={120}
            graphData={graphData}
            height={height}
            linkColor={(link) => EDGE_COLORS[link.type] ?? RELATION_COLOR}
            linkDirectionalArrowLength={(link) => (isRelation(link) ? 4 : 0)}
            linkDirectionalArrowRelPos={1}
            linkLabel={(link) => escapeHtml(link.type)}
            linkWidth={(link) => (link.type === "RELATED_TO" ? 2 : link.type === "DISCUSSES" ? 1 : 1.5)}
            nodeCanvasObject={(node: RenderedNode, context, scale) => {
              const x = node.x ?? 0;
              const y = node.y ?? 0;
              const radius = node.kind === "entity" ? 7 : 5;
              context.fillStyle = node.kind === "entity" ? ENTITY_COLORS[node.entity_type] ?? NOTE_COLOR : NOTE_COLOR;
              context.beginPath();
              if (node.kind === "entity") context.arc(x, y, radius, 0, 2 * Math.PI);
              else context.rect(x - radius, y - radius, radius * 2, radius * 2);
              context.fill();
              const fontSize = Math.max(11 / scale, 2.5);
              context.font = `${node.kind === "entity" ? 600 : 400} ${fontSize}px "Segoe UI", Arial, sans-serif`;
              context.textAlign = "center";
              context.textBaseline = "top";
              context.fillStyle = "#202b28";
              context.fillText(node.label, x, y + radius + 2);
            }}
            nodeLabel={(node) => escapeHtml(node.label)}
            nodePointerAreaPaint={(node: RenderedNode, color, context) => {
              context.fillStyle = color;
              context.beginPath();
              context.arc(node.x ?? 0, node.y ?? 0, 10, 0, 2 * Math.PI);
              context.fill();
            }}
            onNodeClick={(node) => openNode(node)}
            width={width}
          />
        )}
      </div>
      <p className="graph-caption">{t("graphCaption")}</p>
      {/* The canvas is not keyboard accessible; the same nodes as a list. */}
      <details className="graph-node-list">
        <summary>{t("graphNodeList")} ({graphData.nodes.length})</summary>
        <ul>
          {graphData.nodes.map((node) => (
            <li key={node.id}>
              <button className="text-link" onClick={() => openNode(node)} type="button">
                {node.label}
              </button>
              <span className="muted">
                {node.kind === "entity"
                  ? node.note ? node.entity_type : t("entityWithoutNote", { type: node.entity_type })
                  : t("navNotes")}
              </span>
            </li>
          ))}
        </ul>
      </details>
    </>
  );
}
