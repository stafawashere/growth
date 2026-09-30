import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { CHECKED_ITEM, TutorHarness, UNCHECKED_ITEM, frame, scriptedFetch } from "../testing/agent";
import {
   CANNOT_SEE_LINE,
   CONVERSATION_CEILING,
   DAILY_CAP,
   EMPTY_ELSEWHERE,
   EMPTY_ON_ITEM,
   GUARDRAIL_AFTER_CHECKING,
   GUARDRAIL_BEFORE_CHECKING,
   MINUTE_CAP,
   OFFLINE,
   REPLY_STOPPED,
   SCREEN_REFUSED,
   SIGN_IN_EXPIRED,
   THIRD_TURN_CEILING,
   TIMED_PART,
   USAGE_LIMIT_UNKNOWN_RESET,
   WITHHELD,
   WRITING_A_REPLY
} from "./agentCopy";
import { resetTimeText } from "./AgentPanel";

let fetchScript: ReturnType<typeof scriptedFetch>;

beforeEach(() => {
   fetchScript = scriptedFetch();
   vi.stubGlobal("fetch", fetchScript.fetchStub);
});

afterEach(() => {
   cleanup();
   vi.unstubAllGlobals();
});

function askButton() {
   return screen.getByRole("button", { name: "Ask, Ctrl+/" });
}

function composer() {
   return screen.getByLabelText("Message to the tutor") as HTMLTextAreaElement;
}

function panel() {
   return screen.getByTestId("agent-panel");
}

function sendButton() {
   return screen.getByRole("button", { name: "Send" }) as HTMLButtonElement;
}

function pressShortcut() {
   fireEvent.keyDown(document.activeElement ?? document.body, { key: "/", code: "Slash", ctrlKey: true });
}

function type(text: string) {
   fireEvent.change(composer(), { target: { value: text } });
}

async function openAndSend(text: string) {
   fireEvent.click(askButton());
   type(text);
   fireEvent.keyDown(composer(), { key: "Enter" });
   await waitFor(() => expect(fetchScript.fetchStub).toHaveBeenCalled());
}

describe("opening and closing the tutor", () => {
   it("opens from the Ask button and puts focus in the composer", () => {
      render(<TutorHarness screen={{ kind: "today" }} />);

      expect(panel().hidden).toBe(true);
      expect(askButton().getAttribute("aria-controls")).toBe(panel().id);

      fireEvent.click(askButton());

      expect(panel().hidden).toBe(false);
      expect(askButton().getAttribute("aria-expanded")).toBe("true");
      expect(document.activeElement).toBe(composer());
   });

   it("opens from Ctrl+/ anywhere on the page and puts focus in the composer", () => {
      render(<TutorHarness screen={{ kind: "today" }} />);

      screen.getByRole("button", { name: "Page control" }).focus();
      pressShortcut();

      expect(panel().hidden).toBe(false);
      expect(document.activeElement).toBe(composer());
   });

   it("closes on Escape and gives focus back to the element that had it", () => {
      render(<TutorHarness screen={{ kind: "today" }} />);

      const pageControl = screen.getByRole("button", { name: "Page control" });

      pageControl.focus();
      pressShortcut();
      fireEvent.keyDown(composer(), { key: "Escape" });

      expect(panel().hidden).toBe(true);
      expect(document.activeElement).toBe(pageControl);
   });

   it("closes on the shortcut when focus is inside the panel, and moves focus in when it is not", () => {
      render(<TutorHarness screen={{ kind: "today" }} />);

      const pageControl = screen.getByRole("button", { name: "Page control" });

      pageControl.focus();
      pressShortcut();
      pageControl.focus();
      pressShortcut();

      expect(panel().hidden).toBe(false);
      expect(document.activeElement).toBe(composer());

      pressShortcut();

      expect(panel().hidden).toBe(true);
      expect(document.activeElement).toBe(pageControl);
   });

   it("gives focus to the Ask button when the element that had it is gone", () => {
      const { rerender } = render(<TutorHarness screen={{ kind: "today" }} />);

      askButton().focus();
      pressShortcut();
      rerender(<TutorHarness screen={{ kind: "review" }} />);
      fireEvent.keyDown(composer(), { key: "Escape" });

      expect(document.activeElement).toBe(askButton());
   });
});

