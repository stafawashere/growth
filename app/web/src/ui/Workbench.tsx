import type { ReactNode } from "react";

/* The question workbench, direction C of mockup-redesign (chosen 2026-10-01). Every question screen
   sets its question out the same way: the page header names the set and the position, a connected
   bar under it carries one segment per question, and one card is split into a rail of tools, the
   pane that holds the question and the pane that takes the answer, with a status line under the
   card. A screen with no tools has no rail, and a question waiting on nothing from the student, such
   as one already checked, has no answer pane. */

type DataAttributes = { [name: `data-${string}`]: string | undefined };

export interface WorkbenchProps {
   stem: ReactNode;
   work?: ReactNode;
   foot?: ReactNode;
   tools?: ReactNode;
   toolsLabel?: string;
   status?: ReactNode;
   after?: ReactNode;
   testId?: string;
   data?: DataAttributes;
   stemLabel?: string;
   workLabel?: string;
}

export function Workbench(props: WorkbenchProps) {
   const hasTools = props.tools !== undefined && props.tools !== null;
   const hasWork = props.work !== undefined && props.work !== null;
   const hasFoot = props.foot !== undefined && props.foot !== null;
   const hasStatus = props.status !== undefined && props.status !== null;

   return (
      <div className="workbench" data-testid={props.testId} {...props.data}>
         <div className="bench">
            {hasTools ? (
               <div className="bench-rail" role="group" aria-label={props.toolsLabel ?? "Question tools"}>
                  {props.tools}
               </div>
            ) : null}

            <section className="bench-pane bench-stem" aria-label={props.stemLabel ?? "Question"}>
               {props.stem}
            </section>

            {hasWork ? (
               <section className="bench-pane bench-work" aria-label={props.workLabel ?? "Your answer"}>
                  {props.work}

                  {hasFoot ? <div className="bench-foot">{props.foot}</div> : null}
               </section>
            ) : null}
         </div>

         {hasStatus ? <div className="bench-status">{props.status}</div> : null}

         {props.after}
      </div>
   );
}

/* One segment per question, drawn by height so it reads without colour: a hairline still to come, a
   thicker bar answered and the tallest where the student is, with a dot above a question marked for
   review. The segments are read by eye only; the count beside them says the same in words. */

export type TrackState = "current" | "answered" | "open";

export interface TrackMark {
   state: TrackState;
   marked?: boolean;
}

export function trackState(isCurrent: boolean, isAnswered: boolean): TrackState {
   if (isCurrent) {
      return "current";
   }

   return isAnswered ? "answered" : "open";
}

export function QuestionTrack(props: { marks: ReadonlyArray<TrackMark>; count: ReactNode; testId?: string }) {
   return (
      <div className="track" data-testid={props.testId}>
         <ol className="track-marks" aria-hidden="true">
            {props.marks.map((mark, index) => (
               <li key={index} className="track-mark" data-state={mark.state} data-marked={mark.marked === true ? "true" : undefined} />
            ))}
         </ol>

         <p className="track-count">{props.count}</p>
      </div>
   );
}
