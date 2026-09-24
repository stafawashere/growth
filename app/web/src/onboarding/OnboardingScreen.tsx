import type { DiagnosticServedItem, DiagnosticUnit, DiagnosticUnitState } from "../api/types";
import { MathField } from "../input/MathField";
import { MathText } from "../math/MathText";
import { ANSWER_UNAVAILABLE, COMMIT_LABEL } from "../session/Item";

export type OnboardingReason = "first_login" | "long_gap";

export type DiagnosticItemState = "unanswered" | "answered" | "submitted";

export const NOT_LEARNED_LABEL = "I have not learned this yet";

export const FINISHED_LABEL = "Go to today's set";

export const EARLY_STOP_NOTE = "This stops early once it has enough to place you. There is no score at the end.";

/* 08 diagnostic result: unit-level states in words, never a percentage. */
export const UNIT_STATE_WORDS: Record<DiagnosticUnitState, string> = {
   not_started: "Not started yet",
   partial: "Partly there",
   fluent: "Fluent",
   unresolved: "Not placed yet",
   not_probed: "Not asked yet (no items for this unit yet)"
};

interface IntroCopy {
   title: string;
   purpose: string;
   startLabel: string;
}

const INTRO_COPY: Record<OnboardingReason, IntroCopy> = {
   first_login: {
      title: "Before your first set",
      purpose:
         "This is a short diagnostic. It asks questions from across the course so the app knows where to start you. If a question covers something you have not learned yet, say so and it moves on.",
      startLabel: "Start the diagnostic"
   },
   long_gap: {
      title: "Before your next set",
      purpose:
         "It has been a while since your last set, so this is a re-diagnostic. It checks where you are now and updates what the app knows about you. It never resets it.",
      startLabel: "Start the re-diagnostic"
   }
};

export interface DiagnosticIntroProps {
   reason: OnboardingReason;
   onStart: () => void;
}

export function DiagnosticIntro({ reason, onStart }: DiagnosticIntroProps) {
   const copy = INTRO_COPY[reason];

   return (
      <section className="card" data-testid="diagnostic-intro">
         <h1 className="eyebrow">Calculus BC</h1>

         <h2 className="screen-title">{copy.title}</h2>

         <p>{copy.purpose}</p>

         <p>
            It stops early once it has enough to place you, because more questions after that would not
            change where you start.
         </p>

         <p>There is no score at the end. You see where each unit stands, in words.</p>

         <button type="button" className="button-primary" onClick={onStart}>
            {copy.startLabel}
         </button>
      </section>
   );
}

export interface DiagnosticItemProps {
   item: DiagnosticServedItem;
   state: DiagnosticItemState;
   answerUnavailable: boolean;
   onAnswerChange: (mathjson: unknown) => void;
   onAnswerUnavailable: (reason: unknown) => void;
   onCheck: () => void;
   onNotLearned: () => void;
}

export function DiagnosticItem(props: DiagnosticItemProps) {
   const { item, state, answerUnavailable, onAnswerChange, onAnswerUnavailable, onCheck, onNotLearned } = props;

   const questionNumber = item.diagnostic_position + 1;
   const isSubmitted = state === "submitted";
   const isUnanswered = state === "unanswered";
   const canCheck = !isSubmitted && !isUnanswered && !answerUnavailable;
   const offersCheck = !answerUnavailable;

   return (
      <article className="card item" data-testid="diagnostic-item" data-state={state}>
         <h2 className="eyebrow">
            Question {questionNumber} of at most {item.diagnostic_cap}
         </h2>

         <p className="item-stem" data-testid="item-stem"><MathText text={item.stem} /></p>

         <div data-testid="math-answer">
            <MathField key={item.id} label="My answer" onChange={onAnswerChange} onLoadFailure={onAnswerUnavailable} />

            {answerUnavailable ? <p data-testid="answer-unavailable">{ANSWER_UNAVAILABLE}</p> : null}
         </div>

         <button type="button" className="text-button" disabled={isSubmitted} onClick={onNotLearned}>
            {NOT_LEARNED_LABEL}
         </button>

         {offersCheck ? (
            <button
               type="button"
               className="motion-instant-submit-answer button-primary"
               disabled={!canCheck}
               onClick={onCheck}
            >
               {COMMIT_LABEL}
            </button>
         ) : null}

         <p className="caption">{EARLY_STOP_NOTE}</p>
      </article>
   );
}

export interface DiagnosticResultViewProps {
   units: ReadonlyArray<DiagnosticUnit>;
   onFinished: () => void;
}

export function DiagnosticResultView({ units, onFinished }: DiagnosticResultViewProps) {
   return (
      <section className="card" data-testid="diagnostic-result">
         <h1 className="eyebrow">Calculus BC</h1>

         <h2 className="screen-title">Where you are starting</h2>

         <p>There is no score. This is where each unit stands, and today&apos;s set starts from it.</p>

         <dl>
            {units.map((entry) => (
               <div key={entry.unit} data-testid="diagnostic-unit">
                  <dt>{entry.title}</dt>
                  <dd>{UNIT_STATE_WORDS[entry.state]}</dd>
               </div>
            ))}
         </dl>

         <button type="button" className="button-primary" onClick={onFinished}>
            {FINISHED_LABEL}
         </button>
      </section>
   );
}
