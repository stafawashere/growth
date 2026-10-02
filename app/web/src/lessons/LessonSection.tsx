import { useEffect, useState, type ReactNode } from "react";

import type { LessonContrast, LessonDelivery, LessonEventMode, LessonSection as LessonSectionRecord } from "../api/types";
import { CalculatorLink } from "../calculator/CalculatorLink";
import { LessonText } from "./LessonText";
import { MathValue } from "../math/MathValue";
import { CORRECT_GLYPH, INCORRECT_GLYPH } from "../session/StepMarks";
import { FigureControl } from "./FigureControl";
import { FrameStepper } from "./FrameStepper";
import { LessonFallback } from "./LessonFallback";
import { LessonFigure } from "./LessonFigure";
import { anchorFragment } from "./LessonLink";
import { LessonPrediction, PromptField, PromptVerdictLine, type CommittedPrediction, type PromptAnswer } from "./LessonPrompts";
import { LessonTable } from "./LessonTable";
import { ModelTable } from "./ModelTable";
import { StepReveal, type RevealStep } from "./StepReveal";

/* One section of a lesson, switched on its type and, for the blocks that carry one, on its
   delivery mode (CONTRACT.md Reader; TEMPLATE.md Delivery). Strategy, the scoring checklist and a
   prerequisite bridge carry no delivery: the reader fixes their form. */

export const SECTION_HEADINGS: Record<LessonSectionRecord["type"], string> = {
   prediction: "Predict",
   orientation: "What a response shows",
   key_ideas: "Key idea",
   strategy: "Recognising the question",
   worked_example: "Worked example",
   what_a_reader_scores: "What a reader scores",
   common_error: "A common error",
   representations: "Reading the representation",
   prerequisite_bridge: "From earlier"
};

export const STRATEGY_LABELS = ["Cue", "First line", "Rival", "Separating feature"] as const;

export const WRONG_STEP_LABEL = "Wrong step";

export const RIGHT_STEP_LABEL = "Right step";

export const DRAWN_MODES = ["figure", "table", "motion", "interactive", "model"];

export const CONTRAST_THIS_HEADING = "This concept";

export const CONTRAST_NOT_THIS_HEADING = "Not this one";

/* The mode a view of this section is logged under (amendment A-D5): its delivery mode, or text
   for the blocks whose form the reader fixes. A prediction is logged as one, and a strategy block
   carrying the contrast pair as a contrast screen. */
export function sectionMode(section: LessonSectionRecord): LessonEventMode {
   if (section.type === "prediction") {
      return "prediction";
   }

   const isContrastScreen = section.type === "strategy" && section.contrast !== undefined;

   if (isContrastScreen) {
      return "contrast";
   }

   return section.delivery?.mode ?? "text";
}

export function DeliveryBlock({ delivery }: { delivery: LessonDelivery | undefined }) {
   if (delivery === undefined || !DRAWN_MODES.includes(delivery.mode)) {
      return null;
   }

   const { spec, fallback } = delivery;

   if (spec === undefined) {
      return <LessonFallback text={fallback} />;
   }

   const blocks: Record<string, JSX.Element> = {
      figure: <LessonFigure spec={spec} fallback={fallback} />,
      table: <LessonTable spec={spec} fallback={fallback} />,
      motion: <FrameStepper spec={spec} fallback={fallback} />,
      interactive: <FigureControl spec={spec} fallback={fallback} />,
      model: <ModelTable spec={spec} fallback={fallback} />
   };

   return (
      <div className="lesson-delivery" data-testid="lesson-delivery" data-mode={delivery.mode} data-agent-anchor="section_figure">
         {blocks[delivery.mode]}
      </div>
   );
}

function Prose({ text }: { text: string | undefined }) {
   return text === undefined ? null : (
      <p>
         <LessonText text={text} />
      </p>
   );
}

function hasExpression(value: unknown) {
   return value !== undefined && value !== null;
}

interface PromptContext {
   onPromptAnswer?: PromptAnswer;
   onStepsRemaining?: (hasMore: boolean) => void;
   now?: () => number;
}

function revealSteps(section: LessonSectionRecord, stepsOnly: boolean): RevealStep[] {
   return (section.steps ?? []).map((step, index) => ({
      key: String(index),
      main: (
         <>
            <LessonText text={step.cue} />
            {hasExpression(step.expression) ? (
               <p className="lesson-step-math">
                  <MathValue value={step.expression} />
               </p>
            ) : null}
         </>
      ),
      beside: stepsOnly ? undefined : <LessonText text={step.why} />
   }));
}

/* A faded example (fade_from): the steps before fade_from, then the student writes the answer.
   Any verdict reveals the steps held back, and so does the reader's "Show all steps". */
