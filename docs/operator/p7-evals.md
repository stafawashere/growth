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
| two_term | 151300 | 7777 | 0.04529 | 0.03053 | 0.8744 | 0.8161 | +0.0506 | 10896 | 1 | 0 of 432 |
| random_control | 151812 | 8437 | 0.04831 | 0.03113 | 0.8702 | 0.8093 | +0.0406 | 11749 | 0 | 0 of 432 |
| five_term | 149549 | 6953 | 0.03876 | 0.02711 | 0.8699 | 0.8170 | +0.0584 | 10518 | 2 | 0 of 432 |
| no_interleaving | 151845 | 7643 | 0.04435 | 0.03035 | 0.8760 | 0.8185 | +0.0534 | 10782 | 1 | 0 of 433 |
| no_propagation | 151223 | 6965 | 0.04031 | 0.02866 | 0.8769 | 0.8229 | +0.0553 | 10404 | 0 | 0 of 428 |
| decay_lambda_2 | 151300 | 7780 | 0.04539 | 0.03061 | 0.8747 | 0.8163 | +0.0503 | 10909 | 0 | 0 of 432 |
| compensatory_only | 151274 | 7753 | 0.04512 | 0.03042 | 0.8745 | 0.8162 | +0.0505 | 10837 | 1 | 0 of 432 |
| stage_high_0_6 | 151255 | 7774 | 0.04531 | 0.03068 | 0.8751 | 0.8169 | +0.0503 | 10869 | 0 | 0 of 432 |
| stage_high_0_7 | 151299 | 7801 | 0.04538 | 0.03066 | 0.8744 | 0.8162 | +0.0503 | 10846 | 1 | 0 of 432 |
| stage_high_0_8 | 151300 | 7773 | 0.04524 | 0.03058 | 0.8744 | 0.8163 | +0.0510 | 10891 | 1 | 0 of 432 |

- Two-term against the random-within-fringe control, mean paired difference in true mastery per item -0.00301 [-0.00389, -0.00214]. Bar: the interval not wholly below 0. Passes: no. Two-term matched or beat the control for 29.5% of 200 students; the 90% share 10 first stated is kept for reference.
- Five-term against two-term, mean paired difference in true mastery per item -0.00653 [-0.00741, -0.00565]. Bar: the 95% interval of the paired mean difference wholly above 0. Five-term turned on: no. Five-term beat two-term for 16.5% of 200 students.
- Decay term, arm 6 against arm 1, mean paired difference +0.00010 [-0.00002, +0.00022] in true mastery per item and +0.00023 [+0.00000, +0.00047] in retention at day 30. Bar: the 95% interval of the paired mean difference wholly above 0 on either. lambda returns to 2.0: yes. lambda 2.0 beat lambda 0 for 2.5% and 3.5% of 200 students.
- Interleaving removed, mean paired difference in retention at day 30 +0.00241 [-0.00068, +0.00550]. Bar: the 95% interval of the paired mean difference wholly above 0 means the constraint costs retention. It costs retention: no. Retention was higher without interleaving for 56.0% of 200 students.
- Measurement bias: two-term +0.0506, control +0.0406. Within 0.05 in absolute value: yes.
- False mastery: the worst arm, five_term, declared 0.0% of its masteries on skills the student did not know. Ceiling 5%. Within: yes. Set apart the diagnostic's placements, the worst arm's share among masteries declared from practice is 0.0%.

## Forgetting curve: power law

