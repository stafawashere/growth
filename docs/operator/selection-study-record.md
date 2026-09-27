---
title: Selection study record
research_date: 2026-09-26
status: recorded
purpose: The numbers behind docs/operator/selection-study.md, written by tools/selection_study.py; simulation only.
---

# Selection study record

Written by `tools/selection_study.py` in 76 minutes, seed base 20270510, 200 synthetic students per arm, every arm on the same students. Every number is a simulation's measurement on synthetic students whose world model is invented; none is a person's and none is the student's. Intervals are 95 percent: Wilson for shares, normal approximation for means. `two_term_reseeded` is two-term with only the engine's draws reseeded, the noise floor. Worlds: `legacy` is the stage 8 world, `legacy_keyed` adds keyed draws only, `fixed` adds keyed draws, consolidated prior knowledge and daily half-life growth (`app/sim/learning.py` WorldRules).

Mastery per item is the stage 8 measure, read the day after the run. Delayed mastery per item reads the same skills 30 days after the run. Retention day 30 averages over every known skill.

## How often due coverage fires

- Fixed world, exponential, 60 days, the first 20 students under two-term: due coverage was above 0 for some candidate on 145 of 13166 block 2 choices (1.1 percent); on every other choice two-term drew uniformly, as the control does.
- Fixed world, exponential, 226 days, the first 20 students under two-term: due coverage was above 0 for some candidate on 4082 of 54666 block 2 choices (7.5 percent); on every other choice two-term drew uniformly, as the control does.

## World legacy, exponential forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 606 | 74.7 | 5.0 | 0.01021 [0.00976, 0.01065] | 0.00096 [0.00079, 0.00112] | 0.4892 |
| random_control | 200 | 606 | 75.2 | 4.9 | 0.01048 [0.01000, 0.01095] | 0.00104 [0.00087, 0.00121] | 0.4879 |
| oracle_forgetting | 200 | 608 | 36.8 | 12.1 | 0.00726 [0.00673, 0.00780] | 0.00412 [0.00367, 0.00457] | 0.6885 |
| oracle_teaching | 200 | 603 | 106.5 | 4.5 | 0.01185 [0.01139, 0.01231] | 0.00046 [0.00038, 0.00054] | 0.4560 |
| most_recent | 200 | 606 | 53.0 | 6.8 | 0.00902 [0.00840, 0.00964] | 0.00458 [0.00405, 0.00510] | 0.5812 |
| two_term_reseeded | 200 | 608 | 74.8 | 5.1 | 0.01093 [0.01043, 0.01143] | 0.00100 [0.00085, 0.00116] | 0.4894 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term | random_control | mastery per item | 35 / 111 / 54 | 73.0 [66.5, 78.7] | 17.5 [12.9, 23.4] | -0.00027 [-0.00061, 0.00007] | 106 of 200 |
| two_term | random_control | delayed mastery per item | 36 / 111 / 53 | 73.5 [67.0, 79.1] | 18.0 [13.3, 23.9] | -0.00008 [-0.00016, -0.00001] | 106 of 200 |
| two_term_reseeded | two_term | mastery per item | 113 / 0 / 87 | 56.5 [49.6, 63.2] | 56.5 [49.6, 63.2] | +0.00072 [0.00018, 0.00127] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 99 / 0 / 101 | 49.5 [42.6, 56.4] | 49.5 [42.6, 56.4] | +0.00004 [-0.00016, 0.00025] | 0 of 200 |
| two_term_reseeded | random_control | mastery per item | 107 / 0 / 93 | 53.5 [46.6, 60.3] | 53.5 [46.6, 60.3] | +0.00045 [-0.00012, 0.00103] | 0 of 200 |
| two_term_reseeded | random_control | delayed mastery per item | 97 / 0 / 103 | 48.5 [41.7, 55.4] | 48.5 [41.7, 55.4] | -0.00004 [-0.00025, 0.00017] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 53 / 0 / 147 | 26.5 [20.9, 33.0] | 26.5 [20.9, 33.0] | -0.00321 [-0.00390, -0.00253] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 158 / 0 / 42 | 79.0 [72.8, 84.1] | 79.0 [72.8, 84.1] | +0.00308 [0.00260, 0.00355] | 0 of 200 |
| oracle_teaching | random_control | mastery per item | 131 / 0 / 69 | 65.5 [58.7, 71.7] | 65.5 [58.7, 71.7] | +0.00138 [0.00078, 0.00197] | 0 of 200 |
| oracle_teaching | random_control | delayed mastery per item | 67 / 0 / 133 | 33.5 [27.3, 40.3] | 33.5 [27.3, 40.3] | -0.00058 [-0.00075, -0.00042] | 0 of 200 |
| most_recent | random_control | mastery per item | 73 / 0 / 127 | 36.5 [30.1, 43.4] | 36.5 [30.1, 43.4] | -0.00146 [-0.00218, -0.00073] | 0 of 200 |
| most_recent | random_control | delayed mastery per item | 169 / 0 / 31 | 84.5 [78.8, 88.9] | 84.5 [78.8, 88.9] | +0.00353 [0.00300, 0.00406] | 0 of 200 |

