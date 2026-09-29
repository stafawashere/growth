import { useEffect, useRef, useState } from "react";

import { bookletAddress, type SaveQuestionFields } from "../api/client";
import type {
   AssessmentAnswer,
   AssessmentFrqItem,
   AssessmentItem,
   AssessmentPart,
   AssessmentQuestion,
   AssessmentTool,
   HighlightRange
} from "../api/types";
import { FigureView } from "../figures/FigureView";
import { MathAnswerField } from "../input/MathAnswerField";
import { McqControl } from "../input/McqControl";
import { mathJsonToLatex } from "../math/mathjson";
import { MathText } from "../math/MathText";
import { clockText, FIVE_MINUTE_ANNOUNCEMENT, partHeading } from "./format";
import { GraphingPanel } from "./graphing/GraphingPanel";
import { DesmosPanel } from "../input/DesmosPanel";

const PART_OPTION_KEYS = ["a", "b", "c", "d", "e"];

export const PART_KEY_HINT = "A, B, C and D choose. N goes to the next question and P to the previous one.";

/* One open timed part, laid out as 08's two mock wireframes. Questions carry their exam number,
   which runs on across a section's parts, and are counted against the section's total, so the
   first question of Section I Part B reads "Question 30 of 42". Every tool is drawn only when the
   part's tools list names it, so the graphing panel is absent from a no-calculator part rather than
   hidden. The server holds the clock, so the countdown starts from its time_remaining_ms and restarts
   from each new reply, and at zero the container re-reads the session, where the part has closed. */

export interface PartRunnerProps {
   part: AssessmentPart;
   radianNote: string;
   sectionCount: number | null;
   onSave: (number: number, fields: SaveQuestionFields) => void;
   onSubmit: () => void;
   onTimeUp: () => void;
}

interface QuestionWork {
   answer: AssessmentAnswer | null;
   marked: boolean;
   eliminated: string[];
   notes: string;
   highlights: HighlightRange[];
}

const ZOOM_STEPS = [100, 125, 150];

const HIGHLIGHT_NAME = "assessment-highlight";

const SHORT_ANSWER_SAVE_DELAY_MS = 1000;

const TICK_MS = 1000;

interface HighlightRegistry {
   set(name: string, highlight: unknown): void;
   delete(name: string): void;
}

type HighlightConstructor = new (...ranges: Range[]) => unknown;

function workOf(question: AssessmentQuestion): QuestionWork {
   return {
      answer: question.answer,
      marked: question.marked,
      eliminated: question.eliminated,
      notes: question.notes ?? "",
      highlights: question.highlights
   };
}

function isFreeResponse(question: AssessmentQuestion) {
   return question.kind === "frq";
}

function showsOptions(question: AssessmentQuestion) {
   const item = question.item as AssessmentItem;
   const isChoice = question.kind === "mcq" || item.requires_choice === true;
   const hasOptions = Array.isArray(item.options) && item.options.length > 0;

   return isChoice && hasOptions;
}

function isAnswered(work: QuestionWork) {
   return work.answer !== null;
}

function textRangeOf(container: HTMLElement, start: number, end: number): Range | null {
   const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
   const range = document.createRange();
   let offset = 0;
   let hasStart = false;
   let node = walker.nextNode();

   while (node !== null) {
      const nodeEnd = offset + (node.textContent?.length ?? 0);
      const startsHere = !hasStart && start <= nodeEnd;

      if (startsHere) {
         range.setStart(node, start - offset);
         hasStart = true;
      }

      const endsHere = hasStart && end <= nodeEnd;

      if (endsHere) {
         range.setEnd(node, end - offset);

         return range;
      }

      offset = nodeEnd;
      node = walker.nextNode();
   }

   return null;
}

/* The selection's offsets in the stem's plain text, the text content the stem renders. */
export function selectionOffsets(container: HTMLElement, selection: Selection | null): HighlightRange | null {
   const hasSelection = selection !== null && selection.rangeCount > 0 && !selection.isCollapsed;

   if (!hasSelection) {
      return null;
   }

   const range = selection.getRangeAt(0);
   const isInside = container.contains(range.startContainer) && container.contains(range.endContainer);

   if (!isInside) {
      return null;
   }

   const before = document.createRange();

   before.selectNodeContents(container);
   before.setEnd(range.startContainer, range.startOffset);

   const start = before.toString().length;
   const end = start + range.toString().length;

   return end > start ? { start, end } : null;
}

