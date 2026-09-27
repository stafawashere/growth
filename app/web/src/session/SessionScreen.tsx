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
import { FigureView } from "../figures/FigureView";
import { MathText } from "../math/MathText";
import { MathValue } from "../math/MathValue";
import { ActionFailed, LoadFailed, Loading } from "../status/LoadState";
import { CONFIDENCE_CHOICES } from "./ConfidencePrompt";
import { ElaboratedPanel } from "./ElaboratedPanel";
import { ErrorNoteField } from "./ErrorNoteField";
import { collectsConfidence, Item, servesChoice } from "./Item";
import { SelfExplanationPrompt } from "./SelfExplanationPrompt";
import { StepMarks } from "./StepMarks";

export const SET_FINISHED = "That is today's set finished.";

export const SET_STOPPED = "You stopped here for today.";

export const STOP_LABEL = "I want to stop here";

export const STOP_CONFIRM_LABEL = "Stop and close this set";

export const KEEP_GOING_LABEL = "Keep going";

export const YOU_WROTE_LABEL = "You wrote";

const OPTION_KEYS = ["a", "b", "c", "d", "e"];

interface Remaining {
   items: number;
   minutes: number;
}

/* GET /sessions/{id} lists the queue slots not yet answered, the current one included, and
   queue.forecasts holds the minute forecast per archetype, so the two give what is left. */
export function remainingFrom(payload: SessionPayload): Remaining {
   const minutes = payload.remaining.reduce((total, slot) => total + (payload.queue.forecasts[slot.archetype_id] ?? 0), 0);

   return { items: payload.remaining.length, minutes: Math.ceil(minutes) };
}

export function remainingSentence(remaining: Remaining) {
   const itemWord = remaining.items === 1 ? "item" : "items";
   const minuteWord = remaining.minutes === 1 ? "minute" : "minutes";
   const hasForecast = remaining.minutes > 0;

   if (!hasForecast) {
      return `${remaining.items} ${itemWord} left in this set`;
   }

   return `${remaining.items} ${itemWord} left in this set, about ${remaining.minutes} ${minuteWord}`;
}

export function workedSentence(items: number) {
   const itemWord = items === 1 ? "item" : "items";

   return `You worked through ${items} ${itemWord} in this sitting.`;
}

export function correctedSentence(corrected: number) {
   const isOne = corrected === 1;

   if (isOne) {
      return "The one you corrected comes back in Review, with your note.";
   }

   return `The ${corrected} you corrected come back in Review, with your notes.`;
}

/* The keys a whole item can be answered with. A key typed into a field is the student's text, so
   only Enter is read there, and only from the math field, where it has no other use. */
function isTypingTarget(target: HTMLElement) {
   return target.matches("textarea, select, input:not([type='radio']):not([type='checkbox'])");
}

