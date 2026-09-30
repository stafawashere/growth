import { useEffect, useState } from "react";

import { readMe, readPace, readProgress, type MePayload } from "../api/client";
import type { PacePayload, ProgressPayload } from "../api/types";
import type { OnboardingReason } from "../onboarding/OnboardingScreen";
import { daysToExam, formatPlanDate } from "./dates";
import { HomeScreen, type HomeScreenStatus, type QueueLine } from "./HomeScreen";
import { useAgentScreen } from "../agent/AgentProvider";
import { useLoad } from "../status/load";
import { LoadFailed, Loading } from "../status/LoadState";

export interface HomeRouteProps {
   today: () => Date;
   onStartSession: () => void;
   onResumeSession: (sessionId: string) => void;
   onStartOnboarding?: (reason: OnboardingReason, resumeSessionId: string | null) => void;
}

function isPacePayload(value: unknown): value is PacePayload {
   const isObject = typeof value === "object" && value !== null;

   return isObject && typeof (value as PacePayload).verdict === "string" && typeof (value as PacePayload).statement === "string";
}

/* The pace verdict rides on the countdown. It is read on its own so home never waits for it or
   fails with it: a verdict that cannot be read leaves the countdown without its mark. */
function usePace() {
   const [pace, setPace] = useState<PacePayload | null>(null);

   useEffect(() => {
      let isCurrent = true;

      Promise.resolve()
         .then(() => readPace())
         .then((payload) => {
            if (isCurrent && isPacePayload(payload)) {
               setPace(payload);
            }
         })
         .catch(() => undefined);

      return () => {
         isCurrent = false;
      };
   }, []);

   return pace;
}

async function readHome(): Promise<{ me: MePayload; progress: ProgressPayload }> {
   const [me, progress] = await Promise.all([readMe(), readProgress()]);

   return { me, progress };
}

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

export function HomeRoute({ today, onStartSession, onResumeSession, onStartOnboarding }: HomeRouteProps) {
   const load = useLoad(readHome);
   const pace = usePace();
   const redirects = load.kind === "loaded" && sendsToOnboarding(load.value.progress);

   useAgentScreen({ kind: "today" });

   useEffect(() => {
      const canRedirect = redirects && load.kind === "loaded" && onStartOnboarding !== undefined;

      if (!canRedirect) {
         return;
      }

      const { progress } = load.value;
      const reason = progress.home_state === "long_gap" ? "long_gap" : "first_login";

      onStartOnboarding(reason, progress.diagnostic_in_progress);
   }, [redirects, load, onStartOnboarding]);

   if (load.kind === "waiting") {
      return <Loading testId="home-waiting" />;
   }

   if (load.kind === "failed") {
      return <LoadFailed testId="home-failed" onRetry={load.retry} />;
   }

   if (redirects) {
      return null;
   }

   const { me, progress } = load.value;
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
         focus={progress.focus ?? []}
         skillsDueForReview={progress.skills_due_for_review}
         dueTodaySkills={progress.due_today_skills}
         dueTodayMinutes={progress.due_today_minutes}
         pace={pace === null ? null : { verdict: pace.verdict, statement: pace.statement }}
         onStartSession={onStartSession}
         onAddPracticeSet={onStartSession}
         onResumeSession={resume}
         onStartRediagnostic={() => onStartOnboarding?.("long_gap", null)}
      />
   );
}