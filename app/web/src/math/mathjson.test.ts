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
