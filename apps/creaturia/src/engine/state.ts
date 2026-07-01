// state.ts — the Field Journal: what you've discovered, persisted across sessions.
// Solid store for fine-grained reactivity; persistence goes through src/lib/platform.ts storage
// (localStorage on web, Capacitor Preferences natively) — the engine never touches storage directly.

import { createStore, unwrap } from 'solid-js/store';
import { storage } from '../lib/platform';

const KEY = 'creaturia-journal-v1';

export interface JournalState {
  found: Record<string, { at: number; scene: string }>;
  scenesVisited: string[];
}

export function createJournal(total: number) {
  const [state, setState] = createStore<JournalState>({ found: {}, scenesVisited: [] });

  // Hydrate from storage (async; the store just fills in when it resolves).
  storage.get<JournalState>(KEY).then((saved) => {
    if (saved && saved.found) setState(saved);
  });

  const persist = () => void storage.set(KEY, unwrap(state));

  return {
    state,
    total,
    isFound: (creatureId: string) => !!state.found[creatureId],
    foundCount: () => Object.keys(state.found).length,
    /** Record a discovery. Returns true only the first time (so reveals feel "new" once). */
    record(creatureId: string, scene: string): boolean {
      if (state.found[creatureId]) return false;
      setState('found', creatureId, { at: Date.now(), scene });
      persist();
      return true;
    },
    visit(scene: string) {
      if (state.scenesVisited.includes(scene)) return;
      setState('scenesVisited', (list) => [...list, scene]);
      persist();
    },
    reset() {
      setState({ found: {}, scenesVisited: [] });
      persist();
    },
  };
}

export type Journal = ReturnType<typeof createJournal>;
