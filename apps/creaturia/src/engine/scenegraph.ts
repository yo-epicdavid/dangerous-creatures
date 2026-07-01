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
export type RevealKind = 'creature' | 'fact' | 'clip' | 'place' | 'game' | 'guide';

export interface Hotspot {
  id: string;
  region: Region;
  reveal: RevealKind;
  /** For creature/fact/clip reveals: which creature this uncovers (→ Field Journal). */
  creatureId?: string;
  /** For `place` reveals: the scene id to travel to. Absent (or `locked`) → a "coming soon" tease. */
  to?: string;
  /** Map markers (`place`/`guide`) are VISIBLE — a map is for reading, not hunting: name + art. */
  label?: string;
  /** Placeholder marker art: inline SVG (currentColor), same contract as Creature.silhouette. */
  art?: string;
  color?: string;
  /** A locked habitat: an intriguing, non-enterable silhouette that teases the bigger world. */
  locked?: boolean;
  /** For `guide` reveals: which explorer this marker introduces. */
  guideId?: string;
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

/** An explorer guide (CREATURIA.md §3 roster) — a real public-domain naturalist used directly,
 * or an original inspired-by character where name/likeness rights apply. */
export interface Guide {
  id: string;
  name: string;
  /** Real PD figures carry their real dates — part of teaching their real work. */
  years: string;
  tagline: string;
  /** The one-line invitation on the intro card, in the guide's own voice. */
  invite: string;
  /** Placeholder art: a CSS color + inline SVG portrait silhouette. Swapped for real art later. */
  color: string;
  portrait: string;
  /** The habitat scene their expedition walks through. */
  habitat: string;
}

export interface Scene {
  id: string;
  name: string;
  /** Placeholder backdrop: a CSS background value. Becomes a layered illustration later. */
  bg: string;
  /** Optional inline-SVG art layer over the bg, behind the hotspots (e.g. the map's continents). */
  backdrop?: string;
  ambient?: string;
  hotspots: Hotspot[];
  /** The no-dead-end guarantee: every scene names at least one onward thread. */
  onward: string[];
}

export interface SceneGraph {
  start: string;
  scenes: Record<string, Scene>;
  creatures: Record<string, Creature>;
  guides?: Record<string, Guide>;
}
