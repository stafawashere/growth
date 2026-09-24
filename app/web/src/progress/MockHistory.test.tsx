import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";

import { MockHistory } from "./MockHistory";

afterEach(() => {
   cleanup();
});

describe("mock history on progress", () => {
   it("lists each finished mock with its date, band and raw counts, and no single score", () => {
      render(
         <MockHistory
            history={{
               mocks: [
                  {
                     session_id: "SES-1",
                     taken_at: "2026-09-24T21:50:04.525785+00:00",
                     band: { low: 1, high: 5 },
                     multiple_choice: { correct: 14, total: 42 },
                     free_response: { earned: 0, pending: 32, total: 54 }
                  },
                  {
                     session_id: "SES-2",
                     taken_at: "2026-11-02T15:00:00+00:00",
                     band: { low: 3, high: 5 },
                     multiple_choice: { correct: 30, total: 42 },
                     free_response: { earned: 31, pending: 0, total: 54 }
                  }
               ]
            }}
         />
      );

      const rows = screen.getAllByTestId("mock-history-row").map((row) => row.textContent);

      expect(rows).toEqual([
         "24 September 2026Band: 1 to 5Multiple choice 14 of 42 correctFree response 0 of 54 points, 32 pending",
         "2 November 2026Band: 3 to 5Multiple choice 30 of 42 correctFree response 31 of 54 points, 0 pending"
      ]);
      expect(document.body.textContent).not.toMatch(/predict|score|trend/i);
   });

   it("says so when no mock has been finished", () => {
      render(<MockHistory history={{ mocks: [] }} />);

      expect(screen.getByText("No mock has been finished yet.")).toBeTruthy();
      expect(screen.queryByTestId("mock-history-row")).toBeNull();
   });
});
