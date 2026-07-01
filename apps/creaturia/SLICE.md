# Vertical slice — build status

The first **playable** rainforest slice: an Astro shell + a **Solid `client:only`** discovery engine.
Built hand-first (not fanned out) so we can playtest the *feel* before scaling — per CREATURIA.md §8.

## Decisions locked (this session)

- **Start point:** build the engine now, with placeholder art, in parallel with the Claude Design track.
- **Roster (5):** Jaguar · Poison-Arrow Frog · Harpy Eagle · Army Ants · Boa — ids match the museum
  data (`jagu`/`arow`/`harp`/`aant`/`boac`) so full facts/media can back-fill later.
- **Orientation:** **landscape-locked** (tablet sweet spot); small phones get a "turn sideways" nudge.
- **Slice art:** **abstract placeholders** only (a color + a rough inline-SVG silhouette per creature) —
  enough to prove the loop is fun. The **target aesthetic is photo-realistic** (photo-real animals +
  photographic habitat scenes + real video on reveal, honoring the original discs' montages — see
  CREATURIA.md §5/§7). Placeholders swap for that in Phase 4 with **no engine change**: the silhouette
  → a photo cut-out, the CSS-gradient scene → a photographic plate, the reveal card → a photo/clip.

## What works (verified in a headless browser)

The full loop — **spot → reveal → delight → record → wander on**:

- A 16:9 scene hides five creatures; each is an invisible `%`-positioned hotspot that shows only a
  subtle **idle-hint** shimmer (staggered) — mystery by default.
- Tap → the creature silhouette settles into the scene, a **reveal card** pops (kicker varies by
  reveal kind: *Did you know?* / *Caught in motion*), a **"Spotted!"** stamp lands, and it's recorded.
- The **Field Journal** rail fills (locked = grey silhouette, found = lit in the creature's color),
  persisted via `platform.storage` (localStorage on web, Capacitor Preferences native).
- **Cross-link lures:** the card's onward button pulses the cousin/rival's hiding spot (jaguar→boa,
  harpy→frog, …) — the "fall down a rabbit hole" pull.
- **Accessibility ↔ mystery:** a "Reveal spots" toggle outlines every undiscovered region; hotspots
  are real `<button>`s (tab + Enter); Esc closes the card; full `prefers-reduced-motion` path.
- **Footprint:** engine bundles to ~7.5 KB + Solid store ~19.5 KB + ~6 KB CSS (gzip ≈13 KB) — the
  low-end-Fire-tablet budget Solid was chosen for.

## Run it

```bash
pnpm install                 # from repo root (adds astro + @astrojs/solid-js + solid-js)
pnpm --filter creaturia dev      # or: cd here && pnpm dev
pnpm --filter creaturia build    # static build → dist/
```

## Map

```
src/
  pages/index.astro      # shell → mounts <World client:only="solid" graph={rainforest}/>
  layouts/Layout.astro   # head, viewport-fit=cover, safe-area vars, imports web/styles.css
  engine/                # the Solid engine
    World.tsx            #   root island: state, activation, lures, journal wiring
    SceneStage.tsx       #   landscape stage + hotspot layout
    Hotspot.tsx          #   hidden → hinted → revealed (a real <button>)
    RevealCard.tsx       #   the reveal payload (name, fact, stamp, onward lure)
    Journal.tsx          #   the progress rail
    state.ts             #   Field Journal store, persisted via platform.storage
    transitions.ts       #   View Transitions API w/ reduced-motion + no-support fallbacks
    scenegraph.ts        #   the data model (superset of museum classic.screens hotspots)
    engine.css           #   component styles (tokens only → re-themes per world)
  data/rainforest.ts     # the slice scene-graph + clean-room creature content
  lib/platform.ts        # the web⇄native (Capacitor) seam — the ONLY native touchpoint
web/styles.css           # :root THEME tokens (bold rainforest look, not the museum restraint)
capacitor.config.ts      # native wrap config (native `cap add` is a follow-up step)
```

## Not done yet (next steps, ordered)

1. **Playtest** the loop on a phone, an iPad, and a **real low-end Fire tablet** — the only true
   "is it fun?" test. Tune hint timing, reveal punch, touch targets.
2. **Content polish:** human editing pass on the five clean-room facts; add narration scripts.
3. **Assets (Phase 4):** swap placeholders for **photo-real** habitat plates + creature cut-outs
   (style bible → real species reference photos → character-sheet-then-edit → species-accuracy QA
   loop); source real CC video clips (Commons / iNaturalist / Pexels — mind per-item licenses); add CC
   ambient/SFX + TTS narration. Everything into a **license ledger** (`web/data/assets.json`).
4. **More reveal kinds:** wire real `clip` playback (`platform.playSound`/`<video>`), a `game` payload
   ("whose eyes?"), and `place` hotspots that travel between scenes (View-Transition morphs).
5. **Native wrap:** install Capacitor + plugins, `cap add ios android`, fill the `TODO(native)` blocks
   in `platform.ts`, lock orientation natively, sideload to Fire. Add PWA/service-worker for offline.
6. **Design handoff:** when the Claude Design bundle lands, reconcile tokens/components with `web/styles.css`
   + `engine.css` (they already follow the per-world token architecture) and run `/design-sync`.
7. **Scale (Phase 6):** the slice is the template — fan out content/assets/scene-assembly with the
   multi-agent workflow, adversarial QA gates.
```
