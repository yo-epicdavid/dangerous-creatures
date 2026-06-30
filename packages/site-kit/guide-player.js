// Shared flat guided-tour narration player (Dangerous Creatures + Dinosaurs — one narration list
// per tour). Wires the #play / #prev / #next buttons, the #step label and #prog bar to a single
// <audio id="player-audio">, auto-advancing through the clips. STR carries the localized strings
// the player touches: { stepOf: 'Step %N% of %T%', play, pause }. Markup lives in each GuideView.
// (Oceans' guide player is host-with-three-tours and stays local — different shape.)
export function initGuidePlayer({ narration = [], STR = {} } = {}) {
  const fmt = (s, v) => s.replace(/%(\w+)%/g, (_, k) => v[k]);
  const audio = document.getElementById('player-audio');
  if (!audio) return;
  const playBtn = document.getElementById('play');
  const playGlyph = playBtn.querySelector('.play-glyph');
  const stepLbl = document.getElementById('step');
  const prog = document.getElementById('prog');
  let step = 0;
  function setPlayState(playing) {
    playGlyph.textContent = playing ? '❚❚' : '▶';
    playBtn.setAttribute('aria-label', playing ? STR.pause : STR.play);
    playBtn.setAttribute('aria-pressed', playing ? 'true' : 'false');
  }
  function setStep(i, autoplay) {
    step = Math.max(0, Math.min(i, narration.length - 1));
    audio.src = narration[step];
    stepLbl.textContent = fmt(STR.stepOf, { N: step + 1, T: narration.length });
    prog.value = step + 1;
    if (autoplay) audio.play();
  }
  playBtn.addEventListener('click', () => { audio.paused ? audio.play() : audio.pause(); });
  document.getElementById('prev').addEventListener('click', () => setStep(step - 1, true));
  document.getElementById('next').addEventListener('click', () => setStep(step + 1, true));
  audio.addEventListener('play', () => setPlayState(true));
  audio.addEventListener('pause', () => setPlayState(false));
  audio.addEventListener('ended', () => { if (step < narration.length - 1) setStep(step + 1, true); else setPlayState(false); });
  if (narration.length) setStep(0, false);
}
