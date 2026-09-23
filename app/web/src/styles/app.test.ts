import { readFileSync } from "node:fs";

import { describe, expect, it } from "vitest";

const MODULE_URL = import.meta.url;

const STYLESHEET_TEXT = readFileSync(new URL("./app.css", MODULE_URL), "utf8");

const TOKENS_SOURCE = readFileSync(new URL("../../../design/tokens.py", MODULE_URL), "utf8");

const DESIGN_BRIEF_TEXT = readFileSync(
   new URL("../../../../docs/plan/08-design-brief.md", MODULE_URL),
   "utf8"
);

const CUSTOM_PROPERTY_PREFIX = "--growth-";

interface Declaration {
   selector: string;
   property: string;
   value: string;
}

interface Rule {
   selector: string;
   declarations: Declaration[];
}

function withoutComments(text: string) {
   return text.replace(/\/\*[\s\S]*?\*\//g, " ");
}

function declarationsIn(selector: string, body: string): Declaration[] {
   const declarations: Declaration[] = [];

   for (const statement of body.split(";")) {
      const colon = statement.indexOf(":");
      const isDeclaration = colon > 0;

      if (!isDeclaration) {
         continue;
      }

      const property = statement.slice(0, colon).trim().toLowerCase();
      const value = statement.slice(colon + 1).trim();

      declarations.push({ selector, property, value });
   }

   return declarations;
}

function rulesIn(text: string): Rule[] {
   const rules: Rule[] = [];
   const blockPattern = /([^{}]+)\{([^{}]*)\}/g;

   for (const match of text.matchAll(blockPattern)) {
      const selector = match[1].trim();

      rules.push({ selector, declarations: declarationsIn(selector, match[2]) });
   }

   return rules;
}

const RULES = rulesIn(withoutComments(STYLESHEET_TEXT));

const DECLARATIONS = RULES.flatMap((rule) => rule.declarations);

function pythonBlock(name: string, opener: string, closer: string) {
   const start = TOKENS_SOURCE.indexOf(`\n${name} = `);

   if (start < 0) {
      throw new Error(`app/design/tokens.py no longer defines ${name}`);
   }

   const open = TOKENS_SOURCE.indexOf(opener, start);
   const close = TOKENS_SOURCE.indexOf("\n" + closer, open);

   return TOKENS_SOURCE.slice(open, close + 2);
}

function colourTokenNames() {
   const block = pythonBlock("COLOUR_TOKENS", "(", ")");

   return Array.from(block.matchAll(/"([a-z0-9-]+)"/g), (match) => match[1]);
}

function typeTokenNames() {
   const block = pythonBlock("TYPE_TOKENS", "{", "}");

   return Array.from(block.matchAll(/"([a-z0-9-]+)":/g), (match) => match[1]);
}

function spacingTokenNames() {
   const block = pythonBlock("SPACING_TOKENS", "{", "}");
   const nameTemplate = block.match(/"([a-z-]+)\{0\}"/);
   const values = block.match(/for value in \(([^)]*)\)/);

   if (nameTemplate === null || values === null) {
      throw new Error("app/design/tokens.py SPACING_TOKENS no longer has the shape this test reads");
   }

   return values[1].split(",").map((value) => nameTemplate[1] + value.trim());
}

const COLOUR_TOKENS = colourTokenNames();

const TYPE_TOKENS = typeTokenNames();

const SPACING_TOKENS = spacingTokenNames();

const KNOWN_TOKENS = [...COLOUR_TOKENS, ...TYPE_TOKENS, ...SPACING_TOKENS];

/* 08's type table, read row by row: the token in the first column and the px line height in the
   third. */
function lineHeightsByTypeToken() {
   const lineHeights = new Map<string, number>();
   const rowPattern = /^\| `(type-[a-z-]+)` \| \d+ px \| (\d+) px \|/gm;

   for (const match of DESIGN_BRIEF_TEXT.matchAll(rowPattern)) {
      lineHeights.set(match[1], Number(match[2]));
   }

   return lineHeights;
}

function proseMeasure() {
   const match = DESIGN_BRIEF_TEXT.match(/Measure is capped at (\d+) characters/);

   if (match === null) {
      throw new Error("08-design-brief.md no longer states the prose measure where expected");
   }

   return Number(match[1]);
}

