---
title: Selection study record
research_date: 2026-09-29
status: recorded
purpose: The numbers behind docs/operator/selection-study.md, written by tools/selection_study.py; simulation only.
---

# Selection study record

Re-run on 2026-09-29 during the Today redesign on the engine as it stood at commit 635c03b (the 2026-09-29 mastery corrections and the relearn-on-feedback world rule included), on the recorded seeds; it supersedes the 2026-09-26 record, whose numbers no longer reproduce. The reading is in `selection-study.md`, "Re-run of 2026-09-29".

Written by `tools/selection_study.py` in 124 minutes, seed base 20270510, 200 synthetic students per arm, every arm on the same students. Every number is a simulation's measurement on synthetic students whose world model is invented; none is a person's and none is the student's. Intervals are 95 percent: Wilson for shares, normal approximation for means. `two_term_reseeded` is two-term with only the engine's draws reseeded, the noise floor. Worlds: `legacy` is the stage 8 world, `legacy_keyed` adds keyed draws only, `fixed` adds keyed draws, consolidated prior knowledge and daily half-life growth (`app/sim/learning.py` WorldRules).

Mastery per item is the stage 8 measure, read the day after the run. Delayed mastery per item reads the same skills 30 days after the run. Retention day 30 averages over every known skill.

## How often due coverage fires

- Fixed world, exponential, 60 days, the first 20 students under two-term: due coverage was above 0 for some candidate on 6085 of 15209 block 2 choices (40.0 percent); on every other choice two-term drew uniformly, as the control does.
- Fixed world, exponential, 226 days, the first 20 students under two-term: due coverage was above 0 for some candidate on 26750 of 58369 block 2 choices (45.8 percent); on every other choice two-term drew uniformly, as the control does.

## World legacy, exponential forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 753 | 32.1 | 38.1 | 0.02062 [0.01943, 0.02181] | 0.01625 [0.01525, 0.01726] | 0.8622 |
| random_control | 200 | 756 | 34.4 | 39.9 | 0.02143 [0.02030, 0.02256] | 0.01663 [0.01568, 0.01758] | 0.8506 |
| oracle_forgetting | 200 | 752 | 24.0 | 41.8 | 0.02136 [0.02018, 0.02254] | 0.01840 [0.01734, 0.01946] | 0.9273 |
| oracle_teaching | 200 | 743 | 32.3 | 33.6 | 0.01964 [0.01851, 0.02077] | 0.01553 [0.01463, 0.01644] | 0.8446 |
| most_recent | 200 | 749 | 25.1 | 38.8 | 0.02296 [0.02168, 0.02423] | 0.01998 [0.01887, 0.02109] | 0.9068 |
| two_term_reseeded | 200 | 752 | 31.4 | 37.7 | 0.02038 [0.01908, 0.02167] | 0.01615 [0.01508, 0.01723] | 0.8640 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term | random_control | mastery per item | 84 / 0 / 116 | 42.0 [35.4, 48.9] | 42.0 [35.4, 48.9] | -0.00081 [-0.00188, 0.00026] | 0 of 200 |
| two_term | random_control | delayed mastery per item | 87 / 0 / 113 | 43.5 [36.8, 50.4] | 43.5 [36.8, 50.4] | -0.00038 [-0.00127, 0.00051] | 0 of 200 |
| two_term_reseeded | two_term | mastery per item | 102 / 0 / 98 | 51.0 [44.1, 57.8] | 51.0 [44.1, 57.8] | -0.00024 [-0.00146, 0.00098] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 101 / 0 / 99 | 50.5 [43.6, 57.4] | 50.5 [43.6, 57.4] | -0.00010 [-0.00109, 0.00089] | 0 of 200 |
| two_term_reseeded | random_control | mastery per item | 81 / 0 / 119 | 40.5 [33.9, 47.4] | 40.5 [33.9, 47.4] | -0.00105 [-0.00232, 0.00022] | 0 of 200 |
| two_term_reseeded | random_control | delayed mastery per item | 89 / 0 / 111 | 44.5 [37.8, 51.4] | 44.5 [37.8, 51.4] | -0.00048 [-0.00151, 0.00054] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 97 / 0 / 103 | 48.5 [41.7, 55.4] | 48.5 [41.7, 55.4] | -0.00006 [-0.00134, 0.00121] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 112 / 0 / 88 | 56.0 [49.1, 62.7] | 56.0 [49.1, 62.7] | +0.00177 [0.00068, 0.00285] | 0 of 200 |
| oracle_teaching | random_control | mastery per item | 90 / 0 / 110 | 45.0 [38.3, 51.9] | 45.0 [38.3, 51.9] | -0.00179 [-0.00312, -0.00045] | 0 of 200 |
| oracle_teaching | random_control | delayed mastery per item | 93 / 0 / 107 | 46.5 [39.7, 53.4] | 46.5 [39.7, 53.4] | -0.00110 [-0.00216, -0.00004] | 0 of 200 |
| most_recent | random_control | mastery per item | 109 / 0 / 91 | 54.5 [47.6, 61.3] | 54.5 [47.6, 61.3] | +0.00153 [0.00023, 0.00283] | 0 of 200 |
| most_recent | random_control | delayed mastery per item | 133 / 0 / 67 | 66.5 [59.7, 72.7] | 66.5 [59.7, 72.7] | +0.00335 [0.00225, 0.00445] | 0 of 200 |

