import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";

import * as client from "../api/client";
import type {
   CheckpointsPayload,
   CheckpointView,
   ProbePayload,
   RepresentationMatrixPayload
} from "../api/types";
import { SELF_SCORED_NOTE } from "./CheckpointHistory";
import { ProgressRoute } from "./ProgressRoute";

vi.mock("../api/client");

const mocked = vi.mocked(client);

const matrix: RepresentationMatrixPayload = {
   representations: [
      { id: "BC-REP-01", name: "Analytical" },
      { id: "BC-REP-02", name: "Graphical" },
      { id: "BC-REP-03", name: "Tabular" }
   ],
   cells: [
      { source: "BC-REP-02", target: "BC-REP-01", attempts: 5, correct: 3 },
      { source: "BC-REP-01", target: "BC-REP-02", attempts: 2, correct: 2 },
      { source: "BC-REP-03", target: "BC-REP-02", attempts: 0, correct: 0 }
   ],
   translation_attempts: 7,
   practice_attempts: 40
};

const finished: CheckpointView = {
   id: "CKP-1",
   form_year: 2024,
   started_at: "2026-08-01T12:00:00+00:00",
   finished_at: "2026-08-01T12:00:00+00:00",
   scored_by: "student_self_score",
   free_response_url: "https://apcentral.collegeboard.org/media/pdf/ap24-frq-calculus-bc.pdf",
   scoring_guidelines_url: "https://apcentral.collegeboard.org/media/pdf/ap24-sg-calculus-bc.pdf",
   sections: [],
   scores: {},
   questions: [
      { question: 1, earned: 5, possible: 9, published_mean: 3.1234, published_mean_years: [2024] },
      { question: 2, earned: 2, possible: 9, published_mean: null, published_mean_years: [] }
   ],
   total_earned: 7,
   total_possible: 18,
   published_total: 3.1234
};

const checkpointsAvailable: CheckpointsPayload = {
   availability: {
      open_checkpoint_id: null,
      available: true,
      opens_on: null,
      forms_remaining: 3,
      cadence_days: 42
   },
   history: [finished],
   expected_effect: { low: 0.4, high: 0.7 }
};

const checkpointsWaiting: CheckpointsPayload = {
   ...checkpointsAvailable,
   availability: { ...checkpointsAvailable.availability, available: false, opens_on: "2026-09-12" }
};

const probe: ProbePayload = {
   availability: { open_administration_id: null, available: false, opens_on: "2026-10-20", items: 12, cadence_days: 56 },
   history: [
      {
         id: "PRB-1",
         probe_set: "stable-probe-v1",
         started_at: "2026-08-25T12:00:00+00:00",
         finished_at: "2026-08-25T12:00:00+00:00",
         answered: 12,
         graded: 11,
         correct: 8,
         items: 12
      }
   ]
};

function neverAnswers() {
   return new Promise<never>(() => undefined);
}

beforeEach(() => {
   vi.clearAllMocks();
   mocked.readMasteryMap.mockReturnValue(neverAnswers());
   mocked.readCalibration.mockReturnValue(neverAnswers());
   mocked.readRepresentations.mockResolvedValue(matrix);
   mocked.readCheckpoints.mockResolvedValue(checkpointsAvailable);
   mocked.readProbe.mockResolvedValue(probe);
});

afterEach(() => {
   cleanup();
});

function cellAt(sourceName: string, targetName: string) {
   const table = within(screen.getByTestId("representation-matrix")).getByRole("table");
   const targets = Array.from(table.querySelectorAll("thead th")).map((header) => header.textContent);
   const row = within(table).getByRole("rowheader", { name: sourceName }).closest("tr") as HTMLTableRowElement;
   const column = targets.indexOf(targetName);

   return row.children[column].textContent;
}

describe("the representation matrix on progress", () => {
   it("puts correct of attempts in the source row and target column, and blanks a pair that is no translation", async () => {
      render(<ProgressRoute />);

      await screen.findByTestId("representation-matrix");

      expect(cellAt("Graphical", "Analytical")).toBe("3 of 5");
      expect(cellAt("Analytical", "Graphical")).toBe("2 of 2");
      expect(cellAt("Tabular", "Graphical")).toBe("no attempts");
      expect(cellAt("Analytical", "Tabular")).toBe("");
      expect(cellAt("Tabular", "Tabular")).toBe("");
   });

   it("states the translation attempt count against the graded practice attempts", async () => {
      render(<ProgressRoute />);

      const count = await screen.findByTestId("translation-attempts");

      expect(count.textContent!.replace(/\s+/g, " ")).toContain(
         "7 of 40 graded practice attempts asked for a translation"
      );
   });

   it("keeps the checkpoint history drawn when the matrix fails to load", async () => {
      mocked.readRepresentations.mockRejectedValue(new Error("the connection dropped"));
      render(<ProgressRoute />);

      expect(await screen.findByTestId("matrix-failed")).toBeTruthy();
      expect(await screen.findByTestId("checkpoint-history")).toBeTruthy();
      expect(screen.queryByTestId("representation-matrix")).toBeNull();
   });
});

describe("the checkpoint history on progress", () => {
   it("gives each finished checkpoint's form year, total, per-question result against the published mean and who scored it", async () => {
      render(<ProgressRoute />);

      const result = await screen.findByTestId("checkpoint-result");
      const questions = within(result)
         .getAllByTestId("checkpoint-question")
         .map((line) => line.textContent!.replace(/\s+/g, " "));

      expect(within(result).getByRole("heading").textContent).toBe("2024 released free-response form");
      expect(within(result).getByTestId("checkpoint-total").textContent).toBe("7 of 18 points.");
      expect(questions).toEqual([
         "Question 1, 5 of 9 points, against a published mean of 3.12 from 2024.",
         "Question 2, 2 of 9 points, no published mean for this question."
      ]);
      expect(within(result).getByText(SELF_SCORED_NOTE)).toBeTruthy();
   });

   it("omits the self-scoring note for a checkpoint scored some other way", async () => {
      mocked.readCheckpoints.mockResolvedValue({
         ...checkpointsAvailable,
         history: [{ ...finished, scored_by: "per_point_grader" }]
      });
      render(<ProgressRoute />);

      const result = await screen.findByTestId("checkpoint-result");

      expect(within(result).queryByText(SELF_SCORED_NOTE)).toBeNull();
   });

   it("opens the checkpoint screen from the history when one is available", async () => {
      render(<ProgressRoute />);

      fireEvent.click(await screen.findByRole("button", { name: "Take a checkpoint" }));

      expect(await screen.findByTestId("checkpoint-intro")).toBeTruthy();
      expect(mocked.startCheckpoint).not.toHaveBeenCalled();
   });

   it("states the day the next checkpoint opens and offers none before it", async () => {
      mocked.readCheckpoints.mockResolvedValue(checkpointsWaiting);
      render(<ProgressRoute />);

      const opensOn = await screen.findByTestId("checkpoint-opens-on");

      expect(opensOn.textContent).toBe("The next checkpoint opens on 12 September 2026.");
      expect(screen.queryByRole("button", { name: "Take a checkpoint" })).toBeNull();
      expect(screen.queryByRole("button", { name: "Continue the checkpoint" })).toBeNull();
   });

   it("gives each finished concept probe as correct of graded", async () => {
      render(<ProgressRoute />);

      const line = await screen.findByTestId("probe-result");

      expect(line.textContent).toBe("8 of 11 graded items correct.");
      expect(screen.getByTestId("probe-opens-on").textContent).toBe("The next concept probe opens on 20 October 2026.");
   });
});