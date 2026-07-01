// scenegraph.ts — the engine's data model. A superset of the museum edition's `classic.screens`
// (percentage-based hotspot regions), enriched with reveal-type, hinting, and discovery state.
// See CREATURIA.md §5. The whole game is data: swap the graph, keep the engine.

/** Region as a percentage of the stage — responsive by construction (reused from museum hotspots). */
export interface Region {
  x: number;
  y: number;
  w: number;
  h: number;
}

/** The "surprise payload" — you never quite know which you'll get. */
export type RevealKind = 'creature' | 'fact' | 'clip' | 'place' | 'game';

export interface Hotspot {
  id: string;
  region: Region;
  reveal: RevealKind;
  /** For creature/fact/clip reveals: which creature this uncovers (→ Field Journal). */
  creatureId?: string;
  /** For `place` reveals: the scene id to travel to. */
  to?: string;
  /** Idle discoverability cue: a slow shimmer draws a curious eye without labelling the spot. */
  hint?: 'idle' | 'none';
}

/** A cross-link "lure" — the original's magic of being pulled toward a rival or cousin. */
export interface Onward {
  creatureId: string;
  label: string;
}

export interface Creature {
  id: string;
  name: string;
  tagline: string;
  /** The one earned "did you know?" line, rewritten clean-room in our own kid voice. */
  fact: string;
  /** Placeholder art: a CSS color + inline SVG silhouette (currentColor). Swapped for real art later. */
  color: string;
  silhouette: string;
  onward?: Onward;
}

export interface Scene {
  id: string;
  name: string;
  /** Placeholder backdrop: a CSS background value. Becomes a layered illustration later. */
  bg: string;
  ambient?: string;
  hotspots: Hotspot[];
  /** The no-dead-end guarantee: every scene names at least one onward thread. */
  onward: string[];
}

export interface SceneGraph {
  start: string;
  scenes: Record<string, Scene>;
  creatures: Record<string, Creature>;
}
