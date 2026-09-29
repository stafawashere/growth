import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { INTEGRAL_CARD } from "./fixtures";
import { ProcedureCard } from "./ProcedureCard";
import { DRILL_THIS_LABEL } from "./words";

/* docs/calculator/design.md, The procedure cards: numbered steps with what is typed in a monospace
   span, the demonstration one step at a time through the lesson reader's step reveal, the habit,
   the Bluebook note, and a "Drill this" that names the card's capability. */

afterEach(() => {
   cleanup();
});

describe("a procedure card", () => {
   it("numbers the steps and sets each step's keys in a code span", () => {
      render(<ProcedureCard card={INTEGRAL_CARD} onDrill={vi.fn()} />);

      const steps = screen.getByTestId("procedure-steps");

      expect(steps.tagName).toBe("OL");
      expect(Array.from(steps.querySelectorAll("li code")).map((code) => code.textContent)).toEqual(["int", "dx"]);
      expect(screen.getByTestId("procedure-bluebook-note").textContent).toContain("Bluebook opens Desmos in radians.");
   });

   it("reveals the demonstration one step at a time, ending on the three-place answer", () => {
      render(<ProcedureCard card={INTEGRAL_CARD} onDrill={vi.fn()} />);

      expect(screen.getAllByTestId("lesson-step")).toHaveLength(1);

      const total = INTEGRAL_CARD.demonstration.lines.length + 3;

      for (let shown = 1; shown < total; shown += 1) {
         fireEvent.click(screen.getByTestId("lesson-next-step"));
      }

      const steps = screen.getAllByTestId("lesson-step");

      expect(steps).toHaveLength(total);
      expect(steps[1].querySelector("code")?.textContent).toBe("f(x)=sin(x^2)");
      expect(steps[total - 1].textContent).toContain("0.805");
      expect(screen.queryByTestId("lesson-next-step")).toBeNull();
   });

   it("drills the card's capability from Drill this", () => {
      const onDrill = vi.fn();

      render(<ProcedureCard card={INTEGRAL_CARD} onDrill={onDrill} />);
      fireEvent.click(screen.getByRole("button", { name: DRILL_THIS_LABEL }));

      expect(onDrill).toHaveBeenCalledWith("integral");
   });

   it("carries no reading time, no completion mark and no checkbox", () => {
      const { container } = render(<ProcedureCard card={INTEGRAL_CARD} onDrill={vi.fn()} />);

      expect(container.querySelectorAll("input[type='checkbox']")).toHaveLength(0);
      expect(container.textContent).not.toMatch(/minute|complete|done/i);
   });
});
