// world.ts — the game's scene-graph: the WORLD MAP hub (the main exploration surface, issue #27)
// plus the vertical-slice rainforest scene hiding five creatures.
//
// CONTENT: clean-room rewrites in our own kid voice, drafted from the *facts* in the museum data
// (facts aren't copyrightable; the original wording is). Ids match the museum creature ids so the
// full data can be back-filled later (jagu/arow/harp/aant/boac). See CREATURIA.md §6.
//
// ART: abstract placeholders only — CSS gradients + rough inline SVG silhouettes. These prove the
// map→habitat→spot→reveal loop is fun before any generated art exists (CREATURIA.md §8, Prompt 3).
// The map backdrop is a stylized flat-regions world (a zoomable globe is a v2 of this hub).

import type { SceneGraph } from '../engine/scenegraph';

// The world-map art layer: abstract continent blobs + a faint graticule, drawn into the stage's
// 16:9 box (viewBox 0 0 160 90). Becomes a photo-real map treatment later — same hotspots.
const WORLD_BACKDROP =
  // graticule: three latitude lines + two bowed meridians, barely-there
  '<g stroke="#cfe6d8" stroke-opacity="0.10" fill="none" stroke-width="0.6">' +
  '<path d="M0 23 H160 M0 45 H160 M0 67 H160"/>' +
  '<path d="M44 0 Q38 45 44 90 M116 0 Q122 45 116 90"/>' +
  '</g>' +
  // arctic cap
  '<path d="M30 0 H130 Q126 9 100 11 Q66 13 38 9 Q32 7 30 0Z" fill="#b9d9e8" opacity="0.35"/>' +
  // north america
  '<path d="M14 10 Q30 4 40 12 Q48 18 40 24 Q34 26 36 32 Q30 40 24 34 Q12 30 10 20 Q10 13 14 10Z" fill="#1b5e3c"/>' +
  // south america (the rainforest's home)
  '<path d="M30 40 Q40 36 42 46 Q44 56 38 66 Q34 76 30 70 Q26 60 27 50 Q27 43 30 40Z" fill="#217a4b"/>' +
  // eurasia
  '<path d="M66 12 Q86 4 108 10 Q124 14 118 24 Q108 32 92 28 Q76 30 68 24 Q60 17 66 12Z" fill="#1b5e3c"/>' +
  // africa (the savanna's home)
  '<path d="M70 34 Q82 30 86 40 Q88 50 82 60 Q76 68 72 60 Q66 48 67 40 Q67 36 70 34Z" fill="#217a4b"/>' +
  // australia (the reef's neighbour)
  '<path d="M120 58 Q130 54 136 60 Q138 68 130 70 Q120 72 117 66 Q116 60 120 58Z" fill="#1b5e3c"/>';

// Habitat marker silhouettes (viewBox 0 0 100 100, currentColor — same contract as creatures).
const MAP_ART = {
  rainforest: // a broad kapok-style canopy
    '<rect x="46" y="56" width="8" height="30" rx="3" fill="currentColor"/>' +
    '<ellipse cx="50" cy="38" rx="30" ry="17" fill="currentColor"/>' +
    '<ellipse cx="24" cy="50" rx="15" ry="9" fill="currentColor"/>' +
    '<ellipse cx="76" cy="50" rx="15" ry="9" fill="currentColor"/>',
  reef: // branching coral + a rising bubble
    '<path d="M50 88 V50 M50 64 Q36 60 34 42 M50 58 Q64 54 66 38 M34 42 Q32 33 37 27 M66 38 Q71 30 65 23" ' +
    'stroke="currentColor" stroke-width="8" fill="none" stroke-linecap="round"/>' +
    '<circle cx="52" cy="14" r="5" fill="currentColor"/>',
  savanna: // a flat-topped acacia
    '<path d="M46 84 h8 L52 50 L60 42 L55 40 L50 46 L44 38 L40 41 L47 50 Z" fill="currentColor"/>' +
    '<ellipse cx="50" cy="32" rx="33" ry="12" fill="currentColor"/>',
  polar: // jagged bergs on a waterline
    '<path d="M18 68 L33 40 L43 52 L56 28 L70 56 L81 46 L88 68 Z" fill="currentColor"/>' +
    '<path d="M12 78 H88" stroke="currentColor" stroke-width="6" stroke-linecap="round"/>',
};

// Humboldt's portrait bust — swept-back hair and a high 1800s collar, silhouette-rough.
const HUMBOLDT_PORTRAIT =
  '<circle cx="50" cy="33" r="15" fill="currentColor"/>' +
  '<path d="M35 31 Q35 14 52 15 Q67 16 66 32 L61 23 Q53 18 43 23 Z" fill="currentColor"/>' +
  '<path d="M24 88 Q26 60 42 53 L46 60 H54 L58 53 Q74 60 76 88 Z" fill="currentColor"/>' +
  '<path d="M46 60 L50 71 L54 60 Z" fill="currentColor"/>';

