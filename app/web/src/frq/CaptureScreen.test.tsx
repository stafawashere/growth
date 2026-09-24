import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";

import * as client from "../api/client";
import type { FrqAttempt, FrqQuestion, GradingsPayload, ReadBack } from "../api/types";
import { CaptureScreen } from "./CaptureScreen";

vi.mock("../api/client", async (importOriginal) => {
   const actual = await importOriginal<typeof client>();

   return {
      ...actual,
      startFrqAttempt: vi.fn(),
      uploadPhoto: vi.fn(),
      requestReadBack: vi.fn(),
      confirmReadBack: vi.fn(),
      submitTypedAnswer: vi.fn(),
      readGradings: vi.fn(),
      readReadBack: vi.fn(),
      askForReread: vi.fn()
   };
});

const mocked = vi.mocked(client);

const QUESTION: FrqQuestion = {
   id: "FRQ-AGT-05007-01",
   archetype_id: "BC-QA-05007",
   calculator_status: "no_calculator",
   stem: "The function g is defined by an integral.",
   parts: [
      { id: "a", prompt: "Find the critical point.", setup_required: false, points: 2 },
      { id: "b", prompt: "Classify it.", setup_required: false, points: 2 }
   ]
};

const READ_BACK: ReadBack = {
   parts: [
      { part_id: "a", lines: [{ kind: "math", content: "x = 3", crossed_out: false, outside_box: false }], answer: "x = 3" },
      { part_id: "b", lines: [{ kind: "text", content: "so a minimum", crossed_out: false, outside_box: false }], answer: "" }
   ],
   unreadable: []
};

function attempt(fields: Partial<FrqAttempt> = {}): FrqAttempt {
   return {
      attempt_id: "ATT-1",
      item_id: QUESTION.id,
      capture_mode: "photo",
      grading_state: "capturing",
      transcription_confirmed: false,
      read_back: null,
      confirmed: null,
      images: [],
      ...fields
   };
}

const GRADED: GradingsPayload = {
   attempt_id: "ATT-1",
   item_id: QUESTION.id,
   grading_state: "graded",
   points: [
      {
         grading_id: "GRD-1",
         part_id: "a",
         point_id: "a2",
         point_type_id: "BC-PT-99004",
         point_label: "Answer with or without supporting work",
         criterion: "Gives x = 3.",
         decided_by: "deterministic",
         earned: 1,
         provisional: false,
         rationale: "sympy_equivalence: x = 3 equals 3",
         evidence_quote: null,
         eligibility_note: null,
         rereads: 0
      },
      {
         grading_id: "GRD-2",
         part_id: "b",
         point_id: "b2",
         point_type_id: "BC-PT-99012",
         point_label: "Classification of a critical point by a derivative test",
         criterion: "Concludes a relative minimum with the sign change.",
         decided_by: "escalated",
         earned: null,
         provisional: true,
         rationale: "the gradings disagreed, 2 of 3 earned, so the point was sent for review rather than averaged",
         evidence_quote: "so a minimum",
         eligibility_note: null,
         rereads: 0
      }
   ],
   earned: 1,
   decided: 1,
   total: 2,
   provisional: 1,
   worked_solution: [],
   probe_scheduled: null
};

function photoFile() {
   return new File(["jpeg"], "page.jpg", { type: "image/jpeg" });
}

async function reachReadBack() {
   mocked.startFrqAttempt.mockResolvedValue(attempt());
   mocked.uploadPhoto.mockResolvedValue({ image_id: "IMG-1", accepted: true, reasons: [], measurements: {} });
   mocked.requestReadBack.mockResolvedValue(attempt({ read_back: READ_BACK, grading_state: "awaiting_confirmation" }));
   render(<CaptureScreen sessionId="SES-1" question={QUESTION} pollMilliseconds={5} readFile={async () => "anBlZw=="} />);

   fireEvent.click(screen.getByRole("button", { name: "Write on paper and photograph it" }));
   fireEvent.change(await screen.findByLabelText("Photo of the page"), { target: { files: [photoFile()] } });
   fireEvent.click(await screen.findByRole("button", { name: "Read my page" }));
   await screen.findByTestId("read-back-confirm");
}

