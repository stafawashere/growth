import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen, within } from "@testing-library/react";

import type { AssessmentResult, PartPacing } from "../api/types";
import { ResultScreen } from "./ResultScreen";

afterEach(() => {
   cleanup();
});

/* Trimmed from a GET /mocks/{id}/result reply captured from the running route. */
const partAPacing: PartPacing = {
   part_key: "I-A",
   label: "Section I, Part A",
   questions: 29,
   limit_seconds: 3720,
   budget_seconds_per_question: 128.27586206896552,
   time_used_seconds: 1830,
   time_remaining_seconds: 1890,
   closed_by: "submitted",
   mean_seconds_per_question: 61.5,
   mean_counts: { numerator: 27, denominator: 29, value: 0.931 },
   answered: { numerator: 28, denominator: 29, value: 0.966 },
   rapid_guess: { numerator: 2, denominator: 29, value: 0.069 },
   revisit: { numerator: 3, denominator: 28, value: 0.107 },
   marked: { numerator: 4, denominator: 29, value: 0.138 },
   per_question: []
};

const STATEMENT = "Position against published distributions, with assumptions. Cut points are not published, so this is a band, not a score.";

const mockResult: AssessmentResult = {
   id: "SES-MOCK",
   mode: "mock",
   complete: true,
   pacing: [partAPacing],
   multiple_choice: { correct: 14, total: 42 },
   free_response: { earned: 11, pending: 6, total: 54 },
   questions: [
      {
         question: 1,
         earned: 5,
         pending: 1,
         possible: 9,
         published: [
            { year: 2023, mean: 5.26, sd: 2.24 },
            { year: 2024, mean: 6.45, sd: 2.25 },
            { year: 2025, mean: 5.22, sd: 2.49 }
         ]
      }
   ],
   band: { low: 2, high: 4 },
   band_years: [2023, 2024, 2025],
   assumptions: [
      { key: "cut_points_unknown", text: "College Board does not publish cut points." },
      { key: "no_guessing_penalty", text: "Multiple choice is scored as the number answered correctly." },
      { key: "uncertainty_one_score_point", text: "The uncertainty is at least one full score point either side." }
   ],
   statement: STATEMENT
};

const drillResult: AssessmentResult = {
   id: "SES-DRILL",
   mode: "part_drill",
   complete: true,
   pacing: [partAPacing],
   multiple_choice: { correct: 20, total: 29 }
};

/* A lone score is a number from 1 to 5 standing alone or tied to the word score, rather than one
   end of the band. */
const LONE_SCORE = /(score\D{0,12}[1-5]\b)|(^\s*[1-5]\s*$)/i;

describe("the mock result", () => {
   it("shows the band with its assumptions on the same screen and the server's statement as sent", () => {
      render(<ResultScreen result={mockResult} onDone={vi.fn()} />);

      expect(screen.getByTestId("band").textContent).toBe("Band: 2 to 4");
      expect(screen.getByTestId("band-statement").textContent).toBe(STATEMENT);
      expect(within(screen.getByTestId("band-assumptions")).getAllByRole("listitem").map((item) => item.textContent)).toEqual(
         mockResult.assumptions!.map((assumption) => assumption.text)
      );
   });

   it("never shows a predicted score, a centre or a single number standing for the result", () => {
      render(<ResultScreen result={mockResult} onDone={vi.fn()} />);

      const text = document.body.textContent ?? "";
      const leaves = Array.from(document.body.querySelectorAll("*")).filter((element) => element.children.length === 0);
      const loneScores = leaves.map((element) => element.textContent ?? "").filter((leaf) => LONE_SCORE.test(leaf));

      expect(text).toContain("Band: 2 to 4");
      expect(text).not.toMatch(/predict/i);
      expect(text).not.toMatch(/cent(re|er)/i);
      expect(text).not.toMatch(/AP score/i);
      expect(loneScores).toEqual([]);
   });

   it("gives the raw counts, the per-question comparison and pacing with every denominator", () => {
      render(<ResultScreen result={mockResult} onDone={vi.fn()} />);

      const counts = screen.getByTestId("raw-counts").textContent;
      const table = screen.getByTestId("question-comparison");
      const pacing = screen.getByTestId("pacing-part").textContent;

      expect(counts).toContain("Multiple choice: 14 of 42 correct");
      expect(counts).toContain("Free response: 11 points earned, 6 pending, of 54");
      expect(within(table).getAllByRole("columnheader").map((cell) => cell.textContent)).toEqual([
         "Question",
         "Your points",
         "2023 mean",
         "2024 mean",
         "2025 mean"
      ]);
      expect(within(table).getAllByRole("cell").map((cell) => cell.textContent)).toEqual(["5 of 9, 1 pending", "5.26", "6.45", "5.22"]);
      expect(pacing).toContain("Time used: 30:30 of 62:00");
      expect(pacing).toContain("61.5 seconds per question, over 27 of 29 questions, against a budget of 128.28 seconds");
      expect(pacing).toContain("Answered: 28 of 29");
      expect(pacing).toContain("Rapid guesses: 2 of 29");
      expect(pacing).toContain("Revisits after answering: 3 of 28");
      expect(pacing).toContain("Marked for review: 4 of 29");
   });
});

describe("a drill result", () => {
   it("shows pacing and counts and no band", () => {
      render(<ResultScreen result={drillResult} onDone={vi.fn()} />);

      expect(screen.getByTestId("pacing-part")).toBeTruthy();
      expect(screen.getByTestId("raw-counts").textContent).toContain("Multiple choice: 20 of 29 correct");
      expect(screen.queryByTestId("band-section")).toBeNull();
      expect(document.body.textContent).not.toContain("Band:");
   });
});
