import { useRef, useState } from "react";

import type {
   LessonPromptAnswerBody,
   LessonPromptVerdict,
   LessonSection as LessonSectionRecord,
   ServedOption
} from "../api/types";
import { MathAnswerField } from "../input/MathAnswerField";
import { McqControl } from "../input/McqControl";
import { CORRECT_GLYPH, CORRECT_WORD, INCORRECT_GLYPH } from "../session/StepMarks";
import { ActionFailed } from "../status/LoadState";
import { ANSWER_UNAVAILABLE_TEXT, NOT_YET } from "./LessonCheck";

/* The prompts of the v2 reader, each posted to POST /lessons/{id}/prompts/{section_id}/answers:
   the prediction that opens a concept lesson, an error block's fix prompt and a faded example's
   answer. A prediction is committed rather than marked, so it shows no verdict; the other two
   read Correct. or Not yet. and then reveal what they held back.

   Each prompt is a part of the sheet its section sits on: the options as lettered lines, or the
   line to write on with its tag in the margin, then the sheet's foot with the one action. */

export type PromptAnswer = (sectionId: string, body: LessonPromptAnswerBody) => Promise<LessonPromptVerdict>;

export interface CommittedPrediction {
   sectionId: string;
   optionLabel: string | null;
   value: unknown;
   correct: boolean | null;
   resolution: string | null;
}

export const COMMITTED = "Committed.";

type Answer = { kind: "none" } | { kind: "math"; value: unknown } | { kind: "option"; id: string };

function elapsedSince(shownAt: number, now: () => number) {
   return Math.max(0, now() - shownAt);
}

export function PromptVerdictLine({ correct }: { correct: boolean }) {
   const glyph = correct ? CORRECT_GLYPH : INCORRECT_GLYPH;
   const word = correct ? `${CORRECT_WORD}.` : NOT_YET;
   const className = correct ? "verdict text-correct" : "verdict text-incorrect";

   return (
      <p className={className} data-testid="lesson-prompt-verdict" aria-live="polite">
         <span data-glyph aria-hidden="true">
            {glyph}
         </span>{" "}
         <span>{word}</span>
      </p>
   );
}

export interface PredictionProps {
   section: LessonSectionRecord;
   committed: CommittedPrediction | null;
   onCommit: (committed: CommittedPrediction) => void;
   onPromptAnswer?: PromptAnswer;
   now?: () => number;
}

/* The options go to McqControl without is_key, so the key never reaches the page. */
function predictionOptions(section: LessonSectionRecord): ServedOption[] {
   return (section.options ?? []).map((option) => ({ id: option.id, label: option.label, value: option.value }));
}

