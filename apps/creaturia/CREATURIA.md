# Creaturia — a new Exploration game

> **Creaturia** is a new game *inspired by* and *continuing* Microsoft Home's Exploration Series
> (Dangerous Creatures · Oceans · Dinosaurs) — **not a remake** of it. It recreates their sense of
> exploration, surprise, and wonder with all‑new, openly‑licensed assets, so it can belong to every
> kid on any device.

---

## 0. The north star

The current site (now on `main`) is a beautiful **museum of the original** — faithful,
preserved, accessible. But the user is right: it's *fully rendered*. You see everything at once.
The original's magic was the opposite — **you didn't know what would happen next.** You hunted for
hidden hotspots, clicked a label not knowing if it led to a video, a fact, or another creature,
and the surprise *was* the reward.

**This project recreates the experience, not the artifact:**

- **Exploration & discovery** over disclosure. Every click is a small surprise.
- **All‑new assets** — AI‑generated art + openly‑licensed footage + fresh prose — so the result
  is legally clean and truly public (no takedown risk, no "swap later").
- **Mobile · tablet · desktop**, designed for touch and for wonder.
- The museum edition stays live as the *preservation*; **Creaturia** is a *new thing
  built beside it.*

> **Design mantra:** *Reward curiosity. Hide a little. Surprise often. Never a dead end.*

---

## 1. What we already have (huge head start)

We are **not starting from zero.** The museum build already produced the skeleton this game
hangs on:

| Asset we already have | How it accelerates the rebuild |
|---|---|
| **66 creatures of structured data** (`web/data/*.json`) — intros, facts, sub‑topics, captions | The *content & facts*. Facts aren't copyrightable; we rewrite the *prose* in our own voice (Phase 3) and reuse the structure. |
| **The Classic hotspot maps** (`classic.screens[].hotspots`) + **cross‑links** (baboon→leopard…) | A large chunk of the **navigation graph** is already digitized — what links to what. |
| **The 4 nav modes** (Atlas/Habitats/Weapons/Guides) + **12 guided‑tour scripts** | The original's information architecture, already modeled as data. |
| **The taxonomies** (`browse.json`: region/habitat/weapon) + **quiz/games data** | Ready‑made structure for explorable worlds and woven‑in play. |
| **The Astro app + build pipeline + tooling** | The engineering foundation; we extend it, not replace it. |
| **The credits posture & habits** | We carry the "credit everyone, non‑commercial, removal‑on‑request" discipline to the new (mostly self‑owned) assets. |

> We keep the **structure and the facts**; we replace the **assets and the prose**; we **add**
> the interaction design the museum edition lacks.

---

## 2. The design problem: where the magic actually lives

The wonder wasn't in the pixels — it was in four things. We must **design for each on purpose**,
because modern "good UX" (everything obvious, everything accessible) accidentally *kills* mystery.

1. **Hidden affordances** — you had to *find* the hotspots. → We bring back *subtle*
   discoverability: scenes that invite poking, gentle hover/idle cues, a "look closer" mode — but
   with an accessible fallback (a toggle that reveals all interactive spots, keyboard nav). Mystery
   by default, clarity on demand.
2. **Surprise payloads** — a click could yield a video, a sound, a creature, a fact. You didn't
   know which. → Varied, unpredictable reveals. Sometimes a creature pounces out; sometimes a
   "did you know?"; sometimes a short film; sometimes a new place.
3. **Non‑linear wandering** — cross‑links let you fall down rabbit holes. → Keep the
   creature‑to‑creature links; add "trails" of association so you can wander for an hour.
4. **A sense of place & reward** — it felt like *somewhere*, and finding things felt earned.
   → Explorable illustrated *worlds* (not lists) + a **Field Journal** that fills as you discover,
   turning exploration into quiet progression.

> The hardest part of this whole project is **not** generating images. It's **making it feel
> magical** — and that is validated only by **playtesting with real kids**, not by tech.

---

## 3. The experience concept (a starting point to refine)

A concrete proposal for the shape of the game. Treat this as v0 of the design — to be sharpened
in Phase 2 and against the walkthrough video.

