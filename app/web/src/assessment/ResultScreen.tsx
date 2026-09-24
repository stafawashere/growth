import type { AssessmentResult, PacingRatio, PartPacing, QuestionComparison } from "../api/types";
import { formatFigure } from "../progress/figures";
import { clockText } from "./format";

/* 05 "AP score estimate" and 08's mock score copy. A full mock shows a band with its assumptions
   on the same screen and never a single number or a centre. The statement is the server's own
   sentence, shown as sent. A drill shows pacing and counts and no band. */

export interface ResultScreenProps {
   result: AssessmentResult;
   onDone: () => void;
}

function ratioText(ratio: PacingRatio) {
   return `${ratio.numerator} of ${ratio.denominator}`;
}

function secondsText(seconds: number | null) {
   return seconds === null ? "not recorded" : clockText(seconds * 1000);
}

function PacingRows(props: { pacing: PartPacing }) {
   const { pacing } = props;
   const hasMean = pacing.mean_seconds_per_question !== null;
   const meanText = hasMean
      ? `${formatFigure(pacing.mean_seconds_per_question as number)} seconds per question, over ${ratioText(pacing.mean_counts)} questions, against a budget of ${formatFigure(pacing.budget_seconds_per_question)} seconds`
      : `no timed question to average, against a budget of ${formatFigure(pacing.budget_seconds_per_question)} seconds`;

   return (
      <article data-testid="pacing-part">
         <h3 className="label-heading">{pacing.label}</h3>

         <ul>
            <li>
               Time used: {secondsText(pacing.time_used_seconds)} of {clockText(pacing.limit_seconds * 1000)}
            </li>
            <li>Mean time: {meanText}</li>
            <li>Answered: {ratioText(pacing.answered)}</li>
            <li>Rapid guesses: {ratioText(pacing.rapid_guess)}</li>
            <li>Revisits after answering: {ratioText(pacing.revisit)}</li>
            <li>Marked for review: {ratioText(pacing.marked)}</li>
         </ul>
      </article>
   );
}

function ComparisonTable(props: { questions: QuestionComparison[] }) {
   const years = [...new Set(props.questions.flatMap((question) => question.published.map((entry) => entry.year)))].sort();

   return (
      <table data-testid="question-comparison">
         <caption className="caption">
            Your points on each free-response question against the published mean for the question in the same
            position. These are the app's own questions, so the comparison is by position, not by problem.
         </caption>

         <thead>
            <tr>
               <th scope="col">Question</th>
               <th scope="col">Your points</th>
               {years.map((year) => (
                  <th key={year} scope="col">
                     {year} mean
                  </th>
               ))}
            </tr>
         </thead>

         <tbody>
            {props.questions.map((question) => {
               const hasPending = question.pending > 0;

               return (
                  <tr key={question.question}>
                     <th scope="row">Question {question.question}</th>
                     <td>
                        {question.earned} of {question.possible}
                        {hasPending ? `, ${question.pending} pending` : ""}
                     </td>
                     {years.map((year) => {
                        const published = question.published.find((entry) => entry.year === year);

                        return <td key={year}>{published === undefined ? "none published" : formatFigure(published.mean)}</td>;
                     })}
                  </tr>
               );
            })}
         </tbody>
      </table>
   );
}

export function ResultScreen({ result, onDone }: ResultScreenProps) {
   const band = result.band;
   const hasBand = band !== undefined;
   const multipleChoice = result.multiple_choice;
   const freeResponse = result.free_response;
   const questions = result.questions ?? [];

   return (
      <section className="card result" data-testid="assessment-result">
         <h1 className="screen-title">{result.mode === "mock" ? "Mock exam result" : "Part drill result"}</h1>

         {hasBand ? (
            <section data-testid="band-section">
               {result.statement !== undefined ? <p data-testid="band-statement">{result.statement}</p> : null}

               <p className="verdict" data-testid="band">
                  Band: {band.low} to {band.high}
               </p>

               <h2 className="section-heading">Assumptions</h2>

               <ul data-testid="band-assumptions">
                  {(result.assumptions ?? []).map((assumption) => (
                     <li key={assumption.key}>{assumption.text}</li>
                  ))}
               </ul>
            </section>
         ) : null}

         <section data-testid="raw-counts">
            <h2 className="section-heading">Raw counts</h2>

            <ul>
               {multipleChoice !== null ? (
                  <li>
                     Multiple choice: {multipleChoice.correct} of {multipleChoice.total} correct
                  </li>
               ) : null}

               {freeResponse !== undefined ? (
                  <li>
                     Free response: {freeResponse.earned} points earned, {freeResponse.pending} pending, of {freeResponse.total}
                  </li>
               ) : null}
            </ul>
         </section>

         {questions.length > 0 ? <ComparisonTable questions={questions} /> : null}

         <section data-testid="pacing">
            <h2 className="section-heading">Pacing</h2>

            {result.pacing.map((pacing) => (
               <PacingRows key={pacing.part_key} pacing={pacing} />
            ))}
         </section>

         <button type="button" className="text-button" onClick={onDone}>
            Back to the mock exam screen
         </button>
      </section>
   );
}
