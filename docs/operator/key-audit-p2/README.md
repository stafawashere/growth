---
title: Stage 1 key audit, gate 29 over Units 1 to 10
research_date: 2026-09-24
status: complete
purpose: Records the 100-item key-audit sample drawn from the stage 1 item banks, its verdicts and the measured key error rate, and says who audited and how.
---

# Stage 1 key audit, gate 29 over Units 1 to 10 [verified]

Key error rate: 0/100

`sample.json` is the 100-item sample `tools/draw_key_audit_sample.py` drew with seed 2026 from the 656 signed-off items in the nine stage 1 banks (`content/items_unit01_agent` to `content/items_unit10_agent`, no Unit 8 bank). The draw ran over a scratch database that ingested only those banks, so no P1 item could enter the sample. The items span nine units, so the base cap of 15 per unit from `app/review/audit.py` `unit_cap_for` already fills 100, and the draw gave Unit 1 11, Unit 2 15, Unit 3 4, Unit 4 11, Unit 5 9, Unit 6 15, Unit 7 15, Unit 9 5 and Unit 10 15. `verdicts.json` holds one verdict per sampled id. `tools/check_audit_verdicts.py verdicts.json sample.json` prints `key error rate: 0.0`. The Wilson 95 percent interval on 0 of 100 is 0 to 0.037.

## Who audited, and how [verified]

The operator ruled on 2026-09-24 that no human review will be done and that Claude performs every review and audit (BUILD-LEDGER.md, "Plan corrections applied"). The auditor is claude-opus-5-5, named in every verdict. Each verdict rests on two checks.

- **The key.** A separate agent received only the stems and wrote each bank's `key_formulations.py`, a SymPy computation of what the stem asks for. It never saw the records, keys or options. `tools/key_recheck.py` compared those answers with the stored key and every option in each bank. All 656 items, the sampled 100 among them, matched, and no distractor equals its key. The comparator's control held on every bank.
- **Ambiguity.** Every sampled stem was read with its options for a second correct answer, an unstated domain or branch, and whether each count the stem asserts holds. Examples are "exactly one vertical asymptote" and "exactly two points at which the tangent line is horizontal". None admitted a second answer.

The audit led to two stem changes before the verdicts were recorded, and neither changed a key:
- The 20 BC-QA-10005 stems now state the integrand and the lower limit of integration. Before, "the improper integral whose convergence matches that of the series" allowed any lower limit.
- The 7 of those stems that already named f lost a redundant clause.

## What this rate is not [inferred]

The auditing model belongs to the same family that drafted and formulated the items, so an error all three would make the same way is not excluded. The recheck control shows the comparator can tell a changed answer from the stored key. It does not show that the formulations read every stem correctly.
