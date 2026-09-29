---
title: Live tutor panel, entry point, geometry, streaming and anti-answer design
research_date: 2026-09-29
status: draft
purpose: Record how shipped in-product assistants stay one click away without covering the work, and turn that evidence plus Growth's own design rules into a concrete panel design for the live tutor.
---

# Live tutor panel UX

This file covers one strand of the live tutor feature. It studies how shipped assistants are entered, where they sit, how they say what they can see, how they stream, how they render mathematics and how they avoid handing over answers. It then applies that evidence to Growth's client under `app/web`. Every web claim carries its URL and the access date 2026-09-29. Several primary pages refused automated fetches (Khan Academy's help centre, PubMed, PNAS, SSRN, OpenAI's help centre, Mozilla's support site, and the rendered Material 3 site), and each place that affected a claim says so.

## Constraints that stand regardless of the evidence [inferred]

These are ground rules of the feature, restated so the recommendations below can be checked against them. They are not argued here.

- The tutor role is never routed to claudebox, and the single-user rule of the subscription backend holds.
- No student-written text reaches a system prompt. Every field substitutes below the prompt-variables marker in `app/providers/base.py` `render_template`, untrusted fields are JSON-encoded into the user message, and untrusted output is screened (plan 13 Safety).
- No tool definitions go to the model by default. Context is composed by the application.
- Plan 03 guardrail. During practice the tutor never states the answer, never receives the student's unsubmitted answer or the key, never evaluates in-progress work on an unsupported or exam-shaped item, and asks before it tells. Worked solutions reach it only after submission. Nothing the tutor says or the student types writes mastery evidence.
- No study advice, schedules, quotas, praise copy or exam prediction talk in any template or interface copy.
- Screen context is structured application state, never a screenshot, and it excludes the draft answer and every key. Every new datum gets a retention row, purge and export cover it, and the student can view and delete it (plan 09).
- Every tutor call goes through `app/providers/guard.py` and the tutor's own pacing caps.

## What Growth's client and plan already fix [verified]

Read directly from the repository on 2026-09-29. The repository is the primary source for these facts.

Top bar. `app/web/src/shell/TopBar.tsx` renders the brand "Growth", a `nav` labelled "Main" with five tabs (Today, Lessons, Review, Progress, Assessments), and a `menu` slot that holds `AccountMenu`. In `app/web/src/styles/app.css` the bar is 56 px tall (`calc(var(--growth-space-8) * 7)`), capped at 1124 px wide (`calc(var(--growth-space-4) * 281)`), and `.account-menu` carries `margin-left: auto`, so everything after the tabs sits at the right edge. Under 600 px the tabs move to a fixed bottom bar 56 px tall, and the top bar keeps only the brand and the avatar. The page column `.app-page` has the same 1124 px cap. Breakpoints in use are 1100, 900 and 600 px.

Menus and dialogs. `app/web/src/shell/AccountMenu.tsx` is a disclosure. Its trigger has `aria-expanded` and `aria-controls`, focus moves to the first item on open, and Escape closes it and returns focus to the trigger. `app/web/src/ui/Dialog.tsx` wraps the native `dialog` element with `showModal`, returns focus to the opener, and its comment cites 08's rule that a focus trap is allowed only inside a modal that Escape closes. There is no drawer, side sheet or bottom sheet primitive in `app.css`. The closest precedent is `.graphing-panel`, which from 1100 px sits beside the question and widens the part to 1152 px.

Motion. `app/web/src/styles/motion.css` holds every transition. Each is 300 ms ease-out on `transform` and `opacity`, the keyboard-triggered classes are `transition: none`, and under `prefers-reduced-motion: reduce` the transform is neutralised while the opacity transition stays. `app.css` says in its header that nothing in it animates.

Mathematics. `app/web/src/math/MathText.tsx` splits text on `\(` and `\)` only (`INLINE_MATH` in `app/web/src/math/mathjson.ts`), renders each formula with KaTeX through `renderLatexToMarkup`, inserts the markup with `dangerouslySetInnerHTML`, and falls back to an ASCII reading when KaTeX returns nothing. `renderLatexToMarkup` sets `throwOnError: false`, `output: "htmlAndMathml"` and one macro (`\lim` with stacked limits). It does not set `trust`, `maxExpand`, `maxSize` or `strict`, so KaTeX's defaults apply. The installed KaTeX is 0.16.47 (`app/web/node_modules/katex/package.json`). Formulas longer than 60 characters get their own line.

AI notices. `app/web/src/notices/AiNotices.tsx` polls `GET /notices` every 5 s and shows each new AI call as a toast in a `role="status"` `aria-live="polite"` stack, fixed 24 px from the bottom right (`.ai-notices` in `app.css`), for 8 s. Every tutor call would therefore raise a toast in the corner where a side panel or a bottom sheet would sit.

Existing keys. `SessionScreen.tsx` and `PartRunner.tsx` listen on `document` for single-character keys (1, 2, 3 for confidence, Enter to commit or advance, option letters, N and P between questions). Both ignore any event with Alt, Ctrl or Meta held, and both ignore events whose target is a `textarea`, `select` or text `input`. A modified shortcut therefore cannot collide with them, and typing in a panel textarea cannot trigger them.

