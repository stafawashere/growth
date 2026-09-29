import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode, type RefObject } from "react";

import { closeAgentConversation } from "../api/client";
import type { AgentEndEvent, AgentErrorKind, AgentScreen, AgentStartEvent, AgentTurnOutcome } from "../api/types";
import { latexToAccessibleText, splitInlineMath } from "../math/mathjson";
import { AgentPanel } from "./AgentPanel";
import { CONVERSATION_CEILING, REPLY_STOPPED, THIRD_TURN_CEILING, WITHHELD } from "./agentCopy";
import { contextLinesFor, type ScreenLabels } from "./screenLines";
import { useAgentStream, type TurnFailure } from "./useAgentStream";

/* The live tutor's client state (docs/agent/architecture.md, "The panel and the settings views"):
   whether the panel is open, the screen every route describes through useAgentScreen, the
   conversation and its turns, the one streaming turn, and the Ctrl+/ or Cmd+/ shortcut
   (docs/agent/design.md, "The entry point"). The provider renders the panel beside its children,
   so the aside is a sibling of main.

   Each route claims the screen with useAgentScreen. A route drawn inside another claims after it
   (its first render comes later), and a claim that changes goes to the top, so the screen is the
   most specific one on the page. A timed part outranks everything, because the Ask button must
   be disabled whatever else is claimed. */

export const PANEL_ID = "tutor-panel";

export const COMPOSER_ID = "tutor-composer";

export const PER_ITEM_TURN_CEILING = 3;

export const MAIN_ID = "main";

export type SheetHeight = "collapsed" | "half" | "full";

export interface AgentTurn {
   id: string;
   role: "student" | "agent";
   text: string;
   state: "waiting" | "streaming" | "done";
   outcome: AgentTurnOutcome | null;
}

export type DegradedKind = AgentErrorKind | "offline" | "conversation_ceiling";

export interface DegradedState {
   kind: DegradedKind;
   resetsAt: string | null;
   copy: string | null;
   screenKey: string;
}

interface ScreenClaim {
   screen: AgentScreen;
   labels: ScreenLabels;
   order: number;
}

interface ScreenRegistry {
   claim: (token: symbol, screen: AgentScreen, labels: ScreenLabels, order: number) => void;
   release: (token: symbol) => void;
}

export interface AgentContextValue {
   isOpen: boolean;
   isMac: boolean;
   isNarrow: boolean;
   isTimed: boolean;
   screen: AgentScreen;
   labels: ScreenLabels;
   draft: string;
   turns: AgentTurn[];
   conversationId: string | null;
   isStreaming: boolean;
   degraded: DegradedState | null;
   announcement: string;
   sheetHeight: SheetHeight;
   askButton: RefObject<HTMLButtonElement>;
   frame: RefObject<HTMLDivElement>;
   composer: RefObject<HTMLTextAreaElement>;
   panel: RefObject<HTMLElement>;
   openPanel: () => void;
   togglePanel: () => void;
   hidePanel: () => void;
   closeConversation: () => void;
   changeDraft: (text: string) => void;
   send: () => void;
   stop: () => void;
   setSheetHeight: (height: SheetHeight) => void;
}

const AgentContext = createContext<AgentContextValue | null>(null);

const ScreenRegistryContext = createContext<ScreenRegistry | null>(null);

const FALLBACK_SCREEN: AgentScreen = { kind: "other", view: "app" };

let claimCounter = 0;

function nextClaimOrder() {
   claimCounter += 1;

   return claimCounter;
}

let localTurnCounter = 0;

function localTurnId(role: AgentTurn["role"]) {
   localTurnCounter += 1;

   return `local-${role}-${localTurnCounter}`;
}

/* schemas/agent/screen.schema.json requires an attempt id on every practice item, but the
   attempts row is written only when the answer is submitted. Until then the item carries an id
   the client mints in the same form, which app/agent/turn.py looks up, finds no row for, and
   leaves alone; from submission on, the real attempt's id replaces it. */
