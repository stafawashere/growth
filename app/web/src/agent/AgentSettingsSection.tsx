import { useEffect, useId, useState } from "react";

import {
   clearAgentMemory,
   deleteAgentConversation,
   deleteAgentMemory,
   editAgentMemory,
   readAgentConversation,
   readAgentConversations,
   readAgentMemories,
   readAgentProfile,
   updateAgentSettings
} from "../api/client";
import type {
   AgentConversationPayload,
   AgentConversationSummary,
   AgentMemoriesPayload,
   AgentMemoryEntry,
   AgentProfilePayload,
   AgentScreenKind
} from "../api/types";
import { formatPlanDate } from "../home/dates";
import { MathText } from "../math/MathText";
import { useAction } from "../settings/SettingsScreen";
import {
   CANCEL_LABEL,
   CONVERSATIONS_HEADING,
   DELETE_LABEL,
   EDIT_LABEL,
   FORGET_EVERYTHING,
   FORGET_EVERYTHING_PHRASE,
   FORGET_THIS,
   MEMORY_HEADING,
   MEMORY_KIND_LABELS,
   OPEN_LABEL,
   PAUSE_MEMORY,
   PROFILE_HEADING,
   PROFILE_OFF,
   RETENTION_LINE,
   SAVE_LABEL,
   TUTOR_SAID,
   YOU_SAID
} from "./agentCopy";

/* The Tutor tab in Settings (docs/agent/design.md, "Memory in settings"), backed by the agent
   settings routes. Each section loads on its own, so one failing leaves the others drawn, and
   every action follows SettingsScreen's pattern: a control is disabled while it works, carries
   data-outcome="done" once it happened, and comes back unchanged when it did not. */

const SCREEN_NAMES: Record<AgentScreenKind, string> = {
   today: "Today",
   session_item: "Today, a practice item",
   session_lesson: "Today, a lesson",
   lesson: "Lesson",
   review: "Review",
   progress: "Progress",
   assessments: "Assessments",
   settings: "Settings",
   other: "Elsewhere in the app"
};

const RECORDED_ONLY_FIELDS = ["stated_requests"];

function dateOf(timestamp: string) {
   return formatPlanDate(timestamp.slice(0, 10));
}

async function happened(action: () => Promise<unknown>) {
   try {
      await action();

      return true;
   } catch {
      return false;
   }
}

function MemoryRow(props: { entry: AgentMemoryEntry; onForget: (id: string) => Promise<boolean>; onEdit: (id: string, text: string) => Promise<boolean> }) {
   const { entry } = props;
   const [isEditing, setIsEditing] = useState(false);
   const [text, setText] = useState(entry.text);
   const forget = useAction(() => props.onForget(entry.id));
   const save = useAction(async () => {
      const saved = await props.onEdit(entry.id, text.trim());

      if (saved) {
         setIsEditing(false);
      }

      return saved;
   });
   const fieldId = useId();
   const canSave = text.trim() !== "" && !save.working;

   return (
      <li className="list-row" data-testid="agent-memory-row">
         <div className="list-row-body">
            {isEditing ? (
               <div className="form-field">
                  <label className="field-label" htmlFor={fieldId}>
                     {EDIT_LABEL}
                  </label>
                  <input id={fieldId} className="input" type="text" value={text} onChange={(event) => setText(event.target.value)} />
               </div>
            ) : (
               <span className="list-row-title">{entry.text}</span>
            )}

            <span className="list-row-meta">{dateOf(entry.created_at)}</span>
         </div>

         <div className="list-row-trail cluster">
            {entry.editable && !isEditing ? (
               <button type="button" className="text-button" onClick={() => setIsEditing(true)}>
                  {EDIT_LABEL}
               </button>
            ) : null}

            {isEditing ? (
               <>
                  <button type="button" className="button-secondary button-small" disabled={!canSave} data-outcome={save.outcome} onClick={() => save.trigger()}>
                     {SAVE_LABEL}
                  </button>

                  <button
                     type="button"
                     className="text-button"
                     onClick={() => {
                        setText(entry.text);
                        setIsEditing(false);
                     }}
                  >
                     {CANCEL_LABEL}
                  </button>
               </>
            ) : null}

            <button type="button" className="text-button text-button-destructive" disabled={forget.working} data-outcome={forget.outcome} onClick={() => forget.trigger()}>
               {FORGET_THIS}
            </button>
         </div>
      </li>
   );
}

