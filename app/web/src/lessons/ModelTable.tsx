import { useState } from "react";

import type { LessonSpec } from "../api/types";
import { compileExpression, type Compiled } from "./expression";
import { LessonFallback } from "./LessonFallback";
import { LessonFigure } from "./LessonFigure";
import { LessonTable } from "./LessonTable";
import { expressionText, formatNumber, isRecord, type SpecRecord, type Substitution } from "./specGraph";

/* Mode model (TEMPLATE.md Delivery): a deterministic numeric experiment the student runs. The
   table is computed here from spec.function or spec.equation at the spec's h_values, n_values or
   x_values, never typed into the record, and is shown beside the process's own figure with the
   current row highlighted. The keyboard entry of the designs is kept: a Run control adds one row
   per press, so the student meets the sequence one value at a time. */

export interface Model {
   rows: number[][];
   figureFor: (row: number) => LessonSpec | null;
}

const EULER_ROWS = 4;

/* "(s(2 + h) - s(2))/h" calls the spec's function by a one-letter name. Each call is replaced by
   the function's body with its variable replaced by the bracketed argument, so the plain
   expression grammar evaluates it. */
function inlineCalls(computed: string, body: string, variable: string) {
   let result = "";
   let index = 0;

   while (index < computed.length) {
      const call = /^([A-Za-z])\(/.exec(computed.slice(index));
      const isStandalone = index === 0 || !/[A-Za-z0-9_]/.test(computed[index - 1]);

      if (call === null || !isStandalone) {
         result += computed[index];
         index += 1;
         continue;
      }

      let depth = 1;
      let end = index + 2;

      while (end < computed.length && depth > 0) {
         depth += computed[end] === "(" ? 1 : computed[end] === ")" ? -1 : 0;
         end += 1;
      }

      const argument = computed.slice(index + 2, end - 1);

      result += `(${body.replace(new RegExp(`\\b${variable}\\b`, "g"), `(${argument})`)})`;
      index = end;
   }

   return result;
}

function variableOf(body: string) {
   return /\bt\b/.test(body) && !/\bx\b/.test(body) ? "t" : "x";
}

function numbers(value: unknown): number[] | null {
   const isList = Array.isArray(value) && value.length > 0 && value.every((entry) => typeof entry === "number");

   return isList ? (value as number[]) : null;
}

function riemann(f: Compiled, variable: string, interval: [number, number], n: number, sum: string) {
   const width = (interval[1] - interval[0]) / n;
   const offset = sum === "right" ? 1 : sum === "midpoint" || sum === "middle" ? 0.5 : 0;
   let total = 0;

   for (let index = 0; index < n; index += 1) {
      total += f({ [variable]: interval[0] + (index + offset) * width }) * width;
   }

   return total;
}

function isInterval(value: unknown): value is [number, number] {
   return Array.isArray(value) && value.length === 2 && value.every((entry) => typeof entry === "number") && value[0] < value[1];
}

export function computeModel(spec: SpecRecord): Model | null {
   if (typeof spec.equation === "string") {
      const match = /^\s*d\s*([A-Za-z])\s*\/\s*d\s*([A-Za-z])\s*=\s*(.+)$/.exec(spec.equation);
      const field = match === null ? null : compileExpression(match[3]);
      const start = spec.start;
      const step = typeof spec.step === "number" ? spec.step : null;

      if (field === null || match === null || !Array.isArray(start) || step === null) {
         return null;
      }

      const [vertical, horizontal] = [match[1], match[2]];
      const rows: number[][] = [];
      let [x, y] = start as [number, number];

      for (let index = 0; index < EULER_ROWS; index += 1) {
         const slope = field({ [horizontal]: x, [vertical]: y });

         rows.push([x, y, slope].map((value) => Number(value.toFixed(10))));
         y += step * slope;
         x += step;
      }

      const window = { x: [start[0] - step / 2, x], y: [Math.min(...rows.map((row) => row[1])) - 1, Math.max(...rows.map((row) => row[1])) + 1] };

      return {
         rows,
         figureFor: (row) => ({ kind: "euler_steps", equation: spec.equation, start, step, window, frames: rows.map(() => ({})), labels: [] , frameIndex: row })
      };
   }

   if (typeof spec.function !== "string") {
      return null;
   }

   const body = expressionText(spec.function);
   const f = compileExpression(body);

   if (f === null) {
      return null;
   }

   const variable = variableOf(body);
   const hValues = numbers(spec.h_values);
   const nValues = numbers(spec.n_values);
   const xValues = numbers(spec.x_values);

   if (hValues !== null && typeof spec.at === "number") {
      const at = spec.at;
      const computedText = typeof spec.computed === "string" ? inlineCalls(spec.computed, body, variable) : `((${body.replace(new RegExp(`\\b${variable}\\b`, "g"), `(${at} + h)`)}) - (${body.replace(new RegExp(`\\b${variable}\\b`, "g"), `(${at})`)}))/h`;
      const quotient = compileExpression(computedText);

      if (quotient === null) {
         return null;
      }

      const rows = hValues.map((h) => [h, Number(quotient({ h }).toFixed(10))]);
      const reach = Math.max(...hValues);

      return {
         rows,
         figureFor: () => ({
            kind: "graph_sweep",
            curves: [{ expr: body.replace(new RegExp(`\\b${variable}\\b`, "g"), "x"), domain: [at - 1, at + reach + 1] }],
            points: [{ at: [at, f({ [variable]: at })] }],
            secant: {},
            labels: []
         })
      };
   }

   if (nValues !== null && isInterval(spec.interval)) {
      const interval = spec.interval;
      const sum = typeof spec.sum === "string" ? spec.sum : "left";
      const rows = nValues.map((n) => [n, Number(riemann(f, variable, interval, n, sum).toFixed(10))]);

      return {
         rows,
         figureFor: (row) => ({
            kind: "graph",
            curves: [{ expr: body.replace(new RegExp(`\\b${variable}\\b`, "g"), "x"), domain: interval }],
            rectangles: { sum, n: nValues[row] },
            labels: []
         })
      };
   }

   if (xValues !== null) {
      const rows = xValues.map((x) => [x, Number(f({ [variable]: x }).toFixed(10))]);

      return rows.every((row) => Number.isFinite(row[1])) ? { rows, figureFor: () => null } : null;
   }

   return null;
}

/* The figure beside the table follows the current row: the secant at the current h, the
   rectangles at the current n, the Euler steps taken so far. */
function substitutionFor(spec: SpecRecord, model: Model, row: number): Substitution {
   const value = model.rows[row][0];

   if (Array.isArray(spec.h_values)) {
      return { scope: { h: value } };
   }

   return { scope: { n: value }, frameIndex: row };
}

export interface ModelTableProps {
   spec: LessonSpec | undefined;
   fallback?: string;
}

export function ModelTable({ spec, fallback }: ModelTableProps) {
   const model = spec === undefined ? null : computeModel(spec);
   const [shown, setShown] = useState(1);

   if (spec === undefined || model === null || model.rows.length === 0) {
      return <LessonFallback text={fallback} />;
   }

   const current = Math.min(shown, model.rows.length) - 1;
   const figure = model.figureFor(current);
   const rows = model.rows.slice(0, current + 1).map((row) => row.map((value) => formatNumber(value)));
   const isComplete = current === model.rows.length - 1;
   const labels = isComplete && Array.isArray(spec.labels) ? spec.labels.filter((label) => !(isRecord(label) && typeof label.at === "string" && /header/.test(label.at))) : [];

   return (
      <div className="model-table" data-testid="model-table">
         <div className="lesson-beside">
            {figure !== null ? <LessonFigure spec={figure} fallback={fallback} substitution={substitutionFor(spec, model, current)} /> : null}

            <LessonTable spec={{ kind: "table", columns: spec.columns, rows, labels }} fallback={fallback} currentRow={current} />
         </div>

         <div className="action-row">
            <button type="button" className="text-button" data-testid="model-run" disabled={isComplete} onClick={() => setShown(shown + 1)}>
               Run the next row
            </button>
         </div>
      </div>
   );
}
