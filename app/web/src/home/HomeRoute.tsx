import { useEffect, useState } from "react";
import { readMe, readProgress, type MePayload } from "../api/client";
import type { ProgressPayload } from "../api/types";
import type { OnboardingReason } from "../onboarding/OnboardingScreen";
import { daysToExam, formatPlanDate } from "./dates";
import { HomeScreen, type HomeScreenStatus, type QueueLine } from "./HomeScreen";

export interface HomeRouteProps {
   today: () => Date;
   onStartSession: () => void;
   onResumeSession: (sessionId: string) => void;
   onOpenProgress?: () => void;
   onOpenReview?: () => void;
   onStartOnboarding?: (reason: OnboardingReason, resumeSessionId: string | null) => void;
}

type HomeLoad =
   | { kind: "waiting" }
   | { kind: "failed" }
   | { kind: "loaded"; me: MePayload; progress: ProgressPayload };

/* 08 home: a first login runs the onboarding diagnostic before any queue exists, and an unfinished
   diagnostic is resumed wherever the student left it, so home itself is never shown for either. */
export function sendsToOnboarding(progress: ProgressPayload) {
   const isFirstLogin = progress.home_state === "first_login";
   const hasDiagnosticInProgress = progress.diagnostic_in_progress !== null;

   return isFirstLogin || hasDiagnosticInProgress;
}

export function homeStatus(progress: ProgressPayload): HomeScreenStatus {
   const isLongGap = progress.home_state === "long_gap";

   if (isLongGap) {
      return "longGap";
   }

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

export function HomeRoute({
   today,
   onStartSession,
   onResumeSession,
   onOpenProgress,
   onOpenReview,
   onStartOnboarding
}: HomeRouteProps) {
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

   const redirects = load.kind === "loaded" && sendsToOnboarding(load.progress);

   useEffect(() => {
      const canRedirect = redirects && load.kind === "loaded" && onStartOnboarding !== undefined;

      if (!canRedirect) {
         return;
      }

      const { progress } = load;
      const reason = progress.home_state === "long_gap" ? "long_gap" : "first_login";

      onStartOnboarding(reason, progress.diagnostic_in_progress);
   }, [redirects, load, onStartOnboarding]);

   if (load.kind === "waiting") {
      return <section aria-busy="true" data-testid="home-waiting" />;
   }

   if (load.kind === "failed") {
      return <section data-testid="home-failed" />;
   }

   if (redirects) {
      return null;
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
         onStartRediagnostic={() => onStartOnboarding?.("long_gap", null)}
         onOpenProgress={onOpenProgress}
         onOpenReview={onOpenReview}
      />
   );
}