function FadedSteps({ section, steps, revealAll, context }: { section: LessonSectionRecord; steps: RevealStep[]; revealAll: boolean; context: PromptContext }) {
   const [verdict, setVerdict] = useState<boolean | null>(null);
   const { onPromptAnswer, onStepsRemaining, now } = context;
   const isRevealed = revealAll || verdict !== null;
   const shownBeforeFade = Math.min(Math.max((section.fade_from ?? 1) - 1, 0), steps.length);
   const isUnanswered = verdict === null;
   const asksForAnswer = isUnanswered && !revealAll;

   useEffect(() => {
      onStepsRemaining?.(!isRevealed);
   }, [isRevealed, onStepsRemaining]);

   return (
      <>
         <StepReveal steps={isRevealed ? steps : steps.slice(0, shownBeforeFade)} revealAll />

         {asksForAnswer ? (
            <PromptField
               label="Write the answer"
               testId="lesson-fade-answer"
               sectionId={section.id}
               onPromptAnswer={onPromptAnswer!}
               onVerdict={setVerdict}
               now={now}
            />
         ) : null}

         {verdict !== null ? <PromptVerdictLine correct={verdict} /> : null}
      </>
   );
}

function WorkedExample({ section, revealAll, stepsOnly, context }: { section: LessonSectionRecord; revealAll: boolean; stepsOnly: boolean; context: PromptContext }) {
   const steps = revealSteps(section, stepsOnly);
   const isFaded = section.fade_from !== undefined && !stepsOnly && context.onPromptAnswer !== undefined;

   return (
      <>
         {section.problem !== undefined ? (
            <p className="item-stem">
               <LessonText text={section.problem.text} />
            </p>
         ) : null}

         {isFaded ? (
            <FadedSteps section={section} steps={steps} revealAll={revealAll} context={context} />
         ) : (
            <StepReveal steps={steps} revealAll={revealAll || stepsOnly} onRemainingChange={context.onStepsRemaining} />
         )}
      </>
   );
}

/* The wrong step beside the right step, each under its label with a glyph, so the pair reads in
   greyscale; the right step is revealed on "Next step". When both steps carry the same expression
   the error is in what surrounds the value (a missing differential, an unstated form, no sentence),
   so the expression is left out and the two texts carry the difference: drawn twice, the rendered
   value would show the very notation the wrong step's text says is missing. With fix_prompt the
   student writes the right step first, or asks to see it; the consequence and the possible reason
   wait for the right step. */
function ErrorBlock({ section, revealAll, context }: { section: LessonSectionRecord; revealAll: boolean; context: PromptContext }) {
   const [showsRight, setShowsRight] = useState(revealAll);
   const [fixVerdict, setFixVerdict] = useState<boolean | null>(null);
   const offersFix = section.fix_prompt === true && !revealAll && context.onPromptAnswer !== undefined;
   const isShown = showsRight || revealAll;
   const showsAftermath = isShown || !offersFix;
   const wrongExpression = section.wrong_step?.expression;
   const rightExpression = section.right_step?.expression;
   const isSameValue = hasExpression(wrongExpression) && JSON.stringify(wrongExpression) === JSON.stringify(rightExpression);
   const showsWrongValue = hasExpression(wrongExpression) && !isSameValue;
   const showsRightValue = hasExpression(rightExpression) && !isSameValue;

   function fixAnswered(correct: boolean) {
      setFixVerdict(correct);
      setShowsRight(true);
   }

   const showRightButton = (
      <button type="button" className="text-button" data-testid="lesson-fix-show" onClick={() => setShowsRight(true)}>
         Show the right step
      </button>
   );

   return (
      <>
         <Prose text={section.observed_behavior} />

         <div className="lesson-pair" data-testid="lesson-error-pair">
            <div className="lesson-pair-side" data-testid="lesson-wrong-step">
               <p className="label-heading">
                  <span aria-hidden="true">{INCORRECT_GLYPH}</span> {WRONG_STEP_LABEL}
               </p>
               <Prose text={section.wrong_step?.text} />
               {showsWrongValue ? <MathValue value={wrongExpression} /> : null}
            </div>

            {isShown ? (
               <div className="lesson-pair-side" data-testid="lesson-right-step">
                  {fixVerdict !== null ? <PromptVerdictLine correct={fixVerdict} /> : null}
                  <p className="label-heading">
                     <span aria-hidden="true">{CORRECT_GLYPH}</span> {RIGHT_STEP_LABEL}
                  </p>
                  <Prose text={section.right_step?.text} />
                  {showsRightValue ? <MathValue value={rightExpression} /> : null}
               </div>
            ) : null}
         </div>

         {!isShown && offersFix ? (
            <PromptField
               label="What should this step be?"
               testId="lesson-fix-prompt"
               submitTestId="lesson-fix-submit"
               sectionId={section.id}
               onPromptAnswer={context.onPromptAnswer!}
               onVerdict={fixAnswered}
               now={context.now}
               secondary={showRightButton}
            />
         ) : null}

         {!isShown && !offersFix ? (
            <button type="button" className="text-button" data-testid="lesson-next-step" onClick={() => setShowsRight(true)}>
               Next step
            </button>
         ) : null}

         {showsAftermath ? (
            <>
               <Prose text={section.scoring_consequence} />
               {section.possible_reason !== undefined ? (
                  <p className="muted">
                     A possible reason: <LessonText text={section.possible_reason.text} />
                  </p>
               ) : null}
            </>
         ) : null}
      </>
   );
}

