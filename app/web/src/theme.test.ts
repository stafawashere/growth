import { readFileSync } from "node:fs";
import { resolve } from "node:path";

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { THEMES, THEME_CHOICE_KEY, applyTheme, chooseTheme, followThemeChoice, readThemeChoice, watchSystemTheme } from "./theme";

const REPO_ROOT = resolve(process.cwd(), "..", "..");

const TOKENS_SOURCE = readFileSync(resolve(REPO_ROOT, "app/design/tokens.py"), "utf8");

const CSS_SOURCE = readFileSync(resolve(REPO_ROOT, "app/design/css.py"), "utf8");

function themeNamesFromTokensSource(): string[] {
   const match = TOKENS_SOURCE.match(/^THEMES\s*=\s*\(([^)]*)\)/m);

   if (match === null) {
      throw new Error("app/design/tokens.py has no THEMES tuple to read theme names from");
   }

   const quoted = match[1].match(/"([^"]+)"/g) ?? [];

   return quoted.map((token) => token.slice(1, -1));
}

function emitsDataThemeSelectorFromThemes(): boolean {
   const importsThemes = /from app\.design\.tokens import[^\n]*\bTHEMES\b/.test(CSS_SOURCE);

   const buildsSelectorFromTheme = /\[data-theme="\{0\}"\]'\.format\(theme\)/.test(CSS_SOURCE);

   return importsThemes && buildsSelectorFromTheme;
}

describe("the theme names theme.ts can write", () => {
   it("are exactly the theme names app/design/css.py emits selectors for", () => {
      expect(
         emitsDataThemeSelectorFromThemes(),
         "app/design/css.py no longer builds [data-theme] selectors from app/design/tokens.py's THEMES"
      ).toBe(true);

      const sourceThemeNames = themeNamesFromTokensSource();

      expect(sourceThemeNames.length).toBeGreaterThan(0);
      expect([...THEMES].sort()).toEqual([...sourceThemeNames].sort());
   });
});

describe("applyTheme", () => {
   it("sets data-theme on the given element", () => {
      const root = document.createElement("html");

      applyTheme("dark", root);

      expect(root.getAttribute("data-theme")).toBe("dark");

      applyTheme("light", root);

      expect(root.getAttribute("data-theme")).toBe("light");
   });
});

describe("watchSystemTheme", () => {
   let listeners: Array<(event: MediaQueryListEvent) => void>;
   let currentMatches: boolean;

   function stubMatchMedia() {
      listeners = [];

      const matchMedia = (query: string) => {
         return {
            get matches() {
               return currentMatches;
            },
            media: query,
            onchange: null,
            addListener: () => undefined,
            removeListener: () => undefined,
            addEventListener: (_type: string, listener: (event: MediaQueryListEvent) => void) => {
               listeners.push(listener);
            },
            removeEventListener: (_type: string, listener: (event: MediaQueryListEvent) => void) => {
               listeners = listeners.filter((candidate) => candidate !== listener);
            },
            dispatchEvent: () => false
         } as unknown as MediaQueryList;
      };

      vi.stubGlobal("matchMedia", matchMedia);
      window.matchMedia = matchMedia;
   }

   beforeEach(() => {
      currentMatches = false;
      stubMatchMedia();
   });

   afterEach(() => {
      vi.unstubAllGlobals();
   });

   it("sets the attribute to each value the media query reports, and follows it on change", () => {
      const root = document.createElement("html");

      currentMatches = false;

      const stop = watchSystemTheme(root);

      expect(root.getAttribute("data-theme")).toBe("light");

      currentMatches = true;

      for (const listener of listeners) {
         listener({ matches: true } as MediaQueryListEvent);
      }

      expect(root.getAttribute("data-theme")).toBe("dark");

      currentMatches = false;

      for (const listener of listeners) {
         listener({ matches: false } as MediaQueryListEvent);
      }

      expect(root.getAttribute("data-theme")).toBe("light");

      stop();

      expect(listeners.length).toBe(0);
   });
});

describe("the theme choice", () => {
   let systemIsDark: boolean;
   let systemListeners: Array<(event: MediaQueryListEvent) => void>;

   beforeEach(() => {
      systemIsDark = false;
      systemListeners = [];
      window.localStorage.clear();
      window.matchMedia = ((query: string) =>
         ({
            get matches() {
               return systemIsDark;
            },
            media: query,
            addEventListener: (_type: string, listener: (event: MediaQueryListEvent) => void) => systemListeners.push(listener),
            removeEventListener: (_type: string, listener: (event: MediaQueryListEvent) => void) => {
               systemListeners = systemListeners.filter((candidate) => candidate !== listener);
            }
         }) as unknown as MediaQueryList) as typeof window.matchMedia;
   });

   afterEach(() => {
      vi.restoreAllMocks();
      followThemeChoice("system", document.createElement("html"));
      window.localStorage.clear();
   });

   function systemTurns(dark: boolean) {
      systemIsDark = dark;

      for (const listener of [...systemListeners]) {
         listener({ matches: dark } as MediaQueryListEvent);
      }
   }

   it("is System until one is chosen, and System follows the operating system", () => {
      const root = document.createElement("html");

      expect(readThemeChoice()).toBe("system");

      followThemeChoice(readThemeChoice(), root);
      expect(root.getAttribute("data-theme")).toBe("light");

      systemTurns(true);
      expect(root.getAttribute("data-theme")).toBe("dark");
   });

   it("applies Light or Dark at once, keeps it over the system's changes, and remembers it", () => {
      const root = document.createElement("html");

      followThemeChoice("system", root);
      chooseTheme("dark", root);

      expect(root.getAttribute("data-theme")).toBe("dark");
      expect(readThemeChoice()).toBe("dark");

      systemTurns(false);
      expect(root.getAttribute("data-theme")).toBe("dark");

      chooseTheme("light", root);
      systemTurns(true);
      expect(root.getAttribute("data-theme")).toBe("light");

      chooseTheme("system", root);
      expect(root.getAttribute("data-theme")).toBe("dark");
      expect(readThemeChoice()).toBe("system");
   });

   it("falls back to System when storage refuses a read or holds an unknown value, and still applies a choice it cannot save", () => {
      const root = document.createElement("html");

      window.localStorage.setItem(THEME_CHOICE_KEY, "sepia");
      expect(readThemeChoice()).toBe("system");

      vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
         throw new Error("storage refused");
      });
      vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
         throw new Error("storage refused");
      });

      expect(readThemeChoice()).toBe("system");
      expect(() => chooseTheme("dark", root)).not.toThrow();
      expect(root.getAttribute("data-theme")).toBe("dark");
   });
});
