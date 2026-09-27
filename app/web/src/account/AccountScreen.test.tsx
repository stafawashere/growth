import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";

import { ACTION_FAILED_TEXT, LOAD_FAILED_TEXT, RETRY_LABEL } from "../status/LoadState";
import { AccountScreen } from "./AccountScreen";

const RECOVERY_CODE = "RC-served-by-signup";
const REPLACEMENT_RECOVERY_CODE = "RC-replacement";
const ENTERED_RECOVERY_CODE = "RC-typed-by-student";
const USERNAME = "calc_student";
const PASSWORD = "a long enough password";

type Status = { user_exists: boolean; needs_password?: boolean };

function jsonResponse(status: number, body: unknown) {
   return {
      ok: status >= 200 && status < 300,
      status,
      statusText: "",
      json: () => Promise.resolve(body)
   };
}

function signupResponse() {
   return jsonResponse(200, {
      user: { id: "USR-1", display_name: "student", exam_date: "2027-05-10", purge_after: "2027-06-09" },
      seeded_skill_states: 0,
      recovery_code: RECOVERY_CODE
   });
}

function resetResponse() {
   return jsonResponse(200, { user_id: "USR-1", recovery_code: REPLACEMENT_RECOVERY_CODE });
}

function serveStatus(status: Status, auth: ReturnType<typeof vi.fn> = vi.fn()) {
   return vi.fn((url: unknown, init?: RequestInit) => {
      const isStatusRequest = new URL(String(url), "http://x").pathname === "/auth/status";

      if (isStatusRequest) {
         return Promise.resolve(jsonResponse(200, status));
      }

      return auth(url, init);
   });
}

async function renderAccount(status: Status, auth?: ReturnType<typeof vi.fn>, onSignedIn: () => void = () => undefined) {
   const fetchMock = serveStatus(status, auth);

   vi.stubGlobal("fetch", fetchMock);
   render(<AccountScreen onSignedIn={onSignedIn} />);

   const firstControl = status.needs_password ? "Reset password" : status.user_exists ? "Sign in" : "Create account";

   await screen.findByRole("button", { name: firstControl });

   return fetchMock;
}

function authCalls(fetchMock: ReturnType<typeof vi.fn>) {
   return fetchMock.mock.calls.filter((call) => new URL(String(call[0]), "http://x").pathname !== "/auth/status");
}

function pathOf(call: unknown[]) {
   return new URL(String(call[0]), "http://x").pathname;
}

function bodyOf(call: unknown[]) {
   return JSON.parse((call[1] as RequestInit).body as string);
}

function neverAnswers() {
   return new Promise(() => undefined);
}

function field(label: string) {
   return screen.getByLabelText(label) as HTMLInputElement;
}

function button(name: string) {
   return screen.getByRole("button", { name }) as HTMLButtonElement;
}

function fillCredentials() {
   fireEvent.change(field("Username"), { target: { value: USERNAME } });
   fireEvent.change(field("Password"), { target: { value: PASSWORD } });
}

function fillRecovery() {
   fireEvent.change(field("Recovery code"), { target: { value: ENTERED_RECOVERY_CODE } });
   fireEvent.change(field("New password"), { target: { value: PASSWORD } });
}

beforeEach(() => {
   vi.unstubAllGlobals();
});

afterEach(() => {
   cleanup();
   vi.unstubAllGlobals();
});