export const world: SceneGraph = {
  start: 'worldmap',

  guides: {
    humboldt: {
      id: 'humboldt',
      name: 'Alexander von Humboldt',
      years: '1769–1859',
      tagline: 'Naturalist · explorer of the Amazon and the Andes',
      invite:
        'I measured mountains, chased electric eels, and filled whole notebooks with questions. The rainforest is waiting — shall we?',
      color: '#e8cf9a',
      portrait: HUMBOLDT_PORTRAIT,
      habitat: 'rainforest',
    },
  },

  creatures: {
    jagu: {
      id: 'jagu',
      name: 'Jaguar',
      tagline: 'The silent king of the riverbank',
      fact: "A jaguar's bite is the strongest of any big cat — it can crunch straight through a turtle's shell, or a skull, in a single chomp.",
      color: '#e8a83a',
      silhouette:
        '<ellipse cx="52" cy="60" rx="30" ry="13" fill="currentColor"/>' +
        '<circle cx="20" cy="47" r="11" fill="currentColor"/>' +
        '<path d="M13 40 l-3 -8 l6 3z M22 39 l3 -8 l4 6z" fill="currentColor"/>' +
        '<rect x="30" y="68" width="6" height="16" rx="3" fill="currentColor"/>' +
        '<rect x="48" y="68" width="6" height="16" rx="3" fill="currentColor"/>' +
        '<rect x="66" y="68" width="6" height="16" rx="3" fill="currentColor"/>' +
        '<path d="M80 54 q20 -4 13 -24" stroke="currentColor" stroke-width="6" fill="none" stroke-linecap="round"/>',
      onward: { creatureId: 'boac', label: 'Something long is coiled in the branches nearby…' },
    },
    arow: {
      id: 'arow',
      name: 'Poison-Arrow Frog',
      tagline: 'Tiny, bright, and not to be licked',
      fact: 'This frog is smaller than your thumb — but the poison on its skin is strong enough to stop the heart of something a thousand times its size.',
      color: '#2fd0b6',
      silhouette:
        '<ellipse cx="50" cy="62" rx="26" ry="19" fill="currentColor"/>' +
        '<circle cx="36" cy="42" r="11" fill="currentColor"/>' +
        '<circle cx="64" cy="42" r="11" fill="currentColor"/>' +
        '<circle cx="36" cy="42" r="4" fill="#04140f"/>' +
        '<circle cx="64" cy="42" r="4" fill="#04140f"/>' +
        '<ellipse cx="22" cy="76" rx="13" ry="6" fill="currentColor"/>' +
        '<ellipse cx="78" cy="76" rx="13" ry="6" fill="currentColor"/>',
      onward: { creatureId: 'jagu', label: 'Big paw-prints lead off through the mud…' },
    },
    harp: {
      id: 'harp',
      name: 'Harpy Eagle',
      tagline: 'The shadow that falls from the canopy',
      fact: "A harpy eagle's talons are as long as a grizzly bear's claws — long enough to snatch a monkey clean out of a treetop.",
      color: '#cdd6dd',
      silhouette:
        '<path d="M50 34 L55 66 L45 66 Z" fill="currentColor"/>' +
        '<path d="M50 42 Q12 30 4 56 Q30 50 49 60 Z" fill="currentColor"/>' +
        '<path d="M50 42 Q88 30 96 56 Q70 50 51 60 Z" fill="currentColor"/>' +
        '<circle cx="50" cy="30" r="8" fill="currentColor"/>' +
        '<path d="M46 64 L54 64 L50 82 Z" fill="currentColor"/>',
      onward: { creatureId: 'arow', label: 'A flash of colour hops on a leaf below…' },
    },
    aant: {
      id: 'aant',
      name: 'Army Ants',
      tagline: 'A river of jaws on the march',
      fact: 'A single army-ant swarm can be millions strong. It flows across the forest floor like a living tide, and anything too slow to flee is stripped to the bone.',
      color: '#d9482f',
      silhouette:
        '<g fill="currentColor">' +
        '<ellipse cx="24" cy="40" rx="7" ry="4"/><ellipse cx="44" cy="34" rx="7" ry="4"/>' +
        '<ellipse cx="64" cy="42" rx="7" ry="4"/><ellipse cx="34" cy="56" rx="7" ry="4"/>' +
        '<ellipse cx="56" cy="58" rx="7" ry="4"/><ellipse cx="76" cy="52" rx="7" ry="4"/>' +
        '<ellipse cx="18" cy="60" rx="7" ry="4"/><ellipse cx="48" cy="72" rx="7" ry="4"/>' +
        '<ellipse cx="70" cy="70" rx="7" ry="4"/>' +
        '</g>',
    },
    boac: {
      id: 'boac',
      name: 'Boa Constrictor',
      tagline: 'The hug you do not walk away from',
      fact: "A boa doesn't crush its prey — every time the animal breathes out, the boa squeezes a little tighter, until there's no breath left to take.",
      color: '#7fae4b',
      silhouette:
        '<path d="M18 34 Q84 18 72 50 Q60 80 30 68 Q6 58 42 50" fill="none" stroke="currentColor" stroke-width="13" stroke-linecap="round"/>' +
        '<circle cx="18" cy="34" r="9" fill="currentColor"/>' +
        '<circle cx="15" cy="32" r="2" fill="#04140f"/>',
      onward: { creatureId: 'jagu', label: 'A low growl comes from the water’s edge…' },
    },
  },

  scenes: {
    worldmap: {
      id: 'worldmap',
      name: 'The World Map',
      // Placeholder backdrop — a deep night ocean; the continents are the SVG layer above.
      bg:
        'radial-gradient(80% 60% at 50% 0%, #1b5a86b0 0%, transparent 60%),' +
        'radial-gradient(120% 90% at 50% 120%, #020b14 0%, transparent 65%),' +
        'linear-gradient(180deg, #0e3a5e 0%, #092741 50%, #041322 100%)',
      backdrop: WORLD_BACKDROP,
      ambient: '', // TODO(assets): soft wind + distant gulls, played via platform.playSound
      onward: ['rainforest'],
      hotspots: [
        // The one enterable habitat (the vertical slice). More unlock as they're built.
        {
          id: 'm-rainforest',
          reveal: 'place',
          to: 'rainforest',
          label: 'Rainforest',
          color: '#38d17a',
          art: MAP_ART.rainforest,
          region: { x: 12, y: 42, w: 17, h: 42 },
        },
        // Locked "coming soon" habitats — intriguing silhouettes that tease the bigger world (#27).
        {
          id: 'm-reef',
          reveal: 'place',
          locked: true,
          label: 'Coral Reef',
          color: '#3fb9c9',
          art: MAP_ART.reef,
          region: { x: 69, y: 56, w: 17, h: 34 },
        },
        {
          id: 'm-savanna',
          reveal: 'place',
          locked: true,
          label: 'Savanna',
          color: '#d9a441',
          art: MAP_ART.savanna,
          region: { x: 39, y: 36, w: 17, h: 40 },
        },
        {
          id: 'm-polar',
          reveal: 'place',
          locked: true,
          label: 'Polar Ice',
          color: '#bfe3f2',
          art: MAP_ART.polar,
          region: { x: 28, y: 1, w: 36, h: 17 },
        },
        // The explorer guide's pin — mid-Atlantic, pointing the way to his rainforest.
        {
          id: 'm-humboldt',
          reveal: 'guide',
          guideId: 'humboldt',
          label: 'Humboldt',
          color: '#e8cf9a',
          art: HUMBOLDT_PORTRAIT,
          region: { x: 28.5, y: 26, w: 9, h: 15 },
        },
      ],
    },

    rainforest: {
      id: 'rainforest',
      name: 'The Steaming Rainforest',
      // Placeholder backdrop — layered greens + a warm light shaft. Becomes a painted scene later.
      bg:
        'radial-gradient(60% 90% at 78% 8%, #2f8f57cc 0%, transparent 55%),' +
        'radial-gradient(120% 80% at 20% 110%, #04140c 0%, transparent 60%),' +
        'linear-gradient(180deg, #135236 0%, #0c3623 45%, #06180f 100%)',
      ambient: '', // TODO(assets): CC rainforest ambience loop, played via platform.playSound
      onward: ['worldmap'],
      hotspots: [
        { id: 'h-jagu', creatureId: 'jagu', reveal: 'clip', hint: 'idle', region: { x: 30, y: 56, w: 22, h: 26 } },
        { id: 'h-arow', creatureId: 'arow', reveal: 'fact', hint: 'idle', region: { x: 53, y: 69, w: 10, h: 12 } },
        { id: 'h-harp', creatureId: 'harp', reveal: 'clip', hint: 'idle', region: { x: 65, y: 12, w: 22, h: 22 } },
        { id: 'h-aant', creatureId: 'aant', reveal: 'fact', hint: 'idle', region: { x: 7, y: 78, w: 20, h: 14 } },
        { id: 'h-boac', creatureId: 'boac', reveal: 'fact', hint: 'idle', region: { x: 71, y: 44, w: 18, h: 22 } },
      ],
    },
  },
};
