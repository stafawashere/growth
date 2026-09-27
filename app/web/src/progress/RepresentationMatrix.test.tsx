import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import type { RepresentationMatrixPayload } from "../api/types";
import { RepresentationMatrix } from "./RepresentationMatrix";

function matrix(translationAttempts: number): RepresentationMatrixPayload {
   return {
      representations: [
         { id: "BC-REP-01", name: "Symbolic (analytical) expression" },
         { id: "BC-REP-02", name: "Graph" }
      ],
      cells: [{ source: "BC-REP-01", target: "BC-REP-02", attempts: translationAttempts, correct: 0 }],
      translation_attempts: translationAttempts,
      practice_attempts: 4
   };
}

afterEach(() => {
   cleanup();
});

describe("RepresentationMatrix", () => {
   it("keeps an empty table closed and opens it once a translation was attempted", () => {
      render(<RepresentationMatrix matrix={matrix(0)} />);

      expect((screen.getByTestId("representation-table") as HTMLDetailsElement).open).toBe(false);

      cleanup();
      render(<RepresentationMatrix matrix={matrix(2)} />);

      expect((screen.getByTestId("representation-table") as HTMLDetailsElement).open).toBe(true);
   });
});