## World legacy, power law forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 604 | 75.3 | 4.1 | 0.02342 [0.02268, 0.02416] | 0.01090 [0.01057, 0.01123] | 0.5208 |
| random_control | 200 | 604 | 75.1 | 4.1 | 0.02335 [0.02264, 0.02406] | 0.01086 [0.01053, 0.01118] | 0.5219 |
| oracle_forgetting | 200 | 602 | 36.9 | 9.8 | 0.01382 [0.01319, 0.01445] | 0.00866 [0.00818, 0.00915] | 0.6971 |
| oracle_teaching | 200 | 603 | 106.2 | 4.0 | 0.02930 [0.02852, 0.03008] | 0.01365 [0.01333, 0.01397] | 0.4928 |
| most_recent | 200 | 604 | 52.5 | 5.6 | 0.01823 [0.01762, 0.01884] | 0.01110 [0.01061, 0.01159] | 0.6089 |
| two_term_reseeded | 200 | 606 | 74.5 | 4.3 | 0.02325 [0.02253, 0.02397] | 0.01084 [0.01050, 0.01117] | 0.5219 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term | random_control | mastery per item | 36 / 120 / 44 | 78.0 [71.8, 83.2] | 18.0 [13.3, 23.9] | +0.00007 [-0.00027, 0.00042] | 116 of 200 |
| two_term | random_control | delayed mastery per item | 41 / 120 / 39 | 80.5 [74.5, 85.4] | 20.5 [15.5, 26.6] | +0.00005 [-0.00007, 0.00016] | 116 of 200 |
| two_term_reseeded | two_term | mastery per item | 97 / 0 / 103 | 48.5 [41.7, 55.4] | 48.5 [41.7, 55.4] | -0.00017 [-0.00083, 0.00049] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 96 / 0 / 104 | 48.0 [41.2, 54.9] | 48.0 [41.2, 54.9] | -0.00006 [-0.00035, 0.00022] | 0 of 200 |
| two_term_reseeded | random_control | mastery per item | 93 / 0 / 107 | 46.5 [39.7, 53.4] | 46.5 [39.7, 53.4] | -0.00010 [-0.00073, 0.00053] | 0 of 200 |
| two_term_reseeded | random_control | delayed mastery per item | 93 / 0 / 107 | 46.5 [39.7, 53.4] | 46.5 [39.7, 53.4] | -0.00002 [-0.00030, 0.00026] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 10 / 0 / 190 | 5.0 [2.7, 9.0] | 5.0 [2.7, 9.0] | -0.00953 [-0.01031, -0.00875] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 53 / 0 / 147 | 26.5 [20.9, 33.0] | 26.5 [20.9, 33.0] | -0.00219 [-0.00270, -0.00169] | 0 of 200 |
| oracle_teaching | random_control | mastery per item | 182 / 0 / 18 | 91.0 [86.2, 94.2] | 91.0 [86.2, 94.2] | +0.00595 [0.00528, 0.00662] | 0 of 200 |
| oracle_teaching | random_control | delayed mastery per item | 182 / 0 / 18 | 91.0 [86.2, 94.2] | 91.0 [86.2, 94.2] | +0.00280 [0.00252, 0.00307] | 0 of 200 |
| most_recent | random_control | mastery per item | 35 / 0 / 165 | 17.5 [12.9, 23.4] | 17.5 [12.9, 23.4] | -0.00512 [-0.00594, -0.00430] | 0 of 200 |
| most_recent | random_control | delayed mastery per item | 104 / 0 / 96 | 52.0 [45.1, 58.8] | 52.0 [45.1, 58.8] | +0.00025 [-0.00027, 0.00076] | 0 of 200 |

