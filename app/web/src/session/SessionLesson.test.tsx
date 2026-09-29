import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import type { LessonMarks, ServedItem, ServedLesson, SessionPayload } from "../api/types";
import * as client from "../api/client";
import { LESSON, planFor } from "../lessons/fixtures";
import { END_OF_SESSION_LESSON } from "../lessons/LessonReader";
import { REDUCED_MOTION_QUERY } from "../styles/motion";
import { SessionScreen } from "./SessionScreen";

vi.mock("../api/client");

const mocked = vi.mocked(client);

/* 15 UI, the session lesson state: GET /sessions/{id}/next serves a lesson slot (entry.kind), the
   reader runs in the session context, and completing or skipping it posts the session lesson
   event and brings the item the lesson went before. */

const SECTIONS = ["LSN-CON-02013#s1", "LSN-CON-02013#s2", "LSN-CON-02013#s5"];

const session: SessionPayload = {
   id: "session-lesson",
   mode: "learning",
   sub_mode: null,
   started_at: "2027-01-05T09:00:00Z",
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

function servedLesson(kind: "lesson" | "refresher" = "lesson"): ServedLesson {
   const reason = kind === "lesson" ? "first_contact" : "T2";

   return {
      kind,
      lesson_id: LESSON.id,
      version: 1,
      band: "low",
      reason,
      concept_id: "BC-CON-02013",
      concept_name: "the product rule",
      before_item_id: "item-example",
      minutes: 4,
      plan: planFor(SECTIONS, [], reason),
      lesson: LESSON
   };
}

const exampleItem: ServedItem & LessonMarks = {
   id: "item-example",
   archetype_id: "BC-QA-02008",
   variant_id: null,
   snapshot_id: null,
   parameter_draw: null,
   stem: "Differentiate f(x) = x^2 sin(x)",
   figure_spec: null,
   options: null,
   calculator_status: null,
   representation: null,
   difficulty_settings: null,
   skills: ["BC-SKL-02036"],
   status: "published",
   stage: "example",
   format: "short_answer",
   is_probe: false,
   kind: "item",
   preceded_by_lesson_id: LESSON.id,
   preceded_by_lesson_version: 1,
   served_steps: [{ index: 1, text: "Name the factors: u = x^2, v = sin(x)" }],
   self_explanation_prompt: null
};

function serveLessonThenItem(lesson: ServedLesson) {
   mocked.openSession.mockResolvedValue(session);
   mocked.readSession.mockResolvedValue(session);
   mocked.readNextItem.mockResolvedValueOnce({ item: lesson }).mockResolvedValueOnce({ item: exampleItem });
   mocked.postSessionLessonEvent.mockResolvedValue({ ok: true, state: null });
}

function lessonEvents() {
   return mocked.postSessionLessonEvent.mock.calls.map(([sessionId, lessonId, body]) => ({ sessionId, lessonId, ...body }));
}

let reducedMotion = false;

beforeEach(() => {
   vi.resetAllMocks();
   reducedMotion = false;
   window.matchMedia = vi.fn().mockImplementation((query: string) => ({
      matches: query === REDUCED_MOTION_QUERY ? reducedMotion : false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn()
   }));
});

afterEach(() => {
   cleanup();
});

describe("SessionScreen lesson state", () => {
   it("renders the lesson before its item, and the item follows on complete", async () => {
      serveLessonThenItem(servedLesson());
      render(<SessionScreen resumeSessionId={null} />);

      await screen.findByTestId("lesson-reader");

      expect(screen.getByTestId("lesson-top-bar").textContent).toBe("Before the first problem on the product rule. About 4 minutes.");
      expect(screen.queryByText(exampleItem.stem)).toBeNull();

      for (let part = 0; part < SECTIONS.length; part += 1) {
         fireEvent.click(screen.getByTestId("lesson-next"));
      }

      expect(screen.getByTestId("lesson-end").textContent).toBe(END_OF_SESSION_LESSON);
      fireEvent.click(screen.getByTestId("lesson-finish"));

      await screen.findByText(exampleItem.stem);

      const events = lessonEvents();
      const viewed = events.filter((event) => event.event === "section_viewed");

      expect(events[0]).toMatchObject({ sessionId: session.id, lessonId: LESSON.id, event: "opened", band: "low", reason: "first_contact" });
      expect(viewed.map((event) => event.section_id)).toEqual(SECTIONS);
      expect(viewed.every((event) => typeof event.mode === "string" && event.elapsed_ms >= 0)).toBe(true);
      expect(events[events.length - 1]).toMatchObject({ event: "completed", band: "low", reason: "first_contact" });
      expect(mocked.readNextItem).toHaveBeenCalledTimes(2);
   });

   it("skip logs the section index it left from and the item follows", async () => {
      serveLessonThenItem(servedLesson());
      render(<SessionScreen resumeSessionId={null} />);

      await screen.findByTestId("lesson-reader");
      fireEvent.click(screen.getByTestId("lesson-next"));
      fireEvent.click(screen.getByTestId("lesson-skip"));

      await screen.findByText(exampleItem.stem);

      const skipped = lessonEvents().find((event) => event.event === "skipped");

      expect(skipped).toMatchObject({ section_id: SECTIONS[1], reason: "first_contact" });
   });

   it("reads a refresher in one panel under its own top bar", async () => {
      serveLessonThenItem(servedLesson("refresher"));
      render(<SessionScreen resumeSessionId={null} />);

      await screen.findByTestId("refresher-panel");

      expect(screen.getByTestId("lesson-top-bar").textContent).toBe("Before the next problem on the product rule. About a minute.");
      fireEvent.click(screen.getByTestId("refresher-back"));

      await screen.findByText(exampleItem.stem);
      expect(lessonEvents().some((event) => event.event === "completed" && event.reason === "T2")).toBe(true);
   });

   it("runs the lesson to its item with the keyboard alone", async () => {
      serveLessonThenItem(servedLesson());
      render(<SessionScreen resumeSessionId={null} />);

      await screen.findByTestId("lesson-reader");

      const pointer: string[] = [];
      const record = (event: Event) => pointer.push(event.type);

      for (const type of ["pointerdown", "mousedown", "touchstart"]) {
         document.addEventListener(type, record, true);
      }

      /* Tab reaches a native button and Enter activates it: the browser turns that key into the
         click jsdom does not, so the driver dispatches it after the key. */
      function pressEnterOn(testId: string) {
         const control = screen.getByTestId(testId);

         control.focus();
         expect(document.activeElement).toBe(control);
         expect(control.tagName).toBe("BUTTON");
         fireEvent.keyDown(control, { key: "Enter" });
         fireEvent.click(control);
      }

      for (let part = 0; part < SECTIONS.length; part += 1) {
         pressEnterOn("lesson-next");
      }

      pressEnterOn("lesson-finish");
      await screen.findByText(exampleItem.stem);

      for (const type of ["pointerdown", "mousedown", "touchstart"]) {
         document.removeEventListener(type, record, true);
      }

      expect(pointer).toEqual([]);
   });

   it("under reduced motion the lesson still pages one part per screen with no motion class on its screen", async () => {
      reducedMotion = true;
      serveLessonThenItem(servedLesson());
      render(<SessionScreen resumeSessionId={null} />);

      await screen.findByTestId("lesson-reader");

      expect(screen.getByTestId("lesson-part").textContent).toBe(`Part 1 of ${SECTIONS.length + 1}`);
      expect(screen.getByTestId("lesson-screen").className).not.toMatch(/motion-/);
      fireEvent.click(screen.getByTestId("lesson-next"));
      expect(screen.getByTestId("lesson-part").textContent).toBe(`Part 2 of ${SECTIONS.length + 1}`);
      fireEvent.click(screen.getByTestId("lesson-skip"));

      await waitFor(() => expect(screen.getByText(exampleItem.stem)).toBeTruthy());
   });
});
