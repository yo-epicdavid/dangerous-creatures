#!/usr/bin/env python3
"""Generate the Castilian-Spanish DC liberation workflow from the es manifest.

Spanish text only — the language-neutral structure (scientific names, browse categories,
hotspots, video) is reused from the English data by build_data_es.py, so topics are keyed by
SCREEN (not id) for matching. Set WF_ONLY="lion,gwsh,cobr,scor,hipp" for a pilot.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.abspath(os.path.join(HERE, "..", "web", "extracted-manifest-es.json"))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "web", "assets", "es"))
OUT = os.environ.get("WF_OUT", os.path.join(HERE, "wf_liberate_es.js"))
ONLY = [s.strip() for s in os.environ.get("WF_ONLY", "").split(",") if s.strip()]

m = json.load(open(MANIFEST))
animals = []
for slug, info in sorted(m.items()):
    if ONLY and slug not in ONLY:
        continue
    stems = info["screens"]
    def p(stem):
        return os.path.join(ASSETS, slug, stem + ".png")
    main = next((p(s) for s in stems if s.endswith("00AA")), None)
    pus = [p(s) for s in stems if "PU" in s]
    fbs = [p(s) for s in stems if "FB" in s]
    tv = next((p(s) for s in stems if s.endswith("TV")), None)
    if not main:
        print(f"  skip {slug}: no 00AA")
        continue
    animals.append({"id": slug, "code": info["code"], "main": main, "pus": pus, "fbs": fbs, "tv": tv})

TEMPLATE = r'''export const meta = {
  name: 'liberate-dangerous-creatures-es',
  description: 'Transcribe the Castilian Spanish "Animales Peligrosos" screens into JSON',
  phases: [
    { title: 'Liberate', detail: "read each animal's Spanish screens -> data (Sonnet vision)" },
    { title: 'Verify', detail: 'adversarial re-read & correct (Sonnet)' },
    { title: 'Consistency', detail: 'cross-animal Spanish normalization (Opus)' }
  ]
}

const ANIMALS = __ANIMALS__;

const CAP = { type: 'array', items: { type: 'object', required: ['label','text'], properties: { label: { type: 'string' }, text: { type: 'string' } } } };
const SCHEMA = {
  type: 'object',
  required: ['id','code','name','scientificName','tagline','intro','facts','topics'],
  properties: {
    id: { type: 'string' }, code: { type: 'string' }, name: { type: 'string' },
    scientificName: { type: 'string' }, tagline: { type: 'string' }, intro: { type: 'string' },
    facts: { type: 'array', items: { type: 'object', required: ['label','value','danger'], properties: { label: { type: 'string' }, value: { type: 'string' }, danger: { type: 'boolean' } } } },
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

function libPrompt(a) {
  const screens = [
    `Pantalla PRINCIPAL (título del animal + párrafo de introducción + etiquetas de zonas activas en NARANJA/ROJO): ${a.main}`,
    ...a.pus.map((x, i) => `Pantalla de subtema ${i + 1} (título + texto; quizá fotos con pie): ${x}`),
    ...a.fbs.map((x, i) => `Ficha de datos ${i + 1} ("Hechos": cómo mata, presa, advertencia, tamaño, dónde vive): ${x}`),
    ...(a.tv ? [`Fotograma del VÍDEO (la pantalla principal lleva una etiqueta de película naranja/roja que lo nombra): ${a.tv}`] : [])
  ].join('\n');
  return `Estás reconstruyendo el CD-ROM en CASTELLANO "Animales Peligrosos de Microsoft" (la versión española de Dangerous Creatures) como una web moderna. Cada pantalla es una imagen con el texto incrustado, EN ESPAÑOL. Lee TODAS las imágenes con la herramienta Read (Read muestra las imágenes), y transcríbelas a JSON.

Pantallas:
${screens}

Devuelve SOLO un objeto JSON (sin prosa ni fences) para id "${a.id}", code "${a.code}", con esta forma exacta:
{ "id","code","name","scientificName","tagline","intro","facts":[{"label","value","danger"}],"topics":[{"screen","title","text","captions":[{"label","text"}]}],"video":{"title","caption"} }

Reglas:
- Transcribe el intro, el texto de cada subtema y los valores de los datos LITERALMENTE, en español (palabras, números y unidades exactas). No traduzcas al inglés ni parafrasees.
- name = el nombre que aparece en el título de la pantalla principal (en español, p. ej. "León", "Tiburón blanco").
- scientificName = el nombre científico en latín (género especie) según tu conocimiento; añade " (unverified)" si no estás seguro.
- tagline = un gancho breve, vívido y apto para niños que escribes TÚ en español, en el espíritu del contenido.
- facts: los datos de la ficha "Hechos" como {label, value, danger}. Usa etiquetas en español, p. ej.: "Cómo mata", "Comida favorita", "¡Cuidado!", "Tamaño", "Dónde vive". Solo el dato de advertencia/peligro lleva danger:true; el resto danger:false.
- topics: uno por cada pantalla de subtema (PU), en orden. screen = el código de la pantalla (p. ej. "${a.code}01PU"). title y text en español. captions: SOLO fotos con etiqueta real; cada caption con "label" y "text" no vacíos.
- video: title = el texto de la etiqueta de película (naranja/roja) de la pantalla principal, en español; caption = una breve descripción del clip en español (una frase). Inclúyelo solo si hay un fotograma de vídeo.
Tu mensaje final debe ser ÚNICAMENTE el objeto JSON.`;
}

function verifyPrompt(a, draft) {
  const screens = [`MAIN: ${a.main}`, ...a.pus.map((x, i) => `PU${i + 1}: ${x}`), ...a.fbs.map((x, i) => `FB${i + 1}: ${x}`), ...(a.tv ? [`TV: ${a.tv}`] : [])].join('\n');
  return `Revisa una extracción borrador del CD-ROM en castellano "Animales Peligrosos". Vuelve a leer las pantallas con Read y devuelve un JSON CORREGIDO completo (mismo esquema). Corrige errores de transcripción, rellena lo que falte, asegúrate de que el intro/temas/datos sean LITERALES y EN ESPAÑOL (no inglés), que cada caption tenga "label" y "text" no vacíos, y que solo el dato de advertencia lleve danger:true.

Pantallas:
${screens}

JSON borrador a corregir:
${JSON.stringify(draft)}

Devuelve SOLO el objeto JSON corregido (mismo formato). Conserva lo correcto; cambia solo lo erróneo o ausente.`;
}

function consPrompt(summary) {
  return `Eres el editor de consistencia de una web infantil en castellano reconstruida de "Animales Peligrosos". Abajo van los resúmenes de los ${summary.length} animales (id, name, scientificName, tagline, etiquetas de datos, títulos de temas).

${JSON.stringify(summary, null, 1)}

Devuelve SOLO JSON: { "canonicalFactLabels": [el conjunto estándar y ordenado de etiquetas de datos en español], "patches": [ {"id","field","value"} ], "notes": "resumen breve" }.
Reglas:
- canonicalFactLabels: el vocabulario consistente en español, p. ej. ["Cómo mata","Comida favorita","¡Cuidado!","Tamaño","Dónde vive"].
- patches: SOLO para los campos "tagline", "name" o "scientificName" cuando una entrada sea inconsistente en el tono, duplicada o claramente errónea. value = el texto corregido (en español). Mínimos y de alta confianza.
- En notes, señala nombres duplicados o nombres científicos contradictorios.`;
}

phase('Liberate');
log(`Liberating ${ANIMALS.length} animals in Castilian Spanish (Sonnet vision OCR) + verify, pipelined...`);
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
print(f"wrote {OUT}  ({len(animals)} animals{' [pilot: '+','.join(ONLY)+']' if ONLY else ''})")
