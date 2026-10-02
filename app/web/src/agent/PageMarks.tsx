import { useCallback, useEffect, useId, useLayoutEffect, useMemo, useRef, useState, type ReactNode } from "react";

import type { FigurePoint, TutorMark, TutorMarkKind, TutorMarkSide, TutorMarkTarget, TutorMarksSpec } from "../api/types";
import { MathText } from "../math/MathText";
import { FIGURE_STEP_CLASS, FIGURE_WIPE_CLASS } from "../styles/motion";
import { highlighterData, pathData, presenceOf, roleClassOf, rounded, useEnteringSteps, type EnteringSteps, type Presence, type RoleClass } from "./TutorFigure";

/* The live tutor's marks on the page itself (docs/agent/drawing-design.md, "Marks on the page"):
   an underline under a phrase of the stem, a ring on the item's own graph, a highlighted table row,
   a note in the margin, an arrow across the page. The model never names a pixel. Each mark names an
   anchor the screen declared with data-agent-anchor, and the overlay finds that element, measures
   it and draws over it wherever it is laid out, following scroll, resize and layout changes. A
   mark whose anchor or quoted phrase is not on the screen is left out.

   Two fixed layers sit above the page content and below the tutor panel, which the provider
   renders after them: highlighter bands in a layer that multiplies with the page, so the words
   under a band stay readable, and the strokes and notes above it. Neither takes a pointer event
   or focus, and both are hidden from assistive technology; the reply lists what was marked. */

export const MAXIMUM_MARK_STEPS = 6;

export const MAXIMUM_MARKS = 12;

const KINDS: TutorMarkKind[] = ["ring", "underline", "highlight", "strike", "bracket", "note", "arrow", "point", "segment", "line", "vline", "hline"];

const TARGETED_KINDS: TutorMarkKind[] = ["ring", "underline", "highlight", "strike", "bracket", "note"];

const GRAPH_KINDS: TutorMarkKind[] = ["segment", "line", "vline", "hline"];

const ROLES = ["given", "constructed", "highlight", "error"];

const STYLES = ["solid", "dashed", "dotted"];

const WEIGHTS = ["thin", "regular", "bold"];

const ARROWS = ["none", "end", "start", "both"];

const SIDES: TutorMarkSide[] = ["left", "right", "above", "below"];

const ANCHOR_ID = /^[A-Za-z0-9_]+$/;

const ARROWHEAD_ROLES: RoleClass[] = ["given", "constructed", "highlight", "error", "ghost"];

/* Distances in CSS pixels between a mark and what it marks. */
const UNDERLINE_DROP = 2;

const RING_MARGIN = 6;

const POINT_RING_RADIUS = 10;

const BAND_OVERHANG = 2;

const BRACKET_GAP = 8;

const BRACKET_HOOK = 6;

const NOTE_GAP = 8;

const VIEWPORT_MARGIN = 8;

const ARROW_CLEARANCE = 4;

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

function isIndex(value: unknown) {
   return Number.isInteger(value) && (value as number) >= 0;
}

function isOneOf(value: unknown, options: readonly string[]) {
   return typeof value === "string" && options.includes(value);
}

function isStepReference(value: unknown, stepIds: Set<string>) {
   return typeof value === "string" && stepIds.has(value);
}

function targetOf(value: unknown): TutorMarkTarget | null {
   if (!isRecord(value)) {
      return null;
   }

   const namesAnchor = typeof value.anchor === "string" && ANCHOR_ID.test(value.anchor);
   const quoteReads = value.quote === null || value.quote === undefined || typeof value.quote === "string";
   const atReads = value.at === null || value.at === undefined || isPoint(value.at);
   const rowReads = value.row === null || value.row === undefined || isIndex(value.row);
   const columnReads = value.column === null || value.column === undefined || isIndex(value.column);
   const cellReads = value.cell === null || value.cell === undefined || (Array.isArray(value.cell) && value.cell.length === 2 && value.cell.every(isIndex));
   const reads = namesAnchor && quoteReads && atReads && rowReads && columnReads && cellReads;

   if (!reads) {
      return null;
   }

   return {
      anchor: value.anchor as string,
      quote: (value.quote as string | null | undefined) ?? null,
      at: (value.at as FigurePoint | null | undefined) ?? null,
      row: (value.row as number | null | undefined) ?? null,
      column: (value.column as number | null | undefined) ?? null,
      cell: (value.cell as [number, number] | null | undefined) ?? null
   };
}

