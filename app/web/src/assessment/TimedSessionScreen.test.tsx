import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";

import * as client from "../api/client";
import type { AssessmentFrqItem, AssessmentShape, ShapePart } from "../api/types";
import { calculatorPart, freeResponsePart, freeResponseQuestion, noCalculatorPart, sessionWith } from "./fixtures";
import { TimedSessionScreen } from "./TimedSessionScreen";

vi.mock("../api/client", async (importOriginal) => {
   const actual = await importOriginal<typeof client>();

   return {
      ...actual,
      readTimedSession: vi.fn(),
      readAssessmentShape: vi.fn(),
      startPart: vi.fn(),
      submitPart: vi.fn(),
      saveQuestion: vi.fn(),
      finishMock: vi.fn(),
      readTimedResult: vi.fn(),
      startFrqAttempt: vi.fn()
   };
});

const mocked = vi.mocked(client);

function shapePart(key: string, section: string, part: string, questionCount: number): ShapePart {
   return {
      ...noCalculatorPart({ key, section, part, question_count: questionCount }),
      label: `Section ${section}, Part ${part}`
   };
}

/* The four parts' counts as GET /assessments/shape serves them. */
const EXAM_SHAPE: AssessmentShape = {
   form: "2027",
   parts: [shapePart("I-A", "I", "A", 29), shapePart("I-B", "I", "B", 13), shapePart("II-A", "II", "A", 2), shapePart("II-B", "II", "B", 4)],
   multiple_choice_total: 42,
   free_response_total: 6,
   points_per_free_response_question: 9,
   section_weights: { I: 50, II: 50 },
   testing_minutes: 190,
   reference_sheet: { shown: false, note: "No reference sheet is shown." },
   radian_note: "Your calculator should be in radian mode.",
   timed_available: true
};

beforeEach(() => {
   vi.clearAllMocks();
   mocked.saveQuestion.mockResolvedValue({ number: 1, saved: true });
   mocked.readAssessmentShape.mockResolvedValue(EXAM_SHAPE);
});

afterEach(() => {
   cleanup();
});

const closedFirstPart = noCalculatorPart({ status: "closed", closed_by: "submitted", questions: [] });

const waitingSecondPart = calculatorPart({ status: "not_started", time_remaining_ms: null, questions: [] });

describe("a closed part", () => {
   it("offers no way back once submitted, only the break and the next part", async () => {
      const open = sessionWith([noCalculatorPart(), calculatorPart({ status: "not_started", questions: [] })]);
      const afterSubmit = sessionWith([closedFirstPart, waitingSecondPart]);

      mocked.submitPart.mockResolvedValue(afterSubmit);
      render(<TimedSessionScreen kind="mocks" sessionId="SES-MOCK" initial={open} onShowResult={vi.fn()} />);

      expect(screen.getByTestId("part-runner")).toBeTruthy();

      fireEvent.click(screen.getByRole("button", { name: "Submit part" }));
      fireEvent.click(screen.getByRole("button", { name: "Submit and close this part" }));

      await screen.findByTestId("break-screen");

      expect(mocked.submitPart).toHaveBeenCalledWith("mocks", "SES-MOCK", 1);
      expect(screen.getByTestId("break-note").textContent).toBe(
         "Section I, Part A is closed. Take your break here. The next part starts when you choose to start it, and its timer starts then."
      );
      expect(screen.queryByTestId("part-runner")).toBeNull();
      expect(screen.queryByText(/twice differentiable/)).toBeNull();

      const labels = screen.getAllByRole("button").map((button) => button.textContent);

      expect(labels).toEqual(["Start next part"]);
   });

   it("starts the next part and names the closed one above it, with no control that returns to it", async () => {
      mocked.startPart.mockResolvedValue(sessionWith([closedFirstPart, calculatorPart()]));
      render(
         <TimedSessionScreen
            kind="mocks"
            sessionId="SES-MOCK"
            initial={sessionWith([closedFirstPart, waitingSecondPart])}
            onShowResult={vi.fn()}
         />
      );

      fireEvent.click(screen.getByRole("button", { name: "Start next part" }));

      await screen.findByTestId("part-runner");

      expect(mocked.startPart).toHaveBeenCalledWith("mocks", "SES-MOCK", 2);
      expect(screen.getByTestId("closed-part-note").textContent).toBe(
         "Section I, Part A is closed. You cannot return to its questions."
      );

      const partAControls = screen.getAllByRole("button").filter((button) => /Part A/.test(button.textContent ?? ""));

      expect(partAControls).toEqual([]);
      expect(screen.getByTestId("question-stem").textContent).toContain("question 30");
   });

   it("shows the server's refusal and re-reads the session when a start is refused", async () => {
      const refusal = new client.ApiError(409, "this part is closed and cannot be reopened");
      const current = sessionWith([closedFirstPart, waitingSecondPart]);

      mocked.startPart.mockRejectedValue(refusal);
      mocked.readTimedSession.mockResolvedValue(current);
      render(<TimedSessionScreen kind="mocks" sessionId="SES-MOCK" initial={current} onShowResult={vi.fn()} />);

      fireEvent.click(screen.getByRole("button", { name: "Start next part" }));

      expect((await screen.findByRole("alert")).textContent).toBe("this part is closed and cannot be reopened");
      await waitFor(() => expect(mocked.readTimedSession).toHaveBeenCalledWith("mocks", "SES-MOCK"));
   });
});

