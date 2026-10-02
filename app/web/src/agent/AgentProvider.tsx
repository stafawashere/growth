import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode, type RefObject } from "react";

import { closeAgentConversation } from "../api/client";
import type {
   AgentEndEvent,
   AgentErrorKind,
   AgentFigureRefusedEvent,
   AgentFigureStepEvent,
   AgentScreen,
   AgentStartEvent,
   AgentTurnOutcome,
   TutorFigureSpec,
   TutorMarksSpec
} from "../api/types";
import { latexToAccessibleText, splitInlineMath } from "../math/mathjson";
import { AgentPanel } from "./AgentPanel";
import { CONVERSATION_CEILING, FIGURE_REFUSED, MARKS_REFUSED, REPLY_STOPPED, THIRD_TURN_CEILING, WITHHELD, figureAnnouncement, marksAnnouncement } from "./agentCopy";
import { createReplyPacer, type ReplyPacer } from "./figurePacing";
import { PageMarks, parseTutorMarks } from "./PageMarks";
import { contextLinesFor, type ScreenLabels } from "./screenLines";
import { parseTutorFigure } from "./TutorFigure";
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

/* A reply's figure (docs/agent/drawing-design.md, "States and copy"): announced by its opening
   fence, drawn at the length of the reply text shown when it arrived, or refused with one line in
   its place. */
export type ReplyFigure =
   | { state: "pending" }
   | { state: "shown"; spec: TutorFigureSpec; offset: number; revealed: number }
   | { state: "refused"; offset: number; copy: string };

/* A reply's marks on the page (docs/agent/drawing-design.md, "Marks on the page"), kept with the
   key of the screen the reply was asked on, or refused with one line under the reply. */
export type ReplyMarks = { state: "shown"; spec: TutorMarksSpec; revealed: number; screenKey: string } | { state: "refused"; copy: string };

export interface AgentTurn {
   id: string;
   role: "student" | "agent";
   text: string;
   state: "waiting" | "streaming" | "done";
   outcome: AgentTurnOutcome | null;
   figure?: ReplyFigure;
   marks?: ReplyMarks;
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
   showAll: (turnId: string) => void;
   marksTurnId: string | null;
   clearMarks: () => void;
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

/* The screen marks belong to: its kind and the ids that name what it shows, so an item keeps its
   marks from before it was checked to after, and a lesson's marks are its section's. */
export function marksScreenKey(screen: AgentScreen) {
   switch (screen.kind) {
      case "session_item":
         return JSON.stringify([screen.kind, screen.session_id, screen.item_id]);
      case "session_lesson":
         return JSON.stringify([screen.kind, screen.session_id, screen.lesson_id, screen.version, screen.section_id]);
      case "lesson":
         return JSON.stringify([screen.kind, screen.lesson_id, screen.version, screen.section_id]);
      case "progress":
         return JSON.stringify([screen.kind, screen.tab, screen.skill_id ?? null]);
      case "assessments":
         return JSON.stringify([screen.kind, screen.format]);
      case "settings":
         return JSON.stringify([screen.kind, screen.tab]);
      case "other":
         return JSON.stringify([screen.kind, screen.view]);
      default:
         return JSON.stringify([screen.kind]);
   }
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

function withFigureAt(turn: AgentTurn, spec: TutorFigureSpec | null): AgentTurn {
   const offset = turn.text.length;
   const figure: ReplyFigure = spec === null ? { state: "refused", offset, copy: FIGURE_REFUSED } : { state: "shown", spec, offset, revealed: 0 };

   return { ...turn, figure };
}

function withoutReply(marksByScreen: Record<string, string>, replyId: string) {
   return Object.fromEntries(Object.entries(marksByScreen).filter(([, turnId]) => turnId !== replyId));
}

function withMarksStepRevealed(turn: AgentTurn, stepIndex: number): AgentTurn {
   const marks = turn.marks;

   if (marks?.state !== "shown") {
      return turn;
   }

   return { ...turn, marks: { ...marks, revealed: Math.max(marks.revealed, stepIndex + 1) } };
}

function withStepRevealed(turn: AgentTurn, stepIndex: number): AgentTurn {
   const figure = turn.figure;

   if (figure?.state !== "shown") {
      return turn;
   }

   return { ...turn, figure: { ...figure, revealed: Math.max(figure.revealed, stepIndex + 1) } };
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

/* A usage limit whose reset time has already passed when it arrives (a clock skew, or a reset
   stamped in the past) is not cleared by a timer, which would hide the copy at once. It stays
   until the student edits or sends again. */
export function isLapsedUsageLimit(state: DegradedState | null, now: number = Date.now()) {
   const isUsageLimit = state !== null && state.kind === "usage_limit" && state.resetsAt !== null;

   if (!isUsageLimit) {
      return false;
   }

   const resetMoment = Date.parse(state.resetsAt as string);

   return Number.isFinite(resetMoment) && resetMoment <= now;
}

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
   const [isPacing, setIsPacing] = useState(false);
   const [marksByScreen, setMarksByScreen] = useState<Record<string, string>>({});
   const frame = useRef<HTMLDivElement>(null);
   const isNarrow = useSheetLayout(frame, enabled);
   const stream = useAgentStream();
   const pacing = useRef<{ replyId: string; pacer: ReplyPacer } | null>(null);
   const isReplying = stream.isStreaming || isPacing;

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
   const currentMarksKey = marksScreenKey(screen);
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
      const isInFuture = Number.isFinite(wait) && wait > 0;

      if (!isInFuture) {
         return undefined;
      }

      const timer = setTimeout(() => setDegraded(null), wait);

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
      setDegraded((current) => {
         const clearsOnEdit = current !== null && CLEARS_ON_EDIT.includes(current.kind);

         return clearsOnEdit || isLapsedUsageLimit(current) ? null : current;
      });
   }, []);