function strokeReads(value: unknown) {
   if (!isRecord(value)) {
      return false;
   }

   const hasEnums = isOneOf(value.style, STYLES) && isOneOf(value.weight, WEIGHTS) && isOneOf(value.arrow, ARROWS);

   return hasEnums && typeof value.highlighter === "boolean";
}

function markOf(value: unknown, stepIds: Set<string>): TutorMark | null {
   if (!isRecord(value)) {
      return null;
   }

   const addedByStep = isStepReference(value.step, stepIds);
   const fadeIsKnown = value.faded_at === null || value.faded_at === undefined || isStepReference(value.faded_at, stepIds);
   const eraseIsKnown = value.erased_at === null || value.erased_at === undefined || isStepReference(value.erased_at, stepIds);
   const hasBase = addedByStep && typeof value.element === "string" && isOneOf(value.role, ROLES) && strokeReads(value.stroke) && fadeIsKnown && eraseIsKnown;
   const hasKind = isOneOf(value.kind, KINDS);

   if (!hasBase || !hasKind) {
      return null;
   }

   const kind = value.kind as TutorMarkKind;
   const target = targetOf(value.target);
   const from = targetOf(value.from);
   const to = targetOf(value.to);
   const text = typeof value.text === "string" ? value.text : null;
   const side = isOneOf(value.side, SIDES) ? (value.side as TutorMarkSide) : null;
   const points = Array.isArray(value.points) && value.points.length === 2 && value.points.every(isPoint) ? (value.points as [FigurePoint, FigurePoint]) : null;
   const at = isPoint(value.at) ? value.at : null;

   const lacksTarget = TARGETED_KINDS.includes(kind) && target === null;
   const lacksText = kind === "note" && text === null;
   const lacksEnds = kind === "arrow" && (from === null || to === null);
   const lacksPoints = GRAPH_KINDS.includes(kind) && points === null;
   const lacksPoint = kind === "point" && at === null;
   const isMissingSomething = lacksTarget || lacksText || lacksEnds || lacksPoints || lacksPoint;

   if (isMissingSomething) {
      return null;
   }

   return {
      step: value.step as string,
      element: value.element as string,
      role: value.role as TutorMark["role"],
      stroke: value.stroke as TutorMark["stroke"],
      faded_at: (value.faded_at as string | null | undefined) ?? null,
      erased_at: (value.erased_at as string | null | undefined) ?? null,
      kind,
      target,
      from,
      to,
      text,
      side,
      at,
      open: value.open === true,
      points
   };
}

/* Types, finite numbers, known steps and the caps of the marks contract; null for anything else. */
export function parseTutorMarks(value: unknown): TutorMarksSpec | null {
   if (!isRecord(value)) {
      return null;
   }

   const hasText = typeof value.id === "string" && typeof value.description === "string";
   const steps = value.steps;
   const hasSteps = Array.isArray(steps) && steps.length >= 1 && steps.length <= MAXIMUM_MARK_STEPS;
   const marks = value.marks;
   const hasMarks = Array.isArray(marks) && marks.length <= MAXIMUM_MARKS;
   const readsAsMarks = hasText && hasSteps && hasMarks;

   if (!readsAsMarks) {
      return null;
   }

   const everyStepReads = steps.every((step) => isRecord(step) && typeof step.id === "string" && typeof step.caption === "string");
   const stepIds = new Set(everyStepReads ? steps.map((step) => step.id as string) : []);
   const hasUsableSteps = everyStepReads && stepIds.size === steps.length;

   if (!hasUsableSteps) {
      return null;
   }

   const parsed = marks.map((mark) => markOf(mark, stepIds));
   const everyMarkReads = parsed.every((mark) => mark !== null);

   if (!everyMarkReads) {
      return null;
   }

   return {
      id: value.id as string,
      description: value.description as string,
      steps: steps.map((step) => ({ id: step.id as string, caption: step.caption as string })),
      marks: parsed as TutorMark[]
   };
}

interface Box {
   left: number;
   top: number;
   right: number;
   bottom: number;
}

function boxOf(rect: { left: number; top: number; right: number; bottom: number }): Box {
   return { left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom };
}

