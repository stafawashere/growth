---
title: LSN-CON-09007 Integral of a vector-valued function taken component by component
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09007, integrating a vector-valued function one component at a time, built from authoring_bundle("BC-CON-09007") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09007 Integral of a vector-valued function taken component by component

Concept BC-CON-09007 (skills BC-SKL-09019, BC-SKL-09020), topic 9.5 of Unit 9, loaded by one archetype, BC-QA-09005 (family parametric-motion). Neither skill is independently assessable (`assessability_basis`: assessable only inside multi-skill parts), so the lesson works inside the coordinate-recovery shape and stresses what is this concept's own: one component integrated on its own, with its own starting value, and the vector of component integrals read as displacement.

## Prediction

Posed on ex-1's numbers, both bands, before any rule. Stem: a particle with velocity \(\langle 3\cos(t^2/2), 2\sqrt{t}e^{-t/2}\rangle\), \(x(1)=2\), \(y(1)=-3\), and which starting value goes with the integral of \(x'(t)\) when finding \(x(3)\). Form `mcq`, three options, key A, \(x(1)=2\). The distractors, \(y(1)=-3\) and the sum of both starts, are the single-constant and wrong-start moves of BC-ERR-09019, and neither is true of this integral. The resolution states ki-1's claim that each component carries its own constant, fixed by its own initial value. Sources: BC-CON-09007, BC-EK-FUN-8A1 and the Required mathematical knowledge paragraph of topic 9.5.

## Orientation

Served text (25 words), from BC-CON-09007 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.5 Integrating Vector-Valued Functions): a response integrates each velocity component on its own, each with its own starting value, and the free-response part scores the definite integral, the use of the initial condition and the value (sg-24:7, sg-23:7).

## Key ideas

One BC-EK maps to both skills, BC-EK-FUN-8A1 (ced:175), so one core block, both bands.

- ki-1 (core). Paraphrase of the topic's Required mathematical knowledge (Vector integration, Notation): integrals of real valued functions extend to vector-valued ones by integrating each component separately; each component carries its own constant, fixed by its own initial condition; the vector of the two definite integrals over an interval is the displacement (BC-EK-FUN-8B2, ced:176, via BC-SKL-09020). Anchor quote (15 words) from ced:175. Notation line: component wise integration.

## Recognition

