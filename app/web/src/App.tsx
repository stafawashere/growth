import { useState } from "react";

import type { HomeScreenProps } from "./home/HomeScreen";
import type { SessionScreenProps } from "./session/SessionScreen";
import type { SettingsScreenProps } from "./settings/SettingsScreen";

export type Destination = "home" | "session" | "settings";

export interface DestinationEntry {
   id: Destination;
   label: string;
}

export interface UnsuppliedInput {
   name: string;
   wants: string;
}

export const DESTINATIONS: ReadonlyArray<DestinationEntry> = [
   { id: "home", label: "Home" },
   { id: "session", label: "Session" },
   { id: "settings", label: "Settings" }
];

const TOKEN_PROBE = "--growth-surface-page";

const homeInputs = [
   { name: "queueMinutes", wants: "the minute forecast for today's queue" },
   { name: "queueLines", wants: "the count on each queue line" },
   { name: "examDate", wants: "the exam date" },
   { name: "daysToExam", wants: "the days left before the exam" }
] as const satisfies ReadonlyArray<{ name: Extract<keyof HomeScreenProps, string>; wants: string }>;

const sessionInputs = [
   { name: "workedStepsFor", wants: "the worked solution steps an example or a completion item shows" },
   { name: "selfExplanationPromptFor", wants: "the prompt the student answers before submitting" }
] as const satisfies ReadonlyArray<{
   name: Extract<keyof SessionScreenProps, string>;
   wants: string;
}>;

const settingsInputs = [
   { name: "providers", wants: "the provider and model assigned to each role" },
   { name: "dailyCapDollars", wants: "the daily spend cap" },
   { name: "spentThisMonthDollars", wants: "the spend so far this month" },
   { name: "perRoleCaps", wants: "the per-role spend caps and what each has spent today" },
   { name: "purgeConfirmationPhrase", wants: "the phrase a student types to confirm a purge" },
   { name: "onReauthenticate", wants: "the passkey re-authentication ceremony" },
   { name: "examDate", wants: "the exam date" }
] as const satisfies ReadonlyArray<{
   name: Extract<keyof SettingsScreenProps, string>;
   wants: string;
}>;

export const UNSUPPLIED_INPUTS: Record<Destination, ReadonlyArray<UnsuppliedInput>> = {
   home: homeInputs,
   session: sessionInputs,
   settings: settingsInputs
};

const pageStyle = {
   background: "var(--growth-surface-page)",
   color: "var(--growth-text-primary)"
};

const noticeStyle = {
   background: "var(--growth-surface-raised)",
   color: "var(--growth-text-primary)",
   border: "1px solid var(--growth-border-hairline)"
};

const mutedTextStyle = { color: "var(--growth-text-muted)" };

function tokenStylesheetIsLoaded(): boolean {
   const value = getComputedStyle(document.documentElement).getPropertyValue(TOKEN_PROBE);

   return value.trim() !== "";
}

function TokenNotice() {
   return (
      <p role="status" style={noticeStyle}>
         The generated design tokens stylesheet is absent, so every colour, type and spacing custom
         property on this page resolves to nothing and falls back to the browser default. The
         operator fills the token file and the build writes the stylesheet from it.
      </p>
   );
}

function UnsuppliedPanel(props: { destination: Destination }) {
   const inputs = UNSUPPLIED_INPUTS[props.destination];

   return (
      <section style={noticeStyle}>
         <h2>This screen is not built yet</h2>

         <p style={mutedTextStyle}>
            Every input below is required by the screen and no route on this client supplies it, so
            the screen is held back rather than rendered with a stand-in figure.
         </p>

         <ul>
            {inputs.map((input) => (
               <li key={input.name} data-testid="unsupplied-input" style={mutedTextStyle}>
                  <code>{input.name}</code>, {input.wants}
               </li>
            ))}
         </ul>
      </section>
   );
}

export function App() {
   const [destination, setDestination] = useState<Destination>("home");

   const tokensAreLoaded = tokenStylesheetIsLoaded();

   return (
      <main style={pageStyle}>
         <nav>
            {DESTINATIONS.map((entry) => (
               <button key={entry.id} type="button" onClick={() => setDestination(entry.id)}>
                  {entry.label}
               </button>
            ))}
         </nav>

         {tokensAreLoaded ? null : <TokenNotice />}

         <UnsuppliedPanel destination={destination} />
      </main>
   );
}
