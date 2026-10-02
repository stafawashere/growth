import type { ReactNode } from "react";

import { Icon } from "../ui/Icon";

/* The step control at the foot of an assessment sheet: Back and Next joined as one pair, then a
   mark for every question in the set, so the student can see where they are and what is still
   open without leaving the question. The marks are read by eye only; the header carries the
   position in words and the question menu, where a part offers one, carries the jump. */

export type StepperMarkState = "current" | "answered" | "open";

export interface StepperMark {
   state: StepperMarkState;
   marked: boolean;
}

export interface QuestionStepperProps {
   marks: ReadonlyArray<StepperMark>;
   isFirst: boolean;
   isLast: boolean;
   onBack: () => void;
   onNext: () => void;
   caption?: ReactNode;
}

export function stepperState(isCurrent: boolean, isAnswered: boolean): StepperMarkState {
   if (isCurrent) {
      return "current";
   }

   return isAnswered ? "answered" : "open";
}

export function QuestionStepper({ marks, isFirst, isLast, onBack, onNext, caption }: QuestionStepperProps) {
   const hasCaption = caption !== undefined && caption !== null;

   return (
      <div className="sheet-nav" data-testid="question-stepper">
         <div className="sheet-nav-pair">
            <button type="button" className="sheet-nav-step motion-instant-question-move" disabled={isFirst} onClick={onBack}>
               <Icon name="back" />
               <span>Back</span>
            </button>

            <button type="button" className="sheet-nav-step motion-instant-question-move" disabled={isLast} onClick={onNext}>
               <span>Next</span>
               <Icon name="next" />
            </button>
         </div>

         <div className="sheet-nav-index">
            <ol className="sheet-nav-marks" aria-hidden="true">
               {marks.map((mark, index) => (
                  <li key={index} className="sheet-nav-mark" data-state={mark.state} data-marked={mark.marked ? "true" : undefined} />
               ))}
            </ol>

            {hasCaption ? <p className="helper sheet-nav-caption">{caption}</p> : null}
         </div>
      </div>
   );
}
