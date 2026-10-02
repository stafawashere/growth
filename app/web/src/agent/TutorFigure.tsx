import { useCallback, useEffect, useId, useLayoutEffect, useMemo, useRef, useState, type KeyboardEvent, type ReactNode, type RefObject } from "react";

import type {
   FigurePoint,
   TutorFigureAlign,
   TutorFigureCell,
   TutorFigureDot,
   TutorFigureKind,
   TutorFigureLabel,
   TutorFigurePath,
   TutorFigurePrimitive,
   TutorFigureRole,
   TutorFigureSpec
} from "../api/types";
import { GraphFrame, graphLayout, withoutMathDelimiters, type GraphLayout, type TextBox } from "../figures/GraphFrame";
import { prefersReducedMotion } from "../lessons/FrameStepper";
import { MathText } from "../math/MathText";
import { FIGURE_STEP_CLASS, FIGURE_WIPE_CLASS } from "../styles/motion";
import { CURRENT_STEP_WORD, NEXT_STEP_LABEL, PREVIOUS_STEP_LABEL, SHOW_ALL_LABEL, STEPS_LABEL, stepLine } from "./agentCopy";

/* The figure the tutor draws into a reply (docs/agent/drawing-design.md, "The client"). The server
   compiled it into the render spec of drawing-build-plan.md; it arrives as JSON, so it is checked
   again here and a spec that does not check out draws nothing, and the caller shows the refused
   line instead (parseTutorFigure tells it which).

   While the reply streams, the caller reveals steps as their sentences arrive and wires Show all.
   Once the reply has finished, the student steps through the figure with Previous, Next and Show
   all, or with the arrow keys, Home and End while the figure has focus. A step revealed after the
   figure first drew enters with the wipe and the fade of motion.css; steps drawn when it mounted
   are drawn as they end. Labels are an HTML layer over the drawing so they can be typeset, and are
   hidden from assistive technology, which reads the title, the description and the step list. */

export interface TutorFigureProps {
   spec: unknown;
   /* How many steps the stream has revealed, 0 to the number of steps. */
   revealed: number;
   /* The reply has ended, so the student steps through the figure. */
   finished: boolean;
   /* While the reply streams, Show all asks the caller to open every waiting step. */
   onShowAll?: () => void;
   /* Once finished, the index of the step the student moved to. */
   onStep?: (stepIndex: number) => void;
   /* Stands in for the prefers-reduced-motion query. */
   reducedMotion?: boolean;
}

export const MAXIMUM_PRIMITIVES = 200;

export const MAXIMUM_POINTS = 4000;

export const MAXIMUM_STEPS = 6;

const KINDS: TutorFigureKind[] = ["graph", "diagram", "number_line", "table"];

const ROLES: TutorFigureRole[] = ["given", "constructed", "highlight", "error"];

const STYLES = ["solid", "dashed", "dotted"];

const WEIGHTS = ["thin", "regular", "bold"];

const ARROWS = ["none", "end", "start", "both"];

const FILLS = ["none", "region", "region_below"];

const ALIGNS: TutorFigureAlign[] = ["start", "middle", "end"];

/* Half the width of the highlighter under a highlighted stroke, in view units. */
const HIGHLIGHTER_HALF_WIDTH = 5;

/* Where the highlighter bends by more than this, a round join fills the outside of the bend. */
const HIGHLIGHTER_JOIN_ANGLE = Math.PI / 12;

export type RoleClass = TutorFigureRole | "ghost";

const ARROWHEAD_ROLES: RoleClass[] = ["given", "constructed", "highlight", "error", "ghost"];

