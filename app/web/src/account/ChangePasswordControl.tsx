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
      <section className="card settings" data-testid="password-settings">
         <h2 className="section-heading">Password</h2>

         <form className="field" onSubmit={submit}>
            <label htmlFor="current-password">Current password</label>

            <input
               id="current-password"
               type="password"
               autoComplete="current-password"
               value={currentPassword}
               disabled={isWorking}
               onChange={(event) => setCurrentPassword(event.target.value)}
            />

            <label htmlFor="new-password">New password</label>

            <input
               id="new-password"
               type="password"
               autoComplete="new-password"
               value={newPassword}
               disabled={isWorking}
               onChange={(event) => setNewPassword(event.target.value)}
            />

            <button type="submit" className="text-button" disabled={isWorking}>
               Change password
            </button>
         </form>

         <p role="status">{state.changed ? "Password changed. Other devices are signed out." : ""}</p>

         <FeedbackLine feedback={state.feedback} />
      </section>
   );
}
