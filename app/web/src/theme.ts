const DARK_SCHEME_QUERY = "(prefers-color-scheme: dark)";

const THEME_ATTRIBUTE = "data-theme";

/* app/design/tokens.py's THEMES tuple is the source of these two names, and app/design/css.py
   emits colour tokens only under a [data-theme="light"] or [data-theme="dark"] selector built
   from that tuple. 08-design-brief.md names a theme setting under accessibility; stage 11 builds
   it as System, Light and Dark, with System, following the operating system, the default. */

export const THEMES = ["light", "dark"] as const;

export type Theme = (typeof THEMES)[number];

function themeForMatches(matches: boolean): Theme {
   return matches ? "dark" : "light";
}

export function applyTheme(theme: Theme, root: HTMLElement = document.documentElement): void {
   root.setAttribute(THEME_ATTRIBUTE, theme);
}

export function watchSystemTheme(root: HTMLElement = document.documentElement): () => void {
   const media = window.matchMedia(DARK_SCHEME_QUERY);

   applyTheme(themeForMatches(media.matches), root);

   const listener = (event: MediaQueryListEvent) => {
      applyTheme(themeForMatches(event.matches), root);
   };

   media.addEventListener("change", listener);

   return () => {
      media.removeEventListener("change", listener);
   };
}


export const THEME_CHOICES = ["system", "light", "dark"] as const;

export type ThemeChoice = (typeof THEME_CHOICES)[number];

export const THEME_CHOICE_KEY = "growth-theme";

/* The choice lives in this browser's storage, which can be missing, full or refused outright, so
   every read and write is guarded and a choice that cannot be read is System. */
export function readThemeChoice(): ThemeChoice {
   try {
      const stored = window.localStorage.getItem(THEME_CHOICE_KEY);
      const isKnown = THEME_CHOICES.some((choice) => choice === stored);

      return isKnown ? (stored as ThemeChoice) : "system";
   } catch {
      return "system";
   }
}

function saveThemeChoice(choice: ThemeChoice) {
   try {
      window.localStorage.setItem(THEME_CHOICE_KEY, choice);
   } catch {
      return;
   }
}

let stopFollowing: () => void = () => undefined;

export function followThemeChoice(choice: ThemeChoice, root: HTMLElement = document.documentElement): void {
   stopFollowing();

   if (choice === "system") {
      stopFollowing = watchSystemTheme(root);

      return;
   }

   stopFollowing = () => undefined;
   applyTheme(choice, root);
}

/* Applies at once, with no reload, and is remembered for the next visit. */
export function chooseTheme(choice: ThemeChoice, root: HTMLElement = document.documentElement): void {
   saveThemeChoice(choice);
   followThemeChoice(choice, root);
}