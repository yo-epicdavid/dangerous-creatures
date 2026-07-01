import { createEffect, onCleanup } from 'solid-js';
import type { Guide } from './scenegraph';

/** An explorer guide's intro card — name, one-line invitation, and a "Start the expedition"
 * button. STUB for now: starting the expedition simply travels into the guide's habitat; the
 * narrated hand-held tour (CREATURIA.md §3) is a follow-up. */
export default function GuideCard(props: {
  guide: Guide;
  onStart: (habitat: string) => void;
  onClose: () => void;
}) {
  // Esc closes; focus the card so keyboard explorers land somewhere sensible (as RevealCard does).
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
    <div class="rf-scrim" role="dialog" aria-modal="true" aria-label={props.guide.name} onClick={props.onClose}>
      <div class="rf-card" ref={card} tabindex="-1" onClick={(e) => e.stopPropagation()}>
        <button class="rf-close" aria-label="Close" onClick={props.onClose}>×</button>

        <svg
          class="rf-card__art rf-card__art--guide"
          viewBox="0 0 100 100"
          aria-hidden="true"
          style={`--c:${props.guide.color}`}
          innerHTML={props.guide.portrait}
        />

        <div class="rf-kicker">An explorer awaits</div>
        <h2 class="rf-card__name">{props.guide.name}</h2>
        <p class="rf-card__tag">{props.guide.years} · {props.guide.tagline}</p>
        <p class="rf-card__fact">“{props.guide.invite}”</p>

        <div class="rf-card__actions">
          <button class="rf-onward" onClick={() => props.onStart(props.guide.habitat)}>
            Start the expedition
          </button>
          <button class="rf-btn" onClick={props.onClose}>Maybe later</button>
        </div>
      </div>
    </div>
  );
}
