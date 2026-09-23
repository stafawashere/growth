import { latexToAccessibleText, renderLatexToMarkup, splitInlineMath } from "./mathjson";

export interface MathTextProps {
   text: string;
}

/* Stems and worked-solution steps are plain text that may carry LaTeX delimited \( like this \)
   (app/items/ingest.py records, e.g. tests/fixtures/items_p1). Agent-drafted items carry no
   delimiters at all, so this renders exactly the plain text it always did for them. */
export function MathText({ text }: MathTextProps) {
   const segments = splitInlineMath(text);

   return (
      <>
         {segments.map((segment, index) => {
            if (segment.kind === "text") {
               return <span key={index}>{segment.text}</span>;
            }

            const markup = renderLatexToMarkup(segment.latex);
            const accessibleText = latexToAccessibleText(segment.latex);

            return (
               <span key={index}>
                  <span aria-hidden="true" dangerouslySetInnerHTML={{ __html: markup }} />
                  <span className="visually-hidden">{accessibleText}</span>
               </span>
            );
         })}
      </>
   );
}