function unionOf(boxes: Box[]): Box {
   return {
      left: Math.min(...boxes.map((box) => box.left)),
      top: Math.min(...boxes.map((box) => box.top)),
      right: Math.max(...boxes.map((box) => box.right)),
      bottom: Math.max(...boxes.map((box) => box.bottom))
   };
}

function centreOf(box: Box): FigurePoint {
   return [(box.left + box.right) / 2, (box.top + box.bottom) / 2];
}

function anchorElement(anchor: string) {
   return document.querySelector(`[data-agent-anchor="${anchor}"]`);
}

interface TextPosition {
   start: [Node, number] | { before: Element };
   end: [Node, number] | { after: Element };
}

/* The anchor's text as the packet held it: its words with whitespace collapsed, and each typeset
   formula read back as its source between \( and \). Every character remembers where it sits in
   the page, so a quoted phrase becomes a DOM range. */
function readableText(root: Element) {
   let text = "";
   const positions: TextPosition[] = [];

   function add(character: string, position: TextPosition) {
      const isSpace = /\s/.test(character);
      const followsSpace = text === "" || text.endsWith(" ");

      if (isSpace && followsSpace) {
         return;
      }

      text += isSpace ? " " : character;
      positions.push(position);
   }

   function walk(node: Node) {
      if (node.nodeType === Node.TEXT_NODE) {
         const data = node.textContent ?? "";

         for (let offset = 0; offset < data.length; offset += 1) {
            add(data[offset], { start: [node, offset], end: [node, offset + 1] });
         }

         return;
      }

      if (!(node instanceof Element)) {
         return;
      }

      const isFormula = node.classList.contains("katex");

      if (isFormula) {
         const source = node.querySelector('annotation[encoding="application/x-tex"]')?.textContent ?? "";

         for (const character of `\\(${source}\\)`) {
            add(character, { start: { before: node }, end: { after: node } });
         }

         return;
      }

      node.childNodes.forEach(walk);
   }

   walk(root);

   return { text, positions };
}

function normalisedQuote(quote: string) {
   return quote.replace(/\\\[/g, "\\(").replace(/\\\]/g, "\\)").replace(/\s+/g, " ").trim();
}

function quoteBoxes(element: Element, quote: string): Box[] | null {
   const { text, positions } = readableText(element);
   const wanted = normalisedQuote(quote);
   const found = wanted === "" ? -1 : text.indexOf(wanted);

   if (found < 0) {
      return null;
   }

   const range = document.createRange();
   const first = positions[found].start;
   const last = positions[found + wanted.length - 1].end;

   if (Array.isArray(first)) {
      range.setStart(first[0], first[1]);
   } else {
      range.setStartBefore(first.before);
   }

   if (Array.isArray(last)) {
      range.setEnd(last[0], last[1]);
   } else {
      range.setEndAfter(last.after);
   }

   const canMeasure = typeof range.getClientRects === "function";
   const lines = canMeasure ? Array.from(range.getClientRects()).filter((rect) => rect.width > 0) : [];

   return lines.length > 0 ? lines.map(boxOf) : null;
}

function numbersIn(attribute: string | null, count: number) {
   const numbers = (attribute ?? "").trim().split(/\s+/).map(Number);
   const reads = numbers.length === count && numbers.every(Number.isFinite);

   return reads ? numbers : null;
}

/* A point of the item's own graph: its window maps onto the plot box in the SVG's units, and the
   SVG's screen matrix takes it to the page. */
function graphPoint(anchor: Element, [x, y]: FigurePoint): FigurePoint | null {
   const plotWindow = numbersIn(anchor.getAttribute("data-agent-window"), 4);
   const plot = numbersIn(anchor.getAttribute("data-agent-plot"), 4);

   if (plotWindow === null || plot === null) {
      return null;
   }

   const [xMin, xMax, yMin, yMax] = plotWindow;
   const [left, top, right, bottom] = plot;
   const viewX = left + ((x - xMin) / (xMax - xMin)) * (right - left);
   const viewY = top + ((yMax - y) / (yMax - yMin)) * (bottom - top);
   const graphic = anchor as SVGGraphicsElement;
   const matrix = typeof graphic.getScreenCTM === "function" ? graphic.getScreenCTM() : null;

   if (matrix !== null) {
      return [matrix.a * viewX + matrix.c * viewY + matrix.e, matrix.b * viewX + matrix.d * viewY + matrix.f];
   }

   const viewBox = numbersIn(anchor.getAttribute("viewBox"), 4);

   if (viewBox === null) {
      return null;
   }

   const box = anchor.getBoundingClientRect();
   const [minX, minY, width, height] = viewBox;

   return [box.left + ((viewX - minX) / width) * box.width, box.top + ((viewY - minY) / height) * box.height];
}

