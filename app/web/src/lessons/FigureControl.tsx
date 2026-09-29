import { useState, type KeyboardEvent } from "react";

import type { LessonSpec } from "../api/types";
import { LessonText } from "./LessonText";
import { LessonFigure } from "./LessonFigure";
import { buildGraph, formatNumber, isPanelKind, isRecord, panelsOf, type SpecRecord, type Substitution } from "./specGraph";

/* Mode interactive (TEMPLATE.md Delivery; amendments A-D2 and A-D4): exactly one control per
   screen, a slider, a stepper or a draggable point, operated with the arrow keys (Home and End go
   to the ends), with the reading the spec's question names shown above it and a readout that
   updates as the control moves. The figure re-renders with the control's value substituted. */

export interface ControlModel {
   name: string;
   label: string;
   min: number;
   max: number;
   step: number;
   start: number;
   values: number[] | null;
   onCurve: boolean;
   fixed: Record<string, number>;
   drives: string;
}

function pair(value: unknown): [number, number] | null {
   const isPair = Array.isArray(value) && value.length === 2 && value.every((entry) => typeof entry === "number");

   return isPair ? (value as [number, number]) : null;
}

/* The control's variable: parameter, variable or name, with a descriptive name ("upper limit b",
   "input x") reduced to its last word, the symbol the expressions use. */
function variableName(control: SpecRecord) {
   const raw = [control.parameter, control.variable, control.name].find((value) => typeof value === "string") as string | undefined;

   if (raw === undefined) {
      return "x";
   }

   const words = raw.trim().split(/\s+/);

   return words.length > 1 ? words[words.length - 1] : raw;
}