export function unsubmittedAttemptId() {
   const bytes = new Uint8Array(16);

   crypto.getRandomValues(bytes);

   return `ATT-${Array.from(bytes, (byte) => byte.toString(16).padStart(2, "0")).join("")}`;
}

export function detectMac() {
   const platform = typeof navigator === "undefined" ? "" : `${navigator.platform} ${navigator.userAgent}`;

   return /Mac|iPhone|iPad|iPod/.test(platform);
}

function isTimedScreen(screen: AgentScreen) {
   return screen.kind === "assessments" && screen.timed === true;
}

export function screenKey(screen: AgentScreen) {
   return JSON.stringify(screen);
}

function effectiveClaim(claims: Map<symbol, ScreenClaim>): ScreenClaim | null {
   const all = Array.from(claims.values());
   const timed = all.find((claim) => isTimedScreen(claim.screen));

   if (timed !== undefined) {
      return timed;
   }

   return all.reduce<ScreenClaim | null>((best, claim) => (best === null || claim.order > best.order ? claim : best), null);
}

function isUncheckedItem(screen: AgentScreen) {
   return screen.kind === "session_item" && !screen.submitted;
}

/* The status region reads the reply as words: each formula is given as its ASCII reading, the
   same fallback MathText shows when KaTeX refuses one. */
export function spokenReply(text: string) {
   return splitInlineMath(text)
      .map((segment) => (segment.kind === "text" ? segment.text : latexToAccessibleText(segment.latex)))
      .join("")
      .trim();
}

/* Whether the panel is the phone sheet is read from the stylesheet rather than restated here:
   under 900 px app.css fixes the panel's frame over the viewport, and that is the one place the
   breakpoint lives. It is read again whenever the window is resized. */
function useSheetLayout(frame: RefObject<HTMLElement>, isMounted: boolean) {
   const [isNarrow, setIsNarrow] = useState(false);

   useEffect(() => {
      function follow() {
         const element = frame.current;
         const isSheet = element !== null && getComputedStyle(element).position === "fixed";

         setIsNarrow(isSheet);
      }

      follow();
      window.addEventListener("resize", follow);

      return () => window.removeEventListener("resize", follow);
   }, [frame, isMounted]);

   return isNarrow;
}

/* Clearing rules for a degraded state. No connection and the minute cap clear when the student
   edits what they typed, so Send comes back for the next try; a timed or ceiling refusal belongs to
   the screen it was given on; the rest hold until the conversation is closed. */
const CLEARS_ON_EDIT: ReadonlyArray<DegradedKind> = ["offline", "minute_cap", "refused"];

const CLEARS_ON_SCREEN_CHANGE: ReadonlyArray<DegradedKind> = ["ceiling", "timed"];

export interface AgentProviderProps {
   enabled: boolean;
   children: ReactNode;
}

