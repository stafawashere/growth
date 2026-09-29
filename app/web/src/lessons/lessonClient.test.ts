import { afterEach, describe, expect, it, vi } from "vitest";

import {
   answerLessonCheck,
   postLessonEvent,
   postSessionLessonEvent,
   readLesson,
   readLessonPlan,
   readLibrary
} from "../api/client";

/* The lessons endpoints of the framework contract (app/api/routes/lessons.py): each call names the
   path, the method and the body the route reads. */

function jsonResponse(body: unknown) {
   return new Response(JSON.stringify(body), { status: 200, headers: { "Content-Type": "application/json" } });
}

function issued(fetchMock: ReturnType<typeof vi.fn>) {
   const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];

   return { url, method: init.method ?? "GET", body: init.body === undefined ? undefined : JSON.parse(String(init.body)) };
}

async function call(run: () => Promise<unknown>) {
   const fetchMock = vi.fn().mockResolvedValue(jsonResponse({ ok: true }));

   vi.stubGlobal("fetch", fetchMock);
   await run();

   return issued(fetchMock);
}

afterEach(() => {
   vi.unstubAllGlobals();
});

describe("the lessons client", () => {
   it("reads the library, optionally for one unit", async () => {
      expect(await call(() => readLibrary())).toEqual({ url: "/lessons", method: "GET", body: undefined });
      expect((await call(() => readLibrary("BC-UNIT-06"))).url).toBe("/lessons?unit=BC-UNIT-06");
   });

   it("reads a lesson, optionally at the version seen, and its plan for a band and reason", async () => {
      expect((await call(() => readLesson("LSN-CON-02013"))).url).toBe("/lessons/LSN-CON-02013");
      expect((await call(() => readLesson("LSN-CON-02013", 2))).url).toBe("/lessons/LSN-CON-02013?version=2");
      expect((await call(() => readLessonPlan("LSN-CON-02013", "low"))).url).toBe("/lessons/LSN-CON-02013/plan?band=low");
      expect((await call(() => readLessonPlan("LSN-CON-02013", "mid", "read_again"))).url).toBe(
         "/lessons/LSN-CON-02013/plan?band=mid&reason=read_again"
      );
   });

   it("posts library and session events and a check answer", async () => {
      const body = { event: "section_viewed" as const, section_id: "LSN-CON-02013#s1", mode: "text", elapsed_ms: 900 };

      expect(await call(() => postLessonEvent("LSN-CON-02013", body))).toEqual({
         url: "/lessons/LSN-CON-02013/events",
         method: "POST",
         body
      });
      expect(await call(() => postSessionLessonEvent("SES-1", "LSN-CON-02013", body))).toEqual({
         url: "/sessions/SES-1/lessons/LSN-CON-02013/events",
         method: "POST",
         body
      });
      expect(
         await call(() => answerLessonCheck("LSN-CON-02013", "LSN-CON-02013#chk-3", { option_id: "C", elapsed_ms: 3000 }))
      ).toEqual({
         url: "/lessons/LSN-CON-02013/checks/LSN-CON-02013%23chk-3/answers",
         method: "POST",
         body: { option_id: "C", elapsed_ms: 3000 }
      });
   });
});
