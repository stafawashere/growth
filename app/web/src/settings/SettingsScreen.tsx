import { useEffect, useState } from "react";
import type { UpdateSettingsFields } from "../api/client";
import type { BudgetsPayload, ProviderRole, RoleBudget, SettingsPayload } from "../api/types";
import { daysBetween, formatPlanDate } from "../home/dates";

/* Each section takes the payload of the route that feeds it, or null while that request is in
   flight or after it failed, and a null section renders its heading and no figure. None of these
   props has a default, so a screen mounted without a route answers for it at the call site.

   Every action resolves true when it happened and false when it did not, a declined or refused
   re-authentication included. No plan sentence exists for a failure, so a control that failed
   says so by coming back enabled with no done state, and one that succeeded carries
   data-outcome="done". */

export type SettingsAction = () => Promise<boolean>;

export interface SettingsScreenProps {
   providers: ReadonlyArray<ProviderRole> | null;
   budgets: BudgetsPayload | null;
   onCapChange: (role: string, capUsd: number | null, capTokens: number | null) => Promise<boolean>;
   queueSettings: SettingsPayload | null;
   onSettingsChange: (fields: UpdateSettingsFields) => Promise<boolean>;
   onExport: SettingsAction;
   purgeConfirmationPhrase: string | null;
   onReauthenticate: SettingsAction;
   onPurge: (confirmation: string) => Promise<boolean>;
}

/* docs/plan/08-design-brief.md, Settings wireframe: "Default retention: until 30 days after
   10 May 2027", which 06 defines as purge_after defaulting to exam_date plus 30 days. */
export const DEFAULT_RETENTION_DAYS = 30;

export const DONE_OUTCOME = "done";

const warningTextStyle = { color: "var(--growth-state-incorrect)" };

function useAction<Args extends unknown[]>(run: (...args: Args) => Promise<boolean>) {
   const [working, setWorking] = useState(false);
   const [done, setDone] = useState(false);

   async function trigger(...args: Args) {
      setWorking(true);
      setDone(false);

      try {
         const happened = await run(...args);

         setDone(happened);

         return happened;
      } finally {
         setWorking(false);
      }
   }

   const outcome = done ? DONE_OUTCOME : undefined;

   return { working, outcome, trigger };
}

function purgesAtTheDefault(settings: SettingsPayload) {
   const hasPurgeDate = settings.purge_after !== null;

   if (!hasPurgeDate) {
      return false;
   }

   return daysBetween(settings.exam_date, settings.purge_after as string) === DEFAULT_RETENTION_DAYS;
}

function capFromField(text: string) {
   const trimmed = text.trim();
   const isBlank = trimmed === "";

   if (isBlank) {
      return null;
   }

   return Number(trimmed);
}

function fieldFromCap(cap: number | null) {
   return cap === null ? "" : String(cap);
}

function RoleCapRow(props: { budget: RoleBudget; onCapChange: SettingsScreenProps["onCapChange"] }) {
   const { budget, onCapChange } = props;

   const [capUsdField, setCapUsdField] = useState(fieldFromCap(budget.cap_usd));
   const [capTokensField, setCapTokensField] = useState(fieldFromCap(budget.cap_tokens));
   const save = useAction(onCapChange);

   useEffect(() => {
      setCapUsdField(fieldFromCap(budget.cap_usd));
      setCapTokensField(fieldFromCap(budget.cap_tokens));
   }, [budget.cap_usd, budget.cap_tokens]);

   const capUsd = capFromField(capUsdField);
   const capTokens = capFromField(capTokensField);
   const namesNoCap = capUsd === null && capTokens === null;
   const isUnreadable = Number.isNaN(capUsd) || Number.isNaN(capTokens);
   const canSave = !namesNoCap && !isUnreadable && !save.working;

   return (
      <li data-testid="per-role-cap-row">
         <span className="muted">{budget.role}</span>

         <label>
            cap $
            <input
               type="text"
               inputMode="decimal"
               value={capUsdField}
               onChange={(event) => setCapUsdField(event.target.value)}
            />
         </label>

         <label>
            cap tokens
            <input
               type="text"
               inputMode="numeric"
               value={capTokensField}
               onChange={(event) => setCapTokensField(event.target.value)}
            />
         </label>

         <span className="muted">spent today ${budget.cost_usd.toFixed(2)}</span>

         <button
            type="button"
            className="text-button"
            disabled={!canSave}
            data-outcome={save.outcome}
            onClick={() => save.trigger(budget.role, capUsd, capTokens)}
         >
            save
         </button>
      </li>
   );
}

function DateField(props: {
   label: string;
   savedValue: string;
   onSave: (value: string) => Promise<boolean>;
}) {
   const { label, savedValue, onSave } = props;

   const [value, setValue] = useState(savedValue);
   const save = useAction(onSave);

   useEffect(() => {
      setValue(savedValue);
   }, [savedValue]);

   const isChanged = value !== savedValue;
   const isFilled = value !== "";
   const canSave = isChanged && isFilled && !save.working;

   return (
      <div data-testid={`date-field-${label}`}>
         <label>
            {label}
            <input type="date" value={value} onChange={(event) => setValue(event.target.value)} />
         </label>

         <button
            type="button"
            className="text-button"
            disabled={!canSave}
            data-outcome={save.outcome}
            onClick={() => save.trigger(value)}
         >
            save
         </button>
      </div>
   );
}

function ProvidersSection(props: { providers: SettingsScreenProps["providers"] }) {
   const { providers } = props;

   return (
      <section>
         <h2 className="section-heading">Providers</h2>

         {providers === null ? null : (
            <table>
               <tbody>
                  {providers.map((row) => (
                     <tr key={row.role} data-testid="provider-row">
                        <td className="muted">{row.role}</td>

                        <td className="muted">{row.provider ?? ""}</td>

                        <td className="muted">{row.model ?? ""}</td>

                        <td className="muted">{row.wired ? "wired" : "not wired"}</td>
                     </tr>
                  ))}
               </tbody>
            </table>
         )}
      </section>
   );
}

