import { renderHook, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { useLoad } from "./load";

const payload = { lines: 3 };

function readPayload() {
   return Promise.resolve(payload);
}

describe("useLoad", () => {
   it("keeps the same value across renders until the load changes", async () => {
      const { result, rerender } = renderHook(() => useLoad(readPayload));

      await waitFor(() => expect(result.current.kind).toBe("loaded"));

      const loaded = result.current;

      rerender();

      expect(result.current).toBe(loaded);
   });
});
