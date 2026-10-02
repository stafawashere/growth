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

   it("is a modal dialog that takes focus on its first word and hands it back when it closes", () => {
      const opener = document.createElement("button");

      document.body.appendChild(opener);
      opener.focus();

      const { unmount } = render(<ConfidencePrompt value={null} onChange={vi.fn()} onClose={vi.fn()} />);
      const dialog = screen.getByRole("dialog");

      expect(dialog.getAttribute("aria-modal")).toBe("true");
      expect(dialog.getAttribute("aria-labelledby")).not.toBeNull();
      expect(document.activeElement).toBe(screen.getByRole("radio", { name: "guess" }));

      unmount();

      expect(document.activeElement).toBe(opener);

      opener.remove();
      cleanup();
   });

   it("chooses on the digit keys and on Space, and only moves between the words on the arrows", () => {
      const onChange = vi.fn();

      render(<ConfidencePrompt value={null} onChange={onChange} onClose={vi.fn()} />);

      const guess = screen.getByRole("radio", { name: "guess" });

      fireEvent.keyDown(guess, { key: "ArrowDown" });

      expect(document.activeElement).toBe(screen.getByRole("radio", { name: "unsure" }));
      expect(onChange).not.toHaveBeenCalled();

      fireEvent.keyDown(document.activeElement as HTMLElement, { key: "ArrowUp" });

      expect(document.activeElement).toBe(guess);

      fireEvent.keyDown(guess, { key: "3" });

      expect(onChange).toHaveBeenCalledWith("confident");

      cleanup();
   });

   it("closes on Escape and on its Close button without choosing, and offers no close when the rating is required", () => {
      const onChange = vi.fn();
      const onClose = vi.fn();

      render(<ConfidencePrompt value={null} onChange={onChange} onClose={onClose} />);
      fireEvent.keyDown(screen.getByRole("radio", { name: "guess" }), { key: "Escape" });

      expect(onClose).toHaveBeenCalledTimes(1);

      fireEvent.click(screen.getByRole("button", { name: "Close" }));

      expect(onClose).toHaveBeenCalledTimes(2);
      expect(onChange).not.toHaveBeenCalled();

      cleanup();
      render(<ConfidencePrompt value={null} onChange={onChange} />);

      expect(screen.queryByRole("button", { name: "Close" })).toBeNull();

      fireEvent.keyDown(screen.getByRole("radio", { name: "guess" }), { key: "Escape" });

      expect(onChange).not.toHaveBeenCalled();

      cleanup();
   });
});