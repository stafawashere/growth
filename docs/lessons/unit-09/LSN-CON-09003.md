---
title: LSN-CON-09003 Second derivative of a parametric curve
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09003, the second derivative d2y/dx2 of a parametric curve built as the derivative of the slope in t divided by dx/dt and read for concavity, built from authoring_bundle("BC-CON-09003") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09003 Second derivative of a parametric curve

Concept BC-CON-09003 (skills BC-SKL-09007 to BC-SKL-09010), topic 9.2 of Unit 9, BC only (ced:172), loaded by one archetype, BC-QA-09002 (family parametric-calculus). Its Unit 9 hard parents are BC-CON-09001 and BC-CON-09002 (docs/lessons/unit-09/README.md, section 1), so both component derivatives and the slope quotient are assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers at \(t=2\), the rate of the slope in t (-2) and the rate of x in t (2), with the core claim that the second derivative divides the first by dx/dt. Key A, -1. The distractors are -2 (no division) and -4 (a product). The slope changing by -2 per unit of t while x moves 2 per unit of t answers it by rate reasoning before any rule is taught, and the x-rate is not 1, so the division shows. The resolution states the per-unit-x reading with no verdict. Source: BC-CON-09003 and the topic section the key idea cites.

## Orientation

From BC-CON-09003 `description_plain` ("Differentiate the slope with respect to the parameter, then divide by dx/dt again") and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.2 Second Derivatives of Parametric Equations): a response builds the expression in order and reads its value or sign. No count, no frequency.

## Key ideas

All four skills map to BC-EK-CHA-3G3 (ced:172): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs Second derivative, Order of operations and Concavity. Notation line from the concept's `notation`. No anchor quote: the cached page prints the formula as broken equation text, so no exact match is possible.

## Recognition

