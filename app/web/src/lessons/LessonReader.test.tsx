import { act, cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest";

import type { LessonCheckVerdict } from "../api/types";
import {
   activate,
   defineKeyboardMathField,
   pointerEvents,
   press,
   startRecordingPointer,
   stopRecordingPointer,
   tabTo
} from "../testing/keyboard";
import { LESSON, planFor } from "./fixtures";
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
      ...overrides
   };
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

      for (let guard = 0; guard < 40 && screen.queryByTestId("lesson-next") !== null; guard += 1) {
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
            const mode = id.endsWith("#stems") ? "contrast" : id.includes("#chk-") ? "check" : section?.delivery?.mode ?? "text";

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

      activate(screen.getByTestId("lesson-next"));
      activate(screen.getByTestId("lesson-next"));
      tabTo(document.querySelector("input[type='radio']") as HTMLElement);
      press("ArrowDown");
      activate(screen.getByTestId("lesson-check-submit"));
      await settle();

      expect(given.onCheckAnswer).toHaveBeenCalledWith("LSN-CON-02013#chk-3", expect.objectContaining({ option_id: "B" }));

      const feedback = screen.getByTestId("lesson-check-verdict");

      expect(feedback.textContent).toContain(
         "Not yet. The response multiplies the derivatives of the two factors together. The part above on that error shows the right step beside it."
      );
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
