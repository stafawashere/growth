import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { TutorFigurePath, TutorFigureSpec } from "../api/types";
import { REDUCED_MOTION_QUERY } from "../styles/motion";
import { EVERY_ROLE_FIGURE, SECANT_TO_TANGENT, TABLE_OF_VALUES, TRIANGLE_DIAGRAM, figureCell, figureDot, figurePath } from "./figureFixtures";
import { TutorFigure, parseTutorFigure } from "./TutorFigure";

/* The caps the client re-checks, as docs/agent/drawing-build-plan.md "The render spec contract"
   states them. */
const CONTRACT_PRIMITIVES = 200;

const CONTRACT_POINTS = 4000;

const CONTRACT_STEPS = 6;

function mockReducedMotion(reduce: boolean) {
   const matchMedia = (query: string) =>
      ({
         matches: reduce && query.replace(/\s+/g, " ").trim() === REDUCED_MOTION_QUERY,
         media: query,
         onchange: null,
         addListener: () => undefined,
         removeListener: () => undefined,
         addEventListener: () => undefined,
         removeEventListener: () => undefined,
         dispatchEvent: () => false
      }) as unknown as MediaQueryList;

   vi.stubGlobal("matchMedia", matchMedia);
   window.matchMedia = matchMedia;
}

afterEach(() => {
   cleanup();
   vi.unstubAllGlobals();
});

function drawn(container: HTMLElement, element: string) {
   return Array.from(container.querySelectorAll(`svg [data-element="${element}"]`));
}

function labelTexts(container: HTMLElement) {
   return Array.from(container.querySelectorAll("[data-testid='tutor-figure-label']")).map((label) => label.getAttribute("data-element"));
}

function classesOf(element: Element | null | undefined) {
   return (element?.getAttribute("class") ?? "").split(/\s+/);
}

function stepLine() {
   return screen.getByTestId("tutor-figure-step-line").textContent;
}

function figureWrapper() {
   return screen.getByTestId("tutor-figure");
}

function stepsNamed(count: number) {
   return Array.from({ length: count }, (_, index) => ({ id: `s${index}`, caption: "A step" }));
}

function withPath(points: number) {
   const path = figurePath("curve", "long", "given", Array.from({ length: points }, (_, index) => [index / points, 0] as [number, number]));

   return { ...SECANT_TO_TANGENT, primitives: [path] };
}

describe("TutorFigure reveals its steps", () => {
   it("draws each primitive only once the step that adds it is revealed", () => {
      const { container, rerender } = render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={1} finished={false} />);

      expect(drawn(container, "f").length).toBe(1);
      expect(drawn(container, "P")).toEqual([]);
      expect(drawn(container, "s1")).toEqual([]);
      expect(labelTexts(container)).toEqual(["f"]);

      rerender(<TutorFigure spec={SECANT_TO_TANGENT} revealed={2} finished={false} />);

      expect(drawn(container, "P").length).toBe(1);
      expect(drawn(container, "Q").length).toBe(1);
      expect(drawn(container, "s1").length).toBe(1);
      expect(drawn(container, "t")).toEqual([]);
      expect(labelTexts(container)).toEqual(["f", "P", "Q"]);
   });

   it("draws the frame of a graph at once, even before any step, and no frame for a diagram", () => {
      const { container } = render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={0} finished={false} />);

      expect(container.querySelector("[data-testid='graph-frame']")).not.toBeNull();
      expect(container.querySelectorAll("[data-testid='figure-gridlines'] line").length).toBeGreaterThan(0);
      expect(container.querySelectorAll("text.figure-tick").length).toBeGreaterThan(0);
      expect(container.querySelectorAll("svg [data-element]")).toHaveLength(0);

      cleanup();

      const diagram = render(<TutorFigure spec={TRIANGLE_DIAGRAM} revealed={2} finished />).container;

      expect(diagram.querySelector("[data-testid='graph-frame']")).toBeNull();
      expect(diagram.querySelector("text.figure-tick")).toBeNull();
      expect(drawn(diagram, "ladder").length).toBe(1);
   });

   it("maps world coordinates into the view the server laid out, plot height being the view less its padding", () => {
      const { container } = render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={2} finished />);
      const svg = container.querySelector("svg")!;
      const pointP = drawn(container, "P")[0];
      const plotWidth = 320 - 40;
      const plotHeight = 300 - 40;

      expect(svg.getAttribute("viewBox")).toBe("0 0 320 300");
      expect(Number(pointP.getAttribute("cx"))).toBeCloseTo(20 + (2 / 5) * plotWidth, 1);
      expect(Number(pointP.getAttribute("cy"))).toBeCloseTo(20 + (8 / 10) * plotHeight, 1);
   });
});

