import { describe, expect, it } from "vitest";
import { render } from "@testing-library/react";
import { FigureView, PLOT_PADDING, VIEW_WIDTH } from "./FigureView";

const PLOT_WIDTH = VIEW_WIDTH - PLOT_PADDING * 2;

function squareGraph(overrides: Record<string, unknown> = {}) {
   return {
      kind: "function_graph",
      domain: [-2, 2],
      range: [-2, 2],
      curves: [],
      fills: [],
      marks: [],
      labels: [],
      gridlines: true,
      axis_titles: ["x", "y"],
      alt: "The graph of f on the closed interval from -2 to 2.",
      ...overrides
   };
}

function pointCount(polyline: Element) {
   return (polyline.getAttribute("points") ?? "").trim().split(/\s+/).length;
}

describe("FigureView graph kinds", () => {
   it("draws each label as an SVG text node at its anchor mapped into the view, with nothing outside the SVG", () => {
      const spec = squareGraph({ labels: [{ text: "y = f(x)", anchor: [1, 1], placement: "inside" }] });
      const { container } = render(<FigureView spec={spec} />);

      const svg = container.querySelector("svg");
      const label = svg?.querySelector('[data-testid="figure-label"]');
      const expectedX = PLOT_PADDING + (3 / 4) * PLOT_WIDTH;
      const expectedY = PLOT_PADDING + (1 / 4) * PLOT_WIDTH;

      expect(svg?.getAttribute("role")).toBe("img");
      expect(svg?.getAttribute("aria-label")).toBe(spec.alt);
      expect(label?.tagName.toLowerCase()).toBe("text");
      expect(label?.textContent).toBe("y = f(x)");
      expect(Number(label?.getAttribute("x"))).toBeCloseTo(expectedX);
      expect(Number(label?.getAttribute("y"))).toBeCloseTo(expectedY);
      expect(container.querySelector("figcaption")).toBeNull();
      expect(container.textContent?.replace(svg?.textContent ?? "", "")).toBe("");
   });

   it("flips y so a point higher in the figure has a smaller SVG y", () => {
      const spec = squareGraph({
         marks: [
            { type: "point", at: [0, -1] },
            { type: "open_point", at: [0, 1] }
         ]
      });
      const { container } = render(<FigureView spec={spec} />);

      const lower = container.querySelector('circle[data-mark="point"]');
      const higher = container.querySelector('circle[data-mark="open_point"]');

      expect(Number(higher?.getAttribute("cy"))).toBeLessThan(Number(lower?.getAttribute("cy")));
   });

   it("draws each curve segment as its own polyline carrying every sampled point", () => {
      const firstSegment = [[-2, -1], [-1, 0], [0, 1], [1, 0], [2, -1]];
      const secondSegment = [[-1, 1.5], [0, 1.8], [1, 1.5]];
      const spec = squareGraph({ curves: [{ segments: [firstSegment, secondSegment], style: "solid" }] });
      const { container } = render(<FigureView spec={spec} />);

      const polylines = Array.from(container.querySelectorAll("polyline"));

      expect(polylines.length).toBe(2);
      expect(pointCount(polylines[0])).toBe(firstSegment.length);
      expect(pointCount(polylines[1])).toBe(secondSegment.length);
   });

   it("renders nothing, and does not throw, for a spec it cannot read", () => {
      const malformed: unknown[] = [
         null,
         "function_graph",
         { kind: "pie_chart", domain: [0, 1], range: [0, 1] },
         squareGraph({ domain: [2, -2] }),
         squareGraph({ range: [0] }),
         squareGraph({ curves: [{ segments: [[[0, "one"]]] }] }),
         squareGraph({ marks: [{ type: "arrow", at: [0, 0] }] }),
         squareGraph({ labels: [{ text: "A" }] }),
         { kind: "table", columns: [], rows: [] },
         { kind: "table", columns: ["x"], rows: [[1]] }
      ];

      for (const spec of malformed) {
         const { container, unmount } = render(<FigureView spec={spec} />);

         expect(container.innerHTML).toBe("");

         unmount();
      }
   });
});

describe("FigureView table kind", () => {
   it("renders a header row and body cells, typesetting inline LaTeX through MathText", () => {
      const spec = {
         kind: "table",
         columns: ["\\(x\\)", "\\(f(x)\\)"],
         rows: [
            ["0", "\\(\\frac{1}{2}\\)"],
            ["1", "3"]
         ],
         labels: [],
         alt: "A table of f at x equal to 0 and 1."
      };
      const { container } = render(<FigureView spec={spec} />);

      const headers = container.querySelectorAll("thead th");
      const cells = container.querySelectorAll("tbody td");
      const caption = container.querySelector("caption");

      expect(headers.length).toBe(2);
      expect(cells.length).toBe(4);
      expect(container.querySelectorAll("thead .katex").length).toBe(2);
      expect(cells[1].querySelectorAll(".katex").length).toBe(1);
      expect(container.textContent).not.toMatch(/\\\(/);
      expect(caption?.textContent).toBe(spec.alt);
      expect(caption?.className).toBe("visually-hidden");
   });
});
