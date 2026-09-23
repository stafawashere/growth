import { useCallback, useEffect, useRef, useState } from "react";
import {
   closeSession,
   openSession,
   readFeedback,
   readNextItem,
   readSession,
   submitAttempt,
   submitConfidence,
   submitErrorNote,
   submitSelfExplanation
} from "../api/client";
import type { AttemptAnswer } from "../api/client";
import type {
   AttemptResult,
   Confidence,
   FeedbackPayload,
   ServedItem,
   SessionPayload
} from "../api/types";
import { ElaboratedPanel } from "./ElaboratedPanel";
import { ErrorNoteField } from "./ErrorNoteField";
import { collectsConfidence, Item } from "./Item";
import { SelfExplanationPrompt } from "./SelfExplanationPrompt";
import { StepMarks } from "./StepMarks";

export const SET_FINISHED = "That is today's set finished.";

export const NEXT_LABEL = "Next item";

/* resumeSessionId names the open session GET /progress reported, and null opens a new one. It
   has no default, because opening a session writes a row and resuming one must not. */

export interface SessionScreenProps {
   resumeSessionId: string | null;
}

export function SessionScreen({ resumeSessionId }: SessionScreenProps) {
   const [session, setSession] = useState<SessionPayload | null>(null);
   const [item, setItem] = useState<ServedItem | null>(null);
   const [committed, setCommitted] = useState<AttemptResult | null>(null);
   const [feedback, setFeedback] = useState<FeedbackPayload | null>(null);
   const [feedbackUnreadable, setFeedbackUnreadable] = useState(false);
   const [confidence, setConfidence] = useState<Confidence | null>(null);
   const [answerMathJson, setAnswerMathJson] = useState<unknown>(null);
   const [selectedOptionId, setSelectedOptionId] = useState<string | null>(null);
   const [selfExplanation, setSelfExplanation] = useState("");
   const [answerUnavailable, setAnswerUnavailable] = useState(false);
   const [errorNote, setErrorNote] = useState("");
   const [finished, setFinished] = useState(false);

   const opened = useRef(false);
   const inFlight = useRef(false);
   const writtenForAttempt = useRef({ attemptId: "", note: false, explanation: false });

   const advance = useCallback(async (sessionId: string) => {
      const next = await readNextItem(sessionId);

      setCommitted(null);
      setFeedback(null);
      setFeedbackUnreadable(false);
      setConfidence(null);
      setAnswerMathJson(null);
      setSelectedOptionId(null);
      setSelfExplanation("");
      setErrorNote("");
      setAnswerUnavailable(false);

      if (next.item === null) {
         await closeSession(sessionId);

         setItem(null);
         setFinished(true);

         return;
      }

      setItem(next.item);
   }, []);

   useEffect(() => {
      if (opened.current) {
         return;
      }

      opened.current = true;

      const isResuming = resumeSessionId !== null;
      const reached = isResuming ? readSession(resumeSessionId) : openSession();

      reached.then((payload) => {
         setSession(payload);

         return advance(payload.id);
      });
   }, [advance, resumeSessionId]);

   const noteAnswerUnavailable = useCallback(() => {
      setAnswerUnavailable(true);
   }, []);

   /* The attempt is already written when feedback is read, so a refused read must not hold the
      student on an item they cannot commit again. No plan copy exists for a feedback screen that
      failed to load, so it shows no sentence and only the way on. */
   const showFeedback = useCallback(async (sessionId: string, attemptId: string) => {
      try {
         const payload = await readFeedback(sessionId, attemptId);

         setFeedback(payload);
      } catch {
         setFeedbackUnreadable(true);
      }
   }, []);

   const commit = useCallback(async () => {
      const isIdle = !inFlight.current;
      const canCommit = session !== null && item !== null && isIdle;

      if (!canCommit) {
         return;
      }

      inFlight.current = true;

      try {
         const isMcq = item.format === "mcq" && item.stage === "unsupported";
         const answer: AttemptAnswer = isMcq ? { option_id: selectedOptionId ?? "" } : { mathjson: answerMathJson };
         const ratesConfidence = collectsConfidence(item.stage) && confidence !== null;

         const result = await submitAttempt(session.id, {
            item_id: item.id,
            answer,
            confidence: ratesConfidence ? confidence : undefined
         });

         setCommitted(result);

         /* The attempt row the server wrote is what says whether the rating was recorded, so an
            attempt that came back unrated holds the feedback back until the student rates it. */
         const awaitsRating = collectsConfidence(result.served_stage) && result.confidence === null;

         if (awaitsRating) {
            return;
         }

         await showFeedback(session.id, result.id);
      } finally {
         inFlight.current = false;
      }
   }, [session, item, selectedOptionId, answerMathJson, confidence, showFeedback]);

   const rateConfidence = useCallback(
      async (value: Confidence) => {
         setConfidence(value);

         const isIdle = !inFlight.current;
         const isCommitted = session !== null && committed !== null;
         const awaitsRating =
            isCommitted && collectsConfidence(committed.served_stage) && committed.confidence === null;

         if (!awaitsRating || !isIdle) {
            return;
         }

         inFlight.current = true;

         try {
            const rated = await submitConfidence(session.id, committed.id, { confidence: value });

            setCommitted({ ...committed, confidence: rated.confidence });
            await showFeedback(session.id, committed.id);
         } catch {
            // no plan copy exists for a refused rating, so the prompt stays on screen to retry
         } finally {
            inFlight.current = false;
         }
      },
      [session, committed, showFeedback]
   );

   const moveOn = useCallback(async () => {
      const isIdle = !inFlight.current;
      const canMoveOn = session !== null && committed !== null && isIdle;

      if (!canMoveOn) {
         return;
      }

      const note = errorNote.trim();
      const wasCorrected = committed.correct === false;
      const owesNote = wasCorrected && note.length === 0;

      if (owesNote) {
         return;
      }

      const explanation = selfExplanation.trim();
      const wasInvited = feedback !== null && feedback.self_explanation_prompt !== null;
      const hasExplanation = wasInvited && explanation.length > 0;

      const isSameAttempt = writtenForAttempt.current.attemptId === committed.id;

      if (!isSameAttempt) {
         writtenForAttempt.current = { attemptId: committed.id, note: false, explanation: false };
      }

      const written = writtenForAttempt.current;
      const writesNote = wasCorrected && !written.note;
      const writesExplanation = hasExplanation && !written.explanation;

      inFlight.current = true;

      try {
         if (writesNote) {
            await submitErrorNote(session.id, committed.id, note);
            written.note = true;
         }

         if (writesExplanation) {
            await submitSelfExplanation(session.id, committed.id, { answer: explanation });
            written.explanation = true;
         }

         await advance(session.id);
      } catch {
         // no plan copy exists for a refused in-session request, so the feedback stays on screen to retry
      } finally {
         inFlight.current = false;
      }
   }, [session, committed, feedback, errorNote, selfExplanation, advance]);

   if (finished) {
      return (
         <div className="card">
            <p>{SET_FINISHED}</p>
         </div>
      );
   }

   if (item === null) {
      return <div />;
   }

   const showsFeedback = feedback !== null || feedbackUnreadable;
   const marksSteps = feedback !== null && feedback.stage !== "unsupported";
   const showsElaborated = feedback !== null && feedback.stage === "unsupported";

   /* 11 P1 scope item 10: one note per corrected item, written before the retry is scheduled. An
      item the student got right is requeued by nothing and asks for nothing. */
   const wasCorrected = committed !== null && committed.correct === false;
   const owesNote = wasCorrected && errorNote.trim().length === 0;
   const awaitsRating =
      committed !== null && collectsConfidence(committed.served_stage) && committed.confidence === null;

   return (
      <div>
         {showsFeedback ? (
            <section className="card feedback" data-testid="feedback">
               {marksSteps ? <StepMarks marks={feedback.step_marks} /> : null}

               {showsElaborated ? (
                  <ElaboratedPanel elaborated={feedback.elaborated} sentence={feedback.sentence} />
               ) : null}

               <SelfExplanationPrompt
                  prompt={feedback?.self_explanation_prompt ?? null}
                  value={selfExplanation}
                  onChange={setSelfExplanation}
               />

               {wasCorrected ? <ErrorNoteField value={errorNote} onChange={setErrorNote} /> : null}

               <button
                  type="button"
                  className="motion-instant-question-move button-primary"
                  disabled={owesNote}
                  onClick={moveOn}
               >
                  {NEXT_LABEL}
               </button>
            </section>
         ) : (
            <Item
               item={item}
               onAnswerChange={setAnswerMathJson}
               answerUnavailable={answerUnavailable}
               onAnswerUnavailable={noteAnswerUnavailable}
               selectedOptionId={selectedOptionId}
               onOptionChange={setSelectedOptionId}
               confidence={confidence}
               onConfidenceChange={rateConfidence}
               selfExplanation={selfExplanation}
               onSelfExplanationChange={setSelfExplanation}
               onCommit={commit}
               awaitingConfidence={awaitsRating}
            />
         )}
      </div>
   );
}