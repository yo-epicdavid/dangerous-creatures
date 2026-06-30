// Shared Browse-page tab switcher (DC region/habitat/weapon · Oceans kind/zone/sea ·
// Dinosaurs kind/period/diet). The tab keys and which panel starts visible are read straight
// from the DOM (#tabs buttons + .tabpanel[data-tab]), so only the localized title strings
// (STR = { docTitle: {tab: label}, suffix }) need to be passed in from the page.
export function initBrowseTabs(STR = {}) {
  const root = document.getElementById('tabs');
  if (!root) return;
  const btns = Array.from(root.querySelectorAll('button'));
  const panels = document.querySelectorAll('.tabpanel');
  const valid = btns.map((b) => b.dataset.tab);
  const def = valid[0];
  const params = new URLSearchParams(location.search);
  let tab = valid.includes(params.get('tab')) ? params.get('tab') : def;

  function setTab(t, scroll) {
    tab = valid.includes(t) ? t : def;
    panels.forEach((p) => (p.hidden = p.dataset.tab !== tab));
    btns.forEach((b) => {
      const active = b.dataset.tab === tab;
      b.classList.toggle('is-active', active);
      b.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    history.replaceState(null, '', `?tab=${tab}${location.hash}`);
    if (STR.docTitle) document.title = STR.docTitle[tab] + ' — ' + STR.suffix;
    if (scroll && location.hash) {
      const el = document.getElementById(location.hash.slice(1));
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }
  }
  btns.forEach((b) => b.addEventListener('click', () => setTab(b.dataset.tab, false)));
  setTab(tab, true);
}