function ForgetEverything(props: { onClear: (phrase: string) => Promise<boolean> }) {
   const [typed, setTyped] = useState("");
   const clearing = useAction(props.onClear);
   const fieldId = useId();
   const matches = typed === FORGET_EVERYTHING_PHRASE;

   return (
      <div className="stack stack-tight" data-testid="agent-forget-everything">
         <div className="form-field">
            <label className="field-label" htmlFor={fieldId}>
               Type &quot;{FORGET_EVERYTHING_PHRASE}&quot; to confirm
            </label>
            <input id={fieldId} className="input" type="text" value={typed} onChange={(event) => setTyped(event.target.value)} />
         </div>

         <div className="cluster">
            <button
               type="button"
               className="text-button text-button-destructive"
               disabled={!matches || clearing.working}
               data-outcome={clearing.outcome}
               onClick={() => clearing.trigger(typed)}
            >
               {FORGET_EVERYTHING}
            </button>
         </div>
      </div>
   );
}

function MemorySection(props: { memories: AgentMemoriesPayload | null; onChanged: () => void; setMemories: (next: AgentMemoriesPayload) => void }) {
   const { memories } = props;
   const [pauseWorking, setPauseWorking] = useState(false);

   async function forget(id: string) {
      const done = await happened(() => deleteAgentMemory(id));

      if (done) {
         props.onChanged();
      }

      return done;
   }

   async function edit(id: string, text: string) {
      const done = await happened(() => editAgentMemory(id, text));

      if (done) {
         props.onChanged();
      }

      return done;
   }

   async function clear(phrase: string) {
      const done = await happened(() => clearAgentMemory(phrase));

      if (done) {
         props.onChanged();
      }

      return done;
   }

   async function pause(paused: boolean) {
      if (memories === null) {
         return;
      }

      setPauseWorking(true);

      try {
         const readBack = await updateAgentSettings({ memory_paused: paused });

         props.setMemories({ ...memories, memory_paused: readBack.memory_paused });
      } catch {
         // a refused change leaves the switch as the server last reported it
      } finally {
         setPauseWorking(false);
      }
   }

   const groups = memories === null ? [] : memories.groups.filter((group) => group.entries.length > 0);

   return (
      <section className="section" data-testid="agent-memory-section">
         <h2 className="section-header">{MEMORY_HEADING}</h2>

         {memories === null ? null : (
            <>
               <label className="check">
                  <input type="checkbox" role="switch" checked={memories.memory_paused} disabled={pauseWorking} onChange={(event) => void pause(event.target.checked)} />
                  {PAUSE_MEMORY}
               </label>

               {groups.map((group) => (
                  <div key={group.kind} className="stack stack-tight" data-testid={`agent-memory-group-${group.kind}`}>
                     <h3 className="eyebrow">{MEMORY_KIND_LABELS[group.kind] ?? group.label}</h3>

                     <ul className="list list-flush">
                        {group.entries.map((entry) => (
                           <MemoryRow key={`${entry.id}-${entry.text}`} entry={entry} onForget={forget} onEdit={edit} />
                        ))}
                     </ul>
                  </div>
               ))}

               <ForgetEverything onClear={clear} />
            </>
         )}
      </section>
   );
}

function ConversationRow(props: { conversation: AgentConversationSummary; onDelete: (id: string) => Promise<boolean> }) {
   const { conversation } = props;
   const [opened, setOpened] = useState<AgentConversationPayload | null>(null);
   const deleting = useAction(() => props.onDelete(conversation.id));

   async function toggle() {
      if (opened !== null) {
         setOpened(null);

         return;
      }

      try {
         setOpened(await readAgentConversation(conversation.id));
      } catch {
         // a conversation that cannot be read stays closed
      }
   }

   return (
      <li className="list-row" data-testid="agent-conversation-row">
         <div className="list-row-body">
            <span className="list-row-title">{dateOf(conversation.opened_at)}</span>
            <span className="list-row-meta">{SCREEN_NAMES[conversation.opened_on_screen] ?? conversation.opened_on_screen}</span>

            {opened !== null ? (
               <ol className="agent-turns" data-testid="agent-conversation-turns">
                  {opened.turns.map((turn) => (
                     <li key={turn.id} className={turn.role === "student" ? "agent-turn agent-turn-student" : "agent-turn agent-turn-tutor"}>
                        <span className="visually-hidden">{turn.role === "student" ? YOU_SAID : TUTOR_SAID}</span>
                        <p>{turn.role === "student" ? turn.text : <MathText text={turn.text} renderer="tutor" />}</p>
                     </li>
                  ))}
               </ol>
            ) : null}
         </div>

         <div className="list-row-trail cluster">
            <button type="button" className="text-button" aria-expanded={opened !== null} onClick={() => void toggle()}>
               {OPEN_LABEL}
            </button>

            <button type="button" className="text-button text-button-destructive" disabled={deleting.working} data-outcome={deleting.outcome} onClick={() => deleting.trigger()}>
               {DELETE_LABEL}
            </button>
         </div>
      </li>
   );
}

