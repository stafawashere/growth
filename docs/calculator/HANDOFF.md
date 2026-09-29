---
title: Desmos fluency, handoff
research_date: 2026-09-29
status: in_progress
purpose: Where the Desmos fluency work stands, what is green, what is not, and the exact resume point, so the next session continues without rereading the ledger.
---

# Desmos fluency, handoff

Branch `calculator/desmos-fluency`, not pushed, main untouched. Build ledger entry: BUILD-LEDGER.md, "Desmos fluency, 2026-09-29".

## State

| Stage | State | Commit |
|---|---|---|
| A research (docs/calculator/research/) | done | e9b56d9 |
| Corpus: web pages as cached documents, 40 added | done, qa 14 PASS | 22383d9 |
| Library edits (calculator-policy, unresolved, claims, PROGRESS) | done, qa 14 PASS | e9b56d9 |
| B design, architecture, synthesis, build plan, plan amendments | done | e9b56d9, bb6d30c |
| C slice 1a drill engine | in progress | |
| C slice 1b cards and checker | in progress | |
| C slice 2 storage, service, routes | not started | |
| C slice 3 web | in progress | |
| D verification in the app | not started | |
| E ledger, PROGRESS, handoff | this file | |

## Resume point

Read docs/calculator/build-plan.md, then the ledger entry, then `git log --oneline main..calculator/desmos-fluency`. The next command is the check of whichever slice above is not green; each slice's checks are listed in the build plan.

## Rulings waiting on the operator

See docs/calculator/build-plan.md, Rulings waiting on the operator, and docs/calculator/research/synthesis.md.
