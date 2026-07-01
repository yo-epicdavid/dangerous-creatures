# Designing Creaturia with Claude Design

A practical guide + paste-ready prompts for using **Claude Design** (Anthropic Labs) to shape the
visual and interaction language of **Creaturia** — the explorable,
discovery-driven rebuild of **Dangerous Creatures**, **Oceans**, and **Dinosaurs**, shipping as a web
app *and* an installable native app. Pairs with [`CREATURIA.md`](./CREATURIA.md); this is the
**design half of Phase 2 (§5)** — the style bible + interaction design you do *before* generating
final assets.

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
| **Claude Code** (this repo) + `/design-sync` | Receive the handoff bundle, build it into the real app, keep the component library synced. |

> The loop: **design in Claude Design → "Handoff to Claude Code" → I build it → `/design-sync` keeps
> both sides in step.**

> [!IMPORTANT]
> **New look — not the museum look, and the art is PHOTO‑REALISTIC.** The imagery honors what made the
> original discs feel real — *actual photos & video of the animals*, montaged — done now at modern
> fidelity: photo‑real creatures (AI‑generated and/or real CC photos) composited into photo‑real
> habitat scenes, with real video on reveal. So the **creatures and scenes are photographic** (not flat
> illustration); the **UI chrome** (journal, cards, nav) is the *fresh, kid‑friendly, energetic* layer
> over that photography — not the museum edition's archival restraint. Point Claude Design at the repo
> only to learn the **theming architecture** (how `site-kit` themes per app via `:root` tokens) and
> have it design a *fresh photographic* look that themes the same way.

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
   here, and I'll build it into the Creaturia app, theme it per world, and **wrap it natively** for
   the app stores (next section).

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
- **Multisensory reveals.** Motion + sound + (on mobile/native) haptics make discovery feel physical.
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

## Platforms & form factors

This isn't only a website — it ships as an **installable native app** too, so it lands in the stores
where kids and parents actually look. The goal is *maximum reach for kids on the devices they have*:

| Store | Devices | How |
|---|---|---|
| **Apple App Store** | iPhone, iPad | one web build wrapped with **Capacitor** |
| **Google Play** | Android phones & tablets | the same build, Android shell |
| **Amazon Appstore** | **Fire tablets** (Fire OS = Android) | the Android build, no Google-Play-Services deps |
| **The web** | any browser | the same Astro app, also installable as a PWA |

**One offline-capable web codebase → web + iOS + Android + Fire.** That's *why* the plan stays Astro +
client island (§5): **Capacitor** reuses ~all of it and adds the native bits (haptics, local storage,
audio, share) behind a thin layer that falls back to web APIs in the browser — instead of rebuilding
the whole thing in React Native/Flutter. Fire tablets run Fire OS (an Android fork), so the Android
build goes to the **Amazon Appstore**; just avoid hard Google-Play-Services dependencies.

**What this means for the *design*:**
- **Many shapes.** Design responsive or **pannable** scenes — a fixed composition crops badly between
  a tall phone (~19.5:9) and a 4:3 iPad. Tablets are the sweet spot (often landscape); phones lean
  portrait (the vertical "expedition" flow).
- **Safe areas.** Keep tappable things and the journal clear of notches, rounded corners, and the
  home indicator.
- **Low-end hardware is the floor, not the ceiling.** Fire tablets are cheap and slow — budget the
  motion/media to stay smooth *there* and degrade gracefully. (This is exactly why the prototype must
  be tested on a real low-end tablet, not just an iPad.)
- **Fully offline.** Assets bundle with the app (or download on first run); no network needed to play.
- **Kids-store compliant by design.** No third-party ads, tracking, analytics, data collection, or
  sign-in walls; external links / purchases (if any) sit behind a parent gate. (Apple Kids Category,
  Google Play Families, Amazon kids policies.) The project's no-ads / non-commercial posture already
  fits — keep it that way in the UI.
- **Store assets are design work too** — app icon, splash screen, store screenshots. Claude Design
  makes those (Prompt 5).

---

## The prompts — paste into Claude Design, in order

Run Prompt 0 once when you start the project, then 1 → 2 → 3 → 4 → 5.

### Prompt 0 · The brief (paste once, first)

