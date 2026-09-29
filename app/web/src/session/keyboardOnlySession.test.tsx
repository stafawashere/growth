import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest";

import { App } from "../App";
import * as client from "../api/client";
import type { AttemptResult, FeedbackPayload, ProgressPayload, ServedItem, SessionPayload } from "../api/types";
import { multipleChoiceQuestion, noCalculatorPart } from "../assessment/fixtures";
import { PartRunner } from "../assessment/PartRunner";

vi.mock("../api/client");

const mocked = vi.mocked(client);

/* 11's P8 end-to-end test_keyboard_only_session: a whole learning session with no pointer. jsdom
   moves no focus on Tab and turns no key into a click, so the driver below does what a browser
   does. Tab and Shift+Tab walk the tabbable elements in document order, a radio group being one
   stop at its checked radio or, with none checked, its first. Enter on a button or link and Space
   on a button, checkbox or radio dispatch the click the browser would. An arrow key in a radio
   group checks and clicks the next radio. A printable key in a text field enters that character.
   Every pointer event is recorded, and so is any click the driver did not dispatch as a keyboard
   activation; either fails the test, as does a step whose control Tab never reaches. */

const TABBABLE = [
   "button:not(:disabled)",
   "input:not(:disabled):not([type='hidden'])",
   "select:not(:disabled)",
   "textarea:not(:disabled)",
   "a[href]",
   "summary",
   "[tabindex]"
].join(", ");

const POINTER_EVENTS = ["pointerdown", "pointerup", "mousedown", "mouseup", "touchstart", "touchend"];

const pointerEvents: string[] = [];

let isKeyboardActivation = false;

function recordPointer(event: Event) {
   pointerEvents.push(`${event.type} on ${(event.target as Element).tagName}`);
}

function recordPointerClick(event: Event) {
   if (!isKeyboardActivation) {
      pointerEvents.push(`pointer click on ${(event.target as Element).tagName}`);
   }
}

function isHiddenByAncestor(element: Element) {
   return element.closest("[hidden], [inert]") !== null;
}

function isRadioStop(element: HTMLInputElement, all: Element[]) {
   const group = all.filter(
      (candidate): candidate is HTMLInputElement =>
         candidate instanceof HTMLInputElement && candidate.type === "radio" && candidate.name === element.name
   );
   const checked = group.find((radio) => radio.checked);

   return element === (checked ?? group[0]);
}

function tabbables(): HTMLElement[] {
   const all = Array.from(document.body.querySelectorAll(TABBABLE));

   return all.filter((element): element is HTMLElement => {
      const index = Number(element.getAttribute("tabindex") ?? "0");
      const isRadio = element instanceof HTMLInputElement && element.type === "radio";

      if (index < 0 || isHiddenByAncestor(element)) {
         return false;
      }

      return isRadio ? isRadioStop(element as HTMLInputElement, all) : true;
   });
}

function moveFocus(step: 1 | -1) {
   const order = tabbables();
   const current = order.indexOf(document.activeElement as HTMLElement);
   const start = current === -1 ? (step === 1 ? -1 : 0) : current;
   const next = order[(start + step + order.length) % order.length];

   fireEvent.keyDown(document.activeElement ?? document.body, { key: "Tab", shiftKey: step === -1 });
   act(() => next.focus());
}

const tab = () => moveFocus(1);

const shiftTab = () => moveFocus(-1);

/* Tabs until the target has focus, failing if a full cycle never reaches it. */
function tabTo(target: HTMLElement) {
   const stops = tabbables().length;

   for (let pressed = 0; pressed <= stops; pressed += 1) {
      if (document.activeElement === target) {
         return;
      }

      tab();
   }

   throw new Error(`Tab never reaches ${target.outerHTML.slice(0, 120)}`);
}

function keyboardClick(element: Element) {
   isKeyboardActivation = true;

   try {
      act(() => {
         element.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, detail: 0 }));
      });
   } finally {
      isKeyboardActivation = false;
   }
}

function typeCharacter(field: HTMLInputElement | HTMLTextAreaElement, character: string) {
   fireEvent.input(field, { target: { value: field.value + character } });
}

function press(key: string) {
   const focused = document.activeElement as HTMLElement;
   const proceeds = fireEvent.keyDown(focused, { key });

   if (!proceeds) {
      return;
   }

   const isButton = focused instanceof HTMLButtonElement || focused instanceof HTMLAnchorElement;
   const isChoice = focused instanceof HTMLInputElement && (focused.type === "radio" || focused.type === "checkbox");
   const isTextField = (focused instanceof HTMLInputElement && !isChoice) || focused instanceof HTMLTextAreaElement;
   const isArrow = ["ArrowDown", "ArrowRight", "ArrowUp", "ArrowLeft"].includes(key);

   if (key === "Enter" && isButton) {
      keyboardClick(focused);
   } else if (key === " " && (isButton || isChoice)) {
      keyboardClick(focused);
   } else if (isArrow && focused instanceof HTMLInputElement && focused.type === "radio") {
      const group = Array.from(document.querySelectorAll<HTMLInputElement>(`input[type='radio'][name='${focused.name}']`));
      const step = key === "ArrowDown" || key === "ArrowRight" ? 1 : -1;
      const next = group[(group.indexOf(focused) + step + group.length) % group.length];

      act(() => next.focus());
      keyboardClick(next);
   } else if (key.length === 1 && isTextField) {
      typeCharacter(focused as HTMLInputElement, key);
   }

   fireEvent.keyUp(focused, { key });
}