describe("which form the screen offers", () => {
   it("asks /auth/status before offering anything", async () => {
      const statusServer = serveStatus({ user_exists: false });

      vi.stubGlobal("fetch", statusServer);
      render(<AccountScreen onSignedIn={() => undefined} />);

      await screen.findByRole("button", { name: "Create account" });

      expect(pathOf(statusServer.mock.calls[0])).toBe("/auth/status");
      expect(statusServer.mock.calls[0][1]?.method ?? "GET").toBe("GET");
   });

   it("offers sign-up only while the installation has no user", async () => {
      await renderAccount({ user_exists: false });

      expect(button("Create account")).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Sign in" })).toBeNull();
      expect(screen.queryByRole("button", { name: "Use recovery code" })).toBeNull();
   });

   it("offers sign-in and the recovery code, and no sign-up, once the installation has its user", async () => {
      await renderAccount({ user_exists: true });

      expect(button("Sign in")).toBeTruthy();
      expect(button("Use recovery code")).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Create account" })).toBeNull();
   });

   it("shows the reset form, with a username field and no way back to sign-in, when the account needs a password", async () => {
      await renderAccount({ user_exists: true, needs_password: true });

      expect(field("Recovery code")).toBeTruthy();
      expect(field("Username")).toBeTruthy();
      expect(field("New password")).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Sign in" })).toBeNull();
      expect(screen.queryByRole("button", { name: "Back to sign in" })).toBeNull();
   });

   it("shows the loading state and no form while the status is still unanswered", () => {
      vi.stubGlobal("fetch", vi.fn().mockReturnValue(neverAnswers()));
      render(<AccountScreen onSignedIn={() => undefined} />);

      expect(screen.getByTestId("account-waiting").getAttribute("aria-busy")).toBe("true");
      expect(screen.queryAllByRole("button")).toHaveLength(0);
      expect(screen.queryAllByRole("textbox")).toHaveLength(0);
   });

   it("says the status did not load, offers no form, and asks again on retry", async () => {
      const fetchMock = vi
         .fn()
         .mockResolvedValueOnce(jsonResponse(500, { detail: "the status could not be read" }))
         .mockResolvedValue(jsonResponse(200, { user_exists: true }));

      vi.stubGlobal("fetch", fetchMock);
      render(<AccountScreen onSignedIn={() => undefined} />);

      expect((await screen.findByRole("alert")).textContent).toBe(LOAD_FAILED_TEXT);
      expect(screen.getByTestId("account-failed")).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Sign in" })).toBeNull();

      fireEvent.click(button(RETRY_LABEL));

      expect(await screen.findByRole("button", { name: "Sign in" })).toBeTruthy();
      expect(fetchMock).toHaveBeenCalledTimes(2);
   });
});

describe("sign-up", () => {
   it("posts the username and password to /auth/signup", async () => {
      const auth = vi.fn().mockResolvedValue(signupResponse());
      const fetchMock = await renderAccount({ user_exists: false }, auth);

      fillCredentials();
      fireEvent.click(button("Create account"));

      await screen.findByText(RECOVERY_CODE);

      const [call] = authCalls(fetchMock);

      expect(pathOf(call)).toBe("/auth/signup");
      expect((call[1] as RequestInit).method).toBe("POST");
      expect(bodyOf(call)).toEqual({ username: USERNAME, password: PASSWORD });
   });

   it("shows the recovery code once and signs in only after the single acknowledgement", async () => {
      const onSignedIn = vi.fn();

      await renderAccount({ user_exists: false }, vi.fn().mockResolvedValue(signupResponse()), onSignedIn);
      fillCredentials();
      fireEvent.click(button("Create account"));

      expect(await screen.findByText(RECOVERY_CODE)).toBeTruthy();
      expect(screen.getAllByText(RECOVERY_CODE)).toHaveLength(1);
      expect(onSignedIn).not.toHaveBeenCalled();

      fireEvent.click(button("I have saved it"));

      expect(document.body.textContent ?? "").not.toContain(RECOVERY_CODE);
      expect(onSignedIn).toHaveBeenCalledTimes(1);
   });

   it("asks the browser for a new password and a username, not a stored one", async () => {
      await renderAccount({ user_exists: false });

      expect(field("Username").autocomplete).toBe("username");
      expect(field("Password").autocomplete).toBe("new-password");
      expect(field("Password").type).toBe("password");
   });

   it("disables the form while the request is in flight", async () => {
      await renderAccount({ user_exists: false }, vi.fn().mockReturnValue(neverAnswers()));
      fillCredentials();
      fireEvent.click(button("Create account"));

      expect(button("Create account").disabled).toBe(true);
      expect(field("Username").disabled).toBe(true);
      expect(field("Password").disabled).toBe(true);
   });

   it("shows the server's refusal and hands the form back", async () => {
      const detail = "a password of 12 to 128 characters is required";

      await renderAccount({ user_exists: false }, vi.fn().mockResolvedValue(jsonResponse(400, { detail })));
      fillCredentials();
      fireEvent.click(button("Create account"));

      expect((await screen.findByRole("alert")).textContent).toBe(detail);
      expect(button("Create account").disabled).toBe(false);
      expect(field("Username").value).toBe(USERNAME);
      expect(document.body.textContent ?? "").not.toContain(RECOVERY_CODE);
   });

   it("says the action did not go through when the request never reached the server", async () => {
      await renderAccount({ user_exists: false }, vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));
      fillCredentials();
      fireEvent.click(button("Create account"));

      expect((await screen.findByRole("alert")).textContent).toBe(ACTION_FAILED_TEXT);
      expect(button("Create account").disabled).toBe(false);
   });
});