## World legacy, power law forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 751 | 31.8 | 37.4 | 0.02418 [0.02279, 0.02556] | 0.01917 [0.01801, 0.02033] | 0.8704 |
| random_control | 200 | 754 | 34.3 | 39.1 | 0.02527 [0.02402, 0.02651] | 0.01969 [0.01866, 0.02073] | 0.8571 |
| oracle_forgetting | 200 | 751 | 23.5 | 41.1 | 0.02289 [0.02167, 0.02410] | 0.01958 [0.01848, 0.02068] | 0.9315 |
| oracle_teaching | 200 | 741 | 33.0 | 33.4 | 0.02325 [0.02207, 0.02442] | 0.01776 [0.01685, 0.01867] | 0.8477 |
| most_recent | 200 | 749 | 25.4 | 38.3 | 0.02429 [0.02306, 0.02552] | 0.02073 [0.01963, 0.02184] | 0.9067 |
| two_term_reseeded | 200 | 752 | 31.0 | 37.0 | 0.02351 [0.02218, 0.02484] | 0.01856 [0.01745, 0.01966] | 0.8706 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term | random_control | mastery per item | 78 / 0 / 122 | 39.0 [32.5, 45.9] | 39.0 [32.5, 45.9] | -0.00109 [-0.00211, -0.00007] | 0 of 200 |
| two_term | random_control | delayed mastery per item | 80 / 0 / 120 | 40.0 [33.5, 46.9] | 40.0 [33.5, 46.9] | -0.00052 [-0.00138, 0.00034] | 0 of 200 |
| two_term_reseeded | two_term | mastery per item | 94 / 0 / 106 | 47.0 [40.2, 53.9] | 47.0 [40.2, 53.9] | -0.00067 [-0.00191, 0.00058] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 94 / 0 / 106 | 47.0 [40.2, 53.9] | 47.0 [40.2, 53.9] | -0.00061 [-0.00165, 0.00043] | 0 of 200 |
| two_term_reseeded | random_control | mastery per item | 88 / 0 / 112 | 44.0 [37.3, 50.9] | 44.0 [37.3, 50.9] | -0.00176 [-0.00296, -0.00055] | 0 of 200 |
| two_term_reseeded | random_control | delayed mastery per item | 88 / 0 / 112 | 44.0 [37.3, 50.9] | 44.0 [37.3, 50.9] | -0.00114 [-0.00214, -0.00013] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 72 / 0 / 128 | 36.0 [29.7, 42.9] | 36.0 [29.7, 42.9] | -0.00238 [-0.00346, -0.00130] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 89 / 0 / 111 | 44.5 [37.8, 51.4] | 44.5 [37.8, 51.4] | -0.00011 [-0.00105, 0.00082] | 0 of 200 |
| oracle_teaching | random_control | mastery per item | 95 / 0 / 105 | 47.5 [40.7, 54.4] | 47.5 [40.7, 54.4] | -0.00202 [-0.00331, -0.00073] | 0 of 200 |
| oracle_teaching | random_control | delayed mastery per item | 89 / 0 / 111 | 44.5 [37.8, 51.4] | 44.5 [37.8, 51.4] | -0.00193 [-0.00294, -0.00092] | 0 of 200 |
| most_recent | random_control | mastery per item | 95 / 0 / 105 | 47.5 [40.7, 54.4] | 47.5 [40.7, 54.4] | -0.00098 [-0.00201, 0.00005] | 0 of 200 |
| most_recent | random_control | delayed mastery per item | 116 / 0 / 84 | 58.0 [51.1, 64.6] | 58.0 [51.1, 64.6] | +0.00104 [0.00013, 0.00195] | 0 of 200 |