export function LessonPrediction({ section, committed, onCommit, onPromptAnswer, now = Date.now }: PredictionProps) {
   const [answer, setAnswer] = useState<Answer>({ kind: "none" });
   const [isWorking, setIsWorking] = useState(false);
   const [fieldFailed, setFieldFailed] = useState(false);
   const shownAt = useRef(now());
   const isCommitted = committed !== null;
   const isMcq = section.format !== "short_answer";

   function choose(next: Answer) {
      if (!isCommitted) {
         setAnswer(next);
      }
   }

   async function commit() {
      const optionId = answer.kind === "option" ? answer.id : null;
      const value = answer.kind === "math" ? answer.value : null;
      const option = section.options?.find((entry) => entry.id === optionId);
      const body: LessonPromptAnswerBody = { answer: value, option_id: optionId, elapsed_ms: elapsedSince(shownAt.current, now) };
      let verdict: LessonPromptVerdict | null = null;

      setIsWorking(true);

      /* A prediction that fails to post is still the student's commitment: the lesson goes on,
         and the resolution comes from the record instead of the server. */
      try {
         verdict = onPromptAnswer === undefined ? null : await onPromptAnswer(section.id, body);
      } catch {
         verdict = null;
      }

      setIsWorking(false);
      onCommit({
         sectionId: section.id,
         optionLabel: option?.label ?? null,
         value,
         correct: verdict?.correct ?? null,
         resolution: verdict?.resolution ?? section.resolution?.text ?? null
      });
   }

   return (
      <div className="lesson-prediction sheet-part" data-testid="lesson-prediction" data-committed={isCommitted ? "true" : undefined}>
         {isMcq ? (
            <div className="sheet-answer sheet-options">
               <McqControl
                  groupLabel="My prediction"
                  options={predictionOptions(section)}
                  selectedId={answer.kind === "option" ? answer.id : null}
                  onSelect={(id) => choose({ kind: "option", id })}
               />
            </div>
         ) : (
            <div className="sheet-row sheet-answer">
               <span className="sheet-margin sheet-tag" aria-hidden="true">
                  My prediction
               </span>

               <div className="sheet-body sheet-body-stack">
                  <MathAnswerField label="My prediction" onChange={(value) => choose({ kind: "math", value })} onLoadFailure={() => setFieldFailed(true)} />
                  {fieldFailed ? <p data-testid="answer-unavailable">{ANSWER_UNAVAILABLE_TEXT}</p> : null}
               </div>
            </div>
         )}

         {isCommitted ? (
            <p className="visually-hidden" aria-live="polite">{COMMITTED}</p>
         ) : (
            <div className="sheet-foot">
               <span />

               <button
                  type="button"
                  className="button-primary motion-instant-submit-answer"
                  data-testid="lesson-prediction-commit"
                  disabled={answer.kind === "none" || isWorking}
                  onClick={commit}
               >
                  Commit
               </button>
            </div>
         )}
      </div>
   );
}

export interface PromptFieldProps {
   label: string;
   testId: string;
   submitTestId?: string;
   sectionId: string;
   onPromptAnswer: PromptAnswer;
   onVerdict: (correct: boolean) => void;
   now?: () => number;
   secondary?: JSX.Element;
}

/* A math field and "Check my answer", graded by the prompts route. A post that fails says so and
   keeps the field, and the screen's own reveal is still there. */
export function PromptField({ label, testId, submitTestId, sectionId, onPromptAnswer, onVerdict, now = Date.now, secondary }: PromptFieldProps) {
   const [answer, setAnswer] = useState<Answer>({ kind: "none" });
   const [isWorking, setIsWorking] = useState(false);
   const [failed, setFailed] = useState(false);
   const [fieldFailed, setFieldFailed] = useState(false);
   const shownAt = useRef(now());

   async function check() {
      const value = answer.kind === "math" ? answer.value : null;
      const body: LessonPromptAnswerBody = { answer: value, option_id: null, elapsed_ms: elapsedSince(shownAt.current, now) };

      setIsWorking(true);
      setFailed(false);

      try {
         const verdict = await onPromptAnswer(sectionId, body);

         onVerdict(verdict.correct);
      } catch {
         setFailed(true);
      } finally {
         setIsWorking(false);
      }
   }

   return (
      <div className="lesson-prompt sheet-part" data-testid={testId}>
         <div className="sheet-row sheet-answer">
            <span className="sheet-margin sheet-tag" aria-hidden="true">
               {label}
            </span>

            <div className="sheet-body sheet-body-stack">
               <MathAnswerField label={label} onChange={(value) => setAnswer({ kind: "math", value })} onLoadFailure={() => setFieldFailed(true)} />
               {fieldFailed ? <p data-testid="answer-unavailable">{ANSWER_UNAVAILABLE_TEXT}</p> : null}
               {failed ? <ActionFailed /> : null}
            </div>
         </div>

         <div className="sheet-foot">
            <div className="sheet-foot-lead">{secondary}</div>

            <button
               type="button"
               className="button-secondary motion-instant-submit-answer"
               data-testid={submitTestId}
               disabled={answer.kind === "none" || isWorking}
               onClick={check}
            >
               Check my answer
            </button>
         </div>
      </div>
   );
}