## World legacy_keyed, exponential forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 607 | 74.8 | 5.1 | 0.01042 [0.00997, 0.01087] | 0.00089 [0.00076, 0.00102] | 0.4918 |
| two_term_reseeded | 200 | 606 | 74.9 | 5.0 | 0.01103 [0.01051, 0.01155] | 0.00106 [0.00090, 0.00123] | 0.4882 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term_reseeded | two_term | mastery per item | 115 / 0 / 85 | 57.5 [50.6, 64.1] | 57.5 [50.6, 64.1] | +0.00061 [-0.00002, 0.00125] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 114 / 0 / 86 | 57.0 [50.1, 63.7] | 57.0 [50.1, 63.7] | +0.00018 [-0.00001, 0.00036] | 0 of 200 |

## World legacy_keyed, power law forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 604 | 75.4 | 4.2 | 0.02372 [0.02307, 0.02437] | 0.01080 [0.01051, 0.01109] | 0.5218 |
| two_term_reseeded | 200 | 604 | 74.7 | 4.3 | 0.02350 [0.02280, 0.02421] | 0.01080 [0.01049, 0.01110] | 0.5221 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term_reseeded | two_term | mastery per item | 94 / 0 / 106 | 47.0 [40.2, 53.9] | 47.0 [40.2, 53.9] | -0.00022 [-0.00084, 0.00040] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 103 / 0 / 97 | 51.5 [44.6, 58.3] | 51.5 [44.6, 58.3] | -0.00000 [-0.00026, 0.00026] | 0 of 200 |

