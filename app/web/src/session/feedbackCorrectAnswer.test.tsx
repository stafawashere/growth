import { beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import type { AttemptResult, CorrectAnswer, FadingStage, FeedbackPayload, ServedItem, SessionPayload } from "../api/types";
import * as client from "../api/client";
import { CORRECT_RESULT_LABEL, ElaboratedPanel } from "./ElaboratedPanel";
import { COMMIT_LABEL } from "./Item";
import { OPENER_WITHOUT_TUTOR, SessionScreen } from "./SessionScreen";

vi.mock("../api/client");

const mocked = vi.mocked(client);

const KEYED_LABEL = "The limit is seven halves";

const elaborated = {
   violated_step: "Evaluate the simplified expression at the target",
   observed_behavior: "The factor was cancelled from a sum",
   scoring_consequence: "The answer point is lost",
   worked_solution: null,
   error_id: null
};

const session: SessionPayload = {
   id: "session-1",
   mode: "practice",
   sub_mode: null,
   started_at: "2027-01-05T09:00:00Z",
   ended_at: null,
   updates_mastery: true,
   snapshot_id: null,
   queue: {
      block1: [],
      block2: [],
      block3: [],
      block4: [],
      forecasts: {},
      coverage_gaps: [],
      interleaving_satisfied: true,
      interleaving_shortfalls: []
   },
   remaining: []
};

function servedItem(stage: FadingStage, isOpener = false): ServedItem {
   const showsSteps = stage !== "unsupported";

   return {
      id: "item-1",
      archetype_id: "BC-QA-01007",
      variant_id: null,
      snapshot_id: null,
      parameter_draw: null,
      stem: "Find the limit",
      figure_spec: null,
      options: null,
      calculator_status: null,
      representation: null,
      difficulty_settings: null,
      skills: ["BC-SKL-0101"],
      status: "published",
      stage,
      format: "short_answer",
      is_probe: false,
      ...(isOpener ? { is_opener: true, opener_concept: "BC-CON-01001" } : {}),
      served_steps: showsSteps ? [{ index: 1, text: "Factor the numerator" }] : null,
      self_explanation_prompt: null
   };
}

function attempt(stage: FadingStage, correct: boolean): AttemptResult {
   return {
      id: "attempt-1",
      item_id: "item-1",
      correct,
      confidence: "unsure",
      served_stage: stage,
      format: "short_answer",
      p_split: null,
      p_compensatory: null
   };
}

function payload(fields: Partial<FeedbackPayload> & Pick<FeedbackPayload, "kind" | "stage">): FeedbackPayload {
   return {
      step_marks: [],
      elaborated: null,
      self_explanation_prompt: null,
      confidence: "unsure",
      sentence: null,
      tutor_unavailable: false,
      ...fields
   };
}

function completionMarks(correct: boolean) {
   return [
      { index: 1, text: "Factor the numerator", given: true, correct: null },
      { index: 2, text: "Evaluate at the target", given: false, correct }
   ];
}

async function answerAndReadFeedback(item: ServedItem, result: AttemptResult, feedback: FeedbackPayload) {
   mocked.openSession.mockResolvedValue(session);
   mocked.readSession.mockResolvedValue(session);
   mocked.readNextItem.mockResolvedValue({ item });
   mocked.submitAttempt.mockResolvedValue(result);
   mocked.readFeedback.mockResolvedValue(feedback);

   render(<SessionScreen resumeSessionId={null} />);

   await screen.findByText("Find the limit");
   fireEvent.click(screen.getByRole("button", { name: COMMIT_LABEL }));
   await screen.findByTestId("feedback");
}

beforeEach(() => {
   vi.clearAllMocks();
   cleanup();
});

describe("the correct result after a wrong answer", () => {
   it("sits after the violated step and before the observed behaviour, as a label or as MathJSON", () => {
      const labelled: CorrectAnswer = { label: KEYED_LABEL, mathjson: null };

      render(<ElaboratedPanel elaborated={elaborated} sentence={null} correctAnswer={labelled} />);

      const panel = screen.getByTestId("elaborated-panel");
      const order = Array.from(panel.querySelectorAll("[data-testid]")).map((node) => node.getAttribute("data-testid"));
      const shown = screen.getByTestId("correct-answer");

      expect(order.indexOf("violated-step")).toBeLessThan(order.indexOf("correct-answer"));
      expect(order.indexOf("correct-answer")).toBeLessThan(order.indexOf("observed-behavior"));
      expect(shown.textContent).toContain(CORRECT_RESULT_LABEL);
      expect(shown.textContent).toContain(KEYED_LABEL);

      cleanup();

      render(<ElaboratedPanel elaborated={elaborated} sentence={null} correctAnswer={{ label: null, mathjson: ["Rational", 7, 2] }} />);

      expect(screen.getByTestId("correct-answer").querySelector(".katex, math")).not.toBeNull();
   });

   it("is shown on a wrong unsupported answer", async () => {
      await answerAndReadFeedback(
         servedItem("unsupported"),
         attempt("unsupported", false),
         payload({ kind: "elaborated", stage: "unsupported", elaborated, correct_answer: { label: KEYED_LABEL, mathjson: null } })
      );

      expect(screen.getByTestId("correct-answer").textContent).toContain(KEYED_LABEL);
   });

   it("is shown after the step marks on a wrong completion blank", async () => {
      await answerAndReadFeedback(
         servedItem("completion"),
         attempt("completion", false),
         payload({
            kind: "step_verification",
            stage: "completion",
            step_marks: completionMarks(false),
            correct_answer: { label: KEYED_LABEL, mathjson: null }
         })
      );

      const marks = screen.getByTestId("step-marks");
      const shown = screen.getByTestId("correct-answer");

      expect(marks.compareDocumentPosition(shown) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
   });

   it("is not shown for a correct answer, even if a payload carried one", async () => {
      await answerAndReadFeedback(
         servedItem("completion"),
         attempt("completion", true),
         payload({
            kind: "step_verification",
            stage: "completion",
            step_marks: completionMarks(true),
            correct_answer: { label: KEYED_LABEL, mathjson: null }
         })
      );

      expect(screen.queryByTestId("correct-answer")).toBeNull();
   });
});

describe("an opener's feedback without the tutor", () => {
   it("says the comparison needs the tutor and shows the method's first step", async () => {
      await answerAndReadFeedback(
         servedItem("unsupported", true),
         attempt("unsupported", true),
         payload({ kind: "correct", stage: "unsupported", comparison: null, first_worked_step: { index: 1, text: "Factor the numerator" } })
      );

      const fallback = screen.getByTestId("opener-without-tutor");

      expect(fallback.textContent).toContain(OPENER_WITHOUT_TUTOR);
      expect(screen.getByTestId("opener-first-step").textContent).toContain("Factor the numerator");
   });

   it("is not drawn when the comparison is there", async () => {
      await answerAndReadFeedback(
         servedItem("unsupported", true),
         attempt("unsupported", false),
         payload({
            kind: "comparison",
            stage: "unsupported",
            comparison: {
               label: "The method's first step is to factor.",
               first_step: "factor",
               observed_behavior: "",
               attempt: {},
               worked_steps: [{ index: 1, text: "Factor the numerator" }],
               error_id: null
            }
         })
      );

      expect(screen.getByTestId("comparison-panel")).toBeTruthy();
      expect(screen.queryByTestId("opener-without-tutor")).toBeNull();
      expect(screen.queryByTestId("correct-answer")).toBeNull();
   });
});
