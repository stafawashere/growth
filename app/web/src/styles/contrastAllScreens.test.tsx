import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";

import { cleanup } from "@testing-library/react";
import { afterEach, beforeAll, describe, expect, it, vi } from "vitest";

import {
   COLOUR_PROPERTIES,
   DESKTOP_WIDTH,
   PHONE_WIDTH,
   RULES,
   THEMES,
   VIEWPORT_WIDTHS,
   appliesAtWidth,
   borderPaint,
   contrast,
   declared,
   describePaint,
   effectiveBackground,
   fontSizeToken,
   isMatchable,
   isSvgElement,
   matchingRules,
   ownBackground,
   paintOf,
   resolvedColour,
   resolvedSvgPaint,
   rgbOf,
   setViewportWidth,
   type Paint,
   type Rule
} from "../testing/cascade";
import { SCREENS } from "../testing/screens";

vi.mock("../api/client");

/* 11's P8 eval eval_contrast_all_screens. Every screen in testing/screens.tsx is rendered, and the
   foreground and background of everything drawn is resolved from app.css and the components, so
   the pairs are the ones the client produces, not a list typed here. Text holds 4.5:1, or 3:1 at
   type-title and type-display (WCAG 2.2 SC 1.4.3); a control's boundary, the focus ring and every
   drawn mark hold the SC 1.4.11 floor against what they sit on. Both themes of growth-tokens.json
   are checked, at a desktop and a phone width, each width matching only the @media rules that
   hold there. Coverage then holds every colour-bearing rule in app.css and every colour token a
   component writes to having been drawn by some screen, so a new rule cannot escape.

   Not checked, each for its reason: the text of an element clipped by .visually-hidden or
   KaTeX's .katex-mathml, which is never painted; a fill in a surface or accent tint role, which
   is ground that other marks sit on and is checked as their background; the card's box-shadow,
   which is decoration that 08 says to prefer over borders and which identifies nothing. */

const DESIGN_ROOT = join(__dirname, "..", "..", "..", "design");

const CONTRAST_SOURCE = readFileSync(join(DESIGN_ROOT, "contrast.py"), "utf8");

function floorNamed(name: string) {
   const match = new RegExp(`^${name} = ([\\d.]+)$`, "m").exec(CONTRAST_SOURCE);

   if (match === null) {
      throw new Error(`app/design/contrast.py declares no ${name}`);
   }

   return Number(match[1]);
}

const TEXT_FLOOR = floorNamed("TEXT_CONTRAST_FLOOR");

const LARGE_TEXT_FLOOR = floorNamed("LARGE_TEXT_CONTRAST_FLOOR");

const NON_TEXT_FLOOR = floorNamed("NON_TEXT_CONTRAST_FLOOR");

const LARGE_TYPE_STEPS = ["type-display", "type-title"];

const GROUND_TOKENS = /^(surface-|accent-tint-)/;

const SHAPES = ["line", "polyline", "polygon", "path", "rect", "circle", "ellipse"];

const TEXT_FIELDS = "textarea, math-field, select, input:not([type='radio']):not([type='checkbox']):not([type='hidden'])";

const FOCUSABLE = "button:not(:disabled), input:not(:disabled), textarea, select, math-field, a[href], summary, [tabindex='0']";

interface Pair {
   screen: string;
   width: number | null;
   what: string;
   foreground: Paint;
   background: Paint;
   beneath: Paint | null;
   floor: number;
}

function isPainted(element: Element) {
   const hiddenAncestor = element.closest(".visually-hidden, .katex-mathml, [hidden], title, desc");

   return hiddenAncestor === null;
}

function ownText(element: Element) {
   return Array.from(element.childNodes)
      .filter((node) => node.nodeType === Node.TEXT_NODE)
      .map((node) => node.textContent ?? "")
      .join("")
      .trim();
}

function label(element: Element) {
   const name = element.tagName.toLowerCase();
   const classes = element.getAttribute("class");

   return classes ? `${name}.${classes.split(/\s+/).join(".")}` : name;
}

