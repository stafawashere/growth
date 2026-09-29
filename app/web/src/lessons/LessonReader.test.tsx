import { act, cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest";

import { readFileSync } from "node:fs";
import { resolve } from "node:path";

import type { LessonCheckVerdict, LessonPromptVerdict } from "../api/types";
import {
   activate,
   defineKeyboardMathField,
   pointerEvents,
   press,
   startRecordingPointer,
   stopRecordingPointer,
   tabTo
} from "../testing/keyboard";
import { ERROR_ID, FADED_EXAMPLE_ID, LESSON, PREDICTION_ID, planFor } from "./fixtures";
import { LessonReader, type LessonReaderProps } from "./LessonReader";

/* The reader of plan 15 UI and the framework contract, driven the way
   session/keyboardOnlySession.test.tsx drives a session: no pointer, Tab and Enter, Space and the
   arrow keys only. */

const EVERY_SECTION = [
   "LSN-CON-02013#s1",
   "LSN-CON-02013#s2",
   "LSN-CON-02013#s3",
   "LSN-CON-02013#s5",
   "LSN-CON-02013#s7",
   "LSN-CON-02013#err-BC-ERR-02020",
   "LSN-CON-02013#prq-BC-PRQ-00001",
   "LSN-CON-02013#r-figure",
   "LSN-CON-02013#r-table",
   "LSN-CON-02013#r-motion",
   "LSN-CON-02013#r-interactive",
   "LSN-CON-02013#r-model",
   "LSN-CON-02013#r-unknown"
];

const CHECKS = ["LSN-CON-02013#chk-1", "LSN-CON-02013#chk-3"];

const PRAISE = /great|well done|nice|awesome|excellent|perfect|oops|good job|score|percent|%/i;

function props(overrides: Partial<LessonReaderProps> = {}): LessonReaderProps {
   return {
      lesson: LESSON,
      plan: planFor(EVERY_SECTION, CHECKS),
      band: "low",
      context: "session",
      conceptName: "the product rule",
      onComplete: vi.fn(),
      onSkip: vi.fn(),
      onSectionViewed: vi.fn(),
      onCheckAnswer: vi.fn().mockResolvedValue({ correct: true, error_id: null, anchor: null, explanation_anchor: null }),
      onPromptAnswer: vi.fn().mockImplementation(async (sectionId: string) => promptVerdict(sectionId, false)),
      ...overrides
   };
}

function promptVerdict(sectionId: string, correct: boolean, resolution: string | null = null): LessonPromptVerdict {
   const kind = sectionId === PREDICTION_ID ? "prediction" : sectionId === ERROR_ID ? "fix" : "fade";

   return { correct, section_id: sectionId, kind, resolution };
}

function currentScreen() {
   return screen.getByTestId("lesson-screen");
}

async function settle() {
   await act(async () => {
      await Promise.resolve();
   });
}

/* Works the current screen with the keyboard alone: reveals every step, steps a motion block,
   moves a control, runs a model, answers a check. */
async function workScreen() {
   const kind = currentScreen().getAttribute("data-screen-kind");

   while (screen.queryByTestId("lesson-next-step") !== null) {
      activate(screen.getByTestId("lesson-next-step"));
   }

   const stepper = screen.queryByTestId("frame-stepper");

   if (stepper !== null) {
      tabTo(stepper);
      press("ArrowRight");
   }

   const control = screen.queryByTestId("figure-control");

   if (control !== null) {
      tabTo(control);
      press("ArrowRight");
   }

   const run = screen.queryByTestId("model-run") as HTMLButtonElement | null;

   if (run !== null && !run.disabled) {
      activate(run);
   }

   if (kind === "check") {
      const field = document.querySelector("math-field") as HTMLElement | null;
      const radio = document.querySelector("input[type='radio']") as HTMLElement | null;

      if (field !== null) {
         tabTo(field);
         press("5");
      } else if (radio !== null) {
         tabTo(radio);
         press(" ");
      }

      activate(screen.getByTestId("lesson-check-submit"));
      await settle();
      expect(screen.getByTestId("lesson-check-verdict")).toBeTruthy();
   }
}

beforeAll(() => {
   defineKeyboardMathField();
});

beforeEach(() => {
   startRecordingPointer();
});

afterEach(() => {
   stopRecordingPointer();
   cleanup();
});

describe("LessonReader", () => {
   it("keyboard only, walks from the first section to the end screen, one section per screen", async () => {
      const given = props({ lesson: { ...LESSON, kind: "decision" } });

      render(<LessonReader {...given} />);

      const seen: string[] = [];

      for (let guard = 0; guard < 40 && screen.queryByTestId("lesson-finish") === null; guard += 1) {
         seen.push(currentScreen().getAttribute("data-section-id") ?? "");
         expect(document.querySelectorAll("[data-testid='lesson-screen']")).toHaveLength(1);
         expect(screen.getByTestId("lesson-skip").textContent).toBe("Skip to the problem");

         await workScreen();
         activate(screen.getByTestId("lesson-next"));
      }

      expect(seen).toEqual([
         "LSN-CON-02013#s1",
         "LSN-CON-02013#s2",
         "LSN-CON-02013#s3",
         "LSN-CON-02013#stems",
         ...EVERY_SECTION.slice(3),
         ...CHECKS
      ]);
      expect(currentScreen().getAttribute("data-screen-kind")).toBe("end");
      expect(currentScreen().textContent).toContain("The first problem is next. It shows a full worked solution you complete.");

      activate(screen.getByTestId("lesson-finish"));

      expect(given.onComplete).toHaveBeenCalledTimes(1);
      expect(given.onSkip).not.toHaveBeenCalled();
      expect(given.onCheckAnswer).toHaveBeenCalledTimes(2);
      expect(vi.mocked(given.onSectionViewed).mock.calls.map((call) => [call[0], call[1]])).toEqual(
         seen.map((id) => {
            const section = LESSON.sections.find((entry) => entry.id === id);
            const isContrast = id.endsWith("#stems") || section?.contrast !== undefined;
            const mode = isContrast ? "contrast" : id.includes("#chk-") ? "check" : section?.delivery?.mode ?? "text";

            return [id, mode];
         })
      );
      expect(vi.mocked(given.onSectionViewed).mock.calls.every((call) => typeof call[2] === "number" && call[2] >= 0)).toBe(true);
      expect(pointerEvents).toEqual([]);
   });

   it("reveals a worked example one step at a time, earlier steps staying, the why line beside its step", () => {
      render(<LessonReader {...props({ plan: planFor(["LSN-CON-02013#s5"]) })} />);

      const steps = () => screen.getAllByTestId("lesson-step");

      expect(steps()).toHaveLength(1);

      activate(screen.getByTestId("lesson-next-step"));

      expect(steps()).toHaveLength(2);
      expect(within(steps()[1]).getByTestId("lesson-step-cue").parentElement).toBe(within(steps()[1]).getByTestId("lesson-step-why").parentElement);

      activate(screen.getByTestId("lesson-next-step"));

      expect(steps()).toHaveLength(3);
      expect(screen.queryByTestId("lesson-next-step")).toBeNull();
   });

   it("the skip path calls onSkip with the index of the screen it leaves", () => {
      const given = props();

      render(<LessonReader {...given} />);

      activate(screen.getByTestId("lesson-next"));
      activate(screen.getByTestId("lesson-next"));
      activate(screen.getByTestId("lesson-skip"));

      expect(given.onSkip).toHaveBeenCalledWith(2);
      expect(given.onComplete).not.toHaveBeenCalled();
      expect(vi.mocked(given.onSectionViewed).mock.calls.map((call) => call[0])).toEqual([
         "LSN-CON-02013#s1",
         "LSN-CON-02013#s2",
         "LSN-CON-02013#s3"
      ]);
   });

   it("a wrong check answer names the error block and links its anchor, with no praise and no score", async () => {
      const verdict: LessonCheckVerdict = { correct: false, error_id: "BC-ERR-02020", anchor: "#err-BC-ERR-02020", explanation_anchor: null };
      const given = props({
         plan: planFor(["LSN-CON-02013#s5", "LSN-CON-02013#err-BC-ERR-02020"], ["LSN-CON-02013#chk-3"]),
         onCheckAnswer: vi.fn().mockResolvedValue(verdict)
      });

      render(<LessonReader {...given} />);

      activate(screen.getByTestId("lesson-show-all-steps"));
      activate(screen.getByTestId("lesson-next"));
      activate(screen.getByTestId("lesson-next"));
      tabTo(document.querySelector("input[type='radio']") as HTMLElement);
      press("ArrowDown");
      activate(screen.getByTestId("lesson-check-submit"));
      await settle();

      expect(given.onCheckAnswer).toHaveBeenCalledWith("LSN-CON-02013#chk-3", expect.objectContaining({ option_id: "B" }));

      const feedback = screen.getByTestId("lesson-check-verdict");

      expect(feedback.textContent).toContain("Not yet.");
      expect(feedback.textContent).toContain("The response multiplies the derivatives of the two factors together.");
      expect(screen.getByTestId("lesson-verdict-right-step").textContent).toContain("The right step: The rule adds two terms");
      expect(screen.getByTestId("lesson-verdict-consequence").textContent).toBe("On the exam: The rule point and the result point are both lost.");
      expect(feedback.textContent).not.toMatch(PRAISE);
      expect(feedback.textContent).not.toMatch(/\d/);

      const link = screen.getByTestId("lesson-link");

      expect(link.getAttribute("data-anchor")).toBe("#err-BC-ERR-02020");

      activate(link);

      expect(currentScreen().getAttribute("data-section-id")).toBe("LSN-CON-02013#err-BC-ERR-02020");

      activate(screen.getByTestId("lesson-return"));

      expect(currentScreen().getAttribute("data-section-id")).toBe("LSN-CON-02013#chk-3");
   });

   it("a right check answer reads Correct with its glyph and nothing more", async () => {
      render(<LessonReader {...props({ plan: planFor([], ["LSN-CON-02013#chk-3"]) })} />);

      tabTo(document.querySelector("input[type='radio']") as HTMLElement);
      press(" ");
      activate(screen.getByTestId("lesson-check-submit"));
      await settle();

      expect(screen.getByTestId("lesson-check-verdict").textContent).toBe("ok Correct");
   });

   it("opens an error block the plan left out below the check rather than dropping the link", async () => {
      const verdict: LessonCheckVerdict = { correct: false, error_id: "BC-ERR-02020", anchor: "LSN-CON-02013#err-BC-ERR-02020", explanation_anchor: null };

      render(<LessonReader {...props({ plan: planFor([], ["LSN-CON-02013#chk-1"]), onCheckAnswer: vi.fn().mockResolvedValue(verdict) })} />);

      tabTo(document.querySelector("math-field") as HTMLElement);
      press("6");
      activate(screen.getByTestId("lesson-check-submit"));
      await settle();
      activate(screen.getByTestId("lesson-link"));

      expect(within(currentScreen()).getByTestId("lesson-inline-section").getAttribute("data-section-id")).toBe("LSN-CON-02013#err-BC-ERR-02020");
   });

   it("writes the top bar of plan 15 UI for a session, a library read and a refresher", () => {
      render(<LessonReader {...props()} />);
      expect(screen.getByTestId("lesson-top-bar").textContent).toBe("Before the first problem on the product rule. About 4 minutes.");
      cleanup();

      render(<LessonReader {...props({ context: "library" })} />);
      expect(screen.getByTestId("lesson-top-bar").textContent).toBe("the product rule");
      expect(screen.getByTestId("lesson-back").textContent).toBe("Back to progress");
      expect(screen.queryByTestId("lesson-skip")).toBeNull();
      cleanup();

      const given = props({ plan: planFor(["LSN-CON-02013#s2", "LSN-CON-02013#err-BC-ERR-02020", "LSN-CON-02013#s5"], [], "T1") });

      render(<LessonReader {...given} />);
      expect(screen.getByTestId("lesson-top-bar").textContent).toBe("Before the next problem on the product rule. About a minute.");
      expect(screen.getByTestId("refresher-panel").querySelectorAll("[data-testid='lesson-section']")).toHaveLength(3);

      activate(screen.getByTestId("refresher-back"));
      expect(given.onComplete).toHaveBeenCalledTimes(1);
   });

   it("the library end screen returns to progress", () => {
      const given = props({ context: "library", plan: planFor(["LSN-CON-02013#s1"]) });

      render(<LessonReader {...given} />);
      activate(screen.getByTestId("lesson-next"));

      expect(currentScreen().getAttribute("data-screen-kind")).toBe("end");
      expect(screen.getByTestId("lesson-finish").textContent).toBe("Back to progress");

      activate(screen.getByTestId("lesson-finish"));
      expect(given.onComplete).toHaveBeenCalledTimes(1);
   });

   it("renders a strategy as four labelled lines and the scoring checklist without ticks", () => {
      render(<LessonReader {...props({ plan: planFor(["LSN-CON-02013#s3", "LSN-CON-02013#s7"]) })} />);

      expect(Array.from(currentScreen().querySelectorAll("dt")).map((term) => term.textContent)).toEqual([
         "Cue",
         "First line",
         "Rival",
         "Separating feature"
      ]);

      activate(screen.getByTestId("lesson-next"));

      expect(currentScreen().querySelectorAll("input[type='checkbox']")).toHaveLength(0);
      expect(currentScreen().querySelector("ul")!.className).toContain("lesson-checklist");
   });
});

function stylesheetRule(css: string, selector: string) {
   const escaped = selector.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
   const match = new RegExp(`(^|\\n)\\s*${escaped}\\s*\\{([^}]*)\\}`).exec(css);

   return match === null ? null : match[2];
}

function mediaBlock(css: string, query: string) {
   const start = css.indexOf(`@media ${query}`);

   if (start === -1) {
      return "";
   }

   let depth = 0;
   let opened = false;

   for (let position = css.indexOf("{", start); position < css.length; position += 1) {
      const character = css[position];

      if (character === "{") {
         depth += 1;
         opened = true;
      }

      if (character === "}") {
         depth -= 1;
      }

      const isClosed = opened && depth === 0;

      if (isClosed) {
         return css.slice(start, position + 1);
      }
   }

   return "";
}

function chooseOption(letter: string) {
   const radios = Array.from(currentScreen().querySelectorAll("input[type='radio']")) as HTMLInputElement[];
   const target = radios.findIndex((radio) => radio.value === letter);

   tabTo(radios[0]);

   if (target === 0) {
      press(" ");
   }

   for (let moved = 0; moved < target; moved += 1) {
      press("ArrowDown");
   }
}

async function commitPrediction(letter = "B") {
   chooseOption(letter);
   activate(screen.getByTestId("lesson-prediction-commit"));
   await settle();
}

describe("LessonReader, the v2 screens", () => {
   it("the prediction's Commit gates Next part, posts through the prompts route and says only Committed.", async () => {
      const given = props({ plan: planFor([PREDICTION_ID, "LSN-CON-02013#s1"]) });

      render(<LessonReader {...given} />);

      const next = () => screen.getByTestId("lesson-next") as HTMLButtonElement;

      expect(within(currentScreen()).getByTestId("lesson-prediction")).toBeTruthy();
      expect(screen.getByTestId("lesson-part-name").textContent).toBe("Predict");
      expect(next().disabled).toBe(true);
      expect((screen.getByTestId("lesson-prediction-commit") as HTMLButtonElement).disabled).toBe(true);

      await commitPrediction("B");

      expect(given.onPromptAnswer).toHaveBeenCalledWith(PREDICTION_ID, { answer: null, option_id: "B", elapsed_ms: expect.any(Number) });
      expect(screen.queryByTestId("lesson-prediction-commit")).toBeNull();
      expect(screen.getByTestId("lesson-prediction").textContent).toContain("Committed.");
      expect(screen.getByTestId("lesson-prediction").textContent).not.toMatch(/correct|not yet|wrong|right/i);
      expect(next().disabled).toBe(false);

      activate(next());

      expect(currentScreen().getAttribute("data-section-id")).toBe("LSN-CON-02013#s1");
      expect(pointerEvents).toEqual([]);
   });

   it("the first core key idea opens with the committed prediction and its resolution, and says nothing without one", async () => {
      const given = props({
         plan: planFor([PREDICTION_ID, "LSN-CON-02013#s2"]),
         onPromptAnswer: vi.fn().mockResolvedValue(promptVerdict(PREDICTION_ID, true, "A product gives two terms, each with one derivative."))
      });

      render(<LessonReader {...given} />);
      await commitPrediction("A");
      activate(screen.getByTestId("lesson-next"));

      const line = within(currentScreen()).getByTestId("lesson-prediction-resolution");

      expect(line.textContent).toBe("You predicted The product of the two derivatives. A product gives two terms, each with one derivative.");
      expect(line.compareDocumentPosition(within(currentScreen()).getByText(/For a product/)) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
      cleanup();

      render(<LessonReader {...props({ plan: planFor(["LSN-CON-02013#s2"]) })} />);

      expect(screen.queryByTestId("lesson-prediction-resolution")).toBeNull();
   });

   it("the strategy screen shows the contrast pair under its four lines and posts contrast as its mode", () => {
      const given = props({ plan: planFor(["LSN-CON-02013#s3", "LSN-CON-02013#s1"]) });

      render(<LessonReader {...given} />);

      const pair = within(currentScreen()).getByTestId("lesson-contrast");
      const strategyLines = currentScreen().querySelector("dl")!;

      expect(strategyLines.compareDocumentPosition(pair) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
      expect(screen.getByTestId("lesson-part-name").textContent).toBe("Recognise");
      expect(within(pair).getByTestId("lesson-contrast-this").textContent).toContain("This concept");
      expect(within(pair).getByTestId("lesson-contrast-not-this").textContent).toContain("Not this one");
      expect(pair.textContent).toContain("What separates them: two factors multiplied, not one function inside another");
      expect(pair.querySelector(".muted")!.textContent).toBe("One function sits inside another, so the chain rule applies.");

      activate(screen.getByTestId("lesson-next"));

      expect(vi.mocked(given.onSectionViewed).mock.calls[0].slice(0, 2)).toEqual(["LSN-CON-02013#s3", "contrast"]);
   });

   it("the contrast pair sits side by side and stacks at 600 px and under", () => {
      const css = readFileSync(resolve(__dirname, "..", "styles", "app.css"), "utf8").replace(/\/\*[\s\S]*?\*\//g, " ");
      const wide = stylesheetRule(css, ".lesson-contrast-pair");
      const narrow = stylesheetRule(mediaBlock(css, "(max-width: 600px)"), ".lesson-contrast-pair");

      expect(wide).not.toBeNull();
      expect(wide).toMatch(/display:\s*flex/);
      expect(wide).not.toMatch(/flex-direction:\s*column/);
      expect(narrow).toMatch(/flex-direction:\s*column/);

      render(<LessonReader {...props({ plan: planFor(["LSN-CON-02013#s3"]) })} />);

      expect(screen.getByTestId("lesson-contrast").querySelector(".lesson-contrast-pair")!.children).toHaveLength(2);
   });

   it("a worked example with steps left reads Show all steps, which reveals them, and only then Next part", () => {
      render(<LessonReader {...props({ plan: planFor(["LSN-CON-02013#s5", "LSN-CON-02013#s1"]) })} />);

      expect(screen.queryByTestId("lesson-next")).toBeNull();
      expect(screen.getByTestId("lesson-show-all-steps").textContent).toBe("Show all steps");
      expect(screen.getAllByTestId("lesson-step")).toHaveLength(1);

      activate(screen.getByTestId("lesson-show-all-steps"));

      expect(screen.getAllByTestId("lesson-step")).toHaveLength(3);
      expect(screen.queryByTestId("lesson-show-all-steps")).toBeNull();
      expect(screen.getByTestId("lesson-next").textContent).toBe("Next part");

      activate(screen.getByTestId("lesson-next"));

      expect(currentScreen().getAttribute("data-section-id")).toBe("LSN-CON-02013#s1");
   });

   it("the faded example shows the steps before fade_from, grades the answer through the prompts route and reveals the rest", async () => {
      const given = props({ plan: planFor([FADED_EXAMPLE_ID, "LSN-CON-02013#s1"]) });

      render(<LessonReader {...given} />);

      const fade = within(currentScreen()).getByTestId("lesson-fade-answer");

      expect(screen.getByTestId("lesson-part-name").textContent).toBe("Faded example");
      expect(screen.getAllByTestId("lesson-step")).toHaveLength(1);
      expect(fade.textContent).toContain("Write the answer");
      expect(screen.getByTestId("lesson-show-all-steps")).toBeTruthy();

      tabTo(fade.querySelector("math-field") as HTMLElement);
      press("7");
      activate(within(fade).getByRole("button", { name: "Check my answer" }));
      await settle();

      expect(given.onPromptAnswer).toHaveBeenCalledWith(FADED_EXAMPLE_ID, { answer: 7, option_id: null, elapsed_ms: expect.any(Number) });
      expect(screen.getAllByTestId("lesson-step")).toHaveLength(3);
      expect(currentScreen().textContent).toContain("Not yet.");
      expect(screen.queryByTestId("lesson-show-all-steps")).toBeNull();

      activate(screen.getByTestId("lesson-next"));

      expect(currentScreen().getAttribute("data-section-id")).toBe("LSN-CON-02013#s1");
      expect(pointerEvents).toEqual([]);
   });

   it("a right faded answer reads Correct., and Show all steps without an answer reveals the rest with no post", async () => {
      const given = props({ plan: planFor([FADED_EXAMPLE_ID]), onPromptAnswer: vi.fn().mockResolvedValue(promptVerdict(FADED_EXAMPLE_ID, true)) });

      render(<LessonReader {...given} />);
      tabTo(currentScreen().querySelector("math-field") as HTMLElement);
      press("9");
      activate(within(screen.getByTestId("lesson-fade-answer")).getByRole("button", { name: "Check my answer" }));
      await settle();

      expect(currentScreen().textContent).toContain("Correct.");
      expect(currentScreen().textContent).not.toContain("Not yet.");
      cleanup();

      const unanswered = props({ plan: planFor([FADED_EXAMPLE_ID]) });

      render(<LessonReader {...unanswered} />);
      activate(screen.getByTestId("lesson-show-all-steps"));

      expect(screen.getAllByTestId("lesson-step")).toHaveLength(3);
      expect(screen.queryByTestId("lesson-fade-answer")).toBeNull();
      expect(unanswered.onPromptAnswer).not.toHaveBeenCalled();
   });

   it("a fix prompt asks for the right step, grades it, then shows Not yet. above the right step and the consequence", async () => {
      const given = props({ plan: planFor([ERROR_ID]) });

      render(<LessonReader {...given} />);

      const prompt = within(currentScreen()).getByTestId("lesson-fix-prompt");

      expect(screen.getByTestId("lesson-part-name").textContent).toBe("Trap");
      expect(prompt.textContent).toContain("What should this step be?");
      expect(screen.queryByTestId("lesson-right-step")).toBeNull();
      expect(currentScreen().textContent).not.toContain("The rule point and the result point are both lost.");
      expect(currentScreen().textContent).not.toContain("A possible reason");

      tabTo(prompt.querySelector("math-field") as HTMLElement);
      press("5");
      activate(screen.getByTestId("lesson-fix-submit"));
      await settle();

      expect(given.onPromptAnswer).toHaveBeenCalledWith(ERROR_ID, { answer: 5, option_id: null, elapsed_ms: expect.any(Number) });

      const right = screen.getByTestId("lesson-right-step");

      expect(right.textContent).toMatch(/^x Not yet\..*Right step/);
      expect(screen.getByTestId("lesson-wrong-step").textContent).toContain("Wrong step");
      expect(screen.queryByTestId("lesson-fix-prompt")).toBeNull();
      expect(currentScreen().textContent).toContain("The rule point and the result point are both lost.");
      expect(currentScreen().textContent).toContain("A possible reason");
      expect(pointerEvents).toEqual([]);
   });

   it("Show the right step reveals it with no post and no verdict", () => {
      const given = props({ plan: planFor([ERROR_ID]) });

      render(<LessonReader {...given} />);
      activate(screen.getByTestId("lesson-fix-show"));

      expect(screen.getByTestId("lesson-right-step").textContent).not.toContain("Not yet.");
      expect(currentScreen().textContent).toContain("The rule point and the result point are both lost.");
      expect(given.onPromptAnswer).not.toHaveBeenCalled();
   });

   it("an error block without fix_prompt keeps the Next step reveal", () => {
      const lesson = { ...LESSON, sections: LESSON.sections.map((section) => (section.id === ERROR_ID ? { ...section, fix_prompt: false } : section)) };

      render(<LessonReader {...props({ lesson, plan: planFor([ERROR_ID]) })} />);

      expect(screen.queryByTestId("lesson-fix-prompt")).toBeNull();

      activate(screen.getByTestId("lesson-next-step"));

      expect(screen.getByTestId("lesson-right-step")).toBeTruthy();
   });

   it("posts prediction for a prediction screen and check for a check screen", async () => {
      const given = props({ plan: planFor([PREDICTION_ID], ["LSN-CON-02013#chk-3"]) });

      render(<LessonReader {...given} />);
      await commitPrediction("B");
      activate(screen.getByTestId("lesson-next"));

      expect(vi.mocked(given.onSectionViewed).mock.calls.map((call) => call[1])).toEqual(["prediction"]);

      activate(screen.getByTestId("lesson-next"));

      expect(vi.mocked(given.onSectionViewed).mock.calls.map((call) => [call[0], call[1]])).toEqual([
         [PREDICTION_ID, "prediction"],
         ["LSN-CON-02013#chk-3", "check"]
      ]);
   });

   it("names every part in the pacing line", async () => {
      const sections = [
         PREDICTION_ID,
         "LSN-CON-02013#s1",
         "LSN-CON-02013#prq-BC-PRQ-00001",
         "LSN-CON-02013#s2",
         "LSN-CON-02013#s3",
         "LSN-CON-02013#s5",
         "LSN-CON-02013#s7",
         ERROR_ID,
         FADED_EXAMPLE_ID,
         "LSN-CON-02013#r-figure"
      ];

      render(<LessonReader {...props({ plan: planFor(sections, ["LSN-CON-02013#chk-3"]) })} />);
      await commitPrediction("B");

      const names: string[] = [];

      for (let guard = 0; guard < 20; guard += 1) {
         names.push(screen.getByTestId("lesson-part-name").textContent ?? "");

         if (screen.queryByTestId("lesson-show-all-steps") !== null) {
            activate(screen.getByTestId("lesson-show-all-steps"));
         }

         if (screen.queryByTestId("lesson-next") === null) {
            break;
         }

         activate(screen.getByTestId("lesson-next"));
      }

      expect(names).toEqual([
         "Predict",
         "What a response shows",
         "From earlier",
         "Key idea",
         "Recognise",
         "Example",
         "Example",
         "Trap",
         "Faded example",
         "Reading the representation",
         "Check",
         "End"
      ]);
      expect(screen.getByTestId("lesson-part").textContent).toBe("Part 12 of 12");
   });
});
