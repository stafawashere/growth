import { useState } from "react";

import type { DiagnosticServedItem, DiagnosticUnit, DiagnosticUnitState } from "../api/types";
import { MathAnswerField } from "../input/MathAnswerField";
import { FigureView } from "../figures/FigureView";
import { MathText } from "../math/MathText";
import { ANSWER_UNAVAILABLE, COMMIT_LABEL } from "../session/Item";
import { StudyPlanSection } from "../settings/StudySections";
import { Icon } from "../ui/Icon";
import { List } from "../ui/List";
import { Page, PageHeader } from "../ui/Page";

export type OnboardingReason = "first_login" | "long_gap";

export type DiagnosticItemState = "unanswered" | "answered" | "submitted";

export const NOT_LEARNED_LABEL = "I have not learned this yet";

export const SKIP_UNIT_LABEL = "Skip this unit";

export const SKIP_UNIT_CONFIRM_LABEL = "Skip the rest of this unit";

export const KEEP_ANSWERING_LABEL = "Keep answering";

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
      <section data-testid="diagnostic-intro">
         <Page header={<PageHeader eyebrow={reason === "first_login" ? "Placement" : "Returning after a break"} title={copy.title} intro={copy.purpose} />}>
            <div className="card stack">
               <h2>What to expect</h2>

               <ul className="expect-list">
                  <li>
                     <Icon name="check" />
                     <span>
                        It stops early once it has enough to place you, because more questions after that would not change where you
                        start.
                     </span>
                  </li>

                  <li>
                     <Icon name="check" />
                     <span>If a question covers something you have not learned yet, say so and it moves on.</span>
                  </li>

                  <li>
                     <Icon name="check" />
                     <span>There is no score at the end. You see where each unit stands, in words.</span>
                  </li>
               </ul>
            </div>

            {reason === "first_login" ? <StudyPlanSection /> : null}

            <div className="cluster">
               <button type="button" className="button-primary button-large" onClick={onStart}>
                  {copy.startLabel}
                  <Icon name="next" />
               </button>
            </div>
         </Page>
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
   onSkipUnit?: () => void;
}

export function DiagnosticItem(props: DiagnosticItemProps) {
   const { item, state, answerUnavailable, onAnswerChange, onAnswerUnavailable, onCheck, onNotLearned, onSkipUnit } = props;
   const [isConfirmingSkip, setIsConfirmingSkip] = useState(false);

   const questionNumber = item.diagnostic_position + 1;
   const isSubmitted = state === "submitted";
   const isUnanswered = state === "unanswered";
   const canCheck = !isSubmitted && !isUnanswered && !answerUnavailable;
   const offersCheck = !answerUnavailable;
   const offersSkip = onSkipUnit !== undefined;

   function skipUnit() {
      setIsConfirmingSkip(false);
      onSkipUnit?.();
   }

   return (
      <Page
         header={
            <PageHeader
               eyebrow="Placement"
               title={
                  <>
                     Question {questionNumber} of at most {item.diagnostic_cap}
                  </>
               }
               intro={EARLY_STOP_NOTE}
            />
         }
      >
         <article className="card item" data-testid="diagnostic-item" data-state={state}>
            <div className="question">
               <div className="question-stem">
                  <span className="eyebrow">Solve</span>

                  <p className="item-stem" data-testid="item-stem">
                     <MathText text={item.stem} />
                  </p>

                  {item.figure_spec ? <FigureView spec={item.figure_spec} /> : null}
               </div>
            </div>

            <div data-testid="math-answer">
               <MathAnswerField key={item.id} label="My answer" onChange={onAnswerChange} onLoadFailure={onAnswerUnavailable} />

               {answerUnavailable ? <p data-testid="answer-unavailable">{ANSWER_UNAVAILABLE}</p> : null}
            </div>

            <div className="submit-row">
               <div className="cluster">
                  <button type="button" className="text-button" disabled={isSubmitted} onClick={onNotLearned}>
                     {NOT_LEARNED_LABEL}
                  </button>

                  {offersSkip && !isConfirmingSkip ? (
                     <button type="button" className="text-button" disabled={isSubmitted} onClick={() => setIsConfirmingSkip(true)}>
                        {SKIP_UNIT_LABEL}
                     </button>
                  ) : null}
               </div>

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
            </div>

            {offersSkip && isConfirmingSkip ? (
               <div role="alertdialog" aria-label="Skip this unit" className="callout" data-testid="skip-unit-confirmation">
                  <p>Every question still to come from this unit is answered &quot;{NOT_LEARNED_LABEL}&quot;, this one included.</p>

                  <div className="cluster">
                     <button type="button" className="text-button" disabled={isSubmitted} onClick={skipUnit}>
                        {SKIP_UNIT_CONFIRM_LABEL}
                     </button>

                     <button type="button" className="text-button" onClick={() => setIsConfirmingSkip(false)}>
                        {KEEP_ANSWERING_LABEL}
                     </button>
                  </div>
               </div>
            ) : null}
         </article>
      </Page>
   );
}

export interface DiagnosticResultViewProps {
   units: ReadonlyArray<DiagnosticUnit>;
   onFinished: () => void;
}

const UNIT_STATE_TONE: Record<DiagnosticUnitState, string> = {
   not_started: "badge",
   partial: "badge",
   fluent: "badge badge-correct",
   unresolved: "badge",
   not_probed: "badge"
};

export function DiagnosticResultView({ units, onFinished }: DiagnosticResultViewProps) {
   return (
      <section data-testid="diagnostic-result">
         <Page
            header={
               <PageHeader
                  eyebrow="Diagnostic complete"
                  title="Where you are starting"
                  intro="There is no score. This is where each unit stands, and today's set starts from it."
               />
            }
         >
            <List as="ul" label="Where each unit stands">
               {units.map((entry) => (
                  <li key={entry.unit} data-testid="diagnostic-unit" className="list-row">
                     <div className="list-row-body">
                        <span className="list-row-title">{entry.title}</span>
                     </div>

                     <div className="list-row-trail">
                        <span className={UNIT_STATE_TONE[entry.state]}>{UNIT_STATE_WORDS[entry.state]}</span>
                     </div>
                  </li>
               ))}
            </List>

            <div className="cluster">
               <button type="button" className="button-primary button-large" onClick={onFinished}>
                  {FINISHED_LABEL}
                  <Icon name="next" />
               </button>
            </div>
         </Page>
      </section>
   );
}