function tableBoxes(anchor: Element, target: TutorMarkTarget): Box[] | null {
   const rows = Array.from(anchor.querySelectorAll("tbody tr"));
   const cellAt = (row: number, column: number) => rows[row]?.children[column] ?? null;

   if (target.cell !== null) {
      const cell = cellAt(target.cell[0], target.cell[1]);

      return cell === null ? null : [boxOf(cell.getBoundingClientRect())];
   }

   if (target.row !== null) {
      const row = rows[target.row];

      return row === undefined ? null : [boxOf(row.getBoundingClientRect())];
   }

   const cells = rows.map((row) => row.children[target.column as number]).filter((cell): cell is Element => cell !== undefined);

   return cells.length === 0 ? null : [unionOf(cells.map((cell) => boxOf(cell.getBoundingClientRect())))];
}

interface Located {
   boxes: Box[];
   point: FigurePoint | null;
}

function locate(target: TutorMarkTarget): Located | null {
   const anchor = anchorElement(target.anchor);

   if (anchor === null) {
      return null;
   }

   if (target.at !== null) {
      const point = graphPoint(anchor, target.at);

      return point === null ? null : { boxes: [{ left: point[0], top: point[1], right: point[0], bottom: point[1] }], point };
   }

   if (target.quote !== null) {
      const lines = quoteBoxes(anchor, target.quote);

      return lines === null ? null : { boxes: lines, point: null };
   }

   const namesPartOfTable = target.row !== null || target.column !== null || target.cell !== null;

   if (namesPartOfTable) {
      const parts = tableBoxes(anchor, target);

      return parts === null ? null : { boxes: parts, point: null };
   }

   return { boxes: [boxOf(anchor.getBoundingClientRect())], point: null };
}

function locateIfNamed(target: TutorMarkTarget | null | undefined) {
   return target === null || target === undefined ? null : locate(target);
}

function ellipseData([cx, cy]: FigurePoint, rx: number, ry: number) {
   const left = `${rounded(cx - rx)} ${rounded(cy)}`;
   const right = `${rounded(cx + rx)} ${rounded(cy)}`;
   const radii = `${rounded(rx)} ${rounded(ry)}`;

   return `M${left} A${radii} 0 1 0 ${right} A${radii} 0 1 0 ${left} Z`;
}

function bandData(box: Box) {
   const corners: FigurePoint[] = [
      [box.left - BAND_OVERHANG, box.top],
      [box.right + BAND_OVERHANG, box.top],
      [box.right + BAND_OVERHANG, box.bottom],
      [box.left - BAND_OVERHANG, box.bottom]
   ];

   return pathData(corners, true);
}

/* Where a line from inside a box towards a point leaves the box, a little clear of its edge. */
function edgeToward(located: Located, toward: FigurePoint): FigurePoint {
   const box = unionOf(located.boxes);
   const [fromX, fromY] = located.point ?? centreOf(box);
   const deltaX = toward[0] - fromX;
   const deltaY = toward[1] - fromY;
   const length = Math.hypot(deltaX, deltaY);

   if (length === 0) {
      return [fromX, fromY];
   }

   const halfWidth = (box.right - box.left) / 2;
   const halfHeight = (box.bottom - box.top) / 2;
   const exitX = deltaX === 0 ? Infinity : halfWidth / Math.abs(deltaX);
   const exitY = deltaY === 0 ? Infinity : halfHeight / Math.abs(deltaY);
   const exit = located.point !== null ? 0 : Math.min(exitX, exitY);
   const clearance = ARROW_CLEARANCE / length;
   const along = Math.min(exit + clearance, 1);

   return [fromX + deltaX * along, fromY + deltaY * along];
}

interface StrokeShape {
   d: string;
   points: FigurePoint[] | null;
   markers: boolean;
}

