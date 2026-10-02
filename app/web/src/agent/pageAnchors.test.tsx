import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { FigureView } from "../figures/FigureView";
import { MODE_SECTIONS } from "../lessons/fixtures";
import { LessonSection } from "../lessons/LessonSection";
import { ElaboratedPanel } from "../session/ElaboratedPanel";
import { Item } from "../session/Item";
import { StepMarks } from "../session/StepMarks";
import { FUNCTION_GRAPH, TABLE_FIGURE, servedItem, sessionFeedback } from "../testing/screens";

vi.mock("../api/client");

/* The anchors the tutor's marks name (docs/agent/drawing-build-plan.md, "The marks contract"): each
   anchored element carries data-agent-anchor, and the item's graph carries its window and plot box
   in its own view units. */

afterEach(() => {
   cleanup();
});

function anchored(name: string) {
   return document.querySelector(`[data-agent-anchor="${name}"]`);
}

function itemProps() {
   return {
      onAnswerChange: vi.fn(),
      answerUnavailable: false,
      onAnswerUnavailable: vi.fn(),
      selectedOptionId: null,
      onOptionChange: vi.fn(),
      confidence: null,
      onConfidenceChange: vi.fn(),
      selfExplanation: "",
      onSelfExplanationChange: vi.fn(),
      onCommit: vi.fn(),
      awaitingConfidence: false
   };
}

describe("the anchors of a practice item", () => {
   it("names the stem, and gives the item's graph its window and plot box", () => {
      const wideGraph = { ...FUNCTION_GRAPH, domain: [-2, 6] as [number, number], range: [-1, 3] as [number, number] };

      render(<Item item={servedItem({ figure_spec: wideGraph })} {...itemProps()} />);

      const graph = anchored("item_figure");

      expect(anchored("stem")?.getAttribute("data-testid")).toBe("item-stem");
      expect(graph?.tagName.toLowerCase()).toBe("svg");
      expect(graph?.getAttribute("data-agent-window")).toBe("-2 6 -1 3");
      expect(graph?.getAttribute("data-agent-plot")).toBe("20 20 460 240");
   });

   it("names each option by the letter it shows, on the option and never on its radio", () => {
      const options = ["one", "two", "three", "four"].map((label, index) => ({ id: `id${index}`, label }));

      render(<Item item={servedItem({ format: "mcq", stage: "unsupported", options })} {...itemProps()} />);

      const named = ["option_A", "option_B", "option_C", "option_D"].map(anchored);

      expect(named.map((option) => option?.textContent)).toEqual(["one", "two", "three", "four"]);
      expect(named.every((option) => option?.tagName.toLowerCase() === "label")).toBe(true);
      expect(document.querySelectorAll("input[data-agent-anchor]")).toHaveLength(0);
   });

   it("names the item's table, whose body rows are the rows a mark counts", () => {
      render(<Item item={servedItem({ figure_spec: TABLE_FIGURE })} {...itemProps()} />);

      expect(anchored("item_table")?.tagName.toLowerCase()).toBe("table");
      expect(anchored("item_table")?.querySelectorAll("tbody tr")).toHaveLength(1);
   });

   it("leaves every other figure unanchored, so only the item's own graph is marked", () => {
      const { container } = render(<FigureView spec={FUNCTION_GRAPH} />);

      expect(container.querySelector("[data-agent-anchor], [data-agent-window], [data-agent-plot]")).toBeNull();
   });

   it("names the checked item's graph, its worked solution steps and its feedback panel", async () => {
      await sessionFeedback("completion");

      expect(screen.getByTestId("feedback-figure").querySelector("[data-agent-anchor='item_figure']")).not.toBeNull();
      expect(anchored("solution_step_1")?.getAttribute("data-testid")).toBe("step-mark-1");
      expect(anchored("solution_step_2")?.getAttribute("data-testid")).toBe("step-mark-2");

      cleanup();
      await sessionFeedback("unsupported");

      expect(anchored("feedback")?.getAttribute("data-testid")).toBe("elaborated-panel");
   });

   it("numbers the worked solution's anchors as its steps are numbered", () => {
      render(<StepMarks marks={[{ index: 3, text: "the third", given: true, correct: null }, { index: 4, text: "the fourth", given: false, correct: false }]} />);

      expect(anchored("solution_step_3")?.textContent).toContain("the third");
      expect(anchored("solution_step_4")?.textContent).toContain("the fourth");
   });

   it("names the elaborated feedback panel", () => {
      render(<ElaboratedPanel elaborated={{ violated_step: "The chain rule.", observed_behavior: null, scoring_consequence: null, worked_solution: null, error_id: null }} sentence={null} />);

      expect(anchored("feedback")?.textContent).toContain("The chain rule.");
   });
});

describe("the anchors of a lesson section", () => {
   it("names the section and its figure", () => {
      render(<LessonSection section={MODE_SECTIONS[0]} />);

      expect(anchored("section")?.getAttribute("data-testid")).toBe("lesson-section");
      expect(anchored("section")?.textContent).toContain("The graph and its tangent.");
      expect(anchored("section_figure")).not.toBeNull();
      expect(anchored("section_figure")!.querySelector("svg")).not.toBeNull();
   });
});
