import { useState } from "react";

import { ApiError, askForReread, readReview, submitErrorNote } from "../api/client";
import type { ErrorNoteEntry, ReviewPayload } from "../api/types";
import { ReviewScreen } from "./ReviewScreen";
import { useLoad } from "../status/load";
import { Loading } from "../status/LoadState";
import { PageHeader } from "../page/PageHeader";

/* Review takes no input from the shell: it is reached from home and reads GET /review. An edited
   note goes through the session route that wrote it, which replaces the note. */
export interface ReviewRouteProps {}

function saveFailure(problem: unknown) {
   const hasDetail = problem instanceof ApiError && problem.detail !== "";

   return new Error(hasDetail ? problem.detail : "The note was not saved.");
}

export function ReviewRoute(_props: ReviewRouteProps) {
   const load = useLoad(readReview);
   const [edited, setEdited] = useState<ReviewPayload | null>(null);

   if (load.kind === "waiting") {
      return <Loading testId="review-waiting" />;
   }

   if (load.kind === "failed") {
      return (
         <section className="card">
            <PageHeader title="Review" />

            <p data-testid="review-failed" className="muted">
               The review record could not be loaded.
            </p>
         </section>
      );
   }

   const review = edited ?? load.value;

   async function saveNote(entry: ErrorNoteEntry, note: string) {
      try {
         const saved = await submitErrorNote(entry.session_id, entry.attempt_id, note);
         const replaced = review.error_notes.map((current) =>
            current.attempt_id === entry.attempt_id ? { ...current, note: saved.error_note ?? note } : current
         );

         setEdited({ ...review, error_notes: replaced });
      } catch (problem) {
         throw saveFailure(problem);
      }
   }

   async function reread(gradingId: string) {
      await askForReread(gradingId);

      const marked = review.provisional_points.map((point) =>
         point.grading_id === gradingId ? { ...point, disputed: true } : point
      );

      setEdited({ ...review, provisional_points: marked });
   }

   return (
      <ReviewScreen
         comingBack={review.coming_back}
         errorNotes={review.error_notes}
         provisionalPoints={review.provisional_points}
         onSaveNote={saveNote}
         onAskForReread={review.grading_available ? reread : undefined}
      />
   );
}
