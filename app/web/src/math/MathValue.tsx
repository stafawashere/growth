import { latexToAccessibleText, mathJsonToLatex, renderLatexToMarkup } from "./mathjson";

export interface MathValueProps {
   value: unknown;
   className?: string;
}

/* A served option's value is MathJSON, a bare number or symbol counting as the simplest case
   (app/runtime/bank.py STUDENT_OPTION_FIELDS). Typeset math is decorative to a screen reader, so
   it stays aria-hidden and a plain-text rendering carries the accessible name instead. */
export function MathValue({ value, className }: MathValueProps) {
   const latex = mathJsonToLatex(value);
   const markup = renderLatexToMarkup(latex);
   const accessibleText = latexToAccessibleText(latex);

   return (
      <>
         <span className={className} aria-hidden="true" dangerouslySetInnerHTML={{ __html: markup }} />
         <span className="visually-hidden">{accessibleText}</span>
      </>
   );
}
