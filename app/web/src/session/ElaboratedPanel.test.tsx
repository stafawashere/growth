import { describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { AFFORDANCE_ATTRIBUTE, P1_FEEDBACK_AFFORDANCES } from "../affordances";
import { motionClass } from "../styles/motion";
import type { ElaboratedPayload } from "../api/types";
import { ElaboratedPanel } from "./ElaboratedPanel";

const elaborated: ElaboratedPayload = {
   violated_step: "Product rule applied to both factors at once",
   observed_behavior: "Each factor was differentiated separately and the two derivatives multiplied",
   scoring_consequence: "On an AP rubric this loses the product rule point, and the answer point with it",
   worked_solution: null,
   error_id: "BC-ERR-0304"
};

describe("ElaboratedPanel", () => {
   it("carries the elaborated feedback affordance and its motion class", () => {
      render(<ElaboratedPanel elaborated={elaborated} sentence={null} />);

      const panel = screen.getByTestId("elaborated-panel");

      expect(panel.getAttribute(AFFORDANCE_ATTRIBUTE)).toBe(P1_FEEDBACK_AFFORDANCES.elaboratedFeedbackPanel);
      expect(panel.className).toContain(motionClass("elaboratedFeedbackPanel"));

      cleanup();
   });

   it("names the violated step, the observed behaviour and the scoring consequence", () => {
      render(<ElaboratedPanel elaborated={elaborated} sentence={null} />);

      expect(screen.getByText(elaborated.violated_step as string)).toBeTruthy();
      expect(screen.getByText(elaborated.observed_behavior as string)).toBeTruthy();
      expect(screen.getByText(elaborated.scoring_consequence as string)).toBeTruthy();

      cleanup();
   });

   it("shows the tutor sentence only when the feedback carried one", () => {
      render(<ElaboratedPanel elaborated={elaborated} sentence={null} />);
      expect(screen.queryByTestId("tutor-sentence")).toBeNull();
      cleanup();

      render(<ElaboratedPanel elaborated={elaborated} sentence="Start again from the factors and keep one whole." />);
      expect(screen.getByTestId("tutor-sentence").textContent).toContain("keep one whole");
      cleanup();
   });

   it("states the incorrect result with a word and a glyph, not colour alone", () => {
      render(<ElaboratedPanel elaborated={elaborated} sentence={null} />);

      const verdict = screen.getByTestId("elaborated-verdict");

      expect(verdict.querySelector("[data-glyph]")?.textContent?.trim()).toBeTruthy();
      expect(verdict.textContent).toContain("Not yet");
      expect(verdict.getAttribute("style")).toContain("var(--growth-state-incorrect)");

      cleanup();
   });

   it("renders nothing when the feedback carried no elaboration", () => {
      render(<ElaboratedPanel elaborated={null} sentence={null} />);

      expect(screen.queryByTestId("elaborated-panel")).toBeNull();

      cleanup();
   });
});