import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest";

import * as client from "../api/client";
import { OPEN_DESMOS_LABEL } from "../input/DesmosPanel";
import { activate, defineKeyboardMathField, pointerEvents, press, startRecordingPointer, stopRecordingPointer, tabbables, tabTo } from "../testing/keyboard";
import { CalculatorRoute } from "./CalculatorRoute";
import { DrillScreen } from "./DrillScreen";
import { answer, drill, measured } from "./fixtures";
import {
   CHANGE_CAPABILITY_LABEL,
   CHECK_LABEL,
   HIDE_CLOCK,
   NEXT_LABEL,
   OFFLINE_SENTENCE,
   RESULT_LABEL,
   SETUP_EQUIVALENT,
   SETUP_MISSING,
   SETUP_NOT_EQUIVALENT,
   SKIP_TO_RESULT,
   VALUE_ACCURATE,
   VALUE_FEW_PLACES
} from "./words";

/* docs/calculator/design.md, The drills, Keyboard and When Desmos cannot load. */

vi.mock("../api/client");

const mocked = vi.mocked(client);

async function settle() {
   await act(async () => {
      await Promise.resolve();
      await Promise.resolve();
   });
}

function renderDrill(overrides: Partial<Parameters<typeof DrillScreen>[0]> = {}) {
   let clock = 5000;
   const now = () => clock;
   const advance = (milliseconds: number) => {
      clock += milliseconds;
   };

   render(
      <DrillScreen
         drill={drill("DRL-1")}
         offline={false}
         showsBudget
         focusTaskOnArrival={false}
         onAnswered={vi.fn()}
         onNext={vi.fn()}
         onChangeCapability={vi.fn()}
         now={now}
         {...overrides}
      />
   );

   return advance;
}

function typeSetup(text: string) {
   const field = document.querySelector("math-field") as HTMLElement;

   for (const key of text) {
      fireEvent.keyDown(field, { key });
   }
}

beforeAll(() => {
   defineKeyboardMathField();
});

beforeEach(() => {
   vi.clearAllMocks();
   window.localStorage.clear();
   mocked.answerCalculatorDrill.mockResolvedValue(answer());
});

afterEach(() => {
   cleanup();
   vi.unstubAllGlobals();
});

describe("a drill task", () => {
   it("sends the typed result, the setup and the time since the task first rendered", async () => {
      const advance = renderDrill();

      fireEvent.change(screen.getByLabelText(RESULT_LABEL), { target: { value: "3.901" } });
      typeSetup("7");
      advance(42000);
      fireEvent.click(screen.getByRole("button", { name: CHECK_LABEL }));
      await settle();

      expect(mocked.answerCalculatorDrill).toHaveBeenCalledWith("DRL-1", {
         value: "3.901",
         setup_mathjson: 7,
         elapsed_ms: 42000,
         desmos_open: false
      });
   });

   it("refuses nothing itself: an empty result and no setup go to the server as they are", async () => {
      renderDrill();

      fireEvent.click(screen.getByRole("button", { name: CHECK_LABEL }));
      await settle();

      expect(mocked.answerCalculatorDrill).toHaveBeenCalledWith("DRL-1", { value: "", setup_mathjson: null, elapsed_ms: 0, desmos_open: false });
   });

   it("shows the result line with both accepted forms, the setup line and the time, then Next and Change capability", async () => {
      renderDrill();

      fireEvent.click(screen.getByRole("button", { name: CHECK_LABEL }));
      await settle();

      expect(screen.getByTestId("drill-value-verdict").textContent).toBe(VALUE_ACCURATE);
      expect(screen.getByTestId("drill-accepted-forms").textContent).toBe("Rounded 3.901, truncated 3.900");
      expect(screen.getByTestId("drill-setup-verdict").textContent).toBe(SETUP_EQUIVALENT);
      expect(screen.getByTestId("drill-time").textContent).toBe("42 seconds");
      expect(screen.getByTestId("drill-budget").textContent).toBe("The exam allows 120 seconds a question on Section I Part B.");
      expect(screen.queryByTestId("drill-expected-setup")).toBeNull();
      expect(screen.getByTestId("drill-verdicts").getAttribute("aria-live")).toBe("polite");
      expect(document.activeElement).toBe(screen.getByTestId("drill-result-line"));
      expect(screen.queryByRole("button", { name: CHECK_LABEL })).toBeNull();
      expect(screen.getByRole("button", { name: NEXT_LABEL })).toBeTruthy();
      expect(screen.getByRole("button", { name: CHANGE_CAPABILITY_LABEL })).toBeTruthy();
   });

   it("says why a result was not accurate, and renders the expected setup under a wrong one", async () => {
      mocked.answerCalculatorDrill.mockResolvedValue(
         answer({
            value: { correct: false, reason: "not_three_places", rounded: "3.901", truncated: "3.900" },
            setup: { shown: true, correct: false, reason: "not_equivalent", key_latex: "\\int_0^2 \\sin(x^2)\\,dx" }
         })
      );
      renderDrill({ showsBudget: false });

      fireEvent.click(screen.getByRole("button", { name: CHECK_LABEL }));
      await settle();

      expect(screen.getByTestId("drill-value-verdict").textContent).toBe(VALUE_FEW_PLACES);
      expect(screen.getByTestId("drill-accepted-forms").textContent).toBe("Rounded 3.901, truncated 3.900");
      expect(screen.getByTestId("drill-setup-verdict").textContent).toBe(SETUP_NOT_EQUIVALENT);
      expect(screen.getByTestId("drill-expected-setup").querySelector(".katex")).not.toBeNull();
      expect(screen.queryByTestId("drill-budget")).toBeNull();
   });

   it("says no setup was shown when none was typed", async () => {
      mocked.answerCalculatorDrill.mockResolvedValue(answer({ setup: { shown: false, correct: null, reason: "missing", key_latex: "x" } }));
      renderDrill();

      fireEvent.click(screen.getByRole("button", { name: CHECK_LABEL }));
      await settle();

      expect(screen.getByTestId("drill-setup-verdict").textContent).toBe(SETUP_MISSING);
   });

   it("checks on Enter in the result field", async () => {
      renderDrill();

      fireEvent.keyDown(screen.getByLabelText(RESULT_LABEL), { key: "Enter" });
      await settle();

      expect(mocked.answerCalculatorDrill).toHaveBeenCalledTimes(1);
   });

   it("replaces Desmos with the offline sentence when the browser is offline, and keeps the fields", () => {
      vi.stubGlobal("navigator", { ...navigator, onLine: false });
      renderDrill();

      expect(screen.getByTestId("drill-offline").textContent).toBe(OFFLINE_SENTENCE);
      expect(screen.queryByRole("button", { name: OPEN_DESMOS_LABEL })).toBeNull();
      expect(screen.getByLabelText(RESULT_LABEL)).toBeTruthy();
   });

   it("replaces Desmos with the offline sentence while the app's offline notice shows", () => {
      renderDrill({ offline: true });

      expect(screen.getByTestId("drill-offline").textContent).toBe(OFFLINE_SENTENCE);
   });

   it("records that Desmos was open when it was opened for the task", async () => {
      renderDrill();

      fireEvent.click(screen.getByRole("button", { name: OPEN_DESMOS_LABEL }));
      fireEvent.click(screen.getByRole("button", { name: CHECK_LABEL }));
      await settle();

      expect(mocked.answerCalculatorDrill.mock.calls[0][1].desmos_open).toBe(true);
   });
});