function PartTimer(props: { part: AssessmentPart; onTimeUp: () => void }) {
   const { part, onTimeUp } = props;
   const [anchor, setAnchor] = useState({ remaining: part.time_remaining_ms ?? 0, at: Date.now() });
   const [now, setNow] = useState(Date.now());
   const [isHidden, setIsHidden] = useState(false);
   const [announcements, setAnnouncements] = useState<string[]>([]);
   const hasAlerted = useRef(false);
   const hasReportedZero = useRef(false);
   const timeUp = useRef(onTimeUp);
   const alertMs = part.five_minute_alert_seconds * 1000;

   useEffect(() => {
      timeUp.current = onTimeUp;
   }, [onTimeUp]);

   useEffect(() => {
      const received = Date.now();

      setAnchor({ remaining: part.time_remaining_ms ?? 0, at: received });
      setNow(received);
   }, [part]);

   useEffect(() => {
      const ticker = setInterval(() => setNow(Date.now()), TICK_MS);

      return () => clearInterval(ticker);
   }, []);

   const remaining = Math.max(0, anchor.remaining - (now - anchor.at));
   const isInFinalMinutes = remaining <= alertMs;
   const hasRunOut = remaining <= 0;

   useEffect(() => {
      const shouldAlert = isInFinalMinutes && !hasAlerted.current;

      if (shouldAlert) {
         hasAlerted.current = true;
         setIsHidden(false);
         setAnnouncements((current) => [...current, FIVE_MINUTE_ANNOUNCEMENT]);
      }
   }, [isInFinalMinutes]);

   useEffect(() => {
      const shouldReport = hasRunOut && !hasReportedZero.current;

      if (shouldReport) {
         hasReportedZero.current = true;
         timeUp.current();
      }
   }, [hasRunOut]);

   return (
      <div className="part-timer">
         {isHidden ? null : (
            <p className="part-clock" data-testid="part-timer">
               {clockText(remaining)}
            </p>
         )}

         <button type="button" className="text-button" onClick={() => setIsHidden(!isHidden)}>
            {isHidden ? "Show timer" : "Hide timer"}
         </button>

         <div aria-live="polite" className="visually-hidden" data-testid="timer-announcements">
            {announcements.map((announcement, index) => (
               <p key={index}>{announcement}</p>
            ))}
         </div>
      </div>
   );
}

export const QUESTION_MENU_KEY = "Filled means answered, a heavy border is the question on screen, and * marks one for review.";

/* Each tile shows the question's number and reads without colour: an answered tile is filled with a
   solid border, an unanswered one keeps a dashed border, the one on screen has a heavier border, and
   * follows a number marked for review. The full sentence is the tile's accessible name. */
function QuestionMenuList(props: {
   questions: AssessmentQuestion[];
   work: Record<number, QuestionWork>;
   currentIndex: number;
   onJump: (index: number) => void;
}) {
   return (
      <div className="question-menu-block">
         <ul className="question-menu" aria-label="Questions in this part" data-testid="question-menu">
            {props.questions.map((question, index) => {
               const work = props.work[question.number];
               const choiceState = isAnswered(work) ? "answered" : "unanswered";
               const answeredState = isFreeResponse(question) ? "written in the booklet" : choiceState;
               const markedState = work.marked ? ", marked for review" : "";
               const isCurrent = index === props.currentIndex;

               return (
                  <li key={question.number} data-answered={isAnswered(work)}>
                     <button
                        type="button"
                        className="question-tile motion-instant-question-move"
                        aria-current={isCurrent ? "true" : undefined}
                        aria-label={`Question ${question.number}, ${answeredState}${markedState}`}
                        data-testid="question-menu-entry"
                        onClick={() => props.onJump(index)}
                     >
                        {question.number}
                        {work.marked ? "*" : ""}
                     </button>
                  </li>
               );
            })}
         </ul>

         <p className="muted question-menu-key" aria-hidden="true">
            {QUESTION_MENU_KEY}
         </p>
      </div>
   );
}

function useStemHighlights(stemElement: HTMLElement | null, highlights: HighlightRange[]) {
   useEffect(() => {
      const registry = (globalThis as { CSS?: { highlights?: HighlightRegistry } }).CSS?.highlights;
      const Highlight = (globalThis as { Highlight?: HighlightConstructor }).Highlight;
      const canPaint = registry !== undefined && Highlight !== undefined && stemElement !== null;

      if (!canPaint) {
         return undefined;
      }

      const ranges = highlights
         .map((highlight) => textRangeOf(stemElement, highlight.start, highlight.end))
         .filter((range): range is Range => range !== null);

      registry.set(HIGHLIGHT_NAME, new Highlight(...ranges));

      return () => registry.delete(HIGHLIGHT_NAME);
   }, [stemElement, highlights]);
}

