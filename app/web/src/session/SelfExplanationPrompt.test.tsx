import { describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { AFFORDANCE_ATTRIBUTE, P1_FEEDBACK_AFFORDANCES } from "../affordances";
import { motionClass } from "../styles/motion";
import { SelfExplanationPrompt } from "./SelfExplanationPrompt";

const prompt = "Which rule justifies step 3, and why does it apply here?";

describe("SelfExplanationPrompt", () => {
   it("carries the self explanation affordance and its motion class", () => {
      render(<SelfExplanationPrompt prompt={prompt} value="" onChange={vi.fn()} />);

      const panel = screen.getByTestId("self-explanation-prompt");

      expect(panel.getAttribute(AFFORDANCE_ATTRIBUTE)).toBe(P1_FEEDBACK_AFFORDANCES.selfExplanationPrompt);
      expect(panel.className).toContain(motionClass("selfExplanationPrompt"));

      cleanup();
   });

   it("renders the prompt the server wrote, not a prompt of its own", () => {
      render(<SelfExplanationPrompt prompt={prompt} value="" onChange={vi.fn()} />);

      expect(screen.getByLabelText(prompt)).toBeTruthy();

      cleanup();
   });

   it("reports what the student wrote", () => {
      const onChange = vi.fn();

      render(<SelfExplanationPrompt prompt={prompt} value="" onChange={onChange} />);
      fireEvent.change(screen.getByLabelText(prompt), { target: { value: "The product rule, because f is a product." } });

      expect(onChange).toHaveBeenCalledWith("The product rule, because f is a product.");

      cleanup();
   });

   it("renders nothing when no prompt was attached to this item", () => {
      render(<SelfExplanationPrompt prompt={null} value="" onChange={vi.fn()} />);

      expect(screen.queryByTestId("self-explanation-prompt")).toBeNull();

      cleanup();
   });
});