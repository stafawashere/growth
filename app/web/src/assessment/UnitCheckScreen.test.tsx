import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";

import * as client from "../api/client";
import type { AssessmentSession, CheckResult } from "../api/types";
import { multipleChoiceQuestion, sessionWith } from "./fixtures";
import { UnitCheckScreen } from "./UnitCheckScreen";

vi.mock("../api/client", async (importOriginal) => {
   const actual = await importOriginal<typeof client>();

   return { ...actual, readCheck: vi.fn(), saveCheckQuestion: vi.fn(), submitCheck: vi.fn() };
});

const mocked = vi.mocked(client);

function unitCheckSession(): AssessmentSession {
   const questions = [multipleChoiceQuestion(1), multipleChoiceQuestion(2)];

   return {
      ...sessionWith([]),
      id: "SES-UNIT",
      mode: "unit_check",
      sub_mode: "BC-UNIT-01",
      parts: [
         {
            key: "unit",
            section: "",
            part: "",
            label: "Unit check",
            question_type: "",
            multiple_choice: true,
            question_count: questions.length,
            minutes: null,
            calculator: false,
            calculator_label: null,
            calculator_note: null,
            first_number: 1,
            budget_seconds_per_question: null,
            tools: [],
            five_minute_alert_seconds: 0,
            position: 1,
            status: "open",
            timed: false,
            started_at: "2026-09-24T21:50:07+00:00",
            deadline_at: null,
            closed_at: null,
            closed_by: null,
            time_remaining_ms: null,
            answered: 0,
            questions
         }
      ]
   };
}

/* Trimmed from a POST /unit-checks/{id}/submit reply captured from the running route. */
const submitted: CheckResult = {
   id: "SES-UNIT",
   unit_id: "BC-UNIT-01",
   items: [
      {
         number: 1,
         item_id: "ITM-1",
         archetype_id: "BC-QA-01013",
         answered: true,
         correct: false,
         answer: { option_id: "A" },
         key_option_id: "C",
         worked_solution: [{ step: 1, text: "The input increases without bound.", rule_named: "read the input behaviour" }]
      },
      {
         number: 2,
         item_id: "ITM-2",
         archetype_id: "BC-QA-01001",
         answered: true,
         correct: true,
         answer: { option_id: "B" },
         key_option_id: "B",
         worked_solution: []
      }
   ],
   moved: [
      {
         skill_id: "BC-SKL-01009",
         name: "Estimate a two sided limit from a graph",
         before: { mastered: false, credited_successes: 0, credited_failures: 0 },
         after: { mastered: false, credited_successes: 0, credited_failures: 1 }
      }
   ],
   coverage: {
      covered: ["BC-SKL-01001", "BC-SKL-01009"],
      unreached: { "BC-SKL-01021": "prerequisites not yet mastered" }
   }
};

beforeEach(() => {
   vi.clearAllMocks();
   mocked.saveCheckQuestion.mockResolvedValue({ number: 1, saved: true });
   mocked.submitCheck.mockResolvedValue(submitted);
});

afterEach(() => {
   cleanup();
});

const CORRECTNESS_WORDS = /\b(correct|incorrect|right|wrong|the key)\b/i;

/* Each text node on its own, so words from neighbouring elements never run together. */
function renderedTexts() {
   const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
   const texts: string[] = [];
   let node = walker.nextNode();

   while (node !== null) {
      texts.push(node.textContent ?? "");
      node = walker.nextNode();
   }

   return texts;
}

describe("the unit check", () => {
   it("shows no correctness while answering and the breakdown only after Submit check", async () => {
      render(<UnitCheckScreen sessionId="SES-UNIT" initial={unitCheckSession()} />);

      fireEvent.click(screen.getByRole("radio", { name: /First choice/ }));
      fireEvent.click(screen.getByRole("radio", { name: "confident" }));
      fireEvent.click(screen.getByRole("button", { name: "Next" }));
      fireEvent.click(screen.getByRole("radio", { name: /Second choice/ }));

      const withoutTheUntimedNote = renderedTexts().filter(
         (text) => text !== "Untimed. Nothing is marked right or wrong until you submit the whole check."
      );
      const correctnessBeforeSubmit = withoutTheUntimedNote.filter((text) => CORRECTNESS_WORDS.test(text));

      expect(screen.getByTestId("question-position").textContent).toBe("Question 2 of 2");
      expect(correctnessBeforeSubmit).toEqual([]);
      expect(screen.queryByTestId("unit-check-breakdown")).toBeNull();

      await waitFor(() => expect(mocked.saveCheckQuestion).toHaveBeenCalledTimes(3));

      expect(mocked.saveCheckQuestion).toHaveBeenCalledWith("SES-UNIT", 1, { answer: { option_id: "A" } });
      expect(mocked.saveCheckQuestion).toHaveBeenCalledWith("SES-UNIT", 1, { confidence: "confident" });
      expect(mocked.submitCheck).not.toHaveBeenCalled();

      fireEvent.click(screen.getByRole("button", { name: "Submit check" }));

      const breakdown = await screen.findByTestId("unit-check-breakdown");
      const items = screen.getAllByTestId("check-item").map((item) => item.textContent);

      expect(breakdown).toBeTruthy();
      expect(renderedTexts().filter((text) => CORRECTNESS_WORDS.test(text)).length).toBeGreaterThan(0);
      expect(items[0]).toContain("Question 1: Not correct Your answer: option A. The key is option C.");
      expect(items[1]).toContain("Question 2: Correct");
      expect(screen.getByTestId("moved-skills").textContent).toContain(
         "Estimate a two sided limit from a graphBefore: not mastered, 0 credited successes, 0 credited failures. After: not mastered, 0 credited successes, 1 credited failures."
      );
      expect(screen.getByTestId("coverage").textContent).toBe("The check reached 2 of the unit's 3 skills.");
      expect(screen.getByTestId("unreached-skills").textContent).toBe("BC-SKL-01021: prerequisites not yet mastered");
   });
});
