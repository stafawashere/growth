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