## World fixed, exponential forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 635 | 75.4 | 13.6 | 0.01211 [0.01157, 0.01265] | 0.00227 [0.00199, 0.00255] | 0.5399 |
| random_control | 200 | 636 | 75.8 | 13.7 | 0.01227 [0.01175, 0.01278] | 0.00225 [0.00199, 0.00251] | 0.5387 |
| oracle_forgetting | 200 | 629 | 44.3 | 12.6 | 0.01203 [0.01125, 0.01281] | 0.00731 [0.00671, 0.00791] | 0.6542 |
| oracle_teaching | 200 | 605 | 106.2 | 6.9 | 0.01204 [0.01153, 0.01256] | 0.00072 [0.00058, 0.00086] | 0.4605 |
| most_recent | 200 | 621 | 52.7 | 13.5 | 0.01161 [0.01096, 0.01227] | 0.00678 [0.00619, 0.00737] | 0.6197 |
| five_term | 200 | 627 | 62.3 | 22.6 | 0.01048 [0.00996, 0.01100] | 0.00299 [0.00266, 0.00333] | 0.5796 |
| decay_lambda_2 | 200 | 635 | 75.4 | 13.6 | 0.01211 [0.01157, 0.01265] | 0.00227 [0.00199, 0.00255] | 0.5398 |
| five_term_lambda_2 | 200 | 623 | 66.6 | 22.5 | 0.01063 [0.01015, 0.01110] | 0.00286 [0.00255, 0.00317] | 0.5667 |
| two_term_reseeded | 200 | 635 | 76.6 | 14.3 | 0.01275 [0.01222, 0.01329] | 0.00261 [0.00234, 0.00289] | 0.5381 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term | random_control | mastery per item | 64 / 74 / 62 | 69.0 [62.3, 75.0] | 32.0 [25.9, 38.8] | -0.00016 [-0.00057, 0.00025] | 73 of 200 |
| two_term | random_control | delayed mastery per item | 61 / 74 / 65 | 67.5 [60.7, 73.6] | 30.5 [24.5, 37.2] | +0.00002 [-0.00013, 0.00016] | 73 of 200 |
| two_term_reseeded | two_term | mastery per item | 103 / 0 / 97 | 51.5 [44.6, 58.3] | 51.5 [44.6, 58.3] | +0.00065 [-0.00003, 0.00133] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 123 / 0 / 77 | 61.5 [54.6, 68.0] | 61.5 [54.6, 68.0] | +0.00035 [0.00004, 0.00066] | 0 of 200 |
| two_term_reseeded | random_control | mastery per item | 99 / 0 / 101 | 49.5 [42.6, 56.4] | 49.5 [42.6, 56.4] | +0.00049 [-0.00019, 0.00116] | 0 of 200 |
| two_term_reseeded | random_control | delayed mastery per item | 114 / 0 / 86 | 57.0 [50.1, 63.7] | 57.0 [50.1, 63.7] | +0.00036 [0.00006, 0.00066] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 92 / 0 / 108 | 46.0 [39.2, 52.9] | 46.0 [39.2, 52.9] | -0.00024 [-0.00113, 0.00066] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 182 / 0 / 18 | 91.0 [86.2, 94.2] | 91.0 [86.2, 94.2] | +0.00506 [0.00449, 0.00563] | 0 of 200 |
| oracle_teaching | random_control | mastery per item | 99 / 0 / 101 | 49.5 [42.6, 56.4] | 49.5 [42.6, 56.4] | -0.00023 [-0.00085, 0.00040] | 0 of 200 |
| oracle_teaching | random_control | delayed mastery per item | 35 / 0 / 165 | 17.5 [12.9, 23.4] | 17.5 [12.9, 23.4] | -0.00153 [-0.00180, -0.00127] | 0 of 200 |
| most_recent | random_control | mastery per item | 88 / 0 / 112 | 44.0 [37.3, 50.9] | 44.0 [37.3, 50.9] | -0.00065 [-0.00146, 0.00016] | 0 of 200 |
| most_recent | random_control | delayed mastery per item | 177 / 0 / 23 | 88.5 [83.3, 92.2] | 88.5 [83.3, 92.2] | +0.00453 [0.00396, 0.00510] | 0 of 200 |
| five_term | two_term | mastery per item | 78 / 0 / 122 | 39.0 [32.5, 45.9] | 39.0 [32.5, 45.9] | -0.00163 [-0.00232, -0.00093] | 0 of 200 |
| five_term | two_term | delayed mastery per item | 115 / 0 / 85 | 57.5 [50.6, 64.1] | 57.5 [50.6, 64.1] | +0.00073 [0.00034, 0.00111] | 0 of 200 |
| decay_lambda_2 | two_term | mastery per item | 7 / 191 / 2 | 99.0 [96.4, 99.7] | 3.5 [1.7, 7.0] | +0.00000 [-0.00000, 0.00001] | 122 of 200 |
| decay_lambda_2 | two_term | retention day 30 | 0 / 191 / 9 | 95.5 [91.7, 97.6] | 0.0 [0.0, 1.9] | -0.00016 [-0.00031, -0.00000] | 122 of 200 |
| decay_lambda_2 | two_term | delayed mastery per item | 7 / 191 / 2 | 99.0 [96.4, 99.7] | 3.5 [1.7, 7.0] | +0.00000 [-0.00000, 0.00000] | 122 of 200 |
| five_term_lambda_2 | five_term | mastery per item | 99 / 0 / 101 | 49.5 [42.6, 56.4] | 49.5 [42.6, 56.4] | +0.00014 [-0.00045, 0.00074] | 0 of 200 |
| five_term_lambda_2 | five_term | retention day 30 | 64 / 0 / 136 | 32.0 [25.9, 38.8] | 32.0 [25.9, 38.8] | -0.01292 [-0.01681, -0.00903] | 0 of 200 |
| five_term_lambda_2 | five_term | delayed mastery per item | 90 / 0 / 110 | 45.0 [38.3, 51.9] | 45.0 [38.3, 51.9] | -0.00013 [-0.00049, 0.00023] | 0 of 200 |

