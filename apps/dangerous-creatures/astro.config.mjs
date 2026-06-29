import { defineConfig } from 'astro/config';

// Static site. Animal pages are pre-rendered from web/data/*.json at build time;
// media (web/assets) and data are copied into dist/ by the build script.
//
// Bilingual (i18n): English is the default locale and is served at the root (/),
// Castilian Spanish under /es/. Spanish pages read web/data/es/*.json (Spanish text +
// Spanish media) and are emitted by the /es/ route files, which reuse the same view
// components as the English routes. Guided tours, games, credits and the making-of
// remain English-only in this first pass.
export default defineConfig({
  site: 'https://dangerous-creatures.pages.dev',
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es'],
    routing: { prefixDefaultLocale: false },
  },
});
