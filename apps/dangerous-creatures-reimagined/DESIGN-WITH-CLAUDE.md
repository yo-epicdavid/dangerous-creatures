# Designing the Reimagined Edition with Claude

A practical guide + paste-ready prompts for using **Claude (Artifacts)** to design the visual and
interaction language of the Reimagined *Exploration* Edition — the explorable, discovery-driven
rebuild of **Dangerous Creatures**, **Oceans**, and **Dinosaurs**. Pairs with
[`REIMAGINED.md`](./REIMAGINED.md) (the master plan); this is the **design half of Phase 2 (§5)** —
the style bible + interaction design you do *before* generating a single final asset.

---

## What "designing with Claude" actually is

There's no separate "design mode" — the surface is **Artifacts** in [claude.ai](https://claude.ai).
You describe what you want; Claude writes a self-contained **HTML/SVG mockup** or an **interactive
React + Tailwind prototype** that renders live beside the chat, so you can *see and click* the idea
and refine it in plain language. Two surfaces, two jobs:

| Surface | Use it for |
|---|---|
| **claude.ai → Artifacts** | Diverging on art directions, mocking up key screens, and building a **clickable prototype of the discovery loop** you can feel. |
| **Claude Code** (this repo) | Turning the chosen direction into the real Astro app — the engine (§5), tokens in `site-kit`, wired to real `web/data`. |

> Rule of thumb: **explore and decide in Artifacts; build and ship in Claude Code.**

---

## The method (how to get *good* output, not just pretty output)

1. **Words before pixels.** Paste the brief (Prompt 0) first. Design follows the *feeling* and the
   *core loop* — not "make it look nice."
2. **Diverge before you converge.** First ask for **3–4 genuinely different** art directions, one
   screen each. Don't let Claude polish a single idea — compare, *then* pick.
3. **One screen at a time.** Once a direction wins, design its key screens one per message, with
   specific critical feedback each round.
4. **Prototype the loop, not just the look.** The real question is *"is it fun to discover?"* — only
   a clickable prototype answers that. Build it early and cheap, with placeholder art.
5. **Feed it real content.** Use an actual creature + real facts from `web/data` so the design
   survives true text lengths, not lorem ipsum.
6. **Extract a system.** When you love it, have Claude pull out **tokens + components + a11y notes**
   — which drop straight into `site-kit`'s `:root` token pattern.
7. **Critique like an art director.** "The mystery's too hidden — add an idle shimmer on hotspots."
   "The journal stamp should *thunk* in as a reward." Specific beats vague, every round.

**Artifacts prompting tips**
- Say it explicitly: *"interactive React + Tailwind artifact"* for prototypes; *"one self-contained
  HTML file"* for static mockups.
- Always restate the constraints (kids ~7–11, big touch targets, WCAG contrast,
  `prefers-reduced-motion`, no timers / dark patterns, runs offline as static files).
- Ask Claude to **annotate its choices** (why this palette, why this motion) so you can steer.
- To hold a look across screens, **paste the winning mockup's code back** and say "keep this exact
  language, now design screen X."
- You can **drop in reference / mood images** to anchor the art direction.

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

## The prompts — paste into claude.ai, in order

Each block is meant to be copied verbatim. Run Prompt 0 once, then 1 → 2 → 3 → 4.

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
DESCRIBE art, don't copy the originals).

Don't design yet — confirm you've got it and ask me anything that would sharpen the design.
```

### Prompt 1 · Diverge (4 art directions)

```text
Give me 4 DISTINCT art directions for this game, each as a single self-contained HTML mockup of the
SAME one screen: a creature-entry / reveal screen for a jaguar (image area, name, one earned "did
you know?" snippet, a "spotted!" journal stamp, and one onward thread to a related creature).

Make the four genuinely different in mood and visual language — for example: (1) Explorer's Field
Journal (tactile paper, sketches, stamps), (2) Naturalist's Atlas (painterly maps & plates), (3)
Cabinet of Curiosities (museum-after-dark, drawers & specimens), (4) Living Diorama (a lush
illustrated habitat you peer into). For each: a one-line concept name, a 2-sentence rationale, and a
note on how MYSTERY shows up in it. Kid audience; accessible; touch-friendly.
```

### Prompt 2 · Converge (key screens in the winning direction)

```text
I'm choosing direction #N: [name]. Keep that EXACT visual language. Now design these screens, one
self-contained HTML mockup per message (I'll ask for them one at a time):
  1. the world map / hub (choose a world to enter; shows journal progress)
  2. a habitat scene with 3–4 creatures HIDDEN in it (show the hidden state + a hover/idle hint)
  3. the reveal moment (a creature resolving out of hiding — describe the motion)
  4. the Field Journal (a collection filling up; locked entries shown as silhouettes)
  5. a creature entry (the Prompt-1 screen, refined)
Start with #1.
```

### Prompt 3 · Prototype the loop (the "is it fun?" test)

```text
Now build an interactive React + Tailwind artifact that prototypes the core loop in this visual
language: a single habitat scene with 3 hidden creatures. I can hunt for them (hover/tap to find a
hidden hotspot), tap to REVEAL (animate it in + show a one-line fact), and watch them get RECORDED
into a Field Journal counter ("2 of 3 discovered"). Include the reveal-all-spots accessibility
toggle and a prefers-reduced-motion path. Use placeholder colored shapes for the art. The point is
to FEEL the spot → reveal → record joy — make the reveal satisfying.
```

### Prompt 4 · Extract the design system

```text
Lock this in. Produce a design-system handoff I can implement in an Astro site that themes via CSS
:root tokens:
  - a token set (color — including the 3 per-world palettes — type scale, spacing, radii, shadow,
    motion durations/easings) as CSS custom properties
  - a component inventory (hotspot, reveal card, journal stamp, progress meter, map node, nav chrome)
    with their states: hidden → hinted → revealed
  - motion specs for the reveal/transition
  - accessibility notes per component
Output the tokens as a ready-to-paste :root { … } block.
```

---

## Then bring it back here

Paste the winning direction + the `:root` token block into **Claude Code** on the `reimagined`
branch and I'll: stand the design up in the real reimagined Astro app, build the scene/hotspot
**engine** (§5) against real `web/data`, theme it per world via `site-kit` tokens, and iterate it on
actual devices — then we playtest a one-habitat **vertical slice** (§8) before scaling.

> `REIMAGINED.md` says it best: *map the original, then build one habitat until it feels like magic.*
> This guide is how you find that magic in Artifacts before we build it for real.
