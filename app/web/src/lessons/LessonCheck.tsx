import { useRef, useState } from "react";

import type {
   LessonCheck as LessonCheckRecord,
   LessonCheckAnswerBody,
   LessonCheckVerdict,
   LessonSection as LessonSectionRecord,
   ServedOption
} from "../api/types";
import { MathAnswerField } from "../input/MathAnswerField";
import { McqControl } from "../input/McqControl";
import { MathValue } from "../math/MathValue";
import { latexToAccessibleText, mathJsonToLatex } from "../math/mathjson";
import { LessonText } from "./LessonText";
import { CORRECT_GLYPH, CORRECT_WORD, INCORRECT_GLYPH } from "../session/StepMarks";
import { ActionFailed } from "../status/LoadState";
import { LessonLink, sectionIdMatches } from "./LessonLink";

/* A lesson check (15 UI; CONTRACT.md Reader): the item input controls Item.tsx uses, MathLive for a
   short answer and McqControl for a choice, graded by the server. A wrong answer that matched an
   error block reads "Not yet." and three lines, the observed behaviour in the record's words, the
   right step and the consequence on the exam, then the link to that error's part and one "Try
   again"; a second wrong answer shows the worked solution and no further retry. There is no
   praise, no score and no percent, and a right answer reads Correct with its glyph and nothing
   more. A wrong answer with no error block to point at shows the worked solution at once. */

export const NOT_YET = "Not yet.";

export const RIGHT_STEP_PREFIX = "The right step: ";

export const CONSEQUENCE_PREFIX = "On the exam: ";

export const ANSWER_UNAVAILABLE_TEXT = "The math keyboard did not load, so this check cannot take an answer here.";

export interface LessonCheckProps {
   check: LessonCheckRecord;
   sections: LessonSectionRecord[];
   onCheckAnswer: (checkId: string, body: LessonCheckAnswerBody) => Promise<LessonCheckVerdict>;
   onOpenAnchor: (anchor: string) => void;
   now?: () => number;
}

function servedOptions(check: LessonCheckRecord): ServedOption[] {
   return (check.options ?? []).map((option) => ({ id: option.id, value: option.value, label: option.label, mathjson: option.mathjson }));
}

export function errorSectionFor(verdict: LessonCheckVerdict, sections: LessonSectionRecord[]) {
   const byAnchor = verdict.anchor === null ? undefined : sections.find((section) => sectionIdMatches(section.id, verdict.anchor!));
   const byError = verdict.error_id === null ? undefined : sections.find((section) => section.error_id === verdict.error_id);

   return byAnchor ?? byError ?? null;
}

