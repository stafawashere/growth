import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";

import { AccountScreen } from "./AccountScreen";

/* Each base64url literal below was computed outside this suite, so the client's codec is checked
   against fixed text rather than against a second copy of itself. */
const CHALLENGE = { text: "-_-_AD4_", bytes: [251, 255, 191, 0, 62, 63] };
const USER_HANDLE = { text: "VVNSLTE", bytes: [85, 83, 82, 45, 49] };
const CREDENTIAL = { text: "AKv-EA", bytes: [0, 171, 254, 16], hex: "00abfe10" };
const CLIENT_DATA = { text: "eyJ0In0", bytes: [123, 34, 116, 34, 125] };
const ATTESTATION = { text: "o2NmbXQ", bytes: [163, 99, 102, 109, 116] };
const AUTHENTICATOR_DATA = { text: "--8", bytes: [251, 239] };
const SIGNATURE = { text: "BQYH", bytes: [5, 6, 7] };
const EXCLUDED = { text: "-AA", bytes: [248, 0] };

const RECOVERY_CODE = "RC-served-by-finish";
const REPLACEMENT_RECOVERY_CODE = "RC-replacement";
const ENTERED_RECOVERY_CODE = "RC-typed-by-student";

function buffer(bytes: number[]) {
   return new Uint8Array(bytes).buffer;
}

function jsonResponse(status: number, body: unknown) {
   return {
      ok: status >= 200 && status < 300,
      status,
      statusText: "",
      json: () => Promise.resolve(body)
   };
}

function registrationOptions() {
   return {
      rp: { name: "Growth", id: "localhost" },
      user: { id: USER_HANDLE.text, name: "student", displayName: "student" },
      challenge: CHALLENGE.text,
      pubKeyCredParams: [{ type: "public-key", alg: -7 }],
      timeout: 60000,
      excludeCredentials: [{ id: EXCLUDED.text, type: "public-key" }],
      attestation: "none"
   };
}

function attestation() {
   return {
      id: CREDENTIAL.text,
      rawId: buffer(CREDENTIAL.bytes),
      type: "public-key",
      authenticatorAttachment: "platform",
      response: {
         clientDataJSON: buffer(CLIENT_DATA.bytes),
         attestationObject: buffer(ATTESTATION.bytes),
         getTransports: () => ["internal"]
      },
      getClientExtensionResults: () => ({})
   };
}

function assertion() {
   return {
      id: CREDENTIAL.text,
      rawId: buffer(CREDENTIAL.bytes),
      type: "public-key",
      authenticatorAttachment: "platform",
      response: {
         clientDataJSON: buffer(CLIENT_DATA.bytes),
         authenticatorData: buffer(AUTHENTICATOR_DATA.bytes),
         signature: buffer(SIGNATURE.bytes),
         userHandle: buffer(USER_HANDLE.bytes)
      },
      getClientExtensionResults: () => ({})
   };
}

function registrationServer() {
   return vi
      .fn()
      .mockResolvedValueOnce(jsonResponse(200, { challenge_id: "CH-REG", options: registrationOptions() }))
      .mockResolvedValueOnce(
         jsonResponse(200, {
            user: { id: "USR-1", display_name: "student", exam_date: "2027-05-10", purge_after: "2027-06-09" },
            seeded_skill_states: 0,
            recovery_code: RECOVERY_CODE
         })
      );
}

function recoveryRegistrationServer() {
   return vi
      .fn()
      .mockResolvedValueOnce(jsonResponse(200, { challenge_id: "CH-RECOVERY", options: registrationOptions() }))
      .mockResolvedValueOnce(
         jsonResponse(200, {
            user_id: "USR-1",
            credential_id: CREDENTIAL.hex,
            recovery_code: REPLACEMENT_RECOVERY_CODE
         })
      );
}

function loginServer() {
   return vi
      .fn()
      .mockResolvedValueOnce(
         jsonResponse(200, { challenge_id: "CH-LOGIN", options: { challenge: CHALLENGE.text, userVerification: "preferred" } })
      )
      .mockResolvedValueOnce(jsonResponse(200, { user_id: "USR-1" }));
}

