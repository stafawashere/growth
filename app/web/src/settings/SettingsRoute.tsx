import { useEffect, useRef, useState } from "react";
import {
   readBudgets,
   readExport,
   readProviders,
   readSettings,
   reauthenticate,
   requestExport,
   requestPurge,
   updateBudget,
   updateSettings,
   type UpdateSettingsFields
} from "../api/client";
import type { BudgetsPayload, ProviderRole, SettingsPayload } from "../api/types";
import { SettingsScreen } from "./SettingsScreen";

/* purgeConfirmationPhrase has no source a client route serves and no plan sentence, so the caller
   passes it, and null withholds the purge controls rather than guessing a phrase. saveFile is the
   one browser side effect an export needs, passed in so the route never picks a download path on
   its own. */

export interface SettingsRouteProps {
   purgeConfirmationPhrase: string | null;
   saveFile: (name: string, contents: Blob) => void;
}

function exportFileName(exportId: string) {
   return `growth-export-${exportId}.json`;
}

export function SettingsRoute({ purgeConfirmationPhrase, saveFile }: SettingsRouteProps) {
   const [providers, setProviders] = useState<ProviderRole[] | null>(null);
   const [budgets, setBudgets] = useState<BudgetsPayload | null>(null);
   const [queueSettings, setQueueSettings] = useState<SettingsPayload | null>(null);

   const purgeToken = useRef<string | null>(null);
   const inFlight = useRef(false);

   useEffect(() => {
      let isCurrent = true;

      function keep<T>(set: (value: T) => void) {
         return (value: T) => {
            if (isCurrent) {
               set(value);
            }
         };
      }

      const ignoreFailure = () => undefined;

      readProviders().then((payload) => payload.roles).then(keep(setProviders), ignoreFailure);
      readBudgets().then(keep(setBudgets), ignoreFailure);
      readSettings().then(keep(setQueueSettings), ignoreFailure);

      return () => {
         isCurrent = false;
      };
   }, []);

   /* Resolves whether the action happened. A declined passkey, a refused token and a failed
      request all resolve false, and the screen shows that by returning the control unchanged. */
   async function exclusively(action: () => Promise<void>) {
      const isBusy = inFlight.current;

      if (isBusy) {
         return false;
      }

      inFlight.current = true;

      try {
         await action();

         return true;
      } catch {
         return false;
      } finally {
         inFlight.current = false;
      }
   }

   function changeCap(role: string, capUsd: number | null, capTokens: number | null) {
      return exclusively(async () => {
         const token = await reauthenticate();
         const readBack = await updateBudget({ role, cap_usd: capUsd, cap_tokens: capTokens, reauth_token: token });

         setBudgets(readBack);
      });
   }

   function changeSettings(fields: UpdateSettingsFields) {
      return exclusively(async () => {
         const readBack = await updateSettings(fields);

         setQueueSettings(readBack);
      });
   }

   function exportEverything() {
      return exclusively(async () => {
         const token = await reauthenticate();
         const job = await requestExport({ reauth_token: token });
         const archive = await readExport(job.id);

         saveFile(exportFileName(job.id), archive);
      });
   }

   async function reauthenticateForPurge() {
      purgeToken.current = null;

      try {
         purgeToken.current = await reauthenticate();
      } catch {
         return false;
      }

      return true;
   }

   async function purge(confirmation: string) {
      const token = purgeToken.current;
      const hasToken = token !== null;

      if (!hasToken) {
         return false;
      }

      purgeToken.current = null;

      return exclusively(async () => {
         await requestPurge({ confirmation, reauth_token: token });
      });
   }

   return (
      <SettingsScreen
         providers={providers}
         budgets={budgets}
         onCapChange={changeCap}
         queueSettings={queueSettings}
         onSettingsChange={changeSettings}
         onExport={exportEverything}
         purgeConfirmationPhrase={purgeConfirmationPhrase}
         onReauthenticate={reauthenticateForPurge}
         onPurge={purge}
      />
   );
}