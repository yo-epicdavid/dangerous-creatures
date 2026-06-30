#!/usr/bin/env python3
"""Generate the Castilian-Spanish Oceans liberation workflow from the es manifest.

Spanish TEXT only — the language-neutral structure (category, scientificName, zones, oceans,
crosslinks, hotspots) is reused from the English data by build_data_es.py, so topics are keyed
by SCREEN for matching. Set WF_ONLY="dolp,shar,cora,tide,divi" for a pilot.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.abspath(os.path.join(HERE, "..", "web", "extracted-manifest-es.json"))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "web", "assets", "es"))
OUT = os.environ.get("WF_OUT", os.path.join(HERE, "wf_liberate_es.js"))
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
    entries.append({"id": slug, "code": info["code"], "main": main, "pus": pus, "pv": pv})

TEMPLATE = r'''export const meta = {
  name: 'liberate-oceans-es',
  description: 'Transcribe the Castilian Spanish "Oceanos de Microsoft" entries into JSON',
  phases: [
    { title: 'Liberate', detail: "read each entry's Spanish screens -> data (Sonnet vision)" },
    { title: 'Verify', detail: 'adversarial re-read & correct (Sonnet)' },
    { title: 'Consistency', detail: 'cross-entry Spanish normalization (Opus)' }
  ]
}

const ENTRIES = __ENTRIES__;

const CAP = { type: 'array', items: { type: 'object', required: ['label','text'], properties: { label: { type: 'string' }, text: { type: 'string' } } } };
const SCHEMA = {
  type: 'object',
  required: ['id','code','name','tagline','intro','facts','topics'],
  properties: {
    id: { type: 'string' }, code: { type: 'string' }, name: { type: 'string' },
    tagline: { type: 'string' }, intro: { type: 'string' },
    facts: { type: 'array', items: { type: 'object', required: ['label','value'], properties: { label: { type: 'string' }, value: { type: 'string' } } } },
    topics: { type: 'array', items: { type: 'object', required: ['screen','title','text'], properties: { screen: { type: 'string' }, title: { type: 'string' }, text: { type: 'string' }, captions: CAP } } },
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

function libPrompt(e) {
  const screens = [
    `Pantalla PRINCIPAL (título + párrafo de introducción + etiquetas de zonas activas NARANJAS alrededor de la foto; quizá un botón "Quiz" y enlaces a otros temas): ${e.main}`,
    ...e.pus.map((x, i) => `Pantalla de subtema ${i + 1} (título + texto; quizá fotos con pie): ${x}`),
    ...(e.pv ? [`Fotograma de VÍDEO (la pantalla principal lleva una etiqueta de película naranja que lo nombra): ${e.pv}`] : [])
  ].join('\n');
  return `Estás reconstruyendo el CD-ROM en CASTELLANO «Océanos de Microsoft» (1995), la versión española de Microsoft Oceans, como una web moderna para niños. Cada pantalla es una imagen con el texto incrustado, EN ESPAÑOL. Lee TODAS las imágenes con la herramienta Read (Read muestra las imágenes) y transcríbelas a JSON.

Pantallas:
${screens}

Devuelve SOLO un objeto JSON (sin prosa ni fences) para id "${e.id}", code "${e.code}", con esta forma exacta:
{ "id","code","name","tagline","intro","facts":[{"label","value"}],"topics":[{"screen","title","text","captions":[{"label","text"}]}],"video":{"title","caption"} }

Reglas:
- Transcribe el intro y el texto de cada subtema LITERALMENTE, en español (palabras, números y unidades exactas). No traduzcas al inglés ni parafrasees.
- name = el título que aparece en la pantalla principal (en español, p. ej. "Tiburón blanco", "Las mareas", "Arrecifes de coral").
- tagline = un gancho breve, vívido y apto para niños que escribes TÚ en español, en el espíritu del contenido.
- facts: de 3 a 6 datos breves y curiosos extraídos del texto (este CD no tiene ficha de datos; destila lo más interesante — tamaño, profundidad, velocidad, dieta, un "¿Sabías que...?"). label = una categoría de 1-3 palabras en español (p. ej. "Tamaño","Profundidad","Dieta","Velocidad","¿Sabías que?"); value = el dato en español. No inventes números que no aparezcan en el contenido.
- topics: uno por cada pantalla de subtema (PU), en orden. screen = el código de la pantalla (p. ej. "${e.code}01PU"). title y text en español. captions: SOLO fotos con etiqueta real; cada caption con "label" y "text" no vacíos.
- video: title = el texto de la etiqueta de película (naranja) de la pantalla principal, en español; caption = una breve descripción del clip en español. Inclúyelo solo si hay un fotograma de vídeo.
Tu mensaje final debe ser ÚNICAMENTE el objeto JSON.`;
}

function verifyPrompt(e, draft) {
  const screens = [`MAIN: ${e.main}`, ...e.pus.map((x, i) => `PU${i + 1}: ${x}`), ...(e.pv ? [`PV: ${e.pv}`] : [])].join('\n');
  return `Revisa una extracción borrador del CD-ROM en castellano «Océanos de Microsoft». Vuelve a leer las pantallas con Read y devuelve un JSON CORREGIDO completo (mismo esquema). Corrige errores de transcripción, rellena lo que falte, asegúrate de que el intro/temas sean LITERALES y EN ESPAÑOL (no inglés), que cada caption tenga "label" y "text" no vacíos, y que los datos estén respaldados por el contenido (sin números inventados).

Pantallas:
${screens}

JSON borrador a corregir:
${JSON.stringify(draft)}

Devuelve SOLO el objeto JSON corregido (mismo formato). Conserva lo correcto; cambia solo lo erróneo o ausente.`;
}

function consPrompt(summary) {
  return `Eres el editor de consistencia de una web infantil en castellano reconstruida de «Océanos de Microsoft». Abajo van los resúmenes de los ${summary.length} temas (id, name, tagline, etiquetas de datos, títulos de subtemas).

${JSON.stringify(summary, null, 1)}

Devuelve SOLO JSON: { "canonicalFactLabels": [el conjunto estándar y ordenado de etiquetas de datos en español], "patches": [ {"id","field","value"} ], "notes": "resumen breve" }.
Reglas:
- canonicalFactLabels: el vocabulario consistente en español, p. ej. ["Tamaño","Profundidad","Dieta","Velocidad","Distribución","¿Sabías que?"].
- patches: SOLO para los campos "tagline" o "name" cuando una entrada sea inconsistente en el tono, duplicada o claramente errónea. value = el texto corregido (en español). Mínimos y de alta confianza.
- En notes, señala nombres duplicados o incoherencias.`;
}

phase('Liberate');
log(`Liberating ${ENTRIES.length} Oceans entries in Castilian Spanish (Sonnet vision OCR) + verify, pipelined...`);
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
const summary = entriesData.map(d => ({ id: d.id, name: d.name, tagline: d.tagline, factLabels: (d.facts || []).map(f => f.label), topicTitles: (d.topics || []).map(t => t.title) }));
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
