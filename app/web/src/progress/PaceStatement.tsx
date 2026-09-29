import type { PacePayload } from "../api/types";
import { paceLabel } from "../ui/Countdown";
import { Icon, type IconName } from "../ui/Icon";

/* The pace verdict at the top of progress (app/progress/pace.py). The sentence is the server's, so
   the verdict and its numbers cannot disagree. The figures under it are the ones the verdict rests
   on, each with what it counts, and an unmeasured figure says so instead of showing a zero. */

export interface PaceStatementProps {
   pace: PacePayload;
}

function countOf(count: number, noun: string) {
   return count === 1 ? `1 ${noun}` : `${count} ${noun}s`;
}

function studyTimeText(pace: PacePayload) {
   const time = pace.study_time;
   const hasMinutes = time.minutes_per_active_day !== null;

   if (!hasMinutes) {
      return `not logged on any of the last ${countOf(time.attempts, "attempt")}`;
   }

   return `${Math.round(time.minutes_per_active_day ?? 0)} minutes a practice day, ${time.active_days_per_week} days a week`;
}

function accuracyText(pace: PacePayload) {
   const accuracy = pace.evidence.recent_accuracy;

   if (accuracy.value === null) {
      return `no graded attempts in ${accuracy.days} days`;
   }

   return `${accuracy.correct} of ${accuracy.graded} correct over ${accuracy.days} days`;
}

function retentionText(pace: PacePayload) {
   const retention = pace.evidence.retention_30_day;

   if (retention.value === null) {
      return "not measured yet";
   }

   return `${retention.correct} of ${retention.attempts} held a month after a success`;
}

const VERDICT_ICON: Record<PacePayload["verdict"], IconName> = {
   complete: "check",
   ahead: "check",
   on_pace: "check",
   behind: "alert",
   well_behind: "alert",
   too_early: "clock",
   exam_passed: "clock"
};

const VERDICT_TONE: Record<PacePayload["verdict"], string> = {
   complete: "status-icon text-correct",
   ahead: "status-icon text-correct",
   on_pace: "status-icon text-correct",
   behind: "status-icon text-incorrect",
   well_behind: "status-icon text-incorrect",
   too_early: "status-icon muted",
   exam_passed: "status-icon muted"
};

export function PaceStatement(props: PaceStatementProps) {
   const pace = props.pace;

   return (
      <section aria-labelledby="pace-title" data-testid="pace-statement" data-verdict={pace.verdict} className="card pace">
         <div className="card-header">
            <span className={VERDICT_TONE[pace.verdict]}>
               <Icon name={VERDICT_ICON[pace.verdict]} size="md" />
            </span>

            <h2 id="pace-title">Pace</h2>

            <span className="badge">{paceLabel(pace.verdict)}</span>
         </div>

         <p className="lead" data-testid="pace-sentence">
            {pace.statement}
         </p>

         <dl className="pace-figures">
            <div>
               <dt>Exam</dt>
               <dd>
                  {pace.exam_date}, in {countOf(pace.days_to_exam, "day")}
               </dd>
            </div>

            <div>
               <dt>Skills held</dt>
               <dd>
                  {pace.skills.held} of {pace.skills.total}, with {pace.skills.fading} fading
               </dd>
            </div>

            <div>
               <dt>Mastery rate</dt>
               <dd>
                  {pace.rate.weekly} weighted skills a week, {pace.rate.required_weekly} needed
               </dd>
            </div>

            <div>
               <dt>Study time</dt>
               <dd>{studyTimeText(pace)}</dd>
            </div>

            <div>
               <dt>Recent accuracy</dt>
               <dd>{accuracyText(pace)}</dd>
            </div>

            <div>
               <dt>Retention</dt>
               <dd>{retentionText(pace)}</dd>
            </div>
         </dl>

         <p className="helper">{pace.caveat}</p>
      </section>
   );
}