**You are an explorer with a field journal.** Your home base is a **living world map** — the *main*
way you explore (issue #27): pan and **zoom** across the globe into **habitat regions** — a steaming
rainforest, a coral reef, the savanna at dusk, polar ice, a desert at noon. Tap a habitat and you
*travel in* to that living scene; you can always step **back to the map** and wander somewhere else.
Each habitat is a rich **photographic** world *hiding creatures.* You poke around; a shape resolves
into a jaguar; tap it and it *reveals* — a short film plays, a narrator whispers a fact, the
creature joins your journal. Some creatures point you to a rival or cousin (the cross‑links),
luring you deeper. **Guides** are recast as *explorers* (issue #27), of two kinds: **real
public‑domain naturalists** used directly — **Alexander von Humboldt** (Amazon), **Charles Darwin**
(islands/adaptation), **Alfred Russel Wallace**, **Mary Anning** (Dinosaurs) — and **original
characters inspired by** modern greats where name/likeness rights apply: *Captain Mira Delmar*, an
ocean‑explorer (à la Cousteau/Earle), and *Dr. Amara Okafor*, a great‑ape naturalist (à la Goodall,
who died Oct 2025). Real *living* figures we feature only *with permission* (e.g. Paul Rosolie → the
Amazon). Each hosts a narrated, hand‑held journey through their habitat — a thread that ties the three
editions together. *(Rights rule: use PD figures directly and teach their real work; for
living/recently‑deceased or brand‑managed figures, build an original inspired‑by character — distinct
name, look & backstory — not a portrayal.)*
**Mini‑games** are woven in as discoveries, not a separate menu
("whose eyes are these?" appears when you find a pair of eyes in the dark).

- **Discovery loop:** *spot → reveal → delight → record → wander on.*
- **Progress:** the Field Journal (creatures found, habitats explored, "danger badges") gives
  gentle goals without turning it into a chore.
- **No dead ends:** every screen offers at least one onward thread.

**Per‑device interaction:**

| Device | Primary interaction | Notes |
|---|---|---|
| **Mobile** | Tap to discover; vertical "expedition" flow; big touch targets | Mystery via subtle motion/parallax; haptics on reveal |
| **Tablet** | Tap + drag to roam larger scenes; the "sweet spot" device | Pannable scenes, two‑hand play |
| **Desktop** | Hover‑to‑hint + click; widest scenes, richest parallax | Keyboard‑navigable for accessibility |

### Guides — the explorer roster (issue #27)

Two kinds of guide, picked by a simple **rights rule**: use real **public‑domain** figures directly
(and teach their real work); for **living / recently‑deceased / brand‑managed** figures, build an
**original character inspired by** the archetype — distinct name, look & backstory, never a portrayal.
*(Inspired‑by names below are placeholders — rename freely. The rainforest slice ships with Humboldt.)*

**Real · public domain · use now**

| Guide | Lived | Domain → habitat | Edition |
|---|---|---|---|
| **Alexander von Humboldt** | 1769–1859 | Amazon rainforest + the Andes | DC — **rainforest slice guide** |
| **Charles Darwin** | 1809–1882 | Galápagos, islands, adaptation | DC |
| **Alfred Russel Wallace** | 1823–1913 | rainforests; the Wallace Line (why animals live where they do) | DC |
| **Mary Anning** | 1799–1847 | fossils, ancient seas | Dinosaurs |
| **Roy Chapman Andrews** | 1884–1960 | Gobi desert, dinosaur eggs | DC desert · Dinosaurs |
| **John James Audubon** | 1785–1851 | birds, forests & wetlands | DC |
| **Amundsen / Shackleton** | 1872–1928 / 1874–1922 | polar ice (explorers of place) | DC polar |

**Original · inspired‑by · use now (no permission)**

| Guide *(placeholder name)* | Inspired by | Domain → habitat (kept distinct from the real person) |
|---|---|---|
| **Captain Mira Delmar** | Cousteau · Sylvia Earle · William Beebe | reef & open ocean — teal drysuit, boat *the Marlin* (no red cap, no *Calypso*) |
| **Dr. Amara Okafor** | Goodall · Dian Fossey · Biruté Galdikas | great apes & forest floor — field journal, binoculars |

**Real · living · only with written permission**

| Guide | Domain → habitat | Note |
|---|---|---|
| **Paul Rosolie** (b. 1987) | the Amazon | your outreach; Humboldt / Delmar cover the slot until then |
| **David Attenborough** (b. 1926) · **Sylvia Earle** (b. 1935) | narrator / oceans | aspirational |

---

## 4. Phase 1 — Map the original (the walkthrough as blueprint)

Goal: a **complete, machine‑readable interaction map** of the original — every screen, every
clickable region, every transition, every sound, and the overall shell/menu flow — to use as the
blueprint (what to recreate) and to fill the gaps our liberated data doesn't cover (the intro
sequence, the main hub UX, transitions, animations, click sounds, "feel").

**Two complementary methods — use both:**

### 4a. Native video understanding (fast, holistic)
Modern long‑context multimodal models (e.g. **Gemini 2.x**, which ingests video directly — even a
YouTube URL) can watch the *whole* walkthrough and emit a structured flow: "from the main menu,
clicking the globe opens the Atlas; from there…". Prompt it for a **state graph** (screens →
hotspots → destinations + transition/sound notes). Great for the *flow and feel*; cross‑check it
against our existing hotspot data.

