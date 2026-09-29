import { Suspense, lazy, useCallback, useEffect, useRef, useState } from "react";

import { AccountScreen } from "./account/AccountScreen";
import { AgentProvider, useAgent, useAgentScreen } from "./agent/AgentProvider";
import { accountFrom, forgetCachedAccount, readCachedAccount, saveCachedAccount, type CachedAccount } from "./account/cachedAccount";
import { ApiError, SESSION_ENDED_EVENT, readAuthStatus, readMe, signOut, type MePayload } from "./api/client";
import { HomeRoute } from "./home/HomeRoute";
import { AiNotices, readAiNoticesEnabled } from "./notices/AiNotices";
import type { OnboardingReason } from "./onboarding/OnboardingScreen";
import { usePlace, type GoOptions, type Place, type View } from "./routing";
import { AccountMenu } from "./shell/AccountMenu";
import { TABS, TopBar } from "./shell/TopBar";
import { ActionFailed, RETRY_LABEL } from "./status/LoadState";

const AccountPage = lazy(() => import("./account/AccountPage").then((module) => ({ default: module.AccountPage })));
const AssessmentsRoute = lazy(() => import("./assessment/AssessmentRoute").then((module) => ({ default: module.AssessmentsRoute })));
const CheckpointRoute = lazy(() => import("./evaluation/CheckpointRoute").then((module) => ({ default: module.CheckpointRoute })));
const MetricsRoute = lazy(() => import("./evaluation/MetricsRoute").then((module) => ({ default: module.MetricsRoute })));
const ProbeRoute = lazy(() => import("./evaluation/ProbeRoute").then((module) => ({ default: module.ProbeRoute })));
const LessonRoute = lazy(() => import("./lessons/LessonRoute").then((module) => ({ default: module.LessonRoute })));
const LessonsRoute = lazy(() => import("./lessons/LessonsRoute").then((module) => ({ default: module.LessonsRoute })));
const OnboardingRoute = lazy(() => import("./onboarding/OnboardingRoute").then((module) => ({ default: module.OnboardingRoute })));
const ProgressRoute = lazy(() => import("./progress/ProgressRoute").then((module) => ({ default: module.ProgressRoute })));
const ReviewRoute = lazy(() => import("./review/ReviewRoute").then((module) => ({ default: module.ReviewRoute })));
const SessionScreen = lazy(() => import("./session/SessionScreen").then((module) => ({ default: module.SessionScreen })));
const SettingsPage = lazy(() => import("./settings/SettingsPage").then((module) => ({ default: module.SettingsPage })));

export type Destination = View;

export interface DestinationEntry {
   id: (typeof TABS)[number]["id"];
   label: string;
}

/* The redesign's information architecture (mockup-redesign/, the operator's ruling of 2026-09-29,
   amending 08's): Today, Lessons, Review, Progress and Assessments are tabs on the bar; settings and
   the account open from the avatar menu; a session and onboarding open from Today, a lesson from
   Lessons or Progress, and a checkpoint or probe from Progress. */
export const DESTINATIONS: ReadonlyArray<DestinationEntry> = TABS.map((entry) => ({ id: entry.id, label: entry.label }));

export interface UnsuppliedInput {
   name: string;
   wants: string;
}

export const UNSUPPLIED_INPUTS: Record<Destination, ReadonlyArray<UnsuppliedInput>> = {
   home: [],
   session: [],
   onboarding: [],
   lessons: [],
   lesson: [],
   review: [],
   progress: [],
   checkpoint: [],
   probe: [],
   assessments: [],
   settings: [],
   evidence: [],
   account: []
};

/* Ruled 2026-09-23: the purge confirmation phrase is the literal text "delete my data", matching
   app/api/routes/purge.py's PURGE_CONFIRMATION. 08 gives no phrase of its own, so this is the
   operator's decision rather than a plan reading, and it is why this is a constant here rather
   than a value the client reads off a route. */
export const PURGE_CONFIRMATION_PHRASE = "delete my data";