function serveStatus(userExists: boolean, ceremony: ReturnType<typeof vi.fn> = vi.fn()) {
   return vi.fn((url: unknown, init?: RequestInit) => {
      const isStatusRequest = new URL(String(url), "http://x").pathname === "/auth/status";

      if (isStatusRequest) {
         return Promise.resolve(jsonResponse(200, { user_exists: userExists }));
      }

      return ceremony(url, init);
   });
}

async function renderAccount(userExists: boolean, ceremony?: ReturnType<typeof vi.fn>, onSignedIn: () => void = () => undefined) {
   vi.stubGlobal("fetch", serveStatus(userExists, ceremony));
   render(<AccountScreen onSignedIn={onSignedIn} />);

   const firstControl = userExists ? "Sign in with a passkey" : "Register a passkey";

   await screen.findByRole("button", { name: firstControl });
}

function pathOf(fetchMock: ReturnType<typeof vi.fn>, callIndex: number) {
   return new URL(String(fetchMock.mock.calls[callIndex][0]), "http://x").pathname;
}

function bodyOf(fetchMock: ReturnType<typeof vi.fn>, callIndex: number) {
   return JSON.parse(fetchMock.mock.calls[callIndex][1].body);
}

function notAllowed() {
   return Promise.reject(new DOMException("The operation either timed out or was not allowed.", "NotAllowedError"));
}

function registerButton() {
   return screen.getByRole("button", { name: "Register a passkey" }) as HTMLButtonElement;
}

function signInButton() {
   return screen.getByRole("button", { name: "Sign in with a passkey" }) as HTMLButtonElement;
}

function recoveryEntryButton() {
   return screen.getByRole("button", { name: "Register a passkey with a recovery code" }) as HTMLButtonElement;
}

function recoveryCodeField() {
   return screen.getByLabelText("Recovery code") as HTMLInputElement;
}

function useRecoveryCodeButton() {
   return screen.getByRole("button", { name: "Use recovery code" }) as HTMLButtonElement;
}

function enterRecoveryScreen() {
   fireEvent.click(recoveryEntryButton());
   fireEvent.change(recoveryCodeField(), { target: { value: ENTERED_RECOVERY_CODE } });
}

beforeEach(() => {
   vi.unstubAllGlobals();
});

afterEach(() => {
   cleanup();
   vi.unstubAllGlobals();
});

describe("which ceremony the screen offers", () => {
   it("asks /auth/status before offering anything", async () => {
      const statusServer = serveStatus(false);

      vi.stubGlobal("fetch", statusServer);
      render(<AccountScreen onSignedIn={() => undefined} />);

      await screen.findByRole("button", { name: "Register a passkey" });

      expect(statusServer).toHaveBeenCalled();
      expect(pathOf(statusServer, 0)).toBe("/auth/status");
      expect(statusServer.mock.calls[0][1]?.method ?? "GET").toBe("GET");
   });

   it("offers registration only while the installation has no user", async () => {
      await renderAccount(false);

      expect(registerButton()).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Sign in with a passkey" })).toBeNull();
      expect(screen.queryByRole("button", { name: "Register a passkey with a recovery code" })).toBeNull();
   });

   it("offers sign-in and recovery, and no registration, once the installation has its user", async () => {
      await renderAccount(true);

      expect(signInButton()).toBeTruthy();
      expect(recoveryEntryButton()).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Register a passkey" })).toBeNull();
   });

   it("offers no ceremony while the status is still unanswered", () => {
      vi.stubGlobal("fetch", vi.fn().mockReturnValue(new Promise(() => undefined)));
      render(<AccountScreen onSignedIn={() => undefined} />);

      expect(screen.queryAllByRole("button")).toHaveLength(0);
   });

   it("shows the server's refusal and offers no ceremony when the status request fails", async () => {
      const detail = "the status could not be read";

      vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(500, { detail })));
      render(<AccountScreen onSignedIn={() => undefined} />);

      expect((await screen.findByRole("alert")).textContent).toBe(detail);
      expect(screen.queryAllByRole("button")).toHaveLength(0);
   });
});

