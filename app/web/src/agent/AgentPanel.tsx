import { useEffect, useState, type FormEvent, type KeyboardEvent } from "react";

import { MathText } from "../math/MathText";
import { holdUnclosedMath } from "../math/mathjson";
import { TUTOR_SHEET_CLASS } from "../styles/motion";
import { Icon } from "../ui/Icon";
import {
   CLOSE_LABEL,
   COMPOSER_LABEL,
   CONVERSATION_CEILING,
   DAILY_CAP,
   EMPTY_ELSEWHERE,
   EMPTY_ON_ITEM,
   FULL_HEIGHT_LABEL,
   MINUTE_CAP,
   OFFLINE,
   PANEL_TITLE,
   SCREEN_REFUSED,
   SEND_LABEL,
   SHOW_ITEM_LABEL,
   SIGN_IN_EXPIRED,
   STOP_LABEL,
   THIRD_TURN_CEILING,
   TIMED_PART,
   TUTOR_SAID,
   USAGE_LIMIT_UNKNOWN_RESET,
   WHAT_IT_CAN_SEE,
   WRITING_A_REPLY,
   YOU_SAID,
   closeHint,
   usageLimitUntil
} from "./agentCopy";
import { COMPOSER_ID, PANEL_ID, useAgent, type AgentTurn, type DegradedState } from "./AgentProvider";
import { contextLinesFor } from "./screenLines";

/* The tutor panel of docs/agent/design.md, "The panel": from 1100 px an aside beside main, from
   900 px a narrower one, and under 900 px a bottom sheet with three heights and the buttons that
   do what a drag would. It is a disclosure region, not a dialog, so nothing traps focus. Replies
   are text nodes with formulas typeset by MathText's tutor renderer, never Markdown or HTML, and
   while a reply streams a formula is held back until its closing delimiter arrives. The one live
   region is the visually hidden status line, present from the first render.

   The frame around the aside lays nothing out from 900 px. Under it, it is a column over the
   viewport whose spacer takes the height the sheet does not, which is how the sheet is half, full
   or collapsed without a viewport length in the stylesheet. */

const RESET_TIME: Intl.DateTimeFormatOptions = { hour: "numeric", minute: "2-digit" };

const RESET_DAY_AND_TIME: Intl.DateTimeFormatOptions = { weekday: "long", hour: "numeric", minute: "2-digit" };

export function resetTimeText(resetsAt: string, now: Date = new Date()) {
   const reset = new Date(resetsAt);
   const isReadable = !Number.isNaN(reset.getTime());

   if (!isReadable) {
      return null;
   }

   const isSameDay = reset.toDateString() === now.toDateString();

   return reset.toLocaleString(undefined, isSameDay ? RESET_TIME : RESET_DAY_AND_TIME);
}

export function degradedCopy(state: DegradedState) {
   switch (state.kind) {
      case "offline":
         return OFFLINE;
      case "usage_limit": {
         const time = state.resetsAt === null ? null : resetTimeText(state.resetsAt);

         return time === null ? USAGE_LIMIT_UNKNOWN_RESET : usageLimitUntil(time);
      }
      case "daily_cap":
         return DAILY_CAP;
      case "minute_cap":
         return MINUTE_CAP;
      case "sign_in":
         return SIGN_IN_EXPIRED;
      case "timed":
         return TIMED_PART;
      case "ceiling":
         return THIRD_TURN_CEILING;
      case "conversation_ceiling":
         return CONVERSATION_CEILING;
      case "unavailable":
         return OFFLINE;
      case "refused":
         return SCREEN_REFUSED;
   }
}

function paragraphsOf(text: string) {
   return text.split(/\n\s*\n/).filter((paragraph) => paragraph.trim() !== "");
}

function ReplyText(props: { text: string; isStreaming: boolean }) {
   const shown = props.isStreaming ? holdUnclosedMath(props.text).shown : props.text;

   return (
      <>
         {paragraphsOf(shown).map((paragraph, index) => (
            <p key={index}>
               <MathText text={paragraph} renderer="tutor" />
            </p>
         ))}
      </>
   );
}

function Turn(props: { turn: AgentTurn }) {
   const { turn } = props;

   if (turn.role === "student") {
      return (
         <li className="agent-turn agent-turn-student">
            <span className="visually-hidden">{YOU_SAID}</span>
            <p className="agent-student-text">{turn.text}</p>
         </li>
      );
   }

   const isStreaming = turn.state !== "done";
   const awaitsFirstText = turn.text === "" && isStreaming;

   return (
      <li className="agent-turn agent-turn-tutor">
         <span className="visually-hidden">{TUTOR_SAID}</span>

         <div className="agent-reply" aria-busy={isStreaming} data-testid="agent-reply">
            {awaitsFirstText ? <p className="agent-writing">{WRITING_A_REPLY}</p> : <ReplyText text={turn.text} isStreaming={isStreaming} />}
         </div>
      </li>
   );
}

function firstLineOf(turns: AgentTurn[]) {
   const lastReply = [...turns].reverse().find((turn) => turn.role === "agent" && turn.text !== "");

   if (lastReply === undefined) {
      return null;
   }

   const shown = holdUnclosedMath(lastReply.text).shown;

   return shown.split("\n").find((line) => line.trim() !== "") ?? null;
}

