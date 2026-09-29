import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { act, cleanup, render, screen, waitFor } from "@testing-library/react";

import * as client from "../api/client";
import type { ProgressPayload } from "../api/types";
import { App, OFFLINE_TEXT } from "../App";
import { ACCOUNT_CACHE_KEY, readCachedAccount } from "./cachedAccount";

vi.mock("../api/client");

const mocked = vi.mocked(client);

/* docs/plan/09-security-and-privacy.md, "Session lifetime": a reload draws the signed-in app from
   the cached account while /me checks the session, only a 401 from /me signs the student out, and
   a failure to reach the server leaves them signed in. */

const ME: client.MePayload = { id: "USR-1", username: "sam", display_name: "Sam", exam_date: "2027-05-10", purge_after: "2027-06-09" };

const PROGRESS: ProgressPayload = {
   home_state: "queue",
   days_since_last_session: 1,
   diagnostic_in_progress: null,
   skills_due_for_review: 2,
   frontier_skills: 1,
   corrected_items_returning: 0,
   forecast_minutes: 10,
   due_today_skills: 2,
   due_today_minutes: 5,
   session_in_progress: null,
   focus: []
};

function sessionEnded() {
   return Object.assign(Object.create(client.ApiError.prototype), { status: 401, detail: "a session is required" });
}

function cacheAccount() {
   window.localStorage.setItem(ACCOUNT_CACHE_KEY, JSON.stringify({ id: "USR-1", username: "sam", displayName: "Sam" }));
}

beforeEach(() => {
   vi.clearAllMocks();
   window.history.replaceState(null, "", "/");
   window.localStorage.clear();
   mocked.readAuthStatus.mockResolvedValue({ user_exists: true });
   mocked.readProgress.mockResolvedValue(PROGRESS);
});

afterEach(() => {
   cleanup();
});

describe("the signed-in account kept in this browser", () => {
   it("draws the signed-in app at once from the cached account while /me has not answered", () => {
      cacheAccount();
      mocked.readMe.mockReturnValue(new Promise(() => undefined));

      render(<App />);

      expect(screen.getByRole("navigation", { name: "Main" })).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Sign in" })).toBeNull();
      expect(screen.getByRole("button", { name: "Account and settings" }).textContent).toContain("S");
      expect(screen.getByText("@sam")).toBeTruthy();
   });

   it("keeps the student signed in and says the server is out of reach when /me cannot be reached", async () => {
      cacheAccount();
      mocked.readMe.mockRejectedValue(new TypeError("Failed to fetch"));

      render(<App />);

      expect(await screen.findByText(OFFLINE_TEXT)).toBeTruthy();
      expect(screen.getByRole("navigation", { name: "Main" })).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Sign in" })).toBeNull();
      expect(readCachedAccount()).not.toBeNull();
   });

   it("signs out and forgets the cached account only when /me answers 401", async () => {
      cacheAccount();
      mocked.readMe.mockRejectedValue(sessionEnded());

      render(<App />);

      expect(await screen.findByRole("button", { name: "Sign in" })).toBeTruthy();
      expect(readCachedAccount()).toBeNull();
   });

   it("keeps the account's non-secret fields after /me answers, and nothing else", async () => {
      mocked.readMe.mockResolvedValue(ME);

      render(<App />);

      await waitFor(() => expect(readCachedAccount()).not.toBeNull());

      expect(JSON.parse(window.localStorage.getItem(ACCOUNT_CACHE_KEY) ?? "{}")).toEqual({ id: "USR-1", username: "sam", displayName: "Sam" });
   });
});

describe("a 401 from another route while the student works", () => {
   it("asks /me again and stays signed in when /me still accepts the session", async () => {
      cacheAccount();
      mocked.readMe.mockResolvedValue(ME);

      render(<App />);
      await waitFor(() => expect(mocked.readMe).toHaveBeenCalled());

      const callsBefore = mocked.readMe.mock.calls.length;

      act(() => {
         window.dispatchEvent(new CustomEvent(client.SESSION_ENDED_EVENT));
      });

      await waitFor(() => expect(mocked.readMe.mock.calls.length).toBeGreaterThan(callsBefore));

      expect(screen.getByRole("navigation", { name: "Main" })).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Sign in" })).toBeNull();
   });

   it("signs out when /me confirms the session has ended", async () => {
      cacheAccount();
      mocked.readMe.mockResolvedValueOnce(ME);

      render(<App />);
      await waitFor(() => expect(mocked.readMe).toHaveBeenCalled());
      await screen.findByText(/Start today's set/);

      mocked.readMe.mockRejectedValue(sessionEnded());

      act(() => {
         window.dispatchEvent(new CustomEvent(client.SESSION_ENDED_EVENT));
      });

      expect(await screen.findByRole("button", { name: "Sign in" })).toBeTruthy();
   });
});
