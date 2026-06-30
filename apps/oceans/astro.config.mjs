import { defineConfig } from 'astro/config';

// Static site. Topic pages are pre-rendered from web/data/*.json at build time;
// media (web/assets) and data are copied into dist/ by the build script.
export default defineConfig({
  // The Cloudflare Pages project is "oceans-2s9" — oceans.pages.dev is a dead domain (522),
  // so absolute URLs (og:image, twitter:image) must use the real host or social previews break.
  site: 'https://oceans-2s9.pages.dev',
  // Bilingual: English at the root, Castilian Spanish under /es/ (web/data/es/*.json +
  // web/assets/es/). The /es/ route files reuse the same view components as the English routes.
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es'],
    routing: { prefixDefaultLocale: false },
  },
});
