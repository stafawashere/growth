import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";

import * as client from "../api/client";
import type { ComingBackEntry, ErrorNoteEntry, ProvisionalPoint, ReviewPayload } from "../api/types";
import { ReviewRoute } from "./ReviewRoute";
import { ReviewScreen } from "./ReviewScreen";

vi.mock("../api/client", async (importOriginal) => {
   const actual = await importOriginal<typeof client>();

   return { ...actual, readReview: vi.fn(), submitErrorNote: vi.fn(), askForReread: vi.fn() };
});

const mocked = vi.mocked(client);

const COMING_BACK: ComingBackEntry[] = [
   {
      item_id: "ITM-1",
      attempt_id: "ATT-1",
      label: "Quotient rule, numerator order",
      lane: "hypercorrection",
      confidence: "confident",
      corrected_on: "2027-01-04",
      returns_on: "2027-01-05",
      days_until: 0
   },
   {
      item_id: "ITM-2",
      attempt_id: "ATT-2",
      label: "Implicit differentiation, dy/dx",
      lane: "requeue",
      confidence: "unsure",
      corrected_on: "2027-01-05",
      returns_on: "2027-01-06",
      days_until: 1
   },
   {
      item_id: "ITM-3",
      attempt_id: "ATT-3",
      label: "Limit by conjugate",
      lane: "requeue",
      confidence: null,
      corrected_on: "2027-01-05",
      returns_on: "2027-01-07",
      days_until: 2
   }
];

const NOTES: ErrorNoteEntry[] = [
   {
      attempt_id: "ATT-1",
      session_id: "SES-4",
      note: "I keep multiplying the two derivatives instead of using the product rule.",
      written_on: "2027-01-04",
      label: "Product rule"
   },
   {
      attempt_id: "ATT-7",
      session_id: "SES-3",
      note: "I forget the inner derivative when the inner function is linear.",
      written_on: "2027-01-02",
      label: "Chain rule"
   }
];

const POINT: ProvisionalPoint = {
   grading_id: "GRD-1",
   attempt_id: "ATT-9",
   label: "Question 3 part b",
   point_label: "justification point",
   reason: "Two gradings disagreed on whether the justification named the hypothesis.",
   disputed: false
};

function renderScreen(overrides: Partial<Parameters<typeof ReviewScreen>[0]> = {}) {
   const onSaveNote = vi.fn().mockResolvedValue(undefined);

   render(
      <ReviewScreen
         comingBack={COMING_BACK}
         errorNotes={NOTES}
         provisionalPoints={[]}
         onSaveNote={onSaveNote}
         {...overrides}
      />
   );

   return onSaveNote;
}

beforeEach(() => {
   vi.clearAllMocks();
});

afterEach(() => {
   cleanup();
});

