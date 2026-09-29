import { useEffect, useId, useState, type FormEvent } from "react";

import { readMe, renameDisplayName, rotateRecoveryCode, type MePayload } from "../api/client";
import { ActionFailed } from "../status/LoadState";
import { Dialog } from "../ui/Dialog";
import { Icon } from "../ui/Icon";
import { Page, PageHeader, Section } from "../ui/Page";
import { FeedbackLine, NO_FEEDBACK, feedbackFrom, type Feedback } from "./AccountScreen";
import { ChangePasswordControl } from "./ChangePasswordControl";
import { usePasswordReauth } from "./ReauthPrompt";

/* The account, opened from the avatar menu: the display name, the password, the recovery code and
   signing out. A new recovery code needs the password again and is shown once, the way sign-up
   shows the first one. */

export const DISPLAY_NAME_LIMIT = 60;

export interface AccountPageProps {
   onRenamed: (me: MePayload) => void;
   onSignOut: () => void;
}

function ProfileSection(props: { me: MePayload | null; onRenamed: (me: MePayload) => void }) {
   const [draft, setDraft] = useState(props.me?.display_name ?? "");
   const [working, setWorking] = useState(false);
   const [feedback, setFeedback] = useState<Feedback>(NO_FEEDBACK);
   const [saved, setSaved] = useState(false);
   const fieldId = useId();

   useEffect(() => {
      setDraft(props.me?.display_name ?? "");
   }, [props.me]);

   const trimmed = draft.trim();
   const isChanged = trimmed !== (props.me?.display_name ?? "");
   const canSave = props.me !== null && trimmed !== "" && isChanged && !working;

   async function save(event: FormEvent) {
      event.preventDefault();

      if (!canSave) {
         return;
      }

      setWorking(true);
      setFeedback(NO_FEEDBACK);
      setSaved(false);

      try {
         const me = await renameDisplayName(trimmed);

         props.onRenamed(me);
         setSaved(true);
      } catch (failure) {
         setFeedback(feedbackFrom(failure));
      } finally {
         setWorking(false);
      }
   }

   return (
      <Section title="Profile">
         <form className="stack" onSubmit={save}>
            <div className="form-field">
               <label className="field-label" htmlFor={fieldId}>
                  Display name
               </label>

               <input
                  id={fieldId}
                  className="input"
                  type="text"
                  maxLength={DISPLAY_NAME_LIMIT}
                  value={draft}
                  disabled={props.me === null || working}
                  onChange={(event) => {
                     setDraft(event.target.value);
                     setSaved(false);
                  }}
               />
            </div>

            <div className="cluster">
               <button type="submit" className="button-secondary" disabled={!canSave}>
                  Save name
               </button>

               {saved ? <span className="helper">Saved.</span> : null}
            </div>

            <FeedbackLine feedback={feedback} />
         </form>
      </Section>
   );
}

function RecoverySection() {
   const reauth = usePasswordReauth();
   const [code, setCode] = useState<string | null>(null);
   const [failed, setFailed] = useState(false);
   const [working, setWorking] = useState(false);

   async function rotate() {
      setFailed(false);
      setWorking(true);

      try {
         const token = await reauth.ask();
         const rotated = await rotateRecoveryCode(token);

         setCode(rotated.recovery_code);
      } catch (failure) {
         const wasCancelled = failure instanceof Error && failure.name === "ReauthCancelled";

         setFailed(!wasCancelled);
      } finally {
         setWorking(false);
      }
   }

   return (
      <Section title="Recovery code">
         <div className="list list-flush">
            <div className="list-row">
               <div className="list-row-body">
                  <span className="list-row-title">A single-use code for getting back in</span>
                  <span className="list-row-meta">
                     If you forget your password, the code sets a new one. Making a new code retires the old one.
                  </span>
               </div>

               <div className="list-row-trail">
                  <button type="button" className="button-secondary button-small" disabled={working} onClick={rotate}>
                     <Icon name="refresh" />
                     Make a new code
                  </button>
               </div>
            </div>
         </div>

         {failed ? <ActionFailed /> : null}

         {reauth.view}

         <Dialog
            open={code !== null}
            title="Save your new recovery code"
            onClose={() => setCode(null)}
            actions={
               <button type="button" className="button-primary" onClick={() => setCode(null)}>
                  I have saved it
               </button>
            }
         >
            <p>This is the only time it is shown. Keep it somewhere safe and apart from this device.</p>

            <p className="code-block" data-testid="new-recovery-code">
               {code}
            </p>
         </Dialog>
      </Section>
   );
}

export function AccountPage(props: AccountPageProps) {
   const [me, setMe] = useState<MePayload | null>(null);
   const [failed, setFailed] = useState(false);

   useEffect(() => {
      let isCurrent = true;

      readMe().then(
         (payload) => {
            if (isCurrent) {
               setMe(payload);
            }
         },
         () => {
            if (isCurrent) {
               setFailed(true);
            }
         }
      );

      return () => {
         isCurrent = false;
      };
   }, []);

   function renamed(next: MePayload) {
      setMe(next);
      props.onRenamed(next);
   }

   const name = me?.display_name ?? "";
   const username = me?.username ?? null;
   const intro = username === null ? "AP Calculus BC" : `${name === "" ? "" : `${name}, `}@${username}, AP Calculus BC`;

   return (
      <Page header={<PageHeader eyebrow="Your workspace" title="Account" intro={intro} />}>
         {failed ? <ActionFailed /> : null}

         <ProfileSection me={me} onRenamed={renamed} />

         <ChangePasswordControl />

         <RecoverySection />

         <Section title="Sign out">
            <p className="muted">You stay signed in on this device until you sign out, even after the app restarts.</p>

            <div className="cluster">
               <button type="button" className="button-secondary" onClick={props.onSignOut}>
                  <Icon name="signOut" />
                  Sign out
               </button>
            </div>
         </Section>
      </Page>
   );
}
