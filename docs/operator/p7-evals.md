---
title: P7 simulation record
research_date: 2026-09-26
status: recorded
purpose: The P7 policy comparison on a synthetic world that learns, and the decisions it makes on the five-term score, the decay term and the other acceptance thresholds of docs/plan/10.
---

# P7 simulation record

Written by `tools/p7_evals.py` from `app/sim/p7_evals.py` and `app/sim/learning.py`, seed base 20270510, 200 synthetic students, 60 daily sessions after a diagnostic, every arm on the same students and seeds. Every number is a simulation's measurement on synthetic students whose world model is invented. None is a human's measurement and none is a real student's. A simulation can falsify a policy choice and cannot validate one.

The world learns. Each student starts from the P2 knowledge state, closed under hard prerequisites, and carries a learning rate per skill drawn uniformly from 0.05 to 0.3. An attempt can teach a loaded skill whose hard parents are all known, with that rate scaled by the fading stage the item was served at (example 1.0, completion 0.75, unsupported 0.5). True mastery per item is the sum, over skills learned during the run, of the student's chance of retrieving each skill the day after the run, divided by items served. Retention at day 7 and day 30 is the mean retrieval chance over every known skill that many days after the run with no practice. Bias is 10's measurement bias, the mean of sigmoid(m_k) minus the retrieval chance over observed skills. The learning band and the stage multipliers are [inferred]; no source gives them.

## Forgetting curve: exponential

| Arm | Items | Skills learned | True mastery per item | Retention day 7 | Retention day 30 | Bias | Declared | Declared, not known | Placed, not known |
|---|---|---|---|---|---|---|---|---|---|
| two_term | 121175 | 14948 | 0.01021 | 0.5074 | 0.4892 | +0.2464 | 1327 | 29 | 29 of 329 |
| random_control | 121273 | 15044 | 0.01048 | 0.5065 | 0.4879 | +0.2459 | 1309 | 29 | 29 of 329 |
| five_term | 120481 | 12294 | 0.00929 | 0.6030 | 0.5861 | +0.2215 | 2763 | 29 | 29 of 329 |
| no_interleaving | 121453 | 15115 | 0.01070 | 0.5043 | 0.4857 | +0.2464 | 1317 | 29 | 29 of 329 |
| no_propagation | 121269 | 14892 | 0.01022 | 0.5089 | 0.4907 | +0.2428 | 1326 | 29 | 29 of 330 |
| decay_lambda_2 | 121175 | 14948 | 0.01021 | 0.5074 | 0.4892 | +0.2464 | 1327 | 29 | 29 of 329 |
| compensatory_only | 121175 | 14948 | 0.01021 | 0.5074 | 0.4892 | +0.2464 | 1327 | 29 | 29 of 329 |
| stage_high_0_6 | 121986 | 14836 | 0.01052 | 0.5141 | 0.4952 | +0.2427 | 1420 | 29 | 29 of 329 |
| stage_high_0_7 | 121430 | 14944 | 0.01030 | 0.5089 | 0.4907 | +0.2459 | 1345 | 29 | 29 of 329 |
| stage_high_0_8 | 121190 | 14955 | 0.01023 | 0.5075 | 0.4892 | +0.2462 | 1329 | 29 | 29 of 329 |

- Two-term against the random-within-fringe control: two-term matched or beat the control on true mastery per item for 73.0% of 200 students. Bar 90%. Passes: no.
- Five-term against two-term: five-term beat two-term on true mastery per item for 40.0% of 200 students. Bar 90%. Five-term turned on: no.
- Decay term, arm 6 against arm 1: lambda 2.0 beat lambda 0 on true mastery per item for 0.0% and on retention at day 30 for 0.0% of 200 students. Bar 90% on either. lambda returns to 2.0: no.
- Interleaving removed: mean retention at day 30 moved by -0.0035 against two-term, and was higher without interleaving for 32.0% of 200 students. Bar 90%. The constraint costs retention: no.
- Measurement bias: two-term +0.2464, control +0.2459. Within 0.05 in absolute value: yes.
- False mastery: the worst arm, random_control, declared 2.2% of its masteries on skills the student did not know. Ceiling 5%. Within: yes. Set apart the diagnostic's placements, the worst arm's share among masteries declared from practice is 0.0%.

