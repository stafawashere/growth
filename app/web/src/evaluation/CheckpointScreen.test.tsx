import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";

import type { CheckpointView } from "../api/types";
import { CheckpointScreen, MASTERY_NOTE } from "./CheckpointScreen";

const FREE_RESPONSE_URL = "https://apcentral.collegeboard.org/media/pdf/ap24-frq-calculus-bc.pdf";

const SCORING_GUIDELINES_URL = "https://apcentral.collegeboard.org/media/pdf/ap24-sg-calculus-bc.pdf";

const STEM_TEXT = "The function f is defined on the closed interval";

const checkpoint: CheckpointView = {
   id: "CKP-1",
   form_year: 2024,
   started_at: "2026-09-24T12:00:00+00:00",
   finished_at: null,
   scored_by: "student_self_score",
   free_response_url: FREE_RESPONSE_URL,
   scoring_guidelines_url: SCORING_GUIDELINES_URL,
   sections: [
      {
         part: "II-A",
         minutes: 30,
         calculator: "Required",
         questions: [
            {
               question: 1,
               parts: [
                  { record_id: "BC-FRQ-2024-1A", part: "A", points: 2 },
                  { record_id: "BC-FRQ-2024-1B", part: "B", points: 7 }
               ]
            }
         ]
      },
      {
         part: "II-B",
         minutes: 60,
         calculator: "Not permitted",
         questions: [{ question: 3, parts: [{ record_id: "BC-FRQ-2024-3A", part: "A", points: 9 }] }]
      }
   ],
   scores: {},
   questions: [
      { question: 1, earned: 0, possible: 9, published_mean: 4.1, published_mean_years: [2024] },
      { question: 3, earned: 0, possible: 9, published_mean: null, published_mean_years: [] }
   ],
   total_earned: 0,
   total_possible: 18,
   published_total: 4.1
};

/* A view that also carried question text, as a later payload might, must still render none of it. */
const checkpointCarryingStems = {
   ...checkpoint,
   stem: STEM_TEXT,
   sections: checkpoint.sections.map((section) => ({
      ...section,
      questions: section.questions.map((question) => ({ ...question, stem: STEM_TEXT }))
   }))
} as CheckpointView;

afterEach(() => {
   cleanup();
});

function renderScreen(view: CheckpointView = checkpoint) {
   const onScore = vi.fn().mockResolvedValue(true);
   const onFinish = vi.fn().mockResolvedValue(true);

   render(<CheckpointScreen checkpoint={view} onScore={onScore} onFinish={onFinish} onLeave={vi.fn()} />);

   return { onScore, onFinish };
}

function partScore(recordId: string) {
   const row = document.querySelector(`[data-testid="part-score"][data-record-id="${recordId}"]`) as HTMLElement;

   return {
      input: within(row).getByRole("textbox") as HTMLInputElement,
      save: within(row).getByRole("button", { name: "save" }) as HTMLButtonElement
   };
}

describe("the checkpoint screen", () => {
   it("links every question to College Board's documents in a new tab without an opener", () => {
      renderScreen();

      const questionLinks = screen.getAllByTestId("free-response-link");
      const guidelineLinks = screen.getAllByTestId("scoring-guidelines-link");

      expect(questionLinks).toHaveLength(2);
      expect(guidelineLinks).toHaveLength(2);

      for (const link of questionLinks) {
         expect(link.getAttribute("href")).toBe(FREE_RESPONSE_URL);
      }

      for (const link of guidelineLinks) {
         expect(link.getAttribute("href")).toBe(SCORING_GUIDELINES_URL);
      }

      for (const link of [...questionLinks, ...guidelineLinks]) {
         expect(link.getAttribute("target")).toBe("_blank");
         expect(link.getAttribute("rel")).toBe("noopener noreferrer");
      }
   });

   it("renders no question text, even from a payload that carries some", () => {
      renderScreen(checkpointCarryingStems);

      expect(screen.getAllByTestId("checkpoint-question-block")).toHaveLength(2);
      expect(document.body.textContent).not.toContain(STEM_TEXT);
   });

   it("names each part's minutes and calculator rule and says the mastery model is untouched", () => {
      renderScreen();

      const headings = screen.getAllByTestId("checkpoint-section").map((section) => section.querySelector("h2")!.textContent);

      expect(headings).toEqual([
         "Part II-A, 30 minutes, calculator required",
         "Part II-B, 60 minutes, calculator not permitted"
      ]);
      expect(screen.getByText(MASTERY_NOTE)).toBeTruthy();
   });

   it("will not submit more points than a part is worth", () => {
      const { onScore } = renderScreen();
      const { input, save } = partScore("BC-FRQ-2024-1A");

      fireEvent.change(input, { target: { value: "3" } });

      expect(save.disabled).toBe(true);

      fireEvent.click(save);

      expect(onScore).not.toHaveBeenCalled();

      fireEvent.change(input, { target: { value: "2" } });

      expect(save.disabled).toBe(false);

      fireEvent.click(save);

      expect(onScore).toHaveBeenCalledWith("BC-FRQ-2024-1A", 2);
   });

   it("offers the finish only once every part has a saved score", () => {
      renderScreen();

      const finish = screen.getByRole("button", { name: "Finish the checkpoint" }) as HTMLButtonElement;

      expect(finish.disabled).toBe(true);

      cleanup();

      const { onFinish } = renderScreen({
         ...checkpoint,
         scores: { "BC-FRQ-2024-1A": 2, "BC-FRQ-2024-1B": 4, "BC-FRQ-2024-3A": 0 }
      });

      fireEvent.click(screen.getByRole("button", { name: "Finish the checkpoint" }));

      expect(onFinish).toHaveBeenCalledTimes(1);
   });
});