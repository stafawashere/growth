import { latexToAccessibleText, renderLatexToMarkup, splitInlineMath } from "./mathjson";

export interface MathTextProps {
   text: string;
}

/* Stems and worked-solution steps are plain text that may carry LaTeX delimited \( like this \)
   (app/items/ingest.py records, e.g. tests/fixtures/items_p1). Agent-drafted items carry no
   delimiters at all, so this renders exactly the plain text it always did for them.

   KaTeX writes each formula twice, as MathML that a screen reader reads as structure and as HTML
   for the eye that KaTeX itself marks aria-hidden, so the markup goes in whole and nothing else
   reads the formula a second time. A formula KaTeX cannot render falls back to its ASCII reading. */
export function MathText({ text }: MathTextProps) {
   const segments = splitInlineMath(text);

   return (
      <>
         {segments.map((segment, index) => {
            if (segment.kind === "text") {
               return <span key={index}>{segment.text}</span>;
            }

            const markup = renderLatexToMarkup(segment.latex);
            const isRendered = markup !== "";

            if (!isRendered) {
               return <span key={index}>{latexToAccessibleText(segment.latex)}</span>;
            }

            return <span key={index} dangerouslySetInnerHTML={{ __html: markup }} />;
         })}
      </>
   );
}
