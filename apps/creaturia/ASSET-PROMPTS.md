# Creaturia — asset generation: the map, the prompts, the roster

Practical companion to [`CREATURIA.md`](./CREATURIA.md) §7 (Phase 4 — assets). Three things:
**(1)** how to make the photo-real/3D **world map**, **(2)** paste-ready **prompt templates** for
creatures & scenes, **(3)** the **creature roster v0** extracted from the Dangerous Creatures +
Oceans museum data.

> Every asset that comes out of this doc lands in the **license ledger** (`web/data/assets.json`):
> source, license, attribution, prompt/seed, model — and AI-generated images are labeled as such.

---

## 1 · The world map (photo-real / 3D)

**Don't generate the map from scratch — theme a real one.** A free, public-domain Earth is the
perfect img2img base: the geography stays accurate (so the engine's `%`-based hotspot regions stay
put forever), and the AI only does what it's good at — the *look*.

### Free base assets (all safe for the ledger)

| Asset | What it is | License |
|---|---|---|
| **NASA Blue Marble** (visibleearth.nasa.gov) | The photo-real Earth texture, up to 500 m/px, 12 monthly versions (pick the season per mood) + cloud & night layers | Public domain |
| **NASA/NOAA ETOPO + GEBCO bathymetry** | Global terrain + seafloor relief heightmaps — the "3D" in the map | Public domain / free |
| **Natural Earth** (naturalearthdata.com) | PD vector coastlines/land polygons (→ accurate habitat-region outlines for hotspots) + **Natural Earth II** raster, a soft hand-tinted relief that already looks like a storybook atlas | Public domain |
| **Solar System Scope textures** | Ready-made 2K–8K Earth sphere textures (day/night/clouds/normal) for an instant globe render | CC-BY 4.0 |
| **Wikimedia Commons physical maps** | e.g. the Equal Earth physical map — pre-styled PD alternatives | PD/CC (check per item) |

### Free tools to add the 3D

- **Blender** (free) — the workhorse: displace a plane/sphere with ETOPO, texture with Blue Marble,
  exaggerate relief ~3–5×, tilt the camera, render one high-res 16:9 plate. **BlenderGIS** (free
  add-on) imports the real data in a few clicks. Render once → ship a static image; zero runtime cost.
- **three.js / globe.gl** (MIT) — a *real-time* 3D globe in the browser. Tempting, but wrong for
  v1: the engine is a lean Solid island targeting low-end Fire tablets, and CREATURIA.md's pan/zoom
  is planned as CSS transforms over a **pre-rendered plate**. Park this as a possible v3 flourish.
- **Upscayl** (free, open source) — upscale the final plate for tablet retina without re-generating.

### AI restyle with what you have

- **Nano Banana (Gemini 2.5 Flash Image)** — the right tool here, for the same reason §7 picked it:
  **iterative editing with consistency**. Feed it the Blue Marble/Blender render and restyle
  *keeping the geography pinned* (template T4 below), then do per-habitat edits one at a time
  (T5) — make the Amazon steam, the reef shelf glow — without the rest of the map drifting.
- **GPT-image (ChatGPT)** — good for *mood exploration* and alternate art directions in one shot;
  weaker at holding exact coastlines. Use it to explore, then rebuild the winner via the
  base-asset + Nano Banana route.

### The recommended recipe

1. Blue Marble (+ ETOPO relief in Blender if you want true 3D depth) → one 16:9 base render.
2. Nano Banana img2img: restyle to the Creaturia grade (T4), then per-habitat vignette edits (T5).
3. Upscale (Upscayl) → slice if needed (ocean layer / land layer for parallax).
4. Drop into the engine: the map is already data — swap `worldmap.bg`/`backdrop` in
   `src/data/world.ts` for the plate; **the hotspot regions don't change**.
5. Ledger entries: NASA (PD) + "AI-restyled with Gemini 2.5 Flash Image" + prompt.

---

## 2 · Prompt templates

