import { act, cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { TutorHarness, frame, scriptedFetch } from "../testing/agent";
import { declared, readingUnchangedDom } from "../testing/cascade";
import { FIGURE_BUILDING_CLASS } from "./AgentPanel";
import { REPLY_STOPPED, figureAnnouncement } from "./agentCopy";
import { SECANT_TO_TANGENT } from "./figureFixtures";

/* The provider's display queue (docs/agent/drawing-design.md, "The client"): a figure_step is a
   gate that opens when the words shown since the previous gate could have been read at 238 words a
   minute, and the text after it waits with it. Time is faked, so each wait is exact. */

const MILLISECONDS_PER_WORD = 60000 / 238;

const BEFORE_THE_FIGURE = "Look at the curve first. ";

const AFTER_THE_CURVE = "It rises on both sides of zero. ";

const AFTER_THE_SECANT = "The secant joins P and Q.";

let fetchScript: ReturnType<typeof scriptedFetch>;

beforeEach(() => {
   fetchScript = scriptedFetch();
   vi.stubGlobal("fetch", fetchScript.fetchStub);
   vi.useFakeTimers();
});

afterEach(() => {
   cleanup();
   vi.useRealTimers();
   vi.unstubAllGlobals();
});

async function advance(milliseconds: number) {
   await act(async () => {
      await vi.advanceTimersByTimeAsync(milliseconds);
   });
}

async function ask() {
   render(<TutorHarness screen={{ kind: "today" }} />);

   fireEvent.click(screen.getByRole("button", { name: "Ask, Ctrl+/" }));
   fireEvent.change(screen.getByLabelText("Message to the tutor"), { target: { value: "Show me the secant" } });
   fireEvent.keyDown(screen.getByLabelText("Message to the tutor"), { key: "Enter" });
   await advance(0);

   return fetchScript.turns[0];
}

async function streamFigureReply(turn: ReturnType<typeof scriptedFetch>["turns"][number], withEnd: boolean) {
   turn.push(frame("start", { conversation_id: "ACV-1", turn_id: "ATN-1", screen_line: "", can_see: [] }));
   turn.push(frame("text", { delta: BEFORE_THE_FIGURE }));
   turn.push(frame("figure_pending", {}));
   turn.push(frame("figure", SECANT_TO_TANGENT));
   turn.push(frame("figure_step", { figure: "figure", step: "curve" }));
   turn.push(frame("text", { delta: AFTER_THE_CURVE }));
   turn.push(frame("figure_step", { figure: "figure", step: "secant" }));
   turn.push(frame("text", { delta: AFTER_THE_SECANT }));

   if (withEnd) {
      turn.push(frame("end", { turn_id: "ATN-1", outcome: "complete", turns_on_item: 0, turns_in_conversation: 1 }));
      turn.close();
   }

   await advance(0);
}

function reply() {
   return screen.getByTestId("agent-reply");
}

function drawn(element: string) {
   return reply().querySelector(`svg [data-element="${element}"]`);
}

function status() {
   return screen.getByTestId("agent-status").textContent;
}

describe("a reply that draws is shown at reading pace", () => {
   it("opens each step at the reading time of the words before it and not sooner, the text after it waiting with it", async () => {
      const turn = await ask();
      const firstWait = 5 * MILLISECONDS_PER_WORD;
      const secondWait = 7 * MILLISECONDS_PER_WORD;

      await streamFigureReply(turn, true);

      expect(reply().textContent).toContain("Look at the curve first.");
      expect(reply().querySelector("svg")).not.toBeNull();
      expect(drawn("f")).toBeNull();
      expect(reply().textContent).not.toContain("It rises");

      await advance(firstWait - 1);

      expect(drawn("f")).toBeNull();
      expect(reply().textContent).not.toContain("It rises");

      await advance(2);

      expect(drawn("f")).not.toBeNull();
      expect(reply().textContent).toContain("It rises on both sides of zero.");
      expect(drawn("s1")).toBeNull();
      expect(reply().textContent).not.toContain("The secant joins");

      await advance(secondWait - 2);

      expect(drawn("s1")).toBeNull();

      await advance(2);

      expect(drawn("s1")).not.toBeNull();
      expect(reply().textContent).toContain(AFTER_THE_SECANT);
   });

   it("applies the end and announces the reply only once every step has opened, with the figure's title and description", async () => {
      const turn = await ask();

      await streamFigureReply(turn, true);
      await advance(5 * MILLISECONDS_PER_WORD + 1);
      await advance(7 * MILLISECONDS_PER_WORD - 2);

      expect(reply().getAttribute("aria-busy")).toBe("true");
      expect(status()).toBe("");
      expect(screen.getByRole("button", { name: "Stop" })).toBeTruthy();

      await advance(2);

      expect(reply().getAttribute("aria-busy")).toBe("false");
      expect(status()).toBe(`${BEFORE_THE_FIGURE}${AFTER_THE_CURVE}${AFTER_THE_SECANT} ${figureAnnouncement(SECANT_TO_TANGENT.title, SECANT_TO_TANGENT.description)}`);
      expect(screen.queryByRole("button", { name: "Stop" })).toBeNull();
   });

   it("opens every waiting step at once on Show all, and lets later steps through without waiting", async () => {
      const turn = await ask();

      await streamFigureReply(turn, false);

      fireEvent.click(within(reply()).getByRole("button", { name: "Show all" }));

      expect(drawn("f")).not.toBeNull();
      expect(drawn("s1")).not.toBeNull();
      expect(reply().textContent).toContain(AFTER_THE_SECANT);

      await act(async () => {
         turn.push(frame("figure_step", { figure: "figure", step: "closer" }));
         turn.push(frame("text", { delta: " Q moves closer." }));
         await vi.advanceTimersByTimeAsync(0);
      });

      expect(drawn("s2")).not.toBeNull();
      expect(reply().textContent).toContain("Q moves closer.");
   });

   it("opens every waiting step at once on Stop, and ends the turn stopped with everything received shown", async () => {
      const turn = await ask();

      await streamFigureReply(turn, false);

      fireEvent.click(screen.getByRole("button", { name: "Stop" }));
      await advance(0);

      expect(drawn("f")).not.toBeNull();
      expect(drawn("s1")).not.toBeNull();
      expect(reply().textContent).toContain(AFTER_THE_SECANT);
      expect(turn.signal().aborted).toBe(true);
      expect(status()).toBe(REPLY_STOPPED);
      expect(reply().getAttribute("aria-busy")).toBe("false");
      expect(within(reply()).getByRole("button", { name: "Previous" })).toBeTruthy();
   });

   it("on Stop after the server has ended the reply, shows the rest at once and keeps the server's outcome", async () => {
      const turn = await ask();

      await streamFigureReply(turn, true);

      expect(drawn("f")).toBeNull();

      fireEvent.click(screen.getByRole("button", { name: "Stop" }));
      await advance(0);

      expect(drawn("s1")).not.toBeNull();
      expect(reply().textContent).toContain(AFTER_THE_SECANT);
      expect(status()).toContain(figureAnnouncement(SECANT_TO_TANGENT.title, SECANT_TO_TANGENT.description));
      expect(status()).not.toBe(REPLY_STOPPED);
   });

   it("passes a step for another figure, an unknown step or one already opened straight through, as no gate", async () => {
      const turn = await ask();

      await act(async () => {
         turn.push(frame("figure", SECANT_TO_TANGENT));
         turn.push(frame("figure_step", { figure: "figure", step: "curve" }));
         turn.push(frame("text", { delta: BEFORE_THE_FIGURE }));
         turn.push(frame("figure_step", { figure: "another", step: "secant" }));
         turn.push(frame("figure_step", { figure: "figure", step: "nowhere" }));
         turn.push(frame("figure_step", { figure: "figure", step: "curve" }));
         turn.push(frame("text", { delta: "Still flowing." }));
         await vi.advanceTimersByTimeAsync(0);
      });

      expect(drawn("f")).not.toBeNull();
      expect(drawn("s1")).toBeNull();
      expect(reply().textContent).toContain("Still flowing.");
   });

   it("keeps the pace under reduced motion", async () => {
      const matchMedia = (query: string) => ({ matches: query.includes("reduce"), media: query, addEventListener: () => undefined, removeEventListener: () => undefined, addListener: () => undefined, removeListener: () => undefined }) as unknown as MediaQueryList;

      vi.stubGlobal("matchMedia", matchMedia);
      window.matchMedia = matchMedia;

      const turn = await ask();

      await streamFigureReply(turn, true);
      await advance(5 * MILLISECONDS_PER_WORD - 1);

      expect(drawn("f")).toBeNull();

      await advance(2);

      expect(drawn("f")).not.toBeNull();
   });

   it("holds the figure at the top of the conversation while it builds, and lets it go once the reply has ended and every step has opened", async () => {
      const turn = await ask();
      const figure = () => within(reply()).getByTestId("tutor-figure");

      await streamFigureReply(turn, true);

      expect(figure().classList.contains(FIGURE_BUILDING_CLASS)).toBe(true);
      expect(reply().lastElementChild).toBe(figure());
      expect(readingUnchangedDom(() => declared(figure(), "grid-area"))).toBe("figure");
      expect(readingUnchangedDom(() => [declared(figure(), "position"), declared(figure(), "top"), declared(figure(), "background")])).toEqual([
         "sticky",
         "0",
         "var(--growth-surface-page)"
      ]);

      await advance(5 * MILLISECONDS_PER_WORD + 1);

      expect(figure().classList.contains(FIGURE_BUILDING_CLASS)).toBe(true);

      await advance(7 * MILLISECONDS_PER_WORD);

      expect(reply().getAttribute("aria-busy")).toBe("false");
      expect(figure().classList.contains(FIGURE_BUILDING_CLASS)).toBe(false);
      expect(figure().nextElementSibling?.textContent).toContain("It rises on both sides of zero.");
   });

   it("leaves the figure in the flow where holding it would hide every word, as on the phone sheet at half height", async () => {
      const figureHeight = 389;
      const measured = vi.spyOn(HTMLElement.prototype, "getBoundingClientRect").mockImplementation(function (this: HTMLElement) {
         const height = this.getAttribute("data-testid") === "tutor-figure" ? figureHeight : 0;

         return { left: 0, top: 0, right: 0, bottom: height, width: 0, height, x: 0, y: 0, toJSON: () => ({}) } as DOMRect;
      });

      async function figureWhileBuilding(regionHeight: number) {
         const turn = await ask();

         Object.defineProperty(screen.getByTestId("agent-conversation"), "clientHeight", { configurable: true, value: regionHeight });
         await streamFigureReply(turn, false);

         return within(reply()).getByTestId("tutor-figure");
      }

      const short = await figureWhileBuilding(118);

      expect(reply().getAttribute("aria-busy")).toBe("true");
      expect(short.classList.contains(FIGURE_BUILDING_CLASS)).toBe(false);
      expect(reply().classList.contains("agent-reply-building")).toBe(false);

      cleanup();
      fetchScript = scriptedFetch();
      vi.stubGlobal("fetch", fetchScript.fetchStub);

      const tall = await figureWhileBuilding(600);

      expect(tall.classList.contains(FIGURE_BUILDING_CLASS)).toBe(true);

      measured.mockRestore();
   });
});