```text
I'm designing a game for kids (~7–11) called the Exploration Edition — a modern reimagining of the
1990s Microsoft Home CD-ROMs Dangerous Creatures, Oceans, and Dinosaurs. It ships BOTH as a web app
and as an installable NATIVE app (see PLATFORMS).

THE FEELING: exploration, discovery, mystery, wonder. Kids should WANT to click everything to see
what's hidden. The original's magic was that you never knew what a click would do — a video, a fact,
a creature, a new place — and the surprise was the reward.

THE CORE LOOP: spot → reveal → delight → record → wander on. You're an explorer with a Field
Journal. HOME IS A LIVING WORLD MAP — the MAIN way you explore: you pan and ZOOM across the globe into
habitat regions (rainforest, coral reef, savanna, polar ice, desert), TRAVEL IN to a habitat scene
that HIDES creatures, and can always go BACK to the map to roam somewhere else. In a habitat you poke
around, a shape resolves into an animal, you tap it and it reveals (a short clip + a whispered fact),
and it joins your journal. Some creatures lure you to a cousin or rival (cross-links). Mini-games
appear AS discoveries, not as a separate menu.

PROGRESSION: the Field Journal fills as you discover (creatures found, habitats explored, badges) —
gentle goals, never a chore. You unlock snippets of knowledge and new creatures by exploring.

GUIDES: optional narrated, hand-held journeys hosted by EXPLORERS & NATURALISTS, each leading kids
through the habitat they're famous for. Two kinds: (a) REAL public-domain historical figures used
directly (e.g. Charles Darwin, Alexander von Humboldt, Alfred Russel Wallace, Mary Anning), and (b)
ORIGINAL CHARACTERS INSPIRED BY modern greats where name/likeness rights apply — an ocean-explorer
archetype (à la Cousteau) and a great-ape naturalist (à la Goodall) — with a distinct name, look &
backstory, NOT a portrayal. A guide is a calm, optional alternative to free roaming — never forced, no
timers.

PLATFORMS: ships as a web app AND an installable native app — Apple App Store (iPhone, iPad), Google
Play (Android phones & tablets), and the Amazon Appstore (Fire tablets) — from ONE offline-capable
web build wrapped natively (Capacitor). So design for phones AND tablets across many aspect ratios
(tall phones ~19.5:9, iPad ~4:3, Fire/Android tablets ~16:10): habitat scenes must be responsive or
PANNABLE, never a fixed composition that crops. Respect device safe areas (notches, home
indicators). It must run SMOOTHLY ON LOW-END HARDWARE (cheap Fire tablets) — keep motion and media
light, degrade gracefully. Native feel: haptics on reveal, no browser chrome, fully offline.

CONSTRAINTS: touch-first; accessible (big touch targets, WCAG contrast, keyboard nav,
prefers-reduced-motion, plus a "reveal all interactive spots" toggle); KIDS-APP COMPLIANT — no
third-party ads, tracking, analytics, data collection, sign-in walls, or unguarded external links /
purchases (Apple Kids Category, Google Play Families, Amazon kids policies); no stress timers, no
dark patterns; all-new / openly-licensed art (DESCRIBE art, don't copy the originals). ART DIRECTION IS
PHOTO-REALISTIC: the creatures and habitat scenes are PHOTOGRAPHIC — photo-real animals (AI-generated
and/or real openly-licensed photos) composited into photo-real habitat scenes, with real video on
reveal — honoring the original discs' real-photo/video montages, at modern fidelity. NOT flat
illustration for the animals. The UI chrome (journal, cards, nav) is a fresh, kid-friendly, energetic
layer OVER that photography, not our archival museum restraint.

Don't design yet — confirm you've got it and ask me anything that would sharpen the design.
```

### Prompt 1 · Diverge (directions on the canvas)

```text
Before refining anything, show me 3–4 DISTINCT art directions for this game as variations of ONE
screen: a creature-entry / reveal screen for a jaguar (image area, name, one earned "did you know?"
snippet, a "spotted!" journal stamp, and one onward thread to a related creature).

Keep the imagery PHOTO-REALISTIC in every direction (a photo-real jaguar + a photographic habitat) —
what should differ is how the UI CHROME frames that photography. For example: (1) Modern Field Guide
(clean edge-to-edge photo, minimal HUD, a crisp "spotted!" stamp), (2) Explorer's Journal (the real
photo tucked into a tactile field-notebook page with tape & handwriting), (3) Naturalist's Specimen
Card (a photographic plate in an elegant museum-style mat & label), (4) Living Window (a full-bleed
photographic habitat you peer into, chrome dissolving to near-nothing). For each: a one-line concept
name, a 2-sentence rationale, and a note on how MYSTERY shows up in it. Kid audience; accessible;
touch-first; must scale from a phone to a tablet.
```

### Prompt 2 · Converge (key screens in the winning direction)