function textFloor(element: Element) {
   return LARGE_TYPE_STEPS.includes(fontSizeToken(element) ?? "") ? LARGE_TEXT_FLOOR : TEXT_FLOOR;
}

/* What an SVG element may sit on: the page behind the drawing, and every ground-role fill drawn
   before it in the same drawing. */
function svgBackdrops(element: Element): Array<{ paint: Paint; beneath: Paint | null }> {
   const svg = element.closest("svg")!;
   const page = effectiveBackground(svg.parentElement);
   const backdrops: Array<{ paint: Paint; beneath: Paint | null }> = [{ paint: page, beneath: null }];

   for (const shape of Array.from(svg.querySelectorAll(SHAPES.join(", ")))) {
      const isBefore = shape.compareDocumentPosition(element) & Node.DOCUMENT_POSITION_FOLLOWING;

      if (!isBefore || shape === element) {
         continue;
      }

      const fill = resolvedSvgPaint(shape, "fill");
      const isGround = fill !== null && GROUND_TOKENS.test(fill.token);

      if (isGround) {
         backdrops.push({ paint: fill!, beneath: page });
      }
   }

   return backdrops;
}

function pairsIn(screen: string, width: number, container: HTMLElement): Pair[] {
   const pairs: Pair[] = [];
   const focusRule = RULES.find((rule) => rule.selector === ":focus-visible");
   const focusRing = focusRule === undefined ? null : (paintOf(/var\(--growth-[a-z-]+\)/.exec(focusRule.declarations.get("outline") ?? "")?.[0] ?? "") as Paint | null);

   function add(what: string, foreground: Paint | null, background: Paint, floor: number, beneath: Paint | null = null) {
      if (foreground !== null) {
         pairs.push({ screen, width, what, foreground, background, beneath, floor });
      }
   }

   for (const element of Array.from(container.querySelectorAll("*"))) {
      if (!isPainted(element)) {
         continue;
      }

      if (isSvgElement(element)) {
         const tag = element.tagName.toLowerCase();

         for (const backdrop of tag === "svg" ? [] : svgBackdrops(element)) {
            if (tag === "text" && ownText(element) !== "") {
               add(`${label(element)} "${ownText(element)}"`, resolvedSvgPaint(element, "fill"), backdrop.paint, textFloor(element), backdrop.beneath);
            }

            if (SHAPES.includes(tag)) {
               const fill = resolvedSvgPaint(element, "fill");
               const isMarkFill = fill !== null && !GROUND_TOKENS.test(fill.token);

               add(`${label(element)} stroke`, resolvedSvgPaint(element, "stroke"), backdrop.paint, NON_TEXT_FLOOR, backdrop.beneath);
               add(`${label(element)} fill`, isMarkFill ? fill : null, backdrop.paint, NON_TEXT_FLOOR, backdrop.beneath);
            }
         }

         continue;
      }

      const background = effectiveBackground(element);
      const behind = effectiveBackground(element.parentElement);

      if (ownText(element) !== "") {
         add(`${label(element)} "${ownText(element).slice(0, 40)}"`, resolvedColour(element), background, textFloor(element));
      }

      if (element.matches(TEXT_FIELDS)) {
         add(`${label(element)} typed text`, resolvedColour(element), background, TEXT_FLOOR);
      }

      const isChoiceControl = element.matches("input[type='radio'], input[type='checkbox']");

      if (isChoiceControl) {
         const accent = declared(element, "accent-color");

         expect(accent, `${screen}: ${label(element)} is drawn in the browser's colours, not a token`).not.toBeNull();
         add(`${label(element)} accent`, paintOf(accent!) as Paint, behind, NON_TEXT_FLOOR);
      }

      const border = borderPaint(element);

      if (border !== null) {
         add(`${label(element)} border against its own ground`, border, background, NON_TEXT_FLOOR);
         add(`${label(element)} border against what surrounds it`, border, behind, NON_TEXT_FLOOR);
      }

      const fill = ownBackground(element);
      const isControl = element.matches("button, input, textarea, select, math-field");
      const fillIdentifiesControl = isControl && fill !== null && !GROUND_TOKENS.test(fill.token);

      if (fillIdentifiesControl) {
         add(`${label(element)} control fill`, fill, behind, NON_TEXT_FLOOR);
      }

      if (element.matches(FOCUSABLE) && focusRing !== null) {
         add(`${label(element)} focus ring`, focusRing, behind, NON_TEXT_FLOOR);
      }
   }

   return pairs;
}

