---
title: LSN-CON-09013 Rate of change of r with respect to theta
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09013, dr/dtheta as the rate at which the distance from the origin changes with the angle, and its product with dtheta/dt as the rate in time, built from authoring_bundle("BC-CON-09013") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09013 Rate of change of r with respect to theta

Concept BC-CON-09013 (skills BC-SKL-09030, BC-SKL-09031, BC-SKL-09032), topic 9.7 of Unit 9, BC only (ced:177), loaded by BC-QA-09009 and BC-QA-09010 (family polar-calculus) and five further archetypes that load BC-SKL-09030. No Unit 9 hard parent (docs/lessons/unit-09/README.md, section 1); the outside hard parents are BC-SKL-03002 and 03006, so the chain and product rules are assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The curve is \(r=4+3\theta\sin 2\theta\), with r at 0.9 and at 1.0 given. Key B, the rate at which the distance from the origin changes with the angle. The distractors are the speed along the curve and the slope of the tangent line, the two readings BC-ERR-09029 and BC-ERR-09031 record. The two values of r show the change per radian before any rule is stated. The resolution gives the estimate with no verdict word. Source: BC-CON-09013 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-09013 `description_plain` ("The derivative of r says how fast the distance from the origin changes with the angle") and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form): the FRQ opens the calculator part with a rate of change of r and closes it with a rate in time, and requires the differentiation to be visible. The orientation states what a response shows. No count, no frequency.

## Key ideas

Skills map to two essential knowledge statements, BC-EK-FUN-3G2 (BC-SKL-09031, 09032) and BC-EK-FUN-3G1 (BC-SKL-09030), both ced:177.

- ki-1 (core), BC-EK-FUN-3G2. Paraphrase of the Required mathematical knowledge paragraph Meaning of dr/dtheta: r is the distance from the origin, so dr/dtheta is the rate the distance changes with the angle, and with a known dtheta/dt the rate in time is the product (sg-25:10). Notation line: the concept's `notation`.
- ki-2 (extended), BC-EK-FUN-3G1. Paraphrase of Derivatives in polar form and Notation: derivative methods extend, and the differentiation must be indicated (sg-25:7). Low band only, since ex-1 serves the differentiation in both bands. No anchor quotes.

## Recognition

