import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it, beforeEach, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { AFFORDANCE_ATTRIBUTE, P1_FEEDBACK_AFFORDANCES } from "../affordances";
import type { AttemptResult, FadingStage, FeedbackPayload, ServedItem, SessionPayload } from "../api/types";
import * as client from "../api/client";
import { MATHLIVE_LOAD_FAILURE_MESSAGE } from "../input/MathField";
import { SessionScreen } from "./SessionScreen";
import { ANSWER_UNAVAILABLE, COMMIT_LABEL, type WorkedStep } from "./Item";

vi.mock("../api/client");

const mocked = vi.mocked(client);

function servedItem(stage: FadingStage): ServedItem {
   return {
      id: `item-${stage}`,
      archetype_id: "BC-ARCH-0301",
      variant_id: null,
      snapshot_id: null,
      parameter_draw: null,
      stem: "Differentiate f(x) = x^2 sin(x)",
      figure_spec: null,
      options: null,
      calculator_status: null,
      representation: null,
      difficulty_settings: null,
      skills: ["BC-SKL-0301"],
      status: "published",
      stage,
      format: "short_answer"
   };
}

const session: SessionPayload = {
   id: "session-1",
   mode: "practice",
   sub_mode: null,
   started_at: "2027-01-05T09:00:00Z",
   ended_at: null,
   updates_mastery: true,
   snapshot_id: null,
   queue: {},
   remaining: []
};

function attempt(stage: FadingStage): AttemptResult {
   return {
      id: `attempt-${stage}`,
      item_id: `item-${stage}`,
      correct: false,
      confidence: "unsure",
      served_stage: stage,
      format: "short_answer",
      p_split: null,
      p_compensatory: null
   };
}

function feedback(stage: FadingStage): FeedbackPayload {
   const isUnsupported = stage === "unsupported";

   return {
      kind: isUnsupported ? "elaborated" : "step_verification",
      stage,
      step_marks: isUnsupported ? [] : [{ index: 1, description: "Factors named", correct: true }],
      elaborated: isUnsupported
         ? {
              violated_step: "Product rule applied to both factors at once",
              observed_behavior: "Each factor was differentiated separately",
              scoring_consequence: "On an AP rubric this loses the product rule point",
              worked_solution: null,
              error_id: "BC-ERR-0304"
           }
         : null,
      self_explanation_prompt: "Which rule justifies step 3, and why does it apply here?",
      confidence: "unsure",
      sentence: null,
      tutor_unavailable: false
   };
}

const workedSteps: WorkedStep[] = [
   { index: 1, text: "Name the factors: u = x^2, v = sin(x)" },
   { index: 2, text: "u' = 2x, v' = cos(x)" },
   { index: 3, text: "f'(x) = 2x sin(x) + x^2 cos(x)" }
];

function renderScreen() {
   return render(
      <SessionScreen
         workedStepsFor={() => workedSteps}
         selfExplanationPromptFor={() => "Which rule justifies step 3, and why does it apply here?"}
      />
   );
}

function affordanceValues() {
   return Array.from(document.querySelectorAll(`[${AFFORDANCE_ATTRIBUTE}]`)).map((node) =>
      node.getAttribute(AFFORDANCE_ATTRIBUTE)
   );
}

function stageFlow(stage: FadingStage) {
   mocked.openSession.mockResolvedValue(session);
   mocked.readNextItem.mockResolvedValue({ item: servedItem(stage) });
   mocked.submitAttempt.mockResolvedValue(attempt(stage));
   mocked.readFeedback.mockResolvedValue(feedback(stage));
   mocked.submitErrorNote.mockResolvedValue({ id: `attempt-${stage}`, error_note: null });
   mocked.closeSession.mockResolvedValue({ id: session.id, ended_at: "2027-01-05T09:30:00Z" });
}

beforeEach(() => {
   vi.clearAllMocks();
});

