import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";

import * as ts from "typescript";
import { afterEach, beforeAll, describe, expect, it, vi } from "vitest";
import { act, cleanup, render } from "@testing-library/react";

import type { GradingsPayload, ServedItem } from "../api/types";
import { FigureView } from "../figures/FigureView";
import { GradingView } from "../frq/GradingView";
import { ReadBackView } from "../frq/ReadBack";
import { MathField } from "../input/MathField";
import { McqControl } from "../input/McqControl";
import { Item } from "../session/Item";
import { StepMarks } from "../session/StepMarks";
import { MathText } from "./MathText";
import { MathValue } from "./MathValue";

/* 11's P8 eval eval_screen_reader_math: every math region the client renders reads as structure
   under a screen reader, not glyph soup. A typeset region must carry KaTeX's MathML where
   assistive technology can reach it, keep its visual HTML aria-hidden, and carry no second
   plain-text reading of the same formula. The math field carries MathLive's spoken reading. */

const SOURCE_ROOT = join(__dirname, "..");

const STRUCTURAL_MATHML = "mi, mn, mo, mfrac, msup, msub, msubsup, munderover, munder, msqrt, mrow";

function mathRegions(container: HTMLElement) {
   return Array.from(container.querySelectorAll(".katex"));
}

/* What each region fails on, as sentences, empty when every region reads as structure. */
function regionProblems(container: HTMLElement) {
   const problems: string[] = [];

   for (const region of mathRegions(container)) {
      const mathml = region.querySelector("math");
      const visual = region.querySelector(".katex-html");

      if (mathml === null) {
         problems.push(`${region.textContent}: no MathML`);
         continue;
      }

      if (mathml.closest("[aria-hidden='true']") !== null) {
         problems.push(`${region.textContent}: MathML hidden from assistive technology`);
      }

      if (mathml.querySelector(STRUCTURAL_MATHML) === null) {
         problems.push(`${region.textContent}: MathML without structure`);
      }

      if (visual?.getAttribute("aria-hidden") !== "true") {
         problems.push(`${region.textContent}: visual HTML exposed, read as glyphs`);
      }

      const duplicate = region.parentElement?.parentElement?.querySelector(".visually-hidden");

      if (duplicate) {
         problems.push(`${region.textContent}: a plain-text reading duplicates the MathML`);
      }
   }

   return problems;
}

