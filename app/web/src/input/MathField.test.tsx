import { describe, it, expect, vi, beforeAll } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MathField } from "./MathField";
import type { MathFieldProps } from "./MathField";

/* MathLive resolves to its SSR stub under Vite's "node" export condition, which is what
   vitest runs under even with environment: jsdom, so the real MathfieldElement never
   registers here. This stub stands in for it: it implements only the sliver of the real
   MathfieldElement API that MathField.tsx touches, getValue(format) and the "input" event,
   so the test exercises the same seam the component uses against the real element. */
class StubMathField extends HTMLElement {
   private currentValue = "[]";

   getValue(format: string): string {
      if (format !== "math-json") {
         throw new Error("stub only serves math-json in this test");
      }

      return this.currentValue;
   }

   setStubValue(mathJsonString: string) {
      this.currentValue = mathJsonString;
      this.dispatchEvent(new Event("input", { bubbles: true }));
   }
}

beforeAll(() => {
   if (customElements.get("math-field") === undefined) {
      customElements.define("math-field", StubMathField);
   }
});

describe("MathField", () => {
   it("hands out MathJSON rather than a LaTeX string on input", () => {
      const onChange = vi.fn();
      const { container } = render(<MathField label="Answer" onChange={onChange} onLoadFailure={vi.fn()} />);
      const field = container.querySelector("math-field") as StubMathField;

      field.setStubValue(JSON.stringify(["Add", 1, 2]));

      expect(onChange).toHaveBeenCalledTimes(1);

      const received = onChange.mock.calls[0][0];

      expect(typeof received).not.toBe("string");
      expect(received).toEqual(["Add", 1, 2]);
   });

   it("renders an accessible labelled field", () => {
      render(<MathField label="Enter your answer" onChange={vi.fn()} onLoadFailure={vi.fn()} />);

      const field = screen.getByLabelText("Enter your answer");

      expect(field.tagName.toLowerCase()).toBe("math-field");
   });
});

describe("MathField when the MathLive chunk never loads", () => {
   it("refuses to render without a handler for the load failure", () => {
      const withoutHandler = { label: "Answer", onChange: vi.fn() } as unknown as MathFieldProps;

      expect(() => render(<MathField {...withoutHandler} />)).toThrow(/onLoadFailure/);
   });

   it("surfaces the failure to the student and to the caller", async () => {
      vi.resetModules();
      vi.doMock("mathlive", () => {
         throw new Error("chunk load failed");
      });

      const onLoadFailure = vi.fn();

      render(<MathField label="Answer" onChange={vi.fn()} onLoadFailure={onLoadFailure} />);

      await waitFor(() => {
         expect(onLoadFailure).toHaveBeenCalledTimes(1);
      });

      const alert = screen.getByRole("alert");

      expect(alert.textContent).toMatch(/did not load/);

      vi.doUnmock("mathlive");
      vi.resetModules();
   });
});