## World legacy_keyed, exponential forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 755 | 37.7 | 49.6 | 0.04391 [0.04189, 0.04594] | 0.03070 [0.02918, 0.03222] | 0.8918 |
| two_term_reseeded | 200 | 756 | 37.9 | 49.8 | 0.04407 [0.04201, 0.04613] | 0.03047 [0.02892, 0.03202] | 0.8884 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term_reseeded | two_term | mastery per item | 104 / 0 / 96 | 52.0 [45.1, 58.8] | 52.0 [45.1, 58.8] | +0.00015 [-0.00068, 0.00099] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 96 / 0 / 104 | 48.0 [41.2, 54.9] | 48.0 [41.2, 54.9] | -0.00023 [-0.00113, 0.00068] | 0 of 200 |

## World legacy_keyed, power law forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 754 | 37.4 | 46.4 | 0.04250 [0.04052, 0.04448] | 0.03016 [0.02868, 0.03164] | 0.8850 |
| two_term_reseeded | 200 | 755 | 36.7 | 47.4 | 0.04218 [0.04022, 0.04415] | 0.03065 [0.02915, 0.03214] | 0.8925 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term_reseeded | two_term | mastery per item | 97 / 0 / 103 | 48.5 [41.7, 55.4] | 48.5 [41.7, 55.4] | -0.00032 [-0.00109, 0.00046] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 107 / 0 / 93 | 53.5 [46.6, 60.3] | 53.5 [46.6, 60.3] | +0.00049 [-0.00024, 0.00121] | 0 of 200 |

