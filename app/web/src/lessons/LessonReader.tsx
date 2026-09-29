import { useRef, useState } from "react";

import type {
   LessonBand,
   LessonCheck as LessonCheckRecord,
   LessonCheckAnswerBody,
   LessonCheckVerdict,
   LessonPlan,
   LessonRecord,
   LessonSection as LessonSectionRecord
} from "../api/types";
import { PageHeader } from "../page/PageHeader";
import { ContrastPanel } from "./ContrastPanel";
import { LessonCheck } from "./LessonCheck";
import { sectionIdMatches } from "./LessonLink";
import { LessonSection, sectionMode } from "./LessonSection";
import { RefresherPanel } from "./RefresherPanel";

/* The lesson reader of docs/plan/15-lessons.md UI and the framework contract. One section per
   screen in the plan's order, the checks where the plan puts them (and any plan check not already
   placed after the sections), then a defined end: 08 bans infinite scroll. "Next part" moves on;
   "Skip to the problem" in a session, or "Back to progress" in the library, is on every screen but
   the last and leaves with the index of the screen it leaves. Each screen reports its view as it
   leaves, with its delivery mode (amendment A-D5). A plan whose reason is T1 to T5 is a refresher
   and is read in one panel instead. SessionScreen wires this for the session (worker C); the
   library reader is LessonRoute. */

export type LessonContext = "session" | "library";

export interface LessonReaderProps {
   lesson: LessonRecord;
   plan: LessonPlan;
   band: LessonBand;
   context: LessonContext;
   onComplete: () => void;
   onSkip: (sectionIndex: number) => void;
   onSectionViewed: (sectionId: string, mode: string, elapsedMs: number) => void;
   onCheckAnswer: (checkId: string, body: LessonCheckAnswerBody) => Promise<LessonCheckVerdict>;
   conceptName?: string;
   now?: () => number;
}

export const REFRESHER_REASONS = ["T1", "T2", "T3", "T4", "T5"];

export const END_OF_SESSION_LESSON = "The first problem is next. It shows a full worked solution you complete.";

export const END_OF_LIBRARY_LESSON = "That is the end of this lesson.";

/* The concept's name reaches the reader from the library listing or the session entry; when a
   caller has none, the copy still reads as a sentence. */
const UNNAMED_CONCEPT = "this concept";

type Screen =
   | { kind: "section"; id: string; section: LessonSectionRecord; form: "full" | "steps_only" }
   | { kind: "check"; id: string; check: LessonCheckRecord }
   | { kind: "contrast"; id: string }
   | { kind: "end"; id: string };

export function minutesPhrase(minutes: number) {
   const whole = Math.max(1, Math.round(minutes));

   return whole === 1 ? "About 1 minute." : `About ${whole} minutes.`;
}

export function topBarFor(context: LessonContext | "refresher", conceptName: string, minutes: number) {
   if (context === "refresher") {
      return `Before the next problem on ${conceptName}. About a minute.`;
   }

   if (context === "library") {
      return conceptName;
   }

   return `Before the first problem on ${conceptName}. ${minutesPhrase(minutes)}`;
}

/* Only a decision lesson serves stems (plan 15 Decision lessons). Its stems are served on one contrast screen after the strategy blocks, where
   the reader has just met the cues the stems test (plan 15 Decision lessons); a lesson without a
   strategy block shows them after its first screen. */
export function screensFor(lesson: LessonRecord, plan: LessonPlan): Screen[] {
   const screens: Screen[] = [];
   const placedChecks = new Set<string>();

   for (const ref of plan.sections) {
      if (ref.type === "check") {
         const check = lesson.checks.find((entry) => entry.id === ref.id);

         if (check !== undefined) {
            screens.push({ kind: "check", id: check.id, check });
            placedChecks.add(check.id);
         }

         continue;
      }

      const section = lesson.sections.find((entry) => entry.id === ref.id);

      if (section !== undefined) {
         screens.push({ kind: "section", id: section.id, section, form: ref.form });
      }
   }

   for (const checkId of plan.checks) {
      const check = lesson.checks.find((entry) => entry.id === checkId);

      if (check !== undefined && !placedChecks.has(checkId)) {
         screens.push({ kind: "check", id: check.id, check });
      }
   }

   const hasStems = lesson.kind === "decision" && lesson.decision !== undefined && lesson.decision.stems.length >= 2;

   if (hasStems) {
      const lastStrategy = screens.map((entry) => entry.kind === "section" && entry.section.type === "strategy").lastIndexOf(true);
      const position = lastStrategy === -1 ? Math.min(1, screens.length) : lastStrategy + 1;

      screens.splice(position, 0, { kind: "contrast", id: `${lesson.id}#stems` });
   }

   screens.push({ kind: "end", id: `${lesson.id}#end` });

   return screens;
}

function screenMode(screen: Screen) {
   if (screen.kind === "section") {
      return sectionMode(screen.section);
   }

   return screen.kind;
}

