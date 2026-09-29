import { act, cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest";

import type { LessonCheck as LessonCheckRecord, LessonCheckVerdict } from "../api/types";
import { activate, defineKeyboardMathField, pointerEvents, press, startRecordingPointer, stopRecordingPointer, tabTo } from "../testing/keyboard";
import { ERROR_ID, LESSON } from "./fixtures";
import { LessonCheck } from "./LessonCheck";

/* A check's verdict (15 UI; the v2 reader): a wrong answer that matched an error block reads
   "Not yet." and three lines, the observed behaviour, the right step and the consequence on the
   exam, then the link to that error's part and one "Try again". A second wrong answer shows the
   worked solution and offers no further retry. */

const MCQ = LESSON.checks.find((check) => check.format === "mcq")!;

const SHORT = LESSON.checks.find((check) => check.format === "short_answer")!;

const MATCHED: LessonCheckVerdict = {
   correct: false,
   error_id: "BC-ERR-02020",
   anchor: "#err-BC-ERR-02020",
   explanation_anchor: null,
   right_step: "The rule adds two terms, as served.",
   scoring_consequence: "Both points are lost, as served."
};

const UNMATCHED: LessonCheckVerdict = { correct: false, error_id: null, anchor: null, explanation_anchor: null };

async function settle() {
   await act(async () => {
      await Promise.resolve();
   });
}

function renderCheck(check: LessonCheckRecord, onCheckAnswer: ReturnType<typeof vi.fn>, sections = LESSON.sections) {
   const withSolution = { ...check, worked_solution: [{ step: 1, text: "The rule gives two terms." }] };

   render(<LessonCheck check={withSolution} sections={sections} onCheckAnswer={onCheckAnswer} onOpenAnchor={vi.fn()} />);
}

function chooseSecondOption() {
   tabTo(document.querySelector("input[type='radio']") as HTMLElement);
   press("ArrowDown");
}

async function submit() {
   activate(screen.getByTestId("lesson-check-submit"));
   await settle();
}

function sectionsWithRightStep(text: string, expression: unknown) {
   return LESSON.sections.map((section) => (section.id === ERROR_ID ? { ...section, right_step: { text, expression } } : section));
}

function follows(first: HTMLElement, second: HTMLElement) {
   return (first.compareDocumentPosition(second) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0;
}

beforeAll(() => {
   defineKeyboardMathField();
});

beforeEach(() => {
   startRecordingPointer();
});

afterEach(() => {
   stopRecordingPointer();
   cleanup();
});

describe("LessonCheck verdict", () => {
   it("a matched wrong answer reads Not yet. and three lines in order, then the link, then one Try again", async () => {
      renderCheck(MCQ, vi.fn().mockResolvedValue(MATCHED));
      chooseSecondOption();
      await submit();

      const verdict = screen.getByTestId("lesson-check-verdict");
      const observed = screen.getByText("The response multiplies the derivatives of the two factors together.");
      const rightStep = screen.getByTestId("lesson-verdict-right-step");
      const consequence = screen.getByTestId("lesson-verdict-consequence");
      const link = screen.getByTestId("lesson-link");
      const retry = screen.getByTestId("lesson-check-retry");

      expect(verdict.textContent).toMatch(/^x Not yet\./);
      expect(rightStep.textContent).toBe("The right step: The rule adds two terms, as served.");
      expect(consequence.textContent).toBe("On the exam: Both points are lost, as served.");
      expect(link.textContent).toBe("Go to the part on that error");
      expect(retry.textContent).toBe("Try again");
      expect([follows(observed, rightStep), follows(rightStep, consequence), follows(consequence, link), follows(link, retry)]).toEqual([true, true, true, true]);
      expect(screen.queryByTestId("lesson-check-solution")).toBeNull();
      expect(pointerEvents).toEqual([]);
   });

   it("without the served lines, the right step and consequence come from the matched error block", async () => {
      renderCheck(MCQ, vi.fn().mockResolvedValue({ ...MATCHED, right_step: undefined, scoring_consequence: null }));
      chooseSecondOption();
      await submit();

      const errorBlock = LESSON.sections.find((section) => section.id === ERROR_ID)!;

      expect(screen.getByTestId("lesson-verdict-right-step").textContent).toContain(`The right step: `);
      expect(screen.getByTestId("lesson-verdict-right-step").textContent).toContain("The rule adds two terms");
      expect(screen.getByTestId("lesson-verdict-consequence").textContent).toBe(`On the exam: ${errorBlock.scoring_consequence}`);
   });

   it("a right step whose text already ends with its value shows the value once", async () => {
      renderCheck(MCQ, vi.fn().mockResolvedValue({ ...MATCHED, right_step: undefined }), sectionsWithRightStep("Divided by 0.1: 5.2.", 5.2));
      chooseSecondOption();
      await submit();

      const rightStep = screen.getByTestId("lesson-verdict-right-step");

      expect(rightStep.querySelectorAll(".katex")).toHaveLength(0);
      expect(rightStep.textContent).toBe("The right step: Divided by 0.1: 5.2.");
   });

   it("a right step whose text does not carry its value shows the value after the text", async () => {
      renderCheck(MCQ, vi.fn().mockResolvedValue({ ...MATCHED, right_step: undefined }), sectionsWithRightStep("Divide by the change in the input.", 5.2));
      chooseSecondOption();
      await submit();

      const rightStep = screen.getByTestId("lesson-verdict-right-step");
      const renderedValues = rightStep.querySelectorAll(".katex");

      expect(renderedValues).toHaveLength(1);
      expect(renderedValues[0].querySelector("annotation")?.textContent).toBe("5.2");
      expect(rightStep.textContent).toMatch(/^The right step: Divide by the change in the input\. /);
   });

   it("Try again clears a choice for one retry, and a second wrong answer shows the worked solution with no retry", async () => {
      const onCheckAnswer = vi.fn().mockResolvedValue(MATCHED);

      renderCheck(MCQ, onCheckAnswer);
      chooseSecondOption();
      await submit();

      expect((screen.getByTestId("lesson-check-submit") as HTMLButtonElement).disabled).toBe(true);

      activate(screen.getByTestId("lesson-check-retry"));

      expect(screen.queryByTestId("lesson-check-verdict")).toBeNull();
      expect(Array.from(document.querySelectorAll("input[type='radio']")).some((radio) => (radio as HTMLInputElement).checked)).toBe(false);
      expect((screen.getByTestId("lesson-check-submit") as HTMLButtonElement).disabled).toBe(true);

      chooseSecondOption();
      await submit();

      expect(onCheckAnswer).toHaveBeenCalledTimes(2);
      expect(screen.getByTestId("lesson-check-solution").textContent).toContain("The rule gives two terms.");
      expect(screen.queryByTestId("lesson-check-retry")).toBeNull();
      expect((screen.getByTestId("lesson-check-submit") as HTMLButtonElement).disabled).toBe(true);
   });

   it("Try again empties a short answer field, and the retry posts the new answer", async () => {
      const onCheckAnswer = vi.fn().mockResolvedValue(MATCHED);

      renderCheck(SHORT, onCheckAnswer);
      tabTo(document.querySelector("math-field") as HTMLElement);
      press("4");
      await submit();
      activate(screen.getByTestId("lesson-check-retry"));

      const field = document.querySelector("math-field") as HTMLElement & { getValue(format: string): string };

      expect(field.getValue("latex")).toBe("");

      tabTo(field);
      press("6");
      await submit();

      expect(onCheckAnswer.mock.calls.map((call) => call[1].answer)).toEqual([4, 6]);
      expect(screen.queryByTestId("lesson-check-retry")).toBeNull();
   });

   it("a wrong answer with no error block reads Not yet. and shows the worked solution at once, with no retry", async () => {
      renderCheck(MCQ, vi.fn().mockResolvedValue(UNMATCHED));
      chooseSecondOption();
      await submit();

      expect(screen.getByTestId("lesson-check-verdict").textContent).toMatch(/^x Not yet\./);
      expect(screen.getByTestId("lesson-check-solution")).toBeTruthy();
      expect(screen.queryByTestId("lesson-check-retry")).toBeNull();
      expect(screen.queryByTestId("lesson-verdict-right-step")).toBeNull();
   });

   it("a right answer reads Correct with its glyph and nothing more", async () => {
      renderCheck(MCQ, vi.fn().mockResolvedValue({ ...UNMATCHED, correct: true }));
      chooseSecondOption();
      await submit();

      expect(screen.getByTestId("lesson-check-verdict").textContent).toBe("ok Correct");
      expect(screen.queryByTestId("lesson-check-retry")).toBeNull();
   });
});
