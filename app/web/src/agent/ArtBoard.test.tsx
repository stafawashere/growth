import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { useRef, useState } from "react";
import { afterAll, afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest";

import type { TutorFigureSpec } from "../api/types";
import { TutorHarness, frame, scriptedFetch } from "../testing/agent";
import { ArtBoard, BOARD_PLACEMENT_KEY, type BoardFigure, type BoardMode } from "./ArtBoard";
import { SECANT_TO_TANGENT, TRIANGLE_DIAGRAM } from "./figureFixtures";

/* The tutor's art board (docs/agent/drawing-design.md, "The art board"): in the conversation, where
   a figure opens it without taking focus and Show on the board opens it with focus; and on its own,
   where it moves, resizes and docks inside a viewport the test lays out, since jsdom lays out
   nothing. */

const VIEWPORT_WIDTH = 1280;

const VIEWPORT_HEIGHT = 800;

const TOP_BAR_HEIGHT = 56;

/* jsdom has no pointer events, so a mouse event carrying a pointer id stands in for them. */
class TestPointerEvent extends MouseEvent {
   pointerId: number;

   constructor(type: string, init: PointerEventInit = {}) {
      super(type, init);
      this.pointerId = init.pointerId ?? 1;
   }
}

const capture = { set: vi.fn(), has: vi.fn(() => true), release: vi.fn() };

const jsdomWindow = document.defaultView as unknown as Record<string, unknown>;

beforeAll(() => {
   jsdomWindow.PointerEvent = TestPointerEvent;
   Element.prototype.setPointerCapture = capture.set;
   Element.prototype.hasPointerCapture = capture.has;
   Element.prototype.releasePointerCapture = capture.release;
});

afterAll(() => {
   delete jsdomWindow.PointerEvent;
   delete (Element.prototype as Partial<Element>).setPointerCapture;
   delete (Element.prototype as Partial<Element>).hasPointerCapture;
   delete (Element.prototype as Partial<Element>).releasePointerCapture;
});

let fetchScript: ReturnType<typeof scriptedFetch>;

beforeEach(() => {
   fetchScript = scriptedFetch();
   vi.stubGlobal("fetch", fetchScript.fetchStub);
   window.localStorage.clear();
   capture.set.mockClear();
   Object.defineProperty(window, "innerWidth", { configurable: true, value: VIEWPORT_WIDTH });
   Object.defineProperty(window, "innerHeight", { configurable: true, value: VIEWPORT_HEIGHT });
});

afterEach(() => {
   cleanup();
   vi.unstubAllGlobals();
   vi.restoreAllMocks();
   window.localStorage.clear();
});

function board() {
   return screen.getByRole("region", { name: "Art board" });
}

function queryBoard() {
   return screen.queryByRole("region", { name: "Art board" });
}

function composer() {
   return screen.getByLabelText("Message to the tutor");
}

function figureReply(spec: TutorFigureSpec, outcome = "complete") {
   return [
      frame("start", { conversation_id: "ACV-1", turn_id: "ATN-1", screen_line: "", can_see: [] }),
      frame("text", { delta: "Look at this. " }),
      frame("figure", spec),
      frame("text", { delta: "Then read on." }),
      frame("end", { turn_id: "ATN-1", outcome, turns_on_item: 0, turns_in_conversation: 1 })
   ];
}

async function sendAndAnswer(message: string, frames: string[]) {
   const count = fetchScript.turns.length;

   fireEvent.change(composer(), { target: { value: message } });
   fireEvent.keyDown(composer(), { key: "Enter" });
   await waitFor(() => expect(fetchScript.turns.length).toBe(count + 1));

   await act(async () => {
      frames.forEach((text) => fetchScript.turns[count].push(text));
      fetchScript.turns[count].close();
   });
   await waitFor(() => expect(screen.queryByRole("button", { name: "Stop" })).toBeNull());
}

async function conversationWithFigure(spec: TutorFigureSpec = SECANT_TO_TANGENT) {
   render(<TutorHarness screen={{ kind: "today" }} />);

   fireEvent.click(screen.getByRole("button", { name: "Ask, Ctrl+/" }));
   await sendAndAnswer("Draw it", figureReply(spec));
}

describe("the art board in the conversation", () => {
   it("opens on a figure after the tutor panel without taking focus, and the reply keeps one line", async () => {
      await conversationWithFigure();

      const opened = board();

      expect(document.activeElement).toBe(composer());
      expect(within(opened).getByTestId("art-board-figure-title").textContent).toBe(SECANT_TO_TANGENT.title);
      expect(within(opened).getByTestId("art-board-count").textContent).toBe("Figure 1 of 1");
      expect(within(opened).getByRole("img", { name: SECANT_TO_TANGENT.title })).toBeTruthy();
      expect(screen.getByTestId("agent-panel").compareDocumentPosition(opened) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();

      const reply = screen.getByTestId("agent-reply");

      expect(within(reply).queryByRole("img")).toBeNull();
      expect(within(reply).getByTestId("agent-figure-on-board").textContent).toContain(`Figure on the board: ${SECANT_TO_TANGENT.title}`);
   });

   it("opens on Show on the board after it was closed, and moves focus to that figure", async () => {
      await conversationWithFigure();

      fireEvent.click(within(board()).getByRole("button", { name: "Close the art board" }));

      expect(queryBoard()).toBeNull();
      expect(document.activeElement).toBe(screen.getByRole("button", { name: "Ask, Ctrl+/" }));

      fireEvent.click(screen.getByRole("button", { name: "Show on the board" }));

      await waitFor(() => expect(document.activeElement).toBe(within(board()).getByRole("group", { name: SECANT_TO_TANGENT.title })));
   });

   it("steps between the conversation's figures with Previous and Next, and Show on the board picks an earlier one", async () => {
      await conversationWithFigure();
      await sendAndAnswer("And the ladder?", figureReply(TRIANGLE_DIAGRAM));

      const previous = () => within(board()).getByRole("button", { name: "Previous figure" }) as HTMLButtonElement;
      const next = () => within(board()).getByRole("button", { name: "Next figure" }) as HTMLButtonElement;
      const shown = () => [within(board()).getByTestId("art-board-count").textContent, within(board()).getByTestId("art-board-figure-title").textContent];

      expect(shown()).toEqual(["Figure 2 of 2", TRIANGLE_DIAGRAM.title]);
      expect(next().disabled).toBe(true);

      fireEvent.click(previous());

      expect(shown()).toEqual(["Figure 1 of 2", SECANT_TO_TANGENT.title]);
      expect(within(board()).getByRole("img", { name: SECANT_TO_TANGENT.title })).toBeTruthy();
      expect(previous().disabled).toBe(true);

      fireEvent.click(next());

      expect(shown()).toEqual(["Figure 2 of 2", TRIANGLE_DIAGRAM.title]);

      fireEvent.click(screen.getAllByRole("button", { name: "Show on the board" })[0]);

      await waitFor(() => expect(shown()).toEqual(["Figure 1 of 2", SECANT_TO_TANGENT.title]));
   });

   it("minimizes to a bar with Restore, restores, and comes back from the bar when the tutor draws again", async () => {
      await conversationWithFigure();

      fireEvent.click(within(board()).getByRole("button", { name: "Minimize the art board" }));

      expect(board().textContent).toBe(`Art board: ${SECANT_TO_TANGENT.title}Restore`);
      expect(within(board()).queryByRole("img")).toBeNull();
      expect(document.activeElement).toBe(within(board()).getByRole("button", { name: "Restore the art board" }));

      fireEvent.click(within(board()).getByRole("button", { name: "Restore the art board" }));

      expect(within(board()).getByRole("img", { name: SECANT_TO_TANGENT.title })).toBeTruthy();
      expect(document.activeElement).toBe(within(board()).getByRole("button", { name: "Minimize the art board" }));

      fireEvent.click(within(board()).getByRole("button", { name: "Minimize the art board" }));
      composer().focus();
      await sendAndAnswer("And the ladder?", figureReply(TRIANGLE_DIAGRAM));

      expect(within(board()).getByRole("img", { name: TRIANGLE_DIAGRAM.title })).toBeTruthy();
      expect(document.activeElement).toBe(composer());
   });

   it("stays closed until the next figure, which opens it without taking focus", async () => {
      await conversationWithFigure();

      fireEvent.click(within(board()).getByRole("button", { name: "Close the art board" }));
      composer().focus();
      await sendAndAnswer("Say more", [
         frame("start", { conversation_id: "ACV-1", turn_id: "ATN-2", screen_line: "", can_see: [] }),
         frame("text", { delta: "No figure this time." }),
         frame("end", { turn_id: "ATN-2", outcome: "complete", turns_on_item: 0, turns_in_conversation: 2 })
      ]);

      expect(queryBoard()).toBeNull();

      await sendAndAnswer("And the ladder?", figureReply(TRIANGLE_DIAGRAM));

      expect(within(board()).getByTestId("art-board-count").textContent).toBe("Figure 2 of 2");
      expect(document.activeElement).toBe(composer());
   });

   it("drops a withheld reply's figure and shows the latest figure left", async () => {
      await conversationWithFigure();
      await sendAndAnswer("And the ladder?", figureReply(TRIANGLE_DIAGRAM, "withheld"));

      expect(within(board()).getByTestId("art-board-count").textContent).toBe("Figure 1 of 1");
      expect(within(board()).getByTestId("art-board-figure-title").textContent).toBe(SECANT_TO_TANGENT.title);
   });
});

function boardFigure(spec: TutorFigureSpec, turnId: string): BoardFigure {
   return { turnId, spec, revealed: spec.steps.length, finished: true };
}

interface LaidOut {
   panelLeft?: number;
}

/* The top bar and, when given, the open tutor panel, at the sizes the stylesheet gives them. */
function layOut({ panelLeft }: LaidOut = {}) {
   vi.spyOn(Element.prototype, "getBoundingClientRect").mockImplementation(function (this: Element) {
      const isTopBar = this.classList.contains("app-header");
      const isPanel = this.getAttribute("data-testid") === "panel" && panelLeft !== undefined;
      const box = { left: 0, top: 0, width: 0, height: 0 };

      if (isTopBar) {
         Object.assign(box, { width: VIEWPORT_WIDTH, height: TOP_BAR_HEIGHT });
      }

      if (isPanel) {
         Object.assign(box, { left: panelLeft, top: TOP_BAR_HEIGHT, width: VIEWPORT_WIDTH - panelLeft!, height: VIEWPORT_HEIGHT - TOP_BAR_HEIGHT });
      }

      return { ...box, x: box.left, y: box.top, right: box.left + box.width, bottom: box.top + box.height, toJSON: () => ({}) } as DOMRect;
   });
}

function StandaloneBoard(props: { isNarrow?: boolean; isPanelOpen?: boolean; onDock?: (bottom: number | null) => void }) {
   const [mode, setMode] = useState<BoardMode>("open");
   const panel = useRef<HTMLElement>(null);

   return (
      <>
         <header className="app-header" />

         <aside ref={panel} data-testid="panel" />

         <ArtBoard
            figures={[boardFigure(SECANT_TO_TANGENT, "reply")]}
            current={0}
            mode={mode}
            isNarrow={props.isNarrow ?? false}
            isPanelOpen={props.isPanelOpen ?? false}
            panel={panel}
            focusFigure={false}
            onFigureFocused={() => undefined}
            onChoose={() => undefined}
            onMinimize={() => setMode("minimized")}
            onRestore={() => setMode("open")}
            onClose={() => undefined}
            onShowAll={() => undefined}
            onDock={props.onDock}
         />
      </>
   );
}

function placed() {
   const style = board().style;

   return { left: style.left, top: style.top, width: style.width, height: style.height };
}

function titleBar() {
   return screen.getByTestId("art-board-title-bar");
}

function grip() {
   return screen.getByRole("button", { name: "Resize the art board" });
}

function drag(handle: Element, from: [number, number], to: Array<[number, number]>) {
   fireEvent.pointerDown(handle, { pointerId: 7, button: 0, clientX: from[0], clientY: from[1] });

   for (const [x, y] of to) {
      fireEvent.pointerMove(handle, { pointerId: 7, clientX: x, clientY: y });
   }

   fireEvent.pointerUp(handle, { pointerId: 7, clientX: to[to.length - 1][0], clientY: to[to.length - 1][1] });
}

function stored() {
   return JSON.parse(window.localStorage.getItem(BOARD_PLACEMENT_KEY) ?? "null");
}

describe("moving and sizing the art board from 900 px", () => {
   it("starts to the left of the panel's column under the top bar", () => {
      layOut();
      render(<StandaloneBoard />);

      expect(placed()).toEqual({ left: "848px", top: "72px", width: "416px", height: "560px" });
   });

   it("moves with a drag on its title bar, held inside the viewport below the top bar, and remembers where it was left", () => {
      layOut();
      render(<StandaloneBoard />);

      drag(titleBar(), [900, 80], [[700, 140], [500, 200]]);

      expect(capture.set).toHaveBeenCalledWith(7);
      expect(placed()).toMatchObject({ left: "448px", top: "192px" });

      drag(titleBar(), [500, 200], [[-2000, -2000]]);

      expect(placed()).toMatchObject({ left: "0px", top: `${TOP_BAR_HEIGHT}px` });

      drag(titleBar(), [10, 60], [[5000, 5000]]);

      expect(placed()).toEqual({ left: "864px", top: "240px", width: "416px", height: "560px" });
      expect(stored()).toEqual({ left: 864, top: 240, width: 416, height: 560, minimized: false, tall: false });
   });

   it("does not move when the drag starts on a button in the title bar", () => {
      layOut();
      render(<StandaloneBoard />);

      drag(screen.getByRole("button", { name: "Next figure" }), [900, 80], [[500, 300]]);

      expect(placed()).toMatchObject({ left: "848px", top: "72px" });
   });

   it("resizes from the corner grip, no smaller than 280 by 240 and no further than the viewport", () => {
      layOut();
      render(<StandaloneBoard />);

      drag(grip(), [1260, 628], [[100, 100]]);

      expect(placed()).toEqual({ left: "848px", top: "72px", width: "280px", height: "240px" });

      drag(grip(), [1124, 308], [[5000, 5000]]);

      expect(placed()).toEqual({ left: "848px", top: "72px", width: "432px", height: "728px" });
   });

   it("moves 16 px for an arrow key on the focused title bar and 64 px with Shift, and resizes the same way from the grip", () => {
      layOut();
      render(<StandaloneBoard />);

      expect(titleBar().tabIndex).toBe(0);
      expect(titleBar().getAttribute("aria-label")).toBe("Move the art board");

      fireEvent.keyDown(titleBar(), { key: "ArrowLeft" });

      expect(placed()).toMatchObject({ left: "832px", top: "72px" });

      fireEvent.keyDown(titleBar(), { key: "ArrowDown", shiftKey: true });

      expect(placed()).toMatchObject({ left: "832px", top: "136px" });

      fireEvent.keyDown(titleBar(), { key: "ArrowUp", shiftKey: true });
      fireEvent.keyDown(titleBar(), { key: "ArrowUp" });

      expect(placed()).toMatchObject({ top: `${TOP_BAR_HEIGHT}px` });

      fireEvent.keyDown(screen.getByRole("button", { name: "Minimize the art board" }), { key: "ArrowLeft" });

      expect(placed()).toMatchObject({ left: "832px" });

      fireEvent.keyDown(grip(), { key: "ArrowLeft" });
      fireEvent.keyDown(grip(), { key: "ArrowDown", shiftKey: true });

      expect(placed()).toEqual({ left: "832px", top: `${TOP_BAR_HEIGHT}px`, width: "400px", height: "624px" });
   });

   it("keeps out of the open tutor panel's column, so it never covers the composer", () => {
      layOut({ panelLeft: 896 });
      render(<StandaloneBoard isPanelOpen />);

      expect(placed()).toMatchObject({ left: "464px", width: "416px" });

      drag(titleBar(), [500, 80], [[2000, 80]]);

      expect(placed()).toMatchObject({ left: "480px" });

      drag(grip(), [890, 628], [[2000, 628]]);

      expect(placed()).toMatchObject({ left: "480px", width: "416px" });
   });

   it("moves round the corners of the area with one click each, from the corner nearest the board, and remembers each place", () => {
      layOut();
      render(<StandaloneBoard />);

      const move = screen.getByRole("button", { name: "Move the art board to the next corner" });
      const visited: Array<[string, string]> = [];

      for (let click = 0; click < 5; click += 1) {
         fireEvent.click(move);
         visited.push([placed().left, placed().top]);
      }

      expect(move.textContent).toBe("Move");
      expect(visited).toEqual([
         ["864px", "240px"],
         ["0px", "240px"],
         ["0px", `${TOP_BAR_HEIGHT}px`],
         ["864px", `${TOP_BAR_HEIGHT}px`],
         ["864px", "240px"]
      ]);
      expect(stored()).toEqual({ left: 864, top: 240, width: 416, height: 560, minimized: false, tall: false });
   });

   it("keeps the corners Move goes to out of the open tutor panel's column", () => {
      layOut({ panelLeft: 896 });
      render(<StandaloneBoard isPanelOpen />);

      const visited: Array<[string, string]> = [];

      for (let click = 0; click < 4; click += 1) {
         fireEvent.click(screen.getByRole("button", { name: "Move the art board to the next corner" }));
         visited.push([placed().left, placed().top]);
      }

      expect(visited).toEqual([
         ["480px", "240px"],
         ["0px", "240px"],
         ["0px", `${TOP_BAR_HEIGHT}px`],
         ["480px", `${TOP_BAR_HEIGHT}px`]
      ]);
   });

   it("goes round the largest size, the minimum and the default with one click each, and remembers each size", () => {
      layOut();
      render(<StandaloneBoard />);

      const size = screen.getByRole("button", { name: "Change the art board's size" });

      expect(size.textContent).toBe("Size");

      fireEvent.click(size);

      expect(placed()).toEqual({ left: "0px", top: `${TOP_BAR_HEIGHT}px`, width: `${VIEWPORT_WIDTH}px`, height: `${VIEWPORT_HEIGHT - TOP_BAR_HEIGHT}px` });
      expect(stored()).toEqual({ left: 0, top: TOP_BAR_HEIGHT, width: VIEWPORT_WIDTH, height: VIEWPORT_HEIGHT - TOP_BAR_HEIGHT, minimized: false, tall: false });

      fireEvent.click(size);

      expect(placed()).toEqual({ left: "0px", top: `${TOP_BAR_HEIGHT}px`, width: "280px", height: "240px" });
      expect(stored()).toMatchObject({ width: 280, height: 240 });

      fireEvent.click(size);

      expect(placed()).toEqual({ left: "0px", top: `${TOP_BAR_HEIGHT}px`, width: "416px", height: "560px" });
   });

   it("comes back where the student left it, kept inside the viewport", () => {
      window.localStorage.setItem(BOARD_PLACEMENT_KEY, JSON.stringify({ left: 100, top: 120, width: 500, height: 400, minimized: false, tall: false }));
      layOut();
      render(<StandaloneBoard />);

      expect(placed()).toEqual({ left: "100px", top: "120px", width: "500px", height: "400px" });

      cleanup();
      window.localStorage.setItem(BOARD_PLACEMENT_KEY, JSON.stringify({ left: 5000, top: 5000, width: 500, height: 400, minimized: false, tall: false }));
      render(<StandaloneBoard />);

      expect(placed()).toEqual({ left: "780px", top: "400px", width: "500px", height: "400px" });
   });

   it("falls back to the default place when the storage refuses every read and write", () => {
      vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
         throw new DOMException("The operation is insecure.", "SecurityError");
      });
      vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
         throw new DOMException("The operation is insecure.", "SecurityError");
      });
      layOut();
      render(<StandaloneBoard />);

      expect(placed()).toEqual({ left: "848px", top: "72px", width: "416px", height: "560px" });

      fireEvent.keyDown(titleBar(), { key: "ArrowLeft" });

      expect(placed()).toMatchObject({ left: "832px" });
   });

   it("falls back to the default place when what is stored is not a place", () => {
      window.localStorage.setItem(BOARD_PLACEMENT_KEY, JSON.stringify({ left: "far", top: 120, width: 500, height: 400, minimized: false, tall: false }));
      layOut();
      render(<StandaloneBoard />);

      expect(placed()).toEqual({ left: "848px", top: "72px", width: "416px", height: "560px" });
   });

   it("minimizes to a bar where it stood, and remembers that it was minimized", () => {
      layOut();
      render(<StandaloneBoard />);

      fireEvent.click(screen.getByRole("button", { name: "Minimize the art board" }));

      expect(placed()).toEqual({ left: "848px", top: "72px", width: "", height: "" });
      expect(stored()).toMatchObject({ minimized: true });
      expect(screen.queryByRole("button", { name: "Resize the art board" })).toBeNull();
   });
});

