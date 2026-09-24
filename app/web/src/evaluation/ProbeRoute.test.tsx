import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";

import * as client from "../api/client";
import type { ProbeAdministration, ProbeServedItem } from "../api/types";
import { ProbeRoute } from "./ProbeRoute";

vi.mock("../api/client");

const mocked = vi.mocked(client);

const started: ProbeAdministration = {
   id: "PRB-7",
   probe_set: "stable-probe-v1",
   started_at: "2026-09-24T12:00:00+00:00",
   finished_at: null,
   answered: 0,
   graded: 0,
   correct: 0,
   items: 2
};

const probeItem: ProbeServedItem = {
   id: "ITM-P1",
   archetype_id: "BC-ARCH-0101",
   variant_id: null,
   snapshot_id: null,
   parameter_draw: null,
   stem: "Which value is the limit?",
   figure_spec: null,
   options: [
      { id: "A", label: "zero" },
      { id: "B", label: "one" }
   ],
   calculator_status: null,
   representation: null,
   difficulty_settings: null,
   skills: ["BC-SKL-01001"],
   status: "verified",
   format: "mcq"
};

const afterAnswer: ProbeAdministration = {
   ...started,
   finished_at: "2026-09-24T12:00:00+00:00",
   answered: 2,
   graded: 1,
   correct: 1
};

beforeEach(() => {
   vi.clearAllMocks();
   mocked.startProbe.mockResolvedValue(started);
   mocked.readNextProbeItem.mockResolvedValueOnce({ item: probeItem }).mockResolvedValueOnce({ item: null });
   mocked.answerProbeItem.mockResolvedValue(afterAnswer);
});

afterEach(() => {
   cleanup();
});

describe("the concept probe", () => {
   it("serves an item with no confidence rating, sends the answer without feedback and ends on correct of graded", async () => {
      render(<ProbeRoute openAdministrationId={null} onLeave={vi.fn()} />);

      fireEvent.click(screen.getByRole("button", { name: "Start the concept probe" }));

      await screen.findByText(probeItem.stem);

      expect(screen.queryByRole("button", { name: /guess|unsure|confident/i })).toBeNull();
      expect(screen.queryByText(/Before you see the answer/)).toBeNull();

      fireEvent.click(screen.getByLabelText("one"));
      fireEvent.click(screen.getByRole("button", { name: "Next question" }));

      const score = await screen.findByTestId("probe-score");

      expect(score.textContent).toBe("1 of 1 graded items correct.");
      expect(mocked.answerProbeItem).toHaveBeenCalledWith(
         "PRB-7",
         expect.objectContaining({ item_id: "ITM-P1", answer: { option_id: "B" } })
      );
      expect(mocked.readFeedback).not.toHaveBeenCalled();
   });

   it("resumes an open probe by its own id rather than starting another", async () => {
      render(<ProbeRoute openAdministrationId="PRB-7" onLeave={vi.fn()} />);

      await screen.findByText(probeItem.stem);

      await waitFor(() => expect(mocked.readNextProbeItem).toHaveBeenCalledWith("PRB-7"));
      expect(mocked.startProbe).not.toHaveBeenCalled();
   });
});