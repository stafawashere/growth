---
title: Gap analysis, Growth's lessons before the redesign
research_date: 2026-09-29
status: draft
purpose: Measure the 127 signed-off lesson records and the reader as they stood on 2026-09-29 before the redesign, then name each flaw against the synthesis and the clean-slate design with the measured number beside it.
---

# Gap analysis

Every number below was computed on 2026-09-29 over `content/lessons/*.json` at commit 82927a2 by a script that loads each record and runs `app/lessons/plan.py plan_lesson` for both bands (the script and its output are in the session scratchpad and the ledger quotes them). The walk was done in the built-in browser against a scratch database on ports 8004 and 5174 with a fresh account, the Lessons tab, and LSN-CON-01001 read end to end.

## The measured state [verified]

| Measure | Value |
|---|---|
| Records | 127, all `signed_off` |
| Section counts | orientation 127, key_ideas 181, strategy 182, worked_example 157, what_a_reader_scores 83, common_error 399, representations 11, prerequisite_bridge 216 |
| Key ideas per lesson | 1 on 85 lessons, 2 on 31, 3 on 10, 4 on 1 |
| Error blocks per lesson | 0 on 2, 1 on 8, 2 on 23, 3 on 31, 4 on 63 |
| Worked examples per lesson | 1 on 97, 2 on 30 |
| Steps per example | min 2, median 4, mean 4.6, max 9; valued steps median 4 |
| Cue and why words per step | cue median 5 (max 16), why median 5 (max 20); caps 20 and 25 |
| Anchor quotes | 102 across 181 key ideas |
| Delivery modes over 875 delivered blocks | step_reveal 556, text 178, figure 76, interactive 23, table 19, motion 19, model 4 |
| Modes by block type | orientation: text 90, figure 31, table 5, interactive 1; key idea: text 88, figure 42, interactive 22, motion 19, table 10; representations: model 4, table 4, figure 3 |
| Lessons with no drawn block (figure, table, motion, interactive or model) | 50 of 127 |
| Lessons with an interactive block | 23 of 127 |
| Drawn blocks per lesson | 0 on 50, 1 on 29, 2 on 36, 3 on 9, 4 on 2, 5 on 1 |
| Checks per lesson | 3 on 105, 2 on 22; kinds completion 127, isomorph 127, mcq 105; every mcq has 4 options |
| Distractors | 315, every one carrying an `error_path` |
| Error blocks with the same expression on the wrong and the right step | 28 of 399 |
| Error blocks with a possible reason | 299 of 399 |
| Reader-score sections | 83, lines per section median 1, max 4 |
| Low band screens (sections plus checks) | min 6, median 12, max 16 |
| Mid band screens | min 6, median 9, max 10 |
| Low band words | min 240, median 481, mean 491, max 825 (cap 900) |
| Mid band words | min 240, median 368, max 420 (cap 450) |
| Low band minutes | min 2.0, median 3.8, max 6.0 (cap 6) |
| Mid band minutes | min 2.0, median 3.0, max 3.0 (cap 3); 22 lessons sit at the cap |
| Screen on which the first check appears, low band | min 5, median 9, max 14 |
| Error blocks between worked example 1 and its completion check | 4 on 63 lessons, 3 on 31, 2 on 23, 1 on 8, 0 on 2 |
| First screen with any student action (a check, or an interactive, motion or model block) | median 8, min 1 |
| What the mid band drops | 30 key ideas, 157 error blocks, 105 checks, across the 127 lessons |
| Orientation or key idea texts carrying a record id or a page citation | 42 (the reader strips citation-only parentheticals before display) |

What adapts per student: the band (full or brief), the error-keyed refresher order, the prerequisite bridge by state, the feedback link into a trap. What is fixed: every sentence, every figure, every check, the order of screens, and the check position.

## The walk, screen by screen [verified]

A first-time student who opens the Lessons tab sees a page headed "Lessons" with the callout "Lessons build context before practice. Reading a lesson does not count toward mastery.", a search field, unit tiles ("Limits and Continuity, 19 ready" through "Applications of Integration, 21 ready", Units 9 and 10 "Coming later"), then every concept row with a mark, the concept name, a state line and a "Start" button. Each row's hidden mark label reads "Coming later" while its state line reads "Coming up", two words for one state on one row.

LSN-CON-01001, low band, 12 parts:

1. "What a response shows", the orientation with a three-row table; the table's label "s(t) = 2t^2 + t + 3" is shown as raw text, not typeset.
2. "Key idea" with a motion figure, four frames of a secant closing on a tangent, "Frame 1 of 4. h = 1", Previous frame, Next frame, "Step on its own".
3. and 4. "Key idea", text only, each with a quotation beneath.
5. "Recognising the question": Cue, First line, Rival, Separating feature as a definition list. The method line reads "First line: First line: the quotient over the first interval." because the record's text already begins with the label.
6. "Worked example": the problem, then step 1 of 4 with its why beside it and a "Next step" button. "Next part" leaves the screen with steps 2 to 4 unrevealed.
7. and 8. "A common error": the observed behaviour, "Wrong step" with its text and value, "Next step" to reveal the right step, then the consequence and "A possible reason". The wrong value 0.52 renders as the fraction 13/25 and 5.2 as 26/5, so the typeset value disagrees with the sentence beside it.
9. and 10. "Check": a stem, a MathLive field, the raw LaTeX inspector, "Check my answer".
11. "Check": a stem and four option rows whose values render as 61/100, 61/10, 6 and 601/100.
12. "That is the end of this lesson." with "Back to lessons".

A wrong answer on part 11 shows a cross, "Not yet.", the error's observed behaviour, the sentence "The part above on that error shows the right step beside it.", and a button "Go to the part on that error". The submit button stays enabled, so a retry is possible but nothing says so. The right step is not shown on the verdict.

The network log shows one `GET /lessons/LSN-CON-01001/plan` and one `POST /lessons/LSN-CON-01001/events` per screen; the three events for the check screens returned 422 because the reader posts `mode: "check"` and the route accepts only the delivery modes, so every check-screen view is lost from the telemetry. The console held no error of the app's own beyond those responses.

## The flaws, each against the synthesis and the clean-slate design [inferred]

| Id | Flaw | Measured | Against |
|---|---|---|---|
| G1 | The student is told before being asked. No lesson opens with a question; the median first action is screen 8 of 12, and in 97 lessons the first action is a check on screen 5 to 14 | first action median 8; prediction sections 0 of 127 | synthesis rank 2; clean slate "Predict" at 0:00 |
| G2 | Practice is delayed past the traps. The completion check of worked example 1 follows every error block in 125 of 127 lessons, so up to 4 blocks and about 160 words separate the example from its own completion | 125 of 127; first check median screen 9 | synthesis rank 1; clean slate 3:30 |
| G3 | The traps are read, not worked. Every one of the 399 error blocks reveals the right step on a button; none asks the student to find or fix the error | 399 of 399 passive | synthesis rank 3; clean slate "Traps" |
| G4 | Recognition names a rival without showing one. The 182 strategy blocks state a rival method in prose; no lesson shows a near-miss stem beside the concept's stem | 0 contrast pairs | synthesis rank 4; clean slate "Recognise" |
| G5 | The second example is not faded. In the 30 lessons with two examples, both are shown in full, so the only fade is check 1's single blank | 30 of 30 unfaded | synthesis rank 1; clean slate 5:00 |
| G6 | Half the lessons have nothing to look at or move. 50 of 127 lessons carry no figure, table, motion, interactive or model block; 23 carry an interactive one | 50 of 127 | synthesis rank 6; clean slate "Key idea" |
| G7 | The wrong-answer verdict verifies more than it informs. It names the behaviour and links the trap; it does not show the right step or the consequence, and the retry is silent | walk, part 11 | synthesis rank 5; clean slate "The feedback loop" |
| G8 | A worked example can be left with its steps unrevealed | walk, part 6 | clean slate "Interaction design" |
| G9 | Decimal values render as fractions, and a table label is not typeset | walk, parts 1, 7, 8, 11 | clean slate "Visual system" |
| G10 | Check-screen views are rejected by the events route | 3 of 12 views lost, 422 | clean slate "Engineering" |
| G11 | The pacing bar says how many parts remain and nothing about what kind | walk, every part | clean slate "Interaction design" |
| G12 | The mid band drops both traps on lessons at the 3-minute cap only by the plan function's word fit, not by design | 22 lessons at 3.0 minutes | rulings C4 |
| G13 | 28 error blocks carry the same expression on both sides, so the difference is in the sentence alone and a fix prompt cannot be posed | 28 of 399 | clean slate "Content model" |
| G14 | 42 served texts carry a record id or a page citation that the reader has to strip at render time | 42 | clean slate "Content model" |
| G15 | The strategy method line begins with the label the reader already prints, so the screen reads "First line: First line: ..." | 67 of 127 lessons | design defect across the units; the served-text rule in the clean slate refuses a leading label |
| G16 | The library row says "Coming later" and "Coming up" for the same state | walk, Lessons tab | copy defect, `LessonsRoute.tsx` |

Nothing measured contradicts the caps: every record is under 900 and 450 words and under 6 and 3 minutes, so the redesign fits inside them. Nothing measured touches the engine, the mastery rule or any credited state, and the redesign leaves those untouched.

## What is already right, and kept [inferred]

The step reveal with a why beside each step (synthesis rank 10), the scoring checklist from BC-PT records, the cue-method-rival strategy block, the error path on every distractor, the caps, the plan function's determinism, the verification pipeline before sign-off, the always-present skip, and the library's "Reading a lesson does not count toward mastery" line. The redesign changes what happens on a screen and where the screens fall, not what the lesson is allowed to say.