function BudgetsSection(props: {
   budgets: SettingsScreenProps["budgets"];
   onCapChange: SettingsScreenProps["onCapChange"];
}) {
   const { budgets, onCapChange } = props;

   const [showPerRoleCaps, setShowPerRoleCaps] = useState(false);

   return (
      <section>
         <h2 className="section-heading">Budgets</h2>

         {budgets === null ? null : (
            <>
               <button type="button" className="text-button" onClick={() => setShowPerRoleCaps(true)}>
                  open
               </button>

               <p className="muted">this month so far ${budgets.month_to_date_usd.toFixed(2)}</p>

               {showPerRoleCaps && (
                  <ul>
                     {budgets.roles.map((budget) => (
                        <RoleCapRow
                           key={budget.role}
                           budget={budget}
                           onCapChange={onCapChange}
                        />
                     ))}
                  </ul>
               )}
            </>
         )}
      </section>
   );
}

function QueueSettingsSection(props: {
   queueSettings: SettingsScreenProps["queueSettings"];
   onSettingsChange: SettingsScreenProps["onSettingsChange"];
}) {
   const { queueSettings, onSettingsChange } = props;

   return (
      <section>
         <h2 className="section-heading">Queue settings</h2>

         {queueSettings === null ? null : (
            <>
               <DateField
                  label="exam date"
                  savedValue={queueSettings.exam_date}
                  onSave={(value) => onSettingsChange({ exam_date: value })}
               />

               <dl>
                  <dt className="muted">desired retention</dt>
                  <dd>{queueSettings.desired_retention}</dd>
               </dl>
            </>
         )}
      </section>
   );
}

function DataExportSection(props: {
   queueSettings: SettingsScreenProps["queueSettings"];
   onSettingsChange: SettingsScreenProps["onSettingsChange"];
   onExport: SettingsScreenProps["onExport"];
}) {
   const { queueSettings, onSettingsChange, onExport } = props;

   const exporting = useAction(onExport);
   const statesDefaultRetention = queueSettings !== null && purgesAtTheDefault(queueSettings);

   return (
      <section>
         <h2 className="section-heading">Data export</h2>

         <button
            type="button"
            className="text-button"
            disabled={exporting.working}
            data-outcome={exporting.outcome}
            onClick={() => exporting.trigger()}
         >
            export
         </button>

         {queueSettings === null ? null : (
            <DateField
               label="purge date"
               savedValue={queueSettings.purge_after ?? ""}
               onSave={(value) => onSettingsChange({ purge_after: value })}
            />
         )}

         {statesDefaultRetention ? (
            <p className="muted">
               Default retention: until {DEFAULT_RETENTION_DAYS} days after {formatPlanDate(queueSettings.exam_date)}.
            </p>
         ) : null}
      </section>
   );
}

function PurgeSection(props: {
   purgeConfirmationPhrase: SettingsScreenProps["purgeConfirmationPhrase"];
   onReauthenticate: SettingsScreenProps["onReauthenticate"];
   onPurge: SettingsScreenProps["onPurge"];
}) {
   const { purgeConfirmationPhrase, onReauthenticate, onPurge } = props;

   const [typedConfirmation, setTypedConfirmation] = useState("");
   const [reauthenticated, setReauthenticated] = useState(false);
   const purging = useAction(onPurge);

   const hasPhrase = purgeConfirmationPhrase !== null;
   const textMatches = hasPhrase && typedConfirmation === purgeConfirmationPhrase;
   const isPurged = purging.outcome === DONE_OUTCOME;
   const canVerify = textMatches && !purging.working && !isPurged;
   const canPurge = canVerify && reauthenticated;

   function handleConfirmationChange(event: React.ChangeEvent<HTMLInputElement>) {
      setTypedConfirmation(event.target.value);
      setReauthenticated(false);
   }

   async function handleVerify() {
      const verified = await onReauthenticate();

      setReauthenticated(verified);
   }

   async function handlePurge() {
      setReauthenticated(false);
      await purging.trigger(typedConfirmation);
   }

   return (
      <section>
         <h2 className="section-heading">Purge</h2>

         <p style={warningTextStyle}>Purging is destructive and irreversible.</p>

         {hasPhrase ? (
            <label>
               Type &quot;{purgeConfirmationPhrase}&quot; to confirm
               <input type="text" value={typedConfirmation} onChange={handleConfirmationChange} />
            </label>
         ) : null}

         <button type="button" className="text-button" disabled={!canVerify} onClick={handleVerify}>
            verify identity
         </button>

         <button
            type="button"
            className="text-button text-button-destructive"
            disabled={!canPurge}
            data-outcome={purging.outcome}
            onClick={handlePurge}
         >
            purge everything
         </button>
      </section>
   );
}

export function SettingsScreen(props: SettingsScreenProps) {
   return (
      <section className="card settings">
         <h1 className="screen-title">Settings</h1>

         <ProvidersSection providers={props.providers} />

         <BudgetsSection budgets={props.budgets} onCapChange={props.onCapChange} />

         <QueueSettingsSection queueSettings={props.queueSettings} onSettingsChange={props.onSettingsChange} />

         <DataExportSection
            queueSettings={props.queueSettings}
            onSettingsChange={props.onSettingsChange}
            onExport={props.onExport}
         />

         <PurgeSection
            purgeConfirmationPhrase={props.purgeConfirmationPhrase}
            onReauthenticate={props.onReauthenticate}
            onPurge={props.onPurge}
         />
      </section>
   );
}