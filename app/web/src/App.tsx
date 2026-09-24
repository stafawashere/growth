import { useEffect, useState } from "react";

import { AccountScreen } from "./account/AccountScreen";
import { AddPasskeyControl } from "./account/AddPasskeyControl";
import { ApiError, readMe } from "./api/client";
import { MetricsRoute } from "./evaluation/MetricsRoute";
import { FrqRoute } from "./frq/FrqRoute";
import { HomeRoute } from "./home/HomeRoute";
import { OnboardingRoute } from "./onboarding/OnboardingRoute";
import type { OnboardingReason } from "./onboarding/OnboardingScreen";
import { ProgressRoute } from "./progress/ProgressRoute";
import { ReviewRoute } from "./review/ReviewRoute";
import { SessionScreen } from "./session/SessionScreen";
import { OperatorSettings } from "./settings/ExperimentsSection";
import type { SettingsScreenProps } from "./settings/SettingsScreen";
import { SettingsRoute } from "./settings/SettingsRoute";

export type Destination = "home" | "session" | "settings" | "progress" | "review" | "onboarding" | "frq";

export interface DestinationEntry {
   id: Destination;
   label: string;
}

export interface UnsuppliedInput {
   name: string;
   wants: string;
}

/* 08-design-brief.md, Information architecture: settings is reached from the top bar, a session
   from home's one primary action, progress, review and the free-response unit check from home,
   and onboarding only when home sends a first login, an unfinished diagnostic or a long gap there,
   so none of the last five is here. */
export const DESTINATIONS: ReadonlyArray<DestinationEntry> = [
   { id: "home", label: "Home" },
   { id: "settings", label: "Settings" }
];

const TOKEN_PROBE = "--growth-surface-page";

/* Ruled 2026-09-23: the purge confirmation phrase is the literal text "delete my data", matching
   app/api/routes/purge.py's PURGE_CONFIRMATION. 08 gives no phrase of its own, so this is the
   operator's decision rather than a plan reading, and it is why this is a constant here rather
   than a value the client reads off a route. */
export const PURGE_CONFIRMATION_PHRASE = "delete my data";

const settingsInputs = [] as const satisfies ReadonlyArray<{
   name: Extract<keyof SettingsScreenProps, string>;
   wants: string;
}>;

export const UNSUPPLIED_INPUTS: Record<Destination, ReadonlyArray<UnsuppliedInput>> = {
   home: [],
   session: [],
   settings: settingsInputs,
   progress: [],
   review: [],
   onboarding: [],
   frq: []
};

const noticeStyle = {
   background: "var(--growth-surface-raised)",
   color: "var(--growth-text-primary)",
   border: "1px solid var(--growth-border-hairline)"
};

type SessionTarget = { resumeSessionId: string | null };

type OnboardingTarget = { reason: OnboardingReason; resumeSessionId: string | null };

type Access = "unknown" | "signedIn" | "signedOut";

/* The operator's evidence of learning opens from settings and returns there. It is a page of
   settings rather than a destination, so it is never on the bar and home cannot reach it. */
type SettingsPage = "settings" | "evidence";

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
   const [onboardingTarget, setOnboardingTarget] = useState<OnboardingTarget>({
      reason: "first_login",
      resumeSessionId: null
   });

   const [access, setAccess] = useState<Access>("unknown");
   const [settingsPage, setSettingsPage] = useState<SettingsPage>("settings");

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

   function visit(destination: Destination) {
      setSettingsPage("settings");
      setDestination(destination);
   }

   function startSession() {
      setSessionTarget({ resumeSessionId: null });
      setDestination("session");
   }

   function resumeSession(sessionId: string) {
      setSessionTarget({ resumeSessionId: sessionId });
      setDestination("session");
   }

   function startOnboarding(reason: OnboardingReason, resumeSessionId: string | null) {
      setOnboardingTarget({ reason, resumeSessionId });
      setDestination("onboarding");
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
               <button key={entry.id} type="button" className="text-button" onClick={() => visit(entry.id)}>
                  {entry.label}
               </button>
            ))}
         </nav>

         {tokensAreLoaded ? null : <TokenNotice />}

         {destination === "home" ? (
            <HomeRoute
               today={() => new Date()}
               onStartSession={startSession}
               onResumeSession={resumeSession}
               onOpenProgress={() => setDestination("progress")}
               onOpenReview={() => setDestination("review")}
               onOpenFreeResponse={() => setDestination("frq")}
               onStartOnboarding={startOnboarding}
            />
         ) : null}

         {destination === "onboarding" ? (
            <OnboardingRoute
               reason={onboardingTarget.reason}
               resumeSessionId={onboardingTarget.resumeSessionId}
               onFinished={() => setDestination("home")}
            />
         ) : null}

         {destination === "session" ? <SessionScreen resumeSessionId={sessionTarget.resumeSessionId} /> : null}

         {destination === "progress" ? <ProgressRoute /> : null}

         {destination === "review" ? <ReviewRoute /> : null}

         {destination === "frq" ? <FrqRoute /> : null}

         {destination === "settings" && settingsPage === "settings" ? (
            <>
               <SettingsRoute purgeConfirmationPhrase={PURGE_CONFIRMATION_PHRASE} saveFile={saveFile} />
               <OperatorSettings onOpenEvidence={() => setSettingsPage("evidence")} />
               <AddPasskeyControl />
            </>
         ) : null}

         {destination === "settings" && settingsPage === "evidence" ? (
            <MetricsRoute onLeave={() => setSettingsPage("settings")} />
         ) : null}

         <UnsuppliedPanel destination={destination} />
      </main>
   );
}