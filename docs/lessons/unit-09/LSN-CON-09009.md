---
title: LSN-CON-09009 Speed as the magnitude of the velocity vector
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09009, speed as the square root of the sum of the squares of the two velocity components, evaluated at a time or solved for a stated speed, built from authoring_bundle("BC-CON-09009") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09009 Speed as the magnitude of the velocity vector

Concept BC-CON-09009 (skills BC-SKL-09023, 09024, 09028), topic 9.6 of Unit 9, BC only (ced:176), loaded by BC-QA-09006 (speed and the time a speed is reached) and, for BC-SKL-09028, BC-QA-09004 (the acceleration vector with its setup, taught fully in BC-CON-09006). Hard parent inside the unit: BC-CON-09006 (docs/lessons/unit-09/README.md, section 1).

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The core claim is that speed is the magnitude of the velocity vector. The stem gives the components 3.510 and 0.500 at t = 1/2, which are ex-1's velocity components. Key A, 3.546. The distractors are the sum of the components (BC-ERR-09013's form) and the larger component alone (BC-MIS-09011). The Pythagorean relation for a length answers it before any rule. The resolution gives the magnitude with no verdict word. Source: BC-CON-09009 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-09009 `description_plain` (speed is the length of the velocity vector, not either component) and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions): the MCQ forms ask for the speed at a time, and the free-response part asks for a time at which the speed takes a value, scoring the setup and the answer (sg-23:6). No count, no frequency.

## Key ideas

One BC-EK, BC-EK-FUN-8B1 (ced:176), maps the three skills, so one core block, both bands. ki-1 paraphrases the Required mathematical knowledge paragraphs Velocity, speed, acceleration and Notation (parentheses inside a squared component; radian mode). No anchor quote. Notation line: the concept's `notation`.

## Recognition