export function AgentPanel() {
   const agent = useAgent();
   const [isEntering, setIsEntering] = useState(false);
   const isOpen = agent?.isOpen ?? false;
   const isNarrow = agent?.isNarrow ?? false;

   useEffect(() => {
      const animatesIn = isOpen && isNarrow;

      if (!animatesIn) {
         return undefined;
      }

      setIsEntering(true);

      const frame = requestAnimationFrame(() => setIsEntering(false));

      return () => cancelAnimationFrame(frame);
   }, [isOpen, isNarrow]);

   if (agent === null) {
      return null;
   }

   const lines = contextLinesFor(agent.screen, agent.labels);
   const isUncheckedItem = agent.screen.kind === "session_item" && !agent.screen.submitted;
   const isCollapsed = isNarrow && agent.sheetHeight === "collapsed";
   const isFull = isNarrow && agent.sheetHeight === "full";
   const reason = agent.degraded === null ? null : degradedCopy(agent.degraded);
   const hasDraft = agent.draft.trim() !== "";
   const canSend = hasDraft && !agent.isStreaming && agent.degraded === null;
   const peek = isCollapsed ? firstLineOf(agent.turns) : null;
   const sheetClass = isNarrow ? `agent-panel agent-sheet ${TUTOR_SHEET_CLASS}` : "agent-panel";

   function closeOnEscape(event: KeyboardEvent<HTMLElement>) {
      if (event.key === "Escape") {
         event.preventDefault();
         agent?.hidePanel();
      }
   }

   function sendOnEnter(event: KeyboardEvent<HTMLTextAreaElement>) {
      const isPlainEnter = event.key === "Enter" && !event.shiftKey && !event.nativeEvent.isComposing;

      if (isPlainEnter) {
         event.preventDefault();
         agent?.send();
      }
   }

   function submit(event: FormEvent<HTMLFormElement>) {
      event.preventDefault();
      agent?.send();
   }

   return (
      <>
         <div ref={agent.frame} className="agent-frame" hidden={!agent.isOpen} data-sheet-height={isNarrow ? agent.sheetHeight : undefined}>
            <div className="agent-frame-spacer" />

            <aside
               id={PANEL_ID}
               ref={agent.panel}
               className={sheetClass}
               aria-label={PANEL_TITLE}
               hidden={!agent.isOpen}
               data-entering={isEntering ? "true" : undefined}
               data-testid="agent-panel"
               onKeyDown={closeOnEscape}
            >
               <div className="agent-header">
                  <div className="agent-title-row">
                     <h2 className="agent-title">{PANEL_TITLE}</h2>

                     <div className="agent-header-actions">
                        {isNarrow ? (
                           <>
                              <button type="button" className="text-button" onClick={() => agent.setSheetHeight("collapsed")}>
                                 {SHOW_ITEM_LABEL}
                              </button>

                              <button
                                 type="button"
                                 className="text-button"
                                 aria-pressed={isFull}
                                 onClick={() => agent.setSheetHeight(isFull ? "half" : "full")}
                              >
                                 {FULL_HEIGHT_LABEL}
                              </button>
                           </>
                        ) : null}

                        <button type="button" className="text-button agent-close" onClick={agent.closeConversation}>
                           <Icon name="close" />
                           {CLOSE_LABEL}
                        </button>
                     </div>
                  </div>

                  {peek !== null ? (
                     <p className="agent-peek" data-testid="agent-peek">
                        <MathText text={peek} renderer="tutor" />
                     </p>
                  ) : null}

                  {isCollapsed ? null : (
                     <div className="agent-context">
                        <p className="agent-context-line" data-testid="agent-can-see">
                           {lines.canSee}
                        </p>

                        {lines.cannotSee !== null ? (
                           <p className="agent-context-line" data-testid="agent-cannot-see">
                              {lines.cannotSee}
                           </p>
                        ) : null}

                        <details className="agent-disclosure">
                           <summary>{WHAT_IT_CAN_SEE}</summary>

                           <ul className="agent-fields" data-testid="agent-fields">
                              {lines.fields.map((field) => (
                                 <li key={field}>
                                    <code>{field}</code>
                                 </li>
                              ))}
                           </ul>
                        </details>
                     </div>
                  )}
               </div>

               {isCollapsed ? null : (
                  <>
                     {lines.guardrail !== null ? (
                        <p className="agent-guardrail" data-testid="agent-guardrail">
                           {lines.guardrail}
                        </p>
                     ) : null}

                     <div className="agent-conversation">
                        {agent.turns.length === 0 ? (
                           <p className="agent-empty" data-testid="agent-empty">
                              {isUncheckedItem ? EMPTY_ON_ITEM : EMPTY_ELSEWHERE}
                           </p>
                        ) : (
                           <ol className="agent-turns">
                              {agent.turns.map((turn) => (
                                 <Turn key={turn.id} turn={turn} />
                              ))}
                           </ol>
                        )}
                     </div>

                     <form className="agent-composer" onSubmit={submit}>
                        <label className="visually-hidden" htmlFor={COMPOSER_ID}>
                           {COMPOSER_LABEL}
                        </label>

                        <textarea
                           id={COMPOSER_ID}
                           ref={agent.composer}
                           className="input agent-input"
                           rows={3}
                           value={agent.draft}
                           onChange={(event) => agent.changeDraft(event.target.value)}
                           onKeyDown={sendOnEnter}
                        />

                        <div className="agent-composer-row">
                           <button type="submit" className="button-primary button-small" disabled={!canSend} aria-describedby="tutor-send-reason">
                              {SEND_LABEL}
                           </button>

                           {agent.isStreaming ? (
                              <button type="button" className="text-button" onClick={agent.stop}>
                                 {STOP_LABEL}
                              </button>
                           ) : null}

                           <p className={reason === null ? "caption agent-hint" : "agent-reason"} id="tutor-send-reason" data-testid="agent-send-reason">
                              {reason ?? closeHint(agent.isMac)}
                           </p>
                        </div>
                     </form>
                  </>
               )}
            </aside>
         </div>

         <div className="visually-hidden" role="status" data-testid="agent-status">
            {agent.announcement}
         </div>
      </>
   );
}