function FreeResponseBody(props: { question: AssessmentQuestion }) {
   const item = props.question.item as AssessmentFrqItem;
   const attemptId = props.question.attempt_id;

   return (
      <>
         <ul className="frq-parts">
            {item.parts.map((entry) => (
               <li key={entry.id}>
                  ({entry.id}) <MathText text={entry.prompt} />
                  {entry.setup_required ? <span className="muted"> Show the setup for your calculations.</span> : null}
               </li>
            ))}
         </ul>

         <p data-testid="booklet-direction">Write your answer in the booklet, Question {props.question.number}.</p>

         {attemptId !== null ? (
            <a href={bookletAddress(attemptId)} target="_blank" rel="noreferrer">
               Print booklet page
            </a>
         ) : null}
      </>
   );
}

export function PartRunner({ part, radianNote, sectionCount, onSave, onSubmit, onTimeUp }: PartRunnerProps) {
   const questions = part.questions;
   const [index, setIndex] = useState(0);
   const [work, setWork] = useState<Record<number, QuestionWork>>(() =>
      Object.fromEntries(questions.map((question) => [question.number, workOf(question)]))
   );
   const [zoom, setZoom] = useState(ZOOM_STEPS[0]);
   const [isConfirmingSubmit, setIsConfirmingSubmit] = useState(false);
   const [isMenuOpen, setIsMenuOpen] = useState(false);
   const [isGraphingOpen, setIsGraphingOpen] = useState(false);
   const shortcut = useRef<(event: KeyboardEvent) => void>(() => undefined);
   const [highlightProblem, setHighlightProblem] = useState<string | null>(null);
   const [stemElement, setStemElement] = useState<HTMLElement | null>(null);
   const [answerUnavailable, setAnswerUnavailable] = useState(false);
   const visitStartedAt = useRef(Date.now());
   const pendingShortAnswer = useRef<{ number: number; timer: ReturnType<typeof setTimeout> } | null>(null);

   const tools = new Set<AssessmentTool>(part.tools);
   const question = questions[index];
   const current = question === undefined ? null : work[question.number];

   useStemHighlights(stemElement, current?.highlights ?? []);

   useEffect(() => {
      const listener = (event: KeyboardEvent) => shortcut.current(event);

      document.addEventListener("keydown", listener);

      return () => {
         document.removeEventListener("keydown", listener);
      };
   }, []);

   shortcut.current = () => undefined;

   if (question === undefined || current === null) {
      return (
         <section className="card" data-testid="part-runner">
            <p className="muted">This part holds no questions.</p>
         </section>
      );
   }

   const item = question.item;
   const isLast = index === questions.length - 1;
   const isFirst = index === 0;
   const freeResponse = isFreeResponse(question);
   const offersOptions = !freeResponse && showsOptions(question);
   const offersEliminator = offersOptions && tools.has("option_eliminator");
   const hasFigure = !freeResponse && (item as AssessmentItem).figure_spec !== null && (item as AssessmentItem).figure_spec !== undefined;

   function update(number: number, changed: Partial<QuestionWork>) {
      setWork((all) => ({ ...all, [number]: { ...all[number], ...changed } }));
   }

   function flushShortAnswer() {
      const pending = pendingShortAnswer.current;

      if (pending === null) {
         return;
      }

      clearTimeout(pending.timer);
      pendingShortAnswer.current = null;
      onSave(pending.number, { answer: work[pending.number]?.answer ?? null });
   }

   function leaveQuestion() {
      flushShortAnswer();

      const visitMs = Math.max(0, Math.round(Date.now() - visitStartedAt.current));

      onSave(question.number, { visit_ms: visitMs });
      visitStartedAt.current = Date.now();
   }

   function goTo(target: number) {
      const isSame = target === index;

      if (isSame) {
         return;
      }

      leaveQuestion();
      setIndex(target);
      setHighlightProblem(null);
   }

   function chooseOption(optionId: string) {
      const answer = { option_id: optionId };

      update(question.number, { answer });
      onSave(question.number, { answer });
   }

   /* A to D choose, N and P move. A key typed into the notes or the math field is the student's
      text, and a key on a focused button is that button's own activation, so neither is read. */
   shortcut.current = onShortcut;

   function onShortcut(event: KeyboardEvent) {
      const target = event.target as HTMLElement;
      const hasModifier = event.altKey || event.ctrlKey || event.metaKey;
      const isTyping = target.matches("textarea, select, math-field, input:not([type='radio']):not([type='checkbox'])");
      const isActivating = target.matches("button, a[href], summary");
      const isIgnored = hasModifier || event.defaultPrevented || isTyping || isActivating;

      if (isIgnored) {
         return;
      }

      const key = event.key.toLowerCase();
      const options = offersOptions ? (item as AssessmentItem).options ?? [] : [];
      const optionIndex = PART_OPTION_KEYS.indexOf(key);
      const picksOption = optionIndex >= 0 && optionIndex < options.length;
      const movesOn = key === "n" && !isLast;
      const movesBack = key === "p" && !isFirst;

      if (picksOption) {
         event.preventDefault();
         chooseOption(options[optionIndex].id);
      }

      if (movesOn) {
         event.preventDefault();
         goTo(index + 1);
      }

      if (movesBack) {
         event.preventDefault();
         goTo(index - 1);
      }
   }

   function typeShortAnswer(mathjson: unknown) {
      const number = question.number;
      const answer = { mathjson };

      update(number, { answer });

      if (pendingShortAnswer.current !== null) {
         clearTimeout(pendingShortAnswer.current.timer);
      }

      const timer = setTimeout(() => {
         pendingShortAnswer.current = null;
         onSave(number, { answer });
      }, SHORT_ANSWER_SAVE_DELAY_MS);

      pendingShortAnswer.current = { number, timer };
   }

   function toggleEliminated(optionId: string) {
      const isEliminated = current!.eliminated.includes(optionId);
      const eliminated = isEliminated
         ? current!.eliminated.filter((entry) => entry !== optionId)
         : [...current!.eliminated, optionId];

      update(question.number, { eliminated });
      onSave(question.number, { eliminated });
   }

   function toggleMarked(marked: boolean) {
      update(question.number, { marked });
      onSave(question.number, { marked });
   }

   function saveNotes() {
      const saved = question.notes ?? "";
      const hasChanged = current!.notes !== saved;

      if (hasChanged) {
         onSave(question.number, { notes: current!.notes });
      }
   }

   function highlightSelection() {
      const offsets = stemElement === null ? null : selectionOffsets(stemElement, window.getSelection());

      if (offsets === null) {
         setHighlightProblem("Select words in the question first, then highlight them.");

         return;
      }

      const highlights = [...current!.highlights, offsets];

      setHighlightProblem(null);
      update(question.number, { highlights });
      onSave(question.number, { highlights });
   }

   function removeHighlight(position: number) {
      const highlights = current!.highlights.filter((_, entry) => entry !== position);

      update(question.number, { highlights });
      onSave(question.number, { highlights });
   }

   function submit() {
      leaveQuestion();
      setIsConfirmingSubmit(false);
      onSubmit();
   }

   function timeUp() {
      leaveQuestion();
      onTimeUp();
   }

   const stemText = stemElement?.textContent ?? "";
   const shortAnswerLatex = current.answer?.mathjson === undefined ? undefined : mathJsonToLatex(current.answer.mathjson);

   const offersMarkForReview = tools.has("mark_for_review");
   const offersQuestionMenu = tools.has("question_menu");
   const offersZoom = tools.has("zoom");
   const offersToolbar = offersMarkForReview || offersQuestionMenu || offersZoom;
   const offersGraphing = tools.has("graphing_panel");
   const showsGraphingBeside = offersGraphing && isGraphingOpen;

   return (
      <section className="card part-runner" data-testid="part-runner" data-graphing-open={showsGraphingBeside ? "true" : undefined}>
         <header className="part-header">
            <p className="label-heading">{partHeading(part)}</p>

            <p data-testid="question-position">
               Question {question.number}
               {sectionCount !== null ? ` of ${sectionCount}` : null}
            </p>

            {tools.has("timer") ? <PartTimer part={part} onTimeUp={timeUp} /> : null}
         </header>

         <p className="calculator-label" data-testid="calculator-label">
            {part.calculator_label}
         </p>

         {part.calculator_note !== null ? <p data-testid="calculator-note">{part.calculator_note}</p> : null}

         {offersToolbar ? (
            <div className="exam-toolbar">
               {tools.has("mark_for_review") ? (
                  <label className="mark-for-review">
                     <input
                        type="checkbox"
                        className="motion-instant-mark-for-review"
                        checked={current.marked}
                        onChange={(event) => toggleMarked(event.target.checked)}
                     />{" "}
                     Mark for review
                  </label>
               ) : null}

               {tools.has("question_menu") ? (
                  <button type="button" className="text-button" aria-expanded={isMenuOpen} onClick={() => setIsMenuOpen(!isMenuOpen)}>
                     Question menu
                  </button>
               ) : null}

               {tools.has("zoom") ? (
                  <div role="group" aria-label="Zoom" className="choice-row" data-testid="zoom">
                     {ZOOM_STEPS.map((step) => (
                        <button key={step} type="button" className="text-button" aria-pressed={zoom === step} onClick={() => setZoom(step)}>
                           {step} percent
                        </button>
                     ))}
                  </div>
               ) : null}
            </div>
         ) : null}

         {tools.has("question_menu") && isMenuOpen ? (
            <QuestionMenuList
               questions={questions}
               work={work}
               currentIndex={index}
               onJump={(target) => {
                  setIsMenuOpen(false);
                  goTo(target);
               }}
            />
         ) : null}

         {offersGraphing ? <DesmosPanel /> : null}

         <div className="question-layout">
            {offersGraphing ? <GraphingPanel onOpenChange={setIsGraphingOpen} /> : null}

            <div className="question-column">
               <div className="question-area" data-testid="question-area" data-zoom={zoom} style={{ fontSize: `${zoom}%` }}>
                  {item.radian_note ? <p data-testid="radian-note">{radianNote}</p> : null}

                  <p className="item-stem" data-testid="question-stem" ref={setStemElement}>
                     <MathText text={item.stem} />
                  </p>

                  {hasFigure ? <FigureView spec={(item as AssessmentItem).figure_spec} /> : null}

                  {freeResponse ? <FreeResponseBody question={question} /> : null}

                  {offersOptions ? (
                     <McqControl
                        key={question.number}
                        groupLabel={`Question ${question.number}`}
                        options={(item as AssessmentItem).options ?? []}
                        selectedId={current.answer?.option_id ?? null}
                        onSelect={chooseOption}
                        eliminatedIds={current.eliminated}
                        onToggleEliminated={offersEliminator ? toggleEliminated : undefined}
                     />
                  ) : null}

                  {!freeResponse && !offersOptions ? (
                     <div data-testid="math-answer">
                        <MathAnswerField
                           key={question.number}
                           label="My answer"
                           initialLatex={shortAnswerLatex}
                           onChange={typeShortAnswer}
                           onLoadFailure={() => setAnswerUnavailable(true)}
                        />

                        {answerUnavailable ? <p role="alert">The math keyboard did not load, so this question cannot take an answer.</p> : null}
                     </div>
                  ) : null}
               </div>

               {tools.has("highlight_and_notes") ? (
                  <div className="question-tools" data-testid="highlight-and-notes">
                     <button type="button" className="text-button" onClick={highlightSelection}>
                        Highlight selection
                     </button>

                     {highlightProblem !== null ? <p role="alert">{highlightProblem}</p> : null}

                     {current.highlights.length > 0 ? (
                        <ul className="review-list" aria-label="Highlights">
                           {current.highlights.map((highlight, position) => (
                              <li key={`${highlight.start}-${highlight.end}-${position}`}>
                                 <mark className="stem-highlight">{stemText.slice(highlight.start, highlight.end)}</mark>

                                 <button type="button" className="text-button" onClick={() => removeHighlight(position)}>
                                    Remove highlight
                                 </button>
                              </li>
                           ))}
                        </ul>
                     ) : null}

                     <label className="form-field">
                        <span>Notes on this question</span>
                        <textarea
                           value={current.notes}
                           onChange={(event) => update(question.number, { notes: event.target.value })}
                           onBlur={saveNotes}
                        />
                     </label>
                  </div>
               ) : null}
            </div>
         </div>

         <div className="exam-bottom">
            <div className="choice-row">
               <button type="button" className="text-button motion-instant-question-move" disabled={isFirst} onClick={() => goTo(index - 1)}>
                  Back
               </button>

               <button type="button" className="text-button motion-instant-question-move" disabled={isLast} onClick={() => goTo(index + 1)}>
                  Next
               </button>
            </div>

            <p className="caption key-hint">{PART_KEY_HINT}</p>

            <button type="button" className="text-button" onClick={() => setIsConfirmingSubmit(true)}>
               Submit part
            </button>
         </div>

         {isConfirmingSubmit ? (
            <div role="alertdialog" aria-label="Submit this part" className="notice" data-testid="submit-confirmation">
               <p>Submitting closes {part.label}. It cannot be reopened, and you cannot return to its questions.</p>

               <div className="choice-row">
                  <button type="button" className="button-primary motion-instant-submit-answer" onClick={submit}>
                     Submit and close this part
                  </button>

                  <button type="button" className="text-button" onClick={() => setIsConfirmingSubmit(false)}>
                     Keep working
                  </button>
               </div>
            </div>
         ) : null}
      </section>
   );
}
