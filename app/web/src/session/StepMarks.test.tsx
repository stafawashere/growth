import { describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { AFFORDANCE_ATTRIBUTE, P1_FEEDBACK_AFFORDANCES } from "../affordances";
import { motionClass } from "../styles/motion";
import type { StepMark } from "../api/types";
import { CORRECT_WORD, GIVEN_WORD, INCORRECT_WORD, StepMarks } from "./StepMarks";

function given(index: number, text: string): StepMark {
   return { index, text, given: true, correct: null };
}

function blank(index: number, correct: boolean | null): StepMark {
   return { index, text: "f'(x) = 2x sin(x) + x^2 cos(x)", given: false, correct };
}

const completionMarks = (verdict: boolean | null): StepMark[] => [
   given(1, "Name the factors: u = x^2, v = sin(x)"),
   given(2, "u' = 2x, v' = cos(x)"),
   blank(3, verdict)
];

const exampleMarks: StepMark[] = [
   given(1, "Name the factors: u = x^2, v = sin(x)"),
   given(2, "u' = 2x, v' = cos(x)"),
   given(3, "f'(x) = 2x sin(x) + x^2 cos(x)")
];

function glyphOf(row: HTMLElement) {
   return row.querySelector("[data-glyph]")?.textContent?.trim() ?? null;
}

describe("StepMarks", () => {
   it("carries the step verification affordance and its motion class", () => {
      render(<StepMarks marks={completionMarks(true)} />);

      const panel = screen.getByTestId("step-marks");

      expect(panel.getAttribute(AFFORDANCE_ATTRIBUTE)).toBe(P1_FEEDBACK_AFFORDANCES.stepVerificationMark);
      expect(panel.className).toContain(motionClass("stepVerificationMark"));

      cleanup();
   });

   it("labels a given step as given, with no verdict word, no glyph and no verdict colour", () => {
      render(<StepMarks marks={completionMarks(false)} />);

      for (const index of [1, 2]) {
         const row = screen.getByTestId(`step-mark-${index}`);
         const style = row.getAttribute("style") ?? "";

         expect(row.textContent).toContain(GIVEN_WORD);
         expect(row.textContent).not.toContain(CORRECT_WORD);
         expect(row.textContent).not.toContain(INCORRECT_WORD);
         expect(glyphOf(row)).toBeNull();
         expect(style).not.toContain("--growth-state-");
      }

      cleanup();
   });

   it("states the blank's verdict with a word and a glyph, never colour alone", () => {
      render(<StepMarks marks={completionMarks(true)} />);

      const correctRow = screen.getByTestId("step-mark-3");
      const correctGlyph = glyphOf(correctRow);

      expect(correctGlyph).toBeTruthy();
      expect(correctRow.textContent).toContain(CORRECT_WORD);
      expect(correctRow.textContent).not.toContain(GIVEN_WORD);
      expect(correctRow.getAttribute("style")).toContain("var(--growth-state-correct)");

      cleanup();

      render(<StepMarks marks={completionMarks(false)} />);

      const incorrectRow = screen.getByTestId("step-mark-3");

      expect(glyphOf(incorrectRow)).toBeTruthy();
      expect(glyphOf(incorrectRow)).not.toBe(correctGlyph);
      expect(incorrectRow.textContent).toContain(INCORRECT_WORD);
      expect(incorrectRow.getAttribute("style")).toContain("var(--growth-state-incorrect)");

      cleanup();
   });

   it("shows every step of a worked example as given and none as verified", () => {
      render(<StepMarks marks={exampleMarks} />);

      const panel = screen.getByTestId("step-marks");

      expect(panel.querySelectorAll("[data-given]").length).toBe(exampleMarks.length);
      expect(panel.querySelectorAll("[data-glyph]").length).toBe(0);
      expect(panel.textContent).not.toContain(CORRECT_WORD);
      expect(panel.textContent).not.toContain(INCORRECT_WORD);

      cleanup();
   });

   it("gives no verdict to a blank that has none yet", () => {
      render(<StepMarks marks={completionMarks(null)} />);

      const row = screen.getByTestId("step-mark-3");

      expect(glyphOf(row)).toBeNull();
      expect(row.textContent).not.toContain(CORRECT_WORD);
      expect(row.textContent).not.toContain(INCORRECT_WORD);

      cleanup();
   });

   it("renders nothing when the feedback carried no step marks", () => {
      render(<StepMarks marks={[]} />);

      expect(screen.queryByTestId("step-marks")).toBeNull();

      cleanup();
   });
});