/* A rule that sets both a text colour and its own background is a pair whatever it is drawn on. */
function selfContainedPairs(): Pair[] {
   return RULES.flatMap((rule) => {
      const colour = rule.declarations.get("color");
      const ground = rule.declarations.get("background") ?? rule.declarations.get("background-color");
      const hasBoth = colour !== undefined && ground !== undefined;

      if (!hasBoth) {
         return [];
      }

      const foreground = paintOf(colour!);
      const background = paintOf(ground!);
      const isPaintPair = foreground !== null && foreground !== "current" && background !== null && background !== "current";

      return isPaintPair ? [{ screen: "app.css", width: null, what: rule.selector, foreground, background, beneath: null, floor: TEXT_FLOOR }] : [];
   });
}

function colourBearing(rule: Rule) {
   return COLOUR_PROPERTIES.some((property) => {
      const value = rule.declarations.get(property);
      const isDecoration = property === "box-shadow";

      return value !== undefined && !isDecoration && /var\(--growth-/.test(value);
   });
}

function componentColourTokens() {
   const found: Array<{ file: string; token: string }> = [];
   const root = join(__dirname, "..");

   function walk(directory: string) {
      for (const entry of readdirSync(directory)) {
         const path = join(directory, entry);

         if (statSync(path).isDirectory()) {
            walk(path);
            continue;
         }

         const isComponent = entry.endsWith(".tsx") && !entry.includes(".test.");
         const isTestSupport = relative(root, path).startsWith("testing");

         if (!isComponent || isTestSupport) {
            continue;
         }

         const text = readFileSync(path, "utf8");

         for (const match of text.matchAll(/var\(--growth-((?:surface|border|text|focus|accent|state)-[a-z0-9-]+)\)/g)) {
            found.push({ file: relative(root, path), token: match[1] });
         }
      }
   }

   walk(root);

   return found;
}

const collected: { pairs: Pair[]; matchedRules: Set<Rule>; matchedAtWidth: Map<number, Set<Rule>>; renderedMarkup: string; screens: number } = {
   pairs: [],
   matchedRules: new Set(),
   matchedAtWidth: new Map(VIEWPORT_WIDTHS.map((width) => [width, new Set<Rule>()])),
   renderedMarkup: "",
   screens: 0
};

/* Rendering every screen of the catalogue takes about 9 s alone and more beside the other suites,
   so the setup gets its own budget instead of vitest's 10 s hook default. */
const CATALOGUE_RENDER_TIMEOUT_MS = 60000;

beforeAll(async () => {
   for (const entry of SCREENS) {
      const container = await entry.mount();
      const ancestors = [document.documentElement, document.body];

      for (const width of VIEWPORT_WIDTHS) {
         setViewportWidth(width);
         collected.pairs.push(...pairsIn(entry.name, width, container));

         for (const element of [...ancestors, ...Array.from(container.querySelectorAll("*"))]) {
            for (const rule of matchingRules(element)) {
               collected.matchedRules.add(rule);
               collected.matchedAtWidth.get(width)!.add(rule);
            }
         }
      }

      setViewportWidth(DESKTOP_WIDTH);
      collected.renderedMarkup += container.innerHTML;
      collected.screens += 1;
      cleanup();
   }

   collected.pairs.push(...selfContainedPairs());
}, CATALOGUE_RENDER_TIMEOUT_MS);

afterEach(() => {
   cleanup();
   setViewportWidth(DESKTOP_WIDTH);
});

describe("eval_contrast_all_screens", () => {
   it("renders every screen in the catalogue and derives the pairs from what they draw", () => {
      expect(collected.screens).toBe(SCREENS.length);
      expect(collected.pairs.filter((pair) => pair.floor === NON_TEXT_FLOOR).length).toBeGreaterThan(50);
      expect(collected.pairs.filter((pair) => pair.floor === TEXT_FLOOR).length).toBeGreaterThan(200);
      expect([TEXT_FLOOR, LARGE_TEXT_FLOOR, NON_TEXT_FLOOR]).toEqual([4.5, 3, 3]);
   });

   it("reads app.css at both widths, and a phone-only rule is matched at the phone width alone", () => {
      const phoneOnly = Array.from(collected.matchedAtWidth.get(PHONE_WIDTH)!).filter((rule) => rule.media.length > 0);
      const leakedToDesktop = phoneOnly.filter((rule) => collected.matchedAtWidth.get(DESKTOP_WIDTH)!.has(rule));
      const pairsAt = (width: number) => collected.pairs.filter((pair) => pair.width === width).length;

      expect(VIEWPORT_WIDTHS).toEqual([1280, 375]);
      expect(phoneOnly.length).toBeGreaterThan(0);
      expect(leakedToDesktop).toEqual([]);
      expect(pairsAt(DESKTOP_WIDTH)).toBeGreaterThan(250);
      expect(pairsAt(PHONE_WIDTH)).toBeGreaterThan(250);
   });

   it("refuses a media condition it cannot evaluate, rather than guessing", () => {
      const rule = (media: string): Rule => ({ selector: "p", specificity: 1, order: 1, declarations: new Map(), media: [media] });

      expect(appliesAtWidth(rule("(max-width: 600px)"), PHONE_WIDTH)).toBe(true);
      expect(appliesAtWidth(rule("(max-width: 600px)"), DESKTOP_WIDTH)).toBe(false);
      expect(appliesAtWidth(rule("(min-width: 1100px)"), DESKTOP_WIDTH)).toBe(true);
      expect(() => appliesAtWidth(rule("(prefers-reduced-motion: reduce)"), PHONE_WIDTH)).toThrow(/cannot evaluate/);
   });

   it("every pair holds its floor in both themes", () => {
      const failures = new Set<string>();

      for (const theme of THEMES) {
         for (const pair of collected.pairs) {
            const beneath = pair.beneath;
            const background = rgbOf(theme, pair.background, beneath);
            const foreground = rgbOf(theme, pair.foreground, pair.background);
            const ratio = contrast(foreground, background);

            if (ratio < pair.floor) {
               const where = pair.width === null ? pair.screen : `${pair.screen} at ${pair.width} px`;

               failures.add(
                  `${theme}: ${where}: ${pair.what}: ${describePaint(pair.foreground)} on ${describePaint(pair.background)}${beneath ? ` over ${describePaint(beneath)}` : ""} is ${ratio.toFixed(2)}:1, floor ${pair.floor}:1`
               );
            }
         }
      }

      expect(Array.from(failures)).toEqual([]);
   });

   it("every colour-bearing rule in app.css was drawn by some screen", () => {
      const undrawn = RULES.filter((rule) => colourBearing(rule) && isMatchable(rule) && !collected.matchedRules.has(rule))
         .filter((rule) => !rule.selector.includes(":focus-visible"))
         .map((rule) => rule.selector);

      expect(undrawn).toEqual([]);
   });

   it("every colour token a component writes was drawn by some screen", () => {
      const written = componentColourTokens();
      const undrawn = written.filter(({ token }) => !collected.renderedMarkup.includes(`var(--growth-${token})`));

      expect(written.length).toBeGreaterThan(10);
      expect(undrawn).toEqual([]);
   });
});