interface MarkDrawing {
   index: number;
   stepIndex: number;
   element: string;
   roleClass: RoleClass;
   strokes: StrokeShape[];
   bands: string[];
   dots: FigurePoint[];
   note: { anchor: Box; side: TutorMarkSide } | null;
}

function strokeLine(points: FigurePoint[], markers = true): StrokeShape {
   return { d: pathData(points, false), points, markers };
}

function drawingFor(mark: TutorMark, located: Located | null, ends: [Located, Located] | null, graphPoints: FigurePoint[] | null) {
   const strokes: StrokeShape[] = [];
   const bands: string[] = [];
   const dots: FigurePoint[] = [];
   let note: MarkDrawing["note"] = null;

   switch (mark.kind) {
      case "ring": {
         const box = unionOf(located!.boxes);
         const centre = located!.point ?? centreOf(box);
         const radiusX = located!.point !== null ? POINT_RING_RADIUS : (box.right - box.left) / 2 + RING_MARGIN;
         const radiusY = located!.point !== null ? POINT_RING_RADIUS : (box.bottom - box.top) / 2 + RING_MARGIN;

         strokes.push({ d: ellipseData(centre, radiusX, radiusY), points: null, markers: false });
         break;
      }
      case "underline":
         for (const line of located!.boxes) {
            strokes.push(strokeLine([[line.left, line.bottom + UNDERLINE_DROP], [line.right, line.bottom + UNDERLINE_DROP]]));
         }
         break;
      case "strike":
         for (const line of located!.boxes) {
            const middle = (line.top + line.bottom) / 2;

            strokes.push(strokeLine([[line.left, middle], [line.right, middle]]));
         }
         break;
      case "highlight":
         for (const part of located!.boxes) {
            bands.push(located!.point !== null ? ellipseData(located!.point, POINT_RING_RADIUS, POINT_RING_RADIUS) : bandData(part));
         }
         break;
      case "bracket": {
         const box = unionOf(located!.boxes);
         const isRight = mark.side === "right";
         const edge = isRight ? box.right + BRACKET_GAP : box.left - BRACKET_GAP;
         const hook = isRight ? edge - BRACKET_HOOK : edge + BRACKET_HOOK;

         strokes.push(strokeLine([[hook, box.top], [edge, box.top], [edge, box.bottom], [hook, box.bottom]], false));
         break;
      }
      case "note":
         note = { anchor: unionOf(located!.boxes), side: mark.side ?? "right" };
         break;
      case "arrow": {
         const [from, to] = ends!;
         const fromCentre = from.point ?? centreOf(unionOf(from.boxes));
         const toCentre = to.point ?? centreOf(unionOf(to.boxes));

         strokes.push(strokeLine([edgeToward(from, toCentre), edgeToward(to, fromCentre)]));
         break;
      }
      case "point":
         dots.push(graphPoints![0]);
         break;
      default:
         strokes.push(strokeLine(graphPoints!));
   }

   return { strokes, bands, dots, note };
}

interface MarksLayout {
   width: number;
   height: number;
   clipTop: number;
   clipBottom: number;
   drawings: MarkDrawing[];
}

/* The page bars the marks stay under: the top bar, and the tab bar fixed along the bottom of a phone
   screen. Measured, because both follow the layout. */
function clipInsets() {
   const header = document.querySelector(".app-header");
   const bar = document.querySelector(".app-nav");
   const barIsFixed = bar !== null && getComputedStyle(bar).position === "fixed";
   const top = header === null ? 0 : Math.max(0, header.getBoundingClientRect().bottom);
   const bottom = barIsFixed ? Math.max(0, window.innerHeight - bar.getBoundingClientRect().top) : 0;

   return { clipTop: top, clipBottom: bottom };
}

