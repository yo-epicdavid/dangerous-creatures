# Kickoff — starting a fresh session on the Reimagined edition

This edition is big enough to deserve a **fresh, focused session** with full context. Everything a
new session needs lives in this folder — point it here and let it work out the rest.

## Read these first (the source of truth)

1. **[`REIMAGINED.md`](./REIMAGINED.md)** — the master plan: vision, the discovery loop, the phased
   roadmap, risks, and **§5½ Platforms & packaging** (web + native via Capacitor).
2. **[`DESIGN-WITH-CLAUDE.md`](./DESIGN-WITH-CLAUDE.md)** — how to design the look & feel in **Claude
   Design**, with paste-ready prompts (0 → 5) and the handoff-to-Claude-Code loop.
3. **[`src/lib/platform.ts`](./src/lib/platform.ts)** — the web⇄native seam (Capacitor with web
   fallbacks); the engine should reach platform features only through this.

Also worth a skim: the **museum edition** (`apps/dangerous-creatures`, `packages/site-kit`,
`packages/pipeline`) for the data shape (`web/data/*.json`), the per-app `:root` token theming, and
the extraction tooling we're reusing.

## Two tracks, two kinds of session

- **Design track → Claude Design.** Open [claude.ai/design](https://claude.ai/design) (or the Claude
  Desktop sidebar) and run the prompts in `DESIGN-WITH-CLAUDE.md`. Output: the visual language + a
  handoff bundle for Claude Code.
- **Build/plan track → a fresh Claude Code session.** Paste the prompt below. It tells the session to
  read the docs and produce *everything the vertical slice needs* — and to surface the open decisions
  before it writes code.

---

## Paste this into a fresh Claude Code session (on the `reimagined` branch)

```text
You're picking up the "Reimagined (Exploration) Edition" — a kid-focused (~7–11), discovery-driven
rebuild of Microsoft's Dangerous Creatures / Oceans / Dinosaurs. It evokes exploration, mystery, and
wonder: from a painted world map you enter living habitat scenes that HIDE creatures; you poke
around, a shape resolves, you tap to reveal (clip + fact), and it joins your Field Journal. Core
loop: spot → reveal → delight → record → wander on. It ships as ONE offline-capable web app that
ALSO goes native to the Apple App Store, Google Play, and the Amazon Appstore (Fire tablets) via
Capacitor — for maximum reach for kids on whatever device they have.

FIRST, read these in apps/dangerous-creatures-reimagined/: REIMAGINED.md (the plan, incl. §5½
Platforms & packaging), DESIGN-WITH-CLAUDE.md (the design process), and src/lib/platform.ts (the
web⇄native seam). Skim the museum edition (apps/dangerous-creatures, packages/site-kit,
packages/pipeline) for the data shape and the token-theming + extraction patterns we reuse.

THEN produce EVERYTHING needed to build one magical vertical slice — the rainforest, ~5 creatures —
end to end, on phone + tablet + a low-end Fire tablet:
  1. Scaffold plan: the Astro + client-island engine, the Capacitor wrap (iOS/Android/Fire), and how
     src/lib/platform.ts gets wired — exact packages, config, and project structure.
  2. Engine design: the scene-graph data model (extend the museum's classic hotspots), the
     reveal/transition system (View Transitions), the Field Journal state (persisted via
     platform.storage), and the hidden → hinted → revealed progressive-disclosure logic.
  3. Asset & license pipeline (§7): how art/video/audio get generated or sourced (CC), the
     bundled-vs-fetched-on-demand tiers (offline + app-size limits), and the license ledger.
  4. Content plan (§6): clean-room rewrite of the slice's creatures from web/data facts.
  5. A concrete, ordered task list to build and playtest the slice — with the OPEN DECISIONS you need
     from me called out FIRST.

Be exhaustive about what's needed and honest about unknowns, risks, and costs. Ask me the open
questions BEFORE writing code. Respect the constraints: touch-first, accessible, kids-store compliant
(no ads/tracking/data), responsive/pannable scenes with safe-area handling, and smooth on cheap Fire
hardware. Don't boil the ocean — everything aims at one playable, magical rainforest slice first.
```

> Tip: in that session, lean on **multi-agent workflows** (the same approach that liberated 66
> animals) for the fan-out parts — asset generation, content rewrites, QA gates — once the slice's
> template exists. Keep the first slice hand-built and playtested before scaling.
