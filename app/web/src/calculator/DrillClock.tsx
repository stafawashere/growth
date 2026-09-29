import { useEffect, useState } from "react";

import { CLOCK_LABEL, HIDE_CLOCK, SHOW_CLOCK } from "./words";

/* docs/calculator/design.md, The drills: a clock from the moment the task appears, in minutes and
   seconds, in the corner the timed drill keeps its timer. Hiding it stays chosen across drills in
   this browser, and hidden or shown the time is recorded all the same. It changes its text once a
   second and never says whether the time was good. */

export const CLOCK_STORAGE_KEY = "growth-calculator-clock";

const HIDDEN = "hidden";

const SHOWN = "shown";

const TICK_MS = 1000;

export function readClockHidden() {
   try {
      return window.localStorage.getItem(CLOCK_STORAGE_KEY) === HIDDEN;
   } catch {
      return false;
   }
}

function saveClockHidden(isHidden: boolean) {
   try {
      window.localStorage.setItem(CLOCK_STORAGE_KEY, isHidden ? HIDDEN : SHOWN);
   } catch {
      return;
   }
}

export function elapsedClockText(milliseconds: number) {
   const totalSeconds = Math.max(0, Math.floor(milliseconds / 1000));
   const minutes = Math.floor(totalSeconds / 60);
   const seconds = String(totalSeconds % 60).padStart(2, "0");

   return `${minutes}:${seconds}`;
}

export interface DrillClockProps {
   startedAt: number;
   stoppedAt: number | null;
   now: () => number;
}

export function DrillClock(props: DrillClockProps) {
   const { startedAt, stoppedAt, now } = props;
   const [isHidden, setIsHidden] = useState(readClockHidden);
   const [reading, setReading] = useState(() => now());
   const isRunning = stoppedAt === null;
   const shownUntil = stoppedAt ?? reading;

   useEffect(() => {
      if (!isRunning) {
         return undefined;
      }

      setReading(now());

      const timer = window.setInterval(() => setReading(now()), TICK_MS);

      return () => window.clearInterval(timer);
   }, [isRunning, startedAt, now]);

   function toggle() {
      const next = !isHidden;

      setIsHidden(next);
      saveClockHidden(next);
   }

   return (
      <div className="part-timer drill-clock" data-testid="drill-clock">
         {isHidden ? null : (
            <p className="part-clock">
               <span className="visually-hidden">{CLOCK_LABEL} </span>
               <span data-testid="drill-clock-time">{elapsedClockText(shownUntil - startedAt)}</span>
            </p>
         )}

         <button type="button" className="text-button" onClick={toggle}>
            {isHidden ? SHOW_CLOCK : HIDE_CLOCK}
         </button>
      </div>
   );
}
