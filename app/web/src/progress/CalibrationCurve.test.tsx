import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen, within } from "@testing-library/react";

import * as client from "../api/client";
import type { CalibrationBin, CalibrationPayload } from "../api/types";
import { CalibrationCurve } from "./CalibrationCurve";
import { ProgressRoute } from "./ProgressRoute";

vi.mock("../api/client");

const mocked = vi.mocked(client);

const bins: CalibrationBin[] = [
   { confidence: "guess", attempts: 12, correct: 3, accuracy: 0.25, interval_low: 0.0889, interval_high: 0.5324 },
   { confidence: "unsure", attempts: 0, correct: 0, accuracy: null, interval_low: null, interval_high: null },
   { confidence: "confident", attempts: 20, correct: 16, accuracy: 0.8, interval_low: 0.5840, interval_high: 0.9193 }
];

const available: CalibrationPayload = {
   available: true,
   rated_attempts: 32,
   minimum_rated_attempts: 30,
   attempts_needed: 0,
   window_days: 30,
   window_start: "2026-08-25",
   window_end: "2026-09-23",
   bins
};

const notYet: CalibrationPayload = {
   ...available,
   available: false,
   rated_attempts: 29,
   attempts_needed: 1,
   bins: []
};

afterEach(() => {
   cleanup();
   vi.clearAllMocks();
});

function pointFor(confidence: string) {
   const group = document.querySelector(`[data-testid="calibration-point"][data-confidence="${confidence}"]`);

   expect(group, `no point drawn for ${confidence}`).not.toBeNull();

   const circle = group!.querySelector("circle")!;
   const interval = group!.querySelector('[data-testid="calibration-interval"]')!;

   return {
      group: group!,
      pointY: Number(circle.getAttribute("cy")),
      lowY: Number(interval.getAttribute("y1")),
      highY: Number(interval.getAttribute("y2"))
   };
}

describe("the calibration curve below its threshold", () => {
   it("states the count and the shortfall and draws nothing", () => {
      render(<CalibrationCurve calibration={notYet} />);

      const message = screen.getByTestId("calibration-not-yet").textContent!.replace(/\s+/g, " ");

      expect(message).toContain("needs 30 confidence-rated attempts");
      expect(message).toContain("29 are recorded so far");
      expect(message).toContain("1 more are needed");
      expect(screen.queryByTestId("calibration-curve")).toBeNull();
      expect(screen.queryByTestId("calibration-table")).toBeNull();
   });

   it("refuses to draw when the payload says unavailable even if bins came with it", () => {
      render(<CalibrationCurve calibration={{ ...notYet, bins }} />);

      expect(screen.getByTestId("calibration-not-yet")).toBeTruthy();
      expect(document.querySelectorAll('[data-testid="calibration-point"]').length).toBe(0);
   });
});

describe("the calibration curve at or above its threshold", () => {
   it("plots accuracy upward against stated confidence with the interval around each point", () => {
      render(<CalibrationCurve calibration={available} />);

      const curve = screen.getByRole("img", { name: /calibration curve/i });
      const guess = pointFor("guess");
      const confident = pointFor("confident");

      expect(curve.getAttribute("data-testid")).toBe("calibration-curve");
      expect(confident.pointY).toBeLessThan(guess.pointY);

      for (const point of [guess, confident]) {
         expect(point.highY).toBeLessThan(point.pointY);
         expect(point.lowY).toBeGreaterThan(point.pointY);
      }

      expect(guess.group.textContent).toContain("n = 12");
      expect(confident.group.textContent).toContain("n = 20");
   });

   it("draws no point for a level with no attempts and says n = 0 there", () => {
      render(<CalibrationCurve calibration={available} />);

      expect(document.querySelector('[data-confidence="unsure"]')).toBeNull();
      expect(screen.getByTestId("calibration-curve").textContent).toContain("n = 0");
   });

   it("gives a table with the same counts, accuracies and intervals as the text alternative", () => {
      render(<CalibrationCurve calibration={available} />);

      const table = screen.getByTestId("calibration-table");
      const rows = within(table)
         .getAllByRole("row")
         .slice(1)
         .map((row) => Array.from(row.children).map((cell) => cell.textContent));

      expect(rows).toEqual([
         ["guess", "12", "3", "25 percent", "9 percent to 53 percent"],
         ["unsure", "0", "0", "no attempts", "none"],
         ["confident", "20", "16", "80 percent", "58 percent to 92 percent"]
      ]);
      expect(table.querySelector("caption")!.textContent).toContain("32 rated attempts");
      expect(screen.getByTestId("calibration-curve").getAttribute("aria-labelledby")).toMatch(/description/);
   });
});

describe("the progress route", () => {
   beforeEach(() => {
      mocked.readMasteryMap.mockReturnValue(new Promise(() => undefined));
   });

   it("loads the calibration record and draws the curve from it", async () => {
      mocked.readCalibration.mockResolvedValue(available);
      render(<ProgressRoute />);

      expect(await screen.findByTestId("calibration-curve")).toBeTruthy();
      expect(mocked.readCalibration).toHaveBeenCalledTimes(1);
   });

   it("shows the not-yet state when the server has fewer than 30 rated attempts", async () => {
      mocked.readCalibration.mockResolvedValue(notYet);
      render(<ProgressRoute />);

      expect(await screen.findByTestId("calibration-not-yet")).toBeTruthy();
      expect(screen.queryByTestId("calibration-curve")).toBeNull();
   });

   it("says the record could not be loaded rather than drawing a stand-in", async () => {
      mocked.readCalibration.mockRejectedValue(new Error("the connection dropped"));
      render(<ProgressRoute />);

      expect(await screen.findByTestId("progress-failed")).toBeTruthy();
      expect(screen.queryByTestId("calibration-curve")).toBeNull();
   });
});

describe("the progress sources", () => {
   const directory = join(process.cwd(), "src", "progress");
   const sources = readdirSync(directory)
      .filter((entry) => entry.endsWith(".tsx") && !entry.includes(".test."))
      .map((entry) => ({ entry, source: readFileSync(join(directory, entry), "utf8") }));

   it("author every colour as a growth token and animate nothing", () => {
      expect(sources.length).toBeGreaterThan(0);

      let tokenReferences = 0;

      for (const { entry, source } of sources) {
         const references = source.match(/var\(\s*--[\w-]+/g) ?? [];

         expect(source, entry).not.toMatch(/#[0-9a-fA-F]{3,8}\b/);
         expect(source, entry).not.toMatch(/\brgba?\(|\bhsla?\(/);
         expect(references.filter((reference) => !reference.includes("--growth-")), entry).toEqual([]);
         expect(source, entry).not.toMatch(/transition|animation|@keyframes|motion-/);

         tokenReferences += references.length;
      }

      expect(tokenReferences, "the scan found no token reference at all").toBeGreaterThan(0);
   });
});
