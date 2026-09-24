import type { ProbeAdministration, ProbeServedItem } from "../api/types";
import { MathField } from "../input/MathField";
import { McqControl } from "../input/McqControl";
import { MathText } from "../math/MathText";
import { ANSWER_UNAVAILABLE } from "../session/Item";

/* The stable concept probe (11 P7 scope item 6). Items come one at a time in the set's fixed order,
   with no feedback and no confidence rating, because the probe measures and must not teach
   (app/checkpoint/probe.py). The session Item component always asks for a confidence rating, so
   the probe draws its stem and answer controls directly from the same MathText, McqControl and
   MathField the session uses. */

export const PROBE_NOTE =
   "The concept probe shows no answers and no feedback, and it does not change anything in the mastery model.";

export const NEXT_LABEL = "Next question";

export interface ProbeIntroProps {
   refusal: string | null;
   onStart: () => void;
   onLeave: () => void;
}

export interface ProbeItemViewProps {
   item: ProbeServedItem;
   selectedOptionId: string | null;
   onOptionChange: (optionId: string) => void;
   onAnswerChange: (mathjson: unknown) => void;
   answerUnavailable: boolean;
   onAnswerUnavailable: (reason: unknown) => void;
   canSend: boolean;
   onSend: () => void;
}

export interface ProbeFinishedProps {
   administration: ProbeAdministration;
   onLeave: () => void;
}

export function ProbeIntro({ refusal, onStart, onLeave }: ProbeIntroProps) {
   return (
      <section className="card" data-testid="probe-intro">
         <h1 className="screen-title">Concept probe</h1>

         <p>
            The concept probe is a fixed set of questions that never appear in practice. It asks the same
            questions each time, so the results can be compared across the months.
         </p>

         <p>{PROBE_NOTE}</p>

         {refusal === null ? null : <p role="alert">{refusal}</p>}

         <button type="button" className="button-primary" onClick={onStart}>
            Start the concept probe
         </button>

         <button type="button" className="text-button" onClick={onLeave}>
            Back to progress
         </button>
      </section>
   );
}

export function ProbeItemView(props: ProbeItemViewProps) {
   const {
      item,
      selectedOptionId,
      onOptionChange,
      onAnswerChange,
      answerUnavailable,
      onAnswerUnavailable,
      canSend,
      onSend
   } = props;

   const servesMcq = item.format === "mcq";

   return (
      <article className="card item" data-testid="probe-item">
         <h1 className="eyebrow">Concept probe</h1>

         <p className="item-stem" data-testid="item-stem"><MathText text={item.stem} /></p>

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
               <MathField key={item.id} label="My answer" onChange={onAnswerChange} onLoadFailure={onAnswerUnavailable} />

               {answerUnavailable ? <p data-testid="answer-unavailable">{ANSWER_UNAVAILABLE}</p> : null}
            </div>
         )}

         <button type="button" className="button-primary" disabled={!canSend} onClick={onSend}>
            {NEXT_LABEL}
         </button>
      </article>
   );
}

export function ProbeFinished({ administration, onLeave }: ProbeFinishedProps) {
   const hasGraded = administration.graded > 0;
   const ungraded = administration.answered - administration.graded;
   const hasUngraded = ungraded > 0;

   return (
      <section className="card" data-testid="probe-finished">
         <h1 className="screen-title">Concept probe</h1>

         <p data-testid="probe-score">
            {hasGraded
               ? `${administration.correct} of ${administration.graded} graded items correct.`
               : "No answer in this probe could be graded."}
         </p>

         {hasUngraded ? (
            <p className="muted">
               {ungraded} of {administration.answered} answers could not be graded and are not counted.
            </p>
         ) : null}

         <p>{PROBE_NOTE}</p>

         <button type="button" className="text-button" onClick={onLeave}>
            Back to progress
         </button>
      </section>
   );
}