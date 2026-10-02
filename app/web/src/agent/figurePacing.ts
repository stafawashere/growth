import { splitInlineMath } from "../math/mathjson";

/* The pace a figure is built at in a reply (docs/agent/drawing-design.md, "The client"). Each step
   of the figure is a gate in the reply's display queue, and the gate, with every piece of text
   behind it, waits until the words shown since the previous gate could have been read: 238 words
   a minute, a formula counted as three words, and never more than six seconds a step. The first
   gate counts from the moment the reply's first text was shown. */

export const READING_WORDS_PER_MINUTE = 238;

export const WORDS_PER_FORMULA = 3;

export const LONGEST_STEP_WAIT_MILLISECONDS = 6000;

const MILLISECONDS_PER_MINUTE = 60000;

export function wordsIn(text: string) {
   return splitInlineMath(text).reduce((total, segment) => {
      if (segment.kind === "math") {
         return total + WORDS_PER_FORMULA;
      }

      const words = segment.text.split(/\s+/).filter((word) => word !== "");

      return total + words.length;
   }, 0);
}

export function gateDelay(words: number) {
   const readingTime = (words / READING_WORDS_PER_MINUTE) * MILLISECONDS_PER_MINUTE;

   return Math.min(readingTime, LONGEST_STEP_WAIT_MILLISECONDS);
}

export interface PacerHandlers {
   showText: (text: string) => void;
   openGate: (stepIndex: number) => void;
   onBusyChange: (isBusy: boolean) => void;
}

export interface PacerClock {
   now: () => number;
   setTimer: (run: () => void, milliseconds: number) => ReturnType<typeof setTimeout>;
   clearTimer: (timer: ReturnType<typeof setTimeout>) => void;
}

const SYSTEM_CLOCK: PacerClock = {
   now: () => Date.now(),
   setTimer: (run, milliseconds) => setTimeout(run, milliseconds),
   clearTimer: (timer) => clearTimeout(timer)
};

type QueuedItem = { kind: "text"; text: string } | { kind: "gate"; stepIndex: number } | { kind: "action"; run: () => void };

export interface ReplyPacer {
   pushText: (text: string) => void;
   pushGate: (stepIndex: number) => void;
   pushAction: (run: () => void) => void;
   showEverything: () => void;
   dispose: () => void;
}

/* One reply's display queue. Text and actions flow at once unless a gate is waiting ahead of them.
   showEverything opens every gate now and lets whatever arrives later through without waiting,
   which is what Show all and Stop ask for. */
export function createReplyPacer(handlers: PacerHandlers, clock: PacerClock = SYSTEM_CLOCK): ReplyPacer {
   const queue: QueuedItem[] = [];
   let timer: ReturnType<typeof setTimeout> | null = null;
   let previousGateAt: number | null = null;
   let textSincePreviousGate = "";
   let isPaced = true;
   let wasBusy = false;

   function reportBusy() {
      const isBusy = queue.length > 0;

      if (isBusy !== wasBusy) {
         wasBusy = isBusy;
         handlers.onBusyChange(isBusy);
      }
   }

   function stopTimer() {
      if (timer !== null) {
         clock.clearTimer(timer);
         timer = null;
      }
   }

   function show(text: string) {
      const isFirstText = previousGateAt === null && text.trim() !== "";

      if (isFirstText) {
         previousGateAt = clock.now();
      }

      textSincePreviousGate += text;
      handlers.showText(text);
   }

   function open(stepIndex: number) {
      handlers.openGate(stepIndex);
      previousGateAt = clock.now();
      textSincePreviousGate = "";
   }

   function waitBeforeNextGate() {
      if (previousGateAt === null) {
         return 0;
      }

      const opensAt = previousGateAt + gateDelay(wordsIn(textSincePreviousGate));

      return opensAt - clock.now();
   }

   function drain() {
      stopTimer();

      while (queue.length > 0) {
         const head = queue[0];
         const wait = head.kind === "gate" && isPaced ? waitBeforeNextGate() : 0;

         if (wait > 0) {
            timer = clock.setTimer(drain, wait);
            break;
         }

         queue.shift();

         if (head.kind === "text") {
            show(head.text);
         } else if (head.kind === "gate") {
            open(head.stepIndex);
         } else {
            head.run();
         }
      }

      reportBusy();
   }

   function push(item: QueuedItem) {
      queue.push(item);

      const isWaiting = timer !== null;

      if (!isWaiting) {
         drain();
      } else {
         reportBusy();
      }
   }

   return {
      pushText: (text) => push({ kind: "text", text }),
      pushGate: (stepIndex) => push({ kind: "gate", stepIndex }),
      pushAction: (run) => push({ kind: "action", run }),
      showEverything: () => {
         isPaced = false;
         drain();
      },
      dispose: () => {
         stopTimer();
         queue.length = 0;
         reportBusy();
      }
   };
}