describe("question numbering in a timed session", () => {
   it("counts a part drill's questions against its whole section, read from the exam shape", async () => {
      const partB = freeResponsePart({
         key: "II-B",
         part: "B",
         label: "Section II, Part B",
         first_number: 3,
         questions: [freeResponseQuestion(3), freeResponseQuestion(4)]
      });

      render(<TimedSessionScreen kind="drills" sessionId="SES-D" initial={sessionWith([partB])} onShowResult={vi.fn()} />);

      await waitFor(() => expect(screen.getByTestId("question-position").textContent).toBe("Question 3 of 6"));
      expect(mocked.readAssessmentShape).toHaveBeenCalledTimes(1);
   });
});

describe("free-response capture after the part closes", () => {
   it("captures each question from the session payload alone, as after a reload, in the session's capture mode", async () => {
      const heldQuestions = freeResponsePart().questions;
      const closedPart = freeResponsePart({
         status: "closed",
         closed_by: "submitted",
         questions: [],
         capture: heldQuestions.map((question) => ({
            number: question.number,
            item_id: question.item.id,
            attempt_id: question.attempt_id,
            grading_state: "capturing",
            item: question.item as AssessmentFrqItem
         }))
      });

      mocked.readTimedSession.mockResolvedValue(sessionWith([closedPart]));
      mocked.startFrqAttempt.mockReturnValue(new Promise(() => undefined));
      render(<TimedSessionScreen kind="mocks" sessionId="SES-MOCK" onShowResult={vi.fn()} />);

      await screen.findByTestId("timed-finished");

      expect(screen.getByRole("button", { name: "See the result" })).toBeTruthy();

      fireEvent.click(screen.getByRole("button", { name: "Capture Question 2" }));

      expect(await screen.findByTestId("capture-screen")).toBeTruthy();
      expect(screen.getByTestId("capture-screen").textContent).toContain("Find the area of S.");
      expect(mocked.startFrqAttempt).toHaveBeenCalledWith("SES-MOCK", "FRQ-2", "typed");
      expect(screen.queryByRole("button", { name: "Type my answer instead" })).toBeNull();
   });

   function closedPartWith(states: string[]) {
      const heldQuestions = freeResponsePart().questions;

      return freeResponsePart({
         status: "closed",
         closed_by: "submitted",
         questions: [],
         capture: heldQuestions.map((question, index) => ({
            number: question.number,
            item_id: question.item.id,
            attempt_id: question.attempt_id,
            grading_state: states[index],
            item: question.item as AssessmentFrqItem
         }))
      });
   }

   function listedStates() {
      return Array.from(screen.getByTestId("capture-list").querySelectorAll("li > span:first-child")).map((entry) => entry.textContent);
   }

   it("re-reads the session when the student comes back to the list", async () => {
      mocked.startFrqAttempt.mockReturnValue(new Promise(() => undefined));
      mocked.readTimedSession.mockResolvedValue(sessionWith([closedPartWith(["capturing", "graded"])]));
      render(
         <TimedSessionScreen kind="mocks" sessionId="SES-MOCK" initial={sessionWith([closedPartWith(["capturing", "capturing"])])} onShowResult={vi.fn()} />
      );

      fireEvent.click(screen.getByRole("button", { name: "Capture Question 2" }));
      fireEvent.click(await screen.findByRole("button", { name: "Back to free-response capture" }));

      await waitFor(() => expect(listedStates()).toEqual(["Question 1, not captured yet", "Question 2, graded"]));
      expect(mocked.readTimedSession).toHaveBeenCalledWith("mocks", "SES-MOCK");
   });

   it("keeps re-reading while a question is confirmed and stops once it is graded", async () => {
      mocked.readTimedSession.mockResolvedValue(sessionWith([closedPartWith(["graded", "graded"])]));
      render(
         <TimedSessionScreen
            kind="drills"
            sessionId="SES-D"
            initial={sessionWith([closedPartWith(["graded", "confirmed"])])}
            listPollMilliseconds={10}
            onShowResult={vi.fn()}
         />
      );

      expect(listedStates()).toEqual(["Question 1, graded", "Question 2, confirmed, being graded"]);

      await waitFor(() => expect(listedStates()).toEqual(["Question 1, graded", "Question 2, graded"]));

      const readsWhenGraded = mocked.readTimedSession.mock.calls.length;

      await new Promise((resolve) => setTimeout(resolve, 60));

      expect(readsWhenGraded).toBeGreaterThan(0);
      expect(mocked.readTimedSession.mock.calls.length).toBe(readsWhenGraded);
   });
});
