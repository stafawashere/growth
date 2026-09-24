import type {
   CheckpointQuestionResult,
   CheckpointsPayload,
   CheckpointView,
   ProbeAdministration,
   ProbePayload
} from "../api/types";
import { formatPlanDate } from "../home/dates";
import { formatFigure } from "./figures";

/* 08 "Information architecture", progress: checkpoint history, the 6-week released-material results
   (11 P7 scope item 7). The checkpoint and the probe are instruments, so this section reports what
   each one measured and whether the next one is available, and never schedules either. */

export const SCORED_BY_STUDENT = "student_self_score";

export const SELF_SCORED_NOTE = "Scored by the student against the published scoring guidelines.";

export interface CheckpointHistoryProps {
   checkpoints: CheckpointsPayload;
   onOpenCheckpoint: () => void;
}

export interface ProbeHistoryProps {
   probe: ProbePayload;
   onOpenProbe: () => void;
}

function publishedMeanText(result: CheckpointQuestionResult) {
   const hasMean = result.published_mean !== null;

   if (!hasMean) {
      return "no published mean for this question";
   }

   const years = result.published_mean_years.join(", ");

   return `against a published mean of ${formatFigure(result.published_mean as number)} from ${years}`;
}

export function CheckpointResult({ checkpoint }: { checkpoint: CheckpointView }) {
   const isSelfScored = checkpoint.scored_by === SCORED_BY_STUDENT;

   return (
      <article data-testid="checkpoint-result">
         <h3 className="label-heading">{checkpoint.form_year} released free-response form</h3>

         <p data-testid="checkpoint-total">
            {checkpoint.total_earned} of {checkpoint.total_possible} points.
         </p>

         <ul>
            {checkpoint.questions.map((result) => (
               <li key={result.question} data-testid="checkpoint-question">
                  Question {result.question}, {result.earned} of {result.possible} points,{" "}
                  {publishedMeanText(result)}.
               </li>
            ))}
         </ul>

         {isSelfScored ? <p className="caption">{SELF_SCORED_NOTE}</p> : null}
      </article>
   );
}

export function CheckpointHistory({ checkpoints, onOpenCheckpoint }: CheckpointHistoryProps) {
   const { availability, history } = checkpoints;
   const isOpen = availability.open_checkpoint_id !== null;
   const canOpen = isOpen || availability.available;
   const hasHistory = history.length > 0;
   const waitsForADay = !canOpen && availability.opens_on !== null;
   const hasNoFormLeft = !canOpen && !waitsForADay;

   return (
      <section aria-labelledby="checkpoint-heading" data-testid="checkpoint-history">
         <h2 id="checkpoint-heading" className="section-heading">
            Checkpoint history
         </h2>

         {hasHistory ? (
            history.map((checkpoint) => <CheckpointResult key={checkpoint.id} checkpoint={checkpoint} />)
         ) : (
            <p className="muted">No checkpoint has been finished yet.</p>
         )}

         {canOpen ? (
            <button type="button" className="text-button" onClick={onOpenCheckpoint}>
               {isOpen ? "Continue the checkpoint" : "Take a checkpoint"}
            </button>
         ) : null}

         {waitsForADay ? (
            <p className="muted" data-testid="checkpoint-opens-on">
               The next checkpoint opens on {formatPlanDate(availability.opens_on as string)}.
            </p>
         ) : null}

         {hasNoFormLeft ? (
            <p className="muted">Every released form in the library has been used.</p>
         ) : null}
      </section>
   );
}

function ProbeResult({ administration }: { administration: ProbeAdministration }) {
   const hasGraded = administration.graded > 0;

   return (
      <li data-testid="probe-result">
         {hasGraded
            ? `${administration.correct} of ${administration.graded} graded items correct.`
            : "No item of this probe could be graded."}
      </li>
   );
}

export function ProbeHistory({ probe, onOpenProbe }: ProbeHistoryProps) {
   const { availability, history } = probe;
   const isOpen = availability.open_administration_id !== null;
   const canOpen = isOpen || availability.available;
   const hasHistory = history.length > 0;
   const waitsForADay = !canOpen && availability.opens_on !== null;
   const hasNoItems = !canOpen && !waitsForADay;

   return (
      <section aria-labelledby="probe-heading" data-testid="probe-history">
         <h2 id="probe-heading" className="section-heading">
            Concept probe
         </h2>

         {hasHistory ? (
            <ul>
               {history.map((administration) => (
                  <ProbeResult key={administration.id} administration={administration} />
               ))}
            </ul>
         ) : (
            <p className="muted">No concept probe has been finished yet.</p>
         )}

         {canOpen ? (
            <button type="button" className="text-button" onClick={onOpenProbe}>
               {isOpen ? "Continue the concept probe" : "Take the concept probe"}
            </button>
         ) : null}

         {waitsForADay ? (
            <p className="muted" data-testid="probe-opens-on">
               The next concept probe opens on {formatPlanDate(availability.opens_on as string)}.
            </p>
         ) : null}

         {hasNoItems ? <p className="muted">The concept probe has no items yet.</p> : null}
      </section>
   );
}