function ConversationsSection(props: { conversations: AgentConversationSummary[] | null; onDelete: (id: string) => Promise<boolean> }) {
   return (
      <section className="section" data-testid="agent-conversations-section">
         <h2 className="section-header">{CONVERSATIONS_HEADING}</h2>

         <p className="helper">{RETENTION_LINE}</p>

         {props.conversations === null ? null : (
            <ul className="list list-flush">
               {props.conversations.map((conversation) => (
                  <ConversationRow key={conversation.id} conversation={conversation} onDelete={props.onDelete} />
               ))}
            </ul>
         )}
      </section>
   );
}

function valueInWords(value: unknown) {
   if (Array.isArray(value)) {
      return value.map((part) => (typeof part === "object" ? JSON.stringify(part) : String(part))).join(", ");
   }

   if (typeof value === "object" && value !== null) {
      return JSON.stringify(value);
   }

   return String(value);
}

function ProfileSection(props: { profile: AgentProfilePayload | null }) {
   const { profile } = props;
   const isOn = profile !== null && (profile.experiment === "on" || profile.experiment === "randomised");
   const fields = isOn && profile.profile !== null ? Object.entries(profile.profile) : [];

   return (
      <section className="section" data-testid="agent-profile-section">
         <h2 className="section-header">{PROFILE_HEADING}</h2>

         {profile !== null && !isOn ? <p className="helper">{PROFILE_OFF}</p> : null}

         {fields.length > 0 ? (
            <ul className="list list-flush">
               {fields.map(([name, value]) => (
                  <li key={name} className="list-row">
                     <div className="list-row-body">
                        <span className="list-row-title">{name.replace(/_/g, " ")}</span>
                        <span className="list-row-meta">
                           {valueInWords(value)}
                           {RECORDED_ONLY_FIELDS.includes(name) ? ". Recorded and not applied." : null}
                        </span>
                     </div>
                  </li>
               ))}
            </ul>
         ) : null}
      </section>
   );
}

export function AgentSettingsSection() {
   const [memories, setMemories] = useState<AgentMemoriesPayload | null>(null);
   const [conversations, setConversations] = useState<AgentConversationSummary[] | null>(null);
   const [profile, setProfile] = useState<AgentProfilePayload | null>(null);
   const [reads, setReads] = useState(0);

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

      Promise.resolve()
         .then(() => readAgentMemories())
         .then(keep(setMemories), ignoreFailure);
      Promise.resolve()
         .then(() => readAgentConversations())
         .then((payload) => payload.conversations)
         .then(keep(setConversations), ignoreFailure);
      Promise.resolve()
         .then(() => readAgentProfile())
         .then(keep(setProfile), ignoreFailure);

      return () => {
         isCurrent = false;
      };
   }, [reads]);

   const readAgain = () => setReads((count) => count + 1);

   async function deleteConversation(id: string) {
      const done = await happened(() => deleteAgentConversation(id));

      if (done) {
         setConversations((current) => (current === null ? current : current.filter((conversation) => conversation.id !== id)));
      }

      return done;
   }

   return (
      <div className="settings stack stack-wide" data-testid="agent-settings">
         <MemorySection memories={memories} onChanged={readAgain} setMemories={setMemories} />

         <ConversationsSection conversations={conversations} onDelete={deleteConversation} />

         <ProfileSection profile={profile} />
      </div>
   );
}
