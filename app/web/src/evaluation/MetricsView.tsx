import type { ArmOutcomes, ExperimentComparison, LearningMetric, MetricValue, MetricsPayload } from "../api/types";
import { formatPlanDate } from "../home/dates";
import { SCORED_BY_STUDENT } from "../progress/CheckpointHistory";
import { formatFigure } from "../progress/figures";

/* The operator's evidence of whether the app teaches (11 P7, docs/plan/10 "Learning-outcome
   metrics"). It is reached from settings and never from the bar or home, because 08 rules out a
   dashboard in the student's path. Every value is a sentence that names its denominator, and a value
   whose denominator is 0 says there is nothing to count and prints no figure, since a count without
   a denominator is not a claim. */

export const SIMULATION_RECORD = "docs/operator/p7-evals.md";

export interface MetricsViewProps {
   metrics: MetricsPayload;
}

export function valueSentence(entry: MetricValue) {
   const hasDenominator = entry.denominator > 0;

   if (!hasDenominator) {
      return `${entry.label}, no ${entry.denominator_label} yet (0).`;
   }

   const hasFigure = entry.value !== null;
   const hasNumerator = entry.numerator !== null;
   const figure = hasFigure ? `${entry.label} ${formatFigure(entry.value as number)}` : entry.label;
   const counted = hasNumerator
      ? `${entry.numerator} over ${entry.denominator} ${entry.denominator_label}`
      : `over ${entry.denominator} ${entry.denominator_label}`;
   const hasPublishedTotal = typeof entry.published_total === "number";
   const publishedTotal = hasPublishedTotal ? formatFigure(entry.published_total as number) : "";
   const published = hasPublishedTotal ? `, against a published mean total of ${publishedTotal}` : "";
   const isSelfScored = entry.scored_by === SCORED_BY_STUDENT;
   const scorer = isSelfScored ? ", scored by the student against the published scoring guidelines" : "";

   return `${figure}, ${counted}${published}${scorer}.`;
}

function armSentence(arm: ArmOutcomes) {
   const hasOutcomes = arm.outcomes > 0;

   if (!hasOutcomes) {
      return `${arm.arm}, no outcomes yet (0).`;
   }

   return `${arm.arm}, ${arm.correct} correct of ${arm.outcomes} outcomes.`;
}

function outcomesStillNeeded(arm: ArmOutcomes, minimum: number) {
   return Math.max(0, minimum - arm.outcomes);
}

function ExperimentResult({ comparison }: { comparison: ExperimentComparison }) {
   const minimum = comparison.minimum_outcomes_per_arm;
   const hasInterval = comparison.stated && comparison.interval_low !== null && comparison.interval_high !== null;

   return (
      <article data-testid="experiment-result">
         <h3 className="label-heading">{comparison.name}</h3>

         <ul>
            <li data-testid="experiment-arm">{armSentence(comparison.control)}</li>
            <li data-testid="experiment-arm">{armSentence(comparison.treatment)}</li>
         </ul>

         {hasInterval ? (
            <p data-testid="experiment-interval">
               Difference in delayed accuracy, {comparison.treatment.arm} minus {comparison.control.arm},{" "}
               {formatFigure(comparison.difference as number)}, with a 95 percent interval from{" "}
               {formatFigure(comparison.interval_low as number)} to {formatFigure(comparison.interval_high as number)}.
            </p>
         ) : (
            <p data-testid="experiment-shortfall">
               The interval is stated once each arm holds {minimum} outcomes. {comparison.control.arm} needs{" "}
               {outcomesStillNeeded(comparison.control, minimum)} more and {comparison.treatment.arm} needs{" "}
               {outcomesStillNeeded(comparison.treatment, minimum)} more.
            </p>
         )}
      </article>
   );
}

function MetricSection({ metric }: { metric: LearningMetric }) {
   return (
      <section data-testid="metric" data-status={metric.status}>
         <h2 className="section-heading">{metric.name}</h2>

         <p className="caption">{metric.definition}</p>

         {metric.window === null ? null : (
            <p className="caption">
               From {formatPlanDate(metric.window.start)} to {formatPlanDate(metric.window.end)}.
            </p>
         )}

         <ul>
            {metric.values.map((entry, index) => (
               <li key={`${index}-${entry.label}`} data-testid="metric-value">
                  {valueSentence(entry)}
               </li>
            ))}
         </ul>
      </section>
   );
}

export function MetricsView({ metrics }: MetricsViewProps) {
   return (
      <section className="card settings" data-testid="metrics-view">
         <h1 className="screen-title">Evidence of learning</h1>

         <p className="muted">
            For the operator, as of {formatPlanDate(metrics.as_of)}. Each figure names what it is counted over.
            The simulation record is in {SIMULATION_RECORD}.
         </p>

         {metrics.metrics.map((metric) => (
            <MetricSection key={metric.key} metric={metric} />
         ))}

         <section data-testid="experiments">
            <h2 className="section-heading">Experiments</h2>

            {metrics.experiments.map((comparison) => (
               <ExperimentResult key={comparison.name} comparison={comparison} />
            ))}
         </section>
      </section>
   );
}