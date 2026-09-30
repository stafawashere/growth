import { useEffect, useId, useRef, useState, type KeyboardEvent, type MouseEvent } from "react";
import { createPortal } from "react-dom";

import { answerCalculatorDrill } from "../api/client";
import type { CalculatorAnswerPayload, CalculatorDrill } from "../api/types";
import { DesmosPanel } from "../input/DesmosPanel";
import { MathAnswerField } from "../input/MathAnswerField";
import { MathText } from "../math/MathText";
import { Icon, type IconName } from "../ui/Icon";
import { DrillClock } from "./DrillClock";
import {
   ANSWER_FAILED,
   CAPABILITY_NAMES,
   CHANGE_CAPABILITY_LABEL,
   CHECK_LABEL,
   EXPECTED_SETUP_LEAD,
   NEXT_LABEL,
   OFFLINE_SENTENCE,
   RADIAN_NOTE,
   RESULT_LABEL,
   SETUP_LABEL,
   SETUP_TEXT,
   SKIP_TO_RESULT,
   TASK_HEADING,
   acceptedFormsText,
   budgetLine,
   secondsText,
   setupState,
   valueVerdictText,
   type SetupState
} from "./words";

/* One drill task (docs/calculator/design.md, The drills and Keyboard). The task, then Desmos, then
   the two fields in document order, which is the tab order; from 1100 px app.css sets the task and
   the fields on the left and Desmos on the right. The clock runs from the task's first render and
   the elapsed time is measured with performance.now(). Nothing typed is refused here: an empty
   result or setup is sent as it is and the server decides. After Check the screen shows the result
   line with both accepted forms, the setup line, and the time, announced through a live region. */

/* app.css's wide breakpoint, where Desmos opens beside the task without being asked. */
export const WIDE_LAYOUT_MIN_WIDTH = 1100;

function opensDesmosByDefault() {
   return typeof window !== "undefined" && window.innerWidth >= WIDE_LAYOUT_MIN_WIDTH;
}

function browserIsOffline() {
   return typeof navigator !== "undefined" && navigator.onLine === false;
}

function inline(tex: string) {
   return `\\(${tex}\\)`;
}

const SETUP_ICONS: Record<SetupState, IconName> = {
   equivalent: "check",
   not_equivalent: "close",
   missing: "minus",
   unreadable: "question"
};

const SETUP_TONE: Record<SetupState, string> = {
   equivalent: "text-correct",
   not_equivalent: "text-incorrect",
   missing: "text-incorrect",
   unreadable: "muted"
};

function VerdictLine(props: { icon: IconName; tone: string; text: string; testId: string }) {
   return (
      <p className="verdict" data-testid={props.testId}>
         <Icon name={props.icon} className={props.tone} />
         <span>{props.text}</span>
      </p>
   );
}

export interface DrillScreenProps {
   drill: CalculatorDrill;
   offline: boolean;
   showsBudget: boolean;
   focusTaskOnArrival: boolean;
   onAnswered: (answer: CalculatorAnswerPayload) => void;
   onNext: () => void;
   onChangeCapability: () => void;
   clockSlot?: HTMLElement | null;
   now?: () => number;
}

function defaultNow() {
   return performance.now();
}

