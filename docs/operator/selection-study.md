---
title: Selection study
research_date: 2026-09-27
status: recorded
purpose: Whether the P7 learning world can tell selection policies apart, what the plan's selection bars say on it, and the ruling on the bars that only the operator can make. Simulation only.
---

# Selection study

Stage 12 asked whether the stage 8 result (two-term matched or beat the random-within-fringe control on 67.5 and 59.5 percent of 200 students, against 10's 90 percent bar) was a fault of the selection policy or of the simulator, and whether the decay term could be given a path into what is served. Every number here is a simulation's measurement on synthetic students whose world model is invented; none is a person's and none is the student's. Every judgement here is the model's (Claude, working on the operator's delegation), not a person's. The numbers, with intervals, are in [selection-study-record.md](selection-study-record.md), written by `tools/selection_study.py` from seed base 20270510.

## What was run [verified]

Worlds (`app/sim/learning.py`, WorldRules):

| World | Keyed draws | Prior knowledge | Half-life growth | Use |
|---|---|---|---|---|
| `legacy` | no, one stream per student | retention 1.0 until first practised, then the initial half-life | on every correct answer | reproduces the stage 8 record |
| `legacy_keyed` | yes | as legacy | as legacy | isolates what keyed draws do to the noise floor |
| `fixed` | yes | starts at the capped half-life, 365 days | at most once per calendar day | every result below unless named |

