import { useEffect, useRef, useState } from "react";

import { readCheck, saveCheckQuestion, submitCheck, type SaveQuestionFields } from "../api/client";
import type {
   AssessmentAnswer,
   AssessmentItem,
   AssessmentQuestion,
   AssessmentSession,
   CheckItemResult,
   CheckResult,
   Confidence,
   MovedSkill,
   SkillSnapshot
} from "../api/types";
import { FigureView } from "../figures/FigureView";
import { MathField } from "../input/MathField";
import { McqControl } from "../input/McqControl";
import { MathText } from "../math/MathText";
import { MathValue } from "../math/MathValue";
import { ConfidencePrompt } from "../session/ConfidencePrompt";
import { refusalText } from "./format";

/* 05 "Unit check": untimed, one question at a time with a confidence rating, and no correctness
   anywhere until the whole check is submitted, so one question's feedback cannot answer the
   next. After submission, the per-item breakdown, what moved per skill and the coverage with the
   skills the check could not reach. */

export interface UnitCheckScreenProps {
   sessionId: string;
   initial?: AssessmentSession;
   unitTitle?: string;
}

interface CheckWork {
   answer: AssessmentAnswer | null;
   confidence: Confidence | null;
}

function workFrom(questions: AssessmentQuestion[]) {
   return Object.fromEntries(
      questions.map((question) => [question.number, { answer: question.answer, confidence: question.confidence }])
   ) as Record<number, CheckWork>;
}

function servesChoice(question: AssessmentQuestion) {
   const item = question.item as AssessmentItem;
   const isChoice = question.kind === "mcq" || item.requires_choice === true;
   const hasOptions = Array.isArray(item.options) && item.options.length > 0;

   return isChoice && hasOptions;
}

function answerText(answer: AssessmentAnswer | null) {
   if (answer === null) {
      return null;
   }

   if (answer.option_id !== undefined) {
      return <>option {answer.option_id}</>;
   }

   return <MathValue value={answer.mathjson} />;
}

function snapshotText(snapshot: SkillSnapshot | null) {
   if (snapshot === null) {
      return "no record";
   }

   const masteryWord = snapshot.mastered ? "mastered" : "not mastered";

   return `${masteryWord}, ${snapshot.credited_successes} credited successes, ${snapshot.credited_failures} credited failures`;
}

function verdictText(item: CheckItemResult) {
   if (!item.answered) {
      return "Not answered";
   }

   if (item.correct === null) {
      return "Not graded";
   }

   return item.correct ? "Correct" : "Not correct";
}