function measureMarks(spec: TutorMarksSpec, shown: number): MarksLayout {
   const stepIndex = new Map(spec.steps.map((step, index) => [step.id, index]));
   const drawings: MarkDrawing[] = [];

   spec.marks.forEach((mark, index) => {
      const presence: Presence = presenceOf(mark, stepIndex, shown);

      if (presence === "hidden") {
         return;
      }

      const located = locateIfNamed(mark.target);
      const fromLocated = locateIfNamed(mark.from);
      const toLocated = locateIfNamed(mark.to);
      const bothEndsFound = fromLocated !== null && toLocated !== null;
      const ends: [Located, Located] | null = bothEndsFound ? [fromLocated, toLocated] : null;
      const graph = anchorElement("item_figure");
      const graphSources = mark.kind === "point" ? [mark.at as FigurePoint] : mark.points ?? [];
      const mapped = graph === null ? [] : graphSources.map((point) => graphPoint(graph, point));
      const graphPoints = mapped.length > 0 && mapped.every((point) => point !== null) ? (mapped as FigurePoint[]) : null;

      const targetMissing = TARGETED_KINDS.includes(mark.kind) && located === null;
      const endMissing = mark.kind === "arrow" && ends === null;
      const needsGraph = mark.kind === "point" || GRAPH_KINDS.includes(mark.kind);
      const graphMissing = needsGraph && graphPoints === null;
      const isMissing = targetMissing || endMissing || graphMissing;

      if (isMissing) {
         return;
      }

      drawings.push({
         index,
         stepIndex: stepIndex.get(mark.step) ?? 0,
         element: mark.element,
         roleClass: roleClassOf(mark, presence),
         ...drawingFor(mark, located, ends, graphPoints)
      });
   });

   return { width: document.documentElement.clientWidth || window.innerWidth, height: window.innerHeight, ...clipInsets(), drawings };
}

function strokeClass(mark: TutorMark, roleClass: RoleClass) {
   const isGhost = roleClass === "ghost";

   return isGhost ? "tutor-figure-stroke tutor-figure-ghost" : `tutor-figure-stroke tutor-figure-${roleClass} tutor-figure-style-${mark.stroke.style} tutor-figure-weight-${mark.stroke.weight}`;
}

function arrowEnds(mark: TutorMark) {
   const arrow = mark.kind === "arrow" && mark.stroke.arrow === "none" ? "end" : mark.stroke.arrow;

   return { start: arrow === "start" || arrow === "both", end: arrow === "end" || arrow === "both" };
}

function placeNote(anchor: Box, side: TutorMarkSide, width: number, height: number, viewportWidth: number) {
   const [centreX, centreY] = centreOf(anchor);
   const placements: Record<TutorMarkSide, FigurePoint> = {
      right: [anchor.right + NOTE_GAP, centreY - height / 2],
      left: [anchor.left - NOTE_GAP - width, centreY - height / 2],
      above: [centreX - width / 2, anchor.top - NOTE_GAP - height],
      below: [centreX - width / 2, anchor.bottom + NOTE_GAP]
   };
   const [left, top] = placements[side];
   const rightmost = Math.max(VIEWPORT_MARGIN, viewportWidth - width - VIEWPORT_MARGIN);

   return { left: Math.min(Math.max(left, VIEWPORT_MARGIN), rightmost), top };
}

function Note(props: { mark: TutorMark; drawing: MarkDrawing; viewportWidth: number; motion: StepMotion; register: (index: number, element: HTMLDivElement | null) => void }) {
   const { mark, drawing, viewportWidth, register } = props;
   const element = useRef<HTMLDivElement | null>(null);
   const note = drawing.note!;

   useLayoutEffect(() => {
      const node = element.current;

      if (node === null) {
         return;
      }

      const size = node.getBoundingClientRect();
      const placed = placeNote(note.anchor, note.side, size.width, size.height, viewportWidth);

      node.style.left = `${rounded(placed.left)}px`;
      node.style.top = `${rounded(placed.top)}px`;
   });

   const motionClass = props.motion.isEntering ? ` ${FIGURE_STEP_CLASS}` : "";

   return (
      <div
         ref={(node) => {
            element.current = node;
            register(drawing.index, node);
         }}
         className={`page-marks-note tutor-figure-${drawing.roleClass}${motionClass}`}
         data-side={note.side}
         data-mark={mark.element}
         data-entering={props.motion.isFirstFrame ? "true" : undefined}
         data-testid="page-mark-note"
      >
         <MathText text={mark.text ?? ""} renderer="tutor" />
      </div>
   );
}

interface StepMotion {
   isEntering: boolean;
   isFirstFrame: boolean;
}

function motionOf(entering: EnteringSteps, stepIndex: number): StepMotion {
   const isEntering = stepIndex >= entering.from && stepIndex < entering.to;

   return { isEntering, isFirstFrame: isEntering && entering.isFirstFrame };
}

