import type { Confidence, ServedItem } from "../api/types";
import { MathField } from "../input/MathField";
import { McqControl } from "../input/McqControl";
import { ConfidencePrompt } from "./ConfidencePrompt";
import { SelfExplanationPrompt } from "./SelfExplanationPrompt";

/* The server withholds the worked solution until an answer is submitted (app/runtime/bank.py
   _as_item_dict), so a ServedItem carries a stem and no steps. The example and completion stages
   cannot be drawn without them, so the caller passes them in and there is no default: an Item
   built without them says so on screen rather than showing a stage it cannot show. */

export interface WorkedStep {
   index: number;
   text: string;
}

/* 11 P1 scope item 8: the completion stage requires the two step minimum in its Q16. */
export const MINIMUM_COMPLETION_STEPS = 2;

export const COMMIT_LABEL = "Check my answer";

export const EXAMPLE_LABEL = "I have explained this";

export const WORKED_STEPS_MISSING =
   "The worked steps for this problem have not reached me, so I cannot work through it yet.";

export const ANSWER_UNAVAILABLE =
   "The math keyboard did not load, so this problem cannot take my answer. Nothing I type here would be saved.";

/* app/session/service.py collects_confidence: a rating belongs to completion and unsupported and
   never to example, which commits no answer to be confident about (11 implementer decision 3). */
export function collectsConfidence(stage: ServedItem["stage"]) {
   return stage !== "example";
}

export interface ItemProps {
   item: ServedItem;
   workedSteps: WorkedStep[];
   selfExplanationPrompt: string | null;
   onAnswerChange: (mathjson: unknown) => void;
   answerUnavailable: boolean;
   onAnswerUnavailable: (reason: unknown) => void;
   selectedOptionId: string | null;
   onOptionChange: (optionId: string) => void;
   confidence: Confidence | null;
   onConfidenceChange: (confidence: Confidence) => void;
   selfExplanation: string;
   onSelfExplanationChange: (text: string) => void;
   onCommit: () => void;
   awaitingConfidence: boolean;
}

function requiredStepCount(stage: ServedItem["stage"]) {
   if (stage === "completion") {
      return MINIMUM_COMPLETION_STEPS;
   }

   return 1;
}

export function Item(props: ItemProps) {
   const {
      item,
      workedSteps,
      selfExplanationPrompt,
      onAnswerChange,
      answerUnavailable,
      onAnswerUnavailable,
      selectedOptionId,
      onOptionChange,
      confidence,
      onConfidenceChange,
      selfExplanation,
      onSelfExplanationChange,
      onCommit,
      awaitingConfidence
   } = props;

   const handlesAnswerUnavailable = typeof onAnswerUnavailable === "function";

   if (!handlesAnswerUnavailable) {
      throw new Error(
         "Item needs an onAnswerUnavailable handler: a problem whose math field never loads takes no answer"
      );
   }

   const isExample = item.stage === "example";
   const isCompletion = item.stage === "completion";
   const needsWorkedSteps = isExample || isCompletion;
   const hasEnoughSteps = workedSteps.length >= requiredStepCount(item.stage);
   const canDrawStage = !needsWorkedSteps || hasEnoughSteps;

   const shownSteps = isCompletion ? workedSteps.slice(0, -1) : workedSteps;
   const blankedStep = isCompletion ? workedSteps[workedSteps.length - 1] : null;

   const servesMcq = item.format === "mcq" && item.stage === "unsupported";
   const collectsAnswer = !isExample;
   const commitLabel = isExample ? EXAMPLE_LABEL : COMMIT_LABEL;

   const takesNoAnswer = collectsAnswer && !servesMcq && answerUnavailable;
   const isCommitted = awaitingConfidence;
   const showsAnswerArea = canDrawStage && collectsAnswer && !isCommitted;
   const asksForConfidence = canDrawStage && collectsConfidence(item.stage) && !takesNoAnswer;
   const asksToCommit = canDrawStage && !takesNoAnswer && !isCommitted;

   return (
      <article data-testid="item" data-stage={item.stage}>
         <p data-testid="item-stem">{item.stem}</p>

         {needsWorkedSteps && !canDrawStage ? (
            <p data-testid="worked-steps-unavailable">{WORKED_STEPS_MISSING}</p>
         ) : null}

         {needsWorkedSteps && canDrawStage ? (
            <ol data-testid="worked-steps">
               {shownSteps.map((step) => (
                  <li key={step.index} data-step-index={step.index}>
                     {step.text}
                  </li>
               ))}

               {blankedStep !== null ? (
                  <li data-testid="blanked-step" data-step-index={blankedStep.index}>
                     This step is mine to write.
                  </li>
               ) : null}
            </ol>
         ) : null}

         {showsAnswerArea ? (
            <div>
               {servesMcq ? (
                  <div data-testid="mcq-answer">
                     <McqControl
                        groupLabel="My answer"
                        options={item.options ?? []}
                        selectedId={selectedOptionId}
                        onSelect={onOptionChange}
                     />
                  </div>
               ) : (
                  <div data-testid="math-answer">
                     <MathField
                        label="My answer"
                        onChange={onAnswerChange}
                        onLoadFailure={onAnswerUnavailable}
                     />

                     {takesNoAnswer ? (
                        <p data-testid="answer-unavailable">{ANSWER_UNAVAILABLE}</p>
                     ) : null}
                  </div>
               )}
            </div>
         ) : null}

         {canDrawStage && isExample ? (
            <SelfExplanationPrompt
               prompt={selfExplanationPrompt}
               value={selfExplanation}
               onChange={onSelfExplanationChange}
            />
         ) : null}

         {asksForConfidence ? (
            <ConfidencePrompt value={confidence} onChange={onConfidenceChange} />
         ) : null}

         {asksToCommit ? (
            <button type="button" className="motion-instant-submit-answer" onClick={onCommit}>
               {commitLabel}
            </button>
         ) : null}
      </article>
   );
}