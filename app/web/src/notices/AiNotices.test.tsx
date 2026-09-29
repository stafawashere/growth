import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";

import * as client from "../api/client";
import type { AiNotice, NoticesPayload } from "../api/types";
import {
   AI_NOTICES_KEY,
   AiNotices,
   AiNoticesSetting,
   MAXIMUM_SHOWN_NOTICES,
   readAiNoticesEnabled
} from "./AiNotices";

vi.mock("../api/client");

const mocked = vi.mocked(client);

const POLL = 20;

const LONG = 60000;

function notice(id: number, overrides: Partial<AiNotice> = {}): AiNotice {
   return {
      id,
      role: "tutor",
      provider: "ReplayProvider",
      model: "claude-sonnet-5",
      outcome: "answered",
      replayed: true,
      asked: "Asked the tutor to explain the step you missed: differentiate the inner function.",
      answered: `Feedback sentence ${id}.`,
      created_at: "2026-09-29T10:00:00+00:00",
      ...overrides
   };
}

/* The first read only sets the cursor. Every read after it returns the queued payloads in order,
   then nothing new. */
function serve(latest: number, ...later: NoticesPayload[]) {
   const queue = [...later];

   mocked.readNotices.mockImplementation(async (after: number) => {
      const isFirst = mocked.readNotices.mock.calls.length === 1;

      if (isFirst) {
         return { notices: [], latest };
      }

      const next = queue.shift();

      return next ?? { notices: [], latest: Math.max(after, latest) };
   });
}

function pause(milliseconds: number) {
   return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

beforeEach(() => {
   mocked.readNotices.mockReset();
   window.localStorage.clear();
});

afterEach(() => {
   cleanup();
});

describe("the AI call notices", () => {
   it("shows a new notice from the route as a polite status and dismisses it", async () => {
      serve(4, { notices: [notice(5)], latest: 5 });
      render(<AiNotices active={true} pollMilliseconds={POLL} visibleMilliseconds={LONG} />);

      const region = screen.getByRole("status");

      expect(region.getAttribute("aria-live")).toBe("polite");

      const shown = await within(region).findByTestId("ai-notice");

      expect(shown.textContent).toContain("AI tutor: answered");
      expect(shown.textContent).toContain("claude-sonnet-5, replayed from a recording");
      expect(shown.textContent).toContain("Asked the tutor to explain the step you missed");
      expect(shown.textContent).not.toContain("Asked: Asked");
      expect(shown.textContent).toContain("Answer: Feedback sentence 5.");
      expect(mocked.readNotices).toHaveBeenCalledWith(0);
      expect(mocked.readNotices).toHaveBeenCalledWith(4);

      fireEvent.click(within(shown).getByRole("button", { name: "Dismiss: AI tutor: answered" }));

      expect(screen.queryByTestId("ai-notice")).toBeNull();
   });

   it("does not replay the notices that were already there when it started", async () => {
      mocked.readNotices.mockResolvedValue({ notices: [notice(1), notice(2)], latest: 2 });
      render(<AiNotices active={true} pollMilliseconds={POLL} visibleMilliseconds={LONG} />);

      await waitFor(() => expect(mocked.readNotices.mock.calls.length).toBeGreaterThanOrEqual(3));

      expect(screen.queryByTestId("ai-notice")).toBeNull();
      expect(mocked.readNotices).toHaveBeenLastCalledWith(2);
   });

   it("names a stop as a result rather than an answer", async () => {
      const stopped = notice(7, { outcome: "stopped", replayed: false, answered: "Nothing was sent: the tutor usd limit was reached." });
      serve(6, { notices: [stopped], latest: 7 });
      render(<AiNotices active={true} pollMilliseconds={POLL} visibleMilliseconds={LONG} />);

      const shown = await screen.findByTestId("ai-notice");

      expect(shown.textContent).toContain("AI tutor: the call was stopped by a limit");
      expect(shown.textContent).toContain("Result: Nothing was sent");
      expect(shown.textContent).not.toContain("replayed");
   });

   it("dismisses itself after the visible time", async () => {
      serve(0, { notices: [notice(1)], latest: 1 });
      render(<AiNotices active={true} pollMilliseconds={POLL} visibleMilliseconds={POLL * 3} />);

      await screen.findByTestId("ai-notice");
      await waitFor(() => expect(screen.queryByTestId("ai-notice")).toBeNull());
   });

   it("keeps only the newest few of a burst", async () => {
      const burst = [1, 2, 3, 4, 5].map((id) => notice(id));
      serve(0, { notices: burst, latest: 5 });
      render(<AiNotices active={true} pollMilliseconds={POLL} visibleMilliseconds={LONG} />);

      await waitFor(() => expect(screen.getAllByTestId("ai-notice").length).toBe(MAXIMUM_SHOWN_NOTICES));

      const texts = screen.getAllByTestId("ai-notice").map((element) => element.textContent ?? "");

      expect(texts[0]).toContain("Feedback sentence 3.");
      expect(texts[texts.length - 1]).toContain("Feedback sentence 5.");
   });

   it("stops polling and clears its notices when the student signs out", async () => {
      serve(0, { notices: [notice(1)], latest: 1 });
      const view = render(<AiNotices active={true} pollMilliseconds={POLL} visibleMilliseconds={LONG} />);

      await screen.findByTestId("ai-notice");

      view.rerender(<AiNotices active={false} pollMilliseconds={POLL} visibleMilliseconds={LONG} />);

      const callsAtSignOut = mocked.readNotices.mock.calls.length;

      await act(() => pause(POLL * 6));

      expect(mocked.readNotices.mock.calls.length).toBe(callsAtSignOut);
      expect(screen.queryByRole("status")).toBeNull();
      expect(screen.queryByTestId("ai-notice")).toBeNull();
   });

   it("keeps polling after a failed read", async () => {
      mocked.readNotices.mockRejectedValueOnce(new client.ApiError(500, "down"));
      render(<AiNotices active={true} pollMilliseconds={POLL} visibleMilliseconds={LONG} />);

      await waitFor(() => expect(mocked.readNotices.mock.calls.length).toBeGreaterThanOrEqual(2));
   });
});

describe("the AI notices setting", () => {
   it("is on by default and remembers being turned off", () => {
      expect(readAiNoticesEnabled()).toBe(true);

      const changed = vi.fn();
      render(<AiNoticesSetting enabled={true} onChange={changed} />);
      const box = screen.getByRole("checkbox", { name: "Show a short notice each time the app asks an AI model something" });

      fireEvent.click(box);

      expect(changed).toHaveBeenCalledWith(false);
      expect(window.localStorage.getItem(AI_NOTICES_KEY)).toBe("off");
      expect(readAiNoticesEnabled()).toBe(false);
   });
});
