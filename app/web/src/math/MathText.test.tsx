import { describe, expect, it } from "vitest";
import { render } from "@testing-library/react";
import { MathText } from "./MathText";
import { holdUnclosedMath, splitInlineMath } from "./mathjson";

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

describe("MathText for the live tutor", () => {
   it("typesets \\[ \\] as displayed math beside \\( \\) inline math", () => {
      const reply = "Compare \\(u'v\\) with the rule \\[ (uv)' = u'v + uv' \\] and name each factor.";
      const { container } = render(<MathText text={reply} renderer="tutor" />);

      expect(container.querySelectorAll(".katex").length).toBe(2);
      expect(container.querySelectorAll(".katex-display").length).toBe(1);
      expect(container.textContent).not.toContain("\\[");
      expect(splitInlineMath(reply).map((segment) => segment.kind)).toEqual(["text", "math", "text", "math", "text"]);
   });

   it("shows a formula KaTeX refuses as its reading, never KaTeX's error text", () => {
      const { container } = render(<MathText text="Try \\(\\frac{1}{\\) here." renderer="tutor" />);

      expect(container.querySelector(".katex-error")).toBeNull();
      expect(container.textContent).not.toMatch(/ParseError|KaTeX/);
   });

   it("holds back everything after an unclosed delimiter, and nothing once it closes", () => {
      expect(holdUnclosedMath("Look at \\(x^2 + ")).toEqual({ shown: "Look at ", held: "\\(x^2 + " });
      expect(holdUnclosedMath("First \\(a\\), then \\[ b")).toEqual({ shown: "First \\(a\\), then ", held: "\\[ b" });
      expect(holdUnclosedMath("Done \\(a\\) and \\[b\\].")).toEqual({ shown: "Done \\(a\\) and \\[b\\].", held: "" });
   });
});