## World fixed, power law forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 633 | 75.3 | 13.0 | 0.02434 [0.02367, 0.02501] | 0.01163 [0.01132, 0.01195] | 0.5486 |
| random_control | 200 | 634 | 75.9 | 13.0 | 0.02463 [0.02395, 0.02531] | 0.01176 [0.01145, 0.01208] | 0.5475 |
| oracle_forgetting | 200 | 627 | 44.2 | 12.3 | 0.01958 [0.01880, 0.02035] | 0.01274 [0.01214, 0.01333] | 0.6493 |
| oracle_teaching | 200 | 605 | 106.3 | 6.9 | 0.02956 [0.02880, 0.03032] | 0.01392 [0.01361, 0.01423] | 0.4749 |
| most_recent | 200 | 620 | 53.3 | 13.2 | 0.02097 [0.02026, 0.02167] | 0.01339 [0.01281, 0.01397] | 0.6159 |
| five_term | 200 | 626 | 61.6 | 22.7 | 0.02070 [0.02003, 0.02136] | 0.01110 [0.01069, 0.01151] | 0.5862 |
| decay_lambda_2 | 200 | 633 | 75.4 | 13.0 | 0.02435 [0.02369, 0.02502] | 0.01164 [0.01132, 0.01196] | 0.5484 |
| five_term_lambda_2 | 200 | 621 | 66.7 | 22.2 | 0.02183 [0.02109, 0.02257] | 0.01137 [0.01094, 0.01180] | 0.5719 |
| two_term_reseeded | 200 | 634 | 76.7 | 13.7 | 0.02505 [0.02432, 0.02578] | 0.01209 [0.01176, 0.01242] | 0.5466 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term | random_control | mastery per item | 59 / 78 / 63 | 68.5 [61.8, 74.5] | 29.5 [23.6, 36.2] | -0.00029 [-0.00071, 0.00013] | 77 of 200 |
| two_term | random_control | delayed mastery per item | 62 / 78 / 60 | 70.0 [63.3, 75.9] | 31.0 [25.0, 37.7] | -0.00013 [-0.00028, 0.00002] | 77 of 200 |
| two_term_reseeded | two_term | mastery per item | 112 / 0 / 88 | 56.0 [49.1, 62.7] | 56.0 [49.1, 62.7] | +0.00071 [0.00003, 0.00138] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 108 / 0 / 92 | 54.0 [47.1, 60.8] | 54.0 [47.1, 60.8] | +0.00046 [0.00014, 0.00077] | 0 of 200 |
| two_term_reseeded | random_control | mastery per item | 101 / 0 / 99 | 50.5 [43.6, 57.4] | 50.5 [43.6, 57.4] | +0.00042 [-0.00029, 0.00113] | 0 of 200 |
| two_term_reseeded | random_control | delayed mastery per item | 102 / 0 / 98 | 51.0 [44.1, 57.8] | 51.0 [44.1, 57.8] | +0.00033 [-0.00000, 0.00066] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 48 / 0 / 152 | 24.0 [18.6, 30.4] | 24.0 [18.6, 30.4] | -0.00505 [-0.00609, -0.00402] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 112 / 0 / 88 | 56.0 [49.1, 62.7] | 56.0 [49.1, 62.7] | +0.00097 [0.00033, 0.00162] | 0 of 200 |
| oracle_teaching | random_control | mastery per item | 169 / 0 / 31 | 84.5 [78.8, 88.9] | 84.5 [78.8, 88.9] | +0.00493 [0.00424, 0.00561] | 0 of 200 |
| oracle_teaching | random_control | delayed mastery per item | 167 / 0 / 33 | 83.5 [77.7, 88.0] | 83.5 [77.7, 88.0] | +0.00216 [0.00184, 0.00247] | 0 of 200 |
| most_recent | random_control | mastery per item | 61 / 0 / 139 | 30.5 [24.5, 37.2] | 30.5 [24.5, 37.2] | -0.00367 [-0.00457, -0.00277] | 0 of 200 |
| most_recent | random_control | delayed mastery per item | 114 / 0 / 86 | 57.0 [50.1, 63.7] | 57.0 [50.1, 63.7] | +0.00163 [0.00100, 0.00225] | 0 of 200 |
| five_term | two_term | mastery per item | 38 / 0 / 162 | 19.0 [14.2, 25.0] | 19.0 [14.2, 25.0] | -0.00365 [-0.00430, -0.00300] | 0 of 200 |
| five_term | two_term | delayed mastery per item | 77 / 0 / 123 | 38.5 [32.0, 45.4] | 38.5 [32.0, 45.4] | -0.00053 [-0.00093, -0.00013] | 0 of 200 |
| decay_lambda_2 | two_term | mastery per item | 7 / 190 / 3 | 98.5 [95.7, 99.5] | 3.5 [1.7, 7.0] | +0.00001 [-0.00000, 0.00003] | 125 of 200 |
| decay_lambda_2 | two_term | retention day 30 | 0 / 190 / 10 | 95.0 [91.0, 97.3] | 0.0 [0.0, 1.9] | -0.00014 [-0.00028, -0.00000] | 125 of 200 |
| decay_lambda_2 | two_term | delayed mastery per item | 7 / 190 / 3 | 98.5 [95.7, 99.5] | 3.5 [1.7, 7.0] | +0.00001 [0.00000, 0.00001] | 125 of 200 |
| five_term_lambda_2 | five_term | mastery per item | 117 / 0 / 83 | 58.5 [51.6, 65.1] | 58.5 [51.6, 65.1] | +0.00113 [0.00046, 0.00181] | 0 of 200 |
| five_term_lambda_2 | five_term | retention day 30 | 54 / 0 / 146 | 27.0 [21.3, 33.5] | 27.0 [21.3, 33.5] | -0.01425 [-0.01729, -0.01121] | 0 of 200 |
| five_term_lambda_2 | five_term | delayed mastery per item | 107 / 0 / 93 | 53.5 [46.6, 60.3] | 53.5 [46.6, 60.3] | +0.00027 [-0.00014, 0.00068] | 0 of 200 |

