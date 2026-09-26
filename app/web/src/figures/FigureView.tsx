import type {
   FigureLabel,
   FigureMark,
   FigurePoint,
   FigureSpec,
   GraphFigureKind,
   GraphFigureSpec,
   TableFigureSpec
} from "../api/types";
import { MathText } from "../math/MathText";

/* Draws the declarative figure spec app/generation/kit.py builds (prompts/generator/
   figure_spec_v1.md). The spec arrives from the server as JSON, so it is checked here before
   anything is drawn, and a spec that does not check out draws nothing rather than half a figure.
   Every label sits inside the plot at its anchor; there is no caption and no legend. */

export interface FigureViewProps {
   spec: unknown;
}

const GRAPH_KINDS: GraphFigureKind[] = [
   "function_graph",
   "region",
   "parametric_curve",
   "polar_curve",
   "vector_diagram",
   "number_line",
   "slope_field",
   "geometric_diagram"
];

export const VIEW_WIDTH = 480;

export const PLOT_PADDING = 20;

const PLOT_WIDTH = VIEW_WIDTH - PLOT_PADDING * 2;

const MINIMUM_PLOT_HEIGHT = 180;

const MAXIMUM_PLOT_HEIGHT = PLOT_WIDTH;

const MAXIMUM_GRIDLINES_PER_AXIS = 16;

const GRID_STEPS = [0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000];

/* Where text sits relative to the line it labels, and how much room a line of caption text takes,
   in the plot's own units. These place and space text inside the drawing; its size and colour come
   from the figure classes in app.css. */
const TEXT_GAP = 4;

const TICK_LABEL_OFFSET = 14;

const AXIS_TITLE_OFFSET = 6;

const AXIS_TITLE_DROP = 14;

const CAPTION_CHARACTER_WIDTH = 8;

const CAPTION_LINE_HEIGHT = 14;

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

function isArrayOf<T>(value: unknown, check: (entry: unknown) => entry is T): value is T[] {
   return Array.isArray(value) && value.every(check);
}

function isStringArray(value: unknown): value is string[] {
   return isArrayOf(value, (entry): entry is string => typeof entry === "string");
}

function isPolyline(value: unknown): value is FigurePoint[] {
   return isArrayOf(value, isPoint);
}

function isCurve(value: unknown): value is GraphFigureSpec["curves"][number] {
   return isRecord(value) && isArrayOf(value.segments, isPolyline);
}

function isFill(value: unknown): value is GraphFigureSpec["fills"][number] {
   return isRecord(value) && isPolyline(value.points);
}

function isMark(value: unknown): value is FigureMark {
   if (!isRecord(value)) {
      return false;
   }

   const isPointMark = value.type === "point" || value.type === "open_point";

   if (isPointMark) {
      return isPoint(value.at);
   }

   const isSegmentMark = value.type === "segment";
   const hasEnds = isPoint(value.from) && isPoint(value.to);
   const hasKnownStyle = value.style === undefined || value.style === "solid" || value.style === "dashed";

   return isSegmentMark && hasEnds && hasKnownStyle;
}

function isLabel(value: unknown): value is FigureLabel {
   return isRecord(value) && typeof value.text === "string" && isPoint(value.anchor);
}

function optionalArray<T>(value: unknown, check: (entry: unknown) => entry is T): T[] | null {
   if (value === undefined) {
      return [];
   }

   return isArrayOf(value, check) ? value : null;
}

function asGraphSpec(value: Record<string, unknown>): GraphFigureSpec | null {
   const kind = value.kind as GraphFigureKind;
   const hasWindow = isInterval(value.domain) && isInterval(value.range);

   if (!hasWindow) {
      return null;
   }

   const curves = optionalArray(value.curves, isCurve);
   const fills = optionalArray(value.fills, isFill);
   const marks = optionalArray(value.marks, isMark);
   const labels = optionalArray(value.labels, isLabel);
   const axisTitles = optionalArray(value.axis_titles, (entry): entry is string => typeof entry === "string");
   const hasMembers = curves !== null && fills !== null && marks !== null && labels !== null;

   if (!hasMembers || axisTitles === null) {
      return null;
   }

   return {
      kind,
      domain: value.domain as [number, number],
      range: value.range as [number, number],
      curves,
      fills,
      marks,
      labels,
      gridlines: value.gridlines === true,
      axis_titles: axisTitles,
      alt: typeof value.alt === "string" ? value.alt : ""
   };
}

