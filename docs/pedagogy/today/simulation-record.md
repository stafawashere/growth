---
title: Today selection study record
research_date: 2026-09-29
status: recorded
purpose: The numbers behind the Today selection policies of app/sim/today_policies.py, written by tools/today_sim_study.py; simulation only.
---

# Today selection study record

Written by `tools/today_sim_study.py` in 272 minutes, seed base 20270510, 200 synthetic students per arm, every arm on the same students. Every number is a simulation's measurement on synthetic students whose world model is invented; none is a person's and none is the student's. Intervals are 95 percent: Wilson for shares, normal approximation for means. Worlds: `legacy` is the stage 8 world, `fixed` adds keyed draws, consolidated prior knowledge and daily half-life growth (`app/sim/learning.py` WorldRules). Every arm keeps the full interleaving rules and the shipped block 1; `review_first` and `retrievability_priority_both` change block 3, every other candidate changes block 2 only.

Mastery per item is the stage 8 measure, read the day after the run. Delayed mastery per item reads the same skills 30 days after the run. Retention day 30 averages over every known skill. Skills learned counts the skills the world turned known during the run.

## World fixed, exponential forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 756 | 38.9 | 52.3 | 0.04529 [0.04337, 0.04722] | 0.03053 [0.02911, 0.03195] | 0.8161 |
| random_control | 200 | 759 | 42.2 | 56.6 | 0.04831 [0.04632, 0.05030] | 0.03113 [0.02969, 0.03257] | 0.8093 |
| oracle_forgetting | 200 | 757 | 33.5 | 48.9 | 0.04152 [0.03999, 0.04306] | 0.03060 [0.02927, 0.03193] | 0.8386 |
| retrievability_priority | 200 | 751 | 29.4 | 47.8 | 0.03693 [0.03537, 0.03848] | 0.02924 [0.02784, 0.03064] | 0.8431 |
| retrievability_priority_both | 200 | 751 | 30.0 | 49.4 | 0.03763 [0.03611, 0.03915] | 0.02983 [0.02846, 0.03119] | 0.8415 |
| elo_target | 200 | 746 | 31.7 | 47.2 | 0.03290 [0.03143, 0.03437] | 0.02310 [0.02188, 0.02431] | 0.8126 |
| spread | 200 | 759 | 38.5 | 55.9 | 0.04629 [0.04441, 0.04816] | 0.03356 [0.03208, 0.03505] | 0.8284 |
| review_first | 200 | 757 | 40.2 | 54.7 | 0.04639 [0.04452, 0.04825] | 0.03121 [0.02983, 0.03259] | 0.8114 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| oracle_forgetting | two_term | mastery per item | 73 / 0 / 127 | 36.5 [30.1, 43.4] | 36.5 [30.1, 43.4] | -0.00377 [-0.00502, -0.00252] | 0 of 200 |
| oracle_forgetting | two_term | delayed mastery per item | 109 / 0 / 91 | 54.5 [47.6, 61.3] | 54.5 [47.6, 61.3] | +0.00007 [-0.00088, 0.00102] | 0 of 200 |
| oracle_forgetting | two_term | retention day 30 | 155 / 0 / 45 | 77.5 [71.2, 82.7] | 77.5 [71.2, 82.7] | +0.02248 [0.01816, 0.02680] | 0 of 200 |
| oracle_forgetting | two_term | skills learned | 51 / 7 / 142 | 29.0 [23.2, 35.6] | 25.5 [20.0, 32.0] | -5.33500 [-6.51168, -4.15832] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 52 / 0 / 148 | 26.0 [20.4, 32.5] | 26.0 [20.4, 32.5] | -0.00678 [-0.00808, -0.00548] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 98 / 0 / 102 | 49.0 [42.2, 55.9] | 49.0 [42.2, 55.9] | -0.00053 [-0.00154, 0.00048] | 0 of 200 |
| oracle_forgetting | random_control | retention day 30 | 168 / 0 / 32 | 84.0 [78.3, 88.4] | 84.0 [78.3, 88.4] | +0.02928 [0.02482, 0.03373] | 0 of 200 |
| oracle_forgetting | random_control | skills learned | 30 / 7 / 163 | 18.5 [13.7, 24.5] | 15.0 [10.7, 20.6] | -8.63500 [-9.86752, -7.40248] | 0 of 200 |
| retrievability_priority | two_term | mastery per item | 26 / 0 / 174 | 13.0 [9.0, 18.4] | 13.0 [9.0, 18.4] | -0.00837 [-0.00940, -0.00733] | 0 of 200 |
| retrievability_priority | two_term | delayed mastery per item | 85 / 0 / 115 | 42.5 [35.9, 49.4] | 42.5 [35.9, 49.4] | -0.00130 [-0.00219, -0.00040] | 0 of 200 |
| retrievability_priority | two_term | retention day 30 | 162 / 0 / 38 | 81.0 [75.0, 85.8] | 81.0 [75.0, 85.8] | +0.02702 [0.02288, 0.03115] | 0 of 200 |
| retrievability_priority | two_term | skills learned | 16 / 5 / 179 | 10.5 [7.0, 15.5] | 8.0 [5.0, 12.6] | -9.52500 [-10.49370, -8.55630] | 0 of 200 |
| retrievability_priority | random_control | mastery per item | 14 / 0 / 186 | 7.0 [4.2, 11.4] | 7.0 [4.2, 11.4] | -0.01138 [-0.01245, -0.01031] | 0 of 200 |
| retrievability_priority | random_control | delayed mastery per item | 76 / 0 / 124 | 38.0 [31.6, 44.9] | 38.0 [31.6, 44.9] | -0.00189 [-0.00293, -0.00086] | 0 of 200 |
| retrievability_priority | random_control | retention day 30 | 174 / 0 / 26 | 87.0 [81.6, 91.0] | 87.0 [81.6, 91.0] | +0.03381 [0.02942, 0.03821] | 0 of 200 |
| retrievability_priority | random_control | skills learned | 7 / 2 / 191 | 4.5 [2.4, 8.3] | 3.5 [1.7, 7.0] | -12.82500 [-13.82135, -11.82865] | 0 of 200 |
| retrievability_priority_both | two_term | mastery per item | 26 / 0 / 174 | 13.0 [9.0, 18.4] | 13.0 [9.0, 18.4] | -0.00767 [-0.00869, -0.00664] | 0 of 200 |
| retrievability_priority_both | two_term | delayed mastery per item | 96 / 0 / 104 | 48.0 [41.2, 54.9] | 48.0 [41.2, 54.9] | -0.00071 [-0.00163, 0.00022] | 0 of 200 |
| retrievability_priority_both | two_term | retention day 30 | 158 / 0 / 42 | 79.0 [72.8, 84.1] | 79.0 [72.8, 84.1] | +0.02540 [0.02119, 0.02961] | 0 of 200 |
| retrievability_priority_both | two_term | skills learned | 18 / 3 / 179 | 10.5 [7.0, 15.5] | 9.0 [5.8, 13.8] | -8.92500 [-9.88338, -7.96662] | 0 of 200 |
| retrievability_priority_both | random_control | mastery per item | 15 / 0 / 185 | 7.5 [4.6, 12.0] | 7.5 [4.6, 12.0] | -0.01068 [-0.01177, -0.00960] | 0 of 200 |
| retrievability_priority_both | random_control | delayed mastery per item | 82 / 0 / 118 | 41.0 [34.4, 47.9] | 41.0 [34.4, 47.9] | -0.00130 [-0.00236, -0.00025] | 0 of 200 |
| retrievability_priority_both | random_control | retention day 30 | 164 / 0 / 36 | 82.0 [76.1, 86.7] | 82.0 [76.1, 86.7] | +0.03220 [0.02755, 0.03684] | 0 of 200 |
| retrievability_priority_both | random_control | skills learned | 5 / 4 / 191 | 4.5 [2.4, 8.3] | 2.5 [1.1, 5.7] | -12.22500 [-13.22406, -11.22594] | 0 of 200 |
| elo_target | two_term | mastery per item | 2 / 0 / 198 | 1.0 [0.3, 3.6] | 1.0 [0.3, 3.6] | -0.01240 [-0.01344, -0.01135] | 0 of 200 |
| elo_target | two_term | delayed mastery per item | 22 / 0 / 178 | 11.0 [7.4, 16.1] | 11.0 [7.4, 16.1] | -0.00744 [-0.00830, -0.00657] | 0 of 200 |
| elo_target | two_term | retention day 30 | 86 / 0 / 114 | 43.0 [36.3, 49.9] | 43.0 [36.3, 49.9] | -0.00349 [-0.00704, 0.00005] | 0 of 200 |
| elo_target | two_term | skills learned | 19 / 4 / 177 | 11.5 [7.8, 16.7] | 9.5 [6.2, 14.4] | -7.18000 [-8.06462, -6.29538] | 0 of 200 |
| elo_target | random_control | mastery per item | 2 / 0 / 198 | 1.0 [0.3, 3.6] | 1.0 [0.3, 3.6] | -0.01541 [-0.01645, -0.01437] | 0 of 200 |
| elo_target | random_control | delayed mastery per item | 18 / 0 / 182 | 9.0 [5.8, 13.8] | 9.0 [5.8, 13.8] | -0.00803 [-0.00893, -0.00714] | 0 of 200 |
| elo_target | random_control | retention day 30 | 114 / 0 / 86 | 57.0 [50.1, 63.7] | 57.0 [50.1, 63.7] | +0.00330 [-0.00005, 0.00665] | 0 of 200 |
| elo_target | random_control | skills learned | 6 / 4 / 190 | 5.0 [2.7, 9.0] | 3.0 [1.4, 6.4] | -10.48000 [-11.31895, -9.64105] | 0 of 200 |
| spread | two_term | mastery per item | 118 / 0 / 82 | 59.0 [52.1, 65.6] | 59.0 [52.1, 65.6] | +0.00099 [0.00018, 0.00181] | 0 of 200 |
| spread | two_term | delayed mastery per item | 139 / 0 / 61 | 69.5 [62.8, 75.5] | 69.5 [62.8, 75.5] | +0.00303 [0.00216, 0.00390] | 0 of 200 |
| spread | two_term | retention day 30 | 138 / 0 / 62 | 69.0 [62.3, 75.0] | 69.0 [62.3, 75.0] | +0.01236 [0.00862, 0.01611] | 0 of 200 |
| spread | two_term | skills learned | 94 / 9 / 97 | 51.5 [44.6, 58.3] | 47.0 [40.2, 53.9] | -0.42000 [-1.18106, 0.34106] | 0 of 200 |
| spread | random_control | mastery per item | 72 / 0 / 128 | 36.0 [29.7, 42.9] | 36.0 [29.7, 42.9] | -0.00202 [-0.00288, -0.00116] | 0 of 200 |
| spread | random_control | delayed mastery per item | 124 / 0 / 76 | 62.0 [55.1, 68.4] | 62.0 [55.1, 68.4] | +0.00243 [0.00155, 0.00332] | 0 of 200 |
| spread | random_control | retention day 30 | 154 / 0 / 46 | 77.0 [70.7, 82.3] | 77.0 [70.7, 82.3] | +0.01916 [0.01548, 0.02284] | 0 of 200 |
| spread | random_control | skills learned | 44 / 13 / 143 | 28.5 [22.7, 35.1] | 22.0 [16.8, 28.2] | -3.72000 [-4.51745, -2.92255] | 0 of 200 |
| review_first | two_term | mastery per item | 115 / 0 / 85 | 57.5 [50.6, 64.1] | 57.5 [50.6, 64.1] | +0.00109 [0.00025, 0.00194] | 0 of 200 |
| review_first | two_term | delayed mastery per item | 102 / 0 / 98 | 51.0 [44.1, 57.8] | 51.0 [44.1, 57.8] | +0.00068 [-0.00013, 0.00148] | 0 of 200 |
| review_first | two_term | retention day 30 | 95 / 0 / 105 | 47.5 [40.7, 54.4] | 47.5 [40.7, 54.4] | -0.00465 [-0.00790, -0.00140] | 0 of 200 |
| review_first | two_term | skills learned | 107 / 16 / 77 | 61.5 [54.6, 68.0] | 53.5 [46.6, 60.3] | +1.32500 [0.57075, 2.07925] | 0 of 200 |
| review_first | random_control | mastery per item | 77 / 0 / 123 | 38.5 [32.0, 45.4] | 38.5 [32.0, 45.4] | -0.00192 [-0.00290, -0.00095] | 0 of 200 |
| review_first | random_control | delayed mastery per item | 101 / 0 / 99 | 50.5 [43.6, 57.4] | 50.5 [43.6, 57.4] | +0.00008 [-0.00090, 0.00107] | 0 of 200 |
| review_first | random_control | retention day 30 | 103 / 0 / 97 | 51.5 [44.6, 58.3] | 51.5 [44.6, 58.3] | +0.00215 [-0.00139, 0.00568] | 0 of 200 |
| review_first | random_control | skills learned | 60 / 12 / 128 | 36.0 [29.7, 42.9] | 30.0 [24.1, 36.7] | -1.97500 [-2.79433, -1.15567] | 0 of 200 |

