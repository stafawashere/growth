import { useEffect, useRef, useState, type FormEvent } from "react";

import { reauthenticate } from "../api/client";
import { Dialog } from "../ui/Dialog";
import { FeedbackLine, NO_FEEDBACK, feedbackFrom, type Feedback } from "./AccountScreen";

export class ReauthCancelled extends Error {
   constructor() {
      super("the password prompt was closed without a password");

      this.name = "ReauthCancelled";
   }
}

export interface ReauthPromptViewProps {
   working: boolean;
   feedback: Feedback;
   onSubmit: (password: string) => void;
   onCancel: () => void;
}

export function ReauthPromptView({ working, feedback, onSubmit, onCancel }: ReauthPromptViewProps) {
   const [password, setPassword] = useState("");
   const passwordInputRef = useRef<HTMLInputElement | null>(null);

   useEffect(() => {
      if (!working) {
         passwordInputRef.current?.focus();
      }
   }, [working, feedback]);

   function submit(event: FormEvent) {
      event.preventDefault();

      const typed = password;

      setPassword("");
      onSubmit(typed);
   }

   return (
      <Dialog open title="Confirm your password" onClose={onCancel}>
         <section aria-label="Confirm your password" data-testid="reauth-prompt" className="stack">
            <p className="muted">This action needs your password again.</p>

            <form className="stack" onSubmit={submit}>
               <div className="form-field">
                  <label className="field-label" htmlFor="reauth-password">
                     Password
                  </label>

                  <input
                     id="reauth-password"
                     className="input"
                     type="password"
                     autoComplete="current-password"
                     ref={passwordInputRef}
                     value={password}
                     disabled={working}
                     onChange={(event) => setPassword(event.target.value)}
                  />
               </div>

               <FeedbackLine feedback={feedback} />

               <div className="dialog-actions">
                  <button type="button" className="button-secondary" disabled={working} onClick={onCancel}>
                     Cancel
                  </button>

                  <button type="submit" className="button-primary" disabled={working}>
                     Confirm
                  </button>
               </div>
            </form>
         </section>
      </Dialog>
   );
}

type PromptState = { kind: "closed" } | { kind: "open"; working: boolean; feedback: Feedback };

interface Pending {
   resolve: (token: string) => void;
   reject: (reason: Error) => void;
}

/* One password prompt serves every action that needs a fresh re-authentication. ask() opens it and
   settles with the single-use token once the server accepts the password, or rejects when the
   student closes it. A refused password keeps the prompt open with the server's refusal, so a
   typo costs a retry rather than the whole action. */
export function usePasswordReauth() {
   const [prompt, setPrompt] = useState<PromptState>({ kind: "closed" });
   const pending = useRef<Pending | null>(null);

   useEffect(() => {
      return () => {
         pending.current?.reject(new ReauthCancelled());
         pending.current = null;
      };
   }, []);

   function ask() {
      pending.current?.reject(new ReauthCancelled());

      return new Promise<string>((resolve, reject) => {
         pending.current = { resolve, reject };
         setPrompt({ kind: "open", working: false, feedback: NO_FEEDBACK });
      });
   }

   async function submit(password: string) {
      setPrompt({ kind: "open", working: true, feedback: NO_FEEDBACK });

      try {
         const accepted = await reauthenticate({ password });
         const waiting = pending.current;

         pending.current = null;
         setPrompt({ kind: "closed" });
         waiting?.resolve(accepted.reauth_token);
      } catch (failure) {
         setPrompt({ kind: "open", working: false, feedback: feedbackFrom(failure) });
      }
   }

   function cancel() {
      const waiting = pending.current;

      pending.current = null;
      setPrompt({ kind: "closed" });
      waiting?.reject(new ReauthCancelled());
   }

   const view =
      prompt.kind === "open" ? (
         <ReauthPromptView working={prompt.working} feedback={prompt.feedback} onSubmit={submit} onCancel={cancel} />
      ) : null;

   return { ask, view };
}
