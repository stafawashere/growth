import type { MePayload } from "../api/client";

/* The non-secret part of the account, kept in this browser so a reload draws the signed-in app at
   once while /me checks the session behind it (docs/plan/09-security-and-privacy.md, "Session
   lifetime"). The session token never comes here: it stays in the HttpOnly cookie. Storage can be
   missing, full or refused, so every read and write is guarded and a failure means no cache. */

export const ACCOUNT_CACHE_KEY = "growth-account";

export interface CachedAccount {
   id: string;
   username: string | null;
   displayName: string | null;
}

function isCachedAccount(value: unknown): value is CachedAccount {
   const isObject = typeof value === "object" && value !== null;

   if (!isObject) {
      return false;
   }

   const record = value as Record<string, unknown>;
   const hasId = typeof record.id === "string" && record.id !== "";
   const usernameIsValid = record.username === null || typeof record.username === "string";
   const displayNameIsValid = record.displayName === null || typeof record.displayName === "string";

   return hasId && usernameIsValid && displayNameIsValid;
}

export function readCachedAccount(): CachedAccount | null {
   try {
      const stored = window.localStorage.getItem(ACCOUNT_CACHE_KEY);

      if (stored === null) {
         return null;
      }

      const parsed: unknown = JSON.parse(stored);

      return isCachedAccount(parsed) ? parsed : null;
   } catch {
      return null;
   }
}

export function accountFrom(me: MePayload): CachedAccount {
   return { id: me.id, username: me.username ?? null, displayName: me.display_name };
}

export function saveCachedAccount(account: CachedAccount) {
   try {
      window.localStorage.setItem(ACCOUNT_CACHE_KEY, JSON.stringify(account));
   } catch {
      return;
   }
}

export function forgetCachedAccount() {
   try {
      window.localStorage.removeItem(ACCOUNT_CACHE_KEY);
   } catch {
      return;
   }
}

export function initialOf(account: CachedAccount | null) {
   const name = account?.displayName?.trim() || account?.username?.trim() || "";

   return name === "" ? "?" : name.charAt(0).toUpperCase();
}
