import { describe, expect, it } from "vitest";

import { createFrameParser, type ServerSentEvent } from "./useAgentStream";

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
