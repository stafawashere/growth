---
title: LSN-CON-09010 Total distance travelled as the integral of speed
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09010, total distance as the definite integral of speed and a coordinate recovered from a known position, built from authoring_bundle("BC-CON-09010") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09010 Total distance travelled as the integral of speed

Concept BC-CON-09010 (skills BC-SKL-09025, BC-SKL-09026), topic 9.6 of Unit 9, BC only (ced:176), loaded by two archetypes of one family, BC-QA-09007 (distance) and BC-QA-09005 (coordinate from an initial position). The Unit 9 hard parents are BC-CON-09004, 09008 and 09009 (docs/lessons/unit-09/README.md, section 1), so arc length, position from a rate and speed are assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The particle has velocity \(\langle 4\cos(3t/2), 2(t^2-3)\rangle\) on \([0,5/2]\) and its vertical velocity changes sign inside the interval. Key B, the distance is greater than the length of the net change. The distractors are equal and less. A path that turns is longer than the straight gap between its ends, which needs no rule about integrals. The resolution gives both values and says what the integral adds up, with no verdict word. Source: BC-CON-09010 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-09010 `description_plain` ("Integrating speed over the interval gives the length of the path travelled") and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions): the calculator FRQ part asks for a total distance and another for a coordinate from an initial condition, each with the setup shown. The orientation states what a response shows. No count, no frequency.

## Key ideas

Both skills map to one essential knowledge statement, BC-EK-FUN-8B2 (ced:176): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph Displacement and distance: the integral of the velocity vector is the displacement and gives a position, and the integral of speed is the total distance. Notation line: the concept's `notation`, "integral of speed". No anchor quote: the paraphrase carries the whole statement and the brief band has no words to spare.

## Recognition

