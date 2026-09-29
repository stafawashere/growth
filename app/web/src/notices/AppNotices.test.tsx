import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";

import * as client from "../api/client";
import type { AiNotice, ProgressPayload } from "../api/types";
import { App } from "../App";
import { AI_NOTICES_KEY, NOTICE_POLL_MILLISECONDS } from "./AiNotices";

vi.mock("../api/client");

const mocked = vi.mocked(client);

const progress: ProgressPayload = {
   home_state: "queue",
   days_since_last_session: 1,
   diagnostic_in_progress: null,
   skills_due_for_review: 2,
   frontier_skills: 1,
   corrected_items_returning: 0,
   forecast_minutes: 10,
   due_today_skills: 2,
   due_today_minutes: 10,
   session_in_progress: null,
   focus: []
};

const answered: AiNotice = {
   id: 3,
   role: "tutor",
   provider: "ReplayProvider",
   model: "claude-sonnet-5",
   outcome: "answered",
   replayed: true,
   asked: "Asked the tutor to explain the step you missed: the inner derivative.",
   answered: "The inner derivative is missing.",
   created_at: "2026-09-29T10:00:00+00:00"
};

/* Only the intervals are faked, so a real timeout lets the sign-in reads resolve. */
async function settle() {
   await act(() => new Promise((resolve) => setTimeout(resolve, 20)));
}

async function advancePoll() {
   await act(async () => {
      vi.advanceTimersByTime(NOTICE_POLL_MILLISECONDS);
   });
}

function signedInServer() {
   mocked.readAuthStatus.mockResolvedValue({ user_exists: true });
   mocked.readMe.mockResolvedValue({ id: "USR-1", display_name: null, exam_date: "2027-05-10", purge_after: "2027-06-09" });
   mocked.readProgress.mockResolvedValue(progress);
   mocked.signOut.mockResolvedValue({ logged_out: true });
   mocked.readNotices
      .mockResolvedValueOnce({ notices: [], latest: 2 })
      .mockResolvedValueOnce({ notices: [answered], latest: 3 })
      .mockResolvedValue({ notices: [], latest: 3 });
}

beforeEach(() => {
   vi.clearAllMocks();
   window.localStorage.clear();
   vi.useFakeTimers({ toFake: ["setInterval", "clearInterval"] });
});

afterEach(() => {
   cleanup();
   vi.useRealTimers();
});

describe("the AI call notices in the app shell", () => {
   it("polls while signed in, shows a notice, and stops polling once signed out", async () => {
      signedInServer();
      render(<App />);

      await screen.findByRole("button", { name: "Account and settings" });
      await settle();

      expect(mocked.readNotices).toHaveBeenCalledTimes(1);

      await advancePoll();

      expect(await screen.findByTestId("ai-notice")).toBeTruthy();

      fireEvent.click(screen.getByRole("button", { name: "Account and settings" }));
      fireEvent.click(screen.getByRole("button", { name: "Sign out" }));

      await screen.findByRole("button", { name: "Sign in" });

      const callsAtSignOut = mocked.readNotices.mock.calls.length;

      await advancePoll();
      await advancePoll();
      await advancePoll();

      expect(mocked.readNotices.mock.calls.length).toBe(callsAtSignOut);
      expect(screen.queryByTestId("ai-notice")).toBeNull();
   });

   it("never polls when the student has turned the notices off", async () => {
      window.localStorage.setItem(AI_NOTICES_KEY, "off");
      signedInServer();
      render(<App />);

      await screen.findByRole("button", { name: "Account and settings" });
      await settle();
      await advancePoll();
      await advancePoll();

      expect(mocked.readNotices).not.toHaveBeenCalled();
      expect(screen.queryByTestId("ai-notices")).toBeNull();
   });
});
