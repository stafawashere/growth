---
title: P1 key audit, gate 29
research_date: 2026-09-24
status: complete
purpose: Records the drawn 100-item P1 key-audit sample, its verdicts and the measured key error rate, and says who audited and how.
---

# P1 key audit, gate 29 [verified]

Key error rate: 0/100

`sample.json` is the 100-item sample `tools/draw_key_audit_sample.py` drew with seed 2026 from the 130 P1 items after they were signed off (`content/items_p1_agent/`, `signed_off_by` on each record), using the unit cap `app/review/audit.py` `unit_cap_for` sets for three units. `verdicts.json` holds one verdict per sampled id. `tools/check_audit_verdicts.py verdicts.json sample.json` prints `key error rate: 0.0`; the Wilson 95 percent interval on 0 of 100 is 0 to 0.037.

## Who audited, and how [verified]

The operator ruled on 2026-09-24 that no human review will be done and that Claude performs every review and audit (BUILD-LEDGER.md, "Plan corrections applied"). The auditor is therefore claude-opus-5-5, named in every verdict. Each verdict rests on two checks. The key: each stem was written as a SymPy computation from the stem text alone, never from the key (`content/items_p1_agent/key_formulations.py`), and compared with the stored key and every option (`tools/key_recheck.py`, `docs/operator/p1-agent-item-key-check.md`); all 100 matched and no distractor equals its key. Ambiguity: every stem was read with its options for a second correct answer, an unstated domain or quadrant, and for whether each count the stem asserts holds (the BC-QA-03005 stems say "exactly one point" or "two values of k", and each count was recomputed); none admitted a second answer.

## What this rate is not [inferred]

It is a model audit by the model family that drafted the items, so an error both would make the same way is not excluded. Plan 10 describes the P1 rate as the floor P4 must not exceed; it is that floor for a model audit, not for a human one.