/* The first strategy block's pair (the v2 Recognise screen): a stem of this concept beside a stem
   it is mistaken for, each under a heading word so the pair reads without colour. Side by side
   above 600 px and stacked below (app.css .lesson-contrast-pair). */
function ContrastPair({ contrast }: { contrast: LessonContrast }) {
   return (
      <div className="stack stack-tight" data-testid="lesson-contrast">
         <div className="lesson-contrast-pair">
            <article className="lesson-pair-side" data-testid="lesson-contrast-this">
               <p className="label-heading">{CONTRAST_THIS_HEADING}</p>
               <p>
                  <LessonText text={contrast.this.text} />
               </p>
            </article>

            <article className="lesson-pair-side" data-testid="lesson-contrast-not-this">
               <p className="label-heading">{CONTRAST_NOT_THIS_HEADING}</p>
               <p>
                  <LessonText text={contrast.not_this.text} />
               </p>
            </article>
         </div>

         <p>
            What separates them: <LessonText text={contrast.feature} />
         </p>

         {contrast.not_this.why_not !== undefined ? (
            <p className="muted">
               <LessonText text={contrast.not_this.why_not} />
            </p>
         ) : null}
      </div>
   );
}

export interface LessonSectionProps {
   section: LessonSectionRecord;
   form?: "full" | "steps_only";
   revealAll?: boolean;
   /* A line the reader sets above the section's text: the committed prediction on the first core
      key idea. */
   lead?: ReactNode;
   prediction?: { committed: CommittedPrediction | null; onCommit: (committed: CommittedPrediction) => void };
   onPromptAnswer?: PromptAnswer;
   onStepsRemaining?: (hasMore: boolean) => void;
   now?: () => number;
   /* The lesson's calculator_work: its worked example belongs to a calculator archetype, so the
      example ends with the link to calculator practice (docs/calculator/design.md, Where it
      lives). */
   calculatorWork?: boolean;
}

export function LessonSection(props: LessonSectionProps) {
   const { section, form = "full", revealAll = false, lead, prediction, onPromptAnswer, onStepsRemaining, now } = props;
   const endsWithCalculatorLink = section.type === "worked_example" && props.calculatorWork === true;
   const stepsOnly = form === "steps_only";
   const context: PromptContext = { onPromptAnswer, onStepsRemaining, now };
   const asksForPrediction = section.type === "prediction" && prediction !== undefined;

   return (
      <section
         className="lesson-section"
         id={anchorFragment(section.id)}
         data-testid="lesson-section"
         data-section-type={section.type}
         data-mode={sectionMode(section)}
         data-agent-anchor="section"
      >
         <h2 className="section-heading">{SECTION_HEADINGS[section.type] ?? "Part"}</h2>

         {lead}

         {asksForPrediction ? (
            <LessonPrediction section={section} committed={prediction.committed} onCommit={prediction.onCommit} onPromptAnswer={onPromptAnswer} now={now} />
         ) : null}

         {section.type === "prediction" && !asksForPrediction ? <Prose text={section.stem?.text} /> : null}

         {section.type === "strategy" ? (
            <dl className="lesson-strategy">
               {[section.cue, section.method, section.rival, section.separating_feature].map((line, index) => (
                  <div key={STRATEGY_LABELS[index]}>
                     <dt className="label-heading">{STRATEGY_LABELS[index]}</dt>
                     <dd>
                        <LessonText text={line ?? ""} />
                     </dd>
                  </div>
               ))}
            </dl>
         ) : null}

         {section.type === "strategy" && section.contrast !== undefined ? <ContrastPair contrast={section.contrast} /> : null}

         {section.type === "worked_example" ? <WorkedExample section={section} revealAll={revealAll} stepsOnly={stepsOnly} context={context} /> : null}

         {endsWithCalculatorLink ? (
            <p>
               <CalculatorLink />
            </p>
         ) : null}

         {section.type === "what_a_reader_scores" ? (
            <ul className="lesson-checklist">
               {(section.lines ?? []).map((line, index) => (
                  <li key={index}>
                     <LessonText text={line.text} />
                  </li>
               ))}
            </ul>
         ) : null}

         {section.type === "common_error" ? <ErrorBlock section={section} revealAll={revealAll} context={context} /> : null}

         {["orientation", "key_ideas", "representations", "prerequisite_bridge"].includes(section.type) ? (
            <>
               <Prose text={section.text} />
               {section.notation !== undefined ? (
                  <p className="caption">
                     Notation: <LessonText text={section.notation} />
                  </p>
               ) : null}
               {section.quote !== undefined ? (
                  <blockquote className="lesson-quote">
                     <LessonText text={section.quote.text} />
                  </blockquote>
               ) : null}
            </>
         ) : null}

         <DeliveryBlock delivery={section.type === "worked_example" || section.type === "common_error" ? undefined : section.delivery} />
      </section>
   );
}