describe("what the panel says it can see", () => {
   it("shows the guardrail and the cannot-see line before checking, and the after-checking line once checked", () => {
      const { rerender } = render(<TutorHarness screen={UNCHECKED_ITEM} />);

      fireEvent.click(askButton());

      expect(screen.getByTestId("agent-guardrail").textContent).toBe(GUARDRAIL_BEFORE_CHECKING);
      expect(screen.getByTestId("agent-cannot-see").textContent).toBe(CANNOT_SEE_LINE);
      expect(screen.getByTestId("agent-empty").textContent).toBe(EMPTY_ON_ITEM);

      rerender(<TutorHarness screen={CHECKED_ITEM} />);

      expect(screen.getByTestId("agent-guardrail").textContent).toBe(GUARDRAIL_AFTER_CHECKING);
      expect(screen.queryByTestId("agent-cannot-see")).toBeNull();
      expect(screen.getByTestId("agent-empty").textContent).toBe(EMPTY_ELSEWHERE);
   });

   it("lists every field the turn sends under What it can see, and nothing typed on the page", () => {
      render(<TutorHarness screen={UNCHECKED_ITEM} />);

      fireEvent.click(askButton());

      const fields = within(screen.getByTestId("agent-fields"))
         .getAllByRole("listitem")
         .map((item) => item.textContent);

      expect(screen.getByText("What it can see").tagName).toBe("SUMMARY");
      expect(fields).toEqual(["kind", "session_id", "attempt_id", "item_id", "format", "served_stage", "submitted"]);
   });

   it("announces the new line once when the screen changes while the panel is open", () => {
      const { rerender } = render(<TutorHarness screen={{ kind: "today" }} />);

      fireEvent.click(askButton());

      expect(screen.getByTestId("agent-status").textContent).toBe("");

      rerender(<TutorHarness screen={{ kind: "review" }} />);

      expect(screen.getByTestId("agent-status").textContent).toBe("Can see: Review, your error notes and corrected items.");
   });

   it("keeps the Ask button in the bar on a timed part, disabled with its reason, and the shortcut does nothing", () => {
      render(<TutorHarness screen={{ kind: "assessments", format: "mock", timed: true }} />);

      expect((askButton() as HTMLButtonElement).disabled).toBe(true);
      expect(screen.getByTestId("ask-reason").textContent).toBe(TIMED_PART);
      expect(askButton().getAttribute("aria-describedby")).toBe("ask-reason");

      pressShortcut();

      expect(panel().hidden).toBe(true);
   });

   it("closes the panel when a timed part starts while it is open", () => {
      const { rerender } = render(<TutorHarness screen={{ kind: "assessments", format: "mock" }} />);

      fireEvent.click(askButton());
      rerender(<TutorHarness screen={{ kind: "assessments", format: "mock", timed: true }} />);

      expect(panel().hidden).toBe(true);
   });
});

