import type {
   FigurePoint,
   TutorFigureCell,
   TutorFigureDot,
   TutorFigureLabel,
   TutorFigurePath,
   TutorFigureRole,
   TutorFigureSpec
} from "../api/types";

/* Hand-written render specs in the shape of docs/agent/drawing-build-plan.md, "The render spec
   contract", for the tutor figure's tests and the screen catalogue while the server's compiler is
   built beside the client. Each stroke carries the style, weight and highlighter the server gives
   its role by default. Test data only. */

type Extra<T> = Partial<Omit<T, "type" | "step" | "element" | "role">>;

const ROLE_STROKES: Record<TutorFigureRole, Pick<TutorFigurePath, "style" | "weight" | "highlighter">> = {
   given: { style: "solid", weight: "regular", highlighter: false },
   constructed: { style: "solid", weight: "bold", highlighter: false },
   highlight: { style: "solid", weight: "bold", highlighter: true },
   error: { style: "dashed", weight: "regular", highlighter: false }
};

export function figurePath(step: string, element: string, role: TutorFigureRole, points: FigurePoint[], extra: Extra<TutorFigurePath> = {}): TutorFigurePath {
   return {
      type: "path",
      step,
      element,
      role,
      points,
      closed: false,
      fill: "none",
      arrow: "none",
      faded_at: null,
      erased_at: null,
      ...ROLE_STROKES[role],
      ...extra
   };
}

export function figureDot(step: string, element: string, role: TutorFigureRole, at: FigurePoint, extra: Extra<TutorFigureDot> = {}): TutorFigureDot {
   return { type: "dot", step, element, role, at, open: false, faded_at: null, erased_at: null, ...extra };
}

export function figureLabel(step: string, element: string, role: TutorFigureRole, at: FigurePoint, text: string, extra: Extra<TutorFigureLabel> = {}): TutorFigureLabel {
   return { type: "label", step, element, role, at, text, offset: [6, -6], align: "start", faded_at: null, erased_at: null, ...extra };
}

export function figureCell(step: string, element: string, role: TutorFigureRole, row: number | null, column: number | null, extra: Extra<TutorFigureCell> = {}): TutorFigureCell {
   return { type: "cell", step, element, role, row, column, faded_at: null, erased_at: null, ...extra };
}

function sampled(curve: (x: number) => number, from: number, to: number, count: number): FigurePoint[] {
   const points: FigurePoint[] = [];

   for (let index = 0; index < count; index += 1) {
      const x = from + ((to - from) * index) / (count - 1);

      points.push([x, curve(x)]);
   }

   return points;
}

const GRAPH_VIEW = { width: 320, height: 300, padding: 20 };

/* drawing-design.md's worked example: a secant through P on y = x^2 closes on the tangent, each
   earlier secant fading as the next is drawn, and the first Q's label erased when Q moves. */
export const SECANT_TO_TANGENT: TutorFigureSpec = {
   id: "figure",
   kind: "graph",
   title: "Secant to tangent",
   description: "The curve y equals x squared with a point P at x equals 1. A secant from P to a second point Q moves toward P, and the tangent at P is drawn last.",
   window: { x: [-1, 4], y: [-1, 9] },
   view: GRAPH_VIEW,
   axes: { x: "x", y: "y" },
   grid: true,
   equal_scale: false,
   steps: [
      { id: "curve", caption: "The curve y = x^2" },
      { id: "secant", caption: "A secant through P and Q" },
      { id: "closer", caption: "Q moves closer to P" },
      { id: "tangent", caption: "The tangent at P" }
   ],
   columns: null,
   rows: null,
   primitives: [
      figurePath("curve", "f", "given", sampled((x) => x * x, -1, 3, 41)),
      figureLabel("curve", "f", "given", [2.5, 6.25], "\\(y = x^2\\)"),
      figureDot("secant", "P", "constructed", [1, 1]),
      figureLabel("secant", "P", "constructed", [1, 1], "P", { offset: [-6, -6], align: "end" }),
      figureDot("secant", "Q", "constructed", [3, 9], { faded_at: "closer" }),
      figureLabel("secant", "Q", "constructed", [3, 9], "Q", { erased_at: "closer" }),
      figurePath("secant", "s1", "constructed", [[0.5, -1], [3, 9]], { faded_at: "closer" }),
      figureDot("closer", "Q2", "constructed", [2, 4], { faded_at: "tangent" }),
      figureLabel("closer", "Q2", "constructed", [2, 4], "Q"),
      figurePath("closer", "s2", "constructed", [[1 / 3, -1], [11 / 3, 9]], { faded_at: "tangent" }),
      figurePath("tangent", "t", "highlight", [[0, -1], [4, 7]]),
      figureLabel("tangent", "t", "highlight", [3.5, 6], "tangent")
   ]
};

/* Every role on a stroke, a dot and a label, arrowheads at each end, a region above the axis and
   one below it, and a last step that fades the constructed marks and a third region, so one
   finished figure draws every tutor figure style there is. */
