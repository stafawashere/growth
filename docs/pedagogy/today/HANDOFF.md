---
title: Today redesign, handoff
research_date: 2026-09-29
status: in_progress
purpose: Where the overnight Today redesign stands, stage by stage, with the exact resume point if the run is cut off.
---

# Today redesign, handoff

Branch `today/redesign`, from `main` at 635c03b (the operator asked mid-run for every branch to be merged and pushed; main was fast-forwarded to lessons/redesign and ai-fixes merged, then the overnight branch fast-forwarded onto it).

## State [verified]

The worktree is /Users/mahfujm/dev/growth-today (its own .venv and a node_modules symlink); ~/dev/growth was switched to calculator/desmos-fluency by another session mid-run, so nothing is done there any more.

| Stage | State | Last green check | Next command |
|---|---|---|---|
| A research base | done, committed (products, science, question-standards, synthesis, README) | style grep for dashes, 0 | |
| B clean-slate design | done, committed with rulings-for-operator.md | | |
| C gap analysis | done, committed: algorithm (today_metrics 60 and 226 days), walk of a seeded and a fresh student, 72-item audit (64 of 64 keys match blind; 50 clean, 15 fix_distractor, 7 fix_stem) | tests/sim 4 passed; tests/tools 31 passed | selection_study.py re-run and today_sim_study.py still running in ~/dev/growth/var/today-redesign/*.log |
| D design and build | design.md and the plan amendments committed; three Opus agents building: engine priority plus switch, feedback and day screen, item fixes; lints committed (2547bfe) | tests/tools/test_item_standards.py 25 passed | when the agents report: run their named tests, commit per area, then the blind re-solve of var/today-redesign/fixed-stems.json |
| E verify in the app | the capture script agent is writing var/today-redesign/shots/ from the scratch servers (API 8005 seeded, 8006 fresh; web 5175 and 5176); the redesign is not yet served there | | restart the scratch API from the worktree after the build lands, re-walk |
| F record | ledger stub only | | |

## Resume point [verified]

If cut off now: read the three agents' files with `git status` in the worktree, run `timeout 900 .venv/bin/python -m pytest tests/engine/test_priority.py tests/session tests/experiments tests/feedback` and, from app/web, `npx vitest run src/session src/home` and `npx tsc --noEmit -p .`; commit what is green per area; then read docs/pedagogy/today/simulation-record.md when tools/today_sim_study.py finishes and decide D2 (production or switch) on its comparison table; then Stage E and the ledger entry.
