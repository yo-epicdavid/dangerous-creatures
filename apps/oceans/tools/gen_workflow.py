#!/usr/bin/env python3
"""Generate the Oceans liberation workflow from the extraction manifest.

Set WF_ONLY="dolp,shar,cora,tide,divi" to liberate only a pilot subset.
Writes wf_liberate.js (run it with the Workflow tool; save result to web/wf_result.json).
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
    pv = next((p(s) for s in stems if "PV" in s), None)
    if not main:
        print(f"  skip {slug}: no 00AA screen")
        continue
    pv_stem = next((s for s in stems if "PV" in s), None)
    entries.append({"id": slug, "code": info["code"], "main": main, "pus": pus,
                    "pv": pv, "pvStem": pv_stem, "hasVideo": bool(info["video"])})

TEMPLATE = r'''export const meta = {
  name: 'liberate-oceans',
  description: 'Transcribe Microsoft Oceans (1995) entries from screen art into consistent JSON',
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
  required: ['id','code','name','category','scientificName','tagline','intro','facts','topics','crosslinks','hotspots'],
  properties: {
    id: { type: 'string' }, code: { type: 'string' }, name: { type: 'string' },
    category: { type: 'string', enum: ['creature','habitat','concept','place','human'] },
    scientificName: { type: 'string' }, tagline: { type: 'string' }, intro: { type: 'string' },
    zones: { type: 'array', items: { type: 'string' } },
    oceans: { type: 'array', items: { type: 'string' } },
    facts: { type: 'array', items: { type: 'object', required: ['label','value'], properties: { label: { type: 'string' }, value: { type: 'string' } } } },
    topics: { type: 'array', items: { type: 'object', required: ['id','title','screen','text'], properties: { id: { type: 'string' }, title: { type: 'string' }, screen: { type: 'string' }, text: { type: 'string' }, captions: CAP } } },
    video: { type: 'object', required: ['title','screen','caption'], properties: { title: { type: 'string' }, screen: { type: 'string' }, caption: { type: 'string' } } },
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
    `MAIN article screen (title + intro paragraph + ORANGE hotspot labels around the photo; maybe a "Quiz" button and boxed cross-links to other topics): ${e.main}`,
    ...e.pus.map((x, i) => `Sub-topic screen ${i + 1} (title + body text; maybe captioned insets): ${x}`),
    ...(e.pv ? [`Video still (the main screen has an orange film label naming this video): ${e.pv}`] : [])
  ].join('\n');
  return `You are rebuilding the 1995 CD-ROM "Microsoft Oceans" as a modern kids' web app. Each screen is an image with text baked in. Read EVERY image below with the Read tool (Read renders images visually), then transcribe into JSON.

Screens:
${screens}

Output ONLY a JSON object (no prose, no fences) for id "${e.id}", code "${e.code}", with this exact shape:
{ "id","code","name","category","scientificName","tagline","intro","zones":[],"oceans":[],"facts":[{"label","value"}],"topics":[{"id","title","screen","text","captions":[{"label","text"}]}],"video":{"title","screen","caption"},"crosslinks":[{"label","to"}],"hotspots":[{"label","to","x","y","w","h"}] }

Rules:
- Transcribe intro and topic text VERBATIM (exact wording, numbers, units). Do not paraphrase.
- name = the title from the main screen. category = one of: "creature" (a living animal), "habitat" (a place sea life lives, e.g. coral reef, kelp forest, tide pool, the abyss), "concept" (an ocean phenomenon, e.g. currents, tides, waves, the water cycle, weather), "place" (a named ocean or region, e.g. the Pacific, the Arctic), "human" (people & the sea, e.g. diving, navigation, oil rigs, pollution, exploration).
- scientificName = genus species ONLY for category "creature" (append " (unverified)" if unsure); "" for everything else.
- tagline = one short, vivid, kid-friendly hook you write in the spirit of the content.
- zones = ocean zones this relates to (subset of: "Coast & tide pools","Coral reef","Kelp & seagrass","Open ocean","Deep sea","Polar seas","Rivers & estuaries"). oceans = named oceans/seas it relates to, or ["Worldwide"]. Best-effort from the content.
- facts: 3 to 6 short kid-friendly key facts drawn from the screens' text (Oceans has no fact box, so distill the most interesting specifics — size, diet, speed, depth, a "Did you know"). label = a 1-3 word category (e.g. "Size","Diet","Speed","Depth","Did you know"); value = the fact. Do not invent numbers not supported by the content.
- topics: one per sub-topic screen, in order. id = kebab-case of the title. screen = the sub-topic stem (e.g. "${e.code}01PU"). captions: ONLY real labeled inset photos; every caption MUST have non-empty "label" AND "text".
- video: include ONLY if a video still is listed above. title = the orange film-label text on the main screen; screen = "${e.pvStem || ''}"; caption = a short description of the clip.
- crosslinks: the boxed links on the main screen that jump to OTHER topics (e.g. "What's a Fish?"). label = the visible text; to = best-guess kebab-case id of the target topic (omit "to" if unknown).
- hotspots: one per ORANGE label on the MAIN screen. "to" = the topic id it matches, "video" for the film label, or "quiz" for the Quiz button. x,y = top-left as % of the main image (0-100); w,h = size as %. Be reasonably accurate to where the label sits.
Your ENTIRE final message must be the JSON object.`;
}

function verifyPrompt(e, draft) {
  const screens = [
    `MAIN: ${e.main}`,
    ...e.pus.map((x, i) => `PU${i + 1}: ${x}`),
    ...(e.pv ? [`PV: ${e.pv}`] : [])
  ].join('\n');
  return `Quality-check a draft extraction from "Microsoft Oceans" (1995). Re-read the source screens with the Read tool and return a CORRECTED full JSON (same schema). Fix transcription errors, fill missing fields, ensure intro/topic text is VERBATIM, ensure the category is right, ensure every caption has non-empty label AND text, ensure hotspots map to the right targets and sit on their orange labels, ensure facts are supported by the content (no invented numbers).

Source screens:
${screens}

Draft JSON to correct:
${JSON.stringify(draft)}

Output ONLY the corrected JSON object (same shape). Keep correct content; change only what is wrong or missing.`;
}

function consPrompt(summary) {
  return `You are the consistency editor for a kids' ocean web app rebuilt from "Microsoft Oceans". Below are summaries of all ${summary.length} entries (id, name, category, scientificName, tagline, fact labels, topic titles).

${JSON.stringify(summary, null, 1)}

Return ONLY JSON: { "canonicalFactLabels": [the standard ordered set of fact labels entries should prefer], "patches": [ {"id","field","value"} ], "notes": "short summary of issues found" }.
Rules:
- canonicalFactLabels: a small consistent vocabulary the facts should prefer, e.g. ["Size","Diet","Speed","Depth","Range","Did you know"].
- patches: ONLY for fields "tagline", "name", "scientificName", or "category" where an entry is inconsistent in voice, duplicated, or clearly miscategorized. value = the corrected string. Keep patches minimal and high-confidence.
- In notes, flag duplicate names, contradictory scientific names, or likely miscategorizations.`;
}

phase('Liberate');
log(`Liberating ${ENTRIES.length} Oceans entries (Sonnet vision OCR) + adversarial verify, pipelined...`);
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
const summary = entriesData.map(d => ({ id: d.id, name: d.name, category: d.category, scientificName: d.scientificName, tagline: d.tagline, factLabels: (d.facts || []).map(f => f.label), topicTitles: (d.topics || []).map(t => t.title) }));
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
