import { act, cleanup, fireEvent, screen, waitFor, within } from "@testing-library/react";
import type { ReactElement } from "react";
import { afterAll, afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import * as client from "../api/client";
import type { ExperimentState, MasteryNodeState, TutorFigurePrimitive, TutorFigureRole } from "../api/types";
import { SECANT_TO_TANGENT, TABLE_OF_VALUES, figureCell, figureDot, figurePath } from "../agent/figureFixtures";
import { TutorFigure } from "../agent/TutorFigure";
import { multipleChoiceQuestion, noCalculatorPart } from "../assessment/fixtures";
import { FigureView } from "../figures/FigureView";
import { ReadBackView } from "../frq/ReadBack";
import { GradingView } from "../frq/GradingView";
import { McqControl } from "../input/McqControl";
import { CalibrationCurve } from "../progress/CalibrationCurve";
import { NodeMark } from "../progress/MasteryMap";
import { ProvisionalPoints } from "../review/ProvisionalPoints";
import { ConfidencePrompt } from "../session/ConfidencePrompt";
import { StepMarks } from "../session/StepMarks";
import { LessonTable } from "../lessons/LessonTable";
import { LessonLibrary } from "../progress/LessonLibrary";
import { OperatorSettings } from "../settings/ExperimentsSection";
import { SettingsScreen } from "../settings/SettingsScreen";
import { DESKTOP_WIDTH, VIEWPORT_WIDTHS, colourlessDeclarations, isSvgElement, resolvedSvgPaint, setViewportWidth } from "../testing/cascade";
import {
   CALIBRATION,
   EVERY_STEP_MARK,
   FUNCTION_GRAPH,
   READ_BACK,
   gradings,
   inPage,
   partRunner,
   sessionFeedback,
   workedQuestion
} from "../testing/screens";

vi.mock("../api/client");

const mocked = vi.mocked(client);

/* 11's P8 eval eval_greyscale_states: no state a screen shows is lost when colour is removed. Each
   state is rendered, and what is left once every colour property is ignored is written out: the
   text a reader sees, each element's non-colour declarations from app.css and its inline style,
   whether an input is checked, an SVG shape's geometry, and whether a mark is inked, left as
   ground, or unpainted. Hue and lightness are gone from that description, so two states whose
   descriptions match differ by colour alone and fail. Text a sighted reader never sees, under
   .visually-hidden or KaTeX's hidden MathML, is left out, as are ARIA attributes, class names
   and data attributes, which are not drawn. Every state is read at a desktop and a phone width,
   each matching only the @media rules of app.css that hold there. */

const GROUND_TOKENS = /^(surface-|accent-tint-)/;

const GEOMETRY = ["x", "y", "x1", "y1", "x2", "y2", "cx", "cy", "r", "width", "height", "points", "d", "viewBox", "transform"];

function inkOf(element: Element, property: "fill" | "stroke") {
   const paint = resolvedSvgPaint(element, property);

   if (paint === null) {
      return "none";
   }

   return GROUND_TOKENS.test(paint.token) ? "ground" : "ink";
}

function colourless(node: Node): string {
   if (node.nodeType === Node.TEXT_NODE) {
      const text = (node.textContent ?? "").trim();

      return text === "" ? "" : JSON.stringify(text);
   }

   if (node.nodeType !== Node.ELEMENT_NODE) {
      return "";
   }

   const element = node as Element;
   const isUnseen = element.matches(".visually-hidden, .katex-mathml, title, desc, [hidden]");

   if (isUnseen) {
      return "";
   }

   const facts = [element.tagName.toLowerCase(), ...colourlessDeclarations(element)];

   if (isSvgElement(element)) {
      facts.push(...GEOMETRY.map((name) => `${name}=${element.getAttribute(name) ?? ""}`));
      facts.push(`fill=${inkOf(element, "fill")}`, `stroke=${inkOf(element, "stroke")}`);
   }

   if (element instanceof HTMLInputElement) {
      facts.push(`type=${element.type}`, `checked=${element.checked}`, `value=${element.value}`);
   }

   const children = Array.from(element.childNodes).map(colourless).filter((child) => child !== "");

   return `<${facts.join(" ")}>${children.join("")}</>`;
}

/* The pairs of states, by name, whose colourless descriptions are the same. */
function indistinct(states: Record<string, string>) {
   const names = Object.keys(states);
   const same: string[] = [];

   for (const [index, first] of names.entries()) {
      for (const second of names.slice(index + 1)) {
         if (states[first] === states[second]) {
            same.push(`${first} and ${second}`);
         }
      }
   }

   return same;
}

function expectDistinct(states: Record<string, string>) {
   expect(Object.keys(states).length).toBeGreaterThan(1);
   expect(Object.values(states).every((description) => description.length > 0)).toBe(true);
   expect(indistinct(states)).toEqual([]);
}

function described(content: ReactElement, pick: (container: HTMLElement) => Element = (container) => container) {
   const container = inPage(content);
   const description = colourless(pick(container));

   cleanup();

   return description;
}

afterEach(() => {
   cleanup();
});

describe.each(VIEWPORT_WIDTHS)("eval_greyscale_states at %i px", (width) => {
   beforeEach(() => {
      setViewportWidth(width);
   });

   afterAll(() => {
      setViewportWidth(DESKTOP_WIDTH);
   });

   it("tells two states apart that differ only in colour, and not two that differ in text", () => {
      const red = described(<p style={{ color: "var(--growth-state-incorrect)" }}>Checked</p>);
      const green = described(<p style={{ color: "var(--growth-state-correct)" }}>Checked</p>);
      const worded = described(<p style={{ color: "var(--growth-state-correct)" }}>Correct</p>);

      expect(indistinct({ red, green })).toEqual(["red and green"]);
      expect(indistinct({ red, worded })).toEqual([]);
   });

   it("a feedback step reads as given, correct, not yet or unmarked without colour", () => {
      const states = Object.fromEntries(
         EVERY_STEP_MARK.map((mark) => [
            mark.given ? "given" : String(mark.correct),
            described(<StepMarks marks={[{ ...mark, index: 1, text: "the same step" }]} />)
         ])
      );

      expectDistinct(states);
   });

   it("a lesson table's current, marked and plain rows, and the library's row states, read without colour", () => {
      const table = { kind: "table", columns: ["h", "rate"], rows: [["1", "11"], ["1", "11"], ["1", "11"]], marked_rows: [2] };
      const row = (index: number) => (container: HTMLElement) => container.querySelectorAll("tbody tr")[index];

      expectDistinct({
         current: described(<LessonTable spec={table} currentRow={0} />, row(0)),
         marked: described(<LessonTable spec={table} currentRow={0} />, row(1)),
         plain: described(<LessonTable spec={table} currentRow={0} />, row(2))
      });

      const concept = { concept_id: "BC-CON-02013", name: "The product rule", lesson_id: "LSN-CON-02013", version: 1, servable: true, read_at: null };
      const libraryRow = (state: "read" | "coming_up" | "bypassed_by_placement" | "unseen" | "not_available") =>
         described(
            <LessonLibrary
               library={{ units: [{ id: "BC-UNIT-02", name: "Unit 2", order: 2, concepts: [{ ...concept, state, read_at: state === "read" ? "2026-10-03" : null }] }] }}
               onOpenLesson={vi.fn()}
            />,
            (container) => container.querySelector("[data-testid='lesson-library-row']")!
         );

      expectDistinct({
         read: libraryRow("read"),
         comingUp: libraryRow("coming_up"),
         placed: libraryRow("bypassed_by_placement"),
         notRead: libraryRow("unseen"),
         notAvailable: libraryRow("not_available")
      });
   });

   it("a chosen answer option and a crossed-out option read without colour", () => {
      const options = [
         { id: "A", label: "First choice" },
         { id: "B", label: "Second choice" }
      ];
      const optionA = (container: HTMLElement) => container.querySelectorAll("label")[0];

      expectDistinct({
         selected: described(<McqControl groupLabel="Question 1" options={options} selectedId="A" onSelect={vi.fn()} />, optionA),
         unselected: described(<McqControl groupLabel="Question 1" options={options} selectedId={null} onSelect={vi.fn()} />, optionA)
      });

      const eliminator = (eliminated: string[]) => (
         <McqControl groupLabel="Question 1" options={options} onSelect={vi.fn()} eliminatedIds={eliminated} onToggleEliminated={vi.fn()} />
      );
      const firstOption = (container: HTMLElement) => container.querySelector("[data-testid='choice-option']")!;

      expectDistinct({ crossedOut: described(eliminator(["A"]), firstOption), open: described(eliminator([]), firstOption) });
   });

   it("the confidence chosen reads without colour", () => {
      const guess = (container: HTMLElement) => container.querySelector("label")!;

      expectDistinct({
         chosen: described(<ConfidencePrompt value="guess" onChange={vi.fn()} />, guess),
         notChosen: described(<ConfidencePrompt value="unsure" onChange={vi.fn()} />, guess)
      });
   });

   it("every mastery map state, the gap included, has its own shape", () => {
      const states: MasteryNodeState[] = ["mastered", "fading", "in_progress", "not_attempted", "gap"];

      expectDistinct(Object.fromEntries(states.map((state) => [state, described(<NodeMark state={state} />)])));
   });

   it("a figure's filled point and open point differ in shape, not only in colour", () => {
      const point = (type: string) =>
         described(<FigureView spec={{ ...FUNCTION_GRAPH, marks: [{ type, at: [1, 1] }] }} />, (container) => container.querySelector("circle")!);

      expectDistinct({ filled: point("point"), open: point("open_point") });
   });

   it("every role of the tutor's figure reads without colour, on a stroke and on a dot", () => {
      const roles: TutorFigureRole[] = ["given", "constructed", "highlight", "error"];
      const twoSteps = [
         { id: "one", caption: "One" },
         { id: "two", caption: "Two" }
      ];
      const drawing = (container: HTMLElement) => container.querySelector("svg")!;
      const drawnWith = (primitive: TutorFigurePrimitive) =>
         described(<TutorFigure spec={{ ...SECANT_TO_TANGENT, kind: "diagram", axes: null, grid: false, steps: twoSteps, primitives: [primitive] }} revealed={2} finished />, drawing);

      const strokes = Object.fromEntries(roles.map((role) => [role, drawnWith(figurePath("one", "m", role, [[-0.5, 1], [2, 6]]))]));
      const dots = Object.fromEntries(roles.map((role) => [role, drawnWith(figureDot("one", "m", role, [1, 1]))]));

      expectDistinct({ ...strokes, ghost: drawnWith(figurePath("one", "m", "constructed", [[-0.5, 1], [2, 6]], { faded_at: "two" })) });
      expectDistinct({ ...dots, ghost: drawnWith(figureDot("one", "m", "constructed", [1, 1], { faded_at: "two" })) });
   });

   it("a tutor table's highlighted, wrong, faded and plain cells read without colour", () => {
      const oneColumn = {
         ...TABLE_OF_VALUES,
         columns: ["\\(x\\)"],
         rows: [["1"], ["1"], ["1"], ["1"]],
         steps: [
            { id: "one", caption: "One" },
            { id: "two", caption: "Two" }
         ],
         primitives: [
            figureCell("one", "a", "highlight", 0, null),
            figureCell("one", "b", "error", 1, null),
            figureCell("one", "c", "highlight", 2, null, { faded_at: "two" })
         ]
      };
      const table = <TutorFigure spec={oneColumn} revealed={2} finished />;
      const cell = (row: number) => described(table, (container) => container.querySelectorAll("tbody td")[row]);

      expectDistinct({ highlighted: cell(0), wrong: cell(1), faded: cell(2), plain: cell(3) });
   });

   it("the calibration curve's observed point, its interval and an empty level read without colour", () => {
      const container = inPage(<CalibrationCurve calibration={CALIBRATION} />);
      const observed = container.querySelector("[data-testid='calibration-point']")!;

      expectDistinct({
         point: colourless(observed.querySelector("circle")!),
         interval: colourless(observed.querySelector("[data-testid='calibration-interval']")!)
      });
      expect(container.textContent).toContain("n = 0");
   });

   it("provisional and final grading points, and a disputed provisional point, read without colour", () => {
      const container = inPage(<GradingView gradings={gradings()} onAskForReread={vi.fn()} rereadAskedFor={[]} />);
      const [earned, notEarned, provisional] = within(container).getAllByTestId("graded-point").map((point) => colourless(point.querySelector("strong")!));

      expectDistinct({ earned, notEarned, provisional });
      cleanup();

      const point = { grading_id: "G-1", attempt_id: "ATT-1", label: "Question 1", point_label: "Answer", reason: "Two readings" };
      const row = (container: HTMLElement) => container.querySelector("[data-testid='provisional-point']")!;

      expectDistinct({
         disputed: described(<ProvisionalPoints points={[{ ...point, disputed: true }]} onAskForReread={vi.fn()} />, row),
         open: described(<ProvisionalPoints points={[{ ...point, disputed: false }]} onAskForReread={vi.fn()} />, row)
      });
   });

   it("a crossed-out line of the read-back reads without colour", () => {
      const line = (crossedOut: boolean) =>
         described(
            <ReadBackView
               readBack={{ ...READ_BACK, parts: [{ ...READ_BACK.parts[0], lines: [{ ...READ_BACK.parts[0].lines[1], crossed_out: crossedOut }] }] }}
            />,
            (container) => container.querySelector("li li, .read-back-lines > *")!
         );

      expectDistinct({ crossedOut: line(true), kept: line(false) });
   });

   it("a disabled primary action reads as disabled without colour", async () => {
      const container = await sessionFeedback("unsupported");
      const next = screen.getByRole("button", { name: "Next item" });
      const disabled = colourless(next);

      fireEvent.change(screen.getByLabelText("In one line, what went wrong?"), { target: { value: "I multiplied." } });

      expect(container.contains(next)).toBe(true);
      expectDistinct({ disabled, enabled: colourless(next) });
   });

   it("a disabled text button and a disabled destructive button read as disabled without colour", async () => {
      await partRunner(noCalculatorPart({ questions: [workedQuestion(), multipleChoiceQuestion(2)] }));

      const back = screen.getByRole("button", { name: "Back" });
      const disabledBack = colourless(back);

      fireEvent.click(screen.getByRole("button", { name: "Next" }));

      expectDistinct({ disabled: disabledBack, enabled: colourless(back) });
      cleanup();

      inPage(
         <SettingsScreen
            tab="data"
            providers={null}
            budgets={null}
            onCapChange={vi.fn()}
            queueSettings={null}
            onSettingsChange={vi.fn()}
            onExport={vi.fn()}
            purgeConfirmationPhrase="delete my data"
            onReauthenticate={vi.fn().mockResolvedValue(true)}
            onPurge={vi.fn()}
         />
      );

      const purge = screen.getByRole("button", { name: "purge everything" });
      const disabledPurge = colourless(purge);

      fireEvent.change(screen.getByLabelText(/to confirm/), { target: { value: "delete my data" } });
      fireEvent.click(screen.getByRole("button", { name: "verify identity" }));
      await waitFor(() => expect(purge.hasAttribute("disabled")).toBe(false));

      expectDistinct({ disabled: disabledPurge, enabled: colourless(purge) });
   });

   it("keyboard focus reads without colour", async () => {
      await partRunner(noCalculatorPart({ questions: [workedQuestion(), multipleChoiceQuestion(2)] }));

      const submit = screen.getByRole("button", { name: "Submit part" });
      const unfocused = colourless(submit);

      act(() => submit.focus());

      expectDistinct({ focused: colourless(submit), unfocused });
   });

   it("the pressed zoom step, the current question and the timer shown or hidden read without colour", async () => {
      await partRunner(noCalculatorPart({ questions: [workedQuestion(), multipleChoiceQuestion(2)] }));

      const hundred = screen.getByRole("button", { name: "100 percent" });
      const pressed = colourless(hundred);
      const entry = () => screen.getAllByTestId("question-menu-entry")[0];
      const current = colourless(entry());
      const timer = () => colourless(screen.getByText(/Hide timer|Show timer/).parentElement!);
      const timerShown = timer();

      fireEvent.click(screen.getByRole("button", { name: "125 percent" }));
      fireEvent.click(entry());
      fireEvent.click(screen.getByRole("button", { name: "Question menu" }));
      fireEvent.click(screen.getAllByTestId("question-menu-entry")[1]);
      fireEvent.click(screen.getByRole("button", { name: "Question menu" }));
      fireEvent.click(screen.getByRole("button", { name: "Hide timer" }));

      expectDistinct({ pressed, notPressed: colourless(hundred) });
      expectDistinct({ current, notCurrent: colourless(entry()) });
      expectDistinct({ timerShown, timerHidden: timer() });
   });

   it("a question tile reads answered, unanswered and marked for review without colour", async () => {
      const answered = { ...workedQuestion(), number: 2, marked: false };
      const markedUnanswered = { ...multipleChoiceQuestion(4), marked: true };

      await partRunner(noCalculatorPart({ questions: [workedQuestion(), answered, multipleChoiceQuestion(3), markedUnanswered] }));

      const tile = (index: number) => colourless(screen.getAllByTestId("question-menu-entry")[index].parentElement!).replace(/"\d+"/g, "\"N\"");

      expectDistinct({ answered: tile(1), unanswered: tile(2), markedForReview: tile(3) });
   });

   it("which experiment arm is on reads without colour", async () => {
      async function onButton(state: ExperimentState) {
         mocked.readExperiments.mockResolvedValue({
            experiments: [
               {
                  name: "worked_example_fading",
                  description: "Fade worked steps.",
                  unit: "skill",
                  arms: ["control", "treatment"],
                  state,
                  randomised_from: null,
                  assigned_units: { control: 3, treatment: 4 }
               }
            ]
         });

         inPage(<OperatorSettings onOpenEvidence={vi.fn()} />);

         const button = await screen.findByRole("button", { name: "on" });
         const description = colourless(button);

         cleanup();

         return description;
      }

      expectDistinct({ selected: await onButton("on"), notSelected: await onButton("off") });
   });
});