function labelOf(control: SpecRecord, name: string) {
   const raw = [control.parameter, control.variable].find((value) => typeof value === "string") as string | undefined;

   return raw !== undefined && /\(/.test(raw) ? raw : name;
}

function windowX(spec: SpecRecord): [number, number] | null {
   const box = isRecord(spec.window) ? spec.window : isRecord(spec.axes) ? spec.axes : null;

   return box === null ? null : pair(Object.values(box)[0]);
}

export function controlOf(spec: SpecRecord): ControlModel | null {
   const control = Array.isArray(spec.controls) ? spec.controls[0] : spec.control;

   if (!isRecord(control)) {
      return null;
   }

   const name = variableName(control);
   const values = Array.isArray(control.values) && control.values.every((entry) => typeof entry === "number") ? (control.values as number[]) : null;
   const domainRecord = isRecord(control.domain) ? control.domain : null;
   const bounds =
      pair(control.domain) ??
      pair(control.range) ??
      (domainRecord !== null && typeof domainRecord.min === "number" && typeof domainRecord.max === "number" ? ([domainRecord.min, domainRecord.max] as [number, number]) : null) ??
      (values !== null ? ([Math.min(...values), Math.max(...values)] as [number, number]) : null) ??
      windowX(spec);

   if (bounds === null || !(bounds[0] < bounds[1])) {
      return null;
   }

   const start = pair(control.start);
   const isDraggedPoint = control.type === "draggable_point";
   const movesAlongY = isDraggedPoint && start !== null && control.constrained_to !== "curve";
   const [min, max] = movesAlongY ? (isRecord(spec.window) ? pair(Object.values(spec.window)[1]) ?? bounds : bounds) : bounds;
   const stepSource = [control.step, domainRecord?.step].find((value) => typeof value === "number") as number | undefined;
   const step = stepSource ?? (max - min) / 20;
   const initial = [control.initial, control.start].find((value) => typeof value === "number") as number | undefined;
   const fromPair = start === null ? null : movesAlongY ? start[1] : start[0];
   const first = values !== null ? values[0] : min;
   const startValue = Math.min(Math.max(initial ?? fromPair ?? first, min), max);
   const fixed: Record<string, number> = movesAlongY && start !== null ? { x: start[0] } : {};
   const onCurve = !movesAlongY && (control.constrained_to === "curve" || ["x", "t"].includes(name) || control.type === "draggable_rectangle");

   return {
      name: movesAlongY ? "y" : name,
      label: movesAlongY ? "y" : labelOf(control, name),
      min,
      max,
      step,
      start: startValue,
      values,
      onCurve,
      fixed,
      drives: typeof control.drives === "string" ? control.drives : ""
   };
}

function roundToStep(value: number, model: ControlModel) {
   const steps = Math.round((value - model.min) / model.step);

   return Number((model.min + steps * model.step).toFixed(10));
}

export interface FigureControlProps {
   spec: LessonSpec | undefined;
   fallback?: string;
}

function questionText(spec: SpecRecord | undefined) {
   if (spec === undefined) {
      return null;
   }

   if (typeof spec.question === "string") {
      return spec.question;
   }

   return isRecord(spec.question) && typeof spec.question.text === "string" ? spec.question.text : null;
}

function substitutionFor(model: ControlModel, value: number): Substitution {
   return {
      scope: { ...model.fixed, [model.name]: value },
      cursor: { name: model.name, value, onCurve: model.onCurve },
      drives: model.drives
   };
}

/* The height of the drawn function at the control's value, read from the same figure the student
   sees, for the readout. */
function heightAt(spec: SpecRecord, model: ControlModel, value: number) {
   const target = isPanelKind(String(spec.kind)) ? panelsOf(spec)[0] : spec;

   if (target === undefined || !model.onCurve) {
      return null;
   }

   const graph = buildGraph(target, substitutionFor(model, value));
   const point = graph?.spec.marks.find((mark) => mark.type === "point" && Math.abs(mark.at[0] - value) < 1e-9);

   return point !== undefined && point.type !== "segment" ? point.at[1] : null;
}

export function FigureControl({ spec, fallback }: FigureControlProps) {
   const model = spec === undefined ? null : controlOf(spec);
   const [value, setValue] = useState(model?.start ?? 0);
   const question = questionText(spec);

   if (spec === undefined || model === null) {
      return (
         <div className="figure-control">
            {question !== null ? (
               <p className="lesson-question" data-testid="control-question">
                  <LessonText text={question} />
               </p>
            ) : null}
            <LessonFigure spec={undefined} fallback={fallback} />
         </div>
      );
   }

   const values = model.values;
   const position = values === null ? value : values.indexOf(value);

   function moveTo(next: number) {
      if (values !== null) {
         const index = Math.min(Math.max(Math.round(next), 0), values.length - 1);

         setValue(values[index]);

         return;
      }

      setValue(Math.min(Math.max(roundToStep(next, model!), model!.min), model!.max));
   }

   function onKeyDown(event: KeyboardEvent<HTMLInputElement>) {
      const step = values === null ? model!.step : 1;
      const low = values === null ? model!.min : 0;
      const high = values === null ? model!.max : values.length - 1;
      const targets: Record<string, number> = {
         ArrowRight: position + step,
         ArrowUp: position + step,
         ArrowLeft: position - step,
         ArrowDown: position - step,
         Home: low,
         End: high
      };
      const target = targets[event.key];

      if (target !== undefined) {
         event.preventDefault();
         moveTo(target);
      }
   }

   const height = heightAt(spec, model, value);
   const readout = `${model.label} = ${formatNumber(value)}${height === null ? "" : `, height on the curve ${formatNumber(height)}`}`;

   return (
      <div className="figure-control">
         {question !== null ? (
            <p className="lesson-question" data-testid="control-question">
               <LessonText text={question} />
            </p>
         ) : null}

         <LessonFigure spec={spec} fallback={fallback} substitution={substitutionFor(model, value)} />

         <label className="figure-control-slider">
            <span>{model.label}</span>
            <input
               type="range"
               data-testid="figure-control"
               min={values === null ? model.min : 0}
               max={values === null ? model.max : values.length - 1}
               step={values === null ? model.step : 1}
               value={position}
               aria-valuetext={readout}
               onKeyDown={onKeyDown}
               onChange={(event) => moveTo(Number(event.target.value))}
            />
         </label>

         <p className="caption" data-testid="control-readout" aria-live="polite">
            {readout}
         </p>
      </div>
   );
}
