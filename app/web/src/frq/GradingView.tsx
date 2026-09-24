import type { GradedPoint, GradingsPayload } from "../api/types";
import { MathText } from "../math/MathText";

/* 03 "What the student sees for a provisional grade" and 08's provisional-grade copy: a provisional
   point shows its rule, the evidence from the student's own work and a plain statement that the
   app could not decide it; it is left out of the shown score. Every point, provisional or not,
   carries the one-click re-read. No predicted AP score appears anywhere. */

export interface GradingViewProps {
   gradings: GradingsPayload;
   onAskForReread: (gradingId: string) => void;
   rereadAskedFor: ReadonlyArray<string>;
}

export function pointVerdict(point: GradedPoint) {
   if (point.provisional) {
      return "Provisional";
   }

   return point.earned === 1 ? "Earned" : "Not earned";
}

function PointEntry(props: { point: GradedPoint; onAskForReread: (gradingId: string) => void; asked: boolean }) {
   const { point, onAskForReread, asked } = props;
   const hasQuote = (point.evidence_quote ?? "") !== "";
   const hasEligibility = (point.eligibility_note ?? "") !== "";

   return (
      <li data-testid="graded-point" data-provisional={point.provisional ? "true" : "false"}>
         <p>
            <strong>
               Part ({point.part_id}), {point.point_label}: {pointVerdict(point)}
            </strong>
         </p>

         <p className="muted">{point.criterion}</p>

         {point.provisional ? (
            <p data-testid="provisional-copy">
               This point is provisional. {point.rationale}. It is not counted until it is decided, and you
               can ask for it to be re-read.
            </p>
         ) : (
            <p className="muted">{point.rationale}</p>
         )}

         {hasQuote ? (
            <p className="muted">
               From your work: <MathText text={point.evidence_quote ?? ""} />
            </p>
         ) : null}

         {hasEligibility ? <p className="muted">{point.eligibility_note}</p> : null}

         {asked ? (
            <span className="muted">Re-read asked for</span>
         ) : (
            <button type="button" className="text-button" onClick={() => onAskForReread(point.grading_id)}>
               Ask for a re-read
            </button>
         )}
      </li>
   );
}

export function GradingView({ gradings, onAskForReread, rereadAskedFor }: GradingViewProps) {
   const hasProvisional = gradings.provisional > 0;

   return (
      <section aria-labelledby="gradings-heading">
         <h2 id="gradings-heading" className="section-heading">
            Points
         </h2>

         <p data-testid="grading-summary">
            {gradings.earned} of the {gradings.decided} decided points earned
            {hasProvisional ? `, ${gradings.provisional} provisional and not counted` : ""}.
         </p>

         <ul className="review-list">
            {gradings.points.map((point) => (
               <PointEntry
                  key={point.grading_id}
                  point={point}
                  onAskForReread={onAskForReread}
                  asked={rereadAskedFor.includes(point.grading_id)}
               />
            ))}
         </ul>

         {gradings.worked_solution.length > 0 ? (
            <section aria-labelledby="worked-heading">
               <h3 id="worked-heading">What a full answer shows</h3>

               {gradings.worked_solution.map((part) => (
                  <div key={part.part_id}>
                     <p>
                        <strong>({part.part_id})</strong> <MathText text={`\\(${part.answer_latex}\\)`} />
                     </p>

                     <ol>
                        {part.steps.map((step, index) => (
                           <li key={index}>
                              {step.text} <MathText text={`\\(${step.latex}\\)`} />
                           </li>
                        ))}
                     </ol>
                  </div>
               ))}
            </section>
         ) : null}
      </section>
   );
}
