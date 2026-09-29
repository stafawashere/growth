import { Suspense, lazy, useEffect, useState } from "react";

import { AccountScreen } from "./account/AccountScreen";
import { ChangePasswordControl } from "./account/ChangePasswordControl";
import { ApiError, readAuthStatus, readMe, signOut } from "./api/client";
import { HomeRoute } from "./home/HomeRoute";
import { AiNotices, AiNoticesSetting, readAiNoticesEnabled } from "./notices/AiNotices";
import type { OnboardingReason } from "./onboarding/OnboardingScreen";
import { OperatorSettings } from "./settings/ExperimentsSection";
import type { SettingsScreenProps } from "./settings/SettingsScreen";
import { AccessibilitySection } from "./settings/AccessibilitySection";
import { SettingsRoute } from "./settings/SettingsRoute";
import { ActionFailed } from "./status/LoadState";

const AssessmentRoute = lazy(() => import("./assessment/AssessmentRoute").then((module) => ({ default: module.AssessmentRoute })));
const MetricsRoute = lazy(() => import("./evaluation/MetricsRoute").then((module) => ({ default: module.MetricsRoute })));
const LessonRoute = lazy(() => import("./lessons/LessonRoute").then((module) => ({ default: module.LessonRoute })));
const LessonsRoute = lazy(() => import("./lessons/LessonsRoute").then((module) => ({ default: module.LessonsRoute })));
const FrqRoute = lazy(() => import("./frq/FrqRoute").then((module) => ({ default: module.FrqRoute })));
const OnboardingRoute = lazy(() => import("./onboarding/OnboardingRoute").then((module) => ({ default: module.OnboardingRoute })));
const ProgressRoute = lazy(() => import("./progress/ProgressRoute").then((module) => ({ default: module.ProgressRoute })));
const ReviewRoute = lazy(() => import("./review/ReviewRoute").then((module) => ({ default: module.ReviewRoute })));
const SessionScreen = lazy(() => import("./session/SessionScreen").then((module) => ({ default: module.SessionScreen })));

export type Destination = "home" | "lessons" | "session" | "settings" | "progress" | "review" | "onboarding" | "frq" | "mock" | "lesson";

export interface DestinationEntry {
   id: Destination;
   label: string;
}

export interface UnsuppliedInput {
   name: string;
   wants: string;
}

/* 08-design-brief.md, Information architecture: settings is reached from the top bar, a session
   from home's one primary action, progress, review, the free-response unit check and the mock
   exam from home, and onboarding only when home sends a first login, an unfinished diagnostic or
   a long gap there, so none of the last six is here. Lessons has its own tab (the operator's ruling
   of 2026-09-29, amending 15 UI); the lesson reader opens from it or from progress's Lessons section
   and returns to whichever opened it, so the reader itself is not here. */
export const DESTINATIONS: ReadonlyArray<DestinationEntry> = [
   { id: "home", label: "Home" },
   { id: "lessons", label: "Lessons" },
   { id: "settings", label: "Settings" }
];

const TOKEN_PROBE = "--growth-surface-page";

/* Ruled 2026-09-23: the purge confirmation phrase is the literal text "delete my data", matching
   app/api/routes/purge.py's PURGE_CONFIRMATION. 08 gives no phrase of its own, so this is the
   operator's decision rather than a plan reading, and it is why this is a constant here rather
   than a value the client reads off a route. */
export const OPERATOR_EXPERIMENTS_SUMMARY = "For the operator: experiments and evidence of learning";

export const PURGE_CONFIRMATION_PHRASE = "delete my data";

const settingsInputs = [] as const satisfies ReadonlyArray<{
   name: Extract<keyof SettingsScreenProps, string>;
   wants: string;
}>;

export const UNSUPPLIED_INPUTS: Record<Destination, ReadonlyArray<UnsuppliedInput>> = {
   home: [],
   lessons: [],
   session: [],
   settings: settingsInputs,
   progress: [],
   review: [],
   onboarding: [],
   frq: [],
   mock: [],
   lesson: []
};

type SessionTarget = { resumeSessionId: string | null };

type LessonTarget = { lessonId: string; conceptName: string; returnTo: "lessons" | "progress" };

type OnboardingTarget = { reason: OnboardingReason; resumeSessionId: string | null };

type Access = "unknown" | "signedIn" | "signedOut";

type SignOutState = "idle" | "working" | "failed";

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
      <p role="status" className="notice notice-framed">
         The generated design tokens stylesheet is absent, so every colour, type and spacing custom
         property on this page resolves to nothing and falls back to the browser default. The
         operator fills the token file and the build writes the stylesheet from it.
      </p>
   );
}

function AppFooter() {
   return (
      <footer className="app-footer">
         <p>AP Calculus BC</p>
      </footer>
   );
}