function asTableSpec(value: Record<string, unknown>): TableFigureSpec | null {
   const hasColumns = isStringArray(value.columns) && value.columns.length > 0;
   const hasRows = isArrayOf(value.rows, isStringArray);

   if (!hasColumns || !hasRows) {
      return null;
   }

   return {
      kind: "table",
      columns: value.columns as string[],
      rows: value.rows as string[][],
      labels: [],
      alt: typeof value.alt === "string" ? value.alt : ""
   };
}

export function parseFigureSpec(value: unknown): FigureSpec | null {
   if (!isRecord(value)) {
      return null;
   }

   if (value.kind === "table") {
      return asTableSpec(value);
   }

   const isGraphKind = GRAPH_KINDS.includes(value.kind as GraphFigureKind);

   return isGraphKind ? asGraphSpec(value) : null;
}

export function gridStep(span: number) {
   for (const step of GRID_STEPS) {
      const lineCount = span / step;

      if (lineCount <= MAXIMUM_GRIDLINES_PER_AXIS) {
         return step;
      }
   }

   return GRID_STEPS[GRID_STEPS.length - 1];
}

function gridValues(low: number, high: number) {
   const step = gridStep(high - low);
   const values: number[] = [];

   for (let value = Math.ceil(low / step) * step; value <= high; value += step) {
      values.push(value);
   }

   return values;
}

function withoutMathDelimiters(text: string) {
   return text.replace(/\\\(|\\\)/g, "").trim();
}

function plotHeightFor(spec: GraphFigureSpec) {
   const domainSpan = spec.domain[1] - spec.domain[0];
   const rangeSpan = spec.range[1] - spec.range[0];
   const equalScaleHeight = PLOT_WIDTH * (rangeSpan / domainSpan);

   return Math.min(MAXIMUM_PLOT_HEIGHT, Math.max(MINIMUM_PLOT_HEIGHT, equalScaleHeight));
}

function pointList(points: FigurePoint[], toView: (point: FigurePoint) => FigurePoint) {
   return points
      .map((point) => {
         const [viewX, viewY] = toView(point);

         return `${viewX},${viewY}`;
      })
      .join(" ");
}

type TextAnchor = "start" | "middle" | "end";

type TextBaseline = "auto" | "middle";

interface TextBox {
   left: number;
   right: number;
   top: number;
   bottom: number;
}

export interface TickLabel {
   axis: "x" | "y";
   text: string;
   x: number;
   y: number;
   anchor: TextAnchor;
   baseline: TextBaseline;
}

export function tickText(value: number) {
   return String(Number(value.toFixed(6)) + 0);
}

function textBox(x: number, y: number, text: string, anchor: TextAnchor, baseline: TextBaseline): TextBox {
   const width = text.length * CAPTION_CHARACTER_WIDTH;
   const leftByAnchor = { start: x, middle: x - width / 2, end: x - width };
   const top = baseline === "middle" ? y - CAPTION_LINE_HEIGHT / 2 : y - CAPTION_LINE_HEIGHT;

   return { left: leftByAnchor[anchor], right: leftByAnchor[anchor] + width, top, bottom: top + CAPTION_LINE_HEIGHT };
}

function boxesOverlap(first: TextBox, second: TextBox) {
   const apartHorizontally = first.right <= second.left || second.right <= first.left;
   const apartVertically = first.bottom <= second.top || second.bottom <= first.top;

   return !apartHorizontally && !apartVertically;
}

interface GraphLayout {
   viewX: (x: number) => number;
   viewY: (y: number) => number;
   left: number;
   top: number;
   xAxisY: number;
   yAxisX: number;
   showsXAxis: boolean;
   showsYAxis: boolean;
}

function layoutFor(spec: GraphFigureSpec): GraphLayout & { right: number; bottom: number; viewHeight: number } {
   const [xMin, xMax] = spec.domain;
   const [yMin, yMax] = spec.range;
   const plotHeight = plotHeightFor(spec);

   const viewX = (x: number) => PLOT_PADDING + ((x - xMin) / (xMax - xMin)) * PLOT_WIDTH;
   const viewY = (y: number) => PLOT_PADDING + ((yMax - y) / (yMax - yMin)) * plotHeight;

   const left = viewX(xMin);
   const bottom = viewY(yMin);
   const showsXAxis = yMin <= 0 && 0 <= yMax;
   const showsYAxis = xMin <= 0 && 0 <= xMax;

   return {
      viewX,
      viewY,
      left,
      right: viewX(xMax),
      top: viewY(yMax),
      bottom,
      viewHeight: plotHeight + PLOT_PADDING * 2,
      xAxisY: showsXAxis ? viewY(0) : bottom,
      yAxisX: showsYAxis ? viewX(0) : left,
      showsXAxis,
      showsYAxis
   };
}

