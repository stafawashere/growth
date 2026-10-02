import type { MutableRefObject } from "react";
import type { Confidence, ServedItem, ServedStep } from "../api/types";
import { CalculatorLink } from "../calculator/CalculatorLink";
import { DesmosPanel } from "../input/DesmosPanel";
import { MathAnswerField } from "../input/MathAnswerField";
import type { MathFieldReader } from "../input/MathField";
import { FigureView } from "../figures/FigureView";
import { McqControl } from "../input/McqControl";
import { Workbench } from "../ui/Workbench";
import { MathText } from "../math/MathText";
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

export const OPENER_NOTE = "Try this before the method is shown.";

export const ANSWER_UNAVAILABLE =
   "The math keyboard did not load, so this problem cannot take my answer. Nothing I type here would be saved.";

/* app/session/service.py collects_confidence: a rating is collected before feedback on every
   stage, example included. 11 implementer decision 3, which carved example out because it
   committed no answer, is withdrawn (BUILD-LEDGER.md, "Decisions taken on the operator's
   instruction, 2026-09-23"): example now commits a graded answer like any other stage. */
export function collectsConfidence(_stage: ServedItem["stage"]) {
   return true;
}

/* A statement-keyed item has nothing to type, so the server marks it and it is a choice at every
   stage (app/engine/select.py requires_choice); any other multiple-choice item is a choice only
   once it is unsupported. The screen that shows the options and the commit that sends the answer
   both read this, so they cannot disagree. */
export function servesChoice(item: ServedItem) {
   const isAlwaysAChoice = item.requires_choice === true;
   const isMultipleChoice = item.format === "mcq";
   const isUnsupported = item.stage === "unsupported";

   return isMultipleChoice && (isUnsupported || isAlwaysAChoice);
}

/* The keys SessionScreen answers an item with, said beside the button so they can be found. */
export function keyHint(offersOptions: boolean) {
   const optionKeys = offersOptions ? " A, B, C and D pick an option." : "";

   return `Enter checks your answer.${optionKeys}`;
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
   asksConfidence?: boolean;
   onConfidenceClose?: () => void;
   mathReaderRef?: MutableRefObject<MathFieldReader | null>;
   onMathFieldReady?: () => void;
   commitDisabled?: boolean;
}

/* The foot's word for a rating the student gave from the keys before checking, since the dialog
   that would show it is not open. */