## World fixed, exponential forgetting, 226 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 2652 | 132.9 | 32.2 | 0.00147 [0.00134, 0.00159] | 0.00102 [0.00091, 0.00112] | 0.3516 |
| random_control | 200 | 2651 | 132.6 | 32.4 | 0.00145 [0.00134, 0.00157] | 0.00103 [0.00093, 0.00113] | 0.3523 |
| oracle_forgetting | 200 | 2526 | 56.4 | 25.1 | 0.00236 [0.00216, 0.00255] | 0.00216 [0.00198, 0.00234] | 0.4970 |
| oracle_teaching | 200 | 2482 | 145.8 | 25.2 | 0.00042 [0.00036, 0.00048] | 0.00031 [0.00025, 0.00036] | 0.3232 |
| most_recent | 200 | 2491 | 69.4 | 23.4 | 0.00235 [0.00216, 0.00254] | 0.00213 [0.00195, 0.00230] | 0.4579 |
| five_term | 200 | 2593 | 109.2 | 34.2 | 0.00156 [0.00145, 0.00167] | 0.00114 [0.00104, 0.00124] | 0.3873 |
| decay_lambda_2 | 200 | 2652 | 132.9 | 32.2 | 0.00147 [0.00134, 0.00159] | 0.00102 [0.00091, 0.00112] | 0.3516 |
| five_term_lambda_2 | 200 | 2574 | 114.9 | 34.6 | 0.00151 [0.00139, 0.00163] | 0.00108 [0.00097, 0.00118] | 0.3783 |
| two_term_reseeded | 200 | 2654 | 132.8 | 32.9 | 0.00150 [0.00139, 0.00161] | 0.00108 [0.00098, 0.00118] | 0.3529 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term | random_control | mastery per item | 96 / 4 / 100 | 50.0 [43.1, 56.9] | 48.0 [41.2, 54.9] | +0.00001 [-0.00009, 0.00011] | 3 of 200 |
| two_term | random_control | delayed mastery per item | 98 / 4 / 98 | 51.0 [44.1, 57.8] | 49.0 [42.2, 55.9] | -0.00001 [-0.00008, 0.00006] | 3 of 200 |
| two_term_reseeded | two_term | mastery per item | 108 / 0 / 92 | 54.0 [47.1, 60.8] | 54.0 [47.1, 60.8] | +0.00004 [-0.00009, 0.00017] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 108 / 0 / 92 | 54.0 [47.1, 60.8] | 54.0 [47.1, 60.8] | +0.00006 [-0.00005, 0.00017] | 0 of 200 |
| two_term_reseeded | random_control | mastery per item | 100 / 0 / 100 | 50.0 [43.1, 56.9] | 50.0 [43.1, 56.9] | +0.00005 [-0.00008, 0.00018] | 0 of 200 |
| two_term_reseeded | random_control | delayed mastery per item | 106 / 0 / 94 | 53.0 [46.1, 59.8] | 53.0 [46.1, 59.8] | +0.00005 [-0.00005, 0.00016] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 146 / 0 / 54 | 73.0 [66.5, 78.7] | 73.0 [66.5, 78.7] | +0.00090 [0.00071, 0.00109] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 166 / 0 / 34 | 83.0 [77.2, 87.6] | 83.0 [77.2, 87.6] | +0.00113 [0.00096, 0.00130] | 0 of 200 |
| oracle_teaching | random_control | mastery per item | 12 / 0 / 188 | 6.0 [3.5, 10.2] | 6.0 [3.5, 10.2] | -0.00103 [-0.00115, -0.00092] | 0 of 200 |
| oracle_teaching | random_control | delayed mastery per item | 21 / 0 / 179 | 10.5 [7.0, 15.5] | 10.5 [7.0, 15.5] | -0.00072 [-0.00082, -0.00062] | 0 of 200 |
| most_recent | random_control | mastery per item | 146 / 0 / 54 | 73.0 [66.5, 78.7] | 73.0 [66.5, 78.7] | +0.00090 [0.00069, 0.00110] | 0 of 200 |
| most_recent | random_control | delayed mastery per item | 167 / 0 / 33 | 83.5 [77.7, 88.0] | 83.5 [77.7, 88.0] | +0.00110 [0.00092, 0.00128] | 0 of 200 |
| five_term | two_term | mastery per item | 111 / 0 / 89 | 55.5 [48.6, 62.2] | 55.5 [48.6, 62.2] | +0.00009 [-0.00005, 0.00023] | 0 of 200 |
| five_term | two_term | delayed mastery per item | 114 / 0 / 86 | 57.0 [50.1, 63.7] | 57.0 [50.1, 63.7] | +0.00012 [-0.00000, 0.00024] | 0 of 200 |
| decay_lambda_2 | two_term | mastery per item | 0 / 191 / 9 | 95.5 [91.7, 97.6] | 0.0 [0.0, 1.9] | -0.00000 [-0.00000, 0.00000] | 118 of 200 |
| decay_lambda_2 | two_term | retention day 30 | 0 / 191 / 9 | 95.5 [91.7, 97.6] | 0.0 [0.0, 1.9] | -0.00000 [-0.00000, 0.00000] | 118 of 200 |
| decay_lambda_2 | two_term | delayed mastery per item | 0 / 191 / 9 | 95.5 [91.7, 97.6] | 0.0 [0.0, 1.9] | -0.00000 [-0.00000, 0.00000] | 118 of 200 |
| five_term_lambda_2 | five_term | mastery per item | 98 / 0 / 102 | 49.0 [42.2, 55.9] | 49.0 [42.2, 55.9] | -0.00005 [-0.00018, 0.00008] | 0 of 200 |
| five_term_lambda_2 | five_term | retention day 30 | 63 / 0 / 137 | 31.5 [25.5, 38.2] | 31.5 [25.5, 38.2] | -0.00902 [-0.01148, -0.00656] | 0 of 200 |
| five_term_lambda_2 | five_term | delayed mastery per item | 96 / 0 / 104 | 48.0 [41.2, 54.9] | 48.0 [41.2, 54.9] | -0.00006 [-0.00018, 0.00005] | 0 of 200 |

