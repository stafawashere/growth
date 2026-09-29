import { useEffect, useRef, useState, type FormEvent, type Ref } from "react";

import { ApiError, readAuthStatus, resetWithRecoveryCode, signIn, signUp } from "../api/client";
import { Page, PageHeader } from "../ui/Page";
import { useLoad } from "../status/load";
import { ActionFailed, LoadFailed, Loading } from "../status/LoadState";

export interface AccountScreenProps {
   onSignedIn: () => void;
}

/* A server refusal is shown in the server's own words. A request that never reached the server
   is shown as the app's action failure, since there is no refusal to quote. */
export type Feedback = { kind: "none" } | { kind: "refused"; detail: string } | { kind: "failed" };

type AccountState =
   | { kind: "credentials"; working: boolean; feedback: Feedback }
   | { kind: "recovery"; working: boolean; feedback: Feedback }
   | { kind: "recoveryCode"; code: string };

export const NO_FEEDBACK: Feedback = { kind: "none" };

export function feedbackFrom(failure: unknown): Feedback {
   const isServerRefusal = failure instanceof ApiError;

   return isServerRefusal ? { kind: "refused", detail: failure.detail } : { kind: "failed" };
}

export function FeedbackLine(props: { feedback: Feedback }) {
   const { feedback } = props;

   if (feedback.kind === "refused") {
      return (
         <p role="alert" className="field-error">
            {feedback.detail}
         </p>
      );
   }

   if (feedback.kind === "failed") {
      return <ActionFailed />;
   }

   return null;
}

function PasswordField(props: {
   id: string;
   inputRef?: Ref<HTMLInputElement>;
   label: string;
   autoComplete: "new-password" | "current-password";
   value: string;
   disabled: boolean;
   onChange: (value: string) => void;
}) {
   return (
      <div className="form-field">
         <label className="field-label" htmlFor={props.id}>
            {props.label}
         </label>

         <input
            id={props.id}
            className="input"
            type="password"
            autoComplete={props.autoComplete}
            ref={props.inputRef}
            value={props.value}
            disabled={props.disabled}
            onChange={(event) => props.onChange(event.target.value)}
         />
      </div>
   );
}

function UsernameField(props: {
   value: string;
   disabled: boolean;
   inputRef?: Ref<HTMLInputElement>;
   onChange: (value: string) => void;
}) {
   return (
      <div className="form-field">
         <label className="field-label" htmlFor="account-username">
            Username
         </label>

         <input
            id="account-username"
            className="input"
            type="text"
            autoComplete="username"
            autoCapitalize="none"
            spellCheck={false}
            ref={props.inputRef}
            value={props.value}
            disabled={props.disabled}
            onChange={(event) => props.onChange(event.target.value)}
         />
      </div>
   );
}

