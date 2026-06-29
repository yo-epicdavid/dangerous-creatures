// Build-time data access. Reads the existing web/data/*.json (produced by the Python
// pipeline) so the toolchain stays unchanged. cwd is the project root during `astro build`.
import fs from 'node:fs';
import path from 'node:path';

const DATA = path.resolve('web/data');

export const readJSON = (name) => JSON.parse(fs.readFileSync(path.join(DATA, name), 'utf8'));

export const listAnimals = () =>
  fs.readdirSync(DATA)
    .filter((f) => f.endsWith('.json'))
    .map((f) => JSON.parse(fs.readFileSync(path.join(DATA, f), 'utf8')))
    .filter((d) => d && d.classic && d.id)
    .sort((a, b) => a.name.localeCompare(b.name));

// media + data are copied to dist root; reference them absolutely
export const asset = (p) => (!p ? p : p.startsWith('/') ? p : '/' + p);

export const catSlug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
