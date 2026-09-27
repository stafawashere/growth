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

function passwordRefused(detail: string) {
   return Object.assign(Object.create(client.ApiError.prototype), { status: 401, detail });
}

const TYPED_PASSWORD = "the password typed into the prompt";

async function confirmPassword() {
   const passwordField = await screen.findByLabelText("Password");

   fireEvent.change(passwordField, { target: { value: TYPED_PASSWORD } });
   fireEvent.click(screen.getByRole("button", { name: "Confirm" }));
}

async function closePrompt() {
   fireEvent.click(await screen.findByRole("button", { name: "Cancel" }));
}

function mockRoutes() {
   mocked.readProviders.mockResolvedValue({
      roles: [{ role: "tutor", provider: "anthropic", model: "claude-sonnet-5", wired: true }],
      chains: { tutor: ["subscription", "api"], grading: ["subscription", "api"] },
      cooling: []
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
   it("asks for the password, sends the fresh token with the cap, and shows the caps the server read back", async () => {
      mocked.reauthenticate.mockResolvedValue({ reauth_token: "token-cap" });
      mocked.updateBudget.mockResolvedValue(budgetsWith(7));

      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={vi.fn()} />);

      fireEvent.click(await screen.findByRole("button", { name: "open" }));
      fireEvent.change(screen.getByLabelText(/cap \$/), { target: { value: "4" } });
      fireEvent.click(capSave());
      await confirmPassword();

      await waitFor(() => expect(mocked.updateBudget).toHaveBeenCalledTimes(1));

      expect(mocked.reauthenticate).toHaveBeenCalledWith({ password: TYPED_PASSWORD });
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

   it("sends no cap change when the password prompt is closed, and hands the save back undone", async () => {
      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={vi.fn()} />);

      fireEvent.click(await screen.findByRole("button", { name: "open" }));
      fireEvent.change(screen.getByLabelText(/cap \$/), { target: { value: "4" } });

      const save = capSave();

      fireEvent.click(save);
      await closePrompt();

      await waitFor(() => expect(save.disabled).toBe(false));

      expect(mocked.reauthenticate).not.toHaveBeenCalled();
      expect(mocked.updateBudget).not.toHaveBeenCalled();
      expect(screen.queryByTestId("reauth-prompt")).toBeNull();
      expect(save.getAttribute("data-outcome")).toBeNull();
   });
});

describe("SettingsRoute, export", () => {
   it("asks for the password, requests the export with the token, fetches that archive and hands it to saveFile", async () => {
      const archive = new Blob(["{}"], { type: "application/json" });
      const saveFile = vi.fn();

      mocked.reauthenticate.mockResolvedValue({ reauth_token: "token-export" });
      mocked.requestExport.mockResolvedValue({ id: "JOB-1", status: "done", created_at: "2027-01-05T09:00:00" });
      mocked.readExport.mockResolvedValue(archive);

      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={saveFile} />);

      fireEvent.click(screen.getByRole("button", { name: "export" }));
      await confirmPassword();

      await waitFor(() => expect(saveFile).toHaveBeenCalledTimes(1));

      expect(mocked.requestExport).toHaveBeenCalledWith({ reauth_token: "token-export" });
      expect(mocked.readExport).toHaveBeenCalledWith("JOB-1");
      expect(saveFile).toHaveBeenCalledWith("growth-export-JOB-1.json", archive);
   });

   it("shows no done state and hands the export back when the server refuses the token with a 401", async () => {
      const saveFile = vi.fn();

      mocked.reauthenticate.mockResolvedValue({ reauth_token: "token-stale" });
      mocked.requestExport.mockRejectedValue(refused(401));

      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={saveFile} />);

      const exportButton = screen.getByRole("button", { name: "export" }) as HTMLButtonElement;

      fireEvent.click(exportButton);
      await confirmPassword();

      await waitFor(() => expect(mocked.requestExport).toHaveBeenCalledTimes(1));
      await waitFor(() => expect(exportButton.disabled).toBe(false));

      expect(exportButton.getAttribute("data-outcome")).toBeNull();
      expect(mocked.readExport).not.toHaveBeenCalled();
      expect(saveFile).not.toHaveBeenCalled();
   });

   it("marks the export done once the archive reached saveFile", async () => {
      mocked.reauthenticate.mockResolvedValue({ reauth_token: "token-export" });
      mocked.requestExport.mockResolvedValue({ id: "JOB-2", status: "done", created_at: "2027-01-05T09:00:00" });
      mocked.readExport.mockResolvedValue(new Blob(["{}"]));

      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={vi.fn()} />);

      const exportButton = screen.getByRole("button", { name: "export" }) as HTMLButtonElement;

      fireEvent.click(exportButton);
      await confirmPassword();

      await waitFor(() => expect(exportButton.getAttribute("data-outcome")).toBe("done"));
   });

   it("requests no export when the password prompt is closed", async () => {
      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={vi.fn()} />);

      const exportButton = screen.getByRole("button", { name: "export" }) as HTMLButtonElement;

      fireEvent.click(exportButton);
      await closePrompt();

      await waitFor(() => expect(exportButton.disabled).toBe(false));

      expect(mocked.requestExport).not.toHaveBeenCalled();
      expect(exportButton.getAttribute("data-outcome")).toBeNull();
   });

   it("keeps the prompt open with the server's refusal on a wrong password, and exports once the password is accepted", async () => {
      const detail = "the password is incorrect";
      const saveFile = vi.fn();

      mocked.reauthenticate
         .mockRejectedValueOnce(passwordRefused(detail))
         .mockResolvedValueOnce({ reauth_token: "token-second-try" });
      mocked.requestExport.mockResolvedValue({ id: "JOB-3", status: "done", created_at: "2027-01-05T09:00:00" });
      mocked.readExport.mockResolvedValue(new Blob(["{}"]));

      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={saveFile} />);

      fireEvent.click(screen.getByRole("button", { name: "export" }));
      await confirmPassword();

      expect((await within(screen.getByTestId("reauth-prompt")).findByRole("alert")).textContent).toBe(detail);
      expect(mocked.requestExport).not.toHaveBeenCalled();
      expect((screen.getByLabelText("Password") as HTMLInputElement).value).toBe("");

      await confirmPassword();

      await waitFor(() => expect(saveFile).toHaveBeenCalledTimes(1));

      expect(mocked.requestExport).toHaveBeenCalledWith({ reauth_token: "token-second-try" });
      expect(screen.queryByTestId("reauth-prompt")).toBeNull();
   });

   it("moves focus to the password field when the prompt opens", async () => {
      render(<SettingsRoute purgeConfirmationPhrase={null} saveFile={vi.fn()} />);

      fireEvent.click(screen.getByRole("button", { name: "export" }));

      const passwordField = await screen.findByLabelText("Password");

      expect(document.activeElement).toBe(passwordField);
      expect((passwordField as HTMLInputElement).autocomplete).toBe("current-password");
   });
});