function UnsuppliedPanel(props: { destination: Destination }) {
   const inputs = UNSUPPLIED_INPUTS[props.destination];
   const hasGap = inputs.length > 0;

   if (!hasGap) {
      return null;
   }

   return (
      <section className="notice notice-framed">
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

   const [lessonTarget, setLessonTarget] = useState<LessonTarget | null>(null);

   const [access, setAccess] = useState<Access>("unknown");
   const [settingsPage, setSettingsPage] = useState<SettingsPage>("settings");
   const [signOutState, setSignOutState] = useState<SignOutState>("idle");
   const [aiNoticesOn, setAiNoticesOn] = useState<boolean>(readAiNoticesEnabled);

   const tokensAreLoaded = tokenStylesheetIsLoaded();

   useEffect(() => {
      let isCurrent = true;

      /* A status that cannot be read says nothing, so readMe still decides. An account migrated
         from passkeys goes to the reset form whatever readMe would have said. */
      async function decideAccess() {
         const needsPassword = await Promise.resolve()
            .then(() => readAuthStatus())
            .then((status) => status?.needs_password === true)
            .catch(() => false);

         if (needsPassword) {
            if (isCurrent) {
               setAccess("signedOut");
            }

            return;
         }

         try {
            await readMe();

            if (isCurrent) {
               setAccess("signedIn");
            }
         } catch (failure) {
            const shouldSignIn = isCurrent && isSignedOut(failure);

            if (shouldSignIn) {
               setAccess("signedOut");
            }
         }
      }

      void decideAccess();

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

   /* A 401 means the session had already ended, which is the state signing out asks for. Any other
      failure leaves the student signed in and says so. */
   async function leave() {
      setSignOutState("working");

      try {
         await signOut();
      } catch (failure) {
         const isAlreadySignedOut = isSignedOut(failure);

         if (!isAlreadySignedOut) {
            setSignOutState("failed");

            return;
         }
      }

      setSignOutState("idle");
      setSettingsPage("settings");
      setDestination("home");
      setAccess("signedOut");
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

   function openLesson(lessonId: string, conceptName: string) {
      setLessonTarget({ lessonId, conceptName, returnTo: destination === "lessons" ? "lessons" : "progress" });
      setDestination("lesson");
   }

   function startOnboarding(reason: OnboardingReason, resumeSessionId: string | null) {
      setOnboardingTarget({ reason, resumeSessionId });
      setDestination("onboarding");
   }

   if (access === "signedOut") {
      return (
         <>
            <header className="app-header">
               <div className="app-bar">
                  <span className="app-brand">Calculus BC</span>
               </div>
            </header>

            <main className="app-page">
               {tokensAreLoaded ? null : <TokenNotice />}

               <AccountScreen onSignedIn={enterAfterSignIn} />
            </main>

            <AppFooter />
         </>
      );
   }

   const isSigningOut = signOutState === "working";
   const showsAiNotices = access === "signedIn" && aiNoticesOn;

   return (
      <>
         <header className="app-header">
            <div className="app-bar">
               <nav className="app-nav" aria-label="Main">
                  <span className="app-brand">Calculus BC</span>

                  {DESTINATIONS.map((entry) => (
                     <span key={entry.id} className={entry.id === "settings" ? "app-bar-end" : undefined}>
                        <button
                           type="button"
                           className="text-button"
                           aria-current={destination === entry.id ? "page" : undefined}
                           onClick={() => visit(entry.id)}
                        >
                           {entry.label}
                        </button>
                     </span>
                  ))}
               </nav>

               <button type="button" className="text-button" disabled={isSigningOut} onClick={leave}>
                  Sign out
               </button>
            </div>
         </header>

         <main className="app-page">
            {tokensAreLoaded ? null : <TokenNotice />}

            {signOutState === "failed" ? <ActionFailed /> : null}

            <Suspense fallback={null}>

               {destination === "home" ? (
                  <HomeRoute
                     today={() => new Date()}
                     onStartSession={startSession}
                     onResumeSession={resumeSession}
                     onOpenProgress={() => setDestination("progress")}
                     onOpenReview={() => setDestination("review")}
                     onOpenFreeResponse={() => setDestination("frq")}
                     onOpenMockExam={() => setDestination("mock")}
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

               {destination === "lessons" ? <LessonsRoute onOpenLesson={openLesson} /> : null}

               {destination === "progress" ? <ProgressRoute onOpenLesson={openLesson} /> : null}

               {destination === "lesson" && lessonTarget !== null ? (
                  <LessonRoute
                     lessonId={lessonTarget.lessonId}
                     conceptName={lessonTarget.conceptName}
                     onLeave={() => setDestination(lessonTarget.returnTo)}
                     backLabel={lessonTarget.returnTo === "lessons" ? "Back to lessons" : "Back to progress"}
                  />
               ) : null}

               {destination === "review" ? <ReviewRoute /> : null}

               {destination === "frq" ? <FrqRoute /> : null}

               {destination === "mock" ? <AssessmentRoute /> : null}

               {destination === "settings" && settingsPage === "settings" ? (
                  <>
                     <SettingsRoute purgeConfirmationPhrase={PURGE_CONFIRMATION_PHRASE} saveFile={saveFile} />
                     <AccessibilitySection />
                     <AiNoticesSetting enabled={aiNoticesOn} onChange={setAiNoticesOn} />
                     <ChangePasswordControl />
                     <details className="operator-details" data-testid="operator-experiments-evidence">
                        <summary>{OPERATOR_EXPERIMENTS_SUMMARY}</summary>

                        <OperatorSettings onOpenEvidence={() => setSettingsPage("evidence")} />
                     </details>
                  </>
               ) : null}

               {destination === "settings" && settingsPage === "evidence" ? (
                  <MetricsRoute onLeave={() => setSettingsPage("settings")} />
               ) : null}

            </Suspense>

            <UnsuppliedPanel destination={destination} />
         </main>

         <AppFooter />

         <AiNotices active={showsAiNotices} />
      </>
   );
}