### 4b. Keyframe extraction (precise UI reference)
Your instinct is right — but don't blind‑sample at 30fps. Extract **one frame per distinct
screen/state** via **scene‑change detection**, then de‑dupe:

```bash
yt-dlp -f "bestvideo" -o walkthrough.mp4 "<YOUTUBE_URL>"         # download
# keyframes at scene cuts (tunable threshold), not every frame:
ffmpeg -i walkthrough.mp4 -vf "select='gt(scene,0.30)',showinfo" -vsync vfr frames/%05d.jpg
# (or PySceneDetect for smarter shot boundaries)
# then perceptual-hash de-dupe near-identical frames:
#   imagehash / dHash → drop frames within a small Hamming distance
```

This yields ~a few hundred *meaningful* frames (one per screen/animation beat) instead of tens of
thousands. Feed those to a vision model to **label each** (which screen, what's clickable, where it
links) and to serve as **layout reference** for the artists/AI later. Also **transcribe the
narrator's audio** (Whisper) — walkthrough commentary often explains the navigation.

**Merge** 4a + 4b with our existing liberated nav graph → the canonical **`interaction-map.json`**:
a scene graph of `{ screenId, art-intent, hotspots:[{region, action, target}], transitions, sounds }`.

> **Deliverables:** `interaction-map.json` (the blueprint), an annotated UX‑flow doc, and a folder
> of reference keyframes per screen.

---

## 5. Phase 2 — Design & the engine