Plan 08. The Motion rules keep every animation under about 300 ms with ease-out, animate only `transform` and `opacity`, and remove animation from anything triggered by a repeated keystroke. Reduced motion means replace with a cross-fade, never delete. There is no skeleton shimmer or entrance animation. Interface writing uses plain verbs in the student's voice, informational feedback without praise, and no copy that labels output as machine-generated ("AI-powered", sparkle or robot icons). It also says the tutor's refusal is written as a next step, not a refusal notice. The Anti-pattern list bans sparkle and robot iconography, emoji, and "Chat-first layout for tutoring". The Point of view says there is no chat box beside an unsolved problem. The Accessibility section makes keyboard-first the primary model and allows a focus trap only inside a modal that Escape dismisses. `docs/plan/03-diagnosis-and-feedback.md` line 336 says a guardrailed tutor is available beside a practice item. Plan 07's cap table says that at the cap the tutor stops for the day and the student sees that "the tutor is unavailable for the rest of today, with the practice queue unaffected". Plan 09 says model output is rendered as text or KaTeX only, never inserted as HTML, with KaTeX "rendered with untrusted input settings, meaning macro expansion and any command that can emit raw HTML are disabled".

`docs/operator/ui-redesign.md` records that the client has no set position to show, which is why "Set 1 of 3, item 1" was not taken from the prototype. A context line that says "item 3 of 12" therefore needs data the client does not have today.

## Khanmigo [single-source]