function WipeClip(props: { id: string; layout: MarksLayout; isFirstFrame: boolean }) {
   return (
      <clipPath id={props.id}>
         <rect
            className={FIGURE_WIPE_CLASS}
            x={0}
            y={0}
            width={props.layout.width}
            height={props.layout.height}
            data-entering={props.isFirstFrame ? "true" : undefined}
         />
      </clipPath>
   );
}

function StepLayer(props: { stepCount: number; entering: EnteringSteps; clipPrefix: string; layout: MarksLayout; draw: (drawing: MarkDrawing) => ReactNode }) {
   const { entering, layout, clipPrefix } = props;
   const groups = Array.from({ length: props.stepCount }, (_, stepIndex) => {
      const drawn = layout.drawings.filter((drawing) => drawing.stepIndex === stepIndex).map(props.draw).filter((node) => node !== null);
      const motion = motionOf(entering, stepIndex);

      if (drawn.length === 0) {
         return null;
      }

      const clipId = `${clipPrefix}-${stepIndex}`;

      return (
         <g key={stepIndex} className={motion.isEntering ? FIGURE_STEP_CLASS : undefined} data-step-index={stepIndex} data-entering={motion.isFirstFrame ? "true" : undefined}>
            {motion.isEntering ? (
               <defs>
                  <WipeClip id={clipId} layout={layout} isFirstFrame={motion.isFirstFrame} />
               </defs>
            ) : null}
            <g clipPath={motion.isEntering ? `url(#${clipId})` : undefined}>{drawn}</g>
         </g>
      );
   });

   return <>{groups}</>;
}

export interface PageMarksProps {
   spec: TutorMarksSpec;
   /* How many of the marks' steps are revealed. Steps revealed when the overlay mounts are drawn
      finished and without motion, which is how a screen's marks come back when the student returns
      to it. */
   revealed: number;
}

