import { useEffect, useId, useState, type ReactNode } from "react";
import type { UpdateSettingsFields } from "../api/client";
import type { BudgetsPayload, ProviderRole, RoleBudget, SettingsPayload } from "../api/types";
import { daysBetween, formatPlanDate } from "../home/dates";
import type { SettingsTab } from "../routing";
import { Stat, StatGroup } from "../ui/Stats";

/* Each section takes the payload of the route that feeds it, or null while that request is in
   flight or after it failed, and a null section renders its heading and no figure. None of these
   props has a default, so a screen mounted without a route answers for it at the call site.

   Every action resolves true when it happened and false when it did not, a declined or refused
   re-authentication included. No plan sentence exists for a failure, so a control that failed
   says so by coming back enabled with no done state, and one that succeeded carries
   data-outcome="done". */

export type SettingsAction = () => Promise<boolean>;

export interface SettingsScreenProps {
   tab: SettingsTab;
   beforePurge?: ReactNode;
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

function SettingsRow(props: { title: ReactNode; meta?: ReactNode; children?: ReactNode; trail?: ReactNode; testId?: string }) {
   return (
      <div className="list-row" data-testid={props.testId}>
         <div className="list-row-body">
            <span className="list-row-title">{props.title}</span>
            {props.meta !== undefined ? <span className="list-row-meta">{props.meta}</span> : null}
            {props.children}
         </div>

         {props.trail !== undefined ? <div className="list-row-trail">{props.trail}</div> : null}
      </div>
   );
}

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

   const capUsdId = useId();
   const capTokensId = useId();