describe("passkey registration", () => {
   it("hands the authenticator the decoded bytes and finishes with the attestation in base64url", async () => {
      const fetchMock = registrationServer();
      const create = vi.fn().mockResolvedValue(attestation());

      vi.stubGlobal("navigator", { credentials: { create } });

      await renderAccount(false, fetchMock);
      fireEvent.click(registerButton());

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));

      const publicKey = create.mock.calls[0][0].publicKey;

      expect(Array.from(new Uint8Array(publicKey.challenge))).toEqual(CHALLENGE.bytes);
      expect(Array.from(new Uint8Array(publicKey.user.id))).toEqual(USER_HANDLE.bytes);
      expect(Array.from(new Uint8Array(publicKey.excludeCredentials[0].id))).toEqual(EXCLUDED.bytes);
      expect(publicKey.rp).toEqual({ name: "Growth", id: "localhost" });
      expect(publicKey.pubKeyCredParams).toEqual([{ type: "public-key", alg: -7 }]);

      const finish = bodyOf(fetchMock, 1);

      expect(pathOf(fetchMock, 0)).toBe("/auth/passkey/register/begin");
      expect(pathOf(fetchMock, 1)).toBe("/auth/passkey/register/finish");
      expect(finish.challenge_id).toBe("CH-REG");
      expect(finish.credential.id).toBe(CREDENTIAL.text);
      expect(finish.credential.rawId).toBe(CREDENTIAL.text);
      expect(finish.credential.type).toBe("public-key");
      expect(finish.credential.response.clientDataJSON).toBe(CLIENT_DATA.text);
      expect(finish.credential.response.attestationObject).toBe(ATTESTATION.text);
      expect(finish.credential.response.transports).toEqual(["internal"]);
   });

   it("shows the recovery code once and signs in only after the single acknowledgement", async () => {
      const onSignedIn = vi.fn();

      vi.stubGlobal("navigator", { credentials: { create: vi.fn().mockResolvedValue(attestation()) } });

      await renderAccount(false, registrationServer(), onSignedIn);
      fireEvent.click(registerButton());

      expect(await screen.findByText(RECOVERY_CODE)).toBeTruthy();
      expect(screen.getAllByText(RECOVERY_CODE)).toHaveLength(1);
      expect(onSignedIn).not.toHaveBeenCalled();

      const acknowledgements = screen.getAllByRole("button");

      expect(acknowledgements).toHaveLength(1);

      fireEvent.click(acknowledgements[0]);

      expect(screen.queryByText(RECOVERY_CODE)).toBeNull();
      expect(document.body.textContent ?? "").not.toContain(RECOVERY_CODE);
      expect(onSignedIn).toHaveBeenCalledTimes(1);
   });

   it("leaves the button enabled with no recovery code when the authenticator refuses", async () => {
      const fetchMock = registrationServer();
      const onSignedIn = vi.fn();

      vi.stubGlobal("navigator", { credentials: { create: vi.fn().mockImplementation(notAllowed) } });

      await renderAccount(false, fetchMock, onSignedIn);
      fireEvent.click(registerButton());

      await waitFor(() => expect(registerButton().disabled).toBe(false));

      expect(screen.queryByRole("button", { name: "Sign in with a passkey" })).toBeNull();
      expect(fetchMock).toHaveBeenCalledTimes(1);
      expect(document.body.textContent ?? "").not.toContain(RECOVERY_CODE);
      expect(onSignedIn).not.toHaveBeenCalled();
   });

   it("disables registration while its ceremony is running", async () => {
      vi.stubGlobal("navigator", { credentials: { create: vi.fn() } });

      await renderAccount(false, vi.fn().mockReturnValue(new Promise(() => undefined)));
      fireEvent.click(registerButton());

      expect(registerButton().disabled).toBe(true);
   });

   it("shows the server's refusal when registration is closed", async () => {
      const detail = "registration is closed; this installation already has a user";

      vi.stubGlobal("navigator", { credentials: { create: vi.fn() } });

      await renderAccount(false, vi.fn().mockResolvedValue(jsonResponse(403, { detail })));
      fireEvent.click(registerButton());

      expect((await screen.findByRole("alert")).textContent).toBe(detail);
      expect(registerButton().disabled).toBe(false);
   });
});

