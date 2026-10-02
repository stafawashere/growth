/* Every string the tutor panel and the Tutor settings tab show, copied from docs/agent/design.md
   (the context lines table, the empty and degraded states table, Memory in settings) and, for the
   guardrail lines, from docs/agent/research/live-assistant-ux.md "What this means for Growth",
   point 1. The panel and the tests read these exports, so a copy change is made once, here. */

export const PANEL_TITLE = "Tutor";

export const ASK_LABEL = "Ask";

export const CLOSE_LABEL = "Close";

export const SHOW_ITEM_LABEL = "Show the item";

export const FULL_HEIGHT_LABEL = "Full height";

export const SEND_LABEL = "Send";

export const STOP_LABEL = "Stop";

export const WRITING_A_REPLY = "Writing a reply";

export const REPLY_STOPPED = "Reply stopped";

export const YOU_SAID = "You said";

export const TUTOR_SAID = "Tutor said";

export const WHAT_IT_CAN_SEE = "What it can see";

export const COMPOSER_LABEL = "Message to the tutor";

export const CANNOT_SEE_LINE = "Cannot see: your answer or the answer key.";

export const GUARDRAIL_BEFORE_CHECKING =
   "Until you check your answer, this tutor will not give it. Tell it what you tried and it will ask you a question back.";

export const GUARDRAIL_AFTER_CHECKING = "You have checked this item. You can ask about the answer and the worked solution.";

export const LINE_TODAY = "Can see: Today, your queue for today.";

export const LINE_ITEM_NOT_CHECKED = "Can see: Today, practice item, not checked yet.";

export const LINE_ITEM_CHECKED = "Can see: Today, practice item, checked, with its feedback and worked solution.";

export const LINE_REVIEW = "Can see: Review, your error notes and corrected items.";

export const LINE_TIMED_PART = "Can see: Assessments, a timed part.";

export function lessonLine(conceptName: string | null, part: number, total: number) {
   const hasName = conceptName !== null && conceptName.trim() !== "";

   return hasName ? `Can see: Lesson, ${conceptName}, part ${part} of ${total}.` : `Can see: Lesson, part ${part} of ${total}.`;
}

export function progressTabLine(tabName: string) {
   return `Can see: Progress, ${tabName}.`;
}

export function progressSkillLine(skillName: string) {
   return `Can see: Progress, the skill ${skillName}.`;
}

export function assessmentsSetupLine(formatName: string) {
   return `Can see: Assessments, the ${formatName} setup.`;
}

export function settingsLine(tabName: string) {
   return `Can see: Settings, the ${tabName} tab.`;
}

export function otherLine(viewName: string) {
   return `Can see: ${viewName}.`;
}

export const EMPTY_ON_ITEM =
   "Ask about this item. It will ask what you have tried before it explains anything. This conversation is kept for 30 days and you can read or delete it in Settings.";

export const EMPTY_ELSEWHERE = "Ask about what is on this screen. This conversation is kept for 30 days and you can read or delete it in Settings.";

export function usageLimitUntil(time: string) {
   return `The tutor cannot answer right now because the account's Claude usage limit has been reached. It will answer again after ${time}. Practice is not affected.`;
}

export const USAGE_LIMIT_UNKNOWN_RESET =
   "The tutor cannot answer right now because the account's Claude usage limit has been reached. It will answer again when the limit resets. Practice is not affected.";

export const DAILY_CAP = "The tutor has used today's allowance and is unavailable for the rest of today. Practice is not affected.";

export const MINUTE_CAP = "The tutor is answering too many questions at once. Wait a moment and send again.";

export const SIGN_IN_EXPIRED = "The tutor cannot answer because the Claude sign-in on this computer has expired. Practice is not affected.";

export const OFFLINE = "No connection to the tutor right now. What you typed is kept here.";

export const WITHHELD = "That reply would have given away part of the answer, so it was not shown. Check your answer when you are ready, and we can go through it after.";

export const THIRD_TURN_CEILING = "That is the third question on this item. Check your answer when you are ready, and we can go through it after.";

export const TIMED_PART = "Not available during a timed part.";

export const CONVERSATION_CEILING = "This conversation has reached 20 questions. Close it and open a new one to keep asking.";

export const SCREEN_REFUSED = "The tutor could not use what this screen sent. Reload the page and send again.";

