/* Dangerous Creatures — reborn. One data model, two front-ends: Modern + Classic 1994. */
const params = new URLSearchParams(location.search);
const id = params.get("id") || "lion";
const MODE_KEY = "dc-mode";

let DATA = null;
let mode = params.get("mode") || localStorage.getItem(MODE_KEY) || "modern";

const el = (tag, props = {}, ...kids) => {
  const node = Object.assign(document.createElement(tag), props);
  for (const k of kids) node.append(k);
  return node;
};

const catSlug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const chipLink = (label, tab) =>
  el("a", { className: `chip ${tab === "weapons" ? "weapon" : "region"}`, href: `browse.html?tab=${tab}#${catSlug(label)}`, textContent: label });

async function main() {
  const app = document.getElementById("app");
  try {
    const res = await fetch(`data/${id}.json`);
    if (!res.ok) throw new Error(res.status);
    DATA = await res.json();
  } catch (err) {
    app.innerHTML = `<p class="loading">Couldn't load “${id}”. Run a local server (see README) and try again.</p>`;
    return;
  }
  document.title = `${DATA.name} — Dangerous Creatures`;
  setupChrome();
  applyMode();
}

function setupChrome() {
  document.querySelectorAll("#modeswitch button").forEach((b) =>
    b.addEventListener("click", () => setMode(b.dataset.mode))
  );
  wireNarration(DATA);
}

function setMode(m) {
  mode = m;
  localStorage.setItem(MODE_KEY, m);
  applyMode();
}

function applyMode() {
  if (mode === "classic" && !DATA.classic) mode = "modern";
  document.body.dataset.mode = mode;
  document.querySelectorAll("#modeswitch button").forEach((b) =>
    b.classList.toggle("is-active", b.dataset.mode === mode)
  );
  const app = document.getElementById("app");
  app.classList.toggle("wrap", mode === "modern");
  if (mode === "classic") renderClassic(app, DATA);
  else renderModern(app, DATA);
  scrollTo({ top: 0 });
}

/* ============================ MODERN ============================ */
function renderModern(app, d) {
  app.innerHTML = "";

  const hero = el("section", { className: "hero" });
  const media = el("div", { className: "hero__media" });
  media.append(el("img", { src: d.hero.image, alt: d.hero.alt || d.name, loading: "eager" }));
  const title = el("hgroup", { className: "hero__title" });
  title.append(el("div", { className: "name", textContent: d.name }));
  if (d.scientificName) title.append(el("div", { className: "sci", textContent: d.scientificName }));
  media.append(title);
  hero.append(media);
  app.append(hero);

  app.append(el("p", { className: "tagline", textContent: d.tagline || "" }));

  if (d.weapons?.length || d.habitats?.length || d.regions?.length) {
    const chips = el("div", { className: "chips" });
    if (d.weapons?.length) {
      chips.append(el("span", { className: "chips__label", textContent: "Weapons" }));
      for (const w of d.weapons) chips.append(chipLink(w, "weapons"));
    }
    if (d.habitats?.length) {
      chips.append(el("span", { className: "chips__label", textContent: "Habitat" }));
      for (const h of d.habitats) chips.append(chipLink(h, "habitats"));
    }
    if (d.regions?.length) {
      chips.append(el("span", { className: "chips__label", textContent: "Found in" }));
      for (const r of d.regions) chips.append(chipLink(r, "regions"));
    }
    app.append(chips);
  }

  const layout = el("div", { className: "layout" });
  const intro = el("div", { className: "intro" });
  intro.append(el("p", { className: "lead", textContent: d.intro }));
  layout.append(intro);

  const card = el("aside", { className: "factcard" });
  card.append(el("h2", { textContent: "Field notes" }));
  const dl = el("dl");
  const facts = Array.isArray(d.facts)
    ? d.facts
    : Object.entries(d.facts || {}).map(([label, value]) => ({ label, value, danger: /beastly|danger|cannibal/i.test(label + value) }));
  for (const f of facts) {
    const group = el("div", f.danger ? { className: "danger" } : {});
    group.append(el("dt", { textContent: f.label }), el("dd", { textContent: f.value }));
    dl.append(group);
  }
  card.append(dl);
  layout.append(card);
  app.append(layout);

  if (d.topics?.length) {
    app.append(el("h2", { className: "section-head", textContent: "Get closer" }));
    const wrap = el("div", { className: "topics" });
    for (const t of d.topics) wrap.append(renderTopic(t));
    app.append(wrap);
  }

  if (d.video) {
    const vb = el("section", { className: "videoblock" });
    const v = el("video", { controls: true, playsInline: true, poster: d.video.poster || "" });
    v.append(el("source", { src: d.video.src, type: "video/mp4" }));
    vb.append(v);
    vb.append(el("p", { className: "cap" }, el("b", { textContent: d.video.title + " — " }), d.video.caption || ""));
    app.append(el("h2", { className: "section-head", textContent: "Watch" }));
    app.append(vb);
  }

  if (d._provenance) {
    const p = el("p", { className: "prov" });
    p.append(el("b", { textContent: "Source: " }), d._provenance.source + ". ", d._provenance.note || " ");
    p.append(document.createTextNode(" "), el("a", { href: "credits.html", textContent: "Credits & Acknowledgements →" }));
    app.append(p);
  }
}