export function AccountScreen({ onSignedIn }: AccountScreenProps) {
   const status = useLoad(readAuthStatus);
   const [state, setState] = useState<AccountState>({ kind: "credentials", working: false, feedback: NO_FEEDBACK });
   const [username, setUsername] = useState("");
   const [password, setPassword] = useState("");
   const [recoveryCode, setRecoveryCode] = useState("");
   const recoveryCodeInputRef = useRef<HTMLInputElement | null>(null);
   const passwordInputRef = useRef<HTMLInputElement | null>(null);
   const acknowledgeButtonRef = useRef<HTMLButtonElement | null>(null);

   const needsPassword = status.kind === "loaded" && status.value.needs_password === true;
   const showsRecovery = state.kind === "recovery" || (state.kind === "credentials" && needsPassword);
   const recoveryFeedback = state.kind === "recovery" ? state.feedback : NO_FEEDBACK;
   const recoveryIsWorking = state.kind === "recovery" && state.working;

   /* A form that lands back after a request keeps the student's place, so focus goes to the
      control they need next rather than staying on a button that was disabled. */
   useEffect(() => {
      if (state.kind === "recoveryCode") {
         acknowledgeButtonRef.current?.focus();
      }
   }, [state.kind]);

   useEffect(() => {
      const shouldFocusCode = state.kind === "recovery" && !state.working;

      if (shouldFocusCode) {
         recoveryCodeInputRef.current?.focus();
      }
   }, [state.kind, recoveryIsWorking, recoveryFeedback]);

   const credentialsFeedback = state.kind === "credentials" ? state.feedback : NO_FEEDBACK;

   useEffect(() => {
      const wasRefused = credentialsFeedback.kind !== "none";

      if (wasRefused) {
         passwordInputRef.current?.focus();
      }
   }, [credentialsFeedback]);

   async function submitCredentials(event: FormEvent, userExists: boolean) {
      event.preventDefault();
      setState({ kind: "credentials", working: true, feedback: NO_FEEDBACK });

      const fields = { username, password };

      try {
         if (userExists) {
            await signIn(fields);

            setPassword("");
            setState({ kind: "credentials", working: false, feedback: NO_FEEDBACK });
            onSignedIn();

            return;
         }

         const finished = await signUp(fields);

         setPassword("");
         setState({ kind: "recoveryCode", code: finished.recovery_code });
      } catch (failure) {
         setPassword("");
         setState({ kind: "credentials", working: false, feedback: feedbackFrom(failure) });
      }
   }

   async function submitRecovery(event: FormEvent) {
      event.preventDefault();
      setState({ kind: "recovery", working: true, feedback: NO_FEEDBACK });

      const hasUsername = username.trim() !== "";
      const sendsUsername = needsPassword && hasUsername;
      const fields = sendsUsername
         ? { recovery_code: recoveryCode, new_password: password, username }
         : { recovery_code: recoveryCode, new_password: password };

      try {
         const finished = await resetWithRecoveryCode(fields);

         setRecoveryCode("");
         setPassword("");
         setState({ kind: "recoveryCode", code: finished.recovery_code });
      } catch (failure) {
         setPassword("");
         setState({ kind: "recovery", working: false, feedback: feedbackFrom(failure) });
      }
   }

   function openRecovery() {
      setPassword("");
      setState({ kind: "recovery", working: false, feedback: NO_FEEDBACK });
   }

   function closeRecovery() {
      setPassword("");
      setRecoveryCode("");
      setState({ kind: "credentials", working: false, feedback: NO_FEEDBACK });
   }

   function acknowledgeRecoveryCode() {
      setState({ kind: "credentials", working: false, feedback: NO_FEEDBACK });
      onSignedIn();
   }

   if (state.kind === "recoveryCode") {
      return (
         <Page header={<PageHeader eyebrow="Growth account" title="Recovery code" intro="This recovery code is shown once. Keep it somewhere safe and apart from this device." />}>
            <div className="stack">
               <p className="code-block">
                  <code>{state.code}</code>
               </p>

               <button type="button" className="button-primary button-block" ref={acknowledgeButtonRef} onClick={acknowledgeRecoveryCode}>
                  I have saved it
               </button>
            </div>
         </Page>
      );
   }

   if (status.kind === "waiting") {
      return <Loading testId="account-waiting" />;
   }

   if (status.kind === "failed") {
      return <LoadFailed testId="account-failed" onRetry={status.retry} />;
   }

   if (showsRecovery) {
      return (
         <Page
            header={
               <PageHeader
                  eyebrow="Recover your account"
                  title="Account"
                  intro={
                     needsPassword
                        ? "This account has no password yet. Enter your recovery code and choose a username and a password."
                        : "A recovery code sets a new password and gives you a fresh code."
                  }
               />
            }
         >
            <div className="stack stack-loose">
               <form className="stack" onSubmit={submitRecovery}>
                  <div className="form-field">
                     <label className="field-label" htmlFor="recovery-code-input">
                        Recovery code
                     </label>

                     <input
                        id="recovery-code-input"
                        className="input"
                        type="text"
                        autoComplete="off"
                        autoCapitalize="none"
                        spellCheck={false}
                        ref={recoveryCodeInputRef}
                        value={recoveryCode}
                        disabled={recoveryIsWorking}
                        onChange={(event) => setRecoveryCode(event.target.value)}
                     />
                  </div>

                  {needsPassword ? <UsernameField value={username} disabled={recoveryIsWorking} onChange={setUsername} /> : null}

                  <PasswordField
                     id="recovery-new-password"
                     label="New password"
                     autoComplete="new-password"
                     value={password}
                     disabled={recoveryIsWorking}
                     onChange={setPassword}
                  />

                  <button type="submit" className="button-primary button-block" disabled={recoveryIsWorking}>
                     Reset password
                  </button>
               </form>

               {needsPassword ? null : (
                  <div className="cluster">
                     <button type="button" className="text-button" disabled={recoveryIsWorking} onClick={closeRecovery}>
                        Back to sign in
                     </button>
                  </div>
               )}

               <FeedbackLine feedback={recoveryFeedback} />
            </div>
         </Page>
      );
   }

   const userExists = status.value.user_exists;
   const isWorking = state.working;
   const submitLabel = userExists ? "Sign in" : "Create account";

   return (
      <Page
         header={
            <PageHeader
               eyebrow="Growth account"
               title="Account"
               intro={userExists ? "Welcome back. Pick up where you left off." : "Choose a username and a password for this installation."}
            />
         }
      >
         <div className="stack stack-loose">
            <form className="stack" onSubmit={(event) => submitCredentials(event, userExists)}>
               <UsernameField value={username} disabled={isWorking} onChange={setUsername} />

               <PasswordField
                  id="account-password"
                  label="Password"
                  inputRef={passwordInputRef}
                  autoComplete={userExists ? "current-password" : "new-password"}
                  value={password}
                  disabled={isWorking}
                  onChange={setPassword}
               />

               <button type="submit" className="button-primary button-block" disabled={isWorking}>
                  {submitLabel}
               </button>
            </form>

            {userExists ? (
               <div className="cluster">
                  <button type="button" className="text-button" disabled={isWorking} onClick={openRecovery}>
                     Use recovery code
                  </button>
               </div>
            ) : null}

            <FeedbackLine feedback={state.feedback} />
         </div>
      </Page>
   );
}