function typeText(text: string) {
   for (const character of text) {
      press(character);
   }
}

/* The math field seam: MathLive's element is focusable in the tab order and turns keystrokes into
   its value. This stands in for it with only what MathField.tsx reads, getValue and the input
   event. */
class KeyboardMathField extends HTMLElement {
   private latex = "";

   connectedCallback() {
      this.tabIndex = 0;
      this.addEventListener("keydown", (event) => {
         const isCharacter = event.key.length === 1;

         if (isCharacter) {
            this.latex += event.key;
            this.dispatchEvent(new Event("input", { bubbles: true }));
         }
      });
   }

   getValue(format: string) {
      if (format === "math-json") {
         return JSON.stringify(Number.isNaN(Number(this.latex)) ? this.latex : Number(this.latex));
      }

      return this.latex;
   }
}

const me: client.MePayload = { id: "USR-1", display_name: null, exam_date: "2027-05-10", purge_after: "2027-06-09" };

const progress: ProgressPayload = {
   home_state: "queue",
   days_since_last_session: 1,
   diagnostic_in_progress: null,
   skills_due_for_review: 2,
   frontier_skills: 1,
   corrected_items_returning: 0,
   forecast_minutes: 10,
   due_today_skills: 2,
   due_today_minutes: 10,
   session_in_progress: null,
   focus: []
};

const session: SessionPayload = {
   id: "SES-K",
   mode: "learning",
   sub_mode: null,
   started_at: "2027-01-05T09:30:00",
   ended_at: null,
   updates_mastery: true,
   snapshot_id: null,
   queue: {
      block1: [],
      block2: [],
      block3: [],
      block4: [],
      forecasts: {},
      coverage_gaps: [],
      interleaving_satisfied: true,
      interleaving_shortfalls: []
   },
   remaining: []
};