describe("a drill from the keyboard alone", () => {
   beforeEach(() => {
      startRecordingPointer();
      mocked.readCalculatorMeasured.mockResolvedValue(measured());
      mocked.startCalculatorDrill.mockResolvedValueOnce(drill("DRL-1")).mockResolvedValueOnce(drill("DRL-2"));
   });

   afterEach(() => {
      stopRecordingPointer();
   });

   it("walks the chooser, the clock, Desmos, the result, the setup and Check in that order, checks, and moves on with Next", async () => {
      render(<CalculatorRoute section="drill" capability="integral" go={vi.fn()} />);
      await settle();

      const order = tabbables();
      const position = (element: Element) => order.indexOf(element as HTMLElement);
      const chooserButtons = Array.from(screen.getByTestId("capability-chooser").querySelectorAll("button"));
      const stops = [
         chooserButtons[chooserButtons.length - 1],
         screen.getByRole("link", { name: SKIP_TO_RESULT }),
         screen.getByRole("button", { name: HIDE_CLOCK }),
         screen.getByRole("button", { name: OPEN_DESMOS_LABEL }),
         screen.getByLabelText(RESULT_LABEL),
         document.querySelector("math-field") as Element,
         screen.getByRole("button", { name: CHECK_LABEL })
      ];
      const positions = stops.map(position);

      expect(positions.every((index) => index >= 0)).toBe(true);
      expect([...positions].sort((left, right) => left - right)).toEqual(positions);

      activate(screen.getByRole("link", { name: SKIP_TO_RESULT }));

      expect(document.activeElement).toBe(screen.getByLabelText(RESULT_LABEL));

      for (const key of "3.901") {
         press(key);
      }

      tabTo(document.querySelector("math-field") as HTMLElement);
      press("7");
      tabTo(screen.getByLabelText(RESULT_LABEL));
      press("Enter");
      await settle();

      expect(mocked.answerCalculatorDrill.mock.calls[0][1]).toMatchObject({ value: "3.901", setup_mathjson: 7 });
      expect(document.activeElement).toBe(screen.getByTestId("drill-result-line"));

      activate(screen.getByRole("button", { name: NEXT_LABEL }));
      await settle();

      expect(mocked.startCalculatorDrill).toHaveBeenCalledTimes(2);
      expect(document.activeElement).toBe(screen.getByTestId("drill-task"));
      expect(pointerEvents).toEqual([]);
   });
});
