---
title: LSN-CON-08004 Total distance as the definite integral of speed
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08004, total distance as the definite integral of speed split where velocity changes sign, built from authoring_bundle("BC-CON-08004") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08004 Total distance as the definite integral of speed

Concept BC-CON-08004 (skills BC-SKL-08007, BC-SKL-08008, BC-SKL-08011), topic 8.2 of Unit 8, hard parent BC-CON-08003 (docs/lessons/unit-08/README.md, section 1). One archetype, BC-QA-08003. BC-SKL-08008 and BC-SKL-08011 are members of LSN-DEC-08-01 with BC-SKL-08006; the decision lesson follows this one (docs/lessons/unit-08/README.md, section 3).

## Prediction

Predict which expression gives the total distance of a particle with v(t) = 2t^2 - 10t + 8 meters per second on [0, 5], before any rule is stated. Form: mcq, three options, key: the integral of speed. The rivals are the signed integral (BC-ERR-08009) and one absolute value taken at the end (BC-ERR-08010, BC-QA-08003 `wrong_approaches`). The resolution names the split at 1 and 4 and the ex-1 value 49/3, and says nothing about the reader's choice. Sources: BC-CON-08004 and the topic 8.2 section its key idea cites.

## Orientation

Served text, from BC-CON-08004 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals): a response integrates speed, the absolute value of velocity, and by hand splits the interval where velocity changes sign and adds the sizes of the pieces. No count, no frequency.

## Key ideas

All three skills map to BC-EK-CHA-4C1 (ced:153): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Total distance, Notation): the integral of speed over [a, b] is the total distance; where v keeps one sign the two totals agree up to sign, where it changes sign they differ; by hand, the zeros of v cut the interval. No anchor quote. Notation line from the concept record.

## Recognition

BC-QA-08003 (research/question-analysis/question-archetypes.md#BC-QA-08003 Rectilinear motion analysed with definite integrals): `typical_wording` "find the total distance travelled by the particle over the stated time interval and show the setup"; `common_givens` a velocity function or graph, a time interval; `asked_to_produce` a definite integral, a numerical value with units. The signal is "total distance traveled"; the feature that changes the work is a velocity that changes sign inside the interval (`difficulty_variables`). MCQ BC-MCQ-SAMPLE-016, BC-MCQ-PE2012-042; no free response `official_examples` in the record.

What says "not this concept": "displacement" or "change in position" (BC-CON-08003); a position at a later time (BC-CON-08005).

The near miss for the contrast pair is a BC-QA-04003 stem, whose `typical_wording` is "is the speed of the particle increasing, decreasing, or neither at the stated time, and give a reason" (research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed): the same velocity, asked about one instant, so the signs of v and its derivative there decide it and nothing is integrated.

## Method choice

One strategy block, both bands. st-1, BC-QA-08003. Method, `expected_solution_path[0]`: classify the requested quantity, then the integral of |v|. Rival, `wrong_approaches`: integrating velocity and taking the absolute value of the result. Separating feature: v changes sign inside the interval, so pieces cancel inside one signed integral. Not tagged inferred.

Contrast pair on st-1. This: a BC-QA-08003 stem asking for total distance traveled. Not this: a BC-QA-04003 stem asking whether the speed is increasing at one time. The feature is an interval against a single instant.

## Solution path

- ex-1, BC-QA-08003, both bands, no calculator. Draw: size 2, right_first, first_zero 1, gap 3, overrun 1, context particle, units meters, framing bare, so \(v(t)=2(t-1)(t-4)\) on [0, 5]. The right_first constraint holds (net_shape -5/6 < 0). No published item carries this draw.
- Steps: the speed integral (new); v = 0 (new); its roots (solve); the split pieces (new); the sum (equivalent). A fluent solver writes the speed integral, the roots and the sum.

## Scoring

BC-QA-08003 lists no `point_types`: no what_a_reader_scores entry, no point tag (plan 15, R14).

## Traps

Three active errors, in the bundle's order: BC-ERR-08009, BC-ERR-08010, BC-ERR-99010. Low band all three, mid band the first two. On ex-1's draw.

- err-BC-ERR-08009: v integrated as it stands, value -5/3. Possible reason, words from BC-MIS-08005.
- err-BC-ERR-08010: one absolute value at the end, 5/3. Possible reason, words from BC-MIS-08004.
- err-BC-ERR-99010: split only at t = 1, 9. No possible reason line: the linked descriptions do not name the split.

## Representations

None as a separate block; ki-1's figure carries the topic's velocity graph to unsigned area conversion.

## Prerequisite bridge

- BC-PRQ-06005, BC-PRQ-08001, BC-PRQ-08003, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-08003 is `either`, so Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred]. The minutes go on the three pieces.

