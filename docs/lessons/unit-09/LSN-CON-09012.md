---
title: LSN-CON-09012 Polar to Cartesian relations
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09012, the Cartesian coordinates of a point on a polar curve as r times cosine and r times sine of the angle, built from authoring_bundle("BC-CON-09012") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09012 Polar to Cartesian relations

Concept BC-CON-09012 (skill BC-SKL-09029), topic 9.7 of Unit 9, BC only (ced:177), loaded by seven archetypes in two families, polar-calculus (BC-QA-09009, 09011, 99002, 99003, 99006) and polar-motion (BC-QA-99004, 99005). The recorded Unit 9 hard parent is BC-CON-09007 through one edge that looks mis-anchored (docs/lessons/unit-09/README.md, Library gaps), so the lesson assumes only sine and cosine as coordinates and the product rule.

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The curve is \(r=4+2\cos 2\theta\), the value of r at 0.8 is given, and the question is the x-coordinate of the point there. Key B, \(r\cos 0.8\). The distractors are r itself, the reading BC-ERR-09027 records, and \(r\sin 0.8\), the other leg. Sine and cosine as the legs of a triangle on a circle (BC-PRQ-09002) settle it before any rule is stated. The resolution names the two legs with no verdict word. Source: BC-CON-09012 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-09012 `description_plain` ("The coordinates of a polar point are r times cosine and r times sine of the angle") and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form): calculator variants evaluate at decimal angles in radian mode. The orientation states what a response shows. No count, no frequency.

## Key ideas

One essential knowledge statement, BC-EK-FUN-3G2 (ced:177): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph Polar to Cartesian: x equals r cosine theta and y equals r sine theta. The added clause that r is a distance and not a coordinate comes from BC-MIS-09013's description. Notation line: the concept's `notation`. No anchor quote.

## Recognition

