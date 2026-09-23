import { describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { AFFORDANCE_ATTRIBUTE, P1_FEEDBACK_AFFORDANCES } from "../affordances";
import { motionClass } from "../styles/motion";
import { ERROR_NOTE_LABEL, ErrorNoteField } from "./ErrorNoteField";

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
});