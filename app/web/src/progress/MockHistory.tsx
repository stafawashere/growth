import type { MockHistoryPayload, MockHistoryRow } from "../api/types";
import { formatPlanDate } from "../home/dates";

/* 08 "Information architecture": mock history lives on progress under the checkpoint history,
   because both answer whether the internal numbers mean anything against the criterion. Each
   finished mock is a band and its raw counts. There is no trend line and no single score. */

export interface MockHistoryProps {
   history: MockHistoryPayload;
}

function MockRow({ mock }: { mock: MockHistoryRow }) {
   const takenOn = formatPlanDate(mock.taken_at.slice(0, 10));
   const { band, multiple_choice: multipleChoice, free_response: freeResponse } = mock;

   return (
      <li data-testid="mock-history-row">
         <span>{takenOn}</span>
         <span>
            Band: {band.low} to {band.high}
         </span>
         <span>
            Multiple choice {multipleChoice.correct} of {multipleChoice.total} correct
         </span>
         <span>
            Free response {freeResponse.earned} of {freeResponse.total} points, {freeResponse.pending} pending
         </span>
      </li>
   );
}

export function MockHistory({ history }: MockHistoryProps) {
   const hasHistory = history.mocks.length > 0;

   return (
      <section aria-labelledby="mock-history-heading" data-testid="mock-history">
         <h2 id="mock-history-heading" className="section-heading">
            Mock history
         </h2>

         {hasHistory ? (
            <ul className="review-list">
               {history.mocks.map((mock) => (
                  <MockRow key={mock.session_id} mock={mock} />
               ))}
            </ul>
         ) : (
            <p className="muted">No mock has been finished yet.</p>
         )}
      </section>
   );
}
