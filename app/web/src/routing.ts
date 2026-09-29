import { useCallback, useEffect, useState } from "react";

import type { OnboardingReason } from "./onboarding/OnboardingScreen";

/* Where the student is, written into the address as a hash route, so a reload or the back button
   keeps their place. The server serves one page, so the hash is the whole route. */

export type ProgressTab = "mastery" | "calibration" | "representations" | "checkpoints" | "probes" | "lessons";

export type AssessmentFormat = "unit" | "frq" | "drill" | "mock" | "checkpoint";

export type SettingsTab = "study" | "providers" | "budgets" | "accessibility" | "operator" | "data" | "tutor";

export type LessonReturn = "lessons" | "progress";

export type Place =
   | { view: "home" }
   | { view: "session"; resumeSessionId: string | null }
   | { view: "onboarding"; reason: OnboardingReason; resumeSessionId: string | null }
   | { view: "lessons" }
   | { view: "lesson"; lessonId: string; conceptName: string; returnTo: LessonReturn }
   | { view: "review" }
   | { view: "progress"; tab: ProgressTab }
   | { view: "checkpoint"; openCheckpointId: string | null }
   | { view: "probe"; openAdministrationId: string | null }
   | { view: "assessments"; format: AssessmentFormat }
   | { view: "settings"; tab: SettingsTab }
   | { view: "evidence" }
   | { view: "account" };

export type View = Place["view"];

export const PROGRESS_TABS: ReadonlyArray<ProgressTab> = ["mastery", "calibration", "representations", "checkpoints", "probes", "lessons"];

export const ASSESSMENT_FORMATS: ReadonlyArray<AssessmentFormat> = ["unit", "frq", "drill", "mock", "checkpoint"];

export const SETTINGS_TABS: ReadonlyArray<SettingsTab> = ["study", "providers", "budgets", "accessibility", "operator", "data", "tutor"];

const ONBOARDING_REASONS: ReadonlyArray<OnboardingReason> = ["first_login", "long_gap"];

export const HOME: Place = { view: "home" };

function oneOf<T extends string>(value: string | undefined, allowed: ReadonlyArray<T>, fallback: T): T {
   const isAllowed = value !== undefined && (allowed as ReadonlyArray<string>).includes(value);

   return isAllowed ? (value as T) : fallback;
}

function decoded(value: string | undefined) {
   const hasValue = value !== undefined && value !== "";

   if (!hasValue) {
      return null;
   }

   try {
      return decodeURIComponent(value);
   } catch {
      return null;
   }
}

export function placeFromHash(hash: string): Place {
   const [path, query = ""] = hash.replace(/^#\/?/, "").split("?");
   const [view, first, second] = path.split("/");
   const search = new URLSearchParams(query);

   switch (view) {
      case "session":
         return { view: "session", resumeSessionId: decoded(first) };
      case "onboarding":
         return {
            view: "onboarding",
            reason: oneOf(first, ONBOARDING_REASONS, "first_login"),
            resumeSessionId: decoded(second)
         };
      case "lessons":
         return { view: "lessons" };
      case "lesson": {
         const lessonId = decoded(first);

         if (lessonId === null) {
            return { view: "lessons" };
         }

         return {
            view: "lesson",
            lessonId,
            conceptName: search.get("concept") ?? "",
            returnTo: oneOf(second, ["lessons", "progress"] as const, "lessons")
         };
      }
      case "review":
         return { view: "review" };
      case "progress":
         return { view: "progress", tab: oneOf(first, PROGRESS_TABS, "mastery") };
      case "checkpoint":
         return { view: "checkpoint", openCheckpointId: decoded(first) };
      case "probe":
         return { view: "probe", openAdministrationId: decoded(first) };
      case "assessments":
         return { view: "assessments", format: oneOf(first, ASSESSMENT_FORMATS, "unit") };
      case "settings":
         return first === "evidence" ? { view: "evidence" } : { view: "settings", tab: oneOf(first, SETTINGS_TABS, "study") };
      case "account":
         return { view: "account" };
      default:
         return HOME;
   }
}

export function hashFor(place: Place): string {
   switch (place.view) {
      case "home":
         return "#/home";
      case "session":
         return place.resumeSessionId === null ? "#/session" : `#/session/${encodeURIComponent(place.resumeSessionId)}`;
      case "onboarding": {
         const resume = place.resumeSessionId === null ? "" : `/${encodeURIComponent(place.resumeSessionId)}`;

         return `#/onboarding/${place.reason}${resume}`;
      }
      case "lessons":
         return "#/lessons";
      case "lesson": {
         const concept = place.conceptName === "" ? "" : `?concept=${encodeURIComponent(place.conceptName)}`;

         return `#/lesson/${encodeURIComponent(place.lessonId)}/${place.returnTo}${concept}`;
      }
      case "review":
         return "#/review";
      case "progress":
         return `#/progress/${place.tab}`;
      case "checkpoint":
         return place.openCheckpointId === null ? "#/checkpoint" : `#/checkpoint/${encodeURIComponent(place.openCheckpointId)}`;
      case "probe":
         return place.openAdministrationId === null ? "#/probe" : `#/probe/${encodeURIComponent(place.openAdministrationId)}`;
      case "assessments":
         return `#/assessments/${place.format}`;
      case "settings":
         return `#/settings/${place.tab}`;
      case "evidence":
         return "#/settings/evidence";
      case "account":
         return "#/account";
   }
}

function currentHash() {
   return typeof window === "undefined" ? "" : window.location.hash;
}

/* The place follows the address, and going somewhere writes the address, so the browser's history
   holds every step. The state is set at once rather than waiting for hashchange, so a click redraws
   in the same turn. */
export interface GoOptions {
   replace?: boolean;
}

export function usePlace(): [Place, (place: Place, options?: GoOptions) => void] {
   const [place, setPlace] = useState<Place>(() => placeFromHash(currentHash()));

   useEffect(() => {
      function follow() {
         setPlace(placeFromHash(currentHash()));
      }

      window.addEventListener("hashchange", follow);

      return () => window.removeEventListener("hashchange", follow);
   }, []);

   const go = useCallback((next: Place, options?: GoOptions) => {
      setPlace(next);

      const target = hashFor(next);
      const isNewAddress = currentHash() !== target;
      const replaces = options?.replace === true;

      if (isNewAddress && replaces) {
         window.history.replaceState(window.history.state, "", target);
      } else if (isNewAddress) {
         window.location.hash = target;
      }

      const page = document.scrollingElement;
      const canScroll = page !== null && page !== undefined;

      if (canScroll) {
         page.scrollTop = 0;
      }
   }, []);

   return [place, go];
}