- BC-QA-99002 (research/question-analysis/question-archetypes.md#BC-QA-99002 Derivative of a Cartesian coordinate with respect to theta on a polar curve): `common_givens` a polar equation and a stated angle; `asked_to_produce` an expression for the Cartesian coordinate in terms of the angle and the value of its derivative; `typical_wording` find the derivative of the horizontal coordinate with respect to the angle at a stated angle. BC-FRQ-2014-Q2-B.
- BC-QA-99004 (research/question-analysis/question-archetypes.md#BC-QA-99004 Time at which a Cartesian coordinate of a particle on a polar path reaches a value): the angle as a function of time and a target coordinate value. BC-FRQ-2013-Q2-B.
- The other five archetypes (BC-QA-09009, 09011, 99003, 99005, 99006) load the skill too and are named here for recognition only.

What says this concept: a Cartesian coordinate, a horizontal or vertical position, or a distance from an axis, asked of a polar curve. What says a different concept: the rate of r itself (BC-CON-09013). The contrast pair takes its near miss from that sibling concept, BC-QA-09009, on one radial function.

## Method choice

- st-1, BC-QA-99002. Method, `expected_solution_path[0]`: write the requested coordinate as the radial function times the cosine or the sine of the angle. Rival, `wrong_approaches`: treating the coordinate as the radial function itself. Separating feature: the stem names a coordinate. Both cue fields exist, so the block is not inferred. The block carries the contrast pair.
- st-2, BC-QA-99004. Method, `expected_solution_path[0]` and `[1]`. Rival, `wrong_approaches`: equating the radial function to the stated coordinate value. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-99002, both bands, calculator. Draw: constant 4, amplitude 2, frequency 2, trig cos, coordinate x, angle 4/5. No published item on BC-QA-99002 carries this draw (content/items_*). \(dx/d\theta\) about -5.613 by SymPy.
- ex-2, low band, calculator. Draw: constant 5, amplitude 3, frequency 2, trig sin, coordinate y, angle 7/10. No published item carries it. \(dy/d\theta\) about 6.742.
- ex-2 is faded from step 3: the coordinate and its product-rule derivative are shown, the student writes the value, and the value then reveals. The fade falls there because the conversion and the product rule repeat ex-1's pattern and the evaluation is the last decision.
- Steps follow `expected_solution_path`: the coordinate (new), its derivative (differentiate), the value (evaluate, three places). A fluent solver writes the coordinate and its derivative and holds the calculator evaluation.

No productive-failure opener targets this concept, so no comparison callout.

## Scoring

BC-QA-99002 lists BC-PT-99049, 99005 and 99004. ex-1 tags BC-PT-99049 on the derivative, one generated line, and its BC-PT-99004 value point is untagged to keep the brief form under its cap (inferred array); ex-2 tags BC-PT-99049 on the derivative and BC-PT-99004 on the value. The lines are `reader_checks` output. The archetype's `scoring_pattern` gives two points, the expression for the coordinate or its derivative and the value (samples-14-q2:1).

Point losses research names for this shape: many responses did not know the rectangular coordinate is the polar radius times the cosine (research/scoring/common-point-losses.md#Setup points, crabbc-25:30); fewer than three decimals (research/scoring/common-point-losses.md#Answer points).

## Traps

One active error meets the skill, BC-ERR-09027, so the lesson holds one block. It is on ex-1's draw, `fix_prompt` true since the pair is distinct. No possible reason line, to keep the brief form under its cap.

## Representations

None. The topic's Representations paragraph names BC-REP-13, 02, 01 and 09 and the conversion from a polar equation to the Cartesian coordinates of a point; the figure it would carry is the ki-1 figure, so a second block would repeat it.

## Prerequisite bridge

- BC-PRQ-09002, from its `description_plain` and `failure_signature`.

## Time

The MCQ form is Section I Part B, calculator, 2.92 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part: 2 points, 3.33 minutes (docs/lessons/unit-09/README.md, section 5). A fluent solver writes the coordinate and its derivative; the evaluation is held on the calculator.

## Checks

- chk-1, completion of ex-1, both bands: the coordinate given, the value asked. Key -5.613.
- chk-2, isomorph, both bands, BC-QA-99002. Draw: constant 6, amplitude 2, frequency 3, trig sin, coordinate y, angle 7/5. Key -2.175.
- No check 3. Check 3 needs three distractors that each carry the error_path of an error block, and BC-ERR-09027 is the one active error the skill holds; the checker allows two checks. Library gap, reported.

## Delivery

- orientation: figure. Rule 4: BC-REP-13 on BC-SKL-09029. The polar curve with the ray and the point at 0.8.
- ki-1: figure. Rule 4: BC-REP-13; the right triangle with hypotenuse r and legs \(r\cos\theta\) and \(r\sin\theta\) (docs/lessons/unit-09/README.md, section 6). Not promoted: the conversion is a single evaluation.
- ex-1, ex-2, the error block: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, st-2, ex-1, chk-1, err-BC-ERR-09027, ex-2 (faded from step 3) and its lines, chk-2. 720 words, 4.8 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-09027, chk-2. 444 words, 3.0 minutes.
- Refresher: ki-1, err-BC-ERR-09027, ex-1.

## Sources

- BC-CON-09012; BC-SKL-09029; BC-EK-FUN-3G2; ced:177
- BC-QA-99002, BC-QA-99004; BC-PT-99049, BC-PT-99004
- BC-ERR-09027; BC-MIS-09013
- BC-PRQ-09002
- research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form
- research/question-analysis/question-archetypes.md#BC-QA-99002 Derivative of a Cartesian coordinate with respect to theta on a polar curve
- research/exam/exam-structure.md#Section and part layout
- [inferred] the held steps; the untagged value point on ex-1; every non-text delivery mode. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09012",
 "kind": "concept",
 "target_id": "BC-CON-09012",
 "unit": "09",
 "skills": [
  "BC-SKL-09029"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "A polar curve is \\(r=4+2\\cos 2\\theta\\), and at \\(\\theta=0.8\\) the value is \\(r\\approx3.942\\). Predict the x-coordinate of the point on the curve at \\(\\theta=0.8\\).",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(3.942\\), the value of \\(r\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(2.746\\), from \\(r\\cos 0.8\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(2.828\\), from \\(r\\sin 0.8\\)",
    "is_key": false
   }
  ],
  "resolution": "The point lies at distance \\(r\\) from the origin on the ray at angle 0.8, so its horizontal leg is \\(r\\cos 0.8\\approx2.746\\) and its vertical leg is \\(r\\sin 0.8\\). The value of \\(r\\) is neither coordinate.",
  "sources": [
   "BC-CON-09012",
   "research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form"
  ]
 },
 "orientation": {
  "text": "A response converts a point on a polar curve by writing \\(x=r\\cos\\theta\\) and \\(y=r\\sin\\theta\\) before any derivative or equation uses the coordinate, and evaluates in radian mode.",
  "sources": [
   "BC-CON-09012",
   "research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3G2",
   "depth": "core",
   "text": "For a curve given by a polar equation, \\(x=r\\cos\\theta\\) and \\(y=r\\sin\\theta\\). The value of \\(r\\) is the distance from the origin, not a coordinate, so a coordinate is written as \\(r\\) times the cosine or sine of the angle before it is differentiated or set equal to a value.",
   "notation": "x = r cos theta; y = r sin theta",
   "quote": null,
   "sources": [
    "BC-EK-FUN-3G2",
    "ced:177",
    "research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-99002",
   "cue": "A polar equation, a stated angle, and the rate of a Cartesian coordinate.",
   "method": "\\(x=r(\\theta)\\cos\\theta\\) written first, then differentiated by the product rule.",
   "rival": "Treating the coordinate as the radial function itself.",
   "separating_feature": "The stem names x or y, not r.",
   "sources": [
    "BC-QA-99002"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "A curve is \\(r=3+\\sin 2\\theta\\), with \\(x=r\\cos\\theta\\). Find \\(\\frac{dx}{d\\theta}\\) at \\(\\theta=0.6\\).",
     "archetype_id": "BC-QA-99002"
    },
    "not_this": {
     "text": "A curve is \\(r=3+\\sin 2\\theta\\). Find \\(\\frac{dr}{d\\theta}\\) at \\(\\theta=0.6\\).",
     "why_not": "It asks for the rate of \\(r\\) itself, so no conversion is made."
    },
    "feature": "\\(dx/d\\theta\\) differentiates \\(r\\cos\\theta\\); \\(dr/d\\theta\\) differentiates \\(r\\)."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-99004",
   "cue": "A polar curve, the angle as a function of time, and a target for a coordinate.",
   "method": "The coordinate as \\(r\\cos\\theta\\) or \\(r\\sin\\theta\\), the angle replaced by its expression in \\(t\\), then the equation set equal to the target.",
   "rival": "Setting \\(r\\) equal to the target value.",
   "separating_feature": "The target belongs to the Cartesian coordinate, not to \\(r\\).",
   "sources": [
    "BC-QA-99004"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-99002",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "constant": 4,
    "amplitude": 2,
    "frequency": 2,
    "trig": "cos",
    "coordinate": "x",
    "angle": "4/5"
   },
   "problem": {
    "text": "A curve is \\(r=4+2\\cos 2\\theta\\). Using a calculator, find \\(\\frac{dx}{d\\theta}\\) at \\(\\theta=0.8\\), where \\(x=r\\cos\\theta\\). Show the setup.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "The stem names x, not r.",
     "why": "The coordinate is r times the cosine.",
     "expr": "(4 + 2*cos(2*theta))*cos(theta)",
     "relation": "new"
    },
    {
     "cue": "The coordinate is a product.",
     "why": "Product rule, with the chain rule inside r.",
     "expr": "-(2*cos(2*theta) + 4)*sin(theta) - 4*sin(2*theta)*cos(theta)",
     "relation": "differentiate",
     "variable": "theta",
     "point_type_id": "BC-PT-99049"
    },
    {
     "cue": "Radian mode at the stated angle.",
     "why": "Three places after the decimal point.",
     "expr": "-5.613",
     "relation": "evaluate",
     "subs": {
      "theta": "4/5"
     },
     "approx": true
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "-5.613"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-99002",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "constant": 5,
    "amplitude": 3,
    "frequency": 2,
    "trig": "sin",
    "coordinate": "y",
    "angle": "7/10"
   },
   "problem": {
    "text": "A curve is \\(r=5+3\\sin 2\\theta\\). Using a calculator, find \\(\\frac{dy}{d\\theta}\\) at \\(\\theta=0.7\\), where \\(y=r\\sin\\theta\\). Show the setup.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "The stem names y, not r.",
     "why": "The coordinate is r times the sine.",
     "expr": "(5 + 3*sin(2*theta))*sin(theta)",
     "relation": "new"
    },
    {
     "cue": "The coordinate is a product.",
     "why": "Product rule, with the chain rule inside r.",
     "expr": "(3*sin(2*theta) + 5)*cos(theta) + 6*sin(theta)*cos(2*theta)",
     "relation": "differentiate",
     "variable": "theta",
     "point_type_id": "BC-PT-99049"
    },
    {
     "cue": "Radian mode at the stated angle.",
     "why": "Three places after the decimal point.",
     "expr": "6.742",
     "relation": "evaluate",
     "subs": {
      "theta": "7/10"
     },
     "approx": true,
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "6.742"
   },
   "fade_from": 3
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99049"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99049",
     "text": "Derivative of one variable with respect to another by the chain rule in polar or parametric form. Earned by: A correct chain or quotient relation among the derivatives, presented symbolically or numerically (sg-26:7, sg-23:7). Not earned by: An equation of the form expression equals constant that equates a general expression to a single value (sg-22:6, sg-23:6). Notation: sg-25:7 accepts several loose notations for an evaluated derivative, including one written without the evaluation bar, and still awards the point."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99049",
    "BC-PT-99004"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99049",
     "text": "Derivative of one variable with respect to another by the chain rule in polar or parametric form. Earned by: A correct chain or quotient relation among the derivatives, presented symbolically or numerically (sg-26:7, sg-23:7). Not earned by: An equation of the form expression equals constant that equates a general expression to a single value (sg-22:6, sg-23:6). Notation: sg-25:7 accepts several loose notations for an evaluated derivative, including one written without the evaluation bar, and still awards the point."
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
   "error_id": "BC-ERR-09027",
   "observed_behavior": "The value of r is treated as the x coordinate or the y coordinate of the point.",
   "scoring_consequence": "The coordinate is wrong, so any extremum or conversion built on it fails.",
   "wrong_step": {
    "text": "\\(x=r\\), so \\(\\frac{dx}{d\\theta}=\\frac{dr}{d\\theta}\\approx-3.998\\)",
    "expr": "-3.998"
   },
   "right_step": {
    "text": "\\(x=r\\cos\\theta\\), so \\(\\frac{dx}{d\\theta}\\approx-5.613\\)",
    "expr": "-5.613"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-09027"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-09002",
   "text": "Cosine and sine are the coordinates of a point on a circle."
  }
 ],
 "time": {
  "exam_part": "I-B",
  "budget_minutes": 2.92,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2
   ]
  },
  "skipped_steps": {
   "ex-1": [
    3
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
   "archetype_id": "BC-QA-99002",
   "parameter_draw": {
    "constant": 4,
    "amplitude": 2,
    "frequency": 2,
    "trig": "cos",
    "coordinate": "x",
    "angle": "4/5"
   },
   "completes": "ex-1",
   "stem": {
    "text": "With \\(x=(4+2\\cos 2\\theta)\\cos\\theta\\) and its derivative written, use a calculator to find \\(\\frac{dx}{d\\theta}\\) at \\(\\theta=0.8\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-5.613"
   },
   "steps": [
    {
     "text": "The derivative.",
     "expr": "-(2*cos(2*theta) + 4)*sin(theta) - 4*sin(2*theta)*cos(theta)",
     "relation": "new"
    },
    {
     "text": "Radian mode.",
     "expr": "-5.613",
     "relation": "evaluate",
     "subs": {
      "theta": "4/5"
     },
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09029"
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
   "archetype_id": "BC-QA-99002",
   "parameter_draw": {
    "constant": 6,
    "amplitude": 2,
    "frequency": 3,
    "trig": "sin",
    "coordinate": "y",
    "angle": "7/5"
   },
   "stem": {
    "text": "A curve is \\(r=6+2\\sin 3\\theta\\). Using a calculator, find \\(\\frac{dy}{d\\theta}\\) at \\(\\theta=1.4\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-2.175"
   },
   "steps": [
    {
     "text": "The coordinate.",
     "expr": "(6 + 2*sin(3*theta))*sin(theta)",
     "relation": "new"
    },
    {
     "text": "Product rule.",
     "expr": "(2*sin(3*theta) + 6)*cos(theta) + 6*sin(theta)*cos(3*theta)",
     "relation": "differentiate",
     "variable": "theta"
    },
    {
     "text": "Radian mode.",
     "expr": "-2.175",
     "relation": "evaluate",
     "subs": {
      "theta": "7/5"
     },
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09029"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-13 on BC-SKL-09029; not promoted, the conversion is a single evaluation and the stem asks for a value, not a reading",
   "sources": [
    "BC-SKL-09029"
   ],
   "spec": {
    "kind": "diagram",
    "representations": [
     "BC-REP-13"
    ],
    "curve": {
     "polar": "4 + 2*cos(2*theta)",
     "theta_range": [
      0,
      3.1416
     ]
    },
    "point": {
     "theta": 0.8
    },
    "labels": [
     {
      "text": "r",
      "placement": "inside"
     },
     {
      "text": "theta = 0.8",
      "placement": "inside"
     },
     {
      "text": "the point on the curve",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same polar curve static with the ray and the point at theta = 0.8 labelled",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-13 on BC-SKL-09029; the right triangle whose hypotenuse is r and whose legs are the two coordinates is the idea",
   "sources": [
    "BC-SKL-09029"
   ],
   "spec": {
    "kind": "geometric_diagram",
    "representations": [
     "BC-REP-13"
    ],
    "drawn": [
     "a point at angle theta and distance r from the origin",
     "the horizontal leg to the point",
     "the vertical leg to the point"
    ],
    "labels": [
     {
      "text": "r",
      "placement": "inside"
     },
     {
      "text": "theta",
      "placement": "inside"
     },
     {
      "text": "x = r cos theta",
      "placement": "inside"
     },
     {
      "text": "y = r sin theta",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same triangle static with its three labels",
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
   "block": "err-BC-ERR-09027",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-09027",
  "ex-1"
 ],
 "read_minutes": {
  "full": 4.8,
  "brief": 3.0
 },
 "word_count": {
  "full": 720,
  "brief": 444
 },
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "For a curve given by a polar equation, x equals r times the cosine of theta and y equals r times the sine of theta"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the coordinate and its derivative and holds the calculator evaluation.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "ex-1 tags only BC-PT-99049, and its BC-PT-99004 value point is untagged, because a second reader line does not fit the brief cap; ex-2 tags both.",
   "settles": "A brief cap that admits a second reader line."
  },
  {
   "claim": "Every non-text delivery mode chosen here is a proposal.",
   "settles": "The modality A/B on skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-09012",
  "BC-SKL-09029",
  "BC-EK-FUN-3G2",
  "ced:177",
  "BC-QA-99002",
  "BC-QA-99004",
  "BC-PT-99049",
  "BC-PT-99004",
  "BC-ERR-09027",
  "BC-MIS-09013",
  "BC-PRQ-09002",
  "samples-14-q2:1",
  "research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form",
  "research/question-analysis/question-archetypes.md#BC-QA-99002 Derivative of a Cartesian coordinate with respect to theta on a polar curve",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