## Checks

- chk-1, completion of ex-1, both bands: the split pieces are given; the student adds sizes. Key 49/3.
- chk-2, isomorph, both bands. Draw: size 1, left_first, first_zero 2, gap 2, overrun 1/2; \(v(t)=-(t-2)(t-4)\) on [0, 9/2]. Key 199/24.
- chk-3, MCQ, low band. Draw: size 1, right_first, first_zero 1, gap 4, overrun 3/2; \(v(t)=(t-1)(t-5)\) on [0, 13/2]. Key 149/8. Distractors -65/24 (BC-ERR-08009), 65/24 (BC-ERR-08010), 59/8 (BC-ERR-99010), the three the archetype's template derives.

## Delivery

- orientation: text. Rule 6.
- ki-1: figure. Rule 4: BC-REP-02 on BC-SKL-08008; the unit README's delivery map (the negative piece reflected, the zeros marked). Not promoted: BC-QA-08003 `difficulty_variables` are presence flags [inferred; settled by the modality A/B].
- ex-1 and the three error blocks: step_reveal. Rule 1.

Figure presence: ki-1 is already a drawn block, so no `no_figure_reason` is carried. The redesign changes no delivery entry here.

## Band plan

The served order of 2026-09-29: prediction, orientation, bridges, key ideas, strategy with the contrast pair, example 1 and its scoring lines, check 1, error blocks, example 2 faded when present, check 2, representations, check 3.

- Low (full): orientation, ki-1, st-1 with the contrast pair, ex-1, three error blocks, chk-1 to chk-3, three bridges, with the prediction first. 489 words, 3.3 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1 with the contrast pair, ex-1, err-BC-ERR-08009, err-BC-ERR-08010, chk-1, chk-2, three bridges, with the prediction first. 424 words, 2.83 minutes (cap 450 and 3).
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-08004; BC-SKL-08007, BC-SKL-08008, BC-SKL-08011; BC-EK-CHA-4C1; ced:153
- BC-QA-08003
- BC-ERR-08009, BC-ERR-08010, BC-ERR-99010; BC-MIS-08005, BC-MIS-08004
- BC-PRQ-06005, BC-PRQ-08001, BC-PRQ-08003
- research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals
- research/question-analysis/question-archetypes.md#BC-QA-08003 Rectilinear motion analysed with definite integrals
- research/exam/exam-structure.md#Section and part layout
- [inferred] Exam part I-A for an "either" archetype. Settled by the item mix.
- [inferred] ki-1 as a static figure. Settled by the modality A/B.
- [inferred] pr-1 and the st-1 contrast pair are authored for the redesign. Settled by the pretest and contrast measurements in the build plan.
- research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed

## Machine record

