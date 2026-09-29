---
title: LSN-CON-08003 Displacement as the definite integral of velocity
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08003, displacement as the signed definite integral of velocity, built from authoring_bundle("BC-CON-08003") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08003 Displacement as the definite integral of velocity

Concept BC-CON-08003 (skill BC-SKL-08006), topic 8.2 of Unit 8, first in the motion strand with no Unit 8 hard parent (docs/lessons/unit-08/README.md, section 1). One archetype loads the skill, BC-QA-08003 (family motion-by-accumulation). BC-SKL-08006 is a member of the confusable set LSN-DEC-08-01 (displacement against total distance on BC-QA-08003), taught after LSN-CON-08004 (docs/lessons/unit-08/README.md, section 3).

## Orientation

Served text, from BC-CON-08003 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals): a response integrates velocity itself over the stated interval, keeps the sign, and names the result displacement, not distance. No count, no frequency.

## Key ideas

BC-SKL-08006 maps to BC-EK-CHA-4C1 (ced:153): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Displacement, Notation): the integral of velocity over [a, b] is the displacement; a stretch where v is negative subtracts; a negative result is net movement in the negative direction; the quantity is named displacement. No anchor quote. Notation line from the concept record.

## Recognition

BC-QA-08003 (research/question-analysis/question-archetypes.md#BC-QA-08003 Rectilinear motion analysed with definite integrals): `typical_wording` "find the total distance travelled by the particle over the stated time interval", "find the position of the particle at the later time"; `common_givens` a velocity function or graph, an initial position, a time interval; `asked_to_produce` a definite integral, a numerical value with units. The signal for this concept is the word "displacement" or "change in position" beside a velocity. Shapes: a single MCQ (BC-MCQ-SAMPLE-016, BC-MCQ-PE2012-042) or two or three parts of a free response question; the record lists no free response `official_examples`.

What says "not this concept": "total distance traveled" (BC-CON-08004, the absolute value of v); "the position at time b" with a stated position (BC-CON-08005, the initial value added).

## Method choice

One strategy block, both bands. st-1, BC-QA-08003. Method, `expected_solution_path[0]`: classify the requested quantity. Rival, `wrong_approaches`: integrating velocity and taking the absolute value of the result. Separating feature: displacement keeps the sign; only total distance removes it. The archetype carries `asked_to_produce` and `common_givens`, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-08003, both bands, no calculator. Draw: size 1, direction left_first, first_zero 1, gap 2, overrun 1/2, context particle, units meters, framing bare, so \(v(t)=-(t-1)(t-3)\) on [0, 7/2]. The constraint for left_first holds (net_shape 7/24 > 0, middle_shape 4/3 > last_shape 7/24). The template's item asks for total distance; this example asks for displacement on the same draw, which the archetype's `description` covers. No published item carries this draw.
- Steps: classify (no value); the integral (new); its value (equivalent). A fluent solver writes the integral and the value and classifies in the head.

## Scoring

BC-QA-08003 lists no `point_types`, so no what_a_reader_scores entry, no point tag, and the served text names no point beyond the error record's scoring_consequence (plan 15, R14).

## Traps

One active error meets the skill: err-BC-ERR-99010, shown on ex-1's draw as the displacement -7/24 reported where total distance, 71/24, was asked. Possible reason, words from BC-MIS-08004. Both bands.

## Representations

None as a separate block. The topic's Representations paragraph names velocity graph to signed and unsigned area (BC-REP-02 to BC-REP-01); ki-1's figure carries it.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` and `failure_signature`.

## Time

BC-QA-08003 is `either`, so the lesson takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: an "either" archetype takes I-A; settled by the item mix the archetype is served in]. The minutes go on the antiderivative evaluated at 7/2.

## Checks

- chk-1, completion of ex-1, both bands: the integral is given; the student evaluates. Key -7/24.
- chk-2, isomorph, both bands. Draw: size 2, right_first, first_zero 1, gap 4, overrun 1, context cart, units feet, framing context; \(v(t)=2(t-1)(t-5)\) on [0, 6]. Key -12.
- No chk-3: one error in the bundle, fewer than three distractors need (listed inferred).

## Delivery

- orientation: text. Rule 6.
- ki-1: figure. Rule 4 through the topic Representations paragraph, "velocity graph to signed and unsigned area", and the unit README's delivery map (signed velocity areas); BC-SKL-08006 itself carries BC-REP-01 and 05 [inferred; settled by the modality A/B].
- ex-1, err-BC-ERR-99010: step_reveal. Rule 1.

## Band plan

- Low (full) and mid (brief) serve the same blocks: orientation, ki-1, st-1, ex-1, err-BC-ERR-99010, chk-1, chk-2, the bridge. 293 words, 2.0 minutes in each band (caps 900 and 6, 450 and 3).
- Refresher: ki-1, err-BC-ERR-99010, ex-1.

## Sources

- BC-CON-08003; BC-SKL-08006; BC-EK-CHA-4C1; ced:153
- BC-QA-08003
- BC-ERR-99010; BC-MIS-08004
- BC-PRQ-06005
- research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals
- research/question-analysis/question-archetypes.md#BC-QA-08003 Rectilinear motion analysed with definite integrals
- research/exam/exam-structure.md#Section and part layout
- [inferred] Exam part I-A for an "either" archetype. Settled by the item mix.
- [inferred] ki-1 as a static figure. Settled by the modality A/B.
- [inferred] Two checks only. Settled by a second and third active error on BC-SKL-08006.

## Machine record

```json
{
 "id": "LSN-CON-08003",
 "kind": "concept",
 "target_id": "BC-CON-08003",
 "unit": "08",
 "skills": ["BC-SKL-08006"],
 "orientation": {
  "text": "A response integrates velocity itself over the stated interval, keeps the sign, and names the result displacement, the net change in position, not distance.",
  "sources": ["BC-CON-08003", "research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-4C1",
   "depth": "core",
   "text": "For a particle moving on a line, the integral of velocity over [a, b] is the displacement. Where v is negative the particle moves in the negative direction and that stretch subtracts. A negative displacement is net movement in the negative direction.",
   "notation": "displacement; net change in position",
   "quote": null,
   "sources": ["BC-EK-CHA-4C1", "ced:153", "research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08003",
   "cue": "A velocity function or graph and a time interval, with displacement or change in position asked.",
   "method": "First: classify the requested quantity. Displacement: the integral of v over the interval.",
   "rival": "Rival: integrating velocity and taking the absolute value of the result.",
   "separating_feature": "Displacement keeps the sign; only total distance removes it.",
   "sources": ["BC-QA-08003"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08003",
   "bands": ["low", "mid"],
   "parameter_draw": {"size": 1, "direction": "left_first", "first_zero": 1, "gap": 2, "overrun": "1/2", "context": "particle", "units": "meters", "framing": "bare"},
   "problem": {"text": "A particle moves on the x-axis with velocity v(t) = -t^2 + 4t - 3 meters per second. Find its displacement over [0, 7/2].", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "The stem says displacement.", "why": "Net change in position: velocity itself, sign kept."},
    {"cue": "Displacement over [0, 7/2] names the integral of v.", "why": "One integral; the left stretches subtract.", "expr": "Integral(-t**2 + 4*t - 3, (t, 0, 7/2))", "relation": "new"},
    {"cue": "No calculator: antiderivative at 7/2 minus at 0.", "why": "Meters; negative means net movement left.", "expr": "-7/24", "relation": "equivalent"}
   ],
   "answer": {"form": "symbolic", "expr": "-7/24"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-99010",
   "observed_behavior": "Responses integrate velocity without an absolute value, or split the interval incorrectly, and report the net change as the total distance travelled.",
   "scoring_consequence": "The setup point for total distance is not earned; the numerical answer point follows the setup.",
   "wrong_step": {"text": "Distance asked, -7/24 reported.", "expr": "-7/24"},
   "right_step": {"text": "Distance: 71/24.", "expr": "71/24"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08004", "text": "treats the integral of velocity as the length of the trip"},
   "sources": ["BC-ERR-99010", "BC-MIS-08004"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "v(t) is the rate the integral accumulates; reading position for velocity puts the wrong function inside."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 3]}, "skipped_steps": {"ex-1": [1]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08003",
   "parameter_draw": {"size": 1, "direction": "left_first", "first_zero": 1, "gap": 2, "overrun": "1/2", "context": "particle", "units": "meters", "framing": "bare"},
   "completes": "ex-1",
   "stem": {"text": "The displacement is the integral of -t^2 + 4t - 3 from 0 to 7/2. Evaluate it.", "command_verb": "evaluate"},
   "key": {"form": "symbolic", "expr": "-7/24"},
   "steps": [
    {"text": "The integral.", "expr": "Integral(-t**2 + 4*t - 3, (t, 0, 7/2))", "relation": "new"},
    {"text": "Its value.", "expr": "-7/24", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08006"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08003",
   "parameter_draw": {"size": 2, "direction": "right_first", "first_zero": 1, "gap": 4, "overrun": "1", "context": "cart", "units": "feet", "framing": "context"},
   "stem": {"text": "A cart's velocity is v(t) = 2t^2 - 12t + 10 feet per second. Find its displacement over [0, 6].", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "-12"},
   "steps": [
    {"text": "The integral.", "expr": "Integral(2*t**2 - 12*t + 10, (t, 0, 6))", "relation": "new"},
    {"text": "Its value.", "expr": "-12", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08006"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: a statement of what a response shows", "sources": ["BC-SKL-08006"]},
  {"block": "ki-1", "mode": "figure", "reason": "rule 4 through the topic Representations paragraph, velocity graph to signed and unsigned area (BC-REP-02 to BC-REP-01); unit README delivery map", "sources": ["BC-SKL-08006", "BC-QA-08003"],
   "spec": {"kind": "graph", "representations": ["BC-REP-02"], "window": {"x": [0, 3.5], "y": [-3.5, 1.5]},
    "curves": [{"expr": "-t**2 + 4*t - 3", "domain": [0, 3.5]}],
    "shaded": [{"between": ["-t**2 + 4*t - 3", "0"], "domain": [0, 1], "sign": "negative"}, {"between": ["-t**2 + 4*t - 3", "0"], "domain": [1, 3], "sign": "positive"}, {"between": ["-t**2 + 4*t - 3", "0"], "domain": [3, 3.5], "sign": "negative"}],
    "labels": [{"text": "-4/3", "placement": "inside"}, {"text": "+4/3", "placement": "inside"}, {"text": "-7/24", "placement": "inside"}, {"text": "sum: displacement -7/24", "placement": "inside"}]},
   "fallback": "the same graph, static, with the three signed areas and the sum labelled inside", "keyboard": "no control; the figure description is reached with Tab"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99010", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-99010", "ex-1"],
 "read_minutes": {"full": 2.0, "brief": 2.0},
 "word_count": {"full": 293, "brief": 293},
 "research_lines": [
  {"file": "research/units/unit-08-applications-integration.md", "line": "the definite integral of velocity over [a,b] is the displacement"}
 ],
 "inferred": [
  {"claim": "BC-QA-08003 is an either archetype, so the lesson takes Section I Part A and a no calculator example.", "settles": "The exam part mix the archetype is served in."},
  {"claim": "ki-1 is served as a static figure of the signed velocity areas.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {"claim": "The lesson carries two checks: the bundle holds one error, fewer than the three distractors a 4-option MCQ needs.", "settles": "Further active BC-ERR records on BC-SKL-08006."}
 ],
 "sources": ["BC-CON-08003", "BC-SKL-08006", "BC-EK-CHA-4C1", "ced:153", "BC-QA-08003", "BC-ERR-99010", "BC-MIS-08004", "BC-PRQ-06005", "research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals", "research/question-analysis/question-archetypes.md#BC-QA-08003 Rectilinear motion analysed with definite integrals", "research/exam/exam-structure.md#Section and part layout"]
}
```