function item(overrides: Partial<ServedItem>): ServedItem {
   return {
      id: "ITM-1",
      archetype_id: "BC-ARCH-0101",
      variant_id: null,
      snapshot_id: null,
      parameter_draw: null,
      stem: "Evaluate the limit of (x^2 - 9)/(x - 3) as x approaches 3.",
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

const shortAnswer = item({
   stage: "completion",
   served_steps: [{ index: 1, text: "Factor the numerator as (x - 3)(x + 3)" }]
});

const multipleChoice = item({
   id: "ITM-2",
   stem: "Which is the derivative of x^2?",
   format: "mcq",
   options: [
      { id: "A", label: "x" },
      { id: "B", label: "2x" },
      { id: "C", label: "x^2 / 2" }
   ]
});

function attempt(served: ServedItem, correct: boolean, confidence: AttemptResult["confidence"]): AttemptResult {
   return {
      id: `ATT-${served.id}`,
      item_id: served.id,
      correct,
      confidence,
      served_stage: served.stage,
      format: served.format,
      p_split: null,
      p_compensatory: null
   };
}

function feedback(correct: boolean): FeedbackPayload {
   return {
      kind: correct ? "step_verification" : "elaborated",
      stage: correct ? "completion" : "unsupported",
      step_marks: correct
         ? [
              { index: 1, text: "Factor the numerator as (x - 3)(x + 3)", given: true, correct: null },
              { index: 2, text: "Cancel x - 3 and substitute, 6", given: false, correct: true }
           ]
         : [],
      elaborated: correct
         ? null
         : {
              violated_step: "The power rule multiplies by the exponent",
              observed_behavior: "The exponent was dropped without multiplying",
              scoring_consequence: null,
              worked_solution: null,
              error_id: "BC-ERR-0201"
           },
      self_explanation_prompt: null,
      confidence: null,
      sentence: null,
      tutor_unavailable: false
   };
}

beforeAll(() => {
   if (customElements.get("math-field") === undefined) {
      customElements.define("math-field", KeyboardMathField);
   }
});

beforeEach(() => {
   vi.clearAllMocks();
   pointerEvents.length = 0;

   for (const type of POINTER_EVENTS) {
      document.addEventListener(type, recordPointer, true);
   }

   document.addEventListener("click", recordPointerClick, true);
});

afterEach(() => {
   for (const type of POINTER_EVENTS) {
      document.removeEventListener(type, recordPointer, true);
   }

   document.removeEventListener("click", recordPointerClick, true);
   cleanup();
});

describe("test_keyboard_only_session", () => {
   it("the driver records a pointer click and moves focus only through tabbable controls", () => {
      render(
         <div>
            <button type="button">First</button>
            <button type="button" tabIndex={-1}>
               Skipped
            </button>
            <button type="button" disabled>
               Disabled
            </button>
            <input type="radio" name="probe" aria-label="one" />
            <input type="radio" name="probe" aria-label="two" />
            <button type="button">Last</button>
         </div>
      );

      tab();
      expect(document.activeElement?.textContent).toBe("First");
      tab();
      expect(document.activeElement?.getAttribute("aria-label")).toBe("one");
      tab();
      expect(document.activeElement?.textContent).toBe("Last");
      shiftTab();
      expect(document.activeElement?.getAttribute("aria-label")).toBe("one");

      fireEvent.click(screen.getByText("Last"));

      expect(pointerEvents).toEqual(["pointer click on BUTTON"]);
   });

   it("runs a whole session from home to the end of the set with the keyboard alone", async () => {
      mocked.readMe.mockResolvedValue(me);
      mocked.readProgress.mockResolvedValue(progress);
      mocked.openSession.mockResolvedValue(session);
      mocked.readNextItem
         .mockResolvedValueOnce({ item: shortAnswer })
         .mockResolvedValueOnce({ item: multipleChoice })
         .mockResolvedValue({ item: null });
      mocked.submitAttempt
         .mockResolvedValueOnce(attempt(shortAnswer, true, "confident"))
         .mockResolvedValueOnce(attempt(multipleChoice, false, "guess"));
      mocked.readFeedback.mockResolvedValueOnce(feedback(true)).mockResolvedValueOnce(feedback(false));
      mocked.submitErrorNote.mockResolvedValue({ id: "ATT-ITM-2", error_note: "I dropped the exponent." });
      mocked.closeSession.mockResolvedValue({ id: session.id, ended_at: "2027-01-05T10:00:00" });

      render(<App />);

      tabTo(await screen.findByRole("button", { name: "Start today's set" }));
      press("Enter");

      await screen.findByTestId("item");
      tabTo(screen.getByLabelText("My answer"));
      typeText("6");
      tabTo(screen.getByRole("radio", { name: "guess" }));
      press("ArrowRight");
      press("ArrowRight");
      expect(screen.getByRole("radio", { name: "confident" })).toHaveProperty("checked", true);

      tabTo(screen.getByRole("button", { name: "Check my answer" }));
      shiftTab();
      expect(document.activeElement).toBe(screen.getByRole("radio", { name: "confident" }));
      tab();
      press("Enter");

      expect((await screen.findByTestId("step-marks")).textContent).toContain("Correct");
      tabTo(screen.getByRole("button", { name: "Next item" }));
      press("Enter");

      await screen.findByText("Which is the derivative of x^2?");
      tabTo(screen.getAllByRole("radio")[0]);
      press("ArrowDown");
      tabTo(screen.getByRole("radio", { name: "guess" }));
      press(" ");
      tabTo(screen.getByRole("button", { name: "Check my answer" }));
      press("Enter");

      const corrected = await screen.findByTestId("elaborated-panel");

      expect(corrected.textContent).toContain("Not yet");
      expect(screen.getByRole("button", { name: "Next item" })).toHaveProperty("disabled", true);

      tabTo(screen.getByLabelText("In one line, what went wrong?"));
      typeText("I dropped the exponent.");
      tabTo(screen.getByRole("button", { name: "Next item" }));
      press("Enter");

      await screen.findByText("That is today's set finished.");

      expect(mocked.submitAttempt.mock.calls.map((call) => [call[1].answer, call[1].confidence])).toEqual([
         [{ mathjson: 6 }, "confident"],
         [{ option_id: "B" }, "guess"]
      ]);
      expect(mocked.submitErrorNote).toHaveBeenCalledWith(session.id, "ATT-ITM-2", "I dropped the exponent.");
      expect(mocked.closeSession).toHaveBeenCalledWith(session.id);
      expect(pointerEvents).toEqual([]);
   });

   it("answers and submits a timed mock part with the keyboard alone", async () => {
      const onSubmit = vi.fn();
      const onSave = vi.fn();

      render(
         <PartRunner
            part={noCalculatorPart({ questions: [multipleChoiceQuestion(1), multipleChoiceQuestion(2)] })}
            radianNote="Radian mode."
            sectionCount={42}
            onSave={onSave}
            onSubmit={onSubmit}
            onTimeUp={vi.fn()}
         />
      );

      tabTo(screen.getByRole("radio", { name: /First choice/ }));
      press("ArrowDown");
      tabTo(screen.getByRole("button", { name: "Next" }));
      press("Enter");

      await screen.findByText(/question 2\./);
      tabTo(screen.getByRole("radio", { name: /First choice/ }));
      press(" ");
      tabTo(screen.getByRole("button", { name: "Submit part" }));
      press("Enter");
      tabTo(screen.getByRole("button", { name: "Submit and close this part" }));
      press("Enter");

      await waitFor(() => expect(onSubmit).toHaveBeenCalledTimes(1));

      const answers = onSave.mock.calls.filter((call) => call[1].answer !== undefined).map((call) => [call[0], call[1].answer]);

      expect(answers).toContainEqual([1, { option_id: "B" }]);
      expect(answers).toContainEqual([2, { option_id: "A" }]);
      expect(pointerEvents).toEqual([]);
   });
});
