---
title: P4 key audit over the generated banks
research_date: 2026-09-24
status: complete
purpose: Records the 100-item key-audit sample drawn from the generated banks for P4's exit criterion, its verdicts and the measured key error rate, and says who audited and how.
---

# P4 key audit over the generated banks [verified]

Key error rate: 0/100, Wilson 95 percent interval 0 to 0.037. The P1 baseline in
[../key-audit-p1/](../key-audit-p1/) is 0/100 with the same interval, so the P4 rate does not exceed
it.

`sample.json` is the sample `tools/draw_key_audit_sample.py <db> data sample.json 2026 --generated`
drew from the 2,339 signed-off generated items in `content/items_gen_unit01` to
`content/items_gen_unit10`, over a scratch database that ingested only those banks. `--generated`
restricts the draw to items whose provenance names a template. The sample spans 73 archetypes: 74
no-calculator and 26 calculator items, 11 from Unit 1, 10 from Unit 2, 8 from Unit 3, 7 from Unit 4,
9 from Unit 5, 7 from Unit 6, 5 from Unit 7, 14 from Unit 8, 10 from Unit 9, 11 from Unit 10 and 8
from the 99 block. `tools/check_audit_verdicts.py verdicts.json sample.json` prints
`key error rate: 0.0`.

## Who audited, and how [verified]

This is a model audit, not a human verdict. The operator ruled on 2026-09-24 that no human review
will be done, and the auditor named in every verdict is claude-opus-5-5 on that delegation.

Every sampled item was read in full (stem, figure description or table, key, all four options with
their named errors) and its key re-derived by hand: each exact key by differentiating,
integrating, factoring or summing it, and each three-decimal key by recomputing it at 25 digits
with mpmath (quadrature, root finding or numerical differentiation). All 100 agreed with the stored
key. Every distractor label on the statement items was read for truth: none was a second correct
answer.

The audit found one surface defect and no key error. ITM-GEN-01005-17's option B printed a unit
coefficient as `1 x^{2}`. The template now prints a unit coefficient as a sign, four items were
rebuilt from their seeds with the same keys, and the gate gained a check that fails a family whose
mathematics prints a coefficient of 1 (`tests/generation/test_template_gate.py`).

## What this rate is not [inferred]

The template authors, the blind solvers and the auditor are all the same model family, so an error
all three would make the same way is not excluded. Before the audit every generated key had
already matched both the template's own SymPy answer and a blind formulation written from the stem
alone, with the recheck control holding (`tests/generation/test_generated_banks.py`); the audit
adds a third reading, not an independent human one.
