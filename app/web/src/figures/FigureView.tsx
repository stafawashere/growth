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

const POINT_RADIUS = 4;

const DASH_PATTERN = "6 4";

const CURVE_STROKE_WIDTH = 2;

const MARK_STROKE_WIDTH = 1.5;

const FILL_OPACITY = 0.5;

const labelText = {
   fill: "var(--growth-text-primary)",
   fontSize: "var(--growth-type-caption)"
};

const tableCell = {
   border: "1px solid var(--growth-border-hairline)",
   padding: "var(--growth-space-4) var(--growth-space-8)",
   textAlign: "center" as const
};

const axisTitleText = {
   fill: "var(--growth-text-secondary)",
   fontSize: "var(--growth-type-caption)",
   fontStyle: "italic"
};

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

function GraphFigure({ spec }: { spec: GraphFigureSpec }) {
   const [xMin, xMax] = spec.domain;
   const [yMin, yMax] = spec.range;
   const plotHeight = plotHeightFor(spec);
   const viewHeight = plotHeight + PLOT_PADDING * 2;

   const viewX = (x: number) => PLOT_PADDING + ((x - xMin) / (xMax - xMin)) * PLOT_WIDTH;
   const viewY = (y: number) => PLOT_PADDING + ((yMax - y) / (yMax - yMin)) * plotHeight;
   const toView = (point: FigurePoint): FigurePoint => [viewX(point[0]), viewY(point[1])];

   const left = viewX(xMin);
   const right = viewX(xMax);
   const top = viewY(yMax);
   const bottom = viewY(yMin);

   const showsXAxis = yMin <= 0 && 0 <= yMax;
   const showsYAxis = xMin <= 0 && 0 <= xMax;
   const xAxisY = showsXAxis ? viewY(0) : bottom;
   const yAxisX = showsYAxis ? viewX(0) : left;
   const [xTitle, yTitle] = spec.axis_titles;

   return (
      <svg
         role="img"
         aria-label={spec.alt}
         viewBox={`0 0 ${VIEW_WIDTH} ${viewHeight}`}
         width="100%"
         style={{ display: "block", maxWidth: VIEW_WIDTH, height: "auto" }}
         data-testid="figure-graph"
         data-kind={spec.kind}
      >
         {spec.gridlines ? (
            <g stroke="var(--growth-border-hairline)" strokeWidth={1} data-testid="figure-gridlines">
               {gridValues(xMin, xMax).map((x) => (
                  <line key={`x${x}`} x1={viewX(x)} x2={viewX(x)} y1={top} y2={bottom} />
               ))}
               {gridValues(yMin, yMax).map((y) => (
                  <line key={`y${y}`} x1={left} x2={right} y1={viewY(y)} y2={viewY(y)} />
               ))}
            </g>
         ) : null}

         <g stroke="var(--growth-text-secondary)" strokeWidth={1}>
            {showsXAxis ? <line x1={left} x2={right} y1={xAxisY} y2={xAxisY} data-testid="figure-x-axis" /> : null}
            {showsYAxis ? <line x1={yAxisX} x2={yAxisX} y1={top} y2={bottom} data-testid="figure-y-axis" /> : null}
         </g>

         {spec.fills.map((fill, index) => (
            <polygon
               key={`fill${index}`}
               points={pointList(fill.points, toView)}
               fill="var(--growth-accent-tint-2)"
               fillOpacity={FILL_OPACITY}
               stroke="none"
            />
         ))}

         {spec.curves.map((curve, curveIndex) =>
            curve.segments.map((segment, segmentIndex) => (
               <polyline
                  key={`curve${curveIndex}-${segmentIndex}`}
                  points={pointList(segment, toView)}
                  fill="none"
                  stroke="var(--growth-accent-base)"
                  strokeWidth={CURVE_STROKE_WIDTH}
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
                     x1={viewX(mark.from[0])}
                     y1={viewY(mark.from[1])}
                     x2={viewX(mark.to[0])}
                     y2={viewY(mark.to[1])}
                     stroke="var(--growth-text-primary)"
                     strokeWidth={MARK_STROKE_WIDTH}
                     strokeDasharray={isDashed ? DASH_PATTERN : undefined}
                  />
               );
            }

            const isOpen = mark.type === "open_point";

            return (
               <circle
                  key={`mark${index}`}
                  cx={viewX(mark.at[0])}
                  cy={viewY(mark.at[1])}
                  r={POINT_RADIUS}
                  fill={isOpen ? "var(--growth-surface-raised)" : "var(--growth-text-primary)"}
                  stroke="var(--growth-text-primary)"
                  strokeWidth={MARK_STROKE_WIDTH}
                  data-mark={mark.type}
               />
            );
         })}

         {spec.labels.map((label, index) => (
            <text
               key={`label${index}`}
               x={viewX(label.anchor[0])}
               y={viewY(label.anchor[1])}
               style={labelText}
               data-testid="figure-label"
            >
               {withoutMathDelimiters(label.text)}
            </text>
         ))}

         {xTitle ? (
            <text x={right - 4} y={xAxisY - 6} textAnchor="end" style={axisTitleText}>
               {xTitle}
            </text>
         ) : null}

         {yTitle ? (
            <text x={yAxisX + 6} y={top + 14} textAnchor="start" style={axisTitleText}>
               {yTitle}
            </text>
         ) : null}
      </svg>
   );
}

function TableFigure({ spec }: { spec: TableFigureSpec }) {
   return (
      <table className="figure-table" data-testid="figure-table" style={{ borderCollapse: "collapse" }}>
         <caption className="visually-hidden">{spec.alt}</caption>
         <thead>
            <tr>
               {spec.columns.map((column, index) => (
                  <th key={index} scope="col" style={tableCell}>
                     <MathText text={column} />
                  </th>
               ))}
            </tr>
         </thead>
         <tbody>
            {spec.rows.map((row, rowIndex) => (
               <tr key={rowIndex}>
                  {row.map((cell, cellIndex) => (
                     <td key={cellIndex} style={tableCell}>
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
      <div className="item-figure" data-testid="item-figure" style={{ maxWidth: VIEW_WIDTH }}>
         {figure.kind === "table" ? <TableFigure spec={figure} /> : <GraphFigure spec={figure} />}
      </div>
   );
}
