import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import { CLOCK_STORAGE_KEY, DrillClock } from "./DrillClock";
import { HIDE_CLOCK, SHOW_CLOCK } from "./words";

/* docs/calculator/design.md, The drills: the clock reads minutes and seconds, hides on its own
   control, and stays hidden across drills in this browser. */

beforeEach(() => {
   window.localStorage.clear();
});

afterEach(() => {
   cleanup();
});

describe("the drill clock", () => {
   it("reads the elapsed minutes and seconds and stops where it was stopped", () => {
      render(<DrillClock startedAt={1000} stoppedAt={1000 + 83500} now={() => 999999} />);

      expect(screen.getByTestId("drill-clock-time").textContent).toBe("1:23");
   });

   it("hides, and a later drill's clock stays hidden until shown again", () => {
      render(<DrillClock startedAt={0} stoppedAt={null} now={() => 0} />);
      fireEvent.click(screen.getByRole("button", { name: HIDE_CLOCK }));

      expect(screen.queryByTestId("drill-clock-time")).toBeNull();
      expect(window.localStorage.getItem(CLOCK_STORAGE_KEY)).toBe("hidden");

      cleanup();
      render(<DrillClock startedAt={0} stoppedAt={null} now={() => 0} />);

      expect(screen.queryByTestId("drill-clock-time")).toBeNull();

      fireEvent.click(screen.getByRole("button", { name: SHOW_CLOCK }));

      expect(screen.getByTestId("drill-clock-time").textContent).toBe("0:00");
      expect(window.localStorage.getItem(CLOCK_STORAGE_KEY)).toBe("shown");
   });
});