BC-QA-09006 is the archetype for BC-SKL-09023 and 09024 (research/question-analysis/question-archetypes.md#BC-QA-09006 Speed of a particle in planar motion). BC-QA-09004 loads BC-SKL-09028 and is taught in BC-CON-09006.

- `common_givens`: two velocity components, and a time or a target speed. `asked_to_produce`: a magnitude expression, and a numerical speed or time. `typical_wording`: find the speed of the particle at the given time, or the first time at which the speed equals the stated value, and show the work.
- The signal in the stem: the word speed, not velocity vector or acceleration. The difficulty variables are whether a value or a time is requested and whether the first such time is demanded.
- Shapes: one part of the calculator active free response, BC-FRQ-2021-Q2-A, BC-FRQ-2015-Q2-C, BC-FRQ-2023-Q2-B, BC-FRQ-2024-Q2-A.

The near miss of the contrast pair is the acceleration vector stem from BC-QA-09004 (outside the block's archetype): the same velocity and time, but a vector of derivatives is asked. The `common_distractors` entry "the magnitude of the acceleration" is a second near miss.

## Method choice

- st-1, BC-QA-09006. Cue from `common_givens`. Method, `expected_solution_path`: square both velocity components, add and take the square root, then evaluate at the time or set equal to the target and solve. Rival: `common_distractors` "the sum of the two components" and "one component alone". Separating feature: speed is one magnitude. Both cue fields exist, so the block is not inferred. The block carries the contrast pair, a speed stem beside an acceleration stem.

## Solution path

- ex-1, BC-QA-09006, both bands, calculator. Draw: amplitude 4, frequency 1, growth 2, time 1/2, target 6, units feet, request value. \(v(t)=\langle 4\cos t, 2t^2\rangle\), speed at 1/2 is 3.546 by SymPy. No published item on BC-QA-09006 carries this draw (ITM-GEN-09006-00 to 21).
- ex-2, low band, calculator. Draw: amplitude 2, frequency 1, growth 3, time 3/4, target 7, units meters, request time. \(v(t)=\langle 2\cos t, 3t^2\rangle\), the first time the speed is 7 is 1.527 by a numerical solve.
- ex-2 is faded from step 3: steps 1 and 2 (the target and the speed expression) are shown, the student writes the equation and the time, and steps 3 and 4 then reveal. The fade falls there because the magnitude repeats ex-1, and the equation with its solve is what a time request adds.
- The steps follow `expected_solution_path`. A fluent solver writes the magnitude and the value or the equation, and holds the squaring.
- No productive-failure comparison: BC-CON-09009 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-09006 lists BC-PT-99050, 99052, 99004. ex-1 tags BC-PT-99050, the speed setup, on the magnitude line; ex-2 tags BC-PT-99050 and BC-PT-99004. BC-PT-99052 is the acceleration point and belongs to BC-CON-09006. The lines are `reader_checks` output.

Point losses from research: the words speed equals the value alone do not earn the setup, a bare time earns neither point, and a parenthesis error in a squared component costs the setup but not the answer point (sg-23:6, sg-24:5) (research/scoring/common-point-losses.md#Setup points).

## Traps

Six errors meet the skills; the cap of 4 keeps the first four in bundle order: BC-ERR-09013 and 09014 (linked BC-MIS-09005, 09011, high), BC-ERR-09022, BC-ERR-09023. BC-ERR-99002 and 99021 fall past the cap. Low band all four, mid band the first two.

- err-BC-ERR-09013: the sum of the components, on ex-1's draw. Distinct, `fix_prompt` true. Possible reason, BC-MIS-09005.
- err-BC-ERR-09014: \(2t^4\) for \((2t^2)^2\), on ex-1's draw. Distinct, `fix_prompt` true. No possible reason line.
- err-BC-ERR-09022: the time with no equation, on ex-2's draw. The value is the same and the difference lives in the sentence, so `relation` equivalent and `fix_prompt` false.
- err-BC-ERR-09023: degree mode, on ex-1's draw. Distinct, `fix_prompt` true.

## Representations

None. The topic's Representations paragraph names the conversion of component rates to a speed; the orientation and ki-1 figures already carry it.

## Prerequisite bridge

- BC-PRQ-08001, BC-PRQ-08007, BC-PRQ-09001, BC-PRQ-09003, each from its `description_plain` and `failure_signature`, gated by state.

## Time

BC-QA-09006 is an MCQ in Section I Part B, 2.92 minutes (research/exam/exam-structure.md#Section and part layout); as a free response part it scores 2 points, 3.33 minutes (docs/lessons/unit-09/README.md, section 5). A fluent solver writes the magnitude expression and the value, or the equation and the time; the squaring is held [inferred]. No target.

## Checks

- chk-1, completion of ex-1, both bands: the magnitude given, the value asked. Key 3.546.
- chk-2, isomorph, both bands, calculator. Draw: amplitude 5, frequency 1/2, growth 3, time 5/4, target 8, units meters, request value. Key 6.198.
- chk-3, MCQ, low band, calculator. Draw: amplitude 3, frequency 1/2, growth 2, time 3/2, target 6, units feet, request value. Key 5.007. Distractors: 6.695, the components added (BC-ERR-09013); 3.866, the coefficient left unsquared (BC-ERR-09014); 5.408, degree mode (BC-ERR-09023).

## Delivery

- orientation: figure. Unit README section 6 names FUN-8B1 for BC-CON-09009. Rule 3 of the README: BC-REP-14 on BC-SKL-09023, 09024 and 09028. The velocity vector with its two legs and its length.
- ki-1: interactive. Rule 3 promoted (TEMPLATE rule 4): BC-QA-09006 `common_givens` names a time or a target speed and `difficulty_variables` whether a value or a time is requested; the stem asks for a reading. One slider, the time; the control drives the process's own picture, not a representation the stem carries.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, the four error blocks, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 772 words, 5.2 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-09013, err-BC-ERR-09014, chk-2. 450 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-09009; BC-SKL-09023, BC-SKL-09024, BC-SKL-09028; BC-EK-FUN-8B1; ced:176, ced:173
- BC-QA-09006, BC-QA-09004; BC-PT-99050, BC-PT-99004
- BC-ERR-09013, BC-ERR-09014, BC-ERR-09022, BC-ERR-09023; BC-MIS-09005, BC-MIS-09011, BC-MIS-09008
- BC-PRQ-08001, BC-PRQ-08007, BC-PRQ-09001, BC-PRQ-09003
- sg-23:6, sg-24:5
- research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions
- research/question-analysis/question-archetypes.md#BC-QA-09006 Speed of a particle in planar motion
- research/scoring/common-point-losses.md#Setup points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The solve step of ex-2, the interactive mode and the held steps, each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09009",
 "kind": "concept",
 "target_id": "BC-CON-09009",
 "unit": "09",
 "skills": [
  "BC-SKL-09023",
  "BC-SKL-09024",
  "BC-SKL-09028"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "A particle has velocity components \\(3.510\\) and \\(0.500\\) at \\(t=\\frac12\\). Predict its speed.",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(3.546\\)",
    "is_key": true
   },
   {
    "id": "B",
    "label": "\\(4.010\\)",
    "is_key": false
   },
   {
    "id": "C",
    "label": "\\(3.510\\)",
    "is_key": false
   }
  ],
  "resolution": "Speed is the length of the velocity vector, \\(\\sqrt{3.510^2+0.500^2}\\approx3.546\\), a single number.",
  "sources": [
   "BC-CON-09009",
   "research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions"
  ]
 },
 "orientation": {
  "text": "Speed is the magnitude of the velocity vector, one number. A response shows the root of the sum of squares of the components, then the value, or the equation for a stated speed.",
  "sources": [
   "BC-CON-09009",
   "research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-8B1",
   "depth": "core",
   "text": "Speed is the magnitude of the velocity vector, the square root of the sum of the squares of its components, each component squared whole. To find when the speed has a stated value, set that expression equal to the value and solve, with the calculator in radian mode.",
   "notation": "speed as the magnitude of velocity",
   "quote": null,
   "sources": [
    "BC-EK-FUN-8B1",
    "ced:176",
    "research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09006",
   "cue": "Two velocity components, and a time or a target speed.",
   "method": "Square both components, add, take the root, then evaluate or solve.",
   "rival": "The sum of the components, or one alone.",
   "separating_feature": "Speed asks for one magnitude, not a vector or a component.",
   "sources": [
    "BC-QA-09006"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "A particle has velocity \\(\\langle 3\\cos t, 2t\\rangle\\). Find its speed at \\(t=1\\).",
     "archetype_id": "BC-QA-09006"
    },
    "not_this": {
     "text": "A particle has velocity \\(\\langle 3\\cos t, 2t\\rangle\\). Find its acceleration vector at \\(t=1\\).",
     "why_not": "It asks for a vector, the derivative of the velocity."
    },
    "feature": "Speed is one magnitude; acceleration is a vector of derivatives."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-09006",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "amplitude": "4",
    "frequency": "1",
    "growth": "2",
    "time": "1/2",
    "target": "6",
    "units": "feet",
    "request": "value"
   },
   "problem": {
    "text": "A particle has velocity \\(\\langle 4\\cos t, 2t^2\\rangle\\), in feet per second. Find its speed at \\(t=\\frac12\\) to three decimals, showing the setup.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Speed asks for one number.",
     "why": "It is the length of the velocity vector."
    },
    {
     "cue": "Square each component whole.",
     "why": "Root of the sum of squares.",
     "expr": "sqrt((4*cos(t))**2 + (2*t**2)**2)",
     "relation": "new",
     "point_type_id": "BC-PT-99050"
    },
    {
     "cue": "Evaluate at \\(t=\\frac12\\).",
     "why": "Radian mode.",
     "expr": "3.546",
     "relation": "evaluate",
     "subs": {
      "t": "1/2"
     },
     "approx": true
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "3.546"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-09006",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "amplitude": "2",
    "frequency": "1",
    "growth": "3",
    "time": "3/4",
    "target": "7",
    "units": "meters",
    "request": "time"
   },
   "fade_from": 3,
   "problem": {
    "text": "A particle has velocity \\(\\langle 2\\cos t, 3t^2\\rangle\\), in meters per second. Find the first time \\(t>0\\) at which its speed is 7, to three decimals, showing the work.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "A target speed is given.",
     "why": "The speed expression is set equal to it."
    },
    {
     "cue": "Speed expression.",
     "why": "Root of the sum of squares.",
     "expr": "sqrt((2*cos(t))**2 + (3*t**2)**2)",
     "relation": "new",
     "point_type_id": "BC-PT-99050"
    },
    {
     "cue": "Set equal to 7.",
     "why": "The equation is what earns the setup.",
     "expr": "sqrt((2*cos(t))**2 + (3*t**2)**2) = 7",
     "relation": "new"
    },
    {
     "cue": "Solve with the calculator.",
     "why": "First positive root, radian mode.",
     "expr": "1.527",
     "relation": "new",
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "1.527"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99050"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99050",
     "text": "Speed of a parametric or vector-valued motion. Earned by: The square root of the sum of squares of the two component derivatives, with the setup visible (sg-24:5, sg-22:7). Not earned by: A bare statement that speed equals the target value, which sg-23:6 states does not earn the point."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99050",
    "BC-PT-99004"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99050",
     "text": "Speed of a parametric or vector-valued motion. Earned by: The square root of the sum of squares of the two component derivatives, with the setup visible (sg-24:5, sg-22:7). Not earned by: A bare statement that speed equals the target value, which sg-23:6 states does not earn the point."
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
    "text": "\\(4\\cos t+2t^2\\), giving \\(4.010\\).",
    "expr": "4*cos(t) + 2*t**2"
   },
   "right_step": {
    "text": "\\(\\sqrt{(4\\cos t)^2+(2t^2)^2}\\), giving \\(3.546\\).",
    "expr": "sqrt((4*cos(t))**2 + (2*t**2)**2)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-09005",
    "text": "adds the horizontal and vertical rates rather than combining them by the Pythagorean relation"
   },
   "sources": [
    "BC-ERR-09013",
    "BC-MIS-09005"
   ]
  },
  {
   "error_id": "BC-ERR-09014",
   "observed_behavior": "A squared component is written so that only part of it is squared.",
   "scoring_consequence": "The setup point is lost while the answer point remains available, and the same error is not assessed again in a later part (sg-23:6, sg-23:8).",
   "wrong_step": {
    "text": "\\(\\sqrt{(4\\cos t)^2+2t^4}\\).",
    "expr": "sqrt((4*cos(t))**2 + 2*t**4)"
   },
   "right_step": {
    "text": "\\(\\sqrt{(4\\cos t)^2+(2t^2)^2}\\).",
    "expr": "sqrt((4*cos(t))**2 + (2*t**2)**2)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09014"
   ]
  },
  {
   "error_id": "BC-ERR-09022",
   "observed_behavior": "A time at which the speed takes a value is given with no equation and no speed expression.",
   "scoring_consequence": "Neither the setup point nor the answer point is earned; the words speed equals the value alone also fail to earn the setup point (sg-23:6).",
   "wrong_step": {
    "text": "On ex-2, \\(t\\approx1.527\\) alone.",
    "expr": "1.527"
   },
   "right_step": {
    "text": "On ex-2, \\(\\sqrt{(2\\cos t)^2+(3t^2)^2}=7\\), so \\(t\\approx1.527\\).",
    "expr": "1.527"
   },
   "relation": "equivalent",
   "fix_prompt": false,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09022",
    "BC-MIS-09008"
   ]
  },
  {
   "error_id": "BC-ERR-09023",
   "observed_behavior": "Trigonometric values throughout a question are computed in degree measure, producing internally consistent but wrong numbers.",
   "scoring_consequence": "The response does not earn the first point it would otherwise have earned and is generally eligible for the rest (sg-23:6, sg-23:7).",
   "wrong_step": {
    "text": "Degree mode: \\(4.031\\).",
    "expr": "4.031"
   },
   "right_step": {
    "text": "Radian mode: \\(3.546\\).",
    "expr": "3.546"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09023"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-08001",
   "text": "Set an expression equal to a value and solve."
  },
  {
   "prq_id": "BC-PRQ-08007",
   "text": "A magnitude is a root of squares."
  },
  {
   "prq_id": "BC-PRQ-09001",
   "text": "Horizontal entry first."
  },
  {
   "prq_id": "BC-PRQ-09003",
   "text": "Radian mode on the calculator."
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
    3,
    4
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
   "archetype_id": "BC-QA-09006",
   "parameter_draw": {
    "amplitude": "4",
    "frequency": "1",
    "growth": "2",
    "time": "1/2",
    "target": "6",
    "units": "feet",
    "request": "value"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The speed is \\(\\sqrt{(4\\cos t)^2+(2t^2)^2}\\). Give it at \\(t=\\frac12\\) to three decimals.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "3.546"
   },
   "steps": [
    {
     "text": "The magnitude.",
     "expr": "sqrt((4*cos(t))**2 + (2*t**2)**2)",
     "relation": "new",
     "point_type_id": "BC-PT-99050"
    },
    {
     "text": "The calculator.",
     "expr": "3.546",
     "relation": "evaluate",
     "subs": {
      "t": "1/2"
     },
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09023"
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
   "archetype_id": "BC-QA-09006",
   "parameter_draw": {
    "amplitude": "5",
    "frequency": "1/2",
    "growth": "3",
    "time": "5/4",
    "target": "8",
    "units": "meters",
    "request": "value"
   },
   "stem": {
    "text": "A particle has velocity \\(\\langle 5\\cos(t/2), 3t^2\\rangle\\), in meters per second. Find its speed at \\(t=\\frac54\\) to three decimals.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "6.198"
   },
   "steps": [
    {
     "text": "The magnitude.",
     "expr": "sqrt((5*cos(t/2))**2 + (3*t**2)**2)",
     "relation": "new",
     "point_type_id": "BC-PT-99050"
    },
    {
     "text": "The calculator.",
     "expr": "6.198",
     "relation": "evaluate",
     "subs": {
      "t": "5/4"
     },
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09023"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-09006",
   "parameter_draw": {
    "amplitude": "3",
    "frequency": "1/2",
    "growth": "2",
    "time": "3/2",
    "target": "6",
    "units": "feet",
    "request": "value"
   },
   "stem": {
    "text": "A particle has velocity \\(\\langle 3\\cos(t/2), 2t^2\\rangle\\), in feet per second. With a calculator, its speed at \\(t=\\frac32\\) is",
    "command_verb": "identify"
   },
   "key": {
    "form": "numeric",
    "expr": "5.007"
   },
   "steps": [
    {
     "text": "The magnitude.",
     "expr": "sqrt((3*cos(t/2))**2 + (2*t**2)**2)",
     "relation": "new"
    },
    {
     "text": "The calculator.",
     "expr": "5.007",
     "relation": "evaluate",
     "subs": {
      "t": "3/2"
     },
     "approx": true
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "6.695",
     "error_path": "BC-ERR-09013",
     "derivation": "the two components added instead of combined as a magnitude"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "3.866",
     "error_path": "BC-ERR-09014",
     "derivation": "the second component squared as 2t^4, the coefficient left unsquared"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "5.007",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "5.408",
     "error_path": "BC-ERR-09023",
     "derivation": "the cosine evaluated with the calculator in degree mode"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09023"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3 of the unit README: BC-REP-14 on BC-SKL-09023, 09024 and 09028",
   "sources": [
    "BC-SKL-09023"
   ],
   "spec": {
    "kind": "vector_diagram",
    "tail": [
     0,
     0
    ],
    "head": [
     3.51,
     0.5
    ],
    "legs": [
     {
      "axis": "x",
      "value": "x'(t)"
     },
     {
      "axis": "y",
      "value": "y'(t)"
     }
    ],
    "labels": [
     {
      "text": "velocity vector at t = 1/2",
      "placement": "inside"
     },
     {
      "text": "speed = its length",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same diagram static with both labels",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 3 promoted (TEMPLATE rule 4): BC-REP-14 on BC-SKL-09023, 09024 and 09028; BC-QA-09006 common_givens a time or a target speed and difficulty_variables whether a value or a time is requested, so the stem asks for a reading of the speed against the time. The control drives the process's own picture",
   "sources": [
    "BC-SKL-09023",
    "BC-SKL-09024",
    "BC-QA-09006"
   ],
   "spec": {
    "kind": "vector_diagram",
    "vector": "<4*cos(t), 2*t**2>",
    "legs": [
     {
      "axis": "x",
      "value": "x'(t)"
     },
     {
      "axis": "y",
      "value": "y'(t)"
     }
    ],
    "controls": [
     {
      "type": "slider",
      "parameter": "t",
      "range": [
       0,
       2
      ],
      "step": 0.25,
      "start": 0.5
     }
    ],
    "labels": [
     {
      "text": "x'(t)",
      "placement": "inside"
     },
     {
      "text": "y'(t)",
      "placement": "inside"
     },
     {
      "text": "speed = length of the vector",
      "placement": "inside"
     }
    ],
    "question": "At which time does the length of the vector reach a stated value?"
   },
   "fallback": "three static frames at t = 0.5, 1 and 1.5 with the two legs and the length labelled inside",
   "keyboard": "Tab focuses the slider; left and right arrow keys change t by 0.25; the components and the length are announced"
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
   "block": "err-BC-ERR-09022",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09023",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-09013",
  "err-BC-ERR-09014",
  "err-BC-ERR-09022",
  "err-BC-ERR-09023",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "Speed is the magnitude of the velocity vector, so it is the square root of the sum of the squares of the components."
  }
 ],
 "inferred": [
  {
   "claim": "The solve step of ex-2 and of the time answers is not recomputed by the checker, whose solve relation tests a root exactly and a decimal root fails; the root 1.527 was found with a numerical solver in SymPy and its equation step is a new chain.",
   "settles": "A checker relation that accepts a root to three decimals."
  },
  {
   "claim": "The interactive mode on ki-1 serves this concept better than text or a static figure.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "A fluent solver writes the magnitude expression and the value or the equation, and holds the squaring of each component.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-09009",
  "BC-SKL-09023",
  "BC-SKL-09024",
  "BC-SKL-09028",
  "BC-EK-FUN-8B1",
  "ced:176",
  "ced:173",
  "BC-QA-09006",
  "BC-QA-09004",
  "BC-PT-99050",
  "BC-PT-99004",
  "sg-23:6",
  "sg-24:5",
  "BC-ERR-09013",
  "BC-ERR-09014",
  "BC-ERR-09022",
  "BC-ERR-09023",
  "BC-MIS-09005",
  "BC-MIS-09011",
  "BC-MIS-09008",
  "BC-PRQ-08001",
  "BC-PRQ-08007",
  "BC-PRQ-09001",
  "BC-PRQ-09003",
  "research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions",
  "research/question-analysis/question-archetypes.md#BC-QA-09006 Speed of a particle in planar motion",
  "research/scoring/common-point-losses.md#Setup points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 772,
  "brief": 450
 },
 "read_minutes": {
  "full": 5.2,
  "brief": 3.0
 }
}
```