## World fixed, power law forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 756 | 38.0 | 51.0 | 0.04342 [0.04164, 0.04520] | 0.03048 [0.02917, 0.03178] | 0.7884 |
| random_control | 200 | 758 | 41.4 | 55.0 | 0.04665 [0.04479, 0.04850] | 0.03156 [0.03025, 0.03287] | 0.7836 |
| oracle_forgetting | 200 | 757 | 32.9 | 47.6 | 0.04024 [0.03878, 0.04170] | 0.03031 [0.02908, 0.03154] | 0.8086 |
| retrievability_priority | 200 | 751 | 28.9 | 47.2 | 0.03600 [0.03450, 0.03750] | 0.02868 [0.02737, 0.03000] | 0.8106 |
| retrievability_priority_both | 200 | 750 | 29.5 | 48.4 | 0.03662 [0.03511, 0.03813] | 0.02938 [0.02805, 0.03071] | 0.8083 |
| elo_target | 200 | 746 | 31.5 | 46.7 | 0.03301 [0.03155, 0.03446] | 0.02356 [0.02242, 0.02469] | 0.7821 |
| spread | 200 | 758 | 38.0 | 53.7 | 0.04494 [0.04314, 0.04675] | 0.03292 [0.03152, 0.03432] | 0.7968 |
| review_first | 200 | 756 | 39.3 | 52.7 | 0.04456 [0.04275, 0.04637] | 0.03140 [0.03007, 0.03274] | 0.7838 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| oracle_forgetting | two_term | mastery per item | 73 / 0 / 127 | 36.5 [30.1, 43.4] | 36.5 [30.1, 43.4] | -0.00318 [-0.00425, -0.00211] | 0 of 200 |
| oracle_forgetting | two_term | delayed mastery per item | 100 / 0 / 100 | 50.0 [43.1, 56.9] | 50.0 [43.1, 56.9] | -0.00016 [-0.00099, 0.00066] | 0 of 200 |
| oracle_forgetting | two_term | retention day 30 | 157 / 0 / 43 | 78.5 [72.3, 83.6] | 78.5 [72.3, 83.6] | +0.02018 [0.01680, 0.02357] | 0 of 200 |
| oracle_forgetting | two_term | skills learned | 51 / 12 / 137 | 31.5 [25.5, 38.2] | 25.5 [20.0, 32.0] | -5.12000 [-6.19458, -4.04542] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 39 / 0 / 161 | 19.5 [14.6, 25.5] | 19.5 [14.6, 25.5] | -0.00641 [-0.00756, -0.00527] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 86 / 0 / 114 | 43.0 [36.3, 49.9] | 43.0 [36.3, 49.9] | -0.00125 [-0.00207, -0.00043] | 0 of 200 |
| oracle_forgetting | random_control | retention day 30 | 173 / 0 / 27 | 86.5 [81.1, 90.6] | 86.5 [81.1, 90.6] | +0.02501 [0.02145, 0.02856] | 0 of 200 |
| oracle_forgetting | random_control | skills learned | 26 / 6 / 168 | 16.0 [11.6, 21.7] | 13.0 [9.0, 18.4] | -8.45000 [-9.61427, -7.28573] | 0 of 200 |
| retrievability_priority | two_term | mastery per item | 27 / 0 / 173 | 13.5 [9.4, 18.9] | 13.5 [9.4, 18.9] | -0.00742 [-0.00838, -0.00646] | 0 of 200 |
| retrievability_priority | two_term | delayed mastery per item | 74 / 0 / 126 | 37.0 [30.6, 43.9] | 37.0 [30.6, 43.9] | -0.00179 [-0.00258, -0.00100] | 0 of 200 |
| retrievability_priority | two_term | retention day 30 | 159 / 0 / 41 | 79.5 [73.4, 84.5] | 79.5 [73.4, 84.5] | +0.02221 [0.01857, 0.02585] | 0 of 200 |
| retrievability_priority | two_term | skills learned | 17 / 6 / 177 | 11.5 [7.8, 16.7] | 8.5 [5.4, 13.2] | -9.10500 [-10.05432, -8.15568] | 0 of 200 |
| retrievability_priority | random_control | mastery per item | 13 / 0 / 187 | 6.5 [3.8, 10.8] | 6.5 [3.8, 10.8] | -0.01065 [-0.01168, -0.00961] | 0 of 200 |
| retrievability_priority | random_control | delayed mastery per item | 61 / 0 / 139 | 30.5 [24.5, 37.2] | 30.5 [24.5, 37.2] | -0.00288 [-0.00371, -0.00205] | 0 of 200 |
| retrievability_priority | random_control | retention day 30 | 165 / 0 / 35 | 82.5 [76.6, 87.1] | 82.5 [76.6, 87.1] | +0.02703 [0.02314, 0.03092] | 0 of 200 |
| retrievability_priority | random_control | skills learned | 3 / 2 / 195 | 2.5 [1.1, 5.7] | 1.5 [0.5, 4.3] | -12.43500 [-13.46967, -11.40033] | 0 of 200 |
| retrievability_priority_both | two_term | mastery per item | 34 / 0 / 166 | 17.0 [12.4, 22.8] | 17.0 [12.4, 22.8] | -0.00680 [-0.00779, -0.00582] | 0 of 200 |
| retrievability_priority_both | two_term | delayed mastery per item | 81 / 0 / 119 | 40.5 [33.9, 47.4] | 40.5 [33.9, 47.4] | -0.00109 [-0.00195, -0.00024] | 0 of 200 |
| retrievability_priority_both | two_term | retention day 30 | 152 / 0 / 48 | 76.0 [69.6, 81.4] | 76.0 [69.6, 81.4] | +0.01991 [0.01628, 0.02354] | 0 of 200 |
| retrievability_priority_both | two_term | skills learned | 19 / 4 / 177 | 11.5 [7.8, 16.7] | 9.5 [6.2, 14.4] | -8.54500 [-9.49263, -7.59737] | 0 of 200 |
| retrievability_priority_both | random_control | mastery per item | 15 / 0 / 185 | 7.5 [4.6, 12.0] | 7.5 [4.6, 12.0] | -0.01003 [-0.01099, -0.00907] | 0 of 200 |
| retrievability_priority_both | random_control | delayed mastery per item | 70 / 0 / 130 | 35.0 [28.7, 41.8] | 35.0 [28.7, 41.8] | -0.00218 [-0.00299, -0.00137] | 0 of 200 |
| retrievability_priority_both | random_control | retention day 30 | 159 / 0 / 41 | 79.5 [73.4, 84.5] | 79.5 [73.4, 84.5] | +0.02474 [0.02079, 0.02868] | 0 of 200 |
| retrievability_priority_both | random_control | skills learned | 8 / 3 / 189 | 5.5 [3.1, 9.6] | 4.0 [2.0, 7.7] | -11.87500 [-12.83820, -10.91180] | 0 of 200 |
| elo_target | two_term | mastery per item | 7 / 0 / 193 | 3.5 [1.7, 7.0] | 3.5 [1.7, 7.0] | -0.01041 [-0.01134, -0.00949] | 0 of 200 |
| elo_target | two_term | delayed mastery per item | 17 / 0 / 183 | 8.5 [5.4, 13.2] | 8.5 [5.4, 13.2] | -0.00692 [-0.00768, -0.00616] | 0 of 200 |
| elo_target | two_term | retention day 30 | 73 / 0 / 127 | 36.5 [30.1, 43.4] | 36.5 [30.1, 43.4] | -0.00625 [-0.00943, -0.00307] | 0 of 200 |
| elo_target | two_term | skills learned | 19 / 7 / 174 | 13.0 [9.0, 18.4] | 9.5 [6.2, 14.4] | -6.49500 [-7.39415, -5.59585] | 0 of 200 |
| elo_target | random_control | mastery per item | 5 / 0 / 195 | 2.5 [1.1, 5.7] | 2.5 [1.1, 5.7] | -0.01364 [-0.01461, -0.01268] | 0 of 200 |
| elo_target | random_control | delayed mastery per item | 13 / 0 / 187 | 6.5 [3.8, 10.8] | 6.5 [3.8, 10.8] | -0.00801 [-0.00876, -0.00725] | 0 of 200 |
| elo_target | random_control | retention day 30 | 96 / 0 / 104 | 48.0 [41.2, 54.9] | 48.0 [41.2, 54.9] | -0.00143 [-0.00426, 0.00141] | 0 of 200 |
| elo_target | random_control | skills learned | 10 / 0 / 190 | 5.0 [2.7, 9.0] | 5.0 [2.7, 9.0] | -9.82500 [-10.69473, -8.95527] | 0 of 200 |
| spread | two_term | mastery per item | 121 / 0 / 79 | 60.5 [53.6, 67.0] | 60.5 [53.6, 67.0] | +0.00152 [0.00076, 0.00228] | 0 of 200 |
| spread | two_term | delayed mastery per item | 134 / 0 / 66 | 67.0 [60.2, 73.1] | 67.0 [60.2, 73.1] | +0.00244 [0.00170, 0.00318] | 0 of 200 |
| spread | two_term | retention day 30 | 130 / 0 / 70 | 65.0 [58.2, 71.3] | 65.0 [58.2, 71.3] | +0.00838 [0.00547, 0.01128] | 0 of 200 |
| spread | two_term | skills learned | 88 / 17 / 95 | 52.5 [45.6, 59.3] | 44.0 [37.3, 50.9] | -0.04000 [-0.74708, 0.66708] | 0 of 200 |
| spread | random_control | mastery per item | 78 / 0 / 122 | 39.0 [32.5, 45.9] | 39.0 [32.5, 45.9] | -0.00171 [-0.00249, -0.00092] | 0 of 200 |
| spread | random_control | delayed mastery per item | 116 / 0 / 84 | 58.0 [51.1, 64.6] | 58.0 [51.1, 64.6] | +0.00135 [0.00060, 0.00211] | 0 of 200 |
| spread | random_control | retention day 30 | 143 / 0 / 57 | 71.5 [64.9, 77.3] | 71.5 [64.9, 77.3] | +0.01320 [0.01029, 0.01611] | 0 of 200 |
| spread | random_control | skills learned | 52 / 10 / 138 | 31.0 [25.0, 37.7] | 26.0 [20.4, 32.5] | -3.37000 [-4.12838, -2.61162] | 0 of 200 |
| review_first | two_term | mastery per item | 116 / 0 / 84 | 58.0 [51.1, 64.6] | 58.0 [51.1, 64.6] | +0.00114 [0.00046, 0.00182] | 0 of 200 |
| review_first | two_term | delayed mastery per item | 111 / 0 / 89 | 55.5 [48.6, 62.2] | 55.5 [48.6, 62.2] | +0.00093 [0.00024, 0.00161] | 0 of 200 |
| review_first | two_term | retention day 30 | 75 / 0 / 125 | 37.5 [31.1, 44.4] | 37.5 [31.1, 44.4] | -0.00461 [-0.00762, -0.00161] | 0 of 200 |
| review_first | two_term | skills learned | 110 / 21 / 69 | 65.5 [58.7, 71.7] | 55.0 [48.1, 61.7] | +1.29500 [0.61422, 1.97578] | 0 of 200 |
| review_first | random_control | mastery per item | 75 / 0 / 125 | 37.5 [31.1, 44.4] | 37.5 [31.1, 44.4] | -0.00209 [-0.00293, -0.00125] | 0 of 200 |
| review_first | random_control | delayed mastery per item | 96 / 0 / 104 | 48.0 [41.2, 54.9] | 48.0 [41.2, 54.9] | -0.00016 [-0.00088, 0.00056] | 0 of 200 |
| review_first | random_control | retention day 30 | 93 / 0 / 107 | 46.5 [39.7, 53.4] | 46.5 [39.7, 53.4] | +0.00021 [-0.00286, 0.00328] | 0 of 200 |
| review_first | random_control | skills learned | 67 / 12 / 121 | 39.5 [33.0, 46.4] | 33.5 [27.3, 40.3] | -2.03500 [-2.87296, -1.19704] | 0 of 200 |

