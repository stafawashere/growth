---
title: Live tutor agent, design
research_date: 2026-09-29
status: draft
purpose: Specify the live tutor agent as the student meets it, from the one entry point to every degraded state, with the copy for each and the rules the copy obeys.
---

# Live tutor agent, design

The agent is a tutor the student can open from any screen with one click or one keystroke. It sees a structured description of what is on the screen, it remembers what the student has told it across sessions, and it is held to the plan 03 guardrail: before an item is checked it never gives the answer and never says whether work in progress is right. The research behind every choice is in `research/synthesis.md`, which ranks the decisions and names the alternatives rejected. This file is the student-facing specification. `architecture.md` is the engineering specification and `build-plan.md` schedules the work.

Minimal and convenient are the standards. Nothing in the panel animates a wait, awards anything, or labels itself as machine-made. Every line of copy below obeys plan 08's Interface writing: plain verbs in the student's voice, informational and never praise, no study advice, no schedule, no quota, no prediction about the exam, no exclamation mark, no em dash.

## The entry point [inferred]

One text button, "Ask", with the existing `question` icon, sits in the top bar's right cluster immediately left of the avatar, at every width. It is a disclosure button: `aria-expanded` reflects the panel, `aria-controls` names it, and its accessible name is "Ask, Ctrl+/" (or "Cmd+/" on macOS). It is present on every screen while signed in. On a timed part (a mock, a drill or a timed unit check) it stays visible and is disabled with a visible reason under it: "Not available during a timed part."

The keyboard shortcut is Ctrl+/ on Windows and Linux and Cmd+/ on macOS. It carries a modifier, so WCAG 2.1.4 does not apply and it cannot fire the session screen's single-key handlers. From anywhere with the panel closed it opens the panel and puts focus in the composer. With the panel open and focus elsewhere it moves focus to the composer. With focus inside the panel it closes the panel and returns focus to where it came from. The listener runs on `window` in the capture phase so it works while a MathLive field has focus.

Rejected: a floating bubble at the bottom right, because that corner holds the AI notices and, on a phone, the tab bar. Rejected: an entry point inside each screen, which would multiply focus-return cases and break "one entry point".

## The panel [inferred]

On desktop (1100 px and wider) the panel is an `aside` labelled "Tutor", a sibling of `main`, docked to the right below the top bar, full remaining height, 384 px wide. The page column reflows into the remaining width, so the panel covers nothing and the item stays whole. From 900 to 1099 px the panel is 320 px. Both the panel and the page scroll on their own. It is a disclosure region, not a dialog: no focus trap, no scrim, Tab moves out of it into the page.

Under 900 px the panel is a bottom sheet with no scrim, at most 640 px wide. It has three heights: collapsed (a 56 px bar showing "Tutor" and the first line of the last reply), half (half the dynamic viewport, the default on open), and full (the viewport minus the top bar). A row of text buttons, "Show the item", "Full height" and "Close", does everything a drag would, and `main` gains bottom padding equal to the sheet's height so every control on the item can scroll above it. "Show the item" collapses the sheet without losing the conversation.

The panel has, from the top: the header line "Tutor" with a close control; the context lines; the guardrail line on a practice item; the conversation; and the composer with a Send button and, while a reply streams, a Stop button.

Desktop, an unchecked practice item, panel open:

```
+--------------------------------------------------------------------------------------+
| Growth   Today  Lessons  Review  Progress  Assessments             [? Ask]  (M) v    |
+------------------------------------------------------+-------------------------------+
|                                                      | Tutor                   [x]   |
|  Evaluate the limit of (x^2 - x - 6)/(x^2 - 9)       | Can see: Today, practice      |
|  as x approaches 3.                                  | item, not checked yet.        |
|                                                      | Cannot see: your answer or    |
|  ( ) A   0                                           | the answer key.               |
|  ( ) B   5/6                                         | > What it can see             |
|  ( ) C   1                                           |                               |
|  ( ) D   does not exist                              | Until you check your answer,  |
|                                                      | this tutor will not give it.  |
|                                                      | Tell it what you tried and it |
|                              [ Check my answer ]     | will ask you a question back. |
|                                                      |                               |
|                                                      | You said                      |
|                                                      | I plugged in 3 and got 0/0.   |
|                                                      |                               |
|                                                      | Tutor said                    |
|                                                      | What does 0/0 tell you about  |
|                                                      | the form of this limit, and   |
|                                                      | what could you do to the      |
|                                                      | fraction before substituting? |
|                                                      |                               |
|                                                      | [ composer                  ] |
|                                                      | [Send]      Ctrl+/ to close   |
+------------------------------------------------------+-------------------------------+
```

