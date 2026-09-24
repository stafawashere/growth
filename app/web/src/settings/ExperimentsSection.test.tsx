import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";

import * as client from "../api/client";
import type { ExperimentsPayload, ExperimentSwitch } from "../api/types";
import { ExperimentsSection } from "./ExperimentsSection";

vi.mock("../api/client");

const mocked = vi.mocked(client);

const feedback: ExperimentSwitch = {
   name: "feedback_elaboration",
   description: "Elaborated feedback against verification-only feedback on a wrong answer at stage unsupported.",
   unit: "item",
   arms: ["elaborated", "verification_only"],
   state: "off",
   randomised_from: null,
   assigned_units: { elaborated: 0, verification_only: 0 }
};

const retrieval: ExperimentSwitch = {
   name: "retrieval_entry",
   description: "A skill joins the mixed-review pool after 1 against 3 unaided successes at stage unsupported.",
   unit: "skill",
   arms: ["entry_1", "entry_3"],
   state: "off",
   randomised_from: null,
   assigned_units: { entry_1: 0, entry_3: 0 }
};

const bothOff: ExperimentsPayload = { experiments: [feedback, retrieval] };

beforeEach(() => {
   vi.clearAllMocks();
   mocked.readExperiments.mockResolvedValue(bothOff);
});

afterEach(() => {
   cleanup();
});

function switchRow(name: string) {
   const rows = screen.getAllByTestId("experiment-switch");

   return rows.find((row) => row.textContent!.includes(name)) as HTMLElement;
}

describe("the experiments section on settings", () => {
   it("lists both switches with their description and state", async () => {
      render(<ExperimentsSection />);

      await waitFor(() => expect(screen.getAllByTestId("experiment-switch")).toHaveLength(2));

      for (const experiment of bothOff.experiments) {
         const row = switchRow(experiment.name);

         expect(row.textContent).toContain(experiment.description);
         expect(row.getAttribute("data-state")).toBe("off");
      }
   });

   it("sets the chosen switch's state and shows the state the server read back", async () => {
      mocked.setExperimentState.mockResolvedValue({
         experiments: [{ ...feedback, state: "randomised", randomised_from: "2026-09-24T12:00:00+00:00" }, retrieval]
      });
      render(<ExperimentsSection />);

      await waitFor(() => expect(screen.getAllByTestId("experiment-switch")).toHaveLength(2));

      fireEvent.click(within(switchRow("feedback_elaboration")).getByRole("button", { name: "randomised" }));

      await waitFor(() => expect(switchRow("feedback_elaboration").getAttribute("data-state")).toBe("randomised"));

      expect(mocked.setExperimentState).toHaveBeenCalledWith("feedback_elaboration", { state: "randomised" });
      expect(switchRow("feedback_elaboration").textContent).toContain("randomised since 24 September 2026");
      expect(switchRow("retrieval_entry").getAttribute("data-state")).toBe("off");
   });
});