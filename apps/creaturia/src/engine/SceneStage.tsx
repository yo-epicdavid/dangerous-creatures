import { For, Show } from 'solid-js';
import Hotspot from './Hotspot';
import MapRegion, { GuideMarker } from './MapRegion';
import type { Hotspot as HotspotData, Scene, SceneGraph } from './scenegraph';

/** The landscape-locked stage: a 16:9 scene with its hotspots laid over it. Creature hotspots are
 * hidden (you hunt); `place`/`guide` markers are visible (a map is for reading). */
export default function SceneStage(props: {
  scene: Scene;
  graph: SceneGraph;
  isFound: (creatureId: string) => boolean;
  revealAll: () => boolean;
  luredId: () => string | null;
  nudgedId: () => string | null;
  onActivate: (spot: HotspotData) => void;
}) {
  return (
    <div class="rf-stagewrap">
      <div class="rf-stage" style={`background:${props.scene.bg}`} role="group" aria-label={props.scene.name}>
        <Show when={props.scene.backdrop}>
          {(art) => (
            <svg class="rf-backdrop" viewBox="0 0 160 90" aria-hidden="true" innerHTML={art()} />
          )}
        </Show>
        <For each={props.scene.hotspots}>
          {(spot, i) => {
            if (spot.reveal === 'place') {
              return (
                <MapRegion
                  spot={spot}
                  nudged={() => props.nudgedId() === spot.id}
                  revealAll={props.revealAll}
                  onActivate={props.onActivate}
                />
              );
            }
            if (spot.reveal === 'guide') {
              return <GuideMarker spot={spot} revealAll={props.revealAll} onActivate={props.onActivate} />;
            }
            const creature = spot.creatureId ? props.graph.creatures[spot.creatureId] : undefined;
            return (
              <Hotspot
                spot={spot}
                creature={creature}
                index={i()}
                found={() => (spot.creatureId ? props.isFound(spot.creatureId) : false)}
                revealAll={props.revealAll}
                lured={() => !!spot.creatureId && props.luredId() === spot.creatureId}
                onActivate={props.onActivate}
              />
            );
          }}
        </For>
      </div>
    </div>
  );
}