Phone, the same item, sheet at half height:

```
+--------------------------------+
| Growth              [? Ask] (M)|
+--------------------------------+
|  Evaluate the limit of         |
|  (x^2 - x - 6)/(x^2 - 9)       |
|  as x approaches 3.            |
|  ( ) A  0      ( ) B  5/6      |
|  ( ) C  1      ( ) D  none     |
|          [ Check my answer ]   |
|                                |
+--------------------------------+
| Tutor        Show the item     |
|              Full height  Close|
| Can see: Today, practice item, |
| not checked yet.               |
| Cannot see: your answer or the |
| answer key.                    |
| Until you check your answer,   |
| this tutor will not give it.   |
| ...                            |
| [ composer          ] [Send]   |
+--------------------------------+
```

## The context lines [inferred]

The second line of the header always reads "Can see: {screen}, {object}, {state}." and is rebuilt from the structured state the client sends with every turn. On an unchecked practice item a third line reads "Cannot see: your answer or the answer key." A disclosure "What it can see" opens a plain list of the fields sent, in the way a code assistant lists the references it used. The line updates when the screen changes while the panel is open, and the change is announced once through the status region.

| Screen | Line |
| --- | --- |
| Today, no session open | Can see: Today, your queue for today. |
| A practice item before checking | Can see: Today, practice item, not checked yet. Cannot see: your answer or the answer key. |
| The same item after checking | Can see: Today, practice item, checked, with its feedback and worked solution. |
| A lesson in a session or the library | Can see: Lesson, {concept name}, part {n} of {total}. |
| Review | Can see: Review, your error notes and corrected items. |
| Progress, a tab | Can see: Progress, {tab name}. |
| Progress, a skill opened | Can see: Progress, the skill {skill name}. |
| Assessments, before starting | Can see: Assessments, the {format} setup. |
| Settings | Can see: Settings, the {tab} tab. |

"Item 3 of 12" is not shown, because the client has no set position today. It returns only if the session payload gains one.

## What the tutor does and does not do [inferred]

Before an item is checked, the tutor restates what the item asks, names the representation the givens use, asks what the student has tried, offers the next question the student could ask themselves, names the rule that governs the step after the student has answered a question, and points to a lesson section by name. It never states or bounds the final answer, never says whether the student's current work is right, never names a distractor or an error pattern for this item, never names a misconception as the student's, and never writes the next line of the solution. Its first reply on an item opens with a question. After one unanswered turn it may name a rule or point to a lesson section. It stops offering new help on an item at the per-item ceiling of 3 turns and says so: "That is the third question on this item. Check your answer when you are ready, and we can go through it after."

After an item is checked, the tutor can discuss the answer and the worked solution at the level of the step the response missed: which point was not earned and what the earning condition says, what the correct response showed at that step, and one question that asks the student to name the rule that justifies the step. It stays at that step unless the student asks about another part, and it never asserts a misconception; the most it does is ask the discriminating question.

On a lesson, Review, Progress or Assessments screen there is no item and no key, so the tutor answers questions about the concept on screen, explains a lesson section in other words, or says where a thing is in the app. It never writes a plan for the student, never sets a schedule or a quota, and never predicts what the exam will hold. If asked about the exam it cites the exam-structure record and states nothing from memory.

In every reply the tutor speaks in AP scoring language: it names the function a reason must name, says which point is earned or not in rubric terms, asks for units where a rate is asked, and talks about the work and never about the student.

## Streaming [inferred]

The student's message appears in the conversation at once and focus stays in the composer. Below it a static line in muted text reads "Writing a reply" until the first sentence arrives. There is no spinner, no pulsing dots, no shimmer and no caret. Text is added as it arrives, sentence by sentence, with no animation. A "Stop" text button is focusable for the whole stream. When the reply finishes, a visually hidden status region that exists from the first render announces the whole reply once, and "Reply stopped" if the student stopped it. The reply element carries `aria-busy` while text arrives.

Mathematics in a reply is written by the tutor as `\( ... \)` inline and `\[ ... \]` displayed, and rendered through the existing MathText path with KaTeX in its untrusted configuration. Text after an unclosed `\(` is held back until the closing delimiter arrives, so raw LaTeX never flashes. A formula KaTeX rejects renders as its accessible text, never as an error message. Model output is never rendered as Markdown or HTML.

