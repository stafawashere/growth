import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { measure, measured } from "./fixtures";
import { MeasuredView } from "./MeasuredView";
import { NOT_MEASURED_YET } from "./words";

/* docs/calculator/design.md, The measured view: every figure over its denominator, and the median
   time "not measured yet" under three answered drills, never a number. */

afterEach(() => {
   cleanup();
});

function medianFor(capability: string) {
   const row = screen.getAllByTestId("measured-row").find((element) => element.getAttribute("data-capability") === capability);

   return row?.querySelector("[data-testid='measured-median']")?.textContent;
}

describe("the measured view", () => {
   it("says not measured yet under three answered drills and gives the median from three", () => {
      render(<MeasuredView measured={measured([measure("integral", 14, 38000), measure("derivative", 2, 51000), measure("zero", 0, null)])} />);

      expect(medianFor("integral")).toBe("38 seconds");
      expect(medianFor("derivative")).toBe(NOT_MEASURED_YET);
      expect(medianFor("zero")).toBe(NOT_MEASURED_YET);
   });

   it("puts a denominator on every figure and no percent anywhere", () => {
      const { container } = render(<MeasuredView measured={measured([measure("integral", 14, 38000)])} />);
      const cells = Array.from(screen.getAllByTestId("measured-row")[0].querySelectorAll("td")).map((cell) => cell.textContent);

      expect(cells).toEqual(["14", "14 of 14", "14 of 14", "14 of 14", "38 seconds"]);
      expect(container.textContent).not.toContain("%");
      expect(screen.getByTestId("measured-budget").textContent).toBe(
         "The exam allows 120 seconds a question on Section I Part B and 900 seconds a question on Section II Part A."
      );
   });
});