describe("SettingsRoute, purge", () => {
   it("sends the typed confirmation with the token the verify step obtained", async () => {
      mocked.reauthenticate.mockResolvedValue({ reauth_token: "token-purge" });
      mocked.requestPurge.mockResolvedValue({ purged: true, deleted: {} });

      render(<SettingsRoute purgeConfirmationPhrase="PHRASE UNDER TEST" saveFile={vi.fn()} />);

      fireEvent.change(screen.getByLabelText(/type/i), { target: { value: "PHRASE UNDER TEST" } });
      fireEvent.click(screen.getByRole("button", { name: /verify identity/i }));
      await confirmPassword();

      const purgeButton = screen.getByRole("button", { name: /purge everything/i }) as HTMLButtonElement;

      await waitFor(() => expect(purgeButton.disabled).toBe(false));

      fireEvent.click(purgeButton);

      await waitFor(() => expect(mocked.requestPurge).toHaveBeenCalledTimes(1));

      expect(mocked.requestPurge).toHaveBeenCalledWith({
         confirmation: "PHRASE UNDER TEST",
         reauth_token: "token-purge"
      });
   });

   it("keeps purge disabled when the password is refused", async () => {
      mocked.reauthenticate.mockRejectedValue(passwordRefused("the password is incorrect"));

      render(<SettingsRoute purgeConfirmationPhrase="PHRASE UNDER TEST" saveFile={vi.fn()} />);

      fireEvent.change(screen.getByLabelText(/type/i), { target: { value: "PHRASE UNDER TEST" } });
      fireEvent.click(screen.getByRole("button", { name: /verify identity/i }));
      await confirmPassword();

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