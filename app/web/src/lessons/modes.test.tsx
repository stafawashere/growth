import { act, cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { REDUCED_MOTION_QUERY } from "../styles/motion";
import { ContrastPanel } from "./ContrastPanel";
import { FigureControl } from "./FigureControl";
import { CONTRAST_SPEC, INTERACTIVE_SPEC, LESSON, MODEL_SPEC, MOTION_SPEC } from "./fixtures";
import { FrameStepper, FRAME_INTERVAL_MS } from "./FrameStepper";
import { ModelTable, computeModel } from "./ModelTable";

/* The mode components of TEMPLATE.md Delivery and amendments A-D2 to A-D4. The matchMedia mock is
   session/reduced_motion.test.tsx's: only the reduce query matches. */
function mockReducedMotion(reduce: boolean) {
   const matchMedia = (query: string) => {
      const asksForReduce = query.replace(/\s+/g, " ").trim() === REDUCED_MOTION_QUERY;

      return {
         matches: reduce && asksForReduce,
         media: query,
         onchange: null,
         addListener: () => undefined,
         removeListener: () => undefined,
         addEventListener: () => undefined,
         removeEventListener: () => undefined,
         dispatchEvent: () => false
      } as unknown as MediaQueryList;
   };

   vi.stubGlobal("matchMedia", matchMedia);
   window.matchMedia = matchMedia;
}

function frameIndex() {
   return Number(screen.getByTestId("frame-view").getAttribute("data-frame-index"));
}

afterEach(() => {
   cleanup();
   vi.useRealTimers();
   vi.unstubAllGlobals();
});

describe("FrameStepper", () => {
   beforeEach(() => {
      mockReducedMotion(false);
   });

   it("steps frames on ArrowRight and ArrowLeft, Home and End, and announces the frame", () => {
      render(<FrameStepper spec={MOTION_SPEC} fallback="The five frames in a row." />);

      const stepper = screen.getByTestId("frame-stepper");

      expect(frameIndex()).toBe(0);
      expect(screen.getByTestId("frame-announcement").textContent).toBe("Frame 1 of 5. h = 1");

      fireEvent.keyDown(stepper, { key: "ArrowRight" });
      fireEvent.keyDown(stepper, { key: "ArrowRight" });

      expect(frameIndex()).toBe(2);
      expect(screen.getByTestId("frame-announcement").textContent).toBe("Frame 3 of 5. h = 0.25");
      expect(screen.getByTestId("frame-announcement").getAttribute("aria-live")).toBe("polite");

      fireEvent.keyDown(stepper, { key: "ArrowLeft" });
      expect(frameIndex()).toBe(1);

      fireEvent.keyDown(stepper, { key: "End" });
      expect(frameIndex()).toBe(4);

      fireEvent.keyDown(stepper, { key: "ArrowRight" });
      expect(frameIndex()).toBe(4);

      fireEvent.keyDown(stepper, { key: "Home" });
      expect(frameIndex()).toBe(0);
   });

   it("re-renders the figure with the frame's values substituted", () => {
      render(<FrameStepper spec={MOTION_SPEC} fallback="The five frames in a row." />);

      const labelAt = () => screen.getAllByTestId("figure-label").map((label) => label.textContent);

      expect(labelAt()).toContain("h = 1");

      fireEvent.keyDown(screen.getByTestId("frame-stepper"), { key: "ArrowRight" });

      expect(labelAt()).toContain("h = 0.5");
   });

   it("Space toggles auto-advance, which stops at the last frame", () => {
      vi.useFakeTimers();
      render(<FrameStepper spec={MOTION_SPEC} fallback="The five frames in a row." />);

      const stepper = screen.getByTestId("frame-stepper");

      fireEvent.keyDown(stepper, { key: " " });
      expect(screen.getByTestId("frame-auto").getAttribute("aria-pressed")).toBe("true");

      act(() => {
         vi.advanceTimersByTime(FRAME_INTERVAL_MS * 2);
      });
      expect(frameIndex()).toBe(2);

      fireEvent.keyDown(stepper, { key: " " });
      act(() => {
         vi.advanceTimersByTime(FRAME_INTERVAL_MS * 3);
      });
      expect(frameIndex()).toBe(2);

      fireEvent.keyDown(stepper, { key: " " });
      act(() => {
         vi.advanceTimersByTime(FRAME_INTERVAL_MS * 10);
      });
      expect(frameIndex()).toBe(4);
   });

   it("under prefers-reduced-motion: reduce never auto-advances and cross-fades on key press", () => {
      mockReducedMotion(true);
      vi.useFakeTimers();
      render(<FrameStepper spec={MOTION_SPEC} fallback="The five frames in a row." />);

      const stepper = screen.getByTestId("frame-stepper");

      expect(screen.queryByTestId("frame-auto")).toBeNull();

      fireEvent.keyDown(stepper, { key: " " });
      act(() => {
         vi.advanceTimersByTime(FRAME_INTERVAL_MS * 10);
      });
      expect(frameIndex()).toBe(0);

      fireEvent.keyDown(stepper, { key: "ArrowRight" });
      expect(frameIndex()).toBe(1);
      expect(screen.getByTestId("frame-view").className).toContain("lesson-frame-fading");

      act(() => {
         vi.advanceTimersByTime(FRAME_INTERVAL_MS);
      });
      expect(screen.getByTestId("frame-view").className).not.toContain("lesson-frame-fading");
      expect(frameIndex()).toBe(1);
   });

   it("shows the fallback on every frame of a kind it cannot draw", () => {
      render(<FrameStepper spec={{ kind: "hologram", frames: [{ a: 1 }, { a: 2 }] }} fallback="Two static panels." />);

      expect(screen.getByTestId("lesson-figure-fallback").textContent).toContain("Two static panels.");

      fireEvent.keyDown(screen.getByTestId("frame-stepper"), { key: "ArrowRight" });

      expect(screen.getByTestId("lesson-figure-fallback").textContent).toContain("Two static panels.");
   });

   it("renders the fallback, not a blank, when the spec names no frames", () => {
      render(<FrameStepper spec={{ kind: "graph" }} fallback="No frames here." />);

      expect(screen.getByTestId("lesson-figure-fallback").textContent).toContain("No frames here.");
   });
});

describe("FigureControl", () => {
   it("asks the spec's question above one control, which moves by its step on the arrow keys and updates the readout", () => {
      render(<FigureControl spec={INTERACTIVE_SPEC} fallback="The graph of f' with its sign marked." />);

      expect(screen.getByTestId("control-question").textContent).toBe(INTERACTIVE_SPEC.question);
      expect(screen.getAllByTestId("figure-control")).toHaveLength(1);

      const control = screen.getByTestId("figure-control") as HTMLInputElement;
      const before = screen.getByTestId("control-readout").textContent;

      expect(control.value).toBe("-3");

      fireEvent.keyDown(control, { key: "ArrowRight" });

      expect(Number(control.value)).toBeCloseTo(-2.9, 9);
      expect(screen.getByTestId("control-readout").textContent).not.toBe(before);
      expect(screen.getByTestId("control-readout").textContent).toContain("x = -2.9");

      fireEvent.keyDown(control, { key: "ArrowLeft" });
      fireEvent.keyDown(control, { key: "ArrowLeft" });
      expect(Number(control.value)).toBe(-3);

      fireEvent.keyDown(control, { key: "End" });
      expect(Number(control.value)).toBe(2);

      fireEvent.keyDown(control, { key: "Home" });
      expect(Number(control.value)).toBe(-3);
   });

   it("re-renders the figure with the control's value", () => {
      render(<FigureControl spec={INTERACTIVE_SPEC} fallback="The graph of f'." />);

      const pointX = () => screen.getByTestId("figure-graph").querySelector("line.figure-mark-dashed")!.getAttribute("x1");
      const before = pointX();

      fireEvent.keyDown(screen.getByTestId("figure-control"), { key: "ArrowUp" });

      expect(pointX()).not.toBe(before);
   });

   it("steps through a stepper's values", () => {
      render(
         <FigureControl
            spec={{
               kind: "solution_curves",
               equation: "dP/dt = 2P/5 - P^2/2000",
               window: { t: [0, 30], P: [0, 1000] },
               controls: [{ type: "stepper", parameter: "P(0)", values: [160, 400, 640, 960], start: 160 }],
               labels: [{ text: "P = 800: rate zero", placement: "inside" }],
               question: "Which level does the curve approach?"
            }}
            fallback="Four curves."
         />
      );

      const control = screen.getByTestId("figure-control");

      expect(screen.getByTestId("control-readout").textContent).toContain("P(0) = 160");

      fireEvent.keyDown(control, { key: "ArrowRight" });

      expect(screen.getByTestId("control-readout").textContent).toContain("P(0) = 400");
   });

   it("shows the fallback with the question when the spec cannot be drawn or names no control", () => {
      render(<FigureControl spec={{ kind: "diagram", shape: "cone", question: "Which labels change?" }} fallback="A cone." />);

      expect(screen.getByTestId("lesson-figure-fallback").textContent).toContain("A cone.");
      expect(screen.getByTestId("control-question").textContent).toBe("Which labels change?");
   });
});

describe("ModelTable", () => {
   it("computes the table from the function at the h values", () => {
      const model = computeModel(MODEL_SPEC)!;

      expect(model.rows.map((row) => row[0])).toEqual([1, 0.1, 0.01, 0.001]);
      expect(model.rows[0][1]).toBeCloseTo(11, 9);
      expect(model.rows[3][1]).toBeCloseTo(8.003, 9);
   });

   it("computes Riemann sums at the n values and Euler steps from an equation", () => {
      const sums = computeModel({ kind: "numeric_experiment", function: "3*x**2", interval: [1, 3], sum: "right", n_values: [2, 100], columns: ["n", "right sum"] })!;

      expect(sums.rows[0]).toEqual([2, 39]);
      expect(sums.rows[1][1]).toBeCloseTo(26.2404, 3);

      const euler = computeModel({ kind: "numeric_experiment", equation: "dy/dx = 2*x + y + 1", start: [0, 1], step: 0.5, columns: ["x", "y", "slope"] })!;

      expect(euler.rows.slice(0, 3)).toEqual([[0, 1, 2], [0.5, 2, 4], [1, 4, 7]]);
   });

   it("shows the computed table beside its figure with the current row highlighted, one row added per Run", () => {
      render(<ModelTable spec={MODEL_SPEC} fallback="The four rows as a static table." />);

      expect(screen.getByTestId("figure-graph")).toBeTruthy();
      expect(screen.getByTestId("lesson-table").querySelectorAll("tbody tr")).toHaveLength(1);

      fireEvent.click(screen.getByTestId("model-run"));

      const rows = screen.getByTestId("lesson-table").querySelectorAll("tbody tr");

      expect(rows).toHaveLength(2);
      expect(rows[1].getAttribute("data-current")).toBe("true");
      expect(rows[1].textContent).toContain("current");
      expect(rows[0].getAttribute("data-current")).toBe("false");
   });

   it("falls back when the function cannot be read", () => {
      render(<ModelTable spec={{ kind: "numeric_experiment", function: "f from ex-1", x_values: [1, 2], columns: ["x", "total"] }} fallback="The running totals." />);

      expect(screen.getByTestId("lesson-figure-fallback").textContent).toContain("The running totals.");
   });
});

describe("ContrastPanel", () => {
   it("puts every stem on one screen with the selecting feature marked in each", () => {
      render(<ContrastPanel decision={LESSON.decision!} delivery={LESSON.decision!.delivery} />);

      const stems = screen.getAllByTestId("contrast-stem");

      expect(stems).toHaveLength(2);
      expect(within(stems[0]).getByTestId("contrast-feature").textContent).toContain("a product of two expressions");
      expect(within(stems[1]).getByTestId("contrast-feature").textContent).toContain("four supplied values at a point");
      expect(screen.getByTestId("contrast-panel").textContent).toContain("whether the stem gives expressions or values");
      expect(CONTRAST_SPEC.kind).toBe("panels");
   });
});
