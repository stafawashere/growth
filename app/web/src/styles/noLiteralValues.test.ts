import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";

import * as ts from "typescript";
import { describe, expect, it } from "vitest";

/* 11's P8 gate test_no_literal_values: every colour, font size, spacing length, line height,
   border or stroke width and duration in the client resolves to a token from
   app/design/tokens.py, with no literal value outside the token file.

   What is scanned: every .css, .ts and .tsx under src except the tests and the shared test support
   under src/testing. What counts as a design value in TypeScript: any string that carries a colour
   or a CSS length or duration, any value given to a presentation attribute that sets a size,
   weight, width, dash, radius or opacity, the rendered size of an svg or img, and every value of an
   inline style object that is not a token reference.

   What is geometry and deliberately not scanned: the numbers an SVG is drawn with in its own user
   units, which are viewBox extents, plot margins, positions, point lists, path data and offsets
   computed from a figure's data. They scale with the drawing and never reach CSS, so they are
   coordinates rather than design values.

   The exemptions below are the only literals allowed, each with its reason. */

const SOURCE_ROOT = join(__dirname, "..");

const DESIGN_ROOT = join(SOURCE_ROOT, "..", "..", "design");

const TOKENS_SOURCE = readFileSync(join(DESIGN_ROOT, "tokens.py"), "utf8");

const DESIGN_BRIEF_TEXT = readFileSync(join(SOURCE_ROOT, "..", "..", "..", "docs", "plan", "08-design-brief.md"), "utf8");

function motionDurationToken() {
   const match = /"motion-duration": "([^"]+)"/.exec(TOKENS_SOURCE);

   if (match === null) {
      throw new Error("app/design/tokens.py names no motion-duration token");
   }

   return match[1];
}

function proseMeasure() {
   const match = DESIGN_BRIEF_TEXT.match(/Measure is capped at (\d+) characters/);

   if (match === null) {
      throw new Error("08-design-brief.md no longer states the prose measure where expected");
   }

   return `${match[1]}ch`;
}

const MOTION_DURATION_TOKEN = motionDurationToken();

const PROSE_MEASURE = proseMeasure();

interface Exemption {
   file: string;
   literal: string;
   reason: string;
}

/* motion.test.ts's "no hex colour and no second duration appear in the stylesheet" requires
   motion.css to state its one duration as a literal, so that literal stays and is held here to
   the motion-duration token's value; any other duration in motion.css still fails. motion.ts
   carries the same value for that test to compare against. The zoom tool scales the question
   area by the percentage the student picks, which is their setting, not a design value. */
const EXEMPTIONS: Exemption[] = [
   {
      file: "styles/motion.css",
      literal: MOTION_DURATION_TOKEN,
      reason: "motion.test.ts pins the one duration as a literal; it must equal tokens.py motion-duration"
   },
   {
      file: "styles/motion.ts",
      literal: MOTION_DURATION_TOKEN,
      reason: "the value motion.test.ts compares motion.css against; it must equal tokens.py motion-duration"
   },
   {
      file: "assessment/PartRunner.tsx",
      literal: "style.fontSize=`${zoom}%`",
      reason: "the student's zoom setting from the Bluebook zoom tool"
   }
];

function isTestCode(path: string) {
   const name = relative(SOURCE_ROOT, path);
   const isTestFile = /\.test\.tsx?$/.test(name);
   const isTestSupport = name.startsWith("testing/");

   return isTestFile || isTestSupport;
}

function sourceFiles(directory: string): string[] {
   const found: string[] = [];

   for (const entry of readdirSync(directory)) {
      const path = join(directory, entry);
      const isDirectory = statSync(path).isDirectory();

      if (isDirectory) {
         found.push(...sourceFiles(path));
         continue;
      }

      const isScanned = /\.(css|ts|tsx)$/.test(entry) && !/\.d\.ts$/.test(entry);

      if (isScanned && !isTestCode(path)) {
         found.push(path);
      }
   }

   return found;
}