| Arm | Items | Skills learned | True mastery per item | Delayed mastery per item | Retention day 7 | Retention day 30 | Bias | Declared | Declared, not known | Placed, not known |
|---|---|---|---|---|---|---|---|---|---|---|
| two_term | 151143 | 7607 | 0.04342 | 0.03048 | 0.8508 | 0.7884 | +0.0615 | 10624 | 0 | 0 of 431 |
| random_control | 151665 | 8273 | 0.04665 | 0.03156 | 0.8489 | 0.7836 | +0.0514 | 11426 | 0 | 0 of 427 |
| five_term | 149493 | 6817 | 0.03793 | 0.02748 | 0.8474 | 0.7887 | +0.0677 | 10283 | 1 | 0 of 432 |
| no_interleaving | 151704 | 7499 | 0.04274 | 0.03010 | 0.8511 | 0.7890 | +0.0638 | 10457 | 0 | 0 of 432 |
| no_propagation | 151085 | 6869 | 0.03937 | 0.02902 | 0.8522 | 0.7935 | +0.0671 | 10183 | 0 | 0 of 426 |
| decay_lambda_2 | 151143 | 7603 | 0.04339 | 0.03045 | 0.8508 | 0.7883 | +0.0615 | 10605 | 0 | 0 of 431 |
| compensatory_only | 151120 | 7609 | 0.04345 | 0.03047 | 0.8509 | 0.7885 | +0.0617 | 10573 | 0 | 0 of 431 |
| stage_high_0_6 | 151105 | 7609 | 0.04345 | 0.03044 | 0.8510 | 0.7885 | +0.0617 | 10605 | 0 | 0 of 432 |
| stage_high_0_7 | 151143 | 7622 | 0.04352 | 0.03051 | 0.8509 | 0.7884 | +0.0614 | 10616 | 0 | 0 of 432 |
| stage_high_0_8 | 151143 | 7619 | 0.04352 | 0.03050 | 0.8509 | 0.7884 | +0.0612 | 10644 | 0 | 0 of 432 |

- Two-term against the random-within-fringe control, mean paired difference in true mastery per item -0.00323 [-0.00401, -0.00245]. Bar: the interval not wholly below 0. Passes: no. Two-term matched or beat the control for 27.5% of 200 students; the 90% share 10 first stated is kept for reference.
- Five-term against two-term, mean paired difference in true mastery per item -0.00549 [-0.00638, -0.00460]. Bar: the 95% interval of the paired mean difference wholly above 0. Five-term turned on: no. Five-term beat two-term for 19.5% of 200 students.
- Decay term, arm 6 against arm 1, mean paired difference -0.00003 [-0.00012, +0.00005] in true mastery per item and -0.00004 [-0.00012, +0.00005] in retention at day 30. Bar: the 95% interval of the paired mean difference wholly above 0 on either. lambda returns to 2.0: no. lambda 2.0 beat lambda 0 for 1.0% and 1.0% of 200 students.
- Interleaving removed, mean paired difference in retention at day 30 +0.00057 [-0.00228, +0.00343]. Bar: the 95% interval of the paired mean difference wholly above 0 means the constraint costs retention. It costs retention: no. Retention was higher without interleaving for 52.0% of 200 students.
- Measurement bias: two-term +0.0615, control +0.0514. Within 0.05 in absolute value: yes.
- False mastery: the worst arm, five_term, declared 0.0% of its masteries on skills the student did not know. Ceiling 5%. Within: yes. Set apart the diagnostic's placements, the worst arm's share among masteries declared from practice is 0.0%.

## Reading the table

Arms that served every student exactly what two-term served, item for item: exponential, none; power law, none. Since stage 12, p_A is read at today's retrievability in the stage bands and the review floor, the two places two-term selection reads `sigmoid(m_k)`, so `LAMBDA` 2.0 can change the fading stage a candidate is served at and, once that changes an outcome, everything served after it. It never enters the choice between candidates directly, because due coverage reads retrievability through the due test and never through `m_k`. The compensatory prediction is read only by the stage bands of skills with no credited observation. The study of the controls, the noise floor and the longer horizon is `docs/operator/selection-study.md`.

Retention at day 7 and day 30 averages over every known skill, including skills known from the start and never practised, which sit at 1.0. An arm that teaches fewer skills keeps a higher mean, so an arm can lead on retention while losing on true mastery per item.

## Decisions

A setting changes only when it clears its bar under both forgetting curves, so no decision rests on a curve shape the world model invented. Since the operator's ruling of 2026-09-27 (BUILD-LEDGER.md), 10's "on at least 90 percent of simulated students" is decided by the paired mean difference and its 95 percent interval (normal approximation), because on this world the same policy against itself wins on 47 to 58 percent of students and even controls that read the hidden student reach 90 percent in one setting of eight (`docs/operator/selection-study.md`). The share is kept and reported.

- The five-term score, `W_LEARN`, `W_COV`, `W_WEIGHT`, `W_REP` and `EXPLORE_SHARE`: stays off.
- `lambda`: stays 0.
