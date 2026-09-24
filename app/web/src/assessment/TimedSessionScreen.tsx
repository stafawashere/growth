import { useEffect, useRef, useState } from "react";

import {
   finishMock,
   readAssessmentShape,
   readTimedResult,
   readTimedSession,
   saveQuestion,
   startPart,
   submitPart,
   type CaptureMode,
   type SaveQuestionFields
} from "../api/client";
import type {
   AssessmentPart,
   AssessmentResult,
   AssessmentSession,
   AssessmentShape,
   FreeResponseCapture,
   FrqQuestion,
   TimedKind
} from "../api/types";
import { CaptureScreen } from "../frq/CaptureScreen";
import { refusalText, withLabel } from "./format";
import { PartRunner } from "./PartRunner";

/* A full mock or a part drill, from the first part's start to the result. Parts run in order and
   a closed part is never offered again. The only way forward is the next part, and there is no
   control that leads back. Free-response answers are written on paper during the part and
   captured once it has closed, through the same capture, read-back and grading screens the unit
   check uses, for the attempt the server opened when the part started. Each capture entry carries
   its question, so a reload after the part closed still reaches the capture step. */

export interface TimedSessionScreenProps {
   kind: TimedKind;
   sessionId: string;
   initial?: AssessmentSession;
   pollMilliseconds?: number;
   listPollMilliseconds?: number;
   onShowResult: (result: AssessmentResult) => void;
}

const GRADING_STATE_WORDS: Record<string, string> = {
   capturing: "not captured yet",
   awaiting_confirmation: "waiting for you to confirm the read-back",
   confirmed: "confirmed, being graded",
   partly_graded: "partly graded",
   graded: "graded",
   grading_split: "graded, with a provisional point",
   dispute: "being re-read"
};

const DEFAULT_LIST_POLL_MILLISECONDS = 5000;

/* Confirmed means the grader has the answer and has not finished, so the list keeps re-reading
   the session until the state moves on. */
function awaitsGrading(session: AssessmentSession) {
   return session.parts.some((part) => (part.capture ?? []).some((capture) => capture.grading_state === "confirmed"));
}

function gradingStateText(state: string | null) {
   if (state === null) {
      return "not started";
   }

   return GRADING_STATE_WORDS[state] ?? state.replace(/_/g, " ");
}

function captureModeOf(session: AssessmentSession): CaptureMode {
   return session.capture_mode === "typed" ? "typed" : "photo";
}

function asQuestion(capture: FreeResponseCapture): FrqQuestion {
   const item = capture.item;

   return {
      id: item.id,
      archetype_id: item.archetype_id,
      calculator_status: item.calculator_status,
      stem: item.stem,
      parts: item.parts,
      attempt_id: capture.attempt_id,
      grading_state: capture.grading_state
   };
}

/* A section's question count is the sum over its parts in the exam shape, which a drill's session
   alone cannot give because it holds one part. */
export function sectionCountOf(shape: AssessmentShape | null, section: string) {
   if (shape === null) {
      return null;
   }

   return shape.parts.filter((part) => part.section === section).reduce((total, part) => total + part.question_count, 0);
}

function PartFacts(props: { part: AssessmentPart }) {
   const { part } = props;

   return (
      <>
         <p>
            {part.label}: {part.question_count} questions, {part.minutes} minutes.
         </p>

         <p className="calculator-label">{part.calculator_label}</p>

         {part.calculator_note !== null ? <p>{part.calculator_note}</p> : null}
      </>
   );
}

function CaptureList(props: {
   parts: AssessmentPart[];
   onCapture: (capture: FreeResponseCapture) => void;
}) {
   const entries = props.parts
      .filter((part) => part.status === "closed")
      .flatMap((part) => part.capture ?? []);
   const hasEntries = entries.length > 0;

   if (!hasEntries) {
      return null;
   }

   return (
      <section data-testid="capture-list">
         <h2 className="section-heading">Free-response capture</h2>

         <p className="muted">
            Each answer you wrote in the booklet is captured and graded point by point. Nothing is scored until you
            confirm what was read from your page.
         </p>

         <ul className="review-list">
            {entries.map((capture) => {
               const hasAttempt = capture.attempt_id !== null;

               return (
                  <li key={capture.number}>
                     <span>
                        Question {capture.number}, {gradingStateText(capture.grading_state)}
                     </span>

                     {hasAttempt ? (
                        <button type="button" className="text-button" onClick={() => props.onCapture(capture)}>
                           Capture Question {capture.number}
                        </button>
                     ) : null}
                  </li>
               );
            })}
         </ul>
      </section>
   );
}

