---
title: LSN-CON-09004 Arc length of a parametric curve
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09004, the length of a parametric curve as the integral of the square root of the sum of the squared rates over an interval that traces it once, and the total distance of a particle, built from authoring_bundle("BC-CON-09004") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09004 Arc length of a parametric curve

Concept BC-CON-09004 (skills BC-SKL-09011 to BC-SKL-09014), topic 9.3 of Unit 9, BC only (ced:173), loaded by BC-QA-09003 (family arc-length) and BC-QA-09007 (family parametric-motion). Its Unit 9 hard parent is BC-CON-09001 (docs/lessons/unit-09/README.md, section 1); the outside hard parents BC-SKL-06034, 08056 and 08059 mean a definite integral and the function arc length are assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's own rates at t = 1 (dx/dt = 8, dy/dt = 2cos 1) with the core claim that a small piece of the curve has length sqrt of dx/dt squared plus dy/dt squared, times dt. Key B. The distractors are the rates added, dx/dt alone and the sum of squares with no root. The piece is the hypotenuse of a right triangle with legs dx and dy, which the Pythagorean theorem gives before any method is taught. The resolution states the hypotenuse and the general form, with no verdict. Source: BC-CON-09004 and the topic section the key idea cites.

## Orientation

From BC-CON-09004 `description_plain` ("The length is the integral of the magnitude of the pair of rates") and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.3 Finding Arc Lengths of Curves Given by Parametric Equations): the MCQ asks which integral gives the length, the free response asks for total distance with the integral and the value scored separately. No count, no frequency.

## Key ideas

All four skills map to BC-EK-CHA-6B1 (ced:173): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs Parametric arc length, Length and distance (the particle case, BC-EK-FUN-8B2 on ced:176), Tracing and Notation. Notation line from the concept's `notation`. No anchor quote: the cached page prints the sentence with a bc only tag inside it, so the block paraphrases.

## Recognition

