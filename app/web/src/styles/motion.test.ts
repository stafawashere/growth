import { readFileSync } from "node:fs";

import { beforeAll, describe, expect, it } from "vitest";

import {
   ANIMATABLE_PROPERTIES,
   INSTANT_CLASSES,
   MOTION_CLASSES,
   MOTION_DURATION,
   MOTION_EASING,
   REDUCED_MOTION_QUERY,
   TRANSFORM_MOTION_CLASSES
} from "./motion";

const MODULE_URL = import.meta.url;

const STYLESHEET_TEXT = readFileSync(new URL("./motion.css", MODULE_URL), "utf8");

let baseRules: Map<string, CSSStyleDeclaration>;
let reducedRules: Map<string, CSSStyleDeclaration>;

function selectorClass(selectorText: string) {
   return selectorText.trim().replace(/^\./, "");
}

function transitionSegments(declaration: CSSStyleDeclaration) {
   const value = declaration.getPropertyValue("transition");

   const isEmpty = value.trim() === "";

   if (isEmpty) {
      return [];
   }

   const withoutGroups = value.replace(/\(([^)]*)\)/g, (_match, inner: string) =>
      "(" + inner.replace(/,/g, ";") + ")"
   );

   return withoutGroups.split(",").map((part) => part.trim());
}

function transitionedProperties(declaration: CSSStyleDeclaration) {
   return transitionSegments(declaration).map((segment) => segment.split(/\s+/)[0]);
}

beforeAll(() => {
   const element = document.createElement("style");
   element.textContent = STYLESHEET_TEXT;
   document.head.appendChild(element);

   const sheet = document.styleSheets[document.styleSheets.length - 1];

   baseRules = new Map();
   reducedRules = new Map();

   for (const rule of Array.from(sheet.cssRules)) {
      const isStyleRule = rule instanceof CSSStyleRule;

      if (isStyleRule) {
         baseRules.set(selectorClass(rule.selectorText), rule.style);
      }

      const isMediaRule = rule instanceof CSSMediaRule;
      const isReducedMotionRule = isMediaRule && rule.conditionText.includes("prefers-reduced-motion");

      if (isReducedMotionRule) {
         expect(rule.conditionText).toBe(REDUCED_MOTION_QUERY);

         for (const inner of Array.from(rule.cssRules)) {
            const isInnerStyleRule = inner instanceof CSSStyleRule;

            if (isInnerStyleRule) {
               reducedRules.set(selectorClass(inner.selectorText), inner.style);
            }
         }
      }
   }
});

describe("the motion stylesheet", () => {
   it("every motion class the contract names is defined in the stylesheet", () => {
      expect(MOTION_CLASSES.length).toBeGreaterThan(0);

      for (const className of MOTION_CLASSES) {
         expect(baseRules.has(className), `${className} has no rule in motion.css`).toBe(true);
      }
   });

   it("animates only transform and opacity, at one duration and one easing", () => {
      for (const className of TRANSFORM_MOTION_CLASSES) {
         const declaration = baseRules.get(className) as CSSStyleDeclaration;

         for (const property of transitionedProperties(declaration)) {
            expect(ANIMATABLE_PROPERTIES, `${className} animates ${property}`).toContain(property);
         }

         expect(transitionedProperties(declaration), `${className} does not animate transform`)
            .toContain("transform");

         for (const segment of transitionSegments(declaration)) {
            const timing = segment.split(/\s+/).slice(1).join(" ");

            expect(timing, `${className} times ${segment} off the single duration and easing`)
               .toBe(`${MOTION_DURATION} ${MOTION_EASING}`);
         }
      }
   });

   it("the classes on repeated keystroke paths carry no transition at all", () => {
      for (const className of INSTANT_CLASSES) {
         const declaration = baseRules.get(className) as CSSStyleDeclaration;

         expect(declaration.getPropertyValue("transition"), `${className} is animated`).toBe("none");
      }
   });

   it("every transform transition has a reduced-motion rule that cross-fades opacity instead", () => {
      for (const className of TRANSFORM_MOTION_CLASSES) {
         const declaration = reducedRules.get(className);

         expect(declaration, `${className} has no rule under ${REDUCED_MOTION_QUERY}`).toBeDefined();

         const properties = transitionedProperties(declaration as CSSStyleDeclaration);

         expect(properties, `${className} still animates transform under reduce`)
            .not.toContain("transform");

         expect(properties, `${className} does not cross-fade opacity under reduce`)
            .toContain("opacity");

         expect(
            (declaration as CSSStyleDeclaration).getPropertyValue("transform"),
            `${className} does not neutralise its transform under reduce`
         ).toBe("none");
      }
   });

   it("the reduced-motion block never removes the transition outright", () => {
      for (const className of TRANSFORM_MOTION_CLASSES) {
         const declaration = reducedRules.get(className) as CSSStyleDeclaration;
         const transition = declaration.getPropertyValue("transition");
         const animation = declaration.getPropertyValue("animation");

         expect(transition, `${className} drops its transition under reduce`).not.toBe("");
         expect(transition, `${className} drops its transition under reduce`).not.toBe("none");
         expect(animation, `${className} ships animation: none under reduce`).not.toBe("none");

         expect(transition, `${className} cross-fades without a duration under reduce`)
            .toContain(MOTION_DURATION);
      }
   });

   it("no hex colour and no second duration appear in the stylesheet", () => {
      const hexColours = STYLESHEET_TEXT.match(/#[0-9a-fA-F]{3,8}\b/g) ?? [];

      expect(hexColours, "motion.css authors a colour").toEqual([]);

      const durations = STYLESHEET_TEXT.match(/\b\d+(?:\.\d+)?m?s\b/g) ?? [];

      expect(durations.length, "motion.css states no duration").toBeGreaterThan(0);
      expect(Array.from(new Set(durations))).toEqual([MOTION_DURATION]);

      const curves = STYLESHEET_TEXT.match(/cubic-bezier\([^)]*\)/g) ?? [];

      expect(curves, "motion.css invents an easing curve").toEqual([]);
   });
});