describe("free-response capture", () => {
   beforeEach(() => {
      vi.clearAllMocks();
   });

   afterEach(() => {
      cleanup();
   });

   it("says what to fix on a rejected photo and offers no read-back until one passes", async () => {
      mocked.startFrqAttempt.mockResolvedValue(attempt());
      mocked.uploadPhoto.mockResolvedValue({
         image_id: "IMG-1",
         accepted: false,
         reasons: ["the photo is blurred; hold the phone still and let it focus"],
         measurements: {}
      });
      render(<CaptureScreen sessionId="SES-1" question={QUESTION} readFile={async () => "anBlZw=="} />);

      fireEvent.click(screen.getByRole("button", { name: "Write on paper and photograph it" }));
      fireEvent.change(await screen.findByLabelText("Photo of the page"), { target: { files: [photoFile()] } });

      expect(await screen.findByText(/hold the phone still/)).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Read my page" })).toBeNull();
      expect(mocked.requestReadBack).not.toHaveBeenCalled();
      expect(screen.getByRole("link", { name: "Print the answer page" }).getAttribute("href")).toBe("/attempts/ATT-1/booklet.png");
   });

   it("confirms nothing until a confidence is chosen, then confirms the read-back as read", async () => {
      await reachReadBack();

      const confirm = screen.getByRole("button", { name: "Yes, grade it" }) as HTMLButtonElement;

      expect(confirm.disabled).toBe(true);
      expect(screen.getByText("Nothing is scored until you confirm this.")).toBeTruthy();

      mocked.confirmReadBack.mockResolvedValue(attempt({ transcription_confirmed: true }));
      mocked.readGradings.mockResolvedValue(GRADED);
      fireEvent.click(screen.getByLabelText("unsure"));
      fireEvent.click(confirm);

      await waitFor(() => expect(mocked.confirmReadBack).toHaveBeenCalledWith("ATT-1", { confidence: "unsure" }));
   });

   it("sends the corrected read-back when the student fixes a line", async () => {
      await reachReadBack();
      mocked.confirmReadBack.mockResolvedValue(attempt({ transcription_confirmed: true }));
      mocked.readGradings.mockResolvedValue(GRADED);

      fireEvent.click(screen.getByRole("button", { name: "No, let me fix it" }));
      fireEvent.change(screen.getAllByLabelText("Line 1")[0], { target: { value: "x = 4" } });
      fireEvent.click(screen.getByLabelText("confident"));
      fireEvent.click(screen.getByRole("button", { name: "Grade what I wrote" }));

      await waitFor(() => expect(mocked.confirmReadBack).toHaveBeenCalled());

      const sent = mocked.confirmReadBack.mock.calls[0][1];

      expect(sent.read_back?.parts[0].lines[0].content).toBe("x = 4");
      expect(sent.confidence).toBe("confident");
   });

   it("shows a provisional point with the copy that it is not counted and a re-read on every point", async () => {
      await reachReadBack();
      mocked.confirmReadBack.mockResolvedValue(attempt({ transcription_confirmed: true }));
      mocked.readGradings.mockResolvedValue(GRADED);
      mocked.askForReread.mockResolvedValue({ grading_id: "GRD-2", attempt_id: "ATT-1", rereading: true });

      fireEvent.click(screen.getByLabelText("unsure"));
      fireEvent.click(screen.getByRole("button", { name: "Yes, grade it" }));

      expect(await screen.findByTestId("grading-summary")).toBeTruthy();
      expect(screen.getByTestId("grading-summary").textContent).toContain("1 of the 1 decided points earned, 1 provisional and not counted");
      expect(screen.getByTestId("provisional-copy").textContent).toContain("This point is provisional.");
      expect(screen.getAllByRole("button", { name: "Ask for a re-read" })).toHaveLength(2);
      expect(screen.queryByText(/AP score/)).toBeNull();

      fireEvent.click(screen.getAllByRole("button", { name: "Ask for a re-read" })[1]);

      await waitFor(() => expect(mocked.askForReread).toHaveBeenCalledWith("GRD-2"));
   });

   it("grades a typed answer without a photograph or a read-back", async () => {
      mocked.startFrqAttempt.mockResolvedValue(attempt({ capture_mode: "typed" }));
      mocked.submitTypedAnswer.mockResolvedValue(attempt({ capture_mode: "typed", transcription_confirmed: true }));
      mocked.readGradings.mockResolvedValue(GRADED);
      render(<CaptureScreen sessionId="SES-1" question={QUESTION} pollMilliseconds={5} />);

      fireEvent.click(screen.getByRole("button", { name: "Type my answer instead" }));
      expect(await screen.findByTestId("typed-entry")).toBeTruthy();

      fireEvent.click(screen.getAllByRole("button", { name: "Add a line of words" })[1]);
      fireEvent.change(screen.getByLabelText("Part (b), line 2, words"), { target: { value: "so a minimum" } });
      fireEvent.click(screen.getByLabelText("guess"));
      fireEvent.click(screen.getByRole("button", { name: "Grade my answer" }));

      await waitFor(() => expect(mocked.submitTypedAnswer).toHaveBeenCalled());

      const sent = mocked.submitTypedAnswer.mock.calls[0][1];

      expect(sent.read_back.parts[1].lines[1]).toEqual({ kind: "text", content: "so a minimum", crossed_out: false, outside_box: false });
      expect(mocked.requestReadBack).not.toHaveBeenCalled();
      expect(mocked.uploadPhoto).not.toHaveBeenCalled();
      expect(await screen.findByTestId("grading-summary")).toBeTruthy();
   });
});

