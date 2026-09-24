import type { CalibrationBin, CalibrationPayload } from "../api/types";

/* The calibration curve beneath the mastery map on progress, 08-design-brief.md "Progress".

   08's wireframe also draws an ideal diagonal and a sentence such as "overconfident on confident
   by 18 points". Both need each rating mapped to a probability, and no plan document fixes that
   mapping, so neither is drawn: the curve shows observed accuracy per stated level, its Wilson
   95 percent interval and the attempt count, and nothing that would imply a target it cannot
   source. Nothing here animates, so reduced motion has nothing to replace. */

export interface CalibrationCurveProps {
   calibration: CalibrationPayload;
}

const LEVEL_LABELS: Record<CalibrationBin["confidence"], string> = {
   guess: "guess",
   unsure: "unsure",
   confident: "confident"
};

const VIEW_WIDTH = 480;

const VIEW_HEIGHT = 300;

const PLOT_LEFT = 64;

const PLOT_RIGHT = 464;

const PLOT_TOP = 32;

const PLOT_BOTTOM = 236;

const POINT_RADIUS = 6;

const INTERVAL_CAP_HALF_WIDTH = 8;

const ACCURACY_TICKS = [0, 0.5, 1];

const TITLE_ID = "calibration-curve-title";

const DESCRIPTION_ID = "calibration-curve-description";

const captionText = {
   fill: "var(--growth-text-secondary)",
   fontSize: "var(--growth-type-caption)"
};

export function percent(value: number) {
   return `${Math.round(value * 100)} percent`;
}

function levelX(index: number, levelCount: number) {
   const slotWidth = (PLOT_RIGHT - PLOT_LEFT) / levelCount;

   return PLOT_LEFT + slotWidth * (index + 0.5);
}

function accuracyY(accuracy: number) {
   return PLOT_BOTTOM - accuracy * (PLOT_BOTTOM - PLOT_TOP);
}

function attemptCount(attempts: number) {
   return attempts === 1 ? "1 attempt" : `${attempts} attempts`;
}

function hasObservation(bin: CalibrationBin) {
   const hasAttempts = bin.attempts > 0;
   const hasAccuracy = bin.accuracy !== null;
   const hasLowerBound = bin.interval_low !== null;
   const hasUpperBound = bin.interval_high !== null;

   return hasAttempts && hasAccuracy && hasLowerBound && hasUpperBound;
}

function NotYet({ calibration }: CalibrationCurveProps) {
   return (
      <p data-testid="calibration-not-yet">
         The calibration curve needs {calibration.minimum_rated_attempts} confidence-rated attempts from
         the last {calibration.window_days} days. {calibration.rated_attempts} are recorded so far, so{" "}
         {calibration.attempts_needed} more are needed.
      </p>
   );
}

function BinMark(props: { bin: CalibrationBin; x: number }) {
   const { bin, x } = props;

   if (!hasObservation(bin)) {
      return (
         <text x={x} y={PLOT_BOTTOM - POINT_RADIUS * 2} textAnchor="middle" style={captionText}>
            n = 0
         </text>
      );
   }

   const pointY = accuracyY(bin.accuracy!);
   const lowY = accuracyY(bin.interval_low!);
   const highY = accuracyY(bin.interval_high!);

   return (
      <g data-testid="calibration-point" data-confidence={bin.confidence}>
         <line
            x1={x}
            x2={x}
            y1={lowY}
            y2={highY}
            stroke="var(--growth-accent-base)"
            strokeWidth={2}
            data-testid="calibration-interval"
         />
         <line
            x1={x - INTERVAL_CAP_HALF_WIDTH}
            x2={x + INTERVAL_CAP_HALF_WIDTH}
            y1={lowY}
            y2={lowY}
            stroke="var(--growth-accent-base)"
            strokeWidth={2}
         />
         <line
            x1={x - INTERVAL_CAP_HALF_WIDTH}
            x2={x + INTERVAL_CAP_HALF_WIDTH}
            y1={highY}
            y2={highY}
            stroke="var(--growth-accent-base)"
            strokeWidth={2}
         />
         <circle cx={x} cy={pointY} r={POINT_RADIUS} fill="var(--growth-accent-base)" />
         <text x={x} y={highY - POINT_RADIUS * 2} textAnchor="middle" style={captionText}>
            n = {bin.attempts}
         </text>
      </g>
   );
}

