---
title: Live tutor agent, handoff
research_date: 2026-09-29
status: draft
purpose: State where the live tutor agent build stands on the branch agent/live-tutor and what the next session does first.
---

# Live tutor agent, handoff

Branch `agent/live-tutor`, worktree `/Users/mahfujm/dev/growth-live-tutor`, nine commits from the checkout's HEAD (8cb6be9, which sits on `today/redesign`, two commits past `main` 635c03b). Nothing pushed, `main` untouched. The full record is the "Live tutor agent, 2026-09-29" entry in `BUILD-LEDGER.md`.

## State [verified]

Built and verified in the running app: the Ask button in the top bar on every signed-in screen, Ctrl+/ and Cmd+/, the aside beside main from 900 px and the bottom sheet under it, the context lines, the guardrail line, streamed replies with rendered mathematics, the Tutor settings tab with the conversation list, the memory entries (read, edit, delete, clear, pause), the per-student profile behind the `tutor_profile` switch, the memory consolidation job on the auto drain, and the degraded states (usage limit, daily cap, minute cap, sign-in, unavailable, timed part, item and conversation ceilings, refused screen).

The stage D walk made 11 live subscription calls in all (9 agent turns and probes, 2 memory consolidations), logged in the ledger's live-call table. Every other state was exercised through the fake CLI at `tests/fixtures/fake_claude/claude`.

## What is behind a switch [verified]

- `tutor_profile` (`app/experiments/switches.py`): the profile is computed and stored for every student, and rendered into the prompt only for the `profile_applied` arm. Analysis in `app/experiments/analysis.py` `tutor_profile_comparison`, with a calibration guard per arm.
- Memory: `users.agent_memory_paused`, the student's own switch in the Tutor settings tab.

## Not done [inferred]

- The reader's `#end` screen and a decision lesson's `#stems` screen send section ids the server cannot find; a turn there is refused with the "could not use what this screen sent" copy (a 400). The client should send those screens as a lesson with no section, or the server should accept the two ids.
- A lesson question stays in practice mode after the student has answered it, because the server does not read `lesson_check_responses`. Conservative, so the key is never given, but the discussion after an answered check is guarded when it need not be.
- A `usage_limit` error with no `resets_at` has no clear path other than the student editing the draft. Needs a ruling on what the copy should say.
- `tests/eval/test_prompt_output_goldens.py` fails on this branch (a cassette miss and a prompt-set mismatch that lists `memory/consolidate_v1` among others). It also failed on HEAD before the branch for the other prompts; the new memory prompt has no recorded output golden. Recording one needs a live call the operator approves.
- The Ollama floor is not built (ruling in `docs/plan/12-open-questions.md`).
- No study advice, praise, prediction or schedule copy anywhere; the deterministic screen holds the line, and the golden set labels where the model would break it.

## Next actions [inferred]

1. Read the rulings list in `docs/plan/12-open-questions.md`, "Rulings the live tutor agent needs, 2026-09-29", and the two added by the walk (the answered-check mode and the `usage_limit` copy with no reset time).
2. Decide whether to merge `agent/live-tutor` into `main`. It carries the two `today/redesign` commits under it, so merge that branch first or rebase this one onto `main`.
3. After a week of use, read the five-hour and seven-day utilisation the CLI reports on every call (`var/subscription_pacing.json` and the audit rows) and set the agent's pacing from measurement.
4. Record the consolidation prompt's output golden with one approved live call so `test_prompt_output_goldens.py` covers `memory/consolidate_v1`.

## Scratch state left behind [verified]

Scratch servers were stopped at the end of the session. The scratch database, cookies and logs live under the session's scratchpad and are not part of the repository. Screenshots from the walk are under `var/agent/` (gitignored), numbered 01 to 15.
