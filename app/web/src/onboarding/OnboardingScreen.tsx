import { useEffect, useId, useRef, useState, type KeyboardEvent } from "react";

import type { DiagnosticServedItem, DiagnosticUnit, DiagnosticUnitState } from "../api/types";
import { MathAnswerField } from "../input/MathAnswerField";
import { FigureView } from "../figures/FigureView";
import { MathText } from "../math/MathText";
import { ANSWER_UNAVAILABLE, COMMIT_LABEL } from "../session/Item";
import { StudyPlanSection } from "../settings/StudySections";
import { Icon, type IconName } from "../ui/Icon";
import { List } from "../ui/List";
import { Page, PageHeader } from "../ui/Page";
import { QuestionTrack, trackState, Workbench } from "../ui/Workbench";

export type OnboardingReason = "first_login" | "long_gap";

export type DiagnosticItemState = "unanswered" | "answered" | "submitted";

export const NOT_LEARNED_LABEL = "I have not learned this yet";

export const SKIP_UNIT_LABEL = "Skip this unit";

export const SKIP_UNIT_CONFIRM_LABEL = "Skip the rest of this unit";

export const NOTHING_LEARNED_LABEL = "I have not learned anything";

export const NOTHING_LEARNED_CONFIRM_LABEL = "Answer every question that way";

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
   onSkipEverything?: () => void;
}

type SkipScope = "question" | "unit" | "everything";

type ConfirmableScope = Exclude<SkipScope, "question">;

interface ScopeStep {
   scope: SkipScope;
   label: string;
   reach: string;
   icon: IconName;
}

/* The three rungs of the not-learned ladder, narrowest first. Each rung's reach says what the
   diagnostic does with the rest of the run, so the student sees the scope grow before pressing. */
const SCOPE_STEPS: ReadonlyArray<ScopeStep> = [
   { scope: "question", label: NOT_LEARNED_LABEL, reach: "Only this question. The next one comes up.", icon: "spanOne" },
   { scope: "unit", label: SKIP_UNIT_LABEL, reach: "This question and the rest of its unit. The next unit comes up.", icon: "spanUnit" },
   {
      scope: "everything",
      label: NOTHING_LEARNED_LABEL,
      reach: "Every question still to come. The diagnostic ends here.",
      icon: "spanAll"
   }
];

const SKIP_CONFIRMATION: Record<ConfirmableScope, { title: string; lead: string; body: string; confirmLabel: string; testId: string }> = {
   unit: {
      title: SKIP_UNIT_LABEL,
      lead: "The rest of this unit is set aside.",
      body: `Every question still to come from this unit is answered "${NOT_LEARNED_LABEL}", this one included. The other units are still asked.`,
      confirmLabel: SKIP_UNIT_CONFIRM_LABEL,
      testId: "skip-unit-confirmation"
   },
   everything: {
      title: NOTHING_LEARNED_LABEL,
      lead: "This ends the diagnostic.",
      body: `Every question still to come, from every unit, is answered "${NOT_LEARNED_LABEL}", this one included. You start from the beginning of the course.`,
      confirmLabel: NOTHING_LEARNED_CONFIRM_LABEL,
      testId: "skip-everything-confirmation"
   }
};

