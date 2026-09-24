import { describe, it, expect, vi } from "vitest";
import { render, fireEvent } from "@testing-library/react";
import { McqControl } from "./McqControl";
import type { ServedOption } from "../api/types";

function makeOptions(count: number): ServedOption[] {
   const letters = ["A", "B", "C", "D", "E", "F"];
   const options: ServedOption[] = [];

   for (let index = 0; index < count; index += 1) {
      options.push({ id: `opt-${index}`, label: letters[index] });
   }

   return options;
}

describe("McqControl", () => {
   it("renders exactly as many options as the item carries, at four options", () => {
      const options = makeOptions(4);
      const { container } = render(
         <McqControl groupLabel="Choose one" options={options} onSelect={vi.fn()} />
      );

      const radios = container.querySelectorAll('input[type="radio"]');

      expect(radios.length).toBe(options.length);
   });

   it("renders exactly as many options as the item carries, at a different count", () => {
      const options = makeOptions(6);
      const { container } = render(
         <McqControl groupLabel="Choose one" options={options} onSelect={vi.fn()} />
      );

      const radios = container.querySelectorAll('input[type="radio"]');

      expect(radios.length).toBe(options.length);
   });

   it("reports the chosen option id on selection and is operable by keyboard", () => {
      const options = makeOptions(4);
      const onSelect = vi.fn();
      const { container } = render(
         <McqControl groupLabel="Choose one" options={options} onSelect={onSelect} />
      );

      const radios = Array.from(container.querySelectorAll('input[type="radio"]')) as HTMLInputElement[];
      const target = radios[2];

      target.focus();

      expect(document.activeElement).toBe(target);
      expect(target.tabIndex).not.toBe(-1);

      /* A browser turns a Space keypress on a focused radio into a click event; jsdom does
         not perform that conversion itself, so the keydown establishes the keyboard context
         and the click stands in for the activation the browser would dispatch. */
      fireEvent.keyDown(target, { key: " ", code: "Space" });
      fireEvent.click(target);

      expect(onSelect).toHaveBeenCalledWith(options[2].id);
   });

   it("exposes no is_key and no error_path anywhere in the rendered DOM, and no attribute distinguishes one option from another", () => {
      const options = makeOptions(4) as Array<ServedOption & { is_key?: boolean; error_path?: string }>;

      options[1].is_key = true;
      options[2].error_path = "unit-03/errors/e12";

      const { container } = render(
         <McqControl groupLabel="Choose one" options={options} onSelect={vi.fn()} />
      );

      expect(container.innerHTML).not.toMatch(/is_key/);
      expect(container.innerHTML).not.toMatch(/error_path/);

      const legitimatelyVaryingAttributes = new Set(["value", "id", "checked"]);
      const radios = Array.from(container.querySelectorAll('input[type="radio"]')) as HTMLInputElement[];
      const attributePairs = radios.map((radio) =>
         Array.from(radio.attributes)
            .filter((attribute) => !legitimatelyVaryingAttributes.has(attribute.name))
            .map((attribute) => `${attribute.name}=${attribute.value}`)
            .sort()
      );

      const [firstPairs, ...restPairs] = attributePairs;

      for (const pairs of restPairs) {
         expect(pairs).toEqual(firstPairs);
      }
   });

   it("typesets a MathJSON option as math and never prints the raw array", () => {
      const options: ServedOption[] = [
         { id: "A", value: 0 },
         { id: "B", value: ["Add", ["Multiply", -5, ["Sin", "x"]], 3] },
         { id: "C", value: ["Rational", 5, 6] },
         { id: "D", value: 1 }
      ];

      const { container } = render(
         <McqControl groupLabel="Choose one" options={options} onSelect={vi.fn()} />
      );

      expect(container.innerHTML).not.toMatch(/Multiply/);
      expect(container.innerHTML).not.toMatch(/Sin/);
      expect(container.innerHTML).not.toMatch(/Rational/);
      expect(container.querySelectorAll(".katex").length).toBe(options.length);
   });

   it("typesets inline LaTeX in an option label through MathText and never prints its delimiters", () => {
      const options: ServedOption[] = [
         { id: "A", label: "\\(\\frac{1}{2}\\)" },
         { id: "B", label: "3" }
      ];

      const { container } = render(
         <McqControl groupLabel="Choose one" options={options} onSelect={vi.fn()} />
      );

      const labels = container.querySelectorAll("label");

      expect(labels[0].querySelectorAll(".katex").length).toBe(1);
      expect(labels[1].querySelectorAll(".katex").length).toBe(0);
      expect(container.textContent).not.toMatch(/\\\(/);
   });
});
