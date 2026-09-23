import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";

import { AddPasskeyControl } from "./AddPasskeyControl";

/* Base64url literals computed outside this suite, as in AccountScreen.test.tsx. */
const CHALLENGE = { text: "-_-_AD4_", bytes: [251, 255, 191, 0, 62, 63] };
const USER_HANDLE = { text: "VVNSLTE", bytes: [85, 83, 82, 45, 49] };
const CREDENTIAL = { text: "AKv-EA", bytes: [0, 171, 254, 16] };
const CLIENT_DATA = { text: "eyJ0In0", bytes: [123, 34, 116, 34, 125] };
const ATTESTATION = { text: "o2NmbXQ", bytes: [163, 99, 102, 109, 116] };
const REAUTH_CHALLENGE = { text: "AQID", bytes: [1, 2, 3] };
const REAUTH_TOKEN = "reauth-token-1";

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
      attestation: "none"
   };
}

function attestation() {
   return {
      id: CREDENTIAL.text,
      rawId: buffer(CREDENTIAL.bytes),
      type: "public-key",
      authenticatorAttachment: "cross-platform",
      response: {
         clientDataJSON: buffer(CLIENT_DATA.bytes),
         attestationObject: buffer(ATTESTATION.bytes),
         getTransports: () => ["hybrid"]
      },
      getClientExtensionResults: () => ({})
   };
}

function reauthAssertion() {
   return {
      id: "reauth-credential",
      rawId: buffer(REAUTH_CHALLENGE.bytes),
      type: "public-key",
      response: {
         clientDataJSON: buffer(CLIENT_DATA.bytes),
         authenticatorData: buffer([9]),
         signature: buffer([9, 9]),
         userHandle: null
      },
      getClientExtensionResults: () => ({})
   };
}

/* The add ceremony now needs a fresh re-authentication before it can finish (ruled 2026-09-23),
   so the fetch sequence is add/begin, reauth/begin, reauth/finish, add/finish. */
function addServer() {
   return vi
      .fn()
      .mockResolvedValueOnce(jsonResponse(200, { challenge_id: "CH-ADD", options: registrationOptions() }))
      .mockResolvedValueOnce(
         jsonResponse(200, {
            challenge_id: "CH-REAUTH",
            options: { challenge: REAUTH_CHALLENGE.text, allowCredentials: [], userVerification: "preferred" }
         })
      )
      .mockResolvedValueOnce(jsonResponse(200, { reauth_token: REAUTH_TOKEN }))
      .mockResolvedValueOnce(jsonResponse(200, { credential_id: "PKC-2" }));
}

function credentialsDouble(create: ReturnType<typeof vi.fn>) {
   return { credentials: { create, get: vi.fn().mockResolvedValue(reauthAssertion()) } };
}

function notAllowed() {
   return Promise.reject(new DOMException("The operation either timed out or was not allowed.", "NotAllowedError"));
}

function pathOf(fetchMock: ReturnType<typeof vi.fn>, callIndex: number) {
   return new URL(String(fetchMock.mock.calls[callIndex][0]), "http://x").pathname;
}

function addButton() {
   return screen.getByRole("button", { name: "Add a passkey" }) as HTMLButtonElement;
}

beforeEach(() => {
   vi.unstubAllGlobals();
});

afterEach(() => {
   cleanup();
   vi.unstubAllGlobals();
});

