import { defineConfig } from 'astro/config';

// Static site. Topic pages are pre-rendered from web/data/*.json at build time;
// media (web/assets) and data are copied into dist/ by the build script.
export default defineConfig({
  site: 'https://dinosaurs.pages.dev',
});
