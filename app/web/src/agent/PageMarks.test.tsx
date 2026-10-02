import { cleanup, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { TutorMark, TutorMarksSpec } from "../api/types";
import { REDUCED_MOTION_QUERY } from "../styles/motion";
import { declared, readingUnchangedDom } from "../testing/cascade";
import { ITEM_MARKS, markTarget, pageMark } from "./figureFixtures";
import { PageMarks, parseTutorMarks } from "./PageMarks";

/* The contract's caps: at most 12 marks and 6 steps. */
const CONTRACT_MARKS = 12;

/* jsdom lays nothing out, so every anchor is given the rectangle a browser would measure, and a
   text range reports one line box per 40 characters of the phrase, 8 pixels a character, starting
   where the phrase starts in its text. */

interface Rect {
   left: number;
   top: number;
   width: number;
   height: number;
}

function domRect({ left, top, width, height }: Rect) {
   return { left, top, width, height, right: left + width, bottom: top + height, x: left, y: top, toJSON: () => ({}) } as DOMRect;
}

function placeAt(element: Element | null, rect: Rect) {
   Object.defineProperty(element, "getBoundingClientRect", { configurable: true, value: () => domRect(rect) });
}

const STEM_BOX: Rect = { left: 100, top: 200, width: 400, height: 40 };

const LINE_HEIGHT = 20;

const CHARACTER_WIDTH = 8;

const CHARACTERS_PER_LINE = 40;

function fakeRangeRects(this: Range) {
   const phrase = this.toString();
   const startsAt = this.startContainer.textContent?.indexOf(phrase) ?? 0;
   const lines: DOMRect[] = [];

   for (let taken = 0; taken < phrase.length; taken += CHARACTERS_PER_LINE) {
      const length = Math.min(CHARACTERS_PER_LINE, phrase.length - taken);
      const line = lines.length;
      const left = line === 0 ? STEM_BOX.left + startsAt * CHARACTER_WIDTH : STEM_BOX.left;

      lines.push(domRect({ left, top: STEM_BOX.top + line * LINE_HEIGHT, width: length * CHARACTER_WIDTH, height: LINE_HEIGHT }));
   }

   return lines as unknown as DOMRectList;
}

const STEM_TEXT = "Find the slope of the tangent line to the curve y equals x squared where it passes through the point P.";

/* The item figure: window x from -2 to 2 and y from -1 to 3, its plot from (20, 20) to (460, 460)
   in view units, its box at (100, 400) and half size. The screen matrix puts it at (120, 410)
   instead, so a mapping that ignores the matrix is caught. */
function Page() {
   return (
      <main id="main">
         <p data-agent-anchor="stem">{STEM_TEXT}</p>
         <svg data-agent-anchor="item_figure" data-agent-window="-2 2 -1 3" data-agent-plot="20 20 460 460" viewBox="0 0 480 480" />
         <table data-agent-anchor="item_table">
            <tbody>
               <tr>
                  <td>0</td>
                  <td>1</td>
               </tr>
               <tr>
                  <td>1</td>
                  <td>3</td>
               </tr>
            </tbody>
         </table>
      </main>
   );
}

function layOutPage(options: { screenMatrix?: boolean } = {}) {
   placeAt(document.querySelector("[data-agent-anchor='stem']"), STEM_BOX);

   const graph = document.querySelector("[data-agent-anchor='item_figure']")!;

   placeAt(graph, { left: 100, top: 400, width: 240, height: 240 });

   if (options.screenMatrix !== false) {
      Object.defineProperty(graph, "getScreenCTM", { configurable: true, value: () => ({ a: 0.5, b: 0, c: 0, d: 0.5, e: 120, f: 410 }) });
   }

   const rows = document.querySelectorAll("[data-agent-anchor='item_table'] tbody tr");

   placeAt(rows[0], { left: 100, top: 700, width: 200, height: 30 });
   placeAt(rows[1], { left: 100, top: 730, width: 200, height: 30 });
}

function marksOf(...marks: TutorMark[]): TutorMarksSpec {
   return { id: "marks", description: "Marks.", steps: [{ id: "one", caption: "One" }, { id: "two", caption: "Two" }], marks };
}

function drawn(element: string) {
   return Array.from(document.querySelectorAll(`[data-testid='page-marks'] [data-mark='${element}'], [data-testid='page-marks-highlights'] [data-mark='${element}']`));
}

function numbersIn(d: string | null) {
   return (d ?? "").match(/-?\d+(\.\d+)?/g)!.map(Number);
}

let originalRangeRects: unknown;

beforeEach(() => {
   originalRangeRects = (Range.prototype as { getClientRects?: unknown }).getClientRects;
   Object.defineProperty(Range.prototype, "getClientRects", { configurable: true, writable: true, value: fakeRangeRects });
});

afterEach(() => {
   cleanup();
   Object.defineProperty(Range.prototype, "getClientRects", { configurable: true, writable: true, value: originalRangeRects });
   vi.unstubAllGlobals();
});

function renderMarks(spec: TutorMarksSpec, revealed: number, options: { screenMatrix?: boolean } = {}) {
   const page = render(<Page />);

   layOutPage(options);

   const marks = render(<PageMarks spec={spec} revealed={revealed} />);

   return { page, marks };
}

describe("PageMarks places each mark over the element it names", () => {
   it("underlines a quoted phrase of the stem under each of its line boxes", () => {
      renderMarks(marksOf(pageMark("one", "u", "constructed", "underline", { target: markTarget("stem", { quote: "the tangent line to the curve y equals x squared" }) })), 1);

      const lines = drawn("u");
      const startsAt = STEM_TEXT.indexOf("the tangent line");

      expect(lines).toHaveLength(2);
      expect(numbersIn(lines[0].getAttribute("d"))).toEqual([STEM_BOX.left + startsAt * CHARACTER_WIDTH, 222, STEM_BOX.left + startsAt * CHARACTER_WIDTH + 320, 222]);
      expect(numbersIn(lines[1].getAttribute("d"))).toEqual([STEM_BOX.left, 242, STEM_BOX.left + 8 * 8, 242]);
   });

   it("strikes through the middle of a quoted phrase and bands a highlighted one", () => {
      renderMarks(
         marksOf(
            pageMark("one", "s", "error", "strike", { target: markTarget("stem", { quote: "the slope" }) }),
            pageMark("one", "h", "highlight", "highlight", { target: markTarget("stem", { quote: "the point P." }) })
         ),
         1
      );

      const strike = drawn("s")[0];
      const band = drawn("h")[0];
      const bandStart = STEM_BOX.left + STEM_TEXT.indexOf("the point P.") * CHARACTER_WIDTH;

      expect(numbersIn(strike.getAttribute("d"))[1]).toBe(STEM_BOX.top + LINE_HEIGHT / 2);
      expect(strike.getAttribute("class")).toContain("tutor-figure-error");
      expect(band.closest("[data-testid='page-marks-highlights']")).not.toBeNull();
      expect(band.getAttribute("class")).toBe("tutor-figure-highlighter");
      expect(numbersIn(band.getAttribute("d")).slice(0, 2)).toEqual([bandStart - 2, STEM_BOX.top]);
   });

   it("maps a point of the item's graph through its window, its plot box and the SVG's screen matrix", () => {
      renderMarks(marksOf(pageMark("one", "p", "constructed", "point", { at: [1, 1] })), 1);

      const dot = drawn("p")[0];
      const viewX = 20 + (3 / 4) * 440;
      const viewY = 20 + (2 / 4) * 440;

      expect(Number(dot.getAttribute("cx"))).toBe(120 + viewX / 2);
      expect(Number(dot.getAttribute("cy"))).toBe(410 + viewY / 2);
   });

   it("maps a graph point through the SVG's box and view box where there is no screen matrix", () => {
      renderMarks(marksOf(pageMark("one", "p", "constructed", "point", { at: [-2, 3] })), 1, { screenMatrix: false });

      const dot = drawn("p")[0];

      expect(Number(dot.getAttribute("cx"))).toBe(100 + 20 / 2);
      expect(Number(dot.getAttribute("cy"))).toBe(400 + 20 / 2);
   });

   it("draws a construction on the item's graph between its two mapped points", () => {
      renderMarks(marksOf(pageMark("one", "t", "highlight", "line", { points: [[-2, -1], [2, 3]] })), 1);

      const line = drawn("t").find((element) => element.closest("[data-testid='page-marks']") !== null)!;

      expect(numbersIn(line.getAttribute("d"))).toEqual([130, 640, 350, 420]);
   });

   it("bands the table row a mark names, using the anchor's body rows in order", () => {
      renderMarks(marksOf(pageMark("one", "r", "highlight", "highlight", { target: markTarget("item_table", { row: 1 }) })), 1);

      expect(numbersIn(drawn("r")[0].getAttribute("d"))).toEqual([98, 730, 302, 730, 302, 760, 98, 760]);
   });

   it("draws an arrow from the edge of one target to a point on another, with its arrowhead", () => {
      renderMarks(marksOf(pageMark("one", "a", "constructed", "arrow", { from: markTarget("stem"), to: markTarget("item_figure", { at: [1, 1] }) })), 1);

      const arrow = drawn("a")[0];
      const [startX, startY, endX, endY] = numbersIn(arrow.getAttribute("d"));
      const pointX = 120 + (20 + (3 / 4) * 440) / 2;
      const pointY = 410 + (20 + (2 / 4) * 440) / 2;

      expect(startY).toBeGreaterThan(STEM_BOX.top + STEM_BOX.height);
      expect(startY).toBeLessThan(STEM_BOX.top + STEM_BOX.height + 5);
      expect(Math.hypot(endX - pointX, endY - pointY)).toBeCloseTo(4, 1);
      expect(startX).toBeGreaterThan(STEM_BOX.left);
      expect(arrow.getAttribute("marker-end")).toMatch(/^url\(#.+-arrow-constructed\)$/);
      expect(document.querySelector(`marker[id="${arrow.getAttribute("marker-end")!.slice(5, -1)}"]`)).not.toBeNull();
   });

   it("rings a whole anchor and a graph point, and brackets an anchor in the margin", () => {
      renderMarks(
         marksOf(
            pageMark("one", "whole", "constructed", "ring", { target: markTarget("stem") }),
            pageMark("one", "at", "constructed", "ring", { target: markTarget("item_figure", { at: [1, 1] }) }),
            pageMark("one", "b", "given", "bracket", { target: markTarget("stem") })
         ),
         1
      );

      const whole = numbersIn(drawn("whole")[0].getAttribute("d"));
      const bracket = numbersIn(drawn("b")[0].getAttribute("d"));

      expect(whole.slice(0, 2)).toEqual([STEM_BOX.left - 6, STEM_BOX.top + 20]);
      expect(whole.slice(2, 4)).toEqual([206, 26]);
      expect(numbersIn(drawn("at")[0].getAttribute("d")).slice(2, 4)).toEqual([10, 10]);
      expect(bracket).toEqual([98, 200, 92, 200, 92, 240, 98, 240]);
   });

   it("puts a note beside its target on the side named, kept inside the width of the page", () => {
      const noteSize = { width: 120, height: 24 };
      const measureNote = vi.spyOn(HTMLDivElement.prototype, "getBoundingClientRect").mockImplementation(function (this: HTMLDivElement) {
         return this.classList.contains("page-marks-note") ? domRect({ left: 0, top: 0, ...noteSize }) : domRect({ left: 0, top: 0, width: 0, height: 0 });
      });

      renderMarks(
         marksOf(
            pageMark("one", "right", "given", "note", { target: markTarget("stem"), text: "\\(x = 1\\) here", side: "right" }),
            pageMark("one", "above", "error", "note", { target: markTarget("stem"), text: "this step", side: "above" })
         ),
         1
      );

      const [right, above] = screen.getAllByTestId("page-mark-note");
      const rightmost = window.innerWidth - noteSize.width - 8;

      expect(parseFloat(right.style.left)).toBe(Math.min(STEM_BOX.left + STEM_BOX.width + 8, rightmost));
      expect(parseFloat(right.style.top)).toBe(STEM_BOX.top + 20 - 12);
      expect(right.querySelector(".katex")).not.toBeNull();
      expect(right.className).toContain("tutor-figure-given");
      expect(parseFloat(above.style.left)).toBe(STEM_BOX.left + 200 - 60);
      expect(parseFloat(above.style.top)).toBe(STEM_BOX.top - 8 - 24);

      measureNote.mockRestore();
   });

   it("keeps a note that would run off the right edge of the page inside it", () => {
      vi.spyOn(HTMLDivElement.prototype, "getBoundingClientRect").mockImplementation(function (this: HTMLDivElement) {
         return domRect({ left: 0, top: 0, width: this.classList.contains("page-marks-note") ? 600 : 0, height: 20 });
      });

      renderMarks(marksOf(pageMark("one", "n", "given", "note", { target: markTarget("stem"), text: "a long note beside the stem", side: "right" })), 1);

      expect(parseFloat(screen.getByTestId("page-mark-note").style.left)).toBe(window.innerWidth - 600 - 8);

      vi.restoreAllMocks();
   });

   it("leaves out, without complaint, a mark whose anchor or phrase is not on the page, and draws the rest", () => {
      renderMarks(
         marksOf(
            pageMark("one", "gone", "constructed", "ring", { target: markTarget("solution_step_9") }),
            pageMark("one", "misquoted", "constructed", "underline", { target: markTarget("stem", { quote: "a phrase the stem never says" }) }),
            pageMark("one", "noRow", "highlight", "highlight", { target: markTarget("item_table", { row: 7 }) }),
            pageMark("one", "kept", "constructed", "ring", { target: markTarget("stem") })
         ),
         1
      );

      expect(drawn("gone")).toHaveLength(0);
      expect(drawn("misquoted")).toHaveLength(0);
      expect(drawn("noRow")).toHaveLength(0);
      expect(drawn("kept")).toHaveLength(1);
   });
});

describe("PageMarks reveals its steps", () => {
   it("draws only the steps revealed, and fades a mark once a later step fades it", () => {
      const spec = marksOf(
         pageMark("one", "first", "constructed", "ring", { target: markTarget("stem"), faded_at: "two" }),
         pageMark("two", "second", "constructed", "underline", { target: markTarget("stem") })
      );
      const { marks } = renderMarks(spec, 1);

      expect(drawn("first")).toHaveLength(1);
      expect(drawn("second")).toHaveLength(0);

      marks.rerender(<PageMarks spec={spec} revealed={2} />);

      expect(drawn("second")).toHaveLength(1);
      expect(drawn("first")[0].getAttribute("class")).toBe("tutor-figure-stroke tutor-figure-ghost");
   });

   it("wipes the strokes and fades the notes of the step just revealed, from a marked first frame, and moves nothing already drawn", async () => {
      const spec = marksOf(
         pageMark("one", "first", "constructed", "ring", { target: markTarget("stem") }),
         pageMark("two", "second", "constructed", "underline", { target: markTarget("stem") }),
         pageMark("two", "note", "given", "note", { target: markTarget("stem"), text: "here" })
      );
      const { marks } = renderMarks(spec, 1);

      expect(document.querySelectorAll(".motion-figure-step, .motion-figure-wipe")).toHaveLength(0);

      marks.rerender(<PageMarks spec={spec} revealed={2} />);

      const secondGroup = drawn("second")[0].closest("g[data-step-index]")!;
      const firstGroup = drawn("first")[0].closest("g[data-step-index]")!;
      const wipe = document.querySelector("[data-testid='page-marks'] clipPath rect")!;

      expect(secondGroup.getAttribute("class")).toBe("motion-figure-step");
      expect(secondGroup.getAttribute("data-entering")).toBe("true");
      expect(wipe.getAttribute("class")).toBe("motion-figure-wipe");
      expect(drawn("second")[0].closest("g[clip-path]")?.getAttribute("clip-path")).toBe(`url(#${wipe.parentElement!.id})`);
      expect(screen.getByTestId("page-mark-note").className).toContain("motion-figure-step");
      expect(firstGroup.hasAttribute("class")).toBe(false);

      await waitFor(() => expect(document.querySelectorAll("[data-entering]").length).toBe(0));
   });

   it("draws every step it mounts with finished and still, as when the student comes back to a screen", () => {
      renderMarks(ITEM_MARKS, ITEM_MARKS.steps.length);

      expect(drawn("u").length).toBeGreaterThan(0);
      expect(drawn("r").length).toBeGreaterThan(0);
      expect(document.querySelectorAll(".motion-figure-step, .motion-figure-wipe, clipPath")).toHaveLength(0);
   });

   it("keeps the fade under reduced motion, where the stylesheet takes the wipe's movement away", () => {
      const matchMedia = (query: string) => ({ matches: query === REDUCED_MOTION_QUERY, media: query, addEventListener: () => undefined, removeEventListener: () => undefined }) as unknown as MediaQueryList;

      vi.stubGlobal("matchMedia", matchMedia);

      const spec = marksOf(pageMark("one", "first", "constructed", "ring", { target: markTarget("stem") }), pageMark("two", "second", "constructed", "ring", { target: markTarget("stem") }));
      const { marks } = renderMarks(spec, 1);

      marks.rerender(<PageMarks spec={spec} revealed={2} />);

      expect(drawn("second")[0].closest("g[data-step-index]")?.getAttribute("class")).toBe("motion-figure-step");
   });
});

describe("PageMarks never gets in the way", () => {
   it("takes no pointer events, is hidden from assistive technology and holds nothing that takes focus", () => {
      renderMarks(ITEM_MARKS, ITEM_MARKS.steps.length);

      const layers = [screen.getByTestId("page-marks"), screen.getByTestId("page-marks-highlights")];

      for (const layer of layers) {
         expect(layer.getAttribute("aria-hidden")).toBe("true");
         expect(readingUnchangedDom(() => declared(layer, "pointer-events"))).toBe("none");
         expect(readingUnchangedDom(() => declared(layer, "position"))).toBe("fixed");
         expect(layer.querySelectorAll("a, button, input, [tabindex]")).toHaveLength(0);
      }
   });

   it("covers the viewport, and stays under the top bar by clipping itself below its measured bottom edge", () => {
      const header = document.createElement("header");

      header.className = "app-header";
      document.body.prepend(header);
      placeAt(header, { left: 0, top: 0, width: 1024, height: 56 });

      renderMarks(ITEM_MARKS, 1);

      expect(screen.getByTestId("page-marks").style.getPropertyValue("clip-path")).toBe("inset(56px 0 0px 0)");

      for (const layer of [screen.getByTestId("page-marks"), screen.getByTestId("page-marks-highlights")]) {
         const drawing = layer.querySelector("svg")!;

         expect([drawing.style.width, drawing.style.height]).toEqual([`${window.innerWidth}px`, `${window.innerHeight}px`]);
      }

      header.remove();
   });
});

describe("parseTutorMarks", () => {
   it("reads the contract's marks and refuses a spec it cannot check", () => {
      const ringsOnTheStem = (count: number) => Array.from({ length: count }, (_, index) => pageMark("phrase", `m${index}`, "given", "ring", { target: markTarget("stem") }));
      const tooMany = { ...ITEM_MARKS, marks: ringsOnTheStem(CONTRACT_MARKS + 1) };
      const bad: unknown[] = [
         null,
         { ...ITEM_MARKS, steps: [] },
         tooMany,
         { ...ITEM_MARKS, marks: [pageMark("nowhere", "m", "given", "ring", { target: markTarget("stem") })] },
         { ...ITEM_MARKS, marks: [pageMark("phrase", "m", "given", "ring", { target: markTarget("stem [x]") })] },
         { ...ITEM_MARKS, marks: [pageMark("phrase", "m", "given", "ring")] },
         { ...ITEM_MARKS, marks: [pageMark("phrase", "m", "given", "note", { target: markTarget("stem") })] },
         { ...ITEM_MARKS, marks: [pageMark("phrase", "m", "given", "point", { at: [Number.NaN, 0] })] },
         { ...ITEM_MARKS, marks: [pageMark("phrase", "m", "given", "segment", { points: null })] },
         { ...ITEM_MARKS, marks: [{ ...pageMark("phrase", "m", "given", "ring", { target: markTarget("stem") }), kind: "circle" }] }
      ];

      expect(parseTutorMarks(ITEM_MARKS)).not.toBeNull();
      expect(parseTutorMarks({ ...ITEM_MARKS, marks: ringsOnTheStem(CONTRACT_MARKS) })).not.toBeNull();

      for (const spec of bad) {
         expect(parseTutorMarks(spec), JSON.stringify(spec)?.slice(0, 80)).toBeNull();
      }
   });
});
