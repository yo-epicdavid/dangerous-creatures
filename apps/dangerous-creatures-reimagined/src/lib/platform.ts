// platform.ts — the thin seam between the web build and its native (Capacitor) shells.
//
// The Reimagined edition is ONE offline-capable web app that ALSO ships native on iOS, Android, and
// Amazon Fire via Capacitor. Everything platform-specific lives behind this module: the engine calls
// these helpers and they "just work" — Capacitor plugins when running natively, plain web APIs in the
// browser. Nothing else in the app should import a Capacitor plugin directly.
//
// SKETCH / contract, not final. The native wiring is marked TODO(native) and imported LAZILY so the
// web build never hard-depends on Capacitor. When the native shell is scaffolded, install the plugins
// and fill in the TODOs:
//   npm i @capacitor/core @capacitor/haptics @capacitor/preferences @capacitor/share
// See REIMAGINED.md §5½ (Platforms & packaging).

export type PlatformName = 'web' | 'ios' | 'android';

// Capacitor injects `window.Capacitor` inside native shells — detect it without importing Capacitor,
// so the web bundle carries no native dependency.
function cap(): any | null {
  return (typeof window !== 'undefined' && (window as any).Capacitor) || null;
}

/** True only inside a Capacitor native shell (iOS/Android/Fire); false on the web/PWA. */
export const isNative: boolean = !!cap()?.isNativePlatform?.();

/** 'ios' | 'android' natively (Fire reports 'android'); 'web' in the browser. */
export const platform: PlatformName = (cap()?.getPlatform?.() as PlatformName) ?? 'web';

/** Light tactile feedback on a discovery/reveal. No-op where unsupported (e.g. iOS Safari). */
export const haptics = {
  async tap(): Promise<void> {
    if (isNative) {
      // TODO(native): const { Haptics, ImpactStyle } = await import('@capacitor/haptics');
      //               await Haptics.impact({ style: ImpactStyle.Light });
      return;
    }
    navigator.vibrate?.(10); // Web Vibration API (Android browsers); iOS ignores it — fine.
  },
};

/** Persisted explorer state — the Field Journal, settings, progress. JSON in, JSON out. */
export const storage = {
  async get<T>(key: string): Promise<T | null> {
    if (isNative) {
      // TODO(native): const { Preferences } = await import('@capacitor/preferences');
      //               const { value } = await Preferences.get({ key });
      //               return value ? (JSON.parse(value) as T) : null;
    }
    try {
      const v = localStorage.getItem(key);
      return v ? (JSON.parse(v) as T) : null;
    } catch {
      return null;
    }
  },
  async set<T>(key: string, value: T): Promise<void> {
    const json = JSON.stringify(value);
    if (isNative) {
      // TODO(native): const { Preferences } = await import('@capacitor/preferences');
      //               await Preferences.set({ key, value: json });
      return;
    }
    try {
      localStorage.setItem(key, json);
    } catch {
      /* quota/full — ignore for the slice */
    }
  },
};

/**
 * Safe-area insets (notch, home indicator) for JS layout math. CSS should prefer
 * `env(safe-area-inset-*)` directly; mirror those onto CSS vars in global CSS so this can read them:
 *   :root { --sai-top: env(safe-area-inset-top); --sai-right: env(safe-area-inset-right);
 *           --sai-bottom: env(safe-area-inset-bottom); --sai-left: env(safe-area-inset-left); }
 */
export function safeAreaInsets(): { top: number; right: number; bottom: number; left: number } {
  const read = (name: string) =>
    parseInt(getComputedStyle(document.documentElement).getPropertyValue(name), 10) || 0;
  return {
    top: read('--sai-top'),
    right: read('--sai-right'),
    bottom: read('--sai-bottom'),
    left: read('--sai-left'),
  };
}

/** Tiny audio helper (ambient / SFX / narration). Swap for Web Audio if you need mixing/low latency. */
export function playSound(src: string, { volume = 1 }: { volume?: number } = {}): HTMLAudioElement | null {
  if (typeof Audio === 'undefined') return null;
  const a = new Audio(src);
  a.volume = volume;
  a.play().catch(() => {}); // autoplay policies: first sound must follow a user gesture
  return a;
}

/** Share a discovery (optional; parent-gate any outbound action for kids-store compliance). */
export async function share(data: { title?: string; text?: string; url?: string }): Promise<void> {
  if (isNative) {
    // TODO(native): const { Share } = await import('@capacitor/share'); await Share.share(data);
    return;
  }
  if (navigator.share) {
    try {
      await navigator.share(data);
    } catch {
      /* user cancelled */
    }
  }
}
