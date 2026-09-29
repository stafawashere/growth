import { useRef } from "react";

import type { LessonPlan, LessonRecord } from "../api/types";
import { LessonSection, sectionMode } from "./LessonSection";

/* 15 Re-teaching and UI: a refresher is a short re-read before the next problem, so its sections
   sit in one scrollable panel rather than one per screen, every step already shown, with one way
   out: "Back to the problem". The time on the panel is logged against each section it served in
   equal shares, since a single panel gives no per-section time. */

export interface RefresherPanelProps {
   lesson: LessonRecord;
   plan: LessonPlan;
   topBar: string;
   onComplete: () => void;
   onSectionViewed: (sectionId: string, mode: string, elapsedMs: number) => void;
   now?: () => number;
}

export function RefresherPanel({ lesson, plan, topBar, onComplete, onSectionViewed, now = Date.now }: RefresherPanelProps) {
   const openedAt = useRef(now());
   const served = plan.sections
      .map((ref) => ({ ref, section: lesson.sections.find((section) => section.id === ref.id) }))
      .filter((entry) => entry.section !== undefined);

   function leave() {
      const share = served.length === 0 ? 0 : Math.round(Math.max(0, now() - openedAt.current) / served.length);

      for (const entry of served) {
         onSectionViewed(entry.section!.id, sectionMode(entry.section!), share);
      }

      onComplete();
   }

   return (
      <section className="card lesson-reader" data-testid="lesson-reader" data-context="refresher">
         <p className="eyebrow" data-testid="lesson-top-bar">
            {topBar}
         </p>

         <div className="lesson-refresher" data-testid="refresher-panel" tabIndex={0} aria-label="Refresher">
            {served.map((entry) => (
               <LessonSection key={entry.ref.id} section={entry.section!} form={entry.ref.form} revealAll />
            ))}
         </div>

         <div className="action-row">
            <button type="button" className="button-primary" data-testid="refresher-back" onClick={leave}>
               Back to the problem
            </button>
         </div>
      </section>
   );
}
