---
title: Desmos fluency, handoff
research_date: 2026-09-29
status: draft
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
| C slice 1a drill engine | done | 41615e2, 2b06b69 |
| C slice 1b cards and checker | done | a7919ce |
| C slice 2 storage, service, routes | done | 795d243, 47b7e37 |
| C slice 3 web | done | 49174bb, 9f7533d |
| D verification in the app | done, see the ledger entry | |
| E ledger, PROGRESS, handoff | done | |

## Resume point

Every stage is done. To continue: read the ledger entry, then `git log --oneline today/redesign..calculator/desmos-fluency`. The next work is whichever ruling the operator gives (below), or the Not done list in the ledger entry. To walk the feature again: build the client (`npm --prefix app/web run build`), start the API on a free port with a scratch `GROWTH_DB_PATH`, and drive it with var/calculator/driver.py (gitignored; `start`, `goto`, `click`, `type`, `eval`, `shot`, `console`, `requests`, `stop`); the keys of an open drill can be recomputed from its stored draw with the registry, as the scratch script did.

## Rulings waiting on the operator

See docs/calculator/build-plan.md, Rulings waiting on the operator, and docs/calculator/research/synthesis.md.