const HEX_COLOUR = /#[0-9a-fA-F]{3,8}\b/;

const COLOUR_FUNCTION = /\b(rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(/i;

const CSS_LENGTH_OR_DURATION = /(^|[^\w.-])(-?\d*\.?\d+)(px|rem|em|pt|pc|ch|ex|vh|vw|vmin|vmax|cm|mm|in|q|ms|s|%)(?![\w-])/i;

const GROWTH_REFERENCE = /var\(\s*--growth-[a-z0-9-]+\s*\)/g;

const CSS_WIDE_KEYWORDS = ["inherit", "initial", "unset", "revert", "revert-layer"];

const CONTEXT_COLOUR_KEYWORDS = ["currentcolor", "transparent"];

/* A bare word is only read as a named colour where a colour is expected, because class names such
   as "field" and "mark" are CSS system colours and "tan" is a function in the graphing panel. */
const COLOUR_ATTRIBUTES = ["fill", "stroke", "color", "stopColor", "floodColor", "lightingColor", "background", "backgroundColor", "borderColor", "outlineColor"];

function namesAColour(word: string) {
   const isWord = /^[a-z]+$/i.test(word);

   if (!isWord) {
      return false;
   }

   const probe = document.createElement("div");

   probe.style.color = "";
   probe.style.color = word;

   const parsed = probe.style.color.toLowerCase();
   const parsedAsColour = parsed.length > 0;
   const isKeyword = CSS_WIDE_KEYWORDS.includes(parsed) || CONTEXT_COLOUR_KEYWORDS.includes(parsed);

   return parsedAsColour && !isKeyword;
}

function isExempt(file: string, literal: string) {
   return EXEMPTIONS.some((exemption) => exemption.file === file && exemption.literal === literal);
}

/* CSS: every number left in a declaration once its token references are removed must be a bare
   zero, a unitless factor applied to a token inside calc, or 08's prose measure. */
function cssOffenders(file: string, text: string) {
   const offenders: string[] = [];
   const withoutComments = text.replace(/\/\*[\s\S]*?\*\//g, " ");
   const numberPattern = /(^|[^\w-])(-?\d*\.?\d+)([a-z%]*)/gi;

   for (const block of withoutComments.matchAll(/([^{}]+)\{([^{}]*)\}/g)) {
      const selector = block[1].trim();

      for (const statement of block[2].split(";")) {
         const colon = statement.indexOf(":");

         if (colon <= 0) {
            continue;
         }

         const property = statement.slice(0, colon).trim();
         const value = statement.slice(colon + 1).trim();
         const where = `${file}: ${selector} { ${property}: ${value} }`;

         const hasColourLiteral = HEX_COLOUR.test(value) || COLOUR_FUNCTION.test(value);
         const namedColours = value
            .replace(GROWTH_REFERENCE, " ")
            .split(/[\s,()]+/)
            .filter((word) => word.length > 0 && namesAColour(word));

         if (hasColourLiteral || namedColours.length > 0) {
            offenders.push(`${where}: colour literal`);
         }

         const stripped = value.replace(GROWTH_REFERENCE, "TOKEN");

         for (const match of stripped.matchAll(numberPattern)) {
            const start = (match.index ?? 0) + match[1].length;
            const literal = `${match[2]}${match[3]}`;
            const amount = Number(match[2]);
            const unit = match[3].toLowerCase();
            const preceding = stripped.slice(0, start).trimEnd();
            const following = stripped.slice((match.index ?? 0) + match[0].length).trimStart();

            const isBareZero = amount === 0 && unit === "";
            const isOpacityEndpoint = property === "opacity" && unit === "" && (amount === 0 || amount === 1);
            const scalesAToken = preceding.endsWith("*") || preceding.endsWith("/") || following.startsWith("*");
            const isFactor = unit === "" && scalesAToken;
            const isMeasure = literal === PROSE_MEASURE;
            const isAllowed = isBareZero || isOpacityEndpoint || isFactor || isMeasure || isExempt(file, literal);

            if (!isAllowed) {
               offenders.push(`${where}: literal ${literal}`);
            }
         }
      }
   }

   return offenders;
}

/* Presentation attributes that size, weight or fade a drawn mark. A token reaches them through a
   class in app.css, never through the attribute. */
const DESIGN_ATTRIBUTES = [
   "strokeWidth",
   "strokeDasharray",
   "strokeOpacity",
   "fillOpacity",
   "opacity",
   "fontSize",
   "fontWeight",
   "letterSpacing",
   "lineHeight",
   "r",
   "rx",
   "ry"
];

/* Elements whose width and height attributes set a rendered size rather than a coordinate. */
const SIZED_ELEMENTS = ["svg", "img", "canvas", "iframe", "video"];

function stringPieces(node: ts.Node): string[] {
   const isPlainString = ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node);

   if (isPlainString) {
      return [node.text];
   }

   if (ts.isTemplateExpression(node)) {
      return [node.head.text, ...node.templateSpans.map((span) => span.literal.text)];
   }

   return [];
}

function isTokenString(node: ts.Node) {
   const pieces = stringPieces(node);
   const isSingleString = ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node);

   if (!isSingleString) {
      return false;
   }

   const withoutTokens = pieces[0]
      .replace(GROWTH_REFERENCE, "")
      .replace(/[*/]\s*\d*\.?\d+|\d*\.?\d+\s*\*/g, "")
      .replace(/calc\(|\)|[\s+-]/g, "");

   return pieces[0].includes("var(--growth-") && withoutTokens === "";
}

function isInColourContext(node: ts.Node) {
   let current: ts.Node = node;

   while (ts.isConditionalExpression(current.parent) || ts.isParenthesizedExpression(current.parent) || ts.isJsxExpression(current.parent)) {
      current = current.parent;
   }

   const parent = current.parent;
   const isColourAttribute = ts.isJsxAttribute(parent) && COLOUR_ATTRIBUTES.includes(parent.name.getText());
   const isColourProperty = ts.isPropertyAssignment(parent) && COLOUR_ATTRIBUTES.includes(parent.name.getText());

   return isColourAttribute || isColourProperty;
}

function tsxOffenders(file: string, text: string) {
   const offenders: string[] = [];
   const source = ts.createSourceFile(file, text, ts.ScriptTarget.Latest, true, file.endsWith(".tsx") ? ts.ScriptKind.TSX : ts.ScriptKind.TS);
   const styleIdentifiers = new Set<string>();
   const objectInitialisers = new Map<string, ts.ObjectLiteralExpression>();
   const constantInitialisers = new Map<string, ts.Expression>();

   function collectConstants(node: ts.Node) {
      const isNamedDeclaration = ts.isVariableDeclaration(node) && ts.isIdentifier(node.name) && node.initializer !== undefined;

      if (isNamedDeclaration) {
         const declaration = node as ts.VariableDeclaration;

         constantInitialisers.set((declaration.name as ts.Identifier).text, declaration.initializer!);
      }

      ts.forEachChild(node, collectConstants);
   }

   function where(node: ts.Node) {
      const { line } = source.getLineAndCharacterOfPosition(node.getStart());

      return `${file}:${line + 1}`;
   }

   /* A style value may be a token string, a keyword, a conditional between those, or a constant in
      the same file that holds one. */
   function holdsOnlyTokens(value: ts.Expression): boolean {
      const isKeywordString = ts.isStringLiteral(value) && /^[a-z-]+$/.test(value.text);

      if (isTokenString(value) || isKeywordString) {
         return true;
      }

      if (ts.isParenthesizedExpression(value)) {
         return holdsOnlyTokens(value.expression);
      }

      if (ts.isConditionalExpression(value)) {
         return holdsOnlyTokens(value.whenTrue) && holdsOnlyTokens(value.whenFalse);
      }

      if (ts.isIdentifier(value)) {
         const initialiser = constantInitialisers.get(value.text);

         return initialiser !== undefined && holdsOnlyTokens(initialiser);
      }

      return false;
   }

   function checkStyleObject(object: ts.ObjectLiteralExpression) {
      for (const property of object.properties) {
         const isAssignment = ts.isPropertyAssignment(property);

         if (!isAssignment) {
            offenders.push(`${where(property)}: style object entry that is not a plain property`);
            continue;
         }

         const name = property.name.getText(source);
         const value = property.initializer;
         const literal = `style.${name}=${value.getText(source)}`;

         if (isExempt(file, literal)) {
            continue;
         }

         const isAllowed = holdsOnlyTokens(value);

         if (!isAllowed) {
            offenders.push(`${where(property)}: ${literal}`);
         }
      }
   }

   function visit(node: ts.Node) {
      for (const piece of stringPieces(node)) {
         const hasColourLiteral = HEX_COLOUR.test(piece) || COLOUR_FUNCTION.test(piece);
         const isNamedColour = isInColourContext(node) && namesAColour(piece.trim());
         const lengthMatch = CSS_LENGTH_OR_DURATION.exec(piece);
         const length = lengthMatch === null ? null : `${lengthMatch[2]}${lengthMatch[3]}`;

         if (hasColourLiteral || isNamedColour) {
            offenders.push(`${where(node)}: colour literal ${JSON.stringify(piece)}`);
         }

         const isFlaggedLength = length !== null && !isExempt(file, length);

         if (isFlaggedLength) {
            offenders.push(`${where(node)}: length or duration literal ${JSON.stringify(piece)}`);
         }
      }

      if (ts.isVariableDeclaration(node) && ts.isIdentifier(node.name) && node.initializer !== undefined) {
         const isObject = ts.isObjectLiteralExpression(node.initializer);

         if (isObject) {
            objectInitialisers.set(node.name.text, node.initializer as ts.ObjectLiteralExpression);
         }
      }

      if (ts.isJsxAttribute(node)) {
         const name = node.name.getText(source);
         const element = node.parent.parent;
         const tagName = ts.isJsxOpeningElement(element) || ts.isJsxSelfClosingElement(element) ? element.tagName.getText(source) : "";
         const initializer = node.initializer;
         const expression = initializer !== undefined && ts.isJsxExpression(initializer) ? initializer.expression : initializer;
         const isDesignAttribute = DESIGN_ATTRIBUTES.includes(name);
         const isRenderedSize = (name === "width" || name === "height") && SIZED_ELEMENTS.includes(tagName);

         if (isDesignAttribute || isRenderedSize) {
            const holdsToken = expression !== undefined && isTokenString(expression);

            if (!holdsToken) {
               offenders.push(`${where(node)}: <${tagName} ${node.getText(source)}>`);
            }
         }

         if (name === "style" && expression !== undefined) {
            if (ts.isObjectLiteralExpression(expression)) {
               checkStyleObject(expression);
            } else if (ts.isIdentifier(expression)) {
               styleIdentifiers.add(expression.text);
            } else {
               offenders.push(`${where(node)}: style from an expression this scan cannot read`);
            }
         }
      }

      ts.forEachChild(node, visit);
   }

   collectConstants(source);
   visit(source);

   for (const identifier of styleIdentifiers) {
      const object = objectInitialisers.get(identifier);

      if (object === undefined) {
         offenders.push(`${file}: style={${identifier}} is not an object literal in the same file`);
         continue;
      }

      checkStyleObject(object);
   }

   return offenders;
}

function offendersIn(path: string) {
   const file = relative(SOURCE_ROOT, path);
   const text = readFileSync(path, "utf8");

   return file.endsWith(".css") ? cssOffenders(file, text) : tsxOffenders(file, text);
}

const FILES = sourceFiles(SOURCE_ROOT);

describe("test_no_literal_values", () => {
   it("scans every stylesheet and every component, and no test", () => {
      const names = FILES.map((path) => relative(SOURCE_ROOT, path));

      expect(names).toContain("styles/app.css");
      expect(names).toContain("styles/motion.css");
      expect(names).toContain("figures/FigureView.tsx");
      expect(names).toContain("progress/MasteryMap.tsx");
      expect(names.filter((name) => name.includes(".test."))).toEqual([]);
      expect(names.length).toBeGreaterThan(60);
   });

   it("finds no colour, size, spacing, line height, width or duration literal outside the token file", () => {
      const offenders = FILES.flatMap(offendersIn);

      expect(offenders).toEqual([]);
   });

   it("flags each kind of literal it exists to catch", () => {
      const probes: Array<[string, string]> = [
         ["probe.css", ".a { color: #123456; }"],
         ["probe.css", ".a { color: rebeccapurple; }"],
         ["probe.css", ".a { font-size: 14px; }"],
         ["probe.css", ".a { line-height: 1.5; }"],
         ["probe.css", ".a { padding: 12px; }"],
         ["probe.css", ".a { border: 1px solid var(--growth-border-hairline); }"],
         ["probe.css", ".a { transition: opacity 200ms ease-out; }"],
         ["probe.tsx", "const a = <p style={{ color: \"red\" }} />;"],
         ["probe.tsx", "const a = <p style={{ maxWidth: 480 }} />;"],
         ["probe.tsx", "const s = { border: \"1px solid var(--growth-border-hairline)\" };\nconst a = <p style={s} />;"],
         ["probe.tsx", "const a = <line strokeWidth={2} />;"],
         ["probe.tsx", "const WIDTH = 2;\nconst a = <line strokeWidth={WIDTH} />;"],
         ["probe.tsx", "const a = <circle r={4} />;"],
         ["probe.tsx", "const a = <svg width={16} />;"],
         ["probe.tsx", "const a = <text fontSize=\"12\" />;"],
         ["probe.ts", "export const DURATION = \"150ms\";"],
         ["probe.ts", "export const INK = \"#fff\";"]
      ];

      for (const [file, text] of probes) {
         const offenders = file.endsWith(".css") ? cssOffenders(file, text) : tsxOffenders(file, text);

         expect(offenders.length, `${text} passed the scan`).toBeGreaterThan(0);
      }

      const clean = [
         cssOffenders("probe.css", ".a { padding: calc(var(--growth-space-4) / 2) 0; max-width: 68ch; }"),
         tsxOffenders("probe.tsx", "const a = <line x1={3} y2={13} stroke=\"var(--growth-text-muted)\" className=\"chart-axis\" />;"),
         tsxOffenders("probe.tsx", "const a = <p style={{ color: \"var(--growth-state-correct)\" }} />;")
      ];

      expect(clean).toEqual([[], [], []]);
   });

   it("keeps each exemption bound to a file that still carries it", () => {
      for (const exemption of EXEMPTIONS) {
         const text = readFileSync(join(SOURCE_ROOT, exemption.file), "utf8");
         const literal = exemption.literal.replace(/^style\.[a-zA-Z]+=/, "");

         expect(text, `${exemption.file} no longer carries ${exemption.literal}: ${exemption.reason}`).toContain(literal);
      }

      const motionCss = readFileSync(join(SOURCE_ROOT, "styles", "motion.css"), "utf8").replace(/\/\*[\s\S]*?\*\//g, " ");
      const durations = motionCss.match(/\b\d+(?:\.\d+)?m?s\b/g) ?? [];

      expect(durations.length).toBeGreaterThan(0);
      expect(new Set(durations)).toEqual(new Set([MOTION_DURATION_TOKEN]));
   });
});