/* Text a reader meets outside the typeset regions must carry no LaTeX source. */
function rawLatexOutsideRegions(container: HTMLElement) {
   const copy = container.cloneNode(true) as HTMLElement;

   for (const region of Array.from(copy.querySelectorAll(".katex"))) {
      region.remove();
   }

   return (copy.textContent ?? "").match(/\\\(|\\\)|\\[a-z]+\{?/g) ?? [];
}

function expectStructuredMath(container: HTMLElement, minimumRegions: number) {
   expect(mathRegions(container).length).toBeGreaterThanOrEqual(minimumRegions);
   expect(regionProblems(container)).toEqual([]);
   expect(rawLatexOutsideRegions(container)).toEqual([]);
}

const STEM = "Find \\(\\lim_{x \\to 3} \\dfrac{x^2 - 9}{x - 3}\\).";

function servedItem(overrides: Partial<ServedItem>): ServedItem {
   return {
      id: "ITM-1",
      archetype_id: "BC-ARCH-0101",
      variant_id: null,
      snapshot_id: null,
      parameter_draw: null,
      stem: STEM,
      figure_spec: null,
      options: null,
      calculator_status: null,
      representation: null,
      difficulty_settings: null,
      skills: ["BC-SKL-0101"],
      status: "verified",
      stage: "unsupported",
      format: "short_answer",
      is_probe: false,
      served_steps: null,
      self_explanation_prompt: null,
      ...overrides
   };
}

function itemProps(item: ServedItem) {
   return {
      item,
      onAnswerChange: vi.fn(),
      answerUnavailable: false,
      onAnswerUnavailable: vi.fn(),
      selectedOptionId: null,
      onOptionChange: vi.fn(),
      confidence: null,
      onConfidenceChange: vi.fn(),
      selfExplanation: "",
      onSelfExplanationChange: vi.fn(),
      onCommit: vi.fn(),
      awaitingConfidence: false
   };
}

class SpeakingMathField extends HTMLElement {
   getValue(format: string): string {
      const outputs: Record<string, string> = {
         "math-json": JSON.stringify(["Power", "x", 2]),
         latex: "x^2",
         "spoken-text": "x squared"
      };

      return outputs[format];
   }
}

beforeAll(() => {
   if (customElements.get("math-field") === undefined) {
      customElements.define("math-field", SpeakingMathField);
   }
});

afterEach(() => {
   cleanup();
});

describe("eval_screen_reader_math", () => {
   it("MathText and MathValue expose KaTeX's MathML and hide only its visual half", () => {
      const { container } = render(
         <p>
            <MathText text={STEM} /> <MathValue value={["Divide", 1, ["Power", "x", 2]]} />
         </p>
      );

      expectStructuredMath(container, 2);
   });

   it("the item stem, its worked steps and both kinds of option read as structure", () => {
      const mcq = servedItem({
         format: "mcq",
         options: [
            { id: "A", mathjson: ["Multiply", 2, "x"] },
            { id: "B", label: "\\(\\sqrt{x}\\) at the endpoint" },
            { id: "C", value: 6 }
         ]
      });
      const completion = servedItem({
         stage: "completion",
         served_steps: [
            { index: 1, text: "Factor: \\(x^2 - 9 = (x - 3)(x + 3)\\)" },
            { index: 2, text: "Cancel \\(x - 3\\)" }
         ]
      });

      const choice = render(<Item {...itemProps(mcq)} />);

      expectStructuredMath(choice.container, 4);
      cleanup();

      const worked = render(<Item {...itemProps(completion)} />);

      expectStructuredMath(worked.container, 3);
   });

   it("the option labels a radio button is named by include the MathML", () => {
      const { container } = render(
         <McqControl groupLabel="My answer" options={[{ id: "A", mathjson: ["Power", "x", 2] }]} onSelect={vi.fn()} />
      );
      const label = container.querySelector("label")!;

      expectStructuredMath(container, 1);
      expect(label.querySelector("input[type='radio']")).not.toBeNull();
      expect(label.querySelector("math")).not.toBeNull();
   });

   it("feedback step marks typeset the math in each step", () => {
      const { container } = render(
         <StepMarks
            marks={[
               { index: 1, text: "\\(u = x^2\\)", given: true, correct: null },
               { index: 2, text: "\\(f'(x) = 2x \\sin x + x^2 \\cos x\\)", given: false, correct: false }
            ]}
         />
      );

      expectStructuredMath(container, 2);
   });

   it("the read-back and the graded points read the student's math as structure", () => {
      const readBack = render(
         <ReadBackView
            readBack={{
               parts: [
                  {
                     part_id: "a",
                     lines: [{ kind: "math", content: "g'(x) = (x - 3)e^{x}", crossed_out: false, outside_box: false }],
                     answer: "x = 3"
                  }
               ],
               unreadable: []
            }}
         />
      );

      expectStructuredMath(readBack.container, 2);
      cleanup();

      const gradings: GradingsPayload = {
         attempt_id: "ATT-1",
         item_id: "ITM-1",
         grading_state: "graded",
         points: [
            {
               grading_id: "G-1",
               part_id: "a",
               point_id: "P-1",
               point_type_id: "answer",
               point_label: "Answer",
               criterion: "States the critical point",
               decided_by: "grader",
               earned: 1,
               provisional: false,
               rationale: "The answer is stated",
               evidence_quote: "x = 3",
               eligibility_note: null,
               rereads: 0
            }
         ],
         earned: 1,
         decided: 1,
         total: 1,
         provisional: 0,
         worked_solution: [{ part_id: "a", answer_latex: "x = 3", steps: [{ text: "Set the derivative to zero", latex: "g'(x) = 0" }] }],
         probe_scheduled: null
      };
      const graded = render(<GradingView gradings={gradings} onAskForReread={vi.fn()} rereadAskedFor={[]} />);

      expectStructuredMath(graded.container, 3);
   });

   it("a table figure typesets its cells, and a graph is one image named by its plain-sentence alt", () => {
      const table = render(
         <FigureView spec={{ kind: "table", columns: ["\\(x\\)", "\\(f(x)\\)"], rows: [["1", "\\(e^{2}\\)"]], alt: "Values of f." }} />
      );

      expectStructuredMath(table.container, 3);
      cleanup();

      const graph = render(
         <FigureView
            spec={{
               kind: "function_graph",
               domain: [-2, 2],
               range: [-2, 2],
               labels: [{ text: "\\(y = f(x)\\)", anchor: [1, 1], placement: "inside" }],
               alt: "The graph of y = f(x), rising through the origin."
            }}
         />
      );
      const svg = graph.container.querySelector("svg")!;

      expect(svg.getAttribute("role")).toBe("img");
      expect(svg.getAttribute("aria-label")).toBe("The graph of y = f(x), rising through the origin.");
      expect(rawLatexOutsideRegions(graph.container)).toEqual([]);
   });

   it("the math field carries MathLive's spoken reading of what is in it as its description", () => {
      const { container } = render(<MathField label="My answer" onChange={vi.fn()} onLoadFailure={vi.fn()} />);
      const field = container.querySelector("math-field")!;

      act(() => {
         field.dispatchEvent(new Event("input", { bubbles: true }));
      });

      const describedBy = field.getAttribute("aria-describedby");
      const description = describedBy === null ? null : document.getElementById(describedBy);

      expect(field.getAttribute("aria-label")).toBe("My answer");
      expect(description?.textContent).toBe("x squared");
   });

   it("no component hides a math region from assistive technology or typesets outside MathText and MathValue", () => {
      const offenders: string[] = [];

      function componentFiles(directory: string): string[] {
         return readdirSync(directory).flatMap((entry) => {
            const path = join(directory, entry);

            if (statSync(path).isDirectory()) {
               return componentFiles(path);
            }

            return entry.endsWith(".tsx") && !entry.includes(".test.") ? [path] : [];
         });
      }

      const files = componentFiles(SOURCE_ROOT);

      for (const path of files) {
         const name = relative(SOURCE_ROOT, path);
         const text = readFileSync(path, "utf8");
         const source = ts.createSourceFile(name, text, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
         const isMathModule = name.startsWith("math/");

         if (!isMathModule && /renderLatexToMarkup|from "katex"/.test(text)) {
            offenders.push(`${name} typesets math itself`);
         }

         function visit(node: ts.Node) {
            const isElement = ts.isJsxElement(node);
            const opening = isElement ? node.openingElement : null;
            const hidesChildren = opening?.attributes.properties.some(
               (attribute) => ts.isJsxAttribute(attribute) && attribute.name.getText(source) === "aria-hidden"
            );

            if (hidesChildren && /<Math(Text|Value)\b/.test(node.getText(source))) {
               offenders.push(`${name} puts a math region under aria-hidden`);
            }

            ts.forEachChild(node, visit);
         }

         visit(source);
      }

      expect(files.length).toBeGreaterThan(40);
      expect(offenders).toEqual([]);
   });
});
