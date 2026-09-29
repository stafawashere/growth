import { useCallback, useEffect, useRef, useState } from "react";
import {
   answerLessonCheck,
   answerLessonPrompt,
   closeSession,
   openSession,
   postSessionLessonEvent,
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
   LessonCheckAnswerBody,
   LessonEventBody,
   LessonEventMode,
   LessonPromptAnswerBody,
   MarkedQueueSlot,
   ServedItem,
   ServedLesson,
   SessionLessonSlot,
   SessionPayload
} from "../api/types";
import { isServedLesson } from "../api/types";
import { LessonReader } from "../lessons/LessonReader";
import { FigureView } from "../figures/FigureView";
import { MathText } from "../math/MathText";
import { MathValue } from "../math/MathValue";
import { ActionFailed, LoadFailed, Loading } from "../status/LoadState";
import { isEmptyMathJson, UNREAD_FIELD } from "../input/MathField";
import type { MathFieldReader } from "../input/MathField";
import { COMPARISON_LABEL, ComparisonPanel, METHOD_LABEL } from "./ComparisonPanel";
import { CONFIDENCE_CHOICES } from "./ConfidencePrompt";
import { CorrectResult, ElaboratedPanel } from "./ElaboratedPanel";
import { ErrorNoteField } from "./ErrorNoteField";
import { collectsConfidence, Item, servesChoice } from "./Item";
import { SelfExplanationPrompt } from "./SelfExplanationPrompt";
import { StepMarks } from "./StepMarks";
import { Icon } from "../ui/Icon";
import { Page, PageHeader } from "../ui/Page";

export const SET_FINISHED = "That is today's set finished.";

export const SET_STOPPED = "You stopped here for today.";

export const STOP_LABEL = "I want to stop here";

export const STOP_CONFIRM_LABEL = "Stop and close this set";

export const KEEP_GOING_LABEL = "Keep going";

export const YOU_WROTE_LABEL = "You wrote";

export const OPENER_WITHOUT_TUTOR =
   "Setting your attempt beside the method needs the tutor, which is not available, so the comparison is not shown here.";

const OPTION_KEYS = ["a", "b", "c", "d", "e"];

interface Remaining {
   items: number;
   minutes: number;
}

function isLessonSlot(slot: MarkedQueueSlot | SessionLessonSlot): slot is SessionLessonSlot {
   return slot.kind === "lesson" || slot.kind === "refresher";
}

/* GET /sessions/{id} lists the queue slots not yet answered, the current one included, and
   queue.forecasts holds the minute forecast per archetype, so the two give what is left. A lesson
   slot is not an item: its minutes count and it does not (15, Session assembly forecast). */