export const EVERY_ROLE_FIGURE: TutorFigureSpec = {
   id: "figure",
   kind: "graph",
   title: "Every role",
   description: "A parabola with a constructed segment, a wrong segment, a highlighted line and two shaded regions, one above and one below the x axis.",
   window: { x: [-3, 3], y: [-2, 4] },
   view: GRAPH_VIEW,
   axes: { x: "x", y: "y" },
   grid: true,
   equal_scale: false,
   steps: [
      { id: "given", caption: "The curve" },
      { id: "constructed", caption: "A segment drawn from A" },
      { id: "error", caption: "The segment the response used" },
      { id: "highlight", caption: "The line this is about" },
      { id: "fills", caption: "The regions above and below the axis" },
      { id: "fade", caption: "The segment from A fades" }
   ],
   columns: null,
   rows: null,
   primitives: [
      figurePath("given", "f", "given", sampled((x) => (x * x) / 2 - 1, -3, 3, 25)),
      figureDot("given", "V", "given", [0, -1]),
      figureLabel("given", "f", "given", [2, 1], "\\(f\\)"),
      figurePath("constructed", "a", "constructed", [[-2, 3], [-0.5, 3]], { arrow: "end", faded_at: "fade" }),
      figureDot("constructed", "A", "constructed", [-2, 3], { open: true, faded_at: "fade" }),
      figureLabel("constructed", "A", "constructed", [-2, 3], "A", { offset: [-6, -6], align: "end", faded_at: "fade" }),
      figurePath("error", "w", "error", [[0.5, 3.5], [2.5, 3.5]], { arrow: "start" }),
      figureDot("error", "W", "error", [2.5, 3.5]),
      figureLabel("error", "w", "error", [0.5, 3.5], "right endpoints", { offset: [0, -8] }),
      figurePath("highlight", "h", "highlight", [[-1.5, -2], [0.5, 2]], { arrow: "both" }),
      figureDot("highlight", "H", "highlight", [-0.5, 0]),
      figureLabel("highlight", "h", "highlight", [0.5, 2], "tangent"),
      figurePath("fills", "above", "constructed", [[1.5, 0], [1.5, 0.125], [2, 1], [2.5, 2.125], [2.5, 0]], { closed: true, fill: "region" }),
      figurePath("fills", "below", "constructed", [[-1, 0], [-1, -0.5], [0, -1], [1, -0.5], [1, 0]], { closed: true, fill: "region_below" }),
      figurePath("fills", "strip", "constructed", [[-2.5, 0], [-2.5, 2.125], [-2, 1], [-2, 0]], { closed: true, fill: "region", faded_at: "fade" })
   ]
};

/* A right triangle with no axes, which the server lays out point by point. */
export const TRIANGLE_DIAGRAM: TutorFigureSpec = {
   id: "figure",
   kind: "diagram",
   title: "A ladder against a wall",
   description: "A right triangle with legs 3 and 4 and hypotenuse 5.",
   window: { x: [-1, 5], y: [-1, 4] },
   view: { width: 320, height: 260, padding: 20 },
   axes: null,
   grid: false,
   equal_scale: true,
   steps: [
      { id: "triangle", caption: "The triangle" },
      { id: "hypotenuse", caption: "The ladder" }
   ],
   columns: null,
   rows: null,
   primitives: [
      figurePath("triangle", "legs", "given", [[0, 0], [4, 0], [4, 3]]),
      figurePath("triangle", "mark", "given", [[3.6, 0], [3.6, 0.4], [4, 0.4]], { weight: "thin" }),
      figurePath("hypotenuse", "ladder", "constructed", [[0, 0], [4, 3]]),
      figureLabel("hypotenuse", "ladder", "constructed", [2, 1.5], "5", { offset: [-10, -4], align: "end" })
   ]
};

/* A table of values whose second row is highlighted, then one cell marked wrong, then the row
   highlight faded while a column is highlighted. */
export const TABLE_OF_VALUES: TutorFigureSpec = {
   id: "figure",
   kind: "table",
   title: "Values of f",
   description: "A table of x, f of x and f prime of x at x equals 0, 1 and 2.",
   window: null,
   view: null,
   axes: null,
   grid: false,
   equal_scale: false,
   steps: [
      { id: "row", caption: "The row where x = 1" },
      { id: "cell", caption: "The rate the response read" },
      { id: "column", caption: "The values of f" }
   ],
   columns: ["\\(x\\)", "\\(f(x)\\)", "\\(f'(x)\\)"],
   rows: [
      ["0", "1", "2"],
      ["1", "3", "\\(\\frac{5}{2}\\)"],
      ["2", "5", "3"]
   ],
   primitives: [
      figureCell("row", "r1", "highlight", 1, null, { faded_at: "column" }),
      figureCell("cell", "c22", "error", 2, 2),
      figureCell("column", "k1", "highlight", null, 1)
   ]
};

/* The same table with the server's words on a highlighted row and on the wrong cell. */
export const LABELLED_TABLE: TutorFigureSpec = {
   ...TABLE_OF_VALUES,
   primitives: [
      figureCell("row", "r1", "highlight", 1, null, { text: "\\(x = 1\\)" }),
      figureCell("cell", "c22", "error", 2, 2, { text: "read as 3" }),
      figureCell("column", "k1", "highlight", null, 1)
   ]
};
