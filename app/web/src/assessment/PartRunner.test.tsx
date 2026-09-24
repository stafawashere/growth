import { afterEach, describe, expect, it, vi } from "vitest";
import { act, cleanup, fireEvent, render, screen, within } from "@testing-library/react";

import type { AssessmentTool } from "../api/types";
import { calculatorPart, freeResponsePart, noCalculatorPart } from "./fixtures";
import { FIVE_MINUTE_ANNOUNCEMENT } from "./format";
import { PartRunner } from "./PartRunner";

afterEach(() => {
   cleanup();
   vi.useRealTimers();
});

function renderRunner(part = noCalculatorPart(), handlers: Partial<Parameters<typeof PartRunner>[0]> = {}) {
   const props = {
      part,
      radianNote: "Your calculator should be in radian mode.",
      sectionCount: 42 as number | null,
      onSave: vi.fn(),
      onSubmit: vi.fn(),
      onTimeUp: vi.fn(),
      ...handlers
   };

   render(<PartRunner {...props} />);

   return props;
}

const TOOL_PROBES: Record<AssessmentTool, () => HTMLElement | null> = {
   timer: () => screen.queryByRole("button", { name: /Hide timer|Show timer/ }),
   highlight_and_notes: () => screen.queryByTestId("highlight-and-notes"),
   mark_for_review: () => screen.queryByRole("checkbox", { name: /Mark for review/ }),
   option_eliminator: () => screen.queryByRole("button", { name: "Cross out option A" }),
   question_menu: () => screen.queryByRole("button", { name: "Question menu" }),
   zoom: () => screen.queryByTestId("zoom"),
   graphing_panel: () => screen.queryByTestId("graphing-panel")
};

const EVERY_TOOL = Object.keys(TOOL_PROBES) as AssessmentTool[];

describe("the calculator lockout", () => {
   it("leaves the graphing panel out of the DOM on a no-calculator part and puts it in on a calculator part", () => {
      renderRunner(noCalculatorPart());

      expect(screen.getByTestId("calculator-label").textContent).toBe("NO CALCULATOR ALLOWED");
      expect(screen.getByTestId("calculator-note").textContent).toContain("It is not there.");
      expect(screen.queryByTestId("graphing-panel")).toBeNull();
      expect(screen.queryByRole("button", { name: /graphing panel/ })).toBeNull();
      expect(screen.queryByTestId("angle-mode")).toBeNull();

      cleanup();
      renderRunner(calculatorPart());

      expect(screen.getByTestId("calculator-label").textContent).toBe("CALCULATOR REQUIRED");
      expect(screen.queryByTestId("calculator-note")).toBeNull();
      expect(screen.getByTestId("graphing-panel")).toBeTruthy();
      expect(screen.getByTestId("angle-mode").textContent).toBe("Angle mode: Radians");
   });
});

describe("the tool set", () => {
   it.each(EVERY_TOOL)("draws %s exactly when the part's tools list names it", (tool) => {
      const withTool = calculatorPart({ tools: EVERY_TOOL });
      const withoutTool = calculatorPart({ tools: EVERY_TOOL.filter((entry) => entry !== tool) });

      renderRunner(withTool);

      expect(TOOL_PROBES[tool](), `${tool} is missing when named`).not.toBeNull();

      cleanup();
      renderRunner(withoutTool);

      expect(TOOL_PROBES[tool](), `${tool} is drawn when not named`).toBeNull();
   });

   it("offers the option eliminator only on multiple choice", () => {
      renderRunner(noCalculatorPart());

      expect(screen.getAllByRole("button", { name: /Cross out option/ })).toHaveLength(4);

      cleanup();
      renderRunner(freeResponsePart({ tools: EVERY_TOOL }));

      expect(screen.getByTestId("booklet-direction").textContent).toBe("Write your answer in the booklet, Question 1.");
      expect(screen.queryByRole("button", { name: /Cross out option/ })).toBeNull();
   });

   it("crosses an option out without choosing it and saves it as eliminated", () => {
      const props = renderRunner();

      fireEvent.click(screen.getByRole("button", { name: "Cross out option B" }));

      const optionB = screen.getAllByTestId("choice-option")[1];

      expect(optionB.getAttribute("data-eliminated")).toBe("true");
      expect(within(optionB).getByRole("radio")).toHaveProperty("checked", false);
      expect(props.onSave).toHaveBeenCalledWith(1, { eliminated: ["B"] });
   });
});

