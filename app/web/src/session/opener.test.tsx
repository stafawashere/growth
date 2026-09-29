import { describe, expect, it, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import type { ServedItem } from "../api/types";
import { Item, OPENER_NOTE } from "./Item";

function servedItem(isOpener: boolean | undefined): ServedItem {
   return {
      id: "item-1",
      archetype_id: "BC-QA-06004",
      variant_id: null,
      snapshot_id: null,
      parameter_draw: null,
      stem: "Find the accumulated change",
      figure_spec: null,
      options: null,
      calculator_status: null,
      representation: null,
      difficulty_settings: null,
      skills: ["BC-SKL-06001"],
      status: "verified",
      stage: "unsupported",
      format: "short_answer",
      is_probe: false,
      ...(isOpener === undefined ? {} : { is_opener: isOpener, opener_concept: "BC-CON-06001" }),
      served_steps: null,
      self_explanation_prompt: null
   };
}

function renderItem(isOpener: boolean | undefined) {
   return render(
      <Item
         item={servedItem(isOpener)}
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

describe("the productive-failure opener", () => {
   it("serves the opener as an unsupported item under a one-line header and no worked steps", () => {
      renderItem(true);

      expect(screen.getByTestId("opener-note").textContent).toBe(OPENER_NOTE);
      expect(screen.getByTestId("item").getAttribute("data-stage")).toBe("unsupported");
      expect(screen.queryByTestId("worked-steps")).toBeNull();
      expect(screen.getByTestId("math-answer")).toBeTruthy();

      cleanup();
   });

   it("shows no header on an ordinary item, with or without the field", () => {
      renderItem(false);

      expect(screen.queryByTestId("opener-note")).toBeNull();

      cleanup();
      renderItem(undefined);

      expect(screen.queryByTestId("opener-note")).toBeNull();

      cleanup();
   });
});
