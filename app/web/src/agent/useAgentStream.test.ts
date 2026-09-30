import { act, renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { frame, scriptedFetch } from "../testing/agent";
import { createFrameParser, useAgentStream, type ServerSentEvent, type TurnHandlers } from "./useAgentStream";

function parse(chunks: string[]) {
   const frames: ServerSentEvent[] = [];
   const parser = createFrameParser((frame) => frames.push(frame));

   for (const chunk of chunks) {
      parser.push(chunk);
   }

   parser.finish();

   return frames;
}

describe("the server-sent event parser", () => {
   const stream = 'event: start\ndata: {"conversation_id":"ACV-1"}\n\nevent: text\ndata: {"delta":"Hi"}\n\n';
   const expected = [
      { event: "start", data: '{"conversation_id":"ACV-1"}' },
      { event: "text", data: '{"delta":"Hi"}' }
   ];

   it("reads every frame whatever the chunk boundaries, one character at a time included", () => {
      expect(parse([stream])).toEqual(expected);
      expect(parse(stream.split(""))).toEqual(expected);
      expect(parse([stream.slice(0, 20), stream.slice(20, 43), stream.slice(43)])).toEqual(expected);
   });

   it("reads CRLF line ends, joins multi-line data and skips comments", () => {
      const frames = parse([": keep-alive\r\n\r\nevent: text\r\ndata: one\r\ndata: two\r\n\r\n"]);

      expect(frames).toEqual([{ event: "text", data: "one\ntwo" }]);
   });

   it("keeps a frame whose blank line never came until the stream finishes", () => {
      expect(parse(['event: end\ndata: {"outcome":"complete"}'])).toEqual([{ event: "end", data: '{"outcome":"complete"}' }]);
   });
});

function recordingHandlers() {
   const calls: string[] = [];
   const handlers: TurnHandlers = {
      onStart: () => calls.push("start"),
      onText: () => calls.push("text"),
      onEnd: () => calls.push("end"),
      onFailure: () => calls.push("failure"),
      onStopped: () => calls.push("stopped")
   };

   return { calls, handlers };
}

const TURN_BODY = { screen: { kind: "today" as const }, message: "Hi", conversation_id: null };

const TIMEOUT_MILLISECONDS = 50;

describe("a turn after its end frame", () => {
   afterEach(() => {
      vi.useRealTimers();
      vi.unstubAllGlobals();
   });

   it("is read to its close and never aborted, by the first-text timer, by Stop or by unmounting", async () => {
      const fetchScript = scriptedFetch();

      vi.stubGlobal("fetch", fetchScript.fetchStub);

      const { result, unmount } = renderHook(() => useAgentStream(TIMEOUT_MILLISECONDS));
      const { calls, handlers } = recordingHandlers();
      let finished: Promise<void> = Promise.resolve();

      act(() => {
         finished = result.current.start(TURN_BODY, handlers);
      });
      await waitFor(() => expect(fetchScript.turns).toHaveLength(1));

      const turn = fetchScript.turns[0];

      await act(async () => {
         turn.push(frame("start", { conversation_id: "ACV-1", turn_id: "ATN-1", screen_line: "", can_see: [] }));
         turn.push(frame("end", { turn_id: "ATN-2", outcome: "complete", turns_on_item: 0, turns_in_conversation: 1 }));
      });
      await waitFor(() => expect(calls).toEqual(["start", "end"]));
      await waitFor(() => expect(result.current.isStreaming).toBe(false));

      await act(async () => {
         await new Promise((resolve) => setTimeout(resolve, TIMEOUT_MILLISECONDS * 2));
      });
      act(() => result.current.stop());
      unmount();

      expect(turn.signal().aborted).toBe(false);

      await act(async () => {
         turn.close();
         await finished;
      });

      expect(turn.signal().aborted).toBe(false);
      expect(calls).toEqual(["start", "end"]);
   });

   it("keeps Stop as an abort while the reply streams", async () => {
      const fetchScript = scriptedFetch();

      vi.stubGlobal("fetch", fetchScript.fetchStub);

      const { result } = renderHook(() => useAgentStream(TIMEOUT_MILLISECONDS * 100));
      const { calls, handlers } = recordingHandlers();
      let finished: Promise<void> = Promise.resolve();

      act(() => {
         finished = result.current.start(TURN_BODY, handlers);
      });
      await waitFor(() => expect(fetchScript.turns).toHaveLength(1));

      const turn = fetchScript.turns[0];

      await act(async () => {
         turn.push(frame("text", { delta: "Part of a reply" }));
      });
      await waitFor(() => expect(calls).toEqual(["text"]));

      await act(async () => {
         result.current.stop();
         await finished;
      });

      expect(turn.signal().aborted).toBe(true);
      expect(calls).toEqual(["text", "stopped"]);
   });
});

describe("a reply that draws", () => {
   afterEach(() => {
      vi.unstubAllGlobals();
   });

   function figureHandlers() {
      const calls: unknown[] = [];
      const handlers: TurnHandlers = {
         onStart: () => calls.push("start"),
         onText: (delta) => calls.push(["text", delta]),
         onEnd: () => calls.push("end"),
         onFailure: (failure) => calls.push(["failure", failure.kind]),
         onStopped: () => calls.push("stopped"),
         onFigurePending: () => calls.push("figure_pending"),
         onFigure: (spec) => calls.push(["figure", spec]),
         onFigureStep: (event) => calls.push(["figure_step", event]),
         onFigureRefused: (event) => calls.push(["figure_refused", event])
      };

      return { calls, handlers };
   }

   async function openTurn(timeoutMilliseconds: number) {
      const fetchScript = scriptedFetch();

      vi.stubGlobal("fetch", fetchScript.fetchStub);

      const { result, unmount } = renderHook(() => useAgentStream(timeoutMilliseconds));
      const { calls, handlers } = figureHandlers();

      act(() => {
         void result.current.start(TURN_BODY, handlers);
      });
      await waitFor(() => expect(fetchScript.turns).toHaveLength(1));

      return { turn: fetchScript.turns[0], calls, unmount };
   }

   async function waitPast(milliseconds: number) {
      await act(async () => {
         await new Promise((resolve) => setTimeout(resolve, milliseconds));
      });
   }

   const SPEC = { id: "figure", kind: "graph", title: "A curve" };

   it("hands each figure event to its own handler, in the order the frames came", async () => {
      const { turn, calls } = await openTurn(TIMEOUT_MILLISECONDS * 100);

      await act(async () => {
         turn.push(frame("text", { delta: "Look first." }));
         turn.push(frame("figure_pending", {}));
         turn.push(frame("figure", SPEC));
         turn.push(frame("figure_step", { figure: "figure", step: "curve" }));
         turn.push(frame("text", { delta: " The curve." }));
         turn.push(frame("figure_refused", { reason: "extra", copy: "The figure for this reply could not be drawn." }));
         turn.push(frame("end", { turn_id: "ATN-1", outcome: "complete", turns_on_item: 0, turns_in_conversation: 1 }));
      });

      await waitFor(() => expect(calls).toContain("end"));

      expect(calls).toEqual([
         ["text", "Look first."],
         "figure_pending",
         ["figure", SPEC],
         ["figure_step", { figure: "figure", step: "curve" }],
         ["text", " The curve."],
         ["figure_refused", { reason: "extra", copy: "The figure for this reply could not be drawn." }],
         "end"
      ]);
   });

   it("abandons a turn that sends nothing within the first-text wait", async () => {
      const { turn, calls, unmount } = await openTurn(TIMEOUT_MILLISECONDS);

      await waitPast(TIMEOUT_MILLISECONDS * 3);

      expect(turn.signal().aborted).toBe(true);
      expect(calls).toEqual([["failure", "offline"]]);

      unmount();
   });

   it("takes the opening of a figure, or the figure itself, as the reply having begun, so the first-text wait no longer applies", async () => {
      for (const [event, data] of [
         ["figure_pending", {}],
         ["figure", SPEC]
      ] as const) {
         const { turn, calls, unmount } = await openTurn(TIMEOUT_MILLISECONDS);

         await act(async () => {
            turn.push(frame(event, data));
         });
         await waitFor(() => expect(calls).toHaveLength(1));
         await waitPast(TIMEOUT_MILLISECONDS * 3);

         expect(turn.signal().aborted, event).toBe(false);
         expect(calls, event).not.toContainEqual(["failure", "offline"]);

         unmount();
      }
   });
});