BC-QA-09002 (research/question-analysis/question-archetypes.md#BC-QA-09002 Second derivative of a parametric curve) is the only archetype loading the four skills. `common_givens` "a parametric pair" and "a parameter value"; `asked_to_produce` "a second derivative expression" and "a value or a statement of concavity"; `typical_wording` "find the second derivative of y with respect to x at the given parameter value, or state the concavity of the curve there". Shapes: an MCQ that offers the quotient of the two second parametric derivatives as a distractor (BC-MCQ-CED-018); no free response part appears in the corpus.

The near miss of the contrast pair is the acceleration vector on the same position pair (BC-QA-09004, BC-CON-09006), which also takes second derivatives but in time, of each component separately. What says "not this concept": an acceleration or a second derivative asked with respect to t.

## Method choice

- st-1, BC-QA-09002. Cue from `common_givens` and `asked_to_produce`. Method `expected_solution_path[0..2]`. Rival: `wrong_approaches` "dividing the second derivative of y by the second derivative of x" and `common_distractors` "the derivative of the slope with respect to the parameter without the second division". Separating feature: the order of operations. It carries the contrast pair, a d2y/dx2 stem beside an acceleration stem on the same pair. Both cue fields exist, so the block is not inferred.

## Solution path

- ex-1, BC-QA-09002, both bands, no calculator. Draw: x_square 1, x_linear -2, x_constant 0, y_cube 1, y_square 2, y_constant 0, time 2, direction forward. \(x=t^2-2t\), \(y=t^3+2t^2\); \(dy/dx=\frac{3t^2+4t}{2t-2}\), its t-derivative is -2 at t = 2, \(dx/dt=2\), so \(d^2y/dx^2=-1\), concave down. No published item on BC-QA-09002 carries this draw (content/items_gen_unit09, ITM-GEN-09002-00 to 21).
- ex-2, low band, no calculator, faded from step 3. Draw: x_square 2, x_linear -2, x_constant 0, y_cube 1, y_square 3, y_constant 0, time 1, direction forward. \(x=2t^2-2t\), \(y=t^3+3t^2\); key -3/2. Steps 1 and 2 (the slope and its derivative in t) are shown and the student writes the second derivative; steps 3 and 4 then reveal, because the second division is the step that gets dropped.
- A fluent solver writes the slope, its derivative in t and the quotient; the evaluation is held. No productive-failure comparison: BC-CON-09003 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

None. BC-QA-09002 lists no point types, so this lesson carries no scoring lines and says nothing about points (docs/lessons/unit-09/README.md, Library gaps met). The archetype's `scoring_pattern` is inferred from the slope scoring of 2023 and no free response part of this shape is in the corpus.

## Traps

Bundle order is BC-ERR-09009, 09010, 09012, 99019, 99021. The first three are the blocks, on ex-1's draw, all `fix_prompt` true. BC-ERR-99019 and 99021 are left out: the archetype's draws are no calculator with exact answers, so neither has a wrong and right pair on them. Mid band shows the first two.

- err-BC-ERR-09009: \(y''/x''=8\) against -1. Possible reason, BC-MIS-09004.
- err-BC-ERR-09010: stopping at the derivative of the slope, -2, against -1. No possible reason line.
- err-BC-ERR-09012: the sign of d2y/dt2 (16) read as concavity, against d2y/dx2 (-1).

## Representations

None. The concavity arcs are carried by the ki-1 delivery entry (the topic's Representations paragraph gives a sign converted to a statement of concavity, BC-REP-01 to BC-REP-04).

## Prerequisite bridge

- BC-PRQ-06005 and BC-PRQ-08006, each from its `description_plain` and `failure_signature`.

## Time

The archetype's draws are no calculator: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred for an either archetype]. No free response part of this shape is recorded, so no point budget is given. A fluent solver writes the slope, its derivative in t and the quotient; the evaluation is held. The minutes go on differentiating the quotient.

## Checks

- chk-1, completion of ex-1, both bands: the derivative of the slope and dx/dt given, \(d^2y/dx^2\) asked. Key -1.
- chk-2, isomorph, both bands. Draw: x_square -1, x_linear 1, x_constant 0, y_cube 1, y_square 1, y_constant 0, time 1, direction backward. \(x=-t^2+t\), \(y=t^3+t^2\). Key -2.
- chk-3, MCQ, low band. Draw: x_square 2, x_linear -2, x_constant 0, y_cube 2, y_square 1, y_constant 0, time 1, direction forward. \(x=2t^2-2t\), \(y=2t^3+t^2\). Key -1/2. Distractors: -1, no second division (BC-ERR-09010); 7/2, y'' over x'' (BC-ERR-09009); 14, d2y/dt2 (BC-ERR-09012). No published draw matches any of these.

## Delivery

- orientation, ki-1: figure. Rule 4 (README rule 3): BC-REP-12 on BC-SKL-09007 to 09010. The orientation shows the path at t = 2; ki-1 marks the concave down arc (t below about 2.53) and the concave up arc, so the sign of d2y/dx2 is read off the picture. Not promoted: BC-QA-09002 `difficulty_variables` vary the form asked.
- ex-1, ex-2, the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, the three error blocks, ex-2 (faded from step 3), chk-2, chk-3. 528 words, 3.7 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-09009, err-BC-ERR-09010, chk-2. 407 words, 2.9 minutes.
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-09003; BC-SKL-09007 to BC-SKL-09010; BC-EK-CHA-3G3; ced:172
- BC-QA-09002, BC-QA-09004
- BC-ERR-09009, BC-ERR-09010, BC-ERR-09012; BC-MIS-09004
- BC-PRQ-06005, BC-PRQ-08006
- research/units/unit-09-parametric-polar-vector.md#9.2 Second Derivatives of Parametric Equations
- research/question-analysis/question-archetypes.md#BC-QA-09002 Second derivative of a parametric curve
- research/exam/exam-structure.md#Section and part layout
- [inferred] Part A timing; the held steps; no scoring lines; every non-text delivery mode. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09003",
 "kind": "concept",
 "target_id": "BC-CON-09003",
 "unit": "09",
 "skills": [
  "BC-SKL-09007",
  "BC-SKL-09008",
  "BC-SKL-09009",
  "BC-SKL-09010"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "At \\(t=2\\) on the curve of the example, the slope \\(dy/dx\\) changes at rate \\(-2\\) per unit of \\(t\\), and \\(x\\) changes at rate \\(2\\) per unit of \\(t\\). Predict \\(d^2y/dx^2\\) there.",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(-1\\)",
    "is_key": true
   },
   {
    "id": "B",
    "label": "\\(-2\\)",
    "is_key": false
   },
   {
    "id": "C",
    "label": "\\(-4\\)",
    "is_key": false
   }
  ],
  "resolution": "\\(d^2y/dx^2\\) is the rate of the slope per unit of \\(x\\): \\(-2\\) per unit \\(t\\) over \\(2\\) per unit \\(t\\) gives \\(-1\\).",
  "sources": [
   "BC-CON-09003",
   "research/units/unit-09-parametric-polar-vector.md#9.2 Second Derivatives of Parametric Equations"
  ]
 },
 "orientation": {
  "text": "The second derivative \\(d^2y/dx^2\\) of a parametric curve is the derivative of the slope in \\(t\\), divided by \\(dx/dt\\). A response builds it in that order, then reads its value or sign as concavity.",
  "sources": [
   "BC-CON-09003",
   "research/units/unit-09-parametric-polar-vector.md#9.2 Second Derivatives of Parametric Equations"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3G3",
   "depth": "core",
   "text": "\\(\\dfrac{d^2y}{dx^2}\\) is \\(\\dfrac{d}{dt}\\left(\\dfrac{dy}{dx}\\right)\\) divided by \\(\\dfrac{dx}{dt}\\). Form the slope, differentiate it in \\(t\\), then divide by \\(dx/dt\\). The quotient of the two second derivatives in \\(t\\) is a different expression. Concavity follows the sign of \\(d^2y/dx^2\\), never that of \\(d^2y/dt^2\\).",
   "notation": "second derivative of y with respect to x",
   "quote": null,
   "sources": [
    "BC-EK-CHA-3G3",
    "ced:172",
    "research/units/unit-09-parametric-polar-vector.md#9.2 Second Derivatives of Parametric Equations"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09002",
   "cue": "A parametric pair, a parameter value, and \\(d^2y/dx^2\\) or concavity.",
   "method": "Form \\(dy/dx\\), differentiate it in \\(t\\), then divide by \\(dx/dt\\).",
   "rival": "\\(\\dfrac{d^2y/dt^2}{d^2x/dt^2}\\), the quotient of second derivatives.",
   "separating_feature": "The slope is differentiated first, then divided by \\(dx/dt\\) again.",
   "sources": [
    "BC-QA-09002"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Position \\(x=t^2-t\\), \\(y=t^3+t\\). Find \\(d^2y/dx^2\\) at \\(t=2\\).",
     "archetype_id": "BC-QA-09002"
    },
    "not_this": {
     "text": "Position \\(x=t^2-t\\), \\(y=t^3+t\\). Find the acceleration vector at \\(t=2\\).",
     "why_not": "It asks for the second derivatives of x and y in time, taken separately."
    },
    "feature": "The slope's change per unit x, not accelerations in time."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-09002",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "x_square": "1",
    "x_linear": "-2",
    "x_constant": "0",
    "y_cube": "1",
    "y_square": "2",
    "y_constant": "0",
    "time": "2",
    "direction": "forward"
   },
   "problem": {
    "text": "A curve is defined by \\(x=t^2-2t\\) and \\(y=t^3+2t^2\\). Find \\(d^2y/dx^2\\) at \\(t=2\\), and state whether the curve is concave up or concave down there.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Form the slope.",
     "why": "\\(dy/dx\\) is \\(dy/dt\\) over \\(dx/dt\\).",
     "expr": "(3*t**2 + 4*t)/(2*t - 2)",
     "relation": "new"
    },
    {
     "cue": "Differentiate the slope in \\(t\\).",
     "why": "The slope is a function of \\(t\\).",
     "expr": "(-t*(3*t + 4) + 2*(t - 1)*(3*t + 2))/(2*(t - 1)**2)",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "Divide by \\(dx/dt\\) again.",
     "why": "That gives the rate of the slope per unit \\(x\\).",
     "expr": "(-t*(3*t + 4) + 2*(t - 1)*(3*t + 2))/(4*(t - 1)**3)",
     "relation": "new"
    },
    {
     "cue": "Evaluate at the stated \\(t\\).",
     "why": "The sign gives the concavity.",
     "expr": "-1",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     }
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "-1"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-09002",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "x_square": "2",
    "x_linear": "-2",
    "x_constant": "0",
    "y_cube": "1",
    "y_square": "3",
    "y_constant": "0",
    "time": "1",
    "direction": "forward"
   },
   "problem": {
    "text": "A curve is defined by \\(x=2t^2-2t\\) and \\(y=t^3+3t^2\\). Find \\(d^2y/dx^2\\) at \\(t=1\\), and state whether the curve is concave up or concave down there.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Form the slope.",
     "why": "\\(dy/dx\\) is \\(dy/dt\\) over \\(dx/dt\\).",
     "expr": "(3*t**2 + 6*t)/(4*t - 2)",
     "relation": "new"
    },
    {
     "cue": "Differentiate the slope in \\(t\\).",
     "why": "The slope is a function of \\(t\\).",
     "expr": "3*(-t*(t + 2) + (t + 1)*(2*t - 1))/(2*t - 1)**2",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "Divide by \\(dx/dt\\) again.",
     "why": "That gives the rate of the slope per unit \\(x\\).",
     "expr": "3*(-t*(t + 2) + (t + 1)*(2*t - 1))/(2*(2*t - 1)**3)",
     "relation": "new"
    },
    {
     "cue": "Evaluate at the stated \\(t\\).",
     "why": "The sign gives the concavity.",
     "expr": "-3/2",
     "relation": "evaluate",
     "subs": {
      "t": "1"
     }
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "-3/2"
   },
   "fade_from": 3
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-09009",
   "observed_behavior": "The second derivative of y with respect to x is written as the second derivative of y with respect to t divided by the second derivative of x with respect to t.",
   "scoring_consequence": "The setup point is lost.",
   "wrong_step": {
    "text": "\\(y''/x''=16/2=8\\).",
    "expr": "8"
   },
   "right_step": {
    "text": "\\(-2/2=-1\\).",
    "expr": "-1"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-09004",
    "text": "replacing each first derivative with a second derivative"
   },
   "sources": [
    "BC-ERR-09009",
    "BC-MIS-09004"
   ]
  },
  {
   "error_id": "BC-ERR-09010",
   "observed_behavior": "The derivative of dy/dx with respect to the parameter is reported as the second derivative of y with respect to x.",
   "scoring_consequence": "The setup point is lost.",
   "wrong_step": {
    "text": "Stopped at \\(-2\\).",
    "expr": "-2"
   },
   "right_step": {
    "text": "Divided by \\(dx/dt=2\\).",
    "expr": "-1"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09010"
   ]
  },
  {
   "error_id": "BC-ERR-09012",
   "observed_behavior": "The response decides whether the curve is concave up from the sign of the second derivative of y with respect to the parameter.",
   "scoring_consequence": "The conclusion is unsupported and the justification point is lost.",
   "wrong_step": {
    "text": "\\(d^2y/dt^2=16>0\\), so concave up.",
    "expr": "16"
   },
   "right_step": {
    "text": "\\(d^2y/dx^2=-1<0\\), so concave down.",
    "expr": "-1"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09012"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(f'\\) and \\(f\\) are different functions, and each is read at the stated input."
  },
  {
   "prq_id": "BC-PRQ-08006",
   "text": "Three places after the point when a decimal is asked, rounded once."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
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
   "archetype_id": "BC-QA-09002",
   "parameter_draw": {
    "x_square": "1",
    "x_linear": "-2",
    "x_constant": "0",
    "y_cube": "1",
    "y_square": "2",
    "y_constant": "0",
    "time": "2",
    "direction": "forward"
   },
   "completes": "ex-1",
   "stem": {
    "text": "At \\(t=2\\), \\(\\frac{d}{dt}(dy/dx)=-2\\) and \\(dx/dt=2\\). Write \\(d^2y/dx^2\\).",
    "command_verb": "write"
   },
   "key": {
    "form": "numeric",
    "expr": "-1"
   },
   "steps": [
    {
     "text": "Divide by \\(dx/dt\\).",
     "expr": "(-2)/2",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-09008"
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
   "archetype_id": "BC-QA-09002",
   "parameter_draw": {
    "x_square": "-1",
    "x_linear": "1",
    "x_constant": "0",
    "y_cube": "1",
    "y_square": "1",
    "y_constant": "0",
    "time": "1",
    "direction": "backward"
   },
   "stem": {
    "text": "A curve is defined by \\(x=-t^2+t\\) and \\(y=t^3+t^2\\). Find \\(d^2y/dx^2\\) at \\(t=1\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-2"
   },
   "steps": [
    {
     "cue": "Form the slope.",
     "why": "\\(dy/dx\\) is \\(dy/dt\\) over \\(dx/dt\\).",
     "expr": "(3*t**2 + 2*t)/(1 - 2*t)",
     "relation": "new"
    },
    {
     "cue": "Differentiate the slope in \\(t\\).",
     "why": "The slope is a function of \\(t\\).",
     "expr": "2*(t*(3*t + 2) + (1 - 2*t)*(3*t + 1))/(1 - 2*t)**2",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "Divide by \\(dx/dt\\) again.",
     "why": "That gives the rate of the slope per unit \\(x\\).",
     "expr": "2*(t*(3*t + 2) + (1 - 2*t)*(3*t + 1))/(1 - 2*t)**3",
     "relation": "new"
    },
    {
     "cue": "Evaluate at the stated \\(t\\).",
     "why": "The sign gives the concavity.",
     "expr": "-2",
     "relation": "evaluate",
     "subs": {
      "t": "1"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-09009"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-09002",
   "parameter_draw": {
    "x_square": "2",
    "x_linear": "-2",
    "x_constant": "0",
    "y_cube": "2",
    "y_square": "1",
    "y_constant": "0",
    "time": "1",
    "direction": "forward"
   },
   "stem": {
    "text": "A curve is defined by \\(x=2t^2-2t\\) and \\(y=2t^3+t^2\\). Find \\(d^2y/dx^2\\) at \\(t=1\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-1/2"
   },
   "steps": [
    {
     "cue": "Form the slope.",
     "why": "\\(dy/dx\\) is \\(dy/dt\\) over \\(dx/dt\\).",
     "expr": "(6*t**2 + 2*t)/(4*t - 2)",
     "relation": "new"
    },
    {
     "cue": "Differentiate the slope in \\(t\\).",
     "why": "The slope is a function of \\(t\\).",
     "expr": "(-2*t*(3*t + 1) + (2*t - 1)*(6*t + 1))/(2*t - 1)**2",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "Divide by \\(dx/dt\\) again.",
     "why": "That gives the rate of the slope per unit \\(x\\).",
     "expr": "(-2*t*(3*t + 1) + (2*t - 1)*(6*t + 1))/(2*(2*t - 1)**3)",
     "relation": "new"
    },
    {
     "cue": "Evaluate at the stated \\(t\\).",
     "why": "The sign gives the concavity.",
     "expr": "-1/2",
     "relation": "evaluate",
     "subs": {
      "t": "1"
     }
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "-1",
     "error_path": "BC-ERR-09010",
     "derivation": "the derivative of dy/dx in t, with no division by dx/dt = 2"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "7/2",
     "error_path": "BC-ERR-09009",
     "derivation": "y'' over x'': 14 divided by 4"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "-1/2",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "14",
     "error_path": "BC-ERR-09012",
     "derivation": "d2y/dt2 at t = 1, read as the second derivative"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-09009"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4 (README rule 3): BC-REP-12 on BC-SKL-09007 to 09010; not promoted, BC-QA-09002 difficulty_variables vary the form asked, not a quantity read off a figure",
   "sources": [
    "BC-SKL-09007"
   ],
   "spec": {
    "kind": "parametric_path",
    "representations": [
     "BC-REP-12"
    ],
    "x": "t**2 - 2*t",
    "y": "t**3 + 2*t**2",
    "t_range": [
     1.25,
     3
    ],
    "marks": [
     {
      "t": 2
     }
    ],
    "drawn": [
     "the path for t from 1.25 to 3",
     "the point at t = 2"
    ],
    "labels": [
     {
      "text": "t = 2",
      "placement": "inside"
     },
     {
      "text": "(x(t), y(t))",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same path static with the point at t = 2 and its labels",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4 (README rule 3): BC-REP-12 on BC-SKL-09007 to 09010; concave arcs marked by the sign of d2y/dx2, not promoted",
   "sources": [
    "BC-SKL-09010"
   ],
   "spec": {
    "kind": "parametric_path",
    "representations": [
     "BC-REP-12"
    ],
    "x": "t**2 - 2*t",
    "y": "t**3 + 2*t**2",
    "t_range": [
     1.25,
     3
    ],
    "arcs": [
     {
      "t_from": 1.25,
      "t_to": 2.5275,
      "sign": "negative"
     },
     {
      "t_from": 2.5275,
      "t_to": 3,
      "sign": "positive"
     }
    ],
    "labels": [
     {
      "text": "d2y/dx2 < 0, concave down",
      "placement": "inside"
     },
     {
      "text": "d2y/dx2 > 0, concave up",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same path static with the two arcs and their labels",
   "keyboard": "no control; the figure description is reached with Tab"
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
   "block": "err-BC-ERR-09009",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09010",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09012",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-09009",
  "err-BC-ERR-09010",
  "err-BC-ERR-09012",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "The slope must be assembled first, then differentiated with respect to the parameter, then divided by dx/dt."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-09002 is calculator status either; its generator marks every draw no_calculator, so the lesson is timed against Section I Part A at 2.14 minutes.",
   "settles": "Timing data on parametric second derivative items split by exam part."
  },
  {
   "claim": "A fluent solver writes the slope, its derivative in t and the quotient, and holds the evaluation.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "BC-QA-09002 carries no point_types and no free response part appears in the corpus, so the lesson says nothing about points.",
   "settles": "A scoring guideline for a parametric second derivative part."
  },
  {
   "claim": "Every non-text delivery choice.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-09003",
  "BC-SKL-09007",
  "BC-SKL-09008",
  "BC-SKL-09009",
  "BC-SKL-09010",
  "BC-EK-CHA-3G3",
  "ced:172",
  "BC-QA-09002",
  "BC-QA-09004",
  "BC-ERR-09009",
  "BC-ERR-09010",
  "BC-ERR-09012",
  "BC-MIS-09004",
  "BC-PRQ-06005",
  "BC-PRQ-08006",
  "research/units/unit-09-parametric-polar-vector.md#9.2 Second Derivatives of Parametric Equations",
  "research/question-analysis/question-archetypes.md#BC-QA-09002 Second derivative of a parametric curve",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 528,
  "brief": 407
 },
 "read_minutes": {
  "full": 3.7,
  "brief": 2.9
 }
}
```
