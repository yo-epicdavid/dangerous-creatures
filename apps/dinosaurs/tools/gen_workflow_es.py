#!/usr/bin/env python3
"""Generate the Castilian-Spanish Dinosaurs TRANSLATION workflow.

UNLIKE the DC/Oceans editions, no Spanish Dinosaurs disc ever existed — so this is an
unofficial AI FAN TRANSLATION of the English text, not a restoration. The media stays English.
Each agent reads an English data file (web/data/<id>.json) and returns the Spanish text fields,
keeping ids exact for merging by build_data_es.py. Set WF_ONLY="albe,tyra,aftr,arch,ammo".
"""
import os, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "web", "data"))
OUT = os.environ.get("WF_OUT", os.path.join(HERE, "wf_translate_es.js"))
ONLY = [s.strip() for s in os.environ.get("WF_ONLY", "").split(",") if s.strip()]

SKIP = {"index.json", "browse.json", "quiz.json", "credits.json", "guides.json"}
entries = []
for f in sorted(glob.glob(os.path.join(DATA, "*.json"))):
    if os.path.basename(f) in SKIP:
        continue
    d = json.load(open(f))
    if not (isinstance(d, dict) and d.get("id")):
        continue
    if ONLY and d["id"] not in ONLY:
        continue
    entries.append({"id": d["id"], "path": f})

TEMPLATE = r'''export const meta = {
  name: 'translate-dinosaurs-es',
  description: 'AI fan-translate the English Microsoft Dinosaurs entries into Castilian Spanish',
  phases: [
    { title: 'Translate', detail: "read each English entry -> Spanish text (Sonnet)" },
    { title: 'Consistency', detail: 'cross-entry Spanish normalization (Opus)' }
  ]
}

const ENTRIES = __ENTRIES__;

const CAP = { type: 'array', items: { type: 'object', required: ['label','text'], properties: { label: { type: 'string' }, text: { type: 'string' } } } };
const SCHEMA = {
  type: 'object',
  required: ['id','name','tagline','intro','facts','topics'],
  properties: {
    id: { type: 'string' }, name: { type: 'string' }, meaning: { type: 'string' },
    tagline: { type: 'string' }, intro: { type: 'string' },
    facts: { type: 'array', items: { type: 'object', required: ['label','value'], properties: { label: { type: 'string' }, value: { type: 'string' } } } },
    topics: { type: 'array', items: { type: 'object', required: ['id','title','text'], properties: { id: { type: 'string' }, title: { type: 'string' }, text: { type: 'string' }, captions: CAP } } },
    video: { type: 'object', required: ['title','caption'], properties: { title: { type: 'string' }, caption: { type: 'string' } } }
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

function transPrompt(e) {
  return `Traduce al CASTELLANO (español de España) esta entrada del CD-ROM «Microsoft Dinosaurs» (1993) para una web infantil. Es una TRADUCCIÓN NO OFICIAL hecha por aficionados — el CD original solo se publicó en inglés, así que NO es contenido de un disco español.

Lee el archivo JSON en inglés con la herramienta Read: ${e.path}

Devuelve SOLO un objeto JSON (sin prosa ni fences) con la traducción al español, conservando los "id" EXACTOS:
{ "id":"${e.id}","name","meaning","tagline","intro","facts":[{"label","value"}],"topics":[{"id","title","text","captions":[{"label","text"}]}],"video":{"title","caption"} }

Reglas:
- Traduce con naturalidad y rigor científico, para niños, en español de España. No añadas ni omitas información; traduce lo que dice el texto.
- name: para dinosaurios y animales conocidos usa la forma española habitual (p. ej. "Tyrannosaurus"→"Tiranosaurio", "Allosaurus"→"Alosaurio", "Triceratops"→"Triceratops", "Stegosaurus"→"Estegosaurio"); para géneros poco comunes, conserva el nombre científico tal cual. Para conceptos y temas generales, traduce por completo (p. ej. "Life After Dinosaurs"→"La vida después de los dinosaurios").
- meaning: traduce el significado del nombre (p. ej. "Alberta lizard"→"lagarto de Alberta"). Si no hay, omite el campo.
- facts: traduce "label" y "value". Usa etiquetas coherentes en español (p. ej. "Place"→"Lugar","Size"→"Tamaño","Period"→"Época","Diet"→"Dieta","Weight"→"Peso","Length"→"Longitud").
- topics: conserva el "id" en inglés EXACTO de cada tema; traduce "title" y "text". captions: traduce "label" y "text" (no vacíos); si un tema no tiene captions, omítelas.
- video: traduce "title" y "caption" SOLO si existen en el original.
Tu mensaje final debe ser ÚNICAMENTE el objeto JSON.`;
}

function consPrompt(summary) {
  return `Eres el editor de consistencia de una web infantil en castellano traducida de «Microsoft Dinosaurs». Abajo van los resúmenes de las ${summary.length} entradas (id, name, etiquetas de datos, títulos de temas).

${JSON.stringify(summary, null, 1)}

Devuelve SOLO JSON: { "canonicalFactLabels": [el conjunto estándar y ordenado de etiquetas de datos en español], "patches": [ {"id","field","value"} ], "notes": "resumen breve" }.
Reglas:
- canonicalFactLabels: el vocabulario consistente en español, p. ej. ["Significado","Época","Dieta","Tamaño","Peso","Lugar","Cómo se dice"].
- patches: SOLO para "name" o "tagline" cuando una entrada sea incoherente, duplicada o claramente errónea. value = el texto corregido (en español). Mínimos y de alta confianza.
- En notes, señala nombres incoherentes (p. ej. mezclar "Tiranosaurio" y "Tyrannosaurus").`;
}

phase('Translate');
log(`Fan-translating ${ENTRIES.length} Dinosaurs entries into Castilian Spanish (Sonnet)...`);
const results = await pipeline(ENTRIES,
  e => agent(transPrompt(e), { label: `tr:${e.id}`, phase: 'Translate', schema: SCHEMA, model: 'sonnet' })
);
const entriesData = results.filter(Boolean);
log(`Translated ${entriesData.length}/${ENTRIES.length} entries.`);

phase('Consistency');
const summary = entriesData.map(d => ({ id: d.id, name: d.name, factLabels: (d.facts || []).map(f => f.label), topicTitles: (d.topics || []).map(t => t.title) }));
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
