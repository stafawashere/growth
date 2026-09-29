import { useEffect, useRef, useState } from "react";

import type {
   LessonBand,
   LessonCheck as LessonCheckRecord,
   LessonCheckAnswerBody,
   LessonCheckVerdict,
   LessonEventMode,
   LessonPlan,
   LessonPromptAnswerBody,
   LessonPromptVerdict,
   LessonRecord,
   LessonSection as LessonSectionRecord,
   LessonSectionType
} from "../api/types";
import { MathValue } from "../math/MathValue";
import { Icon } from "../ui/Icon";
import { PageHeader } from "../ui/Page";
import { ContrastPanel } from "./ContrastPanel";
import { LessonCheck } from "./LessonCheck";
import { sectionIdMatches } from "./LessonLink";
import type { CommittedPrediction } from "./LessonPrompts";
import { LessonSection, sectionMode } from "./LessonSection";
import { LessonText } from "./LessonText";
import { RefresherPanel } from "./RefresherPanel";

/* The lesson reader of docs/plan/15-lessons.md UI and the framework contract. One section per
   screen in the plan's order, the checks where the plan puts them (and any plan check not already
   placed after the sections), then a defined end: 08 bans infinite scroll. "Next part" moves on;
   "Skip to the problem" in a session, or "Back to progress" in the library, is on every screen but
   the last and leaves with the index of the screen it leaves. Each screen reports its view as it
   leaves, with its delivery mode (amendment A-D5). A plan whose reason is T1 to T5 is a refresher
   and is read in one panel instead. SessionScreen wires this for the session (worker C); the
   library reader is LessonRoute.

   The v2 screens: a prediction's Commit comes before "Next part"; the first core key idea opens
   with what was predicted and its resolution; a worked example with steps still hidden offers
   "Show all steps" in place of "Next part". Prompt answers go through onPromptAnswer. */

export type LessonContext = "session" | "library";

export interface LessonReaderProps {
   lesson: LessonRecord;
   plan: LessonPlan;
   band: LessonBand;
   context: LessonContext;
   onComplete: () => void;
   onSkip: (sectionIndex: number) => void;
   onSectionViewed: (sectionId: string, mode: LessonEventMode, elapsedMs: number) => void;
   onCheckAnswer: (checkId: string, body: LessonCheckAnswerBody) => Promise<LessonCheckVerdict>;
   /* Grades a prediction, a fix prompt or a faded example. A caller that has none (the feedback
      panel's anchored read) still gets a prediction that commits, and the error blocks and faded
      examples fall back to plain reveals. */
   onPromptAnswer?: (sectionId: string, body: LessonPromptAnswerBody) => Promise<LessonPromptVerdict>;
   conceptName?: string;
   /* The library back and finish label, naming where the reader returns. */
   backLabel?: string;
   /* Told the screen on show each time it changes, for the live tutor's context line. A refresher
      is one panel, so it reports its first section as part 1 of 1. */
   onPositionChange?: (position: LessonPosition) => void;
   now?: () => number;
}

