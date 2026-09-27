import { cleanup, fireEvent, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { DESKTOP_WIDTH, PHONE_WIDTH, declared, setViewportWidth } from "../testing/cascade";
import { partRunner } from "../testing/screens";
import { calculatorPart, noCalculatorPart } from "./fixtures";

vi.mock("../api/client");

/* 08 puts reference material beside the problem. From 1100 px an open graphing panel and the
   question sit in two columns; below it, and while the panel is closed, they stack as before. The
   layout is read from app.css at each width through the evals' cascade. */

const NARROW_DESKTOP = 1099;

function layoutAt(width: number) {
   setViewportWidth(width);

   const layout = screen.getByTestId("part-runner").querySelector(".question-layout")!;
   const display = declared(layout, "display");

   setViewportWidth(DESKTOP_WIDTH);

   return display;
}

afterEach(() => {
   cleanup();
   setViewportWidth(DESKTOP_WIDTH);
});

describe("the graphing panel beside the question", () => {
   it("sits beside the question from 1100 px while it is open, and stacks when closed or narrower", async () => {
      await partRunner(calculatorPart());

      const part = screen.getByTestId("part-runner");
      const panel = screen.getByTestId("graphing-panel");
      const questionColumn = screen.getByTestId("question-area").parentElement!;

      expect(layoutAt(DESKTOP_WIDTH)).toBeNull();

      fireEvent.click(screen.getByRole("button", { name: "Open graphing panel" }));

      expect(part.getAttribute("data-graphing-open")).toBe("true");
      expect(layoutAt(DESKTOP_WIDTH)).toBe("flex");
      expect(layoutAt(1100)).toBe("flex");
      expect(layoutAt(NARROW_DESKTOP)).toBeNull();
      expect(layoutAt(PHONE_WIDTH)).toBeNull();
      expect(panel.nextElementSibling).toBe(questionColumn);

      fireEvent.click(screen.getByRole("button", { name: "Close graphing panel" }));

      expect(part.hasAttribute("data-graphing-open")).toBe(false);
      expect(layoutAt(DESKTOP_WIDTH)).toBeNull();
   });

   it("never appears on a part without a calculator, so nothing is laid out beside the question", async () => {
      await partRunner(noCalculatorPart());

      expect(screen.queryByTestId("graphing-panel")).toBeNull();
      expect(screen.getByTestId("part-runner").hasAttribute("data-graphing-open")).toBe(false);
      expect(layoutAt(DESKTOP_WIDTH)).toBeNull();
   });
});
