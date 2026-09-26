import { describe, expect, it } from "vitest";
import { render } from "@testing-library/react";
import { FigureView, PLOT_PADDING, VIEW_WIDTH } from "./FigureView";

/* A mock question was missed because a value had to be read off a function graph by counting grid
   squares. Every gridline on both axes now carries its number. */

const PLOT_WIDTH = VIEW_WIDTH - PLOT_PADDING * 2;

const EVERY_VALUE_BUT_ZERO = ["-8", "-7", "-6", "-5", "-4", "-3", "-2", "-1", "1", "2", "3", "4", "5", "6", "7", "8"];

function graph(overrides: Record<string, unknown> = {}) {
   return {
      kind: "function_graph",
      domain: [-8, 8],
      range: [-8, 8],
      curves: [],
      fills: [],
      marks: [],
      labels: [],
      gridlines: true,
      axis_titles: ["x", "y"],
      alt: "The graph of f on the closed interval from -8 to 8.",
      ...overrides
   };
}

function ticks(container: HTMLElement, axis: "x" | "y") {
   return Array.from(container.querySelectorAll(`text.figure-tick[data-axis="${axis}"]`));
}

function tickTexts(container: HTMLElement, axis: "x" | "y") {
   return ticks(container, axis).map((tick) => tick.textContent);
}

describe("function graph tick labels", () => {
   it("prints the value of every gridline on both axes, leaving out the origin the axes cross at", () => {
      const { container } = render(<FigureView spec={graph()} />);

      expect(tickTexts(container, "x")).toEqual(EVERY_VALUE_BUT_ZERO);
      expect(tickTexts(container, "y")).toEqual(EVERY_VALUE_BUT_ZERO);
   });

   it("puts each x value under its own gridline and each y value level with its own", () => {
      const { container } = render(<FigureView spec={graph()} />);
      const gridlines = Array.from(container.querySelectorAll('[data-testid="figure-gridlines"] line'));
      const verticalXs = gridlines.filter((line) => line.getAttribute("x1") === line.getAttribute("x2")).map((line) => Number(line.getAttribute("x1")));
      const horizontalYs = gridlines.filter((line) => line.getAttribute("y1") === line.getAttribute("y2")).map((line) => Number(line.getAttribute("y1")));

      expect(ticks(container, "x").length).toBe(EVERY_VALUE_BUT_ZERO.length);
      expect(ticks(container, "y").length).toBe(EVERY_VALUE_BUT_ZERO.length);

      for (const tick of ticks(container, "x")) {
         const value = Number(tick.textContent);
         const expectedX = PLOT_PADDING + ((value + 8) / 16) * PLOT_WIDTH;

         expect(Number(tick.getAttribute("x"))).toBeCloseTo(expectedX);
         expect(verticalXs.some((x) => Math.abs(x - expectedX) < 1e-9)).toBe(true);
      }

      for (const tick of ticks(container, "y")) {
         const value = Number(tick.textContent);
         const expectedY = PLOT_PADDING + ((8 - value) / 16) * PLOT_WIDTH;

         expect(Number(tick.getAttribute("y"))).toBeCloseTo(expectedY);
         expect(horizontalYs.some((y) => Math.abs(y - expectedY) < 1e-9)).toBe(true);
      }
   });

   it("labels a window the axes do not cross along its edges, every gridline included", () => {
      const { container } = render(<FigureView spec={graph({ domain: [2, 12], range: [3, 13] })} />);

      expect(tickTexts(container, "x")).toEqual(["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]);
      expect(tickTexts(container, "y")).toEqual(["3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]);
   });

   it("leaves out a tick label that would print over a label the figure carries", () => {
      const underTwo = { text: "P", anchor: [2, -0.4], placement: "inside" };
      const { container } = render(<FigureView spec={graph({ labels: [underTwo] })} />);

      expect(tickTexts(container, "x")).toEqual(EVERY_VALUE_BUT_ZERO.filter((value) => value !== "2"));
      expect(tickTexts(container, "y")).toEqual(EVERY_VALUE_BUT_ZERO);
   });

   it("draws its numbers inside the figure's own drawing, which a screen reader reads through the alt", () => {
      const { container } = render(<FigureView spec={graph()} />);
      const svg = container.querySelector("svg")!;

      const allTicks = [...ticks(container, "x"), ...ticks(container, "y")];

      expect(allTicks.length).toBeGreaterThan(0);
      expect(allTicks.every((tick) => svg.contains(tick))).toBe(true);
      expect(svg.getAttribute("role")).toBe("img");
   });
});
