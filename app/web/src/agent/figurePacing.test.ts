import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { createReplyPacer, gateDelay, wordsIn } from "./figurePacing";

/* 238 words a minute is 60000 / 238 milliseconds a word. */
const MILLISECONDS_PER_WORD = 60000 / 238;

describe("wordsIn", () => {
   it("counts the words of plain text however it is spaced", () => {
      expect(wordsIn("The left sum uses the height.")).toBe(6);
      expect(wordsIn("  two\nwords  ")).toBe(2);
      expect(wordsIn("")).toBe(0);
      expect(wordsIn("   ")).toBe(0);
   });

   it("counts an inline or a displayed formula as three words, whatever it holds", () => {
      expect(wordsIn("Let \\(x^2 + 1 = y\\) be positive")).toBe(6);
      expect(wordsIn("\\[\\int_0^1 x \\, dx\\] is the area")).toBe(6);
      expect(wordsIn("\\(a\\)\\(b\\)")).toBe(6);
   });
});

describe("gateDelay", () => {
   it("is the reading time at 238 words a minute", () => {
      expect(gateDelay(0)).toBe(0);
      expect(gateDelay(10)).toBeCloseTo(10 * MILLISECONDS_PER_WORD, 6);
      expect(gateDelay(23)).toBeCloseTo(5798.32, 2);
   });

   it("never waits more than six seconds", () => {
      expect(gateDelay(24)).toBe(6000);
      expect(gateDelay(238)).toBe(6000);
   });
});

function recordingPacer() {
   const shown: string[] = [];
   const opened: number[] = [];
   const busy: boolean[] = [];
   const pacer = createReplyPacer({
      showText: (text) => shown.push(text),
      openGate: (stepIndex) => opened.push(stepIndex),
      onBusyChange: (isBusy) => busy.push(isBusy)
   });

   return { pacer, shown, opened, busy };
}

const TEN_WORDS = "One two three four five six seven eight nine ten. ";

const FIVE_WORDS = "One two three four five. ";

describe("createReplyPacer", () => {
   beforeEach(() => {
      vi.useFakeTimers();
   });

   afterEach(() => {
      vi.useRealTimers();
   });

   it("shows text at once when no step waits ahead of it", () => {
      const { pacer, shown, busy } = recordingPacer();

      pacer.pushText("Hello ");
      pacer.pushText("there.");

      expect(shown).toEqual(["Hello ", "there."]);
      expect(busy).toEqual([]);
   });

   it("opens a step at the reading time of the words since the first text, not before, and holds the text behind it", () => {
      const { pacer, shown, opened } = recordingPacer();
      const readingTime = 10 * MILLISECONDS_PER_WORD;

      pacer.pushText(TEN_WORDS);
      vi.advanceTimersByTime(1000);
      pacer.pushGate(0);
      pacer.pushText("After the step.");

      expect(opened).toEqual([]);
      expect(shown).toEqual([TEN_WORDS]);

      vi.advanceTimersByTime(readingTime - 1000 - 1);

      expect(opened).toEqual([]);
      expect(shown).toEqual([TEN_WORDS]);

      vi.advanceTimersByTime(2);

      expect(opened).toEqual([0]);
      expect(shown).toEqual([TEN_WORDS, "After the step."]);
   });

   it("counts the next step from the moment the previous one opened, over the words shown since", () => {
      const { pacer, opened } = recordingPacer();

      pacer.pushGate(0);
      pacer.pushText(FIVE_WORDS);
      pacer.pushGate(1);

      expect(opened).toEqual([0]);

      vi.advanceTimersByTime(5 * MILLISECONDS_PER_WORD - 1);

      expect(opened).toEqual([0]);

      vi.advanceTimersByTime(2);

      expect(opened).toEqual([0, 1]);
   });

   it("opens a step that arrives after its reading time at once", () => {
      const { pacer, opened } = recordingPacer();

      pacer.pushText(FIVE_WORDS);
      vi.advanceTimersByTime(5000);
      pacer.pushGate(0);

      expect(opened).toEqual([0]);
   });

   it("waits no more than six seconds for a step however long the text before it", () => {
      const { pacer, opened } = recordingPacer();

      pacer.pushText(`${TEN_WORDS}${TEN_WORDS}${TEN_WORDS}`);
      pacer.pushGate(0);
      vi.advanceTimersByTime(5999);

      expect(opened).toEqual([]);

      vi.advanceTimersByTime(1);

      expect(opened).toEqual([0]);
   });

   it("holds an action behind a waiting step, and reports itself busy until everything has been shown", () => {
      const { pacer, opened, busy } = recordingPacer();
      const ended = vi.fn();

      pacer.pushText(TEN_WORDS);
      pacer.pushGate(0);
      pacer.pushAction(ended);

      expect(ended).not.toHaveBeenCalled();
      expect(busy).toEqual([true]);

      vi.advanceTimersByTime(6000);

      expect(opened).toEqual([0]);
      expect(ended).toHaveBeenCalledTimes(1);
      expect(busy).toEqual([true, false]);
   });

   it("opens every waiting step at once on showEverything, and lets later steps through without waiting", () => {
      const { pacer, shown, opened, busy } = recordingPacer();

      pacer.pushText(TEN_WORDS);
      pacer.pushGate(0);
      pacer.pushText(TEN_WORDS);
      pacer.pushGate(1);
      pacer.pushText("Last.");
      pacer.showEverything();

      expect(opened).toEqual([0, 1]);
      expect(shown).toEqual([TEN_WORDS, TEN_WORDS, "Last."]);
      expect(busy).toEqual([true, false]);

      pacer.pushGate(2);
      pacer.pushText("After.");

      expect(opened).toEqual([0, 1, 2]);
      expect(shown[shown.length - 1]).toBe("After.");
   });

   it("drops what waits and its timer when disposed", () => {
      const { pacer, shown, opened } = recordingPacer();

      pacer.pushText(TEN_WORDS);
      pacer.pushGate(0);
      pacer.pushText("Never shown.");
      pacer.dispose();
      vi.advanceTimersByTime(6000);

      expect(opened).toEqual([]);
      expect(shown).toEqual([TEN_WORDS]);

      pacer.pushText("Late.");

      expect(opened).toEqual([]);
      expect(shown).not.toContain("Never shown.");
   });
});