describe("sending and streaming", () => {
   it("sends on Enter with the screen and the message, and a Shift+Enter adds a line instead", async () => {
      render(<TutorHarness screen={UNCHECKED_ITEM} />);

      fireEvent.click(askButton());
      type("I plugged in 3 and got 0/0.");
      fireEvent.keyDown(composer(), { key: "Enter", shiftKey: true });

      expect(fetchScript.fetchStub).not.toHaveBeenCalled();

      fireEvent.keyDown(composer(), { key: "Enter" });

      await waitFor(() => expect(fetchScript.fetchStub).toHaveBeenCalledTimes(1));

      const [path, init] = fetchScript.fetchStub.mock.calls[0];

      expect(path).toBe("/agent/turns");
      expect((init as RequestInit).method).toBe("POST");
      expect(fetchScript.turns[0].body()).toEqual({ conversation_id: null, screen: UNCHECKED_ITEM, message: "I plugged in 3 and got 0/0." });
      expect(screen.getByText("I plugged in 3 and got 0/0.")).toBeTruthy();
      expect(composer().value).toBe("");
      expect(document.activeElement).toBe(composer());
   });

   it("adds text as frames arrive, even split mid-frame, and announces the whole reply once when it ends", async () => {
      render(<TutorHarness screen={UNCHECKED_ITEM} />);

      const status = screen.getByTestId("agent-status");
      const announced: string[] = [];
      const observer = new MutationObserver(() => {
         if (status.textContent !== "") {
            announced.push(status.textContent ?? "");
         }
      });

      observer.observe(status, { childList: true, characterData: true, subtree: true });

      await openAndSend("Where do I start?");

      const turn = fetchScript.turns[0];
      const reply = () => screen.getByTestId("agent-reply");

      expect(reply().textContent).toBe(WRITING_A_REPLY);
      expect(reply().getAttribute("aria-busy")).toBe("true");

      const start = frame("start", { conversation_id: "ACV-1", turn_id: "ATN-1", screen_line: "Can see: Today, practice item, not checked yet.", can_see: ["kind"] });
      const first = frame("text", { delta: "What does 0/0 tell you" });
      const second = frame("text", { delta: " about the form of this limit?" });

      await act(async () => {
         turn.push(start + first.slice(0, 17));
      });

      expect(reply().textContent).toBe(WRITING_A_REPLY);

      await act(async () => {
         turn.push(first.slice(17) + second.slice(0, 5));
      });

      await waitFor(() => expect(reply().textContent).toBe("What does 0/0 tell you"));
      expect(status.textContent).toBe("");

      await act(async () => {
         turn.push(second.slice(5));
         turn.push(frame("end", { turn_id: "ATN-1", outcome: "complete", turns_on_item: 1, turns_in_conversation: 1 }));
         turn.close();
      });

      await waitFor(() => expect(reply().getAttribute("aria-busy")).toBe("false"));

      observer.disconnect();

      expect(reply().textContent).toBe("What does 0/0 tell you about the form of this limit?");
      expect(announced).toEqual(["What does 0/0 tell you about the form of this limit?"]);
   });

   it("carries the conversation id into the next turn", async () => {
      render(<TutorHarness screen={{ kind: "today" }} />);

      await openAndSend("First");
      await act(async () => {
         fetchScript.turns[0].push(frame("start", { conversation_id: "ACV-7", turn_id: "ATN-1", screen_line: "", can_see: [] }));
         fetchScript.turns[0].push(frame("text", { delta: "A question back?" }));
         fetchScript.turns[0].push(frame("end", { turn_id: "ATN-1", outcome: "complete", turns_on_item: 0, turns_in_conversation: 1 }));
         fetchScript.turns[0].close();
      });

      await waitFor(() => expect(screen.queryByRole("button", { name: "Stop" })).toBeNull());

      type("Second");
      fireEvent.keyDown(composer(), { key: "Enter" });

      await waitFor(() => expect(fetchScript.turns).toHaveLength(2));
      expect((fetchScript.turns[1].body() as { conversation_id: string }).conversation_id).toBe("ACV-7");
   });

   it("stops the reply with Stop, aborting the request, and announces that it stopped", async () => {
      render(<TutorHarness screen={{ kind: "today" }} />);

      await openAndSend("Explain this part");
      await act(async () => {
         fetchScript.turns[0].push(frame("text", { delta: "The first part" }));
      });

      const stop = await screen.findByRole("button", { name: "Stop" });

      fireEvent.click(stop);

      await waitFor(() => expect(screen.getByTestId("agent-status").textContent).toBe(REPLY_STOPPED));
      expect(fetchScript.turns[0].signal().aborted).toBe(true);
      expect(screen.getByTestId("agent-reply").textContent).toBe("The first part");
      expect(screen.queryByRole("button", { name: "Stop" })).toBeNull();
   });

   it("shows the fixed withheld line in place of a withheld reply", async () => {
      render(<TutorHarness screen={UNCHECKED_ITEM} />);

      await openAndSend("Just tell me");
      await act(async () => {
         fetchScript.turns[0].push(frame("text", { delta: "declined" }));
         fetchScript.turns[0].push(frame("end", { turn_id: "ATN-2", outcome: "withheld", turns_on_item: 1, turns_in_conversation: 1 }));
         fetchScript.turns[0].close();
      });

      await waitFor(() => expect(screen.getByTestId("agent-reply").textContent).toBe(WITHHELD));
   });

   it("says the third question on an item is the last, and holds Send until the screen changes", async () => {
      const { rerender } = render(<TutorHarness screen={UNCHECKED_ITEM} />);

      await openAndSend("Third try");
      await act(async () => {
         fetchScript.turns[0].push(frame("text", { delta: "Which rule applies?" }));
         fetchScript.turns[0].push(frame("end", { turn_id: "ATN-3", outcome: "complete", turns_on_item: 3, turns_in_conversation: 3 }));
         fetchScript.turns[0].close();
      });

      await waitFor(() => expect(screen.getByTestId("agent-send-reason").textContent).toBe(THIRD_TURN_CEILING));

      type("A fourth");

      expect(sendButton().disabled).toBe(true);

      rerender(<TutorHarness screen={CHECKED_ITEM} />);

      expect(sendButton().disabled).toBe(false);
   });

   it("renders a reply's formulas and holds an unclosed one back while it streams", async () => {
      render(<TutorHarness screen={{ kind: "today" }} />);

      await openAndSend("Show me");
      await act(async () => {
         fetchScript.turns[0].push(frame("text", { delta: "Look at \\(x^2" }));
      });

      await waitFor(() => expect(screen.getByTestId("agent-reply").textContent).toBe("Look at "));
      expect(screen.getByTestId("agent-reply").textContent).not.toContain("\\(");

      await act(async () => {
         fetchScript.turns[0].push(frame("text", { delta: "\\) first." }));
      });

      await waitFor(() => expect(screen.getByTestId("agent-reply").querySelector(".katex")).not.toBeNull());
      expect(screen.getByTestId("agent-reply").textContent).not.toContain("\\(");
   });
});

