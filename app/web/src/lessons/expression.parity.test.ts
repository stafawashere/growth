import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

import { compileExpression } from "./expression";

/* The figure grammar on the server (app/agent/drawing/expression.py) is a twin of this one, and
   tests/agent/drawing/test_expression.py reads the same fixture, so the two cannot drift apart on
   what an expression means. The server alone refuses what the fixture lists under
   python_only_refusals; this grammar keeps its own behaviour there. */

interface ParityCase {
   expression: string;
   variable: string;
   points: Array<[number, number]>;
}

interface UndefinedCase {
   expression: string;
   variable: string;
   points: number[];
}

interface RefusalCase {
   expression: string;
   variable: string;
}

interface ParityFixture {
   tolerance: number;
   cases: ParityCase[];
   undefined: UndefinedCase[];
   refusals: RefusalCase[];
}

const REPO_ROOT = resolve(process.cwd(), "..", "..");

const FIXTURE = JSON.parse(
   readFileSync(resolve(REPO_ROOT, "tests/fixtures/drawing/expressions.json"), "utf8")
) as ParityFixture;

describe("the shared expression fixture", () => {
   it("reads a fixture with cases and refusals in it", () => {
      expect(FIXTURE.cases.length).toBeGreaterThan(30);
      expect(FIXTURE.refusals.length).toBeGreaterThan(10);
   });

   it.each(FIXTURE.cases.map((entry) => [entry.expression, entry] as const))("%s has the listed values", (_text, entry) => {
      const compiled = compileExpression(entry.expression);

      expect(compiled).not.toBeNull();

      for (const [point, expected] of entry.points) {
         const value = compiled?.({ [entry.variable]: point }) ?? NaN;
         const allowed = FIXTURE.tolerance * Math.max(1, Math.abs(expected));

         expect(Math.abs(value - expected)).toBeLessThanOrEqual(allowed);
      }
   });

   it.each(FIXTURE.undefined.map((entry) => [entry.expression, entry] as const))("%s is undefined at the listed points", (_text, entry) => {
      const compiled = compileExpression(entry.expression);

      expect(compiled).not.toBeNull();

      for (const point of entry.points) {
         expect(Number.isFinite(compiled?.({ [entry.variable]: point }))).toBe(false);
      }
   });

   it.each(FIXTURE.refusals.map((entry) => [entry.expression, entry] as const))("refuses %j", (_text, entry) => {
      expect(compileExpression(entry.expression)).toBeNull();
   });
});
