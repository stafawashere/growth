---
title: Growth's Today, measured against the research base
research_date: 2026-09-29
status: in_progress
purpose: Measure the algorithm, the session shape and the question bank behind Today before judging them, and name each flaw against the Stage A and Stage B evidence.
---

# Growth's Today, measured

Every number below was measured in this session, by the command named beside it. Simulated numbers are a simulation's measurement on synthetic students whose world model is invented; the browser walk and the item audit are readings of the real application and the real bank. Flaws are numbered T1 onward and each names the synthesis rank or design section it is measured against.

## The algorithm, on the simulator [verified]

Source: `tools/today_metrics.py 20 <days> exponential fixed 2` (`audit/today-metrics-60d.md`, `audit/today-metrics-226d.md`), two-term arm, fixed world, 20 synthetic students from seed 20270510, mean with the 95 percent interval.

| Measure | 60 days | 226 days |
|---|---|---|
| items per session | 12.6 [12.5, 12.8] | 12.9 [12.9, 12.9] |
| forecast minutes per session | 37.9 [37.5, 38.4] | 38.7 [38.6, 38.8] |
| block 2 choices decided by due coverage, single winner | 15.6 percent | 16.0 percent |
| decided by due coverage with a tie among the best | 17.5 percent | 19.1 percent |
| decided by a uniform draw (no candidate reached a due skill) | 66.9 percent [62.1, 71.7] | 64.9 percent [61.2, 68.5] |
| tied pool size at the choice, modal value | 1 (22 percent), then 6 (14 percent) | 1 (19 percent) |
| window removed candidates per choice | 0.27 | 0.16 |
| window changed the eventual pick | 12.9 percent of choices | 4.9 percent |
| hypercorrection items served | 0 | 0 |
| requeued corrected items served per student | 58.8 | 224.8 |
| sessions with at least one due skill | 51.6 of 60 | 217.4 of 226 |
| due skills per due session | 5.5 | 12.4 |
| archetypes the compression cover chose per due session | 1.3 | 3.5 |
| due skills left uncovered per due session | 3.9 [2.6, 5.3] | 8.4 [7.3, 9.4] |
| compression ratio, due skills per cover archetype | 4.1 | 4.0 |
| skills mastered from practice per student | 54.8 [49.2, 60.3] | 157.8 [145.9, 169.6] |
| items loading a skill before it is declared, median | 25.4 | 26.8 |
| forecast over simulated minutes | 1.000 | 1.000 |

The recorded selection study of 2026-09-27 found due coverage firing on 1.1 percent of block 2 choices at 60 days and 7.5 percent at 226, with 13.6 and 32.2 skills mastered from practice. On today's engine the same students master four to five times as many skills (the 2026-09-29 corrections to mastery condition 3, the example skip and the failure decay), so due coverage now decides a third of block 2 choices. The re-run of `tools/selection_study.py` on the recorded seeds is reported in the ledger entry; its record supersedes the 2026-09-27 numbers.

Flaws measured here:

- T1. Two thirds of block 2 picks are uniform random and the modal tied pool is the whole candidate set (synthesis rank 1; clean-slate design, the selection policy). The one informative term reads only mastered skills; retrievability exists for every observed skill and is not read by the choice.
- T2. Block 3 serves the retrieval pool by due coverage and the window, never by predicted forgetting, so the least-retained learned skill is served no sooner than any other (synthesis rank 1, the block 3 reading).
- T3. Most due skills go unserved: 3.9 of 5.5 per due session at 60 days and 8.4 of 12.4 at 226 are uncovered by the greedy cover under the retrieval floor and the published-item test, and block 1 stops at 5 items or 5 minutes in any case (synthesis rank 6, the hidden backlog; design, review compression). The cause split (no published item, floor, window) is not yet instrumented per skill; C2 in the rulings file asks for it before any threshold moves.
- T4. The interleaving window is nearly inert as a constraint: it removes 0.16 to 0.27 candidates per choice and changes the pick on 5 to 13 percent of choices, because the random draw already supplies variety. Contrast between confusable skills is never chosen on purpose (synthesis rank 3).
- T5. The hypercorrection lane cannot be measured on this simulator, which rates every answer unsure, so 0 is a limit of the harness, not a finding about the app. The walk below measures it on the real feedback screen.
- T6. The minute forecast equals the simulated time by construction (3 minutes per attempt on both sides), so the simulator cannot test the forecast. The walk reads the real forecast against the wall clock.
- T7. A cold-start skill takes a median of 25 to 27 items that load it before it is declared mastered, at about 13 items a session (synthesis rank 9, kept by design; science.md 7 on over-practice). The number is a cost to show the operator, not a gate to move.

