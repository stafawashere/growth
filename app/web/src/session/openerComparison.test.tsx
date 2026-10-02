import { beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import type { AttemptResult, FeedbackPayload, ServedItem, SessionPayload } from "../api/types";
import * as client from "../api/client";
import { COMPARISON_LABEL, METHOD_LABEL } from "./ComparisonPanel";
import { SessionScreen } from "./SessionScreen";

vi.mock("../api/client");

const mocked = vi.mocked(client);

const LABEL =
   "The method's first step is to partition the region at the points where the graph changes character.";

const session: SessionPayload = {
   id: "session-1",
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

function servedItem(isOpener: boolean): ServedItem {
   return {
      id: "item-1",
      archetype_id: "BC-QA-06004",
      variant_id: null,
      snapshot_id: null,
      parameter_draw: null,
      stem: "Find the accumulated change",
      figure_spec: null,
      options: null,
      calculator_status: null,
      representation: null,
      difficulty_settings: null,
      skills: ["BC-SKL-06001"],
      status: "verified",
      stage: "unsupported",
      format: "short_answer",
      is_probe: false,
      is_opener: isOpener,
      opener_concept: isOpener ? "BC-CON-06001" : undefined,
      served_steps: null,
      self_explanation_prompt: null
   };
}

const missed: AttemptResult = {
   id: "attempt-1",
   item_id: "item-1",
   correct: false,
   confidence: "unsure",
   served_stage: "unsupported",
   format: "short_answer",
   p_split: null,
   p_compensatory: null
};

/* The self-explanation prompt is set here although the server sends none with a comparison, so
   the test shows the screen withholds it on its own account too. */
const comparisonFeedback: FeedbackPayload = {
   kind: "comparison",
   stage: "unsupported",
   step_marks: [],
   elaborated: null,
   self_explanation_prompt: "which rule justifies step 1, and why does it apply here",
   confidence: "unsure",
   comparison: {
      label: LABEL,
      first_step: "partition the region at the points where the graph changes character",
      observed_behavior: "",
      attempt: { mathjson: 3 },
      worked_steps: [
         { index: 1, text: "Split the interval where the graph turns." },
         { index: 2, text: "Add the signed areas." }
      ],
      error_id: null
   },
   sentence: null,
   tutor_unavailable: false
};

function openerFlow(isOpener: boolean) {
   mocked.openSession.mockResolvedValue(session);
   mocked.readSession.mockResolvedValue(session);
   mocked.readNextItem.mockResolvedValueOnce({ item: servedItem(isOpener) }).mockResolvedValue({ item: null });
   mocked.submitAttempt.mockResolvedValue(missed);
   mocked.readFeedback.mockResolvedValue(comparisonFeedback);
   mocked.closeSession.mockResolvedValue({ id: session.id, ended_at: "2027-01-05T09:30:00Z" });
}

async function commitTheOpener() {
   render(<SessionScreen resumeSessionId={null} />);
   await screen.findByText("Find the accumulated change");
   fireEvent.click(screen.getByRole("button", { name: "Check my answer" }));
   fireEvent.click(await screen.findByRole("radio", { name: "unsure" }));
   await screen.findByTestId("feedback");
}

beforeEach(() => {
   vi.clearAllMocks();
   mocked.readNextItem.mockReset();
});

describe("the comparison after an opener miss", () => {
   it("puts the worked solution beside the attempt under the one-line comparison", async () => {
      openerFlow(true);
      await commitTheOpener();

      const panel = await screen.findByTestId("comparison-panel");

      expect(panel.textContent).toContain(COMPARISON_LABEL);
      expect(screen.getByTestId("comparison-label").textContent).toBe(LABEL);
      expect(screen.getByTestId("comparison-method").textContent).toContain(METHOD_LABEL);
      expect(screen.getByText("Split the interval where the graph turns.")).toBeTruthy();
      expect(screen.getByText("Add the signed areas.")).toBeTruthy();
      expect(screen.getByTestId("comparison-attempt")).toBeTruthy();
      expect(screen.queryByTestId("elaborated-panel")).toBeNull();

      cleanup();
   });

   it("offers no error note and no self-explanation prompt, and moves on without writing either", async () => {
      openerFlow(true);
      await commitTheOpener();

      expect(screen.queryByTestId("error-note-field")).toBeNull();
      expect(screen.queryByTestId("self-explanation-prompt")).toBeNull();

      const next = screen.getByRole("button", { name: "Next item" }) as HTMLButtonElement;

      expect(next.disabled).toBe(false);

      fireEvent.click(next);

      await waitFor(() => expect(mocked.closeSession).toHaveBeenCalledWith(session.id));
      expect(mocked.submitErrorNote).not.toHaveBeenCalled();
      expect(mocked.submitSelfExplanation).not.toHaveBeenCalled();
      expect(screen.queryByText(/you corrected/)).toBeNull();

      cleanup();
   });

   it("still asks for the note on an ordinary miss", async () => {
      openerFlow(false);
      mocked.readFeedback.mockResolvedValue({ ...comparisonFeedback, kind: "elaborated", comparison: null });
      await commitTheOpener();

      expect(screen.getByTestId("error-note-field")).toBeTruthy();
      expect(screen.queryByTestId("comparison-panel")).toBeNull();

      cleanup();
   });
});
