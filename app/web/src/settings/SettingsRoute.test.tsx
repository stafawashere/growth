import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import * as client from "../api/client";
import type { BudgetsPayload, RoleBudget } from "../api/types";
import { SettingsRoute } from "./SettingsRoute";

vi.mock("../api/client");

const mocked = vi.mocked(client);

function roleBudget(capUsd: number): RoleBudget {
   return {
      role: "tutor",
      cap_usd: capUsd,
      cap_tokens: null,
      cost_usd: 0.25,
      tokens_in: 0,
      tokens_out: 0,
      tokens_cached_read: 0,
      tokens_cached_write: 0,
      hard_stopped: false
   };
}

function budgetsWith(capUsd: number): BudgetsPayload {
   return { day: "2027-01-05", roles: [roleBudget(capUsd)], month_to_date_usd: 1.75 };
}

function capSave() {
   return within(screen.getByTestId("per-role-cap-row")).getByRole("button", { name: "save" }) as HTMLButtonElement;
}

function refused(status: number) {
   return Object.assign(new Error("refused"), { status });
}

function mockRoutes() {
   mocked.readProviders.mockResolvedValue({
      roles: [{ role: "tutor", provider: "anthropic", model: "claude-sonnet-5", wired: true }]
   });
   mocked.readBudgets.mockResolvedValue(budgetsWith(2));
   mocked.readSettings.mockResolvedValue({
      exam_date: "2027-05-10",
      purge_after: "2027-06-09",
      desired_retention: 0.9
   });
}

beforeEach(() => {
   vi.clearAllMocks();
   mockRoutes();
});

afterEach(() => {
   cleanup();
});

describe("SettingsRoute, budget cap change", () => {
   it("re-authenticates, sends the fresh token with the cap, and shows the caps the server read back", async () => {
      mocked.reauthenticate.mockResolvedValue("token-cap");
      mocked.updateBudget.mockResolvedValue(budgetsWith(7));

      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={vi.fn()} />);

      fireEvent.click(await screen.findByRole("button", { name: "open" }));
      fireEvent.change(screen.getByLabelText(/cap \$/), { target: { value: "4" } });
      fireEvent.click(capSave());

      await waitFor(() => expect(mocked.updateBudget).toHaveBeenCalledTimes(1));

      expect(mocked.updateBudget).toHaveBeenCalledWith({
         role: "tutor",
         cap_usd: 4,
         cap_tokens: null,
         reauth_token: "token-cap"
      });
      expect(mocked.reauthenticate.mock.invocationCallOrder[0]).toBeLessThan(
         mocked.updateBudget.mock.invocationCallOrder[0]
      );

      await waitFor(() => {
         const capField = screen.getByLabelText(/cap \$/) as HTMLInputElement;

         expect(capField.value).toBe("7");
      });
   });

   it("sends no cap change when the passkey ceremony is declined, and hands the save back undone", async () => {
      mocked.reauthenticate.mockRejectedValue(new client.ReauthDeclined());

      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={vi.fn()} />);

      fireEvent.click(await screen.findByRole("button", { name: "open" }));
      fireEvent.change(screen.getByLabelText(/cap \$/), { target: { value: "4" } });

      const save = capSave();

      fireEvent.click(save);

      await waitFor(() => expect(mocked.reauthenticate).toHaveBeenCalledTimes(1));
      await waitFor(() => expect(save.disabled).toBe(false));

      expect(mocked.updateBudget).not.toHaveBeenCalled();
      expect(save.getAttribute("data-outcome")).toBeNull();
   });
});