Fixed simulator parameters, all unchanged from stage 8 except the three rules above: learning rate per skill uniform on 0.05 to 0.30, scaled by the served stage (example 1.0, completion 0.75, unsupported 0.5); initial half-life 5 days, growth 1.7 per retrieval, cap 365 days; slip 0.10; short-answer guess 0.02, MCQ floor 0.25; unit ability uniform on -3 to 3; 3 synthetic items per active archetype; 3 forecast minutes per attempt; start day 2026-10-01; a diagnostic, then one assembled session a day. Horizons: 60 days (stage 8's) and 226 days (2026-09-26 to the exam on 2027-05-10). 200 students per arm, every arm on the same students.

Arms, beyond 10's: `two_term_reseeded` (two-term with only the engine's draws reseeded after the diagnostic, the noise floor), `oracle_forgetting` (the positive control the brief names: block 2 serves the candidate reaching the student's truly least-retained known skill), `oracle_teaching` (a second positive control aimed at what mastery per item counts: the candidate whose loaded skills the student is ready to learn at the highest summed rate), `most_recent` (the negative control: the candidate loading the skill the student most recently learned), and `five_term_lambda_2` (informational, the only place the plan lets `lambda` move which archetype is chosen). Controls act in block 2 only; blocks 1 and 3 run the shipped policy in every arm.

Measures: mastery per item (stage 8's, retention of skills learned in the run, read the day after it, per item), delayed mastery per item (the same skills 30 days after the run, per item, added here), and retention at day 30 (10's, over every known skill).

## Step 1: can the simulator tell policies apart? [verified, simulation]

**Two-term's one non-random term rarely fires.** Over the first 20 students under two-term on the fixed world, due coverage was above 0 for any candidate on 145 of 13,166 block 2 choices (1.1 percent) in 60 days and 4,082 of 54,666 (7.5 percent) in 226 days. On every other choice two-term draws uniformly from the gated fringe, which is what the control does. The reason is that due coverage needs a skill the engine has declared mastered whose retrievability has fallen below 0.90, and practice declares few: a mean of 13.6 skills per student in 60 days and 32.2 in 226 on the fixed world, 5.0 in 60 days on the legacy world. So on this world two-term and the control are nearly the same policy, and the stage 8 comparison compared a policy with itself.

**Most of stage 8's share was ties.** On the legacy world, where the stage 8 record now reads 73.0 and 78.0 percent, two-term served 106 and 116 of 200 students exactly what the control served. The strict wins were 35 of 200 (17.5 percent, 95% CI 12.9 to 23.4) and 36 of 200 (18.0, 13.3 to 23.9). The mean paired difference in mastery per item was -0.00027 (-0.00061 to 0.00007) and +0.00007 (-0.00027 to 0.00042), both intervals across 0.

**The noise floor is 50 percent, plus or minus about 7.** Two-term against itself with reseeded engine draws, share of students on whom the reseeded run beat the original on mastery per item:

| World, horizon | Exponential | Power law |
|---|---|---|
| legacy, 60 days | 56.5% [49.6, 63.2] | 48.5% [41.7, 55.4] |
| legacy_keyed, 60 days | 57.5% [50.6, 64.1] | 47.0% [40.2, 53.9] |
| fixed, 60 days | 51.5% [44.6, 58.3] | 56.0% [49.1, 62.7] |
| fixed, 226 days | 54.0% [47.1, 60.8] | 51.0% [44.1, 57.8] |

No run tied, so "matched or beat" equals "beat" here. The 67.5 and 59.5 percent of stage 8 and the 73.0 and 78.0 percent of the current record therefore sit within reach of a policy identical to the control once ties are counted as matches, which is what the record's reading of "no more items than the control" does.

**Pairing.** Every arm already shared the student's seed, the student's parameters and the diagnostic. The world's draws came from one stream per student, so they matched only until two arms first served different items. Keyed draws (`KeyedDraws`) now give every roll its own uniform, fixed by the student and by what is rolled, so two arms serving the same item on the same day see the same outcome. That makes the comparison paired in its draws as well as its student, and it did not narrow the noise floor (57.5 against 56.5 percent, 47.0 against 48.5), because the per-student noise comes from the policy path diverging, after which the arms serve different items and no draw alignment can pair them. The model's judgement: the noise is intrinsic to comparing policies one student at a time on this world, not a harness defect.

**The controls separate from random, and the bad control separates in the same direction as the good one.** Share of students on whom the control beat random, fixed world:

| Control | 60 d, exp, mastery | 60 d, exp, delayed | 60 d, power, mastery | 60 d, power, delayed | 226 d, exp, mastery | 226 d, exp, delayed | 226 d, power, mastery | 226 d, power, delayed |
|---|---|---|---|---|---|---|---|---|
| oracle_forgetting | 46.0 | 91.0 | 24.0 | 56.0 | 73.0 | 83.0 | 39.5 | 48.0 |
| oracle_teaching | 49.5 | 17.5 | 84.5 | 83.5 | 6.0 | 10.5 | 12.0 | 16.0 |
| most_recent | 44.0 | 88.5 | 30.5 | 57.0 | 73.0 | 83.5 | 42.0 | 47.0 |

Each cell is a percent of 200 students with a Wilson interval of about plus or minus 5 to 7 in the record. The controls move the measures by far more than the noise floor, so the simulator can measure a large selection effect. What it cannot do is tell good spacing from bad. The negative control, which re-serves whatever was learned most recently, scores within 7 points of the forgetting oracle in every cell and ahead of it in four of the eight. The reason is in the world: a retrieval grows the half-life by the same factor whatever the lag since the last one, so a skill practised every day reaches the cap in about 8 days and the world never rewards waiting. 01's spacing evidence (Cepeda et al 2008, Rohrer and Taylor 2006) is about the lag, and nothing in this world depends on the lag beyond the once-a-day rule. No control reaches 90 percent on both curves; the best single cell is the forgetting oracle's 91.0 percent [86.2, 94.2], and on the other curve the same oracle scores 56.0.

**Horizon and metric.** 60 days spans the initial half-life (5 days) about 12 times, but not the engine's own timescale: mastery needs three unsupported successes over at least 7 days, and a mastered skill only comes due weeks later, so due coverage fires on 1.1 percent of choices at 60 days and 7.5 percent at 226. Mastery per item reads retention the day after the run, when a skill practised in the last days is near 1.0 whatever the schedule; that measure cannot see spacing, so delayed mastery per item (30 days after the run, 10's day-30 delay applied to the skills the run taught) was added. The existing measures are kept. Retention at day 30 averages over every known skill, including prior knowledge, so an arm that teaches less keeps a higher mean (the forgetting oracle learns 44 skills against random's 76 in 60 days and leads on it).

**Three world defects were fixed** (all in `app/sim/learning.py`, each tested and each switchable back through `LEGACY_WORLD`): draws keyed rather than streamed; prior knowledge starting at the capped half-life, where the stage 8 world held it at retention 1.0 until first practised and then let it decay from 5 days, so practising a known skill lowered its retention; and half-life growth at most once a calendar day, 01's "Same-day repeats | do not count" (Rohrer and Taylor 2006), where the stage 8 world grew it on every correct answer. The capped starting half-life is [inferred]; nothing gives the age of a student's prior knowledge.

## Step 2: the decay term's path [verified]

02 writes the strength as `beta_k + gamma * phi(c_k) + rho * phi(f_k) - lambda * (1 - R_k)` and mastery condition 1 as `sigmoid(m_k) >= 0.9` "at the current retrievability". Two-term selection reads `m_k` in exactly two places, the stage bands of `serve_stage` and the review floor of `review_eligible`, and both read it with no retrievability, so `lambda` could not reach anything served. Both now take today's retrievability map (`app/engine/fringe.py`, `app/engine/select.py`, `app/session/build.py`). At `LAMBDA = 0` the decay term is 0 and every served stage and eligibility is what it was; the path is live only when the switch is on. The update rule's condition 1 and un-mastery already read strength after the observation has set `last_practised_at` to today, where retrievability is about 1, so they were left alone: there the term is inert by construction and changing the order would change mastery for the live student. No weight was invented; `lambda` 2.0 is 02's own value.

Arm 6 now serves differently from two-term for 78 and 75 of 200 students at 60 days and 82 and 80 at 226 days (exponential, power law). `tests/eval/test_selection_study.py::test_the_decay_arm_serves_differently_from_two_term` was red with the retrievability argument removed from `serve_stage` and green with it restored. The difference is always a lower fading stage for a candidate whose loaded skills have decayed; two-term's choice between candidates reads retrievability only through the due test, never through `m_k`, so under two-term `lambda` can change support and never which archetype is picked. Under five-term, `lambda` reaches the choice through `W_LEARN`'s `p_A`.

## Step 3: the comparison at 10's bars [verified, simulation]

Fixed world, 200 students, paired on seeds. Shares are percent of students with Wilson 95% intervals; differences are mean paired differences with normal 95% intervals. The bars are 10's, read as stage 8 read them (Plan corrections, 2026-09-24), unchanged.

| Bar (10) | Horizon | Exponential | Power law | Clears |
|---|---|---|---|---|
| Two-term no worse than random on at least 90% of students (matched or beat, mastery per item) | 60 d | 69.0 [62.3, 75.0], diff -0.00016 [-0.00057, 0.00025] | 68.5 [61.8, 74.5], diff -0.00029 [-0.00071, 0.00013] | no |
| same | 226 d | 50.0 [43.1, 56.9], diff +0.00001 [-0.00009, 0.00011] | 55.0 [48.1, 61.7], diff +0.00004 [-0.00007, 0.00015] | no |
| Five-term beats two-term on at least 90% (mastery per item) | 60 d | 39.0 [32.5, 45.9], diff -0.00163 [-0.00232, -0.00093] | 19.0 [14.2, 25.0], diff -0.00365 [-0.00430, -0.00300] | no |
| same | 226 d | 55.5 [48.6, 62.2], diff +0.00009 [-0.00005, 0.00023] | 39.0 [32.5, 45.9], diff -0.00034 [-0.00051, -0.00016] | no |
| Arm 6 beats arm 1 on at least 90%, on mastery per item or on retention at day 30 | 60 d | 3.5 [1.7, 7.0] and 0.0 | 3.5 [1.7, 7.0] and 0.0 | no |
| same | 226 d | 0.0 [0.0, 1.9] and 0.0 | 0.0 [0.0, 1.9] and 0.0 | no |

On delayed mastery per item the picture is the same: five-term against two-term 57.5, 38.5, 57.0 and 41.0 percent; arm 6 3.5, 3.5, 0.0 and 0.0. `five_term_lambda_2` against `five_term` lost on retention at day 30 for 68.0, 73.0, 68.5 and 75.0 percent of students and was within noise on mastery per item. Every result sits well outside the noise floor on the side of failing, except two-term against random, which sits inside it.

## Step 4: what ships [inferred, the model's judgement]

Nothing live changes what the student is served. Two-term stays the live score, `LAMBDA` stays 0, the five-term score and `EXPLORE_SHARE` stay in `app/sim/five_term.py`, which nothing live imports. The retrievability path into the stage bands and the review floor ships, because at `LAMBDA = 0` it computes the same number, and `LAMBDA` is the switch that stays off (`test_the_live_decay_term_matches_the_recorded_decision`).

The decay decision is decided in this simulator in the direction it runs: arm 6 now differs from two-term and beats it on at most 3.5 percent of students, so `lambda` stays 0 on evidence rather than by construction. That decision carries the limit above: this world cannot reward spacing, and under two-term the term moves only the fading stage.

## The case for the operator [inferred, the model's judgement]

What the bars ask: that a policy beat (or, for two-term against random, match) another on at least 90 percent of simulated students, one student at a time.

What the noise allows: the same policy against itself wins on 47 to 58 percent of students. For a 90 percent per-student share, the policy's effect has to exceed each student's own run-to-run variation nine times in ten. On this world only the controls that read the hidden student come near it, and only in single cells (91.0 percent once, 88.5 once); none clears on both curves at either horizon.

What that means for each bar:

- Two-term against random cannot be decided by this simulator. The two policies differ on 1.1 to 7.5 percent of block 2 choices, their mean difference is within 0.0008 of 0 with intervals across 0 at every horizon and curve, and the share measure counts ties as matches, so it reads 69 percent at 60 days and 50 percent at 226 days for what is, within the noise, no difference. Failing this bar does not show that due coverage is worse than random; it shows the term has almost nothing to act on while so little is mastered.
- Five-term against two-term is decided on either reading: five-term loses or ties on the mean at both horizons and both curves, so no change to the bar's form would turn it on today.
- The decay bar is decided on either reading for the same reason.

What the operator could rule on, without which nothing here changes: whether 10's "on at least 90 percent of simulated students" should become a paired mean difference whose 95 percent interval lies wholly above 0 (or, for the two-term floor, wholly above a stated tolerance below 0), with the per-student share kept and reported. The model does not change the bar. On today's numbers that ruling would change no live setting: five-term and `lambda` fail on the mean too, and two-term stays live under either reading because it is already live.

What would settle more than a ruling: a world where the gain from a retrieval grows with the lag since the last one, so that spacing can matter, and the first weeks of the student's real attempts, where 10's delayed accuracy at a checkpoint measures what no simulator here can.

## The ruling [inferred, the model's judgement on the operator's delegation]

On 2026-09-27 the operator delegated the ruling above to the model. Decided: the bars in 10 are read from the paired mean difference and its 95 percent interval, with the per-student share kept and reported. A challenger turns on only when the interval lies wholly above 0 under both curves, and the two-term floor fails only when two-term's interval against the random control lies wholly below 0. Reasons: the share cannot be met by policies that differ, even by oracles; the mean interval shrinks with more students where the share does not; and the asymmetry keeps the burden on whatever would change the live policy. Under this reading the two-term floor passes (every interval spans 0), and five-term, `lambda` and removing interleaving stay off, as `docs/operator/p7-evals.md` records. The ruling is written into 10's acceptance thresholds.
