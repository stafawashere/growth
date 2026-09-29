import type { FigureLabel, FigureMark, FigurePoint, GraphFigureKind, GraphFigureSpec } from "../api/types";
import { PLOT_PADDING, VIEW_WIDTH } from "../figures/FigureView";
import {
   compileExpression,
   insideWindow,
   marchingSquares,
   numberFrom,
   sampleFunction,
   sampleParametric,
   windowOf,
   type Compiled,
   type Interval2,
   type Scope
} from "./expression";

/* Turns a lesson delivery spec (the design's declarative spec, CONTRACT.md spec kinds and keys)
   into the GraphFigureSpec that figures/FigureView.tsx draws, so a lesson figure is drawn by the
   same code as an item figure and keeps 04 Figures rule 13: every label sits inside the plot and
   there is no caption. The designs were written by hand and vary in how they name the same thing
   (window or axes, curves or curve, at or x and y), so every key is read defensively. A spec from
   which nothing can be drawn returns null and the caller shows the block's fallback text. */

export type SpecRecord = Record<string, unknown>;

/* The values a frame or a control substitutes: numbers into the expressions, and a window or a
   frame record for the kinds whose frames carry more than a number. */
export interface Substitution {
   scope: Scope;
   frame?: SpecRecord;
   frameIndex?: number;
   cursor?: { name: string; value: number; onCurve: boolean };
   drives?: string;
}

const EMPTY: Substitution = { scope: {} };

/* FigureView's own layout, repeated here only to place labels in view units before handing them
   over as data coordinates: the plot is VIEW_WIDTH wide inside PLOT_PADDING, its height follows
   the window's aspect between these bounds, and a character of label text is about this wide. */
const PLOT_WIDTH = VIEW_WIDTH - PLOT_PADDING * 2;

const MINIMUM_PLOT_HEIGHT = 180;

const CHARACTER_WIDTH = 8;

const LINE_HEIGHT = 14;

const LABEL_GAP = 6;

const SLOPE_MARK_LENGTH = 14;

const PANEL_KINDS = ["graph_panels", "stacked_graphs", "graph_pair", "panels", "slice_shapes"];

