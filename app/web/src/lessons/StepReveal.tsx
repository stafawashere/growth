import { useEffect, useState, type ReactNode } from "react";

/* 15 UI and TEMPLATE.md Delivery, step_reveal: one step at a time on "Next step", the earlier steps
   staying in view, each step's why line beside it rather than below the whole solution (01 split
   attention). Shown in full when the reader asks for every step at once, as a refresher does or as
   the reader's "Show all steps" does; onRemainingChange tells the reader whether steps are left. */

export interface RevealStep {
   key: string;
   main: ReactNode;
   beside?: ReactNode;
}

export interface StepRevealProps {
   steps: RevealStep[];
   revealAll?: boolean;
   className?: string;
   onRemainingChange?: (hasMore: boolean) => void;
}

export function StepReveal(props: StepRevealProps) {
   const { steps, revealAll = false, onRemainingChange } = props;
   const [shown, setShown] = useState(1);
   const visible = revealAll ? steps.length : Math.min(shown, steps.length);
   const hasMore = visible < steps.length;

   useEffect(() => {
      onRemainingChange?.(hasMore);
   }, [hasMore, onRemainingChange]);

   return (
      <>
         <ol className={props.className ?? "lesson-steps"} data-testid="lesson-steps">
            {steps.slice(0, visible).map((step) => (
               <li key={step.key} data-testid="lesson-step">
                  <div className="lesson-step-row">
                     <div data-testid="lesson-step-cue">{step.main}</div>
                     {step.beside !== undefined ? (
                        <div className="lesson-step-why" data-testid="lesson-step-why">
                           {step.beside}
                        </div>
                     ) : null}
                  </div>
               </li>
            ))}
         </ol>

         {hasMore ? (
            <button type="button" className="text-button" data-testid="lesson-next-step" onClick={() => setShown(visible + 1)}>
               Next step
            </button>
         ) : null}
      </>
   );
}
