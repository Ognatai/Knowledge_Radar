import { forceCollide, forceX, forceY } from "d3-force-3d";
import { useEffect, useMemo, useRef, useState } from "react";
import ForceGraph2D, { type ForceGraphMethods, type LinkObject, type NodeObject } from "react-force-graph-2d";
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
  Dataset: "#7a6a3a",
  Source: "#5f6b66",
};
const NOTE_COLOR = "#8f9a94";
const EDGE_COLORS: Record<string, string> = {
  DISCUSSES: "#c9d3ce",
  RELATED_TO: "#8eafa2",
};
// Entity-to-entity relations (BASED_ON, REGULATES, ...) are directed facts.
// Translucent, so that crossings stay readable; a highlighted node's edges are drawn darker.
const RELATION_COLOR = "rgba(92, 111, 104, 0.3)";
const ACTIVE_EDGE = "#3f4d48";
const DIMMED_EDGE = "rgba(92, 111, 104, 0.07)";
const DIMMED_NODE_ALPHA = 0.15;
// A label is drawn when degree × zoom reaches this, so hubs are named first and
// the rest appear while zooming in; highlighted nodes are always named.
const LABEL_THRESHOLD = 6;
// The best-connected nodes are named at any zoom level.
const ALWAYS_LABELLED = 15;
// Weak pull to the centre, so that small separate clusters do not drift away and
// shrink the fitted view.
const GRAVITY = 0.06;
const isRelation = (edge: GraphEdge) => !(edge.type in EDGE_COLORS);

type RenderedNode = NodeObject<GraphNode & { label: string }>;
type RenderedLink = LinkObject<GraphNode & { label: string }, GraphEdge>;

interface GraphViewProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  language: Language;
  openNode: (node: GraphNode) => void;
}