describe("TutorFigure styles a mark by its role", () => {
   it("gives each stroke its role, its style and its weight, and a ghost only the ghost style", () => {
      const { container } = render(<TutorFigure spec={EVERY_ROLE_FIGURE} revealed={6} finished />);
      const stroke = (element: string) => drawn(container, element)[0];

      expect(classesOf(stroke("f"))).toEqual(expect.arrayContaining(["tutor-figure-given", "tutor-figure-style-solid", "tutor-figure-weight-regular"]));
      expect(classesOf(stroke("w"))).toEqual(expect.arrayContaining(["tutor-figure-error", "tutor-figure-style-dashed", "tutor-figure-weight-regular"]));
      expect(classesOf(stroke("h"))).toEqual(expect.arrayContaining(["tutor-figure-highlight", "tutor-figure-style-solid", "tutor-figure-weight-bold"]));
      expect(classesOf(stroke("a"))).toEqual(["tutor-figure-stroke", "tutor-figure-ghost"]);
      expect(classesOf(drawn(container, "H")[0])).toEqual(expect.arrayContaining(["tutor-figure-dot", "tutor-figure-highlight"]));
      expect(classesOf(drawn(container, "A")[0])).toEqual(expect.arrayContaining(["tutor-figure-dot", "tutor-figure-ghost", "tutor-figure-dot-open"]));
   });

   it("takes a stroke's dash and weight from the spec, not from its role", () => {
      const dottedThin = figurePath("curve", "g", "given", [[0, 0], [1, 1]], { style: "dotted", weight: "thin" });
      const { container } = render(<TutorFigure spec={{ ...SECANT_TO_TANGENT, primitives: [dottedThin] }} revealed={1} finished />);

      expect(classesOf(drawn(container, "g")[0])).toEqual(expect.arrayContaining(["tutor-figure-given", "tutor-figure-style-dotted", "tutor-figure-weight-thin"]));
   });

   it("lays a highlighter under a highlighted stroke and dot, before every stroke, and none under a ghost", () => {
      const { container } = render(<TutorFigure spec={EVERY_ROLE_FIGURE} revealed={6} finished />);
      const underlays = Array.from(container.querySelectorAll(".tutor-figure-underlays .tutor-figure-highlighter"));
      const firstStroke = container.querySelector(".tutor-figure-marks .tutor-figure-stroke")!;

      expect(underlays.map((underlay) => underlay.tagName.toLowerCase()).sort()).toEqual(["circle", "path"]);
      expect(underlays.every((underlay) => underlay.compareDocumentPosition(firstStroke) & Node.DOCUMENT_POSITION_FOLLOWING)).toBe(true);
      expect(container.querySelectorAll(".tutor-figure-marks .tutor-figure-highlighter")).toHaveLength(0);

      cleanup();

      const faded = figurePath("curve", "k", "highlight", [[0, 0], [1, 1]], { faded_at: "secant" });
      const ghostOnly = render(<TutorFigure spec={{ ...SECANT_TO_TANGENT, primitives: [faded] }} revealed={2} finished />).container;

      expect(ghostOnly.querySelectorAll(".tutor-figure-highlighter")).toHaveLength(0);
   });

   it("fills a region above the axis and one below it in their own tints, under the frame", () => {
      const { container } = render(<TutorFigure spec={EVERY_ROLE_FIGURE} revealed={5} finished />);
      const above = drawn(container, "above")[0];
      const below = drawn(container, "below")[0];
      const frame = container.querySelector("[data-testid='graph-frame']")!;

      expect(classesOf(above)).toEqual(["tutor-figure-fill", "tutor-figure-fill-region"]);
      expect(classesOf(below)).toEqual(["tutor-figure-fill", "tutor-figure-fill-region-below"]);
      expect(above.getAttribute("d")).toMatch(/ Z$/);
      expect(above.compareDocumentPosition(frame) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
   });

   it("gives each figure its own arrowheads, one per role, and points a stroke's ends at its role's", () => {
      const first = render(<TutorFigure spec={EVERY_ROLE_FIGURE} revealed={4} finished />).container;
      const second = render(<TutorFigure spec={EVERY_ROLE_FIGURE} revealed={4} finished />).container;
      const markerIds = (container: HTMLElement) => Array.from(container.querySelectorAll("marker")).map((marker) => marker.id);

      expect(markerIds(first)).toHaveLength(5);
      expect(new Set([...markerIds(first), ...markerIds(second)]).size).toBe(10);

      const markerOf = (url: string | null) => first.querySelector(`marker[id="${url?.replace(/^url\(#|\)$/g, "")}"] path`);
      const [error, highlight, constructed] = ["w", "h", "a"].map((element) => drawn(first, element)[0]);

      expect(error.getAttribute("marker-start")).not.toBeNull();
      expect(error.getAttribute("marker-end")).toBeNull();
      expect(classesOf(markerOf(error.getAttribute("marker-start")))).toContain("tutor-figure-error");
      expect(classesOf(markerOf(highlight.getAttribute("marker-start")))).toContain("tutor-figure-highlight");
      expect(classesOf(markerOf(highlight.getAttribute("marker-end")))).toContain("tutor-figure-highlight");
      expect(constructed.getAttribute("marker-start")).toBeNull();
      expect(classesOf(markerOf(constructed.getAttribute("marker-end")))).toContain("tutor-figure-constructed");
   });

   it("draws nothing it does not need: no arrowheads for a figure without arrows", () => {
      const { container } = render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={4} finished />);

      expect(container.querySelectorAll("marker")).toHaveLength(0);
   });
});

