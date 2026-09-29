import type { FigurePoint } from "../api/types";

/* The expressions a lesson's delivery spec carries are SymPy strings (docs/lessons/BUILD-PLAN.md
   amendment A-D1 and the orchestrator's contract, spec keys): ** powers, explicit *, sqrt, exp,
   log, pi and oo. The designs were written by hand, so ^ for a power and a number written against
   a bracket or a letter (2(x + 1), 3x) are read as well. Nothing here guesses: a string that does
   not parse compiles to null and the block falls back to its authored text. No dependency is
   added for this, so the grammar is the small one below. */

export type Scope = Record<string, number>;

export type Compiled = (scope: Scope) => number;

export interface Interval2 {
   x: [number, number];
   y: [number, number];
}

type Token =
   | { kind: "number"; value: number }
   | { kind: "name"; value: string }
   | { kind: "op"; value: string };

const FUNCTIONS: Record<string, (value: number) => number> = {
   sqrt: Math.sqrt,
   exp: Math.exp,
   log: Math.log,
   ln: Math.log,
   sin: Math.sin,
   cos: Math.cos,
   tan: Math.tan,
   asin: Math.asin,
   acos: Math.acos,
   atan: Math.atan,
   sec: (value) => 1 / Math.cos(value),
   csc: (value) => 1 / Math.sin(value),
   cot: (value) => 1 / Math.tan(value),
   sinh: Math.sinh,
   cosh: Math.cosh,
   tanh: Math.tanh,
   abs: Math.abs,
   Abs: Math.abs,
   sign: Math.sign
};

const CONSTANTS: Record<string, number> = {
   pi: Math.PI,
   e: Math.E,
   E: Math.E,
   oo: Infinity
};

const NUMBER = /^(\d+\.?\d*|\.\d+)(e[+-]?\d+)?/i;

const NAME = /^[A-Za-z_][A-Za-z0-9_]*/;

function tokenize(text: string): Token[] | null {
   const tokens: Token[] = [];
   let rest = text.trim();

   while (rest.length > 0) {
      const number = NUMBER.exec(rest);
      const name = NAME.exec(rest);

      if (number !== null) {
         tokens.push({ kind: "number", value: Number(number[0]) });
         rest = rest.slice(number[0].length);
      } else if (name !== null) {
         tokens.push({ kind: "name", value: name[0] });
         rest = rest.slice(name[0].length);
      } else if (rest.startsWith("**")) {
         tokens.push({ kind: "op", value: "**" });
         rest = rest.slice(2);
      } else if ("+-*/^()".includes(rest[0])) {
         tokens.push({ kind: "op", value: rest[0] === "^" ? "**" : rest[0] });
         rest = rest.slice(1);
      } else {
         return null;
      }

      rest = rest.trimStart();
   }

   return tokens;
}

/* SymPy's real root: a negative base under a rational power with an odd denominator, as in
   Abs(x)**(2/3) or (x - 1)**(1/3), has a real value, where Math.pow gives NaN. */
function realPower(base: number, exponent: number) {
   const direct = Math.pow(base, exponent);
   const needsRealRoot = Number.isNaN(direct) && base < 0;

   if (!needsRealRoot) {
      return direct;
   }

   for (const denominator of [3, 5, 7, 9]) {
      const numerator = exponent * denominator;
      const isRational = Math.abs(numerator - Math.round(numerator)) < 1e-9;

      if (isRational) {
         const magnitude = Math.pow(-base, exponent);
         const isOddNumerator = Math.abs(Math.round(numerator)) % 2 === 1;

         return isOddNumerator ? -magnitude : magnitude;
      }
   }

   return direct;
}

class Parser {
   private position = 0;

   constructor(private readonly tokens: Token[]) {}

   parse(): Compiled | null {
      const expression = this.sum();
      const isFinished = this.position === this.tokens.length;

      return expression !== null && isFinished ? expression : null;
   }

   private peek() {
      return this.tokens[this.position];
   }

   private isOp(value: string) {
      const token = this.peek();

      return token !== undefined && token.kind === "op" && token.value === value;
   }

   private sum(): Compiled | null {
      let left = this.product();

      while (left !== null && (this.isOp("+") || this.isOp("-"))) {
         const isPlus = this.isOp("+");

         this.position += 1;

         const right = this.product();

         if (right === null) {
            return null;
         }

         const first: Compiled = left;

         left = isPlus ? (scope) => first(scope) + right(scope) : (scope) => first(scope) - right(scope);
      }

      return left;
   }

   /* A number, a closing bracket or a one-letter variable followed by an opening bracket, a
      number or a name multiplies by juxtaposition. Two names side by side do not, so prose such as
      "an increasing curve" never reads as a product. */
   private startsImplicitFactor(previous: Token | undefined) {
      const next = this.peek();

      if (previous === undefined || next === undefined) {
         return false;
      }

      const previousEndsValue =
         previous.kind === "number" || (previous.kind === "op" && previous.value === ")") || previous.kind === "name";
      const nextStartsValue = next.kind === "name" || (next.kind === "op" && next.value === "(");
      const isNameAfterName = previous.kind === "name" && next.kind === "name";
      const isCallAfterName =
         previous.kind === "name" && next.kind === "op" && next.value === "(" && previous.value.length > 1;

      return previousEndsValue && nextStartsValue && !isNameAfterName && !isCallAfterName;
   }