function axisTitleBoxes(spec: GraphFigureSpec, layout: GraphLayout & { right: number }) {
   const [xTitle, yTitle] = spec.axis_titles;
   const boxes: TextBox[] = [];

   if (xTitle) {
      boxes.push(textBox(layout.right - TEXT_GAP, layout.xAxisY - AXIS_TITLE_OFFSET, xTitle, "end", "auto"));
   }

   if (yTitle) {
      boxes.push(textBox(layout.yAxisX + AXIS_TITLE_OFFSET, layout.top + AXIS_TITLE_DROP, yTitle, "start", "auto"));
   }

   return boxes;
}

/* A number at every gridline on both axes, so a value can be read off the graph rather than
   counted in grid squares. A tick label is left out where it would sit across the other axis or
   over a label or axis title already in the figure, and the y labels move to the right of the axis
   when the left side has no room inside the drawing. */
export function tickLabelsFor(spec: GraphFigureSpec): TickLabel[] {
   const layout = layoutFor(spec);
   const taken = [
      ...spec.labels.map((label) =>
         textBox(
            layout.viewX(label.anchor[0]),
            layout.viewY(label.anchor[1]),
            withoutMathDelimiters(label.text),
            "start",
            "auto"
         )
      ),
      ...axisTitleBoxes(spec, layout)
   ];
   const ticks: TickLabel[] = [];

   function place(candidate: TickLabel) {
      const box = textBox(candidate.x, candidate.y, candidate.text, candidate.anchor, candidate.baseline);
      const crossesYAxis = layout.showsYAxis && box.left < layout.yAxisX && layout.yAxisX < box.right;
      const crossesXAxis = layout.showsXAxis && box.top < layout.xAxisY && layout.xAxisY < box.bottom;
      const coversText = taken.some((other) => boxesOverlap(box, other));
      const collides = crossesYAxis || crossesXAxis || coversText;

      if (collides) {
         return;
      }

      taken.push(box);
      ticks.push(candidate);
   }

   for (const x of gridValues(spec.domain[0], spec.domain[1])) {
      place({
         axis: "x",
         text: tickText(x),
         x: layout.viewX(x),
         y: layout.xAxisY + TICK_LABEL_OFFSET,
         anchor: "middle",
         baseline: "auto"
      });
   }

   for (const y of gridValues(spec.range[0], spec.range[1])) {
      const text = tickText(y);
      const leftSideStart = layout.yAxisX - TEXT_GAP - text.length * CAPTION_CHARACTER_WIDTH;
      const fitsOnTheLeft = leftSideStart >= 0;

      place({
         axis: "y",
         text,
         x: fitsOnTheLeft ? layout.yAxisX - TEXT_GAP : layout.yAxisX + TEXT_GAP,
         y: layout.viewY(y),
         anchor: fitsOnTheLeft ? "end" : "start",
         baseline: "middle"
      });
   }

   return ticks;
}