   return (
      <li data-testid="per-role-cap-row" className="list-row cap-row">
         <div className="list-row-body">
            <span className="list-row-title role-name">{budget.role}</span>
            <span className="list-row-meta">spent today ${budget.cost_usd.toFixed(2)}</span>
         </div>

         <div className="list-row-trail cap-fields">
            <div className="form-field">
               <label className="field-label" htmlFor={capUsdId}>
                  cap $
               </label>
               <input
                  id={capUsdId}
                  className="input input-small input-inline"
                  type="text"
                  inputMode="decimal"
                  value={capUsdField}
                  onChange={(event) => setCapUsdField(event.target.value)}
               />
            </div>

            <div className="form-field">
               <label className="field-label" htmlFor={capTokensId}>
                  cap tokens
               </label>
               <input
                  id={capTokensId}
                  className="input input-small input-inline"
                  type="text"
                  inputMode="numeric"
                  value={capTokensField}
                  onChange={(event) => setCapTokensField(event.target.value)}
               />
            </div>

            <button
               type="button"
               className="button-secondary button-small"
               disabled={!canSave}
               data-outcome={save.outcome}
               onClick={() => save.trigger(budget.role, capUsd, capTokens)}
            >
               save
            </button>
         </div>
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

   const inputId = useId();

   return (
      <div data-testid={`date-field-${label}`} className="cluster date-field">
         <label className="visually-hidden" htmlFor={inputId}>
            {label}
         </label>

         <input id={inputId} className="input input-inline" type="date" value={value} onChange={(event) => setValue(event.target.value)} />

         <button
            type="button"
            className="button-secondary button-small"
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
      <section className="section">
         <h2 className="section-header">Providers</h2>

         <p className="helper">One role, one responsibility. Each role is served by the provider and model below; keys are set by the operator on the server.</p>

         {providers === null ? null : (
            <div className="list list-flush">
               {providers.map((row) => (
                  <SettingsRow
                     key={row.role}
                     testId="provider-row"
                     title={<span className="role-name">{row.role}</span>}
                     meta={[row.provider, row.model].filter((part) => part !== null && part !== "").join(", ")}
                     trail={<span className={row.wired ? "badge badge-correct" : "badge"}>{row.wired ? "wired" : "not wired"}</span>}
                  />
               ))}
            </div>
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
      <section className="section">
         <h2 className="section-header">Budgets</h2>

         <p className="helper">Keep usage predictable. Changing a cap asks for your password again.</p>

         {budgets === null ? null : (
            <>
               <StatGroup>
                  <Stat value={`$${budgets.month_to_date_usd.toFixed(2)}`} label="this month so far" />
               </StatGroup>

               <div className="cluster">
                  <button type="button" className="button-secondary" aria-expanded={showPerRoleCaps} onClick={() => setShowPerRoleCaps(true)}>
                     open
                  </button>
                  <span className="helper">Per-role daily caps</span>
               </div>

               {showPerRoleCaps && (
                  <ul className="list">
                     {budgets.roles.map((budget) => (
                        <RoleCapRow key={budget.role} budget={budget} onCapChange={onCapChange} />
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
      <section className="section">
         <h2 className="section-header">Queue settings</h2>

         {queueSettings === null ? null : (
            <div className="list list-flush">
               <SettingsRow
                  title="Exam target date"
                  meta="Used for your countdown. Confirm the date with your school."
                  trail={<DateField label="exam date" savedValue={queueSettings.exam_date} onSave={(value) => onSettingsChange({ exam_date: value })} />}
               />

               <SettingsRow
                  title="Desired retention"
                  meta="The recall target the scheduler holds each skill to. The engine sets it, and it rises as the exam nears."
                  trail={<span className="badge badge-strong">{queueSettings.desired_retention}</span>}
               />
            </div>
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
      <section className="section">
         <h2 className="section-header">Data export</h2>

         <div className="list list-flush">
            <SettingsRow
               title="Export everything"
               meta="Download notes, answers, settings and assessment history as JSON. Asks for your password again."
               trail={
                  <button
                     type="button"
                     className="button-secondary button-small"
                     disabled={exporting.working}
                     data-outcome={exporting.outcome}
                     onClick={() => exporting.trigger()}
                  >
                     export
                  </button>
               }
            />

            {queueSettings === null ? null : (
               <SettingsRow
                  title="Purge date"
                  meta={
                     statesDefaultRetention ? (
                        <>Default retention: until {DEFAULT_RETENTION_DAYS} days after {formatPlanDate(queueSettings.exam_date)}.</>
                     ) : (
                        "Your records are kept until this date."
                     )
                  }
                  trail={<DateField label="purge date" savedValue={queueSettings.purge_after ?? ""} onSave={(value) => onSettingsChange({ purge_after: value })} />}
               />
            )}
         </div>
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

   const confirmationId = useId();

   return (
      <section className="section">
         <h2 className="section-header">Purge</h2>

         <p style={warningTextStyle}>Purging is destructive and irreversible.</p>

         {hasPhrase ? (
            <div className="form-field">
               <label className="field-label" htmlFor={confirmationId}>
                  Type &quot;{purgeConfirmationPhrase}&quot; to confirm
               </label>
               <input id={confirmationId} className="input" type="text" value={typedConfirmation} onChange={handleConfirmationChange} />
            </div>
         ) : null}

         <div className="cluster">
            <button type="button" className="button-secondary" disabled={!canVerify} onClick={handleVerify}>
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
         </div>
      </section>
   );
}

/* The sections this screen owns, by the settings tab each belongs to. 11's scope 17 names these
   five and no more; the study plan, accessibility, AI notices and the operator's switches are drawn
   beside them by SettingsPage. */
export const SECTIONS_BY_TAB: Record<SettingsTab, ReadonlyArray<string>> = {
   study: ["Queue settings"],
   providers: ["Providers"],
   budgets: ["Budgets"],
   accessibility: [],
   operator: [],
   data: ["Data export", "Purge"]
};

export function SettingsScreen(props: SettingsScreenProps) {
   const { tab } = props;

   return (
      <div className="settings stack stack-wide">
         {tab === "study" ? <QueueSettingsSection queueSettings={props.queueSettings} onSettingsChange={props.onSettingsChange} /> : null}

         {tab === "providers" ? <ProvidersSection providers={props.providers} /> : null}

         {tab === "budgets" ? <BudgetsSection budgets={props.budgets} onCapChange={props.onCapChange} /> : null}

         {tab === "data" ? (
            <>
               <DataExportSection queueSettings={props.queueSettings} onSettingsChange={props.onSettingsChange} onExport={props.onExport} />

               {props.beforePurge}

               <PurgeSection purgeConfirmationPhrase={props.purgeConfirmationPhrase} onReauthenticate={props.onReauthenticate} onPurge={props.onPurge} />
            </>
         ) : null}
      </div>
   );
}
