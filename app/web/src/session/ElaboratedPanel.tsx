import { useEffect, useState } from "react";

import { affordanceProps } from "../affordances";
import { answerLessonCheck, readLesson } from "../api/client";
import { motionClass } from "../styles/motion";
import type { CorrectAnswer, ElaboratedPayload, FeedbackLessonLink, LessonPlan, LessonRecord } from "../api/types";
import { LessonReader } from "../lessons/LessonReader";
import { sectionIdMatches } from "../lessons/LessonLink";
import { MathText } from "../math/MathText";
import { MathValue } from "../math/MathValue";
import { INCORRECT_GLYPH, INCORRECT_WORD } from "./StepMarks";

export const READ_THE_PART_LABEL = "Read the part on this error";

export const BACK_TO_FEEDBACK_LABEL = "Back to the feedback";

export const CORRECT_RESULT_LABEL = "The step should give";

export interface ElaboratedPanelProps {
   elaborated: ElaboratedPayload | null;
   sentence: string | null;
   lessonLink?: FeedbackLessonLink | null;
   correctAnswer?: CorrectAnswer | null;
}

/* 03 Content, part 3: what the correct response would have shown, read as the violated step's
   result. The server sends it only after a wrong answer is graded. */
export function CorrectResult({ answer }: { answer: CorrectAnswer | null | undefined }) {
   if (answer === null || answer === undefined) {
      return null;
   }

   const hasLabel = answer.label !== null && answer.label.trim().length > 0;
   const hasValue = answer.mathjson !== null && answer.mathjson !== undefined;

   if (!hasLabel && !hasValue) {
      return null;
   }

   return (
      <div className="stack stack-tight sheet-row" data-testid="correct-answer">
         <p className="sheet-margin sheet-tag">{CORRECT_RESULT_LABEL}</p>

         <p className="sheet-body note-quote math-overflow">
            {hasLabel ? <MathText text={answer.label as string} /> : <MathValue value={answer.mathjson} />}
         </p>
      </div>
   );
}

/* 15 Diagnosis links: the lesson opens at the error's block, in the library reader, so it reads as
   a reference rather than a lesson slot and writes no session event. The plan is that one block. */
function anchoredPlan(lesson: LessonRecord, link: FeedbackLessonLink): LessonPlan {
   const section = lesson.sections.find((entry) => sectionIdMatches(entry.id, link.anchor));
   const sections = section === undefined ? [] : [{ id: section.id, type: section.type, form: "full" as const }];

   return {
      lesson_id: lesson.id,
      version: lesson.version,
      band: "low",
      reason: "feedback",
      sections,
      checks: [],
      minutes: 1,
      words: 0,
      anchors: [link.anchor]
   };
}

function LessonAtAnchor({ link, onClose }: { link: FeedbackLessonLink; onClose: () => void }) {
   const [lesson, setLesson] = useState<LessonRecord | null>(null);
   const [failed, setFailed] = useState(false);

   useEffect(() => {
      let isCurrent = true;

      readLesson(link.lesson_id, link.version)
         .then((payload) => {
            if (isCurrent) {
               setLesson(payload);
            }
         })
         .catch(() => {
            if (isCurrent) {
               setFailed(true);
            }
         });

      return () => {
         isCurrent = false;
      };
   }, [link]);

   return (
      <div className="lesson-inline" data-testid="error-lesson" data-anchor={link.anchor}>
         {lesson !== null ? (
            <LessonReader
               lesson={lesson}
               plan={anchoredPlan(lesson, link)}
               band="low"
               context="library"
               onComplete={onClose}
               onSkip={onClose}
               onSectionViewed={() => undefined}
               onCheckAnswer={(checkId, body) => answerLessonCheck(link.lesson_id, checkId, body)}
            />
         ) : null}

         {failed ? <p className="muted">The lesson could not be opened just now.</p> : null}

         <button type="button" className="text-button" data-testid="error-lesson-close" onClick={onClose}>
            {BACK_TO_FEEDBACK_LABEL}
         </button>
      </div>
   );
}

export function ElaboratedPanel({ elaborated, sentence, lessonLink = null, correctAnswer = null }: ElaboratedPanelProps) {
   const [isReading, setIsReading] = useState(false);

   if (elaborated === null) {
      return null;
   }

   const hasSentence = sentence !== null && sentence.trim().length > 0;

   return (
      <section
         {...affordanceProps("elaboratedFeedbackPanel")}
         className={`${motionClass("elaboratedFeedbackPanel")} sheet-row`}
         data-testid="elaborated-panel"
      >
         <p className="sheet-margin verdict step-mark-verdict" data-testid="elaborated-verdict" style={{ color: "var(--growth-state-incorrect)" }}>
            <span data-glyph aria-hidden="true">
               {INCORRECT_GLYPH}
            </span>
            <span>{INCORRECT_WORD}</span>
         </p>

         <div className="sheet-body sheet-body-stack">
            {elaborated.violated_step !== null ? (
               <p data-testid="violated-step">{elaborated.violated_step}</p>
            ) : null}

            <CorrectResult answer={correctAnswer} />

            {elaborated.observed_behavior !== null ? (
               <p data-testid="observed-behavior">{elaborated.observed_behavior}</p>
            ) : null}

            {elaborated.scoring_consequence !== null ? (
               <p className="muted" data-testid="scoring-consequence">{elaborated.scoring_consequence}</p>
            ) : null}

            {hasSentence ? <p className="tutor-note" data-testid="tutor-sentence">{sentence}</p> : null}

            {lessonLink !== null && !isReading ? (
               <button type="button" className="text-button" data-testid="read-error-part" data-anchor={lessonLink.anchor} onClick={() => setIsReading(true)}>
                  {READ_THE_PART_LABEL}
               </button>
            ) : null}

            {lessonLink !== null && isReading ? <LessonAtAnchor link={lessonLink} onClose={() => setIsReading(false)} /> : null}
         </div>
      </section>
   );
}