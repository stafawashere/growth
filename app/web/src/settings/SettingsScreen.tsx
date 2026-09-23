import { useState } from "react";

export interface ProviderRow {
   id: string;
   role: string;
   provider: string;
   model: string;
}

export interface PerRoleCap {
   id: string;
   role: string;
   dailyCapDollars: number;
   spentTodayDollars: number;
}

export interface SettingsScreenProps {
   providers: ReadonlyArray<ProviderRow>;
   onChangeProvider: (id: string) => void;
   dailyCapDollars: number;
   spentThisMonthDollars: number;
   onDailyCapChange: (value: number) => void;
   perRoleCaps: ReadonlyArray<PerRoleCap>;
   onOpenPerRoleCaps: () => void;
   examDate: string;
   onExport: () => void;
   purgeConfirmationPhrase: string;
   onReauthenticate: () => Promise<boolean>;
   onPurge: () => void;
   queueSettingsContent?: React.ReactNode;
}

const surfaceStyle = { background: "var(--growth-surface-raised)", color: "var(--growth-text-primary)" };
const mutedTextStyle = { color: "var(--growth-text-muted)" };
const primaryButtonStyle = {
   background: "var(--growth-accent-base)",
   color: "var(--growth-accent-contrast-text)",
   border: "1px solid var(--growth-border-hairline)"
};
const secondaryButtonStyle = {
   background: "var(--growth-surface-sunken)",
   color: "var(--growth-text-primary)",
   border: "1px solid var(--growth-border-hairline)"
};
const warningTextStyle = { color: "var(--growth-state-incorrect)" };

export function SettingsScreen(props: SettingsScreenProps) {
   const {
      providers,
      onChangeProvider,
      dailyCapDollars,
      spentThisMonthDollars,
      onDailyCapChange,
      perRoleCaps,
      onOpenPerRoleCaps,
      examDate,
      onExport,
      purgeConfirmationPhrase,
      onReauthenticate,
      onPurge,
      queueSettingsContent
   } = props;

   const [typedConfirmation, setTypedConfirmation] = useState("");
   const [reauthenticated, setReauthenticated] = useState(false);
   const [showPerRoleCaps, setShowPerRoleCaps] = useState(false);

   const textMatches = typedConfirmation === purgeConfirmationPhrase;
   const canPurge = textMatches && reauthenticated;

   function handleConfirmationChange(event: React.ChangeEvent<HTMLInputElement>) {
      setTypedConfirmation(event.target.value);
      setReauthenticated(false);
   }

   async function handleVerify() {
      const verified = await onReauthenticate();

      setReauthenticated(verified);
   }

   function handleDailyCapChange(event: React.ChangeEvent<HTMLInputElement>) {
      onDailyCapChange(Number(event.target.value));
   }

   function handleOpenPerRoleCaps() {
      onOpenPerRoleCaps();
      setShowPerRoleCaps(true);
   }

   return (
      <section style={surfaceStyle}>
         <h1 style={{ color: "var(--growth-text-primary)" }}>Settings</h1>

         <section>
            <h2 style={{ color: "var(--growth-text-primary)" }}>Providers</h2>

            <ul>
               {providers.map((row) => (
                  <li key={row.id} data-testid="provider-row">
                     <span style={mutedTextStyle}>{row.role}</span>

                     <span style={mutedTextStyle}>{row.provider}</span>

                     <span style={mutedTextStyle}>{row.model}</span>

                     <button type="button" style={secondaryButtonStyle} onClick={() => onChangeProvider(row.id)}>
                        change
                     </button>
                  </li>
               ))}
            </ul>
         </section>

         <section>
            <h2 style={{ color: "var(--growth-text-primary)" }}>Budgets</h2>

            <label>
               daily cap, all roles
               <input type="number" value={dailyCapDollars} onChange={handleDailyCapChange} />
            </label>

            <button type="button" style={secondaryButtonStyle} onClick={handleOpenPerRoleCaps}>
               open
            </button>

            <p style={mutedTextStyle}>this month so far ${spentThisMonthDollars.toFixed(2)}</p>

            {showPerRoleCaps && (
               <ul>
                  {perRoleCaps.map((cap) => (
                     <li key={cap.id} data-testid="per-role-cap-row">
                        <span style={mutedTextStyle}>{cap.role}</span>

                        <span style={mutedTextStyle}>
                           cap ${cap.dailyCapDollars.toFixed(2)}, spent today ${cap.spentTodayDollars.toFixed(2)}
                        </span>
                     </li>
                  ))}
               </ul>
            )}
         </section>

         <section>
            <h2 style={{ color: "var(--growth-text-primary)" }}>Queue settings</h2>

            {queueSettingsContent ?? <p style={mutedTextStyle}>No queue settings are defined yet.</p>}
         </section>

         <section>
            <h2 style={{ color: "var(--growth-text-primary)" }}>Data export</h2>

            <button type="button" style={secondaryButtonStyle} onClick={onExport}>
               export
            </button>

            <p style={mutedTextStyle}>Default retention: until 30 days after {examDate}.</p>
         </section>

         <section>
            <h2 style={{ color: "var(--growth-text-primary)" }}>Purge</h2>

            <p style={warningTextStyle}>Purging is destructive and irreversible.</p>

            <label>
               Type &quot;{purgeConfirmationPhrase}&quot; to confirm
               <input type="text" value={typedConfirmation} onChange={handleConfirmationChange} />
            </label>

            <button type="button" style={secondaryButtonStyle} disabled={!textMatches} onClick={handleVerify}>
               verify identity
            </button>

            <button type="button" style={primaryButtonStyle} disabled={!canPurge} onClick={onPurge}>
               purge everything
            </button>
         </section>
      </section>
   );
}