function isActivatingTarget(target: HTMLElement) {
   return target.matches("button, a[href], summary");
}

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
   const [stopped, setStopped] = useState(false);
   const [isConfirmingStop, setIsConfirmingStop] = useState(false);
   const [loadFailed, setLoadFailed] = useState(false);
   const [actionFailed, setActionFailed] = useState(false);
   const [remaining, setRemaining] = useState<Remaining | null>(null);
   const [worked, setWorked] = useState({ items: 0, corrected: 0 });
   const [openAttempt, setOpenAttempt] = useState(0);

   const opened = useRef(false);
   const shortcut = useRef<(event: KeyboardEvent) => void>(() => undefined);
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

      Promise.resolve()
         .then(() => readSession(sessionId))
         .then((payload) => {
            if (payload) {
               setRemaining(remainingFrom(payload));
            }
         })
         .catch(() => undefined);
   }, []);

   useEffect(() => {
      if (opened.current) {
         return;
      }

      opened.current = true;

      const isResuming = resumeSessionId !== null;
      const reached = isResuming ? readSession(resumeSessionId) : openSession();

      reached
         .then((payload) => {
            setSession(payload);

            return advance(payload.id);
         })
         .catch(() => setLoadFailed(true));
   }, [advance, resumeSessionId, openAttempt]);

   function retryLoading() {
      setLoadFailed(false);

      if (session !== null) {
         advance(session.id).catch(() => setLoadFailed(true));

         return;
      }

      opened.current = false;
      setOpenAttempt((attempt) => attempt + 1);
   }

   /* The keys are read on the document, because after a page loads focus sits on the body, outside
      any element of this screen. */
   useEffect(() => {
      const listener = (event: KeyboardEvent) => shortcut.current(event);

      document.addEventListener("keydown", listener);

      return () => {
         document.removeEventListener("keydown", listener);
      };
   }, []);

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
      setActionFailed(false);

      try {
         const isMcq = servesChoice(item);
         const answer: AttemptAnswer = isMcq ? { option_id: selectedOptionId ?? "" } : { mathjson: answerMathJson };
         const ratesConfidence = collectsConfidence(item.stage) && confidence !== null;

         const result = await submitAttempt(session.id, {
            item_id: item.id,
            answer,
            confidence: ratesConfidence ? confidence : undefined
         });

         setCommitted(result);
         setWorked((sofar) => ({
            items: sofar.items + 1,
            corrected: sofar.corrected + (result.correct === false ? 1 : 0)
         }));

         /* The attempt row the server wrote is what says whether the rating was recorded, so an
            attempt that came back unrated holds the feedback back until the student rates it. */
         const awaitsRating = collectsConfidence(result.served_stage) && result.confidence === null;

         if (awaitsRating) {
            return;
         }

         await showFeedback(session.id, result.id);
      } catch {
         setActionFailed(true);
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
         setActionFailed(false);

         try {
            const rated = await submitConfidence(session.id, committed.id, { confidence: value });

            setCommitted({ ...committed, confidence: rated.confidence });
            await showFeedback(session.id, committed.id);
         } catch {
            setActionFailed(true);
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
      setActionFailed(false);

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
         setActionFailed(true);
      } finally {
         inFlight.current = false;
      }
   }, [session, committed, feedback, errorNote, selfExplanation, advance]);

   const stop = useCallback(async () => {
      const isIdle = !inFlight.current;
      const canStop = session !== null && isIdle;

      if (!canStop) {
         return;
      }

      inFlight.current = true;
      setActionFailed(false);

      try {
         await closeSession(session.id);

         setItem(null);
         setStopped(true);
         setFinished(true);
      } catch {
         setActionFailed(true);
      } finally {
         inFlight.current = false;
         setIsConfirmingStop(false);
      }
   }, [session]);

   shortcut.current = () => undefined;

   if (finished) {
      return (
         <section className="card session-end" data-testid="session-end">
            <h1 className="screen-title">{stopped ? SET_STOPPED : SET_FINISHED}</h1>

            {worked.items > 0 ? <p>{workedSentence(worked.items)}</p> : null}

            {worked.corrected > 0 ? <p>{correctedSentence(worked.corrected)}</p> : null}

            <p className="muted">Home shows what is due next, in minutes, whenever you open it.</p>
         </section>
      );
   }

   if (loadFailed) {
      return <LoadFailed testId="session-failed" onRetry={retryLoading} />;
   }

   if (item === null) {
      return <Loading testId="session-waiting" />;
   }

   const showsFeedback = feedback !== null || feedbackUnreadable;
   const hasFigure = item.figure_spec !== null && item.figure_spec !== undefined;
   const marksSteps = feedback !== null && feedback.stage !== "unsupported";
   const showsElaborated = feedback !== null && feedback.stage === "unsupported";

   /* 11 P1 scope item 10: one note per corrected item, written before the retry is scheduled. An
      item the student got right is requeued by nothing and asks for nothing. */
   const wasCorrected = committed !== null && committed.correct === false;
   const owesNote = wasCorrected && errorNote.trim().length === 0;
   const awaitsRating =
      committed !== null && collectsConfidence(committed.served_stage) && committed.confidence === null;

   const choiceServed = servesChoice(item);
   const chosenOption = choiceServed ? (item.options ?? []).find((option) => option.id === selectedOptionId) ?? null : null;
   const wroteMath = !choiceServed && answerMathJson !== null;
   const showsWhatWasWritten = chosenOption !== null || wroteMath;

   const shownItem = item;

   shortcut.current = onShortcut;

   function onShortcut(event: KeyboardEvent) {
      const target = event.target as HTMLElement;
      const hasModifier = event.altKey || event.ctrlKey || event.metaKey;
      const isInMathField = target.tagName.toLowerCase() === "math-field";
      const isIgnored = hasModifier || event.defaultPrevented || isTypingTarget(target) || isActivatingTarget(target);

      if (isIgnored) {
         return;
      }

      const key = event.key.toLowerCase();
      const isEnter = key === "enter";

      if (isEnter) {
         const canMoveOn = showsFeedback;
         const canCommit = !showsFeedback && committed === null;

         if (canMoveOn || canCommit) {
            event.preventDefault();
         }

         if (canMoveOn) {
            moveOn();
         }

         if (canCommit) {
            commit();
         }

         return;
      }

      const isAnswering = !isInMathField && !showsFeedback;

      if (!isAnswering) {
         return;
      }

      const confidenceIndex = ["1", "2", "3"].indexOf(key);
      const ratesConfidence = confidenceIndex >= 0 && collectsConfidence(shownItem.stage);

      if (ratesConfidence) {
         event.preventDefault();
         rateConfidence(CONFIDENCE_CHOICES[confidenceIndex].value);

         return;
      }

      const optionIndex = OPTION_KEYS.indexOf(key);
      const options = shownItem.options ?? [];
      const picksOption = choiceServed && committed === null && optionIndex >= 0 && optionIndex < options.length;

      if (picksOption) {
         event.preventDefault();
         setSelectedOptionId(options[optionIndex].id);
      }
   }

   return (
      <div>
         <div className="session-meta">
            <span className="badge">Stage: {item.stage}</span>

            {remaining !== null ? (
               <span className="muted" data-testid="session-remaining">
                  {remainingSentence(remaining)}
               </span>
            ) : null}

            {isConfirmingStop ? null : (
               <button type="button" className="text-button session-stop" onClick={() => setIsConfirmingStop(true)}>
                  {STOP_LABEL}
               </button>
            )}
         </div>

         {isConfirmingStop ? (
            <div role="alertdialog" aria-label="Stop this set" className="notice notice-framed" data-testid="stop-confirmation">
               <p>This closes today&apos;s set. What you answered is kept, and home builds the next set from it.</p>

               <div className="choice-row">
                  <button type="button" className="button-primary" onClick={stop}>
                     {STOP_CONFIRM_LABEL}
                  </button>

                  <button type="button" className="text-button" onClick={() => setIsConfirmingStop(false)}>
                     {KEEP_GOING_LABEL}
                  </button>
               </div>
            </div>
         ) : null}

         {actionFailed ? <ActionFailed /> : null}

         {showsFeedback ? (
            <section className="card feedback" data-testid="feedback">
               {showsWhatWasWritten ? (
                  <div className="you-wrote" data-testid="you-wrote">
                     <p className="eyebrow">{YOU_WROTE_LABEL}</p>

                     <p>
                        {chosenOption !== null ? (
                           chosenOption.label !== undefined ? (
                              <MathText text={chosenOption.label} />
                           ) : (
                              <MathValue value={chosenOption.mathjson ?? chosenOption.value ?? chosenOption.id} />
                           )
                        ) : (
                           <MathValue value={answerMathJson} />
                        )}
                     </p>
                  </div>
               ) : null}
               {hasFigure ? (
                  <div data-testid="feedback-figure">
                     <FigureView spec={item.figure_spec} />
                  </div>
               ) : null}

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

               <div className="submit-row submit-row-end">
                  <button
                     type="button"
                     className="motion-instant-question-move button-primary"
                     disabled={owesNote}
                     onClick={moveOn}
                  >
                     {NEXT_LABEL}
                  </button>
               </div>
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