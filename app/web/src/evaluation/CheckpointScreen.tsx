import { useEffect, useState } from "react";

import type { CheckpointPart, CheckpointQuestion, CheckpointSection, CheckpointView } from "../api/types";
import { CheckpointResult } from "../progress/CheckpointHistory";

/* The six-week checkpoint (11 P7 scope item 5). The form is released College Board material used by
   reference only (app/checkpoint/forms.py): this screen names the year, the parts and the questions
   and links College Board's own documents, and it never renders a question's text, because the app
   holds none. The student works on paper and enters the points earned per part. */

export const MASTERY_NOTE = "This checkpoint does not change anything in the mastery model.";

export const NEW_TAB_REL = "noopener noreferrer";

export interface CheckpointIntroProps {
   refusal: string | null;
   onStart: () => void;
   onLeave: () => void;
}

export interface CheckpointScreenProps {
   checkpoint: CheckpointView;
   onScore: (recordId: string, pointsEarned: number) => Promise<boolean>;
   onFinish: () => Promise<boolean>;
   onLeave: () => void;
}

export function CheckpointIntro({ refusal, onStart, onLeave }: CheckpointIntroProps) {
   return (
      <section className="card" data-testid="checkpoint-intro">
         <h1 className="screen-title">Checkpoint</h1>

         <p>
            A checkpoint is one released AP free-response form, worked on paper under the exam&apos;s part
            timings and scored by you against College Board&apos;s published scoring guidelines.
         </p>

         <p>{MASTERY_NOTE} It checks whether the practice numbers hold up against released exam material.</p>

         {refusal === null ? null : <p role="alert">{refusal}</p>}

         <button type="button" className="button-primary" onClick={onStart}>
            Start the checkpoint
         </button>

         <button type="button" className="text-button" onClick={onLeave}>
            Back to progress
         </button>
      </section>
   );
}

function wholePointsIn(text: string) {
   const trimmed = text.trim();
   const isWhole = /^\d+$/.test(trimmed);

   return isWhole ? Number(trimmed) : null;
}

function PartScore(props: {
   part: CheckpointPart;
   saved: number | undefined;
   onScore: CheckpointScreenProps["onScore"];
}) {
   const { part, saved, onScore } = props;

   const savedText = saved === undefined ? "" : String(saved);
   const [text, setText] = useState(savedText);
   const [working, setWorking] = useState(false);

   useEffect(() => {
      setText(savedText);
   }, [savedText]);

   const points = wholePointsIn(text);
   const isInRange = points !== null && points <= part.points;
   const isChanged = text.trim() !== savedText;
   const canSave = isInRange && isChanged && !working;
   const isOutOfRange = text.trim() !== "" && !isInRange;

   async function save() {
      if (!canSave) {
         return;
      }

      setWorking(true);

      try {
         await onScore(part.record_id, points as number);
      } finally {
         setWorking(false);
      }
   }

   return (
      <div className="field" data-testid="part-score" data-record-id={part.record_id}>
         <label>
            Part ({part.part.toLowerCase()}), points earned out of {part.points}
            <input
               type="text"
               inputMode="numeric"
               value={text}
               aria-invalid={isOutOfRange}
               onChange={(event) => setText(event.target.value)}
            />
         </label>

         {isOutOfRange ? (
            <p className="caption" role="alert">
               Enter a whole number of points from 0 to {part.points}.
            </p>
         ) : null}

         <button type="button" className="text-button" disabled={!canSave} onClick={save}>
            save
         </button>
      </div>
   );
}

function QuestionBlock(props: {
   question: CheckpointQuestion;
   checkpoint: CheckpointView;
   onScore: CheckpointScreenProps["onScore"];
}) {
   const { question, checkpoint, onScore } = props;
   const year = checkpoint.form_year;

   return (
      <article data-testid="checkpoint-question-block">
         <h3 className="label-heading">Question {question.question}</h3>

         <p>
            <a href={checkpoint.free_response_url} target="_blank" rel={NEW_TAB_REL} data-testid="free-response-link">
               Question {question.question} in the {year} free-response questions
            </a>
         </p>

         <p>
            <a
               href={checkpoint.scoring_guidelines_url}
               target="_blank"
               rel={NEW_TAB_REL}
               data-testid="scoring-guidelines-link"
            >
               Question {question.question} in the {year} scoring guidelines
            </a>
         </p>

         {question.parts.map((part) => (
            <PartScore key={part.record_id} part={part} saved={checkpoint.scores[part.record_id]} onScore={onScore} />
         ))}
      </article>
   );
}

function SectionBlock(props: {
   section: CheckpointSection;
   checkpoint: CheckpointView;
   onScore: CheckpointScreenProps["onScore"];
}) {
   const { section, checkpoint, onScore } = props;

   return (
      <section data-testid="checkpoint-section">
         <h2 className="section-heading">
            Part {section.part}, {section.minutes} minutes, calculator {section.calculator.toLowerCase()}
         </h2>

         {section.questions.map((question) => (
            <QuestionBlock key={question.question} question={question} checkpoint={checkpoint} onScore={onScore} />
         ))}
      </section>
   );
}

function everyPartIsScored(checkpoint: CheckpointView) {
   const parts = checkpoint.sections.flatMap((section) => section.questions.flatMap((question) => question.parts));

   return parts.every((part) => checkpoint.scores[part.record_id] !== undefined);
}

export function CheckpointScreen({ checkpoint, onScore, onFinish, onLeave }: CheckpointScreenProps) {
   const [finishing, setFinishing] = useState(false);

   const isFinished = checkpoint.finished_at !== null;
   const canFinish = everyPartIsScored(checkpoint) && !finishing;

   async function finish() {
      setFinishing(true);

      try {
         await onFinish();
      } finally {
         setFinishing(false);
      }
   }

   if (isFinished) {
      return (
         <section className="card" data-testid="checkpoint-finished">
            <h1 className="screen-title">Checkpoint</h1>

            <CheckpointResult checkpoint={checkpoint} />

            <p>{MASTERY_NOTE}</p>

            <button type="button" className="text-button" onClick={onLeave}>
               Back to progress
            </button>
         </section>
      );
   }

   return (
      <section className="card" data-testid="checkpoint-screen">
         <h1 className="eyebrow">Checkpoint</h1>

         <h2 className="screen-title">{checkpoint.form_year} released free-response form</h2>

         <p>{MASTERY_NOTE}</p>

         <p>
            Work each part on paper within its time and under its calculator rule. Then score each part
            against the scoring guidelines and enter the points you earned.
         </p>

         {checkpoint.sections.map((section) => (
            <SectionBlock key={section.part} section={section} checkpoint={checkpoint} onScore={onScore} />
         ))}

         <button type="button" className="button-primary" disabled={!canFinish} onClick={finish}>
            Finish the checkpoint
         </button>

         <button type="button" className="text-button" onClick={onLeave}>
            Back to progress
         </button>
      </section>
   );
}