function isRecord(value: unknown): value is Record<string, unknown> {
   return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isFiniteNumber(value: unknown): value is number {
   return typeof value === "number" && Number.isFinite(value);
}

function isPoint(value: unknown): value is FigurePoint {
   const isPair = Array.isArray(value) && value.length === 2;

   return isPair && isFiniteNumber(value[0]) && isFiniteNumber(value[1]);
}

function isInterval(value: unknown): value is [number, number] {
   return isPoint(value) && value[0] < value[1];
}

function isOneOf<T extends string>(value: unknown, options: readonly T[]): value is T {
   return typeof value === "string" && options.includes(value as T);
}

function isStringArray(value: unknown): value is string[] {
   return Array.isArray(value) && value.every((entry) => typeof entry === "string");
}

function isStepReference(value: unknown, stepIds: Set<string>) {
   return typeof value === "string" && stepIds.has(value);
}

function isCellIndex(value: unknown, count: number) {
   const isIndex = Number.isInteger(value) && (value as number) >= 0;

   return value === null || (isIndex && (value as number) < count);
}

function hasPrimitiveBase(value: Record<string, unknown>, stepIds: Set<string>) {
   const addedByStep = isStepReference(value.step, stepIds);
   const namesElement = typeof value.element === "string";
   const hasRole = isOneOf(value.role, ROLES);
   const fadeIsKnown = value.faded_at === null || isStepReference(value.faded_at, stepIds);
   const eraseIsKnown = value.erased_at === null || isStepReference(value.erased_at, stepIds);

   return addedByStep && namesElement && hasRole && fadeIsKnown && eraseIsKnown;
}

function isPath(value: Record<string, unknown>) {
   const hasPoints = Array.isArray(value.points) && value.points.every(isPoint);
   const hasFlags = typeof value.closed === "boolean" && typeof value.highlighter === "boolean";
   const hasStroke = isOneOf(value.style, STYLES) && isOneOf(value.weight, WEIGHTS) && isOneOf(value.arrow, ARROWS);

   return hasPoints && hasFlags && hasStroke && isOneOf(value.fill, FILLS);
}

function isDot(value: Record<string, unknown>) {
   return isPoint(value.at) && typeof value.open === "boolean";
}

function isLabel(value: Record<string, unknown>) {
   return isPoint(value.at) && isPoint(value.offset) && isOneOf(value.align, ALIGNS) && typeof value.text === "string";
}

function pointsIn(primitive: TutorFigurePrimitive) {
   if (primitive.type === "path") {
      return primitive.points.length;
   }

   return primitive.type === "cell" ? 0 : 1;
}

function isPrimitive(value: unknown, stepIds: Set<string>, table: { columns: number; rows: number } | null): value is TutorFigurePrimitive {
   const hasBase = isRecord(value) && hasPrimitiveBase(value, stepIds);

   if (!hasBase) {
      return false;
   }

   if (table !== null) {
      const isCell = value.type === "cell";
      const textReads = value.text === undefined || typeof value.text === "string";

      return isCell && textReads && isCellIndex(value.row, table.rows) && isCellIndex(value.column, table.columns);
   }

   switch (value.type) {
      case "path":
         return isPath(value);
      case "dot":
         return isDot(value);
      case "label":
         return isLabel(value);
      default:
         return false;
   }
}

function isView(value: unknown): value is NonNullable<TutorFigureSpec["view"]> {
   if (!isRecord(value)) {
      return false;
   }

   const { width, height, padding } = value;
   const hasNumbers = isFiniteNumber(width) && isFiniteNumber(height) && isFiniteNumber(padding);

   if (!hasNumbers) {
      return false;
   }

   const leavesAPlot = padding >= 0 && padding * 2 < width && padding * 2 < height;

   return leavesAPlot;
}

function axesOf(value: unknown): TutorFigureSpec["axes"] | undefined {
   if (value === null || value === undefined) {
      return null;
   }

   if (!isRecord(value)) {
      return undefined;
   }

   const hasTitles = ["x", "y"].every((axis) => value[axis] === undefined || typeof value[axis] === "string");

   return hasTitles ? { x: (value.x as string | undefined) ?? "", y: (value.y as string | undefined) ?? "" } : undefined;
}

/* Types, finite numbers, known steps and the caps; null for anything else. */
export function parseTutorFigure(value: unknown): TutorFigureSpec | null {
   if (!isRecord(value)) {
      return null;
   }

   const hasText = typeof value.id === "string" && typeof value.title === "string" && typeof value.description === "string";
   const hasKind = isOneOf(value.kind, KINDS);
   const steps = value.steps;
   const hasSteps = Array.isArray(steps) && steps.length >= 1 && steps.length <= MAXIMUM_STEPS;
   const readsAsAFigure = hasText && hasKind && hasSteps;

   if (!readsAsAFigure) {
      return null;
   }

   const everyStepReads = steps.every((step) => isRecord(step) && typeof step.id === "string" && typeof step.caption === "string");
   const stepIds = new Set(everyStepReads ? steps.map((step) => step.id as string) : []);
   const stepIdsUnique = stepIds.size === steps.length;
   const hasUsableSteps = everyStepReads && stepIdsUnique;

   if (!hasUsableSteps) {
      return null;
   }

   const isTable = value.kind === "table";
   const hasTableCells = isStringArray(value.columns) && value.columns.length > 0 && Array.isArray(value.rows) && value.rows.every(isStringArray);
   const windowRecord = isRecord(value.window) ? value.window : null;
   const hasWindow = windowRecord !== null && isInterval(windowRecord.x) && isInterval(windowRecord.y);
   const hasPlot = hasWindow && isView(value.view);
   const axes = axesOf(value.axes);
   const hasSurface = isTable ? hasTableCells : hasPlot;
   const isDrawable = hasSurface && axes !== undefined;

   if (!isDrawable) {
      return null;
   }

   const table = isTable ? { columns: (value.columns as string[]).length, rows: (value.rows as string[][]).length } : null;
   const primitives = value.primitives;
   const isWithinPrimitiveCap = Array.isArray(primitives) && primitives.length <= MAXIMUM_PRIMITIVES;
   const everyPrimitiveReads = isWithinPrimitiveCap && primitives.every((primitive) => isPrimitive(primitive, stepIds, table));

   if (!everyPrimitiveReads) {
      return null;
   }

   const pointCount = (primitives as TutorFigurePrimitive[]).reduce((total, primitive) => total + pointsIn(primitive), 0);

   if (pointCount > MAXIMUM_POINTS) {
      return null;
   }

   return {
      id: value.id as string,
      kind: value.kind as TutorFigureKind,
      title: value.title as string,
      description: value.description as string,
      window: hasWindow ? { x: windowRecord.x as [number, number], y: windowRecord.y as [number, number] } : null,
      view: hasPlot ? (value.view as TutorFigureSpec["view"]) : null,
      axes,
      grid: value.grid === true,
      equal_scale: value.equal_scale === true,
      steps: steps.map((step) => ({ id: step.id as string, caption: step.caption as string })),
      columns: isTable ? (value.columns as string[]) : null,
      rows: isTable ? (value.rows as string[][]) : null,
      primitives: primitives as TutorFigurePrimitive[]
   };
}

export type Presence = "hidden" | "drawn" | "ghost";

/* Anything added by a step and perhaps faded or erased by a later one: a figure's primitive or a
   mark on the page. */
export interface Stepped {
   step: string;
   role: TutorFigureRole;
   faded_at: string | null;
   erased_at: string | null;
}

export function presenceOf(primitive: Stepped, stepIndex: Map<string, number>, shown: number): Presence {
   const isAdded = (stepIndex.get(primitive.step) ?? Infinity) < shown;
   const isErased = primitive.erased_at !== null && (stepIndex.get(primitive.erased_at) ?? Infinity) < shown;
   const isFaded = primitive.faded_at !== null && (stepIndex.get(primitive.faded_at) ?? Infinity) < shown;

   if (!isAdded || isErased) {
      return "hidden";
   }

   return isFaded ? "ghost" : "drawn";
}

export function roleClassOf(primitive: Stepped, presence: Presence): RoleClass {
   return presence === "ghost" ? "ghost" : primitive.role;
}

export function rounded(value: number) {
   return Math.round(value * 100) / 100;
}

export function pathData(points: FigurePoint[], closed: boolean) {
   const moves = points.map(([x, y], index) => `${index === 0 ? "M" : "L"}${rounded(x)} ${rounded(y)}`);

   return `${moves.join(" ")}${closed ? " Z" : ""}`;
}

/* A circle wound the same way as the segment outlines, so where they overlap the nonzero fill
   rule fills them as one shape. */
export function circleData([x, y]: FigurePoint, radius: number) {
   const right = `${rounded(x + radius)} ${rounded(y)}`;
   const left = `${rounded(x - radius)} ${rounded(y)}`;

   return `M${right} A${radius} ${radius} 0 1 0 ${left} A${radius} ${radius} 0 1 0 ${right} Z`;
}

function turnAngle(before: FigurePoint, at: FigurePoint, after: FigurePoint) {
   const inAngle = Math.atan2(at[1] - before[1], at[0] - before[0]);
   const outAngle = Math.atan2(after[1] - at[1], after[0] - at[0]);
   const turn = Math.abs(outAngle - inAngle);

   return Math.min(turn, Math.PI * 2 - turn);
}

/* The highlighter is drawn as a filled outline around the stroke rather than as a wide stroke, so
   it is ground that the stroke sits on: a band along each segment, with round ends and round
   joins where the stroke bends. */
export function highlighterData(points: FigurePoint[], closed: boolean) {
   const vertices = closed ? [...points, points[0]] : points;
   const pieces: string[] = [];

   for (let index = 1; index < vertices.length; index += 1) {
      const [startX, startY] = vertices[index - 1];
      const [endX, endY] = vertices[index];
      const length = Math.hypot(endX - startX, endY - startY);

      if (length === 0) {
         continue;
      }

      const normalX = (-(endY - startY) / length) * HIGHLIGHTER_HALF_WIDTH;
      const normalY = ((endX - startX) / length) * HIGHLIGHTER_HALF_WIDTH;
      const corners: FigurePoint[] = [
         [startX + normalX, startY + normalY],
         [endX + normalX, endY + normalY],
         [endX - normalX, endY - normalY],
         [startX - normalX, startY - normalY]
      ];

      pieces.push(pathData(corners, true));
   }

   vertices.forEach((vertex, index) => {
      const isEnd = index === 0 || index === vertices.length - 1;
      const bends = !isEnd && turnAngle(vertices[index - 1], vertex, vertices[index + 1]) > HIGHLIGHTER_JOIN_ANGLE;
      const needsJoin = (isEnd && !closed) || bends;

      if (needsJoin) {
         pieces.push(circleData(vertex, HIGHLIGHTER_HALF_WIDTH));
      }
   });

   return pieces.join(" ");
}

interface PlacedLabel {
   index: number;
   label: TutorFigureLabel;
   presence: Presence;
   leftPercent: number;
   topPercent: number;
   align: TutorFigureAlign;
   x: number;
   y: number;
}

function anchorInside(x: number, width: number, align: TutorFigureAlign, viewWidth: number): { x: number; align: TutorFigureAlign } {
   const startsAt = { start: x, middle: x - width / 2, end: x - width }[align];
   const spillsLeft = startsAt < 0;
   const spillsRight = startsAt + width > viewWidth;

   if (spillsLeft) {
      return { x: 0, align: "start" };
   }

   if (spillsRight) {
      return { x: viewWidth, align: "end" };
   }

   return { x, align };
}

/* The label layer is HTML at the caption type's own size, in CSS pixels, while the drawing scales
   with the width it is given, so a label is larger in view units the smaller the figure is drawn.
   These are the caption's estimated width per character and its line height. */
const LABEL_CHARACTER_PIXELS = 8;

const LABEL_LINE_PIXELS = 18;

function labelWidth(label: TutorFigureLabel, scale: number) {
   return (withoutMathDelimiters(label.text).length * LABEL_CHARACTER_PIXELS) / scale;
}

/* A label sits on its anchor the way SVG text sits on its baseline. It is kept inside the view by
   an estimate of its width at the scale the figure is drawn at; one that would run off an edge is
   anchored to that edge instead, so the text grows back into the figure whatever its typeset width
   turns out to be. */
function placeLabel(index: number, label: TutorFigureLabel, presence: Presence, layout: GraphLayout, scale: number): PlacedLabel {
   const width = labelWidth(label, scale);
   const anchorX = layout.viewX(label.at[0]) + label.offset[0];
   const anchorY = layout.viewY(label.at[1]) + label.offset[1];
   const placed = anchorInside(anchorX, width, label.align, layout.viewWidth);
   const y = Math.min(Math.max(anchorY, LABEL_LINE_PIXELS / scale), layout.viewHeight);

   return {
      index,
      label,
      presence,
      leftPercent: (placed.x / layout.viewWidth) * 100,
      topPercent: (y / layout.viewHeight) * 100,
      align: placed.align,
      x: placed.x,
      y
   };
}

export interface EnteringSteps {
   lastShown: number;
   from: number;
   to: number;
   isFirstFrame: boolean;
}

/* The steps revealed by the latest increase in the shown count. Their first frame is marked so the
   stylesheet starts them collapsed and transparent; the next frame lets them run. When another
   step arrives, the previous ones leave the entering set and jump to their end state. */
export function useEnteringSteps(shown: number) {
   const [entering, setEntering] = useState<EnteringSteps>({ lastShown: shown, from: shown, to: shown, isFirstFrame: false });
   let current = entering;

   if (shown !== entering.lastShown) {
      const grew = shown > entering.lastShown;

      current = grew ? { lastShown: shown, from: entering.lastShown, to: shown, isFirstFrame: true } : { lastShown: shown, from: shown, to: shown, isFirstFrame: false };
      setEntering(current);
   }

   useEffect(() => {
      if (!entering.isFirstFrame) {
         return undefined;
      }

      const frame = requestAnimationFrame(() => setEntering((latest) => ({ ...latest, isFirstFrame: false })));

      return () => cancelAnimationFrame(frame);
   }, [entering]);

   return current;
}

function PositionedLabel(props: { placed: PlacedLabel; motionClass: string; isFirstFrame: boolean }) {
   const { placed } = props;
   const element = useRef<HTMLDivElement>(null);

   useLayoutEffect(() => {
      const node = element.current;

      if (node === null) {
         return;
      }

      node.style.left = `${placed.leftPercent}%`;
      node.style.top = `${placed.topPercent}%`;
   }, [placed.leftPercent, placed.topPercent]);

   return (
      <div
         ref={element}
         className={`tutor-figure-label tutor-figure-${roleClassOf(placed.label, placed.presence)} ${props.motionClass}`.trim()}
         data-align={placed.align}
         data-element={placed.label.element}
         data-index={placed.index}
         data-entering={props.isFirstFrame ? "true" : undefined}
         data-testid="tutor-figure-label"
      >
         <span className="tutor-figure-label-text">
            <MathText text={placed.label.text} renderer="tutor" />
         </span>
      </div>
   );
}

interface StepMotion {
   isEntering: boolean;
   isFirstFrame: boolean;
}

function StepGroup(props: { stepId: string; motion: StepMotion; clipId: string; wipedIn: ReactNode[]; fadedIn: ReactNode[] }) {
   const { motion } = props;
   const hasContent = props.wipedIn.length > 0 || props.fadedIn.length > 0;

   if (!hasContent) {
      return null;
   }

   return (
      <g className={motion.isEntering ? FIGURE_STEP_CLASS : undefined} data-step={props.stepId} data-entering={motion.isFirstFrame ? "true" : undefined}>
         {props.wipedIn.length > 0 ? <g clipPath={motion.isEntering ? `url(#${props.clipId})` : undefined}>{props.wipedIn}</g> : null}
         {props.fadedIn}
      </g>
   );
}

function arrowId(uid: string, roleClass: RoleClass) {
   return `${uid}-arrow-${roleClass}`;
}

function strokeClass(path: TutorFigurePath, roleClass: RoleClass) {
   const isGhost = roleClass === "ghost";

   return isGhost ? "tutor-figure-stroke tutor-figure-ghost" : `tutor-figure-stroke tutor-figure-${roleClass} tutor-figure-style-${path.style} tutor-figure-weight-${path.weight}`;
}

function fillClass(path: TutorFigurePath, roleClass: RoleClass) {
   const isGhost = roleClass === "ghost";
   const tint = path.fill === "region_below" ? "tutor-figure-fill-region-below" : "tutor-figure-fill-region";

   return isGhost ? "tutor-figure-fill tutor-figure-fill-ghost" : `tutor-figure-fill ${tint}`;
}

function Stroke(props: { path: TutorFigurePath; roleClass: RoleClass; toView: (point: FigurePoint) => FigurePoint; uid: string }) {
   const { path, roleClass, uid } = props;
   const hasStart = path.arrow === "start" || path.arrow === "both";
   const hasEnd = path.arrow === "end" || path.arrow === "both";
   const marker = `url(#${arrowId(uid, roleClass)})`;

   return (
      <path
         className={strokeClass(path, roleClass)}
         d={pathData(path.points.map(props.toView), path.closed)}
         markerStart={hasStart ? marker : undefined}
         markerEnd={hasEnd ? marker : undefined}
         data-element={path.element}
      />
   );
}

function Dot(props: { dot: TutorFigureDot; roleClass: RoleClass; toView: (point: FigurePoint) => FigurePoint }) {
   const { dot, roleClass } = props;
   const [cx, cy] = props.toView(dot.at);
   const openClass = dot.open ? " tutor-figure-dot-open" : "";

   return <circle className={`tutor-figure-dot tutor-figure-${roleClass}${openClass}`} cx={rounded(cx)} cy={rounded(cy)} data-element={dot.element} />;
}

interface Layers {
   fills: ReactNode[];
   underlays: ReactNode[];
   underlayDots: ReactNode[];
   strokes: ReactNode[];
   dots: ReactNode[];
}

function emptyLayers(): Layers {
   return { fills: [], underlays: [], underlayDots: [], strokes: [], dots: [] };
}

interface DrawnLabels {
   scale: number;
   boxes: Record<number, TextBox>;
}

function estimatedLabelBox(placed: PlacedLabel, scale: number): TextBox {
   const width = labelWidth(placed.label, scale);
   const left = { start: placed.x, middle: placed.x - width / 2, end: placed.x - width }[placed.align];

   return { left, right: left + width, top: placed.y - LABEL_LINE_PIXELS / scale, bottom: placed.y };
}

/* The scale the figure is drawn at and, for each label drawn, where it is in view units, measured
   after layout and again whenever the figure changes size, so the frame leaves out the tick numbers
   a label covers. Without layout (or before it) the scale is 1 and no label is measured. */
function useDrawnLabels(canvas: RefObject<HTMLDivElement>, viewWidth: number) {
   const [drawn, setDrawn] = useState<DrawnLabels>({ scale: 1, boxes: {} });
   const lastDrawn = useRef(JSON.stringify(drawn));

   const measure = useCallback(() => {
      const node = canvas.current;
      const frame = node?.getBoundingClientRect();
      const hasLayout = node !== null && node !== undefined && frame !== undefined && frame.width > 0;

      if (!hasLayout) {
         return;
      }

      const scale = frame.width / viewWidth;
      const inView = (pixels: number) => rounded(pixels / scale);
      const boxes: Record<number, TextBox> = {};

      node.querySelectorAll("[data-testid='tutor-figure-label']").forEach((label) => {
         const text = label.querySelector(".tutor-figure-label-text")?.getBoundingClientRect();
         const isDrawn = text !== undefined && text.width > 0;

         if (isDrawn) {
            boxes[Number(label.getAttribute("data-index"))] = {
               left: inView(text.left - frame.left),
               right: inView(text.right - frame.left),
               top: inView(text.top - frame.top),
               bottom: inView(text.bottom - frame.top)
            };
         }
      });

      const next = { scale: rounded(scale), boxes };
      const serialised = JSON.stringify(next);

      if (serialised !== lastDrawn.current) {
         lastDrawn.current = serialised;
         setDrawn(next);
      }
   }, [canvas, viewWidth]);

   useLayoutEffect(measure);

   useEffect(() => {
      const node = canvas.current;
      const canObserve = node !== null && typeof ResizeObserver === "function";

      if (!canObserve) {
         return undefined;
      }

      const observer = new ResizeObserver(measure);

      observer.observe(node);

      return () => observer.disconnect();
   }, [canvas, measure]);

   return drawn;
}

function Drawing(props: { figure: TutorFigureSpec; shown: number; entering: EnteringSteps; uid: string; titleId: string; describedBy: string }) {
   const { figure, shown, entering, uid } = props;
   const canvas = useRef<HTMLDivElement>(null);
   const view = figure.view!;
   const drawnLabels = useDrawnLabels(canvas, view.width);
   const plotWindow = { domain: figure.window!.x, range: figure.window!.y };
   const layout = graphLayout(plotWindow, view.width, view.padding, view.height - view.padding * 2);
   const toView = (point: FigurePoint): FigurePoint => [layout.viewX(point[0]), layout.viewY(point[1])];
   const stepIndex = new Map(figure.steps.map((step, index) => [step.id, index]));
   const byStep = figure.steps.map(emptyLayers);
   const labels: PlacedLabel[] = [];
   const hasArrows = figure.primitives.some((primitive) => primitive.type === "path" && primitive.arrow !== "none");

   const labelBoxes = figure.primitives.flatMap((primitive, index) => {
      if (primitive.type !== "label") {
         return [];
      }

      const measured = drawnLabels.boxes[index];

      return [measured ?? estimatedLabelBox(placeLabel(index, primitive, "drawn", layout, drawnLabels.scale), drawnLabels.scale)];
   });

   figure.primitives.forEach((primitive, index) => {
      const presence = presenceOf(primitive, stepIndex, shown);

      if (presence === "hidden") {
         return;
      }

      const layers = byStep[stepIndex.get(primitive.step)!];
      const roleClass = roleClassOf(primitive, presence);
      const isGhost = presence === "ghost";

      if (primitive.type === "label") {
         labels.push(placeLabel(index, primitive, presence, layout, drawnLabels.scale));
         return;
      }

      if (primitive.type === "dot") {
         const isHighlighted = primitive.role === "highlight" && !isGhost;

         if (isHighlighted) {
            const [cx, cy] = toView(primitive.at);

            layers.underlayDots.push(<circle key={index} className="tutor-figure-highlighter tutor-figure-dot-halo" cx={rounded(cx)} cy={rounded(cy)} />);
         }

         layers.dots.push(<Dot key={index} dot={primitive} roleClass={roleClass} toView={toView} />);
         return;
      }

      const isDrawablePath = primitive.type === "path" && primitive.points.length >= 2;

      if (!isDrawablePath) {
         return;
      }

      if (primitive.fill !== "none") {
         layers.fills.push(
            <path key={index} className={fillClass(primitive, roleClass)} d={pathData(primitive.points.map(toView), true)} data-element={primitive.element} />
         );
         return;
      }

      const hasHighlighter = primitive.highlighter && !isGhost;

      if (hasHighlighter) {
         layers.underlays.push(<path key={index} className="tutor-figure-highlighter" d={highlighterData(primitive.points.map(toView), primitive.closed)} />);
      }

      layers.strokes.push(<Stroke key={index} path={primitive} roleClass={roleClass} toView={toView} uid={uid} />);
   });

   function motionOf(index: number): StepMotion {
      const isEntering = index >= entering.from && index < entering.to;

      return { isEntering, isFirstFrame: isEntering && entering.isFirstFrame };
   }

   const enteringWithPaths = figure.steps
      .map((step, index) => ({ step, index }))
      .filter(({ index }) => {
         const layers = byStep[index];
         const hasPaths = layers.underlays.length > 0 || layers.strokes.length > 0;

         return motionOf(index).isEntering && hasPaths;
      });

   const clipIdOf = (index: number) => `${uid}-wipe-${index}`;

   return (
      <div className="tutor-figure-canvas" ref={canvas}>
         <svg
            role="img"
            aria-labelledby={props.titleId}
            aria-describedby={props.describedBy}
            viewBox={`0 0 ${view.width} ${view.height}`}
            className="tutor-figure-svg"
            data-kind={figure.kind}
            data-testid="tutor-figure-svg"
         >
            <defs>
               {hasArrows
                  ? ARROWHEAD_ROLES.map((roleClass) => (
                       <marker
                          key={roleClass}
                          id={arrowId(uid, roleClass)}
                          viewBox="0 0 10 10"
                          refX={9}
                          refY={5}
                          markerWidth={5}
                          markerHeight={5}
                          markerUnits="strokeWidth"
                          orient="auto-start-reverse"
                       >
                          <path className={`tutor-figure-arrowhead tutor-figure-${roleClass}`} d="M0 0 L10 5 L0 10 Z" />
                       </marker>
                    ))
                  : null}

               {enteringWithPaths.map(({ index }) => (
                  <clipPath key={index} id={clipIdOf(index)}>
                     <rect
                        className={FIGURE_WIPE_CLASS}
                        x={0}
                        y={0}
                        width={view.width}
                        height={view.height}
                        data-entering={motionOf(index).isFirstFrame ? "true" : undefined}
                     />
                  </clipPath>
               ))}
            </defs>

            <g className="tutor-figure-fills">
               {figure.steps.map((step, index) => (
                  <StepGroup key={step.id} stepId={step.id} motion={motionOf(index)} clipId={clipIdOf(index)} wipedIn={[]} fadedIn={byStep[index].fills} />
               ))}
            </g>

            {figure.kind === "graph" ? (
               <GraphFrame
                  plotWindow={plotWindow}
                  layout={layout}
                  gridlines={figure.grid}
                  axisTitles={[figure.axes?.x ?? "", figure.axes?.y ?? ""]}
                  labelBoxes={labelBoxes}
               />
            ) : null}

            <g className="tutor-figure-underlays">
               {figure.steps.map((step, index) => (
                  <StepGroup
                     key={step.id}
                     stepId={step.id}
                     motion={motionOf(index)}
                     clipId={clipIdOf(index)}
                     wipedIn={byStep[index].underlays}
                     fadedIn={byStep[index].underlayDots}
                  />
               ))}
            </g>

            <g className="tutor-figure-marks">
               {figure.steps.map((step, index) => (
                  <StepGroup key={step.id} stepId={step.id} motion={motionOf(index)} clipId={clipIdOf(index)} wipedIn={byStep[index].strokes} fadedIn={byStep[index].dots} />
               ))}
            </g>
         </svg>

         <div className="tutor-figure-labels" aria-hidden="true" data-testid="tutor-figure-labels">
            {labels.map((placed) => {
               const index = stepIndex.get(placed.label.step)!;
               const motion = motionOf(index);

               return (
                  <PositionedLabel
                     key={placed.index}
                     placed={placed}
                     motionClass={motion.isEntering ? FIGURE_STEP_CLASS : ""}
                     isFirstFrame={motion.isFirstFrame}
                  />
               );
            })}
         </div>
      </div>
   );
}

function cellClassOf(cell: TutorFigureCell, presence: Presence) {
   if (presence === "ghost") {
      return "tutor-figure-cell-ghost";
   }

   return cell.role === "error" ? "tutor-figure-cell-error" : "tutor-figure-cell-highlight";
}

function Table(props: { figure: TutorFigureSpec; shown: number; titleId: string; describedBy: string }) {
   const { figure, shown } = props;
   const stepIndex = new Map(figure.steps.map((step, index) => [step.id, index]));
   const marked = new Map<string, string>();
   const notes = new Map<string, string>();

   for (const primitive of figure.primitives) {
      const presence = presenceOf(primitive, stepIndex, shown);
      const isShownCell = primitive.type === "cell" && presence !== "hidden";

      if (!isShownCell) {
         continue;
      }

      const cell = primitive as TutorFigureCell;
      const className = cellClassOf(cell, presence);
      const covered: string[] = [];

      figure.rows!.forEach((row, rowIndex) => {
         row.forEach((_, columnIndex) => {
            const inRow = cell.row === null || cell.row === rowIndex;
            const inColumn = cell.column === null || cell.column === columnIndex;

            if (inRow && inColumn) {
               covered.push(`${rowIndex},${columnIndex}`);
               marked.set(`${rowIndex},${columnIndex}`, className);
            }
         });
      });

      /* A highlight's words go once, in the first cell it covers, so a labelled row reads as one
         label and not as a label in every cell. */
      const hasNote = cell.text !== undefined && cell.text.trim() !== "" && covered.length > 0;

      if (hasNote) {
         notes.set(covered[0], cell.text!);
      }
   }

   return (
      <div className="tutor-figure-table-frame">
         <table className="tutor-figure-table" aria-labelledby={props.titleId} aria-describedby={props.describedBy} data-testid="tutor-figure-table">
            <thead>
               <tr>
                  {figure.columns!.map((column, index) => (
                     <th key={index} scope="col">
                        <MathText text={column} renderer="tutor" />
                     </th>
                  ))}
               </tr>
            </thead>
            <tbody>
               {figure.rows!.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                     {row.map((cell, columnIndex) => (
                        <td key={columnIndex} className={marked.get(`${rowIndex},${columnIndex}`)}>
                           <MathText text={cell} renderer="tutor" />
                           {notes.has(`${rowIndex},${columnIndex}`) ? (
                              <span className="tutor-figure-cell-note" data-testid="tutor-figure-cell-note">
                                 <MathText text={notes.get(`${rowIndex},${columnIndex}`)!} renderer="tutor" />
                              </span>
                           ) : null}
                        </td>
                     ))}
                  </tr>
               ))}
            </tbody>
         </table>
      </div>
   );
}