## World fixed, exponential forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 756 | 38.9 | 52.3 | 0.04529 [0.04337, 0.04722] | 0.03053 [0.02911, 0.03195] | 0.8161 |
| random_control | 200 | 759 | 42.2 | 56.6 | 0.04831 [0.04632, 0.05030] | 0.03113 [0.02969, 0.03257] | 0.8093 |
| oracle_forgetting | 200 | 757 | 33.5 | 48.9 | 0.04152 [0.03999, 0.04306] | 0.03060 [0.02927, 0.03193] | 0.8386 |
| oracle_teaching | 200 | 750 | 43.2 | 49.5 | 0.04768 [0.04577, 0.04958] | 0.03026 [0.02890, 0.03163] | 0.8009 |
| most_recent | 200 | 754 | 29.7 | 49.4 | 0.03726 [0.03580, 0.03872] | 0.02953 [0.02825, 0.03082] | 0.8448 |
| five_term | 200 | 748 | 34.8 | 50.4 | 0.03876 [0.03708, 0.04045] | 0.02711 [0.02573, 0.02850] | 0.8170 |
| decay_lambda_2 | 200 | 756 | 38.9 | 52.4 | 0.04539 [0.04346, 0.04732] | 0.03061 [0.02919, 0.03202] | 0.8163 |
| five_term_lambda_2 | 200 | 747 | 33.5 | 49.5 | 0.03713 [0.03553, 0.03873] | 0.02564 [0.02433, 0.02696] | 0.8165 |
| two_term_reseeded | 200 | 757 | 38.2 | 52.4 | 0.04424 [0.04236, 0.04613] | 0.03036 [0.02896, 0.03176] | 0.8187 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term | random_control | mastery per item | 59 / 0 / 141 | 29.5 [23.6, 36.2] | 29.5 [23.6, 36.2] | -0.00301 [-0.00389, -0.00214] | 0 of 200 |
| two_term | random_control | delayed mastery per item | 83 / 0 / 117 | 41.5 [34.9, 48.4] | 41.5 [34.9, 48.4] | -0.00060 [-0.00149, 0.00030] | 0 of 200 |
| two_term_reseeded | two_term | mastery per item | 85 / 0 / 115 | 42.5 [35.9, 49.4] | 42.5 [35.9, 49.4] | -0.00105 [-0.00194, -0.00016] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 93 / 0 / 107 | 46.5 [39.7, 53.4] | 46.5 [39.7, 53.4] | -0.00017 [-0.00099, 0.00064] | 0 of 200 |
| two_term_reseeded | random_control | mastery per item | 52 / 0 / 148 | 26.0 [20.4, 32.5] | 26.0 [20.4, 32.5] | -0.00407 [-0.00504, -0.00309] | 0 of 200 |
| two_term_reseeded | random_control | delayed mastery per item | 91 / 0 / 109 | 45.5 [38.7, 52.4] | 45.5 [38.7, 52.4] | -0.00077 [-0.00174, 0.00021] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 52 / 0 / 148 | 26.0 [20.4, 32.5] | 26.0 [20.4, 32.5] | -0.00678 [-0.00808, -0.00548] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 98 / 0 / 102 | 49.0 [42.2, 55.9] | 49.0 [42.2, 55.9] | -0.00053 [-0.00154, 0.00048] | 0 of 200 |
| oracle_teaching | random_control | mastery per item | 86 / 0 / 114 | 43.0 [36.3, 49.9] | 43.0 [36.3, 49.9] | -0.00063 [-0.00174, 0.00048] | 0 of 200 |
| oracle_teaching | random_control | delayed mastery per item | 90 / 0 / 110 | 45.0 [38.3, 51.9] | 45.0 [38.3, 51.9] | -0.00087 [-0.00181, 0.00008] | 0 of 200 |
| most_recent | random_control | mastery per item | 14 / 0 / 186 | 7.0 [4.2, 11.4] | 7.0 [4.2, 11.4] | -0.01105 [-0.01216, -0.00993] | 0 of 200 |
| most_recent | random_control | delayed mastery per item | 84 / 0 / 116 | 42.0 [35.4, 48.9] | 42.0 [35.4, 48.9] | -0.00160 [-0.00259, -0.00060] | 0 of 200 |
| five_term | two_term | mastery per item | 33 / 0 / 167 | 16.5 [12.0, 22.3] | 16.5 [12.0, 22.3] | -0.00653 [-0.00741, -0.00565] | 0 of 200 |
| five_term | two_term | delayed mastery per item | 50 / 0 / 150 | 25.0 [19.5, 31.4] | 25.0 [19.5, 31.4] | -0.00342 [-0.00427, -0.00257] | 0 of 200 |
| decay_lambda_2 | two_term | mastery per item | 5 / 191 / 4 | 98.0 [95.0, 99.2] | 2.5 [1.1, 5.7] | +0.00010 [-0.00002, 0.00022] | 148 of 200 |
| decay_lambda_2 | two_term | retention day 30 | 7 / 191 / 2 | 99.0 [96.4, 99.7] | 3.5 [1.7, 7.0] | +0.00023 [0.00000, 0.00047] | 148 of 200 |
| decay_lambda_2 | two_term | delayed mastery per item | 7 / 191 / 2 | 99.0 [96.4, 99.7] | 3.5 [1.7, 7.0] | +0.00007 [0.00001, 0.00014] | 148 of 200 |
| five_term_lambda_2 | five_term | mastery per item | 65 / 0 / 135 | 32.5 [26.4, 39.3] | 32.5 [26.4, 39.3] | -0.00163 [-0.00240, -0.00086] | 0 of 200 |
| five_term_lambda_2 | five_term | retention day 30 | 103 / 0 / 97 | 51.5 [44.6, 58.3] | 51.5 [44.6, 58.3] | -0.00058 [-0.00339, 0.00223] | 0 of 200 |
| five_term_lambda_2 | five_term | delayed mastery per item | 70 / 0 / 130 | 35.0 [28.7, 41.8] | 35.0 [28.7, 41.8] | -0.00147 [-0.00221, -0.00072] | 0 of 200 |