describe("the degraded states", () => {
   const errorCases = [
      { name: "usage limit", kind: "usage_limit", resets_at: null, serverCopy: "server words", copy: USAGE_LIMIT_UNKNOWN_RESET },
      { name: "daily cap", kind: "daily_cap", resets_at: null, serverCopy: "server words", copy: DAILY_CAP },
      { name: "minute cap", kind: "minute_cap", resets_at: null, serverCopy: "server words", copy: MINUTE_CAP },
      { name: "sign-in expired", kind: "sign_in", resets_at: null, serverCopy: "server words", copy: SIGN_IN_EXPIRED },
      { name: "timed part", kind: "timed", resets_at: null, serverCopy: "server words", copy: TIMED_PART },
      { name: "third turn on an item", kind: "ceiling", resets_at: null, serverCopy: THIRD_TURN_CEILING, copy: THIRD_TURN_CEILING },
      { name: "twentieth turn in a conversation", kind: "ceiling", resets_at: null, serverCopy: CONVERSATION_CEILING, copy: CONVERSATION_CEILING },
      { name: "unavailable", kind: "unavailable", resets_at: null, serverCopy: "server words", copy: OFFLINE },
      { name: "a screen the server could not use", kind: "refused", resets_at: null, serverCopy: "server words", copy: SCREEN_REFUSED }
   ];

   for (const errorCase of errorCases) {
      it(`${errorCase.name}: says why, disables Send and keeps what was typed`, async () => {
         render(<TutorHarness screen={UNCHECKED_ITEM} />);

         await openAndSend("My question");
         await act(async () => {
            fetchScript.turns[0].push(frame("error", { kind: errorCase.kind, resets_at: errorCase.resets_at, copy: errorCase.serverCopy }));
            fetchScript.turns[0].close();
         });

         await waitFor(() => expect(screen.getByTestId("agent-send-reason").textContent).toBe(errorCase.copy));
         expect(sendButton().disabled).toBe(true);
         expect(composer().value).toBe("My question");
      });
   }

   it("usage limit with a reset time names the time", async () => {
      const resetsAt = new Date(Date.now() + 3600000).toISOString();

      render(<TutorHarness screen={{ kind: "today" }} />);

      await openAndSend("My question");
      await act(async () => {
         fetchScript.turns[0].push(frame("error", { kind: "usage_limit", resets_at: resetsAt }));
         fetchScript.turns[0].close();
      });

      const expected = `The tutor cannot answer right now because the account's Claude usage limit has been reached. It will answer again after ${resetTimeText(resetsAt)}. Practice is not affected.`;

      await waitFor(() => expect(screen.getByTestId("agent-send-reason").textContent).toBe(expected));
      expect(sendButton().disabled).toBe(true);
   });

   it("usage limit with a reset time already past keeps its copy until the student edits", async () => {
      const resetsAt = new Date(Date.now() - 60000).toISOString();

      render(<TutorHarness screen={{ kind: "today" }} />);

      await openAndSend("My question");
      await act(async () => {
         fetchScript.turns[0].push(frame("error", { kind: "usage_limit", resets_at: resetsAt }));
         fetchScript.turns[0].close();
      });

      const expected = `The tutor cannot answer right now because the account's Claude usage limit has been reached. It will answer again after ${resetTimeText(resetsAt)}. Practice is not affected.`;

      await waitFor(() => expect(screen.getByTestId("agent-send-reason").textContent).toBe(expected));
      await act(async () => {
         await new Promise((resolve) => setTimeout(resolve, 20));
      });

      expect(screen.getByTestId("agent-send-reason").textContent).toBe(expected);

      type("My question, again");

      expect(screen.getByTestId("agent-send-reason").textContent).not.toBe(expected);
      expect(sendButton().disabled).toBe(false);
   });

   it("no connection: a refused fetch says so, disables Send and keeps what was typed", async () => {
      fetchScript.answerNextWith(() => Promise.reject(new TypeError("Failed to fetch")));
      render(<TutorHarness screen={{ kind: "today" }} />);

      await openAndSend("Are you there?");

      await waitFor(() => expect(screen.getByTestId("agent-send-reason").textContent).toBe(OFFLINE));
      expect(sendButton().disabled).toBe(true);
      expect(composer().value).toBe("Are you there?");
      expect(screen.queryByText("Are you there?", { selector: "p" })).toBeNull();
   });

   it("a 5xx is treated as no connection", async () => {
      fetchScript.answerNextWith(() => Promise.resolve({ ok: false, status: 502, body: null, json: async () => ({}) }));
      render(<TutorHarness screen={{ kind: "today" }} />);

      await openAndSend("Hello");

      await waitFor(() => expect(screen.getByTestId("agent-send-reason").textContent).toBe(OFFLINE));
      expect(composer().value).toBe("Hello");
   });

   it("a 4xx JSON body is read as the turn's error", async () => {
      fetchScript.answerNextWith(() => Promise.resolve({ ok: false, status: 429, body: null, json: async () => ({ kind: "daily_cap", copy: "server words" }) }));
      render(<TutorHarness screen={{ kind: "today" }} />);

      await openAndSend("Hello");

      await waitFor(() => expect(screen.getByTestId("agent-send-reason").textContent).toBe(DAILY_CAP));
      expect(sendButton().disabled).toBe(true);
   });

   it("no connection clears once the student edits what they typed", async () => {
      fetchScript.answerNextWith(() => Promise.reject(new TypeError("Failed to fetch")));
      render(<TutorHarness screen={{ kind: "today" }} />);

      await openAndSend("Retry me");
      await waitFor(() => expect(sendButton().disabled).toBe(true));

      type("Retry me again");

      expect(sendButton().disabled).toBe(false);
   });
});