describe("the review screen", () => {
   it("lists what is coming back in the order served, the confident error first, with when and how it was rated", () => {
      renderScreen();

      const rows = screen.getAllByTestId("coming-back");

      expect(rows.map((row) => row.getAttribute("data-lane"))).toEqual(["hypercorrection", "requeue", "requeue"]);
      expect(rows.map((row) => row.textContent)).toEqual([
         "todayQuotient rule, numerator order(was confident)",
         "tomorrowImplicit differentiation, dy/dx(was unsure)",
         "in 2 daysLimit by conjugate"
      ]);
   });

   it("says so when nothing is coming back", () => {
      renderScreen({ comingBack: [] });

      expect(screen.getByTestId("coming-back-empty")).toBeTruthy();
   });

   it("filters the error notes by what the search box holds, and says when nothing matches", () => {
      renderScreen();

      const search = screen.getByLabelText("Search my notes");

      fireEvent.change(search, { target: { value: "INNER" } });

      expect(screen.getAllByTestId("error-note").map((row) => within(row).getByText(/inner|product/).textContent)).toEqual([
         NOTES[1].note
      ]);

      fireEvent.change(search, { target: { value: "chain" } });

      expect(screen.getAllByTestId("error-note")).toHaveLength(1);

      fireEvent.change(search, { target: { value: "quotient" } });

      expect(screen.queryAllByTestId("error-note")).toHaveLength(0);
      expect(screen.getByTestId("error-notes-no-match")).toBeTruthy();
   });

   it("edits a note from the keyboard and hands the trimmed text to the save handler", async () => {
      const onSaveNote = renderScreen();

      fireEvent.click(screen.getByRole("button", { name: `Edit the note "${NOTES[0].note}"` }));

      const field = screen.getByLabelText("In one line, what went wrong?");

      fireEvent.change(field, { target: { value: "  I multiplied the derivatives.  " } });
      fireEvent.keyDown(field, { key: "Enter" });

      await waitFor(() => expect(screen.queryByLabelText("In one line, what went wrong?")).toBeNull());

      expect(onSaveNote).toHaveBeenCalledWith(NOTES[0], "I multiplied the derivatives.");
   });

   it("keeps the field open and shows why when the save is refused, and Escape abandons the edit", async () => {
      renderScreen({ onSaveNote: vi.fn().mockRejectedValue(new Error("the error note is one line")) });

      fireEvent.click(screen.getByRole("button", { name: `Edit the note "${NOTES[1].note}"` }));
      fireEvent.keyDown(screen.getByLabelText("In one line, what went wrong?"), { key: "Enter" });

      expect((await screen.findByRole("alert")).textContent).toBe("the error note is one line");

      fireEvent.keyDown(screen.getByLabelText("In one line, what went wrong?"), { key: "Escape" });

      expect(screen.queryByLabelText("In one line, what went wrong?")).toBeNull();
   });

   it("shows the provisional points empty state until P3 supplies points", () => {
      renderScreen();

      expect(screen.getByTestId("provisional-empty")).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Ask for a re-read" })).toBeNull();
   });

   it("offers a re-read on each provisional point only once P3 plugs a handler in", () => {
      const onAskForReread = vi.fn();

      renderScreen({ provisionalPoints: [POINT, { ...POINT, grading_id: "GRD-2", disputed: true }] });

      expect(screen.getAllByTestId("provisional-point")).toHaveLength(2);
      expect(screen.queryByRole("button", { name: "Ask for a re-read" })).toBeNull();

      cleanup();
      renderScreen({ provisionalPoints: [POINT, { ...POINT, grading_id: "GRD-2", disputed: true }], onAskForReread });

      const buttons = screen.getAllByRole("button", { name: "Ask for a re-read" });

      expect(buttons).toHaveLength(1);

      fireEvent.click(buttons[0]);

      expect(onAskForReread).toHaveBeenCalledWith("GRD-1");
   });
});

describe("the review route over GET /review", () => {
   const payload: ReviewPayload = {
      today: "2027-01-05",
      coming_back: COMING_BACK,
      error_notes: NOTES,
      grading_available: false,
      provisional_points: []
   };

   it("saves an edited note through the session route that wrote it and shows the stored text", async () => {
      mocked.readReview.mockResolvedValue(payload);
      mocked.submitErrorNote.mockResolvedValue({ id: "ATT-7", error_note: "I drop the inner derivative." });
      render(<ReviewRoute />);

      fireEvent.click(await screen.findByRole("button", { name: `Edit the note "${NOTES[1].note}"` }));
      fireEvent.change(screen.getByLabelText("In one line, what went wrong?"), {
         target: { value: "I drop the inner derivative" }
      });
      fireEvent.click(screen.getByRole("button", { name: "Save" }));

      expect(await screen.findByText("I drop the inner derivative.")).toBeTruthy();
      expect(mocked.submitErrorNote).toHaveBeenCalledWith("SES-3", "ATT-7", "I drop the inner derivative");
   });

   it("reaches every provisional point with a one-click re-read once grading is available", async () => {
      const provisional: ProvisionalPoint = {
         grading_id: "GRD-9",
         attempt_id: "ATT-9",
         label: "Critical point classified, part b",
         point_label: "Classification of a critical point",
         reason: "the gradings disagreed, 2 of 3 earned",
         disputed: false
      };
      mocked.readReview.mockResolvedValue({ ...payload, grading_available: true, provisional_points: [provisional] });
      mocked.askForReread.mockResolvedValue({ grading_id: "GRD-9", attempt_id: "ATT-9", rereading: true });
      render(<ReviewRoute />);

      fireEvent.click(await screen.findByRole("button", { name: "Ask for a re-read" }));

      await waitFor(() => expect(mocked.askForReread).toHaveBeenCalledWith("GRD-9"));
      expect(await screen.findByText("Re-read asked for")).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Ask for a re-read" })).toBeNull();
   });

   it("says the record could not be loaded when GET /review fails", async () => {
      mocked.readReview.mockRejectedValue(new Error("the connection dropped"));
      render(<ReviewRoute />);

      expect(await screen.findByTestId("review-failed")).toBeTruthy();
   });
});
