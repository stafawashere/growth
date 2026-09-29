---
title: LSN-CON-08005 Position and velocity recovered from an initial value
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08005, a later position or velocity as the initial value plus the accumulated change, built from authoring_bundle("BC-CON-08005") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08005 Position and velocity recovered from an initial value

Concept BC-CON-08005 (skills BC-SKL-08009, BC-SKL-08010), topic 8.2 of Unit 8, hard parent BC-CON-08003 (docs/lessons/unit-08/README.md, section 1). The bundle lists BC-QA-06005 first (successor of the retired archetype id BC-SKL-08009 names) and BC-QA-08003.

## Prediction

Predict which expression gives x(3) for v(t) = 3t^2 - 4t + 5 meters per second with x(1) = 25 meters, before any rule is stated. Form: mcq, three options, key: the known value plus the integral. The rivals are the integral alone (BC-ERR-08011, BC-QA-06005 `wrong_approaches`) and the known value multiplied into the integral. The resolution states the change 20 and the ex-1 value 45, and says nothing about the reader's choice. Sources: BC-CON-08005 and the topic 8.2 section its key idea cites.

## Orientation

Served text, from BC-CON-08005 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals): a response writes the later value as the known value plus the definite integral of the rate, then adds. The integral alone is the change. No count, no frequency.

## Key ideas

Both skills map to BC-EK-CHA-4C1 (ced:153): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Recovering a value): with v continuous on [a, b] and the position known at a, the position at b is the position at a plus the integral of v over [a, b]; velocity from acceleration the same way. No anchor quote. Notation line from the concept record.

## Recognition