describe("closing the conversation", () => {
   it("posts the close for the conversation the server opened and empties the panel", async () => {
      render(<TutorHarness screen={{ kind: "today" }} />);

      await openAndSend("Hi");
      await act(async () => {
         fetchScript.turns[0].push(frame("start", { conversation_id: "ACV-9", turn_id: "ATN-1", screen_line: "", can_see: [] }));
         fetchScript.turns[0].push(frame("text", { delta: "What is on screen?" }));
         fetchScript.turns[0].push(frame("end", { turn_id: "ATN-1", outcome: "complete", turns_on_item: 0, turns_in_conversation: 1 }));
         fetchScript.turns[0].close();
      });
      await waitFor(() => expect(screen.queryByRole("button", { name: "Stop" })).toBeNull());

      fetchScript.answerNextWith(() => Promise.resolve({ ok: true, status: 200, json: async () => ({ closed: "ACV-9" }) }));
      fireEvent.click(screen.getByRole("button", { name: "Close" }));

      await waitFor(() => expect(fetchScript.fetchStub).toHaveBeenCalledTimes(2));
      expect(fetchScript.fetchStub.mock.calls[1][0]).toBe("/agent/conversations/ACV-9/close");
      expect((fetchScript.fetchStub.mock.calls[1][1] as RequestInit).method).toBe("POST");
      expect(panel().hidden).toBe(true);
   });

   it("posts nothing when no conversation was opened", () => {
      render(<TutorHarness screen={{ kind: "today" }} />);

      fireEvent.click(askButton());
      fireEvent.click(screen.getByRole("button", { name: "Close" }));

      expect(fetchScript.fetchStub).not.toHaveBeenCalled();
      expect(panel().hidden).toBe(true);
   });
});

