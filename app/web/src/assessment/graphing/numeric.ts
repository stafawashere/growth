import type { RealFunction } from "./expression";

/* The four capabilities the CED requires of a calculator (05, Calculator-part handling): plot in
   a window, find zeros, a numerical derivative at a point and a numerical definite integral. */

export interface PlotWindow {
   xMin: number;
   xMax: number;
   yMin: number;
   yMax: number;
}

const ZERO_SCAN_STEPS = 2000;

const BISECTION_ROUNDS = 200;

const ZERO_RESIDUAL = 1e-6;

const DERIVATIVE_STEP = 1e-5;

const SIMPSON_TOLERANCE = 1e-10;

const SIMPSON_MAX_DEPTH = 40;

export function windowIsUsable(window: PlotWindow) {
   const values = [window.xMin, window.xMax, window.yMin, window.yMax];
   const allFinite = values.every((value) => Number.isFinite(value));
   const xIncreases = window.xMax > window.xMin;
   const yIncreases = window.yMax > window.yMin;

   return allFinite && xIncreases && yIncreases;
}

function bisect(f: RealFunction, left: number, right: number) {
   let low = left;
   let high = right;
   let lowValue = f(low);

   for (let round = 0; round < BISECTION_ROUNDS; round += 1) {
      const middle = (low + high) / 2;
      const middleValue = f(middle);
      const hasConverged = middle === low || middle === high;

      if (hasConverged) {
         break;
      }

      const signChangesBelow = Math.sign(middleValue) !== Math.sign(lowValue);

      if (signChangesBelow) {
         high = middle;
      } else {
         low = middle;
         lowValue = middleValue;
      }
   }

   return (low + high) / 2;
}

/* Scans the window for sign changes, then bisects each one. A sign change across a pole (tan x at
   pi/2) is not a zero, so a root is kept only when the function is near zero there. */
export function findZeros(f: RealFunction, xMin: number, xMax: number): number[] {
   const zeros: number[] = [];
   const step = (xMax - xMin) / ZERO_SCAN_STEPS;
   let left = xMin;
   let leftValue = f(left);

   for (let index = 1; index <= ZERO_SCAN_STEPS; index += 1) {
      const right = index === ZERO_SCAN_STEPS ? xMax : xMin + index * step;
      const rightValue = f(right);
      const bothFinite = Number.isFinite(leftValue) && Number.isFinite(rightValue);
      const landsOnZero = bothFinite && leftValue === 0;
      const changesSign = bothFinite && leftValue * rightValue < 0;

      if (landsOnZero) {
         zeros.push(left);
      }

      if (changesSign) {
         const root = bisect(f, left, right);
         const isNearZero = Math.abs(f(root)) < ZERO_RESIDUAL;

         if (isNearZero) {
            zeros.push(root);
         }
      }

      left = right;
      leftValue = rightValue;
   }

   const endsOnZero = leftValue === 0;

   if (endsOnZero) {
      zeros.push(xMax);
   }

   return zeros.filter((zero, index) => index === 0 || Math.abs(zero - zeros[index - 1]) > step / 2);
}

export function derivativeAt(f: RealFunction, x: number) {
   const step = DERIVATIVE_STEP * Math.max(1, Math.abs(x));

   return (f(x + step) - f(x - step)) / (2 * step);
}

function simpson(fa: number, fm: number, fb: number, width: number) {
   return (width / 6) * (fa + 4 * fm + fb);
}

function adaptiveSimpson(
   f: RealFunction,
   a: number,
   b: number,
   fa: number,
   fm: number,
   fb: number,
   whole: number,
   tolerance: number,
   depth: number
): number {
   const middle = (a + b) / 2;
   const leftMiddle = (a + middle) / 2;
   const rightMiddle = (middle + b) / 2;
   const fLeftMiddle = f(leftMiddle);
   const fRightMiddle = f(rightMiddle);
   const left = simpson(fa, fLeftMiddle, fm, middle - a);
   const right = simpson(fm, fRightMiddle, fb, b - middle);
   const difference = left + right - whole;
   const isSettled = depth <= 0 || Math.abs(difference) <= 15 * tolerance;

   if (isSettled) {
      return left + right + difference / 15;
   }

   return (
      adaptiveSimpson(f, a, middle, fa, fLeftMiddle, fm, left, tolerance / 2, depth - 1) +
      adaptiveSimpson(f, middle, b, fm, fRightMiddle, fb, right, tolerance / 2, depth - 1)
   );
}

export function integrate(f: RealFunction, lower: number, upper: number) {
   const isEmpty = lower === upper;

   if (isEmpty) {
      return 0;
   }

   const fa = f(lower);
   const fb = f(upper);
   const fm = f((lower + upper) / 2);
   const whole = simpson(fa, fm, fb, upper - lower);

   return adaptiveSimpson(f, lower, upper, fa, fm, fb, whole, SIMPSON_TOLERANCE, SIMPSON_MAX_DEPTH);
}

export interface PlotPoint {
   x: number;
   y: number;
}

/* Samples the function across the window and splits the curve wherever it is undefined or leaves
   the window, so an asymptote is not drawn as a vertical line. */
export function plotSegments(f: RealFunction, window: PlotWindow, samples: number): PlotPoint[][] {
   const segments: PlotPoint[][] = [];
   const height = window.yMax - window.yMin;
   let current: PlotPoint[] = [];

   for (let index = 0; index <= samples; index += 1) {
      const x = window.xMin + ((window.xMax - window.xMin) * index) / samples;
      const y = f(x);
      const isDrawable = Number.isFinite(y) && y >= window.yMin - height && y <= window.yMax + height;

      if (isDrawable) {
         current.push({ x, y });
         continue;
      }

      if (current.length > 1) {
         segments.push(current);
      }

      current = [];
   }

   if (current.length > 1) {
      segments.push(current);
   }

   return segments;
}

export function formatResult(value: number) {
   const isFinite = Number.isFinite(value);

   if (!isFinite) {
      return "undefined";
   }

   const rounded = value.toFixed(6);

   return rounded === "-0.000000" ? "0.000000" : rounded;
}
