import { describe, expect, it } from "vitest";

import type { AgentScreen } from "../api/types";
import { CHECKED_ITEM, UNCHECKED_ITEM } from "../testing/agent";
import { contextLinesFor, type ScreenLabels } from "./screenLines";

/* docs/agent/design.md, "The context lines": one row per screen shape, in the table's own words. */
const CASES: Array<{ screen: AgentScreen; labels?: ScreenLabels; line: string }> = [
   { screen: { kind: "today" }, line: "Can see: Today, your queue for today." },
   { screen: UNCHECKED_ITEM, line: "Can see: Today, practice item, not checked yet." },
   { screen: CHECKED_ITEM, line: "Can see: Today, practice item, checked, with its feedback and worked solution." },
   {
      screen: { kind: "lesson", lesson_id: "LSN-CON-02013", version: 1, section_id: "LSN-CON-02013#s2", section_index: 1, section_count: 7, return_to: "/lessons" },
      labels: { conceptName: "The product rule" },
      line: "Can see: Lesson, The product rule, part 2 of 7."
   },
   {
      screen: { kind: "session_lesson", session_id: "SES-1", lesson_id: "LSN-CON-02013", version: 1, section_id: "LSN-CON-02013#s1", section_index: 0, section_count: 5 },
      labels: { conceptName: "The product rule" },
      line: "Can see: Lesson, The product rule, part 1 of 5."
   },
   { screen: { kind: "review" }, line: "Can see: Review, your error notes and corrected items." },
   { screen: { kind: "progress", tab: "calibration" }, labels: { tabName: "Calibration" }, line: "Can see: Progress, Calibration." },
   {
      screen: { kind: "progress", tab: "mastery", skill_id: "BC-SKL-00301" },
      labels: { skillName: "Chain rule" },
      line: "Can see: Progress, the skill Chain rule."
   },
   { screen: { kind: "assessments", format: "unit" }, labels: { formatName: "unit check" }, line: "Can see: Assessments, the unit check setup." },
   { screen: { kind: "assessments", format: "mock", timed: true }, line: "Can see: Assessments, a timed part." },
   { screen: { kind: "settings", tab: "tutor" }, labels: { tabName: "Tutor" }, line: "Can see: Settings, the Tutor tab." },
   { screen: { kind: "other", view: "account" }, labels: { viewName: "Account" }, line: "Can see: Account." }
];

describe("the context line", () => {
   for (const entry of CASES) {
      it(`reads "${entry.line}"`, () => {
         expect(contextLinesFor(entry.screen, entry.labels).canSee).toBe(entry.line);
      });
   }

   it("adds the cannot-see line on an unchecked item only", () => {
      const withCannotSee = CASES.filter((entry) => contextLinesFor(entry.screen, entry.labels).cannotSee !== null).map((entry) => entry.screen);

      expect(withCannotSee).toEqual([UNCHECKED_ITEM]);
   });
});