describe("the timer", () => {
   it("hides and shows on request", () => {
      renderRunner();

      expect(screen.getByTestId("part-timer").textContent).toBe("62:00");

      fireEvent.click(screen.getByRole("button", { name: "Hide timer" }));

      expect(screen.queryByTestId("part-timer")).toBeNull();

      fireEvent.click(screen.getByRole("button", { name: "Show timer" }));

      expect(screen.getByTestId("part-timer")).toBeTruthy();
   });

   it("shows itself at five minutes left and announces it once", () => {
      vi.useFakeTimers();
      renderRunner(noCalculatorPart({ time_remaining_ms: 302_000 }));

      fireEvent.click(screen.getByRole("button", { name: "Hide timer" }));

      const announcements = screen.getByTestId("timer-announcements");

      expect(announcements.closest("[aria-live]")?.getAttribute("aria-live")).toBe("polite");
      expect(announcements.textContent).toBe("");
      expect(screen.queryByTestId("part-timer")).toBeNull();

      act(() => {
         vi.advanceTimersByTime(3000);
      });

      expect(screen.getByTestId("part-timer").textContent).toBe("4:59");
      expect(announcements.querySelectorAll("p")).toHaveLength(1);
      expect(announcements.textContent).toBe(FIVE_MINUTE_ANNOUNCEMENT);

      fireEvent.click(screen.getByRole("button", { name: "Hide timer" }));

      act(() => {
         vi.advanceTimersByTime(60_000);
      });

      expect(screen.queryByTestId("part-timer")).toBeNull();
      expect(announcements.querySelectorAll("p")).toHaveLength(1);
   });

   it("reports the time running out once, after saving the visit", () => {
      vi.useFakeTimers();
      const props = renderRunner(noCalculatorPart({ time_remaining_ms: 2000 }));

      act(() => {
         vi.advanceTimersByTime(5000);
      });

      expect(props.onTimeUp).toHaveBeenCalledTimes(1);
      expect(props.onSave).toHaveBeenCalledWith(1, { visit_ms: expect.any(Number) });
   });
});

describe("the question menu", () => {
   it("lists answered, unanswered and marked questions and jumps to the one chosen", () => {
      const props = renderRunner();

      fireEvent.click(screen.getByRole("radio", { name: /First choice/ }));
      fireEvent.click(screen.getByRole("button", { name: "Next" }));
      fireEvent.click(screen.getByRole("checkbox", { name: /Mark for review/ }));
      fireEvent.click(screen.getByRole("button", { name: "Question menu" }));

      const entries = screen.getAllByTestId("question-menu-entry").map((entry) => entry.textContent);

      expect(entries).toEqual([
         "Question 1, answered",
         "Question 2, unanswered, marked for review",
         "Question 3, unanswered"
      ]);

      fireEvent.click(screen.getAllByTestId("question-menu-entry")[2]);

      expect(screen.getByTestId("question-position").textContent).toBe("Question 3 of 42");
      expect(screen.getByTestId("question-stem").textContent).toContain("question 3");
      expect(props.onSave).toHaveBeenCalledWith(1, { answer: { option_id: "A" } });
      expect(props.onSave).toHaveBeenCalledWith(2, { marked: true });
      expect(props.onSave).toHaveBeenCalledWith(2, { visit_ms: expect.any(Number) });
   });
});

describe("question numbering", () => {
   it("shows each question's exam number against the section's total, as the menu does", () => {
      renderRunner(calculatorPart(), { sectionCount: 42 });

      expect(screen.getByTestId("question-position").textContent).toBe("Question 30 of 42");

      fireEvent.click(screen.getByRole("button", { name: "Next" }));

      expect(screen.getByTestId("question-position").textContent).toBe("Question 31 of 42");

      fireEvent.click(screen.getByRole("button", { name: "Question menu" }));

      expect(screen.getAllByTestId("question-menu-entry").map((entry) => entry.textContent)).toEqual([
         "Question 30, unanswered",
         "Question 31, unanswered"
      ]);
   });
});

describe("the part boundary", () => {
   it("confirms that a submitted part cannot be reopened before submitting", () => {
      const props = renderRunner();

      fireEvent.click(screen.getByRole("button", { name: "Submit part" }));

      expect(screen.getByTestId("submit-confirmation").textContent).toContain("It cannot be reopened");
      expect(props.onSubmit).not.toHaveBeenCalled();

      fireEvent.click(screen.getByRole("button", { name: "Submit and close this part" }));

      expect(props.onSubmit).toHaveBeenCalledTimes(1);
      expect(props.onSave).toHaveBeenCalledWith(1, { visit_ms: expect.any(Number) });
   });

   it("shows the radian note above a question that carries it", () => {
      renderRunner(freeResponsePart());

      expect(screen.getByTestId("radian-note").textContent).toBe("Your calculator should be in radian mode.");
      expect(screen.getByRole("link", { name: "Print booklet page" }).getAttribute("href")).toBe("/attempts/ATT-1/booklet.png");
   });
});

describe("highlights and zoom", () => {
   it("saves a highlight as offsets in the stem's plain text", () => {
      const props = renderRunner();
      const stem = screen.getByTestId("question-stem");
      const text = stem.textContent ?? "";
      const start = text.indexOf("twice");
      const textNode = document.createTreeWalker(stem, NodeFilter.SHOW_TEXT).nextNode()!;
      const range = document.createRange();

      range.setStart(textNode, start);
      range.setEnd(textNode, start + "twice".length);
      window.getSelection()!.removeAllRanges();
      window.getSelection()!.addRange(range);

      fireEvent.click(screen.getByRole("button", { name: "Highlight selection" }));

      expect(props.onSave).toHaveBeenCalledWith(1, { highlights: [{ start, end: start + 5 }] });
      expect(within(screen.getByRole("list", { name: "Highlights" })).getByText("twice")).toBeTruthy();
   });

   it("steps the question area through 100, 125 and 150 percent", () => {
      renderRunner();

      const area = screen.getByTestId("question-area");

      expect(area.style.fontSize).toBe("100%");

      fireEvent.click(screen.getByRole("button", { name: "150 percent" }));

      expect(area.style.fontSize).toBe("150%");
   });
});
