import { useCallback, useEffect, useId, useLayoutEffect, useRef, useState, type KeyboardEvent, type PointerEvent, type RefObject } from "react";

import type { TutorFigureSpec } from "../api/types";
import {
   ART_BOARD_TITLE,
   CHANGE_SIZE_LABEL,
   CLOSE_BOARD_LABEL,
   CLOSE_LABEL,
   MINIMIZE_BOARD_LABEL,
   MINIMIZE_LABEL,
   MOVE_BOARD_HINT,
   MOVE_BOARD_LABEL,
   MOVE_LABEL,
   MOVE_TO_NEXT_CORNER_LABEL,
   NEXT_FIGURE_LABEL,
   NEXT_STEP_LABEL,
   PREVIOUS_FIGURE_LABEL,
   PREVIOUS_STEP_LABEL,
   RESIZE_BOARD_HINT,
   RESIZE_BOARD_LABEL,
   RESTORE_BOARD_LABEL,
   RESTORE_LABEL,
   SHORTER_LABEL,
   SIZE_LABEL,
   TALLER_LABEL,
   boardFigureCount,
   minimizedBoard
} from "./agentCopy";
import { TutorFigure } from "./TutorFigure";

/* The tutor's art board (docs/agent/drawing-design.md, "The art board"): a window over the page
   that holds the conversation's figures, one at a time, each built there step by step as the
   reply's words arrive. It is not a dialog and never takes focus on its own; the provider renders
   it after the page and the tutor panel, so it paints above the page and comes after the panel in
   the tab order.

   From 900 px it floats. The title bar drags it and the corner grip resizes it, and both answer
   the arrow keys when focused. It keeps to the viewport below the top bar and, while the tutor
   panel is open beside the page, to the left of the panel, so it never covers the composer. Under
   900 px it docks full width under the top bar with a height of its own, and reports where it ends
   so the tutor sheet starts below it. For anyone who cannot drag, Move and Size do the same with
   one click each: Move goes round the corners of the area and Size round three sizes.

   Every place and size is measured from the page and set on the element, as PageMarks does, and
   what the student chose is kept in this browser's storage. */

export interface BoardFigure {
   turnId: string;
   spec: TutorFigureSpec;
   revealed: number;
   finished: boolean;
}

export type BoardMode = "open" | "minimized";

export interface ArtBoardProps {
   figures: BoardFigure[];
   /* The index of the figure shown, among figures. */
   current: number;
   mode: BoardMode;
   /* Under 900 px, as the tutor panel's sheet layout reports it. */
   isNarrow: boolean;
   isPanelOpen: boolean;
   panel: RefObject<HTMLElement>;
   /* The student asked to see a figure, so focus moves to it once it is drawn. */
   focusFigure: boolean;
   onFigureFocused: () => void;
   onChoose: (turnId: string) => void;
   onMinimize: () => void;
   onRestore: () => void;
   onClose: () => void;
   onShowAll: (turnId: string) => void;
   /* Where the docked board ends, in viewport pixels, or null when it is not docked. */
   onDock?: (bottom: number | null) => void;
}

export interface BoardPlacement {
   left: number | null;
   top: number | null;
   width: number | null;
   height: number | null;
   minimized: boolean;
   tall: boolean;
}

export interface BoardArea {
   left: number;
   top: number;
   right: number;
   bottom: number;
}

export interface BoardFrame {
   left: number;
   top: number;
   width: number;
   height: number;
}

export const BOARD_PLACEMENT_KEY = "growth-art-board";

export const DEFAULT_PLACEMENT: BoardPlacement = { left: null, top: null, width: null, height: null, minimized: false, tall: false };

export const MINIMUM_WIDTH = 280;

export const MINIMUM_HEIGHT = 240;

export const KEY_STEP = 16;

export const LARGE_KEY_STEP = 64;

/* A figure is drawn at most 384 px wide in its own frame, so the board starts wide enough for that
   with its padding, and tall enough for the figure, its step line and its controls. */
export const DEFAULT_WIDTH = 416;

export const DEFAULT_HEIGHT = 560;

/* The space the default place leaves between the board and the top bar or the panel. */
export const EDGE_GAP = 16;

/* Docked, the board takes this share of the height between the top bar and the bottom of the
   screen, shorter or taller as the student chose. */
export const SHORT_SHARE = 0.4;

export const TALL_SHARE = 0.65;

const ARROW_DIRECTIONS: Record<string, [number, number]> = {
   ArrowLeft: [-1, 0],
   ArrowRight: [1, 0],
   ArrowUp: [0, -1],
   ArrowDown: [0, 1]
};

