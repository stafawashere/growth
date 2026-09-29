---
title: Today redesign, handoff
research_date: 2026-09-29
status: in_progress
purpose: Where the overnight Today redesign stands, stage by stage, with the exact resume point if the run is cut off.
---

# Today redesign, handoff

Branch `today/redesign`, from `main` at 635c03b (the operator asked mid-run for every branch to be merged and pushed; main was fast-forwarded to lessons/redesign and ai-fixes merged, then the overnight branch fast-forwarded onto it).

## State [verified]

| Stage | State | Last green check | Next command |
|---|---|---|---|
| A research base | running: five Sonnet research agents writing docs/pedagogy/today/products/*.md, science.md, question-standards.md | none yet | write synthesis.md and README.md when the agents return |
| B clean-slate design | not started | | |
| C gap analysis | running: tools/selection_study.py re-run in the background (var/today-redesign/selection-study-rerun.log); Opus agents writing app/sim/today_metrics.py, tools/draw_today_audit_sample.py, tools/seed_history_student.py | | |
| D redesign and build | not started | | |
| E verify in the app | not started; scratch server on 127.0.0.1:8005 and web on 5175 (launch config growth-today, growth-web-today) | | |
| F record | this file and the ledger stub | | |

## Resume point [verified]

If cut off before Stage A closes: read the agent outputs under docs/pedagogy/today/, write synthesis.md and README.md, run `qa/12_report.py` only if data/ or research/ changed (they have not), commit.