describe("sign-in", () => {
   it("posts the username and password to /auth/login and signs in", async () => {
      const onSignedIn = vi.fn();
      const auth = vi.fn().mockResolvedValue(jsonResponse(200, { user_id: "USR-1" }));
      const fetchMock = await renderAccount({ user_exists: true }, auth, onSignedIn);

      fillCredentials();
      fireEvent.click(button("Sign in"));

      await waitFor(() => expect(onSignedIn).toHaveBeenCalledTimes(1));

      const [call] = authCalls(fetchMock);

      expect(pathOf(call)).toBe("/auth/login");
      expect(bodyOf(call)).toEqual({ username: USERNAME, password: PASSWORD });
   });

   it("asks the browser for the stored password", async () => {
      await renderAccount({ user_exists: true });

      expect(field("Username").autocomplete).toBe("username");
      expect(field("Password").autocomplete).toBe("current-password");
   });

   it("shows the refusal, clears the password, keeps the username and puts focus back on the password", async () => {
      const onSignedIn = vi.fn();
      const detail = "username or password is incorrect";

      await renderAccount({ user_exists: true }, vi.fn().mockResolvedValue(jsonResponse(401, { detail })), onSignedIn);
      fillCredentials();
      fireEvent.click(button("Sign in"));

      expect((await screen.findByRole("alert")).textContent).toBe(detail);
      expect(field("Password").value).toBe("");
      expect(field("Username").value).toBe(USERNAME);
      expect(onSignedIn).not.toHaveBeenCalled();

      await waitFor(() => expect(document.activeElement).toBe(field("Password")));
   });

   it("disables sign-in and the recovery link while the request is in flight", async () => {
      await renderAccount({ user_exists: true }, vi.fn().mockReturnValue(neverAnswers()));
      fillCredentials();
      fireEvent.click(button("Sign in"));

      expect(button("Sign in").disabled).toBe(true);
      expect(button("Use recovery code").disabled).toBe(true);
   });
});

