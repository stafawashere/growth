import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";

import * as client from "../api/client";
import type { UnfinishedAssessment } from "../api/types";
import { AssessmentRoute } from "./AssessmentRoute";
import { calculatorPart, multipleChoiceQuestion, noCalculatorPart, sessionWith } from "./fixtures";

vi.mock("../api/client", async (importOriginal) => {
   const actual = await importOriginal<typeof client>();

   return {
      ...actual,
      readAssessmentShape: vi.fn(),
      readCheckUnits: vi.fn(),
      readUnfinished: vi.fn(),
      readTimedSession: vi.fn(),
      readCheck: vi.fn()
   };
});

const mocked = vi.mocked(client);

const closedMock: UnfinishedAssessment = {
   id: "SES-M",
   mode: "mock",
   sub_mode: "full_mock",
   started_at: "2026-09-24T21:50:04+00:00",
   parts_closed: 2,
   parts_total: 2
};

const openDrill: UnfinishedAssessment = {
   id: "SES-D",
   mode: "part_drill",
   sub_mode: "I-B",
   started_at: "2026-09-23T10:00:00+00:00",
   parts_closed: 0,
   parts_total: 1
};

const openUnitCheck: UnfinishedAssessment = {
   id: "SES-U",
   mode: "unit_check",
   sub_mode: "BC-UNIT-01",
   started_at: "2026-09-22T10:00:00+00:00",
   parts_closed: 0,
   parts_total: 1
};

beforeEach(() => {
   vi.clearAllMocks();
   mocked.readAssessmentShape.mockRejectedValue(new Error("not needed here"));
   mocked.readCheckUnits.mockResolvedValue({
      units: [
         { unit_id: "BC-UNIT-01", items: 12, covered_skills: 55, unit_skills: 68, available: true, title: "Limits and Continuity" }
      ]
   });
   mocked.readUnfinished.mockResolvedValue({ unfinished: [closedMock, openDrill, openUnitCheck] });
});

afterEach(() => {
   cleanup();
});

describe("resuming an unfinished assessment from setup", () => {
   it("lists every unfinished session with how many parts are closed", async () => {
      render(<AssessmentRoute />);

      const list = await screen.findByTestId("resume-list");

      expect(Array.from(list.querySelectorAll("li")).map((entry) => entry.textContent)).toEqual([
         "Resume Full mock examStarted 24 September 2026, 2 of 2 parts closed",
         "Resume Part drill, I-BStarted 23 September 2026, 0 of 1 parts closed",
         "Resume Unit check, Limits and ContinuityStarted 22 September 2026, 0 of 1 parts closed"
      ]);
   });

   it("lands a mock whose parts are all closed on its capture and finish step", async () => {
      const closedParts = [
         noCalculatorPart({ status: "closed", closed_by: "submitted", questions: [] }),
         calculatorPart({ status: "closed", closed_by: "time", questions: [] })
      ];

      mocked.readTimedSession.mockResolvedValue(sessionWith(closedParts));
      render(<AssessmentRoute />);

      fireEvent.click(await screen.findByRole("button", { name: "Resume Full mock exam" }));

      expect(await screen.findByTestId("timed-finished")).toBeTruthy();
      expect(mocked.readTimedSession).toHaveBeenCalledWith("mocks", "SES-M");
      expect(screen.getByRole("button", { name: "See the result" })).toBeTruthy();
   });

   it("reopens a drill through the drill route and its open part in the runner", async () => {
      mocked.readTimedSession.mockResolvedValue({ ...sessionWith([calculatorPart({ position: 1 })]), id: "SES-D", mode: "part_drill" });
      render(<AssessmentRoute />);

      fireEvent.click(await screen.findByRole("button", { name: "Resume Part drill, I-B" }));

      expect(await screen.findByTestId("part-runner")).toBeTruthy();
      expect(mocked.readTimedSession).toHaveBeenCalledWith("drills", "SES-D");
   });

   it("reopens a unit check through the unit-check route", async () => {
      const unitSession = sessionWith([
         noCalculatorPart({ key: "unit", tools: [], timed: false, time_remaining_ms: null, questions: [multipleChoiceQuestion(1)] })
      ]);

      mocked.readCheck.mockResolvedValue({ ...unitSession, id: "SES-U", mode: "unit_check" });
      render(<AssessmentRoute />);

      fireEvent.click(await screen.findByRole("button", { name: "Resume Unit check, Limits and Continuity" }));

      expect(await screen.findByTestId("unit-check")).toBeTruthy();
      expect(mocked.readCheck).toHaveBeenCalledWith("SES-U");
      expect(mocked.readTimedSession).not.toHaveBeenCalled();
      expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("Unit check, Limits and Continuity");
   });
});
