import { createSignal, onMount, Show } from 'solid-js';
import './engine.css';
import SceneStage from './SceneStage';
import Journal from './Journal';
import RevealCard from './RevealCard';
import GuideCard from './GuideCard';
import { createJournal } from './state';
import { withTransition } from './transitions';
import { haptics } from '../lib/platform';
import type { Guide, Hotspot, RevealKind, SceneGraph } from './scenegraph';

interface ActiveReveal {
  creatureId: string;
  kind: RevealKind;
  isNew: boolean;
}

/** The whole game: one Solid island driving the scene-graph — the world-map hub, travel, hit-testing,
 * reveals, the Field Journal, and the cross-link "lures". Everything platform-specific goes through
 * src/lib/platform.ts. */
export default function World(props: { graph: SceneGraph }) {
  const graph = props.graph;
  const creatureList = Object.values(graph.creatures);

  const journal = createJournal(creatureList.length);
  const [sceneId, setSceneId] = createSignal(graph.start);
  const [reveal, setReveal] = createSignal<ActiveReveal | null>(null);
  const [guide, setGuide] = createSignal<Guide | null>(null);
  const [revealAll, setRevealAll] = createSignal(false);
  const [luredId, setLuredId] = createSignal<string | null>(null);
  const [nudgedId, setNudgedId] = createSignal<string | null>(null);

  const scene = () => graph.scenes[sceneId()];
  // The hub is the start scene (the world map): everywhere else offers the way back to it.
  const atHub = () => sceneId() === graph.start;
  let lureTimer: ReturnType<typeof setTimeout> | undefined;
  let nudgeTimer: ReturnType<typeof setTimeout> | undefined;

  onMount(() => journal.visit(graph.start));

  function travel(to: string) {
    withTransition(() => {
      setSceneId(to);
      journal.visit(to);
    });
  }

  function activate(spot: Hotspot) {
    // A "place" hotspot travels — unless it's a locked habitat, which answers with a gentle
    // "coming soon" nudge (a tease of the bigger world, never a dead click).
    if (spot.reveal === 'place') {
      if (spot.locked || !spot.to) {
        setNudgedId(spot.id);
        clearTimeout(nudgeTimer);
        nudgeTimer = setTimeout(() => setNudgedId(null), 2600);
        return;
      }
      travel(spot.to);
      return;
    }
    // A guide marker introduces an explorer (the intro card; the narrated tour is a follow-up).
    if (spot.reveal === 'guide') {
      setGuide((spot.guideId && graph.guides?.[spot.guideId]) || null);
      return;
    }
    // Everything else uncovers a creature (the varied payload).
    if (!spot.creatureId) return;
    const isNew = journal.record(spot.creatureId, sceneId());
    void haptics.tap(); // native buzz on discovery; no-op on the web where unsupported
    setReveal({ creatureId: spot.creatureId, kind: spot.reveal, isNew });
  }

  function followOnward(creatureId: string) {
    setReveal(null);
    // the "lure": pulse the cousin/rival's hiding spot so you're pulled deeper
    setLuredId(creatureId);
    clearTimeout(lureTimer);
    lureTimer = setTimeout(() => setLuredId(null), 6000);
  }

  return (
    <div class="rf-root">
      <header class="rf-topbar">
        <Show when={!atHub()}>
          <button class="rf-btn" onClick={() => travel(graph.start)}>
            ← Back to the map
          </button>
        </Show>
        <h1 class="rf-title">
          Creaturia <b>· {scene().name}</b>
        </h1>
        <span class="rf-spacer" />
        <button
          class="rf-btn"
          aria-pressed={revealAll()}
          onClick={() => setRevealAll((v) => !v)}
        >
          {revealAll() ? 'Hide spots' : 'Reveal spots'}
        </button>
      </header>

      <SceneStage
        scene={scene()}
        graph={graph}
        isFound={(id) => journal.isFound(id)}
        revealAll={revealAll}
        luredId={luredId}
        nudgedId={nudgedId}
        onActivate={activate}
      />

      <Journal creatures={creatureList} journal={journal} />

      <Show when={reveal()}>
        {(r) => (
          <RevealCard
            creature={graph.creatures[r().creatureId]}
            kind={r().kind}
            isNew={r().isNew}
            onClose={() => setReveal(null)}
            onFollow={followOnward}
          />
        )}
      </Show>

      <Show when={guide()}>
        {(g) => (
          <GuideCard
            guide={g()}
            onClose={() => setGuide(null)}
            onStart={(habitat) => {
              setGuide(null);
              travel(habitat);
            }}
          />
        )}
      </Show>

      {/* Landscape-locked: gently ask small phones to turn sideways. */}
      <div class="rf-portrait" aria-hidden="true">
        <p><span class="rf-roticon">📱</span>Turn me sideways to explore</p>
      </div>
    </div>
  );
}