   function updateTurn(id: string, change: (turn: AgentTurn) => AgentTurn) {
      setTurns((current) => current.map((turn) => (turn.id === id ? change(turn) : turn)));
   }

   useEffect(() => {
      return () => pacing.current?.pacer.dispose();
   }, []);

   const send = useCallback(() => {
      const message = draft.trim();
      const isDegraded = degraded !== null && !isLapsedUsageLimit(degraded);
      const isBlocked = message === "" || isReplying || isDegraded || isTimed;

      if (isBlocked) {
         return;
      }

      const sentOn = screen;
      const sentOnKey = currentKey;
      const sentOnMarksKey = currentMarksKey;
      const studentTurn: AgentTurn = { id: localTurnId("student"), role: "student", text: message, state: "done", outcome: null };
      const replyId = localTurnId("agent");
      const reply: AgentTurn = { id: replyId, role: "agent", text: "", state: "waiting", outcome: null };
      let receivedText = "";
      let drawnFigure: TutorFigureSpec | null = null;
      let drawnMarks: TutorMarksSpec | null = null;
      let latestFigureGate = -1;
      let latestMarksGate = -1;
      const gates: Array<() => void> = [];

      /* While a figure or the marks are building, each of their steps is a gate: the step and the
         text after it wait until the words before it could have been read (figurePacing.ts). The end
         is applied, and the reply announced, once everything received has been shown. */
      const pacer = createReplyPacer({
         showText: (delta) => updateTurn(replyId, (turn) => ({ ...turn, text: turn.text + delta, state: "streaming" })),
         openGate: (gate) => gates[gate]?.(),
         onBusyChange: setIsPacing
      });

      function pushGate(open: () => void) {
         gates.push(open);
         pacer.pushGate(gates.length - 1);
      }

      pacing.current?.pacer.dispose();
      pacing.current = { replyId, pacer };

      setTurns((current) => [...current, studentTurn, reply]);
      setDraft("");
      setAnnouncement("");
      setDegraded(null);

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
               pacer.pushText(delta);
            },
            onFigurePending: () => {
               pacer.pushAction(() => updateTurn(replyId, (turn) => ({ ...turn, figure: { state: "pending" }, state: "streaming" })));
            },
            onFigure: (spec: unknown) => {
               const checked = parseTutorFigure(spec);

               drawnFigure = checked;
               pacer.pushAction(() => updateTurn(replyId, (turn) => ({ ...withFigureAt(turn, checked), state: "streaming" })));
            },
            onMarks: (spec: unknown) => {
               const checked = parseTutorMarks(spec);

               drawnMarks = checked;
               pacer.pushAction(() => {
                  if (checked === null) {
                     updateTurn(replyId, (turn) => ({ ...turn, marks: { state: "refused", copy: MARKS_REFUSED } }));
                     return;
                  }

                  updateTurn(replyId, (turn) => ({ ...turn, marks: { state: "shown", spec: checked, revealed: 0, screenKey: sentOnMarksKey }, state: "streaming" }));
                  setMarksByScreen((current) => ({ ...current, [sentOnMarksKey]: replyId }));
               });
            },
            onFigureStep: (event: AgentFigureStepEvent) => {
               const figure = drawnFigure;
               const marks = drawnMarks;
               const isFigureStep = figure !== null && event.figure === figure.id;
               const isMarksStep = marks !== null && event.figure === marks.id;
               const figureStep = isFigureStep ? figure.steps.findIndex((step) => step.id === event.step) : -1;
               const marksStep = isMarksStep ? marks.steps.findIndex((step) => step.id === event.step) : -1;
               const opensFigureStep = figureStep > latestFigureGate;
               const opensMarksStep = marksStep > latestMarksGate;

               if (opensFigureStep) {
                  latestFigureGate = figureStep;
                  pushGate(() => updateTurn(replyId, (turn) => withStepRevealed(turn, figureStep)));
               } else if (opensMarksStep) {
                  latestMarksGate = marksStep;
                  pushGate(() => updateTurn(replyId, (turn) => withMarksStepRevealed(turn, marksStep)));
               }
            },
            onFigureRefused: (event: AgentFigureRefusedEvent) => {
               const isMarks = event.part === "marks";
               const fallback = isMarks ? MARKS_REFUSED : FIGURE_REFUSED;
               const copy = event.copy.trim() === "" ? fallback : event.copy;

               pacer.pushAction(() =>
                  updateTurn(replyId, (turn) =>
                     isMarks ? { ...turn, marks: { state: "refused", copy } } : { ...turn, figure: { state: "refused", offset: turn.text.length, copy }, state: "streaming" }
                  )
               );
            },
            onEnd: (event: AgentEndEvent) => {
               pacer.pushAction(() => {
                  const isWithheld = event.outcome === "withheld";
                  const finalText = isWithheld ? WITHHELD : receivedText;
                  const reachedCeiling = isUncheckedItem(currentScreen.current) && event.turns_on_item >= PER_ITEM_TURN_CEILING;
                  const figure = isWithheld ? null : drawnFigure;
                  const marks = isWithheld ? null : drawnMarks;
                  const figureClause = figure === null ? "" : ` ${figureAnnouncement(figure.title, figure.description)}`;
                  const marksClause = marks === null ? "" : ` ${marksAnnouncement(marks.description)}`;

                  updateTurn(replyId, (turn) => ({
                     ...turn,
                     text: finalText,
                     state: "done",
                     outcome: event.outcome,
                     figure: isWithheld ? undefined : turn.figure,
                     marks: isWithheld ? undefined : turn.marks
                  }));
                  setAnnouncement(`${spokenReply(finalText)}${figureClause}${marksClause}`.trim());

                  if (isWithheld) {
                     setMarksByScreen((current) => withoutReply(current, replyId));
                  }

                  if (reachedCeiling) {
                     setDegraded({ kind: "ceiling", resetsAt: null, copy: THIRD_TURN_CEILING, screenKey: sentOnKey });
                  }
               });
            },
            onFailure: (failure: TurnFailure) => {
               pacer.showEverything();

               const hasReply = receivedText !== "" || drawnFigure !== null || drawnMarks !== null;
               const resetsAt = failure.kind === "offline" ? null : failure.resetsAt;
               const copy = failure.kind === "offline" ? null : failure.copy;
               const isConversationCeiling = failure.kind === "ceiling" && copy === CONVERSATION_CEILING;
               const kind: DegradedKind = isConversationCeiling ? "conversation_ceiling" : failure.kind;

               if (hasReply) {
                  updateTurn(replyId, (turn) => ({ ...turn, state: "done", outcome: "incomplete" }));
               } else {
                  giveBackDraft();
               }

               setDegraded({ kind, resetsAt, copy, screenKey: sentOnKey });
            },
            onStopped: () => {
               pacer.showEverything();
               updateTurn(replyId, (turn) => ({ ...turn, state: "done", outcome: "stopped" }));
               setAnnouncement(REPLY_STOPPED);
            }
         }
      );
   }, [draft, stream, degraded, isTimed, screen, currentKey, currentMarksKey, conversationId, isReplying]);

   const clearMarks = useCallback(() => {
      setMarksByScreen((current) => {
         const next = { ...current };

         delete next[currentMarksKey];

         return next;
      });
   }, [currentMarksKey]);

   const showAll = useCallback((turnId: string) => {
      const isPacedReply = pacing.current !== null && pacing.current.replyId === turnId;

      if (isPacedReply) {
         pacing.current!.pacer.showEverything();
      }
   }, []);

   /* Stop opens every waiting step at once. While the reply still streams it also ends the request,
      and the turn ends stopped; once the server has ended the reply, what it sent is shown and the
      turn ends as the server said. */
   const stop = useCallback(() => {
      pacing.current?.pacer.showEverything();
      stream.stop();
   }, [stream]);

   const closeConversation = useCallback(() => {
      const closing = conversationId;

      pacing.current?.pacer.dispose();
      pacing.current = null;
      stream.stop();
      setTurns([]);
      setMarksByScreen({});
      setConversationId(null);
      setDegraded(null);
      hidePanel();

      if (closing !== null) {
         closeAgentConversation(closing).catch(() => undefined);
      }
   }, [conversationId, stream, hidePanel]);

   /* The marks of the screen the student is on, drawn over the page between the page and the panel.
      Keyed by the screen and the reply, so returning to a screen draws its marks again from scratch,
      finished and without motion. */
   const marksTurnId = marksByScreen[currentMarksKey] ?? null;
   const marksTurn = marksTurnId === null ? undefined : turns.find((turn) => turn.id === marksTurnId);
   const pageMarks = marksTurn?.marks?.state === "shown" ? marksTurn.marks : null;

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
      isStreaming: isReplying,
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
      stop,
      showAll,
      marksTurnId,
      clearMarks,
      setSheetHeight
   };

   return (
      <ScreenRegistryContext.Provider value={registry}>
         <AgentContext.Provider value={enabled ? value : null}>
            {children}

            {enabled && pageMarks !== null ? <PageMarks key={`${currentMarksKey} ${marksTurnId}`} spec={pageMarks.spec} revealed={pageMarks.revealed} /> : null}

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