   private product(): Compiled | null {
      let left = this.unary();

      while (left !== null) {
         const previous = this.tokens[this.position - 1];

         if (this.isOp("*") || this.isOp("/")) {
            const isTimes = this.isOp("*");

            this.position += 1;

            const right = this.unary();

            if (right === null) {
               return null;
            }

            const first: Compiled = left;

            left = isTimes ? (scope) => first(scope) * right(scope) : (scope) => first(scope) / right(scope);
         } else if (this.startsImplicitFactor(previous)) {
            const right = this.power();

            if (right === null) {
               return null;
            }

            const first: Compiled = left;

            left = (scope) => first(scope) * right(scope);
         } else {
            break;
         }
      }

      return left;
   }

   private unary(): Compiled | null {
      if (this.isOp("-")) {
         this.position += 1;

         const operand = this.unary();

         return operand === null ? null : (scope) => -operand(scope);
      }

      if (this.isOp("+")) {
         this.position += 1;

         return this.unary();
      }

      return this.power();
   }

   /* ** binds tighter than unary minus on its left and is right associative, so -x**2 is
      -(x**2) and 2**3**2 is 2**9, as in SymPy. */
   private power(): Compiled | null {
      const base = this.atom();

      if (base === null) {
         return null;
      }

      if (this.isOp("**")) {
         this.position += 1;

         const exponent = this.unary();

         return exponent === null ? null : (scope) => realPower(base(scope), exponent(scope));
      }

      return base;
   }

   private atom(): Compiled | null {
      const token = this.peek();

      if (token === undefined) {
         return null;
      }

      this.position += 1;

      if (token.kind === "number") {
         const value = token.value;

         return () => value;
      }

      if (token.kind === "op" && token.value === "(") {
         const inner = this.sum();

         if (inner === null || !this.isOp(")")) {
            return null;
         }

         this.position += 1;

         return inner;
      }

      if (token.kind !== "name") {
         return null;
      }

      const name = token.value;
      const isCall = this.isOp("(") && name.length > 1;

      if (isCall) {
         const apply = FUNCTIONS[name];

         if (apply === undefined) {
            return null;
         }

         this.position += 1;

         const argument = this.sum();

         if (argument === null || !this.isOp(")")) {
            return null;
         }

         this.position += 1;

         return (scope) => apply(argument(scope));
      }

      if (name in FUNCTIONS) {
         return null;
      }

      return (scope) => {
         if (name in scope) {
            return scope[name];
         }

         return name in CONSTANTS ? CONSTANTS[name] : NaN;
      };
   }
}

const cache = new Map<string, Compiled | null>();

export function compileExpression(text: string): Compiled | null {
   if (cache.has(text)) {
      return cache.get(text) ?? null;
   }

   const tokens = tokenize(text);
   const compiled = tokens === null || tokens.length === 0 ? null : new Parser(tokens).parse();

   cache.set(text, compiled);

   return compiled;
}

export function evaluate(text: string, scope: Scope): number {
   const compiled = compileExpression(text);

   return compiled === null ? NaN : compiled(scope);
}

/* A number, a numeric string or an expression in the current parameters, as a spec writes
   shade {to: "b"} or a frame's g: "-8 + pi". */
export function numberFrom(value: unknown, scope: Scope = {}): number | null {
   if (typeof value === "number") {
      return Number.isFinite(value) ? value : null;
   }

   if (typeof value !== "string") {
      return null;
   }

   const result = evaluate(value, scope);

   return Number.isFinite(result) ? result : null;
}

function isPair(value: unknown): value is [number, number] {
   const isArray = Array.isArray(value) && value.length === 2;

   return isArray && typeof value[0] === "number" && typeof value[1] === "number" && value[0] < value[1];
}

/* A window is written window {x, y}, axes {x, y}, or with the design's own variable names such as
   {t, P}; the first two keys are the horizontal and the vertical axis in that order. */
export function windowOf(spec: Record<string, unknown>): Interval2 | null {
   const box = (spec.window ?? spec.axes) as Record<string, unknown> | undefined;
   const isBox = typeof box === "object" && box !== null;

   if (!isBox) {
      return null;
   }

   const values = Object.values(box);
   const horizontal = box.x !== undefined && isPair(box.y) ? box.x : values[0];
   const vertical = box.x !== undefined && isPair(box.y) ? box.y : values[1];

   if (!isPair(horizontal) || !isPair(vertical)) {
      return null;
   }

   return { x: horizontal, y: vertical };
}

export const SAMPLES_PER_CURVE = 240;

export interface SampleOptions {
   domain?: [number, number];
   window: Interval2;
   variable?: string;
   scope?: Scope;
}