export function remainingFrom(payload: SessionPayload): Remaining {
   let minutes = 0;
   let items = 0;

   for (const slot of payload.remaining) {
      if (isLessonSlot(slot)) {
         minutes += slot.minutes;
      } else {
         minutes += payload.queue.forecasts[slot.archetype_id] ?? 0;
         items += 1;
      }
   }

   return { items, minutes: Math.ceil(minutes) };
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

/* The verdict line at the top of feedback: a glyph and a word as well as the colour, so the
   greyscale render says the same thing. An opener carries no verdict, only the comparison. */
function FeedbackHead(props: { correct: boolean | null; isOpener: boolean }) {
   const hasVerdict = props.correct !== null && !props.isOpener;

   if (!hasVerdict) {
      return (
         <div className="feedback-head">
            <span className="eyebrow">Feedback</span>
         </div>
      );
   }

   return (
      <div className="feedback-head" data-testid="feedback-verdict">
         <span className={props.correct ? "status-icon text-correct" : "status-icon text-incorrect"}>
            <Icon name={props.correct ? "check" : "alert"} size="md" />
         </span>

         <h2>{props.correct ? "That holds." : "Not yet. Here is where it turned."}</h2>
      </div>
   );
}

/* Every session lesson event carries the slot's band and reason: the route tells a refresher
   (T1 to T5) from a first-contact lesson by the reason, and the forecast reads the band. */
function lessonEventBody(lesson: ServedLesson, fields: Omit<LessonEventBody, "band" | "reason">): LessonEventBody {
   return { ...fields, band: lesson.band, reason: lesson.reason };
}

/* resumeSessionId names the open session GET /progress reported, and null opens a new one. It
   has no default, because opening a session writes a row and resuming one must not. */

export interface SessionScreenProps {
   resumeSessionId: string | null;
   onLeave?: () => void;
   onOpened?: (sessionId: string) => void;
}

const STAGE_TITLE: Record<ServedItem["stage"], string> = {
   example: "Worked example",
   completion: "Finish the solution",
   unsupported: "On your own"
};

export const OPENER_TITLE = "Before the method";

function stageTitle(item: ServedItem) {
   return item.is_opener === true ? OPENER_TITLE : STAGE_TITLE[item.stage];
}

/* The set's progress as steps: the items already worked, the current one, and those still to come.
   It is drawn only once GET /sessions/{id} has said what remains. */
function SetProgress(props: { worked: number; remaining: Remaining }) {
   const total = props.worked + props.remaining.items;
   const hasSteps = total > 0;

   if (!hasSteps) {
      return null;
   }

   const current = Math.min(props.worked, total - 1);
   const steps = Array.from({ length: total }, (_, index) => {
      if (index < current) {
         return "done";
      }

      return index === current ? "current" : "ahead";
   });

   return (
      <div
         className="progress-steps"
         role="progressbar"
         aria-label="Items in this set"
         aria-valuemin={1}
         aria-valuemax={total}
         aria-valuenow={current + 1}
         data-testid="set-progress"
      >
         {steps.map((state, index) => (
            <span key={index} className="progress-step" data-state={state} />
         ))}
      </div>
   );
}

export function SessionScreen({ resumeSessionId, onLeave, onOpened }: SessionScreenProps) {
   const [session, setSession] = useState<SessionPayload | null>(null);
   const [item, setItem] = useState<ServedItem | null>(null);
   const [lesson, setLesson] = useState<ServedLesson | null>(null);
   const lessonOpenedAt = useRef(0);
   const [committed, setCommitted] = useState<AttemptResult | null>(null);
   const [feedback, setFeedback] = useState<FeedbackPayload | null>(null);
   const [feedbackUnreadable, setFeedbackUnreadable] = useState(false);
   const [confidence, setConfidence] = useState<Confidence | null>(null);
   const [answerMathJson, setAnswerMathJson] = useState<unknown>(null);
   const [mathFieldReady, setMathFieldReady] = useState(false);
   const mathReader = useRef<MathFieldReader | null>(null);
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
         setLesson(null);
         setFinished(true);

         return;
      }

      /* 15 UI: a lesson or refresher slot is the session's lesson state, switched on entry.kind;
         it is opened here so the server records served with its band. */
      if (isServedLesson(next.item)) {
         const served = next.item;

         setItem(null);
         setLesson(served);
         lessonOpenedAt.current = Date.now();
         postSessionLessonEvent(sessionId, served.lesson_id, lessonEventBody(served, { event: "opened", elapsed_ms: 0 })).catch(
            () => undefined
         );

         return;
      }

      setLesson(null);
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

            if (!isResuming) {
               onOpened?.(payload.id);
            }

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

   const noteMathFieldReady = useCallback(() => {
      setMathFieldReady(true);
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

      const isMcq = servesChoice(item);
      const readNow = mathReader.current === null ? UNREAD_FIELD : mathReader.current();
      const wasRead = readNow !== UNREAD_FIELD;
      const typed = wasRead ? readNow : answerMathJson;
      const fieldIsEmpty = isEmptyMathJson(typed);
      const knowsTheFieldIsEmpty = fieldIsEmpty && (wasRead || mathFieldReady);
      const refusesEmptyAnswer = !isMcq && knowsTheFieldIsEmpty;

      if (refusesEmptyAnswer) {
         return;
      }

      inFlight.current = true;
      setActionFailed(false);

      try {
         const answer: AttemptAnswer = isMcq ? { option_id: selectedOptionId ?? "" } : { mathjson: typed };
         const ratesConfidence = collectsConfidence(item.stage) && confidence !== null;

         const result = await submitAttempt(session.id, {
            item_id: item.id,
            answer,
            confidence: ratesConfidence ? confidence : undefined
         });

         /* An opener miss is not corrected: it is neither requeued nor noted (02, Session
            assembly), so it does not come back in Review. */
         const isCorrection = result.correct === false && item.is_opener !== true;

         if (!isMcq) {
            setAnswerMathJson(typed);
         }

         setCommitted(result);
         setWorked((sofar) => ({
            items: sofar.items + 1,
            corrected: sofar.corrected + (isCorrection ? 1 : 0)
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
   }, [session, item, selectedOptionId, answerMathJson, mathFieldReady, confidence, showFeedback]);

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
      const wasOpener = item !== null && item.is_opener === true;
      const wasCorrected = committed.correct === false && !wasOpener;
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
   }, [session, item, committed, feedback, errorNote, selfExplanation, advance]);

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

   const leaveLesson = useCallback(
      async (event: "completed" | "skipped", sectionIndex?: number) => {
         const isIdle = !inFlight.current;
         const canLeave = session !== null && lesson !== null && isIdle;

         if (!canLeave) {
            return;
         }

         inFlight.current = true;
         setActionFailed(false);

         const skippedAt = sectionIndex === undefined ? undefined : lesson.plan.sections[sectionIndex]?.id;
         const elapsed = Math.max(0, Date.now() - lessonOpenedAt.current);

         try {
            await postSessionLessonEvent(
               session.id,
               lesson.lesson_id,
               lessonEventBody(lesson, skippedAt === undefined ? { event, elapsed_ms: elapsed } : { event, elapsed_ms: elapsed, section_id: skippedAt })
            );
            await advance(session.id);
         } catch {
            setActionFailed(true);
         } finally {
            inFlight.current = false;
         }
      },
      [session, lesson, advance]
   );

   shortcut.current = () => undefined;

   if (finished) {
      return (
         <section data-testid="session-end">
            <Page header={<PageHeader eyebrow={stopped ? "Set stopped" : "Session complete"} title={stopped ? SET_STOPPED : SET_FINISHED} />}>
               <div className="card stack">
                  {worked.items > 0 ? <p>{workedSentence(worked.items)}</p> : null}

                  {worked.corrected > 0 ? <p>{correctedSentence(worked.corrected)}</p> : null}

                  <p className="muted">Today shows what is due next, in minutes, whenever you open it.</p>
               </div>

               {onLeave !== undefined ? (
                  <div className="cluster">
                     <button type="button" className="button-secondary" onClick={onLeave}>
                        <Icon name="back" />
                        Back to Today
                     </button>
                  </div>
               ) : null}
            </Page>
         </section>
      );
   }

   if (loadFailed) {
      return <LoadFailed testId="session-failed" onRetry={retryLoading} />;
   }

   if (lesson !== null && session !== null) {
      const shown = lesson;
      const sessionId = session.id;

      function sectionViewed(sectionId: string, mode: LessonEventMode, elapsedMs: number) {
         postSessionLessonEvent(sessionId, shown.lesson_id, lessonEventBody(shown, { event: "section_viewed", section_id: sectionId, mode, elapsed_ms: elapsedMs })).catch(
            () => undefined
         );
      }

      function checkAnswer(checkId: string, body: LessonCheckAnswerBody) {
         return answerLessonCheck(shown.lesson_id, checkId, body);
      }

      function promptAnswer(sectionId: string, body: LessonPromptAnswerBody) {
         return answerLessonPrompt(shown.lesson_id, sectionId, body);
      }

      return (
         <div data-testid="session-lesson" data-lesson-kind={shown.kind} className="stack stack-loose">
            <div className="session-meta">
               <span className="eyebrow">{shown.kind === "refresher" ? "A short refresher" : "A lesson first"}</span>

               {remaining !== null ? (
                  <span className="helper" data-testid="session-remaining">
                     {remainingSentence(remaining)}
                  </span>
               ) : null}
            </div>

            {actionFailed ? <ActionFailed /> : null}

            {shown.lesson === null ? (
               <LoadFailed testId="session-lesson-failed" onRetry={() => leaveLesson("skipped", 0)} />
            ) : (
               <LessonReader
                  key={`${shown.lesson_id}-${shown.before_item_id}`}
                  lesson={shown.lesson}
                  plan={shown.plan}
                  band={shown.band}
                  context="session"
                  conceptName={shown.concept_name ?? undefined}
                  onComplete={() => leaveLesson("completed")}
                  onSkip={(sectionIndex) => leaveLesson("skipped", sectionIndex)}
                  onSectionViewed={sectionViewed}
                  onCheckAnswer={checkAnswer}
                  onPromptAnswer={promptAnswer}
               />
            )}
         </div>
      );
   }

   if (item === null) {
      return <Loading testId="session-waiting" />;
   }

   const showsFeedback = feedback !== null || feedbackUnreadable;
   const hasFigure = item.figure_spec !== null && item.figure_spec !== undefined;
   const comparison = feedback?.comparison ?? null;
   const showsComparison = comparison !== null;
   const marksSteps = feedback !== null && feedback.stage !== "unsupported";
   const showsElaborated = feedback !== null && feedback.stage === "unsupported" && !showsComparison;
   const reinforcement = feedback !== null && feedback.kind === "correct" ? feedback.sentence : null;
   const showsReinforcement = reinforcement !== null && reinforcement.trim().length > 0;
   const correctAnswer = feedback?.correct_answer ?? null;

   /* 11 P1 scope item 10: one note per corrected item, written before the retry is scheduled. An
      item the student got right is requeued by nothing and asks for nothing, and neither is an
      opener, whose feedback is the comparison alone. */
   const isOpener = item.is_opener === true;
   const wasCorrected = committed !== null && committed.correct === false && !isOpener;
   const showsStepResult = marksSteps && wasCorrected;
   const openerWithoutComparison = isOpener && feedback !== null && !showsComparison && !showsReinforcement;
   const openerFirstStep = feedback?.first_worked_step ?? null;
   const owesNote = wasCorrected && errorNote.trim().length === 0;
   const awaitsRating =
      committed !== null && collectsConfidence(committed.served_stage) && committed.confidence === null;

   const choiceServed = servesChoice(item);
   const awaitsMathValue = !choiceServed && mathFieldReady && !answerUnavailable && isEmptyMathJson(answerMathJson);
   const chosenOption = choiceServed ? (item.options ?? []).find((option) => option.id === selectedOptionId) ?? null : null;
   const wroteMath = !choiceServed && answerMathJson !== null;
   const showsWhatWasWritten = chosenOption !== null || wroteMath;

   const youWrote = showsWhatWasWritten ? (
      <div className="you-wrote" data-testid="you-wrote">
         <p className="eyebrow">{YOU_WROTE_LABEL}</p>

         <p className="note-quote">
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
   ) : null;

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

   const sessionAside = (
      <>
         {remaining !== null ? (
            <span data-testid="session-remaining">{remainingSentence(remaining)}</span>
         ) : null}

         {isConfirmingStop ? null : (
            <button type="button" className="text-button session-stop" onClick={() => setIsConfirmingStop(true)}>
               {STOP_LABEL}
            </button>
         )}
      </>
   );

   return (
      <Page header={<PageHeader eyebrow={<span data-testid="session-stage">Stage: {item.stage}</span>} title={stageTitle(item)} aside={sessionAside} />}>
         {remaining !== null ? <SetProgress worked={worked.items} remaining={remaining} /> : null}

         {isConfirmingStop ? (
            <div role="alertdialog" aria-label="Stop this set" className="callout callout-row" data-testid="stop-confirmation">
               <p>This closes today&apos;s set. What you answered is kept, and Today builds the next set from it.</p>

               <div className="cluster">
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
               <FeedbackHead correct={committed?.correct ?? null} isOpener={isOpener} />

               {comparison !== null ? <ComparisonPanel comparison={comparison} attempt={youWrote} /> : youWrote}

               {hasFigure ? (
                  <div data-testid="feedback-figure">
                     <FigureView spec={item.figure_spec} />
                  </div>
               ) : null}

               {marksSteps ? <StepMarks marks={feedback.step_marks} /> : null}

               {showsStepResult ? <CorrectResult answer={correctAnswer} /> : null}

               {openerWithoutComparison ? (
                  <section className="comparison" data-testid="opener-without-tutor">
                     <p className="eyebrow">{COMPARISON_LABEL}</p>

                     <p>{OPENER_WITHOUT_TUTOR}</p>

                     {openerFirstStep !== null ? (
                        <div data-testid="opener-first-step">
                           <p className="eyebrow">{METHOD_LABEL}</p>

                           <ol className="worked-steps">
                              <li data-step-index={openerFirstStep.index}>
                                 <MathText text={openerFirstStep.text} />
                              </li>
                           </ol>
                        </div>
                     ) : null}
                  </section>
               ) : null}

               {showsReinforcement ? (
                  <p className="tutor-note" data-testid="tutor-sentence">
                     {reinforcement}
                  </p>
               ) : null}

               {showsElaborated ? (
                  <ElaboratedPanel
                     elaborated={feedback.elaborated}
                     sentence={feedback.sentence}
                     lessonLink={feedback.lesson_link ?? null}
                     correctAnswer={isOpener ? null : correctAnswer}
                  />
               ) : null}

               <SelfExplanationPrompt
                  prompt={showsComparison ? null : feedback?.self_explanation_prompt ?? null}
                  value={selfExplanation}
                  onChange={setSelfExplanation}
               />

               {wasCorrected ? <ErrorNoteField value={errorNote} onChange={setErrorNote} /> : null}

               <div className="submit-row">
                  {owesNote ? <p className="helper">Write the note first, so the retry comes back with it.</p> : <span />}

                  <button
                     type="button"
                     className="motion-instant-question-move button-primary"
                     disabled={owesNote}
                     onClick={moveOn}
                  >
                     {NEXT_LABEL}
                     <Icon name="next" />
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
               mathReaderRef={mathReader}
               onMathFieldReady={noteMathFieldReady}
               commitDisabled={awaitsMathValue}
            />
         )}
      </Page>
   );
}