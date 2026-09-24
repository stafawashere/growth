import { describe, expect, it } from "vitest";

import { compile, ExpressionError } from "./expression";
import { derivativeAt, findZeros, formatResult, integrate, plotSegments } from "./numeric";

describe("the expression reader", () => {
   it("reads precedence, unary minus and implicit multiplication", () => {
      expect(compile("-x^2", "radians")(3)).toBe(-9);
      expect(compile("2x", "radians")(5)).toBe(10);
      expect(compile("3sin(x)", "radians")(Math.PI / 2)).toBeCloseTo(3, 12);
      expect(compile("(x+1)(x-1)", "radians")(4)).toBe(15);
      expect(compile("2^-1", "radians")(0)).toBe(0.5);
      expect(compile("1 + 2 * 3 - 4 / 2", "radians")(0)).toBe(5);
      expect(compile("e^x", "radians")(1)).toBeCloseTo(Math.E, 12);
      expect(compile("ln(e) + log(100) + sqrt(16) + abs(-2) + exp(0)", "radians")(0)).toBeCloseTo(10, 12);
      expect(compile("pi", "radians")(0)).toBe(Math.PI);
   });

   it("refuses what it cannot read instead of guessing", () => {
      expect(() => compile("2 + ", "radians")).toThrow(ExpressionError);
      expect(() => compile("foo(x)", "radians")).toThrow(ExpressionError);
      expect(() => compile("(x + 1", "radians")).toThrow(ExpressionError);
   });
});

describe("the four calculator capabilities", () => {
   it("finds the zero of cos x on [1, 2] at pi/2", () => {
      const zeros = findZeros(compile("cos(x)", "radians"), 1, 2);

      expect(zeros).toHaveLength(1);
      expect(zeros[0]).toBeCloseTo(Math.PI / 2, 9);
   });

   it("does not report the pole of tan x as a zero", () => {
      const zeros = findZeros(compile("tan(x)", "radians"), 1, 2);

      expect(zeros).toEqual([]);
   });

   it("finds every zero of x^3 - x in the window", () => {
      const zeros = findZeros(compile("x^3 - x", "radians"), -2, 2.1);

      expect(zeros).toHaveLength(3);
      expect(zeros[0]).toBeCloseTo(-1, 9);
      expect(zeros[1]).toBeCloseTo(0, 9);
      expect(zeros[2]).toBeCloseTo(1, 9);
   });

   it("takes the derivative of x^3 at 2 as 12", () => {
      expect(derivativeAt(compile("x^3", "radians"), 2)).toBeCloseTo(12, 6);
   });

   it("integrates sin x from 0 to pi as 2", () => {
      expect(integrate(compile("sin(x)", "radians"), 0, Math.PI)).toBeCloseTo(2, 9);
   });

   it("integrates e^(-x^2) from 0 to 1 to the published 0.746824", () => {
      expect(formatResult(integrate(compile("e^(-x^2)", "radians"), 0, 1))).toBe("0.746824");
   });

   it("plots within the window and breaks the curve at an asymptote", () => {
      const window = { xMin: -1, xMax: 1, yMin: -10, yMax: 10 };
      const segments = plotSegments(compile("1/x", "radians"), window, 200);

      expect(segments).toHaveLength(2);

      for (const segment of segments) {
         for (const point of segment) {
            expect(point.x).toBeGreaterThanOrEqual(window.xMin);
            expect(point.x).toBeLessThanOrEqual(window.xMax);
         }
      }
   });
});

describe("the angle mode", () => {
   it("evaluates sin(90) as 1 in degrees and as sin of 90 radians in radians", () => {
      expect(compile("sin(90)", "degrees")(0)).toBeCloseTo(1, 12);
      expect(compile("sin(90)", "radians")(0)).toBeCloseTo(Math.sin(90), 12);
   });

   it("returns inverse trigonometry in the chosen unit", () => {
      expect(compile("arctan(1)", "degrees")(0)).toBeCloseTo(45, 12);
      expect(compile("arctan(1)", "radians")(0)).toBeCloseTo(Math.PI / 4, 12);
   });
});
