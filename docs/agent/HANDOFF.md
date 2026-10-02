---
title: Live tutor agent, handoff
research_date: 2026-09-30
status: draft
purpose: State where the live tutor agent build stands, now with its drawing ability on the branch agent/drawing, and what the next session does first.
---

# Live tutor agent, handoff

Branch `agent/drawing`, worktree `/Users/mahfujm/dev/growth-drawing`, from `main` at fa514089, merged with `main` at 0f80de16 (another session's restyle) on 2026-10-01 and then merged into `main` with `--no-ff` on the operator's instruction. Nothing pushed. The full record is the "Tutor drawing, 2026-09-30" entry in `BUILD-LEDGER.md`; the live tutor's own entry, "Live tutor agent, 2026-09-29", is unchanged.

## State [verified]

Built and verified live in the running app on 2026-10-01 (the subscription backend, the shared `var/test.db`, the drawing server on 5191 and 8741):

- The tutor draws one figure per reply when the move allows it: a closed, declarative figure language the model writes as a fenced block, compiled and screened on the server, built in the panel step by step with the sentences that introduce each step, at reading pace, with step controls, a step list, a description for assistive technology, roles that read without colour, and a sticky hold so the figure stays in view while it builds.
- The art board (2026-10-01): figures open on a movable, resizable, minimizable board instead of in the chat, which keeps one line per figure with "Show on the board".
- Marks on the page: underlines, highlights, rings, notes, arrows and constructions on the item's own graph, drawn over the real elements, bound to the screen they were drawn on (hidden when the student leaves, restored when they return).
- The guardrail: a figure or marks block that shows the key before checking withholds the reply with the fixed decline; malformed, oversized, cut-off, extra and closed-turn blocks are dropped with one line and the reply continues; option anchors are never offered.

Screenshots `var/agent/drawing/01` to `30`, the walkthrough video `var/agent/drawing-walkthrough.mp4`, both gitignored. The recorder is `tools/record_walkthrough.mjs`; its walk script lives in the session scratchpad because it holds the test password, and the ledger lists its steps.

## What is behind a switch [verified]

- `GROWTH_AGENT_DRAWING` (default `on`). `off` closes drawing and marks on every turn and drops any block with the reason `off`.
- Unchanged from the live tutor: `tutor_profile` and the student's memory pause.

## Not done [inferred]

- No live call produced a malformed or oversized block (one attempt drew a valid figure within the caps instead); those two refusals were shown through the real route and client with the repository's fake CLI.
- A figure built on the item's own data uses free shapes (rectangles, boxes) rather than the item's table; the language has no shape that reads the item's table into a Riemann sum, so a model must copy the values, which the screen then checks.
- The route refuses a marks block whose step ids repeat a shown figure's, and the golden set has no case for it.
- A correct opener whose first worked step shows on screen is not listed as a `solution_step` anchor, because the packet cannot see that.
- The reading pace (238 words a minute) is an adult average applied to a school-age reader; the first week of use should set it.
- Carried from the live tutor handoff and still open: the reader's `#end` and a decision lesson's `#stems` screens send ids the server refuses; an answered lesson question stays in practice mode; the `usage_limit` copy with no reset time; `tests/eval/test_prompt_output_goldens.py` has no recorded output for `memory/consolidate_v1` (it now also has none for `agent/live_v2`).
- Four checks fail on `main` at fa514089 and on this branch, confirmed on a clean `main` checkout on 2026-10-01: `tests/providers/test_ai_notices.py::test_a_grader_brief_summarises_the_decision_and_leaves_out_the_student_work`, `tests/providers/test_prompt_cache_prefix_length.py::test_prompt_cache_prefix_length`, `tests/providers/test_prompts.py::test_prompt_templates_are_versioned_and_golden` (no golden digest for `prompts/generator/lesson_v1.md` and `lesson_v2.md`), and the web test `client.test.ts` `GradingsPayload`.

## Next actions [inferred]

1. Read the rulings in `docs/plan/12-open-questions.md`, "Rulings the tutor drawing needs, 2026-09-30", in particular the three test inventories pointed at the new template and column, the 12,000-token prefix ceiling approved in chat, stated givens equal to the key, and the reading pace.
2. Run the next tutor run from the prompt at `var/agent/tutor-next-run-prompt.md` (kept outside git): it audits what the tutor lacks in reaching the page and builds the skills that close the gaps. Watch `useAgentStream.test.ts` "a turn after its end frame", which failed once under load with "Controller is already closed" and passed alone.
3. Watch a week of `figure=` and `steps=` on the agent's log lines and the `agent_turns.figure` outcomes to set the share of turns that draw (plan 14 assumes 0.3) and to see how often a figure is dropped or withheld.
4. Remove the `growth-drawing` entry from `/Users/mahfujm/dev/growth/.claude/launch.json` when the walk server is no longer wanted.

## Scratch state left behind [verified]

Walk sessions were opened for the test account in `var/test.db` in rehearsal mode (no mastery updates): `SES-ecca3e1e764845caab3c3e5abf221890`, `SES-5ba69638cf7144cca2b2c64defa2c878`, `SES-ccc7e0cce09a4fa7b4e711bf78f636f6` and `SES-f07c4b52405a44cb92d83ce60d145295`. The test database gained the additive `agent_turns.figure` column, which code on `main` ignores.
