import { useEffect, useState } from "react";

import { AccountScreen } from "./account/AccountScreen";
import { AddPasskeyControl } from "./account/AddPasskeyControl";
import { ApiError, readMe } from "./api/client";
import { HomeRoute } from "./home/HomeRoute";
import { SessionScreen } from "./session/SessionScreen";
import type { SettingsScreenProps } from "./settings/SettingsScreen";
import { SettingsRoute } from "./settings/SettingsRoute";

export type Destination = "home" | "session" | "settings";

export interface DestinationEntry {
   id: Destination;
   label: string;
}

export interface UnsuppliedInput {
   name: string;
   wants: string;
}

/* 08-design-brief.md, Information architecture: settings is reached from the top bar, and a
   session is reached from home's one primary action, never from a bar that would open one. */
export const DESTINATIONS: ReadonlyArray<DestinationEntry> = [
   { id: "home", label: "Home" },
   { id: "settings", label: "Settings" }
];

const TOKEN_PROBE = "--growth-surface-page";

/* 08 gives the claudebox acknowledgement verbatim and no phrase for purge, and no client route
   serves one, so the purge controls stay withheld and the gap is named on the screen. */
const settingsInputs = [
   { name: "purgeConfirmationPhrase", wants: "the phrase a student types to confirm a purge" }
] as const satisfies ReadonlyArray<{
   name: Extract<keyof SettingsScreenProps, string>;
   wants: string;
}>;

export const UNSUPPLIED_INPUTS: Record<Destination, ReadonlyArray<UnsuppliedInput>> = {
   home: [],
   session: [],
   settings: settingsInputs
};

const noticeStyle = {
   background: "var(--growth-surface-raised)",
   color: "var(--growth-text-primary)",
   border: "1px solid var(--growth-border-hairline)"
};

type SessionTarget = { resumeSessionId: string | null };

type Access = "unknown" | "signedIn" | "signedOut";

function isSignedOut(failure: unknown) {
   const isServerRefusal = failure instanceof ApiError;

   return isServerRefusal && failure.status === 401;
}

function tokenStylesheetIsLoaded(): boolean {
   const value = getComputedStyle(document.documentElement).getPropertyValue(TOKEN_PROBE);

   return value.trim() !== "";
}

function saveFile(name: string, contents: Blob) {
   const address = URL.createObjectURL(contents);
   const link = document.createElement("a");

   link.href = address;
   link.download = name;
   link.click();

   setTimeout(() => URL.revokeObjectURL(address));
}

function TokenNotice() {
   return (
      <p role="status" className="notice" style={noticeStyle}>
         The generated design tokens stylesheet is absent, so every colour, type and spacing custom
         property on this page resolves to nothing and falls back to the browser default. The
         operator fills the token file and the build writes the stylesheet from it.
      </p>
   );
}

function UnsuppliedPanel(props: { destination: Destination }) {
   const inputs = UNSUPPLIED_INPUTS[props.destination];
   const hasGap = inputs.length > 0;

   if (!hasGap) {
      return null;
   }

   return (
      <section className="notice" style={noticeStyle}>
         <p className="muted">
            No route on this client supplies the input below, so the part of this screen that needs
            it is held back rather than rendered with a stand-in.
         </p>

         <ul>
            {inputs.map((input) => (
               <li key={input.name} data-testid="unsupplied-input" className="muted">
                  <code>{input.name}</code>, {input.wants}
               </li>
            ))}
         </ul>
      </section>
   );
}

export function App() {
   const [destination, setDestination] = useState<Destination>("home");
   const [sessionTarget, setSessionTarget] = useState<SessionTarget>({ resumeSessionId: null });

   const [access, setAccess] = useState<Access>("unknown");

   const tokensAreLoaded = tokenStylesheetIsLoaded();

   useEffect(() => {
      let isCurrent = true;

      readMe().then(
         () => {
            if (isCurrent) {
               setAccess("signedIn");
            }
         },
         (failure) => {
            const shouldSignIn = isCurrent && isSignedOut(failure);

            if (shouldSignIn) {
               setAccess("signedOut");
            }
         }
      );

      return () => {
         isCurrent = false;
      };
   }, []);

   function enterAfterSignIn() {
      readMe().then(
         () => {
            setDestination("home");
            setAccess("signedIn");
         },
         () => undefined
      );
   }

   function startSession() {
      setSessionTarget({ resumeSessionId: null });
      setDestination("session");
   }

   function resumeSession(sessionId: string) {
      setSessionTarget({ resumeSessionId: sessionId });
      setDestination("session");
   }

   if (access === "signedOut") {
      return (
         <main className="app-page">
            {tokensAreLoaded ? null : <TokenNotice />}

            <AccountScreen onSignedIn={enterAfterSignIn} />
         </main>
      );
   }

   return (
      <main className="app-page">
         <nav className="app-bar">
            {DESTINATIONS.map((entry) => (
               <button key={entry.id} type="button" className="text-button" onClick={() => setDestination(entry.id)}>
                  {entry.label}
               </button>
            ))}
         </nav>

         {tokensAreLoaded ? null : <TokenNotice />}

         {destination === "home" ? (
            <HomeRoute today={() => new Date()} onStartSession={startSession} onResumeSession={resumeSession} />
         ) : null}

         {destination === "session" ? <SessionScreen resumeSessionId={sessionTarget.resumeSessionId} /> : null}

         {destination === "settings" ? (
            <>
               <SettingsRoute purgeConfirmationPhrase={null} saveFile={saveFile} />
               <AddPasskeyControl />
            </>
         ) : null}

         <UnsuppliedPanel destination={destination} />
      </main>
   );
}