- BC-QA-09007 (research/question-analysis/question-archetypes.md#BC-QA-09007 Total distance travelled by a particle in the plane): `common_givens` two velocity components and a time interval; `asked_to_produce` a definite integral of the speed and a numerical distance; `typical_wording` find the total distance travelled and show the setup. Calculator FRQ part, BC-FRQ-2021-Q2-B and five more, and BC-MCQ-SAMPLE-023.
- BC-QA-09005 (research/question-analysis/question-archetypes.md#BC-QA-09005 Coordinate of a particle recovered from an initial position): `common_givens` a velocity component, the position at one time, a second time; `asked_to_produce` an expression with an integral and the initial value, and a numerical coordinate. BC-FRQ-2021-Q2-C and three more.

What says this concept: the words total distance travelled, or a position asked at a time other than the one given. What says a different concept: net change or displacement alone (BC-CON-09007), or a speed at one instant (BC-CON-09009). The contrast pair sets a distance stem beside a position stem on one velocity, the position stem coming from BC-QA-09005, which loads the sibling concept BC-CON-09007 through BC-SKL-09020.

## Method choice

- st-1, BC-QA-09007. Method, `expected_solution_path[0]` and `[1]`: write the speed as the magnitude of the velocity, then integrate it over the interval. Rival, `wrong_approaches`: integrating the velocity components and then taking a magnitude. Separating feature: the magnitude is taken before the integral. Both cue fields exist, so the block is not inferred. The block carries the contrast pair.
- st-2, BC-QA-09005. Method, `expected_solution_path[0]`: the coordinate as the known value plus the definite integral of the matching component. Rival, `wrong_approaches` and `common_distractors`: omitting the initial condition, or using the other coordinate's starting value. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-09007, both bands, calculator. Draw: amplitude 4, frequency 3/2, vertical_scale 2, turning_square 3, end_time 5/2, units meters, framing bare. No published item on BC-QA-09007 carries this draw (content/items_*). Distance about 12.272 by SymPy.
- ex-2, BC-QA-09005, low band, calculator. Draw: x_amplitude 5, x_spread 2, y_rate 3, x_start 3, y_start -2, known_time 1, offset 2, requested x, direction later, given_as coordinates. No published item carries it. \(x(3)\) about 1.006.
- ex-2 is faded from step 3: steps 1 and 2 (the x-integral and the start plus the integral) are shown, the student writes the value, and step 3 then reveals. The fade falls there because the component choice and the initial value are the two decisions, and the evaluation is the last.
- Steps follow `expected_solution_path`: speed (new), the setup integral (new), the value (evaluate, three places); on ex-2 the integral (new), the start plus the integral (new), the value (evaluate). A fluent solver writes the setup and the value and holds the speed and the component choice.

No productive-failure opener targets this concept, so no comparison callout.

## Scoring

BC-QA-09007 lists BC-PT-99051 and BC-PT-99004; ex-1 tags nothing, since the brief cap has no room for a reader line beside the prediction and the contrast pair (inferred array). BC-QA-09005 lists BC-PT-99033, 99004 and others; ex-2 tags BC-PT-99033 on the start-plus-integral line and BC-PT-99004 on the value. The lines are `reader_checks` output.

Point losses research names for this shape: a distance setup where displacement was written (research/scoring/common-point-losses.md#Setup points, cr-23:8); fewer than three decimals (research/scoring/common-point-losses.md#Answer points); a variable expression equated to a number (research/scoring/common-point-losses.md#Notation points, cr-24:27).

## Traps

Four errors meet the skills, in the bundle's order: BC-ERR-08011, BC-ERR-09024, BC-ERR-99010, BC-ERR-99002. Low band all four, mid band the first two. Blocks 08011 and 99002 sit on ex-2's draw, blocks 09024 and 99010 on ex-1's. The first three carry `fix_prompt` true, since each pair is distinct; 99002 is equivalent (the same value, written with \(x(t)\) or \(x(3)\)), so its `fix_prompt` is false. Possible reason lines are dropped to fit the brief cap.

## Representations

None. The topic's Representations paragraph names BC-REP-14 and 12 and conversions to a speed and a distance; the figure it would carry is the orientation figure and the ki-1 motion, so a second block would repeat them.

## Prerequisite bridge

- BC-PRQ-06005 and BC-PRQ-08007, each from its `description_plain` and `failure_signature`.

## Time

The MCQ form of the distance draw is Section I Part B, calculator, 2.92 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part: 2 points, 3.33 minutes, and the coordinate part 3 points, 5.0 minutes (docs/lessons/unit-09/README.md, section 5). A fluent solver writes the setup integral with its limits and the value, and on the coordinate part writes the start plus the integral. The speed expression and the choice of component are held. The minutes go on the setup.

## Checks

- chk-1, completion of ex-1, both bands: the setup given, the value asked. Key 12.272.
- chk-2, isomorph, both bands, BC-QA-09007. Draw: amplitude 3, frequency 1, vertical_scale 3, turning_square 4, end_time 5/2, units feet, framing bare. Key 18.340.
- chk-3, MCQ, low band, BC-QA-09007. Draw: amplitude 2, frequency 3/2, vertical_scale 3, turning_square 2, end_time 3. Key 21.011. Distractors: 9.094, the length of the net change (BC-ERR-99010); 45.274, the speed with the vertical constant's sign reversed (BC-ERR-09024); 5.925, the interval cut at the sign change of the vertical velocity (BC-ERR-99010). Two distractors share BC-ERR-99010 because BC-ERR-08011 and BC-ERR-99002 belong to the coordinate archetype and a notation error has no value.

## Delivery

- orientation: figure. Rule 4: BC-REP-14 on both skills. The static path with its net change arrow.
- ki-1: motion. Rule 2: distance accumulating along a traced path, with the net change beside it; BC-MIS-08004's probe is a path that returns toward its start (docs/lessons/unit-09/README.md, section 6). Fallback four frames side by side, `reduced_motion` a cross-fade on the student's key press.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, st-2, ex-1 and its line, chk-1, the four error blocks, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 844 words, 5.7 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-08011, err-BC-ERR-09024, chk-2. 450 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-09010; BC-SKL-09025, BC-SKL-09026; BC-EK-FUN-8B2; ced:176
- BC-QA-09007, BC-QA-09005; BC-PT-99051, BC-PT-99033, BC-PT-99004
- BC-ERR-08011, BC-ERR-09024, BC-ERR-99010, BC-ERR-99002; BC-MIS-08004
- BC-PRQ-06005, BC-PRQ-08007
- sg-23:8, sg-24:6, sg-24:7
- research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions
- research/question-analysis/question-archetypes.md#BC-QA-09007 Total distance travelled by a particle in the plane
- research/exam/exam-structure.md#Section and part layout
- [inferred] the held steps; the untagged points on ex-1; every non-text delivery mode. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09010",
 "kind": "concept",
 "target_id": "BC-CON-09010",
 "unit": "09",
 "skills": [
  "BC-SKL-09025",
  "BC-SKL-09026"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "A particle has velocity \\(\\langle 4\\cos(3t/2),\\ 2(t^2-3)\\rangle\\) for \\(0\\le t\\le 5/2\\), and its vertical velocity changes sign at \\(t=\\sqrt3\\). Predict how the distance it travels compares with the length of its net change in position.",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Equal to that length",
    "is_key": false
   },
   {
    "id": "B",
    "label": "Greater than that length",
    "is_key": true
   },
   {
    "id": "C",
    "label": "Less than that length",
    "is_key": false
   }
  ],
  "resolution": "The distance is the integral of speed, about 12.272, and the net change has length about 4.830. The integral adds the length of the velocity vector at each instant.",
  "sources": [
   "BC-CON-09010",
   "research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions"
  ]
 },
 "orientation": {
  "text": "A response writes total distance as the definite integral of speed over the time interval and gives its value, or writes a coordinate at one time as the known coordinate plus the integral of that coordinate's velocity component.",
  "sources": [
   "BC-CON-09010",
   "research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-8B2",
   "depth": "core",
   "text": "The definite integral of the velocity vector is the displacement, and the definite integral of speed is the total distance travelled. Speed is \\(\\sqrt{x'(t)^2+y'(t)^2}\\), so the magnitude sits inside the integral. A coordinate at another time is its known value plus the integral of its own velocity component.",
   "notation": "integral of speed",
   "quote": null,
   "sources": [
    "BC-EK-FUN-8B2",
    "ced:176",
    "research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09007",
   "cue": "Two velocity components, a time interval, and total distance.",
   "method": "\\(\\int_a^b\\sqrt{x'(t)^2+y'(t)^2}\\,dt\\), the speed integrated over the interval.",
   "rival": "Integrate each component, then take the magnitude of the result.",
   "separating_feature": "Distance follows the path, so the magnitude is taken before integrating.",
   "sources": [
    "BC-QA-09007"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "A particle has velocity \\(\\langle 3\\cos 2t,\\ t^2-2\\rangle\\). Find the total distance it travels for \\(0\\le t\\le 2\\).",
     "archetype_id": "BC-QA-09007"
    },
    "not_this": {
     "text": "A particle has velocity \\(\\langle 3\\cos 2t,\\ t^2-2\\rangle\\) and is at \\((1,4)\\) at \\(t=0\\). Find its position at \\(t=2\\).",
     "why_not": "It asks for a position: each component is integrated and added to its start."
    },
    "feature": "Distance asks for path length, a position asks for coordinates."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-09005",
   "cue": "A velocity component, a position at one time, and a second time.",
   "method": "The known coordinate plus \\(\\int\\) of the matching velocity component between the two times.",
   "rival": "The integral alone, or the other coordinate's starting value.",
   "separating_feature": "The stem gives a position at one time and asks for a coordinate at another.",
   "sources": [
    "BC-QA-09005"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-09007",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "amplitude": 4,
    "frequency": "3/2",
    "vertical_scale": 2,
    "turning_square": 3,
    "end_time": "5/2",
    "units": "meters",
    "framing": "bare"
   },
   "problem": {
    "text": "A particle has velocity \\(v(t)=\\langle 4\\cos(3t/2),\\ 2(t^2-3)\\rangle\\). Using a calculator, find the total distance for \\(0\\le t\\le 5/2\\). Show the setup.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Distance is asked, so the speed is needed.",
     "why": "Speed is the length of the velocity vector.",
     "expr": "sqrt((4*cos(3*t/2))**2 + (2*(t**2 - 3))**2)",
     "relation": "new"
    },
    {
     "cue": "The stem gives 0 to 5/2.",
     "why": "Distance is the integral of speed.",
     "expr": "Integral(sqrt((4*cos(3*t/2))**2 + (2*(t**2 - 3))**2), (t, 0, 5/2))",
     "relation": "new"
    },
    {
     "cue": "Setup is on paper, so the calculator evaluates it.",
     "why": "Three places after the decimal point.",
     "expr": "12.272",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "12.272"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-09005",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "x_amplitude": 5,
    "x_spread": 2,
    "y_rate": 3,
    "x_start": 3,
    "y_start": -2,
    "known_time": 1,
    "offset": 2,
    "requested": "x",
    "direction": "later",
    "given_as": "coordinates"
   },
   "problem": {
    "text": "A particle has velocity \\(v(t)=\\langle 5\\cos(t^2/2),\\ 3\\sqrt t\\,e^{-t/2}\\rangle\\), with \\(x(1)=3\\) and \\(y(1)=-2\\). Using a calculator, find \\(x(3)\\). Show the setup.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "The x-coordinate is asked: use the x-velocity.",
     "why": "Only the matching component is integrated.",
     "expr": "Integral(5*cos(t**2/2), (t, 1, 3))",
     "relation": "new"
    },
    {
     "cue": "The stem gives \\(x(1)=3\\), the x start, not \\(y(1)\\).",
     "why": "The known value is added to the accumulated change.",
     "expr": "3 + Integral(5*cos(t**2/2), (t, 1, 3))",
     "relation": "new",
     "point_type_id": "BC-PT-99033"
    },
    {
     "cue": "Setup written, so the calculator evaluates it.",
     "why": "Three places after the decimal point.",
     "expr": "1.006",
     "relation": "evaluate",
     "subs": {},
     "approx": true,
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "1.006"
   },
   "fade_from": 3
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [],
   "lines": []
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
    "text": "\\(\\int_1^3 5\\cos(t^2/2)\\,dt\\approx -1.994\\)",
    "expr": "-1.994"
   },
   "right_step": {
    "text": "\\(3+\\int_1^3 5\\cos(t^2/2)\\,dt\\approx 1.006\\)",
    "expr": "1.006"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-08011"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-09024",
   "observed_behavior": "The integrand for total distance is an incorrect speed declared in an earlier part.",
   "scoring_consequence": "The integral point is earned and the answer point is not (sg-23:8).",
   "wrong_step": {
    "text": "A sign slip in the speed: \\(\\int_0^{5/2}\\sqrt{(4\\cos(3t/2))^2+(2(t^2+3))^2}\\,dt\\approx 26.547\\)",
    "expr": "26.547"
   },
   "right_step": {
    "text": "\\(\\int_0^{5/2}\\sqrt{(4\\cos(3t/2))^2+(2(t^2-3))^2}\\,dt\\approx 12.272\\)",
    "expr": "12.272"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-09024"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99010",
   "observed_behavior": "Responses integrate velocity without an absolute value, or split the interval incorrectly, and report the net change as the total distance travelled.",
   "scoring_consequence": "The setup point for total distance is not earned; the numerical answer point follows the setup.",
   "wrong_step": {
    "text": "The length of the net change: \\(\\sqrt{\\left(\\int x'\\,dt\\right)^2+\\left(\\int y'\\,dt\\right)^2}\\approx 4.830\\)",
    "expr": "4.830"
   },
   "right_step": {
    "text": "The integral of speed: \\(\\int_0^{5/2}\\sqrt{x'(t)^2+y'(t)^2}\\,dt\\approx 12.272\\)",
    "expr": "12.272"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-99010"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99002",
   "observed_behavior": "Responses join unequal objects with an equals sign, for example writing a general expression in t equal to the value of that expression at one instant, or stringing several lines of work together with equals signs.",
   "scoring_consequence": "The presentation point or the setup point is lost, and in some parts the response becomes ineligible for later points in that part.",
   "wrong_step": {
    "text": "\\(x(t)=1.006\\)",
    "expr": "x(t) = 1.006"
   },
   "right_step": {
    "text": "\\(x(3)=1.006\\)",
    "expr": "1.006"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-99002"
   ],
   "fix_prompt": false
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(x(1)\\) is a value, not the function."
  },
  {
   "prq_id": "BC-PRQ-08007",
   "text": "Speed is a root of squares, not a sum."
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
   "archetype_id": "BC-QA-09007",
   "parameter_draw": {
    "amplitude": 4,
    "frequency": "3/2",
    "vertical_scale": 2,
    "turning_square": 3,
    "end_time": "5/2",
    "units": "meters",
    "framing": "bare"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The integral of speed is \\(\\int_0^{5/2}\\sqrt{(4\\cos(3t/2))^2+(2(t^2-3))^2}\\,dt\\). Using a calculator, find the total distance.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "12.272"
   },
   "steps": [
    {
     "text": "The setup.",
     "expr": "Integral(sqrt((4*cos(3*t/2))**2 + (2*(t**2 - 3))**2), (t, 0, 5/2))",
     "relation": "new"
    },
    {
     "text": "Calculator.",
     "expr": "12.272",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09025"
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
   "archetype_id": "BC-QA-09007",
   "parameter_draw": {
    "amplitude": 3,
    "frequency": "1",
    "vertical_scale": 3,
    "turning_square": 4,
    "end_time": "5/2",
    "units": "feet",
    "framing": "bare"
   },
   "stem": {
    "text": "A particle has velocity \\(\\langle 3\\cos t,\\ 3(t^2-4)\\rangle\\). Using a calculator, find the total distance it travels for \\(0\\le t\\le 5/2\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "18.340"
   },
   "steps": [
    {
     "text": "Speed.",
     "expr": "sqrt((3*cos(t))**2 + (3*(t**2 - 4))**2)",
     "relation": "new"
    },
    {
     "text": "The setup.",
     "expr": "Integral(sqrt((3*cos(t))**2 + (3*(t**2 - 4))**2), (t, 0, 5/2))",
     "relation": "new"
    },
    {
     "text": "Calculator.",
     "expr": "18.340",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09025"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-09007",
   "parameter_draw": {
    "amplitude": 2,
    "frequency": "3/2",
    "vertical_scale": 3,
    "turning_square": 2,
    "end_time": "3",
    "units": "meters",
    "framing": "bare"
   },
   "stem": {
    "text": "A particle has velocity \\(\\langle 2\\cos(3t/2),\\ 3(t^2-2)\\rangle\\). Using a calculator, find the total distance it travels for \\(0\\le t\\le 3\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "21.011"
   },
   "steps": [
    {
     "text": "Speed.",
     "expr": "sqrt((2*cos(3*t/2))**2 + (3*(t**2 - 2))**2)",
     "relation": "new"
    },
    {
     "text": "The setup.",
     "expr": "Integral(sqrt((2*cos(3*t/2))**2 + (3*(t**2 - 2))**2), (t, 0, 3))",
     "relation": "new"
    },
    {
     "text": "Calculator.",
     "expr": "21.011",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "9.094",
     "error_path": "BC-ERR-99010",
     "derivation": "the length of the net change in position, from the integrals of the two components"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "21.011",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "45.274",
     "error_path": "BC-ERR-09024",
     "derivation": "the speed carried in with the sign of the vertical constant reversed"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "5.925",
     "error_path": "BC-ERR-99010",
     "derivation": "the interval cut at the time the vertical velocity changes sign, and only the first piece integrated"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09025"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-14 on BC-SKL-09025 and BC-SKL-09026; not promoted, the orientation states what a response shows and asks for no reading",
   "sources": [
    "BC-SKL-09025",
    "BC-SKL-09026"
   ],
   "spec": {
    "kind": "parametric_path",
    "representations": [
     "BC-REP-14"
    ],
    "x": "8*sin(3*t/2)/3",
    "y": "2*t**3/3 - 6*t",
    "t_range": [
     0,
     2.5
    ],
    "marks": [
     {
      "t": 0
     },
     {
      "t": 2.5
     }
    ],
    "labels": [
     {
      "text": "start",
      "placement": "inside"
     },
     {
      "text": "end",
      "placement": "inside"
     },
     {
      "text": "net change in position",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same path static, with the start, the end and the net change arrow labelled",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: distance accumulating along a traced path; the frames set the distance travelled beside the net change, which separates them on a path that turns; rule 4, BC-REP-14, for the static fallback",
   "sources": [
    "BC-SKL-09025",
    "BC-MIS-08004"
   ],
   "spec": {
    "kind": "parametric_trace",
    "representations": [
     "BC-REP-14",
     "BC-REP-09"
    ],
    "x": "8*sin(3*t/2)/3",
    "y": "2*t**3/3 - 6*t",
    "frames": [
     {
      "t": 0
     },
     {
      "t": 0.8
     },
     {
      "t": 1.7
     },
     {
      "t": 2.5
     }
    ],
    "drawn": [
     "the path traced up to the frame's t",
     "the particle at (x(t), y(t))",
     "the arrow from the start to the particle"
    ],
    "readouts": [
     "distance travelled so far",
     "length of the net change so far"
    ],
    "labels": [
     {
      "text": "distance so far",
      "placement": "inside"
     },
     {
      "text": "net change so far",
      "placement": "inside"
     },
     {
      "text": "t",
      "placement": "inside"
     }
    ]
   },
   "fallback": "four frames side by side (t = 0, 0.8, 1.7, 2.5), static, each with its two readouts inside",
   "keyboard": "Right arrow steps to the next frame, Left arrow to the previous; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame"
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
   "block": "err-BC-ERR-09024",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99010",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99002",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-08011",
  "err-BC-ERR-09024",
  "err-BC-ERR-99010",
  "err-BC-ERR-99002",
  "ex-1"
 ],
 "read_minutes": {
  "full": 5.7,
  "brief": 3.0
 },
 "word_count": {
  "full": 844,
  "brief": 450
 },
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "The definite integral of the velocity vector is the displacement, from which the position may be determined, and the definite integral of speed is the total distance travelled"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the setup integral and the value, and holds the speed expression in the head.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "ex-1 tags no point type, because the prediction, contrast pair and a reader line of 88 or more words do not fit the brief cap; ex-2 tags BC-PT-99033 and BC-PT-99004.",
   "settles": "A brief cap that admits a second reader line."
  },
  {
   "claim": "Every non-text delivery mode chosen here is a proposal.",
   "settles": "The modality A/B on skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-09010",
  "BC-SKL-09025",
  "BC-SKL-09026",
  "BC-EK-FUN-8B2",
  "ced:176",
  "BC-QA-09007",
  "BC-QA-09005",
  "BC-PT-99051",
  "BC-PT-99033",
  "BC-PT-99004",
  "BC-ERR-08011",
  "BC-ERR-09024",
  "BC-ERR-99010",
  "BC-ERR-99002",
  "BC-MIS-08004",
  "BC-PRQ-06005",
  "BC-PRQ-08007",
  "sg-23:8",
  "sg-24:6",
  "sg-24:7",
  "research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions",
  "research/question-analysis/question-archetypes.md#BC-QA-09007 Total distance travelled by a particle in the plane",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
