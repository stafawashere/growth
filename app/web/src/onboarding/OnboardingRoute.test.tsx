import { afterEach, beforeAll, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";

import * as client from "../api/client";
import type { AttemptResult, DiagnosticResult, DiagnosticServedItem, SessionPayload } from "../api/types";
import { OnboardingRoute } from "./OnboardingRoute";

vi.mock("../api/client");

const mocked = vi.mocked(client);

/* The same MathfieldElement stand-in as input/MathField.test.tsx: MathLive resolves to its SSR
   stub under vitest, so only getValue and the input event are provided. */
class StubMathField extends HTMLElement {
   private currentValue = "[]";

   getValue(): string {
      return this.currentValue;
   }

   setStubValue(mathJsonString: string) {
      this.currentValue = mathJsonString;
      this.dispatchEvent(new Event("input", { bubbles: true }));
   }
}

beforeAll(() => {
   if (customElements.get("math-field") === undefined) {
      customElements.define("math-field", StubMathField);
   }
});

afterEach(() => {
   cleanup();
   vi.resetAllMocks();
});

const session = { id: "SES-D", mode: "diagnostic" } as SessionPayload;

function item(id: string, position: number): DiagnosticServedItem {
   return {
      id,
      archetype_id: "BC-QA-01004",
      variant_id: null,
      snapshot_id: null,
      parameter_draw: null,
      stem: `Evaluate item ${id}`,
      figure_spec: null,
      options: null,
      calculator_status: null,
      representation: null,
      difficulty_settings: null,
      skills: ["BC-SKL-01024"],
      status: "verified",
      stage: "unsupported",
      format: "short_answer",
      is_probe: false,
      served_steps: null,
      self_explanation_prompt: null,
      diagnostic_position: position,
      diagnostic_cap: 30
   };
}

const attempt = { id: "ATT-1", item_id: "ITM-A", correct: null } as AttemptResult;

const result: DiagnosticResult = {
   session_id: "SES-D",
   finished: true,
   asked: 2,
   cap: 30,
   stop_reason: "pool_exhausted",
   units: [
      { unit: "BC-UNIT-01", title: "Limits and Continuity", state: "fluent" },
      { unit: "BC-UNIT-02", title: "Differentiation: Definition and Fundamental Properties", state: "partial" },
      { unit: "BC-UNIT-06", title: "Integration and Accumulation of Change", state: "not_started" },
      { unit: "BC-UNIT-03", title: "Differentiation: Composite, Implicit, and Inverse Functions", state: "unresolved" },
      { unit: "BC-UNIT-10", title: "Infinite Sequences and Series", state: "not_probed" }
   ],
   unprobeable_units: ["BC-UNIT-10"]
};

function serveTwoThenFinish() {
   mocked.openDiagnostic.mockResolvedValue(session);
   mocked.readNextItem
      .mockResolvedValueOnce({ item: item("ITM-A", 0), diagnostic_finished: false })
      .mockResolvedValueOnce({ item: item("ITM-B", 1), diagnostic_finished: false })
      .mockResolvedValue({ item: null, diagnostic_finished: true });
   mocked.submitAttempt.mockResolvedValue(attempt);
   mocked.readDiagnostic.mockResolvedValue(result);
}

describe("the onboarding diagnostic", () => {
   it("runs intro, items and result, posting each answer with no rating and no feedback", async () => {
      serveTwoThenFinish();
      const onFinished = vi.fn();
      render(<OnboardingRoute reason="first_login" resumeSessionId={null} onFinished={onFinished} />);

      expect(screen.getByTestId("diagnostic-intro").textContent).toContain("no score");
      expect(mocked.openDiagnostic).not.toHaveBeenCalled();

      fireEvent.click(screen.getByRole("button", { name: "Start the diagnostic" }));

      await screen.findByText("Evaluate item ITM-A");

      expect(screen.getByText("Question 1 of at most 30")).toBeTruthy();
      expect(screen.getByTestId("diagnostic-item").getAttribute("data-state")).toBe("unanswered");

      fireEvent.click(screen.getByRole("button", { name: "I have not learned this yet" }));

      await screen.findByText("Evaluate item ITM-B");

      expect(mocked.submitAttempt).toHaveBeenCalledTimes(1);
      expect(mocked.submitAttempt.mock.calls[0][0]).toBe("SES-D");
      expect(mocked.submitAttempt.mock.calls[0][1]).toMatchObject({ item_id: "ITM-A", answer: { not_learned: true } });
      expect(screen.getByText("Question 2 of at most 30")).toBeTruthy();

      const field = document.querySelector("math-field") as StubMathField;

      field.setStubValue(JSON.stringify(["Rational", 5, 6]));

      await waitFor(() => expect(screen.getByTestId("diagnostic-item").getAttribute("data-state")).toBe("answered"));

      fireEvent.click(screen.getByRole("button", { name: "Check my answer" }));

      const shown = await screen.findByTestId("diagnostic-result");

      expect(mocked.submitAttempt.mock.calls[1][1]).toMatchObject({
         item_id: "ITM-B",
         answer: { mathjson: ["Rational", 5, 6] }
      });
      expect(mocked.submitConfidence).not.toHaveBeenCalled();
      expect(mocked.readFeedback).not.toHaveBeenCalled();
      expect(mocked.readDiagnostic).toHaveBeenCalledWith("SES-D");

      const text = shown.textContent ?? "";

      for (const words of ["Fluent", "Partly there", "Not started yet", "Not placed yet", "Not asked yet"]) {
         expect(text).toContain(words);
      }

      expect(text).not.toMatch(/\d/);
      expect(text).not.toContain("%");

      fireEvent.click(screen.getByRole("button", { name: "Go to today's set" }));

      expect(onFinished).toHaveBeenCalledTimes(1);
   });

   it("keeps Check my answer shut until something is typed", async () => {
      serveTwoThenFinish();
      render(<OnboardingRoute reason="first_login" resumeSessionId={null} onFinished={vi.fn()} />);
      fireEvent.click(screen.getByRole("button", { name: "Start the diagnostic" }));
      await screen.findByText("Evaluate item ITM-A");

      const check = screen.getByRole("button", { name: "Check my answer" }) as HTMLButtonElement;

      expect(check.disabled).toBe(true);

      fireEvent.click(check);

      expect(mocked.submitAttempt).not.toHaveBeenCalled();
   });

   it("says a long-gap run updates and never resets what the app knows", () => {
      serveTwoThenFinish();
      render(<OnboardingRoute reason="long_gap" resumeSessionId={null} onFinished={vi.fn()} />);

      const intro = screen.getByTestId("diagnostic-intro").textContent ?? "";

      expect(intro).toContain("re-diagnostic");
      expect(intro).toContain("never resets");
   });

   it("resumes an open diagnostic without the intro and without opening another", async () => {
      serveTwoThenFinish();
      render(<OnboardingRoute reason="first_login" resumeSessionId="SES-OPEN" onFinished={vi.fn()} />);

      await screen.findByText("Evaluate item ITM-A");

      expect(mocked.readNextItem).toHaveBeenCalledWith("SES-OPEN");
      expect(mocked.openDiagnostic).not.toHaveBeenCalled();
      expect(screen.queryByTestId("diagnostic-intro")).toBeNull();
   });
});
