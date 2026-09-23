import { describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { AFFORDANCE_ATTRIBUTE, P1_FEEDBACK_AFFORDANCES } from "../affordances";
import { motionClass } from "../styles/motion";
import type { Confidence } from "../api/types";
import { CONFIDENCE_CHOICES, ConfidencePrompt } from "./ConfidencePrompt";

describe("ConfidencePrompt", () => {
   it("carries the confidence affordance and its motion class", () => {
      render(<ConfidencePrompt value={null} onChange={vi.fn()} />);

      const prompt = screen.getByTestId("confidence-prompt");

      expect(prompt.getAttribute(AFFORDANCE_ATTRIBUTE)).toBe(P1_FEEDBACK_AFFORDANCES.confidencePrompt);
      expect(prompt.className).toContain(motionClass("confidencePrompt"));

      cleanup();
   });

   it("offers exactly guess, unsure and confident", () => {
      render(<ConfidencePrompt value={null} onChange={vi.fn()} />);

      const rendered = screen.getAllByRole("radio").map((radio) => (radio as HTMLInputElement).value);
      const expected: Confidence[] = ["guess", "unsure", "confident"];

      expect(rendered).toEqual(expected);
      expect(CONFIDENCE_CHOICES.map((choice) => choice.value)).toEqual(expected);

      cleanup();
   });

   it("asks before the answer is shown, in the student's voice", () => {
      render(<ConfidencePrompt value={null} onChange={vi.fn()} />);

      expect(screen.getByText("Before you see the answer: guess, unsure, or confident?")).toBeTruthy();

      cleanup();
   });

   it("reports the choice the student made", () => {
      const onChange = vi.fn();

      render(<ConfidencePrompt value={null} onChange={onChange} />);
      fireEvent.click(screen.getByRole("radio", { name: "unsure" }));

      expect(onChange).toHaveBeenCalledWith("unsure");

      cleanup();
   });

   it("marks the rating the student already gave", () => {
      render(<ConfidencePrompt value="confident" onChange={vi.fn()} />);

      const confident = screen.getByRole("radio", { name: "confident" }) as HTMLInputElement;

      expect(confident.checked).toBe(true);

      cleanup();
   });
});