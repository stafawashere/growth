import { describe, expect, it } from "vitest";

import { render } from "@testing-library/react";

import { ReadBackView, mixedText } from "./ReadBack";

describe("what a read-back answer or evidence quote is shown as", () => {
   it("typesets bare LaTeX and leaves words and delimited math as they are", () => {
      expect(mixedText("x = 3")).toBe("\\(x = 3\\)");
      expect(mixedText("(x-3)e^{x} = 0")).toBe("\\((x-3)e^{x} = 0\\)");
      expect(mixedText("g has a relative minimum at x = 3")).toBe("g has a relative minimum at x = 3");
      expect(mixedText("so \\(g\\) has a minimum")).toBe("so \\(g\\) has a minimum");
      expect(mixedText("\\sin x + \\cos x")).toBe("\\(\\sin x + \\cos x\\)");
   });
});

describe("the places the transcriber was not sure of", () => {
   it("typesets the delimited mathematics in a note instead of showing its backslashes", () => {
      const readBack = { parts: [{ part_id: "d", lines: [], answer: "" }], unreadable: ["part d, line 2, the \\(H'(t)\\) prime is written small"] };
      const { getByTestId } = render(<ReadBackView readBack={readBack} />);
      const notes = getByTestId("unreadable");

      expect(notes.textContent).not.toContain("\\(");
      expect(notes.querySelector("math")).not.toBeNull();
   });
});