describe("passkey sign-in", () => {
   it("hands the authenticator the decoded challenge and finishes with the assertion and a hex credential id", async () => {
      const fetchMock = loginServer();
      const get = vi.fn().mockResolvedValue(assertion());
      const onSignedIn = vi.fn();

      vi.stubGlobal("navigator", { credentials: { get } });

      await renderAccount(true, fetchMock, onSignedIn);
      fireEvent.click(signInButton());

      await waitFor(() => expect(onSignedIn).toHaveBeenCalledTimes(1));

      const publicKey = get.mock.calls[0][0].publicKey;
      const finish = bodyOf(fetchMock, 1);

      expect(Array.from(new Uint8Array(publicKey.challenge))).toEqual(CHALLENGE.bytes);
      expect(pathOf(fetchMock, 0)).toBe("/auth/passkey/login/begin");
      expect(pathOf(fetchMock, 1)).toBe("/auth/passkey/login/finish");
      expect(finish.challenge_id).toBe("CH-LOGIN");
      expect(finish.credential.credential_id).toBe(CREDENTIAL.hex);
      expect(finish.credential.rawId).toBe(CREDENTIAL.text);
      expect(finish.credential.response.clientDataJSON).toBe(CLIENT_DATA.text);
      expect(finish.credential.response.authenticatorData).toBe(AUTHENTICATOR_DATA.text);
      expect(finish.credential.response.signature).toBe(SIGNATURE.text);
      expect(finish.credential.response.userHandle).toBe(USER_HANDLE.text);
   });

   it("leaves the button enabled and signs nobody in when the authenticator refuses", async () => {
      const fetchMock = loginServer();
      const onSignedIn = vi.fn();

      vi.stubGlobal("navigator", { credentials: { get: vi.fn().mockImplementation(notAllowed) } });

      await renderAccount(true, fetchMock, onSignedIn);
      fireEvent.click(signInButton());

      await waitFor(() => expect(signInButton().disabled).toBe(false));

      expect(fetchMock).toHaveBeenCalledTimes(1);
      expect(onSignedIn).not.toHaveBeenCalled();
      expect(screen.queryByRole("alert")).toBeNull();
   });

   it("disables sign-in and recovery while the sign-in ceremony is running", async () => {
      vi.stubGlobal("navigator", { credentials: { get: vi.fn() } });

      await renderAccount(true, vi.fn().mockReturnValue(new Promise(() => undefined)));
      fireEvent.click(signInButton());

      expect(signInButton().disabled).toBe(true);
      expect(recoveryEntryButton().disabled).toBe(true);
   });
});