## World fixed, exponential forgetting, 226 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 2914 | 121.2 | 155.1 | 0.03335 [0.03236, 0.03434] | 0.02478 [0.02396, 0.02560] | 0.6895 |
| random_control | 200 | 2917 | 130.8 | 166.4 | 0.03703 [0.03603, 0.03803] | 0.02639 [0.02555, 0.02723] | 0.6988 |
| oracle_forgetting | 200 | 2915 | 89.2 | 135.7 | 0.02726 [0.02638, 0.02814] | 0.02151 [0.02071, 0.02230] | 0.7283 |
| retrievability_priority | 200 | 2908 | 72.9 | 121.2 | 0.02218 [0.02128, 0.02308] | 0.01814 [0.01730, 0.01897] | 0.7101 |
| retrievability_priority_both | 200 | 2909 | 73.3 | 125.2 | 0.02187 [0.02098, 0.02275] | 0.01772 [0.01691, 0.01854] | 0.6964 |
| elo_target | 200 | 2904 | 109.7 | 154.2 | 0.02802 [0.02714, 0.02889] | 0.02288 [0.02213, 0.02362] | 0.6916 |
| spread | 200 | 2917 | 106.0 | 156.7 | 0.03172 [0.03073, 0.03272] | 0.02569 [0.02477, 0.02662] | 0.7219 |
| review_first | 200 | 2915 | 126.0 | 158.1 | 0.03387 [0.03289, 0.03484] | 0.02519 [0.02437, 0.02601] | 0.6741 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| oracle_forgetting | two_term | mastery per item | 30 / 0 / 170 | 15.0 [10.7, 20.6] | 15.0 [10.7, 20.6] | -0.00609 [-0.00690, -0.00528] | 0 of 200 |
| oracle_forgetting | two_term | delayed mastery per item | 48 / 0 / 152 | 24.0 [18.6, 30.4] | 24.0 [18.6, 30.4] | -0.00327 [-0.00396, -0.00259] | 0 of 200 |
| oracle_forgetting | two_term | retention day 30 | 175 / 0 / 25 | 87.5 [82.2, 91.4] | 87.5 [82.2, 91.4] | +0.03881 [0.03392, 0.04371] | 0 of 200 |
| oracle_forgetting | two_term | skills learned | 11 / 2 / 187 | 6.5 [3.8, 10.8] | 5.5 [3.1, 9.6] | -32.01000 [-34.92709, -29.09291] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 12 / 0 / 188 | 6.0 [3.5, 10.2] | 6.0 [3.5, 10.2] | -0.00977 [-0.01053, -0.00900] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 34 / 0 / 166 | 17.0 [12.4, 22.8] | 17.0 [12.4, 22.8] | -0.00488 [-0.00556, -0.00421] | 0 of 200 |
| oracle_forgetting | random_control | retention day 30 | 153 / 0 / 47 | 76.5 [70.2, 81.8] | 76.5 [70.2, 81.8] | +0.02945 [0.02382, 0.03509] | 0 of 200 |
| oracle_forgetting | random_control | skills learned | 7 / 0 / 193 | 3.5 [1.7, 7.0] | 3.5 [1.7, 7.0] | -41.64000 [-44.39695, -38.88305] | 0 of 200 |
| retrievability_priority | two_term | mastery per item | 8 / 0 / 192 | 4.0 [2.0, 7.7] | 4.0 [2.0, 7.7] | -0.01117 [-0.01200, -0.01035] | 0 of 200 |
| retrievability_priority | two_term | delayed mastery per item | 20 / 0 / 180 | 10.0 [6.6, 14.9] | 10.0 [6.6, 14.9] | -0.00664 [-0.00734, -0.00595] | 0 of 200 |
| retrievability_priority | two_term | retention day 30 | 145 / 0 / 55 | 72.5 [65.9, 78.2] | 72.5 [65.9, 78.2] | +0.02065 [0.01551, 0.02579] | 0 of 200 |
| retrievability_priority | two_term | skills learned | 2 / 0 / 198 | 1.0 [0.3, 3.6] | 1.0 [0.3, 3.6] | -48.32500 [-51.21533, -45.43467] | 0 of 200 |
| retrievability_priority | random_control | mastery per item | 2 / 0 / 198 | 1.0 [0.3, 3.6] | 1.0 [0.3, 3.6] | -0.01485 [-0.01568, -0.01402] | 0 of 200 |
| retrievability_priority | random_control | delayed mastery per item | 15 / 0 / 185 | 7.5 [4.6, 12.0] | 7.5 [4.6, 12.0] | -0.00825 [-0.00899, -0.00752] | 0 of 200 |
| retrievability_priority | random_control | retention day 30 | 112 / 0 / 88 | 56.0 [49.1, 62.7] | 56.0 [49.1, 62.7] | +0.01129 [0.00537, 0.01721] | 0 of 200 |
| retrievability_priority | random_control | skills learned | 0 / 0 / 200 | 0.0 [0.0, 1.9] | 0.0 [0.0, 1.9] | -57.95500 [-60.77078, -55.13922] | 0 of 200 |
| retrievability_priority_both | two_term | mastery per item | 4 / 0 / 196 | 2.0 [0.8, 5.0] | 2.0 [0.8, 5.0] | -0.01148 [-0.01235, -0.01062] | 0 of 200 |
| retrievability_priority_both | two_term | delayed mastery per item | 20 / 0 / 180 | 10.0 [6.6, 14.9] | 10.0 [6.6, 14.9] | -0.00705 [-0.00779, -0.00631] | 0 of 200 |
| retrievability_priority_both | two_term | retention day 30 | 116 / 0 / 84 | 58.0 [51.1, 64.6] | 58.0 [51.1, 64.6] | +0.00689 [0.00147, 0.01231] | 0 of 200 |
| retrievability_priority_both | two_term | skills learned | 2 / 0 / 198 | 1.0 [0.3, 3.6] | 1.0 [0.3, 3.6] | -47.89500 [-50.96117, -44.82883] | 0 of 200 |
| retrievability_priority_both | random_control | mastery per item | 0 / 0 / 200 | 0.0 [0.0, 1.9] | 0.0 [0.0, 1.9] | -0.01516 [-0.01601, -0.01431] | 0 of 200 |
| retrievability_priority_both | random_control | delayed mastery per item | 7 / 0 / 193 | 3.5 [1.7, 7.0] | 3.5 [1.7, 7.0] | -0.00866 [-0.00940, -0.00792] | 0 of 200 |
| retrievability_priority_both | random_control | retention day 30 | 87 / 0 / 113 | 43.5 [36.8, 50.4] | 43.5 [36.8, 50.4] | -0.00247 [-0.00873, 0.00379] | 0 of 200 |
| retrievability_priority_both | random_control | skills learned | 0 / 0 / 200 | 0.0 [0.0, 1.9] | 0.0 [0.0, 1.9] | -57.52500 [-60.40731, -54.64269] | 0 of 200 |
| elo_target | two_term | mastery per item | 34 / 0 / 166 | 17.0 [12.4, 22.8] | 17.0 [12.4, 22.8] | -0.00534 [-0.00613, -0.00454] | 0 of 200 |
| elo_target | two_term | delayed mastery per item | 70 / 0 / 130 | 35.0 [28.7, 41.8] | 35.0 [28.7, 41.8] | -0.00190 [-0.00255, -0.00125] | 0 of 200 |
| elo_target | two_term | retention day 30 | 108 / 0 / 92 | 54.0 [47.1, 60.8] | 54.0 [47.1, 60.8] | +0.00212 [-0.00235, 0.00658] | 0 of 200 |
| elo_target | two_term | skills learned | 51 / 2 / 147 | 26.5 [20.9, 33.0] | 25.5 [20.0, 32.0] | -11.47500 [-14.42473, -8.52527] | 0 of 200 |
| elo_target | random_control | mastery per item | 9 / 0 / 191 | 4.5 [2.4, 8.3] | 4.5 [2.4, 8.3] | -0.00901 [-0.00981, -0.00822] | 0 of 200 |
| elo_target | random_control | delayed mastery per item | 48 / 0 / 152 | 24.0 [18.6, 30.4] | 24.0 [18.6, 30.4] | -0.00351 [-0.00420, -0.00282] | 0 of 200 |
| elo_target | random_control | retention day 30 | 87 / 0 / 113 | 43.5 [36.8, 50.4] | 43.5 [36.8, 50.4] | -0.00724 [-0.01225, -0.00224] | 0 of 200 |
| elo_target | random_control | skills learned | 20 / 5 / 175 | 12.5 [8.6, 17.8] | 10.0 [6.6, 14.9] | -21.10500 [-24.02088, -18.18912] | 0 of 200 |
| spread | two_term | mastery per item | 76 / 0 / 124 | 38.0 [31.6, 44.9] | 38.0 [31.6, 44.9] | -0.00163 [-0.00233, -0.00092] | 0 of 200 |
| spread | two_term | delayed mastery per item | 112 / 0 / 88 | 56.0 [49.1, 62.7] | 56.0 [49.1, 62.7] | +0.00092 [0.00030, 0.00154] | 0 of 200 |
| spread | two_term | retention day 30 | 167 / 0 / 33 | 83.5 [77.7, 88.0] | 83.5 [77.7, 88.0] | +0.03247 [0.02798, 0.03695] | 0 of 200 |
| spread | two_term | skills learned | 36 / 5 / 159 | 20.5 [15.5, 26.6] | 18.0 [13.3, 23.9] | -15.22000 [-17.76532, -12.67468] | 0 of 200 |
| spread | random_control | mastery per item | 28 / 0 / 172 | 14.0 [9.9, 19.5] | 14.0 [9.9, 19.5] | -0.00530 [-0.00596, -0.00465] | 0 of 200 |
| spread | random_control | delayed mastery per item | 88 / 0 / 112 | 44.0 [37.3, 50.9] | 44.0 [37.3, 50.9] | -0.00069 [-0.00128, -0.00011] | 0 of 200 |
| spread | random_control | retention day 30 | 142 / 0 / 58 | 71.0 [64.4, 76.8] | 71.0 [64.4, 76.8] | +0.02311 [0.01814, 0.02808] | 0 of 200 |
| spread | random_control | skills learned | 14 / 0 / 186 | 7.0 [4.2, 11.4] | 7.0 [4.2, 11.4] | -24.85000 [-27.22043, -22.47957] | 0 of 200 |
| review_first | two_term | mastery per item | 104 / 0 / 96 | 52.0 [45.1, 58.8] | 52.0 [45.1, 58.8] | +0.00052 [-0.00011, 0.00115] | 0 of 200 |
| review_first | two_term | delayed mastery per item | 102 / 0 / 98 | 51.0 [44.1, 57.8] | 51.0 [44.1, 57.8] | +0.00041 [-0.00014, 0.00096] | 0 of 200 |
| review_first | two_term | retention day 30 | 59 / 0 / 141 | 29.5 [23.6, 36.2] | 29.5 [23.6, 36.2] | -0.01534 [-0.01990, -0.01079] | 0 of 200 |
| review_first | two_term | skills learned | 110 / 7 / 83 | 58.5 [51.6, 65.1] | 55.0 [48.1, 61.7] | +4.81500 [2.48195, 7.14805] | 0 of 200 |
| review_first | random_control | mastery per item | 45 / 0 / 155 | 22.5 [17.3, 28.8] | 22.5 [17.3, 28.8] | -0.00316 [-0.00379, -0.00253] | 0 of 200 |
| review_first | random_control | delayed mastery per item | 81 / 0 / 119 | 40.5 [33.9, 47.4] | 40.5 [33.9, 47.4] | -0.00120 [-0.00175, -0.00065] | 0 of 200 |
| review_first | random_control | retention day 30 | 45 / 0 / 155 | 22.5 [17.3, 28.8] | 22.5 [17.3, 28.8] | -0.02470 [-0.02958, -0.01983] | 0 of 200 |
| review_first | random_control | skills learned | 70 / 8 / 122 | 39.0 [32.5, 45.9] | 35.0 [28.7, 41.8] | -4.81500 [-7.11131, -2.51869] | 0 of 200 |

