// Shared image lightbox. Tap any [data-zoomable] image to view it full-screen in the page's
// native <dialog id="lightbox"> (free focus trap + Esc-to-close). Backdrop click or the ✕
// closes it; clicking the image itself does not. The <dialog> markup + localized labels live
// in each app's Layout.astro; only this behavior is shared. See base.css for the styles.
export function initLightbox() {
  const lb = document.getElementById('lightbox');
  if (!lb || typeof lb.showModal !== 'function') return;
  const img = lb.querySelector('.lightbox__img');
  document.addEventListener('click', (e) => {
    const z = e.target.closest('[data-zoomable]');
    if (!z) return;
    const im = z.tagName === 'IMG' ? z : z.querySelector('img');
    if (!im) return;
    e.preventDefault();
    img.src = im.currentSrc || im.src;
    img.alt = im.alt || '';
    lb.showModal();
  });
  lb.addEventListener('click', (e) => {
    if (e.target === lb || e.target.closest('[data-lightbox-close]')) lb.close();
  });
  lb.addEventListener('close', () => { img.removeAttribute('src'); });
}
