import { affordanceProps } from "../affordances";
import { motionClass } from "../styles/motion";
import type { StepMark } from "../api/types";
import { MathText } from "../math/MathText";

/* 08's Accessibility section: every state that uses state-correct or state-incorrect also carries
   a glyph and a word, so the greyscale render says the same thing as the colour render. The
   glyphs stay inside the ASCII range because the repository bans symbol characters.

   A step the stage showed was given, not verified, so it carries 08's own "given" label from the
   completion wireframe and neither verdict colour. Only the blank carries a verdict, and a blank
   with no verdict yet shows none. */

export const CORRECT_GLYPH = "ok";

export const INCORRECT_GLYPH = "x";

export const CORRECT_WORD = "Correct";

export const INCORRECT_WORD = "Not yet";

export const GIVEN_WORD = "given";

/* The live tutor names each shown step of the worked solution solution_step_1 onward, numbered as
   the steps are. */
export function solutionStepAnchor(index: number) {
   return `solution_step_${index}`;
}

export interface StepMarksProps {
   marks: StepMark[];
}

function GivenStep({ mark }: { mark: StepMark }) {
   return (
      <li
         data-testid={`step-mark-${mark.index}`}
         data-given="true"
         data-agent-anchor={solutionStepAnchor(mark.index)}
         style={{ color: "var(--growth-text-secondary)" }}
      >
         <span className="sheet-margin step-mark-verdict">
            <span>{GIVEN_WORD}</span>
         </span>
         <span className="sheet-body math-overflow"><MathText text={mark.text} /></span>
      </li>
   );
}

function BlankStep({ mark }: { mark: StepMark }) {
   const hasVerdict = mark.correct !== null;

   if (!hasVerdict) {
      return (
         <li data-testid={`step-mark-${mark.index}`} data-agent-anchor={solutionStepAnchor(mark.index)}>
            <span className="sheet-body math-overflow"><MathText text={mark.text} /></span>
         </li>
      );
   }

   const glyph = mark.correct ? CORRECT_GLYPH : INCORRECT_GLYPH;
   const word = mark.correct ? CORRECT_WORD : INCORRECT_WORD;
   const token = mark.correct ? "var(--growth-state-correct)" : "var(--growth-state-incorrect)";

   return (
      <li data-testid={`step-mark-${mark.index}`} data-agent-anchor={solutionStepAnchor(mark.index)} style={{ color: token }}>
         <span className="sheet-margin step-mark-verdict">
            <span data-glyph aria-hidden="true">
               {glyph}
            </span>
            <span>{word}</span>
         </span>
         <span className="sheet-body math-overflow"><MathText text={mark.text} /></span>
      </li>
   );
}

export function StepMarks({ marks }: StepMarksProps) {
   const hasMarks = marks.length > 0;

   if (!hasMarks) {
      return null;
   }

   return (
      <ul
         {...affordanceProps("stepVerificationMark")}
         className={`${motionClass("stepVerificationMark")} step-marks sheet-list`}
         data-testid="step-marks"
      >
         {marks.map((mark) =>
            mark.given ? <GivenStep key={mark.index} mark={mark} /> : <BlankStep key={mark.index} mark={mark} />
         )}
      </ul>
   );
}