## World fixed, power law forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 756 | 38.0 | 51.0 | 0.04342 [0.04164, 0.04520] | 0.03048 [0.02917, 0.03178] | 0.7884 |
| random_control | 200 | 758 | 41.4 | 55.0 | 0.04665 [0.04479, 0.04850] | 0.03156 [0.03025, 0.03287] | 0.7836 |
| oracle_forgetting | 200 | 757 | 32.9 | 47.6 | 0.04024 [0.03878, 0.04170] | 0.03031 [0.02908, 0.03154] | 0.8086 |
| oracle_teaching | 200 | 749 | 42.4 | 48.1 | 0.04673 [0.04489, 0.04858] | 0.03133 [0.03005, 0.03262] | 0.7766 |
| most_recent | 200 | 753 | 28.9 | 48.2 | 0.03598 [0.03462, 0.03735] | 0.02908 [0.02788, 0.03028] | 0.8135 |
| five_term | 200 | 747 | 34.1 | 49.3 | 0.03793 [0.03622, 0.03964] | 0.02748 [0.02614, 0.02882] | 0.7887 |
| decay_lambda_2 | 200 | 756 | 38.0 | 50.9 | 0.04339 [0.04160, 0.04518] | 0.03045 [0.02914, 0.03176] | 0.7883 |
| five_term_lambda_2 | 200 | 747 | 33.5 | 48.6 | 0.03681 [0.03521, 0.03841] | 0.02650 [0.02522, 0.02779] | 0.7872 |
| two_term_reseeded | 200 | 756 | 37.7 | 50.6 | 0.04286 [0.04103, 0.04470] | 0.03012 [0.02878, 0.03147] | 0.7880 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term | random_control | mastery per item | 55 / 0 / 145 | 27.5 [21.8, 34.1] | 27.5 [21.8, 34.1] | -0.00323 [-0.00401, -0.00245] | 0 of 200 |
| two_term | random_control | delayed mastery per item | 84 / 0 / 116 | 42.0 [35.4, 48.9] | 42.0 [35.4, 48.9] | -0.00109 [-0.00174, -0.00043] | 0 of 200 |
| two_term_reseeded | two_term | mastery per item | 94 / 0 / 106 | 47.0 [40.2, 53.9] | 47.0 [40.2, 53.9] | -0.00056 [-0.00138, 0.00026] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 98 / 0 / 102 | 49.0 [42.2, 55.9] | 49.0 [42.2, 55.9] | -0.00035 [-0.00110, 0.00040] | 0 of 200 |
| two_term_reseeded | random_control | mastery per item | 59 / 0 / 141 | 29.5 [23.6, 36.2] | 29.5 [23.6, 36.2] | -0.00378 [-0.00464, -0.00293] | 0 of 200 |
| two_term_reseeded | random_control | delayed mastery per item | 83 / 0 / 117 | 41.5 [34.9, 48.4] | 41.5 [34.9, 48.4] | -0.00144 [-0.00216, -0.00071] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 39 / 0 / 161 | 19.5 [14.6, 25.5] | 19.5 [14.6, 25.5] | -0.00641 [-0.00756, -0.00527] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 86 / 0 / 114 | 43.0 [36.3, 49.9] | 43.0 [36.3, 49.9] | -0.00125 [-0.00207, -0.00043] | 0 of 200 |
| oracle_teaching | random_control | mastery per item | 103 / 0 / 97 | 51.5 [44.6, 58.3] | 51.5 [44.6, 58.3] | +0.00009 [-0.00082, 0.00099] | 0 of 200 |
| oracle_teaching | random_control | delayed mastery per item | 104 / 0 / 96 | 52.0 [45.1, 58.8] | 52.0 [45.1, 58.8] | -0.00023 [-0.00094, 0.00048] | 0 of 200 |
| most_recent | random_control | mastery per item | 15 / 0 / 185 | 7.5 [4.6, 12.0] | 7.5 [4.6, 12.0] | -0.01066 [-0.01169, -0.00964] | 0 of 200 |
| most_recent | random_control | delayed mastery per item | 65 / 0 / 135 | 32.5 [26.4, 39.3] | 32.5 [26.4, 39.3] | -0.00248 [-0.00324, -0.00172] | 0 of 200 |
| five_term | two_term | mastery per item | 39 / 0 / 161 | 19.5 [14.6, 25.5] | 19.5 [14.6, 25.5] | -0.00549 [-0.00638, -0.00460] | 0 of 200 |
| five_term | two_term | delayed mastery per item | 50 / 0 / 150 | 25.0 [19.5, 31.4] | 25.0 [19.5, 31.4] | -0.00300 [-0.00379, -0.00221] | 0 of 200 |
| decay_lambda_2 | two_term | mastery per item | 2 / 194 / 4 | 98.0 [95.0, 99.2] | 1.0 [0.3, 3.6] | -0.00003 [-0.00012, 0.00005] | 149 of 200 |
| decay_lambda_2 | two_term | retention day 30 | 2 / 194 / 4 | 98.0 [95.0, 99.2] | 1.0 [0.3, 3.6] | -0.00004 [-0.00012, 0.00005] | 149 of 200 |
| decay_lambda_2 | two_term | delayed mastery per item | 3 / 194 / 3 | 98.5 [95.7, 99.5] | 1.5 [0.5, 4.3] | -0.00002 [-0.00009, 0.00005] | 149 of 200 |
| five_term_lambda_2 | five_term | mastery per item | 87 / 0 / 113 | 43.5 [36.8, 50.4] | 43.5 [36.8, 50.4] | -0.00112 [-0.00185, -0.00040] | 0 of 200 |
| five_term_lambda_2 | five_term | retention day 30 | 81 / 0 / 119 | 40.5 [33.9, 47.4] | 40.5 [33.9, 47.4] | -0.00150 [-0.00422, 0.00123] | 0 of 200 |
| five_term_lambda_2 | five_term | delayed mastery per item | 77 / 0 / 123 | 38.5 [32.0, 45.4] | 38.5 [32.0, 45.4] | -0.00097 [-0.00158, -0.00037] | 0 of 200 |

