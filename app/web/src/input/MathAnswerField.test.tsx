import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";

import { act, render, screen } from "@testing-library/react";
import { beforeAll, describe, expect, it, vi } from "vitest";

import { LATEX_INSPECTOR_LABEL, MathAnswerField } from "./MathAnswerField";

/* The MathfieldElement stand-in: MathLive resolves to its SSR stub under vitest, so this serves the
   two formats MathField.tsx reads on input, and a LaTeX string that differs from the MathJSON so
   the inspector can be seen to show the one and not the other. */
class TypedMathField extends HTMLElement {
   getValue(format: string): string {
      const outputs: Record<string, string> = {
         "math-json": JSON.stringify(["Divide", ["Subtract", ["Power", "x", 2], 9], ["Subtract", "x", 3]]),
         latex: "\\frac{x^2-9}{x-3}",
         "spoken-text": "x squared minus 9 over x minus 3"
      };

      return outputs[format];
   }

   type() {
      this.dispatchEvent(new Event("input", { bubbles: true }));
   }
}

beforeAll(() => {
   if (customElements.get("math-field") === undefined) {
      customElements.define("math-field", TypedMathField);
   }
});

function componentSources() {
   const root = join(__dirname, "..");
   const found: Array<{ file: string; text: string }> = [];

   function walk(directory: string) {
      for (const entry of readdirSync(directory)) {
         const path = join(directory, entry);

         if (statSync(path).isDirectory()) {
            walk(path);
            continue;
         }

         const isComponent = entry.endsWith(".tsx") && !entry.includes(".test.");

         if (isComponent) {
            found.push({ file: relative(root, path), text: readFileSync(path, "utf8") });
         }
      }
   }

   walk(root);

   return found;
}

describe("the raw LaTeX inspector", () => {
   it("shows the LaTeX the student typed, and still hands the caller the same LaTeX", () => {
      const onLatexChange = vi.fn();
      const { container } = render(
         <MathAnswerField label="My answer" onChange={vi.fn()} onLatexChange={onLatexChange} onLoadFailure={vi.fn()} />
      );

      act(() => (container.querySelector("math-field") as TypedMathField).type());

      const inspector = screen.getByTestId("latex-inspector");

      expect(inspector.textContent).toBe(`${LATEX_INSPECTOR_LABEL}: \\frac{x^2-9}{x-3}`);
      expect(onLatexChange).toHaveBeenCalledWith("\\frac{x^2-9}{x-3}");
   });

   it("is labelled in its own text and adds no stop to the tab order", () => {
      render(<MathAnswerField label="My answer" initialLatex="x^2" onChange={vi.fn()} onLoadFailure={vi.fn()} />);

      const inspector = screen.getByTestId("latex-inspector");
      const focusable = inspector.querySelectorAll("a, button, input, textarea, select, [tabindex], [contenteditable]");

      expect(inspector.textContent).toBe(`${LATEX_INSPECTOR_LABEL}: x^2`);
      expect(inspector.hasAttribute("tabindex")).toBe(false);
      expect(inspector.tabIndex).toBe(-1);
      expect(focusable.length).toBe(0);
   });

   it("sits under every math answer field a screen renders", () => {
      const bareFields = componentSources().filter(({ file, text }) => {
         const isTheWrapper = file === join("input", "MathAnswerField.tsx");

         return !isTheWrapper && /<MathField\b/.test(text);
      });
      const wrapped = componentSources().filter(({ text }) => /<MathAnswerField\b/.test(text));

      expect(bareFields.map(({ file }) => file)).toEqual([]);
      expect(wrapped.length).toBeGreaterThanOrEqual(6);
   });
});
