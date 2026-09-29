import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import * as client from "../api/client";
import type { LibraryPayload } from "../api/types";
import { LESSON, planFor } from "../lessons/fixtures";
import { LessonLibrary, STATE_COPY } from "./LessonLibrary";
import { ProgressRoute } from "./ProgressRoute";

vi.mock("../api/client");

const mocked = vi.mocked(client);

const LIBRARY: LibraryPayload = {
   units: [
      {
         id: "BC-UNIT-03",
         name: "Differentiation: Composite, Implicit, and Inverse Functions",
         order: 3,
         concepts: [
            { concept_id: "BC-CON-03001", name: "The chain rule", lesson_id: null, version: null, servable: false, state: "not_available", read_at: null }
         ]
      },
      {
         id: "BC-UNIT-02",
         name: "Differentiation: Definition and Fundamental Properties",
         order: 2,
         concepts: [
            { concept_id: "BC-CON-02013", name: "The product rule", lesson_id: "LSN-CON-02013", version: 1, servable: true, state: "read", read_at: "2026-10-03T09:00:00Z" },
            { concept_id: "BC-CON-02014", name: "The quotient rule", lesson_id: "LSN-CON-02014", version: 1, servable: true, state: "coming_up", read_at: null },
            { concept_id: "BC-CON-02015", name: "Derivatives of trigonometric functions", lesson_id: "LSN-CON-02015", version: 1, servable: true, state: "bypassed_by_placement", read_at: null },
            { concept_id: "BC-CON-02016", name: "Derivatives of exponentials", lesson_id: "LSN-CON-02016", version: 1, servable: true, state: "skipped", read_at: null }
         ]
      }
   ]
};

afterEach(() => {
   cleanup();
   vi.clearAllMocks();
});

describe("the Lessons section of progress", () => {
   it("lists units in order with each concept's name and state copy, and no percent and no count", () => {
      render(<LessonLibrary library={LIBRARY} onOpenLesson={vi.fn()} />);

      const units = screen.getAllByTestId("lesson-library-unit");

      expect(units.map((unit) => within(unit).getByRole("heading").textContent)).toEqual([
         "Differentiation: Definition and Fundamental Properties",
         "Differentiation: Composite, Implicit, and Inverse Functions"
      ]);

      const rows = screen.getAllByTestId("lesson-library-row").map((row) => row.textContent);

      expect(rows).toEqual([
         "The product ruleRead on 3 October 2026",
         "The quotient ruleComing up",
         "Derivatives of trigonometric functionsPlaced, not needed",
         "Derivatives of exponentialsNot read",
         "The chain ruleNot yet available"
      ]);
      expect(screen.getByTestId("lesson-library").textContent).toContain("Reading a lesson does not count toward mastery.");
      expect(screen.getByTestId("lesson-library").textContent).not.toMatch(/%|percent|\d+ of \d+/);
      expect(Object.values(STATE_COPY)).toContain("Not read");
   });

   it("opens the library reader from a row with a signed-off lesson, and a row without one is not a button", () => {
      const onOpenLesson = vi.fn();

      render(<LessonLibrary library={LIBRARY} onOpenLesson={onOpenLesson} />);

      fireEvent.click(screen.getByRole("button", { name: /The product rule/ }));

      expect(onOpenLesson).toHaveBeenCalledWith("LSN-CON-02013", "The product rule");
      expect(screen.queryByRole("button", { name: /The chain rule/ })).toBeNull();
   });

   it("progress shows the section under the mastery map and opens the reader, whose back returns to progress", async () => {
      mocked.readMasteryMap.mockRejectedValue(new Error("offline"));
      mocked.readCalibration.mockRejectedValue(new Error("offline"));
      mocked.readRepresentations.mockRejectedValue(new Error("offline"));
      mocked.readCheckpoints.mockRejectedValue(new Error("offline"));
      mocked.readProbe.mockRejectedValue(new Error("offline"));
      mocked.readMockHistory.mockRejectedValue(new Error("offline"));
      mocked.readLibrary.mockResolvedValue(LIBRARY);
      mocked.readLessonPlan.mockResolvedValue({ lesson: LESSON, plan: planFor(["LSN-CON-02013#s1"]), band: "low", state: null });
      mocked.postLessonEvent.mockResolvedValue({ ok: true, state: null });

      render(<ProgressRoute />);

      const library = await screen.findByTestId("lesson-library");
      const order = Array.from(document.querySelectorAll("[data-testid='mastery-failed'], [data-testid='lesson-library']")).map((node) =>
         node.getAttribute("data-testid")
      );

      expect(order).toEqual(["mastery-failed", "lesson-library"]);

      fireEvent.click(within(library).getByRole("button", { name: /The product rule/ }));

      expect(await screen.findByTestId("lesson-reader")).toBeTruthy();
      expect(mocked.readLessonPlan).toHaveBeenCalledWith("LSN-CON-02013", "low", "read_again");
      expect(screen.getByTestId("lesson-top-bar").textContent).toBe("The product rule");

      fireEvent.click(screen.getByTestId("lesson-back"));

      expect(await screen.findByTestId("lesson-library")).toBeTruthy();
   });
});