Per §7's consistency playbook: **lock the style into every prompt, condition on real reference
photos** (Wikimedia Commons / iNaturalist — CC0/CC-BY, research-grade; record each item's license),
generate each species **once as a character sheet**, then *edit* — never re-roll from scratch.

### The style lock (prepend to every image prompt)

```text
STYLE LOCK — Creaturia. Photo-realistic documentary wildlife photography, National Geographic
grade. Real-photo look: telephoto DSLR, natural light only, shallow depth of field, true-to-species
anatomy. NOT illustration, NOT cartoon, NOT a 3D-render look. No text, watermarks, or borders.
Color grade: [HABITAT GRADE from the table below]. Match the attached reference photos for species
accuracy and the attached anchor image for grade.
```

### Habitat grades (the per-world photographic language — §5's style bible in one table)

| Habitat | Grade line to paste |
|---|---|
| Rainforest | humid pre-dawn emerald greens, god-rays through canopy mist, deep shadow pockets |
| Coral reef | sunlit turquoise shallows at ~10 m, dancing light caustics, crystal clarity |
| Savanna | golden-hour dusk, long amber shadows, dry haze on the horizon |
| Polar ice | blue-hour arctic light, cold cyan-whites, low sun sparkling on ice |
| Desert (later) | hard noon light, bleached sand tones, faint heat shimmer |
| Rivers & wetlands (later) | overcast soft light, tannin-brown water, wet green banks |

### T1 · Habitat plate (the explorable scene — generate FIRST, per habitat)

```text
[STYLE LOCK]
A 16:9 photographic habitat plate of [SCENE — e.g. an Amazon rainforest interior at dawn, a slow
river curling through the frame]. Explorer's eye level. Rich layered depth: detailed foreground
[leaf litter, buttress roots], midground [riverbank, fallen log], softly blurred background [mist
between trunks]. CRITICAL: no animals anywhere in the frame — the scene must feel alive but empty,
with 5–7 natural hiding pockets (dark hollows, dense foliage, water edges, high branches) where a
creature can later be composited. Even, believable lighting; high resolution, landscape.
```

*(Why empty: creatures are separate cut-outs so hotspot placement stays controllable and the same
plate hosts different creature sets — exactly the originals' montage approach.)*

### T2 · Creature character sheet (once per species — the anchor)

```text
[STYLE LOCK]
Using the attached real reference photos of [COMMON NAME (Scientific name)], generate a photo-real
character sheet of ONE consistent adult individual on a neutral mid-grey studio background:
(a) full-body side profile, (b) 3/4 front view, (c) head close-up, (d) one species-typical action
pose [e.g. mid-pounce]. The SAME individual in every view — identical markings, proportions, eye
color. Anatomy must match the references exactly. Soft even light, no background shadows.
```

### T3 · Cut-out states (EDIT the sheet — never regenerate)

```text
From this character sheet (attached), produce the [STATE] of the SAME individual on a plain
neutral background for clean cut-out, lit to match the attached habitat plate ([HABITAT GRADE],
key light from [DIRECTION]):
 - hidden/cameo: [only the eyes and brow above a log; body swallowed by shadow]
 - revealed: alert full body, caught mid-glance toward the viewer
 - action: [species-typical burst — pounce / strike / dive / wings flaring]
```

### T4 · World map restyle (the §1 recipe's AI step)

```text
Using the attached satellite/relief render of Earth (NASA Blue Marble), restyle it into Creaturia's
world-map hub, KEEPING THE GEOGRAPHY EXACTLY IN PLACE — continent outlines must not move (game
hotspots depend on them). Photo-real "explorer's atlas seen from orbit" look: gently exaggerated
3D terrain relief, deep night-blue oceans with subtle seafloor relief, habitats reading as distinct
textures — steaming emerald Amazon, amber savanna belt, turquoise reef shelf off Australia,
white-blue polar caps. Soft atmospheric rim light at the edges. No labels, borders, or icons — the
UI draws those. 16:9, high resolution.
```

### T5 · Per-habitat map vignette (iterative edits, one at a time)

```text
Edit the attached Creaturia world map: make the [Amazon basin] gently glow with life — [denser
canopy texture, one wisp of rising mist] — WITHOUT moving any coastline or changing the global
grade. Leave every other region untouched.
```

### T6 · Explorer-guide portrait

```text
[STYLE LOCK — portrait grade: warm window light, field-tent backdrop]
A kid-friendly photo-real portrait of [Alexander von Humboldt (1769–1859)] as a field naturalist,
grounded in the attached public-domain portraits for likeness: [wind-swept hair, high collar, a
leather field journal in hand], rainforest bokeh behind. Honest to the historical face —
approachable, never caricature.
```

*(Inspired-by guides — Capt. Mira Delmar, Dr. Amara Okafor — same template but a DISTINCT invented
face/outfit; explicitly "not resembling any real person".)*

### T7 · QA gate (paste into a vision model with the output + references)

```text
Score this generated image 1–5 on: (a) species/anatomy accuracy vs the attached reference photos,
(b) photographic realism — flag AI artifacts (extra limbs, melted fur/scales, wrong pupil shape),
(c) lighting match to [HABITAT GRADE], (d) on-model vs the character sheet. Reject if any score
< 4 and say in one line what to fix.
```

### Worked example — the jaguar (slice creature #1)

1. Collect 4–6 CC0/CC-BY photos of *Panthera onca* (Commons, iNaturalist research-grade) → ledger.
2. T2 with "Jaguar (Panthera onca)" → character sheet → human + T7 QA.
3. T3 ×3 states, lit for "rainforest / god-rays from upper left".
4. Composite into the T1 rainforest plate at the scene-graph's `h-jagu` region.

---

## 3 · Creature roster v0 (from the museum data)

Extracted from `apps/dangerous-creatures/web/data/browse.json` (66 animals — Scorpion is missing
from its regions taxonomy, caught from the entry files) and `apps/oceans/web/data/browse.json`
(41 Sea Life entries). Ids match the museum data, so full facts/media back-fill later — same trick
as the slice's five.

### Dangerous Creatures — 66, grouped by target Creaturia habitat

*(DC's own habitat taxonomy; animals in several habitats are listed at each — pick one home per
creature when scenes are assembled.)*

- **Rainforest & jungle (13):** Army Ant `aant` · Boa `boac` · Centipede `cent` · Cockroach `cock`
  · Harpy Eagle `harp` · Jaguar `jagu` · Mangrove Snake `mang` · Passion-vine Caterpillar `post` ·
  Poison Arrow Frog `arow` · Python `pyth` · Tarantula `tran` · Tiger `tigr` · Vampire Bat `vamp`
- **Grassland & savanna (20):** Baboon `babn` · Black Mamba `mamb` · Cape Buffalo `cbuf` · Cape
  Hunting Dog `cdog` · Cheetah `chee` · Cobra `cobr` · Elephant `elef` · European Adder `addr` ·
  Hyena `hyen` · Killer Bee `kbee` · Komodo Dragon `komd` · Leopard `leop` · Lion `lion` ·
  Rattlesnake `rttl` · Rhinoceros `rhin` · Vulture `vult` · Warthog `wart` · Wolf `wolf` ·
  (+ Army Ant, Python)
- **Oceans & coral reefs (14):** Australian Sea Wasp `swsp` · Barracuda `bara` · Blue-ringed
  Octopus `boct` · Crab `crab` · Giant Squid `gsqu` · Great White Shark `gwsh` · Hammerhead Shark
  `hamr` · Killer Whale `orca` · Lionfish `lfsh` · Moray Eel `meel` · Porcupine Fish `porc` ·
  Portuguese Man-of-War `mwar` · Sea Snake `seas` · Stingray `sray`
- **Rivers, lakes & wetlands (10):** Alligator `alig` · Cane Toad `cane` · Crocodile `croc` ·
  Electric Eel `eeel` · Hippopotamus `hipp` · Mosquito `mosq` · Piranha `pira` · Platypus `plat` ·
  Snapping Turtle `snap` · (+ Mangrove Snake, Stingray)
- **Desert (3 + shared):** Gila Monster `gila` · Scorpion `scor` · (+ Cockroach, Rattlesnake,
  Tarantula)
- **Polar & tundra (2 + shared):** Polar Bear `pbea` · (+ Killer Whale, Wolf, Wolverine)
- **Forest, woodland & mountains (10):** Black Widow Spider `bwid` · Cougar `coug` · Fire
  Salamander `fsal` · Funnel-web Spider `funl` · Grizzly Bear `griz` · Tasmanian Devil `tasm` ·
  Wasp `wasp` · Wolverine `wlvr` · (+ Cobra, Elephant, Adder, Komodo, Leopard, Rhino, Tiger, Wolf)
- **Cities & farmland (1 + shared):** Rat `rats` · (+ Black Widow, Cane Toad, Cockroach, Killer
  Bee, Mosquito, Vampire Bat, Wasp)

### Oceans — 41 Sea Life entries (mostly *groups* → pick 1–2 star species each)

Anemones `anem` · Angler Fish `angl` · Baleen Whales `whlb` · Barnacles `barn` · Birds of Lakes and
Coasts `lake` · Boxfish `boxy` · Clams, Oysters & Scallops `clam` · Corals `cora` · Crabs `crab` ·
Dolphins & Porpoises `dolp` · Eels `eels` · Fanworms & Bristleworms `fanw` · Fascinating Sharks
`fasc` · Flatworms `flat` · Flying Sea Birds `bird` · Inflatable Fish `infl` · Jellyfish &
Men-of-War `jell` · Lobsters `lobs` · Manatees & Dugongs `mana` · Marine Iguanas `igua` · Octopuses
`octo` · Penguins `peng` · Rays `rays` · Saltwater Crocodiles `croc` · Scary Sharks `shar` ·
Scorpionfish `scor` · Sea Horses & Pipefish `pipe` · Sea Mosses `moss` · Sea Otters `ottr` · Sea
Slugs `slug` · Sea Snakes `snak` · Sea Squirts `sqrt` · Sea Turtles `turt` · Sea Urchins & Sea
Cucumbers `urch` · Seals & Sea Lions `seal` · Shrimp `shri` · Sponges `spon` · Squid & Cuttlefish
`squi` · Starfish `star` · Toothed Whales `whlt` · Walruses `walr`

*(Oceans' habitat topics — Coral Reefs `reef`, The Shallows `shal`, The Abyss `abys`, The Shoreline
`shor`, Islands `isla` — are ready-made scene briefs for T1 plates.)*

### Growing the list later

- **Dinosaurs** adds 166 more entries when that world comes (same extraction from
  `apps/dinosaurs/web/data/browse.json`).
- **Gap-fill per habitat** for richness beyond "dangerous": rainforest (sloth, toucan, morpho
  butterfly, capybara, anaconda), reef (clownfish, parrotfish, reef octopus, manta), polar (emperor
  penguin, arctic fox, narwhal, snowy owl), savanna (giraffe, zebra, meerkat, secretary bird).
  All new entries need clean-room facts (§6) — no museum text to lean on.
- Overlaps between discs (crocodile, sea snake, crab, squid…) collapse into one Creaturia creature
  with the richer fact set.
