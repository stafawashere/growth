import { readFileSync } from "node:fs";
import { join } from "node:path";

/* Test support for the P8 evals: a small cascade over app.css that resolves, for a rendered
   element, the token each colour property ends at and the non-colour declarations that decide
   what the element looks like once colour is taken away. jsdom matches selectors but neither
   resolves custom properties nor inherits, so the resolution is done here, from the same
   stylesheet the client ships. */

const SOURCE_ROOT = join(__dirname, "..");

const DESIGN_ROOT = join(SOURCE_ROOT, "..", "..", "design");

export const STYLESHEET = readFileSync(join(SOURCE_ROOT, "styles", "app.css"), "utf8");

export const TOKEN_FILE = JSON.parse(readFileSync(join(DESIGN_ROOT, "growth-tokens.json"), "utf8")) as Record<
   string,
   Record<string, string>
>;

export const THEMES = ["light", "dark"];

export interface Rule {
   selector: string;
   specificity: number;
   order: number;
   declarations: Map<string, string>;
}

export const COLOUR_PROPERTIES = [
   "color",
   "background",
   "background-color",
   "border",
   "border-color",
   "border-inline-start",
   "outline",
   "outline-color",
   "fill",
   "stroke",
   "accent-color",
   "box-shadow",
   "text-decoration-color"
];

function specificityOf(selector: string) {
   const withoutNot = selector.replace(/:not\(([^)]*)\)/g, " $1 ");
   const ids = (withoutNot.match(/#[\w-]+/g) ?? []).length;
   const classes = (withoutNot.match(/\.[\w-]+|\[[^\]]*\]|:(?!:)[\w-]+/g) ?? []).length;
   const types = (withoutNot.replace(/\[[^\]]*\]/g, " ").match(/(^|[\s>+~])[a-z][\w-]*/gi) ?? []).length;

   return ids * 10000 + classes * 100 + types;
}