function Axes(props: { bins: ReadonlyArray<CalibrationBin> }) {
   const { bins } = props;

   return (
      <g aria-hidden="true">
         <line
            x1={PLOT_LEFT}
            x2={PLOT_LEFT}
            y1={PLOT_TOP}
            y2={PLOT_BOTTOM}
            stroke="var(--growth-text-muted)"
            strokeWidth={1}
         />
         <line
            x1={PLOT_LEFT}
            x2={PLOT_RIGHT}
            y1={PLOT_BOTTOM}
            y2={PLOT_BOTTOM}
            stroke="var(--growth-text-muted)"
            strokeWidth={1}
         />

         {ACCURACY_TICKS.map((tick) => (
            <text
               key={tick}
               x={PLOT_LEFT - POINT_RADIUS * 2}
               y={accuracyY(tick)}
               textAnchor="end"
               dominantBaseline="middle"
               style={captionText}
            >
               {tick.toFixed(1)}
            </text>
         ))}

         <text x={PLOT_LEFT} y={PLOT_TOP - POINT_RADIUS * 2} textAnchor="middle" style={captionText}>
            accuracy
         </text>

         {bins.map((bin, index) => (
            <text
               key={bin.confidence}
               x={levelX(index, bins.length)}
               y={PLOT_BOTTOM + POINT_RADIUS * 4}
               textAnchor="middle"
               style={captionText}
            >
               {LEVEL_LABELS[bin.confidence]}
            </text>
         ))}

         <text x={PLOT_RIGHT} y={VIEW_HEIGHT - POINT_RADIUS} textAnchor="end" style={captionText}>
            confidence
         </text>
      </g>
   );
}

function CurveTable({ calibration }: CalibrationCurveProps) {
   return (
      <table data-testid="calibration-table">
         <caption className="caption">
            Observed accuracy by stated confidence, {calibration.rated_attempts} rated attempts from{" "}
            {calibration.window_start} to {calibration.window_end}
         </caption>
         <thead>
            <tr>
               <th scope="col">Confidence</th>
               <th scope="col">Attempts</th>
               <th scope="col">Correct</th>
               <th scope="col">Observed accuracy</th>
               <th scope="col">95 percent interval</th>
            </tr>
         </thead>
         <tbody>
            {calibration.bins.map((bin) => {
               const observed = hasObservation(bin);

               return (
                  <tr key={bin.confidence}>
                     <th scope="row">{LEVEL_LABELS[bin.confidence]}</th>
                     <td>{bin.attempts}</td>
                     <td>{bin.correct}</td>
                     <td>{observed ? percent(bin.accuracy!) : "no attempts"}</td>
                     <td>
                        {observed ? `${percent(bin.interval_low!)} to ${percent(bin.interval_high!)}` : "none"}
                     </td>
                  </tr>
               );
            })}
         </tbody>
      </table>
   );
}

function Curve({ calibration }: CalibrationCurveProps) {
   const { bins } = calibration;

   return (
      <>
         <svg
            role="img"
            aria-labelledby={`${TITLE_ID} ${DESCRIPTION_ID}`}
            viewBox={`0 0 ${VIEW_WIDTH} ${VIEW_HEIGHT}`}
            width="100%"
            data-testid="calibration-curve"
         >
            <title id={TITLE_ID}>Calibration curve</title>
            <desc id={DESCRIPTION_ID}>
               Observed accuracy for each stated confidence level, with its 95 percent interval, from{" "}
               {attemptCount(calibration.rated_attempts)}. The table that follows lists the same values.
            </desc>

            <Axes bins={bins} />

            {bins.map((bin, index) => (
               <BinMark key={bin.confidence} bin={bin} x={levelX(index, bins.length)} />
            ))}
         </svg>

         <CurveTable calibration={calibration} />
      </>
   );
}

export function CalibrationCurve({ calibration }: CalibrationCurveProps) {
   const hasBins = calibration.bins.length > 0;
   const canDraw = calibration.available && hasBins;

   return (
      <section aria-labelledby="calibration-heading">
         <h2 id="calibration-heading" className="section-heading">
            Calibration, last {calibration.window_days} days
         </h2>

         {canDraw ? <Curve calibration={calibration} /> : <NotYet calibration={calibration} />}
      </section>
   );
}