describe("the art board under 900 px", () => {
   it("docks full width under the top bar, with no grip and no drag, and reports where it ends", () => {
      const docks = vi.fn();

      layOut();
      render(<StandaloneBoard isNarrow onDock={docks} />);

      const shortHeight = Math.round((VIEWPORT_HEIGHT - TOP_BAR_HEIGHT) * 0.4);

      expect(board().getAttribute("data-docked")).toBe("true");
      expect(placed()).toEqual({ left: "", top: `${TOP_BAR_HEIGHT}px`, width: "", height: `${shortHeight}px` });
      expect(screen.queryByRole("button", { name: "Resize the art board" })).toBeNull();
      expect(titleBar().hasAttribute("tabindex")).toBe(false);
      expect(docks).toHaveBeenLastCalledWith(TOP_BAR_HEIGHT + shortHeight);

      drag(titleBar(), [200, 80], [[20, 400]]);
      fireEvent.keyDown(titleBar(), { key: "ArrowDown" });

      expect(placed()).toEqual({ left: "", top: `${TOP_BAR_HEIGHT}px`, width: "", height: `${shortHeight}px` });
      expect(capture.set).not.toHaveBeenCalled();
   });

   it("shows no Move or Size, which the dock does not need", () => {
      layOut();
      render(<StandaloneBoard isNarrow />);

      expect(screen.queryByRole("button", { name: "Move the art board to the next corner" })).toBeNull();
      expect(screen.queryByRole("button", { name: "Change the art board's size" })).toBeNull();
      expect(screen.getByRole("button", { name: "Taller" })).toBeTruthy();
   });

   it("grows with Taller and shrinks back with Shorter", () => {
      const docks = vi.fn();

      layOut();
      render(<StandaloneBoard isNarrow onDock={docks} />);

      const tallHeight = Math.round((VIEWPORT_HEIGHT - TOP_BAR_HEIGHT) * 0.65);

      fireEvent.click(screen.getByRole("button", { name: "Taller" }));

      expect(placed()).toMatchObject({ height: `${tallHeight}px` });
      expect(docks).toHaveBeenLastCalledWith(TOP_BAR_HEIGHT + tallHeight);
      expect(stored()).toMatchObject({ tall: true });

      fireEvent.click(screen.getByRole("button", { name: "Shorter" }));

      expect(placed()).toMatchObject({ height: `${Math.round((VIEWPORT_HEIGHT - TOP_BAR_HEIGHT) * 0.4)}px` });
   });

   it("stops reporting a dock once it is gone", () => {
      const docks = vi.fn();

      layOut();

      const { unmount } = render(<StandaloneBoard isNarrow onDock={docks} />);

      unmount();

      expect(docks).toHaveBeenLastCalledWith(null);
   });
});
