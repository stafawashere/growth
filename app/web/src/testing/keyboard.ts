import { act, fireEvent } from "@testing-library/react";

/* Test support: the keyboard-only driver of session/keyboardOnlySession.test.tsx (11's P8
   test_keyboard_only_session), shared so the lesson reader's traversal and the per-record render
   harness drive the page the same way. Tab walks the tabbable elements in document order, a radio
   group being one stop; Enter on a button and Space on a button or radio click it; an arrow key in
   a radio group checks the next radio; a printable key in a text field or the math field stand-in
   enters that character. Every pointer event, and any click not dispatched as a keyboard
   activation, is recorded, so a test can require that none happened. */

const TABBABLE = [
   "button:not(:disabled)",
   "input:not(:disabled):not([type='hidden'])",
   "select:not(:disabled)",
   "textarea:not(:disabled)",
   "a[href]",
   "summary",
   "[tabindex]"
].join(", ");

const POINTER_EVENTS = ["pointerdown", "pointerup", "mousedown", "mouseup", "touchstart", "touchend"];

export const pointerEvents: string[] = [];

let isKeyboardActivation = false;

function recordPointer(event: Event) {
   pointerEvents.push(`${event.type} on ${(event.target as Element).tagName}`);
}

function recordPointerClick(event: Event) {
   if (!isKeyboardActivation) {
      pointerEvents.push(`pointer click on ${(event.target as Element).tagName}`);
   }
}

export function startRecordingPointer() {
   pointerEvents.length = 0;

   for (const type of POINTER_EVENTS) {
      document.addEventListener(type, recordPointer, true);
   }

   document.addEventListener("click", recordPointerClick, true);
}

export function stopRecordingPointer() {
   for (const type of POINTER_EVENTS) {
      document.removeEventListener(type, recordPointer, true);
   }

   document.removeEventListener("click", recordPointerClick, true);
}

function isRadioStop(element: HTMLInputElement, all: Element[]) {
   const group = all.filter(
      (candidate): candidate is HTMLInputElement =>
         candidate instanceof HTMLInputElement && candidate.type === "radio" && candidate.name === element.name
   );
   const checked = group.find((radio) => radio.checked);

   return element === (checked ?? group[0]);
}

export function tabbables(): HTMLElement[] {
   const all = Array.from(document.body.querySelectorAll(TABBABLE));

   return all.filter((element): element is HTMLElement => {
      const index = Number(element.getAttribute("tabindex") ?? "0");
      const isRadio = element instanceof HTMLInputElement && element.type === "radio";

      if (index < 0 || element.closest("[hidden], [inert]") !== null) {
         return false;
      }

      return isRadio ? isRadioStop(element as HTMLInputElement, all) : true;
   });
}

export function tab() {
   const order = tabbables();
   const current = order.indexOf(document.activeElement as HTMLElement);
   const next = order[(current + 1) % order.length];

   fireEvent.keyDown(document.activeElement ?? document.body, { key: "Tab" });
   act(() => next.focus());
}

/* Tabs until the target has focus, failing if a full cycle never reaches it. */
export function tabTo(target: HTMLElement) {
   const stops = tabbables().length;

   for (let pressed = 0; pressed <= stops; pressed += 1) {
      if (document.activeElement === target) {
         return;
      }

      tab();
   }

   throw new Error(`Tab never reaches ${target.outerHTML.slice(0, 120)}`);
}

function keyboardClick(element: Element) {
   isKeyboardActivation = true;

   try {
      act(() => {
         element.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, detail: 0 }));
      });
   } finally {
      isKeyboardActivation = false;
   }
}

export function press(key: string) {
   const focused = document.activeElement as HTMLElement;
   const proceeds = fireEvent.keyDown(focused, { key });

   if (!proceeds) {
      fireEvent.keyUp(focused, { key });

      return;
   }

   const isButton = focused instanceof HTMLButtonElement || focused instanceof HTMLAnchorElement;
   const isChoice = focused instanceof HTMLInputElement && (focused.type === "radio" || focused.type === "checkbox");
   const isTextField = (focused instanceof HTMLInputElement && !isChoice) || focused instanceof HTMLTextAreaElement;
   const isArrow = ["ArrowDown", "ArrowRight", "ArrowUp", "ArrowLeft"].includes(key);

   if (key === "Enter" && isButton) {
      keyboardClick(focused);
   } else if (key === " " && (isButton || isChoice)) {
      keyboardClick(focused);
   } else if (isArrow && focused instanceof HTMLInputElement && focused.type === "radio") {
      const group = Array.from(document.querySelectorAll<HTMLInputElement>(`input[type='radio'][name='${focused.name}']`));
      const step = key === "ArrowDown" || key === "ArrowRight" ? 1 : -1;
      const next = group[(group.indexOf(focused) + step + group.length) % group.length];

      act(() => next.focus());
      keyboardClick(next);
   } else if (key.length === 1 && isTextField) {
      fireEvent.input(focused, { target: { value: (focused as HTMLInputElement).value + key } });
   }

   fireEvent.keyUp(focused, { key });
}

/* Tabs to the target and activates it with Enter. */
export function activate(target: HTMLElement) {
   tabTo(target);
   press("Enter");
}

/* The math field seam: MathLive's element is focusable in the tab order and turns keystrokes into
   its value. This stands in for it with only what MathField.tsx reads, getValue and the input
   event. */
export class KeyboardMathField extends HTMLElement {
   private latex = "";

   connectedCallback() {
      this.tabIndex = 0;
      this.addEventListener("keydown", (event) => {
         if (event.key.length === 1) {
            this.latex += event.key;
            this.dispatchEvent(new Event("input", { bubbles: true }));
         }
      });
   }

   getValue(format: string) {
      if (format === "math-json") {
         return JSON.stringify(Number.isNaN(Number(this.latex)) ? this.latex : Number(this.latex));
      }

      return this.latex;
   }
}

export function defineKeyboardMathField() {
   if (customElements.get("math-field") === undefined) {
      customElements.define("math-field", KeyboardMathField);
   }
}