## World fixed, power law forgetting, 226 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 2914 | 116.5 | 146.6 | 0.03147 [0.03061, 0.03232] | 0.02398 [0.02326, 0.02470] | 0.6721 |
| random_control | 200 | 2916 | 125.1 | 156.1 | 0.03452 [0.03359, 0.03544] | 0.02515 [0.02438, 0.02592] | 0.6805 |
| oracle_forgetting | 200 | 2915 | 86.0 | 131.9 | 0.02576 [0.02492, 0.02660] | 0.02055 [0.01979, 0.02130] | 0.7084 |
| retrievability_priority | 200 | 2908 | 70.8 | 116.9 | 0.02105 [0.02023, 0.02187] | 0.01727 [0.01652, 0.01801] | 0.6850 |
| retrievability_priority_both | 200 | 2908 | 71.5 | 123.6 | 0.02077 [0.01993, 0.02161] | 0.01714 [0.01637, 0.01791] | 0.6746 |
| elo_target | 200 | 2904 | 104.9 | 147.4 | 0.02664 [0.02580, 0.02748] | 0.02184 [0.02114, 0.02255] | 0.6694 |
| spread | 200 | 2916 | 102.1 | 150.3 | 0.02989 [0.02901, 0.03077] | 0.02417 [0.02336, 0.02498] | 0.6979 |
| review_first | 200 | 2914 | 119.6 | 148.7 | 0.03134 [0.03044, 0.03223] | 0.02385 [0.02309, 0.02460] | 0.6536 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| oracle_forgetting | two_term | mastery per item | 24 / 0 / 176 | 12.0 [8.2, 17.2] | 12.0 [8.2, 17.2] | -0.00571 [-0.00646, -0.00495] | 0 of 200 |
| oracle_forgetting | two_term | delayed mastery per item | 47 / 0 / 153 | 23.5 [18.2, 29.8] | 23.5 [18.2, 29.8] | -0.00343 [-0.00409, -0.00277] | 0 of 200 |
| oracle_forgetting | two_term | retention day 30 | 174 / 0 / 26 | 87.0 [81.6, 91.0] | 87.0 [81.6, 91.0] | +0.03630 [0.03174, 0.04085] | 0 of 200 |
| oracle_forgetting | two_term | skills learned | 13 / 0 / 187 | 6.5 [3.8, 10.8] | 6.5 [3.8, 10.8] | -30.55000 [-33.42301, -27.67699] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 7 / 0 / 193 | 3.5 [1.7, 7.0] | 3.5 [1.7, 7.0] | -0.00876 [-0.00955, -0.00796] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 36 / 0 / 164 | 18.0 [13.3, 23.9] | 18.0 [13.3, 23.9] | -0.00460 [-0.00528, -0.00393] | 0 of 200 |
| oracle_forgetting | random_control | retention day 30 | 154 / 0 / 46 | 77.0 [70.7, 82.3] | 77.0 [70.7, 82.3] | +0.02787 [0.02314, 0.03260] | 0 of 200 |
| oracle_forgetting | random_control | skills learned | 6 / 0 / 194 | 3.0 [1.4, 6.4] | 3.0 [1.4, 6.4] | -39.06000 [-41.92072, -36.19928] | 0 of 200 |
| retrievability_priority | two_term | mastery per item | 5 / 0 / 195 | 2.5 [1.1, 5.7] | 2.5 [1.1, 5.7] | -0.01041 [-0.01115, -0.00967] | 0 of 200 |
| retrievability_priority | two_term | delayed mastery per item | 19 / 0 / 181 | 9.5 [6.2, 14.4] | 9.5 [6.2, 14.4] | -0.00671 [-0.00736, -0.00607] | 0 of 200 |
| retrievability_priority | two_term | retention day 30 | 130 / 0 / 70 | 65.0 [58.2, 71.3] | 65.0 [58.2, 71.3] | +0.01283 [0.00834, 0.01733] | 0 of 200 |
| retrievability_priority | two_term | skills learned | 3 / 0 / 197 | 1.5 [0.5, 4.3] | 1.5 [0.5, 4.3] | -45.77500 [-48.63807, -42.91193] | 0 of 200 |
| retrievability_priority | random_control | mastery per item | 1 / 0 / 199 | 0.5 [0.1, 2.8] | 0.5 [0.1, 2.8] | -0.01346 [-0.01420, -0.01273] | 0 of 200 |
| retrievability_priority | random_control | delayed mastery per item | 8 / 0 / 192 | 4.0 [2.0, 7.7] | 4.0 [2.0, 7.7] | -0.00788 [-0.00851, -0.00726] | 0 of 200 |
| retrievability_priority | random_control | retention day 30 | 110 / 0 / 90 | 55.0 [48.1, 61.7] | 55.0 [48.1, 61.7] | +0.00441 [-0.00051, 0.00932] | 0 of 200 |
| retrievability_priority | random_control | skills learned | 0 / 0 / 200 | 0.0 [0.0, 1.9] | 0.0 [0.0, 1.9] | -54.28500 [-57.07537, -51.49463] | 0 of 200 |
| retrievability_priority_both | two_term | mastery per item | 10 / 0 / 190 | 5.0 [2.7, 9.0] | 5.0 [2.7, 9.0] | -0.01070 [-0.01153, -0.00987] | 0 of 200 |
| retrievability_priority_both | two_term | delayed mastery per item | 18 / 0 / 182 | 9.0 [5.8, 13.8] | 9.0 [5.8, 13.8] | -0.00684 [-0.00754, -0.00615] | 0 of 200 |
| retrievability_priority_both | two_term | retention day 30 | 103 / 0 / 97 | 51.5 [44.6, 58.3] | 51.5 [44.6, 58.3] | +0.00244 [-0.00203, 0.00691] | 0 of 200 |
| retrievability_priority_both | two_term | skills learned | 4 / 1 / 195 | 2.5 [1.1, 5.7] | 2.0 [0.8, 5.0] | -45.08000 [-48.18200, -41.97800] | 0 of 200 |
| retrievability_priority_both | random_control | mastery per item | 2 / 0 / 198 | 1.0 [0.3, 3.6] | 1.0 [0.3, 3.6] | -0.01375 [-0.01452, -0.01298] | 0 of 200 |
| retrievability_priority_both | random_control | delayed mastery per item | 8 / 0 / 192 | 4.0 [2.0, 7.7] | 4.0 [2.0, 7.7] | -0.00801 [-0.00865, -0.00738] | 0 of 200 |
| retrievability_priority_both | random_control | retention day 30 | 82 / 0 / 118 | 41.0 [34.4, 47.9] | 41.0 [34.4, 47.9] | -0.00599 [-0.01089, -0.00108] | 0 of 200 |
| retrievability_priority_both | random_control | skills learned | 0 / 0 / 200 | 0.0 [0.0, 1.9] | 0.0 [0.0, 1.9] | -53.59000 [-56.45488, -50.72512] | 0 of 200 |
| elo_target | two_term | mastery per item | 35 / 0 / 165 | 17.5 [12.9, 23.4] | 17.5 [12.9, 23.4] | -0.00482 [-0.00551, -0.00414] | 0 of 200 |
| elo_target | two_term | delayed mastery per item | 61 / 0 / 139 | 30.5 [24.5, 37.2] | 30.5 [24.5, 37.2] | -0.00213 [-0.00271, -0.00156] | 0 of 200 |
| elo_target | two_term | retention day 30 | 89 / 0 / 111 | 44.5 [37.8, 51.4] | 44.5 [37.8, 51.4] | -0.00271 [-0.00641, 0.00099] | 0 of 200 |
| elo_target | two_term | skills learned | 54 / 3 / 143 | 28.5 [22.7, 35.1] | 27.0 [21.3, 33.5] | -11.64000 [-14.38527, -8.89473] | 0 of 200 |
| elo_target | random_control | mastery per item | 9 / 0 / 191 | 4.5 [2.4, 8.3] | 4.5 [2.4, 8.3] | -0.00787 [-0.00858, -0.00717] | 0 of 200 |
| elo_target | random_control | delayed mastery per item | 42 / 0 / 158 | 21.0 [15.9, 27.2] | 21.0 [15.9, 27.2] | -0.00331 [-0.00391, -0.00270] | 0 of 200 |
| elo_target | random_control | retention day 30 | 70 / 0 / 130 | 35.0 [28.7, 41.8] | 35.0 [28.7, 41.8] | -0.01114 [-0.01543, -0.00684] | 0 of 200 |
| elo_target | random_control | skills learned | 24 / 3 / 173 | 13.5 [9.4, 18.9] | 12.0 [8.2, 17.2] | -20.15000 [-23.00352, -17.29648] | 0 of 200 |
| spread | two_term | mastery per item | 78 / 0 / 122 | 39.0 [32.5, 45.9] | 39.0 [32.5, 45.9] | -0.00157 [-0.00221, -0.00094] | 0 of 200 |
| spread | two_term | delayed mastery per item | 100 / 0 / 100 | 50.0 [43.1, 56.9] | 50.0 [43.1, 56.9] | +0.00019 [-0.00037, 0.00075] | 0 of 200 |
| spread | two_term | retention day 30 | 164 / 0 / 36 | 82.0 [76.1, 86.7] | 82.0 [76.1, 86.7] | +0.02580 [0.02194, 0.02967] | 0 of 200 |
| spread | two_term | skills learned | 37 / 3 / 160 | 20.0 [15.0, 26.1] | 18.5 [13.7, 24.5] | -14.48500 [-16.95224, -12.01776] | 0 of 200 |
| spread | random_control | mastery per item | 24 / 0 / 176 | 12.0 [8.2, 17.2] | 12.0 [8.2, 17.2] | -0.00463 [-0.00523, -0.00403] | 0 of 200 |
| spread | random_control | delayed mastery per item | 76 / 0 / 124 | 38.0 [31.6, 44.9] | 38.0 [31.6, 44.9] | -0.00098 [-0.00150, -0.00047] | 0 of 200 |
| spread | random_control | retention day 30 | 141 / 0 / 59 | 70.5 [63.8, 76.4] | 70.5 [63.8, 76.4] | +0.01738 [0.01315, 0.02160] | 0 of 200 |
| spread | random_control | skills learned | 14 / 1 / 185 | 7.5 [4.6, 12.0] | 7.0 [4.2, 11.4] | -22.99500 [-25.26027, -20.72973] | 0 of 200 |
| review_first | two_term | mastery per item | 99 / 0 / 101 | 49.5 [42.6, 56.4] | 49.5 [42.6, 56.4] | -0.00013 [-0.00069, 0.00043] | 0 of 200 |
| review_first | two_term | delayed mastery per item | 101 / 0 / 99 | 50.5 [43.6, 57.4] | 50.5 [43.6, 57.4] | -0.00013 [-0.00060, 0.00034] | 0 of 200 |
| review_first | two_term | retention day 30 | 42 / 0 / 158 | 21.0 [15.9, 27.2] | 21.0 [15.9, 27.2] | -0.01853 [-0.02236, -0.01470] | 0 of 200 |
| review_first | two_term | skills learned | 114 / 7 / 79 | 60.5 [53.6, 67.0] | 57.0 [50.1, 63.7] | +3.08000 [0.83529, 5.32471] | 0 of 200 |
| review_first | random_control | mastery per item | 45 / 0 / 155 | 22.5 [17.3, 28.8] | 22.5 [17.3, 28.8] | -0.00318 [-0.00373, -0.00264] | 0 of 200 |
| review_first | random_control | delayed mastery per item | 73 / 0 / 127 | 36.5 [30.1, 43.4] | 36.5 [30.1, 43.4] | -0.00130 [-0.00175, -0.00086] | 0 of 200 |
| review_first | random_control | retention day 30 | 27 / 0 / 173 | 13.5 [9.4, 18.9] | 13.5 [9.4, 18.9] | -0.02696 [-0.03066, -0.02325] | 0 of 200 |
| review_first | random_control | skills learned | 70 / 11 / 119 | 40.5 [33.9, 47.4] | 35.0 [28.7, 41.8] | -5.43000 [-7.66796, -3.19204] | 0 of 200 |

