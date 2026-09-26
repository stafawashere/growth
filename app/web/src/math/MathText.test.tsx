import { describe, expect, it } from "vitest";
import { render } from "@testing-library/react";
import { MathText } from "./MathText";

describe("MathText", () => {
   it("renders an agent-drafted plain-text stem unchanged, with no delimiters to typeset", () => {
      const stem = "Let s be defined by s(x) = k^2 sin(x) for x < pi/2.";
      const { container } = render(<MathText text={stem} />);

      expect(container.textContent).toBe(stem);
      expect(container.querySelectorAll(".katex").length).toBe(0);
   });

   it("typesets \\( \\)-delimited math and never prints the raw LaTeX source", () => {
      const stem = "Evaluate \\( \\lim_{x \\to 3} \\dfrac{x^2 - x - 6}{x^2 - 9} \\).";
      const { container } = render(<MathText text={stem} />);

      expect(container.querySelectorAll(".katex").length).toBe(1);

      const visibleMath = container.querySelector(".katex-html");

      expect(visibleMath?.textContent).not.toMatch(/\\/);
      expect(container.textContent?.startsWith("Evaluate ")).toBe(true);

      const region = container.querySelector(".katex")!;
      const trailing = region.parentElement!.nextElementSibling;

      expect(trailing?.textContent).toBe(".");
      expect(region.compareDocumentPosition(trailing!) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();

      const mathml = region.querySelector("math");

      expect(mathml, "KaTeX rendered no MathML").not.toBeNull();
      expect(mathml!.closest("[aria-hidden='true']"), "the MathML sits under aria-hidden").toBeNull();
      expect(region.querySelector(".katex-html")?.getAttribute("aria-hidden")).toBe("true");
      expect(container.querySelectorAll(".visually-hidden").length, "a plain-text reading duplicates the MathML").toBe(0);
   });
});