function Breakdown(props: { result: CheckResult }) {
   const { result } = props;
   const unreached = Object.entries(result.coverage.unreached);
   const coveredCount = result.coverage.covered.length;
   const skillCount = coveredCount + unreached.length;

   return (
      <section className="card" data-testid="unit-check-breakdown">
         <h1 className="screen-title">Unit check, what it showed</h1>

         <h2 className="section-heading">Each question</h2>

         <ol className="review-list">
            {result.items.map((item) => (
               <li key={item.number} data-testid="check-item">
                  <p>
                     Question {item.number}: <strong>{verdictText(item)}</strong>
                     {item.answered ? <> Your answer: {answerText(item.answer)}.</> : null}
                     {item.key_option_id !== null ? <> The key is option {item.key_option_id}.</> : null}
                  </p>

                  {item.worked_solution.length > 0 ? (
                     <ol className="worked-steps">
                        {item.worked_solution.map((step) => (
                           <li key={step.step}>
                              <MathText text={step.text} />
                              {step.rule_named !== undefined ? <span className="muted"> ({step.rule_named})</span> : null}
                           </li>
                        ))}
                     </ol>
                  ) : null}
               </li>
            ))}
         </ol>

         <h2 className="section-heading">What moved</h2>

         {result.moved.length === 0 ? <p className="muted">No skill's record changed.</p> : null}

         <ul className="review-list" data-testid="moved-skills">
            {result.moved.map((skill: MovedSkill) => (
               <li key={skill.skill_id}>
                  <span>{skill.name}</span>
                  <span className="muted">
                     Before: {snapshotText(skill.before)}. After: {snapshotText(skill.after)}.
                  </span>
               </li>
            ))}
         </ul>

         <h2 className="section-heading">Coverage</h2>

         <p data-testid="coverage">
            The check reached {coveredCount} of the unit's {skillCount} skills.
         </p>

         {unreached.length > 0 ? (
            <ul className="review-list" data-testid="unreached-skills">
               {unreached.map(([skillId, reason]) => (
                  <li key={skillId}>
                     {skillId}: {reason}
                  </li>
               ))}
            </ul>
         ) : null}
      </section>
   );
}

export function UnitCheckScreen({ sessionId, initial, unitTitle }: UnitCheckScreenProps) {
   const [session, setSession] = useState<AssessmentSession | null>(initial ?? null);
   const [work, setWork] = useState<Record<number, CheckWork>>(() => workFrom(initial?.parts[0]?.questions ?? []));
   const [index, setIndex] = useState(0);
   const [result, setResult] = useState<CheckResult | null>(null);
   const [problem, setProblem] = useState<string | null>(null);
   const [answerUnavailable, setAnswerUnavailable] = useState(false);
   const pendingSaves = useRef<Promise<unknown>>(Promise.resolve());
   const unsavedMath = useRef<{ number: number; answer: AssessmentAnswer } | null>(null);

   useEffect(() => {
      if (initial !== undefined) {
         return;
      }

      readCheck(sessionId).then(
         (payload) => {
            setSession(payload);
            setWork(workFrom(payload.parts[0]?.questions ?? []));
         },
         (failure) => setProblem(refusalText(failure, "The unit check could not be loaded."))
      );
   }, []);

   if (result !== null) {
      return <Breakdown result={result} />;
   }

   if (session === null) {
      return problem === null ? <section aria-busy="true" data-testid="unit-check-waiting" /> : <p role="alert">{problem}</p>;
   }

   const questions = session.parts[0]?.questions ?? [];
   const question = questions[index];

   function save(number: number, fields: SaveQuestionFields) {
      pendingSaves.current = pendingSaves.current
         .then(() => saveCheckQuestion(sessionId, number, fields))
         .catch((failure) => setProblem(refusalText(failure, "Your answer could not be saved.")));
   }

   function change(number: number, changed: Partial<CheckWork>) {
      setWork((all) => ({ ...all, [number]: { ...all[number], ...changed } }));
      save(number, changed);
   }

   /* A typed answer changes on every keystroke, so it is saved when the student moves on. */
   function typeAnswer(number: number, mathjson: unknown) {
      const answer = { mathjson };

      setWork((all) => ({ ...all, [number]: { ...all[number], answer } }));
      unsavedMath.current = { number, answer };
   }

   function flushTyped() {
      const unsaved = unsavedMath.current;

      if (unsaved !== null) {
         unsavedMath.current = null;
         save(unsaved.number, { answer: unsaved.answer });
      }
   }

   function goTo(target: number) {
      flushTyped();
      setIndex(target);
   }

   async function submit() {
      setProblem(null);
      flushTyped();

      try {
         await pendingSaves.current;
         setResult(await submitCheck(sessionId));
      } catch (failure) {
         setProblem(refusalText(failure, "The unit check could not be submitted."));
      }
   }

   if (question === undefined) {
      return (
         <section className="card">
            <p className="muted">This unit check holds no questions.</p>
         </section>
      );
   }

   const item = question.item as AssessmentItem;
   const current = work[question.number] ?? { answer: null, confidence: null };
   const answeredCount = questions.filter((entry) => work[entry.number]?.answer !== null).length;
   const hasFigure = item.figure_spec !== null && item.figure_spec !== undefined;
   const isFirst = index === 0;
   const isLast = index === questions.length - 1;

   return (
      <section className="card" data-testid="unit-check">
         <h1 className="screen-title">{unitTitle === undefined ? "Unit check" : `Unit check, ${unitTitle}`}</h1>

         <p className="muted">Untimed. Nothing is marked right or wrong until you submit the whole check.</p>

         <p data-testid="question-position">
            Question {index + 1} of {questions.length}
         </p>

         {problem !== null ? <p role="alert">{problem}</p> : null}

         <p className="item-stem">
            <MathText text={item.stem} />
         </p>

         {hasFigure ? <FigureView spec={item.figure_spec} /> : null}

         {servesChoice(question) ? (
            <McqControl
               key={question.number}
               groupLabel="My answer"
               options={item.options ?? []}
               selectedId={current.answer?.option_id ?? null}
               onSelect={(optionId) => change(question.number, { answer: { option_id: optionId } })}
            />
         ) : (
            <div data-testid="math-answer">
               <MathField
                  key={question.number}
                  label="My answer"
                  onChange={(mathjson) => typeAnswer(question.number, mathjson)}
                  onLoadFailure={() => setAnswerUnavailable(true)}
               />

               {answerUnavailable ? <p role="alert">The math keyboard did not load, so this question cannot take an answer.</p> : null}
            </div>
         )}

         <ConfidencePrompt
            key={`confidence-${question.number}`}
            value={current.confidence}
            onChange={(confidence) => change(question.number, { confidence })}
         />

         <div className="choice-row">
            <button type="button" className="text-button motion-instant-question-move" disabled={isFirst} onClick={() => goTo(index - 1)}>
               Back
            </button>

            <button type="button" className="text-button motion-instant-question-move" disabled={isLast} onClick={() => goTo(index + 1)}>
               Next
            </button>
         </div>

         <p className="muted">
            {answeredCount} of {questions.length} answered.
         </p>

         <button type="button" className="button-primary" onClick={submit}>
            Submit check
         </button>
      </section>
   );
}