## World fixed, exponential forgetting, 226 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 2914 | 121.2 | 155.1 | 0.03335 [0.03236, 0.03434] | 0.02478 [0.02396, 0.02560] | 0.6895 |
| random_control | 200 | 2917 | 130.8 | 166.4 | 0.03703 [0.03603, 0.03803] | 0.02639 [0.02555, 0.02723] | 0.6988 |
| oracle_forgetting | 200 | 2915 | 89.2 | 135.7 | 0.02726 [0.02638, 0.02814] | 0.02151 [0.02071, 0.02230] | 0.7283 |
| oracle_teaching | 200 | 2908 | 134.2 | 152.5 | 0.03596 [0.03502, 0.03690] | 0.02519 [0.02444, 0.02595] | 0.6712 |
| most_recent | 200 | 2911 | 78.8 | 134.0 | 0.02430 [0.02340, 0.02521] | 0.02029 [0.01945, 0.02113] | 0.7230 |
| five_term | 200 | 2906 | 106.8 | 152.1 | 0.02902 [0.02809, 0.02996] | 0.02261 [0.02180, 0.02343] | 0.6946 |
| decay_lambda_2 | 200 | 2914 | 121.5 | 155.0 | 0.03337 [0.03239, 0.03436] | 0.02480 [0.02399, 0.02562] | 0.6888 |
| five_term_lambda_2 | 200 | 2905 | 104.9 | 152.1 | 0.02809 [0.02716, 0.02902] | 0.02169 [0.02090, 0.02248] | 0.6899 |
| two_term_reseeded | 200 | 2915 | 122.2 | 154.4 | 0.03349 [0.03255, 0.03444] | 0.02476 [0.02396, 0.02555] | 0.6878 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term | random_control | mastery per item | 40 / 0 / 160 | 20.0 [15.0, 26.1] | 20.0 [15.0, 26.1] | -0.00368 [-0.00429, -0.00307] | 0 of 200 |
| two_term | random_control | delayed mastery per item | 68 / 0 / 132 | 34.0 [27.8, 40.8] | 34.0 [27.8, 40.8] | -0.00161 [-0.00215, -0.00107] | 0 of 200 |
| two_term_reseeded | two_term | mastery per item | 104 / 0 / 96 | 52.0 [45.1, 58.8] | 52.0 [45.1, 58.8] | +0.00014 [-0.00047, 0.00075] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 98 / 0 / 102 | 49.0 [42.2, 55.9] | 49.0 [42.2, 55.9] | -0.00002 [-0.00054, 0.00050] | 0 of 200 |
| two_term_reseeded | random_control | mastery per item | 42 / 0 / 158 | 21.0 [15.9, 27.2] | 21.0 [15.9, 27.2] | -0.00354 [-0.00411, -0.00296] | 0 of 200 |
| two_term_reseeded | random_control | delayed mastery per item | 60 / 0 / 140 | 30.0 [24.1, 36.7] | 30.0 [24.1, 36.7] | -0.00163 [-0.00216, -0.00110] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 12 / 0 / 188 | 6.0 [3.5, 10.2] | 6.0 [3.5, 10.2] | -0.00977 [-0.01053, -0.00900] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 34 / 0 / 166 | 17.0 [12.4, 22.8] | 17.0 [12.4, 22.8] | -0.00488 [-0.00556, -0.00421] | 0 of 200 |
| oracle_teaching | random_control | mastery per item | 70 / 0 / 130 | 35.0 [28.7, 41.8] | 35.0 [28.7, 41.8] | -0.00107 [-0.00162, -0.00051] | 0 of 200 |
| oracle_teaching | random_control | delayed mastery per item | 68 / 0 / 132 | 34.0 [27.8, 40.8] | 34.0 [27.8, 40.8] | -0.00120 [-0.00172, -0.00067] | 0 of 200 |
| most_recent | random_control | mastery per item | 3 / 0 / 197 | 1.5 [0.5, 4.3] | 1.5 [0.5, 4.3] | -0.01272 [-0.01355, -0.01190] | 0 of 200 |
| most_recent | random_control | delayed mastery per item | 24 / 0 / 176 | 12.0 [8.2, 17.2] | 12.0 [8.2, 17.2] | -0.00610 [-0.00683, -0.00536] | 0 of 200 |
| five_term | two_term | mastery per item | 39 / 0 / 161 | 19.5 [14.6, 25.5] | 19.5 [14.6, 25.5] | -0.00433 [-0.00501, -0.00365] | 0 of 200 |
| five_term | two_term | delayed mastery per item | 57 / 0 / 143 | 28.5 [22.7, 35.1] | 28.5 [22.7, 35.1] | -0.00216 [-0.00273, -0.00160] | 0 of 200 |
| decay_lambda_2 | two_term | mastery per item | 9 / 182 / 9 | 95.5 [91.7, 97.6] | 4.5 [2.4, 8.3] | +0.00002 [-0.00011, 0.00016] | 79 of 200 |
| decay_lambda_2 | two_term | retention day 30 | 9 / 182 / 9 | 95.5 [91.7, 97.6] | 4.5 [2.4, 8.3] | -0.00062 [-0.00171, 0.00047] | 79 of 200 |
| decay_lambda_2 | two_term | delayed mastery per item | 10 / 182 / 8 | 96.0 [92.3, 98.0] | 5.0 [2.7, 9.0] | +0.00003 [-0.00010, 0.00015] | 79 of 200 |
| five_term_lambda_2 | five_term | mastery per item | 89 / 0 / 111 | 44.5 [37.8, 51.4] | 44.5 [37.8, 51.4] | -0.00093 [-0.00162, -0.00024] | 0 of 200 |
| five_term_lambda_2 | five_term | retention day 30 | 96 / 0 / 104 | 48.0 [41.2, 54.9] | 48.0 [41.2, 54.9] | -0.00466 [-0.00882, -0.00050] | 0 of 200 |
| five_term_lambda_2 | five_term | delayed mastery per item | 84 / 0 / 116 | 42.0 [35.4, 48.9] | 42.0 [35.4, 48.9] | -0.00092 [-0.00150, -0.00035] | 0 of 200 |

