// d3-force-3d ships without type declarations; only these forces are used.
declare module "d3-force-3d" {
  interface Force {
    (alpha: number): void;
    strength(strength: number): Force;
  }
  export function forceCollide<NodeType>(radius: (node: NodeType) => number): Force;
  export function forceX(x?: number): Force;
  export function forceY(y?: number): Force;
}
