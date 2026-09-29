import { useState } from "react";

import type { LessonDelivery, LessonSection as LessonSectionRecord } from "../api/types";
import { MathText } from "../math/MathText";
import { MathValue } from "../math/MathValue";
import { CORRECT_GLYPH, INCORRECT_GLYPH } from "../session/StepMarks";
import { FigureControl } from "./FigureControl";
import { FrameStepper } from "./FrameStepper";
import { LessonFallback } from "./LessonFallback";
import { LessonFigure } from "./LessonFigure";
import { anchorFragment } from "./LessonLink";
import { LessonTable } from "./LessonTable";
import { ModelTable } from "./ModelTable";
import { StepReveal } from "./StepReveal";

/* One section of a lesson, switched on its type and, for the blocks that carry one, on its
   delivery mode (CONTRACT.md Reader; TEMPLATE.md Delivery). Strategy, the scoring checklist and a
   prerequisite bridge carry no delivery: the reader fixes their form. */

export const SECTION_HEADINGS: Record<LessonSectionRecord["type"], string> = {
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

/* The mode a view of this section is logged under (amendment A-D5): its delivery mode, or text
   for the blocks whose form the reader fixes. */
export function sectionMode(section: LessonSectionRecord) {
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
      <div className="lesson-delivery" data-testid="lesson-delivery" data-mode={delivery.mode}>
         {blocks[delivery.mode]}
      </div>
   );
}

function Prose({ text }: { text: string | undefined }) {
   return text === undefined ? null : (
      <p>
         <MathText text={text} />
      </p>
   );
}

function hasExpression(value: unknown) {
   return value !== undefined && value !== null;
}

function WorkedExample({ section, revealAll, stepsOnly }: { section: LessonSectionRecord; revealAll: boolean; stepsOnly: boolean }) {
   const steps = (section.steps ?? []).map((step, index) => ({
      key: String(index),
      main: (
         <>
            <MathText text={step.cue} />
            {hasExpression(step.expression) ? (
               <p className="lesson-step-math">
                  <MathValue value={step.expression} />
               </p>
            ) : null}
         </>
      ),
      beside: stepsOnly ? undefined : <MathText text={step.why} />
   }));

   return (
      <>
         {section.problem !== undefined ? (
            <p className="item-stem">
               <MathText text={section.problem.text} />
            </p>
         ) : null}

         <StepReveal steps={steps} revealAll={revealAll || stepsOnly} />
      </>
   );
}

/* The wrong step beside the right step, each under its label with a glyph, so the pair reads in
   greyscale; the right step is revealed on "Next step". */
function ErrorPair({ section, revealAll }: { section: LessonSectionRecord; revealAll: boolean }) {
   const [showsRight, setShowsRight] = useState(revealAll);
   const isShown = showsRight || revealAll;

   return (
      <>
         <div className="lesson-pair" data-testid="lesson-error-pair">
            <div className="lesson-pair-side" data-testid="lesson-wrong-step">
               <p className="label-heading">
                  <span aria-hidden="true">{INCORRECT_GLYPH}</span> {WRONG_STEP_LABEL}
               </p>
               <Prose text={section.wrong_step?.text} />
               {hasExpression(section.wrong_step?.expression) ? <MathValue value={section.wrong_step?.expression} /> : null}
            </div>

            {isShown ? (
               <div className="lesson-pair-side" data-testid="lesson-right-step">
                  <p className="label-heading">
                     <span aria-hidden="true">{CORRECT_GLYPH}</span> {RIGHT_STEP_LABEL}
                  </p>
                  <Prose text={section.right_step?.text} />
                  {hasExpression(section.right_step?.expression) ? <MathValue value={section.right_step?.expression} /> : null}
               </div>
            ) : null}
         </div>

         {isShown ? null : (
            <button type="button" className="text-button" data-testid="lesson-next-step" onClick={() => setShowsRight(true)}>
               Next step
            </button>
         )}
      </>
   );
}

export interface LessonSectionProps {
   section: LessonSectionRecord;
   form?: "full" | "steps_only";
   revealAll?: boolean;
}

export function LessonSection({ section, form = "full", revealAll = false }: LessonSectionProps) {
   const stepsOnly = form === "steps_only";

   return (
      <section
         className="lesson-section"
         id={anchorFragment(section.id)}
         data-testid="lesson-section"
         data-section-type={section.type}
         data-mode={sectionMode(section)}
      >
         <h2 className="section-heading">{SECTION_HEADINGS[section.type] ?? "Part"}</h2>

         {section.type === "strategy" ? (
            <dl className="lesson-strategy">
               {[section.cue, section.method, section.rival, section.separating_feature].map((line, index) => (
                  <div key={STRATEGY_LABELS[index]}>
                     <dt className="label-heading">{STRATEGY_LABELS[index]}</dt>
                     <dd>
                        <MathText text={line ?? ""} />
                     </dd>
                  </div>
               ))}
            </dl>
         ) : null}

         {section.type === "worked_example" ? <WorkedExample section={section} revealAll={revealAll} stepsOnly={stepsOnly} /> : null}

         {section.type === "what_a_reader_scores" ? (
            <ul className="lesson-checklist">
               {(section.lines ?? []).map((line, index) => (
                  <li key={index}>
                     <MathText text={line.text} />
                  </li>
               ))}
            </ul>
         ) : null}

         {section.type === "common_error" ? (
            <>
               <Prose text={section.observed_behavior} />
               <ErrorPair section={section} revealAll={revealAll} />
               <Prose text={section.scoring_consequence} />
               {section.possible_reason !== undefined ? (
                  <p className="muted">
                     A possible reason: <MathText text={section.possible_reason.text} />
                  </p>
               ) : null}
            </>
         ) : null}

         {["orientation", "key_ideas", "representations", "prerequisite_bridge"].includes(section.type) ? (
            <>
               <Prose text={section.text} />
               {section.notation !== undefined ? (
                  <p className="caption">
                     Notation: <MathText text={section.notation} />
                  </p>
               ) : null}
               {section.quote !== undefined ? (
                  <blockquote className="lesson-quote">
                     <MathText text={section.quote.text} />
                  </blockquote>
               ) : null}
            </>
         ) : null}

         <DeliveryBlock delivery={section.type === "worked_example" || section.type === "common_error" ? undefined : section.delivery} />
      </section>
   );
}
