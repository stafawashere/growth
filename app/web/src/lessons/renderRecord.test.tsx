import { readdirSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";

import { act, cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest";

import type { LessonBand, LessonCheck, LessonPlan, LessonRecord, LessonSection, LessonSectionRef } from "../api/types";
import {
   activate,
   defineKeyboardMathField,
   pointerEvents,
   press,
   startRecordingPointer,
   stopRecordingPointer,
   tabTo
} from "../testing/keyboard";
import { ERROR_ID, FADED_EXAMPLE_ID, LESSON, PREDICTION_ID } from "./fixtures";
import { LessonReader } from "./LessonReader";
import { DRAWN_MODES } from "./LessonSection";

/* The per-record render harness later lesson workers run:

      LESSON_RECORD=../../content/lessons/LSN-CON-06004.json npx vitest run src/lessons/renderRecord.test.tsx

   LESSON_RECORD is a path relative to app/web (default ../../content/lessons/LSN-CON-02013.json).
   For each band the harness builds the plan the plan endpoint would serve at first contact
   (app/lessons/plan.py first_contact_refs: every section in band order with the checks where the
   plan puts them, with every prerequisite bridge taken as needed so every section is rendered, and
   without the word fit, which only drops sections), renders it through LessonReader in the library
   context, and walks every screen with the keyboard alone. It fails on a drawn block that renders
   blank, a delivery mode that needs a spec with none present, a figure label outside its plot, a
   check without an input control, or any served text carrying an em dash or an en dash. The same
   walk runs over the reader's own fixture, which carries one block of every drawn mode. */

const RECORD_PATH = process.env.LESSON_RECORD ?? "../../content/lessons/LSN-CON-02013.json";

/* LESSON_RECORD_DIR, relative to app/web like LESSON_RECORD, walks every record in a directory in
   one run instead of one record per run. */
const RECORD_DIR = process.env.LESSON_RECORD_DIR;

const WEB_ROOT = resolve(__dirname, "..", "..");

const LOW_ERRORS_MAX = 4;

const MID_ERRORS = 2;

const LOW_CHECKS_MAX = 3;

const MID_CHECKS = 2;

const LOW_EXAMPLES_MAX = 2;

const CHARACTER_WIDTH = 8;

const DASHES = /[\u2013\u2014]/;

const SPEC_MODES = [...DRAWN_MODES, "contrast"];

function inBand(record: { bands?: string[] }, band: LessonBand) {
   return record.bands === undefined || record.bands.includes(band);
}

function firstContactPlan(lesson: LessonRecord, band: LessonBand): LessonPlan {
   const ofType = (type: LessonSection["type"], filtered = true) =>
      lesson.sections.filter((section) => section.type === type && (!filtered || inBand(section, band)));
   const isLow = band === "low";
   const keyIdeas = ofType("key_ideas").filter((section) => isLow || section.depth === "core");
   const strategies = isLow ? ofType("strategy") : ofType("strategy").slice(0, 1);
   const examples = ofType("worked_example").slice(0, isLow ? LOW_EXAMPLES_MAX : 1);
   const errors = ofType("common_error").slice(0, isLow ? LOW_ERRORS_MAX : MID_ERRORS);
   const checks = lesson.checks.filter((check) => inBand(check, band)).slice(0, isLow ? LOW_CHECKS_MAX : MID_CHECKS);
   const scoresFor = (example: LessonSection) => ofType("what_a_reader_scores", false).filter((section) => section.example_id === example.id);
   const sequence: Array<LessonSection | LessonCheck> = [
      ...ofType("prediction"),
      ...ofType("orientation"),
      ...ofType("prerequisite_bridge", false),
      ...keyIdeas,
      ...strategies
   ];

   for (const example of examples.slice(0, 1)) {
      sequence.push(example, ...scoresFor(example));
   }

   sequence.push(...errors, ...checks.slice(0, 1));

   for (const example of examples.slice(1, 2)) {
      sequence.push(example, ...scoresFor(example));
   }

   sequence.push(...checks.slice(1, 2), ...ofType("representations"), ...checks.slice(2));

   const refs: LessonSectionRef[] = sequence.map((entry) => ({
      id: entry.id,
      type: "type" in entry ? entry.type : "check",
      form: "full"
   }));

   return {
      lesson_id: lesson.id,
      version: lesson.version,
      band,
      reason: "first_contact",
      sections: refs,
      checks: checks.map((check) => check.id),
      minutes: lesson.read_minutes[isLow ? "full" : "brief"],
      words: lesson.word_count[isLow ? "full" : "brief"],
      anchors: []
   };
}

/* A delivery mode that draws needs its spec; one without is a record error the reader would cover
   with the fallback, so the harness names it rather than letting the fallback hide it. */
function specFailures(lesson: LessonRecord) {
   const deliveries = [
      ...lesson.sections.map((section) => ({ where: section.id, delivery: section.delivery })),
      ...(lesson.decision === undefined ? [] : [{ where: `${lesson.id} decision stems`, delivery: lesson.decision.delivery }])
   ];

   return deliveries
      .filter((entry) => entry.delivery !== undefined && SPEC_MODES.includes(entry.delivery.mode) && entry.delivery.spec === undefined)
      .map((entry) => `${entry.where}: mode ${entry.delivery!.mode} carries no spec`);
}

function screenFailures(where: string): string[] {
   const failures: string[] = [];
   const screenElement = screen.getByTestId("lesson-screen");

   for (const block of Array.from(screenElement.querySelectorAll("[data-testid='lesson-delivery']"))) {
      const hasDrawing = block.querySelector("svg, table") !== null;
      const fallback = block.querySelector("[data-testid='lesson-figure-fallback']");
      const hasFallbackText = fallback !== null && (fallback.textContent ?? "").trim() !== "";

      if (!hasDrawing && !hasFallbackText) {
         failures.push(`${where}: the ${block.getAttribute("data-mode")} block renders blank`);
      }
   }

   for (const svg of Array.from(screenElement.querySelectorAll("svg[data-testid='figure-graph']"))) {
      const [, , width, height] = (svg.getAttribute("viewBox") ?? "0 0 0 0").split(" ").map(Number);

      for (const label of Array.from(svg.querySelectorAll("text.figure-label"))) {
         const x = Number(label.getAttribute("x"));
         const y = Number(label.getAttribute("y"));
         const right = x + (label.textContent ?? "").length * CHARACTER_WIDTH;
         const isInside = x >= 0 && y >= 0 && y <= height && right <= width;

         if (!isInside) {
            failures.push(`${where}: label "${label.textContent}" sits outside the plot`);
         }
      }
   }

   const isCheck = screenElement.getAttribute("data-screen-kind") === "check";
   const prediction = screenElement.querySelector("[data-testid='lesson-prediction']");
   const hasInput = screenElement.querySelector("math-field, input[type='radio']") !== null;

   if (isCheck && !hasInput) {
      failures.push(`${where}: the check has no input control`);
   }

   if (prediction !== null && prediction.querySelector("math-field, input[type='radio']") === null) {
      failures.push(`${where}: the prediction has no input control`);
   }

   if (DASHES.test(document.body.textContent ?? "")) {
      failures.push(`${where}: served text carries an em dash or an en dash`);
   }

   return failures;
}

async function settle() {
   await act(async () => {
      await Promise.resolve();
   });
}

function typeKeys(text: string) {
   for (const key of text) {
      press(key);
   }
}

/* The key option is chosen with the arrow keys; a short answer key is typed when it is a number,
   and any other key stands in as 1, since the harness mocks the grading. */
function answerPrediction(section: LessonSection) {
   const radios = Array.from(document.querySelectorAll("[data-testid='lesson-prediction'] input[type='radio']")) as HTMLInputElement[];
   const field = document.querySelector("[data-testid='lesson-prediction'] math-field") as HTMLElement | null;

   if (radios.length > 0) {
      const keyId = (section.options ?? []).find((option) => option.is_key)?.id ?? radios[0].value;

      tabTo(radios[0]);
      press(" ");

      for (let moved = 0; moved < radios.length && (document.activeElement as HTMLInputElement).value !== keyId; moved += 1) {
         press("ArrowDown");
      }
   } else if (field !== null) {
      const key = section.answer_key?.mathjson;

      tabTo(field);
      typeKeys(typeof key === "number" ? String(key) : "1");
   }
}

async function answerPrompt(promptTestId: string, submit: () => HTMLElement | null) {
   const prompt = screen.queryByTestId(promptTestId);
   const field = prompt?.querySelector("math-field") as HTMLElement | null | undefined;

   if (field === null || field === undefined) {
      return;
   }

   tabTo(field);
   press("1");

   const button = submit() as HTMLButtonElement | null;

   if (button !== null && !button.disabled) {
      activate(button);
      await settle();
   }
}

/* Works the current screen with the keyboard alone: the prediction committed, a fix prompt and a
   faded example answered, every step revealed, a motion block stepped to its last frame, a
   control moved, a model run to its last row, a check answered. */
async function workScreen(lesson: LessonRecord) {
   const sectionId = screen.getByTestId("lesson-screen").getAttribute("data-section-id");
   const section = lesson.sections.find((entry) => entry.id === sectionId);

   if (section?.type === "prediction" && screen.queryByTestId("lesson-prediction-commit") !== null) {
      answerPrediction(section);

      const commit = screen.getByTestId("lesson-prediction-commit") as HTMLButtonElement;

      if (!commit.disabled) {
         activate(commit);
         await settle();
      }
   }

   await answerPrompt("lesson-fix-prompt", () => screen.queryByTestId("lesson-fix-submit"));
   await answerPrompt("lesson-fade-answer", () => {
      const fade = screen.queryByTestId("lesson-fade-answer");

      return fade === null ? null : within(fade).queryByRole("button", { name: "Check my answer" });
   });

   if (screen.queryByTestId("lesson-show-all-steps") !== null) {
      activate(screen.getByTestId("lesson-show-all-steps"));
   }

   while (screen.queryByTestId("lesson-next-step") !== null) {
      activate(screen.getByTestId("lesson-next-step"));
   }

   const stepper = screen.queryByTestId("frame-stepper");

   if (stepper !== null) {
      tabTo(stepper);
      press("End");
   }

   const control = screen.queryByTestId("figure-control");

   if (control !== null) {
      tabTo(control);
      press("ArrowRight");
   }

   let run = screen.queryByTestId("model-run") as HTMLButtonElement | null;

   while (run !== null && !run.disabled) {
      activate(run);
      run = screen.queryByTestId("model-run") as HTMLButtonElement | null;
   }

   if (screen.getByTestId("lesson-screen").getAttribute("data-screen-kind") === "check") {
      const field = document.querySelector("math-field") as HTMLElement | null;
      const radio = document.querySelector("input[type='radio']") as HTMLElement | null;

      if (field !== null) {
         tabTo(field);
         press("1");
      } else if (radio !== null) {
         tabTo(radio);
         press(" ");
      }

      const submit = screen.queryByTestId("lesson-check-submit") as HTMLButtonElement | null;

      if (submit !== null && !submit.disabled) {
         activate(submit);
         await settle();
      }
   }
}

async function walk(lesson: LessonRecord, band: LessonBand) {
   const plan = firstContactPlan(lesson, band);
   const firstError = lesson.sections.find((section) => section.type === "common_error");
   const onCheckAnswer = vi.fn().mockResolvedValue({
      correct: false,
      error_id: firstError?.error_id ?? null,
      anchor: firstError?.id ?? null,
      explanation_anchor: null
   });
   const onPromptAnswer = vi.fn().mockImplementation(async (sectionId: string) => ({ correct: false, section_id: sectionId, kind: "fade", resolution: null }));
   const failures: string[] = [...specFailures(lesson)];
   const seen: string[] = [];

   render(
      <main className="app-page">
         <LessonReader
            lesson={lesson}
            plan={plan}
            band={band}
            context="library"
            conceptName={lesson.target_id}
            onComplete={vi.fn()}
            onSkip={vi.fn()}
            onSectionViewed={vi.fn()}
            onCheckAnswer={onCheckAnswer}
            onPromptAnswer={onPromptAnswer}
         />
      </main>
   );

   for (let guard = 0; guard < 200 && screen.queryByTestId("lesson-finish") === null; guard += 1) {
      const where = `${band} ${screen.getByTestId("lesson-screen").getAttribute("data-section-id")}`;

      seen.push(where);
      failures.push(...screenFailures(where));
      await workScreen(lesson);
      failures.push(...screenFailures(`${where}, worked`));

      const next = screen.queryByTestId("lesson-next") as HTMLButtonElement | null;
      const canLeave = next !== null && !next.disabled;

      if (!canLeave) {
         failures.push(`${where}: Next part is not available after the screen was worked`);
         break;
      }

      activate(next);
   }

   const reachedEnd = screen.getByTestId("lesson-screen").getAttribute("data-screen-kind") === "end";

   if (reachedEnd) {
      failures.push(...screenFailures(`${band} end`));
   } else {
      failures.push(`${band}: the walk did not reach the end screen`);
   }

   return { failures, seen, plan, onPromptAnswer };
}

function recordPaths(): string[] {
   if (RECORD_DIR === undefined) {
      return [RECORD_PATH];
   }

   const names = readdirSync(resolve(WEB_ROOT, RECORD_DIR)).filter((name) => name.endsWith(".json"));

   return names.sort().map((name) => join(RECORD_DIR, name));
}

function readRecord(path: string): LessonRecord {
   return JSON.parse(readFileSync(resolve(WEB_ROOT, path), "utf8")) as LessonRecord;
}

const RECORD_CASES = recordPaths().flatMap((path) => (["low", "mid"] as LessonBand[]).map((band) => [path, band] as const));

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

describe.each(RECORD_CASES)("render harness, %s, band %s", (path, band) => {
   it("renders every section and check of the band keyboard only, with nothing blank, unlabelled, dashed or without its control", async () => {
      const lesson = readRecord(path);
      const { failures, seen, plan } = await walk(lesson, band);

      expect(failures).toEqual([]);
      expect(seen.length).toBe(plan.sections.length + (lesson.kind === "decision" ? 1 : 0));
      expect(pointerEvents).toEqual([]);
   });
});

describe.each(["low", "mid"] as LessonBand[])("render harness, the reader fixture with every drawn mode, band %s", (band) => {
   it("walks every mode block and every v2 prompt with nothing blank", async () => {
      const { failures, onPromptAnswer } = await walk({ ...LESSON, sections: LESSON.sections.map((section) => ({ ...section, bands: section.bands ?? ["low", "mid"] })) }, band);
      const answered = onPromptAnswer.mock.calls.map((call) => call[0]);

      expect(failures).toEqual([]);
      expect(answered).toEqual(band === "low" ? [PREDICTION_ID, ERROR_ID, FADED_EXAMPLE_ID] : [PREDICTION_ID, ERROR_ID]);
      expect(onPromptAnswer.mock.calls[0][1]).toMatchObject({ option_id: "B" });
      expect(pointerEvents).toEqual([]);
   });

   it("names a prediction the walk could not commit", async () => {
      const unanswerable: LessonRecord = {
         ...LESSON,
         sections: LESSON.sections.map((section) => (section.id === PREDICTION_ID ? { ...section, options: [] } : section))
      };
      const { failures } = await walk(unanswerable, band);

      expect(failures).toContain(`${band} ${PREDICTION_ID}: the prediction has no input control`);
      expect(failures).toContain(`${band} ${PREDICTION_ID}: Next part is not available after the screen was worked`);
      expect(failures).toContain(`${band}: the walk did not reach the end screen`);
   });

   it("names a drawn mode that carries no spec", async () => {
      const broken: LessonRecord = {
         ...LESSON,
         sections: [...LESSON.sections, { id: "LSN-CON-02013#r-nospec", type: "representations", text: "A table.", delivery: { mode: "table", reason: "rule 5" } }]
      };
      const { failures } = await walk(broken, band);

      expect(failures).toContain("LSN-CON-02013#r-nospec: mode table carries no spec");
   });
});
