import { describe, expect, it } from "vitest";

import { mathJsonToLatex, renderLatexToMarkup } from "./mathjson";

/* compute-engine 0.24 writes the constant e as \exponentialE, a macro of its own that KaTeX does
   not know, so an option holding e rendered as raw LaTeX. */
describe("mathJsonToLatex", () => {
   it("writes the constant e in a form KaTeX renders", () => {
      const latex = mathJsonToLatex(["Multiply", 440, ["Power", "ExponentialE", "t"]]);
      const markup = renderLatexToMarkup(latex);

      expect(latex).not.toContain("exponentialE");
      expect(markup).not.toContain("katex-error");
      expect(markup).toContain("<mi mathvariant=\"normal\">e</mi>");
   });
});

describe("mathJsonToLatex decimal strings", () => {
   it("keeps the trailing zeros of a decimal string number", () => {
      expect(mathJsonToLatex({ num: "4.290" })).toBe("4.290");
      expect(mathJsonToLatex({ num: "0.100" })).toBe("0.100");
   });

   it("keeps the trailing zeros of a decimal string inside an expression", () => {
      expect(mathJsonToLatex(["Negate", { num: "0.760" }])).toBe("-0.760");
      expect(mathJsonToLatex(["Add", "x", { num: "2.500" }])).toContain("2.500");
   });
});
