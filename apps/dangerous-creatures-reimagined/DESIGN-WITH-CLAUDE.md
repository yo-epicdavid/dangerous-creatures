# Designing the Reimagined Edition with Claude Design

A practical guide + paste-ready prompts for using **Claude Design** (Anthropic Labs) to shape the
visual and interaction language of the Reimagined *Exploration* Edition — the explorable,
discovery-driven rebuild of **Dangerous Creatures**, **Oceans**, and **Dinosaurs**. Pairs with
[`REIMAGINED.md`](./REIMAGINED.md); this is the **design half of Phase 2 (§5)** — the style bible +
interaction design you do *before* generating final assets.

---

## What Claude Design is

[Claude Design](https://claude.ai/design) (Anthropic Labs · launched April 2026 · Claude Opus 4.7
vision) is a **chat + canvas** tool: describe what you want on the left, Claude builds it live on the
right, and you refine it conversationally. Two things make it a near-perfect fit for *this* project:

- **It learns a design system from your codebase.** Point it at this repo and it reads your colors,
  type, and components, builds every screen *with* them, and checks its own output against them.
- **It hands off straight to Claude Code.** When a design is ready, Claude Design packages a
  **handoff bundle** that Claude Code continues from — *not* a screenshot — closing the loop from
  exploration → prototype → production. The **`/design-sync`** skill then keeps the local component
  library and the Claude Design project in step, one component at a time.

