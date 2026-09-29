import type { AgentScreen } from "../api/types";
import {
   CANNOT_SEE_LINE,
   GUARDRAIL_AFTER_CHECKING,
   GUARDRAIL_BEFORE_CHECKING,
   LINE_ITEM_CHECKED,
   LINE_ITEM_NOT_CHECKED,
   LINE_REVIEW,
   LINE_TIMED_PART,
   LINE_TODAY,
   assessmentsSetupLine,
   lessonLine,
   otherLine,
   progressSkillLine,
   progressTabLine,
   settingsLine
} from "./agentCopy";

/* The panel's context lines, composed on the client from the same screen shape the turn sends
   (docs/agent/design.md, "The context lines"). The shape carries ids only, so the names a line
   reads out (the concept, the skill, the tab) come in labels from the route that knows them, and
   labels are never sent. */

export interface ScreenLabels {
   conceptName?: string | null;
   skillName?: string;
   tabName?: string;
   formatName?: string;
   viewName?: string;
}

export interface ContextLines {
   canSee: string;
   cannotSee: string | null;
   guardrail: string | null;
   fields: string[];
}

function canSeeLine(screen: AgentScreen, labels: ScreenLabels) {
   switch (screen.kind) {
      case "today":
         return LINE_TODAY;
      case "session_item":
         return screen.submitted ? LINE_ITEM_CHECKED : LINE_ITEM_NOT_CHECKED;
      case "session_lesson":
      case "lesson":
         return lessonLine(labels.conceptName ?? null, screen.section_index + 1, screen.section_count);
      case "review":
         return LINE_REVIEW;
      case "progress":
         return screen.skill_id !== undefined ? progressSkillLine(labels.skillName ?? screen.skill_id) : progressTabLine(labels.tabName ?? screen.tab);
      case "assessments":
         return screen.timed === true ? LINE_TIMED_PART : assessmentsSetupLine(labels.formatName ?? screen.format);
      case "settings":
         return settingsLine(labels.tabName ?? screen.tab);
      case "other":
         return otherLine(labels.viewName ?? screen.view);
   }
}

function guardrailLine(screen: AgentScreen) {
   if (screen.kind !== "session_item") {
      return null;
   }

   return screen.submitted ? GUARDRAIL_AFTER_CHECKING : GUARDRAIL_BEFORE_CHECKING;
}

export function contextLinesFor(screen: AgentScreen, labels: ScreenLabels = {}): ContextLines {
   const isUncheckedItem = screen.kind === "session_item" && !screen.submitted;

   return {
      canSee: canSeeLine(screen, labels),
      cannotSee: isUncheckedItem ? CANNOT_SEE_LINE : null,
      guardrail: guardrailLine(screen),
      fields: Object.keys(screen)
   };
}