function renderTopic(t) {
  const topic = el("article", { className: "topic" });
  const media = el("div", { className: "topic__media" });
  media.append(el("img", { src: t.image, alt: t.title, loading: "lazy" }));
  const body = el("div", { className: "topic__body" });
  body.append(el("h3", { textContent: t.title }), el("p", { textContent: t.text }));
  if (t.captions?.length) {
    const caps = el("div", { className: "topic__captions" });
    for (const c of t.captions) {
      const cap = el("div", { className: "cap" });
      cap.append(el("b", { textContent: c.label }), document.createTextNode(c.text));
      caps.append(cap);
    }
    body.append(caps);
  }
  topic.append(media, body);
  return topic;
}

/* ============================ CLASSIC 1994 ============================ */
function renderClassic(app, d) {
  app.innerHTML = "";
  const c = d.classic;
  const root = el("div", { className: "classic" });

  const bar = el("div", { className: "classic__bar" });
  bar.append(el("div", { className: "classic__title", textContent: `${d.name} — original 1994 screens` }));
  const reveal = el("button", { className: "btn", textContent: "Show clickable spots" });
  bar.append(reveal);
  root.append(bar);

  const stage = el("div", { className: "classic__stage" });
  root.append(stage);
  app.append(root);

  reveal.addEventListener("click", () => {
    const on = stage.classList.toggle("reveal");
    reveal.textContent = on ? "Hide clickable spots" : "Show clickable spots";
  });
  if (params.get("spots") === "1") { stage.classList.add("reveal"); reveal.textContent = "Hide clickable spots"; }

  const history = [];

  function show(key) {
    const sc = c.screens[key];
    if (!sc) return;
    stage.innerHTML = "";

    if (sc.video) {
      const v = el("video", { className: "classic__screen", controls: true, autoplay: true, playsInline: true, poster: sc.poster || "" });
      v.append(el("source", { src: sc.video, type: "video/mp4" }));
      stage.append(v);
    } else {
      const frame = el("div", { className: "classic__frame" });
      frame.append(el("img", { className: "classic__screen", src: sc.image, alt: `${d.name} — ${key}` }));
      for (const h of sc.hotspots || []) {
        const b = el("button", { className: "hotspot", title: h.label, ariaLabel: h.label });
        Object.assign(b.style, { left: h.x + "%", top: h.y + "%", width: h.w + "%", height: h.h + "%" });
        if (h.disabled) b.classList.add("hotspot--disabled");
        if (h.external || h.link) b.classList.add("hotspot--link");
        b.append(el("span", { className: "hotspot__tip", textContent: h.label + (h.external || h.link ? " →" : "") }));
        b.addEventListener("click", () => {
          if (h.link) { location.href = h.link; return; }
          if (h.external) { location.href = h.external + "&mode=classic"; return; }
          if (h.disabled) return;
          if (h.to) { history.push(key); show(h.to); }
        });
        frame.append(b);
      }
      stage.append(frame);
    }

    if (key !== c.start) {
      const back = el("button", { className: "classic__back btn", textContent: "‹ Back" });
      back.addEventListener("click", () => show(history.pop() || c.start));
      stage.append(back);
    }
  }

  show(c.start);
}

/* ============================ shared ============================ */
function wireNarration(d) {
  if (!d.narration) return;
  const btn = document.getElementById("narrate");
  const audio = document.getElementById("narration");
  audio.src = d.narration;
  btn.hidden = false;
  btn.addEventListener("click", () => { if (audio.paused) audio.play(); else audio.pause(); });
  const reset = () => { btn.textContent = "▶ Listen to the story"; btn.classList.remove("is-playing"); };
  audio.addEventListener("play", () => { btn.textContent = "❚❚ Pause"; btn.classList.add("is-playing"); });
  audio.addEventListener("pause", reset);
  audio.addEventListener("ended", reset);
}

main();