Entry point and placement. A search result from Khan Academy's help article on where to find Khanmigo says the Khanmigo icon sits at the bottom right of content pages and opens the conversation window (https://support.khanacademy.org/hc/en-us/articles/13982530363533-Where-can-I-access-Khanmigo-while-working-on-Khan-Academy, accessed 2026-09-29, the page itself returned 403, so this rests on the search summary). Khan's student course describes Khanmigo as working on the side of an exercise, video or article, and also offers a separate "Tutor me: Math and Science" activity (https://www.khanacademy.org/college-careers-more/khanmigo-for-students/x5443352261243283:introducing-khanmigo/x5443352261243283:learning-with-khanmigo/v/khanmigo-for-students-how-to-use-math-or-science-tutoring-on-khanmigo, accessed 2026-09-29, the page body did not load, so this also rests on the search summary). Whether the panel covers the exercise could not be established from a primary page, so it is unknown here.

Refusing answers. The learner page says Khanmigo "never gives you the answer" and guides learners to find it themselves (https://www.khanmigo.ai/learners, accessed 2026-09-29).

What it sees. Khan's March 2025 engineering post says accuracy improved when Khanmigo had the exercise's human-written steps, hints and solutions before it evaluated anything, that the architecture was changed so it always gathers that context first, and that Khan generated textual descriptions of all graphics so Khanmigo can "see" what the learner sees by reading text (https://blog.khanacademy.org/khanmigo-math-computation-and-tutoring-updates/, accessed 2026-09-29). This is the same approach Growth takes (structured state rather than screenshots). No primary page found shows Khanmigo telling the student what it can see in the interface.

Parent and teacher visibility. Search summaries of Khan's help articles say every child with access is told that chat history is visible to parents and, where applicable, teachers and administrators, that teachers see chat history in the roster, and that moderation flags send an email and an in-app notice to the linked adult (https://support.khanacademy.org/hc/en-us/articles/14394814244365-What-safety-features-does-Khanmigo-have and https://support.khanacademy.org/hc/en-us/articles/15127248640525-How-do-I-view-my-students-Khanmigo-chat-history, accessed 2026-09-29, both returned 403 to a direct fetch).

Failure modes. EdWeek reports that a February 2024 Wall Street Journal test found Khanmigo "regularly struggled with basic computation" and that Khan then routed numerical problems to a calculator (https://www.edweek.org/teaching-learning/ai-gets-math-wrong-sometimes-how-teachers-deal-with-its-shortcomings/2024/09, accessed 2026-09-29). Dan Meyer's February 2024 critique shows Khanmigo asking a student for a y-intercept the student had already given, and attributes this to the prompt not carrying the student's answer, so it could not acknowledge what was partly right (https://danmeyer.substack.com/p/khanmigo-doesnt-love-kids, accessed 2026-09-29). Khan's May 2026 research post reports that restricting the maths agent to the maths the student had already done, rather than also working out the remaining steps, cut answer-giving by 50 percent, and that a summary of recent problem-solving history raised correctness by 3.4 percent (https://blog.khanacademy.org/how-khan-academy-is-building-a-better-ai-tutor-our-most-recent-learnings/, accessed 2026-09-29).

## Duolingo Max, Explain My Answer and Roleplay [single-source]

Entry point and timing. Duolingo's post announcing that Explain My Answer is free says a button appears after exercises, on correct and incorrect answers, and that the learner chooses whether to open it (https://blog.duolingo.com/explain-my-answer-now-free, accessed 2026-09-29). The 2023 product manager interview quotes Duolingo sending the model context of the form "Here's what they got wrong" (https://www.techlearning.com/how-to/what-is-duolingo-max-the-gpt-4-powered-learning-tool-explained-by-the-apps-product-manager, accessed 2026-09-29). The assistant therefore exists only after the answer is committed, which removes the answer-machine risk by construction rather than by prompt.

Roleplay. Duolingo's Max post says humans write the Roleplay scenarios, the model gives feedback on accuracy and complexity afterwards, and a learner can report a wrong message by holding it down (https://blog.duolingo.com/duolingo-max/, accessed 2026-09-29).

What it does badly. A January 2025 review says Explain My Answer "still has a tendency to be wrong" and sometimes does not explain the part of the answer the learner wanted, and that early Roleplay scenarios are too hard for beginners (https://duoplanet.com/duolingo-max-review/, accessed 2026-09-29).

Mathematics rendering, keyboard access and reduced motion are not applicable or not documented for this product.

## Brilliant and Koji [single-source]

Brilliant's help centre says Koji "sees what you are working on" and walks through the thinking step by step "without giving the answer", and that a learner can ask Koji a question from the Home tab and be routed to the relevant lesson (https://brilliant.org/help/features/, accessed 2026-09-29). Search summaries describe Koji drawing on the lesson and giving hints, and describe a hint button on each lesson problem with scaffolding removed in practice sets, but those rest on secondary pages (https://beginnersinai.org/brilliant-explained/, accessed 2026-09-29) and were not confirmed on a Brilliant page. How Koji's surface is placed, whether it covers the problem, and how it renders mathematics are unknown here.

## Photomath [single-source]

Photomath's App Store listing says a "step-by-step explanation (and answer!) instantly appears" after the camera scans a problem, and sells Animated Steps and paid tutorials (https://apps.apple.com/us/app/photomath/id919087726, accessed 2026-09-29). Google's help overview says images go to cloud servers where a neural network reads the formula and a solving algorithm produces the solution and steps, and that the paid tier adds hints for when the learner is stuck (https://support.google.com/photomath/answer/14328660?hl=en, accessed 2026-09-29).

The design point is that the answer is the first thing produced and the steps explain it afterwards. Nothing in the flow asks what the learner tried. That makes it an answer machine regardless of how good the steps are. No peer-reviewed study of Photomath's learning effect was found in this session. The closest evidence is the Bastani field experiment recorded in `docs/plan/08-design-brief.md` and `docs/plan/03-diagnosis-and-feedback.md`, where unguarded chat gained 48 percent during assisted practice and lost 17 percent against control on the unassisted exam. PubMed, PNAS and SSRN all refused automated fetches in this session, so those figures are carried from the plan's record, not re-read.

## GitHub Copilot Chat in VS Code [single-source]

Entry points. The Chat view opens with Ctrl+Alt+I (Cmd+Ctrl+I on macOS), inline chat with Ctrl+I (Cmd+I), and Quick Chat with Ctrl+Shift+Alt+L (https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features, accessed 2026-09-29). Inline chat opens inside the editor at the code and shows its result as a diff with Keep and Undo, and Quick Chat opens at the top of the editor for short questions (https://code.visualstudio.com/docs/copilot/chat/inline-chat, accessed 2026-09-29). The three surfaces trade coverage against context. The Chat view sits beside the code, and inline chat overlays the code it is about.

Context indicators. The active file, the selection and the file name are sent implicitly, and the user adds context by typing `#` followed by a file, folder, symbol, terminal output or tool (https://code.visualstudio.com/docs/copilot/chat/copilot-chat and https://code.visualstudio.com/docs/chat/copilot-chat-context, accessed 2026-09-29). The context page describes an expandable "used N references" list under a response that shows which items were actually consulted (same URL). The two-level disclosure is the pattern worth copying: a short always-visible line, and an expandable exact list.

Mathematics. VS Code 1.103 (July 2025) added KaTeX rendering of `$...$` and `$$...$$` in chat behind `chat.math.enabled`, off by default, and 1.104 made it generally available and on by default (https://code.visualstudio.com/updates/v1_103 and https://code.visualstudio.com/updates/v1_104, accessed 2026-09-29).

Accessibility. The Accessible View (Alt+F2) covers chat responses so they can be read line by line (https://code.visualstudio.com/docs/configure/accessibility/accessibility, accessed 2026-09-29). VS Code has audio signals for chat request sent, response pending and response received, and an issue dated 7 February 2025 reports the pending cue timing out on long sessions (https://github.com/microsoft/vscode/issues/239996, accessed 2026-09-29).

What it does badly. The timed-out pending cue is one. Another is that the implicit context is easy to miss, which is why the context page has to teach it. Whether the Chat view follows `prefers-reduced-motion` is not documented on the pages read.

## Cursor [single-source]

Cursor's shortcut page lists Cmd+I and Cmd+L as "Toggle Sidepanel", Cmd+E to toggle the agent layout, Cmd+K for inline edit, and Cmd+Shift+L to add the selection to chat (https://cursor.com/docs/configuration/kbd, accessed 2026-09-29). The agent overview places the agent in the side pane, creates checkpoints before significant changes, and notes that restoring a checkpoint reverts files but not messages (https://cursor.com/docs/agent/overview, accessed 2026-09-29). Context is attached by typing `@` for files, folders, terminals, earlier chats, diffs or the built-in browser (https://cursor.com/help/customization/context, accessed 2026-09-29).

Mathematics. A forum request dated 30 June 2025 asks Cursor to render `$` math with KaTeX in chat to match VS Code, and related threads report LaTeX rendering failures into 2026 (https://forum.cursor.com/t/align-chat-rendering-with-vscodes-katex-support/111053, accessed 2026-09-29). Whether Cursor renders LaTeX in chat today is unknown here.

## Claude and ChatGPT canvas [uncertain]

A search summary of Anthropic's August 2024 post says Claude added LaTeX rendering in chat as a feature preview (https://x.com/AnthropicAI/status/1826667671364272301, accessed 2026-09-29, not fetched directly). ChatGPT canvas opened a window on the right of the chat. An OpenAI community thread from December 2024 records users asking how to stop canvas opening by itself, with no staff answer (https://community.openai.com/t/canvas-opens-automatically-how-to-prevent-that/1055091, accessed 2026-09-29). OpenAI's help article returned 403. A secondary site claims the canvas panel was removed in May 2026 (https://www.ai-toolbox.co/chatgpt-management-and-productivity/how-to-use-chatgpt-canvas-guide-2026, accessed 2026-09-29), which was not confirmed on an OpenAI page. The one usable lesson is that a panel the system opens without being asked is a complaint, not a feature.

## Comparison across the products [inferred]

Built from the sections above. "Unknown" means no primary page read in this session settled it.

| Product | Entry point | Covers the work | Says what it sees | Maths in chat | Answer-machine control |
| --- | --- | --- | --- | --- | --- |
| Khanmigo | Icon at the bottom right of a content page | Unknown | Not shown to the student, context gathered server-side | Unknown | Prompt policy, calculator for arithmetic, later restricted to work already done |
| Duolingo Explain My Answer | Button after an exercise | Opens after the answer, so nothing left to cover | Implicit, it is about the answer just given | Not applicable | Exists only after submission |
| Brilliant Koji | In the lesson, and from Home | Unknown | "Sees what you are working on", stated in help | Unknown | Stated policy, no answer |
| Photomath | Camera | Replaces the problem with its solution | Shows the recognised expression | Its own renderer | None, the answer comes first |
| Copilot Chat | Ctrl+Alt+I side view, Ctrl+I inline | Side view no, inline overlays the code it edits | Implicit file chip, `#` mentions, "used N references" | KaTeX since 1.103, default since 1.104 | Not applicable |
| Cursor | Cmd+I or Cmd+L side pane | No | `@` mentions | Requested, reported broken | Not applicable |

## Accessibility patterns for a panel and a stream [verified]

Dialog or landmark. The APG modal dialog pattern says Tab and Shift+Tab stay inside the dialog, Escape closes it, focus returns to the invoking element, and when the content is large the first focus can go to a static element at the start (https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/, accessed 2026-09-29). The same page says both modal and non-modal dialogs contain their tab sequence, which is the wrong model for a panel that must sit beside an item the student is still working on. The complementary landmark fits better. APG defines it as a supporting section at a similar level to the main content that stays meaningful on its own, says it should be top level, and says each of several should have a unique label (https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/, accessed 2026-09-29). MDN agrees, maps it to `aside`, and advises against labels such as "Sidebar" because the screen reader already announces the landmark type (https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/complementary_role, accessed 2026-09-29). The toggle that shows and hides it is the APG disclosure pattern, a button with `aria-expanded` and optionally `aria-controls`, activated by Enter or Space (https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/, accessed 2026-09-29). This is the pattern `AccountMenu.tsx` already follows.

Not covering focus. WCAG 2.2 SC 2.4.11 requires that a focused component is "not entirely hidden due to author-created content", names non-modal dialogs and sticky footers as the typical offenders, and says content the user opened, such as a chatbot, passes only if the user can reveal the focused element without dismissing it (https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html, accessed 2026-09-29). A panel that shares the width rather than overlaying it avoids the question on desktop. On a phone the page needs bottom padding equal to the sheet so focused controls can scroll above it.

Dragging. SC 2.5.7 requires every dragging action to have a single-pointer alternative unless dragging is essential (https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html, accessed 2026-09-29). A bottom sheet that resizes by drag needs buttons that do the same.

Live regions and streaming. MDN says a polite region speaks when the user is idle, that the region must exist in the DOM before its content changes (ideally in the initial markup), and that `role="log"` and `role="status"` are implicitly polite (https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions and https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/log_role, accessed 2026-09-29). Two independent guides on streamed model output agree that pointing a live region at the element receiving tokens produces fragmented or dropped speech, and that the reliable pattern is to let the text appear silently and announce the finished message once (https://tianpan.co/blog/2026/04/17/ai-accessibility-streaming-screen-readers and https://accessibility.build/guides/accessible-ai-chat, accessed 2026-09-29). The second adds that focus stays in the composer after sending and that a Stop control stays focusable for the whole stream.

## Keyboard shortcut evidence [single-source]

WCAG 2.2 SC 2.1.4 applies to shortcuts made only of printable characters, which must be possible to turn off, remap to include a modifier, or be active only on focus. Shortcuts that need a modifier are outside its scope, and the reason for the criterion is speech users whose dictation fires single-letter commands (https://www.w3.org/WAI/WCAG22/Understanding/character-key-shortcuts.html, accessed 2026-09-29). A global tutor key must therefore carry Ctrl or Cmd.

Collisions checked.

| Candidate | Chrome | Safari (macOS) | Firefox | MathLive | Precedent |
| --- | --- | --- | --- | --- | --- |
| Ctrl/Cmd+K | Ctrl+K is "Search from anywhere on the page" on Windows and Linux | Not listed | Unknown | Not bound | Cursor inline edit |
| Ctrl/Cmd+I | Not listed | Not listed | Search summaries give Ctrl+I or Cmd+I for Page Info, a support thread disputes it on Windows | Not bound | VS Code inline chat, Cursor side pane |
| Ctrl/Cmd+L | Jump to the address bar | Smart Search field | Unknown | Ctrl+L scrolls into view | Cursor side pane |
| Ctrl/Cmd+J | Downloads | Not listed | Unknown | Not bound | None |
| Ctrl/Cmd+/ | Not listed | Not listed | Unknown | Not bound | None among the products above |

Sources for the table: https://support.google.com/chrome/answer/157179?hl=en, https://support.apple.com/guide/safari/keyboard-and-other-shortcuts-cpsh003/mac, https://mathlive.io/mathfield/reference/keybindings/, https://support.mozilla.org/en-US/kb/firefox-page-info-window and https://support.mozilla.org/en-US/questions/900972 (all accessed 2026-09-29). Mozilla's main shortcut page did not load in two attempts, so every Firefox cell is unknown or disputed. Ctrl/Cmd+/ is the only candidate with no collision on any page that loaded, and MathLive binds none of the candidates except Ctrl+L. Keyboard layouts where `/` needs Shift (for example German, where it is Shift+7) were not tested. Whether a key event carrying Ctrl and `/` arrives with `event.key === "/"` on those layouts is unknown.

## Side and bottom sheets [single-source]

`m3.material.io` rendered only its title in this session, as it did for 08. The Material Components for Android documentation on GitHub was used instead. It distinguishes standard side sheets, which keep secondary content visible while the main region scrolls, from modal side sheets that block the rest of the screen behind a scrim, and describes coplanar side sheets that compress the sibling view and are "not recommended for narrow screens" (https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/SideSheet.md, accessed 2026-09-29). Its bottom sheet page separates standard sheets, which coexist with the main UI and allow interaction with both, from modal sheets with a scrim, lists collapsed, half-expanded, expanded and hidden states, gives a default maximum width of 640 dp, and gives the drag handle a minimum height of 48 dp and accessibility actions to expand and collapse (https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/BottomSheet.md, accessed 2026-09-29). The side sheet page gives 256 dp as an example width only, so no width guidance was sourced.

## Reduced motion and mathematics safety [single-source]

MDN says `prefers-reduced-motion: reduce` signals a preference for removing, reducing or replacing motion, names scaling and panning of large objects as vestibular triggers, and shows opacity as the replacement (https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion, accessed 2026-09-29). This matches 08's rule and `motion.css`.

KaTeX's options page gives `trust` a default of false, which blocks commands such as `\includegraphics`, `maxExpand` a default of 1000 to stop macro loops, `maxSize` a default of Infinity, and `output` a default of `htmlAndMathml` (https://katex.org/docs/options, accessed 2026-09-29). The security page says `maxSize` and `maxExpand` guard untrusted input, that output "should be safe" from script injection, recommends sanitising it with a generous allow-list including SVG and MathML, and warns that error messages may contain unescaped source (https://katex.org/docs/security, accessed 2026-09-29). Measured against plan 09's "macro expansion disabled", `renderLatexToMarkup` today relies on the default `maxExpand` of 1000 and an unlimited `maxSize`. That is acceptable for curated stems, but it is short of 09's rule for model output. Macro expansion cannot be literally zero while the `\lim` macro is in use, so 09's wording needs a number.

## Where the evidence and Growth's rules pull apart [inferred]

08 bans "Chat-first layout for tutoring" and says there is no chat box beside an unsolved problem. Plan 03 says a guardrailed tutor is available beside a practice item, and the feature brief asks for a tutor one click away on every screen. These can be reconciled only if the panel is closed by default, never opens by itself (the canvas complaint), is never the layout's primary region, and enforces 03's guardrail before submission. 08's Point of view should be amended from "no chat box beside an unsolved problem" to "no unguarded chat beside an unsolved problem, and none open by default". That is a plan amendment for the operator to rule on, not something this file settles.

Meyer's critique and Khan's 2026 result both point to the same thing: a tutor helps most when it sees the student's own work. Growth's guardrail keeps the unsubmitted answer out of the tutor's context. Before submission, the only student work the tutor sees is what the student chooses to type into the panel, which 03 permits ("asks what the student has tried"). The panel copy has to make that explicit so the student does not assume the tutor can see the MathLive field.

## What this means for Growth [inferred]

Ranked by how much each change affects whether the panel helps or harms learning, then by how often the student meets it.

1. **The panel never gives the answer before submission, and its controls make that visible.** A fixed guardrail line sits under the panel header on any unsubmitted practice item: "Until you check your answer, this tutor will not give it. Tell it what you tried and it will ask you a question back." After submission the line changes to "You have checked this item. You can ask about the answer and the worked solution." There is no Solve, Show answer or Explain solution button and no starter prompt that asks for one. Replies before submission open with a question (03's ask-before-tell), and the tutor's first reply on an item restates what the item asks and asks what the student has tried. In a timed part, a mock or any exam-shaped item, the entry point stays in the bar but is disabled, with a visible reason: "Not available during a timed part." Rejected: Duolingo's post-answer-only model, which is the safest by construction but drops 03's pre-submission tutor. Also rejected: a prompt-only guardrail with no visible line, because the student cannot tell which mode applies and would push against a hidden rule.

2. **One entry point, in the top bar, labelled in words.** A text button "Ask" with the existing `question` icon sits in the right-hand cluster, immediately left of the avatar, at every width including under 600 px where the tabs move to the bottom bar. It is a disclosure button (`aria-expanded`, `aria-controls` pointing at the panel), as `AccountMenu` already is. No sparkle, robot or "AI" wording, per 08. There is no floating bubble at the bottom right, because that corner holds the AI notices stack and, on a phone, sits over the bottom tab bar. Rejected: Khanmigo's bottom-right icon, which collides with `.ai-notices` and the phone tab bar. Also rejected: an entry point inside each screen, which would break "one entry point" and multiply focus-return cases.

3. **The shortcut is Ctrl+/ on Windows and Linux and Cmd+/ on macOS.** It is the only candidate with no collision on the Chrome, Safari or MathLive pages that loaded, it carries a modifier so SC 2.1.4 does not apply, and it cannot fire the session's 1, 2, 3, N or P handlers, which ignore modified keys. The listener goes on `window` in the capture phase so it works while a MathLive field has focus. Behaviour is as follows. From anywhere with the panel closed, it opens the panel and focuses the composer. With the panel open and focus elsewhere, it moves focus to the composer. With focus in the panel, it closes the panel and returns focus to where it came from. The button's accessible name includes the shortcut ("Ask, Ctrl+/"), and the visible tooltip shows it. Rejected: Cmd/Ctrl+I, which matches VS Code and Cursor, but Firefox may bind it to Page Info. Rejected: Cmd/Ctrl+K, which Chrome takes on Windows and Linux. Rejected: any single letter, which 2.1.4 and the existing single-key handlers rule out. The German-layout behaviour is unknown and should be tested before shipping.

4. **Desktop geometry shares the width and never covers the item.** At 1100 px and wider, the panel is a standard coplanar side sheet: an `aside` labelled "Tutor", a top-level sibling of `main`, docked to the right below the 56 px bar, full remaining height, 384 px wide (`calc(var(--growth-space-96) * 4)`). The page column reflows into the remaining width. At 1100 px this leaves 716 px, or 652 px after the 32 px gutters, which is still over the width of 08's 68-character measure. From 900 to 1099 px the panel is 320 px (`calc(var(--growth-space-64) * 5)`), and the column narrows below the measure, which is a maximum, not a minimum. The panel scrolls on its own and the item scrolls on its own. Because it overlays nothing, SC 2.4.11 cannot fail on the item. Rejected: an overlay drawer, which covers the right side of the item and fails 2.4.11 whenever focus lands under it. Rejected: a modal side sheet with a scrim, which would stop the student working on the item while the tutor is open, and whose dialog semantics trap Tab.

5. **Phone and narrow geometry is a standard bottom sheet with buttons, not only a drag.** Under 900 px the panel is a bottom sheet with no scrim, capped at 640 px wide (the Material default), and it covers the bottom tab bar while open. It has three heights. Collapsed is a 56 px bar showing "Tutor" and the last reply's first line. Half is 50 percent of the dynamic viewport and is the default on open. Full is the viewport minus the 56 px top bar. A row of text buttons ("Show the item", "Full height", "Close") does everything the 48 px drag handle does, for SC 2.5.7. While the sheet is open, `main` gets bottom padding equal to the sheet's height so every item control can scroll above it, which is what 2.4.11 asks for with user-opened content. "Show the item" collapses the sheet without losing the conversation. How iOS Safari's virtual keyboard resizes a sheet sized in `dvh` is unknown and has to be tested on a device. Rejected: a full-screen modal chat on phones, which hides the item entirely and turns the tutor into the primary surface 08 bans.

6. **The context line is short and fixed in shape, with an exact list behind it.** The header's second line reads "Can see: {screen}, {object}, {state}." Examples: "Can see: Today, practice item, not checked yet." "Can see: Review, card for chain rule." "Can see: Lesson, section 2." On an unsubmitted item a third line always reads "Cannot see: your answer or the answer key." A disclosure "What it can see" expands to the exact structured fields sent, in the same way VS Code's "used N references" works. "Item 3 of 12" is dropped because the client has no set position (see `docs/operator/ui-redesign.md`). It should come back only if the session payload gains one. The line updates when the screen changes while the panel is open, and the change is announced politely once. Rejected: Khanmigo's silent context, because a student who assumes the tutor sees their draft will misread a question-first reply as not paying attention.

7. **Streaming shows text, not motion.** The student's message appears at once, and focus stays in the composer. Below it a static line in `text-muted` reads "Writing a reply" until the first token arrives, with no spinner, pulsing dots, shimmer or blinking caret, because 08 bans skeleton shimmer and the motion is not feedback. Text is added as it arrives with no animation. A "Stop" text button is focusable for the whole stream. The message list is a plain list with visually hidden "You said" and "Tutor said" labels and no live region of its own. A separate visually hidden `role="status"` region that exists from the first render announces the whole reply once when it finishes (replies are short because they are question-first), and "Reply stopped" if stopped. The reply element carries `aria-busy="true"` while it streams. Rejected: `role="log"` or `aria-live` on the streaming element, which both guides show produces fragmented or dropped speech. Rejected: a non-streaming reply behind a spinner, which 08's motion rules and the wait length both argue against.

8. **Mathematics goes through the existing MathText path, hardened for model output.** The tutor template instructs the model to write inline mathematics as `\( ... \)` and displayed mathematics as `\[ ... \]`. `splitInlineMath` gains `\[ ... \]` for display. Dollar signs are not accepted, because a dollar in prose would be misread. A separate `renderTutorLatex` sets `trust: false` explicitly, `maxExpand` to a small number that still covers the `\lim` macro, `maxSize` to a small cap in ems, and keeps `output: "htmlAndMathml"` so screen readers get MathML. Text between formulas stays React text nodes, so it is escaped. No Markdown is converted to HTML. Paragraph breaks come from blank lines and nothing else. During streaming, text after an unclosed `\(` is held back until the closing delimiter arrives, so raw LaTeX never flashes and then jumps into typeset form. The only `dangerouslySetInnerHTML` is KaTeX's own markup, as in `MathText.tsx` today, optionally passed through an allow-list sanitiser as KaTeX's security page suggests. A formula KaTeX rejects falls back to `latexToAccessibleText`, never to the raw error message. Plan 09's "macro expansion disabled" should be amended to the `maxExpand` number chosen. Rejected: a general Markdown renderer, which is an HTML path for model output that 09 forbids. Rejected: MathJax, which would be a second maths renderer beside the KaTeX the client already ships.

9. **The empty state and the degraded states say what is true and what still works.** Every state keeps the composer's text if one was typed.
   - Empty, on an unsubmitted item: "Ask about this item. It will ask what you have tried before it explains anything." On any other screen: "Ask about what is on this screen." A second line for privacy: "This conversation is kept and you can read or delete it in Settings." The retention period goes into that line once plan 09 fixes it.
   - Usage limit (the subscription's own limit, reported by the provider): "The tutor cannot answer right now because the account's usage limit has been reached. It will answer again after {reset time}. Practice is not affected." If the reset time is not reported: "It will answer again when the limit resets." Whether the Claude Code CLI reports a reset time is unknown here.
   - Cap (the tutor's daily cap in `budgets`, plan 07): "The tutor has used today's allowance and is unavailable for the rest of today. Practice is not affected." This is plan 07's wording, restated in the student's voice.
   - Offline (the browser is offline or the server cannot be reached): "No connection, so the tutor cannot answer. What you typed is kept here." The question is not queued for later, because a reply written for a screen the student has left would carry stale context.
   - In each degraded state the Send button is disabled and has a visible reason next to it, not only in a tooltip. None of the copy uses praise, exclamation marks, advice about when to study, or blame.

10. **The keyboard-only flow is complete and matches existing primitives.** Ctrl/Cmd+/ opens the panel and focuses the composer. Enter sends, and Shift+Enter adds a line. Enter in the composer cannot commit an item, because `isTypingTarget` in `SessionScreen.tsx` already matches `textarea`. Tab moves from the composer to Stop (while streaming), then to the context disclosure and the message list, then out of the panel into the rest of the page, with no trap. The student reads the reply either from the status announcement or by Shift+Tab into the list. Escape anywhere in the panel closes it and returns focus to the element that had focus before it opened (the MathLive field, a button, or `main`), falling back to the Ask button if that element is gone. This is the APG rule and what `AccountMenu` and `Dialog` already do. Rejected: moving focus to the reply when it finishes, which both streaming guides advise against.

11. **Motion is instant on the keyboard path and a cross-fade at most elsewhere.** The desktop panel opens and closes with no transition, because it is toggled by a repeated keystroke and 08 removes animation from those, and because the column reflow cannot be animated with `transform` alone. The phone sheet may move in with a 300 ms ease-out `translateY` and `opacity`, added as `.motion-tutor-sheet` in `motion.css`, with the `reduce` branch keeping only the opacity transition, which is the file's existing pattern. Streamed text, the "Writing a reply" line and the status announcement never animate. Rejected: `animation: none` under reduced motion, which 08 calls wrong.

12. **AI notices do not duplicate the panel.** While the tutor panel is open, `AiNotices` skips notices whose role is the tutor, because the panel already discloses the call, and the toast stack at the bottom right would otherwise sit over the panel or the sheet. Notices for other roles move to the bottom left while the panel is open on desktop. Rejected: leaving the notices as they are, which puts a toast for every tutor reply over the reply itself.

13. **An optional second route into the same panel from feedback.** After submission, the elaborated feedback panel (`app/web/src/session/ElaboratedPanel.tsx`) can carry a text button "Ask about this feedback" that opens the same panel with the feedback in context. This is Duolingo's strongest pattern, and it adds no second chat surface. It is ranked last because the top-bar entry point already reaches the same place.

Desktop at 1100 px and wider, with the panel open on an unsubmitted item. The wireframe follows 08's style and uses the recommended copy.

```
+--------------------------------------------------------------------------------------+
| GROWTH   Today  Lessons  Review  Progress  Assessments            [? Ask]  (M) v     |
+------------------------------------------------------+-------------------------------+
|                                                      | Tutor                   [x]   |
|  Differentiate  f(x) = x^2 sin(x)                    | Can see: Today, practice      |
|                                                      | item, not checked yet.        |
|  Worked so far                                       | Cannot see: your answer or    |
|   1. u = x^2 , v = sin(x)          [given]           | the answer key.               |
|   2. u' = 2x , v' = cos(x)         [given]           | > What it can see             |
|   3. f' = u'v + uv'                [given]           |                               |
|   4. f'(x) = ____________          [you]             | Until you check your answer,  |
|                                                      | this tutor will not give it.  |
|  [ MathLive field ]                                  |                               |
|                                                      |        which part is u'v?     |
|  ( ) guess  ( ) unsure  ( ) confident                | Which factor did you call u,  |
|                                                      | and what is its derivative?   |
|                              [ Check my answer ]     |                               |
|                                                      | [ composer               ]    |
|                                                      | Send          Ctrl+/ to close |
+------------------------------------------------------+-------------------------------+
```

## Sources [verified]

- https://support.khanacademy.org/hc/en-us/articles/13982530363533-Where-can-I-access-Khanmigo-while-working-on-Khan-Academy (accessed 2026-09-29, 403 on fetch, search summary only)
- https://www.khanacademy.org/college-careers-more/khanmigo-for-students/x5443352261243283:introducing-khanmigo/x5443352261243283:learning-with-khanmigo/v/khanmigo-for-students-how-to-use-math-or-science-tutoring-on-khanmigo (accessed 2026-09-29, body did not load, search summary only)
- https://www.khanmigo.ai/learners (accessed 2026-09-29)
- https://blog.khanacademy.org/khanmigo-math-computation-and-tutoring-updates/ (accessed 2026-09-29)
- https://blog.khanacademy.org/how-khan-academy-is-building-a-better-ai-tutor-our-most-recent-learnings/ (accessed 2026-09-29)
- https://support.khanacademy.org/hc/en-us/articles/14394814244365-What-safety-features-does-Khanmigo-have (accessed 2026-09-29, 403 on fetch, search summary only)
- https://support.khanacademy.org/hc/en-us/articles/15127248640525-How-do-I-view-my-students-Khanmigo-chat-history (accessed 2026-09-29, search summary only)
- https://www.edweek.org/teaching-learning/ai-gets-math-wrong-sometimes-how-teachers-deal-with-its-shortcomings/2024/09 (accessed 2026-09-29)
- https://danmeyer.substack.com/p/khanmigo-doesnt-love-kids (accessed 2026-09-29)
- https://blog.duolingo.com/explain-my-answer-now-free (accessed 2026-09-29)
- https://blog.duolingo.com/duolingo-max/ (accessed 2026-09-29)
- https://www.techlearning.com/how-to/what-is-duolingo-max-the-gpt-4-powered-learning-tool-explained-by-the-apps-product-manager (accessed 2026-09-29)
- https://duoplanet.com/duolingo-max-review/ (accessed 2026-09-29)
- https://brilliant.org/help/features/ (accessed 2026-09-29)
- https://beginnersinai.org/brilliant-explained/ (accessed 2026-09-29, search summary only)
- https://apps.apple.com/us/app/photomath/id919087726 (accessed 2026-09-29)
- https://support.google.com/photomath/answer/14328660?hl=en (accessed 2026-09-29)
- https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features (accessed 2026-09-29)
- https://code.visualstudio.com/docs/copilot/chat/inline-chat (accessed 2026-09-29)
- https://code.visualstudio.com/docs/copilot/chat/copilot-chat (accessed 2026-09-29)
- https://code.visualstudio.com/docs/chat/copilot-chat-context (accessed 2026-09-29)
- https://code.visualstudio.com/updates/v1_103 (accessed 2026-09-29)
- https://code.visualstudio.com/updates/v1_104 (accessed 2026-09-29)
- https://code.visualstudio.com/docs/configure/accessibility/accessibility (accessed 2026-09-29)
- https://github.com/microsoft/vscode/issues/239996 (accessed 2026-09-29)
- https://cursor.com/docs/configuration/kbd (accessed 2026-09-29)
- https://cursor.com/docs/agent/overview (accessed 2026-09-29)
- https://cursor.com/help/customization/context (accessed 2026-09-29)
- https://forum.cursor.com/t/align-chat-rendering-with-vscodes-katex-support/111053 (accessed 2026-09-29)
- https://x.com/AnthropicAI/status/1826667671364272301 (accessed 2026-09-29, search summary only)
- https://community.openai.com/t/canvas-opens-automatically-how-to-prevent-that/1055091 (accessed 2026-09-29)
- https://www.ai-toolbox.co/chatgpt-management-and-productivity/how-to-use-chatgpt-canvas-guide-2026 (accessed 2026-09-29, search summary only)
- https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ (accessed 2026-09-29)
- https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/ (accessed 2026-09-29)
- https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/ (accessed 2026-09-29)
- https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/complementary_role (accessed 2026-09-29)
- https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions (accessed 2026-09-29)
- https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/log_role (accessed 2026-09-29)
- https://tianpan.co/blog/2026/04/17/ai-accessibility-streaming-screen-readers (accessed 2026-09-29)
- https://accessibility.build/guides/accessible-ai-chat (accessed 2026-09-29)
- https://www.w3.org/WAI/WCAG22/Understanding/character-key-shortcuts.html (accessed 2026-09-29)
- https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html (accessed 2026-09-29)
- https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html (accessed 2026-09-29)
- https://support.google.com/chrome/answer/157179?hl=en (accessed 2026-09-29)
- https://support.apple.com/guide/safari/keyboard-and-other-shortcuts-cpsh003/mac (accessed 2026-09-29)
- https://support.mozilla.org/en-US/kb/keyboard-shortcuts-perform-firefox-tasks-quickly (accessed 2026-09-29, did not load)
- https://support.mozilla.org/en-US/kb/firefox-page-info-window (accessed 2026-09-29, search summary only)
- https://support.mozilla.org/en-US/questions/900972 (accessed 2026-09-29, search summary only)
- https://mathlive.io/mathfield/reference/keybindings/ (accessed 2026-09-29)
- https://m3.material.io/components/side-sheets/guidelines (accessed 2026-09-29, rendered only its title)
- https://m3.material.io/components/bottom-sheets/guidelines (accessed 2026-09-29, rendered only its title)
- https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/SideSheet.md (accessed 2026-09-29)
- https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/BottomSheet.md (accessed 2026-09-29)
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion (accessed 2026-09-29)
- https://katex.org/docs/options (accessed 2026-09-29)
- https://katex.org/docs/security (accessed 2026-09-29)
- https://pubmed.ncbi.nlm.nih.gov/40560616/ (accessed 2026-09-29, cookie wall, figures carried from plan 03 and 08)
- https://www.pnas.org/doi/10.1073/pnas.2422633122 (accessed 2026-09-29, 403)
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4895486 (accessed 2026-09-29, 403)