function escapeForPattern(text: string) {
   return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/* The design texts mostly end with the value already ("Divided by 0.1: 5.2."), so the value is
   appended only when the text does not carry it. A match must not sit inside a longer number, so
   5 is not found in 0.5 or 5.2. */
export function textCarriesValue(text: string, value: unknown) {
   const plainForms = [latexToAccessibleText(mathJsonToLatex(value))];

   if (typeof value === "number" || typeof value === "string") {
      plainForms.push(String(value));
   }

   return plainForms.some((form) => {
      const hasForm = form.trim().length > 0;

      if (!hasForm) {
         return false;
      }

      const standaloneForm = new RegExp(`(?<![\\d.])${escapeForPattern(form.trim())}(?!\\d|\\.\\d)`);

      return standaloneForm.test(text);
   });
}

type Answer = { kind: "none" } | { kind: "math"; value: unknown } | { kind: "option"; id: string };

export function LessonCheck({ check, sections, onCheckAnswer, onOpenAnchor, now = Date.now }: LessonCheckProps) {
   const [answer, setAnswer] = useState<Answer>({ kind: "none" });
   const [verdict, setVerdict] = useState<LessonCheckVerdict | null>(null);
   const [isWorking, setIsWorking] = useState(false);
   const [failed, setFailed] = useState(false);
   const [fieldFailed, setFieldFailed] = useState(false);
   const [hasRetried, setHasRetried] = useState(false);
   const [fieldKey, setFieldKey] = useState(0);
   const shownAt = useRef(now());
   const isMcq = check.format === "mcq";

   async function submit() {
      const body: LessonCheckAnswerBody =
         answer.kind === "option"
            ? { option_id: answer.id, elapsed_ms: Math.max(0, now() - shownAt.current) }
            : { answer: answer.kind === "math" ? answer.value : null, elapsed_ms: Math.max(0, now() - shownAt.current) };

      setIsWorking(true);
      setFailed(false);

      try {
         setVerdict(await onCheckAnswer(check.id, body));
      } catch {
         setFailed(true);
      } finally {
         setIsWorking(false);
      }
   }

   function retry() {
      setVerdict(null);
      setAnswer({ kind: "none" });
      setHasRetried(true);
      setFieldKey((key) => key + 1);
      shownAt.current = now();
   }

   const errorSection = verdict === null || verdict.correct ? null : errorSectionFor(verdict, sections);
   const anchor = errorSection === null ? null : verdict?.anchor ?? errorSection.id;
   const isWrong = verdict !== null && !verdict.correct;
   const namesError = errorSection !== null && anchor !== null;
   const offersRetry = isWrong && namesError && !hasRetried;
   const showsSolution = isWrong && (!namesError || hasRetried);
   const rightStepText = verdict?.right_step ?? errorSection?.right_step?.text ?? null;
   const rightStepValue = errorSection?.right_step?.expression;
   const hasRightStepValue = rightStepValue !== undefined && rightStepValue !== null;
   const showsRightStepValue = hasRightStepValue && rightStepText !== null && !textCarriesValue(rightStepText, rightStepValue);
   const consequence = verdict?.scoring_consequence ?? errorSection?.scoring_consequence ?? null;

   return (
      <div className="lesson-check" data-testid="lesson-check">
         <p className="item-stem">
            <LessonText text={check.stem.text} />
         </p>

         {isMcq ? (
            <div data-testid="mcq-answer">
               <McqControl
                  groupLabel="My answer"
                  options={servedOptions(check)}
                  selectedId={answer.kind === "option" ? answer.id : null}
                  onSelect={(id) => setAnswer({ kind: "option", id })}
               />
            </div>
         ) : (
            <div data-testid="math-answer">
               <MathAnswerField key={fieldKey} label="My answer" onChange={(value) => setAnswer({ kind: "math", value })} onLoadFailure={() => setFieldFailed(true)} />
               {fieldFailed ? <p data-testid="answer-unavailable">{ANSWER_UNAVAILABLE_TEXT}</p> : null}
            </div>
         )}

         <div className="submit-row">
            <button
               type="button"
               className="button-primary motion-instant-submit-answer"
               data-testid="lesson-check-submit"
               disabled={answer.kind === "none" || isWorking || verdict !== null}
               onClick={submit}
            >
               Check my answer
            </button>
         </div>

         {failed ? <ActionFailed /> : null}

         {verdict !== null && verdict.correct ? (
            <p className="verdict" data-testid="lesson-check-verdict" style={{ color: "var(--growth-state-correct)" }}>
               <span aria-hidden="true">{CORRECT_GLYPH}</span> <span>{CORRECT_WORD}</span>
            </p>
         ) : null}

         {isWrong ? (
            <div className="stack stack-tight" data-testid="lesson-check-verdict" aria-live="polite">
               <p className="verdict" style={{ color: "var(--growth-state-incorrect)" }}>
                  <span aria-hidden="true">{INCORRECT_GLYPH}</span> <span>{NOT_YET}</span>
               </p>

               {namesError ? (
                  <>
                     <p>
                        <LessonText text={errorSection.observed_behavior ?? ""} />
                     </p>

                     {rightStepText !== null ? (
                        <p data-testid="lesson-verdict-right-step">
                           {RIGHT_STEP_PREFIX}
                           <LessonText text={rightStepText} />
                           {showsRightStepValue ? (
                              <>
                                 {" "}
                                 <MathValue value={rightStepValue} />
                              </>
                           ) : null}
                        </p>
                     ) : null}

                     {consequence !== null ? (
                        <p data-testid="lesson-verdict-consequence">
                           {CONSEQUENCE_PREFIX}
                           <LessonText text={consequence} />
                        </p>
                     ) : null}

                     <div className="cluster">
                        <LessonLink anchor={anchor} onOpen={onOpenAnchor}>
                           Go to the part on that error
                        </LessonLink>

                        {offersRetry ? (
                           <button type="button" className="text-button" data-testid="lesson-check-retry" onClick={retry}>
                              Try again
                           </button>
                        ) : null}
                     </div>
                  </>
               ) : null}

               {showsSolution ? (
                  <ol className="worked-steps" data-testid="lesson-check-solution">
                     {(check.worked_solution ?? []).map((step) => (
                        <li key={step.step}>
                           <LessonText text={step.text} />
                        </li>
                     ))}
                  </ol>
               ) : null}
            </div>
         ) : null}
      </div>
   );
}
