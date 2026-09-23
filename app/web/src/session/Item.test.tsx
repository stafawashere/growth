import { describe, expect, it, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { P1_FEEDBACK_AFFORDANCES, AFFORDANCE_ATTRIBUTE } from "../affordances";
import type { FadingStage, ServedFormat, ServedItem, ServedStep } from "../api/types";
import type { ItemProps } from "./Item";
import { ANSWER_UNAVAILABLE, COMMIT_LABEL, Item } from "./Item";

const SELF_EXPLANATION_PROMPT = "Which rule justifies step 3, and why does it apply here?";

const workedSteps: ServedStep[] = [
   { index: 1, text: "Name the factors: u = x^2, v = sin(x)" },
   { index: 2, text: "u' = 2x, v' = cos(x)" },
   { index: 3, text: "Product rule: f' = u'v + uv'" },
   { index: 4, text: "f'(x) = 2x sin(x) + x^2 cos(x)" }
];

/* app/runtime/bank.py served_steps: every step at example, all but the last at completion. */
function servedStepsAt(stage: FadingStage): ServedStep[] | null {
   if (stage === "example") {
      return workedSteps;
   }

   if (stage === "completion") {
      return workedSteps.slice(0, -1);
   }

   return null;
}

function servedItem(
   stage: FadingStage,
   format: ServedFormat,
   steps: ServedStep[] | null = servedStepsAt(stage)
): ServedItem {
   return {
      id: "item-1",
      archetype_id: "BC-ARCH-0301",
      variant_id: null,
      snapshot_id: null,
      parameter_draw: null,
      stem: "Differentiate f(x) = x^2 sin(x)",
      figure_spec: null,
      options: format === "mcq" ? [{ id: "opt-a", label: "2x sin(x)" }, { id: "opt-b", label: "2x cos(x)" }] : null,
      calculator_status: null,
      representation: null,
      difficulty_settings: null,
      skills: ["BC-SKL-0301"],
      status: "published",
      stage,
      format,
      is_probe: false,
      served_steps: steps,
      self_explanation_prompt: stage === "example" ? SELF_EXPLANATION_PROMPT : null
   };
}

function renderItem(
   stage: FadingStage,
   format: ServedFormat,
   steps: ServedStep[] | null = servedStepsAt(stage),
   answerUnavailable = false,
   onAnswerUnavailable: ItemProps["onAnswerUnavailable"] = vi.fn(),
   awaitingConfidence = false
) {
   return render(
      <Item
         item={servedItem(stage, format, steps)}
         onAnswerChange={vi.fn()}
         answerUnavailable={answerUnavailable}
         onAnswerUnavailable={onAnswerUnavailable}
         selectedOptionId={null}
         onOptionChange={vi.fn()}
         confidence={null}
         onConfidenceChange={vi.fn()}
         selfExplanation=""
         onSelfExplanationChange={vi.fn()}
         onCommit={vi.fn()}
         awaitingConfidence={awaitingConfidence}
      />
   );
}

function affordanceValues() {
   const nodes = Array.from(document.querySelectorAll(`[${AFFORDANCE_ATTRIBUTE}]`));

   return nodes.map((node) => node.getAttribute(AFFORDANCE_ATTRIBUTE));
}

describe("Item fading stages", () => {
   it("renders the worked example and the self explanation prompt at stage example, and no confidence prompt", () => {
      renderItem("example", "short_answer");

      expect(screen.getByText(workedSteps[3].text)).toBeTruthy();
      expect(affordanceValues()).toContain(P1_FEEDBACK_AFFORDANCES.selfExplanationPrompt);
      expect(affordanceValues()).not.toContain(P1_FEEDBACK_AFFORDANCES.confidencePrompt);

      cleanup();
   });

   it("blanks the last worked step and gives the earlier ones at stage completion", () => {
      renderItem("completion", "short_answer");

      expect(screen.getByText(workedSteps[0].text)).toBeTruthy();
      expect(screen.getByText(workedSteps[1].text)).toBeTruthy();
      expect(screen.getByText(workedSteps[2].text)).toBeTruthy();
      expect(screen.queryByText(workedSteps[3].text)).toBeNull();
      expect(screen.getByTestId("blanked-step").getAttribute("data-step-index")).toBe("4");

      cleanup();
   });

   it("collects confidence before feedback at stage completion and at stage unsupported", () => {
      renderItem("completion", "short_answer");
      expect(affordanceValues()).toContain(P1_FEEDBACK_AFFORDANCES.confidencePrompt);
      cleanup();

      renderItem("unsupported", "short_answer");
      expect(affordanceValues()).toContain(P1_FEEDBACK_AFFORDANCES.confidencePrompt);
      cleanup();
   });

   it("shows the problem alone at stage unsupported, with no worked steps and no self explanation prompt", () => {
      renderItem("unsupported", "short_answer");

      expect(screen.queryByText(workedSteps[0].text)).toBeNull();
      expect(screen.queryByTestId("worked-steps")).toBeNull();
      expect(affordanceValues()).not.toContain(P1_FEEDBACK_AFFORDANCES.selfExplanationPrompt);

      cleanup();
   });

   it("renders the stem at every stage", () => {
      const stages: FadingStage[] = ["example", "completion", "unsupported"];

      for (const stage of stages) {
         renderItem(stage, "short_answer");
         expect(screen.getByText("Differentiate f(x) = x^2 sin(x)")).toBeTruthy();
         cleanup();
      }
   });
});

describe("Item served format", () => {
   it("renders the math field for a short answer item at stage unsupported", () => {
      renderItem("unsupported", "short_answer");

      expect(screen.getByTestId("math-answer")).toBeTruthy();
      expect(screen.queryByTestId("mcq-answer")).toBeNull();

      cleanup();
   });

   it("renders the option control for an mcq item at stage unsupported", () => {
      renderItem("unsupported", "mcq");

      expect(screen.getByTestId("mcq-answer")).toBeTruthy();
      expect(screen.queryByTestId("math-answer")).toBeNull();

      cleanup();
   });

   it("renders the math field at stage completion whatever format the item names", () => {
      renderItem("completion", "mcq");

      expect(screen.getByTestId("math-answer")).toBeTruthy();
      expect(screen.queryByTestId("mcq-answer")).toBeNull();

      cleanup();
   });
});

describe("Item worked step guard", () => {
   it("refuses the example stage when no worked steps arrived, rather than inventing them", () => {
      renderItem("example", "short_answer", []);

      expect(screen.getByTestId("worked-steps-unavailable")).toBeTruthy();
      expect(screen.queryByTestId("worked-steps")).toBeNull();

      cleanup();
   });

   it("draws a two step solution at completion, the first step given and the second blanked", () => {
      renderItem("completion", "short_answer", [workedSteps[0]]);

      expect(screen.queryByTestId("worked-steps-unavailable")).toBeNull();
      expect(screen.getByText(workedSteps[0].text)).toBeTruthy();
      expect(screen.getByTestId("blanked-step").getAttribute("data-step-index")).toBe("2");

      cleanup();
   });

   it("refuses the completion stage below the two step minimum, which served no given step", () => {
      renderItem("completion", "short_answer", []);

      expect(screen.getByTestId("worked-steps-unavailable")).toBeTruthy();
      expect(screen.queryByTestId("blanked-step")).toBeNull();

      cleanup();
   });
});

describe("Item copy", () => {
   it("asks in the student's voice at the stages that commit an answer", () => {
      renderItem("completion", "short_answer");

      expect(screen.getByRole("button", { name: "Check my answer" })).toBeTruthy();

      cleanup();
   });
});

describe("Item math input failure", () => {
   it("refuses construction when nothing is given to carry a math input failure", () => {
      const missingHandler = undefined as unknown as ItemProps["onAnswerUnavailable"];

      const build = () =>
         render(
            <Item
               item={servedItem("unsupported", "short_answer")}
               onAnswerChange={vi.fn()}
               answerUnavailable={false}
               onAnswerUnavailable={missingHandler}
               selectedOptionId={null}
               onOptionChange={vi.fn()}
               confidence={null}
               onConfidenceChange={vi.fn()}
               selfExplanation=""
               onSelfExplanationChange={vi.fn()}
               onCommit={vi.fn()}
               awaitingConfidence={false}
            />
         );

      expect(build).toThrow(/onAnswerUnavailable/);

      cleanup();
   });

   it("tells the student the problem takes no answer and withdraws the commit button", () => {
      renderItem("unsupported", "short_answer", null, true);

      expect(screen.getByTestId("answer-unavailable").textContent).toBe(ANSWER_UNAVAILABLE);
      expect(screen.queryByRole("button", { name: COMMIT_LABEL })).toBeNull();
      expect(affordanceValues()).not.toContain(P1_FEEDBACK_AFFORDANCES.confidencePrompt);

      cleanup();
   });

   it("leaves an mcq item alone, since no math field failed there", () => {
      renderItem("unsupported", "mcq", null, true);

      expect(screen.queryByTestId("answer-unavailable")).toBeNull();
      expect(screen.getByRole("button", { name: COMMIT_LABEL })).toBeTruthy();

      cleanup();
   });
});

describe("Item waiting on the rating the attempt was committed without", () => {
   it("keeps the confidence prompt and withdraws the answer entry and the commit button", () => {
      const stages: FadingStage[] = ["completion", "unsupported"];

      for (const stage of stages) {
         renderItem(stage, "short_answer", servedStepsAt(stage), false, vi.fn(), true);

         expect(affordanceValues()).toContain(P1_FEEDBACK_AFFORDANCES.confidencePrompt);
         expect(screen.queryByRole("button", { name: COMMIT_LABEL })).toBeNull();
         expect(screen.queryByTestId("math-answer")).toBeNull();
         expect(screen.getByText("Differentiate f(x) = x^2 sin(x)")).toBeTruthy();

         cleanup();
      }
   });

   it("still collects no rating at stage example, which commits no answer to rate", () => {
      renderItem("example", "short_answer", servedStepsAt("example"), false, vi.fn(), true);

      expect(affordanceValues()).not.toContain(P1_FEEDBACK_AFFORDANCES.confidencePrompt);

      cleanup();
   });
});