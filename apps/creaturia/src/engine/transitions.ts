// transitions.ts — buttery scene-to-scene morphs via the View Transitions API, with graceful
// fallbacks: no API support, or the explorer prefers reduced motion → just run the update.
// See CREATURIA.md §5 ("the View Transitions API gives buttery screen-to-screen morphs").

function prefersReducedMotion(): boolean {
  return typeof matchMedia !== 'undefined' && matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/** Run a DOM-mutating update inside a view transition when we safely can. */
export function withTransition(update: () => void): void {
  const doc = document as Document & {
    startViewTransition?: (cb: () => void) => unknown;
  };
  if (typeof doc.startViewTransition === 'function' && !prefersReducedMotion()) {
    doc.startViewTransition(update);
  } else {
    update();
  }
}
