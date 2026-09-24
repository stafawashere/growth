---
title: P7 simulation record
research_date: 2026-09-24
status: recorded
purpose: The P7 policy comparison on a synthetic world that learns, and the decisions it makes on the five-term score, the decay term and the other acceptance thresholds of docs/plan/10.
---

# P7 simulation record

Written by `tools/p7_evals.py` from `app/sim/p7_evals.py` and `app/sim/learning.py`, seed base 20270510, 200 synthetic students, 60 daily sessions after a diagnostic, every arm on the same students and seeds. Every number is a simulation's measurement on synthetic students whose world model is invented. None is a human's measurement and none is a real student's. A simulation can falsify a policy choice and cannot validate one.

The world learns. Each student starts from the P2 knowledge state, closed under hard prerequisites, and carries a learning rate per skill drawn uniformly from 0.05 to 0.3. An attempt can teach a loaded skill whose hard parents are all known, with that rate scaled by the fading stage the item was served at (example 1.0, completion 0.75, unsupported 0.5). True mastery per item is the sum, over skills learned during the run, of the student's chance of retrieving each skill the day after the run, divided by items served. Retention at day 7 and day 30 is the mean retrieval chance over every known skill that many days after the run with no practice. Bias is 10's measurement bias, the mean of sigmoid(m_k) minus the retrieval chance over observed skills. The learning band and the stage multipliers are [inferred]; no source gives them.

## Forgetting curve: exponential

| Arm | Items | Skills learned | True mastery per item | Retention day 7 | Retention day 30 | Bias | Declared | Declared, not known | Placed, not known | Seeded, not known |
|---|---|---|---|---|---|---|---|---|---|---|
| two_term | 121652 | 14724 | 0.01092 | 0.5232 | 0.5036 | +0.2470 | 3681 | 795 | 210 of 1625 | 585 of 1137 |
| random_control | 122018 | 14788 | 0.01055 | 0.5243 | 0.5059 | +0.2453 | 3705 | 817 | 214 of 1626 | 603 of 1138 |
| five_term | 120558 | 12026 | 0.00905 | 0.6156 | 0.5985 | +0.2229 | 5050 | 833 | 211 of 1629 | 622 of 1138 |
| no_interleaving | 122146 | 14622 | 0.01051 | 0.5260 | 0.5072 | +0.2461 | 3769 | 803 | 209 of 1626 | 594 of 1137 |
| no_propagation | 121560 | 14732 | 0.01077 | 0.5240 | 0.5050 | +0.2426 | 3698 | 792 | 213 of 1627 | 579 of 1135 |
| decay_lambda_2 | 121652 | 14724 | 0.01092 | 0.5232 | 0.5036 | +0.2470 | 3681 | 795 | 210 of 1625 | 585 of 1137 |
| compensatory_only | 121652 | 14724 | 0.01092 | 0.5232 | 0.5036 | +0.2470 | 3681 | 795 | 210 of 1625 | 585 of 1137 |
| stage_high_0_6 | 122694 | 14625 | 0.01077 | 0.5270 | 0.5081 | +0.2453 | 3817 | 797 | 208 of 1633 | 589 of 1140 |
| stage_high_0_7 | 121841 | 14747 | 0.01091 | 0.5231 | 0.5035 | +0.2467 | 3714 | 796 | 210 of 1625 | 586 of 1137 |
| stage_high_0_8 | 121673 | 14717 | 0.01091 | 0.5233 | 0.5038 | +0.2470 | 3684 | 796 | 210 of 1625 | 586 of 1137 |

- Two-term against the random-within-fringe control: two-term matched or beat the control on true mastery per item for 67.5% of 200 students. Bar 90%. Passes: no.
- Five-term against two-term: five-term beat two-term on true mastery per item for 35.0% of 200 students. Bar 90%. Five-term turned on: no.
- Decay term, arm 6 against arm 1: lambda 2.0 beat lambda 0 on true mastery per item for 0.0% and on retention at day 30 for 0.0% of 200 students. Bar 90% on either. lambda returns to 2.0: no.
- Interleaving removed: mean retention at day 30 moved by +0.0036 against two-term, and was higher without interleaving for 40.5% of 200 students. Bar 90%. The constraint costs retention: no.
- Measurement bias: two-term +0.2470, control +0.2453. Within 0.05 in absolute value: yes.
- False mastery: the worst arm, random_control, declared 22.1% of its masteries on skills the student did not know. Ceiling 5%. Within: no. Set apart the diagnostic's placements and the seeded parents of `app/session/seed.py`, the worst arm's share among masteries declared from practice is 0.0%.

