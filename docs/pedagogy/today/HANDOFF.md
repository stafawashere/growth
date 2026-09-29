---
title: Today redesign, handoff
research_date: 2026-09-29
status: in_progress
purpose: Where the overnight Today redesign stands, stage by stage, with the exact resume point if the run is cut off.
---

# Today redesign, handoff

Branch `today/redesign`, from `main` at 635c03b (the operator asked mid-run for every branch to be merged and pushed; main was fast-forwarded to lessons/redesign and ai-fixes merged, then the overnight branch fast-forwarded onto it).

## State [verified]

The worktree is /Users/mahfujm/dev/growth-today (its own .venv and a copied node_modules, because Vite refused fonts through a symlink); ~/dev/growth was switched to calculator/desmos-fluency by another session mid-run, so nothing is done there any more except the two long simulations started before the switch, which import that checkout's code.

| Stage | State | Last green check | Next command |
|---|---|---|---|
| A research base | done, committed (products, science, question-standards, synthesis, README) | style grep for dashes, 0 | |
| B clean-slate design | done, committed with rulings-for-operator.md | | |
| C gap analysis | done, committed: algorithm (today_metrics 60 and 226 days, the selection study re-run of 2026-09-29 in docs/operator/selection-study-record.md), walk of a seeded and a fresh student, 72-item audit (64 of 64 keys match blind; 50 clean, 15 fix_distractor, 7 fix_stem) | tests/sim 8 passed (one red by design, C10); tests/tools 157 passed | |
| D design and build | done, committed: engine priority behind the selection_priority switch (default off), session assembly audit rows, feedback correct result, math field live read, Today overview line, question standards lints, 395 item fixes through the pipeline (blind re-solve 180 of 180 formulated keys match), 13 templates regenerated from stored seeds | tests/engine 90, tests/session 93, tests/experiments 9, tests/feedback 47 passed (one load-only failure), check_items exit 0 on 19 of 20 banks (unit03_agent is load-bound, see the ledger) | when tools/today_sim_study.py finishes, read docs/pedagogy/today/simulation-record.md and decide D2 on the paired mean differences; the switch is the landing unless every interval sits above 0 |
| E verify in the app | done: after-set captures (fresh and history, light and dark, 390 and 1280 widths), 0 console errors, 0 failed requests; the 390 overflow was a wide worked step and is fixed (50c75a9, wideMathScrolls.test.tsx) | vitest touched files 35 passed; tsc 0; build 9.69 s | full vitest run in var/today-redesign/checks/vitest-final.log |
| F record | ledger entry drafted with placeholders COMMIT_COUNT, SIMULATION_SUMMARY, CAPTURE_SUMMARY, CHECK_TABLE, PENDING_RUNS | | fill from the logs under var/today-redesign/checks/, the study record and the P7 re-run (var/today-redesign/p7-evals-rerun.log), then commit; then merge today/redesign into main and push, as the operator asked mid-run |

## Resume point [verified]

If cut off now: `git status` in the worktree should be clean; check `tail ~/dev/growth/var/today-redesign/today-sim-study.log` (the study writes docs/pedagogy/today/simulation-record.md in ~/dev/growth when done; copy it into the worktree) and `tail var/today-redesign/p7-evals-rerun.log`; fill the five placeholders in BUILD-LEDGER.md, quoting the pass and fail lines from var/today-redesign/checks/*.log; commit; merge into main and push.
