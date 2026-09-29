import { useCallback, useEffect, useRef, useState } from "react";

import { answerLessonCheck, answerLessonPrompt, postLessonEvent, readLessonPlan } from "../api/client";
import type { LessonCheckAnswerBody, LessonEventBody, LessonPlanPayload, LessonPromptAnswerBody } from "../api/types";
import { useAgentScreen } from "../agent/AgentProvider";
import { hashFor, type LessonReturn } from "../routing";
import { LoadFailed, Loading } from "../status/LoadState";
import { useLoad } from "../status/load";
import { LessonReader, type LessonPosition } from "./LessonReader";

/* The library reader (15 UI, Library), reached from the Lessons tab or the progress Lessons section,
   never itself on the bar. Any signed-off lesson can be read here whatever the gating, and a library
   read serves the full lesson, so the plan is the low band's first-contact plan (read_again is the
   short refresher subset). Events go
   to the library events route, which writes read with read_source library and no engine state; an
   event that fails to post is not retried and does not hold the student on the page. */

export interface LessonRouteProps {
   lessonId: string;
   conceptName: string;
   onLeave: () => void;
   backLabel?: string;
   /* Where the reader goes back to, sent to the live tutor as its screen's return_to. */
   returnTo?: LessonReturn;
}

const LIBRARY_BAND = "low";

function returnPath(returnTo: LessonReturn | undefined) {
   if (returnTo === undefined) {
      return null;
   }

   const place = returnTo === "lessons" ? ({ view: "lessons" } as const) : ({ view: "progress", tab: "lessons" } as const);

   return hashFor(place).replace(/^#/, "");
}

export function LessonRoute({ lessonId, conceptName, onLeave, backLabel, returnTo }: LessonRouteProps) {
   const read = useCallback(() => readLessonPlan(lessonId, LIBRARY_BAND, "first_contact"), [lessonId]);
   const load = useLoad<LessonPlanPayload>(read);
   const openedAt = useRef(Date.now());
   const openedPosted = useRef(false);
   const [position, setPosition] = useState<LessonPosition | null>(null);
   const lesson = load.kind === "loaded" ? load.value.lesson : null;
   const describesLesson = lesson !== null && position !== null;

   useAgentScreen(
      describesLesson
         ? {
              kind: "lesson",
              lesson_id: lesson.id,
              version: lesson.version,
              section_id: position.sectionId,
              section_index: position.index,
              section_count: position.count,
              return_to: returnPath(returnTo)
           }
         : null,
      { conceptName, posesQuestion: position?.posesQuestion === true }
   );

   const post = useCallback(
      (body: Omit<LessonEventBody, "band">) => postLessonEvent(lessonId, { ...body, band: LIBRARY_BAND }).catch(() => undefined),
      [lessonId]
   );

   useEffect(() => {
      if (load.kind === "loaded" && !openedPosted.current) {
         openedPosted.current = true;
         openedAt.current = Date.now();
         void post({ event: "opened", elapsed_ms: 0 });
      }
   }, [load.kind, post]);

   if (load.kind === "waiting") {
      return <Loading testId="lesson-waiting" />;
   }

   if (load.kind === "failed") {
      return <LoadFailed testId="lesson-failed" onRetry={load.retry} />;
   }

   const elapsed = () => Math.max(0, Date.now() - openedAt.current);

   async function complete() {
      await post({ event: "completed", elapsed_ms: elapsed() });
      onLeave();
   }

   async function skip(sectionIndex: number) {
      const sectionRef = load.kind === "loaded" ? load.value.plan.sections[sectionIndex] : undefined;

      await post({ event: "skipped", section_id: sectionRef?.id, elapsed_ms: elapsed() });
      onLeave();
   }

   return (
      <LessonReader
         lesson={load.value.lesson}
         plan={load.value.plan}
         band={LIBRARY_BAND}
         context="library"
         conceptName={conceptName}
         backLabel={backLabel}
         onPositionChange={setPosition}
         onComplete={complete}
         onSkip={skip}
         onSectionViewed={(sectionId, mode, elapsedMs) => void post({ event: "section_viewed", section_id: sectionId, mode, elapsed_ms: elapsedMs })}
         onCheckAnswer={(checkId, body: LessonCheckAnswerBody) => answerLessonCheck(lessonId, checkId, body)}
         onPromptAnswer={(sectionId, body: LessonPromptAnswerBody) => answerLessonPrompt(lessonId, sectionId, body)}
      />
   );
}
