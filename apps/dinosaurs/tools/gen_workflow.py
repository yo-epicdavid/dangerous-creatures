#!/usr/bin/env python3
"""Generate the Dinosaurs liberation workflow from the extraction manifest.

Set WF_ONLY="tyra,allo,apat,arch,extn" to liberate only a pilot subset.
Writes wf_liberate.js (run with the Workflow tool; save result to web/wf_result.json).
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.abspath(os.path.join(HERE, "..", "web", "extracted-manifest.json"))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "web", "assets"))
OUT = os.environ.get("WF_OUT", os.path.join(HERE, "wf_liberate.js"))
ONLY = [s.strip() for s in os.environ.get("WF_ONLY", "").split(",") if s.strip()]

m = json.load(open(MANIFEST))
entries = []
for slug, info in sorted(m.items()):
    if ONLY and slug not in ONLY:
        continue
    stems = info["screens"]
    def p(stem):
        return os.path.join(ASSETS, slug, stem + ".png")
    main = next((p(s) for s in stems if s.endswith("00AA")), None)
    pus = [p(s) for s in stems if "PU" in s]
    fb = next((p(s) for s in stems if "FB" in s), None)
    if not main:
        print(f"  skip {slug}: no 00AA")
        continue
    entries.append({"id": slug, "code": info["code"], "main": main, "pus": pus, "fb": fb})

TEMPLATE = r'''export const meta = {
  name: 'liberate-dinosaurs',
  description: 'Transcribe Microsoft Dinosaurs (1993) entries from screen art into consistent JSON',
  phases: [
    { title: 'Liberate', detail: "read each entry's screens -> data model (Sonnet vision)" },
    { title: 'Verify', detail: 'adversarial re-read & correct (Sonnet)' },
    { title: 'Consistency', detail: 'cross-entry normalization (Opus)' }
  ]
}

const ENTRIES = __ENTRIES__;

const CAP = { type: 'array', items: { type: 'object', required: ['label','text'], properties: { label: { type: 'string' }, text: { type: 'string' } } } };
const SCHEMA = {
  type: 'object',
  required: ['id','code','name','category','scientificName','pronunciation','meaning','period','diet','tagline','intro','facts','topics','crosslinks','hotspots'],
  properties: {
    id: { type: 'string' }, code: { type: 'string' }, name: { type: 'string' },
    category: { type: 'string', enum: ['dinosaur','creature','concept'] },
    scientificName: { type: 'string' }, pronunciation: { type: 'string' }, meaning: { type: 'string' },
    period: { type: 'string' }, diet: { type: 'string', enum: ['Carnivore','Herbivore','Omnivore',''] },
    tagline: { type: 'string' }, intro: { type: 'string' },
    facts: { type: 'array', items: { type: 'object', required: ['label','value'], properties: { label: { type: 'string' }, value: { type: 'string' } } } },
    topics: { type: 'array', items: { type: 'object', required: ['id','title','screen','text'], properties: { id: { type: 'string' }, title: { type: 'string' }, screen: { type: 'string' }, text: { type: 'string' }, captions: CAP } } },
    crosslinks: { type: 'array', items: { type: 'object', required: ['label'], properties: { label: { type: 'string' }, to: { type: 'string' } } } },
    hotspots: { type: 'array', items: { type: 'object', required: ['label','to','x','y','w','h'], properties: { label: { type: 'string' }, to: { type: 'string' }, x: { type: 'number' }, y: { type: 'number' }, w: { type: 'number' }, h: { type: 'number' } } } }
  }
};
const CONS_SCHEMA = {
  type: 'object',
  required: ['canonicalFactLabels','patches','notes'],
  properties: {
    canonicalFactLabels: { type: 'array', items: { type: 'string' } },
    patches: { type: 'array', items: { type: 'object', required: ['id','field','value'], properties: { id: { type: 'string' }, field: { type: 'string' }, value: { type: 'string' } } } },
    notes: { type: 'string' }
  }
};

function libPrompt(e) {
  const screens = [
    `MAIN screen (big title + a speaker/pronunciation icon + intro paragraph + ORANGE hotspot labels around the art; maybe a boxed cross-link like "Record Breakers"): ${e.main}`,
    ...e.pus.map((x, i) => `Sub-topic screen ${i + 1} (title + body text; maybe captioned insets): ${x}`),
    ...(e.fb ? [`FACT BOX screen (a "fast facts" panel: name meaning, pronunciation, when it lived / period, length, weight, diet, where found, discovered by): ${e.fb}`] : [])
  ].join('\n');
  return `You are rebuilding the 1993 CD-ROM "Microsoft Dinosaurs" as a modern kids' web app. Each screen is an image with text baked in. Read EVERY image below with the Read tool (Read renders images visually), then transcribe into JSON.

Screens:
${screens}

Output ONLY a JSON object (no prose, no fences) for id "${e.id}", code "${e.code}", with this exact shape:
{ "id","code","name","category","scientificName","pronunciation","meaning","period","diet","tagline","intro","facts":[{"label","value"}],"topics":[{"id","title","screen","text","captions":[{"label","text"}]}],"crosslinks":[{"label","to"}],"hotspots":[{"label","to","x","y","w","h"}] }

Rules:
- Transcribe intro, topic text, and fact values VERBATIM (exact wording, numbers, units). Do not paraphrase.
- name = the title on the main screen. category = "dinosaur" (a true dinosaur), "creature" (another prehistoric animal — pterosaur, marine reptile, ammonite, early mammal, etc.), or "concept" (a topic/idea — extinction, fossils, warm-blooded, the periods, armor, discovery, etc.).
- scientificName = the genus (italicized form) for dinosaurs/creatures; "" for concepts. pronunciation = the phonetic spelling shown on the fact box, or write one from the name (e.g. "tie-RAN-uh-SOR-us"). meaning = what the name means (often in the intro or fact box, e.g. "tyrant lizard king"); "" if none.
- period = when it lived (e.g. "Late Cretaceous", "Jurassic"); "" for concepts. diet = one of "Carnivore","Herbivore","Omnivore", or "" if not an animal / unknown.
- tagline = one short, vivid, kid-friendly hook you write in the spirit of the content.
- facts: the fast-facts from the FACT BOX (and key specifics from the text) as {label,value}: e.g. "Length","Weight","Period","Diet","Meaning","Discovered","Found in". Do not invent numbers.
- topics: one per sub-topic screen, in order. id = kebab-case of the title. screen = the sub-topic stem (e.g. "${e.code}01PU"). captions: ONLY real labeled inset photos; every caption MUST have non-empty "label" AND "text".
- crosslinks: boxed links to OTHER entries (e.g. "Record Breakers"). label = visible text; to = best-guess kebab-case id (omit "to" if unknown).
- hotspots: one per ORANGE label on the MAIN screen. "to" = the topic id it matches, or "facts" for the fact-box icon. x,y = top-left as % of the main image (0-100); w,h = size as %.
Your ENTIRE final message must be the JSON object.`;
}

function verifyPrompt(e, draft) {
  const screens = [
    `MAIN: ${e.main}`,
    ...e.pus.map((x, i) => `PU${i + 1}: ${x}`),
    ...(e.fb ? [`FB: ${e.fb}`] : [])
  ].join('\n');
  return `Quality-check a draft extraction from "Microsoft Dinosaurs" (1993). Re-read the source screens with the Read tool and return a CORRECTED full JSON (same schema). Fix transcription errors, fill missing fields, ensure intro/topic/fact text is VERBATIM, ensure the category/period/diet are right, ensure every caption has non-empty label AND text, ensure hotspots map to the right targets, ensure facts come from the fact box (no invented numbers).

Source screens:
${screens}

Draft JSON to correct:
${JSON.stringify(draft)}

Output ONLY the corrected JSON object (same shape). Keep correct content; change only what is wrong or missing.`;
}

function consPrompt(summary) {
  return `You are the consistency editor for a kids' dinosaur web app rebuilt from "Microsoft Dinosaurs". Below are summaries of all ${summary.length} entries (id, name, category, period, diet, fact labels, topic titles).

${JSON.stringify(summary, null, 1)}

Return ONLY JSON: { "canonicalFactLabels": [the standard ordered set of fact labels entries should prefer], "patches": [ {"id","field","value"} ], "notes": "short summary of issues found" }.
Rules:
- canonicalFactLabels: a small consistent vocabulary, e.g. ["Meaning","Pronunciation","Period","Length","Weight","Diet","Found in","Discovered"].
- patches: ONLY for fields "tagline","name","category","period", or "diet" where an entry is inconsistent, duplicated, or clearly wrong. value = the corrected string. Keep patches minimal and high-confidence.
- In notes, flag duplicate names, contradictory periods, or likely miscategorizations.`;
}

phase('Liberate');
log(`Liberating ${ENTRIES.length} Dinosaurs entries (Sonnet vision OCR) + adversarial verify, pipelined...`);
const results = await pipeline(ENTRIES,
  e => agent(libPrompt(e), { label: `lib:${e.id}`, phase: 'Liberate', schema: SCHEMA, model: 'sonnet' }),
  (draft, e) => {
    if (!draft) return null;
    return agent(verifyPrompt(e, draft), { label: `ver:${e.id}`, phase: 'Verify', schema: SCHEMA, model: 'sonnet' })
      .then(v => v || draft);
  }
);
const entriesData = results.filter(Boolean);
log(`Liberated + verified ${entriesData.length}/${ENTRIES.length} entries.`);

phase('Consistency');
const summary = entriesData.map(d => ({ id: d.id, name: d.name, category: d.category, period: d.period, diet: d.diet, factLabels: (d.facts || []).map(f => f.label), topicTitles: (d.topics || []).map(t => t.title) }));
let consistency = null;
try {
  consistency = await agent(consPrompt(summary), { label: 'consistency', phase: 'Consistency', schema: CONS_SCHEMA, model: 'opus' });
} catch (err) {
  log('consistency pass failed: ' + err);
}

return { count: entriesData.length, entries: entriesData, consistency };
'''

with open(OUT, "w") as f:
    f.write(TEMPLATE.replace("__ENTRIES__", json.dumps(entries, indent=0)))
print(f"wrote {OUT}  ({len(entries)} entries{' [pilot: '+','.join(ONLY)+']' if ONLY else ''})")
