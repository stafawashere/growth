---
title: LSN-CON-09008 Particular position from a rate vector and an initial position
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09008, a coordinate at one time as its known value plus the definite integral of its velocity component, forward or backward in time, built from authoring_bundle("BC-CON-09008") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09008 Particular position from a rate vector and an initial position

Concept BC-CON-09008 (skills BC-SKL-09021, 09022), topic 9.5 of Unit 9, BC only (ced:175), loaded by one archetype, BC-QA-09005 (family parametric-motion). Hard parent inside the unit: BC-CON-09007 (docs/lessons/unit-09/README.md, section 1); the outside hard parent BC-SKL-06037, an initial value plus an accumulated change, is assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The core claim is that a coordinate is its known value plus the accumulated change. The stem gives the point \((-3, 4)\) and the integral 2.054. Key B, 6.054. The distractors are the integral alone (BC-ERR-08011's form) and the start minus the integral. The definition of an integral of a rate as a change answers it before any rule. The resolution states the sum with no verdict word. Source: BC-CON-09008 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-09008 `description_plain` (each coordinate is its starting value plus the accumulated change) and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.5 Integrating Vector-Valued Functions): the free-response part asks for one coordinate at a time given the position at another, and scores the integral, the use of the initial condition and the answer (sg-24:7). No count, no frequency.

## Key ideas

One BC-EK, BC-EK-FUN-8A1 (ced:175), maps both skills, so one core block, both bands. ki-1 paraphrases the Required mathematical knowledge paragraphs Particular solution, Direction of accumulation and Notation (each component has its own constant). No anchor quote. Notation line: the concept's `notation`.

## Recognition

BC-QA-09005 is the only archetype loading the skills (research/question-analysis/question-archetypes.md#BC-QA-09005 Coordinate of a particle recovered from an initial position).

- `common_givens`: a velocity component, the position at one time, a second time. `asked_to_produce`: an expression with an integral and the initial value, and a numerical coordinate.
- The signal in the stem: a known position at one time and a coordinate asked at another. The difficulty variables are whether the requested time is before or after the known time, and whether the position is given as a point.
- Shapes: one part of the calculator active free response, BC-FRQ-2021-Q2-C, BC-FRQ-2022-Q2-C, BC-FRQ-2015-Q2-A, BC-FRQ-2024-Q2-C.

The near miss of the contrast pair is the total distance stem from BC-QA-09007 (outside the block's archetype): the same velocity and interval, but the integrand is the speed and no start is added.

## Method choice

- st-1, BC-QA-09005. Cue from `common_givens`. Method, `expected_solution_path[0]`: write the coordinate as the known value plus the definite integral of the velocity component. Rival: `wrong_approaches` "omitting the initial condition" and "integrating forwards when the known position is later". Separating feature: the requested letter names the component and its own start. Both cue fields exist, so the block is not inferred. The block carries the contrast pair, a coordinate stem beside a total distance stem.

## Solution path

- ex-1, BC-QA-09005, both bands, calculator. Draw: x_amplitude 5, x_spread 3, y_rate 2, x_start -3, y_start 4, known_time 1, offset 2, requested y, direction later, given_as point. \(\int_1^3 2\sqrt{t}e^{-t/2}\,dt=2.054\), \(y(3)=6.054\) by SymPy. No published item on BC-QA-09005 carries this draw (ITM-GEN-09005-00 to 21).
- ex-2, low band, calculator. Draw: x_amplitude 4, x_spread 2, y_rate 2, x_start 2, y_start -3, known_time 3, offset 1, requested x, direction earlier, given_as coordinates. \(\int_2^3 4\cos(t^2/2)\,dt=-3.035\), so \(x(2)=5.035\).
- ex-2 is faded from step 3: steps 1 and 2 (the direction and the setup with its subtraction) are shown, the student writes the value, and step 3 then reveals. The fade falls there because the setup is what changes with the direction, and the evaluation repeats ex-1.
- The steps follow `expected_solution_path`: the known value, the integral, the sum. A fluent solver writes the setup and the value, and holds the choice of start and direction.
- No productive-failure comparison: BC-CON-09008 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-09005 lists BC-PT-99013, 99010, 99033, 99004, 99005, 99002, 99001. ex-1 tags BC-PT-99033 on the setup, the initial condition point, which is this concept's own point; ex-2 tags BC-PT-99033 and BC-PT-99004. BC-PT-99001 (the integral with correct limits) is earned by the same line but untagged, so one line carries one point in the brief band. The lines are `reader_checks` output.

Point losses from research: a definite integral alone with the known value never added does not earn the initial condition point (sg-22:8), and several arrangements of the subtraction and the limits earn the first two points (sg-24:7) (research/scoring/common-point-losses.md#Setup points).

## Traps

Two errors meet the skills, in bundle order: BC-ERR-08011 (linked BC-MIS-08006 and 09010, high) and BC-ERR-09021 (BC-MIS-09010 and 09012, high). Both blocks show in both bands. The first block is on ex-1's draw, the integral alone against start plus integral, with the possible reason from BC-MIS-09010, `fix_prompt` true. The second is on ex-2's draw, because the record's behaviour is the integral added when it should be subtracted, which needs an earlier requested time; `fix_prompt` true.

## Representations

None. The topic's Representations paragraph names the conversions of a rate vector with an initial condition to a coordinate value and of a position statement back to an integral; the orientation and ki-1 figures already carry them.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` and `failure_signature`, gated by state.

## Time

BC-QA-09005 is an MCQ in Section I Part B, 2.92 minutes (research/exam/exam-structure.md#Section and part layout); as a free response part it scores 3 points, 5.0 minutes (docs/lessons/unit-09/README.md, section 5). A fluent solver writes the known value plus the integral with limits, and the value; the choice of start and of direction are held [inferred]. No target.

## Checks

- chk-1, completion of ex-1, both bands: the setup given, the value asked. Key 6.054.
- chk-2, isomorph, both bands, calculator. Draw: x_amplitude 2, x_spread 4, y_rate 3, x_start 3, y_start -2, known_time 2, offset 1, requested y, direction later, given_as coordinates. Key -0.641.
- chk-3, MCQ, low band, calculator. Draw: x_amplitude 4, x_spread 2, y_rate 3, x_start -2, y_start 5, known_time 3, offset 2, requested x, direction earlier, given_as coordinates. Key -0.405. Distractors: -3.595, the integral added (BC-ERR-09021); -1.595, the integral from 1 to 3 alone, and 1.595, the integral from 3 to 1 alone (both BC-ERR-08011).

## Delivery

- orientation, ki-1: figure. Unit README section 6 names FUN-8B2 as a figure for BC-CON-09008; rule 3 of the README: BC-REP-14 on BC-SKL-09021 and 09022. Not promoted to interactive: the direction is a form of the stem, and the stem asks for a coordinate value. The orientation marks the known position and the asked one; ki-1 draws the displacement arrow backward in time.
- ex-1, ex-2, the two error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, the two error blocks, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 657 words, 4.4 minutes.
- Mid (brief): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, both error blocks, chk-2. 450 words, 3.0 minutes.
- Refresher: ki-1, both error blocks, ex-1.

## Sources

- BC-CON-09008; BC-SKL-09021, BC-SKL-09022; BC-EK-FUN-8A1; ced:175
- BC-QA-09005; BC-PT-99033, BC-PT-99004
- BC-ERR-08011, BC-ERR-09021; BC-MIS-09010
- BC-PRQ-06005
- sg-24:7, sg-22:8, sg-25:3, sg-26:4
- research/units/unit-09-parametric-polar-vector.md#9.5 Integrating Vector-Valued Functions
- research/question-analysis/question-archetypes.md#BC-QA-09005 Coordinate of a particle recovered from an initial position
- research/scoring/common-point-losses.md#Setup points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The figure modes, the held steps and the check 3 distractor pairing, each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09008",
 "kind": "concept",
 "target_id": "BC-CON-09008",
 "unit": "09",
 "skills": [
  "BC-SKL-09021",
  "BC-SKL-09022"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "A particle is at the point \\((-3, 4)\\) at \\(t=1\\), and \\(\\int_1^3 y'(t)\\,dt\\approx2.054\\). Predict \\(y(3)\\).",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(2.054\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(6.054\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(1.946\\)",
    "is_key": false
   }
  ],
  "resolution": "The integral is the change in \\(y\\), so \\(y(3)\\) is the starting value plus it, \\(4+2.054\\).",
  "sources": [
   "BC-CON-09008",
   "research/units/unit-09-parametric-polar-vector.md#9.5 Integrating Vector-Valued Functions"
  ]
 },
 "orientation": {
  "text": "Each coordinate is its starting value plus the accumulated change. A response writes the definite integral of the velocity component, adds the known value, and gives the coordinate.",
  "sources": [
   "BC-CON-09008",
   "research/units/unit-09-parametric-polar-vector.md#9.5 Integrating Vector-Valued Functions"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-8A1",
   "depth": "core",
   "text": "Given a velocity component and the position at one time, the coordinate at another time is its known value plus the definite integral of that component between the two times. Each coordinate has its own start. When the known time is later, the integral is subtracted, or its limits are reversed.",
   "notation": "position from velocity plus initial position",
   "quote": null,
   "sources": [
    "BC-EK-FUN-8A1",
    "ced:175",
    "research/units/unit-09-parametric-polar-vector.md#9.5 Integrating Vector-Valued Functions"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09005",
   "cue": "A velocity component, the position at one time, a second time.",
   "method": "Write the known value plus the definite integral of that component.",
   "rival": "The integral alone, or added when the known time is later.",
   "separating_feature": "The requested letter names the component and its own start.",
   "sources": [
    "BC-QA-09005"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "A particle has \\(x'(t)=3\\cos(t^2/2)\\) and \\(x(1)=2\\). Find \\(x(3)\\).",
     "archetype_id": "BC-QA-09005"
    },
    "not_this": {
     "text": "A particle has velocity \\(\\langle 3\\cos(t^2/2), 2\\sqrt{t}\\rangle\\). Find the total distance from \\(t=1\\) to \\(t=3\\).",
     "why_not": "Distance integrates the speed, and no start is added."
    },
    "feature": "A known start and a coordinate at another time mean start plus integral."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-09005",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "x_amplitude": "5",
    "x_spread": "3",
    "y_rate": "2",
    "x_start": "-3",
    "y_start": "4",
    "known_time": "1",
    "offset": "2",
    "requested": "y",
    "direction": "later",
    "given_as": "point"
   },
   "problem": {
    "text": "A particle has velocity \\(\\langle 5\\cos(t^2/3), 2\\sqrt{t}e^{-t/2}\\rangle\\) and is at the point \\((-3, 4)\\) at \\(t=1\\). Find \\(y(3)\\) to three decimals, showing the setup.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "The point gives \\(y(1)=4\\).",
     "why": "\\(y\\) uses its own start."
    },
    {
     "cue": "Known at 1, asked at 3.",
     "why": "Start plus forward accumulation.",
     "expr": "4 + Integral(2*sqrt(t)*exp(-t/2), (t, 1, 3))",
     "relation": "new",
     "point_type_id": "BC-PT-99033"
    },
    {
     "cue": "No elementary antiderivative.",
     "why": "The calculator evaluates it.",
     "expr": "6.054",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "6.054"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-09005",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "x_amplitude": "4",
    "x_spread": "2",
    "y_rate": "2",
    "x_start": "2",
    "y_start": "-3",
    "known_time": "3",
    "offset": "1",
    "requested": "x",
    "direction": "earlier",
    "given_as": "coordinates"
   },
   "fade_from": 3,
   "problem": {
    "text": "A particle has velocity \\(\\langle 4\\cos(t^2/2), 2\\sqrt{t}e^{-t/2}\\rangle\\), with \\(x(3)=2\\) and \\(y(3)=-3\\). Find \\(x(2)\\) to three decimals, showing the setup.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Known at 3, asked at the earlier 2.",
     "why": "Going back in time subtracts the change."
    },
    {
     "cue": "\\(x\\) starts at 2.",
     "why": "Subtract the integral from 2 to 3.",
     "expr": "2 - Integral(4*cos(t**2/2), (t, 2, 3))",
     "relation": "new",
     "point_type_id": "BC-PT-99033"
    },
    {
     "cue": "Evaluate with the calculator.",
     "why": "Three places.",
     "expr": "5.035",
     "relation": "evaluate",
     "subs": {},
     "approx": true,
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "5.035"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99033"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99033",
     "text": "Uses the initial condition in an accumulation expression. Earned by: Adding the known function value at one endpoint to a definite integral of the rate (sg-24:3, sg-22:8). Not earned by: A definite integral alone with the known value never added (sg-22:8). Notation: sg-22:8 lists cases where a missing differential shifts which of the three points are available."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99033",
    "BC-PT-99004"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99033",
     "text": "Uses the initial condition in an accumulation expression. Earned by: Adding the known function value at one endpoint to a definite integral of the rate (sg-24:3, sg-22:8). Not earned by: A definite integral alone with the known value never added (sg-22:8). Notation: sg-22:8 lists cases where a missing differential shifts which of the three points are available."
    },
    {
     "point_type_id": "BC-PT-99004",
     "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-08011",
   "observed_behavior": "The response evaluates the integral of the rate and reports it as the value of the quantity.",
   "scoring_consequence": "The initial condition point is lost and the answer point falls with it (sg-24:7).",
   "wrong_step": {
    "text": "The integral alone: \\(2.054\\).",
    "expr": "Integral(2*sqrt(t)*exp(-t/2), (t, 1, 3))"
   },
   "right_step": {
    "text": "Start plus integral: \\(6.054\\).",
    "expr": "4 + Integral(2*sqrt(t)*exp(-t/2), (t, 1, 3))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-09010",
    "text": "reads the accumulation as the position itself rather than as the change in it"
   },
   "sources": [
    "BC-ERR-08011",
    "BC-MIS-09010"
   ]
  },
  {
   "error_id": "BC-ERR-09021",
   "observed_behavior": "The integral between the known time and the requested time is added when it should be subtracted, or its limits are in the wrong order.",
   "scoring_consequence": "The answer point is lost; the guideline lists several correct arrangements of the subtraction and the limits (sg-24:7).",
   "wrong_step": {
    "text": "On ex-2, \\(2+\\int_2^3\\): \\(-1.035\\).",
    "expr": "2 + Integral(4*cos(t**2/2), (t, 2, 3))"
   },
   "right_step": {
    "text": "On ex-2, \\(2-\\int_2^3\\): \\(5.035\\).",
    "expr": "2 - Integral(4*cos(t**2/2), (t, 2, 3))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09021",
    "BC-MIS-09010"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(x'(t)\\) is a rate and \\(x(1)\\) a value at one input."
  }
 ],
 "time": {
  "exam_part": "I-B",
  "budget_minutes": 2.92,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    3
   ],
   "ex-2": [
    2,
    3
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1
   ],
   "ex-2": [
    1
   ]
  }
 },
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": [
    "low",
    "mid"
   ],
   "archetype_id": "BC-QA-09005",
   "parameter_draw": {
    "x_amplitude": "5",
    "x_spread": "3",
    "y_rate": "2",
    "x_start": "-3",
    "y_start": "4",
    "known_time": "1",
    "offset": "2",
    "requested": "y",
    "direction": "later",
    "given_as": "point"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The setup is \\(y(3)=4+\\int_1^3 2\\sqrt{t}e^{-t/2}\\,dt\\). Give \\(y(3)\\) to three decimals.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "6.054"
   },
   "steps": [
    {
     "text": "The known value plus the accumulation.",
     "expr": "4 + Integral(2*sqrt(t)*exp(-t/2), (t, 1, 3))",
     "relation": "new",
     "point_type_id": "BC-PT-99033"
    },
    {
     "text": "The calculator.",
     "expr": "6.054",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09021"
   ]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": [
    "low",
    "mid"
   ],
   "archetype_id": "BC-QA-09005",
   "parameter_draw": {
    "x_amplitude": "2",
    "x_spread": "4",
    "y_rate": "3",
    "x_start": "3",
    "y_start": "-2",
    "known_time": "2",
    "offset": "1",
    "requested": "y",
    "direction": "later",
    "given_as": "coordinates"
   },
   "stem": {
    "text": "Velocity \\(\\langle 2\\cos(t^2/4), 3\\sqrt{t}e^{-t/2}\\rangle\\), \\(x(2)=3\\), \\(y(2)=-2\\). Find \\(y(3)\\) to three decimals.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-0.641"
   },
   "steps": [
    {
     "text": "The \\(y\\) start plus the \\(y\\) accumulation.",
     "expr": "-2 + Integral(3*sqrt(t)*exp(-t/2), (t, 2, 3))",
     "relation": "new",
     "point_type_id": "BC-PT-99033"
    },
    {
     "text": "The calculator.",
     "expr": "-0.641",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09021"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-09005",
   "parameter_draw": {
    "x_amplitude": "4",
    "x_spread": "2",
    "y_rate": "3",
    "x_start": "-2",
    "y_start": "5",
    "known_time": "3",
    "offset": "2",
    "requested": "x",
    "direction": "earlier",
    "given_as": "coordinates"
   },
   "stem": {
    "text": "Velocity \\(\\langle 4\\cos(t^2/2), 3\\sqrt{t}e^{-t/2}\\rangle\\), \\(x(3)=-2\\), \\(y(3)=5\\). With a calculator, \\(x(1)\\) is",
    "command_verb": "identify"
   },
   "key": {
    "form": "numeric",
    "expr": "-0.405"
   },
   "steps": [
    {
     "text": "Known at 3, asked at 1.",
     "expr": "-2 - Integral(4*cos(t**2/2), (t, 1, 3))",
     "relation": "new"
    },
    {
     "text": "The calculator.",
     "expr": "-0.405",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "-3.595",
     "error_path": "BC-ERR-09021",
     "derivation": "the integral from 1 to 3 added to the known value, so the accumulation runs the wrong way"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "-1.595",
     "error_path": "BC-ERR-08011",
     "derivation": "the integral from 1 to 3 reported alone, with the known value never used"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "-0.405",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "1.595",
     "error_path": "BC-ERR-08011",
     "derivation": "the integral from 3 to 1 reported alone, with the known value never used"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09022"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3 of the unit README: BC-REP-14 on BC-SKL-09021 and 09022; not promoted, the stem asks for a coordinate value",
   "sources": [
    "BC-SKL-09021"
   ],
   "spec": {
    "kind": "vector_diagram",
    "tail": [
     -3,
     4
    ],
    "head": [
     1,
     6.05
    ],
    "legs": [
     {
      "axis": "y",
      "value": "integral of y' from 1 to 3"
     }
    ],
    "labels": [
     {
      "text": "known: (-3, 4) at t = 1",
      "placement": "inside"
     },
     {
      "text": "asked: y(3) = start + integral",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same diagram static with both labels",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 3 of the unit README: BC-REP-14 on BC-SKL-09021 and 09022; not promoted, because BC-QA-09005 difficulty_variables name whether the requested time is before or after the known time, a form of the stem, and the stem asks for a value",
   "sources": [
    "BC-SKL-09021",
    "BC-SKL-09022",
    "BC-QA-09005"
   ],
   "spec": {
    "kind": "displacement_arrow",
    "known": {
     "t": 3,
     "value": "known position"
    },
    "asked": {
     "t": 2,
     "value": "requested position"
    },
    "direction": "backward in time",
    "labels": [
     {
      "text": "known at t = 3",
      "placement": "inside"
     },
     {
      "text": "asked at t = 2: subtract the change",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same arrow static, forward and backward versions side by side",
   "keyboard": "no control"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "ex-2",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08011",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09021",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-08011",
  "err-BC-ERR-09021",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "each coordinate at another time is its known value plus the definite integral of the corresponding velocity component between the two times."
  }
 ],
 "inferred": [
  {
   "claim": "Two errors meet the two skills, so check 3 anchors a distractor pair to each: BC-ERR-09021 for the added integral and BC-ERR-08011 for the two integral-alone forms (from the known time to the requested time, and the reverse).",
   "settles": "A third error record for BC-SKL-09021 or 09022, for example a wrong-limits error on this shape."
  },
  {
   "claim": "The figure modes serve this concept better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "A fluent solver writes the setup and the value and holds the choice of start and of direction.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-09008",
  "BC-SKL-09021",
  "BC-SKL-09022",
  "BC-EK-FUN-8A1",
  "ced:175",
  "BC-QA-09005",
  "BC-PT-99033",
  "BC-PT-99004",
  "sg-24:7",
  "sg-22:8",
  "sg-25:3",
  "sg-26:4",
  "BC-ERR-08011",
  "BC-ERR-09021",
  "BC-MIS-09010",
  "BC-PRQ-06005",
  "research/units/unit-09-parametric-polar-vector.md#9.5 Integrating Vector-Valued Functions",
  "research/question-analysis/question-archetypes.md#BC-QA-09005 Coordinate of a particle recovered from an initial position",
  "research/exam/exam-structure.md#Section and part layout",
  "research/scoring/common-point-losses.md#Setup points"
 ],
 "word_count": {
  "full": 657,
  "brief": 450
 },
 "read_minutes": {
  "full": 4.4,
  "brief": 3.0
 }
}
```
