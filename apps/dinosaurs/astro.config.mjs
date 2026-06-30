import { defineConfig } from 'astro/config';

// Static site. Topic pages are pre-rendered from web/data/*.json at build time;
// media (web/assets) and data are copied into dist/ by the build script.
export default defineConfig({
  site: 'https://dinosaurs.pages.dev',
  // Bilingual: English at the root, Castilian Spanish under /es/. The Spanish edition is an
  // unofficial AI FAN TRANSLATION (no Spanish disc ever existed) — es data reuses the English
  // media and only the text is translated.
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es'],
    routing: { prefixDefaultLocale: false },
  },
});
