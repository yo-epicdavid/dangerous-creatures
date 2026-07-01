/// <reference types="node" />
// Capacitor wrap for the native shells (iOS / Android / Amazon Fire). Not part of the web build —
// this file is only read by the Capacitor CLI. Native scaffolding is a follow-up step:
//   pnpm add -D @capacitor/cli && pnpm add @capacitor/core @capacitor/haptics \
//              @capacitor/preferences @capacitor/share @capacitor/status-bar @capacitor/splash-screen
//   npx cap init && npx cap add ios && npx cap add android
// Then `pnpm build && pnpm cap:sync`. See CREATURIA.md §5½.
import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.epicdavid.creaturia',
  appName: 'Creaturia',
  webDir: 'dist',
  // Kids-store compliance: no analytics/tracking plugins. Keep it offline + local-only.
};

export default config;
