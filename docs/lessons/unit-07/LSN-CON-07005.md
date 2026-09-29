---
title: LSN-CON-07005 Solution curves read off a slope field
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-07005, reading solution behaviour from a slope field or from the differential equation without solving, built from authoring_bundle("BC-CON-07005") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-07005 Solution curves read off a slope field

Concept BC-CON-07005 (skills BC-SKL-07014 to BC-SKL-07018), topic 7.4 of Unit 7, loaded by BC-QA-07001, 07005, 07002 and 07010. Hard parent BC-CON-07004 (docs/lessons/unit-07/README.md, section 1).

## Prediction

Both bands, served first, before any rule. Form `mcq`, three options, on ex-1's equation \(dy/dx=(y-1)(x+1)(x-2)\) at the point \((1,2)\), a point that is not the example's critical point. The student says whether the solution is rising or falling there without solving. Key: falling, because the slope there is negative. The resolution states what the right side gives at the point (the slope \(-2\)) and that its sign gives the direction, and never grades the choice. Sources: BC-CON-07005 and the 7.4 topic section that ki-1 cites (BC-EK-FUN-7C3, ced:140). Delivery: text. [inferred] Settled by the prediction's first-try rate in the build plan.

## Orientation

Served text, from BC-CON-07005 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-07-differential-equations.md#7.4 Reasoning Using Slope Fields): a solution follows the segments and never crosses the equilibrium row; its rise, fall and turning points come from the sign of the right side, without solving. No count, no frequency.

## Key ideas

All five skills map to BC-EK-FUN-7C3 (ced:140), one core block, both bands, from the Solution curve and Reading behaviour paragraphs. Anchor quote from ced:140. The Reading behaviour paragraph says the field shows "whether" solutions approach a horizontal asymptote, so ki-1 says a solution need not approach the flat row: SymPy gives y = e^(x^2/2) + 2 for dy/dx = x(y - 2), y(0) = 3, which tends to infinity both ways, and y = 2 + e^(-x/2) for dy/dx = (2 - y)/2, y(0) = 3, which approaches 2 from above. "Never crosses" is the sketch standard's correct side condition (sg-23:9, BC-PT-99065); it holds where solutions through a point are unique, as for this lesson's polynomial right sides [inferred].

## Recognition

