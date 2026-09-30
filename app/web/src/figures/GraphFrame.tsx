/* The frame of a graph: gridlines, axes, a number at every gridline and the axis titles, laid out
   for a window drawn into a view of a given width. The item figure (FigureView, 480 units wide)
   and the tutor's figure (TutorFigure, the width the server chose) share it, so a value is read off
   either one the same way. */

export interface FrameWindow {
   domain: [number, number];
   range: [number, number];
}

export interface GraphLayout {
   viewWidth: number;
   viewHeight: number;
   viewX: (x: number) => number;
   viewY: (y: number) => number;
   left: number;
   right: number;
   top: number;
   bottom: number;
   xAxisY: number;
   yAxisX: number;
   showsXAxis: boolean;
   showsYAxis: boolean;
}

const MAXIMUM_GRIDLINES_PER_AXIS = 16;

const GRID_STEPS = [0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000];

/* Where text sits relative to the line it labels, and how much room a line of caption text takes,
   in the plot's own units. These place and space text inside the drawing; its size and colour come
   from the figure classes in app.css. */
export const TEXT_GAP = 4;

const TICK_LABEL_OFFSET = 14;

const AXIS_TITLE_OFFSET = 6;

const AXIS_TITLE_DROP = 14;

export const CAPTION_CHARACTER_WIDTH = 8;

export const CAPTION_LINE_HEIGHT = 14;

export type TextAnchor = "start" | "middle" | "end";

type TextBaseline = "auto" | "middle";

export interface TextBox {
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

export function gridStep(span: number) {
   for (const step of GRID_STEPS) {
      const lineCount = span / step;

      if (lineCount <= MAXIMUM_GRIDLINES_PER_AXIS) {
         return step;
      }
   }

   return GRID_STEPS[GRID_STEPS.length - 1];
}

export function gridValues(low: number, high: number) {
   const step = gridStep(high - low);
   const values: number[] = [];

   for (let value = Math.ceil(low / step) * step; value <= high; value += step) {
      values.push(value);
   }

   return values;
}

export function withoutMathDelimiters(text: string) {
   return text.replace(/\\\(|\\\)/g, "").trim();
}

export function tickText(value: number) {
   return String(Number(value.toFixed(6)) + 0);
}

export function textBox(x: number, y: number, text: string, anchor: TextAnchor, baseline: TextBaseline): TextBox {
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

/* The window maps onto the plot, which is the view less its padding on every side: x across the
   plot's width and y, flipped so larger values sit higher, down its height. */
export function graphLayout(plotWindow: FrameWindow, viewWidth: number, padding: number, plotHeight: number): GraphLayout {
   const [xMin, xMax] = plotWindow.domain;
   const [yMin, yMax] = plotWindow.range;
   const plotWidth = viewWidth - padding * 2;

   const viewX = (x: number) => padding + ((x - xMin) / (xMax - xMin)) * plotWidth;
   const viewY = (y: number) => padding + ((yMax - y) / (yMax - yMin)) * plotHeight;

   const left = viewX(xMin);
   const bottom = viewY(yMin);
   const showsXAxis = yMin <= 0 && 0 <= yMax;
   const showsYAxis = xMin <= 0 && 0 <= xMax;

   return {
      viewWidth,
      viewHeight: plotHeight + padding * 2,
      viewX,
      viewY,
      left,
      right: viewX(xMax),
      top: viewY(yMax),
      bottom,
      xAxisY: showsXAxis ? viewY(0) : bottom,
      yAxisX: showsYAxis ? viewX(0) : left,
      showsXAxis,
      showsYAxis
   };
}

function axisTitleBoxes(axisTitles: string[], layout: GraphLayout) {
   const [xTitle, yTitle] = axisTitles;
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
export function frameTickLabels(plotWindow: FrameWindow, layout: GraphLayout, axisTitles: string[], labelBoxes: TextBox[]): TickLabel[] {
   const taken = [...labelBoxes, ...axisTitleBoxes(axisTitles, layout)];
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

   for (const x of gridValues(plotWindow.domain[0], plotWindow.domain[1])) {
      place({
         axis: "x",
         text: tickText(x),
         x: layout.viewX(x),
         y: layout.xAxisY + TICK_LABEL_OFFSET,
         anchor: "middle",
         baseline: "auto"
      });
   }

   for (const y of gridValues(plotWindow.range[0], plotWindow.range[1])) {
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

export function FrameGridlines(props: { plotWindow: FrameWindow; layout: GraphLayout }) {
   const { plotWindow, layout } = props;

   return (
      <g className="figure-gridlines" stroke="var(--growth-border-hairline)" data-testid="figure-gridlines">
         {gridValues(plotWindow.domain[0], plotWindow.domain[1]).map((x) => (
            <line key={`x${x}`} x1={layout.viewX(x)} x2={layout.viewX(x)} y1={layout.top} y2={layout.bottom} />
         ))}
         {gridValues(plotWindow.range[0], plotWindow.range[1]).map((y) => (
            <line key={`y${y}`} x1={layout.left} x2={layout.right} y1={layout.viewY(y)} y2={layout.viewY(y)} />
         ))}
      </g>
   );
}

export function FrameAxes(props: { layout: GraphLayout }) {
   const { left, right, top, bottom, xAxisY, yAxisX, showsXAxis, showsYAxis } = props.layout;

   return (
      <g className="figure-axes" stroke="var(--growth-text-secondary)">
         {showsXAxis ? <line x1={left} x2={right} y1={xAxisY} y2={xAxisY} data-testid="figure-x-axis" /> : null}
         {showsYAxis ? <line x1={yAxisX} x2={yAxisX} y1={top} y2={bottom} data-testid="figure-y-axis" /> : null}
      </g>
   );
}

export function FrameTicks(props: { ticks: TickLabel[] }) {
   return (
      <g data-testid="figure-ticks">
         {props.ticks.map((tick) => (
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
   );
}

export function FrameAxisTitles(props: { layout: GraphLayout; axisTitles: string[] }) {
   const { right, top, xAxisY, yAxisX } = props.layout;
   const [xTitle, yTitle] = props.axisTitles;

   return (
      <>
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
      </>
   );
}

export interface GraphFrameProps {
   plotWindow: FrameWindow;
   layout: GraphLayout;
   gridlines: boolean;
   axisTitles: string[];
   labelBoxes: TextBox[];
}

/* The whole frame in one piece, for a drawing whose marks all sit above it. */
export function GraphFrame({ plotWindow, layout, gridlines, axisTitles, labelBoxes }: GraphFrameProps) {
   return (
      <g className="graph-frame" data-testid="graph-frame">
         {gridlines ? <FrameGridlines plotWindow={plotWindow} layout={layout} /> : null}
         <FrameAxes layout={layout} />
         {gridlines ? <FrameTicks ticks={frameTickLabels(plotWindow, layout, axisTitles, labelBoxes)} /> : null}
         <FrameAxisTitles layout={layout} axisTitles={axisTitles} />
      </g>
   );
}
