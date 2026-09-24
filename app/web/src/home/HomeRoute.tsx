import { useEffect, useState } from "react";
import { readMe, readProgress, type MePayload } from "../api/client";
import type { ProgressPayload } from "../api/types";
import { daysToExam, formatPlanDate } from "./dates";
import { HomeScreen, type HomeScreenStatus, type QueueLine } from "./HomeScreen";

export interface HomeRouteProps {
   today: () => Date;
   onStartSession: () => void;
   onResumeSession: (sessionId: string) => void;
   onOpenProgress?: () => void;
}

type HomeLoad =
   | { kind: "waiting" }
   | { kind: "failed" }
   | { kind: "loaded"; me: MePayload; progress: ProgressPayload };

export function homeStatus(progress: ProgressPayload): HomeScreenStatus {
   const hasSessionInProgress = progress.session_in_progress !== null;

   if (hasSessionInProgress) {
      return "inProgress";
   }

   const countsAreZero =
      progress.skills_due_for_review === 0 &&
      progress.frontier_skills === 0 &&
      progress.corrected_items_returning === 0;
   const forecastIsZero = progress.forecast_minutes === 0;
   const queueIsEmpty = countsAreZero && forecastIsZero;

   return queueIsEmpty ? "empty" : "ready";
}

/* The three lines of the Home wireframe in 08-design-brief.md, in its order and its words. */
export function queueLinesFrom(progress: ProgressPayload): QueueLine[] {
   return [
      { id: "due", label: "skills due for review", count: progress.skills_due_for_review },
      { id: "frontier", label: "skills at your current frontier", count: progress.frontier_skills },
      { id: "corrected", label: "corrected items coming back", count: progress.corrected_items_returning }
   ];
}

export function HomeRoute({ today, onStartSession, onResumeSession, onOpenProgress }: HomeRouteProps) {
   const [load, setLoad] = useState<HomeLoad>({ kind: "waiting" });

   useEffect(() => {
      let isCurrent = true;

      Promise.all([readMe(), readProgress()]).then(
         ([me, progress]) => {
            if (isCurrent) {
               setLoad({ kind: "loaded", me, progress });
            }
         },
         () => {
            if (isCurrent) {
               setLoad({ kind: "failed" });
            }
         }
      );

      return () => {
         isCurrent = false;
      };
   }, []);

   if (load.kind === "waiting") {
      return <section aria-busy="true" data-testid="home-waiting" />;
   }

   if (load.kind === "failed") {
      return <section data-testid="home-failed" />;
   }

   const { me, progress } = load;
   const openSessionId = progress.session_in_progress;

   function resume() {
      const canResume = openSessionId !== null;

      if (canResume) {
         onResumeSession(openSessionId);
      }
   }

   return (
      <HomeScreen
         status={homeStatus(progress)}
         examDate={formatPlanDate(me.exam_date)}
         daysToExam={daysToExam(me.exam_date, today())}
         queueMinutes={Math.ceil(progress.forecast_minutes)}
         queueLines={queueLinesFrom(progress)}
         onStartSession={onStartSession}
         onAddPracticeSet={onStartSession}
         onResumeSession={resume}
         onOpenProgress={onOpenProgress}
      />
   );
}