describe("waiting on the grader", () => {
   beforeEach(() => {
      vi.clearAllMocks();
   });

   afterEach(() => {
      cleanup();
   });

   it("shows the re-read's result once it has run", async () => {
      await reachReadBack();
      mocked.confirmReadBack.mockResolvedValue(attempt({ transcription_confirmed: true }));
      const reread = {
         ...GRADED,
         earned: 2,
         decided: 2,
         provisional: 0,
         points: GRADED.points.map((point) =>
            point.grading_id === "GRD-2" ? { ...point, provisional: false, earned: 1, decided_by: "model", rereads: 1 } : point
         )
      };
      mocked.readGradings.mockResolvedValueOnce(GRADED).mockResolvedValueOnce(GRADED).mockResolvedValue(reread);
      mocked.askForReread.mockResolvedValue({ grading_id: "GRD-2", attempt_id: "ATT-1", rereading: true });

      fireEvent.click(screen.getByLabelText("unsure"));
      fireEvent.click(screen.getByRole("button", { name: "Yes, grade it" }));
      await screen.findByTestId("provisional-copy");
      fireEvent.click(screen.getAllByRole("button", { name: "Ask for a re-read" })[1]);

      await waitFor(() => expect(screen.queryByTestId("provisional-copy")).toBeNull());
      expect(screen.getByTestId("grading-summary").textContent).toContain("2 of the 2 decided points earned");
   });

   it("says grading stalled instead of waiting forever", async () => {
      await reachReadBack();
      mocked.confirmReadBack.mockResolvedValue(attempt({ transcription_confirmed: true }));
      mocked.readGradings.mockResolvedValue({ ...GRADED, grading_state: "confirmed", points: [] });

      fireEvent.click(screen.getByLabelText("unsure"));
      fireEvent.click(screen.getByRole("button", { name: "Yes, grade it" }));

      expect(await screen.findByText(/Grading has not finished/, undefined, { timeout: 4000 })).toBeTruthy();
   });

   it.each(["confirmed", "partly_graded", "graded"])(
      "reopens an attempt already %s on its grading, not on the photo step",
      async (state) => {
         mocked.startFrqAttempt.mockResolvedValue(attempt({ grading_state: state, transcription_confirmed: true, confirmed: READ_BACK }));
         mocked.readGradings.mockResolvedValue(GRADED);
         render(<CaptureScreen sessionId="SES-1" question={QUESTION} pollMilliseconds={5} captureMode="photo" />);

         expect(await screen.findByTestId("grading-summary")).toBeTruthy();
         expect(mocked.startFrqAttempt).toHaveBeenCalledWith("SES-1", QUESTION.id, "photo");
         expect(screen.queryByLabelText("Photo of the page")).toBeNull();
         expect(screen.queryByTestId("photo-capture")).toBeNull();
      }
   );

   it("offers to grade a reopened confirmed answer again when no point arrives, with the reason, using the stored read-back", async () => {
      mocked.startFrqAttempt.mockResolvedValue(attempt({ grading_state: "confirmed", transcription_confirmed: true, confirmed: READ_BACK }));
      mocked.readGradings.mockResolvedValue({ ...GRADED, grading_state: "confirmed", points: [] });
      mocked.readReadBack.mockResolvedValue(attempt({ grading_state: "confirmed", transcription_confirmed: true, confirmed: READ_BACK }));
      mocked.confirmReadBack.mockResolvedValue(attempt({ grading_state: "confirmed", transcription_confirmed: true }));
      render(<CaptureScreen sessionId="SES-1" question={QUESTION} pollMilliseconds={1} captureMode="photo" />);

      const stalled = await screen.findByTestId("grading-stalled", undefined, { timeout: 4000 });

      expect(stalled.textContent).toContain("no point has been graded after about five minutes");
      expect(screen.queryByTestId("photo-capture")).toBeNull();
      expect(mocked.confirmReadBack).not.toHaveBeenCalled();

      mocked.readGradings.mockResolvedValue(GRADED);
      fireEvent.click(screen.getByRole("button", { name: "Grade it again" }));

      await waitFor(() => expect(mocked.confirmReadBack).toHaveBeenCalledWith("ATT-1", { read_back: READ_BACK }));
      expect(await screen.findByTestId("grading-summary")).toBeTruthy();
   });
});
