import { latexToAccessibleText, mathJsonToLatex, renderLatexToMarkup } from "./mathjson";

export interface MathValueProps {
   value: unknown;
   className?: string;
}

/* A served option's value is MathJSON, a bare number or symbol counting as the simplest case
   (app/runtime/bank.py STUDENT_OPTION_FIELDS). KaTeX's MathML half is what a screen reader reads,
   and its HTML half is already aria-hidden, the same as MathText. */
export function MathValue({ value, className }: MathValueProps) {
   const latex = mathJsonToLatex(value);
   const markup = renderLatexToMarkup(latex);
   const isRendered = markup !== "";

   if (!isRendered) {
      return <span className={className}>{latexToAccessibleText(latex)}</span>;
   }

   return <span className={className} dangerouslySetInnerHTML={{ __html: markup }} />;
}
