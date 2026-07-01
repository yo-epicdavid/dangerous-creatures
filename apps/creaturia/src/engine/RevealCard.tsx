import { createEffect, onCleanup, Show } from 'solid-js';
import type { Creature, RevealKind } from './scenegraph';

const KICKER: Record<RevealKind, string> = {
  creature: 'You found',
  fact: 'Did you know?',
  clip: 'Caught in motion',
  place: 'A new place',
  game: 'A puzzle appears',
  guide: 'An explorer awaits', // guides get their own GuideCard; kept for the exhaustive record
};

/** The reveal payload — the surprise after a tap. Creature art + one earned fact + an onward lure. */
export default function RevealCard(props: {
  creature: Creature;
  kind: RevealKind;
  isNew: boolean;
  onClose: () => void;
  onFollow: (creatureId: string) => void;
}) {
  // Esc closes; focus the card so keyboard explorers land somewhere sensible.
  let card: HTMLDivElement | undefined;
  createEffect(() => {
    card?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') props.onClose();
    };
    window.addEventListener('keydown', onKey);
    onCleanup(() => window.removeEventListener('keydown', onKey));
  });

  return (
    <div class="rf-scrim" role="dialog" aria-modal="true" aria-label={props.creature.name} onClick={props.onClose}>
      <div class="rf-card" ref={card} tabindex="-1" onClick={(e) => e.stopPropagation()}>
        <button class="rf-close" aria-label="Close" onClick={props.onClose}>×</button>

        <svg
          class="rf-card__art"
          classList={{ 'is-clip': props.kind === 'clip' }}
          viewBox="0 0 100 100"
          aria-hidden="true"
          style={`--c:${props.creature.color}`}
          innerHTML={props.creature.silhouette}
        />

        <Show when={props.isNew}>
          <div class="rf-stamp">Spotted!</div>
        </Show>

        <div class="rf-kicker">{KICKER[props.kind]}</div>
        <h2 class="rf-card__name">{props.creature.name}</h2>
        <p class="rf-card__tag">{props.creature.tagline}</p>
        <p class="rf-card__fact">{props.creature.fact}</p>

        <div class="rf-card__actions">
          <Show when={props.creature.onward}>
            <button class="rf-onward" onClick={() => props.onFollow(props.creature.onward!.creatureId)}>
              {props.creature.onward!.label}
            </button>
          </Show>
          <button class="rf-btn" onClick={props.onClose}>Keep exploring</button>
        </div>
      </div>
    </div>
  );
}
