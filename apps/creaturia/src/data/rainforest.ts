// rainforest.ts — the vertical-slice scene-graph: one Amazon scene hiding five creatures.
//
// CONTENT: clean-room rewrites in our own kid voice, drafted from the *facts* in the museum data
// (facts aren't copyrightable; the original wording is). Ids match the museum creature ids so the
// full data can be back-filled later (jagu/arow/harp/aant/boac). See CREATURIA.md §6.
//
// ART: abstract placeholders only — a color + a rough inline SVG silhouette per creature. These prove
// the spot→reveal→record loop is fun before any generated art exists (CREATURIA.md §8, Prompt 3).

import type { SceneGraph } from '../engine/scenegraph';

export const rainforest: SceneGraph = {
  start: 'rainforest',

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
    rainforest: {
      id: 'rainforest',
      name: 'The Steaming Rainforest',
      // Placeholder backdrop — layered greens + a warm light shaft. Becomes a painted scene later.
      bg:
        'radial-gradient(60% 90% at 78% 8%, #2f8f57cc 0%, transparent 55%),' +
        'radial-gradient(120% 80% at 20% 110%, #04140c 0%, transparent 60%),' +
        'linear-gradient(180deg, #135236 0%, #0c3623 45%, #06180f 100%)',
      ambient: '', // TODO(assets): CC rainforest ambience loop, played via platform.playSound
      onward: [],
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