**Art direction / style bible (do this *before* generating a single final asset).**
**The art direction is LOCKED: photo‑realistic.** It honors what actually made the original discs feel
real — *real photographs and video of the animals*, composited into montage scenes with 90s tech. We
do the same thing at modern fidelity: photo‑real creatures (AI‑generated and/or real CC photos) cut
out and composited into photo‑real habitat plates, with real openly‑licensed video on reveal. So the
style bible isn't "illustrated vs. painted" — it's the *photographic* language: per‑habitat
lighting/time‑of‑day, depth‑of‑field, color grade, and how cut‑outs are matted believably into a
scene. The one thing still open is how the **UI chrome** (journal, cards, nav) frames that photography
— clean‑modern over photos vs. a tactile field‑guide/specimen frame (decide in Claude Design). Produce
a 1–2 page style bible + a set of **anchor images** every generation references. (Photo‑realism makes
*consistency & species‑accuracy* the #1 risk — see §7's reference‑photo workflow and §9.)

**The engine — a data‑driven hypermedia runtime.** The game is essentially a *state machine of
scenes with hotspots, transitions, audio, and history* — which is exactly what `classic.screens`
already is, just richer. Build a small engine that reads a scene graph and handles:

- hotspot hit‑testing (responsive %‑based regions, touch‑friendly),
- **reveal/transition animations** (the **View Transitions API** gives buttery screen‑to‑screen
  morphs — perfect for "discovery" feel; Astro supports it natively),
- audio (ambient + SFX + narration), history/back, the Field Journal state (persisted locally),
- progressive‑disclosure logic (hidden → hinted → revealed), reduced‑motion + reveal‑all toggles.

**Tech:** stay on **Astro** for the shell/SEO/static content; build the interactive "world" as a
**single `client:only` island in [Solid](https://www.solidjs.com/)** (via `@astrojs/solid-js`)
driving the engine. Solid is the deliberate pick: fine-grained reactivity (no virtual-DOM diffing)
and a ~7 KB runtime keep a game-like, animation-heavy UI smooth on **low-end Fire tablets** — where a
heavier framework would hurt most. Astro stays the shell; Capacitor wraps whatever the build emits
(framework-agnostic). If a single scene ever needs particles/real-time, add **Pixi.js** for that
layer and keep the chrome in Solid. Keep media **lazy‑loaded, responsive (`srcset`), WebP/AVIF + streamed video.**

**Accessibility & the mystery tension:** default to subtle/hidden; always offer (a) a "reveal
interactive spots" toggle, (b) full keyboard navigation, (c) `prefers-reduced-motion` paths, and
(d) text alternatives. Mystery for those who want it; clarity for those who need it.

---

## 5½. Platforms & packaging (web + native)

Creaturia ships **both as a web app and as an installable native app** — the goal is
*maximum reach for kids on whatever device they have*:

| Store | Devices | Build |
|---|---|---|
| **Apple App Store** | iPhone, iPad | the web build wrapped with **Capacitor** |
| **Google Play** | Android phones & tablets | the same build, Android shell |
| **Amazon Appstore** | **Fire tablets** (Fire OS = Android) | the Android build, no Google‑Play‑Services deps |
| **Web / PWA** | any browser | the same Astro app |

**One offline‑capable web codebase → web + iOS + Android + Fire.** This is *why* §5 stays Astro + a
client‑island engine: **Capacitor** reuses it wholesale and adds native capability (haptics, local
storage, audio, share, status‑bar/safe‑area) behind a thin `platform` layer that falls back to web
APIs in the browser — sketch in [`src/lib/platform.ts`](./src/lib/platform.ts). No second codebase,
no React‑Native/Flutter rewrite.

**Consequences that become first‑class design & engineering constraints (fold into §5/§9):**

- **Form factors.** Phones *and* tablets across many aspect ratios → scenes must be responsive or
  **pannable**, never a fixed composition that crops; honor **safe‑area insets** (notch, home bar).
- **Low‑end is the floor, not the ceiling.** Fire tablets are cheap and slow — performance‑budget
  motion/media, degrade gracefully, and **playtest the slice on a real Fire tablet**, not just an
  iPad. (Promote this to a top §9 risk.)
- **Offline‑first assets.** Bundle the slice's media; fetch later habitats **on demand** (app‑size
  limits) — the asset pipeline (§7) emits both a *bundled* and a *remotely‑fetched* tier.
- **Kids‑store compliance.** No third‑party ads / tracking / analytics / data collection; parent‑gate
  any external links or purchases; ship a privacy policy. The existing no‑ads, non‑commercial posture
  already fits — keep it that way in the UI.
- **Release overhead** (plan for it): Apple Developer ($99/yr), Google Play ($25 once), Amazon
  Appstore (free); per‑store review; app icon / splash / store screenshots (Claude Design — see the
  design guide's Prompt 5).

> Net: going native costs us a **thin platform layer + a packaging/release pipeline**, not a rewrite —
> but it makes **performance, offline, and store‑compliance** first‑class from the vertical slice
> onward, not afterthoughts.

---

## 6. Phase 3 — Content (clean‑room rewrite)

The museum edition transcribed Microsoft's prose *verbatim* — fine for preservation, not for a
clean public product. **Facts are free; the exact wording isn't.** So:

- **Rewrite every creature's text in our own kid‑friendly voice** from the structured facts (an LLM
  drafts; a human edits for accuracy, tone, and that spark of wonder). This is *easy* now that the
  data is structured — and it lets us make the writing *better* and more playful than the original.
- **Write the discovery layer:** short "did you know?" surprises, reveal one‑liners, narration
  scripts for guides, habitat intros, journal entries.
- Keep the data shape (so the engine and pipeline are unchanged); just swap the strings.

---

## 7. Phase 4 — Asset generation (the multi‑model engine)

### Images — photo‑realistic, generated *and* sourced
- **Two feedstocks, one photographic look (the modern montage):** (a) **AI‑generated** photo‑real
  animals & habitat plates, and (b) **real openly‑licensed photos** — Wikimedia Commons, iNaturalist
  (CC), Pexels/Pixabay. Compose both into layered scenes — exactly what the originals did with 90s
  montage, now at modern fidelity.
- **Models:** **Gemini 2.5 Flash Image ("Nano Banana")** — strong at *consistency & iterative
  editing*, ideal for keeping a creature photo‑real & on‑model across poses and for editing a scene to
  add/hide animals; **GPT‑image / GPT‑5** and **Imagen** as alternates. Best per task; no single model
  wins everything.
- **Species‑accuracy is the photo‑real catch:** a slightly‑off *stylized* jaguar reads as "art"; a
  slightly‑off *photo‑real* jaguar reads as **wrong/uncanny**. So **condition generation on real
  reference photos** — feed CC Commons/iNaturalist images of the actual species as img2img/editing
  refs so the AI output stays anatomically true — rather than prompting from text alone.
- **The consistency playbook (this is where projects fail):**
  - Lock the **style bible** into every prompt; pass **anchor/reference images** (incl. the real
    species photos above).
  - Generate each **creature once as a photo‑real "character sheet"**, then *edit* that reference into
    new poses/scenes rather than re‑rolling from scratch.
  - Fix seeds where supported; build scenes in **layers** (habitat plate → creature cut‑outs
    composited/in‑painted) so you control hotspot placement and can matte cut‑outs believably.
  - A **QA loop**: a vision model (and a human) scores each asset for photographic consistency,
    **species/anatomy accuracy**, lighting‑match, and on‑model‑ness; rejects route back for re‑edit.
    (Great fit for multi‑agent orchestration — §8.)
  - **Label AI‑generated images as such** in the ledger (honesty + evolving kids‑store AI disclosure).
- **Asset types:** habitat plates (the explorable worlds), per‑creature cut‑outs (multiple states:
  hidden/cameo/revealed/"action"), the world map, UI chrome & icons, transition art, journal art.

### Video — sourcing, not generating (mostly)
- **Prefer real, openly‑licensed animal footage** — it's authentic, educational, and free of the
  consistency problems of AI video: **Pexels, Pixabay, Wikimedia Commons, iNaturalist (CC),
  Internet Archive, NASA/gov sources.** Vet each license; **log attribution** in a ledger.
  *(License gotcha — applies to the sourced photos in §Images too: iNaturalist & Commons are licensed
  **per item**, and much of iNaturalist is **CC‑BY‑NC or All‑Rights‑Reserved**, not CC0. We're
  non‑commercial, so CC‑BY(‑NC) is fine **with attribution**, but filter out ARR, prefer
  research‑grade + CC0/CC‑BY, and record the exact license per asset.)*
- Multiple short clips per creature (your "maybe multiple YouTube videos" idea) → variety + the
  "what will I get?" surprise. Build a **sourcing + license‑tracking pipeline**.
- **AI video (Veo / Sora)** only for short *transitions/ambiance* where real footage doesn't fit —
  used sparingly (cost/consistency).

### Audio
- **Narration:** modern TTS with warm, kid‑friendly voices (**ElevenLabs / Google / OpenAI**) — one
  voice per guide character for personality.
- **SFX & ambient:** CC libraries (Freesound, etc.) — roars, rustles, reef bubbles, savanna wind.
  Sound is *half* the magic; budget real effort here.

> Every generated/sourced asset lands in an **asset manifest + license ledger** (`assets.json`):
> source, license, attribution, prompt/seed, model — so the credits page writes itself and the
> project stays defensible.

---

## 8. Phase 5 — Build it (vertical slice first, then scale)

**Do not boil the ocean.** The #1 way this dies is trying to generate 66 creatures × 5 habitats up
front. Instead:

1. **One magical vertical slice:** pick a single habitat (say the **rainforest**) with ~5 creatures.
   Build the *entire* loop — explorable scene, hidden creatures, reveals, video, sound, journal,
   transitions — across mobile/tablet/desktop. **Playtest it.** Iterate until it has the magic.
2. **Then scale** via the pipeline + **multi‑agent orchestration** (the same workflow approach that
   liberated 66 animals): fan out content rewrites, asset generation, QA, and scene assembly, with
   adversarial review gates. The slice becomes the template; the swarm fills the world.

---

## 9. Risks & honest expectations

| Risk | Mitigation |
|---|---|
| **AI image *consistency*** (the big one) | Style bible + anchor refs + character‑sheet‑then‑edit + QA loop. Accept that this is the main cost center. |
| **"It's not actually fun"** | Tech can't guarantee wonder. Vertical slice + **playtest with kids** before scaling. |
| **Video licensing** | CC‑only sourcing + license ledger; when unsure, don't use it. |
| **Scope & cost** | This is a *months‑long, multi‑model, real‑budget* effort. Vertical‑slice gating keeps spend tied to proven value. |
| **Performance** (lots of media) | Responsive `srcset`, AVIF/WebP, lazy‑load, streamed/poster video, code‑split the engine. |
| **Accessibility vs. mystery** | Design the tension on purpose (reveal toggle, keyboard, reduced‑motion). |

---

## 10. Multi‑model orchestration map

| Task | Best‑fit model(s) |
|---|---|
| Watch the walkthrough → nav/flow map | **Gemini 2.x** (native video understanding) |
| Label keyframes / QA generated art | A strong **vision** model (Gemini / GPT‑5 / Claude vision) |
| Rewrite prose, narration scripts, journal copy | **Claude** / GPT‑5 (long‑form, voice control) |
| Generate & *edit* images (consistency) | **Gemini 2.5 Flash Image "Nano Banana"**; GPT‑image; Imagen |
| Short transition/ambient video | **Veo / Sora** (sparingly) |
| Narration TTS | **ElevenLabs / Google / OpenAI** voices |
| Source & license real footage | Human + scripted search across CC libraries |
| Orchestrate the pipeline (fan‑out + gates) | **Claude Code multi‑agent workflows** |

---

## 11. Phased roadmap (suggested order)

- [ ] **P1 — Map** the original from the walkthrough (+ merge with our data) → `interaction-map.json`
- [ ] **P2 — Design**: style bible, interaction/motion design, the engine prototype, responsive system
- [ ] **P3 — Content**: clean‑room rewrite of one habitat's creatures (then all)
- [ ] **P4 — Assets**: generation/sourcing pipeline + license ledger; produce the slice's assets
- [ ] **P5 — Vertical slice**: one habitat, fully magical, all devices → **playtest with kids**
- [ ] **P6 — Scale**: orchestrate generation/build across all habitats & 66 creatures
- [ ] **P7 — Launch**: clean, credited, responsive, SEO/OG, on Cloudflare — *for any kid, anywhere.*

---

## 12. Repo / branch strategy

- This plan lives on the **`reimagined`** branch. `main` (the museum edition) stays the canonical
  preservation and stays deployable.
- Creaturia lives in its **own app dir** (`apps/creaturia/`) so the two editions can
  coexist — perhaps even cross‑linked ("Explore the game" ↔ "View the 1994 archive").
- Reuse `web/data` (structure/facts) and the tooling; everything *asset*‑related is new and tracked
  in the license ledger.

---

*This is a starting blueprint, meant to be argued with and sharpened — especially the experience
concept (§3) and the style bible (§5). The single most important next step is small: **map the
original from the walkthrough, then build one habitat until it feels like magic.** Everything else
scales from a slice that already works.*