export function isRecord(value: unknown): value is SpecRecord {
   return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isPoint(value: unknown): value is FigurePoint {
   const isPair = Array.isArray(value) && value.length === 2;

   return isPair && typeof value[0] === "number" && typeof value[1] === "number";
}

function isInterval(value: unknown): value is [number, number] {
   return isPoint(value) && value[0] < value[1];
}

function asArray(value: unknown): unknown[] {
   if (value === undefined || value === null) {
      return [];
   }

   return Array.isArray(value) ? value : [value];
}

export function isPanelKind(kind: string) {
   return PANEL_KINDS.includes(kind);
}

/* ------------------------------------------------------------------ curves */

interface CurveSource {
   f: ((x: number, scope: Scope) => number) | null;
   segments?: FigurePoint[][];
   domain: [number, number] | null;
   label: string | null;
   dashed: boolean;
}

const COORDINATE_PAIR = /\(\s*(-?\d*\.?\d+)\s*,\s*(-?\d*\.?\d+)\s*\)/g;

export function coordinatesIn(text: string): FigurePoint[] {
   return Array.from(text.matchAll(COORDINATE_PAIR)).map((match) => [Number(match[1]), Number(match[2])] as FigurePoint);
}

function piecewiseLinear(points: FigurePoint[]) {
   const sorted = [...points].sort((a, b) => a[0] - b[0]);

   return (x: number) => {
      for (let index = 0; index < sorted.length - 1; index += 1) {
         const [x0, y0] = sorted[index];
         const [x1, y1] = sorted[index + 1];

         if (x >= x0 && x <= x1) {
            return x1 === x0 ? y0 : y0 + ((y1 - y0) * (x - x0)) / (x1 - x0);
         }
      }

      return NaN;
   };
}

function span(points: FigurePoint[]): [number, number] | null {
   const xs = points.map(([x]) => x);
   const low = Math.min(...xs);
   const high = Math.max(...xs);

   return low < high ? [low, high] : null;
}

/* "y = x^2 + 2", "f'(x) = 3x^2 - 3", "x + 1": the right-hand side of a named equation, with the
   design's trailing notes (", dashed") dropped. */
export function expressionText(text: string) {
   const withoutNote = text.replace(/,\s*dashed\s*$/i, "");
   const named = /^\s*[A-Za-z]'*\s*(\(\s*[a-z]\s*\))?\s*=\s*(.+)$/.exec(withoutNote);

   return (named === null ? withoutNote : named[2]).trim();
}

function variableOf(text: string) {
   const compiledWithT = /\bt\b/.test(text) && !/\bx\b/.test(text);

   return compiledWithT ? "t" : "x";
}

function curveFromText(text: string, domain: [number, number] | null, label: string | null): CurveSource | null {
   const isDashed = /,\s*dashed\s*$/i.test(text);
   const hasThrough = /\bthrough\b/i.test(text);

   if (hasThrough) {
      const points = coordinatesIn(text);

      if (points.length < 2) {
         return null;
      }

      const f = piecewiseLinear(points);

      return { f: (x) => f(x), domain: span(points), label, dashed: isDashed };
   }

   const body = expressionText(text);
   const compiled = compileExpression(body);

   if (compiled === null) {
      return null;
   }

   const variable = variableOf(body);

   return { f: (x, scope) => compiled({ ...scope, [variable]: x }), domain, label, dashed: isDashed };
}

function semicircle(entry: SpecRecord): CurveSource | null {
   const centre = entry.center ?? entry.centre;
   const radius = entry.radius;

   if (!isPoint(centre) || typeof radius !== "number") {
      return null;
   }

   const sign = entry.side === "below" ? -1 : 1;
   const f = (x: number) => centre[1] + sign * Math.sqrt(radius * radius - (x - centre[0]) ** 2);

   return { f, domain: [centre[0] - radius, centre[0] + radius], label: null, dashed: false };
}

function labelText(value: unknown): string | null {
   if (typeof value === "string") {
      return value;
   }

   return isRecord(value) && typeof value.text === "string" ? value.text : null;
}

function curveFromEntry(entry: unknown): CurveSource | null {
   if (typeof entry === "string") {
      return curveFromText(entry, null, null);
   }

   if (!isRecord(entry)) {
      return null;
   }

   const domain = isInterval(entry.domain) ? entry.domain : null;
   const label = labelText(entry.label);

   if (typeof entry.expr === "string") {
      return curveFromText(entry.expr, domain, label);
   }

   const polyline = entry.type === "polyline" ? entry.points : entry.piecewise_linear;

   if (Array.isArray(polyline) && polyline.every(isPoint) && polyline.length > 1) {
      const f = piecewiseLinear(polyline);

      return { f: (x) => f(x), domain: span(polyline), label, dashed: false };
   }

   if (entry.type === "semicircle") {
      return semicircle(entry);
   }

   if (isRecord(entry.semicircle)) {
      return semicircle(entry.semicircle);
   }

   if (typeof entry.curve === "string") {
      return curveFromText(entry.curve, domain, label);
   }

   return null;
}

function regionBounds(spec: SpecRecord): { upper: string; lower: string; interval: [number, number] } | null {
   const region = isRecord(spec.region) ? spec.region : isRecord(spec.base) ? spec.base : null;

   if (region !== null && typeof region.upper === "string" && typeof region.lower === "string" && isInterval(region.interval)) {
      return { upper: region.upper, lower: region.lower, interval: region.interval };
   }

   const hasCurveAndLower = typeof spec.curve === "string" && typeof spec.region_lower === "string" && isInterval(spec.interval);

   if (hasCurveAndLower) {
      return { upper: spec.curve as string, lower: spec.region_lower as string, interval: spec.interval as [number, number] };
   }

   return null;
}

function curvesOf(spec: SpecRecord): CurveSource[] {
   const entries = [...asArray(spec.curves), ...asArray(spec.curve), ...asArray(spec.true_curve)];
   const region = regionBounds(spec);

   if (region !== null && entries.length === 0) {
      entries.push(region.upper, region.lower);
   } else if (region !== null) {
      entries.push(region.lower);
   }

   const sources = entries.map(curveFromEntry).filter((source): source is CurveSource => source !== null);
   const interval = isInterval(spec.interval) ? spec.interval : region?.interval ?? null;

   return sources.map((source) => ({ ...source, domain: source.domain ?? interval }));
}

/* The value of the figure's function at x: the first curve whose domain holds x, so a graph drawn
   as a polyline followed by a semicircle reads as one piecewise function. */
function valueAt(curves: CurveSource[], x: number, scope: Scope) {
   for (const curve of curves) {
      const holds = curve.domain === null || (x >= curve.domain[0] && x <= curve.domain[1]);

      if (curve.f !== null && holds) {
         const y = curve.f(x, scope);

         if (Number.isFinite(y)) {
            return y;
         }
      }
   }

   return NaN;
}

/* ------------------------------------------------------------------ window */

function paddedRange(values: number[]): [number, number] | null {
   const finite = values.filter(Number.isFinite);

   if (finite.length === 0) {
      return null;
   }

   const low = Math.min(...finite);
   const high = Math.max(...finite);
   const margin = high > low ? (high - low) * 0.1 : 1;

   return [low - margin, high + margin];
}

function windowFrom(spec: SpecRecord, curves: CurveSource[], points: FigurePoint[], substitution: Substitution): Interval2 | null {
   const frameWindow = substitution.frame === undefined ? null : windowOf(substitution.frame);

   if (frameWindow !== null) {
      return frameWindow;
   }

   const centre = spec.center ?? spec.centre;
   const halfWidth = substitution.scope.half_width;

   if (isPoint(centre) && typeof halfWidth === "number") {
      return { x: [centre[0] - halfWidth, centre[0] + halfWidth], y: [centre[1] - halfWidth * 2, centre[1] + halfWidth * 2] };
   }

   const given = windowOf(spec);

   if (given !== null) {
      return given;
   }

   const box = isRecord(spec.window) ? spec.window : null;
   const givenX = box !== null && isInterval(box.x) ? box.x : null;
   const givenY = box !== null && isInterval(box.y) ? box.y : null;
   const domains = curves.flatMap((curve) => (curve.domain === null ? [] : curve.domain));
   const x = givenX ?? paddedRange([...domains, ...points.map(([px]) => px)]) ?? [-5, 5];
   const sampled: number[] = [];

   for (let index = 0; index <= 60; index += 1) {
      sampled.push(valueAt(curves, x[0] + ((x[1] - x[0]) * index) / 60, substitution.scope));
   }

   const y = givenY ?? paddedRange([...sampled, ...points.map(([, py]) => py), 0]);

   return y === null ? null : { x, y };
}

/* ------------------------------------------------------------------ labels */

interface ViewMap {
   toView: (point: FigurePoint) => FigurePoint;
   toData: (point: FigurePoint) => FigurePoint;
   left: number;
   right: number;
   top: number;
   bottom: number;
}

export function plotHeightFor(window: Interval2) {
   const aspect = (window.y[1] - window.y[0]) / (window.x[1] - window.x[0]);

   return Math.min(PLOT_WIDTH, Math.max(MINIMUM_PLOT_HEIGHT, PLOT_WIDTH * aspect));
}

export function viewMapFor(window: Interval2): ViewMap {
   const height = plotHeightFor(window);
   const xSpan = window.x[1] - window.x[0];
   const ySpan = window.y[1] - window.y[0];

   return {
      toView: ([x, y]) => [PLOT_PADDING + ((x - window.x[0]) / xSpan) * PLOT_WIDTH, PLOT_PADDING + ((window.y[1] - y) / ySpan) * height],
      toData: ([vx, vy]) => [window.x[0] + ((vx - PLOT_PADDING) / PLOT_WIDTH) * xSpan, window.y[1] - ((vy - PLOT_PADDING) / height) * ySpan],
      left: PLOT_PADDING,
      right: PLOT_PADDING + PLOT_WIDTH,
      top: PLOT_PADDING,
      bottom: PLOT_PADDING + height
   };
}

function textWidth(text: string) {
   return text.replace(/\\\(|\\\)/g, "").trim().length * CHARACTER_WIDTH;
}

/* A label's anchor is where its text starts, on its baseline. Clamping keeps the whole text box
   inside the plot, so a label never runs past the drawing (04 rule 13). */
function clampedAnchor(view: ViewMap, text: string, vx: number, vy: number): FigurePoint {
   const width = textWidth(text);
   const rightmost = Math.max(view.left + 2, view.right - width - 2);
   const x = Math.min(Math.max(vx, view.left + 2), rightmost);
   const y = Math.min(Math.max(vy, view.top + LINE_HEIGHT), view.bottom - 2);

   return view.toData([x, y]);
}

type Side = "above" | "below" | "left" | "right";

function sideOf(at: string): Side {
   const lower = at.toLowerCase();

   if (lower.includes("left")) {
      return "left";
   }

   if (lower.includes("below") || lower.includes("under")) {
      return "below";
   }

   if (lower.includes("above")) {
      return "above";
   }

   return "right";
}

function besidePoint(view: ViewMap, text: string, point: FigurePoint, side: Side): FigurePoint {
   const [vx, vy] = view.toView(point);
   const width = textWidth(text);
   const offsets: Record<Side, FigurePoint> = {
      above: [vx - width / 2, vy - LABEL_GAP],
      below: [vx - width / 2, vy + LINE_HEIGHT + LABEL_GAP],
      left: [vx - width - LABEL_GAP, vy - LABEL_GAP],
      right: [vx + LABEL_GAP, vy - LABEL_GAP]
   };
   const [x, y] = offsets[side];

   return clampedAnchor(view, text, x, y);
}

/* Labels with no coordinate stack in the plot's corners: from the top unless the design says
   bottom or lower, on the left unless it says right. Each corner fills one line at a time so two
   such labels never share a line. */
class CornerSlots {
   private used: Record<string, number> = {};

   constructor(private readonly view: ViewMap) {}

   place(text: string, at: string): FigurePoint {
      const lower = at.toLowerCase();
      const isBottom = lower.includes("bottom") || lower.includes("lower");
      const isRight = lower.includes("right");
      const key = `${isBottom ? "b" : "t"}${isRight ? "r" : "l"}`;
      const line = this.used[key] ?? 0;

      this.used[key] = line + 1;

      const x = isRight ? this.view.right - textWidth(text) - LABEL_GAP : this.view.left + LABEL_GAP;
      const y = isBottom ? this.view.bottom - LABEL_GAP - line * LINE_HEIGHT : this.view.top + LINE_HEIGHT + LABEL_GAP / 2 + line * LINE_HEIGHT;

      return clampedAnchor(this.view, text, x, y);
   }
}

function substitute(text: string, scope: Scope) {
   return text.replace(/\{([A-Za-z_][A-Za-z0-9_]*)\}/g, (whole, name: string) =>
      name in scope ? formatNumber(scope[name]) : whole
   );
}

export function formatNumber(value: number) {
   if (!Number.isFinite(value)) {
      return String(value);
   }

   return String(Number(value.toPrecision(4)));
}

/* ------------------------------------------------------------------ marks */

function pointOf(entry: unknown, curves: CurveSource[], substitution: Substitution, parametric: ParametricPath | null): FigurePoint | null {
   if (isPoint(entry)) {
      return entry;
   }

   if (typeof entry === "string") {
      const found = coordinatesIn(entry);

      return found.length === 1 ? found[0] : null;
   }

   if (!isRecord(entry)) {
      return null;
   }

   if (isPoint(entry.at)) {
      return entry.at;
   }

   const scope = substitution.scope;

   if (entry.t !== undefined && parametric !== null) {
      const t = numberFrom(entry.t, scope);

      return t === null ? null : parametric.at(t);
   }

   const x = numberFrom(entry.at ?? entry.x, scope);

   if (x === null) {
      return null;
   }

   const y = entry.y === undefined ? valueAt(curves, x, scope) : numberFrom(entry.y, scope);

   return y === null || !Number.isFinite(y) ? null : [x, y];
}

function dashed(from: FigurePoint, to: FigurePoint): FigureMark {
   return { type: "segment", from, to, style: "dashed" };
}

function verticalAt(window: Interval2, x: number): FigureMark {
   return dashed([x, window.y[0]], [x, window.y[1]]);
}

function horizontalAt(window: Interval2, y: number): FigureMark {
   return dashed([window.x[0], y], [window.x[1], y]);
}

function numberAfter(text: string, name: "x" | "y") {
   const match = new RegExp(`\\b${name}\\s*=\\s*(-?\\d*\\.?\\d+)`).exec(text);

   return match === null ? null : Number(match[1]);
}

/* ------------------------------------------------------------------ parametric and fields */

interface ParametricPath {
   at: (t: number) => FigurePoint;
   range: [number, number];
}

/* x(t), y(t) given directly, or their rates from a start point, integrated by the trapezoid rule
   in small steps from the start of the t range. */
function parametricOf(spec: SpecRecord): ParametricPath | null {
   const range = isInterval(spec.t_range) ? spec.t_range : null;
   const x = typeof spec.x === "string" ? compileExpression(expressionText(spec.x)) : null;
   const y = typeof spec.y === "string" ? compileExpression(expressionText(spec.y)) : null;

   if (x !== null && y !== null) {
      return { at: (t) => [x({ t }), y({ t })], range: range ?? [0, 1] };
   }

   const xRate = typeof spec.x_rate === "string" ? compileExpression(spec.x_rate) : null;
   const yRate = typeof spec.y_rate === "string" ? compileExpression(spec.y_rate) : null;

   if (xRate === null || yRate === null || range === null || !isPoint(spec.start)) {
      return null;
   }

   const start = spec.start;
   const steps = 400;
   const table: FigurePoint[] = [start];
   const dt = (range[1] - range[0]) / steps;

   for (let index = 0; index < steps; index += 1) {
      const t0 = range[0] + index * dt;
      const t1 = t0 + dt;
      const [px, py] = table[index];

      table.push([px + ((xRate({ t: t0 }) + xRate({ t: t1 })) * dt) / 2, py + ((yRate({ t: t0 }) + yRate({ t: t1 })) * dt) / 2]);
   }

   return {
      at: (t) => table[Math.min(steps, Math.max(0, Math.round((t - range[0]) / dt)))],
      range
   };
}

/* dy/dx = F(x, y) with the design's own names: "dP/dt = 2P/5 - P^2/2000" reads P as the vertical
   variable and t as the horizontal one. */
function fieldOf(spec: SpecRecord): ((x: number, y: number) => number) | null {
   if (typeof spec.equation !== "string") {
      return null;
   }

   const match = /^\s*d\s*([A-Za-z])\s*\/\s*d\s*([A-Za-z])\s*=\s*(.+)$/.exec(spec.equation);
   const [vertical, horizontal, body] = match === null ? ["y", "x", spec.equation] : [match[1], match[2], match[3]];
   const compiled = compileExpression(body);

   if (compiled === null) {
      return null;
   }

   return (x, y) => compiled({ [horizontal]: x, [vertical]: y });
}

function slopeMarks(field: (x: number, y: number) => number, window: Interval2, step: number): FigurePoint[][] {
   const view = viewMapFor(window);
   const segments: FigurePoint[][] = [];

   for (let x = Math.ceil(window.x[0] / step) * step; x <= window.x[1] + 1e-9; x += step) {
      for (let y = Math.ceil(window.y[0] / step) * step; y <= window.y[1] + 1e-9; y += step) {
         const slope = field(x, y);

         if (!Number.isFinite(slope)) {
            continue;
         }

         const [vx, vy] = view.toView([x, y]);
         const [ax, ay] = view.toView([x + 1, y + slope]);
         const length = Math.hypot(ax - vx, ay - vy);
         const ux = ((ax - vx) / length) * (SLOPE_MARK_LENGTH / 2);
         const uy = ((ay - vy) / length) * (SLOPE_MARK_LENGTH / 2);

         segments.push([view.toData([vx - ux, vy - uy]), view.toData([vx + ux, vy + uy])]);
      }
   }

   return segments;
}

function rungeKutta(field: (x: number, y: number) => number, start: FigurePoint, end: number, window: Interval2): FigurePoint[] {
   const points: FigurePoint[] = [start];
   const steps = 200;
   const h = (end - start[0]) / steps;
   let [x, y] = start;

   for (let index = 0; index < steps; index += 1) {
      const k1 = field(x, y);
      const k2 = field(x + h / 2, y + (h * k1) / 2);
      const k3 = field(x + h / 2, y + (h * k2) / 2);
      const k4 = field(x + h, y + h * k3);

      y += (h * (k1 + 2 * k2 + 2 * k3 + k4)) / 6;
      x += h;

      if (!insideWindow([x, y], window)) {
         break;
      }

      points.push([x, y]);
   }

   return points;
}

/* ------------------------------------------------------------------ the builder */

function graphKindFor(kind: string): GraphFigureKind {
   const byKind: Record<string, GraphFigureKind> = {
      region: "region",
      region_with_axis: "region",
      washer: "region",
      solid_from_slices: "region",
      solid_of_revolution: "region",
      slope_field: "slope_field",
      field_trace: "slope_field",
      euler_steps: "slope_field",
      solution_curves: "slope_field",
      parametric_path: "parametric_curve",
      parametric_trace: "parametric_curve",
      vector_diagram: "vector_diagram",
      geometric_diagram: "geometric_diagram",
      number_line_pair: "number_line",
      particle_on_line: "number_line"
   };

   return byKind[kind] ?? "function_graph";
}

function axisTitles(spec: SpecRecord): string[] {
   const box = isRecord(spec.window) ? spec.window : isRecord(spec.axes) ? spec.axes : null;
   const names = box === null ? [] : Object.keys(box);
   const isPlain = names.length < 2 || (names[0] === "x" && names[1] === "y");

   return isPlain ? ["x", "y"] : [names[0], names[1]];
}

function fillUnder(curves: CurveSource[], from: number, to: number, scope: Scope, window: Interval2): FigurePoint[] | null {
   const [low, high] = [Math.max(Math.min(from, to), window.x[0]), Math.min(Math.max(from, to), window.x[1])];

   if (!(low < high)) {
      return null;
   }

   const base = Math.min(Math.max(0, window.y[0]), window.y[1]);
   const points: FigurePoint[] = [[low, base]];

   for (let index = 0; index <= 80; index += 1) {
      const x = low + ((high - low) * index) / 80;
      const y = valueAt(curves, x, scope);

      if (Number.isFinite(y)) {
         points.push([x, Math.min(Math.max(y, window.y[0]), window.y[1])]);
      }
   }

   points.push([high, base]);

   return points.length > 3 ? points : null;
}

function fillBetween(upper: Compiled, lower: Compiled, from: number, to: number, scope: Scope, window: Interval2): FigurePoint[] | null {
   const top: FigurePoint[] = [];
   const bottom: FigurePoint[] = [];
   const clamp = (y: number) => Math.min(Math.max(y, window.y[0]), window.y[1]);

   for (let index = 0; index <= 80; index += 1) {
      const x = from + ((to - from) * index) / 80;
      const a = upper({ ...scope, x });
      const b = lower({ ...scope, x });

      if (Number.isFinite(a) && Number.isFinite(b)) {
         top.push([x, clamp(a)]);
         bottom.unshift([x, clamp(b)]);
      }
   }

   return top.length > 1 ? [...top, ...bottom] : null;
}

function compiledCurve(text: unknown) {
   return typeof text === "string" ? compileExpression(expressionText(text)) : null;
}

interface Build {
   curves: GraphFigureSpec["curves"];
   fills: GraphFigureSpec["fills"];
   marks: FigureMark[];
   labels: FigureLabel[];
}

function addShading(spec: SpecRecord, curves: CurveSource[], window: Interval2, substitution: Substitution, build: Build) {
   const scope = substitution.scope;
   const shade = spec.shade ?? spec.shaded;

   if (isRecord(shade)) {
      const between = Array.isArray(shade.between) ? shade.between.map(compiledCurve) : null;
      const range = isInterval(shade.x) ? shade.x : null;
      const hasBetween = between !== null && between.length === 2 && between[0] !== null && between[1] !== null && range !== null;

      if (hasBetween) {
         const fill = fillBetween(between![0]!, between![1]!, range![0], range![1], scope, window);

         if (fill !== null) {
            build.fills.push({ points: fill });
         }
      } else {
         const from = numberFrom(shade.from, scope);
         const to = numberFrom(shade.to, scope);
         const fill = from !== null && to !== null ? fillUnder(curves, from, to, scope, window) : null;

         if (fill !== null) {
            build.fills.push({ points: fill });
         }
      }
   }

   for (const entry of asArray(spec.shading)) {
      const interval = isRecord(entry) && isInterval(entry.interval) ? entry.interval : null;
      const fill = interval === null ? null : fillUnder(curves, interval[0], interval[1], scope, window);

      if (fill !== null) {
         build.fills.push({ points: fill });
      }
   }

   const region = regionBounds(spec);
   const regionShaded = region !== null && build.fills.length === 0;

   if (regionShaded) {
      const upper = compiledCurve(region!.upper);
      const lower = compiledCurve(region!.lower);
      const fill = upper !== null && lower !== null ? fillBetween(upper, lower, region!.interval[0], region!.interval[1], scope, window) : null;

      if (fill !== null) {
         build.fills.push({ points: fill });
      }
   }
}

function addRectangles(spec: SpecRecord, curves: CurveSource[], window: Interval2, scope: Scope, build: Build) {
   const rectangles = spec.rectangles;

   if (isRecord(rectangles) && typeof rectangles.n === "number") {
      const domain = curves.find((curve) => curve.domain !== null)?.domain ?? window.x;
      const n = numberFrom(scope.n ?? rectangles.n, scope) ?? rectangles.n;
      const width = (domain[1] - domain[0]) / n;
      const offset = rectangles.sum === "right" ? 1 : rectangles.sum === "midpoint" ? 0.5 : 0;

      for (let index = 0; index < n; index += 1) {
         const left = domain[0] + index * width;
         const height = valueAt(curves, left + offset * width, scope);

         if (Number.isFinite(height)) {
            build.fills.push({ points: [[left, 0], [left, height], [left + width, height], [left + width, 0]] });
         }
      }
   }

   for (const entry of asArray(Array.isArray(rectangles) ? rectangles : [])) {
      if (!isRecord(entry)) {
         continue;
      }

      const x = numberFrom(entry.x, scope);
      const width = numberFrom(entry.width, scope) ?? 0;
      const top = compiledCurve(entry.to);
      const bottom = compiledCurve(entry.from);

      if (x !== null && top !== null && bottom !== null) {
         const low = bottom({ ...scope, x });
         const high = top({ ...scope, x });

         build.fills.push({ points: [[x - width / 2, low], [x - width / 2, high], [x + width / 2, high], [x + width / 2, low]] });
      }
   }
}

function addLines(spec: SpecRecord, curves: CurveSource[], window: Interval2, substitution: Substitution, build: Build) {
   const scope = substitution.scope;

   for (const entry of asArray(spec.asymptotes)) {
      if (!isRecord(entry)) {
         continue;
      }

      const x = numberFrom(entry.x, scope);
      const y = numberFrom(entry.y, scope);

      if (x !== null) {
         build.marks.push(verticalAt(window, x));
      } else if (y !== null) {
         build.marks.push(horizontalAt(window, y));
      }
   }

   for (const entry of asArray(spec.segments)) {
      if (isRecord(entry) && isPoint(entry.from) && isPoint(entry.to)) {
         build.marks.push({ type: "segment", from: entry.from, to: entry.to, style: entry.style === "dashed" ? "dashed" : "solid" });
      }
   }

   for (const entry of asArray(spec.guides)) {
      const vertical = isRecord(entry) ? numberFrom(entry.vertical, scope) : typeof entry === "string" ? numberAfter(entry, "x") : null;
      const horizontal = isRecord(entry) ? numberFrom(entry.horizontal, scope) : typeof entry === "string" ? numberAfter(entry, "y") : null;

      if (vertical !== null) {
         build.marks.push(verticalAt(window, vertical));
      } else if (horizontal !== null) {
         build.marks.push(horizontalAt(window, horizontal));
      }
   }

   for (const entry of asArray(spec.partition)) {
      const x = numberFrom(entry, scope);
      const y = x === null ? NaN : valueAt(curves, x, scope);

      if (x !== null && Number.isFinite(y)) {
         build.marks.push(dashed([x, 0], [x, y]));
      }
   }

   const tangent = isRecord(spec.tangent) ? spec.tangent : null;
   const tangentAt = tangent === null ? null : numberFrom(tangent.at, scope);
   const tangentSlope = tangent === null ? null : numberFrom(tangent.slope, scope);

   if (tangentAt !== null && tangentSlope !== null) {
      const y0 = valueAt(curves, tangentAt, scope);
      const line = (x: number) => y0 + tangentSlope * (x - tangentAt);

      build.curves.push({ segments: sampleFunction(line, window.x, window), style: "solid" });
   }

   /* A sweep's secant through the marked point and the point h to its right (graph_sweep). */
   const h = scope.h;
   const anchor = asArray(spec.points).find((entry) => isRecord(entry) && isPoint(entry.at)) as SpecRecord | undefined;

   if (spec.secant !== undefined && typeof h === "number" && anchor !== undefined) {
      const [x0] = anchor.at as FigurePoint;
      const y0 = valueAt(curves, x0, scope);
      const y1 = valueAt(curves, x0 + h, scope);
      const slope = (y1 - y0) / h;

      if (Number.isFinite(slope)) {
         build.curves.push({ segments: sampleFunction((x) => y0 + slope * (x - x0), window.x, window), style: "solid" });
         build.marks.push({ type: "point", at: [x0 + h, y1] });
      }
   }

}

function addFields(spec: SpecRecord, window: Interval2, substitution: Substitution, build: Build) {
   const field = fieldOf(spec);

   if (field === null) {
      return;
   }

   const kind = spec.kind;
   const step = typeof spec.lattice_step === "number" ? spec.lattice_step : (window.x[1] - window.x[0]) / 10;
   const drawsLattice = kind === "slope_field" || kind === "field_trace" || kind === "solution_curves";

   if (drawsLattice) {
      build.curves.push({ segments: slopeMarks(field, window, step), style: "solid" });
   }

   for (const entry of asArray(spec.marked)) {
      if (isPoint(entry)) {
         build.marks.push({ type: "point", at: entry });
      }
   }

   const scope = substitution.scope;
   const start = isPoint(spec.start) ? spec.start : null;
   const cursorStart =
      substitution.cursor !== undefined && kind === "solution_curves" ? ([window.x[0], substitution.cursor.value] as FigurePoint) : null;
   const draggedStart =
      substitution.cursor !== undefined && kind === "slope_field" && start === null
         ? ([scope.x ?? 0, scope.y ?? 0] as FigurePoint)
         : null;
   const traceFrom = cursorStart ?? draggedStart ?? (kind === "field_trace" ? start : null);

   if (traceFrom !== null) {
      const reach = kind === "field_trace" ? numberFrom(scope.x, scope) : null;
      const ends = reach === null ? [window.x[1], window.x[0]] : [reach];
      const segments = ends
         .filter((end) => end !== traceFrom[0])
         .map((end) => rungeKutta(field, traceFrom, end, window))
         .filter((segment) => segment.length > 1);

      build.curves.push({ segments, style: "solid" });
      build.marks.push({ type: "point", at: traceFrom });
   }

   if (kind === "euler_steps" && start !== null) {
      const h = typeof spec.step === "number" ? spec.step : 0.5;
      const count = substitution.frameIndex ?? asArray(spec.frames).length - 1;
      const path: FigurePoint[] = [start];

      for (let index = 0; index < count; index += 1) {
         const [x, y] = path[index];

         path.push([x + h, y + h * field(x, y)]);
      }

      build.curves.push({ segments: [path], style: "solid" });
      path.forEach((point) => build.marks.push({ type: "point", at: point }));
   }
}

function addParametric(spec: SpecRecord, parametric: ParametricPath | null, window: Interval2, substitution: Substitution, build: Build) {
   if (parametric === null) {
      return;
   }

   const t = substitution.scope.t;
   const end = typeof t === "number" ? t : parametric.range[1];
   const start = spec.kind === "parametric_trace" ? Math.min(...asArray(spec.frames).map((frame) => (isRecord(frame) ? Number(frame.t) : 0))) : parametric.range[0];
   const range: [number, number] = [start, Math.max(end, start + 1e-6)];
   const x = (scope: Scope) => parametric.at(scope.t)[0];
   const y = (scope: Scope) => parametric.at(scope.t)[1];

   build.curves.push({ segments: sampleParametric(x, y, range, window), style: "solid" });

   if (typeof t === "number") {
      const at = parametric.at(t);

      build.marks.push({ type: "point", at }, dashed([at[0], 0], at), dashed([0, at[1]], at));
   }
}

function parametricWindow(parametric: ParametricPath): Interval2 | null {
   const points: FigurePoint[] = [];

   for (let index = 0; index <= 100; index += 1) {
      points.push(parametric.at(parametric.range[0] + ((parametric.range[1] - parametric.range[0]) * index) / 100));
   }

   const x = paddedRange([...points.map(([px]) => px), 0]);
   const y = paddedRange([...points.map(([, py]) => py), 0]);

   return x === null || y === null ? null : { x, y };
}

/* Kinds drawn on a line rather than a plane: number_line_pair puts the numerator on an upper line
   and the denominator on a lower one; particle_on_line puts the particle on one line at x(t). */
function lineKind(spec: SpecRecord, substitution: Substitution, build: Build): Interval2 | null {
   const scope = substitution.scope;

   if (spec.kind === "number_line_pair") {
      const frames = asArray(spec.frames).filter(isRecord);
      const values = frames.flatMap((frame) => [Number(frame.numerator), Number(frame.denominator)]);
      const x = paddedRange([...values, 0]);

      if (x === null) {
         return null;
      }

      const window: Interval2 = { x, y: [-1, 2] };
      const frame = substitution.frame ?? frames[frames.length - 1] ?? {};

      build.marks.push({ type: "segment", from: [x[0], 1], to: [x[1], 1], style: "solid" });
      build.marks.push({ type: "segment", from: [x[0], 0], to: [x[1], 0], style: "solid" });

      const numerator = numberFrom(frame.numerator, scope);
      const denominator = numberFrom(frame.denominator, scope);

      if (numerator !== null) {
         build.marks.push({ type: "point", at: [numerator, 1] });
      }

      if (denominator !== null) {
         build.marks.push({ type: "point", at: [denominator, 0] });
      }

      return window;
   }

   const position = typeof spec.position === "string" ? compileExpression(expressionText(spec.position)) : null;
   const given = windowOf(spec);

   if (position === null || given === null) {
      return null;
   }

   const window: Interval2 = { x: given.y, y: [-1, 1] };
   const t = scope.t ?? given.x[0];

   build.marks.push({ type: "segment", from: [window.x[0], 0], to: [window.x[1], 0], style: "solid" });
   build.marks.push({ type: "point", at: [position({ t }), 0] });

   return window;
}

export interface BuiltGraph {
   spec: GraphFigureSpec;
   window: Interval2;
}

/* The one path every graph-like kind takes. Returns null when nothing in the spec can be drawn: no
   curve, fill, field or point survived parsing, so the figure would be empty axes. */
export function buildGraph(spec: SpecRecord, substitution: Substitution = EMPTY, alt = ""): BuiltGraph | null {
   const scope = substitution.scope;
   const build: Build = { curves: [], fills: [], marks: [], labels: [] };
   const kind = typeof spec.kind === "string" ? spec.kind : "graph";
   const curves = curvesOf(spec);
   const parametric = parametricOf(spec);
   const isLineKind = kind === "number_line_pair" || kind === "particle_on_line";
   const lineWindow = isLineKind ? lineKind(spec, substitution, build) : null;
   const pointEntries = [...asArray(spec.points), ...asArray(spec.marks)];
   const plainPoints = pointEntries
      .map((entry) => pointOf(entry, curves, substitution, parametric))
      .filter((point): point is FigurePoint => point !== null);
   const vectorPoints = [spec.tail, spec.head].filter(isPoint);
   const window =
      lineWindow ??
      (parametric !== null && windowOf(spec) === null ? parametricWindow(parametric) : null) ??
      windowFrom(spec, curves, [...plainPoints, ...vectorPoints], substitution);

   if (window === null) {
      return null;
   }

   for (const curve of curves) {
      const domain = curve.domain ?? window.x;
      const segments = curve.f === null ? curve.segments ?? [] : sampleFunction((x) => curve.f!(x, scope), domain, window);

      if (segments.length > 0) {
         build.curves.push({ segments, style: curve.dashed ? "dashed" : "solid" });
      }
   }

   /* An implicit curve: "(y - 1)^2 = x^2 (x + 3)" is F = left - right, drawn by marching squares
      unless one side is y alone, which is y = f(x) and is sampled as a graph. */
   if (kind === "implicit_curve" && typeof spec.curve === "string" && spec.curve.includes("=")) {
      const [left, right] = spec.curve.split("=");
      const isExplicit = left.trim() === "y" && !/\by\b/.test(right);
      const lhs = compileExpression(left);
      const rhs = compileExpression(right);

      if (!isExplicit && lhs !== null && rhs !== null) {
         build.curves.splice(0, build.curves.length, {
            segments: marchingSquares((x, y) => lhs({ ...scope, x, y }) - rhs({ ...scope, x, y }), window),
            style: "solid"
         });
      }
   }

   if (kind === "solid_of_revolution" && curves.length > 0) {
      const mirror = curves[0];
      const domain = mirror.domain ?? window.x;

      build.curves.push({ segments: sampleFunction((x) => -(mirror.f?.(x, scope) ?? NaN), domain, window), style: "solid" });
   }

   addShading(spec, curves, window, substitution, build);
   addRectangles(spec, curves, window, scope, build);
   addLines(spec, curves, window, substitution, build);
   addFields(spec, window, substitution, build);
   addParametric(spec, parametric, window, substitution, build);

   if (vectorPoints.length === 2) {
      const [tail, head] = vectorPoints;

      build.marks.push({ type: "segment", from: tail, to: head, style: "solid" }, { type: "point", at: head });

      if (asArray(spec.legs).length > 0) {
         build.marks.push(dashed(tail, [head[0], tail[1]]), dashed([head[0], tail[1]], head));
      }
   }

   for (const entry of pointEntries) {
      const at = pointOf(entry, curves, substitution, parametric);
      const style = isRecord(entry) ? entry.style : undefined;

      if (at !== null) {
         build.marks.push({ type: style === "open" ? "open_point" : "point", at });
      }
   }

   const slice = numberFrom(spec.slice_at_x ?? (kind === "solid_from_slices" ? scope.x : undefined), scope);
   const highlight = isRecord(spec.highlight) ? numberFrom(spec.highlight.disc_at_x, scope) : null;

   for (const x of [slice, highlight]) {
      if (x !== null) {
         build.marks.push(verticalAt(window, x));
      }
   }

   /* Only what the spec itself draws counts: a control's guide line on empty axes is not a
      figure, so a spec drawn in prose alone still falls back to its text. */
   const drewSomething = build.curves.some((curve) => curve.segments.length > 0) || build.fills.length > 0 || build.marks.length > 0;

   if (!drewSomething) {
      return null;
   }

   const drives = substitution.drives ?? "";
   const drivenY = numberAfter(substitute(drives.replace(/\by\s*=\s*([A-Za-z])\b/, (_whole, name: string) => `y = {${name}}`), scope), "y");

   if (drivenY !== null) {
      build.marks.push(horizontalAt(window, drivenY));
   }

   const cursor = substitution.cursor;

   if (cursor !== undefined && cursor.onCurve && kind !== "solution_curves") {
      const y = kind === "slope_field" ? NaN : valueAt(curves, cursor.value, scope);

      build.marks.push(verticalAt(window, cursor.value));

      if (Number.isFinite(y)) {
         build.marks.push({ type: "point", at: [cursor.value, y] });
      }
   }

   build.labels = labelsFor(spec, curves, window, substitution, parametric);

   const figure: GraphFigureSpec = {
      kind: graphKindFor(kind),
      domain: window.x,
      range: window.y,
      curves: build.curves.filter((curve) => curve.segments.length > 0),
      fills: build.fills,
      marks: build.marks.filter((mark) => (mark.type === "segment" ? true : insideWindow(mark.at, window))),
      labels: build.labels,
      gridlines: !isLineKind,
      axis_titles: isLineKind ? [] : axisTitles(spec),
      alt
   };

   return { spec: figure, window };
}

/* Every label the spec carries, each with placement inside (CONTRACT.md: the checker enforces it
   on the record). A label at a coordinate sits there; a point's label sits beside its point on the
   side the design names; a curve's label sits on the curve two thirds of the way along its longest
   piece; every other label takes the next free line in the corner its "at" names. */
function labelsFor(spec: SpecRecord, curves: CurveSource[], window: Interval2, substitution: Substitution, parametric: ParametricPath | null): FigureLabel[] {
   const view = viewMapFor(window);
   const corners = new CornerSlots(view);
   const labels: FigureLabel[] = [];
   const scope = substitution.scope;

   function add(text: string, anchor: FigurePoint) {
      labels.push({ text: substitute(text, scope), anchor, placement: "inside" });
   }

   for (const entry of asArray(spec.points)) {
      const text = isRecord(entry) ? labelText(entry.label) : null;
      const at = pointOf(entry, curves, substitution, parametric);

      if (text !== null && at !== null && insideWindow(at, window)) {
         const where = isRecord(entry) && isRecord(entry.label) && typeof entry.label.at === "string" ? entry.label.at : "right";

         add(text, besidePoint(view, text, at, sideOf(where)));
      }
   }

   for (const [index, entry] of asArray(spec.curves).entries()) {
      const text = isRecord(entry) ? labelText(entry.label) : null;
      const curve = curves[index];

      if (text === null || curve === undefined || curve.f === null) {
         continue;
      }

      const domain = curve.domain ?? window.x;
      const pieces = sampleFunction((x) => curve.f!(x, scope), domain, window);
      const longest = pieces.sort((a, b) => b.length - a.length)[0];

      if (longest !== undefined) {
         add(text, besidePoint(view, text, longest[Math.floor((longest.length * 2) / 3)], "above"));
      }
   }

   const titled = isRecord(spec.title) ? [spec.title] : [];

   for (const entry of [...titled, ...asArray(spec.labels)]) {
      const text = labelText(entry);

      if (text === null) {
         continue;
      }

      const at = isRecord(entry) ? entry.at : undefined;
      const coordinates = typeof at === "string" ? coordinatesIn(at) : [];

      if (isPoint(at) && insideWindow(at, window)) {
         add(text, clampedAnchor(view, text, ...view.toView(at)));
      } else if (coordinates.length === 1 && insideWindow(coordinates[0], window)) {
         add(text, besidePoint(view, text, coordinates[0], sideOf(String(at))));
      } else {
         add(text, corners.place(text, typeof at === "string" ? at : ""));
      }
   }

   return labels;
}

/* ------------------------------------------------------------------ panels */

/* The sub-specs a panel kind draws side by side or stacked. A panel takes the parent's window and
   curves where it names none of its own, and the parent's labels are shared out in order, one to
   each panel in turn, so each stays inside a plot. graph_pair written as top and bottom strings
   becomes two panels. */
export function panelsOf(spec: SpecRecord): SpecRecord[] {
   const rawPanels = Array.isArray(spec.panels)
      ? spec.panels
      : [spec.top, spec.bottom].filter((entry) => entry !== undefined).map((entry) => (typeof entry === "string" ? { curve: entry } : entry));
   const panels = rawPanels.filter(isRecord);
   const parentLabels = asArray(spec.labels);
   const inherited: SpecRecord = {};

   for (const key of ["window", "axes", "curves", "guides", "interval"]) {
      if (spec[key] !== undefined) {
         inherited[key] = spec[key];
      }
   }

   return panels.map((panel, index) => {
      const ownCurve = panel.curve !== undefined || panel.curves !== undefined;
      const merged: SpecRecord = { ...inherited, ...(ownCurve ? { curves: undefined } : {}), ...panel, kind: "graph" };
      const parentWindow = isRecord(spec.window) ? spec.window : null;
      const panelWindow = isRecord(panel.window) ? panel.window : null;

      if (parentWindow !== null && panelWindow !== null) {
         merged.window = { ...parentWindow, ...panelWindow };
      }

      const shared = parentLabels.filter((_label, labelIndex) => labelIndex % panels.length === index);

      merged.labels = [...asArray(panel.labels), ...shared];

      return merged;
   });
}