describe("adding a passkey while signed in", () => {
   it("runs the add ceremony with the decoded options and finishes with the attestation and a fresh reauth token", async () => {
      const fetchMock = addServer();
      const create = vi.fn().mockResolvedValue(attestation());

      vi.stubGlobal("fetch", fetchMock);
      vi.stubGlobal("navigator", credentialsDouble(create));

      render(<AddPasskeyControl />);
      fireEvent.click(addButton());

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(4));

      const publicKey = create.mock.calls[0][0].publicKey;
      const finish = JSON.parse(fetchMock.mock.calls[3][1].body);

      expect(Array.from(new Uint8Array(publicKey.challenge))).toEqual(CHALLENGE.bytes);
      expect(Array.from(new Uint8Array(publicKey.user.id))).toEqual(USER_HANDLE.bytes);
      expect(pathOf(fetchMock, 0)).toBe("/auth/passkey/add/begin");
      expect(pathOf(fetchMock, 1)).toBe("/auth/reauth/begin");
      expect(pathOf(fetchMock, 2)).toBe("/auth/reauth/finish");
      expect(pathOf(fetchMock, 3)).toBe("/auth/passkey/add/finish");
      expect(finish.challenge_id).toBe("CH-ADD");
      expect(finish.reauth_token).toBe(REAUTH_TOKEN);
      expect(finish.credential.rawId).toBe(CREDENTIAL.text);
      expect(finish.credential.response.clientDataJSON).toBe(CLIENT_DATA.text);
      expect(finish.credential.response.attestationObject).toBe(ATTESTATION.text);
      expect(finish.credential.response.transports).toEqual(["hybrid"]);
   });

   it("says the passkey was added only after the server accepts it", async () => {
      vi.stubGlobal("fetch", addServer());
      vi.stubGlobal("navigator", credentialsDouble(vi.fn().mockResolvedValue(attestation())));

      render(<AddPasskeyControl />);

      expect(screen.queryByRole("status")?.textContent ?? "").toBe("");

      fireEvent.click(addButton());

      await waitFor(() => expect(screen.getByRole("status").textContent).toBe("Passkey added."));
      expect(addButton().disabled).toBe(false);
   });

   it("disables the control while the ceremony runs", () => {
      vi.stubGlobal("fetch", vi.fn().mockReturnValue(new Promise(() => undefined)));
      vi.stubGlobal("navigator", credentialsDouble(vi.fn()));

      render(<AddPasskeyControl />);
      fireEvent.click(addButton());

      expect(addButton().disabled).toBe(true);
   });

   it("shows the server's refusal and reports nothing added", async () => {
      const detail = "this passkey is already registered";

      vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(409, { detail })));
      vi.stubGlobal("navigator", credentialsDouble(vi.fn()));

      render(<AddPasskeyControl />);
      fireEvent.click(addButton());

      expect((await screen.findByRole("alert")).textContent).toBe(detail);
      expect(document.body.textContent ?? "").not.toContain("Passkey added.");
      expect(addButton().disabled).toBe(false);
   });

   it("shows the server's refusal when re-authentication is stale, and reports nothing added", async () => {
      const detail = "adding a passkey needs a fresh passkey re-authentication";
      const fetchMock = vi
         .fn()
         .mockResolvedValueOnce(jsonResponse(200, { challenge_id: "CH-ADD", options: registrationOptions() }))
         .mockResolvedValueOnce(
            jsonResponse(200, {
               challenge_id: "CH-REAUTH",
               options: { challenge: REAUTH_CHALLENGE.text, allowCredentials: [], userVerification: "preferred" }
            })
         )
         .mockResolvedValueOnce(jsonResponse(200, { reauth_token: REAUTH_TOKEN }))
         .mockResolvedValueOnce(jsonResponse(401, { detail }));

      vi.stubGlobal("fetch", fetchMock);
      vi.stubGlobal("navigator", credentialsDouble(vi.fn().mockResolvedValue(attestation())));

      render(<AddPasskeyControl />);
      fireEvent.click(addButton());

      expect((await screen.findByRole("alert")).textContent).toBe(detail);
      expect(document.body.textContent ?? "").not.toContain("Passkey added.");
      expect(addButton().disabled).toBe(false);
   });

   it("returns to the control with no alert when the authenticator refuses", async () => {
      const fetchMock = addServer();

      vi.stubGlobal("fetch", fetchMock);
      vi.stubGlobal("navigator", { credentials: { create: vi.fn().mockImplementation(notAllowed) } });

      render(<AddPasskeyControl />);
      fireEvent.click(addButton());

      await waitFor(() => expect(addButton().disabled).toBe(false));

      expect(fetchMock).toHaveBeenCalledTimes(1);
      expect(screen.queryByRole("alert")).toBeNull();
      expect(document.body.textContent ?? "").not.toContain("Passkey added.");
   });
});