import { createSignal, onMount, Show } from 'solid-js';
import './engine.css';
import SceneStage from './SceneStage';
import Journal from './Journal';
import RevealCard from './RevealCard';
import { createJournal } from './state';
import { withTransition } from './transitions';
import { haptics } from '../lib/platform';
import type { Hotspot, RevealKind, SceneGraph } from './scenegraph';

interface ActiveReveal {
  creatureId: string;
  kind: RevealKind;
  isNew: boolean;
}

/** The whole game: one Solid island driving the scene-graph — hit-testing, reveals, the Field
 * Journal, and the cross-link "lures". Everything platform-specific goes through src/lib/platform.ts. */
export default function World(props: { graph: SceneGraph }) {
  const graph = props.graph;
  const creatureList = Object.values(graph.creatures);

  const journal = createJournal(creatureList.length);
  const [sceneId, setSceneId] = createSignal(graph.start);
  const [reveal, setReveal] = createSignal<ActiveReveal | null>(null);
  const [revealAll, setRevealAll] = createSignal(false);
  const [luredId, setLuredId] = createSignal<string | null>(null);

  const scene = () => graph.scenes[sceneId()];
  let lureTimer: ReturnType<typeof setTimeout> | undefined;

  onMount(() => journal.visit(graph.start));

  function activate(spot: Hotspot) {
    // A "place" hotspot travels; everything else uncovers a creature (the varied payload).
    if (spot.reveal === 'place' && spot.to) {
      withTransition(() => {
        setSceneId(spot.to!);
        journal.visit(spot.to!);
      });
      return;
    }
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
        <h1 class="rf-title">
          Creaturia <b>· Rainforest</b>
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

      {/* Landscape-locked: gently ask small phones to turn sideways. */}
      <div class="rf-portrait" aria-hidden="true">
        <p><span class="rf-roticon">📱</span>Turn me sideways to explore the rainforest</p>
      </div>
    </div>
  );
}