## Forgetting curve: power law

| Arm | Items | Skills learned | True mastery per item | Retention day 7 | Retention day 30 | Bias | Declared | Declared, not known | Placed, not known | Seeded, not known |
|---|---|---|---|---|---|---|---|---|---|---|
| two_term | 121289 | 14723 | 0.02306 | 0.5695 | 0.5390 | +0.2176 | 3527 | 800 | 214 of 1615 | 586 of 1129 |
| random_control | 121678 | 14807 | 0.02310 | 0.5671 | 0.5366 | +0.2192 | 3502 | 817 | 212 of 1620 | 605 of 1134 |
| five_term | 119592 | 11927 | 0.01919 | 0.6467 | 0.6194 | +0.2058 | 4677 | 837 | 211 of 1624 | 626 of 1137 |
| no_interleaving | 121364 | 14637 | 0.02286 | 0.5701 | 0.5395 | +0.2185 | 3513 | 807 | 210 of 1615 | 597 of 1131 |
| no_propagation | 121008 | 14682 | 0.02285 | 0.5695 | 0.5393 | +0.2146 | 3513 | 798 | 211 of 1612 | 587 of 1132 |
| decay_lambda_2 | 121289 | 14723 | 0.02306 | 0.5695 | 0.5390 | +0.2176 | 3527 | 800 | 214 of 1615 | 586 of 1129 |
| compensatory_only | 121289 | 14723 | 0.02306 | 0.5695 | 0.5390 | +0.2176 | 3527 | 800 | 214 of 1615 | 586 of 1129 |
| stage_high_0_6 | 121994 | 14609 | 0.02286 | 0.5716 | 0.5409 | +0.2176 | 3607 | 793 | 210 of 1622 | 583 of 1136 |
| stage_high_0_7 | 121484 | 14744 | 0.02315 | 0.5695 | 0.5388 | +0.2172 | 3531 | 800 | 214 of 1616 | 586 of 1129 |
| stage_high_0_8 | 121289 | 14723 | 0.02306 | 0.5695 | 0.5390 | +0.2176 | 3527 | 800 | 214 of 1615 | 586 of 1129 |

- Two-term against the random-within-fringe control: two-term matched or beat the control on true mastery per item for 59.5% of 200 students. Bar 90%. Passes: no.
- Five-term against two-term: five-term beat two-term on true mastery per item for 21.5% of 200 students. Bar 90%. Five-term turned on: no.
- Decay term, arm 6 against arm 1: lambda 2.0 beat lambda 0 on true mastery per item for 0.0% and on retention at day 30 for 0.0% of 200 students. Bar 90% on either. lambda returns to 2.0: no.
- Interleaving removed: mean retention at day 30 moved by +0.0004 against two-term, and was higher without interleaving for 36.5% of 200 students. Bar 90%. The constraint costs retention: no.
- Measurement bias: two-term +0.2176, control +0.2192. Within 0.05 in absolute value: yes.
- False mastery: the worst arm, random_control, declared 23.3% of its masteries on skills the student did not know. Ceiling 5%. Within: no. Set apart the diagnostic's placements and the seeded parents of `app/session/seed.py`, the worst arm's share among masteries declared from practice is 0.0%.

## Reading the table

Arms that served every student exactly what two-term served, item for item: exponential, decay_lambda_2, compensatory_only; power law, decay_lambda_2, compensatory_only, stage_high_0_8. Under two-term selection `LAMBDA` reaches only `sigmoid(m_k)` taken with a retrievability argument. The fringe, block 1's due coverage and the mastery rule read none of that, so the decay term has no path into what is served, and arm 6 cannot pass its gate by construction. Its failure is not evidence that decay is useless. The compensatory prediction is read only by the stage bands of skills with no credited observation.

Retention at day 7 and day 30 averages over every known skill, including skills known from the start and never practised, which sit at 1.0. An arm that teaches fewer skills keeps a higher mean, so an arm can lead on retention while losing on true mastery per item.

## Decisions

A setting changes only when it clears its bar under both forgetting curves, so no decision rests on a curve shape the world model invented.

- The five-term score, `W_LEARN`, `W_COV`, `W_WEIGHT`, `W_REP` and `EXPLORE_SHARE`: stays off.
- `lambda`: stays 0.
