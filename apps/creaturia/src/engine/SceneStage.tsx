import { For } from 'solid-js';
import Hotspot from './Hotspot';
import type { Hotspot as HotspotData, Scene, SceneGraph } from './scenegraph';

/** The landscape-locked stage: a 16:9 scene with its hidden hotspots laid over it. */
export default function SceneStage(props: {
  scene: Scene;
  graph: SceneGraph;
  isFound: (creatureId: string) => boolean;
  revealAll: () => boolean;
  luredId: () => string | null;
  onActivate: (spot: HotspotData) => void;
}) {
  return (
    <div class="rf-stagewrap">
      <div class="rf-stage" style={`background:${props.scene.bg}`} role="group" aria-label={props.scene.name}>
        <For each={props.scene.hotspots}>
          {(spot, i) => {
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