## Memory in settings [inferred]

Settings gains a tab, "Tutor", with three sections.

"What the tutor remembers" lists every active memory entry grouped by kind, in plain words, each with the date of the conversation it came from and a "Forget this" control. Entries the student can edit (preferences and confusions in their own words) have an "Edit" control. A "Forget everything" control sits behind a typed confirmation, "forget everything", and removes every entry and every stored conversation. A switch, "Pause memory", stops the tutor from saving new entries and from reading existing ones, and leaves the entries in place.

The kinds, as the page names them: "How you like to be helped" (preferences), "Confusions in your words", "What you said was hard", and "Last conversation" (the episode summary).

"Conversations" lists the stored conversations of the last 30 days by date and screen, each openable and each with a "Delete" control. A line under the heading says: "Conversations are kept for 30 days so you can read them here, then deleted."

"How the tutor is tuned to you" shows the tutoring profile when the `tutor_profile` experiment switch is on: each field, its current value in words, where it came from and how many conversations support it. When the switch is off the section says "Off. The operator can turn it on under Operator." Requests the student has made that the tutor cannot follow ("wants the answer before checking") are shown here as recorded and not applied.

Every deletion writes an audit entry without the deleted text. The export archive includes every entry, every conversation and the profile, and the purge removes them all.

## The empty state and the degraded states [inferred]

Every state keeps whatever the student has typed in the composer. In a degraded state the Send button is disabled and the reason is written next to it, not hidden in a tooltip.

| State | Copy |
| --- | --- |
| Empty, on an unchecked item | Ask about this item. It will ask what you have tried before it explains anything. This conversation is kept for 30 days and you can read or delete it in Settings. |
| Empty, on any other screen | Ask about what is on this screen. This conversation is kept for 30 days and you can read or delete it in Settings. |
| Usage limit, reset time known | The tutor cannot answer right now because the account's Claude usage limit has been reached. It will answer again after {time}. Practice is not affected. |
| Usage limit, reset time unknown | The tutor cannot answer right now because the account's Claude usage limit has been reached. It will answer again when the limit resets. Practice is not affected. |
| Daily cap | The tutor has used today's allowance and is unavailable for the rest of today. Practice is not affected. |
| Minute cap | The tutor is answering too many questions at once. Wait a moment and send again. |
| Sign-in expired | The tutor cannot answer because the Claude sign-in on this computer has expired. Practice is not affected. |
| Offline or no reply within 15 seconds | No connection to the tutor right now. What you typed is kept here. |
| A reply the screen withheld | That reply would have given away part of the answer, so it was not shown. Check your answer when you are ready, and we can go through it after. |
| Third turn on one item | That is the third question on this item. Check your answer when you are ready, and we can go through it after. |
| Timed part | Not available during a timed part. |
| Twentieth turn in one conversation | This conversation has reached 20 questions. Close it and open a new one to keep asking. |
| The screen sent something the server could not use | The tutor could not use what this screen sent. Reload the page and send again. |

The offline and limit states do not queue the question for later. A reply written for a screen the student has left would carry stale context, and the queue would store the student's words in the jobs table.

## Keyboard and motion [inferred]

Ctrl+/ or Cmd+/ opens the panel and focuses the composer. Enter sends and Shift+Enter adds a line. Enter in the composer cannot commit an item, because the session screen already ignores keys typed in a textarea. Tab moves from the composer to Stop while streaming, then to the "What it can see" disclosure and the conversation, then out of the panel into the page, with no trap. Escape anywhere in the panel closes it and returns focus to the element that had it before the panel opened, or to the Ask button if that element is gone.

The desktop panel opens and closes with no transition, because a keystroke opens it and plan 08 removes animation from keyboard-triggered actions. The phone sheet slides in over 300 ms ease-out on transform and opacity, and under reduced motion only the opacity transition runs. Streamed text, the "Writing a reply" line and the status announcement never animate.

While the panel is open, AI notices for the agent role are not shown, because the panel already discloses the call. Notices for other roles keep appearing.

## Dark mode and phone width [inferred]

The panel uses the same design tokens as every other surface, so it follows the theme with no additional colour. Boundaries are the tint-ramp ring shadows the redesign uses for hairlines. Under 900 px the sheet replaces the side panel as described above. At 600 px and under the top bar keeps the Ask button, and the sheet covers the bottom tab bar while open.