export function DrillScreen(props: DrillScreenProps) {
   const { drill, onAnswered } = props;
   const now = props.now ?? defaultNow;
   const [startedAt] = useState(() => now());
   const [stoppedAt, setStoppedAt] = useState<number | null>(null);
   const [value, setValue] = useState("");
   const [setup, setSetup] = useState<unknown>(null);
   const [answer, setAnswer] = useState<CalculatorAnswerPayload | null>(null);
   const [isChecking, setIsChecking] = useState(false);
   const [failed, setFailed] = useState(false);
   const [wentOffline, setWentOffline] = useState(() => props.offline || browserIsOffline());
   const [openByDefault] = useState(opensDesmosByDefault);
   const desmosWasOpen = useRef(false);
   const taskRef = useRef<HTMLDivElement | null>(null);
   const resultLineRef = useRef<HTMLDivElement | null>(null);
   const resultFieldRef = useRef<HTMLInputElement | null>(null);
   const resultFieldId = useId();
   const taskHeadingId = useId();

   const isAnswered = answer !== null;

   useEffect(() => {
      if (props.offline) {
         setWentOffline(true);
      }
   }, [props.offline]);

   useEffect(() => {
      function markOffline() {
         setWentOffline(true);
      }

      window.addEventListener("offline", markOffline);

      return () => window.removeEventListener("offline", markOffline);
   }, []);

   useEffect(() => {
      if (props.focusTaskOnArrival) {
         taskRef.current?.focus();
      }
   }, [props.focusTaskOnArrival]);

   useEffect(() => {
      if (isAnswered) {
         resultLineRef.current?.focus();
      }
   }, [isAnswered]);

   function noteDesmos(isOpen: boolean) {
      if (isOpen) {
         desmosWasOpen.current = true;
      }
   }

   async function check() {
      const isBusy = isChecking || isAnswered;

      if (isBusy) {
         return;
      }

      const checkedAt = now();
      const elapsedMs = Math.max(0, Math.round(checkedAt - startedAt));

      setIsChecking(true);
      setFailed(false);

      try {
         const verdict = await answerCalculatorDrill(drill.drill_id, {
            value,
            setup_mathjson: setup ?? null,
            elapsed_ms: elapsedMs,
            desmos_open: desmosWasOpen.current
         });

         setStoppedAt(checkedAt);
         setAnswer(verdict);
         onAnswered(verdict);
      } catch {
         setFailed(true);
      } finally {
         setIsChecking(false);
      }
   }

   function checkOnEnter(event: KeyboardEvent<HTMLInputElement>) {
      if (event.key !== "Enter") {
         return;
      }

      event.preventDefault();
      void check();
   }

   function skipToResult(event: MouseEvent<HTMLAnchorElement>) {
      event.preventDefault();
      resultFieldRef.current?.focus();
   }

   const clock = <DrillClock startedAt={startedAt} stoppedAt={stoppedAt} now={now} />;
   const clockInSlot = props.clockSlot !== undefined && props.clockSlot !== null;
   const setupShape = answer === null ? null : setupState(answer.setup);
   const showsExpectedSetup = setupShape === "not_equivalent";

   return (
      <section className="drill-screen" data-testid="drill-screen" aria-labelledby={taskHeadingId}>
         <a className="skip-link" href={`#${resultFieldId}`} onClick={skipToResult}>
            {SKIP_TO_RESULT}
         </a>

         <header className="part-header drill-head">
            <h2 className="section-heading" id={taskHeadingId}>
               {CAPABILITY_NAMES[drill.capability]}
            </h2>

            {clockInSlot ? createPortal(clock, props.clockSlot as HTMLElement) : clock}
         </header>

         <div className="drill-layout">
            <div className="drill-task stack stack-tight" ref={taskRef} tabIndex={-1} data-testid="drill-task">
               <span className="eyebrow">{TASK_HEADING}</span>

               <p className="item-stem">
                  <MathText text={drill.prompt} />
               </p>

               {drill.radian_sensitive ? <p className="helper">{RADIAN_NOTE}</p> : null}
            </div>

            <div className="drill-desmos">
               {wentOffline ? (
                  <p className="callout" data-testid="drill-offline">
                     {OFFLINE_SENTENCE}
                  </p>
               ) : (
                  <DesmosPanel openByDefault={openByDefault} onOpenChange={noteDesmos} />
               )}
            </div>

            <div className="drill-answer stack">
               <div className="form-field">
                  <label className="field-label" htmlFor={resultFieldId}>
                     {RESULT_LABEL}
                  </label>

                  <input
                     id={resultFieldId}
                     ref={resultFieldRef}
                     className="input"
                     type="text"
                     inputMode="decimal"
                     autoComplete="off"
                     spellCheck={false}
                     value={value}
                     readOnly={isAnswered}
                     onChange={(event) => setValue(event.target.value)}
                     onKeyDown={checkOnEnter}
                  />
               </div>

               <MathAnswerField label={SETUP_LABEL} onChange={setSetup} onLoadFailure={() => setSetup(null)} />

               {isAnswered ? null : (
                  <div>
                     <button type="button" className="button-primary" disabled={isChecking} onClick={() => void check()}>
                        {CHECK_LABEL}
                     </button>
                  </div>
               )}

               {failed ? (
                  <p role="alert" className="notice">
                     {ANSWER_FAILED}
                  </p>
               ) : null}

               <div className="drill-verdicts stack stack-tight" aria-live="polite" data-testid="drill-verdicts">
                  {answer !== null && setupShape !== null ? (
                     <>
                        <div className="stack stack-tight" ref={resultLineRef} tabIndex={-1} data-testid="drill-result-line">
                           <VerdictLine
                              icon={answer.value.correct ? "check" : "close"}
                              tone={answer.value.correct ? "text-correct" : "text-incorrect"}
                              text={valueVerdictText(answer.value)}
                              testId="drill-value-verdict"
                           />

                           <p className="helper" data-testid="drill-accepted-forms">
                              {acceptedFormsText(answer.value.rounded, answer.value.truncated)}
                           </p>
                        </div>

                        <div className="stack stack-tight" data-testid="drill-setup-line">
                           <VerdictLine icon={SETUP_ICONS[setupShape]} tone={SETUP_TONE[setupShape]} text={SETUP_TEXT[setupShape]} testId="drill-setup-verdict" />

                           {showsExpectedSetup ? (
                              <p data-testid="drill-expected-setup">
                                 {EXPECTED_SETUP_LEAD} <MathText text={inline(answer.setup.key_latex)} />
                              </p>
                           ) : null}
                        </div>

                        <p data-testid="drill-time">{secondsText(answer.elapsed_ms)}</p>

                        {props.showsBudget ? (
                           <p className="helper" data-testid="drill-budget">
                              {budgetLine(answer.budget_seconds["I-B"])}
                           </p>
                        ) : null}
                     </>
                  ) : null}
               </div>

               {isAnswered ? (
                  <div className="cluster">
                     <button type="button" className="button-primary" onClick={props.onNext}>
                        {NEXT_LABEL}
                     </button>

                     <button type="button" className="button-secondary" onClick={props.onChangeCapability}>
                        {CHANGE_CAPABILITY_LABEL}
                     </button>
                  </div>
               ) : null}
            </div>
         </div>
      </section>
   );
}
