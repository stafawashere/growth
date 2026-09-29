import { latexToAccessibleText, renderLatexToMarkup, splitInlineMath, type TextOrMathSegment } from "./mathjson";

export interface MathTextProps {
   text: string;
}

/* Stems and worked-solution steps are plain text that may carry LaTeX delimited \( like this \)
   (app/items/ingest.py records, e.g. tests/fixtures/items_p1). Agent-drafted items carry no
   delimiters at all, so this renders exactly the plain text it always did for them.

   KaTeX writes each formula twice, as MathML that a screen reader reads as structure and as HTML
   for the eye that KaTeX itself marks aria-hidden, so the markup goes in whole and nothing else
   reads the formula a second time. A formula KaTeX cannot render falls back to its ASCII reading.

   A formula too long to sit in a sentence without wrapping mid-expression gets a line of its own,
   and the punctuation that closes the sentence goes with it so it is not stranded below. */
export function MathText({ text }: MathTextProps) {
   const segments = displayLongFormulas(splitInlineMath(text));

   return (
      <>
         {segments.map((segment, index) => {
            if (segment.kind === "text") {
               return <span key={index}>{segment.text}</span>;
            }

            const markup = renderLatexToMarkup(segment.latex, segment.isDisplayed);
            const isRendered = markup !== "";

            if (!isRendered) {
               return <span key={index}>{latexToAccessibleText(segment.latex)}</span>;
            }

            return <span key={index} dangerouslySetInnerHTML={{ __html: markup }} />;
         })}
      </>
   );
}

const LONGEST_INLINE_LATEX = 60;

const CLOSING_PUNCTUATION = /^[.,;:]/;

type PlacedSegment = { kind: "text"; text: string } | { kind: "math"; latex: string; isDisplayed: boolean };

function displayLongFormulas(segments: TextOrMathSegment[]): PlacedSegment[] {
   const placed: PlacedSegment[] = [];

   for (const segment of segments) {
      if (segment.kind === "math") {
         const isDisplayed = segment.latex.length > LONGEST_INLINE_LATEX;
         placed.push({ ...segment, isDisplayed });
         continue;
      }

      const previous = placed[placed.length - 1];
      const followsDisplayedMath = previous?.kind === "math" && previous.isDisplayed;
      const punctuation = segment.text.match(CLOSING_PUNCTUATION)?.[0];
      const shouldCarryPunctuation = followsDisplayedMath && punctuation !== undefined;

      if (shouldCarryPunctuation) {
         previous.latex = `${previous.latex}${punctuation}`;
         const rest = segment.text.slice(1);

         if (rest.trim().length > 0) {
            placed.push({ kind: "text", text: rest });
         }

         continue;
      }

      placed.push(segment);
   }

   return placed;
}
