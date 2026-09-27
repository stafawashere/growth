import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";

import * as client from "../api/client";
import { ChangePasswordControl } from "./ChangePasswordControl";

vi.mock("../api/client");

const mocked = vi.mocked(client);

const CURRENT_PASSWORD = "the current password";
const NEW_PASSWORD = "the new password for this account";

function refusal(status: number, detail: string) {
   return Object.assign(Object.create(client.ApiError.prototype), { status, detail });
}

function field(label: string) {
   return screen.getByLabelText(label) as HTMLInputElement;
}

function changeButton() {
   return screen.getByRole("button", { name: "Change password" }) as HTMLButtonElement;
}

function submitChange() {
   fireEvent.change(field("Current password"), { target: { value: CURRENT_PASSWORD } });
   fireEvent.change(field("New password"), { target: { value: NEW_PASSWORD } });
   fireEvent.click(changeButton());
}

beforeEach(() => {
   vi.clearAllMocks();
});

afterEach(() => {
   cleanup();
});

describe("ChangePasswordControl", () => {
   it("re-authenticates with the current password, then spends that token on the change", async () => {
      mocked.reauthenticate.mockResolvedValue({ reauth_token: "token-change" });
      mocked.changePassword.mockResolvedValue({ password_changed: true });

      render(<ChangePasswordControl />);
      submitChange();

      await waitFor(() => expect(mocked.changePassword).toHaveBeenCalledTimes(1));

      expect(mocked.reauthenticate).toHaveBeenCalledWith({ password: CURRENT_PASSWORD });
      expect(mocked.changePassword).toHaveBeenCalledWith({
         current_password: CURRENT_PASSWORD,
         new_password: NEW_PASSWORD,
         reauth_token: "token-change"
      });
      expect(mocked.reauthenticate.mock.invocationCallOrder[0]).toBeLessThan(
         mocked.changePassword.mock.invocationCallOrder[0]
      );
   });

   it("says the password changed only after the server accepted it, and clears both fields", async () => {
      mocked.reauthenticate.mockResolvedValue({ reauth_token: "token-change" });
      mocked.changePassword.mockResolvedValue({ password_changed: true });

      render(<ChangePasswordControl />);

      expect(screen.getByRole("status").textContent).toBe("");

      submitChange();

      await waitFor(() => expect(screen.getByRole("status").textContent).toContain("Password changed."));

      expect(field("Current password").value).toBe("");
      expect(field("New password").value).toBe("");
   });

   it("sends no change and shows the refusal when the current password is wrong", async () => {
      const detail = "the password is incorrect";

      mocked.reauthenticate.mockRejectedValue(refusal(401, detail));

      render(<ChangePasswordControl />);
      submitChange();

      expect((await screen.findByRole("alert")).textContent).toBe(detail);
      expect(mocked.changePassword).not.toHaveBeenCalled();
      expect(screen.getByRole("status").textContent).toBe("");
      expect(changeButton().disabled).toBe(false);
   });

   it("shows the server's rule when the new password is refused", async () => {
      const detail = "a password of 12 to 128 characters is required";

      mocked.reauthenticate.mockResolvedValue({ reauth_token: "token-change" });
      mocked.changePassword.mockRejectedValue(refusal(400, detail));

      render(<ChangePasswordControl />);
      submitChange();

      expect((await screen.findByRole("alert")).textContent).toBe(detail);
      expect(screen.getByRole("status").textContent).toBe("");
   });

   it("disables the form while the change is in flight", () => {
      mocked.reauthenticate.mockReturnValue(new Promise(() => undefined));

      render(<ChangePasswordControl />);
      submitChange();

      expect(changeButton().disabled).toBe(true);
      expect(field("Current password").disabled).toBe(true);
      expect(field("New password").disabled).toBe(true);
   });

   it("asks the browser for the stored password and a new one", () => {
      render(<ChangePasswordControl />);

      expect(field("Current password").autocomplete).toBe("current-password");
      expect(field("New password").autocomplete).toBe("new-password");
   });
});