## World legacy, exponential forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 753 | 32.1 | 38.1 | 0.02062 [0.01943, 0.02181] | 0.01625 [0.01525, 0.01726] | 0.8622 |
| random_control | 200 | 756 | 34.4 | 39.9 | 0.02143 [0.02030, 0.02256] | 0.01663 [0.01568, 0.01758] | 0.8506 |
| oracle_forgetting | 200 | 752 | 24.0 | 41.8 | 0.02136 [0.02018, 0.02254] | 0.01840 [0.01734, 0.01946] | 0.9273 |
| retrievability_priority | 200 | 748 | 24.6 | 37.4 | 0.02083 [0.01955, 0.02212] | 0.01801 [0.01685, 0.01916] | 0.9201 |
| retrievability_priority_both | 200 | 748 | 24.9 | 38.3 | 0.02106 [0.01981, 0.02231] | 0.01832 [0.01720, 0.01943] | 0.9197 |
| elo_target | 200 | 744 | 28.0 | 37.2 | 0.01730 [0.01644, 0.01815] | 0.01389 [0.01314, 0.01465] | 0.8863 |
| spread | 200 | 756 | 32.0 | 39.4 | 0.02125 [0.02015, 0.02236] | 0.01699 [0.01608, 0.01790] | 0.8717 |
| review_first | 200 | 753 | 33.1 | 39.9 | 0.02203 [0.02080, 0.02327] | 0.01748 [0.01646, 0.01850] | 0.8598 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| oracle_forgetting | two_term | mastery per item | 109 / 0 / 91 | 54.5 [47.6, 61.3] | 54.5 [47.6, 61.3] | +0.00075 [-0.00055, 0.00204] | 0 of 200 |
| oracle_forgetting | two_term | delayed mastery per item | 123 / 0 / 77 | 61.5 [54.6, 68.0] | 61.5 [54.6, 68.0] | +0.00215 [0.00104, 0.00325] | 0 of 200 |
| oracle_forgetting | two_term | retention day 30 | 193 / 0 / 7 | 96.5 [93.0, 98.3] | 96.5 [93.0, 98.3] | +0.06514 [0.05966, 0.07062] | 0 of 200 |
| oracle_forgetting | two_term | skills learned | 20 / 9 / 171 | 14.5 [10.3, 20.0] | 10.0 [6.6, 14.9] | -8.16000 [-9.27555, -7.04445] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 97 / 0 / 103 | 48.5 [41.7, 55.4] | 48.5 [41.7, 55.4] | -0.00006 [-0.00134, 0.00121] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 112 / 0 / 88 | 56.0 [49.1, 62.7] | 56.0 [49.1, 62.7] | +0.00177 [0.00068, 0.00285] | 0 of 200 |
| oracle_forgetting | random_control | retention day 30 | 199 / 0 / 1 | 99.5 [97.2, 99.9] | 99.5 [97.2, 99.9] | +0.07672 [0.07096, 0.08247] | 0 of 200 |
| oracle_forgetting | random_control | skills learned | 18 / 7 / 175 | 12.5 [8.6, 17.8] | 9.0 [5.8, 13.8] | -10.47500 [-11.66738, -9.28262] | 0 of 200 |
| retrievability_priority | two_term | mastery per item | 104 / 0 / 96 | 52.0 [45.1, 58.8] | 52.0 [45.1, 58.8] | +0.00022 [-0.00116, 0.00160] | 0 of 200 |
| retrievability_priority | two_term | delayed mastery per item | 119 / 0 / 81 | 59.5 [52.6, 66.1] | 59.5 [52.6, 66.1] | +0.00176 [0.00057, 0.00295] | 0 of 200 |
| retrievability_priority | two_term | retention day 30 | 189 / 0 / 11 | 94.5 [90.4, 96.9] | 94.5 [90.4, 96.9] | +0.05793 [0.05221, 0.06365] | 0 of 200 |
| retrievability_priority | two_term | skills learned | 32 / 9 / 159 | 20.5 [15.5, 26.6] | 16.0 [11.6, 21.7] | -7.47500 [-8.63771, -6.31229] | 0 of 200 |
| retrievability_priority | random_control | mastery per item | 87 / 0 / 113 | 43.5 [36.8, 50.4] | 43.5 [36.8, 50.4] | -0.00059 [-0.00190, 0.00071] | 0 of 200 |
| retrievability_priority | random_control | delayed mastery per item | 105 / 0 / 95 | 52.5 [45.6, 59.3] | 52.5 [45.6, 59.3] | +0.00138 [0.00024, 0.00251] | 0 of 200 |
| retrievability_priority | random_control | retention day 30 | 194 / 0 / 6 | 97.0 [93.6, 98.6] | 97.0 [93.6, 98.6] | +0.06951 [0.06377, 0.07525] | 0 of 200 |
| retrievability_priority | random_control | skills learned | 18 / 6 / 176 | 12.0 [8.2, 17.2] | 9.0 [5.8, 13.8] | -9.79000 [-10.95905, -8.62095] | 0 of 200 |
| retrievability_priority_both | two_term | mastery per item | 110 / 0 / 90 | 55.0 [48.1, 61.7] | 55.0 [48.1, 61.7] | +0.00045 [-0.00091, 0.00180] | 0 of 200 |
| retrievability_priority_both | two_term | delayed mastery per item | 126 / 0 / 74 | 63.0 [56.1, 69.4] | 63.0 [56.1, 69.4] | +0.00206 [0.00089, 0.00323] | 0 of 200 |
| retrievability_priority_both | two_term | retention day 30 | 186 / 0 / 14 | 93.0 [88.6, 95.8] | 93.0 [88.6, 95.8] | +0.05752 [0.05196, 0.06308] | 0 of 200 |
| retrievability_priority_both | two_term | skills learned | 38 / 7 / 155 | 22.5 [17.3, 28.8] | 19.0 [14.2, 25.0] | -7.18500 [-8.33989, -6.03011] | 0 of 200 |
| retrievability_priority_both | random_control | mastery per item | 97 / 0 / 103 | 48.5 [41.7, 55.4] | 48.5 [41.7, 55.4] | -0.00036 [-0.00163, 0.00091] | 0 of 200 |
| retrievability_priority_both | random_control | delayed mastery per item | 116 / 0 / 84 | 58.0 [51.1, 64.6] | 58.0 [51.1, 64.6] | +0.00168 [0.00058, 0.00278] | 0 of 200 |
| retrievability_priority_both | random_control | retention day 30 | 191 / 0 / 9 | 95.5 [91.7, 97.6] | 95.5 [91.7, 97.6] | +0.06910 [0.06336, 0.07484] | 0 of 200 |
| retrievability_priority_both | random_control | skills learned | 25 / 4 / 171 | 14.5 [10.3, 20.0] | 12.5 [8.6, 17.8] | -9.50000 [-10.69699, -8.30301] | 0 of 200 |
| elo_target | two_term | mastery per item | 73 / 0 / 127 | 36.5 [30.1, 43.4] | 36.5 [30.1, 43.4] | -0.00332 [-0.00447, -0.00217] | 0 of 200 |
| elo_target | two_term | delayed mastery per item | 74 / 0 / 126 | 37.0 [30.6, 43.9] | 37.0 [30.6, 43.9] | -0.00236 [-0.00330, -0.00142] | 0 of 200 |
| elo_target | two_term | retention day 30 | 153 / 0 / 47 | 76.5 [70.2, 81.8] | 76.5 [70.2, 81.8] | +0.02405 [0.01850, 0.02960] | 0 of 200 |
| elo_target | two_term | skills learned | 51 / 10 / 139 | 30.5 [24.5, 37.2] | 25.5 [20.0, 32.0] | -4.12000 [-5.25978, -2.98022] | 0 of 200 |
| elo_target | random_control | mastery per item | 59 / 0 / 141 | 29.5 [23.6, 36.2] | 29.5 [23.6, 36.2] | -0.00413 [-0.00521, -0.00305] | 0 of 200 |
| elo_target | random_control | delayed mastery per item | 60 / 0 / 140 | 30.0 [24.1, 36.7] | 30.0 [24.1, 36.7] | -0.00274 [-0.00363, -0.00185] | 0 of 200 |
| elo_target | random_control | retention day 30 | 163 / 0 / 37 | 81.5 [75.5, 86.3] | 81.5 [75.5, 86.3] | +0.03563 [0.02983, 0.04142] | 0 of 200 |
| elo_target | random_control | skills learned | 38 / 7 / 155 | 22.5 [17.3, 28.8] | 19.0 [14.2, 25.0] | -6.43500 [-7.62678, -5.24322] | 0 of 200 |
| spread | two_term | mastery per item | 116 / 0 / 84 | 58.0 [51.1, 64.6] | 58.0 [51.1, 64.6] | +0.00063 [-0.00065, 0.00192] | 0 of 200 |
| spread | two_term | delayed mastery per item | 120 / 0 / 80 | 60.0 [53.1, 66.5] | 60.0 [53.1, 66.5] | +0.00074 [-0.00034, 0.00181] | 0 of 200 |
| spread | two_term | retention day 30 | 110 / 0 / 90 | 55.0 [48.1, 61.7] | 55.0 [48.1, 61.7] | +0.00947 [0.00375, 0.01519] | 0 of 200 |
| spread | two_term | skills learned | 99 / 14 / 87 | 56.5 [49.6, 63.2] | 49.5 [42.6, 56.4] | -0.16500 [-1.29006, 0.96006] | 0 of 200 |
| spread | random_control | mastery per item | 102 / 0 / 98 | 51.0 [44.1, 57.8] | 51.0 [44.1, 57.8] | -0.00018 [-0.00132, 0.00097] | 0 of 200 |
| spread | random_control | delayed mastery per item | 108 / 0 / 92 | 54.0 [47.1, 60.8] | 54.0 [47.1, 60.8] | +0.00036 [-0.00059, 0.00130] | 0 of 200 |
| spread | random_control | retention day 30 | 139 / 0 / 61 | 69.5 [62.8, 75.5] | 69.5 [62.8, 75.5] | +0.02105 [0.01561, 0.02649] | 0 of 200 |
| spread | random_control | skills learned | 74 / 12 / 114 | 43.0 [36.3, 49.9] | 37.0 [30.6, 43.9] | -2.48000 [-3.60052, -1.35948] | 0 of 200 |
| review_first | two_term | mastery per item | 111 / 0 / 89 | 55.5 [48.6, 62.2] | 55.5 [48.6, 62.2] | +0.00142 [0.00036, 0.00247] | 0 of 200 |
| review_first | two_term | delayed mastery per item | 117 / 0 / 83 | 58.5 [51.6, 65.1] | 58.5 [51.6, 65.1] | +0.00123 [0.00035, 0.00211] | 0 of 200 |
| review_first | two_term | retention day 30 | 97 / 0 / 103 | 48.5 [41.7, 55.4] | 48.5 [41.7, 55.4] | -0.00240 [-0.00711, 0.00230] | 0 of 200 |
| review_first | two_term | skills learned | 104 / 21 / 75 | 62.5 [55.6, 68.9] | 52.0 [45.1, 58.8] | +0.96500 [0.18838, 1.74162] | 0 of 200 |
| review_first | random_control | mastery per item | 105 / 0 / 95 | 52.5 [45.6, 59.3] | 52.5 [45.6, 59.3] | +0.00061 [-0.00046, 0.00167] | 0 of 200 |
| review_first | random_control | delayed mastery per item | 109 / 0 / 91 | 54.5 [47.6, 61.3] | 54.5 [47.6, 61.3] | +0.00085 [-0.00005, 0.00174] | 0 of 200 |
| review_first | random_control | retention day 30 | 119 / 0 / 81 | 59.5 [52.6, 66.1] | 59.5 [52.6, 66.1] | +0.00918 [0.00395, 0.01440] | 0 of 200 |
| review_first | random_control | skills learned | 76 / 17 / 107 | 46.5 [39.7, 53.4] | 38.0 [31.6, 44.9] | -1.35000 [-2.26234, -0.43766] | 0 of 200 |

