import { useEffect, useId, useState } from "react";

import { deleteEveryPhoto, readStudyPlan, updateStudyPlan } from "../api/client";
import { ActionFailed } from "../status/LoadState";
import { Dialog } from "../ui/Dialog";

/* 01, "Implementation intention and queue-bound streak": at setup the student writes one if-then
   plan naming a fixed time and place. It is the student's own sentence, kept on the server and
   shown back here, where it can be rewritten. */
export const STUDY_PLAN_LABEL = "My if-then plan";

export const STUDY_PLAN_HINT = "Name a fixed time and place, such as: after breakfast, I work at my desk.";

export function StudyPlanSection() {
   const [saved, setSaved] = useState<string | null>(null);
   const [draft, setDraft] = useState("");
   const [loaded, setLoaded] = useState(false);
   const [working, setWorking] = useState(false);
   const [failed, setFailed] = useState(false);
   const [done, setDone] = useState(false);
   const fieldId = useId();
   const hintId = useId();

   useEffect(() => {
      let isCurrent = true;

      Promise.resolve()
         .then(() => readStudyPlan())
         .then((payload) => {
            if (isCurrent && payload !== undefined) {
               setSaved(payload.study_plan);
               setDraft(payload.study_plan ?? "");
               setLoaded(true);
            }
         })
         .catch(() => undefined);

      return () => {
         isCurrent = false;
      };
   }, []);

   const isChanged = draft.trim() !== (saved ?? "");
   const canSave = loaded && isChanged && !working;

   async function save() {
      setWorking(true);
      setFailed(false);
      setDone(false);

      try {
         const payload = await updateStudyPlan(draft);

         setSaved(payload.study_plan);
         setDraft(payload.study_plan ?? "");
         setDone(true);
      } catch {
         setFailed(true);
      } finally {
         setWorking(false);
      }
   }

   return (
      <section className="section" data-testid="study-plan-settings">
         <h2 className="section-header">Study plan</h2>

         <div className="form-field">
            <label className="field-label" htmlFor={fieldId}>
               {STUDY_PLAN_LABEL}
            </label>

            <textarea
               id={fieldId}
               className="input"
               aria-describedby={hintId}
               value={draft}
               disabled={!loaded}
               onChange={(event) => {
                  setDraft(event.target.value);
                  setDone(false);
               }}
            />

            <p className="field-hint" id={hintId}>
               {STUDY_PLAN_HINT}
            </p>
         </div>

         {failed ? <ActionFailed /> : null}

         <div className="cluster">
            <button type="button" className="button-secondary" disabled={!canSave} data-outcome={done ? "done" : undefined} onClick={save}>
               Save my plan
            </button>

            {done ? <span className="helper">Saved.</span> : null}
         </div>
      </section>
   );
}

export function StartingPointSection(props: { onRunDiagnostic: () => void }) {
   return (
      <section className="section">
         <h2 className="section-header">Starting point</h2>

         <div className="list list-flush">
            <div className="list-row">
               <div className="list-row-body">
                  <span className="list-row-title">Run the placement again</span>
                  <span className="list-row-meta">A short re-diagnostic that updates what the app knows about you and never resets it.</span>
               </div>

               <div className="list-row-trail">
                  <button type="button" className="button-secondary button-small" onClick={props.onRunDiagnostic}>
                     Run a diagnostic
                  </button>
               </div>
            </div>
         </div>
      </section>
   );
}

/* 08's settings wireframe, Data: "Delete my FRQ photos". Every stored page photo goes at once,
   after a confirmation, and the count the server removed is said back. */
export function DeletePhotosSection() {
   const [confirming, setConfirming] = useState(false);
   const [working, setWorking] = useState(false);
   const [failed, setFailed] = useState(false);
   const [removed, setRemoved] = useState<number | null>(null);

   async function remove() {
      setWorking(true);
      setFailed(false);

      try {
         const payload = await deleteEveryPhoto();

         setRemoved(payload.deleted);
         setConfirming(false);
      } catch {
         setFailed(true);
      } finally {
         setWorking(false);
      }
   }

   return (
      <section className="section" data-testid="delete-photos-settings">
         <h2 className="section-header">Response photos</h2>

         <div className="list list-flush">
            <div className="list-row">
               <div className="list-row-body">
                  <span className="list-row-title">Delete my FRQ photos</span>
                  <span className="list-row-meta">Removes every photographed page. Grades and typed read-backs stay.</span>
               </div>

               <div className="list-row-trail">
                  <button type="button" className="text-button text-button-destructive" onClick={() => setConfirming(true)}>
                     delete
                  </button>
               </div>
            </div>
         </div>

         {removed !== null ? (
            <p className="helper" role="status" data-testid="photos-deleted">
               {removed === 0 ? "There were no photos to delete." : removed === 1 ? "One photo was deleted." : `${removed} photos were deleted.`}
            </p>
         ) : null}

         <Dialog
            open={confirming}
            title="Delete every response photo?"
            onClose={() => setConfirming(false)}
            actions={
               <>
                  <button type="button" className="button-secondary" onClick={() => setConfirming(false)}>
                     Keep them
                  </button>
                  <button type="button" className="text-button text-button-destructive" disabled={working} onClick={remove}>
                     Delete the photos
                  </button>
               </>
            }
         >
            <p>Each photographed page is removed from this app. This cannot be undone.</p>

            {failed ? <ActionFailed /> : null}
         </Dialog>
      </section>
   );
}
