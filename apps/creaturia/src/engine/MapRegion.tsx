import { Show } from 'solid-js';
import type { Hotspot as HotspotData } from './scenegraph';

/**
 * A habitat region on the world map. Unlike scene hotspots (hidden — you hunt for them), map
 * markers are VISIBLE: a map is for reading. Enterable regions travel in; locked ones are
 * "coming soon" teasers — an intriguing silhouette whose tap earns a gentle nudge, never a dead
 * click. Accessibility: a real <button> either way (keyboard users get the same nudge), and the
 * "Reveal spots" toggle outlines the enterable ones.
 */
export default function MapRegion(props: {
  spot: HotspotData;
  nudged: () => boolean;
  revealAll: () => boolean;
  onActivate: (spot: HotspotData) => void;
}) {
  const r = props.spot.region;
  return (
    <button
      class="rf-region"
      classList={{
        'is-locked': !!props.spot.locked,
        'is-outlined': !props.spot.locked && props.revealAll(),
        'is-nudged': props.nudged(),
      }}
      style={`left:${r.x}%;top:${r.y}%;width:${r.w}%;height:${r.h}%`}
      aria-label={
        props.spot.locked
          ? `${props.spot.label} — still uncharted, coming soon`
          : `${props.spot.label} — travel in`
      }
      onClick={() => props.onActivate(props.spot)}
    >
      <svg
        class="rf-region__art"
        viewBox="0 0 100 100"
        aria-hidden="true"
        style={`color:${props.spot.color ?? 'currentColor'}`}
        innerHTML={props.spot.art ?? ''}
      />
      <span class="rf-region__name">{props.spot.label}</span>
      <span class="rf-region__state">{props.spot.locked ? '🔒 Coming soon' : 'Travel in'}</span>
      <Show when={props.nudged()}>
        <span class="rf-nudge" role="status">Still uncharted — coming soon!</span>
      </Show>
    </button>
  );
}

/** An explorer guide's map pin — a small round portrait. Tap → the guide's intro card. */
export function GuideMarker(props: {
  spot: HotspotData;
  revealAll: () => boolean;
  onActivate: (spot: HotspotData) => void;
}) {
  const r = props.spot.region;
  return (
    <button
      class="rf-guidepin"
      classList={{ 'is-outlined': props.revealAll() }}
      style={`left:${r.x}%;top:${r.y}%;width:${r.w}%;height:${r.h}%`}
      aria-label={`Meet ${props.spot.label} — an explorer guide`}
      onClick={() => props.onActivate(props.spot)}
    >
      <svg
        class="rf-guidepin__face"
        viewBox="0 0 100 100"
        aria-hidden="true"
        style={`color:${props.spot.color ?? 'currentColor'}`}
        innerHTML={props.spot.art ?? ''}
      />
      <span class="rf-guidepin__name">{props.spot.label}</span>
    </button>
  );
}