## The session shape, in the browser [uncertain]

Measured on the scratch servers (API 127.0.0.1:8005 and 8006, web 5175 and 5176, `GROWTH_AI_BACKEND=none`), a fresh student and a student with 28 seeded days, on 2026-09-29. Filled in from the walk below.

WALK_PLACEHOLDER

## The question bank [verified]

Source: `tools/draw_today_audit_sample.py --size 72 --seed 2026` over the 3,316 records under content/items_*, then the blind re-solve (`audit/recheck-2026-09-29.md`, `audit/blind-notes-2026-09-29.md`) and the judgment audit (`audit/judgment-2026-09-29.md`), each by a separate Opus agent, the re-solver never seeing a key.

| Measure | Value |
|---|---|
| records in the bank | 3,316 (template 2,530, agent draft 656, P1 draft 130; mcq 3,261, short answer 55; calculator 615) |
| sample | 72 across 11 unit blocks, 3 provenance classes, 6 short answer, 12 calculator |
| keys re-solved blind | 64 of 72 formulated; 64 of 64 match the stored key; control 8 of 8 perturbations reported different; 8 not formulable from the stem alone (5 need a table, 3 the graph of f') |
| key errors found | 0 of 64 (Wilson 95 percent interval 0.0 to 5.7 percent) |
| judgment verdicts | clean 50, fix_distractor 15, fix_stem 7, key suspect 0, reject 0 |
| distractors that follow from their named error | 204 of 216 |
| distinct error paths among the three distractors | 3 on 44 items, 2 on 23, 1 on 5 (all five agent drafts) |
| statement items with a defensible second choice | 3 of 18 |
| items with a cue toward the key | 16 of 72 |
| representation | symbolic 45.8 percent of the sample against 40.1 in the bank; table 5.6 against 8.1 |
| calculator | 12 of 72 (16.7 percent) against 18.5 in the bank; 2 of the 12 need no calculator |
| difficulty, the auditor's judgement | easy 20, medium 47, hard 5 |
| duplicates inside the sample | 9 groups over 19 items |
| items per active archetype (148) | min 20, median 22, max 28; none under 5 |
| distinct stems per archetype with digits masked | min 1, median 17, max 27; 12 archetypes under 5, 2 with one |
| bank-wide, from question-standards.md 12 | distractors sharing an error path 30.1 percent of items; numeric options unsorted 92.1 percent; statement key the longest option 40.8 percent; missing command_verb 786; missing mechanism and derivation 2,358; 87 calculator stems ask for three decimals and 48 keys carry fewer |

Flaws:

- T8. One in three items has two distractors from one error path and one in fourteen has all three from one, so a wrong answer diagnoses less than it could (question-standards.md 2; synthesis, warnings).
- T9. One in four sampled items shows a cue toward the key: the only positive area, the only interior value, the key's negation among the options, the longest statement (question-standards.md 3).
- T10. 15 of 66 sampled mcq stems ask for work, a setup, units or a stated form that four options cannot carry, all template items (question-standards.md 7).
- T11. 3 of 18 statement items carry a distractor a student can defend, the failure the standing audit rule names first (question-standards.md 1).
- T12. Calculator items are under-served against the exam's 15 percent of Section I and 33 percent of Section II, 2 of 12 sampled calculator items need no calculator, and 48 calculator keys carry fewer than three decimals (question-standards.md 5).
- T13. Tabular and graphical representations are under the bank's own share in the sample and 8 of 72 items cannot be solved from their stem text because the table or graph lives outside it, which also blocks any blind re-solve of them (question-standards.md 6).
- T14. Repetition: 12 archetypes carry fewer than 5 distinct stems, so a 226-day student (2,917 items) sees the same problem with new numbers many times on those archetypes (question-standards.md 11).
- T15. Keys are sound where they could be checked: 0 of 64, with the caveat that the 8 figure-dependent items were re-solved by the judgment auditor from the record, not blind.
