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
import { LessonText } from "./LessonText";
import { CORRECT_GLYPH, CORRECT_WORD, INCORRECT_GLYPH } from "../session/StepMarks";
import { ActionFailed } from "../status/LoadState";
import { LessonLink, sectionIdMatches } from "./LessonLink";

/* A lesson check (15 UI; CONTRACT.md Reader): the item input controls Item.tsx uses, MathLive for a
   short answer and McqControl for a choice, graded by the server. Feedback names the error block
   and links its anchor, in 15's Interface writing row: "Not yet. The two derivatives were
   multiplied. The part above on that error shows the right step beside it." There is no praise, no
   score and no percent, and a right answer reads Correct with its glyph and nothing more. A wrong
   answer with no error block to point at shows the check's worked solution instead. */

export const NOT_YET = "Not yet.";

export const ERROR_LINK_SENTENCE = "The part above on that error shows the right step beside it.";

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

type Answer = { kind: "none" } | { kind: "math"; value: unknown } | { kind: "option"; id: string };

export function LessonCheck({ check, sections, onCheckAnswer, onOpenAnchor, now = Date.now }: LessonCheckProps) {
   const [answer, setAnswer] = useState<Answer>({ kind: "none" });
   const [verdict, setVerdict] = useState<LessonCheckVerdict | null>(null);
   const [isWorking, setIsWorking] = useState(false);
   const [failed, setFailed] = useState(false);
   const [fieldFailed, setFieldFailed] = useState(false);
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

   const errorSection = verdict === null || verdict.correct ? null : errorSectionFor(verdict, sections);
   const anchor = errorSection === null ? null : verdict?.anchor ?? errorSection.id;

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
               <MathAnswerField label="My answer" onChange={(value) => setAnswer({ kind: "math", value })} onLoadFailure={() => setFieldFailed(true)} />
               {fieldFailed ? <p data-testid="answer-unavailable">{ANSWER_UNAVAILABLE_TEXT}</p> : null}
            </div>
         )}

         <div className="submit-row">
            <button
               type="button"
               className="button-primary motion-instant-submit-answer"
               data-testid="lesson-check-submit"
               disabled={answer.kind === "none" || isWorking}
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

         {verdict !== null && !verdict.correct ? (
            <div data-testid="lesson-check-verdict" aria-live="polite">
               {errorSection !== null && anchor !== null ? (
                  <>
                     <p>
                        <span className="verdict" style={{ color: "var(--growth-state-incorrect)" }}>
                           <span aria-hidden="true">{INCORRECT_GLYPH}</span> <span>{NOT_YET}</span>
                        </span>{" "}
                        <LessonText text={errorSection.observed_behavior ?? ""} /> {ERROR_LINK_SENTENCE}
                     </p>
                     <LessonLink anchor={anchor} onOpen={onOpenAnchor}>
                        Go to the part on that error
                     </LessonLink>
                  </>
               ) : (
                  <>
                     <p className="verdict" style={{ color: "var(--growth-state-incorrect)" }}>
                        <span aria-hidden="true">{INCORRECT_GLYPH}</span> <span>{NOT_YET}</span>
                     </p>
                     <ol className="worked-steps" data-testid="lesson-check-solution">
                     {(check.worked_solution ?? []).map((step) => (
                        <li key={step.step}>
                           <LessonText text={step.text} />
                        </li>
                     ))}
                     </ol>
                  </>
               )}
            </div>
         ) : null}
      </div>
   );
}