describe("TutorFigure fades and erases", () => {
   it("turns an element into a ghost once the step that fades it is revealed, and removes an erased one", () => {
      const { container, rerender } = render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={2} finished={false} />);

      expect(classesOf(drawn(container, "s1")[0])).toContain("tutor-figure-constructed");
      expect(classesOf(drawn(container, "Q")[0])).toContain("tutor-figure-constructed");
      expect(labelTexts(container)).toContain("Q");

      rerender(<TutorFigure spec={SECANT_TO_TANGENT} revealed={3} finished={false} />);

      expect(classesOf(drawn(container, "s1")[0])).toEqual(["tutor-figure-stroke", "tutor-figure-ghost"]);
      expect(classesOf(drawn(container, "Q")[0])).toContain("tutor-figure-ghost");
      expect(classesOf(drawn(container, "s2")[0])).toContain("tutor-figure-constructed");
      expect(labelTexts(container)).toEqual(["f", "P", "Q2"]);
   });

   it("fades a label into the ghost style with its element", () => {
      const { container } = render(<TutorFigure spec={EVERY_ROLE_FIGURE} revealed={6} finished />);
      const label = container.querySelector("[data-testid='tutor-figure-label'][data-element='A']");

      expect(classesOf(label)).toContain("tutor-figure-ghost");
      expect(classesOf(label)).not.toContain("tutor-figure-constructed");
   });
});

