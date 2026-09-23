import { describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { AFFORDANCE_ATTRIBUTE, P1_FEEDBACK_AFFORDANCES } from "../affordances";
import { motionClass } from "../styles/motion";
import type { StepMark } from "../api/types";
import { StepMarks } from "./StepMarks";

const marks: StepMark[] = [
   { index: 1, description: "Factors named", correct: true },
   { index: 2, description: "Derivatives of the factors", correct: false }
];

describe("StepMarks", () => {
   it("carries the step verification affordance and its motion class", () => {
      render(<StepMarks marks={marks} />);

      const panel = screen.getByTestId("step-marks");

      expect(panel.getAttribute(AFFORDANCE_ATTRIBUTE)).toBe(P1_FEEDBACK_AFFORDANCES.stepVerificationMark);
      expect(panel.className).toContain(motionClass("stepVerificationMark"));

      cleanup();
   });

   it("states each mark with a word and a glyph, never colour alone", () => {
      render(<StepMarks marks={marks} />);

      const correctRow = screen.getByTestId("step-mark-1");
      const incorrectRow = screen.getByTestId("step-mark-2");

      expect(correctRow.querySelector("[data-glyph]")?.textContent?.trim()).toBeTruthy();
      expect(correctRow.textContent).toContain("Correct");
      expect(incorrectRow.querySelector("[data-glyph]")?.textContent?.trim()).toBeTruthy();
      expect(incorrectRow.textContent).toContain("Not yet");

      const glyphsDiffer =
         correctRow.querySelector("[data-glyph]")?.textContent !==
         incorrectRow.querySelector("[data-glyph]")?.textContent;

      expect(glyphsDiffer).toBe(true);

      cleanup();
   });

   it("colours the two states from growth tokens and from no hex value", () => {
      render(<StepMarks marks={marks} />);

      const correctRow = screen.getByTestId("step-mark-1");
      const incorrectRow = screen.getByTestId("step-mark-2");

      expect(correctRow.getAttribute("style")).toContain("var(--growth-state-correct)");
      expect(incorrectRow.getAttribute("style")).toContain("var(--growth-state-incorrect)");

      cleanup();
   });

   it("renders nothing when the feedback carried no step marks", () => {
      render(<StepMarks marks={[]} />);

      expect(screen.queryByTestId("step-marks")).toBeNull();

      cleanup();
   });
});