describe("SettingsRoute, export", () => {
   it("re-authenticates, requests the export with the token, fetches that archive and hands it to saveFile", async () => {
      const archive = new Blob(["{}"], { type: "application/json" });
      const saveFile = vi.fn();

      mocked.reauthenticate.mockResolvedValue("token-export");
      mocked.requestExport.mockResolvedValue({ id: "JOB-1", status: "done", created_at: "2027-01-05T09:00:00" });
      mocked.readExport.mockResolvedValue(archive);

      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={saveFile} />);

      fireEvent.click(screen.getByRole("button", { name: "export" }));

      await waitFor(() => expect(saveFile).toHaveBeenCalledTimes(1));

      expect(mocked.requestExport).toHaveBeenCalledWith({ reauth_token: "token-export" });
      expect(mocked.readExport).toHaveBeenCalledWith("JOB-1");
      expect(saveFile).toHaveBeenCalledWith("growth-export-JOB-1.json", archive);
   });

   it("shows no done state and hands the export back when the server refuses the token with a 401", async () => {
      const saveFile = vi.fn();

      mocked.reauthenticate.mockResolvedValue("token-stale");
      mocked.requestExport.mockRejectedValue(refused(401));

      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={saveFile} />);

      const exportButton = screen.getByRole("button", { name: "export" }) as HTMLButtonElement;

      fireEvent.click(exportButton);

      await waitFor(() => expect(mocked.requestExport).toHaveBeenCalledTimes(1));
      await waitFor(() => expect(exportButton.disabled).toBe(false));

      expect(exportButton.getAttribute("data-outcome")).toBeNull();
      expect(mocked.readExport).not.toHaveBeenCalled();
      expect(saveFile).not.toHaveBeenCalled();
   });

   it("marks the export done once the archive reached saveFile", async () => {
      mocked.reauthenticate.mockResolvedValue("token-export");
      mocked.requestExport.mockResolvedValue({ id: "JOB-2", status: "done", created_at: "2027-01-05T09:00:00" });
      mocked.readExport.mockResolvedValue(new Blob(["{}"]));

      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={vi.fn()} />);

      const exportButton = screen.getByRole("button", { name: "export" }) as HTMLButtonElement;

      fireEvent.click(exportButton);

      await waitFor(() => expect(exportButton.getAttribute("data-outcome")).toBe("done"));
   });

   it("requests no export when the passkey ceremony is refused", async () => {
      mocked.reauthenticate.mockRejectedValue(new client.ReauthDeclined());

      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={vi.fn()} />);

      fireEvent.click(screen.getByRole("button", { name: "export" }));

      await waitFor(() => expect(mocked.reauthenticate).toHaveBeenCalledTimes(1));

      expect(mocked.requestExport).not.toHaveBeenCalled();
   });
});

describe("SettingsRoute, purge", () => {
   it("sends the typed confirmation with the token the verify step obtained", async () => {
      mocked.reauthenticate.mockResolvedValue("token-purge");
      mocked.requestPurge.mockResolvedValue({ purged: true, deleted: {} });

      render(<SettingsRoute purgeConfirmationPhrase="PHRASE UNDER TEST" saveFile={vi.fn()} />);

      fireEvent.change(screen.getByLabelText(/type/i), { target: { value: "PHRASE UNDER TEST" } });
      fireEvent.click(screen.getByRole("button", { name: /verify identity/i }));

      const purgeButton = screen.getByRole("button", { name: /purge everything/i }) as HTMLButtonElement;

      await waitFor(() => expect(purgeButton.disabled).toBe(false));

      fireEvent.click(purgeButton);

      await waitFor(() => expect(mocked.requestPurge).toHaveBeenCalledTimes(1));

      expect(mocked.requestPurge).toHaveBeenCalledWith({
         confirmation: "PHRASE UNDER TEST",
         reauth_token: "token-purge"
      });
   });

   it("keeps purge disabled when the passkey ceremony is refused", async () => {
      mocked.reauthenticate.mockRejectedValue(new client.ReauthDeclined());

      render(<SettingsRoute purgeConfirmationPhrase="PHRASE UNDER TEST" saveFile={vi.fn()} />);

      fireEvent.change(screen.getByLabelText(/type/i), { target: { value: "PHRASE UNDER TEST" } });
      fireEvent.click(screen.getByRole("button", { name: /verify identity/i }));

      await waitFor(() => expect(mocked.reauthenticate).toHaveBeenCalledTimes(1));

      const purgeButton = screen.getByRole("button", { name: /purge everything/i }) as HTMLButtonElement;

      expect(purgeButton.disabled).toBe(true);
      expect(mocked.requestPurge).not.toHaveBeenCalled();
   });
});

describe("SettingsRoute, queue and purge dates", () => {
   it("sends a changed exam date through PUT /settings and shows the date the server read back", async () => {
      mocked.updateSettings.mockResolvedValue({
         exam_date: "2028-05-09",
         purge_after: "2027-06-09",
         desired_retention: 0.9
      });

      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={vi.fn()} />);

      const field = within(await screen.findByTestId("date-field-exam date"));

      fireEvent.change(field.getByLabelText("exam date"), { target: { value: "2028-05-08" } });
      fireEvent.click(field.getByRole("button", { name: "save" }));

      await waitFor(() => expect(mocked.updateSettings).toHaveBeenCalledWith({ exam_date: "2028-05-08" }));
      await waitFor(() => expect((field.getByLabelText("exam date") as HTMLInputElement).value).toBe("2028-05-09"));
   });

   it("sends a changed purge date as purge_after", async () => {
      mocked.updateSettings.mockResolvedValue({
         exam_date: "2027-05-10",
         purge_after: "2028-06-07",
         desired_retention: 0.9
      });

      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={vi.fn()} />);

      const field = within(await screen.findByTestId("date-field-purge date"));

      fireEvent.change(field.getByLabelText("purge date"), { target: { value: "2028-06-07" } });
      fireEvent.click(field.getByRole("button", { name: "save" }));

      await waitFor(() => expect(mocked.updateSettings).toHaveBeenCalledWith({ purge_after: "2028-06-07" }));
   });
});