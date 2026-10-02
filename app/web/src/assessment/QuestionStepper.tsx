import { Icon } from "../ui/Icon";

/* Back and Next at the foot of the answer pane. Where the student stands in the set is drawn on the
   connected bar over the card (ui/Workbench.tsx QuestionTrack), and the question menu, where a part
   offers one, carries the jump. */

export interface QuestionStepperProps {
   isFirst: boolean;
   isLast: boolean;
   onBack: () => void;
   onNext: () => void;
}

export function QuestionStepper({ isFirst, isLast, onBack, onNext }: QuestionStepperProps) {
   return (
      <div className="step-pair" data-testid="question-stepper">
         <button type="button" className="button-secondary motion-instant-question-move" disabled={isFirst} onClick={onBack}>
            <Icon name="back" />
            Back
         </button>

         <button type="button" className="button-primary motion-instant-question-move" disabled={isLast} onClick={onNext}>
            Next
            <Icon name="next" />
         </button>
      </div>
   );
}