**Where:** [claude.ai/design](https://claude.ai/design) on the web, or the **Claude Design** entry in
the **Claude Desktop** sidebar. **Plans:** Pro / Max / Team / Enterprise (research preview).

| Surface | Role |
|---|---|
| **Claude Design** (web or Desktop) | Diverge on directions, design the key screens on the canvas, build a clickable prototype of the discovery loop. |
| **Claude Code** (this repo) + `/design-sync` | Receive the handoff bundle, build it into the real Astro app, keep the component library synced. |

> The loop: **design in Claude Design → "Handoff to Claude Code" → I build it → `/design-sync` keeps
> both sides in step.**

> [!IMPORTANT]
> **New look — not the museum look.** Claude Design builds a system *from your codebase*, but the
> codebase today is the *museum* edition (`site-kit` tokens — restrained, archival). The reimagined
> edition wants its own bolder, playful language. So either **start a brand-new design system** for
> this edition, or point it at the repo only to learn the **theming architecture** (how `site-kit`
> themes per app via `:root` tokens) and ask it to design a *fresh* look that themes the same way —
> don't let it inherit the archive's restraint.

---

## The method

1. **Set the context.** Start a project at claude.ai/design — either fresh (new design system) or
   pointed at this repo for the per-world token architecture. Optionally use the **web-capture** tool
   to grab the live museum edition as a continuity reference.
2. **Words before pixels.** Paste the brief (Prompt 0). Design follows the *feeling* and the *core
   loop*, not "make it nice."
3. **Diverge first.** Ask for **2–4 distinct directions** of one key screen on the canvas (it's good
   at variations to compare). Don't let it polish a single idea — pick one, then go deep.
4. **Refine with the right tool for each change** (this is the canvas superpower):
   - **Chat** for structural / broad changes ("make it darker, more mysterious").
   - **Inline comments** for targeted tweaks (click an element → "bigger touch target here").
   - **Adjustment knobs / direct canvas edits** for aesthetics (spacing, color, layout).
   - Be **specific**: *"tighten spacing to 8px"* beats *"this looks off."*
5. **Prototype the loop, not just the look.** Have it build an interactive prototype of *spot →
   reveal → record* — the real **"is it fun?"** test — before any final art exists.
6. **Feed it real content.** Use an actual creature + real facts from `web/data` so the design
   survives true text lengths, not lorem.
7. **Hand off to Claude Code.** When you love it, use **Handoff to Claude Code**, bring the bundle
   here, and I'll build it into the reimagined Astro app, themed per world, iterating on device.

**Best practices (per the docs):** import the *complete* system; start simple, then layer
complexity; request **2–3 variations** to compare; ask Claude Design to **review accessibility**.
**Beta quirks:** inline comments can occasionally vanish (use the comments view), very large repos
can lag, and simultaneous multi-person editing is unreliable.

---

## Design principles for *this* audience (sharpening the §2 instinct)

Modern "good UX" — everything obvious, everything labeled — accidentally **kills mystery**. Design
the tension on purpose:

- **Reward every click.** No empty interactions: always a creature, a fact, a sound, or a new place.
- **Mystery, never frustration.** Locked = an *intriguing silhouette* with a clear way in — never a
  paywall or a dead end.
- **Gentle, visible progress.** The Field Journal fills like an adventure log, not a chore tracker;
  no shame for blanks.
- **Low text, high image, bite-size knowledge.** A snippet you *earn* beats a paragraph you're handed.
- **Multisensory reveals.** Motion + sound + (on mobile) haptics make discovery feel physical.
- **Calm by default.** No stress timers; challenge is opt-in.
- **Accessibility is a toggle, not a tax.** Reveal-all-spots, keyboard nav, reduced-motion — designed
  to *coexist* with the mystery, per §5.

---

## One language, three worlds

Design the system **once**, then theme it per world — exactly how the museum edition themes
`site-kit` via per-app `:root` tokens:

- 🦁 **Dangerous Creatures** — savanna dusk / jungle / reef-edge; warm, golden, a little dangerous.
- 🌊 **Oceans** — sunlit shallows → crushing abyss; cool, deep, bioluminescent.
- 🦕 **Dinosaurs** — Mesozoic dawn; earthy, ancient, amber.

Same components, same discovery loop, same journal — different palette, creatures, and ambient mood.
**Decide the shared skeleton first; theme last.**

---

## The prompts — paste into Claude Design, in order

Run Prompt 0 once when you start the project, then 1 → 2 → 3 → 4.

### Prompt 0 · The brief (paste once, first)

```text
I'm designing a web game for kids (~7–11) called the Exploration Edition — a modern reimagining of
the 1990s Microsoft Home CD-ROMs Dangerous Creatures, Oceans, and Dinosaurs.

THE FEELING: exploration, discovery, mystery, wonder. Kids should WANT to click everything to see
what's hidden. The original's magic was that you never knew what a click would do — a video, a fact,
a creature, a new place — and the surprise was the reward.

THE CORE LOOP: spot → reveal → delight → record → wander on. You're an explorer with a Field
Journal. From a painted world map you enter living habitat scenes that HIDE creatures; you poke
around, a shape resolves into an animal, you tap it and it reveals (a short clip + a whispered
fact), and it joins your journal. Some creatures lure you to a cousin or rival (cross-links).
Mini-games appear AS discoveries, not as a separate menu.

PROGRESSION: the Field Journal fills as you discover (creatures found, habitats explored, badges) —
gentle goals, never a chore. You unlock snippets of knowledge and new creatures by exploring.

CONSTRAINTS: mobile / tablet / desktop, touch-first; static site (Astro), works offline; accessible
(big touch targets, WCAG contrast, keyboard nav, prefers-reduced-motion, plus a "reveal all
interactive spots" toggle); no stress timers, no dark patterns; all-new / openly-licensed art (so
DESCRIBE art, don't copy the originals). This is a NEW visual language — bolder and more playful
than our existing archival site — so don't inherit a restrained museum look.

Don't design yet — confirm you've got it and ask me anything that would sharpen the design.
```

### Prompt 1 · Diverge (directions on the canvas)

```text
Before refining anything, show me 3–4 DISTINCT art directions for this game as variations of ONE
screen: a creature-entry / reveal screen for a jaguar (image area, name, one earned "did you know?"
snippet, a "spotted!" journal stamp, and one onward thread to a related creature).

Make them genuinely different in mood and visual language — for example: (1) Explorer's Field Journal
(tactile paper, sketches, stamps), (2) Naturalist's Atlas (painterly maps & plates), (3) Cabinet of
Curiosities (museum-after-dark, drawers & specimens), (4) Living Diorama (a lush illustrated habitat
you peer into). For each: a one-line concept name, a 2-sentence rationale, and a note on how MYSTERY
shows up in it. Kid audience; accessible; touch-first.
```

### Prompt 2 · Converge (key screens in the winning direction)

```text
I'm choosing direction #N: [name]. Keep that EXACT visual language and design system. Design these
screens on the canvas, one at a time (I'll refine each with comments before we move on):
  1. the world map / hub (choose a world to enter; shows journal progress)
  2. a habitat scene with 3–4 creatures HIDDEN in it (show the hidden state + a hover/idle hint)
  3. the reveal moment (a creature resolving out of hiding — describe the motion)
  4. the Field Journal (a collection filling up; locked entries shown as silhouettes)
  5. a creature entry (the Prompt-1 screen, refined)
Start with #1.
```

### Prompt 3 · Prototype the loop (the "is it fun?" test)

```text
Build an interactive prototype of the core loop in this visual language: a single habitat scene with
3 hidden creatures. I can hunt for them (hover/tap to find a hidden hotspot), tap to REVEAL (animate
it in + show a one-line fact), and watch them get RECORDED into a Field Journal counter ("2 of 3
discovered"). Include the "reveal all interactive spots" accessibility toggle and a
prefers-reduced-motion path. Use placeholder shapes for the art. The point is to FEEL the
spot → reveal → record joy — make the reveal satisfying.
```

### Prompt 4 · Ready it for build + hand off

```text
This is the direction. Get it build-ready:
  (a) express everything with reusable design-system components and tokens — color (including the 3
      per-world palettes: Dangerous Creatures, Oceans, Dinosaurs), type scale, spacing, radii,
      shadow, motion durations/easings;
  (b) review the whole thing for accessibility and touch ergonomics and fix issues;
  (c) then HAND OFF TO CLAUDE CODE so I can build it into the Astro app.
In the handoff notes, summarize the token set and a component inventory (hotspot, reveal card,
journal stamp, progress meter, map node, nav chrome) with their states: hidden → hinted → revealed.
```

---

## Then bring it back here

Use **Handoff to Claude Code** in Claude Design, then on the `reimagined` branch I'll: take the
bundle, stand the design up in the real reimagined Astro app, build the scene/hotspot **engine**
(§5) against real `web/data`, theme it per world, and run **`/design-sync`** to keep the component
library and your Claude Design project in step. Then we playtest a one-habitat **vertical slice**
(§8) before scaling.

> `REIMAGINED.md` says it best: *map the original, then build one habitat until it feels like magic.*
> Claude Design is where you find that magic; the handoff is how it becomes real.
