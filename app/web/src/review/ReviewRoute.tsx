import { useState } from "react";

import { ApiError, askForReread, readReview, submitErrorNote } from "../api/client";
import type { ErrorNoteEntry, ReviewPayload } from "../api/types";
import { ReviewScreen } from "./ReviewScreen";
import { useAgentScreen } from "../agent/AgentProvider";
import { useLoad } from "../status/load";
import { Loading } from "../status/LoadState";
import { Page, PageHeader } from "../ui/Page";

/* Review reads GET /review. An edited note goes through the session route that wrote it, which
   replaces the note. Practising what is coming back opens a set, whose first block serves the due
   reviews. */
export interface ReviewRouteProps {
   onStartPractice?: () => void;
}

function saveFailure(problem: unknown) {
   const hasDetail = problem instanceof ApiError && problem.detail !== "";

   return new Error(hasDetail ? problem.detail : "The note was not saved.");
}

export function ReviewRoute(props: ReviewRouteProps) {
   const load = useLoad(readReview);
   const [edited, setEdited] = useState<ReviewPayload | null>(null);

   useAgentScreen({ kind: "review" });

   if (load.kind === "waiting") {
      return <Loading testId="review-waiting" />;
   }

   if (load.kind === "failed") {
      return (
         <Page header={<PageHeader eyebrow="Revisit, refine, retain" title="Review" />}>
            <div className="state state-failed">
               <p data-testid="review-failed" role="alert">
                  The review record could not be loaded.
               </p>

               <button type="button" className="button-secondary" onClick={load.retry}>
                  Try again
               </button>
            </div>
         </Page>
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
         onStartPractice={props.onStartPractice}
      />
   );
}
