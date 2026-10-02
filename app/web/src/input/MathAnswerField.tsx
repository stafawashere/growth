import { useState } from "react";

import { MathField, type MathFieldProps } from "./MathField";

export const LATEX_INSPECTOR_LABEL = "raw LaTeX";

/* A MathField with 08's raw LaTeX inspector beneath it, which shows the student what they typed as
   plain LaTeX: text-secondary on surface-sunken in type-mono, with no syntax colouring. It is read
   in place after its visible label and is never focusable, so it adds no stop to the tab order and
   takes no key a shortcut listens for. It is dropped when the math keyboard failed to load, since
   the field then takes nothing. */
export function MathAnswerField(props: MathFieldProps) {
   const { initialLatex, onLatexChange, onLoadFailure } = props;
   const [latex, setLatex] = useState(initialLatex ?? "");
   const [keyboardFailed, setKeyboardFailed] = useState(false);

   function showLatex(typed: string) {
      setLatex(typed);
      onLatexChange?.(typed);
   }

   function failed(reason: unknown) {
      setKeyboardFailed(true);
      onLoadFailure(reason);
   }

   const isEmpty = latex.trim().length === 0;

   return (
      <>
         <MathField {...props} onLatexChange={showLatex} onLoadFailure={failed} />

         {keyboardFailed ? null : (
            <p className="latex-inspector" data-testid="latex-inspector" data-empty={isEmpty ? "true" : undefined}>
               <span className="latex-inspector-label">{LATEX_INSPECTOR_LABEL}: </span>
               <code>{latex}</code>
            </p>
         )}
      </>
   );
}
