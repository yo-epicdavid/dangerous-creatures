// Build-time data access. Reads web/data/*.json (produced by the Python pipeline)
// so the toolchain stays unchanged. cwd is the app root during `astro build`.
//
// Locale-aware: English data lives in web/data/, Castilian Spanish in web/data/es/.
import fs from 'node:fs';
import path from 'node:path';

const DATA = path.resolve('web/data');
const dir = (locale) => (locale === 'es' ? path.join(DATA, 'es') : DATA);

export const readJSON = (name, locale = 'en') =>
  JSON.parse(fs.readFileSync(path.join(dir(locale), name), 'utf8'));

export const listEntries = (locale = 'en') =>
  fs.readdirSync(dir(locale))
    .filter((f) => f.endsWith('.json'))
    .map((f) => JSON.parse(fs.readFileSync(path.join(dir(locale), f), 'utf8')))
    .filter((d) => d && d.classic && d.id)
    .sort((a, b) => a.name.localeCompare(b.name, locale));

// media + data are copied to dist root; reference them absolutely
export const asset = (p) => (!p ? p : p.startsWith('/') ? p : '/' + p);

export const catSlug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

// Localized path: prefix non-default locales (Spanish under /es/). '/' -> '/es/'.
export const lp = (locale, p = '/') =>
  locale === 'es' ? (p === '/' ? '/es/' : '/es' + p) : p;
