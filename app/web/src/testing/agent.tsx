import { vi } from "vitest";

import type { AgentScreen } from "../api/types";
import { TopBar } from "../shell/TopBar";
import { AgentProvider, useAgentScreen } from "../agent/AgentProvider";
import type { ScreenLabels } from "../agent/screenLines";

/* Test support for the tutor panel: a shell with the Ask button, a page control to take focus, and
   a route that claims whatever screen the test gives it; and a fetch stand-in whose body is a
   stream the test writes server-sent event frames into, in whatever pieces it likes. */

export const UNCHECKED_ITEM: AgentScreen = {
   kind: "session_item",
   session_id: "SES-0123456789abcdef0123456789abcdef",
   attempt_id: "ATT-fedcba9876543210fedcba9876543210",
   item_id: "ITM-BC-0301-A",
   format: "mcq",
   served_stage: "unsupported",
   submitted: false
};

export const CHECKED_ITEM: AgentScreen = {
   ...UNCHECKED_ITEM,
   attempt_id: "ATT-0123456789abcdef0123456789abcdef",
   submitted: true,
   feedback_kind: "elaborated"
};

function Claim(props: { screen: AgentScreen | null; labels?: ScreenLabels }) {
   useAgentScreen(props.screen, props.labels);

   return null;
}

export function TutorHarness(props: { screen: AgentScreen | null; labels?: ScreenLabels }) {
   return (
      <AgentProvider enabled>
         <TopBar view="home" go={() => undefined} />

         <main className="app-page">
            <button type="button">Page control</button>

            <Claim screen={props.screen} labels={props.labels} />
         </main>
      </AgentProvider>
   );
}

export function frame(event: string, data: unknown) {
   return `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;
}

export interface ControlledTurn {
   push: (text: string) => void;
   close: () => void;
   signal: () => AbortSignal;
   body: () => unknown;
}

/* Each call to fetch gets the next scripted answer. A streamed answer stays open until the test
   closes it, and aborting the request errors the stream as a browser does. */
export function scriptedFetch() {
   const encoder = new TextEncoder();
   const turns: ControlledTurn[] = [];
   const answers: Array<() => Promise<unknown>> = [];

   const fetchStub = vi.fn((_path: string, init?: RequestInit) => {
      const next = answers.shift();

      if (next !== undefined) {
         return next();
      }

      let controller: ReadableStreamDefaultController<Uint8Array> | null = null;
      const body = new ReadableStream<Uint8Array>({
         start(streamController) {
            controller = streamController;
         }
      });
      const signal = init?.signal as AbortSignal;

      signal?.addEventListener("abort", () => {
         try {
            controller?.error(new DOMException("The operation was aborted.", "AbortError"));
         } catch {
            // already closed
         }
      });

      turns.push({
         push: (text) => controller?.enqueue(encoder.encode(text)),
         close: () => controller?.close(),
         signal: () => signal,
         body: () => JSON.parse(String(init?.body ?? "null"))
      });

      return Promise.resolve({ ok: true, status: 200, body, json: async () => ({}) } as unknown as Response);
   });

   function answerNextWith(answer: () => Promise<unknown>) {
      answers.push(answer);
   }

   return { fetchStub, turns, answerNextWith };
}