describe("password reset by recovery code", () => {
   it("posts the typed code and the new password, then shows the replacement code once", async () => {
      const onSignedIn = vi.fn();
      const fetchMock = await renderAccount({ user_exists: true }, vi.fn().mockResolvedValue(resetResponse()), onSignedIn);

      fireEvent.click(button("Use recovery code"));
      fillRecovery();
      fireEvent.click(button("Reset password"));

      expect(await screen.findByText(REPLACEMENT_RECOVERY_CODE)).toBeTruthy();

      const [call] = authCalls(fetchMock);

      expect(pathOf(call)).toBe("/auth/recovery/reset");
      expect(bodyOf(call)).toEqual({ recovery_code: ENTERED_RECOVERY_CODE, new_password: PASSWORD });
      expect(screen.getAllByText(REPLACEMENT_RECOVERY_CODE)).toHaveLength(1);
      expect(onSignedIn).not.toHaveBeenCalled();

      fireEvent.click(button("I have saved it"));

      expect(document.body.textContent ?? "").not.toContain(REPLACEMENT_RECOVERY_CODE);
      expect(onSignedIn).toHaveBeenCalledTimes(1);
   });

   it("sends the chosen username when the account has no password yet", async () => {
      const fetchMock = await renderAccount({ user_exists: true, needs_password: true }, vi.fn().mockResolvedValue(resetResponse()));

      fillRecovery();
      fireEvent.change(field("Username"), { target: { value: USERNAME } });
      fireEvent.click(button("Reset password"));

      await screen.findByText(REPLACEMENT_RECOVERY_CODE);

      expect(bodyOf(authCalls(fetchMock)[0])).toEqual({
         recovery_code: ENTERED_RECOVERY_CODE,
         new_password: PASSWORD,
         username: USERNAME
      });
   });

   it("shows the server's refusal and re-enables the form", async () => {
      const detail = "recovery code is invalid or already used";

      await renderAccount({ user_exists: true }, vi.fn().mockResolvedValue(jsonResponse(401, { detail })));
      fireEvent.click(button("Use recovery code"));
      fillRecovery();
      fireEvent.click(button("Reset password"));

      expect((await screen.findByRole("alert")).textContent).toBe(detail);
      expect(button("Reset password").disabled).toBe(false);
      expect(field("Recovery code").disabled).toBe(false);
   });

   it("keeps the recovery code out of the browser's saved form history, since a saved code would defeat show-once", async () => {
      await renderAccount({ user_exists: true });
      fireEvent.click(button("Use recovery code"));

      expect(field("Recovery code").autocomplete).toBe("off");
      expect(field("New password").autocomplete).toBe("new-password");
   });

   it("writes no recovery code to local or session storage", async () => {
      await renderAccount({ user_exists: false }, vi.fn().mockResolvedValue(signupResponse()));
      fillCredentials();
      fireEvent.click(button("Create account"));
      await screen.findByText(RECOVERY_CODE);

      const stored = [localStorage, sessionStorage].flatMap((store) =>
         Array.from({ length: store.length }, (_, index) => store.getItem(store.key(index) as string) ?? "")
      );

      expect(stored.join(" ")).not.toContain(RECOVERY_CODE);
   });

   it("moves focus to the recovery-code input when the form opens", async () => {
      await renderAccount({ user_exists: true });
      fireEvent.click(button("Use recovery code"));

      await waitFor(() => expect(document.activeElement).toBe(field("Recovery code")));
   });

   it("moves focus to the acknowledgement button once the reset succeeds", async () => {
      await renderAccount({ user_exists: true }, vi.fn().mockResolvedValue(resetResponse()));
      fireEvent.click(button("Use recovery code"));
      fillRecovery();
      fireEvent.click(button("Reset password"));

      const acknowledgeButton = await screen.findByRole("button", { name: "I have saved it" });

      await waitFor(() => expect(document.activeElement).toBe(acknowledgeButton));
   });

   it("moves focus back to the recovery-code input when the server refuses the code", async () => {
      const detail = "recovery code is invalid or already used";

      await renderAccount({ user_exists: true }, vi.fn().mockResolvedValue(jsonResponse(401, { detail })));
      fireEvent.click(button("Use recovery code"));
      fillRecovery();
      fireEvent.click(button("Reset password"));

      await screen.findByRole("alert");

      await waitFor(() => expect(document.activeElement).toBe(field("Recovery code")));
   });

   it("goes back to sign-in without sending anything", async () => {
      const auth = vi.fn();

      await renderAccount({ user_exists: true }, auth);
      fireEvent.click(button("Use recovery code"));
      fireEvent.click(button("Back to sign in"));

      expect(button("Sign in")).toBeTruthy();
      expect(auth).not.toHaveBeenCalled();
   });
});

describe("the screen's landmark heading", () => {
   it("starts the sign-in screen at h1", async () => {
      await renderAccount({ user_exists: true });

      expect(screen.getByRole("heading", { level: 1, name: "Account" })).toBeTruthy();
   });

   it("starts the recovery screen at h1", async () => {
      await renderAccount({ user_exists: true });
      fireEvent.click(button("Use recovery code"));

      expect(screen.getByRole("heading", { level: 1, name: "Account" })).toBeTruthy();
   });

   it("starts the recovery-code screen at h1", async () => {
      await renderAccount({ user_exists: false }, vi.fn().mockResolvedValue(signupResponse()));
      fillCredentials();
      fireEvent.click(button("Create account"));

      expect(await screen.findByRole("heading", { level: 1, name: "Recovery code" })).toBeTruthy();
   });
});