describe("SessionScreen flow", () => {
   it("opens the session and asks for the first item", async () => {
      stageFlow("unsupported");
      renderScreen();

      await screen.findByText("Differentiate f(x) = x^2 sin(x)");

      expect(mocked.openSession).toHaveBeenCalledTimes(1);
      expect(mocked.readNextItem).toHaveBeenCalledWith(session.id);

      cleanup();
   });

   it("sends the confidence the student rated with the attempt, before any feedback is read", async () => {
      stageFlow("unsupported");
      renderScreen();

      await screen.findByText("Differentiate f(x) = x^2 sin(x)");
      fireEvent.click(screen.getByRole("radio", { name: "guess" }));
      fireEvent.click(screen.getByRole("button", { name: "Check my answer" }));

      await waitFor(() => expect(mocked.readFeedback).toHaveBeenCalled());

      const fields = mocked.submitAttempt.mock.calls[0][1];

      expect(fields.confidence).toBe("guess");
      expect(fields.item_id).toBe("item-unsupported");
      expect(mocked.submitAttempt.mock.invocationCallOrder[0]).toBeLessThan(
         mocked.readFeedback.mock.invocationCallOrder[0]
      );

      cleanup();
   });

   it("shows the elaborated panel and the error note field after an unsupported item", async () => {
      stageFlow("unsupported");
      renderScreen();

      await screen.findByText("Differentiate f(x) = x^2 sin(x)");
      fireEvent.click(screen.getByRole("button", { name: "Check my answer" }));

      await screen.findByTestId("elaborated-panel");

      expect(affordanceValues()).toContain(P1_FEEDBACK_AFFORDANCES.elaboratedFeedbackPanel);
      expect(affordanceValues()).toContain(P1_FEEDBACK_AFFORDANCES.errorNoteField);
      expect(screen.queryByTestId("step-marks")).toBeNull();

      cleanup();
   });

   it("shows the step verification marks after a completion item and no elaborated panel", async () => {
      stageFlow("completion");
      renderScreen();

      await screen.findByText("Differentiate f(x) = x^2 sin(x)");
      fireEvent.click(screen.getByRole("button", { name: "Check my answer" }));

      await screen.findByTestId("step-marks");

      expect(affordanceValues()).toContain(P1_FEEDBACK_AFFORDANCES.stepVerificationMark);
      expect(screen.queryByTestId("elaborated-panel")).toBeNull();

      cleanup();
   });

   it("writes the error note before asking for the next item", async () => {
      stageFlow("unsupported");
      renderScreen();

      await screen.findByText("Differentiate f(x) = x^2 sin(x)");
      fireEvent.click(screen.getByRole("button", { name: "Check my answer" }));
      await screen.findByTestId("elaborated-panel");

      fireEvent.change(screen.getByLabelText("In one line, what went wrong?"), {
         target: { value: "I multiplied the derivatives." }
      });
      fireEvent.click(screen.getByRole("button", { name: "Next item" }));

      await waitFor(() =>
         expect(mocked.submitErrorNote).toHaveBeenCalledWith(
            session.id,
            "attempt-unsupported",
            "I multiplied the derivatives."
         )
      );

      cleanup();
   });

   it("closes the session when the queue runs out", async () => {
      stageFlow("unsupported");
      mocked.readNextItem.mockResolvedValue({ item: null });
      renderScreen();

      await waitFor(() => expect(mocked.closeSession).toHaveBeenCalledWith(session.id));
      expect(screen.getByText("That is today's set finished.")).toBeTruthy();

      cleanup();
   });
});

describe("SessionScreen affordance vocabulary", () => {
   it("renders only attribute values drawn from P1_FEEDBACK_AFFORDANCES", async () => {
      const known = Object.values(P1_FEEDBACK_AFFORDANCES) as string[];

      stageFlow("unsupported");
      renderScreen();
      await screen.findByText("Differentiate f(x) = x^2 sin(x)");
      fireEvent.click(screen.getByRole("button", { name: "Check my answer" }));
      await screen.findByTestId("elaborated-panel");

      const rendered = affordanceValues();

      expect(rendered.length).toBeGreaterThan(0);

      for (const value of rendered) {
         expect(known).toContain(value);
      }

      cleanup();
   });

   it("reaches every affordance in P1_FEEDBACK_AFFORDANCES over the three stages", async () => {
      const seen = new Set<string>();
      const stages: FadingStage[] = ["example", "completion", "unsupported"];

      for (const stage of stages) {
         stageFlow(stage);
         renderScreen();
         await screen.findByText("Differentiate f(x) = x^2 sin(x)");

         for (const value of affordanceValues()) {
            seen.add(value as string);
         }

         fireEvent.click(screen.getAllByRole("button", { name: /Check my answer|I have explained this/ })[0]);
         await screen.findByRole("button", { name: "Next item" });

         for (const value of affordanceValues()) {
            seen.add(value as string);
         }

         cleanup();
      }

      for (const name of Object.keys(P1_FEEDBACK_AFFORDANCES) as (keyof typeof P1_FEEDBACK_AFFORDANCES)[]) {
         expect(seen).toContain(P1_FEEDBACK_AFFORDANCES[name]);
      }
   });
});

