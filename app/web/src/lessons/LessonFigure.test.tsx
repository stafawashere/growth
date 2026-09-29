import { readFileSync } from "node:fs";
import { join } from "node:path";

import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { VIEW_WIDTH } from "../figures/FigureView";
import { GRAPH_SPEC, TABLE_SPEC } from "./fixtures";
import { LessonFigure } from "./LessonFigure";
import { LessonTable } from "./LessonTable";

afterEach(() => {
   cleanup();
});

function labelsInsideViewBox() {
   const svg = screen.getAllByTestId("figure-graph")[0];
   const [, , width, height] = svg.getAttribute("viewBox")!.split(" ").map(Number);

   return screen.getAllByTestId("figure-label").every((label) => {
      const x = Number(label.getAttribute("x"));
      const y = Number(label.getAttribute("y"));

      return x >= 0 && x <= width && y >= 0 && y <= height;
   });
}

describe("LessonFigure", () => {
   it("draws a graph kind through FigureView with every label inside the plot and no caption", () => {
      render(<LessonFigure spec={GRAPH_SPEC} fallback="The curve and its tangent." />);

      const svg = screen.getByTestId("figure-graph");

      expect(svg.getAttribute("data-kind")).toBe("function_graph");
      expect(svg.querySelectorAll("polyline").length).toBeGreaterThan(1);
      expect(screen.getAllByTestId("figure-label").map((label) => label.textContent)).toEqual([
         "(3, 5)",
         "y = f(x)",
         "tangent at x = 3"
      ]);
      expect(labelsInsideViewBox()).toBe(true);
      expect(Number(svg.getAttribute("viewBox")!.split(" ")[2])).toBe(VIEW_WIDTH);
      expect(document.querySelector("figcaption")).toBeNull();
      expect(screen.queryByTestId("lesson-figure-fallback")).toBeNull();
   });

   it("shows the fallback text inside a figure frame on an unknown kind, never a blank", () => {
      render(<LessonFigure spec={{ kind: "hologram" }} fallback="The five frames as small panels." />);

      const fallback = screen.getByTestId("lesson-figure-fallback");

      expect(fallback.tagName).toBe("FIGURE");
      expect(fallback.textContent).toContain("The five frames as small panels.");
      expect(screen.queryByTestId("figure-graph")).toBeNull();
   });

   it("shows the fallback when a known kind carries nothing it can draw", () => {
      render(
         <LessonFigure
            spec={{ kind: "diagram", shape: "cone, vertex down", labels: [{ text: "h", placement: "inside" }] }}
            fallback="A cone with water to depth h."
         />
      );

      expect(screen.getByTestId("lesson-figure-fallback").textContent).toContain("A cone with water to depth h.");
   });

   it("samples an implicit curve on the window by marching squares", () => {
      render(
         <LessonFigure
            spec={{ kind: "implicit_curve", curve: "(y - 1)^2 = x^2 (x + 3)", window: { x: [-4, 2], y: [-3, 5] }, labels: [{ text: "(0, 1): both 0", placement: "inside" }] }}
            fallback="The loop."
         />
      );

      expect(screen.getByTestId("figure-graph").querySelectorAll("polyline").length).toBeGreaterThan(20);
      expect(labelsInsideViewBox()).toBe(true);
   });

   it("draws a slope field, a parametric path and a vector diagram through the same path", () => {
      render(
         <>
            <LessonFigure spec={{ kind: "slope_field", equation: "dy/dx = 2*(y - x + 1)", window: { x: [-2, 2], y: [-2, 2] }, lattice_step: 1, labels: [] }} fallback="Field." />
            <LessonFigure spec={{ kind: "parametric_path", x_rate: "3*cos(t**2/2)", y_rate: "2*sqrt(t)*exp(-t/2)", t_range: [1, 3], start: [2, -3], points: [{ t: 1 }], labels: [{ text: "t = 1: (2, -3)", placement: "inside" }] }} fallback="Path." />
            <LessonFigure spec={{ kind: "vector_diagram", tail: [2, -3], head: [0.804, -1.5], legs: [{ axis: "x" }], labels: [{ text: "displacement", placement: "inside" }] }} fallback="Vector." />
         </>
      );

      expect(screen.getAllByTestId("figure-graph").map((svg) => svg.getAttribute("data-kind"))).toEqual([
         "slope_field",
         "parametric_curve",
         "vector_diagram"
      ]);
      expect(screen.queryByTestId("lesson-figure-fallback")).toBeNull();
   });

   it("draws panel kinds side by side, each through FigureView, with the parent's labels shared out", () => {
      render(
         <LessonFigure
            spec={{
               kind: "graph_panels",
               panels: [
                  { curve: "Abs(x)", window: { x: [-2, 2], y: [-1, 2] }, labels: [{ text: "corner", placement: "inside" }] },
                  { curve: "Abs(x)**(2/3)", window: { x: [-2, 2], y: [-1, 2] }, labels: [{ text: "cusp", placement: "inside" }] }
               ],
               labels: [{ text: "each continuous at x = 0", placement: "inside" }]
            }}
            fallback="Two panels."
         />
      );

      const panels = screen.getAllByTestId("lesson-figure-panel");

      expect(panels).toHaveLength(2);
      expect(within(panels[0]).getAllByTestId("figure-label").map((label) => label.textContent)).toEqual([
         "corner",
         "each continuous at x = 0"
      ]);
   });

   it("lays panels out as a row under the app stylesheet, not as the figure's column", () => {
      const sheet = document.createElement("style");
      sheet.textContent = readFileSync(join(__dirname, "..", "styles", "app.css"), "utf8");
      document.head.appendChild(sheet);

      try {
         const panelSpec = { curve: "Abs(x)", window: { x: [-2, 2], y: [-1, 2] } };
         render(<LessonFigure spec={{ kind: "graph_panels", panels: [panelSpec, panelSpec] }} fallback="Two panels." />);

         const panelRow = screen.getAllByTestId("lesson-figure-panel")[0].parentElement!;

         expect(panelRow.dataset.layout).toBe("row");
         expect(getComputedStyle(panelRow).flexDirection).toBe("row");
      } finally {
         sheet.remove();
      }
   });

   it("draws graph_with_table as the graph and its table", () => {
      render(
         <LessonFigure
            spec={{
               kind: "graph_with_table",
               axes: { x: [0, 8], y: [60, 110] },
               curves: [{ expr: "100 + 2*t - t**2", domain: [0, 8] }],
               tangent: { at: 4, slope: -6 },
               table: { columns: ["t", "V(t)"], rows: [[3.9, 92.59], [4, 92], [4.1, 91.39]] },
               labels: [{ text: "slope -6", placement: "inside" }]
            }}
            fallback="Graph and table."
         />
      );

      expect(screen.getByTestId("figure-graph")).toBeTruthy();
      expect(screen.getByTestId("lesson-table").querySelectorAll("tbody tr")).toHaveLength(3);
   });
});

describe("LessonTable", () => {
   it("renders columns and rows, marks the marked rows with a glyph and a word, and keeps its labels inside the frame", () => {
      render(<LessonTable spec={TABLE_SPEC} fallback="The five readings." />);

      const rows = screen.getByTestId("lesson-table").querySelectorAll("tbody tr");

      expect(rows).toHaveLength(5);
      expect(rows[1].getAttribute("data-marked")).toBe("true");
      expect(rows[1].textContent).toContain("marked");
      expect(rows[0].getAttribute("data-marked")).toBe("false");
      expect(screen.getByTestId("lesson-table").querySelector("tfoot")!.textContent).toContain("21/5 meters per minute");
   });

   it("shows the fallback when there are no columns", () => {
      render(<LessonTable spec={{ kind: "table", rows: [] }} fallback="The readings as prose." />);

      expect(screen.getByTestId("lesson-figure-fallback").textContent).toContain("The readings as prose.");
   });
});
