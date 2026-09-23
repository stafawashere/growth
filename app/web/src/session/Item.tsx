import type { Confidence, ServedItem, ServedStep } from "../api/types";
import { MathField } from "../input/MathField";
import { McqControl } from "../input/McqControl";
import { ConfidencePrompt } from "./ConfidencePrompt";
import { SelfExplanationPrompt } from "./SelfExplanationPrompt";

/* GET /sessions/{id}/next carries the steps a stage shows as served_steps (app/runtime/bank.py
   served_steps): every step at example, every step but the last at completion, none at
   unsupported. The blank at completion is the step after the last one served, and the server
   never sends its text. An item whose steps did not arrive says so rather than drawing a stage it
   cannot show. */

/* 11 P1 scope item 8: the completion stage requires the two step minimum in its Q16. That counts
   the whole worked solution, and the served list is that solution less its blanked last step.
   Stage example now blanks the same way (BUILD-LEDGER.md, "Decisions taken on the operator's
   instruction, 2026-09-23": implementer decision 3 is withdrawn, and example collects a graded
   answer), so the two stages share the minimum. */
export const MINIMUM_COMPLETION_STEPS = 2;

const BLANKED_AT_COMPLETION = 1;

export const COMMIT_LABEL = "Check my answer";

export const WORKED_STEPS_MISSING =
   "The worked steps for this problem have not reached me, so I cannot work through it yet.";

export const ANSWER_UNAVAILABLE =
   "The math keyboard did not load, so this problem cannot take my answer. Nothing I type here would be saved.";

/* app/session/service.py collects_confidence: a rating is collected before feedback on every
   stage, example included. 11 implementer decision 3, which carved example out because it
   committed no answer, is withdrawn (BUILD-LEDGER.md, "Decisions taken on the operator's
   instruction, 2026-09-23"): example now commits a graded answer like any other stage. */
export function collectsConfidence(_stage: ServedItem["stage"]) {
   return true;
}

export interface ItemProps {
   item: ServedItem;
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

function requiredServedStepCount(stage: ServedItem["stage"]) {
   if (stage === "completion" || stage === "example") {
      return MINIMUM_COMPLETION_STEPS - BLANKED_AT_COMPLETION;
   }

   return 1;
}

function blankedStepAfter(shownSteps: ServedStep[]) {
   const lastShown = shownSteps[shownSteps.length - 1];

   return { index: lastShown.index + BLANKED_AT_COMPLETION };
}

export function Item(props: ItemProps) {
   const {
      item,
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
   const shownSteps = item.served_steps ?? [];
   const hasEnoughSteps = shownSteps.length >= requiredServedStepCount(item.stage);
   const canDrawStage = !needsWorkedSteps || hasEnoughSteps;

   const blanksAStep = (isCompletion || isExample) && hasEnoughSteps;
   const blankedStep = blanksAStep ? blankedStepAfter(shownSteps) : null;

   const servesMcq = item.format === "mcq" && item.stage === "unsupported";
   const collectsAnswer = true;
   const commitLabel = COMMIT_LABEL;

   const takesNoAnswer = collectsAnswer && !servesMcq && answerUnavailable;
   const isCommitted = awaitingConfidence;
   const showsAnswerArea = canDrawStage && collectsAnswer && !isCommitted;
   const asksForConfidence = canDrawStage && collectsConfidence(item.stage) && !takesNoAnswer;
   const asksToCommit = canDrawStage && !takesNoAnswer && !isCommitted;

   return (
      <article className="card item" data-testid="item" data-stage={item.stage}>
         <p className="item-stem" data-testid="item-stem">{item.stem}</p>

         {needsWorkedSteps && !canDrawStage ? (
            <p data-testid="worked-steps-unavailable">{WORKED_STEPS_MISSING}</p>
         ) : null}

         {needsWorkedSteps && canDrawStage ? (
            <ol className="worked-steps" data-testid="worked-steps">
               {shownSteps.map((step) => (
                  <li key={step.index} data-step-index={step.index}>
                     {step.text}
                  </li>
               ))}

               {blankedStep !== null ? (
                  <li className="blanked-step" data-testid="blanked-step" data-step-index={blankedStep.index}>
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
               prompt={item.self_explanation_prompt}
               value={selfExplanation}
               onChange={onSelfExplanationChange}
            />
         ) : null}

         {asksForConfidence ? (
            <ConfidencePrompt value={confidence} onChange={onConfidenceChange} />
         ) : null}

         {asksToCommit ? (
            <button type="button" className="motion-instant-submit-answer button-primary" onClick={onCommit}>
               {commitLabel}
            </button>
         ) : null}
      </article>
   );
}