/* The polylines FigureView draws for y = f(x). A sample outside the window, or one that is not a
   finite number, ends the current segment, so a curve with a vertical asymptote is drawn as the
   separate pieces on either side rather than as a line through the jump. */
export function sampleFunction(f: (x: number) => number, domain: [number, number], window: Interval2): FigurePoint[][] {
   const [low, high] = [Math.max(domain[0], window.x[0]), Math.min(domain[1], window.x[1])];
   const segments: FigurePoint[][] = [];
   let current: FigurePoint[] = [];

   if (!(low < high)) {
      return segments;
   }

   for (let index = 0; index <= SAMPLES_PER_CURVE; index += 1) {
      const x = low + ((high - low) * index) / SAMPLES_PER_CURVE;
      const y = f(x);
      const isInside = Number.isFinite(y) && y >= window.y[0] && y <= window.y[1];

      if (isInside) {
         current.push([x, y]);
      } else if (current.length > 0) {
         segments.push(current);
         current = [];
      }
   }

   if (current.length > 0) {
      segments.push(current);
   }

   return segments.filter((segment) => segment.length > 1);
}

export function sampleCurve(text: string, options: SampleOptions): FigurePoint[][] {
   const compiled = compileExpression(text);

   if (compiled === null) {
      return [];
   }

   const variable = options.variable ?? "x";
   const scope = options.scope ?? {};
   const f = (x: number) => compiled({ ...scope, [variable]: x });

   return sampleFunction(f, options.domain ?? options.window.x, options.window);
}

/* A parametric path (x(t), y(t)) sampled over [t0, t1], split where it leaves the window. */
export function sampleParametric(
   x: Compiled,
   y: Compiled,
   range: [number, number],
   window: Interval2,
   scope: Scope = {}
): FigurePoint[][] {
   const segments: FigurePoint[][] = [];
   let current: FigurePoint[] = [];

   for (let index = 0; index <= SAMPLES_PER_CURVE; index += 1) {
      const t = range[0] + ((range[1] - range[0]) * index) / SAMPLES_PER_CURVE;
      const point: FigurePoint = [x({ ...scope, t }), y({ ...scope, t })];
      const isInside = insideWindow(point, window);

      if (isInside) {
         current.push(point);
      } else if (current.length > 0) {
         segments.push(current);
         current = [];
      }
   }

   if (current.length > 0) {
      segments.push(current);
   }

   return segments.filter((segment) => segment.length > 1);
}

export function insideWindow(point: FigurePoint, window: Interval2) {
   const [x, y] = point;
   const isFinite = Number.isFinite(x) && Number.isFinite(y);

   return isFinite && x >= window.x[0] && x <= window.x[1] && y >= window.y[0] && y <= window.y[1];
}

export const MARCHING_CELLS = 64;

/* An implicit curve F(x, y) = 0 by marching squares on the window: each cell whose corners change
   sign contributes the segment joining the edge crossings, found by linear interpolation. A cell
   with all four edges crossed (a saddle) takes the two segments that pair adjacent edges. */
export function marchingSquares(F: (x: number, y: number) => number, window: Interval2, cells = MARCHING_CELLS): FigurePoint[][] {
   const segments: FigurePoint[][] = [];
   const dx = (window.x[1] - window.x[0]) / cells;
   const dy = (window.y[1] - window.y[0]) / cells;
   const values: number[][] = [];

   for (let row = 0; row <= cells; row += 1) {
      values.push([]);

      for (let column = 0; column <= cells; column += 1) {
         values[row].push(F(window.x[0] + column * dx, window.y[0] + row * dy));
      }
   }

   const crossing = (x0: number, y0: number, v0: number, x1: number, y1: number, v1: number): FigurePoint => {
      const share = v0 / (v0 - v1);

      return [x0 + (x1 - x0) * share, y0 + (y1 - y0) * share];
   };

   for (let row = 0; row < cells; row += 1) {
      for (let column = 0; column < cells; column += 1) {
         const x0 = window.x[0] + column * dx;
         const y0 = window.y[0] + row * dy;
         const x1 = x0 + dx;
         const y1 = y0 + dy;
         const a = values[row][column];
         const b = values[row][column + 1];
         const c = values[row + 1][column + 1];
         const d = values[row + 1][column];
         const corners = [a, b, c, d];

         if (!corners.every(Number.isFinite)) {
            continue;
         }

         const edges: FigurePoint[] = [];

         if (a < 0 !== b < 0) {
            edges.push(crossing(x0, y0, a, x1, y0, b));
         }

         if (b < 0 !== c < 0) {
            edges.push(crossing(x1, y0, b, x1, y1, c));
         }

         if (c < 0 !== d < 0) {
            edges.push(crossing(x1, y1, c, x0, y1, d));
         }

         if (d < 0 !== a < 0) {
            edges.push(crossing(x0, y1, d, x0, y0, a));
         }

         if (edges.length === 2) {
            segments.push([edges[0], edges[1]]);
         } else if (edges.length === 4) {
            segments.push([edges[0], edges[1]], [edges[2], edges[3]]);
         }
      }
   }

   return segments;
}
