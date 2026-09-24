import type { ProvisionalPoint } from "../api/types";

/* The grading-disputes section of 08's Review screen. It renders whatever GET /review carries in
   provisional_points, which stays empty until P3's grader writes gradings. P3 plugs its re-read
   path in through onAskForReread, which POSTs to /gradings/{gid}/dispute (06's API surface); with
   no handler the points are listed without the control. */

export interface ProvisionalPointsProps {
   points: ReadonlyArray<ProvisionalPoint>;
   onAskForReread?: (gradingId: string) => void;
}

export function ProvisionalPoints({ points, onAskForReread }: ProvisionalPointsProps) {
   const hasPoints = points.length > 0;
   const offersReread = onAskForReread !== undefined;

   return (
      <section aria-labelledby="provisional-heading">
         <h2 id="provisional-heading" className="section-heading">
            Provisional points
         </h2>

         {hasPoints ? null : (
            <p className="muted" data-testid="provisional-empty">
               Nothing is provisional. When a free-response point is graded two ways, it waits here and
               you can ask for it to be re-read.
            </p>
         )}

         {hasPoints ? (
            <ul className="review-list">
               {points.map((point) => {
                  const canAskForReread = offersReread && !point.disputed;

                  return (
                     <li key={point.grading_id} data-testid="provisional-point">
                        <span>
                           {point.label}, {point.point_label}
                        </span>

                        <span className="muted">{point.reason}</span>

                        {point.disputed ? <span className="muted">Re-read asked for</span> : null}

                        {canAskForReread ? (
                           <button type="button" className="text-button" onClick={() => onAskForReread!(point.grading_id)}>
                              Ask for a re-read
                           </button>
                        ) : null}
                     </li>
                  );
               })}
            </ul>
         ) : null}
      </section>
   );
}