export function AgentProvider({ enabled, children }: AgentProviderProps) {
   const [claims, setClaims] = useState<Map<symbol, ScreenClaim>>(() => new Map());
   const [isOpen, setIsOpen] = useState(false);
   const [draft, setDraft] = useState("");
   const [turns, setTurns] = useState<AgentTurn[]>([]);
   const [conversationId, setConversationId] = useState<string | null>(null);
   const [degraded, setDegraded] = useState<DegradedState | null>(null);
   const [announcement, setAnnouncement] = useState("");
   const [sheetHeight, setSheetHeight] = useState<SheetHeight>("half");
   const [focusRequest, setFocusRequest] = useState(0);
   const [isMac] = useState(detectMac);
   const frame = useRef<HTMLDivElement>(null);
   const isNarrow = useSheetLayout(frame, enabled);
   const stream = useAgentStream();

   const askButton = useRef<HTMLButtonElement>(null);
   const composer = useRef<HTMLTextAreaElement>(null);
   const panel = useRef<HTMLElement>(null);
   const returnTarget = useRef<HTMLElement | null>(null);
   const shownLine = useRef<string | null>(null);

   const registry = useMemo<ScreenRegistry>(
      () => ({
         claim: (token, screen, labels, order) =>
            setClaims((current) => {
               const next = new Map(current);

               next.set(token, { screen, labels, order });

               return next;
            }),
         release: (token) =>
            setClaims((current) => {
               if (!current.has(token)) {
                  return current;
               }

               const next = new Map(current);

               next.delete(token);

               return next;
            })
      }),
      []
   );

   const claim = effectiveClaim(claims);
   const screen = claim?.screen ?? FALLBACK_SCREEN;
   const labels = claim?.labels ?? {};
   const isTimed = isTimedScreen(screen);
   const currentKey = screenKey(screen);
   const currentScreen = useRef(screen);

   currentScreen.current = screen;

   const rememberReturnTarget = useCallback(() => {
      const active = document.activeElement as HTMLElement | null;
      const isInPanel = active !== null && panel.current?.contains(active) === true;
      const isPageBody = active === null || active === document.body;

      if (!isInPanel) {
         returnTarget.current = isPageBody ? null : active;
      }
   }, []);

   const openPanel = useCallback(() => {
      if (isTimed) {
         return;
      }

      rememberReturnTarget();
      setIsOpen(true);
      setSheetHeight("half");
      setFocusRequest((request) => request + 1);
   }, [isTimed, rememberReturnTarget]);

   const hidePanel = useCallback(() => {
      const target = returnTarget.current;
      const canReturn = target !== null && target.isConnected;

      setIsOpen(false);
      returnTarget.current = null;

      if (canReturn) {
         target.focus();
      } else {
         askButton.current?.focus();
      }
   }, []);

   const togglePanel = useCallback(() => {
      if (isOpen) {
         hidePanel();
      } else {
         openPanel();
      }
   }, [isOpen, hidePanel, openPanel]);

   useEffect(() => {
      const hasRequest = focusRequest > 0;

      if (hasRequest && isOpen) {
         composer.current?.focus();
      }
   }, [focusRequest, isOpen]);

   useEffect(() => {
      if (!enabled) {
         return undefined;
      }

      function onShortcut(event: KeyboardEvent) {
         const hasPlatformModifier = isMac ? event.metaKey : event.ctrlKey;
         const isSlash = event.key === "/" || event.code === "Slash";
         const isShortcut = hasPlatformModifier && isSlash && !event.altKey;

         if (!isShortcut) {
            return;
         }

         event.preventDefault();
         event.stopPropagation();

         if (isTimed) {
            return;
         }

         const active = document.activeElement;
         const focusIsInPanel = active !== null && panel.current?.contains(active) === true;

         if (!isOpen) {
            openPanel();
         } else if (focusIsInPanel) {
            hidePanel();
         } else {
            rememberReturnTarget();
            setSheetHeight((height) => (height === "collapsed" ? "half" : height));
            setFocusRequest((request) => request + 1);
         }
      }

      window.addEventListener("keydown", onShortcut, true);

      return () => window.removeEventListener("keydown", onShortcut, true);
   }, [enabled, isMac, isTimed, isOpen, openPanel, hidePanel, rememberReturnTarget]);

   useEffect(() => {
      if (isTimed && isOpen) {
         stream.stop();
         setIsOpen(false);
      }
   }, [isTimed, isOpen, stream]);

   useEffect(() => {
      setDegraded((current) => {
         const belongsToScreen = current !== null && CLEARS_ON_SCREEN_CHANGE.includes(current.kind);
         const screenChanged = current !== null && current.screenKey !== currentKey;

         return belongsToScreen && screenChanged ? null : current;
      });
   }, [currentKey]);

   const lines = contextLinesFor(screen, labels);

   useEffect(() => {
      const previous = shownLine.current;
      const changedWhileOpen = isOpen && previous !== null && previous !== lines.canSee;

      if (changedWhileOpen) {
         setAnnouncement(lines.canSee);
      }

      shownLine.current = isOpen ? lines.canSee : null;
   }, [isOpen, lines.canSee]);

   useEffect(() => {
      const isUsageLimit = degraded !== null && degraded.kind === "usage_limit" && degraded.resetsAt !== null;

      if (!isUsageLimit) {
         return undefined;
      }

      const wait = Date.parse(degraded.resetsAt as string) - Date.now();
      const isReadable = Number.isFinite(wait);

      if (!isReadable) {
         return undefined;
      }

      const timer = setTimeout(() => setDegraded(null), Math.max(0, wait));

      return () => clearTimeout(timer);
   }, [degraded]);

   useEffect(() => {
      function backOnline() {
         setDegraded((current) => (current !== null && current.kind === "offline" ? null : current));
      }

      window.addEventListener("online", backOnline);

      return () => window.removeEventListener("online", backOnline);
   }, []);

   /* Under 900 px the sheet sits over the page, so main gets bottom padding equal to its height and
      every control on the item can scroll above it (design.md, The panel). The height is measured,
      because it follows the viewport and the sheet's own state, so it is geometry rather than a
      design value and is set on main directly. */
   const showsSheet = enabled && isOpen && isNarrow;

   useEffect(() => {
      const main = document.getElementById(MAIN_ID);
      const sheet = panel.current;
      const canMeasure = showsSheet && main !== null && sheet !== null && typeof ResizeObserver === "function";

      if (!canMeasure) {
         return undefined;
      }

      const observer = new ResizeObserver(() => {
         main.style.paddingBottom = `${Math.ceil(sheet.getBoundingClientRect().height)}px`;
      });

      observer.observe(sheet);

      return () => {
         observer.disconnect();
         main.style.removeProperty("padding-bottom");
      };
   }, [showsSheet]);

   useEffect(() => {
      const root = document.documentElement;
      const showsAside = enabled && isOpen && !isNarrow;

      root.toggleAttribute("data-agent-panel", showsAside);

      return () => {
         root.toggleAttribute("data-agent-panel", false);
      };
   }, [enabled, isOpen, isNarrow]);

   const changeDraft = useCallback((text: string) => {
      setDraft(text);
      setDegraded((current) => (current !== null && CLEARS_ON_EDIT.includes(current.kind) ? null : current));
   }, []);

   function updateTurn(id: string, change: (turn: AgentTurn) => AgentTurn) {
      setTurns((current) => current.map((turn) => (turn.id === id ? change(turn) : turn)));
   }

   const send = useCallback(() => {
      const message = draft.trim();
      const isBlocked = message === "" || stream.isStreaming || degraded !== null || isTimed;

      if (isBlocked) {
         return;
      }

      const sentOn = screen;
      const sentOnKey = currentKey;
      const studentTurn: AgentTurn = { id: localTurnId("student"), role: "student", text: message, state: "done", outcome: null };
      const replyId = localTurnId("agent");
      const reply: AgentTurn = { id: replyId, role: "agent", text: "", state: "waiting", outcome: null };
      let receivedText = "";

      setTurns((current) => [...current, studentTurn, reply]);
      setDraft("");
      setAnnouncement("");

      function giveBackDraft() {
         setTurns((current) => current.filter((turn) => turn.id !== studentTurn.id && turn.id !== replyId));
         setDraft((current) => (current === "" ? message : current));
      }

      void stream.start(
         { conversation_id: conversationId, screen: sentOn, message },
         {
            onStart: (event: AgentStartEvent) => {
               setConversationId(event.conversation_id);
            },
            onText: (delta: string) => {
               receivedText += delta;
               updateTurn(replyId, (turn) => ({ ...turn, text: turn.text + delta, state: "streaming" }));
            },
            onEnd: (event: AgentEndEvent) => {
               const isWithheld = event.outcome === "withheld";
               const finalText = isWithheld ? WITHHELD : receivedText;
               const reachedCeiling = isUncheckedItem(currentScreen.current) && event.turns_on_item >= PER_ITEM_TURN_CEILING;

               updateTurn(replyId, (turn) => ({ ...turn, text: finalText, state: "done", outcome: event.outcome }));
               setAnnouncement(spokenReply(finalText));

               if (reachedCeiling) {
                  setDegraded({ kind: "ceiling", resetsAt: null, copy: THIRD_TURN_CEILING, screenKey: sentOnKey });
               }
            },
            onFailure: (failure: TurnFailure) => {
               const hasText = receivedText !== "";
               const resetsAt = failure.kind === "offline" ? null : failure.resetsAt;
               const copy = failure.kind === "offline" ? null : failure.copy;
               const isConversationCeiling = failure.kind === "ceiling" && copy === CONVERSATION_CEILING;
               const kind: DegradedKind = isConversationCeiling ? "conversation_ceiling" : failure.kind;

               if (hasText) {
                  updateTurn(replyId, (turn) => ({ ...turn, state: "done", outcome: "incomplete" }));
               } else {
                  giveBackDraft();
               }

               setDegraded({ kind, resetsAt, copy, screenKey: sentOnKey });
            },
            onStopped: () => {
               updateTurn(replyId, (turn) => ({ ...turn, state: "done", outcome: "stopped" }));
               setAnnouncement(REPLY_STOPPED);
            }
         }
      );
   }, [draft, stream, degraded, isTimed, screen, currentKey, conversationId]);

   const closeConversation = useCallback(() => {
      const closing = conversationId;

      stream.stop();
      setTurns([]);
      setConversationId(null);
      setDegraded(null);
      hidePanel();

      if (closing !== null) {
         closeAgentConversation(closing).catch(() => undefined);
      }
   }, [conversationId, stream, hidePanel]);

   const value: AgentContextValue = {
      isOpen: enabled && isOpen,
      isMac,
      isNarrow,
      isTimed,
      screen,
      labels,
      draft,
      turns,
      conversationId,
      isStreaming: stream.isStreaming,
      degraded,
      announcement,
      sheetHeight,
      askButton,
      frame,
      composer,
      panel,
      openPanel,
      togglePanel,
      hidePanel,
      closeConversation,
      changeDraft,
      send,
      stop: stream.stop,
      setSheetHeight
   };

   return (
      <ScreenRegistryContext.Provider value={registry}>
         <AgentContext.Provider value={enabled ? value : null}>
            {children}

            {enabled ? <AgentPanel /> : null}
         </AgentContext.Provider>
      </ScreenRegistryContext.Provider>
   );
}

