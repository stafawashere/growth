import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { CorrectResult } from "./ElaboratedPanel";
import { StepMarks } from "./StepMarks";

const WIDE_KEY = [
   "Divide",
   2,
   ["Sqrt", ["Subtract", 121, ["Power", ["Subtract", ["Multiply", -2, "x"], 1], 2]]]
];

const WIDE_STEP =
   "Express the trigonometric factor in x by the Pythagorean identity: " +
   "\\(\\sin(g(x)) = \\sqrt{1 - \\cos^2(g(x))} = \\sqrt{1 - \\left(-\\frac{2x}{11} - \\frac{1}{11}\\right)^2}\\).";

afterEach(cleanup);

describe("math wider than a phone screen", () => {
   it("scrolls inside the correct result rather than widening the page", () => {
      render(<CorrectResult answer={{ label: null, mathjson: WIDE_KEY }} />);

      const block = screen.getByTestId("correct-answer");
      const math = block.querySelector(".katex");

      expect(math, "the correct result rendered no KaTeX").not.toBeNull();

      const mathHolder = math?.closest(".math-overflow") ?? null;

      expect(mathHolder, "the correct result's math sits in no scrolling holder").not.toBeNull();
   });

   it("scrolls inside a worked step rather than widening the page", () => {
      render(<StepMarks marks={[{ index: 1, text: WIDE_STEP, given: true, correct: null }]} />);

      const step = screen.getByTestId("step-mark-1");
      const displayedMath = step.querySelector(".katex-display");

      expect(displayedMath, "the wide step was not given a line of its own").not.toBeNull();

      const mathHolder = displayedMath?.closest(".math-overflow") ?? null;

      expect(mathHolder, "the worked step's display math sits in no scrolling holder").not.toBeNull();
   });
});