export interface LessonPosition {
   sectionId: string;
   index: number;
   count: number;
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

function screenMode(screen: Exclude<Screen, { kind: "end" }>): LessonEventMode {
   if (screen.kind === "section") {
      return sectionMode(screen.section);
   }

   return screen.kind;
}

/* The pacing line names each part: "Part 3 of 13, Key idea". A reader's scoring lines belong to
   the example before them. */
export const PART_NAMES: Record<LessonSectionType, string> = {
   prediction: "Predict",
   orientation: "What a response shows",
   prerequisite_bridge: "From earlier",
   key_ideas: "Key idea",
   strategy: "Recognise",
   worked_example: "Example",
   what_a_reader_scores: "Example",
   common_error: "Trap",
   representations: "Reading the representation"
};

export function partName(screen: Screen) {
   if (screen.kind === "section") {
      const isFaded = screen.section.type === "worked_example" && screen.section.fade_from !== undefined;

      return isFaded ? "Faded example" : PART_NAMES[screen.section.type] ?? "Part";
   }

   const names = { check: "Check", contrast: "Recognise", end: "End" };

   return names[screen.kind];
}

function PredictionLine({ committed }: { committed: CommittedPrediction }) {
   const predicted = committed.optionLabel !== null ? <LessonText text={committed.optionLabel} /> : <MathValue value={committed.value} />;

   return (
      <p data-testid="lesson-prediction-resolution">
         You predicted {predicted}.{committed.resolution !== null ? " " : null}
         {committed.resolution !== null ? <LessonText text={committed.resolution} /> : null}
      </p>
   );
}

export function LessonReader(props: LessonReaderProps) {
   const { lesson, plan, context, onComplete, onSkip, onSectionViewed, onCheckAnswer, onPromptAnswer, now = Date.now } = props;
   const conceptName = props.conceptName ?? UNNAMED_CONCEPT;
   const backLabel = props.backLabel ?? "Back to progress";
   const screens = screensFor(lesson, plan);
   const [index, setIndex] = useState(0);
   const [returnTo, setReturnTo] = useState<number | null>(null);
   const [inlineAnchor, setInlineAnchor] = useState<string | null>(null);
   const [committed, setCommitted] = useState<CommittedPrediction | null>(null);
   const [stepsRemain, setStepsRemain] = useState(false);
   const [showAllSteps, setShowAllSteps] = useState(false);
   const enteredAt = useRef(now());
   const isRefresher = REFRESHER_REASONS.includes(plan.reason);
   const shownIndex = Math.min(index, screens.length - 1);
   const positionSectionId = isRefresher ? plan.sections[0]?.id ?? lesson.id : screens[shownIndex].id;
   const positionIndex = isRefresher ? 0 : shownIndex;
   const positionCount = isRefresher ? 1 : screens.length;
   const onPositionChange = props.onPositionChange;

   useEffect(() => {
      onPositionChange?.({ sectionId: positionSectionId, index: positionIndex, count: positionCount });
   }, [onPositionChange, positionSectionId, positionIndex, positionCount]);

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
      setStepsRemain(false);
      setShowAllSteps(false);
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

   const partNumber = Math.min(index + 1, screens.length);
   const isSectionScreen = current.kind === "section";
   const currentType = current.kind === "section" ? current.section.type : null;
   const isExample = currentType === "worked_example";
   const offersShowAll = isExample && stepsRemain;
   const awaitsCommit = currentType === "prediction" && committed === null;
   const firstCoreKeyIdea = screens.find((screen) => screen.kind === "section" && screen.section.type === "key_ideas" && screen.section.depth !== "extended");
   const isFirstCoreKeyIdea = isSectionScreen && firstCoreKeyIdea !== undefined && firstCoreKeyIdea.id === current.id;
   const lead = isFirstCoreKeyIdea && committed !== null ? <PredictionLine committed={committed} /> : null;

   return (
      <section className="lesson-reader stack stack-loose" data-testid="lesson-reader" data-context={context}>
         {isSession ? (
            <p className="lead" data-testid="lesson-top-bar">
               {topBar}
            </p>
         ) : (
            <PageHeader eyebrow="Lesson" title={<span data-testid="lesson-top-bar">{topBar}</span>} />
         )}

         <div className="stack stack-tight">
            <p className="helper">
               <span data-testid="lesson-part">
                  Part {partNumber} of {screens.length}
               </span>
               , <span data-testid="lesson-part-name">{partName(current)}</span>
            </p>

            <div className="progress-steps" aria-hidden="true">
               {screens.map((screen, position) => (
                  <span key={`${screen.id}-${position}`} className="progress-step" data-state={position < index ? "done" : position === index ? "current" : "ahead"} />
               ))}
            </div>
         </div>

         <div
            key={`${current.id}-${index}`}
            className="card lesson-screen"
            data-testid="lesson-screen"
            data-screen-kind={current.kind}
            data-section-id={current.kind === "end" ? undefined : current.id}
         >
            {current.kind === "section" ? (
               <LessonSection
                  section={current.section}
                  form={current.form}
                  revealAll={isExample && showAllSteps}
                  lead={lead}
                  prediction={{ committed, onCommit: setCommitted }}
                  onPromptAnswer={onPromptAnswer}
                  onStepsRemaining={setStepsRemain}
                  now={now}
               />
            ) : null}

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

         <div className="submit-row lesson-actions">
            <div className="cluster">
               {returnTo !== null ? (
                  <button type="button" className="text-button" data-testid="lesson-return" onClick={backToCheck}>
                     <Icon name="back" />
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
                     {backLabel}
                  </button>
               ) : null}
            </div>

            {isEnd ? (
               <button type="button" className="button-primary" data-testid="lesson-finish" onClick={finish}>
                  {isSession ? "Go to the problem" : backLabel}
                  <Icon name="next" />
               </button>
            ) : null}

            {/* One button that turns from "Show all steps" into "Next part", so focus stays on it. */}
            {!isEnd ? (
               <button
                  type="button"
                  className="button-primary"
                  data-testid={offersShowAll ? "lesson-show-all-steps" : "lesson-next"}
                  disabled={awaitsCommit}
                  onClick={offersShowAll ? () => setShowAllSteps(true) : next}
               >
                  {offersShowAll ? "Show all steps" : "Next part"}
                  {offersShowAll ? null : <Icon name="next" />}
               </button>
            ) : null}
         </div>
      </section>
   );
}