export function LessonReader(props: LessonReaderProps) {
   const { lesson, plan, context, onComplete, onSkip, onSectionViewed, onCheckAnswer, now = Date.now } = props;
   const conceptName = props.conceptName ?? UNNAMED_CONCEPT;
   const screens = screensFor(lesson, plan);
   const [index, setIndex] = useState(0);
   const [returnTo, setReturnTo] = useState<number | null>(null);
   const [inlineAnchor, setInlineAnchor] = useState<string | null>(null);
   const enteredAt = useRef(now());
   const isRefresher = REFRESHER_REASONS.includes(plan.reason);

   if (isRefresher) {
      return (
         <RefresherPanel
            lesson={lesson}
            plan={plan}
            topBar={topBarFor("refresher", conceptName, plan.minutes)}
            onComplete={onComplete}
            onSectionViewed={onSectionViewed}
            now={now}
         />
      );
   }

   const current = screens[Math.min(index, screens.length - 1)];
   const isEnd = current.kind === "end";
   const isSession = context === "session";

   function reportLeaving() {
      if (current.kind !== "end") {
         onSectionViewed(current.id, screenMode(current), Math.max(0, now() - enteredAt.current));
      }

      enteredAt.current = now();
   }

   function go(next: number) {
      reportLeaving();
      setInlineAnchor(null);
      setIndex(next);
   }

   function next() {
      setReturnTo(null);
      go(index + 1);
   }

   function skip() {
      reportLeaving();
      onSkip(index);
   }

   function finish() {
      onComplete();
   }

   /* A check's error link goes to that error's screen when the plan serves it, with a way back to
      the check; an error block the plan left out opens below the check instead. */
   function openAnchor(anchor: string) {
      const target = screens.findIndex((screen) => screen.kind === "section" && sectionIdMatches(screen.id, anchor));

      if (target !== -1) {
         setReturnTo(index);
         go(target);

         return;
      }

      setInlineAnchor(anchor);
   }

   function backToCheck() {
      const target = returnTo;

      setReturnTo(null);

      if (target !== null) {
         go(target);
      }
   }

   const inlineSection = inlineAnchor === null ? undefined : lesson.sections.find((section) => sectionIdMatches(section.id, inlineAnchor));
   const topBar = topBarFor(context, conceptName, plan.minutes);

   return (
      <section className="card lesson-reader" data-testid="lesson-reader" data-context={context}>
         {isSession ? (
            <p className="eyebrow" data-testid="lesson-top-bar">
               {topBar}
            </p>
         ) : (
            <PageHeader title={<span data-testid="lesson-top-bar">{topBar}</span>} />
         )}

         <p className="caption" data-testid="lesson-part">
            Part {Math.min(index + 1, screens.length)} of {screens.length}
         </p>

         <div
            key={`${current.id}-${index}`}
            className="lesson-screen"
            data-testid="lesson-screen"
            data-screen-kind={current.kind}
            data-section-id={current.kind === "end" ? undefined : current.id}
         >
            {current.kind === "section" ? <LessonSection section={current.section} form={current.form} /> : null}

            {current.kind === "contrast" && lesson.decision !== undefined ? (
               <ContrastPanel decision={lesson.decision} delivery={lesson.decision.delivery} />
            ) : null}

            {current.kind === "check" ? (
               <>
                  <h2 className="section-heading">Check</h2>
                  <LessonCheck check={current.check} sections={lesson.sections} onCheckAnswer={onCheckAnswer} onOpenAnchor={openAnchor} now={now} />
                  {inlineSection !== undefined ? (
                     <div className="lesson-inline" data-testid="lesson-inline-section" data-section-id={inlineSection.id}>
                        <LessonSection section={inlineSection} revealAll />
                     </div>
                  ) : null}
               </>
            ) : null}

            {current.kind === "end" ? <p data-testid="lesson-end">{isSession ? END_OF_SESSION_LESSON : END_OF_LIBRARY_LESSON}</p> : null}
         </div>

         <div className="action-row lesson-actions">
            {isEnd ? (
               <button type="button" className="button-primary" data-testid="lesson-finish" onClick={finish}>
                  {isSession ? "Go to the problem" : "Back to progress"}
               </button>
            ) : (
               <button type="button" className="button-primary" data-testid="lesson-next" onClick={next}>
                  Next part
               </button>
            )}

            {returnTo !== null ? (
               <button type="button" className="text-button" data-testid="lesson-return" onClick={backToCheck}>
                  Back to the check
               </button>
            ) : null}

            {!isEnd && isSession ? (
               <button type="button" className="text-button" data-testid="lesson-skip" onClick={skip}>
                  Skip to the problem
               </button>
            ) : null}

            {!isEnd && !isSession ? (
               <button type="button" className="text-button" data-testid="lesson-back" onClick={skip}>
                  Back to progress
               </button>
            ) : null}
         </div>
      </section>
   );
}
