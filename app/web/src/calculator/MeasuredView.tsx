import type { CalculatorCapabilityMeasure, CalculatorMeasuredPayload, CalculatorRatio, CalculatorRecentDrill } from "../api/types";
import { MathText } from "../math/MathText";
import {
   CAPABILITY_NAMES,
   CAPABILITY_ORDER,
   MEASURED_COLUMNS,
   NO_DRILLS_YET,
   NOT_MEASURED_YET,
   RECENT_HEADING,
   SETUP_TEXT,
   budgetLines,
   ratioText,
   secondsText,
   setupState,
   VALUE_ACCURATE,
   VALUE_NOT_ACCURATE
} from "./words";

/* docs/calculator/design.md, The measured view: per capability what has been measured, every
   figure over its denominator, the median time "not measured yet" under three answered drills (the
   server sends median_ms null there), the exam's two per-question figures, and the last twenty
   drills. No bar, no percent, no trend arrow, and nothing that says whether any of it is enough. */

function ratio(value: CalculatorRatio) {
   return ratioText(value.numerator, value.denominator);
}

export const MINIMUM_ANSWERED_FOR_MEDIAN = 3;

function medianText(measure: CalculatorCapabilityMeasure) {
   const isTooFew = measure.answered < MINIMUM_ANSWERED_FOR_MEDIAN;
   const isUnmeasured = isTooFew || measure.median_ms === null;

   return isUnmeasured ? NOT_MEASURED_YET : secondsText(measure.median_ms as number);
}

function inOrder(capabilities: CalculatorCapabilityMeasure[]) {
   return [...capabilities].sort((left, right) => CAPABILITY_ORDER.indexOf(left.capability) - CAPABILITY_ORDER.indexOf(right.capability));
}

/* The recent list reads the value verdict only as accurate or not, since the row carries no
   reason. */
function recentValueText(drill: CalculatorRecentDrill) {
   return drill.value_correct ? VALUE_ACCURATE : VALUE_NOT_ACCURATE;
}

function recentSetupText(drill: CalculatorRecentDrill) {
   const state = setupState({ shown: drill.setup_shown, correct: drill.setup_correct, reason: null, key_latex: "" });

   return SETUP_TEXT[state];
}

export function MeasuredView(props: { measured: CalculatorMeasuredPayload }) {
   const { measured } = props;
   const rows = inOrder(measured.capabilities);
   const hasRecent = measured.recent.length > 0;

   return (
      <div className="stack stack-loose" data-testid="calculator-measured">
         <div className="table-wrap">
            <table>
               <thead>
                  <tr>
                     {MEASURED_COLUMNS.map((column) => (
                        <th key={column} scope="col">
                           {column}
                        </th>
                     ))}
                  </tr>
               </thead>

               <tbody>
                  {rows.map((measure) => (
                     <tr key={measure.capability} data-testid="measured-row" data-capability={measure.capability}>
                        <th scope="row">{CAPABILITY_NAMES[measure.capability]}</th>
                        <td>{measure.answered}</td>
                        <td>{ratio(measure.value_correct)}</td>
                        <td>{ratio(measure.setup_shown)}</td>
                        <td>{ratio(measure.setup_correct)}</td>
                        <td data-testid="measured-median">{medianText(measure)}</td>
                     </tr>
                  ))}
               </tbody>
            </table>
         </div>

         <p className="helper" data-testid="measured-budget">
            {budgetLines(measured.budget_seconds["I-B"], measured.budget_seconds["II-A"])}
         </p>

         <section className="stack stack-tight">
            <h2 className="section-heading">{RECENT_HEADING}</h2>

            {hasRecent ? (
               <ul className="list" data-testid="measured-recent">
                  {measured.recent.map((drill) => (
                     <li key={drill.drill_id} className="list-row">
                        <span>{CAPABILITY_NAMES[drill.capability]}</span>
                        <MathText text={`\\(${drill.function_tex}\\)`} />
                        <span>{recentValueText(drill)}</span>
                        <span>{recentSetupText(drill)}</span>
                        <span>{secondsText(drill.elapsed_ms)}</span>
                     </li>
                  ))}
               </ul>
            ) : (
               <p className="muted">{NO_DRILLS_YET}</p>
            )}
         </section>
      </div>
   );
}
