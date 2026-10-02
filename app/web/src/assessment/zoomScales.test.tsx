import { cleanup, fireEvent, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { declared } from "../testing/cascade";
import { partRunner } from "../testing/screens";
import { noCalculatorPart } from "./fixtures";

vi.mock("../api/client");

/* 08 names zoom among the Bluebook tools. Every size in app.css is a type token, so the percentage
   the student picks moves the stem and the answers up the type scale rather than scaling a length:
   body at 100, heading at 125, title at 150. The sizes are read from app.css through the cascade. */

afterEach(() => {
   cleanup();
});

describe("the zoom tool", () => {
   it("steps the stem and every answer up the type scale at 125 and 150 percent", async () => {
      await partRunner(noCalculatorPart());

      const stem = screen.getByTestId("question-stem");
      const answers = () => Array.from(document.querySelectorAll(".option-content"));

      expect(declared(stem, "font-size")).toBe("var(--growth-type-body)");

      fireEvent.click(screen.getByRole("button", { name: "125 percent" }));

      expect(declared(stem, "font-size")).toBe("var(--growth-type-heading)");
      expect(answers().length).toBeGreaterThan(0);
      expect(answers().map((answer) => declared(answer, "font-size"))).toEqual(answers().map(() => "var(--growth-type-heading)"));

      fireEvent.click(screen.getByRole("button", { name: "150 percent" }));

      expect(declared(stem, "font-size")).toBe("var(--growth-type-title)");
      expect(answers().map((answer) => declared(answer, "font-size"))).toEqual(answers().map(() => "var(--growth-type-title)"));

      fireEvent.click(screen.getByRole("button", { name: "100 percent" }));

      expect(declared(stem, "font-size")).toBe("var(--growth-type-body)");
   });
});