const CSS_WIDE_KEYWORDS = ["inherit", "initial", "unset", "revert", "revert-layer"];

const CONTEXT_COLOUR_KEYWORDS = ["currentcolor", "transparent"];

const HEX_COLOUR = /#[0-9a-fA-F]{3,8}\b/g;

const COLOUR_FUNCTION = /\b(rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(/gi;

const GROWTH_REFERENCE = /var\(\s*(--[a-z0-9-]+)\s*\)/g;

function namesAColour(word: string) {
   const probe = document.createElement("div");

   probe.style.color = "";
   probe.style.color = word;

   const parsed = probe.style.color.toLowerCase();
   const parsedAsColour = parsed.length > 0;
   const isKeyword = CSS_WIDE_KEYWORDS.includes(parsed) || CONTEXT_COLOUR_KEYWORDS.includes(parsed);

   return parsedAsColour && !isKeyword;
}

function wordsOutsideReferences(value: string) {
   return value
      .replace(GROWTH_REFERENCE, " ")
      .split(/[\s,()]+/)
      .filter((word) => word.length > 0);
}

function typeTokenOf(rule: Rule) {
   const fontSize = rule.declarations.find((declaration) => declaration.property === "font-size");

   if (fontSize === undefined) {
      return null;
   }

   const match = fontSize.value.match(/^var\(--growth-(type-[a-z-]+)\)$/);

   return match === null ? null : match[1];
}

/* Every numeric literal a declaration may carry once its spacing references are removed: a bare
   zero, a unitless factor applied to a spacing step inside calc, the prose measure in ch, and a
   px line height that 08's type table pairs with the rule's own type token. */
function lengthOffenders(rule: Rule, measure: number, lineHeights: Map<string, number>) {
   const offenders: string[] = [];
   const numberPattern = /(^|[^\w-])(-?\d*\.?\d+)([a-z%]*)/gi;

   for (const declaration of rule.declarations) {
      const stripped = declaration.value.replace(GROWTH_REFERENCE, "SPACE");

      for (const match of stripped.matchAll(numberPattern)) {
         const start = (match.index ?? 0) + match[1].length;
         const amount = Number(match[2]);
         const unit = match[3].toLowerCase();
         const preceding = stripped.slice(0, start).trimEnd();
         const following = stripped.slice((match.index ?? 0) + match[0].length).trimStart();

         const isBareZero = amount === 0 && unit === "";
         const isUnitless = unit === "";
         const scalesANeighbour = preceding.endsWith("*") || preceding.endsWith("/") || following.startsWith("*");
         const isFactor = isUnitless && scalesANeighbour;
         const isMeasure = unit === "ch" && amount === measure;

         const ruleToken = typeTokenOf(rule);
         const pairedLineHeight = ruleToken === null ? undefined : lineHeights.get(ruleToken);
         const isLineHeight = declaration.property === "line-height" && unit === "px";
         const isTableLineHeight = isLineHeight && pairedLineHeight === amount;

         const isAllowed = isBareZero || isFactor || isMeasure || isTableLineHeight;

         if (!isAllowed) {
            offenders.push(`${rule.selector} { ${declaration.property}: ${declaration.value} }`);
         }
      }
   }

   return offenders;
}

describe("the application stylesheet", () => {
   it("parses into rules and declarations", () => {
      expect(RULES.length, "app.css parsed to no rules").toBeGreaterThan(0);
      expect(DECLARATIONS.length, "app.css parsed to no declarations").toBeGreaterThan(0);

      const colourDeclarations = DECLARATIONS.filter((declaration) => declaration.property === "color");

      expect(colourDeclarations.length, "app.css sets no colour at all").toBeGreaterThan(0);
   });

   it("writes no colour literal and no font size outside a token", () => {
      const source = withoutComments(STYLESHEET_TEXT);

      expect(source.match(HEX_COLOUR) ?? [], "app.css writes a hex colour").toEqual([]);
      expect(source.match(COLOUR_FUNCTION) ?? [], "app.css writes a colour function").toEqual([]);

      const namedColours = DECLARATIONS.flatMap((declaration) =>
         wordsOutsideReferences(declaration.value)
            .filter(namesAColour)
            .map((word) => `${declaration.selector} { ${declaration.property}: ${word} }`)
      );

      expect(namedColours, "app.css names a colour").toEqual([]);

      const fontSizes = DECLARATIONS.filter((declaration) => declaration.property === "font-size");

      expect(fontSizes.length, "app.css sets no font size").toBeGreaterThan(0);

      for (const declaration of fontSizes) {
         expect(declaration.value, `${declaration.selector} sets a font size outside a type token`)
            .toMatch(/^var\(--growth-type-[a-z-]+\)$/);
      }
   });

   it("references only custom properties app/design/tokens.py names", () => {
      expect(COLOUR_TOKENS.length).toBeGreaterThan(0);
      expect(TYPE_TOKENS.length).toBeGreaterThan(0);
      expect(SPACING_TOKENS.length).toBeGreaterThan(0);

      const references = Array.from(
         withoutComments(STYLESHEET_TEXT).matchAll(/var\(\s*(--[a-zA-Z0-9-]+)/g),
         (match) => match[1]
      );

      expect(references.length, "app.css references no token").toBeGreaterThan(0);

      for (const reference of references) {
         const isGrowthReference = reference.startsWith(CUSTOM_PROPERTY_PREFIX);

         expect(isGrowthReference, `${reference} is not a growth token`).toBe(true);

         const token = reference.slice(CUSTOM_PROPERTY_PREFIX.length);

         expect(KNOWN_TOKENS, `${reference} names no token in app/design/tokens.py`).toContain(token);
      }
   });

   it("every length is a spacing step or derived from one, and every line height is 08's", () => {
      const measure = proseMeasure();
      const lineHeights = lineHeightsByTypeToken();

      expect(lineHeights.size, "08's type table did not parse").toBe(TYPE_TOKENS.length);

      const offenders = RULES.flatMap((rule) => lengthOffenders(rule, measure, lineHeights));

      expect(offenders).toEqual([]);

      const spacingReferences = DECLARATIONS.filter((declaration) =>
         declaration.value.includes("var(--growth-space-")
      );

      expect(spacingReferences.length, "app.css uses no spacing step").toBeGreaterThan(0);

      const measureDeclarations = DECLARATIONS.filter((declaration) =>
         declaration.value.includes(`${measure}ch`)
      );

      expect(measureDeclarations.length, "app.css never caps the column at 08's measure")
         .toBeGreaterThan(0);
   });

   it("animates nothing, leaving every transition to motion.css", () => {
      const moving = DECLARATIONS.filter((declaration) =>
         /^(transition|animation)(-|$)/.test(declaration.property)
      );

      expect(moving.map((declaration) => `${declaration.selector} { ${declaration.property} }`))
         .toEqual([]);
   });

   it("sets a focus-visible outline from the focus-ring token, reaching buttons, inputs and links", () => {
      const focusRules = RULES.filter((rule) =>
         rule.selector.split(",").some((part) => part.trim().endsWith(":focus-visible"))
      );

      expect(focusRules.length, "app.css sets no :focus-visible rule").toBeGreaterThan(0);

      const growthOutline = focusRules
         .flatMap((rule) => rule.declarations)
         .find(
            (declaration) =>
               (declaration.property === "outline" || declaration.property === "outline-color") &&
               declaration.value.includes("var(--growth-focus-ring)")
         );

      expect(growthOutline, "no :focus-visible rule sets an outline from --growth-focus-ring")
         .toBeTruthy();

      const coveringSelectors = focusRules.flatMap((rule) =>
         rule.selector.split(",").map((part) => part.trim())
      );
      const isUniversal = coveringSelectors.includes(":focus-visible");

      const coversTag = (tag: string) =>
         isUniversal ||
         coveringSelectors.some((selector) => new RegExp(`^${tag}(\\[[^\\]]*\\])?:focus-visible$`).test(selector));

      expect(coversTag("button"), "the focus-visible rule does not reach button").toBe(true);
      expect(coversTag("input"), "the focus-visible rule does not reach input").toBe(true);
      expect(coversTag("a"), "the focus-visible rule does not reach a link").toBe(true);
   });
});