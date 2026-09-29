import { useEffect, useRef, useState, type KeyboardEvent } from "react";

import type { LessonSpec } from "../api/types";
import { REDUCED_MOTION_QUERY, motionClass } from "../styles/motion";
import { LessonFallback } from "./LessonFallback";
import { LessonFigure } from "./LessonFigure";
import { LessonTable } from "./LessonTable";
import { formatNumber, isRecord, type SpecRecord } from "./specGraph";
import { numberFrom, type Scope } from "./expression";

/* Mode motion (TEMPLATE.md Delivery; amendment A-D3). A process shown as discrete frames the
   student steps through: Left and Right step, Home and End go to the ends, and Space toggles
   auto-advance. The frame number and its values are announced to assistive technology. Under
   prefers-reduced-motion: reduce the block never advances on its own and each key press
   cross-fades to the next frame (08 Motion rules: replace, do not delete). Auto-advance stops at
   the last frame rather than looping, so the process ends where the lesson's point is. */

export const FRAME_INTERVAL_MS = 1600;

/* motion.css holds every transition the client runs and app.css animates nothing, so the frame
   borrows the step reveal's rule: opacity over the one duration, with the transform neutralised
   under reduced motion. That rule is the cross-fade A-D3 asks for. */
const FRAME_MOTION_CLASS = motionClass("stepVerificationMark");

/* The fade restarts on the next tick, so the new frame arrives at opacity 0 and the stylesheet's
   one motion duration carries it back to full. */
const FADE_RESTART_MS = 20;

export function prefersReducedMotion() {
   try {
      return typeof window.matchMedia === "function" && window.matchMedia(REDUCED_MOTION_QUERY).matches;
   } catch {
      return false;
   }
}

export interface Frame {
   scope: Scope;
   record: SpecRecord;
   row: unknown[] | null;
   readout: string;
}

function readoutOf(record: SpecRecord) {
   return Object.entries(record)
      .filter(([, value]) => typeof value === "number" || typeof value === "string")
      .map(([name, value]) => `${name} = ${typeof value === "number" ? formatNumber(value) : value}`)
      .join(", ");
}

/* Frames come from spec.frames (records, or rows for a table sweep) or from a parameter sweep,
   written parameter {name, values} or parameter {name, frames}. */
export function framesOf(spec: SpecRecord): Frame[] {
   const parameter = isRecord(spec.parameter) ? spec.parameter : null;
   const sweep = parameter === null ? null : parameter.values ?? parameter.frames;
   const name = parameter !== null && typeof parameter.name === "string" ? parameter.name : "t";
   const raw: unknown[] = Array.isArray(spec.frames) ? spec.frames : Array.isArray(sweep) ? sweep.map((value) => ({ [name]: value })) : [];

   return raw.map((entry, index) => {
      if (Array.isArray(entry)) {
         return { scope: {}, record: {}, row: entry, readout: `row ${index + 1}` };
      }

      const record = isRecord(entry) ? entry : {};
      const scope: Scope = {};

      for (const [key, value] of Object.entries(record)) {
         const number = numberFrom(value);

         if (number !== null) {
            scope[key] = number;
         }
      }

      return { scope, record, row: null, readout: readoutOf(record) };
   });
}

export interface FrameStepperProps {
   spec: LessonSpec | undefined;
   fallback?: string;
}

export function FrameStepper({ spec, fallback }: FrameStepperProps) {
   const frames = spec === undefined ? [] : framesOf(spec);
   const [index, setIndex] = useState(0);
   const [isAuto, setIsAuto] = useState(false);
   const [isFading, setIsFading] = useState(false);
   const [reduced] = useState(prefersReducedMotion);
   const fadeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
   const last = frames.length - 1;

   useEffect(() => {
      const advances = isAuto && !reduced;

      if (!advances) {
         return undefined;
      }

      const timer = setInterval(() => setIndex((current) => Math.min(current + 1, last)), FRAME_INTERVAL_MS);

      return () => clearInterval(timer);
   }, [isAuto, reduced, last]);

   useEffect(
      () => () => {
         if (fadeTimer.current !== null) {
            clearTimeout(fadeTimer.current);
         }
      },
      []
   );

   if (spec === undefined || frames.length === 0) {
      return <LessonFallback text={fallback} />;
   }

   function show(next: number) {
      const bounded = Math.min(Math.max(next, 0), last);

      if (bounded === index) {
         return;
      }

      setIndex(bounded);
      setIsFading(true);

      if (fadeTimer.current !== null) {
         clearTimeout(fadeTimer.current);
      }

      fadeTimer.current = setTimeout(() => setIsFading(false), FADE_RESTART_MS);
   }

   function toggleAuto() {
      if (reduced) {
         return;
      }

      setIsAuto((current) => !current);
   }

   function onKeyDown(event: KeyboardEvent<HTMLDivElement>) {
      const steps: Record<string, number> = { ArrowRight: index + 1, ArrowDown: index + 1, ArrowLeft: index - 1, ArrowUp: index - 1, Home: 0, End: last };
      const target = steps[event.key];
      const isOnGroup = event.target === event.currentTarget;

      if (target !== undefined) {
         event.preventDefault();
         show(target);
      } else if (event.key === " " && isOnGroup) {
         event.preventDefault();
         toggleAuto();
      }
   }

   const frame = frames[index];
   const isTableSweep = spec.kind === "table_sweep";
   const sweepRows = frames.slice(0, index + 1).map((entry) => entry.row ?? []);

   return (
      <div
         className="frame-stepper"
         data-testid="frame-stepper"
         role="group"
         aria-roledescription="frames"
         aria-label="Frames: Left and Right arrow keys step, Space starts or stops stepping on its own"
         tabIndex={0}
         onKeyDown={onKeyDown}
      >
         <div
            className={`${FRAME_MOTION_CLASS} lesson-frame${isFading ? " lesson-frame-fading" : ""}`}
            data-testid="frame-view"
            data-frame-index={index}
         >
            {isTableSweep ? (
               <LessonTable spec={{ ...spec, rows: sweepRows }} fallback={fallback} currentRow={index} />
            ) : (
               <LessonFigure spec={spec} fallback={fallback} substitution={{ scope: frame.scope, frame: frame.record, frameIndex: index }} />
            )}
         </div>

         <p className="caption" data-testid="frame-announcement" aria-live="polite">
            Frame {index + 1} of {frames.length}. {frame.readout}
         </p>

         <div className="action-row">
            <button type="button" className="text-button" data-testid="frame-previous" disabled={index === 0} onClick={() => show(index - 1)}>
               Previous frame
            </button>
            <button type="button" className="text-button" data-testid="frame-next" disabled={index === last} onClick={() => show(index + 1)}>
               Next frame
            </button>
            {reduced ? null : (
               <button type="button" className="text-button" data-testid="frame-auto" aria-pressed={isAuto} onClick={toggleAuto}>
                  Step on its own
               </button>
            )}
         </div>
      </div>
   );
}
