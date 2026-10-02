import { beforeAll, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import type { AttemptResult, ServedItem, SessionPayload } from "../api/types";
import * as client from "../api/client";
import { COMMIT_LABEL } from "./Item";
import { SessionScreen } from "./SessionScreen";

vi.mock("../api/client");

const mocked = vi.mocked(client);

/* MathLive resolves to its SSR stub under vitest, so this stands in for the upgraded element. Its
   value can change without an input event, which is the gap between a keystroke and a check
   pressed at once. MathLive writes an empty field as Nothing. */
class LiveMathField extends HTMLElement {
   private currentValue = JSON.stringify("Nothing");

   getValue(format: string): string {
      if (format === "math-json") {
         return this.currentValue;
      }

      return "";
   }

   type(mathJson: unknown) {
      this.currentValue = JSON.stringify(mathJson);
      this.dispatchEvent(new Event("input", { bubbles: true }));
   }

   typeWithoutEvent(mathJson: unknown) {
      this.currentValue = JSON.stringify(mathJson);
   }
}

const session: SessionPayload = {
   id: "session-1",
   mode: "practice",
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

const item: ServedItem = {
   id: "item-1",
   archetype_id: "BC-QA-01007",
   variant_id: null,
   snapshot_id: null,
   parameter_draw: null,
   stem: "Find the limit",
   figure_spec: null,
   options: null,
   calculator_status: null,
   representation: null,
   difficulty_settings: null,
   skills: ["BC-SKL-0101"],
   status: "published",
   stage: "unsupported",
   format: "short_answer",
   is_probe: false,
   served_steps: null,
   self_explanation_prompt: null
};

const result: AttemptResult = {
   id: "attempt-1",
   item_id: "item-1",
   correct: true,
   confidence: null,
   served_stage: "unsupported",
   format: "short_answer",
   p_split: null,
   p_compensatory: null
};

beforeAll(() => {
   if (customElements.get("math-field") === undefined) {
      customElements.define("math-field", LiveMathField);
   }
});

beforeEach(() => {
   vi.clearAllMocks();
   cleanup();
   mocked.openSession.mockResolvedValue(session);
   mocked.readSession.mockResolvedValue(session);
   mocked.readNextItem.mockResolvedValue({ item });
   mocked.submitAttempt.mockResolvedValue(result);
});

async function readyField() {
   render(<SessionScreen resumeSessionId={null} />);

   await screen.findByText("Find the limit");

   const commit = screen.getByRole("button", { name: COMMIT_LABEL }) as HTMLButtonElement;

   await waitFor(() => expect(commit.disabled).toBe(true));

   return { field: document.querySelector("math-field") as LiveMathField, commit };
}

function pressEnter() {
   fireEvent.keyDown(document.body, { key: "Enter" });
}

describe("checking a short answer", () => {
   it("sends the value in the field when the check follows the typing at once", async () => {
      const { field, commit } = await readyField();

      field.type(5);
      await waitFor(() => expect(commit.disabled).toBe(false));
      field.typeWithoutEvent(7);
      fireEvent.click(commit);
      fireEvent.click(await screen.findByRole("radio", { name: "unsure" }));

      await waitFor(() => expect(mocked.submitAttempt).toHaveBeenCalledTimes(1));
      expect(mocked.submitAttempt.mock.calls[0][1].answer).toEqual({ mathjson: 7 });
   });

   it("sends the value in the field on Enter as well", async () => {
      const { field, commit } = await readyField();

      field.type(5);
      await waitFor(() => expect(commit.disabled).toBe(false));
      field.typeWithoutEvent(7);
      pressEnter();
      fireEvent.click(await screen.findByRole("radio", { name: "unsure" }));

      await waitFor(() => expect(mocked.submitAttempt).toHaveBeenCalledTimes(1));
      expect(mocked.submitAttempt.mock.calls[0][1].answer).toEqual({ mathjson: 7 });
   });

   it("cannot submit an empty field by the button or by Enter", async () => {
      const { commit } = await readyField();

      fireEvent.click(commit);
      pressEnter();
      await new Promise((resolve) => setTimeout(resolve, 20));

      expect(commit.disabled).toBe(true);
      expect(mocked.submitAttempt).not.toHaveBeenCalled();
   });

   it("cannot submit a field emptied after typing, whose last input said it held a value", async () => {
      const { field, commit } = await readyField();

      field.type(5);
      await waitFor(() => expect(commit.disabled).toBe(false));
      field.typeWithoutEvent("Nothing");
      pressEnter();
      await new Promise((resolve) => setTimeout(resolve, 20));

      expect(mocked.submitAttempt).not.toHaveBeenCalled();
   });
});