export const OPERATOR_EXPERIMENTS_SUMMARY = "For the operator: experiments and evidence of learning";

export const OFFLINE_TEXT = "The app could not reach its server, so what you see may be out of date. You are still signed in.";

const TOKEN_PROBE = "--growth-surface-page";

/* unknown: nothing cached and /me has not answered. signedIn: /me answered, or this browser holds the
   account from an earlier visit and /me has not refused it. signedOut: /me answered 401, or the
   account must set a password first. */
type Access = "unknown" | "signedIn" | "signedOut";

type SignOutState = "idle" | "working" | "failed";

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
      <p role="status" className="notice">
         The generated design tokens stylesheet is absent, so every colour, type and spacing custom
         property on this page resolves to nothing and falls back to the browser default. The
         operator fills the token file and the build writes the stylesheet from it.
      </p>
   );
}

/* The views that describe their own screen to the tutor with useAgentScreen. Every other view is
   "other", named by the shell (docs/agent/architecture.md, "The screen context"). */
const VIEWS_WITH_OWN_SCREEN: ReadonlyArray<View> = ["home", "session", "lesson", "review", "progress", "assessments", "settings"];

const OTHER_VIEW_NAMES: Partial<Record<View, string>> = {
   onboarding: "Getting started",
   lessons: "Lessons",
   checkpoint: "Progress, a checkpoint",
   probe: "Progress, a concept probe",
   evidence: "Settings, evidence of learning",
   account: "Account"
};

function OtherViewScreen(props: { view: View }) {
   const hasOwnScreen = VIEWS_WITH_OWN_SCREEN.includes(props.view);

   useAgentScreen(hasOwnScreen ? null : { kind: "other", view: props.view }, { viewName: OTHER_VIEW_NAMES[props.view] });

   return null;
}

function ShellNotices(props: { active: boolean }) {
   const agent = useAgent();

   return <AiNotices active={props.active} hideAgentNotices={agent?.isOpen === true} />;
}

function OfflineNotice(props: { onRetry: () => void }) {
   return (
      <div role="status" className="callout callout-row" data-testid="offline-notice">
         <p>{OFFLINE_TEXT}</p>

         <button type="button" className="button-secondary button-small" onClick={props.onRetry}>
            {RETRY_LABEL}
         </button>
      </div>
   );
}