## World legacy, power law forgetting, 60 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 751 | 31.8 | 37.4 | 0.02418 [0.02279, 0.02556] | 0.01917 [0.01801, 0.02033] | 0.8704 |
| random_control | 200 | 754 | 34.3 | 39.1 | 0.02527 [0.02402, 0.02651] | 0.01969 [0.01866, 0.02073] | 0.8571 |
| oracle_forgetting | 200 | 751 | 23.5 | 41.1 | 0.02289 [0.02167, 0.02410] | 0.01958 [0.01848, 0.02068] | 0.9315 |
| retrievability_priority | 200 | 746 | 24.6 | 37.2 | 0.02301 [0.02175, 0.02427] | 0.01953 [0.01843, 0.02063] | 0.9227 |
| retrievability_priority_both | 200 | 746 | 25.4 | 38.5 | 0.02398 [0.02272, 0.02525] | 0.02043 [0.01932, 0.02155] | 0.9236 |
| elo_target | 200 | 744 | 28.1 | 37.4 | 0.02058 [0.01959, 0.02158] | 0.01640 [0.01557, 0.01724] | 0.8904 |
| spread | 200 | 754 | 31.3 | 37.4 | 0.02385 [0.02259, 0.02511] | 0.01890 [0.01785, 0.01995] | 0.8735 |
| review_first | 200 | 751 | 32.6 | 39.1 | 0.02504 [0.02369, 0.02638] | 0.01975 [0.01862, 0.02087] | 0.8673 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| oracle_forgetting | two_term | mastery per item | 84 / 0 / 116 | 42.0 [35.4, 48.9] | 42.0 [35.4, 48.9] | -0.00129 [-0.00248, -0.00010] | 0 of 200 |
| oracle_forgetting | two_term | delayed mastery per item | 107 / 0 / 93 | 53.5 [46.6, 60.3] | 53.5 [46.6, 60.3] | +0.00041 [-0.00066, 0.00147] | 0 of 200 |
| oracle_forgetting | two_term | retention day 30 | 194 / 0 / 6 | 97.0 [93.6, 98.6] | 97.0 [93.6, 98.6] | +0.06112 [0.05623, 0.06601] | 0 of 200 |
| oracle_forgetting | two_term | skills learned | 21 / 8 / 171 | 14.5 [10.3, 20.0] | 10.5 [7.0, 15.5] | -8.30500 [-9.37251, -7.23749] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 72 / 0 / 128 | 36.0 [29.7, 42.9] | 36.0 [29.7, 42.9] | -0.00238 [-0.00346, -0.00130] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 89 / 0 / 111 | 44.5 [37.8, 51.4] | 44.5 [37.8, 51.4] | -0.00011 [-0.00105, 0.00082] | 0 of 200 |
| oracle_forgetting | random_control | retention day 30 | 198 / 0 / 2 | 99.0 [96.4, 99.7] | 99.0 [96.4, 99.7] | +0.07442 [0.06974, 0.07910] | 0 of 200 |
| oracle_forgetting | random_control | skills learned | 9 / 6 / 185 | 7.5 [4.6, 12.0] | 4.5 [2.4, 8.3] | -10.76500 [-11.86903, -9.66097] | 0 of 200 |
| retrievability_priority | two_term | mastery per item | 91 / 0 / 109 | 45.5 [38.7, 52.4] | 45.5 [38.7, 52.4] | -0.00117 [-0.00252, 0.00019] | 0 of 200 |
| retrievability_priority | two_term | delayed mastery per item | 108 / 0 / 92 | 54.0 [47.1, 60.8] | 54.0 [47.1, 60.8] | +0.00036 [-0.00081, 0.00153] | 0 of 200 |
| retrievability_priority | two_term | retention day 30 | 187 / 0 / 13 | 93.5 [89.2, 96.2] | 93.5 [89.2, 96.2] | +0.05226 [0.04762, 0.05690] | 0 of 200 |
| retrievability_priority | two_term | skills learned | 35 / 6 / 159 | 20.5 [15.5, 26.6] | 17.5 [12.9, 23.4] | -7.20500 [-8.33259, -6.07741] | 0 of 200 |
| retrievability_priority | random_control | mastery per item | 78 / 0 / 122 | 39.0 [32.5, 45.9] | 39.0 [32.5, 45.9] | -0.00226 [-0.00343, -0.00109] | 0 of 200 |
| retrievability_priority | random_control | delayed mastery per item | 102 / 0 / 98 | 51.0 [44.1, 57.8] | 51.0 [44.1, 57.8] | -0.00016 [-0.00117, 0.00085] | 0 of 200 |
| retrievability_priority | random_control | retention day 30 | 196 / 0 / 4 | 98.0 [95.0, 99.2] | 98.0 [95.0, 99.2] | +0.06556 [0.06105, 0.07007] | 0 of 200 |
| retrievability_priority | random_control | skills learned | 18 / 4 / 178 | 11.0 [7.4, 16.1] | 9.0 [5.8, 13.8] | -9.66500 [-10.79173, -8.53827] | 0 of 200 |
| retrievability_priority_both | two_term | mastery per item | 110 / 0 / 90 | 55.0 [48.1, 61.7] | 55.0 [48.1, 61.7] | -0.00019 [-0.00165, 0.00126] | 0 of 200 |
| retrievability_priority_both | two_term | delayed mastery per item | 121 / 0 / 79 | 60.5 [53.6, 67.0] | 60.5 [53.6, 67.0] | +0.00126 [0.00001, 0.00252] | 0 of 200 |
| retrievability_priority_both | two_term | retention day 30 | 194 / 0 / 6 | 97.0 [93.6, 98.6] | 97.0 [93.6, 98.6] | +0.05316 [0.04842, 0.05790] | 0 of 200 |
| retrievability_priority_both | two_term | skills learned | 41 / 9 / 150 | 25.0 [19.5, 31.4] | 20.5 [15.5, 26.6] | -6.43000 [-7.61748, -5.24252] | 0 of 200 |
| retrievability_priority_both | random_control | mastery per item | 98 / 0 / 102 | 49.0 [42.2, 55.9] | 49.0 [42.2, 55.9] | -0.00129 [-0.00257, -0.00000] | 0 of 200 |
| retrievability_priority_both | random_control | delayed mastery per item | 111 / 0 / 89 | 55.5 [48.6, 62.2] | 55.5 [48.6, 62.2] | +0.00074 [-0.00037, 0.00185] | 0 of 200 |
| retrievability_priority_both | random_control | retention day 30 | 200 / 0 / 0 | 100.0 [98.1, 100.0] | 100.0 [98.1, 100.0] | +0.06646 [0.06187, 0.07105] | 0 of 200 |
| retrievability_priority_both | random_control | skills learned | 27 / 4 / 169 | 15.5 [11.1, 21.2] | 13.5 [9.4, 18.9] | -8.89000 [-10.07286, -7.70714] | 0 of 200 |
| elo_target | two_term | mastery per item | 67 / 0 / 133 | 33.5 [27.3, 40.3] | 33.5 [27.3, 40.3] | -0.00359 [-0.00469, -0.00250] | 0 of 200 |
| elo_target | two_term | delayed mastery per item | 70 / 0 / 130 | 35.0 [28.7, 41.8] | 35.0 [28.7, 41.8] | -0.00277 [-0.00366, -0.00187] | 0 of 200 |
| elo_target | two_term | retention day 30 | 142 / 0 / 58 | 71.0 [64.4, 76.8] | 71.0 [64.4, 76.8] | +0.01995 [0.01482, 0.02507] | 0 of 200 |
| elo_target | two_term | skills learned | 61 / 13 / 126 | 37.0 [30.6, 43.9] | 30.5 [24.5, 37.2] | -3.72500 [-4.85273, -2.59727] | 0 of 200 |
| elo_target | random_control | mastery per item | 51 / 0 / 149 | 25.5 [20.0, 32.0] | 25.5 [20.0, 32.0] | -0.00468 [-0.00573, -0.00364] | 0 of 200 |
| elo_target | random_control | delayed mastery per item | 56 / 0 / 144 | 28.0 [22.2, 34.6] | 28.0 [22.2, 34.6] | -0.00329 [-0.00412, -0.00245] | 0 of 200 |
| elo_target | random_control | retention day 30 | 167 / 0 / 33 | 83.5 [77.7, 88.0] | 83.5 [77.7, 88.0] | +0.03325 [0.02836, 0.03814] | 0 of 200 |
| elo_target | random_control | skills learned | 41 / 12 / 147 | 26.5 [20.9, 33.0] | 20.5 [15.5, 26.6] | -6.18500 [-7.35624, -5.01376] | 0 of 200 |
| spread | two_term | mastery per item | 92 / 0 / 108 | 46.0 [39.2, 52.9] | 46.0 [39.2, 52.9] | -0.00033 [-0.00161, 0.00095] | 0 of 200 |
| spread | two_term | delayed mastery per item | 97 / 0 / 103 | 48.5 [41.7, 55.4] | 48.5 [41.7, 55.4] | -0.00027 [-0.00133, 0.00079] | 0 of 200 |
| spread | two_term | retention day 30 | 100 / 0 / 100 | 50.0 [43.1, 56.9] | 50.0 [43.1, 56.9] | +0.00305 [-0.00190, 0.00801] | 0 of 200 |
| spread | two_term | skills learned | 93 / 14 / 93 | 53.5 [46.6, 60.3] | 46.5 [39.7, 53.4] | -0.50500 [-1.64643, 0.63643] | 0 of 200 |
| spread | random_control | mastery per item | 87 / 0 / 113 | 43.5 [36.8, 50.4] | 43.5 [36.8, 50.4] | -0.00142 [-0.00262, -0.00023] | 0 of 200 |
| spread | random_control | delayed mastery per item | 90 / 0 / 110 | 45.0 [38.3, 51.9] | 45.0 [38.3, 51.9] | -0.00079 [-0.00180, 0.00022] | 0 of 200 |
| spread | random_control | retention day 30 | 135 / 0 / 65 | 67.5 [60.7, 73.6] | 67.5 [60.7, 73.6] | +0.01635 [0.01134, 0.02137] | 0 of 200 |
| spread | random_control | skills learned | 67 / 13 / 120 | 40.0 [33.5, 46.9] | 33.5 [27.3, 40.3] | -2.96500 [-4.06187, -1.86813] | 0 of 200 |
| review_first | two_term | mastery per item | 118 / 0 / 82 | 59.0 [52.1, 65.6] | 59.0 [52.1, 65.6] | +0.00086 [-0.00015, 0.00188] | 0 of 200 |
| review_first | two_term | delayed mastery per item | 113 / 0 / 87 | 56.5 [49.6, 63.2] | 56.5 [49.6, 63.2] | +0.00058 [-0.00029, 0.00144] | 0 of 200 |
| review_first | two_term | retention day 30 | 93 / 0 / 107 | 46.5 [39.7, 53.4] | 46.5 [39.7, 53.4] | -0.00313 [-0.00774, 0.00147] | 0 of 200 |
| review_first | two_term | skills learned | 109 / 13 / 78 | 61.0 [54.1, 67.5] | 54.5 [47.6, 61.3] | +0.75500 [-0.07882, 1.58882] | 0 of 200 |
| review_first | random_control | mastery per item | 105 / 0 / 95 | 52.5 [45.6, 59.3] | 52.5 [45.6, 59.3] | -0.00023 [-0.00134, 0.00088] | 0 of 200 |
| review_first | random_control | delayed mastery per item | 102 / 0 / 98 | 51.0 [44.1, 57.8] | 51.0 [44.1, 57.8] | +0.00005 [-0.00086, 0.00096] | 0 of 200 |
| review_first | random_control | retention day 30 | 133 / 0 / 67 | 66.5 [59.7, 72.7] | 66.5 [59.7, 72.7] | +0.01016 [0.00542, 0.01491] | 0 of 200 |
| review_first | random_control | skills learned | 74 / 12 / 114 | 43.0 [36.3, 49.9] | 37.0 [30.6, 43.9] | -1.70500 [-2.63245, -0.77755] | 0 of 200 |

