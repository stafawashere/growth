---
title: P7 simulation record
research_date: 2026-09-26
status: recorded
purpose: The P7 policy comparison on a synthetic world that learns, and the decisions it makes on the five-term score, the decay term and the other acceptance thresholds of docs/plan/10.
---

# P7 simulation record

Written by `tools/p7_evals.py` from `app/sim/p7_evals.py` and `app/sim/learning.py`, seed base 20270510, 200 synthetic students, 60 daily sessions after a diagnostic, every arm on the same students and seeds. Every number is a simulation's measurement on synthetic students whose world model is invented. None is a human's measurement and none is a real student's. A simulation can falsify a policy choice and cannot validate one.

The world learns. Each student starts from the P2 knowledge state, closed under hard prerequisites, and carries a learning rate per skill drawn uniformly from 0.05 to 0.3. An attempt can teach a loaded skill whose hard parents are all known, with that rate scaled by the fading stage the item was served at (example 1.0, completion 0.75, unsupported 0.5). True mastery per item is the sum, over skills learned during the run, of the student's chance of retrieving each skill the day after the run, divided by items served; delayed mastery per item is the same sum 30 days after the run. The world is `learning.WORLD`: keyed draws, consolidated prior knowledge and daily half-life growth (`docs/operator/selection-study.md`). Retention at day 7 and day 30 is the mean retrieval chance over every known skill that many days after the run with no practice. Bias is 10's measurement bias, the mean of sigmoid(m_k) minus the retrieval chance over observed skills. The learning band and the stage multipliers are [inferred]; no source gives them.

## Forgetting curve: exponential

| Arm | Items | Skills learned | True mastery per item | Delayed mastery per item | Retention day 7 | Retention day 30 | Bias | Declared | Declared, not known | Placed, not known |
|---|---|---|---|---|---|---|---|---|---|---|
| two_term | 126997 | 15074 | 0.01211 | 0.00227 | 0.5764 | 0.5399 | +0.2039 | 3051 | 29 | 29 of 334 |
| random_control | 127108 | 15168 | 0.01227 | 0.00225 | 0.5754 | 0.5387 | +0.2038 | 3073 | 30 | 30 of 334 |
| five_term | 125424 | 12469 | 0.01048 | 0.00299 | 0.6150 | 0.5796 | +0.2090 | 4845 | 29 | 29 of 335 |
| no_interleaving | 127137 | 15138 | 0.01210 | 0.00237 | 0.5758 | 0.5394 | +0.2039 | 3158 | 29 | 29 of 334 |
| no_propagation | 127034 | 15098 | 0.01208 | 0.00233 | 0.5761 | 0.5398 | +0.2004 | 3034 | 29 | 29 of 333 |
| decay_lambda_2 | 126997 | 15086 | 0.01211 | 0.00227 | 0.5762 | 0.5398 | +0.2039 | 3051 | 29 | 29 of 334 |
| compensatory_only | 126997 | 15074 | 0.01211 | 0.00227 | 0.5764 | 0.5399 | +0.2039 | 3051 | 29 | 29 of 334 |
| stage_high_0_6 | 128036 | 15020 | 0.01216 | 0.00232 | 0.5776 | 0.5410 | +0.2043 | 3247 | 29 | 29 of 335 |
| stage_high_0_7 | 127280 | 15160 | 0.01209 | 0.00227 | 0.5752 | 0.5388 | +0.2039 | 3122 | 29 | 29 of 334 |
| stage_high_0_8 | 127086 | 15116 | 0.01215 | 0.00227 | 0.5759 | 0.5394 | +0.2038 | 3074 | 29 | 29 of 334 |

- Two-term against the random-within-fringe control, mean paired difference in true mastery per item -0.00016 [-0.00057, +0.00025]. Bar: the interval not wholly below 0. Passes: yes. Two-term matched or beat the control for 69.0% of 200 students; the 90% share 10 first stated is kept for reference.
- Five-term against two-term, mean paired difference in true mastery per item -0.00163 [-0.00232, -0.00093]. Bar: the 95% interval of the paired mean difference wholly above 0. Five-term turned on: no. Five-term beat two-term for 39.0% of 200 students.
- Decay term, arm 6 against arm 1, mean paired difference +0.00000 [-0.00000, +0.00001] in true mastery per item and -0.00016 [-0.00031, -0.00000] in retention at day 30. Bar: the 95% interval of the paired mean difference wholly above 0 on either. lambda returns to 2.0: no. lambda 2.0 beat lambda 0 for 3.5% and 0.0% of 200 students.
- Interleaving removed, mean paired difference in retention at day 30 -0.00054 [-0.00328, +0.00219]. Bar: the 95% interval of the paired mean difference wholly above 0 means the constraint costs retention. It costs retention: no. Retention was higher without interleaving for 34.5% of 200 students.
- Measurement bias: two-term +0.2039, control +0.2038. Within 0.05 in absolute value: yes.
- False mastery: the worst arm, random_control, declared 1.0% of its masteries on skills the student did not know. Ceiling 5%. Within: yes. Set apart the diagnostic's placements, the worst arm's share among masteries declared from practice is 0.0%.

