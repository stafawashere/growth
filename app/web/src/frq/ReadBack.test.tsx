import { describe, expect, it } from "vitest";

import { mixedText } from "./ReadBack";

describe("what a read-back answer or evidence quote is shown as", () => {
   it("typesets bare LaTeX and leaves words and delimited math as they are", () => {
      expect(mixedText("x = 3")).toBe("\\(x = 3\\)");
      expect(mixedText("(x-3)e^{x} = 0")).toBe("\\((x-3)e^{x} = 0\\)");
      expect(mixedText("g has a relative minimum at x = 3")).toBe("g has a relative minimum at x = 3");
      expect(mixedText("so \\(g\\) has a minimum")).toBe("so \\(g\\) has a minimum");
      expect(mixedText("\\sin x + \\cos x")).toBe("\\(\\sin x + \\cos x\\)");
   });
});