function isLength(value: unknown) {
   return value === null || (typeof value === "number" && Number.isFinite(value));
}

/* The board's place lives in this browser's storage, which can be missing, full or refused
   outright, so every read and write is guarded and a place that cannot be read is the default. */
export function readBoardPlacement(): BoardPlacement {
   try {
      const stored: unknown = JSON.parse(window.localStorage.getItem(BOARD_PLACEMENT_KEY) ?? "null");
      const isRecord = typeof stored === "object" && stored !== null;

      if (!isRecord) {
         return DEFAULT_PLACEMENT;
      }

      const record = stored as Record<string, unknown>;
      const hasLengths = [record.left, record.top, record.width, record.height].every(isLength);
      const hasFlags = typeof record.minimized === "boolean" && typeof record.tall === "boolean";

      if (!hasLengths || !hasFlags) {
         return DEFAULT_PLACEMENT;
      }

      return {
         left: record.left as number | null,
         top: record.top as number | null,
         width: record.width as number | null,
         height: record.height as number | null,
         minimized: record.minimized as boolean,
         tall: record.tall as boolean
      };
   } catch {
      return DEFAULT_PLACEMENT;
   }
}

export function saveBoardPlacement(placement: BoardPlacement) {
   try {
      window.localStorage.setItem(BOARD_PLACEMENT_KEY, JSON.stringify(placement));
   } catch {
      return;
   }
}

function within(value: number, low: number, high: number) {
   return Math.min(Math.max(value, low), Math.max(low, high));
}

/* Where the board is drawn: the student's place and size, or the default to the left of the panel
   under the top bar, kept inside the area and no smaller than the minimum the area allows. */
export function placeBoard(placement: Pick<BoardPlacement, "left" | "top" | "width" | "height">, area: BoardArea): BoardFrame {
   const areaWidth = Math.max(area.right - area.left, 0);
   const areaHeight = Math.max(area.bottom - area.top, 0);
   const defaultHeight = Math.min(DEFAULT_HEIGHT, areaHeight - EDGE_GAP * 2);
   const width = within(placement.width ?? DEFAULT_WIDTH, Math.min(MINIMUM_WIDTH, areaWidth), areaWidth);
   const height = within(placement.height ?? defaultHeight, Math.min(MINIMUM_HEIGHT, areaHeight), areaHeight);
   const left = within(placement.left ?? area.right - width - EDGE_GAP, area.left, area.right - width);
   const top = within(placement.top ?? area.top + EDGE_GAP, area.top, area.bottom - height);

   return { left, top, width, height };
}

export function movedBoard(frame: BoardFrame, deltaX: number, deltaY: number, area: BoardArea): BoardFrame {
   return placeBoard({ ...frame, left: frame.left + deltaX, top: frame.top + deltaY }, area);
}

/* The grip is the lower right corner, so the upper left corner stays where it is and the board
   grows no further than the viewport's right and bottom edges. */
export function resizedBoard(frame: BoardFrame, deltaX: number, deltaY: number, area: BoardArea): BoardFrame {
   const width = Math.min(frame.width + deltaX, area.right - frame.left);
   const height = Math.min(frame.height + deltaY, area.bottom - frame.top);

   return placeBoard({ left: frame.left, top: frame.top, width, height }, area);
}

/* The corners of the area in the order Move goes round them: top left, top right, bottom right,
   bottom left. Move goes on from the corner nearest the board, so the first click always moves it
   visibly, and skips a corner where the board already stands, as a board the full width of the
   area does at both top corners. */
export function nextCorner(frame: BoardFrame, area: BoardArea): BoardFrame {
   const rightmost = area.right - frame.width;
   const lowest = area.bottom - frame.height;
   const corners: Array<[number, number]> = [
      [area.left, area.top],
      [rightmost, area.top],
      [rightmost, lowest],
      [area.left, lowest]
   ];
   const placed = corners.map(([left, top]) => placeBoard({ ...frame, left, top }, area));
   const distances = placed.map((corner) => Math.hypot(corner.left - frame.left, corner.top - frame.top));
   const nearest = distances.indexOf(Math.min(...distances));

   for (let step = 1; step <= placed.length; step += 1) {
      const candidate = placed[(nearest + step) % placed.length];
      const movesTheBoard = candidate.left !== frame.left || candidate.top !== frame.top;

      if (movesTheBoard) {
         return candidate;
      }
   }

   return frame;
}

/* The minimum, the default and the largest the area holds, each kept inside the area from the
   board's upper left corner. Size goes to the next one larger than the board is now, and from the
   largest back to the minimum. */