- BC-QA-06005 (family accumulation-with-initial-condition; research/question-analysis/question-archetypes.md#BC-QA-06005 Net change from a rate with an initial condition): `typical_wording` "find the value of the modelled quantity at the later time and show the setup for the calculations"; `common_givens` a rate function and a known value of the quantity at one time; `asked_to_produce` an integral expression with the initial value, a numerical value with units. Official parts include BC-FRQ-2019-Q1-A, 2024-Q1-C, 2026-Q1-C.
- BC-QA-08003 (research/question-analysis/question-archetypes.md#BC-QA-08003 Rectilinear motion analysed with definite integrals): "find the position of the particle at the later time", with an initial position among the `common_givens`.

The signal: a stated value at one time and a request for the value, not the change, at another. What says "not this concept": "displacement", "change in", "how much entered" (the integral alone).

The near miss for the contrast pair is the net change alone, the rival of BC-QA-06005 and the subject of BC-CON-08003 (a sibling concept): it gives the same rate and interval and asks for the change, so the integral is the whole answer.

## Method choice

- st-1, BC-QA-06005 (both bands). Method, `expected_solution_path[0]`: the value at the later input as the value at the earlier input plus the definite integral of the rate. Rival, `wrong_approaches`: reporting the net change as the amount. Separating feature: a known value is given and a value is asked.
- st-2, BC-QA-08003 (low band). Method: classify the requested quantity; a position uses the initial condition. Rival: integrating velocity and taking the absolute value of the result. Separating feature: a position keeps the sign of v.

Both archetypes carry `asked_to_produce` and `common_givens`; neither block is tagged inferred.

Contrast pair on st-1. This: a BC-QA-06005 stem with a stated Q(0) asking for Q at the later time. Not this: the same rate with the net change over the interval asked. The feature is a stated start with a value asked.

## Solution path

- ex-1, BC-QA-06005, both bands, no calculator. Draw: cubic 1, square -2, linear 5, start 1, span 2, known 25, base_rate 5, swing 1, stretch 3, horizon 3, context tank, tool exact, direction forward; the rate is \(3t^2-4t+5\) on [1, 3]. The constraints hold, including distinct exact options (45, 20, 41, 49). The example frames the rate as a velocity and the known value as a position; the draw's context label is the archetype's, and the motion framing is listed inferred. No published item carries this draw.
- Steps: the setup (new, tagged BC-PT-99033); the integral's value in place (equivalent); the answer (equivalent, tagged BC-PT-99004). A fluent solver writes all three.

## Scoring

BC-QA-06005 lists BC-PT-99001, 99004, 99069, 99002, 99033, 99003. ex-1 tags BC-PT-99033 and BC-PT-99004; the lines are `reader_checks` output. The scoring pattern: the integral value presented without the initial condition does not earn the initial condition point (sg-24:3, sg-24:4); for a position, a point each for the integral, the initial condition and the answer (sg-24:7).

Scoring change of 2026-09-29: the answer point BC-PT-99004 is earned on step 3 but no longer tagged, so only the initial condition line BC-PT-99033 is served.

## Traps

One active error, BC-ERR-08011, both bands, on ex-1's draw: 20 reported as the position. Possible reason, words from BC-MIS-08006.

## Representations

None. The topic's Representations paragraph offers no figure-shaped conversion for a value recovered from an initial condition.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` and `failure_signature`.

## Time

BC-QA-06005 is `either`, so Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred]. The minutes go on the antiderivative evaluated at both limits.

## Checks

- chk-1, completion of ex-1, both bands. Key 45.
- chk-2, isomorph, both bands, backward direction. Draw: cubic 0, square 3, linear 1, start 1, span 2, known 60, direction backward; x(3) = 60 with velocity \(6t+1\), find x(1). Key 34.
- No chk-3: one error in the bundle (listed inferred).

## Delivery

- orientation, ki-1: text. Rule 6: BC-REP-01 and 05 on the skills; the unit README's delivery map names text.
- ex-1, err-BC-ERR-08011: step_reveal. Rule 1.

Figure presence: no delivery entry is drawn, so the record carries `no_figure_reason`. No skill of BC-CON-08005 carries a figure-bearing representation (BC-REP-01 and 05 only), and ki-1 is one symbolic relation with no process. Rules 2 to 5 do not apply.

## Band plan

The served order of 2026-09-29: prediction, orientation, bridges, key ideas, strategy with the contrast pair, example 1 and its scoring lines, check 1, error blocks, example 2 faded when present, check 2, representations, check 3.

- Low (full): orientation, ki-1, st-1 with the contrast pair, st-2, ex-1 with its scoring line, err-BC-ERR-08011, chk-1, chk-2, the bridge, with the prediction first. 459 words, 3.1 minutes (cap 900 and 6).
- Mid (brief): the same blocks without st-2. 411 words, 2.8 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-08011, ex-1.

## Sources

- BC-CON-08005; BC-SKL-08009, BC-SKL-08010; BC-EK-CHA-4C1; ced:153
- BC-QA-06005, BC-QA-08003; BC-PT-99033, BC-PT-99004; sg-24:3, sg-24:4, sg-24:7
- BC-ERR-08011; BC-MIS-08006
- BC-PRQ-06005
- research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals
- research/question-analysis/question-archetypes.md#BC-QA-06005 Net change from a rate with an initial condition
- research/question-analysis/question-archetypes.md#BC-QA-08003 Rectilinear motion analysed with definite integrals
- research/exam/exam-structure.md#Section and part layout
- [inferred] Exam part I-A for an "either" archetype. Settled by the item mix.
- [inferred] The motion framing on a BC-QA-06005 draw. Settled by a motion context value in BC-QA-06005's parameter_spec, or an initial position parameter in BC-QA-08003's.
- [inferred] Two checks only. Settled by further active errors on BC-SKL-08009 or BC-SKL-08010.
- [inferred] pr-1 and the st-1 contrast pair are authored for the redesign. Settled by the pretest and contrast measurements in the build plan.
- [inferred] No drawn block. Settled by a figure-bearing representation on BC-SKL-08009 or BC-SKL-08010.
- [inferred] BC-PT-99004 untagged on ex-1 step 3 to hold the brief cap, the last resort after the orientation, key idea, strategy and contrast were shortened. Settled by a brief band cap that admits two reader lines.

## Machine record

```json
{
 "id": "LSN-CON-08005",
 "kind": "concept",
 "target_id": "BC-CON-08005",
 "unit": "08",
 "skills": ["BC-SKL-08009", "BC-SKL-08010"],
 "prediction": {"id": "pr-1", "stem": {"text": "Predict: v(t) = 3t^2 - 4t + 5 and x(1) = 25. Which gives x(3)?", "command_verb": "predict"}, "format": "mcq", "options": [{"id": "A", "label": "The integral of v from 1 to 3", "is_key": false}, {"id": "B", "label": "25 plus the integral of v from 1 to 3", "is_key": true}, {"id": "C", "label": "25 times the integral of v from 1 to 3", "is_key": false}], "resolution": "The integral of v from 1 to 3 is the change in position, 20 meters. Adding the known 25 gives x(3) = 45.", "sources": ["BC-CON-08005", "research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals"]},
 "no_figure_reason": "The topic offers no figure-shaped conversion for a value recovered from an initial condition, and no skill carries a figure-bearing representation. The key idea is one symbolic relation with no process.",
 "orientation": {"text": "A response adds the known value to the integral of the rate.", "sources": ["BC-CON-08005", "research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals"]},
 "key_ideas": [
  {"id": "ki-1", "ek_id": "BC-EK-CHA-4C1", "depth": "core", "text": "The position at b is the position at a plus the integral of v over [a, b].", "notation": "s(b) = s(a) + integral of v", "quote": null, "sources": ["BC-EK-CHA-4C1", "ced:153", "research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals"]}
 ],
 "strategy": [
  {"id": "st-1", "archetype_id": "BC-QA-06005", "cue": "A rate and a known value; a later value is asked.", "method": "Known value plus the definite integral of the rate.", "rival": "Reporting the net change as the amount.", "separating_feature": "A value, not a change, is asked.", "sources": ["BC-QA-06005"], "evidence_tag": "verified", "contrast": {"this": {"text": "R(t) = 3t^2 + 2 is the rate of Q, with Q(0) = 10. Find Q(4).", "archetype_id": "BC-QA-06005"}, "not_this": {"text": "R(t) = 3t^2 + 2 is the rate of Q. Find the net change in Q on [0, 4].", "why_not": "It asks for the change alone."}, "feature": "Start given, value asked: add the start."}},
  {"id": "st-2", "archetype_id": "BC-QA-08003", "cue": "A velocity, an initial position and a time interval; the position at a later time is asked.", "method": "Classify the requested quantity. A position uses the initial condition.", "rival": "Integrating velocity and taking the absolute value of the result.", "separating_feature": "A position keeps the sign of v and adds the start.", "sources": ["BC-QA-08003"], "evidence_tag": "verified"}
 ],
 "worked_examples": [
  {"id": "ex-1", "archetype_id": "BC-QA-06005", "bands": ["low", "mid"], "parameter_draw": {"cubic": 1, "square": -2, "linear": 5, "start": 1, "span": 2, "known": 25, "base_rate": 5, "swing": 1, "stretch": 3, "horizon": 3, "context": "tank", "tool": "exact", "direction": "forward"}, "problem": {"text": "A particle has velocity v(t) = 3t^2 - 4t + 5 meters per second, and x(1) = 25 meters. Find x(3), showing the setup.", "command_verb": "find"}, "calculator_status": "no_calculator", "steps": [{"cue": "A position at t = 3 from a known position at t = 1.", "why": "The integral is the change; the start is added.", "expr": "25 + Integral(3*t**2 - 4*t + 5, (t, 1, 3))", "relation": "new", "point_type_id": "BC-PT-99033"}, {"cue": "No calculator: t^3 - 2t^2 + 5t from 1 to 3.", "why": "24 - 4 = 20 meters of change.", "expr": "25 + 20", "relation": "equivalent"}, {"cue": "Add the known value.", "why": "Meters: the position at t = 3.", "expr": "45", "relation": "equivalent"}], "answer": {"form": "symbolic", "expr": "45"}}
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99033"], "lines": [{"point_type_id": "BC-PT-99033", "text": "Uses the initial condition in an accumulation expression. Earned by: Adding the known function value at one endpoint to a definite integral of the rate (sg-24:3, sg-22:8). Not earned by: A definite integral alone with the known value never added (sg-22:8). Notation: sg-22:8 lists cases where a missing differential shifts which of the three points are available."}]}
 ],
 "common_errors": [
  {"error_id": "BC-ERR-08011", "observed_behavior": "The response evaluates the integral of the rate and reports it as the value of the quantity.", "scoring_consequence": "The initial condition point is lost and the answer point falls with it (sg-24:7).", "wrong_step": {"text": "The integral alone, 20.", "expr": "Integral(3*t**2 - 4*t + 5, (t, 1, 3))"}, "right_step": {"text": "25 plus the integral.", "expr": "25 + Integral(3*t**2 - 4*t + 5, (t, 1, 3))"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-08006", "text": "reads an accumulation integral as the quantity itself rather than as the change in it"}, "sources": ["BC-ERR-08011", "BC-MIS-08006"], "fix_prompt": true}
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "x(1) = 25 is the value at input 1, not at 3."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 3]}, "skipped_steps": {"ex-1": []}},
 "checks": [
  {"id": "chk-1", "check_kind": "completion", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-06005", "parameter_draw": {"cubic": 1, "square": -2, "linear": 5, "start": 1, "span": 2, "known": 25, "base_rate": 5, "swing": 1, "stretch": 3, "horizon": 3, "context": "tank", "tool": "exact", "direction": "forward"}, "completes": "ex-1", "stem": {"text": "x(1) = 25, and the integral of v from 1 to 3 is 20. Find x(3).", "command_verb": "find"}, "key": {"form": "symbolic", "expr": "45"}, "steps": [{"text": "Known value plus change.", "expr": "25 + 20", "relation": "new"}, {"text": "Add.", "expr": "45", "relation": "equivalent"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-08009"]},
  {"id": "chk-2", "check_kind": "isomorph", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-06005", "parameter_draw": {"cubic": 0, "square": 3, "linear": 1, "start": 1, "span": 2, "known": 60, "base_rate": 5, "swing": 1, "stretch": 3, "horizon": 3, "context": "tank", "tool": "exact", "direction": "backward"}, "stem": {"text": "v(t) = 6t + 1 and x(3) = 60. Find x(1).", "command_verb": "find"}, "key": {"form": "symbolic", "expr": "34"}, "steps": [{"text": "Known value minus the change from 1 to 3.", "expr": "60 - Integral(6*t + 1, (t, 1, 3))", "relation": "new"}, {"text": "60 - 26.", "expr": "34", "relation": "equivalent"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-08009"]}
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: BC-REP-01 and 05 on the skills, none figure-bearing", "sources": ["BC-SKL-08009"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 6: a symbolic relation; the unit README delivery map names text", "sources": ["BC-SKL-08009", "BC-SKL-08010"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08011", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-08011", "ex-1"],
 "read_minutes": {"full": 3.1, "brief": 2.8},
 "word_count": {"full": 459, "brief": 411},
 "research_lines": [
  {"file": "research/units/unit-08-applications-integration.md", "line": "the position at b is the position at a plus the definite integral of v over [a,b]"}
 ],
 "inferred": [
  {"claim": "BC-QA-06005 is an either archetype, so the lesson takes Section I Part A and a no calculator example.", "settles": "The exam part mix the archetype is served in."},
  {"claim": "The example frames a BC-QA-06005 draw as a velocity and a position, though the draw's context label is tank.", "settles": "A motion context value in BC-QA-06005's parameter_spec, or an initial position parameter in BC-QA-08003's."},
  {"claim": "The lesson carries two checks: the bundle holds one error, fewer than the three distractors a 4-option MCQ needs.", "settles": "Further active BC-ERR records on BC-SKL-08009 or BC-SKL-08010."},
  {"claim": "BC-PT-99004 is earned on ex-1 step 3 but not tagged, because its reader line would take the brief band past 450 words.", "settles": "A brief band cap that admits two reader lines, or a shorter BC-PT-99004 reader line."}
 ],
 "sources": ["BC-CON-08005", "BC-SKL-08009", "BC-SKL-08010", "BC-EK-CHA-4C1", "ced:153", "BC-QA-06005", "BC-QA-08003", "BC-PT-99033", "BC-PT-99004", "sg-24:3", "sg-24:4", "sg-24:7", "BC-ERR-08011", "BC-MIS-08006", "BC-PRQ-06005", "research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals", "research/question-analysis/question-archetypes.md#BC-QA-06005 Net change from a rate with an initial condition", "research/exam/exam-structure.md#Section and part layout"]
}
```
