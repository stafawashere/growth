import { describe, expect, it } from "vitest";

import { compileExpression, evaluate, sampleCurve, windowOf } from "./expression";

/* The SymPy strings the lesson specs carry (CONTRACT.md, spec keys): numbers, variables, the four
   operations and **, unary minus, parentheses, the named functions and the constants pi, e, oo. */
describe("evaluate", () => {
   const cases: Array<[string, Record<string, number>, number]> = [
      ["1 + 2*3", {}, 7],
      ["(1 + 2)*3", {}, 9],
      ["2**3**2", {}, 512],
      ["-x**2", { x: 3 }, -9],
      ["(-x)**2", { x: 3 }, 9],
      ["2**-1", {}, 0.5],
      ["10/4/5", {}, 0.5],
      ["7 - 2 - 1", {}, 4],
      ["sqrt(4*x**2 + 5)/(3*x + 1)", { x: 1 }, 3 / 4],
      ["exp(0) + log(e) + sin(pi/2) + cos(0) + tan(0)", {}, 4],
      ["abs(-2.5) + Abs(-0.5)", {}, 3],
      ["3*t**2 - 4*t + 6", { t: 2 }, 10],
      ["x^2 + 1", { x: 2 }, 5],
      ["2(x + 1)", { x: 1 }, 4],
      ["1.5e1 + .5", {}, 15.5]
   ];

   it.each(cases)("%s", (text, scope, expected) => {
      expect(evaluate(text, scope)).toBeCloseTo(expected, 9);
   });

   it("reads oo as Infinity and takes a real odd root of a negative base", () => {
      expect(evaluate("oo", {})).toBe(Infinity);
      expect(evaluate("-oo", {})).toBe(-Infinity);
      expect(evaluate("(-8)**(1/3)", {})).toBeCloseTo(-2, 9);
      expect(evaluate("Abs(x)**(2/3)", { x: -8 })).toBeCloseTo(4, 9);
   });

   it("refuses what it cannot read rather than guessing", () => {
      expect(compileExpression("an increasing curve on [0, 8]")).toBeNull();
      expect(compileExpression("2 +")).toBeNull();
      expect(compileExpression("foo(x)")).toBeNull();
      expect(evaluate("q + 1", {})).toBeNaN();
   });
});

describe("sampleCurve", () => {
   it("turns an expression, a domain and a window into polyline segments", () => {
      const segments = sampleCurve("x**2", { domain: [-2, 2], window: { x: [-3, 3], y: [-1, 5] } });

      expect(segments).toHaveLength(1);
      expect(segments[0][0][0]).toBeCloseTo(-2, 6);
      expect(segments[0][segments[0].length - 1][1]).toBeCloseTo(4, 6);
   });

   it("splits at a discontinuity where the curve leaves the window", () => {
      const segments = sampleCurve("1/x", { window: { x: [-2, 2], y: [-5, 5] } });

      expect(segments.length).toBe(2);
      expect(segments.every((segment) => segment.every(([, y]) => y >= -5 && y <= 5))).toBe(true);
      expect(Math.max(...segments[0].map(([x]) => x))).toBeLessThan(0);
      expect(Math.min(...segments[1].map(([x]) => x))).toBeGreaterThan(0);
   });

   it("reads a window from window, axes or the first two keys given", () => {
      expect(windowOf({ window: { x: [0, 1], y: [2, 3] } })).toEqual({ x: [0, 1], y: [2, 3] });
      expect(windowOf({ axes: { x: [0, 8], y: [60, 110] } })).toEqual({ x: [0, 8], y: [60, 110] });
      expect(windowOf({ window: { t: [0, 6], P: [0, 9] } })).toEqual({ x: [0, 6], y: [0, 9] });
      expect(windowOf({})).toBeNull();
   });
});