describe("SessionScreen math input failure", () => {
   it("tells the student the problem takes no answer when the math keyboard never loads", async () => {
      vi.resetModules();
      vi.doMock("mathlive", () => {
         throw new Error("chunk request failed");
      });

      stageFlow("unsupported");
      renderScreen();

      await screen.findByText("Differentiate f(x) = x^2 sin(x)");

      const told = await screen.findByText(ANSWER_UNAVAILABLE);
      const alerted = screen.getByRole("alert");

      expect(told).toBeTruthy();
      expect(alerted.textContent).toBe(MATHLIVE_LOAD_FAILURE_MESSAGE);
      expect(screen.queryByRole("button", { name: COMMIT_LABEL })).toBeNull();

      cleanup();
      vi.doUnmock("mathlive");
      vi.resetModules();
   });
});

describe("session source files", () => {
   it("writes no hex colour anywhere under src/session", () => {
      const directory = join(process.cwd(), "src", "session");
      const names = readdirSync(directory).filter((name) => name.endsWith(".tsx") || name.endsWith(".ts"));
      const hex = /#[0-9a-fA-F]{3,8}\b/;
      const offenders: string[] = [];

      expect(names.length).toBeGreaterThan(0);

      for (const name of names) {
         const source = readFileSync(join(directory, name), "utf8");

         if (hex.test(source)) {
            offenders.push(name);
         }
      }

      expect(offenders).toEqual([]);
   });

   it("names every colour it does use as a growth custom property", () => {
      const directory = join(process.cwd(), "src", "session");
      const names = readdirSync(directory).filter((name) => name.endsWith(".tsx"));
      const anyVar = /var\(\s*--[a-z-]+/g;
      const foreign: string[] = [];

      for (const name of names) {
         const source = readFileSync(join(directory, name), "utf8");
         const used = source.match(anyVar) ?? [];

         for (const reference of used) {
            const isGrowthToken = reference.includes("--growth-");

            if (!isGrowthToken) {
               foreign.push(`${name}: ${reference}`);
            }
         }
      }

      expect(foreign).toEqual([]);
   });
});
function deferred<T>() {
   let settle: (value: T) => void = () => undefined;

   const promise = new Promise<T>((resolve) => {
      settle = resolve;
   });

   return { promise, settle };
}

async function commitOn(label: RegExp) {
   renderScreen();

   await screen.findByText("Differentiate f(x) = x^2 sin(x)");
   fireEvent.click(screen.getAllByRole("button", { name: label })[0]);
}

const COMMIT_BUTTONS = /Check my answer|I have explained this/;

describe("SessionScreen confidence gate, 11 implementer decision 3", () => {
   const RATED_STAGES: FadingStage[] = ["completion", "unsupported"];

   it("withholds feedback until the rating the committed attempt came back without is recorded", async () => {
      for (const stage of RATED_STAGES) {
         vi.clearAllMocks();
         stageFlow(stage);
         mocked.submitAttempt.mockResolvedValue({ ...attempt(stage), confidence: null });
         mocked.submitConfidence.mockResolvedValue({ id: `attempt-${stage}`, confidence: "confident" });

         await commitOn(COMMIT_BUTTONS);
         await waitFor(() => expect(mocked.submitAttempt).toHaveBeenCalledTimes(1));

         expect({ stage, feedbackRead: mocked.readFeedback.mock.calls.length }).toEqual({
            stage,
            feedbackRead: 0
         });
         expect(screen.queryByTestId("feedback")).toBeNull();

         fireEvent.click(screen.getByRole("radio", { name: "confident" }));

         await screen.findByTestId("feedback");

         expect(mocked.submitConfidence).toHaveBeenCalledWith(session.id, `attempt-${stage}`, {
            confidence: "confident"
         });
         expect(mocked.submitConfidence.mock.invocationCallOrder[0]).toBeLessThan(
            mocked.readFeedback.mock.invocationCallOrder[0]
         );

         cleanup();
      }
   });

   it("collects no rating at stage example and serves that feedback straight away", async () => {
      stageFlow("example");
      mocked.submitAttempt.mockResolvedValue({ ...attempt("example"), confidence: null });

      await commitOn(COMMIT_BUTTONS);
      await screen.findByTestId("feedback");

      expect(mocked.submitAttempt.mock.calls[0][1].confidence).toBeUndefined();
      expect(mocked.submitConfidence).not.toHaveBeenCalled();

      cleanup();
   });
});

describe("SessionScreen error note, 11 P1 scope item 10", () => {
   it("asks for no note on an item the student got right and advances without one", async () => {
      stageFlow("unsupported");
      mocked.submitAttempt.mockResolvedValue({ ...attempt("unsupported"), correct: true });

      await commitOn(COMMIT_BUTTONS);
      await screen.findByTestId("feedback");

      expect(screen.queryByTestId("error-note-field")).toBeNull();

      fireEvent.click(screen.getByRole("button", { name: "Next item" }));

      await waitFor(() => expect(mocked.readNextItem).toHaveBeenCalledTimes(2));
      expect(mocked.submitErrorNote).not.toHaveBeenCalled();

      cleanup();
   });

   it("holds a corrected item on the feedback screen until the note is written", async () => {
      stageFlow("unsupported");

      await commitOn(COMMIT_BUTTONS);
      await screen.findByTestId("feedback");

      const next = screen.getByRole("button", { name: "Next item" }) as HTMLButtonElement;

      expect(next.disabled).toBe(true);

      fireEvent.change(screen.getByLabelText("In one line, what went wrong?"), {
         target: { value: "   " }
      });
      fireEvent.click(next);

      await waitFor(() => expect(mocked.submitAttempt).toHaveBeenCalledTimes(1));

      expect(mocked.submitErrorNote).not.toHaveBeenCalled();
      expect(mocked.readNextItem).toHaveBeenCalledTimes(1);

      fireEvent.change(screen.getByLabelText("In one line, what went wrong?"), {
         target: { value: "I multiplied the derivatives." }
      });

      expect(next.disabled).toBe(false);

      fireEvent.click(next);

      await waitFor(() => expect(mocked.readNextItem).toHaveBeenCalledTimes(2));
      expect(mocked.submitErrorNote).toHaveBeenCalledWith(
         session.id,
         "attempt-unsupported",
         "I multiplied the derivatives."
      );

      cleanup();
   });
});

describe("SessionScreen in-flight guard", () => {
   it("sends one error note when Next item is clicked twice", async () => {
      stageFlow("unsupported");

      const note = deferred<{ id: string; error_note: string | null }>();

      mocked.submitErrorNote.mockReturnValue(note.promise);

      await commitOn(COMMIT_BUTTONS);
      await screen.findByTestId("feedback");

      fireEvent.change(screen.getByLabelText("In one line, what went wrong?"), {
         target: { value: "I multiplied the derivatives." }
      });

      const next = screen.getByRole("button", { name: "Next item" });

      fireEvent.click(next);
      fireEvent.click(next);

      note.settle({ id: "attempt-unsupported", error_note: "I multiplied the derivatives." });

      await waitFor(() => expect(mocked.readNextItem).toHaveBeenCalledTimes(2));
      expect(mocked.submitErrorNote).toHaveBeenCalledTimes(1);

      cleanup();
   });

   it("submits one attempt when Check my answer is clicked twice", async () => {
      stageFlow("unsupported");

      const committed = deferred<AttemptResult>();

      mocked.submitAttempt.mockReturnValue(committed.promise);
      renderScreen();

      await screen.findByText("Differentiate f(x) = x^2 sin(x)");

      const commit = screen.getByRole("button", { name: "Check my answer" });

      fireEvent.click(commit);
      fireEvent.click(commit);

      committed.settle(attempt("unsupported"));

      await screen.findByTestId("feedback");

      expect(mocked.submitAttempt).toHaveBeenCalledTimes(1);

      cleanup();
   });
});