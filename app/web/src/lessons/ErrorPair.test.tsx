import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import type { LessonSection as LessonSectionRecord } from "../api/types";
import { LessonSection } from "./LessonSection";

const INTEGRAL = ["Integrate", ["Add", ["Negate", ["Power", "x", 2]], ["Multiply", 7, "x"], -10], ["Tuple", "x", 2, 5]];

function errorBlock(wrong: unknown, right: unknown): LessonSectionRecord {
   return {
      id: "LSN-CON-08010#err-BC-ERR-99006",
      type: "common_error",
      bands: ["low", "mid"],
      error_id: "BC-ERR-99006",
      observed_behavior: "The differential is missing.",
      scoring_consequence: "A point may be lost.",
      wrong_step: { text: "The integral with no dx.", expression: wrong },
      right_step: { text: "The integral with its dx.", expression: right },
      relation: "equivalent"
   } as LessonSectionRecord;
}

function drawnValues(testId: string) {
   return screen.getByTestId(testId).querySelectorAll(".katex, math, [data-math-value]").length;
}

afterEach(() => {
   cleanup();
});

describe("an error pair", () => {
   it("leaves out an expression both steps share, so the text carries the difference", () => {
      render(<LessonSection section={errorBlock(INTEGRAL, INTEGRAL)} revealAll />);

      expect(drawnValues("lesson-wrong-step")).toBe(0);
      expect(drawnValues("lesson-right-step")).toBe(0);
      expect(screen.getByTestId("lesson-wrong-step").textContent).toContain("with no dx");
   });

   it("draws both expressions when the values differ", () => {
      render(<LessonSection section={errorBlock(["Multiply", 2, "x"], ["Multiply", 3, "x"])} revealAll />);

      expect(drawnValues("lesson-wrong-step")).toBeGreaterThan(0);
      expect(drawnValues("lesson-right-step")).toBeGreaterThan(0);
   });
});