- BC-QA-09009 (research/question-analysis/question-archetypes.md#BC-QA-09009 Derivative of r with respect to theta on a polar curve): `common_givens` a polar equation and an angle; `asked_to_produce` a derivative expression and a numerical value; `typical_wording` find the rate of change of r with respect to theta at the stated angle and show the setup. BC-FRQ-2025-Q2-A and four more.
- BC-QA-09010 (research/question-analysis/question-archetypes.md#BC-QA-09010 Rate at which a particle's distance from the origin changes): `common_givens` a polar equation, a constant rate of change of the angle, an angle; `asked_to_produce` a chain rule product and a numerical rate. BC-FRQ-2025-Q2-D and three more.
- BC-QA-99002 loads BC-SKL-09030 too, and is treated in LSN-CON-09012.

What says this concept: the rate of r, or the distance from the origin, with respect to the angle or to time. What says a different concept: the slope of the tangent line (BC-CON-09014). The contrast pair takes that near miss, `common_distractors` "dy/dx at the same angle", on one radial function.

## Method choice

- st-1, BC-QA-09009. Method, `expected_solution_path[0]` and `[1]`: differentiate r with respect to theta, evaluate at the angle. Rival, `wrong_approaches`: reporting a value with no indication that r was differentiated. Separating feature from the record's `difficulty_variables`: dy/dx requested instead of dr/dtheta. Both cue fields exist, so the block is not inferred. The block carries the contrast pair.
- st-2, BC-QA-09010. Method, `expected_solution_path[0]` and `[1]`. Rival, `wrong_approaches`: omitting the factor giving the rate of the angle. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-09009, both bands, calculator. Draw: constant 4, coefficient 3, frequency 2, trig sin, angle 9/10, framing distance. No published item on BC-QA-09009 carries this draw (content/items_*). \(dr/d\theta\) about 1.695 by SymPy.
- ex-2, BC-QA-09010, low band, calculator. Draw: constant 6, amplitude 3, frequency 2, trig cos, angle 7/10, angle_rate 3/2, rate_form constant. No published item carries it. \(dr/dt\) about -8.869.
- ex-2 is faded from step 3: the radius and its derivative are shown, the student writes the rate in time, and the product and the value then reveal. The fade falls there because the derivative repeats ex-1 and the angular factor is what the student must supply.
- Steps follow `expected_solution_path`: r (new), \(dr/d\theta\) (differentiate), on ex-2 the product (new), the value (evaluate, three places). A fluent solver writes the derivative and the value and holds the recognition of r as the distance.

No productive-failure opener targets this concept, so no comparison callout.

## Scoring

BC-QA-09009 lists BC-PT-99049, 99004 and 99005; BC-QA-09010 lists BC-PT-99005, 99068, 99004 and 99049. ex-1 tags nothing, since the brief cap has no room for a reader line beside the prediction and the contrast pair (inferred array); ex-2 tags BC-PT-99049 on the derivative and BC-PT-99004 on the value. The lines are `reader_checks` output. The `scoring_pattern` of BC-QA-09010 gives two points, the chain rule product and the value (sg-25:10).

Point losses research names for this shape: fewer than three decimals or an intermediate rounded before reuse (research/scoring/common-point-losses.md#Answer points, crabbc-25:30); the chain rule product formed from the wrong derivatives (research/scoring/common-point-losses.md#Setup points, crabbc-25:30).

## Traps

Seven errors meet the skills; the cap is four. The bundle's order is BC-ERR-09028, 09029, 09030, 09039, 99031, 09023, 99019. This design keeps 09028, 09029, 09030 and 09023, and skips BC-ERR-09039, whose only link is BC-SKL-09031 (a polar area error about inner and outer radii, unrelated to dr/dtheta), and BC-ERR-99031, which repeats 09030 and 09028 in one long record. Low band all four, mid band the first two. 09028 is equivalent (the same value, shown with and without the differentiation), so its `fix_prompt` is false; the other three are distinct and carry `fix_prompt` true. 09028, 09029 and 09023 are on ex-1's draw, 09030 on ex-2's.

## Representations

None. The topic's Representations paragraph names BC-REP-13, 02, 01 and 09 and the conversion from a polar equation to a rate of change of distance from the origin; the figure it would carry is the orientation figure and the ki-1 interactive, so a second block would repeat them.

## Prerequisite bridge

- BC-PRQ-06005 and BC-PRQ-09003, each from its `description_plain` and `failure_signature`.

## Time

The MCQ form is Section I Part B, calculator, 2.92 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part: dr/dtheta 1 point, 1.67 minutes; the rate in time 2 points, 3.33 minutes (docs/lessons/unit-09/README.md, section 5). A fluent solver writes the derivative and the value, and the product on the rate in time; the recognition of r as the distance is held.

## Checks

- chk-1, completion of ex-1, both bands: the derivative given, the value asked. Key 1.695.
- chk-2, isomorph, both bands, BC-QA-09009. Draw: constant 3, coefficient 2, frequency 1, trig cos, angle 4/5, framing bare. Key 0.246.
- chk-3, MCQ, low band, BC-QA-09010. Draw: constant 5, amplitude 2, frequency 3, trig sin, angle 9/10, angle_rate 2, rate_form constant. Key -10.849. Distractors: -5.424, the angular rate left out (BC-ERR-09030); 0.209, degree mode (BC-ERR-09023); 15.963, the speed along the curve times the angular rate (BC-ERR-09029).

## Delivery

- orientation: figure. Rule 4: BC-REP-13 on the three skills. The polar curve with the ray at 0.9.
- ki-1: interactive. Rule 4 promoted: BC-QA-09009 `common_givens` name an angle and `difficulty_variables` name whether the reading as a rate of distance from the origin is demanded. One slider, the angle; the reading is growing or shrinking against the sign of dr/dtheta.
- ki-2: text. Rule 6: a differentiation rule and a notation habit; the skill's figure is on ki-1.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, ki-2, st-1 with the contrast pair, st-2, ex-1, chk-1, the four error blocks, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 816 words, 5.5 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-09028, err-BC-ERR-09029, chk-2. 413 words, 2.8 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-09013; BC-SKL-09030, BC-SKL-09031, BC-SKL-09032; BC-EK-FUN-3G1, BC-EK-FUN-3G2; ced:177
- BC-QA-09009, BC-QA-09010; BC-PT-99049, BC-PT-99004
- BC-ERR-09028, BC-ERR-09029, BC-ERR-09030, BC-ERR-09023; BC-MIS-09014
- BC-PRQ-06005, BC-PRQ-09003
- sg-25:7, sg-25:10
- research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form
- research/question-analysis/question-archetypes.md#BC-QA-09009 Derivative of r with respect to theta on a polar curve
- research/exam/exam-structure.md#Section and part layout
- [inferred] the held steps; the untagged points on ex-1; every non-text delivery mode. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09013",
 "kind": "concept",
 "target_id": "BC-CON-09013",
 "unit": "09",
 "skills": [
  "BC-SKL-09030",
  "BC-SKL-09031",
  "BC-SKL-09032"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "A curve is \\(r=4+3\\theta\\sin 2\\theta\\), with \\(r(0.9)\\approx6.629\\) and \\(r(1.0)\\approx6.728\\). Predict what \\(\\frac{dr}{d\\theta}\\) near \\(\\theta=0.9\\) describes.",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "The speed of the point along the curve",
    "is_key": false
   },
   {
    "id": "B",
    "label": "How fast the distance from the origin changes with \\(\\theta\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "The slope of the tangent line",
    "is_key": false
   }
  ],
  "resolution": "Here \\(r\\) grows by about 0.099 over 0.1 radian, an average of 0.985 per radian. \\(dr/d\\theta\\) is that rate at an instant: the change in the distance from the origin per radian.",
  "sources": [
   "BC-CON-09013",
   "research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form"
  ]
 },
 "orientation": {
  "text": "A response differentiates \\(r\\) with respect to \\(\\theta\\) with the differentiation visible, evaluates in radian mode, says the value is the rate of the distance from the origin, and for a rate in time multiplies by \\(d\\theta/dt\\).",
  "sources": [
   "BC-CON-09013",
   "research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3G2",
   "depth": "core",
   "text": "Since \\(r\\) is the distance from the origin, \\(dr/d\\theta\\) is the rate at which that distance changes with the angle: positive means moving away, negative means toward. For a particle with known \\(d\\theta/dt\\), the rate in time is \\(\\frac{dr}{d\\theta}\\cdot\\frac{d\\theta}{dt}\\).",
   "notation": "dr/dtheta",
   "quote": null,
   "sources": [
    "BC-EK-FUN-3G2",
    "ced:177",
    "sg-25:10",
    "research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-3G1",
   "depth": "extended",
   "text": "Methods for calculating derivatives extend to polar coordinates, so \\(r(\\theta)\\) is differentiated with the product, chain and quotient rules. The response indicates the differentiation, not only a value, and evaluates in radian mode.",
   "notation": "dr/dtheta",
   "quote": null,
   "sources": [
    "BC-EK-FUN-3G1",
    "ced:177",
    "sg-25:7",
    "research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09009",
   "cue": "A polar equation, an angle, and the rate of change of \\(r\\).",
   "method": "\\(r'(\\theta)\\) written, then evaluated at the angle.",
   "rival": "Reporting a value with no sign of differentiation.",
   "separating_feature": "The rate asked is of \\(r\\), not of \\(y\\) with respect to \\(x\\).",
   "sources": [
    "BC-QA-09009"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "A curve is \\(r=2+\\theta\\cos\\theta\\). Find the rate of change of \\(r\\) with respect to \\(\\theta\\) at \\(\\theta=0.5\\).",
     "archetype_id": "BC-QA-09009"
    },
    "not_this": {
     "text": "A curve is \\(r=2+\\theta\\cos\\theta\\). Find the slope of the tangent line at \\(\\theta=0.5\\).",
     "why_not": "It asks for \\(dy/dx\\), which needs both coordinates."
    },
    "feature": "Rate of \\(r\\) means \\(dr/d\\theta\\); slope means \\(dy/dx\\)."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-09010",
   "cue": "A polar curve, a constant rate of the angle, and a rate in time.",
   "method": "\\(\\frac{dr}{d\\theta}\\) at the angle, multiplied by \\(\\frac{d\\theta}{dt}\\).",
   "rival": "Reporting \\(dr/d\\theta\\) alone.",
   "separating_feature": "A rate in time carries the angular rate as a factor.",
   "sources": [
    "BC-QA-09010"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-09009",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "constant": 4,
    "coefficient": 3,
    "frequency": 2,
    "trig": "sin",
    "angle": "9/10",
    "framing": "distance"
   },
   "problem": {
    "text": "A particle moves along \\(r=4+3\\theta\\sin 2\\theta\\). Using a calculator, find the rate at which its distance from the origin changes with respect to \\(\\theta\\) at \\(\\theta=0.9\\). Show the setup.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Distance from the origin is \\(r\\).",
     "why": "The rate wanted is \\(dr/d\\theta\\).",
     "expr": "4 + 3*theta*sin(2*theta)",
     "relation": "new"
    },
    {
     "cue": "\\(r\\) has a product.",
     "why": "Product rule, chain rule inside.",
     "expr": "6*theta*cos(2*theta) + 3*sin(2*theta)",
     "relation": "differentiate",
     "variable": "theta"
    },
    {
     "cue": "Radian mode at 0.9.",
     "why": "Three places.",
     "expr": "1.695",
     "relation": "evaluate",
     "subs": {
      "theta": "9/10"
     },
     "approx": true
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "1.695"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-09010",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "constant": 6,
    "amplitude": 3,
    "frequency": 2,
    "trig": "cos",
    "angle": "7/10",
    "angle_rate": "3/2",
    "rate_form": "constant"
   },
   "problem": {
    "text": "A particle moves along \\(r=6+3\\cos 2\\theta\\) with \\(\\frac{d\\theta}{dt}=\\frac32\\). Using a calculator, find the rate at which its distance from the origin changes with respect to time when \\(\\theta=0.7\\). Show the setup.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Distance from the origin is \\(r\\).",
     "why": "\\(dr/d\\theta\\) comes first.",
     "expr": "6 + 3*cos(2*theta)",
     "relation": "new"
    },
    {
     "cue": "\\(r\\) has a cosine of \\(2\\theta\\).",
     "why": "Chain rule inside the cosine.",
     "expr": "-6*sin(2*theta)",
     "relation": "differentiate",
     "variable": "theta",
     "point_type_id": "BC-PT-99049"
    },
    {
     "cue": "The stem gives \\(d\\theta/dt=3/2\\).",
     "why": "A rate in time multiplies by the angular rate.",
     "expr": "(-6*sin(2*theta))*(3/2)",
     "relation": "new"
    },
    {
     "cue": "Radian mode at 0.7.",
     "why": "Three places.",
     "expr": "-8.869",
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
    "expr": "-8.869"
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
   "error_id": "BC-ERR-09028",
   "observed_behavior": "A correct decimal for dr/dtheta appears with nothing showing that r was differentiated.",
   "scoring_consequence": "The point is not earned, because the guideline requires the response to indicate differentiation of r (sg-25:7).",
   "wrong_step": {
    "text": "\\(1.695\\) alone",
    "expr": "1.695"
   },
   "right_step": {
    "text": "\\(\\frac{dr}{d\\theta}=3\\sin2\\theta+6\\theta\\cos2\\theta\\approx1.695\\)",
    "expr": "1.695"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-09028"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-09029",
   "observed_behavior": "The interpretation of dr/dtheta names the speed along the curve rather than the rate at which the distance from the origin changes.",
   "scoring_consequence": "The interpretation is wrong, and the chain rule part built on it reports the wrong quantity.",
   "wrong_step": {
    "text": "The speed along the curve: \\(\\sqrt{r^2+(dr/d\\theta)^2}\\approx6.843\\)",
    "expr": "6.843"
   },
   "right_step": {
    "text": "The rate of the distance from the origin: \\(dr/d\\theta\\approx1.695\\)",
    "expr": "1.695"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-09029"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-09030",
   "observed_behavior": "The rate at which the distance from the origin changes with time is reported as dr/dtheta alone.",
   "scoring_consequence": "The chain rule point is lost (sg-25:10).",
   "wrong_step": {
    "text": "\\(\\frac{dr}{dt}=\\frac{dr}{d\\theta}\\approx-5.913\\)",
    "expr": "-5.913"
   },
   "right_step": {
    "text": "\\(\\frac{dr}{dt}=\\frac{dr}{d\\theta}\\cdot\\frac{d\\theta}{dt}\\approx-8.869\\)",
    "expr": "-8.869"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-09030"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-09023",
   "observed_behavior": "Trigonometric values throughout a question are computed in degree measure, producing internally consistent but wrong numbers.",
   "scoring_consequence": "The response does not earn the first point it would otherwise have earned and is generally eligible for the rest (sg-23:6, sg-23:7).",
   "wrong_step": {
    "text": "Degree mode: \\(dr/d\\theta\\approx0.188\\)",
    "expr": "0.188"
   },
   "right_step": {
    "text": "Radian mode: \\(dr/d\\theta\\approx1.695\\)",
    "expr": "1.695"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-09023"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(r(0.9)\\) is a value, \\(r'\\) a rate."
  },
  {
   "prq_id": "BC-PRQ-09003",
   "text": "Keep the calculator in radian mode."
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
   "archetype_id": "BC-QA-09009",
   "parameter_draw": {
    "constant": 4,
    "coefficient": 3,
    "frequency": 2,
    "trig": "sin",
    "angle": "9/10",
    "framing": "distance"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For \\(r=4+3\\theta\\sin 2\\theta\\), \\(\\frac{dr}{d\\theta}=3\\sin 2\\theta+6\\theta\\cos 2\\theta\\). Using a calculator, find its value at \\(\\theta=0.9\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "1.695"
   },
   "steps": [
    {
     "text": "The derivative.",
     "expr": "6*theta*cos(2*theta) + 3*sin(2*theta)",
     "relation": "new"
    },
    {
     "text": "Radian mode.",
     "expr": "1.695",
     "relation": "evaluate",
     "subs": {
      "theta": "9/10"
     },
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09030"
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
   "archetype_id": "BC-QA-09009",
   "parameter_draw": {
    "constant": 3,
    "coefficient": 2,
    "frequency": 1,
    "trig": "cos",
    "angle": "4/5",
    "framing": "bare"
   },
   "stem": {
    "text": "A curve is \\(r=3+2\\theta\\cos\\theta\\). Using a calculator, find \\(\\frac{dr}{d\\theta}\\) at \\(\\theta=0.8\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "0.246"
   },
   "steps": [
    {
     "text": "The radius.",
     "expr": "3 + 2*theta*cos(theta)",
     "relation": "new"
    },
    {
     "text": "Product rule.",
     "expr": "-2*theta*sin(theta) + 2*cos(theta)",
     "relation": "differentiate",
     "variable": "theta"
    },
    {
     "text": "Radian mode.",
     "expr": "0.246",
     "relation": "evaluate",
     "subs": {
      "theta": "4/5"
     },
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09030"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-09010",
   "parameter_draw": {
    "constant": 5,
    "amplitude": 2,
    "frequency": 3,
    "trig": "sin",
    "angle": "9/10",
    "angle_rate": "2",
    "rate_form": "constant"
   },
   "stem": {
    "text": "A particle moves along \\(r=5+2\\sin 3\\theta\\) with \\(\\frac{d\\theta}{dt}=2\\). Using a calculator, find the rate at which its distance from the origin changes with respect to time when \\(\\theta=0.9\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-10.849"
   },
   "steps": [
    {
     "text": "The radius.",
     "expr": "5 + 2*sin(3*theta)",
     "relation": "new"
    },
    {
     "text": "Chain rule.",
     "expr": "6*cos(3*theta)",
     "relation": "differentiate",
     "variable": "theta"
    },
    {
     "text": "Times the angular rate.",
     "expr": "(6*cos(3*theta))*2",
     "relation": "new"
    },
    {
     "text": "Radian mode.",
     "expr": "-10.849",
     "relation": "evaluate",
     "subs": {
      "theta": "9/10"
     },
     "approx": true
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "-5.424",
     "error_path": "BC-ERR-09030",
     "derivation": "the angular rate left out, so dr/dtheta alone"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "0.209",
     "error_path": "BC-ERR-09023",
     "derivation": "the derivative evaluated with the calculator in degree mode"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "-10.849",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "15.963",
     "error_path": "BC-ERR-09029",
     "derivation": "the speed along the curve, the root of r squared plus dr/dtheta squared, times the angular rate"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09032"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-13 on BC-SKL-09030 to 09032; not promoted, the orientation states what a response shows and asks for no reading",
   "sources": [
    "BC-SKL-09030",
    "BC-SKL-09031",
    "BC-SKL-09032"
   ],
   "spec": {
    "kind": "diagram",
    "representations": [
     "BC-REP-13"
    ],
    "curve": {
     "polar": "4 + 3*theta*sin(2*theta)",
     "theta_range": [
      0,
      1.6
     ]
    },
    "point": {
     "theta": 0.9
    },
    "labels": [
     {
      "text": "r",
      "placement": "inside"
     },
     {
      "text": "theta = 0.9",
      "placement": "inside"
     },
     {
      "text": "distance from the origin",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same polar curve static with the ray at theta = 0.9 and r labelled",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 4 promoted: BC-REP-13 on BC-SKL-09031, and BC-QA-09009 `common_givens` name an angle and `difficulty_variables` name whether the reading as a rate of distance from the origin is demanded; one control, the angle",
   "sources": [
    "BC-SKL-09031",
    "BC-QA-09009"
   ],
   "spec": {
    "kind": "diagram",
    "representations": [
     "BC-REP-13",
     "BC-REP-04"
    ],
    "curve": {
     "polar": "4 + 3*theta*sin(2*theta)",
     "theta_range": [
      0,
      1.6
     ]
    },
    "controls": [
     {
      "name": "theta",
      "type": "slider",
      "range": [
       0,
       1.6
      ],
      "step": 0.05
     }
    ],
    "readouts": [
     "r at the angle",
     "sign of dr/dtheta",
     "distance from the origin growing or shrinking"
    ],
    "reading": "As the angle increases here, is the distance from the origin growing or shrinking, and what does that say about the sign of dr/dtheta?",
    "labels": [
     {
      "text": "r",
      "placement": "inside"
     },
     {
      "text": "dr/dtheta > 0",
      "placement": "inside"
     },
     {
      "text": "dr/dtheta < 0",
      "placement": "inside"
     }
    ]
   },
   "fallback": "three static frames (theta = 0.3, 0.9, 1.4), each with r, the sign of dr/dtheta and growing or shrinking",
   "keyboard": "Left and Right arrows move theta by 0.05, Shift with an arrow by 0.2; the readouts are announced on each change"
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a differentiation rule and a notation habit; the skill's BC-REP-13 figure is on ki-1",
   "sources": [
    "BC-SKL-09030"
   ]
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
   "block": "err-BC-ERR-09028",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09029",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09030",
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
  "err-BC-ERR-09028",
  "err-BC-ERR-09029",
  "err-BC-ERR-09030",
  "err-BC-ERR-09023",
  "ex-1"
 ],
 "read_minutes": {
  "full": 5.5,
  "brief": 2.8
 },
 "word_count": {
  "full": 816,
  "brief": 413
 },
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "the rate at which its distance from the origin changes with time is dr/dtheta multiplied by dtheta/dt"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the derivative and the value, and on the rate in time the product, and holds the recognition of r as the distance.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "ex-1 tags no point type, because the prediction, contrast pair and a reader line of 78 or more words do not fit the brief cap; ex-2 tags BC-PT-99049 and BC-PT-99004.",
   "settles": "A brief cap that admits a reader line."
  },
  {
   "claim": "Every non-text delivery mode chosen here is a proposal.",
   "settles": "The modality A/B on skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-09013",
  "BC-SKL-09030",
  "BC-SKL-09031",
  "BC-SKL-09032",
  "BC-EK-FUN-3G1",
  "BC-EK-FUN-3G2",
  "ced:177",
  "BC-QA-09009",
  "BC-QA-09010",
  "BC-PT-99049",
  "BC-PT-99004",
  "BC-ERR-09028",
  "BC-ERR-09029",
  "BC-ERR-09030",
  "BC-ERR-09023",
  "BC-MIS-09014",
  "BC-PRQ-06005",
  "BC-PRQ-09003",
  "sg-25:7",
  "sg-25:10",
  "research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form",
  "research/question-analysis/question-archetypes.md#BC-QA-09009 Derivative of r with respect to theta on a polar curve",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