describe("TutorFigure labels", () => {
   it("typesets a label on the tutor renderer in a layer hidden from assistive technology", () => {
      const { container } = render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={1} finished />);
      const layer = screen.getByTestId("tutor-figure-labels");
      const label = within(layer).getAllByTestId("tutor-figure-label")[0];

      expect(layer.getAttribute("aria-hidden")).toBe("true");
      expect(label.querySelector(".katex")).not.toBeNull();
      expect(layer.textContent).not.toMatch(/\\\(/);
      expect(container.querySelector("svg text:not(.figure-tick):not(.figure-axis-title)")).toBeNull();
   });

   it("positions a label in percentages of the view at its anchor plus its offset", () => {
      render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={1} finished />);
      const label = screen.getAllByTestId("tutor-figure-label")[0];
      const anchorX = 20 + (3.5 / 5) * 280 + 6;
      const anchorY = 20 + (2.75 / 10) * 260 - 6;

      expect(parseFloat(label.style.left)).toBeCloseTo((anchorX / 320) * 100, 3);
      expect(label.style.left).toMatch(/%$/);
      expect(parseFloat(label.style.top)).toBeCloseTo((anchorY / 300) * 100, 3);
      expect(label.getAttribute("data-align")).toBe("start");
   });

   it("keeps a label inside the figure by anchoring one that would run off an edge to that edge", () => {
      const nearRight = { type: "label", step: "curve", element: "r", role: "given", at: [3.9, 4], offset: [6, -6], align: "start", text: "a long label here", faded_at: null, erased_at: null };
      const nearLeft = { ...nearRight, element: "l", at: [-1, 4], offset: [-6, -6], align: "end", text: "left" };
      const nearTop = { ...nearRight, element: "t", at: [0, 9], offset: [0, -20], text: "top" };
      render(<TutorFigure spec={{ ...SECANT_TO_TANGENT, primitives: [nearRight, nearLeft, nearTop] }} revealed={1} finished />);
      const [right, left, top] = screen.getAllByTestId("tutor-figure-label");

      expect(right.getAttribute("data-align")).toBe("end");
      expect(parseFloat(right.style.left)).toBe(100);
      expect(left.getAttribute("data-align")).toBe("start");
      expect(parseFloat(left.style.left)).toBe(0);
      expect(parseFloat(top.style.top)).toBeGreaterThan(0);
   });
});

describe("TutorFigure refuses a spec it cannot check", () => {
   it("draws nothing, and does not throw, for a spec over a cap or with anything unreadable", () => {
      const sevenSteps = { ...SECANT_TO_TANGENT, steps: stepsNamed(CONTRACT_STEPS + 1), primitives: [] };
      const tooManyPrimitives = { ...SECANT_TO_TANGENT, primitives: Array.from({ length: CONTRACT_PRIMITIVES + 1 }, (_, index) => figureDot("curve", `d${index}`, "given", [0, 0])) };
      const bad: unknown[] = [
         null,
         "figure",
         sevenSteps,
         { ...SECANT_TO_TANGENT, steps: [] },
         tooManyPrimitives,
         withPath(CONTRACT_POINTS + 1),
         { ...SECANT_TO_TANGENT, kind: "chart" },
         { ...SECANT_TO_TANGENT, window: { x: [4, -1], y: [-1, 9] } },
         { ...SECANT_TO_TANGENT, view: { width: 320, height: 300, padding: 200 } },
         { ...SECANT_TO_TANGENT, primitives: [figureDot("curve", "n", "given", [Number.NaN, 0])] },
         { ...SECANT_TO_TANGENT, primitives: [figureDot("curve", "i", "given", [Number.POSITIVE_INFINITY, 0])] },
         { ...SECANT_TO_TANGENT, primitives: [{ ...figureDot("curve", "s", "given", [0, 0]), at: ["0", 0] }] },
         { ...SECANT_TO_TANGENT, primitives: [figureDot("nowhere", "u", "given", [0, 0])] },
         { ...SECANT_TO_TANGENT, primitives: [figureDot("curve", "u", "given", [0, 0], { faded_at: "later" })] },
         { ...SECANT_TO_TANGENT, primitives: [{ ...figureDot("curve", "c", "given", [0, 0]), role: "colour" }] },
         { ...SECANT_TO_TANGENT, primitives: [{ ...(SECANT_TO_TANGENT.primitives[0] as TutorFigurePath), style: "wavy" }] },
         { ...TABLE_OF_VALUES, primitives: [figureDot("row", "d", "given", [0, 0])] },
         { ...TABLE_OF_VALUES, primitives: [{ ...TABLE_OF_VALUES.primitives[0], row: 3 }] },
         { ...SECANT_TO_TANGENT, primitives: [TABLE_OF_VALUES.primitives[0]] }
      ];

      for (const spec of bad) {
         const { container, unmount } = render(<TutorFigure spec={spec} revealed={1} finished />);

         expect(container.innerHTML, JSON.stringify(spec)?.slice(0, 80)).toBe("");
         expect(parseTutorFigure(spec)).toBeNull();

         unmount();
      }
   });

   it("draws a spec at every cap exactly", () => {
      const sixSteps = { ...SECANT_TO_TANGENT, steps: stepsNamed(CONTRACT_STEPS), primitives: [] };
      const atPrimitiveCap = { ...SECANT_TO_TANGENT, primitives: Array.from({ length: CONTRACT_PRIMITIVES }, (_, index) => figureDot("curve", `d${index}`, "given", [0, 0])) };

      expect(parseTutorFigure(sixSteps)).not.toBeNull();
      expect(parseTutorFigure(atPrimitiveCap)).not.toBeNull();
      expect(parseTutorFigure(withPath(CONTRACT_POINTS))).not.toBeNull();
      expect(parseTutorFigure(TABLE_OF_VALUES)).not.toBeNull();
   });
});

