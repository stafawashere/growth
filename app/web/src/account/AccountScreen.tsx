import { useEffect, useRef, useState, type FormEvent } from "react";

import {
   ApiError,
   readAuthStatus,
   registerPasskey,
   registerPasskeyWithRecoveryCode,
   signInWithPasskey
} from "../api/client";

export interface AccountScreenProps {
   onSignedIn: () => void;
}

type AccountState =
   | { kind: "idle"; refusal: string | null }
   | { kind: "working" }
   | { kind: "recoveryEntry"; refusal: string | null }
   | { kind: "recoveryCode"; code: string };

type InstallationStatus =
   | { kind: "unanswered" }
   | { kind: "answered"; userExists: boolean }
   | { kind: "unreadable"; refusal: string | null };

/* Only the server's own refusal is shown. An authenticator the student dismissed is not an error
   to report, so it returns the screen to where it was. */
function refusalFrom(failure: unknown) {
   const isServerRefusal = failure instanceof ApiError;

   return isServerRefusal ? failure.detail : null;
}

export function AccountScreen({ onSignedIn }: AccountScreenProps) {
   const [state, setState] = useState<AccountState>({ kind: "idle", refusal: null });
   const [installation, setInstallation] = useState<InstallationStatus>({ kind: "unanswered" });
   const [recoveryCodeInput, setRecoveryCodeInput] = useState("");
   const recoveryCodeInputRef = useRef<HTMLInputElement | null>(null);
   const acknowledgeButtonRef = useRef<HTMLButtonElement | null>(null);

   useEffect(() => {
      let isCurrent = true;

      readAuthStatus().then(
         (status) => {
            if (isCurrent) {
               setInstallation({ kind: "answered", userExists: status.user_exists });
            }
         },
         (failure) => {
            if (isCurrent) {
               setInstallation({ kind: "unreadable", refusal: refusalFrom(failure) });
            }
         }
      );

      return () => {
         isCurrent = false;
      };
   }, []);

   /* The working state renders neither the recovery form nor the recovery-code screen, so
      whichever of those two the ceremony lands back on has just been mounted fresh and keyboard
      focus is still on body. Move it to the control the student needs next. */
   useEffect(() => {
      if (state.kind === "recoveryCode") {
         acknowledgeButtonRef.current?.focus();
      }

      if (state.kind === "recoveryEntry") {
         recoveryCodeInputRef.current?.focus();
      }
   }, [state.kind]);

   async function runCeremony(ceremony: () => Promise<void>, onFailure: (refusal: string | null) => AccountState) {
      setState({ kind: "working" });

      try {
         await ceremony();
      } catch (failure) {
         setState(onFailure(refusalFrom(failure)));
      }
   }

   function register() {
      return runCeremony(
         async () => {
            const finished = await registerPasskey();

            setState({ kind: "recoveryCode", code: finished.recovery_code });
         },
         (refusal) => ({ kind: "idle", refusal })
      );
   }

   function signIn() {
      return runCeremony(
         async () => {
            await signInWithPasskey();

            setState({ kind: "idle", refusal: null });
            onSignedIn();
         },
         (refusal) => ({ kind: "idle", refusal })
      );
   }

   function openRecoveryEntry() {
      setState({ kind: "recoveryEntry", refusal: null });
   }

   function submitRecoveryCode(event: FormEvent) {
      event.preventDefault();

      return runCeremony(
         async () => {
            const finished = await registerPasskeyWithRecoveryCode(recoveryCodeInput);

            setRecoveryCodeInput("");
            setState({ kind: "recoveryCode", code: finished.recovery_code });
         },
         (refusal) => ({ kind: "recoveryEntry", refusal })
      );
   }

   function acknowledgeRecoveryCode() {
      setState({ kind: "idle", refusal: null });
      onSignedIn();
   }

   if (state.kind === "recoveryCode") {
      return (
         <section className="card">
            <h1 className="screen-title">Recovery code</h1>

            <p className="muted">This recovery code is shown once.</p>

            <p>
               <code>{state.code}</code>
            </p>

            <button
               type="button"
               className="button-primary"
               ref={acknowledgeButtonRef}
               onClick={acknowledgeRecoveryCode}
            >
               I have saved it
            </button>
         </section>
      );
   }

   const isWorking = state.kind === "working";

   if (state.kind === "recoveryEntry") {
      return (
         <section className="card">
            <h1 className="screen-title">Account</h1>

            <form className="field" onSubmit={submitRecoveryCode}>
               <label htmlFor="recovery-code-input">Recovery code</label>

               <input
                  id="recovery-code-input"
                  type="text"
                  autoComplete="off"
                  ref={recoveryCodeInputRef}
                  value={recoveryCodeInput}
                  disabled={isWorking}
                  onChange={(event) => setRecoveryCodeInput(event.target.value)}
               />

               <button type="submit" className="button-primary" disabled={isWorking}>
                  Use recovery code
               </button>
            </form>

            {state.refusal === null ? null : <p role="alert">{state.refusal}</p>}
         </section>
      );
   }

   const refusal = state.kind === "idle" ? state.refusal : null;
   const statusRefusal = installation.kind === "unreadable" ? installation.refusal : null;
   const isAnswered = installation.kind === "answered";
   const offersRegistration = isAnswered && !installation.userExists;
   const offersSignIn = isAnswered && installation.userExists;

   return (
      <section className="card">
         <h1 className="screen-title">Account</h1>

         {offersRegistration ? (
            <button type="button" className="button-primary" disabled={isWorking} onClick={register}>
               Register a passkey
            </button>
         ) : null}

         {offersSignIn ? (
            <button type="button" className="button-primary" disabled={isWorking} onClick={signIn}>
               Sign in with a passkey
            </button>
         ) : null}

         {offersSignIn ? (
            <button type="button" className="text-button" disabled={isWorking} onClick={openRecoveryEntry}>
               Register a passkey with a recovery code
            </button>
         ) : null}

         {statusRefusal === null ? null : <p role="alert">{statusRefusal}</p>}

         {refusal === null ? null : <p role="alert">{refusal}</p>}
      </section>
   );
}