export function nextSize(frame: BoardFrame, area: BoardArea): BoardFrame {
   const sizes = [
      { width: MINIMUM_WIDTH, height: MINIMUM_HEIGHT },
      { width: DEFAULT_WIDTH, height: DEFAULT_HEIGHT },
      { width: area.right - area.left, height: area.bottom - area.top }
   ];
   const placed = sizes.map((size) => placeBoard({ left: frame.left, top: frame.top, ...size }, area));
   const currentArea = frame.width * frame.height;

   return placed.find((candidate) => candidate.width * candidate.height > currentArea) ?? placed[0];
}

export function dockedHeight(area: BoardArea, tall: boolean) {
   return Math.round((area.bottom - area.top) * (tall ? TALL_SHARE : SHORT_SHARE));
}

function topBarHeight() {
   const header = document.querySelector(".app-header");

   return header === null ? 0 : header.getBoundingClientRect().height;
}

function viewportWidth() {
   return document.documentElement.clientWidth || window.innerWidth;
}

function floatingArea(panel: HTMLElement | null, isPanelOpen: boolean): BoardArea {
   const right = viewportWidth();
   const panelBox = isPanelOpen && panel !== null ? panel.getBoundingClientRect() : null;
   const panelIsBeside = panelBox !== null && panelBox.width > 0;

   return { left: 0, top: topBarHeight(), right: panelIsBeside ? Math.min(right, panelBox.left) : right, bottom: window.innerHeight };
}

/* Docked, the board ends above the tab bar fixed along the bottom of a phone screen. */
function dockedArea(): BoardArea {
   const bar = document.querySelector(".app-nav");
   const barIsFixed = bar !== null && getComputedStyle(bar).position === "fixed";
   const bottom = barIsFixed ? bar.getBoundingClientRect().top : window.innerHeight;

   return { left: 0, top: topBarHeight(), right: viewportWidth(), bottom };
}

function isSameArea(first: BoardArea | null, second: BoardArea) {
   const sameEdges = first !== null && first.left === second.left && first.top === second.top;

   return sameEdges && first.right === second.right && first.bottom === second.bottom;
}

function pixels(value: number) {
   return `${Math.round(value)}px`;
}

type DragKind = "move" | "resize";

interface Drag {
   kind: DragKind;
   pointerId: number;
   startX: number;
   startY: number;
   start: BoardFrame;
}