```text
I'm choosing direction #N: [name]. Keep that EXACT visual language and design system. Design these
screens on the canvas, one at a time (I'll refine each with comments before we move on), and show
each at BOTH a phone (portrait) and a tablet (landscape) size:
  1. THE WORLD MAP / HUB — the MAIN exploration surface: a living, ZOOMABLE world map with distinct
     habitat regions (rainforest, coral reef, savanna, polar ice, desert) you pan/zoom and TRAVEL
     INTO; show journal progress, a couple of "locked / coming soon" habitats as intriguing
     silhouettes, and the entry points for the explorer GUIDES (photo-real map treatment)
  2. a habitat scene with 3–4 creatures HIDDEN in it (show the hidden state + a hover/idle hint), plus
     a clear "back to the map" affordance
  3. the reveal moment (a creature resolving out of hiding — describe the motion)
  4. the Field Journal (a collection filling up; locked entries shown as silhouettes)
  5. a creature entry (the Prompt-1 screen, refined)
  6. an EXPLORER GUIDE intro — either a real public-domain figure (e.g. Charles Darwin, Alexander von
     Humboldt) OR an original character inspired by a modern great (an ocean-explorer à la Cousteau, a
     great-ape naturalist à la Goodall — distinct name/look, not a portrayal) inviting the kid on a
     narrated journey through their habitat; show how their portrait/persona, name, and a "start the
     expedition" call-to-action are framed
Start with #1.
```

### Prompt 3 · Prototype the loop (the "is it fun?" test)

```text
Build an interactive prototype of the core loop in this visual language: a single habitat scene with
3 hidden creatures. I can hunt for them (hover/tap to find a hidden hotspot), tap to REVEAL (animate
it in + show a one-line fact), and watch them get RECORDED into a Field Journal counter ("2 of 3
discovered"). Include the "reveal all interactive spots" accessibility toggle and a
prefers-reduced-motion path. It must feel right with TOUCH on a tablet and a phone. Use placeholder
shapes for the art and keep the animation lightweight (it has to be smooth on a cheap Fire tablet).
The point is to FEEL the spot → reveal → record joy — make the reveal satisfying.
```

### Prompt 4 · Ready it for build + hand off

```text
This is the direction. Get it build-ready:
  (a) express everything with reusable design-system components and tokens — color (including the 3
      per-world palettes: Dangerous Creatures, Oceans, Dinosaurs), type scale, spacing, radii,
      shadow, motion durations/easings;
  (b) review the whole thing for accessibility, touch ergonomics, safe-area handling, and how it
      reflows between a phone and a tablet — and fix issues;
  (c) then HAND OFF TO CLAUDE CODE so I can build it into the app and wrap it natively.
In the handoff notes, summarize the token set and a component inventory (hotspot, reveal card,
journal stamp, progress meter, world-map + habitat-region node, zoom/pan + "back to map" controls,
explorer-guide card, nav chrome) with their states: hidden → hinted → revealed.
```

### Prompt 5 · App identity & store assets

```text
We're also shipping this as a native app on the App Store, Google Play, and the Amazon Appstore.
Design the app/store identity in this same visual language:
  - an APP ICON that reads at small sizes and works as an adaptive icon (one iconic motif — e.g. the
    explorer's journal, a world-map compass/pin, or a hidden-creature silhouette);
  - a SPLASH / launch screen (calm, on-brand, works on phone + tablet, respects safe areas);
  - 3–5 STORE SCREENSHOTS that sell the discovery feeling (a hero line + one key screen each), sized
    for iPhone, iPad, and an Android / Fire tablet.
Keep it kid-friendly and parent-trustworthy (no ads / in-app-purchase vibes).
```

---

## Then bring it back here

Use **Handoff to Claude Code** in Claude Design, then on the `reimagined` branch I'll: take the
bundle, stand the design up in the real Creaturia Astro app, build the scene/hotspot **engine** (§5)
against real `web/data`, theme it per world, and **wrap it with Capacitor** so the *same* build ships
to the App Store, Google Play, and the Amazon Appstore (Fire) — plus the web/PWA. I'll run
**`/design-sync`** to keep the component library and your Claude Design project in step. Then we
playtest a one-habitat **vertical slice** (§8) on real devices — *including a cheap Fire tablet* —
before scaling.

> `CREATURIA.md` says it best: *map the original, then build one habitat until it feels like magic.*
> Claude Design is where you find that magic; the handoff — and the native wrap — is how it reaches
> every kid, on whatever device they've got.
