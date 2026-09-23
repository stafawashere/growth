import { affordanceProps } from "../affordances";
import { motionClass } from "../styles/motion";
import type { StepMark } from "../api/types";

/* 08's Accessibility section: every state that uses state-correct or state-incorrect also carries
   a glyph and a word, so the greyscale render says the same thing as the colour render. The
   glyphs stay inside the ASCII range because the repository bans symbol characters. */

export const CORRECT_GLYPH = "ok";

export const INCORRECT_GLYPH = "x";

export const CORRECT_WORD = "Correct";

export const INCORRECT_WORD = "Not yet";

export interface StepMarksProps {
   marks: StepMark[];
}

export function StepMarks({ marks }: StepMarksProps) {
   const hasMarks = marks.length > 0;

   if (!hasMarks) {
      return null;
   }

   return (
      <ul
         {...affordanceProps("stepVerificationMark")}
         className={motionClass("stepVerificationMark")}
         data-testid="step-marks"
      >
         {marks.map((mark) => {
            const glyph = mark.correct ? CORRECT_GLYPH : INCORRECT_GLYPH;
            const word = mark.correct ? CORRECT_WORD : INCORRECT_WORD;
            const token = mark.correct ? "var(--growth-state-correct)" : "var(--growth-state-incorrect)";

            return (
               <li key={mark.index} data-testid={`step-mark-${mark.index}`} style={{ color: token }}>
                  <span data-glyph aria-hidden="true">
                     {glyph}
                  </span>
                  <span>{word}</span>
                  <span>{mark.description}</span>
               </li>
            );
         })}
      </ul>
   );
}