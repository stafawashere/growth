---
title: Growth's Today, measured against the research base
research_date: 2026-09-29
status: draft
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

The recorded selection study of 2026-09-27 found due coverage firing on 1.1 percent of block 2 choices at 60 days and 7.5 percent at 226, with 13.6 and 32.2 skills mastered from practice. On today's engine the same students master four to five times as many skills (the 2026-09-29 corrections to mastery condition 3, the example skip and the failure decay), so due coverage now decides a third of block 2 choices. The re-run of `tools/selection_study.py` on the recorded seeds (124 minutes, `docs/operator/selection-study.md`, "Re-run of 2026-09-29") confirms it on 200 students: due coverage fires on 40.0 percent of block 2 choices at 60 days and 45.8 at 226, and with the term firing two-term now teaches fewer skills than the random control and sits wholly below it on mastery per item at both horizons under both curves (paired mean difference -0.00301 [-0.00389, -0.00214] at 60 days, exponential). The two-term floor of plan 10 fails on this record under the 2026-09-27 ruling; the floor is not moved, and the finding is T1's other half: the one informative term, when it fires, spends block 2 on mastered skills and teaches less.

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

The seeded student (28 closed sessions from 2026-09-01 to 2026-09-28, 595 items at 0.70 accuracy, placed fluent in Units 1 to 3 by `tools/seed_history_student.py`) and a fresh student created at the sign-in form.

Screen by screen, the seeded student:

1. Sign in, then Today shows "Loading" for 20 seconds: `GET /progress` answered in 20.6 s and 18.2 s on two reads (the machine was under the simulation load; the ledger's Known defects already record over 45 s on an idle server). The read assembles the whole session to preview it.
2. Today: the exam countdown with the verdict "Behind pace"; 38 minutes estimated; two count lines, 11 skills at the frontier and 5 corrected items coming back; the third line, skills due for review, is hidden because it reads 0; three focus cards naming block, intent, units, item count and the first four skill names, including the mixed block's. The payload behind it says 39 skills are due today, 48 forecast minutes of them, and 0 of those reach block 1: the review block's 5 items are all corrected-item requeues.
3. Start today's set: 38 items, about 39 minutes, a progress bar of dots, "I want to stop here". Item 1 at stage unsupported, short answer with the math field and the raw LaTeX inspector, the confidence prompt before checking.
4. An answer typed and checked within the same second was stored as `{"mathjson": null}`: the attempt was written ungraded (correct null, every skill `not_attempted`), the feedback screen showed only "You wrote 5" and "Next item", no verdict, no elaboration, no error note, and the item was consumed. With a two-second pause before checking, the same field graded normally on items 4 and 5. The field commits its value on MathLive's change event, so a fast student can lose an item.
5. Item 2 at stage completion, a statement choice with two worked steps shown and the last step to choose: a wrong answer rated confident gave the verdict head "Not yet. Here is where it turned.", the step marks (given, given, "Not yet" with the right step's text), the self-explanation prompt and the required one-line error note. The correct option itself is not named apart from the right step's sentence.
6. Item 3 at stage example, a choice with all steps shown: a correct answer gave "That holds.", the step marks with "Correct" on the last step, and no reinforcement sentence (the tutor is off with `GROWTH_AI_BACKEND=none`).
7. Item 4 at stage unsupported, a table item, a wrong short answer: the elaborated panel showed the violated step name only ("report the numerical value"), no observed behaviour and no scoring consequence, because a short answer carries no error path and no diagnostician runs without a model. The correct value was not shown anywhere.
8. A refresher slot ("A short refresher, about a minute", two key ideas, "Back to the problem") before item 5.
9. Item 5 at stage unsupported, a four-option integral: a wrong option rated confident gave the full elaborated panel (violated step, the BC-ERR observed behaviour, the scoring consequence) and "Read the part on this error". The correct option was not shown.
10. "I want to stop here" asks for confirmation; the end screen says 5 items worked, "The 3 you corrected come back in Review, with your notes.", and "Today shows what is due next, in minutes, whenever you open it." The ungraded item counted as worked and not as corrected.
11. Back on Today the set was rebuilt for the same day (39 minutes, 2 corrected items, 11 frontier skills, 8 mixed), the stopped set was not resumable, and the payload still carried 37 due skills and 40 due minutes with 0 of them in block 1. The Review tab listed 19 corrected items "coming back", 16 of them due today, so the requeue lane alone exceeds block 1's cap of 5.

The fresh student:

1. Create account, the recovery code, then the placement: "Question 1 of at most 30", every question a short answer with "I have not learned this yet" and "Skip this unit" (confirmed by "Skip the rest of this unit"); the first four questions came from Units 9, 6, 8 and 8 before any Unit 1 or 2 question; four questions answered correctly (Units 2, 1, 1, 2) and the rest skipped or not learned; done at question 27 of 30. The result screen: Unit 1 "Not placed yet" after two correct Unit 1 answers, Unit 2 "Fluent", the rest "Not started yet". Two P1 stems rendered as plain text with carets.
2. Today: "Too early to call" on the countdown, 36 minutes, 6 frontier skills, no review line, a New ground card of 8 items across Units 1, 2, 3, 4 and 5 (critical points from Unit 5 among them for a student placed only in Unit 2) and a Mixed practice card of 4 Unit 2 items, with skill names.
3. Start today's set: 10 items, about 37 minutes. Item 1 is the productive-failure opener ("Before the method", "Try this before the method is shown"): a correct answer rated confident gave "Feedback", "You wrote", "Next item" and no comparison with the canonical method (the comparison needs the tutor, which is off).
4. Item 2 was preceded by "A lesson first" (3 minutes, 11 parts, the prediction screen with Commit, "Skip to the problem"), then a stage-example concept check with three steps shown and the last step to choose, the self-explanation prompt, and the confidence prompt.

Flaws measured on the walk:

- T16. The wrong-answer feedback never shows the correct answer: a short-answer miss shows the violated step's name alone, a choice miss shows the step, the observed behaviour and the scoring consequence, and neither shows what the correct response would have been (plan 03, Content, part 3; synthesis rank 5).
- T17. The due queue is starved twice over on a real student: 37 to 39 due skills and 40 to 48 forecast minutes of them, 0 served, while 16 corrected items due today fill block 1's 5-item cap and 11 more wait behind them (T3 confirmed; synthesis rank 6; rulings C1 and C2).
- T18. A fast submission on the math field records an ungraded attempt and consumes the item with no feedback and no requeue (a client defect, not a design flaw; it is listed for the build stage).
- T19. Today shows "Loading" for about 20 seconds on a student with history because the preview assembles the whole session (Known defects, 2026-09-23); the fresh student waited 6 seconds.
- T20. The mixed block's focus card names its skills before the set, which is the announced-review pattern Matuschak names (synthesis warnings; rulings R10).
- T21. The pace verdict ("Behind pace", "Too early to call") is the one element of Today that reads as a target or a forecast about the student (rulings C5).
- T22. A stopped set is discarded and rebuilt rather than resumed, so the stop confirmation's promise "Today builds the next set from it" holds but the ordering the student had seen is lost; the ungraded item of T18 is counted as worked.
- T23. Without the tutor the opener shows no comparison and a correct answer shows no reinforcement, so the plan 02 productive-failure opener degrades to a plain item when `GROWTH_AI_BACKEND=none` (plan 01, Productive-failure openers).
- T24. A fresh student placed only in Unit 2 is served Unit 5 skills in block 2, because a parent no archetype loads does not gate (`blocking_parents`), so the fringe on a new student spans five units on day one (plan 02, Prerequisite gating; the 2026-09-26 and 2026-09-28 corrections).
- T25. The placement result says "Not placed yet" for a unit whose two questions were answered correctly, and the first four questions came from Units 6, 8 and 9 (plan 02, Cold-start diagnostic, the unit pool cap).

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