export function TimedSessionScreen({ kind, sessionId, initial, pollMilliseconds, listPollMilliseconds, onShowResult }: TimedSessionScreenProps) {
   const [session, setSession] = useState<AssessmentSession | null>(initial ?? null);
   const [problem, setProblem] = useState<string | null>(null);
   const [loadFailed, setLoadFailed] = useState(false);
   const [capturing, setCapturing] = useState<FreeResponseCapture | null>(null);
   const pendingSaves = useRef<Promise<unknown>>(Promise.resolve());
   const [shape, setShape] = useState<AssessmentShape | null>(null);

   function accept(payload: AssessmentSession) {
      setSession(payload);
   }

   async function reread() {
      try {
         accept(await readTimedSession(kind, sessionId));
      } catch {
         setLoadFailed(true);
      }
   }

   /* Read once on arrival. Every later read follows a server reply or the clock reaching zero. */
   useEffect(() => {
      if (initial === undefined) {
         reread();
      }

      readAssessmentShape().then(setShape, () => undefined);
   }, []);

   const showsCaptureList = session !== null && capturing === null && !session.parts.some((part) => part.status === "open");
   const keepsPolling = showsCaptureList && session !== null && awaitsGrading(session);

   useEffect(() => {
      if (!keepsPolling) {
         return undefined;
      }

      const poller = setInterval(reread, listPollMilliseconds ?? DEFAULT_LIST_POLL_MILLISECONDS);

      return () => clearInterval(poller);
   }, [keepsPolling, listPollMilliseconds]);

   function backToCaptureList() {
      setCapturing(null);
      reread();
   }

   async function refused(failure: unknown, fallback: string) {
      setProblem(refusalText(failure, fallback));
      await reread();
   }

   async function start(position: number) {
      setProblem(null);

      try {
         accept(await startPart(kind, sessionId, position));
      } catch (failure) {
         await refused(failure, "The part could not be started.");
      }
   }

   /* Saves go out one after another, and a submit or a re-read at zero waits for them, so the
      visit that ended with the submit is recorded before the part closes. */
   function save(position: number, number: number, fields: SaveQuestionFields) {
      pendingSaves.current = pendingSaves.current
         .then(() => saveQuestion(kind, sessionId, position, number, fields))
         .catch((failure) => refused(failure, "Your work on that question could not be saved."));
   }

   async function timeUp() {
      await pendingSaves.current;
      await reread();
   }

   async function submit(position: number) {
      setProblem(null);

      try {
         await pendingSaves.current;
         accept(await submitPart(kind, sessionId, position));
      } catch (failure) {
         await refused(failure, "The part could not be submitted.");
      }
   }

   async function showResult() {
      setProblem(null);

      try {
         const result = kind === "mocks" ? await finishMock(sessionId) : await readTimedResult(kind, sessionId);

         onShowResult(result);
      } catch (failure) {
         setProblem(refusalText(failure, "The result could not be read."));
      }
   }

   if (session === null) {
      return loadFailed ? (
         <section className="card">
            <p className="muted">This timed session could not be loaded.</p>
         </section>
      ) : (
         <section aria-busy="true" data-testid="timed-waiting" />
      );
   }

   const problemLine = problem !== null ? <p role="alert">{problem}</p> : null;
   if (capturing !== null) {
      return (
         <>
            <button type="button" className="text-button" onClick={backToCaptureList}>
               Back to free-response capture
            </button>

            <CaptureScreen
               key={capturing.number}
               sessionId={session.id}
               question={asQuestion(capturing)}
               captureMode={captureModeOf(session)}
               pollMilliseconds={pollMilliseconds}
            />
         </>
      );
   }

   const openPart = session.parts.find((part) => part.status === "open");
   const closedParts = session.parts.filter((part) => part.status === "closed");
   const lastClosed = closedParts.length > 0 ? closedParts[closedParts.length - 1] : null;
   const nextPart = session.parts.find((part) => part.status === "not_started");

   if (openPart !== undefined) {
      return (
         <>
            {problemLine}

            {lastClosed !== null ? (
               <p className="notice" data-testid="closed-part-note">
                  {withLabel(session.closed_part_note, lastClosed.label)}
               </p>
            ) : null}

            <PartRunner
               key={openPart.position}
               part={openPart}
               radianNote={session.radian_note}
               sectionCount={sectionCountOf(shape, openPart.section)}
               onSave={(number, fields) => save(openPart.position, number, fields)}
               onSubmit={() => submit(openPart.position)}
               onTimeUp={timeUp}
            />
         </>
      );
   }

   if (nextPart !== undefined && lastClosed === null) {
      return (
         <section className="card" data-testid="part-intro">
            <h1 className="screen-title">{kind === "mocks" ? "Mock exam" : "Part drill"}</h1>

            {problemLine}

            <PartFacts part={nextPart} />

            <p className="muted">{session.reference_sheet.note}</p>

            <p>The timer starts when you start the part, and a submitted part cannot be reopened.</p>

            <button type="button" className="button-primary" onClick={() => start(nextPart.position)}>
               Start the part
            </button>
         </section>
      );
   }

   if (nextPart !== undefined && lastClosed !== null) {
      return (
         <section className="card" data-testid="break-screen">
            <h1 className="screen-title">Break</h1>

            {problemLine}

            <p data-testid="break-note">{withLabel(session.break_note, lastClosed.label)}</p>

            {lastClosed.closed_by === "time" ? <p className="muted">Time ran out on {lastClosed.label}, so it closed as you left it.</p> : null}

            <h2 className="section-heading">Next</h2>

            <PartFacts part={nextPart} />

            <button type="button" className="button-primary" onClick={() => start(nextPart.position)}>
               Start next part
            </button>

            <CaptureList parts={session.parts} onCapture={setCapturing} />
         </section>
      );
   }

   return (
      <section className="card" data-testid="timed-finished">
         <h1 className="screen-title">Every part is closed</h1>

         {problemLine}

         {lastClosed !== null ? <p>{withLabel(session.closed_part_note, lastClosed.label)}</p> : null}

         <CaptureList parts={session.parts} onCapture={setCapturing} />

         <button type="button" className="button-primary" onClick={showResult}>
            See the result
         </button>
      </section>
   );
}
