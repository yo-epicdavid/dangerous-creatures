#!/usr/bin/env python3
"""Generate the liberate-all workflow script from the extraction manifest."""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.abspath(os.path.join(HERE, "..", "web", "extracted-manifest.json"))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "web", "assets"))
OUT = os.environ.get("WF_OUT", os.path.join(HERE, "wf_liberate.js"))

m = json.load(open(MANIFEST))
animals = []
for slug, info in sorted(m.items()):
    stems = info["screens"]
    def p(stem):
        return os.path.join(ASSETS, slug, stem + ".png")
    main = next((p(s) for s in stems if s.endswith("00AA")), None)
    pus = [p(s) for s in stems if "PU" in s]
    fbs = [p(s) for s in stems if "FB" in s]
    tv = next((p(s) for s in stems if s.endswith("TV")), None)
    if not main:
        print(f"  skip {slug}: no 00AA screen")
        continue
    animals.append({"id": slug, "code": info["code"], "main": main, "pus": pus, "fbs": fbs, "tv": tv})

TEMPLATE = r'''export const meta = {
  name: 'liberate-dangerous-creatures',
  description: 'Transcribe all 66 Dangerous Creatures animals from screen art into consistent JSON',
  phases: [
    { title: 'Liberate', detail: "read each animal's screens -> data model (Sonnet vision)" },
    { title: 'Verify', detail: 'adversarial re-read & correct (Sonnet)' },
    { title: 'Consistency', detail: 'cross-animal normalization (Opus)' }
  ]
}

const ANIMALS = __ANIMALS__;

const CAP = { type: 'array', items: { type: 'object', required: ['label','text'], properties: { label: { type: 'string' }, text: { type: 'string' } } } };
const SCHEMA = {
  type: 'object',
  required: ['id','code','name','scientificName','tagline','intro','facts','topics','video','hotspots'],
  properties: {
    id: { type: 'string' }, code: { type: 'string' }, name: { type: 'string' },
    scientificName: { type: 'string' }, tagline: { type: 'string' }, intro: { type: 'string' },
    facts: { type: 'array', items: { type: 'object', required: ['label','value','danger'], properties: { label: { type: 'string' }, value: { type: 'string' }, danger: { type: 'boolean' } } } },
    topics: { type: 'array', items: { type: 'object', required: ['id','title','screen','text'], properties: { id: { type: 'string' }, title: { type: 'string' }, screen: { type: 'string' }, text: { type: 'string' }, captions: CAP } } },
    video: { type: 'object', required: ['title','screen','caption'], properties: { title: { type: 'string' }, screen: { type: 'string' }, caption: { type: 'string' } } },
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

function libPrompt(a) {
  const screens = [
    `MAIN article screen (creature title + intro paragraph + RED hotspot labels around the photo): ${a.main}`,
    ...a.pus.map((x, i) => `Sub-topic screen ${i + 1} (title + body text; maybe captioned insets): ${x}`),
    ...a.fbs.map((x, i) => `Fact-box screen ${i + 1} (kill method, prey, danger note, size, region): ${x}`),
    ...(a.tv ? [`Video still (the MAIN screen has a red film-icon label naming this video): ${a.tv}`] : [])
  ].join('\n');
  return `You are rebuilding the 1994 CD-ROM "Microsoft Dangerous Creatures" as a modern web app. Each screen is an image with text baked in. Read EVERY image below with the Read tool (Read renders images visually), then transcribe into JSON.

Screens:
${screens}

Output ONLY a JSON object (no prose, no markdown fences) for id "${a.id}", code "${a.code}", with this exact shape:
{ "id","code","name","scientificName","tagline","intro","facts":[{"label","value","danger"}],"topics":[{"id","title","screen","text","captions":[{"label","text"}]}],"video":{"title","screen","caption"},"hotspots":[{"label","to","x","y","w","h"}] }

Rules:
- Transcribe intro, topic text, and fact values VERBATIM (exact wording, numbers, units). Do not paraphrase.
- name = the common name from the main screen title. scientificName = genus species from your knowledge; append " (unverified)" if unsure.
- tagline = one short, vivid, kid-friendly hook you write in the spirit of the content.
- facts: use these labels in this order when present: "How it kills", "Favorite meals", "Watch out" (danger:true), "Size", "Where it lives". Omit any whose info is genuinely absent. Only the warning fact gets danger:true.
- topics: one per sub-topic (PU) screen, in screen order. id = kebab-case of the title. screen = the PU stem (e.g. "${a.code}01PU"). captions: include ONLY real labeled inset photos; every caption MUST have a non-empty "label" AND non-empty "text" (if an inset has a single line, write a short label and put the sentence in text).
- video.title = the red video label text on the main screen; video.screen = the TV stem.
- hotspots: one per RED label on the MAIN screen. "to" = the topic id it matches, or "video" for the film label, or "facts" for the top-left creature-head Facts icon. x,y = top-left corner as % of the main image (0-100); w,h = size as %. Be reasonably accurate to where the red text sits.
Your ENTIRE final message must be the JSON object.`;
}

function verifyPrompt(a, draft) {
  const screens = [
    `MAIN: ${a.main}`,
    ...a.pus.map((x, i) => `PU${i + 1}: ${x}`),
    ...a.fbs.map((x, i) => `FB${i + 1}: ${x}`),
    ...(a.tv ? [`TV: ${a.tv}`] : [])
  ].join('\n');
  return `Quality-check a draft extraction from "Microsoft Dangerous Creatures". Re-read the source screens with the Read tool and return a CORRECTED full JSON (same schema). Fix transcription errors, fill missing fields, ensure intro/topic/fact text is VERBATIM, ensure every caption has a non-empty label AND text, ensure hotspots map to the right targets and sit on their labels, ensure facts use the standard labels with the danger flag only on the warning fact.

Source screens:
${screens}

Draft JSON to correct:
${JSON.stringify(draft)}

Output ONLY the corrected JSON object (same shape). Keep correct content; change only what is wrong or missing.`;
}

function consPrompt(summary) {
  return `You are the consistency editor for a kids' wildlife web app rebuilt from "Dangerous Creatures". Below are summaries of all ${summary.length} animals (id, name, scientificName, tagline, fact labels, topic titles).

${JSON.stringify(summary, null, 1)}

Return ONLY JSON: { "canonicalFactLabels": [the standard ordered set of fact labels every animal should use], "patches": [ {"id","field","value"} ], "notes": "short summary of issues found" }.
Rules:
- canonicalFactLabels: the consistent vocabulary, e.g. ["How it kills","Favorite meals","Watch out","Size","Where it lives"].
- patches: ONLY for fields "tagline", "name", or "scientificName" where an entry is inconsistent in voice, duplicated, or clearly wrong. value = the corrected string. Keep patches minimal and high-confidence.
- In notes, flag any duplicate names or contradictory scientific names.`;
}

phase('Liberate');
log(`Liberating ${ANIMALS.length} animals (Sonnet vision OCR) + adversarial verify, pipelined...`);
const results = await pipeline(ANIMALS,
  a => agent(libPrompt(a), { label: `lib:${a.id}`, phase: 'Liberate', schema: SCHEMA, model: 'sonnet' }),
  (draft, a) => {
    if (!draft) return null;
    return agent(verifyPrompt(a, draft), { label: `ver:${a.id}`, phase: 'Verify', schema: SCHEMA, model: 'sonnet' })
      .then(v => v || draft);
  }
);
const animalsData = results.filter(Boolean);
log(`Liberated + verified ${animalsData.length}/${ANIMALS.length} animals.`);

phase('Consistency');
const summary = animalsData.map(d => ({ id: d.id, name: d.name, scientificName: d.scientificName, tagline: d.tagline, factLabels: (d.facts || []).map(f => f.label), topicTitles: (d.topics || []).map(t => t.title) }));
let consistency = null;
try {
  consistency = await agent(consPrompt(summary), { label: 'consistency', phase: 'Consistency', schema: CONS_SCHEMA, model: 'opus' });
} catch (e) {
  log('consistency pass failed: ' + e);
}

return { count: animalsData.length, animals: animalsData, consistency };
'''

with open(OUT, "w") as f:
    f.write(TEMPLATE.replace("__ANIMALS__", json.dumps(animals, indent=0)))
print(f"wrote {OUT}  ({len(animals)} animals)")
