import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { ServedItem } from "../api/types";
import { noCalculatorPart, calculatorPart } from "../assessment/fixtures";
import { PartRunner } from "../assessment/PartRunner";
import { Item } from "../session/Item";
import { CLOSE_DESMOS_LABEL, DESMOS_OPENS_IN, DESMOS_TITLE, DESMOS_URL, DesmosPanel, OPEN_DESMOS_LABEL } from "./DesmosPanel";

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

function renderPart(part: ReturnType<typeof calculatorPart>) {
   render(<PartRunner part={part} radianNote="Radian mode." sectionCount={42} onSave={vi.fn()} onSubmit={vi.fn()} onTimeUp={vi.fn()} />);
}

afterEach(() => {
   cleanup();
});

describe("Desmos on calculator questions", () => {
   it("opens the Desmos calculator in the page from a calculator item, and closes it again", () => {
      renderItem("calculator");

      expect(screen.queryByTitle(DESMOS_TITLE)).toBeNull();

      fireEvent.click(screen.getByRole("button", { name: OPEN_DESMOS_LABEL }));

      expect(screen.getByTitle(DESMOS_TITLE).getAttribute("src")).toBe(DESMOS_URL);

      fireEvent.click(screen.getByRole("button", { name: CLOSE_DESMOS_LABEL }));

      expect(screen.queryByTitle(DESMOS_TITLE)).toBeNull();
   });

   it("offers no Desmos on a no-calculator item", () => {
      renderItem("no_calculator");

      expect(screen.queryByRole("button", { name: OPEN_DESMOS_LABEL })).toBeNull();
   });

   it("offers Desmos on a calculator part and removes it from a no-calculator part", () => {
      renderPart(calculatorPart());

      expect(screen.getByRole("button", { name: OPEN_DESMOS_LABEL })).toBeTruthy();

      cleanup();
      renderPart(noCalculatorPart());

      expect(screen.queryByRole("button", { name: OPEN_DESMOS_LABEL })).toBeNull();
   });
});

describe("which Desmos opens, and how", () => {
   afterEach(() => {
      vi.restoreAllMocks();
   });

   it("frames the College Board version Bluebook carries, not the public calculator", () => {
      render(<DesmosPanel />);
      fireEvent.click(screen.getByRole("button", { name: OPEN_DESMOS_LABEL }));

      expect(DESMOS_OPENS_IN).toBe("frame");
      expect(screen.getByTitle(DESMOS_TITLE).getAttribute("src")).toBe("https://www.desmos.com/testing/collegeboard/graphing");
   });

   it("opens already when asked to open by default", () => {
      render(<DesmosPanel openByDefault />);

      expect(screen.getByTitle(DESMOS_TITLE)).toBeTruthy();
      expect(screen.getByRole("button", { name: CLOSE_DESMOS_LABEL }).getAttribute("aria-expanded")).toBe("true");
   });

   it("opens the same address in its own window, with no opener, when set to window", () => {
      const open = vi.spyOn(window, "open").mockReturnValue(null);

      render(<DesmosPanel opensIn="window" openByDefault />);

      expect(screen.queryByTitle(DESMOS_TITLE)).toBeNull();

      fireEvent.click(screen.getByRole("button", { name: OPEN_DESMOS_LABEL }));

      expect(open).toHaveBeenCalledWith(DESMOS_URL, "_blank", "noopener,noreferrer");
      expect(screen.queryByTitle(DESMOS_TITLE)).toBeNull();
   });
});
