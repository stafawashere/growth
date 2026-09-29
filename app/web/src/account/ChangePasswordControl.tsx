import { useState, type FormEvent } from "react";

import { changePassword, reauthenticate } from "../api/client";
import { FeedbackLine, NO_FEEDBACK, feedbackFrom, type Feedback } from "./AccountScreen";

type ChangeState = { working: boolean; feedback: Feedback; changed: boolean };

/* The server asks for a fresh re-authentication before it takes a new password, so the current
   password is sent twice: once to obtain the single-use token and once with the change itself.
   Other devices are signed out by the change, and this one stays signed in. */
export function ChangePasswordControl() {
   const [state, setState] = useState<ChangeState>({ working: false, feedback: NO_FEEDBACK, changed: false });
   const [currentPassword, setCurrentPassword] = useState("");
   const [newPassword, setNewPassword] = useState("");

   async function submit(event: FormEvent) {
      event.preventDefault();
      setState({ working: true, feedback: NO_FEEDBACK, changed: false });

      try {
         const reauth = await reauthenticate({ password: currentPassword });

         await changePassword({
            current_password: currentPassword,
            new_password: newPassword,
            reauth_token: reauth.reauth_token
         });

         setCurrentPassword("");
         setNewPassword("");
         setState({ working: false, feedback: NO_FEEDBACK, changed: true });
      } catch (failure) {
         setState({ working: false, feedback: feedbackFrom(failure), changed: false });
      }
   }

   const isWorking = state.working;

   return (
      <section className="section" data-testid="password-settings">
         <h2 className="section-header">Password</h2>

         <p className="helper">Changing it signs out every other device. This one stays signed in.</p>

         <form className="stack" onSubmit={submit}>
            <div className="form-field">
               <label className="field-label" htmlFor="current-password">
                  Current password
               </label>

               <input
                  id="current-password"
                  className="input"
                  type="password"
                  autoComplete="current-password"
                  value={currentPassword}
                  disabled={isWorking}
                  onChange={(event) => setCurrentPassword(event.target.value)}
               />
            </div>

            <div className="form-field">
               <label className="field-label" htmlFor="new-password">
                  New password
               </label>

               <input
                  id="new-password"
                  className="input"
                  type="password"
                  autoComplete="new-password"
                  value={newPassword}
                  disabled={isWorking}
                  onChange={(event) => setNewPassword(event.target.value)}
               />
            </div>

            <div className="cluster">
               <button type="submit" className="button-secondary" disabled={isWorking}>
                  Change password
               </button>
            </div>
         </form>

         <p role="status" className="helper">
            {state.changed ? "Password changed. Other devices are signed out." : ""}
         </p>

         <FeedbackLine feedback={state.feedback} />
      </section>
   );
}
