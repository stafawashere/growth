import { readFileSync } from "node:fs";
import { resolve } from "node:path";

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { THEMES, applyTheme, watchSystemTheme } from "./theme";

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