export function PageMarks({ spec, revealed }: PageMarksProps) {
   const uid = useId().replace(/:/g, "");
   const shown = Math.min(Math.max(Math.floor(revealed), 0), spec.steps.length);
   const entering = useEnteringSteps(shown);
   const [layout, setLayout] = useState<MarksLayout | null>(null);
   const layers = useRef<Array<HTMLDivElement | null>>([]);
   const notes = useRef(new Map<number, HTMLDivElement>());
   const frame = useRef<number | null>(null);
   const lastLayout = useRef("");

   const remeasure = useCallback(() => {
      const next = measureMarks(spec, shown);
      const serialised = JSON.stringify(next);

      if (serialised === lastLayout.current) {
         return;
      }

      lastLayout.current = serialised;
      setLayout(next);
   }, [spec, shown]);

   useLayoutEffect(() => {
      remeasure();
   }, [remeasure]);

   /* Scrolling anywhere, a resize, or a change in the size of the page, an anchor or a note moves
      what the marks sit on, so each is measured again in the next frame. */
   useEffect(() => {
      function scheduleMeasure() {
         if (frame.current !== null) {
            return;
         }

         frame.current = requestAnimationFrame(() => {
            frame.current = null;
            remeasure();
         });
      }

      window.addEventListener("scroll", scheduleMeasure, true);
      window.addEventListener("resize", scheduleMeasure);

      const canObserve = typeof ResizeObserver === "function";
      const observer = canObserve ? new ResizeObserver(scheduleMeasure) : null;
      const watched = [document.getElementById("main") ?? document.body, ...Array.from(document.querySelectorAll("[data-agent-anchor]")), ...notes.current.values()];

      watched.forEach((element) => observer?.observe(element));

      return () => {
         window.removeEventListener("scroll", scheduleMeasure, true);
         window.removeEventListener("resize", scheduleMeasure);
         observer?.disconnect();

         if (frame.current !== null) {
            cancelAnimationFrame(frame.current);
            frame.current = null;
         }
      };
   }, [remeasure, layout]);

   useLayoutEffect(() => {
      if (layout === null) {
         return;
      }

      for (const layer of layers.current) {
         const drawing = layer?.querySelector("svg");

         layer?.style.setProperty("clip-path", `inset(${rounded(layout.clipTop)}px 0 ${rounded(layout.clipBottom)}px 0)`);
         drawing?.style.setProperty("width", `${rounded(layout.width)}px`);
         drawing?.style.setProperty("height", `${rounded(layout.height)}px`);
      }
   }, [layout]);

   const registerNote = useCallback((index: number, element: HTMLDivElement | null) => {
      if (element === null) {
         notes.current.delete(index);
      } else {
         notes.current.set(index, element);
      }
   }, []);

   const hasArrows = useMemo(() => spec.marks.some((mark) => arrowEnds(mark).start || arrowEnds(mark).end), [spec]);

   if (layout === null) {
      return null;
   }

   function drawStrokes(drawing: MarkDrawing) {
      const mark = spec.marks[drawing.index];
      const ends = arrowEnds(mark);
      const marker = `url(#${uid}-arrow-${drawing.roleClass})`;
      const paths = drawing.strokes.map((stroke, index) => (
         <path
            key={`stroke${index}`}
            className={strokeClass(mark, drawing.roleClass)}
            d={stroke.d}
            markerStart={stroke.markers && ends.start ? marker : undefined}
            markerEnd={stroke.markers && ends.end ? marker : undefined}
            data-mark={drawing.element}
         />
      ));
      const isGhostBand = drawing.roleClass === "ghost" && drawing.bands.length > 0;
      const isWrongHighlight = mark.kind === "highlight" && drawing.roleClass === "error";
      const showsOutline = isGhostBand || isWrongHighlight;
      const outlines = showsOutline
         ? drawing.bands.map((band, index) => <path key={`outline${index}`} className={strokeClass(mark, drawing.roleClass)} d={band} data-mark={drawing.element} />)
         : [];
      const dots = drawing.dots.map(([cx, cy], index) => (
         <circle
            key={`dot${index}`}
            className={`tutor-figure-dot tutor-figure-${drawing.roleClass}${mark.open ? " tutor-figure-dot-open" : ""}`}
            cx={rounded(cx)}
            cy={rounded(cy)}
            data-mark={drawing.element}
         />
      ));
      const all = [...paths, ...outlines, ...dots];

      return all.length === 0 ? null : <g key={drawing.index}>{all}</g>;
   }

   function drawBands(drawing: MarkDrawing) {
      const mark = spec.marks[drawing.index];
      const isGhost = drawing.roleClass === "ghost";
      const hasUnderlay = mark.stroke.highlighter && !isGhost;
      const underlays = hasUnderlay ? drawing.strokes.filter((stroke) => stroke.points !== null).map((stroke) => highlighterData(stroke.points!, false)) : [];
      const bands = isGhost ? [] : [...drawing.bands, ...underlays];

      if (bands.length === 0) {
         return null;
      }

      return (
         <g key={drawing.index}>
            {bands.map((band, index) => (
               <path key={index} className="tutor-figure-highlighter" d={band} data-mark={drawing.element} />
            ))}
         </g>
      );
   }

   return (
      <>
         <div className="page-marks page-marks-highlights" aria-hidden="true" ref={(node) => (layers.current[0] = node)} data-testid="page-marks-highlights">
            <svg className="page-marks-svg">
               <StepLayer stepCount={spec.steps.length} entering={entering} clipPrefix={`${uid}-band`} layout={layout} draw={drawBands} />
            </svg>
         </div>

         <div className="page-marks" aria-hidden="true" ref={(node) => (layers.current[1] = node)} data-testid="page-marks">
            <svg className="page-marks-svg">
               {hasArrows ? (
                  <defs>
                     {ARROWHEAD_ROLES.map((roleClass) => (
                        <marker
                           key={roleClass}
                           id={`${uid}-arrow-${roleClass}`}
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
                     ))}
                  </defs>
               ) : null}

               <StepLayer stepCount={spec.steps.length} entering={entering} clipPrefix={`${uid}-mark`} layout={layout} draw={drawStrokes} />
            </svg>

            {layout.drawings
               .filter((drawing) => drawing.note !== null)
               .map((drawing) => (
                  <Note
                     key={drawing.index}
                     mark={spec.marks[drawing.index]}
                     drawing={drawing}
                     viewportWidth={layout.width}
                     motion={motionOf(entering, drawing.stepIndex)}
                     register={registerNote}
                  />
               ))}
         </div>
      </>
   );
}
