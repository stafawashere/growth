import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";

import * as client from "../api/client";
import type { MasteryMapPayload } from "../api/types";
import { ProgressRoute } from "./ProgressRoute";

vi.mock("../api/client");

const mocked = vi.mocked(client);

const MAP: MasteryMapPayload = {
   today: "2027-01-05",
   states: ["not_attempted", "in_progress", "mastered", "fading", "gap"],
   units: [
      {
         unit_id: "BC-UNIT-03",
         number: 3,
         name: "Differentiation: Composite, Implicit, and Inverse Functions",
         nodes: [
            {
               skill_id: "BC-SKL-03004",
               name: "Chain rule with three layers",
               state: "in_progress",
               depth: 0,
               assumed: false,
               last_success_on: null,
               days_since_success: null
            }
         ]
      }
   ]
};

const DETAIL: client.SkillDetail = {
   skill_id: "BC-SKL-03004",
   name: "Chain rule with three layers",
   unit_id: "BC-UNIT-03",
   state: "in_progress",
   assumed: false,
   last_success_on: null,
   days_since_success: null,
   description: "Differentiate a composite of three functions.",
   mastered_if: "Each layer's derivative is multiplied in, outermost first.",
   partially_mastered_if: "The innermost derivative goes missing.",
   prerequisites: [
      { id: "BC-SKL-03001", name: "Chain rule with two layers", kind: "hard", state: "mastered" },
      { id: "BC-PRQ-03001", name: "Composing functions", kind: "supporting", state: null }
   ],
   concept_id: "BC-CON-03001",
   lesson_id: "LSN-CON-03001"
};

beforeEach(() => {
   vi.clearAllMocks();
   mocked.readPace.mockReturnValue(new Promise(() => undefined));
   mocked.readMasteryMap.mockResolvedValue(MAP);
   mocked.readSkill.mockResolvedValue(DETAIL);
});

afterEach(() => {
   cleanup();
});

describe("a skill opened from the mastery map", () => {
   it("shows what mastering it means and what it is built on, and opens its lesson", async () => {
      const onOpenLesson = vi.fn();

      render(<ProgressRoute onOpenLesson={onOpenLesson} />);

      fireEvent.click(await screen.findByRole("button", { name: /Chain rule with three layers/ }));
      fireEvent.click(screen.getByRole("button", { name: "Open this skill" }));

      const detail = await screen.findByTestId("skill-detail");

      expect(mocked.readSkill).toHaveBeenCalledWith("BC-SKL-03004");
      expect(detail.textContent).toContain(DETAIL.mastered_if);
      expect(within(detail).getAllByTestId("skill-prerequisite").map((row) => row.textContent)).toEqual([
         "Chain rule with two layersMastered, required first",
         "Composing functionsAlgebra and earlier work, supports it"
      ]);

      fireEvent.click(within(detail).getByRole("button", { name: "Read the lesson" }));

      expect(onOpenLesson).toHaveBeenCalledWith("LSN-CON-03001", "Chain rule with three layers");
   });
});