## World fixed, power law forgetting, 226 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 2914 | 116.5 | 146.6 | 0.03147 [0.03061, 0.03232] | 0.02398 [0.02326, 0.02470] | 0.6721 |
| random_control | 200 | 2916 | 125.1 | 156.1 | 0.03452 [0.03359, 0.03544] | 0.02515 [0.02438, 0.02592] | 0.6805 |
| oracle_forgetting | 200 | 2915 | 86.0 | 131.9 | 0.02576 [0.02492, 0.02660] | 0.02055 [0.01979, 0.02130] | 0.7084 |
| oracle_teaching | 200 | 2907 | 127.7 | 145.5 | 0.03375 [0.03287, 0.03464] | 0.02443 [0.02371, 0.02516] | 0.6567 |
| most_recent | 200 | 2911 | 75.2 | 128.6 | 0.02283 [0.02203, 0.02363] | 0.01912 [0.01838, 0.01987] | 0.6986 |
| five_term | 200 | 2905 | 104.3 | 148.1 | 0.02822 [0.02732, 0.02913] | 0.02238 [0.02162, 0.02314] | 0.6777 |
| decay_lambda_2 | 200 | 2914 | 116.5 | 146.3 | 0.03145 [0.03059, 0.03232] | 0.02399 [0.02327, 0.02471] | 0.6718 |
| five_term_lambda_2 | 200 | 2905 | 101.2 | 144.8 | 0.02712 [0.02626, 0.02798] | 0.02136 [0.02063, 0.02210] | 0.6732 |
| two_term_reseeded | 200 | 2914 | 116.5 | 147.6 | 0.03132 [0.03044, 0.03220] | 0.02375 [0.02302, 0.02449] | 0.6695 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| two_term | random_control | mastery per item | 41 / 0 / 159 | 20.5 [15.5, 26.6] | 20.5 [15.5, 26.6] | -0.00305 [-0.00358, -0.00252] | 0 of 200 |
| two_term | random_control | delayed mastery per item | 77 / 0 / 123 | 38.5 [32.0, 45.4] | 38.5 [32.0, 45.4] | -0.00117 [-0.00164, -0.00071] | 0 of 200 |
| two_term_reseeded | two_term | mastery per item | 97 / 0 / 103 | 48.5 [41.7, 55.4] | 48.5 [41.7, 55.4] | -0.00014 [-0.00067, 0.00039] | 0 of 200 |
| two_term_reseeded | two_term | delayed mastery per item | 95 / 0 / 105 | 47.5 [40.7, 54.4] | 47.5 [40.7, 54.4] | -0.00022 [-0.00068, 0.00023] | 0 of 200 |
| two_term_reseeded | random_control | mastery per item | 39 / 0 / 161 | 19.5 [14.6, 25.5] | 19.5 [14.6, 25.5] | -0.00319 [-0.00371, -0.00268] | 0 of 200 |
| two_term_reseeded | random_control | delayed mastery per item | 63 / 0 / 137 | 31.5 [25.5, 38.2] | 31.5 [25.5, 38.2] | -0.00140 [-0.00187, -0.00092] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 7 / 0 / 193 | 3.5 [1.7, 7.0] | 3.5 [1.7, 7.0] | -0.00876 [-0.00955, -0.00796] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 36 / 0 / 164 | 18.0 [13.3, 23.9] | 18.0 [13.3, 23.9] | -0.00460 [-0.00528, -0.00393] | 0 of 200 |
| oracle_teaching | random_control | mastery per item | 84 / 0 / 116 | 42.0 [35.4, 48.9] | 42.0 [35.4, 48.9] | -0.00077 [-0.00133, -0.00021] | 0 of 200 |
| oracle_teaching | random_control | delayed mastery per item | 87 / 0 / 113 | 43.5 [36.8, 50.4] | 43.5 [36.8, 50.4] | -0.00072 [-0.00118, -0.00026] | 0 of 200 |
| most_recent | random_control | mastery per item | 3 / 0 / 197 | 1.5 [0.5, 4.3] | 1.5 [0.5, 4.3] | -0.01169 [-0.01251, -0.01087] | 0 of 200 |
| most_recent | random_control | delayed mastery per item | 25 / 0 / 175 | 12.5 [8.6, 17.8] | 12.5 [8.6, 17.8] | -0.00603 [-0.00672, -0.00533] | 0 of 200 |
| five_term | two_term | mastery per item | 42 / 0 / 158 | 21.0 [15.9, 27.2] | 21.0 [15.9, 27.2] | -0.00324 [-0.00387, -0.00262] | 0 of 200 |
| five_term | two_term | delayed mastery per item | 65 / 0 / 135 | 32.5 [26.4, 39.3] | 32.5 [26.4, 39.3] | -0.00159 [-0.00213, -0.00106] | 0 of 200 |
| decay_lambda_2 | two_term | mastery per item | 4 / 189 / 7 | 96.5 [93.0, 98.3] | 2.0 [0.8, 5.0] | -0.00001 [-0.00011, 0.00008] | 77 of 200 |
| decay_lambda_2 | two_term | retention day 30 | 3 / 189 / 8 | 96.0 [92.3, 98.0] | 1.5 [0.5, 4.3] | -0.00028 [-0.00079, 0.00022] | 77 of 200 |
| decay_lambda_2 | two_term | delayed mastery per item | 6 / 189 / 5 | 97.5 [94.3, 98.9] | 3.0 [1.4, 6.4] | +0.00001 [-0.00006, 0.00009] | 77 of 200 |
| five_term_lambda_2 | five_term | mastery per item | 81 / 0 / 119 | 40.5 [33.9, 47.4] | 40.5 [33.9, 47.4] | -0.00110 [-0.00173, -0.00047] | 0 of 200 |
| five_term_lambda_2 | five_term | retention day 30 | 91 / 0 / 109 | 45.5 [38.7, 52.4] | 45.5 [38.7, 52.4] | -0.00453 [-0.00809, -0.00097] | 0 of 200 |
| five_term_lambda_2 | five_term | delayed mastery per item | 77 / 0 / 123 | 38.5 [32.0, 45.4] | 38.5 [32.0, 45.4] | -0.00102 [-0.00153, -0.00051] | 0 of 200 |