function DrawnFigure(props: Omit<TutorFigureProps, "spec"> & { figure: TutorFigureSpec }) {
   const { figure, finished, onShowAll, onStep } = props;
   const uid = useId().replace(/:/g, "");
   const titleId = `${uid}-title`;
   const descriptionId = `${uid}-description`;
   const stepsId = `${uid}-steps`;
   const [prefersReduced] = useState(prefersReducedMotion);
   const isReduced = props.reducedMotion ?? prefersReduced;
   const revealed = Number.isFinite(props.revealed) ? Math.floor(props.revealed) : 0;
   const available = Math.min(Math.max(revealed, 0), figure.steps.length);
   const [chosen, setChosen] = useState<number | null>(null);
   const shown = finished && chosen !== null ? Math.min(chosen, available) : available;
   const entering = useEnteringSteps(shown);
   const hasSteps = finished && available > 0;
   const describedBy = hasSteps ? `${descriptionId} ${stepsId}` : descriptionId;
   const current = figure.steps[shown - 1];

   function showStep(count: number) {
      const bounded = Math.min(Math.max(count, 1), available);

      if (bounded === shown) {
         return;
      }

      setChosen(bounded);
      onStep?.(bounded - 1);
   }

   function showAll() {
      if (!finished) {
         onShowAll?.();
         return;
      }

      showStep(available);
   }

   function stepOnKey(event: KeyboardEvent<HTMLDivElement>) {
      const isOnFigure = event.target === event.currentTarget;
      const targets: Record<string, number> = { ArrowLeft: shown - 1, ArrowRight: shown + 1, Home: 1, End: available };
      const target = targets[event.key];
      const shouldStep = hasSteps && isOnFigure && target !== undefined;

      if (shouldStep) {
         event.preventDefault();
         showStep(target);
      }
   }

   const isBuilding = !finished;
   const everyStepShown = shown >= (isBuilding ? figure.steps.length : available);

   return (
      <div
         className="tutor-figure"
         role="group"
         tabIndex={0}
         aria-labelledby={titleId}
         aria-describedby={descriptionId}
         onKeyDown={stepOnKey}
         data-testid="tutor-figure"
      >
         <p className="tutor-figure-title" id={titleId}>
            {figure.title}
         </p>

         {figure.kind === "table" ? (
            <Table figure={figure} shown={shown} titleId={titleId} describedBy={describedBy} />
         ) : (
            <Drawing figure={figure} shown={shown} entering={entering} uid={uid} titleId={titleId} describedBy={describedBy} />
         )}

         <p className="visually-hidden" id={descriptionId}>
            {figure.description}
         </p>

         {hasSteps && current !== undefined ? (
            <p className="tutor-figure-step-line" data-testid="tutor-figure-step-line">
               <MathText text={stepLine(shown, available, current.caption)} renderer="tutor" />
            </p>
         ) : null}

         {isBuilding || hasSteps ? (
            <div className="tutor-figure-controls">
               {hasSteps ? (
                  <>
                     <button type="button" className="text-button" disabled={shown <= 1} onClick={() => showStep(shown - 1)}>
                        {PREVIOUS_STEP_LABEL}
                     </button>

                     <button type="button" className="text-button" disabled={shown >= available} onClick={() => showStep(shown + 1)}>
                        {NEXT_STEP_LABEL}
                     </button>
                  </>
               ) : null}

               <button type="button" className="text-button" disabled={everyStepShown} onClick={showAll}>
                  {SHOW_ALL_LABEL}
               </button>
            </div>
         ) : null}

         {hasSteps ? (
            <details className="tutor-figure-steps" open={isReduced} data-testid="tutor-figure-steps">
               <summary>{STEPS_LABEL}</summary>

               <ol className="tutor-figure-step-list" id={stepsId}>
                  {figure.steps.slice(0, available).map((step, index) => {
                     const isCurrent = index === shown - 1;

                     return (
                        <li key={step.id} aria-current={isCurrent ? "step" : undefined}>
                           <MathText text={step.caption} renderer="tutor" />
                           {isCurrent ? <span className="tutor-figure-now">{CURRENT_STEP_WORD}</span> : null}
                        </li>
                     );
                  })}
               </ol>
            </details>
         ) : null}
      </div>
   );
}

export function TutorFigure({ spec, ...rest }: TutorFigureProps) {
   const figure = useMemo(() => parseTutorFigure(spec), [spec]);

   if (figure === null) {
      return null;
   }

   return <DrawnFigure figure={figure} {...rest} />;
}
