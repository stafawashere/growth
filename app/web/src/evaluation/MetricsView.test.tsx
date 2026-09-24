import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen, within } from "@testing-library/react";

import type { ExperimentComparison, LearningMetric, MetricsPayload } from "../api/types";
import { MetricsView } from "./MetricsView";

const measured: LearningMetric = {
   key: "calibration",
   name: "Calibration",
   status: "measured",
   definition: "Ratings mapped to guess 0.25, unsure 0.60, confident 0.90.",
   window: { start: "2026-08-26", end: "2026-09-24" },
   values: [
      {
         label: "Brier score",
         value: 0.2134,
         numerator: null,
         denominator: 34,
         denominator_label: "rated attempts"
      },
      {
         label: "method-selection accuracy",
         value: 0.8,
         numerator: 8,
         denominator: 10,
         denominator_label: "graded multiple-choice attempts"
      }
   ]
};

const noData: LearningMetric = {
   key: "retention_7_30",
   name: "Retention at 7 and 30 days",
   status: "no_data",
   definition: "First-attempt accuracy on a skill after an interval since its last success.",
   window: null,
   values: [
      {
         label: "first-attempt accuracy 5 to 9 days after a success",
         value: null,
         numerator: 0,
         denominator: 0,
         denominator_label: "first attempts in the interval"
      }
   ]
};

const stated: ExperimentComparison = {
   name: "feedback_elaboration",
   control: { arm: "elaborated", outcomes: 41, correct: 30, accuracy: 30 / 41 },
   treatment: { arm: "verification_only", outcomes: 37, correct: 22, accuracy: 22 / 37 },
   difference: -0.1371,
   interval_low: -0.3398,
   interval_high: 0.0736,
   stated: true,
   minimum_outcomes_per_arm: 30
};

const notStated: ExperimentComparison = {
   name: "retrieval_entry",
   control: { arm: "entry_1", outcomes: 4, correct: 3, accuracy: 0.75 },
   treatment: { arm: "entry_3", outcomes: 0, correct: 0, accuracy: null },
   difference: null,
   interval_low: null,
   interval_high: null,
   stated: false,
   minimum_outcomes_per_arm: 30
};

const payload: MetricsPayload = {
   as_of: "2026-09-24",
   metrics: [measured, noData],
   experiments: [stated, notStated]
};

afterEach(() => {
   cleanup();
});

function valueLines(metricName: string) {
   const heading = screen.getByRole("heading", { name: metricName });
   const section = heading.closest("section") as HTMLElement;

   return within(section)
      .getAllByTestId("metric-value")
      .map((line) => (line.textContent ?? "").replace(/\s+/g, " "));
}

describe("the metrics view", () => {
   it("heads every metric with its name and definition", () => {
      render(<MetricsView metrics={payload} />);

      for (const metric of payload.metrics) {
         expect(screen.getByRole("heading", { name: metric.name })).toBeTruthy();
         expect(screen.getByText(metric.definition)).toBeTruthy();
      }
   });

   it("states the denominator in every measured value's sentence", () => {
      render(<MetricsView metrics={payload} />);

      expect(valueLines("Calibration")).toEqual([
         "Brier score 0.21, over 34 rated attempts.",
         "method-selection accuracy 0.8, 8 over 10 graded multiple-choice attempts."
      ]);
   });

   it("says a zero-denominator value has nothing to count and prints no figure for it", () => {
      render(<MetricsView metrics={payload} />);

      const [line] = valueLines("Retention at 7 and 30 days");
      const withoutLabel = line.replace(noData.values[0].label, "");

      expect(line).toBe("first-attempt accuracy 5 to 9 days after a success, no first attempts in the interval yet (0).");
      expect(withoutLabel.replace("(0)", "")).not.toMatch(/\d/);
   });

   it("gives the interval only when it is stated, and otherwise how many outcomes each arm still needs", () => {
      render(<MetricsView metrics={payload} />);

      const results = screen.getAllByTestId("experiment-result");
      const statedResult = within(results[0]);
      const pendingResult = within(results[1]);

      expect(statedResult.getAllByTestId("experiment-arm").map((line) => line.textContent)).toEqual([
         "elaborated, 30 correct of 41 outcomes.",
         "verification_only, 22 correct of 37 outcomes."
      ]);
      expect(statedResult.getByTestId("experiment-interval").textContent!.replace(/\s+/g, " ")).toContain(
         "-0.14, with a 95 percent interval from -0.34 to 0.07"
      );

      expect(pendingResult.queryByTestId("experiment-interval")).toBeNull();
      expect(pendingResult.getAllByTestId("experiment-arm").map((line) => line.textContent)).toEqual([
         "entry_1, 3 correct of 4 outcomes.",
         "entry_3, no outcomes yet (0)."
      ]);
      expect(pendingResult.getByTestId("experiment-shortfall").textContent!.replace(/\s+/g, " ")).toBe(
         "The interval is stated once each arm holds 30 outcomes. entry_1 needs 26 more and entry_3 needs 30 more."
      );
   });

   it("names where the simulation record is kept", () => {
      render(<MetricsView metrics={payload} />);

      expect(document.body.textContent).toContain("The simulation record is in docs/operator/p7-evals.md.");
   });
});