export function ratedSentence(confidence: Confidence) {
   return `Rated ${confidence}.`;
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
      awaitingConfidence,
      asksConfidence = false,
      onConfidenceClose,
      mathReaderRef,
      onMathFieldReady,
      commitDisabled = false
   } = props;

   const handlesAnswerUnavailable = typeof onAnswerUnavailable === "function";

   if (!handlesAnswerUnavailable) {
      throw new Error(
         "Item needs an onAnswerUnavailable handler: a problem whose math field never loads takes no answer"
      );
   }

   const isOpener = item.is_opener === true;
   const isExample = item.stage === "example";
   const isCompletion = item.stage === "completion";
   const needsWorkedSteps = isExample || isCompletion;
   const shownSteps = item.served_steps ?? [];
   const hasEnoughSteps = shownSteps.length >= requiredServedStepCount(item.stage);
   const canDrawStage = !needsWorkedSteps || hasEnoughSteps;

   const blanksAStep = (isCompletion || isExample) && hasEnoughSteps;
   const blankedStep = blanksAStep ? blankedStepAfter(shownSteps) : null;

   const hasFigure = item.figure_spec !== null && item.figure_spec !== undefined;
   const allowsCalculator = item.calculator_status === "calculator";

   const servesMcq = servesChoice(item);
   const collectsAnswer = true;
   const commitLabel = COMMIT_LABEL;

   const takesNoAnswer = collectsAnswer && !servesMcq && answerUnavailable;
   const isCommitted = awaitingConfidence;
   const showsAnswerArea = canDrawStage && collectsAnswer && !isCommitted;
   const collectsRating = canDrawStage && collectsConfidence(item.stage) && !takesNoAnswer;
   const opensRatingDialog = collectsRating && (isCommitted || asksConfidence);
   const ratingCanClose = !isCommitted;
   const asksToCommit = canDrawStage && !takesNoAnswer && !isCommitted;
   const showsRated = asksToCommit && collectsRating && confidence !== null;

   const promptKind = servesMcq ? "Concept check" : "Solve";

   const explanationPrompt = item.self_explanation_prompt;
   const hasExplanationPrompt = explanationPrompt !== null && explanationPrompt.trim().length > 0;
   const asksToExplain = canDrawStage && isExample && hasExplanationPrompt;

   const stem = (
      <>
         <div className="bench-part">
            <p className="bench-tag">{promptKind}</p>

            <div className="question-stem">
               {isOpener ? (
                  <p className="caption" data-testid="opener-note">
                     {OPENER_NOTE}
                  </p>
               ) : null}

               <p className="item-stem" data-testid="item-stem" data-agent-anchor="stem">
                  <MathText text={item.stem} />
               </p>

               {hasFigure ? <FigureView spec={item.figure_spec} isItemFigure /> : null}

               {allowsCalculator ? <DesmosPanel beside={<CalculatorLink />} /> : null}
            </div>
         </div>

         {needsWorkedSteps && !canDrawStage ? (
            <p className="callout" data-testid="worked-steps-unavailable">
               {WORKED_STEPS_MISSING}
            </p>
         ) : null}

         {needsWorkedSteps && canDrawStage ? (
            <div className="bench-part">
               <p className="bench-tag">Worked so far</p>

               <ol className="worked-steps" data-testid="worked-steps">
                  {shownSteps.map((step) => (
                     <li key={step.index} data-step-index={step.index}>
                        <MathText text={step.text} />
                     </li>
                  ))}

                  {blankedStep !== null ? (
                     <li className="blanked-step" data-testid="blanked-step" data-step-index={blankedStep.index}>
                        This step is mine to write.
                     </li>
                  ) : null}
               </ol>
            </div>
         ) : null}
      </>
   );

   const work = showsAnswerArea ? (
      <>
         <p className="bench-tag" aria-hidden="true">
            My answer
         </p>

         {servesMcq ? (
            <div className="bench-answer" data-testid="mcq-answer">
               <McqControl
                  groupLabel="My answer"
                  options={item.options ?? []}
                  selectedId={selectedOptionId}
                  onSelect={onOptionChange}
                  anchorsOptions
               />
            </div>
         ) : (
            <div className="bench-answer" data-testid="math-answer">
               <MathAnswerField
                  label="My answer"
                  onChange={onAnswerChange}
                  onLoadFailure={onAnswerUnavailable}
                  readerRef={mathReaderRef}
                  onReady={onMathFieldReady}
               />

               {takesNoAnswer ? <p data-testid="answer-unavailable">{ANSWER_UNAVAILABLE}</p> : null}
            </div>
         )}

         {asksToExplain ? (
            <SelfExplanationPrompt prompt={explanationPrompt} value={selfExplanation} onChange={onSelfExplanationChange} />
         ) : null}
      </>
   ) : null;

   const foot = asksToCommit ? (
      <button type="button" className="motion-instant-submit-answer button-primary" disabled={commitDisabled} onClick={onCommit}>
         {commitLabel}
      </button>
   ) : null;

   const status = asksToCommit ? (
      <>
         <p className="key-hint" data-testid="key-hint">
            {keyHint(servesMcq)}
         </p>

         {showsRated ? (
            <p className="rated-note" data-testid="rated-confidence">
               {ratedSentence(confidence as Confidence)}
            </p>
         ) : null}
      </>
   ) : null;

   return (
      <Workbench
         testId="item"
         data={{ "data-stage": item.stage }}
         stem={stem}
         work={work}
         foot={foot}
         status={status}
         after={
            opensRatingDialog ? (
               <ConfidencePrompt value={confidence} onChange={onConfidenceChange} onClose={ratingCanClose ? onConfidenceClose : undefined} />
            ) : null
         }
      />
   );
}