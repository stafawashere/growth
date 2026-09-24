---
title: Golden sets
research_date: 2026-09-24
status: recorded
purpose: The golden set for every model role, who wrote and labelled each, what each measures and when, and the baselines measurable at no model cost.
---

# Golden sets

Written by `tools/golden_sets.py`. Every set in `content/golden/` was authored and labelled by claude-opus-5-5 on the operator's delegation of 2026-09-24. None is a human's work and none has been reviewed by a human. Where 10 and 11 say the operator authors or verifies a set, a model did it and each file says so in its `authored_by` and `labelled_by` lines. `app/evals/golden.py` validates each set before any number is read off it, and every set passed on this run.

| Role | Set | Cases | Breakdown | Measured |
|---|---|---|---|---|
| tutor | tutor_goldens | 48 | False 24, True 24 | now, on any recorded or live tutor sentence, once a sentence is labelled against the four checks |
| grader | golden_set_2 | 85 | eligible_after_error 17, fully_correct 17, narrow_fail 17, notation_failure 17, unconventional_valid 17 | when P3 wires the grader; per-point-type exact match with its count, kappa with its interval |
| transcriber | golden_set_3 | 20 | angled 3, crossed_out 3, good_light 3, injected_instruction 2, low_light 3, margin_work 3, slight_blur 3 | when P3 wires the transcriber and each page has been written by hand and photographed |
| diagnostician | diagnostician_goldens | 46 | 40 distinct archetype_id values | when P3 wires the diagnostician; observed-error exact match and top-hypothesis agreement |
| generator | golden_set_1 | 28 | no_calculator 28 | now as a regression guard on the bank's frozen keys; as a generator eval when P4 wires the generator |
| verifier | verifier_goldens | 42 | calculator_boundary 6, distractor_equals_key 6, duplicate_distractors 6, none 6, unresolvable_error_path 6, wrong_key 6, wrong_worked_step 6 | now, for the deterministic checks; for the model verifier when P4 wires it |

The grader set labels 63 of 85 responses earned. It covers the 17 BC-PT records that reach a model, five responses each, one per adversarial category of 10. 10 asks for 30 point types drawn from those that reach a model, and only 17 exist, so 17 by 5 is the whole population rather than a sample of it.

## Deterministic verifier baseline

The checks `app/items/ingest.py` runs on the way into the bank, plus the distractor-path rule, scored against the verifier set. A case counts as caught when the verdict matches the expected one; the none row is the control, whose expected verdict is accept.

| Defect | Caught | Cases |
|---|---|---|
| none | 6 | 6 |
| wrong_key | 6 | 6 |
| distractor_equals_key | 6 | 6 |
| duplicate_distractors | 6 | 6 |
| unresolvable_error_path | 6 | 6 |
| calculator_boundary | 0 | 6 |
| wrong_worked_step | 0 | 6 |

Every kind the checks do not catch is a defect only the independent re-solve and the model verifier of 04 can catch, which is the reason P4 keeps both.