```json
{
 "id": "LSN-CON-08004",
 "kind": "concept",
 "target_id": "BC-CON-08004",
 "unit": "08",
 "skills": ["BC-SKL-08007", "BC-SKL-08008", "BC-SKL-08011"],
 "prediction": {"id": "pr-1", "stem": {"text": "v(t) = 2t^2 - 10t + 8 meters per second. Which gives the total distance over [0, 5]?", "command_verb": "predict"}, "format": "mcq", "options": [{"id": "A", "label": "The integral of v over [0, 5]", "is_key": false}, {"id": "B", "label": "The absolute value of the integral of v", "is_key": false}, {"id": "C", "label": "The integral of the speed over [0, 5]", "is_key": true}], "resolution": "Total distance is the integral of speed, |v|. Here v is negative on (1, 4), so the split is at 1 and 4, giving 49/3 meters.", "sources": ["BC-CON-08004", "research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals"]},
 "orientation": {"text": "A response integrates speed, |v|, splitting at sign changes of v when done by hand.", "sources": ["BC-CON-08004", "research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals"]},
 "key_ideas": [
  {"id": "ki-1", "ek_id": "BC-EK-CHA-4C1", "depth": "core", "text": "Total distance is the integral of |v| over [a, b]. By hand, the zeros of v cut the interval and each piece counts as positive.", "notation": "total distance", "quote": null, "sources": ["BC-EK-CHA-4C1", "ced:153", "research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals"]}
 ],
 "strategy": [
  {"id": "st-1", "archetype_id": "BC-QA-08003", "cue": "Total distance traveled from a velocity and an interval.", "method": "Classify the quantity. Total distance: the integral of |v|.", "rival": "The absolute value of the integral of v.", "separating_feature": "v changes sign inside the interval.", "sources": ["BC-QA-08003", "BC-QA-04003"], "evidence_tag": "verified", "contrast": {"this": {"text": "Velocity is v(t) = t^2 - 7t + 10. Find the total distance traveled over [0, 6].", "archetype_id": "BC-QA-08003"}, "not_this": {"text": "Velocity is v(t) = t^2 - 7t + 10. Is the speed increasing at t = 3?", "why_not": "One instant: compare the signs of v(3) and a(3)."}, "feature": "Total distance integrates |v| over an interval; one instant compares signs."}}
 ],
 "worked_examples": [
  {"id": "ex-1", "archetype_id": "BC-QA-08003", "bands": ["low", "mid"], "parameter_draw": {"size": 2, "direction": "right_first", "first_zero": 1, "gap": 3, "overrun": "1", "context": "particle", "units": "meters", "framing": "bare"}, "problem": {"text": "A particle moves on the x-axis with v(t) = 2t^2 - 10t + 8 meters per second. Find the total distance it travels over [0, 5].", "command_verb": "find"}, "calculator_status": "no_calculator", "steps": [{"cue": "Total distance traveled: the integral of speed.", "why": "Every stretch counts as positive.", "expr": "Integral(Abs(2*t**2 - 10*t + 8), (t, 0, 5))", "relation": "new"}, {"cue": "No calculator, so |v| is split where v changes sign.", "why": "v = 2(t - 1)(t - 4).", "expr": "2*t**2 - 10*t + 8 = 0", "relation": "new"}, {"cue": "Zeros inside [0, 5].", "why": "Sign changes at 1 and 4: three pieces.", "expr": "FiniteSet(1, 4)", "relation": "solve", "variable": "t"}, {"cue": "v is negative on [1, 4], so that piece is reversed.", "why": "Pieces 11/3, 9, 11/3.", "expr": "Integral(2*t**2 - 10*t + 8, (t, 0, 1)) - Integral(2*t**2 - 10*t + 8, (t, 1, 4)) + Integral(2*t**2 - 10*t + 8, (t, 4, 5))", "relation": "new"}, {"cue": "Add the sizes.", "why": "Meters.", "expr": "49/3", "relation": "equivalent"}], "answer": {"form": "symbolic", "expr": "49/3"}}
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {"error_id": "BC-ERR-08009", "observed_behavior": "The integrand for total distance is the velocity itself rather than its absolute value.", "scoring_consequence": "The setup point is lost.", "wrong_step": {"text": "v as the integrand.", "expr": "Integral(2*t**2 - 10*t + 8, (t, 0, 5))"}, "right_step": {"text": "|v| as the integrand.", "expr": "Integral(Abs(2*t**2 - 10*t + 8), (t, 0, 5))"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-08005", "text": "does not attach the absolute value to speed"}, "sources": ["BC-ERR-08009", "BC-MIS-08005"], "fix_prompt": true},
  {"error_id": "BC-ERR-08010", "observed_behavior": "The response integrates velocity over the whole interval and takes one absolute value at the end.", "scoring_consequence": "The value is too small, so the answer point is lost.", "wrong_step": {"text": "One absolute value at the end.", "expr": "Abs(Integral(2*t**2 - 10*t + 8, (t, 0, 5)))"}, "right_step": {"text": "Sizes of the three pieces.", "expr": "49/3"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-08004", "text": "treats the integral of velocity as the length of the trip"}, "sources": ["BC-ERR-08010", "BC-MIS-08004"], "fix_prompt": true},
  {"error_id": "BC-ERR-99010", "observed_behavior": "Responses integrate velocity without an absolute value, or split the interval incorrectly, and report the net change as the total distance travelled.", "scoring_consequence": "The setup point for total distance is not earned; the numerical answer point follows the setup.", "wrong_step": {"text": "Split only at t = 1.", "expr": "11/3 + Abs(-9 + 11/3)"}, "right_step": {"text": "Split at 1 and 4.", "expr": "11/3 + 9 + 11/3"}, "relation": "distinct", "possible_reason": null, "sources": ["BC-ERR-99010"], "fix_prompt": true}
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "v(t) is velocity at time t."},
  {"prq_id": "BC-PRQ-08001", "text": "Solve v(t) = 0 for every root."},
  {"prq_id": "BC-PRQ-08003", "text": "|v| is v where v is at least 0, otherwise -v."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 3, 5]}, "skipped_steps": {"ex-1": [2, 4]}},
 "checks": [
  {"id": "chk-1", "check_kind": "completion", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-08003", "parameter_draw": {"size": 2, "direction": "right_first", "first_zero": 1, "gap": 3, "overrun": "1", "context": "particle", "units": "meters", "framing": "bare"}, "completes": "ex-1", "stem": {"text": "The pieces of v on [0, 1], [1, 4], [4, 5] are 11/3, -9, 11/3. Find the total distance.", "command_verb": "find"}, "key": {"form": "symbolic", "expr": "49/3"}, "steps": [{"text": "Sizes of the pieces.", "expr": "Abs(11/3) + Abs(-9) + Abs(11/3)", "relation": "new"}, {"text": "Sum.", "expr": "49/3", "relation": "equivalent"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-08007", "BC-SKL-08008"]},
  {"id": "chk-2", "check_kind": "isomorph", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-08003", "parameter_draw": {"size": 1, "direction": "left_first", "first_zero": 2, "gap": 2, "overrun": "1/2", "context": "bead", "units": "feet", "framing": "bare"}, "stem": {"text": "v(t) = -t^2 + 6t - 8. Find the total distance traveled over [0, 9/2].", "command_verb": "find"}, "key": {"form": "symbolic", "expr": "199/24"}, "steps": [{"text": "Split at 2 and 4, negative pieces reversed.", "expr": "-Integral(-t**2 + 6*t - 8, (t, 0, 2)) + Integral(-t**2 + 6*t - 8, (t, 2, 4)) - Integral(-t**2 + 6*t - 8, (t, 4, 9/2))", "relation": "new"}, {"text": "Sum.", "expr": "199/24", "relation": "equivalent"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-08007", "BC-SKL-08008"]},
  {"id": "chk-3", "check_kind": "mcq", "format": "mcq", "bands": ["low"], "archetype_id": "BC-QA-08003", "parameter_draw": {"size": 1, "direction": "right_first", "first_zero": 1, "gap": 4, "overrun": "3/2", "context": "cart", "units": "meters", "framing": "bare"}, "stem": {"text": "v(t) = t^2 - 6t + 5. Which is the total distance traveled over [0, 13/2]?", "command_verb": "identify"}, "key": {"form": "symbolic", "expr": "149/8"}, "steps": [{"text": "Split at 1 and 5, the middle piece reversed.", "expr": "Integral(t**2 - 6*t + 5, (t, 0, 1)) - Integral(t**2 - 6*t + 5, (t, 1, 5)) + Integral(t**2 - 6*t + 5, (t, 5, 13/2))", "relation": "new"}, {"text": "Sum.", "expr": "149/8", "relation": "equivalent"}], "options": [{"id": "A", "is_key": false, "expr": "-65/24", "error_path": "BC-ERR-08009", "derivation": "v itself integrated over [0, 13/2]"}, {"id": "B", "is_key": false, "expr": "65/24", "error_path": "BC-ERR-08010", "derivation": "one absolute value taken at the end"}, {"id": "C", "is_key": true, "expr": "149/8", "error_path": null}, {"id": "D", "is_key": false, "expr": "59/8", "error_path": "BC-ERR-99010", "derivation": "split only at t = 1, so the last two pieces net"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-08007", "BC-SKL-08008"]}
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: a statement of what a response shows", "sources": ["BC-SKL-08007"]},
  {"block": "ki-1", "mode": "figure", "reason": "rule 4: BC-REP-02 on BC-SKL-08008; unit README delivery map; not promoted, BC-QA-08003 difficulty_variables are presence flags", "sources": ["BC-SKL-08008", "BC-QA-08003"], "spec": {"kind": "graph", "representations": ["BC-REP-02"], "window": {"x": [0, 5], "y": [-5, 9]}, "curves": [{"expr": "2*t**2 - 10*t + 8", "domain": [0, 5], "style": "dashed"}, {"expr": "Abs(2*t**2 - 10*t + 8)", "domain": [0, 5]}], "points": [{"at": [1, 0]}, {"at": [4, 0]}], "labels": [{"text": "v(t)", "placement": "inside"}, {"text": "|v(t)|: the negative piece reflected", "placement": "inside"}, {"text": "split at t = 1 and t = 4", "placement": "inside"}]}, "fallback": "the same graph, static, with v dashed, |v| solid, the zeros marked and the labels inside", "keyboard": "no control; the figure description is reached with Tab"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08009", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08010", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99010", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-08009", "err-BC-ERR-08010", "err-BC-ERR-99010", "ex-1"],
 "read_minutes": {"full": 3.3, "brief": 2.83},
 "word_count": {"full": 488, "brief": 423},
 "research_lines": [
  {"file": "research/units/unit-08-applications-integration.md", "line": "Where velocity keeps one sign the two quantities agree up to sign, and where velocity changes sign they differ"}
 ],
 "inferred": [
  {"claim": "BC-QA-08003 is an either archetype, so the lesson takes Section I Part A and a no calculator example.", "settles": "The exam part mix the archetype is served in."},
  {"claim": "ki-1 is served as a static figure with the negative piece reflected.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-08004", "BC-SKL-08007", "BC-SKL-08008", "BC-SKL-08011", "BC-EK-CHA-4C1", "ced:153", "BC-QA-08003", "BC-QA-04003", "BC-ERR-08009", "BC-ERR-08010", "BC-ERR-99010", "BC-MIS-08005", "BC-MIS-08004", "BC-PRQ-06005", "BC-PRQ-08001", "BC-PRQ-08003", "research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals", "research/question-analysis/question-archetypes.md#BC-QA-08003 Rectilinear motion analysed with definite integrals", "research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed", "research/exam/exam-structure.md#Section and part layout"]
}
```