function GraphFigure({ spec }: { spec: GraphFigureSpec }) {
   const layout = layoutFor(spec);
   const { viewX, viewY, left, right, top, bottom, xAxisY, yAxisX, showsXAxis, showsYAxis, viewHeight } = layout;
   const toView = (point: FigurePoint): FigurePoint => [viewX(point[0]), viewY(point[1])];
   const [xTitle, yTitle] = spec.axis_titles;

   return (
      <svg
         role="img"
         aria-label={spec.alt}
         viewBox={`0 0 ${VIEW_WIDTH} ${viewHeight}`}
         className="figure-graph"
         data-testid="figure-graph"
         data-kind={spec.kind}
      >
         {spec.fills.map((fill, index) => (
            <polygon key={`fill${index}`} className="figure-region" points={pointList(fill.points, toView)} stroke="none" />
         ))}

         {spec.gridlines ? (
            <g className="figure-gridlines" stroke="var(--growth-border-hairline)" data-testid="figure-gridlines">
               {gridValues(spec.domain[0], spec.domain[1]).map((x) => (
                  <line key={`x${x}`} x1={viewX(x)} x2={viewX(x)} y1={top} y2={bottom} />
               ))}
               {gridValues(spec.range[0], spec.range[1]).map((y) => (
                  <line key={`y${y}`} x1={left} x2={right} y1={viewY(y)} y2={viewY(y)} />
               ))}
            </g>
         ) : null}

         <g className="figure-axes" stroke="var(--growth-text-secondary)">
            {showsXAxis ? <line x1={left} x2={right} y1={xAxisY} y2={xAxisY} data-testid="figure-x-axis" /> : null}
            {showsYAxis ? <line x1={yAxisX} x2={yAxisX} y1={top} y2={bottom} data-testid="figure-y-axis" /> : null}
         </g>

         {spec.curves.map((curve, curveIndex) =>
            curve.segments.map((segment, segmentIndex) => (
               <polyline
                  key={`curve${curveIndex}-${segmentIndex}`}
                  className="figure-curve"
                  points={pointList(segment, toView)}
                  fill="none"
                  stroke="var(--growth-accent-base)"
                  strokeLinejoin="round"
                  strokeLinecap="round"
               />
            ))
         )}

         {spec.marks.map((mark, index) => {
            if (mark.type === "segment") {
               const isDashed = mark.style === "dashed";

               return (
                  <line
                     key={`mark${index}`}
                     className={isDashed ? "figure-mark figure-mark-dashed" : "figure-mark"}
                     x1={viewX(mark.from[0])}
                     y1={viewY(mark.from[1])}
                     x2={viewX(mark.to[0])}
                     y2={viewY(mark.to[1])}
                     stroke="var(--growth-text-primary)"
                  />
               );
            }

            const isOpen = mark.type === "open_point";

            return (
               <circle
                  key={`mark${index}`}
                  className="figure-mark figure-point"
                  cx={viewX(mark.at[0])}
                  cy={viewY(mark.at[1])}
                  fill={isOpen ? "var(--growth-surface-raised)" : "var(--growth-text-primary)"}
                  stroke="var(--growth-text-primary)"
                  data-mark={mark.type}
               />
            );
         })}

         {spec.gridlines ? (
            <g data-testid="figure-ticks">
               {tickLabelsFor(spec).map((tick) => (
                  <text
                     key={`${tick.axis}${tick.text}`}
                     className="figure-tick"
                     x={tick.x}
                     y={tick.y}
                     textAnchor={tick.anchor}
                     dominantBaseline={tick.baseline}
                     data-axis={tick.axis}
                  >
                     {tick.text}
                  </text>
               ))}
            </g>
         ) : null}

         {spec.labels.map((label, index) => (
            <text
               key={`label${index}`}
               className="figure-label"
               x={viewX(label.anchor[0])}
               y={viewY(label.anchor[1])}
               data-testid="figure-label"
            >
               {withoutMathDelimiters(label.text)}
            </text>
         ))}

         {xTitle ? (
            <text className="figure-axis-title" x={right - TEXT_GAP} y={xAxisY - AXIS_TITLE_OFFSET} textAnchor="end">
               {xTitle}
            </text>
         ) : null}

         {yTitle ? (
            <text className="figure-axis-title" x={yAxisX + AXIS_TITLE_OFFSET} y={top + AXIS_TITLE_DROP} textAnchor="start">
               {yTitle}
            </text>
         ) : null}
      </svg>
   );
}

function TableFigure({ spec }: { spec: TableFigureSpec }) {
   return (
      <table className="figure-table" data-testid="figure-table">
         <caption className="visually-hidden">{spec.alt}</caption>
         <thead>
            <tr>
               {spec.columns.map((column, index) => (
                  <th key={index} scope="col">
                     <MathText text={column} />
                  </th>
               ))}
            </tr>
         </thead>
         <tbody>
            {spec.rows.map((row, rowIndex) => (
               <tr key={rowIndex}>
                  {row.map((cell, cellIndex) => (
                     <td key={cellIndex}>
                        <MathText text={cell} />
                     </td>
                  ))}
               </tr>
            ))}
         </tbody>
      </table>
   );
}

export function FigureView({ spec }: FigureViewProps) {
   const figure = parseFigureSpec(spec);

   if (figure === null) {
      return null;
   }

   return (
      <div className="item-figure" data-testid="item-figure">
         {figure.kind === "table" ? <TableFigure spec={figure} /> : <GraphFigure spec={figure} />}
      </div>
   );
}