/* jsdom lays nothing out, so the conversation region is given a height and a content height, and
   its scrollTop is recorded. */
function laidOutConversation(clientHeight: number) {
   const region = screen.getByTestId("agent-conversation");
   const layout = { scrollHeight: clientHeight, scrollTop: 0 };
   const scrollTopWrites: number[] = [];

   Object.defineProperty(region, "clientHeight", { configurable: true, get: () => clientHeight });
   Object.defineProperty(region, "scrollHeight", { configurable: true, get: () => layout.scrollHeight });
   Object.defineProperty(region, "scrollTop", {
      configurable: true,
      get: () => layout.scrollTop,
      set: (value: number) => {
         layout.scrollTop = value;
         scrollTopWrites.push(value);
      }
   });

   return { region, layout, scrollTopWrites };
}

describe("the conversation region", () => {
   it("is the panel's scrolling region and follows a streaming reply to its newest line", async () => {
      render(<TutorHarness screen={{ kind: "today" }} />);

      await openAndSend("First");

      const { region, layout, scrollTopWrites } = laidOutConversation(200);

      expect(region.classList.contains("agent-conversation")).toBe(true);
      expect(within(panel()).getAllByTestId("agent-conversation")).toEqual([region]);

      layout.scrollHeight = 600;
      await act(async () => {
         fetchScript.turns[0].push(frame("start", { conversation_id: "ACV-1", turn_id: "ATN-1", screen_line: "", can_see: [] }));
         fetchScript.turns[0].push(frame("text", { delta: "A long first line." }));
      });

      await waitFor(() => expect(scrollTopWrites).toContain(600));
   });

   it("stops following once the student scrolls up, and follows again on the next send", async () => {
      render(<TutorHarness screen={{ kind: "today" }} />);

      await openAndSend("First");

      const { region, layout, scrollTopWrites } = laidOutConversation(200);

      layout.scrollHeight = 600;
      await act(async () => {
         fetchScript.turns[0].push(frame("start", { conversation_id: "ACV-1", turn_id: "ATN-1", screen_line: "", can_see: [] }));
         fetchScript.turns[0].push(frame("text", { delta: "A long first line." }));
      });
      await waitFor(() => expect(layout.scrollTop).toBe(600));

      layout.scrollTop = 100;
      fireEvent.scroll(region);
      scrollTopWrites.length = 0;
      layout.scrollHeight = 900;
      await act(async () => {
         fetchScript.turns[0].push(frame("text", { delta: " More text arrives." }));
         fetchScript.turns[0].push(frame("end", { turn_id: "ATN-1", outcome: "complete", turns_on_item: 0, turns_in_conversation: 1 }));
         fetchScript.turns[0].close();
      });
      await waitFor(() => expect(screen.queryByRole("button", { name: "Stop" })).toBeNull());

      expect(scrollTopWrites).toEqual([]);

      type("Second");
      fireEvent.keyDown(composer(), { key: "Enter" });

      await waitFor(() => expect(scrollTopWrites).toContain(900));
   });
});