describe("TutorFigure is named, described and stepped from the keyboard", () => {
   it("names the focusable figure and its drawing by the visible title and describes the drawing by the description and the steps", () => {
      render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={4} finished />);
      const group = screen.getByRole("group", { name: "Secant to tangent" });
      const image = screen.getByRole("img", { name: "Secant to tangent" });
      const describedBy = (image.getAttribute("aria-describedby") ?? "").split(" ").map((id) => document.getElementById(id));

      expect(group.getAttribute("tabindex")).toBe("0");
      expect(image.tagName.toLowerCase()).toBe("svg");
      expect(screen.getByText("Secant to tangent").tagName.toLowerCase()).not.toBe("title");
      expect(describedBy[0]?.textContent).toBe(SECANT_TO_TANGENT.description);
      expect(describedBy[0]?.className).toBe("visually-hidden");
      expect(image.contains(describedBy[0]!)).toBe(false);
      expect(describedBy[1]?.tagName.toLowerCase()).toBe("ol");
      expect(describedBy[1]?.textContent).toContain("The tangent at P");
      expect(document.getElementById(group.getAttribute("aria-describedby")!)?.textContent).toBe(SECANT_TO_TANGENT.description);
   });

   it("steps with Left, Right, Home and End while the figure has focus, and with Previous and Next", () => {
      const onStep = vi.fn();
      const { container } = render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={4} finished onStep={onStep} />);

      expect(stepLine()).toBe("Step 4 of 4: The tangent at P");

      fireEvent.keyDown(figureWrapper(), { key: "ArrowLeft" });

      expect(stepLine()).toBe("Step 3 of 4: Q moves closer to P");
      expect(drawn(container, "t")).toEqual([]);
      expect(onStep).toHaveBeenLastCalledWith(2);

      fireEvent.keyDown(figureWrapper(), { key: "Home" });

      expect(stepLine()).toBe("Step 1 of 4: The curve y = x^2");
      expect(drawn(container, "P")).toEqual([]);

      fireEvent.keyDown(figureWrapper(), { key: "ArrowLeft" });

      expect(stepLine()).toBe("Step 1 of 4: The curve y = x^2");

      fireEvent.keyDown(figureWrapper(), { key: "ArrowRight" });

      expect(stepLine()).toBe("Step 2 of 4: A secant through P and Q");

      fireEvent.keyDown(figureWrapper(), { key: "End" });

      expect(stepLine()).toBe("Step 4 of 4: The tangent at P");

      fireEvent.click(screen.getByRole("button", { name: "Previous" }));

      expect(stepLine()).toBe("Step 3 of 4: Q moves closer to P");

      fireEvent.click(screen.getByRole("button", { name: "Show all" }));

      expect(stepLine()).toBe("Step 4 of 4: The tangent at P");
      expect(screen.getByRole("button", { name: "Next" }).hasAttribute("disabled")).toBe(true);

      fireEvent.keyDown(screen.getByRole("button", { name: "Previous" }), { key: "ArrowLeft" });

      expect(stepLine()).toBe("Step 4 of 4: The tangent at P");
   });

   it("marks the current step in the Steps list with aria-current and the word now", () => {
      render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={4} finished />);

      fireEvent.keyDown(figureWrapper(), { key: "ArrowLeft" });

      const items = within(screen.getByTestId("tutor-figure-steps")).getAllByRole("listitem");
      const current = items.filter((item) => item.getAttribute("aria-current") === "step");

      expect(items).toHaveLength(4);
      expect(current).toEqual([items[2]]);
      expect(items[2].textContent).toBe("Q moves closer to Pnow");
      expect(items[3].textContent).toBe("The tangent at P");
   });

   it("opens the Steps disclosure under reduced motion and leaves it closed otherwise", () => {
      mockReducedMotion(true);
      render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={4} finished />);

      expect(screen.getByTestId("tutor-figure-steps").hasAttribute("open")).toBe(true);

      cleanup();
      mockReducedMotion(false);
      render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={4} finished />);

      expect(screen.getByTestId("tutor-figure-steps").hasAttribute("open")).toBe(false);
   });

   it("while the reply streams shows only Show all, which asks the caller to open every step", () => {
      const onShowAll = vi.fn();
      const { rerender } = render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={1} finished={false} onShowAll={onShowAll} />);

      expect(screen.getAllByRole("button").map((button) => button.textContent)).toEqual(["Show all"]);
      expect(screen.queryByTestId("tutor-figure-step-line")).toBeNull();
      expect(screen.queryByTestId("tutor-figure-steps")).toBeNull();

      fireEvent.keyDown(figureWrapper(), { key: "End" });
      fireEvent.click(screen.getByRole("button", { name: "Show all" }));

      expect(onShowAll).toHaveBeenCalledTimes(1);
      expect(drawn(document.body, "t")).toEqual([]);

      rerender(<TutorFigure spec={SECANT_TO_TANGENT} revealed={4} finished={false} onShowAll={onShowAll} />);

      expect(screen.getByRole("button", { name: "Show all" }).hasAttribute("disabled")).toBe(true);
   });

   it("never takes focus on its own when it mounts or a step arrives", () => {
      const { rerender } = render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={1} finished={false} />);

      rerender(<TutorFigure spec={SECANT_TO_TANGENT} revealed={2} finished={false} />);
      rerender(<TutorFigure spec={SECANT_TO_TANGENT} revealed={4} finished />);

      expect(document.activeElement).toBe(document.body);
   });
});