/* A figure in a reply, from docs/agent/drawing-design.md "States and copy" and "What the student
   sees". */

export const DRAWING_A_FIGURE = "Drawing a figure";

export const FIGURE_REFUSED = "The figure for this reply could not be drawn.";

export const PREVIOUS_STEP_LABEL = "Previous";

export const NEXT_STEP_LABEL = "Next";

export const SHOW_ALL_LABEL = "Show all";

export const STEPS_LABEL = "Steps";

export const CURRENT_STEP_WORD = "now";

export function stepLine(step: number, total: number, caption: string) {
   return `Step ${step} of ${total}: ${caption}`;
}

export function figureAnnouncement(title: string, description: string) {
   return `Figure: ${title}. ${description}`;
}

/* The art board, from docs/agent/drawing-design.md "The art board". The visible words of the
   board's buttons begin their accessible names, which say which board or figure they act on. */

export const ART_BOARD_TITLE = "Art board";

export function figureOnTheBoard(title: string) {
   return `Figure on the board: ${title}`;
}

export const SHOW_ON_THE_BOARD = "Show on the board";

export function boardFigureCount(figure: number, total: number) {
   return `Figure ${figure} of ${total}`;
}

export const PREVIOUS_FIGURE_LABEL = "Previous figure";

export const NEXT_FIGURE_LABEL = "Next figure";

export const MINIMIZE_LABEL = "Minimize";

export const MINIMIZE_BOARD_LABEL = "Minimize the art board";

export const RESTORE_LABEL = "Restore";

export const RESTORE_BOARD_LABEL = "Restore the art board";

export const CLOSE_BOARD_LABEL = "Close the art board";

export const TALLER_LABEL = "Taller";

export const SHORTER_LABEL = "Shorter";

export const MOVE_BOARD_LABEL = "Move the art board";

export const MOVE_LABEL = "Move";

export const MOVE_TO_NEXT_CORNER_LABEL = "Move the art board to the next corner";

export const SIZE_LABEL = "Size";

export const CHANGE_SIZE_LABEL = "Change the art board's size";

export const MOVE_BOARD_HINT = "Arrow keys move the board. Hold Shift to move it further.";

export const RESIZE_BOARD_LABEL = "Resize the art board";

export const RESIZE_BOARD_HINT = "Arrow keys resize the board. Hold Shift to resize it further.";

export function minimizedBoard(title: string) {
   return `${ART_BOARD_TITLE}: ${title}`;
}

/* Marks on the page, from docs/agent/drawing-design.md "Marks on the page", "What the student
   sees". */

export const MARKED_ON_THE_PAGE = "Marked on the page";

export const CLEAR_MARKS = "Clear marks";

export const MARKS_REFUSED = "The marks on the page for this reply could not be drawn.";

export function marksAnnouncement(description: string) {
   return `Marks on the page: ${description}`;
}

export function shortcutName(isMac: boolean) {
   return isMac ? "Cmd+/" : "Ctrl+/";
}

export function askAccessibleName(isMac: boolean) {
   return `${ASK_LABEL}, ${shortcutName(isMac)}`;
}

export function closeHint(isMac: boolean) {
   return `${shortcutName(isMac)} to close`;
}

/* The Tutor tab in Settings. */

export const SETTINGS_TAB_LABEL = "Tutor";

export const MEMORY_HEADING = "What the tutor remembers";

export const CONVERSATIONS_HEADING = "Conversations";

export const PROFILE_HEADING = "How the tutor is tuned to you";

export const MEMORY_KIND_LABELS = {
   preference: "How you like to be helped",
   confusion: "Confusions in your words",
   stated_difficulty: "What you said was hard",
   episode: "Last conversation"
} as const;

export const FORGET_THIS = "Forget this";

export const EDIT_LABEL = "Edit";

export const SAVE_LABEL = "Save";

export const CANCEL_LABEL = "Cancel";

export const FORGET_EVERYTHING = "Forget everything";

export const FORGET_EVERYTHING_PHRASE = "forget everything";

export const PAUSE_MEMORY = "Pause memory";

export const OPEN_LABEL = "Open";

export const DELETE_LABEL = "Delete";

export const RETENTION_LINE = "Conversations are kept for 30 days so you can read them here, then deleted.";

export const PROFILE_OFF = "Off. The operator can turn it on under Operator.";
