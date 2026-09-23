import { affordanceProps } from "../affordances";
import { motionClass } from "../styles/motion";
import type { ElaboratedPayload } from "../api/types";
import { INCORRECT_GLYPH, INCORRECT_WORD } from "./StepMarks";

export interface ElaboratedPanelProps {
   elaborated: ElaboratedPayload | null;
   sentence: string | null;
}

export function ElaboratedPanel({ elaborated, sentence }: ElaboratedPanelProps) {
   if (elaborated === null) {
      return null;
   }

   const hasSentence = sentence !== null && sentence.trim().length > 0;

   return (
      <section
         {...affordanceProps("elaboratedFeedbackPanel")}
         className={motionClass("elaboratedFeedbackPanel")}
         data-testid="elaborated-panel"
      >
         <p data-testid="elaborated-verdict" style={{ color: "var(--growth-state-incorrect)" }}>
            <span data-glyph aria-hidden="true">
               {INCORRECT_GLYPH}
            </span>
            <span>{INCORRECT_WORD}</span>
         </p>

         {elaborated.violated_step !== null ? (
            <p data-testid="violated-step">{elaborated.violated_step}</p>
         ) : null}

         {elaborated.observed_behavior !== null ? (
            <p data-testid="observed-behavior">{elaborated.observed_behavior}</p>
         ) : null}

         {elaborated.scoring_consequence !== null ? (
            <p data-testid="scoring-consequence">{elaborated.scoring_consequence}</p>
         ) : null}

         {hasSentence ? <p data-testid="tutor-sentence">{sentence}</p> : null}
      </section>
   );
}