/* null outside a signed-in shell, so a screen rendered on its own in a test draws no tutor. */
export function useAgent() {
   return useContext(AgentContext);
}

/* Every route calls this with the screen it shows, or null when it has nothing to say. It never
   takes the draft answer, the selected option or a key; labels are names shown in the panel's
   context line and are never sent. Outside the provider it does nothing. */
export function useAgentScreen(screen: AgentScreen | null, labels: ScreenLabels = {}) {
   const registry = useContext(ScreenRegistryContext);
   const [token] = useState(() => Symbol("agent-screen"));
   const [firstOrder] = useState(nextClaimOrder);
   const hasClaimed = useRef(false);
   const claimKey = screen === null ? null : JSON.stringify([screen, labels]);

   useEffect(() => {
      if (registry === null) {
         return;
      }

      if (claimKey === null) {
         registry.release(token);

         return;
      }

      const [claimedScreen, claimedLabels] = JSON.parse(claimKey) as [AgentScreen, ScreenLabels];
      const order = hasClaimed.current ? nextClaimOrder() : firstOrder;

      hasClaimed.current = true;
      registry.claim(token, claimedScreen, claimedLabels, order);
   }, [registry, token, claimKey, firstOrder]);

   useEffect(() => {
      return () => registry?.release(token);
   }, [registry, token]);
}
