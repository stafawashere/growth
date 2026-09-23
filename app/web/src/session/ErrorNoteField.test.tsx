import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { AFFORDANCE_ATTRIBUTE, P1_FEEDBACK_AFFORDANCES } from "../affordances";
import { motionClass } from "../styles/motion";
import { ERROR_NOTE_LABEL, ERROR_NOTE_MAX_CHARACTERS, ErrorNoteField } from "./ErrorNoteField";

const SERVICE_SOURCE = readFileSync(resolve(process.cwd(), "..", "..", "app/session/service.py"), "utf8");

function serverErrorNoteCap(): number {
   const declaration = SERVICE_SOURCE.match(/^ERROR_NOTE_MAX_CHARACTERS = (\d+)$/m);

   expect(declaration, "app/session/service.py declares ERROR_NOTE_MAX_CHARACTERS").not.toBeNull();

   return Number(declaration?.[1]);
}

describe("ErrorNoteField", () => {
   it("carries the error note affordance and its motion class", () => {
      render(<ErrorNoteField value="" onChange={vi.fn()} />);

      const panel = screen.getByTestId("error-note-field");

      expect(panel.getAttribute(AFFORDANCE_ATTRIBUTE)).toBe(P1_FEEDBACK_AFFORDANCES.errorNoteField);
      expect(panel.className).toContain(motionClass("errorNoteField"));

      cleanup();
   });

   it("asks for one line, in the student's voice", () => {
      render(<ErrorNoteField value="" onChange={vi.fn()} />);

      expect(ERROR_NOTE_LABEL).toBe("In one line, what went wrong?");
      expect(screen.getByLabelText(ERROR_NOTE_LABEL).tagName).toBe("INPUT");

      cleanup();
   });

   it("reports the note the student wrote", () => {
      const onChange = vi.fn();

      render(<ErrorNoteField value="" onChange={onChange} />);
      fireEvent.change(screen.getByLabelText(ERROR_NOTE_LABEL), { target: { value: "I multiplied the derivatives." } });

      expect(onChange).toHaveBeenCalledWith("I multiplied the derivatives.");

      cleanup();
   });

   it("carries the server's error note cap as its maxLength", () => {
      render(<ErrorNoteField value="" onChange={vi.fn()} />);

      expect(ERROR_NOTE_MAX_CHARACTERS).toBe(serverErrorNoteCap());
      expect(screen.getByLabelText(ERROR_NOTE_LABEL).getAttribute("maxLength")).toBe(
         String(ERROR_NOTE_MAX_CHARACTERS),
      );

      cleanup();
   });
});