import { useId, useState } from "react";

import type { PaceVerdict } from "../api/types";
import { Icon, type IconName } from "./Icon";

export interface CountdownPace {
   verdict: PaceVerdict;
   statement: string;
}

const PACE_LABEL: Record<PaceVerdict, string> = {
   complete: "Every skill held",
   ahead: "Ahead of pace",
   on_pace: "On pace",
   behind: "Behind pace",
   well_behind: "Well behind pace",
   too_early: "Too early to call",
   exam_passed: "The exam date has passed"
};

const PACE_ICON: Record<PaceVerdict, IconName> = {
   complete: "check",
   ahead: "check",
   on_pace: "check",
   behind: "alert",
   well_behind: "alert",
   too_early: "clock",
   exam_passed: "clock"
};

const PACE_TONE: Record<PaceVerdict, string> = {
   complete: "text-correct",
   ahead: "text-correct",
   on_pace: "text-correct",
   behind: "text-incorrect",
   well_behind: "text-incorrect",
   too_early: "muted",
   exam_passed: "muted"
};

export function paceLabel(verdict: PaceVerdict) {
   return PACE_LABEL[verdict];
}

/* The days to the exam, with the pace verdict behind a small mark whose tip carries the server's
   own sentence. The tip opens on hover or focus and Escape closes it. */
export function Countdown(props: { days: number; unit: string; label: string; detail: string; pace?: CountdownPace | null; testId?: string }) {
   const tipId = useId();
   const [tipDismissed, setTipDismissed] = useState(false);
   const pace = props.pace ?? null;
   const hasPace = pace !== null;
   const paceText = hasPace ? PACE_LABEL[pace.verdict] : "";

   return (
      <section className="countdown" data-testid={props.testId} aria-label={props.label}>
         <div className="countdown-figure">
            <span className="countdown-number">{props.days}</span>
            <span className="countdown-unit">{props.unit}</span>
         </div>

         <div className="countdown-copy">
            <span className="countdown-title">{props.label}</span>
            <span className="countdown-date">{props.detail}</span>
         </div>

         {hasPace ? (
            <div
               className="countdown-pace"
               data-tip-hidden={tipDismissed ? "true" : undefined}
               onMouseLeave={() => setTipDismissed(false)}
               onBlur={() => setTipDismissed(false)}
            >
               <span
                  className={`countdown-pace-trigger ${PACE_TONE[pace.verdict]}`}
                  tabIndex={0}
                  aria-describedby={tipId}
                  data-testid="countdown-pace"
                  data-verdict={pace.verdict}
                  onKeyDown={(event) => {
                     if (event.key === "Escape") {
                        setTipDismissed(true);
                     }
                  }}
               >
                  <Icon name={PACE_ICON[pace.verdict]} size="md" />
                  <span className="visually-hidden">{paceText}</span>
               </span>

               <span className="countdown-pace-tip" role="tooltip" id={tipId}>
                  <strong>{paceText}</strong>
                  <span>{pace.statement}</span>
               </span>
            </div>
         ) : null}
      </section>
   );
}
