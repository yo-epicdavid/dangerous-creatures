// @ts-check
import { defineConfig } from 'astro/config';
import solid from '@astrojs/solid-js';

// Astro is the static shell; the interactive "world" is a single Solid client:only island
// (see CREATURIA.md §5). Capacitor later wraps whatever `dist/` emits — no config needed here.
export default defineConfig({
  integrations: [solid()],
  // static output (default). Same posture as the museum apps: build → copy media into dist.
});
