---
title: P2 evaluation record
research_date: 2026-09-26
status: recorded
purpose: The measured results of eval_diagnostic_information, eval_selection_bias_control and eval_two_term_against_five_term at the recorded size, for the P7 gate on the five-term score.
---

# P2 evaluation record

Written by `tools/p2_evals.py` from `app/sim/p2_evals.py`, seed base 20260924. Every
number is a simulation over synthetic students on the whole 541-skill graph with a synthetic bank
of 3 verified items per active archetype (`app/sim/whole_graph.py`). None is a human's measurement
and none is a real student's. The simulated world does not learn: a student's hidden knowledge is
fixed for the run and forgetting follows the P1 runner's half-life curve, so "truly mastered"
counts how many skills the engine declared mastered that the student really knew, which measures
how fast each policy finds what is known rather than how fast it teaches.

## Diagnostic information

400 synthetic students, each one diagnostic from a fresh account.

- Mean posterior movement per item (total variation summed over units): 0.3708 over items 1 to 10, 0.2123 after item 10. Measures after item 10 move less than before it, the ALEKS-observed shape 11 asks for.
- Runs stopping early on the entropy rule: 306 of 400 (76.5%). Longest run 30 items, median 25.0.
- Of the 306 early stops, 290 came in a 3-item window where one answer raised the summed unit entropy. The plan's rule reads a rise as entropy that stopped falling, so most early stops follow an answer the posterior did not expect rather than a posterior that settled. The error direction is conservative (the unit is left unresolved and its skills are fast-tracked), and the rule is a named tunable in 02 for the held-out agreement to settle.
- Held-out extra problem: 400 asked, mean predicted raw probability 0.3761, observed success rate 0.0825. The model over-predicts on this population by 0.2936.
- Placement: 950 skills marked mastered from the unit posterior, 896 truly known, 54 not known (5.7%). A wrongly placed skill is un-mastered only by a credited failure, and on the P7 simulation most were not served again within 60 days (BUILD-LEDGER.md, 2026-09-26, false mastery).

## Selection bias control

25 students, a diagnostic each, then 40 daily sessions per arm, same students and seeds in both arms. The control arm holds retrievability at 1.0, which empties the due set, so every choice is the uniform draw inside the gated fringe (10, arm 2). Bias is mean predicted p_A_knowledge minus observed success over served items.

| Arm | Sessions | Items | Declared mastered | Truly mastered | True mastered per item | Mean predicted p_A | Observed success | Bias |
|---|---|---|---|---|---|---|---|---|
| policy | 1000 | 9983 | 103 | 103 | 0.0103 | 0.4779 | 0.1083 | +0.3696 |
| control | 1000 | 9982 | 103 | 103 | 0.0103 | 0.4782 | 0.1084 | +0.3698 |

## Two-term against five-term

Same students, seeds and days. The five-term arm replaces block 2's ordering with the deferred score of 02 (`app/sim/five_term.py`); blocks 1 and 3 and every hard constraint are unchanged. The live policy stays two-term: nothing in `app/engine` or `app/session` imports the five-term module (R4).

| Arm | Sessions | Items | Declared mastered | Truly mastered | True mastered per item | Mean predicted p_A | Observed success | Bias |
|---|---|---|---|---|---|---|---|---|
| two_term | 1000 | 9983 | 103 | 103 | 0.0103 | 0.4779 | 0.1083 | +0.3696 |
| five_term | 1000 | 9915 | 192 | 192 | 0.0194 | 0.5730 | 0.1865 | +0.3865 |

On this world the five-term score finds more truly mastered skills per item than the two-term score. This is evidence for the P7 gate, which turns the five-term score on only when a simulation shows it beating the two-term score on true mastery per item. It is recorded here and changes nothing in P2.