export function parseRules(text: string): Rule[] {
   const rules: Rule[] = [];
   const withoutComments = text.replace(/\/\*[\s\S]*?\*\//g, " ");
   let order = 0;

   for (const block of withoutComments.matchAll(/([^{}]+)\{([^{}]*)\}/g)) {
      const declarations = new Map<string, string>();

      for (const statement of block[2].split(";")) {
         const colon = statement.indexOf(":");

         if (colon > 0) {
            declarations.set(statement.slice(0, colon).trim().toLowerCase(), statement.slice(colon + 1).trim());
         }
      }

      for (const part of block[1].split(",")) {
         const selector = part.trim();

         order += 1;
         rules.push({ selector, specificity: specificityOf(selector), order, declarations });
      }
   }

   return rules;
}

export const RULES = parseRules(STYLESHEET);

/* :focus-visible is read as :focus, since jsdom focuses only through the keyboard paths the tests
   drive. A pseudo-element or :hover rule never matches an element here. */
function jsdomSelector(selector: string) {
   return selector.replace(/:focus-visible/g, ":focus");
}

export function isMatchable(rule: Rule) {
   const isPseudoElement = rule.selector.includes("::");
   const isHover = rule.selector.includes(":hover");

   return !isPseudoElement && !isHover;
}

export function matchingRules(element: Element): Rule[] {
   return RULES.filter((rule) => {
      if (!isMatchable(rule)) {
         return false;
      }

      try {
         return element.matches(jsdomSelector(rule.selector));
      } catch {
         throw new Error(`jsdom cannot match app.css selector ${rule.selector}`);
      }
   }).sort((first, second) => first.specificity - second.specificity || first.order - second.order);
}

/* The winning declaration for one property, inline style above every rule. */
export function declared(element: Element, property: string): string | null {
   const inline = (element as HTMLElement).style?.getPropertyValue(property) ?? "";

   if (inline !== "") {
      return inline.trim();
   }

   let value: string | null = null;

   for (const rule of matchingRules(element)) {
      const found = rule.declarations.get(property);

      if (found !== undefined) {
         value = found;
      }
   }

   return value;
}

export interface Paint {
   token: string;
   alpha: number;
}

const TOKEN_REFERENCE = /var\(--growth-([a-z0-9-]+)\)/;

export function paintOf(value: string): Paint | null | "current" {
   const trimmed = value.trim().toLowerCase();

   if (trimmed === "none" || trimmed === "transparent" || trimmed === "") {
      return null;
   }

   if (trimmed === "currentcolor" || trimmed === "inherit") {
      return "current";
   }

   const reference = TOKEN_REFERENCE.exec(trimmed);

   if (reference === null) {
      throw new Error(`a colour that is no token: ${value}`);
   }

   const halfTransparent = trimmed.startsWith("color-mix(") && trimmed.includes("transparent");

   return { token: reference[1], alpha: halfTransparent ? 0.5 : 1 };
}

/* The colour token a border, outline or background shorthand carries, if any. */
function shorthandPaint(value: string | null): Paint | null {
   if (value === null) {
      return null;
   }

   const reference = /var\(--growth-(?!space-|stroke-|leading-|type-)[a-z0-9-]+\)/.exec(value);

   if (reference === null) {
      return null;
   }

   return paintOf(value.startsWith("color-mix(") ? value : reference[0]) as Paint;
}

export function isSvgElement(element: Element) {
   return element.namespaceURI === "http://www.w3.org/2000/svg";
}

/* color inherits, and so do an SVG element's fill and stroke; a presentation attribute sits
   below every CSS rule. */
export function resolvedColour(element: Element): Paint | null {
   let current: Element | null = element;

   while (current !== null) {
      const value = declared(current, "color");

      if (value !== null) {
         const paint = paintOf(value);

         if (paint !== "current") {
            return paint;
         }
      }

      current = current.parentElement;
   }

   return null;
}

export function resolvedSvgPaint(element: Element, property: "fill" | "stroke"): Paint | null {
   let current: Element | null = element;

   while (current !== null && isSvgElement(current)) {
      const value = declared(current, property) ?? current.getAttribute(property);

      if (value !== null) {
         const paint = paintOf(value);

         return paint === "current" ? resolvedColour(current) : paint;
      }

      current = current.parentElement;
   }

   return property === "fill" ? resolvedColour(element) : null;
}

export function ownBackground(element: Element): Paint | null {
   const value = declared(element, "background-color") ?? declared(element, "background");

   return value === null ? null : shorthandPaint(value);
}

export function effectiveBackground(element: Element | null): Paint {
   let current = element;

   while (current !== null) {
      const background = isSvgElement(current) ? null : ownBackground(current);

      if (background !== null) {
         return background;
      }

      current = current.parentElement;
   }

   return { token: "surface-page", alpha: 1 };
}

export function borderPaint(element: Element): Paint | null {
   for (const property of ["border", "border-color", "border-inline-start", "outline", "outline-color"]) {
      const paint = shorthandPaint(declared(element, property));

      if (paint !== null) {
         return paint;
      }
   }

   return null;
}

export function fontSizeToken(element: Element): string | null {
   let current: Element | null = element;

   while (current !== null) {
      const value = declared(current, "font-size");
      const reference = value === null ? null : /var\(--growth-(type-[a-z-]+)\)/.exec(value);

      if (reference !== null) {
         return reference[1];
      }

      current = current.parentElement;
   }

   return "type-body";
}

/* A declaration that sets a property back to its initial value draws nothing a reader can see, so
   it describes no difference. */
const INITIAL_VALUES: Record<string, string[]> = {
   "text-decoration": ["none"],
   "font-weight": ["normal"],
   "font-style": ["normal"],
   outline: ["none", "0"],
   border: ["none", "0"],
   transform: ["none"],
   opacity: ["1"]
};

/* What stays visible once every colour property is ignored: each matching rule's other
   declarations, with any colour reference cut out of a shorthand such as a border. */
export function colourlessDeclarations(element: Element): string[] {
   const kept = new Map<string, string>();
   const colourOnly = ["color", "background-color", "border-color", "outline-color", "fill", "stroke", "accent-color", "box-shadow", "text-decoration-color", "cursor"];
   const inline = (element as HTMLElement).style;
   const inlineEntries: Array<[string, string]> = [];

   for (let index = 0; index < (inline?.length ?? 0); index += 1) {
      const property = inline[index];

      inlineEntries.push([property, inline.getPropertyValue(property)]);
   }

   const ruleEntries = matchingRules(element).flatMap((rule) => Array.from(rule.declarations.entries()));

   for (const [property, value] of [...ruleEntries, ...inlineEntries]) {
      if (colourOnly.includes(property)) {
         continue;
      }

      const withoutColour = value.replace(/var\(--growth-(?!space-|stroke-|leading-|type-)[a-z0-9-]+\)/g, "").trim();
      const isBackground = property === "background";

      if (!isBackground) {
         kept.set(property, withoutColour);
      }
   }

   const drawsNothing = Array.from(kept.entries()).filter(([property, value]) => INITIAL_VALUES[property]?.includes(value));

   for (const [property] of drawsNothing) {
      kept.delete(property);
   }

   return Array.from(kept.entries()).map(([property, value]) => `${property}:${value}`).sort();
}

function channels(hex: string) {
   const body = hex.slice(1);
   const full = body.length === 3 ? body.split("").map((digit) => digit + digit).join("") : body;

   return [0, 2, 4].map((start) => parseInt(full.slice(start, start + 2), 16) / 255);
}

function linear(channel: number) {
   return channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4;
}

function luminanceOf(rgb: number[]) {
   const [red, green, blue] = rgb.map(linear);

   return 0.2126 * red + 0.7152 * green + 0.0722 * blue;
}

/* A paint as sRGB channels in one theme, a half-transparent paint blended over what it sits on. */
export function rgbOf(theme: string, paint: Paint, beneath: Paint | null): number[] {
   const colour = channels(TOKEN_FILE[theme][paint.token]);

   if (paint.alpha >= 1 || beneath === null) {
      return colour;
   }

   const under = rgbOf(theme, beneath, null);

   return colour.map((channel, index) => channel * paint.alpha + under[index] * (1 - paint.alpha));
}

export function contrast(foreground: number[], background: number[]) {
   const lighter = Math.max(luminanceOf(foreground), luminanceOf(background));
   const darker = Math.min(luminanceOf(foreground), luminanceOf(background));

   return (lighter + 0.05) / (darker + 0.05);
}

export function describePaint(paint: Paint) {
   return paint.alpha < 1 ? `${paint.token} at ${paint.alpha}` : paint.token;
}