## World fixed, power law forgetting, 226 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 2663 | 132.7 | 35.1 | 0.00426 [0.00412, 0.00440] | 0.00336 [0.00324, 0.00348] | 0.3685 |
| random_control | 200 | 2666 | 133.5 | 35.4 | 0.00422 [0.00409, 0.00435] | 0.00334 [0.00323, 0.00346] | 0.3673 |
| oracle_forgetting | 200 | 2539 | 57.3 | 26.9 | 0.00374 [0.00354, 0.00395] | 0.00332 [0.00314, 0.00351] | 0.4989 |
| oracle_teaching | 200 | 2488 | 146.0 | 28.0 | 0.00317 [0.00306, 0.00327] | 0.00261 [0.00252, 0.00270] | 0.3367 |
| most_recent | 200 | 2499 | 70.5 | 25.4 | 0.00399 [0.00376, 0.00423] | 0.00351 [0.00330, 0.00371] | 0.4581 |
| five_term | 200 | 2605 | 109.1 | 38.4 | 0.00392 [0.00376, 0.00408] | 0.00310 [0.00296, 0.00324] | 0.3996 |
| decay_lambda_2 | 200 | 2663 | 132.7 | 35.1 | 0.00426 [0.00412, 0.00440] | 0.00336 [0.00324, 0.00348] | 0.3684 |
| five_term_lambda_2 | 200 | 2579 | 114.9 | 37.2 | 0.00369 [0.00354, 0.00384] | 0.00291 [0.00278, 0.00303] | 0.3876 |
| two_term_reseeded | 200 | 2668 | 133.7 | 35.5 | 0.00429 [0.00414, 0.00445] | 0.00340 [0.00327, 0.00352] | 0.3679 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term | random_control | mastery per item | 108 / 2 / 90 | 55.0 [48.1, 61.7] | 54.0 [47.1, 60.8] | +0.00004 [-0.00007, 0.00015] | 2 of 200 |
| two_term | random_control | delayed mastery per item | 99 / 2 / 99 | 50.5 [43.6, 57.4] | 49.5 [42.6, 56.4] | +0.00001 [-0.00007, 0.00010] | 2 of 200 |
| two_term_reseeded | two_term | mastery per item | 102 / 0 / 98 | 51.0 [44.1, 57.8] | 51.0 [44.1, 57.8] | +0.00004 [-0.00012, 0.00019] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 104 / 0 / 96 | 52.0 [45.1, 58.8] | 52.0 [45.1, 58.8] | +0.00004 [-0.00009, 0.00017] | 0 of 200 |
| two_term_reseeded | random_control | mastery per item | 102 / 0 / 98 | 51.0 [44.1, 57.8] | 51.0 [44.1, 57.8] | +0.00007 [-0.00009, 0.00024] | 0 of 200 |
| two_term_reseeded | random_control | delayed mastery per item | 102 / 0 / 98 | 51.0 [44.1, 57.8] | 51.0 [44.1, 57.8] | +0.00005 [-0.00008, 0.00019] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 79 / 0 / 121 | 39.5 [33.0, 46.4] | 39.5 [33.0, 46.4] | -0.00048 [-0.00068, -0.00027] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 96 / 0 / 104 | 48.0 [41.2, 54.9] | 48.0 [41.2, 54.9] | -0.00002 [-0.00020, 0.00015] | 0 of 200 |
| oracle_teaching | random_control | mastery per item | 24 / 0 / 176 | 12.0 [8.2, 17.2] | 12.0 [8.2, 17.2] | -0.00105 [-0.00118, -0.00092] | 0 of 200 |
| oracle_teaching | random_control | delayed mastery per item | 32 / 0 / 168 | 16.0 [11.6, 21.7] | 16.0 [11.6, 21.7] | -0.00074 [-0.00085, -0.00062] | 0 of 200 |
| most_recent | random_control | mastery per item | 84 / 0 / 116 | 42.0 [35.4, 48.9] | 42.0 [35.4, 48.9] | -0.00023 [-0.00047, 0.00002] | 0 of 200 |
| most_recent | random_control | delayed mastery per item | 94 / 0 / 106 | 47.0 [40.2, 53.9] | 47.0 [40.2, 53.9] | +0.00016 [-0.00005, 0.00037] | 0 of 200 |
| five_term | two_term | mastery per item | 78 / 0 / 122 | 39.0 [32.5, 45.9] | 39.0 [32.5, 45.9] | -0.00034 [-0.00051, -0.00016] | 0 of 200 |
| five_term | two_term | delayed mastery per item | 82 / 0 / 118 | 41.0 [34.4, 47.9] | 41.0 [34.4, 47.9] | -0.00026 [-0.00041, -0.00011] | 0 of 200 |
| decay_lambda_2 | two_term | mastery per item | 0 / 190 / 10 | 95.0 [91.0, 97.3] | 0.0 [0.0, 1.9] | -0.00000 [-0.00000, 0.00000] | 120 of 200 |
| decay_lambda_2 | two_term | retention day 30 | 0 / 190 / 10 | 95.0 [91.0, 97.3] | 0.0 [0.0, 1.9] | -0.00001 [-0.00002, 0.00000] | 120 of 200 |
| decay_lambda_2 | two_term | delayed mastery per item | 0 / 190 / 10 | 95.0 [91.0, 97.3] | 0.0 [0.0, 1.9] | -0.00000 [-0.00000, -0.00000] | 120 of 200 |
| five_term_lambda_2 | five_term | mastery per item | 85 / 0 / 115 | 42.5 [35.9, 49.4] | 42.5 [35.9, 49.4] | -0.00023 [-0.00039, -0.00008] | 0 of 200 |
| five_term_lambda_2 | five_term | retention day 30 | 50 / 0 / 150 | 25.0 [19.5, 31.4] | 25.0 [19.5, 31.4] | -0.01200 [-0.01462, -0.00939] | 0 of 200 |
| five_term_lambda_2 | five_term | delayed mastery per item | 84 / 0 / 116 | 42.0 [35.4, 48.9] | 42.0 [35.4, 48.9] | -0.00019 [-0.00032, -0.00006] | 0 of 200 |
