import type { ReactNode } from "react";
import type { ComparisonPayload } from "../api/types";
import { MathText } from "../math/MathText";

export const COMPARISON_LABEL = "Comparison";

export const METHOD_LABEL = "The method";

export interface ComparisonPanelProps {
   comparison: ComparisonPayload;
   attempt: ReactNode;
}

/* 01's obligatory comparison step after an opener: the attempt and the canonical worked solution
   side by side, under the one line the server built from the archetype and its error record. */
export function ComparisonPanel({ comparison, attempt }: ComparisonPanelProps) {
   return (
      <section className="comparison" data-testid="comparison-panel">
         <p className="eyebrow">{COMPARISON_LABEL}</p>

         <p data-testid="comparison-label">{comparison.label}</p>

         <div className="comparison-grid">
            <div data-testid="comparison-attempt">{attempt}</div>

            <div data-testid="comparison-method">
               <p className="eyebrow">{METHOD_LABEL}</p>

               <ol className="worked-steps">
                  {comparison.worked_steps.map((step) => (
                     <li key={step.index} data-step-index={step.index}>
                        <MathText text={step.text} />
                     </li>
                  ))}
               </ol>
            </div>
         </div>
      </section>
   );
}
