import { createSignal, onCleanup, onMount, Show } from 'solid-js';
import type { Creature, Hotspot as HotspotData } from './scenegraph';

/**
 * One discoverable region. Progressive disclosure:
 *   hidden  → nothing shown (you have to poke around)
 *   hinted  → a slow shimmer appears after an idle beat, or when a cross-link "lures" you here
 *   revealed→ the creature's silhouette settles into the scene (the world fills as you explore)
 * Accessibility: it's a real <button> (tab + Enter), and "reveal all spots" outlines it.
 */
export default function Hotspot(props: {
  spot: HotspotData;
  creature?: Creature;
  index: number;
  found: () => boolean;
  revealAll: () => boolean;
  lured: () => boolean;
  onActivate: (spot: HotspotData) => void;
}) {
  const [hinting, setHinting] = createSignal(false);

  onMount(() => {
    if (props.spot.hint === 'none') return;
    // stagger the idle cues so the scene "wakes up" gradually, not all at once
    const delay = 3500 + props.index * 1600;
    const t = setTimeout(() => setHinting(true), delay);
    onCleanup(() => clearTimeout(t));
  });

  const r = props.spot.region;
  const style = `left:${r.x}%;top:${r.y}%;width:${r.w}%;height:${r.h}%`;

  const label = () =>
    props.found() && props.creature
      ? props.creature.name
      : 'Something is hidden here — look closer';

  return (
    <button
      class="rf-hotspot"
      classList={{
        'is-found': props.found(),
        'is-outlined': !props.found() && props.revealAll(),
        'is-hinting': !props.found() && hinting(),
        'is-lured': !props.found() && props.lured(),
      }}
      style={style}
      aria-label={label()}
      onClick={() => props.onActivate(props.spot)}
    >
      <Show when={props.found() && props.creature}>
        <svg
          class="rf-silhouette"
          viewBox="0 0 100 100"
          aria-hidden="true"
          style={`color:${props.creature!.color}`}
          innerHTML={props.creature!.silhouette}
        />
      </Show>
      <Show when={!props.found()}>
        <span class="rf-hint" aria-hidden="true" />
      </Show>
    </button>
  );
}
