import { readFileSync } from "node:fs";
import { resolve } from "node:path";

import { act, cleanup, render, screen } from "@testing-library/react";
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
import { LESSON } from "./fixtures";
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
   const hasInput = screenElement.querySelector("math-field, input[type='radio']") !== null;

   if (isCheck && !hasInput) {
      failures.push(`${where}: the check has no input control`);
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

/* Works the current screen with the keyboard alone: every step revealed, a motion block stepped
   to its last frame, a control moved, a model run to its last row, a check answered. */
async function workScreen() {
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
         />
      </main>
   );

   for (let guard = 0; guard < 200 && screen.queryByTestId("lesson-next") !== null; guard += 1) {
      const where = `${band} ${screen.getByTestId("lesson-screen").getAttribute("data-section-id")}`;

      seen.push(where);
      failures.push(...screenFailures(where));
      await workScreen();
      failures.push(...screenFailures(`${where}, worked`));
      activate(screen.getByTestId("lesson-next"));
   }

   failures.push(...screenFailures(`${band} end`));

   expect(screen.getByTestId("lesson-screen").getAttribute("data-screen-kind")).toBe("end");

   return { failures, seen, plan };
}

function readRecord(): LessonRecord {
   return JSON.parse(readFileSync(resolve(WEB_ROOT, RECORD_PATH), "utf8")) as LessonRecord;
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

describe.each(["low", "mid"] as LessonBand[])(`render harness, ${RECORD_PATH}, band %s`, (band) => {
   it("renders every section and check of the band keyboard only, with nothing blank, unlabelled, dashed or without its control", async () => {
      const lesson = readRecord();
      const { failures, seen, plan } = await walk(lesson, band);

      expect(failures).toEqual([]);
      expect(seen.length).toBe(plan.sections.length + (lesson.kind === "decision" ? 1 : 0));
      expect(pointerEvents).toEqual([]);
   });
});

describe.each(["low", "mid"] as LessonBand[])("render harness, the reader fixture with every drawn mode, band %s", (band) => {
   it("walks every mode block with nothing blank", async () => {
      const { failures } = await walk({ ...LESSON, sections: LESSON.sections.map((section) => ({ ...section, bands: section.bands ?? ["low", "mid"] })) }, band);

      expect(failures).toEqual([]);
      expect(pointerEvents).toEqual([]);
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
