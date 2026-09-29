import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { ServedItem } from "../api/types";
import { Item } from "../session/Item";
import { CALCULATOR_PRACTICE } from "./words";

/* docs/calculator/design.md, Where it lives: a calculator item carries "Calculator practice" beside
   its Open Desmos control, and a no-calculator item carries neither. */

function item(calculatorStatus: string): ServedItem {
   return {
      id: "ITM-1",
      archetype_id: "BC-ARCH-0301",
      variant_id: null,
      snapshot_id: null,
      parameter_draw: null,
      stem: "Find the value.",
      figure_spec: null,
      options: null,
      calculator_status: calculatorStatus,
      representation: null,
      difficulty_settings: null,
      skills: ["BC-SKL-0301"],
      status: "published",
      stage: "unsupported",
      format: "short_answer",
      is_probe: false,
      served_steps: null,
      self_explanation_prompt: null
   };
}

function renderItem(calculatorStatus: string) {
   render(
      <Item
         item={item(calculatorStatus)}
         onAnswerChange={vi.fn()}
         answerUnavailable={false}
         onAnswerUnavailable={vi.fn()}
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
}

afterEach(() => {
   cleanup();
});

describe("the calculator practice link on items", () => {
   it("sits beside Open Desmos on a calculator item and opens the procedure cards", () => {
      renderItem("calculator");

      const link = screen.getByRole("link", { name: CALCULATOR_PRACTICE });

      expect(link.getAttribute("href")).toBe("#/calculator/cards");
      expect(link.closest(".desmos-bar")).not.toBeNull();
   });

   it("is absent on a no-calculator item", () => {
      renderItem("no_calculator");

      expect(screen.queryByRole("link", { name: CALCULATOR_PRACTICE })).toBeNull();
   });
});