- BC-QA-07010 (research/question-analysis/question-archetypes.md#BC-QA-07010 Behaviour of a solution obtained from the differential equation itself): "find the input at which the modelled quantity has a critical point and determine whether it is ... a relative minimum, a relative maximum, or neither", with an equation, a bound on the quantity and a range.
- BC-QA-07001 (research/question-analysis/question-archetypes.md#BC-QA-07001 Solution curve sketched on a supplied slope field): "sketch the solution curve through the given point" on a printed field; the opening part of the FRQ (BC-FRQ-2023-Q3-A, BC-FRQ-2024-Q3-A).
- BC-QA-07005 (research/question-analysis/question-archetypes.md#BC-QA-07005 Direction of an approximation decided from the second derivative of a solution): "overestimate or underestimate ... give a reason".

What says "not this concept": "sketch the slope field ... at the indicated points" asks for segments (BC-CON-07004).

The contrast pair on st-1 sets a classification stem beside its near miss. Where the near miss comes from: the sibling concept BC-CON-07004, the slope-field construction stem, which shares the equation and the phrase "indicated points" but calls for drawn segments and not for a critical point's type. The separating feature is what the stem asks for.

## Method choice

Three strategy blocks, one per family (de-qualitative-behaviour, slope-field, euler), each from `expected_solution_path[0]` and `wrong_approaches`. All three archetypes carry `asked_to_produce` and `common_givens`, so none is tagged inferred. The reader prints its own labels, so no strategy field starts with one. st-1 carries the contrast pair: a critical point to classify beside a slope field to sketch.

## Solution path

- ex-1, BC-QA-07010, both bands. Draw: bound_side above, outside_root -1, inside_root 2, level 1, sign 1, scale 1, letters xy: dy/dx = (y - 1)(x + 1)(x - 2), x > 0, y > 1. ex-1 is on BC-QA-07010 rather than the primary BC-QA-07001 because the first two error blocks, which the mid band serves, are classification errors [inferred].
- ex-2, BC-QA-07001, low band. Draw: stability stable, offset 1, level 2, start_x 0, rate 1/2, letters xy: dy/dx = (2 - y)/2 through (0, 3).
- ex-2 is faded, `fade_from` 4: steps 1 to 3 (the slope formula, the slope at (0, 3) and the equation of the flat row) are shown, and the student solves for the flat row and states the curve before steps 4 and 5 reveal. The fade falls there because the last two steps are the solve and the sketch, the parts the example teaches and the ones a sketch point scores (BC-PT-99065).
- Neither draw equals a published draw. A fluent solver writes the zero, the input and the sign sentence; the bound's use is held.

## Scoring

ex-1 tags BC-PT-99010 on the classification; ex-2 tags BC-PT-99065 on the curve. Lines are reader_checks output. The sketch point needs all four conditions (sg-23:9, sg-24:9); a field explanation cites the sign of the segments' slopes (research/scoring/justification-requirements.md#Reasons about slope fields and concavity; sg-26:11). BC-PT-99005 on the input is not tagged, to hold the brief band [inferred].

## Traps

Ten active errors meet the skills; the first four in the bundle's order: BC-ERR-05013, 05021, 05025, 07013. All four are distinct, so every block carries `fix_prompt` true. BC-ERR-05025 and 05021 on ex-1's draw; BC-ERR-05013 on dy/dx = (y - 1)(x - 2)^2, y > 1, where the right side vanishes at 2 without a sign change; BC-ERR-07013 on ex-2's draw, where the field depends on y only. Possible reason on BC-ERR-05025 from BC-MIS-05028.

## Representations

None as a separate block; the orientation interactive and the ki-1 motion carry the field.

## Prerequisite bridge

- BC-PRQ-07006, from `description_plain` and `failure_signature`.

## Time

BC-QA-07001 is `no_calculator`, the opening part of a free-response question, so Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout); the sketch is 1 point and the behaviour part 3 points of 9 (docs/lessons/unit-07/README.md, section 5).

## Checks

- chk-1, completion of ex-1: x = 2 given; classify. Key: relative minimum at x = 2.
- chk-2, isomorph. Draw: below, outside -2, inside 3, level 0, sign -1, scale 2, ty; dy/dt = -2y(t + 2)(t - 3), t > 0, y < 0. Key: relative minimum at t = 3.
- chk-3, MCQ, low band. Draw: above, outside -3, inside 4, level 2, sign -1, scale 1, xy. Key: relative maximum at x = 4 with the sign change. Distractors carry BC-ERR-05021, 05013, 05025.

## Delivery

- orientation: interactive. Rule 4 promoted: BC-REP-07 and 02 on BC-SKL-07014 to 07017; BC-QA-07001 `common_givens` "an initial condition" and `difficulty_variables` "where the initial point sits relative to it", with a reading asked (docs/lessons/unit-07/README.md, section 6) [inferred].
- ki-1: motion. Rule 2: a curve being traced through the field.
- pr-1: text. Rule 6, a prediction on ex-1's equation with nothing to draw.
- ex-1, ex-2, error blocks: step_reveal. Rule 1.

Figure presence: the orientation interactive and the ki-1 motion are drawn blocks, so the record carries no `no_figure_reason`.

## Band plan

- Low (full): prediction, orientation, bridge, ki-1, st-1 with its contrast, st-2, st-3, ex-1 with its line, chk-1, four error blocks, ex-2 faded with its line, chk-2, chk-3. 789 words, 5.3 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, bridge, ki-1, st-1 with its contrast, ex-1 with its line, chk-1, err-BC-ERR-05013, err-BC-ERR-05021, chk-2. 449 words, 3.0 minutes (cap 450 and 3). The orientation, ki-1, the st-1 cue, the bridge and ex-1's cues and whys were shortened to fit; no anchor quote or scoring tag was dropped.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-07005; BC-SKL-07014 to BC-SKL-07018; BC-EK-FUN-7C3; ced:140
- BC-QA-07001, BC-QA-07002, BC-QA-07005, BC-QA-07010; BC-FRQ-2023-Q3-A, BC-FRQ-2024-Q3-A; BC-PT-99010, BC-PT-99065; sg-23:9, sg-24:9, sg-26:11
- BC-ERR-05013, BC-ERR-05021, BC-ERR-05025, BC-ERR-07013; BC-MIS-05028
- BC-PRQ-07006
- research/units/unit-07-differential-equations.md#7.4 Reasoning Using Slope Fields
- research/question-analysis/question-archetypes.md#BC-QA-07001 Solution curve sketched on a supplied slope field
- research/question-analysis/question-archetypes.md#BC-QA-07005 Direction of an approximation decided from the second derivative of a solution
- research/question-analysis/question-archetypes.md#BC-QA-07010 Behaviour of a solution obtained from the differential equation itself
- research/scoring/justification-requirements.md#Reasons about slope fields and concavity
- research/exam/exam-structure.md#Section and part layout
- [inferred] ex-1 on BC-QA-07010; BC-PT-99005 untagged; interactive and motion modes; BC-ERR-05013 on an off-spec draw with a squared factor; never crossing the flat row resting on uniqueness. Settled as listed in the machine record.

## Machine record

```json
{
 "id": "LSN-CON-07005",
 "kind": "concept",
 "target_id": "BC-CON-07005",
 "unit": "07",
 "skills": [
  "BC-SKL-07014",
  "BC-SKL-07015",
  "BC-SKL-07016",
  "BC-SKL-07017",
  "BC-SKL-07018"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. A solution of \\(dy/dx=(y-1)(x+1)(x-2)\\) passes through \\((1,2)\\). Rising or falling there, without solving?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Falling: the slope there is negative.",
    "is_key": true
   },
   {
    "id": "B",
    "label": "Rising: \\(y\\) is above 1.",
    "is_key": false
   },
   {
    "id": "C",
    "label": "Not determined without solving.",
    "is_key": false
   }
  ],
  "resolution": "The slope there is \\((2-1)(1+1)(1-2)=-2\\), so it falls. The right side's sign gives the direction.",
  "sources": [
   "BC-CON-07005",
   "BC-EK-FUN-7C3",
   "ced:140",
   "research/units/unit-07-differential-equations.md#7.4 Reasoning Using Slope Fields"
  ]
 },
 "orientation": {
  "text": "A solution follows the segments. The right side's sign gives its rises, falls and turns, without solving.",
  "sources": [
   "BC-CON-07005",
   "research/units/unit-07-differential-equations.md#7.4 Reasoning Using Slope Fields"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-7C3",
   "depth": "core",
   "text": "A solution curve is tangent to the segment at every point it passes. The sign of the right side says where it rises or falls, and a sign change marks a turn. It never crosses the flat row.",
   "notation": "solution curve; horizontal asymptote",
   "quote": {
    "text": "Solutions to differential equations are functions or families of functions.",
    "source": "ced:140"
   },
   "sources": [
    "BC-EK-FUN-7C3",
    "ced:140",
    "BC-PT-99065",
    "sg-23:9",
    "research/units/unit-07-differential-equations.md#7.4 Reasoning Using Slope Fields"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-07010",
   "cue": "A critical point to classify from the equation.",
   "method": "The right side set equal to zero.",
   "rival": "Solving the equation first.",
   "separating_feature": "The equation is dy/dx, so its sign is read directly.",
   "sources": [
    "BC-QA-07010"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "\\(dy/dx=(y-3)(x+2)(x-4)\\), \\(y>3\\), \\(x>0\\). Find the critical point and classify it.",
     "archetype_id": "BC-QA-07010"
    },
    "not_this": {
     "text": "Sketch the slope field of \\(dy/dx=(y-3)(x+2)\\) at the indicated points.",
     "why_not": "It asks for segments at points."
    },
    "feature": "The stem asks for a critical point's type."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-07001",
   "cue": "A printed field, an equation and an initial condition: sketch the curve through the point.",
   "method": "Locate the initial point, then follow the segments right and left to the edges.",
   "rival": "Solving the equation and plotting the formula.",
   "separating_feature": "The field is printed, so the curve is read from it.",
   "sources": [
    "BC-QA-07001"
   ],
   "evidence_tag": "verified"
  },
  {
   "id": "st-3",
   "archetype_id": "BC-QA-07005",
   "cue": "An approximation is computed; the stem asks over or under, with a reason.",
   "method": "Differentiate the right side, then substitute the equation for dy/dx.",
   "rival": "Solving the equation and comparing numerically.",
   "separating_feature": "Direction is concavity, so the second derivative's sign decides.",
   "sources": [
    "BC-QA-07005"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-07010",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "bound_side": "above",
    "outside_root": -1,
    "inside_root": 2,
    "level": 1,
    "sign": 1,
    "scale": 1,
    "letters": "xy"
   },
   "problem": {
    "text": "dy/dx = (y - 1)(x + 1)(x - 2), with y > 1 for x > 0. Find the critical point for x > 0 and classify it.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Critical point: right side zero.",
     "why": "No solving.",
     "expr": "(y - 1)*(x + 1)*(x - 2) = 0",
     "relation": "new"
    },
    {
     "cue": "y > 1, x > 0.",
     "why": "Only x - 2 vanishes.",
     "expr": "2",
     "relation": "solve",
     "variable": "x"
    },
    {
     "cue": "Sign on each side.",
     "why": "Other factors are positive.",
     "expr": "x - 2",
     "relation": "new"
    },
    {
     "cue": "Left of 2.",
     "why": "Negative.",
     "expr": "-1",
     "relation": "evaluate",
     "subs": {
      "x": "1"
     }
    },
    {
     "cue": "Sign change.",
     "why": "Relative minimum at x = 2.",
     "point_type_id": "BC-PT-99010"
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "relative minimum at x = 2"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-07001",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "stability": "stable",
    "offset": 1,
    "level": 2,
    "start_x": 0,
    "rate": "1/2",
    "letters": "xy"
   },
   "problem": {
    "text": "The field of dy/dx = (2 - y)/2 is printed. Sketch the solution through (0, 3).",
    "command_verb": "sketch"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Locate the start.",
     "why": "Slope there.",
     "expr": "(2 - y)/2",
     "relation": "new"
    },
    {
     "cue": "At (0, 3).",
     "why": "Falling.",
     "expr": "-1/2",
     "relation": "evaluate",
     "subs": {
      "y": "3"
     }
    },
    {
     "cue": "Find the flat row.",
     "why": "The curve cannot cross it.",
     "expr": "(2 - y)/2 = 0",
     "relation": "new"
    },
    {
     "cue": "Solve.",
     "why": "y = 2.",
     "expr": "2",
     "relation": "solve",
     "variable": "y"
    },
    {
     "cue": "Follow segments both ways to the edges.",
     "why": "Above y = 2, flattening toward it on the right.",
     "point_type_id": "BC-PT-99065"
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "decreasing curve through (0, 3), above y = 2, edge to edge"
   },
   "fade_from": 4
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99010"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99010",
     "text": "Justification by sign analysis of a derivative. Earned by: A statement that the derivative is positive on one side and negative on the other, closed by a global claim about the whole interval (sg-25:5, sg-25:9). Not earned by: A local argument only, such as a bare First or Second Derivative Test with no statement that the critical point is the only one on the interval (sg-25:5, sg-22:12)."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99065"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99065",
     "text": "Solution curve sketched on a slope field. Earned by: A curve through the given point that extends close to both edges of the given field, with no obvious conflict with the drawn segments, and that respects the stated asymptote (sg-23:9). Not earned by: A curve crossing the horizontal segments that mark the equilibrium value (sg-23:9)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-05013",
   "observed_behavior": "The response reports a relative maximum or minimum at an input where the derivative is zero but keeps its sign on both sides.",
   "scoring_consequence": "The single answer with reason point is lost.",
   "wrong_step": {
    "text": "dy/dx = (y - 1)(x - 2)^2, y > 1, is 0 at 2, so an extremum at 2.",
    "expr": "FiniteSet(2)"
   },
   "right_step": {
    "text": "Positive on both sides of 2: no extremum.",
    "expr": "EmptySet"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05013"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05021",
   "observed_behavior": "The response reports a relative maximum where the derivative changes from negative to positive, or the reverse.",
   "scoring_consequence": "The answer with reason point is lost.",
   "wrong_step": {
    "text": "Left sign read positive: maximum.",
    "expr": "1"
   },
   "right_step": {
    "text": "Negative: minimum.",
    "expr": "-1"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05021"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05025",
   "observed_behavior": "The response carries a critical point that lies outside the closed interval into the candidate comparison.",
   "scoring_consequence": "The justification point is lost because inputs other than the candidates appear in the argument.",
   "wrong_step": {
    "text": "x = -1 kept.",
    "expr": "FiniteSet(-1, 2)"
   },
   "right_step": {
    "text": "Only x = 2.",
    "expr": "FiniteSet(2)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05028",
    "text": "ignores what the situation permits"
   },
   "sources": [
    "BC-ERR-05025",
    "BC-MIS-05028"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07013",
   "observed_behavior": "The response claims the slope varies along a line on which the printed segments are identical, or the reverse.",
   "scoring_consequence": "The match to a candidate equation is made on a false feature.",
   "wrong_step": {
    "text": "Slopes read as changing along rows.",
    "expr": "x*(2 - y)/2"
   },
   "right_step": {
    "text": "y only.",
    "expr": "(2 - y)/2"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-07013"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-07006",
   "text": "Locate the initial point by its coordinates first."
  }
 ],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    5
   ],
   "ex-2": [
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    3,
    4
   ],
   "ex-2": [
    1,
    2,
    3,
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
   "archetype_id": "BC-QA-07010",
   "parameter_draw": {
    "bound_side": "above",
    "outside_root": -1,
    "inside_root": 2,
    "level": 1,
    "sign": 1,
    "scale": 1,
    "letters": "xy"
   },
   "completes": "ex-1",
   "stem": {
    "text": "dy/dx = (y - 1)(x + 1)(x - 2), y > 1: the critical input for x > 0 is 2. Classify it.",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "relative minimum at x = 2"
   },
   "steps": [
    {
     "text": "Sign is that of x - 2.",
     "expr": "x - 2",
     "relation": "new"
    },
    {
     "text": "Left of 2.",
     "expr": "-1",
     "relation": "evaluate",
     "subs": {
      "x": "1"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07018"
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
   "archetype_id": "BC-QA-07010",
   "parameter_draw": {
    "bound_side": "below",
    "outside_root": -2,
    "inside_root": 3,
    "level": 0,
    "sign": -1,
    "scale": 2,
    "letters": "ty"
   },
   "stem": {
    "text": "dy/dt = -2y(t + 2)(t - 3), y < 0. Find and classify the critical point for t > 0.",
    "command_verb": "find"
   },
   "key": {
    "form": "statement",
    "expr": "relative minimum at t = 3"
   },
   "steps": [
    {
     "text": "Right side zero.",
     "expr": "-2*y*(t + 2)*(t - 3) = 0",
     "relation": "new"
    },
    {
     "text": "t = 3.",
     "expr": "3",
     "relation": "solve",
     "variable": "t"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07018"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-07010",
   "parameter_draw": {
    "bound_side": "above",
    "outside_root": -3,
    "inside_root": 4,
    "level": 2,
    "sign": -1,
    "scale": 1,
    "letters": "xy"
   },
   "stem": {
    "text": "dy/dx = -(y - 2)(x + 3)(x - 4), y > 2. Which response earns the classification for x > 0?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "relative maximum at x = 4"
   },
   "steps": [
    {
     "text": "Right side zero.",
     "expr": "-(y - 2)*(x + 3)*(x - 4) = 0",
     "relation": "new"
    },
    {
     "text": "x = 4.",
     "expr": "4",
     "relation": "solve",
     "variable": "x"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "Maximum at x = 4: dy/dx goes from positive to negative.",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "Minimum at x = 4: dy/dx goes from positive to negative.",
     "error_path": "BC-ERR-05021",
     "derivation": "direction of the change reversed"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "Maximum at x = 4: dy/dx = 0 there.",
     "error_path": "BC-ERR-05013",
     "derivation": "no sign change argued"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "Maximum at x = 4, minimum at x = -3.",
     "error_path": "BC-ERR-05025",
     "derivation": "an input outside x > 0 kept"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07018"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a prediction on ex-1's equation with nothing to draw",
   "sources": [
    "BC-SKL-07018"
   ]
  },
  {
   "block": "orientation",
   "mode": "interactive",
   "reason": "rule 4 promoted: BC-REP-07, 02 on BC-SKL-07014; BC-QA-07001 common_givens an initial condition and difficulty_variables where the initial point sits, with a reading asked",
   "sources": [
    "BC-SKL-07014",
    "BC-SKL-07015",
    "BC-QA-07001"
   ],
   "spec": {
    "kind": "slope_field",
    "representations": [
     "BC-REP-07",
     "BC-REP-02"
    ],
    "equation": "dy/dx = (2 - y)/2",
    "window": {
     "x": [
      -3,
      3
     ],
     "y": [
      0,
      4
     ]
    },
    "controls": [
     {
      "type": "draggable_point",
      "start": [
       0,
       3
      ]
     }
    ],
    "drawn": [
     "the solution curve through the point, redrawn on each move"
    ],
    "labels": [
     {
      "text": "flat row y = 2",
      "placement": "inside",
      "at": "along y = 2"
     },
     {
      "text": "initial point",
      "placement": "inside",
      "at": "beside the point"
     }
    ],
    "question": "Which side of y = 2 does the curve stay on, and what does it approach?"
   },
   "fallback": "a static field with curves through (0, 3) and (0, 1), both approaching y = 2, labels inside",
   "keyboard": "Tab focuses the point; arrow keys move it one lattice step; Enter reads the curve's side and limit"
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: a solution curve traced through the field, tangent to each segment it passes",
   "sources": [
    "BC-EK-FUN-7C3",
    "BC-SKL-07014"
   ],
   "spec": {
    "kind": "field_trace",
    "representations": [
     "BC-REP-07",
     "BC-REP-02"
    ],
    "equation": "dy/dx = (2 - y)/2",
    "window": {
     "x": [
      -3,
      3
     ],
     "y": [
      0,
      4
     ]
    },
    "start": [
     0,
     3
    ],
    "frames": [
     {
      "x": 0
     },
     {
      "x": 1
     },
     {
      "x": 2
     },
     {
      "x": 3
     },
     {
      "x": -1
     },
     {
      "x": -2
     },
     {
      "x": -3
     }
    ],
    "labels": [
     {
      "text": "tangent to each segment",
      "placement": "inside",
      "at": "top left corner"
     },
     {
      "text": "y = 2",
      "placement": "inside",
      "at": "right end of the flat row"
     }
    ]
   },
   "fallback": "the seven frames as small static panels in one row",
   "keyboard": "Right arrow steps to the next frame, Left arrow back; Space pauses auto-advance",
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
   "block": "err-BC-ERR-05013",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05021",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05025",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07013",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-05013",
  "err-BC-ERR-05021",
  "err-BC-ERR-05025",
  "err-BC-ERR-07013",
  "ex-1"
 ],
 "read_minutes": {
  "full": 5.3,
  "brief": 3.0
 },
 "word_count": {
  "full": 789,
  "brief": 449
 },
 "research_lines": [
  {
   "file": "research/units/unit-07-differential-equations.md",
   "line": "A solution curve through a point follows the segments of the field, so it is tangent to the segment at every point it passes"
  }
 ],
 "inferred": [
  {
   "claim": "ex-1 uses BC-QA-07010 rather than the primary BC-QA-07001, because the first two error blocks served in the mid band are classification errors.",
   "settles": "An error ordering that places sketch errors first for BC-CON-07005, or a reviewer decision on example choice."
  },
  {
   "claim": "BC-PT-99005 is not tagged on the critical input in ex-1, to keep the brief band at or under 450 words.",
   "settles": "A band cap that excludes reader lines."
  },
  {
   "claim": "The orientation is an interactive draggable point and ki-1 a motion trace.",
   "settles": "The modality A/B in the build plan."
  },
  {
   "claim": "BC-ERR-07013 is shown on ex-2's draw, not ex-1's.",
   "settles": "A field-reading error block whose draw matches ex-1."
  },
  {
   "claim": "BC-ERR-05013 is shown on dy/dx = (y - 1)(x - 2)^2, y > 1, which BC-QA-07010's parameter_spec cannot produce (its roots are simple, so the sign always changes); the squared factor follows the record's non_conceptual_causes entry on a factor of even multiplicity.",
   "settles": "A BC-QA-07010 parameter that allows a repeated root, or a reviewer decision on off-spec error draws."
  },
  {
   "claim": "ki-1's never crosses the flat row holds where solutions through a point are unique; the library states it as the sketch standard's correct side condition (sg-23:9), not as a theorem.",
   "settles": "A research or CED line stating the uniqueness condition."
  }
 ],
 "sources": [
  "BC-CON-07005",
  "BC-SKL-07014",
  "BC-SKL-07015",
  "BC-SKL-07016",
  "BC-SKL-07017",
  "BC-SKL-07018",
  "BC-EK-FUN-7C3",
  "ced:140",
  "BC-QA-07001",
  "BC-QA-07002",
  "BC-QA-07005",
  "BC-QA-07010",
  "BC-FRQ-2023-Q3-A",
  "BC-FRQ-2024-Q3-A",
  "BC-PT-99010",
  "BC-PT-99065",
  "sg-23:9",
  "sg-24:9",
  "sg-26:11",
  "BC-ERR-05013",
  "BC-ERR-05021",
  "BC-ERR-05025",
  "BC-ERR-07013",
  "BC-MIS-05028",
  "BC-PRQ-07006",
  "research/units/unit-07-differential-equations.md#7.4 Reasoning Using Slope Fields",
  "research/question-analysis/question-archetypes.md#BC-QA-07001 Solution curve sketched on a supplied slope field",
  "research/question-analysis/question-archetypes.md#BC-QA-07005 Direction of an approximation decided from the second derivative of a solution",
  "research/question-analysis/question-archetypes.md#BC-QA-07010 Behaviour of a solution obtained from the differential equation itself",
  "research/scoring/justification-requirements.md#Reasons about slope fields and concavity",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
