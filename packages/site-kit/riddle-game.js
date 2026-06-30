// Shared "riddle" game — Oceans *Sea Riddles* and Dinosaurs *Dino Riddles*. Show a clue with the
// answer's name blanked out, pick it from four options, track score + streak. The only difference
// between the two editions is the feedback sound: Oceans plays committed mp3 SFX (<audio
// id="sfxRight"/"sfxWrong"> in the markup), Dinosaurs synthesizes a quick WebAudio beep (its build
// ships no SFX files). Pass sound: 'sfx' or 'beep' (default). Game data ({ pool, STR }) comes from
// the page; the markup (#riddle/#options/#reveal/#next/#score/#streak) lives in each GamesView.
export function initRiddleGame({ pool = [], STR = {}, sound = 'beep' } = {}) {
  const POOL = pool;
  const $ = (id) => document.getElementById(id);
  if (!$('options') || !POOL.length) return;
  let score = 0, streak = 0, answered = false, cur = null, actx = null;
  const shuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  function beep(ok) {
    try {
      actx = actx || new (window.AudioContext || window.webkitAudioContext)();
      const t = actx.currentTime;
      const tone = (freq, start, dur) => {
        const o = actx.createOscillator(), g = actx.createGain();
        o.connect(g); g.connect(actx.destination); o.type = 'sine'; o.frequency.value = freq;
        g.gain.setValueAtTime(0.0001, t + start);
        g.gain.exponentialRampToValueAtTime(0.2, t + start + 0.01);
        g.gain.exponentialRampToValueAtTime(0.0001, t + start + dur);
        o.start(t + start); o.stop(t + start + dur + 0.02);
      };
      if (ok) { tone(660, 0, 0.16); tone(880, 0.12, 0.2); }
      else { tone(180, 0, 0.32); }
    } catch (e) {}
  }
  function playSfx(ok) {
    const el = $(ok ? 'sfxRight' : 'sfxWrong');
    if (el) { el.currentTime = 0; el.play().catch(() => {}); }
  }
  const feedback = sound === 'sfx' ? playSfx : beep;

  function newRound() {
    answered = false;
    $('reveal').hidden = true;
    cur = POOL[Math.floor(Math.random() * POOL.length)];
    $('riddle').textContent = '“' + cur.clue + '”';
    const others = shuffle(POOL.filter((p) => p.id !== cur.id)).slice(0, 3);
    const opts = shuffle([cur, ...others]);
    const box = $('options');
    box.innerHTML = '';
    for (const o of opts) {
      const b = document.createElement('button');
      b.className = 'opt';
      b.textContent = o.name;
      b.addEventListener('click', () => choose(o, opts));
      box.append(b);
    }
  }
  function choose(o, opts) {
    if (answered) return;
    answered = true;
    const correct = o.id === cur.id;
    document.querySelectorAll('.opt').forEach((b, i) => {
      if (opts[i].id === cur.id) b.classList.add('correct');
      else if (opts[i].id === o.id) b.classList.add('wrong');
      b.disabled = true;
    });
    feedback(correct);
    if (correct) { score++; streak++; } else { streak = 0; }
    $('score').textContent = STR.score + score;
    $('streak').textContent = STR.streak + streak;
    $('revealImg').src = cur.thumb;
    $('revealImg').alt = cur.name;
    $('revealName').innerHTML = (correct ? STR.yes : STR.was).replace('%N%', cur.name);
    $('reveal').hidden = false;
  }
  $('next').addEventListener('click', newRound);
  newRound();
}