export function DiagnosticItem(props: DiagnosticItemProps) {
   const { item, state, answerUnavailable, onAnswerChange, onAnswerUnavailable, onCheck, onNotLearned, onSkipUnit, onSkipEverything } =
      props;
   const [confirmingScope, setConfirmingScope] = useState<ConfirmableScope | null>(null);
   const keepAnsweringRef = useRef<HTMLButtonElement | null>(null);
   const ladderId = useId();

   const questionNumber = item.diagnostic_position + 1;
   const isSubmitted = state === "submitted";
   const isUnanswered = state === "unanswered";
   const canCheck = !isSubmitted && !isUnanswered && !answerUnavailable;
   const offersCheck = !answerUnavailable;
   const offersSkipUnit = onSkipUnit !== undefined;
   const offersSkipEverything = onSkipEverything !== undefined;
   const isConfirming = confirmingScope !== null;
   const confirmation = isConfirming ? SKIP_CONFIRMATION[confirmingScope] : null;

   const offeredSteps = SCOPE_STEPS.filter((step) => {
      const isUnitStep = step.scope === "unit";
      const isEverythingStep = step.scope === "everything";

      if (isUnitStep) {
         return offersSkipUnit;
      }

      if (isEverythingStep) {
         return offersSkipEverything;
      }

      return true;
   });

   useEffect(() => {
      if (isConfirming) {
         keepAnsweringRef.current?.focus();
      }
   }, [isConfirming]);

   function pressStep(scope: SkipScope) {
      if (scope === "question") {
         setConfirmingScope(null);
         onNotLearned();

         return;
      }

      setConfirmingScope(scope);
   }

   function confirmSkip() {
      const scope = confirmingScope;
      setConfirmingScope(null);

      if (scope === "unit") {
         onSkipUnit?.();
      }

      if (scope === "everything") {
         onSkipEverything?.();
      }
   }

   function dismissOnEscape(event: KeyboardEvent<HTMLDivElement>) {
      if (event.key === "Escape") {
         event.stopPropagation();
         setConfirmingScope(null);
      }
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
         <QuestionTrack
            marks={Array.from({ length: item.diagnostic_cap }, (_, position) => ({
               state: trackState(position === item.diagnostic_position, position < item.diagnostic_position)
            }))}
            count={`${item.diagnostic_position} of at most ${item.diagnostic_cap} answered`}
         />

         <Workbench
            testId="diagnostic-item"
            data={{ "data-state": state }}
            stem={
               <div className="bench-part">
                  <p className="bench-tag">Solve</p>

                  <div className="question-stem">
                     <p className="item-stem" data-testid="item-stem">
                        <MathText text={item.stem} />
                     </p>

                     {item.figure_spec ? <FigureView spec={item.figure_spec} /> : null}
                  </div>
               </div>
            }
            work={
               <>
                  <p className="bench-tag" aria-hidden="true">
                     My answer
                  </p>

                  <div className="bench-answer" data-testid="math-answer">
                     <MathAnswerField key={item.id} label="My answer" onChange={onAnswerChange} onLoadFailure={onAnswerUnavailable} />

                     {answerUnavailable ? <p data-testid="answer-unavailable">{ANSWER_UNAVAILABLE}</p> : null}
                  </div>

                  <section className="scope-ladder" role="group" aria-label="Not learned yet" aria-describedby={`${ladderId}-lead`}>
                     <p className="scope-ladder-lead" id={`${ladderId}-lead`}>
                        Not learned yet? Say so and it moves on. Each rung reaches further than the one above it.
                     </p>

                     <ol className="scope-steps">
                        {offeredSteps.map((step, depth) => {
                           const isConfirmable = step.scope !== "question";
                           const isOpen = confirmingScope === step.scope;
                           const showsConfirmation = isOpen && confirmation !== null;
                           const reachId = `${ladderId}-${step.scope}-reach`;

                           return (
                              <li key={step.scope} className="scope-step" data-scope={step.scope} data-depth={depth}>
                                 <div className="scope-step-row">
                                    <button
                                       type="button"
                                       className="text-button scope-step-button"
                                       disabled={isSubmitted}
                                       aria-describedby={reachId}
                                       aria-expanded={isConfirmable ? isOpen : undefined}
                                       onClick={() => pressStep(step.scope)}
                                    >
                                       <Icon name={step.icon} />
                                       <span>{step.label}</span>
                                    </button>

                                    <span className="scope-step-reach" id={reachId}>
                                       {step.reach}
                                    </span>
                                 </div>

                                 {showsConfirmation ? (
                                    <div
                                       role="alertdialog"
                                       aria-label={confirmation.title}
                                       className="scope-confirm"
                                       data-scope={step.scope}
                                       data-testid={confirmation.testId}
                                       onKeyDown={dismissOnEscape}
                                    >
                                       <p>
                                          <strong>{confirmation.lead}</strong> {confirmation.body}
                                       </p>

                                       <div className="cluster scope-confirm-actions">
                                          <button ref={keepAnsweringRef} type="button" className="button-secondary button-small" onClick={() => setConfirmingScope(null)}>
                                             {KEEP_ANSWERING_LABEL}
                                          </button>

                                          <button
                                             type="button"
                                             className={step.scope === "everything" ? "text-button text-button-destructive" : "text-button"}
                                             disabled={isSubmitted}
                                             onClick={confirmSkip}
                                          >
                                             {confirmation.confirmLabel}
                                          </button>
                                       </div>
                                    </div>
                                 ) : null}
                              </li>
                           );
                        })}
                     </ol>
                  </section>
               </>
            }
            foot={
               offersCheck ? (
                  <button type="button" className="motion-instant-submit-answer button-primary" disabled={!canCheck} onClick={onCheck}>
                     {COMMIT_LABEL}
                  </button>
               ) : null
            }
         />
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