describe("passkey registration by recovery code", () => {
   it("finishes with the encoded credential and the typed code, then shows the replacement code once", async () => {
      const fetchMock = recoveryRegistrationServer();
      const onSignedIn = vi.fn();

      vi.stubGlobal("navigator", { credentials: { create: vi.fn().mockResolvedValue(attestation()) } });

      await renderAccount(true, fetchMock, onSignedIn);
      enterRecoveryScreen();
      fireEvent.click(useRecoveryCodeButton());

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));

      const finish = bodyOf(fetchMock, 1);

      expect(pathOf(fetchMock, 0)).toBe("/auth/recovery/register/begin");
      expect(pathOf(fetchMock, 1)).toBe("/auth/recovery/register/finish");
      expect(finish.challenge_id).toBe("CH-RECOVERY");
      expect(finish.recovery_code).toBe(ENTERED_RECOVERY_CODE);
      expect(finish.credential.id).toBe(CREDENTIAL.text);
      expect(finish.credential.rawId).toBe(CREDENTIAL.text);
      expect(finish.credential.type).toBe("public-key");
      expect(finish.credential.response.clientDataJSON).toBe(CLIENT_DATA.text);
      expect(finish.credential.response.attestationObject).toBe(ATTESTATION.text);

      expect(await screen.findByText(REPLACEMENT_RECOVERY_CODE)).toBeTruthy();
      expect(screen.getAllByText(REPLACEMENT_RECOVERY_CODE)).toHaveLength(1);
      expect(onSignedIn).not.toHaveBeenCalled();

      fireEvent.click(screen.getByRole("button", { name: "I have saved it" }));

      expect(screen.queryByText(REPLACEMENT_RECOVERY_CODE)).toBeNull();
      expect(document.body.textContent ?? "").not.toContain(REPLACEMENT_RECOVERY_CODE);
      expect(onSignedIn).toHaveBeenCalledTimes(1);
   });

   it("shows the server's refusal and re-enables the control on a 4xx response", async () => {
      const detail = "that recovery code has already been used";

      vi.stubGlobal("navigator", { credentials: { create: vi.fn() } });

      await renderAccount(true, vi.fn().mockResolvedValue(jsonResponse(403, { detail })));
      enterRecoveryScreen();
      fireEvent.click(useRecoveryCodeButton());

      expect((await screen.findByRole("alert")).textContent).toBe(detail);
      expect(useRecoveryCodeButton().disabled).toBe(false);
      expect(recoveryCodeField().disabled).toBe(false);
   });

   it("re-enables the control with no success state when the authenticator refuses", async () => {
      const fetchMock = recoveryRegistrationServer();
      const onSignedIn = vi.fn();

      vi.stubGlobal("navigator", { credentials: { create: vi.fn().mockImplementation(notAllowed) } });

      await renderAccount(true, fetchMock, onSignedIn);
      enterRecoveryScreen();
      fireEvent.click(useRecoveryCodeButton());

      await waitFor(() => expect(useRecoveryCodeButton().disabled).toBe(false));

      expect(recoveryCodeField().disabled).toBe(false);
      expect(fetchMock).toHaveBeenCalledTimes(1);
      expect(document.body.textContent ?? "").not.toContain(REPLACEMENT_RECOVERY_CODE);
      expect(onSignedIn).not.toHaveBeenCalled();
      expect(screen.queryByRole("alert")).toBeNull();
   });

   it("saves nothing to the browser's own store for a recovery code, since a saved code would defeat show-once", async () => {
      await renderAccount(true);
      enterRecoveryScreen();

      expect(recoveryCodeField().autocomplete).toBe("off");
   });

   it("moves focus to the acknowledgement button once the recovery ceremony succeeds", async () => {
      vi.stubGlobal("navigator", { credentials: { create: vi.fn().mockResolvedValue(attestation()) } });

      await renderAccount(true, recoveryRegistrationServer());
      enterRecoveryScreen();
      fireEvent.click(useRecoveryCodeButton());

      const acknowledgeButton = await screen.findByRole("button", { name: "I have saved it" });

      await waitFor(() => expect(document.activeElement).toBe(acknowledgeButton));
   });

   it("moves focus back to the recovery-code input when the server refuses the code", async () => {
      const detail = "that recovery code has already been used";

      vi.stubGlobal("navigator", { credentials: { create: vi.fn() } });

      await renderAccount(true, vi.fn().mockResolvedValue(jsonResponse(403, { detail })));
      enterRecoveryScreen();
      fireEvent.click(useRecoveryCodeButton());

      await screen.findByRole("alert");

      await waitFor(() => expect(document.activeElement).toBe(recoveryCodeField()));
   });

   it("moves focus back to the recovery-code input when the authenticator refuses", async () => {
      vi.stubGlobal("navigator", { credentials: { create: vi.fn().mockImplementation(notAllowed) } });

      await renderAccount(true, recoveryRegistrationServer());
      enterRecoveryScreen();
      fireEvent.click(useRecoveryCodeButton());

      await waitFor(() => expect(useRecoveryCodeButton().disabled).toBe(false));

      expect(document.activeElement).toBe(recoveryCodeField());
   });
});

describe("the screen's landmark heading", () => {
   it("starts the idle screen at h1, not h2, keeping the visible text unchanged", async () => {
      await renderAccount(true);

      expect(screen.getByRole("heading", { level: 1, name: "Account" })).toBeTruthy();
   });

   it("starts the recovery-entry screen at h1", async () => {
      await renderAccount(true);
      fireEvent.click(recoveryEntryButton());

      expect(screen.getByRole("heading", { level: 1, name: "Account" })).toBeTruthy();
   });

   it("starts the recovery-code screen at h1", async () => {
      vi.stubGlobal("navigator", { credentials: { create: vi.fn().mockResolvedValue(attestation()) } });

      await renderAccount(false, registrationServer());
      fireEvent.click(registerButton());

      expect(await screen.findByRole("heading", { level: 1, name: "Recovery code" })).toBeTruthy();
   });
});