describe("TutorFigure moves only a newly revealed step", () => {
   function stepGroups(container: HTMLElement, step: string) {
      return Array.from(container.querySelectorAll(`svg g[data-step="${step}"]`));
   }

   it("wipes and fades the step just revealed from a marked first frame, and leaves steps already drawn still", async () => {
      const { container, rerender } = render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={1} finished={false} />);

      expect(container.querySelectorAll(".motion-figure-step, .motion-figure-wipe")).toHaveLength(0);
      expect(container.querySelector("clipPath")).toBeNull();

      rerender(<TutorFigure spec={SECANT_TO_TANGENT} revealed={2} finished={false} />);

      const entering = stepGroups(container, "secant");
      const clipRect = container.querySelector("clipPath rect")!;
      const clipped = container.querySelector(".tutor-figure-marks g[data-step='secant'] g[clip-path]")!;
      const secantLabel = container.querySelector("[data-testid='tutor-figure-label'][data-element='P']")!;

      expect(entering.length).toBeGreaterThan(0);
      expect(entering.every((group) => classesOf(group).includes("motion-figure-step"))).toBe(true);
      expect(entering.every((group) => group.getAttribute("data-entering") === "true")).toBe(true);
      expect(classesOf(clipRect)).toEqual(["motion-figure-wipe"]);
      expect(clipRect.getAttribute("data-entering")).toBe("true");
      expect(clipped.getAttribute("clip-path")).toBe(`url(#${clipRect.parentElement!.id})`);
      expect(clipped.querySelector("[data-element='s1']")).not.toBeNull();
      expect(clipped.querySelector("[data-element='P']")).toBeNull();
      expect(classesOf(secantLabel)).toContain("motion-figure-step");
      expect(stepGroups(container, "curve").some((group) => group.hasAttribute("class") || group.hasAttribute("data-entering"))).toBe(false);

      await waitFor(() => expect(container.querySelectorAll("[data-entering]").length).toBe(0));

      expect(stepGroups(container, "secant").every((group) => classesOf(group).includes("motion-figure-step"))).toBe(true);

      rerender(<TutorFigure spec={SECANT_TO_TANGENT} revealed={3} finished={false} />);

      expect(stepGroups(container, "secant").some((group) => group.hasAttribute("class"))).toBe(false);
      expect(stepGroups(container, "closer").every((group) => classesOf(group).includes("motion-figure-step"))).toBe(true);
      expect(container.querySelectorAll("clipPath")).toHaveLength(1);
   });

   it("draws a figure that mounts already built without motion, and moves nothing when stepping back", async () => {
      const { container } = render(<TutorFigure spec={SECANT_TO_TANGENT} revealed={4} finished />);

      expect(container.querySelectorAll(".motion-figure-step, .motion-figure-wipe")).toHaveLength(0);

      fireEvent.keyDown(figureWrapper(), { key: "ArrowLeft" });

      expect(container.querySelectorAll(".motion-figure-step, .motion-figure-wipe")).toHaveLength(0);

      fireEvent.keyDown(figureWrapper(), { key: "ArrowRight" });

      expect(stepGroups(container, "tangent").every((group) => classesOf(group).includes("motion-figure-step"))).toBe(true);

      await act(async () => {
         await new Promise((resolve) => requestAnimationFrame(resolve));
      });
   });
});