export function App() {
   const [place, go] = usePlace();
   const [account, setAccount] = useState<CachedAccount | null>(readCachedAccount);
   const [access, setAccess] = useState<Access>(() => (readCachedAccount() === null ? "unknown" : "signedIn"));
   const [offline, setOffline] = useState(false);
   const [signOutState, setSignOutState] = useState<SignOutState>("idle");
   const [aiNoticesOn, setAiNoticesOn] = useState<boolean>(readAiNoticesEnabled);
   const [barVisits, setBarVisits] = useState(0);
   const main = useRef<HTMLElement | null>(null);
   const checking = useRef(false);

   const tokensAreLoaded = tokenStylesheetIsLoaded();

   const acceptMe = useCallback((me: MePayload) => {
      const known = accountFrom(me);

      saveCachedAccount(known);
      setAccount(known);
      setOffline(false);
      setAccess("signedIn");
   }, []);

   const endSession = useCallback(() => {
      forgetCachedAccount();
      setAccount(null);
      setOffline(false);
      setAccess("signedOut");
   }, []);

   /* Only a 401 from /me signs the student out. A network failure or a server error leaves them
      signed in, says the app is out of reach, and checks again when asked or when the browser
      comes back online. */
   const checkSession = useCallback(async () => {
      if (checking.current) {
         return;
      }

      checking.current = true;

      try {
         const me = await readMe();

         acceptMe(me);
      } catch (failure) {
         if (isSignedOut(failure)) {
            endSession();
         } else {
            setOffline(readCachedAccount() !== null);
         }
      } finally {
         checking.current = false;
      }
   }, [acceptMe, endSession]);

   useEffect(() => {
      let isCurrent = true;

      /* A status that cannot be read says nothing, so readMe still decides. An account migrated
         from passkeys goes to the reset form whatever readMe would have said. */
      async function decideAccess() {
         const needsPassword = await Promise.resolve()
            .then(() => readAuthStatus())
            .then((status) => status?.needs_password === true)
            .catch(() => false);

         if (!isCurrent) {
            return;
         }

         if (needsPassword) {
            endSession();

            return;
         }

         await checkSession();
      }

      void decideAccess();

      return () => {
         isCurrent = false;
      };
   }, [checkSession, endSession]);

   useEffect(() => {
      function recheck() {
         void checkSession();
      }

      window.addEventListener(SESSION_ENDED_EVENT, recheck);
      window.addEventListener("online", recheck);

      return () => {
         window.removeEventListener(SESSION_ENDED_EVENT, recheck);
         window.removeEventListener("online", recheck);
      };
   }, [checkSession]);

   useEffect(() => {
      main.current?.focus({ preventScroll: true });
   }, [place]);

   function enterAfterSignIn() {
      readMe().then(
         (me) => {
            acceptMe(me);
            go({ view: "home" });
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
      endSession();
      go({ view: "home" });
   }

   /* A tab on the bar always lands on that tab's own first page, even when the student is already
      somewhere inside it, so routes that keep an inner page are drawn afresh. */
   function goFromBar(next: Place) {
      setBarVisits((visits) => visits + 1);
      go(next);
   }

   function startOnboarding(reason: OnboardingReason, resumeSessionId: string | null) {
      go({ view: "onboarding", reason, resumeSessionId });
   }

   /* Home hands a first login or an unfinished diagnostic straight on, so that step replaces home in
      the history rather than leaving a page the back button would bounce off. */
   function redirectToOnboarding(reason: OnboardingReason, resumeSessionId: string | null) {
      go({ view: "onboarding", reason, resumeSessionId }, { replace: true });
   }

   function openLesson(returnTo: "lessons" | "progress") {
      return (lessonId: string, conceptName: string) => go({ view: "lesson", lessonId, conceptName, returnTo });
   }

   if (access === "signedOut") {
      return (
         <>
            <a className="skip-link" href="#main">
               Skip to content
            </a>

            <TopBar view={null} go={go} />

            <main className="app-page" id="main" tabIndex={-1} ref={main}>
               {tokensAreLoaded ? null : <TokenNotice />}

               <AccountScreen onSignedIn={enterAfterSignIn} />
            </main>

         </>
      );
   }

   const showsAiNotices = access === "signedIn" && aiNoticesOn;
   const menuCurrent = place.view === "account" ? "account" : place.view === "settings" || place.view === "evidence" ? "settings" : null;

   return (
      <AgentProvider enabled={access === "signedIn"}>
         <a className="skip-link" href="#main">
            Skip to content
         </a>

         <TopBar
            view={place.view}
            go={goFromBar}
            menu={
               <AccountMenu
                  account={account}
                  current={menuCurrent}
                  signingOut={signOutState === "working"}
                  onOpenAccount={() => go({ view: "account" })}
                  onOpenSettings={() => go({ view: "settings", tab: "study" })}
                  onSignOut={leave}
               />
            }
         />

         <main className="app-page" id="main" tabIndex={-1} ref={main}>
            {tokensAreLoaded ? null : <TokenNotice />}

            {offline ? <OfflineNotice onRetry={() => void checkSession()} /> : null}

            {signOutState === "failed" ? <ActionFailed /> : null}

            <Suspense fallback={null}>
               <PlaceView
                  place={place}
                  go={go}
                  barVisits={barVisits}
                  aiNoticesOn={aiNoticesOn}
                  onAiNoticesChange={setAiNoticesOn}
                  onStartOnboarding={startOnboarding}
                  onRedirectToOnboarding={redirectToOnboarding}
                  openLesson={openLesson}
                  onRenamed={acceptMe}
                  onSignOut={leave}
               />
            </Suspense>
         </main>

         <OtherViewScreen view={place.view} />

         <ShellNotices active={showsAiNotices} />
      </AgentProvider>
   );
}

function PlaceView(props: {
   place: Place;
   barVisits: number;
   go: (place: Place, options?: GoOptions) => void;
   aiNoticesOn: boolean;
   onAiNoticesChange: (enabled: boolean) => void;
   onStartOnboarding: (reason: OnboardingReason, resumeSessionId: string | null) => void;
   onRedirectToOnboarding: (reason: OnboardingReason, resumeSessionId: string | null) => void;
   openLesson: (returnTo: "lessons" | "progress") => (lessonId: string, conceptName: string) => void;
   onRenamed: (me: MePayload) => void;
   onSignOut: () => void;
}) {
   const { place, go } = props;

   switch (place.view) {
      case "home":
         return (
            <HomeRoute
               today={() => new Date()}
               onStartSession={() => go({ view: "session", resumeSessionId: null })}
               onResumeSession={(sessionId) => go({ view: "session", resumeSessionId: sessionId })}
               onStartOnboarding={props.onRedirectToOnboarding}
            />
         );
      case "session":
         return (
            <SessionScreen
               resumeSessionId={place.resumeSessionId}
               onLeave={() => go({ view: "home" })}
               onOpened={(sessionId) => go({ view: "session", resumeSessionId: sessionId }, { replace: true })}
            />
         );
      case "onboarding":
         return <OnboardingRoute reason={place.reason} resumeSessionId={place.resumeSessionId} onFinished={() => go({ view: "home" })} />;
      case "lessons":
         return <LessonsRoute onOpenLesson={props.openLesson("lessons")} />;
      case "lesson":
         return (
            <LessonRoute
               lessonId={place.lessonId}
               conceptName={place.conceptName}
               returnTo={place.returnTo}
               onLeave={() => go(place.returnTo === "lessons" ? { view: "lessons" } : { view: "progress", tab: "lessons" })}
               backLabel={place.returnTo === "lessons" ? "Back to lessons" : "Back to progress"}
            />
         );
      case "review":
         return <ReviewRoute onStartPractice={() => go({ view: "session", resumeSessionId: null })} />;
      case "progress":
         return (
            <ProgressRoute
               tab={place.tab}
               onChangeTab={(tab) => go({ view: "progress", tab })}
               onOpenLesson={props.openLesson("progress")}
               onOpenCheckpoint={(openCheckpointId) => go({ view: "checkpoint", openCheckpointId })}
               onOpenProbe={(openAdministrationId) => go({ view: "probe", openAdministrationId })}
            />
         );
      case "checkpoint":
         return <CheckpointRoute openCheckpointId={place.openCheckpointId} onLeave={() => go({ view: "progress", tab: "checkpoints" })} />;
      case "probe":
         return <ProbeRoute openAdministrationId={place.openAdministrationId} onLeave={() => go({ view: "progress", tab: "probes" })} />;
      case "assessments":
         return <AssessmentsRoute key={props.barVisits} format={place.format} onChangeFormat={(format) => go({ view: "assessments", format })} />;
      case "settings":
         return (
            <SettingsPage
               tab={place.tab}
               onChangeTab={(tab) => go({ view: "settings", tab })}
               purgeConfirmationPhrase={PURGE_CONFIRMATION_PHRASE}
               saveFile={saveFile}
               aiNoticesOn={props.aiNoticesOn}
               onAiNoticesChange={props.onAiNoticesChange}
               onOpenEvidence={() => go({ view: "evidence" })}
               onRunDiagnostic={() => props.onStartOnboarding("long_gap", null)}
            />
         );
      case "evidence":
         return <MetricsRoute onLeave={() => go({ view: "settings", tab: "operator" })} />;
      case "account":
         return <AccountPage onRenamed={props.onRenamed} onSignOut={props.onSignOut} />;
   }
}
