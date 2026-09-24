import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";

import { GraphingPanel } from "./GraphingPanel";

afterEach(() => {
   cleanup();
});

function openPanelWith(source: string) {
   render(<GraphingPanel />);
   fireEvent.click(screen.getByRole("button", { name: "Open graphing panel" }));
   fireEvent.change(screen.getByLabelText("y ="), { target: { value: source } });
}

describe("the graphing panel", () => {
   it("starts in radians, says so, and evaluates trigonometry in degrees once switched", () => {
      openPanelWith("sin(x)");

      expect(screen.getByTestId("angle-mode").textContent).toBe("Angle mode: Radians");

      fireEvent.change(screen.getByLabelText("Derivative at x ="), { target: { value: "0" } });
      fireEvent.click(screen.getByRole("button", { name: "Find the derivative" }));

      expect(screen.getByTestId("graphing-derivative").textContent).toBe("The derivative at x = 0.000000 is 1.000000.");

      fireEvent.click(screen.getByRole("radio", { name: "Degrees" }));
      fireEvent.change(screen.getByLabelText("Integral from"), { target: { value: "0" } });
      fireEvent.change(screen.getByLabelText("to"), { target: { value: "180" } });
      fireEvent.click(screen.getByRole("button", { name: "Find the integral" }));

      expect(screen.getByTestId("angle-mode").textContent).toBe("Angle mode: Degrees");
      expect(screen.getByTestId("graphing-integral").textContent).toBe(
         `The integral from 0.000000 to 180.000000 is ${(360 / Math.PI).toFixed(6)}.`
      );
   });

   it("plots as an SVG with a text alternative and finds the zeros in the window", () => {
      openPanelWith("cos(x)");

      fireEvent.change(screen.getByLabelText("x min"), { target: { value: "1" } });
      fireEvent.change(screen.getByLabelText("x max"), { target: { value: "2" } });
      fireEvent.click(screen.getByRole("button", { name: "Find zeros in the window" }));

      const plot = screen.getByRole("img");

      expect(plot.tagName.toLowerCase()).toBe("svg");
      expect(plot.querySelectorAll("path").length).toBeGreaterThan(0);
      expect(screen.getByRole("img", { name: "Graph of y = cos(x) for x from 1 to 2 and y from -10 to 10." })).toBe(plot);
      expect(screen.getByTestId("graphing-zeros").textContent).toBe("Zeros in the window: x = 1.570796.");
   });
});
