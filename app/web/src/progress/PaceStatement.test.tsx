import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";

import type { PacePayload } from "../api/types";
import { PaceStatement } from "./PaceStatement";

afterEach(() => {
   cleanup();
});

const untimed: PacePayload = {
   as_of: "2026-09-29",
   verdict: "too_early",
   statement: "Too early to call.",
   exam_date: "2027-05-10",
   days_to_exam: 223,
   review_reserve_days: 28,
   new_mastery_deadline: "2027-04-12",
   skills: { total: 541, held: 0, fading: 0, assumed: 0, remaining: 541, remaining_weighted: 541 },
   rate: {
      window_start: "2026-09-28",
      window_days: 2,
      earned_weighted: 0,
      weekly: 0,
      required_weekly: 19.42,
      pace_ratio: 0,
      projected_finish: null
   },
   study_time: {
      window_start: "2026-09-28",
      window_days: 2,
      active_days: 2,
      timed_attempts: 0,
      attempts: 8,
      minutes: null,
      minutes_per_active_day: null,
      active_days_per_week: 2,
      minutes_per_week: null
   },
   evidence: {
      graded_attempts: 7,
      practice_days: 2,
      recent_accuracy: { correct: 5, graded: 7, days: 14, value: 0.714 },
      retention_30_day: { correct: 0, attempts: 0, value: null, floor: 0.75 }
   },
   caveat: "A pace on mastering the exam's skills, not a predicted AP score."
};

describe("pace statement on progress", () => {
   it("says study time was not logged instead of drawing zero minutes", () => {
      render(<PaceStatement pace={untimed} />);

      const section = screen.getByTestId("pace-statement");

      expect(section.textContent).toContain("not logged on any of the last 8 attempts");
      expect(section.textContent).not.toContain("0 minutes");
   });
});