describe("TutorFigure tables", () => {
   function cellClass(container: HTMLElement, row: number, column: number) {
      return container.querySelectorAll("tbody tr")[row].querySelectorAll("td")[column].getAttribute("class");
   }

   it("draws the table at once and highlights its cells step by step, typeset on the tutor renderer", () => {
      const { container, rerender } = render(<TutorFigure spec={TABLE_OF_VALUES} revealed={0} finished={false} />);
      const table = screen.getByRole("table", { name: "Values of f" });

      expect(container.querySelectorAll("tbody td")).toHaveLength(9);
      expect(container.querySelectorAll("tbody td[class]")).toHaveLength(0);
      expect(within(table).getAllByRole("columnheader")[1].querySelector(".katex")).not.toBeNull();
      expect(container.querySelector("svg")).toBeNull();

      rerender(<TutorFigure spec={TABLE_OF_VALUES} revealed={1} finished={false} />);

      expect([0, 1, 2].map((column) => cellClass(container, 1, column))).toEqual(Array(3).fill("tutor-figure-cell-highlight"));
      expect(cellClass(container, 0, 0)).toBeNull();

      rerender(<TutorFigure spec={TABLE_OF_VALUES} revealed={2} finished={false} />);

      expect(cellClass(container, 2, 2)).toBe("tutor-figure-cell-error");

      rerender(<TutorFigure spec={TABLE_OF_VALUES} revealed={3} finished />);

      expect(cellClass(container, 1, 0)).toBe("tutor-figure-cell-ghost");
      expect(cellClass(container, 1, 1)).toBe("tutor-figure-cell-highlight");
      expect(cellClass(container, 0, 1)).toBe("tutor-figure-cell-highlight");
      expect(cellClass(container, 2, 2)).toBe("tutor-figure-cell-error");
      expect(stepLine()).toBe("Step 3 of 3: The values of f");
   });
});