## Forgetting curve: power law

| Arm | Items | Skills learned | True mastery per item | Retention day 7 | Retention day 30 | Bias | Declared | Declared, not known | Placed, not known |
|---|---|---|---|---|---|---|---|---|---|
| two_term | 120739 | 15064 | 0.02342 | 0.5523 | 0.5208 | +0.2168 | 1150 | 29 | 29 of 326 |
| random_control | 120813 | 15029 | 0.02335 | 0.5533 | 0.5219 | +0.2165 | 1150 | 30 | 30 of 326 |
| five_term | 119304 | 12211 | 0.01969 | 0.6355 | 0.6071 | +0.2031 | 2440 | 29 | 29 of 328 |
| no_interleaving | 121127 | 14941 | 0.02304 | 0.5537 | 0.5222 | +0.2172 | 1242 | 29 | 29 of 327 |
| no_propagation | 120764 | 15076 | 0.02343 | 0.5525 | 0.5210 | +0.2133 | 1142 | 29 | 29 of 327 |
| decay_lambda_2 | 120739 | 15064 | 0.02342 | 0.5523 | 0.5208 | +0.2168 | 1150 | 29 | 29 of 326 |
| compensatory_only | 120739 | 15064 | 0.02342 | 0.5523 | 0.5208 | +0.2168 | 1150 | 29 | 29 of 326 |
| stage_high_0_6 | 121737 | 14929 | 0.02342 | 0.5566 | 0.5248 | +0.2153 | 1273 | 29 | 29 of 326 |
| stage_high_0_7 | 121029 | 15036 | 0.02323 | 0.5532 | 0.5220 | +0.2167 | 1190 | 29 | 29 of 326 |
| stage_high_0_8 | 120765 | 15061 | 0.02341 | 0.5526 | 0.5212 | +0.2166 | 1157 | 29 | 29 of 326 |

- Two-term against the random-within-fringe control: two-term matched or beat the control on true mastery per item for 78.0% of 200 students. Bar 90%. Passes: no.
- Five-term against two-term: five-term beat two-term on true mastery per item for 21.0% of 200 students. Bar 90%. Five-term turned on: no.
- Decay term, arm 6 against arm 1: lambda 2.0 beat lambda 0 on true mastery per item for 0.0% and on retention at day 30 for 0.0% of 200 students. Bar 90% on either. lambda returns to 2.0: no.
- Interleaving removed: mean retention at day 30 moved by +0.0014 against two-term, and was higher without interleaving for 37.5% of 200 students. Bar 90%. The constraint costs retention: no.
- Measurement bias: two-term +0.2168, control +0.2165. Within 0.05 in absolute value: yes.
- False mastery: the worst arm, random_control, declared 2.6% of its masteries on skills the student did not know. Ceiling 5%. Within: yes. Set apart the diagnostic's placements, the worst arm's share among masteries declared from practice is 0.0%.

## Reading the table

Arms that served every student exactly what two-term served, item for item: exponential, decay_lambda_2, compensatory_only; power law, decay_lambda_2, compensatory_only. Under two-term selection `LAMBDA` reaches only `sigmoid(m_k)` taken with a retrievability argument. The fringe, block 1's due coverage and the mastery rule read none of that, so the decay term has no path into what is served, and arm 6 cannot pass its gate by construction. Its failure is not evidence that decay is useless. The compensatory prediction is read only by the stage bands of skills with no credited observation.

Retention at day 7 and day 30 averages over every known skill, including skills known from the start and never practised, which sit at 1.0. An arm that teaches fewer skills keeps a higher mean, so an arm can lead on retention while losing on true mastery per item.

## Decisions

A setting changes only when it clears its bar under both forgetting curves, so no decision rests on a curve shape the world model invented.

- The five-term score, `W_LEARN`, `W_COV`, `W_WEIGHT`, `W_REP` and `EXPLORE_SHARE`: stays off.
- `lambda`: stays 0.
