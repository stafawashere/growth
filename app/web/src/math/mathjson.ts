/* MathLive ships convertMathJsonToLatex and convertLatexToAsciiMath as pure, DOM-free
   conversions (dist/types/mathlive-ssr.d.ts), but the LaTeX conversion needs the compute
   engine's parser loaded first or it renders nothing. mathlive treats that engine as optional
   and only reaches for it lazily, so the side-effecting import below registers it before any
   conversion runs. */
import "@cortex-js/compute-engine";
import { convertLatexToAsciiMath, convertMathJsonToLatex } from "mathlive";
import katex from "katex";

const DELIMITED_MATH = /\\\(([\s\S]*?)\\\)|\\\[([\s\S]*?)\\\]/g;

const OPENING_DELIMITER = /\\[([]/g;

const CLOSING_FOR: Record<string, string> = { "\\(": "\\)", "\\[": "\\]" };

/* compute-engine writes the constant e as its own \exponentialE, which KaTeX renders as an error. */
const COMPUTE_ENGINE_E = /\\exponentialE(?![a-zA-Z])/g;

/* Inline math would otherwise set the limit's subscript beside lim, as textbooks never do. */
const STACKED_LIMIT_MACROS = {
   "\\lim": "\\mathop{\\mathrm{lim}}\\limits"
};

export function mathJsonToLatex(node: unknown): string {
   if (node === null || node === undefined) {
      return "";
   }

   try {
      const latex = convertMathJsonToLatex(node as Parameters<typeof convertMathJsonToLatex>[0]);

      return latex.replace(COMPUTE_ENGINE_E, "\\mathrm{e}");
   } catch {
      return "";
   }
}

export function latexToAccessibleText(latex: string): string {
   const hasLatex = latex.trim().length > 0;

   if (!hasLatex) {
      return "";
   }

   try {
      return convertLatexToAsciiMath(latex);
   } catch {
      return latex;
   }
}

export function renderLatexToMarkup(latex: string, displayMode = false): string {
   try {
      return katex.renderToString(latex, {
         throwOnError: false,
         errorColor: "var(--growth-text-primary)",
         output: "htmlAndMathml",
         macros: { ...STACKED_LIMIT_MACROS },
         displayMode
      });
   } catch {
      return "";
   }
}

export interface TextSegment {
   kind: "text";
   text: string;
}

export interface MathSegment {
   kind: "math";
   latex: string;
   displayed?: true;
}

export type TextOrMathSegment = TextSegment | MathSegment;

/* Curated stems and worked steps carry inline math delimited \( like this \), plain LaTeX with
   no leading $ or $$. Agent-drafted items carry no delimiters at all, so a text with none of
   these splits into the single plain segment it already was. The live tutor also writes displayed
   math between \[ and \] (docs/agent/design.md, Streaming), which comes back marked displayed. */
export function splitInlineMath(text: string): TextOrMathSegment[] {
   const segments: TextOrMathSegment[] = [];
   let cursor = 0;

   for (const match of text.matchAll(DELIMITED_MATH)) {
      const matchIndex = match.index ?? 0;
      const before = text.slice(cursor, matchIndex);

      if (before.length > 0) {
         segments.push({ kind: "text", text: before });
      }

      const isDisplayed = match[2] !== undefined;

      segments.push(isDisplayed ? { kind: "math", latex: match[2], displayed: true } : { kind: "math", latex: match[1] });
      cursor = matchIndex + match[0].length;
   }

   const remainder = text.slice(cursor);

   if (remainder.length > 0 || segments.length === 0) {
      segments.push({ kind: "text", text: remainder });
   }

   return segments;
}

/* The tutor's replies are model output, so they are typeset with KaTeX's untrusted settings: no
   \href or \includegraphics (trust false), a small macro expansion budget that still covers the
   \lim macro, and a cap on sizes in ems. A formula KaTeX rejects comes back empty, so MathText
   shows its accessible reading and never KaTeX's error text. */
export const TUTOR_MAX_EXPAND = 100;

export const TUTOR_MAX_SIZE = 20;

export function renderTutorLatex(latex: string, displayMode = false): string {
   try {
      return katex.renderToString(latex, {
         throwOnError: true,
         trust: false,
         strict: "ignore",
         maxExpand: TUTOR_MAX_EXPAND,
         maxSize: TUTOR_MAX_SIZE,
         output: "htmlAndMathml",
         macros: { ...STACKED_LIMIT_MACROS },
         displayMode
      });
   } catch {
      return "";
   }
}

export interface HeldText {
   shown: string;
   held: string;
}

/* While a reply streams, a formula whose closing delimiter has not arrived would flash as raw
   LaTeX and then jump into typeset form, so everything from an unclosed \( or \[ on is held back
   until its closing delimiter arrives. */
export function holdUnclosedMath(text: string): HeldText {
   let cursor = 0;

   for (;;) {
      OPENING_DELIMITER.lastIndex = cursor;

      const opening = OPENING_DELIMITER.exec(text);

      if (opening === null) {
         return { shown: text, held: "" };
      }

      const closing = CLOSING_FOR[opening[0]];
      const closeAt = text.indexOf(closing, opening.index + opening[0].length);
      const isUnclosed = closeAt === -1;

      if (isUnclosed) {
         return { shown: text.slice(0, opening.index), held: text.slice(opening.index) };
      }

      cursor = closeAt + closing.length;
   }
}
