import { useCallback, useEffect, useRef, useState } from "react";
import {
   closeSession,
   openSession,
   readFeedback,
   readNextItem,
   submitAttempt,
   submitConfidence,
   submitErrorNote
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
import { collectsConfidence, Item, type WorkedStep } from "./Item";
import { SelfExplanationPrompt } from "./SelfExplanationPrompt";
import { StepMarks } from "./StepMarks";

export const SET_FINISHED = "That is today's set finished.";

export const NEXT_LABEL = "Next item";

/* Neither the worked steps nor the pre-submission self explanation prompt reach the client from
   any P1 route, so both arrive as required functions on this screen. Whoever mounts it has to
   answer for where they come from; nothing here fills them in. */

export interface SessionScreenProps {
   workedStepsFor: (item: ServedItem) => WorkedStep[];
   selfExplanationPromptFor: (item: ServedItem) => string | null;
}

export function SessionScreen({ workedStepsFor, selfExplanationPromptFor }: SessionScreenProps) {
   const [session, setSession] = useState<SessionPayload | null>(null);
   const [item, setItem] = useState<ServedItem | null>(null);
   const [committed, setCommitted] = useState<AttemptResult | null>(null);
   const [feedback, setFeedback] = useState<FeedbackPayload | null>(null);
   const [confidence, setConfidence] = useState<Confidence | null>(null);
   const [answerMathJson, setAnswerMathJson] = useState<unknown>(null);
   const [selectedOptionId, setSelectedOptionId] = useState<string | null>(null);
   const [selfExplanation, setSelfExplanation] = useState("");
   const [answerUnavailable, setAnswerUnavailable] = useState(false);
   const [errorNote, setErrorNote] = useState("");
   const [finished, setFinished] = useState(false);

   const opened = useRef(false);
   const inFlight = useRef(false);

   const advance = useCallback(async (sessionId: string) => {
      const next = await readNextItem(sessionId);

      setCommitted(null);
      setFeedback(null);
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

      openSession().then((payload) => {
         setSession(payload);

         return advance(payload.id);
      });
   }, [advance]);

   const noteAnswerUnavailable = useCallback(() => {
      setAnswerUnavailable(true);
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

         const payload = await readFeedback(session.id, result.id);

         setFeedback(payload);
      } finally {
         inFlight.current = false;
      }
   }, [session, item, selectedOptionId, answerMathJson, confidence]);

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
            const payload = await readFeedback(session.id, committed.id);

            setCommitted({ ...committed, confidence: rated.confidence });
            setFeedback(payload);
         } finally {
            inFlight.current = false;
         }
      },
      [session, committed]
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

      inFlight.current = true;

      try {
         if (wasCorrected) {
            await submitErrorNote(session.id, committed.id, note);
         }

         await advance(session.id);
      } finally {
         inFlight.current = false;
      }
   }, [session, committed, errorNote, advance]);

   if (finished) {
      return (
         <main>
            <p>{SET_FINISHED}</p>
         </main>
      );
   }

   if (item === null) {
      return <main />;
   }

   const showsFeedback = feedback !== null;
   const marksSteps = showsFeedback && feedback.stage !== "unsupported";

   /* 11 P1 scope item 10: one note per corrected item, written before the retry is scheduled. An
      item the student got right is requeued by nothing and asks for nothing. */
   const wasCorrected = committed !== null && committed.correct === false;
   const owesNote = wasCorrected && errorNote.trim().length === 0;
   const awaitsRating =
      committed !== null && collectsConfidence(committed.served_stage) && committed.confidence === null;

   return (
      <main>
         {showsFeedback ? (
            <section data-testid="feedback">
               {marksSteps ? <StepMarks marks={feedback.step_marks} /> : null}

               {feedback.stage === "unsupported" ? (
                  <ElaboratedPanel elaborated={feedback.elaborated} sentence={feedback.sentence} />
               ) : null}

               <SelfExplanationPrompt
                  prompt={feedback.self_explanation_prompt}
                  value={selfExplanation}
                  onChange={setSelfExplanation}
               />

               {wasCorrected ? <ErrorNoteField value={errorNote} onChange={setErrorNote} /> : null}

               <button
                  type="button"
                  className="motion-instant-question-move"
                  disabled={owesNote}
                  onClick={moveOn}
               >
                  {NEXT_LABEL}
               </button>
            </section>
         ) : (
            <Item
               item={item}
               workedSteps={workedStepsFor(item)}
               selfExplanationPrompt={selfExplanationPromptFor(item)}
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
      </main>
   );
}