- BC-QA-09005 (research/question-analysis/question-archetypes.md#BC-QA-09005 Coordinate of a particle recovered from an initial position): `common_givens` a velocity component, the position at one time, a second time; `asked_to_produce` an expression with an integral and the initial value, a numerical coordinate; `typical_wording` "find the coordinate of the position of the particle at the stated time and show the setup for the calculations". FRQ shape only in the corpus: BC-FRQ-2021-Q2-C, BC-FRQ-2022-Q2-C, BC-FRQ-2015-Q2-A, BC-FRQ-2024-Q2-C, each one part of the calculator active Q2 (research/question-analysis/frq-analysis.md#The calculator questions and the no-calculator questions). MCQ forms ask which expression gives a coordinate at a later time (topic Assessment behaviour).

What in the stem says "this concept": a rate given as a vector \(\langle x'(t), y'(t)\rangle\) and a position given as two coordinates or a point. The requested letter selects the one component to integrate and the one starting value that belongs to it. What says "not this one": "total distance travelled" (the integral of speed, BC-CON-09010), "speed" (a magnitude, BC-CON-09009), or "acceleration vector" (differentiate, BC-CON-09006).

The contrast pair in st-1 takes its near miss from the first of these, a distance stem from outside the archetype: it also gives a velocity vector and two times, but asks for the integral of speed. The separating feature is whether one component and its start are asked for.

## Method choice

One strategy block (one archetype family), low and mid bands.

- st-1, BC-QA-09005, with the contrast pair. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[0]`: write the coordinate as the known value plus the definite integral of the velocity component. First written line: \(x(3)=x(1)+\int_1^3 x'(t)\,dt\). Rival, `wrong_approaches`: omitting the initial condition; the concept's own rival is starting from the other coordinate's value (BC-ERR-09019). Separating feature: the requested letter names both the component and its starting value. The pair: this, a velocity \(\langle 4\cos(t^2/3), \sqrt t\rangle\) with \(x(2)=1\), \(y(2)=5\) and \(x(4)\) asked; not this, the total distance travelled by a particle over two times, which integrates speed; feature, whether a single coordinate at a time is requested.

## Solution path

- ex-1, BC-QA-09005, both bands, calculator. Draw: x_amplitude 3, x_spread 2, y_rate 2, x_start 2, y_start -3, known_time 1, offset 2, requested x, direction later, given_as coordinates, so \(v(t)=\langle 3\cos(t^2/2), 2\sqrt t\,e^{-t/2}\rangle\), \(x(1)=2\), \(y(1)=-3\), find \(x(3)\). Steps follow `expected_solution_path`: select the component and its start (no value); write known value plus integral (valued, tagged BC-PT-99033); evaluate on the calculator and add (valued, approx, 0.804). The path's last entry, "report with units", is idle: the stem names no units.
- A fluent solver writes the setup line and the value and holds the component selection in the head.

No productive-failure opener targets this concept, so no comparison callout.

## Scoring

BC-QA-09005 lists point types; ex-1 tags BC-PT-99033 on its setup line, so one generated line:

Uses the initial condition in an accumulation expression. Earned by: Adding the known function value at one endpoint to a definite integral of the rate (sg-24:3, sg-22:8). Not earned by: A definite integral alone with the known value never added (sg-22:8). Notation: sg-22:8 lists cases where a missing differential shifts which of the three points are available.

The archetype's `scoring_pattern` gives three points (the definite integral, the initial condition, the answer; sg-24:7). Point losses research names for this shape: no calculator setup before a numerical answer (research/scoring/common-point-losses.md#Setup points, BC-ERR-99021); fewer than three decimals (research/scoring/common-point-losses.md#Answer points, BC-ERR-99019); a missing differential can block the answer point when the expression is equated to a value (research/scoring/notation-requirements.md#The differential is normally optional, sg-23:8).

## Traps

Two active errors meet the concept's skills, in the bundle's order; both bands show both.

- err-BC-ERR-09019 (BC-MIS-09009, BC-MIS-99004). Wrong step on ex-1's draw: \(-3+\int_1^3 x'(t)\,dt\approx-4.196\), the \(y\) start used for \(x\). Right step: \(2+\int_1^3 x'(t)\,dt\approx0.804\). Distinct. Possible reason, words from BC-MIS-09009.
- err-BC-ERR-99010 (BC-MIS-08004, BC-MIS-99002). Wrong step: the displacement \(\int_1^3 x'(t)\,dt\) reported as a distance. Right step: \(\int_1^3\sqrt{x'(t)^2+y'(t)^2}\,dt\). Distinct. No possible reason line, to keep the brief form under its cap.

## Representations

None. The topic's Representations paragraph names BC-REP-14, BC-REP-01 and BC-REP-09 and conversions from a rate vector to a coordinate value; the figure it would carry is the ki-1 figure, so a second block would repeat it.

## Prerequisite bridge

Two BC-PRQ parents: BC-PRQ-06005 (supporting to BC-SKL-09020) and BC-PRQ-09001 (supporting to BC-SKL-09019), each one short paragraph from `description_plain` and `failure_signature`.

## Time

BC-QA-09005 is `calculator` and "One part of the calculator active BC free response question", so the part is Section II Part A, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout); this part is 3 of 9 points, a 5.0 minute share (README section 5). A fluent solver writes the setup line and the value (steps 2 and 3) and holds step 1. The setup is written before the calculator is touched because it carries two of the three points (research/exam/calculator-policy.md#The setup-plus-result rule).

## Checks

- chk-1, completion of ex-1, both bands: the setup is given, the value is asked. Key 0.804, equal to ex-1's answer.
- chk-2, isomorph on BC-QA-09005, both bands: x_amplitude 5, x_spread 3, y_rate 3, x_start -4, y_start 1, known_time 3, offset 1, requested y, later, coordinates. Key 1.979.
- No chk-3. Two error blocks exist and only BC-ERR-09019 yields a coordinate value on this archetype, so a 4-option MCQ with three anchored distractors is not available; listed as inferred.

No draw equals a published BC-QA-09005 `parameter_draw` (content/items_gen_unit09).

## Delivery

- orientation: figure. Rule 4 (the unit README's rule 3): BC-REP-14 on BC-SKL-09019 and BC-SKL-09020. The path from \(t=1\) to \(t=3\) with the start point labelled by both coordinates.
- ki-1: figure. Rule 4 (README rule 3), not promoted: the stem asks for a value, not a reading (README section 6). The displacement vector between the positions at \(t=1\) and \(t=3\), its legs labelled as the two component integrals.
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-09019, err-BC-ERR-99010: step_reveal. Rule 1.

Every non-text choice is [inferred], settled by the modality A/B in the build plan.

## Band plan

- Low (full): prediction, orientation, both bridges, ki-1, st-1 with the contrast pair, ex-1 with its scoring line, chk-1, err-09019, err-99010, chk-2. 447 words, 3.0 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, both bridges, ki-1, st-1 with the contrast pair, ex-1 with its scoring line, chk-1, err-09019, err-99010, chk-2. 447 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-09019, err-BC-ERR-99010, ex-1.

## Sources

- BC-CON-09007; BC-SKL-09019, BC-SKL-09020; BC-EK-FUN-8A1, BC-EK-FUN-8B2; ced:175, ced:176
- BC-QA-09005; BC-FRQ-2021-Q2-C, BC-FRQ-2022-Q2-C, BC-FRQ-2015-Q2-A, BC-FRQ-2024-Q2-C
- BC-PT-99033; sg-24:7, sg-23:7, sg-23:8, sg-24:3, sg-22:8
- BC-ERR-09019, BC-ERR-99010, BC-ERR-99021, BC-ERR-99019; BC-MIS-09009, BC-MIS-99004, BC-MIS-08004, BC-MIS-99002
- BC-PRQ-06005, BC-PRQ-09001
- research/units/unit-09-parametric-polar-vector.md#9.5 Integrating Vector-Valued Functions
- research/question-analysis/question-archetypes.md#BC-QA-09005 Coordinate of a particle recovered from an initial position
- research/question-analysis/frq-analysis.md#The calculator questions and the no-calculator questions
- research/scoring/common-point-losses.md#Setup points
- research/scoring/common-point-losses.md#Answer points
- research/scoring/notation-requirements.md#The differential is normally optional
- research/exam/exam-structure.md#Section and part layout
- research/exam/calculator-policy.md#The setup-plus-result rule
- [inferred] Two checks only: the bundle holds two errors and only one produces a coordinate value on BC-QA-09005. Settled by a library error record for the vector antiderivative that yields a value on this archetype.
- [inferred] The figure modes on the orientation and ki-1. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-09007",
 "kind": "concept",
 "target_id": "BC-CON-09007",
 "unit": "09",
 "skills": ["BC-SKL-09019", "BC-SKL-09020"],
 "prediction": {"id": "pr-1", "stem": {"text": "Before the rule: a particle has velocity \\(\\langle 3\\cos(t^2/2), 2\\sqrt{t}e^{-t/2}\\rangle\\), \\(x(1)=2\\) and \\(y(1)=-3\\). Which start goes with the integral of \\(x'(t)\\) when finding \\(x(3)\\)?", "command_verb": "predict"}, "format": "mcq",
  "options": [{"id": "A", "label": "\\(x(1)=2\\)", "is_key": true}, {"id": "B", "label": "\\(y(1)=-3\\)", "is_key": false}, {"id": "C", "label": "The sum of both starts", "is_key": false}],
  "resolution": "Each component carries its own constant, fixed by its own initial value, so \\(x(3)=2+\\int_1^3 x'(t)\\,dt\\).",
  "sources": ["BC-CON-09007", "BC-EK-FUN-8A1", "research/units/unit-09-parametric-polar-vector.md#9.5 Integrating Vector-Valued Functions"]},
 "orientation": {
  "text": "Each velocity component is integrated on its own, from its own start. A coordinate is its known value plus the definite integral of its component.",
  "sources": ["BC-CON-09007", "research/units/unit-09-parametric-polar-vector.md#9.5 Integrating Vector-Valued Functions", "sg-24:7"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-8A1",
   "depth": "core",
   "text": "Integrate a vector-valued rate one component at a time. Each component carries its own constant, fixed by its own initial value. Over an interval, the vector of the two definite integrals is the displacement.",
   "notation": "component wise integration",
   "quote": {"text": "Methods for calculating integrals of real-valued functions can be extended to parametric or vector-valued functions.", "source": "ced:175"},
   "sources": ["BC-EK-FUN-8A1", "ced:175", "BC-EK-FUN-8B2", "ced:176", "research/units/unit-09-parametric-polar-vector.md#9.5 Integrating Vector-Valued Functions"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09005",
   "cue": "A velocity component, a position at one time, and a second time.",
   "method": "Known value plus the integral, \\(x(3)=x(1)+\\int_1^3 x'(t)\\,dt\\).",
   "rival": "Starting from the other coordinate's value.",
   "separating_feature": "The requested letter names the component and its start.",
   "sources": ["BC-QA-09005", "BC-ERR-09019"],
   "evidence_tag": "verified",
   "contrast": {
    "this": {"text": "Velocity \\(\\langle 4\\cos(t^2/3), \\sqrt{t}\\rangle\\), \\(x(2)=1\\), \\(y(2)=5\\). Find \\(x(4)\\).", "archetype_id": "BC-QA-09005"},
    "not_this": {"text": "Velocity \\(\\langle 4\\cos(t^2/3), \\sqrt{t}\\rangle\\). Find the total distance travelled from \\(t=2\\) to \\(t=4\\).", "why_not": "It asks for the integral of speed, not one coordinate."},
    "feature": "One coordinate at a later time is asked for."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-09005",
   "bands": ["low", "mid"],
   "parameter_draw": {"x_amplitude": "3", "x_spread": "2", "y_rate": "2", "x_start": "2", "y_start": "-3", "known_time": "1", "offset": "2", "requested": "x", "direction": "later", "given_as": "coordinates"},
   "problem": {"text": "A particle has velocity \\(\\langle 3\\cos(t^2/2), 2\\sqrt{t}e^{-t/2}\\rangle\\), with \\(x(1)=2\\) and \\(y(1)=-3\\). Find \\(x(3)\\) to three decimals, showing the setup.", "command_verb": "find"},
   "calculator_status": "calculator",
   "steps": [
    {"cue": "The stem asks for \\(x(3)\\).", "why": "Only \\(x'(t)\\) and its own start \\(x(1)=2\\) are used."},
    {"cue": "Known at 1, asked at 3.", "why": "Start plus forward accumulation: \\(x(3)=2+\\int_1^3 3\\cos(t^2/2)\\,dt\\).", "expr": "2 + Integral(3*cos(t**2/2), (t, 1, 3))", "relation": "new", "point_type_id": "BC-PT-99033"},
    {"cue": "No elementary antiderivative.", "why": "The calculator gives the integral as about \\(-1.196\\), so \\(x(3)\\approx0.804\\).", "expr": "0.804", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "answer": {"form": "numeric", "expr": "0.804"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99033"], "lines": [{"point_type_id": "BC-PT-99033", "text": "Uses the initial condition in an accumulation expression. Earned by: Adding the known function value at one endpoint to a definite integral of the rate (sg-24:3, sg-22:8). Not earned by: A definite integral alone with the known value never added (sg-22:8). Notation: sg-22:8 lists cases where a missing differential shifts which of the three points are available."}]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-09019",
   "observed_behavior": "A vector antiderivative carries a single constant rather than one in each component.",
   "scoring_consequence": "The particular solution cannot satisfy both initial conditions, so the answer is wrong.",
   "wrong_step": {"text": "The \\(y\\) start used for \\(x\\): \\(-3+\\int_1^3 x'(t)\\,dt\\approx-4.196\\).", "expr": "-4.196"},
   "right_step": {"text": "The \\(x\\) start: \\(2+\\int_1^3 x'(t)\\,dt\\approx0.804\\).", "expr": "0.804"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-09009", "text": "a single constant of integration all look immaterial"},
   "sources": ["BC-ERR-09019", "BC-MIS-09009"]
  },
  {
   "error_id": "BC-ERR-99010",
   "observed_behavior": "Responses integrate velocity without an absolute value, or split the interval incorrectly, and report the net change as the total distance travelled.",
   "scoring_consequence": "The setup point for total distance is not earned; the numerical answer point follows the setup.",
   "wrong_step": {"text": "Displacement \\(\\int_1^3 x'(t)\\,dt\\) reported as distance.", "expr": "Integral(3*cos(t**2/2), (t, 1, 3))"},
   "right_step": {"text": "Distance integrates speed: \\(\\int_1^3\\sqrt{x'^2+y'^2}\\,dt\\).", "expr": "Integral(sqrt(9*cos(t**2/2)**2 + 4*t*exp(-t)), (t, 1, 3))"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": ["BC-ERR-99010"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "Do not swap the rate \\(x'(t)\\) and the value \\(x(1)\\)."},
  {"prq_id": "BC-PRQ-09001", "text": "In \\(\\langle x'(t), y'(t)\\rangle\\) the horizontal component is first."}
 ],
 "time": {"exam_part": "II-A", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 3]}, "skipped_steps": {"ex-1": [1]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-09005",
   "parameter_draw": {"x_amplitude": "3", "x_spread": "2", "y_rate": "2", "x_start": "2", "y_start": "-3", "known_time": "1", "offset": "2", "requested": "x", "direction": "later", "given_as": "coordinates"},
   "completes": "ex-1",
   "stem": {"text": "The setup is \\(x(3)=2+\\int_1^3 3\\cos(t^2/2)\\,dt\\). Give \\(x(3)\\) to three decimals.", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "0.804"},
   "steps": [
    {"text": "The known value plus the accumulation.", "expr": "2 + Integral(3*cos(t**2/2), (t, 1, 3))", "relation": "new", "point_type_id": "BC-PT-99033"},
    {"text": "The calculator gives about 0.804.", "expr": "0.804", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-09019"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-09005",
   "parameter_draw": {"x_amplitude": "5", "x_spread": "3", "y_rate": "3", "x_start": "-4", "y_start": "1", "known_time": "3", "offset": "1", "requested": "y", "direction": "later", "given_as": "coordinates"},
   "stem": {"text": "Velocity \\(\\langle 5\\cos(t^2/3), 3\\sqrt{t}e^{-t/2}\\rangle\\), \\(x(3)=-4\\), \\(y(3)=1\\). Find \\(y(4)\\) to three decimals.", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "1.979"},
   "steps": [
    {"text": "The \\(y\\) start plus the \\(y\\) accumulation from 3 to 4.", "expr": "1 + Integral(3*sqrt(t)*exp(-t/2), (t, 3, 4))", "relation": "new", "point_type_id": "BC-PT-99033"},
    {"text": "The calculator gives about 1.979.", "expr": "1.979", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-09019", "BC-SKL-09020"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "figure", "reason": "rule 4 (unit README rule 3): BC-REP-14 on BC-SKL-09019 and BC-SKL-09020", "sources": ["BC-SKL-09019", "BC-SKL-09020"],
   "spec": {"kind": "parametric_path", "x_rate": "3*cos(t**2/2)", "y_rate": "2*sqrt(t)*exp(-t/2)", "t_range": [1, 3], "start": [2, -3], "points": [{"t": 1, "style": "filled"}, {"t": 3, "style": "open"}], "labels": [{"text": "t = 1: (2, -3)", "placement": "inside"}, {"text": "t = 3: x(3) = ?", "placement": "inside"}]},
   "fallback": "the same path static with both labels", "keyboard": "no control; the figure description is reached with Tab"},
  {"block": "ki-1", "mode": "figure", "reason": "rule 4 (unit README rule 3): BC-REP-14 on BC-SKL-09020; not promoted, the stem asks for a value, not a reading", "sources": ["BC-SKL-09020"],
   "spec": {"kind": "vector_diagram", "tail": [2, -3], "head": [0.804, -1.5], "legs": [{"axis": "x", "value": "integral of x' from 1 to 3"}, {"axis": "y", "value": "integral of y' from 1 to 3"}], "labels": [{"text": "displacement", "placement": "inside"}, {"text": "x leg: integral of x'", "placement": "inside"}, {"text": "y leg: integral of y'", "placement": "inside"}]},
   "fallback": "the static vector with its two legs labelled", "keyboard": "no control"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-09019", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99010", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-09019", "err-BC-ERR-99010", "ex-1"],
 "read_minutes": {"full": 3.0, "brief": 3.0},
 "word_count": {"full": 447, "brief": 447},
 "research_lines": [
  {"file": "research/units/unit-09-parametric-polar-vector.md", "line": "Each component carries its own constant of integration."},
  {"file": "research/scoring/common-point-losses.md", "line": "Displacement setup given where total distance was asked"}
 ],
 "inferred": [
  {"claim": "Two checks only: the bundle holds two errors and only BC-ERR-09019 produces a coordinate value on BC-QA-09005, so check 3 has no three anchored distractors.", "settles": "A library error record for the vector antiderivative that yields a value on BC-QA-09005."},
  {"claim": "Figure mode on the orientation and ki-1 serves this concept better than text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-09007", "BC-SKL-09019", "BC-SKL-09020", "BC-EK-FUN-8A1", "BC-EK-FUN-8B2", "ced:175", "ced:176", "BC-QA-09005", "BC-PT-99033", "sg-24:7", "sg-23:7", "sg-23:8", "sg-24:3", "sg-22:8", "BC-ERR-09019", "BC-ERR-99010", "BC-ERR-99021", "BC-ERR-99019", "BC-MIS-09009", "BC-MIS-99004", "BC-MIS-08004", "BC-MIS-99002", "BC-PRQ-06005", "BC-PRQ-09001", "BC-FRQ-2021-Q2-C", "BC-FRQ-2022-Q2-C", "BC-FRQ-2015-Q2-A", "BC-FRQ-2024-Q2-C", "research/units/unit-09-parametric-polar-vector.md#9.5 Integrating Vector-Valued Functions", "research/question-analysis/question-archetypes.md#BC-QA-09005 Coordinate of a particle recovered from an initial position", "research/question-analysis/frq-analysis.md#The calculator questions and the no-calculator questions", "research/scoring/common-point-losses.md#Setup points", "research/scoring/common-point-losses.md#Answer points", "research/scoring/notation-requirements.md#The differential is normally optional", "research/exam/exam-structure.md#Section and part layout", "research/exam/calculator-policy.md#The setup-plus-result rule"]
}
```