describe("TutorFigure labelled table cells", () => {
   const labelled = {
      ...TABLE_OF_VALUES,
      primitives: [figureCell("row", "r1", "highlight", 1, null, { text: "\\(x = 1\\) here" }), figureCell("cell", "c22", "error", 2, 2, { text: "read as 3" })]
   };

   function noteIn(container: HTMLElement, row: number, column: number) {
      return container.querySelectorAll("tbody tr")[row].querySelectorAll("td")[column].querySelector("[data-testid='tutor-figure-cell-note']");
   }

   it("writes a highlight's words once, in the first cell it covers, typeset, once its step is revealed", () => {
      const { container, rerender } = render(<TutorFigure spec={labelled} revealed={0} finished={false} />);

      expect(container.querySelectorAll("[data-testid='tutor-figure-cell-note']")).toHaveLength(0);

      rerender(<TutorFigure spec={labelled} revealed={1} finished={false} />);

      expect(container.querySelectorAll("[data-testid='tutor-figure-cell-note']")).toHaveLength(1);
      expect(noteIn(container, 1, 0)?.querySelector(".katex")).not.toBeNull();
      expect(noteIn(container, 1, 0)?.closest("td")?.getAttribute("class")).toBe("tutor-figure-cell-highlight");

      rerender(<TutorFigure spec={labelled} revealed={2} finished />);

      expect(noteIn(container, 2, 2)?.textContent).toBe("read as 3");
      expect(noteIn(container, 2, 2)?.closest("td")?.textContent).toBe("3read as 3");
   });

   it("refuses a cell whose text is not a string", () => {
      const numbered = { ...TABLE_OF_VALUES, primitives: [{ ...figureCell("row", "r1", "highlight", 1, null), text: 5 }] };

      expect(parseTutorFigure(numbered)).toBeNull();
   });
});

describe("TutorFigure keeps tick numbers out from under its labels", () => {
   /* Window x from -1 to 9 and y from -2 to 24, as the live Riemann figure had: the x axis sits at
      260 in view units, and the number 2 sits under x = 104, in the box from 260 to 274. A width
      label sits under x = 2, its baseline 34 units below the axis at 294. */
   const widths: TutorFigureSpec = {
      ...SECANT_TO_TANGENT,
      window: { x: [-1, 9], y: [-2, 24] },
      steps: [{ id: "curve", caption: "The widths" }],
      primitives: [{ type: "label", step: "curve", element: "w", role: "given", at: [2, 0], offset: [0, 34], align: "middle", text: "\\(4\\)", faded_at: null, erased_at: null }]
   };

   function xTicks(container: HTMLElement) {
      return Array.from(container.querySelectorAll("text.figure-tick[data-axis='x']")).map((tick) => tick.textContent);
   }

   function drawAt(element: Element | null, rect: { left: number; top: number; width: number; height: number }) {
      Object.defineProperty(element, "getBoundingClientRect", {
         configurable: true,
         value: () => ({ ...rect, right: rect.left + rect.width, bottom: rect.top + rect.height, x: rect.left, y: rect.top, toJSON: () => ({}) })
      });
   }

   it("leaves out the number a label covers once the figure is drawn smaller than its view, where the label is larger in view units", () => {
      const { container, rerender } = render(<TutorFigure spec={widths} revealed={1} finished />);

      drawAt(container.querySelector(".tutor-figure-canvas"), { left: 0, top: 0, width: 320, height: 300 });
      rerender(<TutorFigure spec={widths} revealed={1} finished />);

      expect(xTicks(container)).toContain("2");

      drawAt(container.querySelector(".tutor-figure-canvas"), { left: 0, top: 0, width: 160, height: 150 });
      rerender(<TutorFigure spec={widths} revealed={1} finished />);

      expect(xTicks(container)).not.toContain("2");
      expect(xTicks(container)).toContain("1");
      expect(xTicks(container)).toContain("3");
   });

   it("leaves out the number under a label as the label is actually drawn, not only as estimated", () => {
      const { container, rerender } = render(<TutorFigure spec={widths} revealed={1} finished />);

      drawAt(container.querySelector(".tutor-figure-canvas"), { left: 0, top: 0, width: 320, height: 300 });
      rerender(<TutorFigure spec={widths} revealed={1} finished />);

      expect(xTicks(container)).toContain("2");

      drawAt(container.querySelector(".tutor-figure-label-text"), { left: 96, top: 262, width: 16, height: 32 });
      rerender(<TutorFigure spec={widths} revealed={1} finished />);

      expect(xTicks(container)).not.toContain("2");
      expect(xTicks(container)).toContain("3");
   });
});