export function ArtBoard(props: ArtBoardProps) {
   const { figures, mode, isNarrow, isPanelOpen, panel, onDock, onFigureFocused } = props;
   const uid = useId().replace(/:/g, "");
   const section = useRef<HTMLElement>(null);
   const body = useRef<HTMLDivElement>(null);
   const minimizeButton = useRef<HTMLButtonElement>(null);
   const restoreButton = useRef<HTMLButtonElement>(null);
   const focusAfterModeChange = useRef<BoardMode | null>(null);
   const drag = useRef<Drag | null>(null);
   const [placement, setPlacement] = useState(readBoardPlacement);
   const [area, setArea] = useState<BoardArea | null>(null);
   const [isDragging, setIsDragging] = useState(false);
   const index = within(props.current, 0, figures.length - 1);
   const figure = figures[index];
   const isMinimized = mode === "minimized";
   const isFloating = !isNarrow;
   const frame = area === null ? null : placeBoard(placement, area);
   const moveHintId = `${uid}-move-hint`;
   const resizeHintId = `${uid}-resize-hint`;

   const measure = useCallback(() => {
      const next = isNarrow ? dockedArea() : floatingArea(panel.current, isPanelOpen);

      setArea((current) => (isSameArea(current, next) ? current : next));
   }, [isNarrow, isPanelOpen, panel]);

   useLayoutEffect(measure, [measure, mode]);

   useEffect(() => {
      window.addEventListener("resize", measure);

      return () => window.removeEventListener("resize", measure);
   }, [measure]);

   useLayoutEffect(() => {
      const node = section.current;

      if (node === null || area === null || frame === null) {
         return;
      }

      const style = node.style;

      if (isNarrow) {
         const height = dockedHeight(area, placement.tall);
         const drawnBox = node.getBoundingClientRect();
         const isLaidOut = drawnBox.height > 0;

         style.top = pixels(area.top);
         style.removeProperty("left");
         style.removeProperty("width");

         if (isMinimized) {
            style.removeProperty("height");
         } else {
            style.height = pixels(height);
         }

         const expectedBottom = area.top + (isMinimized ? 0 : height);

         onDock?.(isLaidOut ? node.getBoundingClientRect().bottom : expectedBottom);
         return;
      }

      style.left = pixels(frame.left);
      style.top = pixels(frame.top);

      if (isMinimized) {
         style.removeProperty("width");
         style.removeProperty("height");
         style.maxWidth = pixels(frame.width);
      } else {
         style.width = pixels(frame.width);
         style.height = pixels(frame.height);
         style.removeProperty("max-width");
      }

      onDock?.(null);
   });

   useEffect(() => {
      return () => onDock?.(null);
   }, [onDock]);

   useEffect(() => {
      if (!isDragging) {
         saveBoardPlacement({ ...placement, minimized: isMinimized });
      }
   }, [placement, isMinimized, isDragging]);

   useEffect(() => {
      const target = focusAfterModeChange.current;

      focusAfterModeChange.current = null;

      if (target === "minimized") {
         restoreButton.current?.focus();
      } else if (target === "open") {
         minimizeButton.current?.focus();
      }
   }, [mode]);

   const turnId = figure?.turnId;

   useEffect(() => {
      if (!props.focusFigure) {
         return;
      }

      const drawnFigure = body.current?.querySelector<HTMLElement>("[data-testid='tutor-figure']");

      drawnFigure?.focus();
      onFigureFocused();
   }, [props.focusFigure, turnId, mode, onFigureFocused]);

   if (figure === undefined) {
      return null;
   }

   function startDrag(kind: DragKind, event: PointerEvent<HTMLElement>) {
      const startsOnButton = kind === "move" && event.target instanceof Element && event.target.closest("button") !== null;
      const isPrimaryButton = event.button === 0;
      const canDrag = isFloating && !isMinimized && frame !== null && isPrimaryButton && !startsOnButton;

      if (!canDrag) {
         return;
      }

      const handle = event.currentTarget;

      event.preventDefault();

      if (typeof handle.setPointerCapture === "function") {
         handle.setPointerCapture(event.pointerId);
      }

      drag.current = { kind, pointerId: event.pointerId, startX: event.clientX, startY: event.clientY, start: frame };
      setIsDragging(true);
   }

   function followDrag(event: PointerEvent<HTMLElement>) {
      const current = drag.current;
      const isThisDrag = current !== null && current.pointerId === event.pointerId && area !== null;

      if (!isThisDrag) {
         return;
      }

      const deltaX = event.clientX - current.startX;
      const deltaY = event.clientY - current.startY;
      const next = current.kind === "move" ? movedBoard(current.start, deltaX, deltaY, area) : resizedBoard(current.start, deltaX, deltaY, area);

      setPlacement((latest) => ({ ...latest, ...next }));
   }

   function endDrag(event: PointerEvent<HTMLElement>) {
      const isThisDrag = drag.current !== null && drag.current.pointerId === event.pointerId;

      if (!isThisDrag) {
         return;
      }

      const handle = event.currentTarget;
      const holdsCapture = typeof handle.hasPointerCapture === "function" && handle.hasPointerCapture(event.pointerId);

      drag.current = null;

      if (holdsCapture) {
         handle.releasePointerCapture(event.pointerId);
      }

      setIsDragging(false);
   }

   function stepByKey(kind: DragKind, event: KeyboardEvent<HTMLElement>) {
      const direction = ARROW_DIRECTIONS[event.key];
      const isOnHandle = event.target === event.currentTarget;
      const canStep = direction !== undefined && isOnHandle && isFloating && frame !== null && area !== null;

      if (!canStep) {
         return;
      }

      event.preventDefault();

      const step = event.shiftKey ? LARGE_KEY_STEP : KEY_STEP;
      const deltaX = direction[0] * step;
      const deltaY = direction[1] * step;
      const next = kind === "move" ? movedBoard(frame, deltaX, deltaY, area) : resizedBoard(frame, deltaX, deltaY, area);

      setPlacement((latest) => ({ ...latest, ...next }));
   }

   function stepBoard(step: (frame: BoardFrame, area: BoardArea) => BoardFrame) {
      if (frame === null || area === null) {
         return;
      }

      const next = step(frame, area);

      setPlacement((latest) => ({ ...latest, ...next }));
   }

   function minimize() {
      focusAfterModeChange.current = "minimized";
      props.onMinimize();
   }

   function restore() {
      focusAfterModeChange.current = "open";
      props.onRestore();
   }

   const title = figure.spec.title;
   const docked = isNarrow ? "true" : "false";

   if (isMinimized) {
      return (
         <section ref={section} className="art-board" aria-label={ART_BOARD_TITLE} data-docked={docked} data-minimized="true" data-testid="art-board">
            <p className="art-board-bar-title">{minimizedBoard(title)}</p>

            <button ref={restoreButton} type="button" className="text-button" aria-label={RESTORE_BOARD_LABEL} onClick={restore}>
               {RESTORE_LABEL}
            </button>
         </section>
      );
   }

   const isFirst = index === 0;
   const isLast = index === figures.length - 1;

   return (
      <section ref={section} className="art-board" aria-label={ART_BOARD_TITLE} data-docked={docked} data-testid="art-board">
         <div
            className="art-board-title-bar"
            role={isFloating ? "group" : undefined}
            tabIndex={isFloating ? 0 : undefined}
            aria-label={isFloating ? MOVE_BOARD_LABEL : undefined}
            aria-describedby={isFloating ? moveHintId : undefined}
            onPointerDown={(event) => startDrag("move", event)}
            onPointerMove={followDrag}
            onPointerUp={endDrag}
            onPointerCancel={endDrag}
            onLostPointerCapture={endDrag}
            onKeyDown={(event) => stepByKey("move", event)}
            data-testid="art-board-title-bar"
         >
            <div className="art-board-title-row">
               <h2 className="art-board-heading">{ART_BOARD_TITLE}</h2>

               <p className="art-board-figure-title" data-testid="art-board-figure-title">
                  {title}
               </p>

               <div className="art-board-actions">
                  {isNarrow ? (
                     <button type="button" className="text-button" onClick={() => setPlacement((latest) => ({ ...latest, tall: !latest.tall }))}>
                        {placement.tall ? SHORTER_LABEL : TALLER_LABEL}
                     </button>
                  ) : (
                     <>
                        <button type="button" className="text-button" aria-label={MOVE_TO_NEXT_CORNER_LABEL} onClick={() => stepBoard(nextCorner)}>
                           {MOVE_LABEL}
                        </button>

                        <button type="button" className="text-button" aria-label={CHANGE_SIZE_LABEL} onClick={() => stepBoard(nextSize)}>
                           {SIZE_LABEL}
                        </button>
                     </>
                  )}

                  <button ref={minimizeButton} type="button" className="text-button" aria-label={MINIMIZE_BOARD_LABEL} onClick={minimize}>
                     {MINIMIZE_LABEL}
                  </button>

                  <button type="button" className="text-button" aria-label={CLOSE_BOARD_LABEL} onClick={props.onClose}>
                     {CLOSE_LABEL}
                  </button>
               </div>
            </div>

            <div className="art-board-figures">
               <button type="button" className="text-button" aria-label={PREVIOUS_FIGURE_LABEL} disabled={isFirst} onClick={() => props.onChoose(figures[index - 1].turnId)}>
                  {PREVIOUS_STEP_LABEL}
               </button>

               <p className="art-board-count" data-testid="art-board-count">
                  {boardFigureCount(index + 1, figures.length)}
               </p>

               <button type="button" className="text-button" aria-label={NEXT_FIGURE_LABEL} disabled={isLast} onClick={() => props.onChoose(figures[index + 1].turnId)}>
                  {NEXT_STEP_LABEL}
               </button>
            </div>

            {isFloating ? (
               <p className="visually-hidden" id={moveHintId}>
                  {MOVE_BOARD_HINT}
               </p>
            ) : null}
         </div>

         <div className="art-board-body" ref={body}>
            <TutorFigure key={figure.turnId} spec={figure.spec} revealed={figure.revealed} finished={figure.finished} onShowAll={() => props.onShowAll(figure.turnId)} />
         </div>

         {isFloating ? (
            <>
               <button
                  type="button"
                  className="art-board-grip"
                  aria-label={RESIZE_BOARD_LABEL}
                  aria-describedby={resizeHintId}
                  onPointerDown={(event) => startDrag("resize", event)}
                  onPointerMove={followDrag}
                  onPointerUp={endDrag}
                  onPointerCancel={endDrag}
                  onLostPointerCapture={endDrag}
                  onKeyDown={(event) => stepByKey("resize", event)}
                  data-testid="art-board-grip"
               >
                  <svg className="art-board-grip-mark" viewBox="0 0 12 12" aria-hidden="true" focusable="false">
                     <path d="M11 3 L3 11 M11 7 L7 11" />
                  </svg>
               </button>

               <p className="visually-hidden" id={resizeHintId}>
                  {RESIZE_BOARD_HINT}
               </p>
            </>
         ) : null}
      </section>
   );
}
