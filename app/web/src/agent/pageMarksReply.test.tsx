import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { AgentScreen, TutorMarksSpec } from "../api/types";
import { CHECKED_ITEM, TutorHarness, UNCHECKED_ITEM, frame, scriptedFetch } from "../testing/agent";
import { CLEAR_MARKS, MARKED_ON_THE_PAGE, MARKS_REFUSED, marksAnnouncement } from "./agentCopy";
import { markTarget, pageMark } from "./figureFixtures";

/* The provider keeps a reply's marks with the screen the question was asked on
   (docs/agent/drawing-design.md, "Marks on the page"): they reveal step by step through the same
   display queue as a figure's steps, leave with the screen and come back finished and still. */

const MILLISECONDS_PER_WORD = 60000 / 238;

function marks(element: string, id = "marks"): TutorMarksSpec {
   return {
      id,
      description: `The stem is marked with ${element}.`,
      steps: [
         { id: `${element}-phrase`, caption: "The key phrase" },
         { id: `${element}-whole`, caption: "The whole question" }
      ],
      marks: [
         pageMark(`${element}-phrase`, element, "highlight", "underline", { target: markTarget("stem") }),
         pageMark(`${element}-whole`, `${element}-ring`, "constructed", "ring", { target: markTarget("stem") })
      ]
   };
}

const END = frame("end", { turn_id: "ATN-1", outcome: "complete", turns_on_item: 1, turns_in_conversation: 1 });

let fetchScript: ReturnType<typeof scriptedFetch>;

beforeEach(() => {
   fetchScript = scriptedFetch();
   vi.stubGlobal("fetch", fetchScript.fetchStub);
});

afterEach(() => {
   cleanup();
   vi.useRealTimers();
   vi.unstubAllGlobals();
});

function Screen(props: { screen: AgentScreen }) {
   return (
      <>
         <p data-agent-anchor="stem">Find the tangent line at P.</p>
         <TutorHarness screen={props.screen} />
      </>
   );
}

function drawn(element: string) {
   return document.querySelector(`[data-testid='page-marks'] [data-mark='${element}']`);
}

function composer() {
   return screen.getByLabelText("Message to the tutor");
}

function ask(question: string) {
   const isOpen = screen.getByTestId("agent-panel").hidden === false;

   if (!isOpen) {
      fireEvent.click(screen.getByRole("button", { name: "Ask, Ctrl+/" }));
   }

   fireEvent.change(composer(), { target: { value: question } });
   fireEvent.keyDown(composer(), { key: "Enter" });

   return fetchScript.turns[fetchScript.turns.length - 1];
}

/* Marks before any text, so every step opens as it arrives. */
async function replyWithMarks(spec: TutorMarksSpec | null, text = "Here it is.") {
   const turn = ask("Mark it for me");
   const steps = (spec?.steps ?? []).map((step) => frame("figure_step", { figure: spec!.id, step: step.id }));

   await act(async () => {
      if (spec !== null) {
         turn.push(frame("marks", spec));
         steps.forEach((step) => turn.push(step));
      }

      turn.push(frame("text", { delta: text }));
      turn.push(END);
      turn.close();
   });

   await waitFor(() => expect(screen.queryByRole("button", { name: "Stop" })).toBeNull());
}

function replies() {
   return screen.getAllByTestId("agent-reply");
}