## World legacy, exponential forgetting, 226 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 2910 | 58.8 | 58.9 | 0.00612 [0.00575, 0.00649] | 0.00568 [0.00534, 0.00602] | 0.7655 |
| random_control | 200 | 2914 | 63.2 | 60.7 | 0.00626 [0.00589, 0.00662] | 0.00580 [0.00546, 0.00614] | 0.7540 |
| oracle_forgetting | 200 | 2909 | 43.7 | 71.6 | 0.00776 [0.00729, 0.00823] | 0.00723 [0.00679, 0.00767] | 0.8591 |
| retrievability_priority | 200 | 2904 | 44.0 | 64.6 | 0.00767 [0.00715, 0.00820] | 0.00713 [0.00664, 0.00762] | 0.8590 |
| retrievability_priority_both | 200 | 2904 | 40.7 | 61.6 | 0.00672 [0.00627, 0.00718] | 0.00631 [0.00588, 0.00673] | 0.8541 |
| elo_target | 200 | 2901 | 61.8 | 67.8 | 0.00676 [0.00636, 0.00716] | 0.00626 [0.00589, 0.00662] | 0.7862 |
| spread | 200 | 2914 | 53.2 | 61.9 | 0.00656 [0.00618, 0.00694] | 0.00609 [0.00574, 0.00644] | 0.7979 |
| review_first | 200 | 2910 | 61.0 | 59.7 | 0.00600 [0.00565, 0.00634] | 0.00557 [0.00525, 0.00589] | 0.7447 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| oracle_forgetting | two_term | mastery per item | 137 / 0 / 63 | 68.5 [61.8, 74.5] | 68.5 [61.8, 74.5] | +0.00164 [0.00114, 0.00214] | 0 of 200 |
| oracle_forgetting | two_term | delayed mastery per item | 137 / 0 / 63 | 68.5 [61.8, 74.5] | 68.5 [61.8, 74.5] | +0.00155 [0.00109, 0.00201] | 0 of 200 |
| oracle_forgetting | two_term | retention day 30 | 179 / 0 / 21 | 89.5 [84.5, 93.0] | 89.5 [84.5, 93.0] | +0.09355 [0.08484, 0.10226] | 0 of 200 |
| oracle_forgetting | two_term | skills learned | 44 / 6 / 150 | 25.0 [19.5, 31.4] | 22.0 [16.8, 28.2] | -15.01500 [-17.96946, -12.06054] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 131 / 0 / 69 | 65.5 [58.7, 71.7] | 65.5 [58.7, 71.7] | +0.00150 [0.00103, 0.00198] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 134 / 0 / 66 | 67.0 [60.2, 73.1] | 67.0 [60.2, 73.1] | +0.00143 [0.00099, 0.00187] | 0 of 200 |
| oracle_forgetting | random_control | retention day 30 | 183 / 0 / 17 | 91.5 [86.8, 94.6] | 91.5 [86.8, 94.6] | +0.10512 [0.09540, 0.11485] | 0 of 200 |
| oracle_forgetting | random_control | skills learned | 39 / 2 / 159 | 20.5 [15.5, 26.6] | 19.5 [14.6, 25.5] | -19.44000 [-22.45266, -16.42734] | 0 of 200 |
| retrievability_priority | two_term | mastery per item | 130 / 0 / 70 | 65.0 [58.2, 71.3] | 65.0 [58.2, 71.3] | +0.00156 [0.00100, 0.00211] | 0 of 200 |
| retrievability_priority | two_term | delayed mastery per item | 131 / 0 / 69 | 65.5 [58.7, 71.7] | 65.5 [58.7, 71.7] | +0.00145 [0.00094, 0.00195] | 0 of 200 |
| retrievability_priority | two_term | retention day 30 | 175 / 0 / 25 | 87.5 [82.2, 91.4] | 87.5 [82.2, 91.4] | +0.09351 [0.08357, 0.10345] | 0 of 200 |
| retrievability_priority | two_term | skills learned | 49 / 3 / 148 | 26.0 [20.4, 32.5] | 24.5 [19.1, 30.9] | -14.70500 [-17.87613, -11.53387] | 0 of 200 |
| retrievability_priority | random_control | mastery per item | 126 / 0 / 74 | 63.0 [56.1, 69.4] | 63.0 [56.1, 69.4] | +0.00142 [0.00091, 0.00192] | 0 of 200 |
| retrievability_priority | random_control | delayed mastery per item | 129 / 0 / 71 | 64.5 [57.7, 70.8] | 64.5 [57.7, 70.8] | +0.00132 [0.00086, 0.00179] | 0 of 200 |
| retrievability_priority | random_control | retention day 30 | 180 / 0 / 20 | 90.0 [85.1, 93.4] | 90.0 [85.1, 93.4] | +0.10508 [0.09475, 0.11541] | 0 of 200 |
| retrievability_priority | random_control | skills learned | 41 / 3 / 156 | 22.0 [16.8, 28.2] | 20.5 [15.5, 26.6] | -19.13000 [-22.32592, -15.93408] | 0 of 200 |
| retrievability_priority_both | two_term | mastery per item | 121 / 0 / 79 | 60.5 [53.6, 67.0] | 60.5 [53.6, 67.0] | +0.00061 [0.00013, 0.00109] | 0 of 200 |
| retrievability_priority_both | two_term | delayed mastery per item | 122 / 0 / 78 | 61.0 [54.1, 67.5] | 61.0 [54.1, 67.5] | +0.00063 [0.00019, 0.00107] | 0 of 200 |
| retrievability_priority_both | two_term | retention day 30 | 167 / 0 / 33 | 83.5 [77.7, 88.0] | 83.5 [77.7, 88.0] | +0.08853 [0.07863, 0.09843] | 0 of 200 |
| retrievability_priority_both | two_term | skills learned | 41 / 1 / 158 | 21.0 [15.9, 27.2] | 20.5 [15.5, 26.6] | -18.02500 [-21.07694, -14.97306] | 0 of 200 |
| retrievability_priority_both | random_control | mastery per item | 111 / 0 / 89 | 55.5 [48.6, 62.2] | 55.5 [48.6, 62.2] | +0.00047 [0.00003, 0.00091] | 0 of 200 |
| retrievability_priority_both | random_control | delayed mastery per item | 114 / 0 / 86 | 57.0 [50.1, 63.7] | 57.0 [50.1, 63.7] | +0.00050 [0.00010, 0.00091] | 0 of 200 |
| retrievability_priority_both | random_control | retention day 30 | 178 / 0 / 22 | 89.0 [83.9, 92.6] | 89.0 [83.9, 92.6] | +0.10010 [0.08945, 0.11075] | 0 of 200 |
| retrievability_priority_both | random_control | skills learned | 35 / 0 / 165 | 17.5 [12.9, 23.4] | 17.5 [12.9, 23.4] | -22.45000 [-25.50615, -19.39385] | 0 of 200 |
| elo_target | two_term | mastery per item | 122 / 0 / 78 | 61.0 [54.1, 67.5] | 61.0 [54.1, 67.5] | +0.00064 [0.00016, 0.00113] | 0 of 200 |
| elo_target | two_term | delayed mastery per item | 122 / 0 / 78 | 61.0 [54.1, 67.5] | 61.0 [54.1, 67.5] | +0.00057 [0.00014, 0.00101] | 0 of 200 |
| elo_target | two_term | retention day 30 | 123 / 0 / 77 | 61.5 [54.6, 68.0] | 61.5 [54.6, 68.0] | +0.02067 [0.00872, 0.03262] | 0 of 200 |
| elo_target | two_term | skills learned | 112 / 2 / 86 | 57.0 [50.1, 63.7] | 56.0 [49.1, 62.7] | +3.02500 [-0.85780, 6.90780] | 0 of 200 |
| elo_target | random_control | mastery per item | 118 / 0 / 82 | 59.0 [52.1, 65.6] | 59.0 [52.1, 65.6] | +0.00051 [0.00005, 0.00096] | 0 of 200 |
| elo_target | random_control | delayed mastery per item | 119 / 0 / 81 | 59.5 [52.6, 66.1] | 59.5 [52.6, 66.1] | +0.00045 [0.00004, 0.00087] | 0 of 200 |
| elo_target | random_control | retention day 30 | 130 / 0 / 70 | 65.0 [58.2, 71.3] | 65.0 [58.2, 71.3] | +0.03224 [0.02004, 0.04444] | 0 of 200 |
| elo_target | random_control | skills learned | 97 / 7 / 96 | 52.0 [45.1, 58.8] | 48.5 [41.7, 55.4] | -1.40000 [-5.40156, 2.60156] | 0 of 200 |
| spread | two_term | mastery per item | 118 / 0 / 82 | 59.0 [52.1, 65.6] | 59.0 [52.1, 65.6] | +0.00044 [-0.00001, 0.00089] | 0 of 200 |
| spread | two_term | delayed mastery per item | 117 / 0 / 83 | 58.5 [51.6, 65.1] | 58.5 [51.6, 65.1] | +0.00041 [0.00000, 0.00082] | 0 of 200 |
| spread | two_term | retention day 30 | 142 / 0 / 58 | 71.0 [64.4, 76.8] | 71.0 [64.4, 76.8] | +0.03241 [0.02346, 0.04136] | 0 of 200 |
| spread | two_term | skills learned | 79 / 5 / 116 | 42.0 [35.4, 48.9] | 39.5 [33.0, 46.4] | -5.53000 [-8.42804, -2.63196] | 0 of 200 |
| spread | random_control | mastery per item | 115 / 0 / 85 | 57.5 [50.6, 64.1] | 57.5 [50.6, 64.1] | +0.00030 [-0.00011, 0.00072] | 0 of 200 |
| spread | random_control | delayed mastery per item | 112 / 0 / 88 | 56.0 [49.1, 62.7] | 56.0 [49.1, 62.7] | +0.00029 [-0.00010, 0.00067] | 0 of 200 |
| spread | random_control | retention day 30 | 149 / 0 / 51 | 74.5 [68.0, 80.0] | 74.5 [68.0, 80.0] | +0.04398 [0.03471, 0.05325] | 0 of 200 |
| spread | random_control | skills learned | 63 / 3 / 134 | 33.0 [26.9, 39.8] | 31.5 [25.5, 38.2] | -9.95500 [-12.95201, -6.95799] | 0 of 200 |
| review_first | two_term | mastery per item | 98 / 0 / 102 | 49.0 [42.2, 55.9] | 49.0 [42.2, 55.9] | -0.00012 [-0.00047, 0.00023] | 0 of 200 |
| review_first | two_term | delayed mastery per item | 99 / 0 / 101 | 49.5 [42.6, 56.4] | 49.5 [42.6, 56.4] | -0.00011 [-0.00043, 0.00021] | 0 of 200 |
| review_first | two_term | retention day 30 | 73 / 0 / 127 | 36.5 [30.1, 43.4] | 36.5 [30.1, 43.4] | -0.02084 [-0.03018, -0.01150] | 0 of 200 |
| review_first | two_term | skills learned | 103 / 19 / 78 | 61.0 [54.1, 67.5] | 51.5 [44.6, 58.3] | +2.25000 [-0.50347, 5.00347] | 0 of 200 |
| review_first | random_control | mastery per item | 88 / 0 / 112 | 44.0 [37.3, 50.9] | 44.0 [37.3, 50.9] | -0.00026 [-0.00062, 0.00010] | 0 of 200 |
| review_first | random_control | delayed mastery per item | 88 / 0 / 112 | 44.0 [37.3, 50.9] | 44.0 [37.3, 50.9] | -0.00023 [-0.00057, 0.00010] | 0 of 200 |
| review_first | random_control | retention day 30 | 84 / 0 / 116 | 42.0 [35.4, 48.9] | 42.0 [35.4, 48.9] | -0.00927 [-0.01898, 0.00044] | 0 of 200 |
| review_first | random_control | skills learned | 79 / 10 / 111 | 44.5 [37.8, 51.4] | 39.5 [33.0, 46.4] | -2.17500 [-5.09472, 0.74472] | 0 of 200 |

## World legacy, power law forgetting, 226 days

| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |
|---|---|---|---|---|---|---|---|
| two_term | 200 | 2909 | 63.3 | 63.5 | 0.00783 [0.00739, 0.00828] | 0.00701 [0.00661, 0.00741] | 0.7530 |
| random_control | 200 | 2912 | 66.7 | 63.5 | 0.00807 [0.00762, 0.00852] | 0.00725 [0.00685, 0.00765] | 0.7405 |
| oracle_forgetting | 200 | 2908 | 46.2 | 75.8 | 0.00899 [0.00846, 0.00952] | 0.00819 [0.00771, 0.00867] | 0.8479 |
| retrievability_priority | 200 | 2904 | 44.8 | 65.4 | 0.00845 [0.00794, 0.00896] | 0.00771 [0.00725, 0.00817] | 0.8503 |
| retrievability_priority_both | 200 | 2904 | 45.5 | 71.2 | 0.00843 [0.00792, 0.00894] | 0.00772 [0.00726, 0.00818] | 0.8427 |
| elo_target | 200 | 2902 | 68.6 | 78.4 | 0.00932 [0.00882, 0.00982] | 0.00836 [0.00792, 0.00881] | 0.7683 |
| spread | 200 | 2912 | 57.2 | 63.8 | 0.00806 [0.00757, 0.00855] | 0.00728 [0.00684, 0.00772] | 0.7788 |
| review_first | 200 | 2908 | 64.8 | 65.1 | 0.00768 [0.00724, 0.00812] | 0.00692 [0.00653, 0.00731] | 0.7332 |

| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |
|---|---|---|---|---|---|---|---|
| oracle_forgetting | two_term | mastery per item | 123 / 0 / 77 | 61.5 [54.6, 68.0] | 61.5 [54.6, 68.0] | +0.00116 [0.00063, 0.00169] | 0 of 200 |
| oracle_forgetting | two_term | delayed mastery per item | 125 / 0 / 75 | 62.5 [55.6, 68.9] | 62.5 [55.6, 68.9] | +0.00118 [0.00070, 0.00166] | 0 of 200 |
| oracle_forgetting | two_term | retention day 30 | 183 / 0 / 17 | 91.5 [86.8, 94.6] | 91.5 [86.8, 94.6] | +0.09491 [0.08552, 0.10430] | 0 of 200 |
| oracle_forgetting | two_term | skills learned | 45 / 6 / 149 | 25.5 [20.0, 32.0] | 22.5 [17.3, 28.8] | -17.08500 [-20.13011, -14.03989] | 0 of 200 |
| oracle_forgetting | random_control | mastery per item | 114 / 0 / 86 | 57.0 [50.1, 63.7] | 57.0 [50.1, 63.7] | +0.00093 [0.00041, 0.00144] | 0 of 200 |
| oracle_forgetting | random_control | delayed mastery per item | 116 / 0 / 84 | 58.0 [51.1, 64.6] | 58.0 [51.1, 64.6] | +0.00095 [0.00048, 0.00141] | 0 of 200 |
| oracle_forgetting | random_control | retention day 30 | 194 / 0 / 6 | 97.0 [93.6, 98.6] | 97.0 [93.6, 98.6] | +0.10740 [0.09889, 0.11592] | 0 of 200 |
| oracle_forgetting | random_control | skills learned | 36 / 0 / 164 | 18.0 [13.3, 23.9] | 18.0 [13.3, 23.9] | -20.46500 [-23.45073, -17.47927] | 0 of 200 |
| retrievability_priority | two_term | mastery per item | 116 / 0 / 84 | 58.0 [51.1, 64.6] | 58.0 [51.1, 64.6] | +0.00061 [0.00013, 0.00110] | 0 of 200 |
| retrievability_priority | two_term | delayed mastery per item | 118 / 0 / 82 | 59.0 [52.1, 65.6] | 59.0 [52.1, 65.6] | +0.00070 [0.00026, 0.00113] | 0 of 200 |
| retrievability_priority | two_term | retention day 30 | 180 / 0 / 20 | 90.0 [85.1, 93.4] | 90.0 [85.1, 93.4] | +0.09733 [0.08788, 0.10678] | 0 of 200 |
| retrievability_priority | two_term | skills learned | 36 / 1 / 163 | 18.5 [13.7, 24.5] | 18.0 [13.3, 23.9] | -18.47500 [-21.36496, -15.58504] | 0 of 200 |
| retrievability_priority | random_control | mastery per item | 112 / 0 / 88 | 56.0 [49.1, 62.7] | 56.0 [49.1, 62.7] | +0.00038 [-0.00006, 0.00082] | 0 of 200 |
| retrievability_priority | random_control | delayed mastery per item | 115 / 0 / 85 | 57.5 [50.6, 64.1] | 57.5 [50.6, 64.1] | +0.00046 [0.00006, 0.00086] | 0 of 200 |
| retrievability_priority | random_control | retention day 30 | 191 / 0 / 9 | 95.5 [91.7, 97.6] | 95.5 [91.7, 97.6] | +0.10982 [0.10131, 0.11834] | 0 of 200 |
| retrievability_priority | random_control | skills learned | 23 / 3 / 174 | 13.0 [9.0, 18.4] | 11.5 [7.8, 16.7] | -21.85500 [-24.52340, -19.18660] | 0 of 200 |
| retrievability_priority_both | two_term | mastery per item | 107 / 0 / 93 | 53.5 [46.6, 60.3] | 53.5 [46.6, 60.3] | +0.00059 [0.00001, 0.00117] | 0 of 200 |
| retrievability_priority_both | two_term | delayed mastery per item | 111 / 0 / 89 | 55.5 [48.6, 62.2] | 55.5 [48.6, 62.2] | +0.00071 [0.00019, 0.00123] | 0 of 200 |
| retrievability_priority_both | two_term | retention day 30 | 181 / 0 / 19 | 90.5 [85.6, 93.8] | 90.5 [85.6, 93.8] | +0.08969 [0.08022, 0.09917] | 0 of 200 |
| retrievability_priority_both | two_term | skills learned | 48 / 3 / 149 | 25.5 [20.0, 32.0] | 24.0 [18.6, 30.4] | -17.83000 [-21.04818, -14.61182] | 0 of 200 |
| retrievability_priority_both | random_control | mastery per item | 103 / 0 / 97 | 51.5 [44.6, 58.3] | 51.5 [44.6, 58.3] | +0.00036 [-0.00019, 0.00091] | 0 of 200 |
| retrievability_priority_both | random_control | delayed mastery per item | 107 / 0 / 93 | 53.5 [46.6, 60.3] | 53.5 [46.6, 60.3] | +0.00047 [-0.00002, 0.00096] | 0 of 200 |
| retrievability_priority_both | random_control | retention day 30 | 186 / 0 / 14 | 93.0 [88.6, 95.8] | 93.0 [88.6, 95.8] | +0.10219 [0.09268, 0.11170] | 0 of 200 |
| retrievability_priority_both | random_control | skills learned | 31 / 4 / 165 | 17.5 [12.9, 23.4] | 15.5 [11.1, 21.2] | -21.21000 [-24.34007, -18.07993] | 0 of 200 |
| elo_target | two_term | mastery per item | 135 / 0 / 65 | 67.5 [60.7, 73.6] | 67.5 [60.7, 73.6] | +0.00149 [0.00094, 0.00203] | 0 of 200 |
| elo_target | two_term | delayed mastery per item | 135 / 0 / 65 | 67.5 [60.7, 73.6] | 67.5 [60.7, 73.6] | +0.00135 [0.00088, 0.00183] | 0 of 200 |
| elo_target | two_term | retention day 30 | 116 / 0 / 84 | 58.0 [51.1, 64.6] | 58.0 [51.1, 64.6] | +0.01534 [0.00392, 0.02676] | 0 of 200 |
| elo_target | two_term | skills learned | 120 / 4 / 76 | 62.0 [55.1, 68.4] | 60.0 [53.1, 66.5] | +5.27500 [1.48217, 9.06783] | 0 of 200 |
| elo_target | random_control | mastery per item | 123 / 0 / 77 | 61.5 [54.6, 68.0] | 61.5 [54.6, 68.0] | +0.00125 [0.00071, 0.00179] | 0 of 200 |
| elo_target | random_control | delayed mastery per item | 124 / 0 / 76 | 62.0 [55.1, 68.4] | 62.0 [55.1, 68.4] | +0.00111 [0.00064, 0.00159] | 0 of 200 |
| elo_target | random_control | retention day 30 | 128 / 0 / 72 | 64.0 [57.1, 70.3] | 64.0 [57.1, 70.3] | +0.02783 [0.01710, 0.03857] | 0 of 200 |
| elo_target | random_control | skills learned | 103 / 3 / 94 | 53.0 [46.1, 59.8] | 51.5 [44.6, 58.3] | +1.89500 [-1.82476, 5.61476] | 0 of 200 |
| spread | two_term | mastery per item | 101 / 0 / 99 | 50.5 [43.6, 57.4] | 50.5 [43.6, 57.4] | +0.00023 [-0.00025, 0.00071] | 0 of 200 |
| spread | two_term | delayed mastery per item | 101 / 0 / 99 | 50.5 [43.6, 57.4] | 50.5 [43.6, 57.4] | +0.00027 [-0.00015, 0.00069] | 0 of 200 |
| spread | two_term | retention day 30 | 137 / 0 / 63 | 68.5 [61.8, 74.5] | 68.5 [61.8, 74.5] | +0.02584 [0.01593, 0.03575] | 0 of 200 |
| spread | two_term | skills learned | 78 / 4 / 118 | 41.0 [34.4, 47.9] | 39.0 [32.5, 45.9] | -6.15500 [-9.24683, -3.06317] | 0 of 200 |
| spread | random_control | mastery per item | 98 / 0 / 102 | 49.0 [42.2, 55.9] | 49.0 [42.2, 55.9] | -0.00000 [-0.00050, 0.00049] | 0 of 200 |
| spread | random_control | delayed mastery per item | 98 / 0 / 102 | 49.0 [42.2, 55.9] | 49.0 [42.2, 55.9] | +0.00003 [-0.00041, 0.00047] | 0 of 200 |
| spread | random_control | retention day 30 | 142 / 0 / 58 | 71.0 [64.4, 76.8] | 71.0 [64.4, 76.8] | +0.03834 [0.02860, 0.04807] | 0 of 200 |
| spread | random_control | skills learned | 63 / 6 / 131 | 34.5 [28.3, 41.3] | 31.5 [25.5, 38.2] | -9.53500 [-12.67186, -6.39814] | 0 of 200 |
| review_first | two_term | mastery per item | 95 / 0 / 105 | 47.5 [40.7, 54.4] | 47.5 [40.7, 54.4] | -0.00016 [-0.00059, 0.00027] | 0 of 200 |
| review_first | two_term | delayed mastery per item | 97 / 0 / 103 | 48.5 [41.7, 55.4] | 48.5 [41.7, 55.4] | -0.00009 [-0.00046, 0.00028] | 0 of 200 |
| review_first | two_term | retention day 30 | 76 / 0 / 124 | 38.0 [31.6, 44.9] | 38.0 [31.6, 44.9] | -0.01978 [-0.02967, -0.00989] | 0 of 200 |
| review_first | two_term | skills learned | 100 / 10 / 90 | 55.0 [48.1, 61.7] | 50.0 [43.1, 56.9] | +1.53500 [-1.39197, 4.46197] | 0 of 200 |
| review_first | random_control | mastery per item | 87 / 0 / 113 | 43.5 [36.8, 50.4] | 43.5 [36.8, 50.4] | -0.00039 [-0.00084, 0.00006] | 0 of 200 |
| review_first | random_control | delayed mastery per item | 86 / 0 / 114 | 43.0 [36.3, 49.9] | 43.0 [36.3, 49.9] | -0.00033 [-0.00073, 0.00007] | 0 of 200 |
| review_first | random_control | retention day 30 | 80 / 0 / 120 | 40.0 [33.5, 46.9] | 40.0 [33.5, 46.9] | -0.00729 [-0.01763, 0.00306] | 0 of 200 |
| review_first | random_control | skills learned | 88 / 6 / 106 | 47.0 [40.2, 53.9] | 44.0 [37.3, 50.9] | -1.84500 [-5.05435, 1.36435] | 0 of 200 |
