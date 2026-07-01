import { For } from 'solid-js';
import type { Creature } from './scenegraph';
import type { Journal as JournalStore } from './state';

/** The Field Journal rail — fills as you discover. Locked entries show as grey silhouettes, never
 * blanks (mystery, not shame). Progress is gentle: a count, not a nag. */
export default function Journal(props: { creatures: Creature[]; journal: JournalStore }) {
  return (
    <div class="rf-journal">
      <span class="rf-journal__label">
        Field Journal · {props.journal.foundCount()} of {props.journal.total}
      </span>
      <div class="rf-slots">
        <For each={props.creatures}>
          {(c) => {
            const found = () => props.journal.isFound(c.id);
            return (
              <div
                class="rf-slot"
                classList={{ 'is-found': found() }}
                style={found() ? `--c:${c.color}` : ''}
                title={found() ? c.name : 'Not yet discovered'}
                aria-label={found() ? `${c.name} — discovered` : 'Undiscovered creature'}
              >
                <svg viewBox="0 0 100 100" aria-hidden="true" innerHTML={c.silhouette} />
              </div>
            );
          }}
        </For>
      </div>
    </div>
  );
}
