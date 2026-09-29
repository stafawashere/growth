import type { CalculatorCapability, CalculatorCard } from "../api/types";
import { StepReveal, type RevealStep } from "../lessons/StepReveal";
import { MathText } from "../math/MathText";
import {
   BLUEBOOK_HEADING,
   DEMO_ANSWER_LEAD,
   DEMO_FUNCTION_LEAD,
   DEMO_SETUP_LEAD,
   DEMO_SHOWS_LEAD,
   DEMONSTRATION_HEADING,
   DRILL_THIS_LABEL,
   EXAM_HABIT_HEADING,
   STEPS_HEADING
} from "./words";

/* One procedure card on one screen, top to bottom (docs/calculator/design.md, The procedure cards):
   the task, the Desmos steps with what is typed in a monospace span exactly as Desmos documents it,
   one worked instance through the lesson reader's step reveal, the exam habit, the Bluebook note
   when there is one, and "Drill this". No reading time, no completion mark, no checkbox, and no
   source on the screen. */

function inline(tex: string) {
   return `\\(${tex}\\)`;
}

function demonstrationSteps(card: CalculatorCard): RevealStep[] {
   const { demonstration } = card;

   const opening: RevealStep = {
      key: "function",
      main: (
         <>
            {DEMO_FUNCTION_LEAD} <MathText text={inline(demonstration.function_tex)} />
         </>
      )
   };

   const typed: RevealStep[] = demonstration.lines.map((line, index) => ({
      key: `line-${index}`,
      main: <code className="kbd">{line.typed}</code>,
      beside: (
         <>
            {DEMO_SHOWS_LEAD} <MathText text={line.shows} />
         </>
      )
   }));

   const setup: RevealStep = {
      key: "setup",
      main: (
         <>
            {DEMO_SETUP_LEAD} <MathText text={inline(demonstration.setup_latex)} />
         </>
      )
   };

   const answer: RevealStep = {
      key: "answer",
      main: (
         <>
            {DEMO_ANSWER_LEAD} {demonstration.answer}
         </>
      )
   };

   return [opening, ...typed, setup, answer];
}

export interface ProcedureCardProps {
   card: CalculatorCard;
   onDrill: (capability: CalculatorCapability) => void;
}

export function ProcedureCard(props: ProcedureCardProps) {
   const { card } = props;
   const hasBluebookNote = card.bluebook_note !== null && card.bluebook_note !== "";

   return (
      <article className="card stack procedure-card" data-testid="procedure-card" aria-labelledby="procedure-card-title">
         <h2 id="procedure-card-title">{card.title}</h2>

         <p className="lead">
            <MathText text={card.task} />
         </p>

         <section className="stack stack-tight">
            <h3 className="section-heading">{STEPS_HEADING}</h3>

            <ol className="procedure-steps" data-testid="procedure-steps">
               {card.steps.map((step, index) => (
                  <li key={index}>
                     <MathText text={step.text} /> {step.keys === "" ? null : <code className="kbd">{step.keys}</code>}
                  </li>
               ))}
            </ol>
         </section>

         <section className="stack stack-tight" data-testid="procedure-demonstration">
            <h3 className="section-heading">{DEMONSTRATION_HEADING}</h3>

            <StepReveal steps={demonstrationSteps(card)} />
         </section>

         <section className="stack stack-tight">
            <h3 className="section-heading">{EXAM_HABIT_HEADING}</h3>

            {card.exam_habit.map((habit, index) => (
               <p key={index}>
                  <MathText text={habit.text} />
               </p>
            ))}
         </section>

         {hasBluebookNote ? (
            <section className="callout stack stack-tight" data-testid="procedure-bluebook-note">
               <h3 className="section-heading">{BLUEBOOK_HEADING}</h3>

               <p>
                  <MathText text={card.bluebook_note as string} />
               </p>
            </section>
         ) : null}

         <div>
            <button type="button" className="button-primary" onClick={() => props.onDrill(card.capability)}>
               {DRILL_THIS_LABEL}
            </button>
         </div>
      </article>
   );
}
