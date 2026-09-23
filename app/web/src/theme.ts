const DARK_SCHEME_QUERY = "(prefers-color-scheme: dark)";

const THEME_ATTRIBUTE = "data-theme";

/* app/design/tokens.py's THEMES tuple is the source of these two names, and app/design/css.py
   emits colour tokens only under a [data-theme="light"] or [data-theme="dark"] selector built
   from that tuple. 08-design-brief.md names a theme setting under accessibility, but P1's
   settings scope does not include it, so following the system preference is an implementer
   choice with no plan sentence picking a default. */

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
