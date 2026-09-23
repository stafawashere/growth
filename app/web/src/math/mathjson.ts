/* MathLive ships convertMathJsonToLatex and convertLatexToAsciiMath as pure, DOM-free
   conversions (dist/types/mathlive-ssr.d.ts), but the LaTeX conversion needs the compute
   engine's parser loaded first or it renders nothing. mathlive treats that engine as optional
   and only reaches for it lazily, so the side-effecting import below registers it before any
   conversion runs. */
import "@cortex-js/compute-engine";
import { convertLatexToAsciiMath, convertMathJsonToLatex } from "mathlive";
import katex from "katex";

const INLINE_MATH = /\\\(([\s\S]*?)\\\)/g;

export function mathJsonToLatex(node: unknown): string {
   if (node === null || node === undefined) {
      return "";
   }

   try {
      return convertMathJsonToLatex(node as Parameters<typeof convertMathJsonToLatex>[0]);
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
         output: "htmlAndMathml",
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
}

export type TextOrMathSegment = TextSegment | MathSegment;

/* Curated stems and worked steps carry inline math delimited \( like this \), plain LaTeX with
   no leading $ or $$. Agent-drafted items carry no delimiters at all, so a text with none of
   these splits into the single plain segment it already was. */
export function splitInlineMath(text: string): TextOrMathSegment[] {
   const segments: TextOrMathSegment[] = [];
   let cursor = 0;

   for (const match of text.matchAll(INLINE_MATH)) {
      const matchIndex = match.index ?? 0;
      const before = text.slice(cursor, matchIndex);

      if (before.length > 0) {
         segments.push({ kind: "text", text: before });
      }

      segments.push({ kind: "math", latex: match[1] });
      cursor = matchIndex + match[0].length;
   }

   const remainder = text.slice(cursor);

   if (remainder.length > 0 || segments.length === 0) {
      segments.push({ kind: "text", text: remainder });
   }

   return segments;
}