describe("a reply's marks on the page", () => {
   it("reveals each marked step at reading pace, like a figure's steps, and lists what is marked", async () => {
      vi.useFakeTimers();
      render(<Screen screen={UNCHECKED_ITEM} />);

      const turn = ask("Mark it");
      const spec = marks("u");

      await act(async () => {
         turn.push(frame("text", { delta: "Look here now. " }));
         turn.push(frame("marks", spec));
         turn.push(frame("figure_step", { figure: "marks", step: "u-phrase" }));
         turn.push(frame("text", { delta: "This phrase." }));
         await vi.advanceTimersByTimeAsync(0);
      });

      expect(drawn("u")).toBeNull();
      expect(screen.queryByTestId("agent-marks")).toBeNull();

      await act(async () => {
         await vi.advanceTimersByTimeAsync(3 * MILLISECONDS_PER_WORD - 1);
      });

      expect(drawn("u")).toBeNull();
      expect(replies()[0].textContent).not.toContain("This phrase.");

      await act(async () => {
         await vi.advanceTimersByTimeAsync(2);
      });

      const listed = within(screen.getByTestId("agent-marks"));

      expect(drawn("u")).not.toBeNull();
      expect(drawn("u-ring")).toBeNull();
      expect(replies()[0].textContent).toContain("This phrase.");
      expect(listed.getByText(MARKED_ON_THE_PAGE)).toBeTruthy();
      expect(listed.getAllByRole("listitem").map((item) => item.textContent)).toEqual(["The key phrasenow"]);
      expect(listed.getAllByRole("listitem")[0].getAttribute("aria-current")).toBe("step");
   });

   it("announces the marks' description after the reply's words", async () => {
      render(<Screen screen={UNCHECKED_ITEM} />);

      await replyWithMarks(marks("u"));

      expect(screen.getByTestId("agent-status").textContent).toBe(`Here it is. ${marksAnnouncement(marks("u").description)}`);
   });

   it("hides a screen's marks when the student leaves it, and draws them again finished and still on return", async () => {
      const { rerender } = render(<Screen screen={UNCHECKED_ITEM} />);

      await replyWithMarks(marks("u"));

      expect(drawn("u")).not.toBeNull();
      expect(drawn("u-ring")).not.toBeNull();

      rerender(<Screen screen={{ kind: "review" }} />);

      expect(screen.queryByTestId("page-marks")).toBeNull();

      rerender(<Screen screen={UNCHECKED_ITEM} />);

      expect(drawn("u")).not.toBeNull();
      expect(drawn("u-ring")).not.toBeNull();
      expect(document.querySelectorAll("[data-testid='page-marks'] .motion-figure-step, [data-testid='page-marks'] clipPath")).toHaveLength(0);
   });

   it("keeps an item's marks when the item is checked, since the screen is still that item", async () => {
      const { rerender } = render(<Screen screen={UNCHECKED_ITEM} />);

      await replyWithMarks(marks("u"));
      rerender(<Screen screen={CHECKED_ITEM} />);

      expect(drawn("u")).not.toBeNull();
   });

   it("replaces a screen's marks with the next reply's, and leaves them for a reply that marks nothing", async () => {
      render(<Screen screen={UNCHECKED_ITEM} />);

      await replyWithMarks(marks("u"));
      await replyWithMarks(marks("v"));

      expect(drawn("u")).toBeNull();
      expect(drawn("v")).not.toBeNull();
      expect(within(replies()[0]).queryByRole("button", { name: CLEAR_MARKS })).toBeNull();
      expect(within(replies()[1]).getByRole("button", { name: CLEAR_MARKS })).toBeTruthy();

      await replyWithMarks(null, "Nothing to mark.");

      expect(drawn("v")).not.toBeNull();
   });

   it("clears the current screen's marks on Clear marks, and keeps the list of what was marked", async () => {
      render(<Screen screen={UNCHECKED_ITEM} />);

      await replyWithMarks(marks("u"));

      fireEvent.click(screen.getByRole("button", { name: CLEAR_MARKS }));

      expect(screen.queryByTestId("page-marks")).toBeNull();
      expect(screen.getByTestId("agent-marks").textContent).toContain(MARKED_ON_THE_PAGE);
      expect(screen.queryByRole("button", { name: CLEAR_MARKS })).toBeNull();
   });

   it("shows the refused line under the reply when the server refused the marks, and the reply goes on", async () => {
      render(<Screen screen={UNCHECKED_ITEM} />);

      const turn = ask("Mark it");

      await act(async () => {
         turn.push(frame("text", { delta: "Look. " }));
         turn.push(frame("figure_refused", { reason: "malformed", copy: "", part: "marks" }));
         turn.push(frame("text", { delta: "More." }));
         turn.push(END);
         turn.close();
      });

      await waitFor(() => expect(screen.getByTestId("agent-marks-refused").textContent).toBe(MARKS_REFUSED));

      expect(replies()[0].textContent).toBe(`Look. More.${MARKS_REFUSED}`);
      expect(screen.queryByTestId("page-marks")).toBeNull();
   });

   it("shows the refused line for marks that do not check out on the client", async () => {
      render(<Screen screen={UNCHECKED_ITEM} />);

      await replyWithMarks({ ...marks("u"), marks: "not a list" } as unknown as TutorMarksSpec);

      expect(screen.getByTestId("agent-marks-refused").textContent).toBe(MARKS_REFUSED);
      expect(screen.queryByTestId("page-marks")).toBeNull();
   });

   it("empties the marks with the conversation when it is closed", async () => {
      render(<Screen screen={UNCHECKED_ITEM} />);

      await replyWithMarks(marks("u"));

      fetchScript.answerNextWith(() => Promise.resolve({ ok: true, status: 200, json: async () => ({ closed: "ACV-1" }) }));
      fireEvent.click(screen.getByRole("button", { name: "Close" }));

      expect(screen.queryByTestId("page-marks")).toBeNull();
   });
});
