import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import * as client from "../api/client";
import { LESSON, planFor } from "./fixtures";
import { LessonRoute } from "./LessonRoute";

vi.mock("../api/client");

const mocked = vi.mocked(client);

async function settle() {
   await act(async () => {
      await Promise.resolve();
   });
}

afterEach(() => {
   cleanup();
   vi.clearAllMocks();
});

describe("LessonRoute, the library reader", () => {
   it("reads the full lesson for the low band, posts library events and returns to progress when done", async () => {
      mocked.readLessonPlan.mockResolvedValue({ lesson: LESSON, plan: planFor(["LSN-CON-02013#s1", "LSN-CON-02013#s2"]), band: "low", state: null });
      mocked.postLessonEvent.mockResolvedValue({ ok: true, state: null });

      const onLeave = vi.fn();

      render(<LessonRoute lessonId="LSN-CON-02013" conceptName="The product rule" onLeave={onLeave} />);

      await screen.findByTestId("lesson-reader");

      expect(mocked.readLessonPlan).toHaveBeenCalledWith("LSN-CON-02013", "low", "first_contact");
      expect(mocked.postLessonEvent).toHaveBeenCalledWith("LSN-CON-02013", expect.objectContaining({ event: "opened", band: "low" }));

      fireEvent.click(screen.getByTestId("lesson-next"));
      fireEvent.click(screen.getByTestId("lesson-next"));
      fireEvent.click(screen.getByTestId("lesson-finish"));
      await settle();

      const events = mocked.postLessonEvent.mock.calls.map((call) => [call[1].event, call[1].section_id ?? null, call[1].mode ?? null]);

      expect(events).toEqual([
         ["opened", null, null],
         ["section_viewed", "LSN-CON-02013#s1", "text"],
         ["section_viewed", "LSN-CON-02013#s2", "text"],
         ["completed", null, null]
      ]);
      expect(onLeave).toHaveBeenCalledTimes(1);
   });

   it("back to progress posts skipped and leaves; a failed read offers a retry", async () => {
      mocked.readLessonPlan.mockRejectedValueOnce(new Error("offline"));
      mocked.readLessonPlan.mockResolvedValue({ lesson: LESSON, plan: planFor(["LSN-CON-02013#s1"]), band: "low", state: null });
      mocked.postLessonEvent.mockResolvedValue({ ok: true, state: null });

      const onLeave = vi.fn();

      render(<LessonRoute lessonId="LSN-CON-02013" conceptName="The product rule" onLeave={onLeave} />);

      fireEvent.click(await screen.findByRole("button", { name: "Try again" }));
      fireEvent.click(await screen.findByTestId("lesson-back"));
      await settle();

      expect(mocked.postLessonEvent.mock.calls.map((call) => call[1].event)).toEqual(["opened", "section_viewed", "skipped"]);
      expect(onLeave).toHaveBeenCalledTimes(1);
   });

   it("sends a check answer to the check route", async () => {
      mocked.readLessonPlan.mockResolvedValue({ lesson: LESSON, plan: planFor([], ["LSN-CON-02013#chk-3"]), band: "low", state: null });
      mocked.postLessonEvent.mockResolvedValue({ ok: true, state: null });
      mocked.answerLessonCheck.mockResolvedValue({ correct: true, error_id: null, anchor: null, explanation_anchor: null });

      render(<LessonRoute lessonId="LSN-CON-02013" conceptName="The product rule" onLeave={vi.fn()} />);

      await screen.findByTestId("lesson-check");
      fireEvent.click(document.querySelector("input[type='radio'][value='C']")!);
      fireEvent.click(screen.getByTestId("lesson-check-submit"));
      await settle();

      expect(mocked.answerLessonCheck).toHaveBeenCalledWith("LSN-CON-02013", "LSN-CON-02013#chk-3", expect.objectContaining({ option_id: "C" }));
      expect(screen.getByTestId("lesson-check-verdict").textContent).toBe("ok Correct");
   });
});