## Forgetting curve: power law

| Arm | Items | Skills learned | True mastery per item | Delayed mastery per item | Retention day 7 | Retention day 30 | Bias | Declared | Declared, not known | Placed, not known |
|---|---|---|---|---|---|---|---|---|---|---|
| two_term | 126562 | 15066 | 0.02434 | 0.01163 | 0.5992 | 0.5486 | +0.1881 | 2938 | 29 | 29 of 334 |
| random_control | 126713 | 15181 | 0.02463 | 0.01176 | 0.5983 | 0.5475 | +0.1878 | 2933 | 30 | 30 of 334 |
| five_term | 125176 | 12330 | 0.02070 | 0.01110 | 0.6348 | 0.5862 | +0.1978 | 4876 | 29 | 29 of 335 |
| no_interleaving | 126757 | 15227 | 0.02478 | 0.01206 | 0.5986 | 0.5479 | +0.1873 | 3028 | 29 | 29 of 333 |
| no_propagation | 126547 | 15132 | 0.02468 | 0.01178 | 0.5991 | 0.5482 | +0.1836 | 2953 | 29 | 29 of 334 |
| decay_lambda_2 | 126562 | 15078 | 0.02435 | 0.01164 | 0.5991 | 0.5484 | +0.1881 | 2938 | 29 | 29 of 334 |
| compensatory_only | 126562 | 15066 | 0.02434 | 0.01163 | 0.5992 | 0.5486 | +0.1881 | 2938 | 29 | 29 of 334 |
| stage_high_0_6 | 127438 | 15032 | 0.02446 | 0.01167 | 0.6005 | 0.5495 | +0.1881 | 3082 | 29 | 29 of 335 |
| stage_high_0_7 | 126896 | 15129 | 0.02441 | 0.01166 | 0.5987 | 0.5480 | +0.1881 | 2994 | 29 | 29 of 334 |
| stage_high_0_8 | 126673 | 15076 | 0.02437 | 0.01164 | 0.5992 | 0.5485 | +0.1881 | 2948 | 29 | 29 of 334 |

- Two-term against the random-within-fringe control, mean paired difference in true mastery per item -0.00029 [-0.00071, +0.00013]. Bar: the interval not wholly below 0. Passes: yes. Two-term matched or beat the control for 68.5% of 200 students; the 90% share 10 first stated is kept for reference.
- Five-term against two-term, mean paired difference in true mastery per item -0.00365 [-0.00430, -0.00300]. Bar: the 95% interval of the paired mean difference wholly above 0. Five-term turned on: no. Five-term beat two-term for 19.0% of 200 students.
- Decay term, arm 6 against arm 1, mean paired difference +0.00001 [-0.00000, +0.00003] in true mastery per item and -0.00014 [-0.00028, -0.00000] in retention at day 30. Bar: the 95% interval of the paired mean difference wholly above 0 on either. lambda returns to 2.0: no. lambda 2.0 beat lambda 0 for 3.5% and 0.0% of 200 students.
- Interleaving removed, mean paired difference in retention at day 30 -0.00063 [-0.00281, +0.00155]. Bar: the 95% interval of the paired mean difference wholly above 0 means the constraint costs retention. It costs retention: no. Retention was higher without interleaving for 35.0% of 200 students.
- Measurement bias: two-term +0.1881, control +0.1878. Within 0.05 in absolute value: yes.
- False mastery: the worst arm, random_control, declared 1.0% of its masteries on skills the student did not know. Ceiling 5%. Within: yes. Set apart the diagnostic's placements, the worst arm's share among masteries declared from practice is 0.0%.

## Reading the table

Arms that served every student exactly what two-term served, item for item: exponential, compensatory_only; power law, compensatory_only. Since stage 12, p_A is read at today's retrievability in the stage bands and the review floor, the two places two-term selection reads `sigmoid(m_k)`, so `LAMBDA` 2.0 can change the fading stage a candidate is served at and, once that changes an outcome, everything served after it. It never enters the choice between candidates directly, because due coverage reads retrievability through the due test and never through `m_k`. The compensatory prediction is read only by the stage bands of skills with no credited observation. The study of the controls, the noise floor and the longer horizon is `docs/operator/selection-study.md`.

Retention at day 7 and day 30 averages over every known skill, including skills known from the start and never practised, which sit at 1.0. An arm that teaches fewer skills keeps a higher mean, so an arm can lead on retention while losing on true mastery per item.

## Decisions

A setting changes only when it clears its bar under both forgetting curves, so no decision rests on a curve shape the world model invented. Since the operator's ruling of 2026-09-27 (BUILD-LEDGER.md), 10's "on at least 90 percent of simulated students" is decided by the paired mean difference and its 95 percent interval (normal approximation), because on this world the same policy against itself wins on 47 to 58 percent of students and even controls that read the hidden student reach 90 percent in one setting of eight (`docs/operator/selection-study.md`). The share is kept and reported.

- The five-term score, `W_LEARN`, `W_COV`, `W_WEIGHT`, `W_REP` and `EXPLORE_SHARE`: stays off.
- `lambda`: stays 0.