function escapeHtml(text: string): string {
  return text.replace(/[&<>"']/g, (char) => `&#${char.charCodeAt(0)};`);
}

// After the simulation starts, force-graph replaces link endpoints by node objects.
function endpointId(endpoint: unknown): string {
  return typeof endpoint === "object" && endpoint !== null ? String((endpoint as { id: string }).id) : String(endpoint);
}

export function GraphView({ nodes, edges, language, openNode }: GraphViewProps) {
  const { t } = useTranslation();
  const containerRef = useRef<HTMLDivElement>(null);
  const graphRef = useRef<ForceGraphMethods<RenderedNode, RenderedLink>>();
  const fittedRef = useRef(false);
  const [width, setWidth] = useState(800);
  const [showNotes, setShowNotes] = useState(false);
  const [focusId, setFocusId] = useState<string | null>(null);
  const [hoverId, setHoverId] = useState<string | null>(null);
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

  const { graphData, neighbours, degree } = useMemo(() => {
    const ids = new Set(visibleNodes.map((node) => node.id));
    const links = edges.filter((edge) => ids.has(edge.source) && ids.has(edge.target));
    const neighbours = new Map<string, Set<string>>();
    for (const edge of links) {
      for (const [from, to] of [[edge.source, edge.target], [edge.target, edge.source]]) {
        if (!neighbours.has(from)) neighbours.set(from, new Set());
        neighbours.get(from)!.add(to);
      }
    }
    const degree = (id: string) => neighbours.get(id)?.size ?? 0;
    return {
      neighbours,
      degree,
      // Without notes, entities that only notes discuss would float unconnected; they
      // are drawn once notes are shown and stay in the node list below either way.
      // force-graph mutates the objects it receives, so it gets fresh copies.
      graphData: {
        nodes: visibleNodes
          .filter((node) => showNotes || degree(node.id) > 0)
          .map((node) => ({ ...node, label: nodeLabel(node, language) })),
        links: links.map((edge) => ({ ...edge })),
      },
    };
  }, [edges, language, showNotes, visibleNodes]);

  const hubs = useMemo(
    () =>
      new Set(
        [...graphData.nodes]
          .sort((a, b) => degree(b.id) - degree(a.id))
          .slice(0, ALWAYS_LABELLED)
          .map((node) => node.id),
      ),
    [degree, graphData],
  );

  const listedNodes = useMemo(
    () => visibleNodes.map((node) => ({ ...node, label: nodeLabel(node, language) })),
    [language, visibleNodes],
  );

  const radius = (node: RenderedNode) =>
    node.kind === "entity" ? Math.min(3 + Math.sqrt(degree(String(node.id))) * 1.5, 12) : 4;

  // Spread the layout: repulsion, longer relation edges, and no overlapping nodes.
  useEffect(() => {
    const graph = graphRef.current;
    if (!graph) return;
    fittedRef.current = false;
    graph.d3Force("charge")?.strength(-220);
    graph.d3Force("link")?.distance((link: RenderedLink) => (isRelation(link) ? 60 : 35));
    graph.d3Force("collide", forceCollide<RenderedNode>((node) => radius(node) + 3));
    graph.d3Force("x", forceX(0).strength(GRAVITY));
    graph.d3Force("y", forceY(0).strength(GRAVITY));
    graph.d3ReheatSimulation();
    // Fit the pre-computed layout right away; onEngineStop fits the settled one again.
    const timer = window.setTimeout(() => graph.zoomToFit(0, 20), 50);
    return () => window.clearTimeout(timer);
    // radius only depends on graphData, which this effect already follows.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [graphData]);

  const active = focusId ?? hoverId;
  const highlighted = useMemo(
    () => (active ? new Set([active, ...(neighbours.get(active) ?? [])]) : null),
    [active, neighbours],
  );

  const height = width < 600 ? 420 : 640;

  function toggleType(type: string) {
    setHiddenTypes((current) => {
      const next = new Set(current);
      if (next.has(type)) next.delete(type);
      else next.add(type);
      return next;
    });
  }

  function linkColor(link: RenderedLink) {
    if (highlighted && active) {
      const touches = endpointId(link.source) === active || endpointId(link.target) === active;
      return touches ? ACTIVE_EDGE : DIMMED_EDGE;
    }
    return EDGE_COLORS[link.type] ?? RELATION_COLOR;
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
            cooldownTicks={250}
            // Lay the graph out before the first frame instead of letting it unfold on screen.
            warmupTicks={150}
            graphData={graphData}
            height={height}
            linkColor={linkColor}
            linkDirectionalArrowLength={(link) => (isRelation(link) && !link.undirected ? 4 : 0)}
            linkDirectionalArrowRelPos={1}
            linkLabel={(link) => escapeHtml(link.type)}
            linkWidth={(link) => (link.type === "RELATED_TO" ? 1.5 : 1)}
            nodeCanvasObject={(node: RenderedNode, context, scale) => {
              const x = node.x ?? 0;
              const y = node.y ?? 0;
              const id = String(node.id);
              const size = radius(node);
              const isHighlighted = highlighted?.has(id) ?? false;
              context.globalAlpha = highlighted && !isHighlighted ? DIMMED_NODE_ALPHA : 1;
              context.fillStyle = node.kind === "entity" ? ENTITY_COLORS[node.entity_type] ?? NOTE_COLOR : NOTE_COLOR;
              context.beginPath();
              if (node.kind === "entity") context.arc(x, y, size, 0, 2 * Math.PI);
              else context.rect(x - size, y - size, size * 2, size * 2);
              context.fill();
              if (id === active) {
                context.lineWidth = 2 / scale;
                context.strokeStyle = "#202b28";
                context.stroke();
              }
              if (isHighlighted || hubs.has(id) || degree(id) * scale >= LABEL_THRESHOLD) {
                const fontSize = Math.max(11 / scale, 2.5);
                context.font = `${node.kind === "entity" ? 600 : 400} ${fontSize}px "Segoe UI", Arial, sans-serif`;
                context.textAlign = "center";
                context.textBaseline = "top";
                context.fillStyle = "#202b28";
                context.fillText(node.label, x, y + size + 2);
              }
              context.globalAlpha = 1;
            }}
            nodeLabel={(node) => escapeHtml(node.label)}
            nodePointerAreaPaint={(node: RenderedNode, color, context) => {
              context.fillStyle = color;
              context.beginPath();
              context.arc(node.x ?? 0, node.y ?? 0, Math.max(radius(node), 6), 0, 2 * Math.PI);
              context.fill();
            }}
            onBackgroundClick={() => setFocusId(null)}
            onEngineStop={() => {
              if (!fittedRef.current) {
                fittedRef.current = true;
                graphRef.current?.zoomToFit(400, 20);
              }
            }}
            onNodeClick={(node) => {
              // First click highlights the neighbourhood, a second click opens the node.
              if (focusId === String(node.id)) openNode(node);
              else setFocusId(String(node.id));
            }}
            onNodeHover={(node) => setHoverId(node ? String(node.id) : null)}
            ref={graphRef}
            width={width}
          />
        )}
      </div>
      <p className="graph-caption">{t("graphCaption")}</p>
      {/* The canvas is not keyboard accessible; the same nodes as a list. */}
      <details className="graph-node-list">
        <summary>{t("graphNodeList")} ({listedNodes.length})</summary>
        <ul>
          {listedNodes.map((node) => (
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