BC-QA-09003 (research/question-analysis/question-archetypes.md#BC-QA-09003 Length of a parametric curve): `common_givens` "a parametric pair or a velocity vector" and "a parameter or time interval"; `asked_to_produce` "a definite integral of a radical integrand" and "a numerical length"; `typical_wording` "find the length of the curve on the stated parameter interval, or the total distance travelled by the particle over the stated time interval, and show the setup". It lists no official examples; the Q2 distance parts are filed under BC-QA-09007 (BC-FRQ-2021-Q2-B, 2022-Q2-D, 2015-Q2-D, 2023-Q2-D, 2024-Q2-B, 2018-Q2-D; BC-MCQ-SAMPLE-023), whose `common_givens` are "two velocity components" and "a time interval".

The near miss of the contrast pair is the displacement on the same velocity, `common_distractors` "the magnitude of the displacement" and "the integral of one component alone", which belongs to BC-CON-09007. What says "not this concept": displacement, position or change in position asked for; a curve given as y in x, which is the function arc length (BC-CON-08021).

## Method choice

- st-1, BC-QA-09003. Cue from `common_givens` and `asked_to_produce`. Method `expected_solution_path[0..2]`. Rival: `wrong_approaches` "adding the component rates before squaring" and `common_distractors` "the sum of the two component integrals". Separating feature: one radical over both rates. It carries the contrast pair, a length stem beside a displacement stem on one interval.
- st-2, BC-QA-09007, low band only. Cue from `common_givens`; method `expected_solution_path[0..1]`; rival `wrong_approaches` "integrating the velocity components and then taking a magnitude".

## Solution path

- ex-1, BC-QA-09003, both bands, calculator. Draw: stretch 4, height 2, frequency 1, end 2, units meters, given curve. \(x=4t^2\), \(y=2\sin t\); \(\int_0^2\sqrt{(8t)^2+(2\cos t)^2}\,dt=16.5674\) by SymPy, reported 16.567. No published item on BC-QA-09003 carries this draw (content/items_gen_unit09, ITM-GEN-09003-00 to 21).
- ex-2, BC-QA-09007, low band, calculator, faded from step 2. Draw: amplitude 4, frequency 1, vertical_scale 2, turning_square 1, end_time 2, units feet, framing bare. Velocity \(\langle4\cos t,2(t^2-1)\rangle\); distance 6.7251 by SymPy, reported 6.725. Step 1 (the speed) is shown and the student writes the integral and value; steps 2 and 3 then reveal, because the setup is the scored step. No published item on BC-QA-09007 carries this draw (ITM-GEN-09007-00 to 20).
- A fluent solver writes both rates and the integral with limits; the evaluation is held. No productive-failure comparison: BC-CON-09004 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-09003 lists no point types, so ex-1 carries no scoring lines and no tag. BC-QA-09007 lists BC-PT-99051 and BC-PT-99004; ex-2 tags the integral step and the value step, and the lines are `reader_checks` output.

Point losses from research: the parenthesis lost inside a squared component costs the setup point once and is not assessed again in a later part (research/scoring/notation-requirements.md#Parentheses, sg-23:6, sg-23:8); displacement setup where total distance was asked (research/scoring/common-point-losses.md#Setup points, BC-ERR-99010); a calculator value with no setup earns nothing (BC-ERR-99021, same heading).

## Traps

Bundle order is BC-ERR-09013, 09014, 09016, 99010, 99029, 99019, 99021. The blocks are BC-ERR-09013, 09014 and 99010, on ex-1's draw, all `fix_prompt` true. BC-ERR-09016 (an interval that traces the curve more than once) is left out: BC-QA-09003's parameter_spec keeps x increasing, so no draw of the archetype has a retraced arc to show wrong beside right. The tracing condition is taught in ki-1 and its motion entry (library gap). Mid band shows the first two.

- err-BC-ERR-09013: the integrand 8t + 2cos t against the radical. No possible reason line.
- err-BC-ERR-09014: \(8t^2\) in place of \((8t)^2\).
- err-BC-ERR-99010: 16.103, the straight-line distance from start to end, against 16.567.

## Representations

None. The path figure and the tracing frames are carried by the orientation and ki-1 delivery entries (the topic's Representations paragraph names an integral expression converted to a statement of distance travelled).

## Prerequisite bridge

- BC-PRQ-06005, BC-PRQ-08006, BC-PRQ-08007 and BC-PRQ-09004, each from its `description_plain` and `failure_signature`.

## Time

Both archetypes are calculator: Section I Part B, 2.92 minutes (research/exam/exam-structure.md#Section and part layout); as a free response part, 2 points, 3.33 minutes (docs/lessons/unit-09/README.md, section 5). A fluent solver writes both rates and the integral with limits; squaring each rate and the evaluation are held. The minutes go on the setup.

## Checks

- chk-1, completion of ex-1, both bands: the rates given, the length asked. Key 16.567.
- chk-2, isomorph, both bands. Draw: stretch 3, height 4, frequency 1, end 3/2, units meters, given curve. Key 8.626 (SymPy 8.62599).
- chk-3, MCQ, low band. Draw: stretch 2, height 4, frequency 1/2, end 2, units feet, given curve. Key 9.103 (SymPy 9.10257). Distractors: 11.366, the rates added (BC-ERR-09013); 5.590, \(4t^2\) unsquared inside the root (BC-ERR-09014); 8.679, the straight-line distance (BC-ERR-99010). No published draw matches any of these.

## Delivery

- orientation: figure. Rule 4 (README rule 3): BC-REP-12 on BC-SKL-09011 to 09014; the path with its interval marked.
- ki-1: motion. Rule 2: a parameter interval that revisits an arc is a curve being traced, and the retraced arc is highlighted on the second pass. The frames illustrate a circle traced past one turn, not a draw of the lesson. Reduced motion steps the frames on a key press.
- ex-1, ex-2, the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, st-2, ex-1, chk-1, the three error blocks, ex-2 (faded from step 2) and its lines, chk-2, chk-3. 767 words, 5.3 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-09013, err-BC-ERR-09014, chk-2. 427 words, 3.0 minutes.
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-09004; BC-SKL-09011 to BC-SKL-09014; BC-EK-CHA-6B1; ced:173
- BC-QA-09003, BC-QA-09007; BC-PT-99051, BC-PT-99004
- BC-ERR-09013, BC-ERR-09014, BC-ERR-99010
- BC-PRQ-06005, BC-PRQ-08006, BC-PRQ-08007, BC-PRQ-09004
- sg-23:6, sg-23:8
- research/units/unit-09-parametric-polar-vector.md#9.3 Finding Arc Lengths of Curves Given by Parametric Equations
- research/question-analysis/question-archetypes.md#BC-QA-09003 Length of a parametric curve
- research/exam/exam-structure.md#Section and part layout
- [inferred] The untagged ex-1; the held steps; every non-text delivery mode. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09004",
 "kind": "concept",
 "target_id": "BC-CON-09004",
 "unit": "09",
 "skills": [
  "BC-SKL-09011",
  "BC-SKL-09012",
  "BC-SKL-09013",
  "BC-SKL-09014"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "At \\(t=1\\) on the curve \\(x=4t^2\\), \\(y=2\\sin t\\), \\(dx/dt=8\\) and \\(dy/dt=2\\cos1\\). Predict the length of the piece of curve traced from \\(t=1\\) to \\(t=1+dt\\).",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\((8+2\\cos1)\\,dt\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(\\sqrt{64+4\\cos^21}\\,dt\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(8\\,dt\\)",
    "is_key": false
   },
   {
    "id": "D",
    "label": "\\((64+4\\cos^21)\\,dt\\)",
    "is_key": false
   }
  ],
  "resolution": "The piece is the hypotenuse of legs \\(8\\,dt\\) and \\(2\\cos1\\,dt\\), so its length is \\(\\sqrt{64+4\\cos^21}\\,dt\\), and \\(\\sqrt{(dx/dt)^2+(dy/dt)^2}\\,dt\\) in general.",
  "sources": [
   "BC-CON-09004",
   "research/units/unit-09-parametric-polar-vector.md#9.3 Finding Arc Lengths of Curves Given by Parametric Equations"
  ]
 },
 "orientation": {
  "text": "The length of a parametric curve is the integral of \\(\\sqrt{(dx/dt)^2+(dy/dt)^2}\\) over the parameter interval that traces it once. For a particle it is the total distance. A response writes the integral with limits, then the value.",
  "sources": [
   "BC-CON-09004",
   "research/units/unit-09-parametric-polar-vector.md#9.3 Finding Arc Lengths of Curves Given by Parametric Equations"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-6B1",
   "depth": "core",
   "text": "With \\(x'\\) and \\(y'\\) continuous, the length is \\(\\int_a^b\\sqrt{(dx/dt)^2+(dy/dt)^2}\\,dt\\). Each rate is squared in full and the radical covers the sum. The interval must trace the curve once, because a repeated arc is counted twice. For a particle the integrand is speed and the value is total distance.",
   "notation": "parametric arc length integral",
   "quote": null,
   "sources": [
    "BC-EK-CHA-6B1",
    "ced:173",
    "research/units/unit-09-parametric-polar-vector.md#9.3 Finding Arc Lengths of Curves Given by Parametric Equations"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09003",
   "cue": "A parametric pair or velocity, an interval, and a length.",
   "method": "Write both rates, then \\(\\int_a^b\\sqrt{(x')^2+(y')^2}\\,dt\\).",
   "rival": "Adding the rates, or squaring without parentheses.",
   "separating_feature": "One radical covers both rates, not a sum of two pieces.",
   "sources": [
    "BC-QA-09003"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Position \\(x=3t^2\\), \\(y=4\\sin t\\). Find the length of the curve for \\(0\\le t\\le\\frac32\\).",
     "archetype_id": "BC-QA-09003"
    },
    "not_this": {
     "text": "Velocity \\(\\langle6t,4\\cos t\\rangle\\). Find the displacement for \\(0\\le t\\le\\frac32\\).",
     "why_not": "It asks for net change in position, the integral of each component."
    },
    "feature": "Length along the path, not net change in position."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-09007",
   "cue": "Two velocity components, a time interval, and total distance.",
   "method": "Write the speed as a magnitude, then integrate it over the interval.",
   "rival": "Integrating the components, then taking a magnitude.",
   "separating_feature": "Distance integrates the speed, not the velocity.",
   "sources": [
    "BC-QA-09007"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-09003",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "stretch": "4",
    "height": "2",
    "frequency": "1",
    "end": "2",
    "units": "meters",
    "given": "curve"
   },
   "problem": {
    "text": "A curve is defined by \\(x=4t^2\\) and \\(y=2\\sin t\\). Using a calculator, find the length of the curve for \\(0\\le t\\le2\\), to three decimals.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Differentiate \\(x\\).",
     "why": "Length needs both rates.",
     "expr": "8*t",
     "relation": "new"
    },
    {
     "cue": "Differentiate \\(y\\).",
     "why": "Same parameter.",
     "expr": "2*cos(t)",
     "relation": "new"
    },
    {
     "cue": "A length: root of the squares, over the interval.",
     "why": "Each rate squared whole, one radical.",
     "expr": "Integral(sqrt((8*t)**2 + (2*cos(t))**2), (t, 0, 2))",
     "relation": "new"
    },
    {
     "cue": "Three places asked.",
     "why": "The setup is written before the value.",
     "expr": "16.567",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "16.567"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-09007",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "amplitude": "4",
    "frequency": "1",
    "vertical_scale": "2",
    "turning_square": "1",
    "end_time": "2",
    "units": "feet",
    "framing": "bare"
   },
   "problem": {
    "text": "A particle moves with velocity \\(\\langle4\\cos t,\\,2(t^2-1)\\rangle\\). Using a calculator, find the total distance traveled for \\(0\\le t\\le2\\), to three decimals.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Total distance: the speed first.",
     "why": "Speed is the magnitude of the velocity.",
     "expr": "sqrt((4*cos(t))**2 + (2*(t**2-1))**2)",
     "relation": "new"
    },
    {
     "cue": "Integrate the speed over the interval.",
     "why": "The written integral is the setup.",
     "expr": "Integral(sqrt((4*cos(t))**2 + (2*(t**2-1))**2), (t, 0, 2))",
     "relation": "new",
     "point_type_id": "BC-PT-99051"
    },
    {
     "cue": "Three places asked.",
     "why": "The calculator value, rounded once.",
     "expr": "6.725",
     "relation": "evaluate",
     "subs": {},
     "approx": true,
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "6.725"
   },
   "fade_from": 2
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99051",
    "BC-PT-99004"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99051",
     "text": "Arc length or total distance integrand. Earned by: A definite integral whose integrand is the square root of one plus the square of the derivative, or the square root of the sum of the squares of the component derivatives (sg-26:19, sg-22:9). Not earned by: An unsupported value (sg-22:9); an integrand imported from an incorrect speed function, which sg-23:8 allows for this point but not for the answer point. Notation: sg-26:19 requires the limits to be numerical but not correct for this point, and assesses the derivative expression and the straight boundaries in the following point."
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
   "error_id": "BC-ERR-09013",
   "observed_behavior": "The speed or the arc length integrand is the sum of the two rates rather than the square root of the sum of their squares.",
   "scoring_consequence": "The setup point is lost.",
   "wrong_step": {
    "text": "The rates added.",
    "expr": "Integral(8*t + 2*cos(t), (t, 0, 2))"
   },
   "right_step": {
    "text": "Root of the sum of squares.",
    "expr": "Integral(sqrt((8*t)**2 + (2*cos(t))**2), (t, 0, 2))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09013"
   ]
  },
  {
   "error_id": "BC-ERR-09014",
   "observed_behavior": "A squared component is written so that only part of it is squared.",
   "scoring_consequence": "The setup point is lost while the answer point remains available, and the same error is not assessed again in a later part (sg-23:6, sg-23:8).",
   "wrong_step": {
    "text": "\\(8t^2\\) in place of \\((8t)^2\\).",
    "expr": "Integral(sqrt(8*t**2 + (2*cos(t))**2), (t, 0, 2))"
   },
   "right_step": {
    "text": "\\((8t)^2\\).",
    "expr": "Integral(sqrt((8*t)**2 + (2*cos(t))**2), (t, 0, 2))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09014"
   ]
  },
  {
   "error_id": "BC-ERR-99010",
   "observed_behavior": "Responses integrate velocity without an absolute value, or split the interval incorrectly, and report the net change as the total distance travelled.",
   "scoring_consequence": "The setup point for total distance is not earned; the numerical answer point follows the setup.",
   "wrong_step": {
    "text": "The straight-line distance from start to end.",
    "expr": "16.103"
   },
   "right_step": {
    "text": "The length along the curve.",
    "expr": "16.567"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-99010"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(x'(t)\\) is a rate, read at the stated input."
  },
  {
   "prq_id": "BC-PRQ-08006",
   "text": "Three places after the point, rounded once, at the end."
  },
  {
   "prq_id": "BC-PRQ-08007",
   "text": "Two components combine as a root of squares, not a sum."
  },
  {
   "prq_id": "BC-PRQ-09004",
   "text": "Name the interval that traces the curve exactly once."
  }
 ],
 "time": {
  "exam_part": "I-B",
  "budget_minutes": 2.92,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    3
   ]
  },
  "skipped_steps": {
   "ex-1": [
    4
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
   "archetype_id": "BC-QA-09003",
   "parameter_draw": {
    "stretch": "4",
    "height": "2",
    "frequency": "1",
    "end": "2",
    "units": "meters",
    "given": "curve"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(dx/dt=8t\\) and \\(dy/dt=2\\cos t\\). Find the length for \\(0\\le t\\le2\\), to three decimals.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "16.567"
   },
   "steps": [
    {
     "text": "The length integral.",
     "expr": "Integral(sqrt((8*t)**2 + (2*cos(t))**2), (t, 0, 2))",
     "relation": "new"
    },
    {
     "text": "To three decimals.",
     "expr": "16.567",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09012"
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
   "archetype_id": "BC-QA-09003",
   "parameter_draw": {
    "stretch": "3",
    "height": "4",
    "frequency": "1",
    "end": "3/2",
    "units": "meters",
    "given": "curve"
   },
   "stem": {
    "text": "A curve is defined by \\(x=3t^2\\) and \\(y=4\\sin t\\). Using a calculator, find its length for \\(0\\le t\\le\\frac32\\), to three decimals.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "8.626"
   },
   "steps": [
    {
     "text": "\\(dx/dt\\).",
     "expr": "6*t",
     "relation": "new"
    },
    {
     "text": "\\(dy/dt\\).",
     "expr": "4*cos(t)",
     "relation": "new"
    },
    {
     "text": "The length integral.",
     "expr": "Integral(sqrt((6*t)**2 + (4*cos(t))**2), (t, 0, 3/2))",
     "relation": "new"
    },
    {
     "text": "To three decimals.",
     "expr": "8.626",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09011"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-09003",
   "parameter_draw": {
    "stretch": "2",
    "height": "4",
    "frequency": "1/2",
    "end": "2",
    "units": "feet",
    "given": "curve"
   },
   "stem": {
    "text": "A curve is defined by \\(x=2t^2\\) and \\(y=4\\sin(t/2)\\). Using a calculator, find its length for \\(0\\le t\\le2\\), in feet.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "9.103"
   },
   "steps": [
    {
     "text": "\\(dx/dt\\).",
     "expr": "4*t",
     "relation": "new"
    },
    {
     "text": "\\(dy/dt\\).",
     "expr": "2*cos(t/2)",
     "relation": "new"
    },
    {
     "text": "The length integral.",
     "expr": "Integral(sqrt((4*t)**2 + (2*cos(t/2))**2), (t, 0, 2))",
     "relation": "new"
    },
    {
     "text": "To three decimals.",
     "expr": "9.103",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "11.366",
     "error_path": "BC-ERR-09013",
     "derivation": "the integral of 4t + 2cos(t/2), the rates added"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "5.590",
     "error_path": "BC-ERR-09014",
     "derivation": "4t^2 under the radical in place of (4t)^2"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "9.103",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "8.679",
     "error_path": "BC-ERR-99010",
     "derivation": "the straight-line distance from (0, 0) to (8, 4 sin 1)"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09012"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4 (README rule 3): BC-REP-12 on BC-SKL-09011 to 09014; the path with the stated interval marked",
   "sources": [
    "BC-SKL-09011"
   ],
   "spec": {
    "kind": "parametric_path",
    "representations": [
     "BC-REP-12"
    ],
    "x": "4*t**2",
    "y": "2*sin(t)",
    "t_range": [
     0,
     2
    ],
    "marks": [
     {
      "t": 0
     },
     {
      "t": 2
     }
    ],
    "drawn": [
     "the path",
     "the endpoints at t = 0 and t = 2"
    ],
    "labels": [
     {
      "text": "t = 0",
      "placement": "inside"
     },
     {
      "text": "t = 2",
      "placement": "inside"
     },
     {
      "text": "length of this arc",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same path static with both endpoints and their labels",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: a parameter interval that traces part of the curve twice is a curve being traced; BC-QA-09003 difficulty_variables name whether the interval traces the curve once. The illustration is a circle traced from t = 0 to 4 pi, not a draw of the lesson",
   "sources": [
    "BC-SKL-09014",
    "BC-QA-09003"
   ],
   "spec": {
    "kind": "parametric_trace",
    "representations": [
     "BC-REP-12"
    ],
    "x": "3*cos(t)",
    "y": "3*sin(t)",
    "frames": [
     {
      "t": 3.1416
     },
     {
      "t": 6.2832
     },
     {
      "t": 9.4248
     },
     {
      "t": 12.5664
     }
    ],
    "drawn": [
     "the path traced up to the frame's t",
     "the retraced arc highlighted from the second pass"
    ],
    "labels": [
     {
      "text": "first pass",
      "placement": "inside"
     },
     {
      "text": "retraced arc",
      "placement": "inside"
     },
     {
      "text": "t",
      "placement": "inside"
     }
    ]
   },
   "fallback": "four frames side by side, static, each with its labels inside",
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
   "block": "err-BC-ERR-09013",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09014",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99010",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-09013",
  "err-BC-ERR-09014",
  "err-BC-ERR-99010",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "A parameter interval that traces part of the curve twice gives a length larger than the length of the curve."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-09003 carries no point_types, so ex-1 is untagged and carries no scoring lines; its integral point is taught through ex-2 on BC-QA-09007, which lists BC-PT-99051 and BC-PT-99004.",
   "settles": "Point types on BC-QA-09003, which its scoring_pattern already describes as an integral point and a value point."
  },
  {
   "claim": "A fluent solver writes both rates and the integral with limits and holds the calculator evaluation.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "Every non-text delivery choice.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-09004",
  "BC-SKL-09011",
  "BC-SKL-09012",
  "BC-SKL-09013",
  "BC-SKL-09014",
  "BC-EK-CHA-6B1",
  "ced:173",
  "BC-QA-09003",
  "BC-QA-09007",
  "BC-PT-99051",
  "BC-PT-99004",
  "BC-ERR-09013",
  "BC-ERR-09014",
  "BC-ERR-99010",
  "BC-PRQ-06005",
  "BC-PRQ-08006",
  "BC-PRQ-08007",
  "BC-PRQ-09004",
  "sg-23:6",
  "sg-23:8",
  "research/units/unit-09-parametric-polar-vector.md#9.3 Finding Arc Lengths of Curves Given by Parametric Equations",
  "research/question-analysis/question-archetypes.md#BC-QA-09003 Length of a parametric curve",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 767,
  "brief": 427
 },
 "read_minutes": {
  "full": 5.3,
  "brief": 3.0
 }
}
```
