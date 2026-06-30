import { defineConfig } from 'astro/config';

// Static site. Topic pages are pre-rendered from web/data/*.json at build time;
// media (web/assets) and data are copied into dist/ by the build script.
export default defineConfig({
  // The Cloudflare Pages project is "oceans-2s9" — oceans.pages.dev is a dead domain (522),
  // so absolute URLs (og:image, twitter:image) must use the real host or social previews break.
  site: 'https://oceans-2s9.pages.dev',
});
